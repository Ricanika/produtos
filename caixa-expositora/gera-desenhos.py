#!/usr/bin/env python3
"""
Gera os desenhos tecnicos da caixa expositora (SVG, cotas em mm, escala 1:1).

  faca-expositora.svg  - planificacao completa com vincos, cortes e picote
  arranjos.svg         - vista superior do arranjo de cada kit na camada
  conversao.svg        - as 3 etapas: caixa fechada -> destaque -> expositor

As cores usam var(--x, #fallback): abrem corretas num navegador (fallback) e
assumem o tema quando o SVG e embutido numa pagina que define os tokens.
"""
import math

# ------------------------------------------------------ parametros da caixa
ESP = 7                 # onda BC (mm)
FI, PI, HI = 560, 530, 720          # internas
PF, PL = FI + ESP, PI + ESP         # painel frente/tras, painel lateral
ABA_COLA = 40
AI_LAT = PF / 2 - 2      # aba inferior das laterais (se encontram na frente)
AI_FT = PL / 2 - 2       # aba inferior frente/tras (se encontram na profund.)
AS_FT = PL / 2 - 2       # aba superior frente/tras
AS_LAT = 100             # aba superior lateral = aro de travamento

H_FRENTE = 240           # altura da frente que fica (retem o produto)
FLECHA = 40              # rebaixo do arco no centro
RECUO = 15               # quanto o picote entra na lateral

CUT = 'var(--cut,#16181A)'
VINCO = 'var(--vinco,#2F6FA8)'
PICOTE = 'var(--picote,#D2451E)'
FILL = 'var(--board,#EFECE4)'
MUT = 'var(--mut,#6B7280)'
BG = 'var(--figbg,#FFFFFF)'
FAM = "var(--figmono, ui-monospace)"


STYLE = ('<style>text{font-family:var(--figmono),ui-monospace,SFMono-Regular,'
         'Menlo,Consolas,monospace}</style>')


def svg(w, h, body, pad=0):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {w+2*pad} {h+2*pad}" '
            f'role="img" style="max-width:100%;height:auto">\n{STYLE}\n'
            f'<rect x="{-pad}" y="{-pad}" width="{w+2*pad}" height="{h+2*pad}" fill="{BG}"/>\n'
            f'{body}\n</svg>\n')


def txt(x, y, s, size=17, anchor="middle", color=CUT, weight=500, rot=None):
    t = f' transform="rotate({rot},{x},{y})"' if rot else ''
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}"{t}>{s}</text>\n')


def cota(x1, y1, x2, y2, label, off=0, side=1, size=15):
    """Linha de cota simples com setas."""
    o = []
    if y1 == y2:
        y = y1 + off
        o.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{MUT}" stroke-width="1.2"/>')
        for x, d in ((x1, 1), (x2, -1)):
            o.append(f'<path d="M{x} {y} l{7*d} -4 v8 z" fill="{MUT}"/>')
        o.append(txt((x1 + x2) / 2, y - 7, label, size, color=MUT))
    else:
        x = x1 + off
        o.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{MUT}" stroke-width="1.2"/>')
        for y, d in ((y1, 1), (y2, -1)):
            o.append(f'<path d="M{x} {y} l-4 {7*d} h8 z" fill="{MUT}"/>')
        o.append(txt(x - 8, (y1 + y2) / 2, label, size, anchor="middle", color=MUT,
                     rot=-90))
    return "".join(o)


