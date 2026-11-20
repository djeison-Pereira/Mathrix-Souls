"""Gera o executável do Mathrix Souls.

Precisa de:  pip install pyinstaller numpy comtypes pygame-ce
Uso (na pasta arquivos):

    python gerar_exe.py            -> MathrixSouls.exe de DESENVOLVIMENTO, na pasta principal.
                                      Ele lê o notebook e os áudios da pasta 'arquivos' toda vez que abre:
                                      mudou uma fala ou o código no notebook? É só abrir o .exe de novo.

    python gerar_exe.py --entrega  -> entrega/MathrixSouls.exe de ENTREGA.
                                      Leva o notebook e todas as gravações DENTRO dele: funciona sozinho,
                                      sem nenhuma outra pasta. Gere de novo sempre que mudar algo.

    python gerar_exe.py --pasta    -> ESTA É A ENTREGA: entrega/MathrixSouls/ (a pasta do jogo) e entrega/MathrixSouls_pasta.zip.
                                      Igual à entrega, mas em PASTA em vez de um arquivo só: o .exe não se
                                      descompacta ao abrir, o que costuma assustar menos os antivírus.
                                      Quem receber extrai o .zip e abre MathrixSouls.exe de dentro da pasta.

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


def gerar(entrega=False, pasta=False):
    entrega = entrega or pasta
    destino = os.path.join(RAIZ, "entrega") if entrega else RAIZ
    with tempfile.TemporaryDirectory() as temp:
        comando = [
            sys.executable, "-m", "PyInstaller",
            "--onedir" if pasta else "--onefile",     # pasta com o .exe, ou um arquivo só
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
    if pasta:
        exe = os.path.join(destino, "MathrixSouls", "MathrixSouls.exe")
        arquivo_zip = shutil.make_archive(os.path.join(destino, "MathrixSouls_pasta"), "zip", root_dir=destino,
                                          base_dir="MathrixSouls")      # o zip leva a pasta "MathrixSouls" inteira
        print(f"\nPronto (pasta): {exe}\nZip: {arquivo_zip} ({os.path.getsize(arquivo_zip) // 1024 // 1024} MB)")
        return exe
    exe = os.path.join(destino, "MathrixSouls.exe")
    print(f"\nPronto ({'entrega' if entrega else 'desenvolvimento'}): {exe}")
    return exe


if __name__ == "__main__":
    argumentos = sys.argv[1:]
    desconhecidos = [a for a in argumentos if a not in ("--entrega", "--pasta")]
    if desconhecidos:                                # não gera nada com uma opção digitada errado
        sys.exit(f"Opção desconhecida: {' '.join(desconhecidos)}. Use --entrega, --pasta ou nada.")
    gerar(entrega="--entrega" in argumentos, pasta="--pasta" in argumentos)
