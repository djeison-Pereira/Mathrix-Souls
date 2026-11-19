"""Gera o roteiro de gravação do Mathrix Souls (PDF), direto das falas do notebook.

Uso (dentro de arquivos):
    python gerar_roteiro_gravacao.py

Gera:
    Material/Roteiro_de_Gravacao.pdf                  -> o roteiro completo (todas as pessoas + efeitos sonoros)
    Material/Roteiros_por_pessoa/Roteiro_<nome>.pdf   -> um PDF só com as falas de cada pessoa

Sempre que uma fala mudar no notebook, é só rodar de novo: o PDF sai com os textos e códigos atuais.
Precisa de:  pip install reportlab
"""
import datetime
import json
import os
import re
import sys
from xml.sax.saxutils import escape

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")      # só para o notebook carregar sem abrir som

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether)
from reportlab.platypus.tableofcontents import TableOfContents

AQUI = os.path.dirname(os.path.abspath(__file__))
NOTEBOOK = os.path.join(AQUI, "mathrix_souls.ipynb")
SAIDA = os.path.join(AQUI, "Material")

# ------------------------------------------------------------------------------------------ quem grava
# (nome, [personagens]). Para trocar alguém de lugar, é só mexer aqui e rodar de novo.
PESSOAS = [
    ("Felipe", ["Narrador", "Grilo Falante"]),
    ("Vinícius", ["Goblin", "Max", "Ecos"]),
    ("Matheus", ["Taverneiro", "Cavaleiro Fantasma"]),
    ("João", ["Marinheiro", "Dragão"]),
    ("Daniel", ["Alquimista", "Golem"]),
    ("A definir", ["Mãe"]),
]
COMO_FALAR = {
    "Narrador": "Calmo e claro, ritmo de contador de histórias.",
    "Grilo Falante": "Agudo, rápido e animado. Tagarela.",
    "Goblin": "Agudo, apressado, debochado.",
    "Max": "Bêbado: arrastado, meio dormindo.",
    "Ecos": "Sussurrado, grave e lento. Vozes de magos que não voltaram.",
    "Taverneiro": "Grandalhão simpático, animado, voz de balcão.",
    "Cavaleiro Fantasma": "Frio, solene, antigo.",
    "Marinheiro": "Velho, rouco, gasto pelo sal. Fala devagar.",
    "Dragão": "O mais grave de todos, lento e ameaçador.",
    "Alquimista": "Convencido e teatral, mas no fundo preocupado.",
    "Golem": "Grave e bem lento. Frases curtas, como pedra.",
    "Mãe": "Carinhosa, devagar, como quem lê um bilhete em voz alta.",
    "Sistema": "Neutro e curto. Hoje sai na voz do computador.",
}
# falas que existem no código, mas o jogo não usa mais (não precisam ser gravadas)
NAO_USADAS = {"N08_0.75", "N08_1.0", "N08_1.25", "N08_1.5", "N08_2.0", "N08_2.5", "N08_3.0", "N08_max", "N08_min", "N09"}

AZUL = colors.HexColor("#2f6db5")
ESCURO = colors.HexColor("#2b2b2b")
CINZA = colors.HexColor("#777777")
LINHA = colors.HexColor("#dddddd")
FAIXA = colors.HexColor("#eef3fa")



# ------------------------------------------------------------------------------------------ dados
def carregar_notebook():
    """Roda o notebook (até antes do ▶ Jogar) e devolve (falas na ordem, globais do jogo)."""
    nb = json.load(open(NOTEBOOK, encoding="utf-8"))
    g = {"__name__": "__main__"}
    secao = "Falas do jogo"
    ordem = []                                           # (codigo, quem, texto, secao)
    for celula in nb["cells"]:
        fonte = "".join(celula["source"])
        if celula["cell_type"] == "markdown":
            for linha in fonte.split("\n"):
                m = re.match(r"#{1,3}\s+(Cena .+|Epílogo.+|Pedaços.+|Parte 2.+)", linha.strip())
                if m:
                    secao = m.group(1).strip()
                    if secao.startswith("Parte 2"):
                        secao = "Menu, instruções e avisos do jogo"
                    elif secao.startswith("Pedaços"):
                        secao = "Pedaços curtos (números e partes das frases de matriz)"
                    break
            continue
        if fonte.strip() == "jogar()":
            break
        antes = set(g.get("FALAS", {}))
        exec(compile(fonte, NOTEBOOK, "exec"), g)
        for codigo, (quem, texto) in g.get("FALAS", {}).items():
            if codigo not in antes:
                ordem.append((codigo, quem, texto, secao))
    return [f for f in ordem if f[0] not in NAO_USADAS], g


