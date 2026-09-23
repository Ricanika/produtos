#!/usr/bin/env python3
"""
Cesto organizador empilhavel e encaixavel -- peca unica em PP.

FORMA: adaptada do STL de referencia enviado em 16/09 (bin de 150 x 100 x 80 mm).
A silhueta lateral de la, medida no proprio solido, e uma caixa com DOIS
CHANFROS A 45 GRAUS na frente -- um no topo e um no pe -- deixando uma face
frontal curta centrada na meia-altura:

    topo ________________________
        |                        \\
        |                         \\  chanfro de topo, 45 graus
        |                          |  face frontal (26 mm)
        |                         /
        |________________________/   chanfro do pe, 45 graus
    fundo

Proporcao do STL de referencia (150 x 100 x 80): chanfros de 32 mm e face
frontal de 16 mm, ou 40% e 20% da altura. Escalado para a nossa altura de
130 mm: chanfros de 52 mm e face frontal de 26 mm (52 + 26 + 52 = 130).

O PEDIDO sobre essa forma:
  - raios da lateral trabalhados, com as pontas arredondadas -> os quatro
    cantos da silhueta saem em R20 (chanfro/topo e chanfro/fundo) e R12 (as
    duas quinas da face frontal), por fillet no perfil 2D;
  - vazado em FUROS REDONDOS com o diametro caindo de cima para baixo, faixa
    cega no pe e FUNDO SOLIDO;
  - empilha: os quatro pes de canto assentam no trilho do rim da peca de baixo;
  - encaixa: saida de 3,5 graus por lado faz o corpo afundar na boca.

Uso:  python3 modelo3d.py
"""
import os
import numpy as np
from build123d import (Align, Axis, Box, Cylinder, Plane, Polyline, Pos,
                       Rectangle, RectangleRounded, Rot, export_step,
                       export_stl, extrude, fillet, loft, make_face)

RHO = 0.905e-3            # g/mm3 - PP copolimero

# --- envelope ---------------------------------------------------------------
# O P estava girado: o lado MAIOR e o comprimento (Y, frente-fundo) e a
# ABERTURA fica na LARGURA (X, os 200 mm). Os pes vao nas faces de 215 mm.
LARG   = 200.0            # X - largura da boca: e nela que fica a abertura
PROF   = 250.0            # Y - comprimento (o lado maior)
ALT    = 130.0            # Z - altura
DRAFT  = 3.5              # graus por lado: saida de molde e folga de encaixe

# --- silhueta lateral, na proporcao do STL de referencia --------------------
CHANFRO    = 52.0         # chanfro de TOPO: 40% da altura, a 45 graus
CHANFRO_PE = 36.0         # chanfro do PE: reduzido de 52 para devolver volume
FRENTE_H   = ALT - CHANFRO - CHANFRO_PE   # face frontal resultante
R_CANTO   = 20.0          # raio nas duas pontas dos chanfros (o pedido)
R_FRENTE  = 12.0          # raio nas duas quinas da face frontal

# --- paredes ----------------------------------------------------------------
T_PAREDE = 1.4
T_FUNDO  = 2.0
T_RIM    = 3.2            # parede engrossada na faixa do rim
H_RIM    = 10.0
H_PE     = 5.0            # a chapa do fundo flutua 5 mm acima do piso
# Pezinhos: 4 blocos ocos SOB a chapa, recuados da borda dela. De fora nao
# aparecem -- a chapa faz aba sobre eles. As posicoes em y sao assimetricas de
# proposito (ver PE_Y/BERCO_Y).
PE_W, PE_T = 13.0, 1.4     # PE_X e derivado da base (ver _pezinhos)
PE_Y = ((-40.0, -20.0), (52.0, 78.0))     # frente e TRASEIRO
SOQ_H, SOQ_T, SOQ_F = 2.5, 2.0, 0.6       # soquete: altura, parede, folga

# --- ESTRUTURA DE EMPILHAMENTO (ideia do cliente, das fotos do cesto laranja)
# Uma parede que sai da BORDA SUPERIOR, por fora do rim, e uma nervura externa
# ("pe na diagonal") que desce pela parede e apoia em cima dela. O ponto e que
# do lado de fora do rim ninguem passa durante o encaixe: a parede da peca de
# cima nunca chega a 107,5 mm. Por isso da empilhar E encaixar.
# As nervuras e as paredes ficam em posicoes ESPELHADAS em y (PAR_Y = -NERV_Y)
# e os intervalos nao se cruzam. Assim, na MESMA orientacao a nervura cai onde
# nao ha parede -> ENCAIXA; girada 180 ela encontra a parede -> EMPILHA.
NERV_Y = ((-46.0, -24.0), (8.0, 22.0))
PAR_Y = tuple((-b, -a) for a, b in NERV_Y)   # (24..46) e (-22..-8)

# ACOPLAMENTO DENTRO DAS PAREDES DA BORDA -- cauda de andorinha vertical.
# Duas pecas lado a lado se tocam justamente onde essas paredes ficam, e a
# feicao e prismatica em z (aberta no topo): sai na direcao de abertura, sem
# gaveta. Em cada lateral uma parede e macho e a outra e femea, espelhado ->
# o arranjo e invariante a 180 graus, entao a pilha girada continua acoplando.
ACO_P = 1.4        # quanto o macho avanca alem de LARG/2
ACO_PESC = 0.5     # profundidade do pescoco (o resto e cabeca)
ACO_WR, ACO_WC = 5.0, 9.0     # largura do pescoco e da cabeca, em y
ACO_F = 0.35       # folga
# Cotas resolvidas do sistema de restricoes (ver README 4.5): com a parede da
# borda de altura h = z0 o passo empilhado da ALT, e o encaixe fica limitado a
# d <= 29,9 mm. Escolhido d = 26 -> passo encaixado de 104 mm.
# O PE e o fundo da propria nervura: ela desce ate z=0 e e nela que a peca se
# apoia -- e e ela que cai no pino da peca de baixo. Passo empilhado = ALT+EMP_H.
EMP_Z0 = 0.0                  # pe da nervura, no chao
EMP_H = 10.0                  # altura do pino na borda
EMP_S = 0.015                 # inclinacao da face externa da nervura
EMP_APOIO_B, EMP_FOLGA_C = 1.6, 0.4    # apoio do pe no pino e folga
EMP_X0 = 103.30               # recalculados por set_draft()
EMP_XI = 101.70
EMP_DIAG = 16.0               # a diagonal de entrada da nervura
EMP_APOIO = 2.5               # trecho reto do pe da nervura, que e o apoio
BERCO_L, BERCO_P, BERCO_H = 18.0, 10.0, 5.0   # orelhas de apoio no rim
BERCO_Y = (-38.0, 75.0)   # centros, nos cantos -- fora das travas

# --- acoplamento lateral: MACHO em +X, FEMEA em -X --------------------------
H_BANDA  = 18.0            # faixa da canaleta: z de 112 a 130
Y_CAN    = (-47.0, 85.0)   # o trecho RETO da lateral no rim: 132 mm
SALTO    = 7.5             # o macho avanca 7,5 -- tem de vencer o rim de 3,2
GANCHO_D = 2.5             # espessura do gancho
GANCHO_H = 6.0             # quanto o gancho desce abaixo da faixa
TRAVA_L  = 40.0            # opcao C: duas abas de 40
JANELA_L = 42.0
Y_TRAVAS = (-26.0, 24.0)   # inicio de cada aba / janela
RISCO_D  = 0.9             # profundidade do risco decorativo da canaleta
# Opcao B, medida a partir do PLANO DA JUNTA (u=0 na face do rim do macho,
# crescendo para dentro da peca femea). A boca e estreita e o bolso e largo:
# e o bolso atras da boca que trava a cabeca da lingueta em X.
B_BOCA   = 4.0             # profundidade da boca (onde passa o pescoco)
B_BOLSO  = 3.9             # profundidade do bolso (onde mora a cabeca)
B_COSTAS = 0.8             # costas do bloco, atras do bolso
B_PESC   = (118.0, 124.0)  # z do pescoco
B_CAB    = (116.0, 126.0)  # z da cabeca

