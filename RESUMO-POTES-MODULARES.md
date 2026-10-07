# Potes retangulares modulares em PP — resumo para retomar em outro chat

**Projeto 115 do ERP (Nitron) · Revisão 12 · 07/10/2026**
Branch: `claude/serene-johnson-ja8az8` · pasta `potes-modulares/`

Este arquivo é auto-contido: cole ele num chat novo e o contexto está todo aqui.

---

## 1. O pedido

Linha nova de potes retangulares em PP transparente, inspirada num render de referência
(potes com tampa de teca e tampa verde). Requisitos que o Ricardo deu, na ordem em que apareceram:

1. **Tampas.** Começou em três (teca com TPE · PE · PP dosadora), **na revisão 6 caiu para duas**
   (teca com chanfro + aro de TPE, e PE 100%) e **na revisão 9 voltou a três**: entrou a **tampa de
   correr, com bico aberto em U** (item 8 abaixo).
2. **Quatro litragens.** Começou em 500 ml / 1 L / 1,5 L / 2 L e **mudou para 600 / 1200 / 1800 /
   2400 ml** (pacote de mantimento).
3. **Modular:** empilhando os menores, tem que chegar exatamente na altura do maior.
4. **Parede reta**, não conada, com cantos arredondados.
5. **Sem trava**, acabamento liso.
6. Validar tudo contra o parque de injetoras real (via MCP Sankhya / Nitron).
7. **(revisão 12 — mini lombadas, e a de correr vira tampa de BICO)** Dois pedidos.
   **Lombadas:** os reforços de ponta chata viraram crista em MEIA-CANA de R0,34 (0,90
   na raiz, 2,40 de altura, 3°/face). Ponta chata segura vacuo e arrasta aresta viva no
   aco; meia-cana sai por rolamento. Custou rigidez (a crista tira area no alto, onde o
   braco e maior) e o PASSO recuperou: grade 7x4 em vez de 5x3 -> I 2,13x por 1,65 g,
   contra 2,2x por 1,29 g da ponta chata.
   **A tampa de CORRER SAIU.** "nao ficou legal... preciso de algo mais robusto... algo
   que nao vaze tmb e seja hermetico com o bico... essa versao nao precisa empilhar".
   Justo: ela tinha gaveta de 1,80 correndo em trilhos com 0,25 mm de folga por lado e
   um 2o aro vedando por compressao AXIAL - o que o projeto descartou na revisao 4.
   **Entra a TAMPA DE BICO.** A ideia que faltava: SEPARAR quem veda de quem escorre.
   - GARGALO: colar fechado de 24 x 46 subindo 7,50 mm do deck. O topo e ANEL PLANO -
     linha de vedacao plana, nao curva 3D. 983 mm2 de passagem na secao mais estreita.
   - CALHA: canal aberto em U saindo do gargalo por cima da aba ate um labio 9 mm alem
     da tampa, caindo 7,2°, labio de 0,50 virando 15° para baixo.
   - FECHO: plug conico de 1° num gargalo de 5°. Cones DIFERENTES de proposito: entra
     folgado 0,15/lado na boca, as retas se cruzam em 2,14 mm e aperta ate 0,18/lado no
     pe. O ponto de contato ANDA conforme desgasta ou flui. Dobradica viva atras.
   **NAO EMPILHA** (liberado pelo Ricardo) - e e isso que deixa o gargalo subir acima do
   plano modular e a calha passar por cima da aba.
   **A altura do colar nao e estilo:** a primeira tentativa (4,40) punha o piso da calha
   em +0,80 e o labio em +0,20, ABAIXO da aba de +1,20 - cortaria o apoio na borda e
   pingaria no pote. Foi a verificacao que pegou. Minimo 7,30; ficou 7,50.
   **Hermeticidade:** prometo que nao vaza deitado nem virado (PP contra PP conico sela
   liquido a pressao atmosferica). NAO prometo a classe da tampa principal, que e radial
   com silicone. Se o ensaio de agua colorida acusar, a resposta e um filete de silicone
   no plug - o QUARTO perfil extrudado da linha.