# ------------------------------------------------------------------------------------------ estilos
def estilos():
    base = dict(fontName="Helvetica", fontSize=9, leading=12)
    return {
        "capa": ParagraphStyle("capa", fontName="Helvetica-Bold", fontSize=28, leading=32, spaceAfter=4),
        "sub": ParagraphStyle("sub", fontName="Helvetica", fontSize=12, leading=16, textColor=CINZA, spaceAfter=14),
        "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=20, leading=24, spaceAfter=6, textColor=ESCURO),
        "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=14, leading=18, spaceBefore=10, spaceAfter=2, textColor=AZUL),
        "h3": ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=9.5, leading=13, spaceBefore=8, spaceAfter=3,
                             backColor=FAIXA, borderPadding=(3, 4, 3, 4), keepWithNext=True),
        "txt": ParagraphStyle("txt", spaceAfter=4, **base),
        "peq": ParagraphStyle("peq", fontName="Helvetica", fontSize=8, leading=10.5, textColor=CINZA),
        "cel": ParagraphStyle("cel", **base),
        "arq": ParagraphStyle("arq", fontName="Helvetica-Bold", fontSize=8, leading=10.5),
        "hd": ParagraphStyle("hd", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=colors.white),
        "toc1": ParagraphStyle("toc1", fontName="Helvetica-Bold", fontSize=10.5, leading=14.5, leftIndent=0),
        "toc2": ParagraphStyle("toc2", fontName="Helvetica", fontSize=9, leading=12, leftIndent=16, textColor=CINZA),
    }


class Titulo(Paragraph):
    """Parágrafo que vira marcador do PDF e entrada do sumário."""
    def __init__(self, texto, estilo, nivel, chave):
        super().__init__(escape(texto), estilo)
        self.texto, self.nivel, self.chave = texto, nivel, chave


class Documento(BaseDocTemplate):
    def __init__(self, arquivo, titulo_rodape, **kw):
        super().__init__(arquivo, pagesize=A4, leftMargin=34, rightMargin=34, topMargin=40, bottomMargin=48, **kw)
        self.titulo_rodape = titulo_rodape
        quadro = Frame(34, 48, A4[0] - 68, A4[1] - 88, id="f")
        self.addPageTemplates([PageTemplate(id="p", frames=[quadro], onPage=self.rodape)])

    def rodape(self, c, doc):
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(34, 28, self.titulo_rodape)
        c.drawRightString(A4[0] - 34, 28, f"página {doc.page}")

    def afterFlowable(self, f):
        if isinstance(f, Titulo):
            self.canv.bookmarkPage(f.chave)
            self.canv.addOutlineEntry(f.texto, f.chave, f.nivel, 0)
            self.notify("TOCEntry", (f.nivel, f.texto, self.page, f.chave))


# ------------------------------------------------------------------------------------------ montagem
def tabela_de_falas(linhas, e):
    """linhas: [(codigo, texto)] -> tabela [ ] arquivo | fala."""
    dados = [[Paragraph("", e["cel"]), Paragraph("Arquivo", e["hd"]), Paragraph("Fala", e["hd"])]]
    for codigo, texto in linhas:
        dados.append(["", Paragraph(escape(codigo) + ".ogg", e["arq"]), Paragraph(escape(texto), e["cel"])])
    t = Table(dados, colWidths=[16, 112, A4[0] - 68 - 16 - 112], repeatRows=1)
    estilo = [("BACKGROUND", (0, 0), (-1, 0), ESCURO), ("VALIGN", (0, 0), (-1, -1), "TOP"),
              ("LINEBELOW", (0, 1), (-1, -1), 0.4, LINHA), ("TOPPADDING", (0, 0), (-1, -1), 3.5),
              ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5)]
    for i in range(1, len(dados)):
        estilo.append(("BOX", (0, i), (0, i), 0.6, colors.HexColor("#999999")))   # caixinha para marcar "gravado"
    t.setStyle(TableStyle(estilo))
    return t


