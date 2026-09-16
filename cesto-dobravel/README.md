# Linha Cestos Organizadores Dobráveis Empilháveis em PP

**Status:** estudo de viabilidade técnica · **Data:** 16/09/2026
**Origem:** vídeo de referência recebido em 16/09/2026 · **Planta:** Nitron – Fábrica (CODPLP 1)
**Mandato no ERP:** Projeto 100 "Relançar caixa dobrável" — **Aprovado** desde 04/10/2021, sem molde lançado

Documento de engenharia para o pedido: cesto organizador **vazado**, **dobrável**, **empilhável com
acesso frontal**, em **3 tamanhos**, com **cantos arredondados e desenho contemporâneo**, alvo de
**e-commerce** e uso doméstico (B2C). Ferramental novo, orçamento aberto.

Todo número de máquina, resina, custo, ferramental e venda abaixo saiu do Sankhya (produção,
compras, cadastro de centros de trabalho, custos, projetos e faturamento), não de estimativa de
catálogo. As fontes estão citadas em cada seção. A memória de cálculo é `calculo-dobravel.py`.


> **Correção de 16/09/2026 — leia antes das seções 4, 6, 7, 9 e 10.**
> O modelo 3D (`cad/modelo3d.py`) mostrou que este estudo contava a saia do
> fundo duas vezes: calculava o painel com a altura externa cheia, quando o
> painel começa no topo da saia. Peso, tonelagem, ferramental e payback abaixo
> foram corrigidos com o volume do sólido real; **a conclusão da seção 7.2
> mudou de sinal** e está refeita. O detalhamento e a lista completa de
> correções estão em [`P-especificacao.md`](P-especificacao.md), seção 1.

---

## 1. Veredito

| Requisito | Situação |
|---|---|
| Cesto vazado dobrável empilhável | **Viável** — a casa já fabrica caixa dobrável (ref. 213) desde antes de 2019 |
| 3 tamanhos com empilhamento coerente | **Viável e resolvido** — passo único de 58 mm, duas P = uma G (seção 4) |
| Dobrar plano | **Viável, e é a restrição que dimensiona o produto** — obriga largura interna ≥ altura do painel traseiro (seção 4.2) |
| Cantos arredondados | **Viável com uma regra rígida**: o raio mora no fundo e nas colunas de canto; **os painéis têm que ficar planos** (seção 5) |
| Injeção no parque atual | **Cabe sem máquina nova**, mas o fundo monopoliza a INJ 34 (600 t) em campanha (seção 7) |
| Resina | **Já é compra de rotina** — PP CP 141 copolímero, 109 t em 12 meses (seção 8) |
| Ferramental | **USD 114,6 mil FOB** para a família inteira: 4 moldes + 6 jogos de inserto (seção 9) |
| Payback | **≈ 17,8 meses** a 21.500 un/ano por tamanho (seção 10) |
| Ganho de e-commerce | **Frete cobrado cai 6,3× no tamanho G** (6,84 → 1,09 kg cubados) — é a tese do produto (seção 6) |
| Ficha das injetoras | **Bloqueio de dado, herdado** — `AD_INJETORAFICHA` segue vazia (seção 7.3) |

O ponto crítico desta linha não é tonelagem nem custo: é **geometria de dobra**. Um painel
articulado numa aresta tomba sobre a dimensão oposta, então a altura do painel traseiro não pode
passar da largura interna do fundo. Com os painéis embutidos, os quatro tombam **para dentro da
bandeja** — e por isso os três tamanhos fecham na mesma altura dobrada de 37 mm, o que dá uma
caixa master única para a família.

---

## 2. O que o vídeo mostra

Leitura técnica dos 88 s (frames extraídos a 1/4 s; **o áudio não foi transcrito** — o download do
modelo de voz está bloqueado pelo proxy desta sessão, então nada do que foi falado entrou aqui).

