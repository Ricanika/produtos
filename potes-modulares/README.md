# Linha Potes Retangulares Modulares em PP

**Status:** estudo de viabilidade técnica · **Revisão 8** · 23/09/2026
**Origem:** evolução do Projeto 115 do ERP ("Conjunto Potes Modular") · **Planta:** Nitron – Fábrica (CODPLP 1)

Linha retangular em PP transparente, **parede reta com cantos arredondados**, quatro litragens
(**600 ml · 1,2 L · 1,8 L · 2,4 L**), duas tampas e modularidade de empilhamento — qualquer
combinação empilhada chega à altura do maior.

Todos os números de máquina, matéria-prima, custo e ferramental saíram do Sankhya, não de
estimativa de catálogo. Fontes citadas em cada seção.

> **Revisão 8 — a borda, a partir do STL de referência.** O Ricardo mandou `REF_231.stl`
> (66 591 triângulos: um pote e uma tampa, em escala 1:10 — a parede medida, 0,113 mm, é o que
> fixa a escala). As cotas da linha ficam como estavam; o que muda é a **borda superior do corpo**
> e a **tampa de PP**.
>
> **O que foi medido na referência:**
>
> | | referência (×10) | o que virou aqui |
> |---|---|---|
> | corpo | 129,1 × 197,6 × 56,3 mm | fica o da linha: 142,5 × 76,6, alturas 62/122/182/242 |
> | borda | 17,3 mm de altura (31% do pote), sobressai 9,6 mm/lado | 12,0 mm + flare de 4,0, sobressai 5,60 mm/lado |
> | topo da borda | faixa chata de 4,3 mm, raio 2,5 fora e 1,9 dentro | faixa chata de 2,0 mm, raio 1,2 fora e chanfro 0,6 dentro |
> | travas | **2**, uma por lado comprido, 115,9 mm = **58%** do comprimento | 2, uma por lado comprido, 89 mm = 58% |
> | gancho | pega 19,5 mm abaixo do topo da tampa; rabo desce até 39 | pega a 10 mm; rabo até 16 |
>
> - **Borda alta e OCA.** A parede sobe reta, abre num **flare** de 4 mm, sobe pela **perna de
>   dentro** (1,40 mm, é ela que faz a boca), vira a **faixa chata do topo** e desce por fora numa
>   **saia livre** (1,20 mm) até 10 mm abaixo do topo. Entre a saia e a perna fica um **canal** de
>   1,20 mm, aberto para baixo. A face de baixo da saia — um anel horizontal de 1,20 mm — é a
>   **aresta de engate**.
> - **Duas travas de clipe**, uma por lado comprido, 89 mm cada, com gancho e rabo para o dedo.
>   Cada uma pede 2,0 kgf para fechar e 1,2 kgf no dedo para abrir.
> - **Tampa em PP** (era PEAD na revisão 6-7). Volta a ser monomaterial com o corpo.
>
> **O erro da revisão 7 que a referência revelou.** Na revisão 7 a boca media 144,95 mm e a face
> externa do corpo, 141,55. O colar era então um anel de material entre 144,95 e 148,55
> **pairando sobre um corpo que ia só até 141,55** — as duas seções não se encostavam em lugar
> nenhum. A malha fechava porque as duas superfícies horizontais em `z_col` se cancelavam: volume
> assinado plausível, normais consistentes, e **a peça em dois pedaços**. Impresso, o colar sairia
> solto. Foi ter de construir a borda como casca de verdade que trouxe isso à tona; agora
> `gera-3d.py` tem `secao_conexa()`, e um autoteste que a roda contra a geometria da revisão 7 a
> cada execução — ela **tem** de reprovar (seção 12).
>
> **O que a revisão custou:** a borda oca precisa de 3,80 mm de largura (saia 1,20 + canal 1,20 +
> perna 1,40) contra 1,80 de uma parede só. Pelo orçamento de largura (seção 3.2) isso empurra o
> rebaixo de 3,50 para **5,60 mm**, e como o módulo fixa a seção interna, a diferença sai do
> footprint: a medida máxima do corpo vai de **148,6 × 84,9 para 153,7 × 87,8 mm**, o peso do
> 600 ml de 47,0 para **52,9 g**, e a área projetada de 125 para **134 cm²**.
>
> **Terceira correção de número publicado:** a revisão 7 publicava **146 cm²** de área projetada
> para os quatro corpos — mas 146 é a silhueta do **deck da tampa**, um retângulo cheio maior que
> a peça. O corpo tem 134 cm². Cada peça agora usa a sua.

---

## 1. Veredito

| Requisito | Situação |
|---|---|
| Modularidade de empilhamento | **Viável** — passo único de 60 mm |
| Litragens 600 / 1200 / 1800 / 2400 ml | **Viável e exatas** — a parede reta elimina o conflito com o passo |
| Parede reta com cantos arredondados | **Viável** com 0,5°/lado e R10 na borda — o aninhamento a vazio **não piorou** (seção 3.4) |
| Rodapé reto para IML | **Viável** — seção constante do flare ao fundo, 46 mm no 600 ml |
| Trava na borda, nas duas tampas | **Só na de PP.** Teca é placa maciça com friso: segura por atrito |
| Capacidade útil com a tampa fechada | **Decisão aberta**: 486 ml no pote de 600 de borda (seção 5.6) |
| Tampa única para os 4 tamanhos | **Viável** — já é prática da casa (ref. 321-T serve três alturas) |
| Vedação das duas tampas | **Um filete de TPE** em friso, radial contra a boca, 0,20 mm de compressão (seção 5) |
| Tampa de teca empilhar | **Resolvido na revisão 7**: o topo da placa É o plano modular, sem poço a usinar |
| Tampa com trava | **Viável** — 2 travas de clipe em PP RP 141, 24,5 g, R$ 0,23 + filete |
| Injeção dos 4 corpos no parque atual | **Cabe no que já temos**, sem máquina nova |
| Confirmação documental de curso/extração | **Bloqueio de dado**: ficha das injetoras vazia (seção 4.4) |
| Rigidez da face comprida | **600 ml 2,4× mais rígido, 2,4 L 12% mais flexível** — a borda alta encurta a parede e alarga o painel (seção 3.3) |

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

