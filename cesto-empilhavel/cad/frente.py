#!/usr/bin/env python3
"""O rasgo inferior frontal, fechado -- e o teste que faltava.

Pedido de 22/09: "o rasgo inferior frontal ainda esta ali, eu quero fechar ele
tmb... aqui corre o risco dos produtos colocados nele escorrer e sair pelo
buraco".

O chanfro do pe (45 graus, CHANFRO_PE = 36) passa POR DENTRO da parede da
frente ate z = 10,63 mm. Entre o topo da chapa do fundo (z = 7) e essa cota a
parede simplesmente nao existia -- 237 mm2 de rasgo em 130 mm de frente, com a
borda da chapa servindo de rampa para ele.

E a licao de metodo: o teste anterior (secao contra a casca ja recortada pela
silhueta) NAO pegava isso, porque a referencia tinha o mesmo rasgo -- o
chanfro come a parede nas duas. O teste que pega nao usa referencia: raio, de
dentro para fora. Se um raio sai sem cruzar material, ha caminho.
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
from trimesh.intersections import mesh_plane

import modelo3d as M

DEST = os.path.dirname(os.path.abspath(__file__))
FUNDO, TINTA, GRIS = "#fbfaf8", "#1f2328", "#6b7280"
NOVO, VERDE, CINZ, VERM = "#c2410c", "#15803d", "#64748b", "#b91c1c"

Z_RAIO = 7.5          # cota do teste de raios: onde o rasgo e mais aberto
N_RAIO = 720


def vg(x, casas=1, un=""):
    t = f"{x:.{casas}f}".replace(".", ",")
    return f"{t} {un}".strip()


def constroi(tapa):
    if not tapa:
        guarda = M._tapa_frente
        M._tapa_frente = lambda fora, sil: Pos(0, 0, -50) * Box(.01, .01, .01)
    try:
        p, n = M.cesto(aba=True)
    finally:
        if not tapa:
            M._tapa_frente = guarda
    return p, n


def corte(m, z):
    s = mesh_plane(m, plane_normal=[0, 0, 1], plane_origin=[0, 0, z])
    return s[:, :, :2] if s is not None and len(s) else np.zeros((0, 2, 2))


def raios(seg, org, dirs):
    """Quantos segmentos cada raio cruza. Zero = caminho livre para fora."""
    a, b = seg[:, 0, :], seg[:, 1, :]
    e = b - a
    ao = a - org[None, :]
    cont = np.zeros(len(dirs), int)
    for i, d in enumerate(dirs):
        den = d[0] * e[:, 1] - d[1] * e[:, 0]
        ok = np.abs(den) > 1e-12
        dd = np.where(ok, den, 1.0)
        t = np.where(ok, (ao[:, 0] * e[:, 1] - ao[:, 1] * e[:, 0]) / dd, -1.0)
        u = np.where(ok, (ao[:, 0] * d[1] - ao[:, 1] * d[0]) / dd, -1.0)
        cont[i] = int(np.count_nonzero(
            ok & (t > 1e-9) & (u >= -1e-9) & (u <= 1 + 1e-9)))
    return cont


def area_rasgo(m, dx=0.5, dz=0.125):
    """Area do rasgo frontal: varredura de raios em -y sobre (x, z).

    So conta quem esta DE FATO dentro do cesto -- o raio para tras tem de
    bater em material. Sem isso os x fora da largura da frente entram na
    conta e dao um piso falso de 21 mm.
    """
    xs = np.arange(-104.0, 104.0 + dx, dx)
    tot, faixa = 0.0, []
    for z in np.arange(M.H_PE, 13.0 + dz, dz):
        seg = corte(m, z)
        if not len(seg):
            continue
        a, b = seg[:, 0, :], seg[:, 1, :]
        e = b - a
        ok = np.abs(e[:, 0]) > 1e-12
        livre = np.zeros(len(xs), bool)
        for i, x in enumerate(xs):
            u = np.where(ok, (x - a[:, 0]) / np.where(ok, e[:, 0], 1.0), -1.0)
            cr = ok & (u >= 0.0) & (u <= 1.0)
            y = a[:, 1] + u * e[:, 1]
            livre[i] = np.any(cr & (y > 0.0)) and not np.any(cr & (y < 0.0))
        larg = livre.sum() * dx
        tot += larg * dz
        if larg > 0.5:
            faixa.append((z, larg, xs[livre].min(), xs[livre].max()))
    return tot, faixa


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
    d = {}
    ang = np.linspace(0, 2 * np.pi, N_RAIO, endpoint=False)
    dirs = np.stack([np.cos(ang), np.sin(ang)], 1)
    for nome, tapa in (("antes", False), ("depois", True)):
        p, n = constroi(tapa)
        arq = os.path.join(DEST, f"frente-{nome}.stl")
        export_stl(p, arq)
        m = trimesh.load(arq)
        seg = corte(m, Z_RAIO)
        c = raios(seg, np.array([0.0, 0.0]), dirs)
        ar, faixa = area_rasgo(m)
        d[nome] = dict(p=p, m=m, seg=seg, fuga=(c == 0), ang=ang,
                       area=ar, faixa=faixa, peso=p.volume * M.RHO,
                       yz=mesh_plane(m, plane_normal=[1, 0, 0],
                                     plane_origin=[0, 0, 0])[:, :, 1:])
        esc = int((c == 0).sum())
        a = np.degrees(ang[c == 0])
        print(f"{nome:7s}: {esc:3d}/{N_RAIO} raios escapam em z={Z_RAIO}"
              + (f" ({a.min():.0f}..{a.max():.0f} graus)" if esc else "")
              + f" · rasgo {ar:.0f} mm2 · {p.volume*M.RHO:.1f} g")
        if faixa:
            print(f"         faixa z {faixa[0][0]:.2f}..{faixa[-1][0]:.2f} mm,"
                  f" largura ate {max(f[1] for f in faixa):.0f} mm")
    # O selo da folha afirmava encaixe e empilhamento; media-os agora, em vez
    # de repetir os 46,80/130,00 da saida de 12 graus.
    d["depois"]["pn"] = passo(d["depois"]["p"], 0.0)
    d["depois"]["pe"] = passo(d["depois"]["p"], M.DESLOC)
    print(f"         encaixa {d['depois']['pn']:.2f} · "
          f"empilha {d['depois']['pe']:.2f}")
    folha(d)


def painel_planta(fig, rect, dd, nome, titulo, cor):
    ax = fig.add_axes(rect)
    seg = dd["seg"]
    for a, b in seg:
        ax.plot([a[0], b[0]], [a[1], b[1]], color=TINTA, lw=0.7,
                solid_capstyle="round")
    fuga, ang = dd["fuga"], dd["ang"]
    for t in ang[fuga]:
        ax.plot([0, 150 * np.cos(t)], [0, 150 * np.sin(t)], color=VERM,
                lw=0.5, alpha=0.55)
    n = int(fuga.sum())
    ax.plot(0, 0, "o", color=TINTA, ms=3)
    ax.text(0, 143, titulo, color=cor, fontsize=11, weight="bold",
            ha="center", va="bottom")
    ax.text(0, -152, (f"{n} de {N_RAIO} raios saem sem cruzar material"
                      if n else f"0 de {N_RAIO} raios saem — nenhum caminho"),
            color=VERM if n else VERDE, fontsize=8.8, ha="center", va="top")
    if n:
        a = np.degrees(ang[fuga])
        ax.text(0, -163, f"todos entre {a.min():.0f}° e {a.max():.0f}°, "
                "ou seja apontando para a frente", color=VERM, fontsize=8.4,
                ha="center", va="top")
    ax.set_xlim(-150, 150); ax.set_ylim(-175, 155)
    ax.set_aspect("equal"); ax.axis("off")


def painel_corte(fig, rect, d):
    """O corte no meio (x = 0), no pe da frente, em ZOOM.

    A janela e de 11 x 10 mm: o rasgo tem 1,8 mm de altura e some em qualquer
    enquadramento mais largo. Escala 1:1 nos dois eixos -- o chanfro tem de
    continuar a 45 graus.
    """
    ax = fig.add_axes(rect)
    zc = (M.CHANFRO_PE - (M.PROF / 2 - M.BASE_Y / 2)) / (1 - M.TAN)
    for nome, cor, dy in (("antes", CINZ, 0.0), ("depois", NOVO, 13.5)):
        for a, b in d[nome]["yz"]:
            if max(a[1], b[1]) > 13.5 or min(a[0], b[0]) < -101.5:
                continue
            if min(a[0], b[0]) > -90.0 and max(a[1], b[1]) < 4.0:
                continue                      # a chapa corre longe, nao cabe
            ax.plot([a[0] + dy, b[0] + dy], [a[1], b[1]], color=cor, lw=2.0,
                    solid_capstyle="round")
        ax.text(-95.5 + dy, 13.0, nome.upper(), color=cor, fontsize=10.5,
                weight="bold", ha="center")

    # o rasgo, no antes
    ax.annotate("", xy=(-96.3, 7.9), xytext=(-99.6, 11.4),
                arrowprops=dict(arrowstyle="->", color=VERM, lw=1.2))
    ax.text(-99.8, 11.5, f"o rasgo\n{vg(d['antes']['faixa'][-1][0] - d['antes']['faixa'][0][0], 1)} mm",
            color=VERM, fontsize=8.6,
            ha="left", va="bottom")
    ax.plot([-101.2, -93.5], [M.H_PE + M.T_FUNDO] * 2, color=GRIS, lw=0.7,
            ls=":")
    ax.text(-101.4, M.H_PE + M.T_FUNDO, "topo da\nchapa, z = 7", color=GRIS,
            fontsize=7.8, va="center", ha="right")
    # a tapa, no depois
    ax.plot([-95.0 + 13.5, -86.0 + 13.5], [zc] * 2, color=VERDE, lw=0.7,
            ls=":")
    ax.text(-85.5 + 13.5, zc, f"z = {vg(zc, 2)}: o chanfro\nsai da casca e a "
            "tapa\ntermina sozinha", color=VERDE, fontsize=7.8, va="center")
    ax.annotate("", xy=(-96.3 + 13.5, 8.3), xytext=(-99.6 + 13.5, 11.4),
                arrowprops=dict(arrowstyle="->", color=VERDE, lw=1.2))
    ax.text(-99.8 + 13.5, 11.5, "a tapa\n1,4 mm", color=VERDE, fontsize=8.6,
            ha="left", va="bottom")
    ax.set_xlim(-104.5, -62.0); ax.set_ylim(3.6, 14.2)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("O CORTE NO MEIO (x = 0), NO PÉ DA FRENTE · zoom 1:1",
                 fontsize=12, color=TINTA, weight="bold", pad=4)


def folha(d):
    fig = plt.figure(figsize=(16.4, 10.0), facecolor=FUNDO)
    fig.text(0.5, 0.985, "O rasgo inferior frontal, fechado",
             ha="center", va="top", fontsize=22, color=TINTA, weight="bold")
    fig.text(0.5, 0.950, "o chanfro do pé passava por dentro da parede · e o "
             "teste que pega isso não usa referência: raio, de dentro para fora",
             ha="center", va="top", fontsize=11.5, color="#3d444d")

    a, b = d["antes"], d["depois"]
    painel_planta(fig, [0.030, 0.415, 0.245, 0.470], a, "antes",
                  f"ANTES · corte em z = {vg(Z_RAIO)} mm", VERM)
    painel_planta(fig, [0.285, 0.415, 0.245, 0.470], b, "depois",
                  f"DEPOIS · corte em z = {vg(Z_RAIO)} mm", VERDE)
    painel_corte(fig, [0.030, 0.038, 0.500, 0.345], d)

    tb = fig.add_axes([0.556, 0.560, 0.205, 0.320]); tb.axis("off")
    tb.add_patch(Rectangle((0, 0), 1, 1, transform=tb.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.3))
    tb.text(0.07, 0.945, "MEDIDO", fontsize=11, color=NOVO, weight="bold",
            va="top")
    itens = [("", "antes", "depois"),
             ("rasgo frontal", f"{a['area']:.0f} mm²", f"{b['area']:.0f} mm²"),
             ("raios que escapam", f"{int(a['fuga'].sum())}", "0"),
             ("parede, z = 7,5", "0 mm", "2,18 mm"),
             ("parede, z = 9,5", "0,63", "2,18 mm"),
             ("peso em PP", vg(a["peso"]), vg(b["peso"]))]
    y = 0.855
    for i, (k, v1, v2) in enumerate(itens):
        w = "bold" if i == 0 else "normal"
        tb.text(0.06, y, k, fontsize=8.8, color=GRIS if i == 0 else TINTA,
                va="center", weight=w)
        tb.text(0.66, y, v1, fontsize=8.8, color=GRIS if i == 0 else CINZ,
                va="center", ha="right", weight=w)
        tb.text(0.97, y, v2, fontsize=8.8, color=GRIS if i == 0 else VERDE,
                va="center", ha="right", weight=w)
        y -= 0.125
    # Encaixe e empilhamento MEDIDOS. Estavam digitados em 46,80/130,00, da
    # saida de 12 graus; e o bloco ficava logo abaixo do fim da caixa, com a
    # ultima linha por fora dela -- por isso ele agora comeca em y + 0.035.
    tb.text(0.07, y + 0.035,
            f"a peça toda continua\nencaixando em {vg(b['pn'], 2)} e\n"
            f"empilhando em {vg(b['pe'], 2)} mm",
            fontsize=8.4, color=NOVO, va="top")

    tx = fig.add_axes([0.556, 0.038, 0.416, 0.505]); tx.axis("off")
    tx.add_patch(Rectangle((0, 0), 1, 1, transform=tx.transAxes,
                           facecolor="#f6f7f9", edgecolor="#e3e0da", lw=1.2))
    tx.text(0.04, 0.955, "POR QUE ESCAPOU DOS TESTES ANTERIORES",
            fontsize=12, color=TINTA, weight="bold", va="top")
    zc = (M.CHANFRO_PE - (M.PROF / 2 - M.BASE_Y / 2)) / (1 - M.TAN)
    tx.text(0.04, 0.870,
            "Eu media a parede CONTRA A CASCA JÁ RECORTADA PELA SILHUETA, e\n"
            "achava zero de furo em toda a faixa de baixo. O problema é que a\n"
            "referência tinha o mesmo rasgo: o chanfro do pé come a parede nas\n"
            "duas, então a comparação não podia enxergar o que faltava.\n\n"
            "O teste que pega não usa referência nenhuma. De um ponto dentro do\n"
            f"cesto, {N_RAIO} raios na horizontal: se um sai sem cruzar "
            "material,\n"
            f"há caminho. Em z = {vg(Z_RAIO)} mm, "
            f"{int(a['fuga'].sum())} raios saíam — todos entre\n"
            f"{np.degrees(a['ang'][a['fuga']]).min():.0f}° e "
            f"{np.degrees(a['ang'][a['fuga']]).max():.0f}°, "
            "ou seja apontando para a frente. Depois: zero, em\n"
            "todas as cotas de 7,5 a 39 mm (a 41 escapam 380: sao as\n"
            "listras, que e para estarem abertas).\n\n"
            "A CONTA DO RASGO. O chanfro é a reta y = −89 − z; a parede\n"
            f"externa, y = −({vg(M.BASE_Y/2, 2)} + {vg(M.TAN, 4)} z). Elas se "
            f"cruzam em z = {vg(zc, 2)} mm:\n"
            "abaixo dali o chanfro passa POR DENTRO da parede e a apaga. Como\n"
            f"a chapa do fundo termina em z = 7, sobrava rasgo de "
            f"{vg(a['faixa'][0][0], 1)} a {vg(a['faixa'][-1][0], 1)} mm\n"
            f"({vg(a['faixa'][-1][0] - a['faixa'][0][0], 1)} mm de altura) em "
            f"ate {max(f[1] for f in a['faixa']):.0f} mm de largura = "
            f"{a['area']:.0f} mm².\n"
            f"Acima dali, ate {vg(zc, 2)}, a parede sobrevivia como LÂMINA de "
            f"0 a 1,4 mm —\nseção que não enche na injeção.\n\n"
            "A TAPA é uma parede de 1,4 mm deitada sobre o plano do chanfro: a\n"
            "silhueta menos ela mesma deslocada 1,4/√2 em y e em z. Cortada\n"
            "por `fora`, ela TERMINA SOZINHA onde o chanfro sai da casca — não\n"
            "há cota para acertar à mão, e se o chanfro mudar ela acompanha.\n"
            f"Custa {vg(b['peso'] - a['peso'], 1)} g (eram 0,7 g a 12° de "
            f"saída, quando a faixa a\ntapar tinha 1,8 mm de altura e não "
            f"{vg(a['faixa'][-1][0] - a['faixa'][0][0], 1)}). Por dentro fica "
            f"uma transição\nchanfrada no pé da parede da frente, que ainda "
            f"ajuda a varrer o cesto.",
            fontsize=8.2, color=TINTA, va="top", linespacing=1.44)

    fig.savefig(os.path.join(DEST, "frente.png"), dpi=118, facecolor=FUNDO)
    print("gerado frente.png")


if __name__ == "__main__":
    main()
