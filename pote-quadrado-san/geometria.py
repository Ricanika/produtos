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
SAIDA = 3.0                       # graus por face: e o que faz aninhar
K = math.tan(math.radians(SAIDA))
MODULO = 57.0                     # altura do menor; os outros sao 2x, 3x, 4x
ALTURAS = [MODULO * n for n in (1, 2, 3, 4)]

U_I = 62.0      # meio-lado INTERNO na boca (124 mm de vao) - igual nos quatro
T = 2.0         # parede SAN
R_I = 8.0       # raio interno do canto (externo = 10), constante na altura
FUNDO_Z = 3.0   # face de baixo do fundo (o pe ocupa 0..3)
FUNDO_T = 2.2   # espessura do fundo

# borda: saia livre pendurada para fora, canal aberto para baixo
CANAL = 1.2     # canal entre parede e saia
SAIA_T = 1.6    # saia na raiz
SAIA_H = 7.0    # da borda ate o pe da saia
U_BORDA = U_I + T + CANAL + SAIA_T + 0.1   # 66.9 - medida maxima /2

# pe comum (o mesmo nos quatro) e o bolsao da tampa que o recebe
PE_I, PE_O, PE_H = 45.0, 47.6, 3.0
BOLSAO = 48.2   # meio-lado do bolsao da tampa (folga 0,6 sobre o pe)

# nervuras anti-travamento no meio de cada lado, por dentro
NERV_E = 0.6    # quanto avanca para dentro
NERV_L = 4.0    # largura
NERV_TOPO = 20.0  # comeca 20 mm abaixo da borda: fica fora da zona da fita

# tampa / vedacao
FOLGA = 0.25    # face do plug ate a parede do corpo, por lado
PLUG = 16.0     # quanto o plug desce na boca
CAVA_Z0, CAVA_Z1 = -3.0, -13.4   # cava de 10,4 mm de altura
CAVA_P = 1.62   # profundidade da cava
FITA_T, FITA_L = 2.0, 10.0       # a fita pedida: 2 x 10 mm
SAIA_PLUG_T = 1.4  # parede de PP atras da cava
TAMPA_T = 2.0   # espessura de casca da tampa
ABA_H = 3.0     # aba da tampa acima da borda = profundidade do bolsao

# tampa de bico + copo
BICO_X = 30.0   # centro do bico, deslocado para o lado +X (lado de verter)
BICO_RE, BICO_RI_TOPO, BICO_H = 19.0, 16.8, 25.0

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


def anel_quadrado(u, r, c, th):
    """Interseca raios saindo de c com o quadrado arredondado (u, r).
    Bissecao na funcao de distancia: robusta para c fora do centro."""
    if u <= 1e-9:
        return np.zeros((len(th), 2))
    r = min(r, u)
    d = np.stack([np.cos(th), np.sin(th)], 1)
    lo = np.zeros(len(th))
    hi = np.full(len(th), 4 * u + 2 * abs(c[0]) + 2 * abs(c[1]))
    cc = np.array(c)
    for _ in range(48):
        m = (lo + hi) / 2
        p = np.abs(cc + d * m[:, None])
        q = p - (u - r)
        sd = (np.linalg.norm(np.maximum(q, 0), axis=1)
              + np.minimum(np.maximum(q[:, 0], q[:, 1]), 0) - r)
        dentro = sd < 0
        lo = np.where(dentro, m, lo)
        hi = np.where(dentro, hi, m)
    return cc + d * ((lo + hi) / 2)[:, None]


def anel(spec, c, th):
    if spec[0] == 's':
        _, u, z, r = spec
        xy = anel_quadrado(u, r, c, th)
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
    """Solido lofteado entre secoes de 4 pontos (x,y,z). Nervura, orelha."""
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
    def sec(z, e):
        x0, x1 = ui(z) - e, ui(z) + 0.6
        h = NERV_L / 2
        return [(x0, -h, z), (x0, h, z), (x1, h, z), (x1, -h, z)]
    nb = caixa([sec(z0 - 0.01, 0.02), sec(z0 + 1.2, NERV_E), sec(z1, NERV_E), sec(z2, 0.02)])
    for q in range(4):
        nerv.append(roda(nb, q * math.pi / 2))
    return np.concatenate([malha] + nerv), P


def _aba_e_plug(P, s, ate_cava=True):
    """Trecho comum das tres tampas, da aba ao pe do plug, por FORA."""
    pf = lambda z: u_int(z) - FOLGA            # face do plug
    s(U_BORDA - 0.5, ABA_H)
    s(U_BORDA, ABA_H - 0.5)
    s(U_BORDA, 0.0)
    s(pf(0) + 0.6, 0.0)
    s(pf(-0.8), -0.8)
    s(pf(CAVA_Z0), CAVA_Z0)
    s(pf(CAVA_Z0) - CAVA_P, CAVA_Z0)
    s(pf(CAVA_Z1) - CAVA_P, CAVA_Z1)
    s(pf(CAVA_Z1), CAVA_Z1)
    s(pf(-PLUG + 0.8), -PLUG + 0.8)
    s(pf(-PLUG) - 0.8, -PLUG)
    return pf


