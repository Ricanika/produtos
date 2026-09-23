#!/usr/bin/env python3
"""
Memoria de calculo da linha de potes retangulares modulares em PP.

REVISAO 8 - borda alta e OCA, trava de clipe, tampa em PP.

DE ONDE VEM A GEOMETRIA
  Do STL de referencia que o Ricardo mandou (REF_231.stl, 66 591 triangulos,
  um pote e uma tampa em escala 1:10 - a parede medida, 0,113 mm, da 1,13 mm
  reais, e e isso que fixa a escala). O que foi medido nele:

      corpo          129,1 x 197,6 x 56,3 mm
      borda          17,3 mm de altura = 31% do pote, sobressai 9,6 mm/lado
      topo da borda  faixa chata de 4,3 mm, raio 2,5 fora e 1,9 dentro
      travas         DUAS, uma por lado COMPRIDO, 115,9 mm = 58% do comprimento
      gancho         pega 19,5 mm abaixo do topo da tampa; rabo desce ate 39

  O que veio da referencia: a borda alta com face externa reta, o topo chato
  com raios generosos, a aresta de engate na base da borda, e o layout de duas
  travas largas com rabo para o dedo. O que NAO veio: as cotas dos potes, que
  sao as da linha (altura, comprimento, largura e o R10 de canto).

O QUE A REFERENCIA OBRIGOU A CORRIGIR - e o erro da revisao 7
  Na revisao 7 a boca (144,95) era MAIS LARGA que a face externa do corpo
  (141,55). O colar era entao um anel de material entre 144,95 e 148,55,
  flutuando sobre um corpo que ia so ate 141,55: as duas secoes nao se
  encostavam. A malha fechava porque os dois aneis horizontais em z_col se
  cancelavam (volume zero), e nem o volume assinado nem a checagem de normais
  acusam isso. Impresso, o colar sairia solto.

  A referencia resolve com uma BORDA OCA: a parede sobe, abre num tronco de
  cone (o FLARE), vira o topo chato e desce de volta por fora numa SAIA livre.
  Entre a saia e a perna de dentro fica um canal aberto para baixo. A aresta de
  baixo da saia - uma face horizontal de W_SAIA mm - e a aresta de engate da
  trava. Como a saia e livre, essa aresta e material de verdade, nao um anel
  flutuando.

  O preco: a borda oca custa W_SAIA + CANAL + W_IN de largura, contra uma
  parede so. Isso empurra REB para cima e, pelo orcamento abaixo, o footprint
  cresce. Nao ha como fugir: o modulo fixa a secao interna.

A ALGEBRA DO PASSO
  Com A = secao interna, H_n = altura externa, e_n = altura do piso interno
  acima do fundo externo e t = quanto a superficie de apoio da tampa fica ACIMA
  da borda:
      capacidade   A*(H_n - e_n) = n*600e3   ->  H_n = e_n + n*k,  k = 600e3/A
      passo        p_n = H_n + t  e  p_n = n*p_1
      juntando     e_n = n*e_1 + (n-1)*t
  Com e_1 = BASE_T = 2,0, o unico t que mantem o fundo rente nos quatro e
  t = -2,0: o apoio TEM de ficar 2,0 mm dentro da boca.

AS DUAS TAMPAS, UM SO FILETE
  teca - placa macica, friso na face lateral, filete de TPE vedando RADIAL
         contra a boca. Sem trava: segura por atrito.
  PP   - plug com o MESMO friso e o MESMO filete, mais DUAS travas de clipe que
         engatam sob a saia da borda. A trava da a forca de fechamento; o
         filete so veda.

Uso:  python3 calculo-modular.py
"""
import math

RHO_PP, RHO_TPE = 0.905e-3, 1.10e-3

