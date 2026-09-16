# Organizador Dobrável P — especificação de projeto e 3D

**Status:** 3D fechado, pronto para cotação de ferramental · **Data:** 16/09/2026
**Projeto no ERP:** 100 "Relançar caixa dobrável" (Aprovado 04/10/2021)
**Modelo:** `cad/modelo3d.py` · **Memória de cálculo:** `calculo-dobravel.py`
**Arquivos:** `cad/P-*.step` (ferramentaria), `cad/P-*.stl`, `cad/0*-P.png`

Primeiro tamanho da família. O fundo e o padrão de furos aqui definidos servem
os três tamanhos — M e G herdam a mesma bandeja e o mesmo reticulado, mudando
só a altura dos painéis (por inserto de molde).

---

## 1. Correção do estudo anterior

O 3D derrubou dois números do `README.md` da pasta, e é melhor registrar do que
deixar a inconsistência:

| | Estudo (estimado) | 3D (sólido real) |
|---|---|---|
| Altura do painel | = altura externa | **= altura externa − 27 mm** (a saia do fundo ocupa a base) |
| Peso do P | 563 g | **436,7 g** |
| Peso do G | 689 g | **588,8 g** |
| Altura dobrada | 48 mm | **37 mm, igual nos três tamanhos** |
| Compactação do G | 4,5× | **6,3×** |
| Ferramental | USD 86,2 mil | **USD 114,6 mil** |
| Payback | 11 meses | **17,8 meses** |

**A causa foi contar a saia do fundo duas vezes**: o estudo calculava o painel
com a altura externa cheia, quando o painel começa no topo da saia. Isso inflava
peso e tonelagem. A memória de cálculo agora **importa a geometria do 3D** em vez
de manter estimativa própria em paralelo — a duplicação era a origem do erro.

Duas consequências mudam decisão:

1. **O tamanho P deixou de ser o problema comercial que o estudo apontou.** Com
   436,7 g (e não 563 g), sai a **R$ 1,61/L** contra os R$ 2,07/L estimados. O
   organizador rattan 16 L da casa está em R$ 1,40/L: o P fica competitivo, não
   dependente de kit.
2. **A seção 7.2 do estudo está errada.** Ela concluía que encolher o footprint
   para caber numa injetora de 380 t "quebra o 20 L por 8 mm". Com a altura de
   painel correta, **não quebra**: num footprint de 340 × 254 mm o painel do G
   ficaria com 205 mm contra um limite de dobra de 239 mm. Essa alternativa é
   viável e libera a INJ 34 — ver seção 7.3.

O ferramental subiu por dois motivos legítimos, não por erro: o frontal deixou
de ser comum (seção 3.3) e os insertos de altura carregam as próprias filas de
pinos de furo, então custam mais que bloco de shut-off simples.

---

## 2. Geometria

| Cota | Valor |
|---|---|
| Footprint externo | **345 × 285 mm** (comum aos 3 tamanhos) |
| Raio de canto externo | **R15** na saia |
| Altura externa / passo empilhado | **116 mm** = 2 × módulo de 58 mm |
| Cavidade interna | 331 × 271 mm |
| Volume nominal (até a borda) | **9,76 L** |
| Volume útil (até a borda do frontal) | 6,26 L |
| Altura dobrada | **37 mm** → compactação **3,1×** |
| Peso do conjunto | **436,7 g** |
| Peça | PP copolímero CP 141 (CODPROD 994), R$ 10,52/kg → **R$ 4,59 de resina** |

Regra modular preservada: **duas P empilhadas = 232 mm = uma G**.

---

## 3. As cinco peças

