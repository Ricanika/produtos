# Linha Potes Retangulares Modulares em PP

**Status:** estudo de viabilidade técnica · **Revisão 7** · 22/09/2026
**Origem:** evolução do Projeto 115 do ERP ("Conjunto Potes Modular") · **Planta:** Nitron – Fábrica (CODPLP 1)

Linha retangular em PP transparente, **parede reta com cantos arredondados**, quatro litragens
(**600 ml · 1,2 L · 1,8 L · 2,4 L**), três tampas e modularidade de empilhamento — qualquer
combinação empilhada chega à altura do maior.

Todos os números de máquina, matéria-prima, custo e ferramental saíram do Sankhya, não de
estimativa de catálogo. Fontes citadas em cada seção.

> **Revisão 7 — mudança de arquitetura.** A partir de uma referência física (pote hermético de
> travas), o corpo foi refeito. **Três coisas saíram do projeto:** a aba em U da borda, o pé
> embutido, e a garra da tampa PE — que engatava justamente na aba. Entram:
>
> - **Colar de borda.** A borda superior fica lisa, com a aresta de cima arredondada em 0,5 mm.
>   Na lateral ela sobressai **3,50 mm por lado** sobre o corpo. A face de baixo desse colar é a
>   **aresta de engate** da trava: 3,46 mm de encosto. Não é canaleta — é degrau.
> - **Rodapé reto.** O pé embutido saiu. O corpo é seção constante de 141,6 × 77,9 mm do colar até
>   o fundo, com 0,5°/lado, **sem degrau nenhum** — que é o que o IML pede para assentar o rótulo.
> - **Travas na tampa.** 6 abas de 18 × 1,00 mm com farpa, engatando sob o colar. Cada uma fecha
>   com ~2 kgf; as seis seguram 12 kgf.
> - **Um filete de TPE para as duas tampas.** A de teca é uma **placa maciça de 8 mm** com friso na
>   face lateral; a de PP/PE tem o mesmo friso no plug. Objetivo perseguido desde a revisão 4,
>   fechado aqui.
>
> **O que quase não sobreviveu:** sem pé embutido, quem desce na bandeja da tampa passa a ser o
> **fundo reto do pote de cima** — e ele tem de caber dentro da boca. É essa conta que dimensiona o
> colar (seção 3.2), e ela só fecha com 3,50 mm de rebaixo, com **0,30 mm de folga**. Se o rebaixo
> fosse 2,6 mm a linha não empilharia.
>
> **O que a revisão custou:** o colar cresceu de 145,7 para **154,8 mm** na medida máxima (o deck da
> tampa), e apareceu um número que nenhuma revisão anterior tinha olhado — **a tampa plug come
> volume útil**: a de teca leva 115 ml do 600 ml, 19% (seção 5.6).
>
> **Duas correções pegas por verificação, não por leitura:** o filete estava desenhado **0,40 mm
> aquém da boca** (não vedaria nada) e metade das abas entrava **espelhada** no visualizador
> (volume negativo, cancelando as outras três). Nenhuma checagem de malha acusa isso; foi o
> confronto entre cálculo, malha e montagem (seção 12).
>
> **Revisão 6 — o que mudou:** a linha passa de três tampas para **duas** — teca com chanfro e
> aro de TPE, e **PE 100%**. A tampa PE deixa de ser um plug e passa a **fechar por fora**: uma saia
> desce por fora da borda e uma garra engata sob o lábio da aba em U. Como a aba já existia desde a
> revisão 3 para enrijecer a boca, **o pote não mudou uma cota sequer** — o lábio já dava 3,04 mm/lado
> de ressalto e a garra só precisa de 0,80.
>
> Isso me obriga a corrigir o julgamento das revisões 2 a 5: eu recomendava PP contra PE, mas
> aquilo era **contra um PE em forma de plug**, e nessa forma continuava certo. Como sobretampa sem
> aro, três dos quatro argumentos caem (seção 6.0). Fica de pé o mais sério: PE é compra residual.
>
> Resina recomendada: **PEAD HA 7260 IF 20 a R$ 9,34/kg** — grau de injeção declarado e mais barato
> que o próprio PP RP 141. Tampa de 27,6 g a R$ 0,26.
>
> Dois pontos ficaram abertos e estão registrados: a rigidez do deck contra rotação da saia, que
> pede elemento finito ou protótipo (6.1.5), e a **tampa de teca, que não pode ser o plug de parede
> fina desenhado para injeção** e precisa do poço da bandeja usinado, senão não empilha (6.2).
>
> **Revisão 5 — o que mudou:** o desenho voltou para a proporção da referência conceitual. O pote
> estava **largo e muito arredondado** (121,2 × 93,2 com canto R18); agora é **frente estreita e
> pote fundo** (139,7 × 79,8) com **canto R10**. Altura, módulo, passo, curso de abertura e altura
> de molde não mudam — foi escolhido de propósito o caminho que não mexe na injetora.
>
> Três coisas vieram junto, duas delas correções de erro meu:
>
> 1. **A área projetada era 125 cm², não 139.** O número da revisão 4 não saía do cálculo. Com
>    125 cm² o 600 ml usa 72% de uma injetora de 160 t e **volta para a classe de 160 t** em vez de
>    disputar as 200 t com o 1,2 L (seção 4.1).
> 2. **O pé embutido estava fixo no código em 112,4 mm** e foi o único número que quebrou com a
>    troca de footprint — virou um degrau de 13 mm. Ele nunca foi uma escolha: sai da bandeja da
>    tampa, que sai da boca. Agora é derivado (`pe_l()` em `calculo-modular.py`).
> 3. **Custa 17,6 g de resina e rigidez na face comprida** — a única conta em que a revisão 5 é
>    pior que a 4. Está medida na seção 3.3, e é a decisão que sobrou em aberto.
>
> **Revisão 4:** a vedação passa a ser **radial**, do jeito certo: a tampa tem um
> *plug* que desce dentro do pote e leva o aro de TPE numa canaleta, trabalhando contra a **parede**.
> Sem trava e sem saia externa — a tampa fica lisa. Some a força permanente de fechamento; o que
> resta é 1,0 kgf para abrir descascando um canto. Pé de 113,0 para 112,4 mm.
>
> **Revisão 3:** refez a vedação da revisão 2 (que não fechava) com um lábio de PP moldado na tampa,
> e acrescentou a **aba em U** na borda, que dá rigidez ao lado reto. O lábio foi substituído pelo
> plug na revisão 4; a aba ficou.
>
> **Revisão 2:** escala migrou de 500/1000/1500/2000 para 600/1200/1800/2400 ml (pacote de
> mantimento); parede deixou de ser conada e passou a reta com R18 de canto.

