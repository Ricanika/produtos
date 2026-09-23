#!/usr/bin/env python3
"""Aba plana no rim + pes com cavidade interna.

Os tres pedidos desta rodada, medidos no solido:
  1. empilhar na MESMA orientacao do encaixe (mesma frente, sem inverter);
  2. uma parte plana de ~1 cm em toda a borda, e nela que o pe pousa;
  3. cavidade interna nos pes, para eles se engolirem no transporte.
"""
import os
import textwrap

import numpy as np
import trimesh
from build123d import Box, Pos, export_step, export_stl

import modelo3d as M
import render
import cortes

DEST = os.path.dirname(os.path.abspath(__file__))
COR, COR2, CINZ = (0.93, 0.44, 0.13), (0.72, 0.30, 0.08), (0.55, 0.63, 0.72)
FUNDO, TINTA, GRIS = "#fbfaf8", "#1f2328", "#6b7280"
NOVO, VERDE = "#c2410c", "#15803d"
DESLOC = None          # vem de modelo3d.DESLOC (14 mm)
PASSO_E = 130.0


def passo_xy(p, dy=0.0, lo=0.0, hi=180.0, tol=0.02):
    """Menor deslocamento vertical sem interferencia, com a peca de cima
    tambem deslocada dy em y. E a medida que arbitra tudo neste projeto."""
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if (p & (Pos(0, dy, mid) * p)).volume > 2.0:
            lo = mid
        else:
            hi = mid
    return hi


def apoios(p, dy, passo, eps=0.3):
    """As manchas de contato do andar de cima, medidas: baixa eps alem do
    passo e cada solido da interseccao e um apoio. Area = volume / eps."""
    try:
        inter = p & (Pos(0, dy, passo - eps) * p)
    except Exception:
        return []
    out = [(s.volume / eps, s.bounding_box())
           for s in inter.solids() if s.volume > 0.005]
    return sorted(out, key=lambda t: -t[0])


def folga_friso(p, dy, passo, eixo):
    """Quanto o andar de cima anda no eixo antes de o friso bater.

    E o numero que importa para a MONTAGEM: folga pequena demais e a peca nem
    assenta (a propria injecao varia ±0,4 mm em 200 mm de PP)."""
    d = {"x": (1, 0), "y": (0, 1)}[eixo]
    lo, hi = 0.0, 4.0
    while hi - lo > 0.05:
        mid = (lo + hi) / 2
        try:
            v = (p & (Pos(mid * d[0], dy + mid * d[1], passo) * p)).volume
        except Exception:
            v = 0.0
        if v > 0.05:
            hi = mid
        else:
            lo = mid
    return hi


def stl(s, nome):
    export_stl(s, os.path.join(DEST, nome))
    return trimesh.load(os.path.join(DEST, nome))


