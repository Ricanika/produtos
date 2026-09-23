#!/usr/bin/env python3
"""As colunas de listra da lateral, ancoradas no pe.

Pedido de 22/09: "nas duas laterais, colado no pe, temos 3 buracos verticais
que estao cortados, retire eles, e aproxime os outros 3 furos para mais
proximo do pe".

A grade vinha de grade(), CENTRADA EM y = 0 -- ela nao sabia do pe. Com passo
de 11 mm e o pe em y = -58, duas colunas caiam em cima dele (uma cortada pela
aresta, a que o cliente viu) e as duas vizinhas ficavam a 6,01 e 1,01 mm. Essa
lasca de 1 mm e justo onde o pe descarrega a pilha na casca.
"""
import os
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from build123d import Pos, export_stl
from matplotlib.patches import Rectangle

import modelo3d as M
import render

DEST = os.path.dirname(os.path.abspath(__file__))
COR = (0.80, 0.36, 0.12)
FUNDO, TINTA, GRIS = "#fbfaf8", "#1f2328", "#6b7280"
NOVO, VERDE, CINZ, VERM = "#c2410c", "#15803d", "#64748b", "#b91c1c"
VISTA = (-1.0, 0.22, -0.42)     # o ponto de vista do print do cliente


def vg(x, casas=2):
    return f"{x:.{casas}f}".replace(".", ",")


def passo(p, dy, lo=0.0, hi=180.0, tol=0.02):
    """Menor deslocamento em z em que duas pecas nao se interpenetram."""
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if (p & (Pos(0, dy, mid) * p)).volume > 0.002:
            lo = mid
        else:
            hi = mid
    return hi


def main():
    M.padrao()
    yc, L, _, ky, _, _ = M.PES[0]
    meia = L / 2 + ky * M.listras()[-1][1]
    grade_antiga = lambda: M.grade(
        M.secao(M.BANDA, M.T_RIM)[1] - M.LIS_W - 30, M.LIS_P)
    orig = M.cols_lateral
    d = {}
    for nome, fn in (("antes", grade_antiga), ("depois", orig)):
        M.cols_lateral = fn
        try:
            cols = fn()
            p, n = M.cesto(aba=True)
        finally:
            M.cols_lateral = orig
        arq = os.path.join(DEST, f"col-{nome}.stl")
        export_stl(p, arq)
        folgas = sorted((abs(y - yc) - meia - M.LIS_W / 2, y) for y in cols)
        d[nome] = dict(cols=cols, n=n, peso=p.volume * M.RHO, folgas=folgas,
                       corta=sum(1 for f, _ in folgas if f < 0))
        if nome == "depois":
            # Encaixe e empilhamento MEDIDOS: a folha os afirmava digitados
            # em 46,80/130,00, da saida de 12 graus.
            d[nome]["pn"] = passo(p, 0.0)
            d[nome]["pe"] = passo(p, M.DESLOC)
            print(f"         encaixa {d[nome]['pn']:.2f} · "
                  f"empilha {d[nome]['pe']:.2f}")
        print(f"{nome:7s}: {len(cols)} colunas, {n} rasgos, "
              f"{p.volume*M.RHO:.1f} g, {d[nome]['corta']} cortada(s) pelo pe")
        render.salvar(render.render([(trimesh.load(arq), COR)], direcao=VISTA,
                                    largura=1000),
                      os.path.join(DEST, f"col-{nome}.png"))
    folha(d, meia)


