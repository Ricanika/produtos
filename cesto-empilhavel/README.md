# Linha ELO — organizadores empilháveis, encaixáveis e acopláveis em PP

> **ELO P** (4,09 L · 179,2 g) e **ELO M** (~25 L), peça única injetada cada.
> O corpo deste documento é o registro do projeto do P; o M está na **§4.2.8**.
> O diferencial da linha — **dois P acoplados empilham no M** — está medido em
> 0,0000 mm³ de interferência.
>
> A **§4.2.7** descreve um M intermediário de 9,10 L, com a mesma planta do par
> e o pouso centrado. Ele foi superado em 23/09 pelo M de 25 L, que é mais
> fundo e recebe o par recuado. Fica no registro porque é ele que mostra de
> onde veio a largura de 380 mm.

**Status:** 3D fechado na **configuração C** (aba para fora, extrai em molde de duas placas), pronto para cotação de ferramental · **Data:** 23/09/2026
**Referência:** STL enviado em 16/09 (bin de 150 × 100 × 80 mm, 192 faces) + anúncio
"10 peças Cesto Mini Organizador Empilhável" (MLBU4092388469) + fotos cotadas
(Mercado Livre MLBU4092388469) + fotos cotadas enviadas em 16/09/2026
**Modelo:** `cad/modelo3d.py` (`padrao()` fixa o P, `padrao_m()` fixa o M) · **Economia:** `economia.py`
**Sólido do projeto:** `cad/cesto-aba.step` / `cad/cesto-aba.stl` · **Visores 3D:** `cad/visor3d.html` (o P) e `cad/visor-elo.html` (a linha) · **Impressão:** `cad/print/`

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
| Forma da referência | **Medida no STL, não interpretada** — chanfros a 45°: 52 mm no topo, 36 mm no pé (seção 2.2) |
| Vazado | **3 faixas de listra**, rasgo de 6 × 18,33 mm, 123 rasgos em 13 colunas, faixa cega de 40 mm (seção 4.2.3). O vazado de bolinha, medido lado a lado, pesa 6,3 g mais |
| Fundo sólido | **Atendido e medido** — chapa de 188,6 × 187,5 × 2,0 mm com **0 mm² de furo**, parede cega até z = 40, bolsa cega sob o pé (seção 4.2.4) |
| Pé discreto | **Resolvido** — **tripé**: um pé oco por lateral, na frente (y = −58), e uma saia corrida na traseira, todos sob a chapa, que flutua 5 mm acima do piso. 469 mm² de contato de face plana (seções 4.1 e 4.2.6) |
| Empilhar, encaixar **e** acoplar | **Os três, medidos no sólido** — empilha **130,0 mm** (0,0000 mm³ de interferência) · encaixa **39,99 mm** · acopla com trava de 27,2 mm³, solta a 7,5 mm de levantamento (seções 4.2.1, 4.2.2 e 4.2.6) |
| Acoplar lateralmente | **Resolvido dentro das paredes de empilhamento** — cauda de andorinha vertical de 1,4 mm, sem gaveta, trava puxando de lado (seção 4.2.2) |
| Encaixar para reduzir volume | **Medido no sólido: passo de 39,99 mm**, 572 mm para 12 peças (era 46,80 com a aba para dentro). Exclusivo do empilhamento a 130 mm — ver seção 4.2 |
| Extração | **Auditada por interseção de sombras** — a aba para DENTRO prendia 58.242 mm³ no molde e era inviável em duas placas; virada para FORA sobra a linha de base de 9.217 mm³, que são os rasgos passantes na parede com saída (seção 4.2.5) |
| Injeção no parque atual | **1 cavidade numa 250 t (68%)** — a casa tem **9 máquinas** dessa classe. A aba para fora levou o footprint de 430 para 480 cm², e com ele o fechamento de 151 para 169 t: saiu da classe de 200 t |
| Ferramental | **USD 19,5 mil FOB**, 1 molde — por analogia direta com dois moldes da casa |
| Payback | **~6,2 meses** a 150 mil un/ano em PP virgem (4,9 com moído), com o molde estimado por cima |
| Preço do anúncio de referência | **Não obtido** — o proxy desta sessão bloqueia o Mercado Livre (seção 6) |

O produto é uma **commodity de volume**: contribuição de ~R$ 1,79 por peça em virgem (R$ 2,24 em moído), então a conta fecha
por quantidade, não por margem unitária. Isso muda o critério de decisão em relação à caixa
dobrável: lá o risco era o ferramental caro; aqui o ferramental é barato (USD 19,5 mil, ~14% do
que custaria a família dobrável) e **o risco é o volume de venda**.

---

## 2. Geometria

Todos os valores abaixo são **medidos no sólido** (`cad/cesto-aba.step`) na
configuração C, não cotas de intenção. As seções 3 e 4 são o registro de como
se chegou neles — os números citados lá são os da etapa que cada seção
descreve, e não os de hoje.

| Cota | Valor |
|---|---|
| Boca do corpo | **180 × 230 mm** |
| Envelope de planta, com a aba | **200 × 250 mm** |
| Base (z = 0) | 152,7 × 202,7 mm |
| Altura | **130 mm** |
| Envelope real | **204,0 × 235,1 × 132,5 mm** |
| Chanfros da frente | **52 mm no topo · 36 mm no pé**, ambos a 45° |
| Face frontal | **42 mm** (130 − 52 − 36) |
| Raios trabalhados | **R20** nas duas pontas dos chanfros · **R12** nas duas quinas da face frontal |
| Raio de planta | **R14** na casca externa (`RectangleRounded`) |
| Saída de molde | **6° por lado** (era 3,5° e depois 12° — ver 4.2.6) |
| Parede / fundo / rim | 1,4 / 2,0 / 3,2 mm |
| Aba do rim | **10 mm para FORA** × 2,5 mm, com dobra de 5 mm descendo na aresta |
| Pé | **tripé** — 1 pé oco por lateral na frente (y = ±58 espelhado) + saia corrida de 108 mm na traseira, sob a chapa, que flutua 5 mm acima do piso; bolsa cega, sola sem furo |
| Chapa do fundo | 188,6 × 187,5 × 2,0 mm, **0 mm² de furo** |
| Vazado | 3 faixas de listra, rasgo **6 × 18,33 mm**, 123 rasgos, 13 colunas |
| Capacidade | **4,09 L** |
| Peso | **179,2 g** em PP (198,0 cm³ × 0,905) |
| Área projetada | 480 cm² |
| Empilha | **130,0 mm** deslocando 21 mm — 0,0000 mm³ de interferência |
| Encaixa | **39,99 mm** — 12 peças em 572 mm. As folhas dão 39,98 a 40,00: é a tolerância da busca binária de cada script (0,01 a 0,02 mm), não geometrias diferentes |
| Preso no molde | **9.217 mm³**, todo ele rasgo passante em parede com saída |

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

**179,2 g para 4,09 L**, contra o **Cesto Organizador Vime 7 L (047) da casa, que faz 7 L com
213 g**. A **43,8 g/L** a peça fica **bem acima** do 047 (30,4 g/L), e isso é geometria, não
desperdício: um cesto de 4 L tem mais área de parede por litro que um de 7 L, e a parede já está
no mínimo da casa (1,4 mm).

O histórico do peso, todo medido no sólido:

| etapa | peso | por quê |
|---|---|---|
| primeira geometria | 230 g | caixa reta com aba em gancho |
| chanfros a 45° | 155 g | os chanfros tiram material e a aba em gancho saiu inteira |
| tripé + acoplamento + friso | 169 g | o que empilhar, encaixar e acoplar custam |
| **configuração C** | **179,2 g** | +4,7 g da tapa da frente, +4,3 g da dobra da aba, ~1 g do resto (aba virada e saída de 6°) |

Os 10,2 g entre 169,0 e 179,2 não são gordura: 4,7 g fecham o rasgo frontal que o cliente mandou fechar
e 4,3 g são a dobra sem a qual duas peças não acoplam (§4.2.6). **O único alívio grande que resta é
perfurar a chapa do fundo** — 52,2 g dos 179,2, 29% da peça —, e o cliente pediu explicitamente
fundo fechado, porque o P guarda miudezas. Se o try-out pedir mais, o caminho é parede de 1,2 mm na
banda superior, onde não há carga de empilhamento.

---

## 3. O vazado

> **Esta seção é o estudo do vazado de BOLINHA, que não é o que a peça tem
> hoje.** O desenho escolhido é o de **listra vertical em 3 faixas** (§4.2.3), e
> a comparação medida entre os dois está em `cad/listras.png`: a bolinha pesa
> 6,3 g mais. `VAZADO = "bolinha"` em `modelo3d.py` reconstrói o que está
> descrito abaixo. O que segue valendo daqui são as duas regras de retículado
> no fim da seção e o §3.1, sobre o custo no molde — que vale para qualquer um
> dos dois desenhos.

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

> **Etapa intermediária.** Os quatro pezinhos descritos aqui foram depois
> substituídos pelo **tripé** — um pé por lateral, na frente, e uma saia
> corrida na traseira (§4.2). O que segue valendo desta subseção é o
> princípio: chapa flutuando 5 mm, pé oco, e a chapa fazendo aba sobre ele.

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

### 4.2.3 Vocabulário, mais ângulo, e a conta que decide

**EMPILHAR** = uma sobre a outra, vários andares, altura cheia.
**ENCAIXAR** = uma dentro da outra, para transporte.
**ACOPLAR** = lado a lado.

A saída de molde subiu de **3,5° para 9°** e o **pé virou o fundo da nervura**:
é ele que cai no pino da peça de baixo, como pedido. Com o pino de 10 mm, o
passo empilhado é ALT + 10 = **140 mm por andar**.

#### Um erro que estava mascarando tudo

Os pezinhos tinham a face externa em **x = 97,5 fixo**, cota de quando a saída
era 3,5°. A 9° a base tem 86,9 mm de meia-largura — os pezinhos ficavam **para
fora da parede** e matavam o encaixe. A peça nua media 89,1 mm de passo quando
deveria medir 23,8. Corrigido: a face externa passou a ser derivada da base
(`BASE_X/2 − 2`).

#### A conta

> passo_encaixe ≥ passo_pilha / 2 + (rim + apoio + folga) / (2 · tg saída)

O pino está no alto e o pé embaixo. Encaixando, os dois se aproximam ao mesmo
tempo — cada milímetro conta duas vezes, e o termo **passo_pilha/2 não some com
ângulo nenhum**. Medido no sólido:

| saída | base | encaixa | 6 peças | 12 peças | 12 SEM estrutura |
|---|---|---|---|---|---|
| 3,5° | 199 | 106,6 | 663 | 1.303 | 740 |
| 7,0° | 183 | 86,0 | 560 | 1.076 | 446 |
| **9,0°** | **174** | **82,0** | **540** | **1.032** | **392** |
| 12,0° | 160 | 78,5 | 522 | 994 | 616 |

(A 12° o encaixe sem estrutura piora porque outra feição passa a limitar.)

#### Onde está o custo — medido isolando cada feição

| | encaixa | 12 peças |
|---|---|---|
| pino + nervura | 82,0 mm | 1.032 mm |
| **só o pino** | **82,0 mm** | 1.032 mm |
| só a nervura | 74,5 mm | 949 mm |
| nenhum dos dois | **22,8 mm** | **381 mm** |

**O pino sozinho já custa todo o encaixe.** Ele precisa avançar para dentro do
rim o suficiente para a nervura o alcançar, e é exatamente esse avanço que
fecha a boca. Não é a nervura, não é o acoplamento: é o pino.

#### A bifurcação

