"""Pote quadrado modular em SAN - gerador parametrico.

Corpo em SAN (Sangel Standard Cristal, CODPROD 16811), tampa em PP, fita de
vedacao em TPE (Karinprene 45, CODPROD 997). Quatro alturas, uma boca so.

Uso:  python3 geometria.py          -> stl/*.stl + malhas.json + relatorio
      python3 geometria.py --teste  -> so as verificacoes

Convencoes
  - mm, Z para cima. Corpo: z=0 no plano de apoio (pe). Tampas, fita e copo
    sao desenhados com z=0 no TOPO DA BORDA do corpo; para montar, soma H.
  - Toda peca sai de UMA funcao: varre(perfil). O perfil e uma lista de aneis,
    e cada anel e um quadrado de cantos arredondados ('s', meio-lado, z, raio)
    ou um circulo ('c', raio, z). O anel e amostrado por RAIOS saindo de um
    centro c - todos os aneis de uma peca com o mesmo c e o mesmo N, entao
    ligar aneis vizinhos e so ligar ponto k com ponto k.
  - Raio de canto: r = 8 + (u - parede_interna(z)). E a regra da curva
    paralela. Com ela a folga no CANTO e igual a folga no LADO - se o raio
    ficasse fixo, a tampa encostaria no canto antes de encostar no lado.
"""
import json
import math
import os
import struct
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- cotas
SAIDA = 2.0                       # graus por face: e o que faz aninhar (rev. 2: era 3)
K = math.tan(math.radians(SAIDA))
MODULO = 57.0                     # altura do menor; os outros sao 2x, 3x, 4x
ALTURAS = [MODULO * n for n in (1, 2, 3, 4)]

# rev. 6: RETANGULAR, 13 x 10 cm por fora na borda (era quadrado de 13,4).
# Toda cota 'u' e o meio-COMPRIMENTO (eixo X); o meio-largura (eixo Y) e
# sempre u - DIF. Diferenca constante = curva paralela tambem no retangulo.
COMPRIMENTO, LARGURA = 130.0, 100.0          # medida maxima, na borda
DIF = (COMPRIMENTO - LARGURA) / 2            # 15
U_I = COMPRIMENTO / 2 - 4.9  # meio-comprimento INTERNO na boca - igual nos quatro
T = 2.0         # parede SAN
R_I = 8.0       # raio interno do canto (externo = 10), constante na altura
FUNDO_Z = 3.0   # face de baixo do fundo (o pe ocupa 0..3)
FUNDO_T = 2.2   # espessura do fundo

# borda: saia livre pendurada para fora, canal aberto para baixo
CANAL = 1.2     # canal entre parede e saia
SAIA_T = 1.6    # saia na raiz
SAIA_H = 7.0    # da borda ate o pe da saia
U_BORDA = U_I + T + CANAL + SAIA_T + 0.1   # 65,0 - meio-comprimento maximo

# pe comum (o mesmo nos quatro) e o bolsao da tampa que o recebe
PE_I, PE_O, PE_H = 45.0, 47.6, 3.0
BOLSAO = 48.2   # meio-lado do bolsao da tampa (folga 0,6 sobre o pe)

# nervuras anti-travamento no meio de cada lado, por dentro
NERV_E = 0.4    # quanto avanca para dentro (rev. 2: era 0,6)
NERV_L = 4.0    # largura
NERV_TOPO = 20.0  # comeca 20 mm abaixo da borda: fica fora da zona da fita

# tampa / vedacao
FOLGA = 0.25    # face do plug ate a parede do corpo, por lado
# rev. 3 (foto 4, perfil da referencia): a fita fica em GANCHO. Embaixo do
# plug ha duas ALETAS com uma FENDA entre elas; a borda de baixo da fita entra
# na fenda, a fita contorna a ponta da aleta de cima e sobe encostada no corpo
# REBAIXADO da tampa ate a aba. Quem veda e a faixa da fita SOBRE A PONTA da
# aleta de cima: uma linha estreita, nao a fita inteira. Cotas medidas a
# partir da PAREDE do corpo (u_int), negativo = para dentro.
# rev. 4: o VAO (fenda entre as aletas) ficou 3x mais fundo - 5,0 mm alem da
# ponta, era 1,55 - e a fita e RETA, dobrada na montagem. Para nao virar um
# anel macico de PP de 6 mm (chupa), as aletas viraram duas LAMINAS saindo
# de uma saia fina; o fundo do vao e a propria face da saia.
ALETA_PONTA = 1.85  # ponta da aleta de cima: a fita livre passaria 0,15 da parede
VAO = 5.0           # fundo do vao alem da ponta da aleta (rev. 3: 1,55)
VAO_REV3 = 1.55
FENDA_FUNDO = ALETA_PONTA + VAO     # 6,85: face da saia, medida da parede
ALETA_PONTA2 = 1.4  # ponta da aleta de baixo
Z_ALETA_RAIZ = -3.6     # topo da aleta de cima na raiz (rampa = saida da gaveta)
Z_ALETA_TOPO = -4.0     # topo da aleta de cima, na ponta
Z_FENDA_TETO = -5.3     # aleta de cima com 1,3 na ponta
Z_FENDA_PISO = -7.0     # vao de 1,7: aperta a fita de 2,0 em 15% (segura)
PLUG = 8.2              # pe da aleta de baixo (1,2)
# teca: aleta de 1,3 mm em madeira quebra - fica a cava no macico (rev. 1)
CAVA_Z0, CAVA_Z1 = -3.0, -13.4
CAVA_P = 1.62
PLUG_TECA = 16.0
FITA_T, FITA_L = 2.0, 10.0       # a fita pedida: 2 x 10 mm
SAIA_PLUG_T = 1.4  # parede de PP atras da fenda
TAMPA_T = 2.0   # espessura de casca da tampa
ABA_H = 3.0     # aba da tampa acima da borda = profundidade do bolsao

