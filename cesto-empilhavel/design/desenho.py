#!/usr/bin/env python3
"""Desenho vetorial dos conceitos B2C -- silhuetas, nao renders.

Sao croquis 2D de PROPORCAO CERTA: a silhueta sai das cotas reais do P
(boca 180, altura 130, saida 6 graus, envelope 204 com a aba), entao o que
a folha mostra e a peca de hoje com cada gesto aplicado em cima. Nenhum
destes desenhos e um solido -- o 3D so vem depois da escolha.
"""

MM = 1.12                     # px por mm
LARG, PROF, ALT = 180.0, 230.0, 130.0
ABA, ENV = 12.0, 204.0        # aba livre e envelope em x
TAN6 = 0.10510
BASE = LARG - 2 * ALT * TAN6  # 152,7 mm

CX, TOPO = 132.0, 34.0
H = ALT * MM
Y_BASE = TOPO + H


def x(mm_do_eixo):
    return CX + mm_do_eixo * MM


def frente(rasgos=None, extras="", pes=True, aba=True, plinto=False,
           boca=LARG, base=BASE, altura=ALT):
    """Vista frontal generica: aba, corpo com saida, pes."""
    hb = altura * MM
    yb = TOPO + hb
    p = []
    if aba:
        p.append(f'<path class="ln" d="M{x(-ENV/2):.1f} {TOPO:.1f} '
                 f'h{ENV*MM:.1f} v6 h-4 v-4 h-{(ENV-8)*MM/1:.1f} v4 h-4 z"/>')
    p.append(f'<path class="corpo" d="M{x(-boca/2):.1f} {TOPO+6:.1f} '
             f'L{x(boca/2):.1f} {TOPO+6:.1f} '
             f'L{x(base/2):.1f} {yb-10:.1f} '
             f'Q{x(base/2):.1f} {yb:.1f} {x(base/2-9):.1f} {yb:.1f} '
             f'L{x(-base/2+9):.1f} {yb:.1f} '
             f'Q{x(-base/2):.1f} {yb:.1f} {x(-base/2):.1f} {yb-10:.1f} Z"/>')
    if plinto:
        p.append(f'<path class="ln" d="M{x(-base/2+14):.1f} {yb:.1f} '
                 f'v7 h{(base-28)*MM:.1f} v-7"/>')
        p.append(f'<line class="sombra" x1="{x(-base/2+16):.1f}" '
                 f'y1="{yb+8:.1f}" x2="{x(base/2-16):.1f}" y2="{yb+8:.1f}"/>')
    elif pes:
        for s in (-1, 1):
            p.append(f'<path class="ln" d="M{x(s*(base/2-18)):.1f} {yb:.1f} '
                     f'v6 h{-s*22:.1f} v-6"/>')
    if rasgos:
        p.append(rasgos)
    return "".join(p) + extras


def listras(n=13, w=6.0, h=18.0, faixas=3, r=2.5):
    """O vazado de hoje: 3 faixas de listra curta, 13 colunas."""
    out = []
    passo = LARG / (n + 1)
    for f in range(faixas):
        y0 = TOPO + 26 + f * (h * MM + 9)
        for i in range(n):
            xm = -LARG / 2 + passo * (i + 1)
            enc = (1 - (y0 - TOPO) / H * 0.21)
            out.append(f'<rect class="furo" x="{x(xm*enc)-w*MM/2:.1f}" '
                       f'y="{y0:.1f}" width="{w*MM:.1f}" '
                       f'height="{h*MM:.1f}" rx="{r:.1f}"/>')
    return "".join(out)


def ripas(n=9, w=9.0, r=5.0, y0=26, y1=26):
    """Ripa vertical continua, ponta arredondada: uma so por coluna."""
    out = []
    passo = LARG / (n + 1)
    for i in range(n):
        xm = -LARG / 2 + passo * (i + 1)
        a, b = TOPO + y0, Y_BASE - y1
        enc = 1 - 0.10
        out.append(f'<rect class="furo" x="{x(xm*enc)-w*MM/2:.1f}" y="{a:.1f}" '
                   f'width="{w*MM:.1f}" height="{b-a:.1f}" rx="{w*MM/2:.1f}"/>')
    return "".join(out)


def canelado(n=21):
    """Nervura em relevo: linha, nao furo."""
    out = []
    passo = LARG / (n + 1)
    for i in range(n):
        xm = -LARG / 2 + passo * (i + 1)
        out.append(f'<line class="canel" x1="{x(xm):.1f}" y1="{TOPO+13:.1f}" '
                   f'x2="{x(xm*0.86):.1f}" y2="{Y_BASE-4:.1f}"/>')
    return "".join(out)


def arco(larg=122.0, sobe=26.0, alt=62.0, fleche=30.0):
    """Recorte em arco na frente: alca, acesso e assinatura, tudo junto.

    Laterais retas, topo em meia-elipse -- arco de verdade. Desenhado como
    caixa de canto arredondado ele volta a ler como rasgo, que e justamente
    o que este conceito quer eliminar.
    """
    yb = Y_BASE - sobe * MM
    ya = yb - alt * MM
    ys = ya + fleche * MM
    rx, ry = larg * MM / 2, fleche * MM
    return (f'<path class="furo" d="M{x(-larg/2):.1f} {yb:.1f} '
            f'L{x(-larg/2):.1f} {ys:.1f} '
            f'A{rx:.1f} {ry:.1f} 0 0 1 {x(larg/2):.1f} {ys:.1f} '
            f'L{x(larg/2):.1f} {yb:.1f} Z"/>')