**Peça 1 (0–60 s) — a referência adotada.** Cesto retangular laranja, paredes laterais e traseira
vazadas com rasgos oblongos em malha densa, **fundo sólido com ponto de injeção central**, **frente
rebaixada** com recorte de pega e lingueta no meio. As quatro paredes são **painéis planos
articulados no fundo**, por pino em berço (não dobradiça viva). Empilha por pé que assenta no berço
do rim — aparece empilhado em dois níveis, com a frente rebaixada dando acesso ao conteúdo **sem
desempilhar**. É esse o produto.

**Peça 2 (60–88 s) — fora de escopo.** Bin preto de parede lisa, borda com perfil estruturado,
porta-etiqueta cinza na frente e encaixe macho/fêmea que acopla duas unidades lado a lado. É bin de
picking industrial, não B2C. Foi descartada por decisão de escopo, não por inviabilidade — o mesmo
chassi de fundo serviria a ela numa segunda fase.

O que a referência tem de **errado para o alvo B2C** e precisa mudar: cantos vivos, malha de rasgos
pequena e utilitária (cara de caixa de feira), e nenhuma continuidade com a identidade da linha.
As três coisas são tratadas na seção 5.

---

## 3. O que já existe na casa

| Achado | Fonte |
|---|---|
| **Projeto 100 "Relançar caixa dobrável" — status Aprovado**, 04/10/2021. Observação registrada: *"Fazer colorida multicores? Preto ficava muito apagado."* Nunca gerou molde | `AD_PROJETOS` |
| **Caixa Prática Dobrável 20 L (ref. 213)** em linha, 425 × 295 × 202 mm, 800 g, arquitetura de 4 peças distintas: aro (213-A), bandeja (213-B), lateral fixa (213-LF), lateral móvel (213-LG) | `TGFPRO` |
| Projeto 66 "Cestos empilháveis": *"Fazer PMG. Pensar em algo diferente dos furinhos desse modelo"* — Aguardando Decisão | `AD_PROJETOS` |
| Projeto 112 "Organizador empilhável Sterilite": *"trava, dobradiça, divisória, empilhamento"* — Aguardando Decisão | `AD_PROJETOS` |
| Projeto 73 "Organizadores Modulares Fine": *"Desenhar os 3 tamanhos conforme amostras. Conseguimos reduzir peso?"* — Aguardando Decisão | `AD_PROJETOS` |
| Categoria organização: **249 SKUs, 2,29 milhões de peças, R$ 20,2 milhões em 12 meses** | `TGFITE`/`TGFCAB` |
| Âncoras de preço na categoria: organizadora rattan 16 L (069) **R$ 22,37**; gaveteiro 4 gav. (004) **R$ 22,22**; gaveteiro modular 8,2 L (254) **R$ 19,77**; flat 10,35 L (503) **R$ 12,54** | `TGFITE` 12 meses |
| **Amazon é cliente ativo**: FCs GRU5, GRU8 e XCV9 somam **R$ 292,6 mil em 12 meses** | `TGFCAB`/`TGFPAR` |
| Centros de trabalho de **MONTAGEM** já cadastrados (CODWCP 78, 79) | `TPRWCP` |

**O 213 é o alerta, não o modelo.** Ele desabou: 506 peças em 2023, 1.278 em 2024, **26 em 2025 e
20 em 2026** (`TGFITE`, notas liberadas). O projeto 100 reconhece o motivo na própria observação —
produto sem apelo visual. O relançamento não é problema de ferramental, é de desenho; e é
exatamente o que o pedido de "cantos arredondados e cara mais moderna" resolve.

**Recomendação de cadastro:** consolidar os projetos **100, 66, 112 e 73 num só** e desenvolver sob
o 100, que já está aprovado. Abrir projeto novo é recomeçar uma aprovação que a casa já deu.

---

## 4. A regra modular e a regra da dobra

### 4.1 Passo de empilhamento

```
módulo M = 58 mm
P = 2 M = 116 mm      M = 3 M = 174 mm      G = 4 M = 232 mm
```