**Medida máxima do corpo 153,7 × 87,8 mm** (face externa da saia da borda) · **corpo reto
142,5 × 76,6 mm** · canto **R10** na borda · saída **0,5°/lado** · módulo **60 mm**
**Borda 12,0 mm de altura + flare de 4,0 mm**, sobressaindo **5,60 mm/lado** · boca **146,1 mm** ·
fundo **2,0 mm igual nos quatro** · **rodapé reto, para IML**

A borda, camada por camada (seção no meio de um lado, por lado):

| | cota | o que é |
|---|---|---|
| face externa | 153,7 mm, reta, 0,5°/lado, do topo até −10,0 | o que a mão pega e a tampa cobre |
| faixa chata do topo | 2,00 mm de largura útil | raio 1,20 por fora, chanfro 0,60 na boca |
| saia externa | parede 1,20 mm, desce 10,0 mm | **ponta livre** — é o que torna a aresta material |
| canal | 1,20 mm de largura, 8,6 mm de profundidade | nervura de aço de 7,2:1 no molde |
| perna de dentro | parede 1,40 mm | faz a boca de 146,1 mm |
| **aresta de engate** | face de baixo da saia, **1,20 mm/lado**, a 10,0 mm do topo | o gancho avança 0,80 mm nela |
| flare | abre 3,20 mm/lado em 4,0 mm = 39° da vertical | liga a parede reta à perna |

| Tamanho | Altura total | Passo | Corpo reto | Fundo externo | Elev. fundo | Parede | Volume | Peso |
|---|---|---|---|---|---|---|---|---|
| 600 ml | 62,0 mm | 60 mm | 142,5 × 76,6 | 141,67 | 3,74 mm | 1,15 mm | 600 ml | 52,9 g |
| 1,2 L | 122,0 mm | 120 mm | 142,5 × 76,6 | 140,62 | 4,42 mm | 1,20 mm | 1200 ml | 80,8 g |
| 1,8 L | 182,0 mm | 180 mm | 142,5 × 76,6 | 139,58 | 3,19 mm | 1,30 mm | 1800 ml | 113,8 g |
| 2,4 L | 242,0 mm | 240 mm | 142,5 × 76,6 | 138,53 | 0,00 mm | 1,40 mm | 2400 ml | 150,9 g |

**O molde continua sem gaveta.** Descendo, por fora a peça **só estreita**: 153,7 (saia) → 148,9
(perna) → 142,5 (corpo) → 138,5 (fundo do 2,4 L). Por dentro também: 146,1 (boca) → 140,2 (corpo).
Nenhuma contra-saída.

**O que o molde ganha de novo:** a **nervura do canal** — 1,20 mm de espessura por 8,6 mm de
altura (7,2:1), contínua nos 466 mm de perímetro, na cavidade. Pede raio no pé, saída própria e
escape de ar na ponta. É o preço de ter uma aresta de engate que é material de verdade, e não um
anel flutuando como na revisão 7.

Empilhamento conferido — todas as combinações dão 240 mm:
`600×4` · `1,2 L×2` · `600+600+1,2 L` · `600+1,8 L` · `2,4 L`.

### 3.1 Por que a parede reta ajuda

Na revisão 1 (pote conado, 1,2° a 2,1°) havia um conflito estrutural: com bocal comum e passo
constante, a parede inclinada faz o volume crescer mais rápido que a altura, e as capacidades
redondas só fechavam variando muito a saída entre os tamanhos.

**Com parede reta o volume fica praticamente proporcional à altura** e o conflito some. Sobra um
resíduo pequeno (a seção ainda cresce 0,5° por lado, e a faixa do colar tem parede diferente do
corpo), absorvido por uma **elevação de fundo de 0 a 3,9 mm** — invisível por fora, sem efeito no
empilhamento e sem custo de ferramenta.

**A álgebra por trás disso não deixa escolha.** Com `A` = seção interna, `H` = altura externa,
`e` = altura do piso interno acima do fundo externo e `t` = quanto o apoio da tampa fica *acima*
da borda: capacidade exige `H = e + n·k`, passo exige `H + t = n·(H₁ + t)`, e juntando,
`eₙ = n·e₁ + (n−1)·t`. Com `e₁` = 2,0 mm, **o único `t` que mantém o fundo rente nos quatro é
−2,0** — isto é, o apoio tem de ficar 2,0 mm *dentro* da boca. Apoio acima da borda levanta o
fundo, e no 2,4 L isso vira 6 a 12 mm de espaço morto.

### 3.2 O encaixe: três regras que fazem o passo fechar exato

Esta é a parte que não pode ser negociada no design, porque é ela que sustenta a modularidade:

1. **Fundo de 2,0 mm, igual nos quatro potes.**
2. **A tampa é uma bandeja cujo piso fica 2,0 mm abaixo do topo da borda** — recuado para dentro da
   boca, não apoiado em cima dela. Esse piso é o plano modular: é nele que o pote de cima se apoia.
3. **O fundo reto do pote de cima desce dentro da bandeja.** Com o rodapé reto exigido pelo IML não
   há pé embutido: **o próprio fundo faz o serviço**.

**E é a regra 3, junto com a borda oca, que dimensiona o rebaixo.** O fundo reto tem de caber
dentro da boca, e a boca fica atrás de toda a largura da borda:

```
borda 3,80 (saia 1,20 + canal 1,20 + perna 1,40)
     + folga de encaixe 0,50 + parede do plug 0,80 + folga do plug 0,60   = 5,70 mm/lado
a saída já estreita, no corpo do 600 ml                                    = 0,40 mm
logo rebaixo = 5,70 - 0,40 + margem 0,30                                   = 5,60 mm
confere: bandeja 143,27 recebe o fundo de 141,67 com +0,80 mm/lado
```

**É aqui que a revisão 8 cobra.** Na revisão 7 a borda era uma parede só, 1,80 mm, e o rebaixo
fechava com 3,50. Mas aquela borda não podia ter aresta de engate: para o anel horizontal de baixo
existir como material, a saia precisa de **ponta livre**, e ponta livre exige canal, e canal exige
largura. São 2,00 mm a mais de borda, que viram 2,10 mm a mais de rebaixo — e como o módulo fixa a
seção interna (600 ml por 60 mm de altura), a diferença só pode sair do footprint:

