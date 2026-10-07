#!/usr/bin/env python3
"""
Gera os STL da linha - REVISAO 10 (borda de 8 mm com dente, aro em U).

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

NA REVISAO 10 A BORDA VIROU UM L
     Parede reta sobe ate o dente; um WEB horizontal de 1,00 mm atravessa para
     fora; a parede da borda sobe dele ate o topo, que e uma meia-cana. A face
     de BAIXO do web e o DENTE (onde a trava engata) e a de CIMA e o DEGRAU
     (onde a placa de teca pousa). Saiu a borda oca inteira - saia livre, canal
     e flare.

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
BORDA_H, BORDA_PAR, WEB_T, DENTE = cm.BORDA_H, cm.BORDA_PAR, cm.WEB_T, cm.DENTE
ARRED = cm.ARRED
WALL = cm.WALL
ELEV = {p['n']: p['elev'] for p in POTES}

SAIA_T, SAIA_FOLGA, RECUO = cm.SAIA_T, cm.SAIA_FOLGA, cm.RECUO
LING_T, LING_H = cm.LING_T, cm.LING_H
ARO_PAR, ARO_FUNDO, ARO_H = cm.ARO_PAR, cm.ARO_FUNDO, cm.ARO_H
DENTE_ARO, DENTE_ARO_H, DENTE_ARO_R = cm.DENTE_ARO, cm.DENTE_ARO_H, cm.DENTE_ARO_R
ARO_BOLSA_H = cm.ARO_BOLSA_H
NERV_T, NERV_H, NERV_MARG = cm.NERV_T, cm.NERV_H, cm.NERV_MARG
PP_DECK, PP_FLANGE = cm.PP_DECK, cm.PP_FLANGE
TRAVA_N, TRAVA_T, TRAVA_FOLGA = cm.TRAVA_N, cm.TRAVA_T, cm.TRAVA_FOLGA
TRAVA_FARPA, TRAVA_RABO, TRAVA_BULGE = cm.TRAVA_FARPA, cm.TRAVA_RABO, cm.TRAVA_BULGE
TRAVA_LARG = cm.TRAVA_FRAC * COLAR_L
TECA_ESP, TECA_FRISO, TECA_CORDA = cm.TECA_ESP, cm.TECA_FRISO, cm.TECA_CORDA
Z_DENTE, Z_DEGRAU, Z_MOD, Z_DECK_B = cm.Z_DENTE, cm.Z_DEGRAU, cm.Z_MOD, cm.Z_DECK_B

SAIA_O = BOCA - 2 * SAIA_FOLGA          # face externa da saia da tampa
LING_O = SAIA_O - 2 * RECUO             # face externa da lingueta
LING_I = LING_O - 2 * LING_T            # face interna da lingueta
DECK_UTIL = SAIA_O - 2 * SAIA_T         # o que sobra de deck para o pote de cima
TAMPA_O = COLAR_L + 2 * TRAVA_FOLGA     # face externa da aba da tampa

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


def contorno(L, W, R, seg, q, cx=0.0, cy=0.0, corte=None):
    """Retangulo arredondado com pontos TAMBEM nos trechos retos.

    anel() so poe vertice nos cantos: o lado reto e uma aresta unica, e nao ha
    onde encaixar um entalhe. Aqui cada canto leva seg pontos e cada face reta
    leva q; a face +X leva 3q, partida em y = -corte e +corte, para que as duas
    bordas do entalhe do bico caiam EXATAMENTE em cima de vertices.

    Devolve (pontos, mascara) - a mascara marca os pontos dentro do entalhe.
    Ordem igual a de anel(): horario visto de cima.

    Cuidado que ja custou uma rodada: nenhum ponto pode sair repetido. Os arcos
    entram com a ponta inicial e SEM a final, e os trechos retos so com as
    pontas que os arcos nao deram - senao aparece aresta de comprimento zero e
    a checagem de normais reprova sem dizer por que.
    """
    hx, hy = L / 2 - R, W / 2 - R
    if corte is None or corte >= hy:
        corte = hy / 3.0
    P, M = [], []

    def arco(ax, ay, a0):
        for k in range(seg):
            a = math.radians(a0 + 90 * k / seg)
            P.append((ax + R * math.cos(a), ay + R * math.sin(a))); M.append(False)

    def reta(p0, p1, n, inc0=False, inc1=False, dentro=False):
        for k in range(n):
            t = (k / n) if inc0 else ((k + 1) / n if inc1 else (k + 1) / (n + 1))
            P.append((p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t))
            M.append(dentro)

    arco(hx, hy, 0)
    reta((hx, hy + R), (-hx, hy + R), q)
    arco(-hx, hy, 90)
    reta((-hx - R, hy), (-hx - R, -hy), q)
    arco(-hx, -hy, 180)
    reta((-hx, -hy - R), (hx, -hy - R), q)
    arco(hx, -hy, 270)
    reta((hx + R, -hy), (hx + R, -corte), q, inc1=True)   # termina EM -corte
    M[-1] = True
    reta((hx + R, -corte), (hx + R, corte), q, dentro=True)
    reta((hx + R, corte), (hx + R, hy), q, inc0=True)     # comeca EM +corte
    M[len(P) - q] = True

    P = [(x + cx, y + cy) for x, y in P]
    P.reverse(); M.reverse()
    return P, M


class Casca:
    def __init__(self, seg):
        self.seg = seg
        self.m = seg * 4
        self.tris = []
        self.loops = []
        self.bands = []
        self.caps = []
        self.prismas = []          # travas: perfil extrudado, fora dos aneis

    def add(self, z, L, W=None, R=None, pts=None):
        """Um anel. pts, quando dado, e a lista (x,y,z) ja pronta - e o que
        permite furo, entalhe e rampa, que a regra (z, L) nao expressa."""
        if pts is not None:
            self.loops.append(dict(pts=[list(p) for p in pts]))
            self.m = len(pts)
        else:
            R = max(raio(L) if R is None else R, 0.15)
            self.loops.append(dict(z=z, L=L, W=largura(L) if W is None else W, R=R))
        return len(self.loops) - 1

    def _pts(self, i):
        lp = self.loops[i]
        if 'pts' in lp:
            return [tuple(p) for p in lp['pts']]
        # STL em Z PARA CIMA. (O visualizador remonta em Y para cima, que e a
        # convencao do three.js - a conversao fica la, nao aqui.)
        return [(x, y, lp['z']) for x, y in anel(lp['L'], lp['R'], self.seg)]

    def banda(self, a, b):
        """Liga dois aneis. Quadrilatero de largura zero e PULADO.

        Onde o entalhe come uma faixa inteira, dois aneis coincidem naquele
        trecho. Emitir o quadrilatero ali cria triangulo de area zero e aresta
        repetida, e a checagem de normais reprova. Pulado, a malha continua
        fechada: a aresta passa a ser compartilhada pelas bandas de cima e de
        baixo, uma em cada sentido.
        """
        self.bands.append([a, b])
        A, B = self._pts(a), self._pts(b)
        m = len(A)
        for k in range(m):
            k2 = (k + 1) % m
            i0, i1 = A[k] == B[k], A[k2] == B[k2]
            if i0 and i1:
                continue
            if not i0:
                self.tris.append((B[k], B[k2], A[k]))
            if not i1:
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

    A BORDA, de baixo para cima: a parede reta sobe ate z_dente; ali o WEB
    horizontal atravessa para FORA (a face de baixo dele e o DENTE, onde a
    trava engata) e a parede da borda sobe do web ate o topo, que e uma
    meia-cana de raio BORDA_PAR/2. Por dentro, descendo: boca -> DEGRAU (a face
    de cima do web, onde a placa de teca pousa) -> corpo.

    Por fora, descendo, a peca so estreita (borda -> corpo -> fundo) e por
    dentro tambem (boca -> degrau -> corpo): nenhuma contra-saida. O dente esta
    no TOPO, que e onde a cavidade ja e mais larga - a peca sai reta.
    """
    w, elev = WALL[n_mod], ELEV[n_mod]
    H = n_mod * M + BASE_T
    z_dente  = H - BORDA_H                       # face de baixo do web
    z_degrau = z_dente + WEB_T                   # face de cima do web
    piso = BASE_T + elev
    corpo_z = lambda z: CORPO_L - 2 * (z_dente - z) * T
    boca_z  = lambda z: BOCA - 2 * (H - z) * T
    colar_z = lambda z: COLAR_L - 2 * (H - z) * T

    c = Casca(seg)
    A = [c.add(0.0,      corpo_z(0.0)),                   # aresta do fundo
         c.add(z_dente,  corpo_z(z_dente)),               # topo da parede reta
         c.add(z_dente,  colar_z(z_dente))]               # O DENTE
    A.append(c.add(H - ARRED, colar_z(H - ARRED)))        # face externa da borda
    # meia-cana do topo: do raio externo ao raio da boca, sem faixa chata.
    rc = COLAR_L / 2 - ARRED
    for k in (1, 2, 3):
        ang = math.radians(180.0 * k / 4)
        A.append(c.add(H - ARRED + ARRED * math.sin(ang),
                       2 * (rc + ARRED * math.cos(ang))))
    A += [c.add(H - ARRED,  boca_z(H - ARRED)),           # boca, sob a meia-cana
          c.add(z_degrau,   boca_z(z_degrau)),            # fim da boca
          c.add(z_degrau,   corpo_z(z_degrau) - 2 * w),   # O DEGRAU INTERNO
          c.add(piso,       corpo_z(piso) - 2 * w)]       # piso interno
    for a, b in zip(A, A[1:]):
        c.banda(a, b)
    c.cap(A[-1], True)
    if elev >= 0.05:
        B0 = c.add(elev, corpo_z(elev) - 2 * w)           # face de baixo do piso
        B1 = c.add(0.0,  corpo_z(0.0) - 2 * w)            # face interna do rodape
        c.cap(B0, False)
        c.banda(B0, B1)
        c.banda(B1, A[0])
    else:
        B1 = c.add(0.0, corpo_z(0.0) - 2 * w)
        c.cap(B1, False)
        c.banda(B1, A[0])
    return c, H


