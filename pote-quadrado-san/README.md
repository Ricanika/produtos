# Pote quadrado modular em SAN, revisão 1

Produto novo, injetado na Nitron. É separado da linha `potes-modulares/` (PP, retangular, parede reta).
Daquele estudo aproveitamos o parque de injetoras e o cadastro do TPE.

## O pedido

- Corpo em **SAN** (Sangel), tampa em **PP**, vedação em **TPE**.
- **Quatro alturas com a mesma boca**, para ter um tamanho de tampa só.
- **O mais quadrado possível**, mas os potes têm de **entrar um no outro** para dar cubagem no
  transporte. A ideia era um trapézio.
- **Tampa hermética** com uma **fita de TPE de ~2 × 10 mm** envolvendo a lateral da tampa, numa cava.
  Não é o anel padrão de mercado.
- **Três tampas:** fechada, de **teca** com a mesma borracha, e com **bico + copo** que fecha o bico.

## Como ficou

| | |
|---|---|
| Forma | tronco de pirâmide quadrada, **3° de saída por face**, canto R10 por fora (R8 por dentro) |
| Boca | **124 × 124 mm** por dentro, igual nos quatro; medida máxima **133,8 mm** na borda |
| Alturas | **57 · 114 · 171 · 228 mm** (1, 2, 3 e 4 módulos) |
| Parede / fundo | 2,0 mm / 2,2 mm de SAN |
| Pé | anel de 95,2 mm × 3 mm, **o mesmo nos quatro** |
| Borda | saia livre pendurada para fora, com canal aberto para baixo. Sem contra-saída |

| Corpo | Capacidade na borda | Útil, tampa fechada | Fundo externo | Massa SAN | Resina (R$ 14/kg) |
|---|---|---|---|---|---|
| 57 mm | 759 ml | 706 ml | 122,0 mm | 98,7 g | R$ 1,38 |
| 114 mm | 1.518 ml | 1.465 ml | 116,1 mm | 152,1 g | R$ 2,13 |
| 171 mm | 2.200 ml | 2.147 ml | 110,1 mm | 202,6 g | R$ 2,84 |
| 228 mm | 2.809 ml | 2.756 ml | 104,1 mm | 250,4 g | R$ 3,51 |

Como nome comercial cabe 700 ml / 1,4 L / 2,1 L / 2,7 L pela capacidade útil, ou 750 ml / 1,5 L /
2,2 L / 2,8 L pela borda. A decisão é sua.

### Por que 3°

É a saída que deixa os potes aninharem sem deixar o pote alto com cara de balde. O passo de aninhar
é `(parede + nervura) / tan(saída)`:

| Saída | Passo aninhado | Fundo do pote de 228 |
|---|---|---|
| 2° | 74,5 mm | 112,1 mm |
| **3°** | **49,6 mm** | **104,1 mm** |
| 4° | 37,2 mm | 96,1 mm |
| 5° | 29,7 mm | 88,1 mm |

Como a boca e a saída são iguais nos quatro, **o passo é o mesmo para qualquer combinação**: o 114
entra no 228 do mesmo jeito que o 228 entra no 228.

| 12 potes vazios | Soltos | Aninhados | Ganho |
|---|---|---|---|
| 57 mm | 684 mm | 603 mm | 12% |
| 114 mm | 1.368 mm | 660 mm | 52% |
| 171 mm | 2.052 mm | 717 mm | 65% |
| 228 mm | 2.736 mm | 774 mm | 72% |

O pote de 57 quase não ganha, porque a altura dele é praticamente o passo. Isso é geometria, não
detalhe de projeto: para ele aninhar bem a saída teria de ir para uns 5°.

**Nervuras anti-travamento:** quatro nervuras de 0,6 × 4 mm no meio de cada lado, por dentro,
começando 20 mm abaixo da borda (fora da zona da fita). Elas param o pote de dentro antes de a
parede encostar. SAN contra SAN, parede com parede, gruda por atrito e por vácuo; com as nervuras
o contato fica em quatro linhas e o ar entra pelos lados. Estão no macho, então não criam
contra-saída.

### Empilhar na mesma altura

O pé de cada pote cai num **bolsão de 3 mm** no tampo da tampa, e a aba da tampa tem exatamente
3 mm acima da borda. Então **a tampa não soma altura na pilha**: 57 + 57 + 114 = 228 + tampa.
Isso vale para a fechada e para a de teca. A de bico não empilha.

## A vedação: fita de TPE 2 × 10 na lateral

Ver o corte 2D na página do modelo.

- O **plug** da tampa desce 16 mm dentro da boca, com a mesma saída de 3° da parede.
- Na lateral do plug há uma **cava de 10,4 × 1,62 mm**. A fita de **2,0 × 10 mm** calça nela,
  esticada uns 3% para não sair na lavagem.
- A fita sobressai **0,38 mm** da face do plug, a folga até a parede é **0,25 mm**: sobram
  **0,13 mm de compressão (6,5%)**.
- **A vedação é radial:** a fita aperta a parede lateral do corpo. O topo da borda só serve de
  batente. Não precisa de trava, e o SAN, que é quebradiço, não tem nenhum engate.
- **O cone ajuda a fechar:** a fita só toca a parede nos **últimos 2,5 mm** de curso. Até ali o ar
  sai pela folga, então não há colchão de ar a vencer. No fim fica o "pop" de tampa hermética.
- **Aperto baixo de propósito.** Uma fita larga e fina, presa entre duas paredes, fica muito rígida
  na compressão (fator de forma 2,5). Quem dá a mola é a saia de PP, e mesmo assim cada décimo de
  milímetro conta. Começamos com 0,13 mm e **ajustamos a profundidade da cava no try-out**. Tirar
  aço da cava é barato; pôr aço de volta não.