def folha(d, meia):
    from PIL import Image
    fig = plt.figure(figsize=(16.4, 8.0), facecolor=FUNDO)
    fig.text(0.5, 0.982, "As colunas de listra, ancoradas no pé",
             ha="center", va="top", fontsize=22, color=TINTA, weight="bold")
    fig.text(0.5, 0.943, "a grade era centrada em y = 0 e não sabia do pé · "
             "agora as colunas nascem dele para fora",
             ha="center", va="top", fontsize=11.5, color="#3d444d")

    a, b = d["antes"], d["depois"]
    for i, (nome, dd, cor, sub) in enumerate((
            ("ANTES", a, VERM,
             f"{len(a['cols'])} colunas · {a['corta']} cortadas pelo pé · "
             f"folgas de {vg(a['folgas'][2][0])} e {vg(a['folgas'][3][0])} mm"),
            ("DEPOIS", b, VERDE,
             f"{len(b['cols'])} colunas · nenhuma cortada · "
             f"{vg(b['folgas'][0][0])} mm dos dois lados do pé"))):
        ax = fig.add_axes([0.025 + i * 0.315, 0.115, 0.30, 0.755])
        ax.imshow(np.asarray(Image.open(
            os.path.join(DEST, f"col-{nome.lower()}.png"))))
        ax.set_anchor("N"); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#e3e0da")
        ax.set_title(nome, fontsize=12.5, color=cor, weight="bold", pad=5)
        ax.text(0.5, -0.03, "\n".join(textwrap.wrap(sub, 58)),
                transform=ax.transAxes, ha="center", va="top", fontsize=9.3,
                color=GRIS, linespacing=1.4)

    tb = fig.add_axes([0.665, 0.115, 0.308, 0.755]); tb.axis("off")
    tb.add_patch(Rectangle((0, 0), 1, 1, transform=tb.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.3))
    tb.text(0.045, 0.962, "AS COLUNAS PERTO DO PÉ", fontsize=11.5, color=NOVO,
            weight="bold", va="top")
    tb.text(0.045, 0.915, f"folga até a PEGADA do pé (meia-largura "
            f"{vg(meia)} mm\nno topo do campo, onde ele é mais largo)",
            fontsize=8.6, color=GRIS, va="top", linespacing=1.4)
    y = 0.815
    for rot, dd, cor in (("antes", a, CINZ), ("depois", b, VERDE)):
        tb.text(0.045, y, rot.upper(), fontsize=9.6, color=cor, weight="bold",
                va="center")
        y -= 0.054
        for f, yy in dd["folgas"][:4]:
            marca = "  CORTA O PÉ" if f < 0 else ""
            tb.text(0.10, y, f"y = {yy:6.1f} mm", fontsize=9.0, color=TINTA,
                    va="center", family="DejaVu Sans Mono")
            tb.text(0.62, y, f"{vg(f):>7} mm", fontsize=9.0,
                    color=VERM if f < 0 else TINTA, va="center",
                    family="DejaVu Sans Mono")
            tb.text(0.80, y, marca, fontsize=8.4, color=VERM, va="center")
            y -= 0.048
        y -= 0.03
    # As tres pilhas de texto vinham com y CORRIDO para as duas primeiras e
    # y FIXO (0,155) para a terceira: com 4 folgas por lado elas se cruzavam.
    # Agora as duas de baixo saem de ancoras fixas, com espaco reservado.
    tb.text(0.045, 0.300, f"nº de rasgos    {a['n']} → {b['n']}\n"
            f"peso em PP      {vg(a['peso'],1)} → {vg(b['peso'],1)} g\n"
            f"nervura entre listras   {M.LIS_P - M.LIS_W:.0f} mm, toda a "
            f"lateral\n"
            f"folga até o pé  LIS_FOLGA_PE = {M.LIS_FOLGA_PE:.0f} mm, "
            "os dois lados",
            fontsize=9.0, color=TINTA, va="top", linespacing=1.7)
    tb.text(0.045, 0.160, "A pegada do pé CRESCE com z (L/2 + ky·z), então quem\n"
            "manda é a cota mais alta do campo. cols_lateral() gera as\n"
            "colunas do pé para fora, nos dois sentidos — não há cota\n"
            "para acertar à mão, e se o pé mudar as colunas acompanham.\n"
            f"Encaixe {vg(b['pn'], 2)} e empilhamento {vg(b['pe'], 2)} "
            f"inalterados.",
            fontsize=8.6, color=NOVO, va="top", linespacing=1.55)

    fig.savefig(os.path.join(DEST, "colunas.png"), dpi=118, facecolor=FUNDO)
    print("gerado colunas.png")


if __name__ == "__main__":
    main()
