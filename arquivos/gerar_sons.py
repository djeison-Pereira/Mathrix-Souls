"""Gera os efeitos sonoros do Mathrix Souls por síntese (só NumPy, sem baixar nada).

Uso (dentro de arquivos):
    python gerar_sons.py                 -> gera todos em audios/sons
    python gerar_sons.py trovao fogo     -> gera só esses
    python gerar_sons.py --lista         -> lista os nomes
    python gerar_sons.py --forcar        -> sobrescreve os que já existem (cuidado: apaga sons reais trocados à mão)

Cada efeito vira audios/sons/<nome>.wav (16 bits, 22050 Hz). Os que têm lado
(golpe_esquerda, garra_direita...) saem em estéreo; os outros, em mono.
O resultado é determinístico (semente fixa): rodar de novo gera os mesmos arquivos.
"""
import os
import sys
import wave

import numpy as np

SR = 22050
rng = np.random.default_rng(7)
EFEITOS = {}


# ---------------------------------------------------------------- ferramentas
def T(d):
    return np.arange(int(d * SR)) / SR


def E(d, tau):
    """Envelope exponencial decrescente."""
    return np.exp(-T(d) / tau)


def bump(d, c, w):
    """Pico suave centrado em c segundos, com largura w."""
    return np.exp(-(((T(d) - c) / w) ** 2))


def fft_filter(x, lo=None, hi=None):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.ones_like(f)
    if lo:
        m *= 1 / (1 + (lo / np.maximum(f, 1e-9)) ** 4)
    if hi:
        m *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * m, len(x))


def nz(d, lo=None, hi=None):
    """Ruído filtrado, normalizado (desvio padrão 1)."""
    x = fft_filter(rng.standard_normal(int(d * SR)), lo, hi)
    return x / (x.std() + 1e-12)


def lfo(d, rate, lo=0.0, hi=1.0):
    """Modulação lenta e aleatória entre lo e hi."""
    n = int(d * SR)
    k = max(2, int(d * rate) + 2)
    pts = rng.uniform(lo, hi, k)
    return np.interp(np.linspace(0, k - 1, n), np.arange(k), pts)


def glide(f0, f1, d):
    return np.linspace(f0, f1, int(d * SR))


def osc(f, d, kind="sin"):
    n = int(d * SR)
    if np.ndim(f) == 0:
        f = np.full(n, float(f))
    else:
        f = np.interp(np.linspace(0, len(f) - 1, n), np.arange(len(f)), f)
    ph = np.cumsum(f) / SR
    if kind == "saw":
        return 2 * (ph % 1) - 1
    if kind == "sq":
        return np.sign(np.sin(2 * np.pi * ph))
    return np.sin(2 * np.pi * ph)


BELL = ((1, 1.0), (2.76, 0.6), (5.4, 0.35), (8.93, 0.2))
GLASS = ((1, 1.0), (2.32, 0.5), (4.25, 0.3), (6.63, 0.15))
COIN = ((1, 1.0), (1.51, 0.7), (2.4, 0.4))


def ping(f, d, tau, parts=((1, 1.0),)):
    t = T(d)
    x = sum(a * np.sin(2 * np.pi * f * r * t) for r, a in parts)
    return x * np.exp(-t / tau) * np.minimum(1, t / 0.001)


def sweep(d, f0, f1, k=8, larg=1.4):
    """Ruído de banda que varre de f0 a f1 (vento passando, 'whoosh')."""
    out = np.zeros(int(d * SR))
    for i in range(k):
        c = f0 * (f1 / f0) ** (i / (k - 1))
        out += nz(d, c / larg, c * larg) * bump(d, d * i / (k - 1), d / k)
    return out


def crackle(d, por_seg=40, lo=1200):
    """Estalidos aleatórios (fogo, lareira, pedrinhas)."""
    n = int(d * SR)
    imp = np.zeros(n)
    idx = rng.integers(0, n, max(1, int(d * por_seg)))
    imp[idx] = rng.uniform(0.2, 1, len(idx)) ** 2
    ker = nz(0.006, lo) * np.exp(-np.arange(int(0.006 * SR)) / (0.0012 * SR))
    return np.convolve(imp, ker)[:n]


