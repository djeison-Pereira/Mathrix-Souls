"""Iniciador do Mathrix Souls: é o código do MathrixSouls.exe.

Ele lê o notebook `mathrix_souls.ipynb` e roda as células de código, sem precisar de Jupyter.
- .exe de desenvolvimento: lê o notebook e as gravações da pasta 'arquivos' toda vez que abre,
  então mudanças nas falas e no código valem sem gerar o .exe de novo.
- .exe de entrega (gerar_exe.py --entrega): leva o notebook e as gravações dentro dele.

Uso sem .exe (na pasta arquivos):  python iniciar_jogo.py
Para gerar o .exe:                  python gerar_exe.py
"""
import json
import os
import sys
import traceback

# Bibliotecas que o notebook usa. O import aqui faz o PyInstaller colocá-las dentro do .exe.
import base64       # noqa: F401
import random       # noqa: F401
import subprocess   # noqa: F401
import time         # noqa: F401
import winsound     # noqa: F401
from collections import defaultdict  # noqa: F401

import numpy        # noqa: F401
import comtypes.client  # noqa: F401  (voz da Maria via SAPI)

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame       # noqa: F401,E402  (toca as gravações em .wav, .mp3 e .ogg)

NOTEBOOK = "mathrix_souls.ipynb"


def achar_notebook():
    """Retorna (caminho do notebook, pasta de trabalho, se é o .exe de entrega).
    - .exe de ENTREGA: usa só o notebook e os áudios que estão dentro dele.
    - .exe de DESENVOLVIMENTO (ou o script): lê a pasta 'arquivos' ao lado, então
      mudanças no notebook e gravações novas valem na hora, sem gerar o .exe de novo."""
    interno = getattr(sys, "_MEIPASS", None)
    if interno and os.path.exists(os.path.join(interno, "entrega.marca")):
        return os.path.join(interno, NOTEBOOK), interno, True
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    for pasta in (os.path.join(base, "arquivos"), base):
        if os.path.exists(os.path.join(pasta, NOTEBOOK)):
            return os.path.join(pasta, NOTEBOOK), pasta, False
    raise FileNotFoundError(
        f"Não achei o {NOTEBOOK}. Este é o .exe de desenvolvimento: ele precisa da pasta 'arquivos' "
        "ao lado. Para um .exe que funciona sozinho, gere o de entrega (python gerar_exe.py --entrega).")


def main():
    notebook, pasta, _entrega = achar_notebook()
    os.chdir(pasta)  # para achar a pasta audios/
    with open(notebook, encoding="utf-8") as f:
        nb = json.load(f)
    ambiente = {"__name__": "__main__"}
    for celula in nb["cells"]:
        if celula["cell_type"] != "code":
            continue
        codigo = "".join(celula["source"])
        if codigo.strip() == "jogar()":
            break  # para antes do Apêndice; o jogo começa logo abaixo
        exec(compile(codigo, NOTEBOOK, "exec"), ambiente)
    ambiente["jogar"]()


if __name__ == "__main__":
    if os.name == "nt":
        os.system("title Mathrix Souls")
    try:
        main()
    except Exception:
        traceback.print_exc()
        print("\nO jogo encontrou um erro e precisa fechar. Aperte Enter para sair.")
        try:
            import winsound as _w
            _w.MessageBeep()
        except Exception:
            pass
        input()
