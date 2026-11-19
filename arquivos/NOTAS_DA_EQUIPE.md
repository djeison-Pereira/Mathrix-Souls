# Notas da equipe: Mathrix Souls

Documento interno: o que foi construído, o que mudou em relação ao roteiro, como gravar as vozes e como o código funciona.

---

## ⭐ Meta da versão final: um executável (.exe)

**A versão final do jogo tem que ser um executável Windows (`.exe`).** O notebook é onde o jogo é desenvolvido.

**Por quê:** a pessoa cega precisa conseguir abrir e jogar **sozinha**, sem depender de alguém para instalar Python ou Jupyter, rodar células ou configurar qualquer coisa. Com o `.exe`, basta dar dois cliques no arquivo pela acessibilidade do próprio Windows (leitor de tela, Explorador de Arquivos), e o jogo já começa falando.

O que a versão final precisa garantir:
- **Nada para instalar:** Python, bibliotecas e todas as gravações vão dentro do pacote. Por exemplo, com PyInstaller, gerando um `.exe` ou uma pasta com o `.exe` e os áudios.
- **O jogo começa falando** assim que abre, sem nenhuma tela ou clique antes do menu narrado.
- **Teclas sem Enter**, som estéreo e tempo de esquiva (ver seção 6).
- **Funciona sem internet** e sem permissões de administrador.
- **Testado num computador "limpo"**, sem Python instalado, e de olhos fechados, do duplo clique até o fim do jogo.

### Situação atual: dois `.exe`
Os dois rodam o jogo (DEMO e completo) **sem instalar nada**: Python, NumPy, a voz e o pygame (que toca `.wav`, `.mp3` e `.ogg`) vão dentro deles. Cada um tem cerca de 28 MB; o de entrega cresce conforme as gravações entram. Ainda **faltam** o som estéreo, o tempo de esquiva, os efeitos sonoros e o teste num computador sem Python.
⚠️ O `.exe` de **entrega** está **desatualizado**: ele só vai ser gerado de novo na entrega final, para não gastar tempo gerando a cada mudança. O de desenvolvimento lê o notebook a cada abertura e já tem tudo.

| | Onde fica | Para quê | Como funciona |
|---|---|---|---|
| **Desenvolvimento** | `MathrixSouls.exe` (pasta principal) | A equipe testar enquanto mexe no jogo | Toda vez que abre, **lê o notebook e os áudios da pasta `arquivos`**. Mudou uma fala ou o código no notebook? Salve (Ctrl+S) e abra o `.exe` de novo. **Não precisa gerar outro.** Sem a pasta `arquivos` ao lado, ele avisa que não achou o notebook. |
| **Entrega** | `entrega/MathrixSouls.exe` | Mandar para quem vai jogar | Leva o notebook e **todas as gravações dentro dele**. Funciona sozinho, sem nenhuma outra pasta. É uma "foto" do jogo no momento em que foi gerado: mudou algo, gere de novo. |

```
Mathrix-Souls/
├── MathrixSouls.exe        ← .exe de desenvolvimento: dois cliques e ele começa a falar
├── README.md               ← página do projeto no GitHub (precisa ficar na raiz)
├── entrega/
│   └── MathrixSouls.exe    ← .exe de entrega: funciona sozinho
└── arquivos/
    ├── mathrix_souls.ipynb   ← o jogo inteiro (falas, cenas, motor)
    ├── iniciar_jogo.py            ← código dos .exe: lê o notebook e roda as células
    ├── gerar_exe.py               ← gera os .exe
    ├── NOTAS_DA_EQUIPE.md         ← este documento
    ├── audios/                    ← gravações (audios/<CÓDIGO>.wav)
    │   └── sons/                  ← efeitos sonoros
    └── Material/                  ← roteiro e documento do projeto
```

**Como gerar os `.exe`** (antes, `pip install pyinstaller numpy comtypes pygame-ce`):

> Use o **`pygame-ce`**, não o `pygame`: o `pygame` original ainda não instala no Python 3.14. O `pygame-ce` é a versão mantida pela comunidade, e o código não muda nada (continua `import pygame`).
- **Entrega:** no fim do notebook, no bloco **"Apêndice 2: Gerar o .exe de entrega"**, troque `GERAR_EXE_DE_ENTREGA` para `True` e rode só aquela célula. Pelo terminal, o comando é `python gerar_exe.py --entrega`, dentro de `arquivos`.
- **Desenvolvimento:** `python gerar_exe.py`, dentro de `arquivos`. Só é preciso se o `iniciar_jogo.py` mudar ou se o notebook passar a usar uma biblioteca nova.
- Para rodar sem `.exe` (útil para testar), use `python iniciar_jogo.py` dentro de `arquivos`.

**Teste feito:** editei uma fala e a configuração de voz numa cópia do notebook **sem** gerar o `.exe` de novo, e o `.exe` de desenvolvimento já abriu com as duas mudanças. O de entrega rodou sozinho, copiado para uma pasta vazia.

### Vozes do computador: Maria e Daniel
Enquanto não houver gravações, o jogo fala tudo com as vozes do Windows em português do Brasil: a **Maria** (feminina) e o **Daniel** (masculino). Assim ele já é jogável sem nenhuma gravação. A voz, a velocidade e a voz masculina ficam na célula 1.1 (`VOZ_PREFERIDA`, `VOZ_VELOCIDADE`, `VOZ_MASCULINA`).

**Versão 1: só vozes do computador.** Não há gravações, e o menu não tem mais a tecla G (escolher entre vozes gravadas e do computador). O código ainda toca `audios/<CÓDIGO>.wav` se um dia o arquivo existir, e os efeitos sonoros de `audios/sons` também.

