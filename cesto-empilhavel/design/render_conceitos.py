#!/usr/bin/env python3
"""Renderiza os solidos dos conceitos: uma vista 3/4 e uma de topo por peca.

Le os STL que conceitos3d.py deixou em design/stl/. Nao constroi nada.

Uso:  python3 render_conceitos.py [n ...]
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "cad"))

import trimesh

import render

DEST = os.path.dirname(os.path.abspath(__file__))
STL = os.path.join(DEST, "stl")
IMG = os.path.join(DEST, "img")

COR = (0.902, 0.878, 0.839)          # off-white quente: leitura de produto
FUNDO = (0.976, 0.969, 0.957)
# A camera fica do lado OPOSTO ao vetor: com y negativo ela cai atras da
# peca e a frente -- onde moram o arco, o chanfro e a tapa, ou seja o lado
# que quase todo conceito mexe -- some. O 3/4 tem de vir de y positivo.
VISTAS = {"34": (-1.0, 1.42, -0.60), "topo": (-0.18, 0.30, -1.0)}


def torre(base, m, pitch=130.0):
    """Duas pecas empilhadas: e o conceito 10 inteiro. Sozinha, a peca nao
    mostra do que ele se trata."""
    c = m.copy()
    c.apply_translation([0, 21.0, pitch])
    img = render.render([(m, COR), (c, COR)], direcao=VISTAS["34"],
                        largura=1000, fundo=FUNDO, margem=0.07)
    render.salvar(img, os.path.join(IMG, f"{base}-torre.png"))


def main(quais=None):
    os.makedirs(IMG, exist_ok=True)
    for arq in sorted(os.listdir(STL)):
        if not arq.endswith(".stl"):
            continue
        n = int(arq[1:3])
        if quais and n not in quais:
            continue
        m = trimesh.load(os.path.join(STL, arq))
        base = arq[:-4]
        for nome, d in VISTAS.items():
            img = render.render([(m, COR)], direcao=d, largura=1000,
                                fundo=FUNDO, margem=0.07)
            render.salvar(img, os.path.join(IMG, f"{base}-{nome}.png"))
        if n in (0, 10):
            torre(base, m)
        print(f"  {base}")


if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:] if a.isdigit()] or None)
