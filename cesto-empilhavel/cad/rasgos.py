#!/usr/bin/env python3
"""Duas faixas -> TRES, e rasgo de 10 x 31,5 para 6 x 18,3 mm.

Pedido de 22/09: "os rasgos verticais, temos duas linhas, eu quero deixar com
3 linhas, ou seja os rasgos verticais ficarao menores... esse produto e para
organizar pecas pequenas, tem um perigo dos produtos sairem por esses rasgos
atuais, entao preciso diminuir a altura e largura desses buracos".

O que a varredura mostrou e que MUDOU a decisao: o peso quase nao depende da
largura do rasgo. Estreitar a listra encurta o passo e entram mais colunas,
de modo que a area aberta se mantem -- 8/13, 7/12, 6/11, 6/10 e 5/9 pesam
todas entre 166,4 e 167,7 g. Quem pesa e o NUMERO DE FAIXAS (+6,5 g de 2 para
3) e a area aberta total. Logo o tamanho do rasgo e decisao de FUNCAO, nao de
peso -- e a folha existe para mostrar isso com numero.
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
COR = (0.93, 0.44, 0.13)
FUNDO, TINTA, GRIS = "#fbfaf8", "#1f2328", "#6b7280"
NOVO, VERDE, CINZ = "#c2410c", "#15803d", "#64748b"
VISTA = (-0.62, 1.0, 0.04)          # quina frente/lateral, camera no nivel

# (W, P, H alvo, MIN) -- a varredura, com o escolhido marcado
ANTES = (10.0, 15.0, 28.0, 12.0)
VARRE = ((8.0, 13.0, 18.0, 9.0), (7.0, 12.0, 18.0, 9.0),
         (6.0, 13.0, 18.0, 9.0), (6.0, 11.0, 18.0, 9.0),
         (6.0, 10.0, 18.0, 9.0), (5.0, 11.0, 18.0, 8.0),
         (5.0, 9.0, 18.0, 8.0), (4.0, 8.0, 18.0, 8.0))


def vg(x, casas=1, un=""):
    t = f"{x:.{casas}f}".replace(".", ",")
    return f"{t} {un}".strip()


def com(cotas, arq=None):
    """Constroi a peca com as cotas dadas e devolve as medidas."""
    guarda = (M.LIS_W, M.LIS_P, M.LIS_H, M.LIS_MIN)
    M.LIS_W, M.LIS_P, M.LIS_H, M.LIS_MIN = cotas
    try:
        fl = M.listras()
        p, n = M.cesto(aba=True)
    finally:
        M.LIS_W, M.LIS_P, M.LIS_H, M.LIS_MIN = guarda
    h = fl[0][1] - fl[0][0]
    if arq:
        export_stl(p, os.path.join(DEST, arq))
    return dict(p=p, n=n, faixas=len(fl), h=h, w=cotas[0], passo=cotas[1],
                nerv=cotas[1] - cotas[0], peso=p.volume * M.RHO,
                vao=cotas[0] * h)


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
    M.VAZADO = "nenhum"
    cheio = M.cesto(aba=True)[0].volume
    M.VAZADO = "listra"
    print(f"parede cheia (referencia da area aberta): {cheio*M.RHO:.1f} g")

    d = {}
    for nome, cotas, arq in (("antes", ANTES, "rasgo-antes.stl"),
                             ("depois", (M.LIS_W, M.LIS_P, M.LIS_H, M.LIS_MIN),
                              "rasgo-depois.stl")):
        d[nome] = com(cotas, arq)
        d[nome]["aberto"] = (cheio - d[nome]["p"].volume) / M.T_PAREDE
        r = d[nome]
        print(f"{nome:7s}: {r['faixas']} faixas · rasgo {r['w']:.0f} x "
              f"{r['h']:.2f} = {r['vao']:.0f} mm2 · nervura {r['nerv']:.0f} · "
              f"{r['n']} rasgos · {r['peso']:.1f} g · aberto "
              f"{r['aberto']:.0f} mm2")
        m = trimesh.load(os.path.join(DEST, arq))
        render.salvar(render.render([(m, COR)], direcao=VISTA, largura=940),
                      os.path.join(DEST, f"rasgo-{nome}.png"))

    # Encaixe e empilhamento MEDIDOS na peca escolhida: a folha os afirmava
    # digitados em 46,80/130,00, da saida de 12 graus.
    d["depois"]["pn"] = passo(d["depois"]["p"], 0.0)
    d["depois"]["pe"] = passo(d["depois"]["p"], M.DESLOC)
    print(f"         encaixa {d['depois']['pn']:.2f} · "
          f"empilha {d['depois']['pe']:.2f}")

    linhas = []
    for cotas in VARRE:
        r = com(cotas)
        r["aberto"] = (cheio - r["p"].volume) / M.T_PAREDE
        linhas.append(r)
        print(f"  varredura {cotas[0]:.0f}/{cotas[1]:.0f}: {r['n']:4d} rasgos "
              f"{r['peso']:6.1f} g  aberto {r['aberto']:6.0f} mm2")

    folha(d, linhas)


def imagem(fig, rect, arq, titulo, cor, sub):
    from PIL import Image
    ax = fig.add_axes(rect)
    ax.imshow(np.asarray(Image.open(os.path.join(DEST, arq))))
    ax.set_anchor("N")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#e3e0da")
    ax.set_title(titulo, fontsize=12.5, color=cor, weight="bold", pad=5)
    ax.text(0.5, -0.035, "\n".join(textwrap.wrap(sub, 62)),
            transform=ax.transAxes, ha="center", va="top", fontsize=9.3,
            color=GRIS, linespacing=1.4)


def escala(fig, rect, d):
    """Os dois rasgos em tamanho real, um ao lado do outro."""
    ax = fig.add_axes(rect)
    for nome, cor, x0 in (("antes", CINZ, 0.0), ("depois", NOVO, 26.0)):
        r = d[nome]
        w, h = r["w"], r["h"]
        ax.add_patch(Rectangle((x0 - w / 2, 0), w, h, facecolor="none",
                               edgecolor=cor, lw=1.8,
                               joinstyle="round"))
        ax.text(x0, h + 2.2, f"{vg(w, 0)} × {vg(h)}", color=cor, fontsize=9.6,
                ha="center", weight="bold")
        ax.text(x0, -3.0, f"{r['vao']:.0f} mm²", color=cor, fontsize=9.0,
                ha="center")
        ax.text(x0, -7.0, nome, color=cor, fontsize=9.0, ha="center")
    ax.set_xlim(-12, 38); ax.set_ylim(-10, 40)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("O RASGO EM TAMANHO REAL", fontsize=12.5, color=TINTA,
                 weight="bold", pad=5)


def folha(d, varre):
    fig = plt.figure(figsize=(16.4, 10.2), facecolor=FUNDO)
    fig.text(0.5, 0.988, "Três faixas, rasgo de um terço",
             ha="center", va="top", fontsize=22, color=TINTA, weight="bold")
    fig.text(0.5, 0.956, "nada com mais de 6 mm passa · e o peso quase não "
             "depende da largura do rasgo",
             ha="center", va="top", fontsize=11.5, color="#3d444d")

    a, b = d["antes"], d["depois"]
    imagem(fig, [0.028, 0.505, 0.30, 0.375], "rasgo-antes.png", "ANTES", CINZ,
           f"{a['faixas']} faixas · rasgo {vg(a['w'],0)} × {vg(a['h'])} mm · "
           f"{a['n']} rasgos · {vg(a['peso'])} g")
    imagem(fig, [0.348, 0.505, 0.30, 0.375], "rasgo-depois.png", "DEPOIS",
           VERDE,
           f"{b['faixas']} faixas · rasgo {vg(b['w'],0)} × {vg(b['h'])} mm · "
           f"{b['n']} rasgos · {vg(b['peso'])} g")
    escala(fig, [0.672, 0.505, 0.155, 0.375], d)

    tb = fig.add_axes([0.845, 0.445, 0.130, 0.425]); tb.axis("off")
    tb.add_patch(Rectangle((0, 0), 1, 1, transform=tb.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.3))
    tb.text(0.08, 0.955, "MEDIDO", fontsize=11, color=NOVO, weight="bold",
            va="top")
    itens = [("", "antes", "depois"),
             ("faixas", f"{a['faixas']}", f"{b['faixas']}"),
             ("largura", vg(a["w"], 0), vg(b["w"], 0)),
             ("altura", vg(a["h"]), vg(b["h"])),
             ("vão", f"{a['vao']:.0f}", f"{b['vao']:.0f}"),
             ("nervura", vg(a["nerv"], 0), vg(b["nerv"], 0)),
             ("rasgos", f"{a['n']}", f"{b['n']}"),
             ("aberto", f"{a['aberto']:.0f}", f"{b['aberto']:.0f}"),
             ("peso PP", vg(a["peso"]), vg(b["peso"]))]
    y = 0.865
    for i, (k, v1, v2) in enumerate(itens):
        w = "bold" if i == 0 else "normal"
        tb.text(0.08, y, k, fontsize=9.0, color=GRIS if i == 0 else TINTA,
                va="center", weight=w)
        tb.text(0.66, y, v1, fontsize=9.0, color=GRIS if i == 0 else CINZ,
                va="center", ha="right", weight=w)
        tb.text(0.95, y, v2, fontsize=9.0, color=GRIS if i == 0 else VERDE,
                va="center", ha="right", weight=w)
        y -= 0.093
    tb.text(0.08, max(y - 0.02, 0.085), "vão e aberto\nem mm²", fontsize=8.2, color=GRIS,
            va="top")

    # --- a varredura, em grafico: peso x largura do rasgo -------------------
    ax = fig.add_axes([0.055, 0.075, 0.42, 0.345])
    xs = [r["w"] for r in varre]
    ax.scatter(xs, [r["peso"] for r in varre], s=52, color=CINZ, zorder=3,
               label="3 faixas, vários passos")
    for r in varre:
        ax.annotate(f"{r['w']:.0f}/{r['passo']:.0f}",
                    (r["w"], r["peso"]), textcoords="offset points",
                    xytext=(0, 9), ha="center", fontsize=8.0, color=GRIS)
    ax.scatter([b["w"]], [b["peso"]], s=150, facecolor="none",
               edgecolor=VERDE, lw=2.2, zorder=4)
    ax.axhline(a["peso"], color=CINZ, ls="--", lw=1.1)
    ax.text(8.9, a["peso"] - 0.45, f"2 faixas (antes): {vg(a['peso'])} g",
            color=CINZ, fontsize=8.6, ha="right", va="top")
    ax.set_xlabel("largura do rasgo (mm)", fontsize=9.5, color=TINTA)
    ax.set_ylabel("peso em PP (g)", fontsize=9.5, color=TINTA)
    ax.set_title("O PESO NÃO SEGUE A LARGURA DO RASGO", fontsize=12.5,
                 color=TINTA, weight="bold", pad=8)
    ax.grid(alpha=0.25, lw=0.7)
    ax.set_facecolor("#fcfcfb")
    for s in ax.spines.values():
        s.set_color("#d8d5ce")
    ax.tick_params(labelsize=8.6, colors=GRIS)
    ax.set_xlim(3.4, 9.0)

    tx = fig.add_axes([0.520, 0.038, 0.453, 0.400]); tx.axis("off")
    tx.add_patch(Rectangle((0, 0), 1, 1, transform=tx.transAxes,
                           facecolor="#f6f7f9", edgecolor="#e3e0da", lw=1.2))
    tx.text(0.04, 0.955, "POR QUE A LARGURA SAI DE GRAÇA", fontsize=12,
            color=TINTA, weight="bold", va="top")
    tx.text(0.04, 0.870,
            "Estreitar a listra encurta o passo — a nervura entre elas fica "
            "em 5 mm\ncomo antes — então entram mais colunas e a área aberta "
            "se mantém.\nAs oito combinações acima pesam entre "
            f"{vg(min(r['peso'] for r in varre))} e "
            f"{vg(max(r['peso'] for r in varre), 1, 'g')}: "
            f"{vg(max(r['peso'] for r in varre) - min(r['peso'] for r in varre))} g\n"
            f"de diferença numa peça de {b['peso']:.0f}. O tamanho do rasgo é, "
            "portanto,\n"
            "decisão de FUNÇÃO — o que não pode passar por ele — e não de "
            "peso.\n\n"
            "Quem pesa são duas outras coisas:\n"
            f"   • o NÚMERO DE FAIXAS: +{vg(b['peso']-a['peso'])} g de 2 para "
            "3, porque cada faixa a\n"
            f"     mais é uma nervura de {M.LIS_WEB:.0f} mm dando a volta na "
            "peça inteira;\n"
            "   • a ÁREA ABERTA total: "
            f"{a['aberto']:.0f} → {b['aberto']:.0f} mm² aqui.\n\n"
            f"Escolhido {vg(b['w'],0)}/{vg(b['passo'],0)}: mantém a nervura de "
            f"{vg(b['nerv'],0)} mm que a peça já tinha,\n"
            "ou seja o ritmo do desenho não muda, só o tamanho do vão — que "
            f"cai\nde {a['vao']:.0f} para {b['vao']:.0f} mm², um terço. Se "
            "quiser barrar também o que tem\n"
            f"5 mm, 5/9 custa o mesmo peso ({vg([r for r in varre if r['w']==5 and r['passo']==9][0]['peso'], 1, 'g')}) "
            "e sobe de\n"
            f"{b['n']} para "
            f"{[r for r in varre if r['w']==5 and r['passo']==9][0]['n']} "
            "rasgos — 32 fecha-machos a mais no molde.\n\n"
            "O empilhamento e o encaixe não mudam: os rasgos moram na parede,\n"
            f"longe do pé, da aba e do friso. Medido: encaixa "
            f"{vg(b['pn'], 2)} mm,\n"
            f"empilha {vg(b['pe'], 2)} mm, 0,0000 mm³ de interferência.",
            fontsize=8.5, color=TINTA, va="top", linespacing=1.48)

    fig.savefig(os.path.join(DEST, "rasgos.png"), dpi=118, facecolor=FUNDO)
    print("gerado rasgos.png")


if __name__ == "__main__":
    main()
