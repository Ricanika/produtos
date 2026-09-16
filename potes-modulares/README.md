# Linha Potes Retangulares Modulares em PP

**Status:** estudo de viabilidade técnica · **Data:** 16/09/2026
**Origem:** evolução do Projeto 115 do ERP ("Conjunto Potes Modular") · **Planta:** Nitron – Fábrica (CODPLP 1)

Documento de engenharia para o pedido: linha retangular em PP transparente, **3 tipos de tampa**
(teca + vedação TPE, PE, PP para líquidos), **4 litragens** (500 ml, 1 L, 1,5 L, 2 L) e
**modularidade de empilhamento** — qualquer combinação empilhada tem que chegar à altura do maior.

Todos os números de máquina, matéria-prima, custo e ferramental abaixo saíram do Sankhya
(produção, compras, cadastro de centros de trabalho e projetos), não de estimativa de catálogo.
As fontes estão citadas em cada seção.

---

## 1. Veredito

| Requisito | Situação |
|---|---|
| Modularidade de empilhamento | **Viável e resolvida** — passo único de 62 mm (seção 3) |
| 4 litragens exatas 500/1000/1500/2000 ml | **Viável** com bocal comum + pé de 6 mm e saída variando 1,2°–2,1° |
| Tampa única para os 4 tamanhos | **Viável** — já é prática da casa (ref. 321-T serve 800 ml, 1,2 L e 2,4 L) |
| Tampa teca + TPE | **Viável e diferencial** — madeira é cadeia própria (Teak Brazil / planta WOOD, FSC) |
| Tampa PE | Viável, **mas PEBD hoje é compra residual** (500 kg/12 meses) — precisa contrato |
| Tampa PP para sabão/amaciante | Viável — exige bico dosador e definição de vedação |
| Injeção dos 4 corpos no parque atual | **Cabe nas injetoras que já temos**, sem máquina nova (seção 5) |
| Confirmação documental de curso/altura de molde | **Bloqueio de dado**: a ficha das injetoras está vazia no ERP (seção 5.4) |

O ponto crítico da linha não é tonelagem — é **profundidade**. Os quatro corpos têm a mesma área
projetada (≈106 cm²) e pedem os mesmos ~100–116 t com 2 cavidades, mas o 2 L tem 250 mm de
profundidade e exige ~550 mm de curso de abertura. Isso empurra o 2 L para as injetoras de 380 t
(31/32/33) — que hoje já rodam o pote alto de 5,8 L e o modular de 2,4 L.

---

## 2. O que já existe na casa (e deve ser reaproveitado)

| Achado | Fonte |
|---|---|
| **Projeto 115 – "Conjunto Potes Modular"**, status Aprovado, produto já modelado. Descrição: *"Fazer 2 formatos: retangular e quadrado / cada formato com 3 alturas para manter as tampas"* | `AD_PROJETOS` |
| Molde 115/1 "potes modulares" — orçamento **aprovado de USD 47.100**, 2 cavidades, 75 dias, MR Plastic Mould, 04/2021 | `AD_MOLDE`, `AD_ORCAMENTO` |
| Linha modular quadrada em catálogo: 319-C (250 ml), 320-C (450 ml), 321-C (800 ml), 322-C (1,2 L), 323-C (2,4 L) | `TGFPRO` |
| **Tampa única já validada**: ref. 321-T = "TAMPA POTE QUADRADO MODULAR M. 800, 1,2, 2,4" — uma tampa para três alturas | `TGFPRO` |
| Kit modular vende: 353.006.001 "Kit Potes Modulares 6 pçs transparente" — **19.078 kits / R$ 449 mil em 12 meses** (R$ 23,54 médio) | `TGFITE`/`TGFCAB` |
| Tampa de madeira já é produto corrente, com FSC 100% (NEO-COC-191022): ref. 256-TFSC e cestos de juta com tampa de teca | `TGFPRO` |

**Recomendação:** reabrir o Projeto 115 em vez de criar projeto novo — o orçamento aprovado com a
MR Plastic Mould é a base de negociação do ferramental desta linha.

---

## 3. A regra modular

A exigência "empilhou, chega na altura do maior" é uma regra de **passo**, não de volume:
cada pote tem que somar um número inteiro de módulos.

```
módulo M = 62 mm
500 ml = 1 M      1 L = 2 M      1,5 L = 3 M      2 L = 4 M
```

Combinações conferidas (todas dão 248 mm = altura do 2 L):

