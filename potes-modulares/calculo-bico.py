#!/usr/bin/env python3
"""
A TAMPA DE BICO - revisao 12. Substitui a tampa de correr da revisao 9.

POR QUE A DE CORRER SAIU
  "nao ficou legal... preciso de algo mais robusto... algo que nao vaze tmb e
  seja hermetico com o bico". E justo. A de correr tinha uma gaveta de 1,80 mm
  correndo em trilhos com 0,25 mm de folga por lado, um 2o aro de silicone que
  vedava por compressao axial e uma janela no piso. Tres coisas que so dao
  certo com tolerancia apertada, e vedacao axial num retangulo e exatamente o
  que este projeto descartou na revisao 4.

O QUE ENTRA NO LUGAR
  Nada que corre, nada que escorrega. A tampa e a MESMA da linha - saia,
  lingueta, aro em U, duas travas - com tres coisas somadas:

    GARGALO  um colar de parede fechada subindo do deck. O furo passa por
             dentro dele. O topo do colar e um ANEL PLANO: e nele que o fecho
             veda, e por isso a linha de vedacao e plana, nao uma curva 3D.
    CALHA    aberta em U, saindo do gargalo para fora, por cima da aba, ate um
             labio que passa da borda da tampa. Aberta e o que o Ricardo pediu
             desde a revisao 9 - para escorrer e para lavar.
    FECHO    tampa do bico com PLUG CONICO entrando no gargalo. Conico porque
             se auto-centra, porque a forca de fechamento vira atrito
             distribuido e porque nao depende de tolerancia de interferencia
             reta. Dobradica viva atras (nao esta na malha).

  O FURO NAO E O BICO. O furo (gargalo) e redondo-retangular e plano - facil de
  vedar. O BICO e a calha aberta depois dele. Separar os dois e o que permite
  "aberto" e "hermetico" na mesma peca: quem veda e o gargalo, quem escorre e a
  calha. Na de correr os dois eram a mesma coisa, e por isso ela nao vedava.

ESTA VERSAO NAO EMPILHA - foi o Ricardo que liberou, e isso paga:
  - o gargalo pode subir acima do plano modular (sobe 4,40 mm);
  - a calha pode passar por cima da aba sem cortar nada;
  - o fecho pode ter aba de dedo.
  O deck continua em -2,00 por economia de ferramenta, nao por necessidade.

Uso:  python3 calculo-bico.py
"""
import importlib.util, math, os

_BASE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('cm', os.path.join(_BASE, 'calculo-modular.py'))
cm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cm)

P = cm.linha(cm.footprint())
P0 = P[0]
COLAR_L, COLAR_W = P0['colar_l'], P0['colar_w']
DLW = COLAR_L - COLAR_W
BOCA = P0['boca']
SAIA_O = BOCA - 2 * cm.SAIA_FOLGA
DECK = SAIA_O - 2 * cm.SAIA_T                 # vao livre do deck
DECK_W = DECK - DLW
TAMPA_O = COLAR_L + 2 * cm.TRAVA_FOLGA        # face externa da aba
Z_MOD = cm.Z_MOD                              # topo do deck

# ---- o gargalo ----
GARG_L   = 24.0     # furo, no sentido do escoamento
GARG_W   = 46.0     # furo, na largura - a mesma frente util da revisao 9
# Raio de canto quase igual a metade do lado menor: o furo e um ESTADIO, nao um
# retangulo com canto quebrado. Pedido do Ricardo ("mais organico, mais clean,
# mais curvado"), e de quebra canto redondo nao segura liquido nem sujeira - o
# mesmo argumento da lavagem.
GARG_R   = 11.0     # raio de canto do furo (metade do lado menor e 12,0)
GARG_PAR = 1.50     # parede do colar (mais grossa que o deck: e onde o fecho
                    # aperta e onde o dedo faz forca)