# tampa de bico + copo
# rev. 9: UM VAO SO. O copo REDONDO senta no vao entre o gargalo e a parede.
# O bico vai para um CANTO da tampa. Na boca do copo ha um REBORDO de 0,4 que
# passa por um LABIO da parede de PP e TRAVA embaixo dele (clique); o mesmo
# labio aperta 0,15 a parede do copo em volta e e a VEDACAO. Os drenos ficam
# no piso do vao, DENTRO do copo - por dentro da vedacao.
BICO_X, BICO_Y = 27.0, 12.0                   # centro do bico: canto +X +Y da tampa
GARG_O, GARG_R, GARG_T = 22.0, 8.0, 1.6      # gargalo quadrado: abertura 40,8 x 40,8
PISO_Z = ABA_H                                # o vao e o proprio tampo (sem rebaixo)
GARG_H = PISO_Z + 19.0                        # topo do gargalo (z acima da borda)
BEICO_A, BEICO_B, BEICO_P = 2.5, 4.0, 4.0     # beico em +X: abre 2,5, sobe 4
COPO_RO = 33.0                                # raio externo do copo acima do rebordo
COPO_T = 1.8                                  # parede de SAN
COPO_SAIDA = math.tan(math.radians(1.0))      # 1 grau por face
COPO_FUNDO = 52.0                             # profundidade interna (vira copo medidor)
COPO_ZB = PISO_Z + 0.3                        # boca do copo, 0,3 acima do piso
COPO_TETO = COPO_ZB + COPO_FUNDO
REBORDO = 0.4                                 # trava na boca do copo
REBORDO_H = 1.0
LABIO_APERTO = 0.15                           # labio da parede sobre o copo = vedacao
PAREDE_FOLGA = 0.4                            # do rebordo ate a parede, embaixo do labio
PAREDE_T = 1.6
PAREDE_H = 5.5                                # altura da parede sobre o tampo
R_PAREDE_I = COPO_RO + REBORDO + PAREDE_FOLGA # 33,8: face interna embaixo do labio
R_LABIO = COPO_RO - LABIO_APERTO              # 32,85
R_PAREDE_O = R_PAREDE_I + PAREDE_T            # 35,4
Z_LABIO0, Z_LABIO1 = 1.9, 2.9                 # faixa do labio, acima do piso
DRENO_L, DRENO_W = 12.0, 3.0

N_ANEL = 240    # pontos por anel no STL
N_VIEW = 144    # pontos por anel no visualizador


def u_int(z_rel):
    """Parede interna do corpo, medida a partir da borda (z_rel <= 0)."""
    return U_I + min(z_rel, 0.0) * K


def r_par(u, z_rel):
    """Raio de canto pela regra da curva paralela, num anel a altura z_rel."""
    return max(0.4, R_I + (u - u_int(z_rel)))


# ---------------------------------------------------------------- malha
def thetas(n):
    """Angulos adensados nas diagonais: e onde estao os cantos."""
    t = np.linspace(0, 2 * np.pi, n, endpoint=False) + np.pi / n
    return t + 0.18 * np.sin(4 * t)


def anel_quadrado(u, r, c, th, dif=None, ctr=(0.0, 0.0)):
    """Interseca raios saindo de c com o RETANGULO arredondado de meios-lados
    (u, u - DIF) e raio r. Bissecao na funcao de distancia: robusta para c
    fora do centro. u = 0 e o eixo (anel colapsado num ponto)."""
    if u <= 1e-9:
        return np.tile(np.array(ctr, float), (len(th), 1))
    dif = DIF if dif is None else dif
    assert u - dif > 0.5, f'anel estreito demais: u={u}'
    hs = np.array([u, u - dif])
    r = min(r, hs[1])
    d = np.stack([np.cos(th), np.sin(th)], 1)
    lo = np.zeros(len(th))
    hi = np.full(len(th), 4 * u + 2 * abs(c[0]) + 2 * abs(c[1]))
    cc = np.array(c)
    for _ in range(48):
        m = (lo + hi) / 2
        p = np.abs(cc + d * m[:, None] - np.array(ctr))
        q = p - (hs - r)
        sd = (np.linalg.norm(np.maximum(q, 0), axis=1)
              + np.minimum(np.maximum(q[:, 0], q[:, 1]), 0) - r)
        dentro = sd < 0
        lo = np.where(dentro, m, lo)
        hi = np.where(dentro, hi, m)
    return cc + d * ((lo + hi) / 2)[:, None]


def beico(th, p=BEICO_P):
    """Calombo suave em volta de theta=0 (lado +X): 1 no meio, 0 a +-90."""
    return np.maximum(np.cos(th), 0) ** p


def anel(spec, c, th):
    """('s', u, z, r[, A, B]) - A abre o anel para fora e B o levanta no
    lado +X, na forma de beico(). E o que faz o labio de verter."""
    if spec[0] in ('s', 'q'):
        u, z, r = spec[1:4]
        A, B = (spec[4], spec[5]) if len(spec) > 4 else (0.0, 0.0)
        q = spec[0] == 'q'
        xy = anel_quadrado(u, r, c, th, 0.0 if q else None, (BICO_X, BICO_Y) if q else (0.0, 0.0))
        if A or B:
            f = beico(th)
            d = np.stack([np.cos(th), np.sin(th)], 1)
            xy = xy + d * (A * f)[:, None]
            return np.column_stack([xy, z + B * f])
    else:
        _, rho, z = spec[:3]
        xy = np.array(c) + rho * np.stack([np.cos(th), np.sin(th)], 1)
    return np.column_stack([xy, np.full(len(th), z)])


