# Caixa Expositora Tri-Kit

**Status:** projeto de embalagem · **Revisão 3** · 16/09/2026
**Escopo:** uma caixa de papelão ondulado que transporta e expõe **os três kits juntos**

Caixa **sortida**: os três kits viajam e vendem na mesma caixa, cada um na sua coluna vertical,
três facings. O **rasgo frontal é pequeno** — 340 mm de abertura contra 900 de altura — e o muro de
retenção fica com **62% da frente**. O picote em U sobe pelas duas quinas, corre até o fim do topo e
**morre no vinco TRASEIRA/TOPO**: a peça não sai, dobra duas vezes e vira uma **testeira de parede
dupla** que se trava sozinha.

**Internas: 780 × 580 × 900 mm** · externo 790 × 590 × 910 mm · ocupa um meio-palete 800 × 600
inteiro · **64 kits** (16 A + 18 B + 30 C) · onda C simples · chapa 3060 × 1415 mm ·
display montado com 1344 mm.

> **Revisão 3 — o rasgo encolheu.** Na Rev. 2 a abertura tomava 73% da frente e a caixa ficava mole
> no ponto de venda. A referência de mercado mostra por quê isso não é necessário: **o cliente pega
> o produto por cima**, com o topo aberto — o rasgo frontal serve para *ver*, não para pegar. Com
> isso a abertura caiu para 38% e a frente voltou a ser estrutura. A testeira continua saindo da
> mesma peça, com **um vinco a mais no topo**; em troca, o vinco reverso da Rev. 2 deixou de ser
> necessário e a altura da caixa deixou de ser ditada pela mecânica (seção 2).

---

## 1. Veredito

| Requisito | Situação |
|---|---|
| Os 3 kits na mesma caixa | **Resolvido** — uma coluna por kit, três facings, 16 trios completos |
| **Caixa não pode ficar mole** | **Resolvido** — muro de retenção com **62% da frente**, contra 27% na Rev. 2 |
| Picote que vai até o fim do topo e não sai | **Resolvido** — picote em **U**, peça articulada no vinco TRASEIRA/TOPO |
| Testeira por dobra | **Resolvido** — 290 mm, **parede dupla**, travada por uma aba de 340 mm |
| Cubagem que faça sentido | **81% de ocupação interna**, meio-palete 800 × 600 **100% usado** |
| Construção | Deixa de ser caixa americana: vira **wrap** (seção 4) |
| Chapa de 3060 mm | **Risco de formato** — confirmar com o fornecedor; alternativa em 2 peças (seção 4.3) |
| Peso bruto ~42 kg | **Bloqueio de dado** — depende do peso do kit, ainda não confirmado |

---

## 2. O rasgo pequeno e o vinco que trava a montagem

### 2.1 Por que o rasgo pode ser pequeno

Porque **o cliente não pega o produto pela frente.** Quando a testeira sobe, o topo da caixa fica
aberto — é por ali que ele tira o kit. O rasgo frontal existe para **mostrar** o que tem dentro e
para dar o facing da marca.

Entendido isso, a abertura não precisa ser grande, e a frente volta a ser estrutura:

| | Rev. 2 | **Rev. 3** |
|---|---|---|
| Muro de retenção | 240 mm (27% da frente) | **560 mm (62%)** |
| Abertura frontal | 660 mm | **340 mm nas quinas, 420 no centro** |
| Testeira | 580 mm | **290 mm** |
| Display montado | 1634 mm | **1344 mm** |

O corte não é reto: **arco de flecha 80 mm**, descendo a 480 no centro (R 873). É o que dá o desenho
da referência e o que facilita ver o produto sem baixar o muro nas quinas, onde ele trabalha.

**O que o muro de 560 retém:** 5 camadas inteiras do kit quadrado, 4 do retangular alto, 7 do
retangular baixo. **O que aparece pelo rasgo** (a carga vai até 840): 2,7 camadas do quadrado na
quina e 3,4 no centro; 2,0 e 2,6 do alto; 3,5 e 4,5 do baixo. Facing cheio nos três.

