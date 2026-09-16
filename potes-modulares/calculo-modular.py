#!/usr/bin/env python3
"""
Memoria de calculo da linha de potes retangulares modulares em PP.

Regra: o passo empilhado de cada pote e um multiplo inteiro do modulo M,
de modo que qualquer combinacao empilhada chegue a altura do maior:
    500 ml = 1M | 1 L = 2M | 1,5 L = 3M | 2 L = 4M

Com bocal comum (tampa unica) e passo constante, a parede inclinada faz o
volume crescer mais rapido que a altura. A saida por lado e a variavel livre
que fecha as quatro capacidades; o pe (rebaixo de fundo) de 6 mm e comum.

Uso:  python3 calculo-modular.py [--modulo 600]   # 600 = escala alternativa B
"""
import math, sys

RHO = 0.905e-3          # g/mm3 - PP
ASP = 113.5 / 87.2      # razao do footprint (comprimento/largura)
PUNT = 6.0              # pe / rebaixo de fundo (mm)
M = 62.0                # modulo de empilhamento (mm)
WALL   = {1: 1.10, 2: 1.15, 3: 1.25, 4: 1.35}   # parede lateral por tamanho
BASE_T = {1: 1.70, 2: 1.80, 3: 1.90, 4: 2.00}   # fundo
PRES   = {1: 0.42, 2: 0.45, 3: 0.48, 4: 0.50}   # t/cm2 de fechamento
CICLO  = {1: 16, 2: 20, 3: 24, 4: 28}           # s, estimado
SAIDA_2L_ALVO = 1.2                             # graus: ancora do footprint


def volume(a0, b0, at, bt, h):
    """Prismatoide - exato para tronco de piramide de base retangular."""
    am, bm = (a0 + at) / 2, (b0 + bt) / 2
    return h / 6 * (a0 * b0 + 4 * am * bm + at * bt)


def linha(ext_l, alvo_ml):
    """Para um footprint dado, resolve a saida de cada tamanho que fecha a capacidade."""
    ext_w = ext_l / ASP
    potes = []
    for n in (1, 2, 3, 4):
        w = WALL[n]
        at, bt = ext_l - 2 * w, ext_w - 2 * w      # bocal interno
        h = n * M                                  # profundidade interna
        alvo = n * alvo_ml * 1e3
        lo, hi = 0.2, 4.0                          # bisseccao na saida (graus)
        for _ in range(80):
            d = (lo + hi) / 2
            t = math.tan(math.radians(d))
            a0, b0 = at - 2 * h * t, bt - 2 * h * t
            ap, bp = a0 + 2 * PUNT * t, b0 + 2 * PUNT * t
            if volume(ap, bp, at, bt, h - PUNT) > alvo:
                lo = d
            else:
                hi = d
        d = (lo + hi) / 2
        t = math.tan(math.radians(d))
        a0, b0 = at - 2 * h * t, bt - 2 * h * t
        ap, bp = a0 + 2 * PUNT * t, b0 + 2 * PUNT * t
        peso = (2 * ((a0 + at) / 2 + (b0 + bt) / 2) * h * w     # parede lateral
                + a0 * b0 * BASE_T[n]                          # fundo
                + 2 * (at + bt) * 6 * (2.3 - w)                # reforco de borda
                + (ap + bp) * 2 * PUNT * w) * RHO              # parede do pe
        potes.append(dict(n=n, cap=n * alvo_ml, ext_l=ext_l, ext_w=ext_w,
                          at=at, bt=bt, a0=a0, b0=b0, h=h, H=h + BASE_T[n],
                          saida=d, util=h - PUNT, w=w, peso=peso,
                          vol=volume(ap, bp, at, bt, h - PUNT) / 1e3))
    return potes


def footprint_para(alvo_ml):
    """Footprint tal que o maior pote fique com a saida minima desejada."""
    lo, hi = 95.0, 145.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if linha(mid, alvo_ml)[3]['saida'] < SAIDA_2L_ALVO:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    alvo = 600 if '--modulo' in sys.argv and '600' in sys.argv else 500
    potes = linha(footprint_para(alvo), alvo)
    p0 = potes[0]
    print(f"Footprint externo {p0['ext_l']:.1f} x {p0['ext_w']:.1f} mm | "
          f"modulo {M:.0f} mm | pe {PUNT:.0f} mm\n")
    print(f"{'':>8} {'H ext':>7} {'passo':>6} {'bocal int':>13} {'base int':>13} "
          f"{'saida':>7} {'util':>7} {'par.':>5} {'V':>6} {'peso':>7}")
    for p in potes:
        print(f"{p['cap']:>6}ml {p['H']:>7.1f} {p['n'] * M:>6.0f} "
              f"{p['at']:>6.1f}x{p['bt']:<6.1f} {p['a0']:>6.1f}x{p['b0']:<6.1f} "
              f"{p['saida']:>6.2f}° {p['util']:>7.1f} {p['w']:>5.2f} "
              f"{p['vol']:>5.0f} {p['peso']:>6.1f}g")

    print("\nEmpilhamento (tudo tem que dar %d mm):" % (4 * M))
    for combo in [(1, 1, 1, 1), (2, 2), (1, 1, 2), (1, 3), (4,)]:
        total = sum(combo) * M
        ok = 'OK' if abs(total - 4 * M) < 1e-9 else 'FALHA'
        print("  " + " + ".join(f"{c * alvo}ml" for c in combo).ljust(34)
              + f"= {total:.0f} mm  {ok}")

    print("\nInjecao (2 cavidades):")
    for p in potes:
        a_proj = (p['ext_l'] + 4) * (p['ext_w'] + 4) / 100      # cm2, com aba
        ton = a_proj * PRES[p['n']] * 2 * 1.10                  # +10% canal
        shot = p['peso'] * 2 * 1.15 / RHO / 1e3                 # cm3
        print(f"{p['cap']:>6}ml | Aproj {a_proj:>4.0f} cm2 | {ton:>4.0f} t | "
              f"injecao {shot:>4.0f} cm3 | L/t {(p['H'] + p['ext_l'] / 2) / p['w']:>4.0f} | "
              f"curso >= {2.2 * p['H']:>4.0f} mm | altura molde ~{p['H'] + 190:>4.0f} mm")

    print("\nCapacidade (2 cav, 20 h/dia, 22 dias):")
    for p in potes:
        pch = 3600 / CICLO[p['n']] * 2
        print(f"{p['cap']:>6}ml | ciclo {CICLO[p['n']]:>2} s | {pch:>5.0f} pc/h | "
              f"{pch * 20 * 22 / 1000:>6.1f} mil pc/mes | resina {p['peso'] * pch / 1000:>5.1f} kg/h")


if __name__ == '__main__':
    main()