```
500+500+500+500 = 248 mm     1000+1000 = 248 mm
500+500+1000    = 248 mm     500+1500  = 248 mm
```

### 3.1 Como o passo fecha exatamente

Três decisões de projeto sustentam o passo:

1. **Bocal único.** Os quatro corpos têm a mesma boca (110 × 84 mm interno) — daí uma tampa só
   para a linha inteira.
2. **Tampa rebaixada.** O topo da tampa fica abaixo da borda do pote, formando um berço que
   recebe o pé do pote de cima. A profundidade desse berço é igual ao que a base + o assento da
   tampa consomem, e é isso que faz o passo empilhado ser exatamente n × 62 mm, sem sobra.
3. **Pé de 6 mm.** O fundo é elevado 6 mm (rebaixo/punt). Ele centra o pote empilhado, esconde o
   ponto de injeção, dá rigidez ao fundo — e é o ajuste fino que faz a capacidade fechar redonda.

### 3.2 Por que a saída varia de 1,2° a 2,1°

Com bocal comum e passo constante, a parede inclinada faz o volume crescer mais rápido que a
altura: o pote de 1 módulo "sobra" volume e o de 4 módulos "falta". O ajuste é a saída — mais
saída nos baixos, menos nos altos. Os valores resultantes (1,19° a 2,09°) estão todos dentro da
prática de moldagem para PP polido. **Não existe solução com saída idêntica nos quatro e as
quatro capacidades redondas** — é geometricamente sobredeterminado; a saída é a variável livre.

---

## 4. Especificação dimensional

**Footprint externo (comum aos 4): 112,6 × 86,5 mm** · pé/rebaixo 6 mm · saída por lado conforme tabela

| Tamanho | Altura ext. corpo | Passo empilhado | Bocal interno | Base interna | Saída/lado | Prof. útil | Parede | Peso corpo |
|---|---|---|---|---|---|---|---|---|
| 500 ml | 63,7 mm | 62 mm | 110,4 × 84,3 | 106,0 × 80,0 | 2,01° | 56,0 mm | 1,10 mm | 41,3 g |
| 1 L | 125,8 mm | 124 mm | 110,3 × 84,2 | 101,3 × 75,2 | 2,09° | 118,0 mm | 1,15 mm | 64,9 g |
| 1,5 L | 187,9 mm | 186 mm | 110,1 × 84,0 | 100,0 × 73,9 | 1,55° | 180,0 mm | 1,25 mm | 94,7 g |
| 2 L | 250,0 mm | 248 mm | 109,9 × 83,8 | 99,5 × 73,5 | 1,19° | 242,0 mm | 1,35 mm | 128,9 g |

A parede engrossa com a altura por causa do comprimento de fluxo (seção 9.1). Peso calculado com
PP a 0,905 g/cm³, incluindo reforço de borda e parede do pé.

---

## 5. Validação nas injetoras

### 5.1 O parque (46 injetoras, 45 monitoradas — `TPRWCP` + `TPRCAP`)

| Classe | Qtd | Máquinas |
|---|---|---|
| 80 t | 1 | 18 |
| 120 t | 7 | 13, 14, 15, 16, 17, 44, 45 |
| 150 t | 2 | 42, 43 |
| 160 t | 9 | 7, 8, 9, 10, 11, 12, 36, 40, 41 |
| 200 t | 12 | 1–6, 19–22, 35, 37 |
| 250 t | 9 | 23–28, 38, 39, 46 |
| 280 t / 300 t | 2 | 29, 30 |
| 380 t | 3 | 31, 32, 33 |
| 600 t | 1 | 34 |

### 5.2 O que cada tamanho exige

| Tamanho | Área proj. | Fecham. 2 cav | Curso abert. mín. | Altura de molde | Injeção 2 cav | L/t |
|---|---|---|---|---|---|---|
| 500 ml | 106 cm² | 98 t | 140 mm | ~254 mm | ~105 cm³ | 109 |
| 1 L | 106 cm² | 104 t | 277 mm | ~316 mm | ~165 cm³ | 158 |
| 1,5 L | 106 cm² | 111 t | 413 mm | ~378 mm | ~241 cm³ | 195 |
| 2 L | 106 cm² | 116 t | 550 mm | ~440 mm | ~327 cm³ | 227 |

Fechamento a 0,42–0,50 t/cm² (PP, parede fina, peça profunda), + 10% de canal. Curso mínimo =
2,2 × profundidade da peça.

