#!/usr/bin/env python3
"""
Memoria de calculo da linha de potes retangulares modulares em PP.

REVISAO 10 - borda de 8 mm com DENTE, tampa de uma saia so, aro em U de silicone.

O QUE MUDOU, E POR QUE
  O Ricardo trouxe uma referencia fisica (fotos de um pote cinza com tampa
  canelada e um perfil de silicone em U na mao) e descreveu tres coisas:

    1) borda superior de ~8 mm de altura, com um DENTE em toda a volta na base
       dela - e nesse dente que a trava da tampa engata;
    2) a borda EXPANDE PARA FORA ~3 mm, e nessa expansao encaixa a parte
       interna da tampa;
    3) a tampa entra no corpo; na lateral dela fica um vao, e nesse vao vai o
       silicone, EXTRUDADO EM FORMATO DE U.

  Isso substitui a borda OCA da revisao 8 inteira. A borda oca existia por um
  motivo so: dar a trava uma aresta de engate que fosse material de verdade, e
  ela custava saia 1,20 + canal 1,20 + perna 1,40 = 3,80 mm de largura, mais a
  nervura de aco de 1,20 x 8,6 mm (7,2:1) no molde. O dente faz o mesmo
  trabalho com uma parede so e SEM nervura nenhuma.

  O que a conta devolve: o footprint cai de 153,7 x 87,8 para 147,1 x 84,1 mm,
  e o molde perde a feicao mais cara que a revisao 8 tinha introduzido.

A SECAO DA BORDA, DE BAIXO PARA CIMA
  A parede reta sobe ate -8,00 (cotado do topo da borda). Ali um WEB horizontal
  de 1,00 mm atravessa para fora e a parede da borda sobe dele ate o topo.
  Entao:
    - a face de BAIXO do web, entre a parede do corpo e a face da borda, e o
      DENTE: anel horizontal de DENTE mm de largura. E material macico, com a
      parede da borda em cima dele - nao e aba flutuando (o erro da revisao 7).
    - a face de CIMA do web e um DEGRAU INTERNO. E ele que sustenta a placa de
      teca, e e ele que fixa a espessura dela: BORDA_H - WEB_T - BASE_T = 5,00.
    - entre o web e o topo sobra a BOCA, 7,00 mm de profundidade: e nela que a
      saia da tampa entra e e contra ela que o U veda.

  Molde: descendo por fora, a peca SO ESTREITA (borda -> dente -> corpo ->
  fundo); descendo por dentro, idem (boca -> degrau -> corpo). O dente nao e
  contra-saida: ele esta no topo, que e onde a cavidade e mais larga. Nenhuma
  gaveta, nenhuma extracao por arraste no corpo.

A ALGEBRA DO PASSO - nao mudou
  Com A = secao interna, H_n = altura externa, e_n = elevacao do piso interno e
  t = quanto o apoio da tampa fica ACIMA da borda:
      capacidade   A*(H_n - e_n) = n*600e3   ->  H_n = e_n + n*k
      passo        p_n = H_n + t  e  p_n = n*p_1
      juntando     e_n = n*e_1 + (n-1)*t
  Com e_1 = BASE_T = 2,0 o unico t que mantem o fundo rente nos quatro e
  t = -2,0: o apoio TEM de ficar 2,0 mm dentro da boca. Continua valendo.

A VEDACAO - o U, e por que ele e melhor que a corda
  O filete redondo da revisao 8 era um cordao macico esmagado contra a boca. O
  U calca na LINGUETA da saia da tampa (nao e colado, nao e encaixado a forca:
  ele abraca) e a perna de fora dele e que veda, radial, contra a boca. Tres
  ganhos: retencao mecanica (o U nao sai sozinho na lavagem), montagem sem
  cola, e uma perna fina comprimida ARO_COMP/ARO_PAR em vez de um cordao
  macico - menos forca para fechar com a mesma vedacao.

  O que o U NAO resolve: a tampa de teca. Uma lingueta de 0,80 mm em madeira
  quebra. A teca continua com corda redonda em friso usinado (secao TECA).

Uso:  python3 calculo-modular.py
"""
import math

RHO_PP, RHO_SIL = 0.905e-3, 1.15e-3

# ---- corpo ----
ASP     = 1.75      # footprint: comprimento / largura (frente estreita)
R_EXT   = 10.0      # raio de canto externo, na face externa da borda
M       = 60.0      # modulo: 600 ml por modulo
SAIDA   = 0.50      # saida por lado (graus)
BASE_T  = 2.00      # espessura do fundo - IGUAL nos quatro, trava o passo
WALL    = {1: 1.15, 2: 1.20, 3: 1.30, 4: 1.40}

# ---- a borda de 8 mm com dente (revisao 10) ----
BORDA_H   = 8.00    # do topo da borda ate a face de baixo do web = o DENTE
BORDA_PAR = 1.20    # parede da borda
WEB_T     = 1.00    # espessura do web horizontal que liga corpo e borda
ARRED     = BORDA_PAR / 2   # o topo da borda e uma MEIA-CANA: a parede tem
                            # 1,20, entao raio 0,60 nos dois lados consome
                            # ela inteira. Nao ha faixa chata para raio
                            # generoso + chanfro, como havia na borda oca.
DENTE_CHF = 0.40    # quebra-canto na quina de fora do dente (entrada da trava)

# ---- tampa: saia unica, lingueta e folgas ----
SAIA_T     = 1.20   # parede da saia da tampa
SAIA_FOLGA = 0.45   # folga entre a face externa da saia e a parede da boca
LING_T     = 0.80   # espessura da lingueta em que o U calca
RECUO      = (SAIA_T - LING_T) / 2      # recuo da lingueta em cada face
BANDEJA_FE = 0.50   # folga lateral do fundo do pote de cima dentro da saia
MARGEM     = 0.30   # sobra que o orcamento de largura tem de deixar

# ---- o aro em U, silicone extrudado ----
ARO_COMP  = 0.35    # compressao radial da perna de fora, por lado
ARO_PAR   = SAIA_FOLGA + RECUO + ARO_COMP   # perna do U - DERIVADA, nao chutada
ARO_FUNDO = 0.70    # fundo do U, abaixo da ponta da lingueta
ARO_GRIP  = 0.10    # interferencia do vao do U sobre a lingueta
ARO_FOLGA = 0.40    # folga entre o fundo do U e o degrau interno
E_SIL     = 2.5     # modulo do silicone ~50 ShA, MPa
MU_SIL    = 0.75    # atrito silicone / PP