def instrucoes(e):
    itens = [
        "<b>Uma fala por arquivo</b>, com o nome exato da coluna <b>Arquivo</b> (ex.: <b>T02_01.ogg</b>). Maiúsculas, números e o "
        "sublinhado precisam ficar iguais.",
        "<b>Formato:</b> .ogg (ou .mp3) em <b>mono</b>. No Audacity: Arquivo &gt; Exportar &gt; Exportar como OGG, com o canal em mono.",
        "<b>Onde salvar:</b> mande os arquivos para quem cuida do jogo; ele coloca em <b>arquivos/audios</b>. O jogo toca a "
        "gravação sozinho; o que ainda não foi gravado continua na voz do computador.",
        "<b>Sem silêncio</b> no começo nem no fim. Nos <b>pedaços curtos</b> (números, \"em cima\", \"opção A\"...) isso é "
        "obrigatório: eles são tocados um atrás do outro para formar frases.",
        "<b>Não diga o nome do personagem</b> antes da fala, nem nada que não esteja no texto: grave só o que está escrito.",
        "<b>Ouça o jogo antes:</b> cada personagem já tem uma voz do computador com o tom e o ritmo parecidos com os do "
        "papel. Use isso como guia.",
        "As falas estão na <b>ordem em que aparecem no jogo</b>, separadas por cena. Algumas só tocam numa escolha do jogador "
        "(por exemplo, se ele fala com o Max ou se erra uma resposta); essas também precisam ser gravadas.",
        "Use a caixinha à esquerda de cada linha para marcar o que já gravou.",
    ]
    return [Paragraph("&bull; " + i, e["txt"]) for i in itens]


def secao_pessoa(nome, personagens, falas, e, chave):
    """Todas as falas de uma pessoa, personagem por personagem e cena por cena."""
    out = []
    por_personagem = {p: [f for f in falas if f[1] == p] for p in personagens}
    total = sum(len(v) for v in por_personagem.values())
    out.append(Titulo(nome, e["h1"], 0, chave))
    resumo = " · ".join(f"{p} ({len(v)})" for p, v in por_personagem.items())
    out.append(Paragraph(f"<b>{total} falas</b> &nbsp;|&nbsp; {escape(resumo)}", e["txt"]))
    for p, lista in por_personagem.items():
        out.append(Titulo(f"{p} ({len(lista)} falas)", e["h2"], 1, f"{chave}_{re.sub('[^A-Za-z0-9]', '', p)}"))
        out.append(Paragraph(f"<b>Como falar:</b> {escape(COMO_FALAR.get(p, ''))}", e["txt"]))
        secoes = []
        for codigo, _q, texto, sec in lista:
            if not secoes or secoes[-1][0] != sec:
                secoes.append((sec, []))
            secoes[-1][1].append((codigo, texto))
        for sec, linhas in secoes:
            out.append(Paragraph(escape(f"{sec}  ·  {len(linhas)}"), e["h3"]))
            out.append(tabela_de_falas(linhas, e))
    return out


def tabela_de_sons(g, e):
    existe = lambda nome: any(os.path.exists(os.path.join(AQUI, "audios", sub, nome + ext))
                              for sub in ("sons", "ambiente") for ext in (".wav", ".mp3", ".ogg"))
    redundantes = set(g.get("SOM_REDUNDANTE", ()))
    dados = [[Paragraph(x, e["hd"]) for x in ("Arquivo", "Quando toca", "O que o jogador ouve", "Busca sugerida", "Situação")]]
    for nome, cena, desc, busca, obs in SONS:
        if existe(nome):
            sit = '<font color="#2e7d32"><b>OK</b></font>'
        elif nome in redundantes:
            sit = '<font color="#b26a00"><b>FALTA</b></font><br/>a narração já cobre'
        else:
            sit = '<font color="#b26a00"><b>FALTA</b></font><br/>o Narrador diz'
        obs = obs.strip("; ")
        d = [Paragraph(escape(desc), e["cel"])] + ([Paragraph(escape(obs), e["peq"])] if obs else [])
        dados.append([Paragraph(escape(nome) + ".ogg", e["arq"]), Paragraph(escape(cena), e["cel"]), d,
                      Paragraph(escape(busca), e["cel"]), Paragraph(sit, e["cel"])])
    t = Table(dados, colWidths=[98, 80, 155, 88, 74], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), ESCURO), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LINEBELOW", (0, 1), (-1, -1), 0.4, LINHA), ("TOPPADDING", (0, 0), (-1, -1), 4),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def pagina_de_personagens(e):
    dados = [[Paragraph(x, e["hd"]) for x in ("Personagem", "Quem grava", "Como falar")]]
    quem = {p: n for n, ps in PESSOAS for p in ps}
    quem["Sistema"] = "voz do computador"
    for p, como in COMO_FALAR.items():
        dados.append([Paragraph(f"<b>{escape(p)}</b>", e["cel"]), Paragraph(escape(quem.get(p, "")), e["cel"]),
                      Paragraph(escape(como), e["cel"])])
    t = Table(dados, colWidths=[110, 90, A4[0] - 68 - 200], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), ESCURO), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LINEBELOW", (0, 1), (-1, -1), 0.4, LINHA), ("TOPPADDING", (0, 0), (-1, -1), 3.5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5)]))
    return t