| | revisão 7 | revisão 8 |
|---|---|---|
| medida máxima do corpo | 148,6 × 84,9 | **153,7 × 87,8** |
| corpo reto | 141,6 × 77,9 | **142,5 × 76,6** |
| boca | 145,0 | **146,1** |
| peso do 600 ml | 47,0 g | **52,9 g** |
| área projetada do corpo | 125 cm² | **134 cm²** |
| aresta de engate | 1,80 mm — **sobre material que não existia** | 1,20 mm, material de verdade |

**Caminho de carga:** fundo do pote de cima → piso da bandeja → parede do plug → topo da borda →
perna de dentro → flare → parede do pote. O filete de TPE fica no friso do plug, mais abaixo,
vedando radialmente contra a boca — fora do caminho de carga, para não ser comprimido pelo peso da
pilha.

### 3.3 O que a borda alta fez com a rigidez

Dois efeitos opostos. A borda de 16 mm (12 + flare) **come altura de parede reta**, o que encurta o
painel; o rebaixo maior derruba o canto do corpo de R6,5 para **R4,4**, o que **alarga** o painel.
O painel plano é o trecho de parede entre dois cantos.

Flecha de placa engastada nas quatro bordas, `flecha ~ α·b⁴/t³`, `b` = menor vão; 1,00 = o mesmo
tamanho na revisão 7:

| Tamanho | Painel rev. 7 | Painel rev. 8 | Flecha |
|---|---|---|---|
| **600 ml** | 128,6 × 55 | 133,7 × 44 | **0,42×** |
| 1,2 L | 128,6 × 115 | 133,7 × 104 | 0,82× |
| 1,8 L | 128,6 × 175 | 133,7 × 164 | 1,03× |
| **2,4 L** | 128,6 × 235 | 133,7 × 224 | **1,12×** |

No 600 ml o vão menor é a altura, e ela encurtou 11 mm: o painel ficou **2,4× mais rígido**. Do
1,8 L para cima o vão menor passa a ser a largura, e aí o painel mais largo pesa mais que a altura
menor — o 2,4 L fica **12% mais flexível**.

Em compensação a boca ganhou muito. A borda oca é um **caixão fechado de 3,80 × 12,0 mm**, contra o
colar de 1,80 × 5,0 da revisão 7. Quem prende o filete é a boca, e é ela que enrijeceu.

O que o protótipo tem de responder continua sendo o mesmo desde a revisão 5: **se a face comprida do
2,4 L cede o bastante para ovalizar a boca e soltar o filete**. Com a borda virando caixão fechado,
essa é a pergunta que mais mudou de resposta — e continua sem medida. Se o protótipo acusar, a
saída é o **bombê de 1,0 a 1,5 mm** na face comprida: lê como reta a olho nu, e não é parede conada
(a saída continua 0,5°, o molde continua de extração simples).

O número honesto: a **razão** é confiável, porque só a geometria mudou entre as colunas. A **flecha
absoluta** não é — depende de carga e engastamento real, e pedia elemento finito ou protótipo.
Nenhuma revisão foi prototipada.

### 3.4 Quanto de saída é "reto"

Saída zero não extrai: a peça agarra o macho. O que se faz é a saída mínima de extração.

| Saída/lado | Base mais estreita que o topo | Aninhamento de 6 potes de 2,4 L |
|---|---|---|
| 0,25° | 2,1 mm (1,5%) | 1.452 mm — **não aninha** |
| **0,50°** | **4,2 mm (3,0%)** | **1.044 mm (−28%)** |
| 0,75° | 6,3 mm (4,5%) | 777 mm (−47%) |
| 1,00° | 8,4 mm (6,0%) | 643 mm (−56%) |

**Recomendação: 0,5°/lado.** No maior pote a base fica 4,0 mm mais estreita que o topo em 142,5 mm
de largura — 2,8%, imperceptível com parede polida. Abaixo disso a peça deixa de aninhar a vazio e o
frete do pote vazio sobe ~28%.

**Eu esperava que a borda alta estragasse o aninhamento — não estraga.** A 0,5° a pilha de seis
2,4 L continua dando os mesmos 1.044 mm da revisão 7. Quem manda ali é a saída, não a borda: o
flare só vira batente abaixo de 0,3°, onde já não aninhava mesmo. O cálculo agora confere isso
varrendo o perfil externo de um pote contra o interno do outro, em vez de aplicar uma fórmula
fechada (`aninha()` em `calculo-modular.py`).

Condições para a parede reta funcionar na extração:
- **acabamento polido** (SPI A2 ou melhor) nas laterais — textura exige saída extra (~1° a cada
  0,025 mm de profundidade de textura) e mataria o "reto";
- **extração por placa impulsora** (não por pinos), com **válvula de ar no topo do macho** para
  quebrar o vácuo;
- força de extração estimada em ~5 kN no 2,4 L (932 cm² de contato) contra ~62 kN disponíveis numa
  injetora de 380 t — **força não é o problema; curso de extração e vácuo são**;
- o canto R10 da borda ainda é aliado; no corpo ele agora é R4,4, mais agressivo no arrasto — item para a ferramentaria olhar junto com a nervura do canal.

## 4. Validação nas injetoras

### 4.1 O que cada tamanho exige

| Tamanho | Área proj. | Fecham. 2 cav | Curso abert. mín. | Altura de molde | Injeção 2 cav | L/t |
|---|---|---|---|---|---|---|
| 600 ml | 134 cm² | 124 t | 136 mm | ~252 mm | 136 cm³ | 116 |
| 1,2 L | 134 cm² | 133 t | 268 mm | ~312 mm | 208 cm³ | 161 |
| 1,8 L | 134 cm² | 142 t | 400 mm | ~372 mm | 292 cm³ | 195 |
| 2,4 L | 134 cm² | 147 t | 532 mm | ~432 mm | 388 cm³ | 224 |

**Correção de número publicado.** A revisão 7 trazia 146 cm² para os quatro corpos — mas 146 é a
silhueta do **deck da tampa**, calculada como retângulo cheio, maior que a peça. A área projetada
do corpo é a da borda, com os cantos R10 descontados: **134 cm²**. A tampa, essa sim, tem 146 cm².
Cada peça agora usa a sua.

