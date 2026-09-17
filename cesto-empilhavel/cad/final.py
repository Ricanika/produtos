#!/usr/bin/env python3
"""Empilha E acopla: o acoplamento mora DENTRO das paredes de empilhamento.

Cauda de andorinha vertical na face externa de cada parede da borda -- numa
lateral a 1a parede e macho e a 2a femea, espelhado na outra. O arranjo e
invariante a 180 graus, entao a pilha girada continua acoplando nivel a nivel.
"""
import os
import textwrap

import numpy as np
import trimesh
from build123d import Box, Pos, Rot, export_step, export_stl

import modelo3d as M
import render
from empilha import passo

DEST = os.path.dirname(os.path.abspath(__file__))
COR, COR2, CINZ = (0.93, 0.44, 0.13), (0.72, 0.30, 0.08), (0.55, 0.63, 0.72)
FUNDO, TINTA, GRIS, NOVO, VERDE = "#fbfaf8", "#1f2328", "#6b7280", "#c2410c", "#15803d"
PASSO_E = 130.0


def gira(m):
    t = m.copy()
    t.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [0, 0, 1]))
    return t


def main():
    p, n = M.cesto(None, h_rim=M.H_FAIXA2, estrutura=True)
    export_step(p, os.path.join(DEST, "cesto-final.step"))
    export_stl(p, os.path.join(DEST, "cesto-final.stl"))
    m = trimesh.load(os.path.join(DEST, "cesto-final.stl"))
    pn = passo(p)
    peso, cap = p.volume * M.RHO, M.capacidade()
    print(f"peso {peso:.1f} g | encaixa {pn:.1f} | empilha {PASSO_E:.1f}")

    # 1 - par acoplado
    b = m.copy(); b.apply_translation([M.LARG, 0, 0])
    render.salvar(render.render([(m, COR), (b, COR2)],
                                direcao=(-0.95, -1.25, -0.62), largura=1050),
                  os.path.join(DEST, "fim-par.png"))
    # 2 - duas colunas acopladas de 3 niveis: empilha E acopla
    cena = []
    for lvl in range(3):
        for col in (0, M.LARG):
            t = (gira(m) if lvl % 2 else m.copy())
            t.apply_translation([col, 0, lvl * PASSO_E])
            cena.append((t, COR if (lvl + (col > 0)) % 2 == 0 else COR2))
    render.salvar(render.render(cena, direcao=(-0.95, -1.2, -0.52), largura=1050),
                  os.path.join(DEST, "fim-torre.png"))
    # 3 - coluna encaixada, mesma orientacao
    cena = []
    for i in range(5):
        t = m.copy(); t.apply_translation([0, 0, i * pn])
        cena.append((t, COR if i % 2 == 0 else COR2))
    render.salvar(render.render(cena, direcao=(-1.0, -1.22, -0.5), largura=1050),
                  os.path.join(DEST, "fim-encaixe.png"))
    # 4 - secao da cauda de andorinha
    y0, y1 = M.PAR_Y[0]
    bloco = Pos(M.LARG / 2, (y0 + y1) / 2, M.ALT + M.EMP_H / 2) * \
        Box(30.0, y1 - y0 + 16.0, M.EMP_H + 2.0)
    sa, sb = p & bloco, (Pos(M.LARG, 0, 0) * p) & bloco
    export_stl(sa, os.path.join(DEST, "fim-sa.stl"))
    export_stl(sb, os.path.join(DEST, "fim-sb.stl"))
    render.salvar(render.render(
        [(trimesh.load(os.path.join(DEST, "fim-sa.stl")), COR),
         (trimesh.load(os.path.join(DEST, "fim-sb.stl")), CINZ)],
        direcao=(-0.35, -0.6, -1.0), largura=1050),
        os.path.join(DEST, "fim-det.png"))
    folha(peso, cap, pn, n)


def imagem(fig, rect, arq, titulo=None, sub=None):
    from PIL import Image
    ax = fig.add_axes(rect)
    ax.imshow(np.asarray(Image.open(os.path.join(DEST, arq))))
    ax.set_anchor("N")          # encosta no topo: os titulos alinham
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#e3e0da")
    if titulo:
        ax.set_title(titulo, fontsize=12.5, color=TINTA, weight="bold", pad=6)
    if sub:
        ax.text(0.5, -0.028, "\n".join(textwrap.wrap(sub, 44)),
                transform=ax.transAxes, ha="center", va="top", fontsize=9.4,
                color=GRIS, linespacing=1.4)