8. **(revisão 11 — tampa encorpada, farpa no aro, e os 3° de saída)** Três pedidos, e o
   terceiro conflita com um requisito antigo dele.
   **Nervuras sob o deck:** grade 5 × 3 (célula 33 × 34, nervura 0,80 na raiz / 0,49 na
   ponta / 3,00 de altura, **saída de 3° por face**). I da seção T sobe **2,2×**, flecha cai
   para 0,46, custo **1,29 g** (6% da tampa). Altura limitada pelo DEGRAU interno do pote
   (−7,00), não por moldagem.
   **Farpa na lingueta:** 0,25 mm por face, rampa de entrada de 36°, degrau de saída de 90°.
   Para o aro cair, o vão de 0,70 teria de abrir até 1,30 — antes eram 0,10 mm de aperto. O U
   ganhou **bolsa** de 1,40 × 0,95 que recebe a farpa: montado o silicone RELAXA, em vez de
   ficar esticado 0,50 para sempre (deformação permanente é o que mata vedante). É a segunda
   contra-saída da tampa; 5,2% de deformação de fibra na extração por arraste (PP escoa ~8%).
   **Os 3° de saída:** aplicados em toda FEIÇÃO (nervura, bolso, calha, trilho, rabo, farpa),
   onde não custam nada. **Na parede do pote, não.** A 3° o fundo do 2,4 L fica 24 mm mais
   estreito que a boca em 242 mm (16,1% de conicidade) — vira balde e o IML não cola. A saída
   NÃO precisa ser a mesma nos quatro (cada tamanho tem molde próprio, só a borda é comum):
   a 2° o 600 ml ainda dá 2,5%. Mas o 2,4 L, o mais fundo e difícil, é o que menos tolera.
   O que resolve extração sem saída já está no projeto: polimento A2, placa impulsora e
   válvula de ar. **Recomendação: manter 0,5° e levar a tabela à ferramentaria antes de
   fechar o molde — se 0,5° não sair, muda o produto, não só o molde.**