| | A · com estrutura | B · sem estrutura | C · duas peças |
|---|---|---|---|
| Empilha | **140 mm/andar** | não | 140 mm/andar |
| Encaixa | 82,1 mm | **23,9 mm** | **23,9 mm** |
| 6 peças | 541 mm | **250 mm** | **250 mm** |
| 12 peças | 1.033 mm | **393 mm** | **393 mm** |
| Acopla | sim | sim (parede externa) | sim |
| Molde | 1 | 1 | 1 + 1 pequeno |

A **C** é a única que entrega os dois no alvo: a peça sai sem pino (encaixa
fundo) e os **4 pinos vão soltos na embalagem**, encaixando no rim quando o
cliente quer torre. Como a cauda de andorinha do acoplamento mora no pino, o
clipe traz empilhamento **e** acoplamento juntos. Custa um 2º molde pequeno
(~USD 3 a 5 mil), 4 peças a mais por cesto e um passo de embalagem.

Capacidade a 9°: **3,95 L** (era 4,46 a 3,5°). Peso 171,8 g.

### 4.2.4 A aba plana no rim + pés com cavidade — e o fim da bifurcação

Pedido do cliente, em três partes: (1) empilhar **na mesma ordem do encaixe**,
os andares com a mesma frente, sem inverter; (2) para isso, **uma parte plana
de ~1 cm em toda a borda superior**, e é nessa aba que o pé encaixa; (3) os pés
com **cavidade interna**, para se engolirem no transporte.

Essa arquitetura dispensa o pino, e com ele some a conta de 4.2.3 — que só
existia porque o pino e o pé se aproximavam ao mesmo tempo. Aqui **quem manda
no encaixe é a largura da aba**, e só ela:

> passo_encaixe = ABA_W / tg(saída) = 10 / tg 12° = **47,1 mm** (medido: 46,9)

A parede da peça de cima tem de passar pela borda interna da aba, e mais nada
encosta. Medido no sólido, a 12° de saída:

| | medido |
|---|---|
| encaixa (mesma frente, sem deslocar) | **46,9 mm** |
| 6 peças / 12 peças na caixa | **364 / 646 mm** |
| empilha (deslocando 10 mm em y) | **130,0 mm** — altura cheia |
| deslocamento mínimo para empilhar | 5 mm |
| apoios na aba | 6 pés × 3,0 × 9,8 mm |
| trava lateral a partir de | 0,6 mm |
| solta levantando | 15 mm |
| peso / capacidade | 163,8 g / 3,66 L |

Os alvos do cliente eram 6 peças no mínimo e 12 no ideal: **12 peças cabem em
646 mm de caixa**.

#### O pé: saída em y, e a cavidade subtraída da peça INTEIRA

Duas correções fizeram o pé funcionar. A primeira: ele **não tinha saída nas
faces em y**. Sem ela a boca da cavidade (`NERV_L − 2·NERV_T` = 6,8 mm) é
sempre mais estreita que a língua (10 mm) e **o pé nunca entra no pé** — a peça
media 106,8 mm de passo, e todos os seis pés apareciam na medição de
interferência com o vão em y exatamente igual ao comprimento do pé. Com 2,6°
por lado (`NERV_KY = 0,045`), o pé de cima entra depois de descer
`NERV_T/NERV_KY` = 35,6 mm — abaixo dos 46,9 que a aba impõe, então não limita.

A segunda: a cavidade é subtraída da **peça inteira**, não do pé. De uma só vez
ela (a) esvazia o pé, deixando só o piso de apoio embaixo; (b) **vaza a parede
atrás do pé** — janela de 6,8 mm, escondida de fora pela própria face externa
do pé; (c) abre o recorte na aba. Sem a janela (b) o piso do pé de cima bate na
parede da peça de baixo: ele nasce na parede e avança 20,6 mm para fora, tem de
atravessá-la. A janela é fechamento macho-fêmea no molde, de graça.

A face externa do pé sobe de `LARG/2 − ABA_W + NERV_B` = 100,5 mm no piso até
`LARG/2` = 107,5 exatamente no rim. Essa inclinação própria (3,1°) faz o pé se
apagar na parede sem nenhuma face virada para cima — a silhueta da peça nunca
diminui subindo, logo **nenhuma contra-saída**.

#### Por que o empilhamento exige deslocar 10 mm

Não é escolha: é teorema. Para uma peça única e translação vertical, o repouso
é determinado pela geometria — existe **um** menor deslocamento sem
interferência. Alinhadas (dy = 0) as peças encaixam a 46,9 mm, e é onde a
gravidade as deixa; não há como elas pararem a 130 mm na mesma pose. Empilhar e
encaixar na pose idêntica são **mutuamente exclusivos**, e todo sistema real
usa um discriminador: girar 180° (o cliente recusou) ou **deslocar**.

Aqui o discriminador é o deslocamento: o recorte da aba tem 18,5 mm e o piso do
pé 10 mm, então basta o pé sair do recorte. Medido: 5 mm já dão 130,0 mm, e
**10 mm dão apoio cheio nos seis pés**. A frente continua sendo a frente — não
há inversão, que era o que o cliente recusava. E funciona nos **dois sentidos**
(±10 medidos), então alternando o sinal a coluna não caminha: fica dentro de
uma faixa de 10 mm em vez de escalonar.

#### O acoplamento ficou de graça

Com passo de encaixe de 46,9 mm, tudo o que estiver **acima de 83 mm** da peça
de cima fica acima do rim da de baixo — não custa nada no encaixe. A cauda de
andorinha do acoplamento mora nos 14 mm de cima: em **planta**, pescoço de 7 mm
no plano da junta e ponta de 11 mm, macho na direita e fêmea na esquerda (as
duas peças na mesma orientação, então a direita de uma encontra a esquerda da
outra). Prismática em z e aberta no topo: desmolda **sem gaveta**.

Medido: separação lateral bloqueada a partir de 0,6 mm e a ponta de 11 mm não
passa pela boca de 7,4 mm — para soltar, levanta 15 mm.

#### O que essa arquitetura custa

- A aba é interrompida por **6 recortes de 18,5 mm** (11% do perímetro do rim).
  A borda **externa** da aba continua inteira — sobra um lábio de 1,6 mm que
  atravessa o recorte —, então de fora o rim se lê contínuo; de cima aparecem
  seis rasgos.
- Os pés são **contrafortes de 20,6 mm de avanço no piso**, apagando-se no rim.
  A 12° de saída a base é 55 mm mais estreita que a boca, e o pé tem de vencer
  essa diferença para alcançar a aba — não há como fugir disso. De fora eles se
  leem como três pilastras por lateral, que é justo o que as caixas de
  referência do cliente têm.
- Capacidade caiu para **3,66 L** (era 4,46 L a 3,5°). É o preço do ângulo que
  entrega as 12 peças.

Arquivos: `cad/aba.py` (folha `aba.png`), `cad/cortes.py` (`cortes.png`, cortes
2D tirados do sólido), `cad/cesto-aba.step` e `.stl`.

#### Dois pés por lateral: um pé na frente e um ENCAIXE atrás

Segunda rodada do pedido: dos três pés por lateral ficaram **dois** — o da
frente (na altura do rasgo curvado da silhueta) sustenta, o do meio saiu, e o
de trás virou um **encaixe** mais fino, com o **pino na aba** da referência do
cliente.

| | frente | trás (encaixe) |
|---|---|---|
| y do centro | −39 mm | +40 mm |
| comprimento em y | 10 mm | 8 mm |
| parede | 1,6 mm | 1,2 mm |
| saída em y | 2,6°/lado | 1,8°/lado |
| face externa no piso | 100,5 mm | 103,0 mm |
| recorte que abre na aba | 18,5 mm | 13,9 mm |

Regra de cada pé: **saída em y ≥ parede / passo_encaixe**, senão a boca da
cavidade nunca engole a língua. A 46,9 mm de passo isso dá 0,034 para 1,6 mm
de parede e 0,026 para 1,2 — as duas com folga.

Resultado medido: **peso caiu de 163,8 para 154,0 g**, o encaixe continua em
**46,9 mm** e o empilhamento em **130,0 mm** (0,00 mm³ de interferência a
130,0 exatos), agora com **4 apoios e 148 mm² de contato**. A aba interrompida
caiu de 111 para **65 mm** do perímetro (8%).

**O pino.** Saliência de 3 mm acima da aba, encostada com 0,3 mm de folga na
lateral do piso do pé da peça de cima, do lado do recorte: é o que impede a
peça de escorregar de volta para a posição de encaixe. Custa **zero** no
encaixe — a 46,9 mm de passo o rim da peça de baixo encontra a peça de cima
onde a parede dela ainda está em x = LARG/2 − ABA_W, e o pino mora para fora
disso.

**O que isso custou, e é honesto dizer:** o deslocamento agora só funciona no
sentido **+y**. O chanfro de topo come a aba a partir de
y = −PROF/2 + CHANFRO = −48 mm, e o pé da frente deslocado −14 mm cai no vazio
— medido: **2 apoios em vez de 4**. Por isso o pino aponta um só sentido, e a
coluna sobe **escalonada de 14 mm por andar**. Para empilhar nos dois sentidos
(coluna a prumo) o pé da frente teria de recuar para y = −26, o que encurta o
braço de apoio de 79 para 66 mm. É uma escolha de projeto, não uma limitação
de molde.

Com 4 apoios num retângulo de 200 × 79 mm dentro de uma peça de 200 mm de
profundidade, a cesta de cima **pode balançar** se for carregada muito na
frente ou muito atrás. Quem resolveria isso é um pé na parede de trás (a aba
corre lá também, e a distância a vencer é a mesma 17,6 mm) — mais um recorte,
a decidir.

#### A frente sem meias-bolas, e o friso no lugar do pino

**A frente é a parte aberta** (−Y no modelo), e a borda dela é o corte da
silhueta na casca inclinada: no meio ela fica em z ≈ 89 mm e nas pontas sobe
para ≈ 101 mm, por causa do raio de canto da planta. Os furos da frente
estavam **trombando nesse arco**, e cada um deixava uma meia-bola na borda.

A causa era um cilindro só varando a frente E o fundo: para manter o fundo
cheio (lá a parede vai até o rim) era obrigatório aceitar o furo cortado na
frente. Agora **a frente e o fundo são furados separadamente**, e a frente
descarta o furo que não passa o teste `cabe_na_frente(x, z, d, folga)` —
avaliado no topo do furo e no x dele mais próximo do meio, que é onde a borda
está mais baixa. As duas fileiras de cima da frente saem; o fundo continua com
as quatro. Borda limpa, sem recorte na aresta.

**O pino virou friso.** No lugar da saliência única, um **U de três pernas de
1,2 × 2,5 mm** em relevo na aba, no lugar exato onde o piso do pé de trás da
peça de cima pousa. Medido, empurrando a peça de cima 1 mm:

| sentido | interferência |
|---|---|
| y + | 16,3 mm³ |
| y − | 16,3 mm³ |
| x + | 15,0 mm³ |
| x − | 15,0 mm³ |

Os quatro sentidos travam a partir de **0,6 mm** de folga — o andar fica
**posicionado**, não só apoiado. Antes, com um pino só, apenas o sentido do
encaixe estava seguro.

O friso custa **zero** no encaixe, e há uma conta que garante isso:

> friso_x0 = LARG/2 − ABA_W + tg(saída)·FRISO_H + 0,6 = **98,6 mm**

A peça de cima, encaixada, cruza a cota do rim da de baixo com a parede em
x = LARG/2 − ABA_W = 97,5 mm; subindo os 2,5 mm de relevo ela engorda
tg 12° × 2,5 = 0,53. O friso mora para fora disso. Se o relevo crescer, a face
interna dele tem de recuar na mesma proporção.

O encaixe de trás também andou de y = 40 para **36 mm**: pousando em
y = 50…58 ele estava encostando no fim do trecho reto da lateral (58,4 mm, onde
começa o raio de canto). Em 36 ele pousa em 46…54, com 4,4 mm de sobra.

