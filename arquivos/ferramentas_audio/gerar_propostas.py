"""Revisão dos efeitos sintetizados (e dos que estão sem som): gera uma PROPOSTA nova para cada um,
ao lado do som VELHO, para a equipe comparar de ouvido. Não mexe em nada do jogo.

Uso (dentro de arquivos):
    python ferramentas_audio/gerar_propostas.py            -> gera todas as propostas
    python ferramentas_audio/gerar_propostas.py fogo grilo  -> só essas
    python ferramentas_audio/montar_indice.py               -> a página para ouvir lado a lado (depois de gerar todas)

Saída: ferramentas_audio/revisao/<nome>/velho.wav (o que está no jogo hoje, se houver) e proposta.wav.
Para levar uma proposta ao jogo, copie proposta.wav para audios/sons/<nome>.wav (veja o LEIA.md).

O que muda em relação ao gerar_sons.py (que usa seno + ruído para quase tudo):
- batidas por SÍNTESE MODAL: cada material tem as suas ressonâncias (madeira, pedra, metal, vidro, moeda, louça),
  com decaimentos diferentes e um pouco de variação a cada batida (duas batidas nunca soam iguais);
- rangidos por ATRITO: um trem de pequenos "trancos" irregulares excitando o corpo do objeto (é assim que madeira
  e metal rangem de verdade), em vez de uma onda dente-de-serra;
- folhas, pedrinhas, estalos de fogo e bolhas de riacho por GRÃOS (milhares de eventos curtos aleatórios);
- vento com FILTRO QUE SE MOVE (a rajada abre o som para o agudo) e assobio de banda estreita;
- vozes (goblin, dragão) por FORMANTES (as ressonâncias da garganta), não por dente-de-serra filtrado;
- lado esquerdo/direito com diferença de TEMPO entre os ouvidos e o ouvido de longe mais abafado (fica muito mais
  claro de onde vem o som no fone, o que importa para o jogador cego);
- onde existe gravação real em audios_originais (mar, floresta, taverna, porta com trinco), ela entra na mistura.
"""
import json
import os
import shutil
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.dirname(AQUI)
SAIDA = os.path.join(AQUI, "revisao")            # fora do jogo: só para comparar de ouvido
sys.path.insert(0, ARQ)
from masterizar_audios import ler, gravar  # noqa: E402

SR = 22050
ORIG = os.path.join(ARQ, "audios_originais")
SONS = os.path.join(ARQ, "audios", "sons")
rng = np.random.default_rng(2026)
PROPOSTAS = {}


def proposta(nota, alvo_db=None):
    def deco(fn):
        PROPOSTAS[fn.__name__] = (fn, nota, alvo_db)
        return fn
    return deco


# ================================================================== ferramentas básicas
def n(d):
    return int(round(d * SR))


def T(d):
    return np.arange(n(d)) / SR


def filtro(x, lo=None, hi=None, ordem=2):
    if x.ndim == 2:
        return np.stack([filtro(x[:, c], lo, hi, ordem) for c in range(x.shape[1])], 1)
    X = np.fft.rfft(x)
    f = np.maximum(np.fft.rfftfreq(len(x), 1 / SR), 1e-3)
    m = np.ones_like(f)
    if lo:
        m /= np.sqrt(1 + (lo / f) ** (2 * ordem))
    if hi:
        m /= np.sqrt(1 + (f / hi) ** (2 * ordem))
    return np.fft.irfft(X * m, len(x))


def ruido(d, lo=None, hi=None):
    x = filtro(rng.standard_normal(n(d)), lo, hi)
    return x / (x.std() + 1e-12)


def conv(a, b):
    m = len(a) + len(b) - 1
    N = 1 << (m - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(a, N) * np.fft.rfft(b, N), N)[:m]


def suave(d, taxa, lo=0.0, hi=1.0):
    """Curva aleatória lenta e suave (interpolação cosseno entre pontos sorteados)."""
    k = int(d * taxa) + 3
    pts = rng.uniform(lo, hi, k)
    xs = np.linspace(0, k - 2.0001, n(d))
    i = np.floor(xs).astype(int)
    fr = (1 - np.cos(np.pi * (xs - i))) / 2
    return pts[i] * (1 - fr) + pts[i + 1] * fr


def ataque_queda(d, ataque, queda):
    t = T(d)
    return np.minimum(1, t / max(ataque, 1e-4)) * np.minimum(1, np.maximum(0, d - t) / max(queda, 1e-4))


def bump(d, c, w):
    return np.exp(-(((T(d) - c) / w) ** 2))


def soma(*xs):
    """Soma sons de durações diferentes (o resultado tem a duração do mais longo)."""
    out = np.zeros(max(len(x) for x in xs))
    for x in xs:
        out[: len(x)] += x
    return out


def norm(x):
    return x / (np.max(np.abs(x)) + 1e-12)


def rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(np.asarray(x, float) ** 2)) + 1e-12)


# ================================================================== síntese modal (batidas)
MADEIRA = dict(r=[1, 2.57, 4.1, 5.7, 7.4, 9.2], tau=[.06, .03, .02, .012, .008, .006], a=[1, .7, .5, .35, .25, .15])
PEDRA = dict(r=[1, 1.73, 2.9, 4.3, 6.1, 8.3, 10.7], tau=[.03, .02, .014, .01, .008, .006, .005], a=[1, .8, .7, .5, .4, .3, .2])
METAL = dict(r=[1, 2.76, 5.40, 8.93, 13.34], tau=[1.2, .8, .5, .35, .25], a=[1, .6, .45, .3, .2])
VIDRO = dict(r=[1, 2.32, 4.25, 6.63, 9.38], tau=[.9, .5, .3, .2, .12], a=[1, .5, .35, .2, .1])
MOEDA = dict(r=[1, 1.51, 2.40, 3.30, 4.6], tau=[.5, .35, .25, .18, .12], a=[1, .8, .6, .4, .25])
LOUCA = dict(r=[1, 1.59, 2.14, 2.9, 3.8], tau=[.15, .1, .07, .05, .04], a=[1, .7, .6, .4, .3])
SINO = dict(r=[0.5, 1, 1.19, 1.5, 2.0, 2.5, 3.0], tau=[1.6, 1.2, 1.0, .8, .6, .45, .35], a=[.5, 1, .6, .4, .35, .2, .15])


def modos(mat, f0, tau_mult=1.0, var=0.02):
    return [(f0 * r * (1 + rng.uniform(-var, var)), tau * tau_mult * rng.uniform(0.8, 1.2), a * rng.uniform(0.7, 1.0))
            for r, tau, a in zip(mat["r"], mat["tau"], mat["a"])]


def ir_modal(ms, d):
    t = T(d)
    x = np.zeros_like(t)
    for f, tau, a in ms:
        if f < SR * 0.45:
            x += a * np.exp(-t / tau) * np.sin(2 * np.pi * f * t + rng.uniform(0, 2 * np.pi))
    return x


