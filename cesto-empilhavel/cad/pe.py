#!/usr/bin/env python3
"""Pezinho e encaixe do pe traseiro -- 3D e folha de comparacao.

Duas versoes da MESMA peca (opcao D de acoplamento):
  N - so pezinhos: ENCAIXA, passo 55,5 mm. Nada avanca para dentro do rim.
  P - pezinhos + soquetes no rim: EMPILHA a 130 mm e NAO encaixa.
As duas sao exclusivas por geometria, nao por acabamento: qualquer berco que
avance para dentro do rim fecha a passagem da chapa da peca de cima.
"""
import os
import textwrap

import numpy as np
import trimesh
from build123d import Box, Pos, export_step, export_stl

import modelo3d as M
import render

DEST = os.path.dirname(os.path.abspath(__file__))
COR, COR2 = (0.93, 0.44, 0.13), (0.72, 0.30, 0.08)
COR_SUP = (0.55, 0.63, 0.72)      # peca de CIMA na secao, para contrastar
FUNDO, TINTA, CINZA, NOVO, VERDE = "#fbfaf8", "#1f2328", "#6b7280", "#c2410c", "#15803d"


def malha(sol, nome):
    export_stl(sol, os.path.join(DEST, f"pe-{nome}.stl"))
    return trimesh.load(os.path.join(DEST, f"pe-{nome}.stl"))


def main():
    from empilha import passo
    dados = {}
    for tag, emp in (("N", False), ("P", True)):
        p, _ = M.cesto("D", empilha=emp)
        export_step(p, os.path.join(DEST, f"pe-{tag}.step"))
        m = malha(p, tag)
        peso = p.volume * M.RHO
        pas = passo(p)

        # pilha / coluna encaixada
        cena = []
        for i in range(3 if emp else 4):
            t = m.copy(); t.apply_translation([0, 0, i * pas])
            cena.append((t, COR if i % 2 == 0 else COR2))
        render.salvar(render.render(cena, direcao=(-1.0, -1.25, -0.5),
                                   largura=1000),
                      os.path.join(DEST, f"pe-{tag}-pilha.png"))

        # secao no pe traseiro, com duas pecas na posicao de uso
        # corta NO MEIO do pe traseiro e olha a face de corte de frente: e a
        # unica vista em que o pe dentro do soquete aparece
        y0, y1 = M.PE_Y[1]
        yc = (y0 + y1) / 2
        # o corte em x tira a parede INTERNA do soquete, senao ela esconde o pe
        bloco = Pos(102.0, (yc + 102.0) / 2, (M.ALT - 12 + M.ALT + 20) / 2) * \
            Box(32.0, 102.0 - yc, 32.0)
        sa = p & bloco
        sb = (Pos(0, 0, pas) * p) & bloco
        ca = [(malha(sa, f"{tag}-sa"), COR)]
        if sb.volume > 1:
            ca.append((malha(sb, f"{tag}-sb"), COR_SUP))
            print(f"  secao {tag}: peca de baixo {sa.volume/1000:.1f} cm3 | "
                  f"peca de cima {sb.volume/1000:.1f} cm3")
        render.salvar(render.render(ca, direcao=(0.22, -1.0, -0.26),
                                   largura=1000),
                      os.path.join(DEST, f"pe-{tag}-sec.png"))
        dados[tag] = dict(peso=peso, passo=pas)
        print(f"{tag}: peso {peso:6.1f} g | passo {pas:5.1f} mm")

    # vistas do pe: valem para as duas (os pezinhos sao iguais)
    m = trimesh.load(os.path.join(DEST, "pe-N.stl"))
    render.salvar(render.render([(m, COR)], direcao=(-0.55, -0.85, 1.0),
                               largura=1000),
                  os.path.join(DEST, "pe-baixo.png"))
    render.salvar(render.render([(m, COR)], direcao=(-0.25, -1.0, 0.30),
                               largura=1000),
                  os.path.join(DEST, "pe-rasante.png"))
    folha(dados)


def imagem(fig, rect, arq, titulo=None, sub=None):
    from PIL import Image
    ax = fig.add_axes(rect)
    ax.imshow(np.asarray(Image.open(os.path.join(DEST, arq))))
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#e3e0da")
    if titulo:
        ax.set_title(titulo, fontsize=12, color=TINTA, weight="bold", pad=6)
    if sub:
        ax.text(0.5, -0.035, sub, transform=ax.transAxes, ha="center",
                va="top", fontsize=9.3, color=CINZA)
    return ax


