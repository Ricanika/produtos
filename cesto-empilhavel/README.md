# Cesto Mini Organizador Empilhável e Encaixável — peça única em PP

**Status:** 3D fechado, pronto para cotação de ferramental · **Data:** 16/09/2026
**Referência:** STL enviado em 16/09 (bin de 150 × 100 × 80 mm, 192 faces) + anúncio
"10 peças Cesto Mini Organizador Empilhável" (MLBU4092388469) + fotos cotadas
(Mercado Livre MLBU4092388469) + fotos cotadas enviadas em 16/09/2026
**Modelo:** `cad/modelo3d.py` · **Economia:** `economia.py` · **Arquivos:** `cad/cesto.step`

**Forma adaptada do STL de referência, com o vazado em furos redondos.** A silhueta lateral foi
**medida no próprio sólido** do STL, não interpretada de foto: é uma caixa com **dois chanfros a
45°** na frente — um no topo e um no pé — deixando uma face frontal curta centrada na meia-altura.
Escalada para a nossa altura, e com os raios da lateral trabalhados conforme pedido. Peça única
injetada: sem dobradiça, sem painel, sem montagem.

> **Correção de rumo.** As versões anteriores deste arquivo descreviam uma *sela* no topo da
> lateral e depois uma *aba em gancho* avançando à frente. As duas eram minha leitura das fotos e
> as duas estavam erradas — o STL mostrou que a forma é bem mais simples. O histórico está nos
> commits; o que vale é o que está abaixo.

> **Substitui o estudo da caixa dobrável** em [`../cesto-dobravel/`](../cesto-dobravel/), que
> partiu de um vídeo de referência com o produto errado. Daquele estudo seguem valendo e foram
> reaproveitados aqui: o parque de injeção e as tonelagens, o levantamento de resinas, o modelo
> de custo por kg da categoria e os bloqueios de dado do ERP.

---

## 1. Veredito

| Requisito | Situação |
|---|---|
| Peça única empilhável e encaixável | **Viável** — é a arquitetura mais simples possível: 1 peça, 1 molde, zero montagem |
| Forma da referência | **Medida no STL, não interpretada** — chanfros a 45°: 52 mm no topo, 36 mm no pé, face frontal de 42 mm (seção 2.2) |
| Furos redondos em gradiente | **Resolvido** — 4 bandas, Ø 15 → 6 mm, passo 21 mm, 68 furos, faixa cega de 40 mm |
| Fundo sólido | **Atendido** — chapa de 2,0 mm sem furo |
| Pé discreto | **Resolvido** — 4 pezinhos ocos sob a chapa, recuados 2 mm da borda; a chapa faz aba (seção 4.1) |
| Empilhar, encaixar **e** acoplar | **Os três, medidos no sólido** — empilha 130,0 · encaixa 102,7 na mesma orientação · acopla com trava, 0,00 mm³ de interferência na cena (seções 4.2.1 e 4.2.2) |
| Acoplar lateralmente | **Resolvido dentro das paredes de empilhamento** — cauda de andorinha vertical de 1,4 mm, sem gaveta, trava puxando de lado (seção 4.2.2) |
| Encaixar para reduzir volume | **Medido no sólido: passo de 55,5 mm**, 630 mm para 10 peças. Exclusivo do empilhamento a 130 mm — ver seção 4.2 |
| Injeção no parque atual | **1 cavidade numa 200 t (76%)** — a casa tem **12 máquinas** dessa classe |
| Ferramental | **USD 19,5 mil FOB**, 1 molde — por analogia direta com dois moldes da casa |
| Payback | **~6,8 meses** a 150 mil un/ano em PP virgem (5,4 com moído), com o molde estimado por cima |
| Preço do anúncio de referência | **Não obtido** — o proxy desta sessão bloqueia o Mercado Livre (seção 6) |

O produto é uma **commodity de volume**: contribuição de ~R$ 2,20 por peça, então a conta fecha
por quantidade, não por margem unitária. Isso muda o critério de decisão em relação à caixa
dobrável: lá o risco era o ferramental caro; aqui o ferramental é barato (USD 19,5 mil, ~14% do
que custaria a família dobrável) e **o risco é o volume de venda**.

---

## 2. Geometria

| Cota | Valor |
|---|---|
| Boca (rim) | **215 × 200 mm** |
| Base | 199,1 × 184,1 mm |
| Altura | **130 mm** |
| Envelope real | **215 × 197 × 130 mm** |
| Chanfros da frente | **52 mm no topo · 36 mm no pé**, ambos a 45° |
| Face frontal | **42 mm** (o chanfro do pé foi reduzido para devolver volume) |
| Raios trabalhados | **R20** nas duas pontas dos chanfros · **R12** nas duas quinas da face frontal |
| Saída de molde | **3,5° por lado** — é ela que permite o encaixe |
| Parede / fundo / rim | 1,4 / 2,0 / 3,2 mm |
| Pé | **4 pezinhos ocos** sob a chapa, que flutua 5 mm acima do piso |
| Capacidade | **4,46 L** |
| Peso | **170,8 g** (versão final, com estrutura e acoplamento) |
| Área projetada | 430 cm² |

