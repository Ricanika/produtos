# Protótipo em FDM — Kobra 3 Max + CR-PETG cinza

**Filamento:** Creality CR-PETG cinza · 1,75 mm · 1,0 kg · impressão 230–250 °C (do rótulo)
**Impressora:** Anycubic Kobra 3 Max · bico 0,4 mm · mesa PEI texturizada
**Peças:** `stl/impressao/` — corpo de 600 ml (duas versões) e tampa

> Não consegui gerar o G-code aqui — não há fatiador neste ambiente. O que vai abaixo é o
> perfil para você aplicar no AnycubicSlicerNext (ou OrcaSlicer) e os STL já orientados.

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
- ~63 g de PETG, algo em torno de 4–5 h.

### `pote-600-real.stl` — a peça como ela é
O fundo rebaixado de 1,8 mm, apoiando no anel do pé. **Só imprima este depois que o outro sair
bem** — é o teste de fogo da sua mesa. Brim de 10 mm obrigatório.

### `tampa.stl`
- Posição: **de cabeça para baixo** — a face de cima na mesa, o plug apontando para cima.
  Contato de 2.727 mm² numa moldura de 6,9 mm; com brim, 6.897 mm².
- **Suporte só dentro do poço da bandeja** (3,5 mm de profundidade): use "suporte apenas sobre a
  mesa". É raso e sai fácil.
- Sem suporte no plug — ele aponta para cima e não tem balanço.
- ~31 g, cerca de 2 h.

**O aro de TPE não se imprime em FDM.** Para o protótipo use **O-ring de seção 2,0 mm** cortado no
comprimento e colado com cianoacrilato, ou corda de silicone de 2 mm. Perímetro de vedação: 389 mm.

---

## 4. O que conferir na peça impressa

1. **Primeira camada:** linhas encostadas, sem vão. É o retrato de tudo.
2. **Encaixe do plug na boca:** a folga de projeto é 1,00 mm por lado. Em FDM a parede sai ~0,1 mm
   mais grossa que o nominal, então espere um pouco apertado. Se travar, o problema é a impressão,
   não o projeto.
3. **A canaleta de 0,6 mm não sai fiel em FDM** — com bico de 0,4 e camada de 0,2 ela vira um
   sulco raso. Serve para posicionar o O-ring, não para medir a retenção. **A retenção do aro só se
   testa em peça injetada.**
4. **Empilhamento:** imprima dois corpos e uma tampa e confira o passo de 60 mm entre os pés.
   É a prova que importa.
5. **Pé na bandeja:** o pé de 112,4 mm tem que entrar no vão de 113,4 mm da tampa com folga de
   0,5 mm por lado. Em FDM isso vira ~0,3 mm. Se entrar justo demais, é a impressão.

---

## 5. Perfil para importar

`perfil-orca-petg-kobra3max.json` na mesma pasta. Importar em **Filamento → Importar perfil**.
Se o fatiador reclamar do campo `inherits`, troque `"Generic PETG"` pelo nome exato do perfil PETG
que aparece na sua lista. Os valores da tabela acima valem de qualquer jeito, digitados na mão.