O passo empilhado é a altura externa exata, porque o pé de cada peça assenta no berço do rim da
peça de baixo — sem sobra. Toda combinação fecha em múltiplo de 58 mm, e **duas P somam exatamente
uma G** (232 mm), que é a regra que o cliente percebe na prateleira.

| Combinação | Altura | |
|---|---|---|
| P + P | 232 mm | = G |
| P + M | 290 mm | 5 M |
| M + M / P + P + P | 348 mm | 6 M |
| G + G | 464 mm | 8 M |

### 4.2 A regra da dobra — a restrição que manda no projeto

Um painel articulado numa aresta de comprimento E **tomba sobre a dimensão oposta**:

- os dois **laterais** (277 mm, articulados nas arestas curtas) tombam sobre o **comprimento
  interno**, 331 mm → altura ≤ 325 mm, folgado;
- o **traseiro** (337 mm, articulado na aresta longa) tomba sobre a **largura interna**, 271 mm →
  **altura ≤ 265 mm**. Esta é a restritiva.

Com o G a 205 mm de painel, a margem é de 60 mm — sobra para um quarto tamanho (5 M = 290 mm,
~25 L) no futuro sem tocar no fundo.

Os painéis são **embutidos** (337 e 277 mm contra uma boca de 340 × 280 mm), então tombam **para
dentro da bandeja** e não sobre o rim. Acima de 37 mm quem manda é a saia do fundo, não os
painéis — e por isso **os três tamanhos fecham na mesma altura dobrada**.

**Ordem de dobra:** laterais → traseiro → frontal. No P os quatro tombam lado a lado sem se
sobrepor; no M e no G os laterais se sobrepõem, e aí os eixos de dobradiça precisam ser
**escalonados em ~3,8 mm por camada**. Como o fundo é comum aos três, **as orelhas já têm que sair
escalonadas no molde do fundo** — se isso não entrar na cotação, o M e o G não dobram.

### 4.3 Por que os dois painéis repetidos são os menores

Os painéis que existem em par são os de 277 mm (esquerdo e direito); o de 337 mm é único (traseiro).
Isso não é detalhe de nomenclatura: o molde de 2 cavidades é o do painel **menor**, o que derruba a
tonelagem de 341 t para 282 t e leva a lateral do G das 600 t para as 380 t (seção 7.1).

---

## 5. Cantos arredondados sem perder a dobra

O pedido de "cantos arredondados e cara mais moderna" tem uma consequência dura:

> **Painel que dobra plano não pode ter curvatura no plano horizontal.** Painel curvo não achata.

Então o raio não pode estar no painel. A regra de projeto é:

1. **Raio externo R15 no fundo** — a saia perimetral do fundo carrega o raio nos quatro cantos.
2. **Colunas de canto solidárias ao fundo**, subindo até a borda, com o mesmo R15 externo. São elas
   que dão o canto arredondado ao produto montado, e são elas que recebem o berço das dobradiças e
   as travas dos painéis.
3. **Os quatro painéis permanecem planos**, encaixando entre as colunas. A junta painel/coluna fica
   escondida na quina, não na face.

Ganho colateral: a coluna de canto é o elemento estrutural natural para receber a carga de
empilhamento, que hoje na referência do vídeo passa pela borda do painel.

**Vazado.** Trocar a malha densa de rasgos por **ripado vertical largo**, mantendo a mesma área
aberta — tira a cara de caixa de feira, conserva ventilação e visibilidade e reduz linhas de solda no
painel. O cálculo adota **35% de área aberta** como premissa de projeto (não é medição do vídeo, que
não dá para escalar); fechar para 30% engorda os painéis em ~7%. A alternativa, mais alinhada à linha, é usar a linguagem de textura que
a casa já domina (rattan/juta) na face externa dos painéis; o projeto 66 pede literalmente *"algo
diferente dos furinhos desse modelo"*.