Peso **153,9 g**. Encaixe e empilhamento inalterados: 46,9 e 130,0 mm.

#### O P estava girado: a abertura vai na LARGURA

O lado maior é o **comprimento** e a **abertura fica na largura**. O modelo
estava ao contrário — a abertura na face de 215 mm e os pés nas de 200. Agora:

| | antes | agora |
|---|---|---|
| X — largura (onde fica a abertura) | 215 mm | **200 mm** |
| Y — comprimento (o lado maior) | 200 mm | **215 mm** |
| pés e acoplamento | faces de 200 | **faces de 215** |
| passo acoplado | 215 mm | **200 mm** |

A troca é mais que renomear eixos: as cotas dos pés, do friso e das caudas de
andorinha são em y, e o trecho reto da lateral mudou de [−46, 58] para
**[−53,5, 63,9] mm** (o limite de trás é o raio de canto da planta no topo,
41,6 mm a 12°; o da frente é onde o chanfro come a aba). Reposicionado:

| | antes | agora |
|---|---|---|
| pé da frente | y = −39 | **−43 mm** |
| encaixe de trás | y = 36 | **42 mm** |
| caudas de acoplamento | −22 / +26 | **−26 / +28 mm** |
| braço de apoio | 79 mm | **85 mm** |

`aba_livre()` passou a contar o **berço do friso** como ocupado: a fêmea da
cauda escava a aba 4 mm para dentro e o friso mora justo aí — sem isso a fêmea
cortaria a perna do friso.

Tudo o que foi medido antes continua valendo, agora com o P na orientação
certa: **encaixa 46,9 mm** (12 peças em 648 mm), **empilha 130,0 mm** com 4
apoios e 148 mm² de contato, acoplamento travando a partir de 0,6 mm e
soltando com 15 mm de levantamento. Peso **155,6 g**, capacidade **3,68 L**,
envelope 204 × 206 × 132,5 mm.

**O ângulo da abertura** é o chanfro de topo, e com o comprimento em 215 mm
sobrou trecho reto atrás — ou seja, dá para abrir mais sem mexer no
empilhamento. `cad/abertura.py` desenha as três (folha `abertura.png`):

| chanfro | face frontal | topo da frente | aba livre atrás |
|---|---|---|---|
| 40 mm | 54 mm | z = 90 mm | 175 mm |
| **52 mm (hoje)** | **42 mm** | **z = 78 mm** | **163 mm** |
| 68 mm | 26 mm | z = 62 mm | 147 mm |

#### 250 mm de comprimento, e a canetinha no lugar dos pés de trás

Largura fica em 200 mm, comprimento vai a **250 mm**, e os dois pés de trás
saem: no lugar deles, **uma canetinha curvada única na sola da base, atrás**.
Com os dois pés da frente ela forma um **tripé** — mais estável que quatro
apoios amontoados no meio do comprimento.

| | medido |
|---|---|
| encaixa (mesma frente) | **46,9 mm** — 12 peças em 648 mm |
| empilha (desloca 17 mm) | **130,0 mm**, 0,000 mm³ a 130,0 exatos |
| apoios | **3 (tripé) · 141 mm²** — canetinha 80, pés 30 cada |
| friso trava o andar | y ± e x ± a partir de 0,6 mm |
| acopla | trava a partir de 0,6 mm, solta levantando 15 mm |
| peso / capacidade | **169,2 g / 4,41 L** (era 155,6 g / 3,68 L) |
| envelope | 204 × 241 × 132,5 mm |

**A canetinha, e por que a curva é CONCAVA.** A primeira tentativa usou o
mesmo perfil dos pés — uma rampa que sobe até o rim. Ela não funcionou, e a
medição disse o porquê: a canetinha pousa na aba de **trás**, e o
deslocamento do empilhamento também é em y. Deslocar não tira o pé de cima de
cima do recorte, porque **o recorte ocupa a mesma faixa em y que a própria
aba**. Resultado: 2 apoios em vez de 3, e o encaixe subiu de 46,9 para
**73,4 mm**.

A solução é a curva ao contrário:

> y(z) = y₀ + (PROF/2 − y₀) · (z/ALT)^2,2

Com o expoente **maior que 1** a canetinha sobe devagar — projeta só
**4,6 mm** da parede no piso — e o **cone a alcança em z = 42 mm**, onde ela
se apaga na parede. Ou seja, ela nunca chega à cota do rim e **não abre
recorte nenhum na aba**. A peça encaixada passa pela cota do rim da de baixo
com a canetinha ainda em y = 112,5 mm, dentro da borda interna da aba (115).
E a silhueta continua crescendo para cima em todo o percurso: nenhuma
contra-saída, nenhuma gaveta.

`y₀ = PROF/2 − ABA_W + CAN_B − DESLOC` amarra a canetinha ao deslocamento: ela
nasce DESLOC mm mais para dentro para, deslocada, cair exatamente sobre a aba.

**O deslocamento subiu de 14 para 17 mm**, e isso foi medido, não escolhido:
com um pé por lateral o friso passou para o pé da **frente**, cujo recorte na
aba é mais largo (meia-boca de 9,25 mm), e a perna do friso caía **dentro** do
recorte — o pé da peça encaixada batia nela. O mínimo é
`meia-boca + L/2 + folga + espessura = 15,75 mm`.

Com o comprimento em 250 mm o trecho reto da lateral virou **[−71, 81,4] mm**,
e o pé da frente pôde ir para y = **−58** (era −43). O braço do tripé ficou:
pés em y = −58 e canetinha em y = +119, ou seja **177 mm de base** numa peça
de 250 — contra os 85 mm de antes. As caudas de acoplamento foram para
**−27 e +74**, 101 mm de braço.

#### Mais clean: saia de trás invisível e pés da frente arredondados

**O pé de trás saiu de vista.** A canetinha projetava 4,6 mm da parede e
aparecia. No lugar dela, a parede de trás simplesmente **continua para baixo**
nos 5 mm de H_PE que `p -= extrude(..., H_PE)` tinha cortado — usando o mesmo
cone da casca, então fica **rente**: não há saliência nenhuma para se ver de
fora. As pontas em planta são arredondadas em R10.

Ela custa **zero** no encaixe, e por construção: a face externa dela **é** a
superfície do cone, então ela encaixa como a própria parede encaixa (basta
passo ≥ T_PAREDE/tg 12° = 6,6 mm). Nenhuma janela, nenhuma cavidade, nenhum
recorte na aba.

E o apoio melhorou muito: a aresta de baixo tem 4 mm de espessura e **108 mm
de largura**, o que dá **370 mm² de contato** na aba de trás, contra os 80 mm²
da canetinha. Total do tripé: **417 mm²** (era 141).

| | canetinha | saia |
|---|---|---|
| aparece de fora | 4,6 mm de saliência | **nada** |
| contato na aba | 80 mm² | **370 mm²** |
| custo no encaixe | zero (curva concava) | **zero (é o cone)** |
| recorte na aba | nenhum | **nenhum** |

**O deslocamento subiu para 21 mm.** A saia é rente, então a aresta de apoio
dela nasce em y = BASE_Y/2 = 97,4 mm e a borda interna da aba está em 115 —
são 17,6 mm só para alcançar a aba, mais o apoio que se quer ter em cima dela.

**Os pés da frente viraram língua.** A planta deixou de ser retângulo: agora é
um retângulo **arredondado em R4,2**, e o pé é construído por `loft` entre a
planta do piso e a do rim. Bico redondo, lateral curvada, nenhum canto vivo. A
cavidade usa o mesmo loft com `rc = R − parede`, o que mantém a parede
constante **inclusive no bico**.

Isso trouxe um efeito colateral que a medição pegou: com o bico redondo o piso
do pé afina depressa, e a perna do friso — posicionada em L/2 — ficou com
0,8 mm de folga e praticamente **não travava** em y (0,05 mm³ empurrando
1 mm). `pe_apoio_h()` passou a calcular a meia-largura real do piso na face do
friso (4,29 mm em vez de 5,00), e a trava voltou: **2,04 mm³**.

Peso **170,3 g**, capacidade 4,41 L. Encaixe 46,9 e empilhamento 130,0
inalterados (0,000 mm³ a 130,0 exatos).

#### Bolinhas → listras verticais (e onde o peso realmente está)

Mesma casca, mesmas curvas, mesma estrutura: muda **só o vazado**. Cada listra
é um estádio vertical de 10 mm de largura com as pontas em R5, e as faixas
seguem as bordas — na frente elas param no arco da silhueta, na lateral
encurtam acompanhando o chanfro de topo, em vez de serem descartadas.

**170,3 g → 157,1 g** (−13,2 g, −7,8%). Encaixe 46,9 mm, empilhamento 130,0 mm
e acoplamento **inalterados** (o vazado não toca em nenhuma feição funcional:
ele mora em z de 40 a 111, e os pés são somados depois dele).

#### O que a varredura ensinou

| variante | peso |
|---|---|
| w9 · p15 · 3 faixas | 163,2 g |
| w11 · p15 · 3 faixas | 162,5 g |
| w9 · p13 · 3 faixas | 163,3 g |
| **w10 · p15 · 2 faixas** | **157,1 g** |
| w10 · p14 · 2 faixas · banda 32 | 154,6 g |

**O que pesa não é a largura nem o passo da listra — é o número de faixas.**
Cada faixa a mais é uma nervura horizontal de 8 mm dando a volta na peça
inteira: de 3 para 2 faixas saem 6,1 g. Mexer na largura de 9 para 11 mm rende
0,7 g (e ainda tira colunas, porque a margem de canto cresce). Duas faixas é o
mínimo razoável: a nervura do meio é o que segura a parede contra embarrigar
sob a pilha.

#### Onde o peso está — medido por faixa de altura

(remedido na peça atual da configuração C, **179,2 g** — três faixas de
listra, tudo fechado, aba para fora com a dobra)

| | peso | % |
|---|---|---|
| pés + saia (z 0–5) | 2,5 g | 1% |
| **chapa do fundo (5–7)** | **52,2 g** | **29%** |
| banda cega do pé (7–40) | 36,1 g | 20% |
| parede vazada (40–111) | 48,3 g | 27% |
| faixa do rim + aba (111–133) | 40,1 g | 22% |

A faixa do rim subiu de 32,1 para 40,1 g ao virar a aba para fora: a dobra de
5 mm corre todo o perímetro. É o preço de extrair em molde de duas placas, e
está pago — sem ela a peça não sai (§4.2.5).

A parede vazada é só **27%** da peça — é por isso que otimizar listra dá pouco.
A **chapa do fundo é 29% e está intacta**: o vazado nunca chegou nela. Vazar o
fundo (como as cestas da referência do cliente fazem) é a única alavanca de
peso que sobra de verdade, e é decisão do cliente porque muda a função de
conter. As outras duas: a banda cega de 33 mm no pé da parede (20%) e a faixa
do rim de 3,2 mm (22%), que é onde mora a aba e o acoplamento.

Arquivos: `cad/listras.py` (folha `listras.png`); `VAZADO = "listra"` ou
`"bolinha"` em `modelo3d.py` alterna os dois desenhos.

#### Os dois furos do pé, fechados — e um teorema de molde

Pedido de 22/09: "é o tamanho P, ou seja, a usabilidade dele é para coisas
pequenas, miúdas — portanto tanto o furo da base do pé quanto o furo da
frente, na parte inferior colada com a base, precisam ser fechados".

Os dois furos eram **o mesmo sólido**. A cavidade do pé é um bloco vertical e,
subtraída da peça inteira, ela não esvaziava só o pé:

| | medido |
|---|---|
| slots na chapa do fundo | 2 × 31,8 × 7,4 mm = **194 mm² de furo** |
| a parede abria em | **z = 1,6 mm** — rente ao piso |

