# Linha Potes Retangulares Modulares em PP

**Status:** estudo de viabilidade técnica · **Revisão 6** · 21/09/2026
**Origem:** evolução do Projeto 115 do ERP ("Conjunto Potes Modular") · **Planta:** Nitron – Fábrica (CODPLP 1)

Linha retangular em PP transparente, **parede reta com cantos arredondados**, quatro litragens
(**600 ml · 1,2 L · 1,8 L · 2,4 L**), três tampas e modularidade de empilhamento — qualquer
combinação empilhada chega à altura do maior.

Todos os números de máquina, matéria-prima, custo e ferramental saíram do Sankhya, não de
estimativa de catálogo. Fontes citadas em cada seção.

> **Revisão 6 — o que mudou:** a linha passa de três tampas para **duas** — teca com chanfro e
> aro de TPE, e **PE 100%**. A tampa PE deixa de ser um plug e passa a **fechar por fora**: uma saia
> desce por fora da borda e uma garra engata sob o lábio da aba em U. Como a aba já existia desde a
> revisão 3 para enrijecer a boca, **o pote não mudou uma cota sequer** — o lábio já dava 3,04 mm/lado
> de ressalto e a garra só precisa de 0,80.
>
> Isso me obriga a corrigir o julgamento das revisões 2 a 5: eu recomendava PP contra PE, mas
> aquilo era **contra um PE em forma de plug**, e nessa forma continuava certo. Como sobretampa sem
> aro, três dos quatro argumentos caem (seção 6.0). Fica de pé o mais sério: PE é compra residual.
>
> Resina recomendada: **PEAD HA 7260 IF 20 a R$ 9,34/kg** — grau de injeção declarado e mais barato
> que o próprio PP RP 141. Tampa de 27,6 g a R$ 0,26.
>
> Dois pontos ficaram abertos e estão registrados: a rigidez do deck contra rotação da saia, que
> pede elemento finito ou protótipo (6.1.5), e a **tampa de teca, que não pode ser o plug de parede
> fina desenhado para injeção** e precisa do poço da bandeja usinado, senão não empilha (6.2).
>
> **Revisão 5 — o que mudou:** o desenho voltou para a proporção da referência conceitual. O pote
> estava **largo e muito arredondado** (121,2 × 93,2 com canto R18); agora é **frente estreita e
> pote fundo** (139,7 × 79,8) com **canto R10**. Altura, módulo, passo, curso de abertura e altura
> de molde não mudam — foi escolhido de propósito o caminho que não mexe na injetora.
>
> Três coisas vieram junto, duas delas correções de erro meu:
>
> 1. **A área projetada era 125 cm², não 139.** O número da revisão 4 não saía do cálculo. Com
>    125 cm² o 600 ml usa 72% de uma injetora de 160 t e **volta para a classe de 160 t** em vez de
>    disputar as 200 t com o 1,2 L (seção 4.1).
> 2. **O pé embutido estava fixo no código em 112,4 mm** e foi o único número que quebrou com a
>    troca de footprint — virou um degrau de 13 mm. Ele nunca foi uma escolha: sai da bandeja da
>    tampa, que sai da boca. Agora é derivado (`pe_l()` em `calculo-modular.py`).
> 3. **Custa 17,6 g de resina e rigidez na face comprida** — a única conta em que a revisão 5 é
>    pior que a 4. Está medida na seção 3.3, e é a decisão que sobrou em aberto.
>
> **Revisão 4:** a vedação passa a ser **radial**, do jeito certo: a tampa tem um
> *plug* que desce dentro do pote e leva o aro de TPE numa canaleta, trabalhando contra a **parede**.
> Sem trava e sem saia externa — a tampa fica lisa. Some a força permanente de fechamento; o que
> resta é 1,0 kgf para abrir descascando um canto. Pé de 113,0 para 112,4 mm.
>
> **Revisão 3:** refez a vedação da revisão 2 (que não fechava) com um lábio de PP moldado na tampa,
> e acrescentou a **aba em U** na borda, que dá rigidez ao lado reto. O lábio foi substituído pelo
> plug na revisão 4; a aba ficou.
>
> **Revisão 2:** escala migrou de 500/1000/1500/2000 para 600/1200/1800/2400 ml (pacote de
> mantimento); parede deixou de ser conada e passou a reta com R18 de canto.

---

## 1. Veredito

| Requisito | Situação |
|---|---|
| Modularidade de empilhamento | **Viável** — passo único de 60 mm |
| Litragens 600 / 1200 / 1800 / 2400 ml | **Viável e exatas** — a parede reta elimina o conflito com o passo |
| Parede reta com cantos arredondados | **Viável** com 0,5°/lado e R10 — custa aninhamento no frete (seção 3.2) |
| Tampa única para os 4 tamanhos | **Viável** — já é prática da casa (ref. 321-T serve três alturas) |
| Vedação da tampa de teca | **Refeita na revisão 4**: plug com aro de TPE radial contra a parede, sem trava (seção 5) |
| Vedação da tampa PE | **Cordão axial + garra** sob o lábio da aba — fecha por fora, sem aro (seção 6.1) |
| Retenção da garra num retângulo | **Decisão aberta**: o aro da saia dá 3 gf; quem segura é o deck (seção 6.1.5) |
| Tampa de teca empilhar | **Ponto em aberto**: precisa do poço da bandeja usinado no maciço (seção 6.2) |
| Tampa PE 100%, fechando por fora | **Viável** — PEAD HA 7260, 27,6 g, R$ 0,26 (seção 6.1) |
| Injeção dos 4 corpos no parque atual | **Cabe no que já temos**, sem máquina nova |
| Confirmação documental de curso/extração | **Bloqueio de dado**: ficha das injetoras vazia (seção 4.4) |
| Rigidez da face comprida com R10 | **Decisão aberta**: face do 2,4 L ficou 3,8× mais flexível (seção 3.3) |

---

## 2. O que já existe na casa

| Achado | Fonte |
|---|---|
| **Projeto 115 – "Conjunto Potes Modular"**, status Aprovado, produto já modelado | `AD_PROJETOS` |
| Molde 115/1 "potes modulares" — orçamento **aprovado de USD 47.100**, 2 cavidades, 75 dias, MR Plastic Mould | `AD_MOLDE`, `AD_ORCAMENTO` |
| Linha modular quadrada em catálogo: 319-C a 323-C (250 ml a 2,4 L) | `TGFPRO` |
| **Tampa única já validada**: ref. 321-T serve 800 ml, 1,2 L e 2,4 L | `TGFPRO` |
| O 2,4 L é o tamanho que gira: 35 mil un/ano só no cliente Natura (ref. 323) | `TGFITE`/`TGFCAB` |
| Kit modular vende: 19.078 kits / R$ 449 mil em 12 meses (ref. 353) | `TGFITE`/`TGFCAB` |
| Tampa de madeira já é produto corrente com **FSC 100%** (NEO-COC-191022) | `TGFPRO` |

