# Base Modular Rattan G

**Status:** estudo de produto · **Revisão 1** · 23/09/2026
**Serve:** 069.006.003 (Rattan G, 38,5 × 28 × 19,0 cm) e 261.006.003 (Rattan G Baixo, 38,5 × 28 × 8,3 cm)

Gaveteiro empilhável: cada módulo recebe um cesto, que entra pela frente como gaveta. **Três peças, três moldes:**

| Peça | Serve | Peso | Resina (PP CP 141 a R$ 10,51/kg) | Injetora |
|---|---|---|---|---|
| Módulo alto | 069.006.003 | 693 g | R$ 7,28 | 380 t: INJ 31, 32, 33 |
| Módulo baixo | 261.006.003 | 580 g | R$ 6,09 | 380 t: INJ 31, 32, 33 |
| Tampo | fecha a torre | 387 g | R$ 4,07 | 600 t: INJ 34 (a 380 t depende de Moldflow) |

Página publicada, com o 3D para montar a torre: https://claude.ai/artifact/6T3wh7od7kxZ3uwmojPYph

---

## 1. As regras que fecham o produto

1. **Uma planta só.** Os dois módulos e o tampo medem **336 × 395 mm** e usam o mesmo encaixe: um pino de Ø 12 no topo
   de cada montante entra na guia de baixo da peça seguinte, com 0,3 mm de folga. Qualquer módulo vai em cima de qualquer
   outro, e o tampo vai em cima dos dois.
2. **Passo 220 / 110 mm, ou seja, dois baixos dão um alto.** Duas torres lado a lado ficam alinhadas.
3. **O teto de cada módulo é o piso do módulo de cima.** O módulo é um U: piso mais duas laterais, aberto na frente, atrás e
   em cima. Por isso o molde abre em Z, e o tampo existe só para fechar o último.
4. **Nenhuma gaveta nos três moldes.** A janela lateral é o único furo em parede vertical. Ela sai do molde porque a lateral
   é feita em degrau (seção 2).

## 2. A janela lateral sem gaveta

Corte da lateral direita, de dentro para fora:

```
x 146,0 -> 149,0   PEITORIL   parede de 3 mm que sobe 30 mm do piso. Feito pelo MACHO, que vem de cima.
x 149,0 -> 168,0   RASGO      o piso termina no peitoril. Daqui para fora, está aberto até embaixo.
x 156,4 -> 168,0   TRAVESSA   U invertido no alto. Feita pela CAVIDADE, que sobe pelo rasgo.
```

Em planta, o peitoril e a travessa não se sobrepõem. Dentro da janela, o macho e a cavidade se encontram num plano inclinado
que vai do topo do peitoril até a base da travessa. **O recuo de 7,4 mm dá 3,0° de fechamento** nos 142 mm de janela do
módulo alto, que é a mais alta. No módulo baixo o mesmo recuo dá 10,0°. `x_trav()` em `geometria.py` calcula o recuo a
partir do ângulo.

Custo do desenho: o rasgo corta a ligação direta entre o piso e a lateral. Quem leva a carga do piso até os montantes
passa a ser o peitoril, que funciona como viga.

## 3. O cesto cabe e sai

| Módulo | Vão livre (mm) | Folga lado | Folga fundo | Folga topo | Flecha do piso* |
|---|---|---|---|---|---|
| Alto | 292 × 389 × 202 | 6,0 | 4,0 | 12,0 | 4,5 mm com 8 kg |
| Baixo | 292 × 389 × 92 | 6,0 | 4,0 | 9,0 | 2,3 mm com 4 kg |

\*Flecha com o módulo de fluência a 1.000 h (400 MPa), piso tratado como biapoiado e sem contar as nervuras longitudinais.
É um limite conservador.

Um **batente de 4 mm** na frente segura o cesto. Para tirar, levanta-se o cesto 4 mm, e por isso a folga de topo tem de cobrir
o batente mais a flecha do piso de cima.

