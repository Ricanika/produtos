#!/usr/bin/env python3
"""
Desenhos tecnicos da caixa expositora SORTIDA (wrap com testeira articulada).

  faca-expositora.svg  - planificacao do wrap: FUNDO | FRENTE | TOPO | TRAS
  arranjo.svg          - vista superior das 3 colunas + vista frontal das pilhas
  conversao.svg        - as 4 etapas ate o expositor montado

Cores em var(--x, #fallback): abrem corretas no navegador e assumem o tema
quando o SVG e embutido numa pagina que define os tokens.
"""
import math

ESP = 5
W, D, H = 780, 580, 900              # internas
PW = W + ESP                          # largura do painel na chapa
PD, PH = D + ESP, H + ESP
ABA_COLA = 80
ABA_LAT = D / 2 + 25                  # 315 - sobrepoem 50 mm no meio da lateral
ABA_TOPO_LAT = 60                     # aba de cola do topo
FRENTE_FICA = 240
RECUO = 15                            # picote entra 15 mm no painel
DEDEIRA = 35

CUT = 'var(--cut,#14171A)'
VINCO = 'var(--vinco,#2C6A9E)'
REV = 'var(--rev,#1E8A6E)'            # vinco reverso
PICOTE = 'var(--picote,#BC3C19)'
FILL = 'var(--board,#ECE8DE)'
MUT = 'var(--mut,#5F686D)'
BG = 'var(--figbg,#FFFFFF)'
STYLE = ('<style>text{font-family:var(--figmono, ui-monospace),SFMono-Regular,'
         'Menlo,Consolas,monospace}</style>')


def svg(w, h, body, pad=0):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} '
            f'{w+2*pad} {h+2*pad}" role="img">\n{STYLE}\n'
            f'<rect x="{-pad}" y="{-pad}" width="{w+2*pad}" height="{h+2*pad}" fill="{BG}"/>\n'
            f'{body}\n</svg>\n')


def txt(x, y, s, size=20, anchor="middle", color=CUT, weight=500, rot=None):
    t = f' transform="rotate({rot},{x:.1f},{y:.1f})"' if rot else ''
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}"{t}>{s}</text>\n')


def rect(x, y, w, h, fill=FILL, stroke=CUT, sw=2.4, op=1.0):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" '
            f'fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>\n')


def cota(x1, y1, x2, y2, label, off=0, size=19, color=MUT):
    o = []
    if y1 == y2:
        y = y1 + off
        o.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" '
                 f'stroke="{color}" stroke-width="1.3"/>')
        for x, d in ((x1, 1), (x2, -1)):
            o.append(f'<path d="M{x:.1f} {y:.1f} l{8*d} -4.5 v9 z" fill="{color}"/>')
        o.append(txt((x1 + x2) / 2, y - 9, label, size, color=color))
    else:
        x = x1 + off
        o.append(f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2:.1f}" '
                 f'stroke="{color}" stroke-width="1.3"/>')
        for y, d in ((y1, 1), (y2, -1)):
            o.append(f'<path d="M{x:.1f} {y:.1f} l-4.5 {8*d} h9 z" fill="{color}"/>')
        o.append(txt(x - 10, (y1 + y2) / 2, label, size, color=color, rot=-90))
    return "".join(o)


