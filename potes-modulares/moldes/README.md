# Moldes — conceito gerado

`gera-molde.py` lê o mesmo paramétrico que gera a peça (`../gera-3d.py`), aplica
**contração** e escreve o conceito de molde dos quatro corpos.

```bash
python3 gera-molde.py                        # contração 1,5%, 2 cavidades
python3 gera-molde.py --contracao 1.8 --cav 4 --seg 24
```

## O que sai

| Arquivo | O que é |
|---|---|
| `stl/<tam>/cavidade.stl` | postiço de cavidade — a bolsa que forma o lado de fora, com o ressalto do rebaixo de fundo |
| `stl/<tam>/macho.stl` | postiço de macho — parte formadora + haste que atravessa a impulsora + flange de fixação |
| `stl/<tam>/placa-impulsora.stl` | placa com o rasgo da boca; a face de baixo empurra a aba da peça |
| `stl/<tam>/refrigeracao.stl` | circuitos como corpos separados, para ver e conferir |
| `desenhos/molde-<tam>.svg` | corte do conjunto em escala, com gate, plano de fechamento e água |
| `ficha-molde-<tam>.md` | fechamento, injeção, postiços, porta-molde, curso, água, ciclo |

## Como o molde foi concebido

**Duas placas, câmara quente valvulada, extração por placa impulsora.** A peça
fica **de boca para baixo**: o plano de fechamento é o plano da aba da borda, a
cavidade (lado fixo) forma todo o lado de fora e o bico quente entra no centro do
fundo, que é o ponto mais alto do molde fechado. O macho fica no lado móvel — a
peça contrai em cima dele e vai junto na abertura. A placa impulsora empurra a
aba e descasca a peça do macho.

Isso resolve o canal em U da borda sem gaveta: o U abre para baixo e o degrau de
aço que o forma é parte da parede da bolsa. Extração puramente em +z.

## Conferências que o gerador faz sozinho

1. **Malha fechada e normais consistentes** nas 12 peças de aço.
2. **O vazio entre cavidade e macho tem que ser a peça × (1+contração)³** — dentro
   de 0,5%. É o teste que pega erro de cota: quando o ressalto do rebaixo de fundo
   ficou faltando na primeira versão, esta conferência acusou +3,3% de volume
   (o pote sairia com fundo chato e ~3% de litragem a mais).

## Os números que saíram (contração 1,5%, 2 cavidades)

| | 600 ml | 1,2 L | 1,8 L | 2,4 L |
|---|---|---|---|---|
| Postiço de cavidade | 212 × 151 × 98 | × 159 | × 220 | 212 × 151 × 281 |
| Aço do postiço de cavidade | 2,45 L | 3,73 L | 5,01 L | 6,29 L |
| Fechamento (2 cav) | 119 tf | 119 tf | 119 tf | 119 tf |
| Altura de molde | 420 mm | 542 mm | 663 mm | 785 mm |
| Abertura mínima | 211 mm | 333 mm | 454 mm | 576 mm |
| **Espaço entre platôs** | **631 mm** | **874 mm** | **1.118 mm** | **1.362 mm** |

**O achado:** a área projetada é a mesma nos quatro potes (o footprint não muda),
então **o fechamento é idêntico nos quatro — 119 tf**. Quem escolhe a injetora
nesta linha **não é a tonelagem, é o espaço entre platôs**: 631 mm no 600 ml
contra 1.362 mm no 2,4 L. É por isso que o 2,4 L cai numa 380 t e não numa 150 t,
e é a razão técnica para a pendência de `AD_INJETORAFICHA` (`CURSOABERT`,
`ALTMINMOLDE`, `ALTMAXMOLDE`) deixar de ser cadastro e virar bloqueio de projeto.

## O que este conceito NÃO é

Não é projeto executivo, e cada ficha traz a lista do que falta. O resumo:
contração por direção e por tamanho (aqui é linear e igual nos quatro, o que a
seção 12.1 do [agente de moldes](../../agentes/AGENTE-Projetista-de-Moldes.md)
já aponta como errado), porta-molde normalizado real com código de catálogo,
câmara quente especificada por modelo, respiros, detalhamento 2D com tolerâncias
e cotas steel safe, aço e tratamento por componente, Moldflow e plano de try-out.

**É malha, não sólido CAD** — mesma ressalva do gerador da peça.