# ---- o mini dente que segura o aro (revisao 11) ----
# Sem ele o U so e segurado pelo aperto de ARO_GRIP, e aperto de borracha cede
# com o tempo e com a lavagem. O dente e uma FARPA na ponta da lingueta: entra
# por uma rampa e sai por um degrau de 90°, e o U tem uma BOLSA na base do vao
# que recebe a farpa - assim ele encaixa e RELAXA, em vez de ficar esticado
# para sempre em cima dela (deformacao permanente e o que mata vedante).
DENTE_ARO   = 0.25    # quanto a farpa avanca, por face
DENTE_ARO_H = 0.50    # altura do degrau de 90° da farpa
DENTE_ARO_R = 0.35    # altura da rampa de entrada

# ---- nervuras sob o deck (revisao 11) ----
# "mais encorpada" nao e so sensacao: um deck de 1,50 mm vencendo 78 mm de vao
# e um painel mole. Nervura e o jeito barato de enrijecer - rigidez sobe com o
# quadrado do braco, peso sobe so com a area da nervura.
NERV_T     = 0.80   # espessura da nervura na raiz (53% do deck: abaixo dos 60%
                    # em que a marca de chupagem aparece na face de cima)
NERV_H     = 3.00   # altura. Limitada pelo DEGRAU interno do pote, nao por
                    # moldagem: mais que isso e a nervura da borda bate nele.
SAIDA_NERV = 3.00   # saida das nervuras, por face - o que a maquina do Ricardo
                    # pede. Numa nervura isso e de graca; na parede do pote nao
                    # (secao SAIDA DE EXTRACAO).
NERV_MARG  = 5.00   # quanto a nervura para antes da borda do deck

# ---- tampa de PP com trava de clipe ----
PP_DECK   = 1.50    # espessura do deck (o piso que recebe o pote de cima)
PP_FLANGE = 1.20    # espessura da aba que cruza por cima do topo da borda
TRAVA_N     = 2     # DUAS travas, uma por lado comprido (veio da referencia)
TRAVA_FRAC  = 0.58  # fracao do comprimento que cada trava cobre (referencia)
TRAVA_T     = 0.80  # espessura da trava
TRAVA_FOLGA = 0.30  # folga da trava sobre a face externa da borda
TRAVA_FARPA = 0.80  # quanto o gancho avanca sob o dente
TRAVA_RABO  = 6.00  # rabo abaixo do gancho, para o dedo
TRAVA_BULGE = 1.50  # quanto o rabo abre para fora, para dar pega
E_PP        = 1100.0  # modulo do PP randomico, MPa

# ---- teca ----
RHO_TECA  = 0.65e-3   # teca seca, g/mm3
TECA_FRISO = 0.60     # profundidade do friso usinado na lateral da placa
TECA_CORDA = 1.40     # corda de silicone da teca (a mesma secao do filete)
TECA_SOB   = 0.65     # quanto a corda sobra do friso. Com SAIA_FOLGA de
                      # 0,45 isso da 0,20 mm de compressao - o mesmo valor que
                      # a revisao 8 usava e que ja tinha numero de atrito.

PRES    = {1: 0.42, 2: 0.45, 3: 0.48, 4: 0.50}   # t/cm2 de fechamento
CICLO   = {1: 17, 2: 21, 3: 25, 4: 29}           # s

T = math.tan(math.radians(SAIDA))

# ---- cotas DERIVADAS da borda (nao digitadas) ----
Z_DENTE  = -BORDA_H                  # face de baixo do web = o dente
Z_DEGRAU = -(BORDA_H - WEB_T)        # face de cima do web = degrau interno
Z_MOD    = -BASE_T                   # plano modular: topo do deck / da placa
Z_DECK_B = Z_MOD - PP_DECK           # face de baixo do deck da tampa
TECA_ESP = Z_MOD - Z_DEGRAU          # a PLACA POUSA NO DEGRAU -> 5,00 mm
LING_H   = (Z_DECK_B - Z_DEGRAU) - ARO_FUNDO - ARO_FOLGA   # altura da lingueta
ARO_H    = LING_H + ARO_FUNDO        # altura total do U
ARO_VAO  = LING_T - ARO_GRIP         # vao livre do U (aperta na lingueta)
LING_PTA = LING_T + 2 * DENTE_ARO    # lingueta na farpa
ARO_BOLSA = LING_PTA + 0.10          # bolsa na base do vao, recebe a farpa
ARO_BOLSA_H = DENTE_ARO_H + DENTE_ARO_R + 0.10   # a bolsa cobre o degrau E a rampa
ARO_W    = 2 * ARO_PAR + LING_T      # largura total do U montado


def area(a, b, r):
    return a * b - (4 - math.pi) * r * r


def perim(a, b, r):
    return 2 * (a + b) - (8 - 2 * math.pi) * r


def raio(L, colar_l):
    """Curva paralela: deslocar a secao de d para dentro tira d do raio."""
    return max(R_EXT + (L - colar_l) / 2, 0.15)


def tronco(L0, L1, h, colar_l, dLW, passos=400):
    """Volume de um tronco entre duas secoes de retangulo arredondado."""
    if h <= 0:
        return 0.0
    s = 0.0
    for i in range(passos):
        L = L0 + (L1 - L0) * (i + .5) / passos
        s += area(L, L - dLW, raio(L, colar_l))
    return s * h / passos


def dente_necessario():
    """O dente nao e estetica: e o orcamento de largura.

    No plano modular, da face externa da borda ate onde o fundo do pote de cima
    pousa cabem, por lado: parede da borda + folga da saia + parede da saia +
    folga do fundo. Quem paga e o DENTE mais o que a saida ja estreitou no
    corpo do menor pote.
    """
    ganho = (M + BASE_T - BORDA_H) * T
    preciso = BORDA_PAR + SAIA_FOLGA + SAIA_T + BANDEJA_FE
    return preciso, ganho, preciso - ganho + MARGEM


PRECISO, GANHO, DENTE = dente_necessario()