### 2.2 A silhueta, medida no STL de referência

O STL tem 150 × 100 × 80 mm. Extraindo os vértices do plano lateral:

| Ponto | y | z |
|---|---|---|
| fundo, atrás | −80 | 0 |
| costas, no alto | −80 | 80 |
| fim do topo | +38 | 80 |
| topo da face frontal | +70 | 48 |
| pé da face frontal | +70 | 32 |
| fim do chanfro do pé | +38 | 0 |

Ou seja: o topo corre **78,7% da profundidade**, os chanfros têm **32 mm a 45° exatos**, e a face
frontal tem **16 mm centrada na meia-altura** — 40% / 20% / 40% da altura. Escalado para a nossa
altura de 130 mm: **52 / 26 / 52**, que fecham exatos.

No modelo isso é **um perfil 2D único** usado como interseção (`silhueta()` em `cad/modelo3d.py`),
então a forma tem um só lugar para mexer — e é nele que os fillets R20/R12 entram.

### 2.1 Peso

155,4 g para 4,50 L, contra o **Cesto Organizador Vime 7 L (047) da casa, que faz 7 L com 213 g**.
A **32,9 g/L**, a peça fica na mesma eficiência do 047 (30,4 g/L) — sinal de que a parede de
1,4 mm está coerente com a prática da casa. O peso caiu de 230 para 155 g ao trocar a forma: os
chanfros tiram material e a aba em gancho da versão anterior saiu inteira.

Não vejo mais gordura óbvia para cortar. Se o try-out pedir, o caminho é parede de 1,2 mm na
banda superior, onde não há carga de empilhamento.

---

## 3. O vazado

Furos **redondos** em 4 bandas horizontais de cota Z fixa, com o diâmetro caindo de cima para
baixo — é a alteração pedida em relação ao vazado de cortes verticais da referência.

| Banda | Cota | Ø |
|---|---|---|
| 1 (topo) | z 111 mm | **15,0 mm** |
| 2 | z 90 mm | 12,0 mm |
| 3 | z 69 mm | 9,0 mm |
| 4 | z 48 mm | **6,0 mm** |
| faixa cega | z 0 a 40 mm | — |

Passo do retículado: **21 mm**, o que dá 6 mm de web na fileira de cima e 15 mm na de baixo.
Total: **68 furos**. Fundo **sólido**.

Duas coisas que o modelo aprendeu na marra e ficaram como regra:

1. **Passo ≥ Ø do topo + 6 mm.** A 15 mm de passo com Ø14, os furos da fileira de cima se fundiam
   numa fileira contínua — 1 mm de web não é furo nem parede.
2. **Colunas calculadas uma vez**, com a margem do maior diâmetro, e usadas por todas as fileiras.
   Calculando por fileira, a de Ø15 saía com 5 colunas e a de Ø6 com 7, e o retículado desalinhava.

Nas laterais as bandas são recortadas pela silhueta, com 9 mm de folga — então o campo de furos
acompanha o chanfro do topo.

### 3.1 O que isso custa no molde

Os furos estão nas **paredes laterais e de fundo**, perpendiculares à direção de abertura. Eles são
formados por **encosto (shut-off) entre macho e cavidade** — o macho tem pastilhas que tocam a
cavidade. É a prática padrão em caixa vazada e **não exige gaveta nem movimento lateral**: a peça
sai do macho na direção Z e a saída de 4° libera as bordas do furo.

Duas consequências para a cotação:

1. **Furo redondo é o melhor caso de shut-off** — pastilha torneada, autocentrante, fácil de
   retificar e polir. O rasgo oblongo da referência tem quinas, que é onde nasce rebarba. A
   mudança que você pediu **simplifica** o ferramental.
2. **Pedir pastilhas postiças, não usinadas no macho.** Com 92 encostos, uma pastilha batida não
   pode condenar o macho inteiro.

---

## 4. Empilhar e encaixar — os dois modos

### 4.1 Empilhado

#### O pé: 4 pezinhos sob a chapa

A chapa do fundo fica **5 mm acima do piso** e quem apoia são **4 pezinhos
ocos de 13 × 20 e 13 × 26 mm**, recuados 2 mm da borda da chapa. A chapa faz
aba sobre eles: de fora não se vê pé — vê-se a chapa e uma sombra de 5 mm.

Eles substituem a saia corrida de 6 mm que estava aqui antes, e a troca é boa
nos dois sentidos: a peça ficou **mais leve** (162,6 contra 167,6 g) e a saia
era justamente o que impedia o encaixe (seção 4.2).

São ocos e abertos embaixo — pino na cavidade, na direção de abertura. Parede
de 1,4 mm, como o resto da peça: nada de bloco maciço, que marcaria a face.

#### O encaixe do pé traseiro

