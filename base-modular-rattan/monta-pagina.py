#!/usr/bin/env python3
"""
Monta base-modular.html (ficha + visualizador 3D) a partir de calculo.py e
geometria.py. Nenhum numero da pagina e digitado a mao: tudo sai daqui.

Uso:  python3 monta-pagina.py      (roda gera-3d.py antes, para o malhas.json)
"""
import json, os
import geometria as g
import calculo as c

AQUI = os.path.dirname(os.path.abspath(__file__))
r = c.calcula()
br = c.br
P = r["pecas"]
E = r["encaixe"]
R = r["rigidez"]
K = r["constantes"]
malhas = json.load(open(os.path.join(AQUI, "malhas.json")))
from solidos import perfil_lombada

USD = {"modulo-alto": (30, 36), "modulo-baixo": (26, 32), "tampo": (18, 24)}
INJ = {"modulo-alto": "380 t · INJ 31, 32, 33",
       "modulo-baixo": "380 t · INJ 31, 32, 33",
       "tampo": "600 t · INJ 34 (380 t só com Moldflow)"}
NOME = {"modulo-alto": "Módulo alto", "modulo-baixo": "Módulo baixo", "tampo": "Tampo"}
CESTO_REF = {"modulo-alto": "069.006.003", "modulo-baixo": "261.006.003", "tampo": "fecha a torre"}


# ------------------------------------------------------- corte da lateral ---
def svg_corte():
    """Corte da lateral direita do modulo alto, no meio da profundidade."""
    s = 2.5                          # px por mm, escala UNICA nos dois eixos
    x0, x1, z0, z1 = 112.0, 176.0, -14.0, 234.0
    ox, oy = 40, 24
    W = 640
    H = int((z1 - z0) * s + oy + 40)
    X = lambda x: ox + (x - x0) * s
    Z = lambda z: oy + (z1 - z) * s
    Pa = K["PASSO"]["alto"]
    xt = K["X_TRAV"]
    zj0, zj1 = E["alto"]["janela"]
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Corte da lateral do módulo alto">']

    def rect(xa, xb, za, zb, cls):
        o.append(f'<rect x="{X(xa):.1f}" y="{Z(zb):.1f}" width="{(xb-xa)*s:.1f}" '
                 f'height="{(zb-za)*s:.1f}" class="{cls}"/>')

    # montante atras do plano de corte (tracejado)
    rect(g.X_IN, g.X_EXT, 0, Pa, "atras")
    # cesto, parede esquerda da figura
    o.append(f'<line x1="{X(140):.1f}" y1="{Z(g.PISO_H):.1f}" x2="{X(140):.1f}" '
             f'y2="{Z(g.PISO_H + 190):.1f}" class="cesto"/>')
    # cortado: piso, peitoril, travessa
    rect(x0, g.X_IN, g.PISO_H - g.PISO_PELE, g.PISO_H, "corte")
    rect(g.X_IN, g.X_PEIT, 0, g.PISO_H + g.PEIT_H, "corte")
    zt = Pa - g.TRAV_H["alto"]
    rect(xt, g.X_EXT, Pa - g.TRAV_TOPO, Pa, "corte")
    rect(xt, xt + g.T, zt, Pa, "corte")
    rect(g.X_EXT - g.T, g.X_EXT, zt, Pa, "corte")
    # plano de fechamento macho/cavidade
    o.append(f'<line x1="{X(g.X_PEIT):.1f}" y1="{Z(zj0):.1f}" x2="{X(xt):.1f}" y2="{Z(zj1):.1f}" class="shut"/>')
    # regioes de aco
    o.append(f'<text x="{X(114):.1f}" y="{Z(120):.1f}" class="aco">MACHO</text>')
    o.append(f'<text x="{X(114):.1f}" y="{Z(120)+14:.1f}" class="aco2">sai para cima</text>')
    o.append(f'<path d="M{X(120):.1f},{Z(150):.1f} v-22 m-5,6 l5,-6 l5,6" class="seta"/>')
    o.append(f'<text x="{X(160.5):.1f}" y="{Z(95):.1f}" class="aco" text-anchor="middle">CAV.</text>')
    o.append(f'<path d="M{X(160.5):.1f},{Z(70):.1f} v22 m-5,-6 l5,6 l5,-6" class="seta"/>')
    # chamadas a direita
    lx = X(x1) + 16

    def chamada(xp, zp, texto, sub, zl=None):
        yy = Z(zp)
        yl = Z(zl) if zl is not None else yy
        o.append(f'<polyline points="{X(xp):.1f},{yy:.1f} {lx-18:.1f},{yy:.1f} {lx-4:.1f},{yl:.1f}" class="lider" fill="none"/>')
        o.append(f'<circle cx="{X(xp):.1f}" cy="{yy:.1f}" r="2.2" class="ponto"/>')
        o.append(f'<text x="{lx:.1f}" y="{yl+4:.1f}" class="cham">{texto}</text>')
        o.append(f'<text x="{lx:.1f}" y="{yl+19:.1f}" class="cham2">{sub}</text>')

    chamada(g.X_EXT - 1, Pa - 1.5, "Travessa em U invertido",
            f"x {br(xt)} → {br(g.X_EXT)} · feita pela cavidade")
    chamada((g.X_PEIT + xt) / 2, (zj0 + zj1) / 2, f"Fechamento a {br(E['alto']['shutoff_graus'],1)}°",
            f"recuo de {br(xt - g.X_PEIT)} mm em {br(zj1 - zj0,0)} mm de janela")
    chamada(g.X_PEIT - 1.5, g.PISO_H + g.PEIT_H - 4, "Peitoril",
            f"{br(g.PEIT_T)} mm · sobe {br(g.PEIT_H,0)} mm do piso · feito pelo macho", zl=g.PISO_H + g.PEIT_H + 6)
    chamada(g.X_PEIT + 5, 8, "Rasgo no piso",
            f"x {br(g.X_PEIT)} → {br(g.X_EXT)} · aberto até embaixo", zl=-6)
    chamada(135, g.PISO_H - 1, "Piso", f"topo a {br(g.PISO_H,0)} mm · pele {br(g.PISO_PELE)} + nervura", zl=g.PISO_H + 16)
    # linha de base e topo
    o.append(f'<line x1="{X(x0):.1f}" y1="{Z(0):.1f}" x2="{X(x1):.1f}" y2="{Z(0):.1f}" class="base"/>')
    o.append(f'<line x1="{X(x0):.1f}" y1="{Z(Pa):.1f}" x2="{X(x1):.1f}" y2="{Z(Pa):.1f}" class="base"/>')
    o.append(f'<text x="{X(x0):.1f}" y="{Z(0)-5:.1f}" class="cota">z 0</text>')
    o.append(f'<text x="{X(x0):.1f}" y="{Z(Pa)-6:.1f}" class="cota">z {br(Pa,0)} · plano de apoio do módulo de cima</text>')
    o.append(f'<text x="{X(139):.1f}" y="{Z(g.PISO_H+100):.1f}" class="cesto-t" transform="rotate(-90 {X(139):.1f} {Z(g.PISO_H+100):.1f})" text-anchor="middle">parede do cesto 069</text>')
    o.append("</svg>")
    return "\n".join(o)