def batida(mat, f0, tau_mult=1.0, excit_ms=1.0, clique=0.3, d=None):
    """Uma batida: um impulso curto (excit_ms; mais longo = batida mais macia) excita as ressonâncias do material."""
    ms = modos(mat, f0, tau_mult)
    d = d or min(3.0, max(tau for _, tau, _ in ms) * 6)
    k = max(2, n(excit_ms / 1000))
    ex = rng.standard_normal(k) * np.hanning(k)
    y = conv(ex, ir_modal(ms, d))[: n(d)]
    y[:k] += ex * clique * np.max(np.abs(y)) / (np.max(np.abs(ex)) + 1e-12)
    return norm(y)


def baque(f0=70, d=0.4, tau=0.08):
    """O peso de uma batida: um grave que cai de tom (o chão ou o corpo cedendo)."""
    t = T(d)
    f = f0 * (1 + 0.6 * np.exp(-t / 0.02))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / tau) * np.minimum(1, t / 0.002)


# ================================================================== atrito (rangidos)
def atrito(d, taxa, corpo, jitter=0.15, amp=None):
    """Trem de 'trancos' (stick-slip) com taxa(t) por segundo, cada um excitando o corpo (resposta ao impulso)."""
    imp = np.zeros(n(d))
    t = 0.0
    while True:
        r = max(taxa(t), 1.0)
        t += max(1e-4, (1 / r) * (1 + jitter * rng.standard_normal()))
        if t >= d:
            break
        imp[int(t * SR)] += (amp(t) if amp else 1.0) * rng.uniform(0.5, 1.0)
    return conv(imp, corpo)[: n(d)]


def corpo(mat, f0, tau_mult=0.5, d=0.2):
    return ir_modal(modos(mat, f0, tau_mult, 0.05), d)


# ================================================================== grãos
def granulos(d, densidade, grao):
    """densidade(t): grãos por segundo; grao(t): um array curto."""
    out = np.zeros(n(d) + SR)
    t = 0.0
    while True:
        t += rng.exponential(1 / max(densidade(t), 1e-3))
        if t >= d:
            break
        g = grao(t)
        i = int(t * SR)
        out[i: i + len(g)] += g
    return out[: n(d)]


def grao_folha(t=0, lo=1500, hi=7000):
    dur = rng.uniform(0.003, 0.018)
    g = filtro(rng.standard_normal(n(dur) + 2), lo * rng.uniform(0.7, 1.3), hi)
    return g * np.hanning(len(g)) * rng.uniform(0.2, 1.0) ** 2


def grao_pedra(t=0, lo=500, hi=3000):
    return batida(PEDRA, rng.uniform(lo, hi), tau_mult=rng.uniform(0.3, 0.8), clique=0.5) * rng.uniform(0.1, 1.0) ** 2


def estalo_fogo(t=0):
    f = rng.uniform(1200, 5000)
    d = rng.uniform(0.004, 0.02)
    tt = T(d)
    g = np.sin(2 * np.pi * f * tt) * np.exp(-tt / (d / 4)) + 0.5 * rng.standard_normal(len(tt)) * np.exp(-tt / 0.0015)
    return g * rng.uniform(0.1, 1.0) ** 3


def bolha(t=0):
    """Bolha de riacho (Minnaert): um seno curto que SOBE de tom."""
    r_mm = rng.uniform(1.5, 6.0)
    f0 = 3260 / r_mm
    d = rng.uniform(0.02, 0.06)
    tt = T(d)
    f = f0 * (1 + 2.5 * tt / d * 0.3)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / (d / 3)) * np.minimum(1, tt / 0.001) * rng.uniform(0.1, 1.0) ** 2


