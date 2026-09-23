# Protótipo em FDM — Kobra 3 Max + CR-PETG cinza

**Filamento:** Creality CR-PETG cinza · 1,75 mm · 1,0 kg · impressão 230–250 °C (do rótulo)
**Impressora:** Anycubic Kobra 3 Max · bico 0,4 mm · mesa PEI texturizada
**Peças:** `stl/impressao/` — corpo de 600 ml (duas versões) e as três tampas

> **O G-code está pronto**, em `fatiamento/saida/` — seis arquivos, todos com o `G9111` que a
> Kobra 3 Max exige e todos validados (`fatiamento/valida.py`). Reproduza tudo com
> `bash fatiamento/gerar.sh`. O que vai abaixo é o perfil equivalente para o AnycubicSlicerNext
> (ou OrcaSlicer), caso você prefira fatiar aí, e os STL já orientados.

---

## 1. Por que está descolando — comece por aqui

**PETG normalmente gruda DEMAIS em PEI.** O problema clássico é o contrário do seu: a peça
arranca lasca da chapa. Se a sua está soltando, **não é o material nem a chapa — é parâmetro ou
é a peça**. E neste caso é principalmente a peça:

| | Área de contato na mesa |
|---|---|
| Corpo 600 ml como é a peça (apoia num anel de pé de 1,15 mm) | **421 mm²** |
| Mesmo corpo **+ brim de 10 mm** | 4.123 mm² (10×) |
| Corpo **com fundo plano** (variante de impressão) | 9.320 mm² (22×) |
| Fundo plano **+ brim** | 13.021 mm² (31×) |

**421 mm² para segurar uma peça de 62 mm de altura é pouco para qualquer impressora.** O pote
apoia só no anel do pé, de 1,15 mm de largura por 370 mm de perímetro. Qualquer força de contração
ganha dessa área.

### Na ordem em que eu atacaria

1. **Brim de 10 mm, sempre.** Resolve 10× o problema de uma vez. Custa 3 min de impressão.
2. **Ventoinha a 0% nas 4 primeiras camadas**, e no máximo 40% depois. Se você estiver usando um
   perfil de PLA com o filamento PETG, a ventoinha a 100% na camada 2 levanta a peça sozinha.
   **Esta é a causa mais comum de "descola do nada" com PETG.**
3. **Mesa a 80 °C na primeira camada, 75 °C no resto.** PETG a 60 °C (temperatura de PLA) não segura.
4. **Primeira camada a 25 mm/s** e altura de 0,25 mm. A Kobra 3 vem rápida de fábrica; primeira
   camada rápida sobre 421 mm² não cola.
5. **Z-offset:** a primeira camada tem que ficar *esmagada*, com as linhas encostando uma na outra,
   sem vão. Se dá para ver o vão entre as linhas, está alto.
6. **Limpe o bico antes de cada impressão.** PETG deixa bolota no bico, e a Kobra 3 nivela sondando
   com o bico — bolota ali desnivela a mesa inteira.

### A lavagem pode ter piorado

Detergente de louça com **hidratante, glicerina ou perfume** deixa filme e é péssimo para aderência.
Se o seu tem "hidrata as mãos" no rótulo, o problema pode ter começado aí. Procedimento certo:

1. água morna + detergente **neutro, sem hidratante**, com esponja macia;
2. **enxaguar muito** — o filme de detergente é o que atrapalha;
3. secar com papel toalha;
4. passar **álcool isopropílico 90%+** (não use álcool 70% de farmácia, tem água e aditivo);
5. **não encostar o dedo na chapa depois disso.** Gordura da mão é o suficiente.

### Se depois de tudo isso ainda soltar

- **Filamento úmido.** PETG puxa umidade rápido, e no Brasil um rolo aberto há semanas já está
  molhado. Sintomas: fiapos, estalos no bico, extrusão irregular. **Secar a 65 °C por 6–8 h.**
- **Corrente de ar.** Kobra 3 Max é aberta e a peça é alta. Longe de janela e ventilador.
- **Cola em bastão.** Em PEI texturizada com PETG, uma camada fina de cola bastão ajuda de verdade
  (em PEI lisa ela serve para o contrário: evitar que grude demais).

---

## 2. Perfil de impressão

| Parâmetro | Valor | Por quê |
|---|---|---|
| Bico | **240 °C** (245 na 1ª camada) | meio da faixa do rótulo (230–250) |
| Mesa | **80 °C** 1ª camada · **75 °C** resto | PETG precisa disso; 60 não segura |
| Altura de camada | 0,20 mm (0,25 na 1ª) | |
| Largura de extrusão 1ª camada | 0,50 mm | mais material, mais cola |
| **Ventoinha** | **0% até a camada 4**, depois **40% máx.** | o item que mais causa descolamento |
| Velocidade 1ª camada | **25 mm/s** | |
| Velocidade paredes | 40–50 mm/s | PETG não gosta de correr |
| Velocidade preenchimento | 60 mm/s | |
| **Brim** | **10 mm**, tipo externo | 10× a área de contato |
| Perímetros | 3 | parede do modelo 1,15 mm ≈ 3 × 0,4 |
| Topo / fundo | 5 / 4 camadas | |
| Preenchimento | 10% giroide | a peça é casca, quase não usa |
| Retração (direct drive) | 1,0–1,5 mm a 35 mm/s | |
| Fluxo | 95% | PETG tende a superextrudar |
| Z-hop | 0,2 mm | evita bater em bolota |
| Detectar paredes finas | ligado | a peça é toda parede fina |