**Ajudas para quem joga só ouvindo:**
- **Uma voz para cada personagem.** O Daniel não aparece na lista comum de vozes do Windows: ele é uma das vozes do Narrador do Windows ("OneCore"), e o jogo o encontra por lá. Cada personagem usa a Maria ou o Daniel, com **tom e ritmo próprios** (tabela `VOZES_PERSONAGENS`, célula 1.3). Tom medido gravando em `.wav`:

  Regra usada no ajuste: **personagens da mesma cena precisam soar bem diferentes**, no tom, no ritmo ou na voz. Medido em nov/2026, com a mesma frase gravada em `.wav` (a duração mostra o ritmo):

  | Personagem | Voz | Tom medido | Duração da frase | Aparece com |
  |---|---|---|---|---|
  | Narrador | Maria | 184 Hz | 7,1 s | todos |
  | Sistema | Maria | 200 Hz | 6,4 s | todos |
  | Grilo Falante | Maria | 240 Hz (bem agudo) | 5,7 s | quase todos |
  | Ecos (a voz misteriosa) | Maria | 136 Hz (sussurro grave) | 11,1 s | Grilo |
  | Mãe (o bilhete da cena 1) | Maria | 162 Hz (mais grave que o Narrador) | 11,1 s (bem devagar) | Narrador |
  | Goblin | Daniel | 165 Hz (o mais agudo) | 4,8 s (o mais rápido) | Grilo; no epílogo, Marinheiro e Taverneiro |
  | Taverneiro | Daniel | 150 Hz (animado) | 6,0 s | Alquimista e Max |
  | Alquimista | Daniel | 126 Hz | 7,5 s | Taverneiro, Max, Marinheiro, Dragão |
  | Max | Daniel | 118 Hz | 11,7 s (o mais arrastado) | Taverneiro e Alquimista |
  | Marinheiro | Daniel | 103 Hz (velho e grave) | 9,4 s | Alquimista e Grilo |
  | Cavaleiro Fantasma | Daniel | 102 Hz | 8,3 s | Grilo |
  | Dragão | Daniel | 98 Hz | 7,5 s | Alquimista e Grilo |
  | Golem | Daniel | 97 Hz | 10,4 s (bem lento) | Grilo |

  **Se o computador não tiver o Daniel**, os personagens dele usam a Maria com um tom de reserva (de 140 a 224 Hz), como era antes. A reserva pelo PowerShell só tem a Maria.

- **Nome do personagem antes da fala, na voz do Narrador.** Quando o personagem muda, o Narrador diz o nome antes ("Alquimista." na voz do Narrador, e depois "Ah, é você..." na voz do Alquimista). Ficou porque, mesmo com duas vozes, vários personagens dividem a mesma voz, e quem joga ouvindo pode confundir. Medido em `.wav`: "Dragão." saiu a 184 Hz (Maria, o Narrador) e a fala dele a 109 Hz (Daniel).
- **Tecla O (opções de agora):** fala só as teclas que valem naquele momento, com o que cada uma faz. O **H** lista todos os comandos, e o **R** continua repetindo a fala da história. Como a lista é montada na hora, ela sai sempre na voz do computador. Se o mesmo personagem fala várias vezes seguidas, o nome não é repetido. O **R** sempre repete com o nome. Isso pode ser desligado em `DIZER_NOME_DO_PERSONAGEM`. Com as falas gravadas, o nome não é dito, porque a própria voz de cada um já identifica o personagem.
- **Sinal sonoro de "sua vez".** Quando a fala termina e o jogo passa a esperar uma tecla, toca um bipe curto. Para trocar, grave `audios/sons/vez_do_jogador.wav`; para desligar, use `SINAL_DE_ESPERA`.
- **A fala diz qual tecla usar?** Quase sempre: o menu, as escolhas de caminho, as perguntas ("Opção A..., Opção W..., Opção D...") e o "Aperte W para continuar" (falado nas 3 primeiras vezes; depois fica só o bipe). Há duas exceções de propósito:
  - Na **esquiva**, a fala diz só de onde vem o golpe, porque o desafio é o jogador saber para onde pular. O Grilo explica as teclas antes do combate.
  - Em qualquer momento, **H** lista os comandos e **R** repete a última fala.
- **Responder sem esperar a fala acabar** (no `.exe` e no terminal; no Jupyter, não):
  - A tecla funciona **na hora, sem Enter**, e as **setas** valem como W, A, S, D.
  - Uma tecla apertada **durante a fala** cala a voz na hora, tanto a da Maria quanto as gravações.
  - Numa **pergunta** (menu, escolhas, opções de matriz), a tecla **já vale como resposta**, e o jogo não lê o resto das opções. Numa fala da história, a tecla **pula aquela fala**, exceto os comandos: **R** recomeça a fala; **P** pausa e, ao voltar, repete a fala; **V** e **H** dizem as vidas e os comandos e repetem a fala; **Q** sai do jogo. (Corrigido: antes, o R no meio da fala pulava para a próxima em vez de repetir.)
  - Para desligar, use `PODE_INTERROMPER`.
  - Testado com tecla simulada:
    - **Menu:** com a tecla em 1,5 s, a fala de 7 s parou e a resposta valeu.
    - **Pergunta de matriz:** respondeu em 2,5 s, quando ler as opções levaria uns 15 s.
    - **Gravação `.ogg`:** a fala de 4,1 s parou em 1,0 s.
- **Velocidade da fala:** 0,75x, 1x, 1,25x, 1,5x, 2x, 2,5x e 3x. Dá para mudar de dois jeitos:
  - **No menu (W):** **D** aumenta, **A** diminui e **W** volta. Cada mudança é anunciada já na velocidade nova.
  - **Durante o jogo:** **+** (ou **=**) acelera e **−** desacelera, **sem anunciar nada**, para não atrapalhar a história. No meio de uma fala, a voz **acelera ou desacelera na hora, sem parar nem recomeçar**. Esperando uma resposta, toca só um bipe curto (agudo = acelerou, grave = desacelerou), que pode ser desligado em `BIPE_DE_VELOCIDADE`. No limite, nada acontece.
  - **Como funciona:** o tom e o ritmo de cada personagem vão marcados no texto, e a velocidade escolhida pelo jogador vai na propriedade `Rate` da voz do Windows, que muda ao vivo.
  - **Testado com tecla simulada e a voz real:**
    - **Narrador:** uma fala de 12,2 s, com +++ aos 2 s (2x), terminou em 7,7 s; com − aos 2 s (0,75x), em 15,9 s.
    - **Alquimista:** uma fala de 26,1 s caiu para 15,0 s, mantendo o tom dele.
  - **Limites:** só na voz SAPI. Na reserva pelo PowerShell, a velocidade nova vale a partir da próxima fala. Nas gravações, + e − não mudam nada, porque elas tocam em 1x.
  - Ela acelera a voz da Maria **sem mudar o tom** e encurta as pausas entre as falas. Medido em `.wav` (relativo ao 1x): 1,25x, 1,55x, 1,92x, 2,42x e, no máximo, **2,7x**, que é o teto da voz do Windows.
  - **Por que não passa de 3x:** a voz SAPI do Windows aceita no máximo +10 de velocidade. Testamos forçar mais (somando a velocidade do texto), e a fala chegou a "5,8x", mas **engolia palavras**: os trechos de fala medidos caíram de 28 para 10. Para quem joga só ouvindo, isso é pior que lento. (Leitores de tela como o Narrador e o NVDA usam outras vozes e escalas próprias; o "50" do Windows é uma posição no controle de velocidade, não 50 vezes.)
  - **Trava por personagem:** a velocidade escolhida mais o ritmo do personagem nunca passam de +10. Por isso, nas velocidades mais altas, o Goblin e o Grilo deixam de ser mais rápidos que os outros: todos chegam ao mesmo teto, sem embolar.
  - **As gravações continuam em 1x.** Acelerar um áudio gravado sem a voz ficar fina pede *time-stretch*, que ainda não está no jogo. Uma saída futura é gerar, ao montar o `.exe` de entrega, cópias aceleradas de cada gravação com uma ferramenta própria para isso (ex.: ffmpeg com o filtro `atempo`).