Mesmo corrigido, o 600 ml **não volta para a classe de 160 t** que a revisão 6 tinha conquistado: a
124 t ele usaria 78% de uma 160 t, acima do limite prático de 70–80% da casa. Fica na de 200 t,
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

O 2,4 L com 2 cavidades usa 147 t numa máquina de 380 t (39% do fechamento). Com **4 cavidades**
(~294 t, molde ~640 × 510 mm, cabe entre as colunas de uma 380 t) dobra a produção na mesma hora
de máquina. Mesma avaliação para o 1,8 L numa 250 t.

### 4.4 Bloqueio de dado

`AD_INJETORAFICHA` tem **1 registro com os 29 campos de especificação nulos**. Com parede reta o
dado que faltava ficou mais crítico, porque a extração passa a ser o ponto de projeto — e agora há
a nervura do canal no meio dela. Preencher
para as 46 injetoras antes de liberar o molde: `CURSOABERT`, `CURSOEXTR`, `FORCAEXTR`,
`ALTMINMOLDE`, `ALTMAXMOLDE`, `COLUNASH`, `COLUNASV`, `CAPINJECAO`, `FORCAFECH`.

---

## 5. A vedação — um filete de TPE para as duas tampas

Duas revisões erradas antes de chegar aqui, e vale registrar as duas.

**Revisão 2** especificava um aro de TPE comprimido contra a boca, sem dizer como ele ficaria preso
nem de onde viria a força. **Revisão 3** trocou por um lábio de PP moldado na tampa. Ambas partiam
do mesmo engano: tratar a vedação como **axial** — aro ou lábio esmagado entre a tampa e a borda.
Vedação axial num retângulo sem trava não funciona, e o número é implacável: 32 kgf de força
permanente ao longo dos 435 mm de perímetro.

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
| **0,20 mm** | **7,3 kgf** | **1,2 kgf** |
| 0,30 mm | 10,6 kgf | 1,8 kgf |
| 0,40 mm | 16,4 kgf | 2,7 kgf |

Ninguém puxa a tampa reta: levanta um canto e ela descasca, com ~1/6 do perímetro trabalhando por
vez. **1,0 kgf para abrir** é tampa de pote, não alicate.

Há um ganho de tabela que eu não tinha visto: **vedação radial tolera a borda flexionar.** Se o lado
reto abre um pouco, o aro acompanha o movimento da parede em vez de perder contato — que é
exatamente o que mata um aro axial. A **borda oca** cumpre esse papel desde a revisão 8: um caixão
de 3,80 × 12,0 mm que limita a flexão da boca a menos que a compressão de 0,20 mm — não para
segurar a tampa, para manter a boca redonda.

### 5.2 Cotas

```
boca do pote ......... 146,1 mm (perna de dentro 1,40 mm nos quatro tamanhos)
face do plug ......... 144,9 mm — folga de 0,60 mm por lado
parede do plug ....... 0,80 mm  (= parede da bandeja)
friso ................ 0,60 mm de profundidade, entre 3,0 e 4,4 mm abaixo do topo
filete de TPE ........ corda de 1,40 mm, sobra 0,80 mm do fundo do friso
                       -> 0,20 mm de compressão contra a parede da boca
plug desce ........... 8,0 mm dentro do pote (a boca tem 12,0 mm)
vão da bandeja ....... 143,3 mm, recebe o FUNDO RETO de 141,67 mm (+0,80/lado)
filete ............... 0,9 g, perímetro 438 mm
```

O plug faz três coisas de uma vez: **veda**, **forma a parede da bandeja** onde o pote de cima
apoia, e **centra a tampa**. O mesmo filete serve a tampa de teca, num friso 2,0 mm mais fundo.

### 5.3 O que ainda precisa de atenção

**Retenção do filete.** O friso tem 0,60 mm de profundidade. Um plug de parede fina sai disso por
**arranque** (stripping), com rampas nos dois ombros, sem gaveta no molde. O filete é montado
depois, esticado sobre o plug; a própria tensão mais os dois ombros o seguram contra o atrito da
parede. **Confirmar no primeiro tryout** — é o ponto que mais merece teste de vida (abrir e fechar
500 vezes e ver se o filete migra).

**Ar preso.** O filete só encosta nos últimos 2 mm do curso, mas isso ainda comprime o ar de dentro:
3,5 kPa (3,8 kgf) no 600 ml, 0,9 kPa (0,9 kgf) no 2,4 L. No 600 ml dá para sentir. Reduz-se com o
**chanfro de entrada da boca** (0,60 mm, já no modelo) ou aumentando-o para 1,5 mm. É o mesmo "pop"
que a OXO transformou em argumento de venda.

**Montagem.** O filete é peça montada — não existe bi-injeção no parque. 0,9 g de TPE mais alguns
segundos por tampa. O lado bom: o **mesmo filete serve as duas tampas**, então o molde dele
amortiza na linha inteira.

**Na revisão 8 o filete não mudou.** Mesma corda, mesma compressão, mesmo friso — só mudou o
diâmetro de trabalho, porque a boca passou de 145,0 para 146,1 mm.

### 5.4 O que entrega

**Entrega:** vedação contra umidade, poeira e cheiro, e resistência a tombo com o pote deitado.
Vedação radial com aro é o mesmo princípio de um O-ring — segura pressão, não só poeira.

**Não entrega sem teste:** estanqueidade garantida de cabeça para baixo com líquido. Com 0,20 mm de
compressão e a borda enrijecida é **plausível**, mas isso se mede no protótipo, não se promete na
planilha. Primeiro tryout com água colorida, pote deitado e de cabeça para baixo, 24 h.

### 5.5 Orçamento de altura

```
topo da borda ................... 62,0 mm   (600 ml)
piso da bandeja da tampa ........ 60,0 mm   = PLANO MODULAR, 2,0 mm abaixo do topo
vão livre da bandeja ............ 143,3 × 77,4 mm  (recebe o fundo reto de 141,67)
plug ............................ desce até 8,0 mm abaixo do topo, dentro da boca
```

O fundo do pote de cima tem que pousar no piso **junto à parede da bandeja** — que é a parede do
plug. A carga desce plug → topo da borda → perna de dentro → flare → parede do pote.

### 5.6 Capacidade de borda × capacidade útil

