#!/usr/bin/env python3
"""
Memoria de calculo da BASE MODULAR Rattan G / Rattan G Baixo.

Le a geometria de geometria.py (a mesma que gera o 3D) e confere, nesta ordem:
  1. o cesto cabe e sai (folgas, batente)
  2. a janela lateral sai do molde sem gaveta (angulo de fechamento)
  3. peso e resina de cada peca, pela UNIAO dos solidos
  4. injetora: area projetada, fechamento, curso de abertura
  5. rigidez: flecha do piso com o cesto cheio, montante sob a torre
  6. torres montadas: altura, peso, custo de resina

Fontes do ERP (Sankhya via MCP Nitron, 23/09/2026):
  TGFPRO   069.006.003 CODPROD 347 e 261.006.003 CODPROD 1854: 38,5 x 28 x
           19,0 / 8,3 cm. Pesos 549 g (corpo 069-C 392 g + tampa 069-T 139 g)
           e 370 g.
  TGFICP   corpo 069-C em PP CP 141 (CODPROD 994) + master 2%.
  TGFITE   PP CP 141: R$ 10,51/kg, 109 t comprados em 12 meses (ult. 17/09/2026).
  TPRAPA   corpo 069-C roda na INJ 33 (380 t, 248 apont.) e INJ 34 (600 t, 221).
  TGFITE   vendas 12 meses: familia 069 65.302 un / R$ 1,45 mi;
           familia 261 19.305 un / R$ 350 mil.
  AD_MOLDE/AD_ORCAMENTO  283-C (corpo lixeira 12 L): molde 72x77x69 cm,
           3.000 kg, 380 t, USD 36.900 aprovado.

Uso:  python3 calculo.py [--json dados.json]
"""
import json, math, sys
import geometria as g

RHO = 0.900e-3              # g/mm3, PP CP 141
RS_KG = 10.51               # R$/kg, media de compra 12 meses
MASTER = 0.02               # 2% de master, mesmo teor do 069-C (nao precificado)
E_CURTO = 1100.0            # MPa, PP copolimero heterofasico
E_LONGO = 400.0             # MPa, modulo de fluencia ~1000 h a 23 C
BAR_CAV = 300.0             # pressao media de cavidade, parede 2,2 e L/t ~120
BAR_CAV_TAMPO = 220.0       # tampo com 2 pontos de camara quente: L/t cai a ~60
MARGEM_FECH = 1.15
CARGA_KG = {"alto": 8.0, "baixo": 4.0}   # conteudo de projeto, alem do cesto
PESO_CESTO_KG = {"alto": 0.549 - 0.139, "baixo": 0.370}  # alto vai sem tampa
CICLO_S = {"modulo-alto": 38.0, "modulo-baixo": 32.0, "tampo": 30.0}  # estimados, sem ficha


def secao_T(bw, hw, bf, hf):
    """I (mm4) de uma secao T: alma bw x hw embaixo, mesa bf x hf em cima."""
    a1, a2 = bw * hw, bf * hf
    y1, y2 = hw / 2, hw + hf / 2
    yc = (a1 * y1 + a2 * y2) / (a1 + a2)
    return (bw * hw ** 3 / 12 + a1 * (y1 - yc) ** 2 +
            bf * hf ** 3 / 12 + a2 * (y2 - yc) ** 2)


def flecha_biapoiada(W_N, L, E, I):
    """Carga W distribuida num vao L simplesmente apoiado."""
    return 5 * W_N * L ** 3 / (384 * E * I)


