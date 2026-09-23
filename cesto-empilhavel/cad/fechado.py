#!/usr/bin/env python3
"""Fechar os dois furos que o pe abria -- e o tamanho P, para coisas miudas.

O pedido de 22/09: "tanto o furo da base do pe, quanto o furo da frente, na
parte inferior colada com a base, precisam ser fechados".

Os dois furos eram O MESMO solido. A cavidade do pe e um bloco vertical e,
subtraida da peca inteira, ela nao esvaziava so o pe: tambem furava a chapa
do fundo (dois slots de 31,8 x 7,4 mm) e abria a parede desde z = 1,6 mm.
Eram dois caminhos do interior do cesto direto para a mesa.

Esta folha mostra o antes e o depois medidos no solido, e o preco: a sola do
pe deixa de ser chapa cheia e vira COROA (anel), porque com dois posticos que
saem em +z e -z nao ha como ter sola fechada E pe oco -- ou a parede e vazada
onde o pe e oco, ou o pe e esvaziado por baixo.
"""
import os
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from build123d import Box, Pos, export_stl
from matplotlib.patches import Rectangle

import modelo3d as M
import render
from cortes import desenha, seg

DEST = os.path.dirname(os.path.abspath(__file__))
COR, COR2 = (0.93, 0.44, 0.13), (0.72, 0.30, 0.08)
FUNDO, TINTA, GRIS = "#fbfaf8", "#1f2328", "#6b7280"
NOVO, VERDE, CINZ = "#c2410c", "#15803d", "#64748b"
VERM = "#b91c1c"


def vg(x, casas=1, un=""):
    """Numero em portugues: virgula decimal. Formatado UM POR UM, nunca com
    replace no paragrafo -- ja transformei ponto de frase em virgula assim."""
    t = f"{x:.{casas}f}".replace(".", ",")
    return f"{t} {un}".strip()


def vol(*ss):
    try:
        r = ss[0]
        for x in ss[1:]:
            r = r & x
        return r.volume
    except Exception:
        return 0.0


def passo(p, dy=0.0, tol=0.01):
    lo, hi = 0.0, 145.0
    while hi - lo > tol:
        m = (lo + hi) / 2
        if vol(p, Pos(0, dy, m) * p) > 2.0:
            lo = m
        else:
            hi = m
    return hi


def constroi(fechado):
    """A peca com (fechado=True) e sem (False) as duas correcoes."""
    z_cav, memb = M.Z_CAV, M.CAV_MEMB
    if not fechado:                       # a versao anterior: cavidade no piso
        M.Z_CAV = M.NERV_T
        M.CAV_MEMB = M.NERV_T             # bolsa some (termina onde comeca)
    try:
        p, n = M.cesto(aba=True)
    finally:
        M.Z_CAV, M.CAV_MEMB = z_cav, memb
    return p, n


def furos(p):
    """Area de furo na chapa do fundo, medida contra a chapa INTEIRA.

    A referencia nao e a secao do tronco: a silhueta (o chanfro do pe) come um
    canto da chapa de proposito, e isso nao e furo. A referencia e o tronco JA
    recortado pela silhueta -- o que a chapa seria se o pe nao existisse.
    """
    e = M.T_FUNDO * 0.9
    fatia = Pos(0, 0, M.H_PE + M.T_FUNDO / 2) * Box(500, 500, e)
    tronco = M.extrude(M.RectangleRounded(M.BASE_X, M.BASE_Y, 14.0),
                       M.ALT, taper=-M.DRAFT)
    inteira = tronco & M.extrude(M.Plane.YZ * M.silhueta(),
                                 M.LARG / 2 + 30, both=True)
    # so o que esta DENTRO do tronco: os pes e a saia moram por fora dele e
    # entrariam na conta como material a mais
    return (vol(inteira, fatia) - vol(p, tronco, fatia)) / e


CARGA_PE = 13.2   # N, ver varredura.py