def varre(perfil, c=(0.0, 0.0), n=N_ANEL, fechado=True):
    """Liga anel a anel. Triangulo com dois vertices iguais e PULADO: e o que
    deixa um anel colapsar num ponto (o eixo) sem furar a malha."""
    th = thetas(n)
    A = [np.round(anel(s, c, th), 6) for s in perfil]
    pares = list(zip(A, A[1:])) + ([(A[-1], A[0])] if fechado else [])
    tris = []
    for P, Q in pares:
        P2, Q2 = np.roll(P, -1, 0), np.roll(Q, -1, 0)
        for t in ((P, P2, Q2), (P, Q2, Q)):
            tri = np.stack(t, 1)                       # (n,3,3)
            ok = ~(np.all(tri[:, 0] == tri[:, 1], 1) | np.all(tri[:, 1] == tri[:, 2], 1)
                   | np.all(tri[:, 0] == tri[:, 2], 1))
            tris.append(tri[ok])
    T_ = np.concatenate(tris)
    return orienta(T_)


def volume(T_):
    return float(np.einsum('ij,ij->i', T_[:, 0], np.cross(T_[:, 1], T_[:, 2])).sum() / 6)


def orienta(T_):
    return T_[:, ::-1].copy() if volume(T_) < 0 else T_


def caixa(secoes):
    """Solido lofteado entre secoes de 4 pontos (x,y,z). Nervura."""
    tris = []
    S = [np.array(s, float) for s in secoes]
    for a, b in zip(S, S[1:]):
        for k in range(4):
            k2 = (k + 1) % 4
            tris += [(a[k], a[k2], b[k2]), (a[k], b[k2], b[k])]
    for s, inv in ((S[0], True), (S[-1], False)):
        t1, t2 = (s[0], s[1], s[2]), (s[0], s[2], s[3])
        tris += [t1[::-1], t2[::-1]] if inv else [t1, t2]
    return orienta(np.array(tris))


