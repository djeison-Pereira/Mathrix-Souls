"""Monta audios/sons/madeira_embarca.wav: dois passos ocos no casco do bote + água balançando + rangido.
Uso (dentro de arquivos): python ferramentas_audio/gerar_madeira_embarca.py"""
import os
import sys
import numpy as np
ARQ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ARQ)                       # os caminhos abaixo são relativos à pasta arquivos
sys.path.insert(0, ARQ)
from masterizar_audios import ler, gravar

SR = 22050
rng = np.random.default_rng(3)


def mono(caminho, ini=0.0, fim=None):
    x, sr = ler(caminho)
    x = x.mean(1)
    x = x[int(ini * sr): int(fim * sr) if fim else None]
    idx = np.arange(0, len(x), sr / SR)                      # reamostra para 22050
    return np.interp(idx, np.arange(len(x)), x)


def eq(x, curva):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * curva(np.maximum(f, 1)), len(x))


def passa_baixa(fc):
    return lambda f: 1 / np.sqrt(1 + (f / fc) ** 4)


def passa_alta(fc):
    return lambda f: 1 / np.sqrt(1 + (fc / f) ** 4)


def oco(f):
    """O casco é uma caixa oca: reforça os graves de madeira (~150 e ~320 Hz) e abafa o agudo."""
    pico = 1 + 2.5 * np.exp(-((np.log(f / 150)) / 0.35) ** 2) + 1.2 * np.exp(-((np.log(f / 320)) / 0.3) ** 2)
    return pico * passa_baixa(2200)(f) * passa_alta(60)(f)


def sala_oca(x, t60=0.35, w=0.3):
    n = int(t60 * SR)
    t = np.arange(n) / SR
    r = eq(rng.standard_normal(n), passa_baixa(1800)) * np.exp(-6.9 * t / t60)
    r /= np.sqrt(np.sum(r ** 2))
    m = len(x) + n
    y = np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(r, m), m)[: len(x)]
    return (1 - w) * x + w * y


def fade(x, ini, fim):
    x = x.copy()
    a, b = int(ini * SR), int(fim * SR)
    if a:
        x[:a] *= np.linspace(0, 1, a)
    if b:
        x[-b:] *= np.linspace(1, 0, b)
    return x


def norm(x):
    return x / (np.sqrt(np.mean(x ** 2)) + 1e-12)


d = 2.6
out = np.zeros(int(d * SR))


def put(x, t0, g):
    i = int(t0 * SR)
    x = x[: len(out) - i]
    out[i: i + len(x)] += g * x


O = "audios_originais/"
passos = eq(mono(O + "767432__discordantscraps__wood-tumble.flac"), oco)          # as duas batidas (você e o Grilo)
put(fade(passos, 0.002, 0.1), 0.0, 1.0)

agua = eq(mono(O + "338345__lubini__splashing-water-by-oars.flac", 1.6, 3.6), passa_baixa(1100))   # água batendo no casco
agua = fade(norm(agua), 0.25, 0.6) * np.sqrt(np.sum(passos ** 2) / len(passos))
put(agua, 0.05, 0.45)

rangido = mono(O + "536365__kostas17__creaking-floor.flac", 4.25, 5.2)
rangido = np.interp(np.arange(0, len(rangido), 0.75), np.arange(len(rangido)), rangido)   # mais lento = mais grave, casco pesado
rangido = eq(rangido, lambda f: passa_baixa(1400)(f) * passa_alta(120)(f))
rangido = fade(norm(rangido), 0.15, 0.3) * np.sqrt(np.sum(passos ** 2) / len(passos))
put(rangido, 1.0, 0.3)                                   # o bote balança com o peso

out = sala_oca(out)
out = fade(out, 0, 0.25)
out = out / np.max(np.abs(out)) * 0.8
gravar("audios/sons/madeira_embarca.wav", out[:, None], SR)
print("ok", len(out) / SR)
