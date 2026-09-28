#!/usr/bin/env python3
"""Folha mercado.png: a linha ELO contra o mercado, em peso e em preco.

Desenhada por mercado.py --folha. Nao busca nada e nao mede nada: recebe
tudo de la, porque a fonte de cada numero tem de morar num lugar so.

As cores das tres series passaram pelo validador de paleta (banda de
luminosidade, piso de croma, separacao para daltonismo deutan/protan/tritan
e contraste contra o fundo): laranja #c2410c para a ELO -- a cor da casa
nas outras folhas --, azul #0369a1 para o cesto expositor e violeta #6d28d9
para a caixa agricola. O par laranja+verde que as outras folhas usam
REPROVOU aqui (deltaE 7,0 em deutan): verde e laranja lado a lado, como
series de dados, somem juntos para quem nao distingue vermelho e verde.
"""
import os

import matplotlib
matplotlib.use("Agg")
# Dois "$" na mesma string ligam o modo matematico do matplotlib: um texto
# como "R$ 3,85 contra R$ 3,88" sai em italico, sem os $, tudo colado.
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

DEST = os.path.dirname(os.path.abspath(__file__))

FUNDO = "#faf8f4"
TINTA, GRIS = "#1d1813", "#6d645a"
ELO, EXPO, AGRI = "#c2410c", "#0369a1", "#6d28d9"
GRADE = "#e7e2da"
TIER = {"expositor": EXPO, "agricola": AGRI}
NOME_TIER = {"expositor": "cesto expositor (canal loja)",
             "agricola": "caixa agricola hortifruti"}


def vg(x, casas=1, un=""):
    t = f"{x:.{casas}f}".replace(".", ",")
    return f"{t} {un}".strip()


def mil(x):
    return f"{x:,.0f}".replace(",", ".")