---

## Música, ambiente e efeitos reais

- **Música por cena** (`audios/musica/`) e **ambiente em loop** (`audios/ambiente/`), definidos no dicionário `CENA_SOM` (célula Parte 4). Para trocar a trilha de uma cena, é só mudar o nome ali. Volumes em `VOLUME_MUSICA`, `VOLUME_AMBIENTE`, `VOLUME_EFEITOS` e `GANHO_MUSICA` (célula 1.1 e 1.2); `MUSICA_ATIVA = False` desliga a música.
- **Efeitos junto com a narração:** `som("descrição", "nome", fundo=True)` toca sem esperar. Se existir `audios/ambiente/<nome>`, ele vira loop até a cena acabar (ex.: taverna, tempestade). Sem arquivo, o jogo continua descrevendo o efeito em voz alta.
- **Efeitos que ainda não existem de verdade:** só os sons reais (e o vento da janela) ficam em `audios/sons`; os outros foram sintetizados e estão em `sons_sinteticos/`, **fora do jogo**. Sem o arquivo, o Narrador diz a descrição (sem o "Som:"), a não ser que o efeito esteja em `SOM_REDUNDANTE` (célula 1.1): aí ele não diz nada, porque a narração da cena já conta o que acontece. Para testar um sintético, copie o `.wav` para `audios/sons`; para trocar por um real, coloque o arquivo com o mesmo nome. O PDF do roteiro de gravação marca cada um como OK ou FALTA.
- Na cena do Goblin não há música, para o jogador ouvir de onde vem o golpe.
- **Créditos:** `audios/CREDITOS.txt` (as licenças precisam ser conferidas e citadas no relatório). Os arquivos originais ficam em `audios_originais/`, fora da pasta `audios`, para não inflar o .exe.
- **Masterização:** `python masterizar_audios.py` nivela, comprime e limita todos os áudios (música em -24 dB no arquivo e salva em .mp3 pelo codificador do Windows, `wav_para_mp3.ps1`; ambientes e efeitos em volumes-alvo; ver o topo do script). O volume final de cada música fica em `GANHO_MUSICA`. O `abertura` (trovão + sino) é montado à mão e o script não mexe nele. Para deixar uma música mais alta ou mais baixa, mude o `GANHO_MUSICA`, não o arquivo.
- `gerar_sons.py` não sobrescreve mais um efeito que já existe (use `--forcar`).

## 1. Resumo do que existe hoje

- **Arquivo do jogo:** [`mathrix_souls.ipynb`](mathrix_souls.ipynb), um notebook Python com **o jogo completo**. Antes ele se chamava `mathrix_souls_demo.ipynb`.
- **No menu:** **E** = continuar de onde parou (se houver salvo, é a primeira coisa que o menu diz) · **A** = DEMO (cenas 1 a 9, termina no Farol) · **D** = jogo completo (cenas 1 a 12 + epílogo) · **C** = seleção de cenas · **S** = como jogar · **Q** = sair.
- **Seleção de cenas (C):** **S** = próxima, **W** = anterior, **D** = jogar a partir dela, **A** = voltar ao menu.
  - A cena escolhida segue até o fim do jogo completo, e a cena 11 aparece como 11A (Cavaleiro) e 11B (Golem).
  - Se o jogador perder todas as vidas antes de passar por um checkpoint, volta para a cena escolhida.
  - Serve para testar uma cena sem jogar tudo de novo, e para quem quer rejogar uma parte.
  - Testado: começar no Golem, morrer no Dragão e voltar ao Dragão, morrer na tempestade e voltar com "De novo.", e passar do começo e do fim da lista.
- **DEMO:** Casa, Taverna, Lição da soma, Grilo, Bifurcação, Goblin, Praia (checkpoint), Barco na tempestade e Farol.
- **Jogo completo:** continua do Farol, que vira checkpoint, para a Masmorra, um dos dois guardiões (Cavaleiro Fantasma **ou** Golem), o Dragão e o epílogo na taverna.
- **Matemática usada**, sempre com justificativa falada:

  | Onde | Conteúdo | O que o jogador faz |
  |---|---|---|
  | Onde | Conteúdo | O que o jogador faz |
  |---|---|---|
  | Lição + Goblin | Matriz quadrada e **soma** | Escolhe A + B entre 3 respostas |
  | Praia + Barco | **Triangular superior** | Identifica a triangular entre 3 matrizes sorteadas |
  | Farol (só no completo) | **Diagonal**, **identidade** e a regra do **tipo mais específico** | Lição com exemplos; dá para ouvir de novo |
  | Cavaleiro Fantasma | **Nula** como elemento neutro da soma; **transposta** e **simétrica** (o espelho) | A + 0 = A; escolhe a transposta; escolhe a simétrica |
  | Golem | **Nula** como matriz menos ela mesma | A − A = 0 |
  | Puzzle das pedras | **Nula**, **identidade** e **diagonal** | Pisa na pedra do tipo que o Golem pede |
  | Farol (os dois modos) | **Charada da porta**: triangular superior | Escolhe entre 2x3, triangular superior e "zero em cima da diagonal" |
  | Dragão | **Classificação** (o combate do MVP) e o golpe final do **determinante** | Diz o tipo mais específico de 2 fogos (a nula pode aparecer); no último, calcula o determinante 2x2 |

  São **7 tipos** (quadrada, triangular superior, diagonal, identidade, nula, transposta e simétrica), **2 operações** (soma e subtração) e o **determinante**. Pelo caminho do Golem, o jogador não vê transposta nem simétrica; o Dragão só cobra os tipos que ele aprendeu.
