#!/usr/bin/env python3
"""
Monta base-modular.html (ficha + visualizador 3D) a partir de calculo.py e
geometria.py. Nenhum numero da pagina e digitado a mao: tudo sai daqui.

Uso:  python3 monta-pagina.py      (roda gera-3d.py antes para o pecas.json)
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
pecas = json.load(open(os.path.join(AQUI, "pecas.json")))

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
dados_js = json.dumps({"pecas": pecas, "K": K,
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
    "{{PISO_H}}": br(g.PISO_H, 0), "{{BATENTE}}": br(g.BATENTE_F, 0),
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
