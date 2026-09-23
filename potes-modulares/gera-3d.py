#!/usr/bin/env python3
"""
Gera os STL da linha - REVISAO 8 (borda alta e oca, trava de clipe, tampa PP).

AS COTAS VEM DE calculo-modular.py
  Nada de constante repetida. Na revisao 7 este arquivo tinha a propria copia
  das cotas e elas ja tinham divergido uma vez. Aqui o modulo e importado.

COMO A CASCA E FEITA
  Cada peca e uma casca fechada de secoes de retangulo com cantos arredondados
  empilhadas em alturas diferentes. Bandas de quadrilateros ligam um anel ao
  seguinte e tampos em leque fecham as pontas. O raio de cada anel sai da regra
  de curva paralela: deslocar a secao de d para dentro tira d do raio.

TRES ARMADILHAS JA PAGAS
  1. anel() sai em sentido HORARIO visto de cima. Se sair anti-horario, o
     volume assinado vem negativo.
  2. Volume assinado NAO detecta normal invertida: uma casca estanque com um
     tampo ao contrario continua fechada e ainda devolve um numero. Por isso
     normais_consistentes() confere que toda aresta aparece uma vez em cada
     sentido, e main() aborta se falhar.
  3. Nem uma coisa nem outra detecta SOLIDO DESCONECTADO. Era o caso da
     revisao 7: a boca (144,95) era mais larga que a face externa do corpo
     (141,55), entao o colar era um anel de material pairando sobre o corpo,
     e as duas superficies horizontais em z_col se cancelavam. Malha estanque,
     normais certas, volume plausivel - e a peca solta. Por isso agora existe
     secao_conexa(), que percorre a altura e confere que o material de uma
     altura encosta no da seguinte.

Uso:  python3 gera-3d.py [--seg 12]      (--seg = pontos por canto)
"""
import importlib.util, json, math, struct, sys, os

_BASE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('cm', os.path.join(_BASE, 'calculo-modular.py'))
cm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cm)

POTES = cm.linha(cm.footprint())
COLAR_L, COLAR_W = POTES[0]['colar_l'], POTES[0]['colar_w']
CORPO_L = POTES[0]['corpo_l']
BOCA    = POTES[0]['boca']
R_EXT, M, T, BASE_T = cm.R_EXT, cm.M, cm.T, cm.BASE_T
BORDA_H, FLARE, SAIA_H, TOPO_T = cm.BORDA_H, cm.FLARE, cm.SAIA_H, cm.TOPO_T
W_SAIA, CANAL, W_IN, W_BORDA = cm.W_SAIA, cm.CANAL, cm.W_IN, cm.W_BORDA
ARRED, CHANF = cm.ARRED, cm.CHANF
WALL = cm.WALL
ELEV = {p['n']: p['elev'] for p in POTES}

PLUG_FOLGA, FRISO_PROF = cm.PLUG_FOLGA, cm.FRISO_PROF
FILETE_D, FILETE_SOB = cm.FILETE_D, cm.FILETE_SOB
PP_DECK, PP_DECK_FORA = cm.PP_DECK, cm.PP_DECK_FORA
PP_PLUG_PAR, PP_PLUG_H = cm.PP_PLUG_PAR, cm.PP_PLUG_H
TRAVA_N, TRAVA_T, TRAVA_FOLGA = cm.TRAVA_N, cm.TRAVA_T, cm.TRAVA_FOLGA
TRAVA_FARPA, TRAVA_RABO, TRAVA_BULGE = cm.TRAVA_FARPA, cm.TRAVA_RABO, cm.TRAVA_BULGE
TRAVA_LARG = cm.TRAVA_FRAC * COLAR_L
TECA_ESP = cm.TECA_ESP

DLW = COLAR_L - COLAR_W


def largura(L):
    """Toda secao guarda a mesma diferenca comprimento-largura."""
    return L - DLW


def raio(L):
    """Curva paralela: deslocar a secao de d para dentro tira d do raio."""
    return R_EXT + (L - COLAR_L) / 2


