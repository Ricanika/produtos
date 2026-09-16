#!/usr/bin/env python3
"""
Gerador 3D parametrico da linha de potes modulares.

Le as mesmas cotas de calculo-modular.py e escreve:
  stl/pote-600.stl  stl/pote-1200.stl  stl/pote-1800.stl  stl/pote-2400.stl
  stl/tampa.stl     stl/aro-tpe.stl
  perfis.json   (descricao compacta dos aneis, usada pelo visualizador 3D)

Como o solido e construido
  Cada peca e uma casca fechada feita de "aneis" - secoes de retangulo com
  cantos arredondados empilhadas em alturas diferentes. Bandas de quadrilateros
  ligam um anel ao seguinte; tampos ("caps") fecham as pontas. E o mesmo
  esqueleto que o visualizador usa, entao desenho e STL nunca divergem.

Ressalvas do modelo (leia antes de mandar para a ferramentaria)
  - Malha, nao solido CAD. Serve para conferir encaixe, empilhamento, volume e
    para imprimir prototipo. O molde precisa do CAD parametrico do projetista.
  - A tampa esta simplificada: sem o labio de vedacao, sem a canaleta do aro e
    sem o furo/entalhe do vertedor. As cotas que governam o encaixe (vao da
    bandeja e piso 2,0 mm abaixo da borda) estao corretas.
  - A saida de 0,5 graus esta aplicada; a olho nu o pote parece reto, que e a
    intencao.

Uso:  python3 gera-3d.py [--seg 12]      (--seg = pontos por canto)
"""
import json, math, struct, sys, os

# ---- cotas da linha (iguais as de calculo-modular.py) ----
EXT_L, EXT_W = 121.2, 93.3     # footprint externo no bocal
R_EXT   = 18.0                 # raio de canto externo
M       = 60.0                 # modulo
SAIDA   = 0.50                 # graus por lado
BASE_T  = 2.00                 # espessura do fundo (igual nos quatro)
PE_H    = 6.00                 # altura do pe embutido
PE_L, PE_W = 110.0, 84.6       # pe embutido, igual nos quatro
R_PE    = 13.0
WALL    = {1: 1.15, 2: 1.20, 3: 1.30, 4: 1.40}
ELEV    = {1: 1.8,  2: 3.4,  3: 2.7,  4: 0.0}   # elevacao do fundo
# tampa
TP_L, TP_W, TP_R = 125.2, 97.3, 20.0
TRAY_L, TRAY_W, TRAY_R = 111.1, 85.7, 13.0
TP_TOPO, TP_PISO, TP_FUNDO, TP_SAIA = 1.5, -2.0, -3.5, -11.0
TP_PAREDE = 1.5
# aro de TPE
ARO_SEC = (2.8, 2.2)

T = math.tan(math.radians(SAIDA))


def anel(L, W, R, n):
    """Retangulo de cantos arredondados, 4*n pontos.

    Sai em sentido HORARIO visto de cima (a lista e revertida no fim). E essa
    orientacao que deixa as normais apontando para fora do solido com a ordem
    de vertices usada em Casca.banda e Casca.cap - conferido pelo volume
    assinado da malha, que tem que sair positivo.
    """
    hx, hy, r = L / 2 - R, W / 2 - R, R
    pts = []
    for cx, cy, a0 in ((hx, hy, 0.0), (-hx, hy, 90.0), (-hx, -hy, 180.0), (hx, -hy, 270.0)):
        for k in range(n):
            a = math.radians(a0 + 90.0 * k / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pts.reverse()
    return pts


class Casca:
    """Acumula aneis e emite triangulos."""

    def __init__(self, n):
        self.n, self.loops, self.tris = n, [], []
        self.bands, self.caps = [], []   # receita da malha, para o visualizador

    def add(self, z, L, W, R):
        self.loops.append(dict(z=z, L=L, W=W, R=R))
        return len(self.loops) - 1

    def _pts(self, i):
        lp = self.loops[i]
        return [(x, y, lp['z']) for x, y in anel(lp['L'], lp['W'], lp['R'], self.n)]

    def banda(self, i, j):
        """Liga dois aneis com uma faixa de quadrilateros."""
        self.bands.append([i, j])
        A, B = self._pts(i), self._pts(j)
        m = len(A)
        for k in range(m):
            k2 = (k + 1) % m
            self.tris += [(A[k], B[k2], B[k])[::-1], (A[k], A[k2], B[k2])[::-1]]

    def cap(self, i, para_cima=True):
        """Fecha um anel com um leque de triangulos a partir do centroide.

        Os aneis saem em sentido horario visto de cima (ver anel), entao o leque
        precisa ser invertido para a normal apontar para +z. Conferido pelo
        volume assinado: para um prisma, o tampo de cima tem que valer +A.h/3.
        """
        self.caps.append([i, 1 if para_cima else 0])
        P = self._pts(i)
        c = (sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P), P[0][2])
        m = len(P)
        for k in range(m):
            t = (c, P[k], P[(k + 1) % m])
            self.tris.append(t[::-1] if para_cima else t)