def main():
    M.padrao()
    dados = {}
    for nome, fechado in (("antes", False), ("depois", True)):
        p, n = constroi(fechado)
        arq = os.path.join(DEST, f"fechado-{nome}.stl")
        export_stl(p, arq)
        m = trimesh.load(arq)
        pn, pe = passo(p), passo(p, M.DESLOC)
        # coroa/chapa da sola e quanto dela pousa na aba
        sola = p & (Pos(0, 0, 0.15) * Box(500, 500, 0.3))
        faixa_aba = Pos(M.LARG / 2 - M.ABA_W / 2, 0, 0.15) * Box(M.ABA_W, 500, 0.3)
        pe_dir = max(sola.solids(), key=lambda s: s.center().X)
        ap = []
        try:
            inter = p & (Pos(0, M.DESLOC, pe - 0.3) * p)
            ap = sorted((s.volume / 0.3 for s in inter.solids()
                         if s.volume > 0.002), reverse=True)
        except Exception:
            pass
        dados[nome] = dict(
            p=p, m=m, n=n, peso=p.volume * M.RHO, pn=pn, pe=pe,
            furo_chapa=furos(p),
            z_janela=(M.NERV_T if not fechado else M.Z_CAV),
            sola=pe_dir.volume / 0.3,
            sola_aba=vol(pe_dir, faixa_aba) / 0.3,
            apoios=ap)
        print(f"{nome:7s}: peso {dados[nome]['peso']:.1f} g  encaixa {pn:.2f}  "
              f"empilha {pe:.2f}  furo na chapa {dados[nome]['furo_chapa']:.0f} mm2  "
              f"janela desde z={dados[nome]['z_janela']:.1f}  "
              f"sola {dados[nome]['sola']:.0f} mm2 (na aba "
              f"{dados[nome]['sola_aba']:.1f})")

    # --- renders -------------------------------------------------------------
    # Nada de render para o furo: no cesto inteiro o slot tem 7 mm e vira um
    # pixel, e recortado perde o contexto. Em PLANTA, cortando a chapa, ele e
    # inequivoco -- e a planta vai desenhada na folha, do proprio solido.
    # por baixo, so a versao nova: e onde a bolsa aparece
    render.salvar(render.render([(dados["depois"]["m"], COR)],
                                direcao=(-0.22, -0.34, 1.0), largura=760),
                  os.path.join(DEST, "fechado-baixo.png"))

    folha(dados)


def imagem(fig, rect, arq, titulo=None, cor=TINTA, sub=None):
    from PIL import Image
    ax = fig.add_axes(rect)
    ax.imshow(np.asarray(Image.open(os.path.join(DEST, arq))))
    ax.set_anchor("N")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#e3e0da")
    if titulo:
        ax.set_title(titulo, fontsize=12, color=cor, weight="bold", pad=5)
    if sub:
        ax.text(0.5, -0.03, "\n".join(textwrap.wrap(sub, 52)),
                transform=ax.transAxes, ha="center", va="top", fontsize=9.2,
                color=GRIS, linespacing=1.4)
    return ax


def planta(fig, rect, dados):
    """A chapa do fundo em PLANTA, cortada em z = 6 mm no proprio solido.

    E aqui que o furo se le: no render do cesto inteiro ele tem 7 mm e vira um
    pixel. A planta vem de trimesh.intersections.mesh_plane, ou seja do solido.
    """
    from trimesh.intersections import mesh_plane
    ax = fig.add_axes(rect)
    z = M.H_PE + M.T_FUNDO / 2
    for nome, cor, dx in (("antes", VERM, 0.0), ("depois", VERDE, 360.0)):
        sg = mesh_plane(dados[nome]["m"], plane_normal=[0, 0, 1],
                        plane_origin=[0, 0, z])
        sg = sg[:, :, [0, 1]]
        for a, b in sg:
            ax.plot([a[0] + dx, b[0] + dx], [a[1], b[1]], color=cor, lw=1.0,
                    solid_capstyle="round")
        ax.text(dx, 132, nome.upper(), color=cor, fontsize=10.5,
                weight="bold", ha="center", va="bottom")
    for sx in (-1, 1):                     # a marca do furo, so no antes
        ax.annotate("", xy=(sx * 80, M.PES[0][0]), xytext=(sx * 128, -112),
                    arrowprops=dict(arrowstyle="->", color=VERM, lw=1.2))
    ax.text(0, -128, "os dois slots de 31,8 × 7,4 mm\n"
            f"{vg(abs(dados['antes']['furo_chapa']), 0, 'mm²')} de furo",
            color=VERM, fontsize=8.6, ha="center", va="top")
    ax.text(360, -128, "chapa inteira: 0 mm² de furo, medido\ncontra a chapa "
            "que existiria sem o pé", color=VERDE, fontsize=8.6,
            ha="center", va="top")
    ax.set_xlim(-140, 500); ax.set_ylim(-175, 152)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("A CHAPA DO FUNDO EM PLANTA · corte em z = 6 mm",
                 fontsize=12, color=TINTA, weight="bold", pad=4)