def linha(colar_l):
    """colar_l e a medida MAXIMA do corpo (a face externa da borda)."""
    colar_w = colar_l / ASP
    dLW = colar_l - colar_w
    corpo_l = colar_l - 2 * DENTE                # corpo reto, abaixo do dente
    boca    = colar_l - 2 * BORDA_PAR            # furo no plano do topo
    potes = []
    for n in (1, 2, 3, 4):
        w, H = WALL[n], n * M + BASE_T
        z_dente  = H - BORDA_H                   # face de baixo do web
        z_degrau = z_dente + WEB_T               # face de cima do web
        corpo_z = lambda z: corpo_l - 2 * (z_dente - z) * T
        boca_z  = lambda z: boca - 2 * (H - z) * T
        base_ext = corpo_z(0.0)                  # fundo: a medida mais estreita

        def vol_com(e):
            piso = BASE_T + e
            return (tronco(corpo_z(piso) - 2 * w, corpo_z(z_degrau) - 2 * w,
                           z_degrau - piso, colar_l, dLW)
                    + tronco(boca_z(z_degrau), boca, BORDA_H - WEB_T, colar_l, dLW))

        lo, hi = -1.0, 16.0
        for _ in range(40):
            e = (lo + hi) / 2
            lo, hi = (e, hi) if vol_com(e) > n * 600e3 else (lo, e)
        e = (lo + hi) / 2

        # peso: fundo + parede reta + web + parede da borda
        med_corpo = (corpo_z(BASE_T) + corpo_z(z_degrau)) / 2 - w
        med_boca  = (boca_z(z_degrau) + boca) / 2
        bore_corpo = corpo_z(z_dente) - 2 * w
        vol_mat = (area(base_ext, base_ext - dLW, raio(base_ext, colar_l)) * BASE_T
                   + perim(med_corpo, med_corpo - dLW, raio(med_corpo, colar_l))
                   * (z_dente - BASE_T) * w
                   + (area(colar_z := corpo_z(z_dente) + 2 * DENTE,
                           colar_z - dLW, raio(colar_z, colar_l))
                      - area(bore_corpo, bore_corpo - dLW, raio(bore_corpo, colar_l)))
                   * WEB_T
                   + perim(med_boca + BORDA_PAR, med_boca + BORDA_PAR - dLW,
                           raio(med_boca + BORDA_PAR, colar_l))
                   * (BORDA_H - WEB_T) * BORDA_PAR)
        potes.append(dict(n=n, cap=n * 600, colar_l=colar_l, colar_w=colar_w,
                          corpo_l=corpo_l, corpo_w=corpo_l - dLW,
                          base_ext=base_ext, boca=boca, H=H, passo=n * M,
                          elev=e, vol=vol_com(e) / 1e3, peso=vol_mat * RHO_PP,
                          w=w, z_dente=z_dente, z_degrau=z_degrau, dLW=dLW,
                          bore_corpo=bore_corpo))
    return potes


def footprint():
    """Borda em que o maior pote fecha 2400 ml com o fundo no nivel."""
    lo, hi = 110.0, 230.0
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if linha(mid)[3]['elev'] > 0.0 else (mid, hi)
    return (lo + hi) / 2


def verifica(potes):
    """As relacoes que, se quebrarem, entregam uma peca que PARECE certa.

    Toda revisao deste projeto quebrou pelo menos uma relacao entre duas pecas
    sem que nenhuma peca estivesse errada sozinha. Estas sao as que importam.
    """
    p, erros = potes[0], []
    boca, colar_l, corpo_l = p['boca'], p['colar_l'], p['corpo_l']

    def exige(cond, txt):
        erros.append(txt) if not cond else None
        print(f"  [{'ok ' if cond else 'FALHA'}] {txt}")

    print("\nVERIFICACAO")
    folga = (boca - p['base_ext']) / 2
    exige(folga >= SAIA_FOLGA + SAIA_T + BANDEJA_FE,
          f"no plano modular a boca ({boca:.2f}) recebe o fundo do pote de cima "
          f"({p['base_ext']:.2f}): {folga:.2f} >= {SAIA_FOLGA + SAIA_T + BANDEJA_FE:.2f} mm/lado")
    exige(abs((ARO_PAR - SAIA_FOLGA - RECUO) - ARO_COMP) < 1e-9,
          f"a perna do U fecha a folga e comprime {ARO_COMP:.2f} mm/lado "
          f"({ARO_COMP / ARO_PAR * 100:.0f}% da perna de {ARO_PAR:.2f})")
    exige(Z_DECK_B - ARO_H > Z_DEGRAU,
          f"o fundo do U ({Z_DECK_B - ARO_H:+.2f}) nao bate no degrau interno "
          f"({Z_DEGRAU:+.2f}): {Z_DECK_B - ARO_H - Z_DEGRAU:.2f} mm de folga")
    exige(abs(Z_DEGRAU + TECA_ESP - Z_MOD) < 1e-9,
          f"a placa de teca de {TECA_ESP:.2f} mm POUSA no degrau e o topo dela cai "
          f"em {Z_MOD:+.2f} - o plano modular")
    exige(TRAVA_FARPA < DENTE - DENTE_CHF,
          f"o gancho avanca {TRAVA_FARPA:.2f} mm sob um dente de {DENTE:.2f} "
          f"({TRAVA_FARPA / (DENTE - DENTE_CHF) * 100:.0f}% do dente util)")
    fora = [p['base_ext'], corpo_l, colar_l]
    exige(all(a <= b + 1e-9 for a, b in zip(fora, fora[1:])),
          f"por fora so estreita descendo: {colar_l:.1f} -> {corpo_l:.1f} -> "
          f"{p['base_ext']:.1f} (sem contra-saida, sem gaveta)")
    dentro = [p['bore_corpo'], boca]
    exige(all(a <= b + 1e-9 for a, b in zip(dentro, dentro[1:])),
          f"por dentro so estreita descendo: {boca:.1f} -> {p['bore_corpo']:.1f}")
    exige(DENTE_ARO_H + DENTE_ARO_R < LING_H,
          f"a farpa ({DENTE_ARO_H:.2f} de degrau + {DENTE_ARO_R:.2f} de rampa) cabe "
          f"na lingueta de {LING_H:.2f} mm")
    exige(ARO_BOLSA_H >= DENTE_ARO_H + DENTE_ARO_R,
          f"a bolsa do U ({ARO_BOLSA_H:.2f}) cobre o degrau E a rampa da farpa "
          f"({DENTE_ARO_H + DENTE_ARO_R:.2f}): o silicone RELAXA em vez de esticar")
    exige(ARO_PAR - (DENTE_ARO + 0.05) >= 0.50,
          f"na bolsa a perna do U afina para "
          f"{ARO_PAR - (DENTE_ARO + 0.05):.2f} mm (minimo 0,50 para extrudar)")
    saia_o = p['boca'] - 2 * SAIA_FOLGA
    deck_u = saia_o - 2 * SAIA_T
    nv = nervuras(deck_u, deck_u - p['dLW'])
    exige(Z_DECK_B - NERV_H > Z_DEGRAU,
          f"a nervura ({Z_DECK_B - NERV_H:+.2f}) nao bate no degrau interno "
          f"({Z_DEGRAU:+.2f}): {Z_DECK_B - NERV_H - Z_DEGRAU:.2f} mm de folga")
    exige(nv['t_pta'] >= 0.40,
          f"com {SAIDA_NERV:.0f}° por face a nervura chega na ponta com "
          f"{nv['t_pta']:.2f} mm (abaixo de 0,40 nao enche)")
    exige(NERV_T / PP_DECK <= 0.60,
          f"nervura de {NERV_T:.2f} sobre deck de {PP_DECK:.2f} = "
          f"{NERV_T / PP_DECK * 100:.0f}% (acima de 60% marca chupagem por fora)")
    exige(all(q['elev'] >= -1e-6 for q in potes),
          "elevacao de fundo >= 0 nos quatro (nenhum pote pede fundo negativo)")
    for combo in ((1, 1, 1, 1), (2, 2), (1, 1, 2), (1, 3), (4,)):
        if sum(combo) * M != 4 * M:
            erros.append("empilhamento")
    exige(not any(e == "empilhamento" for e in erros),
          f"toda combinacao empilhada fecha {4 * M:.0f} mm")
    if erros:
        raise SystemExit("\n  VERIFICACAO REPROVOU: " + " | ".join(erros))
    return True