def secao2d(fig, rect):
    """Secao cotada do pezinho no soquete, no plano XZ."""
    from matplotlib.patches import Polygon, Rectangle as R
    ax = fig.add_axes(rect); ax.set_facecolor("white")
    for sp in ax.spines.values():
        sp.set_color("#e3e0da")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    ax.set_xlim(72, 118); ax.set_ylim(109, 143.5)
    T, L2 = M.TAN, M.LARG / 2
    xe = M.PE_X - M.PE_W - M.SOQ_F
    xd = M.PE_X + M.SOQ_F
    # --- peca de BAIXO -----------------------------------------------------
    pb, eb = "#e07a3c", "#8a3d10"
    # parede: faixa do rim (T_RIM) e parede fina abaixo dela
    ax.add_patch(Polygon([(L2 - M.T_RIM, 116), (L2, 116), (L2, 130),
                          (L2 - M.T_RIM, 130)], closed=True, facecolor=pb,
                         edgecolor=eb, lw=1.3))
    zb = 109
    ax.add_patch(Polygon([(99.55 + zb * T, zb), (99.55 + zb * T + 1.4, zb),
                          (L2 - M.T_RIM + 1.4, 116), (L2 - M.T_RIM, 116)],
                         closed=True, facecolor=pb, edgecolor=eb, lw=1.3))
    ax.add_patch(R((M.PE_X - M.PE_W - 2, 126), L2 - (M.PE_X - M.PE_W - 2), 4,
                   facecolor=pb, edgecolor=eb, lw=1.3))          # berco
    for x0 in (xe - M.SOQ_T, xd):
        ax.add_patch(R((x0, 130), M.SOQ_T, M.SOQ_H, facecolor="#ef7c3a",
                       edgecolor=eb, lw=1.4))                    # soquete
    # --- peca de CIMA ------------------------------------------------------
    pc, ec = "#aeb9c4", "#4a5560"
    ax.add_patch(R((M.PE_X - M.PE_W, 130), M.PE_W, M.H_PE, facecolor=pc,
                   edgecolor=ec, lw=1.4))                        # pezinho
    ax.add_patch(R((72, 130 + M.H_PE), 99.55 + 5 * T - 72, M.T_FUNDO,
                   facecolor=pc, edgecolor=ec, lw=1.4))          # chapa
    ax.add_patch(Polygon([(99.55 + 5 * T - 1.4, 137), (99.55 + 5 * T, 137),
                          (99.55 + 12 * T, 142), (99.55 + 12 * T - 1.4, 142)],
                         closed=True, facecolor=pc, edgecolor=ec, lw=1.4))
    # --- cotas e chamadas --------------------------------------------------
    n = "#c2410c"
    ax.annotate("", (M.PE_X - M.PE_W, 124.2), (M.PE_X, 124.2),
                arrowprops=dict(arrowstyle="<->", color=n, lw=1))
    ax.text(M.PE_X - M.PE_W / 2, 123.0, "13", fontsize=9, color=n,
            ha="center", va="top")
    ax.annotate("", (103.5, 130), (103.5, 135),
                arrowprops=dict(arrowstyle="<->", color=n, lw=1))
    ax.text(104.4, 132.5, "5", fontsize=9, color=n, va="center")
    ax.annotate("soquete de 2 × 2,5\nfolga de 0,6 por lado", (xd + 1, 131.6),
                (112, 140), fontsize=9, color=n, ha="center", va="center",
                arrowprops=dict(arrowstyle="-", color=n, lw=.9))
    ax.annotate("pezinho oco", (M.PE_X - M.PE_W + 3, 132.5), (74, 127),
                fontsize=9, color=ec, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=ec, lw=.9))
    ax.annotate("berço no rim, 4 mm", (100, 128), (100, 117), fontsize=9,
                color=n, ha="center", va="center",
                arrowprops=dict(arrowstyle="-", color=n, lw=.9))
    ax.text(73, 141.6, "peça de CIMA", fontsize=9.6, color=ec, weight="bold")
    ax.text(73, 110.6, "peça de BAIXO", fontsize=9.6, color=eb, weight="bold")
    return ax