Empilhadas, as peças precisam de um batente, senão a de cima corre — e corre
justamente para a frente, que é onde o chanfro abre. O **pé traseiro** resolve:
o berço do rim que o recebe ganha **duas paredes de 2 × 2,5 mm** formando um
soquete, com 0,6 mm de folga por lado. O pé cai dentro e a pilha não corre nem
para a frente nem para o lado. O berço tem 4 mm de espessura e o topo rasante a
z = 130, então o passo empilhado fica **exatamente 130 mm** — medido no sólido.

### 4.2 Encaixado — e o achado: empilhar a 130 mm e encaixar são exclusivos

**Correção.** Eu vinha citando 601 mm para 10 peças encaixadas sem nunca ter
medido. Medindo no sólido — busca binária do menor deslocamento vertical em que
duas cópias não se interpenetram (`cad/empilha.py`) — o resultado foi **130,0 mm
nas duas orientações**: a peça não encaixava. A causa eram os berços que eu mesmo
havia posto no rim quando troquei o pé: eles avançam 10 mm para dentro, deixando
94,3 mm de abertura livre contra 99,55 mm de meia-largura da base.

Tirando o que avança para dentro do rim, o passo encaixado medido é **55,5 mm**
— 10 peças em **630 mm** de caixa.

E aqui está o problema de fundo, que não é de acabamento:

| | precisa | consequência |
|---|---|---|
| Empilhar a 130 mm | algo segurando a peça de cima **dentro** da boca da de baixo | fecha a passagem |
| Encaixar | **nada** dentro da boca | não há batente |

A chapa da peça de cima tem 99,9 mm de meia-largura; o soquete deixa 82,5 mm de
abertura livre. Não passa. E **girar 180° não salva**: os pezinhos estão em
posições assimétricas em y e se desviam dos soquetes, mas a chapa e a parede
passam por todo y. Medido: 127,6 mm girada.

A raiz é a conicidade. Para encaixar é preciso que a base seja menor que a boca
livre (base + 2 × 3,2 ≤ boca); para empilhar sobre o rim é preciso que a base
alcance a boca livre (base ≥ boca − 2 × 3,2). As duas condições se excluem, e
nenhuma feição resolve isso porque a saliência que alcançaria o rim seria
contra-saída (mesma regra da seção 4.4).

As duas versões estão modeladas e medidas:

| | N · só pezinhos | P · pezinhos + soquetes |
|---|---|---|
| Passo medido | **55,5 mm** (encaixa) | **130,0 mm** (empilha) |
| 10 peças na caixa | **630 mm** | 1.300 mm |
| Peso | **162,6 g** | 172,5 g |
| Capacidade | 4,46 L | 4,46 L |

**Recomendo a N.** O pedido foi "empilhar para dar cubagem e acoplar para usar":
a cubagem vem do encaixe (metade da caixa) e o uso vem do acoplamento lateral da
seção 4.4. E a N não deixa de empilhar — empilha a 55,5 mm, com o chanfro de topo
abrindo a frente de cada nível. O que ela não faz é empilhar a 130 mm.

Se os 130 mm forem obrigatórios, há um caminho com peça a mais: rim só com berço
raso e **4 espaçadores** de encaixar, que vão na embalagem e só entram quando o
cliente quer torre. Custa um 2º molde pequeno.

### 4.2.1 A solução: estrutura na borda (ideia do cliente)

O cliente mandou fotos de um cesto laranja em produção e a leitura dele estava
certa: **uma parede que sai da borda superior, por fora do rim, e uma nervura
externa com o pé na diagonal** que desce pela parede e apoia em cima dessa
parede.

Isso derruba o meu argumento da seção 4.2, e por um motivo que eu havia
invertido: eu tinha posto os berços **por dentro** do rim, no caminho da peça de
cima. Medindo onde a peça de cima realmente passa no encaixe mais profundo, a
parede dela nunca chega a 107,5 mm — na cota do rim ela está em x 102,7…104,1.
**Da borda para fora ninguém passa.** É lá que a estrutura tem de morar.

O mecanismo é de duas posições, e a assimetria é de propósito:

- as nervuras e as paredes ficam nas **mesmas posições em y** (−46…−24 e
  60…82, duas por lateral), e essas posições são assimétricas em relação a
  y = 0;
- **mesma orientação** → nervura encontra parede → **empilha a 130 mm**, com o
  chanfro sempre na frente;
- **girada 180°** → a nervura cai onde não há parede → **encaixa**.

Cotas resolvidas do sistema de restrições (parede de altura h = z0 = 10 mm para
o passo dar exatamente ALT):

| | |
|---|---|
| Face interna da parede da borda | 101,70 mm (folga de 0,4 da peça de cima) |
| Face externa da nervura no seu pé | 103,30 mm — **apoio de 1,6 mm** |
| Inclinação dessa face | 0,015 (0,86°) |
| Pé da nervura / altura da parede | 10 / 10 mm |
| Diagonal de entrada | 16 mm |

A nervura **nunca passa dos 107,5 mm** da boca: ela é um reforço que preenche
parte do vazio da conicidade, invisível em planta. O envelope só cresce por
causa da parede da borda: 216,8 mm.

