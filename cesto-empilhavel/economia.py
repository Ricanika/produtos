#!/usr/bin/env python3
"""
Custo, ferramental e payback do cesto mini organizador empilhavel.

Todas as ancoras vem do ERP (TGFCUS, TGFITE, TGFPRO, AD_MOLDE, AD_ORCAMENTO),
nao de estimativa de catalogo. O peso da peca vem do solido em cad/modelo3d.py.

Uso:  python3 economia.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cad"))

# --- ancoras de produtos comparaveis da casa (12 meses) ---------------------
# ref, descricao, peso kg, custo medio R$, preco medio R$
COMPARAVEIS = [
    ("047/P", "Cesto Organizador Vime 7 L (aberto, liso)", 0.213, 2.141, 4.58),
    ("047/B", "Cesto Organizador Vime 7 L branco",          0.213, 2.141, 4.90),
    ("041/P", "Organizador Multiuso 3 divisorias",          0.118, 1.374, 3.93),
    ("268/P", "Cesto Europa Juta 5,3 L",                    0.260, 4.739, 7.30),
    ("214/P", "Organizador Multiuso 6 divisorias",          0.230, 4.217, 7.25),
    ("256/P", "Cesto Alongado Juta 1,5 L",                  0.100, 2.183, 4.34),
]

# --- resinas (TGFITE compras 12 meses) --------------------------------------
RESINAS = [("PP RP 141 randon fluidez 40", 9.54, 299.1, "recomendada: fluidez p/ parede de 1,4 mm"),
           ("PP CP 141 copolimero",       10.52, 108.9, "alternativa: impacto, se o teste de queda pedir"),
           ("PP H 103 homopolimero",       9.90, 473.2, "nao: fragil em cesto carregado"),
           ("PP moido branco",             7.69, 124.3, "alavanca de custo, se a cor permitir"),
           ("PP moido preto 0055",         6.19, 336.8, "so na versao preta")]

# --- ferramental: analogia direta com os moldes da casa ---------------------
# (AD_MOLDE + AD_ORCAMENTO, ambos MR Plastic Mould, ambos peca unica aberta)
MOLDES_CASA = [
    ("214-U", "Organizador Rattan 6 div", (160, 178, 191), 0.235, 250, 1128, 18900),
    ("284-U", "Cesto Transporta Tudo",    (182, 263, 313), 0.313, 280, 1556, 20100),
]
MOLDE_1CAV = 19500.0      # USD FOB, por analogia (peca entre os dois acima)
MOLDE_2CAV = 34000.0      # USD FOB, ~1,75x o de 1 cavidade
CAMBIO, LANDED = 5.45, 1.30

PRES = 0.32               # t/cm2, valvulado
CANAL = 1.10
CICLO = {1: 22.0, 2: 24.0}   # s, estimado
PARQUE = {200: 12, 250: 9, 280: 1, 300: 1, 380: 3, 600: 1}


def main():
    import modelo3d as M
    p, n_furos = M.cesto()
    peso = p.volume * M.RHO / 1000        # kg
    cap = M.capacidade()
    area = M.LARG * M.PROF / 100.0

    print(f"PECA: {peso*1000:.1f} g | {cap:.2f} L | pe em saia de {M.H_PE:.0f} mm "
          f"| area projetada {area:.0f} cm2 | {n_furos} furos\n")

    print("COMPARAVEIS DA CASA (TGFCUS x TGFITE, 12 meses)")
    print(f"{'ref':7} {'peso':>7} {'custo':>8} {'preco':>8} {'R$/kg cst':>10} "
          f"{'R$/kg prc':>10} {'margem':>7}")
    for ref, _, kg, c, v in COMPARAVEIS:
        print(f"{ref:7} {kg*1000:6.0f}g {c:8.2f} {v:8.2f} {c/kg:10.2f} "
              f"{v/kg:10.2f} {(v-c)/v*100:6.1f}%")
    abertos = [x for x in COMPARAVEIS if x[0].startswith(("047", "268"))]
    print("  cestos abertos e lisos (as duas analogias diretas): custo "
          f"{min(c/kg for _,_,kg,c,_ in abertos):.1f}-{max(c/kg for _,_,kg,c,_ in abertos):.1f}"
          f" e preco {min(v/kg for _,_,kg,_,v in abertos):.1f}-"
          f"{max(v/kg for _,_,kg,_,v in abertos):.1f} R$/kg")

    print("\nRESINA (TGFITE compras 12 meses)")
    for nome, preco, ton, nota in RESINAS:
        print(f"  {nome:30} R$ {preco:5.2f}/kg  {ton:6.1f} t/ano   {nota}")

    print("\nFECHAMENTO (a %.2f t/cm2 + %.0f%% de canal)" % (PRES, (CANAL-1)*100))
    for cav in (1, 2):
        t = area * PRES * CANAL * cav
        cabe = [(ton, q) for ton, q in sorted(PARQUE.items()) if t <= 0.80 * ton]
        ton, q = cabe[0]
        print(f"  {cav} cavidade(s): {t:5.0f} t -> {ton} t ({t/ton*100:.0f}%), "
              f"{q} maquinas dessa classe | ciclo {CICLO[cav]:.0f} s -> "
              f"{3600/CICLO[cav]*cav:.0f} pc/h")

    print("\nCENARIOS DE CUSTO (peso de %.0f g)" % (peso*1000))
    cen = [("virgem RP 141", 15.00, 25.00), ("moido + pigmento", 11.50, 24.00)]
    for nome, ckg, pkg in cen:
        c, v = peso * ckg, peso * pkg
        print(f"  {nome:20} custo R$ {c:5.2f}  preco R$ {v:5.2f}  "
              f"margem {(v-c)/v*100:4.1f}%  contrib R$ {v-c:5.2f}  "
              f"| pack de 10: R$ {v*10:6.2f}")

    print("\nPAYBACK")
    for cav, usd in ((1, MOLDE_1CAV), (2, MOLDE_2CAV)):
        inv = usd * CAMBIO * LANDED
        print(f"  {cav} cav | USD {usd:,.0f} FOB -> R$ {inv:,.0f} nacionalizado")
        for vol in (60000, 150000, 300000):
            for nome, ckg, pkg in cen:
                contrib = peso * (pkg - ckg)
                meses = inv / (vol * contrib) * 12
                horas = vol / (3600 / CICLO[cav] * cav)
                print(f"      {vol:7,} un/ano  {nome:18} contrib R$ "
                      f"{vol*contrib:9,.0f}/ano  payback {meses:5.1f} meses  "
                      f"({horas:5.0f} h de maquina)")


if __name__ == "__main__":
    main()