def secao_conexa(n_mod, passo=0.25):
    """Confere que o material de cada altura encosta no da altura seguinte.

    Foi isto que faltou na revisao 7. Em cada z o corpo e uma coroa (ou duas,
    na faixa do canal). Se a coroa de um nivel nao tem intersecao radial com a
    do nivel de baixo, a peca esta partida ali.
    """
    w, elev = WALL[n_mod], ELEV[n_mod]
    H = n_mod * M + BASE_T
    z_dente, z_degrau = H - BORDA_H, H - BORDA_H + WEB_T
    piso = BASE_T + elev
    corpo_z = lambda z: CORPO_L - 2 * (z_dente - z) * T
    boca_z  = lambda z: BOCA - 2 * (H - z) * T
    colar_z = lambda z: COLAR_L - 2 * (H - z) * T

    def coroas(z):
        """Lista de (r_int, r_ext) em meia-largura, no meio de um lado."""
        if z <= piso:
            return [(0.0, corpo_z(z) / 2)]
        if z <= z_dente:
            return [(corpo_z(z) / 2 - w, corpo_z(z) / 2)]
        if z <= z_degrau:                                # o web: macico
            return [(corpo_z(z) / 2 - w, colar_z(z) / 2)]
        return [(boca_z(z) / 2, colar_z(z) / 2)]         # parede da borda

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
    z_dente, z_degrau = H - BORDA_H, H - BORDA_H + WEB_T
    piso = BASE_T + elev
    corpo_z = lambda z: CORPO_L - 2 * (z_dente - z) * T
    boca_z  = lambda z: BOCA - 2 * (H - z) * T
    c = Casca(seg)
    K0 = c.add(piso,     corpo_z(piso) - 2 * w)
    K1 = c.add(z_degrau, corpo_z(z_degrau) - 2 * w)
    K2 = c.add(z_degrau, boca_z(z_degrau))
    K3 = c.add(H,        BOCA)
    c.cap(K0, False)
    for a, b in ((K0,K1),(K1,K2),(K2,K3)):
        c.banda(a, b)
    c.cap(K3, True)
    return volume_assinado(c.tris)