def aninha(p, s, boca, colar_l):
    """Quanto cada pote a mais soma na pilha, com saida s graus.

    Varredura do perfil externo do pote de cima contra o interno do de baixo.
    Formula fechada aqui ja deu numero sem sentido uma vez.
    """
    t = math.tan(math.radians(s))
    H, zd, zg = p['H'], p['z_dente'], p['z_degrau']

    def fora(y):
        if y <= zd:
            return (p['corpo_l'] - 2 * (zd - y) * t) / 2
        return (colar_l - 2 * (H - y) * t) / 2

    def dentro(d):
        if d <= BORDA_H - WEB_T:
            return (boca - 2 * d * t) / 2
        return (p['corpo_l'] - 2 * p['w']
                - 2 * (d - (BORDA_H - WEB_T)) * t) / 2

    lo, hi = 0.0, H
    for _ in range(50):
        mid = (lo + hi) / 2
        ok = all(fora(y) <= dentro(mid - y) + 1e-9
                 for y in [mid - d * mid / 120 for d in range(121)] if 0 <= y <= H)
        lo, hi = (mid, hi) if ok else (lo, mid)
    return H - lo


def nervuras(deck_l, deck_w):
    """Grade de nervuras sob o deck: posicoes, comprimento, peso e rigidez.

    A conta de rigidez e a de uma secao T: a nervura so serve se o deck andar
    junto com ela, e quem faz isso e a aba do T - por isso o ganho nao e o
    I da nervura sozinha, e sim o do conjunto em torno do centroide comum.
    """
    uso_l, uso_w = deck_l - 2 * NERV_MARG, deck_w - 2 * NERV_MARG
    n_trans = 5                      # nervuras ao longo da LARGURA (cortam o comprimento)
    n_long = 3                       # nervuras ao longo do COMPRIMENTO
    px, py = uso_l / (n_trans - 1), uso_w / (n_long - 1)
    xs = [-uso_l / 2 + i * px for i in range(n_trans)]
    ys = [-uso_w / 2 + i * py for i in range(n_long)]
    t_pta = NERV_T - 2 * NERV_H * math.tan(math.radians(SAIDA_NERV))
    t_med = (NERV_T + t_pta) / 2
    comp = n_trans * uso_w + n_long * uso_l
    vol = comp * t_med * NERV_H

    # secao T equivalente, por passo da grade (usa o passo menor, o que manda)
    p = min(px, py)
    a_f, y_f = p * PP_DECK, PP_DECK / 2
    a_n, y_n = t_med * NERV_H, PP_DECK + NERV_H / 2
    yb = (a_f * y_f + a_n * y_n) / (a_f + a_n)
    I_t = (p * PP_DECK ** 3 / 12 + a_f * (yb - y_f) ** 2
           + t_med * NERV_H ** 3 / 12 + a_n * (y_n - yb) ** 2)
    I_0 = p * PP_DECK ** 3 / 12
    return dict(xs=xs, ys=ys, px=px, py=py, t_pta=t_pta, t_med=t_med,
                comp=comp, vol=vol, peso=vol * RHO_PP, ganho=I_t / I_0,
                celula=(px, py), uso=(uso_l, uso_w))


def cenario(saida_graus):
    """A linha inteira resolvida com outra saida de extracao."""
    global T, DENTE, PRECISO, GANHO
    T0, D0, P0, G0 = T, DENTE, PRECISO, GANHO
    T = math.tan(math.radians(saida_graus))
    PRECISO, GANHO, DENTE = dente_necessario()
    pots = linha(footprint())
    an = aninha(pots[3], saida_graus, pots[0]['boca'], pots[0]['colar_l'])
    T, DENTE, PRECISO, GANHO = T0, D0, P0, G0
    return pots, an


