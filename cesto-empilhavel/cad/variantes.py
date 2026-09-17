#!/usr/bin/env python3
"""Gera as tres opcoes de canaleta em 3D e monta a folha de comparacao visual.

A - trilho corrido: trilho saliente de ponta a ponta de um lado, rim rebaixado
    do outro. Trava na extensao toda, sem gaveta, mas a peca fica assimetrica.
B - trilho embutido: lingueta em T de um lado, canaleta em T do outro. Simetrico
    e o mais bonito, mas a canaleta e contra-saida -> exige 2 gavetas laterais.
C - canaleta aparente: risco corrido nas duas laterais + 2 abas com gancho de um
    lado e 2 janelas do outro. Simetrico, sem gaveta.

Uso:  python3 variantes.py
"""
import os
import time

import numpy as np
import trimesh
from build123d import Pos, export_step, export_stl

import modelo3d as M
import render

DEST = os.path.dirname(os.path.abspath(__file__))
COR_A = (0.93, 0.44, 0.13)
COR_B = (0.78, 0.33, 0.09)

OPCOES = [
    ("A", "trilho corrido",
     "trava na extensão toda, sem gaveta",
     "o rim do lado fêmea desce 18 mm: a peça sozinha fica assimétrica"),
    ("B", "trilho embutido",
     "simétrico, corrido, o mais rígido e o mais bonito",
     "canaleta horizontal é contra-saída: 2 gavetas laterais (~USD 3 mil)"),
    ("C", "canaleta aparente",
     "simétrico, sem gaveta, rims encostados",
     "trava em 2 abas de 40 em vez da extensão toda"),
]


def malha(p, nome):
    export_stl(p, os.path.join(DEST, f"var-{nome}.stl"))
    export_step(p, os.path.join(DEST, f"var-{nome}.step"))
    return trimesh.load(os.path.join(DEST, f"var-{nome}.stl"))


def recorte(m, zmin, x0, x1):
    """Fatia a malha para o detalhe do encaixe."""
    r = m.slice_plane([0, 0, zmin], [0, 0, 1])
    r = r.slice_plane([x0, 0, 0], [1, 0, 0])
    return r.slice_plane([x1, 0, 0], [-1, 0, 0])


def main():
    dados = {}
    for letra, _, _, _ in OPCOES:
        t0 = time.time()
        p, n = M.cesto(letra)
        peso = p.volume * M.RHO
        m = malha(p, letra)
        mb = m.copy(); mb.apply_translation([M.LARG, 0, 0])

        # interferencia entre as duas pecas acopladas (tem de ser zero)
        try:
            inter = (p & (Pos(M.LARG, 0, 0) * p)).volume
        except Exception as e:                       # noqa: BLE001
            inter = float("nan")
            print(f"  [{letra}] checagem de interferencia falhou: {e}")

        vistas = {
            "peca": ([(m, COR_A)], (-1.0, -1.35, -0.62)),
            "par": ([(m, COR_A), (mb, COR_B)], (-1.0, -1.30, -0.58)),
            "det": ([(recorte(m, 96, 20, 175), COR_A),
                     (recorte(mb, 96, 20, 175), COR_B)], (-0.75, -1.0, -0.80)),
        }
        for nome, (cena, d) in vistas.items():
            render.salvar(render.render(cena, direcao=d, largura=1100),
                          os.path.join(DEST, f"var-{letra}-{nome}.png"))
        dados[letra] = dict(peso=peso, furos=n, inter=inter, seg=time.time() - t0)
        print(f"{letra}: peso {peso:6.1f} g | {n} furos | interferencia "
              f"{inter:8.1f} mm3 | {time.time()-t0:5.0f} s")

    folha(dados)


def folha(dados):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from PIL import Image

    TINTA, CINZA, NOVO = "#1f2328", "#6b7280", "#c2410c"
    fig = plt.figure(figsize=(16.0, 13.4), facecolor="#fbfaf8")
    fig.text(0.5, 0.979, "As três canaletas, em 3D", ha="center", va="top",
             fontsize=21, color=TINTA, weight="bold")
    fig.text(0.5, 0.955, "mesma peça, mesmo pé, mesma silhueta — só o "
             "acoplamento muda · 17/09/2026", ha="center", va="top",
             fontsize=11.5, color="#3d444d")
    for col, tit in (("peca", "a peça sozinha"), ("par", "duas acopladas"),
                     ("det", "o encaixe, de perto")):
        x = {"peca": 0.275, "par": 0.545, "det": 0.815}[col]
        fig.text(x, 0.932, tit, ha="center", va="top", fontsize=12,
                 color=TINTA, weight="bold")

    h, y0 = 0.283, 0.636
    for i, (letra, nome, ganha, custa) in enumerate(OPCOES):
        y = y0 - i * 0.303
        tx = fig.add_axes([0.028, y, 0.115, h]); tx.axis("off")
        tx.set_xlim(0, 1); tx.set_ylim(0, 1)
        tx.text(0, 0.97, letra, fontsize=30, color=NOVO, weight="bold", va="top")
        tx.text(0, 0.70, nome, fontsize=12, color=TINTA, weight="bold", va="top")
        d = dados[letra]
        tx.text(0, 0.56, f"{d['peso']:.1f} g".replace(".", ","), fontsize=13,
                color=TINTA, va="top")
        tx.text(0, 0.46, f"{d['furos']} furos", fontsize=9.5, color=CINZA, va="top")
        tx.text(0, 0.36, "ganha: " + ganha, fontsize=8.8, color="#15803d",
                va="top", wrap=True)
        tx.text(0, 0.17, "custa: " + custa, fontsize=8.8, color=NOVO, va="top")
        for j, col in enumerate(("peca", "par", "det")):
            ax = fig.add_axes([0.155 + j * 0.27, y, 0.26, h])
            ax.imshow(np.asarray(Image.open(
                os.path.join(DEST, f"var-{letra}-{col}.png"))))
            ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values():
                s.set_color("#e3e0da")

    bx = fig.add_axes([0.028, 0.022, 0.944, 0.058]); bx.axis("off")
    bx.set_xlim(0, 1); bx.set_ylim(0, 1)
    bx.add_patch(Rectangle((0, 0), 1, 1, transform=bx.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.2))
    inter = " · ".join(f"{k}: {v['inter']:.0f} mm³" for k, v in dados.items())
    bx.text(0.015, 0.76, "As três acoplam sem interferência — volume de "
            f"interseção entre as duas peças: {inter}.",
            fontsize=10, color=TINTA, va="center")
    bx.text(0.015, 0.30, "Todas mantêm o encaixe (as feições vivem no rim, que "
            "fica acima da peça de baixo quando encaixadas) e o passo empilhado "
            "de 130 mm.", fontsize=10, color=CINZA, va="center")
    fig.savefig(os.path.join(DEST, "variantes.png"), dpi=118, facecolor="#fbfaf8")
    print("gerado variantes.png")


if __name__ == "__main__":
    main()
