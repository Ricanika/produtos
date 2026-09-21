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
                       RectangleRounded, Rot, export_step, export_stl,
                       extrude, fillet, make_face)

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
ABA_F = 2.0                   # folga do recorte alem do pe
NERV_P = 24.0                 # profundidade do pe em x (>20,6: encosta na parede)
NERV_T = 1.6                  # parede do pe da frente
# Deslocamento em y que troca ENCAIXAR por EMPILHAR. 14 mm nao serve mais:
# com um pe por lateral o friso passou para o pe da FRENTE, cujo recorte na
# aba e mais largo (meia-boca 9,25 mm), e a perna do friso caia DENTRO do
# recorte -- o pe da peca encaixada batia nela e o encaixe subia para 73,4 mm.
# Minimo = meia-boca + L/2 + folga + espessura = 9,25 + 5 + 0,3 + 1,2 = 15,75.
DESLOC = 17.0

# DOIS pes por lateral (pedido de 18/09; o do meio saiu):
#   frente -- o pe que sustenta, na altura do rasgo curvado da silhueta
#   tras   -- o ENCAIXE: nervura fina, com o pino da referencia na aba
# (yc, L em y, parede, saida em y, face externa no piso, tem pino na aba)
# Um pe por lateral, na frente, com o friso. Atras nao tem pe: tem a
# CANETINHA, um friso curvo unico na sola da base (pedido de 21/09).
PES = (
    (-58.0, 10.0, 1.6, 0.045, LARG / 2 - ABA_W + 3.0, True),
)

# --- CANETINHA: o terceiro apoio, na sola da base atras ---------------------
# Uma so, no meio da parede de tras. Ela substitui os dois pes de tras: com os
# dois pes da frente forma um TRIPE, que e mais estavel que quatro apoios
# amontoados no meio do comprimento.
CAN_L = 20.0                  # largura em x
CAN_T = 1.2                   # parede (ela e oca, como os pes)
CAN_KX = 0.032                # saida das faces em x
CAN_D = 24.0                  # profundidade em y
CAN_P = 2.2                   # expoente do perfil curvo -- ver can_perfil()
CAN_B = 4.0                   # apoio sobre a aba de tras
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
FRISO_F = 0.3                 # folga entre o friso e o piso do pe
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

TAN = np.tan(np.radians(DRAFT))
BASE_X = LARG - 2 * ALT * TAN
BASE_Y = PROF - 2 * ALT * TAN


def secao(z, folga=0.0):
    """Planta externa na cota z (a boca e LARG x PROF no topo)."""
    return (BASE_X + 2 * z * TAN - 2 * folga,
            BASE_Y + 2 * z * TAN - 2 * folga)


def silhueta():
    """Perfil lateral (plano YZ) com as pontas arredondadas. Frente em -Y."""
    yf, yb = -PROF / 2, PROF / 2
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


def cabe_na_frente(x, z, d, folga):
    """O furo da frente respeita a borda arqueada?

    Avalia no topo do furo e no x dele mais proximo do meio, que e onde a
    borda esta mais BAIXA (no meio z_silhueta vale ~89 mm, nas pontas ~118).
    """
    zt = z + d / 2
    xs = np.sign(x) * max(abs(x) - d / 2, 0.0)
    return zt + folga <= z_silhueta(y_frente(xs, zt))


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


def _aba(fora, interno):
    """Aba plana de ABA_W no rim inteiro -- e nela que o pe pousa.

    Os recortes por onde o pe da peca de cima desce NAO sao feitos aqui: quem
    os abre e _pes_cavidade(), subtraida da peca inteira, de modo que o
    recorte da aba, a janela na parede e a cavidade do pe sejam UM unico
    solido (a mesma folga, por construcao).
    """
    r = 14.0 + ALT * TAN
    a = Pos(0, 0, ALT - ABA_T) * extrude(
        RectangleRounded(LARG, PROF, r), ABA_T)
    a -= Pos(0, 0, ALT - ABA_T - 1) * extrude(
        RectangleRounded(LARG - 2 * ABA_W, PROF - 2 * ABA_W,
                         max(r - ABA_W, 1.0)), ABA_T + 2)
    return a


