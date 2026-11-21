"""Monta ferramentas_audio/revisao/index.html (ouvir velho x proposta lado a lado) a partir de revisao/indice.json.
Uso (dentro de arquivos): python ferramentas_audio/montar_indice.py   (rodar depois de gerar_propostas.py, todas)"""
import html
import json
import os

AQUI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "revisao")

with open(os.path.join(AQUI, "indice.json"), encoding="utf-8") as f:
    dados = json.load(f)


def cartao(s):
    velho = (f'<audio controls preload="none" src="{s["nome"]}/{s["velho"]}.wav"></audio>' if s["velho"]
             else '<p class="vazio">sem arquivo</p>')
    rotulo_velho = "Velho (no jogo hoje)" if s["no_jogo"] else "Velho (sintetizado que ficou fora do jogo)"
    selo = '<span class="selo jogo">no jogo</span>' if s["no_jogo"] else '<span class="selo falta">sem som no jogo</span>'
    est = '<span class="selo">estéreo: use fone</span>' if s["estereo"] else ""
    return f"""
<article data-nome="{s['nome']}">
  <header><h2>{s['nome']}</h2>{selo}{est}<span class="dur">{s['dur']} s</span></header>
  <p class="nota">{html.escape(s['nota'])}</p>
  <div class="par">
    <div><h3>{rotulo_velho}</h3>{velho}</div>
    <div><h3>Proposta</h3><audio controls preload="none" src="{s['nome']}/proposta.wav"></audio></div>
  </div>
  <div class="escolha" role="radiogroup" aria-label="Escolha para {s['nome']}">
    <label><input type="radio" name="e_{s['nome']}" value="proposta"> Usar a proposta</label>
    <label><input type="radio" name="e_{s['nome']}" value="velho"> Manter o velho</label>
    <label><input type="radio" name="e_{s['nome']}" value="ajustar"> Proposta, com ajuste</label>
    <input type="text" class="obs" placeholder="O que ajustar?" aria-label="Ajuste para {s['nome']}">
  </div>
</article>"""


