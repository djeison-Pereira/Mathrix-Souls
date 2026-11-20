# Ferramentas de áudio

Scripts que geram os efeitos de `audios/sons`. Nada daqui vai para o .exe. Rode sempre de dentro da pasta `arquivos`.

| Script | O que gera |
|---|---|
| `../gerar_sons.py` | efeitos sintetizados "clássicos" (seno + ruído), direto em `audios/sons` |
| `gerar_propostas.py` | efeitos sintetizados da revisão de nov/2026 (síntese modal, atrito, grãos, estéreo) e os que misturam gravação real; saem em `ferramentas_audio/revisao/<nome>/proposta.wav` para ouvir antes de levar ao jogo |
| `montar_indice.py` | a página `revisao/index.html` para ouvir velho x proposta lado a lado (depois de rodar `gerar_propostas.py` sem nomes) |
| `gerar_madeira_embarca.py` | `audios/sons/madeira_embarca.wav` (embarque no bote) |
| `gerar_rangido_barco.py` | `audios/sons/rangido_barco.wav` (os remos) |

As gravações reais usadas pelos scripts ficam em `audios_originais` (fora do git; os créditos estão em `audios/CREDITOS.txt`).

## De onde vem cada som do jogo

**gerar_sons.py** (mesmo nome): abismo, cajado, esquiva, fogo, fogo_apaga, garra_esquerda, garra_direita, garra_frente,
goblin_foge, goblin_salta, golem_poeira, mar_calmo, passo, pedra_firme, pedra_afunda, queimadura, tesouro, vento_janela,
vento_seco, vez_do_jogador e o sino da abertura. O `frascos` saiu do efeito "armadura" dele, sem a buzina.

**gerar_sons.py, com outro nome no jogo** (o nome original agora é de outro som):
- função `calmaria` → `calmaria_vento.wav`
- função `desmoronamento` → `desmoronamento_2.wav`
- função `farol` → `farol_porta.wav`

**gerar_propostas.py** (copiar `revisao/<nome>/proposta.wav` para `audios/sons`):
- com o mesmo nome: banquete, bifurcacao, calmaria, dano, desmoronamento, espelho, farol, goblin_risada, golem, grilo, magia, teleporte
- com outro nome: `abismo` → `abismo_forte.wav`; `esquiva` → `esquiva_dragao.wav`; `garra_<lado>` → `garra_dragao_<lado>.wav`;
  `vento_janela` → `vento_muda.wav`

**Scripts próprios:** madeira_embarca e rangido_barco (acima). O `agua_empurra.wav` é o começo (1,6 s, com fade) do antigo
`madeira_cai.wav`, que está no histórico do git.

**Gravações reais, sem script:** abertura, dragao_cai, galo_vento, masmorra, porta, trovao.

## Cuidado

- `python gerar_sons.py --forcar` (sem nomes) **sobrescreve** calmaria, dano, desmoronamento, farol, grilo e teleporte com as
  versões antigas. Sem `--forcar` ele só cria o que falta. Prefira passar os nomes: `python gerar_sons.py --forcar fogo`.
- Os sons sorteiam detalhes (posição de cada estalo, de cada grão): gerar só alguns nomes dá uma variação parecida, não o
  mesmo arquivo. Para mexer num som aprovado, ouça o resultado antes de substituir.
- Narração e sons: o efeito sem arquivo é dito pelo Narrador, a não ser que esteja em `SOM_REDUNDANTE` (notebook, célula 1.1).
