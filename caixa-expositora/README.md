# Caixa Expositora Tri-Kit

**Status:** projeto de embalagem · **Revisão 2** · 16/09/2026
**Escopo:** uma caixa de papelão ondulado que transporta e expõe **os três kits juntos**

Caixa **sortida**: os três kits viajam e vendem na mesma caixa, cada um na sua coluna vertical,
três facings. O picote sobe pela frente a partir de 240 mm, corre pelas duas quinas até o fim do
topo e **morre ali** — a peça não sai. Ela fica articulada no vinco TOPO/TRASEIRA, gira para cima
e dobra sobre si mesma virando uma **testeira de parede dupla**.

**Internas: 780 × 580 × 900 mm** · externo 790 × 590 × 910 mm · ocupa um meio-palete 800 × 600
inteiro · **64 kits** (16 A + 18 B + 30 C) · onda C simples · chapa 3060 × 1415 mm.

> **Revisão 2 — o que mudou em relação à Rev. 1:** a caixa passou de mono-kit para **sortida**;
> a testeira deixou de ser aba destacável e virou **peça articulada que dobra** (frente + topo);
> a construção deixou de ser caixa americana e virou **wrap**, porque o topo precisa ser um painel
> inteiriço preso na traseira; o footprint passou a ser ditado pelo **meio-palete**; e a onda caiu
> de BC para **C simples**, porque a frente não é mais destruída (seção 5).

---

## 1. Veredito

| Requisito | Situação |
|---|---|
| Os 3 kits na mesma caixa | **Resolvido** — uma coluna por kit, três facings, 16 trios completos |
| Picote que vai até o fim do topo e não sai | **Resolvido** — picote em **U**, peça articulada no vinco TOPO/TRASEIRA |
| Testeira por dobra | **Resolvido** — 580 mm, **parede dupla**, travada por uma aba de 80 mm |
| Cubagem que faça sentido | **81% de ocupação interna**, meio-palete 800 × 600 **100% usado** |
| Construção | Deixa de ser caixa americana: vira **wrap** (seção 4) |
| Chapa de 3060 mm | **Risco de formato** — confirmar com o fornecedor; alternativa em 2 peças (seção 4.3) |
| Peso bruto ~42 kg | **Bloqueio de dado** — depende do peso do kit, ainda não confirmado |

---

## 2. A altura não é escolha, é consequência

Esse é o número que amarra o projeto inteiro. A peça que dobra tem duas partes: a **face**
(o pedaço alto da frente) e o **dorso** (o topo). Quando o dorso sobe e fica em pé, a face desce
por cima dele. Para a face cobrir o dorso e ainda travar, ela precisa ser **maior que a
profundidade**:

```
altura interna  =  muro de retenção  +  profundidade  +  aba de travamento
      900       =        240         +       580      +        80
```

Em outras palavras: **quem escolhe a altura é a profundidade.** Mudou a profundidade, mudou a
altura, ou a testeira deixa de travar. Ninguém pode mexer nesses três números isoladamente.

E o resultado bate com o que a carga pede:

| | |
|---|---|
| Altura interna | 900 mm |
| Folga de topo | 30 mm |
| **Altura útil de carga** | **870 mm** |
| Altura real da pilha | **840 mm** nos três kits (seção 3) |

---

## 3. O sortimento

Uma coluna vertical por kit. Cada coluna tem seu próprio número de camadas, e um **calço nivela
os três topos em 840 mm** — o expositor fica plano, sem degrau.

| Coluna | Kit | Facing | Fundos | Por camada | Camadas | Pilha | Calço | **Kits** |
|---|---|---|---|---|---|---|---|---|
| A | quadrado 23,5 × 25,5 × 10,5 | 235 mm | 2 × 255 | 2 | 8 | 840 mm | — | **16** |
| B | ret. alto 18 × 26 × 14 | 260 mm | 3 × 180 | 3 | 6 | 840 mm | — | **18** |
| C | ret. baixo 18 × 26 × 8 | 260 mm | 3 × 180 | 3 | 10 | 800 mm | **40 mm** | **30** |

**Total: 64 kits · 16 trios completos · 331 L de produto em 407 L internos = 81% de ocupação.**

As três colunas + 2 divisórias de 3 mm somam 761 mm dos 780 internos — sobram 19 mm de folga
operacional, distribuídos.

### 3.1 Por que 840 mm fecha nos três

É coincidência aritmética, e é ela que faz o expositor ficar bonito:

```
kit A:  8 camadas × 105 = 840
kit B:  6 camadas × 140 = 840
kit C: 10 camadas ×  80 = 800  + calço de 40 = 840
```

