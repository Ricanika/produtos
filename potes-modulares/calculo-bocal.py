#!/usr/bin/env python3
"""
A TAMPA DE BOCAL - revisao 14. Era "tampa de bico" ate a revisao 13.

O BICO SAIU
  "tire esse bico, e deixe mais alto o buraco e a tampinha do buraco deixe
  alto tmb". A calha era a feicao mais trabalhada da peca - secao em U varrida,
  abrindo 12%, baixando 70%, caindo em t^1,8 - e saiu inteira. Vale registrar
  por que isso NAO e perda:

    - a calha era um balanco de 16,7 mm fora da silhueta da tampa. Com ela, a
      medida maxima da peca era 166,1 mm; sem ela, volta a 149,7 - a MESMA das
      outras duas tampas. A linha volta a embalar, paletizar e expor igual.
    - a calha exigia que o colar tivesse altura MINIMA (o piso dela tinha de
      passar acima da aba). Sem calha, a altura do colar fica livre - e e
      justamente isso que o Ricardo pediu em seguida.
    - a calha era a unica feicao da linha que precisava de uma secao varrida.
      O codigo que a fazia (varrido(), em gera-3d.py) FICA, porque as lombadas
      sob o deck usam o mesmo mecanismo.

  Sem calha, quem verte e o PROPRIO BOCAL. E por isso ele cresce: o colar passa
  de 7,50 para 14,00 mm acima do deck. Bocal alto verte melhor que bocal raso
  pela mesma razao que garrafa verte melhor que lata - o jato se forma longe da
  parede da peca e nao tem por onde voltar.

O QUE FICA, E POR QUE
  GARGALO  colar de parede fechada subindo 14,00 mm do deck, furo em ESTADIO
           de 24 x 46 (raio 11). O furo e conico (3°/face) e o colar tem 3° de
           saida por fora: os dois saem do aco sem arrasto.
           A ARESTA EXTERNA DO ARO FICA VIVA, de proposito. Raio na saida do
           bocal e o que faz o liquido envolver e escorrer pela parede - a
           gota so se solta de aresta.
  FECHO    tampa de bocal com SAIA por fora do colar e PLUG CONICO por dentro
           dele. A saia e a altura que o Ricardo pediu, e e tambem a pega: o
           dedo aperta a parede da saia, nao uma crista. Entre a saia e o plug
           fica um ARO PLANO - e nele que o aro do colar encosta e para.
           Dobradica viva atras (nao esta na malha).

  POR QUE A ALTURA DO FECHO VEM DA SAIA, E NAO DE UM BOTAO EM CIMA
  Tentar deixar o fecho alto crescendo PARA CIMA da uma peca impossivel: botao
  oco em cima de um tampo macico e um VAZIO FECHADO, que nenhum macho forma;
  botao macico e 4 mm de PP solido, que chupa na face que se ve. Casca de tampa
  tem de abrir para BAIXO em todo ponto - e e isso que a saia faz. A altura
  aparece por fora, o vazio sai pelo lado aberto, e a secao fica em 1,30 a 1,60
  em qualquer corte.

ESTA VERSAO NAO EMPILHA - foi o Ricardo que liberou, e e isso que deixa o colar
subir 14 mm acima do plano modular. O deck continua em -2,00 por economia de
ferramenta, nao por necessidade.

Uso:  python3 calculo-bocal.py
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
GARG_W   = 46.0     # furo, na largura
# Raio de canto quase igual a metade do lado menor: o furo e um ESTADIO, nao um
# retangulo com canto quebrado. Canto redondo nao segura liquido nem sujeira.
GARG_R   = 11.0     # raio de canto do furo (metade do lado menor e 12,0)
GARG_PAR = 1.50     # parede do colar (mais grossa que o deck: e onde o fecho
                    # aperta e onde o dedo faz forca)
GARG_H   = 14.00    # altura do colar acima do deck -> aro em +12,00.
                    # Na revisao 13 eram 7,50, e o que mandava era a calha: o
                    # piso dela tinha de passar acima da aba (minimo 7,30).
                    # Sem calha essa amarra sumiu, e quem verte agora e o
                    # proprio bocal - entao ele sobe.
GARG_MARG = 8.0     # quanto o colar para antes da parede da saia. Subiu de 6,0
                    # porque a SAIA do fecho agora passa por fora do colar e
                    # pede os 2 mm de volta.
GARG_CONE = 3.00    # cone do furo, graus por face (mais largo em cima)
COLAR_SAI = 3.00    # saida da face EXTERNA do colar, graus por face
# Com 14 mm de colar, o cone de 5° da revisao 13 estrangularia o furo em 2,7 mm
# de lado a lado. 3° e o minimo que o Ricardo pede em feicao e o bastante para
# o macho sair - e o que se perde de aperto no plug volta como curso (veja
# PLUG_H).

# ---- o fecho ----
FECHO_TOPO  = 1.60  # espessura da casca do fecho (tampo, saia e domo)
FECHO_SAIA  = 9.00  # quanto a saia do fecho desce por fora do colar - e a
                    # altura que se ve e a pega que o dedo usa
FECHO_PAR   = 1.30  # parede da saia
FECHO_FOLGA = 0.35  # folga entre a saia e a face externa do colar
FECHO_DOMO  = 2.50  # altura do domo sobre o aro plano
FECHO_RUN   = 7.00  # corrida do domo: quanto ele encolhe da mola ate o
                    # planalto (planalto, nao pico - pico em molde e ponto que
                    # nao enche, e planalto e onde o dedao apoia)
PLUG_PAR    = 1.20  # parede do plug
PLUG_H      = 9.00  # quanto o plug desce dentro do gargalo. Eram 5,00 com o
                    # colar de 7,50; colar alto paga curso, e curso e o que
                    # faz a vedacao com cone pequeno.
# O cone do GARGALO e mais aberto que o do PLUG, e e essa DIFERENCA que faz a
# vedacao. Se os dois tivessem o mesmo cone, as faces seriam paralelas e o
# aperto dependeria de tolerancia de interferencia reta - que e justamente o
# que nao se controla em injecao. Com cones diferentes o plug entra FOLGADO na
# boca e vai apertando conforme desce: a vedacao acontece onde as duas retas se
# cruzam, e esse ponto anda sozinho para compensar desgaste e creep.
PLUG_CONE   = 1.00  # cone do plug, graus por face
PLUG_BOCA   = 0.15  # folga do plug na BOCA do gargalo, por lado

T_GARG, T_PLUG = (math.tan(math.radians(GARG_CONE)),
                  math.tan(math.radians(PLUG_CONE)))
T_COLAR = math.tan(math.radians(COLAR_SAI))

# cotas derivadas
Z_COL   = Z_MOD + GARG_H                       # aro do gargalo = plano de apoio
Z_SAIA  = Z_COL - FECHO_SAIA                   # borda de baixo da saia do fecho
Z_PLUG  = Z_COL - PLUG_H                       # ponta do plug
Z_DOMO  = Z_COL + FECHO_TOPO + FECHO_DOMO      # planalto do domo
X_GARG  = DECK / 2 - GARG_MARG - GARG_L / 2    # centro do furo
PESCOCO = Z_SAIA - Z_MOD                       # quanto de colar fica a vista


# ---------------------------------------------------------------------------
# UMA SO FONTE PARA OS ANEIS
#
# Tudo nesta peca - furo, colar, saia, plug, domo - e o MESMO estadio deslocado
# para dentro ou para fora. Deslocar um retangulo arredondado para dentro em d
# tira d de cada lado E TIRA d DO RAIO: quem mantem o raio fixo nao esta
# fazendo um cone, esta fazendo um estadio escalado, e no colar de 14 mm isso
# estoura (o raio de 11 nao cabe num lado menor de 21,3).
#
# Era esta a licao de secao_calha() na revisao 13: quem precisa medir a peca
# pergunta aqui, nao recalcula por fora.
# ---------------------------------------------------------------------------
def desloca(d):
    """O estadio do furo deslocado d para DENTRO (d<0 = para fora)."""
    return (GARG_L - 2 * d, GARG_W - 2 * d, GARG_R - d)


def furo(z):
    """O furo conico na altura z: mais largo no aro, estreitando para baixo."""
    return desloca((Z_COL - z) * T_GARG)


def colar_ext(z):
    """A face externa do colar na altura z, com os 3° de saida."""
    return desloca(-(GARG_PAR + (Z_COL - z) * T_COLAR))


def saia_int(z):
    return desloca(-(GARG_PAR + (Z_COL - z) * T_COLAR + FECHO_FOLGA))


def saia_ext(z):
    return desloca(-(GARG_PAR + (Z_COL - z) * T_COLAR + FECHO_FOLGA + FECHO_PAR))


def plug_ext(z):
    """Face externa do plug. Entra folgado no aro e aperta descendo."""
    return desloca(PLUG_BOCA + (Z_COL - z) * T_PLUG)


def plug_int(z):
    return desloca(PLUG_BOCA + (Z_COL - z) * T_PLUG + PLUG_PAR)


D_MOLA = PLUG_BOCA + PLUG_PAR                  # onde o domo nasce: a aresta
                                               # interna do plug, no aro
ANEIS = dict(furo=furo, colar_ext=colar_ext, saia_int=saia_int,
             saia_ext=saia_ext, plug_ext=plug_ext, plug_int=plug_int)


def domo(s):
    """O domo, por fracao da corrida: 0 na mola, 1 no planalto.

    A face de DENTRO e a mesma curva FECHO_TOPO abaixo - e por isso que a mola
    dela cai exatamente no aro plano (z = Z_COL) e a casca fica constante.
    """
    L, W, R = desloca(D_MOLA + FECHO_RUN * s)
    return L, W, R, Z_COL + FECHO_TOPO + FECHO_DOMO * math.sin(math.pi / 2 * s)


def area_estadio(L, W, R):
    return L * W - (4 - math.pi) * R ** 2


def perim_estadio(L, W, R):
    return 2 * (L + W) - (8 - 2 * math.pi) * R


def geometria():
    # a passagem e a secao MAIS ESTREITA do furo conico, no pe do colar
    zb = Z_MOD - cm.PP_DECK
    pe = furo(zb)
    aro = furo(Z_COL)
    # onde as duas retas se cruzam = onde o aperto comeca
    d_toca = PLUG_BOCA / (T_GARG - T_PLUG)
    interf = PLUG_H * (T_GARG - T_PLUG) - PLUG_BOCA        # por lado, no fim
    per = perim_estadio(*plug_ext(Z_PLUG))
    I = PLUG_PAR ** 3 / 12
    k = 3 * cm.E_PP * I / PLUG_H ** 3          # N/mm por mm de perimetro
    F = k * max(interf, 0.0) * per
    # a saia como pega: perimetro de parede que o dedo aperta
    pega = perim_estadio(*saia_ext(Z_SAIA)) * FECHO_SAIA / 100.0   # cm2
    return dict(area_aro=area_estadio(*aro), area_pe=area_estadio(*pe),
                pe=pe, aro=aro, d_toca=d_toca, interf=interf,
                banda=PLUG_H - d_toca, per=per, F=F / 9.81,
                pega=pega, alt_fecho=Z_DOMO - Z_SAIA,
                max_x=X_GARG + saia_ext(Z_SAIA)[0] / 2)


def menor_raio():
    """O menor raio de canto de qualquer anel da peca, e onde ele esta.

    Deslocar para dentro come o raio. Se ele chegar a zero o estadio virou
    retangulo de canto vivo; se passar de zero, o contorno se cruza e a malha
    deixa de ser malha. Vale olhar TODOS, nao so o que parece pior.
    """
    casos = [('furo no pe', furo(Z_MOD - cm.PP_DECK)),
             ('furo no aro', furo(Z_COL)),
             ('plug na ponta', plug_int(Z_PLUG)),
             ('plug no aro', plug_int(Z_COL)),
             ('domo no planalto', desloca(D_MOLA + FECHO_RUN)[:3])]
    return min(((n, a[2], a) for n, a in casos), key=lambda t: t[1])


def verifica():
    """O que, se quebrar, entrega um bocal que PARECE certo e nao serve."""
    g = geometria()
    f = []
    nome, r, anel = menor_raio()
    if r < 0.30:
        f.append('o raio de canto cai a %.2f mm em "%s": deslocar para dentro '
                 'come o raio, e abaixo de zero o contorno se cruza' % (r, nome))
    if r > min(anel[0], anel[1]) / 2:
        f.append('em "%s" o raio (%.2f) passou de metade do lado menor (%.2f)'
                 % (nome, r, min(anel[0], anel[1]) / 2))
    if GARG_CONE <= PLUG_CONE:
        f.append('o cone do gargalo (%.1f°) nao e mais aberto que o do plug '
                 '(%.1f°): as faces ficam paralelas e nao ha aperto progressivo'
                 % (GARG_CONE, PLUG_CONE))
    if g['interf'] <= 0.05:
        f.append('no fim do curso o plug aperta so %.3f mm/lado' % g['interf'])
    if g['interf'] > 0.35:
        f.append('no fim do curso o plug aperta %.2f mm/lado: fechar viraria '
                 'esforco de duas maos' % g['interf'])
    if g['d_toca'] >= PLUG_H - 1.0:
        f.append('o aperto so comeca em %.2f mm, a %.2f do fim: banda de vedacao '
                 'curta demais' % (g['d_toca'], PLUG_H - g['d_toca']))
    if COLAR_SAI < cm.SAIDA_NERV:
        f.append('a face externa do colar tem %.1f° de saida, menos que os %.1f° '
                 'que a maquina pede em feicao' % (COLAR_SAI, cm.SAIDA_NERV))
    if PESCOCO < 2.0:
        f.append('a saia do fecho desce ate %+.2f e deixa so %.2f mm de colar a '
                 'vista: o fecho encosta no deck antes de assentar no aro'
                 % (Z_SAIA, PESCOCO))
    if Z_SAIA <= cm.PP_FLANGE:
        f.append('a borda da saia (%+.2f) desce abaixo da aba (%+.2f)'
                 % (Z_SAIA, cm.PP_FLANGE))
    if Z_PLUG <= Z_MOD:
        f.append('a ponta do plug (%+.2f) passa do plano do deck (%+.2f)'
                 % (Z_PLUG, Z_MOD))
    if g['area_pe'] < 700.0:
        f.append('a passagem no pe do colar caiu a %.0f mm2: o cone de %.1f° '
                 'estrangulou o furo' % (g['area_pe'], GARG_CONE))
    if g['max_x'] >= DECK / 2 - 1.0:
        f.append('a saia do fecho vai ate %+.2f e o deck acaba em %+.2f: ela '
                 'encosta na parede da saia da tampa'
                 % (g['max_x'], DECK / 2))
    if GARG_W + 2 * GARG_PAR >= DECK_W - 2.0:
        f.append('o colar nao cabe na largura do deck')
    if g['alt_fecho'] < 10.0:
        f.append('o fecho tem %.1f mm de altura: nao e "alto" para pegar'
                 % g['alt_fecho'])
    return f


def autoteste():
    """Cada conferencia tem de reprovar a cota que ela vigia.

    Conferencia que nunca disparou nao prova nada. Foi esta regra que pegou o
    vertedouro da revisao 9, a altura do colar na 12 e, na 13, uma conferencia
    de cobertura que cancelava o deslocamento na propria conta - ela diria OK
    para qualquer tampo.
    """
    global GARG_H, GARG_CONE, PLUG_BOCA, PLUG_H, COLAR_SAI, FECHO_SAIA
    global GARG_R, GARG_MARG, Z_COL, Z_SAIA, Z_PLUG, Z_DOMO, X_GARG, PESCOCO
    bons = (GARG_H, GARG_CONE, PLUG_BOCA, PLUG_H, COLAR_SAI, FECHO_SAIA,
            GARG_R, GARG_MARG, Z_COL, Z_SAIA, Z_PLUG, Z_DOMO, X_GARG, PESCOCO)
    casos = []

    def refaz():
        global Z_COL, Z_SAIA, Z_PLUG, Z_DOMO, X_GARG, PESCOCO
        Z_COL = Z_MOD + GARG_H
        Z_SAIA, Z_PLUG = Z_COL - FECHO_SAIA, Z_COL - PLUG_H
        Z_DOMO = Z_COL + FECHO_TOPO + FECHO_DOMO
        X_GARG = DECK / 2 - GARG_MARG - GARG_L / 2
        PESCOCO = Z_SAIA - Z_MOD

    GARG_CONE = PLUG_CONE - 0.5
    casos.append(any('nao e mais aberto' in x for x in verifica()))
    GARG_CONE = bons[1]

    PLUG_BOCA = 1.0
    casos.append(any('aperta so' in x or 'aperto so comeca' in x
                     for x in verifica()))
    PLUG_BOCA = bons[2]

    PLUG_H = 40.0                                  # curso absurdo = aperto absurdo
    casos.append(any('esforco de duas maos' in x for x in verifica()))
    PLUG_H = bons[3]

    COLAR_SAI = 0.5
    casos.append(any('de saida, menos que' in x for x in verifica()))
    COLAR_SAI = bons[4]

    FECHO_SAIA = GARG_H - 1.0; refaz()              # saia quase ate o deck
    casos.append(any('de colar a vista' in x for x in verifica()))
    FECHO_SAIA = bons[5]; refaz()

    FECHO_SAIA = 2.0; refaz()                       # fecho baixo, sem pega
    casos.append(any('nao e "alto" para pegar' in x for x in verifica()))
    FECHO_SAIA = bons[5]; refaz()

    GARG_H = 60.0; refaz()                          # colar alto = furo estrangulado
    casos.append(any('estrangulou o furo' in x or 'raio de canto cai' in x
                     for x in verifica()))
    GARG_H = bons[0]; refaz()

    GARG_R = GARG_L                                 # raio maior que o lado
    casos.append(any('passou de metade' in x or 'raio de canto cai' in x
                     for x in verifica()))
    GARG_R = bons[6]

    GARG_MARG = 0.0; refaz()                        # colar colado na saia
    casos.append(any('encosta na parede da saia' in x for x in verifica()))
    GARG_MARG = bons[7]; refaz()

    if os.environ.get('AUTOTESTE_DEBUG'):
        print('   autoteste:', casos, 'residuo:', verifica())
    return all(casos) and not verifica()


def main():
    g = geometria()
    print("=" * 79)
    print("TAMPA DE BOCAL - o bico saiu, o gargalo subiu, o fecho ganhou saia")
    print("=" * 79)
    print(f"Base (nao muda): aba {TAMPA_O:.1f} | saia {SAIA_O:.1f} | deck "
          f"{DECK:.1f} x {DECK_W:.1f} | aro em U e as 2 travas")
    mx = TAMPA_O + 2 * cm.TRAVA_T
    print(f"Medida maxima da peca: {mx:.1f} x {mx - DLW:.1f} mm - a MESMA")
    print(f"das outras duas tampas. Com a calha da revisao 13 era 166,1 mm.\n")

    print("GARGALO - e ele que verte agora")
    print(f"  furo em estadio {GARG_L:.0f} x {GARG_W:.0f}, raio {GARG_R:.0f} - "
          f"{g['area_aro']:.0f} mm2 no aro")
    print(f"  colar de {GARG_PAR:.2f} de parede subindo {GARG_H:.2f} mm: aro em "
          f"{Z_COL:+.2f}")
    print(f"  (na revisao 13 eram 7,50, e quem mandava era a calha. Sem calha a")
    print(f"  altura ficou livre, e bocal alto verte melhor: o jato se forma longe")
    print(f"  da parede da peca e nao tem por onde voltar)")
    print(f"  furo conico de {GARG_CONE:.1f}°/face: estreita para baixo ate "
          f"{g['pe'][0]:.2f} x {g['pe'][1]:.2f}")
    print(f"  passagem no pe: {g['area_pe']:.0f} mm2 ({100 * g['area_pe'] / g['area_aro']:.0f}% "
          f"da do aro) - e esta que manda na vazao")
    print(f"  face externa com {COLAR_SAI:.1f}° de saida: sai do aco sem arrasto")
    print(f"  ARESTA EXTERNA DO ARO VIVA, de proposito - raio ali e o que faz a")
    print(f"  gota envolver e escorrer pela parede. Gota so se solta de aresta.")
    nome, r, _ = menor_raio()
    print(f"  menor raio de canto da peca: {r:.2f} mm, em \"{nome}\"")

    print("\nFECHO - alto porque a saia desce, nao porque um botao sobe")
    print(f"  saia de {FECHO_PAR:.2f} descendo {FECHO_SAIA:.2f} mm por fora do colar,")
    print(f"  com {FECHO_FOLGA:.2f} de folga. Borda de baixo em {Z_SAIA:+.2f}, e sobram")
    print(f"  {PESCOCO:.2f} mm de colar a vista - o pescoco continua sendo pescoco")
    print(f"  altura total do fecho: {g['alt_fecho']:.2f} mm (era 3,60 de tampo + domo)")
    print(f"  PEGA: {g['pega']:.1f} cm2 de parede de saia para o dedo apertar. Na")
    print(f"  revisao 13 a pega era uma crista de 4 x 1,5 mm no tampo.")
    print(f"  domo de {FECHO_DOMO:.2f} sobre o aro plano, encolhendo {FECHO_RUN:.1f} mm ate")
    print(f"  um PLANALTO - planalto, nao pico: pico em molde e ponto que nao enche")
    print(f"  casca de {FECHO_TOPO:.2f} em qualquer corte - a face de dentro do domo e")
    print(f"  a mesma curva {FECHO_TOPO:.2f} abaixo, e a mola dela cai no aro plano")
    print(f"  ABRE PARA BAIXO EM TODO PONTO: nenhum vazio fechado, nenhuma secao")
    print(f"  macica. Botao oco em cima de tampo macico nao se molda, e botao")
    print(f"  macico chupa na face que se ve - foi por isso que a altura veio da saia.")

    print("\nVEDACAO - cone contra cone")
    print(f"  gargalo {GARG_CONE:.1f}°/face, plug {PLUG_CONE:.1f}°/face, curso "
          f"{PLUG_H:.2f} mm")
    print(f"  entra FOLGADO {PLUG_BOCA:.2f} mm/lado no aro; as duas retas se cruzam")
    print(f"  em {g['d_toca']:.2f} mm e dali ate o fim ele aperta, chegando a "
          f"{g['interf']:.3f} mm/lado")
    print(f"  banda de vedacao de {g['banda']:.2f} mm (eram 2,86 na revisao 13): colar")
    print(f"  alto paga CURSO, e curso e o que faz vedacao com cone pequeno")
    print(f"  o cone caiu de 5° para {GARG_CONE:.1f}° porque 5° em 14 mm de colar")
    print(f"  estrangularia o furo. O que se perdeu de aperto voltou como curso.")
    print(f"  o ponto de contato ANDA conforme a peca desgasta ou flui: e isso que")
    print(f"  cone diferente da e interferencia reta nao da")
    print(f"  o ARO PLANO entre a saia e o plug e o batente - o fecho para nele,")
    print(f"  nao no fundo do furo")
    print(f"  forca para fechar: ~{g['F']:.1f} kgf (limite SUPERIOR - modelo de viga")
    print(f"  engastada num plug que e furado e cede mais que isso)")
    print(f"  dobradica viva atras (lado -X), fora da malha - como a fenda das travas")

    print("\nHERMETICIDADE - o que prometo e o que nao prometo")
    print("  PROMETO: nao vaza deitado nem virado, que e o caso de uso. O plug")
    print("  conico em PP contra PP sela liquido a pressao atmosferica, e e assim")
    print("  que funciona qualquer tampa de detergente ou de azeite. A banda de")
    print(f"  vedacao de {g['banda']:.2f} mm e quase o dobro da da revisao 13.")
    print("  NAO PROMETO a classe da tampa principal, que e radial com silicone:")
    print("  a resposta e um filete de silicone no plug - seria o QUARTO perfil")
    print("  extrudado da linha, e por isso nao entrou de saida.")
    print("  O PP tambem FLUI (creep): plug apertado por meses perde interferencia.")
    print("  O cone ajuda porque o aperto se redistribui ao longo do curso.")

    print("\nCONFERENCIAS")
    print("-" * 79)
    f = verifica()
    for t, chave in (("raio de canto positivo em todo anel", 'raio de canto cai'),
                     ("raio nao passa de metade do lado menor", 'passou de metade'),
                     ("cone do gargalo maior que o do plug", 'nao e mais aberto'),
                     ("o plug aperta no fim do curso", 'aperta so'),
                     ("e nao aperta demais", 'duas maos'),
                     ("banda de vedacao longa o bastante", 'aperto so comeca'),
                     ("colar com a saida que a maquina pede", 'de saida, menos que'),
                     ("sobra pescoco a vista sob a saia", 'de colar a vista'),
                     ("saia acima da aba", 'abaixo da aba'),
                     ("plug nao passa do deck", 'passa do plano do deck'),
                     ("passagem no pe do colar", 'estrangulou o furo'),
                     ("saia do fecho cabe no deck", 'encosta na parede da saia'),
                     ("colar cabe na largura do deck", 'largura do deck'),
                     ("o fecho e alto o bastante para pegar", 'para pegar')):
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
