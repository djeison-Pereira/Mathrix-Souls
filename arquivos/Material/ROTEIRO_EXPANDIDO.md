# Mathrix Souls: roteiro expandido (proposta para revisão)

> **Status:** aplicado no notebook (`mathrix_souls.ipynb`) em nov/2026. Na versão 1, tudo sai na voz do computador; os dubladores abaixo valem para quando houver gravação.
> A matemática e as mecânicas **não mudam**. O que muda é a história: mais diálogos, falas mais longas, dois personagens novos (Taverneiro e Marinheiro) e um fio de mistério que atravessa o jogo inteiro.

---

## 1. Elenco e quem dubla

| Dublador | Personagens | Prefixo dos áudios |
|---|---|---|
| **Felipe** | Narrador, Grilo Falante | `N`, `G` |
| **Vinícius** | Goblin (Trambique) · *proposta:* Max e os Ecos | `GB`, `MX`, `V` |
| **Matheus** | Taverneiro (Bartolo) · *proposta:* Cavaleiro Fantasma | `T`, `CF` |
| **João** | Marinheiro (Bento) · *proposta:* Dragão | `MR`, `DR` |
| **Daniel** | Alquimista, Golem | `A`, `GO` |
| **Protagonista** | É o jogador: não tem voz. Quando ele "fala", o jogador escolhe a resposta com as teclas, e o Narrador conta o que ele disse. | (sem áudio) |
| Mãe | *a definir:* uma fala só, o bilhete da cena 1 (precisa de uma voz feminina) | `ME` |
| Sistema | *proposta:* continua na voz do computador (são frases curtas de menu, vida e acerto) | `S`, `SV`, `SC` |

**Por que essa divisão dos personagens sem dono:** a regra foi **nunca pôr o mesmo dublador em dois personagens da mesma cena**, para quem joga de olhos fechados não confundir.
- **Max → Vinícius:** o Goblin nunca aparece na taverna. O Max é arrastado e bêbado; o Goblin, agudo e rápido.
- **Cavaleiro → Matheus:** o Taverneiro só aparece na taverna, bem longe da masmorra.
- **Dragão → João:** o Marinheiro fica no farol (cena 9) e só volta no epílogo; o Dragão é na cena 12. *Não* dei o Dragão ao Daniel porque o Alquimista fala durante a luta inteira.
- **Ecos (a "voz misteriosa") → Vinícius, sussurrando.** Ela aparece na bifurcação e na masmorra, onde o Goblin não está.

## 2. Nova organização dos áudios

Como ninguém gravou nada ainda, todos os códigos da história foram renumerados assim:

**`PREFIXO` + `número da cena` + `_` + `ordem da fala`**, por exemplo `T02_03` = Taverneiro, cena 2, 3ª fala.

- Cada dublador acha as próprias falas pelo prefixo, e elas já ficam em ordem de cena.
- Entre colchetes está o código antigo, quando a fala já existia: `[A04]`.
- **Não mudam:** menu, sistema, salvamento, seleção de cenas e os pedaços de leitura de matriz (`NUM_`, `MAT_`, `OPCAO_`, `TIPO_`, `J..`), porque são montados pelo código.

**Legenda:** 🆕 fala nova · ✏️ fala que já existia e foi ampliada · ＝ fala que ficou igual · ▶ escolha do jogador · *[som]* efeito sonoro

---

## 3. O fio novo da história: os magos que não voltaram

Hoje, a única pista de que o Alquimista mandou outros magos antes é o Dragão dizendo "eles sempre acham que são os primeiros" e a confissão no fim. Na versão expandida, essa pista aparece aos poucos:

| Cena | Pista |
|---|---|
| 2 Taverna | O Taverneiro cochicha: "os últimos que aceitaram trabalho dele nunca mais pediram café aqui." |
| 3 Lição | O Alquimista solta: "já é melhor do que o meu último aluno." |
| 4 Grilo | O Grilo lembra de um mago que passou pela trilha e nunca voltou. |
| 5 Bifurcação | Um sussurro diz "Volte..." do caminho vermelho, e ninguém sabe de quem é. |
| 6 Goblin | O Goblin cobra uma dívida de "um mago de chapéu azul". |
| 9 Farol | O Marinheiro conta que ensinou a charada da porta para outros magos: o do chapéu azul e uma moça com um amuleto de cristal. |
| 10 Masmorra | O sussurro volta: são os **ecos** dos magos que não voltaram. |
| 12 Dragão | O Dragão se gaba de ter vencido todos. Atrás dele, o herói encontra o chapéu azul e o amuleto de cristal. |
| Epílogo | O Alquimista confessa: com os outros, ele teve pressa e mandou direto para o dragão. Por isso, desta vez, ensinou no caminho e deixou checkpoints. O Marinheiro acende o farol por eles. |

**O ponto fraco do dragão é o determinante, o "coração" da matriz.** É uma conta de verdade: multiplicar as duas diagonais e subtrair. A pista aparece aos poucos, sem a palavra "determinante", que só surge quando o Alquimista ensina antes da luta:
- **Cena 2:** o Alquimista diz que o dragão tem um ponto fraco e que vai contar "na hora certa".
- **Cena 9:** o Marinheiro ouviu dizer que os magos do farol "liam o coração de uma matriz".
- **Cena 10:** os Ecos explicam que o coração é "um único número, escondido entre os outros".
- **Cena 11:** o guardião confirma, pelos dois caminhos. O Cavaleiro diz "não ataque o fogo, leia o coração dele", e o Golem diz que "fogo nenhum aguenta ouvir o próprio coração".
- **Cena 12:** o Alquimista ensina a conta, e o jogador a usa no último fogo.

**Por que os outros falharam e o herói não:** os outros foram com pressa. Aprenderam só a soma, comeram o banquete e atacaram o dragão sem escutar o fogo. O herói aprende uma magia de cada vez e escuta antes de agir, que é exatamente o que o jogador faz.

E dois fios menores:
- **A primeira faísca:** na cena 1, o herói lembra que a primeira faísca de magia dele queimou a cortina da cozinha. No fim, ele mostra a ela uma faísca controlada.
- **O bote "Andorinha"** que o herói usa na tempestade é o bote salva-vidas do navio do Marinheiro. No naufrágio, a corda arrebentou, e a correnteza levou o bote até a praia do continente. No fim, o Marinheiro leva o herói de volta para casa nele (hoje o jogo não explica como o herói sai da ilha).

---

## Cena 1: A Casa

*[som: um galo canta ao longe; o vento arranha a janela]*

- `N01_01` [N10] ＝ **Narrador:** Você é um jovem mago iniciante e acaba de acordar em uma pequena casa, longe do vilarejo de Trim, em um continente desconhecido que guarda propriedades misteriosas.
- `N01_02` [N11] ＝ **Narrador:** Você teve um sonho: enfrentava grandes monstros e desafios com magias absurdamente poderosas. Ao despertar, porém, lembra que ainda sabe pouco de magia e não faz ideia de como usá-la a seu favor.
- `N01_03` 🆕 **Narrador:** Ao lado da cama, uma tigela vazia e um bilhete, com a letra caprichada da sua mãe, escrito antes de ela adoecer. Nele está escrito:
- `ME01_01` 🆕 **Mãe:** *(lendo o bilhete, carinhosa e devagar)* Coma alguma coisa antes de sair.
- `N01_04` [N14] ＝ **Narrador:** O que realmente tira seu sono é a condição de sua mãe. Ela está doente e permanece na casa de cura do vilarejo, sob os cuidados do Druida, mestre no preparo de poções e remédios. Só que as ervas raras capazes de salvá-la custam mais ouro do que você jamais viu.
- `N01_05` 🆕 **Narrador:** Ontem, quando você a visitou, ela segurou a sua mão e disse que tudo ia ficar bem. Mas, no canto do quarto, o Druida balançou a cabeça devagar. As ervas estão acabando, e o pouco ouro da família também.
- `N01_06` [N12] ＝ **Narrador:** Aperte W para pegar o seu antigo cajado de madeira e sair de casa.

