#!/usr/bin/env python3
"""
Memoria de calculo da linha de potes retangulares modulares em PP.

GEOMETRIA
  Parede RETA (saida de 0,5 graus por lado, so o necessario para extrair) com
  cantos arredondados de R18. Nao e pote conado.

REGRA MODULAR
  O passo empilhado e um multiplo inteiro do modulo de 60 mm:
      600 ml = 1M | 1,2 L = 2M | 1,8 L = 3M | 2,4 L = 4M
  Com parede reta o volume fica praticamente proporcional a altura, entao passo
  modular e capacidade redonda deixam de brigar. O residuo (a secao cresce 0,5
  grau por lado ate o bocal) e absorvido por uma elevacao de fundo de 0 a 3,4 mm,
  invisivel por fora e sem efeito no empilhamento.

O ENCAIXE (o que faz o passo fechar exato)
  1. O fundo tem a MESMA espessura nos quatro potes (2,0 mm).
  2. A tampa e uma bandeja cujo piso fica exatamente 2,0 mm abaixo da borda do
     pote - ou seja, recuado para dentro da boca. Esse piso e o plano modular.
  3. Os ultimos 6 mm da base recuam para um PE EMBUTIDO de 113,0 x 86,9 mm,
     medida IGUAL nos quatro tamanhos (o degrau varia de 2,0 a 3,6 mm para
     compensar a saida). Esse pe desce dentro da bandeja da tampa de baixo.
  Resultado: passo = 60n exato, capacidade = 600n exata, uma tampa so.

Uso:  python3 calculo-modular.py
"""
import math

RHO_PP, RHO_TPE = 0.905e-3, 1.10e-3
ASP     = 1.30      # footprint: comprimento / largura
R_EXT   = 18.0      # raio de canto externo (mm)
M       = 60.0      # modulo: 600 ml por modulo
SAIDA   = 0.50      # saida por lado (graus)
BASE_T  = 2.00      # espessura do fundo - IGUAL nos quatro, trava o passo
PE_H    = 6.00      # altura do pe embutido
PE_L    = 110.0     # medida externa do pe - IGUAL nos quatro
WALL    = {1: 1.15, 2: 1.20, 3: 1.30, 4: 1.40}
PRES    = {1: 0.42, 2: 0.45, 3: 0.48, 4: 0.50}   # t/cm2 de fechamento
CICLO   = {1: 17, 2: 21, 3: 25, 4: 29}           # s
OVERLAP = 2.0       # quanto a tampa passa do corpo, por lado
ESP_TAMPA = 1.5


def area(a, b, r):
    return a * b - (4 - math.pi) * r * r


def perim(a, b, r):
    return 2 * (a + b) - (8 - 2 * math.pi) * r


def volume(a0, b0, at, bt, r, h, passos=3000):
    if h <= 0:
        return 0.0
    s = sum(area(a0 + (at - a0) * (i + .5) / passos,
                 b0 + (bt - b0) * (i + .5) / passos, r) for i in range(passos))
    return s * h / passos


def linha(ext_l):
    ext_w = ext_l / ASP
    t = math.tan(math.radians(SAIDA))
    potes = []
    for n in (1, 2, 3, 4):
        w, H = WALL[n], n * M                      # H: do piso interno ate a borda
        at, bt, r = ext_l - 2 * w, ext_w - 2 * w, R_EXT - w
        a0, b0 = at - 2 * H * t, bt - 2 * H * t    # secao interna no nivel do piso
        ext_base = ext_l - 2 * H * t               # base externa do corpo
        degrau = (ext_base - PE_L) / 2             # recuo do pe, por lado
        pa, pb = a0 - 2 * degrau, b0 - 2 * degrau  # secao interna dentro do pe

        def vol_com(e):
            return (volume(pa + 2 * e * t, pb + 2 * e * t,
                           pa + 2 * PE_H * t, pb + 2 * PE_H * t, r, PE_H - e)
                    + volume(a0, b0, at, bt, r, H - PE_H))

        lo, hi = -1.0, 12.0                        # bissecao na elevacao do fundo
        for _ in range(60):
            e = (lo + hi) / 2
            lo, hi = (e, hi) if vol_com(e) > n * 600e3 else (lo, e)
        e = (lo + hi) / 2
        peso = (perim((a0 + at) / 2, (b0 + bt) / 2, r) * (H - PE_H) * w   # parede
                + perim(pa, pb, r) * PE_H * w                            # parede do pe
                + area(pa, pb, r) * BASE_T                               # fundo
                + perim(at, bt, r) * 7 * (2.5 - w)) * RHO_PP             # borda reforcada
        potes.append(dict(n=n, cap=n * 600, ext_l=ext_l, ext_w=ext_w, at=at, bt=bt,
                          ext_base=ext_base, degrau=degrau, H=H + BASE_T, passo=n * M,
                          elev=e, vol=vol_com(e) / 1e3, peso=peso, w=w))
    return potes


def footprint():
    """Footprint em que o maior pote fecha 2400 ml com o fundo no nivel."""
    lo, hi = 95.0, 150.0
    for _ in range(50):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if linha(mid)[3]['elev'] > 0.0 else (mid, hi)
    return (lo + hi) / 2


