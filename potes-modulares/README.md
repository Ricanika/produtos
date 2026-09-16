# Linha Potes Retangulares Modulares em PP

**Status:** estudo de viabilidade técnica · **Revisão 4** · 16/09/2026
**Origem:** evolução do Projeto 115 do ERP ("Conjunto Potes Modular") · **Planta:** Nitron – Fábrica (CODPLP 1)

Linha retangular em PP transparente, **parede reta com cantos arredondados**, quatro litragens
(**600 ml · 1,2 L · 1,8 L · 2,4 L**), três tampas e modularidade de empilhamento — qualquer
combinação empilhada chega à altura do maior.

Todos os números de máquina, matéria-prima, custo e ferramental saíram do Sankhya, não de
estimativa de catálogo. Fontes citadas em cada seção.

> **Revisão 4 — o que mudou:** a vedação passa a ser **radial**, do jeito certo: a tampa tem um
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
| Parede reta com cantos arredondados | **Viável** com 0,5°/lado e R18 — custa aninhamento no frete (seção 3.2) |
| Tampa única para os 4 tamanhos | **Viável** — já é prática da casa (ref. 321-T serve três alturas) |
| Vedação da tampa | **Refeita na revisão 4**: plug com aro de TPE radial contra a parede, sem trava (seção 5) |
| Tampa PE **ou** PP com canaleta de TPE | **Recomendado PP randômico RP 141 + canaleta** (seção 6) |
| Injeção dos 4 corpos no parque atual | **Cabe no que já temos**, sem máquina nova |
| Confirmação documental de curso/extração | **Bloqueio de dado**: ficha das injetoras vazia (seção 4.4) |

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

**Corpo 121,2 × 93,3 mm** · **127,2 × 99,2 mm na aba da borda** · canto **R18** · saída **0,5°/lado** · módulo **60 mm**
Fundo de **2,0 mm igual nos quatro** · parede da borda **1,40 mm igual nos quatro** · pé embutido de **112,4 × 84,4 mm igual nos quatro**

| Tamanho | Altura corpo | Passo | Bocal interno | Base externa | Degrau do pé | Elev. fundo | Parede | Volume | Peso |
|---|---|---|---|---|---|---|---|---|---|
| 600 ml | 62,0 mm | 60 mm | 118,9 × 90,9 | 120,1 | 3,86 mm | 2,0 mm | 1,15 mm | 600 ml | 43,7 g |
| 1,2 L | 122,0 mm | 120 mm | 118,8 × 90,8 | 119,1 | 3,34 mm | 3,4 mm | 1,20 mm | 1200 ml | 69,8 g |
| 1,8 L | 182,0 mm | 180 mm | 118,6 × 90,6 | 118,0 | 2,81 mm | 2,7 mm | 1,30 mm | 1800 ml | 100,6 g |
| 2,4 L | 242,0 mm | 240 mm | 118,4 × 90,4 | 117,0 | 2,29 mm | 0,0 mm | 1,40 mm | 2400 ml | 135,1 g |

Empilhamento conferido — todas as combinações dão 240 mm:
`600×4` · `1,2 L×2` · `600+600+1,2 L` · `600+1,8 L` · `2,4 L`.

### 3.1 Por que a parede reta ajuda

Na revisão 1 (pote conado, 1,2° a 2,1°) havia um conflito estrutural: com bocal comum e passo
constante, a parede inclinada faz o volume crescer mais rápido que a altura, e as capacidades
redondas só fechavam variando muito a saída entre os tamanhos.

**Com parede reta o volume fica praticamente proporcional à altura** e o conflito some. Sobra um
resíduo pequeno (a seção ainda cresce 0,5° por lado até o bocal), absorvido por uma **elevação de
fundo de 0 a 3,4 mm** — invisível por fora, sem efeito no empilhamento e sem custo de ferramenta.

### 3.2 O encaixe: três regras que fazem o passo fechar exato

Esta é a parte que não pode ser negociada no design, porque é ela que sustenta a modularidade:

1. **Fundo de 2,0 mm, igual nos quatro potes.**
2. **A tampa é uma bandeja cujo piso fica 2,0 mm abaixo da borda do pote** — recuado para dentro da
   boca, não apoiado em cima dela. Esse piso é o plano modular: é nele que o pote de cima se apoia.
3. **Os últimos 6 mm da base recuam para um pé embutido de 112,4 × 84,4 mm**, medida igual nos
   quatro (o degrau varia de 2,3 a 3,9 mm para compensar a saída). Esse pé desce dentro da bandeja
   da tampa de baixo.

Com as três juntas: passo = 60n exato, capacidade = 600n exata, e **uma tampa só serve os quatro**.
Sem a terceira, o pote de cima não caberia dentro da bandeja — a boca do pote tem 118,9 mm e o corpo
tem 121,2 mm. O pé embutido é o que resolve, e de quebra os potes ficam **travados entre si** quando
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