**Painel plano é a geometria ideal para IML** (rótulo no molde). Vale registrar como caminho de
diferenciação B2C — mas **a capacidade de IML não está confirmada**: a coluna `TPRWCP.AD_IML` existe
e está **nula nas 89 linhas** do cadastro de centros de trabalho. Confirmar com a produção antes de
prometer decoração no molde.

**Cor.** Os campeões da categoria hoje são branco, preto e **chumbo**; o projeto 100 já avisou que
preto "ficava muito apagado" numa peça dobrável. Lançar em chumbo + branco, e usar o pigmento novo
citado no projeto 116 para "elevar o nível do produto".

---

## 6. Especificação dimensional e o ganho de e-commerce

**Footprint externo comum aos 3: 345 × 285 mm** · cavidade interna 331 × 271 mm · saia de 30 mm com
R15 e pé de 5 mm · frontal rebaixado a 55% do painel (50 / 80 / 115 mm) · parede de painel 1,8 mm,
fundo 2,2 mm, moldura de painel 3,0 mm.

| Tamanho | Altura ext. | Passo | Volume | Peso | Altura dobrada | Compactação |
|---|---|---|---|---|---|---|
| P | 116 mm | 2 M | **9,76 L** | 436,7 g | 37 mm | 3,1× |
| M | 174 mm | 3 M | **14,96 L** | 514,8 g | 37 mm | 4,7× |
| G | 232 mm | 4 M | **20,16 L** | 588,8 g | 37 mm | 6,3× |

Módulo de 58 mm (e não 54: com os painéis embutidos o volume interno caiu, e 58 mm devolve as
litragens redondas). Pesos medidos no volume do sólido, não estimados por área.

Comercializar como **10 L / 15 L / 20 L**. O G reencontra os 20 L do ref. 213 — e com **588,8 g
contra 800 g, é 26% mais leve que a caixa dobrável que a casa faz hoje**, o que responde à pergunta
aberta no projeto 73.

### Decomposição de peso (g)

| | fundo | lateral | × 2 | traseira | frontal | total |
|---|---|---|---|---|---|---|
| P | 280,9 | 38,3 | 76,6 | 45,8 | 33,4 | **436,7** |
| M | 280,9 | 58,0 | 116,0 | 69,0 | 48,8 | **514,8** |
| G | 280,9 | 75,0 | 150,1 | 88,9 | 68,9 | **588,8** |

O fundo é 48% do peso do G e **64% do peso do P**.

### O ganho de frete

Fator de cubagem rodoviário de 300 kg/m³. O que a transportadora cobra é o maior entre peso real e
peso cubado:

| Tamanho | Montado | Peso cubado | Dobrado | Peso cubado | Frete cobrado |
|---|---|---|---|---|---|
| P | 11,41 dm³ | 3,42 kg | 3,64 dm³ | 1,09 kg | **3,1× menor** |
| M | 17,11 dm³ | 5,13 kg | 3,64 dm³ | 1,09 kg | **4,7× menor** |
| G | 22,81 dm³ | 6,84 kg | 3,64 dm³ | 1,09 kg | **6,3× menor** |

**É isso que justifica o produto no canal.** O que o histórico da Amazon mostra é justamente a
ausência do volumoso: nos R$ 292,6 mil de 12 meses, o que vende são frasqueiras e gaveteiros densos
(137 a R$ 11,13; 142 a R$ 21,19; 004/4P a R$ 21,65), enquanto o organizador flat 10,35 L fez **222
peças** e o cesto transporta-tudo **336**. Organizador vazado é oco: paga frete de ar. Dobrado, o G
sai de 6,84 para 1,09 kg cobrados — a categoria inteira muda de patamar no e-commerce.

Efeito no armazém, pela mesma conta: num pallet PBR (1.200 × 1.000 mm) com 1,80 m de empilhamento
útil cabem **9 peças por camada**; montado o G dá 7 camadas (**63 peças**), dobrado dá 48 camadas
(**432 peças**) — **6,9× mais por pallet**. E como os três tamanhos dobram na mesma altura, o
pallet leva 432 peças de qualquer litragem.

---

## 7. Validação nas injetoras