# ---- corpo ----
ASP     = 1.75      # footprint: comprimento / largura (frente estreita)
R_EXT   = 10.0      # raio de canto externo, na face externa da borda
M       = 60.0      # modulo: 600 ml por modulo
SAIDA   = 0.50      # saida por lado (graus)
BASE_T  = 2.00      # espessura do fundo - IGUAL nos quatro, trava o passo

# ---- borda alta e oca (o que veio da referencia) ----
BORDA_H = 12.00     # altura da borda: do topo ate onde comeca o FLARE
FLARE   = 4.00      # tronco de cone que abre da parede do corpo para a borda
SAIA_H  = 10.00     # quanto a saia externa desce -> e o nivel da aresta
TOPO_T  = 1.40      # espessura da faixa chata do topo
W_SAIA  = 1.20      # parede da saia externa = PROFUNDIDADE DA ARESTA DE ENGATE
CANAL   = 1.20      # folga entre a saia e a perna de dentro
W_IN    = 1.40      # parede da perna de dentro (a que faz a boca)
W_BORDA = W_SAIA + CANAL + W_IN         # largura total da borda
ARRED   = 1.20      # raio da aresta de cima, por fora
CHANF   = 0.60      # chanfro de entrada da boca
WALL    = {1: 1.15, 2: 1.20, 3: 1.30, 4: 1.40}

# ---- vedacao, comum as duas tampas ----
PLUG_FOLGA = 0.60   # folga entre a face do plug/placa e a boca
FRISO_PROF = 0.60   # profundidade do friso que aloja o filete
FILETE_D   = 1.40   # diametro do filete de TPE (corda)
FILETE_SOB = 0.80   # quanto o filete sobra do friso -> compressao = SOB - FOLGA
BANDEJA_FE = 0.50   # folga lateral do fundo do pote de cima na bandeja
MARGEM     = 0.30   # sobra que o orcamento de largura tem de deixar

# ---- tampa de PP com trava de clipe ----
PP_DECK     = 1.50  # espessura do deck e do piso da bandeja
PP_DECK_FORA = 1.80 # quanto o deck passa da face da borda, por lado
PP_PLUG_PAR = 0.80  # parede do plug (= parede da bandeja)
PP_PLUG_H   = 8.00  # quanto o plug desce abaixo do plano da borda
TRAVA_N     = 2     # DUAS travas, uma por lado comprido (veio da referencia)
TRAVA_FRAC  = 0.58  # fracao do comprimento que cada trava cobre (referencia)
TRAVA_T     = 1.00  # espessura da trava
TRAVA_FOLGA = 0.30  # folga da trava sobre a face externa da borda
TRAVA_FARPA = 0.80  # quanto o gancho avanca sob a aresta (de W_SAIA = 1,20)
TRAVA_RABO  = 6.00  # rabo abaixo do gancho, para o dedo
TRAVA_BULGE = 1.50  # quanto o rabo abre para fora, para dar pega
E_PP        = 1100.0  # modulo do PP randomico, MPa

# ---- teca ----
TECA_ESP  = 8.0     # espessura da placa de teca
RHO_TECA  = 0.65e-3 # teca seca, g/mm3

PRES    = {1: 0.42, 2: 0.45, 3: 0.48, 4: 0.50}   # t/cm2 de fechamento
CICLO   = {1: 17, 2: 21, 3: 25, 4: 29}           # s

T = math.tan(math.radians(SAIDA))


def area(a, b, r):
    return a * b - (4 - math.pi) * r * r


def perim(a, b, r):
    return 2 * (a + b) - (8 - 2 * math.pi) * r


def raio(L, colar_l):
    """Curva paralela: deslocar a secao de d para dentro tira d do raio."""
    return max(R_EXT + (L - colar_l) / 2, 0.15)


def tronco(L0, L1, h, colar_l, dLW, passos=2000):
    """Volume de um tronco entre duas secoes de retangulo arredondado."""
    if h <= 0:
        return 0.0
    s = 0.0
    for i in range(passos):
        L = L0 + (L1 - L0) * (i + .5) / passos
        s += area(L, L - dLW, raio(L, colar_l))
    return s * h / passos


