#!/usr/bin/env python3
"""Opcoes CAMUFLADAS de acoplamento -- D e E -- contra a C, ja rejeitada.

D - canaleta embutida rasa: a canaleta e cavada DENTRO da faixa do rim, o que
    so e possivel com gaveta lateral. Em troca o trilho avanca 1,8 mm em vez de
    7,5, o rim fica inteiro nos dois lados e a peca fica simetrica.
E - travas nas pontas: sem gaveta, mas o ressalto passa a ser a parede nua de
    1,4 mm em vez do rim de 3,2, o avanco cai para 5,0 mm e as duas janelas vao
    para as PONTAS da lateral, junto dos cantos, deixando o meio do rim inteiro.

Uso:  python3 camufladas.py
"""
import os
import textwrap

import numpy as np
import trimesh
from build123d import Box, Pos, export_step, export_stl

import modelo3d as M
import render

DEST = os.path.dirname(os.path.abspath(__file__))
COR_A, COR_B = (0.93, 0.44, 0.13), (0.72, 0.30, 0.08)
FUNDO, TINTA, CINZA, NOVO = "#fbfaf8", "#1f2328", "#6b7280", "#c2410c"
VERDE = "#15803d"

OPCOES = [
    ("D", "canaleta embutida rasa", 1.8,
     "canaleta cavada dentro da faixa · trilho de 1,8 mm · rim inteiro nos "
     "dois lados · simétrico · trava na extensão toda",
     "exige 2 gavetas laterais (~USD 3 mil) e deixa linha de junta na lateral"),
    ("E", "travas nas pontas", 5.0,
     "sem gaveta · o meio do rim fica inteiro · as duas quebras ficam junto "
     "dos cantos, onde o olho já espera uma quina",
     "ainda aparece: 5 mm de avanço, e o ressalto é a parede nua de 1,4 mm"),
    ("C", "canaleta aparente (a rejeitada)", 7.5,
     "—",
     "7,5 mm de avanço e duas ameias no meio do rim"),
]


def montar(letra):
    p, n = M.cesto(letra)
    export_step(p, os.path.join(DEST, f"var-{letra}.step"))
    export_stl(p, os.path.join(DEST, f"var-{letra}.stl"))
    m = trimesh.load(os.path.join(DEST, f"var-{letra}.stl"))
    passo = M.passo_acoplado(letra)
    mb = m.copy(); mb.apply_translation([passo, 0, 0])
    inter = (p & (Pos(passo, 0, 0) * p)).volume
    z0 = M.Z_D0 - 10 if letra in ("D", "E") else M.Z_B0 - 10
    bloco = Pos(passo / 2, (30 + 130) / 2, (z0 + 135) / 2) * \
        Box(80.0, 100.0, 135 - z0)
    sa, sb = p & bloco, (Pos(passo, 0, 0) * p) & bloco
    export_stl(sa, os.path.join(DEST, f"var-{letra}-sa.stl"))
    export_stl(sb, os.path.join(DEST, f"var-{letra}-sb.stl"))
    ma = trimesh.load(os.path.join(DEST, f"var-{letra}-sa.stl"))
    mbs = trimesh.load(os.path.join(DEST, f"var-{letra}-sb.stl"))
    vistas = {
        "planta": ([(m, COR_A)], (0.0, 0.0008, -1.0)),
        "frente": ([(m, COR_A)], (0.0, -1.0, 0.0)),
        "cima": ([(m, COR_A)], (-0.60, -0.90, -1.10)),
        "par": ([(m, COR_A), (mb, COR_B)], (-0.90, -1.20, -0.75)),
        "det": ([(ma, COR_A), (mbs, COR_B)], (0.12, -1.00, -0.30)),
    }
    for nome, (cena, d) in vistas.items():
        render.salvar(render.render(cena, direcao=d, largura=1150),
                      os.path.join(DEST, f"cam-{letra}-{nome}.png"))
    return dict(peso=p.volume * M.RHO, inter=inter,
                larg=p.bounding_box().size.X)