def roda(T_, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    R = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
    return T_ @ R.T


def move(T_, dz=0.0, dx=0.0, dy=0.0):
    return T_ + np.array([dx, dy, dz])


# ---------------------------------------------------------------- pecas
def arco(cx, cz, R, a0, a1, n, u_fn=None):
    out = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        out.append((cx + R * math.cos(a), cz + R * math.sin(a)))
    return out


def corpo(H, n=N_ANEL):
    """O pote. Tronco de piramide quadrada, 3 graus por face."""
    ui = lambda z: U_I - (H - z) * K           # parede interna
    uo = lambda z: ui(z) + T                   # parede externa
    zi = FUNDO_Z + FUNDO_T
    P = []
    s = lambda u, z, r: P.append(('s', u, z, r))
    s(0, FUNDO_Z, 0)
    # pe: anel de 2,6 x 3,0 - o MESMO nos quatro tamanhos
    for u, z in ((PE_I - 0.2, FUNDO_Z), (PE_I, 0.5), (PE_I + 0.5, 0.0),
                 (PE_O - 0.5, 0.0), (PE_O, 0.5), (PE_O + 0.2, FUNDO_Z)):
        s(u, z, 6.0 + (u - PE_O))
    # aresta do fundo, R3
    for u, z in arco(uo(FUNDO_Z + 3) - 3, FUNDO_Z + 3, 3.0, 270, 357, 5):
        s(u, z, R_I + T + (u - uo(z)))
    # parede externa ate o teto do canal
    zc = H - 1.8
    s(uo(zc), zc, R_I + T)
    # saia da borda: canal abre para BAIXO (lamina na cavidade), saia afina
    # para baixo - nenhuma contra-saida
    si0 = uo(H) + CANAL
    s(si0, zc, r_par(si0, 0))
    zs = H - SAIA_H
    si1 = si0 + (zc - zs) * K
    s(si1, zs, r_par(si1, 0))
    so1 = U_BORDA - (H - 1.0 - zs) * K
    s(so1, zs, r_par(so1, 0))
    s(U_BORDA, H - 1.0, r_par(U_BORDA, 0))
    s(U_BORDA - 0.5, H - 0.13, r_par(U_BORDA - 0.5, 0))
    s(U_BORDA - 1.0, H, r_par(U_BORDA - 1.0, 0))
    s(U_I + 0.6, H, r_par(U_I + 0.6, 0))
    s(U_I + 0.18, H - 0.18, r_par(U_I + 0.18, 0))
    s(U_I, H - 0.6, R_I)
    # parede interna ate o fundo, R3
    pts = arco(ui(zi + 3) - 3, zi + 3, 3.0, 357, 270, 5)
    for u, z in pts:
        s(u, z, max(0.4, R_I + (u - ui(z))))
    s(0, zi, 0)
    malha = varre(P, n=n)
    # nervuras anti-travamento: meio de cada lado, por dentro
    nerv = []
    z0, z1, z2 = zi + 3.5, H - NERV_TOPO - 4, H - NERV_TOPO
    for q in range(4):
        dif = DIF if q % 2 else 0.0        # lados compridos (+-Y) ficam DIF mais perto
        def sec(z, e, dif=dif):
            x0, x1 = ui(z) - dif - e, ui(z) - dif + 0.6
            h = NERV_L / 2
            return [(x0, -h, z), (x0, h, z), (x1, h, z), (x1, -h, z)]
        nb = caixa([sec(z0 - 0.01, 0.02), sec(z0 + 1.2, NERV_E), sec(z1, NERV_E), sec(z2, 0.02)])
        nerv.append(roda(nb, q * math.pi / 2))
    return np.concatenate([malha] + nerv), P


def _aba_e_plug(P, s, aletas=True):
    """Trecho comum das tampas, da aba ao pe do plug, por FORA.

    aletas=True (PP, foto 4): corpo rebaixado, aleta de cima com rampa,
    FENDA, aleta de baixo. A fita entra na fenda e sobe pelo rebaixo.
    aletas=False (teca): cava cortada no macico, fita deitada nela.
    """
    w = u_int
    s(U_BORDA - 0.5, ABA_H)
    s(U_BORDA, ABA_H - 0.5)
    s(U_BORDA, 0.0)
    if aletas:
        fs = lambda z: w(z) - FENDA_FUNDO          # face da saia = fundo do vao
        s(fs(0) + 0.6, 0.0)
        s(fs(-0.6), -0.6)
        s(fs(Z_ALETA_RAIZ), Z_ALETA_RAIZ)
        s(w(Z_ALETA_TOPO) - ALETA_PONTA - 0.3, Z_ALETA_TOPO)
        s(w(Z_ALETA_TOPO - 0.3) - ALETA_PONTA, Z_ALETA_TOPO - 0.3)
        s(w(Z_FENDA_TETO) - ALETA_PONTA, Z_FENDA_TETO)
        s(fs(Z_FENDA_TETO), Z_FENDA_TETO)
        s(fs(Z_FENDA_PISO), Z_FENDA_PISO)
        s(w(Z_FENDA_PISO) - ALETA_PONTA2, Z_FENDA_PISO)
        s(w(-PLUG + 0.4) - ALETA_PONTA2, -PLUG + 0.4)
        s(w(-PLUG) - ALETA_PONTA2 - 0.4, -PLUG)
        return lambda z: w(z) - FENDA_FUNDO - SAIA_PLUG_T, PLUG
    pf = lambda z: w(z) - FOLGA
    s(pf(0) + 0.6, 0.0)
    s(pf(-0.8), -0.8)
    s(pf(CAVA_Z0), CAVA_Z0)
    s(pf(CAVA_Z0) - CAVA_P, CAVA_Z0)
    s(pf(CAVA_Z1) - CAVA_P, CAVA_Z1)
    s(pf(CAVA_Z1), CAVA_Z1)
    s(pf(-PLUG_TECA + 0.8), -PLUG_TECA + 0.8)
    s(pf(-PLUG_TECA) - 0.8, -PLUG_TECA)
    return pf, PLUG_TECA


def saia_int(z):
    """Face interna da saia das tampas de PP."""
    return u_int(z) - FENDA_FUNDO - SAIA_PLUG_T


def tampa_pp(n=N_ANEL):
    """Tampa FECHADA, PP. Bolsao em cima recebe o pe do pote de cima."""
    P = []
    def s(u, z, r=None):
        P.append(('s', u, z, r_par(u, z) if r is None else r))
    s(0, 0.0, 0)
    s(BOLSAO, 0.0, 6.6)
    s(BOLSAO + 1.0, ABA_H, 7.6)               # rampa de entrada do pe
    si, _ = _aba_e_plug(P, s)
    s(si(-PLUG), -PLUG)
    s(si(ABA_H - TAMPA_T), ABA_H - TAMPA_T)
    s(BOLSAO + 1.0 + TAMPA_T, ABA_H - TAMPA_T, 8.0)
    s(BOLSAO + TAMPA_T, -TAMPA_T, 7.0)
    s(0, -TAMPA_T, 0)
    return varre(P, n=n), P


def tampa_teca(n=N_ANEL):
    """Tampa de TECA maciça, CNC. A MESMA cava, a MESMA fita.
    Escavada por baixo: deixa 5 mm de madeira no centro e 5 na lateral."""
    P = []
    def s(u, z, r=None):
        P.append(('s', u, z, r_par(u, z) if r is None else r))
    s(0, 0.0, 0)
    s(BOLSAO, 0.0, 6.6)
    s(BOLSAO + 1.0, ABA_H, 7.6)
    pf, pl = _aba_e_plug(P, s, aletas=False)
    s(pf(-pl) - 5.0, -pl)
    s(pf(-5.0) - 5.0, -5.0)
    s(0, -5.0, 0)
    return varre(P, n=n), P


def tampa_bico(n=N_ANEL):
    """Tampa de BICO (rev. 9). PP. Bico num canto, um vao so.

    Por cima, de fora para dentro: aba -> tampo -> PAREDE redonda (com o
    LABIO que trava e veda o copo) -> VAO (o proprio tampo, com os drenos)
    -> GARGALO de abertura quadrada com beico em +X. Laco varrido com raios
    saindo do centro do bico; os drenos saem por subtracao booleana.
    """
    P = []
    def q(u, z, r, A=0.0, B=0.0):
        P.append(('q', u, z, r, A, B))
    def c(rho, z):
        P.append(('c', rho, z))
    def s(u, z, r=None):
        P.append(('s', u, z, r_par(u, z) if r is None else r, 0.0, 0.0))
    t = TAMPA_T
    ri = GARG_R - GARG_T
    gi = GARG_O - GARG_T
    z0 = PISO_Z
    # gargalo por fora, subindo e abrindo no beico
    q(GARG_O + 0.5, z0, GARG_R + 0.5)
    q(GARG_O, z0 + 0.5, GARG_R)
    q(GARG_O - 0.15, GARG_H - 7.0, GARG_R)
    q(GARG_O - 0.2, GARG_H - 4.0, GARG_R, 0.6 * BEICO_A, 0.35 * BEICO_B)
    q(GARG_O - 0.25, GARG_H - 1.5, GARG_R, 0.9 * BEICO_A, 0.8 * BEICO_B)
    q(GARG_O - 0.25, GARG_H - 0.4, GARG_R, BEICO_A, BEICO_B)
    q(GARG_O - 0.65, GARG_H, GARG_R - 0.4, BEICO_A, BEICO_B)       # labio do bico
    q(gi + 0.3, GARG_H, ri + 0.3, BEICO_A, BEICO_B)
    q(gi - 0.05, GARG_H - 0.4, ri, BEICO_A, BEICO_B)                # aresta viva: corta a gota
    q(gi, GARG_H - 1.8, ri, 0.9 * BEICO_A, 0.8 * BEICO_B)
    q(gi + 0.05, GARG_H - 4.3, ri, 0.6 * BEICO_A, 0.35 * BEICO_B)
    q(gi + 0.15, GARG_H - 7.3, ri)
    q(gi + 0.3, z0 - t, ri)                                         # abertura com saida
    # por baixo: laje do tampo ate a saia
    s(saia_int(z0 - t), z0 - t)
    s(saia_int(-PLUG), -PLUG)
    tmp = []
    _aba_e_plug(tmp, lambda u, z, r=None: tmp.append(('s', u, z, r_par(u, z) if r is None else r, 0.0, 0.0)))
    P += tmp[::-1]
    # por cima, voltando: tampo, parede redonda, labio, vao
    c(R_PAREDE_O + 0.5, z0)
    c(R_PAREDE_O, z0 + 0.5)
    c(R_PAREDE_O - 0.1, z0 + PAREDE_H - 0.5)
    c(R_PAREDE_O - 0.6, z0 + PAREDE_H)
    c(R_PAREDE_I + 0.4, z0 + PAREDE_H)                # chanfro de entrada
    c(R_PAREDE_I - 0.2, z0 + PAREDE_H - 0.6)
    c(R_PAREDE_I - 0.2, z0 + Z_LABIO1 + 1.1)
    c(R_LABIO, z0 + Z_LABIO1)                         # rampa: o rebordo desce abrindo a parede
    c(R_LABIO, z0 + Z_LABIO0)                         # faixa que veda
    c(R_PAREDE_I, z0 + Z_LABIO0 - 0.3)                # face de trava, quase reta
    c(R_PAREDE_I, z0 + 0.4)
    c(R_PAREDE_I - 0.4, z0)
    casca = varre(P, c=(BICO_X, BICO_Y), n=n)
    return com_drenos(casca), P


def drenos():
    """Centro e tamanho dos drenos: lados -X e -Y do gargalo, os que caem
    sobre o interior do pote (os de +X e +Y cairiam na saia)."""
    meio = (GARG_O + COPO_RO - COPO_T) / 2
    return [((BICO_X - meio, BICO_Y), (DRENO_W, DRENO_L)),
            ((BICO_X, BICO_Y - meio), (DRENO_L, DRENO_W))]


def com_drenos(T_):
    import manifold3d as mf
    m = para_manifold(T_)
    zc = PISO_Z - TAMPA_T / 2
    for (cx, cy), (lx, ly) in drenos():
        m = m - mf.Manifold.cube([lx, ly, TAMPA_T + 2.0], True).translate([cx, cy, zc])
    return de_manifold(m)


def para_manifold(T_):
    import manifold3d as mf
    v = np.round(T_.reshape(-1, 3), 6)
    u, idx = np.unique(v, axis=0, return_inverse=True)
    m = mf.Manifold(mf.Mesh(vert_properties=u.astype(np.float32),
                            tri_verts=idx.reshape(-1, 3).astype(np.uint32)))
    assert str(m.status()).endswith('NoError'), f'malha nao e solida: {m.status()}'
    return m


def de_manifold(m):
    mesh = m.to_mesh()
    V = np.array(mesh.vert_properties)[:, :3].astype(float)
    F = np.array(mesh.tri_verts)
    return orienta(V[F])


def copo(n=N_ANEL):
    """Copo medidor de SAN, REDONDO, de boca para baixo (montado).

    Na boca, um REBORDO de 0,4 rente a borda: passa pelo labio da parede de
    PP (que abre) e fica preso embaixo dele - a trava. Rente a boca, sai do
    molde sem gaveta. Saida de 1 grau. Virado, copo medidor de 150 ml.
    """
    P = []
    ro = lambda z: COPO_RO - (z - COPO_ZB) * COPO_SAIDA
    ri = lambda z: ro(z) - COPO_T
    zt = COPO_TETO + COPO_T
    def c(rho, z):
        P.append(('c', rho, z))
    c(0, zt)
    c(ro(zt) - 2.0, zt)
    c(ro(zt - 0.6) - 0.6, zt - 0.6)
    c(ro(zt - 2.0), zt - 2.0)
    c(ro(COPO_ZB + REBORDO_H + 0.3), COPO_ZB + REBORDO_H + 0.3)
    c(COPO_RO + REBORDO, COPO_ZB + REBORDO_H)                  # face de trava do rebordo
    c(COPO_RO + REBORDO, COPO_ZB + 0.3)
    c(COPO_RO + REBORDO - 0.3, COPO_ZB)
    c(ri(COPO_ZB) + 0.4, COPO_ZB)
    c(ri(COPO_ZB + 0.6), COPO_ZB + 0.6)
    c(ri(COPO_TETO - 3.0), COPO_TETO - 3.0)
    c(ri(COPO_TETO) - 3.0, COPO_TETO)                          # fundo arredondado: lava facil
    c(0, COPO_TETO)
    return varre(P, c=(BICO_X, BICO_Y), n=n), P


def copo_ml(ate=None):
    """Volume interno do copo virado, do fundo ate a altura 'ate' (mm)."""
    zs = np.linspace(0, COPO_FUNDO if ate is None else ate, 800)
    a = [math.pi * (COPO_RO - COPO_T - (COPO_FUNDO - h) * COPO_SAIDA) ** 2 for h in zs]
    return float(np.trapezoid(a, zs)) / 1000


def marcas_copo():
    """Altura das marcas de 50/100/150 ml, medida do fundo do copo virado."""
    out = {}
    for ml in (50, 100, 150):
        lo, hi = 0.0, COPO_FUNDO
        for _ in range(40):
            m = (lo + hi) / 2
            lo, hi = (m, hi) if copo_ml(m) < ml else (lo, m)
        out[ml] = round((lo + hi) / 2, 1)
    return out


def fita(n=N_ANEL):
    """A fita RETA de TPE 2 x 10, dobrada em gancho, com a tampa FECHADA.

    Secao (u medido da parede, z da borda): ~5 mm deitados no vao ate a face
    da saia, a dobra contorna a ponta da aleta de cima, e ~4 mm sobem em pe
    encostados na parede. Aperta 0,15 sobre a ponta da aleta.
    """
    w = u_int
    sec = [(-0.4, -0.45), (-0.05, -0.95), (-0.05, -5.6), (-0.5, -6.5),
           (-1.3, Z_FENDA_PISO + 0.05), (-FENDA_FUNDO + 0.05, Z_FENDA_PISO + 0.05),
           (-FENDA_FUNDO + 0.05, Z_FENDA_TETO - 0.05), (-ALETA_PONTA - 0.05, Z_FENDA_TETO - 0.05),
           (-ALETA_PONTA - 0.05, Z_ALETA_TOPO + 0.05), (-2.0, -3.9), (-2.0, -0.45)]
    P = [('s', w(z) + du, z, r_par(w(z) + du, z)) for du, z in sec]
    return varre(P, n=n), P


def fita_teca(n=N_ANEL):
    """A mesma fita, deitada na cava da teca (montagem da rev. 1)."""
    pf = lambda z: u_int(z) - FOLGA - CAVA_P
    z0, z1 = CAVA_Z0 - 0.2, CAVA_Z1 + 0.2
    P = []
    def s(u, z):
        P.append(('s', u, z, r_par(u, z)))
    s(pf(z0), z0)
    s(pf(z0) + FITA_T - 0.25, z0)
    s(pf(z0 - 0.25) + FITA_T, z0 - 0.25)
    s(pf(z1 + 0.25) + FITA_T, z1 + 0.25)
    s(pf(z1) + FITA_T - 0.25, z1)
    s(pf(z1), z1)
    return varre(P, n=n), P


def fita_area():
    """Area da secao em gancho: tem de bater com os 20 mm2 da fita reta."""
    w0 = 0.0
    sec = fita(8)[1]
    pts = [(p[1] - u_int(p[2]), p[2]) for p in sec]
    return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:] + pts[:1]))) / 2


