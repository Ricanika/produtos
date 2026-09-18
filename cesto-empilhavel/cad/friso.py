#!/usr/bin/env python3
"""O friso na aba: a paredinha em U onde o pe de tras da peca de cima pousa."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from build123d import Box, Pos, export_stl
from PIL import Image

import modelo3d as M
import render

DEST = os.path.dirname(os.path.abspath(__file__))
FUNDO, TINTA, GRIS, NOVO = "#fbfaf8", "#1f2328", "#6b7280", "#c2410c"
COR, CINZ = (0.93, 0.44, 0.13), (0.55, 0.63, 0.72)


def main():
    M.set_draft(12.0)
    p, _ = M.cesto(aba=True)
    yr = M.PES[1][0]
    cx = Pos(96.0, yr + M.DESLOC, 128.0) * Box(40.0, 44.0, 28.0)
    export_stl(p & cx, os.path.join(DEST, "fr-a.stl"))
    export_stl((Pos(0, M.DESLOC, 130.0) * p) & cx, os.path.join(DEST, "fr-b.stl"))
    ma = trimesh.load(os.path.join(DEST, "fr-a.stl"))
    mb = trimesh.load(os.path.join(DEST, "fr-b.stl"))
    render.salvar(render.render([(ma, CINZ)], direcao=(-0.6, -0.8, -1.0),
                                largura=980),
                  os.path.join(DEST, "friso-so.png"))
    render.salvar(render.render([(ma, CINZ), (mb, COR)],
                                direcao=(-0.75, -0.9, -0.85), largura=980),
                  os.path.join(DEST, "friso-det.png"))

    # trava medida: empurra a peca de cima nos quatro sentidos
    travas = []
    for nome, d in (("y +", (0, 1.0)), ("y −", (0, -1.0)),
                    ("x +", (1.0, 0)), ("x −", (-1.0, 0))):
        v = (p & (Pos(d[0], M.DESLOC + d[1], 130.0) * p)).volume
        travas.append((nome, v))

    fig = plt.figure(figsize=(13.0, 6.6), facecolor=FUNDO)
    fig.text(0.5, 0.975, "O friso na aba", ha="center", va="top",
             fontsize=19, color=TINTA, weight="bold")
    fig.text(0.5, 0.932, "uma paredinha em U de 2,5 mm de relevo, no lugar "
             "onde o pé de trás da peça de cima pousa", ha="center", va="top",
             fontsize=10.5, color=GRIS)
    for i, (arq, tit, sub) in enumerate((
            ("friso-so.png", "a aba, com o friso",
             "três pernas de 1,2 × 2,5 mm · o resto do rim continua plano"),
            ("friso-det.png", "o pé de trás pousado nele",
             "o piso do pé (laranja) encosta nas três pernas"))):
        ax = fig.add_axes([0.02 + i * 0.33, 0.10, 0.31, 0.74])
        ax.imshow(np.asarray(Image.open(os.path.join(DEST, arq))))
        ax.set_anchor("N"); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#e3e0da")
        ax.set_title(tit, fontsize=12, color=TINTA, weight="bold", pad=6)
        ax.text(0.5, -0.03, sub, transform=ax.transAxes, ha="center",
                va="top", fontsize=9.2, color=GRIS)

    tb = fig.add_axes([0.69, 0.10, 0.29, 0.74]); tb.axis("off")
    tb.set_xlim(0, 1); tb.set_ylim(0, 1)
    tb.text(0.0, 0.97, "O QUE ELE TRAVA", fontsize=11.5, color=NOVO,
            weight="bold", va="top")
    tb.text(0.0, 0.88, "empurrando a peça de cima 1 mm, medido no sólido:",
            fontsize=9.2, color=GRIS, va="top")
    y = 0.76
    for nome, v in travas:
        tb.text(0.04, y, nome, fontsize=9.6, color=GRIS, va="center")
        tb.text(0.96, y, f"{v:.1f} mm³".replace(".", ","), fontsize=9.6,
                color=TINTA, va="center", ha="right", weight="bold")
        y -= 0.07
    tb.plot([0.0, 0.2], [0.44, 0.44], color="#e3e0da", lw=1)
    tb.text(0.0, 0.40, "Os quatro sentidos travam a partir de 0,6 mm de "
            "folga. Antes era um pino só, que segurava apenas o sentido do "
            "encaixe.\n\nCusta zero no encaixe: a face interna do friso mora "
            "em x = 98,6 mm, para fora dos 98,1 mm onde a parede da peça "
            "encaixada passa pela cota do rim.", fontsize=9.0, color=TINTA,
            va="top", linespacing=1.55, wrap=True)
    fig.savefig(os.path.join(DEST, "friso.png"), dpi=125, facecolor=FUNDO)
    print("gerado friso.png")


if __name__ == "__main__":
    main()
