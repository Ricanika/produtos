# Potes retangulares modulares em PP — resumo para retomar em outro chat

**Projeto 115 do ERP (Nitron) · Revisão 4 · 17/09/2026**
Branch: `claude/serene-johnson-ja8az8` · pasta `potes-modulares/`

Este arquivo é auto-contido: cole ele num chat novo e o contexto está todo aqui.

---

## 1. O pedido

Linha nova de potes retangulares em PP transparente, inspirada num render de referência
(potes com tampa de teca e tampa verde). Requisitos que o Ricardo deu, na ordem em que apareceram:

1. **Três tipos de tampa:** teca com vedação em TPE · PE · PP para sabão líquido/amaciante
   (serve também para farofa, cereais).
2. **Quatro litragens.** Começou em 500 ml / 1 L / 1,5 L / 2 L e **mudou para 600 / 1200 / 1800 /
   2400 ml** (pacote de mantimento).
3. **Modular:** empilhando os menores, tem que chegar exatamente na altura do maior.
4. **Parede reta**, não conada, com cantos arredondados.
5. **Sem trava**, acabamento liso.
6. Validar tudo contra o parque de injetoras real (via MCP Sankhya / Nitron).

---

## 2. A linha, como está fechada

**Corpo 121,2 × 93,3 mm · 127,2 × 99,2 mm na aba da borda · canto R18 · saída 0,5°/lado ·
módulo 60 mm · fundo 2,0 mm igual nos quatro · parede da borda 1,40 mm igual nos quatro ·
pé embutido 112,4 × 84,4 mm igual nos quatro**

| Tamanho | Altura corpo | Passo | Parede | Peso corpo | Resina (PP a R$ 11,06/kg) |
|---|---|---|---|---|---|
| 600 ml | 62,0 mm | 60 | 1,15 mm | 43,7 g | R$ 0,48 |
| 1,2 L | 122,0 mm | 120 | 1,20 mm | 69,8 g | R$ 0,77 |
| 1,8 L | 182,0 mm | 180 | 1,30 mm | 100,6 g | R$ 1,11 |
| 2,4 L | 242,0 mm | 240 | 1,40 mm | 135,1 g | R$ 1,49 |

Empilhamento confere: `600×4` = `1,2 L×2` = `600+600+1,2 L` = `600+1,8 L` = `2,4 L` = 240 mm.

Mantimento: o **2,4 L recebe o pacote de 2 kg de arroz** e o **1,2 L o de 1 kg de feijão** — era o
motivo de trocar a escala (na escala antiga o 2 L levava só 1,70 kg de arroz).

### As três regras que fazem o passo fechar

1. Fundo de **2,0 mm igual nos quatro**.
2. **Piso da bandeja da tampa 2,0 mm abaixo da borda** — igual à espessura do fundo. É o plano modular.
3. **Pé embutido nos últimos 6 mm da base**, medida igual nos quatro (degrau varia de 2,3 a 3,9 mm
   para compensar a saída). Sem ele o pote de cima não caberia na bandeja.

### Por que parede reta ajudou

Com pote conado, bocal comum e passo constante, o volume cresce mais rápido que a altura e as
capacidades redondas só fechavam variando muito a saída. **Com parede reta o volume fica
proporcional à altura** e o conflito some; sobra um resíduo absorvido por uma elevação de fundo de
0 a 3,4 mm, invisível.

**Saída de 0,5°/lado** é o compromisso: no maior pote a base fica 4,2 mm mais estreita que o topo
(3,5%, imperceptível), e o pote vazio ainda aninha — 6 potes de 2,4 L em 1.044 mm contra 1.453 soltos
(−28%). A 0,25° não aninha mais e o frete do pote vazio sobe.

Exige polido A2 nas laterais (textura pediria saída extra), extração por **placa impulsora** e
**válvula de ar no macho**. Força de extração ~5 kN contra ~62 kN disponíveis numa 380 t: o gargalo
é curso e vácuo, não força.

---

## 3. A tampa — chegou aqui depois de dois erros meus

### Onde eu errei (não repetir)