# ---------------------------------------------------------------- contas
def area_q(u, r):
    r = min(r, u - DIF)
    return (2 * u) * (2 * (u - DIF)) - (4 - math.pi) * r * r


def capacidade(H, ate):
    """Volume interno do fundo ate z=ate (mm, absoluto), ml."""
    zi = FUNDO_Z + FUNDO_T
    zs = np.linspace(zi, ate, 2000)
    a = [area_q(U_I - (H - z) * K, R_I) for z in zs]
    return float(np.trapezoid(a, zs)) / 1000


def passo_aninhado():
    """Pote dentro de pote: desce ate o lado de fora do de dentro encostar
    nas nervuras do de fora. Mesma boca + mesma saida = MESMO passo para
    qualquer combinacao de alturas (o 1,2 L dentro do 2,4 L aninha igual)."""
    return (T + NERV_E) / K


def checa_malha(T_):
    """Toda aresta usada duas vezes, uma em cada sentido."""
    v = np.round(T_.reshape(-1, 3), 5)
    _, idx = np.unique(v, axis=0, return_inverse=True)
    idx = idx.reshape(-1, 3)
    ar = {}
    for a, b, c in idx:
        for e in ((a, b), (b, c), (c, a)):
            ar[e] = ar.get(e, 0) + 1
    ruins = sum(1 for (a, b), m in ar.items() if m != 1 or ar.get((b, a), 0) != 1)
    return ruins