# ================================================================== filtro que se move (vento, "whoosh")
def filtro_movel(x, centro, largura_oct, N=1024, H=256):
    L = len(x)
    pad = np.concatenate([np.zeros(N), x, np.zeros(N)])
    nf = (len(pad) - N) // H + 1
    idx = np.arange(N)[None, :] + H * np.arange(nf)[:, None]
    w = np.hanning(N)
    F = np.fft.rfft(pad[idx] * w, axis=1)
    f = np.maximum(np.fft.rfftfreq(N, 1 / SR), 1)
    pos = np.clip(H * np.arange(nf) + N // 2 - N, 0, L - 1)
    c = np.asarray(centro)[pos] if np.ndim(centro) else np.full(nf, float(centro))
    lw = np.asarray(largura_oct)[pos] if np.ndim(largura_oct) else np.full(nf, float(largura_oct))
    G = np.exp(-0.5 * (np.log2(f[None, :] / c[:, None]) / lw[:, None]) ** 2)
    y = np.fft.irfft(F * G, N, axis=1) * w
    out = np.zeros(len(pad))
    for k in range(nf):
        out[k * H: k * H + N] += y[k]
    return out[N: N + L] / 1.5


def vento(d, lo=200, hi=1400, taxa=0.5, assobio=0.0, largura=0.9):
    g = suave(d, taxa, 0.1, 1.0) ** 1.5
    c = lo * (hi / lo) ** g                     # a rajada "abre" o vento para o agudo
    x = filtro_movel(ruido(d), c, largura) * (0.25 + 0.75 * g)
    x /= x.std() + 1e-12
    if assobio:
        a = filtro_movel(ruido(d), c * 2.3 * (1 + 0.04 * suave(d, 3, -1, 1)), 0.035)
        x += assobio * a / (a.std() + 1e-12) * g ** 2
    return x


def whoosh(d, f0, f1, f2=None, largura=0.6):
    t = T(d)
    u = t / d
    c = f0 * (f1 / f0) ** np.minimum(1, u * 2) if f2 is None else np.where(
        u < 0.5, f0 * (f1 / f0) ** (u * 2), f1 * (f2 / f1) ** ((u - 0.5) * 2))
    x = filtro_movel(ruido(d), c, largura)
    return norm(x * np.sin(np.pi * u) ** 1.5)


# ================================================================== voz (formantes)
def voz(f0, d, formantes, aspiracao=0.0, jitter=0.01):
    """f0: escalar ou curva. formantes: [(F, largura de banda, ganho)]. Soma de harmônicos com o envelope da garganta."""
    t = T(d)
    f0c = np.full(len(t), float(f0)) if np.ndim(f0) == 0 else np.interp(np.linspace(0, 1, len(t)), np.linspace(0, 1, len(f0)), f0)
    f0c = f0c * (1 + jitter * suave(d, 30, -1, 1))
    fase = 2 * np.pi * np.cumsum(f0c) / SR
    fm = f0c.mean()
    x = np.zeros_like(t)
    for h in range(1, 200):
        if h * fm > SR * 0.45:
            break
        fh = h * fm
        a = sum(g / (1 + ((fh - F) / (bw / 2)) ** 2) for F, bw, g in formantes) / h ** 0.7
        x += a * np.sin(h * fase)
    if aspiracao:
        ns = sum(g * filtro(rng.standard_normal(len(t)), F - bw, F + bw) for F, bw, g in formantes)
        x = norm(x) + aspiracao * norm(ns)
    return norm(x)


# ================================================================== espaço
def espacial(x, pan):
    """pan -1 (esquerda) a 1 (direita): diferença de tempo entre os ouvidos (até 0,65 ms) e o ouvido de longe
    mais baixo e mais abafado (a cabeça faz sombra no agudo). Devolve (n, 2)."""
    a = min(1.0, abs(pan))
    itd = int(0.00065 * a * SR)
    perto = x
    longe = filtro(x, None, 11000 - 7500 * a) * (1 - 0.55 * a)
    longe = np.concatenate([np.zeros(itd), longe])[: len(x)]
    return np.stack([perto, longe], 1) if pan < 0 else np.stack([longe, perto], 1)


def pan_movel(x, p):
    """Panorâmica que anda (p: curva de -1 a 1), em potência constante."""
    p = np.clip(np.interp(np.linspace(0, 1, len(x)), np.linspace(0, 1, len(p)), p), -1, 1) if np.ndim(p) else np.full(len(x), p)
    return np.stack([x * np.sqrt((1 - p) / 2), x * np.sqrt((1 + p) / 2)], 1) * np.sqrt(2)


def sala(x, t60=0.8, mix=0.25, brilho=6000, estereo=None):
    def ir():
        r = filtro(rng.standard_normal(n(t60)), None, brilho) * np.exp(-6.9 * T(t60) / t60)
        r[: n(0.004)] = 0
        pico = np.max(np.abs(r))
        for _ in range(6):                                    # primeiras reflexões (as paredes)
            r[n(rng.uniform(0.006, 0.045))] += rng.choice([-1, 1]) * rng.uniform(0.6, 1.5) * pico
        return r / np.sqrt(np.sum(r ** 2))
    if x.ndim == 1 and not estereo:
        return (1 - mix) * x + mix * conv(x, ir())[: len(x)]
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    return np.stack([(1 - mix) * x[:, c] + mix * conv(x[:, c], ir())[: len(x)] for c in range(2)], 1)


class Mix:
    def __init__(s, d):
        s.x = np.zeros((n(d), 2))
        s.st = False

    def put(s, x, t0=0.0, g=1.0, pan=None):
        x = np.asarray(x, float)
        if pan is not None and x.ndim == 1:
            x = espacial(x, pan)
        if x.ndim == 2:
            s.st = True
        else:
            x = np.stack([x, x], 1)
        i = n(t0)
        m = max(0, min(len(x), len(s.x) - i))
        s.x[i: i + m] += g * x[:m]
        return s

    def saida(s):
        return s.x if s.st else s.x[:, 0]


# ================================================================== gravações reais
_cache = {}


def carregar(nome):
    if nome not in _cache:
        x, sr = ler(os.path.join(ORIG, nome))
        _cache[nome] = (x.mean(1), sr)
    return _cache[nome]


def reamostrar(x, sr):
    if sr == SR:
        return x
    m = int(len(x) * SR / sr)
    X = np.fft.rfft(x)[: m // 2 + 1]
    return np.fft.irfft(X, m) * (m / len(x))


def trecho(nome, ini, d):
    x, sr = carregar(nome)
    return reamostrar(x[int(ini * sr): int((ini + d) * sr)], sr)


def melhor_trecho(nome, d, nota):
    """Procura, de segundo em segundo, o trecho de d segundos com a melhor nota(espectro, freqs, rms)."""
    x, sr = carregar(nome)
    melhor, ini_m = -1e18, 0.0
    for ini in np.arange(0, len(x) / sr - d, 1.0):
        s = x[int(ini * sr): int((ini + d) * sr)]
        S = np.abs(np.fft.rfft(s * np.hanning(len(s))))
        f = np.fft.rfftfreq(len(s), 1 / sr)
        v = nota(S, f, np.sqrt(np.mean(s ** 2)), s, sr)
        if v > melhor:
            melhor, ini_m = v, ini
    return ini_m


def banda(S, f, lo, hi):
    return S[(f >= lo) & (f < hi)]


# ================================================================== PROPOSTAS: sintetizados que estão no jogo
@proposta("Impacto em camadas: o estalo do contato, o 'tapa' no meio e o peso grave do corpo (antes era só um seno que cai).")
def dano():
    m = Mix(0.5)
    m.put(baque(62, 0.45, 0.09), 0, 1.0)
    m.put(batida(dict(r=[1, 1.6, 2.3, 3.1], tau=[.05, .03, .02, .012], a=[1, .6, .4, .2]), 140, excit_ms=3), 0, 0.7)
    m.put(ruido(0.5, 400, 2500) * np.exp(-T(0.5) / 0.012), 0, 0.5)
    m.put(ruido(0.5, 2500) * np.exp(-T(0.5) / 0.002), 0, 0.3)
    return sala(m.saida(), 0.3, 0.12)


@proposta("O vento vai perdendo força e abaixando de tom, e o mar de verdade (gravação do suukadi) entra devagar, calmo.")
def calmaria():
    d = 3.5
    t = T(d)
    m = Mix(d)
    v = vento(d, 150, 900, 0.8) * np.exp(-t / 1.0) * np.minimum(1, t / 0.05)
    m.put(filtro_movel(v, 900 * np.exp(-t / 1.2) + 150, 1.2), 0, 1.0)
    ini = melhor_trecho("410323__suukadi__sea-and-seagull-wave.mp3", d,
                        lambda S, f, r, s, sr: -np.max(banda(S, f, 1200, 4000)) / (np.mean(banda(S, f, 1200, 4000)) + 1e-9) + 30 * r)
    mar = filtro(trecho("410323__suukadi__sea-and-seagull-wave.mp3", ini, d), None, 1800)
    m.put(norm(mar) * np.minimum(1, t / 1.8) ** 2, 0, 1.4)
    return m.saida()


@proposta("Desmoronamento por grãos: dezenas de pedras de tamanhos diferentes caindo umas sobre as outras, o ronco da terra e a poeira assentando.")
def desmoronamento():
    d = 2.6
    m = Mix(d)
    m.put(filtro(ruido(d), 25, 220) * np.exp(-T(d) / 0.9) * np.minimum(1, T(d) / 0.15), 0, 1.0)
    m.put(granulos(d, lambda t: 140 * np.exp(-t / 0.7) + 5, lambda t: filtro(grao_pedra(t, 120, 700), None, 3000)), 0, 0.5)
    for t0 in np.sort(rng.uniform(0.05, 1.4, 5)):                      # as pedras grandes
        m.put(soma(batida(PEDRA, rng.uniform(90, 200), excit_ms=4) * 0.8, baque(rng.uniform(45, 70), 0.4, 0.1)), t0, rng.uniform(0.4, 0.8))
    m.put(ruido(d, 1500, 5000) * np.exp(-T(d) / 1.0) * np.minimum(1, T(d) / 0.5), 0, 0.08)
    return sala(m.saida(), 0.8, 0.22)


@proposta("O golpe passa raspando da esquerda para a direita: um 'whoosh' cujo filtro sobe e desce (o som do ar), com o tecido vibrando.")
def esquiva():
    d = 0.6
    x = whoosh(d, 350, 2800, 700, 0.5)
    x += 0.25 * norm(x * (0.5 + 0.5 * np.sin(2 * np.pi * 28 * T(d))))
    return pan_movel(norm(x), np.linspace(-0.7, 0.7, 50))


@proposta("Farol: o mar de verdade ao longe (abafado), o vento, e uma engrenagem velha de ferro: o dente batendo (metal), "
          "o eixo enferrujado rangendo a cada volta e o peso girando.")
def farol():
    d = 4.5
    t = T(d)
    m = Mix(d)
    m.put(vento(d, 150, 800, 0.4), 0, 0.35)
    ini = melhor_trecho("410323__suukadi__sea-and-seagull-wave.mp3", d,
                        lambda S, f, r, s, sr: -np.max(banda(S, f, 1200, 4000)) / (np.mean(banda(S, f, 1200, 4000)) + 1e-9) + 30 * r)
    m.put(norm(filtro(trecho("410323__suukadi__sea-and-seagull-wave.mp3", ini + 10, d), None, 900)), 0, 0.45)
    t0 = 0.2
    while t0 < d - 0.3:                                                  # os dentes da engrenagem
        m.put(batida(METAL, rng.uniform(780, 860), tau_mult=0.12, excit_ms=0.6), t0, 0.22)
        m.put(batida(METAL, 190, tau_mult=0.15, excit_ms=2), t0 + 0.01, 0.12)
        t0 += 0.33 + rng.uniform(-0.02, 0.02)
    for t0 in (0.8, 2.6):                                                # o eixo enferrujado a cada volta
        dd = 0.9
        ch = atrito(dd, lambda tt: 70 + 60 * np.sin(np.pi * tt / dd), corpo(METAL, 520, 0.08), 0.2)
        m.put(norm(ch) * np.sin(np.pi * T(dd) / dd), t0, 0.18)
    m.put(np.sin(2 * np.pi * 58 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.37 * t)), 0, 0.05)
    return sala(m.saida(), 0.9, 0.2)


@proposta("O fogo vai morrendo de verdade: o ronco da chama baixa, os estalos ficam cada vez mais raros e no fim só sobra um chiado de brasa.")
def fogo_apaga():
    d = 2.0
    t = T(d)
    intens = np.exp(-t / 0.55)
    return _fogo(d, intens, chiado_final=True)


def _fogo(d, intens, chiado_final=False, ronco=0.8):
    t = T(d)
    m = Mix(d)
    m.put(filtro(ruido(d), 40, 260) * suave(d, 8, 0.4, 1.0) * intens, 0, ronco)              # o corpo da chama
    m.put(ruido(d, 1800, 7000) * suave(d, 25, 0.1, 1.0) ** 2 * intens, 0, 0.18)             # o chiado
    m.put(granulos(d, lambda tt: 3 + 45 * intens[min(n(tt), len(intens) - 1)], estalo_fogo), 0, 0.8)
    if chiado_final:
        m.put(ruido(d, 3000, 9000) * bump(d, d * 0.7, d * 0.25), 0, 0.06)
    return m.saida()


def _garra(pan):
    d = 1.3
    m = Mix(d)
    for k, t0 in enumerate((0.05, 0.3)):                       # dois passos rápidos se aproximando (peso + folhas)
        m.put(soma(baque(80, 0.25, 0.05), 0.4 * granulos(0.25, lambda t: 260 * np.exp(-t / 0.05), grao_folha)), t0, 0.5 + 0.2 * k, pan=pan)
    m.put(whoosh(0.35, 300, 1500, None, 0.7), 0.55, 0.5, pan=pan)    # o braço armando
    rasgo = Mix(0.4)
    for k in range(3):                                         # três garras rasgando o ar, uma logo depois da outra
        rasgo.put(whoosh(0.22, 1200, 6500, 2500, 0.35), 0.015 * k, 0.6)
    m.put(rasgo.saida(), 0.8, 0.9, pan=pan)
    m.put(granulos(0.12, lambda t: 900, lambda t: grao_folha(t, 2500, 9000)), 0.86, 0.35, pan=pan)
    m.put(baque(110, 0.2, 0.04), 0.9, 0.4, pan=pan)
    return sala(m.saida(), 0.4, 0.12, estereo=True)


@proposta("Garra vindo da ESQUERDA: passos, o braço armando e três garras rasgando o ar, com diferença de tempo entre os ouvidos "
          "(no fone fica bem mais claro de que lado vem).")
def garra_esquerda():
    return _garra(-1.0)


@proposta("Garra vindo da DIREITA (igual à esquerda, espelhada).")
def garra_direita():
    return _garra(1.0)


@proposta("Garra vindo de FRENTE: igual nos dois ouvidos.")
def garra_frente():
    return _garra(0.0)


def _passo_folhas(g=1.0, longe=0.0):
    p = soma(baque(85, 0.22, 0.04) * 0.8, granulos(0.25, lambda t: 400 * np.exp(-t / 0.06), grao_folha) * 0.6)
    if longe:
        p = filtro(p, None, 8000 * (1 - longe) + 900)
    return p * g


@proposta("O goblin foge: passos correndo nas folhas, cada vez mais rápidos, mais baixos e mais abafados (vai sumindo entre as árvores).")
def goblin_foge():
    d = 2.2
    m = Mix(d)
    t0, gap, k = 0.0, 0.2, 0
    while t0 < d - 0.25:
        longe = min(1.0, t0 / 1.9)
        m.put(_passo_folhas(1 - 0.8 * longe, longe), t0, 0.8, pan=0.15 + 0.35 * longe)
        t0 += gap * rng.uniform(0.9, 1.1)
        gap *= 0.95
        k += 1
    return sala(m.saida(), 0.6, 0.2, estereo=True)


@proposta("O goblin salta: as folhas explodem, o corpo passa pelo ar e aterrissa (peso + folhas espalhando).")
def goblin_salta():
    d = 1.2
    m = Mix(d)
    m.put(granulos(0.4, lambda t: 500 * np.sin(np.pi * t / 0.4) + 20, grao_folha), 0.0, 0.6)
    m.put(whoosh(0.4, 500, 2400, None, 0.6), 0.12, 0.45)
    m.put(baque(95, 0.3, 0.06), 0.52, 1.0)
    m.put(granulos(0.5, lambda t: 1200 * np.exp(-t / 0.08), grao_folha), 0.5, 0.7)
    return sala(m.saida(), 0.3, 0.1)


@proposta("Pedras virando poeira: começam com pedaços maiores e terminam em areia escorrendo (os grãos vão ficando menores e mais agudos).")
def golem_poeira():
    d = 2.8
    m = Mix(d)
    m.put(granulos(2.2, lambda t: 160 * np.exp(-t / 0.8) + 10, lambda t: grao_pedra(t, 300 + 900 * t, 1200 + 2500 * t)), 0, 0.6)
    areia = ruido(d, 2500, 9000) * suave(d, 40, 0.3, 1.0) * np.minimum(1, T(d) / 0.6) * np.exp(-T(d) / 1.2)
    m.put(areia, 0, 0.2)
    m.put(filtro(ruido(d), 30, 200) * np.exp(-T(d) / 0.6), 0, 0.5)
    return sala(m.saida(), 0.8, 0.25)


@proposta("Grilo de verdade: cada cri-cri são 4 pulsos curtos num tom de ~4,6 kHz que cai um pouquinho, com harmônico; vindo da "
          "esquerda com diferença de tempo entre os ouvidos.")
def grilo():
    d = 1.8
    m = Mix(d)
    for g in range(3):
        for p in range(4):
            dd = 0.018
            tt = T(dd)
            f = 4600 * (1 - 0.02 * tt / dd)
            ph = 2 * np.pi * np.cumsum(f) / SR
            env = np.minimum(1, tt / 0.002) * np.exp(-tt / 0.008)
            pulso = (np.sin(ph) + 0.15 * np.sin(2 * ph)) * env
            m.put(pulso, 0.15 + g * 0.55 + p * 0.032, 0.7 * (0.85 + 0.15 * (p in (1, 2))), pan=-0.8)
    return sala(m.saida(), 0.4, 0.1, estereo=True)


@proposta("Passos na folhagem À ESQUERDA (o velho não tinha lado): o peso do pé e as folhas secas estalando, grão a grão.")
def passo():
    d = 1.0
    m = Mix(d)
    for t0 in (0.05, 0.55):
        m.put(_passo_folhas(), t0, 0.9, pan=-0.7)
    return m.saida()


@proposta("Queimadura: a labareda chega num sopro (o ronco que abre para o agudo), a pele chia e a chama estala.")
def queimadura():
    d = 1.0
    t = T(d)
    m = Mix(d)
    m.put(whoosh(0.45, 250, 1800, None, 0.9), 0, 0.8)
    m.put(_fogo(d, np.exp(-t / 0.35), ronco=0.5), 0, 0.8)
    m.put(ruido(d, 3500, 9000) * suave(d, 60, 0, 1) ** 3 * np.exp(-t / 0.3), 0.05, 0.3)
    return m.saida()


def estalo_de_dedos():
    """O estalo é ar, não madeira: um chiado largo e curtíssimo (o dedo batendo na palma solta o ar de uma vez),
    um resto de ar médio que some em ~15 ms e um 'pop' grave e fraco da palma. Sem tom (o tom é que soava a palito)."""
    d = 0.12
    t = T(d)
    clique = ruido(d, 700, 10000) * np.exp(-t / 0.0022)
    ar = ruido(d, 1500, 5000) * np.exp(-t / 0.014) * 0.3
    pop = np.sin(2 * np.pi * 280 * t) * np.exp(-t / 0.007) * 0.25
    return norm(clique + ar + pop)


@proposta("Teleporte: um estalar de dedos de verdade (Snapper4298, Freesound 177507) e, logo depois, um redemoinho de vento "
          "que gira em volta da cabeça.")
def teleporte():
    d = 1.5
    m = Mix(d)
    estalo = trecho("177507__snapper4298__snap_6.flac", 0, 0.4)
    estalo *= np.minimum(1, (len(estalo) - np.arange(len(estalo))) / n(0.1))      # fim suave
    m.put(norm(estalo), 0, 1.0)
    w = whoosh(1.0, 300, 3500, 600, 0.5)                 # o vento entra depois do estalo, sem cobri-lo
    m.put(pan_movel(w, np.sin(np.linspace(0, 3 * np.pi, 80)) * 0.8), 0.3, 0.55)
    return sala(m.saida(), 0.6, 0.2, estereo=True)


@proposta("Moedas de verdade: cada moeda com as suas ressonâncias de metal, um monte caindo e, no fim, uma moeda quicando e girando até parar.")
def tesouro():
    d = 2.8
    m = Mix(d)
    for t0 in np.sort(rng.uniform(0, 1.6, 40)) ** 1.3:
        m.put(batida(MOEDA, rng.uniform(1800, 4200), tau_mult=rng.uniform(0.3, 1.0), excit_ms=0.3), t0, rng.uniform(0.1, 0.5), pan=rng.uniform(-0.4, 0.4))
    f0 = 3100
    t0, gap = 1.7, 0.13
    while gap > 0.012 and t0 < d - 0.2:                        # a última moeda girando cada vez mais rápido
        m.put(batida(MOEDA, f0, tau_mult=0.4, excit_ms=0.3), t0, 0.35 * (gap / 0.13) ** 0.3)
        t0 += gap
        gap *= 0.8
    return sala(m.saida(), 0.6, 0.2, estereo=True)


@proposta("Vento seco: rajadas que abrem e fecham (o filtro anda junto com a força), areia fina raspando e nenhum bicho.")
def vento_seco():
    d = 2.8
    m = Mix(d)
    m.put(vento(d, 250, 1600, 0.7, assobio=0.15), 0, 1.0)
    m.put(granulos(d, lambda t: 600, lambda t: grao_folha(t, 3500, 9000) * 0.3), 0, 0.15)
    return m.saida()


@proposta("Abismo: o vento sobe do fundo com um uivo grave (uma faixa estreita de ressonância que vai subindo de tom), "
          "o ronco lá embaixo e eco de caverna.")
def abismo():
    d = 3.0
    t = T(d)
    amp = np.minimum(1, t / 1.4) * np.minimum(1, (d - t) / 0.6)
    m = Mix(d)
    m.put(filtro_movel(ruido(d), 180 * (1 + 1.2 * t / d), 0.15) * amp, 0, 0.8)
    m.put(vento(d, 150, 900, 0.6) * amp, 0, 0.5)
    m.put(filtro(ruido(d), 25, 90) * amp, 0, 0.6)
    return sala(m.saida(), 1.6, 0.4)


@proposta("Mar calmo de verdade (gravação do suukadi, trecho sem gaivota) e a vela batendo no vento (pano tremulando).")
def mar_calmo():
    d = 4.5
    m = Mix(d)
    ini = melhor_trecho("410323__suukadi__sea-and-seagull-wave.mp3", d,
                        lambda S, f, r, s, sr: -np.max(banda(S, f, 1200, 4000)) / (np.mean(banda(S, f, 1200, 4000)) + 1e-9) + 30 * r)
    m.put(norm(trecho("410323__suukadi__sea-and-seagull-wave.mp3", ini, d)), 0, 0.7)
    for t0 in (0.6, 2.4, 3.5):
        dd = rng.uniform(0.35, 0.6)
        pano = ruido(dd, 250, 3000) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * rng.uniform(13, 19) * T(dd)))) * np.sin(np.pi * T(dd) / dd) ** 2
        m.put(pano, t0, 0.3)
    return m.saida()