- **Tudo em 2x2:** quatro números por opção, para a pergunta ser curta de ouvir e a resposta, simples.
- **Toda magia nova vem com um diálogo que ensina a resolver:**
  - **Alquimista no farol:** diagonal, identidade e a regra do mais específico.
  - **Cavaleiro:** "a diagonal fica parada e os dois números de fora trocam de lugar" (transposta); "os dois números de fora iguais = simétrica".
  - **Grilo, antes de cada salto:** uma dica do tipo pedido.
  - **Alquimista, antes do Dragão:** a **receita** para classificar, que dá para ouvir de novo. Num 2x2, basta escutar os dois números de fora da diagonal (o de cima à direita e o de baixo à esquerda):
    - **Os dois zero:** diagonal. Se a diagonal for 1 e 1, identidade; se tudo for zero, nula.
    - **Só o de baixo zero:** triangular superior.
    - **Os dois iguais:** simétrica.
  - **Alquimista, antes do Dragão, também:** o **determinante**, "o coração da matriz". Multiplique a diagonal principal, multiplique a outra diagonal e tire o segundo do primeiro. Exemplo: três e um em cima, dois e quatro embaixo: 12 − 2 = 10.
- **Tamanho:** 403 falas (com os pedaços para montar frases) e 49 efeitos sonoros.
- **Base da história:** o `roteirorascunho.pdf` (Alquimista, dragão, Max), com a **mãe doente** do `Jogo Inclusivo.md` como motivação do herói. A mãe está na casa de cura (o hospital de Trim), e o tesouro do dragão paga as ervas.

### Revisão matemática
Todas as contas da DEMO foram conferidas: a soma da lição, a soma do goblin com as duas respostas erradas, e a geração e justificativa da triangular superior, que tem sempre exatamente uma resposta certa por relâmpago.

**Jogo completo (conferido na saída do jogo):**
- **Cavaleiro:** [3 1; 2 4] + nula = [3 1; 2 4]. As erradas são a nula ("tudo vira zero") e [4 2; 3 5] ("somar zero aumenta"). A explicação é que a nula é o elemento neutro da soma.
- **Golem:** [4 7; 2 9] − [4 7; 2 9] = nula. As erradas são a própria matriz e o dobro, [8 14; 4 18], que é somar em vez de subtrair.
- **Espelho:** transposta de uma matriz sorteada. As erradas são a própria matriz e a matriz "de cabeça para baixo". A matriz sorteada nunca é simétrica e tem a diagonal com números diferentes, senão duas opções ficariam iguais.
- **Pedras:** em cada salto, exatamente uma pedra é do tipo pedido. As outras são de tipos parecidos que não servem: no salto da identidade, por exemplo, uma diagonal qualquer e a nula.
- **Dragão:** as 2 primeiras rodadas pedem o **tipo mais específico** do fogo, sempre com uma única opção certa. Se o jogador escolhe um tipo em que a matriz "até se encaixa" (diagonal para a identidade), a explicação diz que existe um tipo mais específico. A última rodada é o **determinante** de uma matriz 2x2 com números de 1 a 5, sem as duas diagonais com o mesmo produto. As opções são a certa (`ad − bc`), a soma das diagonais (`ad + bc`) e a conta ao contrário (`bc − ad`), sempre três números diferentes.
- **Números lidos:** de menos cinquenta a cinquenta. Até vinte, um pedaço só (`NUM_0` a `NUM_20`); acima, dezena + "e" + unidade (`NUM_30` + `MAT_E` + `NUM_2` = "trinta e dois"). O determinante vai de −24 a 24, e a soma das diagonais chega a 50.

**Verificação automática (milhares de sorteios cada):**
- **Geradores:** 18 mil matrizes 2x2 dos seis tipos. Em todas, o tipo calculado e a **receita falada pelo Alquimista** dão a mesma resposta.
- **Perguntas:** pedras, espelho e Dragão (pelos dois caminhos) sempre têm exatamente uma resposta certa.
- **Golpe final:** 5 mil sorteios do fogo final. A opção certa é sempre igual ao determinante do NumPy, e as três opções são sempre diferentes e ficam entre −50 e 50.

**Pontos de atenção:**
- **"Multiplicação posição a posição"** (resposta errada do goblin) **não** é a multiplicação de matrizes da disciplina. O produto A·B daria [7 10; 15 6]. No relatório, não chamar de "multiplicação de matrizes".
- **Tipos que se sobrepõem:** a identidade também é diagonal, triangular superior e simétrica; toda diagonal é triangular e simétrica; a nula é tudo isso. O jogo resolve isso com a regra do **tipo mais específico**, na ordem nula → identidade → diagonal → triangular superior → simétrica. O Alquimista ensina a regra no farol.
- No roteiro, golem e dragão usam A − A = matriz nula, o que está correto.

> ✅ **MVP e roteiro juntos:** o `Jogo Inclusivo.md` (MVP) previa classificar identidade, diagonal, triangular, simétrica e nula. Isso agora está no jogo, como o combate de classificação do Dragão e o puzzle das pedras, com a regra do mais específico e respondendo com A/W/D em vez das teclas 1 a 5. A história continua a do roteiro.

---

## 2. Estrutura do notebook

| Parte | O que tem |
|---|---|
| **Introdução** (markdown) | Recorte da DEMO, como rodar, tabela de comandos, regras de gravação |
| **Parte 1: Motor** | 1.1 Configuração · 1.2 Voz e áudio · 1.3 Falas e efeitos · 1.4 Comandos ASDW · 1.5 Vidas/checkpoint · 1.6 Matemática |
| **Parte 2: Narrador e sistema** | Nome do jogo, menu DEMO/completo, instruções, vidas, pausa, acerto, e os **pedaços** para montar a leitura das matrizes |
| **Parte 3: Cenas 1 a 9** | Cada cena tem um bloco de **falas** e um bloco de **lógica** |
| **Parte 3B: Jogo completo** | Cenas 10 (Masmorra), 11A (Cavaleiro), 11B (Golem), 12 (Dragão) e Epílogo, no mesmo formato |
| **Parte 4: Menu e início** | `ROTEIRO_DEMO` e `ROTEIRO_COMPLETO` (a ordem das cenas), o checkpoint e a célula **▶ Jogar** |
| **Apêndice** | Roteiro de gravação: todas as falas e sons, marcados como OK ou FALTA |

### Como as peças se conversam
- `FALAS` é um dicionário `código -> (personagem, texto)`. Cada cena adiciona as suas falas com `FALAS.update({...})`.
- `dizer("A02")` imprime o texto e toca `audios/A02.wav`. Se o arquivo não existir, fala com a voz da Maria.
- A voz sintetizada liga na primeira forma que funcionar: **SAPI direto** (pacote `comtypes`, a mais rápida), **PowerShell** (vem em todo Windows, não precisa instalar nada), **pyttsx3** (fora do Windows) e, por último, só texto.
  - ⚠️ O `pyttsx3` no Windows só fala a **primeira** frase se reaproveitar o motor de voz. Por isso ele cria um motor novo a cada fala e fica como última opção.