**Medido no sólido:** empilhado **130,0 mm**, encaixado **102,7 mm**.

#### O preço, e ele é exato

O encaixe cai de 55,5 para 102,7 mm. A razão é uma conta de uma linha: cada
milímetro que qualquer coisa avança para fora na peça de cima custa
**1/tan 3,5° = 16,3 mm** de profundidade de encaixe, e o apoio precisa de
~4 mm (folga + apoio + a espessura da própria parede). Generalizando, com a
faixa do rim de 3,2 mm e apoio b:

> 2 · tan θ · d ≤ 130 · tan θ − 3,2 − b  →  **d ≤ 65 − (3,2 + b) / (2 tan θ)**

| apoio b | passo encaixado | 10 peças |
|---|---|---|
| 1,0 mm | 99,3 mm | 1.024 mm |
| **1,6 mm** | **102,7 mm (medido)** | **1.054 mm** |
| 2,5 mm | 111,6 mm | 1.134 mm |

E a saída de molde é a única alavanca real: a 5° o passo encaixado cairia para
91,9 mm e a 7° para 84,1 mm — ao custo de a base ir de 199 para 183 mm.

#### Encaixar na mesma orientação — e a regra que decide

O cliente pediu que na versão **encaixada** as peças entrem uma na outra
**todas no mesmo sentido**, sem inverter. Isso é atendido invertendo a
atribuição do mecanismo: as **nervuras** ficam em `NERV_Y` e as **paredes** em
`PAR_Y = −NERV_Y`, com os intervalos de |y| disjuntos. Medido:

| | mesma orientação | girada 180° |
|---|---|---|
| Antes (Q) | empilha 130,0 mm | encaixa 102,7 mm |
| **Agora (Q′)** | **encaixa 102,7 mm** | empilha 129,9 mm |

As cotas são as mesmas — só troca qual dos dois modos é o girado. E isso é uma
regra, não uma limitação do desenho: **trocar entre encaixar e empilhar exige
duas posições, e numa peça injetada de uma só vez a única segunda posição é
girar 180°.** Um dos dois modos vai ser o girado.

O preço da Q′ é que a **pilha** passa a ser a girada, e aí o chanfro alterna
frente/trás a cada nível — perde o acesso frontal em metade dos níveis. Duas
saídas, se isso não servir:

1. **Silhueta simétrica frente/trás** (chanfro nas duas pontas): girar deixa de
   se ver. Custa ~0,4 L de capacidade e aperta o rim, que já divide espaço com a
   canaleta. O acoplamento então tem de virar **hermafrodita** (macho na metade
   da frente e fêmea na de trás, espelhado) — esse arranjo é invariante a 180°,
   o atual não é.
2. **Abrir mão da pilha de 130 mm** e ficar na N: encaixa a 55,5 mm na mesma
   orientação, 630 mm para 10 peças, nada no caminho.

Na Q′ a canaleta de acoplamento também encurta de 80 para **36 mm** (y 48…84):
a estrutura de empilhamento ocupa o rim da lateral.

### 4.2.2 Empilhar E acoplar: o acoplamento dentro das paredes

Com a estrutura de empilhamento ocupando o rim da lateral, sobravam 36 mm para
a canaleta de acoplamento — e o produto deixava de acoplar de verdade. A saída
não foi disputar espaço: **o acoplamento foi morar dentro da própria estrutura.**

É onde duas peças lado a lado se tocam: as paredes da borda ficam face a face
no plano x = 107,5. Na face externa de cada parede entra uma **cauda de
andorinha vertical**:

| | |
|---|---|
| Avanço do macho | **1,4 mm** (pescoço de 0,5 + cabeça de 0,9) |
| Largura do pescoço / cabeça | 5,0 / 9,0 mm |
| Folga | 0,35 mm por lado |
| Altura | os 10 mm da parede, prismática em z |

Três propriedades que fazem isso funcionar:

1. **Prismática em z, aberta no topo** — sai na direção de abertura do molde.
   Nenhuma gaveta, mesmo sendo uma contra-saída em x.
2. **Hermafrodita e invariante a 180°** — numa lateral a 1ª parede é macho e a
   2ª é fêmea, espelhado na outra. Girando a peça, macho e fêmea trocam de lado
   juntos, então a **pilha girada continua acoplando nível a nível**.
3. **Trava por descida.** A cabeça de 9 mm não passa pela boca de 5,7 mm.

#### Medido no sólido

| | |
|---|---|
| Empilha (girada 180°) | **130,0 mm** |
| Encaixa (mesma orientação) | **102,7 mm** — 10 peças em 1.054 mm |
| Acopla, nível não girado | 0,00 mm³ de interferência |
| Acopla, nível girado | 0,00 mm³ |
| **Trava lateral** | bloqueia de **0,2 a 1,2 mm** de afastamento |
| Solta levantando | 35 mm |
| **Cena de 2 colunas × 3 níveis** | **0,00 mm³** |
| Peso / capacidade | **170,8 g** / 4,46 L |
| Envelope | 217,8 × 197 × 140 mm |