@proposta("Vento na janela: a rajada (sem grave, como o velho), o assobio pela fresta e a janela de madeira chacoalhando no pico da rajada.", -26.0)
def vento_janela():
    d = 2.2
    t = T(d)
    amp = np.sin(np.pi * t / d) ** 2
    m = Mix(d)
    m.put(filtro_movel(ruido(d), 700 * (2200 / 700) ** amp, 1.0) * amp, 0, 1.0)
    m.put(filtro_movel(ruido(d), 950 + 300 * amp, 0.03) * amp ** 2, 0, 0.35)
    for t0 in np.sort(rng.uniform(0.8, 1.4, 7)):
        m.put(batida(MADEIRA, rng.uniform(380, 520), tau_mult=0.4, excit_ms=0.8), t0, rng.uniform(0.05, 0.15))
    return filtro(m.saida(), 350, None)


@proposta("Frascos: garrafinhas de vidro batendo umas nas outras (cada batida soa nas duas garrafas, com ressonâncias de vidro de verdade).")
def frascos():
    d = 2.2
    m = Mix(d)
    for t0 in np.sort(rng.uniform(0, 1.6, 9)):
        a, b = rng.uniform(1400, 3800, 2)
        m.put(batida(VIDRO, a, tau_mult=rng.uniform(0.2, 0.5), excit_ms=0.3), t0, rng.uniform(0.3, 0.7), pan=rng.uniform(-0.3, 0.3))
        m.put(batida(VIDRO, b, tau_mult=rng.uniform(0.2, 0.5), excit_ms=0.3), t0 + rng.uniform(0.003, 0.02), rng.uniform(0.2, 0.5), pan=rng.uniform(-0.3, 0.3))
    return sala(m.saida(), 0.5, 0.2, estereo=True)