---

## 1. Veredito

| Requisito | Situação |
|---|---|
| Modularidade de empilhamento | **Viável** — passo único de 60 mm |
| Litragens 600 / 1200 / 1800 / 2400 ml | **Viável e exatas** — a parede reta elimina o conflito com o passo |
| Parede reta com cantos arredondados | **Viável** com 0,5°/lado e R10 — custa aninhamento no frete (seção 3.4) |
| Rodapé reto para IML | **Viável** — seção constante do colar ao fundo, sem degrau |
| Trava na borda, nas duas tampas | **Só na de PP/PE.** Teca é placa maciça com friso: segura por atrito |
| Capacidade útil com a tampa fechada | **Decisão aberta**: 485 ml no pote de 600 de borda (seção 5.6) |
| Tampa única para os 4 tamanhos | **Viável** — já é prática da casa (ref. 321-T serve três alturas) |
| Vedação das duas tampas | **Um filete de TPE** em friso, radial contra a boca, 0,20 mm de compressão (seção 5) |
| Tampa de teca empilhar | **Resolvido na revisão 7**: o topo da placa É o plano modular, sem poço a usinar |
| Tampa com trava | **Viável** — 6 abas em PP RP 141, 21,7 g, R$ 0,21 + filete |
| Injeção dos 4 corpos no parque atual | **Cabe no que já temos**, sem máquina nova |
| Confirmação documental de curso/extração | **Bloqueio de dado**: ficha das injetoras vazia (seção 4.4) |
| Rigidez da face comprida | **Melhorou**: o painel caiu de 119,7 para 128,6 mm mas o colar substitui a aba como aro de boca (seção 3.3) |

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