# ======================================================== 1) FACA (wrap)
def faca():
    xs = [0]
    for w in (PD, PH, PD, PH, ABA_COLA):
        xs.append(xs[-1] + w)
    X_FUN, X_FRE, X_TOP, X_TRA, X_ABA, X_END = xs
    y0 = 0
    y1 = ABA_LAT
    y2 = y1 + PW
    y3 = y2 + ABA_LAT
    o = []

    # paineis do corpo
    o.append(rect(0, y1, X_END, PW))
    # abas laterais grandes (fundo, frente, tras)
    for x0, w in ((X_FUN, PD), (X_FRE, PH), (X_TRA, PH)):
        o.append(rect(x0 + 2, y0, w - 4, ABA_LAT))
        o.append(rect(x0 + 2, y2, w - 4, ABA_LAT))
    # abas de cola do topo (60 mm)
    o.append(rect(X_TOP + 2, y1 - ABA_TOPO_LAT, PD - 4, ABA_TOPO_LAT, op=0.55))
    o.append(rect(X_TOP + 2, y2, PD - 4, ABA_TOPO_LAT, op=0.55))

    # vincos
    v = [f'M{X_FRE} {y1} V{y2}', f'M{X_TRA} {y1} V{y2}', f'M{X_ABA} {y1} V{y2}',
         f'M0 {y1} H{X_END}', f'M0 {y2} H{X_END}']
    o.append(f'<path d="{" ".join(v)}" stroke="{VINCO}" stroke-width="2.2" '
             f'stroke-dasharray="16 8" fill="none"/>')
    # vinco reverso FRENTE/TOPO
    o.append(f'<path d="M{X_TOP} {y1-ABA_TOPO_LAT} V{y2+ABA_TOPO_LAT}" stroke="{REV}" '
             f'stroke-width="3.4" stroke-dasharray="26 7 5 7" fill="none"/>')

    # ---- picote em U
    xp = X_FRE + FRENTE_FICA
    ya, yb = y1 + RECUO, y2 - RECUO
    o.append(f'<path d="M{X_TRA} {ya} H{xp} V{yb} H{X_TRA}" stroke="{PICOTE}" '
             f'stroke-width="3.8" stroke-dasharray="28 10" fill="none"/>')
    o.append(f'<rect x="{xp}" y="{ya}" width="{X_TRA-xp}" height="{yb-ya}" '
             f'fill="{PICOTE}" opacity="0.10"/>')
    # dedeira (corte real) no painel que fica
    ym = (ya + yb) / 2
    o.append(f'<path d="M{xp} {ym-DEDEIRA/2} a{DEDEIRA/2} {DEDEIRA/2} 0 0 1 0 {DEDEIRA}" '
             f'fill="none" stroke="{CUT}" stroke-width="2.4"/>')
    o.append(f'<line x1="{xp-6}" y1="{ym}" x2="{xp-150}" y2="{ym+150}" stroke="{CUT}" stroke-width="1.3"/>')
    o.append(txt(xp - 158, ym + 158, f"dedeira D{DEDEIRA} (corte real)", 19, anchor="end"))

    # ---- rotulos
    nomes = [(X_FUN, PD, "FUNDO"), (X_FRE, PH, "FRENTE"), (X_TOP, PD, "TOPO"),
             (X_TRA, PH, "TRASEIRA")]
    for x0, w, n in nomes:
        o.append(txt(x0 + w / 2, y1 + PW / 2 - 40, n, 40, weight=700))
    o.append(txt(X_ABA + ABA_COLA / 2, y1 + PW / 2, "ABA DE COLA", 19, color=MUT, rot=-90))
    o.append(txt((X_FRE + xp) / 2, y1 + PW / 2 + 20, "muro de retencao", 21, color=MUT))
    o.append(txt((xp + X_TOP) / 2, y1 + PW / 2 + 20, "vira a FACE da testeira", 21, color=PICOTE))
    o.append(txt((X_TOP + X_TRA) / 2, y1 + PW / 2 + 20, "vira o DORSO da testeira", 21, color=PICOTE))
    for x0, w in ((X_FUN, PD), (X_FRE, PH), (X_TRA, PH)):
        for yy in (y0 + ABA_LAT * 0.28, y2 + ABA_LAT * 0.72):
            lbl = "parede lateral" if x0 != X_FUN else "reforco (cola por dentro)"
            o.append(txt(x0 + w / 2, yy + 7, lbl, 19, color=MUT))
    for yy in (y1 - ABA_TOPO_LAT / 2, y2 + ABA_TOPO_LAT / 2):
        o.append(txt(X_TOP + PD / 2, yy + 6, f"aba de cola do topo {ABA_TOPO_LAT} - o picote a libera",
                     17, color=MUT))

    # ---- cotas
    for x0, w in ((X_FUN, PD), (X_FRE, PH), (X_TOP, PD), (X_TRA, PH), (X_ABA, ABA_COLA)):
        o.append(cota(x0, y3, x0 + w, y3, f"{w:.0f}", off=70))
    o.append(cota(0, y3, X_END, y3, f"chapa {X_END:.0f} mm", off=140, size=24))
    o.append(cota(X_END, y0, X_END, y1, f"{ABA_LAT:.0f}", off=62))
    o.append(cota(X_END, y1, X_END, y2, f"{PW:.0f}", off=62))
    o.append(cota(X_END, y2, X_END, y3, f"{ABA_LAT:.0f}", off=62))
    o.append(cota(X_END, y0, X_END, y3, f"chapa {y3:.0f} mm", off=140, size=24))
    o.append(cota(X_FRE, y1, xp, y1, f"{FRENTE_FICA}  muro", off=-62, color=PICOTE))
    o.append(cota(xp, y1, X_TOP, y1, f"{X_TOP-xp:.0f}  face da testeira", off=-130, color=PICOTE))
    o.append(cota(X_TOP, y1, X_TRA, y1, f"{PD:.0f}  dorso", off=-130, color=PICOTE))
    o.append(txt(X_TRA + 34, y1 + PW + 205,
                 "a peca NAO sai: fica articulada neste vinco",
                 25, anchor="start", color=PICOTE, weight=700))
    o.append(f'<path d="M{X_TRA} {y1+PW+212} l0 -110 m0 110 l-16 -22 m16 22 l16 -22" '
             f'stroke="{PICOTE}" stroke-width="3.4" fill="none"/>')

    # legenda
    ly = y3 + 240
    leg = [(CUT, "corte (faca)", "none"), (VINCO, "vinco", "16 8"),
           (REV, "vinco REVERSO", "26 7 5 7"), (PICOTE, "picote ziper", "28 10")]
    for i, (c, s, dash) in enumerate(leg):
        x = i * 560
        o.append(f'<line x1="{x}" y1="{ly}" x2="{x+95}" y2="{ly}" stroke="{c}" '
                 f'stroke-width="3.8" stroke-dasharray="{dash}"/>')
        o.append(txt(x + 115, ly + 8, s, 23, anchor="start", color=MUT))
    o.append(txt(X_END, ly + 8, "cotas em mm - onda C 5 mm - canaletas VERTICAIS no corpo",
                 23, anchor="end", color=MUT))
    return svg(X_END, ly + 50, "".join(o), pad=180)