# ================================================================== PROPOSTAS: os que estão sem som
@proposta("A pedra pulsa com um brilho quente: um acorde grave e morno que pulsa duas vezes, como um coração, com um brilho suave por cima.")
def magia():
    d = 2.0
    t = T(d)
    pulso = bump(d, 0.35, 0.18) + 0.8 * bump(d, 0.75, 0.2) + 0.3 * bump(d, 1.3, 0.4)
    acorde = sum(g * np.sin(2 * np.pi * f * t * (1 + 0.002 * np.sin(2 * np.pi * 5 * t))) for f, g in ((110, 1), (165, .7), (220, .6), (277, .4), (330, .3)))
    m = Mix(d)
    m.put(acorde * pulso, 0, 1.0)
    for t0 in np.sort(rng.uniform(0.2, 1.4, 10)):
        m.put(batida(VIDRO, rng.choice([1320, 1650, 1980, 2640]), tau_mult=0.6, excit_ms=3) * 0.5, t0, 0.15, pan=rng.uniform(-0.5, 0.5))
    return sala(m.saida(), 1.2, 0.35, brilho=4000, estereo=True)


def realcar_canto(x, forca=1.6, N=1024, H=256):
    """Tira o chiado de fundo da gravação (o nível mediano de cada frequência) e deixa os pios saltarem."""
    pad = np.concatenate([np.zeros(N), x, np.zeros(N)])
    nf = (len(pad) - N) // H + 1
    idx = np.arange(N)[None, :] + H * np.arange(nf)[:, None]
    w = np.hanning(N)
    F = np.fft.rfft(pad[idx] * w, axis=1)
    A = np.abs(F) + 1e-12
    G = np.clip(1 - forca * np.median(A, axis=0)[None, :] / A, 0.05, 1)
    y = np.fft.irfft(F * G, N, axis=1) * w
    out = np.zeros(len(pad))
    for k in range(nf):
        out[k * H: k * H + N] += y[k]
    return out[N: N + len(x)] / 1.5