def tampa_teca(seg):
    """Placa macica de teca que POUSA no degrau interno. z=0 no topo da borda.

    A espessura nao foi escolhida: TECA_ESP = BORDA_H - WEB_T - BASE_T = 5,00.
    A placa desce ate o degrau e o topo dela cai exatamente no plano modular.
    O peso do pote de cima vai para o DEGRAU atraves da madeira, em compressao;
    na revisao 8 a placa tinha 8 mm e vencia o vao sozinha, em flexao.

    Vedacao: friso usinado + corda redonda. A placa NAO leva o aro em U - uma
    lingueta de 0,80 mm em madeira quebra.
    """
    teca_l = SAIA_O
    friso = teca_l - 2 * TECA_FRISO
    z_top, z_bot = Z_MOD, Z_DEGRAU
    zf0 = z_top - 1.8
    zf1 = zf0 - TECA_CORDA

    c = Casca(seg)
    P0 = c.add(z_top, teca_l)
    P1 = c.add(zf0,   teca_l)
    P2 = c.add(zf0,   friso)
    P3 = c.add(zf1,   friso)
    P4 = c.add(zf1,   teca_l)
    P5 = c.add(z_bot + 0.6, teca_l)
    P6 = c.add(z_bot, teca_l - 1.2)
    for a, b in ((P1,P0),(P2,P1),(P3,P2),(P4,P3),(P5,P4),(P6,P5)):
        c.banda(a, b)
    c.cap(P0, True)
    c.cap(P6, False)
    return c