# ======================================================== 2) ARRANJO
def arranjo():
    COLS = [("A", "KIT QUADRADO", 235, 255, 105, 2, 8, 0),
            ("B", "KIT RET. ALTO", 260, 180, 140, 3, 6, 0),
            ("C", "KIT RET. BAIXO", 260, 180, 80, 3, 10, 40)]
    DIV = 3
    NIVEL = 840
    o = []
    # ---------- vista superior
    ox, oy = 0, 60
    o.append(rect(ox, oy, W, D, fill="none", sw=3))
    x = ox
    for i, (k, nome, fr, pf, h, nd, cam, cal) in enumerate(COLS):
        for j in range(nd):
            o.append(rect(x + 3, oy + j * pf + 3, fr - 6, pf - 6, fill=PICOTE,
                          op=0.14, stroke=PICOTE, sw=2))
            o.append(txt(x + fr / 2, oy + j * pf + pf / 2 + 8, f"{fr}x{pf}", 22, color=PICOTE))
        o.append(txt(x + fr / 2, oy - 16, f"COLUNA {k}", 26, weight=700))
        o.append(cota(x, oy + D, x + fr, oy + D, f"{fr}", off=48))
        x += fr
        if i < 2:
            o.append(rect(x, oy, DIV + 6, D, fill=MUT, stroke=MUT, sw=1, op=0.55))
            x += DIV
    o.append(cota(ox, oy, ox + W, oy, f"frente interna {W}", off=-70, size=24))
    o.append(cota(ox + W, oy, ox + W, oy + D, f"prof. {D}", off=112, size=24))
    o.append(txt(ox + W / 2, oy + D + 130, "VISTA SUPERIOR - uma coluna por kit, tres facings",
                 26, color=MUT))

    # ---------- vista frontal
    ox2 = W + 320
    o.append(rect(ox2, oy, W, H, fill="none", sw=3))
    x = ox2
    for i, (k, nome, fr, pf, h, nd, cam, cal) in enumerate(COLS):
        base = oy + H
        if cal:
            o.append(rect(x + 2, base - cal, fr - 4, cal, fill=MUT, op=0.30, stroke=MUT, sw=1.6))
            o.append(txt(x + fr / 2, base - cal / 2 + 7, f"calco {cal}", 19, color=MUT))
        for j in range(cam):
            yy = base - cal - (j + 1) * h
            o.append(rect(x + 2, yy + 2, fr - 4, h - 4, fill=PICOTE, op=0.14,
                          stroke=PICOTE, sw=1.8))
        o.append(txt(x + fr / 2, oy - 16, f"{cam} x {nd} = {cam*nd} kits", 24, weight=700))
        x += fr + (DIV if i < 2 else 0)
    ytop = oy + H - NIVEL
    o.append(f'<path d="M{ox2-40} {ytop} H{ox2+W+50}" stroke="{CUT}" stroke-width="2.6" '
             f'stroke-dasharray="18 9"/>')
    o.append(txt(ox2 + W + 58, ytop + 8, f"carga nivelada em {NIVEL}", 24, anchor="start"))
    ymuro = oy + H - FRENTE_FICA
    o.append(f'<path d="M{ox2} {ymuro} H{ox2+W}" stroke="{PICOTE}" stroke-width="3.4" '
             f'stroke-dasharray="26 10"/>')
    o.append(txt(ox2 - 20, ymuro + 8, f"picote {FRENTE_FICA}", 24, anchor="end", color=PICOTE))
    o.append(cota(ox2 + W, oy, ox2 + W, oy + H, f"altura interna {H}", off=200, size=24))
    o.append(txt(ox2 + W / 2, oy + H + 130,
                 "VISTA FRONTAL - o calco de 40 nivela o kit baixo com os outros dois",
                 26, color=MUT))
    return svg(ox2 + W + 420, oy + H + 170, "".join(o), pad=150)


