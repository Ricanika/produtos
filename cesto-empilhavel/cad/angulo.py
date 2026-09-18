#!/usr/bin/env python3
"""Mais saida de molde + o pe virando o fundo da nervura.

EMPILHAR (uma sobre a outra, varios andares)  -> girada 180, passo ALT+pino
ENCAIXAR (uma dentro da outra, transporte)    -> mesma orientacao
ACOPLAR  (lado a lado)                        -> cauda de andorinha nas paredes
"""
import os
import textwrap

import numpy as np
import trimesh
from build123d import export_step, export_stl

import modelo3d as M
import render
from empilha import passo

DEST = os.path.dirname(os.path.abspath(__file__))
COR, COR2 = (0.93, 0.44, 0.13), (0.72, 0.30, 0.08)
FUNDO, TINTA, GRIS, NOVO, VERDE = "#fbfaf8", "#1f2328", "#6b7280", "#c2410c", "#15803d"
SAIDA = 9.0


def gira(m):
    t = m.copy()
    t.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [0, 0, 1]))
    return t


def coluna(m, n, pas, alterna, arq, larg=980):
    cena = []
    for i in range(n):
        t = (gira(m) if (alterna and i % 2) else m.copy())
        t.apply_translation([0, 0, i * pas])
        cena.append((t, COR if i % 2 == 0 else COR2))
    render.salvar(render.render(cena, direcao=(-1.0, -1.22, -0.5), largura=larg),
                  os.path.join(DEST, arq))


def main():
    M.set_draft(SAIDA)
    p, n = M.cesto(None, h_rim=M.H_FAIXA2, estrutura=True)
    export_step(p, os.path.join(DEST, f"cesto-{SAIDA:.0f}g.step"))
    export_stl(p, os.path.join(DEST, f"cesto-{SAIDA:.0f}g.stl"))
    m = trimesh.load(os.path.join(DEST, f"cesto-{SAIDA:.0f}g.stl"))
    pn = passo(p, lo=40.0, hi=150.0)
    ps = passo(p, True, lo=100.0, hi=170.0)
    peso, cap = p.volume * M.RHO, M.capacidade()
    print(f"saida {SAIDA}: peso {peso:.1f} g | cap {cap:.2f} L | "
          f"encaixa {pn:.1f} | empilha {ps:.1f}")

    render.salvar(render.render([(m, COR)], direcao=(-0.9, -1.2, -0.62),
                                largura=980),
                  os.path.join(DEST, "ang-peca.png"))
    coluna(m, 3, ps, True, "ang-pilha.png")
    coluna(m, 6, pn, False, "ang-encaixe.png")
    # referencia: a mesma peca sem a estrutura de empilhamento
    q, _ = M.cesto(None, h_rim=M.H_FAIXA2)
    export_stl(q, os.path.join(DEST, "ang-sem.stl"))
    mq = trimesh.load(os.path.join(DEST, "ang-sem.stl"))
    pq = passo(q, lo=5.0, hi=90.0)
    coluna(mq, 6, pq, False, "ang-sem.png")
    print(f"sem estrutura: encaixa {pq:.1f} mm")
    folha(peso, cap, pn, ps, pq, n)


def painel(fig, x, yb, arq, tit, cota, cor, sub, w=0.30, h=0.325):
    """Titulo, cota e legenda em posicoes FIXAS da figura.

    imshow forca aspecto e encolhe o eixo -- titulo preso ao eixo anda junto e
    acaba invadindo a linha de baixo.
    """
    from PIL import Image
    fig.text(x + w / 2, yb + h + 0.040, tit, ha="center", va="bottom",
             fontsize=12.5, color=TINTA, weight="bold")
    fig.text(x + w / 2, yb + h + 0.016, cota, ha="center", va="bottom",
             fontsize=11.5, color=cor, weight="bold")
    ax = fig.add_axes([x, yb, w, h])
    ax.imshow(np.asarray(Image.open(os.path.join(DEST, arq))))
    ax.set_anchor("N")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#e3e0da")
    fig.text(x + w / 2, yb - 0.012, "\n".join(textwrap.wrap(sub, 44)),
             ha="center", va="top", fontsize=9.4, color=GRIS, linespacing=1.45)