**Colar da borda 148,6 × 84,9 mm** (medida máxima do corpo) · **corpo 141,6 × 77,9 mm**, reto do
colar até o fundo · canto **R10** · saída **0,5°/lado** · módulo **60 mm**
Colar com **5,0 mm de altura**, sobressaindo **3,50 mm/lado** · aresta de cima arredondada em
**0,5 mm** · boca **145,0 mm** (parede da borda 1,80) · fundo **2,0 mm igual nos quatro**
**Sem pé embutido: rodapé reto, para IML.**

| Tamanho | Altura total | Passo | Corpo no topo | Fundo externo | Elev. fundo | Parede | Volume | Peso |
|---|---|---|---|---|---|---|---|---|
| 600 ml | 62,0 mm | 60 mm | 141,6 × 77,9 | 140,56 | 2,96 mm | 1,15 mm | 600 ml | 47,0 g |
| 1,2 L | 122,0 mm | 120 mm | 141,6 × 77,9 | 139,51 | 3,90 mm | 1,20 mm | 1200 ml | 74,6 g |
| 1,8 L | 182,0 mm | 180 mm | 141,6 × 77,9 | 138,46 | 2,92 mm | 1,30 mm | 1800 ml | 107,4 g |
| 2,4 L | 242,0 mm | 240 mm | 141,6 × 77,9 | 137,42 | 0,00 mm | 1,40 mm | 2400 ml | 144,1 g |

**O molde ficou mais simples do que era.** Descendo do colar, a peça **só estreita**:
148,6 → 141,6 → 137,4. Nenhuma contra-saída, nenhuma gaveta, nenhuma extração por arraste. O
rebaixo onde a trava engata não é uma canaleta — é a face de baixo do colar.

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
2. **A tampa é uma bandeja cujo piso fica 2,0 mm abaixo da borda do pote** — recuado para dentro da
   boca, não apoiado em cima dela. Esse piso é o plano modular: é nele que o pote de cima se apoia.
3. **O fundo reto do pote de cima desce dentro da bandeja.** Na revisão 6 quem descia era um pé
   embutido; com o rodapé reto exigido pelo IML, o pé saiu e **o próprio fundo faz o serviço**.

**E é a regra 3 que dimensiona o colar.** O fundo reto tem de caber dentro da boca, e o orçamento
de largura, por lado, é:

```
parede da borda 1,80 + folga de encaixe 0,50 + parede do plug 0,80 + folga do plug 0,60 = 3,70 mm
pago por:  rebaixo do colar 3,50 + o que a saída estreita no 600 ml 0,497   = 4,00 mm
folga:                                                                       +0,30 mm
```

Com rebaixo de 2,6 mm a conta dá parede de bandeja de 0,04 mm — **a linha não empilharia**. Os
3,50 mm não são estética: são o preço de ter rodapé reto e continuar modular. O fundo do 600 ml
(140,56) entra na boca de 145,0 com 2,20 mm por lado.

Com as três juntas: passo = 60n exato, capacidade = 600n exata, e **uma tampa só serve os quatro**.
Sem a terceira, o pote de cima não caberia dentro da bandeja — a boca do pote tem 118,9 mm e o corpo
tem 141,6 mm. O colar é o que resolve, e de quebra os potes ficam **travados entre si** quando
empilhados, em vez de só apoiados.

**Orçamento de largura — é o que dimensiona o pé.** Entre a face externa do corpo e a face externa
do pé sobram 4,1 mm por lado, e tudo tem que caber ali:

| | por lado |
|---|---|
| parede na faixa da borda | 1,40 mm |
| folga entre o plug e a parede (onde o aro trabalha) | 1,00 mm |
| parede do plug | 1,50 mm |
| folga de encaixe do pé | 0,50 mm |
| **soma** | **4,40 mm** |

É esse orçamento que fixa o rebaixo do colar em 3,50 mm. Na revisão 2 havia um aro de TPE dentro dessa conta,
com 2,00 mm reservados para uma canaleta que precisa de 4,00 — era o número errado, e o pé de
110,0 mm saiu dele. Tirando o aro da tampa de PP, a conta fecha e o pé cresce.

**Caminho de carga:** pé do pote de cima → piso da bandeja → parede do plug → borda do pote →
parede do pote. O aro de TPE fica na canaleta do plug, mais abaixo, vedando radialmente contra a
parede — fora do caminho de carga, para não ser comprimido pelo peso da pilha.

### 3.3 O preço do canto R10: a face comprida