▶ **W:** pegar o cajado

- `N01_07` 🆕 **Narrador:** Na saída, você passa pela cozinha e lembra do dia em que soltou a sua primeira faísca de magia, sem querer, e queimou a cortina.

*[som: porta de madeira rangendo]*

- `N01_08` [N13] ＝ **Narrador:** Entre a decepção e a preocupação, você pega o cajado e sai rumo à taverna, atrás de um café da manhã e, quem sabe, de algum trabalho que pague bem.

---

## Cena 2: A Taverna

*[som: murmúrios, canecas batendo, lareira estalando]*

- `N02_01` 🆕 **Narrador:** A taverna Caneco Torto já está cheia logo cedo: lenhadores, caçadores e um bardo desafinado num canto. O cheiro de pão quente se mistura com o de cerveja derramada. Atrás do balcão, um homem grandalhão enxuga canecas: é o Bartolo, o taverneiro.
- `T02_01` 🆕 **Taverneiro:** Olha só quem apareceu, o pequeno mago! Senta aí, senta. O de sempre? Pão, queijo e leite morno?
- `N02_02` 🆕 **Narrador:** Aperte W para aceitar o café da manhã, ou S para dizer que está sem dinheiro.

▶ **W:** aceitar
- `T02_02` 🆕 **Taverneiro:** Isso! Saco vazio não para em pé, e mago com fome não solta nem faísca.

▶ **S:** sem dinheiro
- `T02_03` 🆕 **Taverneiro:** Dinheiro? Deixa disso. Sua mãe sempre pagou tudo certinho. Eu penduro na conta, e quando ela sair da casa de cura a gente acerta.

*(as duas escolhas seguem daqui)*

- `T02_04` 🆕 **Taverneiro:** E ela, como está?
- `N02_03` 🆕 **Narrador:** Você conta que ela piorou, e que as ervas do Druida custam uma fortuna. O Bartolo fica sério e enxuga a mesma caneca três vezes.
- `T02_05` 🆕 **Taverneiro:** Fortuna não falta pra quem tem coragem... ou loucura. Dizem que tem um dragão dormindo em cima de uma montanha de ouro, lá embaixo do farol da ilha. Mas quem foi atrás dele não voltou pra contar.
- `N02_04` [N20] ＝ **Narrador:** No balcão está seu velho amigo Max, passando mal: geme, suspira e deixa a cabeça cair sobre a madeira, completamente bêbado.
- `T02_06` 🆕 **Taverneiro:** E esse aí chegou ontem à noite falando de dragões e de matrizes. Bebeu meio barril e apagou. Tenta falar com ele, se quiser. Boa sorte.
- `N02_05` [N21] ＝ **Narrador:** Aperte W para tentar falar com o Max, ou S para deixá-lo em paz.

▶ **W:** falar com o Max
- `MX02_01` [M01] ＝ **Max:** Hmm... matriz... dragão... mais uma caneca, por favor...
- `T02_07` 🆕 **Taverneiro:** Mais uma caneca, nada. Você vai tomar é água, Max.

*(as duas escolhas seguem daqui)*

- `N02_06` [N22] ＝ **Narrador:** Conhecendo o Max, você sabe que não arrancaria uma frase com sentido dele.
- `N02_07` [N23] ＝ **Narrador:** Atrás de você, uma voz:
- `A02_01` [A01] ＝ **Alquimista:** Finalmente desmaiou. Credo, esse aí fala demais.
- `T02_08` 🆕 **Taverneiro:** *(cochichando)* Cuidado, garoto. Esse aí paga bem... mas os últimos que aceitaram trabalho dele nunca mais pediram café aqui.

*[som: frascos tilintando]*

- `N02_08` [N24] ＝ **Narrador:** Você se vira. Frascos tilintam, e o cheiro de ervas queimadas chega antes das palavras. É o Alquimista Algébrico.
- `A02_02` [A02] ＝ **Alquimista:** Ah, olha só, o jovem mago iniciante. Max e o Druida me falaram de você. Quero te propor um acordo.
- `A02_03` 🆕 **Alquimista:** E você, Bartolo, pode parar de cochichar. Eu ouço tudo. Inclusive a parte do "nunca mais pediram café".
- `T02_09` 🆕 **Taverneiro:** Eu? Eu tava falando do tempo. Vai chover. Muito.
- `N02_09` [N25] ＝ **Narrador:** O Alquimista ainda não disse que acordo é esse. Aperte W para ouvir a proposta dele, ou S para recusar sem nem ouvir.

▶ **W ou S** (tanto faz: ele interrompe)

- `N02_10` [N26] ＝ **Narrador:** Antes que você diga qualquer coisa, ele te interrompe:
- `A02_04` [A03] ＝ **Alquimista:** Ah, ah, nem precisa responder. Ninguém recusa nada vindo do GRANDE alquimista da cidade.

*[som: um estalar de dedos e um sopro de vento]*

- `N02_11` [N27] ＝ **Narrador:** Um estalar de dedos, um sopro de vento, e de repente vocês estão sentados à mesa da sala de estar dele. O ar cheira a enxofre e a ervas queimadas, e frascos borbulham nas prateleiras.
- `A02_05` [A04] ＝ **Alquimista:** Gostou do teleporte? A maioria vomita na primeira vez. Bem, estamos aqui porque quero te fazer uma proposta: eu te ensino magia, e você mata um dragão pra mim, na masmorra do farol.
- `N02_12` 🆕 **Narrador:** Você tem perguntas. Aperte A para perguntar "por que eu?", W para perguntar sobre o dragão, ou S para deixá-lo continuar.

▶ **A:** "por que eu?" (depois volta para a pergunta, sem essa opção)
- `A02_06` 🆕 **Alquimista:** Por que você? Porque eu vi a faísca que você solta quando fica nervoso. Essa aí, que acabou de chamuscar a sua manga. É magia de matriz, crua, sem lapidar. Coisa rara. E porque você precisa de ouro, e eu preciso de um dragão morto. Todo mundo sai ganhando.

▶ **W:** sobre o dragão (depois volta para a pergunta, sem essa opção)
- `A02_07` 🆕 **Alquimista:** O dragão? Grande, velho, mal-humorado e com um bafo que dá pra sentir daqui quando o vento sopra do mar. É esse cheiro que deixa as criaturas da floresta agitadas. Mas, cá entre nós, ele não é tão forte assim. Ele tem um ponto fraco, e eu te conto qual é... na hora certa.

▶ **S:** continuar

- `A02_08` [A05] ＝ **Alquimista:** É uma bela viagem, se você sobreviver a ela. Você atravessa a floresta, chega à grande praia, pega um barco e alcança a ilha.
- `A02_09` [A06] ✏️ **Alquimista:** E por que eu mesmo não vou? Porque, desde que o dragão acordou, o cheiro dele deixa as criaturas de fora agitadas, e alguém precisa proteger Trim. O Druida me proibiu de sair do vilarejo enquanto aquele bicho estiver vivo. Então eu ensino, e outro vai no meu lugar.
- `A02_10` [A08] ＝ **Alquimista:** E não me olhe com essa cara: sei da sua mãe, e ela precisa dos remédios logo. Dragões dormem em cima de ouro, e o tesouro dele é todo seu. Dá para pagar as ervas do Druida e ainda sobra.

▶ **W:** continuar

- `N02_13` [N28] ＝ **Narrador:** Ele te entrega uma pequena pedra. Ao tocar sua mão, ela é absorvida pela pele, deixando um calor suave.
- `A02_11` [A07] ＝ **Alquimista:** Fui eu que fiz. Ela libera o seu potencial mágico. Cada mago tem um tipo de magia, e o seu são as matrizes. O tipo mais forte.
- `A02_12` 🆕 **Alquimista:** Sentiu esse calor? É o seu potencial acordando. Agora sente direito nessa cadeira, porque a aula vai começar. E eu não repito... quer dizer, repito, mas reclamo.

---

## Cena 3: A Lição da Matriz Quadrada