def normalizar(letras, largs, vistas=("planta", "frente")):
    """Poe as vistas ortogonais todas na mesma escala mm/pixel.

    render() enquadra cada cena pela propria largura, entao a peca mais larga
    sairia desenhada menor -- justamente a que se quer mostrar maior.
    """
    from PIL import Image
    lmax = max(largs.values())
    for v in vistas:
        imgs = {L: Image.open(os.path.join(DEST, f"cam-{L}-{v}.png"))
                for L in letras}
        W = max(i.width for i in imgs.values())
        H = max(int(round(i.height * lmax / largs[L]))
                for L, i in imgs.items())
        for L, im in imgs.items():
            f = largs[L] / lmax
            pq = im.resize((max(1, int(round(im.width * f))),
                            max(1, int(round(im.height * f)))),
                           Image.LANCZOS)
            tela = Image.new("RGB", (W, H), (246, 245, 243))
            tela.paste(pq, ((W - pq.width) // 2, (H - pq.height) // 2))
            tela.save(os.path.join(DEST, f"cam-{L}-{v}.png"))


def imagem(fig, rect, arq):
    from PIL import Image
    ax = fig.add_axes(rect)
    ax.imshow(np.asarray(Image.open(os.path.join(DEST, arq))))
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#e3e0da")
    return ax


def folha_camuflagem(d):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(16.2, 10.6), facecolor=FUNDO)
    fig.text(0.5, 0.980, "Quanto cada uma aparece", ha="center", va="top",
             fontsize=21, color=TINTA, weight="bold")
    fig.text(0.5, 0.955, "vistas ortogonais, sem perspectiva — é o teste de "
             "camuflagem · a C é a que você recusou", ha="center", va="top",
             fontsize=11.5, color="#3d444d")
    ordem = ["C", "E", "D"]
    for j, L in enumerate(ordem):
        nome = next(o[1] for o in OPCOES if o[0] == L)
        sal = next(o[2] for o in OPCOES if o[0] == L)
        x = 0.035 + j * 0.322
        fig.text(x + 0.145, 0.925, f"{L} · {nome}", ha="center", va="top",
                 fontsize=13, color=TINTA if L != "C" else CINZA, weight="bold")
        cor = NOVO if L == "D" else (TINTA if L == "E" else CINZA)
        fig.text(x + 0.145, 0.901,
                 f"avanço de {sal:.1f} mm".replace(".", ",") +
                 f"  ·  envelope {d[L]['larg']:.1f} mm".replace(".", ","),
                 ha="center", va="top", fontsize=10.5, color=cor)
        imagem(fig, [x, 0.505, 0.29, 0.375], f"cam-{L}-planta.png")
        imagem(fig, [x, 0.095, 0.29, 0.375], f"cam-{L}-frente.png")
    fig.text(0.012, 0.69, "PLANTA", rotation=90, ha="left", va="center",
             fontsize=11.5, color=NOVO, weight="bold")
    fig.text(0.012, 0.28, "FRENTE", rotation=90, ha="left", va="center",
             fontsize=11.5, color=NOVO, weight="bold")
    fig.text(0.035, 0.055, "A peça tem 215 mm de boca. O que passa disso é o "
             "que se vê: a C põe 7,5 mm de cada lado, a E 5,0, a D 1,8.",
             fontsize=10.5, color=TINTA, va="center")
    fig.text(0.035, 0.028, "Na planta da D o trilho quase não sai do contorno "
             "do rim, e do lado fêmea não há quebra nenhuma no fio do rim.",
             fontsize=10.5, color=CINZA, va="center")
    fig.savefig(os.path.join(DEST, "camufladas-frente.png"), dpi=118,
                facecolor=FUNDO)
    print("gerado camufladas-frente.png")


def folha_3d(d):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig = plt.figure(figsize=(16.4, 10.4), facecolor=FUNDO)
    fig.text(0.5, 0.978, "As duas camufladas, em 3D", ha="center", va="top",
             fontsize=21, color=TINTA, weight="bold")
    fig.text(0.5, 0.953, "mesma peça, mesmo pé, mesma silhueta · 17/09/2026",
             ha="center", va="top", fontsize=11.5, color="#3d444d")
    cols = [("cima", "a peça sozinha, vista de cima",
             "à direita o macho, à esquerda a fêmea"),
            ("par", "duas acopladas", "é assim que ficam no estoque"),
            ("det", "seção do encaixe", "corte no rim, no plano da junta")]
    x0, larg, gap = 0.150, 0.270, 0.011
    for j, (_, tit, sub) in enumerate(cols):
        cx = x0 + j * (larg + gap) + larg / 2
        fig.text(cx, 0.928, tit, ha="center", va="top", fontsize=12.5,
                 color=TINTA, weight="bold")
        fig.text(cx, 0.906, sub, ha="center", va="top", fontsize=9.5, color=CINZA)
    h = 0.355
    for i, (letra, nome, sal, ganha, custa) in enumerate(OPCOES[:2]):
        y = 0.520 - i * 0.390
        tx = fig.add_axes([0.020, y, 0.122, h]); tx.axis("off")
        tx.set_xlim(0, 1); tx.set_ylim(0, 1)
        tx.text(0, 1.0, letra, fontsize=36, color=NOVO, weight="bold", va="top")
        tx.text(0, 0.79, "\n".join(textwrap.wrap(nome, 18)), fontsize=12.5,
                color=TINTA, weight="bold", va="top", linespacing=1.35)
        tx.text(0, 0.60, f"{d[letra]['peso']:.1f}".replace(".", ",") + " g",
                fontsize=15, color=TINTA, va="top")
        tx.text(0, 0.525, f"avanço {sal:.1f} mm".replace(".", ","),
                fontsize=9.5, color=CINZA, va="top")
        tx.text(0, 0.45, "\n".join(textwrap.wrap("ganha: " + ganha, 29)),
                fontsize=8.5, color=VERDE, va="top", linespacing=1.45)
        tx.text(0, 0.16, "\n".join(textwrap.wrap("custa: " + custa, 29)),
                fontsize=8.5, color=NOVO, va="top", linespacing=1.45)
        for j, (col, _, _) in enumerate(cols):
            imagem(fig, [x0 + j * (larg + gap), y, larg, h],
                   f"cam-{letra}-{col}.png")
    bx = fig.add_axes([0.020, 0.016, 0.962, 0.040]); bx.axis("off")
    bx.set_xlim(0, 1); bx.set_ylim(0, 1)
    bx.add_patch(Rectangle((0, 0), 1, 1, transform=bx.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.2))
    it = " · ".join(f"{k} {d[k]['inter']:.0f}" for k in ("D", "E"))
    bx.text(0.014, 0.72, f"Interseção entre as duas peças acopladas (mm³): {it}."
            "  A D entra deslizando pela frente e encosta no fundo da canaleta; "
            "a E trava por descida. As duas mantêm encaixe e empilhamento de "
            "130 mm.", fontsize=10.2, color=TINTA, va="center")
    bx.text(0.014, 0.26, "Pesos: D " +
            f"{d['D']['peso']:.1f}".replace(".", ",") + " g · E " +
            f"{d['E']['peso']:.1f}".replace(".", ",") + " g · contra 177,4 a "
            "187,8 g das A/B/C, e 163,7 g da peça sem acoplamento.",
            fontsize=10.2, color=CINZA, va="center")
    fig.savefig(os.path.join(DEST, "camufladas.png"), dpi=118, facecolor=FUNDO)
    print("gerado camufladas.png")


if __name__ == "__main__":
    dados = {}
    for L, *_ in OPCOES:
        dados[L] = montar(L)
        print(f"{L}: peso {dados[L]['peso']:6.1f} g | envelope "
              f"{dados[L]['larg']:.1f} mm | interferencia "
              f"{dados[L]['inter']:.2f} mm3")
    normalizar([L for L, *_ in OPCOES],
               {L: dados[L]["larg"] for L, *_ in OPCOES})
    folha_camuflagem(dados)
    folha_3d(dados)