def main():
    global DESLOC
    M.padrao()
    DESLOC = M.DESLOC
    p, n = M.cesto(aba=True)
    export_step(p, os.path.join(DEST, "cesto-aba.step"))
    m = stl(p, "cesto-aba.stl")
    pn = passo_xy(p, 0.0)
    pe = passo_xy(p, DESLOC)
    peso, cap = p.volume * M.RHO, M.capacidade()
    bb = p.bounding_box()
    hz = bb.size.Z
    trava = [(dx, (p & (Pos(M.passo_acoplado() + dx, 0, 0) * p)).volume)
             for dx in (0.0, 0.6, 1.2, 2.0)]
    solta = [(dz, (p & (Pos(M.passo_acoplado() + 1.2, 0, dz) * p)).volume)
             for dz in (0.0, 8.0, 15.0)]
    # A altura que solta e DERIVADA da junta (ABA_T + ABA_DOBRA), nao um 15
    # digitado: a tabela desta folha trazia 15 mm da versao com a aba para
    # dentro, onde a femea escavava a faixa inteira do rim.
    lo, hi = 0.0, 20.0
    while hi - lo > 0.05:
        mid = (lo + hi) / 2
        if (p & (Pos(M.passo_acoplado() + 1.2, 0, mid) * p)).volume > 0.0:
            lo = mid
        else:
            hi = mid
    h_solta = hi
    print(f"peso {peso:.1f} g | cap {cap:.2f} L | encaixa {pn:.1f} | "
          f"empilha {pe:.1f} (dy {DESLOC:.0f})")
    ap = apoios(p, DESLOC, pe)
    a_tot = sum(a for a, _ in ap)
    fx, fy = folga_friso(p, DESLOC, pe, "x"), folga_friso(p, DESLOC, pe, "y")
    print(f"trava {trava}\nsolta {solta}")
    print(f"apoios {len(ap)} · {a_tot:.0f} mm2 · " +
          " | ".join(f"{a:.0f}" for a, _ in ap))
    print(f"folga do friso: x ±{fx:.2f} mm, y ±{fy:.2f} mm")

    # 1 - a peca
    render.salvar(render.render([(m, COR)], direcao=(-0.95, -1.25, -0.70),
                                largura=1050),
                  os.path.join(DEST, "aba-peca.png"))

    # 2 e 3 - os cortes no pe: cortes.py, em 2D tirado do solido. De perto
    # o rasterizador 3D vira bloco de cor; o corte em linha se le.
    cortes.main(pn, max((a for a, _ in ap), default=None))

    # 4 - coluna encaixada de 6
    cena = []
    for i in range(6):
        t = m.copy()
        t.apply_translation([0, 0, i * pn])
        cena.append((t, COR if i % 2 == 0 else COR2))
    render.salvar(render.render(cena, direcao=(-1.0, -1.25, -0.52),
                                largura=1050),
                  os.path.join(DEST, "aba-col.png"))

    # 5 - pilha de 3 andares, mesma frente, deslocando 10 mm alternado
    cena = []
    for lvl in range(3):
        for col in (0, M.LARG):
            t = m.copy()
            dy = lvl * DESLOC        # o deslocamento e cumulativo
            t.apply_translation([col, dy, lvl * PASSO_E])
            cena.append((t, COR if (lvl + (col > 0)) % 2 == 0 else COR2))
    render.salvar(render.render(cena, direcao=(-0.95, -1.2, -0.5),
                                largura=1050),
                  os.path.join(DEST, "aba-torre.png"))

    folha(peso, cap, pn, pe, n, trava, solta, hz, bb, h_solta,
          len(ap), a_tot, fx, fy)


def imagem(fig, rect, arq, titulo=None, sub=None):
    from PIL import Image
    ax = fig.add_axes(rect)
    ax.imshow(np.asarray(Image.open(os.path.join(DEST, arq))))
    ax.set_anchor("N")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#e3e0da")
    if titulo:
        ax.set_title(titulo, fontsize=12.5, color=TINTA, weight="bold", pad=6)
    if sub:
        ax.text(0.5, -0.028, "\n".join(textwrap.wrap(sub, 92 if rect[2] > 0.4
                                                     else 46)),
                transform=ax.transAxes, ha="center", va="top", fontsize=9.4,
                color=GRIS, linespacing=1.4)