*[som: o cajado bate no chão e ecoa como um sino grave]*

- `A03_01` [A10] ＝ **Alquimista:** Uma matriz é uma tabela de números, com linhas e colunas. Quando tem o mesmo número de linhas e colunas, é quadrada. A Matriz Quadrada é a sua primeira magia, a base de todas as outras.
- `A03_02` 🆕 **Alquimista:** Pense numa prateleira de frascos: cada frasco tem o seu lugar, numa linha e numa coluna. Troque um frasco de lugar, e a poção explode. Com matriz é igual: a posição de cada número importa.
- `A03_03` [A11] ✏️ **Alquimista:** Para somar duas matrizes, elas precisam ter o mesmo tamanho: o mesmo número de linhas e de colunas. Aí você soma cada número com o número que está na mesma posição da outra matriz. Veja: vou te mostrar duas matrizes, cada uma com duas linhas e duas colunas. Na primeira matriz, a linha de cima tem os números um e dois, e a linha de baixo tem três e quatro. Na segunda matriz, a linha de cima tem cinco e seis, e a linha de baixo tem sete e oito.
- `A03_04` [A12] ✏️ **Alquimista:** Agora some quem está no mesmo lugar. Na linha de cima: um mais cinco, seis; dois mais seis, oito. Na linha de baixo: três mais sete, dez; quatro mais oito, doze. O resultado é uma matriz com seis e oito em cima, e dez e doze embaixo. Simples, não? Eu sou um ótimo professor.
- `N03_01` [N30] ＝ **Narrador:** Aperte W se entendeu, ou S para ouvir a explicação de novo.
- `N03_02` [N31] ＝ **Narrador:** A pedra pulsa na sua pele. Você sente o poder da Matriz Quadrada passar a fazer parte de você.
- `A03_05` 🆕 **Alquimista:** Viu? Nada explodiu. Já é melhor do que o meu último aluno.

---

## Cena 4: O Grilo Falante

- `A04_01` [A13] ＝ **Alquimista:** Agora vá. Saia pela porta, siga a trilha, e a floresta começa logo depois. Se ouvir uma vozinha por aí, não se assuste: é o grilo falante. Ele guia quem passa por essa trilha.
- `N04_01` 🆕 **Narrador:** O vilarejo de Trim vai ficando para trás: o sino da praça, o martelo do ferreiro e, por último, o telhado da casa de cura, onde está a sua mãe.

*[som: cri-cri alegre vindo da esquerda]*

- `N04_02` [N40] ＝ **Narrador:** Na trilha, o silêncio dura pouco. Um cri-cri alegre vem da esquerda, e uma vozinha se aproxima:
- `G04_01` [G01] ＝ **Grilo:** Olá, jovem mago! Eu sou o Grilo Falante, seu guia e narrador nesta jornada. Pode contar comigo para saber onde você está e para onde ir... e para falar bastante, claro.
- `N04_03` [N41] ＝ **Narrador:** É um pequeno grilo que pula de galho em galho, falando mais do que o seu tamanho sugere.
- `G04_02` 🆕 **Grilo:** E antes que você pergunte: não, eu não sou um grilo comum. Grilo comum faz cri-cri. Eu faço cri-cri, narro, dou conselhos e conheço cada pedra desta floresta. E, modéstia à parte, canto muito melhor que aquele bardo da taverna.
- `G04_03` [G02] ＝ **Grilo:** Antes de tudo, os seus comandos. A é esquerda, D é direita, W é frente e S é trás. R repete o que eu acabei de dizer, O diz quais teclas valem agora, P pausa, V conta suas vidas e H lembra os comandos. Se eu estiver falando rápido ou devagar demais, use as teclas mais e menos. Vamos treinar! Aperte A para pular para a esquerda.
- `G04_04` [G03] ＝ **Grilo:** Isso! Agora D, para a direita.
- `G04_05` [G04] ＝ **Grilo:** Muito bem! Agora S, um passo para trás.
- `G04_06` [G05] ＝ **Grilo:** Perfeito! E W para seguir em frente.
- `G04_07` 🆕 **Grilo:** Você é bom nisso! O último mago que passou por aqui tropeçou em todas as raízes da trilha. Ele também ia atrás do dragão. Disse que voltava antes do inverno... Bom, já foram dois invernos.
- `G04_08` [G06] ＝ **Grilo:** Mais à frente, a trilha se divide. Dois caminhos, jovem mago. Um tem pássaros. O outro tem silêncio. Eu escolheria os pássaros.

---

## Cena 5: A Bifurcação

- `N05_01` [N50] ＝ **Narrador:** Você chega ao ponto em que a trilha se divide.

*[som: pássaros e um riacho à esquerda; vento seco à direita]*

- `N05_02` [N51] ＝ **Narrador:** À esquerda, o caminho da floresta é cheio de vida: pássaros, folhas e um riacho correndo ao longe.
- `N05_03` [N52] ＝ **Narrador:** À direita, o caminho vermelho tem terra cor de ferrugem, vento seco e nenhum bicho.
- `N05_04` [N53] ＝ **Narrador:** Aperte A para o caminho da floresta, ou D para o caminho vermelho.

▶ **D:** caminho vermelho
*[som: vento seco, nenhum bicho]*
- `V05_01` [V01] ＝ **Ecos:** Volte...
- `N05_05` [N54] ＝ **Narrador:** Do fundo do caminho vermelho, um sussurro. Aperte S para voltar, ou W para insistir.
  - ▶ **W:** insistir *[som: terra desmoronando]*
    - `N05_06` [N55] ＝ **Narrador:** O chão cede sob seus pés, tudo escurece... e você desperta de novo na bifurcação.
    - `G05_01` [G07] ＝ **Grilo:** Eu avisei! Pássaros, jovem mago. Pássaros.
  - ▶ **S:** voltar
    - `N05_07` [N56] ＝ **Narrador:** Você volta para a bifurcação.
    - `G05_02` 🆕 **Grilo:** E aquele "volte" lá no fundo? Não fui eu, se é o que você está pensando. Eu tenho voz de tenor. Aquilo era... outra coisa.
- *(volta para a escolha do caminho)*

▶ **A:** caminho da floresta
- `N05_08` [N57] ＝ **Narrador:** Você segue pela trilha da floresta. Os pássaros cantam acima de você.
- `G05_03` 🆕 **Grilo:** Viu? Pássaros. Pássaros nunca erram. Bom, quase nunca. Teve aquela vez do pica-pau... deixa pra lá.

---

## Cena 6: O Goblin

*(Se o jogador perdeu as 3 vidas e voltou aqui:)*
- `N06_01` [N63] ＝ **Narrador:** Tudo escurece... Você respira fundo e tenta de novo.
- `G06_01` [G11] ＝ **Grilo:** De volta à floresta. Vamos lá, jovem mago, dessa vez vai!

*[som: risada aguda circulando ao seu redor]*

- `N06_02` [N60] ＝ **Narrador:** Na floresta, uma risada aguda circula você, rápida demais para ser seguida. Um goblin salta à sua frente!
- `GB06_01` [GB01] ✏️ **Goblin:** Alto lá! Quem pisa na floresta do Trambique paga pedágio! Pedágio de ida, pedágio de volta e taxa por respirar perto da minha árvore! Mas antes... vamos ver se você é rápido!
- `G06_02` 🆕 **Grilo:** Ah, não. O Trambique. Ele cobra pedágio até de formiga.
- `GB06_02` 🆕 **Goblin:** E cobro mesmo! Formiga carrega muito peso, estraga a estrada!
- `G06_03` [G08] ＝ **Grilo:** Cuidado! Escute de onde vem o golpe e pule para o lado contrário. Golpe da esquerda, aperte D. Golpe da direita, aperte A. Golpe de frente, aperte S para recuar.

**3 esquivas.** Antes de cada golpe, o Goblin provoca (fala nova, uma por golpe):
- `GB06_03` 🆕 **Goblin:** Toma essa!
- `GB06_04` 🆕 **Goblin:** Para de pular! Fica parado, que dói menos!
- `GB06_05` 🆕 **Goblin:** Último! Esse ninguém escapa!

