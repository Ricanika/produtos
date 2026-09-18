#!/usr/bin/env python3
"""
Memoria de calculo da LINHA 2: potes modulares com TAMPA DESLIZANTE COM CAME.

O que muda em relacao a linha 1 (pasta potes-modulares/)
  Muda o TOPO DO CORPO e a TAMPA. Footprint, canto R18, saida de 0,5 graus,
  modulo de 60 mm, parede reta e o pe embutido continuam.

O MECANISMO
  A tampa nao e empurrada para baixo e nao rosqueia. Ela pousa deslocada uns
  14 mm, o usuario empurra no sentido do comprimento, e nesse curso:

    1. seis GANCHOS rigidos em L da tampa (macho) descem pelas janelas abertas
       no labio da aba do corpo (femea) e passam a correr por baixo dele;
    2. a aresta inferior do labio e uma RAMPA - ela desce no sentido do
       fechamento, entao o gancho e PUXADO PARA BAIXO enquanto avanca, 2,00 mm
       em 10 mm;
    3. os ultimos 3 mm do labio sao um PATAMAR PLANO: e ali que o gancho
       assenta de face inteira, 33,6 mm2, em vez de apoiar numa linha;
    4. quatro LINGUETAS flexiveis caem num rebaixo e dao o "clique". E o
       DETENTE que segura o fecho - nao o atrito da rampa.

  Quem veda e um LABIO de TPE na face inferior da tampa, apoiado na face
  superior da aba - vedacao AXIAL, mas com labio flexivel, nao com aro
  esmagado. Por isso a forca de fechamento cai de ~32 kgf (linha 1, revisao 2)
  para ~1 kgf, e essa forca passa a ser segurada pela GEOMETRIA da rampa.

  Virar de cabeca para baixo nao abre nada: a fuga do gancho e perpendicular a
  carga. E o ponto em que a trava do mercado falha (ela desarma por camagem).

REGRA MODULAR (mudou)
  Na linha 1 a bandeja era um rebaixo que ENTRAVA na boca do pote (piso 2,0 mm
  abaixo da borda). Isso e incompativel com a tampa deslizar: qualquer coisa
  que entre na boca trava o curso horizontal.
  Aqui a bandeja virou um MURETE ACIMA do plano da tampa. Nada entra na boca.
      passo = altura externa do corpo + espessura do prato da tampa = 60n
  Logo o corpo fica 4,0 mm mais baixo que na linha 1 e o footprint cresce um
  pouco para as capacidades continuarem redondas.

Uso:  python3 calculo-deslizante.py
"""
import math

# ---------------- constantes da familia (herdadas da linha 1) ----------------
RHO_PP, RHO_TPE = 0.905e-3, 1.10e-3
ASP     = 1.30
R_EXT   = 18.0
M       = 60.0
SAIDA   = 0.50
BASE_T  = 2.00      # fundo IGUAL nos quatro - volta a regra da linha 1
PE_H    = 6.00
PE_L    = 112.4
W_BORDA = 1.40
ABA_W   = 3.00      # aba da borda, virada para fora, por lado
ABA_T   = 1.60
WALL    = {1: 1.15, 2: 1.20, 3: 1.30, 4: 1.40}
PRES    = {1: 0.42, 2: 0.45, 3: 0.48, 4: 0.50}
CICLO   = {1: 17, 2: 21, 3: 25, 4: 29}
PRECO_H105, PRECO_RP141 = 11.06, 9.54

# ---------------- o que e novo ----------------
PRATO_T   = 1.50    # prato da tampa
RECESSO   = 2.00    # piso da bandeja ABAIXO da borda do pote. E o plano modular
                    # da linha 1, e e o que devolve as cotas originais do corpo.
PENETRA   = RECESSO + PRATO_T   # quanto a bandeja entra na boca = 3,50 mm
MURETE_H  = 3.50    # parede da bandeja (agora rebaixada, nao murete)
MURETE_T  = 1.50
NERV_N, NERV_H, NERV_T = 3, 5.00, 1.20   # nervuras no piso da bandeja
FOLGA_PE  = 1.00    # folga do pe dentro do murete, por lado
SAIA_H    = 9.00    # saia da tampa, por fora do corpo
SAIA_T    = 1.60

CURSO     = 24.0    # curso horizontal do fechamento
RAMPA_L   = 10.0    # trecho de rampa. Limitado por: CURSO - GANCHO_W >= RAMPA_L,
                    # senao o gancho nao chega inteiro ao patamar no fim do curso.
HOVER     = PENETRA + 0.50  # a tampa tem de pairar acima da BOCA, nao so acima da
                            # junta: a bandeja rebaixada entra 3,50 mm na boca.
PATAMAR_L = 14.0    # patamar PLANO no fim da rampa: e onde o gancho assenta

LAB_T, LAB_L, LAB_DEF = 1.30, 4.00, 1.00   # labio de TPE: espessura, balanco, deflexao
RAMPA_DZ  = HOVER            # queda da rampa = altura de pouso. A junta encosta
                             # dentro desse percurso, no ultimo 1,00 mm.
E_TPE     = 3.5     # MPa, TPE ~55 Shore A
E_PP      = 900.0   # MPa, PP RP 141 randomico (tampa)