def reb_necessario():
    """REB nao e estetica: e o orcamento de largura.

    Da face externa da borda ate a face interna da bandeja da tampa cabem, por
    lado:  W_BORDA + folga de encaixe + parede do plug + folga do plug. Quem
    paga e REB mais o que a saida ja estreitou no corpo do menor pote.
    """
    ganho = (M + BASE_T - BORDA_H - FLARE) * T
    preciso = W_BORDA + BANDEJA_FE + PP_PLUG_PAR + PLUG_FOLGA
    return preciso, ganho, preciso - ganho + MARGEM


PRECISO, GANHO, REB = reb_necessario()


def linha(colar_l):
    """colar_l e a medida MAXIMA do corpo (a face externa da borda)."""
    colar_w = colar_l / ASP
    dLW = colar_l - colar_w
    corpo_l = colar_l - 2 * REB                 # corpo, abaixo do flare
    boca    = colar_l - 2 * W_BORDA             # furo, no plano do topo
    potes = []
    for n in (1, 2, 3, 4):
        w, H = WALL[n], n * M + BASE_T
        z_body = H - BORDA_H - FLARE            # topo da parede reta
        z_bord = H - BORDA_H                    # onde a borda comeca
        corpo_z = lambda z: corpo_l - 2 * (z_body - z) * T
        boca_z  = lambda z: boca - 2 * (H - z) * T
        base_ext = corpo_z(0.0)                 # fundo: a medida mais estreita

        def vol_com(e):
            piso = BASE_T + e
            return (tronco(corpo_z(piso) - 2 * w, corpo_l - 2 * w,
                           z_body - piso, colar_l, dLW)
                    + tronco(corpo_l - 2 * w, boca_z(z_bord), FLARE, colar_l, dLW)
                    + tronco(boca_z(z_bord), boca, BORDA_H, colar_l, dLW))

        lo, hi = -1.0, 16.0
        for _ in range(60):
            e = (lo + hi) / 2
            lo, hi = (e, hi) if vol_com(e) > n * 600e3 else (lo, e)
        e = (lo + hi) / 2

        # peso: parede reta + flare + perna de dentro + saia + topo + fundo
        med_corpo = (corpo_z(BASE_T) + corpo_l) / 2 - w
        med_flare = (corpo_l - 2 * w + boca_z(z_bord)) / 2
        med_boca  = (boca_z(z_bord) + boca) / 2
        med_saia  = colar_l - W_SAIA
        slant = math.hypot(FLARE, (boca_z(z_bord) + 2 * W_IN - corpo_l) / 2)
        vol_mat = (perim(med_corpo, med_corpo - dLW, raio(med_corpo, colar_l))
                   * (z_body - BASE_T) * w
                   + perim(med_flare, med_flare - dLW, raio(med_flare, colar_l))
                   * slant * w
                   + perim(med_boca, med_boca - dLW, raio(med_boca, colar_l))
                   * (BORDA_H - TOPO_T) * W_IN
                   + perim(med_saia, med_saia - dLW, raio(med_saia, colar_l))
                   * (SAIA_H - TOPO_T) * W_SAIA
                   + (area(colar_l, colar_w, R_EXT)
                      - area(boca, boca - dLW, raio(boca, colar_l))) * TOPO_T
                   + area(base_ext, base_ext - dLW, raio(base_ext, colar_l)) * BASE_T)
        potes.append(dict(n=n, cap=n * 600, colar_l=colar_l, colar_w=colar_w,
                          corpo_l=corpo_l, corpo_w=corpo_l - dLW,
                          base_ext=base_ext, boca=boca, H=H, passo=n * M,
                          elev=e, vol=vol_com(e) / 1e3, peso=vol_mat * RHO_PP,
                          w=w, z_body=z_body, z_bord=z_bord, dLW=dLW))
    return potes


