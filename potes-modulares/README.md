# Linha Potes Retangulares Modulares em PP

**Status:** estudo de viabilidade técnica · **Revisão 2** · 16/09/2026
**Origem:** evolução do Projeto 115 do ERP ("Conjunto Potes Modular") · **Planta:** Nitron – Fábrica (CODPLP 1)

Linha retangular em PP transparente, **parede reta com cantos arredondados**, quatro litragens
(**600 ml · 1,2 L · 1,8 L · 2,4 L**), três tampas e modularidade de empilhamento — qualquer
combinação empilhada chega à altura do maior.

Todos os números de máquina, matéria-prima, custo e ferramental saíram do Sankhya, não de
estimativa de catálogo. Fontes citadas em cada seção.

> **Revisão 2 — o que mudou:** escala migrou de 500/1000/1500/2000 para 600/1200/1800/2400 ml
> (pacote de mantimento); parede deixou de ser conada e passou a reta com R18 de canto; validado o
> orçamento de altura da tampa; recomendação de tampa PP com canaleta de TPE no lugar da tampa PE.

---

## 1. Veredito

| Requisito | Situação |
|---|---|
| Modularidade de empilhamento | **Viável** — passo único de 60 mm |
| Litragens 600 / 1200 / 1800 / 2400 ml | **Viável e exatas** — a parede reta elimina o conflito com o passo |
| Parede reta com cantos arredondados | **Viável** com 0,5°/lado e R18 — custa aninhamento no frete (seção 3.2) |
| Tampa única para os 4 tamanhos | **Viável** — já é prática da casa (ref. 321-T serve três alturas) |
| Altura da tampa dentro do passo | **Validada**: piso da bandeja 2,0 mm abaixo da borda (seção 5) |
| Tampa PE **ou** PP com canaleta de TPE | **Recomendado PP + canaleta** (seção 6) |
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

**Footprint externo 121,2 × 93,3 mm** · canto **R18** externo · saída **0,5°/lado** · módulo **60 mm**
Fundo de **2,0 mm igual nos quatro** · pé embutido de **110,0 × 84,6 mm igual nos quatro**

| Tamanho | Altura corpo | Passo | Bocal interno | Base externa | Degrau do pé | Elev. fundo | Parede | Volume | Peso |
|---|---|---|---|---|---|---|---|---|---|
| 600 ml | 62,0 mm | 60 mm | 118,9 × 91,0 | 120,2 | 5,09 mm | 1,8 mm | 1,15 mm | 600 ml | 42,5 g |
| 1,2 L | 122,0 mm | 120 mm | 118,8 × 90,9 | 119,1 | 4,57 mm | 3,4 mm | 1,20 mm | 1200 ml | 68,4 g |
| 1,8 L | 182,0 mm | 180 mm | 118,6 × 90,7 | 118,1 | 4,04 mm | 2,7 mm | 1,30 mm | 1800 ml | 98,9 g |
| 2,4 L | 242,0 mm | 240 mm | 118,4 × 90,5 | 117,0 | 3,52 mm | 0,0 mm | 1,40 mm | 2400 ml | 133,2 g |

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
3. **Os últimos 6 mm da base recuam para um pé embutido de 110,0 × 84,6 mm**, medida igual nos
   quatro (o degrau varia de 3,5 a 5,1 mm para compensar a saída). Esse pé desce dentro da bandeja
   da tampa de baixo.

Com as três juntas: passo = 60n exato, capacidade = 600n exata, e **uma tampa só serve os quatro**.
Sem a terceira, o pote de cima não caberia dentro da bandeja — a boca do pote tem 118,9 mm e o corpo
tem 121,2 mm. O pé embutido é o que resolve, e de quebra os potes ficam **travados entre si** quando
empilhados, em vez de só apoiados.

**Orçamento de largura — é o que dimensiona o pé.** Entre a face externa do corpo e a face externa do
pé sobram 5,55 mm por lado, e tudo tem que caber ali:

| | por lado |
|---|---|
| borda reforçada do pote | 2,00 mm |
| lábio com a canaleta do aro de TPE | 2,00 mm |
| parede da bandeja da tampa | 1,00 mm |
| folga de encaixe | 0,55 mm |
| **soma** | **5,55 mm** |

É esse orçamento que fixa o pé em 110,0 mm. Com pé de 113 mm não sobra espaço para o aro de TPE —
foi a conta que definiu a medida.

**Caminho de carga:** pé do pote de cima → piso da bandeja → parede da bandeja → borda do pote →
parede do pote. O aro de TPE fica num lábio de vedação *para dentro* da borda, vedando radialmente
contra a boca — fora do caminho de carga, para não ser comprimido pelo peso da pilha.

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
| 600 ml | 126 cm² | 117 t | 136 mm | ~252 mm | 108 cm³ | 107 |
| 1,2 L | 126 cm² | 125 t | 268 mm | ~312 mm | 174 cm³ | 152 |
| 1,8 L | 126 cm² | 133 t | 400 mm | ~372 mm | 251 cm³ | 187 |
| 2,4 L | 126 cm² | 139 t | 532 mm | ~432 mm | 339 cm³ | 216 |

Os quatro têm a **mesma área projetada**: quem decide a máquina não é tonelagem, é profundidade.

### 4.2 Alocação — e a evidência de que o parque aguenta

| Tamanho | Máquina | Peça equivalente rodando hoje |
|---|---|---|
| 600 ml | 160 t — INJ 7–12, 36, 40, 41 | pote hermético peq. 176-C (ciclo medido 16,7 s) |
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

## 5. Altura da tampa — validação

A modularidade define um orçamento de altura rígido, e ele **não é o que se esperaria**: a tampa não
se apoia em cima da borda, ela desce para dentro da boca.

```
borda do pote ................... 62,0 mm   (600 ml)
piso da bandeja da tampa ........ 60,0 mm   = PLANO MODULAR, 2,0 mm abaixo da borda
vão livre da bandeja ............ 111,1 × 85,7 mm  (recebe o pé de 110,0 × 84,6 do pote de cima)
saia externa .................... livre, pendura 11 mm por fora do corpo — não entra no passo
```

Traduzindo:

- **O piso da bandeja fica 2,0 mm abaixo da borda do pote** e é exatamente igual à espessura do
  fundo. Essas duas medidas têm que casar, senão o passo não fecha.
- **A parede da bandeja sobe livremente acima do plano modular** — 3 a 6 mm dão um colar de
  centragem bonito em volta da base do pote de cima. Isso é escolha de design, não restrição.
- **A saia externa é livre.** Pode pendurar 11 mm ou 15 mm para fora do corpo: só conta para o passo
  o que acontece entre o plano modular e a borda.
- **Detalhe crítico:** o pé do pote de cima tem que pousar no piso da bandeja junto à parede dela,
  não no meio do painel. Assim a carga desce pela parede da bandeja até a borda do pote. Se o apoio
  cair no centro, um 2,4 L com 2 kg de arroz em cima afunda a tampa.
- **Tampa dosadora:** um bico basculante comum tem 8 a 12 mm e não cabe acima do plano modular. Duas
  saídas — um **poço rebaixado no centro da bandeja** para alojar o bico (o apoio do pote de cima
  passa a ser o anel periférico do piso), ou assumir que a versão de líquidos é o topo da pilha.
  A do poço é melhor: mantém a linha inteira empilhável.

Tampa em números: **125,2 × 97,3 mm externos, 24,5 g em PP** (25,0 g em PEBD), saia de 11 mm.

## 6. As três tampas — PE ou PP com canaleta de TPE?

**Recomendação: PP com canaleta para o mesmo aro de TPE da tampa de teca.**