def grava_stl(nome, T_):
    with open(os.path.join(AQUI, 'stl', nome), 'wb') as f:
        f.write(nome.ljust(80).encode()[:80])
        f.write(struct.pack('<I', len(T_)))
        for t in T_:
            nrm = np.cross(t[1] - t[0], t[2] - t[0])
            l = np.linalg.norm(nrm)
            nrm = nrm / l if l else nrm
            f.write(struct.pack('<12fH', *nrm, *t[0], *t[1], *t[2], 0))


def pecas(n):
    out = {}
    for i, H in enumerate(ALTURAS):
        out[f'corpo-{i + 1}'] = corpo(H, n)[0]
    out['tampa-fechada'] = tampa_pp(n)[0]
    out['tampa-teca'] = tampa_teca(n)[0]
    out['tampa-bico'] = tampa_bico(n)[0]
    out['copo'] = copo(n)[0]
    out['fita-tpe'] = fita(n)[0]
    out['fita-teca'] = fita_teca(n)[0]
    return out


DENS = {'corpo': 1.08, 'tampa-fechada': 0.90, 'tampa-bico': 0.90, 'copo': 1.08,
        'tampa-teca': 0.65, 'fita-tpe': 1.00, 'fita-teca': 1.00}
MAT = {'corpo': 'SAN', 'tampa-fechada': 'PP', 'tampa-bico': 'PP', 'copo': 'SAN',
       'tampa-teca': 'teca', 'fita-tpe': 'TPE', 'fita-teca': 'TPE'}


