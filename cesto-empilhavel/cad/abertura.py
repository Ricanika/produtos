#!/usr/bin/env python3
"""Tres aberturas possiveis, no perfil: e o CHANFRO que define o angulo.

Com o P girado, o comprimento passou a 215 mm e sobrou trecho reto atras --
ou seja, cabe abrir mais a frente sem mexer em nada do empilhamento.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import modelo3d as M

DEST = os.path.dirname(os.path.abspath(__file__))
FUNDO, TINTA, GRIS, NOVO, CINZ = "#fbfaf8", "#1f2328", "#6b7280", "#c2410c", "#94a3b8"


def perfil(chanfro, chanfro_pe):
    """Silhueta no plano y-z, do fundo para a frente."""
    yf, yb = -M.PROF / 2, M.PROF / 2
    return np.array([
        (yb, 0.0), (yb, M.ALT), (yf + chanfro, M.ALT),
        (yf, M.ALT - chanfro), (yf, chanfro_pe), (yf + chanfro_pe, 0.0),
        (yb, 0.0),
    ])


def main():
    M.set_draft(12.0)
    opcoes = [
        (40.0, 36.0, CINZ, "mais fechada"),
        (M.CHANFRO, M.CHANFRO_PE, NOVO, "a de hoje"),
        (68.0, 36.0, "#0f766e", "mais aberta"),
    ]
    fig, axs = plt.subplots(1, 3, figsize=(14.6, 5.6), facecolor=FUNDO)
    fig.text(0.5, 0.975, "O ângulo da abertura", ha="center", va="top",
             fontsize=18, color=TINTA, weight="bold")
    fig.text(0.5, 0.932, f"perfil no comprimento ({M.PROF:.0f} mm) · o chanfro "
             "de topo é que define a abertura · a frente é à esquerda",
             ha="center", va="top", fontsize=10, color=GRIS)
    for ax, (ch, chp, cor, nome) in zip(axs, opcoes):
        ax.set_facecolor(FUNDO); ax.set_aspect("equal"); ax.axis("off")
        for c2, cp2, cor2, _ in opcoes:              # as outras, de fundo
            if c2 == ch:
                continue
            q = perfil(c2, cp2)
            ax.plot(q[:, 0], q[:, 1], color="#e2e5ea", lw=1.2)
        q = perfil(ch, chp)
        ax.plot(q[:, 0], q[:, 1], color=cor, lw=2.2)
        # a aba, para lembrar que ela some onde o chanfro come
        ax.plot([-M.PROF / 2 + ch, M.PROF / 2], [M.ALT, M.ALT], color=cor,
                lw=5.0, alpha=0.30, solid_capstyle="butt")
        ax.set_xlim(-M.PROF / 2 - 12, M.PROF / 2 + 12)
        ax.set_ylim(-10, M.ALT + 74)
        ax.set_title(f"chanfro {ch:.0f} mm · {nome}", fontsize=12, pad=8,
                     color=TINTA if cor == NOVO else GRIS,
                     weight="bold" if cor == NOVO else "normal")
        ax.text(0, M.ALT + 68, f"frente com {M.ALT - ch - chp:.0f} mm de face"
                f"\ntopo da frente em z = {M.ALT - ch:.0f} mm"
                f"\naba livre atrás: {M.PROF - ch:.0f} mm",
                ha="center", va="top", fontsize=9.2, color=TINTA,
                linespacing=1.6)
    fig.subplots_adjust(top=0.80, bottom=0.04, left=0.02, right=0.98)
    fig.savefig(os.path.join(DEST, "abertura.png"), dpi=125, facecolor=FUNDO)
    print("gerado abertura.png")


if __name__ == "__main__":
    main()