# A altura do colar NAO e escolha de estilo: e ela que poe o piso da calha
# acima da aba. Com GARG_H de 4,40 (a primeira tentativa) o piso caia em +0,80
# e o labio em +0,20, ambos ABAIXO da aba de +1,20 - a calha cortaria o apoio
# da tampa na borda e pingaria no pote. O minimo e
#   GARG_H >= PP_FLANGE + folga + CALHA_T + BICO_QUEDA - Z_MOD
GARG_H   = 7.50     # altura do colar acima do deck -> topo em +5,50
GARG_MARG = 6.0     # quanto o colar para antes da parede da saia

# ---- a calha ----
CALHA_T    = 1.60   # espessura do piso da calha
BICO_PAR   = 1.50   # parede da calha
BICO_ALT   = 4.00   # altura da parede acima do piso, NA RAIZ (cai ate a ponta)
BICO_FLARE = 0.12   # quanto a calha abre da raiz ate o labio (fracao)
BICO_DECAI = 0.70   # quanto a parede baixa da raiz ate o labio (fracao)
BICO_ENTRA = 0.60   # quanto a calha entra no colar, para fundir. Nao e cota
                    # livre: ela EMPURRA a borda do fecho para dentro, e com
                    # 1,00 o tampo passava a cobrir o furo por so 0,20 mm.
                    # Quem manda aqui e MARGEM_TAMPO, logo abaixo.
BICO_SAI   = 9.00   # quanto o labio passa da face externa da aba
BICO_QUEDA = 2.20   # quanto o piso cai do gargalo ate o labio

# ---- o fecho ----
# Sem saia por fora do colar, e o tampo RENTE a face externa dele. Saia ou
# abano bateriam nas paredes da calha, que comecam na propria face do colar.
# Quem localiza o fecho e o plug conico; quem da pega e a crista no tampo.
FECHO_TOPO = 1.60   # espessura do tampo do fecho
FECHO_ABA  = 1.50   # quanto o tampo passa do colar (so em -X e nos lados: do
                    # lado do bico ele fica rente, senao bate na calha)
FECHO_DOMO = 2.00   # altura do domo do tampo - e a pega, e e o que o deixa
                    # com cara de peca e nao de tampinha
PLUG_PAR   = 1.20   # parede do plug
PLUG_H     = 5.00   # quanto o plug desce dentro do gargalo
# O cone do GARGALO e mais aberto que o do PLUG, e e essa DIFERENCA que faz a
# vedacao. Se os dois tivessem o mesmo cone, as faces seriam paralelas e o
# aperto dependeria de tolerancia de interferencia reta - que e justamente o
# que nao se controla em injecao. Com cones diferentes, o plug entra FOLGADO
# na boca e vai apertando conforme desce: a vedacao acontece onde as duas
# retas se cruzam, e esse ponto anda sozinho para compensar desgaste e creep.
# De quebra o furo com 5° sai do macho sem esforco.
GARG_CONE  = 5.00   # cone do furo, graus por face (mais aberto em cima)
PLUG_CONE  = 1.00   # cone do plug, graus por face
PLUG_BOCA  = 0.15   # folga do plug na BOCA do gargalo, por lado
FECHO_FOLGA = 0.30  # folga entre o tampo e a raiz da parede da calha
FECHO_RUN  = 9.00   # corrida do domo: quanto ele encolhe da borda ate o planalto
                    # (planalto, nao pico - e onde o dedao apoia, e pico em
                    #  molde e ponto que nao enche)


T_GARG, T_PLUG = (math.tan(math.radians(GARG_CONE)),
                  math.tan(math.radians(PLUG_CONE)))