### 7.1 Alocação — tudo cabe no parque confirmado

Fechamento a 0,32 t/cm² (PP parede fina com **câmara quente valvulada sequencial**) + 10% de canal,
limitado a 80% da capacidade da máquina. Área projetada do painel desconta o vazado.

| Peça | Cav. | Fechamento | Máquina | Uso | Injetoras |
|---|---|---|---|---|---|
| Fundo (comum aos 3) | 1 | 346 t | 600 t | 58% | **INJ 34** |
| Lateral P | 2 | 126 t | 160 t | 79% | INJ 7–12, 36, 40, 41 |
| Traseira P | 2 | 151 t | 200 t | 75% | INJ 1–6, 19–22, 35, 37 |
| Frontal P | 2 | 119 t | 150 t | 79% | INJ 42, 43 |
| Lateral M | 2 | 205 t | 280 t | 73% | INJ 29 |
| Traseira M | 2 | 245 t | 380 t | 64% | INJ 31, 32, 33 |
| Frontal M | 2 | 190 t | 250 t | 76% | INJ 23–28, 38, 39, 46 |
| Lateral G | 2 | 272 t | 380 t | 72% | INJ 31, 32, 33 |
| Traseira G | 2 | 324 t | 600 t | 54% | INJ 34 |
| Frontal G | 2 | 273 t | 380 t | 72% | INJ 31, 32, 33 |

Só o fundo precisa de máquina grande, e ocupa pouco: a 21.500 unidades/ano com ciclo estimado de
28 s e 1 cavidade, são **~170 h/ano da INJ 34**, 2% de um turno único. Fundo e traseira do G
rodam na mesma máquina em campanhas separadas (40 min de setup, `TPRWCP.TEMPOSETUP`).

### 7.2 Encolher o fundo: viável, e a decisão é de risco, não de geometria

**Esta seção dizia o contrário e estava errada** (ver o aviso no topo). Com a altura de painel
correta — painel = altura externa − 27 mm, e não a altura externa cheia — o footprint menor
**cabe**:

| | 345 × 285 (recomendado) | 340 × 254 (alternativa) |
|---|---|---|
| Fechamento do fundo | 346 t | 303 t |
| Máquina do fundo | 600 t (INJ 34), 58% | **380 t (INJ 31/32/33), 80%** |
| Painel do G | 205 mm | 205 mm |
| Limite de dobra | 265 mm | 239 mm — **passa** |
| Volume do G | 20,16 L | ~19,9 L |

A alternativa libera a única 600 t da casa e espalha o fundo em três máquinas. O preço é rodar a
**80% do fechamento, sem folga**, sobre um coeficiente de pressão (0,32 t/cm²) que é premissa e só
se confirma no try-out — no molde mais caro da família.

**Recomendação: manter 345 × 285.** Não por geometria, mas por risco: a INJ 34 tem folga
documentada e descobrir no try-out que o fundo não fecha na 380 t custa mais que o ganho. Vale
levar a pergunta à ferramentaria: se a MR Plastic Mould garantir 0,30 t/cm² com valvulado
sequencial, a alternativa passa a ter folga e muda a recomendação.

### 7.3 Bloqueio de dado — herdado do estudo dos potes

`AD_INJETORAFICHA` (ficha Haitian, 1:1 com `TPRWCP`) continua com **1 registro e todos os campos de
especificação nulos**. Curso de abertura, altura máx/mín de molde e distância entre colunas seguem
**não conferíveis no sistema**. Para esta linha o risco é menor que no dos potes — a peça mais
profunda tem 232 mm contra os 250 mm do pote de 2 L — mas o molde do fundo tem 620 × 540 mm de
bloco e **a distância entre colunas da INJ 34 precisa ser medida em campo antes do pedido**.

### 7.4 Centros de trabalho "NITRON" — capacidade não confirmada