Eram dois caminhos do interior do cesto direto para a mesa. Qualquer coisa
miúda apoiada no fundo saía pelo slot da chapa; o que entrasse pela janela da
parede descia dentro do pé e saía por baixo.

**A correção.** A janela na parede só é necessária onde o pé da peça
ENCAIXADA passa, isto é de `z = passo de encaixe` (46,8 mm) para cima. Abaixo
dali ela furava a chapa e a parede a troco de nada. Então `Z_CAV = 40` (a cota
onde começa a primeira faixa de listras, para o desenho não brigar), e o que
esvazia o pé nos 40 mm de baixo é uma **bolsa cega** aberta no piso,
`_pe_bolsa()`, separada da cavidade por uma membrana de 2 mm.

Remedido na configuração C (é o que a folha `fechado.png` mostra hoje; o furo
de 194 mm² acima é a medição original, a 12° de saída — a 6° o mesmo defeito
abre 243 mm²):

| | antes | depois |
|---|---|---|
| furo na chapa do fundo | 243 mm² | **0 mm²** |
| parede abre em z = | 1,6 mm | **40 mm** |
| passo encaixado | 35,54 mm | **39,98 mm** |
| passo empilhado | 130,00 mm | 130,00 mm |
| peso em PP | 175,9 g | **179,2 g** |

(os pesos absolutos são os da peça ATUAL; o delta da correção do pé continua
sendo +3,3 g. O passo encaixado *piora* de 35,5 para 39,98 mm, e isso é
correto: com a sola furada a peça de cima descia mais do que devia — os
35,5 mm eram uma cubagem que só existia porque o fundo estava aberto)

Provado por interseção booleana: `cavidade ∩ parede (z<40) = 0`,
`cavidade ∩ chapa = 0`, e o mesmo para a bolsa. Medindo a seção cota por cota,
todo o material que falta abaixo de 40 mm é **exatamente** a bolsa (224 mm² em
z = 12, 201 em 20, 172 em 30) e nada mais.

**O teorema que apareceu no caminho.** Com dois postiços que saem em +z e −z
não existe pé oco COM sola fechada. Quem forma a cavidade do pé só chega lá de
cima, pela janela; se a parede fosse inteira, esse macho seria um dedo solto
dentro do pé, e como o cone recua 0,213 mm/mm descendo enquanto a face externa
do pé só avança 0,046, o dedo **engrossa para baixo** — contra-saída. Pela
outra via, uma bolsa puxada de baixo tem de ser mais larga no piso, então não
pode ter chapa por cima dela. Logo: **onde o pé é oco a parede é vazada, e onde
a parede é cega o pé é esvaziado por baixo.**

O preço é a sola: nos 40 mm de baixo ela deixa de ser chapa e vira **coroa**,
como o fundo de um balde. Na C o apoio de cada pé na aba vai de 100,1 para
**32,1 mm²**, e o tripé completo mede **469 mm²** de contato de face plana
(415 na canetinha de trás + 27 em cada pé da frente) — mais que os 390 mm² da
versão com a aba para dentro, porque a aba virada para fora dá ao pé uma
faixa de pouso mais larga. Numa coluna de 4 com 1 kg em cada, o pé pega
13,2 N: pressão de contato 0,48 MPa contra ~30 de escoamento do PP (60×), e a
saia flete 0,003 mm trabalhando a 0,41 MPa.

#### O empilhamento: a dúvida do cliente estava certa pelo motivo certo

"Pela minha conta, o empilhamento talvez não funcione, medi a distância dos
pés com o apoio e aparentemente não vai dar certo."

O número que ele mediu existe: **o pé cobre só 3,1 mm dos 10 mm de aba**, e
cobre a borda INTERNA dela — a ponta do lábio em balanço, não a raiz apoiada
na parede (que começa em x = 96,25). Mas o empilhamento fecha: passo
**exatamente na altura, 130,00 mm, com 0,0000 mm³ de interferência**, tripé de
390 mm², e as contas acima dão 34× e 5× de folga.

O que **não** fechava era outra coisa, que só apareceu ao medir: a folga de
montagem do berço do friso era de **0,21 mm em x** — menos que a tolerância da
própria injeção (±0,4 mm em 200 mm de PP, 0,2%). Na prática as duas peças
podiam nem assentar. Duas correções:

- `FRISO_F` 0,3 → **0,8 mm**: a folga medida vai para ±0,91 mm em x e ±1,22 em
  y, e o berço continua travando — para escapar da aba o pé precisa andar
  3,1 mm, e para voltar à posição de encaixe, 21 mm.
- `FRISO_S = 8°` de saída nas pernas do friso. Eram caixas de 0 grau: ruim para
  o molde e, pior, o berço não tinha boca. Com saída o friso afina no alto, ou
  seja o **berço abre para cima** — o pé cai num funil e se centra sozinho.

Arquivos: `cad/fechado.py` (folha `fechado.png`, com a chapa do fundo em planta
antes/depois tirada do próprio sólido). `cad/aba.py` passou a **medir** os
apoios e a folga do friso em vez de trazê-los digitados na tabela, que já
tinham envelhecido calados uma vez.

#### Três faixas de listra, e o rasgo em um terço

Pedido de 22/09, a última alteração de forma: "os rasgos verticais, temos duas
linhas, eu quero deixar com 3 linhas, ou seja os rasgos verticais ficarão
menores... esse produto é para organizar peças pequenas, tem um perigo dos
produtos saírem por esses rasgos atuais, então preciso diminuir a altura e
largura desses buracos".

O número de faixas não é digitado: sai da altura-alvo `LIS_H`, e `listras()`
recalcula a altura real para as faixas preencherem exatamente o campo entre
`BANDA` (40) e `z_topo` (111). Com `LIS_H = 18` dá n = 3 e altura real de
18,33 mm. Largura 10 → **6 mm**, e o passo 15 → **11**, para a nervura entre
listras continuar em **5 mm** — o ritmo do desenho não muda, só o vão.

Remedido na configuração C (é o que a folha `rasgos.png` mostra hoje):

| | antes | depois |
|---|---|---|
| faixas | 2 | **3** |
| rasgo | 10 × 31,5 mm | **6 × 18,3 mm** |
| vão por rasgo | 315 mm² | **110 mm²** — um terço |
| nervura entre rasgos | 5 mm | 5 mm |
| nº de rasgos | 61 | 123 |
| área aberta total | 18.147 mm² | 12.134 mm² |
| peso em PP | 171,6 g | **179,2 g** |

**O achado que mudou a decisão: o peso quase não depende da largura do rasgo.**
Estreitar a listra encurta o passo, entram mais colunas e a área aberta se
mantém. Varredura das oito combinações com 3 faixas (peso em PP e nº de
rasgos, que é custo de fecha-macho no molde):

| W/P | rasgos | peso | área aberta |
|---|---|---|---|
| 8/13 | 101 | 178,2 g | 12.914 mm² |
| 7/12 | 117 | 177,8 g | 13.250 mm² |
| 6/13 | 111 | 180,7 g | 10.906 mm² |
| **6/11** | **123** | **179,2 g** | **12.134 mm²** |
| 6/10 | 139 | 177,2 g | 13.684 mm² |
| 5/11 | 123 | 181,6 g | 10.253 mm² |
| 5/9 | 165 | 177,2 g | 13.735 mm² |
| 4/8 | 181 | 179,1 g | 12.199 mm² |

4,4 g de espalhamento numa peça de 179 — e a variação segue a **área aberta**,
não a largura. Quem pesa são duas outras coisas: o **número de faixas** (+7,6 g
de 2 para 3, porque cada faixa a mais é uma nervura de 8 mm dando a volta na
peça inteira, o que também é o que segura a parede contra embarrigar sob a
pilha) e a área aberta total. Logo o tamanho do rasgo é decisão de **função** —
o que não pode passar por ele — e não de peso.

Se quiser barrar também o que tem 5 mm: `5/9` custa o mesmo peso (166,7 g) e
sobe de 123 para 167 rasgos, 44 fecha-machos a mais. `4/8` já são 183.

A frente fica com **duas** faixas em vez de três porque o arco da borda só
deixa 82,2 mm de altura útil ali; as faixas dela são recalculadas para
preencher essa altura (17,08 mm cada), o que desalinha a nervura horizontal na
quina em 1,25 mm — medi as duas leituras e renderizei: é indistinguível, e a
alternativa (usar as faixas da lateral e deixar a segunda ser cortada pelo
arco coluna a coluna) dá exatamente os mesmos 135 rasgos e o mesmo peso.

Encaixe e empilhamento não mudam — os rasgos moram na parede, longe do pé, da
aba e do friso. Medido na C: encaixa 39,98 mm, empilha 130,00 mm, 0,0000 mm³.

Arquivos: `cad/rasgos.py` (folha `rasgos.png`, com o rasgo em tamanho real e o
gráfico peso × largura). `VAZADO = "nenhum"` em `modelo3d.py` constrói a peça
de parede cheia (**194,6 g** na C), que é a referência para medir a área
aberta.

#### O rasgo inferior frontal — e a lição de método

"O rasgo inferior frontal ainda está ali, eu quero fechar ele tmb... aqui corre
o risco dos produtos colocados nele escorrer e sair pelo buraco."

Estava. O **chanfro do pé** (45°, `CHANFRO_PE = 36`) é a reta y = −89 − z; a
parede externa é y = −(97,37 + 0,2126 z). Elas se cruzam em

    z = (CHANFRO_PE − (PROF/2 − BASE_Y/2)) / (1 − tg θ)

que dava **10,63 mm** aos 12° de saída em que o defeito foi encontrado, e dá
**24,96 mm** aos 6° da configuração C. **Abaixo dessa cota o chanfro passa por
dentro da parede e a apaga.** Como a chapa do fundo termina em z = 7, sobrava
rasgo de **z 7,0 a 8,75 mm** (1,8 mm de altura) em 130 mm de frente =
**237 mm²** a 12°, e **928 mm²** a 6° (faixa de z 7 a 13, até 152 mm de
largura), com a borda da chapa servindo de rampa para ele. Acima dali a parede
sobrevivia como **lâmina de 0 a 1,4 mm** — seção que não enche na injeção.

Que a cota dependa da saída é exatamente onde a primeira versão da tapa
tropeçou: ela tinha a faixa em 14 mm, fixa. Ver §4.2.6.

**A lição.** Os testes anteriores não pegaram isso, e a razão é instrutiva: eu
media a parede *contra a casca já recortada pela silhueta*, e achava zero de
furo em toda a faixa de baixo. A referência tinha o mesmo rasgo — o chanfro
come a parede nas duas — então a comparação não podia enxergar o que faltava.
**Comparar contra uma referência que compartilha o defeito é não medir.**

O teste que pega não usa referência nenhuma: de um ponto dentro do cesto, 720
raios na horizontal; se um sai sem cruzar material, há caminho. Em z = 7,5 mm,
**135 raios saíam, todos entre 236° e 304°** — o setor que aponta para a
frente. Depois da correção: **zero, em todas as cotas de 7,5 a 39 mm**.

**A tapa** é uma parede de `T_PAREDE` deitada sobre o plano do chanfro: a
silhueta menos ela mesma deslocada `T_PAREDE/√2` em y e em z. Cortada por
`fora`, ela **termina sozinha** onde o chanfro sai da casca — não há cota para
acertar à mão, e se `CHANFRO_PE` mudar ela acompanha. Saída de molde: a face
externa dela *é* o plano do chanfro, que já é a silhueta da peça; a interna é
paralela, e subindo o vão só cresce.

Remedido na configuração C (é o que a folha `frente.png` mostra hoje):