| Peça | Qtd | Dimensão | Peso | Furos | Molde |
|---|---|---|---|---|---|
| Fundo | 1 | 345 × 285 × 35 mm | **280,9 g** | — | próprio, **comum aos 3 tamanhos** |
| Lateral | 2 | 277 × 89 × 3 mm | 38,3 g | 60 | comum, **inserto de altura** por tamanho |
| Traseira | 1 | 337 × 89 × 3 mm | 45,8 g | 76 | comum, **inserto de altura** por tamanho |
| Frontal | 1 | 337 × 50 × 3 mm | 33,4 g | — (cego) | comum, **inserto de altura** por tamanho |
| | 5 | | **436,7 g** | **196** | 4 moldes + 3 jogos de inserto por tamanho |

O fundo é **64% do peso** do P. É a peça crítica do projeto e a primeira a ir
para try-out.

### 3.1 Fundo

Chapa **sólida** de 2,2 mm — como pedido, sem furo nenhum no fundo. Saia de
30 mm e 2,5 mm de parede, com R15 nos quatro cantos. Pé de 5 mm na face
inferior, com a mesma seção anelar do berço de empilhamento no topo da saia:
o pé da peça de cima **afunda 5 mm** no berço da de baixo, e é isso que faz o
passo empilhado ser exatamente a altura externa, sem sobra.

Dez orelhas de dobradiça na face interna da saia (3 por aresta longa, 2 por
aresta curta), com alojamento Ø6,8 mm para os pinos dos painéis.

### 3.2 Painéis

Placas planas de 3,0 mm de moldura e **1,8 mm de campo**, com moldura
perimetral de 12 mm. Aresta vertical em R8. São **embutidos** — 337 e 277 mm
contra uma boca de 340 × 280 mm — e é essa folga que permite que os quatro
tombem **para dentro da bandeja**, e não sobre o rim. Daí a altura dobrada de
37 mm ser a mesma nos três tamanhos: acima de 37 mm, quem manda é a saia do
fundo, não os painéis.

**Consequência estética a aprovar:** com painéis embutidos, o corpo fica 4 mm
recuado em relação à saia. Lê como plinto — a saia com R15 vira uma faixa
sólida na base, e o corpo vazado assenta sobre ela. Nos renders de pilha isso
aparece como uma cinta horizontal entre os módulos. É desenho, mas é escolha:
se o corpo tiver que ser rasante com a saia, os painéis pousam no rim e a
altura dobrada sobe de 37 para ~49 mm, derrubando a compactação do G de 6,3×
para 4,7×.

### 3.3 Frontal

**Cego, só com o recorte de pega** — igual à referência do vídeo, e é a decisão
certa: o frontal é a parede que mais sofre e a que recebe a mão.

Altura **proporcional**, 55% do painel (50 mm no P, 80 no M, 115 no G). O
estudo previa frontal comum de 70 mm para os três; não serve: 70 mm num painel
de 89 mm fecharia o acesso frontal do P, e num de 205 mm deixaria o G aberto
demais para o conteúdo não cair. Custa um jogo de inserto a mais por tamanho
(+USD 13 mil no total) e é o que faz o acesso frontal funcionar na família.

Vão de acesso com as peças empilhadas: **39 mm no P** (entre a borda do frontal
e o fundo da peça de cima).

---

## 4. O padrão de furos

Furos **redondos**, em reticulado quadrado de **passo 16 mm**, com o diâmetro
caindo de cima para baixo e **faixa cega no pé do painel**:

| Fila | Ø | |
|---|---|---|
| 1 (topo) | **16,0 mm** | |
| 2 | 13,0 mm | |
| 3 | 10,0 mm | |
| 4 | **7,0 mm** | |
| faixa cega | — | **16 mm** no pé do painel |

15 colunas no painel lateral, 19 no traseiro. Web de 16 mm entre a moldura
superior e a primeira fila.

**Por que a faixa do pé é cega** — e não é só estética: é onde o momento da
dobradiça e a carga de empilhamento se concentram. Furo ali seria concentrador
de tensão no pior lugar possível da peça.

**Por que o gradiente ajuda a estrutura:** a parede carrega mais esforço embaixo
(momento da dobradiça) e menos em cima. Diâmetro caindo para baixo põe material
onde a tensão está. O pedido estético e o cálculo estrutural apontam para o
mesmo lado, o que é raro e vale aproveitar.

