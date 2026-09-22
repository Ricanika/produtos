#!/usr/bin/env python3
"""
Gera os STL da linha - REVISAO 7 (borda lisa com colar, trava, rodape reto).

COMO A CASCA E FEITA
  Cada peca e uma casca fechada de secoes de retangulo com cantos arredondados
  empilhadas em alturas diferentes. Bandas de quadrilateros ligam um anel ao
  seguinte e tampos em leque fecham as pontas. O raio de cada anel sai da regra
  de curva paralela: deslocar a secao de d para dentro tira d do raio.

DUAS ARMADILHAS JA PAGAS
  1. anel() sai em sentido HORARIO visto de cima. Se sair anti-horario, o
     volume assinado vem negativo.
  2. Volume assinado NAO detecta normal invertida: uma casca estanque com um
     tampo ao contrario continua fechada e ainda devolve um numero. Por isso
     normais_consistentes() confere que toda aresta aparece uma vez em cada
     sentido, e main() aborta se falhar.

Uso:  python3 gera-3d.py [--seg 12]      (--seg = pontos por canto)
"""
import json, math, struct, sys, os

# ---- cotas da linha (iguais as de calculo-modular.py) ----
COLAR_L, COLAR_W = 148.6, 84.9   # medida MAXIMA da peca (face externa do colar)
R_EXT   = 10.0                   # raio de canto externo, no colar
M       = 60.0                   # modulo
SAIDA   = 0.50                   # graus por lado
BASE_T  = 2.00                   # espessura do fundo (igual nos quatro)
COLAR_H = 5.00                   # altura do colar
REB     = 3.50                   # quanto o colar sobressai do corpo, por lado
W_BORDA = 1.80                   # parede na faixa do colar
ARRED   = 0.50                   # arredondamento da aresta de cima da borda
CHANF_B = 0.40                   # chanfro de entrada da boca
WALL    = {1: 1.15, 2: 1.20, 3: 1.30, 4: 1.40}
ELEV    = {1: 2.96, 2: 3.90, 3: 2.92, 4: 0.00}   # elevacao do fundo

# ---- vedacao, comum as duas tampas ----
PLUG_FOLGA = 0.60
FRISO_PROF = 0.60
FILETE_D   = 1.40
FILETE_SOB = 0.80
BANDEJA_FE = 0.50

# ---- tampa PE com trava ----
PE_DECK     = 1.50
PE_PLUG_PAR = 0.80
PE_ABA_FORA = 3.10          # quanto o deck passa da face do colar, por lado
PE_PLUG_H   = 6.00          # quanto o plug desce abaixo do plano da borda
ABA_N       = 6
ABA_LARG    = 18.0
ABA_T       = 1.00
ABA_FOLGA   = 0.30          # folga da aba sobre a face do colar
ABA_FARPA   = 1.85          # quanto a farpa avanca para dentro da face do colar
ABA_Z0      = 0.50          # topo da aba, dentro do deck (garante fusao)
ABA_Z1      = -11.00        # ponta do rabo

# ---- tampa de teca ----
TECA_ESP = 8.0

T   = math.tan(math.radians(SAIDA))
DLW = COLAR_L - COLAR_W
BOCA = COLAR_L - 2 * W_BORDA
CORPO_L = COLAR_L - 2 * REB


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
        self.prismas = []          # abas de trava: perfil extrudado, fora dos aneis

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
        """Tampo em leque. O leque inverte para a normal apontar para +z:
        num prisma, o tampo de cima tem de valer +A.h/3 no volume assinado."""
        self.caps.append([i, 1 if para_cima else 0])
        P = self._pts(i)
        c = (sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P), P[0][2])
        for k in range(len(P)):
            t = (c, P[k], P[(k + 1) % len(P)])
            self.tris.append(t[::-1] if para_cima else t)