| | antes | depois |
|---|---|---|
| rasgo frontal | 928 mm² | **0 mm²** |
| raios que escapam (z 7,5) | 165 de 720 | **0** |
| faixa aberta | z 7,0…13,0 mm, até 152 mm de largura | nenhuma |
| peso em PP | 174,5 g | **179,2 g** |

Custa 4,7 g na C (0,7 g eram a conta a 12°, quando a faixa a tapar tinha 1,8 mm
de altura em vez de 6), e por dentro fica uma transição chanfrada no pé da
parede da frente — que de quebra ajuda a varrer o cesto. Encaixe 39,98 e
empilhamento 130,00 inalterados.

Arquivos: `cad/frente.py` (folha `frente.png`, com o leque de raios em planta e
o corte no pé da frente em zoom 1:1).

#### As colunas de listra da lateral, ancoradas no pé

"Nas duas laterais, colado no pé, temos 3 buracos verticais que estão cortados,
retire eles, e aproxime os outros 3 furos para mais próximo do pé."

A grade de colunas da lateral vinha de `grade()`, **centrada em y = 0** — ela
não sabia da existência do pé. Com passo de 11 mm e o pé em y = −58, duas
colunas caíam em cima dele:

| coluna | folga até a pegada do pé (no topo do campo) | |
|---|---|---|
| y = −55 | −9,99 mm | dentro do pé, escondida atrás dele |
| y = −66 | −4,99 mm | **cortada pela aresta do pé** — a que o cliente viu |
| y = −44 | +1,01 mm | lasca de 1 mm de parede |
| y = −77 | +6,01 mm | a que ele pediu para aproximar |

Note a assimetria: 6,01 mm de um lado do pé e 1,01 mm do outro. E aquele
1,01 mm é justo onde o pé descarrega a pilha na casca — um ligamento de 1 mm
de largura por 1,4 de espessura, que não é parede.

A pegada do pé **cresce com z** (meia-largura `L/2 + ky·z`: 6,80 mm em z = 40 e
9,99 mm em z = 111), então quem manda é a cota mais alta do campo. `cols_lateral()`
gera as colunas **do pé para fora**, nos dois sentidos: a primeira de cada lado
a `LIS_FOLGA_PE = 4` mm da pegada, e dali em diante passo `LIS_P`. Assim a
nervura entre listras fica em `LIS_P − LIS_W` = 5 mm em toda a lateral e a folga
até o pé é 4 mm **dos dois lados, por construção** — não há cota para acertar à
mão, e se o pé mudar de posição ou de largura as colunas acompanham.

Remedido na configuração C (é o que a folha `colunas.png` mostra hoje):

| | antes | depois |
|---|---|---|
| colunas na lateral | 15 | **13** |
| colunas cortadas pelo pé | 2 | **0** |
| folga até o pé, dos dois lados | 6,01 e 1,01 mm | **4,00 mm** |
| nº de rasgos | 135 | 123 |
| peso em PP | 178,6 g | **179,2 g** |

Encaixe 39,98 e empilhamento 130,00 inalterados — as listras moram na parede,
entre z = 40 e 111, longe da aba, do friso e da chapa.

Arquivos: `cad/colunas.py` (folha `colunas.png`, com o antes/depois no mesmo
ponto de vista do print do cliente e a tabela de folgas).

### 4.2.5 A aba para DENTRO não extrai — medido

Pergunta do cliente (23/09): "pensando nas nossas injetoras, essa borda
superior para dentro possivelmente não conseguirá fazer a extração, confere?"

**Confere.** E o teste é um só, sem opinião: num molde de duas placas, um ponto
do espaço vazio é formável se **não houver material acima** dele na coluna (o
macho chega de cima) **ou não houver material abaixo** (a cavidade chega de
baixo). O que tem material dos dois lados e não é material precisa de gaveta,
postiço ou macho colapsável:

    preso(z) = sombra_de_cima(z) ∩ sombra_de_baixo(z) − material(z)

Medido em `cad/extracao.py`, cota a cota:

| | volume preso |
|---|---|
| peça como está | **58.242 mm³** |
| a mesma peça **sem a aba** | 6.064 mm³ |
| **portanto a aba responde por** | **52.178 mm³ — 90%** |

Os 6.064 mm³ que sobram são os **rasgos passantes** da parede. Eles entram na
conta pela definição (têm material acima e abaixo), mas ali o fechamento é na
própria superfície com saída da parede e a profundidade presa é só a espessura
dela — 1,4 mm, que zera depois de 1,4/tg 12° = 6,6 mm de curso. É por isso que
caixaria tem centenas de rasgos e se faz em molde de duas placas. Falso
positivo conhecido, anotado no script.

> **Os números acima são da peça de 23/09** — aba para dentro, saída de 12°.
> `cad/extracao.py` hoje roda a configuração C, então o que ele imprime é o
> pós-correção: **9.217 mm³ presos** com a aba, 9.224 sem ela (a aba responde
> por −7 mm³, ou seja, por nada), e a cota que decide vira contrafactual — se
> esta mesma peça tivesse a aba virada para dentro, ela avançaria 6,54 mm sobre
> uma boca interna de 173,1 mm, 7,6% por lado. Pior que a de 12°, porque a
> saída menor estreita a boca.

**A cota que decide** não é o volume, é a profundidade do ressalto: a aba
avança **6,27 mm para dentro da face interna da parede**, numa boca interna de
192,5 mm — **6,5% por lado**, em degrau contínuo de 2,5 mm. Bump-off em PP vive
na faixa de 1 a 2% por lado, em feição arredondada e local. 6,5% num lábio
contínuo de canto vivo não sai forçando: sai com macho colapsável (quatro
postiços angulares mais cunha central), que é custo de ferramental e item de
desgaste.

O teste também trata certo o **chanfro de topo**, que a primeira versão do
script acusava como contra-saída da cavidade. Não é: na frente do cesto, acima
da borda baixa, não há material nenhum na coluna, então aquele espaço é do
MACHO. O macho desta peça tem um lobo que desce na frente da parede baixa e
fecha contra a cavidade na própria aresta do rim — linha de fechamento
acompanhando a borda, o normal em caixaria.

#### Duas armadilhas de medição que apareceram aqui

1. **`to_2D()` do trimesh translada cada corte por conta própria** — medido:
   −45,4 mm em z = 57 e +20,2 mm em z = 128,5. Com ela as cotas ficam
   desalinhadas entre si e qualquer acúmulo cota a cota (como a sombra) sai
   lixo: a primeira rodada acusou 636.542 mm³. Corrigido com `to_planar` na
   identidade, x e y passam a ser os do mundo em todas as cotas.
2. **Com a parede vazada, "furo do polígono" não é o vão interno.** Um corte em
   z = 100 não é uma coroa: são ~60 ilhas, as nervuras entre listras. O vão
   tem de vir do sólido, não da topologia do corte.

Arquivo: `cad/extracao.py`. Depende de `networkx` e `rtree` (dependências
opcionais do trimesh): `pip install networkx rtree`.

### 4.2.6 A configuração C, e a varredura da borda

Escolhida a **C** — envelope de planta em 200 × 250, aba para fora, saída de
molde reduzida de 12° para 6° para devolver litragem. `ABA_DIR` (+1 fora, −1
dentro) e `set_envelope(larg, prof, saída, alt)` geram qualquer das variantes;
derivados novos: `aba_x0/aba_x1`, `pe_topo()` (a face externa do pé morre na
aresta livre da aba — é dali que vem a saída em x de que ele precisa para
telescopar) e `pe_r00()` (o piso do pé tem de alcançar a faixa de pouso).

As quatro remedidas depois da correção da silhueta e da tapa (é o que
`abafora.png` mostra hoje; `hoje` é a peça de 23/09 — aba para dentro, 12°):

| | hoje | A | B | **C** |
|---|---|---|---|---|
| aba / saída | dentro · 12° | fora · 12° | fora · 12° | **fora · 6°** |
| envelope | 204 × 240,9 | 224 × 250,9 | 204 × 230,9 | **204 × 235,1** |
| capacidade | 4,41 L | 4,41 L | 3,52 L | **4,09 L** |
| peso em PP | 169,0 g | 190,1 g | 165,6 g | **179,2 g** |
| passo encaixado | 46,80 | 39,99 | 39,99 | **39,99** |
| 12 peças | 647 mm | 572 mm | 572 mm | **572 mm** |
| preso no molde | 58.242 mm³ | 5.676 | 5.088 | **9.217** |
| **tripé de apoio** | 388 mm² | **62 mm²** | **62 mm²** | **469 mm²** |

A contra-saída acaba nas três; o que sobra é a linha de base dos rasgos
passantes. E o **encaixe melhora** de 46,80 para 39,99 mm porque a aresta
interna da aba deixa de ser o gargalo — 12% menos caixa. Como o passo passa a
ser `NERV_T` / saída em x do **pé**, que não depende da saída do **corpo**, a
saída fica livre para engordar a base: é o que C explora.

**A última linha é a que decide, e ela não estava na primeira comparação.** A
e B, que mantêm os 12° de saída, ficam com **62 mm² de tripé** — a 12° a base é
55 mm mais estreita que a boca e o pé não alcança a faixa de pouso da aba. Não
é questão de cubagem: A e B **não empilham**, pousam na quina. C não foi
escolhida por devolver 0,57 L a mais que B; foi escolhida porque baixar a saída
para 6° é o que traz o pé de volta para cima da aba — 469 mm², mais que os
388 da peça de 23/09. A litragem veio de carona.

#### A varredura pediu três adaptações

**1. `silhueta(folga)` para a aba — era um bug, não uma fragilidade.** O
recorte da silhueta do corpo amputava a aba nova em y: sobravam **0,26 mm** da
aba de trás em vez de 10, e a saia pousava no vazio. Era isso, e não o
deslocamento, o tripé de 60 mm² da primeira rodada. Com a aba recortada pela
sua própria silhueta (offset de `ABA_W`), o tripé volta a **473 mm²** — mais
que os 388 de hoje — e `DESLOC` fica em 21 mm.

**2. Dobra de 5 mm na aresta da aba.** Duas peças acopladas só se tocavam na
espessura da aba: abaixo de z = 127,5 as paredes estão 10 mm para dentro de
cada lado, um vão de 20 mm. O engate da cauda caía de **14 mm** (na versão com
aba para dentro, onde a fêmea escavava a faixa do rim) para **2,5 mm**. A
dobra devolve 7,5 mm de altura de junta, e de quebra enrijece e protege a
aresta — o "mini reforço" que o cliente intuiu. Medido: a trava a 1,2 mm de
deslocamento vai de 11,2 para **27,2 mm³**, e a soltura passa a exigir **7,5 mm**
de levantamento em vez de 2,5 (medido por busca binária; a primeira versão da
folha só amostrava 6 e 10 mm e relatava 10, enquanto `aba.py` relatava 8 — a
mesma peça com dois números). Custa 4,3 g. Sai do molde: a silhueta salta para
fora subindo (89,5 → 100 em z = 122,5) e o canal entre a dobra e a casca abre
para baixo, onde a cavidade chega.

**3. Vaziar a cauda de andorinha.** Era um bloco **maciço de 1.556 mm³ com 7 a
11 mm de espessura** numa peça de parede 1,4 — não fragilidade, o contrário:
massa que chupa a face externa do rim e manda no tempo de ciclo. Vaziada por
cima (o plano da junta, então sai reta): parede de 1,8 mm, seção máxima 3,3 mm,
a mesma do rim.

#### E uma quarta, achada na conferência antes de gerar os arquivos

A tapa do rasgo inferior frontal (§4.2.4) tinha a faixa em z **fixa em 14 mm**.
Aquele 14 não era uma cota do produto: era onde o chanfro de 45° do pé cruzava
a parede **a 12° de saída**. A C baixou a saída para 6° e o cruzamento subiu
para **24,96 mm** — a tapa cobria 14 e reabria ~11 mm de rasgo na frente, junto
da base. Exatamente o defeito que o cliente havia mandado fechar, de volta por
um número mágico.