**Recomendação:** reabrir o Projeto 115 — o orçamento aprovado é a base de renegociação do ferramental.

---

## 3. Geometria

**Corpo 139,7 × 79,8 mm** · **145,7 × 85,8 mm na aba da borda** · canto **R10** · saída **0,5°/lado** · módulo **60 mm**
Fundo de **2,0 mm igual nos quatro** · parede da borda **1,40 mm igual nos quatro** · pé embutido de **130,9 × 71,0 mm igual nos quatro** (medida derivada, não escolhida)

| Tamanho | Altura corpo | Passo | Bocal interno | Base externa | Degrau do pé | Elev. fundo | Parede | Volume | Peso |
|---|---|---|---|---|---|---|---|---|---|
| 600 ml | 62,0 mm | 60 mm | 137,4 × 77,5 | 138,6 | 3,88 mm | 2,0 mm | 1,15 mm | 600 ml | 45,4 g |
| 1,2 L | 122,0 mm | 120 mm | 137,3 × 77,4 | 137,6 | 3,35 mm | 3,5 mm | 1,20 mm | 1200 ml | 73,0 g |
| 1,8 L | 182,0 mm | 180 mm | 137,1 × 77,2 | 136,5 | 2,83 mm | 2,8 mm | 1,30 mm | 1800 ml | 105,8 g |
| 2,4 L | 242,0 mm | 240 mm | 136,9 × 77,0 | 135,5 | 2,31 mm | 0,0 mm | 1,40 mm | 2400 ml | 142,5 g |

Empilhamento conferido — todas as combinações dão 240 mm:
`600×4` · `1,2 L×2` · `600+600+1,2 L` · `600+1,8 L` · `2,4 L`.

### 3.1 Por que a parede reta ajuda

Na revisão 1 (pote conado, 1,2° a 2,1°) havia um conflito estrutural: com bocal comum e passo
constante, a parede inclinada faz o volume crescer mais rápido que a altura, e as capacidades
redondas só fechavam variando muito a saída entre os tamanhos.

**Com parede reta o volume fica praticamente proporcional à altura** e o conflito some. Sobra um
resíduo pequeno (a seção ainda cresce 0,5° por lado até o bocal), absorvido por uma **elevação de
fundo de 0 a 3,5 mm** — invisível por fora, sem efeito no empilhamento e sem custo de ferramenta.

### 3.2 O encaixe: três regras que fazem o passo fechar exato

Esta é a parte que não pode ser negociada no design, porque é ela que sustenta a modularidade:

1. **Fundo de 2,0 mm, igual nos quatro potes.**
2. **A tampa é uma bandeja cujo piso fica 2,0 mm abaixo da borda do pote** — recuado para dentro da
   boca, não apoiado em cima dela. Esse piso é o plano modular: é nele que o pote de cima se apoia.
3. **Os últimos 6 mm da base recuam para um pé embutido de 130,9 × 71,0 mm**, medida igual nos
   quatro (o degrau varia de 2,3 a 3,9 mm para compensar a saída). Esse pé desce dentro da bandeja
   da tampa de baixo.

Com as três juntas: passo = 60n exato, capacidade = 600n exata, e **uma tampa só serve os quatro**.
Sem a terceira, o pote de cima não caberia dentro da bandeja — a boca do pote tem 118,9 mm e o corpo
tem 139,7 mm. O pé embutido é o que resolve, e de quebra os potes ficam **travados entre si** quando
empilhados, em vez de só apoiados.

**Orçamento de largura — é o que dimensiona o pé.** Entre a face externa do corpo e a face externa
do pé sobram 4,1 mm por lado, e tudo tem que caber ali:

| | por lado |
|---|---|
| parede na faixa da borda | 1,40 mm |
| folga entre o plug e a parede (onde o aro trabalha) | 1,00 mm |
| parede do plug | 1,50 mm |
| folga de encaixe do pé | 0,50 mm |
| **soma** | **4,40 mm** |

É esse orçamento que fixa o pé em 130,9 mm. Na revisão 2 havia um aro de TPE dentro dessa conta,
com 2,00 mm reservados para uma canaleta que precisa de 4,00 — era o número errado, e o pé de
110,0 mm saiu dele. Tirando o aro da tampa de PP, a conta fecha e o pé cresce.

**Caminho de carga:** pé do pote de cima → piso da bandeja → parede do plug → borda do pote →
parede do pote. O aro de TPE fica na canaleta do plug, mais abaixo, vedando radialmente contra a
parede — fora do caminho de carga, para não ser comprimido pelo peso da pilha.

### 3.3 O preço do canto R10: a face comprida

Reduzir o raio e afinar a frente ao mesmo tempo tem efeitos opostos, e não se cancelam igual nas
duas faces. O painel plano é o trecho de parede entre os dois cantos:

| | R18 de 121,2 × 93,2 | R10 de 139,7 × 79,8 |
|---|---|---|
| Painel plano da face **curta** | 57,2 mm | **59,8 mm** |
| Painel plano da face **comprida** | 85,2 mm | **119,7 mm** |

A face curta praticamente não mudou — afinar a frente devolveu o que o raio menor tirou. A face
comprida é que paga: 119,7 mm de parede plana sem nada que a segure no meio.

Flecha relativa (placa engastada nas quatro bordas, mesma carga, `flecha ~ α·b⁴/t³`, `b` = menor
vão do painel; 1,00 = a mesma face no desenho R18):

| Tamanho | Face comprida | Face curta | Parede que igualaria a face comprida |
|---|---|---|---|
| 600 ml | 1,21× | 1,10× | 1,23 mm (hoje 1,15) |
| 1,2 L | 2,38× | 1,19× | 1,60 mm (hoje 1,20) |
| 1,8 L | 3,35× | 1,20× | 1,94 mm (hoje 1,30) |
| **2,4 L** | **3,81×** | 1,20× | 2,19 mm (hoje 1,40) |

No 600 ml não é problema: a face comprida tem 119,7 × 60 mm, e quem manda na flecha é o vão menor,
que é a altura — a mesma de antes. O problema aparece à medida que o pote sobe, porque aí o vão
menor passa a ser a largura de 119,7 mm. No 2,4 L a face comprida fica **3,8× mais flexível**.

**Igualar com parede está fora de questão:** 2,19 mm no 2,4 L é +56% de resina. As saídas reais são
três, e nenhuma é minha para escolher:

1. **Aceitar.** Pote de mantimento é pego pelas faces curtas, que não mudaram. A vedação é radial e
   mora no bocal, que é a parte mais rígida da peça (aba em U de 3,0 mm com lábio de 3,5 mm). O que
   precisa ser testado no protótipo é se a face comprida cede o bastante para **ovalizar o bocal** e
   soltar o aro — é o único caminho por onde essa flexão vira defeito funcional.
2. **Bombê de 1,0 a 1,5 mm na face comprida.** Lê como reta a olho nu e transforma o painel num arco
   raso, que é como todo pote de linha resolve isso. Não é parede conada — a saída de extração
   continua 0,5°, o molde continua de extração simples, sem gaveta. É a opção que eu levaria.