def prisma(perfil, eixo, pos, comp):
    """Solido fechado extrudado de um perfil (d, z) ao longo de um lado.

    perfil: lista fechada de (d, z), d medido para FORA a partir da face do
    colar. eixo: 'x' (lado curto) ou 'y' (lado comprido). pos: a coordenada da
    face do colar nesse lado, com sinal. comp: largura da aba.
    """
    n = len(perfil)
    s = 1.0 if pos > 0 else -1.0
    def P(d, z, u):
        v = pos + s * d
        return (u, v, z) if eixo == 'y' else (v, u, z)
    A = [P(d, z, -comp / 2) for d, z in perfil]
    B = [P(d, z, +comp / 2) for d, z in perfil]
    tris = []
    # paredes laterais
    for k in range(n):
        k2 = (k + 1) % n
        tris.append((A[k], A[k2], B[k]))
        tris.append((A[k2], B[k2], B[k]))
    # tampos das duas pontas, em leque
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
    """Um pote. z=0 no plano de apoio (o fundo, que agora e RETO).

    De cima para baixo a peca SO ESTREITA: colar -> corpo -> fundo. Nenhuma
    contra-saida, nenhuma gaveta. O rebaixo onde a trava engata nao e uma
    canaleta: e a face de baixo do colar.
    """
    w, elev = WALL[n_mod], ELEV[n_mod]
    H = n_mod * M + BASE_T
    z_col = H - COLAR_H
    piso = BASE_T + elev
    corpo_z = lambda z: CORPO_L - 2 * (z_col - z) * T      # corpo, face externa
    colar_z = lambda z: COLAR_L - 2 * (H - z) * T          # colar, face externa
    boca_z  = lambda z: BOCA - 2 * (H - z) * T             # furo

    c = Casca(seg)
    L0  = c.add(0.0,            corpo_z(0.0))                 # aresta do fundo
    L1  = c.add(z_col,          CORPO_L)                      # topo do corpo
    L2  = c.add(z_col,          colar_z(z_col))               # ARESTA DE ENGATE
    L3  = c.add(H - ARRED,      COLAR_L)                      # face externa do colar
    L4  = c.add(H,              COLAR_L - 2 * ARRED)          # aresta de cima, arredondada
    L5  = c.add(H,              BOCA + 2 * CHANF_B)           # chanfro de entrada
    L6  = c.add(H - CHANF_B,    BOCA)                         # furo
    L7  = c.add(z_col,          boca_z(z_col))                # furo no fim do colar
    L8  = c.add(z_col,          CORPO_L - 2 * w)              # degrau interno
    L9  = c.add(piso,           corpo_z(piso) - 2 * w)        # piso interno
    for a, b in ((L0,L1),(L1,L2),(L2,L3),(L3,L4),(L4,L5),(L5,L6),(L6,L7),
                 (L7,L8),(L8,L9)):
        c.banda(a, b)
    c.cap(L9, True)                                           # piso, por cima
    if elev >= 0.05:
        L10 = c.add(elev, corpo_z(elev) - 2 * w)              # face de baixo do piso
        L11 = c.add(0.0,  corpo_z(0.0) - 2 * w)               # face interna do rodape
        c.cap(L10, False)
        c.banda(L10, L11)
        c.banda(L11, L0)
    else:
        L11 = c.add(0.0, corpo_z(0.0) - 2 * w)
        c.cap(L11, False)
        c.banda(L11, L0)
    return c, H


def cavidade(n_mod, seg):
    """Fecha so a cavidade interna, para conferir a capacidade na malha."""
    w, elev = WALL[n_mod], ELEV[n_mod]
    H = n_mod * M + BASE_T
    z_col = H - COLAR_H
    piso = BASE_T + elev
    corpo_z = lambda z: CORPO_L - 2 * (z_col - z) * T
    boca_z  = lambda z: BOCA - 2 * (H - z) * T
    c = Casca(seg)
    K0 = c.add(piso,   corpo_z(piso) - 2 * w)
    K1 = c.add(z_col,  CORPO_L - 2 * w)
    K2 = c.add(z_col,  boca_z(z_col))
    K3 = c.add(H,      BOCA)
    c.cap(K0, False)
    for a, b in ((K0,K1),(K1,K2),(K2,K3)):
        c.banda(a, b)
    c.cap(K3, True)
    return volume_assinado(c.tris)


