#!/usr/bin/env python3
"""
Terceira tampa: TAMPA DE CORRER com gaveta e bico em U aberto.

O PEDIDO
  Uma terceira tampa, de correr, com outro aro de TPE, e um bico na propria
  tampa - aberto em "U", nao fechado em "O", para o liquido escorrer e a peca
  poder ser lavada.

O QUE E FIXO, E POR QUE
  Tudo o que toca o pote vem da tampa de PP da revisao 8 e NAO se mexe: o deck,
  o plug, o filete de TPE vedando radial na boca, as duas travas de clipe e o
  piso da bandeja em z = -2,00, que e o plano modular. Assim a terceira tampa
  entra na linha sem tocar nos quatro moldes de corpo.

O MECANISMO
  O piso da bandeja ganha um BOLSO. Dentro dele corre a GAVETA, um painel que
  desliza sob dois trilhos. A JANELA e um furo no fundo do bolso; com a gaveta
  fechada ela some, com a gaveta recuada ela abre.

  O BICO e uma calha ABERTA (perfil em U) que sai da borda da janela, sobe uma
  rampa por cima da parede do plug e da borda do pote, e termina num labio de
  corte na face externa do deck. A calha tem de subir: o plano de vedacao
  (topo da borda, z = 0) esta ACIMA do piso da bandeja (z = -2,00), e furar
  ali embaixo cortaria o filete. Subindo, o filete continua inteiro e quem
  fecha o pote continua sendo ele.

  Em repouso a calha drena sozinha para dentro da janela - o ponto mais baixo
  dela e a janela. E por isso que o bico e em U e nao em O: tubo fechado
  retem liquido e nao se lava.

O QUE A GAVETA COBRA
  Ela fica NO plano modular, entao o pote de cima pousa em parte sobre ela.
  Eu esperava que a flecha decidisse a espessura - nao decide: o vao curto da
  gaveta e curto (34 mm) e a flecha com o 2,4 L cheio em cima da 0,04 mm. Quem
  pede os 1,80 mm e o friso do segundo aro, que come 0,70 da face de baixo.
  O que a gaveta cobra de verdade e outra coisa: com pote carregado em cima o
  atrito trava o painel. Na pratica o pote de vertedor e o do topo da pilha.

Uso:  python3 calculo-correr.py
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
PLUG = BOCA - 2 * cm.PLUG_FOLGA
BANDEJA = PLUG - 2 * cm.PP_PLUG_PAR          # vao livre da bandeja
DECK_O = COLAR_L + 2 * cm.PP_DECK_FORA
BAND_W = BANDEJA - DLW
R_BAND = cm.raio(BANDEJA, COLAR_L)

# ---- a gaveta ----
GAV_T      = 1.80    # espessura: o friso do aro come 0,70 da face de baixo
GAV_FOLGA  = 0.25    # folga lateral nos trilhos, por lado
GAV_ALTURA = 0.40    # quanto a gaveta corre ACIMA do batente, antes de assentar
TRILHO_L   = 3.00    # quanto o trilho avanca sobre a gaveta, por lado
TRILHO_T   = 1.20    # espessura do trilho
SILL       = 4.00    # sobreposicao da gaveta sobre a janela, em cada ponta
GAV_PAREDE = 6.00    # vao entre a ponta da gaveta e a parede da bandeja:
                     # e nele que a rampa mansa sobe do bolso ao piso da bandeja
PUXADOR    = 6.00    # rebaixo para o dedo, no topo da gaveta

# ---- o segundo aro ----
ARO2_D     = 1.60    # corda do aro da gaveta
ARO2_PROF  = 0.70    # profundidade do friso na face de baixo da gaveta
ARO2_COMP  = 0.20    # interferencia axial quando a gaveta assenta
CUNHA      = 2.50    # ultimos mm de curso em que a gaveta desce na rampa

# ---- o bico em U ----
BICO_LIP   = 0.40    # labio de corte na ponta
BICO_PAR   = 1.20    # parede da calha

Z_MOD  = -cm.BASE_T                   # plano modular = piso da bandeja
Z_BOLSO = Z_MOD - GAV_T - 0.15        # fundo do bolso, onde a gaveta corre
Z_SEL  = 1.20                         # piso da calha por cima da borda do pote
Z_TOPO = 4.00                         # topo das paredes da calha, na ponta


def perim_ret(a, b, r):
    return 2 * (a + b) - (8 - 2 * math.pi) * r


# posicao: (rotulo, largura da janela, profundidade da janela, largura do bico,
#           eixo de corrida, quanto da face o bico ocupa)
POSICOES = [
    dict(cod='curto', rot='A · lado curto (frente estreita)',
         jan_w=55.0, jan_d=25.0, bico_w=28.0, eixo='comprimento'),
    dict(cod='canto', rot='B · canto, na diagonal',
         jan_w=34.0, jan_d=19.0, bico_w=24.0, eixo='diagonal'),
    dict(cod='comprido', rot='C · lado comprido',
         jan_w=70.0, jan_d=24.0, bico_w=28.0, eixo='largura'),
]


def dentro_bandeja(x, y, folga=0.0):
    """O ponto cai dentro do vao da bandeja (retangulo de cantos R_BAND)?"""
    hx, hy = BANDEJA / 2 - folga, BAND_W / 2 - folga
    ax, ay = abs(x), abs(y)
    if ax > hx or ay > hy:
        return False
    cx, cy = hx - R_BAND, hy - R_BAND
    if ax <= cx or ay <= cy:
        return True
    return math.hypot(ax - cx, ay - cy) <= R_BAND


def layout(cod, jan_w=None, jan_d=None, rec=None):
    """Onde ficam base, direcao, janela, gaveta e bolso.

    Tudo e medido a partir de uma BASE na parede da bandeja, recuando na
    direcao u. No canto a base e o ponto do canto, nao um raio saindo do
    centro: a 45 graus o raio do centro sai pela face comprida muito antes de
    chegar ao canto, e foi assim que eu errei da primeira vez.
    """
    p = next(q for q in POSICOES if q['cod'] == cod)
    jw = p['jan_w'] if jan_w is None else jan_w
    jd = p['jan_d'] if jan_d is None else jan_d
    if cod == 'curto':
        base, u = (BANDEJA / 2, 0.0), (1.0, 0.0)
        ext = (DECK_O / 2, 0.0)
    elif cod == 'comprido':
        base, u = (0.0, BAND_W / 2), (0.0, 1.0)
        ext = (0.0, (DECK_O - DLW) / 2)
    else:
        r2 = math.sqrt(0.5)
        cx, cy = BANDEJA / 2 - R_BAND, BAND_W / 2 - R_BAND
        base = (cx + R_BAND * r2, cy + R_BAND * r2)
        u = (r2, r2)
        rd = cm.raio(DECK_O, COLAR_L)
        dx, dy = DECK_O / 2 - rd, (DECK_O - DLW) / 2 - rd
        ext = (dx + rd * r2, dy + rd * r2)
    gav_w = jw + 2 * SILL + 2 * TRILHO_L
    gav_l = jd + 2 * SILL
    curso = jd + 2.0
    if rec is None:
        rec = SILL + jd / 2 + GAV_PAREDE            # recuo da base ate o centro da janela
    jan = (base[0] - u[0] * rec, base[1] - u[1] * rec)
    gav_ab = (jan[0] - u[0] * curso, jan[1] - u[1] * curso)
    bolso = (jan[0] - u[0] * curso / 2, jan[1] - u[1] * curso / 2)
    # quanto o liquido atravessa de piso da bandeja antes de chegar a parede
    travessia = max(rec - jd / 2 - SILL - GAV_PAREDE, 0.0)
    return dict(p=p, jan_w=jw, jan_d=jd, base=base, u=u, ext=ext, jan=jan,
                gav_fec=jan, gav_ab=gav_ab, bolso=bolso, rec=rec,
                gav_w=gav_w, gav_l=gav_l, curso=curso, bolso_l=gav_l + curso,
                travessia=travessia)


def cabe(L):
    """O bolso inteiro cai dentro do vao da bandeja?"""
    u = L['u']
    n = (-u[1], u[0])
    c = L['bolso']
    a, b = (L['gav_w'] + 2 * GAV_FOLGA) / 2, L['bolso_l'] / 2
    for sa in (1, -1):
        for sb in (1, -1):
            x = c[0] + sa * n[0] * a + sb * u[0] * b
            y = c[1] + sa * n[1] * a + sb * u[1] * b
            if not dentro_bandeja(x, y, folga=1.0):
                return False
    return True


def recuo_minimo(cod, jw, jd):
    """Menor recuo da base em que o bolso inteiro cabe na bandeja.

    No canto nao basta encostar a gaveta na parede: a 45 graus o bolso
    transborda pela face comprida. Tem de recuar - e o preco e o liquido
    atravessar piso de bandeja antes de chegar ao bico.
    """
    base = SILL + jd / 2 + GAV_PAREDE
    # NAO da para bisseccionar: no canto a folga e uma FAIXA, nao um semi-eixo.
    # Recuar demais faz o bolso sair pelo outro lado. Varre-se e pega-se o
    # primeiro D que cabe. (Bisseccionar aqui me devolveu "nao cabe nunca".)
    d = base
    while d < base + 90.0:
        if cabe(layout(cod, jw, jd, d)):
            return d
        d += 0.25
    return None


def maior_janela(cod, prop):
    """Maior janela que cabe, mantendo a proporcao largura/profundidade."""
    melhor = None
    w = 8.0
    while w < 120.0:
        if recuo_minimo(cod, w, w / prop) is None:
            break
        melhor = w
        w += 0.5
    return (melhor, melhor / prop) if melhor else (None, None)


def geometria(p):
    """Tudo o que sai das cotas da janela, ja com o recuo que faz o bolso caber."""
    jan_w, jan_d = p['jan_w'], p['jan_d']
    rec = recuo_minimo(p['cod'], jan_w, jan_d)
    L = layout(p['cod'], jan_w, jan_d, rec)
    # O caminho do liquido tem DOIS trechos, e so desenhando o corte isso
    # apareceu:
    #   1) do fundo do bolso ate o piso da bandeja - rampa longa e mansa;
    #   2) do piso da bandeja ate o piso da calha - o VERTEDOURO, curto e ingreme.
    # O vertedouro existe porque a calha nao pode descer abaixo de z=0 em cima
    # da borda (ali a tampa POUSA no pote) nem cortar o friso do filete, que
    # comeca em -3,00 na face do plug. E ele que decide quanto se inclina o pote.
    run1 = GAV_PAREDE
    rampa1 = math.degrees(math.atan2(Z_MOD - Z_BOLSO, run1))
    run2 = cm.PP_PLUG_PAR + 2.0
    vert = Z_SEL - Z_MOD
    rampa2 = math.degrees(math.atan2(vert, run2))
    area = jan_w * jan_d - (4 - math.pi) * 3.0 ** 2      # cantos R3 na janela
    aro_per = perim_ret(jan_w + 4.0, jan_d + 4.0, 3.0)   # friso 2 mm fora da janela
    aro_g = aro_per * math.pi * (ARO2_D / 2) ** 2 * cm.RHO_TPE
    gav_g = (L['gav_w'] * L['gav_l'] - (4 - math.pi) * 3.0 ** 2) * GAV_T * cm.RHO_PP
    # forca para fechar: atrito do aro comprimido ARO2_COMP
    Etpe, forma, mu = 1.8, 1.8, 0.75
    pres = Etpe * (ARO2_COMP / ARO2_D) * forma
    larg = 0.9 * math.sqrt(ARO2_D * ARO2_COMP)
    F = mu * pres * aro_per * larg
    g = dict(L)
    g.update(run1=run1, rampa1=rampa1, run2=run2, vert=vert, rampa2=rampa2,
             area=area, aro_per=aro_per, aro_g=aro_g, gav_g=gav_g, F=F / 9.81)
    return g


def flecha_gaveta(g):
    """Flecha do painel da gaveta com o 2,4 L cheio de arroz em cima.

    A gaveta esta NO plano modular, entao ela leva parte da pilha. Placa
    apoiada nos dois trilhos, carga uniforme: flecha ~ alfa*q*b^4/(E*t^3).
    """
    carga = (P[3]['peso'] + 2040) * 9.81e-3            # N, pote + arroz
    apoio = cm.area(BANDEJA, BAND_W, R_BAND)           # area que recebe a pilha
    q = carga / apoio                                   # MPa
    b = min(g['gav_w'] - 2 * TRILHO_L, g['gav_l'])
    a = max(g['gav_w'] - 2 * TRILHO_L, g['gav_l'])
    alfa = 0.044 if a / b < 1.5 else 0.0906
    return alfa * q * b ** 4 / (cm.E_PP * GAV_T ** 3), q * 1e3


def espessura_gaveta():
    """Por que 1,80 mm. NAO e a flecha - e o friso do aro.

    O friso do 2o aro tem ARO2_PROF de profundidade e fica na face de baixo da
    gaveta. O que sobra de parede sob ele e o que segura o painel.
    """
    return GAV_T - ARO2_PROF


def verifica():
    """As relacoes que o corte tem de respeitar. Erram-se de olho, nao de conta.

    Cada uma corresponde a um jeito de a peca ficar errada sem que nada acuse:
    a tampa deixar de vedar, a gaveta nao caber, o bico virar tubo fechado.
    """
    falhas = []
    z_friso = -3.00                                  # topo do friso do filete
    if Z_SEL <= 0.0:
        falhas.append('piso da calha em %+.2f: abaixo de z=0 ele corta o apoio '
                      'da tampa na borda' % Z_SEL)
    if Z_SEL <= z_friso + 1.0:
        falhas.append('piso da calha em %+.2f: encosta no friso do filete (%+.2f) '
                      '-> a tampa nao veda nem fechada' % (Z_SEL, z_friso))
    if Z_SEL - 0.0 < cm.PP_DECK - 0.4:
        falhas.append('so %.2f mm de material entre o piso da calha e o apoio na '
                      'borda' % (Z_SEL - 0.0))
    if Z_BOLSO >= Z_MOD - GAV_T:
        falhas.append('o bolso e raso demais para a gaveta de %.2f mm' % GAV_T)
    if Z_TOPO <= Z_SEL + 1.5:
        falhas.append('a calha tem so %.2f mm de profundidade' % (Z_TOPO - Z_SEL))
    if Z_BOLSO - cm.PP_DECK <= -cm.PP_PLUG_H:
        falhas.append('o fundo do bolso (%+.2f) passa da ponta do plug (%+.2f)'
                      % (Z_BOLSO - cm.PP_DECK, -cm.PP_PLUG_H))
    if GAV_T - ARO2_PROF < 0.8:
        falhas.append('sob o friso do 2o aro sobram so %.2f mm de gaveta'
                      % (GAV_T - ARO2_PROF))
    for p in POSICOES:
        g = geometria(p)
        if not cabe(g):
            falhas.append('%s: o bolso nao cabe na bandeja' % p['cod'])
        if g['curso'] < g['jan_d']:
            falhas.append('%s: curso %.1f nao abre a janela de %.1f'
                          % (p['cod'], g['curso'], g['jan_d']))
        if p['bico_w'] > g['jan_w']:
            falhas.append('%s: bico (%.0f) mais largo que a janela (%.0f)'
                          % (p['cod'], p['bico_w'], g['jan_w']))
    return falhas



def autoteste():
    """Cada conferencia tem de REPROVAR quando a cota que ela vigia e quebrada.

    Verificacao que nunca disparou nao prova nada - foi a licao da revisao 8.
    """
    global Z_SEL, Z_BOLSO, Z_TOPO, GAV_T, ARO2_PROF
    guarda = (Z_SEL, Z_BOLSO, Z_TOPO, GAV_T, ARO2_PROF)
    casos = [('calha abaixo de z=0', 'Z_SEL', -0.5),
             ('calha em cima do friso', 'Z_SEL', -2.5),
             ('bolso raso', 'Z_BOLSO', -2.5),
             ('calha sem profundidade', 'Z_TOPO', 1.8),
             ('gaveta fina sob o friso', 'GAV_T', 1.2)]
    ok = True
    for rot, nome, val in casos:
        globals()[nome] = val
        if not verifica():
            print("  AUTOTESTE FALHOU: ninguem reprova '%s'" % rot)
            ok = False
        Z_SEL, Z_BOLSO, Z_TOPO, GAV_T, ARO2_PROF = guarda
    return ok


def main():
    print("=" * 79)
    print("TERCEIRA TAMPA - DE CORRER, COM GAVETA E BICO EM U ABERTO")
    print("=" * 79)
    print(f"Base (nao muda): deck {DECK_O:.1f} x {DECK_O - DLW:.1f} | plug {PLUG:.1f} | "
          f"bandeja {BANDEJA:.1f} x {BAND_W:.1f} (canto R{R_BAND:.1f})")
    print(f"Plano modular em z = {Z_MOD:+.2f} | vedacao ao pote: o MESMO filete de "
          f"{cm.FILETE_D:.2f} mm na boca")
    print(f"Travas de clipe: {cm.TRAVA_N} de {cm.TRAVA_FRAC * COLAR_L:.0f} mm, "
          f"centradas nos lados COMPRIDOS")

    print("\n" + "-" * 79)
    print("O MECANISMO (igual nas tres posicoes)")
    print("-" * 79)
    print(f"  bolso ........... rebaixo no piso da bandeja, fundo em z = {Z_BOLSO:+.2f}")
    print(f"  gaveta .......... painel de {GAV_T:.2f} mm; o topo dela E o plano modular")
    print(f"  trilhos ......... 2, avancam {TRILHO_L:.2f} mm sobre a gaveta, "
          f"{TRILHO_T:.2f} mm de espessura")
    print(f"  folga ........... {GAV_FOLGA:.2f} mm/lado nos trilhos")
    print(f"  2o aro de TPE ... corda de {ARO2_D:.2f} mm em friso de {ARO2_PROF:.2f} mm")
    print(f"                    na face de BAIXO da gaveta - viaja com ela, nao arrasta")
    print(f"  cunha ........... nos ultimos {CUNHA:.2f} mm de curso a gaveta desce "
          f"{GAV_ALTURA:.2f} mm")
    print(f"                    e so ai o aro encosta. Comprime {ARO2_COMP:.2f} mm.")
    print(f"  bico ............ calha ABERTA em U, parede {BICO_PAR:.2f}, piso em "
          f"z = {Z_SEL:+.2f}, paredes ate {Z_TOPO:+.2f}")
    print(f"                    labio de corte de {BICO_LIP:.2f} mm na ponta")
    print( "  Em repouso o bolso drena pela janela de volta para dentro do pote: o")
    print( "  fundo do bolso e o ponto mais baixo de todo o caminho. E por isso que o")
    print( "  bico e em U e nao em O - tubo fechado retem liquido e nao se lava.")
    gq = geometria(POSICOES[0])
    print("\n  O CAMINHO DO LIQUIDO tem dois trechos, e so o corte mostrou isso:")
    print(f"    1) fundo do bolso -> piso da bandeja: sobe {Z_MOD - Z_BOLSO:.2f} mm em "
          f"{gq['run1']:.1f} mm = {gq['rampa1']:.0f}°")
    print(f"    2) VERTEDOURO: piso da bandeja -> piso da calha, sobe {gq['vert']:.2f} mm "
          f"em {gq['run2']:.1f} mm = {gq['rampa2']:.0f}°")
    print( "  O vertedouro nao tem como ser manso. A calha nao pode descer abaixo de")
    print( "  z=0 em cima da borda (ali a tampa POUSA no pote) nem cortar o friso do")
    print(f"  filete, que comeca em {-3.00:+.2f} na face do plug. Se cortasse, a tampa")
    print( "  deixaria de vedar com a gaveta FECHADA - o furo estaria sempre aberto.")
    print(f"  Consequencia pratica: verter pede inclinar o pote uns 50-60°, e o ultimo")
    print(f"  dedo de liquido nao sai pelo bico. Com pote de mantimento isso e normal;")
    print( "  e o ponto a olhar no primeiro prototipo.")

    print("\n" + "-" * 79)
    print("AS TRES POSICOES")
    print("-" * 79)
    print(f"{'':<34} {'janela':>12} {'vazao':>9} {'bico':>7} {'curso':>7} "
          f"{'travessia':>10} {'gaveta':>12} {'peso':>6}")
    G = {}
    for p in POSICOES:
        g = geometria(p)
        G[p['cod']] = g
        print(f"{p['rot']:<34} {p['jan_w']:>4.0f}x{p['jan_d']:<7.0f} "
              f"{g['area']:>6.0f}mm2 {p['bico_w']:>5.0f}mm {g['curso']:>5.0f}mm "
              f"{g['travessia']:>8.1f}mm {g['gav_w']:>4.0f}x{g['gav_l']:<6.0f} "
              f"{g['gav_g']:>4.1f}g")
    print("\n  travessia = quanto o liquido atravessa de piso da bandeja entre a janela")
    print("  e a parede, antes de entrar na calha. Zero e o que se quer.")
    for p in POSICOES:
        w, d = maior_janela(p['cod'], p['jan_w'] / p['jan_d'])
        print(f"  {p['rot']:<34} maior janela possivel nessa posicao: "
              f"{w:.0f} x {d:.0f} = {w * d:.0f} mm2")

    print(f"\n{'':<34} {'2o aro':>16} {'fechar':>8} {'vertedouro':>11} "
          f"{'bolso cabe?':>14}")
    for p in POSICOES:
        g = G[p['cod']]
        ok = 'sim' if cabe(g) else 'NAO'
        print(f"{p['rot']:<34} {g['aro_per']:>6.0f}mm {g['aro_g']:>4.1f}g "
              f"{g['F']:>6.1f}kgf {g['rampa2']:>6.1f}° {ok:>14}")

    print("\n" + "-" * 79)
    print("O QUE DECIDE, E NAO E O TAMANHO DA JANELA")
    print("-" * 79)
    per_band = perim_ret(BANDEJA, BAND_W, R_BAND)
    for p in POSICOES:
        g = G[p['cod']]
        corte = p['bico_w'] / per_band * 100
        print(f"\n{p['rot']}")
        print(f"  vazao {g['area']:.0f} mm2 | bico de {p['bico_w']:.0f} mm | "
              f"corta {corte:.1f}% da parede da bandeja")
        if p['cod'] == 'curto':
            print( "  + a frente estreita e a face que fica de frente na prateleira:")
            print( "    o bico vira desenho, nao remendo.")
            print(f"  + o bico de {p['bico_w']:.0f} mm num vao de {BAND_W:.0f} mm converge:")
            print( "    o jato concentra em vez de espalhar pela lateral.")
            print( "  + nao encosta nas travas, que estao nos lados compridos.")
            print(f"  + travessia ZERO: a janela encosta na parede e o liquido cai")
            print( "    direto na calha, sem molhar piso de bandeja.")
            print(f"  - o curso da gaveta ({g['curso']:.0f} mm) corre no COMPRIMENTO:")
            print( "    aberta, ela avanca para o meio da tampa.")
        if p['cod'] == 'canto':
            print(f"  - TRAVESSIA de {g['travessia']:.0f} mm. E o numero que derruba esta opcao,")
            print( "    e eu apostava no contrario. A 45 graus o bolso transborda pela face")
            print( "    comprida, entao ele TEM de recuar - e a janela fica longe da parede.")
            print( "    O liquido atravessa piso de bandeja antes de chegar ao bico, e o que")
            print( "    atravessa fica la depois que se para de verter.")
            print(f"  - vazao de {g['area']:.0f} mm2, menos da METADE da opcao A, pelo mesmo")
            print( "    motivo: o canto e estreito e o bolso e quadrado.")
            print( "  + o canto ainda e o melhor lugar para VERTER: concentra o filete e o")
            print(f"    R{cm.R_EXT:.0f} da borda ja faz a curva. So que o preco de chegar la e alto.")
            print( "  - trilho a 45°: o molde nao muda (nervura reta, so girada), mas a")
            print( "    gaveta vira um losango em planta e o puxador fica no canto.")
        if p['cod'] == 'comprido':
            print(f"  + a maior vazao das tres: {g['area']:.0f} mm2, e travessia zero.")
            print(f"  + o curso ({g['curso']:.0f} mm) corre na LARGURA, que sobra "
                  f"({BAND_W:.0f} mm).")
            print( "  - CONFLITO: as duas travas de clipe sao centradas nos lados")
            print(f"    compridos, {cm.TRAVA_FRAC * COLAR_L:.0f} mm cada. O bico cai em cima")
            print( "    de uma delas. Sai uma trava inteira ou ela vira duas menores -")
            print( "    e ai a forca de fechamento daquele lado se reparte.")
            print(f"  - bico de {p['bico_w']:.0f} mm num vao de {BANDEJA:.0f} mm nao converge:")
            print( "    o liquido tende a espalhar pela face comprida.")

    print("\n" + "-" * 79)
    print("O QUE A GAVETA COBRA - vale para as tres")
    print("-" * 79)
    for p in POSICOES:
        g = G[p['cod']]
        fl, q = flecha_gaveta(g)
        print(f"  {p['rot']:<34} flecha {fl:.2f} mm com o 2,4 L cheio em cima")
    print(f"  (carga de {(P[3]['peso'] + 2040) / 1000:.1f} kg espalhada em "
          f"{cm.area(BANDEJA, BAND_W, R_BAND) / 100:.0f} cm2 = "
          f"{flecha_gaveta(G['curto'])[1]:.1f} kPa)")
    print( "  A flecha, entao, NAO e o problema: o vao curto da gaveta e o que manda,")
    print( "  e ele e curto. Quem pede os %.2f mm de espessura e o friso do 2o aro:" % GAV_T)
    print(f"  ele tem {ARO2_PROF:.2f} mm de profundidade e deixa so "
          f"{espessura_gaveta():.2f} mm de parede sob ele.")
    print( "  E por isso que nao se corre a gaveta com pote carregado em cima - o")
    print( "  atrito da carga trava o painel. Na pratica o pote de vertedor e o do topo.")

    print("\n" + "-" * 79)
    print("FERRAMENTAL")
    print("-" * 79)
    print( "  A tampa de correr e um molde NOVO (5 -> 6 pecas injetadas na linha):")
    print( "    corpo x4 . tampa de PP . tampa de correr . filete . 2o aro")
    print( "  O corpo NAO muda: a terceira tampa usa a mesma borda, a mesma boca e o")
    print( "  mesmo filete. Foi por isso que o mecanismo ficou todo dentro da tampa.")
    print( "  A gaveta e peca separada: molde proprio ou cavidade no mesmo bloco.")
    print(f"  O 2o aro e outro perfil de TPE ({ARO2_D:.2f} mm contra "
          f"{cm.FILETE_D:.2f} do filete) - vale perguntar ao fornecedor se sai do")
    print( "  mesmo material com duas matrizes de extrusao, para nao abrir contrato novo.")

    print("\n" + "-" * 79)
    print("CONFERENCIAS")
    print("-" * 79)
    f = verifica()
    if f:
        for x in f:
            print("  FALHA: " + x)
    else:
        print("  piso da calha acima de z=0 e acima do friso do filete ...... OK")
        print("  material entre a calha e o apoio na borda .................. OK")
        print("  bolso fundo o bastante para a gaveta ....................... OK")
        print("  profundidade da calha e parede sob o friso do 2o aro ....... OK")
        print("  bolso cabe na bandeja, curso abre a janela, bico <= janela .. OK")
    if autoteste():
        print("  autoteste: cada conferencia reprova a cota que ela vigia .... OK")
    else:
        return 1
    return 1 if f else 0


if __name__ == '__main__':
    raise SystemExit(main())