def mix(*xs):
    n = max(len(x) for x in xs)
    out = np.zeros(n)
    for x in xs:
        out[: len(x)] += x
    return out


def thud(f0=110, d=0.3, tau=0.06, g=1.0):
    return g * (osc(glide(f0, f0 * 0.4, d), d) * E(d, tau) + 0.5 * fft_filter(nz(d), None, 1200) * E(d, tau * 0.4))


def _passo(g=1.0):
    return thud(95, 0.22, 0.05, g)


def creak(d, f0, f1, g=1.0):
    f = glide(f0, f1, d) * (1 + 0.04 * lfo(d, 30, -1, 1))
    x = fft_filter(osc(f, d, "saw"), 300, 2500) * (0.4 + 0.6 * lfo(d, 22, 0, 1))
    return g * x * np.minimum(1, T(d) / 0.05) * np.minimum(1, (d - T(d)) / 0.08)


def roar(d, f0=85, f1=None, g=1.0):
    f1 = f1 or f0
    f = glide(f0, f1, d) * (1 + 0.05 * lfo(d, 10, -1, 1))
    t = T(d)
    base = fft_filter(osc(f, d, "saw"), 60, 1400) * (1 + 0.8 * np.sin(2 * np.pi * 32 * t))
    ar = nz(d, 150, 3000) * 0.5 * lfo(d, 14, 0.3, 1)
    env = np.minimum(1, t / 0.15) * np.minimum(1, (d - t) / 0.25)
    return g * (base + ar) * env


class Buf:
    def __init__(s, d):
        s.n = int(d * SR)
        s.L = np.zeros(s.n)
        s.R = np.zeros(s.n)
        s.st = False

    def put(s, x, t0=0.0, g=1.0, pan=0.0):
        i = int(t0 * SR)
        if i >= s.n or i < 0:
            return s
        x = np.asarray(x)[: s.n - i] * g
        if pan != 0:
            s.st = True
        s.L[i:i + len(x)] += x * (1 - max(0.0, pan))
        s.R[i:i + len(x)] += x * (1 + min(0.0, pan))
        return s

    def reverb(s, t60=0.8, w=0.25):
        def ir():
            n = int(t60 * SR)
            r = fft_filter(rng.standard_normal(n), None, 5000) * np.exp(-6.9 * T(t60) / t60)
            return r / np.sqrt(np.sum(r ** 2))

        def conv(x, r):
            n = len(x) + len(r)
            return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(r, n), n)[: len(x)]

        a = ir()
        s.L = (1 - w) * s.L + w * conv(s.L, a)
        s.R = (1 - w) * s.R + w * conv(s.R, ir() if s.st else a)
        return s

    def saida(s, pico=0.8):
        x = np.stack([s.L, s.R], 1) if s.st else s.L
        x = x / (np.max(np.abs(x)) + 1e-9) * pico
        f = int(0.03 * SR)
        r = np.linspace(1, 0, f)
        if s.st:
            x[-f:] *= r[:, None]
        else:
            x[-f:] *= r
        return x


def efeito(pico=0.8):
    def deco(fn):
        EFEITOS[fn.__name__] = (fn, pico)
        return fn
    return deco


