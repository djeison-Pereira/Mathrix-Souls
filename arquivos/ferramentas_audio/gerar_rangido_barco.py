"""Monta audios/sons/rangido_barco.wav: duas remadas, cada uma com o rangido do remo no tolete
(madeira contra madeira) e a pá do remo puxando a água logo depois.
Uso (dentro de arquivos): python ferramentas_audio/gerar_rangido_barco.py"""
import os
import sys
import numpy as np
ARQ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ARQ)                       # os caminhos abaixo são relativos à pasta arquivos
sys.path.insert(0, ARQ)
from masterizar_audios import ler, gravar

SR = 22050
O = "audios_originais/"


def mono(caminho, ini, fim, velocidade=1.0):
    x, sr = ler(caminho)
    x = x.mean(1)[int(ini * sr): int(fim * sr)]
    idx = np.arange(0, len(x), sr / SR * velocidade)     # reamostra (velocidade > 1: mais agudo e mais curto)
    return np.interp(idx, np.arange(len(x)), x)


def eq(x, curva):
    X = np.fft.rfft(x)
    f = np.maximum(np.fft.rfftfreq(len(x), 1 / SR), 1)
    return np.fft.irfft(X * curva(f), len(x))


def faixa(lo, hi):
    return lambda f: 1 / np.sqrt(1 + (lo / f) ** 4) / np.sqrt(1 + (f / hi) ** 4)


def fade(x, ini, fim):
    x = x.copy()
    a, b = int(ini * SR), int(fim * SR)
    x[:a] *= np.linspace(0, 1, a) ** 2
    x[-b:] *= np.linspace(1, 0, b) ** 2
    return x


def rms(x):
    return np.sqrt(np.mean(x ** 2)) + 1e-12


d = 2.8
out = np.zeros(int(d * SR))


def put(x, t0, g):
    i = int(t0 * SR)
    x = x[: len(out) - i]
    out[i: i + len(x)] += g * x


# o rangido: dois trechos diferentes do "Creaking floor", um pouco mais agudos (o tolete é menor que um assoalho)
# e só na faixa do corpo da madeira (sem o ronco grave do piso e sem o chiado muito agudo)
corpo = lambda f: faixa(300, 3500)(f) * (1 + 1.5 * np.exp(-((np.log(f / 900)) / 0.5) ** 2))
r1 = eq(mono(O + "536365__kostas17__creaking-floor.flac", 0.3, 1.25, 1.2), corpo)
r2 = eq(mono(O + "536365__kostas17__creaking-floor.flac", 2.95, 3.85, 1.25), corpo)
r1, r2 = fade(r1 / rms(r1), 0.06, 0.15), fade(r2 / rms(r2), 0.06, 0.15)

# a pá do remo puxando a água, abafada e baixa, logo depois de cada rangido
agua = eq(mono(O + "338345__lubini__splashing-water-by-oars.flac", 1.6, 2.6), faixa(150, 1800))
agua = fade(agua / rms(agua), 0.08, 0.45)

put(r1, 0.0, 1.0)
put(agua, 0.45, 0.35)
put(r2, 1.3, 0.9)
put(agua, 1.75, 0.3)

out = fade(out, 0.005, 0.2)
out *= 10 ** (-26 / 20) / rms(out[: int(2.4 * SR)])       # -26 dB: aparece, mas fica por baixo da fala
out *= min(1.0, 0.7 / np.max(np.abs(out)))
gravar("audios/sons/rangido_barco.wav", out[:, None], SR)
print("ok", len(out) / SR)