`TPRWCP` tem 13 centros nomeados apenas "NITRON" (CODWCP 47–59) com capacidades cadastradas de até
**1.100 t**, além de duas de 650 t e três de 600 t. Eles têm atividades com início e aceite
registrados entre 06/2022 e 01/2026 (`TPRIATV`), **nenhuma concluída** (`DHFINAL` nulo), nenhum
parceiro terceiro vinculado e nenhum monitoramento de ciclo. Não entraram na alocação da seção 7.1.

**Se a 1.100 t existir e estiver disponível, muda o projeto**: o fundo iria a 2 cavidades (692 t,
63%) e a linha dobraria de capacidade sem molde adicional. Vale uma pergunta à produção antes de
fechar o pedido de ferramental.

---

## 8. Material

**PP copolímero CP 141 (CODPROD 994) — R$ 10,52/kg, 108,9 t compradas em 12 meses, 221 notas, última
em 15/09/2026** (`TGFITE`/`TGFCAB`).

É a escolha obrigatória, não preferência: a dobradiça de pino em berço e as travas de painel
**flexionam em uso repetido**, e o homopolímero que domina a casa (PP H 105 com clarificante, 926 t
no ano) é frágil ao impacto e trinca no berço. O copolímero já é **compra de rotina** — não abre
cadeia nova de fornecimento, diferente do que aconteceu com o TPE e o PEBD no estudo dos potes.

| Alternativa | Preço | Volume 12 m | Leitura |
|---|---|---|---|
| **PP CP 141 copolímero** | **R$ 10,52/kg** | 108,9 t | **Recomendado** — impacto e fadiga na dobradiça |
| PP RP 141 randon fl. 40 | R$ 9,54/kg | 299,1 t | Aceitável no fundo; evitar nos painéis articulados |
| PP H 105 homopol. c/ clarif. | R$ 11,06/kg | 925,9 t | **Não** — frágil no berço de dobradiça |
| PP moído preto 0055 | R$ 6,19/kg | 336,8 t | Só como carga parcial no fundo; nunca na dobradiça |

Custo de resina por conjunto do G: 0,689 kg × R$ 10,52 = **R$ 7,25**.

---

## 9. Ferramental

Quatro moldes cobrem os três tamanhos, porque **fundo e frontal são comuns** e os painéis variam só
em altura — resolvida por **inserto de altura**, não por molde novo.

| Molde | Cav. | Bloco | Aço | FOB USD | Observação |
|---|---|---|---|---|---|
| Fundo | 1 | 620 × 540 × 520 | 1.367 kg | **30.133** | câmara quente 4 bicos valvulados |
| Lateral | 2 | 700 × 460 × 460 | 1.163 kg | **29.278** | + 2 jogos de inserto (M e G) |
| Traseira | 2 | 700 × 460 × 460 | 1.163 kg | **29.278** | + 2 jogos de inserto (M e G) |
| Frontal | 2 | 700 × 420 × 400 | 923 kg | **25.924** | + 2 jogos de inserto (M e G) |
| | | | | **114.614** | |

Subiu dos USD 86,2 mil estimados por dois motivos legítimos: o frontal deixou de ser comum aos
três (70 mm fecharia o acesso do P e deixaria o G aberto demais — a altura passou a ser 55% do
painel), e os insertos de altura carregam as próprias filas de pinos de furo, então custam
USD 6,5 mil e não USD 4 mil o jogo.

**Rodar o P primeiro é barato:** os 4 moldes base (USD 75,6 mil) são do P e o M e o G os herdam;
cada litragem seguinte entra por **3 jogos de inserto, ~USD 19,5 mil**, sem molde novo.

Preço calculado a **14 USD/kg de bloco**, que é a média dos três moldes comparáveis da casa
(`AD_MOLDE` + `AD_ORCAMENTO`, todos com a **MR Plastic Mould**):

| Referência | Bloco | Peso | Máquina | FOB USD | USD/kg |
|---|---|---|---|---|---|
| 283-C corpo lixeira 12 L | 720 × 770 × 690 | 3.000 kg | 380 t | 36.900 | 12,3 |
| 284-U organizador limpeza | 600 × 550 × 600 | 1.556 kg | 280 t | 20.100 | 12,9 |
| 214-U organizador duplo | 450 × 550 × 580 | 1.128 kg | 250 t | 18.900 | 16,8 |

