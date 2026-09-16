# Cesto Mini Organizador Empilhável e Encaixável — peça única em PP

**Status:** 3D fechado, pronto para cotação de ferramental · **Data:** 16/09/2026
**Referência:** anúncio "10 peças Cesto Mini Organizador Empilhável Caixinha Multiuso"
(Mercado Livre MLBU4092388469) + fotos cotadas enviadas em 16/09/2026
**Modelo:** `cad/modelo3d.py` · **Economia:** `economia.py` · **Arquivos:** `cad/cesto.step`

Produto de **peça única injetada** — sem dobradiça, sem painel, sem montagem. Empilha de pé
com acesso frontal e encaixa inclinado para reduzir volume. Vazado por **furos redondos em
gradiente** (Ø maior em cima, diminuindo para baixo), fundo sólido e frente rebaixada sólida
com ripado, conforme pedido.

> **Substitui o estudo da caixa dobrável** em [`../cesto-dobravel/`](../cesto-dobravel/), que
> partiu de um vídeo de referência com o produto errado. Daquele estudo seguem valendo e foram
> reaproveitados aqui: o parque de injeção e as tonelagens, o levantamento de resinas, o modelo
> de custo por kg da categoria e os bloqueios de dado do ERP.

---

## 1. Veredito

| Requisito | Situação |
|---|---|
| Peça única empilhável e encaixável | **Viável** — é a arquitetura mais simples possível: 1 peça, 1 molde, zero montagem |
| Cotas 21,5 × 20 × 13 cm | **Atendidas** — boca 215 × 200 mm, altura 130 mm |
| Furos redondos em gradiente | **Resolvido** — 6 bandas, Ø 14 → 6 mm, 92 furos, faixa cega de 30 mm no pé |
| Fundo sólido | **Atendido** — chapa de 2,0 mm sem furo |
| Empilhar com acesso frontal | **Resolvido** — rebordo da base assenta no rim; frente rebaixada a 45 mm |
| Encaixar para reduzir volume | **Geometria confirmada** — corpo 11,8 mm menor que a boca; **passo do encaixe a medir na amostra** (seção 4.2) |
| Injeção no parque atual | **1 cavidade numa 200 t (76%)** — a casa tem **12 máquinas** dessa classe |
| Ferramental | **USD 19,5 mil FOB**, 1 molde — por analogia direta com dois moldes da casa |
| Payback | **~5 meses** a 150 mil un/ano |
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
| Base | 196,8 × 181,8 mm |
| Altura | **130 mm** · frente rebaixada a **45 mm** |
| Envelope real | 225,3 × 200 × 135,6 mm (inclui as pegas laterais e os pés) |
| Saída de molde | **4° por lado** — é ela que permite o encaixe |
| Parede / fundo / rim | 1,4 / 2,0 / 3,2 mm |
| Raio de canto em planta | R14 |
| Capacidade | **4,85 L** nominal · **2,73 L** até a borda frontal |
| Peso | **221,1 g** (244,3 cm³ de PP) |
| Área projetada | 430 cm² |

A aresta superior das laterais desce do fundo para a frente numa **curva concava** (expoente 1,7),
não numa reta. É ela que dá o acesso frontal quando empilhado e o rasgo por onde a peça entra
inclinada para encaixar.

### 2.1 Peso — é o ponto a atacar no try-out

221 g para 4,85 L, contra o **Cesto Organizador Vime 7 L (047) da casa, que faz 7 L com 213 g**.
A nossa peça é mais alta em relação ao volume e carrega rebordo de empilhamento e rim reforçado,
mas ainda assim há gordura: **cada 10 g economizados valem R$ 0,15/peça**, ou R$ 22 mil/ano a 150
mil peças. Alvo para o try-out: **200 g**. Caminhos: parede de 1,2 mm na banda superior (onde não
há carga), rim de 2,8 mm, e nervurar o rebordo em vez de engrossá-lo.

---

## 3. O vazado

Furos **redondos** em 6 bandas horizontais de cota Z fixa, com o diâmetro caindo de cima para
baixo. Nas laterais as bandas são recortadas pela curva da aresta, então o campo de furos
acompanha o rebaixo frontal — o gradiente lê nas duas direções.

| Banda | Ø |
|---|---|
| 1 (topo) | **14,0 mm** |
| 2 | 12,4 mm |
| 3 | 10,8 mm |
| 4 | 9,2 mm |
| 5 | 7,6 mm |
| 6 | **6,0 mm** |
| faixa cega | **30 mm** no pé da peça |

Passo do retículado: 15 mm. Total: **92 furos**. Nenhum furo entra no raio de canto (R14), para
não criar parede fina na quina.

