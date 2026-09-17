#!/usr/bin/env python3
"""Proposta de acoplamento no RIM -- desenho de validacao (nao gera solido).

Responde a pergunta "melhorando o angulo esse problema e resolvido?" e
propoe onde o macho e a femea devem morar para que a LATERAL FIQUE LISA e o
encaixe TRAVE (nao solte com tracao lateral).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

TINTA, LINHA = "#1f2328", "#3d444d"
PECA, PECA2 = "#e8e2d9", "#cfd6dd"
NOVO, CINZA = "#c2410c", "#6b7280"
ROSA, FUNDO = "#f8ddcd", "#fbfaf8"

fig = plt.figure(figsize=(15.8, 10.2), facecolor=FUNDO)
fig.text(0.5, 0.974, "Acoplamento no RIM — lateral lisa, encaixe que trava",
         ha="center", va="top", fontsize=19.5, color=TINTA, weight="bold")
fig.text(0.5, 0.945, "Proposta revisada para validação · 17/09/2026 · cotas em mm",
         ha="center", va="top", fontsize=11.5, color=LINHA)


def eixo(rect, num, tit, sub=""):
    ax = fig.add_axes(rect); ax.set_facecolor("white")
    for s in ax.spines.values():
        s.set_color("#e3e0da"); s.set_linewidth(1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.text(0, 1.075, f"{num} · {tit}", transform=ax.transAxes, fontsize=13,
            color=TINTA, weight="bold", va="bottom")
    if sub:
        ax.text(0, 1.018, sub, transform=ax.transAxes, fontsize=9.6,
                color=CINZA, va="bottom")
    return ax


def cota(ax, p0, p1, txt, d=0, vert=False, fs=8.8):
    x0, y0 = p0; x1, y1 = p1
    if vert:
        x = x0 + d
        ax.annotate("", (x, y0), (x, y1), arrowprops=dict(
            arrowstyle="<->", color=NOVO, lw=1, shrinkA=0, shrinkB=0))
        ax.text(x + (1.0 if d >= 0 else -1.0), (y0 + y1) / 2, txt, fontsize=fs,
                color=NOVO, ha="left" if d >= 0 else "right", va="center")
    else:
        y = y0 + d
        ax.annotate("", (x0, y), (x1, y), arrowprops=dict(
            arrowstyle="<->", color=NOVO, lw=1, shrinkA=0, shrinkB=0))
        ax.text((x0 + x1) / 2, y + (0.9 if d >= 0 else -0.9), txt, fontsize=fs,
                color=NOVO, ha="center", va="bottom" if d >= 0 else "top")


# ---------- 1 - POR QUE NAO NA FACE LATERAL --------------------------------
ax = eixo([0.045, 0.555, 0.265, 0.315], "1", "Por que não na face lateral",
          "a conicidade abre uma fresta — e reduzi-la mata o encaixe")
ax.set_xlim(-46, 158); ax.set_ylim(-34, 172)
ax.add_patch(Polygon([(0, 0), (8, 130), (-30, 130), (-38, 0)], closed=True,
                     facecolor=PECA, edgecolor=LINHA, lw=1.4))
ax.add_patch(Polygon([(16, 0), (8, 130), (46, 130), (54, 0)], closed=True,
                     facecolor=PECA2, edgecolor=LINHA, lw=1.4))
ax.plot([8, 8], [130, 146], color=NOVO, lw=1.2)
ax.annotate("", (0, 5), (16, 5), arrowprops=dict(arrowstyle="<->", color=NOVO, lw=1.4))
ax.text(8, -6, "fresta de 15,9 mm\nna base", fontsize=9.2, color=NOVO,
        ha="center", va="top")
ax.text(8, 150, "as peças se tocam\nsó aqui, no rim", fontsize=9, color=NOVO,
        ha="center", va="bottom")
ax.text(74, 136, "saída   fresta  passo  10 pç", fontsize=8.4, color=TINTA,
        family="monospace", va="top")
for i, row in enumerate([("3,5° (hoje)", "15,9", "52", "601"),
                         ("2,5°", "11,3", "73", "790"),
                         ("2,0°", "9,1", "92", "954")]):
    a, b, c, d = row
    ax.text(74, 120 - i * 15, f"{a:<12}{b:>5}{c:>7}{d:>7}", fontsize=8.4,
            color=NOVO if i == 0 else CINZA, family="monospace", va="top")
ax.text(74, 62, "cortar a fresta em 43%\nfaz a pilha de 10 peças\nencaixadas crescer 59%\n"
        "— e a 1,5° o encaixe\nsimplesmente morre",
        fontsize=9, color=TINTA, va="top")

# ---------- 2 - SECAO DO RIM ----------------------------------------------
ax = eixo([0.355, 0.555, 0.285, 0.315], "2", "Macho e fêmea no rim — seção",
          "no único lugar onde as duas peças já se tocam")
ax.set_xlim(-26, 86); ax.set_ylim(-40, 36)
# peca A -- macho
ax.add_patch(Polygon([(-3.2, -30), (0, -30), (0, 12), (-3.2, 12)], closed=True,
                     facecolor=PECA, edgecolor=LINHA, lw=1.4))
ax.add_patch(Polygon([(0, 5), (7, 5), (7, 12), (0, 12)], closed=True,
                     facecolor=ROSA, edgecolor=NOVO, lw=1.7))
ax.add_patch(Polygon([(4, 0), (7, 0), (7, 5), (4, 5)], closed=True,
                     facecolor=ROSA, edgecolor=NOVO, lw=1.7))
ax.text(2, 22, "peça A  ·  MACHO", fontsize=10, color=TINTA, ha="center", weight="bold")
cota(ax, (0, 12), (7, 12), "7", d=3.5)
cota(ax, (7, 0), (7, 12), "12", d=4.5, vert=True)
ax.annotate("gancho de 3", (5.5, 0), (18, -12), fontsize=8.6, color=NOVO,
            ha="left", va="center", arrowprops=dict(arrowstyle="-", color=NOVO, lw=.9))
ax.text(2, -34, "aba no rim com\nGANCHO PARA BAIXO", fontsize=8.8, color=NOVO,
        ha="center", va="top")
# peca B -- femea
ax.add_patch(Polygon([(46, -30), (49.2, -30), (49.2, 6), (46, 6)], closed=True,
                     facecolor=PECA2, edgecolor=LINHA, lw=1.4))
ax.add_patch(Rectangle((46, 6), 3.2, 6, facecolor="white", edgecolor=NOVO,
                       lw=1.4, ls=(0, (3, 2))))
ax.text(56, 22, "peça B  ·  FÊMEA", fontsize=10, color=TINTA, ha="center", weight="bold")
ax.annotate("rasgo\n6 x 34", (49.2, 9), (64, 14), fontsize=8.6, color=NOVO,
            ha="left", va="center", arrowprops=dict(arrowstyle="-", color=NOVO, lw=.9))
ax.annotate("ressalto: é ele\nque o gancho\nagarra", (49.2, 3), (64, -6),
            fontsize=8.6, color=NOVO, ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=NOVO, lw=.9))
ax.text(47.6, -34, "rasgo no rim com\nRESSALTO EMBAIXO", fontsize=8.8, color=NOVO,
        ha="center", va="top")
ax.text(-24, -30, "a PAREDE\nnão é tocada", fontsize=9, color=NOVO,
        ha="left", va="bottom")

# ---------- 3 - PLANTA DO RIM ---------------------------------------------
ax = eixo([0.685, 0.555, 0.27, 0.315], "3", "Planta do rim — hermafrodita",
          "direita e esquerda espelhadas: qualquer peça acopla em qualquer peça")
ax.set_xlim(-72, 292); ax.set_ylim(-34, 238)
ax.add_patch(Rectangle((0, 0), 215, 200, facecolor="none", edgecolor=LINHA, lw=1.6))
ax.add_patch(Rectangle((6, 6), 203, 188, facecolor=PECA, edgecolor="#cfcabf", lw=.9))
for x, y, t in [(215, 60, "M"), (215, 140, "F"), (0, 60, "F"), (0, 140, "M")]:
    if t == "M":
        ax.add_patch(Rectangle((x if x > 0 else -7, y - 17), 7, 34,
                               facecolor=ROSA, edgecolor=NOVO, lw=1.4))
    else:
        ax.add_patch(Rectangle((x - 6 if x > 0 else 0, y - 18), 6, 36,
                               facecolor="white", edgecolor=NOVO, lw=1.4))
    ax.text(x + (34 if x > 0 else -34), y, "macho" if t == "M" else "fêmea",
            fontsize=8.6, color=NOVO, ha="center", va="center", weight="bold")
ax.text(107, 214, "↑ frente", fontsize=9, color=CINZA, ha="center")
ax.text(107, 100, "as quatro feições\nvivem só no rim —\na lateral inteira\nfica lisa",
        fontsize=9.6, color=TINTA, ha="center", va="center")

# ---------- 4 - COMO TRAVA -------------------------------------------------
ax = eixo([0.045, 0.075, 0.455, 0.345], "4", "Como trava — encosta, desce, travou",
          "é o gancho passando por baixo do ressalto: tração lateral não solta")
ax.set_xlim(-24, 132); ax.set_ylim(-44, 40)


def par(ax, ox, off, cap, hi=False):
    """Desenha o par macho/femea deslocado 'off' em z, na origem ox."""
    # peca B (femea) fixa
    ax.add_patch(Polygon([(ox, -34), (ox + 3.2, -34), (ox + 3.2, 6), (ox, 6)],
                         closed=True, facecolor=PECA2, edgecolor=LINHA, lw=1.4))
    ax.add_patch(Rectangle((ox, 6), 3.2, 6, facecolor="white", edgecolor=NOVO,
                           lw=1.2, ls=(0, (3, 2))))
    ax.plot([ox, ox + 3.2], [12, 12], color=LINHA, lw=.8, ls=(0, (2, 2)))
    # peca A (macho) na cota off
    ax.add_patch(Polygon([(ox - 3.2, -34 + off), (ox, -34 + off), (ox, 12 + off),
                          (ox - 3.2, 12 + off)], closed=True, facecolor=PECA,
                         edgecolor=LINHA, lw=1.4))
    ax.add_patch(Polygon([(ox, 5 + off), (ox + 7, 5 + off), (ox + 7, 12 + off),
                          (ox, 12 + off)], closed=True, facecolor=ROSA,
                         edgecolor=NOVO, lw=1.6))
    ax.add_patch(Polygon([(ox + 4, off), (ox + 7, off), (ox + 7, 5 + off),
                          (ox + 4, 5 + off)], closed=True,
                         facecolor="#ef7c3a" if hi else ROSA, edgecolor=NOVO, lw=1.6))
    ax.text(ox + 1.6, -38, cap, fontsize=9, color=TINTA, ha="center", va="top")


par(ax, 4, 9, "1 · encosta com a peça\n7 mm mais alta")
ax.annotate("", (14, 9), (14, 20), arrowprops=dict(arrowstyle="->", color=NOVO, lw=2))
par(ax, 48, 4, "2 · desce: a aba entra\npelo rasgo")
ax.annotate("", (58, 4), (58, 15), arrowprops=dict(arrowstyle="->", color=NOVO, lw=2))
par(ax, 96, 0, "3 · TRAVOU: o gancho\nestá sob o ressalto", hi=True)
ax.annotate("", (78, -16), (91, -16), arrowprops=dict(arrowstyle="->", color=NOVO, lw=2))
ax.text(84.5, -13, "puxa e não sai", fontsize=8.8, color=NOVO, ha="center", va="bottom")
ax.text(4, 34, "para separar, levanta 7 mm — nunca por tração lateral",
        fontsize=9.2, color=NOVO, va="center")

# ---------- 5 - CUSTO / ALTERNATIVA ---------------------------------------
bx = fig.add_axes([0.535, 0.075, 0.42, 0.345]); bx.axis("off")
bx.set_xlim(0, 1); bx.set_ylim(0, 1)
bx.add_patch(Rectangle((0, 0), 1, 1, transform=bx.transAxes, facecolor="#fdf6f1",
                       edgecolor="#f0d3c2", lw=1.3))
bx.text(0.045, 0.935, "O QUE ISSO CUSTA — E A ALTERNATIVA", fontsize=11.5,
        color=NOVO, weight="bold", va="top")
txt = [
    ("Ganha", "A parede lateral fica intacta: lisa, cônica, sem chapado\n"
              "nem rebaixo. O encaixe vai para onde as duas peças\n"
              "já se tocam de verdade.", TINTA),
    ("Custa", "Uma aba de 7 × 34 × 12 mm no rim, de cada lado — cerca\n"
              "de 3,6 g. Some da face, mas aparece no perfil do rim:\n"
              "é o mínimo possível para uma peça invadir a outra.", TINTA),
    ("Molde", "Não muda de classe. A aba e o rasgo saem na direção de\n"
              "abertura, sem gaveta — o rasgo é shut-off entre macho\n"
              "e cavidade, igual aos furos.", TINTA),
    ("Se a aba\nincomodar", "Alternativa: os dois lados só com o rasgo (rim perfeitamente\n"
              "limpo) e um CLIPE separado unindo as peças. Some tudo da\n"
              "peça, mas custa um 2º molde (~USD 4 mil) e uma peça a\n"
              "mais na embalagem.", CINZA),
]
y = 0.825
for t, c, cor in txt:
    bx.text(0.045, y, t, fontsize=9.4, color=NOVO, weight="bold", va="top")
    bx.text(0.215, y, c, fontsize=9.2, color=cor, va="top")
    y -= 0.205
fig.savefig("/home/user/produtos/cesto-empilhavel/cad/proposta-rim.png",
            dpi=135, facecolor=FUNDO)
print("ok")