# ============================================================ 1) PLANIFICACAO
def faca():
    # eixo x: aba de cola | TRAS | LAT D | FRENTE | LAT E
    xs = [0]
    for w in (ABA_COLA, PF, PL, PF, PL):
        xs.append(xs[-1] + w)
    X_COLA, X_TRAS, X_LATD, X_FRENTE, X_LATE, X_END = xs
    # eixo y (0 = topo da chapa)
    Y_TOP = 0
    Y_VTOP = AS_FT                      # vinco superior do corpo
    Y_VBOT = Y_VTOP + HI                # vinco inferior do corpo
    Y_BOT = Y_VBOT + AI_LAT             # borda inferior (abas laterais)
    Y_BOT_FT = Y_VBOT + AI_FT
    Y_TOP_LAT = Y_VTOP - AS_LAT
    W, H = X_END, Y_BOT
    o = []

    def rect(x, y, w, h, fill=FILL, stroke=CUT, sw=2.2):
        o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    # corpo (4 paineis + aba de cola)
    rect(X_COLA, Y_VTOP, W, HI)
    # abas
    for x0, w in ((X_TRAS, PF), (X_FRENTE, PF)):                     # frente/tras
        rect(x0 + 2, Y_TOP, w - 4, AS_FT)
        rect(x0 + 2, Y_VBOT, w - 4, AI_FT)
    for x0, w in ((X_LATD, PL), (X_LATE, PL)):                        # laterais
        rect(x0 + 2, Y_TOP_LAT, w - 4, AS_LAT)
        rect(x0 + 2, Y_VBOT, w - 4, AI_LAT)

    # vincos
    vinc = []
    for x in (X_TRAS, X_LATD, X_FRENTE, X_LATE):
        vinc.append(f'M{x} {Y_VTOP} V{Y_VBOT}')
    vinc.append(f'M{X_COLA} {Y_VTOP} H{X_END}')
    vinc.append(f'M{X_COLA} {Y_VBOT} H{X_END}')
    o.append(f'<path d="{" ".join(vinc)}" stroke="{VINCO}" stroke-width="2" '
             f'stroke-dasharray="14 7" fill="none"/>')

    # ---- picote
    yh = Y_VBOT - H_FRENTE                 # linha do picote nas extremidades
    ya = yh + FLECHA                       # ponto mais baixo do arco (centro)
    R = ((PF / 2) ** 2 + FLECHA ** 2) / (2 * FLECHA)
    xL, xR = X_FRENTE, X_LATE              # quinas da frente
    p = (f'M{xL-RECUO} {yh} H{xL} '
         f'A{R:.0f} {R:.0f} 0 0 0 {xR} {yh} '
         f'H{xR+RECUO} V{Y_VTOP} H{xR} '
         f'M{xL-RECUO} {yh} V{Y_VTOP} H{xL}')
    o.append(f'<path d="{p}" stroke="{PICOTE}" stroke-width="3.4" fill="none" '
             f'stroke-dasharray="26 9"/>')
    # dedeira (corte real) no centro, no painel que FICA
    o.append(f'<path d="M{(xL+xR)/2-17.5} {ya} a17.5 17.5 0 0 0 35 0" fill="none" '
             f'stroke="{CUT}" stroke-width="2.2"/>')
    # hachura do painel destacavel
    o.append(f'<path d="M{xL} {yh+4} A{R:.0f} {R:.0f} 0 0 0 {xR} {yh+4} L{xR} {Y_VTOP} '
             f'L{xL} {Y_VTOP} Z" fill="{PICOTE}" opacity="0.10"/>')
    o.append(f'<path d="M{xL+2} {Y_TOP} h{PF-4} v{AS_FT} h{-(PF-4)} z" fill="{PICOTE}" opacity="0.10"/>')

    # fendas do cartaz promocional na testeira (aba superior traseira)
    for dx in (170, 397):
        o.append(f'<rect x="{X_TRAS+dx:.0f}" y="{Y_TOP+70}" width="60" height="4" '
                 f'rx="2" fill="{CUT}"/>')

    # ---- rotulos
    lbl = [(X_COLA, ABA_COLA, "ABA<tspan x='0'>COLA</tspan>"), (X_TRAS, PF, "TRASEIRA"),
           (X_LATD, PL, "LATERAL"), (X_FRENTE, PF, "FRENTE"), (X_LATE, PL, "LATERAL")]
    for x0, w, name in lbl:
        if name.startswith("ABA"):
            o.append(txt(x0 + w / 2, (Y_VTOP + Y_VBOT) / 2, "ABA DE COLA", 16,
                         color=MUT, rot=-90))
        else:
            o.append(txt(x0 + w / 2, (Y_VTOP + Y_VBOT) / 2 + 200, name, 28, weight=700))
    o.append(txt((X_FRENTE + X_LATE) / 2, (Y_VTOP + Y_VBOT) / 2 + 245,
                 "painel destacavel", 17, color=PICOTE))
    o.append(txt((X_TRAS + X_LATD) / 2, Y_TOP + 150, "TESTEIRA  (dobra 180 para cima)", 18,
                 color=CUT, weight=700))
    for x0, w in ((X_LATD, PL), (X_LATE, PL)):
        o.append(txt(x0 + w / 2, Y_TOP_LAT + 62, "aro de travamento", 16, color=MUT))
    for x0, w in ((X_TRAS, PF), (X_FRENTE, PF), (X_LATD, PL), (X_LATE, PL)):
        o.append(txt(x0 + w / 2, Y_VBOT + 150, "fundo", 16, color=MUT))

    # ---- cotas
    o.append(cota(X_TRAS, Y_BOT, X_LATD, Y_BOT, f"{PF:.0f}", off=62))
    o.append(cota(X_LATD, Y_BOT, X_FRENTE, Y_BOT, f"{PL:.0f}", off=62))
    o.append(cota(X_FRENTE, Y_BOT, X_LATE, Y_BOT, f"{PF:.0f}", off=62))
    o.append(cota(X_LATE, Y_BOT, X_END, Y_BOT, f"{PL:.0f}", off=62))
    o.append(cota(0, Y_BOT, W, Y_BOT, f"chapa {W:.0f} mm", off=118, size=19))
    o.append(cota(X_END, Y_VTOP, X_END, Y_VBOT, f"{HI}", off=58))
    o.append(cota(X_END, Y_TOP, X_END, Y_VTOP, f"{AS_FT:.0f}", off=58))
    o.append(cota(X_END, Y_VBOT, X_END, Y_BOT, f"{AI_LAT:.0f}", off=58))
    o.append(cota(X_END, Y_TOP, X_END, Y_BOT, f"chapa {H:.0f} mm", off=118, size=19))
    o.append(cota(X_FRENTE, Y_VBOT, X_FRENTE, yh, f"{H_FRENTE}", off=-52))
    o.append(f'<line x1="{(xL+xR)/2+120}" y1="{ya}" x2="{(xL+xR)/2+250}" y2="{ya+72}" '
             f'stroke="{PICOTE}" stroke-width="1.2"/>')
    o.append(txt((xL + xR) / 2 + 258, ya + 78, f"flecha {FLECHA} / R{R:.0f}", 17,
                 anchor="start", color=PICOTE))
    o.append(f'<line x1="{(xL+xR)/2}" y1="{ya+18}" x2="{(xL+xR)/2-190}" y2="{ya+110}" '
             f'stroke="{CUT}" stroke-width="1.2"/>')
    o.append(txt((xL + xR) / 2 - 198, ya + 116, "dedeira D35 (corte)", 17, anchor="end"))

    # legenda
    ly = Y_BOT + 190
    leg = [(CUT, "corte (faca)", "none"), (VINCO, "vinco", "14 7"), (PICOTE, "picote ziper", "26 9")]
    for i, (c, s, dash) in enumerate(leg):
        x = 40 + i * 560
        o.append(f'<line x1="{x}" y1="{ly}" x2="{x+90}" y2="{ly}" stroke="{c}" '
                 f'stroke-width="3.4" stroke-dasharray="{dash}"/>')
        o.append(txt(x + 108, ly + 7, s, 20, anchor="start", color=MUT))
    o.append(txt(W, ly + 7, "cotas em mm - escala 1:1 - onda BC 7 mm - canaletas VERTICAIS",
                 20, anchor="end", color=MUT))
    return svg(W, ly + 40, "\n".join(o), pad=140)


