# Impressão 3D em PETG — Cesto Mini Organizador P

Fatiado com PrusaSlicer 2.7.2 a partir de `cad/cesto-aba.stl` (o mesmo sólido
do projeto, 200 × 250 × 130 mm, envelope real 204 × 241 × 132,5 mm).

| arquivo | bico | camada | filamento | tempo |
|---|---|---|---|---|
| `cesto-P-petg.gcode` | 0,4 mm | 0,30 mm | **207 g** | **14 h 32 min** |
| `cesto-P-petg-bico06.gcode` | 0,6 mm | 0,40 mm | 219 g | **8 h 04 min** |

Os `.ini` do lado são os perfis completos: carregue no PrusaSlicer
(`File → Import → Import Config`) e refatie para a sua máquina em um clique.

## ANTES DE IMPRIMIR — três coisas

**1. A cama tem de ter 210 × 250 mm de área útil.** O perfil está para
300 × 300 mm e a peça vai centrada em (150, 150), ocupando x 48…252 e
y 30…270. Se a sua cama for menor:

- **250 × 210** (Prusa MK4): cabe **girando 90°** — `prusa-slicer --rotate 90`,
  ou no GUI a peça entra rotacionada.
- **256 × 256** (Bambu X1/P1): cabe direto.
- **220 × 220** (Ender 3): **não cabe**. 241 mm de comprimento não entram nem
  girando.

**2. O suporte é obrigatório, e são só 5 mm.** A chapa do fundo fica 5 mm
acima do piso (a peça apoia nos pés, não na parede), então esses 5 mm são um
vão de 145 × 195 mm — nenhuma ponte fecha isso. O perfil desliga o suporte
**automático** e força suporte só nas primeiras camadas (18 a 0,3 mm / 14 a
0,4 mm). Isso importa: com o automático ligado, mesmo em "buildplate only", o
PrusaSlicer enchia o cesto inteiro de torre — medido, **260 g de suporte para
196 g de peça**, e 16 h a mais.

**3. E relativo.** O `start_gcode` manda `M83` e o perfil tem
`use_relative_e_distances = 1` + `layer_gcode = G92 E0`. Se você trocar o
start por um da sua impressora que **não** mande M83, tire também o
`use_relative_e_distances` — senão a extrusão sai errada na primeira linha.

## O que a impressão NÃO vai reproduzir

- **A face de baixo da aba** vai cair um pouco. A aba é um degrau de 7 mm para
  dentro, sem apoio embaixo, e não vale a pena erguer 120 mm de torre dentro
  do cesto para salvar uma face que não é funcional. A face de CIMA da aba —
  que é onde os pés pousam — sai plana.
- **As folgas do acoplamento (0,2 mm por face) e do friso (0,3 mm) estão
  abaixo da resolução de FDM.** No protótipo a cauda de andorinha vai entrar
  justa ou precisar de uma lixada. Elas são cotas de molde, não de impressão.
- **A parede de 1,4 mm** sai em 3 perímetros (bico 0,4) ou 2 (bico 0,6). Com
  0,6 ela sai exata: 2 × 0,70 = 1,40 mm.

## PETG — o que está no perfil

240 °C (245 na primeira camada), mesa a 80 °C, ventoinha 40–60% e desligada
nas 3 primeiras camadas, retração de 2 mm com wipe, perímetro externo a
25 mm/s. Brim de 4 mm: numa peça de 250 mm de comprimento a aderência da
primeira camada é o que decide o resultado.

`filament_cost = 120` R$/kg é palpite — troque pelo seu e o PrusaSlicer
recalcula (hoje dá R$ 24,79 por peça no bico 0,4).