def calcula():
    r = {"pecas": {}, "encaixe": {}, "rigidez": {}, "torres": []}
    xt = g.x_trav()

    # ---------------------------------------------------- 1. o cesto cabe --
    for m in ("alto", "baixo"):
        c = g.CESTO[m]
        livre_h = g.PASSO[m] - g.PISO_H
        livre_l = 2 * g.X_IN
        livre_p = g.PROF - 2 * (g.T + 0.8)
        z0, z1 = g.janela(m)
        h_jan = z1 - z0
        ang = math.degrees(math.atan((xt - g.X_PEIT) / h_jan))
        r["encaixe"][m] = {
            "ref": c["ref"], "cesto": [c["L"], c["P"], c["H"]],
            "passo": g.PASSO[m], "vao_livre": [livre_l, livre_p, livre_h],
            "folga_topo": livre_h - c["H"], "folga_lado": (livre_l - c["L"]) / 2,
            "folga_prof": livre_p - c["P"],
            "levanta_batente": g.BATENTE_F,
            "janela": [z0, z1], "shutoff_graus": ang,
        }

    # ------------------------------------------------ 3/4. pecas e injetora --
    for nome, f in g.PECAS.items():
        el = f()
        v = g.uniao_volume(el)
        a = g.area_projetada(el)
        massa = v * RHO
        altura = max((e[6] if e[0] == "caixa" else e[4]) for e in el)
        bar = BAR_CAV_TAMPO if nome == "tampo" else BAR_CAV
        fech_t = a / 100 * bar * 1.0197 / 1000 * MARGEM_FECH
        curso = 2 * altura + 60
        ciclo = CICLO_S[nome]
        r["pecas"][nome] = {
            "massa_g": massa, "volume_cm3": v / 1000,
            "resina_rs": massa / 1000 * RS_KG,
            "area_proj_cm2": a / 100, "fechamento_t": fech_t,
            "altura_mm": altura, "curso_min_mm": curso,
            "molde_mm": [g.LARG + 220, g.PROF + 220, altura + 330],
            "ciclo_s": ciclo,
            "pc_mes": 20 * 22 * 3600 / ciclo,   # 1 cavidade, 20 h/dia, 22 dias
            "gavetas": 0, "cavidades": 1,
        }

    # ---------------------------------------------------- 5. rigidez ---------
    # piso: nervuras transversais sob cada barra cheia, vao = entre peitoris
    vao_x = 2 * g.X_IN
    n_nerv = len(g.nervuras_y())
    # mesa efetiva: a barra cheia entre duas fileiras de oblongos
    bf = g.FUROS["passo_y"] - g.FUROS["furo_y"]
    I_nerv = secao_T(g.T_NERV, g.PISO_H - g.PISO_PELE, bf, g.PISO_PELE)
    for m in ("alto", "baixo"):
        W = (CARGA_KG[m] + PESO_CESTO_KG[m]) * 9.81
        w_nerv = W / n_nerv
        f_piso = flecha_biapoiada(w_nerv, vao_x, E_LONGO, I_nerv)
        # peitoril como viga entre montantes, metade da carga de cada lado
        vao_y = g.PROF - 2 * g.MONT_Y
        I_peit = g.PEIT_T * (g.PISO_H + g.PEIT_H) ** 3 / 12
        f_peit = flecha_biapoiada(W / 2, vao_y, E_LONGO, I_peit)
        r["rigidez"][m] = {"carga_N": W, "flecha_piso_mm": f_piso,
                           "flecha_peitoril_mm": f_peit,
                           "flecha_total_mm": f_piso + f_peit,
                           "folga_topo_mm": r["encaixe"][m]["folga_topo"]}

    # montante: torre de 6 altos cheios, carga no de baixo
    mod = r["pecas"]["modulo-alto"]["massa_g"] / 1000
    tam = r["pecas"]["tampo"]["massa_g"] / 1000
    acima = 5 * (mod + PESO_CESTO_KG["alto"] + CARGA_KG["alto"]) + tam
    N_mont = acima * 9.81 / 4
    bx, by, t = g.X_EXT - g.X_IN, g.MONT_Y, g.T
    A = bx * by - (bx - 2 * t) * (by - 2 * t)
    I_min = (by * bx ** 3 - (by - 2 * t) * (bx - 2 * t) ** 3) / 12
    L = g.PASSO["alto"]
    P_cr = math.pi ** 2 * E_LONGO * I_min / (2.0 * L) ** 2   # K=2, engastado-livre
    r["rigidez"]["montante"] = {"carga_acima_kg": acima, "N_por_montante": N_mont,
                                "tensao_MPa": N_mont / A, "P_flamb_N": P_cr,
                                "fator_flamb": P_cr / N_mont}

    # ---------------------------------------------------- 6. torres ----------
    for seq in (["alto"] * 5, ["alto"] * 3 + ["baixo"] * 2, ["baixo"] * 6,
                ["alto"] * 4, ["alto", "baixo", "alto", "baixo"]):
        h = sum(g.PASSO[m] for m in seq) + g.TAMPO_H
        massa = sum(r["pecas"]["modulo-" + m]["massa_g"] for m in seq) + \
            r["pecas"]["tampo"]["massa_g"]
        r["torres"].append({"seq": seq, "altura_mm": h, "massa_g": massa,
                            "resina_rs": massa / 1000 * RS_KG})
    r["constantes"] = {"LARG": g.LARG, "PROF": g.PROF, "X_IN": g.X_IN,
                       "X_PEIT": g.X_PEIT, "X_TRAV": xt, "X_EXT": g.X_EXT,
                       "PISO_H": g.PISO_H, "PEIT_H": g.PEIT_H,
                       "TRAV_H": g.TRAV_H, "PASSO": g.PASSO,
                       "MONT_Y": g.MONT_Y, "T": g.T, "TAMPO_H": g.TAMPO_H,
                       "RS_KG": RS_KG, "E_LONGO": E_LONGO, "BAR_CAV": BAR_CAV,
                       "CARGA_KG": CARGA_KG}
    return r


