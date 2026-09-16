#!/usr/bin/env python3
"""
Memoria de calculo da caixa expositora de papelao ondulado para os 3 kits.

CONCEITO
  Caixa de transporte que vira expositor no ponto de venda: picote na frente
  subindo ate o topo, destaca-se o painel frontal inteiro (com a aba superior
  da frente junto) e dobra-se a aba superior traseira 180 graus para cima,
  virando a TESTEIRA com a arte da marca.

  Estrutura: caixa de 1 peca, emenda colada, abas superiores DESIGUAIS.
    - abas inferiores: fundo total (as duas camadas se encontram)
    - abas superiores frente/tras: metade da profundidade (fecham o transporte)
    - abas superiores laterais: 100 mm, dobram para DENTRO e viram o aro de
      travamento que impede a caixa de abrir quando a frente sai

REGRA QUE DIMENSIONA TUDO
  Os dois kits retangulares tem 26 cm: 2 x 26 = 52 cm exatos. Com profundidade
  interna de 52 a folga e ZERO. A profundidade interna precisa ser 53 cm.

Uso:  python3 calculo-expositora.py
"""
import math

# ---------------------------------------------------------------- entradas
KITS = {
    "A - kit quadrado":       (23.5, 25.5, 10.5),
    "B - kit retangular alto": (18.0, 26.0, 14.0),
    "C - kit retangular baixo": (18.0, 26.0,  8.0),
}

# caixa: (frente, profundidade, altura) INTERNAS, em cm
BRIEF = (56.0, 52.0, 72.0)   # medidas passadas
REC   = (56.0, 53.0, 72.0)   # com folga no eixo dos 26 cm
ALTA  = (56.0, 53.0, 75.0)   # + ganho de camada

ESP = 0.7        # espessura da onda BC (cm)
FOLGA_H = 0.3    # barriga por camada empilhada de caixinha de kit (cm)


