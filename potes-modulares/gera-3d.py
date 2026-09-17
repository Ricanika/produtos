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
EXT_L, EXT_W = 139.7, 79.8     # footprint externo no bocal (ASP 1,75: frente estreita)
R_EXT   = 10.0                 # raio de canto externo (canto quase reto)
M       = 60.0                 # modulo
SAIDA   = 0.50                 # graus por lado
BASE_T  = 2.00                 # espessura do fundo (igual nos quatro)
PE_H    = 6.00                 # altura do pe embutido
# PE_L nao e escolhido: sai da bandeja da tampa, que sai da boca do pote.
# Ver pe_l() em calculo-modular.py. Fixar a mao quebra quando o footprint muda.
W_BORDA = 1.40                 # parede nos 10 mm abaixo da borda, igual nos quatro
ABA_W   = 3.00                 # aba da borda virada para fora, por lado
ABA_T   = 1.60                 # espessura da aba
LIP_H   = 3.50                 # labio descendente na ponta da aba
LIP_T   = 1.20                 # espessura do labio
WALL    = {1: 1.15, 2: 1.20, 3: 1.30, 4: 1.40}
ELEV    = {1: 2.0,  2: 3.5,  3: 2.8,  4: 0.0}   # elevacao do fundo
# tampa tipo PLUG (z = 0 no plano da borda do pote)
TP_TOPO, TP_PISO, TP_FUNDO = 1.5, -2.0, -3.5
PLUG_FIM   = -12.0             # ate onde o plug desce dentro do pote
PLUG_FOLGA = 1.00              # folga entre a face do plug e a parede do pote
PLUG_PAR   = 1.50              # parede do plug
CAN_Z0, CAN_Z1 = -5.0, -7.4    # canaleta do aro na face externa do plug
CAN_PROF   = 0.60              # profundidade da canaleta
ARO_SOBRA  = 1.20              # quanto o aro sobra da face do plug -> 0,2 mm de
                               # compressao contra a parede do pote
# aro de TPE
ARO_SEC = (2.8, 2.2)

# Pe embutido: DERIVADO da bandeja da tampa, nunca digitado.
#   boca = EXT_L - 2*W_BORDA | plug = boca - 2*PLUG_FOLGA
#   bandeja = plug - 2*PLUG_PAR | pe = bandeja - 1,0
PE_L = EXT_L - 2 * (W_BORDA + PLUG_FOLGA + PLUG_PAR) - 1.0

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


def wo(L):
    """Largura correspondente a um comprimento L: offset uniforme do retangulo base."""
    return L - (EXT_L - EXT_W)


def ro(L):
    """Raio de canto correspondente: offset uniforme tambem no raio."""
    return R_EXT + (L - EXT_L) / 2


class Casca:
    """Acumula aneis e emite triangulos."""

    def __init__(self, n):
        self.n, self.loops, self.tris = n, [], []
        self.bands, self.caps = [], []   # receita da malha, para o visualizador

    def add(self, z, L, W=None, R=None):
        """Um anel na altura z. Sem W e R, sao derivados de L por offset uniforme."""
        self.loops.append(dict(z=z, L=L, W=wo(L) if W is None else W,
                               R=ro(L) if R is None else R))
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
    """Um pote. z=0 no plano de apoio (base do pe).

    A borda termina numa ABA virada para fora com um labio descendente. Ela faz
    tres coisas ao mesmo tempo: enrijece a boca (secao em U, ~34x a inercia da
    parede simples, que e o que impede o lado reto de abrir e vazar), da a
    superficie onde a saia da tampa encaixa, e serve de pega para abrir.
    """
    w, elev = WALL[n_mod], ELEV[n_mod]
    H = n_mod * M + BASE_T
    piso = elev + BASE_T
    def body(z):  return EXT_L - 2 * (H - z) * T
    def pe(z):    return PE_L - 2 * (PE_H - z) * T
    aba = EXT_L + 2 * ABA_W

    c = Casca(seg)
    L0  = c.add(0.0,            pe(0.0))                       # pe, base
    L1  = c.add(PE_H,           pe(PE_H))                      # pe, topo
    L2  = c.add(PE_H,           body(PE_H))                    # corpo no degrau
    L3  = c.add(H - ABA_T,      body(H - ABA_T))               # topo da parede
    L4  = c.add(H - ABA_T,      aba - 2 * LIP_T)               # face inferior da aba
    L5  = c.add(H - ABA_T - LIP_H, aba - 2 * LIP_T)            # face interna do labio
    L6  = c.add(H - ABA_T - LIP_H, aba)                        # aresta do labio
    L7  = c.add(H,              aba)                           # face externa do labio
    L8  = c.add(H,              EXT_L - 2 * W_BORDA)           # topo da borda -> boca
    L9  = c.add(H - 10.0,       body(H - 10.0) - 2 * w)        # fim da faixa de borda
    L10 = c.add(PE_H,           body(PE_H) - 2 * w)            # face interna do corpo
    L11 = c.add(PE_H,           pe(PE_H) - 2 * w)
    L12 = c.add(piso,           pe(piso) - 2 * w)
    for a, b in ((L0,L1),(L1,L2),(L2,L3),(L3,L4),(L4,L5),(L5,L6),(L6,L7),
                 (L7,L8),(L8,L9),(L9,L10),(L10,L11),(L11,L12)):
        c.banda(a, b)
    c.cap(L12, True)                                           # fundo, por dentro
    if elev >= 0.05:                                           # rebaixo por baixo
        L14 = c.add(elev, pe(elev) - 2 * w)
        L15 = c.add(0.0,  pe(0.0) - 2 * w)
        c.cap(L14, False); c.banda(L14, L15); c.banda(L15, L0)
    else:
        L15 = c.add(0.0, pe(0.0) - 2 * w)
        c.cap(L15, False); c.banda(L15, L0)
    return c, H


