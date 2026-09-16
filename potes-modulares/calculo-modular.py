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
PE_L    = 112.4     # medida externa do pe - IGUAL nos quatro
W_BORDA = 1.40      # parede nos 10 mm abaixo da borda - IGUAL nos quatro, para o
                    # labio de vedacao da tampa achar sempre a mesma medida
ABA_W   = 3.00      # aba da borda, virada para fora, por lado
ABA_T   = 1.60      # espessura da aba
LIP_H   = 3.50      # labio descendente na ponta da aba (encaixe da tampa)
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
    """ext_l e a medida do CORPO; a aba da borda passa ABA_W para fora dela."""
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
        peso = ((perim((a0 + at) / 2, (b0 + bt) / 2, r) * (H - PE_H) * w  # parede
                + perim(pa, pb, r) * PE_H * w                            # parede do pe
                + area(pa, pb, r) * BASE_T                               # fundo
                + perim(ext_l, ext_w, R_EXT) * (ABA_W + LIP_H) * ABA_T) * RHO_PP)  # aba
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
    print(f"Pe embutido {PE_H:.0f} mm de altura, {PE_L:.1f} x {(PE_L - (p0['ext_l'] - p0['ext_w'])):.1f} mm — "
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

    # ---- tampa tipo PLUG, com vedacao RADIAL ----
    # Uma saia desce dentro do pote e leva o aro de TPE numa canaleta na face
    # externa. O aro trabalha contra a PAREDE do pote. Vedacao radial nao precisa
    # de forca permanente de fechamento - por isso dispensa trava e a tampa pode
    # ser lisa por fora. O que aparece e atrito, so na hora de enfiar e de tirar.
    PLUG_FOLGA, PLUG_PAR, CAN_PROF, ARO_SOBRA = 1.00, 1.50, 0.60, 1.20
    aba_out = p0['ext_l'] + 2 * ABA_W
    boca = p0['ext_l'] - 2 * W_BORDA
    boca_w = boca - (p0['ext_l'] - p0['ext_w'])
    plug = boca - 2 * PLUG_FOLGA
    bandeja = plug - 2 * PLUG_PAR
    comp = ARO_SOBRA - PLUG_FOLGA                 # compressao radial do aro
    aro_sec = (2.4, CAN_PROF + ARO_SOBRA)
    r_boca = R_EXT - W_BORDA
    per_ved = perim(boca, boca_w, r_boca)

    peso_tampa = (area(aba_out, aba_out - (p0['ext_l'] - p0['ext_w']), R_EXT + ABA_W) * ESP_TAMPA
                  + perim(plug, plug - (p0['ext_l'] - p0['ext_w']), R_EXT - 2.4) * 12.0 * PLUG_PAR) * RHO_PP
    aro = per_ved * (aro_sec[0] * aro_sec[1]) * RHO_TPE

    print(f"\nTampa PLUG, comum aos quatro: {aba_out:.1f} x "
          f"{aba_out - (p0['ext_l'] - p0['ext_w']):.1f} mm, rente a aba (sem saia externa)")
    print(f"  plug desce 12 mm na boca de {boca:.1f} mm | face do plug {plug:.1f} mm | "
          f"folga {PLUG_FOLGA:.2f} mm")
    print(f"  canaleta {CAN_PROF:.1f} mm de profundidade; aro sobra {ARO_SOBRA:.1f} mm "
          f"-> {comp:.2f} mm de compressao contra a parede")
    print(f"  vao da bandeja {bandeja:.1f} mm recebe o pe de {PE_L:.1f} mm")
    print(f"  tampa em PP RP 141 {peso_tampa:>5.1f} g  R$ {peso_tampa * 9.54 / 1000:.2f}")
    print(f"  aro de TPE {aro:>5.1f} g (secao {aro_sec[0]:.1f} x {aro_sec[1]:.1f} mm, "
          f"perimetro {per_ved:.0f} mm)")

    print("\nForca, com o aro trabalhando na parede (radial):")
    E, forma, mu = 1.8, 1.8, 0.75
    for cp in (0.15, 0.20, 0.30, 0.40):
        pres = E * (cp / aro_sec[1]) * forma
        larg = 0.9 * math.sqrt(aro_sec[1] * cp)
        F = mu * pres * per_ved * larg
        marca = "  <- especificado" if abs(cp - comp) < 0.01 else ""
        print(f"  compressao {cp:.2f} mm -> arrancar reto {F / 9.81:5.1f} kgf | "
              f"descascando um canto {F / 9.81 / 6:4.1f} kgf{marca}")
    print("  (para comparar: aro esmagado entre tampa e borda pediria 32 kgf o tempo todo)")

    print("\nAr presinho no fechamento (o aro so encosta nos ultimos 2 mm):")
    A_boca = area(boca, boca_w, r_boca) / 100
    for p in potes:
        dp = 101.3 * (A_boca * 0.2) / p['cap']
        print(f"  {p['cap']:>5} ml -> {dp:4.1f} kPa -> {dp * 1000 * A_boca / 1e4 / 9.81:4.1f} kgf a mais")

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