def corte(fig, rect, dados):
    """Corte no eixo do pe: onde a cavidade comeca, antes e depois."""
    ax = fig.add_axes(rect)
    yc, L = M.PES[0][0], M.PES[0][1]
    for nome, cor, dx in (("antes", CINZ, 0.0), ("depois", NOVO, 130.0)):
        m = dados[nome]["m"]
        # claro: o corte na PAREDE EM Y do pe -- da o contorno externo dele
        for y, lw, al in ((yc + L / 2 - M.NERV_T / 2, 1.0, 0.35),
                          (yc, 1.6, 1.0)):
            s = seg(m, y)
            s = s.copy(); s[:, :, 0] += dx
            desenha(ax, s[(s[:, :, 0] >= 42 + dx).all(1)], cor, lw=lw,
                    alpha=al)
        ax.text(78 + dx, 138, nome.upper(), color=cor, fontsize=10.5,
                weight="bold", ha="center")
    ax.text(78, 130, "claro = o contorno do pé (corte na parede dele)",
            color=GRIS, fontsize=7.8, ha="center")
    # cotas na versao nova
    ax.annotate("", xy=(132, M.Z_CAV), xytext=(132, 0),
                arrowprops=dict(arrowstyle="<->", color=VERDE, lw=1.0))
    ax.text(133.5, M.Z_CAV / 2, f"parede CEGA\naté z = {M.Z_CAV:.0f} mm",
            color=VERDE, fontsize=8.4, va="center")
    ax.plot([130 + 74, 130 + 96], [M.Z_CAV - M.CAV_MEMB / 2] * 2,
            color=VERDE, lw=3.0, alpha=0.5)
    ax.text(130 + 98, M.Z_CAV - 1, "membrana de "
            f"{M.CAV_MEMB:.0f} mm:\né ela que cega a bolsa",
            color=VERDE, fontsize=8.4, va="center")
    ax.annotate("", xy=(66, M.H_PE + M.T_FUNDO / 2), xytext=(40, 34),
                arrowprops=dict(arrowstyle="->", color=VERM, lw=1.1))
    ax.text(39, 35, "a chapa do fundo\nera furada aqui", color=VERM,
            fontsize=8.4, va="bottom", ha="left")
    ax.annotate("", xy=(75, 14), xytext=(58, -16),
                arrowprops=dict(arrowstyle="->", color=VERM, lw=1.1))
    ax.text(57, -18, "e a parede abria\ndesde z = 1,6", color=VERM,
            fontsize=8.4, va="top", ha="right")
    ax.set_xlim(34, 250); ax.set_ylim(-36, 148)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("O CORTE NO EIXO DO PÉ · tirado do sólido",
                 fontsize=12, color=TINTA, weight="bold", pad=4)


