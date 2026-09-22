#!/usr/bin/env python3
"""
Memoria de calculo da linha de potes retangulares modulares em PP.

REVISAO 7 - arquitetura de borda lisa com colar, trava e rodape reto (IML).

O QUE MUDOU E POR QUE
  A aba em U saiu. No lugar dela a borda ganha um COLAR: um ressalto liso de
  REB mm por lado, com a aresta de cima arredondada. A face de baixo do colar e
  a aresta onde a TRAVA da tampa engata. O pe embutido saiu tambem: o rodape
  passa a ser RETO, secao constante do colar ate o fundo, que e o que o IML
  precisa para assentar o rotulo sem prega.

A ALGEBRA DO PASSO - e o que ela obriga
  Com A = secao interna, H_n = altura externa, e_n = altura do piso interno
  acima do fundo externo e t = quanto a superficie de apoio da tampa fica ACIMA
  da borda:
      capacidade   A*(H_n - e_n) = n*600e3   ->  H_n = e_n + n*k,  k = 600e3/A
      passo        p_n = H_n + t  e  p_n = n*p_1
      juntando     e_n = n*e_1 + (n-1)*t
  Com e_1 = BASE_T = 2,0, o unico t que mantem o fundo rente nos quatro e
  t = -2,0: o apoio TEM de ficar 2,0 mm dentro da boca. Qualquer apoio acima da
  borda levanta o fundo, e no 2,4 L isso vira 6 a 12 mm de espaco morto.

  Sem pe embutido, quem desce nesses 2,0 mm e o PROPRIO FUNDO RETO do pote de
  cima. Por isso o fundo tem de caber dentro da boca, e e isso que dimensiona o
  colar: REB nao e estetica, e o orcamento de largura (ver orcamento()).

AS DUAS TAMPAS, UM SO FILETE
  teca  - placa macica, friso na face lateral, filete de TPE vedando RADIAL
          contra a boca. Sem trava: segura por atrito, como sempre foi.
  PE    - plug com o MESMO friso e o MESMO filete, mais abas de trava que
          engatam sob o colar. A trava da a forca de fechamento que a teca nao
          tem; o filete e o mesmo numero de peca nas duas.

Uso:  python3 calculo-modular.py
"""
import math

RHO_PP, RHO_TPE, RHO_PE = 0.905e-3, 1.10e-3, 0.950e-3

# ---- corpo ----
ASP     = 1.75      # footprint: comprimento / largura (frente estreita)
R_EXT   = 10.0      # raio de canto externo, no colar
M       = 60.0      # modulo: 600 ml por modulo
SAIDA   = 0.50      # saida por lado (graus)
BASE_T  = 2.00      # espessura do fundo - IGUAL nos quatro, trava o passo
COLAR_H = 5.00      # altura do colar da borda
REB     = 3.50      # quanto o colar sobressai do corpo, por lado
W_BORDA = 1.80      # parede na faixa do colar - IGUAL nos quatro
WALL    = {1: 1.15, 2: 1.20, 3: 1.30, 4: 1.40}

# ---- vedacao, comum as duas tampas ----
PLUG_FOLGA = 0.60   # folga entre a face do plug/placa e a boca
FRISO_PROF = 0.60   # profundidade do friso que aloja o filete
FILETE_D   = 1.40   # diametro do filete de TPE (corda)
FILETE_SOB = 0.80   # quanto o filete sobra do friso -> compressao = SOB - FOLGA
BANDEJA_FE = 0.50   # folga lateral do fundo do pote de cima na bandeja

# ---- tampa PE com trava ----
PE_DECK_FORA = 3.10 # quanto o deck passa da face do colar, por lado
ABA_FOLGA  = 0.30   # folga da aba sobre a face do colar
PE_DECK    = 1.50   # espessura do deck e do piso da bandeja
PE_PLUG_PAR = 0.80  # parede do plug (= parede da bandeja)
ABA_N      = 6      # numero de abas de trava (2 por lado comprido, 1 por curto)
ABA_LARG   = 18.0   # largura de cada aba
ABA_T      = 1.00   # espessura da aba
ABA_BRACO  = 8.00   # da dobradica ate a farpa
ABA_RABO   = 5.00   # rabo abaixo da farpa, para o dedo
E_PP       = 1100.0 # modulo do PP randomico, MPa

# ---- teca ----
TECA_ESP  = 8.0     # espessura da placa de teca (minimo pratico com friso)
RHO_TECA  = 0.65e-3 # teca seca, g/mm3