**Erro pego pela conta, não pelo desenho:** a primeira geometria tinha piso de 14 mm e passos de 208/104. Dava 12 mm de flecha
para 4 mm de folga: o piso de cima encostaria no cesto de baixo, e o cesto não passaria pelo batente. A correção foi pôr uma
nervura sob cada barra cheia do piso (a cada 20 mm, com 15,8 mm de altura), subir o peitoril para 30 mm e passar os passos
para 220/110.

## 4. Injeção

- **Área projetada dos módulos: 847 cm².** Os oblongos do piso ocupam 38% do vão. Sem eles o módulo passaria de 1.100 cm²
  e sairia da classe de 380 t. A 300 bar, com 15% de margem, dá **298 t**.
- **Tampo: 1.327 cm² de superfície cheia.** Com dois pontos de câmara quente (220 bar) dá **342 t**, 90% de uma 380 t.
  Recomendação: INJ 34 (600 t), que já roda o corpo do 069. Para ir para a 380 t, só com Moldflow.
- **Referência que já roda:** o corpo 069-C (385 × 280 mm, 392 g) vai nas INJ 33 (380 t) e 34 (600 t).
- **Ferramental, em ordem de grandeza: USD 74–92 mil** para os três moldes (1 cavidade, câmara quente, sem gaveta). A base
  é o molde 283-C, de 380 t e 72 × 77 × 69 cm, aprovado por USD 36.900 com a MR Plastic Mould. Os moldes daqui são menores.
- Os ciclos (38 / 32 / 30 s) são **estimados**. Não há ficha técnica do 069-C em `AD_FICHATECNICA`.

## 5. Decisões em aberto

1. **Os 19,0 cm do 069 incluem a tampa do cesto?** No cadastro, o 069 é corpo 069-C mais tampa 069-T. Se a medida inclui a
   tampa, o cesto entra na gaveta sem ela, sobra folga e o passo alto pode cair. Medir uma peça da linha.
2. **Onde injetar o tampo:** INJ 34 ou Moldflow para a 380 t.
3. **Rigidez do piso:** imprimir o módulo baixo em FDM, que cabe na Kobra 3 Max, e medir com carga por uma semana.
4. **Cor:** sugestão de cinza chumbo com o master Cool Gray 7031, já usado no 069-C.
5. **Torres acima de 1,1 m:** prever furo para cinta de parede no tampo.

## 6. Arquivos

| Arquivo | O que é |
|---|---|
| `geometria.py` | cotas e as três peças como listas de caixas e tubos. Volume e área projetada saem da **união** dos sólidos, nunca da soma |
| `calculo.py` | memória de cálculo: folgas, fechamento da janela, peso, injetora, flecha, montante, torres. `--json dados.json` exporta |
| `gera-3d.py` | gera `stl/*.stl` e `pecas.json`. O STL é para **visualizar** (caixas sobrepostas, não é união booleana) |
| `monta-pagina.py` + `pagina.tpl.html` | montam `base-modular.html`, a página publicada. Nenhum número dela é digitado à mão |

Para regenerar tudo:

```
python3 gera-3d.py && python3 calculo.py --json dados.json && python3 monta-pagina.py
```

**A malha é de estudo, não o CAD do molde.** As faces verticais estão sem saída. O projetista parte destas cotas e aplica
1° de saída nas faces verticais.

## 7. Fontes (Sankhya via MCP Nitron, somente leitura, 23/09/2026)

- `TGFPRO`: CODPROD 347 (069.006.003, PRETA 16 L) e 1854 (261.006.003, PRETA 7 L), com medidas e pesos.
- `TGFICP`: corpo 069-C (CODPROD 642) em PP CP 141 (CODPROD 994) mais 2% de master.
- `TGFITE`/`TGFCAB`: PP CP 141 a **R$ 10,51/kg**, 109 t compradas em 12 meses, última compra em 17/09/2026. Vendas de
  12 meses: família 069 com **65.302 un / R$ 1,45 mi**, família 261 com **19.305 un / R$ 350 mil**.
- `TPRAPA → TPRAPO → TPRIATV → TPRWCP/TPRCAP`: onde roda o 069-C.
- `AD_MOLDE`/`AD_ORCAMENTO`: 283-C (USD 36.900, 380 t), 284-U (USD 20.100, 280 t), 214-U (USD 18.900, 250 t).