### 5.3 Alocação proposta — e a evidência de que o parque aguenta

A prova não é catálogo: são peças com a mesma geometria rodando hoje (`TPRAPA`→`TPRIATV`, 24 meses).

| Tamanho novo | Máquina proposta | Peça equivalente que já roda lá |
|---|---|---|
| 500 ml | 160 t — INJ 7–12, 36, 40, 41 | pote hermético peq. 176-C (INJ 13, ciclo 16,7 s) |
| 1 L | 200 t — INJ 1–6, 19–22, 35, 37 | **modular 450 ml (320-C) na INJ 37**; 2 L rosca (238-C) na INJ 1/22 |
| 1,5 L | 250 t — INJ 23–28, 38, 39 | **modular 1,2 L (322-C) na INJ 25**; 3 L (239-C) na INJ 24/27; 8 L (196-C) na INJ 39/24 |
| 2 L | 380 t — INJ 31, 32, 33 | **modular 2,4 L (323-C) na INJ 33**; pote alto 5,8 L (237-C) na INJ 31 e 33 |

Ou seja: a peça mais profunda desta linha (250 mm) é **menos exigente** que o pote de 5,8 L que já
roda nas 380 t. Não há necessidade de máquina nova.

**Máquinas sem ciclo recente na consulta de 16/09/2026 12:11** (`TPRWCP.AD_DHCICLO`):
INJ 30 (300 t, parada desde 08/09), INJ 41 (160 t, desde 10/09), **INJ 32 (380 t, desde 15/09)** —
a INJ 32 é a candidata natural para o try-out do 2 L.

### 5.4 Bloqueio de dado — ficha técnica das injetoras vazia

A tabela `AD_INJETORAFICHA` (ficha Haitian, 1:1 com `TPRWCP`) tem **1 registro e todos os 29
campos de especificação nulos**. Isso significa que **curso de abertura, altura máx/mín de molde,
distância entre colunas e capacidade de injeção não podem ser conferidos no sistema** — a
alocação acima está ancorada em evidência de produção, não em especificação.

Antes de liberar o projeto dos moldes, preencher para as 46 injetoras:
`FORCAFECH`, `CURSOABERT`, `ALTMINMOLDE`, `ALTMAXMOLDE`, `COLUNASH`, `COLUNASV`, `CAPINJECAO`,
`CURSOEXTR`, `DIAMFUSO`. Sem isso, o molde do 2 L (440 mm de altura, 550 mm de curso) é aposta.

### 5.5 Alerta de aproveitamento de máquina

O 2 L com 2 cavidades usa **116 t numa máquina de 380 t (30% do fechamento)**: paga-se hora de
máquina grande para usar pouco. Duas saídas:

- **4 cavidades no 2 L** (≈232 t, molde ~600 × 500 mm — cabe entre as colunas de uma 380 t):
  dobra a produção pela mesma hora-máquina;
- 2 cavidades na INJ 34 (600 t) só se o curso das 380 t não fechar.

Mesma lógica vale para o 1,5 L (111 t numa 250 t): avaliar 3–4 cavidades na segunda fase.

---

## 6. As três tampas

Bocal único ⇒ **uma tampa por tipo atende os quatro tamanhos**. São 3 ferramentas de tampa, não 12.

### 6.1 Teca + vedação TPE
- Madeira é cadeia própria: teca em tora e **ripa serrada** (CODPROD 6759), planta **WOOD** com
  CNC RXK2513, moldureira, lixadeiras e prensa de alta frequência, e a empresa **Teak Brazil**.
  Já se produz tampa de madeira em série (256-TFSC) com **FSC 100%** — argumento comercial forte.
- A vedação: **TPE Karinprene dureza 45 (CODPROD 997) está cadastrado mas sem compra nem consumo
  há mais de 4 anos**. É reintrodução de material, não item de rotina.
- **Não há bi-injeção no parque**: o anel de TPE tem que ser peça injetada à parte e montada
  (molde próprio), ou comprado pronto. Decisão de processo a tomar.
- Peso estimado do anel: ~7 g.

### 6.2 Tampa PE
- PEBD PB608 a R$ 11,10/kg, mas **só 500 kg comprados em 12 meses** — hoje é compra residual.
  Volume desta linha muda a escala de compra; precisa de contrato antes do lançamento.