- **Abrir:** a orelha num canto da tampa serve para descascar. Puxar reto com a tampa inteira vai
  precisar de mais força. Só o protótipo dá esse número com confiança.

## As três tampas

| Tampa | Material | Massa | Notas |
|---|---|---|---|
| **Fechada** | PP RP 141 | 51,3 g | orelha de abrir; bolsão de empilhar no tampo |
| **Teca** | teca maciça, CNC | 76,6 g | a mesma cava e a mesma fita; escavada por baixo (5 mm de madeira no centro e na lateral); aba de 3 mm sobre a borda |
| **Bico** | PP RP 141 | 52,5 g | laje plana; bico redondo Ø38 × 25 mm deslocado 30 mm para um lado (lado de verter); cordão de encaixe |
| **Copo dosador** | PP RP 141 | 7,6 g | ~25 ml; encaixa no cordão do bico (0,35 mm) e veda com um anel-plug que entra 4 mm no furo com 0,2 mm de aperto |
| **Fita** | TPE Karinprene 45 | 9,4 g | 2 × 10 mm, perímetro ~470 mm |

A fechada e a de bico podem sair do **mesmo molde com postiço trocável** no tampo.

## Fabricação

- **SAN:** contração de 0,4–0,6% (o PP fica em 1,5–2%), então **os moldes de PP da casa não servem
  para estes corpos**. É higroscópico: **secar 2–3 h a ~80 °C** antes de injetar. É rígido,
  transparente e quebradiço, e por isso o corpo não tem trava, clipe nem dobradiça.
- **Corpo sem contra-saída:** o canal da borda abre para baixo (lâmina na cavidade), a saia afina
  para baixo, e as nervuras ficam no macho.
- **Tampa de PP:** a cava é **contra-saída externa de 1,62 mm** na saia. O plug não pode flexionar
  para dentro porque o macho está lá, então são **4 gavetas** (uma por lado). É o item caro do
  molde da tampa. A alternativa é extração em dois estágios com a saia sendo arrancada, e isso
  precisa de estudo com a ferramentaria.
- **Fita:** perfil extrudado 2 × 10, cortado e soldado em anel, ou injetado em anel. O Karinprene 45
  (CODPROD 997) está cadastrado, mas **não tem compra nos últimos 24 meses**: recotar.
- **Teca:** CNC na planta WOOD. A madeira trabalha com a umidade. Usar painel colado (finger-joint)
  ou corte radial, e acabamento selado para alimento.

### Injetoras (pelo parque levantado no estudo `potes-modulares/`)

Área projetada do corpo ≈ 179 cm². Com 2 cavidades, quem decide a máquina é a profundidade (curso de
abertura), não o fechamento.

| Corpo | Classe provável | Observação |
|---|---|---|
| 57 | 200 t | |
| 114 | 200 t | |
| 171 | 250 t | |
| 228 | 380 t (INJ 31–33) | o mais fundo; mesma classe do modular 2,4 L que já roda |
| Tampa (4 gavetas) | 200–250 t | o molde fica maior por causa das gavetas |
| Copo | 80–120 t | multicavidade |

## Resina

- **SANGEL STANDARD CRISTAL GRANULADO, CODPROD 16811.** Só houve uma compra: **25 kg a R$ 14,00/kg,
  Polibalbino, set/2026** (lote de amostra). O preço da tabela é ordem de grandeza, não cotação.
- **PP RP 141** para tampa e copo: R$ 9,54/kg (compra corrente).

## Em aberto

1. **Protótipo da vedação.** A compressão de 0,13 mm é o ponto de partida. Ensaio com água colorida,
   24 h, deitado e de cabeça para baixo, e medir a força para abrir pela orelha.
2. **Tampa de teca:** a aba de 3 mm de madeira sobre a borda é frágil na quina. Se lascar no
   protótipo, a teca sobe para 5 mm e deixa de ser modular, ou a aba vira um aro de PP.
3. **Teca e umidade:** ±0,5% de variação dimensional já come a compressão inteira da fita.
4. **Nome comercial** (capacidade útil ou na borda).
5. **Pote de 57 no frete:** aceitar os 12% ou subir a saída.
6. **Cotar SAN em volume** e confirmar o grade com o fornecedor (transparência, resistência a
   lava-louças).
7. **Ferramentaria:** gavetas da cava × extração em dois estágios.

## Arquivos

| Arquivo | O que é |
|---|---|
| `geometria.py` | gerador paramétrico: todas as cotas no topo, STL, relatório e verificações |
| `gera-visualizador.py` | monta `visualizador-3d.html` a partir das malhas e do corte 2D |
| `visualizador-modelo.html` | o molde da página (as malhas entram no lugar de `__DADOS__`) |
| `visualizador-3d.html` | a página publicada |
| `stl/` | 9 peças em mm, Z para cima. Tampa, fita e copo com z=0 no topo da borda |
| `relatorio.json` | massas, capacidades, aninhamento e vedação, gerados |

```
python3 geometria.py            # STL + relatorio + malhas
python3 geometria.py --teste    # so as verificacoes
python3 gera-visualizador.py    # a pagina
```

**As verificações que rodam a cada geração:** folga no canto igual à folga no lado (com
**autoteste**: a mesma conta, com raio fixo, tem de reprovar), compressão da fita dentro da faixa,
cava mais larga que a fita, alturas somando, pé cabendo no bolsão e no fundo do pote mais alto,
passo de aninhar vindo da nervura, nervura fora da zona da fita, bico longe da saia, cordão do copo
engatando, e a malha de cada peça fechada (toda aresta usada duas vezes, uma em cada sentido).

É malha para visualizar e imprimir protótipo. Não é o CAD do molde: o projetista do molde refaz em
sólido paramétrico a partir destas cotas.