# --- ABA CORRIDA NO RIM + PES COM CAVIDADE (pedido de 18/09) ----------------
# Aba plana de ~10 mm em toda a borda: e nela que o pe pousa, em QUALQUER
# posicao, entao empilhar deixa de precisar girar a peca -- a frente fica
# sempre igual. A aba tem RECORTES nas posicoes dos pes: alinhado, os pes
# passam pelos recortes e a peca ENCAIXA; deslocado, pousam na aba e EMPILHA.
ABA_W, ABA_T = 10.0, 2.5      # largura e espessura da aba
# DIRECAO DA ABA. Medido em 23/09 (cad/extracao.py): virada para DENTRO ela
# avanca 6,27 mm para dentro da face interna da parede -- 6,5% por lado num
# labio continuo de 2,5 mm -- e prende 52.178 mm3 do macho. Nao sai em molde
# de duas placas: exigiria macho colapsavel. Para FORA a silhueta so cresce
# subindo, entao a cavidade desce reta e o macho vira um tronco limpo.
#   +1 = para FORA (extrai)      -1 = para DENTRO (a original)
ABA_DIR = +1
# Quanto do pouso o pe cobre: para fora, a faixa de pouso fica de LARG/2 a
# LARG/2 + ABA_W, e o piso do pe tem de alcancar la. ABA_POUSO e a largura do
# apoio; o resto de ABA_W e a saida em x que o pe precisa para telescopar.
ABA_POUSO = 4.0
# DOBRA na aresta da aba, para baixo. Medido em 23/09 na configuracao C: com a
# aba para fora, duas pecas acopladas so se tocam na espessura dela -- abaixo
# de z = 127,5 as paredes estao 10 mm para dentro de cada lado, ou seja ha um
# vao de 20 mm. O engajamento da cauda de andorinha caia de 14 mm (na versao
# com aba para dentro, onde a femea escavava a faixa do rim) para 2,5 mm. A
# dobra devolve altura de junta, e de quebra enrijece e protege a aresta -- o
# "mini reforco" que o cliente intuiu. Sai do molde: a silhueta salta para
# fora subindo (89,5 -> 100 em z = 122,5) e o canal entre a dobra e a casca
# abre para baixo, onde a cavidade chega.
ABA_DOBRA, ABA_DT = 5.0, 2.0
# Parede da cauda de andorinha depois de vaziada. Ela era um bloco MACICO de
# 1.556 mm3 com 7 a 11 mm de espessura numa peca de parede 1,4: chupa a face
# externa do rim e manda no tempo de ciclo. Vaziada por CIMA -- o plano da
# junta -- quem a forma e a metade de cima e sai reta.
ACO2_T, ACO2_PISO = 1.8, 2.0
ABA_F = 2.0                   # folga do recorte alem do pe
NERV_P = 24.0                 # profundidade do pe em x (>20,6: encosta na parede)
NERV_T = 1.6                  # parede do pe da frente
NERV_RC = 4.2                 # raio das pontas do pe em planta (bico redondo)
# ALTURA EM QUE A CAVIDADE DO PE COMECA (pedido de 22/09: e o tamanho P, para
# coisas miudas -- nada pode ter por onde cair).
# A cavidade do pe e um bloco vertical e, subtraida da peca inteira, ela
# tambem furava a CHAPA DO FUNDO (dois slots de 31,8 x 7,4 mm, 227 mm2 cada)
# e abria a parede desde z = 1,6 -- dois caminhos do interior do cesto para a
# mesa. Ela so e necessaria onde o pe da peca ENCAIXADA passa, ou seja de
# z = passo_encaixe (46,8) para cima; abaixo disso nao serve para nada.
# Em 40 mm, que e onde comeca a primeira faixa de listras: a chapa fica
# inteira, a parede fica cega nos 33 mm acima do piso e, de dentro, a janela
# nasce junto com o vazado -- 6,8 mm de sobra para a sola da peca de cima.
Z_CAV = 40.0
CAV_MEMB = 2.0                # membrana que separa a cavidade da bolsa de baixo
# Deslocamento em y que troca ENCAIXAR por EMPILHAR. 14 mm nao serve mais:
# com um pe por lateral o friso passou para o pe da FRENTE, cujo recorte na
# aba e mais largo (meia-boca 9,25 mm), e a perna do friso caia DENTRO do
# recorte -- o pe da peca encaixada batia nela e o encaixe subia para 73,4 mm.
# Minimo por causa do friso = meia-boca + L/2 + folga + espessura = 15,75 mm.
# Em 21 mm por causa da SAIA de tras: ela e rente a parede, entao a aresta de
# apoio dela nasce em y = BASE_Y/2 = 97,4 e a borda interna da aba esta em
# PROF/2 - ABA_W = 115 -- precisa de 17,6 mm so para alcancar a aba, mais o
# apoio que se quer ter em cima dela.
DESLOC = 21.0

# DOIS pes por lateral (pedido de 18/09; o do meio saiu):
#   frente -- o pe que sustenta, na altura do rasgo curvado da silhueta
#   tras   -- o ENCAIXE: nervura fina, com o pino da referencia na aba
# (yc, L em y, parede, saida em y, face externa no piso, tem pino na aba)
# Um pe por lateral, na frente, com o friso. Atras nao tem pe: tem a
# CANETINHA, um friso curvo unico na sola da base (pedido de 21/09).
# r00 (a penultima cota) vem de pe_r00(), que depende de LARG e da direcao
# da aba -- por isso PES e recalculado por set_envelope().
PES = (
    (-58.0, 10.0, 1.6, 0.045, LARG / 2 - ABA_W + 3.0, True),
)

# --- SAIA DE TRAS: o terceiro apoio, embaixo da peca ------------------------
# A parede de tras continua para baixo na faixa de H_PE, rente a casca. Com os
# dois pes da frente forma um TRIPE -- so que sem nada aparente.
SAIA_W = 108.0                # largura da saia em x (o fundo reto tem 116,7)
SAIA_R = 10.0                 # raio das pontas da saia em planta
SAIA_B = 4.0                  # espessura da aresta de apoio
# Regra de cada pe: saida em y >= parede/passo_encaixe, senao a boca da
# cavidade nunca engole a lingua. A 46,9 mm de passo: 0,034 para 1,6 mm de
# parede e 0,026 para 1,2. Em x vale a mesma coisa com NERV_KX.
# PINO na aba (a referencia do cliente): pequena saliencia que encosta na
# lateral do piso do pe e impede a peca de escorregar de volta para a posicao
# de encaixe. Fica do lado do recorte, um para cada sentido de deslocamento.
# FRISO na aba (a "paredinha" da referencia do cliente): um L de relevo que
# o piso do pe de tras da peca de cima encosta -- a perna em y impede de
# escorregar de volta para a posicao de encaixe, a perna em x prende para
# fora. O rim continua plano em todo o resto.
FRISO_H, FRISO_T = 2.5, 1.2   # altura acima da aba e espessura da paredinha
# FOLGA do berco do friso. Era 0,3, e medindo o empilhamento em 22/09 isso
# apareceu como defeito: em x a sobra entre o piso do pe e a perna do friso
# ficava em 0,21 mm -- MENOS do que a tolerancia da propria injecao (±0,4 mm
# em 200 mm de PP, 0,2%). Ou seja, na pratica as duas pecas podiam nem
# assentar. Em 0,8 mm o berco continua travando (para escapar da aba o pe
# precisa andar 3,1 mm, e para voltar a posicao de encaixe, 21 mm), e agora
# ha folga de montagem.
FRISO_F = 0.8
# Saida das pernas do friso. Sem ela as pernas eram caixas de 0 grau: ruim
# para o molde e, pior, o berco nao tinha boca -- entrava com a folga exata.
# Com saida o friso fica mais estreito no alto, ou seja o berco ABRE para
# cima: o pe da peca de cima cai num funil e se centra sozinho.
FRISO_S = 8.0
# ACOPLAMENTO na borda: cauda de andorinha em PLANTA no bordo da aba.
# So e possivel por causa do encaixe raso: com passo de encaixe de 47 mm, tudo
# o que estiver acima de ALT - (ALT - 47) = 47 mm do topo da peca de cima fica
# ACIMA do rim da de baixo -- ou seja, nao custa nada no encaixe. A cauda mora
# nos 14 mm de cima, onde e de graca.
ACO2_H = 14.0                 # altura da cauda (z de 116 a 130)
ACO2_D = 4.0                  # avanco alem do plano da junta
ACO2_WN, ACO2_WT = 7.0, 11.0  # largura no pescoco e na ponta (trava em x)
ACO2_F = 0.2                  # folga por face na femea
# Passo minimo de encaixe imposto pelo pe: o de cima so entra no de baixo
# depois de descer NERV_T/NERV_KY em y (35,6 mm) e NERV_T/NERV_KX em x
# (29,7 mm). Ambos < ABA_W/tg(saida) = 47,1 mm, que e quem manda.

# --- opcoes CAMUFLADAS ------------------------------------------------------
H_FAIXA2 = 14.0            # faixa mais baixa: z de 116 a 130
# D: canaleta cavada DENTRO da faixa. So e possivel com gaveta lateral, e por
# isso o trilho avanca 1,8 mm em vez de 7,5: ele nao precisa passar por tras
# da parede da vizinha, so entrar na canaleta dela.
D_TRILHO = 1.8             # quanto o trilho avanca
D_BOCA   = 0.8             # profundidade da boca (o resto e bolso)
D_PESC   = (121.0, 125.0)  # z do pescoco do trilho
D_CAB    = (119.0, 127.0)  # z da cabeca do trilho
# E: travas curtas nas PONTAS da lateral, junto dos cantos, sem gaveta. O
# ressalto e a parede nua de 1,4 mm (nao o rim), o que derruba o avanco.
E_SALTO  = 5.0
E_GANCHO = (2.0, 4.0)      # espessura, quanto desce
E_Y      = ((-45.0, -13.0), (40.0, 72.0))
E_BERCO_Y, E_BERCO_L = (-3.0, 82.0), 16.0

# --- vazado -----------------------------------------------------------------
PASSO   = 21.0            # >= D_TOPO + 6 mm de web, senao os furos se fundem
D_TOPO  = 15.0
D_BASE  = 6.0
Z_TOPO  = ALT - H_RIM - 9.0
BANDA   = 40.0            # faixa cega no pe da parede
FOLGA_S = 9.0             # folga entre furo e a silhueta (laterais)
FOLGA_F = 6.0             # idem na frente, onde a borda e o arco da silhueta

# --- LISTRAS VERTICAIS ------------------------------------------------------
# Substituem as bolinhas (pedido de 21/09): mesma casca, mesmas curvas, mesma
# estrutura -- muda so o vazado. Uma listra tira mais area que a bolinha que
# ela substitui, entao a peca sai mais leve sem mexer em parede nenhuma.
VAZADO = "listra"         # "listra", "bolinha" (o desenho antigo) ou "nenhum"