# ======================================================== 3) CONVERSAO
def conversao():
    k, TH = 0.30, D                      # testeira tem a altura da profundidade
    kD = k * D
    TOP = H + TH
    FW, FH = W + kD, TOP + kD
    GAP = 300
    HF = FRENTE_FICA
    FACE = H - HF                        # 660 - a parte alta da frente

    def P(x, y, z, ox=0.0):
        return (ox + x + k * y, TOP + kD - z - k * y)

    def face(pts, fill, op=1.0, stroke=CUT, sw=2.6):
        d = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
        return (f'<polygon points="{d}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" '
                f'stroke-width="{sw}" stroke-linejoin="round"/>')

    def corpo(ox, com_frente_alta):
        g = [face([P(0, D, 0, ox), P(W, D, 0, ox), P(W, D, H, ox), P(0, D, H, ox)], FILL, 0.45),
             face([P(W, 0, 0, ox), P(W, D, 0, ox), P(W, D, H, ox), P(W, 0, H, ox)], FILL, 0.8)]
        if not com_frente_alta:
            for n, z0, zk in ((8, 0, 105), (6, 0, 140), (10, 0, 80)):
                pass
            for col, (x0, x1, zk, nc) in enumerate(((0, 240, 105, 8), (243, 508, 140, 6),
                                                    (511, 776, 80, 10))):
                cal = 40 if col == 2 else 0
                for j in range(nc):
                    z = cal + j * zk
                    g.append(face([P(x0 + 10, 40, z, ox), P(x1 - 10, 40, z, ox),
                                   P(x1 - 10, 40, z + zk - 6, ox), P(x0 + 10, 40, z + zk - 6, ox)],
                                  PICOTE, 0.15, MUT, 1.3))
            g.append(face([P(0, 0, 0, ox), P(W, 0, 0, ox), P(W, 0, HF, ox), P(0, 0, HF, ox)], FILL))
            g.append(txt(*[c + d for c, d in zip(P(W / 2, 0, HF / 2, ox), (0, 10))],
                         str(HF), 26, color=MUT))
        return g

    o, legendas = [], [
        "1 - fechada: picote em U na frente",
        "2 - rasga o U - a peca NAO sai",
        "3 - o topo gira 90 e fica em pe",
        "4 - a frente dobra 180 sobre ele"]

    for i in range(4):
        ox = i * (FW + GAP)
        g = []
        if i == 0:
            g += corpo(ox, True)
            g.append(face([P(0, 0, H, ox), P(W, 0, H, ox), P(W, D, H, ox), P(0, D, H, ox)], FILL, 0.55))
            g.append(face([P(0, 0, 0, ox), P(W, 0, 0, ox), P(W, 0, H, ox), P(0, 0, H, ox)], FILL))
            a, b = P(20, 0, HF, ox), P(W - 20, 0, HF, ox)
            c, d = P(20, 0, H, ox), P(W - 20, 0, H, ox)
            g.append(f'<path d="M{c[0]:.0f} {c[1]:.0f} L{a[0]:.0f} {a[1]:.0f} '
                     f'L{b[0]:.0f} {b[1]:.0f} L{d[0]:.0f} {d[1]:.0f}" stroke="{PICOTE}" '
                     f'stroke-width="5" stroke-dasharray="24 10" fill="none"/>')
            g.append(txt(*P(W / 2, 0, HF + 230, ox), "picote em U", 30, color=PICOTE))
        elif i == 1:
            g += corpo(ox, False)
            # peca solta, ainda presa atras, erguida ~25 graus
            ang = math.radians(28)
            def Q(t, s):   # t ao longo da peca a partir da dobra em (y=D, z=H)
                return P(s, D - t * math.cos(ang), H + t * math.sin(ang), ox)
            g.append(face([Q(0, 0), Q(0, W), Q(D, W), Q(D, 0)], PICOTE, 0.14, PICOTE, 3))
            g.append(txt(*[c + dd for c, dd in zip(Q(D / 2, W / 2), (0, 10))],
                         "topo", 26, color=PICOTE))
            p1 = P(W / 2, 0, H + 40, ox)
            p2 = Q(D + 90, W / 2)
            g.append(f'<path d="M{p1[0]:.0f} {p1[1]:.0f} Q{(p1[0]+p2[0])/2+180:.0f} '
                     f'{min(p1[1],p2[1])-40:.0f} {p2[0]:.0f} {p2[1]:.0f}" stroke="{PICOTE}" '
                     f'stroke-width="5" fill="none" marker-end="url(#ar)"/>')
        else:
            g += corpo(ox, False)
            # testeira em pe (o TOPO)
            g.append(face([P(0, D, H, ox), P(W, D, H, ox), P(W, D, TOP, ox), P(0, D, TOP, ox)],
                          FILL, 0.95))
            if i == 2:
                g.append(txt(*[c + d for c, d in zip(P(W / 2, D, H + TH * 0.3, ox), (0, 10))],
                             "dorso", 28, weight=700, color=MUT))
                # frente alta ainda horizontal, apontando para a frente
                g.append(face([P(0, D, TOP, ox), P(W, D, TOP, ox),
                               P(W, D - FACE, TOP, ox), P(0, D - FACE, TOP, ox)],
                              PICOTE, 0.14, PICOTE, 3))
                g.append(txt(*[c + d for c, d in zip(P(W / 2, D - FACE / 2, TOP, ox), (0, 10))],
                             "face", 26, color=PICOTE))
                p1 = P(W / 2, D - FACE, TOP + 40, ox)
                p2 = P(W / 2, D - 40, H + TH / 2, ox)
                g.append(f'<path d="M{p1[0]:.0f} {p1[1]:.0f} Q{p1[0]-200:.0f} '
                         f'{(p1[1]+p2[1])/2:.0f} {p2[0]:.0f} {p2[1]:.0f}" stroke="{PICOTE}" '
                         f'stroke-width="5" fill="none" marker-end="url(#ar)"/>')
            else:
                # face dobrada sobre o dorso, descendo 80 mm por dentro
                g.append(face([P(0, D - 6, TOP, ox), P(W, D - 6, TOP, ox),
                               P(W, D - 6, TOP - FACE, ox), P(0, D - 6, TOP - FACE, ox)],
                              PICOTE, 0.16, PICOTE, 3))
                g.append(txt(*[c + d for c, d in zip(P(W / 2, D - 6, TOP - FACE / 2 + 60, ox), (0, 10))],
                             "TESTEIRA", 34, weight=700, color=PICOTE))
                g.append(txt(*[c + d for c, d in zip(P(W / 2, D - 6, TOP - FACE / 2 - 40, ox), (0, 10))],
                             "parede dupla", 24, color=PICOTE))
                g.append(cota(*P(W + 30, D, TOP, ox), *P(W + 30, D, H, ox), f"{D}", off=54))
                p1 = P(W / 2, D - 6, TOP - FACE - 10, ox)
                g.append(txt(p1[0], p1[1] + 34, f"aba de {FACE-D:.0f} mm desce por dentro e trava",
                             22, color=MUT))
        o.append("".join(g))
        o.append(txt(ox + FW / 2, FH + 100, legendas[i], 28, color=MUT))
    defs = (f'<defs><marker id="ar" markerWidth="11" markerHeight="11" refX="8" refY="5.5" '
            f'orient="auto"><path d="M0 0 L11 5.5 L0 11 z" fill="{PICOTE}"/></marker></defs>')
    return svg(4 * FW + 3 * GAP - GAP + 200, FH + 150, defs + "".join(o), pad=140)


if __name__ == "__main__":
    import pathlib
    base = pathlib.Path(__file__).parent
    for nome, fn in (("faca-expositora", faca), ("arranjo", arranjo), ("conversao", conversao)):
        (base / f"{nome}.svg").write_text(fn(), encoding="utf-8")
        print(f"gerado: {nome}.svg")