A varredura do afastamento lateral é o que prova a trava: a peça teria de passar
por todas as posições de 0,2 a 1,2 mm para separar, e todas elas
interpenetram. Puxar de lado não abre.

A profundidade da cauda é o ajuste fino entre trava e usabilidade — medido:

| avanço | trava até | solta levantando |
|---|---|---|
| 1,0 mm | 0,8 mm | 25 mm |
| **1,4 mm** | **1,2 mm** | **35 mm** |
| 2,0 mm | 1,8 mm | 45 mm |

Escolhido 1,4 mm. A canaleta da opção D no rim foi **removida**: ela não é mais
necessária e liberou a faixa do rim.

#### As três versões, medidas

| | N · só pezinhos | P · soquete interno | **Q′ · estrutura na borda** |
|---|---|---|---|
| Empilha | 55,5 mm | **130,0 mm** | **129,9 mm** (girada) |
| Encaixa | **55,5 mm** (mesma orient.) | não | 102,7 mm (mesma orient.) |
| 10 peças na caixa | **630 mm** | 1.300 mm | 1.054 mm |
| Peso | **162,6 g** | 172,5 g | 172,8 g |
| Canaleta de acoplamento | 80 mm | 80 mm | 36 mm |
| Fundo / molde | sólido / sem gaveta | sólido / sem gaveta | sólido / sem gaveta |

A Q é a única que faz as duas coisas. A escolha real é entre **Q** (os dois
modos, caixa de 1.054 mm) e **N** (só encaixe, caixa de 630 mm).

### 4.3 Acoplado — as três canaletas

O pedido foi uma **canaleta de ponta a ponta na lateral, macho de um lado e
fêmea do outro**. A direção dela não é livre: a saída de 3,5° abre a lateral de
**0 mm no rim a 15,9 mm na base**, então uma canaleta *vertical* de ponta a
ponta teria de ser uma cunha de 7,95 mm por lado no pé — o que leva a peça a
215 mm de largura já na base contra 208,6 mm de boca livre, e **mata o
encaixe** (as 10 peças sairiam de 601 para 1.300 mm de caixa). No rim a fresta
vale zero e em z=113 vale 2,08 mm: a canaleta é **horizontal e mora na faixa de
18 mm sob o rim**.

Dentro dessa faixa há um segundo limite, e é ele que gera as três opções: **um
macho corrido exige uma fêmea corrida**, e rebaixo horizontal na lateral é
contra-saída. A fêmea só sai de graça se for **passante** (shut-off, igual aos
68 furos) — e uma fêmea passante corrida significa rim interrompido.

| | A · trilho corrido | B · trilho embutido | C · canaleta aparente |
|---|---|---|---|
| Macho | trilho corrido de 132 mm, 7,5 mm saliente, gancho corrido | lingueta corrida: pescoço de 6 mm + cabeça de 10 mm | 2 abas de 40 × 18, 7,5 mm salientes, gancho de 2,5 × 6 |
| Fêmea | rim rebaixado 18 mm nos 132 mm | canaleta corrida: boca de 4 mm + bolso de 3,9 mm | 2 janelas de 42 × 18, abertas no topo do rim |
| Trava | extensão toda, em X | extensão toda, em X e em Z | 2 × 40 mm, em X |
| Montagem | desce | desliza pela frente | desce |
| Junta entre as peças | rims encostados | **8,7 mm** | rims encostados |
| Molde | sem gaveta | **2 gavetas laterais** (~USD 3 mil) | sem gaveta |
| Peso | 183,0 g | 187,8 g | **177,4 g** |
| Interferência medida | 0 mm³ | 0 mm³ | 0 mm³ |

A interferência é medida por booleano entre as duas peças acopladas, no sólido.
Zero nas três — e não era assim na primeira rodada: A e C devolviam 1 mm de
parede dentro da janela que acabavam de abrir, e o B era erro de concepção
(os dois lados avançavam um contra o outro, sem nada que recebesse a lingueta).

**As três custam a faixa.** Com acoplamento o rim engrossado sobe de 10 para
18 mm de altura, o que sozinho leva a peça de 163,7 para **168,6 g** e desce a
fila de furos de cima de z=111 para z=103. O acoplamento em si custa +14,5 g
(A), +19,2 g (B) e +8,8 g (C) sobre esses 168,6.

**Nenhuma mantém o encaixe por acidente:** todas as feições vivem no rim, e o
rim da peça de cima fica 52 mm acima do rim da de baixo quando encaixadas —
nunca se cruzam. O passo empilhado segue 130 mm nas três.

#### O que o 3D mostrou que o desenho 2D não mostrava

A fêmea passante da opção C aparece como **duas janelas com um dente de 9 mm
entre elas**: de fora, o rim daquele lado lê como ameia. A opção A troca isso
por **um rebaixo contínuo** — uma face mais baixa em vez de rim quebrado, o que
é mais limpo, ainda trava na extensão toda e custa só +5,6 g sobre a C. A opção
B é a mais bem resolvida vista peça a peça (o bloco lê como reforço de rim,
simétrico nos dois lados), e a pior vista acoplada: a junta de 8,7 mm fica
aparente.