Em cada golpe: *[som: golpe vindo de um lado]* + `N06_03` [N61_esquerda] / `N06_04` [N61_direita] / `N06_05` [N61_frente] ＝ **Narrador:** O golpe vem da esquerda! / da direita! / de frente!

- `GB06_06` [GB02] ＝ **Goblin:** Grrr! Escorregadio! Então paga com a cabeça!
- `GB06_07` 🆕 **Goblin:** Pedágio de cabeça, quer dizer: pedágio inteligente! O Trambique não é só músculo. É cérebro também. Muito cérebro.
- `GB06_08` [GB03] ＝ **Goblin:** Duas matrizes, A e B. Some as duas e eu deixo você passar! A: dois e um em cima, zero e três embaixo. B: um e quatro em cima, cinco e dois embaixo. Quero a soma!
- `G06_04` [G09] ＝ **Grilo:** Lembra da lição: posição com posição. Escute as três respostas.
- `GB06_09` [GB06] ＝ **Goblin:** Qual é a soma de A mais B? Hein? Hein?

▶ **Errou:**
- `GB06_10` [GB05] ＝ **Goblin:** Errado! Hahaha! Paga de novo!
- `G06_05` [G10_subtracao] ＝ **Grilo:** Ops! Essa foi a subtração, não a soma. Na soma, comece pelo canto de cima, à esquerda: dois mais um.
- `G06_06` [G10_multiplicacao] ＝ **Grilo:** Ops! Aí você multiplicou posição com posição, não somou. Na soma, comece pelo canto de cima, à esquerda: dois mais um.

▶ **Acertou:**
- `GB06_11` [GB04] ＝ **Goblin:** Três, cinco, cinco, cinco! Grrr! Passa, passa, mago chato!
- `GB06_12` 🆕 **Goblin:** Mas na volta é dobrado! E se encontrar um mago de chapéu azul por aí, avisa que ele ainda me deve três moedas!

*[som: passos correndo entre as árvores]*

- `N06_06` [N62] ＝ **Narrador:** E some correndo entre as árvores.
- `G06_07` 🆕 **Grilo:** Chapéu azul... Eu lembro dele. Era o mago que tropeçava nas raízes. Também ia atrás do dragão.

---

## Cena 7: A Praia

*[som: ondas e gaivotas]*

- `N07_01` 🆕 **Narrador:** A floresta termina de repente, e o chão vira areia. O mar se estende até onde o ouvido alcança. Bem longe, quase sumindo no horizonte, um ponto de luz pisca devagar: o farol.
- `G07_01` 🆕 **Grilo:** Aquele é o farol. Dizem que ficou anos apagado, mas de uns tempos pra cá voltou a piscar. Alguém mora lá. Ou alguma coisa.
- `N07_02` [N70] ＝ **Narrador:** Ondas, gaivotas e areia sob os pés. A voz do Alquimista chega por telepatia, com um leve eco:
- `A07_01` 🆕 **Alquimista:** Testando, testando... Está me ouvindo? Ótimo. Telepatia é uma das minhas especialidades. As outras são todas as outras.
- `A07_02` [A20] ＝ **Alquimista:** Chegou à praia? Ótimo. Aqui você aprende a Matriz Triangular superior. Mas primeiro, a diagonal principal: é a linha que vai do canto de cima, à esquerda, até o canto de baixo, à direita.
- `A07_03` [A21] ＝ **Alquimista:** Na triangular superior, tudo o que fica embaixo da diagonal principal é zero, e os outros números ficam em cima dela, formando um triângulo. Por exemplo: um e dois em cima, zero e três embaixo. O zero está no canto de baixo, à esquerda, a única posição embaixo da diagonal. Ela corta caminho no meio da tempestade, e você vai precisar dela.
- `N07_03` [N71] ＝ **Narrador:** Aperte W se entendeu, ou S para ouvir a explicação de novo.
- `N07_04` [N72] ＝ **Narrador:** A pedra pulsa de novo.
- `A07_04` [A22] ＝ **Alquimista:** Este é o meu checkpoint. Se der algo errado, você volta para cá.
- `G07_02` 🆕 **Grilo:** Checkpoint... Ele fala cada palavra esquisita. Eu chamo isso de "o lugar onde a gente acorda depois de levar uma surra".

---

## Cena 8: O Barco e a Tempestade

*(Se o jogador perdeu as 3 vidas e voltou à praia:)*
- `N08_01` [N80] ＝ **Narrador:** Tudo escurece... e você acorda na praia. Na sua cabeça, a voz do Alquimista suspira:
- `A08_01` [A23] ＝ **Alquimista:** De novo.

- `N08_02` [N81] ＝ **Narrador:** Um barco de madeira, esquecido na areia. Aperte W para empurrá-lo para a água.

▶ **W:** empurrar o barco

- `N08_03` 🆕 **Narrador:** Na lateral do barco, letras gastas pelo sal: "Andorinha". É um bote salva-vidas, de algum navio grande que um dia passou por estas águas.
- `G08_01` 🆕 **Grilo:** Você sabe remar? ... Eu também não. Mas eu sei torcer muito bem.

*[som: madeira raspando na areia; remos rangendo]*

- `N08_04` [N82] ＝ **Narrador:** Você embarca sozinho. O mar está calmo, só o rangido dos remos. Até que o vento muda, o céu escurece e o primeiro trovão estoura.

*[som: vento forte e ondas batendo no casco]*

- `A08_02` [A24] ＝ **Alquimista:** Tempestade! Foi para isso que te dei a Triangular superior! A cada relâmpago, três matrizes vão aparecer. Ache a que tem zero embaixo da diagonal!

**3 relâmpagos** (como hoje):
- `N08_05` [N83_1] ＝ **Narrador:** Primeiro relâmpago!
- `N08_06` [N83_2] ＝ **Narrador:** Segundo relâmpago!
- `N08_07` [N83_3] ＝ **Narrador:** Terceiro relâmpago! O mais forte de todos!
- `N08_08` [N87] ＝ **Narrador:** Qual destas é triangular superior?
- `N08_09` [N84] ＝ **Narrador:** O barco corta a onda e segue em frente.
- `N08_10` [N85] ＝ **Narrador:** Uma onda gigante acerta o barco!

Entre os relâmpagos, o Grilo reage (fala nova, uma depois do 1º e outra depois do 2º acerto):
- `G08_02` 🆕 **Grilo:** Isso! Mais um desses e eu paro de ficar verde!
- `G08_03` 🆕 **Grilo:** Ainda tô verde. Mas é de orgulho!

*[som: o vento se acalma]*

- `N08_11` 🆕 **Narrador:** No meio da escuridão, uma luz forte varre o mar e para em cima do seu barco: o farol está apontado para você, como se alguém lá em cima tivesse visto você no meio das ondas.
- `N08_12` [N86] ＝ **Narrador:** O vento se acalma, e a proa bate em areia firme: a ilha.
- `G08_04` 🆕 **Grilo:** Terra firme! Nunca mais eu entro num barco. A não ser na volta. Que é obrigatória. Droga.

---

## Cena 9: A Ilha, o Farol e o Marinheiro

*[som: vento, mar distante e uma engrenagem velha girando]*

- `N09_01` [N90] ＝ **Narrador:** Silêncio, só o vento e o barulho distante do mar. O farol gira devagar, com um som de engrenagem velha.
- `N09_02` 🆕 **Narrador:** Passos arrastados descem a escada de pedra do farol. Uma lamparina balança, e uma voz rouca, gasta pelo sal, grita:
- `MR09_01` 🆕 **Marinheiro:** Ô de terra! Ou melhor, ô de mar! Faz quinze anos que ninguém chega vivo numa tempestade dessas. Foi você que eu vi lá no meio das ondas?
- `N09_03` 🆕 **Narrador:** Aperte W para dizer que sim, ou S para ficar em silêncio.