def _pe_bloco(sx, yc, L, ky, r00, ox=0.0, oy=0.0, z0=0.0, z1=None):
    """Tronco do pe no lado sx, centrado em yc.

    Face externa: de r00 no piso ate LARG/2 no rim -- sempre POR FORA do cone,
    de modo que a silhueta da peca nunca diminui subindo (nenhuma face virada
    para cima = nenhuma contra-saida).
    Faces em y: saida ky por lado. Sem ela a boca da cavidade (L - 2*parede)
    e sempre mais estreita que a lingua (L) e o pe NUNCA entra no pe.
    ox/oy recuam a face externa e as laterais: e assim que se obtem a casca
    (a cavidade interna e o mesmo bloco com ox=oy=parede).
    """
    if z1 is None:
        z1 = ALT + 6.0
    kx = (LARG / 2 - r00) / ALT
    r0, r1 = r00 - ox + kx * z0, r00 - ox + kx * z1
    pts = [(sx * r0, z0), (sx * r1, z1),
           (sx * (r1 - NERV_P), z1), (sx * (r0 - NERV_P), z0)]
    bx = extrude(Plane.XZ * make_face(Polyline(*pts, close=True)),
                 PROF, both=True)
    h0 = L / 2 - oy + ky * z0
    h1 = L / 2 - oy + ky * z1
    q = [(yc - h0, z0), (yc + h0, z0), (yc + h1, z1), (yc - h1, z1)]
    by = extrude(Plane.YZ * make_face(Polyline(*q, close=True)),
                 LARG, both=True)
    return bx & by


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
      1. esvazia o pe (casca de `t`), deixando so o piso de apoio embaixo;
      2. vaza a parede atras do pe (janela de L - 2*t, escondida de fora pela
         propria face externa do pe);
      3. abre o recorte na aba por onde a lingua do pe de cima desce.
    Sem a janela (2) o piso do pe de cima bateria na parede da peca de baixo:
    ele nasce na parede e avanca mais de 20 mm para fora, tem de atravessa-la.
    """
    out = None
    for sx in (-1, 1):
        for yc, L, t, ky, r00, _ in PES:
            c = _pe_bloco(sx, yc, L, ky, r00, ox=t, oy=t, z0=t)
            out = c if out is None else out + c
    return out


def can_y0():
    """y da face externa da canetinha no piso.

    Ela pousa na aba de TRAS, e o deslocamento do empilhamento tambem e em y:
    a canetinha tem de nascer DESLOC mm mais para dentro para, deslocada,
    cair em cima da aba (y de PROF/2 - ABA_W a PROF/2).
    """
    return PROF / 2 - ABA_W + CAN_B - DESLOC


def can_perfil(oy, z0, z1, n=28):
    """Perfil curvo da face externa: y0 no piso, acelerando para PROF/2.

    CAN_P > 1 (concavo) e o que faz a canetinha FUNCIONAR, e a primeira
    tentativa com CAN_P < 1 (convexo) falhou por isto: a canetinha pousa na
    aba de TRAS, e o deslocamento do empilhamento tambem e em y -- deslocar
    nao tira o pe de cima de cima do recorte, porque o recorte ocupa a mesma
    faixa em y que a propria aba. Medido: 2 apoios em vez de 3, e o encaixe
    subiu de 46,9 para 73,4 mm.

    Com a curva concava a canetinha sobe devagar, o CONE a alcanca em z ~ 46
    mm e ela se apaga na parede -- ou seja, ela nunca chega a cota do rim e
    NAO abre recorte nenhum na aba. A peca encaixada passa a cota do rim da
    de baixo com a canetinha ainda em y = 113,8 mm, dentro da borda interna
    da aba (115). E a silhueta continua crescendo para cima em todo o
    percurso: nenhuma contra-saida.
    """
    y0 = can_y0() - oy
    y1 = PROF / 2 - oy
    zs = np.linspace(z0, z1, n)
    return [(y0 + (y1 - y0) * (z / ALT) ** CAN_P, z) for z in zs]


def can_ztopo():
    """Cota onde o cone alcanca a canetinha e ela se apaga na parede.

    Acima disso ela nao tem material, e a cavidade dela nao precisa (nem
    deve) subir mais: se subisse, abriria recorte na aba de tras.
    """
    for z in np.arange(0.0, ALT, 0.5):
        y = can_y0() + (PROF / 2 - can_y0()) * (z / ALT) ** CAN_P
        if y + 1.0 <= PROF / 2 - ALT * TAN + TAN * z - T_PAREDE:
            return float(z)
    return ALT


def _canetinha(oy=0.0, ox=0.0, z0=0.0, z1=None):
    """Bloco da canetinha: perfil curvo em y-z cortado por um prisma em x."""
    if z1 is None:
        z1 = can_ztopo()
    fora = can_perfil(oy, z0, z1)
    dentro = [(y - CAN_D, z) for y, z in reversed(fora)]
    by = extrude(Plane.YZ * make_face(Polyline(*fora, *dentro, close=True)),
                 LARG, both=True)
    h0 = CAN_L / 2 - ox + CAN_KX * z0
    h1 = CAN_L / 2 - ox + CAN_KX * z1
    q = [(-h0, z0), (h0, z0), (h1, z1), (-h1, z1)]
    bx = extrude(Plane.XZ * make_face(Polyline(*q, close=True)),
                 PROF, both=True)
    return by & bx


def friso_x0():
    """Face interna do friso: o limite que o encaixe no impoe.

    A peca de cima, encaixada, cruza a cota do rim da de baixo com a parede
    em x = LARG/2 - ABA_W; subindo FRISO_H ela engorda TAN*FRISO_H. O friso
    tem de morar para fora disso, senao ele fecha o encaixe.
    """
    return LARG / 2 - ABA_W + TAN * FRISO_H + 0.6


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
            ya = yc + DESLOC - L / 2 - FRISO_F          # face que o pe encosta
            yb = yc + DESLOC + L / 2 + FRISO_F
            pernas = [
                # perna em y: atravessa a aba, trava o deslocamento
                _caixa(sx, x0, r00 + FRISO_F + FRISO_T,
                       ya - FRISO_T, ya, ALT - 1, ALT + FRISO_H),
                # perna em x: corre ao lado do pe, trava para fora
                _caixa(sx, r00 + FRISO_F, r00 + FRISO_F + FRISO_T,
                       ya - FRISO_T, yb + FRISO_T, ALT - 1, ALT + FRISO_H),
                # perna em y do outro lado: fecha o berco
                _caixa(sx, x0, r00 + FRISO_F + FRISO_T,
                       yb, yb + FRISO_T, ALT - 1, ALT + FRISO_H),
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
            ocupado.append((yc + DESLOC - L / 2 - FRISO_F - FRISO_T - 0.5,
                            yc + DESLOC + L / 2 + FRISO_F + FRISO_T + 0.5))
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
    x0 = LARG / 2
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
    global DRAFT, TAN, BASE_X, BASE_Y, EMP_XI, EMP_X0
    DRAFT = graus
    TAN = np.tan(np.radians(graus))
    BASE_X = LARG - 2 * ALT * TAN
    BASE_Y = PROF - 2 * ALT * TAN
    EMP_XI, EMP_X0 = cotas_empilhamento()[:2]


def passo_acoplado(acopl):
    """Distancia entre os eixos de duas pecas acopladas."""
    return LARG + (X_B - LARG / 2) if acopl == "B" else LARG


def _caixa(sx, x0, x1, y0, y1, z0, z1):
    """Caixa no lado sx (+1 direita, -1 esquerda); x0/x1 sempre positivos."""
    return Pos(sx * (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * \
        Box(x1 - x0, y1 - y0, z1 - z0)


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

    # faixa do rim: parede engrossada no alto
    cheio = fora - Pos(0, 0, T_FUNDO) * extrude(
        RectangleRounded(BASE_X - 2 * T_RIM, BASE_Y - 2 * T_RIM, 11.0),
        ALT, taper=-DRAFT)
    p += cheio & Pos(0, 0, ALT - h_rim) * extrude(
        RectangleRounded(LARG + 40, PROF + 40, 0.1), h_rim + 10)

    if aba:
        p += _aba(fora, interno)
    if acopl == "D":
        p += _colar() - extrude(interno, ALT + 10, taper=-DRAFT)

    # recorta pela silhueta: e isso que da a forma do STL de referencia
    p = p & extrude(Plane.YZ * silhueta(), LARG / 2 + 30, both=True)

    # --- vazado ---
    # Colunas calculadas UMA vez, com a margem do maior diametro, para que
    # todas as fileiras usem as mesmas colunas e o reticulado alinhe.
    fl = filas(z_topo)
    z_ref = fl[0][0]
    cols_fundo = grade(secao(z_ref, T_RIM)[0] - D_TOPO - 30, PASSO)
    cols_lat = grade(secao(z_ref, T_RIM)[1] - D_TOPO - 30, PASSO)

    furos, n = [], 0
    for z, d in fl:
        for x in cols_fundo:
            # frente e fundo furados SEPARADAMENTE: o mesmo cilindro varando
            # os dois obriga a aceitar o furo cortado pela borda da frente
            # (as "meias bolas"). Separados, so a frente perde os furos que
            # tromba na borda -- o fundo, que vai ate o rim, fica cheio.
            furos.append(Pos(x, 95.0, z) * Rot(90, 0, 0)
                         * Cylinder(d / 2, 70.0))            # parede do fundo
            n += 1
            if cabe_na_frente(x, z, d, FOLGA_F):
                furos.append(Pos(x, -95.0, z) * Rot(90, 0, 0)
                             * Cylinder(d / 2, 70.0))        # parede da frente
                n += 1
        for y in cols_lat:                                   # laterais
            if z + d / 2 + FOLGA_S > z_silhueta(y):
                continue
            furos.append(Pos(0, y, z) * Rot(0, 90, 0) * Cylinder(d / 2, LARG + 60))
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
        p += _canetinha(z1=can_ztopo() + 2.0) - env
        p -= _pes_cavidade()
        p -= _canetinha(oy=CAN_T, ox=CAN_T, z0=CAN_T)
        p += _frisos()
        for yc in aco_y():
            p += _cauda2(1, yc) - env          # macho na direita
            p -= _cauda2(-1, yc, dentro=True, f=ACO2_F)   # femea na esquerda
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