- **Revisão 2:** aro de TPE em canaleta de um lábio, comprimido contra a boca. Sem retenção (o aro
  sai na primeira abertura), com orçamento de largura ficcional (2,00 mm reservados para uma canaleta
  que precisa de 4,00) e **sem definir de onde viria a força de fechamento**.
- **Revisão 3:** troquei por lábio de PP moldado na tampa. Melhor, mas ainda **vedação axial**.
- **O erro comum às duas:** vedação axial num retângulo pede **32 kgf permanentes** ao longo dos
  389 mm de perímetro. É por isso que pote retangular hermético usa trava. Como o Ricardo não quer
  trava, axial estava morto desde o começo.

### A solução (dele, e está certa): vedação RADIAL

Um **plug** da tampa desce 12 mm dentro do pote e leva o aro de TPE numa canaleta na face externa.
**O aro trabalha contra a PAREDE do pote, não contra a borda.**

```
boca do pote ..... 118,4 mm      face do plug ..... 116,4 mm (folga 1,00 por lado)
parede do plug ... 1,50 mm       canaleta ......... 0,60 mm, a 5,0-7,4 mm da borda
aro de TPE ....... seção 2,4 × 1,8 mm, sobra 1,20 -> comprime 0,20 contra a parede
plug desce ....... 12 mm         vão da bandeja ... 113,4, recebe o pé de 112,4
tampa ............ 127,2 × 99,2 mm, rente à aba, SEM saia externa. 22,8 g. R$ 0,22 + aro 1,8 g
```

| | O que segura | Força |
|---|---|---|
| Axial (errado) | força permanente de fechamento | 32 kgf o tempo todo → precisa de trava |
| **Radial (certo)** | interferência lateral de 0,20 mm | **zero em repouso · 1,0 kgf para abrir** |

Abrir descascando um canto: **1,0 kgf** (5,8 kgf se puxar reto, o que ninguém faz).

Ganho extra: **vedação radial tolera a borda flexionar** — o aro acompanha a parede em vez de perder
contato, que é o que mata aro axial.

O plug faz três coisas: **veda**, **forma a parede da bandeja** onde o pote de cima apoia, e
**centra a tampa**.

### A aba em U na borda

A borda vira para fora 3,0 mm com lábio descendente de 3,5 mm. Seção em U = **34× a inércia da
parede simples**. É ela que impede o lado reto de abrir, e serve de pega. Custou +13 cm² de área
projetada, o que moveu o 600 ml da classe de 160 t para a de 200 t.

### Aberto, para o tryout

- **Retenção do aro:** canaleta de 0,60 mm sai por arranque (rampas de 30°, sem gaveta). Testar
  500 aberturas e ver se o aro migra.
- **Ar preso:** 3,8 kgf a mais no 600 ml, 0,9 no 2,4 L. Alivia com chanfro de 30° × 1,5 mm na boca.
  É o mesmo "pop" que a OXO vende como característica.
- **Aba de alavanca:** ~18 mm numa lateral curta, com rebaixo na aba da borda para ficar rente.
- **Estanqueidade de cabeça para baixo:** plausível, **não prometida**. Medir com água colorida,
  24 h, deitado e invertido.

---

## 4. Material — as três famílias de PP

| Família | Comporta-se | Grades em casa | Compra 12 m |
|---|---|---|---|
| Homopolímero | rígido e transparente, quebradiço no frio | H 105 (926 t), H 103 (473 t) | R$ 11,06 · R$ 9,90 |
| **Randômico** | transparente, brilhante, tolerante | **RP 141 (299 t)**, RP 340 S (49,5 t) | **R$ 9,54** · R$ 17,00 |
| Heterofásico | impacto altíssimo, porém opaco | CP 141 (109 t) | R$ 10,52 |

- **Corpo: PP H 105** com clarificante (grade que a casa compra em volume).
- **Tampa: PP RP 141 randômico.** Transparente, aceita dobradiça viva (heterofásico não aceita — a
  fase de borracha impede a orientação molecular), e é o mais barato dos três.
- **Tampa PE foi descartada:** PEBD é compra residual (500 kg/12 meses), flui a frio (o plug relaxa e
  a interferência some) e daria material misto na reciclagem.
- **TPE Karinprene 45** (CODPROD 997) está cadastrado mas **sem compra há 4 anos** — recotar.
  Não há bi-injeção no parque: o aro é peça montada.

