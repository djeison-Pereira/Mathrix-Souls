"""Gera Material/Historia_do_Jogo.pdf: a história inteira do jogo, para ler sem jogar.

Joga o jogo sozinho (sem som, no caminho principal, acertando tudo) e monta o PDF com as falas em ordem.
As falas de outros caminhos (erros, outras escolhas) vão num apêndice.

Uso (dentro de arquivos; precisa de  pip install reportlab):
    python gerar_historia_pdf.py
"""
import contextlib, datetime, io, json, os, re, sys
from xml.sax.saxutils import escape
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["SDL_AUDIODRIVER"] = "dummy"
AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)

# ---------------------------------------------------------------- 1) joga o jogo inteiro, sem som
nb = json.load(open("mathrix_souls.ipynb", encoding="utf-8"))
g = {"__name__": "__main__"}
with contextlib.redirect_stdout(io.StringIO()):
    for c in nb["cells"]:
        if c["cell_type"] != "code":
            continue
        fonte = "".join(c["source"])
        if fonte.strip() == "jogar()":
            break
        exec(compile(fonte, "nb", "exec"), g)
buf = io.StringIO()
g["MODO_TESTE"] = True
g["VELOCIDADE"] = 0
g["bipe"] = lambda *a, **k: None
g["musica"] = lambda nome, fade_ms=None: None
g["ambiente"] = lambda nome, fade_ms=None: None
g["apagar_save"] = lambda: None
g["falar_em_voz"] = lambda *a, **k: None
g["usar_gravacoes"] = False
visto = set()
orig_anunciar = g["anunciar"]


def anunciar(quem, texto, pecas=None, pausa=0.6, dizer_nome=False):
    if not dizer_nome:
        visto.add((quem, texto))
        print(f"##F|{quem}|{texto}")
    with contextlib.redirect_stdout(io.StringIO()):
        orig_anunciar(quem, texto, pecas, 0, dizer_nome)


g["anunciar"] = anunciar


def ler_tecla():
    t = g["estado"].resposta_certa
    print(f"##K|{t}")
    return t


g["ler_tecla"] = ler_tecla
orig_trilha = g["trilha_da_cena"]


def trilha(cena):
    print(f"##C|{cena.__name__}")
    return orig_trilha(cena)


g["trilha_da_cena"] = trilha
try:
    with contextlib.redirect_stdout(buf):
        g["jogar_roteiro"](g["ROTEIRO_COMPLETO"], "completo")
except BaseException as ex:
    print("fim:", type(ex).__name__, ex)
linhas = buf.getvalue().split("\n")

# ---------------------------------------------------------------- 2) transforma em blocos
TITULOS = {
    "cena_1_casa": "Cena 1: A Casa", "cena_2_taverna": "Cena 2: A Taverna", "cena_3_licao": "Cena 3: A Lição",
    "cena_4_grilo": "Cena 4: O Grilo Falante", "cena_5_bifurcacao": "Cena 5: A Bifurcação",
    "cena_6_goblin": "Cena 6: O Goblin", "cena_7_praia": "Cena 7: A Praia", "cena_8_barco": "Cena 8: O Barco",
    "cena_9_farol": "Cena 9: O Farol", "cena_10_masmorra": "Cena 10: A Masmorra",
    "cena_11_guardiao": "Cena 11: O Guardião", "cena_12_dragao": "Cena 12: O Dragão", "epilogo": "Epílogo",
}
blocos = []        # (tipo, a, b)
matriz = []


def fecha_matriz():
    global matriz
    if matriz:
        blocos.append(("matriz", "\n".join(matriz), ""))
        matriz = []


for ln in linhas:
    if ln.startswith("##C|"):
        fecha_matriz()
        blocos.append(("cena", TITULOS.get(ln[4:], ln[4:]), ""))
    elif ln.startswith("##F|"):
        fecha_matriz()
        _, quem, texto = ln.split("|", 2)
        blocos.append(("fala", quem, texto))
    elif ln.startswith("##K|"):
        fecha_matriz()
        blocos.append(("tecla", ln[4:], ""))
    elif ln.startswith("[som:"):
        fecha_matriz()
        blocos.append(("som", ln[5:].rstrip("]").strip(), ""))
    elif ln.startswith(" ") and ln.strip():
        matriz.append(ln.rstrip())
    elif not ln.strip():
        fecha_matriz()
fecha_matriz()
print("blocos:", len(blocos))

# falas que não apareceram nesse caminho (outras escolhas, erros, dicas)
PREF = {"N", "A", "T", "MX", "ME", "G", "GB", "MR", "CF", "DR", "GO", "V"}
nao_vistas = {}
for codigo, (quem, texto) in g["FALAS"].items():
    m = re.match(r"^([A-Z]+)(\d{2})_", codigo)
    if not m or m.group(1) not in PREF or (quem, texto) in visto:
        continue
    nao_vistas.setdefault(int(m.group(2)), []).append((quem, texto))