Reduzir o raio e afinar a frente ao mesmo tempo tem efeitos opostos, e não se cancelam igual nas
duas faces. O painel plano é o trecho de parede entre os dois cantos:

| | R18 de 121,2 × 93,2 | R10 de 139,7 × 79,8 |
|---|---|---|
| Painel plano da face **curta** | 57,2 mm | **59,8 mm** |
| Painel plano da face **comprida** | 85,2 mm | **119,7 mm** |

A face curta praticamente não mudou — afinar a frente devolveu o que o raio menor tirou. A face
comprida é que paga: 119,7 mm de parede plana sem nada que a segure no meio.

Flecha relativa (placa engastada nas quatro bordas, mesma carga, `flecha ~ α·b⁴/t³`, `b` = menor
vão do painel; 1,00 = a mesma face no desenho R18):

| Tamanho | Face comprida | Face curta | Parede que igualaria a face comprida |
|---|---|---|---|
| 600 ml | 1,21× | 1,10× | 1,23 mm (hoje 1,15) |
| 1,2 L | 2,38× | 1,19× | 1,60 mm (hoje 1,20) |
| 1,8 L | 3,35× | 1,20× | 1,94 mm (hoje 1,30) |
| **2,4 L** | **3,81×** | 1,20× | 2,19 mm (hoje 1,40) |

No 600 ml não é problema: a face comprida tem 119,7 × 60 mm, e quem manda na flecha é o vão menor,
que é a altura — a mesma de antes. O problema aparece à medida que o pote sobe, porque aí o vão
menor passa a ser a largura de 119,7 mm. No 2,4 L a face comprida fica **3,8× mais flexível**.

**Igualar com parede está fora de questão:** 2,19 mm no 2,4 L é +56% de resina. As saídas reais são
três, e nenhuma é minha para escolher:

1. **Aceitar.** Pote de mantimento é pego pelas faces curtas, que não mudaram. A vedação é radial e
   mora no bocal, que é a parte mais rígida da peça (aba em U de 3,0 mm com lábio de 3,5 mm). O que
   precisa ser testado no protótipo é se a face comprida cede o bastante para **ovalizar o bocal** e
   soltar o aro — é o único caminho por onde essa flexão vira defeito funcional.
2. **Bombê de 1,0 a 1,5 mm na face comprida.** Lê como reta a olho nu e transforma o painel num arco
   raso, que é como todo pote de linha resolve isso. Não é parede conada — a saída de extração
   continua 0,5°, o molde continua de extração simples, sem gaveta. É a opção que eu levaria.
3. **Voltar o ASP de 1,75 para ~1,55.** A face comprida cai para ~105 mm e a flecha do 2,4 L para
   ~2,3×, ao custo de uma frente 5 mm mais larga.

O número honesto sobre esses 3,8×: a razão é confiável, porque só a geometria mudou entre as duas
colunas. A **flecha absoluta** não é — depende de carga de aperto e de engastamento real, e pedia
elemento finito ou protótipo. Nenhuma das duas revisões foi prototipada.

### 3.4 Quanto de saída é "reto"

Saída zero não extrai: a peça agarra o macho. O que se faz é a saída mínima de extração.

| Saída/lado | Base mais estreita que o topo | Aninhamento de 6 potes de 2,4 L |
|---|---|---|
| 0,25° | 2,1 mm (1,5%) | 1.452 mm — **não aninha** |
| **0,50°** | **4,2 mm (3,0%)** | **1.044 mm (−28%)** |
| 0,75° | 6,3 mm (4,5%) | 777 mm (−47%) |
| 1,00° | 8,4 mm (6,0%) | 643 mm (−56%) |

**Recomendação: 0,5°/lado.** No maior pote a base fica 4,2 mm mais estreita que o topo em 141,6 mm de
largura — 3,0%, imperceptível com canto R10 e parede polida. Abaixo disso a peça deixa de aninhar a
vazio e o frete do pote vazio sobe ~28%.

Condições para a parede reta funcionar na extração:
- **acabamento polido** (SPI A2 ou melhor) nas laterais — textura exige saída extra (~1° a cada
  0,025 mm de profundidade de textura) e mataria o "reto";
- **extração por placa impulsora** (não por pinos), com **válvula de ar no topo do macho** para
  quebrar o vácuo;