PRES    = {1: 0.42, 2: 0.45, 3: 0.48, 4: 0.50}   # t/cm2 de fechamento
CICLO   = {1: 17, 2: 21, 3: 25, 4: 29}           # s


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


def orcamento():
    """O que decide REB. Se esta conta nao fecha, a linha nao empilha.

    Da face externa do colar ate a face interna da bandeja da tampa cabem, por
    lado:  W_BORDA + folga de encaixe + parede do plug + folga do plug.
    O que paga essa conta e REB mais o que a saida ja estreitou no corpo do
    menor pote (o de fundo mais largo).
    """
    t = math.tan(math.radians(SAIDA))
    ganho = (1 * M + BASE_T - COLAR_H) * t
    preciso = W_BORDA + BANDEJA_FE + PE_PLUG_PAR + PLUG_FOLGA
    return preciso, ganho, REB + ganho - preciso


def linha(colar_l):
    """colar_l e a medida MAXIMA da peca (a face externa do colar)."""
    colar_w = colar_l / ASP
    dLW = colar_l - colar_w
    t = math.tan(math.radians(SAIDA))
    corpo_l = colar_l - 2 * REB                 # corpo logo abaixo do colar
    boca    = colar_l - 2 * W_BORDA             # furo, no topo
    potes = []
    for n in (1, 2, 3, 4):
        w, H = WALL[n], n * M + BASE_T
        z_col = H - COLAR_H                     # onde o colar comeca
        # secoes externas
        base_ext = corpo_l - 2 * z_col * t      # fundo: a medida mais estreita
        # secoes internas
        int_col_topo = boca                              # furo no plano da borda
        int_col_base = boca - 2 * COLAR_H * t
        int_corpo_topo = corpo_l - 2 * w                 # logo abaixo do colar
        int_corpo_base = base_ext - 2 * w

        def vol_com(e):
            piso = BASE_T + e
            frac = (z_col - piso) / z_col if z_col > 0 else 0.0
            a_piso = int_corpo_base + (int_corpo_topo - int_corpo_base) * (piso / z_col)
            return (volume(a_piso, a_piso - dLW, int_corpo_topo, int_corpo_topo - dLW,
                           R_EXT - REB - w, z_col - piso)
                    + volume(int_col_base, int_col_base - dLW, int_col_topo,
                             int_col_topo - dLW, R_EXT - W_BORDA, COLAR_H))

        lo, hi = -1.0, 14.0
        for _ in range(60):
            e = (lo + hi) / 2
            lo, hi = (e, hi) if vol_com(e) > n * 600e3 else (lo, e)
        e = (lo + hi) / 2
        peso = ((perim((int_corpo_base + int_corpo_topo) / 2,
                       (int_corpo_base + int_corpo_topo) / 2 - dLW, R_EXT - REB - w)
                 * (z_col - BASE_T) * w                              # parede do corpo
                 + perim(boca - COLAR_H * t, boca - COLAR_H * t - dLW, R_EXT - W_BORDA)
                 * COLAR_H * W_BORDA                                 # faixa do colar
                 + area(base_ext, base_ext - dLW, R_EXT - REB) * BASE_T)  # fundo
                * RHO_PP)
        potes.append(dict(n=n, cap=n * 600, colar_l=colar_l, colar_w=colar_w,
                          corpo_l=corpo_l, corpo_w=corpo_l - dLW,
                          base_ext=base_ext, boca=boca, H=H, passo=n * M,
                          elev=e, vol=vol_com(e) / 1e3, peso=peso, w=w,
                          z_col=z_col))
    return potes


def footprint():
    """Colar em que o maior pote fecha 2400 ml com o fundo no nivel."""
    lo, hi = 110.0, 220.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if linha(mid)[3]['elev'] > 0.0 else (mid, hi)
    return (lo + hi) / 2