nao = "".join(f"<li><strong>{html.escape(k)}</strong>: {html.escape(v)}</li>" for k, v in dados["nao_revisados"].items())
pagina = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Revisão dos sons</title>
<style>
:root {{ --fundo:#f6f4ef; --cartao:#fff; --texto:#1d1b18; --suave:#6b665e; --borda:#e2ddd3; --jogo:#2f6b3a; --falta:#9a4b16; }}
@media (prefers-color-scheme: dark) {{ :root {{ --fundo:#16150f; --cartao:#201f19; --texto:#ece8df; --suave:#a39d91; --borda:#36342c; --jogo:#7fc08b; --falta:#e6a06b; }} }}
* {{ box-sizing:border-box }}
body {{ margin:0; background:var(--fundo); color:var(--texto); font:16px/1.5 system-ui, sans-serif; }}
main {{ max-width:980px; margin:0 auto; padding:24px 16px 64px; }}
h1 {{ margin:0 0 4px; font-size:28px }}
.intro {{ color:var(--suave); margin:0 0 20px }}
.barra {{ display:flex; gap:8px; flex-wrap:wrap; margin-bottom:20px; align-items:center }}
button {{ font:inherit; padding:8px 14px; border-radius:8px; border:1px solid var(--borda); background:var(--cartao); color:var(--texto); cursor:pointer }}
article {{ background:var(--cartao); border:1px solid var(--borda); border-radius:12px; padding:16px; margin-bottom:14px }}
article header {{ display:flex; gap:8px; align-items:center; flex-wrap:wrap }}
h2 {{ margin:0; font-size:19px; font-family:ui-monospace, monospace }}
h3 {{ margin:0 0 4px; font-size:13px; color:var(--suave); font-weight:600 }}
.selo {{ font-size:12px; padding:2px 8px; border-radius:99px; border:1px solid var(--borda); color:var(--suave) }}
.selo.jogo {{ color:var(--jogo); border-color:currentColor }} .selo.falta {{ color:var(--falta); border-color:currentColor }}
.dur {{ margin-left:auto; color:var(--suave); font-size:13px }}
.nota {{ margin:8px 0 12px }}
.par {{ display:grid; grid-template-columns:1fr 1fr; gap:12px }}
audio {{ width:100% }}
.vazio {{ color:var(--suave); margin:8px 0 }}
.escolha {{ display:flex; gap:14px; flex-wrap:wrap; margin-top:12px; align-items:center; font-size:14px }}
.obs {{ flex:1; min-width:180px; font:inherit; padding:6px 10px; border-radius:8px; border:1px solid var(--borda); background:transparent; color:var(--texto) }}
textarea {{ width:100%; min-height:140px; font:13px ui-monospace, monospace; background:var(--cartao); color:var(--texto); border:1px solid var(--borda); border-radius:8px; padding:10px }}
@media (max-width:640px) {{ .par {{ grid-template-columns:1fr }} }}
</style></head>
<body><main>
<h1>Revisão dos sons</h1>
<p class="intro">Cada som sintetizado do jogo (e cada um que está sem som) tem o velho e uma proposta nova, no mesmo volume.
Ouça de fone: vários são estéreo e o lado importa. Marque a escolha; ela fica salva neste navegador.
No fim, "Copiar escolhas" gera o resumo para mandar.</p>
<div class="barra"><button id="copiar">Copiar escolhas</button><span id="contagem" class="intro" style="margin:0"></span></div>
{''.join(cartao(s) for s in dados['sons'])}
<article><h2>Não revisados</h2><ul>{nao}</ul></article>
<textarea id="saida" readonly aria-label="Resumo das escolhas"></textarea>
</main>
<script>
const CH = 'revisao_sons_escolhas';
let est = {{}};
try {{ est = JSON.parse(localStorage.getItem(CH) || '{{}}'); }} catch (e) {{}}
function salvar() {{ try {{ localStorage.setItem(CH, JSON.stringify(est)); }} catch (e) {{}} contar(); }}
function contar() {{
  const total = document.querySelectorAll('article[data-nome]').length;
  const feitos = Object.values(est).filter(v => v && v.e).length;
  document.getElementById('contagem').textContent = feitos + ' de ' + total + ' marcados';
}}
document.querySelectorAll('article[data-nome]').forEach(a => {{
  const nome = a.dataset.nome, e = est[nome] || {{}};
  a.querySelectorAll('input[type=radio]').forEach(r => {{
    if (r.value === e.e) r.checked = true;
    r.addEventListener('change', () => {{ est[nome] = Object.assign(est[nome] || {{}}, {{e: r.value}}); salvar(); }});
  }});
  const o = a.querySelector('.obs'); o.value = e.o || '';
  o.addEventListener('input', () => {{ est[nome] = Object.assign(est[nome] || {{}}, {{o: o.value}}); salvar(); }});
}});
// tocar um pausa os outros
document.addEventListener('play', ev => document.querySelectorAll('audio').forEach(x => {{ if (x !== ev.target) x.pause(); }}), true);
document.getElementById('copiar').addEventListener('click', () => {{
  const nomes = {{proposta: 'usar a proposta', velho: 'manter o velho', ajustar: 'proposta com ajuste'}};
  const linhas = Object.entries(est).filter(([k, v]) => v.e || v.o)
    .map(([k, v]) => '- ' + k + ': ' + (nomes[v.e] || 'sem escolha') + (v.o ? ' (' + v.o + ')' : ''));
  const t = document.getElementById('saida'); t.value = linhas.join('\\n');
  t.select(); try {{ navigator.clipboard.writeText(t.value); }} catch (e) {{}}
}});
contar();
</script>
</body></html>"""

with open(os.path.join(AQUI, "index.html"), "w", encoding="utf-8") as f:
    f.write(pagina)
print("ok:", os.path.join(AQUI, "index.html"))
