#!/bin/bash
# Reproduz todos os .gcode a partir dos STL. Ver AGENTE-Kobra3Max-PETG.md.
set -e
cd "$(dirname "$0")"
export QT_QPA_PLATFORM=offscreen
mkdir -p prep saida camadas

python3 preparar.py pecas.json

P="prusa-slicer --export-gcode --dont-arrange --load kobra3max_petg.ini"

# tampa PP: IMPRIME INVERTIDA (flip em pecas.json). De pe apoiaria so na ponta
# das 2 travas - 0 mm2. Invertida, o deck vai na mesa: 3.183 mm2.
# --dont-support-bridges=0 e obrigatorio: sem ele o perfil recusa suporte sob o
# poco da bandeja e o fatiamento sai sem erro, com uma ponte livre no meio.
# --support-material-buildplate-only=0 tambem: com o padrao (=1) o suporte so
# sobe da mesa e para em z=3,3, e a prateleira do gancho - 1,1 mm de balanco em
# 89 mm, a 11,5 mm de altura - sai no ar. Custa 2,8 g e 13 min, e e justamente
# a feicao que o prototipo existe para provar.
$P --brim-width 8  --dont-support-bridges=0 --support-material-buildplate-only=0 --layer-height 0.2 -o saida/1_tampa_pp.gcode   prep/tampa_pp.stl
# a placa de teca e macica: em PETG a 100% daria 111 g e 12 h. Ela so serve para
# conferir encaixe - em producao e CNC em madeira. 15% de preenchimento basta.
$P --brim-width 8 --fill-density=15% --layer-height 0.2 -o saida/2_tampa_teca.gcode prep/tampa_teca.stl
$P --brim-width 10                          --layer-height 0.2 -o saida/3_pote600.gcode    prep/pote600_fundoplano.stl
$P --brim-width 10 --dont-support-bridges=0 --layer-height 0.1 -o saida/4_pote600_q010.gcode prep/pote600_fundoplano.stl

for f in 1_tampa_pp 2_tampa_teca 3_pote600 4_pote600_q010; do
  case $f in
    1_tampa_pp)  src=prep/tampa_pp.stl ;;
    2_tampa_teca) src=prep/tampa_teca.stl ;;
    *)           src=prep/pote600_fundoplano.stl ;;
  esac
  python3 miniatura.py saida/$f.gcode $src
done

python3 valida.py saida
python3 camada.py saida/1_tampa_pp.gcode 0.20 camadas/tampa_pp_z020.png
python3 camada.py saida/3_pote600.gcode  0.20 camadas/pote600_z020.png