- Peso estimado: ~17 g (1,6 mm).
- Avaliar PP copolímero (CP 141, R$ 10,52/kg, 109 t/ano comprados) como alternativa de tampa
  flexível, se o toque atender — evita abrir uma cadeia nova de resina.

### 6.3 Tampa PP para sabão líquido / amaciante
- PP CP 141 (copolímero, R$ 10,52/kg) — resistência a detergente e a queda.
- Exige **bico dosador com tampa basculante** e vedação por compressão (não serve o anel de TPE
  da versão teca).
- **Ponto de ergonomia:** 2 L de líquido ≈ 2 kg num corpo de 112 × 86 mm sem pega. Recomendo
  rebaixo de pega nas laterais dos tamanhos 1,5 L e 2 L, definido junto com o design.
- Peso estimado: ~16 g.

---

## 7. Matéria-prima e custo de material

Preços reais de compra dos últimos 12 meses (`TGFITE`/`TGFCAB`), não tabela:

| Material | Preço médio | Volume comprado 12 m | Uso nesta linha |
|---|---|---|---|
| PP H 105 homopolímero **com clarificante** | **R$ 11,06/kg** | 925,9 t | **corpo transparente** (grade padrão da casa) |
| PP RP 340 S randômico fluidez 45 | R$ 17,00/kg | 49,5 t | alternativa de maior transparência/fluidez p/ o 2 L |
| PP CP 141 copolímero | R$ 10,52/kg | 108,9 t | tampa PP |
| PEBD PB 608 | R$ 11,10/kg | 0,5 t | tampa PE |
| TPE Karinprene 45 | sem compra | — | anel de vedação (reintroduzir) |

| Item | Peso | Resina |
|---|---|---|
| Corpo 500 ml | 41,3 g | R$ 0,46 |
| Corpo 1 L | 64,9 g | R$ 0,72 |
| Corpo 1,5 L | 94,7 g | R$ 1,05 |
| Corpo 2 L | 128,9 g | R$ 1,43 |
| Tampa PE | ~17 g | R$ 0,19 |
| Tampa PP | ~16 g | R$ 0,17 |
| Anel TPE | ~7 g | a cotar |

Só matéria-prima. Transformação (hora-máquina, energia, mão de obra, refugo) e a tampa de teca
entram pelo custo do PCP e da planta WOOD.

---

## 8. Ferramental

Referências dos próprios orçamentos da casa com a MR Plastic Mould (`AD_ORCAMENTO`, em USD):

| Molde | Máquina | Valor |
|---|---|---|
| 283-C corpo lixeira 12 L | 380 t | USD 36.900 |
| 284-U | 280 t | USD 20.100 |
| 214-U | 250 t | USD 18.900 |
| 026-C corpo | 120 t | USD 6.300 |
| 026-T tampa | 90 t | USD 5.500 |
| **115/1 "potes modulares" (aprovado, 2 cav)** | — | **USD 47.100** |

Escopo desta linha: **4 moldes de corpo + 3 moldes de tampa + 1 molde de anel TPE = 8 ferramentas**
(a tampa de teca não usa molde — usa programa de CNC e gabarito na WOOD).

Faixa de referência, a cotar: corpos 2 cav entre USD 25–45 mil cada (o de 2 L no topo, por
profundidade e polimento), tampas USD 15–20 mil, anel TPE ~USD 8 mil. **Ordem de grandeza
USD 150–200 mil** — a cotação de USD 47.100 já aprovada no Projeto 115 deve ser o ponto de partida
da renegociação, não um número novo.

---

## 9. Capacidade e ciclo

Estimativa com 2 cavidades, 20 h úteis/dia, 22 dias. O ciclo medido hoje no parque para peças
equivalentes fica entre 16,7 s (pote pequeno) e 30,5 s (tampa grande) — as estimativas abaixo
estão dentro dessa faixa.

| Tamanho | Ciclo est. | pç/h | pç/mês | Resina |
|---|---|---|---|---|
| 500 ml | 16 s | 450 | 198 mil | 18,6 kg/h |
| 1 L | 20 s | 360 | 158 mil | 23,4 kg/h |
| 1,5 L | 24 s | 300 | 132 mil | 28,4 kg/h |
| 2 L | 28 s | 257 | 113 mil | 33,1 kg/h |

O 2 L é o gargalo do conjunto: se a linha for vendida em kit, ele dita o ritmo. É o argumento
técnico para as 4 cavidades da seção 5.5.

### 9.1 Risco de preenchimento no 2 L