Número que nenhuma revisão anterior tinha olhado, e que a placa de teca tornou grande demais para
ignorar: **o plug come volume**. A capacidade nominal é de **borda** — convenção do setor e de todas
as revisões anteriores —, mas a tampa desce 2,0 mm (plano modular) mais a espessura dela:

| Tampa | Desce | Desloca | 600 ml | 1,2 L | 1,8 L | 2,4 L |
|---|---|---|---|---|---|---|
| Teca (placa 8 mm) | 10,0 mm | 114 ml | **486 ml** | 1.086 ml | 1.686 ml | 2.286 ml |
| PP (plug 8 mm) | 10,0 mm | 114 ml | **486 ml** | 1.086 ml | 1.686 ml | 2.286 ml |

No 600 ml a teca leva **19% do volume**. Na revisão 8 as duas tampas descem igual (10,0 mm), então
o número é o mesmo para as duas. Nos tamanhos maiores o peso relativo cai (5% no 2,4 L),
porque o deslocamento é constante e a capacidade cresce.

**Decisão em aberto:** rotular por borda (como está) ou re-resolver a linha para que a capacidade
*útil* seja 600n. A segunda opção sobe as alturas e quebra o passo de 60 mm — teria de vir com um
módulo novo.

---

## 6. As duas tampas

Duas tampas, **um só filete de TPE**. A de PP passa a fechar com **duas travas de clipe**, uma por
lado comprido, cobrindo 58% do comprimento — é o layout do STL de referência, e é o oposto das
6 abas de 18 mm da revisão 7.

| | **Teca** | **PP com 2 travas** |
|---|---|---|
| O que é | placa maciça 144,9 × 79,0 × 8,0 mm | plug + deck + 2 travas de 89 mm |
| Vedação | filete de TPE em friso usinado, radial | o **mesmo** filete, em friso moldado |
| Retenção | **só atrito**: 7,4 kgf reto, 1,2 descascando | **trava geométrica**: sair exige abrir 0,80 mm |
| Plano modular | o **topo da placa** é o plano | o piso da bandeja |
| Medida máxima | 144,9 × 79,0 mm | 157,3 × 93,4 mm |
| Peso / custo | 59 g em teca · CNC, sem molde | 24,5 g em RP 141 · R$ 0,23 |

**A tampa volta a ser PP.** Nas revisões 6 e 7 ela era PEAD HA 7260, escolhido por ser a resina mais
barata da casa. Em PP RP 141 (R$ 9,55/kg contra 9,34) a tampa custa R$ 0,23 em vez de R$ 0,21 — dois
centavos —, e em troca a linha volta a ser **monomaterial**, que era o único argumento contra o PE
que continuava valendo (o de reciclagem) e o mais sério (compra de PE é residual: 1,1 t em 12 meses
contra as 5,5 t/ano que 200 mil tampas pediriam).

### 6.1 Tampa de PP com trava de clipe

**A aresta de engate agora é material de verdade.** A saia externa da borda termina no ar, 10 mm
abaixo do topo: a face de baixo dela é um anel horizontal de **1,20 mm**, e o gancho avança
**0,80 mm** nele — 67% de engate. Não é canaleta, então o molde continua abrindo sem gaveta.

```
deck ............ passa 1,80 mm/lado da borda -> 157,3 mm de comprimento
travas .......... 2 × 89 mm × 1,00 mm; uma por lado COMPRIDO
                  face interna a 0,30 mm da face externa da borda
gancho .......... avança 0,80 mm sob a aresta; braço de 10,0 mm até ela
rabo ............ 6,0 mm abaixo do gancho, abrindo 1,50 mm para o dedo
medida máxima ... 157,3 × 93,4 mm (a trava só cresce a LARGURA)
plug ............ desce 8,0 mm na boca, com o friso do filete
bandeja ......... piso 2,0 mm abaixo do topo da borda = plano modular
```

**Cada trava fecha com 2,0 kgf, uma de cada vez.** Abrindo pelo rabo, a alavanca de 1,6× deixa
**1,2 kgf** no dedo. A deformação de fibra no fechamento é de **1,20%**, contra os ~8% em que o PP
randômico escoa — folga de 6,7×.

**É essa a diferença entre as duas tampas.** Na teca o filete faz as duas coisas: veda e segura.
Na de PP ele **só veda** — quem segura é a trava, e a trava é um **bloqueio geométrico**: para a
tampa sair, ela tem de abrir 0,80 mm. Por isso a de PP pode prometer hermeticidade sob transporte e
a de teca não.

**Por que duas grandes e não seis pequenas.** As travas ficam só nos lados compridos, que são os
flexíveis; os curtos são rígidos e não precisam. É o que a referência faz, e reduz de 6 para 2 as
feições que a ferramentaria tem de resolver.

### 6.1.1 O que não está resolvido na trava

**A extração ficou mais fácil, mas continua sendo arraste.** A contra-saída do gancho caiu de
**1,85 para 0,80 mm**, e a trava é uma aba livre nos três lados (fenda de ~1 mm) com 10 mm de
braço — dentro do que se faz todo dia em tampa de clipe. Ainda assim é item de ferramentaria, a
fechar antes de orçar o molde. **A fenda não está na malha**: é desenho de CAD.

**A dobradiça viva.** O braço de 10,0 mm com 1,00 mm de espessura funciona como viga engastada no
cálculo, mas uma trava de pote real é **sobre-centro**: ela passa de um ponto morto e trava lá.
Essa geometria não está modelada — o que existe é o gancho e o encosto. Detalhar a dobradiça é o
próximo passo do desenho da tampa.

**Os lados curtos não têm trava.** Como a vedação é radial, a boca tolera um pouco de levantamento
sem perder contato. Mas se o protótipo mostrar a tampa abrindo nos cantos, a resposta é uma
terceira trava (no meio de um lado curto) ou o bombê da seção 3.3.

### 6.2 Tampa de teca

Cadeia própria: teca em tora e ripa serrada (CODPROD 6759), planta **WOOD** (CNC RXK2513,
moldureira, lixadeiras, prensa de alta frequência) e a **Teak Brazil**. Tampa de madeira já é
produto corrente com FSC 100%. Sem molde — programa de CNC e gabarito.