@proposta("Bifurcação: À ESQUERDA pássaros cantando de verdade (o trecho da gravação do klankbeeld com mais pios, com o chiado de "
          "fundo tirado) e água correndo baixinho (gravação do Lubini); À DIREITA só vento seco.")
def bifurcacao():
    d = 3.5
    m = Mix(d)
    nome = "bronze/810428__klankbeeld__park-forest-loonse-en-drunense-duinen-netherlands-1125-am-150410_0602.flac"
    # 52,9 s: o trecho de 3,5 s com mais pios (quadros com um tom forte entre 1,5 e 8 kHz que muda de altura de um
    # quadro para o outro, o que é canto de pássaro; inseto e vento não fazem isso). Medido nas quatro gravações de mata.
    passaros = filtro(realcar_canto(trecho(nome, 52.9, d)), 1600, 9000)
    m.put(norm(passaros), 0, 1.0, pan=-0.9)
    agua = filtro(trecho("338345__lubini__splashing-water-by-oars.flac", 1.6, d), 300, 2500)
    m.put(norm(agua) * np.minimum(1, np.arange(len(agua)) / n(0.4)), 0, 0.18, pan=-0.6)
    m.put(norm(vento(d, 200, 1100, 0.5)), 0, 0.3, pan=0.9)
    x = m.saida()
    k = n(1.6)                                   # some devagar nos últimos 1,6 s (antes terminava seco) e entra em 0,15 s
    x[-k:] *= ((np.cos(np.linspace(0, np.pi, k)) * 0.5 + 0.5) ** 1.5)[:, None]
    x[:n(0.15)] *= np.linspace(0, 1, n(0.15))[:, None]
    return x


@proposta("Risada do goblin de verdade (SnowFightStudios, a risada mais longa da gravação: 12,7 a 14,1 s), dando uma volta "
          "em volta da cabeça: frente, um lado, atrás (mais abafada) e o outro lado.")
def goblin_risada():
    d = 1.75
    x = trecho("643664__snowfightstudios__goblin_various-laughs-and-giggles.mp3", 12.7, 1.4)
    tt = np.arange(len(x)) / SR
    x = x * np.minimum(1, tt / 0.01) * np.minimum(1, (tt[-1] - tt) / 0.08)
    ang = np.linspace(0, 2 * np.pi, len(x))
    atras = np.clip(-np.cos(ang), 0, 1)                         # 0 na frente, 1 atrás da cabeça
    x = x * (1 - atras) + filtro(x, None, 2500) * atras * 0.8
    m = Mix(d)
    m.put(pan_movel(x, 0.9 * np.sin(ang)), 0.05, 1.0)
    return sala(m.saida(), 0.5, 0.15, estereo=True)


def _goblin_risada_sintetica():
    """A proposta anterior (voz sintetizada), guardada para comparar."""
    d = 2.0
    m = Mix(d)
    for i in range(9):
        dd = 0.11
        f0 = np.array([760, 640]) * (1 - 0.025 * i) * rng.uniform(0.96, 1.04)
        s = voz(f0, dd, [(330, 120, 1.0), (2300, 250, 0.8), (3000, 300, 0.4)], aspiracao=0.2, jitter=0.02)
        s *= np.minimum(1, T(dd) / 0.01) * np.minimum(1, (dd - T(dd)) / 0.03)
        h = ruido(0.04, 1500, 5000) * np.hanning(n(0.04)) * 0.25        # o "h" antes do "i"
        ang = 2 * np.pi * i / 6
        s = np.concatenate([h, s])
        if np.cos(ang) < 0:                                            # atrás da cabeça: mais abafado
            s = filtro(s, None, 3000)
        m.put(s, 0.1 + i * 0.16, 0.7, pan=float(np.sin(ang)))
    return sala(m.saida(), 0.5, 0.2, estereo=True)