#### As três foram recusadas — e a razão delas serem grandes

O pedido passou a ser **camuflado**. As A/B/C avançam 7,5 a 8,7 mm por um motivo
só: a aba tem de cruzar a fresta e **passar por trás da parede da vizinha**. Com
o rim engrossado de 3,2 mm como ressalto, a face interna da vizinha fica em
x=111,8 e a aba precisa avançar 6,1 mm; com a parede nua de 1,4 mm, 4,3 mm.

E há uma regra de desmoldagem que fecha o cerco: **a peça sai do molde na
direção do rim, então toda saliência tem de chegar ao rim.** Se ela morre no
meio da parede, a face que olha para cima é contra-saída. Logo a janela da fêmea
também tem de abrir no topo — e o fio do rim daquele lado quebra. **Sem ação
lateral no molde não há como esconder.** Descer a feição na parede não ajuda: o
excesso sobre o contorno da peça é mínimo no rim (3,2 mm) e cresce para baixo,
porque a fresta abre a 0,1223 mm/mm e o contorno só a 0,0612.

### 4.4 As duas camufladas — D e E

| | D · canaleta embutida rasa | E · travas nas pontas |
|---|---|---|
| Como | canaleta **cavada dentro da faixa** do rim; trilho com pescoço de 0,8 e cabeça de 1,0 atrás dele | 2 abas de 32 × 14 nas **pontas** da lateral, junto dos cantos, com gancho de 2,0 × 4,0 |
| Ressalto | as bordas da própria canaleta | a **parede nua de 1,4 mm**, não o rim de 3,2 |
| Avanço | **1,8 mm** | 5,0 mm |
| Envelope | **216,8 mm** (boca 215) | 220,0 mm |
| Rim | **inteiro nos dois lados** | inteiro no meio; quebrado só nas pontas |
| Simetria | simétrico | simétrico |
| Trava | extensão toda, em X e em Z; batente no fundo da canaleta | 2 × 32 mm, em X, com 2 mm de folga em Y |
| Montagem | desliza pela frente (o chanfro é a entrada) | desce |
| Molde | **2 gavetas laterais** (~USD 3 mil) | sem gaveta |
| Peso | 167,6 g | **166,9 g** |
| Interferência medida | 0 mm³ | 0 mm³ |

A D só é possível com gaveta, e é exatamente isso que a torna pequena: a
canaleta é cavada nos 3,2–4,1 mm da faixa, então o trilho **não precisa passar
por trás da parede da vizinha** — basta entrar na canaleta dela. Para a faixa
ter face de encosto de verdade, a face externa dela passa a ser **vertical**
(saída zero) nos 14 mm sob o rim: sem isso as duas faixas se tocariam só no fio
do rim e divergiriam 2 mm até a base da faixa. O colar que faz isso custa parte
dos 3,9 g de diferença para a peça sem acoplamento.

Vista de cima, a fêmea da D é **invisível**: o lábio superior da canaleta cobre
a abertura. E as duas são mais leves que qualquer uma das A/B/C (166,9 e 167,6 g
contra 177,4 a 187,8), porque a faixa caiu de 18 para 14 mm e as saliências
encolheram.

A E tem 2 mm de folga em Y (aba de 32 em janela de 34). A D trava em X e Z na
extensão toda e encosta no fundo da canaleta num sentido; no outro ela sai
deslizando para a frente, e isso se resolve com um detente de ~0,2 mm de
interferência no trilho — cota de ajuste de amostra, não de projeto.

Correção de registro: o risco decorativo de 0,9 mm que eu havia proposto na
opção C **é contra-saída** (um sulco horizontal com material acima dele). Só
sairia por deformação elástica, e 0,9 mm é muito para arrancar em PP. Se um
risco decorativo entrar, ele tem de ser aberto no topo (um degrau) ou raso de
verdade (~0,3 mm) — e confirmado com o ferramenteiro.

## 5. Injeção

Fechamento a 0,32 t/cm² (valvulado) + 10% de canal, limitado a 80% da máquina. Os furos estão nas
paredes, então **não reduzem a área projetada** — o que conta é o footprint de 430 cm².

| Cavidades | Fechamento | Máquina | Uso | Máquinas disponíveis | Ciclo est. | Produção |
|---|---|---|---|---|---|---|
| **1** | 151 t | **200 t** | 76% | **12** (INJ 1–6, 19–22, 35, 37) | 22 s | 163 pç/h |
| 2 | 303 t | 380 t | 80% | 3 (INJ 31, 32, 33) | 24 s | 300 pç/h |

