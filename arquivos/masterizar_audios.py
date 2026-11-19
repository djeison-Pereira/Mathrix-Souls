"""Masteriza os áudios do jogo: nivela o volume, comprime e limita (só NumPy; pygame só para ler .mp3).

Uso (dentro de arquivos):
    python masterizar_audios.py            -> masteriza audios/musica, audios/ambiente e audios/sons
    python masterizar_audios.py --lista    -> só mostra o volume de cada arquivo, sem mexer

O que faz, por tipo:
- Música: nivela devagar (a faixa não fica mais alta no meio), comprime e deixa todas em -24 dB (RMS).
  O volume final de cada faixa fica em GANHO_MUSICA, no notebook. Vira .mp3 mono (96 kbps), codificado pelo próprio
  Windows (wav_para_mp3.ps1); decodificar e codificar de novo perde um pouco de qualidade a cada vez.
- Ambiente: nivela e comprime, em -20 dB no arquivo; vira .mp3 (96 kbps); o volume final de cada um fica em GANHO_AMBIENTE, no notebook.
- Efeitos: comprime e iguala o volume, em ALVO_EFEITO (exceções em ALVO_EFEITO_ESPECIAL).
Rodar de novo é seguro (o resultado converge), mas comprime um pouco mais a cada vez.
"""
import glob
import os
import subprocess
import sys
import wave

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
AUDIOS = os.path.join(AQUI, "audios")

ALVO_MUSICA = -24.0                       # dB RMS no arquivo (o volume final é o GANHO_MUSICA do notebook)
ALVO_AMBIENTE = {"taverna": -20.0, "floresta": -20.0, "caverna": -20.0, "tempestade": -20.0}   # o volume final é o GANHO_AMBIENTE do notebook
ALVO_EFEITO = -22.0
ALVO_EFEITO_ESPECIAL = {"galo_vento": -29.0, "vez_do_jogador": -17.0, "dano": -19.0, "vento_janela": -26.0}
NAO_MEXER = {"abertura", "trovao"}                  # montado à mão (trovão + sino): ver NOTAS_DA_EQUIPE


# ----------------------------------------------------------------------------- arquivos
def ler(caminho):
    """-> (dados float (n, canais), taxa)."""
    if caminho.lower().endswith(".mp3"):
        os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
        import pygame
        pygame.mixer.init(44100, -16, 2)
        s = pygame.mixer.Sound(caminho)
        d = np.frombuffer(s.get_raw(), "<i2").reshape(-1, 2).astype(float) / 32768
        return d, 44100
    with wave.open(caminho) as w:
        d = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32768
        return d.reshape(-1, w.getnchannels()), w.getframerate()


def gravar(caminho, x, taxa):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(caminho, "wb") as w:
        w.setnchannels(x.shape[1])
        w.setsampwidth(2)
        w.setframerate(taxa)
        w.writeframes(pcm.tobytes())


def para_mono_22k(x, taxa):
    m = x.mean(1)
    if taxa == 44100:
        X = np.fft.rfft(m)
        X[np.fft.rfftfreq(len(m), 1 / taxa) > 10000] = 0
        return np.fft.irfft(X, len(m))[::2][:, None], 22050
    return m[:, None], taxa


# ----------------------------------------------------------------------------- medidas
def db(v):
    return 20 * np.log10(np.maximum(v, 1e-9))


def rms_ativo(x, taxa):
    """RMS (dB) só dos trechos que têm som (ignora silêncio), em janelas de 50 ms."""
    m = x.mean(1) if x.shape[1] > 1 else x[:, 0]
    w = max(1, int(0.05 * taxa))
    n = len(m) // w
    if n == 0:
        return db(np.sqrt((m ** 2).mean()))
    p = (m[: n * w].reshape(n, w) ** 2).mean(1)
    ativo = p[db(np.sqrt(p)) > -55]
    return db(np.sqrt(ativo.mean())) if len(ativo) else -90.0


