"""Gera o executável do Mathrix Souls.

Precisa de:  pip install pyinstaller numpy comtypes pygame-ce
Uso (na pasta arquivos):

    python gerar_exe.py            -> MathrixSouls.exe de DESENVOLVIMENTO, na pasta principal.
                                      Ele lê o notebook e os áudios da pasta 'arquivos' toda vez que abre:
                                      mudou uma fala ou o código no notebook? É só abrir o .exe de novo.

    python gerar_exe.py --entrega  -> entrega/MathrixSouls.exe de ENTREGA.
                                      Leva o notebook e todas as gravações DENTRO dele: funciona sozinho,
                                      sem nenhuma outra pasta. Gere de novo sempre que mudar algo.

O .exe de desenvolvimento só precisa ser gerado de novo se o iniciador_jogo.py mudar
ou se o notebook passar a usar uma biblioteca nova.
"""
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
NOTEBOOK = os.path.join(AQUI, "mathrix_souls.ipynb")
AUDIOS = os.path.join(AQUI, "audios")


# Módulos que entram no .exe sem o jogo precisar deles (só deixam o arquivo maior).
EXCLUIR = ["tkinter", "yaml", "psutil", "charset_normalizer", "pydoc_data", "unittest", "xmlrpc", "test",
           "asyncio", "multiprocessing", "concurrent", "http", "urllib", "email", "ssl", "bz2", "lzma", "xml",
           "hashlib", "_hashlib", "hmac", "secrets",
           "pygame.font", "pygame.freetype", "pygame.sysfont", "pygame.image", "pygame.imageext"]   # o jogo só usa o áudio do pygame


def gerar(entrega=False):
    destino = os.path.join(RAIZ, "entrega") if entrega else RAIZ
    with tempfile.TemporaryDirectory() as temp:
        comando = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",                      # um arquivo só
            "--console",                      # janela de texto: o jogo usa teclado e voz
            "--name", "MathrixSouls",
            "--collect-submodules", "comtypes",
            "--exclude-module", "comtypes.test",
            *[arg for modulo in EXCLUIR for arg in ("--exclude-module", modulo)],   # tira o que o jogo não usa (.exe menor)
            "--distpath", destino,
            "--workpath", os.path.join(temp, "build"),
            "--specpath", temp,
            "--noconfirm", "--clean",
        ]
        if entrega:
            marca = os.path.join(temp, "entrega.marca")   # avisa o iniciador: use só o que está dentro
            open(marca, "w").close()
            comando += [
                "--add-data", f"{NOTEBOOK}{os.pathsep}.",
                "--add-data", f"{AUDIOS}{os.pathsep}audios",
                "--add-data", f"{marca}{os.pathsep}.",
            ]
        comando.append(os.path.join(AQUI, "iniciar_jogo.py"))
        subprocess.run(comando, check=True)
    shutil.rmtree(os.path.join(AQUI, "__pycache__"), ignore_errors=True)
    exe = os.path.join(destino, "MathrixSouls.exe")
    print(f"\nPronto ({'entrega' if entrega else 'desenvolvimento'}): {exe}")
    return exe


if __name__ == "__main__":
    gerar(entrega="--entrega" in sys.argv)