GANCHO_N  = 4       # 2 por lado longo
GANCHO_W  = 14.0    # comprimento do gancho, no sentido do curso
GANCHO_P  = 3.60    # espessura do poste do gancho
GANCHO_O  = 2.00    # quanto cada asa do pe do gancho avanca sob a nervura da came
CAME_T    = 3.40    # espessura do labio descendente da aba NA ZONA DA CAME.
                    # O labio ja existia para dar rigidez a borda (secao em U);
                    # engrossado de 1,20 para 3,40 ele vira a propria came, e a
                    # aresta de baixo dele e a rampa. Uma peca, duas funcoes.

AB_L, AB_W = 30.0, 22.0       # abertura da tampa dosadora
CUR_L, CUR_T, CUR_TOPO = 34.0, 1.8, 3.0   # cursor: comprimento, espessura, saliencia
CUR_CAME_L, CUR_CAME_DZ = 5.0, 1.5        # came do cursor
BICO_P, BICO_H = 4.4, 5.0     # bico: projecao e altura
LING_N, LING_L, LING_W, LING_T = 4, 9.0, 16.0, 1.40   # linguetas do detente (2 por lado)
LING_DEF, LING_ANG = 0.60, 35.0

SIGMA_PP  = 30.0    # MPa, escoamento do PP
MU_SECO, MU_SABAO = 0.30, 0.08


def area(a, b, r):  return a * b - (4 - math.pi) * r * r
def perim(a, b, r): return 2 * (a + b) - (8 - 2 * math.pi) * r


def volume(a0, b0, at, bt, r, h):
    """A secao e quadratica em z (a e b variam linear, r e constante), entao
    Simpson com tres pontos e EXATO - nao e aproximacao numerica."""
    if h <= 0: return 0.0
    A0 = area(a0, b0, r)
    Am = area((a0 + at) / 2, (b0 + bt) / 2, r)
    At = area(at, bt, r)
    return h * (A0 + 4 * Am + At) / 6


def linha(ext_l, fundo=None):
    """Regra modular da LINHA 1, restaurada:
      1. fundo de 2,00 mm igual nos quatro;
      2. piso da bandeja da tampa 2,00 mm ABAIXO da borda do pote - e o plano
         modular;
      3. pe embutido nos ultimos 6 mm da base, medida igual nos quatro.
    Com isso o corpo volta a ser exatamente o da linha 1: 121,2 x 93,3 mm e
    alturas de 62 / 122 / 182 / 242 mm."""
    ext_w = ext_l / ASP
    t = math.tan(math.radians(SAIDA))
    potes = []
    for n in (1, 2, 3, 4):
        w = WALL[n]
        H = n * M                               # piso interno ate a borda
        at, bt, r = ext_l - 2 * w, ext_w - 2 * w, R_EXT - w
        a0, b0 = at - 2 * H * t, bt - 2 * H * t
        ext_base = ext_l - 2 * H * t
        degrau = (ext_base - PE_L) / 2
        pa, pb = a0 - 2 * degrau, b0 - 2 * degrau

        def vol_com(e):
            return (volume(pa + 2 * e * t, pb + 2 * e * t,
                           pa + 2 * PE_H * t, pb + 2 * PE_H * t, r, PE_H - e)
                    + volume(a0, b0, at, bt, r, H - PE_H))

        lo, hi = -1.0, 12.0
        for _ in range(60):
            e = (lo + hi) / 2
            lo, hi = (e, hi) if vol_com(e) > n * 600e3 else (lo, e)
        e = (lo + hi) / 2
        peso = ((perim((a0 + at) / 2, (b0 + bt) / 2, r) * (H - PE_H) * w
                + perim(pa, pb, r) * PE_H * w
                + area(pa, pb, r) * BASE_T
                + perim(ext_l, ext_w, R_EXT) * (ABA_W + 5.5) * ABA_T) * RHO_PP)
        potes.append(dict(n=n, cap=n * 600, ext_l=ext_l, ext_w=ext_w, at=at, bt=bt,
                          ext_base=ext_base, degrau=degrau, H_ext=H + BASE_T,
                          passo=n * M, elev=e, vol=vol_com(e) / 1e3, peso=peso, w=w,
                          fundo=BASE_T))
    return potes


def footprint():
    """Footprint em que o MAIOR pote fecha 2400 ml com o fundo no nivel - que e
    o criterio da linha 1, e devolve os mesmos 121,2 x 93,3 mm."""
    lo, hi = 95.0, 170.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if linha(mid)[3]['elev'] > 0.0 else (mid, hi)
    return (lo + hi) / 2


def fundos(ext_l):
    """Mantida por compatibilidade: agora o fundo e 2,00 mm nos quatro."""
    return {n: BASE_T for n in (1, 2, 3, 4)}


def sep(t): print("\n" + t + "\n" + "-" * len(t))


