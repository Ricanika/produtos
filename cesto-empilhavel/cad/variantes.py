#!/usr/bin/env python3
"""Gera as tres opcoes de canaleta em 3D e monta a folha de comparacao visual.

A - trilho corrido: trilho saliente de ponta a ponta de um lado, rim rebaixado
    do outro. Trava na extensao toda, sem gaveta, mas a peca fica assimetrica.
B - trilho embutido: lingueta de um lado, canaleta com boca estreita e bolso
    largo do outro. Simetrico e o mais rigido, mas a canaleta e contra-saida
    -> exige 2 gavetas laterais, e a junta fica com 8,7 mm.
C - canaleta aparente: risco corrido nas duas laterais + 2 abas com gancho de um
    lado e 2 janelas do outro. Simetrico, sem gaveta, rims encostados.

Uso:  python3 variantes.py
"""
import os
import textwrap
import time

import numpy as np
import trimesh
from build123d import Box, Pos, export_step, export_stl

import modelo3d as M
import render

DEST = os.path.dirname(os.path.abspath(__file__))
COR_A = (0.93, 0.44, 0.13)
COR_B = (0.72, 0.30, 0.08)

OPCOES = [
    ("A", "trilho corrido",
     "trava na extensão toda, sem gaveta, rims encostados",
     "o rim do lado fêmea desce 18 mm: a peça sozinha fica assimétrica "
     "e perde os berços daquele lado"),
    ("B", "trilho embutido",
     "trava em X e em Z na extensão toda, simétrico, o mais rígido",
     "canaleta é contra-saída: 2 gavetas (~USD 3 mil) e junta de 8,7 mm "
     "entre as peças"),
    ("C", "canaleta aparente",
     "simétrico, sem gaveta, rims encostados, o mais leve",
     "trava em 2 abas de 40 mm, não na extensão toda"),
]
Z_SEC, Y_SEC = 100.0, 30.0     # janela da secao do encaixe


def malha(p, nome):
    export_stl(p, os.path.join(DEST, f"var-{nome}.stl"))
    return trimesh.load(os.path.join(DEST, f"var-{nome}.stl"))


def secao(p, passo):
    """Recorta as duas pecas acopladas num bloco, para a vista de secao.

    Feito por booleano no solido (nao na malha) para as faces de corte saírem
    fechadas -- malha aberta renderiza como buraco.
    """
    jx = passo / 2
    bloco = Pos(jx, (Y_SEC + 130) / 2, (Z_SEC + 135) / 2) * \
        Box(84.0, 130 - Y_SEC, 135 - Z_SEC)
    return p & bloco, (Pos(passo, 0, 0) * p) & bloco


def main():
    # referencia: a mesma peca com a faixa de 18 mm e nenhuma feicao, para
    # separar o custo da faixa do custo do acoplamento
    pr, _ = M.cesto(None, h_rim=M.H_BANDA)
    ref = pr.volume * M.RHO
    print(f"referencia: faixa de 10 mm = 163,7 g | faixa de {M.H_BANDA:.0f} mm "
          f"= {ref:.1f} g")

    dados = {}
    for letra, _, _, _ in OPCOES:
        t0 = time.time()
        p, n = M.cesto(letra)
        peso = p.volume * M.RHO
        passo = M.passo_acoplado(letra)
        export_step(p, os.path.join(DEST, f"var-{letra}.step"))
        m = malha(p, letra)
        mb = m.copy(); mb.apply_translation([passo, 0, 0])

        inter = (p & (Pos(passo, 0, 0) * p)).volume
        sa, sb = secao(p, passo)
        ma, mbs = malha(sa, f"{letra}-sa"), malha(sb, f"{letra}-sb")

        vistas = {
            "peca": ([(m, COR_A)], (-0.60, -0.90, -1.10)),
            "par": ([(m, COR_A), (mb, COR_B)], (-0.90, -1.20, -0.75)),
            "det": ([(ma, COR_A), (mbs, COR_B)], (0.12, -1.00, -0.30)),
        }
        for nome, (cena, d) in vistas.items():
            render.salvar(render.render(cena, direcao=d, largura=1150),
                          os.path.join(DEST, f"var-{letra}-{nome}.png"))
        dados[letra] = dict(peso=peso, furos=n, inter=inter, passo=passo)
        print(f"{letra}: peso {peso:6.1f} g ({peso-ref:+5.1f} vs faixa nua) | "
              f"passo {passo:.1f} | interferencia {inter:8.1f} mm3 | "
              f"{time.time()-t0:5.0f} s")

    folha(dados, ref)