**Nos outros tamanhos** o reticulado e a faixa cega são idênticos; só o número
de filas muda, e o Ø 16 → 7 se redistribui:

| | Filas | Diâmetros | Furos/conjunto |
|---|---|---|---|
| P | 4 | 16 / 13 / 10 / 7 | **196** |
| M | 8 | 16 → 7 em 8 passos | 343 |
| G | 11 | 16 → 7 em 11 passos | 539 |

### 4.1 O que isso custa no molde

Cada furo é um **shut-off** entre as metades do molde: 196 no P, 539 no G. Duas
consequências para a cotação:

1. **Furo redondo é o melhor caso.** O macho é um pino torneado que assenta em
   alojamento redondo — autocentrante, fácil de retificar e de polir. O rasgo
   oblongo da referência do vídeo tem quinas, que é onde nasce rebarba. Trocar
   rasgo por bolinha **simplifica** o ferramental.
2. **Exigir pinos postiços, não usinados na placa.** Com 539 shut-offs no G, um
   pino batido não pode condenar a placa inteira. Pinos substituíveis são a
   diferença entre uma manutenção de duas horas e um molde paralisado.

Os furos são passantes na direção de abertura do molde, e o painel é plano —
então **nenhuma gaveta, nenhum movimento lateral** em nenhum dos quatro painéis.

---

## 5. Dobradiça e ordem de dobra

Pino em berço (Ø6 no pino, Ø6,8 no alojamento), eixo a 31 mm do apoio, nós de
16 mm de comprimento — 3 nós nos painéis longos, 2 nos curtos.

**Ordem de dobra: laterais → traseiro → frontal.** No P os quatro painéis
tombam lado a lado sem se sobrepor (2 × 89 = 178 mm contra 331 mm de cavidade;
89 + 50 = 139 mm contra 271 mm). No M e no G os laterais se sobrepõem, e aí os
eixos de dobradiça precisam ser **escalonados em ~3,8 mm por camada** para cada
painel assentar sobre o anterior. No P o escalonamento não é necessário, mas o
fundo é comum aos três — então **as orelhas já têm que sair escalonadas no molde
do fundo**, ou o M e o G não fecham. Isso tem que entrar na cotação agora, não
depois.

---

## 6. Cantos arredondados: o que dá e o que não dá

O pedido era canto arredondado. O 3D mostra o limite com clare:

**O que dá.** R15 contínuo na saia do fundo — os 35 mm de base do produto, que
é a parte que a mão toca e o olho lê primeiro. Mais R8 na aresta vertical de
cada painel, o que faz o encontro de canto ler como junta desenhada.

**O que não dá.** Raio contínuo subindo pelo corpo inteiro. Painel que dobra
plano **não pode ter curvatura no plano horizontal** — painel curvo não achata.
E coluna de canto solidária ao fundo, subindo até a borda, resolveria o visual
mas **teria altura diferente por tamanho**: o fundo deixaria de ser comum e
passaríamos de 1 para 3 moldes de fundo, ~USD 60 mil a mais.

**O que sobra como caminho, se o canto cheio for requisito:** coluna de canto
como **quinta peça**, encaixada na saia, com inserto de altura — mesma lógica
dos painéis. Custaria um molde (~USD 18 mil) e 4 peças a mais na montagem por
unidade. Não recomendo na primeira fase: o plinto com R15 já entrega a leitura
de canto macio, e o try-out vai dizer se o corpo reto incomoda.

---

## 7. Injeção

### 7.1 Alocação do P no parque (`TPRWCP` + `TPRCAP`)

Fechamento a 0,32 t/cm² com câmara quente valvulada, + 10% de canal, limitado a
80% da capacidade da máquina. A área dos furos **não** conta no fechamento.

