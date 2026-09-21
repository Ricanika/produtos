# Impressão 3D em PETG — Cesto Mini Organizador P

Fatiado com PrusaSlicer 2.7.2 a partir de `cad/cesto-aba.stl` (o mesmo sólido
do projeto, 200 × 250 × 130 mm, envelope real 204 × 241 × 132,5 mm).

| arquivo | bico | camada | filamento | tempo |
|---|---|---|---|---|
| `cesto-P-petg-bico04.gcode` | 0,4 mm | 0,30 mm | **207 g** | **14 h 32 min** |
| `cesto-P-petg-bico06.gcode` | 0,6 mm | 0,40 mm | 219 g | **8 h 04 min** |

**Para imprimir você usa UM arquivo só: o `.gcode` do seu bico.** Os dois são
a mesma peça, fatiada de dois jeitos — escolha pelo bico que está na máquina.
Os `perfil-*.ini` não vão para a impressora: são a receita, para carregar no
PrusaSlicer (`File → Import → Import Config`) e refatiar se a sua cama ou a
sua máquina forem diferentes.

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

## Se a impressora for Anycubic (erro 10133)

**Não use os `.gcode` desta pasta.** Eles saíram do PrusaSlicer com um perfil
Marlin genérico, e as Anycubic novas (Kobra 3 / 3 Max / 3 Combo / S1 / X)
**validam o arquivo** e recusam o que não veio do Anycubic Slicer Next:

> CODE 10133 — The file is missing necessary commands, which may cause
> printing errors. *"If you don't use the recommended slicing software or the
> recommended parameters, or delete necessary commands such as Start G-code by
> mistake, the printer will report this error."*
> — wiki.anycubic.com/en/error-codes/10133-code

Não dá para consertar remendando o cabeçalho: a firmware é Klipper e o start
correto chama macros da própria máquina. Um cabeçalho forjado pode ser aceito
e a impressora partir **sem homing e sem aquecer** — pior que o erro.

O caminho é fatiar o `cad/cesto-aba.stl` no **Anycubic Slicer Next**, com o
perfil da máquina, e reproduzir lá os parâmetros abaixo.

| parâmetro | valor | por quê |
|---|---|---|
| material | PETG · 240 °C · mesa 80 °C | 245 na 1ª camada |
| altura de camada | 0,30 mm (bico 0,4) | 0,40 se o bico for 0,6 |
| paredes | 3 perímetros | a parede do CAD tem 1,4 mm |
| preenchimento | 100% | só as regiões grossas (rim 3,2 mm, saia 4 mm) |
| topo / fundo | 4 camadas | a chapa do fundo tem 2 mm |
| brim | **2 mm, só externo** | ver cama, abaixo |
| ventoinha | 40–60%, desligada nas 3 primeiras | PETG |
| perímetro externo | 25 mm/s | PETG |

**Suporte — é o ponto que mais importa.** A chapa do fundo fica 5 mm acima do
piso, então esse vão de 145 × 195 mm precisa de suporte. Mas o suporte
automático quer encher o cesto inteiro de torre: medido no PrusaSlicer, **260 g
de suporte para 196 g de peça**, e 16 h a mais. Ligue suporte **"apenas na
mesa" (on build plate only)** e confira a pré-visualização: se aparecer torre
DENTRO do cesto, use um *support blocker* cobrindo o interior acima de z = 6 mm.
O suporte certo é uma laje de 5 mm embaixo da chapa e nada mais.

**A cama.** A peça é 204 × 241 mm:

| modelo | cabe? | sobra |
|---|---|---|
| Kobra 3 / S1 (250 × 250) | cabe | 46 mm em x, **9,1 mm em y** |
| Kobra 3 Max (420 × 420) | cabe folgado | — |
| Kobra 2 / Neo (220 × 220) | **não cabe** | faltam 21 mm em y |

Nos 250 × 250 sobram só 4,5 mm de cada lado em y — por isso brim de 2 mm e
skirt desligado. Girar não resolve (a cama é quadrada) e girar 45° piora.