def folha(peso, cap, pn, ps, pq, furos):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig = plt.figure(figsize=(16.4, 12.6), facecolor=FUNDO)
    fig.text(0.5, 0.990, "Mais angulo — e a conta que decide o resto"
             .replace("angulo", "ângulo"), ha="center", va="top",
             fontsize=21.5, color=TINTA, weight="bold")
    fig.text(0.5, 0.965, f"saída de molde de 3,5° → {SAIDA:.0f}° · o pé virou o "
             "fundo da nervura e é ele que cai no pino", ha="center", va="top",
             fontsize=11.5, color="#3d444d")

    painel(fig, 0.022, 0.545, "ang-peca.png", "a peça a 9°",
           "base 174 × 159 mm", TINTA,
           "mais cônica: a capacidade cai de 4,46 para 3,95 L")
    painel(fig, 0.345, 0.545, "ang-pilha.png", "EMPILHADA",
           f"{ps:.0f} mm por andar", VERDE,
           "girada 180° · o pino de 10 mm aparece entre os andares")
    painel(fig, 0.668, 0.545, "ang-encaixe.png", "ENCAIXADA",
           f"{pn:.1f} mm".replace(".", ",") + " por peça", NOVO,
           f"mesma orientação · 6 peças em {130+5*pn:.0f} mm, "
           f"12 em {130+11*pn:.0f} mm")
    painel(fig, 0.022, 0.115, "ang-sem.png", "SEM a estrutura",
           f"{pq:.1f} mm".replace(".", ",") + " por peça", VERDE,
           f"6 peças em {130+5*pq:.0f} mm, 12 em {130+11*pq:.0f} mm — "
           "mas sem andares: só encaixa")

    bx = fig.add_axes([0.345, 0.115, 0.623, 0.325]); bx.axis("off")
    bx.set_xlim(0, 1); bx.set_ylim(0, 1)
    bx.add_patch(Rectangle((0, 0), 1, 1, transform=bx.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.3))
    bx.text(0.03, 0.95, "A CONTA QUE DECIDE", fontsize=12, color=NOVO,
            weight="bold", va="top")
    bx.text(0.03, 0.855, "passo_encaixe  >=  passo_pilha/2  +  "
            "(rim + apoio + folga) / (2 . tg saida)", fontsize=10.6,
            color=TINTA, va="center", family="monospace")
    bx.text(0.03, 0.755, "\n".join(textwrap.wrap(
        "O pino está no alto e o pé embaixo. Encaixando, os dois se aproximam "
        "ao mesmo tempo — cada milímetro conta duas vezes, e o termo "
        "passo_pilha/2 não some com ângulo nenhum.", 94)),
        fontsize=10.2, color=TINTA, va="top", linespacing=1.5)
    y = 0.575
    cols = ("base", "encaixa", "6 peças", "12 peças", "12 SEM estrut.")
    bx.text(0.03, y, "saída", fontsize=9.6, color=GRIS, weight="bold")
    for j, k in enumerate(cols):
        bx.text(0.27 + j * 0.163, y, k, fontsize=9.6, color=GRIS,
                weight="bold", ha="center")
    y -= 0.078
    for g, base, enc, sem in ((3.5, "199", 106.6, 55.5), (7.0, "183", 86.0, 28.7),
                              (9.0, "174", 82.0, 23.8), (12.0, "160", 78.5, 44.2)):
        forte = abs(g - SAIDA) < 0.1
        cor = NOVO if forte else TINTA
        pesoF = "bold" if forte else "normal"
        bx.text(0.03, y, f"{g:.1f}°".replace(".", ","), fontsize=9.8,
                color=cor, weight=pesoF)
        for j, v in enumerate([base, f"{enc:.1f}".replace(".", ","),
                               f"{130+5*enc:.0f}", f"{130+11*enc:.0f}",
                               f"{130+11*sem:.0f}"]):
            bx.text(0.27 + j * 0.163, y, v, fontsize=9.8, color=cor,
                    ha="center", weight=pesoF)
        y -= 0.072
    bx.plot([0.03, 0.97], [0.205, 0.205], color="#f0d3c2", lw=1)
    bx.text(0.03, 0.168, "\n".join(textwrap.wrap(
        "Medido isolando cada feição: o PINO sozinho já custa todo o encaixe "
        "(82,0 mm com pino só, igual a com pino + nervura). Sem nenhum dos "
        "dois, 22,8 mm. A 9° são 12 peças em 1.032 mm com estrutura contra "
        "381 mm sem — 651 mm de caixa em cada 12 peças.", 94)),
        fontsize=10.2, color=NOVO, va="top", linespacing=1.5)
    fig.savefig(os.path.join(DEST, "angulo.png"), dpi=118, facecolor=FUNDO)
    print("gerado angulo.png")


if __name__ == "__main__":
    main()