- `som("descrição", "nome")` toca `audios/sons/nome.wav`. Sem o arquivo, a descrição é falada em voz alta (o jogador cego precisa dessa pista).
- `escolher({...})` é o **único** lugar que lê o teclado. Ele já trata R, P, V, H, Q e teclas inválidas (avisa e repete as opções).
- `perder_vida()` tira 1 vida. Na terceira, levanta `Derrota`, e o laço de `jogar_demo()` volta para `estado.checkpoint`.
- `Frase` monta uma fala a partir de pedaços gravados (`NUM_3`, `MAT_EM_CIMA`...). É ela que lê as matrizes sorteadas e as justificativas.

### Configuração (célula 1.1)
| Variável | Para que serve |
|---|---|
| `VELOCIDADE` | Pausa entre falas (`0` = sem pausa, bom para testar rápido) |
| `VOZ_ATIVA` | Liga/desliga a voz sintetizada (para as falas sem gravação) |
| `VOZ_PREFERIDA` | Nome da voz do Windows (padrão: `"Maria"`). Se não achar, usa qualquer voz em português |
| `VOZ_VELOCIDADE` | Velocidade da voz, de −10 (lenta) a 10 (rápida). Padrão: `1` |
| `PASTA_AUDIOS` | Pasta das gravações (padrão: `audios`) |
| `SEMENTE` | Número fixo = as matrizes sorteadas são sempre as mesmas |
| `MODO_TESTE` / `ENTRADAS_TESTE` | Joga sozinho com uma lista de teclas, sem digitar |

---

## 3. Guia de gravação

1. Rode o **Apêndice** (última célula) para ver a lista de falas por personagem, com o nome de cada arquivo.
2. Grave **uma fala por arquivo**, com o nome **exato** do código: `GB03.wav`, `S02_1.wav`, `N61_esquerda.wav`.
3. Salve em `audios/` (na mesma pasta do notebook). Efeitos sonoros vão em `audios/sons/`.
4. **Formato: prefira `.ogg` ou `.mp3`, em mono.** Os três formatos (`.wav`, `.mp3`, `.ogg`) funcionam nos `.exe`. No teste, a mesma fala de 4 segundos ficou com 182 KB em `.wav`, 22 KB em `.ogg` e 25 KB em `.mp3`. Com as cerca de 200 falas do jogo completo, é a diferença entre um `.exe` de entrega de uns 65 MB (`.wav`) e um de uns 34 MB (`.ogg`). No Audacity: *Arquivo → Exportar → Exportar como OGG* (ou MP3), com o canal em mono.
   - Não deixe dois arquivos da mesma fala com formatos diferentes (ex.: `A02.wav` e `A02.mp3`); o jogo usa o primeiro que achar, na ordem `.wav`, `.mp3`, `.ogg`.
   - Para rodar o notebook no Jupyter com `.mp3`/`.ogg`, instale o `pygame-ce`. Os `.exe` já o incluem.
5. **Pedaços** (`NUM_0` a `NUM_9`, `MENOS`, `MAT_E`, `MAT_EM_CIMA`, `MAT_EMBAIXO`, `MAT_LINHA_1..3`, `OPCAO_A/W/D`, `J02` a `J05`): grave curto, em tom neutro e **sem silêncio no começo nem no fim**. Eles são tocados em sequência para formar frases como *"Opção A: em cima, dois e um; embaixo, zero e três."*
6. Rode o Apêndice de novo para conferir o que já está OK.

Hoje são **403 falas** (incluindo os pedaços curtos, como os números) e **49 efeitos sonoros**. Na versão 1 nada disso é gravado: tudo sai na voz do computador.

Os códigos da história seguem `PREFIXO` + `número da cena` + `_` + `ordem` (ex.: `T02_03` = Taverneiro, cena 2, 3ª fala).

| Personagem | Dublador previsto | Prefixo dos códigos |
|---|---|---|
| Narrador | Felipe | `N..`, `NUM_..`, `MAT_..`, `OPCAO_..`, `TIPO_..`, `J..`, `MENOS` |
| Grilo Falante | Felipe | `G..` |
| Goblin | Vinícius | `GB..` |
| Max | Vinícius | `MX..` |
| Ecos | Vinícius | `V..` |
| Mãe | a definir | `ME..` |
| Taverneiro | Matheus | `T..` |
| Cavaleiro Fantasma | Matheus | `CF..` |
| Marinheiro | João | `MR..` |
| Dragão | João | `DR..` |
| Alquimista | Daniel | `A..` |
| Golem | Daniel | `GO..` |
| Sistema | voz do computador | `S..`, `SV..`, `SC_..` |

---

## Salvamento

- **Tecla M (voltar ao menu):** vale a qualquer momento da partida, até no meio de uma fala. Salva o jogo sozinho (SV06) e volta ao menu principal. No fim da DEMO e no epílogo não há o que salvar.
- **Menu principal:** quando existe jogo salvo, o menu fala o SV01 **antes** do N03 e aceita a tecla **E** para continuar de onde parou. O **R** repete os dois. Sem salvo, a tecla E não existe.
- **Jogo novo apaga o salvo:** escolher a DEMO (A), o jogo completo (D) ou jogar uma cena pela seleção (C → D) descarta o salvamento anterior.
- **Tecla Q no meio do jogo:** pergunta (SV03) se quer salvar: **W** salva e sai, **S** (ou **Q** de novo) sai sem salvar, **A** volta ao jogo (SV07; a cena atual recomeça do início). No menu, o Q sai direto.
- **O que é guardado:** modo, cena atual, caminho da masmorra, magias, vidas, checkpoint e velocidade da fala. A cena atual **recomeça do início** (não dá para retomar no meio de um diálogo).
- **Onde fica:** `%APPDATA%\MathrixSouls\salvamento.json`, fora da pasta do jogo, para valer também no `.exe` de entrega. Para apagar o progresso, é só deletar esse arquivo.
- **Fim da história:** terminar o jogo completo apaga o salvamento.
- **Testes automáticos:** não salvam nada, a menos que `ARQUIVO_DE_SAVE` aponte para um arquivo.
- **Falas novas:** SV01 a SV07 (voz do Sistema). O S12 cita a tecla M.
- **Velocidade da fala:** o submenu do **W** no menu foi removido. A velocidade muda com **+** e **−** (no menu e no jogo), e o S12 (tecla H) explica isso. O N03 agora cita a tecla H. As falas N08_* e N09 (anúncios do submenu) não são mais usadas e não precisam ser gravadas.

## 4. O que mudou nas falas em relação ao roteiro