É esse orçamento que fixa o pé em 112,4 mm. Na revisão 2 havia um aro de TPE dentro dessa conta,
com 2,00 mm reservados para uma canaleta que precisa de 4,00 — era o número errado, e o pé de
110,0 mm saiu dele. Tirando o aro da tampa de PP, a conta fecha e o pé cresce.

**Caminho de carga:** pé do pote de cima → piso da bandeja → parede do plug → borda do pote →
parede do pote. O aro de TPE fica na canaleta do plug, mais abaixo, vedando radialmente contra a
parede — fora do caminho de carga, para não ser comprimido pelo peso da pilha.

### 3.3 Quanto de saída é "reto"

Saída zero não extrai: a peça agarra o macho. O que se faz é a saída mínima de extração.

| Saída/lado | Base mais estreita que o topo | Aninhamento de 6 potes de 2,4 L |
|---|---|---|
| 0,25° | 2,1 mm (1,8%) | 1.452 mm — **não aninha** |
| **0,50°** | **4,2 mm (3,5%)** | **1.044 mm (−28%)** |
| 0,75° | 6,3 mm (5,3%) | 777 mm (−47%) |
| 1,00° | 8,4 mm (7,1%) | 643 mm (−56%) |

**Recomendação: 0,5°/lado.** No maior pote a base fica 4,2 mm mais estreita que o topo em 121 mm de
largura — 3,5%, imperceptível com canto R18 e parede polida. Abaixo disso a peça deixa de aninhar a
vazio e o frete do pote vazio sobe ~28%.

Condições para a parede reta funcionar na extração:
- **acabamento polido** (SPI A2 ou melhor) nas laterais — textura exige saída extra (~1° a cada
  0,025 mm de profundidade de textura) e mataria o "reto";
- **extração por placa impulsora** (não por pinos), com **válvula de ar no topo do macho** para
  quebrar o vácuo;
- força de extração estimada em ~5 kN no 2,4 L (932 cm² de contato) contra ~62 kN disponíveis numa
  injetora de 380 t — **força não é o problema; curso de extração e vácuo são**;
- o canto R18 é aliado: reduz o arrasto nos cantos, que é onde a peça reta costuma marcar.

## 4. Validação nas injetoras

### 4.1 O que cada tamanho exige

| Tamanho | Área proj. | Fecham. 2 cav | Curso abert. mín. | Altura de molde | Injeção 2 cav | L/t |
|---|---|---|---|---|---|---|
| 600 ml | 139 cm² | 129 t | 136 mm | ~252 mm | 112 cm³ | 107 |
| 1,2 L | 139 cm² | 138 t | 268 mm | ~312 mm | 178 cm³ | 152 |
| 1,8 L | 139 cm² | 147 t | 400 mm | ~372 mm | 256 cm³ | 187 |
| 2,4 L | 139 cm² | 153 t | 532 mm | ~432 mm | 344 cm³ | 216 |

A aba da borda aumentou a área projetada de 126 para 139 cm², e com ela o fechamento. O 600 ml a
129 t numa injetora de 160 t usa 81% do fechamento — **passa a ser alocado na classe de 200 t**
junto com o 1,2 L.

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
permanente ao longo dos 389 mm de perímetro.

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
| **0,20 mm** | **5,8 kgf** | **1,0 kgf** |
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
boca do pote ......... 118,4 mm (parede de 1,40 mm nos quatro tamanhos)
face do plug ......... 116,4 mm — folga de 1,00 mm por lado
parede do plug ....... 1,50 mm
canaleta ............. 0,60 mm de profundidade, entre 5,0 e 7,4 mm abaixo da borda
aro de TPE ........... seção 2,4 × 1,8 mm, sobra 1,20 mm da face do plug
                       -> 0,20 mm de compressão contra a parede