def br(v, d=1):
    return f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def imprime(r):
    c = r["constantes"]
    print("BASE MODULAR RATTAN G - memoria de calculo\n")
    print(f"Planta unica: {br(c['LARG'])} x {br(c['PROF'])} mm   "
          f"passos: alto {br(c['PASSO']['alto'],0)} / baixo {br(c['PASSO']['baixo'],0)} mm")
    print("\n1. O CESTO CABE E SAI")
    for m, e in r["encaixe"].items():
        print(f"  {m:5s} {e['ref']}: vao livre {br(e['vao_livre'][0])} x "
              f"{br(e['vao_livre'][1])} x {br(e['vao_livre'][2])}  folgas "
              f"lado {br(e['folga_lado'])}/lado  prof {br(e['folga_prof'])}  "
              f"topo {br(e['folga_topo'])}  (levanta {br(e['levanta_batente'])} no batente)")
    print("\n2. JANELA SEM GAVETA")
    for m, e in r["encaixe"].items():
        print(f"  {m:5s} janela z {br(e['janela'][0])} -> {br(e['janela'][1])}  "
              f"fechamento {br(e['shutoff_graus'],1)} graus  "
              f"(peitoril x {br(c['X_PEIT'])}, travessa x {br(c['X_TRAV'])})")
    print("\n3/4. PECAS, RESINA E INJETORA  (PP CP 141 a R$ %s/kg)" % br(c["RS_KG"], 2))
    for n, p in r["pecas"].items():
        print(f"  {n:13s} {br(p['massa_g'],0):>5s} g  R$ {br(p['resina_rs'],2)}  "
              f"A.proj {br(p['area_proj_cm2'],0)} cm2  fech {br(p['fechamento_t'],0)} t  "
              f"curso >= {br(p['curso_min_mm'],0)} mm  molde ~{'x'.join(br(v,0) for v in p['molde_mm'])} mm  "
              f"{br(p['pc_mes'],0)} pc/mes")
    print("\n5. RIGIDEZ (modulo de fluencia %s MPa)" % br(c["E_LONGO"], 0))
    for m in ("alto", "baixo"):
        k = r["rigidez"][m]
        print(f"  {m:5s} carga {br(k['carga_N'],0)} N: piso {br(k['flecha_piso_mm'],2)} + "
              f"peitoril {br(k['flecha_peitoril_mm'],2)} = {br(k['flecha_total_mm'],2)} mm "
              f"(folga de topo {br(k['folga_topo_mm'])})")
    k = r["rigidez"]["montante"]
    print(f"  montante do modulo de baixo, torre de 6 altos cheios: {br(k['carga_acima_kg'])} kg acima, "
          f"{br(k['N_por_montante'],0)} N/montante, {br(k['tensao_MPa'],2)} MPa, "
          f"flambagem x{br(k['fator_flamb'],0)}")
    print("\n6. TORRES")
    for t in r["torres"]:
        print(f"  {'+'.join(s[0].upper() for s in t['seq']):12s} altura {br(t['altura_mm'],0)} mm  "
              f"{br(t['massa_g']/1000,2)} kg  resina R$ {br(t['resina_rs'],2)}")


if __name__ == "__main__":
    r = calcula()
    imprime(r)
    if "--json" in sys.argv:
        with open(sys.argv[sys.argv.index("--json") + 1], "w") as f:
            json.dump(r, f, indent=1, ensure_ascii=False)
