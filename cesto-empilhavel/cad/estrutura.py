#!/usr/bin/env python3
"""Estrutura de empilhamento na borda -- a ideia do cliente, em 3D.

Parede que sai da borda superior (por fora do rim) + nervura externa com pe na
diagonal. Mesma orientacao EMPILHA a 130 mm; girada 180 ENCAIXA. As duas coisas
na mesma peca, sem rasgo no fundo e sem gaveta.
"""
import os
import textwrap

import numpy as np
import trimesh
from build123d import Box, Pos, Rot, export_step, export_stl

import modelo3d as M
import render
from empilha import passo

DEST = os.path.dirname(os.path.abspath(__file__))
COR, COR2 = (0.93, 0.44, 0.13), (0.72, 0.30, 0.08)
CINZ = (0.55, 0.63, 0.72)
FUNDO, TINTA, GRIS, NOVO, VERDE = "#fbfaf8", "#1f2328", "#6b7280", "#c2410c", "#15803d"


def gira(m):
    t = m.copy()
    t.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [0, 0, 1]))
    return t


def main():
    p, n = M.cesto("D", estrutura=True)
    export_step(p, os.path.join(DEST, "cesto-final.step"))
    export_stl(p, os.path.join(DEST, "cesto-final.stl"))
    m = trimesh.load(os.path.join(DEST, "cesto-final.stl"))
    pe, pg = passo(p), passo(p, True)
    peso = p.volume * M.RHO
    print(f"peso {peso:.1f} g | empilhado {pe:.1f} mm | encaixado {pg:.1f} mm")

    # pilha: mesma orientacao
    cena = []
    for i in range(3):
        t = m.copy(); t.apply_translation([0, 0, i * pe])
        cena.append((t, COR if i % 2 == 0 else COR2))
    render.salvar(render.render(cena, direcao=(-1.0, -1.25, -0.52), largura=1000),
                  os.path.join(DEST, "fin-pilha.png"))
    # coluna encaixada: girando 180 a cada peca
    cena = []
    for i in range(5):
        t = (gira(m) if i % 2 else m.copy())
        t.apply_translation([0, 0, i * pg])
        cena.append((t, COR if i % 2 == 0 else COR2))
    render.salvar(render.render(cena, direcao=(-1.0, -1.25, -0.52), largura=1000),
                  os.path.join(DEST, "fin-encaixe.png"))
    # a peca sozinha e o detalhe da borda
    render.salvar(render.render([(m, COR)], direcao=(-0.85, -1.15, -0.62),
                                largura=1000),
                  os.path.join(DEST, "fin-peca.png"))
    y0, y1 = M.EMP_Y[1]
    bloco = Pos(100.0, (y0 + y1) / 2, 132.0) * Box(46.0, y1 - y0 + 40.0, 56.0)
    sa, sb = p & bloco, (Pos(0, 0, pe) * p) & bloco
    export_stl(sa, os.path.join(DEST, "fin-sa.stl"))
    export_stl(sb, os.path.join(DEST, "fin-sb.stl"))
    render.salvar(render.render(
        [(trimesh.load(os.path.join(DEST, "fin-sa.stl")), COR),
         (trimesh.load(os.path.join(DEST, "fin-sb.stl")), CINZ)],
        direcao=(0.9, -1.0, -0.35), largura=1000),
        os.path.join(DEST, "fin-det.png"))
    folha(dict(peso=peso, pe=pe, pg=pg, furos=n))


def imagem(fig, rect, arq, titulo=None, sub=None):
    from PIL import Image
    ax = fig.add_axes(rect)
    ax.imshow(np.asarray(Image.open(os.path.join(DEST, arq))))
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#e3e0da")
    if titulo:
        ax.set_title(titulo, fontsize=12.5, color=TINTA, weight="bold", pad=6)
    if sub:
        ax.text(0.5, -0.03, sub, transform=ax.transAxes, ha="center", va="top",
                fontsize=9.4, color=GRIS)