9. **(revisão 10 — a borda com DENTE e o aro em U)** O Ricardo mandou fotos de uma referência
   física (pote cinza, tampa canelada, um perfil de silicone em U na mão) e pediu: borda de
   **~8 mm** com um **dente em toda a volta na base dela** (é onde a trava engata); a borda
   **expandindo ~3 mm para fora**, e nessa expansão encaixa a parte interna da tampa; e a tampa
   entrando no corpo com um **vão na lateral** onde vai o silicone **extrudado em U**.
   **A borda OCA da revisão 8 saiu inteira** — saia livre, canal e flare. No lugar: parede reta
   até −8,00, um **web** horizontal de 1,00 mm atravessando para fora, e a parede da borda subindo
   dele até uma **meia-cana** de R0,60. Face de BAIXO do web = o **dente** (3,18 mm/lado); face de
   CIMA = **degrau interno**; entre o web e o topo, 7,00 mm de **boca**.
   **Perguntei uma coisa antes de cortar** (saia única × saia dupla, porque "a parte INTERNA da
   tampa" sugeria duas) e ele escolheu **saia única**: o U calça numa **lingueta** de 0,80 × 2,40
   recuada 0,20 em cada face, e a perna de fora comprime **0,35 mm/lado** contra a boca.
   **O que isso devolveu:** footprint 153,7 × 87,8 → **147,5 × 84,3**; peso do 600 ml 52,9 →
   **47,1 g** (−11%); área projetada 134 → **123 cm²**; aresta de engate 1,20 → **3,18 mm** (o
   gancho usa 25% dela em vez de 67%); e o molde **perde** a nervura de 1,20 × 8,6 mm (7,2:1) que
   a revisão 8 tinha somado — é a primeira revisão que tira trabalho do ferramental.
   **De brinde:** a placa de teca passou a **pousar no degrau**, e isso FIXA a espessura dela em
   5,00 mm (= borda 8 − web 1 − fundo 2). Ela caiu de 8,0 para 5,0 mm, de 59 para 37 g, e passou
   a comer 14% do pote de 600 em vez de 19%. O peso do pote de cima vai para o degrau através da
   madeira, em compressão: a placa não trabalha mais em flexão.
   **O que custou:** a borda deixou de ser caixão fechado e virou um **L** — menos rígida na boca
   — e encurtou de 16 para 10 mm, o que deixou o painel reto 6 mm mais alto. No 600 ml o painel
   ficou **1,61× mais flexível** que na revisão 8 (ainda mais rígido que na 7); do 1,8 L para cima
   melhorou. A pergunta do protótipo continua: a boca ovaliza o bastante para soltar o aro?
   **E a teca perdeu o vedante comum:** o U calça numa lingueta de 0,80 mm e em madeira ela
   quebra, então a placa ficou com corda redonda em friso usinado (10,2 kgf de atrito). Decisão
   aberta: aceitar dois perfis ou pôr um aro de PP carregando o U sob a placa.
10. **(revisão 9 — a terceira tampa, APOSENTADA na 12)** Pedido do Ricardo: *"uma tampa de correr com outro aro de
   TPE... colocar na tampa mesmo um bico mas não fechado e sim aberto tipo 'U' e não 'O' para poder
   escorrer o líquido"*. Base: a tampa de PP — mesmo plug, mesmo filete, as mesmas duas travas.
   **Mecanismo (escolha dele):** *gaveta na tampa* — painel que corre em trilhos num bolso no piso
   da bandeja e fecha a janela por baixo. É o único que não passa acima do plano modular nem aberto.
   **Cotas:** janela **22 × 46 mm** (1004 mm² de passagem) no lado curto · bico de **46 mm, a mesma
   largura da janela** · gaveta 30 × 60 × **1,80 mm**, curso **24 mm** · 2º aro Ø1,20 de TPE com
   0,35 mm de sobra (**2,7 kgf** para correr) · canal com piso em +1,20 e paredes até +4,00
   (2,80 mm úteis, aberto em cima) · lábio de corte de 0,40 na ponta.
   **Duas coisas que a conta decidiu contra a minha intuição:** (a) eu preferia o **canto**, e a
   posição foi medida — canto dá 626 mm² e 17,8 mm de travessia contra 1004 mm² e zero no lado
   curto; (b) eu tinha desenhado o **bico mais estreito que a janela e chamado isso de virtude** —
   o Ricardo corrigiu ("o bico precisa ocupar a mesma largura da janela, pra não vazar o produto"),
   e está certo: hoje `bico >= janela` é verificação automática.
   **O erro que quase passou:** a primeira rota do líquido **cortava o friso do filete** (começa em
   −3,00 na face do plug) — a tampa pareceria certa e não vedaria, mesmo de gaveta fechada. Rota
   nova em dois trechos: rampa de **18°** e vertedouro de **49°** com 3,20 mm. Virou teste.
   **O que ainda falta (CAD):** batentes de fim de curso da gaveta e puxador.
   **No gerador:** anéis passaram a poder vir como lista de **pontos livres** e `banda()` pula o
   quadrilátero de largura zero — é o que permite furo, entalhe e rampa. A tampa de correr é uma
   casca de **gênero 1**. São **dez** peças agora, todas a 0,00% do STL.
11. **(revisão 8 — a borda, a partir do STL de referência `REF_231.stl`)** O Ricardo mandou um STL
   com um pote e uma tampa em escala 1:10 (a parede medida, 0,113 mm, é o que fixa a escala) e
   pediu: **manter alturas, larguras, comprimentos e o raio de canto**, e refazer a **borda
   superior do corpo** e a **tampa de PP**, pegando dali o **layout de tampa e travas**.
   Medido na referência: borda de **17,3 mm** (31% do pote) saliente **9,6 mm/lado**, topo chato de
   4,3 mm com raios 2,5/1,9, e **duas travas** — uma por lado COMPRIDO — de **58% do comprimento**.
   **O que virou aqui:** borda **alta e OCA** de 12,0 mm + flare de 4,0 — a parede sobe, abre no
   flare, sobe pela perna de dentro (1,40 mm, faz a boca), vira o topo chato e desce por fora numa
   **saia livre** (1,20 mm) até 10 mm do topo, com um **canal** de 1,20 mm entre as duas. A face de
   baixo da saia, 1,20 mm, é a **aresta de engate**. Tampa de **PP** (era PEAD) com **2 travas de
   clipe** de 89 mm, gancho de 0,80 mm (67% de engate), 2,0 kgf para fechar e 1,2 kgf no dedo para
   abrir.
   **O erro da revisão 7 que isso revelou:** lá a boca (144,95) era mais larga que a face externa do
   corpo (141,55), então o colar era um anel de material **pairando sobre o corpo** — as duas
   seções não se encostavam. Malha estanque, normais certas, volume plausível, e a peça em dois
   pedaços; impresso, o colar sairia solto. Agora `gera-3d.py` tem `secao_conexa()` e um
   **autoteste** que roda o critério contra a geometria da revisão 7 e exige que ele reprove.
   **O que custou:** a borda oca precisa de 3,80 mm de largura contra 1,80 de uma parede só; o
   rebaixo vai de 3,50 para **5,60 mm** e, como o módulo fixa a seção interna, o footprint cresce:
   medida máxima **148,6 × 84,9 → 153,7 × 87,8 mm**, peso do 600 ml **47,0 → 52,9 g**, área
   projetada 125 → **134 cm²**. O corpo ficou com canto R4,4 (a borda continua R10).
   **Terceira correção de número publicado:** a revisão 7 dava 146 cm² de área projetada para os
   corpos — 146 é a silhueta do **deck da tampa**. O corpo tem 134.
   **O que NÃO piorou, contra a minha expectativa:** o aninhamento a vazio. A 0,5° a pilha de seis
   2,4 L continua em 1044 mm (−28%) — quem manda ali é a saída, não a borda.
12. **(revisão 7 — mudança de arquitetura, a partir de referência física)** Saem a **aba em U**, o
   **pé embutido** e a garra da tampa. Entram o **colar de borda** (liso, arredondado em cima,
   sobressaindo 3,50 mm/lado, cuja face de baixo é a aresta de engate), o **rodapé reto** para IML
   e **6 abas de trava** na tampa. As duas tampas passam a usar **o mesmo filete de TPE** (objetivo
   desde a revisão 4). A teca vira **placa maciça de 8 mm com friso** — e o ponto em aberto de como
   ela empilharia some, porque **o topo da placa é o plano modular**.
   **A conta que quase não fechou:** sem pé, quem desce na bandeja é o fundo reto do pote de cima,
   e ele tem de caber na boca. Precisa de 3,70 mm/lado, o colar paga 4,00 — **folga de 0,30 mm**.
   **O que custou:** medida máxima de 145,7 para 154,8 mm; área projetada 125 → 146 cm², e com isso
   o 600 ml **perde a classe de 160 t** e volta para 200 t. E apareceu um número novo: **a tampa
   come volume útil** — a teca leva 115 ml do pote de 600, 19% (decisão em aberto: rotular por
   borda ou re-resolver).
   **Três erros pegos por verificação, não por leitura:** filete 0,40 mm aquém da boca (não vedaria
   nada), metade das abas espelhada no visualizador (volume negativo cancelando as outras), e o STL
   saindo com Y para cima em vez de Z. Nenhum deles é acusado por volume assinado ou normais.
13. **(revisão 6)** A tampa PE **fecha por fora**: saia por fora da borda, garra engatando sob o
   lábio da aba em U. Princípio oposto ao plug da teca, na mesma borda, **sem mudar uma cota do
   pote** — o lábio já dava 3,04 mm/lado de ressalto e a garra usa 0,80. Resina **PEAD HA 7260
   IF 20 a R$ 9,34/kg** (a mais barata da casa depois do moído), tampa de 27,6 g a R$ 0,26.
   Vedação por **cordão axial de 0,35 mm** no deck, prensado pela pré-carga de 0,10 mm da garra —
   axial funciona aqui porque a garra é uma trava contínua a 3 mm do cordão, o que não existia na
   tampa plug. Fechamento de pó e aroma, **não hermético**.
   Dois pontos abertos: a retenção depende da rigidez do deck (o aro da saia dá 3 gf, então pede
   elemento finito ou protótipo), e a **tampa de teca não pode ser o plug de parede fina** — em
   maciço, precisa do poço da bandeja usinado ou não empilha.
14. **(estudo, 21/09/2026 — não implementado)** Pedido de referência à vedação da Tupperware.
   Mecanismo levantado: canal em U na tampa que engole um cordão da borda, apertando-o de
   **faces opostas** (US2487400, de 1949, expirada, "nonsnap"). O burp não dá para copiar — a
   tampa deles é membrana, a nossa é datum de empilhamento. Dois caminhos orçados (com e sem
   mexer no molde do corpo), 4,3 e 5,1 kgf de arranque. **Decisão: fica como estudo**, seção 13
   do README. A linha segue na revisão 6.
15. **(revisão 5)** O pote tinha ficado largo e muito arredondado em relação ao render de
   referência. Corrigido para **frente estreita e pote fundo, canto R10** — escolhido de propósito
   o caminho que mantém altura, módulo, curso de abertura e classe de injetora. Custou **+17,6 g**
   de resina nos quatro corpos e deixou a face comprida do 2,4 L **3,8× mais flexível** (única
   decisão ainda aberta: aceitar, pôr bombê de 1,0–1,5 mm, ou reduzir o ASP de 1,75 para ~1,55).

---

## 2. A linha, como está fechada

**Medida máxima 153,7 × 87,8 mm · corpo reto 142,5 × 76,6 mm (do flare ao fundo) · canto R10 na
borda (R4,4 no corpo) · saída 0,5°/lado · módulo 60 mm · fundo 2,0 mm igual nos quatro ·
SEM pé embutido: rodapé reto para IML · borda OCA de 12,0 mm + flare de 4,0, sobressaindo
5,60 mm/lado · boca 146,1 mm**

| Tamanho | Altura corpo | Passo | Parede | Peso corpo | Resina (PP a R$ 11,06/kg) |
|---|---|---|---|---|---|
| 600 ml | 62,0 mm | 60 | 1,15 mm | 52,9 g | R$ 0,59 |
| 1,2 L | 122,0 mm | 120 | 1,20 mm | 80,8 g | R$ 0,90 |
| 1,8 L | 182,0 mm | 180 | 1,30 mm | 113,8 g | R$ 1,27 |
| 2,4 L | 242,0 mm | 240 | 1,40 mm | 150,9 g | R$ 1,69 |

Empilhamento confere: `600×4` = `1,2 L×2` = `600+600+1,2 L` = `600+1,8 L` = `2,4 L` = 240 mm.

Mantimento: o **2,4 L recebe o pacote de 2 kg de arroz** e o **1,2 L o de 1 kg de feijão** — era o
motivo de trocar a escala (na escala antiga o 2 L levava só 1,70 kg de arroz).

### As três regras que fazem o passo fechar

1. Fundo de **2,0 mm igual nos quatro**.
2. **Piso da bandeja da tampa 2,0 mm abaixo do topo da borda** — igual à espessura do fundo. É o
   plano modular.
3. **O fundo reto do pote de cima desce dentro da bandeja** (o pé embutido saiu na revisão 7, por
   causa do IML). É essa conta que dimensiona o rebaixo, e na revisão 8 ela ficou mais cara: a
   borda oca custa 3,80 mm de largura contra 1,80 de uma parede só, então o rebaixo vai de 3,50
   para 5,60 e o footprint cresce.

### Por que parede reta ajudou

Com pote conado, bocal comum e passo constante, o volume cresce mais rápido que a altura e as
capacidades redondas só fechavam variando muito a saída. **Com parede reta o volume fica
proporcional à altura** e o conflito some; sobra um resíduo absorvido por uma elevação de fundo de
0 a 3,4 mm, invisível.

**Saída de 0,5°/lado** é o compromisso: no maior pote a base fica 4,0 mm mais estreita que o topo
(2,8%, imperceptível), e o pote vazio ainda aninha — 6 potes de 2,4 L em 1.044 mm contra 1.452
soltos (−28%), **o mesmo da revisão 7: a borda alta não estragou o aninhamento**. A 0,25° não
aninha mais e o frete do pote vazio sobe.

Exige polido A2 nas laterais (textura pediria saída extra), extração por **placa impulsora** e
**válvula de ar no macho**. Força de extração ~5 kN contra ~62 kN disponíveis numa 380 t: o gargalo
é curso e vácuo, não força.

---

## 3. As tampas — chegaram aqui depois de dois erros meus

### Onde eu errei (não repetir)

- **Revisão 2:** aro de TPE em canaleta de um lábio, comprimido contra a boca. Sem retenção (o aro
  sai na primeira abertura), com orçamento de largura ficcional (2,00 mm reservados para uma canaleta
  que precisa de 4,00) e **sem definir de onde viria a força de fechamento**.
- **Revisão 3:** troquei por lábio de PP moldado na tampa. Melhor, mas ainda **vedação axial**.
- **O erro comum às duas:** vedação axial num retângulo pede **32 kgf permanentes** ao longo dos
  413 mm de perímetro. É por isso que pote retangular hermético usa trava. Como o Ricardo não quer
  trava, axial estava morto desde o começo.

### A solução (dele, e está certa): vedação RADIAL

Um **plug** da tampa desce 8 mm dentro da boca e leva o filete de TPE num friso na face externa.
**O filete trabalha contra a PAREDE DA BOCA, não contra o topo da borda.** O mesmo filete serve as
duas tampas — na teca, num friso 2,0 mm mais fundo.

```
borda do corpo ... 147,5 x 84,3 (maxima)   corpo reto ..... 141,1 x 77,9
borda ............ 8,00 mm de altura ate o DENTE de 3,18 mm/lado
web .............. 1,00 mm: face de baixo = dente, face de cima = DEGRAU interno
boca do pote ..... 145,1 mm      face da saia ..... 144,2 mm (folga 0,45 por lado)
parede da saia ... 1,20 mm       lingueta ......... 0,80 x 2,40, recuada 0,20/face
aro em U ......... 2,80 x 3,10, perna 1,00 -> comprime 0,35 contra a parede
saia+aro descem .. 6,60 mm       vao do deck ...... 141,8, recebe o fundo de 140,16
tampa de PP ...... 149,7 x 89,5 mm com as 2 travas. 23,2 g. R$ 0,22 + aro 3,0 g
lombadas ......... grade 7x4 sob o deck, 0,90 x 2,40, crista R0,34, I +2,13x
farpa ............ 0,25/face na ponta da lingueta + bolsa de 1,40 x 0,95 no U
tampa de teca .... placa maciça 144,2 x 81,0 x 5,00 mm, 37 g, CNC, sem molde
                   POUSA no degrau; corda redonda 1,40 em friso, 10,2 kgf
tampa de bico .... a mesma de PP + gargalo 24 x 46 (sobe 7,50) e calha aberta.
                   24,2 g + fecho 2,7 g. Maxima 166,1 x 89,5 (o labio passa 9 mm)
                   NAO EMPILHA. Plug conico 1° no gargalo 5°: 0,18 mm/lado no pe
```

| | O que segura | Força |
|---|---|---|
| Axial (errado) | força permanente de fechamento | 34 kgf o tempo todo → precisa de trava |
| **Radial (certo)** | interferência lateral de 0,20 mm | **zero em repouso · 7,4 kgf para arrancar reto** |

Abrir descascando um canto: **1,2 kgf**.

Ganho extra: **vedação radial tolera a borda flexionar** — o filete acompanha a parede em vez de
perder contato, que é o que mata aro axial.

O plug faz três coisas: **veda**, **forma a parede da bandeja** onde o pote de cima apoia, e
**centra a tampa**.

### A borda oca, e as duas travas (revisão 8)

A borda deixou de ser um colar maciço e virou um **caixão oco de 3,80 × 12,0 mm**: parede sobe,
flare de 4 mm, perna de dentro (1,40, faz a boca), topo chato, e uma **saia livre** de 1,20 mm
descendo por fora até 10 mm do topo, com um canal de 1,20 entre as duas. **A face de baixo da saia,
1,20 mm, é a aresta de engate** — e como a saia é livre, ela é material de verdade, que era
exatamente o que faltava no colar da revisão 7.

Na tampa, **duas travas de clipe** de 89 mm (58% do comprimento), uma por lado COMPRIDO — layout da
referência. Gancho de 0,80 mm (67% de engate), braço de 10 mm: **2,0 kgf para fechar**, 1,2 kgf no
dedo para abrir, deformação de fibra de 1,20% contra os ~8% em que o PP escoa.

**Quem veda é o filete; quem segura é a trava** — e a trava é bloqueio geométrico, não força
elástica. É essa a diferença para a teca, que só tem o atrito.

### Aberto, para o tryout

- **Retenção do filete:** friso de 0,60 mm sai por arranque (rampas, sem gaveta). Testar 500
  aberturas e ver se o filete migra.
- **Ar preso:** 3,8 kgf a mais no 600 ml, 0,9 no 2,4 L. Alivia com o chanfro de entrada da boca.
  É o mesmo "pop" que a OXO vende como característica.
- **A nervura do canal no molde:** 1,20 × 8,6 mm (7,2:1), contínua nos 466 mm de perímetro. Feição
  nova, a orçar com a ferramentaria.
- **Extração das travas:** contra-saída de 0,80 mm em aba livre nos três lados. Arraste com a aba
  flexionando — dentro do usual em tampa de clipe, mas é item de ferramentaria.
- **A dobradiça sobre-centro** não está modelada: o cálculo trata como viga engastada.
- **Os lados curtos não têm trava.** Se o protótipo mostrar a tampa abrindo nos cantos, a resposta
  é uma terceira trava ou o bombê na face comprida.
- **Estanqueidade de cabeça para baixo:** plausível, **não prometida**. Medir com água colorida,
  24 h, deitado e invertido.

---

## 4. Material — as três famílias de PP

| Família | Comporta-se | Grades em casa | Compra 12 m |
|---|---|---|---|
| Homopolímero | rígido e transparente, quebradiço no frio | H 105 (926 t), H 103 (473 t) | R$ 11,06 · R$ 9,90 |
| **Randômico** | transparente, brilhante, tolerante | **RP 141 (299 t)**, RP 340 S (49,5 t) | **R$ 9,54** · R$ 17,00 |
| Heterofásico | impacto altíssimo, porém opaco | CP 141 (109 t) | R$ 10,52 |

- **Corpo: PP H 105** com clarificante (grade que a casa compra em volume).
- **Tampa: PP RP 141 randômico.** Transparente, aceita dobradiça viva (heterofásico não aceita — a
  fase de borracha impede a orientação molecular), e é o mais barato dos três.
- **Tampa PE foi descartada:** PEBD é compra residual (500 kg/12 meses), flui a frio (o plug relaxa e
  a interferência some) e daria material misto na reciclagem.
- **TPE Karinprene 45** (CODPROD 997) está cadastrado mas **sem compra há 4 anos** — recotar.
  Não há bi-injeção no parque: o aro é peça montada.

---

## 5. Bico da tampa de líquidos — a bandeja é o vertedor

Sem copinho, sem pump, nada acima do plano modular. Aproveita a bandeja que a modularidade já obriga:

1. Furo de vazão no canto (≈25 × 15 mm), encostado na parede da bandeja.
2. Entalhe de 12-15 mm na parede da bandeja — o canto R10 já faz a curva, não se molda bico.
3. **Lábio de corte de 0,4 mm** na aresta: quebra o filme, a gota se solta em vez de escorrer.
4. Piso com caimento de 2-3° para o furo: o que respinga volta para dentro pelo mesmo furo.
5. Aba com dobradiça viva rente ao piso — não veda (quem veda é o aro), só barra poeira e cheiro.

Zero peça adicional, sem gaveta no molde. Descartados: pump comprada (a casa já compra a válvula
CODPROD 10085 do porta-detergente 545/553, mas passa do plano modular) e copinho dosador.

---

## 6. Injetoras — o que o ERP mostrou

Parque: **46 injetoras** (45 monitoradas). 80 t ×1 · 120 t ×7 · 150 t ×2 · 160 t ×9 · 200 t ×12 ·
250 t ×9 · 280 t ×1 · 300 t ×1 · 380 t ×3 · 600 t ×1.
A tonelagem real está em `TPRCAP.DESCRICAO` (via `TPRWCP.CODCAP`) — **não** em `QTDCAPACIDADEPAD`,
que mistura kN e ton.

Os quatro corpos têm a **mesma área projetada (134 cm²)**: quem decide a máquina é profundidade,
não tonelagem. (Duas correções de número publicado: a revisão 4 dizia 139 cm², que não saía do
cálculo; a revisão 7 dizia 146, que é a silhueta do **deck da tampa**, não do corpo.)

| Tamanho | Máquina | Fecham. 2 cav | Curso | Molde | Peça equivalente que já roda lá |
|---|---|---|---|---|---|
| 600 ml | 200 t — INJ 1–6, 19–22, 35, 37 | 124 t | 136 mm | 252 mm | pote 176-C, ciclo medido 16,7 s |
| 1,2 L | 200 t — INJ 1–6, 19–22, 35, 37 | 133 t | 268 mm | 312 mm | modular 450 ml (320-C) na INJ 37 |
| 1,8 L | 250 t — INJ 23–28, 38, 39 | 142 t | 400 mm | 372 mm | modular 1,2 L (322-C) na INJ 25 |
| 2,4 L | 380 t — INJ 31, 32, 33 | 147 t | 532 mm | 432 mm | modular 2,4 L (323-C) na INJ 33 · pote 5,8 L (237-C) na INJ 31/33 |

O 600 ml **não cabe mais na classe de 160 t** que a revisão 6 tinha conquistado: a 124 t ele usaria
78% dela, acima do limite prático da casa.

**Sem máquina nova.** A peça mais funda desta linha é menos exigente que o pote de 5,8 L que já roda
nas 380 t. A **INJ 32 estava parada** — candidata ao try-out.

**Bloqueio de dado:** `AD_INJETORAFICHA` tem 1 registro e os 29 campos de especificação nulos. Curso
de abertura, curso e força de extração não têm conferência documental. Preencher antes de liberar o
molde do 2,4 L.

**Aproveitamento:** 2,4 L com 2 cavidades usa 39% do fechamento de uma 380 t. Avaliar 4 cavidades
(~294 t, molde ~640 × 510 mm).

**Capacidade** (2 cav, 20 h/dia, 22 dias): 186 / 151 / 127 / 109 mil pç/mês. O 2,4 L é o gargalo do
kit. **L/t de 224 no 2,4 L** está no limite: pede câmara quente com 2 pontos de injeção ou parede de
1,5 mm. Definir no Moldflow.

---

## 7. O que já existe no ERP (reaproveitar, não recriar)

| Achado | Onde |
|---|---|
| **Projeto 115 "Conjunto Potes Modular"** — status Aprovado, produto já modelado | `AD_PROJETOS` |
| Molde 115/1 — **orçamento aprovado de USD 47.100**, 2 cav, 75 dias, MR Plastic Mould, 04/2021 | `AD_MOLDE`, `AD_ORCAMENTO` |
| Linha modular quadrada em catálogo: 319-C a 323-C (250 ml a 2,4 L) | `TGFPRO` |
| **Tampa única já validada:** ref. 321-T serve 800 ml, 1,2 L e 2,4 L | `TGFPRO` |
| O 2,4 L é o que gira: 35 mil un/ano só no cliente Natura (ref. 323) | `TGFITE`/`TGFCAB` |
| Kit modular 6 pçs: 19.078 kits / R$ 449 mil em 12 meses (ref. 353) | `TGFITE`/`TGFCAB` |
| Tampa de madeira já é produto corrente com **FSC 100%** (NEO-COC-191022) | `TGFPRO` |
| Cadeia própria de teca: tora, ripa serrada (CODPROD 6759), planta WOOD (CNC, moldureira), Teak Brazil | `TPRPLP`, `TGFPRO` |

**Ferramental:** 4 moldes de corpo + 1 de tampa de PP + 1 de filete de TPE = **6 ferramentas**.
Feição nova na revisão 8: a **nervura do canal** nos quatro moldes de corpo (1,20 × 8,6 mm,
contínua). A teca usa programa de CNC. Benchmarks dos próprios orçamentos com a MR Plastic Mould
(USD): corpo lixeira 12 L/380 t = 36.900 · 284-U/280 t = 20.100 · 214-U/250 t = 18.900 ·
corpo 026/120 t = 6.300 · tampa 026-T/90 t = 5.500. **Ordem de grandeza USD 140–190 mil**, com a
cotação de USD 47.100 já aprovada como ponto de partida.

---

## 8. Arquivos

Branch `claude/serene-johnson-ja8az8`, pasta `potes-modulares/`:

| Arquivo | O que é |
|---|---|
| `README.md` | estudo completo, 14 seções, com o histórico das revisões e os erros registrados |
| `calculo-modular.py` | memória de cálculo: geometria, encaixe, forças de vedação, capacidade, aninhamento |
| `gera-3d.py` | gerador paramétrico → 7 STL + `perfis.json`; importa as cotas de `calculo-modular.py` |
| `verifica-malha.js` | roda o construtor do visualizador fora do navegador e compara com o STL |
| `stl/` | 7 peças em mm, escala real, prontas para imprimir protótipo |
| `visualizador-3d.html`, `ficha-tecnica.html` | cópias das páginas publicadas |

Artifacts publicados:
- Ficha técnica: https://claude.ai/artifact/GnEGBNxhsvXeSJNsZvpfwn
- Modelo 3D interativo: https://claude.ai/artifact/CTZYnTjY2hZYiye2SaHJz6

**A malha se confere sozinha** a cada geração: volume assinado positivo e normais consistentes nas
7 peças, **seção conexa em toda a altura** nos 4 corpos, cavidade dentro de 0,07% da nominal, e o
visualizador batendo com o STL em 0,00%. A checagem de seção conexa vem com **autoteste**: ela roda
contra a geometria da revisão 7 e tem de reprovar — verificação que nunca disparou não prova nada.
É malha, não sólido CAD — **o molde precisa do CAD paramétrico do projetista**.

---

## 9. Próximos passos

1. **Aprovar o footprint de 153,7 × 87,8 mm** (era 148,6 × 84,9). É o preço da borda oca, e tudo
   depende disso.
2. **Orçar a nervura do canal** (1,20 × 8,6 mm, contínua) com a ferramentaria.
3. Confirmar a saída de 0,5° com o design (é o que separa "reto" de "aninha no frete").
4. Preencher `AD_INJETORAFICHA` das 46 injetoras (curso de abertura, curso e força de extração).
5. Reabrir o Projeto 115 e recotar com a MR Plastic Mould a partir da cotação aprovada.
6. Recotar o TPE Karinprene 45 — parado há 4 anos, agora com volume das duas tampas.
7. Protótipo impresso do 600 ml + tampa: testar o clipe das duas travas e a retenção do filete.
8. Moldflow do 2,4 L (L/t 224) e estudo de extração da peça reta com a nervura do canal.
9. Ensaio de vedação: água colorida, 24 h, deitado e invertido. Só depois disso se fala em promessa
   de vedação na embalagem.
10. Reservar INJ 32 (380 t) para o try-out do 2,4 L.
11. Decidir o rótulo: capacidade de borda (como está) ou re-resolver para capacidade útil.
12. Decidir se a **tampa de correr** vira ferramenta agora ou depois do try-out das outras duas —
    é molde novo, mais a gaveta e o 2º aro.
13. **Cotar o perfil em U de silicone** (2,80 × 3,10 mm) com o extrusor e pedir amostra antes do
    try-out: é ele que decide a vedação e não há como imprimi-lo em FDM.
14. Decidir se a **teca fica com corda redonda** (dois perfis na linha) ou ganha um aro de PP
    carregando o mesmo U.

---

## 10. Contexto técnico do ambiente

Os dados saíram do **Sankhya via MCP Nitron** (somente leitura). Tabelas usadas: `TPRWCP` + `TPRCAP`
(parque e tonelagem) · `TPRWCP.AD_CICLOATUAL/AD_DHCICLO` (ciclo ao vivo) · `TPRAPA`→`TPRAPO`→`TPRIATV`
(que peça roda em qual máquina) · `AD_FICHATECNICA` (ciclos de referência) ·
`AD_PROJETOS`/`AD_MOLDE`/`AD_ORCAMENTO` · `TGFITE`/`TGFCAB` (preço real de resina e vendas) · `TGFPRO`.

Armadilha conhecida: o Sankhya cancela chamadas paralelas na mesma sessão HTTP — serializar as
consultas.