def main():
    fp = footprint()
    fnd = fundos(fp)
    potes = linha(fp, fnd)
    p0 = potes[0]
    ext_l, ext_w = p0['ext_l'], p0['ext_w']
    dif = ext_l - ext_w

    sep("1. A LINHA (o corpo so muda do ombro para cima)")
    print(f"Footprint {ext_l:.1f} x {ext_w:.1f} mm | canto R{R_EXT:.0f} | saida {SAIDA}°/lado")
    print(f"Modulo {M:.0f} mm | pe embutido {PE_L:.1f} x {PE_L - dif:.1f} mm x "
          f"{PE_H:.0f} mm de altura")
    print(f"Regra do passo (a da LINHA 1, restaurada): fundo {BASE_T:.2f} mm igual nos quatro,")
    print(f"piso da bandeja da tampa {RECESSO:.2f} mm ABAIXO da borda, pe embutido de "
          f"{PE_H:.0f} mm igual nos quatro.\n")
    print(f"{'':>8} {'H ext':>7} {'passo':>6} {'bocal int':>13} {'base ext':>9} "
          f"{'degrau':>7} {'fundo':>6} {'elev':>5} {'parede':>7} {'V ml':>6} {'peso':>7}")
    for p in potes:
        print(f"{p['cap']:>6}ml {p['H_ext']:>7.1f} {p['passo']:>6.0f} "
              f"{p['at']:>6.1f}x{p['bt']:<6.1f} {p['ext_base']:>9.1f} {p['degrau']:>7.2f} "
              f"{p['fundo']:>6.2f} {p['elev']:>5.1f} {p['w']:>7.2f} {p['vol']:>6.0f} "
              f"{p['peso']:>6.1f}g")
    print("\nEmpilhamento (tudo tem que dar %d mm):" % (4 * M))
    for combo in [(1, 1, 1, 1), (2, 2), (1, 1, 2), (1, 3), (4,)]:
        tot = sum(combo) * M
        print("  " + " + ".join(f"{c*600}ml" for c in combo).ljust(34)
              + f"= {tot:.0f} mm  {'OK' if abs(tot - 4*M) < 1e-9 else 'FALHA'}")
    alturas = "/".join(f"{p['H_ext']:.0f}" for p in potes)
    print(f"\nO CORPO E O DA LINHA 1, cota por cota: {ext_l:.1f} x {ext_w:.1f} mm, "
          f"alturas {alturas} mm.")
    print(f"Nada mudou do ombro para baixo. O mecanismo inteiro vive nos ultimos "
          f"{PENETRA + 2.0:.1f} mm do topo.")

    # ---------------- 2. bandeja: murete em vez de rebaixo ----------------
    sep("2. A BANDEJA VOLTOU A SER REBAIXADA - e o que a came teve de pagar")
    bandeja_int = murete_int = PE_L + 2 * FOLGA_PE
    murete_ext = murete_int + 2 * MURETE_T
    boca_min = min(p['at'] for p in potes)
    print(f"Piso da bandeja {RECESSO:.2f} mm abaixo da borda, prato de {PRATO_T:.2f} mm:")
    print(f"  a bandeja ENTRA {PENETRA:.2f} mm na boca do pote.")
    print(f"  vao interno {bandeja_int:.1f} x {bandeja_int - dif:.1f} mm recebe o pe de "
          f"{PE_L:.1f} mm")
    print(f"\nNa versao anterior eu tinha tirado a bandeja de dentro da boca justamente")
    print(f"porque qualquer coisa que entre na boca trava o curso horizontal. O preco era")
    print(f"corpo 4,0 mm mais baixo e footprint 2,2 mm maior - ou seja, NAO era mais o corpo")
    print(f"da linha 1. Para devolver o corpo original, a came e que teve de crescer:")
    print(f"  a tampa agora paira {HOVER:.2f} mm ({PENETRA:.2f} de bandeja + 0,50 de folga)")
    print(f"  antes de deslizar, em vez de {2.0:.2f} mm. A rampa desce esses {RAMPA_DZ:.2f} mm.")
    print(f"  Isso obrigou curso maior ({CURSO:.0f} mm) e ganchos maiores e em menor numero")
    print(f"  ({GANCHO_N} de {GANCHO_W:.0f} mm, contra 6 de 10). Detalhe na secao 4.")
    print(f"\nBoca do pote: {boca_min:.1f} mm no menor caso; a parede da bandeja fica em")
    print(f"{bandeja_int + 2 * MURETE_T:.1f} mm, com {(boca_min - bandeja_int - 2*MURETE_T)/2:.2f} mm "
          f"de folga por lado.")

    # ---------------- 3. vedacao ----------------
    sep("3. VEDACAO: LABIO DE TPE NA FACE DE CIMA DA ABA (axial, mas flexivel)")
    aba_out = ext_l + 2 * ABA_W
    sel_l = ext_l + ABA_W - 1.0                 # linha de vedacao, no meio da aba
    sel_w = sel_l - dif
    r_sel = R_EXT + (sel_l - ext_l) / 2
    per_sel = perim(sel_l, sel_w, r_sel)
    a_boca = area(boca_min, boca_min - dif, R_EXT - W_BORDA) / 1e2   # cm2

    I_lab = LAB_T ** 3 / 12                      # por mm de perimetro
    f_mm = 3 * E_TPE * I_lab * LAB_DEF / LAB_L ** 3
    F_ved = f_mm * per_sel
    larg_cont = 0.45
    p_cont = f_mm / larg_cont * 1e3              # kPa
    print(f"Linha de vedacao {sel_l:.1f} x {sel_w:.1f} mm, perimetro {per_sel:.0f} mm, "
          f"sobre a aba de {ABA_W+W_BORDA:.1f} mm de largura util")
    print(f"Labio de TPE {LAB_T:.2f} mm de espessura, {LAB_L:.1f} mm de balanco, "
          f"deflexao {LAB_DEF:.2f} mm, E={E_TPE:.1f} MPa")
    print(f"  carga de linha {f_mm:.3f} N/mm -> FORCA TOTAL DE FECHAMENTO "
          f"{F_ved:.1f} N = {F_ved/9.81:.2f} kgf")
    print(f"  pressao de contato {p_cont:.0f} kPa numa faixa de {larg_cont:.2f} mm")
    print(f"  na linha 1 (revisao 2), aro esmagado axial pedia 32 kgf -> "
          f"reducao de {32/(F_ved/9.81):.0f}x. E o que torna a came viavel.")
    print(f"\nO labio abre para DENTRO do pote: pressao interna empurra o labio contra a")
    print(f"sede (auto-energizado). De cabeca para baixo a vedacao melhora, nao piora.")
    print(f"\nPressao interna, pote invertido (sabao rho=1,03):")
    for p in potes:
        h = p['H_ext'] / 1000
        dp = 1030 * 9.81 * h / 1000              # kPa
        F = dp * 1000 * a_boca / 1e4
        print(f"  {p['cap']:>5} ml -> coluna {p['H_ext']:5.1f} mm -> {dp:4.1f} kPa -> "
              f"{F:5.1f} N = {F/9.81:4.2f} kgf querendo levantar a tampa "
              f"({dp/p_cont*100:3.0f}% da pressao de contato)")

    # ---------------- 4. a came ----------------
    sep("4. A CAME: RAMPA E PATAMAR")
    ang_r = math.degrees(math.atan(RAMPA_DZ / RAMPA_L))
    k_ved = F_ved / LAB_DEF
    print(f"Curso total {CURSO:.0f} mm = aproximacao {CURSO-RAMPA_L-PATAMAR_L:.0f} + rampa "
          f"{RAMPA_L:.0f} + patamar {PATAMAR_L:.0f}")
    print(f"Queda da rampa = folga de pouso {HOVER:.2f} + compressao da junta "
          f"{LAB_DEF:.2f} = {RAMPA_DZ:.2f} mm")
    print(f"  {RAMPA_DZ:.2f} mm em {RAMPA_L:.0f} mm -> rampa de {ang_r:.1f}°")
    print(f"  patamar dos ultimos {PATAMAR_L:.0f} mm e PLANO: e ali que o gancho assenta de")
    print(f"  face inteira ({GANCHO_W*CAME_T:.1f} mm2) e onde o detente clica.")
    print(f"\nPor que o patamar tem de ser plano - e onde eu errei primeiro:")
    print(f"  A ideia inicial era um SOBRE-CENTRO na propria came: uma depressao que a")
    print(f"  tampa teria de re-descer para voltar. Nao fecha - um gancho de topo plano nao")
    print(f"  entra numa depressao mais curta que ele, faz ponte.")
    print(f"\nO COMPRIMENTO DO GANCHO TAMBEM NAO E LIVRE:")
    print(f"      GANCHO_W + RAMPA_L <= CURSO")
    print(f"  Com os 6 ganchos de 10 mm e rampa de 6 da versao anterior isso fechava justo.")
    print(f"  Se nao fechar, no fim do curso o gancho fica montado meio na rampa, meio no")
    print(f"  patamar, e o apoio de FACE INTEIRA - que e o que a conta de queda usa -")
    print(f"  simplesmente nao existe. Dai ganchos")
    print(f"  de {GANCHO_W:.0f} mm com rampa de {RAMPA_L:.0f}: {GANCHO_W:.0f} + {RAMPA_L:.0f} = "
          f"{GANCHO_W+RAMPA_L:.0f} <= {CURSO:.0f}, e o gancho chega inteiro ao patamar.")
    print(f"  Uma funcao por peca: a RAMPA puxa, o DETENTE segura.")
    reto = (ABA_L := ext_l + 2 * ABA_W) - 2 * (R_EXT + ABA_W)
    cel = reto / (GANCHO_N // 2)
    jan = GANCHO_W + 1.0
    print(f"\nE O TRILHO SO CABE NO TRECHO RETO DO LADO LONGO")
    print(f"  O canto e R{R_EXT:.0f}. A aba so alcanca a linha do trilho enquanto |x| <= "
          f"{(ABA_L - 2*(R_EXT+ABA_W))/2:.1f} mm -")
    print(f"  fora disso ela ja curvou para dentro e nao ha material sobre o gancho. Logo o")
    print(f"  trilho tem {reto:.1f} mm por lado, nao {ABA_L:.1f}. Com {GANCHO_N//2} celulas:")
    print(f"    celula {cel:.2f} = janela {jan:.1f} + trilho {cel-jan:.2f}")
    print(f"    o trilho precisa de >= CURSO ({CURSO:.0f}) para o gancho chegar em casa: "
          f"{cel-jan:.2f} >= {CURSO:.0f} {'OK' if cel-jan >= CURSO else 'FALHA'}")
    print(f"  Com {GANCHO_N//2} celulas por lado o trilho sobra; o que aperta e a queda de "
          f"{RAMPA_DZ:.2f} mm,")
    print(f"  que exige rampa de {RAMPA_L:.0f} mm para nao ficar ingreme - e rampa longa "
          f"exige curso longo.")
    print(f"\nARMADILHA: sabao e lubrificante. mu do PP cai de ~{MU_SECO:.2f} seco para "
          f"~{MU_SABAO:.2f} ensaboado.")
    for mu in (MU_SECO, 0.15, MU_SABAO, 0.0):
        ang_at = math.degrees(math.atan(mu))
        trava = "trava" if ang_at > ang_r else "NAO TRAVA"
        print(f"  mu={mu:.2f} -> angulo de atrito {ang_at:4.1f}° vs rampa {ang_r:.1f}°: {trava}")
    print(f"Com a rampa a {ang_r:.1f}° nao trava nem seco. Isso NAO e um problema - e a ordem certa:")
    print("rampa livre significa que fechar e abrir custam pouco, e a retencao fica inteira")
    print("com o DETENTE, que e geometrico e funciona com mu = 0. Amarrar travamento a atrito")
    print("num pote de SABAO seria projetar para a bancada, nao para a pia.")

    # ---------------- 5. detente ----------------
    sep("5. DETENTE: E ELE QUE SEGURA, E E A COTA QUE SE AJUSTA NO TRY-OUT")
    I_l = LING_W * LING_T ** 3 / 12
    F_ling = 3 * E_PP * I_l * LING_DEF / LING_L ** 3
    eps = 3 * LING_T * LING_DEF / (2 * LING_L ** 2) * 100
    N_det = LING_N * F_ling
    print(f"{LING_N} linguetas ({LING_N//2} por lado longo) de {LING_L:.0f} x {LING_W:.0f} x "
          f"{LING_T:.2f} mm, deflexao {LING_DEF:.2f} mm")
    print(f"  forca normal por lingueta {F_ling:.1f} N, {LING_N} = {N_det:.1f} N")
    print(f"  deformacao na raiz {eps:.2f}% (PP suporta ~2% em ciclagem; "
          f"{'OK' if eps < 2 else 'ALTO'})")
    print(f"  face de saida a {LING_ANG:.0f}° - mais em pe que isso e a forca de abrir fica")
    print(f"  refem do atrito; mais deitada e o detente nao segura nada.")
    print(f"\nForca no polegar para ABRIR (detente + arrasto da junta no patamar):")
    ta = math.tan(math.radians(LING_ANG))
    for mu in (MU_SABAO, 0.15, MU_SECO):
        f_det = N_det * (ta + mu) / (1 - mu * ta)
        f_at = mu * F_ved
        tot = f_det + f_at
        print(f"  mu={mu:.2f} -> detente {f_det:5.1f} N + junta {f_at:4.1f} N = "
              f"{tot:5.1f} N = {tot/9.81:4.1f} kgf")
    print(f"\nJanela alvo: 2 a 4 kgf. Abaixo disso abre sozinho na bolsa; acima, o usuario")
    print(f"acha que quebrou. A interferencia da lingueta e a cota que se tira aco no")
    print(f"try-out ate o toque ficar certo - nenhuma outra cota do conjunto se mexe.")
    print(f"\nDegradacao segura: se o detente cansar, a tampa NAO sai - os ganchos sao")
    print(f"geometricos. Perde-se o clique e um pouco de vedacao, nao o fecho. Trava de")
    print(f"mercado que quebra perde tudo de uma vez.")

    # ---------------- 6. ganchos e queda ----------------
    sep("6. GANCHOS: DIMENSIONADOS PELA QUEDA, NAO PELA VEDACAO")
    # O contato e a face de baixo do LABIO, na largura engrossada de 2,40 mm.
    A_apoio = GANCHO_W * CAME_T
    A_poste = GANCHO_W * GANCHO_P
    print(f"{GANCHO_N} ganchos em L ({GANCHO_N//2} por lado longo), {GANCHO_W:.0f} mm de "
          f"comprimento, poste {GANCHO_P:.2f} mm, asa avanca {GANCHO_O:.2f} mm para dentro")
    print(f"A came e a aresta de baixo do LABIO DESCENDENTE da aba, engrossado de 1,20 para")
    print(f"{CAME_T:.2f} mm na zona de trabalho. O labio ja existia para dar rigidez a borda.")
    print(f"Sao so {GANCHO_N} ganchos porque a rampa ficou longa ({RAMPA_L:.0f} mm) e o gancho")
    print(f"precisa caber no trilho junto com ela. Cada um pega 1/{GANCHO_N} da carga de queda,")
    print(f"o que obrigou gancho de {GANCHO_W:.0f} mm, labio de {CAME_T:.2f} e poste de "
          f"{GANCHO_P:.2f} mm. A {GANCHO_P:.2f} mm")
    print(f"o poste ja pede alma vazada ou nervura no molde, senao rechupa na saia.")
    print(f"NAO se engrossa a ABA: ela e a face que veda, e variar espessura nela daria")
    print(f"rechupe bem em cima da junta. No labio, que e saia escondida, rechupe nao importa.")
    print(f"O poste desce por FORA do labio e a asa volta para dentro, por baixo dele - assim")
    print(f"o gancho inteiro aparece num corte transversal so.")
    print(f"  area de apoio por gancho {A_apoio:.1f} mm2 ({GANCHO_W:.0f} x {CAME_T:.2f}) | "
          f"secao do poste {A_poste:.1f} mm2")
    print(f"\nEm repouso, so a junta carrega: {F_ved/GANCHO_N:.1f} N por gancho -> "
          f"{F_ved/GANCHO_N/A_apoio:.3f} MPa de esmagamento.")
    print(f"  A essa tensao o PP nao flui. Foi por isso que o labio flexivel teve de vir")
    print(f"  antes da came: a 32 kgf a fluencia comeria a vedacao em poucos meses.")
    m24 = 2400 * 1.03 / 1000 + potes[3]['peso'] / 1000
    print(f"\nQueda com o 2,4 L cheio de sabao ({m24:.2f} kg), impacto na tampa:")
    for h, d in ((0.50, 0.008), (0.75, 0.008), (1.00, 0.008), (1.00, 0.005)):
        F = m24 * 9.81 * h / d
        s_ap = F / GANCHO_N / A_apoio
        s_po = F / GANCHO_N / A_poste
        ok = "OK" if max(s_ap, s_po) < SIGMA_PP else "FALHA"
        print(f"  {h:.2f} m, parada em {d*1000:.0f} mm -> {F:6.0f} N | por gancho "
              f"{F/GANCHO_N:5.0f} N | apoio {s_ap:5.1f} MPa | poste {s_po:5.1f} MPa | "
              f"{ok} (limite {SIGMA_PP:.0f})")
    print(f"\nA carga entra em ESMAGAMENTO e CISALHAMENTO, nao em flexao de trava. Trava de")
    print(f"mercado falha por camagem: a carga gira a trava e ela desarma sozinha. Aqui a")
    print(f"fuga do gancho e perpendicular a carga - a carga nao tem como abrir o gancho.")

    # ---------------- 7. borda entre ganchos ----------------
    sep("7. A BORDA ENTRE GANCHOS (se ela levantar, a vedacao vaza ali)")
    vao = (ext_l + 2*ABA_W - 2*(R_EXT+ABA_W)) / (GANCHO_N // 2)  # so o trecho reto
    b_h = 5.5
    I_u = (ABA_W * ABA_T**3 / 12 + ABA_W * ABA_T * (b_h/2)**2
           + 1.2 * b_h**3 / 12)
    q = f_mm
    d_max = 5 * q * vao**4 / (384 * 1300 * I_u)
    print(f"Ganchos a cada {vao:.0f} mm. Secao em U da aba: I = {I_u:.0f} mm4/mm "
          f"(parede simples de 1,40 mm daria {1.4**3/12:.2f})")
    print(f"Levantamento maximo no meio do vao: {d_max*1000:.1f} um, contra "
          f"{LAB_DEF*1000:.0f} um de deflexao do labio -> a junta acompanha "
          f"({d_max/LAB_DEF*100:.2f}% do curso). Sem risco de perder contato.")

    # ---------------- 8. prato da tampa ----------------
    sep("8. O PRATO AGUENTA A PILHA?")
    b = murete_int - dif
    D = E_PP * PRATO_T**3 / (12 * (1 - 0.42**2))
    q_dist = (2400*1.03/1000 + potes[3]['peso']/1000) * 9.81 / (murete_int * b)
    w_liso = 0.0084 * q_dist * b**4 / D
    # nervura em T: mesa = prato numa largura efetiva, alma = nervura
    lef = murete_int / NERV_N
    Af, Aw = lef * PRATO_T, NERV_T * NERV_H
    yb = (Af * PRATO_T/2 + Aw * (PRATO_T + NERV_H/2)) / (Af + Aw)
    I_n = (lef*PRATO_T**3/12 + Af*(yb - PRATO_T/2)**2
           + NERV_T*NERV_H**3/12 + Aw*(PRATO_T + NERV_H/2 - yb)**2)
    q_n = q_dist * lef
    I_liso = lef * PRATO_T**3 / 12                 # a MESMA faixa, sem nervura
    w_faixa = 5 * q_n * murete_int**4 / (384 * E_PP * I_liso)
    w_nerv = 5 * q_n * murete_int**4 / (384 * E_PP * I_n)
    print(f"Prato {PRATO_T:.1f} mm, E={E_PP:.0f} MPa -> D = {D:.0f} N.mm")
    print(f"Caso REAL (pilha): o pe do pote de cima e um perimetro de {PE_L:.1f} mm que apoia")
    print(f"  a {(murete_int-PE_L)/2:.1f} mm da parede da bandeja - a carga cai praticamente em")
    print(f"  cima do apoio, nao no vao. Flecha desprezivel.")
    print(f"Caso RUIM (alguem poe {m24:.1f} kg espalhado no centro da tampa), carga "
          f"{q_dist*1000:.2f} kPa:")
    print(f"  como PLACA apoiada nos 4 lados (trabalha nas duas direcoes):  {w_liso:.2f} mm")
    print(f"  Comparando faixa com faixa, que e o que mede o ganho da nervura:")
    print(f"    faixa lisa de {lef:.0f} mm, I = {I_liso:.0f} mm4   -> {w_faixa:5.2f} mm")
    print(f"    mesma faixa com nervura {NERV_T:.1f} x {NERV_H:.1f}, I = {I_n:.0f} mm4 -> "
          f"{w_nerv:5.2f} mm  ({I_n/I_liso:.1f}x mais rigida)")
    print(f"  A placa lisa ja da {w_liso:.2f} mm porque trabalha nas duas direcoes; as nervuras")
    print(f"  entram para garantir margem e matar o empenamento de moldagem no prato chato.")
    print(f"  As nervuras ficam NO PISO DA BANDEJA. O pe do pote de cima e")
    print(f"  um perimetro vazado de {PE_H:.0f} mm - as nervuras de {NERV_H:.1f} mm passam por dentro dele.")

    # ---------------- 9. peso e custo ----------------
    sep("9. PESO E CUSTO DA TAMPA")
    tampa_l, tampa_w = aba_out, aba_out - dif
    a_prato = area(tampa_l, tampa_w, R_EXT + ABA_W)
    p_saia = perim(tampa_l, tampa_w, R_EXT + ABA_W)
    p_mur = perim(murete_ext, murete_ext - dif, R_EXT - 4)
    v_ganchos = GANCHO_N * GANCHO_W * (GANCHO_P * 7.0 + GANCHO_O * 2.0)
    v_nerv = NERV_N * murete_int * NERV_T * NERV_H
    peso_tampa = (a_prato * PRATO_T + p_saia * SAIA_H * SAIA_T
                  + p_mur * MURETE_H * MURETE_T + v_ganchos + v_nerv) * RHO_PP
    peso_lab = per_sel * (LAB_T * (LAB_L + 1.5) * 0.8) * RHO_TPE
    print(f"Tampa {tampa_l:.1f} x {tampa_w:.1f} mm (rente a aba), em PP RP 141")
    print(f"  prato {PRATO_T:.1f} | saia {SAIA_H:.1f} x {SAIA_T:.2f} | murete "
          f"{MURETE_H:.1f} x {MURETE_T:.2f} | {NERV_N} nervuras | {GANCHO_N} ganchos | "
          f"2 linguetas")
    print(f"  peso {peso_tampa:.1f} g -> R$ {peso_tampa*PRECO_RP141/1000:.2f}")
    print(f"Labio de TPE (peca montada, perfil extrudado e soldado no canto): "
          f"{peso_lab:.1f} g -> R$ {peso_lab*17.0/1000:.2f} a R$ 17/kg")
    print(f"CONJUNTO 600 ml: corpo R$ {potes[0]['peso']*PRECO_H105/1000:.2f} + tampa "
          f"R$ {peso_tampa*PRECO_RP141/1000:.2f} + labio R$ {peso_lab*17.0/1000:.2f} = "
          f"R$ {(potes[0]['peso']*PRECO_H105 + peso_tampa*PRECO_RP141 + peso_lab*17.0)/1000:.2f} de resina")

    # ---------------- 10. injecao ----------------
    sep("10. INJECAO (2 cavidades) - o parque nao muda")
    for p in potes:
        a_proj = (p['ext_l'] + 2*ABA_W + 2) * (p['ext_w'] + 2*ABA_W + 2) / 100
        ton = a_proj * PRES[p['n']] * 2 * 1.10
        maq = 200 if p['n'] <= 2 else (250 if p['n'] == 3 else 380)
        print(f"{p['cap']:>6}ml | Aproj {a_proj:>4.0f} cm2 | {ton:>4.0f} t | INJ {maq} t | "
              f"curso >= {2.2*p['H_ext']:>4.0f} mm | L/t {(p['H_ext']+p['ext_l']/2)/p['w']:>4.0f} | "
              f"{3600/CICLO[p['n']]*2*20*22/1000:>5.1f} mil pc/mes")
    a_tampa = (tampa_l + 2) * (tampa_w + 2) / 100
    print(f"  tampa | Aproj {a_tampa:>4.0f} cm2 | {a_tampa*0.40*4*1.10:>4.0f} t com 4 cav | "
          f"molde com 2 gavetas laterais (os ganchos)")

    # ---------------- 11. bico ----------------
    sep("11. TAMPA DOSADORA: BOCAL RENTE, FILETE DE TPE E TRAVINHA DE GIRO")
    COL_DI, COL_DE = 40.0, 43.0          # bocal: furo e externo
    LUG_DE, LUG_N, LUG_W, LUG_H = 46.5, 3, 8.0, 1.2
    TPE_D, TPE_SEC, TPE_COMP = 49.0, 2.0, 0.8
    COPO_DI, COPO_PROF = 52.0, 32.0
    GIRO, COPO_DZ = 30.0, 1.2
    col_h = RECESSO + PRATO_T            # do piso da bandeja ate o plano da tampa
    print(f"O bocal DESCEU e virou parte da tampa - nao e mais chamine.")
    print(f"  Ele sobe {col_h:.1f} mm do piso da bandeja e para EXATAMENTE no plano da aba")
    print(f"  da tampa. Saliencia acima da tampa: ZERO. E uma peca so com o prato.")
    print(f"\n  furo ........ {COL_DI:.0f} mm | parede do bocal {(COL_DE-COL_DI)/2:.1f} mm")
    print(f"  travinha .... {LUG_N} ressaltos MACHO na face externa do bocal, ate "
          f"{LUG_DE:.1f} mm,")
    print(f"                {LUG_W:.0f} mm de largura, {LUG_H:.1f} mm de altura")
    print(f"  filete TPE .. cordao de {TPE_SEC:.1f} mm em canaleta no piso, no circulo "
          f"{TPE_D:.0f} mm")
    print(f"  copo ........ {COPO_DI:.0f} mm interno x {COPO_PROF:.0f} mm, com {LUG_N} rasgos "
          f"FEMEA em L na saia")

    print(f"\nO FECHO: pousa, gira {GIRO:.0f}°, trava. Sem rosca, sem orelha, sem trava aparente.")
    print(f"  A perna circunferencial do rasgo e RAMPADA: no giro ela puxa o copo")
    print(f"  {COPO_DZ:.1f} mm para baixo e esmaga o filete {TPE_COMP:.1f} mm.")
    per_c = math.pi * TPE_D
    f_mm_c = 3 * E_TPE * (LAB_T ** 3 / 12) * LAB_DEF / LAB_L ** 3
    F_c = f_mm_c * per_c
    r_lug = LUG_DE / 2
    arco = math.pi * LUG_DE * GIRO / 360
    ang_c = math.degrees(math.atan(COPO_DZ / arco))
    print(f"\n  filete: circulo {TPE_D:.0f} mm, perimetro {per_c:.0f} mm")
    print(f"  forca de fechamento {F_c:.1f} N = {F_c/9.81:.2f} kgf")
    print(f"  rampa do rasgo: {COPO_DZ:.1f} mm em {arco:.1f} mm de arco = {ang_c:.1f}°")
    for mu in (MU_SABAO, MU_SECO):
        ta = math.tan(math.radians(ang_c))
        T = F_c * (r_lug / 1000) * (ta + mu) / (1 - mu * ta)
        print(f"    mu={mu:.2f} -> torque para fechar {T*1000:5.0f} N.mm")
    print(f"  Tampa de vidro comum pede 500 a 1500 N.mm. Ou seja: a vedacao nao da nenhum")
    print(f"  'toque'. Quem da o toque e o DETENTE no fim da rampa, ~300 N.mm.")

    print(f"\nA TRAVINHA AGUENTA? {LUG_N} ressaltos de {LUG_W:.0f} x "
          f"{(LUG_DE-COL_DE)/2:.2f} mm de engate:")
    a_lug = LUG_N * LUG_W * (LUG_DE - COL_DE) / 2
    a_furo = math.pi * (COL_DI / 2) ** 2 / 1e2
    print(f"  area de cisalhamento {a_lug:.1f} mm2 -> capacidade "
          f"{a_lug * SIGMA_PP / 9.81:.0f} kgf")
    for p in potes[-1:]:
        dp = 1030 * 9.81 * (p['H_ext'] / 1000) / 1000
        F = dp * 1000 * a_furo / 1e4
        print(f"  carga real com o 2,4 L invertido: {F:.2f} N = {F/9.81:.2f} kgf "
              f"-> fator {a_lug*SIGMA_PP/F:.0f}x")
    print(f"  E a fuga do ressalto e ROTACIONAL contra carga AXIAL: perpendicular, como")
    print(f"  nos ganchos da tampa. Um tombo nao tem como girar o copo.")

    vol = math.pi * (COPO_DI / 2) ** 2 * COPO_PROF / 1e3
    print(f"\nO COPO E O DOSADOR: {vol:.0f} ml. Marcar 25 e 50 ml em relevo.")
    print(f"  Altura acima do plano da tampa: {COPO_PROF - col_h:.1f} mm.")

    print(f"\nO PRECO DE DEIXAR O BOCAL RENTE - e honesto dizer:")
    print(f"  bico saliente quebra o filete de liquido longe da parede. Bocal rente nao.")
    print(f"  Compensacoes, todas dentro do plano da tampa:")
    print(f"    - piso da bandeja com caimento de 3° para o bocal (nada empoca)")
    print(f"    - entalhe de 14 mm na parede da bandeja, do lado do despejo")
    print(f"    - aresta de corte de 0,4 mm na BORDA EXTERNA da tampa, nesse lado:")
    print(f"      e ali que o filete se solta, a {(ext_l + 2*ABA_W)/2:.1f} mm do centro,")
    print(f"      ja para fora da boca do pote ({boca_min/2:.1f} mm) - o jato nao lambe a parede.")
    print(f"  Fica em aberto medir o respingo no prototipo. Se incomodar, o bico volta a")
    print(f"  subir 4 mm e a tampa dosadora deixa de ser rente - e uma cota, nao um redesenho.")

    print(f"\nRESPIRO: nao precisa. Furo de {COL_DI:.0f} mm - acima de ~20 mm o ar entra")
    print(f"  pelo proprio furo enquanto o liquido sai.")

    sep("12. O QUE FICA ABERTO")
    abertos = [
        ["Busca de anterioridade no INPI/Espacenet (B65D 43/20, 45/16, 53/02) ANTES de",
         "divulgar. O arranjo parece patenteavel como Modelo de Utilidade."],
        ["Atrito real PP/PP com filme de sabao - medir, nao estimar. Toda a janela do",
         "detente depende disso."],
        ["Retencao do labio de TPE na canaleta da tampa: 500 aberturas."],
        ["Ensaio de estanqueidade: agua colorida, 24 h, deitado e invertido, com e sem",
         "ciclagem termica (geladeira -> bancada)."],
        ["Queda de 0,75 m com o 2,4 L cheio, sobre a tampa e sobre o canto."],
        ["Fluencia: 90 dias fechado a 40°C, medir a deflexao residual do labio."],
        ["Prototipo impresso do 600 ml + tampa: o curso da came e o clique se sentem na mao."],
    ]
    for i, linhas in enumerate(abertos, 1):
        print(f"  {i:>2}. {linhas[0]}")
        for extra in linhas[1:]:
            print(f"      {extra}")


if __name__ == '__main__':
    main()