- força de extração estimada em ~5 kN no 2,4 L (932 cm² de contato) contra ~62 kN disponíveis numa
  injetora de 380 t — **força não é o problema; curso de extração e vácuo são**;
- o canto R10 ainda é aliado, mas menos que o R18: reduz o arrasto nos cantos, que é onde a peça reta costuma marcar.

## 4. Validação nas injetoras

### 4.1 O que cada tamanho exige

| Tamanho | Área proj. | Fecham. 2 cav | Curso abert. mín. | Altura de molde | Injeção 2 cav | L/t |
|---|---|---|---|---|---|---|
| 600 ml | 146 cm² | 135 t | 136 mm | ~252 mm | 120 cm³ | 115 |
| 1,2 L | 146 cm² | 144 t | 268 mm | ~312 mm | 190 cm³ | 161 |
| 1,8 L | 146 cm² | 154 t | 400 mm | ~372 mm | 273 cm³ | 194 |
| 2,4 L | 146 cm² | 161 t | 532 mm | ~432 mm | 366 cm³ | 223 |

A área projetada é a silhueta do **deck da tampa**, que é a medida máxima da linha:
154,8 × 91,1 mm = **146 cm²**. Cresceu 17% sobre a revisão 6 (125 cm²), porque o colar afastou o
corpo e a tampa passou a cobri-lo. Com isso o 600 ml pede **135 t: 84% de uma injetora de 160 t**,
acima do limite prático de 80% — então **ele volta para a classe de 200 t**, junto com o 1,2 L. A
alocação de 160 t que a revisão 6 tinha conquistado se perde. É um dos preços do colar.

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

O 2,4 L com 2 cavidades usa 139 t numa máquina de 380 t (37% do fechamento). Com **4 cavidades**
(~278 t, molde ~620 × 500 mm, cabe entre as colunas de uma 380 t) dobra a produção na mesma hora
de máquina. Mesma avaliação para o 1,8 L numa 250 t.

### 4.4 Bloqueio de dado

`AD_INJETORAFICHA` tem **1 registro com os 29 campos de especificação nulos**. Com parede reta o
dado que faltava ficou mais crítico, porque a extração passa a ser o ponto de projeto. Preencher
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
exatamente o que mata um aro axial. A aba em U continua valendo, agora para limitar a flexão a menos
que a compressão de 0,20 mm, não para segurar a tampa.

### 5.2 Cotas

```
boca do pote ......... 145,0 mm (parede da borda 1,80 mm nos quatro tamanhos)
face do plug ......... 143,8 mm — folga de 0,60 mm por lado
parede do plug ....... 1,50 mm
canaleta ............. 0,60 mm de profundidade, entre 5,0 e 7,4 mm abaixo da borda
aro de TPE ........... seção 2,4 × 1,8 mm, sobra 1,20 mm da face do plug
                       -> 0,20 mm de compressão contra a parede
plug desce ........... 12 mm dentro do pote
vão da bandeja ....... 142,2 mm, recebe o FUNDO RETO de 140,56 mm
```

O plug faz três coisas de uma vez: **veda**, **forma a parede da bandeja** onde o pote de cima
apoia, e **centra a tampa**. Por fora não há saia nenhuma — a tampa fica rente à aba da borda.

### 5.3 O que ainda precisa de atenção

**Retenção do aro.** A canaleta tem 0,60 mm de profundidade — 0,5% da largura da peça. Um plug de
parede fina sai disso **por arranque** (stripping), com rampas de 30° nos dois ombros, sem gaveta no
molde. O aro é montado depois, esticado sobre o plug; a própria tensão do aro mais os dois ombros o
seguram contra o atrito da parede. **Confirmar no primeiro tryout** — é o ponto que mais merece
teste de vida (abrir e fechar 500 vezes e ver se o aro migra).

**Ar preso.** O aro só encosta nos últimos 2 mm do curso, mas isso ainda comprime o ar de dentro:

| | Δp | Força a mais |
|---|---|---|
| 600 ml | 3,5 kPa | 3,8 kgf |
| 1,2 L | 1,8 kPa | 1,9 kgf |
| 2,4 L | 0,9 kPa | 0,9 kgf |

No 600 ml dá para sentir. Reduz-se com **chanfro de 30° × 1,5 mm na boca**, que atrasa o contato do
aro. E é o mesmo "pop" que a OXO transformou em argumento de venda — pode virar característica em
vez de defeito.