def salvar(caminho, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(caminho, "wb") as w:
        w.setnchannels(1 if pcm.ndim == 1 else 2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


# ------------------------------------------------------------- sons reutilizáveis
def vento(d, lo=150, hi=900, rate=0.6, g=1.0):
    return g * nz(d, lo, hi) * (0.25 + 0.75 * lfo(d, rate, 0, 1))


def ondas(d, rate=0.25, g=1.0):
    sw = lfo(d, rate, 0.1, 1) ** 2
    return g * (nz(d, None, 900) * sw + 0.35 * nz(d, 1500, 5000) * sw ** 2)


def gaivota(d=0.7):
    u = np.linspace(0, 1, int(d * SR))
    f = 2700 - 1300 * u + 250 * np.sin(2 * np.pi * 16 * u * d)
    return fft_filter(osc(f, d, "saw"), 900, 5000) * np.sin(np.pi * u) ** 0.5


def passaro(d=0.09):
    f = glide(3000, 5200, d) * (1 + 0.04 * np.sin(2 * np.pi * 45 * T(d)))
    return osc(f, d) * np.sin(np.pi * np.linspace(0, 1, int(d * SR)))


def murmurio(d, vozes=6, g=1.0):
    b = Buf(d)
    for _ in range(vozes):
        f = rng.uniform(95, 190)
        x = fft_filter(osc(f * (1 + 0.1 * lfo(d, 4, -1, 1)), d, "saw"), 400, 1800) * lfo(d, 5, 0, 1) ** 2
        b.put(x, 0, 1.0)
    return g * b.L / (b.L.std() + 1e-9)


# ---------------------------------------------------------------------- efeitos
@efeito()
def dano():
    b = Buf(0.4)
    return b.put(thud(180, 0.4, 0.07) + 0.3 * nz(0.4, 800, 5000) * E(0.4, 0.01)).saida()


@efeito()
def magia():
    d = 1.5
    b = Buf(d)
    t = T(d)
    b.put(osc(glide(300, 1200, d), d) * (1 + 0.4 * np.sin(2 * np.pi * 7 * t)) * bump(d, 0.7, 0.4), 0, 0.5)
    for f in (523, 659, 784):
        b.put(np.sin(2 * np.pi * f * t) * bump(d, 0.8, 0.45), 0, 0.2)
    for t0 in np.sort(rng.uniform(0.1, 1.0, 14)):
        b.put(ping(rng.choice([1319, 1568, 1976, 2349, 3136]), 0.5, 0.15), t0, 0.25)
    return b.reverb(0.8, 0.25).saida()


@efeito()
def galo_vento():
    d = 3.5
    b = Buf(d)
    b.put(vento(d, 200, 900, 0.5), 0, 0.5)
    b.put(nz(d, 2500, 6000) * lfo(d, 3, 0, 1) ** 3, 0, 0.12)
    t0 = 0.4
    for f0, f1, dur in ((520, 700, 0.16), (620, 560, 0.12), (780, 1350, 0.22), (1250, 850, 0.7)):
        f = glide(f0, f1, dur) * (1 + 0.03 * np.sin(2 * np.pi * 24 * T(dur)))
        x = fft_filter(osc(f, dur, "saw"), 500, 3500)
        x *= np.minimum(1, T(dur) / 0.02) * np.minimum(1, (dur - T(dur)) / 0.06)
        b.put(x, t0, 0.35)
        t0 += dur + 0.03
    return b.reverb(1.2, 0.35).saida(0.7)


@efeito(0.6)
def vento_janela():
    """Sopro curto de vento (sem grave, para não parecer trovão), antes de o Narrador falar."""
    d = 2.2
    b = Buf(d)
    t = T(d)
    amp = np.sin(np.pi * t / d) ** 2                       # sobe e desce suave
    b.put(sweep(d, 700, 2200, 8, 1.7) * amp, 0, 1.0)       # o ar passando
    apito = osc(950 + 220 * np.sin(2 * np.pi * 0.9 * t), d)
    b.put(fft_filter(apito, 500, 2500) * amp ** 2, 0, 0.10)   # assobio fraco na janela
    b.L = fft_filter(b.L, 350, None)                       # corta o grave
    return b.saida(0.6)


@efeito()
def porta():
    b = Buf(1.6)
    b.put(creak(1.2, 110, 190), 0, 1.0)
    b.put(thud(70, 0.3, 0.08), 1.25, 0.8)
    return b.reverb(0.5, 0.15).saida()


@efeito()
def taverna():
    d = 4.0
    b = Buf(d)
    b.put(murmurio(d), 0, 0.7)
    b.put(crackle(d, 45, 800), 0, 0.5)
    for t0 in np.sort(rng.uniform(0.2, 3.6, 6)):
        b.put(ping(rng.uniform(2200, 3500), 0.2, 0.05, GLASS), t0, 0.25)
    for t0 in (0.9, 2.4):
        b.put(thud(160, 0.15, 0.03), t0, 0.5)
    return b.reverb(0.6, 0.2).saida(0.7)


@efeito()
def frascos():
    d = 2.2
    b = Buf(d)
    for t0 in np.sort(rng.uniform(0, 1.6, 10)):
        b.put(ping(rng.uniform(1800, 5200), 0.6, rng.uniform(0.05, 0.14), GLASS), t0, rng.uniform(0.25, 0.7))
    return b.reverb(0.5, 0.2).saida(0.7)


@efeito()
def teleporte():
    d = 1.4
    b = Buf(d)
    b.put(nz(0.1, 1500, 9000) * E(0.1, 0.01), 0.0, 1.0)
    b.put(thud(900, 0.03, 0.006), 0.0, 0.6)
    b.put(sweep(1.0, 300, 3500), 0.2, 0.7)
    b.put(sweep(0.5, 3500, 600), 0.9, 0.3)
    return b.reverb(0.6, 0.2).saida(0.75)


@efeito()
def cajado_sino():
    d = 3.5
    b = Buf(d)
    b.put(thud(85, 0.25, 0.05), 0, 1.0)
    b.put(nz(0.05, 500, 4000) * E(0.05, 0.01), 0, 0.6)
    b.put(ping(110, d - 0.05, 1.4, BELL), 0.05, 0.9)
    return b.reverb(1.5, 0.35).saida()


@efeito()
def grilo():
    d = 1.8
    b = Buf(d)
    for g in range(3):
        for p in range(5):
            t = T(0.03)
            pulso = np.sin(2 * np.pi * 4800 * t) * np.sin(np.pi * t / 0.03) ** 2
            b.put(pulso, 0.15 + g * 0.55 + p * 0.045, 0.7, pan=-0.8)
    return b.reverb(0.4, 0.1).saida(0.6)


@efeito(0.55)
def passo():
    d = 1.0
    b = Buf(d)
    for t0 in (0.05, 0.55):
        b.put(_passo(0.9), t0)
        b.put(nz(0.18, 1500, 6000) * lfo(0.18, 40, 0, 1) ** 2 * E(0.18, 0.08), t0, 0.5)
    return b.saida(0.55)


@efeito()
def bifurcacao():
    d = 3.5
    b = Buf(d)
    b.put(nz(d, 1200, 5000) * (0.3 + 0.7 * lfo(d, 18, 0, 1)), 0, 0.35, pan=-0.9)
    for t0 in np.sort(rng.uniform(0, 3.0, 12)):
        for k in range(rng.integers(1, 4)):
            b.put(passaro(), t0 + k * 0.11, 0.25, pan=-0.7)
    b.put(vento(d, 150, 700, 0.4), 0, 0.7, pan=0.9)
    return b.reverb(0.5, 0.1).saida(0.7)


@efeito()
def vento_seco():
    d = 2.8
    b = Buf(d)
    b.put(vento(d, 250, 1400, 0.7), 0, 1.0)
    b.put(nz(d, 1200, 2200) * lfo(d, 1.2, 0, 1) ** 4, 0, 0.3)
    return b.saida(0.6)


@efeito()
def desmoronamento():
    d = 2.4
    b = Buf(d)
    b.put(nz(d, 30, 250) * E(d, 0.9) * np.minimum(1, T(d) / 0.2), 0, 1.0)
    b.put(crackle(d, 90, 400) * E(d, 1.0), 0, 1.5)
    for t0 in np.sort(rng.uniform(0.1, 1.6, 6)):
        b.put(thud(rng.uniform(60, 120), 0.25, 0.05), t0, rng.uniform(0.3, 0.7))
    return b.reverb(0.6, 0.2).saida()


def _golpe(pan, d=1.3):
    b = Buf(d)
    for k in range(4):
        b.put(_passo(0.8), 0.05 + k * 0.13, 0.5 + 0.15 * k, pan=pan)
    t = T(0.45)
    f = glide(520, 260, 0.45) * (1 + 0.04 * np.sin(2 * np.pi * 9 * t))
    grito = fft_filter(osc(f, 0.45, "saw"), 400, 2800) * np.minimum(1, t / 0.03) * np.minimum(1, (0.45 - t) / 0.12)
    b.put(grito, 0.55, 0.7, pan=pan)
    b.put(thud(130, 0.3, 0.06), 0.62, 0.7, pan=pan)
    return b.reverb(0.4, 0.12).saida()


@efeito()
def golpe_esquerda():
    return _golpe(-1.0)


@efeito()
def golpe_direita():
    return _golpe(1.0)


@efeito()
def golpe_frente():
    return _golpe(0.0)


def _garra(pan, d=1.3):
    b = Buf(d)
    for k in range(3):
        b.put(fft_filter(nz(0.2), 80, 500) * bump(0.2, 0.1, 0.06), 0.05 + k * 0.22, 0.9, pan=pan)
    b.put(sweep(0.3, 400, 3000), 0.7, 0.4, pan=pan)
    b.put(nz(0.35, 2500, 9000) * E(0.35, 0.07), 0.85, 0.7, pan=pan)
    b.put(thud(100, 0.2, 0.04), 0.88, 0.5, pan=pan)
    return b.reverb(0.4, 0.12).saida()


@efeito()
def garra_esquerda():
    return _garra(-1.0)


@efeito()
def garra_direita():
    return _garra(1.0)


@efeito()
def garra_frente():
    return _garra(0.0)


@efeito()
def esquiva():
    b = Buf(0.6)
    return b.put(sweep(0.5, 500, 5000)).saida(0.7)


@efeito()
def goblin_risada():
    d = 1.9
    b = Buf(d)
    for i in range(9):
        dur = 0.1
        f = glide(780 - i * 20 + rng.uniform(-30, 30), 520 - i * 15, dur)
        x = fft_filter(osc(f, dur, "saw"), 700, 3200) * np.sin(np.pi * np.linspace(0, 1, int(dur * SR))) ** 0.7
        b.put(x, 0.1 + i * 0.15, 0.7, pan=float(np.sin(2 * np.pi * i / 6)))
    return b.reverb(0.5, 0.2).saida(0.7)


@efeito()
def goblin_foge():
    d = 2.0
    b = Buf(d)
    t0, gap, g = 0.0, 0.2, 1.0
    while t0 < d - 0.2:
        b.put(_passo(g), t0, 0.7)
        b.put(nz(0.15, 1500, 6000) * lfo(0.15, 40, 0, 1) ** 2 * E(0.15, 0.06), t0, g * 0.6)
        t0 += gap
        gap *= 0.96
        g *= 0.82
    return b.saida(0.7)


@efeito()
def praia():
    d = 4.5
    b = Buf(d)
    b.put(ondas(d, 0.3), 0, 1.0)
    for t0 in (0.7, 2.2, 3.4):
        b.put(gaivota(rng.uniform(0.5, 0.8)), t0, 0.18)
    return b.reverb(0.5, 0.1).saida(0.7)


@efeito()
def trovao():
    d = 3.2
    b = Buf(d)
    b.put(nz(0.3, 800) * E(0.3, 0.05), 0, 1.0)
    b.put(nz(d, 30, 300) * E(d, 0.9) * (0.5 + 0.5 * lfo(d, 6, 0, 1)) * np.minimum(1, T(d) / 0.1), 0.05, 1.2)
    return b.reverb(1.4, 0.35).saida()


@efeito()
def barco():
    d = 2.8
    b = Buf(d)
    b.put(nz(1.2, 150, 1400) * lfo(1.2, 8, 0.2, 1) * np.minimum(1, (1.2 - T(1.2)) / 0.3), 0, 0.8)
    for t0 in (1.3, 2.0):
        b.put(creak(0.5, 140, 210), t0, 0.8)
    b.put(ondas(d, 0.5), 0, 0.2)
    return b.reverb(0.4, 0.1).saida(0.7)


@efeito()
def tempestade():
    d = 4.5
    b = Buf(d)
    b.put(vento(d, 100, 1500, 0.9), 0, 1.0)
    b.put(nz(d, 800, 2500) * lfo(d, 1.5, 0, 1) ** 3, 0, 0.35)
    for t0 in np.sort(rng.uniform(0.3, 4.0, 6)):
        b.put(nz(0.5, None, 500) * E(0.5, 0.12), t0, 0.7)
        b.put(thud(70, 0.3, 0.08), t0, 0.5)
    return b.reverb(0.6, 0.15).saida()


@efeito()
def calmaria():
    d = 3.0
    b = Buf(d)
    b.put(vento(d, 150, 800, 0.4) * E(d, 1.0), 0, 0.8)
    b.put(ondas(d, 0.25), 0, 0.25 * 1.0)
    return b.saida(0.5)


@efeito()
def porta_pedra():
    d = 3.2
    b = Buf(d)
    t = T(d)
    rasp = nz(d, 70, 700) * lfo(d, 9, 0.3, 1) + 0.6 * fft_filter(osc(55 + 8 * lfo(d, 5), d, "saw"), 40, 400)
    b.put(rasp * np.minimum(1, t / 0.1) * np.minimum(1, (2.6 - t).clip(0) / 0.3), 0, 0.9)
    b.put(thud(50, 0.5, 0.15), 2.7, 1.4)
    return b.reverb(1.0, 0.3).saida()


@efeito()
def farol():
    d = 4.5
    b = Buf(d)
    b.put(vento(d, 150, 800, 0.4), 0, 0.5)
    b.put(ondas(d, 0.2), 0, 0.3)
    for t0 in np.arange(0.2, d - 0.3, 0.33):
        b.put(nz(0.015, 1500, 6000) * E(0.015, 0.004), t0, 0.5)
        b.put(ping(420, 0.18, 0.04, BELL), t0, 0.07)
    b.put(osc(70, d), 0, 0.1)
    return b.reverb(0.8, 0.2).saida(0.6)


@efeito()
def masmorra():
    d = 3.8
    b = Buf(d)
    b.put(creak(1.6, 70, 125, 1.2), 0, 1.0)
    b.put(thud(45, 0.5, 0.15), 1.6, 1.2)
    for t0 in (2.1, 2.9, 3.4):
        b.put(osc(glide(1800, 700, 0.07), 0.07) * E(0.07, 0.02), t0, 0.5)
    b.put(vento(d, 40, 200, 0.3), 0, 0.3)
    return b.reverb(1.6, 0.4).saida()


@efeito()
def corredores():
    d = 3.0
    b = Buf(d)
    for t0 in np.sort(rng.uniform(0.1, 2.3, 9)):
        b.put(mix(ping(rng.uniform(2500, 4800), 0.15, 0.03, GLASS), nz(0.08, 2000, 9000) * E(0.08, 0.015)), t0, 0.35, pan=-0.9)
    for t0 in (0.3, 1.2, 2.1):
        b.put(thud(70, 0.35, 0.09), t0, 1.0, pan=0.9)
    return b.reverb(1.0, 0.3).saida(0.75)


@efeito()
def armadura():
    d = 1.8
    b = Buf(d)
    for t0 in np.sort(rng.uniform(0.0, 1.0, 12)):
        b.put(mix(ping(rng.uniform(2000, 5500), 0.2, 0.04, GLASS), nz(0.05, 3000, 10000) * E(0.05, 0.01)), t0, rng.uniform(0.2, 0.5))
    b.put(creak(0.7, 160, 240), 0.1, 0.25)
    return b.reverb(0.9, 0.3).saida(0.7)


@efeito()
def banquete():
    d = 3.0
    b = Buf(d)
    b.put(murmurio(d, 4), 0, 0.3)
    for t0 in np.sort(rng.uniform(0.05, 2.5, 14)):
        b.put(ping(rng.uniform(1100, 3200), 0.25, 0.04, GLASS), t0, rng.uniform(0.2, 0.5))
    for t0 in (0.5, 1.7):
        b.put(thud(200, 0.12, 0.025), t0, 0.4)
    return b.reverb(0.6, 0.2).saida(0.7)


@efeito()
def espelho():
    d = 3.0
    b = Buf(d)
    t = T(d)
    x = (np.sin(2 * np.pi * 1200 * t) + np.sin(2 * np.pi * 1207 * t) + 0.5 * np.sin(2 * np.pi * 2790 * t))
    b.put(x * (1 + 0.5 * np.sin(2 * np.pi * 6 * t)) * np.minimum(1, t / 0.2) * np.exp(-t / 1.3), 0, 0.5)
    for t0 in np.sort(rng.uniform(0.1, 1.5, 8)):
        b.put(ping(rng.uniform(2500, 6000), 0.5, 0.12, GLASS), t0, 0.2)
    return b.reverb(1.2, 0.3).saida(0.7)


@efeito()
def abismo():
    d = 3.0
    b = Buf(d)
    t = T(d)
    amp = np.minimum(1, t / 1.5) * np.minimum(1, (d - t) / 0.6)
    b.put(sweep(d, 150, 900) * amp, 0, 1.0)
    b.put(osc(95 * (1 + 0.03 * np.sin(2 * np.pi * 0.7 * t)), d) * amp, 0, 0.5)
    return b.reverb(1.0, 0.3).saida(0.7)


@efeito(0.6)
def pedra_firme():
    b = Buf(0.5)
    b.put(thud(90, 0.3, 0.07)).put(nz(0.06, 1500, 6000) * E(0.06, 0.012), 0, 0.3)
    return b.reverb(0.3, 0.1).saida(0.6)


@efeito()
def pedra_afunda():
    d = 1.6
    b = Buf(d)
    t = T(d)
    b.put(nz(0.9, 60, 500) * lfo(0.9, 14, 0.2, 1), 0, 0.9)
    b.put(osc(glide(90, 40, 0.9), 0.9) * np.minimum(1, (0.9 - T(0.9)) / 0.1), 0, 0.6)
    b.put(crackle(0.9, 70, 1500), 0.5, 0.8)
    b.put(thud(50, 0.4, 0.1), 0.95, 1.0)
    return b.reverb(0.6, 0.2).saida()


@efeito()
def golem():
    d = 3.5
    b = Buf(d)
    t = T(d)
    b.put(nz(d, 25, 90) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t)), 0, 1.0)
    b.put(nz(d, 100, 900) * lfo(d, 10, 0, 1) ** 2, 0, 0.5)
    for t0 in (0.3, 1.3, 2.3):
        b.put(thud(55, 0.5, 0.12), t0, 1.2)
        b.put(crackle(0.5, 80, 800), t0, 0.6)
    return b.reverb(1.2, 0.3).saida()