# cotas derivadas
Z_COL   = Z_MOD + GARG_H                       # topo do gargalo = plano de vedacao
Z_PISO  = Z_COL - CALHA_T                      # face de baixo do piso da calha
X_GARG  = DECK / 2 - GARG_MARG - GARG_L / 2    # centro do furo
X_SAIDA = X_GARG + GARG_L / 2 + GARG_PAR       # face externa do colar, lado do bico
X_LABIO = TAMPA_O / 2 + BICO_SAI               # ponta do labio
Z_LABIO = Z_COL - BICO_QUEDA                   # topo do piso no labio
AREA    = GARG_L * GARG_W - (4 - math.pi) * GARG_R ** 2
X_RAIZ  = X_SAIDA - BICO_ENTRA                 # onde a calha nasce, dentro do colar

# O LABIO NAO E COTA ESCOLHIDA. A calha e uma unica secao varrida, escalada em
# altura estacao a estacao - e a mesma escala que baixa a parede afina o piso.
# Pedir parede caindo 70% E pedir piso de 1,60 virando 0,48: o labio sai da
# conta, nao de um numero digitado. Duas cotas que concordam por construcao
# valem mais que duas cotas que precisam ser conferidas.
BICO_LIP = CALHA_T * (1 - BICO_DECAI)          # espessura do labio na ponta

# ---- o tampo do fecho ----
# Em -X e nos lados ele passa FECHO_ABA do colar: e a unha. Do lado do bico ele
# PARA antes da raiz da parede da calha, senao bate nela. O que ele nao pode
# deixar de cobrir e o FURO, e e isso que a conferencia vigia.
FECHO_X1 = X_RAIZ - FECHO_FOLGA                     # borda do tampo, lado do bico
FECHO_X0 = X_GARG - GARG_L / 2 - GARG_PAR - FECHO_ABA
FECHO_L  = FECHO_X1 - FECHO_X0
FECHO_W  = GARG_W + 2 * GARG_PAR + 2 * FECHO_ABA
FECHO_CX = (FECHO_X0 + FECHO_X1) / 2
FECHO_R  = min(GARG_R + GARG_PAR, min(FECHO_L, FECHO_W) / 2 - 0.6)
Z_DOMO   = Z_COL + FECHO_TOPO + FECHO_DOMO     # crista do domo


def perim_ret(a, b, r):
    return 2 * (a + b) - (8 - 2 * math.pi) * r


def estacoes_calha(n=10):
    """Estacoes da calha: (fracao do curso, escala em largura, em altura, dz).

    O piso NAO cai em rampa reta - cai numa curva (t^1.8), mansa na raiz e
    firme na ponta. E o que faz o bico parecer desenhado em vez de cortado. As
    paredes decaem junto (t^1.3) e a calha abre um pouco: na raiz ela e um
    canal, na ponta e uma concha.
    """
    out = []
    for k in range(n + 1):
        t = k / n
        out.append([t,
                    1.0 + BICO_FLARE * t,
                    1.0 - BICO_DECAI * t ** 1.3,
                    -BICO_QUEDA * t ** 1.8])
    return out


def secao_calha(x):
    """As cotas da secao da calha num X do curso.

    A calha e VARRIDA: nenhuma cota dela e constante - nem a largura, nem a
    altura da parede, nem a espessura do piso. Quem quiser medir a calha (a
    conferencia de montagem, a ficha, um desenho) tem de perguntar aqui. Medir
    na cota da raiz e acusar erro que nao existe foi exatamente o que aconteceu
    na primeira rodada desta revisao: a parede tinha aberto 6% para fora e o
    raio passava pela boca aberta do canal em vez de pela parede.
    """
    c = X_LABIO - X_RAIZ
    t = min(max((x - X_RAIZ) / c, 0.0), 1.0)
    sx = 1.0 + BICO_FLARE * t
    sz = 1.0 - BICO_DECAI * t ** 1.3
    dz = -BICO_QUEDA * t ** 1.8
    return dict(t=t, sx=sx, sz=sz,
                y_int=GARG_W / 2 * sx,                  # face interna da parede
                y_par=(GARG_W / 2 + BICO_PAR / 2) * sx, # meio da parede
                y_ext=(GARG_W / 2 + BICO_PAR) * sx,     # face externa
                piso_topo=Z_COL + dz,
                piso_fundo=Z_COL - CALHA_T * sz + dz,
                parede=Z_COL + BICO_ALT * sz + dz,
                esp=CALHA_T * sz, alt=BICO_ALT * sz)