Com parede de 1,35 mm e 250 mm de profundidade, o **L/t chega a 227**. É viável com PP de alta
fluidez (o H 105 e o RP 340 S fluidez 45 que já se compra) e injeção rápida, mas está no limite
superior. Mitigações, em ordem de preferência:

1. câmara quente com **2 pontos de injeção** no fundo;
2. parede de 1,4–1,5 mm no 2 L (custa ~8 g/peça);
3. RP 340 S (fluidez 45) no lugar do H 105 no 2 L — custa R$ 6/kg a mais.

Decidir no estudo de fluxo (Moldflow) antes de fechar o molde.

---

## 10. Decisão comercial que precisa ser tomada antes do molde

A escala pedida (500 / 1000 / 1500 / 2000 ml) não casa com embalagem de mantimento:

| Pote | Arroz | Feijão | Açúcar |
|---|---|---|---|
| 500 ml | 0,42 kg | 0,40 kg | 0,45 kg |
| 1 L | 0,85 kg | 0,80 kg | 0,90 kg |
| 1,5 L | 1,27 kg | 1,20 kg | 1,35 kg |
| **2 L** | **1,70 kg** | 1,60 kg | 1,80 kg |

Um pacote de 2 kg de arroz **não cabe** no 2 L; precisa de 2,4 L. A referência visual do projeto
rotula os potes por mantimento ("ARROZ 2 kg", "FEIJÃO 1 kg") — com esta escala isso não se sustenta.

**Alternativa B — módulo de 600 ml**, mesmas alturas e mesma modularidade, só com o footprint
9% maior (122,6 × 94,2 mm):

| Pote | Altura | Peso | Fecham. 2 cav | Cabe |
|---|---|---|---|---|
| 600 ml | 63,8 mm | 49,1 g | 115 t | açúcar 540 g |
| 1,2 L | 125,9 mm | 75,9 g | 123 t | **feijão 1 kg** |
| 1,8 L | 188,0 mm | 109,7 g | 131 t | arroz 1,5 kg |
| 2,4 L | 250,1 mm | 148,3 g | 140 t | **arroz 2 kg** |

A alternativa B mantém a mesma alocação de máquinas (as alturas não mudam), fica ~15% mais pesada
por peça e **alinha com a linha modular quadrada que já vendemos** (o 2,4 L / ref. 323 é justamente
o tamanho que gira: 35 mil un/ano no cliente Natura).

Esta é uma decisão de posicionamento — grão embalado (B) versus capacidade redonda (A) — e ela
tem que sair antes do desenho do molde, porque muda o footprint.

---

## 11. Próximos passos

1. **Decidir a escala**: 500/1000/1500/2000 (A) ou 600/1200/1800/2400 (B). Muda o footprint.
2. **Preencher `AD_INJETORAFICHA`** para as 46 injetoras (curso, altura de molde, colunas,
   capacidade de injeção) — sem isso o molde do 2 L não tem conferência documental.
3. **Reabrir o Projeto 115** e renegociar com a MR Plastic Mould a partir da cotação aprovada.
4. **Definir a vedação de TPE**: injetar em molde próprio ou comprar pronto — e recotar o
   Karinprene 45, parado há 4 anos.
5. **Contratar PEBD** em escala, ou decidir pela tampa em PP copolímero.
6. **Moldflow do 2 L** antes de fechar o molde (L/t 227).
7. **Design**: rebaixo de pega no 1,5 L e 2 L para a versão de líquidos; berço da tampa com a
   profundidade exata do pé de 6 mm (é o que garante o passo modular).
8. **Try-out**: reservar INJ 32 (380 t) para o 2 L e INJ 25/24 (250 t) para o 1,5 L.

---

### Consultas usadas

`TPRWCP` + `TPRCAP` (parque e tonelagem) · `TPRWCP.AD_CICLOATUAL/AD_DHCICLO` (ciclo e estado ao
vivo) · `TPRAPA`→`TPRAPO`→`TPRIATV` (que peça roda em qual máquina, 24 meses) ·
`AD_FICHATECNICA` (ciclos de referência) · `AD_PROJETOS`/`AD_MOLDE`/`AD_ORCAMENTO` (projeto 115 e
benchmark de ferramental) · `TGFITE`/`TGFCAB` (preço real de resina e venda dos kits modulares) ·
`TGFPRO` (linha modular atual, tampas, teca, TPE).

Memória de cálculo da geometria: `calculo-modular.py`.