# ---------------------------------------------------------------- 3) PDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Preformatted, Spacer

AZUL = colors.HexColor("#2f6db5")
CINZA = colors.HexColor("#777777")
st = {
    "capa": ParagraphStyle("capa", fontName="Helvetica-Bold", fontSize=30, leading=34, spaceAfter=6),
    "sub": ParagraphStyle("sub", fontName="Helvetica", fontSize=12, leading=17, textColor=CINZA, spaceAfter=14),
    "cena": ParagraphStyle("cena", fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=AZUL,
                           spaceBefore=4, spaceAfter=8, keepWithNext=True),
    "nar": ParagraphStyle("nar", fontName="Times-Roman", fontSize=11, leading=15.5, spaceAfter=7),
    "fala": ParagraphStyle("fala", fontName="Times-Roman", fontSize=11, leading=15.5, spaceAfter=7, leftIndent=14),
    "sis": ParagraphStyle("sis", fontName="Helvetica-Oblique", fontSize=9.5, leading=13, textColor=CINZA,
                          spaceAfter=7, leftIndent=14),
    "som": ParagraphStyle("som", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=CINZA,
                          spaceAfter=5, spaceBefore=2),
    "tecla": ParagraphStyle("tecla", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=AZUL,
                            spaceAfter=8, leftIndent=14),
    "txt": ParagraphStyle("txt", fontName="Helvetica", fontSize=10, leading=14, spaceAfter=6),
    "mx": ParagraphStyle("mx", fontName="Courier", fontSize=10, leading=12, leftIndent=30, spaceAfter=8, spaceBefore=2),
}


def rodape(c, doc):
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor("#888888"))
    c.drawString(40, 28, "Mathrix Souls: a história do jogo")
    c.drawRightString(A4[0] - 40, 28, f"página {doc.page}")


def paragrafo(quem, texto):
    if quem == "Narrador":
        return Paragraph(escape(texto), st["nar"])
    if quem == "Sistema":
        return Paragraph(escape(texto), st["sis"])
    return Paragraph(f"<b>{escape(quem)}:</b> {escape(texto)}", st["fala"])


saida = os.path.join(AQUI, "Material", "Historia_do_Jogo.pdf")
doc = BaseDocTemplate(saida, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=44, bottomMargin=48,
                      title="Mathrix Souls: a história do jogo", author="Equipe Mathrix Souls")
doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(40, 48, A4[0] - 80, A4[1] - 92, id="f")], onPage=rodape)])
E = [Spacer(1, 120), Paragraph("Mathrix Souls", st["capa"]),
     Paragraph("A história do jogo, para ler sem jogar", st["sub"]),
     Paragraph("Este texto segue o caminho principal da história: o jogador faz as escolhas esperadas e acerta "
               "as magias de matriz. Os efeitos sonoros aparecem em itálico, entre colchetes, e as teclas que o "
               "jogador aperta aparecem em azul. No fim, o apêndice traz as falas que ficam de fora desse caminho "
               "(outras escolhas, erros e dicas).", st["txt"]),
     Paragraph(f"Gerado em {datetime.date.today():%d/%m/%Y} a partir do próprio jogo.", st["sub"])]
for tipo, a, b in blocos:
    if tipo == "cena":
        E.append(PageBreak())
        E.append(Paragraph(escape(a), st["cena"]))
    elif tipo == "fala":
        E.append(paragrafo(a, b))
    elif tipo == "som":
        E.append(Paragraph(f"[som: {escape(a)}]", st["som"]))
    elif tipo == "tecla":
        E.append(Paragraph(f"Você aperta {escape(a) if a else 'Enter'}.", st["tecla"]))
    elif tipo == "matriz":
        E.append(Preformatted(a, st["mx"]))
if nao_vistas:
    E.append(PageBreak())
    E.append(Paragraph("Apêndice: falas de outros caminhos", st["cena"]))
    E.append(Paragraph("Falas por onde o caminho principal não passa: respostas diferentes, erros do jogador "
                       "e dicas. Estão agrupadas por cena, na ordem do roteiro.", st["txt"]))
    cab = ParagraphStyle("h", parent=st["txt"], fontName="Helvetica-Bold", textColor=AZUL, spaceBefore=8,
                         keepWithNext=True)
    for n in sorted(nao_vistas):
        E.append(Paragraph(f"Cena {n}", cab))
        for quem, texto in nao_vistas[n]:
            E.append(paragrafo(quem, texto))
doc.build(E)
print("ok:", saida, os.path.getsize(saida) // 1024, "KB; apêndice:", sum(len(v) for v in nao_vistas.values()), "falas")