**Aba de alavanca.** Sem saia externa, é preciso um ponto para levantar: uma aba de ~18 mm numa das
laterais curtas, com rebaixo correspondente na aba da borda para ficar rente ao perfil. É o que
mantém o "liso" e ainda permite descascar.

**Montagem.** O aro volta a ser peça montada — não existe bi-injeção no parque. 1,8 g de TPE mais
alguns segundos de montagem por tampa. O lado bom: o **mesmo aro serve as três tampas** (padrão,
dosadora e teca), então o molde do aro amortiza em toda a linha. Esse argumento, que eu tinha
derrubado na revisão 3, volta a valer.

### 5.4 O que entrega

**Entrega:** vedação contra umidade, poeira e cheiro, e resistência a tombo com o pote deitado.
Vedação radial com aro é o mesmo princípio de um O-ring — segura pressão, não só poeira.

**Não entrega sem teste:** estanqueidade garantida de cabeça para baixo com líquido. Com 0,20 mm de
compressão e a borda enrijecida é **plausível**, mas isso se mede no protótipo, não se promete na
planilha. Primeiro tryout com água colorida, pote deitado e de cabeça para baixo, 24 h.

### 5.5 Orçamento de altura

```
borda do pote ................... 62,0 mm   (600 ml)
piso da bandeja da tampa ........ 60,0 mm   = PLANO MODULAR, 2,0 mm abaixo da borda
vão livre da bandeja ............ 142,2 × 78,5 mm  (recebe o fundo reto de 140,56)
plug .......................... desce até 12 mm abaixo da borda, dentro do pote
```

O pé do pote de cima tem que pousar no piso **junto à parede da bandeja** — que agora é a parede do
plug. A carga desce plug → borda → parede do pote.

### 5.6 Capacidade de borda × capacidade útil

Número que nenhuma revisão anterior tinha olhado, e que a placa de teca tornou grande demais para
ignorar: **o plug come volume**. A capacidade nominal é de **borda** — convenção do setor e de todas
as revisões anteriores —, mas a tampa desce 2,0 mm (plano modular) mais a espessura dela:

| Tampa | Desce | Desloca | 600 ml | 1,2 L | 1,8 L | 2,4 L |
|---|---|---|---|---|---|---|
| Teca (placa 8 mm) | 10,0 mm | 115 ml | **485 ml** | 1.085 ml | 1.685 ml | 2.285 ml |
| PP/PE (plug 6 mm) | 8,0 mm | 92 ml | **508 ml** | 1.108 ml | 1.708 ml | 2.308 ml |

No 600 ml a teca leva **19% do volume**. Nos tamanhos maiores o peso relativo cai (5% no 2,4 L),
porque o deslocamento é constante e a capacidade cresce.

**Decisão em aberto:** rotular por borda (como está) ou re-resolver a linha para que a capacidade
*útil* seja 600n. A segunda opção sobe as alturas e quebra o passo de 60 mm — teria de vir com um
módulo novo.

---

## 6. As duas tampas

Duas tampas, **um só filete de TPE**. Foi o objetivo perseguido desde a revisão 4, e só fechou
aqui, quando a borda ficou lisa: com a aba em U, cada tampa precisava de uma geometria diferente.

| | **Teca** | **PP/PE com trava** |
|---|---|---|
| O que é | placa maciça 143,8 × 80,1 × 8,0 mm | plug + deck + 6 abas |
| Vedação | filete de TPE em friso usinado, radial | o **mesmo** filete, em friso moldado |
| Retenção | **só atrito**: 7,3 kgf reto, 1,2 descascando | **trava**: 6 abas, 12 kgf |
| Plano modular | o **topo da placa** é o plano | o piso da bandeja |
| Peso / custo | 60 g em teca · CNC, sem molde | 21,7 g em RP 141 · R$ 0,21 |

### 6.1 Tampa com trava

**A aresta de engate já existe no colar.** A face de baixo dele dá **3,46 mm por lado** de encosto —
o dobro do que a farpa usa. Não foi preciso inventar canaleta: canaleta externa num retângulo
pediria gaveta no molde.

