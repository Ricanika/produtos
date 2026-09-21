#!/usr/bin/env python3
"""Bolinhas -> listras verticais: mesma casca, mesmas curvas, menos peso.

E tambem onde o peso da peca realmente esta -- que nao e no vazado da parede.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from build123d import Box, Pos, export_stl
from matplotlib.patches import Rectangle
from PIL import Image

import modelo3d as M
import render

DEST = os.path.dirname(os.path.abspath(__file__))
FUNDO, TINTA, GRIS, NOVO = "#fbfaf8", "#1f2328", "#6b7280", "#c2410c"
COR = (0.93, 0.44, 0.13)
VISTA = (-1.0, -0.62, -0.5)


def build(vazado, arq):
    M.VAZADO = vazado
    p, n = M.cesto(aba=True)
    export_stl(p, os.path.join(DEST, arq))
    return p, n


def main():
    M.set_draft(12.0)
    out = {}
    for vazado, arq in (("bolinha", "lis-bol.stl"), ("listra", "lis-lis.stl")):
        p, n = build(vazado, arq)
        out[vazado] = (p, n, p.volume * M.RHO)
        m = trimesh.load(os.path.join(DEST, arq))
        render.salvar(render.render([(m, COR)], direcao=VISTA, largura=1020),
                      os.path.join(DEST, f"lis-{vazado}.png"))
    pb, nb, gb = out["bolinha"]
    pl, nl, gl = out["listra"]
    print(f"bolinha {gb:.1f} g ({nb}) | listra {gl:.1f} g ({nl})")

    # onde esta o peso, na versao com listras
    faixas = [("pés + saia", 0.0, M.H_PE),
              ("chapa do fundo", M.H_PE, M.H_PE + M.T_FUNDO),
              ("banda cega do pé", M.H_PE + M.T_FUNDO, M.BANDA),
              ("parede vazada", M.BANDA, M.Z_TOPO),
              ("faixa do rim + aba", M.Z_TOPO, 133.0)]
    peso = []
    for nome, z0, z1 in faixas:
        cx = Pos(0, 0, (z0 + z1) / 2) * Box(400, 400, z1 - z0)
        peso.append((nome, (pl & cx).volume * M.RHO))

    fig = plt.figure(figsize=(15.8, 7.0), facecolor=FUNDO)
    fig.text(0.5, 0.975, "Bolinhas → listras verticais", ha="center",
             va="top", fontsize=19, color=TINTA, weight="bold")
    fig.text(0.5, 0.934, f"mesma casca, mesmas curvas, mesma estrutura · "
             f"{gb:.1f} g → {gl:.1f} g ({gl - gb:+.1f} g, "
             f"{100 * (gl - gb) / gb:+.1f}%)".replace(".", ","), ha="center",
             va="top", fontsize=11, color=GRIS)
    for i, (arq, tit) in enumerate((("lis-bolinha.png", f"antes · {gb:.1f} g"),
                                    ("lis-listra.png", f"agora · {gl:.1f} g"))):
        ax = fig.add_axes([0.015 + i * 0.30, 0.09, 0.285, 0.76])
        ax.imshow(np.asarray(Image.open(os.path.join(DEST, arq))))
        ax.set_anchor("N"); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#e3e0da")
        ax.set_title(tit.replace(".", ","), fontsize=12.5, color=TINTA,
                     weight="bold", pad=6)

    bx = fig.add_axes([0.63, 0.09, 0.355, 0.76]); bx.axis("off")
    bx.set_xlim(0, 1); bx.set_ylim(0, 1)
    bx.add_patch(Rectangle((0, 0), 1, 1, transform=bx.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.3))
    bx.text(0.05, 0.96, "ONDE O PESO ESTÁ", fontsize=11.5, color=NOVO,
            weight="bold", va="top")
    y = 0.86
    tot = sum(g for _, g in peso)
    for nome, g in peso:
        bx.text(0.05, y, nome, fontsize=9.6, color=GRIS, va="center")
        bx.text(0.72, y, f"{g:.1f} g".replace(".", ","), fontsize=9.6,
                color=TINTA, va="center", ha="right", weight="bold")
        bx.text(0.95, y, f"{100 * g / tot:.0f}%", fontsize=9.6, color=GRIS,
                va="center", ha="right")
        y -= 0.075
    bx.plot([0.05, 0.95], [y + 0.03, y + 0.03], color="#f0d3c2", lw=1)
    bx.text(0.05, y - 0.02, "A parede vazada é só 26% da peça. Tirar 1 g dela "
            "custa caro; a chapa do fundo, que é 33%, está intacta — o vazado "
            "nunca chegou nela.\n\nMedido nas variantes de listra: o que pesa "
            "não é a largura nem o passo, é o NÚMERO DE FAIXAS. Cada faixa a "
            "mais é uma nervura horizontal dando a volta na peça: de 3 para 2 "
            "faixas saem 6,1 g. Largura de 9 para 11 mm rende 0,7 g.\n\nDuas "
            "faixas é o mínimo razoável: a nervura do meio é o que segura a "
            "parede contra embarrigar sob a pilha.",
            fontsize=9.0, color=TINTA, va="top", linespacing=1.5, wrap=True)
    fig.savefig(os.path.join(DEST, "listras.png"), dpi=125, facecolor=FUNDO)
    print("gerado listras.png")


if __name__ == "__main__":
    main()
