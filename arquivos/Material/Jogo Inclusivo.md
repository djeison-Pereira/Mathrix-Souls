**Mathrix Souls**  
Ideia principal do trabalho: Jogo RPG com ambientação dark-fantasy, utilizar matrizes como “golpes” e dar uma experiência diferente para pessoas com deficiência visual.  
A entrega será um executável Windows (.exe), para que a pessoa cega abra o jogo de forma independente pela acessibilidade do próprio sistema.

1 Narrador/Grilo \- Felipe   
2 Protagonista \- Usuário   
3 Goblin \- Vinícius   
4 Taverneiro \- Matheus Pletsch  
5 Marinheiro \- João Tormes  
6 Golem/Alquimista(Tessele) \- Daniel

**Ideia principal do jogo**

O protagonista será cego, e será guiado a partir de sons externos.  
O personagem começa em uma taverna desesperado para arrumar dinheiro para a mãe dele que está no hospital.  
Para virar um guerreiro, ele vai para uma masmorra em busca de ouro.   
O alquimista algébrico dá a ele certas instruções.  
Ele acha um companheiro (parecido com o grilo falante) que será seu companheiro.  
Ele precisa chegar até a ilha da masmorra.  
Teclas para esquivar de acordo com o som.  
3 pontos de vida.

Fases do jogo.

1 \- Taberna para a floresta.  
Encontra um goblin querendo roubar o seu ouro.  
Tutorial.

2 \- Praia, encontra o barco que será seu veículo para chegar até a ilha da masmorra.  
A fase será no mar, onde terá que usar as matrizes para nao afundar o barco

3 \- Farol.  
Fala com um marinheiro que naufragou a muito tempo ali.  
Terá que conversar com ele para entrar na masmorra que fica embaixo do farol

4 \- Masmorra, “esfinge” das charadas para entrar na masmorra  
   
5 \- Ele terá sempre dois caminhos para escolher

Lado esquerdo

Ponte 1 \- Cavaleiro fantasma ou armadura sem corpo, após derrotar terá 2 caminhos:

- \-  \> pode ser levado para uma armadilha ou para um banquete, que se for recusado, ganha um brinde que é a matriz nula

Lado direito 

Ponte 2 \- Golem gigante de pedra, após derrotar terá apenas 1 caminho, que será o puzzle das matrizes estilo squid game, terá que pular em cima das pedras certas senão irá cair.

Extras:

Os checkpoints serão onde as matrizes serão conhecidas e aprendidas pelo alquimista;  
Comandos por voz;  
Matriz nula será uma coringa.

### **1\. Requisitos do MVP (o que tem que funcionar)**

1. Jogo todo jogável **sem ver a tela**: menu, instruções, dano, vitória e derrota, tudo narrado.  
2. **Fase 1 (tutorial):** taverna, floresta e goblin. O alquimista ensina as teclas e as primeiras matrizes.  
3. **Combate por som:** o ataque vem da esquerda, do centro ou da direita (áudio estéreo), e o jogador esquiva com a seta do lado certo.  
4. **3 vidas**, e cada erro tira 1\.  
5. **Matrizes como golpes:** o alquimista lê a matriz, o jogador aperta o número da classificação e, se acertar, ataca.  
   * 1 \= identidade  
   * 2 \= diagonal  
   * 3 \= triangular superior  
   * 4 \= simétrica  
   * 5 \= nula  
6. **Justificativa em cada classificação**, falada pelo narrador (a professora pediu isso). Ex: “É diagonal porque todos os números fora da diagonal principal são zero.”  
7. **1 chefe:** o golem de pedra.  
8. **Puzzle das pedras** (estilo Squid Game): o jogador escuta as matrizes e pisa na pedra certa. Se errar, cai e perde vida.  
9. **Tecla R** para repetir a última fala e **tecla P** para pausar.  
10. **Final:** vitória (pegou o ouro) ou derrota (tentar de novo).

**Se sobrar tempo:** farol com o marinheiro, matriz nula como coringa, checkpoints.

**Fica de fora:** comandos por voz, fase do barco, esfinge, os dois caminhos (cavaleiro fantasma e banquete).

### **2\. O que precisamos fazer (tarefas)**

* Código da **classificação das matrizes** e das justificativas  
* Código de **áudio e teclas** (pygame, som estéreo, repetir e pausar)  
* Código da **fase 1** (tutorial e goblin)  
* Código do **chefe golem** e do **puzzle das pedras**  
* **Gravar** todas as falas  
* Achar e editar os **sons e efeitos**  
* **Testar** (de preferência com os olhos fechados) e **juntar tudo**  
* **Relatório e apresentação**

### **3\. Divisão dos 6 membros**

| Membro | Voz que grava | Parte técnica |
| ----- | ----- | ----- |
| **1** | Narrador (N01 a N13) | Relatório e apresentação |
| **2** | Alquimista (A01 a A11) | Classificação das matrizes e justificativas |
| **3** | Grilo (G01 a G04) | Áudio e teclas (pygame, estéreo, repetir e pausar) |
| **4** | Taverneiro e Goblin (T01, GB01, GB02) | Fase 1 (tutorial e combate com o goblin) |
| **5** | Golem e Personagem (GO01, GO02, P01) | Chefe golem e puzzle das pedras |
| **6** | Falas de sistema (S01 a S05) | Sons e efeitos, edição dos áudios, testes e integração Grilo Marinheiro  |

### **4\. Como o roteiro está dividido (cenas)**

| Cena | O que acontece | Falas |
| ----- | ----- | ----- |
| **0 \- Abertura** | Menu e instruções | N01, N02 |
| **1 \- Taverna** | Apresenta a história da mãe no hospital | N03 a N05, T01, P01 |
| **2 \- Floresta** | Tutorial, ensina identidade e diagonal, luta com o goblin | G01, G02, A01 a A04, N06, GB01, GB02 |
| **3 \- Travessia** | Barco até a ilha (curta) | N07 |
| **4 \- Masmorra** | Entrada, ensina triangular superior, simétrica e nula | N08, A05 a A07 |
| **5 \- Chefe** | Golem de pedra, com acertos e erros explicados | N09, GO01, GO02, A08, A09, G03 |
| **6 \- Puzzle** | Pedras com matrizes, 3 rodadas | N10, N11, A10, A11 |
| **7 \- Final** | Vitória ou derrota | N12, N13, G04 |
| **Sistema** | Vida perdida, pausa, acerto e erro | S01 a S05 |

### **5\. Linha do tempo (3 semanas)**

* **Semana 1:** fechar as matrizes e as falas, fazer a classificação, o áudio e as teclas, e gravar tudo.  
* **Semana 2:** fase 1, chefe golem, puzzle e integração.  
* **Semana 3:** testes, correção de bugs, relatório e apresentação. Nada novo entra nessa semana.

Se quiser, eu monto a **tabela de gravação** (código da fala, quem grava, texto e nome do arquivo) para vocês usarem como checklist.

**Possíveis melhorias**

\-Comandos por voz.