105 e 140 têm MMC 420; 840 é o primeiro múltiplo que também fica perto de um múltiplo de 80.
Qualquer outra altura útil quebra pelo menos uma das três colunas.

### 3.2 O mix

A proporção **16 : 18 : 30** sai da geometria, não de giro. Se o comercial quiser outro mix, a
alavanca é a largura do facing — trocar a coluna C por uma segunda coluna B move 12 unidades de C
para B. O que **não** dá para mexer sem refazer a conta é o número de colunas: três facings de
235 + 260 + 260 já consomem 780 mm, que é a frente inteira.

### 3.3 Divisórias

Duas divisórias verticais de onda simples, 580 × 840 mm, encaixadas entre as colunas. Não são
decorativas: sem elas os três kits se misturam na primeira reposição e o display vira bagunça.
De quebra entram no caminho de carga e ajudam na compressão.

---

## 4. Construção: por que wrap e não caixa americana

O topo tem que ser **um painel inteiriço preso na traseira**. Em caixa americana o topo são quatro
abas, e quatro abas não dobram para virar testeira. Então a chapa dá a volta:

```
FUNDO (585) | FRENTE (905) | TOPO (585) | TRASEIRA (905) | aba de cola (80)
```

| | |
|---|---|
| Painel (largura) | 785 mm |
| Abas laterais (fundo, frente e traseira) | 315 mm cada, **sobrepõem 50 mm** no meio da lateral |
| Abas de cola do topo | 60 mm cada lado — **é o que o picote libera** |
| **Chapa** | **3060 × 1415 mm = 4,33 m²** |
| Peso da caixa vazia | 2,2 kg em onda C · 3,0 kg em BC |

A parede lateral é formada pelas abas da FRENTE e da TRASEIRA, que se encontram com 50 mm de
sobreposição colada. As abas do FUNDO sobem por dentro e reforçam os primeiros 315 mm da lateral —
justamente onde a carga senta.

### 4.1 O picote em U

Uma linha só, em forma de U, e ela **não fecha**:

| Trecho | Onde |
|---|---|
| Travessa | na FRENTE, a **240 mm** do fundo, atravessando o painel |
| Duas longarinas | **15 mm para dentro** dos vincos das abas laterais, da travessa até o vinco TOPO/TRASEIRA |
| Fim | morre no vinco TOPO/TRASEIRA — **a peça fica pendurada ali** |
| Dedeira | Ø 35 mm em **corte real**, no centro da travessa, no painel que fica |

As longarinas correm 15 mm para dentro porque **picote em cima de vinco rasga torto**. Os dois
filetes de 15 mm que sobram ficam presos nas abas laterais e viram parte da parede — a lateral
não perde nada.

### 4.2 Os dois vincos que não são iguais aos outros

| Vinco | Função | Especificação |
|---|---|---|
| TOPO / TRASEIRA | é a **dobradiça** da testeira. Abre de 90° para 180° | vinco normal, mas **reforçado** (a peça vai girar com a caixa cheia) |
| FRENTE / TOPO | a face dobra 180° **para o lado contrário** do que dobrou na montagem | **VINCO REVERSO** — obrigatório |

Sem o vinco reverso, a face racha na dobra. E racha na loja, na frente do cliente.

### 4.3 O problema da chapa de 3060 mm

3,06 m de comprimento de chapa não passa em impressora plana comum. Duas saídas:

1. **Uma peça**, em corte rotativo ou casemaker de grande formato — confirmar o formato máximo.
2. **Duas peças**: a "capa" (FRENTE + TOPO + TRASEIRA, 2401 × 1415) e uma **bandeja de fundo**
   colada. Mesma área total de papelão, duas facas menores, uma operação de colagem a mais.

Perguntar isso ao fornecedor **antes** de fechar a faca.

---

## 5. Papelão: por que C simples agora basta

Na Rev. 1 a frente era destacada e saía fora, e a caixa perdia ~45% da compressão — daí a onda BC.
**Agora a frente não sai.** Em transporte a caixa está inteira, os quatro painéis trabalham, e o
derate sumiu. Além disso a caixa viaja em meio-palete, que não empilha três alturas.

BCT por McKee (`5,87 × ECT × √(t × perímetro)`, perímetro 272 cm):

| Papel | ECT | Espessura | BCT | Margem sobre o exigido |
|---|---|---|---|---|
| Onda C simples K180/K180 | 5,2 | 5 mm | 356 kgf | 1,7× |
| **Onda C simples K200/K200** | **6,8** | **5 mm** | **465 kgf** | **2,2×** |
| Onda BC dupla 175/150/175 | 10,5 | 7 mm | 850 kgf | 4,1× |

