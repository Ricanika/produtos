#!/usr/bin/env python3
"""So existem DUAS posicoes: 0 e 180 graus. Um dos dois modos sera o girado.

Compara as tres saidas possiveis:
  Q  - empilha na mesma orientacao, encaixa girando   (o que eu tinha feito)
  Q' - encaixa na mesma orientacao, empilha girando   (o que o cliente pediu)
  N  - so encaixa, na mesma orientacao, a 55,5 mm     (sem estrutura)
"""
import os
import textwrap

import numpy as np
import trimesh
from build123d import export_stl

import modelo3d as M
import render
from empilha import passo

DEST = os.path.dirname(os.path.abspath(__file__))
COR, COR2 = (0.93, 0.44, 0.13), (0.72, 0.30, 0.08)
FUNDO, TINTA, GRIS, NOVO, VERDE = "#fbfaf8", "#1f2328", "#6b7280", "#c2410c", "#15803d"


def gira(m):
    t = m.copy()
    t.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [0, 0, 1]))
    return t


def coluna(m, n, pas, alterna, arq):
    cena = []
    for i in range(n):
        t = (gira(m) if (alterna and i % 2) else m.copy())
        t.apply_translation([0, 0, i * pas])
        cena.append((t, COR if i % 2 == 0 else COR2))
    render.salvar(render.render(cena, direcao=(-1.0, -1.22, -0.5), largura=980),
                  os.path.join(DEST, arq))


def main():
    pq, _ = M.cesto("D", estrutura=True)
    export_stl(pq, os.path.join(DEST, "ori-q.stl"))
    mq = trimesh.load(os.path.join(DEST, "ori-q.stl"))
    pe_q, pg_q = passo(pq), passo(pq, True)

    pn, _ = M.cesto("D")
    export_stl(pn, os.path.join(DEST, "ori-n.stl"))
    mn = trimesh.load(os.path.join(DEST, "ori-n.stl"))
    pe_n = passo(pn)

    coluna(mq, 5, pe_q, False, "ori-q-encaixe.png")
    coluna(mq, 3, pg_q, True, "ori-q-pilha.png")
    coluna(mn, 5, pe_n, False, "ori-n-encaixe.png")
    print(f"Q' encaixe mesma orientacao {pe_q:.1f} | pilha girada {pg_q:.1f} | "
          f"peso {pq.volume*M.RHO:.1f} g")
    print(f"N  encaixe mesma orientacao {pe_n:.1f} | peso {pn.volume*M.RHO:.1f} g")
    folha(pe_q, pg_q, pe_n, pq.volume * M.RHO, pn.volume * M.RHO)


def folha(pe_q, pg_q, pe_n, peso_q, peso_n):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from PIL import Image
    fig = plt.figure(figsize=(16.4, 11.0), facecolor=FUNDO)
    fig.text(0.5, 0.982, "Só existem duas posições: 0° e 180°",
             ha="center", va="top", fontsize=21.5, color=TINTA, weight="bold")
    fig.text(0.5, 0.942, "um dos dois modos vai ser o girado — a escolha é qual",
             ha="center", va="top", fontsize=11.5, color="#3d444d")

    cols = [("ori-q-encaixe.png", "ENCAIXA · mesma orientação",
             f"{pe_q:.1f} mm".replace(".", ",") + " · 10 peças "
             f"{130+9*pe_q:.0f} mm", VERDE,
             "é o que você pediu: todas no mesmo sentido, entrando uma na outra"),
            ("ori-q-pilha.png", "EMPILHA · girando 180°",
             f"{pg_q:.0f} mm", NOVO,
             "o preço: o chanfro alterna frente/trás a cada nível"),
            ("ori-n-encaixe.png", "N · sem estrutura",
             f"{pe_n:.1f} mm".replace(".", ",") + " · 10 peças "
             f"{130+9*pe_n:.0f} mm", VERDE,
             "mesma orientação, nada no caminho — mas não empilha a 130")]
    for j, (arq, tit, cota, cor, sub) in enumerate(cols):
        x = 0.028 + j * 0.324
        fig.text(x + 0.145, 0.912, tit, ha="center", va="top", fontsize=12.5,
                 color=TINTA, weight="bold")
        fig.text(x + 0.145, 0.889, cota, ha="center", va="top", fontsize=11.5,
                 color=cor, weight="bold")
        ax = fig.add_axes([x, 0.30, 0.29, 0.572])
        ax.imshow(np.asarray(Image.open(os.path.join(DEST, arq))))
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#e3e0da")
        fig.text(x + 0.145, 0.285, "\n".join(textwrap.wrap(sub, 46)),
                 ha="center", va="top", fontsize=9.6, color=GRIS,
                 linespacing=1.4)

    bx = fig.add_axes([0.028, 0.032, 0.944, 0.185]); bx.axis("off")
    bx.set_xlim(0, 1); bx.set_ylim(0, 1)
    bx.add_patch(Rectangle((0, 0), 1, 1, transform=bx.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.3))
    bx.text(0.012, 0.88, "A REGRA", fontsize=11.5, color=NOVO, weight="bold",
            va="top")
    bx.text(0.012, 0.64, "\n".join(textwrap.wrap(
        "Trocar entre encaixar e empilhar exige DUAS posições. Numa peça "
        "injetada de uma só vez, a única segunda posição é girar 180° — não há "
        "outra. Então um dos dois modos é o girado, e as cotas são as mesmas "
        "nos dois casos: 102,7 e 130 mm.", 130)),
        fontsize=10.2, color=TINTA, va="center", linespacing=1.55)
    bx.text(0.012, 0.33, "\n".join(textwrap.wrap(
        "Se você quiser os dois modos SEM girar nada, a saída é a silhueta "
        "ficar simétrica frente/trás (chanfro nas duas pontas): aí girar não se "
        "vê. Custa ~0,4 L de capacidade e aperta o rim, que hoje divide espaço "
        "com a canaleta de acoplamento.", 130)),
        fontsize=10.2, color=GRIS, va="center", linespacing=1.55)
    bx.text(0.012, 0.09, f"Pesos: Q' {peso_q:.1f} g".replace(".", ",") +
            f" · N {peso_n:.1f} g".replace(".", ",") +
            ".  Na Q' a canaleta de acoplamento cai de 80 para 36 mm — a "
            "estrutura ocupa o rim da lateral.",
            fontsize=10.2, color=NOVO, va="center")
    fig.savefig(os.path.join(DEST, "orientacao.png"), dpi=118, facecolor=FUNDO)
    print("gerado orientacao.png")


if __name__ == "__main__":
    main()