def gerar_pdf(destino, pessoas, falas, g, completo):
    e = estilos()
    nomes = ", ".join(n for n, _ in pessoas)
    rodape = "Mathrix Souls · Roteiro de gravação" + ("" if completo else f" · {pessoas[0][0]}")
    doc = Documento(destino, rodape, title="Mathrix Souls - Roteiro de gravação", author="Equipe Mathrix Souls")
    hoje = datetime.date.today().strftime("%d/%m/%Y")
    historia = []

    historia.append(Paragraph("Mathrix Souls", e["capa"]))
    historia.append(Paragraph("Roteiro de gravação das vozes" + ("" if completo else f" — {escape(pessoas[0][0])}"), e["sub"]))
    historia.append(Paragraph(f"Atualizado em {hoje}. Cada fala, o nome do arquivo e quem grava.", e["peq"]))
    historia.append(Spacer(1, 10))

    # resumo de quem grava
    dados = [[Paragraph(x, e["hd"]) for x in ("Quem grava", "Personagens", "Falas")]]
    for nome, ps in pessoas:
        n = sum(1 for f in falas if f[1] in ps)
        dados.append([Paragraph(f"<b>{escape(nome)}</b>", e["cel"]),
                      Paragraph(escape(", ".join(f"{p} ({sum(1 for f in falas if f[1] == p)})" for p in ps)), e["cel"]),
                      Paragraph(str(n), e["cel"])])
    t = Table(dados, colWidths=[90, A4[0] - 68 - 90 - 50, 50])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), ESCURO), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LINEBELOW", (0, 1), (-1, -1), 0.4, LINHA), ("TOPPADDING", (0, 0), (-1, -1), 4),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    historia.append(t)
    historia.append(Paragraph("Os números incluem os pedaços curtos que o Narrador grava para o jogo ler as matrizes "
                              "(números, \"em cima\", \"opção A\"...).", e["peq"]))
    historia.append(Spacer(1, 14))

    if completo:
        historia.append(Paragraph("Sumário", e["h2"]))
        toc = TableOfContents()
        toc.levelStyles = [e["toc1"], e["toc2"]]
        historia.append(toc)
    historia.append(PageBreak())

    historia.append(Titulo("Como gravar", e["h1"], 0, "comogravar"))
    historia += instrucoes(e)
    historia.append(Spacer(1, 8))
    historia.append(Titulo("O jeito de cada personagem", e["h2"], 1, "jeito"))
    historia.append(pagina_de_personagens(e))

    for nome, ps in pessoas:
        historia.append(PageBreak())
        historia += secao_pessoa(nome, ps, falas, e, "p_" + re.sub("[^A-Za-z0-9]", "", nome))

    if completo:
        sistema = [f for f in falas if f[1] == "Sistema"]
        historia.append(PageBreak())
        historia.append(Titulo("Sistema (voz do computador)", e["h1"], 0, "sistema"))
        historia.append(Paragraph("Estas falas <b>não precisam ser gravadas</b> por enquanto: saem na voz do computador. Ficam aqui "
                                  "só para consulta (avisos, vidas, pausa, comandos...). Se alguém quiser gravá-las, é só seguir o "
                                  "mesmo processo.", e["txt"]))
        secoes = []
        for codigo, _q, texto, sec in sistema:
            if not secoes or secoes[-1][0] != sec:
                secoes.append((sec, []))
            secoes[-1][1].append((codigo, texto))
        for sec, linhas in secoes:
            historia.append(Paragraph(escape(f"{sec}  ·  {len(linhas)}"), e["h3"]))
            historia.append(tabela_de_falas(linhas, e))

        historia.append(PageBreak())
        historia.append(Titulo("Efeitos sonoros", e["h1"], 0, "efeitos"))
        historia += [Paragraph("&bull; <b>Situação:</b> <b>OK</b> = o jogo já tem o som. <b>FALTA</b> = ainda não há som. \"O Narrador diz\": ele "
                               "fala a descrição do efeito. \"A narração já cobre\": a própria fala da cena já conta o que acontece, então o "
                               "jogo não repete. Ao colocar o arquivo em audios/sons com o nome da coluna, o jogo passa a tocá-lo sozinho.", e["txt"]),
                     Paragraph("&bull; <b>Fontes gratuitas:</b> freesound.org (filtrar por licença Creative Commons 0), pixabay.com/sound-effects, "
                               "opengameart.org. A coluna <b>Busca</b> traz um termo em inglês para pesquisar. Se a licença for CC-BY, o crédito do "
                               "autor precisa constar no jogo/relatório.", e["txt"]),
                     Spacer(1, 6), tabela_de_sons(g, e)]

    doc.multiBuild(historia)