**Placa maciça de 144,9 × 79,0 × 8,0 mm**, ~59 g em teca seca, com **friso usinado na face lateral**
alojando o filete de TPE. Sem trava: segura pelo atrito do filete, 7,4 kgf reto.

**O ponto que estava em aberto na revisão 6 fechou sozinho.** Lá a teca precisaria de um poço da
bandeja usinado, senão não empilharia. Agora **o topo da placa É o plano modular**: ele fica 2,0 mm
abaixo do topo da borda e o fundo reto do pote de cima pousa direto nele. Nada a usinar.

**Com a borda alta, a teca ganhou moldura.** A placa fica embutida 2,0 mm dentro de uma borda de
12 mm: a madeira aparece emoldurada pelo aro de PP, em vez de rente a ele. É ganho de desenho que
veio de graça com a referência.

**Dois cuidados que continuam sendo de madeira, não de plástico:**

1. **Movimentação com a umidade.** Teca maciça de 143 mm trabalha no sentido transversal. A
   profundidade do friso (0,60 mm) tem de ser especificada com essa movimentação, ou a compressão
   de 0,20 mm do filete some no inverno seco. É o item a medir no primeiro protótipo.
2. **Contato com alimento.** A face de baixo e o friso ficam voltados para dentro do pote. Selante
   ou óleo de grau alimentício, e a definição entra na ficha do produto, não no desenho.

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
| PEAD HA 7260 IF 20 | R$ 9,34/kg | 1,1 t | (descartado na revisão 8 — ver seção 6) |
| TPE Karinprene 45 | sem compra | — | aro de vedação, a recotar |

| Item | Peso | Resina |
|---|---|---|
| Corpo 600 ml | 52,9 g | R$ 0,59 |
| Corpo 1,2 L | 80,8 g | R$ 0,90 |
| Corpo 1,8 L | 113,8 g | R$ 1,27 |
| Corpo 2,4 L | 150,9 g | R$ 1,69 |
| **Tampa de PP com 2 travas** | **24,5 g** | R$ 0,23 |
| Tampa de teca (placa maciça 8 mm) | 59 g em teca | CNC, sem resina |
| **Filete de TPE (nas duas tampas)** | **0,9 g** | a cotar |

Só matéria-prima. Transformação entra pelo custo do PCP; a tampa de teca, pelo custo da WOOD.

**O que a revisão 8 custou em resina.** Os quatro corpos somam **398,4 g** contra 373,1 g na
revisão 7 — **+25,3 g, +6,8%**, ou R$ 0,28 por jogo de quatro. Vem todo do footprint maior, que
vem da borda oca (seção 3.2). A tampa, indo de PEAD para PP, sobe de R$ 0,21 para R$ 0,23.

---

## 8. Ferramental

Escopo na revisão 8: **4 moldes de corpo + 1 molde de tampa de PP + 1 molde de filete de TPE
= 6 ferramentas.** A tampa de teca não usa molde (CNC); o filete serve **as duas**.

**Os moldes de corpo continuam de duas placas, sem gaveta.** Descendo, a peça só estreita por fora
(153,7 → 148,9 → 142,5 → 138,5) e por dentro (146,1 → 140,2). O que entra de novo é a **nervura do
canal**: 1,20 mm de espessura por 8,6 mm de altura (7,2:1), contínua nos 466 mm de perímetro, na
cavidade. Pede raio no pé, saída própria e escape de ar na ponta — e é o item novo a orçar.

**A tampa ficou mais fácil que na revisão 7.** Saem as 6 abas com farpa de 1,85 mm; entram 2 travas
com gancho de 0,80 mm, livres nos três lados. Continua sendo extração por arraste com a aba
flexionando, mas com metade da contra-saída e um terço das feições.

Referências dos próprios orçamentos com a MR Plastic Mould (`AD_ORCAMENTO`, USD): corpo lixeira
12 L / 380 t = 36.900 · 284-U / 280 t = 20.100 · 214-U / 250 t = 18.900 · corpo 026 / 120 t = 6.300 ·
tampa 026-T / 90 t = 5.500 · **115/1 "potes modulares" 2 cav = 47.100 (aprovado)**.

Faixa a cotar: corpos 2 cav entre USD 25–45 mil cada (o 2,4 L no topo, por profundidade, polimento,
placa impulsora e agora a nervura do canal), tampa USD 15–20 mil, filete de TPE ~USD 8 mil.
**Ordem de grandeza USD 140–190 mil.**

---

## 9. Capacidade e ciclo

2 cavidades, 20 h úteis/dia, 22 dias. Ciclos um pouco maiores que na revisão 1 por causa da
extração da peça reta (mais tempo de resfriamento antes de arrancar do macho).

| Tamanho | Ciclo est. | pç/h | pç/mês | Resina |
|---|---|---|---|---|
| 600 ml | 17 s | 424 | 186 mil | 20,7 kg/h |
| 1,2 L | 21 s | 343 | 151 mil | 25,7 kg/h |
| 1,8 L | 25 s | 288 | 127 mil | 30,6 kg/h |
| 2,4 L | 29 s | 248 | 109 mil | 34,9 kg/h |

**Risco de preenchimento no 2,4 L:** L/t de 224 com parede de 1,40 mm. Viável com o PP de alta
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

1. **Aprovar o footprint de 153,7 × 87,8 mm** (era 148,6 × 84,9). Tudo abaixo depende disso: é o
   preço da borda oca, e se ele não passar, a borda volta a ser parede só — e a aresta de engate
   volta a não existir como material.
2. **Orçar a nervura do canal** (1,20 × 8,6 mm, contínua) com a ferramentaria. É a feição nova.
3. **Confirmar a saída de 0,5°** com o design — é o que separa "reto" de "aninha no frete".
4. **Preencher `AD_INJETORAFICHA`** (curso de abertura, curso e força de extração) para as 46 injetoras.
5. **Reabrir o Projeto 115** e renegociar com a MR Plastic Mould a partir da cotação aprovada.
6. **Recotar o TPE Karinprene 45** — agora com volume das duas tampas.
7. **Design da tampa**: a fenda que recorta as duas travas, a dobradiça sobre-centro (6.1.1), a
   saia decorativa da referência, e a bandeja-vertedor na versão de líquidos (6.4).
