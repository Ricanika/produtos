#!/usr/bin/env python3
"""Aba para FORA: as tres configuracoes, medidas lado a lado.

A aba virada para DENTRO nao extrai em molde de duas placas -- medido em
cad/extracao.py: 6,27 mm de ressalto para dentro da face interna da parede,
6,5% por lado num labio continuo, 52.178 mm3 do macho presos. Virada para
fora a silhueta so cresce subindo: a cavidade desce reta e o macho vira um
tronco limpo.

Mas a aba e o APOIO DO EMPILHAMENTO. Com saida de molde a base e mais estreita
que a boca, entao quem alcanca o rim sao os pes -- e virando a aba para fora a
faixa de pouso vai para FORA da parede, e os pes tem de alcancar la. O ponto
mais largo da peca sai. Dai as tres configuracoes:

  A  segura o corpo em 200 x 250  -> o envelope cresce
  B  segura o envelope em 200 x 250 -> o corpo encolhe, perde litragem
  C  segura o envelope e reduz a saida de 12 para 6 graus -> devolve litragem,
     porque sem a aba para dentro a saida DEIXA DE SER a alavanca do encaixe
     (o passo passa a ser NERV_T / saida em x do pe, que nao depende dela)

Altura fixa em 130 mm nas tres, de proposito: a saida em x do pe e
(ABA_W - ABA_POUSO)/ALT, logo o passo encaixado cresce junto com a altura e a
razao passo/altura fica constante. Altura nao e alavanca de cubagem aqui --
e decisao de produto.
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

import extracao
import modelo3d as M
import render

DEST = os.path.dirname(os.path.abspath(__file__))
COR = (0.80, 0.36, 0.12)
FUNDO, TINTA, GRIS = "#fbfaf8", "#1f2328", "#6b7280"
NOVO, VERDE, CINZ, VERM = "#c2410c", "#15803d", "#64748b", "#b91c1c"
VISTA = (-1.0, -1.25, -0.62)

# nome, boca do corpo, saida, direcao da aba
CFG = (("hoje", 200.0, 250.0, 12.0, -1),
       ("A", 200.0, 250.0, 12.0, +1),
       ("B", 180.0, 230.0, 12.0, +1),
       ("C", 180.0, 230.0, 6.0, +1))


def vg(x, casas=1, un=""):
    t = f"{x:.{casas}f}".replace(".", ",")
    return f"{t} {un}".strip()


def vol(a, b):
    try:
        return (a & b).volume
    except Exception:
        return 0.0


def mede(nome, larg, prof, graus, adir):
    M.set_envelope(larg, prof, graus, aba_dir=adir)
    p, n = M.cesto(aba=True)

    def passo(dy, tol=0.02):
        lo, hi = 0.0, 180.0
        while hi - lo > tol:
            m = (lo + hi) / 2
            if vol(p, Pos(0, dy, m) * p) > 2.0:
                lo = m
            else:
                hi = m
        return hi

    arq = os.path.join(DEST, f"af-{nome}.stl")
    export_stl(p, arq)
    m = trimesh.load(arq)
    preso, _ = extracao.audita(m)
    bb = p.bounding_box()
    pn, pe = passo(0.0), passo(M.DESLOC)
    # apoios do empilhamento
    try:
        inter = p & (Pos(0, M.DESLOC, pe - 0.3) * p)
        ap = sorted((s.volume / 0.3 for s in inter.solids()
                     if s.volume > 0.002), reverse=True)
    except Exception:
        ap = []
    d = dict(nome=nome, larg=larg, prof=prof, graus=graus, adir=adir,
             ex=bb.size.X, ey=bb.size.Y, ez=bb.size.Z,
             peso=p.volume * M.RHO, cap=M.capacidade(), n=n,
             pn=pn, pe=pe, preso=preso, apoios=ap,
             col12=bb.size.Z + 11 * pn, m=m)
    print(f"{nome:5s}: envelope {bb.size.X:6.1f} x {bb.size.Y:6.1f} | "
          f"cap {d['cap']:.2f} L | {d['peso']:6.1f} g | encaixa {pn:5.2f} | "
          f"empilha {pe:6.2f} | preso {preso:7.0f} mm3 | "
          f"12 pecas {d['col12']:.0f} mm | apoios {sum(ap):.0f} mm2")
    render.salvar(render.render([(m, COR)], direcao=VISTA, largura=760),
                  os.path.join(DEST, f"af-{nome}.png"))
    return d


def main():
    res = [mede(*c) for c in CFG]
    folha(res)


def folha(res):
    from PIL import Image
    fig = plt.figure(figsize=(16.4, 9.6), facecolor=FUNDO)
    fig.text(0.5, 0.986, "A aba para fora: as três configurações",
             ha="center", va="top", fontsize=22, color=TINTA, weight="bold")
    fig.text(0.5, 0.952, "para dentro ela prende 52.178 mm³ do macho · para "
             "fora a cavidade desce reta, e o preço é envelope ou litragem",
             ha="center", va="top", fontsize=11.5, color="#3d444d")

    rot = {"hoje": ("HOJE · aba para dentro", VERM),
           "A": ("A · corpo 200×250", CINZ),
           "B": ("B · envelope 200×250", CINZ),
           "C": ("C · envelope 200×250, saída 6°", VERDE)}
    for i, d in enumerate(res):
        t, cor = rot[d["nome"]]
        ax = fig.add_axes([0.022 + i * 0.246, 0.555, 0.232, 0.335])
        ax.imshow(np.asarray(Image.open(
            os.path.join(DEST, f"af-{d['nome']}.png"))))
        ax.set_anchor("N"); ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#e3e0da")
        ax.set_title(t, fontsize=11.5, color=cor, weight="bold", pad=5)
        ax.text(0.5, -0.035, "\n".join(textwrap.wrap(
            f"envelope {d['ex']:.0f} × {d['ey']:.0f} mm · "
            f"{vg(d['cap'], 2, 'L')} · {vg(d['peso'], 1, 'g')}", 40)),
            transform=ax.transAxes, ha="center", va="top", fontsize=9.2,
            color=GRIS, linespacing=1.4)

    linhas = [
        ("envelope em planta", lambda d: f"{d['ex']:.0f} × {d['ey']:.0f} mm"),
        ("boca do corpo", lambda d: f"{d['larg']:.0f} × {d['prof']:.0f} mm"),
        ("saída de molde", lambda d: f"{d['graus']:.0f}° por lado"),
        ("capacidade", lambda d: vg(d["cap"], 2, "L")),
        ("peso em PP", lambda d: vg(d["peso"], 1, "g")),
        ("passo encaixado", lambda d: vg(d["pn"], 2, "mm")),
        ("12 peças encaixadas", lambda d: f"{d['col12']:.0f} mm"),
        ("passo empilhado", lambda d: vg(d["pe"], 2, "mm")),
        ("apoio do tripé", lambda d: f"{sum(d['apoios']):.0f} mm²"),
        ("PRESO NO MOLDE", lambda d: f"{d['preso']:.0f} mm³"),
    ]
    tb = fig.add_axes([0.022, 0.055, 0.60, 0.450]); tb.axis("off")
    tb.add_patch(Rectangle((0, 0), 1, 1, transform=tb.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.3))
    tb.text(0.025, 0.968, "MEDIDO NO SÓLIDO", fontsize=11.5, color=NOVO,
            weight="bold", va="top")
    cols = [0.40, 0.555, 0.705, 0.855, 0.98]
    for j, d in enumerate(res):
        tb.text(cols[j + 1] - 0.005, 0.908, d["nome"].upper(), fontsize=9.6,
                color=rot[d["nome"]][1], weight="bold", ha="right")
    y = 0.840
    for k, fn in linhas:
        forte = k == "PRESO NO MOLDE"
        tb.text(0.025, y, k, fontsize=9.2,
                color=TINTA if not forte else NOVO, va="center",
                weight="bold" if forte else "normal")
        for j, d in enumerate(res):
            v = fn(d)
            c = rot[d["nome"]][1] if forte or d["nome"] == "C" else TINTA
            tb.text(cols[j + 1] - 0.005, y, v, fontsize=9.2, color=c,
                    va="center", ha="right",
                    weight="bold" if forte else "normal")
        y -= 0.072

    tx = fig.add_axes([0.640, 0.255, 0.338, 0.250]); tx.axis("off")
    tx.add_patch(Rectangle((0, 0), 1, 1, transform=tx.transAxes,
                           facecolor="#f6f7f9", edgecolor="#e3e0da", lw=1.2))
    tx.text(0.05, 0.950, "POR QUE C", fontsize=12, color=TINTA,
            weight="bold", va="top")
    h, a, b, c = res
    tx.text(0.05, 0.865,
            "A aba é o APOIO DO EMPILHAMENTO, não enfeite. A base é mais\n"
            "estreita que a boca, então quem alcança o rim são os pés — e\n"
            "com a aba para fora a faixa de pouso vai para FORA da parede.\n"
            "O ponto mais largo sai, e aí é envelope OU litragem.\n\n"
            "O que destrava a escolha: para dentro o passo encaixado era\n"
            f"ABA_W/tg(saída) = {vg(h['pn'], 1)} mm, então reduzir a saída "
            "PIORAVA o\n"
            "encaixe. Para fora quem manda é a saída em x do PÉ, que não\n"
            "depende da do corpo — ela fica livre para engordar a base.\n\n"
            f"Por isso C: mesmos 200 × 250 de planta, "
            f"{vg(c['cap'], 2, 'L')} contra "
            f"{vg(h['cap'], 2, 'L')},\n"
            f"encaixe de {vg(h['pn'], 1)} para {vg(c['pn'], 1, 'mm')} "
            f"({100*(1-c['col12']/h['col12']):.0f}% menos caixa em 12 peças) "
            "e peso\n"
            # "o MESMO de hoje" era verdade quando hoje pesava 176,5 g.
            # Hoje pesa 169,0: C custa 10,2 g a mais, e o numero tem de sair
            # da medicao, nao de uma afirmacao que envelheceu.
            f"de {vg(c['peso'], 1, 'g')}, "
            f"{vg(c['peso'] - h['peso'], 1, 'g')} acima de hoje. A vertical "
            "não é alavanca:\n"
            "a saída em x do pé é (ABA_W−ABA_POUSO)/ALT, então o passo\n"
            "encaixado cresce junto com a altura e a razão fica em 31%.\n"
            "Altura segue 130 mm, decisão de produto.",
            fontsize=7.5, color=TINTA, va="top", linespacing=1.36)

    al = fig.add_axes([0.640, 0.055, 0.338, 0.182]); al.axis("off")
    al.add_patch(Rectangle((0, 0), 1, 1, transform=al.transAxes,
                           facecolor="#f0fdf4", edgecolor="#bbf7d0", lw=1.3))
    # Esta caixa dizia "FALTA RESOLVER: o tripe caiu de 388 para 469 mm2,
    # sobraram so os dois pes da frente". Era o BUG da silhueta -- o recorte
    # do CORPO amputava a aba nova em y, sobravam 0,26 mm da aba de tras e a
    # saia pousava no vazio. silhueta(folga) resolveu, e 388 -> 469 e uma
    # SUBIDA, nao uma queda. O texto sobreviveu a propria correcao.
    al.text(0.05, 0.90, "O QUE ERA \"FALTA RESOLVER\": O APOIO DE TRÁS",
            fontsize=10.5, color=VERDE, weight="bold", va="top")
    al.text(0.05, 0.72,
            f"Resolvido. Na primeira rodada o tripé media 60 mm²: o recorte\n"
            f"da silhueta do CORPO amputava a aba nova em y, sobravam\n"
            f"0,26 mm da aba de trás em vez de 10, e a saia pousava no\n"
            f"vazio. Com a aba recortada pela sua própria silhueta\n"
            f"(offset de ABA_W), o tripé vai a {sum(c['apoios']):.0f} mm² — "
            f"acima dos {sum(h['apoios']):.0f} de\n"
            f"hoje — e DESLOC fica em 21 mm. A e B ficam em "
            f"{sum(a['apoios']):.0f} mm² por outro\n"
            f"motivo: a 12° de saída o pé não alcança a faixa de pouso.",
            fontsize=7.9, color=TINTA, va="top", linespacing=1.42)

    if False:
        tx.text(0.05, 0.865, "",            fontsize=7.9, color=TINTA, va="top", linespacing=1.42)

    fig.savefig(os.path.join(DEST, "abafora.png"), dpi=118, facecolor=FUNDO)
    print("gerado abafora.png")


if __name__ == "__main__":
    main()