Para calibrar a ordem de grandeza: o molde único do projeto 115 (potes modulares, 2 cavidades) foi
aprovado a **USD 47.100**. USD 114,6 mil por uma família de 3 tamanhos, com 4 moldes e 6 jogos de
inserto, está dentro da escala de compra da casa.

**A nacionalização não está calculada aqui.** O valor é FOB; frete, II, IPI e ICMS sobre molde
importado (NCM 8480.71) precisam vir do fiscal, e se há ex-tarifário aplicável. Para o payback usei
**+30%** como provisão e **R$ 5,45/USD** — os dois são premissa minha, não dado do ERP: não achei
tabela de cotação preenchida (`TSIMOE` existe, `TSIMOD` não é cotação, e a taxa implícita em
`TGFCAB.VLRMOEDA` volta inconsistente). **Trocar por câmbio e alíquota reais antes de decidir.**

---

## 10. Custo, preço e payback

### 10.1 O modelo de custo saiu do próprio ERP

`TGFCUS` cruzado com o peso de peça de `TGFPRO` dá uma regra estável para a linha de organização:

| Produto | Peso | Custo médio | R$/kg | Preço médio | R$/kg |
|---|---|---|---|---|---|
| 065 organizadora 2 L | 150 g | R$ 3,25 | 21,7 | — | — |
| 284 cesto transporta tudo | 300 g | R$ 5,53 | 18,4 | R$ 13,49 | 45,0 |
| 503 flat 10,35 L | 396 g | R$ 5,53 | 14,0 | R$ 12,54 | 31,7 |
| 069 organizadora 16 L | 549 g | R$ 10,57 | 19,2 | R$ 22,37 | 40,7 |
| 254 gaveteiro modular 8,2 L | 561 g | R$ 10,85 | 19,3 | R$ 19,77 | 35,2 |
| 004 gaveteiro 4 gavetas | 590 g | R$ 12,32 | 20,9 | R$ 22,22 | 37,7 |
| 213 caixa dobrável 20 L | 800 g | R$ 12,93 | 16,2 | — | — |

Os seis produtos vivos ficam numa faixa de **R$ 14,0 a R$ 21,7 por kg de custo** (média 18,9) e
**R$ 31,7 a R$ 45,0 por kg de preço** (média 38,1). O cálculo adota **R$ 19,50/kg de custo e
R$ 36,00/kg de preço** — de propósito acima da média no custo e abaixo no preço, para a estimativa
errar contra o projeto e não a favor. Margem resultante: 45,8%.

(O 213 a R$ 16,2/kg é custo de 29/01/2026 num produto que praticamente parou de vender; tratei como
desatualizado e não usei na faixa.)

| Tamanho | Peso | Custo | Preço | Margem | R$/L |
|---|---|---|---|---|---|
| P 10 L | 436,7 g | R$ 8,52 | R$ 15,72 | 45,8% | 1,61 |
| M 15 L | 514,8 g | R$ 10,04 | R$ 18,53 | 45,8% | 1,24 |
| G 20 L | 588,8 g | R$ 11,48 | R$ 21,20 | 45,8% | 1,05 |
| **Kit P+M+G** | 1.540 g | **R$ 30,04** | **R$ 55,45** | 45,8% | — |

O G a R$ 1,05/L entrega **valor por litro bem melhor que a organizadora 16 L de hoje** (R$ 1,40/L),
com dobra e empilhamento de bônus. A conta ainda não tem o custo de montagem das 5 peças, que roda nos
centros MONTAGEM (CODWCP 78, 79) e precisa de cronoanálise — **por isso trate a margem de 45,8%
como teto**, não como previsão.

### 10.2 O tamanho P: o problema encolheu, mas não desapareceu