▶ **W:** dizer que sim
- `MR09_02` 🆕 **Marinheiro:** Pois foi a minha luz que te trouxe, rapaz. Girei o farol na sua direção com essas mãos velhas. De nada.

▶ **S:** ficar em silêncio
- `MR09_03` 🆕 **Marinheiro:** Não é de falar, é? Melhor assim. O mar também não fala, e é o mais sábio de todos. Mas foi a minha luz que te trouxe, viu?

*(as duas escolhas seguem daqui)*

- `MR09_04` 🆕 **Marinheiro:** Meu nome é Bento. Fui marinheiro do Andorinha, o navio mais rápido desta costa. Até a noite em que o dragão acordou e cuspiu fogo no mar. O Andorinha pegou fogo e afundou. Na confusão, a corda do bote salva-vidas arrebentou, e ele saiu à deriva antes que eu conseguisse pular dentro. Tive que nadar até esta ilha. Desde então, cuido do farol.
- `N09_04` 🆕 **Narrador:** Você conta que atravessou o mar num bote com o nome Andorinha.
- `MR09_05` 🆕 **Marinheiro:** O bote do Andorinha?! Então a correnteza levou ele até a praia do continente, e ele ficou lá na areia esse tempo todo, esperando... Teimoso, igualzinho ao dono. Se você chegou nele, é sinal. Velho marinheiro acredita em sinal.
- `G09_01` 🆕 **Grilo:** Ele fala com barco. Eu falo com pássaro. Tô começando a gostar dele.
- `MR09_06` 🆕 **Marinheiro:** E o grilo fala! Quinze anos sozinho, e o primeiro que aparece traz um grilo falante. Tá bom, tá bom. Quem conversa com o mar não pode reclamar de grilo.
- `N09_05` 🆕 **Narrador:** Na sua cabeça, a voz do Alquimista:
- `A09_01` [A25] ✏️ **Alquimista:** Chegou! O dragão está lá no fundo, embaixo do farol. O farol é antigo e cheio de guardiões. Cuidado onde pisa. E quem é esse aí com cheiro de peixe?
- `MR09_07` 🆕 **Marinheiro:** Essa voz na sua cabeça... É o Alquimista de Trim? Ele de novo! Ele mandou outros antes de você, sabia? Um de chapéu azul. Uma moça com um amuleto de cristal. Eu ensinei a charada da porta pra todos eles. Nenhum voltou pra me contar como era lá embaixo.
- `A09_02` 🆕 **Alquimista:** Detalhes, detalhes. Eles não tinham o meu método. Bom, tinham. Mas não tinham você.
- `N09_06` [N91] ✏️ **Narrador:** O marinheiro te leva até o pé do farol. Diante de você está a porta pesada da masmorra. Lá dentro, gotas ecoam em corredores longos.
- `MR09_08` 🆕 **Marinheiro:** Essa porta não abre com força. Abre com a cabeça. Foram os magos de matrizes que construíram o farol, e eles deixaram uma charada gravada na pedra. Diziam que esses magos conseguiam ler o coração de uma matriz, seja lá o que isso quer dizer. A pergunta eu sei de cor. A resposta, quem tem que saber é você.

**A charada da porta** (nova, revisa a magia que o jogador acabou de usar na tempestade):
- `MR09_09` 🆕 **Marinheiro:** Escuta bem: "Tenho tantas linhas quanto colunas. E embaixo da minha diagonal principal, só mora o zero. Quem sou eu?"
- `N09_07` 🆕 **Narrador:** Aperte A para uma matriz de duas linhas e três colunas. W para a Matriz Triangular superior. D para uma matriz com zero em cima da diagonal.

▶ **A** (errado)
- `MR09_10` 🆕 **Marinheiro:** Duas linhas e três colunas? Isso nem é quadrada, rapaz. A porta nem se mexeu. Escuta a charada de novo.

▶ **D** (errado)
- `MR09_11` 🆕 **Marinheiro:** Quase! Mas aí o zero mora em cima da diagonal, não embaixo. A porta nem se mexeu. Escuta a charada de novo.

▶ **W** (certo)
*[som: pedra pesada rangendo e se arrastando]*
- `MR09_12` 🆕 **Marinheiro:** Triangular superior! Escuta só: a porta tá rangendo... Abriu! Toda vez que essa porta abre, me dá um frio na espinha.

**Só no jogo completo:**
- `A09_03` [A26] ✏️ **Alquimista:** Vou deixar um checkpoint aqui no farol. Se a masmorra te derrubar, você volta para esta porta. E lembre: o dragão tem um ponto fraco. Antes da luta, eu te ensino qual é.
- `A09_04` [A31] ＝ **Alquimista:** Antes de entrar, mais duas magias. A Matriz Diagonal só tem números na diagonal principal; fora dela, tudo é zero. Por exemplo: dois e zero em cima, zero e cinco embaixo. Num dois por dois, escute os dois números de fora: o de cima à direita e o de baixo à esquerda. Se os dois forem zero, é diagonal.
- `A09_05` [A32] ＝ **Alquimista:** E a Matriz Identidade é a diagonal mais simples de todas: um em toda a diagonal e zero no resto. Um e zero em cima, zero e um embaixo. Ela é o número um das matrizes.
- `A09_06` [A33] ＝ **Alquimista:** Agora, preste atenção: uma matriz pode ser de vários tipos ao mesmo tempo. A identidade, por exemplo, também é diagonal, porque fora da diagonal ela só tem zero. Quando alguém lá dentro perguntar o tipo, diga sempre o mais específico, o nome mais exato: um e zero em cima, zero e um embaixo, não diga só diagonal, diga identidade.
- `N09_08` [N71] ＝ **Narrador:** Aperte W se entendeu, ou S para ouvir a explicação de novo.

**Nos dois modos:**
- `MR09_13` 🆕 **Marinheiro:** Eu vou ficar lá em cima, girando a luz. Se você vir um clarão lá embaixo, é o farol dizendo que ainda tem alguém esperando por você. E quando voltar... eu te levo pra casa no Andorinha. Palavra de marinheiro.
- `G09_02` [G12] ✏️ **Grilo:** Daqui para frente, jovem mago, nem eu sei o que vem. Mas eu vou junto! ... Eu vou junto, né? Tô indo. Tô indo.

**Fim da DEMO:**
- `N09_09` [N92] ✏️ **Narrador:** Fim da DEMO de Mathrix Souls. A porta está aberta. A masmorra, com seus guardiões, os ecos dos magos perdidos e o dragão, espera por você no jogo completo.
- `N09_10` [N93] ＝ **Narrador:** Obrigado por jogar! Aperte W para voltar ao menu.

---

## Cena 10: A Masmorra

*(Se o jogador perdeu as 3 vidas e voltou ao farol:)*
- `N10_01` [N103] ＝ **Narrador:** Tudo escurece... e você desperta diante da porta do farol, ao som da voz do Alquimista:
- `A10_01` [A27] ＝ **Alquimista:** De novo. Ainda bem que deixei o checkpoint aqui. Respire e entre outra vez.
- `MR10_01` 🆕 **Marinheiro:** Voltou inteiro? Mais ou menos inteiro. Bebe um gole de água, rapaz, e entra de novo. A porta já sabe quem você é.

*[som: porta pesada rangendo; gotas ecoando]*

- `N10_02` [N100] ＝ **Narrador:** Você empurra a porta pesada e entra na masmorra. Gotas ecoam em corredores longos.
- `V10_01` [V02] ✏️ **Ecos:** Há muito tempo, magos de matrizes construíram este farol para guiar os navios no escuro. Eles sabiam ler o coração de cada matriz: um único número, escondido entre os outros. Então veio o dragão, e o cheiro dele corrompeu os guardiões. Agora eles testam todo aquele que se aproxima.
- `V10_02` 🆕 **Ecos:** Volte... Nós também achamos que éramos os primeiros...
- `G10_01` 🆕 **Grilo:** Você ouviu isso? É a mesma voz do caminho vermelho! São eles... os magos que não voltaram. Tô com medo. Não conta pra ninguém que eu disse isso.