# ------------------------------------------------------- perfil da lombada --
def svg_lombada():
    """Corte na frente do modulo, no meio da largura: aba, piso, lombada e o
    pe do cesto. Escala unica nos dois eixos."""
    s = 7.0
    y0, y1, z0, z1 = -8.0, 44.0, -3.0, 44.0
    ox, oy = 20, 20
    W = int((y1 - y0) * s + ox + 250)
    H = int((z1 - z0) * s + oy + 30)
    X = lambda y: ox + (y - y0) * s
    Z = lambda z: oy + (z1 - z) * s
    borda = g.LOMB_W + 1.0 - E["alto"]["recuo_fundo_min"]      # onde encosta a borda do cesto
    fundo = borda + 12.0                                        # suposicao do 3D (medir)
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Perfil da lombada na frente do modulo">']

    def rect(ya, yb, za, zb, cls):
        o.append(f'<rect x="{X(ya):.1f}" y="{Z(zb):.1f}" width="{(yb-ya)*s:.1f}" height="{(zb-za)*s:.1f}" class="{cls}"/>')

    rect(0, g.T + 0.8, 0, g.PISO_H, "corte")
    rect(g.T, y1, g.PISO_H - g.PISO_PELE, g.PISO_H, "corte")
    pf = perfil_lombada(0.0, g.LOMB_W, g.PISO_H, g.LOMB_H, +1)
    o.append('<polygon class="corte" points="' + " ".join(f"{X(u):.1f},{Z(v):.1f}" for u, v in pf) + '"/>')
    # cesto: fundo apoiado, parede subindo ate a borda
    o.append(f'<polyline class="cesto" fill="none" points="{X(y1):.1f},{Z(g.PISO_H):.1f} {X(fundo):.1f},{Z(g.PISO_H):.1f} '
             f'{X(fundo - 3):.1f},{Z(z1 - 2):.1f}"/>')
    o.append(f'<text x="{X(fundo + 2):.1f}" y="{Z(g.PISO_H + 12):.1f}" class="cesto-t">fundo do cesto</text>')
    # cotas
    zc = g.PISO_H + g.LOMB_H
    o.append(f'<line x1="{X(0):.1f}" y1="{Z(zc) - 16:.1f}" x2="{X(g.LOMB_W):.1f}" y2="{Z(zc) - 16:.1f}" class="lider"/>')
    o.append(f'<text x="{X(g.LOMB_W / 2):.1f}" y="{Z(zc) - 21:.1f}" class="cota" text-anchor="middle">{br(g.LOMB_W,0)}</text>')
    o.append(f'<line x1="{X(-4):.1f}" y1="{Z(g.PISO_H):.1f}" x2="{X(-4):.1f}" y2="{Z(zc):.1f}" class="lider"/>')
    o.append(f'<text x="{X(-5):.1f}" y="{Z(g.PISO_H + g.LOMB_H / 2) + 4:.1f}" class="cota" text-anchor="end">{br(g.LOMB_H,0)}</text>')
    o.append(f'<line x1="{X(0):.1f}" y1="{Z(z0):.1f}" x2="{X(0):.1f}" y2="{Z(z1):.1f}" class="base"/>')
    o.append(f'<text x="{X(0) - 4:.1f}" y="{Z(z1) + 12:.1f}" class="cota" text-anchor="end">face</text>')
    # chamadas
    lx = X(y1) + 14
    for yy, zz, tt, ss in ((g.LOMB_W * 0.5, zc - 0.5, "Lombada", f"arco {br(g.LOMB_W,0)} × {br(g.LOMB_H,0)} mm · macho forma"),
                           (fundo + 6, g.PISO_H, "Cesto apoiado", f"sobe {br(g.LOMB_H,0)} mm para sair"),
                           (1.5, 6, "Aba do piso", "viga de frente, 3 mm")):
        o.append(f'<polyline points="{X(yy):.1f},{Z(zz):.1f} {lx - 4:.1f},{Z(zz):.1f}" class="lider" fill="none"/>')
        o.append(f'<circle cx="{X(yy):.1f}" cy="{Z(zz):.1f}" r="2.2" class="ponto"/>')
        o.append(f'<text x="{lx:.1f}" y="{Z(zz) + 4:.1f}" class="cham">{tt}</text>')
        o.append(f'<text x="{lx:.1f}" y="{Z(zz) + 18:.1f}" class="cham2">{ss}</text>')
    o.append(f'<text x="{X(y0) + 2:.1f}" y="{H - 8:.1f}" class="cham2">FRENTE ← · atrás é o espelho</text>')
    o.append("</svg>")
    return "\n".join(o)