def desenhar(linha, mercado, n047, dom25, k_b2b, k_dom, custo_kg, preco_kg,
             coleta, bin_est):
    est, _, fator = bin_est
    fig = plt.figure(figsize=(16.4, 13.6), facecolor=FUNDO)

    fig.text(0.5, 0.985, "ELO contra o mercado: o mesmo litro, quanto de "
             "plástico e quanto de preço", ha="center", va="top",
             fontsize=20.5, color=TINTA, weight="bold")
    fig.text(0.5, 0.962,
             f"vitrines coletadas em {coleta} · preço de fábrica equivalente "
             f"= vitrine ÷ múltiplo de canal ({vg(k_b2b[0], 1)}–"
             f"{vg(k_b2b[1], 1)}× no canal loja, PREMISSA; "
             f"{vg(n047['varejo'][0] / n047['fabrica'], 2)}–"
             f"{vg(n047['varejo'][1] / n047['fabrica'], 2)}× no doméstico, "
             "MEDIDO no nosso 047)",
             ha="center", va="top", fontsize=11, color="#3d444d")

    # ---- painel A: capacidade x peso ------------------------------------
    ax = fig.add_axes([0.050, 0.600, 0.295, 0.320])
    ax.set_facecolor(FUNDO)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRADE)
    ax.grid(True, color=GRADE, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlim(0, 60); ax.set_ylim(0, 1850)
    ax.set_xlabel("capacidade (L)", fontsize=9.5, color=GRIS)
    ax.set_ylabel("peso da peça (g)", fontsize=9.5, color=GRIS)
    ax.tick_params(colors=GRIS, labelsize=8.8)

    # raios de g/L constante: transformam a dispersao em "abaixo e mais leve"
    for gl, fim in ((15, 42.0), (30, 45.0)):
        ax.plot([0, fim], [0, fim * gl], ls=(0, (4, 4)), lw=1.0,
                color="#c9c2b6", zorder=1)
        ax.text(fim - 0.6, fim * gl + 18, f"{gl} g/L", fontsize=8.2,
                color="#9a9184", ha="right", va="bottom")

    vistos = set()
    for ref, desc, tier, dim, lt, kg, pr, fonte, nota in mercado:
        if not kg:
            continue
        x = lt if lt else est
        rot = NOME_TIER[tier] if tier not in vistos else None
        vistos.add(tier)
        ax.plot(x, kg * 1000, "o", ms=9, color=TIER[tier], mec=FUNDO, mew=1.6,
                zorder=4, label=rot)
    ax.plot(n047["litros"], n047["kg"] * 1000, "s", ms=9, color=FUNDO,
            mec=ELO, mew=2.0, zorder=5, label="047, o cesto de hoje (nosso)")
    ax.annotate("047", (n047["litros"], n047["kg"] * 1000),
                textcoords="offset points", xytext=(9, -3), fontsize=8.6,
                color=ELO, weight="bold")
    for it in linha:
        ax.plot(it["litros"], it["kg"] * 1000, "o", ms=11, color=ELO,
                mec=FUNDO, mew=1.8, zorder=6,
                label="linha ELO" if it["nome"] == "ELO P" else None)
        ax.annotate(it["nome"].split()[1],
                    (it["litros"], it["kg"] * 1000),
                    textcoords="offset points", xytext=(10, -4),
                    fontsize=10.5, color=ELO, weight="bold")
    ax.set_title("Mesma prateleira, menos plástico — acima de 25 L",
                 fontsize=12, color=TINTA, weight="bold", pad=8, loc="left")
    leg = ax.legend(loc="upper left", fontsize=8.6, frameon=False,
                    handletextpad=0.4, borderaxespad=0.6)
    for t in leg.get_texts():
        t.set_color(TINTA)

    fig.text(0.050, 0.552,
             f"O G entrega {vg(linha[2]['litros'], 2)} L com "
             f"{vg(linha[2]['kg']*1000)} g — "
             f"{vg(linha[2]['kg']*1000/linha[2]['litros'])} g/L, o mais leve\n"
             f"da amostra. A caixa agrícola de 50 L gasta "
             f"{vg(1.7*1000/50.5)} g/L e o cesto\nexpositor de 55 L, "
             f"{vg(0.95*1000/55)}. No tamanho do P a física vira contra:\n"
             f"{vg(linha[0]['kg']*1000/linha[0]['litros'])} g/L contra "
             f"~{vg(0.170*1000/est)} do bin — parede por litro cresce\n"
             "quando a peça encolhe, e o P ainda perde litro para a saída "
             "de 6°.",
             fontsize=8.7, color=TINTA, va="top", linespacing=1.5)

    # ---- painel B: preco de fabrica equivalente --------------------------
    bx = fig.add_axes([0.620, 0.600, 0.345, 0.320])
    bx.set_facecolor(FUNDO)
    for s in ("top", "right", "left"):
        bx.spines[s].set_visible(False)
    bx.spines["bottom"].set_color(GRADE)
    bx.grid(True, axis="x", color=GRADE, lw=0.8, zorder=0)
    bx.set_axisbelow(True)

    classes = [("mini, 4–5 L", ["bin-10", "bin-amz"], linha[0]),
               ("médio, 20–35 L", ["exp-30", "exp-35", "agr-20"], linha[1]),
               ("grande, 50–55 L", ["exp-55", "agr-50t", "agr-50e"], linha[2])]
    ypos, rotulos, faixas = [], [], []
    y = 0
    for titulo, refs, nosso in classes:
        y0 = y
        for r in refs:
            row = next(x for x in mercado if x[0] == r)
            lo, hi = row[6] / k_b2b[1], row[6] / k_b2b[0]
            bx.plot([lo, hi], [y, y], lw=7, color=TIER[row[2]],
                    solid_capstyle="round", zorder=3)
            bx.text(32.4, y, f"vitrine R$ {vg(row[6], 2)}", fontsize=8.0,
                    color=GRIS, va="center", ha="right")
            rotulos.append(row[1].replace("Caixa agricola", "Caixa agrícola")
                           .replace("plastico", "plástico")
                           .replace("pequeno", "peq.").replace("medio", "méd."))
            ypos.append(y)
            y -= 1
        faixas.append((titulo, y0, y + 1, nosso))
        y -= 0.9

    for titulo, y0, y1, nosso in faixas:
        preco = nosso["kg"] * preco_kg
        c_mo = nosso["kg"] * custo_kg["moido"]
        c_vi = nosso["kg"] * custo_kg["virgem"]
        alto = y0 - y1 + 0.66
        bx.add_patch(Rectangle((c_mo, y1 - 0.33), c_vi - c_mo, alto,
                               facecolor=ELO, alpha=0.13, lw=0, zorder=2))
        bx.plot([preco, preco], [y1 - 0.33, y0 + 0.33], lw=2.2, color=ELO,
                zorder=5)
        bx.text(preco, y0 + 0.44, f"{nosso['nome']}  R$ {vg(preco, 2)}",
                fontsize=8.8, color=ELO, weight="bold", ha="center")

    bx.set_yticks(ypos)
    bx.set_yticklabels(rotulos, fontsize=8.6, color=TINTA)
    bx.tick_params(axis="y", length=0)
    bx.tick_params(axis="x", colors=GRIS, labelsize=8.8)
    bx.set_xlabel("preço de fábrica equivalente (R$/peça)", fontsize=9.5,
                  color=GRIS)
    bx.set_xlim(0, 33)
    bx.set_ylim(y + 0.6, 1.35)
    # loc="left" com o painel comecando em x=0,62 joga o fim do titulo para
    # fora da figura: titulo curto, e o resto explicado na legenda de baixo.
    bx.set_title("A barra é o mercado; a linha, o nosso preço",
                 fontsize=12, color=TINTA, weight="bold", pad=8, loc="left")

    fig.text(0.435, 0.552,
             "Contra a caixa agrícola sobra preço: o M fica 42% abaixo do "
             "teto da de 20 L e o G,\n38% abaixo da de 50 L. Contra o cesto "
             "expositor não sobra: o G fica 14% acima\ndo teto e o M, 21%. "
             "E o P empata no limite, R$ 3,85 contra um teto de R$ 3,88.\n"
             "Onde estamos DENTRO é onde o mercado usa mais plástico do que "
             "nós; onde estamos\nFORA é onde ele usa menos preço — não menos "
             "plástico.\n(A sombra clara é a nossa faixa de custo: moído à "
             "esquerda, virgem à direita.)",
             fontsize=8.7, color=TINTA, va="top", linespacing=1.5)

    # ---- painel C: a tabela, com a fonte de cada linha ------------------
    tb = fig.add_axes([0.050, 0.042, 0.915, 0.438]); tb.axis("off")
    tb.set_xlim(0, 1); tb.set_ylim(0, 1)
    tb.add_patch(Rectangle((0, 0), 1, 1, transform=tb.transAxes,
                           facecolor="#fdfbf7", edgecolor=GRADE, lw=1.3))
    tb.text(0.018, 0.965, "TODA A AMOSTRA, COM A FONTE DE CADA LINHA",
            fontsize=11.5, color=TINTA, weight="bold", va="top")

    cols = [(0.018, "referência", "left"), (0.300, "dim. ext. (cm)", "left"),
            (0.425, "L", "right"), (0.487, "peso", "right"),
            (0.545, "g/L", "right"), (0.625, "vitrine", "right"),
            (0.700, "R$/L fábrica", "right"), (0.812, "fábrica equiv.", "right"),
            (0.830, "fonte", "left")]
    y = 0.905
    for x, t, ha in cols:
        tb.text(x, y, t, fontsize=8.6, color=GRIS, weight="bold",
                ha=ha, va="center")
    y -= 0.048
    tb.plot([0.018, 0.982], [y + 0.018, y + 0.018], color=GRADE, lw=1)

    def escreve(cor, nome, dim, lt, kg, pr, fabrica, fonte, aprox=False,
                peso_bold=False):
        vals = [(0.018, nome, "left"), (0.300, dim, "left"),
                (0.425, lt, "right"), (0.487, kg, "right"),
                (0.545, gl_txt, "right"), (0.625, pr, "right"),
                (0.700, rl_txt, "right"), (0.812, fabrica, "right"),
                (0.830, fonte, "left")]
        # A cor identifica a FAIXA, e quem a carrega e a bolinha, nao a
        # letra: texto colorido some no preto e branco e obriga quem le a
        # distinguir dois tons de nome proprio. O nome fica em tinta.
        tb.plot([0.024], [y], "o", ms=5.5, color=cor, clip_on=False, zorder=4)
        for (x, t, ha) in vals:
            tb.text(x + (0.016 if x < 0.30 else 0), y, t, fontsize=8.5,
                    color=TINTA, ha=ha, va="center",
                    weight="bold" if (x < 0.30 or peso_bold) else "normal")

    for it in linha:
        gl_txt = vg(it["kg"] * 1000 / it["litros"])
        rl_txt = vg(it["kg"] * preco_kg / it["litros"], 2)
        escreve(ELO, it["nome"], "%s × %s × %s" % (
                vg(it["env"][1]), vg(it["env"][2]), vg(it["env"][0])),
                vg(it["litros"], 2), vg(it["kg"] * 1000) + " g",
                "R$ " + vg(it["kg"] * preco_kg, 2), "— (é o nosso)",
                "sólido + ERP", peso_bold=True)
        y -= 0.048
    gl_txt = vg(n047["kg"] * 1000 / n047["litros"])
    rl_txt = vg(n047["fabrica"] / n047["litros"], 2)
    escreve(ELO, "047 Vime 7 L (hoje)", "16,8 × 20,5 × 29,4",
            vg(n047["litros"], 2), vg(n047["kg"] * 1000) + " g",
            "R$ " + vg(n047["fabrica"], 2), "MEDIDO", "ERP (TGFCUS×TGFITE)")
    y -= 0.048
    tb.text(0.018, y, "gôndola do 047, para calibrar o canal:", fontsize=8.5,
            color=GRIS, va="center", style="italic")
    tb.text(0.625, y, f"R$ {vg(n047['varejo'][0], 2)} a "
            f"{vg(n047['varejo'][1], 2)}", fontsize=8.5, color=TINTA,
            ha="right", va="center")
    tb.text(0.830, y, "big lar · nichele · nitron.com.br", fontsize=8.5,
            color=TINTA, va="center")
    y -= 0.062

    for ref, desc, tier, dim, lt, kg, pr, fonte, nota in mercado:
        lt_ = lt if lt else est
        gl_txt = (vg(kg * 1000 / lt_) + ("~" if not lt else "")) if kg else "—"
        lo, hi = pr / k_b2b[1], pr / k_b2b[0]
        rl_txt = vg((lo + hi) / 2 / lt_, 2) + ("~" if not lt else "")
        escreve(TIER[tier], desc.replace("agricola", "agrícola")
                .replace("plastico", "plástico").replace("medio", "médio")
                .replace("Cesto Mini", "Cesto Mini (o gêmeo do P)"),
                "%s × %s × %s" % (vg(dim[0]), vg(dim[1]), vg(dim[2])),
                vg(lt_, 1) + ("~" if not lt else ""),
                (vg(kg * 1000) + " g") if kg else "n/p",
                "R$ " + vg(pr, 2),
                f"R$ {vg(lo, 2)}–{vg(hi, 2)}", fonte)
        y -= 0.048

    y -= 0.014
    tb.plot([0.018, 0.982], [y + 0.020, y + 0.020], color=GRADE, lw=1)
    tb.text(0.018, y - 0.004,
            "(~) a capacidade do cesto bin não é publicada: "
            f"{vg(est, 2)} L saem do envelope dele com o fator de enchimento "
            f"medido no nosso P ({vg(fator, 3)}), que é o número mais "
            "favorável a ele que eu consigo justificar.\n"
            "(n/p) peso não publicado. A ABelt não publica peso, e sem peso "
            "não há comparação por grama — fica só pelo preço.\n"
            "O múltiplo de canal do cesto expositor é PREMISSA: nenhum desses "
            "fabricantes publica preço de fábrica. É a peça que falta, e ela "
            "decide o veredito —\nno canal loja o empate está em "
            "k = 1,40 (G), 1,33 (M) e 1,61 (P). Uma cotação de distribuidor "
            "resolve o que nenhuma busca resolve.",
            fontsize=8.3, color=GRIS, va="top", linespacing=1.55)

    fig.savefig(os.path.join(DEST, "mercado.png"), dpi=112, facecolor=FUNDO)
    print("gerado mercado.png")