@efeito()
def golem_poeira():
    d = 2.8
    b = Buf(d)
    b.put(crackle(2.0, 120, 600) * E(2.0, 0.7), 0, 1.5)
    b.put(nz(d, 2000, 8000) * np.minimum(1, T(d) / 0.8) * E(d, 1.1), 0, 0.3)
    b.put(nz(d, 40, 250) * E(d, 0.6), 0, 0.6)
    return b.reverb(0.8, 0.25).saida(0.7)


@efeito()
def fogo():
    d = 2.8
    b = Buf(d)
    b.put(roar(1.9, 95, 70), 0.0, 1.0)
    b.put(crackle(d, 70, 1500), 0, 0.5)
    b.put(nz(d, 2000, 8000) * bump(d, 1.0, 0.8), 0, 0.2)
    return b.reverb(0.9, 0.25).saida()


@efeito()
def fogo_apaga():
    d = 1.8
    b = Buf(d)
    b.put(crackle(d, 70, 1500) * E(d, 0.6), 0, 0.8)
    b.put(nz(d, 3000, 9000) * E(d, 0.5), 0, 0.4)
    b.put(sweep(d, 1200, 400), 0, 0.2)
    return b.saida(0.7)


@efeito()
def queimadura():
    d = 1.0
    b = Buf(d)
    b.put(sweep(0.4, 300, 2500), 0, 0.8)
    b.put(nz(d, 3000, 9000) * E(d, 0.25), 0.05, 0.5)
    b.put(crackle(d, 90, 1500) * E(d, 0.4), 0, 0.8)
    return b.saida(0.8)