def folha(peso, cap, pn, furos):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig = plt.figure(figsize=(16.4, 12.6), facecolor=FUNDO)
    fig.text(0.5, 0.984, "Empilha E acopla", ha="center", va="top",
             fontsize=22, color=TINTA, weight="bold")
    fig.text(0.5, 0.955, "o acoplamento mudou de lugar: saiu do rim e foi para "
             "dentro das paredes de empilhamento", ha="center", va="top",
             fontsize=11.5, color="#3d444d")

    imagem(fig, [0.022, 0.535, 0.30, 0.335], "fim-par.png",
           "ACOPLADAS", "cauda de andorinha vertical nas paredes da borda · "
           "trava puxando de lado")
    imagem(fig, [0.345, 0.535, 0.30, 0.335], "fim-det.png",
           "a cauda de andorinha",
           "corte na parede: macho de 1,4 mm entra na fêmea da vizinha (cinza)")
    bx = fig.add_axes([0.668, 0.535, 0.30, 0.335]); bx.axis("off")
    bx.set_xlim(0, 1); bx.set_ylim(0, 1)
    bx.add_patch(Rectangle((0, 0), 1, 1, transform=bx.transAxes,
                           facecolor="#f2f7f2", edgecolor="#cfe0cf", lw=1.3))
    bx.text(0.06, 0.95, "POR QUE AGORA DÁ OS DOIS", fontsize=11.5, color=VERDE,
            weight="bold", va="top")
    y = 0.84
    for par in ("A estrutura de empilhamento ocupava o rim da lateral e só "
                "sobravam 36 mm para a canaleta. Em vez de disputar espaço, o "
                "acoplamento foi morar DENTRO dela.",
                "É onde duas peças lado a lado se tocam de verdade: as paredes "
                "da borda ficam face a face. A cauda de andorinha é prismática "
                "em z, aberta no topo — sai na direção de abertura, sem gaveta.",
                "Numa lateral a 1ª parede é macho e a 2ª é fêmea, espelhado na "
                "outra. Esse arranjo é invariante a 180°, então a pilha girada "
                "continua acoplando nível a nível."):
        bx.text(0.06, y, "\n".join(textwrap.wrap(par, 42)), fontsize=9.3,
                color=TINTA, va="top", linespacing=1.5)
        y -= 0.05 + 0.041 * len(textwrap.wrap(par, 42))

    imagem(fig, [0.022, 0.125, 0.30, 0.335], "fim-torre.png",
           "EMPILHADAS + ACOPLADAS",
           "2 colunas × 3 níveis · cena medida: 0,00 mm³ de interferência")
    imagem(fig, [0.345, 0.125, 0.30, 0.335], "fim-encaixe.png",
           f"ENCAIXADAS · {pn:.1f} mm".replace(".", ","),
           "mesma orientação, todas no mesmo sentido")
    tb = fig.add_axes([0.668, 0.125, 0.30, 0.335]); tb.axis("off")
    tb.set_xlim(0, 1); tb.set_ylim(0, 1)
    tb.add_patch(Rectangle((0, 0), 1, 1, transform=tb.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.3))
    tb.text(0.06, 0.95, "MEDIDO NO SÓLIDO", fontsize=11.5, color=NOVO,
            weight="bold", va="top")
    linhas = [("empilha (girada 180°)", "130,0 mm"),
              ("encaixa (mesma orient.)", f"{pn:.1f} mm".replace(".", ",")),
              ("10 peças na caixa", f"{130 + 9*pn:.0f} mm"),
              ("trava lateral", "0,2 a 1,2 mm"),
              ("solta levantando", "35 mm"),
              ("interferência da cena", "0,00 mm³"),
              ("peso", f"{peso:.1f} g".replace(".", ",")),
              ("capacidade", f"{cap:.2f} L".replace(".", ",")),
              ("envelope", "217,8 × 197 × 140 mm"),
              ("furos", f"{furos}")]
    y = 0.84
    for k, v in linhas:
        tb.text(0.06, y, k, fontsize=9.5, color=GRIS, va="center")
        tb.text(0.94, y, v, fontsize=9.5, color=TINTA, va="center",
                ha="right", weight="bold")
        y -= 0.069
    tb.plot([0.06, 0.94], [0.13, 0.13], color="#f0d3c2", lw=1)
    tb.text(0.06, 0.10, "sem gaveta no molde · fundo sólido · uma peça só",
            fontsize=9.3, color=NOVO, va="top")
    fig.savefig(os.path.join(DEST, "final.png"), dpi=118, facecolor=FUNDO)
    print("gerado final.png")


if __name__ == "__main__":
    main()