---

## 5. Bico da tampa de líquidos — a bandeja é o vertedor

Sem copinho, sem pump, nada acima do plano modular. Aproveita a bandeja que a modularidade já obriga:

1. Furo de vazão no canto (≈25 × 15 mm), encostado na parede da bandeja.
2. Entalhe de 12-15 mm na parede da bandeja — o canto R18 já faz a curva, não se molda bico.
3. **Lábio de corte de 0,4 mm** na aresta: quebra o filme, a gota se solta em vez de escorrer.
4. Piso com caimento de 2-3° para o furo: o que respinga volta para dentro pelo mesmo furo.
5. Aba com dobradiça viva rente ao piso — não veda (quem veda é o aro), só barra poeira e cheiro.

Zero peça adicional, sem gaveta no molde. Descartados: pump comprada (a casa já compra a válvula
CODPROD 10085 do porta-detergente 545/553, mas passa do plano modular) e copinho dosador.

---

## 6. Injetoras — o que o ERP mostrou

Parque: **46 injetoras** (45 monitoradas). 80 t ×1 · 120 t ×7 · 150 t ×2 · 160 t ×9 · 200 t ×12 ·
250 t ×9 · 280 t ×1 · 300 t ×1 · 380 t ×3 · 600 t ×1.
A tonelagem real está em `TPRCAP.DESCRICAO` (via `TPRWCP.CODCAP`) — **não** em `QTDCAPACIDADEPAD`,
que mistura kN e ton.

Os quatro corpos têm a **mesma área projetada (139 cm²)**: quem decide a máquina é profundidade,
não tonelagem.

| Tamanho | Máquina | Fecham. 2 cav | Curso | Molde | Peça equivalente que já roda lá |
|---|---|---|---|---|---|
| 600 ml | 200 t — INJ 1–6, 19–22, 35, 37 | 129 t | 136 mm | 252 mm | pote 176-C, ciclo medido 16,7 s |
| 1,2 L | 200 t | 138 t | 268 mm | 312 mm | modular 450 ml (320-C) na INJ 37 |
| 1,8 L | 250 t — INJ 23–28, 38, 39 | 147 t | 400 mm | 372 mm | modular 1,2 L (322-C) na INJ 25 |
| 2,4 L | 380 t — INJ 31, 32, 33 | 153 t | 532 mm | 432 mm | modular 2,4 L (323-C) na INJ 33 · pote 5,8 L (237-C) na INJ 31/33 |

**Sem máquina nova.** A peça mais funda desta linha é menos exigente que o pote de 5,8 L que já roda
nas 380 t. A **INJ 32 estava parada** — candidata ao try-out.

**Bloqueio de dado:** `AD_INJETORAFICHA` tem 1 registro e os 29 campos de especificação nulos. Curso
de abertura, curso e força de extração não têm conferência documental. Preencher antes de liberar o
molde do 2,4 L.

**Aproveitamento:** 2,4 L com 2 cavidades usa 40% do fechamento de uma 380 t. Avaliar 4 cavidades
(~306 t, molde ~620 × 500 mm).

**Capacidade** (2 cav, 20 h/dia, 22 dias): 186 / 151 / 127 / 109 mil pç/mês. O 2,4 L é o gargalo do
kit. **L/t de 216 no 2,4 L** está no limite: pede câmara quente com 2 pontos de injeção ou parede de
1,5 mm. Definir no Moldflow.

---

## 7. O que já existe no ERP (reaproveitar, não recriar)

| Achado | Onde |
|---|---|
| **Projeto 115 "Conjunto Potes Modular"** — status Aprovado, produto já modelado | `AD_PROJETOS` |
| Molde 115/1 — **orçamento aprovado de USD 47.100**, 2 cav, 75 dias, MR Plastic Mould, 04/2021 | `AD_MOLDE`, `AD_ORCAMENTO` |
| Linha modular quadrada em catálogo: 319-C a 323-C (250 ml a 2,4 L) | `TGFPRO` |
| **Tampa única já validada:** ref. 321-T serve 800 ml, 1,2 L e 2,4 L | `TGFPRO` |
| O 2,4 L é o que gira: 35 mil un/ano só no cliente Natura (ref. 323) | `TGFITE`/`TGFCAB` |
| Kit modular 6 pçs: 19.078 kits / R$ 449 mil em 12 meses (ref. 353) | `TGFITE`/`TGFCAB` |
| Tampa de madeira já é produto corrente com **FSC 100%** (NEO-COC-191022) | `TGFPRO` |
| Cadeia própria de teca: tora, ripa serrada (CODPROD 6759), planta WOOD (CNC, moldureira), Teak Brazil | `TPRPLP`, `TGFPRO` |