> z_cruzamento = (CHANFRO_PE − (PROF/2 − BASE_Y/2)) / (1 − tg saída)
> — 10,63 mm a 12°, **24,96 mm a 6°**

Virou `z_chanfro_pe()` e a faixa passou a ser derivada (`z1 = z_chanfro_pe() +
2`), nunca mais literal. Conferido pelo teste de raios **sem referência** (o
mesmo da lição de método de §4.2.4): **0 de 1.440 raios escapam** em z = 7,5 ·
10 · 14,5 · 20 · 24 · 26 · 30 · 39 mm. Em z = 41 escapam 380 — é a primeira
faixa de listra, que é para estar aberta. Custa 2,7 g.

E o teste de acoplamento da folha `aba.png` estava medindo com o passo errado:
`LARG` (180 mm) quando a aba para fora move o passo para `LARG + 2·ABA_W`
(200 mm). Duas peças entravam 20 mm uma na outra e a "trava" acusava
7.551 mm³ de interferência no contato. `passo_acoplado()` agora considera
`ABA_DIR`; com o passo certo a trava mede **0 mm³ no contato**, 27,2 mm³ a
1,2 mm de afastamento, e a peça solta a **7,5 mm** de levantamento — a altura
da junta (`ABA_T` 2,5 + `ABA_DOBRA` 5), como tem de ser.

#### A borda precisa de reforço em todo o perímetro? Não

A seção **não mudou, só espelhou**: antes era uma alma de 3,2 × 14 mm com um
lábio de 10 × 2,5 virado para dentro; agora é a mesma alma com o mesmo lábio
virado para fora. O momento de inércia de um L espelhado é idêntico, então a
rigidez de aro contra ovalizar é a mesma de hoje.

Onde o empilhamento mudou, mudou para **melhor**. Hoje o pé pousa na ponta de
um lábio de 10 mm em balanço; na C ele pousa em x 86,6…94,0 — sobre o topo do
rim (86,8…90,0) **e** a raiz da aba (90…94), direto acima da parede. Braço de
flexão medido: **0,55 mm contra 4,75 mm**. A aba nem entra em flexão.

> **Sobre o 473 mm² do tripé:** as três folhas que medem o contato dão
> **469** (`aba.png`), **472** (`fechado.png`) e **473** (`varredura.png`). É a
> mesma área, medida com espessuras de fatia diferentes em cada script — o
> contato é uma face plana, então a "área" sai do volume de uma lâmina fina, e
> a lâmina não tem a mesma espessura nos três. A dispersão é de 0,9%; nenhuma
> conclusão depende dela. Não unifiquei porque cada folha mede o que ela
> própria afirma, e é assim que uma erra sozinha em vez de as três errarem
> juntas.

Coluna de 4 com 1 kg em cada (34,5 N na peça de baixo):

| | carga | área | tensão |
|---|---|---|---|
| pé (cada) | 13,2 N | 27,4 mm² | 0,48 MPa → 60× |
| saia | 8,1 N | 418 mm² | 0,41 MPa na aba, flecha 0,003 mm |
| parede em compressão | 26,4 N | 64 mm² | 0,41 MPa |

E o encaixe: o batente é **plano** — a membrana do pé, em z = 40 = `Z_CAV`.
Não é cunha, então não agarra. A interferência é 1,83 mm³ no passo e **zero já
a 1 mm acima**; parede-a-parede sobram 2,8 mm de folga e as cunhas do pé
liberam 4,4 mm antes do batente.

Arquivos: `cad/abafora.py` (folha `abafora.png`, as quatro configurações lado a
lado) e `cad/varredura.py` (folha `varredura.png`, a varredura da C com os três
vereditos e a seção da borda).

### 4.2.7 A linha ELO, e o ELO M

O nome da linha é **ELO** (decidido em 23/09). Ele diz o sistema — peças que
se encadeiam — sem prometer uma aparência que a peça não tem, e o slot do
qualificador na gramática da casa (`Cesto Organizador Vime 7 L`,
`Cesto Europa Juta 5,3 L`) aceita palavra de uso, não só de trançado
(`Cesto Transporta Tudo` é precedente). **Não conferi colisão de marca:** o
proxy desta sessão bloqueia o Mercado Livre e não tenho acesso ao INPI. Antes
de gravar em molde ou embalagem, vale busca na classe 21 e varredura nos
marketplaces.

O pedido do M trouxe um diferencial: **dois ELO P acoplados empilham
perfeitamente em um ELO M.** Não encaixam dentro — *empilham em cima*, com os
pés na aba do M, exatamente como um P empilha em outro P.

#### A largura do M não foi escolhida, foi derivada

A aba do P vai de 90 a 100 mm do eixo dele. Dois P acoplados no passo de
200 mm têm as abas **se encontrando exatas em x = 100**, e o conjunto vai de
−100 a +300: **400 mm de pegada de aba**. Para o M ter a mesma pegada, a aba
dele tem de ir de 190 a 200 do seu eixo, logo:

> boca do corpo do M = 2 × LARG_P + 2 × ABA_W = 2 × 180 + 2 × 10 = **380 mm**

E aí as paredes do M caem em **x = −90 e +290**, que é precisamente onde
pousam os pés externos do par. Medido: o envelope do M e o do par batem em
**0,00 mm nos três eixos** (404,0 × 235,1 × 132,5).

**A profundidade não muda: 230 nos dois.** É por isso que a silhueta lateral,
os chanfros da frente (52 / 36), o pé, a saia de trás, o friso e a tapa do
rasgo frontal ficam idênticos — só o x escala. `padrao_m()` em
`modelo3d.py` é uma linha: `set_envelope(380, 230, 6, alt=130, aba_dir=+1)`.

#### Os quatro requisitos, medidos

| | ELO P | **ELO M** |
|---|---|---|
| boca do corpo | 180 × 230 | **380 × 230** |
| envelope | 204,0 × 235,1 × 132,5 | **404,0 × 235,1 × 132,5** |
| capacidade | 4,09 L | **9,10 L** |
| peso em PP | 179,2 g | **298,7 g** |
| rasgos | 123 | **213** |
| **encaixa** | 39,99 mm | **40,00 mm** |
| **empilha** | 130,00 mm | **130,00 mm**, 0,0000 mm³ |
| **acopla** | passo 200, solta a 7,5 mm | **passo 400, solta a 7,5 mm** |
| tripé de apoio | 463 mm² | **463 mm²** — o mesmo |
| preso no molde | 9.217 mm³ | **12.877 mm³** |

**O tripé do M é o mesmo do P: 463 mm²** (medidos os dois pelo mesmo script,
`visor_elo.py`; as outras folhas dão 469 e 473 para o P pela tolerância da
fatia — §4.2.6). Ou seja **a saia de trás e os dois pés não escalaram com a
largura**: `SAIA_W` continua em 108 mm sobre uma traseira que agora tem
352,7 mm de fundo reto. Isso é decisão, e ela tem limite:

- Na carga do §4.2.6 — coluna de 4 com 1 kg em cada — a pressão de contato do
  pé vai de 0,48 para **0,53 MPa**, porque a carga é dominada pelo conteúdo e
  não pelo peso da peça. Passa com ~57× de folga.
- Mas se o M for carregado **proporcional ao volume** (2,2× o conteúdo do P), a
  pressão dobra para ~1,0 MPa. Ainda passa (~30×), e é onde a conta deixa de
  ser confortável.

**Então: se o M for vendido para carga pesada, `SAIA_W` deve escalar** — sobra
fundo reto para levá-la de 108 a ~308 mm sem tocar em nada mais. Não escalei
porque isso é massa (e o M já pesa 298,7 g) e porque a decisão depende do uso,
que é do cliente. Está anotado na §7.

**Fora isso, nada precisou ser adaptado.** Não é sorte: toda cota do modelo é derivada de
`LARG`, e o que dita a silhueta, os chanfros, o pé e a tapa é a
**profundidade**, que não mudou. As duas verificações que importavam passaram
sem toque: **0 de 720 raios escapam** em z = 7,5 · 12 · 20 · 26 · 30 · 39 mm
(a tapa frontal continua fechada, porque `z_chanfro_pe()` depende de `PROF` e
`BASE_Y`), e a auditoria de extração dá **12.877 mm³**, a mesma linha de base
de rasgo passante do P escalada pelos 213 rasgos — nenhuma contra-saída nova.

**E o M é uma peça mais eficiente que o P: 32,8 g/L contra 43,8.** Isso é
geometria outra vez — dobrar a largura dobra o volume mas não dobra a área de
parede. A 32,8 g/L o M encosta nos 30,4 g/L do Cesto Vime 7 L (047) da casa,
enquanto o P fica 44% acima. Se a conversa de custo por litro aparecer, é o M
que defende a linha, não o P.

**O passo de encaixe é o mesmo nos dois tamanhos (40,00 mm), e não é
coincidência.** Quem manda nele é a saída em x do **pé**, que não depende da
largura do corpo (§4.2.6). Por isso o M cuba tão bem quanto o P: 12 peças em
**573 mm nos dois tamanhos** — os 572 que aparecem em outras folhas para o P
são a mesma caixa medida com passo de 39,99 em vez de 40,00, ou seja a
tolerância da busca binária, não um milímetro de diferença real.

#### O empilhamento do par, medido

| | |
|---|---|
| passo | **130,00 mm** — o mesmo do P sobre P |
| desloca em y | **21 mm** — o mesmo `DESLOC` |
| interferência | **0,0000 mm³** |
| contato | **873 mm²** = 410 + 410 + 27 + 27 |

Os 873 mm² são as **duas saias de trás pousando inteiras** mais os **dois pés
externos**. Os dois pés internos ficam sobre a boca do M, no vazio, e não
fazem falta: 873 mm² é **1,9× o próprio tripé do M** (463 mm²).

**E de graça:** com deslocamento **zero** em y o par não empilha — **encaixa
dentro do M**, a 40,00 mm. O mesmo deslocamento de 21 mm que troca encaixe por
pilha no P troca também aqui.

#### O que o M custa no parque

| | |
|---|---|
| área projetada | 404,0 × 235,1 = **950 cm²** |
| fechamento a 0,32 t/cm² + 10% de canal | **334 t** |
| máquina a 80% | 418 t → **classe de 600 t, 1 máquina na casa** |
| a 0,28 t/cm² | 293 t → 366 t → **classe de 380 t, 3 máquinas** |

**É a única má notícia do M, e ela está na premissa, não na peça.** A 0,32
t/cm² o M fica refém da única 600 t da casa — exatamente o argumento que usei
contra as 2 cavidades no P (§5). A 0,28, que é defensável para parede de
1,4 mm e pressão baixa, ele entra na classe de 380 t com três máquinas. **Não
é número meu: é para o processador confirmar antes de fechar ferramental.**
Também não há como fugir engordando ou afinando a peça — os 950 cm² são a
pegada de dois P, e é ela que entrega o diferencial.

Arquivos: `cad/visor_elo.py` (gera `visor-elo.html`, o visor da linha, e
`elo-medidas.json`) e `cad/elo.py` (folha `elo.png`). `padrao_m()` em
`modelo3d.py` fixa a configuração do M.

### 4.2.8 O ELO M de 25 L, e o piso geométrico que quase impediu

Pedido de 23/09: "o organizador M com aproximadamente 30 litros com menos de
500 g, é possível?", e na sequência: **"eu baixaria um pouco mais a altura, e o
G que você criou é o M... deixe aproximadamente 25 litros"**. A resposta curta
é **sim, mas não com a parede do P**.

