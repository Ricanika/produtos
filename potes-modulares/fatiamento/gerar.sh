#!/bin/bash
# Reproduz todos os .gcode a partir dos STL. Ver AGENTE-Kobra3Max-PETG.md.
set -e
cd "$(dirname "$0")"
export QT_QPA_PLATFORM=offscreen
mkdir -p prep saida camadas

python3 preparar.py pecas.json

P="prusa-slicer --export-gcode --dont-arrange --load kobra3max_petg.ini"

# tampa: impressa de cabeca para baixo (flip em pecas.json). O rebaixo de
# empilhamento vira um teto de 113x86 mm -> --dont-support-bridges=0 e
# obrigatorio, senao o perfil recusa suporte e a tampa faz uma ponte de 86 mm.
$P --brim-width 8  --dont-support-bridges=0                  -o saida/1_tampa_q010.gcode   prep/tampa.stl
$P --brim-width 10                                           -o saida/2_pote600_q010.gcode prep/pote600_fundoplano.stl
$P --brim-width 8  --dont-support-bridges=0 --layer-height 0.2 -o saida/3_tampa_r020.gcode   prep/tampa.stl
$P --brim-width 10                          --layer-height 0.2 -o saida/4_pote600_r020.gcode prep/pote600_fundoplano.stl

python3 miniatura.py saida/1_tampa_q010.gcode   prep/tampa.stl
python3 miniatura.py saida/2_pote600_q010.gcode prep/pote600_fundoplano.stl
python3 miniatura.py saida/3_tampa_r020.gcode   prep/tampa.stl
python3 miniatura.py saida/4_pote600_r020.gcode prep/pote600_fundoplano.stl

python3 valida.py saida
python3 camada.py saida/1_tampa_q010.gcode   0.20 camadas/tampa_z020.png
python3 camada.py saida/2_pote600_q010.gcode 0.20 camadas/pote600_z020.png