3. **Voltar o ASP de 1,75 para ~1,55.** A face comprida cai para ~105 mm e a flecha do 2,4 L para
   ~2,3×, ao custo de uma frente 5 mm mais larga.

O número honesto sobre esses 3,8×: a razão é confiável, porque só a geometria mudou entre as duas
colunas. A **flecha absoluta** não é — depende de carga de aperto e de engastamento real, e pedia
elemento finito ou protótipo. Nenhuma das duas revisões foi prototipada.

### 3.4 Quanto de saída é "reto"

Saída zero não extrai: a peça agarra o macho. O que se faz é a saída mínima de extração.

| Saída/lado | Base mais estreita que o topo | Aninhamento de 6 potes de 2,4 L |
|---|---|---|
| 0,25° | 2,1 mm (1,5%) | 1.452 mm — **não aninha** |
| **0,50°** | **4,2 mm (3,0%)** | **1.044 mm (−28%)** |
| 0,75° | 6,3 mm (4,5%) | 777 mm (−47%) |
| 1,00° | 8,4 mm (6,0%) | 643 mm (−56%) |

**Recomendação: 0,5°/lado.** No maior pote a base fica 4,2 mm mais estreita que o topo em 139,7 mm de
largura — 3,0%, imperceptível com canto R10 e parede polida. Abaixo disso a peça deixa de aninhar a
vazio e o frete do pote vazio sobe ~28%.

Condições para a parede reta funcionar na extração:
- **acabamento polido** (SPI A2 ou melhor) nas laterais — textura exige saída extra (~1° a cada
  0,025 mm de profundidade de textura) e mataria o "reto";
- **extração por placa impulsora** (não por pinos), com **válvula de ar no topo do macho** para
  quebrar o vácuo;
- força de extração estimada em ~5 kN no 2,4 L (932 cm² de contato) contra ~62 kN disponíveis numa
  injetora de 380 t — **força não é o problema; curso de extração e vácuo são**;
- o canto R10 ainda é aliado, mas menos que o R18: reduz o arrasto nos cantos, que é onde a peça reta costuma marcar.

## 4. Validação nas injetoras

### 4.1 O que cada tamanho exige

| Tamanho | Área proj. | Fecham. 2 cav | Curso abert. mín. | Altura de molde | Injeção 2 cav | L/t |
|---|---|---|---|---|---|---|
| 600 ml | 125 cm² | 115 t | 136 mm | ~252 mm | 115 cm³ | 115 |
| 1,2 L | 125 cm² | 124 t | 268 mm | ~312 mm | 186 cm³ | 160 |
| 1,8 L | 125 cm² | 132 t | 400 mm | ~372 mm | 269 cm³ | 194 |
| 2,4 L | 125 cm² | 137 t | 532 mm | ~432 mm | 362 cm³ | 223 |

A área projetada é a silhueta da aba da borda: 145,7 × 85,8 mm = **125 cm²**. A revisão 4 trazia
139 cm² e 129–153 t; esse número não saía do cálculo e foi corrigido aqui. A diferença muda
alocação: o 600 ml a **115 t numa injetora de 160 t usa 72%** do fechamento, abaixo do limite
prático de 80% — **volta para a classe de 160 t** em vez de disputar as 200 t com o 1,2 L. São
9 máquinas de 160 t no parque contra 12 de 200 t, e libera hora das 200 t para o 1,2 L.

Os quatro têm a **mesma área projetada**: quem decide a máquina não é tonelagem, é profundidade.

### 4.2 Alocação — e a evidência de que o parque aguenta

| Tamanho | Máquina | Peça equivalente rodando hoje |
|---|---|---|
| 600 ml | 200 t — INJ 1–6, 19–22, 35, 37 | pote hermético peq. 176-C (ciclo medido 16,7 s) |
| 1,2 L | 200 t — INJ 1–6, 19–22, 35, 37 | modular 450 ml (320-C) na INJ 37; 2 L rosca (238-C) na INJ 1/22 |
| 1,8 L | 250 t — INJ 23–28, 38, 39 | modular 1,2 L (322-C) na INJ 25; pote 3 L (239-C) na INJ 24/27 |
| 2,4 L | 380 t — INJ 31, 32, 33 | modular 2,4 L (323-C) na INJ 33; pote alto 5,8 L (237-C) na INJ 31/33 |

Parque (`TPRWCP` + `TPRCAP`): 46 injetoras — 80 t ×1, 120 t ×7, 150 t ×2, 160 t ×9, 200 t ×12,
250 t ×9, 280 t ×1, 300 t ×1, 380 t ×3, 600 t ×1.

**Sem ciclo recente em 16/09/2026 12:11** (`TPRWCP.AD_DHCICLO`): INJ 30 (300 t), INJ 41 (160 t) e
**INJ 32 (380 t, parada desde 15/09)** — candidata natural ao try-out do 2,4 L.

### 4.3 Aproveitamento de máquina

O 2,4 L com 2 cavidades usa 139 t numa máquina de 380 t (37% do fechamento). Com **4 cavidades**
(~278 t, molde ~620 × 500 mm, cabe entre as colunas de uma 380 t) dobra a produção na mesma hora
de máquina. Mesma avaliação para o 1,8 L numa 250 t.

### 4.4 Bloqueio de dado

`AD_INJETORAFICHA` tem **1 registro com os 29 campos de especificação nulos**. Com parede reta o
dado que faltava ficou mais crítico, porque a extração passa a ser o ponto de projeto. Preencher
para as 46 injetoras antes de liberar o molde: `CURSOABERT`, `CURSOEXTR`, `FORCAEXTR`,
`ALTMINMOLDE`, `ALTMAXMOLDE`, `COLUNASH`, `COLUNASV`, `CAPINJECAO`, `FORCAFECH`.

---

## 5. A vedação — tampa plug com aro radial

Duas revisões erradas antes de chegar aqui, e vale registrar as duas.

**Revisão 2** especificava um aro de TPE comprimido contra a boca, sem dizer como ele ficaria preso
nem de onde viria a força. **Revisão 3** trocou por um lábio de PP moldado na tampa. Ambas partiam
do mesmo engano: tratar a vedação como **axial** — aro ou lábio esmagado entre a tampa e a borda.
Vedação axial num retângulo sem trava não funciona, e o número é implacável: 32 kgf de força
permanente ao longo dos 413 mm de perímetro.

**A vedação certa é radial.** Uma saia da tampa — o *plug* — desce dentro do pote e leva o aro de
TPE numa canaleta na sua face externa. **O aro trabalha contra a parede do pote, não contra a
borda.** Não existe força permanente de fechamento: quem segura é a interferência lateral. Por isso
dispensa trava, e por isso a tampa pode ser lisa por fora.

### 5.1 Por que a objeção da revisão 3 não se aplica