*[som: à esquerda, o rangido de uma armadura; à direita, passos de pedra]*

- `N10_03` [N101] ＝ **Narrador:** O corredor se divide. À esquerda, o rangido de uma armadura. À direita, passos pesados de pedra. Os dois caminhos levam ao dragão.
- `G10_02` [G13] ＝ **Grilo:** Dessa vez nem eu sei qual é melhor. Os dois têm cara de encrenca.
- `N10_04` [N102] ＝ **Narrador:** Aperte A para o corredor da armadura, ou D para o corredor de pedra.

---

## Cena 11A: O Cavaleiro Fantasma e o Banquete

*[som: o rangido de uma armadura vazia]*

- `N11A_01` 🆕 **Narrador:** Uma armadura vazia se levanta, peça por peça, com um barulho de metal enferrujado. Dentro do elmo não há rosto, só uma luz fria.
- `CF11_01` [CF01] ＝ **Cavaleiro:** Sou o Cavaleiro Fantasma. Há séculos guardo este corredor. Você deve estar faminto, jovem mago. Venha, sente-se.

*[som: pratos, talheres e cheiro de comida]*

- `N11A_02` [N110] ＝ **Narrador:** Uma mesa gigante surge do nada, com cheiro de carne assada, pão e frutas doces.
- `G11A_01` 🆕 **Grilo:** Banquete? Numa masmorra? Isso tem cara de armadilha. Mas que cheiro bom, hein...
- `CF11_02` [CF02] ＝ **Cavaleiro:** Este é o Banquete Gigante. Coma comigo. Ou recuse, se tiver coragem.
- `N11A_03` [N111] ＝ **Narrador:** Aperte W para comer, ou S para recusar.

▶ **S:** recusar
- `CF11_03` [CF03] ＝ **Cavaleiro:** Poucos resistem. Quem recusa fica de prato vazio, e merece a Matriz Nula: aquela em que todos os números são zero, vazia como o seu prato. O fogo do dragão às vezes vem assim, vazio e frio. Saiba reconhecê-lo.
- `CF11_04` 🆕 **Cavaleiro:** Sabe por que tão poucos recusam? Porque a fome é a armadilha mais antiga que existe. Os magos que vieram antes de você comeram. Todos eles.

▶ **W:** comer (perde 1 vida)
- `N11A_04` [N112] ＝ **Narrador:** O primeiro pedaço é doce e gelado, e você sente um pedaço da sua energia escapar.
- `CF11_05` [CF04] ＝ **Cavaleiro:** Ilusão cara, jovem mago! Mesmo assim, tome a Matriz Nula: aquela em que todos os números são zero. Você vai precisar dela mais do que eu.

**Teste do zero** (igual a hoje):
- `CF11_06` [CF05] ＝ **Cavaleiro:** Mas antes, mostre que entende o zero. Some a Matriz Nula a esta matriz: três e um em cima, dois e quatro embaixo.
- `CF11_07` [CF06] ＝ **Cavaleiro:** Qual é o resultado da soma?
- `CF11_08` [CF07] ＝ **Cavaleiro:** Isso. Somar zero não muda nada: a matriz continua a mesma. A Matriz Nula é o elemento neutro da soma.
- `CF11_09` [CF08_nula] ＝ **Cavaleiro:** Não. Somar zero não apaga a matriz: três mais zero continua três.
- `CF11_10` [CF08_mais_um] ＝ **Cavaleiro:** Não. Somar zero não acrescenta nada: três mais zero é três, não quatro.

**O espelho** (igual a hoje):
- `CF11_11` 🆕 **Cavaleiro:** Antigamente, eu protegia os magos que construíram este farol. Eles me ensinaram tudo o que sei de matrizes. Depois que o dragão chegou, o cheiro dele me prendeu aqui. Agora protejo quem eu mais odeio.
- `CF11_12` [CF09] ＝ **Cavaleiro:** Agora, o espelho. Meu reflexo é a Matriz Transposta: as linhas viram colunas. Um e dois em cima, três e quatro embaixo, no espelho vira um e três em cima, dois e quatro embaixo.
- `CF11_13` [CF16] ＝ **Cavaleiro:** O segredo é simples: a diagonal, do canto de cima à esquerda até o de baixo à direita, fica parada. Só os dois números de fora trocam de lugar: o de cima à direita vai para baixo à esquerda, e o de baixo à esquerda vai para cima à direita.
- `N11A_05` [N150] ＝ **Narrador:** Diante do espelho, a matriz:
- `CF11_14` [CF10] ＝ **Cavaleiro:** Qual é o reflexo dela no espelho, a transposta?
- `CF11_15` [CF11_igual] ＝ **Cavaleiro:** Não. Essa é a própria matriz. No reflexo, a primeira linha vira a primeira coluna.
- `CF11_16` [CF11_giro] ＝ **Cavaleiro:** Não. Aí você virou a matriz de cabeça para baixo. No reflexo, a primeira linha vira a primeira coluna.
- `CF11_17` [CF12] ＝ **Cavaleiro:** Isso. Só atravessa o espelho quem é igual ao próprio reflexo: a Matriz Simétrica. Para saber se é simétrica, escute só os dois números de fora da diagonal: o de cima à direita e o de baixo à esquerda. Se forem iguais, ela é simétrica.
- `CF11_18` [CF13] ＝ **Cavaleiro:** Qual destas atravessa o espelho?
- `CF11_19` [CF14_triangular] ＝ **Cavaleiro:** Não. Ela tem zero de um lado da diagonal e números do outro: o reflexo seria diferente.
- `CF11_20` [CF14_cheia] ＝ **Cavaleiro:** Não. Compare os números que trocam de lugar no espelho: eles são diferentes.
- `CF11_21` [CF15] ＝ **Cavaleiro:** Igual ao próprio reflexo. Pode passar, jovem mago.
- `CF11_22` 🆕 **Cavaleiro:** Um conselho de quem viu muitos magos passarem por aqui: no fim, não ataque o fogo do dragão. Leia o coração dele. E se você derrubar aquele dragão... talvez eu finalmente possa descansar.
- `N11A_06` [N113] ＝ **Narrador:** O espelho se apaga, e o corredor se abre até a porta do dragão.

---

## Cena 11B: O Golem de Pedra e o Puzzle das Pedras

*[som: o chão treme; pedras rangendo]*

- `N11B_01` [N115] ＝ **Narrador:** O chão treme. Pedras se juntam, rangendo, até formar uma voz:
- `GO11_01` [GO01] ＝ **Golem:** Eu sou o Golem. Eu sou pedra. Eu guardo este caminho.
- `GO11_02` 🆕 **Golem:** Os magos me fizeram. Para proteger o farol. Agora o fogo manda. Eu protejo o fogo. Eu não gosto do fogo.
- `G11B_01` 🆕 **Grilo:** Ele fala pouco, mas fala bonito.
- `GO11_03` [GO02] ＝ **Golem:** Mostro uma matriz: quatro e sete em cima, dois e nove embaixo. Diga o que sobra quando ela é subtraída dela mesma.
- `G11B_02` [G14] ＝ **Grilo:** Posição com posição, jovem mago. Quatro menos quatro...
- `GO11_04` [GO03] ＝ **Golem:** O que sobra?
- `GO11_05` [GO04] ＝ **Golem:** Zero. Tudo zero. Você entendeu a Matriz Nula.
- `G11B_03` [G15_igual] ＝ **Grilo:** Ops! Essa é a mesma matriz. Subtrair uma matriz dela mesma não deixa nada sobrando.
- `G11B_04` [G15_dobro] ＝ **Grilo:** Ops! Aí você somou a matriz com ela mesma. Subtrair é tirar: quatro menos quatro dá zero.
- `GO11_06` [GO05] ＝ **Golem:** Mas o caminho ainda não é seu. Atravesse o abismo. Em cada salto, eu digo qual matriz aguenta o seu peso. As outras afundam.
- `GO11_07` 🆕 **Golem:** Pedra pesa. Você pesa. Só a matriz certa aguenta.
- `G11B_05` [G16] ＝ **Grilo:** Em cada salto há três pedras: à esquerda, no meio e à direita. Escute o Golem e pule na pedra certa!