O estudo estimava o P em 563 g e R$ 2,07/L, e concluía que ele não se venderia sozinho. Com o peso
real de 436,7 g, o P sai a **R$ 1,61/L** — contra R$ 1,40/L da organizadora rattan 16 L e R$ 1,21/L
da flat 10,35 L. Continua sendo o pior valor por litro da família (o fundo comum é 64% do seu
peso), mas agora está **dentro da faixa da categoria**, não fora dela.

Isso muda a estratégia de lançamento: o P pode ir sozinho à gôndola. O kit dos três a R$ 55,45
continua sendo o SKU mais interessante — e a casa já tem a prática (o Kit Potes Modulares 6 peças
fez 19.078 kits e R$ 449 mil em 12 meses) — mas deixou de ser necessidade.

### 10.3 Payback

| | |
|---|---|
| Investimento nacionalizado (premissa: R$ 5,45/USD, +30%) | R$ 812.041 |
| Margem de contribuição por kit P+M+G | R$ 25,41 |
| Volume assumido | 21.500 un/ano por tamanho |
| Contribuição anual | R$ 546.407 |
| **Payback** | **≈ 17,8 meses** |

O volume de 21.500/ano por tamanho é um terço do que a organizadora 16 L (069) vendeu em 12 meses
(64.606 peças) — quer dizer, o payback de 17,8 meses fecha se a família nova apenas empatar com
**um** produto da categoria, numa categoria que fatura R$ 20,2 milhões/ano. Se a família chegar ao
ritmo do 069 em cada litragem, cai para ~6 meses.

---

## 11. Riscos e o que confirmar antes do pedido

| Risco | Gravidade | Ação |
|---|---|---|
| Distância entre colunas da INJ 34 vs bloco de 620 × 540 mm | **Alta** | Medir em campo — `AD_INJETORAFICHA` está vazia (7.3) |
| Pressão específica de 0,32 t/cm² com valvulado | **Alta** | Confirmar com a MR Plastic Mould; a 0,40 t/cm² o fundo vai a 433 t e só cabe na INJ 34 |
| Fadiga da dobradiça pino/berço | **Alta** | Ensaio de 5.000 ciclos no try-out, em CP 141, antes de aprovar o 2º try-out |
| Câmbio e nacionalização do molde | Média | Substituir premissa por dado do fiscal (seção 9) |
| Custo de montagem das 5 peças | Média | Cronoanálise nos CODWCP 78/79 — a margem de 45,8% é teto |
| Capacidade de IML não confirmada | Baixa | `TPRWCP.AD_IML` nula nas 89 linhas — não prometer decoração no molde |
| Centros "NITRON" de até 1.100 t | Oportunidade | Confirmar existência: liberaria fundo com 2 cavidades (7.4) |
| Empilhamento carregado | Média | Definir carga de projeto e validar coluna de canto — a referência apoia na borda do painel |

---

## 12. Próximos passos

1. **Consolidar no projeto 100** (já aprovado) e encerrar 66, 112 e 73 como absorvidos — `AD_PROJETOS`.
2. **Medir a INJ 34** (distância entre colunas, altura de molde) e preencher `AD_INJETORAFICHA` para
   as 46 injetoras. É o único bloqueio que impede fechar o pedido do molde do fundo.
3. **Perguntar à produção sobre os centros NITRON 47–59**, em especial a 1.100 t.
4. **Cotar com a MR Plastic Mould** os 4 moldes + 6 jogos de inserto, pedindo separado o preço da
   câmara quente valvulada do fundo e exigindo **pinos de furo postiços** (539 shut-offs no G) e
   **orelhas de dobradiça escalonadas** no molde do fundo.
5. **Fechar o desenho** com o design: raio R15 no fundo e nas colunas de canto, painéis planos,
   ripado vertical ou textura da linha, chumbo + branco.
6. **Try-out do fundo primeiro**, isolado: é a peça que carrega dobradiça, berço de empilhamento,
   raio de canto e o maior risco de ferramental.