| | O que segura | Força |
|---|---|---|
| Aro **axial**, esmagado entre tampa e borda | força permanente de fechamento | **32 kgf o tempo todo** — precisa de trava |
| Aro **radial**, na parede | interferência lateral | **zero** em repouso; só atrito ao enfiar e tirar |

Com o aro comprimindo 0,20 mm contra a parede:

| Compressão | Arrancar reto | Descascando um canto |
|---|---|---|
| 0,15 mm | 3,8 kgf | 0,6 kgf |
| **0,20 mm** | **6,1 kgf** | **1,0 kgf** |
| 0,30 mm | 10,6 kgf | 1,8 kgf |
| 0,40 mm | 16,4 kgf | 2,7 kgf |

Ninguém puxa a tampa reta: levanta um canto e ela descasca, com ~1/6 do perímetro trabalhando por
vez. **1,0 kgf para abrir** é tampa de pote, não alicate.

Há um ganho de tabela que eu não tinha visto: **vedação radial tolera a borda flexionar.** Se o lado
reto abre um pouco, o aro acompanha o movimento da parede em vez de perder contato — que é
exatamente o que mata um aro axial. A aba em U continua valendo, agora para limitar a flexão a menos
que a compressão de 0,20 mm, não para segurar a tampa.

### 5.2 Cotas

```
boca do pote ......... 136,9 mm (parede de 1,40 mm nos quatro tamanhos)
face do plug ......... 134,9 mm — folga de 1,00 mm por lado
parede do plug ....... 1,50 mm
canaleta ............. 0,60 mm de profundidade, entre 5,0 e 7,4 mm abaixo da borda
aro de TPE ........... seção 2,4 × 1,8 mm, sobra 1,20 mm da face do plug
                       -> 0,20 mm de compressão contra a parede
plug desce ........... 12 mm dentro do pote
vão da bandeja ....... 131,9 mm, recebe o pé de 130,9 mm
```

O plug faz três coisas de uma vez: **veda**, **forma a parede da bandeja** onde o pote de cima
apoia, e **centra a tampa**. Por fora não há saia nenhuma — a tampa fica rente à aba da borda.

### 5.3 O que ainda precisa de atenção

**Retenção do aro.** A canaleta tem 0,60 mm de profundidade — 0,5% da largura da peça. Um plug de
parede fina sai disso **por arranque** (stripping), com rampas de 30° nos dois ombros, sem gaveta no
molde. O aro é montado depois, esticado sobre o plug; a própria tensão do aro mais os dois ombros o
seguram contra o atrito da parede. **Confirmar no primeiro tryout** — é o ponto que mais merece
teste de vida (abrir e fechar 500 vezes e ver se o aro migra).

**Ar preso.** O aro só encosta nos últimos 2 mm do curso, mas isso ainda comprime o ar de dentro:

| | Δp | Força a mais |
|---|---|---|
| 600 ml | 3,5 kPa | 3,8 kgf |
| 1,2 L | 1,8 kPa | 1,9 kgf |
| 2,4 L | 0,9 kPa | 0,9 kgf |

No 600 ml dá para sentir. Reduz-se com **chanfro de 30° × 1,5 mm na boca**, que atrasa o contato do
aro. E é o mesmo "pop" que a OXO transformou em argumento de venda — pode virar característica em
vez de defeito.

**Aba de alavanca.** Sem saia externa, é preciso um ponto para levantar: uma aba de ~18 mm numa das
laterais curtas, com rebaixo correspondente na aba da borda para ficar rente ao perfil. É o que
mantém o "liso" e ainda permite descascar.

**Montagem.** O aro volta a ser peça montada — não existe bi-injeção no parque. 1,8 g de TPE mais
alguns segundos de montagem por tampa. O lado bom: o **mesmo aro serve as três tampas** (padrão,
dosadora e teca), então o molde do aro amortiza em toda a linha. Esse argumento, que eu tinha
derrubado na revisão 3, volta a valer.

### 5.4 O que entrega

**Entrega:** vedação contra umidade, poeira e cheiro, e resistência a tombo com o pote deitado.
Vedação radial com aro é o mesmo princípio de um O-ring — segura pressão, não só poeira.

**Não entrega sem teste:** estanqueidade garantida de cabeça para baixo com líquido. Com 0,20 mm de
compressão e a borda enrijecida é **plausível**, mas isso se mede no protótipo, não se promete na
planilha. Primeiro tryout com água colorida, pote deitado e de cabeça para baixo, 24 h.

### 5.5 Orçamento de altura

```
borda do pote ................... 62,0 mm   (600 ml)
piso da bandeja da tampa ........ 60,0 mm   = PLANO MODULAR, 2,0 mm abaixo da borda
vão livre da bandeja ............ 131,9 × 72,0 mm  (recebe o pé de 130,9 × 71,0)
plug .......................... desce até 12 mm abaixo da borda, dentro do pote
```

O pé do pote de cima tem que pousar no piso **junto à parede da bandeja** — que agora é a parede do
plug. A carga desce plug → borda → parede do pote.

## 6. As duas tampas

A linha passou de **três tampas para duas**: **teca com chanfro + aro de TPE** e **PE 100%**. A
tampa PP dosadora sai do escopo, e com ela o bico vertedor (registrado em 6.4, parado).

O que muda de verdade não é o número: é que **a tampa PE agora fecha por FORA**. As duas tampas
passam a usar princípios opostos na mesma borda — a teca é um *plug* que desce por dentro e veda
radialmente contra a parede; a PE é uma *sobretampa* que desce por fora e engata sob o lábio da aba.

### 6.0 Onde eu estava errado sobre o PE

As revisões 2 a 5 recomendavam PP contra PE. **Aquele julgamento era sobre um PE em forma de plug**,
e nessa forma ele estava certo: um plug de PE relaxa e larga o aro de TPE que deveria manter
comprimido. Como **sobretampa sem aro**, três dos quatro argumentos caem:

| Argumento contra o PE (rev. 4) | Vale para a sobretampa? |
|---|---|
| "o plug de PE relaxa e perde a interferência de 0,20 mm" | **Não** — não há plug nem aro. Quem segura é uma garra que é **trava geométrica**, não força elástica: mesmo relaxado, o PE não passa de volta pelo lábio. |
| "PEBD flui a frio e cede sob o pote carregado" | **Reduzido** — a carga do pote de cima entra pela repisa e desce direto na borda do pote de baixo, 2,5 mm de caminho. A tensão de contato fica em ~12 kPa, três ordens de grandeza abaixo do que faz PE fluir. E o PEAD tem 5× o módulo do PEBD. |
| "material misto atrapalha a reciclagem" | **Continua valendo.** Pote PP + tampa PE é mistura. Contra: a tampa de teca já é material misto de qualquer jeito. |
| "PE é compra residual e viraria contrato novo" | **Continua valendo, e é o item mais sério** — ver 6.1.5. |

O que **não** muda: a sobretampa não é hermética. É fechamento de **pó e aroma**, para grão e
farofa. Não prometer estanqueidade de líquido com o pote deitado.