# ================================================== 2) ARRANJO POR CAMADA
def arranjos():
    F, P = 560, 530
    dados = [("Kit quadrado", 255, 235, 2, 2, "4 por camada - 6 camadas - 24 kits"),
             ("Kit ret. alto", 180, 260, 3, 2, "6 por camada - 5 camadas - 30 kits"),
             ("Kit ret. baixo", 180, 260, 3, 2, "6 por camada - 8 camadas - 48 kits")]
    o, gap, sc = [], 190, 1.0
    for i, (nome, a, b, nx, ny, cap) in enumerate(dados):
        ox = i * (F + gap)
        o.append(f'<rect x="{ox}" y="80" width="{F}" height="{P}" fill="none" '
                 f'stroke="{CUT}" stroke-width="3"/>')
        for r in range(nx):
            for c in range(ny):
                o.append(f'<rect x="{ox+r*a+3}" y="{80+c*b+3}" width="{a-6}" height="{b-6}" '
                         f'fill="{PICOTE}" fill-opacity="0.14" stroke="{PICOTE}" stroke-width="2" rx="6"/>')
                o.append(txt(ox + r * a + a / 2, 80 + c * b + b / 2 + 7, f"{a/10:g}x{b/10:g}", 20, color=PICOTE))
        # folgas
        o.append(f'<rect x="{ox+nx*a}" y="80" width="{F-nx*a}" height="{P}" fill="{MUT}" opacity="0.12"/>')
        o.append(f'<rect x="{ox}" y="{80+ny*b}" width="{nx*a}" height="{P-ny*b}" fill="{MUT}" opacity="0.12"/>')
        o.append(txt(ox + F / 2, 0, nome.upper(), 30, weight=700))
        o.append(txt(ox + F / 2, P + 138, cap, 23, color=MUT))
        o.append(txt(ox + F / 2, P + 176,
                     f"folga {(F-nx*a)/10:g} cm x {(P-ny*b)/10:g} cm", 21, color=MUT))
        o.append(cota(ox, 80, ox + F, 80, "560 (frente)", off=-26, size=21))
        o.append(cota(ox + F, 80, ox + F, 80 + P, "530", off=30, size=21))
    return svg(3 * F + 2 * gap, P + 210, "\n".join(o), pad=90)