def relatorio(P_):
    R = {'saida_graus': SAIDA, 'modulo': MODULO,
         'boca_interna': f'{2 * U_I:.1f} x {2 * (U_I - DIF):.1f}',
         'medida_maxima': f'{2 * U_BORDA:.1f} x {2 * (U_BORDA - DIF):.1f}', 'pecas': {}, 'corpos': []}
    for nome, T_ in P_.items():
        base = 'corpo' if nome.startswith('corpo') else nome
        v = volume(T_) / 1000
        R['pecas'][nome] = dict(material=MAT[base], volume_cm3=round(v, 2),
                                massa_g=round(v * DENS[base], 1), triangulos=len(T_))
    deck = -TAMPA_T                              # face de baixo do bolsao
    for i, H in enumerate(ALTURAS):
        brim = capacidade(H, H)
        util = capacidade(H, H + deck)
        # o anel do plug (face + cava + saia) ocupa a faixa de -PLUG a deck
        anel = sum((8 * u_int(z) - 4 * DIF) * (FENDA_FUNDO + SAIA_PLUG_T)
                   for z in np.linspace(-PLUG, deck, 50)) * (PLUG + deck) / 50 / 1000
        fundo_ext = U_I + T - H * K
        R['corpos'].append(dict(
            altura=H, capacidade_borda_ml=round(brim), capacidade_util_ml=round(util - anel),
            fundo_externo=f'{2 * fundo_ext:.1f} x {2 * (fundo_ext - DIF):.1f}', conicidade_pct=round(100 * (1 - fundo_ext / (U_I + T)), 1),
            massa_g=R['pecas'][f'corpo-{i + 1}']['massa_g']))
    p = passo_aninhado()
    R['passo_aninhado'] = round(p, 1)
    R['aninhamento'] = []
    for H in ALTURAS:
        for nn in (6, 12):
            solto = nn * H
            # pote mais baixo que o passo nao desce: so apoia na borda do outro
            ninho = H + (nn - 1) * min(p, H)
            R['aninhamento'].append(dict(altura=H, n=nn, solto=round(solto), aninhado=round(ninho),
                                         ganho_pct=round(100 * (1 - ninho / solto))))
    # vedacao: a fita sobressai da face do plug e encontra a parede
    aperto = FITA_T - ALETA_PONTA
    R['vedacao'] = dict(fita=f'{FITA_T} x {FITA_L} mm', montagem='gancho: borda de baixo na fenda',
                        fenda=f'{Z_FENDA_TETO - Z_FENDA_PISO:.2f} mm de altura x {FENDA_FUNDO - ALETA_PONTA:.2f} de fundo',
                        aperto_na_ponta=round(aperto, 2), aperto_pct=round(100 * aperto / FITA_T, 1),
                        vao=round(VAO, 2), vao_x_rev3=round(VAO / VAO_REV3, 1),
                        sobra_no_canto_mm=round(math.pi / 2 * VAO, 1),
                        aperto_na_fenda_pct=round(100 * (1 - (Z_FENDA_TETO - Z_FENDA_PISO) / FITA_T)),
                        area_secao_mm2=round(fita_area(), 1),
                        curso_vedando=round(aperto / K, 1))
    return R