@efeito()
def dragao_respira():
    d = 3.5
    b = Buf(d)
    t = T(d)
    amp = np.sin(np.pi * t / d) ** 2
    b.put(nz(d, 100, 700) * amp, 0, 1.0)
    b.put(osc(42 + 5 * np.sin(2 * np.pi * 0.5 * t), d) * amp, 0, 0.8)
    b.put(nz(d, 30, 120) * (0.6 + 0.4 * np.sin(2 * np.pi * 5 * t)), 0, 0.8)
    return b.reverb(1.0, 0.3).saida()


@efeito()
def dragao_cai():
    d = 5.0
    b = Buf(d)
    b.put(roar(2.2, 100, 40), 0, 0.9)
    b.put(thud(45, 1.4, 0.35, 2.0), 2.3, 1.0)
    b.put(nz(1.5, 30, 200) * E(1.5, 0.5), 2.3, 1.0)
    b.put(crackle(1.8, 60, 500) * E(1.8, 0.6), 2.4, 1.0)
    return b.reverb(1.6, 0.35).saida()


@efeito()
def tesouro():
    d = 2.6
    b = Buf(d)
    for t0 in np.sort(rng.uniform(0, 1.8, 22)):
        b.put(ping(rng.uniform(2200, 6000), 0.5, rng.uniform(0.05, 0.2), COIN), t0, rng.uniform(0.2, 0.6))
    return b.reverb(0.6, 0.2).saida(0.7)