def geometria():
    corrida = X_LABIO - X_SAIDA
    queda = math.degrees(math.atan2(BICO_QUEDA, corrida))
    # onde as duas retas se cruzam = onde o aperto comeca
    d_toca = 2 * PLUG_BOCA / (2 * (T_GARG - T_PLUG))
    interf = (-2 * PLUG_BOCA + 2 * PLUG_H * (T_GARG - T_PLUG)) / 2   # por lado, no fim
    per = perim_ret(GARG_W, GARG_L, GARG_R)
    I = PLUG_PAR ** 3 / 12
    k = 3 * cm.E_PP * I / PLUG_H ** 3          # N/mm por mm de perimetro
    F = k * max(interf, 0.0) * per
    # a passagem e a secao MAIS ESTREITA do furo conico, no pe do colar
    l_fim = GARG_L - 2 * GARG_H * T_GARG
    w_fim = GARG_W - 2 * GARG_H * T_GARG
    area_fim = l_fim * w_fim - (4 - math.pi) * GARG_R ** 2
    # a calha e BALANCO puro a partir do colar - nao se apoia mais na aba.
    # Secao em U: duas paredes como mesas e o piso como alma.
    b, h, t = GARG_W + 2 * BICO_PAR, BICO_ALT + CALHA_T, BICO_PAR
    I_u = (b * h ** 3 - (b - 2 * t) * (h - CALHA_T) ** 3) / 12
    P_dedo = 20.0                                   # 2 kgf na ponta do labio
    flecha = P_dedo * corrida ** 3 / (3 * cm.E_PP * I_u)
    return dict(corrida=corrida, queda=queda, per=per, F=F / 9.81,
                d_toca=d_toca, interf=interf, area=AREA, area_fim=area_fim,
                l_fim=l_fim, w_fim=w_fim, banda=PLUG_H - d_toca,
                I_u=I_u, flecha=flecha)


def _dist_borda(L, W, R, cx, ang):
    """Raio do contorno arredondado num angulo, medido do centro do FURO.

    Retangulo arredondado nao e circulo: o raio depende do angulo, e o do
    tampo e o do furo tem centros diferentes (o tampo e deslocado). Sem medir
    nos dois nao se sabe se um cobre o outro - e esse foi o tipo de erro que
    quase passou no colar da primeira tentativa.
    """
    dx, dy = math.cos(ang), math.sin(ang)
    a, b = L / 2 - R, W / 2 - R                 # centro do arco de canto
    lo, hi = 0.0, 200.0
    for _ in range(60):
        r = (lo + hi) / 2
        # o ponto sai do centro do FURO; cx e onde esta o centro do contorno
        # que estou medindo. A primeira versao escrevia x = cx + r*dx e depois
        # media abs(x - cx), o que CANCELA o cx: media sempre um tampo
        # centrado, e por isso dizia OK para qualquer deslocamento. Foi o
        # autoteste que pegou - a conferencia que nunca reprova nao e
        # conferencia.
        px, py = r * dx - cx, r * dy            # ponto, no referencial do alvo
        qx, qy = max(abs(px) - a, 0.0), max(abs(py) - b, 0.0)
        dentro = (abs(px) <= L / 2 and abs(py) <= W / 2
                  and math.hypot(qx, qy) <= R)
        lo, hi = (r, hi) if dentro else (lo, r)
    return lo


MARGEM_TAMPO = 0.50     # quanto o tampo tem de sobrar do furo, no pior ponto