def corda_teca(seg):
    """A corda de silicone da placa de teca, desenhada na medida LIVRE.

    A face externa dela passa (TECA_SOB - SAIA_FOLGA) por lado alem da boca:
    essa diferenca e a interferencia. No 3D as malhas se sobrepoem ai, e e
    proposital.
    """
    teca_l = SAIA_O
    dentro = teca_l - 2 * TECA_FRISO
    fora = dentro + 2 * TECA_CORDA
    zf0 = Z_MOD - 1.8
    zf1 = zf0 - TECA_CORDA
    c = Casca(seg)
    A0 = c.add(zf1, dentro)
    A1 = c.add(zf1, fora)
    A2 = c.add(zf0, fora)
    A3 = c.add(zf0, dentro)
    for a, b in ((A0,A1),(A1,A2),(A2,A3),(A3,A0)):
        c.banda(a, b)
    return c


def tampa_pp(seg):
    """Tampa de PP com DUAS travas de clipe. z=0 no plano do topo da borda.

    Uma saia so, que entra na boca (foi a escolha do Ricardo contra a de saia
    dupla). O perfil, de dentro para fora:

      deck .......... topo em Z_MOD = -2,00, o plano modular; e nele que o
                      fundo reto do pote de cima pousa;
      saia .......... sobe do deck ate a aba e desce ate Z_DECK_B;
      lingueta ...... continua a saia, recuada RECUO em cada face. E nela que o
                      aro em U CALCA - nao e colado, ele abraca;
      aba ........... cruza por cima da meia-cana da borda e e o batente
                      vertical da tampa: e ela que poe o deck em -2,00;
      travas ........ penduram da aba e engatam sob o DENTE, 8 mm abaixo.

    O que a malha nao tem: a fenda de ~1 mm que recorta as travas nos tres
    lados livres, e a saia decorativa da referencia.
    """
    c = Casca(seg)
    D0  = c.add(Z_MOD,                DECK_UTIL)   # plano modular, topo do deck
    D1  = c.add(PP_FLANGE,            DECK_UTIL)   # face interna da saia, ate a aba
    D2  = c.add(PP_FLANGE,            TAMPA_O)     # topo da aba
    D3  = c.add(0.0,                  TAMPA_O)     # face externa da aba
    D4  = c.add(0.0,                  SAIA_O)      # a aba pousa na meia-cana
    D5  = c.add(Z_DECK_B,             SAIA_O)      # face externa da saia
    D = [D0, D1, D2, D3, D4, D5] + lingueta(c) + [c.add(Z_DECK_B, DECK_UTIL)]
    for a, b in zip(D, D[1:]):
        c.banda(b, a)
    c.cap(D[0], True)
    c.cap(D[-1], False)

    poe_travas(c)
    poe_nervuras(c)
    return c


def perfil_lingueta():
    """(largura, z) da lingueta com a farpa, de cima para baixo e de volta."""
    z_omb = Z_DECK_B - (LING_H - DENTE_ARO_H - DENTE_ARO_R)   # ombro do degrau
    z_fim = z_omb - DENTE_ARO_H
    z_pta = Z_DECK_B - LING_H
    PTA_O, PTA_I = LING_O + 2 * DENTE_ARO, LING_I - 2 * DENTE_ARO
    return [(LING_O, Z_DECK_B), (LING_O, z_omb), (PTA_O, z_omb), (PTA_O, z_fim),
            (LING_O, z_pta), (LING_I, z_pta), (PTA_I, z_fim), (PTA_I, z_omb),
            (LING_I, z_omb), (LING_I, Z_DECK_B)]


def lingueta(c):
    """A lingueta em que o aro em U calca, com a FARPA que segura ele.

    De cima para baixo: recuo da saia, trecho reto, DEGRAU de 90° para fora
    (e esta face que o aro tem de vencer para cair), trecho cheio da farpa,
    rampa de volta e ponta. O aro entra pela rampa e sai pelo degrau - e por
    isso que ele entra com a mao e nao sai sozinho.
    """
    return [c.add(z, L) for L, z in perfil_lingueta()]