# Vazado da CHAPA DO FUNDO. Desligado no P e no M -- eles guardam miudeza e o
# cliente pediu fundo fechado. Ligado no G, que guarda coisa volumosa: a chapa
# e um terco do peso da peca de 30 L, e e a unica alavanca de peso grande que
# sobrava no projeto (o README aponta isso desde a secao 4.2.3).
FUNDO_VAZADO = False
FUN_W, FUN_P = 14.0, 22.0     # rasgo e passo da chapa
FUN_MARG = 26.0               # margem ate a parede: livra o pe e a saia
# TRES FAIXAS e rasgo pequeno (pedido de 22/09): "esse produto e para
# organizar pecas pequenas, tem um perigo dos produtos sairem por esses rasgos
# atuais". O rasgo era 10 x 31,5 mm = 315 mm2 de vao por listra; agora e
# 6 x 18,3 = 110 mm2, um terco, e nada com mais de 6 mm passa.
# A NERVURA entre listras fica em 5 mm, igual a de antes (LIS_P - LIS_W): o
# ritmo do desenho e a proporcao de fecha-macho no molde nao mudam, so o
# tamanho do vao.
LIS_W = 6.0               # largura da listra, no plano da parede
LIS_P = 11.0              # passo entre listras (nervura de 5 mm entre elas)
LIS_H = 18.0              # altura ALVO da listra (o numero de faixas sai dela)
# Medido: o que pesa nao e a largura da listra, e o NUMERO DE FAIXAS -- cada
# faixa a mais e uma nervura horizontal de LIS_WEB dando a volta na peca
# inteira -- e a AREA ABERTA total. De 2 faixas para 3 entram 7,4 g (160,3
# -> 167,7, medido nesta largura). Ja a
# largura sai quase de graca, porque estreitar a listra encurta o passo e
# entram mais colunas: 8/13, 7/12, 6/11, 6/10 e 5/9 pesam todas entre 166,4 e
# 167,7 g. Ou seja: o tamanho do rasgo e decisao de FUNCAO, nao de peso.
# Varredura completa (3 faixas, com a area aberta e o numero de furos, que e
# custo de fecha-macho no molde):
#   W/P    furos   peso     aberto
#   8/13    111   166,6 g   13715 mm2
#   7/12    123   166,8 g   13575
#   6/13    123   169,1 g   11769
#   6/11    135   167,7 g   12892   <- escolhido: mantem a nervura de 5 mm
#   6/10    145   166,4 g   13873
#   5/11    135   170,2 g   10889
#   5/9     167   167,1 g   13330   <- se quiser barrar tambem o que tem 5 mm
#   4/8     201   167,3 g   13187
LIS_WEB = 8.0             # nervura horizontal entre as faixas
LIS_MIN = 9.0             # listra menor que isso e descartada
# FOLGA entre a listra e a PEGADA DO PE, na lateral. A grade global de
# colunas (centrada em y = 0) nao sabia do pe e deixava duas colunas em cima
# dele: uma CORTADA pela aresta -- o cliente viu e pediu para tirar (22/09) --
# e outra escondida atras. E as duas vizinhas ficavam a distancias diferentes:
# 6,0 mm de um lado e 1,01 mm do outro, uma lasca de parede justo onde o pe
# descarrega na casca. Agora as colunas da lateral nascem DO PE para fora
# (cols_lateral), entao a nervura fica em LIS_P - LIS_W em toda a lateral e a
# folga ate o pe e esta, dos dois lados, por construcao.
LIS_FOLGA_PE = 4.0

TAN = np.tan(np.radians(DRAFT))
BASE_X = LARG - 2 * ALT * TAN
BASE_Y = PROF - 2 * ALT * TAN


def secao(z, folga=0.0):
    """Planta externa na cota z (a boca e LARG x PROF no topo)."""
    return (BASE_X + 2 * z * TAN - 2 * folga,
            BASE_Y + 2 * z * TAN - 2 * folga)


def silhueta(folga=0.0):
    """Perfil lateral (plano YZ) com as pontas arredondadas. Frente em -Y.

    `folga` empurra a frente e o fundo para FORA. Serve para a ABA PARA FORA:
    ela avanca ABA_W alem da parede, e o recorte da silhueta do CORPO a
    amputava em y (medido: sobravam 0,26 mm da aba de tras em vez de 10, e
    por isso a saia de tras pousava no vazio). Com folga = ABA_W o perfil
    acompanha a mesma dobra do rim, 10 mm para fora -- inclusive no chanfro de
    topo, onde a aba tem de seguir a borda que desce.
    """
    yf, yb = -PROF / 2 - folga, PROF / 2 + folga
    pts = [
        (yb, 0.0),                       # fundo, atras
        (yb, ALT),                       # costas, no alto
        (yf + CHANFRO, ALT),             # topo corre ate o inicio do chanfro
        (yf, ALT - CHANFRO),             # chanfro de topo, 45 graus
        (yf, CHANFRO_PE),                # face frontal
        (yf + CHANFRO_PE, 0.0),          # chanfro do pe, 45 graus
    ]
    sk = make_face(Polyline(*pts, close=True))
    # pontas dos dois chanfros
    sk = fillet(sk.vertices().filter_by_position(
        Axis.X, yf + CHANFRO_PE - 1, yf + CHANFRO + 1), R_CANTO)
    # quinas da face frontal
    sk = fillet(sk.vertices().filter_by_position(Axis.X, yf - 1, yf + 1), R_FRENTE)
    return sk


def y_frente(x, z):
    """y da superficie EXTERNA da frente, na cota z e na posicao x.

    Precisa do raio de canto: perto das pontas a planta volta para dentro, e
    e por isso que a borda da frente sobe la (ela e o corte da silhueta na
    casca inclinada). E esse arco que faz as "meias bolas" quando um furo
    tromba nele.
    """
    w, h = secao(z)
    r = 14.0 + z * TAN
    reto = w / 2 - r
    if abs(x) <= reto:
        return -h / 2
    dx = min(abs(x) - reto, r)
    return -(h / 2 - r + np.sqrt(max(r * r - dx * dx, 0.0)))


def z_livre_frente(x, meia, folga):
    """Cota maxima que um vazado da frente pode ocupar, na coluna x.

    Avalia no x da coluna mais proximo do meio, que e onde a borda arqueada
    esta mais BAIXA (no meio z_silhueta vale ~89 mm, nas pontas ~118). E essa
    cota que as listras seguem: em vez de descartar a listra que tromba na
    borda, ela e ENCURTADA ate caber -- o desenho acompanha a curva.
    """
    xs = np.sign(x) * max(abs(x) - meia, 0.0)
    z = ALT
    for _ in range(12):                      # y_frente depende de z: itera
        z = z_silhueta(y_frente(xs, z)) - folga
    return z


def cabe_na_frente(x, z, d, folga):
    """O furo redondo da frente respeita a borda arqueada?"""
    return z + d / 2 <= z_livre_frente(x, d / 2, folga)


def z_silhueta(y):
    """Cota do topo da silhueta em y -- usada para recortar o campo de furos."""
    yf = -PROF / 2
    if y >= yf + CHANFRO:
        return ALT
    return (ALT - CHANFRO) + (y - yf)      # a 45 graus