def margem_do_tampo(n=240):
    """No pior ponto do perimetro, quanto o tampo sobra do furo.

    Dois retangulos arredondados de centros DIFERENTES: a sobra nao e
    (L_tampo - L_furo)/2, varia com o angulo. Sem medir ponto a ponto, o lado
    do bico - que e onde o tampo encurta para nao bater na calha - passa
    desapercebido.
    """
    return min(_dist_borda(FECHO_L, FECHO_W, FECHO_R, FECHO_CX - X_GARG,
                           2 * math.pi * k / n)
               - _dist_borda(GARG_L, GARG_W, GARG_R, 0.0, 2 * math.pi * k / n)
               for k in range(n))


def cobre_o_furo():
    return margem_do_tampo() >= MARGEM_TAMPO


def verifica():
    """O que, se quebrar, entrega um bico que PARECE certo e vaza."""
    g = geometria()
    f = []
    if Z_PISO <= cm.PP_FLANGE:
        f.append('o piso da calha (%+.2f) encosta na aba (%+.2f): a calha cortaria '
                 'o apoio da tampa na borda' % (Z_PISO, cm.PP_FLANGE))
    if g['flecha'] > 1.0:
        f.append('a calha em balanco flecha %.2f mm com 2 kgf na ponta' % g['flecha'])
    if GARG_R > min(GARG_L, GARG_W) / 2:
        f.append('raio de canto (%.1f) maior que metade do lado menor (%.1f)'
                 % (GARG_R, min(GARG_L, GARG_W) / 2))
    if Z_COL <= cm.PP_FLANGE + 0.5:
        f.append('o gargalo (%+.2f) nao sobe o bastante acima da aba (%+.2f)'
                 % (Z_COL, cm.PP_FLANGE))
    if Z_LABIO <= cm.PP_FLANGE:
        f.append('o labio (%+.2f) desce abaixo da aba (%+.2f): pingaria na borda '
                 'do pote' % (Z_LABIO, cm.PP_FLANGE))
    if X_GARG + GARG_L / 2 + GARG_PAR >= DECK / 2 - 1.0:
        f.append('o colar encosta na parede da saia')
    if GARG_W + 2 * GARG_PAR >= DECK_W - 2.0:
        f.append('o colar nao cabe na largura do deck')
    g = geometria()
    if GARG_CONE <= PLUG_CONE:
        f.append('o cone do gargalo (%.1f°) nao e mais aberto que o do plug '
                 '(%.1f°): as faces ficam paralelas e nao ha aperto progressivo'
                 % (GARG_CONE, PLUG_CONE))
    if g['interf'] <= 0.05:
        f.append('no fim do curso o plug aperta so %.3f mm/lado' % g['interf'])
    if g['d_toca'] >= PLUG_H - 1.0:
        f.append('o aperto so comeca em %.2f mm, a %.2f do fim: banda de vedacao '
                 'curta demais' % (g['d_toca'], PLUG_H - g['d_toca']))
    if BICO_LIP >= CALHA_T:
        f.append('o labio (%.2f) nao e mais fino que o piso (%.2f): nao corta a gota'
                 % (BICO_LIP, CALHA_T))
    if BICO_LIP < 0.35:
        f.append('o labio fica com %.2f: fino demais para injetar' % BICO_LIP)
    if FECHO_X1 <= X_GARG + GARG_L / 2:
        f.append('o tampo do fecho para em %+.2f e o furo vai ate %+.2f: o fecho '
                 'nao cobre o bico' % (FECHO_X1, X_GARG + GARG_L / 2))
    if FECHO_X1 >= X_RAIZ:
        f.append('o tampo (%+.2f) bate na raiz da parede da calha (%+.2f)'
                 % (FECHO_X1, X_RAIZ))
    if not cobre_o_furo():
        f.append('no pior ponto do perimetro o tampo sobra so %.2f mm do furo '
                 '(minimo %.2f)' % (margem_do_tampo(), MARGEM_TAMPO))
    if g['queda'] < 5.0:
        f.append('a calha cai so %.1f°: liquido fica parado nela' % g['queda'])
    if PLUG_H <= CALHA_T + 1.0:
        f.append('o plug desce so %.2f: menos que a espessura do piso da calha'
                 % PLUG_H)
    return f