def main():
    potes = linha(footprint())
    p0 = potes[0]
    print(f"Footprint {p0['ext_l']:.1f} x {p0['ext_w']:.1f} mm | canto R{R_EXT:.0f} | "
          f"saida {SAIDA}°/lado | modulo {M:.0f} mm | fundo {BASE_T:.1f} mm nos quatro")
    print(f"Pe embutido {PE_H:.0f} mm de altura, {PE_L:.1f} x {PE_L / ASP:.1f} mm — "
          f"mesma medida nos quatro\n")
    print(f"{'':>8} {'H corpo':>8} {'passo':>6} {'bocal int':>13} {'base ext':>9} "
          f"{'degrau pe':>10} {'elev.fundo':>10} {'parede':>7} {'V':>6} {'peso':>7}")
    for p in potes:
        print(f"{p['cap']:>6}ml {p['H']:>8.1f} {p['passo']:>6.0f} "
              f"{p['at']:>6.1f}x{p['bt']:<6.1f} {p['ext_base']:>9.1f} {p['degrau']:>10.2f} "
              f"{p['elev']:>10.1f} {p['w']:>7.2f} {p['vol']:>5.0f} {p['peso']:>6.1f}g")

    print("\nEmpilhamento (tudo tem que dar %d mm):" % (4 * M))
    for combo in [(1, 1, 1, 1), (2, 2), (1, 1, 2), (1, 3), (4,)]:
        total = sum(combo) * M
        print("  " + " + ".join(f"{c * 600}ml" for c in combo).ljust(34)
              + f"= {total:.0f} mm  {'OK' if abs(total - 4 * M) < 1e-9 else 'FALHA'}")

    print("\nInjecao (2 cavidades):")
    for p in potes:
        a_proj = (p['ext_l'] + 2 * OVERLAP + 2) * (p['ext_w'] + 2 * OVERLAP + 2) / 100
        print(f"{p['cap']:>6}ml | Aproj {a_proj:>4.0f} cm2 | {a_proj * PRES[p['n']] * 2 * 1.10:>4.0f} t | "
              f"curso >= {2.2 * p['H']:>4.0f} mm | altura molde ~{p['H'] + 190:>4.0f} mm | "
              f"injecao {p['peso'] * 2 * 1.15 / RHO_PP / 1e3:>4.0f} cm3 | "
              f"L/t {(p['H'] + p['ext_l'] / 2) / p['w']:>4.0f}")

    print("\nCapacidade (2 cav, 20 h/dia, 22 dias) e resina a R$ 11,06/kg:")
    for p in potes:
        pch = 3600 / CICLO[p['n']] * 2
        print(f"{p['cap']:>6}ml | ciclo {CICLO[p['n']]:>2} s | {pch:>5.0f} pc/h | "
              f"{pch * 20 * 22 / 1000:>6.1f} mil pc/mes | corpo R$ {p['peso'] * 11.06 / 1000:.2f}")

    lid_l, lid_w = p0['ext_l'] + 2 * OVERLAP, p0['ext_w'] + 2 * OVERLAP
    lid_r = R_EXT + OVERLAP
    tray_l, tray_w, tray_r = PE_L + 1.1, PE_L / ASP + 1.1, R_EXT - 4
    p_tray, p_lid = perim(tray_l, tray_w, tray_r), perim(lid_l, lid_w, lid_r)
    peso_tampa = (area(tray_l, tray_w, tray_r) * ESP_TAMPA          # piso da bandeja
                  + p_tray * BASE_T * ESP_TAMPA                     # parede da bandeja
                  + p_lid * ((lid_l - tray_l) / 2) * ESP_TAMPA * .55  # patamar sobre a borda
                  + p_lid * 11.0 * ESP_TAMPA                        # saia externa
                  + p_tray * 5 * ESP_TAMPA) * RHO_PP                # labio de vedacao
    aro = perim(p0['at'] - 2.6, p0['bt'] - 2.6, R_EXT - 3) * (2.8 * 2.2) * RHO_TPE
    print(f"\nTampa comum aos quatro: {lid_l:.1f} x {lid_w:.1f} mm | "
          f"bandeja livre {tray_l:.1f} x {tray_w:.1f} mm | piso {BASE_T:.1f} mm abaixo da borda")
    print(f"  em PP CP 141 ... {peso_tampa:>5.1f} g  R$ {peso_tampa * 10.52 / 1000:.2f}")
    print(f"  em PEBD PB 608 . {peso_tampa * .923 / .905:>5.1f} g  "
          f"R$ {peso_tampa * .923 / .905 * 11.10 / 1000:.2f}")
    print(f"  aro de TPE ..... {aro:>5.1f} g  (2,8 x 2,2 mm) — o mesmo nas tres tampas")

    print("\nAninhamento a vazio (6 potes de 2,4 L):")
    for s in (0.25, 0.50, 0.75, 1.00):
        z = min(WALL[4] / math.tan(math.radians(s)), potes[3]['H'])
        pilha = 5 * z + potes[3]['H']
        print(f"  saida {s:4.2f}° -> sobe {z:5.0f} mm | pilha {pilha:6.0f} mm "
              f"(-{100 * (1 - pilha / (6 * potes[3]['H'])):2.0f}% vs soltos)")

    print("\nMantimento:")
    for p in potes:
        L = p['cap'] / 1000
        print(f"  {p['cap']:>5} ml -> arroz {L * .85:.2f} kg | feijao {L * .80:.2f} kg | "
              f"acucar {L * .90:.2f} kg | macarrao {L * .35:.2f} kg")


if __name__ == '__main__':
    main()
