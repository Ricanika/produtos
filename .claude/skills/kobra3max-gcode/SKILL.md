---
name: kobra3max-gcode
description: Converte um modelo 3D (.stl ou .3mf) em G-code pronto para a impressora Anycubic Kobra 3 Max (bico 0,4), no formato do Anycubic Slicer Next, para evitar o erro CODE 10133 ("arquivo faltando comandos obrigatórios"). Use quando o usuário pedir para fatiar, gerar .gcode ou "transformar STL em gcode" para a Kobra 3 Max, ou mandar um STL para imprimir nela. Filamentos: PETG (padrão, Creality CR-PETG) e PLA.
---

# STL → G-code para Anycubic Kobra 3 Max

A impressora do usuário é uma **Anycubic Kobra 3 Max** (mesa 420×420×500 mm,
firmware V2.5.2.8, Klipper da Anycubic). O filamento padrão é **Creality CR-PETG
1,75 mm (230–250 °C)**.

## Por que existe

Arquivos do PrusaSlicer, Cura etc. são recusados pela Kobra 3 Max com
**CODE 10133**. O firmware espera a estrutura que o Anycubic Slicer Next grava:
`HEADER_BLOCK`, miniaturas, `EXECUTABLE_BLOCK`, marcadores `; CHANGE_LAYER` /
`; Z_HEIGHT` e um `CONFIG_BLOCK` com o perfil da máquina. O script fatia com o
PrusaSlicer usando os valores do **perfil oficial da Kobra 3 Max**
(`profiles/*.json`, extraídos do Anycubic Slicer Next 2.0.0.6) e reescreve o
arquivo nesse formato. O início usa o macro oficial `G9111`, que aquece, faz o
home, nivela e limpa o bico, seguido de `T0`: sem ele o firmware fica preso em
"analisando" (OrcaSlicer issues #12444 e #12952).

## Passos

1. Dependências (uma vez por sessão):
   ```bash
   apt-get install -y prusa-slicer xvfb
   ```
   ```bash
   pip install numpy matplotlib
   ```
2. Fatiar:
   ```bash
   python3 .claude/skills/kobra3max-gcode/scripts/slice_k3max.py CAMINHO/modelo.stl --filament PETG --out CAMINHO/saida.gcode
   ```
   Opções: `--filament PETG|PLA`, `--infill 20`, `--walls 3`, `--layer 0.2`,
   `--brim 5` (0 desliga), `--supports auto|on|off`, `--nozzle-temp`,
   `--nozzle-temp0` (1ª camada), `--bed-temp`,
   `--orient auto|none|x90|x-90|y90|y-90|x180`.
3. Leia o JSON impresso e confira:
   - `orientacao` / `tamanho_mm`: a orientação automática escolhe a face com
     mais apoio e menor altura. Se a peça ficou em pé ou de cabeça para baixo
     sem motivo, rode de novo com `--orient`.
   - `area_pendente_mm2` > 50 liga os suportes automaticamente.
   - `tempo`, `filamento_g`: informe ao usuário.
4. Envie o `.gcode` ao usuário com `SendUserFile` e explique: copiar para o pen
   drive (ou enviar pelo app/Wi-Fi) e selecionar na tela da impressora.

## Padrões

| | PETG (CR-PETG) | PLA |
|---|---|---|
| Bico 1ª camada / demais | 240 / 235 °C | 220 / 210 °C |
| Mesa (PEI texturizada) | 75 °C | 65 °C |
| Camada | 0,2 mm | 0,2 mm |
| Paredes / preenchimento | 3 / 20% giroide | 3 / 20% giroide |
| Brim | 5 mm | 5 mm |

## Limites

- Não há como enviar direto para a impressora: o IP dela (192.168.2.247) é da
  rede local do usuário.
- O formato imita o Anycubic Slicer Next sem ser gerado por ele. Se a impressora
  ainda mostrar CODE 10133, o plano B é o usuário fatiar no Anycubic Slicer Next
  (Ctrl+I importa STL) com Kobra 3 Max 0.4, PETG 240/235 °C, suporte normal(auto)
  e brim externo de 5 mm.
- PETG em placa PEI lisa: usar cola bastão, porque ele pode arrancar pedaço da placa.