def poe_nervuras(c, pula=None):
    """Grade de MINI LOMBADAS sob o deck. E o que deixa a tampa 'encorpada'.

    Nao sao nervuras de ponta chata: a crista e meia-cana. Ponta chata segura
    vacuo e arrasta aresta viva no aco; meia-cana sai por rolamento. Custa
    rigidez (a area some justamente no alto, onde o braco e maior), e a grade
    ficou mais densa para compensar - 7x4 em vez de 5x3.

    Saida de 3° por face, que e o que a maquina pede: numa lombada de 2,4 mm
    isso custa 0,22 mm de espessura na ponta e nada mais. (Na parede do pote a
    mesma saida custaria o produto - ver calculo-modular.py.)

    pula(x, y) -> True para nao por lombada ali.
    """
    nv = cm.nervuras(DECK_UTIL, DECK_UTIL - DLW)
    pts = nv['perfil']
    perfil = ([(+NERV_T / 2, Z_DECK_B + 0.5)]
              + [(+w, Z_DECK_B - h) for w, h in pts]
              + [(-w, Z_DECK_B - h) for w, h in reversed(pts[:-1])]
              + [(-NERV_T / 2, Z_DECK_B + 0.5)])
    uso_l, uso_w = nv['uso']
    for y in nv['ys']:
        if pula and pula(None, y):
            continue
        c.tris += prisma(perfil, 'y', y, uso_l)
        c.prismas.append(dict(perfil=perfil, eixo='y', pos=y, comp=uso_l, off=0.0))
    for x in nv['xs']:
        if pula and pula(x, None):
            continue
        c.tris += prisma(perfil, 'x', x, uso_w)
        c.prismas.append(dict(perfil=perfil, eixo='x', pos=x, comp=uso_w, off=0.0))
    return c


def poe_travas(c):
    """As duas travas de clipe. As duas tampas de PP usam as mesmas.

    O gancho engata sob o DENTE, em z = -BORDA_H. O braco e so a altura da
    borda: 8 mm contra 10 na revisao 8. Como a forca vai com 1/L^3, a trava
    teve de AFINAR de 1,00 para 0,80 mm - senao fechar pediria 3,7 kgf por
    trava em vez de 1,9.
    """
    F, Tt = TRAVA_FOLGA, TRAVA_T
    Zc = Z_DENTE                                   # nivel do dente
    # A farpa e cotada a partir da face da borda NA ALTURA DO DENTE, nao no
    # topo: em BORDA_H mm a saida ja estreitou a borda em BORDA_H*tan(0,5°), e
    # cotar do topo entregaria menos engate do que o pedido. Nenhuma checagem
    # de malha acusa isso - so a conferencia de montagem.
    FA = TRAVA_FARPA + BORDA_H * T
    perfil = [(F,                    PP_FLANGE - 0.5),
              (F,                    Zc),
              (-FA,                  Zc),          # prateleira do gancho
              (-FA,                  Zc - 0.50),
              (F + 0.20,             Zc - 1.70),   # rampa de entrada
              (F + TRAVA_BULGE,      Zc - TRAVA_RABO),
              (F + TRAVA_BULGE + Tt, Zc - TRAVA_RABO + 0.9),
              (F + Tt,               Zc - 0.80),
              (F + Tt,               PP_FLANGE - 0.5)]
    for pos in (COLAR_W / 2, -COLAR_W / 2):
        c.tris += prisma(perfil, 'y', pos, TRAVA_LARG)
        c.prismas.append(dict(perfil=perfil, eixo='y', pos=pos,
                              comp=TRAVA_LARG, off=0.0))
    return c


# ---------------------------------------------------------------------------
# TAMPA DE BICO (revisao 12) - substitui a tampa de correr da revisao 9, que o
# Ricardo reprovou ("nao ficou legal, preciso de algo mais robusto"). Tudo o
# que toca o pote vem da tampa de PP: saia, lingueta, aro em U e as travas. O
# corpo nao muda. O que entra: GARGALO (veda), CALHA (escorre) e FECHO.
#
# A ideia que a de correr nao tinha: SEPARAR quem veda de quem escorre. La a
# janela por onde o produto saia era tambem o que tinha de vedar, e por isso
# precisava de gaveta, trilho e um segundo aro. Aqui o gargalo e um colar
# fechado de topo plano - a linha de vedacao e plana - e a calha e so um canal
# aberto depois dele.
# ---------------------------------------------------------------------------
_sb = importlib.util.spec_from_file_location('cb', os.path.join(_BASE, 'calculo-bico.py'))
cb = importlib.util.module_from_spec(_sb)
_sb.loader.exec_module(cb)