### 2.2 O vinco que faz a testeira fechar exata

A peça que dobra é uma tira de 920 mm: **290 (dorso) + 290 (face) + 340 (aba)**. Ela dobra duas
vezes, e a posição do vinco novo não é livre:

```
c = profundidade / 2 = 290 mm
```

Esse é o **único** valor em que duas coisas acontecem ao mesmo tempo:

1. a **face cobre o dorso exatamente** — testeira de parede dupla em toda a altura, sem sobra nem falta;
2. o **vinco FRENTE/TOPO para exatamente na borda da caixa**, e a partir dali a faixa frontal desce
   reta por dentro, contra a traseira.

| c | Face cobre o dorso | Vinco frente/topo para em |
|---|---|---|
| 240 mm | 240 de 240 | z = 800 (80 abaixo da borda) |
| 270 mm | 270 de 270 | z = 860 |
| **290 mm** | **290 de 290** | **z = 900 — a borda** |
| 300 mm | 280 de 300 — falta 20 | z = 920 (20 acima) |
| 330 mm | 250 de 330 — falta 80 | z = 980 |

Na prática isso vira um **registro visual de montagem**: se o vinco assentou na borda, está certo.
Se sobrou ou faltou, o montador vê na hora.

### 2.3 O que mudou em relação à Rev. 2

- **A altura da caixa deixou de ser travada pela mecânica.** Na Rev. 2 valia
  `H = muro + profundidade + aba`. Agora quem está travado é o vinco de montagem, em `D/2`.
  A altura voltou a ser livre — os 900 mm são escolha da carga (840 de pilha + 60 de borda).
- **O vinco reverso sumiu.** Na Rev. 2 o vinco FRENTE/TOPO dobrava 180° ao contrário. Agora ele
  termina plano na borda: é um vinco comum. O vinco novo do topo também dobra no sentido normal.
  **Nenhum vinco reverso na faca** — um risco de produção a menos.
- **A aba de travamento cresceu** de 80 para 340 mm. Ela desce por dentro, entre a traseira e o
  produto, e passa folgada: as colunas deixam 40 a 70 mm livres atrás, contra 5 mm de papelão.

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

Duas divisórias verticais de onda simples, 580 × 840 mm, encaixadas entre as colunas. Elas fazem
três coisas:

1. **Separam o sortimento** — sem elas os três kits se misturam na primeira reposição.
2. **Travam a frente na traseira.** Correm a profundidade inteira, então amarram o muro frontal ao
   painel traseiro em dois pontos. É o que impede o muro de 560 de barrigar para fora.
3. Entram no caminho de carga e ajudam na compressão.

Com o rasgo pequeno, o item 2 deixou de ser bônus e virou parte da estrutura.

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
| Travessa | na FRENTE, a **560 mm** do fundo, em **arco de flecha 80** (480 no centro, R 873) |
| Duas longarinas | **15 mm para dentro** dos vincos das abas laterais, da travessa até o vinco TRASEIRA/TOPO |
| Fim | morre no vinco TRASEIRA/TOPO — **a peça fica pendurada ali** |
| Dedeira | Ø 35 mm em **corte real**, no ponto mais baixo do arco, no painel que fica |

As longarinas correm 15 mm para dentro porque **picote em cima de vinco rasga torto**. Os dois
filetes de 15 mm que sobram ficam presos nas abas laterais e viram parte da parede — a lateral
não perde nada.

O picote corre por cima do vinco de montagem sem interrupção: ele atravessa o topo inteiro, dos
dois lados, e só para no vinco da traseira.

### 4.2 Os vincos do topo

| Vinco | Posição | Função | Como dobra |
|---|---|---|---|
| TRASEIRA / TOPO | fim do topo | **dobradiça** da testeira | abre de 90° para 180° — vinco normal, **reforçado** (gira com a caixa cheia) |
| **Vinco de montagem** | **290 mm da traseira** | onde a face dobra sobre o dorso | **plano na caixa fechada**, dobra 180° só na loja |
| FRENTE / TOPO | entre os painéis | vira o batente da aba na borda | dobra 90° na montagem da caixa, e **fica plano** no expositor |