def footprint():
    """Borda em que o maior pote fecha 2400 ml com o fundo no nivel."""
    lo, hi = 110.0, 230.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if linha(mid)[3]['elev'] > 0.0 else (mid, hi)
    return (lo + hi) / 2


def main():
    potes = linha(footprint())
    p0 = potes[0]
    dLW = p0['dLW']
    boca = p0['boca']
    colar_l, colar_w = p0['colar_l'], p0['colar_w']

    print("=" * 79)
    print("REVISAO 8 - borda alta e OCA, trava de clipe, tampa em PP")
    print("=" * 79)
    print(f"Corpo (medida maxima, face externa da borda) {colar_l:.1f} x {colar_w:.1f} mm")
    print(f"Corpo reto (onde vai o IML) {p0['corpo_l']:.1f} x {p0['corpo_w']:.1f} mm | "
          f"canto R{R_EXT:.0f} | saida {SAIDA}°/lado | modulo {M:.0f} mm")
    print(f"Borda {BORDA_H:.1f} mm de altura + flare {FLARE:.1f} mm, sobressai "
          f"{REB:.2f} mm/lado | boca {boca:.1f} mm | fundo {BASE_T:.1f} mm nos quatro\n")

    print(f"{'':>8} {'H total':>8} {'passo':>6} {'corpo reto':>14} {'fundo ext':>10} "
          f"{'elev.fundo':>10} {'parede':>7} {'V':>6} {'peso':>7}")
    for p in potes:
        print(f"{p['cap']:>6}ml {p['H']:>8.1f} {p['passo']:>6.0f} "
              f"{p['corpo_l']:>7.1f}x{p['corpo_w']:<6.1f} {p['base_ext']:>10.2f} "
              f"{p['elev']:>10.2f} {p['w']:>7.2f} {p['vol']:>5.0f} {p['peso']:>6.1f}g")

    print("  (o peso acima e estimativa analitica - perimetro x espessura por faixa.")
    print("   gera-3d.py MEDE na malha fechada e da ~1,3% menos, porque a conta")
    print("   analitica conta duas vezes o material dos cantos. O que vai publicado")
    print("   e o da malha: 52,9 / 80,8 / 113,8 / 150,9 g.)")

    print("\nA BORDA, camada por camada (secao no meio de um lado, por lado):")
    print(f"  face externa ...... {colar_l:.1f} mm, reta, {SAIDA}°/lado, "
          f"do topo ate -{SAIA_H:.1f} mm")
    print(f"  faixa chata do topo {(colar_l - boca) / 2 - ARRED - CHANF:.2f} mm de "
          f"largura util, raio {ARRED:.2f} por fora e chanfro {CHANF:.2f} na boca")
    print(f"  saia externa ...... {W_SAIA:.2f} mm de parede, desce {SAIA_H:.1f} mm")
    print(f"  canal ............. {CANAL:.2f} mm de largura, {SAIA_H - TOPO_T:.1f} mm "
          f"de profundidade (nervura de aco de {CANAL:.2f} x {SAIA_H - TOPO_T:.1f})")
    print(f"  perna de dentro ... {W_IN:.2f} mm de parede, faz a boca de {boca:.1f} mm")
    print(f"  ARESTA DE ENGATE .. face de baixo da saia, {W_SAIA:.2f} mm/lado, "
          f"a {SAIA_H:.1f} mm do topo")
    print(f"  flare ............. abre {(boca + 2 * W_IN - p0['corpo_l']) / 2:.2f} mm/lado "
          f"em {FLARE:.1f} mm = {math.degrees(math.atan2((boca + 2 * W_IN - p0['corpo_l']) / 2, FLARE)):.0f}° "
          f"da vertical")

    print(f"\nOrcamento de largura - e ele que dimensiona REB:")
    print(f"  preciso por lado: W_BORDA {W_BORDA:.2f} (= saia {W_SAIA:.2f} + canal "
          f"{CANAL:.2f} + perna {W_IN:.2f}) + folga de encaixe {BANDEJA_FE:.2f}"
          f" + parede do plug {PP_PLUG_PAR:.2f} + folga do plug {PLUG_FOLGA:.2f}"
          f" = {PRECISO:.2f} mm")
    print(f"  a saida ja estreita {GANHO:.3f} mm no corpo do 600 ml")
    print(f"  logo REB = {PRECISO:.2f} - {GANHO:.3f} + margem {MARGEM:.2f} = {REB:.2f} mm")
    bandeja = boca - 2 * (PLUG_FOLGA + PP_PLUG_PAR)
    print(f"  confere: bandeja {bandeja:.2f} recebe o fundo de {p0['base_ext']:.2f} "
          f"com {(bandeja - p0['base_ext']) / 2:+.2f} mm/lado")

    print("\nEmpilhamento (tudo tem que dar %d mm):" % (4 * M))
    for combo in [(1, 1, 1, 1), (2, 2), (1, 1, 2), (1, 3), (4,)]:
        total = sum(combo) * M
        print("  " + " + ".join(f"{c * 600}ml" for c in combo).ljust(34)
              + f"= {total:.0f} mm  {'OK' if abs(total - 4 * M) < 1e-9 else 'FALHA'}")

    print("\nMolde do corpo:")
    print(f"  por fora, descendo: {colar_l:.1f} (saia) -> "
          f"{boca + 2 * W_IN:.1f} (perna) -> {p0['corpo_l']:.1f} (corpo) -> "
          f"{potes[3]['base_ext']:.1f} (fundo do 2,4 L) - so estreita.")
    print(f"  por dentro, descendo: {boca:.1f} (boca) -> "
          f"{p0['corpo_l'] - 2 * WALL[1]:.1f} (corpo) - so estreita.")
    print( "  nenhuma contra-saida: sem gaveta, sem extracao por arraste.")
    print(f"  o que o molde ganha de novo: a nervura do canal, {CANAL:.2f} mm de "
          f"espessura por {SAIA_H - TOPO_T:.1f} mm de altura")
    print(f"  ({(SAIA_H - TOPO_T) / CANAL:.1f}:1), continua nos {perim(colar_l, colar_w, R_EXT):.0f} mm "
          f"de perimetro. Pede raio no pe e saida propria.")
    print(f"  IML: o corpo e secao constante em {p0['corpo_l']:.1f} x {p0['corpo_w']:.1f} "
          f"com {SAIDA}°/lado, do flare ate o fundo - {p0['z_body']:.0f} mm no 600 ml.")

    # ---- vedacao: um filete para as duas tampas ----
    plug = boca - 2 * PLUG_FOLGA
    comp = FILETE_SOB - PLUG_FOLGA
    per_ved = perim(plug, plug - dLW, raio(plug, colar_l))
    filete = per_ved * math.pi * (FILETE_D / 2) ** 2 * RHO_TPE

    print("\n" + "=" * 79)
    print("VEDACAO - um filete de TPE, as duas tampas")
    print("=" * 79)
    print(f"  boca .............. {boca:.1f} x {boca - dLW:.1f} mm, {BORDA_H:.1f} mm de profundidade")
    print(f"  face do plug ...... {plug:.1f} mm (folga {PLUG_FOLGA:.2f}/lado)")
    print(f"  friso ............. {FRISO_PROF:.2f} mm de profundidade, filete "
          f"{FILETE_D:.2f} mm sobra {FILETE_SOB:.2f}")
    print(f"  compressao radial . {comp:.2f} mm/lado contra a parede da boca")
    print(f"  bandeja ........... {bandeja:.1f} mm recebe o fundo de "
          f"{p0['base_ext']:.2f} ({(bandeja - p0['base_ext']) / 2:+.2f} mm/lado)")
    print(f"  filete ............ {filete:.1f} g, perimetro {per_ved:.0f} mm, corda "
          f"de {FILETE_D:.2f} mm")

    a_plug = area(plug, plug - dLW, raio(plug, colar_l))
    print("\n  Capacidade de borda x capacidade util (a tampa entra na boca):")
    print(f"    {'tampa':<8} {'desce':>7} {'desloca':>9} | " +
          "  ".join(f"{p['cap']:>5} ml" for p in potes))
    for nome, prof in (('teca', BASE_T + TECA_ESP), ('PP', BASE_T + PP_PLUG_H)):
        desloc = a_plug * prof / 1e3
        print(f"    {nome:<8} {prof:>6.1f}mm {desloc:>8.0f} ml | " +
              "  ".join(f"{p['cap'] - desloc:>5.0f} ml" for p in potes))
    print("    A capacidade nominal e de BORDA, como manda a pratica do setor.")
    print(f"    No 600 ml a teca leva {a_plug * (BASE_T + TECA_ESP) / 1e3 / 6:.0f}% do volume.")
    print("    Decisao em aberto desde a revisao 7: rotular por borda ou re-resolver.")

    Etpe, forma, mu = 1.8, 1.8, 0.75
    f_filete = 0.0
    print("\n  Forca do filete (vedacao radial, o mesmo modelo da revisao 4):")
    for cp in (0.15, 0.20, 0.30):
        pres = Etpe * (cp / FILETE_D) * forma
        larg = 0.9 * math.sqrt(FILETE_D * cp)
        F = mu * pres * per_ved * larg
        if abs(cp - comp) < 0.01:
            f_filete = F / 9.81
        marca = "  <- especificado" if abs(cp - comp) < 0.01 else ""
        print(f"    compressao {cp:.2f} mm -> arrancar reto {F / 9.81:5.1f} kgf | "
              f"descascando um canto {F / 9.81 / 6:4.1f} kgf{marca}")

    # ---- tampa de teca ----
    a_teca = area(plug, plug - dLW, raio(plug, colar_l))
    print("\n" + "=" * 79)
    print("TAMPA DE TECA - placa macica com friso, sem trava")
    print("=" * 79)
    print(f"  placa {plug:.1f} x {plug - dLW:.1f} x {TECA_ESP:.1f} mm, "
          f"{a_teca * TECA_ESP * RHO_TECA:.0f} g em teca seca")
    print(f"  topo da placa {BASE_T:.1f} mm ABAIXO do topo da borda: e ele o plano")
    print(f"  modular, e o fundo reto do pote de cima pousa direto nele.")
    print(f"  com a borda de {BORDA_H:.1f} mm a placa fica embutida: a madeira aparece")
    print(f"  emoldurada pela borda, {BASE_T:.1f} mm abaixo dela.")
    print(f"  desce {TECA_ESP - BASE_T:.1f} mm dentro da boca de {BORDA_H:.1f} mm | "
          f"friso usinado na face lateral")
    print(f"  retencao: so atrito do filete -> {f_filete:.1f} kgf reto")

    # ---- tampa de PP com trava de clipe ----
    deck_o = colar_l + 2 * PP_DECK_FORA
    trava_larg = TRAVA_FRAC * colar_l
    trava_o = colar_w + 2 * (TRAVA_FOLGA + TRAVA_T + TRAVA_BULGE)
    I_tr = trava_larg * TRAVA_T ** 3 / 12
    braco = SAIA_H
    F_tr = 3 * E_PP * I_tr * TRAVA_FARPA / braco ** 3
    eps = 3 * TRAVA_T * TRAVA_FARPA / (2 * braco ** 2)
    alav = (braco + TRAVA_RABO) / braco
    print("\n" + "=" * 79)
    print("TAMPA DE PP COM TRAVA DE CLIPE - o layout veio da referencia")
    print("=" * 79)
    print(f"  deck: passa {PP_DECK_FORA:.2f} mm/lado da borda -> {deck_o:.1f} mm "
          f"de comprimento")
    print(f"  travas: {TRAVA_N}, uma por lado COMPRIDO, {trava_larg:.0f} mm cada "
          f"({TRAVA_FRAC * 100:.0f}% do comprimento, como na referencia)")
    print(f"  cada trava: {TRAVA_T:.2f} mm de espessura, folga {TRAVA_FOLGA:.2f} sobre "
          f"a borda, rabo de {TRAVA_RABO:.1f} mm abrindo {TRAVA_BULGE:.2f} mm")
    print(f"  medida maxima da tampa: {deck_o:.1f} x {trava_o:.1f} mm "
          f"(a trava so cresce a LARGURA)")
    print(f"  gancho: avanca {TRAVA_FARPA:.2f} mm sob a aresta de {W_SAIA:.2f} mm "
          f"= {TRAVA_FARPA / W_SAIA * 100:.0f}% de engate")
    print(f"  (a farpa e cotada da face da borda NA ALTURA DA ARESTA: em {SAIA_H:.0f} mm a")
    print(f"   saida ja estreitou {SAIA_H * T:.3f} mm, e cotar do topo entregaria "
          f"{TRAVA_FARPA - SAIA_H * T:.2f} mm de engate)")
    print(f"  braco de {braco:.1f} mm -> fechar pede {F_tr / 9.81:.1f} kgf por trava, "
          f"uma de cada vez")
    print(f"  deformacao de fibra {eps * 100:.2f}% (PP randomico escoa perto de 8%)")
    print(f"  abrir pelo rabo: alavanca {alav:.1f}x -> {F_tr / 9.81 / alav:.1f} kgf no dedo")
    print(f"  as {TRAVA_N} juntas travam GEOMETRICAMENTE: para sair, a trava tem de "
          f"abrir {TRAVA_FARPA:.2f} mm.")
    print(f"  o filete sozinho segura {f_filete:.1f} kgf de atrito - e o que a teca tem.")

    # ---- injecao ----
    a_corpo = area(colar_l, colar_w, R_EXT) / 100
    a_tampa = area(deck_o, trava_o, R_EXT) / 100
    print("\n" + "=" * 79)
    print("INJECAO (2 cavidades)")
    print("=" * 79)
    print(f"  area projetada do CORPO {a_corpo:.0f} cm2 (a borda, com os cantos "
          f"descontados) | da TAMPA {a_tampa:.0f} cm2")
    print( "  (revisao 7 publicava a area da TAMPA para os quatro corpos - "
           "146 cm2 - o que")
    print( "   sobrestimava o fechamento do corpo. Aqui cada peca usa a sua.)")
    for p in potes:
        print(f"{p['cap']:>6}ml | Aproj {a_corpo:>4.0f} cm2 | "
              f"{a_corpo * PRES[p['n']] * 2 * 1.10:>4.0f} t | "
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

    def flecha(larg, alt, w):
        b, a = min(larg, alt), max(larg, alt)
        return alfa(a / b) * b ** 4 / w ** 3

    print("\nRigidez do painel reto - cada tamanho contra ELE MESMO na revisao 7:")
    print( "  (rev 7: corpo 141,55, canto R6,5, painel reto de 128,6 mm e altura H-7;")
    print(f"   rev 8: corpo {p0['corpo_l']:.1f}, canto R{R_EXT - REB:.1f}, painel de "
          f"{p0['corpo_l'] - 2 * (R_EXT - REB):.1f} mm e altura H-{BORDA_H + FLARE + BASE_T:.0f})")
    for p in potes:
        l8, h8 = p['corpo_l'] - 2 * (R_EXT - REB), p['z_body'] - BASE_T
        l7, h7 = 128.55, p['H'] - 7.0
        r = flecha(l8, h8, p['w']) / flecha(l7, h7, p['w'])
        print(f"  {p['cap']:>5} ml | painel {l8:.1f} x {h8:.0f} mm | "
              f"flecha {r:.2f}x a da revisao 7")
    print(f"  o painel ficou {p0['corpo_l'] - 2 * (R_EXT - REB) - 128.55:+.1f} mm mais largo "
          f"(canto do corpo caiu de R6,5 para R{R_EXT - REB:.1f})")
    print(f"  e {BORDA_H + FLARE - 5:.0f} mm mais curto, porque a borda alta come altura de parede.")
    print(f"  em compensacao a borda oca e um caixao de {W_BORDA:.2f} x {BORDA_H:.1f} mm:")
    print( "  e ela o aro de rigidez da boca, muito mais rigida que o colar de")
    print( "  1,80 x 5,0 da revisao 7. Quem prende o filete e a boca, e ela enrijeceu.")

    # ---- aninhamento: interferencia real entre o perfil externo e o interno ----
    def aninha(p, s):
        """Quanto cada pote a mais soma na pilha, com saida s graus."""
        t = math.tan(math.radians(s))
        H, zb, zc = p['H'], p['z_body'], p['z_bord']
        def fora(y):                       # meia-largura externa do pote de cima
            if y <= zb:
                return (p['corpo_l'] - 2 * (zb - y) * t) / 2
            if y <= zc:
                return (p['corpo_l'] + (boca + 2 * W_IN - p['corpo_l'])
                        * (y - zb) / FLARE) / 2
            return (colar_l - 2 * (H - y) * t) / 2
        def dentro(d):                     # meia-largura interna do de baixo, a d do topo
            if d <= BORDA_H:
                return (boca - 2 * d * t) / 2
            if d <= BORDA_H + FLARE:
                return (boca - 2 * BORDA_H * t
                        - (boca - 2 * BORDA_H * t - (p['corpo_l'] - 2 * p['w']))
                        * (d - BORDA_H) / FLARE) / 2
            return (p['corpo_l'] - 2 * p['w'] - 2 * (d - BORDA_H - FLARE) * t) / 2
        lo, hi = 0.0, H
        for _ in range(50):                # maior profundidade sem interferencia
            mid = (lo + hi) / 2
            ok = all(fora(y) <= dentro(mid - y) + 1e-9
                     for y in [mid - d * mid / 120 for d in range(121)] if 0 <= y <= H)
            lo, hi = (mid, hi) if ok else (lo, mid)
        return H - lo

    print("\nAninhamento a vazio (6 potes de 2,4 L):")
    p4 = potes[3]
    for s in (0.25, 0.50, 0.75, 1.00):
        sobe = aninha(p4, s)
        pilha = 5 * sobe + p4['H']
        print(f"  saida {s:.2f}° -> sobe {sobe:5.0f} mm | pilha {pilha:6.0f} mm "
              f"({pilha / (6 * p4['H']) - 1:+.0%} vs soltos)")
    print( "  eu esperava que a borda alta estragasse o aninhamento - nao estraga.")
    print( "  A 0,50° da os mesmos 1044 mm da revisao 7: quem manda continua sendo")
    print( "  a saida, nao a borda. O flare so passa a ser o batente abaixo de 0,3°,")
    print( "  e ai ja nao aninhava mesmo.")

    print("\nMantimento:")
    for p in potes:
        print(f"  {p['cap']:>5} ml -> arroz {p['cap'] * 0.85 / 1000:.2f} kg | "
              f"feijao {p['cap'] * 0.80 / 1000:.2f} kg | "
              f"acucar {p['cap'] * 0.90 / 1000:.2f} kg | "
              f"macarrao {p['cap'] * 0.35 / 1000:.2f} kg")


if __name__ == '__main__':
    main()