**Não use "ironing" nem velocidade acima de 150 mm/s.** A Kobra 3 Max alcança, mas PETG a essa
velocidade fica fosco, frágil e com má adesão entre camadas — e aqui o que importa é o encaixe.

---

## 3. Os arquivos e como posicionar cada um

### `pote-600-fundoplano.stl` — **comece por este**
Mesma peça, com a elevação de fundo zerada. **22× mais área de contato.** Muda só o volume interno
(+19 ml); **não muda encaixe, passo, nem a prova da tampa**. Para validar o produto, é equivalente.

- Posição: **natural, boca para cima.** Sem suporte.
- Brim de 10 mm.
- 94 g de PETG, 12 h 45 (camada 0,2) — `saida/3_pote600.gcode`.

### `pote-600-real.stl` — a peça como ela é
O fundo rebaixado de 1,8 mm, apoiando no anel do pé. **Só imprima este depois que o outro sair
bem** — é o teste de fogo da sua mesa. Brim de 10 mm obrigatório.

### `tampa-pp.stl` — a tampa com as duas travas
- Posição: **invertida** — o deck na mesa, o plug apontando para cima. De pé ela apoiaria só na
  ponta das 2 travas (**0 mm²**); invertida, **3.183 mm²**.
- **Suporte de mesa E de peça.** No perfil: `--dont-support-bridges=0` (sem ele o fatiador recusa
  suporte sob o poço da bandeja e entrega uma ponte livre no meio, sem avisar) e
  `--support-material-buildplate-only=0` — com o padrão, o suporte para em z = 3,3 e a **prateleira
  do gancho** (1,1 mm de balanço em 89 mm, a 11,5 mm de altura) sai no ar. Custa 2,8 g e 13 min, e é
  justamente a feição que o protótipo existe para provar.
- 51 g, 6 h 05 — `saida/1_tampa_pp.gcode`.

### `tampa-correr.stl` + `gaveta.stl` — a terceira tampa (revisão 9)
- **A tampa de correr é o pior caso da mesa.** Invertida ela apoia só nas **duas paredes da calha**
  (18 mm²), porque a calha é mais alta que o deck, e o deck fica 2,5 mm no ar. Vai com suporte de
  mesa e de peça e brim de 12 mm: 58 g e 7 h — **mais da metade é suporte**.
- **A gaveta imprime invertida**, e aí o friso do 2º aro fica para cima, sem suporte nenhum: 4 g,
  33 min. Painel de 1,8 mm, 9 camadas.
- **A folga da gaveta é de injeção, 0,25 mm por lado.** Nenhuma FDM entrega isso: conte com lixar,
  ou imprimir a gaveta a 99% em X e Y. Se ela correr *folgada* na primeira tentativa, desconfie da
  impressão, não do projeto.

**Nem o filete nem o 2º aro se imprimem em FDM.** Para o protótipo use corda de silicone de
**1,4 mm** (filete, 438 mm de perímetro) e de **1,2 mm** (2º aro, 147 mm), cortada no comprimento e
colada de topo com cianoacrilato.

---

## 4. O que conferir na peça impressa

1. **Primeira camada:** linhas encostadas, sem vão. É o retrato de tudo.
2. **Encaixe do plug na boca:** a folga de projeto é **0,60 mm por lado** (plug de 144,9 na boca de
   146,1). Em FDM a parede sai ~0,1 mm mais grossa que o nominal, então espere um pouco apertado.
   Se travar, o problema é a impressão, não o projeto.
3. **O friso de 0,6 mm não sai fiel em FDM** — com bico de 0,4 e camada de 0,2 ele vira um sulco
   raso. Serve para posicionar a corda de silicone, não para medir a retenção. **A retenção do
   filete só se testa em peça injetada.**
4. **Empilhamento:** imprima dois corpos e uma tampa e confira o passo de 60 mm entre os fundos.
   É a prova que importa.
5. **O fundo reto na bandeja:** não há pé embutido desde a revisão 7 — quem desce na bandeja é o
   **fundo do pote de cima**, 141,67 mm, no vão de 143,3 mm da tampa: 0,8 mm por lado. Em FDM isso
   aperta. Se entrar justo demais, é a impressão.
6. **A trava de clipe:** é a feição nova da revisão 8 e a razão do suporte de peça. O gancho tem de
   passar 0,80 mm sob a face de baixo da saia da borda e travar. Se a prateleira do gancho saiu
   caída, o suporte não subiu — confira o `--support-material-buildplate-only=0`.
7. **A gaveta correndo:** com o 2º aro colado, ela tem de correr os 24 mm sem levantar e voltar a
   selar a janela. É a única coisa da revisão 9 que só o protótipo responde.

---

## 5. Perfil para importar

`perfil-orca-petg-kobra3max.json` na mesma pasta. Importar em **Filamento → Importar perfil**.
Se o fatiador reclamar do campo `inherits`, troque `"Generic PETG"` pelo nome exato do perfil PETG
que aparece na sua lista. Os valores da tabela acima valem de qualquer jeito, digitados na mão.