@proposta("Porta de pedra: o arrasto é feito de milhares de pequenos trancos de pedra contra pedra (áspero de verdade), com o ronco do "
          "peso, e termina numa batida pesada que levanta pó.")
def porta_pedra():
    d = 3.4
    t = T(d)
    m = Mix(d)
    env = np.minimum(1, t / 0.15) * np.minimum(1, np.maximum(0, 2.6 - t) / 0.3)
    rasp = atrito(d, lambda tt: 350 + 250 * np.sin(2 * np.pi * 0.7 * tt), corpo(PEDRA, 150, 0.6), 0.5)
    m.put(norm(rasp) * env, 0, 0.7)
    m.put(filtro(ruido(d), 30, 110) * env * suave(d, 4, 0.5, 1.0), 0, 0.6)
    m.put(soma(batida(PEDRA, 70, excit_ms=8), baque(48, 0.6, 0.15) * 1.2), 2.65, 1.2)
    m.put(granulos(0.6, lambda tt: 200 * np.exp(-tt / 0.15), lambda tt: grao_pedra(tt, 800, 3000)), 2.68, 0.3)
    return sala(m.saida(), 1.1, 0.3)


def _armadura_rangido(d=0.8):
    ch = atrito(d, lambda tt: 45 + 50 * np.sin(np.pi * tt / d), corpo(METAL, 640, 0.06), 0.25)
    return norm(ch) * np.sin(np.pi * T(d) / d) ** 0.7


@proposta("Corredores: À ESQUERDA uma armadura vazia rangendo (junta de metal) e chacoalhando; À DIREITA passos pesados de pedra.")
def corredores():
    d = 3.0
    m = Mix(d)
    m.put(_armadura_rangido(0.8), 0.1, 0.35, pan=-0.9)
    for t0 in np.sort(rng.uniform(0.8, 2.6, 6)):
        m.put(batida(METAL, rng.uniform(900, 2400), tau_mult=0.25, excit_ms=0.5), t0, rng.uniform(0.1, 0.25), pan=-0.9)
    m.put(_armadura_rangido(0.6), 1.8, 0.25, pan=-0.9)
    for t0 in (0.3, 1.2, 2.1):
        m.put(soma(baque(55, 0.45, 0.1), 0.6 * batida(PEDRA, 140, excit_ms=5)), t0, 0.9, pan=0.9)
    return sala(m.saida(), 1.2, 0.3, estereo=True)


@proposta("Armadura vazia: o rangido da junta de metal (atrito) e as placas batendo umas nas outras, num salão com eco.")
def armadura():
    d = 1.8
    m = Mix(d)
    m.put(_armadura_rangido(0.9), 0.05, 0.5)
    for t0 in np.sort(rng.uniform(0.5, 1.3, 8)):
        m.put(batida(METAL, rng.uniform(900, 2600), tau_mult=0.3, excit_ms=0.5), t0, rng.uniform(0.15, 0.4))
    return sala(m.saida(), 1.0, 0.3)


@proposta("Banquete fantasma: louça e talheres batendo (cerâmica e metal), uma taça tilintando e, ao fundo, o murmúrio de uma taverna "
          "de verdade (ralexpdx) abafado e com eco, como vozes que não estão ali.")
def banquete():
    d = 3.0
    m = Mix(d)
    ini = melhor_trecho("bronze/321220__ralexpdx__my-tavern-1.flac", d,
                        lambda S, f, r, s, sr: np.sum(banda(S, f, 200, 1000)) / (np.sum(banda(S, f, 2000, 8000)) + 1e-9))
    murm = filtro(trecho("bronze/321220__ralexpdx__my-tavern-1.flac", ini, d), 200, 1200)
    m.put(norm(murm), 0, 0.35)
    for t0 in np.sort(rng.uniform(0.05, 2.6, 10)):
        if rng.random() < 0.5:
            m.put(batida(LOUCA, rng.uniform(1100, 2300), excit_ms=0.6), t0, rng.uniform(0.15, 0.4), pan=rng.uniform(-0.5, 0.5))
        else:
            m.put(batida(METAL, rng.uniform(2800, 4500), tau_mult=0.12, excit_ms=0.3), t0, rng.uniform(0.1, 0.3), pan=rng.uniform(-0.5, 0.5))
    m.put(batida(VIDRO, 2650, tau_mult=0.9, excit_ms=0.3), 1.4, 0.35)
    return sala(m.saida(), 1.4, 0.35, brilho=3500, estereo=True)


@proposta("Espelho antigo vibrando: vidro 'cantando' (como dedo molhado na borda da taça), com dois tons quase iguais que batem entre si.")
def espelho():
    d = 3.0
    t = T(d)
    env = np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.8)
    x = (np.sin(2 * np.pi * 1180 * t) + np.sin(2 * np.pi * 1186.5 * t) + 0.35 * np.sin(2 * np.pi * 1180 * 2.32 * t)
         + 0.15 * np.sin(2 * np.pi * 1180 * 4.25 * t)) * env * (0.8 + 0.2 * suave(d, 3, 0, 1))
    m = Mix(d)
    m.put(x, 0, 0.5)
    m.put(ruido(d, 1100, 1300) * env * 0.08, 0, 1.0)                  # o atrito na borda
    return sala(m.saida(), 1.5, 0.35, estereo=True)


@proposta("Pé firme na pedra: a sola batendo (ressonância de pedra, curta), o peso e um pouco de areia rangendo.", -24.0)
def pedra_firme():
    m = Mix(0.6)
    m.put(baque(80, 0.3, 0.05), 0, 0.8)
    m.put(batida(PEDRA, 230, excit_ms=2.5), 0, 0.6)
    m.put(granulos(0.15, lambda t: 300, lambda t: grao_folha(t, 2500, 8000)), 0.01, 0.15)
    return sala(m.saida(), 0.5, 0.15)


@proposta("Pedra afundando: a pedra raspa e range descendo (o atrito vai ficando mais grave), pedrinhas caindo e uma batida funda lá embaixo.")
def pedra_afunda():
    d = 1.8
    t = T(d)
    m = Mix(d)
    env = np.minimum(1, t / 0.05) * np.minimum(1, np.maximum(0, 0.95 - t) / 0.1)
    m.put(norm(atrito(d, lambda tt: 500 * np.exp(-tt / 0.5) + 60, corpo(PEDRA, 120, 0.6), 0.4)) * env, 0, 0.7)
    m.put(granulos(1.0, lambda tt: 80, lambda tt: grao_pedra(tt, 600, 2500)), 0.2, 0.3)
    m.put(soma(baque(42, 0.6, 0.15), 0.5 * batida(PEDRA, 60, excit_ms=8)), 0.95, 1.1)
    return sala(m.saida(), 0.9, 0.3)