def folha(d):
    fig = plt.figure(figsize=(16.4, 9.4), facecolor=FUNDO)
    fig.text(0.5, 0.988, "Os dois furos do pé, fechados",
             ha="center", va="top", fontsize=22, color=TINTA, weight="bold")
    fig.text(0.5, 0.955, "é o tamanho P, para coisas miúdas · nada do que "
             "está dentro do cesto tem por onde cair",
             ha="center", va="top", fontsize=11.5, color="#3d444d")

    imagem(fig, [0.030, 0.520, 0.235, 0.385], "fechado-baixo.png",
           "POR BAIXO", TINTA,
           "a bolsa é CEGA: existe só por fora da casca")
    planta(fig, [0.030, 0.040, 0.445, 0.400], d)

    tb = fig.add_axes([0.305, 0.520, 0.235, 0.385]); tb.axis("off")
    tb.add_patch(Rectangle((0, 0), 1, 1, transform=tb.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.3))
    tb.text(0.06, 0.955, "MEDIDO NO SÓLIDO", fontsize=11.5, color=NOVO,
            weight="bold", va="top")
    linhas = [
        ("", "antes", "depois"),
        ("furo na chapa do fundo", vg(abs(d['antes']['furo_chapa']), 0, "mm²"),
         vg(abs(d['depois']['furo_chapa']), 0, "mm²")),
        ("parede abre em z =", vg(d['antes']['z_janela'], 1, "mm"),
         vg(d['depois']['z_janela'], 0, "mm")),
        ("sola do pé", vg(d['antes']['sola'], 0, "mm²"),
         vg(d['depois']['sola'], 0, "mm²")),
        ("dela, pousada na aba", vg(d['antes']['sola_aba'], 1, "mm²"),
         vg(d['depois']['sola_aba'], 1, "mm²")),
        ("passo encaixado", vg(d['antes']['pn'], 2, "mm"),
         vg(d['depois']['pn'], 2, "mm")),
        ("passo empilhado", vg(d['antes']['pe'], 2, "mm"),
         vg(d['depois']['pe'], 2, "mm")),
        ("peso em PP", vg(d['antes']['peso'], 1, "g"),
         vg(d['depois']['peso'], 1, "g")),
    ]
    y = 0.865
    for i, (a, b, c) in enumerate(linhas):
        w = "bold" if i == 0 else "normal"
        col = GRIS if i == 0 else TINTA
        tb.text(0.06, y, a, fontsize=9.4, color=TINTA if i else GRIS,
                va="center", weight=w)
        tb.text(0.70, y, b, fontsize=9.4, color=CINZ if i else GRIS,
                va="center", ha="right", weight=w)
        tb.text(0.97, y, c, fontsize=9.4, color=VERDE if i else GRIS,
                va="center", ha="right", weight=w)
        y -= 0.095
    tb.text(0.06, y - 0.03, "o empilhamento não mudou: passo exatamente na "
            "altura,\n130,00 mm, com 0,0000 mm³ de interferência",
            fontsize=8.8, color=NOVO, va="top")

    corte(fig, [0.520, 0.040, 0.452, 0.400], d)

    tx = fig.add_axes([0.580, 0.478, 0.392, 0.427]); tx.axis("off")
    tx.add_patch(Rectangle((0, 0), 1, 1, transform=tx.transAxes,
                           facecolor="#f6f7f9", edgecolor="#e3e0da", lw=1.2))
    tx.text(0.04, 0.955, "O PREÇO: A SOLA VIRA COROA", fontsize=11.5,
            color=TINTA, weight="bold", va="top")
    ap = d["depois"]["apoios"]
    texto = (
        "Com dois postiços que saem em +z e −z não existe pé oco COM sola\n"
        "fechada: quem forma a cavidade do pé só chega lá de cima, pela\n"
        "janela na parede — e se a parede fosse inteira esse macho seria um\n"
        "dedo solto que ENGROSSA para baixo (o cone recua 0,213 mm/mm e a\n"
        "face do pé só avança 0,046), ou seja contra-saída.\n\n"
        "Então: onde o pé é oco a parede é vazada, e onde a parede é cega o\n"
        "pé é esvaziado POR BAIXO. Nos 40 mm de baixo a sola deixa de ser\n"
        "chapa e vira coroa, como o fundo de um balde.\n\n"
        f"Apoio de cada pé na aba: {vg(d['antes']['sola_aba'])} → "
        f"{vg(d['depois']['sola_aba'], 1, 'mm²')}.\n"
        f"Tripé completo: {' + '.join(f'{a:.0f}' for a in ap)} = "
        f"{sum(ap):.0f} mm² de contato de face plana.\n\n"
        # A carga por pe (13,2 N dos 34,5 N da coluna de 4) vem da estatica
        # do tripe em varredura.png; a pressao sai da area MEDIDA aqui, para
        # as duas folhas nao divergirem. Estava 11,6 N digitado, da geometria
        # anterior, e a folga do friso trazia ±1,2 em y quando aba.py mede
        # outro valor -- numero repetido em duas folhas envelhece em uma.
        f"Numa coluna de 4 com 1 kg em cada ({vg(CARGA_PE)} N no pé, pela\n"
        f"estática do tripé em varredura.png):\n"
        f"   • pressão de contato {vg(CARGA_PE)} / "
        f"{vg(d['depois']['sola_aba'])} = "
        f"{vg(CARGA_PE/d['depois']['sola_aba'], 2)} MPa (PP cede a ~30) → "
        f"{30/(CARGA_PE/d['depois']['sola_aba']):.0f}×\n"
        "   • a saia pousa na aba direto acima da parede: braço de\n"
        "     flexão de 0,55 mm, e a aba nem entra em flexão\n"
        "Passa nos dois. O que NÃO passava era a folga de montagem\n"
        "do friso: 0,21 mm, menos que a tolerância da própria injeção.\n"
        "Aberta para 0,8 mm e 8° de saída; a folga resultante está\n"
        "medida na folha aba.png.")
    tx.text(0.04, 0.925, texto, fontsize=7.9, color=TINTA, va="top",
            linespacing=1.5, family="DejaVu Sans")

    fig.savefig(os.path.join(DEST, "fechado.png"), dpi=118,
                facecolor=FUNDO)
    print("gerado fechado.png")


if __name__ == "__main__":
    main()