def anel(L, R, n):
    """Retangulo de cantos arredondados, L de comprimento.

    Sai em sentido HORARIO visto de cima (a lista e revertida no fim) - e o que
    faz o volume assinado sair positivo com as bandas montadas como estao.
    """
    W = largura(L)
    hx, hy = L / 2 - R, W / 2 - R
    pts = []
    for cx, cy, a0 in ((hx, hy, 0), (-hx, hy, 90), (-hx, -hy, 180), (hx, -hy, 270)):
        for k in range(n):
            a = math.radians(a0 + 90 * k / n)
            pts.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    pts.reverse()
    return pts


class Casca:
    def __init__(self, seg):
        self.seg = seg
        self.m = seg * 4
        self.tris = []
        self.loops = []
        self.bands = []
        self.caps = []
        self.prismas = []          # travas: perfil extrudado, fora dos aneis

    def add(self, z, L):
        R = max(raio(L), 0.15)
        self.loops.append(dict(z=z, L=L, W=largura(L), R=R))
        return len(self.loops) - 1

    def _pts(self, i):
        lp = self.loops[i]
        # STL em Z PARA CIMA. (O visualizador remonta em Y para cima, que e a
        # convencao do three.js - a conversao fica la, nao aqui.)
        return [(x, y, lp['z']) for x, y in anel(lp['L'], lp['R'], self.seg)]

    def banda(self, a, b):
        self.bands.append([a, b])
        A, B = self._pts(a), self._pts(b)
        for k in range(self.m):
            k2 = (k + 1) % self.m
            self.tris.append((B[k], B[k2], A[k]))
            self.tris.append((B[k2], A[k2], A[k]))

    def cap(self, i, para_cima=True):
        """Tampo em leque. O leque inverte para a normal apontar para +z."""
        self.caps.append([i, 1 if para_cima else 0])
        P = self._pts(i)
        c = (sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P), P[0][2])
        for k in range(len(P)):
            t = (c, P[k], P[(k + 1) % len(P)])
            self.tris.append(t[::-1] if para_cima else t)