> **Roteiro expandido (nov/2026):** a história ganhou o Taverneiro (Bartolo), o Marinheiro (Bento), os Ecos dos magos que não voltaram, a charada da porta do farol e o determinante como golpe final. Todos os códigos foram renumerados. A tabela de/para (código novo e código antigo) e o texto de cada fala estão em [`Material/ROTEIRO_EXPANDIDO.md`](Material/ROTEIRO_EXPANDIDO.md). As seções abaixo usam os **códigos antigos** e contam o histórico de cada mudança.

Legenda: **Nova** = não existia no roteiro · **Adaptada** = texto do roteiro com ajuste · **Igual** = texto do roteiro.
O motivo mais comum das mudanças: o jogador **não vê a tela**, então cada momento de decisão precisa dizer **quais teclas apertar**.

### Narrador e sistema (tudo novo)
- **N01 a N07:** nome do jogo, frase de apresentação, menu (A = DEMO, D = jogo completo, S = como jogar, Q = sair), início do jogo completo, instruções, início da DEMO e despedida.
- **S01 a S12:** tecla inválida, perda de vida, pausa, vidas restantes, acerto, "Esquivou!", magia aprendida e lista de comandos.
- **Variações fixas no lugar de texto variável**, para que tudo possa ser gravado: `S02_2`/`S02_1` (vidas restantes), `S06_3/2/1` (consultar vidas), `S11_soma`/`S11_triangular` (magia aprendida).

### Cena 1: A Casa
- N10, N11: **igual**.
- N14: **nova**. É a motivação do herói: a mãe está doente na casa de cura de Trim, aos cuidados do Druida, e as ervas que podem curá-la custam muito ouro. Vem do `Jogo Inclusivo.md` (a mãe no hospital).
- N12: **nova** ("Aperte W para pegar o cajado e sair de casa").
- N13: **adaptada**. "Entre a decepção e a preocupação... atrás de um café da manhã e, quem sabe, de algum trabalho que pague bem."

### Cena 2: A Taverna
- N20, N22, N23, A01 a A07, N24, N26 a N28: **igual** (A04 a A06 dividem em três a fala longa do Alquimista).
- N21 + **M01**: **novas**. O jogador escolhe falar com o Max, que só resmunga ("matriz... dragão... mais uma caneca").
- N25: **nova**. O jogo pergunta "aceitar ou recusar?" e o Alquimista interrompe de qualquer jeito. A piada do roteiro virou interação.
- A08: **nova**. O Alquimista sabe da mãe e oferece o **tesouro do Dragão** para pagar as ervas. É o motivo para o herói aceitar.

### Cena 3: A Lição da Matriz Quadrada
- A10, A12: **igual** (a lição foi dividida em três falas).
- A11: **adaptada**. Ganhou a regra de que só dá para somar matrizes do mesmo tamanho (mesmo número de linhas e de colunas).
- N30: **nova** (W = entendi, S = ouvir a explicação de novo).
- N31: **igual**.

### Cena 4: O Grilo Falante
- A13, N40, G01, N41: **igual**.
- G02 a G05: **novas**. O Grilo explica os comandos e treina A, D, S e W com o jogador.
- G06: **adaptada** (junta o "você aprende rápido" com o "Dois caminhos... eu escolheria os pássaros").

### Cena 5: A Bifurcação
- N50: **igual**. N51 e N52: **adaptadas** (ganharam "À esquerda" e "À direita" para o jogador saber qual tecla é qual caminho).
- N53, N54: **novas** (instruções de tecla). V01 ("Volte..."): **igual**. N55: **igual**.
- G07 ("Eu avisei! Pássaros."), N56, N57: **novas**.

### Cena 6: O Goblin
- N60: **igual**. GB03 (o pedágio) e GB04 ("Três, cinco, cinco, cinco!"), N62: **igual**.
- GB01: **adaptada** (antes do pedágio, ele testa a sua rapidez).
- **Novas:** G08 (tutorial de esquiva), N61_esquerda/direita/frente (de onde vem o golpe), GB02, G09, GB05 (você errou), GB06 (a pergunta), G10_subtracao / G10_multiplicacao (o Grilo explica o erro), N63 + G11 (voltou depois de perder).
- **Morrer não tem explicação mágica**, por decisão da equipe: é só a mecânica do jogo ("Tudo escurece... Você respira fundo e tenta de novo."). Chegamos a testar a pedra do Alquimista como o que "puxa de volta", mas ela criava outro furo: por que ele não deu a pedra aos magos que mandou antes?

### Cena 7: A Praia
- N70, N72, A22: **igual**.
- A20: **adaptada**. "Matriz Triangular" virou "Matriz Triangular **superior**", porque a inferior tem zeros acima da diagonal, e "diagonal" virou "diagonal principal".
- A21: **adaptada** (ganhou a explicação de onde fica a diagonal principal).
- N71: **nova** (ouvir de novo).

### Cena 8: O Barco e a Tempestade
- N80 + A23 ("De novo."): tocadas quando o jogador volta ao checkpoint da praia. A23 é **igual**. N80 foi **adaptada**: no roteiro, o herói acordava "ao lado do Alquimista", mas ele não pode sair do vilarejo (proibição do Druida, cena 2). Agora o Alquimista fala por telepatia, como no resto da praia e do barco.
- N81, N82: **adaptadas** (N81 ganhou "Aperte W para empurrar o barco").
- A24: **adaptada** ("te dei a Triangular **superior**", pelo mesmo motivo da A20).
- **Novas:** N83_1/2/3 (cada relâmpago), N87 (a pergunta), N84 (acertou), N85 (onda acerta o barco), N86 (chegada à ilha, adaptada do roteiro).
- **Justificativas** J01 a J06: **novas** (pedido da professora).

### Cena 9: O Farol
- N90, A25: **igual**.
- N91: **adaptada**. O jogador para **diante** da porta da masmorra.
- G12, N92, N93: **novas**. N92 é o fim da DEMO; N93 ("Obrigado por jogar!") fecha a DEMO e o jogo completo.
- A26: **nova**, só no jogo completo. O Alquimista deixa um checkpoint no farol e lembra que "o dragão teme o zero".
- A31, A32, A33: **novas**, só no jogo completo. A lição de diagonal, identidade e "o tipo mais específico", com N71 para ouvir de novo.

### Cena 10: A Masmorra
- N100 e V02 (a voz das paredes contando a história): **igual**.
- N101: **igual** ("À esquerda, o rangido de uma armadura. À direita, passos pesados de pedra").
- G13, N102 (A = armadura, D = pedra), N103 + A27 (volta ao checkpoint do farol): **novas**.