```
deck ............ passa 3,10 mm/lado do colar -> 154,8 × 91,1 mm (medida máxima da linha)
abas ............ 6 × 18,0 × 1,00 mm; face interna 149,2 (folga 0,30 sobre o colar)
farpa ........... avança 1,85 mm sob o colar; braço de 8,0 mm da dobradiça até ela
rabo ............ 5,0 mm abaixo da farpa, para o dedo
plug ............ desce 6,0 mm na boca, com o friso do filete
bandeja ......... piso 2,0 mm abaixo da borda = plano modular
```

**Cada aba fecha com ~2 kgf, uma de cada vez** — é assim que se fecha um pote de travas, não as
seis juntas. As seis seguram **12 kgf** de arranque, contra os 7,3 kgf que o filete sozinho dá.

**É essa a diferença entre as duas tampas.** Na teca o filete faz as duas coisas: veda e segura.
Na de trava ele **só veda** — quem segura é a aba. Por isso a de trava pode prometer hermeticidade
sob transporte e a de teca não.

### 6.1.1 O que não está resolvido na trava

**A extração das abas.** Cada farpa é uma contra-saída de 1,85 mm num trecho de 18 mm, voltada para
dentro. Em peça retangular isso normalmente pede gaveta. A saída usual é arraste com a aba
flexionando — o PP randômico aguenta —, mas é item de ferramentaria, não de projeto de produto, e
precisa ser fechado antes de orçar o molde.

**A dobradiça viva.** O braço de 8,0 mm com 1,00 mm de espessura funciona como viga engastada no
cálculo, mas uma trava de pote real é **sobre-centro**: ela passa de um ponto morto e trava. Essa
geometria não está modelada — o que existe é a farpa e o encosto. Detalhar a dobradiça é o próximo
passo do desenho da tampa.

### 6.2 Tampa de teca

Cadeia própria: teca em tora e ripa serrada (CODPROD 6759), planta **WOOD** (CNC RXK2513,
moldureira, lixadeiras, prensa de alta frequência) e a **Teak Brazil**. Tampa de madeira já é
produto corrente com FSC 100%. Sem molde — programa de CNC e gabarito.

**Placa maciça de 143,8 × 80,1 × 8,0 mm**, ~60 g em teca seca, com **friso usinado na face lateral**
alojando o filete de TPE. Sem trava: segura pelo atrito do filete, 7,3 kgf reto.

**O ponto que estava em aberto na revisão 6 fechou sozinho.** Lá a teca precisaria de um poço da
bandeja usinado, senão não empilharia. Agora **o topo da placa É o plano modular**: ele fica 2,0 mm
abaixo da borda e o fundo reto do pote de cima pousa direto nele. Nada a usinar.

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
| PEBD PB 608 | R$ 11,10/kg | 0,5 t | (descartado — ver seção 6) |
| TPE Karinprene 45 | sem compra | — | aro de vedação, a recotar |

| Item | Peso | Resina |
|---|---|---|
| Corpo 600 ml | 47,0 g | R$ 0,52 |
| Corpo 1,2 L | 74,6 g | R$ 0,83 |
| Corpo 1,8 L | 107,4 g | R$ 1,19 |
| Corpo 2,4 L | 144,1 g | R$ 1,59 |
| Tampa de teca (placa maciça 8 mm) | 60 g em teca | CNC, sem resina |
| **Filete de TPE (nas duas tampas)** | **0,7 g** | a cotar |

Só matéria-prima. Transformação entra pelo custo do PCP; a tampa de teca, pelo custo da WOOD.

**O que a revisão 5 custou em resina.** Os quatro corpos somam **366,7 g** contra 349,1 g no
desenho R18 de 121,2 × 93,2 — **+17,6 g, +5,0%**, ou R$ 0,19 por jogo de quatro. Os dois efeitos
empurram para o mesmo lado: mesma área com frente estreita tem mais perímetro, e canto menos
arredondado também. Metade vem do ASP, metade do raio.

---

## 8. Ferramental

Escopo na revisão 7: **4 moldes de corpo + 1 molde de tampa com trava + 1 molde de filete de TPE
= 6 ferramentas.** A tampa de teca não usa molde (CNC); o filete agora serve **as duas**.

**Os moldes de corpo ficaram mais simples.** Sem aba em U e sem pé embutido, a peça só estreita
descendo do colar: duas placas, sem gaveta e sem extração por arraste. O rebaixo da trava é a face
de baixo do colar, não uma canaleta — canaleta externa num retângulo exigiria gaveta.

