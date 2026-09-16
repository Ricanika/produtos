#!/usr/bin/env python3
"""
Memoria de calculo da linha de cestos organizadores dobraveis empilhaveis.

Fonte unica: importa a geometria de cad/modelo3d.py e le PESO e AREA do solido
real, em vez de reestimar por area de parede. A versao anterior deste arquivo
mantinha sua propria estimativa em paralelo ao 3D -- e foi exatamente essa
duplicacao que produziu o erro de contar a saia do fundo duas vezes.

Uso:  python3 calculo-dobravel.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cad"))
import modelo3d as M                                            # noqa: E402

# --- premissas de processo --------------------------------------------------
PRES_FRIO   = 0.40        # t/cm2 - canal frio, peca plana de parede fina
PRES_VALVUL = 0.32        # t/cm2 - camara quente com bico valvulado sequencial
CANAL       = 1.10        # acrescimo de canal no fechamento
USO_MAX     = 0.80        # fracao maxima do fechamento da maquina

# parque confirmado (TPRWCP + TPRCAP, 16/09/2026)
PARQUE = [(120, "13-17, 44, 45"), (150, "42, 43"), (160, "7-12, 36, 40, 41"),
          (200, "1-6, 19-22, 35, 37"), (250, "23-28, 38, 39, 46"), (280, "29"),
          (300, "30"), (380, "31, 32, 33"), (600, "34")]

# --- premissas comerciais ---------------------------------------------------
CUSTO_KG = 19.50          # R$/kg de peca acabada (TGFCUS x TGFPRO, faixa 14,0-21,7)
PRECO_KG = 36.00          # R$/kg de preco de venda (TGFITE 12 m, faixa 31,7-45,0)
RESINA_KG = 10.52         # R$/kg - PP CP 141 copolimero (CODPROD 994)
CUBAGEM = 300.0           # kg/m3 - fator de cubagem rodoviaria
PALLET = (1200.0, 1000.0, 1800.0)

# --- ferramental ------------------------------------------------------------
ACO_KG_DM3 = 7.85
USD_KG     = 14.00        # media dos 3 moldes comparaveis (AD_MOLDE/AD_ORCAMENTO)
CAMARA     = 11000.0      # camara quente 4 bicos valvulados, no fundo
INSERTO    = 6500.0       # jogo de inserto de altura -- carrega as proprias
                          # filas de pinos de furo, nao e so bloco de shut-off
MOLDES = [("fundo 1 cav",    (620, 540, 520), True,  0),
          ("lateral 2 cav",  (700, 460, 460), False, 2),
          ("traseira 2 cav", (700, 460, 460), False, 2),
          ("frontal 2 cav",  (700, 420, 400), False, 2)]


def area_furos(larg, alt):
    """Area total dos furos de um painel, em cm2."""
    n_col = len(M.colunas(larg))
    return sum(n_col * math.pi / 4 * d ** 2 for _, d in M.filas(alt)) / 100.0


def dados(tam):
    pecas, _, h_ext, alt, h_front = M.modelo(tam)
    _, _, vol, vol_util = M.cavidade(h_ext, h_front)
    peso = sum(n * m.volume * M.RHO for m, n, _ in pecas.values())
    furos = sum(n * nf for _, n, nf in pecas.values())
    pesos = {k: v[0].volume * M.RHO for k, v in pecas.items()}
    return dict(tam=tam, h_ext=h_ext, alt=alt, h_front=h_front, vol=vol,
                vol_util=vol_util, peso=peso, furos=furos, pesos=pesos)


def aloca(rot, area_cm2, cavs, pres=PRES_VALVUL):
    for cav in cavs:
        t = area_cm2 * pres * CANAL * cav
        for ton, maqs in PARQUE:
            if t <= USO_MAX * ton:
                return (f"{rot:16} {cav} cav {t:6.0f} t -> {ton:4.0f} t "
                        f"({t/ton*100:2.0f}%)  INJ {maqs}")
    return f"{rot:16} nao cabe no parque"


def main():
    L = [dados(t) for t in ("P", "M", "G")]

    print("GEOMETRIA  (footprint comum %.0f x %.0f mm, modulo %.0f mm, "
          "dobrado %.0f mm)" % (M.EXT_C, M.EXT_L, M.MODULO, M.H_PE + M.H_SAIA + 2))
    print(f"{'':4} {'alt.ext':>8} {'painel':>8} {'frontal':>8} {'nominal':>9} "
          f"{'util':>8} {'peso':>8} {'furos':>7}")
    for r in L:
        print(f"{r['tam']:4} {r['h_ext']:7.0f}mm {r['alt']:7.0f}mm {r['h_front']:7.0f}mm "
              f"{r['vol']:7.2f} L {r['vol_util']:6.2f} L {r['peso']:6.1f} g {r['furos']:7}")

    print("\nPESO POR PECA (g)")
    print(f"{'':4} {'fundo':>8} {'lateral':>8} {'x2':>8} {'traseira':>9} "
          f"{'frontal':>8} {'total':>8}")
    for r in L:
        p = r['pesos']
        print(f"{r['tam']:4} {p['fundo']:8.1f} {p['lateral']:8.1f} "
              f"{2*p['lateral']:8.1f} {p['traseira']:9.1f} {p['frontal']:8.1f} "
              f"{r['peso']:8.1f}")

    print("\nCOMBINACOES EMPILHADAS (passo = altura externa, multiplo de "
          f"{M.MODULO:.0f} mm)")
    h = {r['tam']: r['h_ext'] for r in L}
    for combo in (("P", "P"), ("P", "M"), ("M", "M"), ("P", "P", "P"), ("G", "G")):
        tot = sum(h[c] for c in combo)
        igual = [k for k, v in h.items() if v == tot]
        print(f"  {'+'.join(combo):10} {tot:5.0f} mm = {tot/M.MODULO:.0f} modulos"
              f"{'  = ' + igual[0] if igual else ''}")

    print("\nALOCACAO DE MAQUINA (valvulado, limite de %.0f%% do fechamento)"
          % (USO_MAX * 100))
    a_fundo = M.EXT_C * M.EXT_L / 100.0
    print(" ", aloca("fundo (comum)", a_fundo, [1]))
    for r in L:
        for rot, larg in (("lateral", M.LARG_CURTO), ("traseira", M.LARG_LONGO)):
            bruta = larg * r['alt'] / 100.0
            print(" ", aloca(f"{rot} {r['tam']}", bruta - area_furos(larg, r['alt']),
                             [2, 1]))
        print(" ", aloca(f"frontal {r['tam']}",
                         M.LARG_LONGO * r['h_front'] / 100.0, [2, 1]))

    print(f"\nCUBAGEM E FRETE (fator {CUBAGEM:.0f} kg/m3, pallet PBR "
          f"{PALLET[0]:.0f}x{PALLET[1]:.0f} com {PALLET[2]:.0f} mm uteis)")
    h_dob = M.H_PE + M.H_SAIA + 2
    por_camada = int(PALLET[0] // M.EXT_C) * int(PALLET[1] // M.EXT_L)
    print(f"{'':4} {'montado':>10} {'cubado':>8} {'dobrado':>10} {'cubado':>8} "
          f"{'frete':>7} {'pallet mont':>12} {'pallet dob':>11} {'ganho':>7}")
    for r in L:
        v_m = M.EXT_C * M.EXT_L * r['h_ext'] / 1e9
        v_d = M.EXT_C * M.EXT_L * h_dob / 1e9
        pc_m = max(v_m * CUBAGEM, r['peso'] / 1000)
        pc_d = max(v_d * CUBAGEM, r['peso'] / 1000)
        n_m = por_camada * int(PALLET[2] // r['h_ext'])
        n_d = por_camada * int(PALLET[2] // h_dob)
        print(f"{r['tam']:4} {v_m*1000:7.2f} dm3 {pc_m:6.2f}kg {v_d*1000:7.2f} dm3 "
              f"{pc_d:6.2f}kg {pc_m/pc_d:6.1f}x {n_m:12} {n_d:11} {n_d/n_m:6.1f}x")

    print(f"\nCUSTO E PRECO (custo R$ {CUSTO_KG:.2f}/kg, preco R$ {PRECO_KG:.2f}/kg, "
          f"resina R$ {RESINA_KG:.2f}/kg)")
    print(f"{'':4} {'resina':>8} {'custo':>8} {'preco':>8} {'margem':>8} "
          f"{'R$/L':>7} {'contrib':>8}")
    tc = tp = 0.0
    for r in L:
        kg = r['peso'] / 1000
        c, p = kg * CUSTO_KG, kg * PRECO_KG
        tc += c
        tp += p
        print(f"{r['tam']:4} {kg*RESINA_KG:7.2f} {c:8.2f} {p:8.2f} "
              f"{(p-c)/p*100:7.1f}% {p/r['vol']:6.2f} {p-c:8.2f}")
    print(f"kit  {'':8} {tc:8.2f} {tp:8.2f} {(tp-tc)/tp*100:7.1f}% "
          f"{'':7} {tp-tc:8.2f}")

    print(f"\nFERRAMENTAL (FOB USD, a {USD_KG:.0f} USD/kg de bloco)")
    total = 0.0
    for rot, (c, l, a), camara, ins in MOLDES:
        kg = c * l * a / 1e6 * ACO_KG_DM3
        v = kg * USD_KG + (CAMARA if camara else 0) + ins * INSERTO
        total += v
        extra = [x for x in ("camara quente valvulada" if camara else "",
                             f"{ins} jogos de inserto" if ins else "") if x]
        print(f"  {rot:16} bloco {c}x{l}x{a} {kg:6.0f} kg  USD {v:9,.0f}"
              f"   {', '.join(extra)}")
    print(f"  {'TOTAL FOB':16} {'':34} USD {total:9,.0f}")

    cambio, landed, un_ano = 5.45, 1.30, 21500
    contrib = sum((r['peso'] / 1000) * (PRECO_KG - CUSTO_KG) for r in L)
    invest = total * cambio * landed
    print(f"\nPAYBACK (premissa: R$ {cambio:.2f}/USD, nacionalizacao "
          f"+{(landed-1)*100:.0f}%, {un_ano:,} un/ano por tamanho)")
    print(f"  investimento nacionalizado  R$ {invest:12,.0f}")
    print(f"  contribuicao por kit        R$ {contrib:12,.2f}")
    print(f"  contribuicao anual          R$ {un_ano*contrib:12,.0f}")
    print(f"  payback                     {invest/(un_ano*contrib)*12:12.1f} meses")


if __name__ == "__main__":
    main()