def main():
    potes = linha(footprint())
    p0 = potes[0]
    dLW = p0['colar_l'] - p0['colar_w']
    t = math.tan(math.radians(SAIDA))
    boca = p0['boca']

    print("=" * 79)
    print("REVISAO 7 - borda lisa com colar, trava no rebaixo, rodape reto (IML)")
    print("=" * 79)
    print(f"Colar (medida maxima) {p0['colar_l']:.1f} x {p0['colar_w']:.1f} mm | "
          f"canto R{R_EXT:.0f} | saida {SAIDA}°/lado | modulo {M:.0f} mm")
    print(f"Corpo (onde vai o IML) {p0['corpo_l']:.1f} x {p0['corpo_w']:.1f} mm, "
          f"reto do colar ate o fundo")
    print(f"Colar {COLAR_H:.1f} mm de altura, sobressai {REB:.2f} mm/lado | "
          f"boca {boca:.1f} mm | fundo {BASE_T:.1f} mm nos quatro\n")

    print(f"{'':>8} {'H total':>8} {'passo':>6} {'corpo no topo':>14} {'fundo ext':>10} "
          f"{'elev.fundo':>10} {'parede':>7} {'V':>6} {'peso':>7}")
    for p in potes:
        print(f"{p['cap']:>6}ml {p['H']:>8.1f} {p['passo']:>6.0f} "
              f"{p['corpo_l']:>7.1f}x{p['corpo_w']:<6.1f} {p['base_ext']:>10.2f} "
              f"{p['elev']:>10.2f} {p['w']:>7.2f} {p['vol']:>5.0f} {p['peso']:>6.1f}g")

    preciso, ganho, folga = orcamento()
    print(f"\nOrcamento de largura - e ele que dimensiona o colar:")
    print(f"  preciso por lado: W_BORDA {W_BORDA:.2f} + folga de encaixe {BANDEJA_FE:.2f}"
          f" + parede do plug {PE_PLUG_PAR:.2f} + folga do plug {PLUG_FOLGA:.2f}"
          f" = {preciso:.2f} mm")
    print(f"  pago por: REB {REB:.2f} + o que a saida estreita no 600 ml {ganho:.3f}"
          f" = {REB + ganho:.2f} mm")
    print(f"  folga: {folga:+.2f} mm  ->  {'FECHA' if folga > 0 else 'NAO FECHA'}")
    print(f"  fundo do 600 ml {potes[0]['base_ext']:.2f} entra na boca de {boca:.1f} "
          f"com {(boca - potes[0]['base_ext']) / 2:.2f} mm/lado")

    print("\nEmpilhamento (tudo tem que dar %d mm):" % (4 * M))
    for combo in [(1, 1, 1, 1), (2, 2), (1, 1, 2), (1, 3), (4,)]:
        total = sum(combo) * M
        print("  " + " + ".join(f"{c * 600}ml" for c in combo).ljust(34)
              + f"= {total:.0f} mm  {'OK' if abs(total - 4 * M) < 1e-9 else 'FALHA'}")

    print("\nMolde do corpo - o que a arquitetura nova resolve:")
    print(f"  descendo do colar a peca SO ESTREITA: {p0['colar_l']:.1f} -> "
          f"{p0['corpo_l']:.1f} -> {potes[3]['base_ext']:.1f}")
    print( "  nenhuma contra-saida: sem gaveta, sem extracao por arraste.")
    print( "  o rebaixo da trava e a face de baixo do colar, nao uma canaleta.")
    print(f"  IML: o corpo e secao constante em {p0['corpo_l']:.1f} x {p0['corpo_w']:.1f} "
          f"com {SAIDA}°/lado, sem degrau ate o fundo.")

    # ---- vedacao: um filete para as duas tampas ----
    plug = boca - 2 * PLUG_FOLGA
    bandeja = plug - 2 * PE_PLUG_PAR
    comp = FILETE_SOB - PLUG_FOLGA
    r_boca = R_EXT - W_BORDA
    per_ved = perim(plug, plug - dLW, R_EXT - W_BORDA - PLUG_FOLGA)
    filete = per_ved * math.pi * (FILETE_D / 2) ** 2 * RHO_TPE

    print("\n" + "=" * 79)
    print("VEDACAO - um filete de TPE, as duas tampas")
    print("=" * 79)
    print(f"  boca .............. {boca:.1f} x {boca - dLW:.1f} mm")
    print(f"  face do plug ...... {plug:.1f} mm (folga {PLUG_FOLGA:.2f}/lado)")
    print(f"  friso ............. {FRISO_PROF:.2f} mm de profundidade, filete "
          f"{FILETE_D:.2f} mm sobra {FILETE_SOB:.2f}")
    print(f"  compressao radial . {comp:.2f} mm/lado contra a parede da boca")
    print(f"  vao da bandeja .... {bandeja:.1f} mm recebe o fundo de "
          f"{potes[0]['base_ext']:.2f} ({(bandeja - potes[0]['base_ext']) / 2:+.2f} mm/lado)")
    print(f"  filete ............ {filete:.1f} g, perimetro {per_ved:.0f} mm, corda "
          f"de {FILETE_D:.2f} mm")

    # capacidade de BORDA x capacidade UTIL com a tampa fechada
    a_plug = area(plug, plug - dLW, R_EXT - W_BORDA - PLUG_FOLGA)
    print("\n  Capacidade de borda x capacidade util (a tampa entra na boca):")
    print(f"    {'tampa':<8} {'desce':>7} {'desloca':>9} | " +
          "  ".join(f"{p['cap']:>5} ml" for p in potes))
    for nome, prof in (('teca', BASE_T + TECA_ESP), ('PE', BASE_T + 6.0)):
        desloc = a_plug * prof / 1e3
        print(f"    {nome:<8} {prof:>6.1f}mm {desloc:>8.0f} ml | " +
              "  ".join(f"{p['cap'] - desloc:>5.0f} ml" for p in potes))
    print("    A capacidade nominal e de BORDA, como manda a pratica do setor - e a")
    print("    mesma convencao de todas as revisoes anteriores. Mas o plug precisa")
    print("    descer 2,0 mm (plano modular) mais a espessura da placa, e isso cobra:")
    print(f"    no 600 ml a teca leva {a_plug * (BASE_T + TECA_ESP) / 1e3 / 6:.0f}% do volume.")
    print("    Decisao em aberto: rotular por borda ou re-resolver para util.")

    E, forma, mu = 1.8, 1.8, 0.75
    print("\n  Forca do filete (vedacao radial, o mesmo modelo da revisao 4):")
    for cp in (0.15, 0.20, 0.30):
        pres = E * (cp / FILETE_D) * forma
        larg = 0.9 * math.sqrt(FILETE_D * cp)
        F = mu * pres * per_ved * larg
        marca = "  <- especificado" if abs(cp - comp) < 0.01 else ""
        print(f"    compressao {cp:.2f} mm -> arrancar reto {F / 9.81:5.1f} kgf | "
              f"descascando um canto {F / 9.81 / 6:4.1f} kgf{marca}")

    # ---- tampa de teca ----
    a_teca = area(plug, plug - dLW, R_EXT - W_BORDA - PLUG_FOLGA)
    peso_teca = a_teca * TECA_ESP * RHO_TECA
    print("\n" + "=" * 79)
    print("TAMPA DE TECA - placa macica com friso, sem trava")
    print("=" * 79)
    print(f"  placa {plug:.1f} x {plug - dLW:.1f} x {TECA_ESP:.1f} mm, "
          f"{peso_teca:.0f} g em teca seca")
    print(f"  topo da placa {BASE_T:.1f} mm ABAIXO da borda: e ele o plano modular.")
    print(f"  o fundo do pote de cima ({potes[0]['base_ext']:.2f}) pousa direto nela -")
    print(f"  nao precisa usinar poco nenhum, que era o ponto em aberto da revisao 6.")
    print(f"  desce {TECA_ESP - BASE_T:.1f} mm dentro da boca | friso usinado na face lateral")
    print(f"  retencao: so atrito do filete -> {'%.1f' % (mu * (E * (comp / FILETE_D) * forma) * per_ved * (0.9 * math.sqrt(FILETE_D * comp)) / 9.81)} kgf reto")

    # ---- tampa PE com trava ----
    # NAO ha saia continua: o deck passa do colar e as abas penduram dele.
    # (Ter descrito uma saia aqui e abas soltas na malha foi divergencia de
    #  revisao; quem manda e a peca de gera-3d.py.)
    deck_o = p0['colar_l'] + 2 * PE_DECK_FORA
    aba_i  = p0['colar_l'] + 2 * ABA_FOLGA
    aba_o  = aba_i + 2 * ABA_T
    ledge = REB - COLAR_H * t
    I_aba = ABA_LARG * ABA_T ** 3 / 12
    defl = ledge * 0.6                       # a farpa so precisa passar 60% da aresta
    F_aba = 3 * E_PP * I_aba * defl / ABA_BRACO ** 3
    print("\n" + "=" * 79)
    print("TAMPA PE COM TRAVA - engata sob o colar")
    print("=" * 79)
    print(f"  deck: passa {PE_DECK_FORA:.2f} mm/lado do colar -> {deck_o:.1f} x "
          f"{deck_o - dLW:.1f} mm (medida maxima da linha)")
    print(f"  abas: face interna {aba_i:.1f} (folga {ABA_FOLGA:.2f} sobre o colar), "
          f"externa {aba_o:.1f}")
    print(f"  aresta de engate (face de baixo do colar): {ledge:.2f} mm/lado")
    print(f"  {ABA_N} abas de {ABA_LARG:.0f} x {ABA_T:.2f} mm, braco {ABA_BRACO:.1f} mm, "
          f"rabo de {ABA_RABO:.1f} mm para o dedo")
    print(f"  farpa avanca {defl:.2f} mm -> cada aba pede {F_aba / 9.81:.1f} kgf "
          f"para fechar, uma de cada vez")
    print(f"  as {ABA_N} juntas seguram {ABA_N * F_aba / 9.81:.0f} kgf de arranque, "
          f"contra {'%.1f' % (mu * (E * (comp / FILETE_D) * forma) * per_ved * (0.9 * math.sqrt(FILETE_D * comp)) / 9.81)} kgf do filete sozinho")
    print( "  -> aqui a trava e a forca de fechamento e o filete so veda. E a")
    print( "     diferenca entre a tampa PE e a de teca, que so tem o atrito.")

    print(f"  peso 21,7 g em PP RP 141 -> R$ {21.7 * 9.55 / 1000:.2f} + filete "
          f"{filete:.1f} g   (peso MEDIDO na malha de gera-3d.py, que e a peca)")

    # ---- injecao ----
    print("\n" + "=" * 79)
    print("INJECAO (2 cavidades)")
    print("=" * 79)
    a_proj = (deck_o + 2) * (deck_o - dLW + 2) / 100
    for p in potes:
        print(f"{p['cap']:>6}ml | Aproj {a_proj:>4.0f} cm2 | "
              f"{a_proj * PRES[p['n']] * 2 * 1.10:>4.0f} t | "
              f"curso >= {2.2 * p['H']:>4.0f} mm | altura molde ~{p['H'] + 190:>4.0f} mm | "
              f"injecao {p['peso'] * 2 * 1.15 / RHO_PP / 1e3:>4.0f} cm3 | "
              f"L/t {(p['H'] + p['corpo_l'] / 2) / p['w']:>4.0f}")

    print("\nCapacidade (2 cav, 20 h/dia, 22 dias) e resina a R$ 11,06/kg:")
    for p in potes:
        pch = 3600 / CICLO[p['n']] * 2
        print(f"{p['cap']:>6}ml | ciclo {CICLO[p['n']]:>2} s | {pch:>5.0f} pc/h | "
              f"{pch * 20 * 22 / 1000:>6.1f} mil pc/mes | corpo R$ {p['peso'] * 11.06 / 1000:.2f}")

    # ---- rigidez ----
    def alfa(ab):
        tab = [(1.0, .0138), (1.2, .0188), (1.4, .0226), (1.6, .0251),
               (1.8, .0267), (2.0, .0277), (3.0, .0284), (99., .0284)]
        for (x0, y0), (x1, y1) in zip(tab, tab[1:]):
            if ab <= x1:
                return y0 + (y1 - y0) * (ab - x0) / (x1 - x0)
        return .0284

    def flecha(largura, altura, esp):
        b, a = min(largura, altura), max(largura, altura)
        return alfa(a / b) * b ** 4 / esp ** 3

    print("\nRigidez do painel reto (1,00 = o mesmo painel na revisao 6, 119,7 mm):")
    ref = flecha(119.7, 240.0, 1.40)
    for p in potes:
        pl = p['corpo_l'] - 2 * (R_EXT - REB)
        alt = p['z_col'] - BASE_T
        print(f"  {p['cap']:>5} ml | painel comprido {pl:.1f} x {alt:.0f} mm | "
              f"flecha {flecha(pl, alt, p['w']) / flecha(119.7, min(alt, 240.0), p['w']):.2f}x "
              f"o equivalente da revisao 6")
    print(f"  o colar substitui a aba em U como aro de rigidez da boca: secao de "
          f"{COLAR_H:.1f} x {W_BORDA:.2f} mm")

    print("\nAninhamento a vazio (6 potes de 2,4 L) - melhora sem o pe:")
    for s in (0.25, 0.50, 0.75, 1.00):
        z = min(WALL[4] / math.tan(math.radians(s)), potes[3]['z_col'])
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