**3 saltos** (igual a hoje):
- `N11B_02` / `N11B_03` / `N11B_04` [N116_1/2/3] ＝ **Narrador:** Primeiro salto. / Segundo salto. / Último salto. O vento do abismo sobe forte.
- `GO11_08` / `GO11_09` / `GO11_10` [GO07_nula/identidade/diagonal] ＝ **Golem:** Pise na Matriz Nula. / Pise na Matriz Identidade. / Pise na Matriz Diagonal.
- `G11B_06` / `G11B_07` / `G11B_08` [G18_nula/identidade/diagonal] ＝ **Grilo:** as três dicas de hoje.
- `N11B_05` [N117] ＝ **Narrador:** Em qual pedra ela está?
- `N11B_06` [N118] ＝ **Narrador:** Você pula, e a pedra aguenta firme.
- `N11B_07` [N119] ＝ **Narrador:** A pedra afunda sob seus pés! Você se agarra na borda e volta.

- `GO11_11` [GO06] ＝ **Golem:** Você é digno. Passe.
- `GO11_12` 🆕 **Golem:** Os magos que me fizeram liam o coração das matrizes. Um número só. Fogo nenhum aguenta ouvir o próprio coração. Diga ao dragão... que a pedra lembra quem a fez.

*[som: pedras virando poeira]*

- `N11B_08` [N120] ＝ **Narrador:** O golem se desfaz em poeira, abrindo o caminho até a porta do dragão.

---

## Cena 12: O Dragão

*[som: uma respiração profunda e o chão tremendo]*

- `N12_01` [N121] ＝ **Narrador:** Os dois caminhos se encontram em uma porta enorme. Do outro lado, uma respiração profunda faz o chão tremer, e o ar esquenta.
- `DR12_01` [DR01] ＝ **Dragão:** Mais um mago... Eles sempre acham que são os primeiros.
- `DR12_02` 🆕 **Dragão:** Um de chapéu azul. Uma com um amuleto de cristal. Todos vieram pelo meu ouro, e todos chegaram atacando, sem parar para escutar o meu fogo. Todos viraram cinza. Por que você seria diferente?
- `G12_01` 🆕 **Grilo:** Diz que é porque você tem um grilo! ... Não? Tá. Eu fico quieto.
> **Golpe final novo: o determinante (o "coração" da matriz).** Antes, o último fogo se apagava com "a matriz menos ela mesma", que sempre dá a nula e não exige conta nenhuma. Agora o jogador calcula o **determinante** do fogo: multiplica a diagonal principal, multiplica a outra diagonal e subtrai. A resposta é **um número só**, o que é ótimo para quem joga ouvindo, e muda a cada partida, porque o fogo é sorteado.
> As opções erradas são os dois erros mais comuns: **somar** as diagonais em vez de subtrair, e fazer a conta **ao contrário** (a outra diagonal menos a principal).
> A **Matriz Nula** continua no jogo: os guardiões a ensinam, o Golem a cobra nas pedras e ela passa a poder aparecer como um dos fogos que o jogador classifica.

- `A12_01` [A28] ✏️ **Alquimista:** É ele! O fogo dele é feito de matrizes. A cada fogo, diga que tipo de matriz ele é, sempre o mais específico, e o fogo perde a força. Quando ele estiver fraco, vai cuspir o último fogo, o mais forte de todos. Esse você não classifica: você lê o coração dele. E quando ele atacar com as garras, escute de onde vem e pule para o outro lado.
- `A12_02` [A36] ＝ **Alquimista:** A receita para descobrir o tipo é escutar os dois números de fora da diagonal: o de cima à direita e o de baixo à esquerda.
- `A12_03` [A37] ＝ **Alquimista:** Se os dois forem zero, olhe a diagonal: se ela também for toda zero, é nula; se for um e um, é identidade; se for outra coisa, é diagonal. Se só o de baixo à esquerda for zero, é triangular superior. E se os dois forem iguais, mas não zero, é simétrica.
- `A12_04` 🆕 **Alquimista:** Agora, o ponto fraco. Toda matriz quadrada tem um coração: um único número, chamado determinante. É ele que segura o fogo inteiro. Diga o determinante certo, e o fogo se desfaz por dentro.
- `A12_05` 🆕 **Alquimista:** Num dois por dois, a conta é assim. Primeiro, multiplique os dois números da diagonal principal: o de cima à esquerda e o de baixo à direita. Depois, multiplique os dois números da outra diagonal: o de cima à direita e o de baixo à esquerda. Por último, faça o primeiro resultado menos o segundo.
- `A12_06` 🆕 **Alquimista:** Um exemplo: três e um em cima, dois e quatro embaixo. Diagonal principal: três vezes quatro, doze. Outra diagonal: um vezes dois, dois. Doze menos dois, dez. O determinante é dez.
- `A12_07` 🆕 **Alquimista:** E cuidado com os dois erros de sempre: somar as diagonais em vez de subtrair, e fazer a conta ao contrário. É sempre a diagonal principal menos a outra. Nessa ordem.
- `N12_02` [N71] ＝ **Narrador:** Aperte W se entendeu, ou S para ouvir a explicação de novo.

*[som: um sino grave]*
- `S11_determinante` 🆕 **Sistema:** Nova magia aprendida: Determinante. O coração da matriz.

**3 rodadas.** As duas primeiras são de classificar o fogo, como hoje, agora podendo incluir a nula. A terceira é o determinante. Antes da 2ª e da 3ª, o Dragão provoca (fala nova):
- `DR12_03` 🆕 **Dragão:** Sorte. Pura sorte de mago pequeno.
- `DR12_04` 🆕 **Dragão:** Chega! Vou queimar esta ilha inteira, e aquele farol velho junto!

Falas das rodadas de classificação (iguais a hoje):
- `N12_03` / `N12_04` [N122_1/2] ＝ **Narrador:** O dragão respira fundo e cospe a primeira matriz em chamas! / Furioso, o dragão cospe outra matriz em chamas!
- `N12_06` [N123] ＝ **Narrador:** A matriz em chamas:
- `N12_07` [N128] ＝ **Narrador:** Que tipo de matriz é esse fogo?
- `N12_08` [N129] ＝ **Narrador:** Acertou o tipo! O fogo perde a força, e o dragão recua.
- `A12_08` [A34] ＝ **Alquimista:** Não! Escute o que ele é:
- `N12_11` [N126] ＝ **Narrador:** As chamas te atingem!
- Esquiva das garras: reaproveita `N06_03/04/05` (o golpe vem da esquerda/direita/de frente).

Falas do golpe final (o determinante):
- `A12_09` [A35] ✏️ **Alquimista:** Ele está fraco! Lá vem o último fogo. Escute os quatro números e leia o coração dele!
- `N12_05` [N122_3] ✏️ **Narrador:** O dragão abre as asas e cospe a maior matriz de todas! No centro das chamas, alguma coisa pulsa, como um coração.
- `N12_06` [N123] ＝ **Narrador:** A matriz em chamas: *(lê os quatro números)*
- `N12_09` [N124] ✏️ **Narrador:** Qual é o determinante do fogo, o coração dele?
- *(as opções são lidas como números: "Opção A: dez. Opção W: catorze. Opção D: menos dez.")*

▶ **Acertou:**
- `N12_10` [N125] ✏️ **Narrador:** Você diz o número em voz alta. O coração do fogo para de pulsar, e as chamas se desfazem por dentro! O dragão ruge de dor.

▶ **Somou as diagonais:**
- `A12_10` [A29_dobro] ✏️ **Alquimista:** Não! Você somou as duas diagonais. No determinante, a outra diagonal é tirada da principal, não somada!

▶ **Fez ao contrário:**
- `A12_11` [A29_igual] ✏️ **Alquimista:** Não! Você fez a conta ao contrário. É a diagonal principal menos a outra, não a outra menos a principal. O sinal ficou trocado!