| Peça | Cav. | Fechamento | Máquina | Uso | Injetoras |
|---|---|---|---|---|---|
| Fundo | 1 | 346 t | 600 t | 58% | **INJ 34** |
| Lateral P | 2 | 126 t | 160 t | 79% | INJ 7–12, 36, 40, 41 |
| Traseira P | 2 | 151 t | 200 t | 75% | INJ 1–6, 19–22, 35, 37 |
| Frontal P | 2 | 119 t | 150 t | 79% | INJ 42, 43 |

Só o fundo precisa de máquina grande. A 21.500 unidades/ano e ciclo estimado de
28 s com 1 cavidade, o fundo ocupa **~170 h/ano da INJ 34** — 2% de um turno
único. Não há disputa de capacidade; a questão é só de logística de troca de
molde (40 min de setup, `TPRWCP.TEMPOSETUP`).

Ciclos são **estimativa** (28 s no fundo a 2,2 mm; 20 s nos painéis a 1,8 mm),
a confirmar no try-out.

### 7.2 Bloqueio de dado, de novo

O bloco do molde do fundo tem 620 × 540 mm. `AD_INJETORAFICHA` continua com um
registro e todos os campos nulos, então **a distância entre colunas da INJ 34
não é conferível no sistema** — tem que ser medida em campo antes do pedido.
É o único item que impede fechar a cotação do molde mais caro.

### 7.3 A alternativa que a correção reabriu

Com a altura de painel correta, o footprint menor **volta a ser viável**:

| | 345 × 285 (atual) | 340 × 254 (alternativa) |
|---|---|---|
| Fechamento do fundo | 346 t | 303 t |
| Máquina do fundo | 600 t (INJ 34), 58% | **380 t (INJ 31/32/33), 80%** |
| Painel do G | 205 mm | 205 mm |
| Limite de dobra | 265 mm | 239 mm — passa |
| Volume do G | 20,16 L | ~19,9 L |

A alternativa libera a única 600 t da casa e põe o fundo em três máquinas em vez
de uma. O preço é rodar a **80% do fechamento**, sem folga, num coeficiente de
pressão (0,32 t/cm²) que é premissa e só se confirma no try-out — e o molde do
fundo é o primeiro e mais caro da família.

**Recomendação: manter 345 × 285.** A INJ 34 tem folga documentada e o risco de
descobrir no try-out que o fundo não fecha na 380 t é caro demais para o ganho.
Mas a alternativa merece uma pergunta à ferramentaria na cotação: se a MR
Plastic Mould garantir 0,30 t/cm² com valvulado sequencial, a conta muda.

---

## 8. Ferramental

| Molde | Cav. | Bloco | Aço | FOB USD | |
|---|---|---|---|---|---|
| Fundo | 1 | 620 × 540 × 520 | 1.367 kg | **30.133** | câmara quente 4 bicos valvulados |
| Lateral | 2 | 700 × 460 × 460 | 1.163 kg | **29.278** | + 2 jogos de inserto (M e G) |
| Traseira | 2 | 700 × 460 × 460 | 1.163 kg | **29.278** | + 2 jogos de inserto (M e G) |
| Frontal | 2 | 700 × 420 × 400 | 923 kg | **25.924** | + 2 jogos de inserto (M e G) |
| | | | | **114.614** | família inteira |

A **USD 14/kg de bloco**, que é a média dos três moldes comparáveis da casa
(283-C a 12,3; 284-U a 12,9; 214-U a 16,8 — `AD_MOLDE` + `AD_ORCAMENTO`, todos
com a MR Plastic Mould).

**Só do P: USD 114,6 mil menos os 6 jogos de inserto (USD 39 mil) = USD 75,6 mil**
são os 4 moldes base, que o P paga e o M e o G herdam. Rodar só o P primeiro
custa os 4 moldes; cada tamanho seguinte custa 3 jogos de inserto (~USD 19,5 mil).

Isso responde à ordem que você pediu — **P primeiro, M e G depois** é barato:
a segunda e a terceira litragem entram por inserto, não por molde novo.