# ------------------------------------------------------------ tabelas -------
def linha_peca(n):
    p = P[n]
    return (f"<tr><th>{NOME[n]}</th><td>{CESTO_REF[n]}</td>"
            f"<td class='n'>{br(p['massa_g'],0)} g</td><td class='n'>R$ {br(p['resina_rs'],2)}</td>"
            f"<td class='n'>{br(p['area_proj_cm2'],0)} cm²</td><td class='n'>{br(p['fechamento_t'],0)} t</td>"
            f"<td>{INJ[n]}</td><td class='n'>{br(p['curso_min_mm'],0)} mm</td>"
            f"<td class='n'>{br(p['ciclo_s'],0)} s</td><td class='n'>{br(p['pc_mes']/1000,1)} mil</td>"
            f"<td class='n'>{USD[n][0]}–{USD[n][1]} mil</td></tr>")


def linha_encaixe(m):
    e = E[m]
    return (f"<tr><th>{'Alto' if m=='alto' else 'Baixo'}</th><td>{e['ref']}</td>"
            f"<td class='n'>{br(e['cesto'][0]/10,1)} × {br(e['cesto'][1]/10,1)} × {br(e['cesto'][2]/10,1)} cm</td>"
            f"<td class='n'>{br(e['passo'],0)} mm</td>"
            f"<td class='n'>{br(e['vao_livre'][0],0)} × {br(e['vao_livre'][1],0)} × {br(e['vao_livre'][2],0)}</td>"
            f"<td class='n'>{br(e['folga_lado'],1)}</td><td class='n'>{br(e['folga_prof'],1)}</td>"
            f"<td class='n'>{br(e['folga_topo'],1)}</td>"
            f"<td class='n'>{br(R[m]['flecha_total_mm'],1)} mm</td></tr>")


def linha_torre(t):
    seq = " + ".join(("A" if s == "alto" else "B") for s in t["seq"])
    return (f"<tr><th>{seq} + tampo</th><td class='n'>{br(t['altura_mm'],0)} mm</td>"
            f"<td class='n'>{br(t['massa_g']/1000,2)} kg</td><td class='n'>R$ {br(t['resina_rs'],2)}</td></tr>")