# ----------------------------------------------------------------------------- processamento
def nivelar_devagar(x, taxa, alvo, janela_s=9, limite_db=14):
    """Gain riding lento: tira as subidas e descidas de volume da faixa (sem mexer em trechos mudos)."""
    m = x.mean(1)
    w = taxa
    n = max(1, -(-len(m) // w))            # arredonda para cima: nunca uma janela vazia
    r = db(np.array([np.sqrt((m[i * w:(i + 1) * w] ** 2).mean() + 1e-12) for i in range(n)]))
    k = janela_s
    sm = np.convolve(np.pad(r, (k // 2, k // 2), mode="edge"), np.ones(k) / k, mode="valid")
    g = np.clip(alvo - sm, -limite_db, limite_db)
    g = np.where(sm < -45, 0, g)            # silêncio (fim da faixa) não é levantado
    t = (np.arange(n) + 0.5) * w
    return x * (10 ** (np.interp(np.arange(len(m)), t, g) / 20))[:, None]


def comprimir(x, taxa, limiar_db, razao, ataque=0.01, soltura=0.25):
    """Compressor: reduz o que passa do limiar (em dB do envelope), com ataque e soltura suaves."""
    bloco = max(1, int(0.005 * taxa))
    m = np.abs(x).max(1)
    n = len(m) // bloco + 1
    env = np.array([m[i * bloco:(i + 1) * bloco].max() if i * bloco < len(m) else 0 for i in range(n)])
    a = np.exp(-bloco / (ataque * taxa))
    s = np.exp(-bloco / (soltura * taxa))
    suave = np.zeros(n)
    y = 0.0
    for i in range(n):
        y = a * y + (1 - a) * env[i] if env[i] > y else s * y + (1 - s) * env[i]
        suave[i] = y
    reducao = np.minimum(0, (limiar_db - db(suave))) * (1 - 1 / razao)   # dB (negativo)
    g = np.interp(np.arange(len(m)), (np.arange(n) + 0.5) * bloco, reducao)
    return x * (10 ** (g / 20))[:, None]


def ajustar_rms(x, taxa, alvo):
    return x * 10 ** ((alvo - rms_ativo(x, taxa)) / 20)


def limitar(x, teto):
    """Limitador suave: nada passa do teto, sem corte seco."""
    return teto * np.tanh(x / teto)


def pontas(x, taxa, entrada=0.01, saida=0.05):
    x = x.copy()
    a, b = int(entrada * taxa), int(saida * taxa)
    if a and len(x) > a:
        x[:a] *= np.linspace(0, 1, a)[:, None]
    if b and len(x) > b:
        x[-b:] *= np.linspace(1, 0, b)[:, None]
    return x


def aparar_cauda(x, taxa, relativo=0.02, sobra=0.06):
    """Corta o silêncio (quase mudo) no fim do efeito: o jogo espera o arquivo acabar antes de seguir."""
    a = np.abs(x).max(1)
    idx = np.where(a > a.max() * relativo)[0]
    if not len(idx):
        return x
    fim = min(len(x), idx[-1] + 1 + int(sobra * taxa))
    return x[:fim]


def masterizar_musica(x, taxa):
    x, taxa = para_mono_22k(x, taxa)
    x = nivelar_devagar(x, taxa, ALVO_MUSICA)
    x = comprimir(x, taxa, -20.0, 2.5, 0.02, 0.4)
    return limitar(ajustar_rms(x, taxa, ALVO_MUSICA), 0.9), taxa


def masterizar_ambiente(x, taxa, alvo):
    x, taxa = para_mono_22k(x, taxa)
    x = nivelar_devagar(x, taxa, alvo, janela_s=5, limite_db=8)
    x = comprimir(x, taxa, alvo + 8, 2.5, 0.02, 0.4)
    return limitar(ajustar_rms(x, taxa, alvo), 0.8), taxa


def masterizar_efeito(x, taxa, alvo):
    x = comprimir(x, taxa, -20.0, 3.0, 0.003, 0.12)
    x = ajustar_rms(x, taxa, alvo)
    return pontas(aparar_cauda(limitar(x, 0.8), taxa), taxa), taxa


# ----------------------------------------------------------------------------- principal
def main():
    so_listar = "--lista" in sys.argv
    so_estes = [a for a in sys.argv[1:] if not a.startswith("--")]   # nomes: só esses arquivos
    pastas = [("musica", "*.mp3"), ("musica", "*.wav"), ("ambiente", "*.mp3"), ("ambiente", "*.wav"), ("sons", "*.wav")]
    arquivos = [(sub, c) for sub, padrao in pastas for c in sorted(glob.glob(os.path.join(AUDIOS, sub, padrao)))]
    for sub, caminho in arquivos:
        if True:
            nome = os.path.splitext(os.path.basename(caminho))[0]
            if so_estes and nome not in so_estes:
                continue
            x, taxa = ler(caminho)
            antes = rms_ativo(x, taxa)
            if so_listar:
                print(f"{sub}/{nome:20s} RMS {antes:6.1f} dB   pico {np.abs(x).max():.2f}")
                continue
            if sub == "sons" and nome in NAO_MEXER:
                print(f"{sub}/{nome:20s} (não mexe)")
                continue
            if sub == "musica":
                y, t = masterizar_musica(x, taxa)
            elif sub == "ambiente":
                y, t = masterizar_ambiente(x, taxa, ALVO_AMBIENTE.get(nome, -28.0))
            else:
                y, t = masterizar_efeito(x, taxa, ALVO_EFEITO_ESPECIAL.get(nome, ALVO_EFEITO))
            base = os.path.splitext(caminho)[0]
            if sub in ("musica", "ambiente"):    # música e ambiente: viram .mp3 (Low = 96 kbps) com o codificador do Windows
                gravar(base + ".tmp.wav", y, t)
                subprocess.run(["powershell", "-NoProfile", "-File", os.path.join(AQUI, "wav_para_mp3.ps1"),
                                base + ".tmp.wav", base + ".mp3", "Low"], check=True, capture_output=True)
                os.remove(base + ".tmp.wav")
                destino = base + ".mp3"
                if caminho != destino:
                    os.remove(caminho)           # o .wav antigo
            else:
                destino = base + ".wav"
                gravar(destino, y, t)
            print(f"{sub}/{nome:20s} {antes:6.1f} -> {rms_ativo(y, t):6.1f} dB   pico {np.abs(y).max():.2f}")


if __name__ == "__main__":
    main()