Q_RETO = 6          # pontos por trecho reto do contorno


def tampa_bico(seg):
    """A tampa de bico. Casca de genero 1: o furo do gargalo e a rosca.

    A sequencia de aneis fecha um LOOP (o ultimo liga de volta no primeiro),
    sem tampo nenhum - e isso que faz o furo ser furo. Comeca na boca do
    gargalo, desce por fora dele ate o deck, cruza o deck, sobe na aba, da a
    volta por fora, desce a saia e a lingueta, volta pela face de baixo do deck
    e sobe pelo furo ate fechar.
    """
    q = Q_RETO
    ZC, ZM, ZB = cb.Z_COL, Z_MOD, Z_DECK_B
    gl, gw, gr = cb.GARG_L, cb.GARG_W, cb.GARG_R
    gp, cx = cb.GARG_PAR, cb.X_GARG
    tg = cb.T_GARG

    c = Casca(seg)

    def anelx(L, W, R, z, cx=0.0):
        pts, _ = contorno(L, W, R, seg, q, cx, 0.0, None)
        return c.add(None, None, pts=[(x, y, z) for x, y in pts])

    # o furo e CONICO: mais largo na boca, para o macho sair e para o plug
    # apertar progressivamente. A cota que manda na vazao e a do pe.
    def furo(z):
        d = ZC - z
        return gl - 2 * d * tg, gw - 2 * d * tg

    f0l, f0w = furo(ZC)
    fbl, fbw = furo(ZB)

    A = [anelx(f0l, f0w, gr, ZC, cx),                      # boca do gargalo
         anelx(gl + 2 * gp, gw + 2 * gp, gr + gp, ZC, cx), # topo do colar, por fora
         anelx(gl + 2 * gp, gw + 2 * gp, gr + gp, ZM, cx), # pe do colar
         anelx(DECK_UTIL, largura(DECK_UTIL), raio(DECK_UTIL), ZM),   # deck
         anelx(DECK_UTIL, largura(DECK_UTIL), raio(DECK_UTIL), PP_FLANGE),
         anelx(TAMPA_O, largura(TAMPA_O), raio(TAMPA_O), PP_FLANGE),  # aba
         anelx(TAMPA_O, largura(TAMPA_O), raio(TAMPA_O), 0.0),
         anelx(SAIA_O, largura(SAIA_O), raio(SAIA_O), 0.0),
         ] + [anelx(L, largura(L), raio(L), z) for L, z in perfil_lingueta()] + [
         anelx(DECK_UTIL, largura(DECK_UTIL), raio(DECK_UTIL), ZB),   # deck por baixo
         anelx(fbl, fbw, gr, ZB, cx)]                      # pe do furo
    for a, b in zip(A, A[1:] + A[:1]):
        c.banda(b, a)

    poe_calha(c)
    poe_travas(c)
    # lombadas so no trecho do deck que sobra entre o colar e o lado -X
    poe_nervuras(c, pula=lambda x, y: (False if x is None
                                       else x > cx - gl / 2 - gp - 4.0))
    return c


def poe_calha(c):
    """A calha aberta em U: piso que cai e duas paredes que a seguram.

    O piso sai do colar no nivel do topo dele e cai ate o labio. As paredes
    nao sao so guia: sao a VIGA que segura o piso em balanco. Por isso o perfil
    delas desce ate o deck no trecho de dentro e ate a aba no trecho de cima da
    borda - sem isso o piso seria uma ponte no ar.
    """
    ZC = cb.Z_COL
    u1 = cb.DECK / 2 - cb.X_SAIDA          # onde acaba o deck
    u2 = cb.TAMPA_O / 2 - cb.X_SAIDA       # onde acaba a aba
    L = cb.X_LABIO - cb.X_SAIDA
    queda_lab = 2.5 * math.tan(math.radians(cb.BICO_CURVA))
    zf = lambda u: ZC - cb.BICO_QUEDA * u / L
    esp = lambda u: cb.CALHA_T + (cb.BICO_LIP - cb.CALHA_T) * u / L

    piso = [(0.0, ZC), (L - 2.5, zf(L - 2.5)),
            (L, zf(L) - queda_lab), (L, zf(L) - queda_lab - cb.BICO_LIP),
            (L - 2.5, zf(L - 2.5) - esp(L - 2.5)), (0.0, ZC - cb.CALHA_T)]
    for t in prisma(piso, 'x', cb.X_SAIDA, cb.GARG_W):
        c.tris.append(t)
    c.prismas.append(dict(perfil=piso, eixo='x', pos=cb.X_SAIDA,
                          comp=cb.GARG_W, off=0.0))

    par = [(0.0, Z_MOD), (0.0, ZC + cb.BICO_ALT),
           (L, zf(L) - queda_lab + cb.BICO_ALT * 0.45),
           (L, zf(L) - queda_lab - cb.BICO_LIP),
           (u2, zf(u2) - esp(u2)), (u2, PP_FLANGE),
           (u1, PP_FLANGE), (u1, Z_MOD)]
    for pos in (cb.GARG_W / 2 + cb.BICO_PAR / 2, -(cb.GARG_W / 2 + cb.BICO_PAR / 2)):
        for t in prisma(par, 'x', cb.X_SAIDA, cb.BICO_PAR):
            c.tris.append(tuple((x, y + pos, z) for x, y, z in t))
        c.prismas.append(dict(perfil=par, eixo='x', pos=cb.X_SAIDA,
                              comp=cb.BICO_PAR, off=pos))
    return c