plug desce ........... 12 mm dentro do pote
vão da bandeja ....... 113,4 mm, recebe o pé de 112,4 mm
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
vão livre da bandeja ............ 113,4 × 84,4 mm  (recebe o pé de 112,4 × 84,4)
plug .......................... desce até 12 mm abaixo da borda, dentro do pote
```

O pé do pote de cima tem que pousar no piso **junto à parede da bandeja** — que agora é a parede do
plug. A carga desce plug → borda → parede do pote.

## 6. As três tampas — PE ou PP?

**Recomendação: PP randômico RP 141, com plug e aro de TPE radial.**

| | Tampa PE | **Tampa PP + aro TPE** |
|---|---|---|
| Peso / resina | 23,3 g · R$ 0,26 | **22,8 g · R$ 0,22 + aro 1,8 g** |
| Vedação | plug em PE relaxa e perde a interferência | **plug rígido mantém o aro comprimido** |
| Empilhamento | PEBD **flui a frio** (creep): cede sob carga permanente | PP copolímero segura a carga |
| Cadeia de resina | PEBD: **500 kg comprados em 12 meses** | PP RP 141: **299 t/ano já em casa** |
| Reciclagem | pote PP + tampa PE = material misto | **mono-material**, o aro sai na mão |
| Aro de TPE | não resolve: PEBD relaxa e solta a compressão | **o mesmo aro nas três tampas** |
| Moldes | 3 (PE + PP dosadora + aro) | 3 (PP hermética + PP dosadora + aro) |

Os quatro argumentos que decidem:

1. **Empilhamento é o produto.** A linha inteira existe para empilhar — a tampa é peça estrutural.
   PEBD tem fluência a frio muito maior que PP: sob um 2,4 L carregado, a tampa PE cede com o tempo.
2. **O plug precisa ser rígido.** Ele mantém o aro comprimido contra a parede. Em PEBD o plug
   relaxa e a interferência de 0,20 mm some com o tempo — a vedação vai embora sozinha. PP segura.
3. **O aro de TPE se paga.** Com a vedação radial, o **mesmo aro serve as três tampas** — padrão,
   dosadora e teca — e o molde amortiza em toda a linha. (Eu tinha derrubado este argumento na
   revisão 3, quando a tampa vedava com lábio de PP; com o plug ele volta a valer.)
4. **Suprimentos.** PEBD é compra residual e viraria contrato novo por causa de uma tampa. O PP
   randômico RP 141 já entra 299 t/ano e é mais barato (R$ 9,54/kg).

Ressalvas honestas: a tampa PP precisa de **aba de alavanca bem resolvida** no design, que é o que
permite descascar em vez de puxar reto; e tem que ser **copolímero** (CP 141), não homopolímero, por causa de impacto
em baixa temperatura — e é aí que o randômico RP 141 resolve melhor que o homopolímero (ver 6.2).
O custo por peça fica empatado (R$ 0,23 + aro contra R$ 0,28), então a decisão é técnica, não de custo.

**Se ainda assim quiserem PE**, ele funciona como versão econômica de linha de entrada — mas aí
sem promessa de hermeticidade e com a tampa marcada como "não recebe pote carregado em cima".

### 6.1 Tampa de teca
Cadeia própria: teca em tora e ripa serrada (CODPROD 6759), planta **WOOD** (CNC RXK2513,
moldureira, lixadeiras, prensa de alta frequência) e a empresa **Teak Brazil**. Tampa de madeira já
é produto corrente com FSC 100%. Sem molde — programa de CNC e gabarito. Usa o mesmo aro de TPE,
alojado em canaleta usinada.

### 6.2 Qual PP na tampa — as três famílias

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

### 6.3 O bico da tampa de líquidos

Requisito: prático, que não suje, sem copinho dosador e sem peça cara. E ainda tem que respeitar o
plano modular — nada pode passar acima dele, senão o pote de cima não assenta.

**Conceito recomendado: a bandeja é o vertedor.** A modularidade já obriga a tampa a ter uma bandeja
rebaixada de 2,0 mm. Ela é reaproveitada como bacia anti-gota, sem peça nova:

1. **Um furo de vazão no canto** da bandeja (≈ 25 × 15 mm), encostado na parede.
2. **Um entalhe de 12 a 15 mm na parede da bandeja**, no mesmo canto, por onde o líquido sai quando o
   pote inclina. O canto R18 já faz a curva do vertedor — não precisa moldar bico nenhum.
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

### 6.4 Processo do aro de TPE
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
| Corpo 600 ml | 43,9 g | R$ 0,49 |
| Corpo 1,2 L | 70,0 g | R$ 0,77 |
| Corpo 1,8 L | 100,8 g | R$ 1,11 |
| Corpo 2,4 L | 135,3 g | R$ 1,50 |
| Tampa PP RP 141 | 22,8 g | R$ 0,22 |
| Aro de TPE | 1,8 g | a cotar |
| Aro TPE | 2,6 g | a cotar |

Só matéria-prima. Transformação entra pelo custo do PCP; a tampa de teca, pelo custo da WOOD.

---

## 8. Ferramental

Escopo: **4 moldes de corpo + 2 moldes de tampa (padrão e dosadora) + 1 molde de aro de TPE
= 7 ferramentas.** A tampa de teca não usa molde; o aro serve só a ela.

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

`gera-3d.py` constrói o sólido a partir das mesmas cotas e escreve seis STL em `stl/`:
os quatro corpos, a tampa e o aro de TPE. O visualizador interativo remonta a malha a partir
da mesma receita de anéis, bandas e tampos (`perfis.json`), então desenho e STL não divergem.

**Como o sólido é construído:** cada peça é uma casca fechada feita de seções de retângulo com
cantos arredondados empilhadas em alturas diferentes; bandas de quadriláteros ligam um anel ao
seguinte e tampos em leque fecham as pontas.

**Conferências que a malha faz sozinha** (saem no terminal a cada geração):

| Verificação | Resultado |
|---|---|
| Volume assinado positivo nas seis peças | sólido fechado e orientado para fora |
| Cavidade × capacidade nominal | 605,0 / 1204,2 / 1806,4 / 2410,0 ml contra 600 / 1200 / 1800 / 2400 — dentro de 0,8% |
| Peso da malha × `calculo-modular.py` | 45,2 / 71,4 / 102,5 / 137,4 g nos corpos e 26,1 g na tampa — dentro de 3% nas seis peças |

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