O que ficou: o **M da linha é a peça de ~25 L**, e o M de 9,10 L da §4.2.7
passou a ser etapa (`padrao_m9()` no modelo). A linha é **P + M**.

#### O piso geométrico, antes de desenhar qualquer coisa

Uma caixa de topo aberto com 30 L, na **proporção ótima possível**
(391 × 391 × 196 mm), com parede uniforme de 1,4 mm e **sem rim, sem aba, sem
pé e sem chapa reforçada**, pesa **583 g**. Travar a largura em 380 não muda
nada — dá 583 g também, porque 380 já é quase a proporção ótima. Para fechar
em 500 g a parede teria de ser **1,20 mm**, abaixo do mínimo da casa.

Medido, com a arquitetura inteira do ELO e o vazado do P (8% de parede
aberta):

| candidato | capacidade | peso |
|---|---|---|
| 380 × 230 × 450 (planta travada, só altura) | 31,39 L | **640,0 g** |
| 380 × 300 × 300 (quase cúbica) | 29,32 L | **631,4 g** |
| 380 × 400 × 220 (mais rasa) | 29,55 L | **630,0 g** |

Ou seja: **a forma quase não importa** — 30 L com o vazado do P custa 630 g,
±1%. O que importa é quanto da peça é buraco.

#### As duas alavancas, e por que só agora puderam ser puxadas

O cliente definiu que o 30 L guarda **coisa volumosa**, não miudeza. Isso
libera as duas alavancas que o P tinha travadas:

1. **Rasgo de parede maior** — de 6 × 18,3 para **14 × 34 mm**, passo 22.
2. **Chapa do fundo VAZADA** — a alavanca que o §4.2.3 vinha apontando como "a
   única que sobra de verdade" e que o cliente havia recusado no P, porque
   miudeza escapa. Numa peça de 30 L a chapa sozinha pesa ~244 g.

Medido, na primeira altura testada (220 mm, 29,55 L):

| | peso | o que falta |
|---|---|---|
| parede cheia e chapa inteira | 677,9 g | — |
| só o vazado da parede | **564,0 g** | −113,9 g |
| só o vazado da chapa | **570,9 g** | −107,0 g |
| os dois | **457,0 g** | −220,9 g |

**Nenhuma das duas alavancas fecha sozinha os 500 g** — cada uma para em
564-571 g. As duas juntas passam com 43 g de folga. A primeira vez que
escrevi esta tabela eu tinha −102 e −119, porque estimei a chapa maciça em
244 g em vez de medi-la; medidas, as duas alavancas valem quase o mesmo.

Baixando a altura para **190 mm**, que é o que o cliente pediu ao fechar em
~25 L:

**ELO M: 420,7 g · 25,52 L · 16,5 g/L · 149 rasgos · envelope
404,0 × 407,4 × 192,5 mm.**

Sobram **79 g** do limite de 500. Vale registrar o que esse folga compra: com a
**chapa inteira** a peça iria para ~528 g — ainda acima dos 500, então o vazado
do fundo continua obrigatório, mas por pouco. Uma chapa **parcialmente** vazada
cabe no orçamento.

**16,5 g/L contra 30,4 do Cesto Vime 7 L da casa** — o M é quase o dobro de
eficiente que o melhor comparável, e a razão é geometria mais vazado, não
mágica.

#### A premissa do cliente estava meio certa, e a medição disse qual metade

O pedido dizia "o comprimento precisa ficar igual para poder empilhar os 2
organizadores acoplados". Não é bem isso: **as duas dimensões da planta
travam o empilhamento**, cada uma por um apoio diferente.

| M | contato do par | ilhas |
|---|---|---|
| 380 × 230 (o M de hoje) | **887 mm²** | 416 + 416 + 27 + 27 |
| 380 × **300**, par centrado | **54 mm²** | 27 + 27 |
| 380 × 300, **par recuado 56 mm** | **887 mm²** | 416 + 416 + 27 + 27 |

Os **pés laterais** do par pousam nas abas laterais — travam a **largura em
380**. As **duas saias de trás** pousam na aba de trás — e num G mais fundo,
com o par centrado, elas caem no vazio: 94% do contato some e o par tomba.

**A saída não custa nada:** recuando o par até as saias encontrarem a aba de
trás do G, o contato volta inteiro. Então a profundidade **é livre** — o par
só não fica centrado, encosta atrás e deixa a frente do G aberta. Foi a opção
que o cliente escolheu, e é o que torna o G possível: com a planta travada em
380 × 230, 30 L exigiriam **450 mm de altura**, e aí o passo de encaixe sai de
40 para ~112 mm — 12 peças passariam de 573 mm para 1,3 m de caixa.

#### Um defeito que a mudança de profundidade revelou

As listras da frente e do fundo estavam plantadas em **y = ±95,0 literal** —
que é `PROF/2 − 20` para os 230 mm do P. Com `PROF = 400` o prisma de corte
passa a 60…130 enquanto a parede está em 200: **erra a parede inteira**. Os
três candidatos da tabela acima foram medidos assim, com frente e fundo
maciços — ou seja os 630 g são conservadores. Virou `y_parede()`.

#### O M de 190 mm, medido

| | a 190 mm (o M da linha) | a 220 mm (a primeira tentativa) |
|---|---|---|
| capacidade | **25,52 L** | 29,55 L |
| peso | **420,7 g** | 457,0 g |
| rasgos | 149 | 203 |
| **par recuado** | **190,00 mm · 0,0000 mm³ · 879 mm²** | 220,00 · 0,0000 · 886 |
| par CENTRADO | **53 mm²** — tomba | 54 mm² |
| empilha consigo | **190,00 mm · 0,0000 mm³** | 220,00 · 0,0000 |
| encaixa consigo | **64,65 mm** | 64,65 mm |
| acopla | passo 400 · solta 7,5 mm | idem |
| tripé próprio | 362 mm² | 476 mm² |

O contraste entre **879 mm² recuado e 53 mm² centrado** é a medição que
sustenta a §4.2.8 inteira: sem o recuo o par não pousa, e é o recuo que libera
a profundidade do M.

**Eu previ que baixar a altura melhoraria a cubagem, e a medição me
desmentiu.** A conta que fiz foi `NERV_T` dividido pela saída em x do pé,
`(ABA_W − ABA_POUSO)/ALT`, que daria ~44 mm a 190 de altura. Medido, o passo
de encaixe a 190 mm é **64,65 mm — exatamente o mesmo de 220**.

Ou seja **quem manda no encaixe aqui não é a altura, é a SAÍDA**. O P e o M de
9,10 L, a 6°, encaixam a 40,00 mm; esta peça, a 3°, encaixa a 64,65 seja qual
for a altura. A 3° a parede recua 0,052 mm por mm de subida contra 0,105 a 6°,
então a peça de cima precisa subir o dobro para liberar a mesma folga.

**Se a cubagem do M precisar melhorar, a alavanca é a saída de molde, não a
altura** — e ela cobra litragem em troca, porque a 6° a base encolhe 40 mm em
cada direção numa peça de 190 mm.

**Os 42.598 mm³ presos são rasgo passante e mais nada.** Medi a mesma peça com
e sem o vazado da chapa: **42.598 mm³ nos dois casos**, igual até o dígito, e a
mesma faixa de z (1,5 a 209,5). A chapa vazada **não prende nada** — e é o que
a teoria dizia, porque acima de um rasgo da chapa não há material nenhum, só o
interior do cesto, então o macho chega lá de cima. O número é 3,3× o do M
porque os rasgos da parede do G têm 476 mm² cada contra 110 do M.

O teste de raios era o que mais me preocupava — a tapa da frente depende da
saída, e o G é a primeira peça a 3° (§4.2.6 conta como um 14 fixo reabriu
11 mm de rasgo quando a saída caiu de 12 para 6). A 3° ela continua fechada.

**O preço do G é a cubagem.** O passo de encaixe vai de 40,00 (P e M) para
**64,67 mm**, porque a saída em x do pé é `(ABA_W − ABA_POUSO)/ALT` e o G tem
220 mm de altura contra 130. Em caixa: **12 G ocupam 934 mm contra 573 mm de
12 M**. É consequência da altura, não do vazado, e não tem conserto sem mexer
na aba.

**E uma que não foi medida de jeito nenhum: a rigidez da chapa vazada.** Tirei
107 g dela; com ~40% de furo e 1,4 mm de nervura entre rasgos, numa peça de
30 L com carga volumosa isso pede ensaio ou nervura cruzada. Pesei, não
calculei flexão.

