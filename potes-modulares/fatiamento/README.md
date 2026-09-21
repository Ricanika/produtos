# Fatiamento — potes modulares em PETG na Anycubic Kobra 3 Max

Agente instalado a partir de `AGENTE-Kobra3Max-PETG.md` (runbook recebido pronto e
testado). Este diretório é o ambiente de trabalho que o runbook descreve, já
alimentado com as peças deste projeto. **As cotas seguem a revisão 5** (footprint
139,7 × 79,8, canto R10): rodar `gerar.sh` depois de mexer na geometria já refaz tudo,
porque os STL saem de `gera-3d-impressao.py`, não de arquivo parado.

```
./gerar.sh          # STL -> prep -> gcode -> miniatura -> validação -> desenho de camada
```

Leva ~23 s. Precisa de `prusa-slicer` 2.7.2 e `pip install trimesh numpy pillow`.
`saida/` e `prep/` não vão para o git — são artefatos, refeitos pelo script.

## Os arquivos gerados

| Arquivo | Peça | Camada | Massa | Tempo |
|---|---|---|---|---|
| `1_tampa_q010.gcode`   | tampa      | 0,10 mm | 45,8 g | 8 h 54 |
| `2_pote600_q010.gcode` | corpo 600 ml | 0,10 mm | 89,3 g | 20 h 17 |
| `3_tampa_r020.gcode`   | tampa      | 0,20 mm | 44,4 g | 5 h 21 |
| `4_pote600_r020.gcode` | corpo 600 ml | 0,20 mm | 93,2 g | 12 h 00 |
| `5_tampa_pe_r020.gcode` | **tampa PE** | 0,20 mm | 54,8 g | 6 h 33 |

A **tampa PE** (arquivo 5) é a sobretampa de encaixe externo da revisão 6. Imprime **em pé**
(saia para baixo: 1.262 mm² de contato contra 950 invertida), com suporte da mesa sob o deck e o
piso da bandeja. **Ressalva importante:** PETG é muito mais rígido que PEAD. O protótipo serve para
conferir **encaixe e cotas**, não a **força de abrir** — e há risco real de trincar a garra ao
encaixar. Se trincar, não é erro de projeto, é o material errado para esse teste.

**Para o primeiro protótipo, imprima o par 0,20 mm (3 e 4).** Ele resolve a mesma
pergunta — se o plugue da tampa entra e atrita na parede do pote — em 17 h em vez de
29 h, e é metade das camadas para dar errado. Note que o corpo em 0,20 mm sai
**mais pesado** (93,2 contra 89,3 g): numa parede de 1,15 mm a camada grossa
superextrude. Gasta mais filamento e ainda assim vale pelo tempo. O par 0,10 mm é para a amostra
de apresentação, depois que o encaixe já estiver aprovado.

## Três decisões que não são preferência

**O corpo impresso é o `pote-600-fundoplano.stl`, não o `pote-600-real.stl`.**
A geometria real tem pé rebaixado de 6 mm: ela toca a mesa em **448 mm²** para 62 mm
de altura, e o fundo elevado vira uma ponte de **82 mm sem apoio**. Isso não é ajuste
de parâmetro, é a peça errada para FDM — pé rebaixado existe para a injeção, onde o
molde é que forma o vão. A variante de fundo plano tem **9.244 mm² de contato
(21×)**, custa +19 ml de volume interno, e tem parede e boca idênticas à real — ou
seja, serve inteira para validar o encaixe da tampa.

**A tampa vai de cabeça para baixo** (`"flip": true` em `pecas.json`). Na posição de
uso ela apoia em 601 mm²; invertida, apoia pelo topo em **2.888 mm²**.

**A tampa precisa de `--dont-support-bridges=0`.** Invertida, o rebaixo de
empilhamento (131,9 × 72,0 mm, 3,5 mm de profundidade) vira um teto. O perfil traz
`dont_support_bridges = 1`, que faz o PrusaSlicer **recusar suporte** ali: o
fatiamento sai sem erro nenhum e a camada z=3,60 vira **295 fios de 72,4 mm de vão
livre**. Com a flag, entra uma coluna de suporte de 11 camadas da mesa até z=3,10,
dentro de uma cavidade aberta para baixo — sai com a mão. Não ponha essa flag nos
potes: lá a única ponte é a aba da boca, com 3 mm de vão, que é overhang normal, e
ligar suporte faria uma torre de 60 mm abraçando a parede externa.

## Por que a peça descolava

O diagnóstico não era a limpeza da mesa — PETG normalmente gruda **demais** no PEI.
Era área de contato e parâmetro:

- mesa a **80 °C** (abaixo de ~70 o PETG encosta e solta — é o fator isolado maior);
- ventoinha **30–45 %, desligada nas 4 primeiras camadas** (100 % é o que descola no
  meio da impressão);
- bico **245/240 °C**;
- **aba de 8–10 mm** com `brim_separation = 0`;
- e a área de contato do corpo, que subiu de 448 para 9.244 mm² trocando a geometria.

Detergente com hidratante/glicerina piora a adesão. Lave com detergente neutro, enxágue
bem e passe álcool isopropílico. Não use cola: em PETG cola é desmoldante.
Não arranque a peça com a mesa quente — espere baixar de 50 °C ou o PEI sai junto.

## Verificação feita

Todos os 4 arquivos passam os cinco critérios de aceite do runbook: `G9111` presente,
percurso dentro de 0–420 em X e Y, Z começando em 0,20 e nunca negativo, miniatura
230 × 110 PNG com base64 conferindo, e apenas os comandos permitidos
(`G1 G21 G90 G9111 G92 M82 M84 M104 M106 M107 M117 M140 M400 M900` — sem `G28`,
`M109`, `M190`, `M486`, `M73`). Os desenhos de primeira camada estão em `camadas/`.