### 6.1 Tampa PE — fecha por fora

#### 6.1.1 A borda já tinha o ressalto

A aba em U foi desenhada na revisão 3 para enrijecer a boca reta. O lábio descendente dela, de 1,20
mm de espessura, cria sem querer **3,04 mm por lado de ressalto** sobre o corpo, com a face inferior
em z = −5,10 (z = 0 no plano da borda). É exatamente o degrau de que uma sobretampa precisa. **Não
foi preciso mudar nada no pote** — nem uma cota, nem o molde do corpo.

#### 6.1.2 Cotas

```
lábio da aba (pote) ...... 145,7 mm, face inferior em z = −5,10
saia, face interna ....... 146,2 mm   folga de 0,25 mm/lado sobre o lábio
saia, face externa ....... 148,8 mm   parede 1,30 mm
garra, face interna ...... 144,1 mm   avança 1,05 -> ENGATE de 0,80 mm/lado
topo da garra ............ z = −5,00  0,10 mm de PRÉ-CARGA: puxa o deck contra a borda
aba de pega .............. 151,8 mm   1,5 mm/lado no pé da saia, em z = −5,80 a −7,00
cordão de vedação ........ 0,35 mm de altura, em 139,4 mm, na face inferior do deck
bandeja .................. vão 131,9 mm (o MESMO da tampa plug) recebe o pé de 130,9
repisa ................... z = +3,80, apoia o anel do degrau do pote de cima
altura total ............. 10,80 mm | footprint 151,8 × 91,9 mm | 27,6 g em PEAD
```

#### 6.1.3 O que veda, e por que aqui um cordão axial funciona

Um **cordão de 0,35 mm** na face inferior do deck, apertado contra o topo da borda pela pré-carga
da garra. É vedação **axial** — exatamente o que a seção 5 descartou para a tampa plug. A diferença
é decisiva:

- na tampa plug **não há trava**, então a força de fechamento teria de vir do próprio material ao
  longo de 413 mm de perímetro: 32 kgf permanentes. Inviável;
- aqui **a garra é a trava**, e ela é um aro contínuo a 3 mm do cordão. O deck não precisa ficar
  plano para o cordão vedar — ele é prensado localmente entre a garra (que puxa para baixo em
  146 mm) e o topo da borda (que empurra para cima em 139 mm). Funciona como tampa de garrafa.

O cordão conforma na primeira fechada, que é como toda tampa de PE se acomoda.

#### 6.1.4 O empilhamento continua exato — e ganha um apoio

O piso da bandeja fica em **z = −2,00**, igual ao da tampa plug: o passo segue sendo 60n exato.

A novidade é a **repisa em z = +3,80**. Com o pé assentado no piso, o anel do degrau do pote de
cima chega em z = +4,00 — ou seja, a repisa fica **0,20 mm abaixo dele, de propósito**. Se fosse o
contrário, o anel tocaria primeiro e o passo viraria 60n + 0,20. Assim o pé continua sendo quem
define o passo, e a repisa entra só como **batente**, assim que o piso fletir 0,20 mm. É a resposta
para a ressalva da seção 5.1 ("o pé apoia num anel de 1,15 mm de largura"): agora, sob carga, o
apoio passa a ser um anel de 2,5 mm de largura descarregando direto na borda do pote de baixo.

#### 6.1.5 Os três números que decidem a resina

**A garra sai por arraste, sem gaveta.** O perímetro da garra (435,6 mm) tem de abrir até o da saia
(442,2 mm) para sair do macho: **1,51% de deformação de aro**. PE arrasta 5–8%. Folgado —
placa impulsora, molde de duas placas.

**O engate muda com a temperatura, e é aí que o PEAD ganha.** PE dilata mais que PP, então o engate
afrouxa no quente:

| | −40 °C | 20 °C | +40 °C |
|---|---|---|---|
| **PEAD** (α ≈ 150 µm/m·K) | 0,95 mm | **0,80 mm** | **0,65 mm** |
| PEBD (α ≈ 200 µm/m·K) | 1,09 mm | 0,80 mm | 0,51 mm |

**O aro da saia não segura nada.** Abrir o painel reto da face comprida (120 mm) os 0,80 mm do
engate custa **3 gf em PEAD e 1 gf em PEBD** — nada. Num pote redondo a saia seguraria por tração
de aro; num retângulo de 120 mm de lado reto, não segura. **Quem segura é o deck**: para a saia
abrir, o deck tem de sair da borda, e ele está apoiado nela numa faixa contínua de 4,4 mm.

Esse é o ponto que **não dá para fechar no papel**. A rigidez do deck contra rotação da saia pede
elemento finito ou protótipo. O protótipo já está fatiado (`fatiamento/saida/5_tampa_pe_r020.gcode`),
com a ressalva de que PETG é muito mais rígido que PE: serve para conferir encaixe e cotas, **não**
a força de abrir.

#### 6.1.6 Resina: PEAD HA 7260, não PEBD

| | PEBD PB 608 | **PEAD HA 7260 / HDM520 IF 20** |
|---|---|---|
| Preço (compra 24 m) | R$ 11,10/kg | **R$ 9,34/kg** |
| Comprado em 12 m | 0,5 t | 1,1 t |
| Grau de injeção | não declarado no cadastro | **IF 20 declarado** |
| Módulo | ~200 MPa | ~1000 MPa |
| Engate a +40 °C | 0,51 mm | **0,65 mm** |
| Custo da tampa (27,6 g) | R$ 0,31 | **R$ 0,26** |

**Vai PEAD HA 7260.** É grau de injeção declarado, é **a resina mais barata da casa depois do
moído** — mais barata que o próprio PP RP 141 (R$ 9,55) — e o módulo maior é aliado tanto no
empilhamento quanto na retenção da garra.

**O risco do PEAD é empeno.** Contração de 2–4% contra 1,5–3% do PEBD, num deck plano de
148 × 89 mm. Deck plano grande em PEAD empena se o resfriamento for desigual. Mitigação de projeto:
a repisa e o degrau já quebram o painel em dois anéis, o que ajuda. Mitigação de processo:
refrigeração equilibrada nas duas metades e não tirar quente. **Confirmar no primeiro try-out.**

**A compra é o item aberto de verdade.** Hoje entram 1,1 t/ano de PEAD, em compras avulsas. Uma
linha a 200 mil tampas/ano pede **5,5 t/ano** — cinco vezes o volume atual, e vira contrato.
E há uma lacuna de dado: `AD_FICHATECNICA` tem **14 registros com `CODMP` nulo em todos**, então o
ERP **não consegue dizer se a casa já injetou PE**. Mesma natureza do bloqueio da seção 4.4.

### 6.2 Tampa de teca — e um ponto em aberto

Cadeia própria: teca em tora e ripa serrada (CODPROD 6759), planta **WOOD** (CNC RXK2513,
moldureira, lixadeiras, prensa de alta frequência) e a **Teak Brazil**. Tampa de madeira já é
produto corrente com FSC 100%. Sem molde — programa de CNC e gabarito. Usa o aro de TPE em
canaleta usinada, com chanfro na aresta de cima.