Arquivos: `padrao_g()` e `_vazado_fundo()` em `modelo3d.py`. O visor
`cad/visor-elo.html` passou a ter as **três malhas** e dez cenas, entre elas "A
linha" (P, M e G lado a lado), "Dois P no G" e "G encaixados". `visor_elo.py
--rapido` redesenha a página lendo `elo-medidas.json`, sem reconstruir os
sólidos — remedir custa mais de uma hora de booleano em peças de 200+ rasgos.

Conferido: sintaxe do JS com `node --check`, as três malhas decodificadas em
node (índice máximo < nº de vértices, caixas batendo em 204,0 × 235,1 × 132,5 ·
404,0 × 235,1 × 132,5 · 404,0 × 407,4 × 222,5) e as dez cenas renderizadas no
Chromium headless.

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
paredes, então **não reduzem a área projetada** — o que conta é o footprint, que na configuração C
é o envelope real **com a aba**: 204,0 × 235,1 = **480 cm²** (era 430 com a aba para dentro).

| Cavidades | Fechamento | Máquina | Uso | Máquinas disponíveis | Ciclo est. | Produção |
|---|---|---|---|---|---|---|
| **1** | 169 t | **250 t** | 68% | **9** | 22 s | 164 pç/h |
| 2 | 338 t | 600 t | 56% | 1 | 24 s | 300 pç/h |

(a contagem por classe vem do `PARQUE` em `economia.py`: 12 máquinas de 200 t, **9 de 250 t**,
1 de 280, 1 de 300, 3 de 380 e 1 de 600. As etiquetas INJ da classe de 200 t estão no estudo da
caixa dobrável; não levantei as da classe de 250 t)

**A aba para fora custou uma classe de máquina.** Os 50 cm² a mais de footprint levaram o
fechamento de 151 para 169 t, o que tira a peça dos 200 t (limite de 160 t a 80%) e a põe nos
250 t. A casa tem **9 máquinas** de 250 t contra 12 de 200 t — ainda é classe abundante, mas é
uma perda real, e é o preço de extrair em molde de duas placas (§4.2.5). Não há como devolvê-la
sem desvirar a aba: a aba é o pouso da pilha e o plano do acoplamento.

**Recomendação: começar com 1 cavidade.** Não é só o custo do molde (USD 19,5 mil contra 34 mil):
a versão de 2 cavidades **empurra o produto para a classe de 600 t, onde a casa tem 1 máquina**,
enquanto 1 cavidade roda na classe de 250 t, onde tem **9**. Para uma commodity que vai precisar
de horas de máquina em volume, disputar 1 máquina é inviável.

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

Recalculado para os **179,2 g** da configuração C:

| Cenário | Custo | Preço | Margem | Contribuição | Pacote de 10 |
|---|---|---|---|---|---|
| Virgem RP 141 (R$ 15/kg custo) | R$ 2,69 | R$ 4,58 | 41% | R$ 1,89 | R$ 45,80 |
| Moído + pigmento (R$ 11,50/kg custo) | R$ 2,06 | R$ 4,58 | 55% | R$ 2,52 | R$ 45,80 |

Resina no cenário virgem: 0,1792 kg × R$ 9,54 = **R$ 1,71** por peça.

**Sobre o preço adotado.** Nas versões anteriores eu precifiquei por R$/kg, o mesmo critério do
custo. Está errado como critério de preço: **a regra por kg penaliza a redução de peso**. O
mercado paga pela função e pelo tamanho, não pelos gramas. Então adotei o preço do comparável
direto — **R$ 4,58 do Cesto Vime 7 L (047)**. Contra os 230 g da primeira geometria, os 179,2 g
de hoje derrubam o custo em R$ 0,76 sem derrubar o preço.

A R$ 1,12/L o produto fica acima do 047 (R$ 0,65/L), o que é esperado: 4,09 L com empilhamento e
encaixe vale mais por litro que 7 L de cesto simples. Se o comercial achar o preço agressivo,
R$ 3,99 ainda entrega **33%** de margem no cenário virgem.

> **Esta seção e a 6.5 usam bases de preço diferentes, e isso é deliberado.**
> Aqui o preço é o do comparável (R$ 4,58, fixo). O `economia.py`, que gera a
> tabela de payback de 6.5, ainda precifica por R$/kg — é a base da casa, e é
> por isso que lá a peça mais pesada "rende mais". Os dois caminhos dão
> **5,8 e 6,2 meses** de payback a 150 mil/ano em virgem; a diferença é de 0,4
> mês e nenhuma decisão depende dela. Se for para unificar, a base certa é a
> desta seção — preço de função, não de grama — e aí o payback é o de 5,8.

**A cor laranja é o que decide entre os dois cenários.** A casa compra PP moído **branco**
(R$ 7,69/kg, 124 t/ano) e **preto** (R$ 6,19/kg, 337 t/ano) — não laranja. Laranja em moído exige
lote dedicado de moído claro mais masterbatch, com risco de variação de tom entre lotes. É uma
pergunta para a produção, e vale **R$ 0,63 por peça** (R$ 94 mil/ano a 150 mil peças).

### 6.3 Resina

| Resina | Preço | Volume 12 m | Leitura |
|---|---|---|---|
| **PP RP 141 randon fluidez 40** | R$ 9,54/kg | 299,1 t | **Recomendada** — fluidez é o que uma parede de 1,4 mm sobre 480 cm² pede |
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
| 60.000 | virgem | R$ 107,5 mil | 15,4 meses | 367 h |
| 60.000 | moído | R$ 134,4 mil | 12,3 meses | 367 h |
| **150.000** | **virgem** | **R$ 268,8 mil** | **6,2 meses** | 917 h |
| 150.000 | moído | R$ 336,0 mil | 4,9 meses | 917 h |
| 300.000 | virgem | R$ 537,6 mil | 3,1 meses | 1.833 h |
| 300.000 | moído | R$ 671,9 mil | 2,5 meses | 1.833 h |

> **O payback melhorou porque a peça engordou, e isso é artefato do modelo.** A
> casa precifica em R$/kg, então mais massa é mais contribuição por peça:
> 179,2 g rendem R$ 1,79 contra R$ 1,71 dos 170,8 g. Não leia isso como
> "engordar a peça é bom" — o mercado não paga por grama num organizador de
> R$ 4,48. O que a tabela diz é só que o ferramental se paga rápido nos três
> volumes, e isso continua verdade com qualquer peso desta faixa.

Referência de volume: o **041 (Organizador Multiuso 3 divisórias) vendeu 262 mil unidades em 12
meses** para 1.847 clientes — é o campeão de volume da casa em organizador pequeno. Se o cesto
novo chegar à metade disso (131 mil/ano), o payback é de 7,8 meses em virgem.

---

## 7. O que falta — e o mais importante primeiro

| Item | Gravidade | Por quê |
|---|---|---|
| **Capacidade de 4,09 L é suficiente?** | **Alta** | O chanfro do pé já caiu de 52 para 36 mm para devolver volume. Levá-lo a 24 mm devolve ~0,2 L a mais, sem tocar no acesso frontal. A saída já foi de 12° para 6° por esse motivo (§4.2.6) |
| **Amostra física** | **Alta** | O passo do encaixe e o engate exato da saia nos berços do rim |
| **Passo do encaixe** | **Alta** | É a promessa de embalagem do pacote de 10. Medir na amostra ou em protótipo impresso (seção 4.2) |
| Preço do anúncio de referência | Alta | **Não consegui abrir** — o proxy da sessão bloqueia o Mercado Livre. Precisa do preço do pacote de 10 para validar o cenário de preço |
| Volume-alvo de venda | Alta | É o que decide o payback. Sobre cavidades a resposta mudou: 2 cavidades agora exigem 600 t, onde a casa tem **1 máquina** — acima de ~250 mil/ano a expansão é um segundo molde de 1 cavidade, não um de 2 (§5) |
| Laranja em moído é viável? | Média | Vale R$ 0,63/peça, R$ 94 mil/ano a 150 mil (seção 6.2) |
| Redução de peso | Média | A peça está em 179,2 g. A única alavanca grande que resta é perfurar a chapa do fundo (52,2 g, 29% da peça) — e o cliente pediu fundo fechado |
| **Custo e preço do ELO M** | **Alta** | O `economia.py` roda só o P. O M de ~25 L precisa do cenário próprio e de um comparável de preço — a casa não tem nada nessa litragem, então a analogia terá de vir de fora |
| **Pressão específica do M** | **Alta** | O M de 25 L tem 404 × 407 mm de planta — 1.645 cm², bem mais que os 950 do M de 9,10 L. É o que decide a classe de máquina, e o número de pressão específica é do processador, não meu (§4.2.8) |
| Marca "ELO" | Alta | **Não conferi** — sem acesso ao INPI e com o Mercado Livre bloqueado pelo proxy. Busca na classe 21 antes de gravar em molde ou embalagem |
| Ferramental do M | Média | Os USD 19,5 mil são a analogia do P. O M de 25 L tem ~1.645 cm² de planta contra 480 — precisa de analogia própria |
| **Carga da chapa vazada do M** | **Alta** | A chapa do M tem ~40% de furo e 1,4 mm de nervura entre rasgos. Numa peça de 25 L com carga volumosa isso precisa de ensaio ou de nervura cruzada — **não calculei flexão da chapa, só peso** |
| **Rasgo de 14 mm no M** | Média | Foi dimensionado para "coisa volumosa". Se entrar miudeza, o M precisa do vazado do P e sobe de peso na mesma proporção |
| `SAIA_W` do M escala? | Média | O tripé do M é o mesmo 463 mm² do P. Basta para a carga de referência (0,53 MPa, 57× de folga); se o M for para carga pesada, a saia de trás vai de 108 a ~308 mm sem mexer em mais nada (§4.2.7) |
| Cotas finais para a ferramentaria | Média | O pacote de cotas do molde ainda não foi fechado |
| Ângulo de abertura da frente | Média | `cad/abertura.png` tem três (chanfro de 40 / 52 / 68 mm); está em **52** por ser o medido no STL de referência, e ninguém escolheu outro |
| `ABA_DOBRA` de 5 para 3 mm? | Baixa | Devolve ~1,7 g e ainda deixa 5,5 mm de engate, 2,2× o de antes da dobra. Ficou em 5 mm por falta de resposta, e 5 é o conservador |
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
cad/angulo.py      sweep de saida de molde e a folha angulo.png
cad/cesto-final.step/.stl  a peca com tudo: pezinhos, estrutura de
                   empilhamento e cauda de andorinha do acoplamento
cad/aba.py         a arquitetura de 4.2.4 -- aba plana no rim, pes com
                   cavidade, cauda de andorinha na borda -- e a folha aba.png
cad/cortes.py      cortes 2D no eixo do pe, tirados do solido com
                   trimesh.mesh_plane, e a folha cortes.png
cad/friso.py       o friso em U na aba, com a trava medida nos 4 sentidos
cad/abertura.py    tres angulos de abertura no perfil, e a folha abertura.png
cad/limpo.py       a rodada de acabamento: traseira, pe da frente e planta
cad/listras.py     bolinhas vs listras e a tabela de onde o peso esta
cad/fechado.py     folha fechado.png: os dois furos do pe antes/depois, com
                   a chapa do fundo em planta tirada do solido
cad/rasgos.py      folha rasgos.png: duas faixas -> tres, o rasgo em tamanho
                   real e a varredura peso x largura (o peso nao segue ela)
cad/frente.py      folha frente.png: o rasgo inferior frontal, com o teste de
                   RAIO (de dentro para fora, sem referencia) que o pegou

cad/colunas.py     folha colunas.png: as colunas de listra da lateral antes e
                   depois de serem ancoradas no pe, com a tabela de folgas
cad/extracao.py    auditoria de EXTRACAO: mede o volume que nenhuma das duas
                   metades do molde alcanca (sombra de cima x sombra de baixo)
cad/abafora.py     folha abafora.png: as configuracoes A, B e C da aba para
                   fora, medidas lado a lado com a peca de hoje
cad/varredura.py   folha varredura.png: a varredura da C -- empilhar, acoplar,
                   encaixar, a secao da borda e as tres adaptacoes
cad/visor_elo.py   gera visor-elo.html (o visor da LINHA, com as duas malhas
                   e indice de 32 bits, porque o M passa de 65.535 vertices)
                   e elo-medidas.json, onde as medidas do M vivem
cad/elo.py         folha elo.png: o P, o M, e o par de P empilhado no M.
                   NAO remede -- le elo-medidas.json
cad/elo-medidas.json  as medidas do M, versionadas de proposito: custam ~40
                   min de booleano e sao o que permite redesenhar a folha

padrao_m() em modelo3d.py: o ELO M, 380 x 400 x 190 a 3 graus, com rasgo de
parede maior e CHAPA DO FUNDO VAZADA (_vazado_fundo()). E a chapa que fecha o
peso junto com o rasgo de parede -- medidas na altura de 220, valiam 107,0 e
113,9 g, e nenhuma das duas sozinha descia dos 500 g.
padrao_m9()        o M intermediario de 9,10 L: e nele que a largura de 380
                   foi derivada (2 x 180 + 2 x 10), e e o unico em que o par
                   pousa CENTRADO. Superado em 23/09.

O vazado da lateral: cols_lateral() gera as colunas ANCORADAS NO PE, nao numa
grade centrada em y = 0 -- e o que garante nervura de 5 mm em toda a lateral
e LIS_FOLGA_PE de folga ate a pegada do pe, dos dois lados.
cad/visor3d.py     regera a malha embutida e os numeros do visor3d.html a
                   partir do solido -- para o visor nao envelhecer calado
cad/visor3d.html   visor 3D interativo (artifact): o solido embutido em 823 KB
                   de binario e o desenho em WebGL2 escrito na propria pagina,
                   sem biblioteca externa -- gera-se dele os quatro modos
                   (peca, encaixadas, empilhadas, acopladas)
cad/print/         gcode em PETG: o da Anycubic (Kobra 3 / S1 / 3 Max, com o
                   macro G9111 no start) e os genericos Marlin nos bicos 0,4
                   e 0,6; os perfis .ini, o miniatura.py que injeta a
                   miniatura 230x110 que o PrusaSlicer headless nao desenha,
                   e o LEIA-ME com o que a impressao nao reproduz
cad/cesto-aba.step/.stl    O SOLIDO DO PROJETO -- configuracao C: aba para
                   FORA, 6 graus de saida, 204,0 x 235,1 x 132,5 mm, 179,2 g
                   em PP. E dele que saem o visor3d.html e os tres .gcode
```

**A regeneração é em cadeia, e nesta ordem:** `modelo3d.py` (`padrao()` fixa a
configuração) → `aba.py` exporta `cesto-aba.step`/`.stl` → `visor3d.py` troca a
malha embutida do visor → `prusa-slicer --load print/perfil-*.ini` refatia os
três gcode → `print/miniatura.py` injeta a miniatura no da Anycubic. Todas as
outras folhas leem `padrao()` direto, então podem rodar em qualquer ordem — mas
nenhuma delas alimenta o visor nem o gcode.