@proposta("Golem: o chão treme (grave que pulsa), três passos pesadíssimos de pedra com cascalho caindo, e as juntas de pedra rangendo entre os passos.")
def golem():
    d = 3.5
    t = T(d)
    m = Mix(d)
    m.put(filtro(ruido(d), 22, 80) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t)), 0, 0.6)
    for t0 in (0.3, 1.3, 2.3):
        m.put(soma(baque(40, 0.7, 0.18) * 1.3, 0.6 * batida(PEDRA, 80, excit_ms=10)), t0, 1.0)
        m.put(granulos(0.5, lambda tt: 150 * np.exp(-tt / 0.15), lambda tt: grao_pedra(tt, 400, 2000)), t0 + 0.02, 0.35)
        dd = 0.5
        m.put(norm(atrito(dd, lambda tt: 150 + 100 * np.sin(np.pi * tt / dd), corpo(PEDRA, 110, 0.6), 0.5)) * np.sin(np.pi * T(dd) / dd), t0 + 0.4, 0.3)
    return sala(m.saida(), 1.3, 0.3)


@proposta("Dragão cuspindo fogo: um rugido de garganta de verdade (formantes graves de 'a', com tremor) e logo a labareda (ronco, chiado e estalos).")
def fogo():
    d = 2.8
    t = T(d)
    m = Mix(d)
    rd = 1.6
    f0 = np.array([62, 75, 70, 55, 45])
    rug = voz(f0, rd, [(420, 200, 1.0), (850, 300, 0.7), (1800, 500, 0.3)], aspiracao=0.6, jitter=0.08)
    rug *= np.minimum(1, T(rd) / 0.15) * np.minimum(1, (rd - T(rd)) / 0.4) * (0.75 + 0.25 * np.sin(2 * np.pi * 24 * T(rd)))
    m.put(rug, 0, 0.9)
    intens = np.minimum(1, np.maximum(0, t - 0.5) / 0.2) * np.minimum(1, np.maximum(0, d - t) / 0.8)
    m.put(_fogo(d, intens, ronco=1.0), 0, 0.9)
    m.put(whoosh(0.8, 200, 1500, None, 1.0), 0.45, 0.6)
    return sala(m.saida(), 1.2, 0.3)


@proposta("Respiração do dragão: ele puxa o ar (o filtro sobe) e solta devagar (mais grave, com ronco na garganta), e o chão treme por baixo.")
def dragao_respira():
    d = 3.6
    t = T(d)
    m = Mix(d)
    ent = np.where(t < 1.5, np.sin(np.pi * np.minimum(t, 1.5) / 1.5) ** 2, 0)
    sai = np.where(t > 1.6, np.sin(np.pi * np.clip(t - 1.6, 0, 1.9) / 1.9) ** 1.5, 0)
    m.put(filtro_movel(ruido(d), 500 + 900 * np.minimum(1, t / 1.5), 0.8) * ent, 0, 0.6)
    m.put(filtro_movel(ruido(d), 350 + 200 * suave(d, 2, 0, 1), 0.7) * sai, 0, 0.8)
    rug = voz(np.array([38, 42, 36]), d, [(300, 200, 1.0), (700, 300, 0.5)], aspiracao=0.8, jitter=0.1)
    m.put(rug * sai, 0, 0.45)
    m.put(filtro(ruido(d), 20, 70) * (0.5 + 0.5 * np.sin(2 * np.pi * 5 * t)), 0, 0.5)
    return sala(m.saida(), 1.2, 0.3)


@proposta("Porta da casa de cura: o trinco de uma porta de madeira de verdade (pnmcarrierailfan), a porta rangendo ao abrir e o "
          "sininho da porta balançando (sino pequeno, várias batidinhas).")
def casa_de_cura():
    d = 2.8
    m = Mix(d)
    trinco = trecho("684538__pnmcarrierailfan__doors-wood-door-with-latch_1.mp3", 0, 0.8)
    m.put(norm(trinco), 0, 0.7)
    dd = 0.7
    ch = atrito(dd, lambda tt: 35 + 55 * np.sin(np.pi * tt / dd), corpo(MADEIRA, 320, 0.4), 0.2)
    m.put(norm(ch) * np.sin(np.pi * T(dd) / dd), 0.3, 0.35)
    t0 = 0.95
    for k in range(6):
        m.put(batida(SINO, 1500, tau_mult=0.5, excit_ms=0.4), t0, 0.35 * 0.75 ** k)
        t0 += rng.uniform(0.07, 0.16)
    return sala(m.saida(), 0.7, 0.2)


# ================================================================== saída
NAO_REVISADOS = {
    "cajado": "refeito hoje (batida com eco, sem sino), a pedido",
    "agua_empurra / madeira_embarca / rangido_barco": "refeitos hoje a partir de gravações reais",
    "vez_do_jogador": "é um aviso de interface (dois bipes): precisa ser simples e sempre igual; não mexi",
    "galo_vento, porta, trovao, masmorra, dragao_cai, abertura": "gravações reais (fora do escopo: a revisão é dos sintetizados e dos que faltam)",
}


def finalizar(x, alvo_db):
    x = filtro(np.asarray(x, float), 25, None)         # tira o deslocamento do zero e o grave inaudível
    f = n(0.03)
    rampa = np.linspace(1, 0, f)
    x[-f:] *= rampa[:, None] if x.ndim == 2 else rampa
    x = x * 10 ** ((alvo_db - rms_db(x)) / 20)
    pico = np.max(np.abs(x))
    if pico > 0.95:                                     # limita os picos sem achatar o resto
        x = np.tanh(x / 0.95) * 0.95
    return x


def main():
    nomes = [a for a in sys.argv[1:] if not a.startswith("--")] or list(PROPOSTAS)
    indice = []
    for nome in nomes:
        fn, nota, alvo = PROPOSTAS[nome]
        pasta = os.path.join(SAIDA, nome)
        os.makedirs(pasta, exist_ok=True)
        velho, tipo = os.path.join(SONS, nome + ".wav"), "velho"
        if os.path.exists(velho):
            shutil.copyfile(velho, os.path.join(pasta, tipo + ".wav"))
            xv, _ = ler(velho)
            alvo = alvo if alvo is not None else rms_db(xv)
        else:
            tipo = None
        alvo = alvo if alvo is not None else -22.0
        x = finalizar(fn(), alvo)
        gravar(os.path.join(pasta, "proposta.wav"), x if x.ndim == 2 else x[:, None], SR)
        no_jogo = os.path.exists(os.path.join(SONS, nome + ".wav"))
        indice.append(dict(nome=nome, nota=nota, velho=tipo, no_jogo=no_jogo, dur=round(len(x) / SR, 1),
                           estereo=bool(x.ndim == 2)))
        print(f"{nome:16s} {'no jogo ' if no_jogo else 'SEM SOM '} {len(x) / SR:4.1f}s {'estéreo' if x.ndim == 2 else 'mono   '} {alvo:6.1f} dB")
    if len(nomes) == len(PROPOSTAS):
        with open(os.path.join(SAIDA, "indice.json"), "w", encoding="utf-8") as f:
            json.dump(dict(sons=indice, nao_revisados=NAO_REVISADOS), f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