| | Tampa PE | **Tampa PP + aro TPE** |
|---|---|---|
| Peso / resina | 25,0 g · R$ 0,28 | 24,5 g · R$ 0,26 + aro 2,6 g |
| Vedação | por interferência na borda, sem garantia | **aro de TPE comprimido — vedação real** |
| Empilhamento | PEBD **flui a frio** (creep): cede sob carga permanente | PP copolímero segura a carga |
| Cadeia de resina | PEBD: **500 kg comprados em 12 meses** | PP CP 141: **109 t/ano já em casa** |
| Reciclagem | pote PP + tampa PE = material misto | **mono-material**, o aro sai na mão |
| Aro de TPE | continua necessário só para a teca | **o mesmo aro serve as três tampas** |
| Moldes | 3 (PE + PP dosadora + aro) | 3 (PP hermética + PP dosadora + aro) |

Os quatro argumentos que decidem:

1. **Empilhamento é o produto.** A linha inteira existe para empilhar — a tampa é peça estrutural.
   PEBD tem fluência a frio muito maior que PP: sob um 2,4 L carregado, a tampa PE cede com o tempo.
2. **Parede reta tira a vantagem do PE.** A virtude da tampa PE é vedar esticando sobre a borda. Com
   parede reta a borda tem pouca geometria para agarrar — precisaria de ressalto de encaixe de
   qualquer jeito. O aro de TPE resolve melhor e com menos exigência de tolerância.
3. **O aro de TPE passa a se pagar.** Hoje ele é um molde para servir só a versão de teca. Servindo
   as três tampas, o mesmo molde amortiza em três vezes o volume — e o TPE Karinprene 45, parado há
   4 anos, volta a ter escala para recotação.
4. **Suprimentos.** PEBD é compra residual e viraria contrato novo por causa de uma tampa. O PP
   copolímero já entra 109 t/ano.

Ressalvas honestas: a tampa PP é **mais dura de abrir** que a PE — precisa de aba de alavanca bem
resolvida no design; e tem que ser **copolímero** (CP 141), não homopolímero, por causa de impacto
em baixa temperatura (freezer). O custo por peça fica praticamente empatado (R$ 0,26 + aro contra R$ 0,28),
então a decisão é técnica, não de custo.

**Se ainda assim quiserem PE**, ele funciona como versão econômica de linha de entrada — mas aí
sem promessa de hermeticidade e com a tampa marcada como "não recebe pote carregado em cima".

### 6.1 Tampa de teca
Cadeia própria: teca em tora e ripa serrada (CODPROD 6759), planta **WOOD** (CNC RXK2513,
moldureira, lixadeiras, prensa de alta frequência) e a empresa **Teak Brazil**. Tampa de madeira já
é produto corrente com FSC 100%. Sem molde — programa de CNC e gabarito. Usa o mesmo aro de TPE,
alojado em canaleta usinada.

### 6.2 Processo do aro de TPE
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
| PP CP 141 copolímero | R$ 10,52/kg | 108,9 t | tampas |
| PEBD PB 608 | R$ 11,10/kg | 0,5 t | (descartado — ver seção 6) |
| TPE Karinprene 45 | sem compra | — | aro de vedação, a recotar |

| Item | Peso | Resina |
|---|---|---|
| Corpo 600 ml | 42,5 g | R$ 0,47 |
| Corpo 1,2 L | 68,4 g | R$ 0,76 |
| Corpo 1,8 L | 98,9 g | R$ 1,09 |
| Corpo 2,4 L | 133,2 g | R$ 1,47 |
| Tampa PP | 24,5 g | R$ 0,26 |
| Aro TPE | 2,6 g | a cotar |

Só matéria-prima. Transformação entra pelo custo do PCP; a tampa de teca, pelo custo da WOOD.

---

## 8. Ferramental

Escopo: **4 moldes de corpo + 2 moldes de tampa (hermética e dosadora) + 1 molde de aro de TPE
= 7 ferramentas.** A tampa de teca não usa molde.

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
   da bandeja, aba de alavanca para abrir, e poço rebaixado para o bico da dosadora.
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