@efeito()
def mar_calmo():
    d = 4.5
    b = Buf(d)
    b.put(ondas(d, 0.2), 0, 0.8)
    for t0 in np.sort(rng.uniform(0.3, 3.8, 4)):
        b.put(nz(0.3, 200, 1500) * (lfo(0.3, 18, 0, 1) ** 2) * bump(0.3, 0.15, 0.1), t0, 0.5)
    return b.reverb(0.5, 0.1).saida(0.55)


@efeito()
def casa_de_cura():
    d = 2.6
    b = Buf(d)
    b.put(creak(0.7, 160, 230, 0.8), 0, 0.8)
    b.put(nz(0.03, 1500, 6000) * E(0.03, 0.006), 0.75, 0.7)
    b.put(ping(659, 1.5, 0.5, BELL), 0.9, 0.4)
    b.put(ping(880, 1.3, 0.5, BELL), 1.15, 0.4)
    return b.reverb(0.7, 0.2).saida(0.7)


@efeito()
def abertura():
    d = 5.0
    b = Buf(d)
    b.put(nz(0.3, None, 700) * E(0.3, 0.07), 0.0, 0.5)
    b.put(nz(d, 30, 250) * E(d, 1.1) * (0.5 + 0.5 * lfo(d, 5, 0, 1)), 0, 0.9)
    b.put(ping(98, d - 1.5, 1.6, BELL), 1.5, 1.0)
    return b.reverb(1.8, 0.4).saida()