def folha(d):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig = plt.figure(figsize=(16.4, 11.4), facecolor=FUNDO)
    fig.text(0.5, 0.982, "A sua ideia funciona: empilha E encaixa",
             ha="center", va="top", fontsize=21.5, color=TINTA, weight="bold")
    fig.text(0.5, 0.957, "parede na borda superior + nervura externa com pé na "
             "diagonal · medido no sólido", ha="center", va="top",
             fontsize=11.5, color="#3d444d")
    imagem(fig, [0.022, 0.545, 0.30, 0.335], "fin-peca.png", "a peça",
           "4 paredes na borda e 4 nervuras, 2 por lateral")
    imagem(fig, [0.345, 0.545, 0.30, 0.335], "fin-det.png",
           "o pé na diagonal sobre a parede",
           "corte: a nervura de cima (cinza) apoia na parede da de baixo")
    bx = fig.add_axes([0.668, 0.545, 0.30, 0.335]); bx.axis("off")
    bx.set_xlim(0, 1); bx.set_ylim(0, 1)
    bx.add_patch(Rectangle((0, 0), 1, 1, transform=bx.transAxes,
                           facecolor="#f2f7f2", edgecolor="#cfe0cf", lw=1.3))
    bx.text(0.06, 0.95, "POR QUE FUNCIONA", fontsize=11.5, color=VERDE,
            weight="bold", va="top")
    y = 0.84
    for par in ("Eu tinha posto os berços POR DENTRO do rim, no caminho da peça "
                "de cima. A sua estrutura mora na borda, por fora — e ali a "
                "peça de cima não passa.",
                "Girada 180°, as nervuras se desviam das paredes (as posições "
                "em y são assimétricas) e a peça encaixa. Na mesma orientação "
                "elas se encontram e a peça empilha.",
                "Sem rasgo no fundo, sem gaveta, e a nervura nunca passa dos "
                "107,5 mm da boca — invisível em planta."):
        bx.text(0.06, y, "\n".join(textwrap.wrap(par, 41)), fontsize=9.3,
                color=TINTA, va="top", linespacing=1.5)
        y -= 0.055 + 0.041 * len(textwrap.wrap(par, 41))

    imagem(fig, [0.022, 0.135, 0.30, 0.335], "fin-pilha.png",
           f"EMPILHADA · {d['pe']:.0f} mm", "mesma orientação, chanfro sempre "
           "na frente")
    imagem(fig, [0.345, 0.135, 0.30, 0.335], "fin-encaixe.png",
           f"ENCAIXADA · {d['pg']:.1f} mm".replace(".", ","),
           "girando 180° a cada peça, só na caixa")
    tb = fig.add_axes([0.668, 0.135, 0.30, 0.335]); tb.axis("off")
    tb.set_xlim(0, 1); tb.set_ylim(0, 1)
    tb.add_patch(Rectangle((0, 0), 1, 1, transform=tb.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.3))
    tb.text(0.06, 0.95, "O QUE CUSTA", fontsize=11.5, color=NOVO,
            weight="bold", va="top")
    linhas = [("empilhado", f"{d['pe']:.0f} mm"),
              ("encaixado", f"{d['pg']:.1f} mm".replace(".", ",")),
              ("10 peças na caixa", f"{130 + 9*d['pg']:.0f} mm"),
              ("peso", f"{d['peso']:.1f} g".replace(".", ",")),
              ("capacidade", "4,46 L"),
              ("envelope", "216,8 × 197 × 140 mm")]
    y = 0.82
    for k, v in linhas:
        tb.text(0.06, y, k, fontsize=9.6, color=GRIS, va="center")
        tb.text(0.94, y, v, fontsize=9.6, color=TINTA, va="center",
                ha="right", weight="bold")
        y -= 0.083
    tb.plot([0.06, 0.94], [0.30, 0.30], color="#f0d3c2", lw=1)
    tb.text(0.06, 0.255, "\n".join(textwrap.wrap(
        "O encaixe cai de 55,5 para 102,7 mm: cada milímetro que avança para "
        "fora na peça de cima custa 16,3 mm de profundidade de encaixe, e o "
        "apoio precisa de uns 4. É o preço de ter os dois modos.", 44)),
        fontsize=9.2, color=NOVO, va="top", linespacing=1.5)
    fig.savefig(os.path.join(DEST, "estrutura.png"), dpi=118, facecolor=FUNDO)
    print("gerado estrutura.png")


if __name__ == "__main__":
    main()