def por_camada(F, P, kit):
    """Melhor arranjo em 2 blocos: bloco principal + faixa residual rodada."""
    a, b, _ = kit
    melhor = (0, "")
    for (u, v) in ((a, b), (b, a)):          # orientacao do bloco principal
        nu, nv = int(F // u), int(P // v)
        if nu == 0 or nv == 0:
            continue
        n = nu * nv
        desc = f"{nu} x {nv} ({u:g} x {v:g} cm)"
        # faixa que sobra na profundidade, preenchida com a peca rodada
        sobra = P - nv * v
        mu, mv = int(F // v), int(sobra // u)
        if mu and mv:
            n += mu * mv
            desc += f" + {mu} x {mv} rodados"
        # faixa que sobra na frente
        sobraF = F - nu * u
        ku, kv = int(sobraF // v), int(P // u)
        if ku and kv:
            n2 = nu * nv + ku * kv
            if n2 > n:
                n, desc = n2, f"{nu} x {nv} ({u:g} x {v:g} cm) + {ku} x {kv} rodados"
        if n > melhor[0]:
            melhor = (n, desc)
    return melhor


def camadas(H, h):
    n = int((H + 1e-9) // (h + FOLGA_H))
    return n, n * h


def analise(caixa, titulo):
    F, P, H = caixa
    vol_caixa = F * P * H
    print(f"\n{titulo}  ->  interno {F:g} x {P:g} x {H:g} cm  ({vol_caixa/1000:.1f} L)")
    print(f"{'kit':<26}{'por camada':<30}{'camadas':<10}{'total':<8}{'ocup.':<8}{'folgas (F/P/H)'}")
    tot = {}
    for nome, kit in KITS.items():
        n, desc = por_camada(F, P, kit)
        nc, hu = camadas(H, kit[2])
        total = n * nc
        ocup = total * kit[0] * kit[1] * kit[2] / vol_caixa
        # folga real do arranjo escolhido
        print(f"{nome:<26}{desc:<30}{nc:<10}{total:<8}{ocup*100:>5.0f}%   "
              f"sobra alt. {H - hu:.1f} cm")
        tot[nome] = total
    return tot


def mckee(F, P, ect, t=ESP, derate=1.0):
    """BCT (kgf) por McKee. ect em kgf/cm, t e perimetro em cm."""
    Z = 2 * (F + P)
    return 5.87 * ect * math.sqrt(t * Z) * derate


def blank(F, P, H, esp=ESP):
    """Cotas da chapa planificada (cm). Painel = interno + espessura."""
    pf, pp = F + esp, P + esp
    aba_cola = 4.0
    comp = 2 * pf + 2 * pp + aba_cola
    aba_inf_lat = pf / 2 - 0.2      # laterais se encontram na frente (56)
    aba_inf_ft  = pp / 2 - 0.2      # frente/tras se encontram na prof. (53)
    aba_sup_ft  = pp / 2 - 0.2
    aba_sup_lat = 10.0              # aro de travamento
    larg = aba_inf_lat + H + aba_sup_ft
    return dict(comp=comp, larg=larg, aba_cola=aba_cola,
                painel_frente=pf, painel_lateral=pp,
                aba_inf_lat=aba_inf_lat, aba_inf_ft=aba_inf_ft,
                aba_sup_ft=aba_sup_ft, aba_sup_lat=aba_sup_lat,
                area=comp * larg / 1e4)


def palete(F, P, esp=ESP, pal=(100.0, 120.0)):
    fe, pe = F + 2 * esp, P + 2 * esp
    melhor = (0, "")
    for (u, v) in ((fe, pe), (pe, fe)):
        n = int(pal[0] // u) * int(pal[1] // v)
        if n > melhor[0]:
            melhor = (n, f"{int(pal[0]//u)} x {int(pal[1]//v)}")
    return fe, pe, melhor


if __name__ == "__main__":
    print("=" * 96)
    print("CAIXA EXPOSITORA - 3 KITS")
    print("=" * 96)
    print(f"{'kit':<26}{'dimensoes (cm)':<22}{'volume (L)'}")
    for nome, (a, b, c) in KITS.items():
        print(f"{nome:<26}{a:g} x {b:g} x {c:g}{'':<8}{a*b*c/1000:.2f}")

    t1 = analise(BRIEF, "1) COMO VEIO NO BRIEFING")
    t2 = analise(REC,   "2) RECOMENDADO - profundidade 53 cm (folga no eixo dos 26)")
    t3 = analise(ALTA,  "3) OPCIONAL - altura interna 75 cm")

    print("\nGANHO DA ALTURA 75 cm:")
    for k in KITS:
        d = t3[k] - t2[k]
        print(f"  {k:<26}{t2[k]:>3} -> {t3[k]:>3} kits   ({d:+d}, {d/t2[k]*100:+.0f}%)")

    print("\n" + "-" * 96)
    print("CALCO DE FUNDO (nivela o topo da carga nos 3 kits, caixa interna 72 cm)")
    F, P, H = REC
    for nome, kit in KITS.items():
        nc, hu = camadas(H, kit[2])
        print(f"  {nome:<26}{nc} camadas = {hu:.1f} cm   ->  calco de {H-hu:.1f} cm")

    print("\n" + "-" * 96)
    print("RESISTENCIA A COMPRESSAO (McKee) - caixa 56 x 53, perimetro 218 cm")
    print(f"{'papel':<34}{'ECT':<10}{'BCT fechada':<16}{'BCT c/ frente aberta (-45%)'}")
    for papel, ect in (("onda C simples K180/K180", 5.2),
                       ("onda C simples K200/K200", 6.8),
                       ("onda BC dupla 175/150/175", 10.5),
                       ("onda BC dupla K200/K200", 13.0)):
        b1 = mckee(F, P, ect)
        b2 = mckee(F, P, ect, derate=0.55)
        print(f"{papel:<34}{ect:<10.1f}{b1:<16.0f}{b2:.0f} kgf")

    print("\n  Carga de projeto: 3 caixas empilhadas x 30 kg = 60 kg na de baixo.")
    for fs, desc in ((5, "6 meses de estoque + umidade 80% (fator 5)"),
                     (7, "cenario conservador (fator 7)")):
        print(f"    fator {fs} -> BCT minimo exigido = {60*fs} kgf   ({desc})")

    print("\n" + "-" * 96)
    print("CHAPA PLANIFICADA (onda BC 7 mm, medidas em cm)")
    b = blank(*REC)
    for k, v in b.items():
        print(f"  {k:<18}{v:.1f}")
    print(f"  peso estimado da caixa (BC ~700 g/m2): {b['area']*0.70:.2f} kg")

    print("\n" + "-" * 96)
    print("PALETIZACAO")
    for nome, cx in (("briefing 56x52", BRIEF), ("recomendado 56x53", REC)):
        fe, pe, (n, arr) = palete(cx[0], cx[1])
        area = n * fe * pe / (100 * 120)
        print(f"  {nome:<20}externo {fe:.1f} x {pe:.1f} cm  ->  PBR 100x120: "
              f"{n} caixas/camada ({arr}), {area*100:.0f}% do palete")
    print("  meio-palete 60 x 80 cm: 1 caixa, 57.4 <= 60 e 54.4 <= 80  -> serve como display de chao")