def verifica():
    erros = []
    def ok(cond, msg):
        if not cond:
            erros.append(msg)
    # 1. a regra da curva paralela: folga no canto = folga no lado
    for z in (-1, -8, -15):
        u_c, r_c = u_int(z), R_I
        u_p = u_int(z) - FOLGA
        r_p = r_par(u_p, z)
        dc = math.sqrt(2) * (u_c - r_c) + r_c
        dp = math.sqrt(2) * (u_p - r_p) + r_p
        ok(abs((dc - dp) - FOLGA) < 1e-6, f'folga no canto difere da do lado em z={z}')
    # autoteste: com raio FIXO a conferencia acima tem de reprovar
    u_p = u_int(-8) - FOLGA
    dc = math.sqrt(2) * (u_int(-8) - R_I) + R_I
    dp = math.sqrt(2) * (u_p - R_I) + R_I
    ok(abs((dc - dp) - FOLGA) > 0.05, 'autoteste: a checagem do canto nao reprova raio fixo')
    # 2. a fita encosta, e so nos ultimos mm do curso (o ar sai antes)
    aperto = FITA_T - ALETA_PONTA
    ok(0.05 <= aperto <= 0.30, f'aperto da fita fora da faixa: {aperto:.2f}')
    ok(VAO >= 3 * VAO_REV3, 'vao menos que o triplo da rev. 3')
    ok(Z_FENDA_TETO - Z_FENDA_PISO < FITA_T, 'fenda nao aperta a fita')
    ok(ALETA_PONTA2 > ALETA_PONTA - FITA_T + 0.3, 'aleta de baixo encosta na parede')
    ok(abs(fita_area() - FITA_T * FITA_L) / (FITA_T * FITA_L) < 0.15,
       f'secao em gancho nao bate com a fita 2 x 10: {fita_area():.1f} mm2')
    # 3. modular: n potes empilhados com tampa = o maior com tampa
    for a in range(1, 4):
        ok(abs(ALTURAS[a - 1] + ALTURAS[3 - a] - ALTURAS[3]) < 1e-9, 'alturas nao somam')
    # 4. o pe cabe no bolsao, e o pe cabe dentro do fundo do maior
    ok(PE_O + 0.3 <= BOLSAO, 'pe nao entra no bolsao')
    ok(PE_O + 0.5 < U_I + T - ALTURAS[-1] * K - 3, 'pe sai do fundo do pote mais alto')
    # 5. aninhamento: a nervura encosta antes da parede, e fica abaixo da fita
    p = passo_aninhado()
    folga_parede = p * K - T
    ok(abs(folga_parede - NERV_E) < 1e-9, 'passo nao vem da nervura')
    ok(NERV_TOPO > PLUG + 2, 'nervura invade a zona da fita')
    # 6. o beico cabe dentro do copo, com folga, tambem no canto
    ri_beico = COPO_RO - COPO_T - (GARG_H + BEICO_B - COPO_ZB) * COPO_SAIDA
    canto_garg = (GARG_O - GARG_R) * math.sqrt(2) + GARG_R
    ok(max(GARG_O + BEICO_A, canto_garg) + 0.5 <= ri_beico, 'gargalo ou beico encosta no copo')
    ok(COPO_TETO > GARG_H + BEICO_B + 1.0, 'beico encosta no fundo do copo')
    ok(copo_ml() >= 150, f'copo com menos de 150 ml: {copo_ml():.0f}')
    # 7. a trava: o rebordo passa o labio e fica preso; o labio veda
    ok(COPO_RO + REBORDO > R_LABIO + 0.3, 'rebordo nao trava no labio')
    ok(0.1 <= LABIO_APERTO <= 0.3, 'aperto do labio fora da faixa')
    ok(COPO_ZB + REBORDO_H < PISO_Z + Z_LABIO0, 'rebordo nao cabe embaixo do labio')
    ok((R_PAREDE_I - R_LABIO) / R_PAREDE_I < 0.05, 'labio fundo demais para extrair por arraste')
    # 8. o bico no canto: parede dentro da tampa, abertura dentro da saia
    ok(BICO_X + R_PAREDE_O + 1.5 <= U_BORDA, 'parede passa da tampa no comprimento')
    ok(BICO_Y + R_PAREDE_O + 1.5 <= U_BORDA - DIF, 'parede passa da tampa na largura')
    lim = saia_int(PISO_Z - TAMPA_T)
    ok(BICO_X + GARG_O + 2.0 <= lim, 'abertura cai na saia (comprimento)')
    ok(BICO_Y + GARG_O + 2.0 <= lim - DIF, 'abertura cai na saia (largura)')
    # 8b. drenos dentro do copo e sobre o interior do pote
    for (cx, cy), (lx, ly) in drenos():
        d = math.hypot(cx - BICO_X, cy - BICO_Y) + max(lx, ly) / 2 * 0 + min(lx, ly) / 2
        ok(d <= COPO_RO - COPO_T - 0.3, 'dreno fora do copo')
        ok(abs(cx) + lx / 2 + 1 <= lim and abs(cy) + ly / 2 + 1 <= lim - DIF, 'dreno cai na saia')
    # 9. a fita cabe entre a aba e a aleta: 10 mm desenvolvidos
    ok(Z_FENDA_TETO - Z_FENDA_PISO >= 1.5 and Z_ALETA_TOPO - Z_FENDA_TETO >= 1.2, 'aleta ou vao fino demais')
    return erros, p


def main():
    erros, _ = verifica()
    for e in erros:
        print('ERRO:', e)
    if '--teste' in sys.argv:
        sys.exit(1 if erros else 0)
    P_ = pecas(N_ANEL)
    for nome, T_ in P_.items():
        grava_stl(nome + '.stl', T_)
    # malha conferida peca a peca (as nervuras sao cascas a parte)
    principais = {'corpo-4': varre(corpo(ALTURAS[3])[1], n=96),
                  'tampa-fechada': varre(tampa_pp()[1], n=96),
                  'tampa-teca': varre(tampa_teca()[1], n=96),
                  'tampa-bico': tampa_bico(96)[0],
                  'copo': varre(copo()[1], c=(BICO_X, BICO_Y), n=96),
                  'fita-tpe': varre(fita()[1], n=96),
                  'fita-teca': varre(fita_teca()[1], n=96)}
    for nome, T_ in principais.items():
        r = checa_malha(T_)
        if r:
            erros.append(f'malha aberta em {nome}: {r} arestas')
    R = relatorio(P_)
    R['copo'] = dict(material='SAN', capacidade_ml=round(copo_ml()), marcas_mm=marcas_copo(),
                     medida_externa=f'diametro {2 * (COPO_RO + REBORDO):.1f} x {COPO_FUNDO + COPO_T:.1f} de altura')
    R['verificacoes'] = 'OK' if not erros else erros
    with open(os.path.join(AQUI, 'relatorio.json'), 'w') as f:
        json.dump(R, f, indent=1, ensure_ascii=False)
    # malhas do visualizador: indexadas, int16 em centesimo de mm
    V = pecas(N_VIEW)
    out = {}
    for nome, T_ in V.items():
        v = np.round(T_.reshape(-1, 3) * 100).astype(np.int32)
        u, idx = np.unique(v, axis=0, return_inverse=True)
        out[nome] = dict(v=u.astype(np.int16).flatten().tolist(), i=idx.flatten().tolist())
    out['alturas'] = ALTURAS
    out['passo'] = passo_aninhado()
    out['bico_x'] = BICO_X
    with open(os.path.join(AQUI, 'malhas.json'), 'w') as f:
        json.dump(out, f, separators=(',', ':'))
    print(json.dumps(R, indent=1, ensure_ascii=False))
    for e in erros:
        print('ERRO:', e)


if __name__ == '__main__':
    main()