def folha(d):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig = plt.figure(figsize=(16.4, 12.2), facecolor=FUNDO)
    fig.text(0.5, 0.982, "O pezinho, e o encaixe do pé traseiro",
             ha="center", va="top", fontsize=21.5, color=TINTA, weight="bold")
    fig.text(0.5, 0.958, "4 pezinhos ocos sob a chapa · e a descoberta de que "
             "empilhar a 130 mm e encaixar são exclusivos", ha="center",
             va="top", fontsize=11.5, color="#3d444d")

    fig.text(0.022, 0.925, "1 · O PEZINHO", fontsize=13, color=NOVO,
             weight="bold", va="top")
    imagem(fig, [0.022, 0.585, 0.30, 0.30], "pe-baixo.png",
           "por baixo", "4 pezinhos ocos de 13 × 20/26, recuados 2 mm da borda")
    imagem(fig, [0.345, 0.585, 0.30, 0.30], "pe-rasante.png",
           "rasante, de fora", "a chapa faz aba: o pé não aparece")
    fig.text(0.668, 0.925, "2 · O ENCAIXE DO PÉ TRASEIRO", fontsize=13,
             color=NOVO, weight="bold", va="top")
    fig.text(0.818, 0.899, "seção cotada no pé traseiro", ha="center",
             va="top", fontsize=12, color=TINTA, weight="bold")
    secao2d(fig, [0.668, 0.585, 0.30, 0.30])
    fig.text(0.818, 0.567, "o pé de cima (cinza) cai no soquete: a pilha não "
             "corre nem para a frente nem para o lado", ha="center", va="top",
             fontsize=9.3, color=CINZA)

    fig.text(0.022, 0.508, "3 · E AQUI ESTÁ O PROBLEMA", fontsize=13,
             color=NOVO, weight="bold", va="top")
    imagem(fig, [0.022, 0.135, 0.30, 0.33], "pe-P-pilha.png",
           "P · com soquete", f"empilha a {d['P']['passo']:.0f} mm — "
           "e NÃO encaixa")
    imagem(fig, [0.345, 0.135, 0.30, 0.33], "pe-N-pilha.png",
           "N · sem soquete", f"encaixa a {d['N']['passo']:.1f} mm"
           .replace(".", ",") + " — e não empilha a 130")

    bx = fig.add_axes([0.668, 0.135, 0.30, 0.33]); bx.axis("off")
    bx.set_xlim(0, 1); bx.set_ylim(0, 1)
    bx.add_patch(Rectangle((0, 0), 1, 1, transform=bx.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.3))
    bx.text(0.06, 0.95, "POR QUE SÃO EXCLUSIVOS", fontsize=11.5, color=NOVO,
            weight="bold", va="top")
    txt = ("Para empilhar a 130 mm, algo tem de segurar a peça de cima dentro "
           "da boca da de baixo. Para encaixar, nada pode estar ali.\n\n"
           "A chapa da peça de cima tem 99,9 mm de meia-largura. O soquete "
           "deixa 82,5 mm de abertura livre. Não passa.\n\n"
           "Girar 180° não salva: os pezinhos se desviam dos soquetes, mas a "
           "chapa e a parede passam por todo y. Medido: 127,6 mm girada.\n\n"
           "Medido no sólido, não estimado: busca binária do menor "
           "deslocamento sem interpenetração.")
    y = 0.85
    for par in txt.split("\n\n"):
        bx.text(0.06, y, "\n".join(textwrap.wrap(par, 40)), fontsize=9.2,
                color=TINTA, va="top", linespacing=1.5)
        y -= 0.055 + 0.038 * len(textwrap.wrap(par, 40))

    fb = fig.add_axes([0.022, 0.018, 0.946, 0.082]); fb.axis("off")
    fb.set_xlim(0, 1); fb.set_ylim(0, 1)
    fb.add_patch(Rectangle((0, 0), 1, 1, transform=fb.transAxes,
                           facecolor="#f4f6f4", edgecolor="#dfe5df", lw=1.2))
    fb.text(0.012, 0.76, "10 peças na caixa: " +
            f"{130 + 9*d['N']['passo']:.0f} mm encaixadas (N) contra "
            f"{130 + 9*d['P']['passo']:.0f} mm empilhadas (P) — "
            "a versão que encaixa cabe em metade da caixa.",
            fontsize=10.4, color=TINTA, va="center")
    fb.text(0.012, 0.42, "Pesos: N " + f"{d['N']['peso']:.1f}".replace(".", ",")
            + " g · P " + f"{d['P']['peso']:.1f}".replace(".", ",") +
            " g. Os pezinhos substituem a saia de 6 mm e a peça ficou MAIS "
            "leve: 162,6 contra 167,6 g. Capacidade 4,46 L.",
            fontsize=10.4, color=CINZA, va="center")
    fb.text(0.012, 0.13, "Correção: eu vinha citando 601 mm para 10 peças "
            "encaixadas sem nunca ter medido. Com os berços que eu mesmo "
            "coloquei, o passo era 130 mm — a peça não encaixava.",
            fontsize=10.4, color=NOVO, va="center")
    fig.savefig(os.path.join(DEST, "pezinho.png"), dpi=118, facecolor=FUNDO)
    print("gerado pezinho.png")


if __name__ == "__main__":
    main()