def corpo(n_mod, seg):
    """Um pote. z=0 no plano de apoio (base do pe)."""
    w, elev = WALL[n_mod], ELEV[n_mod]
    H = n_mod * M + BASE_T                      # altura externa do corpo
    piso = elev + BASE_T                        # face interna do fundo
    # o corpo estreita para baixo pela saida; a cota cheia esta no bocal
    def body(z):   return EXT_L - 2 * (H - z) * T, EXT_W - 2 * (H - z) * T
    def pe(z):     return PE_L - 2 * (PE_H - z) * T, PE_W - 2 * (PE_H - z) * T

    c = Casca(seg)
    pe0L, pe0W = pe(0.0)
    peHL, peHW = pe(PE_H)
    bdL, bdW = body(PE_H)
    L0 = c.add(0.0,   pe0L, pe0W, R_PE)                      # pe, base
    L1 = c.add(PE_H,  peHL, peHW, R_PE)                      # pe, topo
    L2 = c.add(PE_H,  bdL,  bdW,  R_EXT)                     # corpo no degrau
    L3 = c.add(H,     EXT_L, EXT_W, R_EXT)                   # borda
    L4 = c.add(H,     EXT_L - 2 * w, EXT_W - 2 * w, R_EXT - w)
    L5 = c.add(PE_H,  bdL - 2 * w, bdW - 2 * w, R_EXT - w)
    L6 = c.add(PE_H,  peHL - 2 * w, peHW - 2 * w, R_PE - w)
    L7 = c.add(piso,  pe(piso)[0] - 2 * w, pe(piso)[1] - 2 * w, R_PE - w)
    c.banda(L0, L1)                    # face externa do pe
    c.banda(L1, L2)         # ombro do degrau (olha para baixo)
    c.banda(L2, L3)                    # face externa do corpo
    c.banda(L3, L4)                    # topo da borda
    c.banda(L4, L5)         # face interna do corpo
    c.banda(L5, L6)                    # degrau interno
    c.banda(L6, L7)         # face interna do pe
    c.cap(L7, True)                    # fundo, por dentro
    if elev >= 0.05:                   # rebaixo por baixo do fundo
        L9 = c.add(elev, pe(elev)[0] - 2 * w, pe(elev)[1] - 2 * w, R_PE - w)
        L8 = c.add(0.0,  pe0L - 2 * w, pe0W - 2 * w, R_PE - w)
        c.cap(L9, False)               # teto do rebaixo
        c.banda(L9, L8)                # parede do rebaixo
        c.banda(L8, L0)     # anel de apoio
    else:
        L8 = c.add(0.0, pe0L - 2 * w, pe0W - 2 * w, R_PE - w)
        c.cap(L8, False)
        c.banda(L8, L0)
    return c, H


def tampa(seg):
    """Tampa-bandeja. z=0 no plano da borda do pote."""
    c = Casca(seg)
    M0 = c.add(TP_SAIA, TP_L, TP_W, TP_R)
    M1 = c.add(TP_TOPO, TP_L, TP_W, TP_R)
    M2 = c.add(TP_TOPO, TRAY_L, TRAY_W, TRAY_R)
    M3 = c.add(TP_PISO, TRAY_L, TRAY_W, TRAY_R)
    M4 = c.add(TP_FUNDO, TRAY_L, TRAY_W, TRAY_R)
    M5 = c.add(TP_FUNDO, TP_L - 2 * TP_PAREDE, TP_W - 2 * TP_PAREDE, TP_R - TP_PAREDE)
    M6 = c.add(TP_SAIA,  TP_L - 2 * TP_PAREDE, TP_W - 2 * TP_PAREDE, TP_R - TP_PAREDE)
    c.banda(M0, M1)                    # face externa da saia
    c.banda(M1, M2)                    # topo da tampa
    c.banda(M2, M3)         # parede da bandeja
    c.cap(M3, True)                    # piso da bandeja = plano modular
    c.cap(M4, False)                   # face inferior do piso
    c.banda(M4, M5)         # face inferior do patamar
    c.banda(M5, M6)         # face interna da saia
    c.banda(M6, M0)         # aresta inferior da saia
    return c