usd_lo = sum(v[0] for v in USD.values())
usd_hi = sum(v[1] for v in USD.values())
dados_js = json.dumps({"malhas": malhas, "K": K,
                       "massa": {n: P[n]["massa_g"] for n in P},
                       "resina": {n: P[n]["resina_rs"] for n in P},
                       "cesto": {m: g.CESTO[m] for m in g.CESTO}},
                      separators=(",", ":"))

tpl = open(os.path.join(AQUI, "pagina.tpl.html"), encoding="utf-8").read()
subs = {
    "{{LARG}}": br(g.LARG, 0), "{{PROF}}": br(g.PROF, 0),
    "{{PASSO_A}}": br(g.PASSO["alto"], 0), "{{PASSO_B}}": br(g.PASSO["baixo"], 0),
    "{{M_A}}": br(P["modulo-alto"]["massa_g"], 0), "{{M_B}}": br(P["modulo-baixo"]["massa_g"], 0),
    "{{M_T}}": br(P["tampo"]["massa_g"], 0),
    "{{RS_KG}}": br(c.RS_KG, 2), "{{SHUT_A}}": br(E["alto"]["shutoff_graus"], 1),
    "{{SHUT_B}}": br(E["baixo"]["shutoff_graus"], 1),
    "{{X_TRAV}}": br(K["X_TRAV"], 1), "{{RECUO}}": br(K["X_TRAV"] - g.X_PEIT, 1),
    "{{FOLGA_TOPO_A}}": br(E["alto"]["folga_topo"], 0), "{{FOLGA_TOPO_B}}": br(E["baixo"]["folga_topo"], 0),
    "{{FLECHA_A}}": br(R["alto"]["flecha_total_mm"], 1), "{{FLECHA_B}}": br(R["baixo"]["flecha_total_mm"], 1),
    "{{E_LONGO}}": br(c.E_LONGO, 0), "{{CARGA_A}}": br(c.CARGA_KG["alto"], 0),
    "{{CARGA_B}}": br(c.CARGA_KG["baixo"], 0),
    "{{MONT_KG}}": br(R["montante"]["carga_acima_kg"], 0),
    "{{MONT_MPA}}": br(R["montante"]["tensao_MPa"], 2),
    "{{MONT_FLAMB}}": br(R["montante"]["fator_flamb"], 0),
    "{{FECH_MOD}}": br(P["modulo-alto"]["fechamento_t"], 0),
    "{{FECH_TAMPO}}": br(P["tampo"]["fechamento_t"], 0),
    "{{AREA_MOD}}": br(P["modulo-alto"]["area_proj_cm2"], 0),
    "{{AREA_TAMPO}}": br(P["tampo"]["area_proj_cm2"], 0),
    "{{USD_LO}}": str(usd_lo), "{{USD_HI}}": str(usd_hi),
    "{{PISO_H}}": br(g.PISO_H, 0),
    "{{LOMB_W}}": br(g.LOMB_W, 0), "{{LOMB_H}}": br(g.LOMB_H, 0),
    "{{RECUO_FUNDO}}": br(E["alto"]["recuo_fundo_min"], 0),
    "{{BORDA_Y}}": br(g.LOMB_W + 1.0 - E["alto"]["recuo_fundo_min"], 0),
    "{{SUBIDA_A}}": br(g.LOMB_H + R["alto"]["flecha_total_mm"], 1),
    "{{SUBIDA_B}}": br(g.LOMB_H + R["baixo"]["flecha_total_mm"], 1),
    "{{R_CANTO}}": br(g.R_CANTO, 0), "{{R_BOCA}}": br(g.R_BOCA, 0),
    "{{R_JANELA}}": br(g.R_JANELA, 0), "{{TAMPO_RF}}": br(g.TAMPO_RF, 0),
    "{{SVG_LOMBADA}}": svg_lombada(),
    "{{TABELA_PECAS}}": "\n".join(linha_peca(n) for n in P),
    "{{TABELA_ENCAIXE}}": "\n".join(linha_encaixe(m) for m in ("alto", "baixo")),
    "{{TABELA_TORRES}}": "\n".join(linha_torre(t) for t in r["torres"]),
    "{{SVG_CORTE}}": svg_corte(),
    "{{DADOS}}": dados_js,
}
for k, v in subs.items():
    tpl = tpl.replace(k, v)
assert "{{" not in tpl, tpl[tpl.index("{{"):tpl.index("{{") + 40]
open(os.path.join(AQUI, "base-modular.html"), "w", encoding="utf-8").write(tpl)
print("base-modular.html", len(tpl) // 1024, "KB")