*(depois do erro:)* `N12_11` [N126] ＝ **Narrador:** As chamas te atingem! *(perde 1 vida; vem um fogo novo, sorteado)*

*[som: um rugido longo e um corpo enorme caindo]*

- `N12_12` [N127] ＝ **Narrador:** O tom do ar desce até quase o silêncio. O dragão ruge, vacila e cai, e a masmorra inteira para de tremer.
- `DR12_05` [DR02] ✏️ **Dragão:** Impossível... um mago... que escuta antes de atacar... e que lê o coração do fogo... Talvez... você seja mesmo... o primeiro.
- `V12_01` 🆕 **Ecos:** *(baixinho, se afastando)* Obrigado...

*[som: moedas de ouro tilintando]*

- `N12_13` [N134] ＝ **Narrador:** Atrás do dragão caído, um monte de moedas de ouro brilha no escuro. É o bastante para as ervas da sua mãe, e ainda sobra.
- `N12_14` 🆕 **Narrador:** Entre as moedas, você encontra um chapéu azul chamuscado e um amuleto de cristal rachado. Lembranças dos que vieram antes.
- `G12_02` 🆕 **Grilo:** Vamos levar isso pra casa. Alguém deve estar esperando por eles também.

---

## Epílogo: De volta para casa

- `N13_01` 🆕 **Narrador:** Na saída da masmorra, o sol está nascendo. Lá embaixo, na praia da ilha, o Bento já te espera, com o Andorinha remendado e uma vela velha amarrada no mastro.
- `MR13_01` 🆕 **Marinheiro:** Eu senti o farol tremer, e depois ficar quieto. Sabia que era você! Sobe, rapaz, que o mar hoje tá manso. Quinze anos... e finalmente eu volto pra casa.
- `MR13_02` 🆕 **Marinheiro:** E deixa o farol aceso. Ele agora brilha pelos que não voltaram.

*[som: ondas calmas e uma vela batendo no vento]*

- `N13_02` 🆕 **Narrador:** A viagem de volta é calma. Atrás de vocês, o farol gira, iluminando o mar como nos velhos tempos.
- `N13_03` [N130] ✏️ **Narrador:** Sem o dragão, o cheiro estranho vai embora, e as criaturas da floresta se acalmam. No caminho, uma voz aguda grita do alto de uma árvore:
- `GB13_01` 🆕 **Goblin:** Ei! O pedágio de volta é dobrado! ... Espera. Isso aí é ouro de dragão? Ahn... pode passar. De graça. Hoje é feriado. Boa viagem, senhor mago!

*[som: a taverna: murmúrios, canecas e lareira]*

- `N13_04` 🆕 **Narrador:** De volta à taverna Caneco Torto, todo mundo para de falar quando você entra.
- `T13_01` 🆕 **Taverneiro:** Voltou! E inteiro! Eu nunca duvidei. ... Tá bom, duvidei um pouquinho. Senta aí, que hoje o café é por conta da casa. Pra sempre.
- `N13_05` 🆕 **Narrador:** O Alquimista já está na mesa do canto, fingindo que nunca duvidou de você:
- `A13_01` [A30] ＝ **Alquimista:** Eu sabia que você conseguiria. Quer dizer... quase tinha certeza.
- `N13_06` 🆕 **Narrador:** Você coloca o chapéu azul e o amuleto de cristal em cima da mesa. O Alquimista para de sorrir.
- `A13_02` [A39] ✏️ **Alquimista:** Tá bom. Eu mandei outros antes de você. Com eles, eu tive pressa: ensinava a soma e mandava direto para o dragão. Nenhum chegou a aprender o determinante. Nenhum voltou, e todas as noites eu pensava neles. Com você, eu fiz diferente: ensinei no caminho, uma magia de cada vez, e deixei checkpoints. E você fez a sua parte: foi o primeiro que parou para escutar.
- `N13_07` [N131] ＝ **Narrador:** No balcão, Max acorda devagar:
- `MX13_01` [M02] ＝ **Max:** Quem... onde... o que eu perdi?
- `G13_01` [G17] ＝ **Grilo:** Só a maior aventura de matrizes da história, Max!
- `MX13_02` 🆕 **Max:** Dragão? Matriz? Eu falei! Eu falei ontem à noite, e ninguém me ouviu!
- `T13_02` 🆕 **Taverneiro:** Você falou "mais uma caneca" quarenta vezes, Max.

*[som: a porta da casa de cura se abrindo]*

- `N13_08` [N133] ＝ **Narrador:** Com o ouro do dragão, você corre até a casa de cura. O Druida conta as moedas, sorri e vai buscar as ervas raras. Com elas, sua mãe vai ficar boa.
- `N13_09` [N135] ✏️ **Narrador:** Na cama, ela abre os olhos e sorri. Você solta uma faísca pequena e controlada, que dança entre os seus dedos sem queimar nada. Ela lembra da cortina da cozinha e ri baixinho. O filho dela virou um mago de verdade.
- `N13_10` [N136] ＝ **Narrador:** Com Trim segura de novo, o Druida libera o Alquimista para sair do vilarejo.
- `A13_03` 🆕 **Alquimista:** Livre! Finalmente! Vou conhecer o mundo inteiro... depois do almoço. O Bartolo prometeu torta.
- `N13_11` [N132] ＝ **Narrador:** Fim de Mathrix Souls.

---

## 4. Resumo por dublador (quantas falas de história cada um grava)

Contagem só das falas desta proposta (fora menu, sistema e pedaços de leitura de matriz, que continuam com o Narrador ou com a voz do computador).

| Dublador | Personagens | Falas hoje | Falas na proposta | Novas |
|---|---|---|---|---|
| Felipe | Narrador | ~90 | ~110 | ~20 |
| Felipe | Grilo | 22 | 40 | 18 |
| Daniel | Alquimista | 33 | 42 | 9 |
| Daniel | Golem | 9 | 12 | 3 |
| Vinícius | Goblin | 6 | 13 | 7 |
| Vinícius | Max (proposta) | 2 | 3 | 1 |
| Vinícius | Ecos (proposta) | 2 | 4 | 2 |
| Matheus | Taverneiro | 0 | 11 | 11 |
| Matheus | Cavaleiro (proposta) | 19 | 22 | 3 |
| João | Marinheiro | 0 | 16 | 16 |
| João | Dragão (proposta) | 2 | 5 | 3 |

*(Contagens aproximadas; os números exatos saem do Apêndice depois que eu passar para o jogo.)*

## 5. O que muda no código quando for aprovado

Na matemática, só o **golpe final do Dragão**:
- **O que sai:** a conta "M − M = nula".
- **O que entra:** o **determinante** de uma matriz 2x2 sorteada, com números de 1 a 5, sem duas diagonais com produto igual (assim as três opções são sempre diferentes).
- **As opções:** a certa (`ad − bc`), a soma (`ad + bc`) e a invertida (`bc − ad`).
- **Leitura dos números:** as respostas vão de menos 24 a 50, então o jogo precisa ler números até cinquenta. Dá para montar com pedaços ("vinte", "trinta", "quarenta", "cinquenta" + "e" + a unidade), em vez de gravar cada número.
- **Classificação:** a nula entra na lista de fogos que o Dragão pode cuspir nas rodadas de classificação.
- **Documentação:** a "Revisão matemática" das notas da equipe e o README precisam ser atualizados.

Fora isso:
1. Renomear os códigos das falas (tabela de/para acima) e acrescentar as falas novas.
2. Personagens novos: **Taverneiro** e **Marinheiro**, com voz de computador própria enquanto não houver gravação. A "Voz misteriosa" vira **Ecos**.
3. Escolhas novas, todas sem perder vida: café da manhã (cena 2), perguntas ao Alquimista (cena 2), responder ao Marinheiro (cena 9) e a **charada da porta** (cena 9).
4. Provocações do Goblin antes de cada golpe, do Grilo entre os relâmpagos e do Dragão entre as rodadas.
5. A seleção de cenas (tecla C) e o salvamento continuam iguais.