def fecho_bico(seg):
    """O fecho do bico, desenhado FECHADO. Plug conico de 1° no gargalo de 5°.

    Desenhado na posicao de vedacao: as malhas se sobrepoem onde o plug aperta,
    e e proposital - e a interferencia. Na peca injetada o fecho e o mesmo
    tiro da tampa, ligado por dobradica viva atras; a dobradica nao esta na
    malha, como a fenda das travas nao esta.
    """
    q = Q_RETO
    ZC = cb.Z_COL
    gl, gw, gr = cb.GARG_L, cb.GARG_W, cb.GARG_R
    cx, tp = cb.X_GARG, cb.T_PLUG
    topo = ZC + cb.FECHO_TOPO
    fim = ZC - cb.PLUG_H

    c = Casca(seg)

    def anelx(L, W, R, z):
        pts, _ = contorno(L, W, R, seg, q, cx, 0.0, None)
        return c.add(None, None, pts=[(x, y, z) for x, y in pts])

    # o plug: na boca entra folgado PLUG_BOCA; como o cone dele e MENOS aberto
    # que o do gargalo, ele vai apertando conforme desce.
    pl = lambda d, base: base - 2 * cb.PLUG_BOCA - 2 * d * tp
    tampo_l, tampo_w = gl + 2 * cb.GARG_PAR, gw + 2 * cb.GARG_PAR

    F = [anelx(tampo_l, tampo_w, gr + cb.GARG_PAR, topo),          # tampo, por cima
         anelx(tampo_l, tampo_w, gr + cb.GARG_PAR, ZC),            # face externa
         anelx(pl(0, gl), pl(0, gw), gr, ZC),                      # raiz do plug
         anelx(pl(cb.PLUG_H, gl), pl(cb.PLUG_H, gw), gr, fim),     # ponta do plug
         anelx(pl(cb.PLUG_H, gl) - 2 * cb.PLUG_PAR,
               pl(cb.PLUG_H, gw) - 2 * cb.PLUG_PAR, max(gr - cb.PLUG_PAR, 0.3), fim),
         anelx(pl(0, gl) - 2 * cb.PLUG_PAR, pl(0, gw) - 2 * cb.PLUG_PAR,
               max(gr - cb.PLUG_PAR, 0.3), ZC - cb.FECHO_TOPO * 0 + 0.0)]
    for a, b in zip(F, F[1:]):
        c.banda(b, a)
    c.cap(F[0], True)
    c.cap(F[-1], False)

    # crista de pega: o fecho nao tem abano nem saia (bateriam na calha), entao
    # a pega e um ressalto no proprio tampo.
    cr = [(-cb.CRISTA_W / 2, topo), (cb.CRISTA_W / 2, topo),
          (cb.CRISTA_W / 2 - 0.6, topo + cb.CRISTA_H),
          (-cb.CRISTA_W / 2 + 0.6, topo + cb.CRISTA_H)]
    comp = gw - 6.0
    for t in prisma(cr, 'x', cx, comp):
        c.tris.append(t)
    c.prismas.append(dict(perfil=cr, eixo='x', pos=cx, comp=comp, off=0.0))
    return c


