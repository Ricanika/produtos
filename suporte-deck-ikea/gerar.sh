#!/bin/bash
# STL -> prep -> gcode -> miniatura -> validacao -> desenho de camada.
# Reusa o perfil e os scripts de ../potes-modulares/fatiamento (Kobra 3 Max, PETG).
set -e
cd "$(dirname "$0")"
export QT_QPA_PLATFORM=offscreen
F=../potes-modulares/fatiamento
mkdir -p prep saida camadas

# o STL vem com a espessura (15 mm) em Y; preparar.py poe Y em Z com a face -Y
# na mesa: os pes (2.530 mm2) apoiam, a grelha fica 3,4-5,3 mm acima.
python3 $F/preparar.py pecas.json

# --dont-support-bridges=0 e obrigatorio: a parte de baixo da grelha e toda ponte
# entre pes; com o padrao do perfil (=1) ela sai sem suporte, em fio solto.
prusa-slicer --export-gcode --dont-arrange --load $F/kobra3max_petg.ini \
  --brim-width 8 --dont-support-bridges=0 --layer-height 0.2 \
  -o saida/suporte_deck_r020.gcode prep/suporte_deck.stl

python3 $F/miniatura.py saida/suporte_deck_r020.gcode prep/suporte_deck.stl
python3 $F/valida.py saida
python3 $F/camada.py saida/suporte_deck_r020.gcode 0.20 camadas/z020.png