**Recomendação: começar com 1 cavidade.** Não é só o custo do molde (USD 19,5 mil contra 34 mil):
a versão de 2 cavidades **empurra o produto para a classe de 380 t, onde a casa tem 3 máquinas**,
enquanto 1 cavidade roda na classe de 200 t, onde tem **12**. Para uma commodity que vai precisar
de horas de máquina em volume, disputar 3 máquinas é pior que disputar 12.

Se o volume passar de ~250 mil/ano, a expansão certa é um **segundo molde de 1 cavidade**
(USD 39 mil os dois) e não um de 2 cavidades (USD 34 mil): custa USD 5 mil a mais e entrega
redundância de ferramental e liberdade de programação na classe abundante.

Ciclos são estimativa (22 s com parede de 1,4 mm e macho de 130 mm de profundidade) — o
resfriamento do macho é o que manda, e só o try-out confirma.

---

## 6. Custo, preço e payback

### 6.1 Âncoras da casa (`TGFCUS` × `TGFITE`, 12 meses)

| Ref | Produto | Peso | Custo | Preço | R$/kg custo | R$/kg preço | Margem |
|---|---|---|---|---|---|---|---|
| **047/P** | Cesto Organizador Vime 7 L | 213 g | R$ 2,14 | R$ 4,58 | **10,05** | **21,5** | 53% |
| 047/B | idem, branco | 213 g | R$ 2,14 | R$ 4,90 | 10,05 | 23,0 | 56% |
| **268/P** | Cesto Europa Juta 5,3 L | 260 g | R$ 4,74 | R$ 7,30 | **18,2** | **28,1** | 35% |
| 041/P | Organizador Multiuso 3 div. | 118 g | R$ 1,37 | R$ 3,93 | 11,6 | 33,3 | 65% |
| 214/P | Organizador Multiuso 6 div. | 230 g | R$ 4,22 | R$ 7,25 | 18,3 | 31,5 | 42% |

As duas analogias diretas (cesto aberto e liso) são o **047 e o 268**: custo de **R$ 10 a 18/kg** e
preço de **R$ 21 a 28/kg**. A diferença entre elas é material — o 047 custa **menos por kg que a
resina virgem**, o que só fecha rodando moído.

### 6.2 Dois cenários

| Cenário | Custo | Preço | Margem | Contribuição | Pacote de 10 |
|---|---|---|---|---|---|
| Virgem RP 141 (R$ 15/kg custo) | R$ 2,33 | R$ 4,58 | 49% | R$ 2,25 | R$ 45,80 |
| Moído + pigmento (R$ 11,50/kg custo) | R$ 1,79 | R$ 4,58 | 61% | R$ 2,79 | R$ 45,80 |

Resina no cenário virgem: 0,1637 kg × R$ 9,54 = **R$ 1,56** por peça.

**Sobre o preço adotado.** Nas versões anteriores eu precifiquei por R$/kg, o mesmo critério do
custo. Está errado como critério de preço: **a regra por kg penaliza a redução de peso**. O
mercado paga pela função e pelo tamanho, não pelos gramas. Então adotei o preço do comparável
direto — **R$ 4,58 do Cesto Vime 7 L (047)** — e é aí que está o ganho: tirar 75 g da peça derruba
o custo em R$ 1,13 sem derrubar o preço, e a margem sai de 40% para 49%.

A R$ 0,86/L o produto fica acima do 047 (R$ 0,65/L), o que é esperado: 4,5 L com empilhamento e
encaixe vale mais por litro que 7 L de cesto simples. Se o comercial achar o preço agressivo,
R$ 3,99 ainda entrega 42% de margem no cenário virgem.

**A cor laranja é o que decide entre os dois cenários.** A casa compra PP moído **branco**
(R$ 7,69/kg, 124 t/ano) e **preto** (R$ 6,19/kg, 337 t/ano) — não laranja. Laranja em moído exige
lote dedicado de moído claro mais masterbatch, com risco de variação de tom entre lotes. É uma
pergunta para a produção, e vale **R$ 0,81 por peça** (R$ 122 mil/ano a 150 mil peças).

### 6.3 Resina

| Resina | Preço | Volume 12 m | Leitura |
|---|---|---|---|
| **PP RP 141 randon fluidez 40** | R$ 9,54/kg | 299,1 t | **Recomendada** — fluidez é o que uma parede de 1,4 mm sobre 430 cm² pede |
| PP CP 141 copolímero | R$ 10,52/kg | 108,9 t | Alternativa, se o teste de queda com carga reprovar o randon |
| PP H 103 homopolímero | R$ 9,90/kg | 473,2 t | **Não** — frágil em cesto carregado |
| PP moído branco / preto | R$ 7,69 / 6,19/kg | 124 / 337 t | Alavanca de custo, se a cor permitir |

### 6.4 Ferramental — por analogia, não por fórmula

Os dois moldes comparáveis da casa, ambos **peça única aberta** e ambos da **MR Plastic Mould**
(`AD_MOLDE` + `AD_ORCAMENTO`):