**O ponto em aberto:** o perfil do plug em `stl/tampa.stl` foi desenhado para **injeção** — saia de
1,50 mm de parede descendo 12 mm. Isso não se faz em madeira: em teca, uma parede de 1,5 mm com 12 mm
de altura lasca. A tampa de teca tem de ser um **plug maciço**, e aí duas coisas mudam:

1. o bloco maciço precisa do **poço da bandeja usinado** (131,9 × 72,0 × 2,0 mm de profundidade),
   senão **a tampa de teca não empilha** — e empilhar é o produto;
2. madeira maciça de 130 mm de largura trabalha com a umidade no sentido transversal. A canaleta do
   aro tem de ser dimensionada com essa movimentação, ou a compressão de 0,20 mm some no inverno.

Isso não estava no estudo e não é detalhe de acabamento: decide se a linha empilha com as duas
tampas ou só com a PE.


Cadeia própria: teca em tora e ripa serrada (CODPROD 6759), planta **WOOD** (CNC RXK2513,
moldureira, lixadeiras, prensa de alta frequência) e a empresa **Teak Brazil**. Tampa de madeira já
é produto corrente com FSC 100%. Sem molde — programa de CNC e gabarito. Usa o mesmo aro de TPE,
alojado em canaleta usinada.

### 6.3 Qual PP na tampa — as três famílias — PARADO

> Não há mais tampa em PP na linha. Fica registrado porque a correção sobre as famílias de PP > (heterofásico é opaco e não aceita dobradiça viva) vale para qualquer peça futura.

"Copolímero" não é uma coisa só, e a diferença muda a tampa. As três famílias que a casa já compra:

| Família | O que é | Comporta-se | Grades em casa | Preço (compra 12 m) |
|---|---|---|---|---|
| **Homopolímero** | só propeno | o mais rígido e o mais transparente com clarificante, mas **quebradiço no frio** | H 105 (925,9 t), H 103 (473,4 t) | R$ 11,06 / R$ 9,90 |
| **Copolímero randômico** | 2–6% de eteno espalhado na cadeia, atrapalhando a cristalização | **transparente e brilhante**, menos rígido, bem menos quebradiço | **RP 141 (299,1 t)**, RP 340 S (49,5 t) | **R$ 9,54** / R$ 17,00 |
| **Copolímero heterofásico (de impacto)** | tem uma fase de borracha dispersa dentro | **impacto altíssimo, inclusive a frio**, mas **opaco/leitoso** | CP 141 (108,9 t) | R$ 10,52 |

**Correção da revisão anterior:** a recomendação genérica de "CP 141 copolímero" para a tampa estava
imprecisa. O certo é **PP RP 141 randômico**, por três motivos:

1. **Transparência.** O CP 141 é heterofásico — sai leitoso. Se a tampa for transparente como o corpo,
   heterofásico não serve.
2. **Dobradiça viva.** A aba do bico dosador precisa de dobradiça viva, e dobradiça viva **não funciona
   em copolímero heterofásico**: a fase de borracha impede a orientação molecular que dá vida à
   dobradiça. Homopolímero e randômico funcionam; randômico é o mais tolerante.
3. **Preço e escala.** R$ 9,54/kg com 299 t/ano já comprados — é o mais barato dos três e o de maior
   volume depois do H 105.

O heterofásico continua fazendo sentido **se a tampa for colorida e sem dobradiça** (a versão de teca,
por exemplo, não tem aba nenhuma). Para a linha toda, RP 141.

Tampa em RP 141: 24,5 g → **R$ 0,23**.

### 6.4 O bico da tampa de líquidos — PARADO

> A tampa dosadora saiu do escopo quando a linha passou a ter duas tampas. O estudo fica > registrado porque o conceito não depende dela: se voltar uma terceira tampa, é daqui que parte.

Requisito: prático, que não suje, sem copinho dosador e sem peça cara. E ainda tem que respeitar o
plano modular — nada pode passar acima dele, senão o pote de cima não assenta.

**Conceito recomendado: a bandeja é o vertedor.** A modularidade já obriga a tampa a ter uma bandeja
rebaixada de 2,0 mm. Ela é reaproveitada como bacia anti-gota, sem peça nova:

1. **Um furo de vazão no canto** da bandeja (≈ 25 × 15 mm), encostado na parede.
2. **Um entalhe de 12 a 15 mm na parede da bandeja**, no mesmo canto, por onde o líquido sai quando o
   pote inclina. O canto R10 já faz a curva do vertedor — não precisa moldar bico nenhum.
3. **Lábio de corte de 0,4 mm** na aresta externa do entalhe: quebra o filme de líquido e faz a gota
   se soltar em vez de escorrer pela face do pote. É o detalhe que resolve o "não vai sujar".
4. **Piso da bandeja com caimento de 2 a 3° para o furo.** O que respinga ou volta cai na bandeja e
   escorre de volta para dentro do pote pelo mesmo furo. Nada fica na parte de fora.
5. **Aba com dobradiça viva** fechando o furo, rente ao piso. Ela não veda — quem veda é o aro do
   plug. A aba só barra poeira e cheiro, e abre com o polegar.

Por que é barato: **zero peça adicional**, zero componente comprado, tudo na mesma ferramenta da tampa,
e sem gaveta no molde — o furo, o entalhe e a aba saem todos no sentido de abertura.

Por que empilha: a aba fecha rente ao piso da bandeja, que é o plano modular. O entalhe tira um pedaço
da parede da bandeja num canto, onde o pote de cima tem raio e quase não apoia.

**Alternativas consideradas:**

- **Bico moldado dentro do poço** — mais "desenhado", mas precisa de poço mais fundo, encarece a
  ferramenta e não resolve melhor a gota que o lábio de corte.
- **Pump comprada** — a casa já compra a válvula pump (CODPROD 10085) para o porta-detergente 545/553.
  Faz sentido para a versão de pia, de uso com uma mão só, mas a pump passa muito do plano modular:
  vira SKU "topo da pilha", não versão modular. E é peça comprada, contra zero peça da bandeja-vertedor.
- **Copinho dosador** (o do porta-sabão em pó ref. 008) — descartado a pedido.

### 6.5 Vedação tipo Tupperware — estudo, não implementado

Pedido de referência: "a vedação do pote da Tupperware é incrível, queria algo similar".
O mecanismo foi levantado e orçado na **seção 13**. Decisão de 21/09/2026: **fica como estudo**,
a linha segue com a tampa PE da revisão 6 como está.

### 6.6 Processo do aro de TPE
**Não há bi-injeção no parque**: o aro é peça injetada à parte e montada, ou comprada pronta. Peso
2,6 g, seção 2,8 × 2,2 mm, perímetro 383 mm. Recotar o Karinprene 45 (dureza 45 shore), sem compra
desde 2022.

---

## 7. Matéria-prima e custo de material