def autoteste():
    """Cada conferencia tem de reprovar a cota que ela vigia.

    Conferencia que nunca disparou nao prova nada - foi esta regra que pegou o
    vertedouro da revisao 9 e a propria altura do colar aqui: a primeira
    tentativa punha o piso da calha em +0,80, abaixo da aba de +1,20.
    """
    global Z_COL, Z_PISO, Z_LABIO, GARG_CONE, BICO_LIP, PLUG_BOCA
    global BICO_DECAI, X_LABIO, GARG_R, FECHO_X1, FECHO_CX
    bons = (Z_COL, Z_PISO, Z_LABIO, GARG_CONE, BICO_LIP, PLUG_BOCA,
            BICO_DECAI, X_LABIO, GARG_R, FECHO_X1, FECHO_CX)
    casos = []

    Z_COL, Z_PISO, Z_LABIO = cm.PP_FLANGE, cm.PP_FLANGE - CALHA_T, cm.PP_FLANGE - 1
    casos.append(any('piso da calha' in x for x in verifica()))
    Z_COL, Z_PISO, Z_LABIO = bons[0], bons[1], bons[2]

    GARG_CONE = PLUG_CONE - 0.5
    casos.append(any('nao e mais aberto' in x for x in verifica()))
    GARG_CONE = bons[3]

    BICO_LIP = CALHA_T + 0.1
    casos.append(any('nao e mais fino' in x for x in verifica()))
    BICO_LIP = bons[4]

    PLUG_BOCA = 1.0
    casos.append(any('aperta so' in x or 'aperto so comeca' in x
                     for x in verifica()))
    PLUG_BOCA = bons[5]

    # as quatro cotas que a revisao 13 trouxe. Sem autoteste, "o tampo cobre o
    # furo" seria uma funcao de 240 pontos que ninguem nunca viu dizer nao.
    BICO_LIP = 0.20
    casos.append(any('fino demais' in x for x in verifica()))
    BICO_LIP = bons[4]

    X_LABIO = X_SAIDA + 80.0                         # bico de palmo em balanco
    casos.append(any('flecha' in x for x in verifica()))
    X_LABIO = bons[7]

    GARG_R = GARG_L                                  # raio maior que o lado
    casos.append(any('raio de canto' in x for x in verifica()))
    GARG_R = bons[8]

    FECHO_X1 = X_GARG                                # tampo parando no meio do furo
    casos.append(any('nao cobre o bico' in x for x in verifica()))
    FECHO_X1 = bons[9]

    FECHO_CX = FECHO_CX - 6.0                        # tampo deslocado demais
    casos.append(any('no pior ponto' in x for x in verifica()))
    FECHO_CX = bons[10]

    if os.environ.get('AUTOTESTE_DEBUG'):
        print('   autoteste:', casos, 'residuo:', verifica())
    return all(casos) and not verifica()