Carga: uma caixa sobre a outra = **42 kg** (estimado), fator 5 para seis meses de estoque a 80% de
umidade → **210 kgf exigidos**.

**Recomendação: onda C simples K200/K200, canaletas verticais no corpo.** Economiza ~30% do papelão
contra BC, e a testeira já é parede dupla por construção — não precisa de onda dupla para ficar em
pé. Subir para BC só se o peso do kit vier bem acima da estimativa, ou se decidirem empilhar três
caixas no armazém.

---

## 6. Conversão em expositor

1. Abrir a caixa e enfiar o dedo na dedeira Ø 35.
2. Puxar o picote em U — os dois lados e a travessa. A peça solta mas **não sai**.
3. **O topo gira 90° e fica em pé**, alinhado com a traseira: é o **dorso** da testeira (580 mm).
4. **A face dobra 180° sobre o dorso**: testeira de parede dupla, arte para o cliente.
5. Os 80 mm que sobram da face descem por dentro da caixa, contra a traseira: **é o travamento**.
   Sem ferramenta, sem fita, sem peça avulsa.

A arte **não fica de cabeça para baixo**: a borda que estava no alto da frente continua no alto da
testeira. A face externa da frente — a que o cliente via na caixa fechada — é a mesma que ele vê na
testeira. Uma arte só serve para as duas situações.

Altura final do display: 910 (caixa) + 580 (testeira) + 144 (palete) = **1634 mm**.

---

## 7. Palete

| | |
|---|---|
| Meio-palete EUR 800 × 600 | caixa 790 × 590 → **10 mm de folga em cada eixo, 1 caixa, 100% do meio-palete** |
| Dois meios-paletes | 800 × 1200 mm — cabem num PBR 1000 × 1200 (80% do piso) |
| Altura carregada | 910 + 144 = 1054 mm por meio-palete |

A caixa **é** o display: sai do caminhão, vai para o chão da loja, rasga e monta. Não há
transbordo, não há montagem de expositor avulso.

---

## 8. Checklist para o fornecedor

- [ ] **Onda C simples K200/K200**, ECT ≥ 6,5 kgf/cm, **canaletas verticais** no corpo
- [ ] Construção **wrap**: FUNDO | FRENTE | TOPO | TRASEIRA | aba de cola
- [ ] Chapa **3060 × 1415 mm** — **confirmar formato máximo**; se não passar, versão em 2 peças
- [ ] Abas laterais da frente e da traseira **sobrepondo 50 mm**, coladas
- [ ] Abas do fundo subindo por dentro da lateral (reforço de 315 mm)
- [ ] **VINCO REVERSO** no vinco FRENTE/TOPO — sem isso a testeira racha
- [ ] Vinco TOPO/TRASEIRA reforçado: é a dobradiça, gira com a caixa cheia
- [ ] Picote **em zíper** em U; as longarinas **15 mm para dentro** dos vincos, nunca sobre o vinco
- [ ] O picote **termina** no vinco TOPO/TRASEIRA — não contornar, a peça não sai
- [ ] Dedeira Ø 35 mm em **corte real**
- [ ] 2 divisórias de 580 × 840 mm e 1 calço de 40 mm (onda simples, sem faca dedicada)
- [ ] Arte: a face da frente acima de 240 mm **é** a testeira — tratar como peça de comunicação
- [ ] Amostra física antes da faca definitiva, com o teste de dobra feito **cheio**, não vazio

---

## 9. O que falta confirmar

| Dado | Por que importa |
|---|---|
| **Peso de cada kit** | Os 42 kg de peso bruto são estimativa (0,12 kg/L). Acima de 55 kg a onda sobe para BC |
| **Formato máximo de chapa do fornecedor** | Define uma peça × duas peças (seção 4.3) |
| **O mix 16 / 18 / 30 serve ao comercial?** | Sai da geometria. Mudar exige trocar coluna, não ajustar quantidade (seção 3.2) |
| **Meio-palete é EUR 800 × 600 ou meio-PBR 1000 × 600?** | Em meio-PBR a frente vai a 984 mm e cabem 5 colunas — outro projeto, mais kits |
| **Altura de gôndola / porta da loja** | 1634 mm de display montado; se houver limite, ele volta para a profundidade (seção 2) |

---

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `calculo-expositora.py` | Memória de cálculo: colunas, camadas, calço, chapa, McKee, palete |
| `gera-desenhos.py` | Gerador dos SVGs |
| `faca-expositora.svg` | Planificação do wrap com vincos, vinco reverso e o picote em U |
| `arranjo.svg` | Vista superior das 3 colunas + vista frontal das pilhas |
| `conversao.svg` | As 4 etapas até o expositor montado |