**Ferramental:** 4 moldes de corpo + 2 de tampa (padrão e dosadora) + 1 de aro de TPE = **7
ferramentas**. A teca usa programa de CNC. Benchmarks dos próprios orçamentos com a MR Plastic Mould
(USD): corpo lixeira 12 L/380 t = 36.900 · 284-U/280 t = 20.100 · 214-U/250 t = 18.900 ·
corpo 026/120 t = 6.300 · tampa 026-T/90 t = 5.500. **Ordem de grandeza USD 140–190 mil**, com a
cotação de USD 47.100 já aprovada como ponto de partida.

---

## 8. Arquivos

Branch `claude/serene-johnson-ja8az8`, pasta `potes-modulares/`:

| Arquivo | O que é |
|---|---|
| `README.md` | estudo completo, 12 seções, com o histórico das revisões e os erros registrados |
| `calculo-modular.py` | memória de cálculo: geometria, encaixe, forças de vedação, capacidade, aninhamento |
| `gera-3d.py` | gerador paramétrico → 6 STL + `perfis.json` (receita de anéis que o visualizador usa) |
| `verifica-malha.js` | roda o construtor do visualizador fora do navegador e compara com o STL |
| `stl/` | 6 peças em mm, escala real, prontas para imprimir protótipo |
| `visualizador-3d.html`, `ficha-tecnica.html` | cópias das páginas publicadas |

Artifacts publicados:
- Ficha técnica: https://claude.ai/artifact/GnEGBNxhsvXeSJNsZvpfwn
- Modelo 3D interativo: https://claude.ai/artifact/CTZYnTjY2hZYiye2SaHJz6

**A malha se confere sozinha** a cada geração: volume assinado positivo nas 6 peças, cavidade dentro
de 0,8% da capacidade nominal, peso dentro de 3% do cálculo. É malha, não sólido CAD — **o molde
precisa do CAD paramétrico do projetista**.

---

## 9. Próximos passos

1. Confirmar a saída de 0,5° com o design (é o que separa "reto" de "aninha no frete").
2. Preencher `AD_INJETORAFICHA` das 46 injetoras (curso de abertura, curso e força de extração).
3. Reabrir o Projeto 115 e recotar com a MR Plastic Mould a partir da cotação aprovada.
4. Recotar o TPE Karinprene 45 — parado há 4 anos, agora com volume das três tampas.
5. Protótipo impresso do 600 ml + tampa: testar o encaixe do plug e a retenção do aro na mão.
6. Moldflow do 2,4 L (L/t 216) e estudo de extração da peça reta.
7. Ensaio de vedação: água colorida, 24 h, deitado e invertido. Só depois disso se fala em promessa
   de vedação na embalagem.
8. Reservar INJ 32 (380 t) para o try-out do 2,4 L.

---

## 10. Contexto técnico do ambiente

Os dados saíram do **Sankhya via MCP Nitron** (somente leitura). Tabelas usadas: `TPRWCP` + `TPRCAP`
(parque e tonelagem) · `TPRWCP.AD_CICLOATUAL/AD_DHCICLO` (ciclo ao vivo) · `TPRAPA`→`TPRAPO`→`TPRIATV`
(que peça roda em qual máquina) · `AD_FICHATECNICA` (ciclos de referência) ·
`AD_PROJETOS`/`AD_MOLDE`/`AD_ORCAMENTO` · `TGFITE`/`TGFCAB` (preço real de resina e vendas) · `TGFPRO`.

Armadilha conhecida: o Sankhya cancela chamadas paralelas na mesma sessão HTTP — serializar as
consultas.