def main():
    potes = linha(footprint())
    p0 = potes[0]
    dLW, boca = p0['dLW'], p0['boca']
    colar_l, colar_w = p0['colar_l'], p0['colar_w']

    print("=" * 79)
    print("REVISAO 10 - borda de 8 mm com DENTE, tampa de uma saia, aro em U")
    print("=" * 79)
    print(f"Corpo (medida maxima, face externa da borda) {colar_l:.1f} x {colar_w:.1f} mm")
    print(f"  (era 153,7 x 87,8 na revisao 8 - a borda oca custava 5,60 mm/lado,")
    print(f"   o dente custa {DENTE:.2f})")
    print(f"Corpo reto (onde vai o IML) {p0['corpo_l']:.1f} x {p0['corpo_w']:.1f} mm | "
          f"canto R{R_EXT:.0f} | saida {SAIDA}°/lado | modulo {M:.0f} mm")
    print(f"Borda {BORDA_H:.1f} mm ate o dente | dente {DENTE:.2f} mm/lado | "
          f"boca {boca:.1f} mm | fundo {BASE_T:.1f} mm nos quatro\n")

    print(f"{'':>8} {'H total':>8} {'passo':>6} {'corpo reto':>14} {'fundo ext':>10} "
          f"{'elev.fundo':>10} {'parede':>7} {'V':>6} {'peso':>7}")
    for p in potes:
        print(f"{p['cap']:>6}ml {p['H']:>8.1f} {p['passo']:>6.0f} "
              f"{p['corpo_l']:>7.1f}x{p['corpo_w']:<6.1f} {p['base_ext']:>10.2f} "
              f"{p['elev']:>10.2f} {p['w']:>7.2f} {p['vol']:>5.0f} {p['peso']:>6.1f}g")
    print("  (peso analitico - perimetro x espessura por faixa. gera-3d.py MEDE na")
    print("   malha fechada e e esse o numero que vai publicado.)")

    print("\nA BORDA, de cima para baixo (secao no meio de um lado, por lado):")
    print(f"  topo .............. MEIA-CANA de raio {ARRED:.2f} - a parede de "
          f"{BORDA_PAR:.2f} vira um semicirculo")
    print(f"                      (a borda oca tinha faixa chata de 2,0 mm; uma parede")
    print(f"                       so nao tem onde por faixa chata, e a meia-cana e")
    print(f"                       tambem a entrada que a saia da tampa precisa)")
    print(f"  parede da borda ... {BORDA_PAR:.2f} mm, desce {BORDA_H - WEB_T:.2f} mm, "
          f"faz a boca de {boca:.1f} mm")
    print(f"  web horizontal .... {WEB_T:.2f} mm de espessura, {DENTE + WALL[1]:.2f} mm "
          f"de largura - liga a borda ao corpo")
    print(f"  DENTE ............. face de BAIXO do web, {DENTE:.2f} mm/lado, a "
          f"{BORDA_H:.1f} mm do topo. E aqui que a trava engata.")
    print(f"  DEGRAU INTERNO .... face de CIMA do web, {DENTE + WALL[1] - BORDA_PAR:.2f} mm/lado, "
          f"a {BORDA_H - WEB_T:.1f} mm do topo. E ele que segura a placa de teca.")
    print(f"  corpo reto ........ {WALL[1]:.2f} a {WALL[4]:.2f} mm de parede, "
          f"secao constante ate o fundo")

    print("\nOrcamento de largura - e ele que dimensiona o DENTE:")
    print(f"  preciso por lado: parede da borda {BORDA_PAR:.2f} + folga da saia "
          f"{SAIA_FOLGA:.2f} + parede da saia {SAIA_T:.2f} + folga do fundo "
          f"{BANDEJA_FE:.2f} = {PRECISO:.2f} mm")
    print(f"  a saida ja estreita {GANHO:.3f} mm no corpo do 600 ml")
    print(f"  logo dente = {PRECISO:.2f} - {GANHO:.3f} + margem {MARGEM:.2f} = {DENTE:.2f} mm")
    print(f"  (voce pediu ~3 mm. A conta pede {DENTE:.2f}: os {DENTE - 3:.2f} mm a mais sao a margem.)")

    verifica(potes)

    print("\nEmpilhamento (tudo tem que dar %d mm):" % (4 * M))
    for combo in [(1, 1, 1, 1), (2, 2), (1, 1, 2), (1, 3), (4,)]:
        total = sum(combo) * M
        print("  " + " + ".join(f"{c * 600}ml" for c in combo).ljust(34)
              + f"= {total:.0f} mm  {'OK' if abs(total - 4 * M) < 1e-9 else 'FALHA'}")

    print("\nMolde do corpo:")
    print(f"  por fora, descendo: {colar_l:.1f} (borda) -> {p0['corpo_l']:.1f} (corpo) "
          f"-> {potes[3]['base_ext']:.1f} (fundo do 2,4 L) - so estreita.")
    print(f"  por dentro, descendo: {boca:.1f} (boca) -> {p0['bore_corpo']:.1f} "
          f"(corpo) - so estreita.")
    print( "  O DENTE NAO E CONTRA-SAIDA: ele esta no topo, que e onde a cavidade")
    print( "  ja e mais larga. A peca sai reta. Sem gaveta, sem extracao por arraste.")
    print( "  O QUE SAIU DO ORCAMENTO DO MOLDE: a nervura do canal da revisao 8,")
    print( "  1,20 x 8,6 mm (7,2:1) continua nos 466 mm de perimetro. Nao existe mais.")
    print(f"  IML: corpo de secao constante {p0['corpo_l']:.1f} x {p0['corpo_w']:.1f}, "
          f"{SAIDA}°/lado, do dente ao fundo - {p0['z_dente']:.0f} mm no 600 ml.")

    # ---- o aro em U ----
    saia_o = boca - 2 * SAIA_FOLGA                 # face externa da saia
    ling_o = saia_o - 2 * RECUO                    # face externa da lingueta
    per_u = perim(ling_o, ling_o - dLW, raio(ling_o, colar_l))
    sec_u = ARO_W * ARO_H - ARO_VAO * LING_H
    massa_u = per_u * sec_u * RHO_SIL
    I_lab = ARO_PAR ** 3 / 12
    F_lab = 3 * E_SIL * I_lab * ARO_COMP / ARO_H ** 3      # N/mm de perimetro
    p_cont = F_lab / (ARO_PAR / 2)
    eps_lab = 3 * ARO_PAR * ARO_COMP / (2 * ARO_H ** 2)

    print("\n" + "=" * 79)
    print("O ARO EM U - silicone extrudado, calcado na lingueta da tampa")
    print("=" * 79)
    print(f"  secao do U ........ {ARO_W:.2f} x {ARO_H:.2f} mm, perna {ARO_PAR:.2f}, "
          f"fundo {ARO_FUNDO:.2f}, vao {ARO_VAO:.2f}")
    print(f"  lingueta da tampa . {LING_T:.2f} x {LING_H:.2f} mm, recuada {RECUO:.2f} "
          f"em cada face da saia de {SAIA_T:.2f}")
    print(f"  aperto na lingueta  {ARO_GRIP:.2f} mm - o U nao e colado, ele ABRACA")
    print(f"  compressao radial . {ARO_COMP:.2f} mm/lado contra a parede da boca "
          f"({ARO_COMP / ARO_PAR * 100:.0f}% da perna)")
    print(f"  perimetro ......... {per_u:.0f} mm | secao {sec_u:.2f} mm2 | "
          f"{massa_u:.1f} g de silicone")
    print(f"  forca do labio .... {F_lab * 1000:.2f} N/m de perimetro -> "
          f"{F_lab * per_u / 9.81 * 1000:.0f} gf radiais no total")
    print(f"  pressao de contato  {p_cont * 1000:.1f} kPa (coluna d'agua de 100 mm "
          f"= 1 kPa: sobra {p_cont * 1000:.0f}x)")
    print(f"  deformacao do labio {eps_lab * 100:.1f}% (silicone rompe acima de 200%)")
    print( "  Modelo de viga engastada para o labio. E o limite INFERIOR: se o labio")
    print( "  ficar confinado em vez de dobrar, a forca sobe muito. O numero que vale")
    print( "  e o do prototipo com o perfil real do extrusor.")
    print(f"  QUEM SEGURA A TAMPA NAO E O ARO, E A TRAVA. O aro so veda.")
    print(f"  TOLERANCIA: {ARO_COMP:.2f} mm de interferencia contra +-0,15 de molde")
    print(f"  nas duas pecas. E a cota mais apertada da linha - pede controle de")
    print(f"  processo na boca, nao so no desenho.")

    # ---- tampa de PP com trava ----
    plug_o = saia_o
    deck_util = saia_o - 2 * SAIA_T
    trava_larg = TRAVA_FRAC * colar_l
    tampa_o = colar_l + 2 * (TRAVA_FOLGA + TRAVA_T)
    trava_o = colar_w + 2 * (TRAVA_FOLGA + TRAVA_T + TRAVA_BULGE)
    I_tr = trava_larg * TRAVA_T ** 3 / 12
    braco = BORDA_H
    F_tr = 3 * E_PP * I_tr * TRAVA_FARPA / braco ** 3
    eps = 3 * TRAVA_T * TRAVA_FARPA / (2 * braco ** 2)
    alav = (braco + TRAVA_RABO) / braco

    print("\n" + "=" * 79)
    print("TAMPA DE PP - uma saia so, aba por cima da borda, 2 travas de clipe")
    print("=" * 79)
    print(f"  deck .............. topo em {Z_MOD:+.2f} (o plano modular), "
          f"{PP_DECK:.2f} mm de espessura")
    print(f"  saia .............. {SAIA_T:.2f} mm, face externa em {saia_o:.1f} mm "
          f"(folga {SAIA_FOLGA:.2f} na boca de {boca:.1f})")
    print(f"  apoio do pote de cima: {deck_util:.1f} mm recebe o fundo de "
          f"{p0['base_ext']:.2f} -> {(deck_util - p0['base_ext']) / 2:+.2f} mm/lado")
    print(f"  aba ............... {PP_FLANGE:.2f} mm, cruza por cima do topo da borda; "
          f"e ela que define a altura da tampa")
    print(f"  travas: {TRAVA_N}, uma por lado COMPRIDO, {trava_larg:.0f} mm cada "
          f"({TRAVA_FRAC * 100:.0f}% do comprimento)")
    print(f"  medida maxima: {tampa_o:.1f} x {trava_o:.1f} mm (o rabo so cresce a largura)")
    print(f"  gancho: avanca {TRAVA_FARPA:.2f} mm sob o dente de {DENTE:.2f} mm")
    print(f"  (na revisao 8 a aresta tinha 1,20 mm e o gancho usava 67% dela. Agora")
    print(f"   o dente tem {DENTE:.2f} e o gancho usa {TRAVA_FARPA / DENTE * 100:.0f}%:")
    print(f"   sobra dente para a tolerancia de molde, que antes nao sobrava.)")
    print(f"  braco de {braco:.1f} mm (a trava e tao alta quanto a borda) -> fechar pede")
    print(f"  {F_tr / 9.81:.1f} kgf por trava, uma de cada vez; deformacao {eps * 100:.2f}%")
    print(f"  abrir pelo rabo: alavanca {alav:.1f}x -> {F_tr / 9.81 / alav:.1f} kgf no dedo")
    print(f"  (a trava afinou de 1,00 para {TRAVA_T:.2f} mm porque o braco encurtou de")
    print(f"   10 para {braco:.0f} mm, e forca vai com 1/L^3: sem afinar daria "
          f"{3 * E_PP * trava_larg * 1.0 ** 3 / 12 * TRAVA_FARPA / braco ** 3 / 9.81:.1f} kgf.)")

    # ---- tampa de teca ----
    teca_l = boca - 2 * SAIA_FOLGA
    a_teca = area(teca_l, teca_l - dLW, raio(teca_l, colar_l))
    per_teca = perim(teca_l, teca_l - dLW, raio(teca_l, colar_l))
    corda_teca = per_teca * math.pi * (TECA_CORDA / 2) ** 2 * RHO_SIL
    cp_teca = TECA_SOB - SAIA_FOLGA
    print("\n" + "=" * 79)
    print("TAMPA DE TECA - a placa POUSA no degrau interno")
    print("=" * 79)
    print(f"  placa {teca_l:.1f} x {teca_l - dLW:.1f} x {TECA_ESP:.2f} mm, "
          f"{a_teca * TECA_ESP * RHO_TECA:.0f} g em teca seca")
    print(f"  a espessura NAO foi escolhida: {TECA_ESP:.2f} = borda {BORDA_H:.1f} - web "
          f"{WEB_T:.1f} - fundo {BASE_T:.1f}.")
    print(f"  A placa desce ate o degrau e o topo dela cai exatamente no plano")
    print(f"  modular. O peso do pote de cima vai para o DEGRAU atraves da madeira,")
    print(f"  em compressao - a placa nao trabalha em flexao. Na revisao 8 ela tinha")
    print(f"  8,0 mm e vencia o vao sozinha.")
    print(f"  vedacao: friso usinado de {TECA_FRISO:.2f} mm na lateral + corda de "
          f"{TECA_CORDA:.2f} mm, comprime {cp_teca:.2f} mm/lado")
    print(f"  {corda_teca:.1f} g de silicone, perimetro {per_teca:.0f} mm")
    forma, mu = 1.8, 0.75
    pres_t = E_SIL * (cp_teca / TECA_CORDA) * forma
    larg_t = 0.9 * math.sqrt(TECA_CORDA * cp_teca)
    F_teca = mu * pres_t * per_teca * larg_t / 9.81
    print(f"  retencao: so atrito -> {F_teca:.1f} kgf para arrancar reto, "
          f"{F_teca / 6:.1f} descascando um canto")
    print( "  (e so o atrito que segura a placa: ela nao tem trava. O mesmo modelo")
    print(f"   da revisao 4, agora com silicone (E={E_SIL:.1f} MPa) em vez de TPE.)")

    a_plug = area(teca_l, teca_l - dLW, raio(teca_l, colar_l))
    print("\n  Capacidade de borda x capacidade util (a tampa entra na boca):")
    print(f"    {'tampa':<8} {'desce':>7} {'desloca':>9} | " +
          "  ".join(f"{q['cap']:>5} ml" for q in potes))
    for nome, prof in (('teca', BASE_T + TECA_ESP),
                       ('PP', BASE_T + PP_DECK + LING_H + ARO_FUNDO)):
        desloc = a_plug * prof / 1e3
        print(f"    {nome:<8} {prof:>6.1f}mm {desloc:>8.0f} ml | " +
              "  ".join(f"{q['cap'] - desloc:>5.0f} ml" for q in potes))
    print(f"    A placa de teca desceu de 8,0 para {TECA_ESP:.1f} mm, entao ela come")
    print(f"    {a_plug * (BASE_T + 8.0) / 1e3 - a_plug * (BASE_T + TECA_ESP) / 1e3:.0f} ml "
          f"a MENOS que na revisao 8 - no 600 ml, de 19% para "
          f"{a_plug * (BASE_T + TECA_ESP) / 1e3 / 6:.0f}%.")
    print( "    Capacidade nominal continua sendo de BORDA, como manda o setor.")
    print( "  POR QUE A TECA NAO LEVA O U: o U calca numa lingueta de "
          f"{LING_T:.2f} mm.")
    print( "  Em madeira essa lingueta quebra. A teca fica com corda redonda em friso,")
    print( "  que e o que ela ja tinha. Quem quiser um vedante so na linha inteira")
    print( "  precisa de um aro de PP carregando o U, com a placa encaixada nele.")

    # ---- nervuras sob o deck ----
    nv = nervuras(deck_util, deck_util - dLW)
    eps_strip = 3 * LING_T * DENTE_ARO / (2 * LING_H ** 2)
    print("\n" + "=" * 79)
    print("NERVURAS SOB O DECK - a tampa 'encorpada'")
    print("=" * 79)
    print(f"  grade {len(nv['xs'])} x {len(nv['ys'])} dentro de "
          f"{nv['uso'][0]:.0f} x {nv['uso'][1]:.0f} mm (margem {NERV_MARG:.1f} da borda)")
    print(f"  celula {nv['px']:.1f} x {nv['py']:.1f} mm | nervura {NERV_T:.2f} na raiz, "
          f"{nv['t_pta']:.2f} na ponta, {NERV_H:.2f} de altura")
    print(f"  saida {SAIDA_NERV:.0f}° por face - numa nervura isso nao custa nada: "
          f"{NERV_T - nv['t_pta']:.2f} mm de diferenca em {NERV_H:.1f} mm")
    print(f"  {nv['comp']:.0f} mm de nervura | {nv['vol'] / 1e3:.2f} cm3 | "
          f"+{nv['peso']:.2f} g na tampa ({nv['peso'] / 21.0 * 100:.0f}%)")
    print(f"  RIGIDEZ: secao T de passo {min(nv['px'], nv['py']):.1f} mm -> "
          f"I sobe {nv['ganho']:.1f}x contra o deck liso")
    print(f"  (flecha cai na mesma proporcao: o deck de {PP_DECK:.2f} mm vencendo "
          f"{deck_util - dLW:.0f} mm")
    print(f"   de vao passa a flechar {1 / nv['ganho']:.2f} do que flechava.)")
    print(f"  altura limitada pelo DEGRAU do pote, nao por moldagem: a nervura para "
          f"em {Z_DECK_B - NERV_H:+.2f}")
    print(f"  e o degrau esta em {Z_DEGRAU:+.2f}. Para subir a nervura teria de "
          f"subir a borda.")
    print(f"  CUSTO ESCONDIDO: as nervuras tiram {nv['vol'] / 1e3:.1f} ml da "
          f"capacidade util - 0,2% no 600 ml.")

    print("\n" + "=" * 79)
    print("O MINI DENTE QUE SEGURA O ARO")
    print("=" * 79)
    print(f"  farpa na PONTA da lingueta: {DENTE_ARO:.2f} mm por face "
          f"({LING_T:.2f} -> {LING_PTA:.2f} mm)")
    print(f"  entra por rampa de {DENTE_ARO_R:.2f} mm "
          f"({math.degrees(math.atan2(DENTE_ARO, DENTE_ARO_R)):.0f}° da vertical) e sai "
          f"por degrau de 90° de {DENTE_ARO_H:.2f} mm")
    print(f"  o U tem BOLSA de {ARO_BOLSA:.2f} x {ARO_BOLSA_H:.2f} mm na base do vao "
          f"(cobre o degrau E a rampa)")
    print(f"  na bolsa a perna do U afina de {ARO_PAR:.2f} para "
          f"{ARO_PAR - DENTE_ARO - 0.05:.2f} mm - ainda extrudavel")
    print(f"  -> montado, o silicone RELAXA em cima da farpa. Sem a bolsa ele ficaria")
    print(f"     esticado {2 * DENTE_ARO:.2f} mm para sempre, e deformacao permanente")
    print(f"     e exatamente o que mata vedante de borracha em 2 anos de armario.")
    print(f"  para sair, o vao de {ARO_VAO:.2f} tem de abrir ate {LING_PTA:.2f}: "
          f"{2 * DENTE_ARO + ARO_GRIP:.2f} mm de esticamento, contra os "
          f"{ARO_GRIP:.2f} mm de aperto que seguravam antes")
    print(f"  EXTRACAO DA TAMPA: a farpa e contra-saida de {DENTE_ARO:.2f} mm numa "
          f"lingueta de {LING_T:.2f} x {LING_H:.2f}")
    print(f"  que flexiona. Deformacao de fibra na saida: {eps_strip * 100:.1f}% "
          f"(PP randomico escoa perto de 8%).")
    print(f"  E a segunda contra-saida da tampa, junto com o gancho da trava - as "
          f"duas por arraste,")
    print( "  nenhuma por gaveta.")

    # ---- saida de extracao: o pedido de 3° contra a parede reta ----
    print("\n" + "=" * 79)
    print("SAIDA DE EXTRACAO - o pedido de 3° contra a parede reta")
    print("=" * 79)
    print("  O Ricardo pediu pelo menos 3° para a peca sair legal da maquina dele.")
    print("  Nas NERVURAS, nos BOLSOS e na CALHA isso ja esta aplicado e nao custa")
    print("  nada. Na PAREDE DO POTE custa o produto inteiro, e o numero mostra")
    print("  por que - o fundo externo do 2,4 L contra a borda dele:\n")
    print(f"  {'saida':>6} {'footprint':>15} {'fundo do 2,4 L':>15} {'conicidade':>11} "
          f"{'pilha de 6':>11} {'IML':>6}")
    for sg in (0.5, 1.0, 1.5, 2.0, 3.0):
        pots, an = cenario(sg)
        p4 = pots[3]
        conic = (p4['corpo_l'] - p4['base_ext']) / p4['corpo_l']
        pilha = 5 * an + p4['H']
        iml = 'ok' if conic < 0.03 else 'NAO'
        marca = '  <- hoje' if abs(sg - SAIDA) < 1e-9 else ''
        print(f"  {sg:>5.1f}° {pots[0]['colar_l']:>8.1f} x {pots[0]['colar_w']:<5.1f} "
              f"{p4['base_ext']:>13.1f} mm {conic:>10.1%} {pilha:>9.0f} mm "
              f"{iml:>6}{marca}")
    print( "\n  A conicidade e o que o olho ve: no 2,4 L, 3° deixam o fundo 24 mm mais")
    print( "  estreito que a boca em 242 mm de altura. Isso nao e 'parede reta com")
    print( "  cantos arredondados' - e um balde. E o IML pede secao constante: com")
    print( "  3° a etiqueta enruga ou descola na base.")
    print( "  O QUE RESOLVE EXTRACAO SEM SAIDA, e ja esta no projeto desde a revisao 5:")
    print( "    - cavidade e macho POLIDOS A2 ou melhor (textura e que pede 1° a cada")
    print( "      0,025 mm de profundidade, e e ela que gera a maioria das regras de 3°)")
    print( "    - extracao por PLACA IMPULSORA, nao por pinos: empurra o rodape inteiro")
    print( "    - VALVULA DE AR no topo do macho, para quebrar o vacuo")
    print(f"    - forca de extracao estimada em ~5 kN no 2,4 L contra ~62 kN")
    print( "      disponiveis numa 380 t: o gargalo nao e forca, e vacuo e risco de")
    print( "      arranhar a parede polida.")
    print( "\n  MAS A SAIDA NAO PRECISA SER A MESMA NOS QUATRO. Cada tamanho tem molde")
    print( "  proprio, e so a BORDA e comum - a saida so decide quanto a parede estreita")
    print( "  descendo. Conicidade (quanto o fundo e mais estreito que o corpo) por")
    print( "  tamanho e por saida:\n")
    print(f"  {'saida':>6} " + " ".join(f"{q['cap']:>8} ml" for q in potes))
    for sg in (0.5, 1.0, 1.5, 2.0, 3.0):
        pots, _ = cenario(sg)
        linha_txt = f"  {sg:>5.1f}° "
        for q in pots:
            c = (q['corpo_l'] - q['base_ext']) / q['corpo_l']
            linha_txt += f"{c:>8.1%}{'*' if c < 0.03 else ' '} "
        print(linha_txt)
    print( "  (* dentro de 3% de conicidade, que e onde o IML e o 'parede reta' aguentam)")
    print( "\n  Le-se assim: o 600 ml aguenta ate 2,0° sem deixar de parecer reto; o")
    print( "  2,4 L nao passa de 0,5°. Se a ferramentaria disser que nao tira a peca,")
    print( "  da para dar MAIS saida aos pequenos e menos aos grandes - mas o 2,4 L,")
    print( "  que e o mais fundo e portanto o mais dificil, e justamente o que menos")
    print( "  tolera. Nele nao ha saida: tem de sair por polimento, placa impulsora e")
    print( "  valvula de ar.")
    print( "\n  RECOMENDACAO: manter 0,5° na parede dos quatro e levar 3° para tudo o")
    print( "  que e FEICAO - nervura, bolso, calha, trilho, rabo da trava, farpa. Levar")
    print( "  a tabela acima para a ferramentaria ANTES de fechar o molde: se eles")
    print( "  disserem que 0,5° nao sai, isso muda o produto, nao so o molde, e a")
    print( "  decisao e sua, nao minha.")

    # ---- injecao ----
    a_corpo = area(colar_l, colar_w, R_EXT) / 100
    a_tampa = area(tampa_o, trava_o, R_EXT) / 100
    print("\n" + "=" * 79)
    print("INJECAO (2 cavidades)")
    print("=" * 79)
    print(f"  area projetada do CORPO {a_corpo:.0f} cm2 | da TAMPA {a_tampa:.0f} cm2")
    print(f"  (era 134 cm2 no corpo da revisao 8: o footprint menor tirou "
          f"{134 - a_corpo:.0f} cm2)")
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

    r_corpo = R_EXT - DENTE
    print("\nRigidez do painel reto - cada tamanho contra ELE MESMO na revisao 8:")
    print(f"  (rev 8: corpo 142,5, canto R4,4, painel de 133,7 mm, altura H-16;")
    print(f"   rev 10: corpo {p0['corpo_l']:.1f}, canto R{r_corpo:.1f}, painel de "
          f"{p0['corpo_l'] - 2 * r_corpo:.1f} mm, altura H-{BORDA_H + BASE_T:.0f})")
    for p in potes:
        l10, h10 = p['corpo_l'] - 2 * r_corpo, p['z_dente'] - BASE_T
        l8, h8 = 133.7, p['H'] - 16.0
        r = flecha(l10, h10, p['w']) / flecha(l8, h8, p['w'])
        print(f"  {p['cap']:>5} ml | painel {l10:.1f} x {h10:.0f} mm | "
              f"flecha {r:.2f}x a da revisao 8")
    print(f"  o painel ficou {p0['corpo_l'] - 2 * r_corpo - 133.7:+.1f} mm mais estreito "
          f"e {BORDA_H + BASE_T - 16:+.0f} mm mais ALTO.")
    print( "  A borda deixou de ser caixao oco e virou um L (web + parede): menos")
    print( "  rigida que a da revisao 8 na boca. E o preco do footprint menor, e e")
    print( "  a pergunta que o prototipo tem de responder - a boca ovaliza?")

    # ---- aninhamento ----
    print("\nAninhamento a vazio (6 potes de 2,4 L):")
    p4 = potes[3]
    for s in (0.25, 0.50, 0.75, 1.00):
        sobe = aninha(p4, s, boca, colar_l)
        pilha = 5 * sobe + p4['H']
        print(f"  saida {s:.2f}° -> sobe {sobe:5.0f} mm | pilha {pilha:6.0f} mm "
              f"({pilha / (6 * p4['H']) - 1:+.0%} vs soltos)")
    print( "  o DEGRAU INTERNO e o novo batente: o pote de cima para nele se a saida")
    print( "  nao tiver estreitado o fundo mais que a parede. Por isso o 600 ml")
    print( "  praticamente nao aninha e o 2,4 L continua aninhando.")

    print("\nMantimento:")
    for p in potes:
        print(f"  {p['cap']:>5} ml -> arroz {p['cap'] * 0.85 / 1000:.2f} kg | "
              f"feijao {p['cap'] * 0.80 / 1000:.2f} kg | "
              f"acucar {p['cap'] * 0.90 / 1000:.2f} kg | "
              f"macarrao {p['cap'] * 0.35 / 1000:.2f} kg")


if __name__ == '__main__':
    main()