**Por que a faixa do pé é cega:** é onde a carga de empilhamento desce até o rebordo e onde a
peça apoia. Furo ali seria concentrador de tensão no caminho da carga.

**Por que o gradiente ajuda:** a parede sofre mais embaixo (a coluna de peso das peças empilhadas
mais o conteúdo) e menos em cima. Diâmetro caindo para baixo põe material onde a tensão está. O
pedido estético e o cálculo apontam para o mesmo lado.

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

A peça é tronco-piramidal, então o corpo é menor que a boca e afundaria. O que segura é o
**rebordo da base**: um flange de 8 mm de altura alargado até a medida da boca (215 × 200), que
assenta no rim da peça de baixo. Nivelada, a peça empilha com **passo de 130 mm** e a frente
rebaixada dá acesso ao conteúdo sem desempilhar.

As **pegas laterais** (as abas que aparecem na foto da referência, no alto da lateral junto à
frente) são para puxar a peça empilhada — não têm função estrutural de empilhamento. Essa é uma
leitura minha da foto: se na amostra física elas forem o apoio do empilhamento, o rebordo da base
sai e o projeto muda (seção 7).

### 4.2 Encaixado

O corpo tem **11,8 mm de folga em X e 10,2 mm em Y** dentro da boca, e a saída de 4° faz a peça
afundar **84 mm** antes de as paredes travarem. O que impede o encaixe na vertical é justamente o
rebordo da base; por isso o encaixe é **inclinado**, entrando pelo vão de 85 mm da frente
rebaixada — que é exatamente como as fotos da referência mostram, com a pilha encaixada deitada.

**O passo do encaixe não está calculado.** Depende do ângulo de inclinação e da cinemática da
entrada, e não vou fingir precisão: o render usa 26 mm como ilustração. **Medir na amostra física
ou num protótipo impresso** — é o número que sustenta a promessa de embalagem do pacote de 10.

Para dimensionar o impacto: a 30 mm de passo, 10 peças encaixadas dão ~400 mm de altura contra
1.300 mm empilhadas. É o que torna o pacote de 10 transportável.

---

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
| Virgem RP 141 (R$ 15/kg custo, R$ 25/kg preço) | R$ 3,32 | R$ 5,53 | 40% | R$ 2,21 | R$ 55,30 |
| Moído + pigmento (R$ 11,50 / R$ 24) | R$ 2,54 | R$ 5,31 | 52% | R$ 2,76 | R$ 53,06 |

Resina no cenário virgem: 0,221 kg × R$ 9,54 = **R$ 2,11** por peça.

**A cor laranja é o que decide entre os dois cenários.** A casa compra PP moído **branco**
(R$ 7,69/kg, 124 t/ano) e **preto** (R$ 6,19/kg, 337 t/ano) — não laranja. Laranja em moído exige
lote dedicado de moído claro mais masterbatch, com risco de variação de tom entre lotes. É uma
pergunta para a produção, e vale **R$ 0,78 por peça** (R$ 117 mil/ano a 150 mil peças).

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

Nossa peça (215 × 200 × 130 mm, 221 g) fica **entre as duas** em envelope e abaixo em peso. Daí
**USD 19,5 mil FOB para 1 cavidade** — estimativa por analogia direta com compras reais da casa,
não por fórmula de USD/kg de bloco.

### 6.5 Payback

Investimento nacionalizado de 1 cavidade: USD 19,5 mil × R$ 5,45 × 1,30 = **R$ 138,2 mil**
(câmbio e nacionalização seguem premissa, não dado do ERP).

| Volume/ano | Cenário | Contribuição/ano | Payback | Horas de máquina |
|---|---|---|---|---|
| 60.000 | virgem | R$ 132,7 mil | 12,5 meses | 368 h |
| **150.000** | **virgem** | **R$ 331,7 mil** | **5,0 meses** | 920 h |
| 150.000 | moído | R$ 414,0 mil | 4,0 meses | 920 h |
| 300.000 | virgem | R$ 663,3 mil | 2,5 meses | 1.840 h |

Referência de volume: o **041 (Organizador Multiuso 3 divisórias) vendeu 262 mil unidades em 12
meses** para 1.847 clientes — é o campeão de volume da casa em organizador pequeno. Se o cesto
novo chegar à metade disso, o payback é de 5 meses.

---

## 7. O que falta — e o mais importante primeiro

| Item | Gravidade | Por quê |
|---|---|---|
| **Amostra física da referência** | **Alta** | Duas leituras minhas saíram de foto e não de peça: (a) as abas laterais são pega e o apoio do empilhamento é o rebordo da base; (b) o passo do encaixe. Se (a) estiver errado, muda o projeto |
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
```