def folha(peso, cap, pn, pe, furos, trava, solta, hz, bb, h_solta,
          n_ap, a_ap, fx, fy):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig = plt.figure(figsize=(16.4, 12.6), facecolor=FUNDO)
    fig.text(0.5, 0.986, "Aba plana no rim + pés com cavidade",
             ha="center", va="top", fontsize=22, color=TINTA, weight="bold")
    fig.text(0.5, 0.957, ("empilha na mesma frente · encaixa "
             f"{pn:.1f} mm de passo".replace(".", ",") +
             f" · 12 peças em {hz + 11*pn:.0f} mm de caixa"),
             ha="center", va="top", fontsize=11.5, color="#3d444d")

    imagem(fig, [0.022, 0.535, 0.30, 0.335], "aba-peca.png",
           "A PEÇA", f"{M.LARG:.0f} × {M.PROF:.0f} × {M.ALT:.0f} mm · 2 pés na frente "
           f"+ saia de trás · tripé de apoio")
    imagem(fig, [0.345, 0.512, 0.635, 0.360], "cortes.png")

    imagem(fig, [0.022, 0.078, 0.30, 0.335], "aba-col.png",
           f"ENCAIXADAS · {pn:.1f} mm".replace(".", ","),
           f"6 peças em {hz + 5*pn:.0f} mm · mesma orientação, todas no "
           f"mesmo sentido")
    imagem(fig, [0.345, 0.078, 0.30, 0.335], "aba-torre.png",
           "EMPILHADAS + ACOPLADAS",
           f"2 colunas × 3 andares · mesma frente, sem inverter · cada "
           f"andar desloca {M.DESLOC:.0f} mm em y · o friso aponta o sentido")
    tb = fig.add_axes([0.668, 0.078, 0.30, 0.335]); tb.axis("off")
    tb.set_xlim(0, 1); tb.set_ylim(0, 1)
    tb.add_patch(Rectangle((0, 0), 1, 1, transform=tb.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.3))
    tb.text(0.06, 0.95, "MEDIDO NO SÓLIDO", fontsize=11.5, color=NOVO,
            weight="bold", va="top")
    linhas = [("encaixa (mesma frente)", f"{pn:.1f} mm".replace(".", ",")),
              ("6 peças / 12 peças", f"{hz+5*pn:.0f} / {hz+11*pn:.0f} mm"),
              (f"empilha (desloca {DESLOC:.0f} mm)",
               f"{pe:.1f} mm".replace(".", ",")),
              ("deslocamento p/ empilhar", f"{M.DESLOC:.0f} mm"),
              ("apoios na aba", f"{n_ap} (tripé) · {a_ap:.0f} mm²"),
              ("trava lateral a partir de", "0,6 mm"),
              ("folga de montagem do friso",
               f"x ±{fx:.1f} · y ±{fy:.1f} mm".replace(".", ",")),
              ("solta levantando",
               f"{h_solta:.1f} mm".replace(".", ",")),
              ("peso", f"{peso:.1f} g".replace(".", ",")),
              ("capacidade", f"{cap:.2f} L".replace(".", ",")),
              ("envelope", f"{bb.size.X:.0f} × {bb.size.Y:.0f} × {bb.size.Z:.1f} mm".replace(".", ",")),
              ("furos", f"{furos}")]
    y = 0.86
    for k, v in linhas:
        tb.text(0.06, y, k, fontsize=9.5, color=GRIS, va="center")
        tb.text(0.94, y, v, fontsize=9.5, color=TINTA, va="center",
                ha="right", weight="bold")
        y -= 0.062
    tb.plot([0.06, 0.16], [0.155, 0.155], color="#f0d3c2", lw=1)
    tb.text(0.06, 0.125, "\n".join(textwrap.wrap(
        "Sem gaveta no molde: pé e cauda são prismáticos em z e abertos no "
        "topo; a janela atrás do pé é fechamento macho-fêmea.", 46)),
        fontsize=9.2, color=NOVO, va="top", linespacing=1.5)

    # As duas legendas eram literais da era dos 12 graus de saida com a aba
    # para DENTRO ("10/tg 12 = 46,9 mm"). Com a aba para FORA quem manda no
    # passo e o pe, e a 6 graus o passo e outro -- por isso saem do medido.
    if M.ABA_DIR > 0:
        l1 = (f"o que mudou: com a aba virada para FORA o gargalo do encaixe "
              f"deixa de ser a aresta interna dela e passa a ser o PÉ — "
              f"medido {pn:.1f} mm".replace(".", ","))
    else:
        l1 = (f"o que mudou: a aba de {M.ABA_W:.0f} mm virou QUEM manda no "
              f"encaixe — {M.ABA_W:.0f}/tg {M.DRAFT:.0f}° = "
              f"{pn:.1f} mm, e nada mais encosta".replace(".", ","))
    fig.text(0.5, 0.475, l1, ha="center",
             va="center", fontsize=10.6, color="#3d444d")
    fig.text(0.5, 0.452, f"saída do corpo {M.DRAFT:.0f}° por lado · a face "
             f"externa do pé morre na aresta livre da aba, e é dali que vem "
             f"a saída em x de que ele precisa para telescopar",
             ha="center", va="center", fontsize=10.2, color=GRIS)

    fig.savefig(os.path.join(DEST, "aba.png"), dpi=118, facecolor=FUNDO)
    print("gerado aba.png")


if __name__ == "__main__":
    main()
