#!/usr/bin/env python3
"""Folha elo.png: a linha ELO -- o P, o M, e o par de P empilhado no M.

NAO remede nada. Le cad/elo-medidas.json e os STLs que visor_elo.py deixa,
porque cada medicao de interferencia nestas pecas custa minutos de booleano --
e medir a mesma coisa em dois scripts e o caminho mais curto para as duas
folhas divergirem (ja aconteceu com o tripe e com a soltura).

Uso:  python3 visor_elo.py   (gera os dados)
      python3 elo.py         (desenha a folha)
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from matplotlib.patches import Rectangle

import render

DEST = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(DEST, "elo-medidas.json")
STL_P = os.path.join(DEST, "elo-p.stl")
STL_M = os.path.join(DEST, "elo-m.stl")

FUNDO = "#faf8f4"
TINTA, GRIS, NOVO, VERDE, CINZ = "#1d1813", "#6d645a", "#c2410c", "#15803d", "#64748b"
COR_P = (0.784, 0.337, 0.102)
COR_M = (0.627, 0.271, 0.102)
VISTA = (-1.0, -1.6, -0.75)


def vg(x, casas=1, un=""):
    t = f"{x:.{casas}f}".replace(".", ",")
    return f"{t} {un}".strip()


def move(m, dx=0.0, dy=0.0, dz=0.0):
    c = m.copy()
    c.apply_translation([dx, dy, dz])
    return c


def cena(pecas, arq, largura=900):
    img = render.render(pecas, direcao=VISTA, largura=largura)
    return render.salvar(img, os.path.join(DEST, arq))


def painel(fig, rect, arq, titulo, cor, linhas, cx=None):
    from PIL import Image
    ax = fig.add_axes(rect)
    ax.imshow(np.asarray(Image.open(os.path.join(DEST, arq))))
    ax.set_anchor("N"); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#e3e0da")
    ax.set_title(titulo, fontsize=12.5, color=cor, weight="bold", pad=6)
    fig.text(cx if cx is not None else rect[0] + rect[2] / 2,
             rect[1] - 0.012, "\n".join(linhas), ha="center", va="top",
             fontsize=8.6, color=TINTA, linespacing=1.55)


def main():
    if not os.path.exists(DADOS):
        raise SystemExit("falta elo-medidas.json -- rode visor_elo.py antes")
    d = json.load(open(DADOS, encoding="utf-8"))
    p, m = d["p"], d["m"]
    mp, mm = trimesh.load(STL_P), trimesh.load(STL_M)
    pp = d["passo_p"] / 2
    dy, zp = d["par"]["dy"], d["par"]["z"]
    ap_par, ap_m = sum(d["par"]["ap"]), sum(d["ap_m"])

    # --- as cenas ---------------------------------------------------------
    cena([(mp, COR_P)], "elo-p.png", 720)
    cena([(mm, COR_M)], "elo-m.png", 900)
    cena([(mm, COR_M),
          (move(mp, -pp, dy, zp), COR_P),
          (move(mp, pp, dy, zp), COR_P)], "elo-dois.png", 1000)
    cena([(move(mm, 0, i * d["desloc"], i * d["pn_m"]), COR_M if i % 2 else COR_P)
          for i in range(6)], "elo-encaixa.png", 760)
    cena([(mm, COR_M), (move(mm, d["passo_m"], 0, 0), COR_P)],
         "elo-acopla.png", 1000)

    # --- a folha ----------------------------------------------------------
    fig = plt.figure(figsize=(16.4, 11.6), facecolor=FUNDO)
    fig.text(0.5, 0.982, "Linha ELO: o M é dois P acoplados",
             ha="center", va="top", fontsize=21, color=TINTA, weight="bold")
    fig.text(0.5, 0.950,
             "boca de 380 = 2 × 180 + 2 × 10 · mesma profundidade, mesma "
             "altura, mesma saída · nada foi adaptado",
             ha="center", va="top", fontsize=11.5, color="#3d444d")

    painel(fig, [0.028, 0.615, 0.175, 0.290], "elo-p.png",
           "ELO P", NOVO,
           [f"{p['larg']:.0f} × {p['prof']:.0f} × {d['alt']:.0f} mm",
            f"{vg(p['peso'])} g · {vg(p['cap'], 2)} L",
            f"{p['furos']} rasgos"])
    painel(fig, [0.225, 0.615, 0.245, 0.290], "elo-m.png",
           "ELO M", VERDE,
           [f"{m['larg']:.0f} × {m['prof']:.0f} × {d['alt']:.0f} mm",
            f"{vg(m['peso'])} g · {vg(m['cap'], 2)} L",
            f"{m['furos']} rasgos"])
    painel(fig, [0.492, 0.615, 0.290, 0.290], "elo-dois.png",
           "DOIS P ACOPLADOS, EMPILHADOS NO M", VERDE,
           [f"passo {vg(zp, 2)} mm · desloca {dy:.0f} mm em y",
            f"interferência {vg(d['par']['interf'], 4)} mm³",
            f"contato {ap_par:.0f} mm² — {vg(ap_par/ap_m)}× o tripé do M"])
    painel(fig, [0.805, 0.615, 0.170, 0.290], "elo-encaixa.png",
           "M ENCAIXADOS", CINZ,
           [f"passo {vg(d['pn_m'], 2)} mm — o mesmo do P",
            f"12 peças em {m['env'][2] + 11*d['pn_m']:.0f} mm",
            f"{vg(d['pe_m']/d['pn_m'])}× mais que empilhado"])

    # --- a tabela ---------------------------------------------------------
    tb = fig.add_axes([0.028, 0.048, 0.455, 0.480]); tb.axis("off")
    # FIXAR os limites: o tb.plot() da linha divisoria autoescala o eixo e
    # joga todo o texto para fora da vista (a caixa desenha, o conteudo nao).
    tb.set_xlim(0, 1); tb.set_ylim(0, 1)
    tb.add_patch(Rectangle((0, 0), 1, 1, transform=tb.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.3))
    tb.text(0.045, 0.955, "MEDIDO NO SÓLIDO", fontsize=11.5, color=NOVO,
            weight="bold", va="top")
    linhas = [("", "ELO P", "ELO M"),
              ("boca do corpo", f"{p['larg']:.0f} × {p['prof']:.0f}",
               f"{m['larg']:.0f} × {m['prof']:.0f}"),
              ("envelope em x", f"{vg(p['larg'] + 20 + 4)} mm",
               f"{vg(m['env'][0])} mm"),
              ("capacidade", vg(p["cap"], 2, "L"), vg(m["cap"], 2, "L")),
              ("peso em PP", vg(p["peso"], 1, "g"), vg(m["peso"], 1, "g")),
              ("rasgos", f"{p['furos']}", f"{m['furos']}"),
              ("passo encaixado", vg(d["pn_p"], 2, "mm"),
               vg(d["pn_m"], 2, "mm")),
              ("passo empilhado", vg(d["pe_p"], 2, "mm"),
               vg(d["pe_m"], 2, "mm")),
              ("passo acoplado", f"{d['passo_p']:.0f} mm",
               f"{d['passo_m']:.0f} mm"),
              ("solta levantando", vg(d["solta_p"], 1, "mm"),
               vg(d["solta_m"], 1, "mm")),
              ("tripé de apoio", f"{sum(d['ap_p']):.0f} mm²",
               f"{ap_m:.0f} mm²"),
              ("preso no molde", f"{d['preso_p']:,.0f} mm³".replace(",", "."),
               f"{d['preso_m']:,.0f} mm³".replace(",", "."))]
    y = 0.865
    for i, (k, a, b) in enumerate(linhas):
        w = "bold" if i == 0 else "normal"
        tb.text(0.045, y, k, fontsize=9.3, color=GRIS if i == 0 else TINTA,
                va="center", weight=w)
        tb.text(0.66, y, a, fontsize=9.3, color=GRIS if i == 0 else CINZ,
                va="center", ha="right", weight=w)
        tb.text(0.955, y, b, fontsize=9.3, color=GRIS if i == 0 else VERDE,
                va="center", ha="right", weight=w)
        y -= 0.058
    tb.plot([0.045, 0.955], [y + 0.022, y + 0.022], color="#f0d3c2", lw=1)
    tb.text(0.045, y - 0.005,
            "O passo ENCAIXADO é o mesmo nos dois tamanhos, e não é\n"
            "coincidência: quem manda nele é a saída em x do PÉ, que não\n"
            f"depende da largura do corpo. Por isso o M cuba tão bem\n"
            f"quanto o P: 12 peças em {m['env'][2] + 11*d['pn_m']:.0f} mm de "
            f"caixa, nos DOIS tamanhos.",
            fontsize=8.8, color=NOVO, va="top", linespacing=1.55)

    # --- o texto ----------------------------------------------------------
    tx = fig.add_axes([0.505, 0.048, 0.470, 0.480]); tx.axis("off")
    tx.set_xlim(0, 1); tx.set_ylim(0, 1)
    tx.add_patch(Rectangle((0, 0), 1, 1, transform=tx.transAxes,
                           facecolor="#f0fdf4", edgecolor="#bbf7d0", lw=1.3))
    tx.text(0.04, 0.955, "POR QUE 380, E POR QUE NADA PRECISOU MUDAR",
            fontsize=11.5, color=VERDE, weight="bold", va="top")
    tx.text(0.04, 0.880,
            "A aba do P vai de 90 a 100 mm do eixo dele. Dois P acoplados no\n"
            "passo de 200 têm as abas se encontrando EXATAS em x = 100, e o\n"
            "conjunto vai de −100 a +300: 400 mm de pegada de aba.\n\n"
            "Para o M ter a MESMA pegada, a aba dele tem de ir de 190 a 200\n"
            "do seu eixo — logo a boca do corpo é 380. E aí as paredes do M\n"
            "caem em x = −90 e +290, que é precisamente onde pousam os pés\n"
            "externos do par. O envelope dos dois bate em 0,00 mm nos três\n"
            f"eixos: {vg(m['env'][0])} × {vg(m['env'][1])} × "
            f"{vg(m['env'][2])} mm.\n\n"
            "A PROFUNDIDADE NÃO MUDA: 230 nos dois. Por isso a silhueta\n"
            "lateral, os chanfros da frente (52 / 36), o pé, a saia de trás,\n"
            "o friso e a tapa do rasgo frontal ficam IDÊNTICOS — só o x\n"
            "escala. Conferido: 0 de 720 raios escapam em z = 7,5 · 12 · 20 ·\n"
            "26 · 30 · 39 mm, igual ao P.\n\n"
            f"O contato do par no M é {ap_par:.0f} mm²: as duas saias de trás\n"
            f"pousam inteiras ({d['par']['ap'][0]:.0f} mm² cada) e os dois\n"
            f"pés externos também ({d['par']['ap'][2]:.0f} mm² cada). Os dois\n"
            "pés internos ficam sobre a boca do M, no vazio, e não fazem\n"
            f"falta: {ap_par:.0f} mm² já é {vg(ap_par/ap_m)}× o próprio tripé\n"
            "do M.\n\n"
            "DE GRAÇA: com deslocamento ZERO em y, o par de P não empilha —\n"
            f"ENCAIXA dentro do M, a {vg(d['pn_m'], 2)} mm. O mesmo "
            "deslocamento\nde 21 mm que troca encaixe por pilha no P troca "
            "também aqui.",
            fontsize=8.5, color=TINTA, va="top", linespacing=1.46)

    fig.savefig(os.path.join(DEST, "elo.png"), dpi=118, facecolor=FUNDO)
    print("gerado elo.png")


if __name__ == "__main__":
    main()
