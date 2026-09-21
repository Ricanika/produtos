#!/usr/bin/env python3
"""A rodada de acabamento: saia de tras invisivel e pes da frente redondos."""
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
COR = (0.93, 0.44, 0.13)


def main():
    M.set_draft(12.0)
    p, _ = M.cesto(aba=True)
    m = trimesh.load(os.path.join(DEST, "cesto-aba.stl"))
    yc = M.PES[0][0]
    # o pe visto de fora e a planta dele
    cx = Pos(80.0, yc, 30.0) * Box(60.0, 60.0, 70.0)
    export_stl(p & cx, os.path.join(DEST, "lp-pe.stl"))
    laje = Pos(80.0, yc, 12.0) * Box(60.0, 60.0, 3.0)
    export_stl(p & laje, os.path.join(DEST, "lp-pl.stl"))

    vistas = [
        ("lp-tras.png", [(m, COR)], (0.4, 1.0, -0.4),
         "a traseira", "a saia é a própria parede descendo: nada aparece"),
        ("lp-pe.png", [(trimesh.load(os.path.join(DEST, "lp-pe.stl")), COR)],
         (-1.0, -0.55, -0.55), "o pé da frente",
         "bico redondo, lateral curvada, nenhum canto vivo"),
        ("lp-pl.png", [(trimesh.load(os.path.join(DEST, "lp-pl.stl")), COR)],
         (0.0, -0.02, -1.0), "planta do pé em z = 12 mm",
         "parede constante inclusive no bico (cavidade com R − parede)"),
    ]
    for arq, cena, d, _, _ in vistas:
        render.salvar(render.render(cena, direcao=d, largura=980),
                      os.path.join(DEST, arq))

    fig = plt.figure(figsize=(15.6, 6.4), facecolor=FUNDO)
    fig.text(0.5, 0.975, "Acabamento: nada aparente atrás, nenhum canto vivo",
             ha="center", va="top", fontsize=18, color=TINTA, weight="bold")
    fig.text(0.5, 0.932, "o pé de trás virou saia rente à casca · os pés da "
             "frente viraram língua arredondada", ha="center", va="top",
             fontsize=10.5, color=GRIS)
    for i, (arq, _, _, tit, sub) in enumerate(vistas):
        ax = fig.add_axes([0.015 + i * 0.33, 0.10, 0.31, 0.74])
        ax.imshow(np.asarray(Image.open(os.path.join(DEST, arq))))
        ax.set_anchor("N"); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#e3e0da")
        ax.set_title(tit, fontsize=12, color=TINTA, weight="bold", pad=6)
        ax.text(0.5, -0.03, sub, transform=ax.transAxes, ha="center",
                va="top", fontsize=9.2, color=GRIS)
    fig.savefig(os.path.join(DEST, "limpo.png"), dpi=125, facecolor=FUNDO)
    print("gerado limpo.png")


if __name__ == "__main__":
    main()