def tampa_teca(seg):
    """Placa macica de teca com friso na face lateral. z=0 no plano da borda.

    O topo da placa fica BASE_T abaixo da borda: e ele o plano modular, e o
    fundo reto do pote de cima pousa direto nele. Nao ha poco a usinar - era o
    ponto em aberto da revisao 6.
    """
    plug = BOCA - 2 * PLUG_FOLGA
    friso = plug - 2 * FRISO_PROF
    z_top = -BASE_T
    z_bot = z_top - TECA_ESP
    zf0, zf1 = z_top - 3.0, z_top - 3.0 - FILETE_D   # faixa do friso

    c = Casca(seg)
    P0 = c.add(z_top, plug)          # topo: o plano modular
    P1 = c.add(zf0,   plug)
    P2 = c.add(zf0,   friso)         # friso
    P3 = c.add(zf1,   friso)
    P4 = c.add(zf1,   plug)
    P5 = c.add(z_bot + 0.6, plug)
    P6 = c.add(z_bot, plug - 1.2)    # quebra-canto embaixo
    for a, b in ((P1,P0),(P2,P1),(P3,P2),(P4,P3),(P5,P4),(P6,P5)):
        c.banda(a, b)
    c.cap(P0, True)
    c.cap(P6, False)
    return c


def tampa_pe(seg):
    """Tampa PP/PE com trava. z=0 no plano da borda do pote.

    Tres coisas, cada uma com uma funcao so:
      - o PLUG desce na boca, leva o MESMO friso e o MESMO filete da teca, e
        veda radial;
      - a BANDEJA (piso 2,0 mm abaixo da borda) recebe o fundo reto do pote de
        cima e e o plano modular;
      - as ABAS engatam sob o colar e dao a forca de fechamento que a teca nao
        tem. O filete so veda; quem segura e a trava.
    """
    plug = BOCA - 2 * PLUG_FOLGA
    friso = plug - 2 * FRISO_PROF
    bandeja = plug - 2 * PE_PLUG_PAR
    deck_o = COLAR_L + 2 * PE_ABA_FORA
    z_pf = -PE_PLUG_H
    zf0, zf1 = -3.0, -3.0 - FILETE_D

    c = Casca(seg)
    D0  = c.add(-BASE_T,        bandeja)        # piso da bandeja = plano modular
    D1  = c.add(PE_DECK,        bandeja)        # parede da bandeja sobe
    D2  = c.add(PE_DECK,        deck_o)         # topo do deck
    D3  = c.add(0.0,            deck_o)         # face externa do deck
    D4  = c.add(0.0,            COLAR_L + 2 * ABA_FOLGA)   # face de baixo do deck
    D5  = c.add(0.0,            plug)           # apoia na borda e entra na boca
    D6  = c.add(zf0,            plug)
    D7  = c.add(zf0,            friso)          # friso do filete
    D8  = c.add(zf1,            friso)
    D9  = c.add(zf1,            plug)
    D10 = c.add(z_pf + 0.5,     plug)
    D11 = c.add(z_pf,           plug - 1.0)     # ponta do plug, com quebra-canto
    D12 = c.add(z_pf,           bandeja)        # face interna do plug
    D13 = c.add(-BASE_T - PE_DECK, bandeja)     # face de baixo do piso
    for a, b in ((D1,D0),(D2,D1),(D3,D2),(D4,D3),(D5,D4),(D6,D5),(D7,D6),(D8,D7),
                 (D9,D8),(D10,D9),(D11,D10),(D12,D11),(D13,D12)):
        c.banda(a, b)
    c.cap(D0, True)
    c.cap(D13, False)

    # ---- abas de trava: prismas separados, 0,5 mm dentro do deck ----
    perfil = [(ABA_FOLGA, ABA_Z0),
              (ABA_FOLGA, -COLAR_H),
              (-ABA_FARPA, -COLAR_H - 0.6),
              (ABA_FOLGA, -COLAR_H - 1.6),
              (ABA_FOLGA, ABA_Z1),
              (ABA_FOLGA + ABA_T, ABA_Z1),
              (ABA_FOLGA + ABA_T, ABA_Z0)]
    meia_l, meia_w = COLAR_L / 2, COLAR_W / 2
    postos = [('y',  meia_w,  34.0), ('y',  meia_w, -34.0),
              ('y', -meia_w,  34.0), ('y', -meia_w, -34.0),
              ('x',  meia_l,   0.0), ('x', -meia_l,  0.0)]
    for eixo, pos, off in postos[:ABA_N]:
        tris = prisma(perfil, eixo, pos, ABA_LARG)
        if eixo == 'y':
            c.tris += [tuple((x + off, y, z) for x, y, z in t) for t in tris]
        else:
            c.tris += [tuple((x, y + off, z) for x, y, z in t) for t in tris]
        c.prismas.append(dict(perfil=perfil, eixo=eixo, pos=pos,
                              comp=ABA_LARG, off=off))
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
    """Toda aresta tem de aparecer uma vez em cada sentido.

    Volume assinado NAO detecta normais invertidas: uma malha estanque com um
    tampo ao contrario continua fechada e ainda devolve um volume, so que
    errado. Foi o que aconteceu com a tampa PE na revisao 6 - 17,5 g em vez de
    27,6 - e so apareceu quando a malha foi aberta noutro programa.
    """
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
    base = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(base, 'stl')
    os.makedirs(out, exist_ok=True)

    perfis = {'seg': seg, 'pecas': {}}
    checar = []
    for n in (1, 2, 3, 4):
        c, H = corpo(n, seg)
        nome = f'pote-{n * 600}'
        grava_stl(os.path.join(out, nome + '.stl'), c.tris, nome)
        perfis['pecas'][nome] = dict(loops=c.loops, bands=c.bands, caps=c.caps,
                                     prismas=c.prismas,
                                     H=H, passo=n * M, cap=n * 600)
        checar.append((nome, c))
        vcav = cavidade(n, seg) / 1000.0
        vmat = volume_assinado(c.tris) / 1000.0
        print(f'{nome:<12} altura {H:6.1f} mm | {len(c.tris):5d} tri | '
              f'cavidade {vcav:7.1f} ml (alvo {n * 600}) | '
              f'peso da malha {vmat * 0.905:6.1f} g')

    t = tampa_teca(seg)
    grava_stl(os.path.join(out, 'tampa-teca.stl'), t.tris, 'tampa-teca')
    perfis['pecas']['tampa-teca'] = dict(loops=t.loops, bands=t.bands, caps=t.caps, prismas=t.prismas)
    checar.append(('tampa-teca', t))
    print(f'{"tampa-teca":<12} {"":13} | {len(t.tris):5d} tri | placa macica, '
          f'{volume_assinado(t.tris) / 1000.0 * 0.65:5.0f} g em teca')

    tp = tampa_pe(seg)
    grava_stl(os.path.join(out, 'tampa-pe.stl'), tp.tris, 'tampa-pe')
    perfis['pecas']['tampa-pe'] = dict(loops=tp.loops, bands=tp.bands, caps=tp.caps, prismas=tp.prismas)
    checar.append(('tampa-pe', tp))
    print(f'{"tampa-pe":<12} {"":13} | {len(tp.tris):5d} tri | com {ABA_N} abas | '
          f'{volume_assinado(tp.tris) / 1000.0 * 0.905:5.1f} g em PP')

    a = filete(seg)
    grava_stl(os.path.join(out, 'filete-tpe.stl'), a.tris, 'filete-tpe')
    perfis['pecas']['filete'] = dict(loops=a.loops, bands=a.bands, caps=a.caps, prismas=a.prismas)
    checar.append(('filete-tpe', a))
    print(f'{"filete-tpe":<12} {"":13} | {len(a.tris):5d} tri | '
          f'{volume_assinado(a.tris) / 1000.0 * 1.10:5.1f} g em TPE')

    with open(os.path.join(base, 'perfis.json'), 'w') as f:
        json.dump(perfis, f, separators=(',', ':'))

    ruim = [nome for nome, cc in checar
            if not normais_consistentes(cc.tris) or volume_assinado(cc.tris) <= 0]
    print('\nSTL em', out)
    print('Normais consistentes e volume positivo nas %d pecas: %s'
          % (len(checar), 'OK' if not ruim else 'FALHOU EM ' + ', '.join(ruim)))
    if ruim:
        sys.exit(1)
    print('\nAs abas de trava sao prismas separados que entram 0,5 mm no deck, para')
    print('fundirem no fatiador. O volume conta esses 0,5 mm duas vezes: ~54 mm3,')
    print('0,2%% da tampa.')


if __name__ == '__main__':
    main()