# ================================================== 3) CONVERSAO EM 3 ETAPAS
def conversao():
    W, D, H = 560, 530, 720
    k, TH = 0.32, 250
    kD, TOP = k * D, H + TH
    FW, FH = W + kD, TOP + kD          # caixa util da figura
    GAP = 360
    HF, ZK, NK = 240, 105, 6           # frente que fica / altura do kit / camadas

    def P(x, y, z, ox=0.0):
        return (ox + x + k * y, TOP + kD - z - k * y)

    def face(pts, fill, op=1.0, stroke=CUT, sw=2.4):
        d = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
        return (f'<polygon points="{d}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" '
                f'stroke-width="{sw}" stroke-linejoin="round"/>')

    o, legendas = [], ["1 - caixa fechada, no transporte",
                       "2 - destaca a frente pelo picote",
                       "3 - dobra a testeira: expositor pronto"]
    for i in range(3):
        ox = i * (FW + GAP)
        g = []
        # traseira + testeira (quando aberta)
        g.append(face([P(0, D, 0, ox), P(W, D, 0, ox), P(W, D, H, ox), P(0, D, H, ox)], FILL, 0.45))
        if i:
            g.append(face([P(0, D, H, ox), P(W, D, H, ox), P(W, D, TOP, ox), P(0, D, TOP, ox)],
                          FILL, 0.95))
            g.append(txt(*[c + d for c, d in zip(P(W / 2, D, H + TH / 2, ox), (0, 10))],
                         "TESTEIRA", 32, weight=700, color=MUT))
        # lateral direita
        g.append(face([P(W, 0, 0, ox), P(W, D, 0, ox), P(W, D, H, ox), P(W, 0, H, ox)], FILL, 0.78))
        if i == 0:
            # tampa fechada + frente inteira
            g.append(face([P(0, 0, H, ox), P(W, 0, H, ox), P(W, D, H, ox), P(0, D, H, ox)], FILL, 0.55))
            g.append(face([P(0, 0, 0, ox), P(W, 0, 0, ox), P(W, 0, H, ox), P(0, 0, H, ox)], FILL))
            a, b = P(0, 0, HF, ox), P(W, 0, HF, ox)
            c, d = P(0, 0, H, ox), P(W, 0, H, ox)
            g.append(f'<path d="M{a[0]:.0f} {a[1]:.0f} H{b[0]:.0f} M{a[0]:.0f} {a[1]:.0f} '
                     f'V{c[1]:.0f} M{b[0]:.0f} {b[1]:.0f} V{d[1]:.0f}" stroke="{PICOTE}" '
                     f'stroke-width="4.5" stroke-dasharray="22 9" fill="none"/>')
            g.append(txt(*[v + dd for v, dd in zip(P(W / 2, 0, 470, ox), (0, 0))],
                         "linha de picote", 28, color=PICOTE))
        else:
            # pilha de kits
            for n in range(NK):
                z = n * ZK
                g.append(face([P(35, 35, z, ox), P(W - 35, 35, z, ox),
                               P(W - 35, 35, z + ZK - 8, ox), P(35, 35, z + ZK - 8, ox)],
                              PICOTE, 0.16, MUT, 1.5))
            g.append(face([P(35, 35, NK * ZK - 8, ox), P(W - 35, 35, NK * ZK - 8, ox),
                           P(W - 35, D - 35, NK * ZK - 8, ox), P(35, D - 35, NK * ZK - 8, ox)],
                          PICOTE, 0.10, MUT, 1.5))
            # aro de travamento: abas superiores laterais dobradas para dentro
            for x0 in (0, W - 100):
                g.append(face([P(x0, 0, H, ox), P(x0 + 100, 0, H, ox),
                               P(x0 + 100, D, H, ox), P(x0, D, H, ox)], FILL, 0.72, MUT, 1.6))
            # frente remanescente
            g.append(face([P(0, 0, 0, ox), P(W, 0, 0, ox), P(W, 0, HF, ox), P(0, 0, HF, ox)], FILL))
            g.append(txt(*[c + d for c, d in zip(P(W / 2, 0, HF / 2, ox), (0, 10))],
                         "240", 26, color=MUT))
            if i == 1:
                gx, gy, gw = ox - 340, 30, 430
                gh = gw * (H - HF) / W
                arc = gw * FLECHA / W
                g.append(f'<path d="M{gx} {gy} h{gw} v{gh:.0f} q{-gw/2:.0f} {arc*2:.0f} '
                         f'{-gw:.0f} 0 z" fill="{PICOTE}" fill-opacity="0.14" stroke="{PICOTE}" '
                         f'stroke-width="3.4" stroke-dasharray="20 8"/>')
                g.append(txt(gx + gw / 2, gy + gh / 2 + 10, "painel destacado", 27, color=PICOTE))
                p1 = P(W / 2 - 60, 0, H - 60, ox)
                g.append(f'<path d="M{p1[0]:.0f} {p1[1]:.0f} Q{p1[0]-120:.0f} '
                         f'{p1[1]-230:.0f} {gx+gw+16:.0f} {gy+gh*0.55:.0f}" stroke="{PICOTE}" '
                         f'stroke-width="5" fill="none" marker-end="url(#ar)"/>')
        o.append("".join(g))
        o.append(txt(ox + FW / 2, FH + 92, legendas[i], 28, color=MUT))
    defs = (f'<defs><marker id="ar" markerWidth="11" markerHeight="11" refX="8" refY="5.5" '
            f'orient="auto"><path d="M0 0 L11 5.5 L0 11 z" fill="{PICOTE}"/></marker></defs>')
    return svg(3 * FW + 2 * GAP, FH + 130, defs + "\n".join(o), pad=120)


if __name__ == "__main__":
    import pathlib
    base = pathlib.Path(__file__).parent
    for nome, fn in (("faca-expositora", faca), ("arranjos", arranjos), ("conversao", conversao)):
        (base / f"{nome}.svg").write_text(fn(), encoding="utf-8")
        print(f"gerado: {nome}.svg")