# ------------------------------------------------------------------------------------------ principal
def main():
    falas, g = carregar_notebook()
    os.makedirs(os.path.join(SAIDA, "Roteiros_por_pessoa"), exist_ok=True)
    gerar_pdf(os.path.join(SAIDA, "Roteiro_de_Gravacao.pdf"), PESSOAS, falas, g, completo=True)
    print(f"Roteiro completo: {len(falas)} falas")
    for pessoa in PESSOAS:
        nome = re.sub(r"[^A-Za-z0-9]", "", pessoa[0].replace("í", "i").replace("ã", "a")) or "pessoa"
        destino = os.path.join(SAIDA, "Roteiros_por_pessoa", f"Roteiro_{nome}.pdf")
        gerar_pdf(destino, [pessoa], falas, g, completo=False)
        print(f"  {pessoa[0]:10s} {sum(1 for f in falas if f[1] in pessoa[1]):3d} falas -> {os.path.relpath(destino, AQUI)}")


# ------------------------------------------------------------------------------------------ efeitos sonoros
# (nome do arquivo, quando toca, o que o jogador ouve, busca sugerida em inglês, observação)
T = ""
SONS = [
 ("iniciar_jogo", "Ao apertar A ou D no menu", "um golpe de orquestra: a aventura começa", "epic game start orchestral hit", "toca junto do aviso de início, sem espera"),
 ("abertura", "Menu", "um trovão distante e um sino grave", "distant thunder deep bell", ""),
 ("vez_do_jogador", "Sempre que o jogo espera uma tecla", "bipe curto de \"sua vez\"", "ui notification beep short", "bem curto (menos de 0,3 s)"),
 ("dano", "Ao perder uma vida", "um impacto seco", "punch hit impact thud", ""),
 ("magia", "Ao aprender uma magia", "a pedra pulsa com um brilho quente", "magic spell chime sparkle", ""),
 ("galo_vento", "Cena 1 · Casa", "um galo canta ao longe", "rooster crow distant + wind window", T),
 ("vento_janela", "Cena 1 · Casa (depois do galo)", "o vento arranha a janela", "short soft wind gust whoosh", "curto (2 s), antes de o Narrador falar"),
 ("porta", "Cena 1 · Casa", "porta de madeira rangendo", "wooden door creak open", T),
 ("taverna", "Cena 2 · Taverna e Epílogo", "murmúrios, canecas batendo, lareira estalando", "tavern ambience crowd fireplace", T),
 ("frascos", "Cena 2 · Taverna", "frascos tilintando", "glass bottles clink potion", ""),
 ("teleporte", "Cena 2 · Taverna", "um estalar de dedos e um sopro de vento", "finger snap wind whoosh", ""),
 ("cajado_sino", "Cena 3 · Lição", "o cajado bate no chão e ecoa como um sino grave", "staff hit ground low bell", ""),
 ("grilo", "Cena 4 · Grilo", "cri-cri alegre vindo da esquerda", "cricket chirp", "estéreo: tudo no lado esquerdo"),
 ("passo", "Cena 4 · Grilo", "passos na folhagem (esquerda, direita, para trás)", "footsteps leaves foliage", "curto, 2 passos"),
 ("bifurcacao", "Cena 5 · Bifurcação", "pássaros e um riacho à esquerda; vento seco à direita", "forest birds stream", "estéreo: pássaros à esquerda, vento à direita"),
 ("vento_seco", "Cena 5 · Bifurcação", "vento seco, nenhum bicho", "dry wind desert", ""),
 ("desmoronamento", "Cena 5 · Bifurcação", "terra desmoronando", "dirt rocks collapse landslide", ""),
 ("golpe_esquerda", "Esquiva (Goblin)", "passos rápidos e um grito vindo da esquerda", "fast footsteps scream attack", "estéreo: só no fone esquerdo"),
 ("golpe_direita", "Esquiva (Goblin)", "passos rápidos e um grito vindo da direita", "fast footsteps scream attack", "estéreo: só no fone direito"),
 ("golpe_frente", "Esquiva (Goblin)", "passos rápidos e um grito vindo de frente", "fast footsteps scream attack", "mono, no centro"),
 ("esquiva", "Esquiva", "o golpe passa raspando", "whoosh swing near miss", ""),
 ("goblin_risada", "Cena 6 · Goblin", "risada aguda circulando ao seu redor", "goblin evil cackle laugh", T + "; ideal: estéreo, passando de um lado ao outro"),
 ("goblin_foge", "Cena 6 · Goblin", "passos correndo entre as árvores", "running footsteps forest leaves", ""),
 ("praia", "Cena 7 · Praia", "ondas e gaivotas", "beach waves seagulls", ""),
 ("trovao", "Tempestade (relâmpago)", "um trovão estoura", "thunder crack close", ""),
 ("barco", "Cena 8 · Barco", "madeira raspando na areia; remos rangendo", "boat dragged sand oars creak", ""),
 ("tempestade", "Cena 8 · Barco", "vento forte e ondas batendo no casco", "storm wind waves boat hull", ""),
 ("calmaria", "Cena 8 · Barco", "o vento se acalma", "wind dies down calm sea", ""),
 ("farol", "Cena 9 · Farol", "vento, mar distante e uma engrenagem velha girando", "lighthouse wind sea old gears", ""),
 ("porta_pedra", "Charada da porta (Farol)", "pedra pesada rangendo e se arrastando", "heavy stone door grinding", T),
 ("masmorra", "Cena 10 · Masmorra", "porta pesada rangendo; gotas ecoando", "dungeon door creak water drip echo", T),
 ("corredores", "Cena 10 · Masmorra", "à esquerda, rangido de armadura; à direita, passos de pedra", "armor rattle + heavy stone footsteps", "estéreo: armadura à esquerda, passos à direita"),
 ("armadura", "Cena 11A · Cavaleiro", "o rangido de uma armadura vazia", "armor clank creak", ""),
 ("banquete", "Cena 11A · Cavaleiro", "pratos, talheres e cheiro de comida", "dishes cutlery plates table", ""),
 ("espelho", "Cena 11A · Espelho", "um espelho antigo vibrando", "glass resonance magic hum", ""),
 ("golem", "Cena 11B · Golem", "o chão treme; pedras rangendo", "stone golem rumble footsteps", ""),
 ("golem_poeira", "Cena 11B · Golem", "pedras virando poeira", "rocks crumble to dust", ""),
 ("abismo", "Puzzle das pedras", "vento subindo do abismo", "wind canyon howl", ""),
 ("pedra_firme", "Puzzle das pedras", "pés firmes na pedra", "stone footstep single", "curto"),
 ("pedra_afunda", "Puzzle das pedras", "pedra afundando", "stone sinking gravel", ""),
 ("dragao_respira", "Cena 12 · Dragão", "uma respiração profunda e o chão tremendo", "dragon breath deep growl", T),
 ("fogo", "Cena 12 · Dragão", "um rugido e o estalo de chamas", "dragon roar fire flames", T),
 ("garra_esquerda", "Cena 12 · Dragão", "asas batendo e garras, vindo da esquerda", "wings flapping claw swipe", "estéreo: só no fone esquerdo"),
 ("garra_direita", "Cena 12 · Dragão", "asas batendo e garras, vindo da direita", "wings flapping claw swipe", "estéreo: só no fone direito"),
 ("garra_frente", "Cena 12 · Dragão", "asas batendo e garras, vindo de frente", "wings flapping claw swipe", "mono, no centro"),
 ("queimadura", "Cena 12 · Dragão", "chamas (quando o jogador erra)", "fire burst flame whoosh", ""),
 ("fogo_apaga", "Cena 12 · Dragão", "fogo enfraquecendo, se desfazendo com um chiado", "fire extinguish hiss", ""),
 ("dragao_cai", "Cena 12 · Dragão", "um rugido longo e um corpo enorme caindo", "dragon roar death fall thud", T),
 ("tesouro", "Cena 12 · Dragão", "moedas de ouro tilintando", "coins treasure jingle", ""),
 ("mar_calmo", "Epílogo", "ondas calmas e uma vela batendo no vento", "calm sea sail flapping", ""),
 ("casa_de_cura", "Epílogo", "a porta da casa de cura se abrindo", "door open soft chime", T),
]

if __name__ == "__main__":
    main()
