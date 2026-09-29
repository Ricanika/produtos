# Suporte plástico do deck (tipo IKEA) — fatiamento

`suporte-deck-ikea.stl` é a base em grelha de uma placa de deck, com 311,1 × 311,1 × 15,0 mm e
94,4 cm³, e a malha é fechada. Ela é fatiada com o mesmo perfil dos potes
(`../potes-modulares/fatiamento/kobra3max_petg.ini`: Anycubic Kobra 3 Max, bico 0,4, PETG,
`G9111` no início).

```
./gerar.sh     # ~1,5 min; precisa de prusa-slicer 2.7.2 e pip install trimesh numpy pillow
```

| Arquivo | Camada | Massa | Tempo |
|---|---|---|---|
| `saida/suporte_deck_r020.gcode` | 0,20 mm | 187 g | 28 h 54 |

**Orientação:** a face −Y do STL fica na mesa. Os pés tocam a mesa em 2.530 mm², e a parte de
baixo da grelha fica a 3,4 e 5,3 mm de altura, sustentada por suporte que sai da mesa. Virada ao
contrário, a peça apoiaria só nas pontas dos clipes (311 mm²), com a grelha a 8 mm do chão.

**O suporte custa caro:** ~55 g de 187 g (suporte + interface). É o preço dessa geometria. A
peça original é injetada, e o molde forma o vão sob a grelha.

**Validação:** tem `G9111`, o percurso fica dentro de X 48–373 / Y 47–372, Z vai de 0,20 a 15,40
em 94 camadas e a miniatura 230 × 110 PNG confere. A primeira camada está desenhada em
`camadas/z020.png`.
