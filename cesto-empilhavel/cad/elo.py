#!/usr/bin/env python3
"""Folha elo.png: a linha ELO inteira -- P, M e G, e os P pousados em cima.

NAO remede nada. As MEDICOES saem de cad/elo-medidas.json e as malhas dos
STLs que visor_elo.py deixa, porque cada interferencia nestas pecas custa
minutos de booleano -- e medir a mesma coisa em dois scripts e o caminho
mais curto para as duas folhas divergirem (ja aconteceu com o tripe e com
a soltura).

As COTAS DE ENTRADA (boca, altura, saida, fundo vazado) saem do proprio
modelo3d, chamando as tres configuracoes: e o unico jeito de a folha nao
envelhecer calada quando o modelo muda. Esta folha JA envelheceu uma vez
assim -- ficou afirmando "o M e dois P acoplados, mesma profundidade,
mesma altura, nada foi adaptado" depois que o M virou 380 x 400 x 190 a
3 graus com fundo vazado. O assert la embaixo existe por causa disso.

Uso:  python3 visor_elo.py   (gera as medicoes e os STLs)
      python3 elo.py         (desenha a folha)
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from matplotlib.patches import Rectangle

import modelo3d as M
import render

DEST = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(DEST, "elo-medidas.json")

FUNDO = "#faf8f4"
TINTA, GRIS, NOVO, VERDE, CINZ = "#1d1813", "#6d645a", "#c2410c", "#15803d", "#64748b"
COR_P = (0.784, 0.337, 0.102)
COR_M = (0.627, 0.271, 0.102)
COR_G = (0.470, 0.220, 0.090)
VISTA = (-1.0, -1.6, -0.75)


def vg(x, casas=1, un=""):
    t = f"{x:.{casas}f}".replace(".", ",")
    return f"{t} {un}".strip()


def mil(x):
    return f"{x:,.0f}".replace(",", ".")


def cotas():
    """Le a boca, a altura e a saida das TRES configuracoes do modelo.

    So chama as funcoes de configuracao -- nao constroi solido nenhum, e
    por isso custa o tempo do import e nada mais.
    """
    c = {}
    for k, fn in (("p", M.padrao), ("m", M.padrao_m), ("g", M.padrao_g)):
        fn()
        c[k] = {"larg": M.LARG, "prof": M.PROF, "alt": M.ALT,
                "saida": M.DRAFT, "base_y": M.BASE_Y,
                "fundo": M.FUNDO_VAZADO, "passo": M.passo_acoplado()}
    return c


def move(m, dx=0.0, dy=0.0, dz=0.0):
    c = m.copy()
    c.apply_translation([dx, dy, dz])
    return c


RAPIDO = False


def cena(pecas, arq, largura=900):
    """Renderiza a cena -- ou reaproveita o PNG, com --rapido.

    As sete cenas levam dois minutos juntas, e mexer no texto ou na diagramacao
    da folha nao muda nenhuma delas.
    """
    destino = os.path.join(DEST, arq)
    if RAPIDO and os.path.exists(destino):
        return destino
    img = render.render(pecas, direcao=VISTA, largura=largura)
    return render.salvar(img, destino)


def painel(fig, x, w, topo, arq, titulo, cor):
    """Uma cena com a moldura do tamanho exato da imagem. Devolve a altura."""
    from PIL import Image
    im = np.asarray(Image.open(os.path.join(DEST, arq)))
    fw, fh = fig.get_size_inches()
    h = w * (fw / fh) * im.shape[0] / im.shape[1]
    ax = fig.add_axes([x, topo - h, w, h])
    ax.imshow(im)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#e3e0da")
    ax.set_title(titulo, fontsize=11.5, color=cor, weight="bold", pad=6)
    return h


def fila(fig, itens, topo, h_alvo, x0=0.028, x1=0.972, gap=0.020):
    """Desenha uma fileira de cenas com a MESMA altura e legendas alinhadas.

    Dar uma largura fixa a cada painel deixa cada moldura com uma altura
    diferente, e a legenda de cada um desce ate onde o painel acabou: a
    fileira sai desalinhada e as legendas mais baixas invadem a caixa de
    baixo. Aqui a altura da fileira e que manda -- as larguras saem do
    aspecto de cada imagem -- e todas as legendas ficam na mesma cota.
    """
    from PIL import Image
    fw, fh = fig.get_size_inches()
    asp = []
    for it in itens:
        im = np.asarray(Image.open(os.path.join(DEST, it[0])))
        asp.append(im.shape[1] / im.shape[0])
    h = min(h_alvo, (x1 - x0 - gap * (len(itens) - 1))
            / sum(a * fh / fw for a in asp))
    largs = [h * (fh / fw) * a for a in asp]
    x = x0 + (x1 - x0 - sum(largs) - gap * (len(itens) - 1)) / 2
    for (arq, titulo, cor, linhas), w in zip(itens, largs):
        painel(fig, x, w, topo, arq, titulo, cor)
        fig.text(x + w / 2, topo - h - 0.010, "\n".join(linhas),
                 ha="center", va="top", fontsize=8.5, color=TINTA,
                 linespacing=1.55)
        x += w + gap
    return h


def main(rapido=False):
    global RAPIDO
    RAPIDO = rapido
    if not os.path.exists(DADOS):
        raise SystemExit("falta elo-medidas.json -- rode visor_elo.py antes")
    d = json.load(open(DADOS, encoding="utf-8"))
    c = cotas()

    # A folha so pode falar do que foi medido: se o modelo mudou de boca
    # depois da ultima medicao, o json e de outra peca.
    for k in ("p", "m", "g"):
        if (c[k]["larg"], c[k]["prof"]) != (d[k]["larg"], d[k]["prof"]):
            raise SystemExit(
                f"elo-medidas.json esta velho: o {k.upper()} do modelo e "
                f"{c[k]['larg']:.0f} x {c[k]['prof']:.0f} e o medido e "
                f"{d[k]['larg']:.0f} x {d[k]['prof']:.0f}. Rode visor_elo.py.")

    p, m, g = d["p"], d["m"], d["g"]
    mp = trimesh.load(os.path.join(DEST, "elo-p.stl"))
    mm = trimesh.load(os.path.join(DEST, "elo-m.stl"))
    mg = trimesh.load(os.path.join(DEST, "elo-g.stl"))

    pp = d["passo_p"] / 2

    def tam(*ms):
        """Envelope de um conjunto de malhas. Bounding box, sem booleano."""
        b = np.array([x.bounds for x in ms])
        return b[:, 1, :].max(0) - b[:, 0, :].min(0)

    env_p = tam(mp)
    env_par = tam(move(mp, -pp), move(mp, pp))
    env_tri = tam(*[move(mp, k * d["passo_p"]) for k in (-1, 0, 1)])
    # A folha afirma que o par bate com o M e o trio com o G em x, com
    # 0,0000 mm. Se algum dia deixar de bater, ela nao pode imprimir isso.
    for nome, a, b in (("par/M", env_par[0], m["env"][0]),
                       ("trio/G", env_tri[0], g["env"][0])):
        if abs(a - b) > 1e-3:
            raise SystemExit(f"{nome} nao bate mais em x: {a:.4f} vs {b:.4f}")

    pn = (d["pn_p"], d["pn_m"], g["pn"])
    pe = (d["pe_p"], d["pe_m"], g["pe"])
    altz = (132.5, m["env"][2], g["env"][2])
    cub = [a + 11 * n for a, n in zip(altz, pn)]     # 12 pecas encaixadas
    ap_p, ap_m, ap_g = sum(d["ap_p"]), sum(d["ap_m"]), sum(g["ap"])
    par, tri = d["par"], g["trio"]["recuado"]
    ap_par, ap_tri = sum(par["ap"]), sum(tri["ap"])
    ap_cen = sum(d["par_todos"]["21"]["ap"])

    # --- as cenas ---------------------------------------------------------
    # Tres paineis separados, cada um normalizado pela largura da imagem,
    # mentem sobre o tamanho relativo -- o P sairia do tamanho do G. Uma
    # cena so, com os tres lado a lado, mostra a linha na escala real.
    # Os centros saem de uma folga de 110 mm entre envelopes: o P ocupa
    # -100..104 do seu eixo, o M -200..204 e o G -300..304. Com o M a -366,
    # como estava, ele entra 136 mm DENTRO do G e as duas pecas saem
    # fundidas na imagem.
    cena([(move(mp, -1030), COR_P), (move(mm, -614), COR_M), (mg, COR_G)],
         "elo-linha.png", 1600)
    cena([(mg, COR_G)] + [(move(mg, 0, i * d["desloc"], i * g["pn"]),
                           COR_G if i % 2 else COR_P) for i in range(1, 6)],
         "elo-encaixa.png", 900)
    cena([(mm, COR_M),
          (move(mp, -pp, par["dy"], par["z"]), COR_P),
          (move(mp, pp, par["dy"], par["z"]), COR_P)], "elo-dois.png", 1000)
    cena([(mg, COR_G)] + [(move(mp, k * d["passo_p"], tri["dy"], tri["z"]),
                           COR_P) for k in (-1, 0, 1)], "elo-trio.png", 1180)
    cena([(mg, COR_G), (move(mg, c["g"]["passo"], 0, 0), COR_P)],
         "elo-acopla.png", 1180)

    # --- a folha ----------------------------------------------------------
    fig = plt.figure(figsize=(16.4, 15.2), facecolor=FUNDO)
    fig.text(0.5, 0.986, "Linha ELO: cada tamanho é a pegada de N P acoplados",
             ha="center", va="top", fontsize=21, color=TINTA, weight="bold")
    fig.text(0.5, 0.963,
             f"em x nada foi escolhido — {m['larg']:.0f} = 2 × "
             f"{p['larg']:.0f} + 2 × 10 e {g['larg']:.0f} = 3 × "
             f"{p['larg']:.0f} + 2 × 20 · em y, altura e saída, tudo "
             "precisou mudar",
             ha="center", va="top", fontsize=11.5, color="#3d444d")

    fila(fig, [
        ("elo-linha.png", "A LINHA, NA MESMA ESCALA", NOVO, [
            f"P  {p['larg']:.0f} × {p['prof']:.0f} × {c['p']['alt']:.0f} a "
            f"{c['p']['saida']:.0f}°  ·  {vg(p['cap'], 2)} L  ·  "
            f"{vg(p['peso'])} g  ·  {vg(p['peso'] / p['cap'])} g/L  ·  "
            f"{p['furos']} rasgos  ·  fundo cheio",
            f"M  {m['larg']:.0f} × {m['prof']:.0f} × {c['m']['alt']:.0f} a "
            f"{c['m']['saida']:.0f}°  ·  {vg(m['cap'], 2)} L  ·  "
            f"{vg(m['peso'])} g  ·  {vg(m['peso'] / m['cap'])} g/L  ·  "
            f"{m['furos']} rasgos  ·  fundo vazado",
            f"G  {g['larg']:.0f} × {g['prof']:.0f} × {c['g']['alt']:.0f} a "
            f"{c['g']['saida']:.0f}°  ·  {vg(g['cap'], 2)} L  ·  "
            f"{vg(g['peso'])} g  ·  {vg(g['peso'] / g['cap'])} g/L  ·  "
            f"{g['furos']} rasgos  ·  fundo vazado"]),
        ("elo-encaixa.png", "G ENCAIXADOS", CINZ, [
            f"passo {vg(g['pn'], 2)} mm · 12 peças em {cub[2]:.0f} mm",
            f"cubagem: P {cub[0]:.0f} · M {cub[1]:.0f} · G {cub[2]:.0f} mm",
            f"{vg(pe[2] / pn[2])}× mais peça que empilhado"]),
    ], 0.925, 0.190)

    fila(fig, [
        ("elo-dois.png", "DOIS P EMPILHADOS NO M", VERDE, [
            f"recuado {par['dy']:.0f} mm em y · passo {vg(par['z'], 2)} mm",
            f"interferência {vg(par['interf'], 4)} mm³",
            f"contato {ap_par:.0f} mm² — {vg(ap_par / ap_m)}× o tripé do M"]),
        ("elo-trio.png", "TRÊS P EMPILHADOS NO G", VERDE, [
            f"recuado {tri['dy']:.0f} mm em y · passo {vg(tri['z'], 2)} mm",
            f"interferência {vg(tri['interf'], 4)} mm³",
            f"contato {mil(ap_tri)} mm² em cinco ilhas "
            f"({tri['ap'][0]:.0f} × 3 + {tri['ap'][3]:.0f} × 2)"]),
        ("elo-acopla.png", "G ACOPLADOS", CINZ, [
            f"passo {c['g']['passo']:.0f} = {g['larg']:.0f} + 2 × 10 mm",
            f"{vg(g['interf'], 4)} mm³ no contato · trava 27,2 a 1,2 mm no M",
            f"solta levantando {vg(g['solta'])} mm"]),
    ], 0.660, 0.175)

    # --- a tabela ---------------------------------------------------------
    tb = fig.add_axes([0.028, 0.032, 0.455, 0.375]); tb.axis("off")
    # FIXAR os limites: o tb.plot() da linha divisoria autoescala o eixo e
    # joga todo o texto para fora da vista (a caixa desenha, o conteudo nao).
    tb.set_xlim(0, 1); tb.set_ylim(0, 1)
    tb.add_patch(Rectangle((0, 0), 1, 1, transform=tb.transAxes,
                           facecolor="#fdf6f1", edgecolor="#f0d3c2", lw=1.3))
    tb.text(0.040, 0.962, "MEDIDO NO SÓLIDO", fontsize=11.5, color=NOVO,
            weight="bold", va="top")
    linhas = [
        ("", "ELO P", "ELO M", "ELO G"),
        ("boca do corpo",
         f"{p['larg']:.0f} × {p['prof']:.0f}", f"{m['larg']:.0f} × {m['prof']:.0f}",
         f"{g['larg']:.0f} × {g['prof']:.0f}"),
        ("altura · saída",
         f"{c['p']['alt']:.0f} · {c['p']['saida']:.0f}°",
         f"{c['m']['alt']:.0f} · {c['m']['saida']:.0f}°",
         f"{c['g']['alt']:.0f} · {c['g']['saida']:.0f}°"),
        ("envelope em x", vg(env_p[0], 1, "mm"), vg(m["env"][0], 1, "mm"),
         vg(g["env"][0], 1, "mm")),
        ("envelope em y", vg(env_p[1], 1, "mm"), vg(m["env"][1], 1, "mm"),
         vg(g["env"][1], 1, "mm")),
        ("capacidade", vg(p["cap"], 2, "L"), vg(m["cap"], 2, "L"),
         vg(g["cap"], 2, "L")),
        ("peso em PP", vg(p["peso"], 1, "g"), vg(m["peso"], 1, "g"),
         vg(g["peso"], 1, "g")),
        ("grama por litro", vg(p["peso"] / p["cap"]), vg(m["peso"] / m["cap"]),
         vg(g["peso"] / g["cap"])),
        ("rasgos", f"{p['furos']}", f"{m['furos']}", f"{g['furos']}"),
        ("fundo vazado", "não", "sim", "sim"),
        ("passo encaixado", vg(pn[0], 2, "mm"), vg(pn[1], 2, "mm"),
         vg(pn[2], 2, "mm")),
        ("passo empilhado", vg(pe[0], 2, "mm"), vg(pe[1], 2, "mm"),
         vg(pe[2], 2, "mm")),
        ("passo acoplado", f"{c['p']['passo']:.0f} mm",
         f"{c['m']['passo']:.0f} mm", f"{c['g']['passo']:.0f} mm"),
        ("solta levantando", vg(d["solta_p"], 1, "mm"),
         vg(d["solta_m"], 1, "mm"), vg(g["solta"], 1, "mm")),
        ("tripé de apoio", f"{ap_p:.0f} mm²", f"{ap_m:.0f} mm²",
         f"{ap_g:.0f} mm²"),
        ("preso no molde", f"{mil(d['preso_p'])} mm³",
         f"{mil(d['preso_m'])} mm³", f"{mil(g['preso'])} mm³"),
    ]
    y = 0.890
    for i, (k, a, b, e) in enumerate(linhas):
        w = "bold" if i == 0 else "normal"
        tb.text(0.040, y, k, fontsize=9.2, color=GRIS if i == 0 else TINTA,
                va="center", weight=w)
        for x, v, cor in ((0.600, a, CINZ), (0.790, b, VERDE),
                          (0.965, e, VERDE)):
            tb.text(x, y, v, fontsize=9.2, color=GRIS if i == 0 else cor,
                    va="center", ha="right", weight=w)
        y -= 0.0470
    tb.plot([0.040, 0.965], [y + 0.020, y + 0.020], color="#f0d3c2", lw=1)
    tb.text(0.040, y - 0.008,
            "O passo ENCAIXADO não segue a altura, segue a SAÍDA. Previ que\n"
            f"baixar o M de 220 para {c['m']['alt']:.0f} mm derrubaria o "
            f"passo de {vg(pn[1], 2)} para ~44 mm;\n"
            f"medido, deu {vg(pn[1], 2)} nas DUAS alturas. O G confirma por "
            "outro caminho:\n"
            f"{vg(pn[2], 2)} mm com {c['g']['alt']:.0f} mm de altura, "
            f"também a {c['g']['saida']:.0f}°. A {c['p']['saida']:.0f}° o P "
            f"dá {vg(pn[0], 2)}.\n"
            "Quem manda no encaixe é a conicidade do PÉ, não o corpo.",
            fontsize=8.7, color=NOVO, va="top", linespacing=1.52)

    # --- o texto ----------------------------------------------------------
    tx = fig.add_axes([0.505, 0.032, 0.470, 0.375]); tx.axis("off")
    tx.set_xlim(0, 1); tx.set_ylim(0, 1)
    tx.add_patch(Rectangle((0, 0), 1, 1, transform=tx.transAxes,
                           facecolor="#f0fdf4", edgecolor="#bbf7d0", lw=1.3))
    tx.text(0.038, 0.962, "POR QUE 380 E 580 — E O QUE PRECISOU MUDAR",
            fontsize=11.5, color=VERDE, weight="bold", va="top")
    tx.text(0.038, 0.905,
            f"A aba do P sai 10 mm para fora de cada lado da boca de "
            f"{p['larg']:.0f}: dois P\nacoplados ficam com passo "
            f"{c['p']['passo']:.0f} mm e o par mede, na malha, "
            f"{vg(env_par[0])} mm\nem x. O M mede {vg(m['env'][0])} — diferença "
            "0,0000 mm. O trio mede\n"
            f"{vg(env_tri[0])} e o G mede {vg(g['env'][0])}, também 0,0000. "
            "É essa igualdade,\ne só ela, que faz o tamanho de baixo pousar "
            "no de cima.\n\n"
            "EM Y NÃO HERDOU NADA. O M e o G têm "
            f"{m['prof']:.0f} mm de profundidade\ncontra "
            f"{p['prof']:.0f} do P, e o par tem {vg(env_par[1])} — sobram "
            f"{vg(m['env'][1] - env_par[1])} mm de folga.\n"
            "Foi preciso decidir ONDE ele pousa, e a medição decidiu:\n"
            f"RECUADO no fundo (dy = {par['dy']:.0f}) apoia as duas saias "
            f"inteiras\n({par['ap'][0]:.0f} mm² cada) e os dois pés externos "
            f"({par['ap'][2]:.0f} mm² cada),\n{ap_par:.0f} mm² no total. "
            f"CENTRADO sobra só a ponta dos pés: {ap_cen:.0f} mm²,\n"
            f"{vg(ap_par / ap_cen)}× menos. O trio no G repete o padrão: "
            f"{mil(ap_tri)} mm²\nrecuado contra "
            f"{sum(g['trio']['centrado']['ap']):.0f} mm² centrado.\n\n"
            "DE GRAÇA: com deslocamento ZERO em y o par não empilha —\n"
            f"ENCAIXA dentro do M, a {vg(d['par_todos']['0']['z'], 2)} mm. "
            f"Os mesmos {d['desloc']:.0f} mm que\ntrocam encaixe por pilha "
            "no P trocam também aqui.\n\n"
            "O QUE FOI ADAPTADO, e não é pouco:\n"
            f"• a saída caiu de {c['p']['saida']:.0f}° para "
            f"{c['m']['saida']:.0f}° — a {c['p']['saida']:.0f}° a base do M "
            f"fecharia em\n  {vg(m['prof'] - 2 * c['m']['alt'] * np.tan(np.radians(c['p']['saida'])))} "
            f"mm contra {vg(c['m']['base_y'])} a "
            f"{c['m']['saida']:.0f}°, e em peça de {m['prof']:.0f} cada mm "
            "de\n  fechamento custa litro;\n"
            "• o fundo virou chapa VAZADA nos dois tamanhos grandes, para\n"
            "  caber no peso — e, medido, sem prender 1 mm³ a mais no molde;\n"
            "• os rasgos de parede tiveram de ser REPLANTADOS: o prisma que\n"
            f"  os corta nasce em PROF/2 − 20, e com o {c['p']['prof'] / 2 - 20:.0f} "
            "fixo do P ele erra a\n  parede de "
            f"{m['prof']:.0f} inteira — a peça sai MACIÇA na frente e no fundo.",
            fontsize=8.4, color=TINTA, va="top", linespacing=1.44)

    fig.savefig(os.path.join(DEST, "elo.png"), dpi=112, facecolor=FUNDO)
    print("gerado elo.png")


if __name__ == "__main__":
    main("--rapido" in sys.argv)
