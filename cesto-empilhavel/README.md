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
| Pé discreto | **Resolvido** — não há pé aparente: a parede desce 6 mm abaixo da chapa do fundo (seção 4.1) |
| Empilhar com acesso frontal | **Resolvido** — a saia de 6 mm assenta em 4 berços internos do rim; chanfro de topo de 52 mm dá o acesso |
| Acoplar lateralmente | **3 opções em 3D, todas com interferência zero** — a canaleta é horizontal e mora no rim; a vertical mataria o encaixe (seção 4.3) |
| Encaixar para reduzir volume | **Geometria confirmada** — saída de 3,5°/lado; **passo do encaixe a medir na amostra** (seção 4.2) |
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
| Pé | **saia de 6 mm** — a parede desce abaixo da chapa; nenhum pé aparente |
| Capacidade | **4,43 L** |
| Peso | **163,7 g** (180,9 cm³ de PP) |
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

#### O pé: não existe pé

Os quatro pés de canto foram removidos. No lugar deles, a **chapa do fundo sobe 6 mm** e a parede
continua descendo abaixo dela — o que apoia no chão é a própria parede, em todo o perímetro. É uma
**saia**, não um pé: de fora não há nada para ver, a base da peça está por cima e o apoio embaixo.

Três consequências:

- **Apoio contínuo.** 6 mm de aba em todo o contorno, contra 4 blocos de 32 × 32 mm. Não balança
  e não marca a bancada.
- **A chapa do fundo não toca o chão.** Fica 6 mm acima — água e poeira não chegam nela.
- **Sem sacrifício de desmoldagem.** A saia sai na direção de abertura, com a mesma saída de 3,5°.
  Nenhum movimento novo no molde.

O que o empilhamento perdeu com isso foi o batente: sem pé de canto, a peça de cima afundaria na de
baixo até encostar na parede. Voltou como **4 berços internos no rim** (30 × 10 × 5 mm, faces
superiores rasantes a z = 130), na face de dentro da parede engrossada. A saia da peça de cima
assenta neles. Ficam **dentro** da peça, invisíveis de fora, e mantêm o passo empilhado em
**exatamente 130 mm**. O chanfro de topo de 52 mm dá o acesso frontal sem desempilhar.

#### O que o pé custou em peso e em volume

| | Antes (4 pés de canto) | Agora (saia + berços) |
|---|---|---|
| Peso | 155,4 g | **163,7 g** |
| Capacidade | 4,50 L | **4,43 L** |

São **+8,3 g (+5,3%)**: a saia corrida pesa mais que 4 blocos de canto, e os berços somam ~4,9 g.
A R$ 9,54/kg de PP virgem isso é **R$ 0,08 por peça** — R$ 12 mil/ano a 150 mil peças. É o preço
de não ter pé aparente, e é um preço que eu pagaria.

O volume caiu porque a chapa do fundo subiu 6 mm. Para compensar, o **chanfro do pé foi reduzido de
52 para 36 mm**: o fundo passou de 148 para 164 mm de profundidade. Sem isso a capacidade cairia
para 4,29 L. O chanfro de topo ficou intacto nos 52 mm — é ele que dá o acesso frontal, e nele não
se mexe.

### 4.2 Encaixado

A saída de **3,5° por lado** faz o corpo ser menor que a boca: a peça afunda na de baixo. O que
limita o afundamento são os **berços do rim**, e eles estão agora na face interna da parede — a
saia da peça de cima passa por dentro deles se a peça entrar **deslocada ou inclinada**, que é
como o encaixe acontece na prática.

**O passo do encaixe não está calculado**, e não vou fingir precisão: depende da cinemática da
entrada. É o número que sustenta a promessa de embalagem do pacote de 10, e sai de uma medição na
amostra ou num protótipo impresso.

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

Se a assimetria da A incomodar, ela encolhe: a faixa pode cair de 18 para 12 mm
(aba de 12 + gancho de 6), e o rebaixo da fêmea cai de 18 para 12 mm junto.

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
```