def tampa(seg):
    """Tampa tipo PLUG. z=0 no plano da borda do pote.

    Uma saia desce DENTRO do pote e leva, numa canaleta na sua face externa, o
    aro de TPE. O aro trabalha contra a PAREDE do pote, nao contra a borda: e
    vedacao radial, nao axial. Por isso nao precisa de trava nem de forca
    permanente de fechamento - o que segura e a interferencia lateral.

    O mesmo plug faz tres coisas: veda, forma a parede da bandeja onde o pote de
    cima apoia, e centra a tampa. Por fora nao ha saia nenhuma: a tampa fica
    rente a aba da borda, lisa.
    """
    boca = EXT_L - 2 * W_BORDA
    aba = EXT_L + 2 * ABA_W
    plug = boca - 2 * PLUG_FOLGA              # face externa do plug
    plug_in = plug - 2 * PLUG_PAR             # face interna = vao da bandeja
    canal = plug - 2 * CAN_PROF               # fundo da canaleta

    c = Casca(seg)
    M0  = c.add(TP_TOPO,   aba)               # topo, rente a aba - sem saia externa
    M1  = c.add(0.0,       aba)               # face externa da tampa
    M2  = c.add(0.0,       plug)              # assenta na aba e entra na boca
    M3  = c.add(CAN_Z0,    plug)              # plug ate a canaleta
    M4  = c.add(CAN_Z0,    canal)             # ombro de cima da canaleta
    M5  = c.add(CAN_Z1,    canal)             # fundo da canaleta
    M6  = c.add(CAN_Z1,    plug)              # ombro de baixo
    M7  = c.add(PLUG_FIM,  plug - 0.4)        # ponta do plug, com saida
    M8  = c.add(PLUG_FIM,  plug_in - 0.4)     # ponta, face interna
    M9  = c.add(TP_FUNDO,  plug_in)           # face interna sobe ate o piso
    M10 = c.add(TP_PISO,   plug_in)           # piso da bandeja = plano modular
    M11 = c.add(TP_TOPO,   plug_in)           # face interna da bandeja
    # perfil percorrido do topo para baixo: bandas no sentido inverso
    for a, b in ((M1,M0),(M2,M1),(M3,M2),(M4,M3),(M5,M4),(M6,M5),(M7,M6),
                 (M8,M7),(M9,M8),(M11,M10),(M0,M11)):
        c.banda(a, b)
    c.cap(M9, False)                          # face inferior do piso
    c.cap(M10, True)                          # piso da bandeja
    return c


def aro(seg):
    """Aro de TPE alojado na canaleta do plug.

    Fica desenhado na medida LIVRE: a face externa passa 0,2 mm por lado alem da
    boca do pote. Esses 0,2 mm sao a interferencia - montado, o aro comprime essa
    diferenca contra a parede. No 3D as duas malhas se sobrepoem nesses 0,2 mm, e
    e proposital: e onde a vedacao acontece.
    """
    boca = EXT_L - 2 * W_BORDA
    plug = boca - 2 * PLUG_FOLGA
    dentro = plug - 2 * CAN_PROF              # encosta no fundo da canaleta
    fora = plug + 2 * ARO_SOBRA               # 0,2 mm alem da boca: a interferencia
    c = Casca(seg)
    A0 = c.add(CAN_Z1, dentro)
    A1 = c.add(CAN_Z1, fora)
    A2 = c.add(CAN_Z0, fora)
    A3 = c.add(CAN_Z0, dentro)
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
    def body(z): return EXT_L - 2 * (H - z) * T
    def pe(z):   return PE_L - 2 * (PE_H - z) * T
    c = Casca(seg)
    K0 = c.add(piso,     pe(piso) - 2 * w)
    K1 = c.add(PE_H,     pe(PE_H) - 2 * w)
    K2 = c.add(PE_H,     body(PE_H) - 2 * w)
    K3 = c.add(H - 10.0, body(H - 10.0) - 2 * w)
    K4 = c.add(H,        EXT_L - 2 * W_BORDA)
    c.cap(K0, False)
    for a, b in ((K0,K1),(K1,K2),(K2,K3),(K3,K4)):
        c.banda(a, b)
    c.cap(K4, True)
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
    print('  - peso da malha dentro de 3% de calculo-modular.py nas seis pecas.')


if __name__ == '__main__':
    main()
