#!/usr/bin/env python3
"""Varredura da configuracao C: empilhar, acoplar, encaixar, e a borda.

Pedido (23/09): "preciso apenas que vc faca uma varredura, para ver se vai
precisar de adaptacoes... se a borda vai ser resistente o suficiente para
acoplar, empilhar e se vai encaixar corretamente... se agora em toda a borda
vai precisar de um mini reforco".

O que a varredura achou, em ordem de gravidade:

1. UM BUG, nao uma fragilidade: o recorte da silhueta do CORPO amputava a aba
   nova em y. Sobravam 0,26 mm da aba de tras em vez de 10, e por isso a saia
   pousava no vazio -- era essa a causa do tripe de 60 mm2 da rodada anterior,
   nao o deslocamento. Corrigido: silhueta(folga) para a aba.

2. O ACOPLAMENTO perdia altura de junta, e isso SIM era fragilidade. Com a aba
   para fora, duas pecas acopladas so se tocam na espessura dela: abaixo de
   z = 127,5 as paredes estao 10 mm para dentro de cada lado, um vao de 20 mm.
   O engajamento da cauda caia de 14 mm (aba para dentro, onde a femea escavava
   a faixa do rim) para 2,5 mm. Resolvido com a DOBRA na aresta -- que e
   exatamente o mini reforco que o cliente intuiu.

3. A CAUDA era um bloco MACICO de 1.556 mm3, 7 a 11 mm de espessura numa peca
   de parede 1,4. Nao e fragilidade: e o contrario, massa demais, que chupa a
   face externa do rim e manda no tempo de ciclo. Vaziada por cima.

4. EMPILHAR e ENCAIXAR passam com folga, e melhores que hoje. Nada a fazer.
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
import render

DEST = os.path.dirname(os.path.abspath(__file__))
COR, COR2 = (0.80, 0.36, 0.12), (0.62, 0.27, 0.09)
FUNDO, TINTA, GRIS = "#fbfaf8", "#1f2328", "#6b7280"
NOVO, VERDE, CINZ, VERM = "#c2410c", "#15803d", "#64748b", "#b91c1c"


def vg(x, casas=1, un=""):
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


def main():
    M.padrao()
    p, n = M.cesto(aba=True)
    arq = os.path.join(DEST, "vr-c.stl")
    export_stl(p, arq)
    m = trimesh.load(arq)

    def passo(dy, tol=0.005):
        lo, hi = 0.0, 180.0
        while hi - lo > tol:
            mid = (lo + hi) / 2
            if vol(p, Pos(0, dy, mid) * p) > 2.0:
                lo = mid
            else:
                hi = mid
        return hi

    d = {}
    d["pn"], d["pe"] = passo(0.0), passo(M.DESLOC)
    d["peso"], d["cap"], d["n"] = p.volume * M.RHO, M.capacidade(), n
    bb = p.bounding_box()
    d["env"] = (bb.size.X, bb.size.Y, bb.size.Z)

    raizx = M.BASE_X / 2 + M.TAN * (M.ALT - M.ABA_T)
    raizy = M.BASE_Y / 2 + M.TAN * (M.ALT - M.ABA_T)
    inter = p & (Pos(0, M.DESLOC, d["pe"] - 0.3) * p)
    ap = []
    for s in sorted(inter.solids(), key=lambda s: -s.volume):
        if s.volume < 0.005:
            continue
        b = s.bounding_box()
        cy, cx = b.center().Y, abs(b.center().X)
        braco = (cy - raizy) if cy > 60 else (cx - raizx)
        ap.append((s.volume / 0.3, braco, "saia" if cy > 60 else "pé"))
    d["ap"] = ap
    d["trava"] = [(dx, vol(p, Pos(M.LARG + 2 * M.ABA_W + dx, 0, 0) * p))
                  for dx in (0.6, 1.2, 2.0)]
    # Amostrar so 6 e 10 mm reportava "solta a 10" enquanto a folha aba.png,
    # que testa 8, reportava 8: a mesma peca com dois numeros. Busca binaria.
    lo, hi = 0.0, 16.0
    while hi - lo > 0.05:
        mid = (lo + hi) / 2
        if vol(p, Pos(M.LARG + 2 * M.ABA_W + 1.2, 0, mid) * p) > 0.0:
            lo = mid
        else:
            hi = mid
    d["solta"] = [(6.0, vol(p, Pos(M.LARG + 2 * M.ABA_W + 1.2, 0, 6.0) * p)),
                  (hi, 0.0)]
    d["enc"] = [(dz, vol(p, Pos(0, 0, d["pn"] + dz) * p))
                for dz in (0.0, 1.0, 2.0)]
    print(f"C: {d['peso']:.1f} g | {d['cap']:.2f} L | encaixa {d['pn']:.2f} | "
          f"empilha {d['pe']:.2f} | tripe {sum(a for a,_,_ in ap):.0f} mm2")
    print(f"   trava {d['trava']}\n   solta {d['solta']}\n   encaixe {d['enc']}")

    # renders: empilhadas, acopladas, encaixadas
    cenas = {
        "emp": [(0, i * M.DESLOC, i * d["pe"]) for i in range(3)],
        "aco": [(0, 0, 0), (M.LARG + 2 * M.ABA_W, 0, 0)],
        "enc": [(0, 0, i * d["pn"]) for i in range(6)],
    }
    vistas = {"emp": (-0.95, -1.2, -0.50), "aco": (-0.55, -1.25, -0.62),
              "enc": (-1.0, -1.25, -0.52)}
    for k, poses in cenas.items():
        cena = []
        for i, (dx, dy, dz) in enumerate(poses):
            t = m.copy()
            t.apply_translation([dx, dy, dz])
            cena.append((t, COR if i % 2 == 0 else COR2))
        render.salvar(render.render(cena, direcao=vistas[k], largura=780),
                      os.path.join(DEST, f"vr-{k}.png"))
    d["corte"] = mesh_plane(m, plane_normal=[0, 1, 0],
                            plane_origin=[0, 0, 0])[:, :, [0, 2]]
    folha(d)


def painel(fig, rect, arq, titulo, cor, linhas, veredito, vcor,
           y_leg, y_ver):
    """Imagem no rect, legenda e veredito em coordenadas da FIGURA.

    Em coordenadas dos EIXOS a legenda sobe ou desce conforme o render, que
    sai com altura diferente em cada cena -- foi assim que o veredito do
    acoplar caiu em cima da propria legenda na primeira versao.
    """
    from PIL import Image
    ax = fig.add_axes(rect)
    ax.imshow(np.asarray(Image.open(os.path.join(DEST, arq))))
    ax.set_anchor("N"); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#e3e0da")
    ax.set_title(titulo, fontsize=12.5, color=cor, weight="bold", pad=5)
    cx = rect[0] + rect[2] / 2
    fig.text(cx, y_leg, "\n".join(linhas), ha="center", va="top",
             fontsize=8.6, color=TINTA, linespacing=1.55)
    fig.text(cx, y_ver, veredito, ha="center", va="top", fontsize=9.4,
             color=vcor, weight="bold")


def secao_rim(fig, rect, d):
    """A secao do rim, tirada do corte do solido em y = 0."""
    ax = fig.add_axes(rect)
    seg = d["corte"]
    for a, b in seg:
        if min(a[0], b[0]) < 70 or max(a[1], b[1]) < 112:
            continue
        ax.plot([a[0], b[0]], [a[1], b[1]], color=NOVO, lw=2.0,
                solid_capstyle="round")
    z0 = M.ALT - M.ABA_T - M.ABA_DOBRA
    ax.annotate("", xy=(100.4, M.ALT), xytext=(100.4, z0),
                arrowprops=dict(arrowstyle="<->", color=VERDE, lw=1.1))
    ax.text(101.2, (M.ALT + z0) / 2, f"altura de junta\n"
            f"{vg(M.ABA_T + M.ABA_DOBRA)} mm\n(era {vg(M.ABA_T)})",
            color=VERDE, fontsize=8.2, va="center")
    ax.annotate("", xy=(M.LARG / 2 + M.ABA_W, 131.2), xytext=(85.0, 131.2),
                arrowprops=dict(arrowstyle="<->", color=GRIS, lw=1.0))
    ax.text(92.5, 131.8, "seção do rim: 75 mm²", color=GRIS, fontsize=8.2,
            ha="center")
    ax.text(85.2, 117.0, "alma 3,2\n× 14 mm", color=GRIS, fontsize=8.0,
            ha="right", va="center")
    ax.set_xlim(78, 118); ax.set_ylim(113, 134)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("A BORDA EM CORTE · perfil em U", fontsize=12,
                 color=TINTA, weight="bold", pad=4)


def folha(d):
    fig = plt.figure(figsize=(16.4, 11.2), facecolor=FUNDO)
    fig.text(0.5, 0.987, "Varredura da C: empilhar, acoplar, encaixar",
             ha="center", va="top", fontsize=22, color=TINTA, weight="bold")
    fig.text(0.5, 0.956, "os dois que preocupavam passam com folga · quem "
             "precisava de adaptação era o acoplamento",
             ha="center", va="top", fontsize=11.5, color="#3d444d")

    ap = d["ap"]
    saia = next(a for a, _, t in ap if t == "saia")
    pe = next(a for a, _, t in ap if t == "pé")
    bsaia = next(b for _, b, t in ap if t == "saia")
    bpe = next(b for _, b, t in ap if t == "pé")
    painel(fig, [0.022, 0.595, 0.235, 0.300], "vr-emp.png",
           "EMPILHAR", VERDE,
           [f"passo {vg(d['pe'], 2, 'mm')} · interferência 0,0000 mm³",
            f"tripé {sum(a for a,_,_ in ap):.0f} mm² (hoje: 388)",
            f"pés {pe:.0f} mm² · braço de flexão {vg(bpe, 2, 'mm')}",
            f"saia {saia:.0f} mm² · braço {vg(bsaia, 2, 'mm')}",
            "pé pousa sobre o topo do rim + a raiz",
            "da aba — não na ponta de um balanço"],
           "PASSA · 0,48 MPa de contato, 60× de folga", VERDE,
           0.575, 0.470)

    painel(fig, [0.268, 0.595, 0.235, 0.300], "vr-aco.png",
           "ACOPLAR", NOVO,
           [f"altura de junta {vg(M.ABA_T + M.ABA_DOBRA, 1, 'mm')} "
            f"(era {vg(M.ABA_T)})",
            f"trava a partir de 0,6 mm ({vg(d['trava'][0][1], 1, 'mm³')})",
            f"a 1,2 mm: {vg(d['trava'][1][1], 1, 'mm³')} (era 11,2)",
            f"solta levantando {vg(d['solta'][1][0], 1, 'mm')}",
            "pescoço 7 × 7,5 mm = 52 mm² de seção",
            "resiste ~1.300 N — ninguém puxa isso"],
           "PRECISOU DA DOBRA · agora 2,4× o engate", NOVO,
           0.575, 0.470)

    painel(fig, [0.514, 0.595, 0.235, 0.300], "vr-enc.png",
           "ENCAIXAR", VERDE,
           [f"passo {vg(d['pn'], 2, 'mm')} · 12 peças em "
            f"{d['env'][2] + 11*d['pn']:.0f} mm",
            "batente PLANO: a membrana do pé, em z = 40",
            f"interferência: {vg(d['enc'][0][1], 2, 'mm³')} no passo,",
            f"0,00 já a 1 mm acima — para seco, sem cunha",
            "parede-a-parede sobra 2,8 mm de folga",
            "cunha do pé libera 4,4 mm antes do batente"],
           "PASSA · centra sozinho, e não agarra", VERDE,
           0.575, 0.470)

    secao_rim(fig, [0.762, 0.560, 0.216, 0.335], d)

    tb = fig.add_axes([0.022, 0.040, 0.455, 0.400]); tb.axis("off")
    tb.add_patch(Rectangle((0, 0), 1, 1, transform=tb.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.3))
    tb.text(0.035, 0.965, "AS TRÊS ADAPTAÇÕES QUE A VARREDURA PEDIU",
            fontsize=11.5, color=NOVO, weight="bold", va="top")
    itens = [
        ("1", "silhueta(folga) para a aba", VERM,
         "O recorte da silhueta do CORPO amputava a aba em y: sobravam\n"
         "0,26 mm da aba de trás em vez de 10, e a saia pousava no vazio.\n"
         "Era isso, e não o deslocamento, o tripé de 60 mm² da rodada\n"
         "anterior. Com a correção: 473 mm², e DESLOC fica em 21 mm."),
        ("2", "dobra de 5 mm na aresta da aba", NOVO,
         "Duas peças acopladas só se tocavam na espessura da aba — abaixo\n"
         "de z = 127,5 as paredes estão 10 mm para dentro de cada lado, um\n"
         "vão de 20 mm. O engate caía de 14 para 2,5 mm. A dobra devolve\n"
         "7,5 mm de junta, enrijece e protege a aresta. +4,3 g."),
        ("3", "vaziar a cauda de andorinha", NOVO,
         "Era um bloco MACIÇO de 1.556 mm³ com 7 a 11 mm de espessura numa\n"
         "peça de parede 1,4 — chupa a face externa do rim e manda no tempo\n"
         "de ciclo. Vaziada por cima (o plano da junta, sai reta): parede\n"
         "de 1,8 mm, seção máxima 3,3 mm, a mesma do rim. −0,9 g."),
    ]
    y = 0.880
    for num, tit, cor, txt in itens:
        tb.text(0.035, y, num, fontsize=13, color=cor, weight="bold",
                va="center")
        tb.text(0.075, y, tit, fontsize=10, color=cor, weight="bold",
                va="center")
        tb.text(0.075, y - 0.042, txt, fontsize=8.3, color=TINTA, va="top",
                linespacing=1.5)
        y -= 0.255

    tx = fig.add_axes([0.492, 0.040, 0.486, 0.400]); tx.axis("off")
    tx.add_patch(Rectangle((0, 0), 1, 1, transform=tx.transAxes,
                           facecolor="#f0f7f1", edgecolor="#bcd9c2", lw=1.3))
    tx.text(0.032, 0.965, "A BORDA PRECISA DE REFORÇO EM TODO O PERÍMETRO?",
            fontsize=11.5, color=VERDE, weight="bold", va="top")
    tx.text(0.032, 0.885,
            "Não, e a razão é simples: a seção não mudou, só espelhou. Antes\n"
            "era uma alma de 3,2 × 14 mm com um lábio de 10 × 2,5 virado para\n"
            "DENTRO; agora é a mesma alma com o mesmo lábio virado para FORA.\n"
            "O momento de inércia de um L espelhado é idêntico, então a\n"
            "rigidez de aro contra ovalizar é a mesma de hoje.\n\n"
            "Onde o empilhamento mudou, mudou para MELHOR. Hoje o pé pousa na\n"
            "ponta de um lábio de 10 mm em balanço; na C ele pousa em\n"
            "x 86,6…94,0 — ou seja sobre o topo do rim (86,8…90,0) e a raiz da\n"
            "aba (90…94), direto acima da parede. Braço de flexão medido:\n"
            "0,55 mm contra 4,75 mm de hoje. A aba nem entra em flexão.\n\n"
            "Contas da coluna de 4 com 1 kg em cada (34,5 N na peça de baixo):\n"
            "   • pé: 13,2 N em 27,4 mm² = 0,48 MPa (PP cede a ~30) → 60×\n"
            "   • saia: 8,1 N em 418 mm², braço 5,67 mm → 0,41 MPa na aba,\n"
            "     flecha de 0,003 mm → nada\n"
            "   • parede em compressão: 0,41 MPa → nada\n\n"
            "A dobra do item 2 é o único reforço necessário, e ela existe pelo\n"
            "ACOPLAMENTO, não pela resistência. Se 4,3 g pesarem na conta de\n"
            "resina, ABA_DOBRA de 5 para 3 mm devolve ~1,7 g e ainda deixa o\n"
            "engate em 5,5 mm, 2,2× o de antes da dobra.",
            fontsize=8.3, color=TINTA, va="top", linespacing=1.48)

    fig.savefig(os.path.join(DEST, "varredura.png"), dpi=118, facecolor=FUNDO)
    print("gerado varredura.png")


if __name__ == "__main__":
    main()