Preços reais de compra dos últimos 12 meses (`TGFITE`/`TGFCAB`):

| Material | Preço médio | Volume 12 m | Uso |
|---|---|---|---|
| PP H 105 homopolímero com clarificante | **R$ 11,06/kg** | 925,9 t | corpo transparente |
| PP RP 340 S randômico fluidez 45 | R$ 17,00/kg | 49,5 t | alternativa de fluidez para o 2,4 L |
| PP RP 141 randômico fluidez 40 | **R$ 9,54/kg** | 299,1 t | **tampas** |
| PP CP 141 copolímero heterofásico | R$ 10,52/kg | 108,9 t | tampa colorida sem dobradiça |
| PEBD PB 608 | R$ 11,10/kg | 0,5 t | (descartado — ver seção 6) |
| TPE Karinprene 45 | sem compra | — | aro de vedação, a recotar |

| Item | Peso | Resina |
|---|---|---|
| Corpo 600 ml | 45,4 g | R$ 0,50 |
| Corpo 1,2 L | 73,0 g | R$ 0,81 |
| Corpo 1,8 L | 105,8 g | R$ 1,17 |
| Corpo 2,4 L | 142,5 g | R$ 1,58 |
| **Tampa PE (PEAD HA 7260)** | **27,6 g** | **R$ 0,26** |
| Tampa de teca (plug) | — | CNC, sem resina |
| Aro de TPE (só na teca) | 2,0 g | a cotar |

Só matéria-prima. Transformação entra pelo custo do PCP; a tampa de teca, pelo custo da WOOD.

**O que a revisão 5 custou em resina.** Os quatro corpos somam **366,7 g** contra 349,1 g no
desenho R18 de 121,2 × 93,2 — **+17,6 g, +5,0%**, ou R$ 0,19 por jogo de quatro. Os dois efeitos
empurram para o mesmo lado: mesma área com frente estreita tem mais perímetro, e canto menos
arredondado também. Metade vem do ASP, metade do raio.

---

## 8. Ferramental

Escopo na revisão 6: **4 moldes de corpo + 1 molde de tampa PE + 1 molde de aro de TPE
= 6 ferramentas** — uma a menos que na revisão 5, porque a tampa PP dosadora saiu do escopo. A
tampa de teca não usa molde (CNC); o aro serve só a ela.

O molde da tampa PE é **de duas placas, extração por placa impulsora, sem gaveta**: a garra é um
undercut de 1,51% de deformação de aro, que o PE arrasta com folga (seção 6.1.5).

Referências dos próprios orçamentos com a MR Plastic Mould (`AD_ORCAMENTO`, USD): corpo lixeira
12 L / 380 t = 36.900 · 284-U / 280 t = 20.100 · 214-U / 250 t = 18.900 · corpo 026 / 120 t = 6.300 ·
tampa 026-T / 90 t = 5.500 · **115/1 "potes modulares" 2 cav = 47.100 (aprovado)**.

Faixa a cotar: corpos 2 cav entre USD 25–45 mil cada (o 2,4 L no topo, por profundidade, polimento
e placa impulsora), tampas USD 15–20 mil, aro de TPE ~USD 8 mil. **Ordem de grandeza USD 140–190 mil.**

---

## 9. Capacidade e ciclo

2 cavidades, 20 h úteis/dia, 22 dias. Ciclos um pouco maiores que na revisão 1 por causa da
extração da peça reta (mais tempo de resfriamento antes de arrancar do macho).

| Tamanho | Ciclo est. | pç/h | pç/mês | Resina |
|---|---|---|---|---|
| 600 ml | 17 s | 424 | 186 mil | 18,4 kg/h |
| 1,2 L | 21 s | 343 | 151 mil | 23,8 kg/h |
| 1,8 L | 25 s | 288 | 127 mil | 28,8 kg/h |
| 2,4 L | 29 s | 248 | 109 mil | 33,3 kg/h |

**Risco de preenchimento no 2,4 L:** L/t de 216 com parede de 1,40 mm. Viável com o PP de alta
fluidez que já se compra, mas no limite. Mitigar com câmara quente de **2 pontos de injeção** no
fundo, ou parede de 1,5 mm, ou RP 340 S. Definir no Moldflow antes de fechar o molde.

---

## 10. Mantimento — o que cabe

| Pote | Arroz | Feijão | Açúcar | Macarrão |
|---|---|---|---|---|
| 600 ml | 0,51 kg | 0,48 kg | 0,54 kg | 0,21 kg |
| 1,2 L | 1,02 kg | **0,96 kg (pacote de 1 kg)** | 1,08 kg | 0,42 kg |
| 1,8 L | 1,53 kg | 1,44 kg | 1,62 kg | 0,63 kg |
| 2,4 L | **2,04 kg (pacote de 2 kg)** | 1,92 kg | 2,16 kg | 0,84 kg |

A escala fecha com embalagem de mercado: o 2,4 L recebe o pacote de 2 kg de arroz e o 1,2 L recebe
o de 1 kg de feijão — que era justamente o que a escala anterior (500/1000/1500/2000) não fazia.

---

## 11. Próximos passos

1. **Confirmar a saída de 0,5°** com o design — é o que separa "reto" de "aninha no frete".
2. **Preencher `AD_INJETORAFICHA`** (curso de abertura, curso e força de extração) para as 46 injetoras.
3. **Reabrir o Projeto 115** e renegociar com a MR Plastic Mould a partir da cotação aprovada.
4. **Recotar o TPE Karinprene 45** — agora com volume das três tampas.
5. **Design da tampa**: bandeja com piso 2,0 mm abaixo da borda, pé do pote alinhado com a parede
   da bandeja, aba de alavanca para abrir, e bandeja-vertedor na versão de líquidos (6.3).
6. **Moldflow do 2,4 L** (L/t 216) e estudo de extração da peça reta.
7. **Try-out**: reservar INJ 32 (380 t) para o 2,4 L e INJ 25/24 (250 t) para o 1,8 L.

---

### Consultas usadas

`TPRWCP` + `TPRCAP` (parque e tonelagem) · `TPRWCP.AD_CICLOATUAL/AD_DHCICLO` (ciclo e estado ao
vivo) · `TPRAPA`→`TPRAPO`→`TPRIATV` (que peça roda em qual máquina, 24 meses) ·
`AD_FICHATECNICA` (ciclos de referência) · `AD_PROJETOS`/`AD_MOLDE`/`AD_ORCAMENTO` (projeto 115 e
benchmark de ferramental) · `TGFITE`/`TGFCAB` (preço real de resina e venda dos kits) ·
`TGFPRO` (linha modular atual, tampas, teca, TPE).

Memória de cálculo: `calculo-modular.py`.

---

## 12. Modelo 3D

`gera-3d.py` constrói o sólido a partir das mesmas cotas e escreve **sete** STL em `stl/`:
os quatro corpos, a tampa plug (perfil da teca), a **tampa PE** e o aro de TPE. O visualizador interativo remonta a malha a partir
da mesma receita de anéis, bandas e tampos (`perfis.json`), então desenho e STL não divergem.