Câmbio e nacionalização seguem **premissa** (R$ 5,45/USD, +30%), não dado do
ERP. Payback da família: **17,8 meses** a 21.500 un/ano por tamanho.

---

## 9. Custo e preço

| | Peso | Resina | Custo | Preço | Margem | R$/L |
|---|---|---|---|---|---|---|
| **P** | 436,7 g | R$ 4,59 | **R$ 8,52** | **R$ 15,72** | 45,8% | **1,61** |
| M | 514,8 g | R$ 5,42 | R$ 10,04 | R$ 18,53 | 45,8% | 1,24 |
| G | 588,8 g | R$ 6,19 | R$ 11,48 | R$ 21,20 | 45,8% | 1,05 |
| Kit | 1.540 g | R$ 16,20 | R$ 30,04 | R$ 55,45 | 45,8% | — |

A R$ 19,50/kg de custo e R$ 36,00/kg de preço, ambos da faixa medida em seis
produtos vivos da categoria (`TGFCUS` × `TGFPRO`, `TGFITE`). **A margem de
45,8% é teto**: não inclui a montagem das 5 peças, que roda nos centros MONTAGEM
(CODWCP 78, 79) e precisa de cronoanálise.

Referências da casa: organizadora rattan 16 L a R$ 22,37 (R$ 1,40/L); flat
10,35 L a R$ 12,54 (R$ 1,21/L); gaveteiro modular 8,2 L a R$ 19,77.

## 10. Frete — a tese do produto

| | Montado | Peso cubado | Dobrado | Peso cubado | Frete | Pallet montado | Pallet dobrado |
|---|---|---|---|---|---|---|---|
| P | 11,41 dm³ | 3,42 kg | 3,64 dm³ | 1,09 kg | **3,1× menor** | 135 un | 432 un |
| M | 17,11 dm³ | 5,13 kg | 3,64 dm³ | 1,09 kg | **4,7× menor** | 90 un | 432 un |
| G | 22,81 dm³ | 6,84 kg | 3,64 dm³ | 1,09 kg | **6,3× menor** | 63 un | 432 un |

Fator de cubagem de 300 kg/m³; pallet PBR com 1.800 mm úteis. Como os três
dobram na mesma altura de 37 mm, **um pallet leva 432 peças de qualquer
tamanho** — e a caixa master é a mesma para a família inteira, o que simplifica
embalagem e kit misto.

---

## 11. O que falta decidir

| Item | Quem decide | Trava o quê |
|---|---|---|
| Medir distância entre colunas da INJ 34 | Produção | Cotação do molde do fundo |
| Confirmar 0,32 t/cm² com valvulado | MR Plastic Mould | Escolha do footprint (7.3) |
| Corpo embutido (plinto) vs rasante | Design/comercial | Altura dobrada: 37 ou 49 mm (3.2) |
| Canto cheio exige 5ª peça? | Design | +USD 18 mil e 4 peças/un (6) |
| Cronoanálise da montagem | Produção | Margem real (9) |
| Câmbio e nacionalização do molde | Fiscal | Payback (8) |
| Pinos de furo postiços | MR Plastic Mould | Manutenção do molde (4.1) |
| Orelhas escalonadas no fundo | Ferramentaria | **Se esquecer, M e G não dobram** (5) |

## 12. Arquivos

```
cad/P-fundo.step      P-lateral.step    P-traseira.step   P-frontal.step
cad/P-conjunto.step   (montado)
cad/P-*.stl           (mesmas peças em malha)
cad/01-montado-P.png  02-frontal-P.png  03-dobrado-P.png
cad/04-pilha-P.png    05-explodido-P.png
cad/modelo3d.py       parametrico: python3 modelo3d.py [P|M|G]
cad/render.py         rasterizador das vistas
calculo-dobravel.py   tonelagem, cubagem, custo e ferramental dos 3 tamanhos
```