def tampa_pp(n=N_ANEL):
    """Tampa FECHADA, PP. Bolsao em cima recebe o pe do pote de cima."""
    P = []
    def s(u, z, r=None):
        P.append(('s', u, z, r_par(u, z) if r is None else r))
    s(0, 0.0, 0)
    s(BOLSAO, 0.0, 6.6)
    s(BOLSAO + 1.0, ABA_H, 7.6)               # rampa de entrada do pe
    pf = _aba_e_plug(P, s)
    si = lambda z: pf(z) - CAVA_P - SAIA_PLUG_T
    s(si(-PLUG), -PLUG)
    s(si(ABA_H - TAMPA_T), ABA_H - TAMPA_T)
    s(BOLSAO + 1.0 + TAMPA_T, ABA_H - TAMPA_T, 8.0)
    s(BOLSAO + TAMPA_T, -TAMPA_T, 7.0)
    s(0, -TAMPA_T, 0)
    return orelha(varre(P, n=n)), P


def tampa_teca(n=N_ANEL):
    """Tampa de TECA maciça, CNC. A MESMA cava, a MESMA fita.
    Escavada por baixo: deixa 5 mm de madeira no centro e 5 na lateral."""
    P = []
    def s(u, z, r=None):
        P.append(('s', u, z, r_par(u, z) if r is None else r))
    s(0, 0.0, 0)
    s(BOLSAO, 0.0, 6.6)
    s(BOLSAO + 1.0, ABA_H, 7.6)
    pf = _aba_e_plug(P, s)
    s(pf(-PLUG) - 5.0, -PLUG)
    s(pf(-5.0) - 5.0, -5.0)
    s(0, -5.0, 0)
    return varre(P, n=n), P


def tampa_bico(n=N_ANEL):
    """Tampa de BICO, PP. Mesmo corpo de tampa, deck plano, bico redondo
    deslocado para um lado. Peca de genero 1 (tem furo): o perfil e um laco
    fechado que passa pelo bico e pela tampa, todos os aneis amostrados por
    raios saindo do CENTRO DO BICO."""
    P = []
    c = lambda rho, z: P.append(('c', rho, z))
    def s(u, z, r=None):
        P.append(('s', u, z, r_par(u, z) if r is None else r))
    zt = ABA_H
    zb = zt + BICO_H
    # bico por fora, com o cordao de encaixe do copo
    c(BICO_RE + 1.2, zt)
    c(BICO_RE, zt + 1.2)
    c(BICO_RE - 0.35, zt + 19.0)
    c(BICO_RE + 0.3, zt + 20.6)
    c(BICO_RE + 0.3, zt + 21.6)
    c(BICO_RE - 0.5, zt + 23.4)
    c(BICO_RE - 0.5, zb - 0.4)
    c(BICO_RE - 0.9, zb)
    c(BICO_RI_TOPO + 0.4, zb)
    c(BICO_RI_TOPO, zb - 0.4)
    c(BICO_RI_TOPO + 0.2, zt - TAMPA_T)      # furo com saida
    # laje por baixo, depois a saia do plug, depois a aba, volta ao deck
    pf = lambda z: u_int(z) - FOLGA
    si = lambda z: pf(z) - CAVA_P - SAIA_PLUG_T
    s(si(zt - TAMPA_T), zt - TAMPA_T)
    s(si(-PLUG), -PLUG)
    tmp = []
    _aba_e_plug(tmp, lambda u, z, r=None: tmp.append(('s', u, z, r_par(u, z) if r is None else r)))
    P += tmp[::-1]
    return orelha(varre(P, c=(BICO_X, 0.0), n=n)), P


def copo(n=N_ANEL):
    """Copo dosador que fecha o bico, encaixado (posicao montada).
    Fecha em DUAS frentes: cordao de encaixe por fora (segura) e um anel-plug
    que entra 4 mm no furo do bico com 0,2 mm de aperto (veda)."""
    zt = ABA_H
    zb = zt + BICO_H
    P = []
    c = lambda rho, z: P.append(('c', rho, z))
    topo = zb + 2.2
    c(0, topo)
    c(20.4, topo)
    c(21.0, topo - 0.6)
    c(21.4, zt + 0.6)
    c(19.6, zt + 0.6)
    c(19.6, zt + 18.4)
    c(18.95, zt + 19.2)
    c(18.95, zt + 19.8)
    c(19.65, zt + 20.4)
    c(19.65, zb + 0.2)
    c(BICO_RI_TOPO + 0.2, zb + 0.2)            # anel-plug: 0,2 de aperto
    c(BICO_RI_TOPO + 0.2, zb - 3.6)
    c(BICO_RI_TOPO - 0.2, zb - 4.0)
    c(BICO_RI_TOPO - 1.2, zb - 4.0)
    c(BICO_RI_TOPO - 1.2, zb + 0.2)
    c(0, zb + 0.2)
    return varre(P, c=(BICO_X, 0.0), n=n), P