| Molde | Peça | Peso peça | Máquina | Bloco | Aço | FOB USD |
|---|---|---|---|---|---|---|
| **214-U** Organizador Rattan 6 div. | 160 × 178 × 191 mm | 235 g | 250 t | 450 × 550 × 580 | 1.128 kg | **18.900** |
| **284-U** Cesto Transporta Tudo | 182 × 263 × 313 mm | 313 g | 280 t | 600 × 550 × 600 | 1.556 kg | **20.100** |

Nossa peça (215 × 197 × 130 mm, 164 g) fica **entre as duas** em envelope e **abaixo das duas** em
peso e em complexidade. Daí **USD 19,5 mil FOB para 1 cavidade** — estimativa por analogia direta
com compras reais da casa, não por fórmula de USD/kg de bloco.

**Essa estimativa agora está conservadora, e de propósito.** A forma final é uma casca
tronco-piramidal com dois chanfros planos: sem aba, sem sela, sem pilar. Desmoldagem direta em Z,
nenhuma gaveta, nenhum movimento lateral, e os 68 furos são encostos redondos simples. É mais
simples que o 214-U, que tem seis divisórias internas. Espero cotação **abaixo** dos USD 19,5 mil;
mantive o número alto para o payback não se apoiar em otimismo.

### 6.5 Payback

Investimento nacionalizado de 1 cavidade: USD 19,5 mil × R$ 5,45 × 1,30 = **R$ 138,2 mil**
(câmbio e nacionalização seguem premissa, não dado do ERP).

| Volume/ano | Cenário | Contribuição/ano | Payback | Horas de máquina |
|---|---|---|---|---|
| 60.000 | virgem | R$ 98,2 mil | 16,9 meses | 367 h |
| 60.000 | moído | R$ 122,8 mil | 13,5 meses | 367 h |
| **150.000** | **virgem** | **R$ 245,6 mil** | **6,8 meses** | 917 h |
| 150.000 | moído | R$ 306,9 mil | 5,4 meses | 917 h |
| 300.000 | virgem | R$ 491,1 mil | 3,4 meses | 1.833 h |
| 300.000 | moído | R$ 613,9 mil | 2,7 meses | 1.833 h |

Referência de volume: o **041 (Organizador Multiuso 3 divisórias) vendeu 262 mil unidades em 12
meses** para 1.847 clientes — é o campeão de volume da casa em organizador pequeno. Se o cesto
novo chegar à metade disso (131 mil/ano), o payback é de 7,8 meses em virgem.

---

## 7. O que falta — e o mais importante primeiro

| Item | Gravidade | Por quê |
|---|---|---|
| **Capacidade de 4,43 L é suficiente?** | **Alta** | O chanfro do pé já caiu de 52 para 36 mm para devolver volume. Levá-lo a 24 mm devolve ~0,2 L a mais, sem tocar no acesso frontal |
| **Amostra física** | **Alta** | O passo do encaixe e o engate exato da saia nos berços do rim |
| **Passo do encaixe** | **Alta** | É a promessa de embalagem do pacote de 10. Medir na amostra ou em protótipo impresso (seção 4.2) |
| Preço do anúncio de referência | Alta | **Não consegui abrir** — o proxy da sessão bloqueia o Mercado Livre. Precisa do preço do pacote de 10 para validar o cenário de preço |
| Volume-alvo de venda | Alta | É o que decide 1 ou 2 cavidades e o payback. A conta é de volume, não de margem |
| Laranja em moído é viável? | Média | Vale R$ 0,78/peça (seção 6.2) |
| Redução de peso para 200 g | Média | Vale R$ 22 mil/ano a 150 mil peças (seção 2.1) |
| Teste de queda com carga | Média | Decide RP 141 vs CP 141 |
| Pastilhas de furo postiças | Média | Manutenção do molde (seção 3.1) |
| Câmbio e nacionalização | Baixa | Premissa, não dado do ERP |

## 8. Arquivos

```
cad/cesto.step     solido para a ferramentaria
cad/cesto.stl      malha (impressao/visualizacao)
cad/01-cesto.png   02-frente.png   03-empilhado.png   04-encaixado.png
cad/modelo3d.py    parametrico -- muda cota, furo, saida e rebordo num lugar
cad/render.py      rasterizador das vistas
economia.py        comparaveis, resina, fechamento, cenarios e payback
cad/variantes.py   monta as 3 opcoes de canaleta, mede a interferencia entre
                   duas pecas acopladas e compoe variantes.png / variantes-iso.png
cad/proposta-canaleta.py  o desenho 2D que motivou as 3 opcoes
cad/camufladas.py  monta as opcoes D e E, normaliza a escala das vistas
                   ortogonais e compoe camufladas.png / camufladas-frente.png
cad/empilha.py     mede no solido o passo de empilhamento e de encaixe
cad/pe.py          pezinhos, soquete do pe traseiro e a folha pezinho.png
cad/estrutura.py   a estrutura de empilhamento na borda e a folha estrutura.png
cad/final.py       a peca completa e a folha final.png
cad/cesto-final.step/.stl  a peca com tudo: pezinhos, estrutura de
                   empilhamento e cauda de andorinha do acoplamento
```