def main():
    g = geometria()
    print("=" * 79)
    print("TAMPA DE BICO - gargalo que veda, calha que escorre, fecho conico")
    print("=" * 79)
    print(f"Base (nao muda): aba {TAMPA_O:.1f} | saia {SAIA_O:.1f} | deck "
          f"{DECK:.1f} x {DECK_W:.1f} | aro em U e as 2 travas")
    print(f"Esta versao NAO EMPILHA (liberado pelo Ricardo) - e e isso que deixa o")
    print(f"gargalo subir acima do plano modular e a calha passar por cima da aba.\n")

    print("GARGALO - e ele que veda")
    print(f"  furo .............. {GARG_L:.1f} x {GARG_W:.1f} na boca, "
          f"{g['l_fim']:.1f} x {g['w_fim']:.1f} no pe (cone de {GARG_CONE:.1f}°/face)")
    print(f"  passagem .......... {g['area_fim']:.0f} mm2 na secao mais estreita "
          f"(canto R{GARG_R:.0f})")
    print(f"  colar ............. parede {GARG_PAR:.2f}, sobe {GARG_H:.2f} mm do deck "
          f"-> topo em {Z_COL:+.2f}")
    print(f"  centro do furo .... x = {X_GARG:+.1f} mm (a {DECK / 2 - X_GARG - GARG_L / 2:.1f} "
          f"mm da parede da saia)")
    print(f"  o topo do colar e um ANEL PLANO: a linha de vedacao e plana, nao uma")
    print(f"  curva 3D. Foi esse o erro conceitual da tampa de correr - la o que")
    print(f"  vedava era a propria janela por onde o produto saia.")

    print("\nCALHA - e ela que escorre, e e aberta")
    print(f"  sai do colar em x={X_SAIDA:.1f} e vai ate o labio em x={X_LABIO:.1f} "
          f"({g['corrida']:.1f} mm de corrida)")
    print(f"  piso de {CALHA_T:.2f} mm caindo {BICO_QUEDA:.2f} mm = {g['queda']:.1f}° "
          f"- liquido nao fica parado")
    print(f"  paredes de {BICO_PAR:.2f} subindo {BICO_ALT:.2f} mm NA RAIZ e caindo "
          f"{BICO_DECAI * 100:.0f}% ate a ponta,")
    print(f"  enquanto a calha abre {BICO_FLARE * 100:.0f}%: na raiz e um canal, na "
          f"ponta e uma CONCHA.")
    print(f"  o piso cai numa CURVA (t^1,8), nao em rampa reta - e o que faz o bico")
    print(f"  parecer desenhado em vez de cortado")
    print(f"  a calha e BALANCO do colar, nao se apoia na aba: com 2 kgf na ponta do")
    print(f"  labio ela flecha {g['flecha']:.3f} mm (secao em U, I = {g['I_u']:.0f} mm4)")
    print(f"  por baixo dela nao ha nada - e aberto e se limpa com um pano")
    print(f"  labio de {BICO_LIP:.2f} mm - e NAO e cota digitada: a mesma escala que")
    print(f"  baixa a parede {BICO_DECAI * 100:.0f}% afina o piso de {CALHA_T:.2f} para "
          f"{BICO_LIP:.2f}. Fica em {Z_LABIO:+.2f},")
    print(f"  acima da aba ({cm.PP_FLANGE:+.2f}), entao nao pinga na borda do pote")
    sm = secao_calha((X_RAIZ + X_LABIO) / 2)
    print(f"  no meio do curso: canal de {sm['alt']:.2f} mm, piso de {sm['esp']:.2f}, "
          f"meia largura {sm['y_ext']:.2f}")
    print(f"  o labio passa {BICO_SAI:.1f} mm da tampa -> medida maxima "
          f"{TAMPA_O + 2 * BICO_SAI:.1f} mm no comprimento")

    print("\nFECHO - plug conico, dobradica viva atras")
    print(f"  gargalo com cone de {GARG_CONE:.1f}°/face, plug com {PLUG_CONE:.1f}°/face")
    print(f"  plug {PLUG_PAR:.2f} de parede, desce {PLUG_H:.2f} mm")
    print(f"  entra FOLGADO {PLUG_BOCA:.2f} mm/lado na boca; as duas retas se cruzam em")
    print(f"  {g['d_toca']:.2f} mm e dali ate o fim ele aperta, chegando a "
          f"{g['interf']:.3f} mm/lado")
    print(f"  banda de vedacao de {g['banda']:.2f} mm, na parte BAIXA do colar - que e")
    print(f"  onde ele e apoiado pelo deck. Vedar junto da boca seria vedar na aresta")
    print(f"  livre, que e a que mais abre.")
    print(f"  o ponto de contato ANDA conforme a peca desgasta ou flui: e isso que")
    print(f"  cone diferente da e interferencia reta nao da.")
    print(f"  tampo de {FECHO_L:.1f} x {FECHO_W:.1f} (raio {FECHO_R:.1f}) com DOMO de "
          f"{FECHO_DOMO:.2f} mm ate {Z_DOMO:+.2f}:")
    print(f"  a pega e o proprio domo, nao uma crista colada em cima dele. Por dentro")
    print(f"  o teto acompanha o domo, entao no meio ha {FECHO_DOMO:.2f} mm de PP e nao")
    print(f"  {FECHO_TOPO + FECHO_DOMO:.2f} macicos - chupagem fica fora da face que se ve")
    print(f"  o domo encolhe {FECHO_RUN:.1f} mm ate um PLANALTO (nao um pico: pico em")
    print(f"  molde e ponto que nao enche, e planalto e onde o dedao apoia)")
    print(f"  o tampo passa {FECHO_ABA:.2f} mm do colar em -X e nos lados e PARA "
          f"{FECHO_FOLGA:.2f} mm")
    print(f"  antes da raiz da calha: e esse deslocamento que da a unha, de graca")
    print(f"  sobra {margem_do_tampo():.2f} mm do furo no PIOR ponto do perimetro "
          f"(minimo {MARGEM_TAMPO:.2f}) -")
    print(f"  conferido ponto a ponto, porque os dois contornos tem centros "
          f"diferentes")
    print(f"  forca para fechar: ~{g['F']:.1f} kgf (limite SUPERIOR - modelo de viga")
    print(f"  engastada num plug que e furado e cede mais que isso)")
    print(f"  dobradica viva atras (lado -X), fora da malha - como a fenda das travas")

    print("\nHERMETICIDADE - o que prometo e o que nao prometo")
    print("  PROMETO: nao vaza deitado nem virado, que e o caso de uso. O plug")
    print("  conico em PP contra PP sela liquido a pressao atmosferica, e e assim")
    print("  que funciona qualquer tampa de detergente ou de azeite.")
    print("  NAO PROMETO: vedacao de classe da tampa principal. Aquela e radial com")
    print("  silicone; esta e PP contra PP. Se o ensaio de agua colorida acusar,")
    print("  a resposta e um filete de silicone no plug - seria o QUARTO perfil")
    print("  extrudado da linha, e por isso nao entrou de saida.")
    print("  O PP tambem FLUI (creep): plug apertado por meses perde interferencia.")
    print("  O cone ajuda porque o aperto se redistribui ao longo do curso.")

    print("\nCONFERENCIAS")
    print("-" * 79)
    f = verifica()
    # cada conferencia vigia uma frase especifica - casar pelo primeiro termo
    # dava falso negativo (varias comecam com "o labio" ou "a calha").
    for t, chave in (("piso da calha acima da aba", 'piso da calha'),
                     ("gargalo sobe o bastante acima da aba", 'gargalo'),
                     ("labio acima da aba - nao pinga na borda", 'labio ('),
                     ("colar cabe no deck, nos dois sentidos", 'colar'),
                     ("cone maior que a interferencia", 'cone do plug'),
                     ("labio mais fino que o piso", 'nao e mais fino'),
                     ("calha cai o bastante", 'calha cai'),
                     ("plug mais fundo que o piso", 'plug desce'),
                     ("labio injetavel - nao fino demais", 'fino demais'),
                     ("calha em balanco nao flecha", 'flecha'),
                     ("raio de canto cabe no lado menor", 'raio de canto'),
                     ("o fecho cobre o bico", 'nao cobre o bico'),
                     ("o fecho nao bate na calha", 'bate na raiz'),
                     ("o tampo sobra do furo em todo o perimetro",
                      'no pior ponto')):
        print(f"  {t:.<62} {'FALHA' if any(chave in x for x in f) else 'OK'}")
    print(f"  {'autoteste: cada conferencia reprova a cota que vigia':.<62} "
          f"{'OK' if autoteste() else 'FALHA'}")
    if f:
        print("\n  FALHAS:")
        for x in f:
            print("   -", x)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
