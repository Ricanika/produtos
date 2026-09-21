#!/usr/bin/env python3
"""Cortes 2D no eixo do pe, tirados do proprio solido.

O rasterizador 3D nao serve para isto: de perto a peca vira bloco de cor. Aqui
os segmentos vem de trimesh.intersections.mesh_plane, ou seja, sao o solido
cortado de verdade -- e o desenho que vai para o ferramenteiro.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from trimesh.intersections import mesh_plane

import modelo3d as M

DESLOC = None  # vem de modelo3d.DESLOC em main()

DEST = os.path.dirname(os.path.abspath(__file__))
FUNDO, TINTA, GRIS = "#fbfaf8", "#1f2328", "#6b7280"
NOVO, CINZ = "#c2410c", "#64748b"
PASSO_E = 130.0


def seg(m, y, dz=0.0):
    """Segmentos do corte em y, no plano x-z, deslocados dz em z."""
    s = mesh_plane(m, plane_normal=[0, 1, 0], plane_origin=[0, y, 0])
    if s is None or len(s) == 0:
        return np.zeros((0, 2, 2))
    out = s[:, :, [0, 2]].copy()
    out[:, :, 1] += dz
    return out


def seg_x(m, x, dy=0.0, dz=0.0):
    """Segmentos do corte em x (plano y-z) -- e nele que a canetinha aparece,
    porque ela mora na parede de TRAS."""
    s = mesh_plane(m, plane_normal=[1, 0, 0], plane_origin=[x, 0, 0])
    if s is None or len(s) == 0:
        return np.zeros((0, 2, 2))
    out = s[:, :, [1, 2]].copy()
    out[:, :, 0] += dy
    out[:, :, 1] += dz
    return out


def desenha(ax, segs, cor, lw=1.6, alpha=1.0):
    for a, b in segs:
        ax.plot([a[0], b[0]], [a[1], b[1]], color=cor, lw=lw, alpha=alpha,
                solid_capstyle="round")


def cota(ax, x, z0, z1, txt, cor=NOVO, lado=1):
    ax.annotate("", xy=(x, z1), xytext=(x, z0),
                arrowprops=dict(arrowstyle="<->", color=cor, lw=1.1))
    ax.text(x + lado * 1.4, (z0 + z1) / 2, txt, color=cor, fontsize=8.6,
            va="center", ha="left" if lado > 0 else "right")


def main(pn):
    global DESLOC
    M.set_draft(12.0)
    DESLOC = M.DESLOC
    arq = os.path.join(DEST, "cesto-aba.stl")
    if not os.path.exists(arq):
        from build123d import export_stl
        p, _ = M.cesto(aba=True)
        export_stl(p, arq)
    m = trimesh.load(arq)
    yc = M.PES[0][0]          # pe da frente (o unico)
    hx = M.LARG / 2           # plano da junta: tudo em x e relativo a ele

    fig, axs = plt.subplots(1, 3, figsize=(17.4, 7.4), facecolor=FUNDO)
    for ax in axs:
        ax.set_facecolor(FUNDO)
        ax.set_aspect("equal")
        ax.axis("off")

    # --- 1: ENCAIXE, corte no eixo do pe ---------------------------------
    ax = axs[0]
    # a 10 mm do eixo a peca esta inteira: e a referencia de onde ficam a
    # parede e a aba. No eixo do pe as duas estao vazadas pela cavidade.
    desenha(ax, seg(m, yc + DESLOC), "#aab4c2", lw=1.0)
    desenha(ax, seg(m, yc), CINZ)
    desenha(ax, seg(m, yc, pn), NOVO)
    ax.set_xlim(hx - 56, hx + 17); ax.set_ylim(-6, 200)
    ax.set_title(f"ENCAIXE · corte no eixo do pé · passo {pn:.1f} mm"
                 .replace(".", ","), fontsize=12, color=TINTA, weight="bold",
                 pad=14)
    cota(ax, hx - 42, 0.0, pn, f"{pn:.1f} mm".replace(".", ","))
    ax.text(hx + 5, 4, "piso do pé de cima\ndentro do pé de baixo", fontsize=8.4,
            color=NOVO, va="center", ha="left")
    ax.annotate("", xy=(M.LARG / 2, 137), xytext=(M.LARG / 2 - M.ABA_W, 137),
                arrowprops=dict(arrowstyle="<->", color=CINZ, lw=1.0))
    ax.text(hx - M.ABA_W - 3, 138,
            "aba 10 mm: a parede de cima tem\nde passar pela borda interna "
            "dela\n→ 10/tg 12° = 46,9 mm",
            fontsize=8.4, color=CINZ, va="bottom", ha="right")
    ax.text(hx - 55, 196, "cinza claro: a mesma peça 14 mm ao lado,\nonde a "
            "parede e a aba estão inteiras", fontsize=8.2, color="#9aa4b2",
            va="top", ha="left")

    # --- 2: EMPILHAMENTO, corte 10 mm ao lado ----------------------------
    ax = axs[1]
    desenha(ax, seg(m, yc + DESLOC), CINZ)
    desenha(ax, seg(m, yc, PASSO_E), NOVO)
    ax.set_xlim(hx - 48, hx + 17); ax.set_ylim(-6, 276)
    ax.set_title(f"EMPILHAMENTO · corte {DESLOC:.0f} mm ao lado do pé · "
                 f"passo {PASSO_E:.1f} mm".replace(".", ","), fontsize=12,
                 color=TINTA, weight="bold", pad=14)
    cota(ax, hx - 42, 0.0, PASSO_E, f"{PASSO_E:.1f} mm".replace(".", ","))
    ax.text(hx + 5, 132, "o piso do pé pousa\nna aba plana", fontsize=8.4,
            color=NOVO, va="center", ha="left")
    ax.text(hx + 5, 120, "aqui a aba é inteira:\no recorte ficou 10 mm\npara lá",
            fontsize=8.4, color=CINZ, va="top", ha="left")

    fig.text(0.5, 0.975, "O mesmo pé nas duas funções",
             ha="center", va="top", fontsize=17, color=TINTA, weight="bold")
    fig.text(0.5, 0.942, "cortes tirados do sólido · cinza = peça de baixo, "
             "laranja = peça de cima", ha="center", va="top", fontsize=10,
             color=GRIS)
    # --- 3: a canetinha, no corte em x = 0 -------------------------------
    ax = axs[2]
    desenha(ax, seg_x(m, 0.0), CINZ)
    desenha(ax, seg_x(m, 0.0, DESLOC, PASSO_E), NOVO)
    ax.set_xlim(88, 132); ax.set_ylim(116, 145)
    ax.set_title("A CANETINHA · corte no meio da traseira", fontsize=12,
                 color=TINTA, weight="bold", pad=14)
    ax.text(89, 144, "a canetinha (laranja) pousa na aba de trás. Ela projeta "
            "só\n%.1f mm da parede e o cone a alcança em z = %.0f mm, onde ela "
            "se\napaga — por isso ela NÃO abre recorte na aba, e o encaixe\n"
            "continua em 46,9 mm." % (M.can_y0() - (M.PROF / 2 - M.ALT * M.TAN),
                                      M.can_ztopo()),
            fontsize=8.4, color=TINTA, va="top", ha="left")

    fig.subplots_adjust(top=0.855, bottom=0.03, left=0.015, right=0.985)
    fig.savefig(os.path.join(DEST, "cortes.png"), dpi=125, facecolor=FUNDO)
    print("gerado cortes.png")


if __name__ == "__main__":
    main(46.9)