**A tampa com trava é que ficou mais difícil.** As 6 abas têm farpa voltada para dentro: cada uma é
uma contra-saída de 1,85 mm num trecho de 18 mm. Em peça retangular isso normalmente pede gaveta;
a saída usual é extração por arraste com a aba flexionando. O PP randômico aguenta, mas **é o item
a fechar com a ferramentaria antes de orçar.**

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
   da bandeja, aba de alavanca para abrir, e bandeja-vertedor na versão de líquidos (6.3).
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

---

## 12. Modelo 3D

`gera-3d.py` constrói o sólido a partir das mesmas cotas e escreve **sete** STL em `stl/`:
os quatro corpos, a placa de teca, a tampa com trava (com as 6 abas) e o filete de TPE. O visualizador interativo remonta a malha a partir
da mesma receita de anéis, bandas e tampos (`perfis.json`), então desenho e STL não divergem.

**Como o sólido é construído:** cada peça é uma casca fechada feita de seções de retângulo com
cantos arredondados empilhadas em alturas diferentes; bandas de quadriláteros ligam um anel ao
seguinte e tampos em leque fecham as pontas.

**Conferências que a malha faz sozinha** (saem no terminal a cada geração):

| Verificação | Resultado |
|---|---|
| Volume assinado positivo **e normais consistentes** nas sete peças | sólido fechado e orientado para fora |
| Cavidade × capacidade nominal | 599,9 / 1200,0 / 1800,5 / 2401,2 ml contra 600 / 1200 / 1800 / 2400 — dentro de **0,06%** |
| Peso da malha × `calculo-modular.py` | 47,1 / 74,9 / 108,0 / 145,2 g nos corpos, 60 g na placa de teca e 21,7 g na tampa com trava |
| Malha do visualizador × STL do Python | `verifica-malha.js`: 0,00% nas sete peças |

**Na revisão 7 a verificação pegou três erros que leitura não pegaria:**

1. **O filete estava 0,40 mm aquém da boca.** A fórmula da face externa usava `FILETE_SOB − FRISO_PROF`
   em vez de `FILETE_D − FRISO_PROF`. A peça ficava com folga onde deveria ter 0,20 mm de
   interferência: **não vedaria nada**, e nenhuma checagem de malha acusa — malha estanque,
   normais certas, volume positivo. Só apareceu na conferência de montagem, comparando cota a cota.
2. **Metade das abas entrava espelhada no visualizador.** Os prismas dos lados de coordenada
   negativa saem espelhados, e espelhar inverte a mão: três abas com volume negativo cancelavam as
   outras três. O total batia com o de uma tampa **sem aba nenhuma**. O gerador Python já se
   corrigia; o JS não.
3. **O STL saiu com Y para cima em vez de Z.** Volume assinado e checagem de normais são agnósticos
   a eixo e passaram os dois. Apareceu quando a medida de área de contato com a mesa deu **zero**.

**A checagem de normais entrou na revisão 6, e entrou porque falhou.** A tampa PE saiu com o piso da
bandeja invertido: a malha ficou **estanque**, o volume assinado devolveu um número plausível
(17,5 g) e nada acusou. O volume real era 27,6 g — 58% a mais. Volume assinado sozinho não detecta
normal invertida; `normais_consistentes()` confere que toda aresta aparece uma vez em cada sentido,
e agora o gerador **aborta** se alguma peça falhar.

A folga de 0,7% na cavidade é a poligonal de 12 segmentos por canto, não erro de cota
(`--seg 24` reduz). `verifica-malha.js` roda o construtor do visualizador fora do navegador e
confere o volume contra o STL — as seis peças batem.

**O que o modelo não é.** É malha, não sólido CAD: serve para conferir encaixe, empilhamento e
volume, e para imprimir protótipo. **O molde precisa do CAD paramétrico do projetista.** Estão no
modelo a aba da borda, o plug e o aro na canaleta; faltam a aba de alavanca, o chanfro de entrada da
boca e o furo e o entalhe do vertedor da seção 6.3. O aro está desenhado na medida livre, e por isso
invade 0,2 mm a parede no modelo — é justamente a interferência.

O corte do visualizador é onde se vê a vedação: o plug descendo dentro do pote e o aro trabalhando
contra a parede.


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
