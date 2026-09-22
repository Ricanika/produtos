# Impressão 3D em PETG — Cesto Mini Organizador P

Fatiado com PrusaSlicer 2.7.2 a partir de `cad/cesto-aba.stl` (o mesmo sólido
do projeto, 200 × 250 × 130 mm, envelope real 204 × 241 × 132,5 mm).

Refatiado em 22/09 duas vezes: depois de fechar os dois furos do pé (chapa do
fundo inteira, parede cega até z = 40, bolsa cega sob o pé) e depois de pôr
**três faixas de listra** com rasgo de 6 × 18,3 mm. Todo `.gcode` desta pasta
é da peça atual. O tempo subiu ~50 min porque são 135 rasgos em vez de 65 —
mais perímetro para contornar.

| arquivo | bico | camada | filamento | tempo |
|---|---|---|---|---|
| `cesto-P-petg-anycubic.gcode` | 0,4 mm | 0,30 mm | **219 g** | **15 h 44 min** |
| `cesto-P-petg-bico04.gcode` | 0,4 mm | 0,30 mm | 219 g | 15 h 44 min |
| `cesto-P-petg-bico06.gcode` | 0,6 mm | 0,40 mm | 231 g | **8 h 39 min** |

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

## Anycubic Kobra 3 / S1 / 3 Max — `cesto-P-petg-anycubic.gcode`

**É este o arquivo para essas máquinas.** O erro que os `.gcode` genéricos dão:

> CODE 10133 — The file is missing necessary commands. *"If you don't use the
> recommended slicing software or the recommended parameters, or delete
> necessary commands such as Start G-code by mistake, the printer will report
> this error."* — wiki.anycubic.com/en/error-codes/10133-code

O comando que faltava é **`G9111`**, o macro de partida da própria Anycubic
(ele faz homing, aquecimento e nivelamento por dentro). A firmware valida o
arquivo antes de imprimir e recusa quem não o tem.

Não inventei o cabeçalho: peguei o start/end do **perfil de Anycubic do
OrcaSlicer**, que é mantido por quem conhece a máquina. Os três modelos novos
usam exatamente a mesma linha, e é por isso que **um arquivo serve nos três**:

| modelo | cama | flavor | start |
|---|---|---|---|
| Kobra 3 | 255 × 255 × 260 | klipper | `G9111 bedTemp= extruderTemp=` |
| Kobra S1 | 250 × 250 × 250 | klipper | idem |
| Kobra 3 Max | 426 × 420 × 501 | klipper | idem |

Fatiado na cama do **menor** dos três (S1, 250 × 250) e centrado nela, então
vale nos outros dois. O que mudou em relação ao perfil genérico:

- `gcode_flavor = klipper` (não Marlin)
- cama 250 × 250, peça centrada em (125, 125)
- `thumbnails = 230x110 PNG` — é a miniatura que aparece na tela da
  impressora. **Atenção:** o PrusaSlicer em linha de comando *não* desenha a
  miniatura (só a interface gráfica desenha), então o arquivo saiu sem ela. A
  miniatura foi gerada depois pelo `miniatura.py`, que desenha a peça a partir
  do STL e injeta o bloco `thumbnail begin/end` (PNG em base64, o mesmo
  formato que o OrcaSlicer escreve) no cabeçalho
- brim de 4 para **2 mm**: a peça tem 241 mm em y e sobram só 4,8 mm de folga
- `M900` (pressure advance) **omitido de propósito**: está no perfil da Kobra 3
  mas não no da S1, e um valor errado estraga o canto
- sem purga manual e sem `G28` no start — quem faz isso é o `G9111`

Conferido no arquivo gerado: `G9111 bedTemp=80 extruderTemp=245` na linha 189
(logo depois da miniatura), miniatura de 230 × 110 conferida byte a byte
(cabeçalho PNG válido, dimensões reais 230 × 110, tamanho declarado igual ao
real), E relativo com `G92 E0` por camada, suporte só entre z 0,3 e 4,9 mm,
tudo dentro de 250 × 250 × 250 (x 10…227, y 4,8…245, z até 132,8) e só
comandos que o Klipper conhece — G1/G21/G90/G91/G92 e
M83/M84/M104/M106/M107/M109/M117/M140/M190/M400. Nenhum M205, M900 ou M420.

**O que eu não pude testar:** a máquina. Se o 10133 insistir, o conserto
determinístico é você me mandar **qualquer** gcode que a sua impressora aceite
(uma peça de teste fatiada no Anycubic Slicer Next serve) — eu transplanto o
cabeçalho exato dela e devolvo o arquivo.

## Os outros `.gcode` desta pasta

Os `cesto-P-petg-bico04/06.gcode` saíram com perfil **Marlin genérico** e
cama de 300 × 300: servem para Prusa, Ender, Bambu e afins, e **não** para as
Anycubic novas, que recusam o arquivo com:

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