def prisma(perfil, eixo, pos, comp):
    """Solido fechado extrudado de um perfil (d, z) ao longo de um lado.

    perfil: lista fechada de (d, z), d medido para FORA a partir da face
    externa da borda. eixo: 'x' (lado curto) ou 'y' (lado comprido). pos: a
    coordenada dessa face, com sinal. comp: largura da trava.
    """
    n = len(perfil)
    s = 1.0 if pos > 0 else -1.0
    def P(d, z, u):
        v = pos + s * d
        return (u, v, z) if eixo == 'y' else (v, u, z)
    A = [P(d, z, -comp / 2) for d, z in perfil]
    B = [P(d, z, +comp / 2) for d, z in perfil]
    tris = []
    for k in range(n):
        k2 = (k + 1) % n
        tris.append((A[k], A[k2], B[k]))
        tris.append((A[k2], B[k2], B[k]))
    ca = (sum(p[0] for p in A) / n, sum(p[1] for p in A) / n, sum(p[2] for p in A) / n)
    cb = (sum(p[0] for p in B) / n, sum(p[1] for p in B) / n, sum(p[2] for p in B) / n)
    for k in range(n):
        k2 = (k + 1) % n
        tris.append((ca, A[k2], A[k]))
        tris.append((cb, B[k], B[k2]))
    v = sum((a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
             + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0 for a, b, c in tris)
    return [t[::-1] for t in tris] if v < 0 else tris


def corpo(n_mod, seg):
    """Um pote. z=0 no plano de apoio (o fundo reto).

    A BORDA, de baixo para cima: a parede sobe reta ate z_body, abre num tronco
    de cone (FLARE) ate a perna de dentro, que sobe e faz a boca; no topo a
    faixa chata liga a perna a SAIA, que desce por fora deixando um canal. A
    face de baixo da saia - W_SAIA mm - e a aresta onde a trava engata.

    Por fora, descendo, a peca so estreita (saia -> perna -> corpo -> fundo) e
    por dentro tambem (boca -> corpo): nenhuma contra-saida.
    """
    w, elev = WALL[n_mod], ELEV[n_mod]
    H = n_mod * M + BASE_T
    z_body = H - BORDA_H - FLARE
    z_bord = H - BORDA_H
    piso = BASE_T + elev
    corpo_z = lambda z: CORPO_L - 2 * (z_body - z) * T
    boca_z  = lambda z: BOCA - 2 * (H - z) * T
    colar_z = lambda z: COLAR_L - 2 * (H - z) * T
    skirt_i = lambda z: colar_z(z) - 2 * W_SAIA
    leg_o   = lambda z: boca_z(z) + 2 * W_IN

    c = Casca(seg)
    A0  = c.add(0.0,          corpo_z(0.0))          # aresta do fundo
    A1  = c.add(z_body,       CORPO_L)               # topo da parede reta
    A2  = c.add(z_bord,       leg_o(z_bord))         # topo do flare
    A3  = c.add(H - TOPO_T,   leg_o(H - TOPO_T))     # teto do canal, lado de dentro
    A4  = c.add(H - TOPO_T,   skirt_i(H - TOPO_T))   # teto do canal, lado de fora
    A5  = c.add(H - SAIA_H,   skirt_i(H - SAIA_H))   # face interna da saia, embaixo
    A6  = c.add(H - SAIA_H,   colar_z(H - SAIA_H))   # ARESTA DE ENGATE
    A7  = c.add(H - ARRED,    colar_z(H - ARRED))    # face externa da saia
    A8  = c.add(H,            COLAR_L - 2 * ARRED)   # aresta de cima, arredondada
    A9  = c.add(H,            BOCA + 2 * CHANF)      # faixa chata do topo
    A10 = c.add(H - CHANF,    BOCA)                  # chanfro de entrada da boca
    A11 = c.add(z_bord,       boca_z(z_bord))        # fim da boca
    A12 = c.add(z_body,       CORPO_L - 2 * w)       # pe do flare, por dentro
    A13 = c.add(piso,         corpo_z(piso) - 2 * w) # piso interno
    for a, b in ((A0,A1),(A1,A2),(A2,A3),(A3,A4),(A4,A5),(A5,A6),(A6,A7),(A7,A8),
                 (A8,A9),(A9,A10),(A10,A11),(A11,A12),(A12,A13)):
        c.banda(a, b)
    c.cap(A13, True)
    if elev >= 0.05:
        A14 = c.add(elev, corpo_z(elev) - 2 * w)     # face de baixo do piso
        A15 = c.add(0.0,  corpo_z(0.0) - 2 * w)      # face interna do rodape
        c.cap(A14, False)
        c.banda(A14, A15)
        c.banda(A15, A0)
    else:
        A15 = c.add(0.0, corpo_z(0.0) - 2 * w)
        c.cap(A15, False)
        c.banda(A15, A0)
    return c, H


def secao_conexa(n_mod, passo=0.25):
    """Confere que o material de cada altura encosta no da altura seguinte.

    Foi isto que faltou na revisao 7. Em cada z o corpo e uma coroa (ou duas,
    na faixa do canal). Se a coroa de um nivel nao tem intersecao radial com a
    do nivel de baixo, a peca esta partida ali.
    """
    w, elev = WALL[n_mod], ELEV[n_mod]
    H = n_mod * M + BASE_T
    z_body, z_bord = H - BORDA_H - FLARE, H - BORDA_H
    piso = BASE_T + elev
    corpo_z = lambda z: CORPO_L - 2 * (z_body - z) * T
    boca_z  = lambda z: BOCA - 2 * (H - z) * T
    colar_z = lambda z: COLAR_L - 2 * (H - z) * T

    def coroas(z):
        """Lista de (r_int, r_ext) em meia-largura, no meio de um lado."""
        if z <= piso:
            return [(0.0, corpo_z(z) / 2)]
        if z <= z_body:
            return [(corpo_z(z) / 2 - w, corpo_z(z) / 2)]
        if z <= z_bord:                                  # flare
            f = (z - z_body) / FLARE
            ext = (CORPO_L + (boca_z(z_bord) + 2 * W_IN - CORPO_L) * f) / 2
            return [(ext - w, ext)]
        out = [(boca_z(z) / 2, boca_z(z) / 2 + W_IN)]    # perna de dentro
        if z >= H - SAIA_H:                              # + saia, com o canal
            if z >= H - TOPO_T:
                return [(boca_z(z) / 2, colar_z(z) / 2)]
            out.append((colar_z(z) / 2 - W_SAIA, colar_z(z) / 2))
        return out

    z = 0.0
    ruim = []
    while z + passo <= H:
        a, b = coroas(z), coroas(z + passo)
        for (i0, i1) in a:
            if not any(min(i1, j1) - max(i0, j0) > 1e-6 for (j0, j1) in b):
                ruim.append(z)
                break
        z += passo
    return ruim


def autoteste_conexao():
    """Uma checagem que nunca disparou nao prova nada.

    Reconstroi aqui a geometria da REVISAO 7 - colar macico de 5 mm cuja boca
    (144,95) era mais larga que a face externa do corpo (141,55) - e exige que
    o mesmo criterio de secao_conexa() a reprove.
    """
    H, colar_l, corpo_l, boca, colar_h, w = 62.0, 148.55, 141.55, 144.95, 5.0, 1.15
    t = math.tan(math.radians(0.5))
    z_col = H - colar_h

    def coroas7(z):
        if z <= 2.0:
            return [(0.0, (corpo_l - 2 * (z_col - z) * t) / 2)]
        if z <= z_col:
            e = (corpo_l - 2 * (z_col - z) * t) / 2
            return [(e - w, e)]
        return [((boca - 2 * (H - z) * t) / 2, (colar_l - 2 * (H - z) * t) / 2)]

    z, achou = 0.0, False
    while z + 0.25 <= H:
        a, b = coroas7(z), coroas7(z + 0.25)
        for (i0, i1) in a:
            if not any(min(i1, j1) - max(i0, j0) > 1e-6 for (j0, j1) in b):
                achou = True
        z += 0.25
    return achou


def cavidade(n_mod, seg):
    """Fecha so a cavidade interna, para conferir a capacidade na malha."""
    w, elev = WALL[n_mod], ELEV[n_mod]
    H = n_mod * M + BASE_T
    z_body, z_bord = H - BORDA_H - FLARE, H - BORDA_H
    piso = BASE_T + elev
    corpo_z = lambda z: CORPO_L - 2 * (z_body - z) * T
    boca_z  = lambda z: BOCA - 2 * (H - z) * T
    c = Casca(seg)
    K0 = c.add(piso,   corpo_z(piso) - 2 * w)
    K1 = c.add(z_body, CORPO_L - 2 * w)
    K2 = c.add(z_bord, boca_z(z_bord))
    K3 = c.add(H,      BOCA)
    c.cap(K0, False)
    for a, b in ((K0,K1),(K1,K2),(K2,K3)):
        c.banda(a, b)
    c.cap(K3, True)
    return volume_assinado(c.tris)


def tampa_teca(seg):
    """Placa macica de teca com friso na face lateral. z=0 no plano da borda.

    O topo da placa fica BASE_T abaixo do topo da borda: e ele o plano modular,
    e o fundo reto do pote de cima pousa direto nele. Com a borda de 12 mm a
    madeira aparece emoldurada, 2 mm abaixo do aro.
    """
    plug = BOCA - 2 * PLUG_FOLGA
    friso = plug - 2 * FRISO_PROF
    z_top = -BASE_T
    z_bot = z_top - TECA_ESP
    zf0, zf1 = z_top - 3.0, z_top - 3.0 - FILETE_D

    c = Casca(seg)
    P0 = c.add(z_top, plug)
    P1 = c.add(zf0,   plug)
    P2 = c.add(zf0,   friso)
    P3 = c.add(zf1,   friso)
    P4 = c.add(zf1,   plug)
    P5 = c.add(z_bot + 0.6, plug)
    P6 = c.add(z_bot, plug - 1.2)
    for a, b in ((P1,P0),(P2,P1),(P3,P2),(P4,P3),(P5,P4),(P6,P5)):
        c.banda(a, b)
    c.cap(P0, True)
    c.cap(P6, False)
    return c


def tampa_pp(seg):
    """Tampa de PP com DUAS travas de clipe. z=0 no plano do topo da borda.

    O layout veio do STL de referencia: duas travas largas, uma por lado
    COMPRIDO, cobrindo 58% do comprimento, com gancho e rabo para o dedo.

    Tres coisas, cada uma com uma funcao so:
      - o PLUG desce na boca, leva o friso e o filete, e veda RADIAL;
      - a BANDEJA (piso 2,0 mm abaixo do topo) recebe o fundo reto do pote de
        cima e e o plano modular;
      - as TRAVAS engatam sob a aresta da saia e dao a forca de fechamento.

    O que a malha nao tem: a saia decorativa continua que a referencia mostra,
    interrompida pelas duas fendas das travas. Aqui o deck passa da borda e as
    travas penduram dele - e o que ja era assim na revisao 7.
    """
    plug = BOCA - 2 * PLUG_FOLGA
    friso = plug - 2 * FRISO_PROF
    bandeja = plug - 2 * PP_PLUG_PAR
    deck_o = COLAR_L + 2 * PP_DECK_FORA
    z_pf = -PP_PLUG_H
    zf0, zf1 = -3.0, -3.0 - FILETE_D

    c = Casca(seg)
    D0  = c.add(-BASE_T,       bandeja)                       # plano modular
    D1  = c.add(PP_DECK,       bandeja)
    D2  = c.add(PP_DECK,       deck_o)                        # topo do deck
    D3  = c.add(0.0,           deck_o)                        # face externa
    D4  = c.add(0.0,           COLAR_L + 2 * TRAVA_FOLGA)
    D5  = c.add(0.0,           plug)                          # pousa na borda
    D6  = c.add(zf0,           plug)
    D7  = c.add(zf0,           friso)
    D8  = c.add(zf1,           friso)
    D9  = c.add(zf1,           plug)
    D10 = c.add(z_pf + 0.5,    plug)
    D11 = c.add(z_pf,          plug - 1.0)
    D12 = c.add(z_pf,          bandeja)
    D13 = c.add(-BASE_T - PP_DECK, bandeja)
    for a, b in ((D1,D0),(D2,D1),(D3,D2),(D4,D3),(D5,D4),(D6,D5),(D7,D6),(D8,D7),
                 (D9,D8),(D10,D9),(D11,D10),(D12,D11),(D13,D12)):
        c.banda(a, b)
    c.cap(D0, True)
    c.cap(D13, False)

    # ---- as duas travas: prismas separados, embutidos 0,5 mm no deck ----
    F, Tt = TRAVA_FOLGA, TRAVA_T
    Zc = -SAIA_H                                   # nivel da aresta de engate
    # A farpa e cotada a partir da face da borda NA ALTURA DA ARESTA, nao no
    # topo: em SAIA_H mm a saida ja estreitou a borda em SAIA_H*tan(0,5°), e
    # cotar do topo entregaria 0,67 mm de engate em vez dos 0,80 pedidos.
    # Nenhuma checagem de malha acusa isso - so a conferencia de montagem.
    FA = TRAVA_FARPA + SAIA_H * T
    perfil = [(F,                    PP_DECK - 0.5),
              (F,                    Zc),
              (-FA,                  Zc),          # prateleira do gancho
              (-FA,                  Zc - 0.50),
              (F + 0.20,             Zc - 1.70),   # rampa de entrada
              (F + TRAVA_BULGE,      Zc - TRAVA_RABO),
              (F + TRAVA_BULGE + Tt, Zc - TRAVA_RABO + 0.9),
              (F + Tt,               Zc - 0.80),
              (F + Tt,               PP_DECK - 0.5)]
    for pos in (COLAR_W / 2, -COLAR_W / 2):
        c.tris += prisma(perfil, 'y', pos, TRAVA_LARG)
        c.prismas.append(dict(perfil=perfil, eixo='y', pos=pos,
                              comp=TRAVA_LARG, off=0.0))
    return c


def filete(seg):
    """Filete de TPE alojado no friso. Desenhado na medida LIVRE: a face
    externa passa 0,20 mm por lado alem da boca. Esses 0,20 mm sao a
    interferencia - montado, o filete comprime essa diferenca contra a parede.
    No 3D as malhas se sobrepoem nesses 0,20 mm, e e proposital."""
    plug = BOCA - 2 * PLUG_FOLGA
    dentro = plug - 2 * FRISO_PROF
    # o filete assenta no FUNDO do friso, entao a face externa dele e
    # (fundo do friso) + 2*FILETE_D = plug + 2*(FILETE_D - FRISO_PROF).
    # Escrever plug + 2*(FILETE_SOB - FRISO_PROF) deixa o filete 0,40 mm
    # AQUEM da boca: nao veda nada, e nenhuma checagem de malha acusa.
    fora = plug - 2 * FRISO_PROF + 2 * FILETE_D
    zf0, zf1 = -3.0, -3.0 - FILETE_D
    c = Casca(seg)
    A0 = c.add(zf1, dentro)
    A1 = c.add(zf1, fora)
    A2 = c.add(zf0, fora)
    A3 = c.add(zf0, dentro)
    for a, b in ((A0,A1),(A1,A2),(A2,A3),(A3,A0)):
        c.banda(a, b)
    return c


def normais_consistentes(tris):
    """Toda aresta tem de aparecer uma vez em cada sentido."""
    from collections import Counter
    e = Counter()
    for a, b, c in tris:
        for p, q in ((a, b), (b, c), (c, a)):
            e[(p, q)] += 1
    for (p, q), k in e.items():
        if k != 1 or e.get((q, p), 0) != 1:
            return False
    return True


def volume_assinado(tris):
    v = 0.0
    for a, b, c in tris:
        v += (a[0] * (b[1] * c[2] - b[2] * c[1])
              - a[1] * (b[0] * c[2] - b[2] * c[0])
              + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0
    return v


def grava_stl(caminho, tris, nome):
    with open(caminho, 'wb') as f:
        f.write(nome.encode()[:80].ljust(80, b' '))
        f.write(struct.pack('<I', len(tris)))
        for a, b, cc in tris:
            ux, uy, uz = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
            vx, vy, vz = (cc[0] - a[0], cc[1] - a[1], cc[2] - a[2])
            nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
            m = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
            f.write(struct.pack('<3f', nx / m, ny / m, nz / m))
            for p in (a, b, cc):
                f.write(struct.pack('<3f', *p))
            f.write(struct.pack('<H', 0))


def main():
    seg = 12
    if '--seg' in sys.argv:
        seg = int(sys.argv[sys.argv.index('--seg') + 1])
    out = os.path.join(_BASE, 'stl')
    os.makedirs(out, exist_ok=True)

    print(f'cotas de calculo-modular.py: borda {COLAR_L:.1f} x {COLAR_W:.1f} | '
          f'corpo {CORPO_L:.1f} | boca {BOCA:.1f} | borda {BORDA_H:.0f} + flare {FLARE:.0f} mm')

    perfis = {'seg': seg, 'pecas': {}}
    checar = []
    partido = []
    for n in (1, 2, 3, 4):
        c, H = corpo(n, seg)
        nome = f'pote-{n * 600}'
        grava_stl(os.path.join(out, nome + '.stl'), c.tris, nome)
        perfis['pecas'][nome] = dict(loops=c.loops, bands=c.bands, caps=c.caps,
                                     prismas=c.prismas,
                                     H=H, passo=n * M, cap=n * 600)
        checar.append((nome, c))
        ruim = secao_conexa(n)
        if ruim:
            partido.append((nome, ruim[0], ruim[-1]))
        vcav = cavidade(n, seg) / 1000.0
        vmat = volume_assinado(c.tris) / 1000.0
        print(f'{nome:<12} altura {H:6.1f} mm | {len(c.tris):5d} tri | '
              f'cavidade {vcav:7.1f} ml (alvo {n * 600}) | '
              f'peso da malha {vmat * 0.905:6.1f} g')

    t = tampa_teca(seg)
    grava_stl(os.path.join(out, 'tampa-teca.stl'), t.tris, 'tampa-teca')
    perfis['pecas']['tampa-teca'] = dict(loops=t.loops, bands=t.bands, caps=t.caps,
                                         prismas=t.prismas)
    checar.append(('tampa-teca', t))
    print(f'{"tampa-teca":<12} {"":13} | {len(t.tris):5d} tri | placa macica, '
          f'{volume_assinado(t.tris) / 1000.0 * cm.RHO_TECA * 1000:5.0f} g em teca')

    tp = tampa_pp(seg)
    grava_stl(os.path.join(out, 'tampa-pp.stl'), tp.tris, 'tampa-pp')
    perfis['pecas']['tampa-pp'] = dict(loops=tp.loops, bands=tp.bands, caps=tp.caps,
                                       prismas=tp.prismas)
    checar.append(('tampa-pp', tp))
    print(f'{"tampa-pp":<12} {"":13} | {len(tp.tris):5d} tri | {TRAVA_N} travas de '
          f'{TRAVA_LARG:.0f} mm | {volume_assinado(tp.tris) / 1000.0 * 0.905:5.1f} g em PP')

    a = filete(seg)
    grava_stl(os.path.join(out, 'filete-tpe.stl'), a.tris, 'filete-tpe')
    perfis['pecas']['filete'] = dict(loops=a.loops, bands=a.bands, caps=a.caps,
                                     prismas=a.prismas)
    checar.append(('filete-tpe', a))
    print(f'{"filete-tpe":<12} {"":13} | {len(a.tris):5d} tri | '
          f'{volume_assinado(a.tris) / 1000.0 * 1.10:5.1f} g em TPE')

    with open(os.path.join(_BASE, 'perfis.json'), 'w') as f:
        json.dump(perfis, f, separators=(',', ':'))

    ruim = [nome for nome, cc in checar
            if not normais_consistentes(cc.tris) or volume_assinado(cc.tris) <= 0]
    print('\nSTL em', out)
    print('Normais consistentes e volume positivo nas %d pecas: %s'
          % (len(checar), 'OK' if not ruim else 'FALHOU EM ' + ', '.join(ruim)))
    if partido:
        for nome, z0, z1 in partido:
            print(f'SOLIDO PARTIDO em {nome}: sem contato entre z={z0:.2f} e {z1:.2f}')
    else:
        print('Secao conexa em toda a altura nos 4 corpos: OK '
              '(era o erro da revisao 7)')
    if autoteste_conexao():
        print('Autoteste: o mesmo criterio REPROVA a geometria da revisao 7. OK')
    else:
        print('Autoteste FALHOU: o criterio nao pega nem o erro conhecido.')
        sys.exit(1)
    if ruim or partido:
        sys.exit(1)
    print(f'\nAs travas sao prismas separados que entram 0,5 mm no deck, para')
    print(f'fundirem no fatiador. Na peca injetada elas sao recortadas por uma')
    print(f'fenda de ~1 mm nos tres lados livres - a malha nao mostra a fenda.')


if __name__ == '__main__':
    main()