def fita(n=N_ANEL):
    """A fita de TPE 2 x 10, montada na cava (esticada)."""
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


def orelha(T_):
    """Orelha de abrir num canto: e por ela que se descasca a tampa."""
    d = math.sqrt(2) * (U_BORDA - r_par(U_BORDA, 0)) + r_par(U_BORDA, 0)
    a, b, w = d - 3.0, d + 11.0, 11.0
    def sec(z):
        return [(a, -w, z), (b, -w * 0.55, z), (b, w * 0.55, z), (a, w, z)]
    tab = caixa([sec(ABA_H - 1.6), sec(ABA_H)])
    return np.concatenate([T_, roda(tab, -math.pi / 4)])


# ---------------------------------------------------------------- contas
def area_q(u, r):
    r = min(r, u)
    return (2 * u) ** 2 - (4 - math.pi) * r * r


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
    return out


DENS = {'corpo': 1.08, 'tampa-fechada': 0.90, 'tampa-bico': 0.90, 'copo': 0.90,
        'tampa-teca': 0.65, 'fita-tpe': 1.00}
MAT = {'corpo': 'SAN', 'tampa-fechada': 'PP', 'tampa-bico': 'PP', 'copo': 'PP',
       'tampa-teca': 'teca', 'fita-tpe': 'TPE'}


def relatorio(P_):
    R = {'saida_graus': SAIDA, 'modulo': MODULO, 'boca_interna': 2 * U_I,
         'medida_maxima': round(2 * U_BORDA, 1), 'pecas': {}, 'corpos': []}
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
        anel = sum(4 * 2 * (u_int(z)) * (FOLGA + CAVA_P + SAIA_PLUG_T)
                   for z in np.linspace(-PLUG, deck, 50)) * (PLUG + deck) / 50 / 1000
        fundo_ext = U_I + T - H * K
        R['corpos'].append(dict(
            altura=H, capacidade_borda_ml=round(brim), capacidade_util_ml=round(util - anel),
            fundo_externo=round(2 * fundo_ext, 1), conicidade_pct=round(100 * (1 - fundo_ext / (U_I + T)), 1),
            massa_g=R['pecas'][f'corpo-{i + 1}']['massa_g']))
    p = passo_aninhado()
    R['passo_aninhado'] = round(p, 1)
    R['aninhamento'] = []
    for H in ALTURAS:
        for nn in (6, 12):
            solto = nn * H
            ninho = H + (nn - 1) * p
            R['aninhamento'].append(dict(altura=H, n=nn, solto=round(solto), aninhado=round(ninho),
                                         ganho_pct=round(100 * (1 - ninho / solto))))
    # vedacao: a fita sobressai da face do plug e encontra a parede
    sobra = FITA_T - CAVA_P
    R['vedacao'] = dict(fita=f'{FITA_T} x {FITA_L} mm', cava=f'{CAVA_Z0 - CAVA_Z1:.1f} x {CAVA_P} mm',
                        folga_plug=FOLGA, sobressai=round(sobra, 2),
                        compressao=round(sobra - FOLGA, 2),
                        compressao_pct=round(100 * (sobra - FOLGA) / FITA_T, 1),
                        curso_vedando=round((sobra - FOLGA) / K, 1))
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
    sobra = FITA_T - CAVA_P
    ok(0.05 <= sobra - FOLGA <= 0.25, f'compressao da fita fora da faixa: {sobra - FOLGA:.2f}')
    ok(CAVA_Z0 - CAVA_Z1 >= FITA_L + 0.2, 'cava mais estreita que a fita')
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
    # 6. o bico cabe no deck
    ok(BICO_X + BICO_RE + 1.2 < u_int(ABA_H - TAMPA_T) - FOLGA - CAVA_P - SAIA_PLUG_T - 2,
       'bico encosta na saia do plug')
    # 7. o copo passa por cima do cordao do bico (encaixe de 0,35 mm)
    ok(18.95 < BICO_RE + 0.3 < 19.65, 'cordao do copo nao engata')
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
    # malha conferida peca a peca (as nervuras e a orelha sao cascas a parte)
    principais = {'corpo-4': varre(corpo(ALTURAS[3])[1], n=96),
                  'tampa-fechada': varre(tampa_pp()[1], n=96),
                  'tampa-teca': varre(tampa_teca()[1], n=96),
                  'tampa-bico': varre(tampa_bico()[1], c=(BICO_X, 0), n=96),
                  'copo': varre(copo()[1], c=(BICO_X, 0), n=96),
                  'fita-tpe': varre(fita()[1], n=96)}
    for nome, T_ in principais.items():
        r = checa_malha(T_)
        if r:
            erros.append(f'malha aberta em {nome}: {r} arestas')
    R = relatorio(P_)
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
