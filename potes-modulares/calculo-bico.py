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
GARG_R   = 6.0      # raio de canto do furo
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
BICO_ALT   = 4.00   # altura da parede acima do piso
BICO_SAI   = 9.00   # quanto o labio passa da face externa da aba
BICO_QUEDA = 2.20   # quanto o piso cai do gargalo ate o labio
BICO_LIP   = 0.50   # espessura do labio na ponta - e ela que corta a gota
BICO_CURVA = 15.0   # quanto o labio vira para baixo, graus

# ---- o fecho ----
# Sem saia por fora do colar, e o tampo RENTE a face externa dele. Saia ou
# abano bateriam nas paredes da calha, que comecam na propria face do colar.
# Quem localiza o fecho e o plug conico; quem da pega e a crista no tampo.
FECHO_TOPO = 1.60   # espessura do tampo do fecho
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
CRISTA_H   = 1.50   # crista de pega no tampo do fecho
CRISTA_W   = 4.00

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


def perim_ret(a, b, r):
    return 2 * (a + b) - (8 - 2 * math.pi) * r


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
    return dict(corrida=corrida, queda=queda, per=per, F=F / 9.81,
                d_toca=d_toca, interf=interf, area=AREA, area_fim=area_fim,
                l_fim=l_fim, w_fim=w_fim, banda=PLUG_H - d_toca)


def verifica():
    """O que, se quebrar, entrega um bico que PARECE certo e vaza."""
    g = geometria()
    f = []
    if Z_PISO <= cm.PP_FLANGE:
        f.append('o piso da calha (%+.2f) encosta na aba (%+.2f): a calha cortaria '
                 'o apoio da tampa na borda' % (Z_PISO, cm.PP_FLANGE))
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
    bons = (Z_COL, Z_PISO, Z_LABIO, GARG_CONE, BICO_LIP, PLUG_BOCA)
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
    print(f"  paredes de {BICO_PAR:.2f} subindo {BICO_ALT:.2f} mm: canal em U aberto "
          f"em cima, para escorrer e para lavar")
    print(f"  labio de {BICO_LIP:.2f} mm virando {BICO_CURVA:.0f}° para baixo, em "
          f"{Z_LABIO:+.2f} - acima da aba ({cm.PP_FLANGE:+.2f}), entao nao pinga na borda")
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
    print(f"  tampo de {FECHO_TOPO:.2f} RENTE a face externa do colar - sem saia e")
    print(f"  sem abano, porque as paredes da calha comecam na propria face do colar")
    print(f"  pega: crista de {CRISTA_W:.1f} x {CRISTA_H:.1f} mm no tampo")
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
                     ("plug mais fundo que o piso", 'plug desce')):
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