@efeito(0.6)
def goblin_salta():
    """O goblin salta para o meio da trilha: folhas farfalhando, um 'whoosh' no ar e a aterrissagem."""
    d = 1.2
    b = Buf(d)
    b.put(nz(0.5, 2000, 7000) * bump(0.5, 0.28, 0.14) * lfo(0.5, 30, 0.2, 1) ** 2, 0.0, 0.5)   # folhas
    b.put(sweep(0.4, 500, 2600), 0.12, 0.45)                                                    # o salto no ar
    b.put(thud(120, 0.25, 0.05), 0.5, 0.9)                                                     # a aterrissagem
    b.put(nz(0.3, 1500, 6500) * E(0.3, 0.07) * lfo(0.3, 50, 0.3, 1), 0.5, 0.6)                   # folhas espalhadas
    return b.reverb(0.3, 0.1).saida(0.6)


@efeito(0.45)
def vez_do_jogador():
    b = Buf(0.3)
    b.put(np.sin(2 * np.pi * 660 * T(0.1)) * np.sin(np.pi * np.linspace(0, 1, int(0.1 * SR))), 0.0)
    b.put(np.sin(2 * np.pi * 880 * T(0.14)) * np.sin(np.pi * np.linspace(0, 1, int(0.14 * SR))), 0.1)
    return b.saida(0.45)


# ------------------------------------------------------------------------- main
if __name__ == "__main__":
    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audios", "sons")
    args = sys.argv[1:]
    if "--lista" in args:
        print("\n".join(sorted(EFEITOS)))
        sys.exit(0)
    forcar = "--forcar" in args
    nomes = [x for x in args if not x.startswith("--")] or sorted(EFEITOS)
    os.makedirs(pasta, exist_ok=True)
    for nome in nomes:
        if not forcar and os.path.exists(os.path.join(pasta, nome + ".wav")):
            print(f"{nome:20s} já existe (pulado; use --forcar para sobrescrever)")
            continue
        fn, _ = EFEITOS[nome]
        x = fn()
        salvar(os.path.join(pasta, nome + ".wav"), x)
        print(f"{nome:20s} {len(x) / SR:4.1f}s  {'estéreo' if x.ndim == 2 else 'mono'}")
    print(f"\n{len(nomes)} efeito(s) em {pasta}")