def folha(dados, ref):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from PIL import Image

    TINTA, CINZA, NOVO, VERDE = "#1f2328", "#6b7280", "#c2410c", "#15803d"
    fig = plt.figure(figsize=(16.6, 14.6), facecolor="#fbfaf8")
    fig.text(0.5, 0.978, "As três canaletas, em 3D", ha="center", va="top",
             fontsize=21.5, color=TINTA, weight="bold")
    fig.text(0.5, 0.956, "mesma peça, mesmo pé, mesma silhueta — só o "
             "acoplamento muda · 17/09/2026", ha="center", va="top",
             fontsize=11.5, color="#3d444d")
    cols = [("peca", "a peça sozinha, vista de cima",
             "à direita o macho, à esquerda a fêmea"),
            ("par", "duas acopladas", "é assim que elas ficam no estoque"),
            ("det", "seção do encaixe",
             "corte no rim, no plano da junta")]
    x0, larg, gap = 0.148, 0.272, 0.010
    for j, (_, tit, sub) in enumerate(cols):
        cx = x0 + j * (larg + gap) + larg / 2
        fig.text(cx, 0.932, tit, ha="center", va="top", fontsize=12.5,
                 color=TINTA, weight="bold")
        fig.text(cx, 0.911, sub, ha="center", va="top", fontsize=9.5, color=CINZA)

    h = 0.258
    for i, (letra, nome, ganha, custa) in enumerate(OPCOES):
        y = 0.635 - i * 0.283
        tx = fig.add_axes([0.022, y, 0.118, h]); tx.axis("off")
        tx.set_xlim(0, 1); tx.set_ylim(0, 1)
        d = dados[letra]
        tx.text(0, 1.0, letra, fontsize=34, color=NOVO, weight="bold", va="top")
        tx.text(0, 0.72, nome, fontsize=12.5, color=TINTA, weight="bold", va="top")
        tx.text(0, 0.60, f"{d['peso']:.1f}".replace(".", ",") + " g",
                fontsize=15, color=TINTA, va="top")
        tx.text(0, 0.50, f"{d['peso']-163.7:+.1f}".replace(".", ",") +
                " g vs. hoje", fontsize=9.2, color=CINZA, va="top")
        tx.text(0, 0.40, "\n".join(textwrap.wrap("ganha: " + ganha, 28)),
                fontsize=8.6, color=VERDE, va="top", linespacing=1.45)
        tx.text(0, 0.17, "\n".join(textwrap.wrap("custa: " + custa, 28)),
                fontsize=8.6, color=NOVO, va="top", linespacing=1.45)
        for j, (col, _, _) in enumerate(cols):
            ax = fig.add_axes([x0 + j * (larg + gap), y, larg, h])
            ax.imshow(np.asarray(Image.open(
                os.path.join(DEST, f"var-{letra}-{col}.png"))))
            ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values():
                s.set_color("#e3e0da")

    bx = fig.add_axes([0.022, 0.014, 0.956, 0.042]); bx.axis("off")
    bx.set_xlim(0, 1); bx.set_ylim(0, 1)
    bx.add_patch(Rectangle((0, 0), 1, 1, transform=bx.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.2))
    it = " · ".join(f"{k} {v['inter']:.0f}" for k, v in dados.items())
    bx.text(0.014, 0.74, "Interseção entre as duas peças acopladas, medida por "
            f"booleano no sólido (mm³): {it}. Zero é o que se quer — nenhuma "
            "das três tem interferência.", fontsize=10.2, color=TINTA, va="center")
    bx.text(0.014, 0.28, "As três mantêm o encaixe e o passo empilhado de 130 mm: "
            "as feições vivem no rim, que fica acima da peça de baixo quando "
            "encaixadas. A faixa de 18 mm sozinha já leva a peça a "
            + f"{ref:.1f}".replace(".", ",") + " g — o resto é o acoplamento.",
            fontsize=10.2, color=CINZA, va="center")
    fig.savefig(os.path.join(DEST, "variantes.png"), dpi=118, facecolor="#fbfaf8")
    print("gerado variantes.png")


if __name__ == "__main__":
    main()