O vinco de montagem é o detalhe que mais escapa: na caixa fechada ele não faz nada, e por isso é
fácil o fornecedor esquecê-lo. **Sem ele a testeira não existe.**

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

1. Enfiar o dedo na dedeira Ø 35, no ponto baixo do arco, e puxar o picote em U. A peça solta mas
   **não sai**.
2. Levantar a peça: os primeiros **290 mm do topo sobem 90°** no vinco da traseira e ficam em pé.
   É o **dorso** da testeira.
3. Dobrar o resto **180° no vinco de montagem**: os 290 seguintes descem sobre o dorso — é a
   **face**, e a testeira fica de parede dupla.
4. A faixa frontal de **340 mm** continua descendo por dentro da caixa, entre a traseira e o
   produto. **É o travamento.** Sem fita, sem cola, sem peça avulsa.
5. Conferir: o vinco FRENTE/TOPO tem que assentar na borda da caixa. Assentou, está montado.

O topo fica **aberto** — é por ali que o cliente pega o kit. O rasgo frontal mostra o produto e
carrega a marca.

**A arte da testeira fica impressa no TOPO**, na metade voltada para a frente, e **na mesma
orientação da frente** — não gira nem espelha. A face externa da chapa é a mesma nos dois painéis,
e o alto da testeira cai para o lado da traseira, que é o mesmo sentido do alto da frente.

Altura final do display: 910 (caixa) + 290 (testeira) + 144 (palete) = **1344 mm**.

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
- [ ] **VINCO DE MONTAGEM no topo, a 290 mm da traseira** — plano na caixa fechada, é o que cria a
      testeira. Não confundir com vinco de dobra do corpo e **não omitir**
- [ ] **Nenhum vinco reverso** na faca (mudou em relação à revisão anterior)
- [ ] Vinco TRASEIRA/TOPO reforçado: é a dobradiça, gira com a caixa cheia
- [ ] Picote **em zíper** em U; as longarinas **15 mm para dentro** dos vincos, nunca sobre o vinco
- [ ] Travessa do picote **em arco**: 560 nas quinas, flecha 80, R 873
- [ ] O picote **termina** no vinco TRASEIRA/TOPO — não contornar, a peça não sai
- [ ] Dedeira Ø 35 mm em **corte real**, no ponto baixo do arco
- [ ] 2 divisórias de 580 × 840 mm (**estruturais** — travam o muro na traseira) e 1 calço de 40 mm
- [ ] Arte da testeira **no painel do TOPO**, metade dianteira, mesma orientação da frente
- [ ] Amostra física antes da faca definitiva, com o teste de dobra feito **cheio**, não vazio

---

## 9. O que falta confirmar

| Dado | Por que importa |
|---|---|
| **Peso de cada kit** | Os 42 kg de peso bruto são estimativa (0,12 kg/L). Acima de 55 kg a onda sobe para BC |
| **Formato máximo de chapa do fornecedor** | Define uma peça × duas peças (seção 4.3) |
| **O mix 16 / 18 / 30 serve ao comercial?** | Sai da geometria. Mudar exige trocar coluna, não ajustar quantidade (seção 3.2) |
| **Meio-palete é EUR 800 × 600 ou meio-PBR 1000 × 600?** | Em meio-PBR a frente vai a 984 mm e cabem 5 colunas — outro projeto, mais kits |
| **Altura de gôndola / porta da loja** | 1344 mm de display montado — a testeira é metade da profundidade, então um limite de altura volta para a profundidade |

---

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `calculo-expositora.py` | Memória de cálculo: colunas, camadas, calço, chapa, McKee, palete |
| `gera-desenhos.py` | Gerador dos SVGs |
| `faca-expositora.svg` | Planificação do wrap com vincos, o vinco de montagem e o picote em U |
| `arranjo.svg` | Vista superior das 3 colunas + vista frontal das pilhas |
| `conversao.svg` | Caixa fechada, montada, e o corte lateral do dobramento |