8. **Moldflow do 2,4 L** (L/t 224) e estudo de extração da peça reta com a nervura do canal.
9. **Try-out**: reservar INJ 32 (380 t) para o 2,4 L e INJ 25/24 (250 t) para o 1,8 L.
10. **Decidir o rótulo**: capacidade de borda (como está) ou re-resolver para capacidade útil (5.6).

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

`gera-3d.py` constrói o sólido a partir das mesmas cotas — **importadas de `calculo-modular.py`, não
copiadas** — e escreve **sete** STL em `stl/`: os quatro corpos, a placa de teca, a tampa de PP com
as duas travas e o filete de TPE. O visualizador interativo remonta a malha a partir da mesma
receita de anéis, bandas e tampos (`perfis.json`), então desenho e STL não divergem.

**Como o sólido é construído:** cada peça é uma casca fechada feita de seções de retângulo com
cantos arredondados empilhadas em alturas diferentes; bandas de quadriláteros ligam um anel ao
seguinte e tampos em leque fecham as pontas.

**Conferências que a malha faz sozinha** (saem no terminal a cada geração):

| Verificação | Resultado |
|---|---|
| Volume assinado positivo **e normais consistentes** nas sete peças | casca fechada e orientada para fora |
| **Seção conexa em toda a altura** nos quatro corpos | o material de cada nível encosta no do nível seguinte |
| Autoteste: o mesmo critério roda contra a geometria da **revisão 7** | tem de **reprovar** — e reprova |
| Cavidade × capacidade nominal | 599,6 / 1199,3 / 1799,1 / 2398,9 ml contra 600 / 1200 / 1800 / 2400 — dentro de **0,07%** |
| Peso da malha × `calculo-modular.py` | 52,9 / 80,8 / 113,8 / 150,9 g nos corpos, 59 g na teca, 24,5 g na tampa de PP |
| Malha do visualizador × STL do Python | `verifica-malha.js`: 0,00% nas sete peças |

**A verificação nova da revisão 8, e por que ela existe.** Na revisão 7 a boca media 144,95 mm e a
face externa do corpo, 141,55: o colar era um anel de material entre 144,95 e 148,55 **pairando
sobre um corpo que ia só até 141,55**. As duas superfícies horizontais em `z_col` se cancelavam, a
malha fechava, o volume assinado dava um número plausível e as normais estavam certas — e a peça
estava **em dois pedaços**. Impresso, o colar sairia solto.

Nem volume assinado nem normais pegam isso. `secao_conexa()` percorre a altura, monta a coroa (ou
as duas coroas, na faixa do canal) de cada nível e exige interseção radial com a do nível seguinte.
E, porque **verificação que nunca disparou não prova nada**, `autoteste_conexao()` reconstrói a
geometria da revisão 7 e exige que o mesmo critério a reprove; se não reprovar, o gerador sai com
erro.

**As três da revisão 7, que valem manter registradas:**

1. **O filete estava 0,40 mm aquém da boca.** A fórmula usava `FILETE_SOB − FRISO_PROF` em vez de
   `FILETE_D − FRISO_PROF`. Não vedaria nada, e nenhuma checagem de malha acusa.
2. **Metade das abas entrava espelhada no visualizador.** Espelhar inverte a mão: três abas com
   volume negativo cancelavam as outras três, e o total batia com o de uma tampa **sem aba nenhuma**.
3. **O STL saiu com Y para cima em vez de Z.** Volume assinado e normais são agnósticos a eixo e
   passaram os dois. Apareceu quando a área de contato com a mesa deu **zero**.

E a da revisão 6: a tampa saiu com o piso da bandeja invertido, malha **estanque**, volume assinado
plausível (17,5 g contra 27,6 reais). Foi ela que trouxe `normais_consistentes()`.

**O que o modelo não é.** É malha, não sólido CAD: serve para conferir encaixe, empilhamento e
volume, e para imprimir protótipo. **O molde precisa do CAD paramétrico do projetista.** Faltam no
modelo: a **fenda de ~1 mm** que recorta as duas travas nos três lados livres, a saia decorativa da
tampa que a referência mostra, e o furo e o entalhe do vertedor da seção 6.4. O filete está
desenhado na medida livre, e por isso invade 0,2 mm a boca no modelo — é justamente a interferência.

O corte do visualizador é onde se vê a borda oca: o flare, a perna de dentro, o canal, a saia livre
e o gancho da trava por baixo dela.

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

---

## 14. O STL de referência — o que foi medido e como

Arquivo: `REF_231.stl`, binário, **66 591 triângulos**, cabeçalho `STL generated by
ImageToStl.com`. Duas cascas separadas (busca em profundidade sobre as arestas): um **corpo** e uma
**tampa**, deslocados do zero — é um recorte de uma cena maior, não uma peça posicionada.

**A escala.** O arquivo não traz unidade útil: a caixa envolvente do corpo dá 12,9 × 19,8 × 5,6.
Medindo a **parede** em cortes horizontais, ela dá **0,113** constante. Parede de pote injetado em
PP é 1,0–1,4 mm, então a escala é **1:10** — e com ela todo o resto fecha: corpo de
129,1 × 197,6 × 56,3 mm, que é um pote de mantimento plausível.

**O que foi medido, e como:**

| Medida | Método | Resultado (×10) |
|---|---|---|
| parede | corte horizontal a meia altura, distância entre as duas coroas | 1,13 mm |
| altura da borda | varredura da meia-largura externa por altura; ela salta de 5,489 para 6,286 em y = 3,90 | 17,3 mm, 31% do pote |
| saliência da borda | mesma varredura, diferença entre o máximo da borda e o da parede | 9,6 mm/lado |
| perfil da borda | corte vertical no meio do lado comprido, contorno encadeado e simplificado (Douglas-Peucker) | topo chato 4,3 mm, raio 2,5 fora, 1,9 dentro |
| travas | vértices nos 0,25 mm mais externos em X, extensão em Z | 2 travas, 115,9 mm cada = 58% do comprimento |
| gancho | corte vertical passando pela trava | pega 19,5 mm abaixo do topo; rabo até 39 mm |