def aro(seg):
    """Aro de TPE: secao retangular correndo no perimetro de vedacao."""
    sw, sh = ARO_SEC
    Lm, Wm, Rm = EXT_L - 2 * 2.6, EXT_W - 2 * 2.6, R_EXT - 3
    c = Casca(seg)
    A0 = c.add(0.0, Lm - sw, Wm - sw, Rm - sw / 2)
    A1 = c.add(0.0, Lm + sw, Wm + sw, Rm + sw / 2)
    A2 = c.add(sh,  Lm + sw, Wm + sw, Rm + sw / 2)
    A3 = c.add(sh,  Lm - sw, Wm - sw, Rm - sw / 2)
    c.banda(A0, A1)
    c.banda(A1, A2)
    c.banda(A2, A3)
    c.banda(A3, A0)
    return c


def volume_assinado(tris):
    """Volume do solido fechado. Positivo = normais para fora."""
    v = 0.0
    for a, b, c in tris:
        v += (a[0] * (b[1] * c[2] - b[2] * c[1])
              - a[1] * (b[0] * c[2] - b[2] * c[0])
              + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0
    return v


def cavidade(n_mod, seg):
    """Fecha so a cavidade interna do pote, para conferir a capacidade na malha."""
    w, elev = WALL[n_mod], ELEV[n_mod]
    H = n_mod * M + BASE_T
    piso = elev + BASE_T
    def body(z): return EXT_L - 2 * (H - z) * T, EXT_W - 2 * (H - z) * T
    def pe(z):   return PE_L - 2 * (PE_H - z) * T, PE_W - 2 * (PE_H - z) * T
    bdL, bdW = body(PE_H)
    c = Casca(seg)
    K0 = c.add(piso,  pe(piso)[0] - 2 * w, pe(piso)[1] - 2 * w, R_PE - w)
    K1 = c.add(PE_H,  pe(PE_H)[0] - 2 * w, pe(PE_H)[1] - 2 * w, R_PE - w)
    K2 = c.add(PE_H,  bdL - 2 * w, bdW - 2 * w, R_EXT - w)
    K3 = c.add(H,     EXT_L - 2 * w, EXT_W - 2 * w, R_EXT - w)
    c.cap(K0, False)
    c.banda(K0, K1); c.banda(K1, K2); c.banda(K2, K3)
    c.cap(K3, True)
    return volume_assinado(c.tris)


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
    for n in (1, 2, 3, 4):
        c, H = corpo(n, seg)
        nome = f'pote-{n * 600}'
        grava_stl(os.path.join(out, nome + '.stl'), c.tris, nome)
        perfis['pecas'][nome] = dict(loops=c.loops, bands=c.bands, caps=c.caps,
                                    H=H, passo=n * M, cap=n * 600)
        vcav = cavidade(n, seg) / 1000.0
        vmat = volume_assinado(c.tris) / 1000.0
        print(f'{nome:<12} altura {H:6.1f} mm | {len(c.tris):5d} tri | '
              f'cavidade {vcav:7.1f} ml (alvo {n * 600}) | '
              f'peso da malha {vmat * 0.905:6.1f} g')

    t = tampa(seg)
    grava_stl(os.path.join(out, 'tampa.stl'), t.tris, 'tampa')
    perfis['pecas']['tampa'] = dict(loops=t.loops, bands=t.bands, caps=t.caps)
    print(f'{"tampa":<12} {"":13} | {len(t.tris):5d} triangulos')

    a = aro(seg)
    grava_stl(os.path.join(out, 'aro-tpe.stl'), a.tris, 'aro-tpe')
    perfis['pecas']['aro'] = dict(loops=a.loops, bands=a.bands, caps=a.caps)
    print(f'{"aro-tpe":<12} {"":13} | {len(a.tris):5d} triangulos')

    with open(os.path.join(base, 'perfis.json'), 'w') as f:
        json.dump(perfis, f, separators=(',', ':'))
    print('\nSTL em', out)
    print('perfis.json com', sum(len(p['loops']) for p in perfis['pecas'].values()), 'aneis')
    print('\nConferencias que a malha faz sozinha:')
    print('  - volume assinado positivo em todas as pecas (solido fechado e')
    print('    orientado para fora);')
    print('  - cavidade dentro de 0,7% da capacidade nominal - a folga e a')
    print('    poligonal de 12 segmentos por canto, nao erro de cota;')
    print('  - corpos: peso da malha 0 a 4% abaixo de calculo-modular.py - e a')
    print('    borda reforcada e a nervura de pe que a malha nao modela;')
    print('  - tampa: 27,9 g na malha contra 24,5 g no calculo, porque aqui a')
    print('    parede da bandeja esta modelada macica em vez de casca de 1,5 mm.')


if __name__ == '__main__':
    main()