def aro_u(seg):
    """O aro em U de silicone, desenhado CALCADO na lingueta.

    A secao tem oito vertices: desce a face externa da perna de fora, cruza o
    fundo, sobe a face interna da perna de dentro e volta pelo VAO - que e o
    furo onde a lingueta entra. Varrido em volta, isso e um toro (genero 1),
    como o filete da revisao 8, so que com secao em U em vez de retangular.

    Desenhado MONTADO: o vao sai com a largura exata da lingueta. Livre, ele e
    ARO_GRIP mais estreito - e esse aperto que segura o aro sem cola.
    A face externa passa ARO_COMP por lado alem da boca: no 3D as malhas se
    sobrepoem ai, e e proposital - e a interferencia de vedacao.
    """
    L_oo = LING_O + 2 * ARO_PAR                 # face externa da perna de fora
    L_ii = LING_I - 2 * ARO_PAR                 # face interna da perna de dentro
    z_top = Z_DECK_B
    z_bot = z_top - ARO_H
    z_vao = z_bot + ARO_FUNDO                   # teto do fundo do U

    c = Casca(seg)
    # BOLSA na base do vao: e ela que recebe a farpa da lingueta. Sem ela o
    # silicone ficaria esticado 0,50 mm em cima da farpa para sempre, e
    # deformacao permanente e o que mata vedante de borracha.
    z_p = z_vao + ARO_BOLSA_H
    BOL_O = LING_O + 2 * (DENTE_ARO + 0.05)
    BOL_I = LING_I - 2 * (DENTE_ARO + 0.05)
    # A ordem dos vertices e o que da o sinal do volume: percorrida ao
    # contrario, a casca fecha igual e o volume sai NEGATIVO.
    U = [c.add(z_top, LING_O), c.add(z_p, LING_O), c.add(z_p, BOL_O),
         c.add(z_vao, BOL_O), c.add(z_vao, BOL_I), c.add(z_p, BOL_I),
         c.add(z_p, LING_I), c.add(z_top, LING_I),
         c.add(z_top, L_ii), c.add(z_bot, L_ii),
         c.add(z_bot, L_oo), c.add(z_top, L_oo)]
    for a, b in zip(U, U[1:] + U[:1]):
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
          f'corpo {CORPO_L:.1f} | boca {BOCA:.1f} | borda {BORDA_H:.0f} mm com dente '
          f'de {DENTE:.2f}')

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

    tb = tampa_bico(seg)
    grava_stl(os.path.join(out, 'tampa-bico.stl'), tb.tris, 'tampa-bico')
    perfis['pecas']['tampa-bico'] = dict(loops=tb.loops, bands=tb.bands, caps=tb.caps,
                                         prismas=tb.prismas)
    checar.append(('tampa-bico', tb))
    print(f'{"tampa-bico":<12} {"":13} | {len(tb.tris):5d} tri | gargalo + calha em U | '
          f'{volume_assinado(tb.tris) / 1000.0 * 0.905:5.1f} g em PP')

    fb = fecho_bico(seg)
    grava_stl(os.path.join(out, 'fecho-bico.stl'), fb.tris, 'fecho-bico')
    perfis['pecas']['fecho-bico'] = dict(loops=fb.loops, bands=fb.bands, caps=fb.caps,
                                         prismas=fb.prismas)
    checar.append(('fecho-bico', fb))
    print(f'{"fecho-bico":<12} {"":13} | {len(fb.tris):5d} tri | plug conico | '
          f'{volume_assinado(fb.tris) / 1000.0 * 0.905:5.1f} g em PP')

    au = aro_u(seg)
    grava_stl(os.path.join(out, 'aro-u.stl'), au.tris, 'aro-u')
    perfis['pecas']['aro-u'] = dict(loops=au.loops, bands=au.bands, caps=au.caps,
                                    prismas=au.prismas)
    checar.append(('aro-u', au))
    print(f'{"aro-u":<12} {"":13} | {len(au.tris):5d} tri | calca na lingueta | '
          f'{volume_assinado(au.tris) / 1000.0 * cm.RHO_SIL * 1000:5.1f} g em silicone')

    ct = corda_teca(seg)
    grava_stl(os.path.join(out, 'corda-teca.stl'), ct.tris, 'corda-teca')
    perfis['pecas']['corda-teca'] = dict(loops=ct.loops, bands=ct.bands, caps=ct.caps,
                                         prismas=ct.prismas)
    checar.append(('corda-teca', ct))
    print(f'{"corda-teca":<12} {"":13} | {len(ct.tris):5d} tri | friso usinado | '
          f'{volume_assinado(ct.tris) / 1000.0 * cm.RHO_SIL * 1000:5.1f} g em silicone')

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
