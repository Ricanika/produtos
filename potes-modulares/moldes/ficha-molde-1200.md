# Ficha de molde — pote 1200 ml (conceito)

Gerado por `gera-molde.py` a partir do parametrico da peca. **Conceito, nao
projeto executivo** — ver o cabecalho do gerador e a secao "O que falta".

| | |
|---|---|
| Peca | corpo 1200 ml, PP, parede 1.20 mm, altura 122.0 mm |
| Peso da peca (malha) | 74.3 g |
| Contracao aplicada | **1.50% linear** (XY e Z) |
| Cavidades | 2 |
| Tipo | duas placas, camara quente valvulada, extracao por placa impulsora |
| Plano de fechamento | plano da aba da borda; peca fica **de boca para baixo**, fundo no lado da injecao |

## 1. Fechamento e injecao

| | |
|---|---|
| Area projetada por cavidade | 123.6 cm² |
| Pressao media adotada | 400 kgf/cm² (parede fina, PP) |
| Fator de seguranca | 1.15 |
| **Fechamento por cavidade** | **57 tf** |
| **Fechamento total (2 cav + canais)** | **119 tf** |
| Volume de injecao por ciclo | 164 cm³ |
| Razao de fluxo L/t estimada | 172 |

## 2. Posticos

| | |
|---|---|
| Postico de cavidade | 212 × 151 × 159 mm |
| Aco lateral em volta da bolsa | 32 mm |
| Aco sob o fundo da bolsa | 35 mm (passagem do bico) |
| Macho, altura total | 218 mm (forma + haste + flange) |
| Placa impulsora | 30 mm, folga de 0.05 mm por lado sobre o macho |

## 3. Porta-molde e curso

| Placa | Espessura (mm) |
|---|---|
| Placa de fixacao fixa | 30 |
| Placa porta-cavidade | 179 |
| Placa impulsora | 30 |
| Placa porta-macho | 50 |
| Calcos (curso de extracao) | 179 |
| Placa extratora dupla | 44 |
| Placa de fixacao movel | 30 |

| | |
|---|---|
| Porta-molde | 302 × 452 mm |
| **Altura de molde fechado** | **542 mm** |
| Curso de extracao | 149 mm |
| **Abertura minima da maquina** | **333 mm** |

> A abertura minima e a conta que reprova maquina em pote alto: altura da peca
> (124) + curso de extracao (149) + queda (60).
> Confrontar com `CURSOABERT`, `ALTMINMOLDE` e `ALTMAXMOLDE` da injetora — os
> campos que estao nulos em `AD_INJETORAFICHA`.

## 4. Refrigeracao

Furos de Ø10 mm a 22 mm da superficie formadora (2.2 × D),
passo vertical de 45 mm. Circuito de cavidade e de macho **separados**.

| Circuito | Altura | Posicao X | Posicao Y |
|---|---|---|---|
| cavidade 1 | z = -12 | x = ±88 | y = ±58 |
| cavidade 2 | z = 32 | x = ±88 | y = ±58 |
| cavidade 3 | z = 78 | x = ±95 | y = ±64 |
| macho (bubbler)  | z = 18 | x = ±33 | y = ±17 |
| macho (bubbler)  | z = 18 | x = ±33 | y = ±17 |
| macho (bubbler)  | z = 18 | x = ±33 | y = ±17 |
| macho (bubbler)  | z = 18 | x = ±33 | y = ±17 |

| | |
|---|---|
| Alvo de regime | Re = 6.000 (turbulento) |
| Velocidade necessaria | 0.60 m/s |
| **Vazao por circuito** | **2.8 L/min** |
| ΔT admissivel no circuito | ≤ 3 °C |

## 5. Ciclo e capacidade

| | |
|---|---|
| Ciclo estimado | 21 s |
| Pecas/hora (2 cav) | 343 |
| Consumo de resina | 25.5 kg/h |

## 6. O que falta para virar projeto executivo

1. **Contracao por direcao e por tamanho** — aqui esta 1.50% linear e igual
   nos dois eixos. O correto sai do Moldflow, e a parede varia de 1,15 a 1,40 mm
   entre os quatro potes.
2. **Porta-molde normalizado real** (HASCO/DME/Meusburger) com codigo de catalogo,
   guias, colunas de apoio, retorno de extracao e refrigeracao das placas.
3. **Camara quente especificada** (marca, modelo, numero de bicos, controlador) e
   o rebaixo do vestigio no pe do pote.
4. **Respiros**: 0,02–0,03 mm na linha de fechamento e no ultimo ponto a encher.
5. **Detalhamento 2D com tolerancias**, cotas steel safe marcadas e stack-up.
6. **Aco e tratamento** por componente; a classe aqui e 101 (≥ 48 HRC).
7. **Moldflow** e o plano de try-out.
