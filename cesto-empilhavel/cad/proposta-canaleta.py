#!/usr/bin/env python3
"""Canaleta de ponta a ponta na lateral -- desenho de validacao.

Responde ao pedido "uma canaleta de ponta a ponta na lateral, de um lado macho
e do outro femea", mostrando (a) por que ela nao pode ser VERTICAL, (b) por que
no rim ela fecha, (c) as tres maneiras de faze-la corrida e o que cada uma
custa. Nao gera solido.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
import numpy as np

TINTA, LINHA = "#1f2328", "#3d444d"
PECA, PECA2 = "#e8e2d9", "#cfd6dd"
NOVO, CINZA = "#c2410c", "#6b7280"
ROSA, FORTE, FUNDO = "#f8ddcd", "#ef7c3a", "#fbfaf8"
T = np.tan(np.radians(3.5))

fig = plt.figure(figsize=(16.4, 11.0), facecolor=FUNDO)
fig.text(0.5, 0.975, "Canaleta de ponta a ponta — onde ela cabe e onde não cabe",
         ha="center", va="top", fontsize=20, color=TINTA, weight="bold")
fig.text(0.5, 0.948, "Proposta para validação · 17/09/2026 · cotas em mm · saída de 3,5°/lado",
         ha="center", va="top", fontsize=11.5, color=LINHA)


def eixo(rect, num, tit, sub=""):
    ax = fig.add_axes(rect); ax.set_facecolor("white")
    for s in ax.spines.values():
        s.set_color("#e3e0da"); s.set_linewidth(1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.text(0, 1.082, f"{num} · {tit}", transform=ax.transAxes, fontsize=13,
            color=TINTA, weight="bold", va="bottom")
    if sub:
        ax.text(0, 1.022, sub, transform=ax.transAxes, fontsize=9.5,
                color=CINZA, va="bottom")
    return ax


# ======== 1 - VERTICAL NAO FECHA ==========================================
ax = eixo([0.042, 0.565, 0.258, 0.30], "1", "Vertical não fecha",
          "a conicidade abre a lateral de 0 a 15,9 mm")
ax.set_xlim(-108, 156); ax.set_ylim(-46, 150)
ax.add_patch(Polygon([(0, 0), (8, 130), (-30, 130), (-38, 0)], closed=True,
                     facecolor=PECA, edgecolor=LINHA, lw=1.4))
ax.add_patch(Polygon([(16, 0), (8, 130), (46, 130), (54, 0)], closed=True,
                     facecolor=PECA2, edgecolor=LINHA, lw=1.4))
# a cunha que uma canaleta vertical precisaria ser
ax.add_patch(Polygon([(8, 130), (8, 0), (0, 0)], closed=True, facecolor=FORTE,
                     edgecolor=NOVO, lw=1.3, alpha=.85))
ax.annotate("a canaleta\nvertical vira\nesta CUNHA:\n0 no topo,\n7,95 na base",
            (5, 46), (-104, 70), fontsize=8.8, color=NOVO, ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=NOVO, lw=.9))
ax.annotate("", (0, 6), (16, 6), arrowprops=dict(arrowstyle="<->", color=LINHA, lw=1.3))
ax.text(8, -4, "15,9", fontsize=9, color=LINHA, ha="center", va="top")
ax.text(64, 128, "e a cunha mata o encaixe:", fontsize=9.6, color=TINTA,
        weight="bold", va="top")
ax.text(64, 110, "ela chega a 215 mm de\nlargura já na base, e a\nboca tem 208,6 mm\n"
        "por dentro. A peça não\nentra mais na de baixo —\nprofundidade de\nencaixe = ZERO.",
        fontsize=8.8, color=TINTA, va="top")
ax.text(64, 24, "10 peças:\n601 → 1.300 mm\n(+116% de caixa)",
        fontsize=9.2, color=NOVO, va="top", weight="bold")

# ======== 2 - NO RIM FECHA ================================================
ax = eixo([0.345, 0.565, 0.258, 0.30], "2", "No rim ela fecha",
          "é lá que a fresta vale zero — por isso a canaleta é horizontal")
ax.set_xlim(-42, 130); ax.set_ylim(-42, 142)
K = 4.0    # afastamento exagerado, senao nao se ve
ax.add_patch(Rectangle((-16, 113), 32, 17, facecolor=ROSA, edgecolor="none", zorder=0))
for sx, cor in ((-1, PECA), (1, PECA2)):
    def fx(z, sx=sx):
        return sx * (130 - z) * T * K
    ax.add_patch(Polygon([(fx(0), 0), (fx(130), 130), (fx(130) + sx * 3.2, 130),
                          (fx(0) + sx * 3.2, 0)], closed=True, facecolor=cor,
                         edgecolor=LINHA, lw=1.4, zorder=2))
ax.plot([-16, 16], [113, 113], color=NOVO, lw=1.2, zorder=1)
ax.plot([-16, 16], [130, 130], color=NOVO, lw=1.2, zorder=1)
ax.text(-40, 136, "faixa da canaleta: 17 mm sob o rim", fontsize=9, color=NOVO,
        ha="left", va="center")
for z, cor in ((130, NOVO), (113, NOVO), (65, TINTA), (0, TINTA)):
    g = 2 * (130 - z) * T
    ax.annotate("", (-g / 2 * K, z), (g / 2 * K, z), arrowprops=dict(
        arrowstyle="<->" if g > 1.5 else "-", color=cor, lw=1.1, shrinkA=0,
        shrinkB=0), zorder=3)
    ax.text(34, z, f"z {z:3d}   fresta {g:5.2f}", fontsize=9.4, color=cor,
            family="monospace", va="center")
ax.text(-40, -18, "A canaleta inteira vive dentro de 2,08 mm de",
        fontsize=9, color=TINTA, va="center")
ax.text(-40, -28, "divergência. Na base são 15,90 — daí ela ser horizontal.",
        fontsize=9, color=TINTA, va="center")
ax.text(-40, -38, "afastamento desenhado em escala 4×", fontsize=8.4,
        color=CINZA, va="center")

# ======== 3 - SECAO DA TRAVA ==============================================
ax = eixo([0.648, 0.565, 0.31, 0.30], "3", "A trava, em seção",
          "a aba de A atravessa a janela de B e engancha por dentro")
ax.set_xlim(-30, 52); ax.set_ylim(88, 143)
# peca A (esquerda): parede + aba + gancho
ax.add_patch(Polygon([(-(130 - 98) * T, 98), (0, 130), (-3.2, 130),
                      (-(130 - 98) * T - 3.2, 98)], closed=True, facecolor=PECA,
                     edgecolor=LINHA, lw=1.4))
ax.add_patch(Polygon([(0, 113), (6, 113), (6, 130), (0, 130)], closed=True,
                     facecolor=ROSA, edgecolor=NOVO, lw=1.7))
ax.add_patch(Polygon([(3.6, 107), (6, 107), (6, 113), (3.6, 113)], closed=True,
                     facecolor=FORTE, edgecolor=NOVO, lw=1.7))
# peca B (direita): parede so ate 113 nesta secao -- acima e a janela
ax.add_patch(Polygon([((130 - 98) * T, 98), (2.08 / 2, 113), (2.08 / 2 + 3.2, 113),
                      ((130 - 98) * T + 3.2, 98)], closed=True, facecolor=PECA2,
                     edgecolor=LINHA, lw=1.4))
ax.add_patch(Rectangle((1.04, 113), 3.2, 17, facecolor="none", edgecolor=NOVO,
                       lw=1.2, ls=(0, (3, 2))))
ax.text(-14, 139, "peça A", fontsize=9.6, color=TINTA, ha="center", weight="bold")
ax.text(26, 139, "peça B", fontsize=9.6, color=TINTA, ha="center", weight="bold")
ax.annotate("janela: 42 x 17,\naberta no topo do rim", (4.2, 124), (14, 130),
            fontsize=8.6, color=NOVO, ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=NOVO, lw=.9))
ax.annotate("ressalto = a própria\nparede de B, 3,2 mm.\nO gancho para aqui.",
            (4.5, 110), (14, 103), fontsize=8.6, color=NOVO, ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=NOVO, lw=.9))
ax.annotate("aba de 6,\ntopo rasante\nao rim", (2.5, 127), (-28, 121), fontsize=8.6,
            color=NOVO, ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=NOVO, lw=.9))
ax.annotate("", (-14, 128), (-14, 136), arrowprops=dict(arrowstyle="->", color=NOVO, lw=2))
ax.text(-16, 132, "desce", fontsize=8.8, color=NOVO, ha="right", va="center")
ax.text(-28, 92, "os rims se encostam · para soltar, levanta 6 mm",
        fontsize=9, color=NOVO, va="center")

# ======== 4 - PONTA A PONTA, VISTA LATERAL ================================
ax = eixo([0.042, 0.075, 0.555, 0.355], "4",
          "Ponta a ponta — as duas laterais da mesma peça",
          "a canaleta corre os 148 mm da lateral; as travas moram dentro dela")
ax.set_aspect("equal")
ax.set_xlim(-24, 466); ax.set_ylim(-62, 152)
SIL = [(200, 0), (200, 130), (52, 130), (0, 78), (0, 36), (36, 0)]
for ox, lado, cor in ((0, "DIREITA — macho", PECA), (250, "ESQUERDA — fêmea", PECA2)):
    ax.add_patch(Polygon([(x + ox, z) for x, z in SIL], closed=True,
                         facecolor=cor, edgecolor=LINHA, lw=1.5))
    # a canaleta: risco corrido de ponta a ponta
    ax.plot([52 + ox, 200 + ox], [113, 113], color=NOVO, lw=1.6)
    ax.plot([52 + ox, 200 + ox], [130, 130], color=NOVO, lw=1.0, ls=(0, (4, 3)))
    ax.text(ox + 126, 142, lado, fontsize=10.5, color=TINTA, ha="center", weight="bold")
    for x0 in (76, 136):
        if ox == 0:
            ax.add_patch(Rectangle((x0 + ox, 113), 40, 17, facecolor=ROSA,
                                   edgecolor=NOVO, lw=1.5))
            ax.add_patch(Rectangle((x0 + ox, 107), 40, 6, facecolor=FORTE,
                                   edgecolor=NOVO, lw=1.5))
        else:
            ax.add_patch(Rectangle((x0 - 1 + ox, 113), 42, 17, facecolor="white",
                                   edgecolor=NOVO, lw=1.5))
    for x0 in (56, 180):   # bercos de empilhamento, nos cantos
        ax.add_patch(Rectangle((x0 + ox, 120), 18, 10, facecolor="#dfe7ee",
                               edgecolor=CINZA, lw=1))
ax.annotate("", (52, -14), (200, -14), arrowprops=dict(
    arrowstyle="<->", color=NOVO, lw=1.2, shrinkA=0, shrinkB=0))
ax.text(126, -18, "148 — a lateral inteira, do fundo ao início do chanfro",
        fontsize=9, color=NOVO, ha="center", va="top")
ax.text(0, -40, "2 abas de 40 × 17 com gancho de 6", fontsize=9, color=NOVO, va="center")
ax.text(250, -40, "2 janelas de 42 × 17", fontsize=9, color=NOVO, va="center")
ax.text(0, -54, "berços de empilhamento migram para os cantos (cinza), fora das travas",
        fontsize=8.8, color=CINZA, va="center")
ax.text(126, 60, "frente ←", fontsize=9, color=CINZA, ha="center")
ax.text(376, 60, "frente ←", fontsize=9, color=CINZA, ha="center")

# ======== 5 - AS TRES MANEIRAS ============================================
bx = fig.add_axes([0.632, 0.075, 0.326, 0.355]); bx.axis("off")
bx.set_xlim(0, 1); bx.set_ylim(0, 1)
bx.add_patch(Rectangle((0, 0), 1, 1, transform=bx.transAxes, facecolor="#fdf6f1",
                       edgecolor="#f0d3c2", lw=1.3))
bx.text(0.05, 0.945, "AS TRÊS MANEIRAS DE FAZER A CANALETA",
        fontsize=11.5, color=NOVO, weight="bold", va="top")
itens = [
 ("A · trilho\ncorrido",
  "Trilho saliente de ponta a ponta de um lado, e do outro o\n"
  "rim REBAIXADO 17 mm nos mesmos 148 mm para recebê-lo.\n"
  "Trava na extensão toda, sem gaveta. Custa: a peça sozinha\n"
  "fica com um lado 17 mm mais baixo — assimetria visível.", TINTA),
 ("B · trilho\nembutido",
  "Trilho corrido de um lado, canaleta corrida do outro, rims\n"
  "encostados, simétrico — é o mais bonito e o mais rígido.\n"
  "Custa: uma canaleta horizontal é rebaixo, então exige\n"
  "2 GAVETAS laterais (~USD 3 mil e linha de junta na lateral).", TINTA),
 ("C · canaleta\naparente\n(recomendo)",
  "O risco da canaleta corre os 148 mm nas duas laterais e\n"
  "fecha a leitura; quem trava são 2 abas de um lado e 2\n"
  "janelas do outro, dentro dela. Rims encostados, simétrico,\n"
  "sem gaveta, +4,3 g (163,7 → 168,0 g).", TINTA),
]
y = 0.855
for t, c, cor in itens:
    bx.text(0.05, y, t, fontsize=9.3, color=NOVO, weight="bold", va="top")
    bx.text(0.27, y, c, fontsize=9.1, color=cor, va="top")
    y -= 0.232
bx.plot([0.05, 0.95], [0.175, 0.175], color="#f0d3c2", lw=1)
bx.text(0.05, 0.152, "Por que fica bonito: o risco horizontal sob o rim dá à peça uma linha\n"
        "só, contrapõe o pontilhado dos furos e amarra no chanfro de 45°. Acopladas,\n"
        "a linha atravessa as duas peças e a junta lê como projeto, não como sobra.",
        fontsize=8.5, color=CINZA, va="top")
fig.savefig("/home/user/produtos/cesto-empilhavel/cad/proposta-canaleta.png",
            dpi=132, facecolor=FUNDO)
print("ok")