def filas(z_topo=None):
    z_topo = Z_TOPO if z_topo is None else z_topo
    n = int((z_topo - BANDA) // PASSO) + 1
    ds = np.linspace(D_TOPO, D_BASE, n)
    return [(z_topo - i * PASSO, float(ds[i])) for i in range(n)]


def listras(z_topo=None):
    """Faixas (z0, z1) das listras, entre BANDA e z_topo.

    O numero de faixas sai da altura alvo, nao o contrario: assim a frente
    (que tem menos altura util, por causa do arco da borda) fica com listras
    da MESMA altura das laterais, so em menos faixas. O pe da parede (BANDA)
    continua cego.
    """
    z_topo = Z_TOPO if z_topo is None else z_topo
    n = max(int(round((z_topo - BANDA + LIS_WEB) / (LIS_H + LIS_WEB))), 1)
    h = (z_topo - BANDA - (n - 1) * LIS_WEB) / n
    return [(BANDA + i * (h + LIS_WEB), BANDA + i * (h + LIS_WEB) + h)
            for i in range(n)]


def _listra(w, z0, z1, plano, comp):
    """Uma listra: estadio vertical de w x (z1-z0), no plano dado.

    plano=Plane.XZ corta na direcao y (frente e fundo); Plane.YZ corta na
    direcao x (laterais). O raio das pontas e w/2 -- nenhum canto vivo, que e
    o que o cliente pediu para todo o resto da peca tambem.
    """
    sk = RectangleRounded(w, z1 - z0, w / 2 - 0.001)
    return Pos(0, 0, (z0 + z1) / 2) * extrude(plano * sk, comp, both=True)


def cols_lateral():
    """Colunas de listra da lateral, ANCORADAS NO PE em vez de em y = 0.

    A pegada do pe cresce com z (meia-largura L/2 + ky*z), entao quem manda e
    a cota mais ALTA do campo de listras -- e la que ele e mais largo. A
    primeira coluna de cada lado fica a LIS_FOLGA_PE da pegada, e dali em
    diante o passo e LIS_P ate acabar a lateral. O limite e o mesmo da grade
    antiga, para o campo nao crescer por acidente.
    """
    yc, L, _, ky, _, _ = PES[0]
    meia = L / 2 + ky * listras()[-1][1]          # pegada no topo do campo
    d0 = meia + LIS_W / 2 + LIS_FOLGA_PE
    lim = (secao(BANDA, T_RIM)[1] - LIS_W - 30) / 2
    out = []
    for s in (-1, 1):
        y = yc + s * d0
        while abs(y) <= lim:
            out.append(y)
            y += s * LIS_P
    return sorted(out)


def _vazado_fundo():
    """Rasgos na chapa do fundo, prismaticos em z.

    Saem por fechamento macho-femea como os da parede: o macho desce pela
    cavidade e encosta na placa que forma a face de baixo da chapa. Sem
    gaveta, sem contra-saida.

    A margem FUN_MARG livra o pe (que e contraforte encostado na parede) e a
    saia de tras. Nao e chute: `fechado.py` mede a sola do pe e acusa se um
    rasgo abrir dentro dela.
    """
    if not FUNDO_VAZADO:
        return None
    sx, sy = secao(H_PE)
    lx, ly = sx - 2 * FUN_MARG, sy - 2 * FUN_MARG
    if lx < FUN_P or ly < FUN_P:
        return None
    campo = Pos(0, 0, H_PE - 1.0) * extrude(
        RectangleRounded(lx, ly, 12.0), T_FUNDO + 2.0)
    corte = []
    for x in grade(lx, FUN_P):
        corte.append(Pos(x, 0, H_PE - 1.0) * extrude(
            RectangleRounded(FUN_W, ly + 4.0, FUN_W * 0.45), T_FUNDO + 2.0))
    return corte and (sum(corte[1:], corte[0]) & campo) or None


def y_parede():
    """Onde plantar o prisma que corta a parede da FRENTE e a do FUNDO.

    Era 95,0 literal -- PROF/2 - 20 para os 230 mm do P. Com PROF = 400 o
    prisma (de +-35 mm de meia-profundidade) passa a 60..130 enquanto a parede
    esta em 200: erra a parede inteira e a peca sai MACICA na frente e no
    fundo. Medido assim antes de eu ver: o candidato de 380 x 400 pesou 630 g
    com as duas faces cheias.
    """
    return PROF / 2 - 20.0


def grade(extensao, passo):
    n = int(np.floor(extensao / passo))
    if n % 2 == 0:
        n -= 1
    return [(-(n - 1) * passo / 2) + i * passo for i in range(n)]


X_OUT = LARG / 2 + SALTO      # plano externo do macho (opcoes A e C)
Z_B0 = ALT - H_BANDA          # base da faixa da canaleta
X_B = LARG / 2 + B_BOCA + B_BOLSO + B_COSTAS   # plano externo do bloco femea
Z_D0 = ALT - H_FAIXA2         # base da faixa das opcoes D e E


def _colar():
    """Faz a face EXTERNA da faixa ficar vertical (saida zero).

    Sem isso as duas faixas se tocam so no fio do rim e divergem 2 mm ate a
    base da faixa -- com ela ha face de encosto de verdade, 14 x 132 mm.
    """
    return Pos(0, 0, Z_D0) * extrude(
        RectangleRounded(LARG, PROF, 14.0 + ALT * TAN), H_FAIXA2)


def _trilho_D(y0, y1):
    """Trilho raso de 1,8 mm: pescoco de 0,8 e cabeca de 1,0 atras dele."""
    s = _caixa(1, LARG / 2, LARG / 2 + D_BOCA, y0, y1, *D_PESC)
    s += _caixa(1, LARG / 2 + D_BOCA, LARG / 2 + D_TRILHO, y0, y1, *D_CAB)
    return s


def _canaleta_D(y0, y1):
    """Canaleta cavada na faixa: boca estreita na face, bolso largo atras.

    Aberta na FRENTE (por onde o trilho entra, no fim do chanfro) e FECHADA no
    fundo: assim o trilho encosta e a peca para de correr no comprimento.
    """
    f = 0.3
    c = _caixa(-1, LARG / 2 - D_BOCA, LARG / 2 + 3, y0 - 9, y1 + 0.4,
               D_PESC[0] - f, D_PESC[1] + f)
    c += _caixa(-1, LARG / 2 - D_TRILHO - f, LARG / 2 - D_BOCA, y0 - 9,
                y1 + 0.4, D_CAB[0] - f, D_CAB[1] + f)
    return c


def _nervura(env, sx, y0, y1):
    """Nervura externa com o pe na diagonal (o 'pe' das fotos 03 e 04)."""
    xo0 = EMP_X0
    xo1 = EMP_X0 + EMP_S * (ALT - EMP_Z0)
    pts = [(sx * xo0, EMP_Z0), (sx * xo1, ALT), (sx * 90.0, ALT),
           (sx * 90.0, EMP_Z0 + EMP_DIAG), (sx * (xo0 - EMP_APOIO), EMP_Z0)]
    sk = make_face(Polyline(*pts, close=True))
    s = Pos(0, (y0 + y1) / 2, 0) * extrude(Plane.XZ * sk, (y1 - y0) / 2,
                                          both=True)
    return s - env


def _parede_borda(sx, y0, y1, macho=None):
    """A parede que sai da borda superior e recebe a nervura de cima.

    macho=True poe a cauda de andorinha do acoplamento na face externa dela;
    macho=False abre a canaleta correspondente.
    """
    x0, z0, z1 = LARG / 2, ALT, ALT + EMP_H
    p = _caixa(sx, EMP_XI, x0, y0, y1, z0, z1)
    # chanfro de entrada no topo interno, para guiar a descida da nervura
    p -= _caixa(sx, EMP_XI - 2, EMP_XI + 1.4, y0 - 1, y1 + 1,
                z1 - 1.4, z1 + 1)
    if macho is None:
        return p
    yc = (y0 + y1) / 2
    if macho:
        p += _caixa(sx, x0, x0 + ACO_PESC, yc - ACO_WR / 2, yc + ACO_WR / 2,
                    z0, z1)
        p += _caixa(sx, x0 + ACO_PESC, x0 + ACO_P, yc - ACO_WC / 2,
                    yc + ACO_WC / 2, z0, z1)
    else:
        f = ACO_F
        p -= _caixa(sx, x0 - ACO_PESC, x0 + 1, yc - ACO_WR / 2 - f,
                    yc + ACO_WR / 2 + f, z0, z1 + 1)
        p -= _caixa(sx, x0 - ACO_P - f, x0 - ACO_PESC, yc - ACO_WC / 2 - f,
                    yc + ACO_WC / 2 + f, z0, z1 + 1)
    return p


def _pezinhos():
    """4 pezinhos ocos sob a chapa, abertos embaixo (pino da cavidade).

    A face externa acompanha a BASE: com saida maior a base encolhe, e um
    pezinho de cota fixa sairia para fora da parede -- foi o que aconteceu ao
    subir a saida de 3,5 para 9 graus, e matava o encaixe.
    """
    pe_x = BASE_X / 2 - 2.0
    out = None
    for sx in (-1, 1):
        for y0, y1 in PE_Y:
            b = _caixa(sx, pe_x - PE_W, pe_x, y0, y1, 0.0, H_PE + T_FUNDO)
            b -= _caixa(sx, pe_x - PE_W + PE_T, pe_x - PE_T,
                        y0 + PE_T, y1 - PE_T, -1.0, H_PE)
            out = b if out is None else out + b
    return out


def _soquetes(fora, so_traseiro=True):
    """Bercos no rim que recebem os pezinhos da peca de cima.

    O traseiro ganha paredes (soquete) e e ele que trava a pilha na frente e
    atras -- daí o nome 'encaixe do pe traseiro'. ATENCAO: qualquer berco que
    avance para dentro do rim fecha o encaixe (a chapa da peca de cima tem
    99,9 mm de meia-largura e nao passa). E empilhar OU encaixar.
    """
    x_i = secao(ALT, T_RIM)[0] / 2
    out = None
    for sx in (-1, 1):
        for i, (y0, y1) in enumerate(PE_Y):
            b = _caixa(sx, PE_X - PE_W - 2, LARG, y0 - 3, y1 + 3,
                       ALT - 4.0, ALT) & fora
            if i == 1 and so_traseiro:        # soquete do pe traseiro
                xe, xd = PE_X - PE_W - SOQ_F, PE_X + SOQ_F
                for cx in ((xe - SOQ_T, xe), (xd, xd + SOQ_T)):
                    b += _caixa(sx, cx[0], cx[1], y0 - SOQ_F - SOQ_T,
                                y1 + SOQ_F + SOQ_T, ALT, ALT + SOQ_H)
                for cy in ((y0 - SOQ_F - SOQ_T, y0 - SOQ_F),
                           (y1 + SOQ_F, y1 + SOQ_F + SOQ_T)):
                    b += _caixa(sx, xe - SOQ_T, xd + SOQ_T, cy[0], cy[1],
                                ALT, ALT + SOQ_H)
            out = b if out is None else out + b
    return out
    """Trava curta com gancho, apoiada na parede nua de 1,4 mm da vizinha."""
    xo = LARG / 2 + E_SALTO
    s = _caixa(1, LARG / 2 - 6, xo, y0, y1, Z_D0, ALT) - env
    s += _caixa(1, xo - E_GANCHO[0], xo, y0, y1,
                Z_D0 - E_GANCHO[1], Z_D0) - env
    return s


def w(z):
    """Meia-largura externa da parede na cota z."""
    return LARG / 2 - ALT * TAN + TAN * z


def cotas_empilhamento():
    """Resolve as cotas do pino e da nervura a partir da saida de molde.

    passo_pilha = ALT + EMP_H - EMP_Z0, e o encaixe fica limitado a
    passo_encaixe >= passo_pilha/2 + (T_RIM + apoio + folga)/(2*tg(saida)):
    o pino esta no alto e o pe embaixo, e encaixando os dois se aproximam ao
    mesmo tempo -- cada milimetro conta duas vezes.
    """
    ps = ALT + EMP_H - EMP_Z0
    pn = ps / 2 + (T_RIM + EMP_APOIO_B + EMP_FOLGA_C) / (2 * TAN)
    xi = w(ALT + EMP_H - pn) + EMP_FOLGA_C
    return xi, xi + EMP_APOIO_B, pn, ps


def nerv_y():
    """Compatibilidade: as faixas em y dos pes (yc +- L/2)."""
    return [(yc - L / 2, yc + L / 2) for yc, L, *_ in PES]


def aba_x0():
    """x onde a aba nasce -- a face externa do rim, e o plano da junta."""
    return LARG / 2


def aba_x1():
    """x da aresta livre da aba."""
    return LARG / 2 + ABA_DIR * ABA_W


def pe_topo():
    """x da face externa do pe no RIM: ela morre na aresta livre da aba.

    Para fora, isso da ao pe a saida em x de que ele precisa para telescopar
    (ABA_W - ABA_POUSO sobre a altura) sem sair da silhueta.
    """
    return LARG / 2 + max(ABA_DIR, 0) * ABA_W


def pe_r00():
    """x do piso do pe: tem de alcancar a faixa de pouso da aba."""
    return (LARG / 2 + ABA_POUSO if ABA_DIR > 0
            else LARG / 2 - ABA_W + 3.0)


def _aba_dobra():
    """Dobra para baixo na aresta livre da aba (so quando ela vai para fora).

    Transforma o labio plano num PERFIL EM U: a altura de junta entre duas
    pecas acopladas passa de ABA_T (2,5 mm) para ABA_T + ABA_DOBRA, e a aresta
    -- que agora e o que bate primeiro numa queda e o que a mao pega -- deixa
    de ser uma lamina de 2,5 mm.
    """
    r = 14.0 + ALT * TAN + ABA_W
    z0 = ALT - ABA_T - ABA_DOBRA
    fr = RectangleRounded(LARG + 2 * ABA_W, PROF + 2 * ABA_W, r)
    dr = RectangleRounded(LARG + 2 * (ABA_W - ABA_DT),
                          PROF + 2 * (ABA_W - ABA_DT), max(r - ABA_DT, 1.0))
    return Pos(0, 0, z0) * (extrude(fr, ABA_DOBRA) - extrude(dr, ABA_DOBRA))


def _cauda2_vazio(sx, yc):
    """O vazio da cauda: a mesma planta recuada ACO2_T, aberta no TOPO."""
    x0 = aba_x1() if ABA_DIR > 0 else LARG / 2
    xi = LARG / 2 + ACO2_T                     # para na face externa do rim
    xe = x0 + ACO2_D - ACO2_T
    wn, wt = ACO2_WN - 2 * ACO2_T, ACO2_WT - 2 * ACO2_T
    pts = [(sx * xi, yc - wn / 2), (sx * x0, yc - wn / 2),
           (sx * xe, yc - wt / 2), (sx * xe, yc + wt / 2),
           (sx * x0, yc + wn / 2), (sx * xi, yc + wn / 2)]
    sk = make_face(Polyline(*pts, close=True))
    z0 = ALT - ACO2_H + ACO2_PISO
    return Pos(0, 0, z0) * extrude(sk, ALT + 2 - z0)


def _aba(fora, interno):
    """Aba plana de ABA_W no rim inteiro -- e nela que o pe pousa.

    Os recortes por onde o pe da peca de cima desce NAO sao feitos aqui: quem
    os abre e _pes_cavidade(), subtraida da peca inteira, de modo que o
    recorte da aba, a janela na parede e a cavidade do pe sejam UM unico
    solido (a mesma folga, por construcao).
    """
    r = 14.0 + ALT * TAN
    if ABA_DIR > 0:
        # PARA FORA: o anel e o que sobra da chapa maior depois de tirar o
        # CONE -- assim ela solda na parede sem folga em cota nenhuma, e a
        # face de baixo dela e um anel plano voltado para baixo, que a
        # cavidade forma descendo (a silhueta so cresce subindo).
        a = Pos(0, 0, ALT - ABA_T) * extrude(
            RectangleRounded(LARG + 2 * ABA_W, PROF + 2 * ABA_W, r + ABA_W),
            ABA_T)
        return a - extrude(RectangleRounded(BASE_X, BASE_Y, 14.0), ALT + 40,
                           taper=-DRAFT)
    a = Pos(0, 0, ALT - ABA_T) * extrude(
        RectangleRounded(LARG, PROF, r), ABA_T)
    a -= Pos(0, 0, ALT - ABA_T - 1) * extrude(
        RectangleRounded(LARG - 2 * ABA_W, PROF - 2 * ABA_W,
                         max(r - ABA_W, 1.0)), ABA_T + 2)
    return a


def _pe_planta(sx, yc, L, ky, r00, z, ox, oy, rc):
    """Planta do pe na cota z: retangulo ARREDONDADO do bico ao interior.

    O bico redondo e o que o cliente pediu ("lateral curvada, cantos
    arredondados"): o pe deixa de ser uma caixa e vira uma lingua. As pontas
    de dentro tambem sao arredondadas, mas ficam dentro da parede e somem no
    - env.
    """
    xi = 60.0                                  # bem dentro da parede
    r = r00 - ox + (pe_topo() - r00) * z / ALT
    h = L / 2 - oy + ky * z
    w = r - xi
    rr = min(rc, h * 0.95, w * 0.45) if rc > 0 else 0.0
    pl = (RectangleRounded(w, 2 * h, rr) if rr > 0.05
          else Rectangle(w, 2 * h))
    return Pos(sx * (r + xi) / 2, yc, z) * pl


def _pe_bloco(sx, yc, L, ky, r00, ox=0.0, oy=0.0, z0=0.0, z1=None,
              rc=NERV_RC):
    """Tronco do pe, por loft entre a planta do piso e a do rim.

    Face externa: de r00 no piso ate LARG/2 no rim -- sempre POR FORA do cone,
    de modo que a silhueta da peca nunca diminui subindo (nenhuma face virada
    para cima = nenhuma contra-saida).
    Faces em y: saida ky por lado. Sem ela a boca da cavidade (L - 2*parede)
    e sempre mais estreita que a lingua (L) e o pe NUNCA entra no pe.
    ox/oy/rc recuam a face externa, as laterais e o raio: e assim que se
    obtem a casca (a cavidade interna e o mesmo bloco com ox=oy=parede e
    rc = raio - parede, o que mantem a parede constante inclusive no bico).
    """
    if z1 is None:
        z1 = ALT + 6.0
    return loft([_pe_planta(sx, yc, L, ky, r00, z0, ox, oy, rc),
                 _pe_planta(sx, yc, L, ky, r00, z1, ox, oy, rc)])


def _pes_nervura(env):
    """Os pes: blocos por fora do cone (a cavidade sai depois, da peca toda)."""
    out = None
    for sx in (-1, 1):
        for yc, L, t, ky, r00, _ in PES:
            b = _pe_bloco(sx, yc, L, ky, r00, z1=ALT) - env
            out = b if out is None else out + b
    return out


def _pes_cavidade():
    """Cavidade interna do pe -- subtraida da PECA INTEIRA, nao do pe.

    Subtraida da peca toda ela faz tres coisas de uma vez:
      1. esvazia o pe (casca de `t`) de Z_CAV para cima;
      2. vaza a parede atras do pe (janela de L - 2*t, escondida de fora pela
         propria face externa do pe);
      3. abre o recorte na aba por onde a lingua do pe de cima desce.
    Sem a janela (2) o piso do pe de cima bateria na parede da peca de baixo:
    ele nasce na parede e avanca mais de 20 mm para fora, tem de atravessa-la.

    Comeca em Z_CAV e nao no piso: a janela (2) so e necessaria de z = passo
    de encaixe para cima, que e onde o pe da peca de cima realmente passa.
    Abaixo dali ela furava a chapa do fundo e a parede a troco de nada. O que
    esvazia o pe la embaixo e _pe_bolsa(), por baixo.

    A janela e a cavidade andam JUNTAS por necessidade geometrica, nao por
    escolha: se a parede ficasse inteira, o macho que forma a cavidade seria
    um dedo solto dentro do pe, e como o cone recua descendo (0,213/mm) mais
    depressa do que a face externa do pe avanca (0,046/mm), esse dedo
    ENGROSSA para baixo -- contra-saida, nao sai do molde. Por isso onde o pe
    e oco a parede e vazada, e onde a parede e cega o pe e esvaziado de baixo.
    """
    out = None
    for sx in (-1, 1):
        for yc, L, t, ky, r00, _ in PES:
            c = _pe_bloco(sx, yc, L, ky, r00, ox=t, oy=t, z0=Z_CAV,
                          rc=NERV_RC - t)
            out = c if out is None else out + c
    return out


def _pe_bolsa(env):
    """Bolsa CEGA sob o pe, aberta no piso -- e ela que esvazia o pe la embaixo.

    Com a cavidade comecando em Z_CAV o pe ficaria MACICO nos primeiros 40 mm:
    22 x 10 mm de secao por 40 de altura, 8 g de PP em cada pe e uma secao
    grossa que chuparia a face externa toda. Esta bolsa o esvazia.

    E formada POR BAIXO, entao a secao nao pode diminuir descendo -- e as duas
    faces do pe fecham para baixo (a externa recua 0,046/mm e a meia-largura
    em y, 0,045/mm). A bolsa nao pode acompanha-las: a face externa dela e
    VERTICAL (x = r00 - t) e a largura em y e CONSTANTE (L/2 - t). Assim a
    parede do pe sai de t no piso e engrossa ate ~3,3 mm no teto da bolsa --
    a mesma ordem do rim (T_RIM = 3,2), de modo que a secao mais grossa da
    peca nao muda. Por dentro quem fecha a bolsa e a propria casca (- env).

    CEGA por causa de CAV_MEMB: sobra uma membrana de 2 mm entre o teto da
    bolsa e o piso da cavidade. E ela que garante que nao ha caminho nenhum
    do interior do cesto para fora -- de dentro da peca a bolsa nao existe.
    """
    out = None
    for sx in (-1, 1):
        for yc, L, t, ky, r00, _ in PES:
            b = _caixa(sx, 40.0, r00 - t, yc - (L / 2 - t), yc + (L / 2 - t),
                       -1.0, Z_CAV - CAV_MEMB) - env
            out = b if out is None else out + b
    return out


def z_chanfro_pe():
    """Cota em que o chanfro do pe SAI da casca.

    Abaixo dela o chanfro passa por DENTRO da parede da frente e a apaga; e
    ate ali que a tapa tem de ir. Sai de
        (CHANFRO_PE - (PROF/2 - BASE_Y/2)) / (1 - tg(saida))
    e portanto DEPENDE DA SAIDA: 10,63 mm a 12 graus, 24,96 a 6. A primeira
    versao da tapa tinha a faixa fixa em 14 mm, o que bastava a 12 graus e
    reabriu 11 mm de rasgo quando a saida caiu para 6 na configuracao C.
    Nunca mais em numero fixo.
    """
    return (CHANFRO_PE - (PROF / 2 - BASE_Y / 2)) / (1 - TAN)


def _tapa_frente(fora, sil):
    """Fecha o RASGO INFERIOR FRONTAL: parede de T_PAREDE sobre o chanfro do pe.

    O chanfro do pe (45 graus, CHANFRO_PE = 36) corta a casca na faixa de
    baixo da frente. Ele passa POR DENTRO da parede ate z = 10,63 mm -- a
    conta e (CHANFRO_PE - (PROF/2 - BASE_Y/2)) / (1 - TAN) -- de modo que
    entre o topo da chapa do fundo (z = 7) e essa cota a parede da frente
    simplesmente NAO EXISTE. Medido no solido em x = 0: em z = 7,5 e em
    z = 8,0 nao ha material nenhum na frente. Um rasgo de ~3 mm de altura na
    largura inteira da frente, com a borda da chapa servindo de RAMPA para
    ele: exatamente por onde peca miuda escorre e sai (pedido de 22/09).

    E ainda: de z = 8,85 a 10,63 a parede sobrevivia como LAMINA de 0 a
    1,4 mm. Secao dessa ordem nao enche na injecao -- sairia rebarba ou falha,
    nao parede.

    A tapa e uma parede de T_PAREDE deitada SOBRE o plano do chanfro: a
    silhueta menos ela mesma deslocada T_PAREDE na normal do chanfro (45
    graus, logo T_PAREDE/raiz(2) em cada eixo). Intersectada com `fora` ela
    TERMINA SOZINHA onde o chanfro sai da casca e a parede de verdade comeca
    -- nao ha cota para acertar a mao, e se CHANFRO_PE mudar a tapa acompanha.

    Saida de molde: a face externa dela E o proprio plano do chanfro, que ja e
    a silhueta da peca; a interna e paralela, e subindo o vao interno so
    cresce. Sai nos dois lados sem nada novo. Por dentro fica uma transicao
    chanfrada de 3,6 mm no pe da parede da frente -- que de quebra ajuda a
    varrer o cesto.
    """
    d = T_PAREDE / np.sqrt(2.0)
    casca_sil = sil - Pos(0, d, d) * sil
    z1 = z_chanfro_pe() + 2.0            # derivada, nunca fixa (ver docstring)
    larg_y = z1 + 25.0                   # a linha do chanfro anda 1 mm por mm
    faixa = Pos(0, -PROF / 2 + larg_y / 2, (H_PE + z1) / 2) * Box(
        LARG + 60, larg_y, z1 - H_PE)
    return casca_sil & fora & faixa


def _saia_tras():
    """Saia da parede de tras, descendo ate o piso RENTE a parede.

    Substitui a canetinha (que projetava 4,6 mm e ficava a vista): aqui o pe
    de tras e a propria parede continuando para baixo na faixa de H_PE que
    `p -= extrude(..., H_PE)` tinha cortado. Como ela usa exatamente o mesmo
    cone da casca, fica RENTE -- nao ha saliencia nenhuma para se ver de
    fora. As pontas em planta sao arredondadas em SAIA_R.

    Custa ZERO no encaixe, e por construcao: a face externa dela E a
    superficie do cone, entao ela encaixa como a propria parede encaixa
    (basta passo >= T_PAREDE/tg = 6,6 mm).

    O apoio e a aresta de baixo, de SAIA_B de espessura: deslocada DESLOC ela
    pousa na aba de tras da peca de baixo.
    """
    faixa = extrude(RectangleRounded(BASE_X, BASE_Y, 14.0), H_PE + 0.2,
                    taper=-DRAFT)
    dentro = Pos(0, 0, -1.0) * extrude(
        RectangleRounded(BASE_X - 2 * SAIA_B, BASE_Y - 2 * SAIA_B,
                         max(14.0 - SAIA_B, 2.0)), H_PE + 3.0, taper=-DRAFT)
    rec = Pos(0, BASE_Y / 2 - 20.0, -0.5) * extrude(
        RectangleRounded(SAIA_W, 50.0, SAIA_R), H_PE + 1.5)
    return (faixa - dentro) & rec


def friso_x0():
    """Face interna do friso: o limite que o encaixe no impoe.

    A peca de cima, encaixada, cruza a cota do rim da de baixo com a parede
    em x = LARG/2 - ABA_W; subindo FRISO_H ela engorda TAN*FRISO_H. O friso
    tem de morar para fora disso, senao ele fecha o encaixe.
    """
    if ABA_DIR > 0:
        # para fora o limite e a propria aresta interna da aba, que E a face
        # externa do rim: a peca de cima passa por dentro dela
        return LARG / 2 + 0.6
    return LARG / 2 - ABA_W + TAN * FRISO_H + 0.6


def pe_apoio_h(L, r00, rc):
    """Meia-largura do piso do pe na face interna do friso.

    Com o bico redondo o piso do pe afina depressa, e e essa largura -- nao
    L/2 -- que posiciona a perna do friso. Medido: com L/2 sobravam 0,8 mm
    de folga e o friso praticamente nao travava em y (0,05 mm3 empurrando
    1 mm); com a largura na borda interna da aba, 0,27; aqui, na face do
    proprio friso, e onde o piso e mais largo dentro do vao da perna.
    """
    d = min(max(r00 - friso_x0(), 0.0), rc)
    return (L / 2 - rc) + np.sqrt(max(rc * rc - (rc - d) ** 2, 0.0))


def _frisos():
    """Friso em L na aba -- a paredinha da referencia do cliente.

    Tres pernas de FRISO_T x FRISO_H de relevo formando um U, no lugar onde o
    piso do pe de tras da peca de cima pousa: as duas pernas em y travam o
    deslocamento nos dois sentidos (uma delas impede de escorregar de volta
    para a posicao de encaixe) e a perna em x prende para fora. Com o friso
    dos dois lados, x fica preso nos dois sentidos tambem -- o empilhamento
    fica POSICIONADO, nao so apoiado.

    So no pe de tras e so no sentido +y. O deslocamento negativo nao serve: o
    chanfro de topo come a aba a partir de y = -PROF/2 + CHANFRO = -48, e o pe
    da frente deslocado -14 mm cairia no vazio (medido: 2 apoios em vez de 4).
    O friso aponta o unico sentido que tem apoio -- e a coluna sobe escalonada
    de DESLOC por andar.
    """
    x0 = friso_x0()
    out = None
    for sx in (-1, 1):
        for yc, L, t, ky, r00, friso in PES:
            if not friso:
                continue
            h = pe_apoio_h(L, r00, NERV_RC)
            ya = yc + DESLOC - h - FRISO_F              # face que o pe encosta
            yb = yc + DESLOC + h + FRISO_F
            # a secao nominal e a da cota da aba (z = ALT); as pernas
            # nascem 1 mm abaixo para soldar na aba e afinam subindo
            g = np.tan(np.radians(FRISO_S))
            pernas = [
                # perna em y: atravessa a aba, trava o deslocamento
                _caixa_s(sx, x0, r00 + FRISO_F + FRISO_T,
                         ya - FRISO_T - g, ya + g, ALT - 1, ALT + FRISO_H,
                         FRISO_S),
                # perna em x: corre ao lado do pe, trava para fora
                _caixa_s(sx, r00 + FRISO_F - g, r00 + FRISO_F + FRISO_T,
                         ya - FRISO_T - g, yb + FRISO_T + g,
                         ALT - 1, ALT + FRISO_H, FRISO_S),
                # perna em y do outro lado: fecha o berco
                _caixa_s(sx, x0, r00 + FRISO_F + FRISO_T,
                         yb - g, yb + FRISO_T + g, ALT - 1, ALT + FRISO_H,
                         FRISO_S),
            ]
            for b in pernas:
                out = b if out is None else out + b
    return out


def aba_livre():
    """Trechos de y da aba livres de recorte e de friso, no lado reto.

    A cauda de andorinha do acoplamento escava a aba de ACO2_D para dentro, e
    o friso mora justo ai: se as duas se encontrarem a femea corta a perna do
    friso. Por isso o berco entra na lista de ocupados.
    """
    r_topo = 14.0 + ALT * TAN
    lim = (-PROF / 2 + CHANFRO + 2, PROF / 2 - r_topo - 2)
    ocupado = []
    for yc, L, t, ky, r00, friso in PES:
        h = L / 2 - t + ky * ALT + 0.5
        ocupado.append((yc - h, yc + h))          # recorte da aba
        if friso:                                  # e o berco do friso
            hb = pe_apoio_h(L, r00, NERV_RC) + FRISO_F + FRISO_T + 0.5
            ocupado.append((yc + DESLOC - hb, yc + DESLOC + hb))
    ocupado.sort()
    livres, y = [], lim[0]
    for a, b in ocupado:
        if a - y > 1:
            livres.append((y, min(a, lim[1])))
        y = max(y, b)
    if lim[1] - y > 1:
        livres.append((y, lim[1]))
    return [(a, b) for a, b in livres if b > a]


def aco_y():
    """Centros das duas caudas de acoplamento, nos trechos livres da aba.

    Duas e nao uma: uma cauda sozinha trava a separacao mas deixa a peca
    girar em torno dela. Com dois pes por lateral sobra um trecho livre
    grande no meio, e as duas caudas cabem dentro dele.
    """
    livres = sorted(aba_livre(), key=lambda ab: ab[0] - ab[1])
    bons = [ab for ab in livres if ab[1] - ab[0] >= ACO2_WT + 3]
    if len(bons) >= 2:
        return sorted((a + b) / 2 for a, b in bons[:2])
    a, b = bons[0]
    m = (ACO2_WT + 3) / 2          # nas pontas do trecho: braco maximo
    return [a + m, b - m]


def _cauda2(sx, yc, dentro=False, f=0.0):
    """Cauda de andorinha em planta: pescoco estreito no plano da junta e
    ponta larga -- e isso que TRAVA a separacao lateral. Prismatica em z e
    aberta no topo: desmolda sem gaveta (a peca de cima desce e entra).

    dentro=True devolve a FEMEA: a mesma planta espelhada no plano da junta,
    escavada para dentro da aba.
    """
    x0 = aba_x1() if ABA_DIR > 0 else LARG / 2
    d = -ACO2_D if dentro else ACO2_D
    xi = x0 - 60.0 if not dentro else x0 + 1.5     # macho: entra na parede
    pts = [(sx * xi, yc - ACO2_WN / 2 - f),
           (sx * x0, yc - ACO2_WN / 2 - f),
           (sx * (x0 + d), yc - ACO2_WT / 2 - f),
           (sx * (x0 + d), yc + ACO2_WT / 2 + f),
           (sx * x0, yc + ACO2_WN / 2 + f),
           (sx * xi, yc + ACO2_WN / 2 + f)]
    sk = make_face(Polyline(*pts, close=True))
    h = ACO2_H + 1.0 if dentro else ACO2_H      # o macho para exatamente no rim
    return Pos(0, 0, ALT - ACO2_H) * extrude(sk, h)


def set_draft(graus):
    """Muda a saida de molde e recalcula tudo que depende dela."""
    global DRAFT, TAN, BASE_X, BASE_Y, EMP_XI, EMP_X0, PES
    DRAFT = graus
    TAN = np.tan(np.radians(graus))
    BASE_X = LARG - 2 * ALT * TAN
    BASE_Y = PROF - 2 * ALT * TAN
    EMP_XI, EMP_X0 = cotas_empilhamento()[:2]
    PES = tuple(t[:4] + (pe_r00(),) + t[5:] for t in PES)


def padrao():
    """A configuracao do projeto: a C, decidida em 23/09.

    Todo script do cad chama isto no lugar de set_draft(12), para que a
    geometria venha de UM lugar e nao de cada folha.
      corpo 180 x 230, envelope de planta 200 x 250 com a aba para fora,
      altura 130, saida 6 graus por lado.
    """
    set_envelope(180.0, 230.0, 6.0, alt=130.0, aba_dir=+1)


def padrao_m():
    """ELO M: a boca do corpo e 380 x 230 -- 2 x LARG_P + 2 x ABA_W.

    Nao e um numero escolhido, e o que faz DOIS P ACOPLADOS EMPILHAREM no M.
    A aba do P vai de 90 a 100 mm do eixo dele; dois P no passo de 200 tem as
    abas se encontrando em x = 100 e o conjunto vai de -100 a +300, ou seja
    400 mm de pegada de aba. Para o M ter a MESMA pegada, a aba dele tem de ir
    de 190 a 200 do seu eixo -- logo a boca do corpo e 380, e as paredes do M
    caem em x = -90 e +290, exatamente onde pousam os pes externos do par.

    A profundidade NAO muda: 230 nos dois. Por isso a silhueta lateral, os
    chanfros da frente (52 / 36) e o desenho da lateral ficam identicos ao P --
    so o x escala.
    """
    set_envelope(380.0, 230.0, 6.0, alt=130.0, aba_dir=+1)


def padrao_g():
    """ELO G: ~30 L com menos de 500 g, para coisa VOLUMOSA.

    A largura fica travada em 380 -- e ela que poe as paredes do G debaixo dos
    pes laterais do par de P. A profundidade e livre porque o par pousa
    RECUADO no fundo (medido: recuando, o contato volta aos mesmos 887 mm2 do
    M; centrado num G mais fundo cai para 54).

    O que muda em relacao ao P e ao M, e por que:
      - saida de 3 graus, nao 6: a 6 a base de uma peca de 220 mm de altura
        encolhe 46 mm e come a litragem
      - rasgo de parede maior: a 8% de parede aberta a peca de 30 L pesa 630 g
      - CHAPA DO FUNDO VAZADA: sao ~200 g de chapa numa peca de 30 L
    """
    global VAZADO, FUNDO_VAZADO, LIS_W, LIS_P, LIS_H, LIS_MIN
    VAZADO, FUNDO_VAZADO = "listra", True
    LIS_W, LIS_P, LIS_H, LIS_MIN = 14.0, 22.0, 34.0, 16.0
    set_envelope(380.0, 400.0, 3.0, alt=220.0, aba_dir=+1)


def set_envelope(larg, prof, graus, alt=None, aba_dir=None):
    """Troca a boca do CORPO, a altura e a saida de uma vez.

    A aba para fora muda o que 'envelope' quer dizer: o ponto mais largo da
    peca passa a ser a aresta livre dela, em LARG/2 + ABA_W. Entao LARG e
    PROF aqui sao a boca do CORPO, e o envelope e LARG + 2*ABA_W.
    """
    global LARG, PROF, ALT, ABA_DIR, FRENTE_H, Z_TOPO
    LARG, PROF = larg, prof
    if alt is not None:
        ALT = alt
        FRENTE_H = ALT - CHANFRO - CHANFRO_PE
        Z_TOPO = ALT - H_RIM - 9.0
    if aba_dir is not None:
        ABA_DIR = aba_dir
    set_draft(graus)


def passo_acoplado(acopl=None):
    """Distancia entre os eixos de duas pecas acopladas.

    Com a ABA PARA FORA o que se toca sao as arestas dela, nao as paredes:
    o passo e LARG + 2*ABA_W, nao LARG. Media com o valor errado, duas pecas
    aparecem 20 mm interpenetradas e a trava mede 7.551 mm3 de "interferencia"
    -- foi o que aconteceu na folha aba.png na primeira rodada da C.
    """
    if acopl == "B":
        return LARG + (X_B - LARG / 2)
    return LARG + 2 * ABA_W * max(ABA_DIR, 0)


def _caixa(sx, x0, x1, y0, y1, z0, z1):
    """Caixa no lado sx (+1 direita, -1 esquerda); x0/x1 sempre positivos."""
    return Pos(sx * (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * \
        Box(x1 - x0, y1 - y0, z1 - z0)


def _caixa_s(sx, x0, x1, y0, y1, z0, z1, s):
    """Caixa com saida de `s` graus por face -- mais ESTREITA no alto.

    A secao nominal e a de z0; em z1 ela perdeu tan(s)*(z1-z0) por face. Usada
    nas pernas do friso: e o que transforma o berco num funil.
    """
    d = np.tan(np.radians(s)) * (z1 - z0)
    return Pos(sx * (x0 + x1) / 2, (y0 + y1) / 2, z0) * extrude(
        Rectangle(x1 - x0, y1 - y0), z1 - z0, taper=s) if d < min(
        x1 - x0, y1 - y0) / 2 else _caixa(sx, x0, x1, y0, y1, z0, z1)


def _macho(env, y0, y1, yg1=None):
    """Aba saliente no lado +X, com gancho para baixo na ponta (opcoes A e C).

    Nasce na propria superficie da parede: a caixa entra no solido e o que
    sobra depois de subtrair o envelope e exatamente a saliencia. O gancho pode
    parar antes de y1: no raio do canto a parede da peca vizinha gira e entra
    no espaco dele.
    """
    s = _caixa(1, LARG / 2 - 6, X_OUT, y0, y1, Z_B0, ALT) - env
    s += _caixa(1, X_OUT - GANCHO_D, X_OUT, y0, yg1 or y1,
                Z_B0 - GANCHO_H, Z_B0) - env
    return s


def _lingueta_T(env, y0, y1):
    """Opcao B: lingueta corrida -- pescoco estreito e cabeca larga."""
    u0 = LARG / 2
    s = _caixa(1, u0 - 6, u0 + B_BOCA, y0, y1, *B_PESC) - env
    s += _caixa(1, u0 + B_BOCA, u0 + B_BOCA + B_BOLSO, y0, y1, *B_CAB) - env
    return s


def _canaleta_T(env, y0, y1):
    """Opcao B: bloco corrido na esquerda com a canaleta, aberta na frente.

    t = X_B - u, onde u e medido do plano da junta para dentro da femea.
    """
    def t(u):
        return X_B - u
    bloco = _caixa(-1, LARG / 2 - 6, X_B, y0, y1, Z_B0, ALT) - env
    # boca: de u=-2 (aberta para fora) ate u=B_BOCA
    cav = _caixa(-1, t(B_BOCA), t(-2.0), y0 - 8, y1 + 8,
                 B_PESC[0] - 0.4, B_PESC[1] + 0.4)
    # bolso: de u=B_BOCA ate u=B_BOCA+B_BOLSO+0.3
    cav += _caixa(-1, t(B_BOCA + B_BOLSO + 0.3), t(B_BOCA), y0 - 8, y1 + 8,
                  B_CAB[0] - 0.4, B_CAB[1] + 0.4)
    return bloco - cav


def _abre_rim(y0, y1):
    """Solido a subtrair para abrir o rim do lado -X (janela ou rebaixo)."""
    return _caixa(-1, LARG / 2 - 14, X_OUT + 8, y0, y1, Z_B0, ALT + 4)


def _risco(sx, faixas):
    """Risco decorativo da canaleta, em trechos de y."""
    out = None
    for y0, y1 in faixas:
        if y1 - y0 < 2:
            continue
        b = _caixa(sx, LARG / 2 - RISCO_D, X_OUT + 8, y0, y1,
                   ALT - 5.5, ALT - 2.5)
        out = b if out is None else out + b
    return out


def cesto(acopl=None, h_rim=None, empilha=False, estrutura=False,
          aba=False):
    """acopl: None, 'A' (trilho corrido), 'B' (trilho embutido), 'C' (travas).

    h_rim permite medir o custo da faixa de 18 mm sem nenhuma feicao.
    empilha=True poe os bercos/soquetes no rim -- o que fecha o encaixe.
    estrutura=True poe a estrutura de empilhamento POR FORA do rim, que
    empilha a 130 mm sem fechar o encaixe.
    """
    if h_rim is None:
        h_rim = (H_FAIXA2 if acopl in ("D", "E")
                 else H_BANDA if acopl else H_RIM)
    z_topo = ALT - h_rim - 9.0

    # casca tronco-piramidal
    fora = extrude(RectangleRounded(BASE_X, BASE_Y, 14.0), ALT, taper=-DRAFT)
    env = extrude(RectangleRounded(BASE_X, BASE_Y, 14.0), ALT + 40, taper=-DRAFT)
    interno = RectangleRounded(BASE_X - 2 * T_PAREDE, BASE_Y - 2 * T_PAREDE, 12.0)
    # Tubo aberto: a cavidade sai do MESMO plano z=0 e com a MESMA saida da
    # casca, entao a parede fica em T_PAREDE constante em toda a altura. (Se a
    # cavidade fosse deslocada para cima mantendo a planta da base, a parede
    # engrossaria em H_PE*tan(DRAFT) -- 0,5 mm, ou +35% de peso.)
    p = fora - extrude(interno, ALT + 10, taper=-DRAFT)
    # chapa do fundo assentada H_PE acima do piso
    p += fora & Pos(0, 0, H_PE) * extrude(
        RectangleRounded(LARG + 40, PROF + 40, 0.1), T_FUNDO)
    # sem saia: a parede termina na chapa e quem apoia sao os pezinhos
    p -= extrude(RectangleRounded(LARG + 40, PROF + 40, 0.1), H_PE)
    vf = _vazado_fundo()
    if vf is not None:
        p -= vf

    # faixa do rim: parede engrossada no alto
    cheio = fora - Pos(0, 0, T_FUNDO) * extrude(
        RectangleRounded(BASE_X - 2 * T_RIM, BASE_Y - 2 * T_RIM, 11.0),
        ALT, taper=-DRAFT)
    p += cheio & Pos(0, 0, ALT - h_rim) * extrude(
        RectangleRounded(LARG + 40, PROF + 40, 0.1), h_rim + 10)

    if acopl == "D":
        p += _colar() - extrude(interno, ALT + 10, taper=-DRAFT)

    # recorta pela silhueta: e isso que da a forma do STL de referencia
    sil = extrude(Plane.YZ * silhueta(), LARG / 2 + 30, both=True)
    p = p & sil
    # ... e devolve a parede que o chanfro do pe tinha comido na frente
    p += _tapa_frente(fora, sil)
    # A ABA entra DEPOIS do recorte, com a silhueta dela: para fora ela passa
    # de PROF/2 e o recorte do corpo a amputaria em y.
    if aba:
        folga = ABA_W if ABA_DIR > 0 else 0.0
        sil_aba = extrude(Plane.YZ * silhueta(folga),
                          LARG / 2 + 30 + folga, both=True)
        p += _aba(fora, interno) & sil_aba
        if ABA_DIR > 0 and ABA_DOBRA > 0:
            p += _aba_dobra() & sil_aba

    # --- vazado ---
    # Colunas calculadas UMA vez, na cota mais BAIXA do campo (onde a parede
    # e mais estreita), para que todas as faixas usem as mesmas colunas.
    if VAZADO == "nenhum":
        # parede cheia: e a referencia para medir a AREA ABERTA do vazado
        # (volume cheio menos volume vazado, sobre a espessura da parede)
        n = 0
    elif VAZADO == "listra":
        cols_fundo = grade(secao(BANDA, T_RIM)[0] - LIS_W - 30, LIS_P)
        cols_lat = cols_lateral()
        fl_lat = listras(z_topo)
        # a frente tem menos altura util: o arco da borda manda
        zf = min(z_livre_frente(x, LIS_W / 2, FOLGA_F) for x in cols_fundo)
        fl_fr = listras(zf)
        furos, n = [], 0
        for x in cols_fundo:
            lim = z_livre_frente(x, LIS_W / 2, FOLGA_F)
            for z0, z1 in fl_lat:                          # parede do fundo
                furos.append(Pos(x, y_parede(), 0)
                             * _listra(LIS_W, z0, z1, Plane.XZ, 35.0))
                n += 1
            for z0, z1 in fl_fr:                           # parede da frente
                zt = min(z1, lim)
                if zt - z0 < LIS_MIN:
                    continue
                furos.append(Pos(x, -y_parede(), 0)
                             * _listra(LIS_W, z0, zt, Plane.XZ, 35.0))
                n += 1
        for y in cols_lat:                                 # laterais
            # o chanfro de topo come a lateral perto da frente: a listra e
            # ENCURTADA ate caber, entao o desenho acompanha a diagonal
            lim = z_silhueta(y - LIS_W / 2) - FOLGA_S
            for z0, z1 in fl_lat:
                zt = min(z1, lim)
                if zt - z0 < LIS_MIN:
                    continue
                furos.append(Pos(0, y, 0) * _listra(
                    LIS_W, z0, zt, Plane.YZ, (LARG + 60) / 2))
                n += 2
        p -= furos
    else:
        fl = filas(z_topo)
        z_ref = fl[0][0]
        cols_fundo = grade(secao(z_ref, T_RIM)[0] - D_TOPO - 30, PASSO)
        cols_lat = grade(secao(z_ref, T_RIM)[1] - D_TOPO - 30, PASSO)
        furos, n = [], 0
        for z, d in fl:
            for x in cols_fundo:
                # frente e fundo furados SEPARADAMENTE: o mesmo cilindro
                # varando os dois obriga a aceitar o furo cortado pela borda
                # da frente (as "meias bolas").
                furos.append(Pos(x, y_parede(), z) * Rot(90, 0, 0)
                             * Cylinder(d / 2, 70.0))
                n += 1
                if cabe_na_frente(x, z, d, FOLGA_F):
                    furos.append(Pos(x, -y_parede(), z) * Rot(90, 0, 0)
                                 * Cylinder(d / 2, 70.0))
                    n += 1
            for y in cols_lat:
                if z + d / 2 + FOLGA_S > z_silhueta(y):
                    continue
                furos.append(Pos(0, y, z) * Rot(0, 90, 0)
                             * Cylinder(d / 2, LARG + 60))
                n += 2
        p -= furos

    # --- acoplamento lateral -------------------------------------------------
    yc0, yc1 = (48.0, 84.0) if estrutura else Y_CAN
    if acopl == "A":
        # trilho corrido de ponta a ponta + rim rebaixado do outro lado
        p += _macho(env, yc0, yc1, yc1 - 9)
        p -= _abre_rim(yc0 - 1.5, yc1 + 1.5)
        p += cheio & _caixa(-1, 60, X_OUT, yc0 - 3, yc1 + 3,
                            Z_B0 - GANCHO_H - 3, Z_B0)
    elif acopl == "B":
        # lingueta em T de um lado, canaleta em T do outro -- exige gaveta
        p += _lingueta_T(env, yc0, yc1)
        p += _canaleta_T(env, yc0, yc1)
    elif acopl == "D":
        p += _trilho_D(yc0, yc1)
        p -= _canaleta_D(yc0, yc1)
    elif acopl == "E":
        for ya, yb in E_Y:
            p += _macho_E(env, ya, yb)
            p -= _caixa(-1, LARG / 2 - 14, LARG / 2 + E_SALTO + 8,
                        ya - 1, yb + 1, Z_D0, ALT + 4)
    elif acopl == "C":
        vaos_m, vaos_f = [], []
        y_ant_m = y_ant_f = yc0
        for ya in Y_TRAVAS:
            p += _macho(env, ya, ya + TRAVA_L)
            jf0, jf1 = ya - 1, ya - 1 + JANELA_L
            p -= _abre_rim(jf0, jf1)
            p += cheio & _caixa(-1, 60, X_OUT, jf0 - 3, jf1 + 3,
                                Z_B0 - GANCHO_H - 3, Z_B0)
            vaos_m.append((y_ant_m, ya)); y_ant_m = ya + TRAVA_L
            vaos_f.append((y_ant_f, jf0)); y_ant_f = jf1
        vaos_m.append((y_ant_m, yc1)); vaos_f.append((y_ant_f, yc1))
        for sx, vaos in ((1, vaos_m), (-1, vaos_f)):
            r = _risco(sx, vaos)
            if r is not None:
                p -= r

    # --- bercos de apoio: 4 orelhas na face INTERNA do rim -------------------
    # A saia da peca de cima assenta nelas. Ficam dentro da peca, invisiveis de
    # fora, e o passo empilhado fica exatamente a altura: 130 mm.
    if aba:
        p += _pes_nervura(env)
        p += _saia_tras()
        p -= _pes_cavidade()
        p -= _pe_bolsa(env)
        p += _frisos()
        for yc in aco_y():
            p += _cauda2(1, yc) - env          # macho na direita
            p -= _cauda2(-1, yc, dentro=True, f=ACO2_F)   # femea na esquerda
        if ABA_DIR > 0:
            for yc in aco_y():                 # vazia o macho por cima
                p -= _cauda2_vazio(1, yc)
    elif not estrutura:       # com estrutura o pe e o fundo da nervura
        p += _pezinhos()
    if empilha:
        p += _soquetes(fora)
    if estrutura:
        for sx in (-1, 1):
            for y0, y1 in NERV_Y:
                p += _nervura(env, sx, y0, y1)
            for i, (y0, y1) in enumerate(PAR_Y):
                # hermafrodita: na direita a 1a parede e macho e a 2a femea;
                # na esquerda o contrario
                p += _parede_borda(sx, y0, y1, macho=((sx > 0) == (i == 0)))
    return p, n


def capacidade():
    cav = extrude(RectangleRounded(BASE_X - 2 * T_PAREDE, BASE_Y - 2 * T_PAREDE,
                                   12.0), ALT, taper=-DRAFT)
    cav -= extrude(RectangleRounded(LARG + 40, PROF + 40, 0.1), H_PE + T_FUNDO)
    cav = cav & extrude(Plane.YZ * silhueta(), LARG / 2 + 30, both=True)
    return cav.volume / 1e6


def main():
    dest = os.path.dirname(os.path.abspath(__file__))
    p, n = cesto()
    bb = p.bounding_box()
    print("CESTO ORGANIZAVEL EMPILHAVEL - forma adaptada do STL de referencia")
    print(f"Boca {LARG:.0f} x {PROF:.0f} mm | base {BASE_X:.1f} x {BASE_Y:.1f} mm "
          f"| altura {ALT:.0f} mm | saida {DRAFT:.1f} deg/lado")
    print(f"Silhueta: chanfro topo {CHANFRO:.0f} / pe {CHANFRO_PE:.0f} mm a 45 deg"
          f" | face frontal {FRENTE_H:.0f} mm | pontas R{R_CANTO:.0f} e R{R_FRENTE:.0f}")
    print(f"Pe: saia de {H_PE:.0f} mm (a parede desce abaixo da chapa) + 4 bercos"
          f" internos no rim de {BERCO_L:.0f} x {BERCO_P:.0f} x {BERCO_H:.0f}")
    print(f"Envelope {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm")
    print(f"Capacidade {capacidade():.2f} L | peso {p.volume*RHO:.1f} g "
          f"(volume {p.volume/1000:.1f} cm3)")
    fl = filas()
    print(f"Vazado: {len(fl)} bandas, D {' / '.join(f'{d:.1f}' for _, d in fl)} mm"
          f" | {n} furos | faixa cega {BANDA:.0f} mm | fundo solido")
    print(f"Area projetada {LARG*PROF/100:.0f} cm2")

    export_step(p, os.path.join(dest, "cesto.step"))
    export_stl(p, os.path.join(dest, "cesto.stl"))

    import trimesh
    import render
    m = trimesh.load(os.path.join(dest, "cesto.stl"))
    cor = (0.93, 0.44, 0.13)
    pilha = []
    for i in range(3):
        t = m.copy()
        t.apply_translation([0, 0, i * ALT])
        pilha.append((t, tuple(c * (1 - 0.05 * (i % 2)) for c in cor)))
    for arq, cena, d in [("01-cesto.png", [(m, cor)], (-1.0, -1.35, -0.62)),
                         ("02-frente.png", [(m, cor)], (0.03, -1.0, -0.16)),
                         ("dbg-lateral.png", [(m, cor)], (-1.0, 0.02, -0.02)),
                         ("03-empilhado.png", pilha, (-1.0, -1.25, -0.5))]:
        render.salvar(render.render(cena, direcao=d, largura=1400), 
                      os.path.join(dest, arq))
        print("gerado", arq)


if __name__ == "__main__":
    main()