def pega_oval(w=74.0, h=20.0, desce=30.0):
    y0 = TOPO + desce
    return (f'<rect class="furo" x="{x(-w/2):.1f}" y="{y0:.1f}" '
            f'width="{w*MM:.1f}" height="{h*MM:.1f}" rx="{h*MM/2:.1f}"/>')


def meia_pele(n=13, w=6.0, h=18.0):
    out = []
    passo = LARG / (n + 1)
    for f in range(2):
        y0 = TOPO + 74 + f * (h * MM + 9)
        for i in range(n):
            xm = -LARG / 2 + passo * (i + 1)
            out.append(f'<rect class="furo" x="{x(xm*0.9)-w*MM/2:.1f}" '
                       f'y="{y0:.1f}" width="{w*MM:.1f}" '
                       f'height="{h*MM:.1f}" rx="2.5"/>')
    return "".join(out)


def planta(raio=28.0, aba=True, oval=False, escala=0.62):
    """Vista de planta: a boca com o raio de canto que o conceito propoe."""
    w, d = LARG * MM * escala, PROF * MM * escala
    r = raio * MM * escala
    cx, cy = 100.0, 96.0
    out = []
    if aba:
        ew, ed = (LARG + 2 * ABA) * MM * escala, (PROF + 2 * ABA) * MM * escala
        out.append(f'<rect class="ln" x="{cx-ew/2:.1f}" y="{cy-ed/2:.1f}" '
                   f'width="{ew:.1f}" height="{ed:.1f}" '
                   f'rx="{r+ABA*MM*escala:.1f}"/>')
    rr = min(w, d) / 2 if oval else r
    out.append(f'<rect class="corpo" x="{cx-w/2:.1f}" y="{cy-d/2:.1f}" '
               f'width="{w:.1f}" height="{d:.1f}" rx="{rr:.1f}"/>')
    out.append(f'<rect class="ln tenue" x="{cx-w/2+7:.1f}" '
               f'y="{cy-d/2+7:.1f}" width="{w-14:.1f}" height="{d-14:.1f}" '
               f'rx="{max(rr-7, 2):.1f}"/>')
    return "".join(out)


def corte_borda():
    """A borda em CORTE, as duas lado a lado: a aba de hoje e a virada.

    Uma secao sozinha nao se le -- e o contraste entre as duas que mostra o
    que o conceito faz. Legenda debaixo de cada uma, dentro da caixa.
    """
    o = []
    # hoje: parede + aba reta para fora, com a dobrinha de 5 mm
    o.append('<path class="corpo" d="M34 158 L34 52 L86 52 L86 76 L78 76 '
             'L78 60 L44 60 L44 158 Z"/>')
    o.append('<text class="cota" x="40" y="174">hoje</text>')
    # proposta: a borda vira para baixo e forma um U; o engate mora dentro
    o.append('<path class="corpo" d="M120 158 L120 64 Q120 50 134 50 '
             'L154 50 Q170 50 170 66 L170 96 Q170 104 162 104 '
             'Q154 104 154 96 L154 70 Q154 64 148 64 L130 64 L130 158 Z"/>')
    o.append('<path class="ln" d="M137 72 L146 72 L146 80"/>')
    o.append('<text class="cota" x="126" y="174">proposta</text>')
    o.append('<text class="cota" x="16" y="190">o engate passa a morar dentro '
             'da borda</text>')
    return "".join(o)


def junta(s=0.62):
    """Duas pecas empilhadas: a linha de junta vira sombra, e a torre e o
    produto. Desenho proprio, em escala menor -- duas pecas no passo real
    (130 mm) nao cabem na mesma caixa de desenho da vista frontal."""
    w, b_, h = LARG * MM * s / 2, BASE * MM * s / 2, ALT * MM * s
    cx = CX
    o = []
    for topo in (110.0, 18.0):
        o.append(f'<path class="corpo" d="M{cx-w:.1f} {topo:.1f} '
                 f'L{cx+w:.1f} {topo:.1f} L{cx+b_:.1f} {topo+h-6:.1f} '
                 f'Q{cx+b_:.1f} {topo+h:.1f} {cx+b_-7:.1f} {topo+h:.1f} '
                 f'L{cx-b_+7:.1f} {topo+h:.1f} '
                 f'Q{cx-b_:.1f} {topo+h:.1f} {cx-b_:.1f} {topo+h-6:.1f} Z"/>')
        o.append(f'<line class="ln" x1="{cx-w-8:.1f}" y1="{topo:.1f}" '
                 f'x2="{cx+w+8:.1f}" y2="{topo:.1f}"/>')
    o.append(f'<line class="sombra forte" x1="{cx-b_+4:.1f}" y1="112.5" '
             f'x2="{cx+b_-4:.1f}" y2="112.5"/>')
    return "".join(o)


def textura(n=140):
    """Pontilhado leve: le-se como superficie fosca, nao como furo."""
    import random
    rnd = random.Random(7)
    o = []
    for _ in range(n):
        yy = rnd.uniform(TOPO + 16, Y_BASE - 10)
        f = 1 - (yy - TOPO) / H * 0.20
        xx = rnd.uniform(-LARG / 2 + 8, LARG / 2 - 8) * f
        o.append(f'<circle class="tex" cx="{x(xx):.1f}" cy="{yy:.1f}" r="1"/>')
    return "".join(o)