### Cena 11A: O Cavaleiro Fantasma e o Banquete
- CF01, N110, CF02, CF03, N112, CF04, N113: **iguais ou quase**. CF03 e CF04 trocaram "tudo vira zero" por "todos os números são zero", que é a definição correta.
- N111 (W comer / S recusar): **nova**. Comer tira 1 vida, como no roteiro.
- CF05 a CF08: **novas**. É o teste do zero, A + 0 = A, porque o roteiro não tinha conta nesse caminho.
- CF09 a CF16 e N150: **novas**. É o espelho: a transposta é o reflexo, e a simétrica é igual ao reflexo, com as dicas de como resolver. N113 mudou para "O espelho se apaga...".

### Cena 11B: O Golem e o Puzzle
- N115, GO01, GO02, GO04, N120: **iguais**. O Golem falava em MAIÚSCULAS no roteiro; aqui o texto está normal, e a voz grave e lenta faz esse papel.
- G14, GO03, G15_igual/G15_dobro: **novas** (dica, pergunta e explicação dos erros).
- GO05, G16, N116_1/2/3, N117, N118, N119, GO06, GO07_nula/identidade/diagonal e G18_nula/identidade/diagonal: **novas**. É o puzzle das pedras do MVP, que no roteiro só era citado no título da cena: o Golem pede um tipo por salto, e o Grilo dá a dica.

### Cena 12: O Dragão
- N121, DR01, N127: **iguais**.
- A28: **adaptada**. O "Subtraia a matriz dela mesma!" do roteiro virou o plano da luta: dizer o tipo de cada fogo e, no fim, apagar o último com a nula.
- A36, A37, A38: **novas**. É a receita de como classificar e de como fazer o golpe final, com N71 para ouvir de novo.
- N122_1/2/3, N123, N124, N125, N126, N128, N129, A29_igual/A29_dobro, A34, A35, DR02: **novas** (2 rodadas de classificação + o golpe final).
- N134: **nova**. O tesouro atrás do dragão caído: "É o bastante para as ervas da sua mãe."

### Pedaços de justificativa (novos)
- TIPO_* (o nome de cada tipo nas opções), JT_* (por que é de tal tipo), JN_* ("Não é a matriz X.") e J_MAIS_ESPECIFICO.
- Saíram J07 a J09 (justificativas da pedra quase nula), que não são mais usadas.

### Epílogo
- A30, N131, M02: **iguais**. N130: **adaptada**. O roteiro falava da neblina clareando; agora são o cheiro do dragão indo embora e as criaturas se acalmando.
- A39: **nova**. O Alquimista confessa que já tinha mandado outros magos ("Mas você foi o primeiro que entendeu o zero"). Fecha o "eles sempre acham que são os primeiros" do Dragão e o "ele não é tão forte assim" do começo.
- N133, N135, N136: **novas**, na voz do **Narrador**. O herói leva o ouro à casa de cura; o **Druida** (antes só citado) compra as ervas, que vão curar a mãe; a **Mãe** acorda e sorri; e o Druida libera o Alquimista para sair do vilarejo. O Druida e a Mãe **não falam** no epílogo: aparecem só na narração. A Mãe só tem voz própria no bilhete da cena 1 (`ME01_01`).
- G17 (o Grilo responde ao Max), N132 ("Fim de Mathrix Souls."): **novas**.

### Neblina removida
A neblina do roteiro saiu da história, por decisão da equipe, porque complicava a motivação (se a neblina indo embora curasse a mãe, o tesouro não seria necessário). Mudaram: A06 (o Druida proíbe o Alquimista de sair porque "as criaturas de fora ficam mais agitadas nesta época"), V02 (o farol guiava "os navios no escuro"), N130 e N133.

### Como a história se fecha
| Aberto no começo | Fechado no fim |
|---|---|
| A mãe doente, e as ervas custam ouro (cena 1) | O ouro do dragão paga as ervas, e a mãe melhora (epílogo) |
| As criaturas de fora estão agitadas, e o cheiro do dragão piora tudo (cena 2) | Sem o dragão, o cheiro vai embora e as criaturas se acalmam (epílogo) |
| O Druida proíbe o Alquimista de sair (cena 2) | O Druida libera o Alquimista (epílogo) |
| "Ele não é tão forte assim" (cena 2) e "eles sempre acham que são os primeiros" (cena 12) | O Alquimista confessa que mandou outros magos antes e que teve pressa com eles (epílogo) |
| Os magos que não voltaram: o Taverneiro, o Grilo, o Goblin e o Marinheiro dão pistas, e os Ecos sussurram | O herói acha o chapéu azul e o amuleto de cristal atrás do dragão; o farol fica aceso por eles |
| "O dragão tem um ponto fraco" (cenas 2 e 9) e "o coração da matriz" (cenas 9 a 11) | O Alquimista ensina o determinante, e o herói lê o coração do último fogo (cena 12) |
| O bote Andorinha à deriva (cenas 8 e 9) | O Marinheiro leva o herói de volta para casa nele (epílogo) |
| O herói não sabe usar a magia (cena 1) | Ele domina as matrizes e virou "um mago de verdade" (epílogo) |

### Sistema
- N03, N05, S12: **mudaram**. Saiu o "aperte Enter"; entraram as setas, a velocidade da fala e o "não precisa esperar a fala terminar".
- N08_0.75 a N08_2.0, N08_max, N08_min, N09: **novas** (ajuste de velocidade da fala; só são ditas no menu).
- N140, N141, SC_1 a SC_12, SC_11A, SC_11B, SC_EPI, SC_INI, SC_FIM: **novas** (seleção de cenas). N03 e N05 passaram a citar a tecla C.
- N160, N161: **removidas** junto com a tecla G (a versão 1 só tem vozes do computador). S12 e G02 citam a tecla O.
- N05 (como jogar, tecla S no menu) e S12 (comandos, tecla H): **resumidas** para não cansar, com o mais usado primeiro. O N05 fica no essencial (W A S D, as três respostas, não precisa esperar, R e H) e o S12 lista o resto em uma frase curta por tecla.
- G02 (o Grilo explicando os comandos): **mudou**. Agora ele também ensina as teclas + e −.
- N04: **mudou**. Antes dizia que o jogo completo estava em construção; agora anuncia o início dele.
- S11_nula, J07 a J09 (justificativas da nula), NUM_10 a NUM_20: **novas**.

---

## 5. Decisões de design (para revisar)