**Como o sólido é construído:** cada peça é uma casca fechada feita de seções de retângulo com
cantos arredondados empilhadas em alturas diferentes; bandas de quadriláteros ligam um anel ao
seguinte e tampos em leque fecham as pontas.

**Conferências que a malha faz sozinha** (saem no terminal a cada geração):

| Verificação | Resultado |
|---|---|
| Volume assinado positivo **e normais consistentes** nas sete peças | sólido fechado e orientado para fora |
| Cavidade × capacidade nominal | 603,2 / 1203,2 / 1803,9 / 2405,3 ml contra 600 / 1200 / 1800 / 2400 — dentro de 0,6% |
| Peso da malha × `calculo-modular.py` | 46,5 / 74,3 / 107,3 / 144,4 g nos corpos, 22,9 g na tampa plug e 27,6 g na tampa PE — dentro de 5% |

**A checagem de normais entrou na revisão 6, e entrou porque falhou.** A tampa PE saiu com o piso da
bandeja invertido: a malha ficou **estanque**, o volume assinado devolveu um número plausível
(17,5 g) e nada acusou. O volume real era 27,6 g — 58% a mais. Volume assinado sozinho não detecta
normal invertida; `normais_consistentes()` confere que toda aresta aparece uma vez em cada sentido,
e agora o gerador **aborta** se alguma peça falhar.

A folga de 0,7% na cavidade é a poligonal de 12 segmentos por canto, não erro de cota
(`--seg 24` reduz). `verifica-malha.js` roda o construtor do visualizador fora do navegador e
confere o volume contra o STL — as seis peças batem.

**O que o modelo não é.** É malha, não sólido CAD: serve para conferir encaixe, empilhamento e
volume, e para imprimir protótipo. **O molde precisa do CAD paramétrico do projetista.** Estão no
modelo a aba da borda, o plug e o aro na canaleta; faltam a aba de alavanca, o chanfro de entrada da
boca e o furo e o entalhe do vertedor da seção 6.3. O aro está desenhado na medida livre, e por isso
invade 0,2 mm a parede no modelo — é justamente a interferência.

O corte do visualizador é onde se vê a vedação: o plug descendo dentro do pote e o aro trabalhando
contra a parede.


---

## 13. Estudo de referência — a vedação da Tupperware

> **Status: não implementado.** Levantado em 21/09/2026 a pedido, orçado, e deixado registrado.
> A linha continua com a tampa PE da revisão 6. Números reproduzíveis em
> `estudos/vedacao-tupperware.py`.

### 13.1 O que a patente diz

A patente original é a **US2487400A**, de Earl Tupper, depositada em 1947 e concedida em
08/11/1949 — **expirada há mais de 60 anos, princípio em domínio público**. O título já entrega
metade: *"Open mouth container and **nonsnap** type of closure therefor"*.

Três coisas fazem a vedação, e só uma é a que todo mundo comenta:

1. **Canal em U que engole a borda.** A tampa tem *"an upwardly directed and inverted U-shaped
   annular groove extending from the periphery"*; o pote tem a borda em **cordão** (*"double
   annular beads, outer annular beads, and inner annular beads"*). O cordão entra no canal e as
   duas paredes o apertam de faces opostas — *"a seal is effected between the engaging walls of
   the closure imposing **opposite pressures**"*. **Dois contatos radiais em faces opostas da
   mesma parede**, não junta achatada.
2. **É nonsnap.** Sem trava; segura por atrito no canal. É o mesmo requisito que o Ricardo deu na
   primeira mensagem — "sem trava, liso".
3. **O burp.** Expulsar o ar deixa o interior abaixo da atmosfera e a tampa flexível é sugada.

**Ressalva de método:** não consegui abrir o texto integral da patente — o proxy de saída desta
sessão bloqueia `patents.google.com`, `justia`, `freepatentsonline` e a Wikipédia. As citações
acima vieram de resumos de busca, **não do documento original**. Conferir antes de virar
especificação.

### 13.2 O que não dá para copiar, e por quê

**O burp está fora, e o motivo é estrutural.** A tampa da Tupperware é uma membrana de PEBD mole.
A nossa **carrega o pote de cima**: o piso da bandeja é o plano modular e tem de ser um datum
rígido. Membrana e datum são requisitos opostos. Dá para copiar a geometria da vedação; o sistema
inteiro, não.

### 13.3 Por que não sai de graça como saiu a garra

Na revisão 6 a sobretampa não custou nada ao pote porque o lábio da aba já era o ressalto de que a
garra precisava. Aqui não:

- o **topo da borda é plano** (4,40 mm/lado de mesa lisa): não há cordão em pé para o canal agarrar;
- a **canaleta em U que o pote já tem** (1,84 mm/lado, entre o corpo em 139,6 e o lábio em 143,3)
  **abre para baixo** — uma tampa que desce de cima não alcança.

### 13.4 Os dois caminhos, com número

| | **A — só na tampa** | **B — canal de faces opostas** |
|---|---|---|
| Muda o pote? | **Não** | **Sim**: cordão de 1,0 × 2,2 mm em pé no topo da borda, nos 4 moldes de corpo |
| Vedação | 2 selos **em série**: lábio no furo + cordão/garra por fora | 2 selos em **faces opostas** do mesmo cordão |
| Arranque reto (PEAD) | 4,3 kgf com 0,30 mm de interferência | 5,1 kgf com 0,20 mm |
| Descascando um canto | 0,7 kgf | 0,8 kgf |
| Depende do deck ficar plano? | Não — a reação fecha no aro do piso da bandeja | Não — as forças se fecham dentro do canal |

**Caminho A** resolveria de quebra o beco da revisão 6. Lá o lábio de vedação no furo não coube
porque a fenda de 0,95 mm ao lado da parede do poço era fina demais para o macho. **Pendurando o
lábio na aresta do piso da bandeja** (z = −3,50) em vez de ao lado da parede, a fenda some: sobra
um lábio de **3,6 × 0,60 mm com 0,30 mm de interferência** contra o furo, e a reação fecha no
próprio anel do piso — um aro em compressão, que é rígido no plano dele.

**Caminho B** é o mecanismo da patente do jeito dela, e é o único que dá o *"opposite pressures"*.
Preço: a borda muda nos quatro moldes de corpo, e o 2,4 L já é o mais caro do escopo.

**Em PEBD os dois caminhos dão 0,6–0,9 kgf** — mole demais para segurar. Mais um voto no PEAD
(seção 6.1.6).

### 13.5 Liberdade de operação

A US2487400 está expirada, mas o campo é povoado de patentes posteriores sobre geometrias
específicas de cordão e nervura — US5356026 (*Double seal container*), EP0283630 (*rim bead with
an engaging region formed inwardly and below it*), WO2008048406 (*double bead sealing system*).
**Antes de abrir molde com qualquer um dos dois caminhos, busca de liberdade de operação é etapa
real, não formalidade.**