**O que a referência não é.** É modelo de aparência, não de fabricação: no corte, a borda aparece
como um **bloco maciço de 8,5 × 17,5 mm**. Nenhuma peça injetada tem seção assim — o que existe na
peça real é uma casca de parede constante. Por isso a revisão 8 tomou da referência a **forma e o
layout** (borda alta com face externa reta, topo chato com raios generosos, aresta de engate na
base, duas travas largas nos lados compridos) e construiu a **seção** do jeito que se injeta: casca
oca, parede constante, saia de ponta livre.

E foi justamente ter de construir a seção de verdade que revelou o erro da revisão 7 (seção 12).

Os scripts da medição ficam no diretório de trabalho da sessão, não no repositório — o que vale
aqui é a tabela acima e o `calculo-modular.py`, que é a fonte das cotas.

---

## 15. Terceira tampa — de correr, com gaveta e bico em U

**Estado: desenhada e conferida no cálculo, ainda sem 3D.** Três posições em aberto; escolhida
uma, sai STL e gcode. Memória: `calculo-correr.py` · desenhos: `desenhos/gera-svg-correr.py`.

O pedido: uma tampa de correr, com **outro aro de TPE**, e um bico na própria tampa **aberto em U,
não fechado em O**, para o líquido escorrer e a peça poder ser lavada. (A referência enviada,
`claude.ai/artifact/DwtbeRFf4zc1VgXNDiFngC`, não abriu — voltou "not found".)

### 15.1 O mecanismo

Tudo o que toca o pote vem da tampa de PP da revisão 8 e **não muda**: deck, plug, filete radial na
boca, duas travas de clipe e o piso da bandeja em z = −2,00. **O corpo não muda nos quatro moldes.**

```
bolso ....... rebaixo no piso da bandeja, fundo em z = -3,95
gaveta ...... painel de 1,80 mm; o TOPO dela e o plano modular
trilhos ..... 2, avancam 3,00 mm sobre a gaveta, folga de 0,25/lado
janela ...... furo no fundo do bolso; a gaveta corre por cima
2o aro ...... TPE de 1,60 mm, friso de 0,70 na face de BAIXO da gaveta
cunha ....... nos ultimos 2,50 mm de curso a gaveta desce 0,40 e so ai o aro encosta
bico ........ calha ABERTA em U, piso em z +1,20, paredes ate +4,00, labio de 0,40
```

Em repouso o bolso **drena pela janela de volta para dentro do pote** — o fundo do bolso é o ponto
mais baixo de todo o caminho. É por isso que o bico é em U e não em O: tubo fechado retém líquido e
não se lava.

### 15.2 O vertedouro — o que o corte revelou

O caminho do líquido tem dois trechos:

| | sobe | em | ângulo |
|---|---|---|---|
| fundo do bolso → piso da bandeja | 1,95 mm | 6,0 mm | 18° |
| **piso da bandeja → piso da calha** | **3,20 mm** | **2,8 mm** | **49°** |

O segundo **não tem como ser manso**. A calha não pode descer abaixo de z = 0 em cima da borda (ali
a tampa *pousa* no pote) nem cortar o friso do filete, que começa em −3,00 na face do plug. Se
cortasse, **a tampa deixaria de vedar mesmo com a gaveta fechada** — o furo estaria sempre aberto.
No primeiro traçado ela cortava; foi desenhar o corte que mostrou. Hoje é uma das conferências que
`calculo-correr.py` roda sozinho, com autoteste que quebra cada cota e exige que a conferência
reprove.

Consequência prática: verter pede inclinar o pote uns **50–60°**, e o último dedo de líquido não sai
pelo bico. Primeiro item do protótipo.

### 15.3 As três posições

| | A · lado curto | B · canto | C · lado comprido |
|---|---|---|---|
| Janela | 55 × 25 | 34 × 19 | 70 × 24 |
| **Vazão** | **1.367 mm²** | 638 mm² | **1.672 mm²** |
| Maior possível ali | 1.664 mm² | 828 mm² | 2.655 mm² |
| **Travessia de piso molhado** | **0 mm** | **17,8 mm** | **0 mm** |
| Bico | 28 mm num vão de 77 | 24 mm no canto | 28 mm num vão de 143 |
| Gaveta | 69 × 33 · 3,7 g | 48 × 27 · 2,1 g | 84 × 32 · 4,4 g |
| 2º aro | 171 mm · 0,38 g | 117 mm · 0,26 g | 199 mm · 0,44 g |
| Fechar | 2,7 kgf | 1,8 kgf | 3,1 kgf |
| Bate na trava de clipe? | não | não | **sim** |

**Eu apostava no canto e a conta derrubou.** A 45° o bolso transborda pela face comprida e tem de
recuar quase 18 mm — o líquido atravessa piso de bandeja antes de chegar ao bico, e o que atravessa
fica lá depois que se para de verter. Pelo mesmo motivo a janela cai para metade da de A.

**C tem a maior vazão e custa uma trava:** as duas travas de clipe são centradas nos lados
compridos, 89 mm cada, e o bico cai em cima de uma. Ela sai inteira ou vira duas menores, e a força
de fechamento daquele lado se reparte.

**A recomendação é A**: vazão suficiente, travessia zero, bico que converge, e fica na face que vai
de frente na prateleira.

### 15.4 O que a gaveta cobra

Ela está **no** plano modular, então o pote de cima pousa em parte sobre ela. Eu esperava que a
flecha decidisse a espessura — não decide: o vão curto da gaveta é curto (33 mm) e com o 2,4 L cheio
em cima a flecha dá **0,04 mm**. Quem pede os 1,80 mm é o friso do 2º aro, que come 0,70 mm da face
de baixo e deixa 1,10 de parede.

O que ela cobra de verdade é outra coisa: **não se corre a gaveta com pote carregado em cima** — o
atrito da carga trava o painel. Na prática o pote de vertedor é o do topo da pilha.

### 15.5 Ferramental

A linha vai de 5 para **6 peças injetadas**: 4 corpos + tampa de PP + tampa de correr, mais o filete
e o 2º aro. A gaveta é peça separada — molde próprio ou cavidade no mesmo bloco. O 2º aro é ⌀1,60
contra ⌀1,40 do filete: **perguntar ao fornecedor se sai do mesmo composto com outra matriz de
extrusão**, para não abrir contrato novo num TPE que já está parado há 4 anos no cadastro.