| Decisão | Por quê |
|---|---|
| Respostas de múltipla escolha com **A / W / D** (1ª, 2ª, 3ª) | Usa as mesmas teclas de direção: esquerda, meio, direita |
| Esquiva para o **lado contrário** do golpe (esquerda → D, direita → A, frente → S) | É o movimento natural de fugir do golpe |
| Goblin ataca 3 vezes antes do pedágio | O MVP pede o tutorial de esquiva pelo som |
| Respostas erradas do goblin são **subtração** e **multiplicação posição a posição** | São erros comuns, e o Grilo explica cada um |
| Tempestade: 3 relâmpagos (2x2, 2x2, 3x3) | Dificuldade crescente |
| Matrizes da tempestade sorteadas | Cada partida é diferente, e voltar ao checkpoint não vira decoreba |
| Caminho vermelho não tira vida | O roteiro só manda o jogador de volta à bifurcação |
| Checkpoint: goblin → recomeça o goblin; tempestade → volta à praia | Segue o roteiro ("Este é o meu checkpoint") |
| "W para continuar" é falado só nas 3 primeiras vezes | Depois o jogador já sabe, e a repetição cansa |
| Checkpoint novo **no farol** (jogo completo) | Morrer na masmorra não obriga a refazer a tempestade. Perder no Dragão volta ao farol, e o jogador pode escolher o outro guardião |
| As **vidas não voltam** entre as cenas, só ao morrer | Era assim na DEMO; errar no Goblin pesa até o fim. Se ficar difícil demais, dá para devolver as 3 vidas em cada checkpoint |
| Os dois guardiões ensinam a nula, de jeitos diferentes, e cada um ensina algo a mais (Cavaleiro: transposta e simétrica; Golem: pratica identidade e diagonal nas pedras) | O roteiro dá a Matriz Nula nos dois caminhos, e assim cada caminho tem a sua matéria própria |
| O Dragão só cobra os tipos que o jogador aprendeu | Quem veio pelo Golem não viu a simétrica, então ela não aparece para ele |
| Tudo em 2x2 | Quatro números por opção: pergunta curta de ouvir e resposta simples |
| Diálogo que ensina antes de cada desafio novo, com opção de ouvir de novo | Quem joga precisa saber **como** resolver, não só o nome do tipo |
| Banquete: comer tira 1 vida, mas o Cavaleiro dá a nula do mesmo jeito | Exatamente como no roteiro |
| Pedras e fogo do Dragão sorteados | Igual à tempestade: voltar ao checkpoint não vira decoreba |

---

## 6. Limitações atuais (notebook e `.exe`)

O `.exe` de hoje roda o mesmo código do notebook, então as limitações valem para os dois:
- **No Jupyter, toda tecla precisa de Enter** e não dá para interromper a fala, porque ele não deixa ler o teclado na hora. No `.exe` e no terminal isso já funciona.
- **Sem som estéreo:** o lado do golpe é dito em palavras. Com pygame, o golpe tocaria no fone esquerdo ou direito.
- **Sem tempo limite na esquiva:** o jogo espera a tecla para sempre. Dá para pôr alguns segundos para reagir.
- **A velocidade da fala não acelera as gravações** (ver "Ajudas para quem joga só ouvindo").
- **Interromper a fala só funciona com a voz SAPI e com o pygame.** Nas reservas (PowerShell, `pyttsx3`, `winsound`), a fala vai até o fim, mas a tecla continua sem Enter.
- Leitores de tela não navegam bem pelo Jupyter. Por isso a narração própria (gravações ou voz da Maria) é obrigatória, e o `.exe` é o jeito certo de jogar.

**Ideia para a próxima versão:** as funções `escolher`, `tocar` e `som` concentram toda a entrada e saída. O pygame já está nos `.exe`, mas hoje ele só toca as gravações; o som estéreo dos golpes ainda não é usado. Trocando só essas funções, as cenas e as falas continuam iguais.

---

## 7. Como foi testado

Um jogador automático percorreu o notebook inteiro (sem pausas e sem voz) em dois cenários:

1. **Sem erros:** abre as instruções e o "jogo completo" no menu, aperta uma tecla inválida, H, V e R, e joga a DEMO até o fim.
2. **Com erros:** insiste no caminho vermelho, perde as 3 vidas no goblin (volta ao goblin), erra o pedágio, usa R e P, perde as 3 vidas na tempestade (volta à praia, "De novo.") e termina a DEMO. Neste cenário, foram usados arquivos `.wav` de teste para conferir que os pedaços gravados tocam na ordem certa.

Os dois chegaram ao fim sem erro, e quase todas as falas foram ditas em algum dos dois cenários (a G10_multiplicacao depende do sorteio).

**Jogo completo:** outro jogador automático rodou quatro cenários:
1. DEMO até o fim.
2. Jogo completo pelo Cavaleiro, sem erros.
3. Jogo completo pelo Golem, sem erros.
4. Jogo completo com erros: errou esquivas, a pergunta do Golem, saltos, o teste do zero e o fogo do Dragão; comeu o banquete; **morreu duas vezes na masmorra e voltou ao checkpoint do farol nas duas**; passou pelos dois guardiões.

Os quatro terminaram sem erro. Os três jogos completos venceram o Dragão e chegaram ao epílogo com as magias soma, triangular e nula.

**Voz e `.exe`:**
- Medi o tempo de cada fala para confirmar que a voz da Maria lê cada frase inteira. Foi assim que apareceu o bug do `pyttsx3`, que só falava a primeira frase.
- A reserva pelo PowerShell foi testada à parte e fala frases com acento no tempo certo.
- O `MathrixSouls.exe` abriu, leu o menu inteiro com a voz da Maria (cerca de 40 segundos) e fechou com a tecla Q. O `.exe` de entrega também rodou **sozinho**, copiado para uma pasta vazia.
- As vozes por personagem foram medidas nos dois motores (SAPI e PowerShell). O nome do personagem é dito só quando ele muda, e textos com `&`, `<` e aspas não quebram a voz.

**Formatos de áudio:** gerei falas de teste em `.wav`, `.ogg` e `.mp3`. As três tocaram inteiras pelo notebook e pelo `.exe` de desenvolvimento: o menu levou 24 segundos com elas, contra 37 segundos só com a voz sintetizada.

**Ainda falta:**
- Testar no Jupyter de verdade.
- Testar o `.exe` num computador sem Python.
- Testar com as gravações reais e, de preferência, com alguém jogando de olhos fechados.

---

## 8. Próximos passos sugeridos

1. Decidir entre o roteiro (soma/triangular) e o MVP (classificação 1 a 5). Ver o aviso da seção 1.
2. Gravar as falas e os efeitos, acompanhando pelo Apêndice.
3. Testar de olhos fechados e ajustar o ritmo (`VELOCIDADE`) e o texto das falas.
4. Melhorar o `.exe` com pygame (estéreo, tecla sem Enter, tempo de esquiva) e testá-lo num computador sem Python (ver a meta no topo deste documento).
5. Jogar o jogo completo de olhos fechados e ajustar a dificuldade: vidas, número de rodadas do Dragão e de saltos nas pedras (`RODADAS_DRAGAO`, `SALTOS`).
