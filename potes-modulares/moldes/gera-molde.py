#!/usr/bin/env python3
"""
Gerador do PROJETO DE MOLDE (conceito) da linha de potes modulares.

Le o mesmo parametrico que gera a peca (gera-3d.py), aplica CONTRACAO e escreve,
por tamanho:

  moldes/stl/<tam>/cavidade.stl        postico de cavidade (forma o lado de fora)
  moldes/stl/<tam>/macho.stl           postico de macho + haste + flange de fixacao
  moldes/stl/<tam>/placa-impulsora.stl placa que extrai a peca pela aba
  moldes/stl/<tam>/refrigeracao.stl    circuitos como corpos solidos (visualizacao)
  moldes/desenhos/molde-<tam>.svg      corte do conjunto, em escala
  moldes/ficha-molde-<tam>.md          ficha com todos os calculos

O QUE ISTO E, E O QUE NAO E
  E   conceito de molde: geometria formadora com contracao aplicada, layout de
      cavidades, dimensionamento de bloco, tonelagem, curso, circuito de agua,
      posicao de gate e de extracao — o suficiente para cotar e para discutir
      com ferramentaria sem comecar do zero.
  NAO e projeto executivo. Falta: porta-molde normalizado real (HASCO/DME/
      Meusburger com codigo de catalogo), detalhamento 2D com GD&T, tolerancias
      de ajuste, eletrodos, camara quente especificada por modelo, respiros,
      parafusos, Moldflow e a validacao de tudo isso no T1.
  E MALHA, nao solido CAD. Serve para ver, medir e cotar; nao para usinar.

Uso:  python3 gera-molde.py [--seg 12] [--contracao 1.5] [--cav 2]
"""
import importlib.util, json, math, os, struct, sys

BASE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(BASE)

# ---- importa o parametrico da peca ----------------------------------------
_spec = importlib.util.spec_from_file_location('gera3d', os.path.join(RAIZ, 'gera-3d.py'))
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)

# ---- regras de projeto do molde (as que o agente da secao 8 lista) --------
ACO_LATERAL   = 32.0    # aco do postico em volta da bolsa, por lado
ACO_FUNDO     = 35.0    # aco sob o fundo da bolsa (por onde passa o bico quente)
ACO_ENTRE_CAV = 60.0    # aco entre duas bolsas no porta-molde
ACO_BORDA     = 45.0    # aco do postico a borda do porta-molde
CANAL_D       = 10.0    # diametro do furo de refrigeracao
CANAL_DIST    = 22.0    # distancia do furo a superficie formadora (2,2 x D)
CANAL_PASSO   = 45.0    # passo vertical entre circuitos (4,5 x D)
HASTE_EXTRA   = 60.0    # haste do macho acima do plano de fechamento
FLANGE_MACHO  = 40.0    # altura da flange de fixacao do macho
IMPULSORA_T   = 30.0    # espessura da placa impulsora
FOLGA_IMPULS  = 0.05    # folga da placa impulsora sobre o macho, por lado
QUEDA_PECA    = 60.0    # folga de queda da peca entre as metades abertas
PLACAS = [('Placa de fixacao fixa', 30.0), ('Placa porta-cavidade', None),
          ('Placa impulsora', IMPULSORA_T), ('Placa porta-macho', 50.0),
          ('Calcos (curso de extracao)', None), ('Placa extratora dupla', 44.0),
          ('Placa de fixacao movel', 30.0)]

RHO_PP = 0.905e-3       # g/mm3
P_CAV  = 400.0          # kgf/cm2 de pressao media na cavidade (parede fina PP)
K_SEG  = 1.15           # fator de seguranca do fechamento
TAMANHOS = {1: '600', 2: '1200', 3: '1800', 4: '2400'}
CICLO  = {1: 17.0, 2: 21.0, 3: 25.0, 4: 29.0}     # s, estimativa do README


# ---- malha ----------------------------------------------------------------
class Malha:
    """Triangulos soltos, com controle explicito de orientacao.

    banda(A, B) espera A = anel de baixo, B = anel de cima (ou, para dois aneis
    no mesmo z, A = externo e B = interno) e emite normais para FORA do solido.
    flip=True inverte — e o que uma bolsa precisa: ali o aco esta do lado de
    fora e a normal aponta para dentro do vazio.
    """

    def __init__(self):
        self.tris = []

    def banda(self, A, B, flip=False):
        m = len(A)
        for k in range(m):
            k2 = (k + 1) % m
            t1 = (A[k], B[k2], B[k])[::-1]
            t2 = (A[k], A[k2], B[k2])[::-1]
            if flip:
                t1, t2 = t1[::-1], t2[::-1]
            self.tris += [t1, t2]

    def tampo(self, P, para_cima=True):
        c = (sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P), P[0][2])
        for k in range(len(P)):
            t = (c, P[k], P[(k + 1) % len(P)])
            self.tris.append(t[::-1] if para_cima else t)

    def soma(self, outra):
        self.tris += outra.tris
        return self


def pts(loop, seg):
    """Anel (dict z/L/W/R) -> lista de pontos 3D."""
    return [(x, y, loop['z']) for x, y in G.anel(loop['L'], loop['W'], loop['R'], seg)]


def ret(L, W, z, seg, R=6.0):
    """Anel retangular de bloco, com os mesmos 4*seg pontos dos aneis da peca."""
    return [(x, y, z) for x, y in G.anel(L, W, R, seg)]


def cilindro(p0, p1, d, n=20):
    """Cilindro solido entre dois pontos, eixo paralelo a X, Y ou Z."""
    eixo = [i for i in range(3) if abs(p1[i] - p0[i]) > 1e-9]
    assert len(eixo) == 1, 'so eixos ortogonais'
    e = eixo[0]
    u, v = [i for i in range(3) if i != e]
    r = d / 2.0
    def anel_z(p):
        out = []
        for k in range(n):
            a = 2 * math.pi * k / n
            q = [0.0, 0.0, 0.0]
            q[e] = p[e]; q[u] = p[u] + r * math.cos(a); q[v] = p[v] + r * math.sin(a)
            out.append(tuple(q))
        return out
    A, B = anel_z(p0), anel_z(p1)
    m = Malha()
    m.banda(A, B)
    m.tampo(B, True); m.tampo(A, False)
    if G.volume_assinado(m.tris) < 0:              # orientacao depende do eixo
        m.tris = [t[::-1] for t in m.tris]
    return m


# ---- peca com contracao ---------------------------------------------------
def aneis_do_pote(n_mod, seg, kxy, kz):
    """Aneis da peca, ja com contracao aplicada. Devolve (externos, internos, H).

    Indices de corpo() em gera-3d.py: 0..7 = superficie externa (pe -> labio da
    aba), 8..12 = superficie interna (boca -> fundo). O assert quebra alto se
    aquele arquivo mudar de ordem.
    """
    c, H = G.corpo(n_mod, seg)
    lp = [dict(z=l['z'] * kz, L=l['L'] * kxy, W=l['W'] * kxy, R=l['R'] * kxy)
          for l in c.loops]
    assert abs(c.loops[7]['z'] - H) < 1e-9 and abs(c.loops[8]['z'] - H) < 1e-9, \
        'gera-3d.py mudou: aneis 7/8 nao estao mais no plano da borda'
    assert c.loops[8]['L'] < c.loops[7]['L'], 'anel 8 deveria ser a boca'
    # 13+ = rebaixo por baixo do fundo (a "elevacao" que fecha a litragem).
    # Com elevacao zero sobra so o anel do fundo raso, e a bolsa fica chata.
    pad = lp[13:] if len(lp) > 14 else []
    return lp[0:8], lp[8:13], H * kz, pad


# ---- solidos --------------------------------------------------------------
def solido_externo(ext, seg, pad=()):
    """Pote 'macico': tudo que fica do lado de fora da peca. Topo no fechamento."""
    m = Malha()
    P = [pts(l, seg) for l in ext]
    if pad:
        PT, PB = pts(pad[0], seg), pts(pad[1], seg)   # teto do rebaixo, base
        m.banda(PB, P[0])                             # anel do pe, face para baixo
        m.banda(PB, PT, flip=True)                    # parede do rebaixo, normal para dentro
        m.tampo(PT, False)                            # teto do rebaixo
    else:
        m.tampo(P[0], False)
    for a in range(len(P) - 1):
        m.banda(P[a], P[a + 1])
    m.tampo(P[-1], True)
    return m


def solido_interno(itn, seg):
    """Vazio interno da peca = superficie formadora do macho."""
    m = Malha()
    P = [pts(l, seg) for l in itn]           # [0] = boca no fechamento, [-1] = fundo
    m.tampo(P[0], True)
    for a in range(len(P) - 1):
        m.banda(P[a + 1], P[a])              # a ordem e de baixo para cima
    m.tampo(P[-1], False)
    return m


def postico_cavidade(ext, seg, pad=()):
    """Bloco com a bolsa. Plano de fechamento no topo; gate entra pelo fundo."""
    P = [pts(l, seg) for l in ext]
    flange = P[-1]                            # anel do labio, no fechamento
    zc = flange[0][2]
    Lb = max(p[0] for p in flange) * 2 + 2 * ACO_LATERAL
    Wb = max(p[1] for p in flange) * 2 + 2 * ACO_LATERAL
    zb = -ACO_FUNDO
    topo, base = ret(Lb, Wb, zc, seg), ret(Lb, Wb, zb, seg)

    m = Malha()
    m.banda(base, topo)                       # lateral do bloco
    m.tampo(base, False)                      # fundo do bloco
    m.banda(topo, flange)                     # face de fechamento (anel plano)
    for a in range(len(P) - 1, 0, -1):        # parede da bolsa, normal para dentro
        m.banda(P[a - 1], P[a], flip=True)
    if pad:                                   # macho postico que faz o rebaixo do fundo
        PT, PB = pts(pad[0], seg), pts(pad[1], seg)
        m.banda(P[0], PB)                     # piso da bolsa, em volta do ressalto
        m.banda(PB, PT)                       # parede do ressalto
        m.tampo(PT, True)                     # topo do ressalto
    else:
        m.tampo(P[0], True)                   # piso raso: fundo chato
    return m, (Lb, Wb, zb, zc)


def postico_macho(itn, seg, H):
    """Macho: parte formadora + haste que atravessa a impulsora + flange."""
    m = solido_interno(itn, seg)
    boca = itn[0]
    P0 = pts(boca, seg)
    z1 = H + HASTE_EXTRA
    P1 = [(x, y, z1) for x, y, _ in P0]
    m.tris = [t for t in m.tris if not _e_tampo(t, H)]   # abre o topo da forma
    m.banda(P0, P1)
    Lf = boca['L'] + 2 * 25.0
    Wf = boca['W'] + 2 * 25.0
    F0, F1 = ret(Lf, Wf, z1, seg), ret(Lf, Wf, z1 + FLANGE_MACHO, seg)
    m.banda(P1, F0)                           # degrau da flange, face para baixo
    m.banda(F0, F1)
    m.tampo(F1, True)
    return m, (Lf, Wf, z1 + FLANGE_MACHO)


def bloco_solido(Lb, Wb, zb, zc, seg):
    """O bloco cheio, sem bolsa. So existe para a conferencia de volume."""
    m = Malha()
    A, B = ret(Lb, Wb, zb, seg), ret(Lb, Wb, zc, seg)
    m.banda(A, B); m.tampo(B, True); m.tampo(A, False)
    return m


def _e_tampo(t, z):
    return all(abs(p[2] - z) < 1e-9 for p in t)


def placa_impulsora(ext, itn, seg, Lb, Wb):
    """Placa com o rasgo da boca: a face de baixo empurra a aba da peca."""
    boca = itn[0]
    z0 = boca['z']
    z1 = z0 + IMPULSORA_T
    furo = dict(z=z0, L=boca['L'] + 2 * FOLGA_IMPULS, W=boca['W'] + 2 * FOLGA_IMPULS,
                R=boca['R'] + FOLGA_IMPULS)
    F0 = pts(furo, seg)
    F1 = [(x, y, z1) for x, y, _ in F0]
    B0, B1 = ret(Lb, Wb, z0, seg), ret(Lb, Wb, z1, seg)
    m = Malha()
    m.banda(B0, B1)                           # lateral
    m.banda(B0, F0, flip=True)                # face de baixo (empurra a aba)
    m.banda(B1, F1)                           # face de cima
    m.banda(F0, F1, flip=True)                # parede do rasgo
    return m


def circuitos(ext, itn, seg, caixa):
    """Circuitos de agua: quadro em volta da bolsa + bubblers no macho.

    Devolve (malha, lista de descricao). Sao corpos separados de proposito: no
    conceito eles existem para ser vistos e conferidos, nao para ser furados.
    """
    Lb, Wb, zb, zc = caixa
    m, desc = Malha(), []
    flange = ext[-1]
    z = zb + CANAL_PASSO / 2
    nivel = 1
    while z < zc - 12.0:
        # meia-largura da peca naquela altura, para saber onde o furo passa
        l = min(ext, key=lambda r: abs(r['z'] - z))
        xf = l['L'] / 2 + CANAL_DIST
        yf = l['W'] / 2 + CANAL_DIST
        if xf > Lb / 2 - 8 or yf > Wb / 2 - 8:
            xf, yf = Lb / 2 - 10, Wb / 2 - 10
        m.soma(cilindro((-Lb / 2 - 5, yf, z), (Lb / 2 + 5, yf, z), CANAL_D))
        m.soma(cilindro((-Lb / 2 - 5, -yf, z), (Lb / 2 + 5, -yf, z), CANAL_D))
        m.soma(cilindro((xf, -Wb / 2 - 5, z), (xf, Wb / 2 + 5, z), CANAL_D))
        m.soma(cilindro((-xf, -Wb / 2 - 5, z), (-xf, Wb / 2 + 5, z), CANAL_D))
        desc.append(dict(tipo='cavidade', nivel=nivel, z=round(z, 1),
                         x=round(xf, 1), y=round(yf, 1)))
        z += CANAL_PASSO
        nivel += 1
    # macho: bubblers subindo pelo nucleo
    fundo = itn[-1]
    zt = itn[0]['z'] + HASTE_EXTRA
    for sx in (-1, 1):
        for sy in (-1, 1):
            x = sx * fundo['L'] / 4
            y = sy * fundo['W'] / 4
            m.soma(cilindro((x, y, fundo['z'] + 12.0), (x, y, zt), 12.0))
            desc.append(dict(tipo='macho (bubbler)', nivel=0, z=round(fundo['z'] + 12, 1),
                             x=round(x, 1), y=round(y, 1)))
    return m, desc


# ---- calculos -------------------------------------------------------------
def calculos(n_mod, seg, kxy, kz, ncav, ext, itn, H, caixa, macho_box, circ):
    c, H0 = G.corpo(n_mod, seg)
    vol_peca = G.volume_assinado(c.tris)                 # mm3, peca no nominal
    peso = vol_peca * RHO_PP
    aba = c.loops[7]
    area = (aba['L'] * aba['W'] - (4 - math.pi) * aba['R'] ** 2) / 100.0   # cm2
    tf_cav = area * P_CAV * K_SEG / 1000.0
    tf_tot = tf_cav * ncav * 1.05                        # +5% de canais
    Lb, Wb, zb, zc = caixa

    # porta-molde para ncav posticos, escolhendo a orientacao mais compacta
    def arranjo(dupla_em_x):
        if dupla_em_x:
            L = ncav * Lb + (ncav - 1) * ACO_ENTRE_CAV + 2 * ACO_BORDA
            W = Wb + 2 * ACO_BORDA
        else:
            L = Lb + 2 * ACO_BORDA
            W = ncav * Wb + (ncav - 1) * ACO_ENTRE_CAV + 2 * ACO_BORDA
        return L, W
    L1, W1 = arranjo(True)
    L2, W2 = arranjo(False)
    Lm, Wm = (L1, W1) if max(L1, W1) <= max(L2, W2) else (L2, W2)

    h_insert = zc - zb
    curso_extr = H + 25.0
    placas = []
    for nome, esp in PLACAS:
        if nome == 'Placa porta-cavidade':
            esp = h_insert + 20.0
        elif nome.startswith('Calcos'):
            esp = curso_extr + 30.0
        placas.append((nome, esp))
    alt_molde = sum(e for _, e in placas)
    abertura = H + curso_extr + QUEDA_PECA

    # agua: velocidade para Re alvo, em furo de CANAL_D
    re_alvo, mu, rho = 6000.0, 1.0e-3, 1000.0
    v = re_alvo * mu / (rho * CANAL_D / 1000.0)                    # m/s
    q = v * math.pi * (CANAL_D / 2000.0) ** 2 * 60000.0            # L/min

    ciclo = CICLO[n_mod]
    return dict(
        peso=peso, vol_peca=vol_peca, area=area, tf_cav=tf_cav, tf_tot=tf_tot,
        inj_cm3=peso * ncav / RHO_PP / 1000.0, Lb=Lb, Wb=Wb, h_insert=h_insert,
        Lm=Lm, Wm=Wm, placas=placas, alt_molde=alt_molde, curso_extr=curso_extr,
        abertura=abertura, v_agua=v, q_agua=q, n_circ=len([d for d in circ if d['nivel']]),
        ciclo=ciclo, pch=3600.0 / ciclo * ncav, H=H, H0=H0,
        kg_h=peso * ncav * 3600.0 / ciclo / 1000.0,
        macho_alt=macho_box[2] - itn[-1]['z'],
        lt=(math.hypot(ext[-1]['L'] / 2, ext[-1]['W'] / 2) + H) / (G.WALL[n_mod] * kxy),
    )


# ---- desenho de corte -----------------------------------------------------
def svg_corte(cam, n_mod, ext, itn, caixa, macho_box, circ, cal, ncav, contr, pad=()):
    Lb, Wb, zb, zc = caixa
    esc = 1.6 if n_mod <= 2 else 1.0
    marg = 70
    zt = macho_box[2]
    Wsvg = Lb * esc + 2 * marg + 210
    Hsvg = (zt - zb) * esc + 2 * marg
    cx, cy = marg + Lb * esc / 2, Hsvg - marg

    def X(x): return cx + x * esc
    def Z(z): return cy - (z - zb) * esc

    def perfil(aneis, lado=1):
        return ' '.join(f'{X(lado * a["L"] / 2):.1f},{Z(a["z"]):.1f}' for a in aneis)

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wsvg:.0f}" height="{Hsvg:.0f}" '
         f'viewBox="0 0 {Wsvg:.0f} {Hsvg:.0f}" font-family="Helvetica,Arial" font-size="11">',
         '<rect width="100%" height="100%" fill="#fbfbf9"/>']
    # postico de cavidade (com a bolsa aberta no topo)
    for lado in (1, -1):
        caminho = [(lado * Lb / 2, zb), (lado * Lb / 2, zc)]
        caminho += [(lado * a['L'] / 2, a['z']) for a in reversed(ext)]
        if pad:
            caminho += [(lado * pad[1]['L'] / 2, pad[1]['z']),
                        (lado * pad[0]['L'] / 2, pad[0]['z']), (0.0, pad[0]['z'])]
        else:
            caminho += [(0.0, ext[0]['z'])]
        caminho += [(0.0, zb)]
        d = ' L '.join(f'{X(x):.1f},{Z(z):.1f}' for x, z in caminho)
        s.append(f'<path d="M {d} Z" fill="#c8d2dc" stroke="#44515e" stroke-width="1"/>')
    # peca
    for lado in (1, -1):
        s.append(f'<polygon points="{perfil(ext, lado)} {perfil(list(reversed(itn)), lado)}" '
                 f'fill="#e8a33d" stroke="#8a5a10" stroke-width="0.8"/>')
    # macho
    boca = itn[0]
    Lf, Wf, ztopo = macho_box
    for lado in (1, -1):
        s.append(f'<polygon points="{perfil(itn, lado)} '
                 f'{X(lado*boca["L"]/2):.1f},{Z(boca["z"]+HASTE_EXTRA):.1f} '
                 f'{X(lado*Lf/2):.1f},{Z(boca["z"]+HASTE_EXTRA):.1f} '
                 f'{X(lado*Lf/2):.1f},{Z(ztopo):.1f} {X(0):.1f},{Z(ztopo):.1f} '
                 f'{X(0):.1f},{Z(itn[-1]["z"]):.1f}" '
                 f'fill="#9aa7b4" stroke="#33404d" stroke-width="1"/>')
    # placa impulsora
    for lado in (1, -1):
        x0, x1 = X(lado * boca['L'] / 2), X(lado * Lb / 2)
        s.append(f'<rect x="{min(x0,x1):.1f}" y="{Z(zc+IMPULSORA_T):.1f}" '
                 f'width="{abs(x1-x0):.1f}" height="{IMPULSORA_T*esc:.1f}" '
                 f'fill="#7d8b99" stroke="#33404d" stroke-width="1"/>')
    # refrigeracao
    for d in circ:
        if d['nivel']:
            for lado in (1, -1):
                s.append(f'<circle cx="{X(lado*d["x"]):.1f}" cy="{Z(d["z"]):.1f}" '
                         f'r="{CANAL_D/2*esc:.1f}" fill="#7fb8e0" stroke="#2c6a9b"/>')
        else:
            s.append(f'<rect x="{X(d["x"])-6*esc:.1f}" y="{Z(macho_box[2]):.1f}" '
                     f'width="{12*esc:.1f}" height="{(macho_box[2]-d["z"])*esc:.1f}" '
                     f'fill="#7fb8e0" fill-opacity="0.55" stroke="#2c6a9b" stroke-dasharray="3 2"/>')
    # gate
    s.append(f'<path d="M {X(0):.1f},{Z(zb):.1f} L {X(0):.1f},{Z(ext[0]["z"]):.1f}" '
             f'stroke="#b0303a" stroke-width="3"/>')
    s.append(f'<text x="{X(0)+6:.1f}" y="{Z(zb)-4:.1f}" fill="#b0303a">bico quente valvulado</text>')
    # linha de fechamento
    s.append(f'<path d="M {marg/2:.1f},{Z(zc):.1f} L {Wsvg-190:.1f},{Z(zc):.1f}" '
             f'stroke="#b0303a" stroke-dasharray="7 4"/>')
    s.append(f'<text x="{marg/2:.1f}" y="{Z(zc)-5:.1f}" fill="#b0303a">plano de fechamento</text>')
    # legenda
    tx = Wsvg - 200
    linhas = [f'POTE {TAMANHOS[n_mod]} ml — corte do molde',
              f'contracao aplicada: {contr:.2f}%',
              f'postico {Lb:.0f} x {Wb:.0f} x {zc-zb:.0f} mm',
              f'porta-molde {cal["Lm"]:.0f} x {cal["Wm"]:.0f} mm, {ncav} cav',
              f'altura de molde {cal["alt_molde"]:.0f} mm',
              f'abertura minima {cal["abertura"]:.0f} mm',
              f'fechamento {cal["tf_tot"]:.0f} tf',
              f'{cal["n_circ"]} circuitos + 4 bubblers no macho',
              '', 'laranja = peca   azul = aco   ',
              'cinza claro = cavidade  escuro = macho']
    for i, t in enumerate(linhas):
        s.append(f'<text x="{tx:.0f}" y="{marg + 18*i:.0f}" fill="#2b2b2b">{t}</text>')
    s.append('</svg>')
    open(cam, 'w').write('\n'.join(s))


# ---- ficha ----------------------------------------------------------------
def ficha(cam, n_mod, cal, ncav, contr, caixa, circ, seg):
    Lb, Wb, zb, zc = caixa
    tam = TAMANHOS[n_mod]
    placas = '\n'.join(f'| {n} | {e:.0f} |' for n, e in cal['placas'])
    circ_tab = '\n'.join(
        f'| {d["tipo"]} {d["nivel"] or ""} | z = {d["z"]:.0f} | x = ±{abs(d["x"]):.0f} | y = ±{abs(d["y"]):.0f} |'
        for d in circ)
    txt = f"""# Ficha de molde — pote {tam} ml (conceito)

Gerado por `gera-molde.py` a partir do parametrico da peca. **Conceito, nao
projeto executivo** — ver o cabecalho do gerador e a secao "O que falta".

| | |
|---|---|
| Peca | corpo {tam} ml, PP, parede {G.WALL[n_mod]:.2f} mm, altura {cal['H0']:.1f} mm |
| Peso da peca (malha) | {cal['peso']:.1f} g |
| Contracao aplicada | **{contr:.2f}% linear** (XY e Z) |
| Cavidades | {ncav} |
| Tipo | duas placas, camara quente valvulada, extracao por placa impulsora |
| Plano de fechamento | plano da aba da borda; peca fica **de boca para baixo**, fundo no lado da injecao |

## 1. Fechamento e injecao

| | |
|---|---|
| Area projetada por cavidade | {cal['area']:.1f} cm² |
| Pressao media adotada | {P_CAV:.0f} kgf/cm² (parede fina, PP) |
| Fator de seguranca | {K_SEG:.2f} |
| **Fechamento por cavidade** | **{cal['tf_cav']:.0f} tf** |
| **Fechamento total ({ncav} cav + canais)** | **{cal['tf_tot']:.0f} tf** |
| Volume de injecao por ciclo | {cal['inj_cm3']:.0f} cm³ |
| Razao de fluxo L/t estimada | {cal['lt']:.0f} |

## 2. Posticos

| | |
|---|---|
| Postico de cavidade | {Lb:.0f} × {Wb:.0f} × {cal['h_insert']:.0f} mm |
| Aco lateral em volta da bolsa | {ACO_LATERAL:.0f} mm |
| Aco sob o fundo da bolsa | {ACO_FUNDO:.0f} mm (passagem do bico) |
| Macho, altura total | {cal['macho_alt']:.0f} mm (forma + haste + flange) |
| Placa impulsora | {IMPULSORA_T:.0f} mm, folga de {FOLGA_IMPULS:.2f} mm por lado sobre o macho |

## 3. Porta-molde e curso

| Placa | Espessura (mm) |
|---|---|
{placas}

| | |
|---|---|
| Porta-molde | {cal['Lm']:.0f} × {cal['Wm']:.0f} mm |
| **Altura de molde fechado** | **{cal['alt_molde']:.0f} mm** |
| Curso de extracao | {cal['curso_extr']:.0f} mm |
| **Abertura minima da maquina** | **{cal['abertura']:.0f} mm** |

> A abertura minima e a conta que reprova maquina em pote alto: altura da peca
> ({cal['H']:.0f}) + curso de extracao ({cal['curso_extr']:.0f}) + queda ({QUEDA_PECA:.0f}).
> Confrontar com `CURSOABERT`, `ALTMINMOLDE` e `ALTMAXMOLDE` da injetora — os
> campos que estao nulos em `AD_INJETORAFICHA`.

## 4. Refrigeracao

Furos de Ø{CANAL_D:.0f} mm a {CANAL_DIST:.0f} mm da superficie formadora ({CANAL_DIST/CANAL_D:.1f} × D),
passo vertical de {CANAL_PASSO:.0f} mm. Circuito de cavidade e de macho **separados**.

| Circuito | Altura | Posicao X | Posicao Y |
|---|---|---|---|
{circ_tab}

| | |
|---|---|
| Alvo de regime | Re = 6.000 (turbulento) |
| Velocidade necessaria | {cal['v_agua']:.2f} m/s |
| **Vazao por circuito** | **{cal['q_agua']:.1f} L/min** |
| ΔT admissivel no circuito | ≤ 3 °C |

## 5. Ciclo e capacidade

| | |
|---|---|
| Ciclo estimado | {cal['ciclo']:.0f} s |
| Pecas/hora ({ncav} cav) | {cal['pch']:.0f} |
| Consumo de resina | {cal['kg_h']:.1f} kg/h |

## 6. O que falta para virar projeto executivo

1. **Contracao por direcao e por tamanho** — aqui esta {contr:.2f}% linear e igual
   nos dois eixos. O correto sai do Moldflow, e a parede varia de 1,15 a 1,40 mm
   entre os quatro potes.
2. **Porta-molde normalizado real** (HASCO/DME/Meusburger) com codigo de catalogo,
   guias, colunas de apoio, retorno de extracao e refrigeracao das placas.
3. **Camara quente especificada** (marca, modelo, numero de bicos, controlador) e
   o rebaixo do vestigio no pe do pote.
4. **Respiros**: 0,02–0,03 mm na linha de fechamento e no ultimo ponto a encher.
5. **Detalhamento 2D com tolerancias**, cotas steel safe marcadas e stack-up.
6. **Aco e tratamento** por componente; a classe aqui e 101 (≥ 48 HRC).
7. **Moldflow** e o plano de try-out.
"""
    open(cam, 'w').write(txt)


# ---- main -----------------------------------------------------------------
def main():
    seg = 12
    contr = 1.5
    ncav = 2
    for flag, alvo in (('--seg', 'seg'), ('--contracao', 'contr'), ('--cav', 'ncav')):
        if flag in sys.argv:
            v = sys.argv[sys.argv.index(flag) + 1]
            if alvo == 'seg':   seg = int(v)
            if alvo == 'contr': contr = float(v)
            if alvo == 'ncav':  ncav = int(v)
    k = 1.0 + contr / 100.0

    os.makedirs(os.path.join(BASE, 'desenhos'), exist_ok=True)
    resumo, ruins = [], []
    for n in (1, 2, 3, 4):
        tam = TAMANHOS[n]
        out = os.path.join(BASE, 'stl', tam)
        os.makedirs(out, exist_ok=True)
        ext, itn, H, pad = aneis_do_pote(n, seg, k, k)

        cav, caixa = postico_cavidade(ext, seg, pad)
        mac, macho_box = postico_macho(itn, seg, H)
        imp = placa_impulsora(ext, itn, seg, caixa[0], caixa[1])
        ref, circ = circuitos(ext, itn, seg, caixa)

        for nome, m in (('cavidade', cav), ('macho', mac), ('placa-impulsora', imp)):
            if G.volume_assinado(m.tris) < 0:
                m.tris = [t[::-1] for t in m.tris]
            ok = G.normais_consistentes(m.tris) and G.volume_assinado(m.tris) > 0
            if not ok:
                ruins.append(f'{tam}/{nome}')
            G.grava_stl(os.path.join(out, nome + '.stl'), m.tris, f'{nome}-{tam}')
        G.grava_stl(os.path.join(out, 'refrigeracao.stl'), ref.tris, f'refrig-{tam}')

        cal = calculos(n, seg, k, k, ncav, ext, itn, H, caixa, macho_box, circ)
        svg_corte(os.path.join(BASE, 'desenhos', f'molde-{tam}.svg'),
                  n, ext, itn, caixa, macho_box, circ, cal, ncav, contr, pad)
        ficha(os.path.join(BASE, f'ficha-molde-{tam}.md'), n, cal, ncav, contr,
              caixa, circ, seg)

        # Conferencia que fecha o gerador: o vazio entre cavidade e macho tem
        # que ser exatamente a peca com a contracao aplicada. Se o rebaixo do
        # fundo, a boca ou a aba sairem errados, este numero acusa.
        bloco = bloco_solido(*caixa, seg)
        vazio = (G.volume_assinado(bloco.tris) - G.volume_assinado(cav.tris)
                 - G.volume_assinado(solido_interno(itn, seg).tris))
        cpeca, _ = G.corpo(n, seg)
        alvo = G.volume_assinado(cpeca.tris) * k ** 3
        erro = (vazio - alvo) / alvo * 100.0
        if abs(erro) > 0.5:
            ruins.append(f'{tam}/vazio fora por {erro:+.2f}%')

        vcav = G.volume_assinado(cav.tris) / 1000.0
        vmac = G.volume_assinado(mac.tris) / 1000.0
        resumo.append((tam, caixa, cal, vcav, vmac))
        print(f'pote {tam:>4} ml | postico {caixa[0]:5.0f} x {caixa[1]:5.0f} x '
              f'{cal["h_insert"]:5.0f} | aco cav {vcav/1000:6.2f} L | macho {vmac/1000:5.2f} L | '
              f'{cal["tf_tot"]:4.0f} tf | abertura {cal["abertura"]:4.0f} mm | '
              f'molde {cal["alt_molde"]:4.0f} mm | vazio {erro:+.2f}% da peca')

    print()
    print(f'{"":14}{"porta-molde":>16}{"fechamento":>13}{"maquina sugerida":>20}')
    for tam, caixa, cal, _, _ in resumo:
        maq = next((t for t in (120, 150, 160, 200, 250, 280, 300, 380, 600)
                    if cal['tf_tot'] <= 0.8 * t), None)
        print(f'pote {tam:>4} ml  {cal["Lm"]:6.0f} x {cal["Wm"]:<6.0f} '
              f'{cal["tf_tot"]:8.0f} tf   {maq or "?"} t por fechamento, MAS precisa de '
              f'{cal["alt_molde"] + cal["abertura"]:.0f} mm entre platos '
              f'({cal["alt_molde"]:.0f} de molde + {cal["abertura"]:.0f} de abertura)')

    if ruins:
        print('\nMALHA RUIM EM:', ', '.join(ruins))
        sys.exit(1)
    print('\nConferencias que o gerador faz sozinho:')
    print('  - malha fechada e normais consistentes nas 12 pecas de aco;')
    print('  - vazio entre cavidade e macho = peca x (1+contracao)^3, dentro de 0,5%')
    print('    (a sobra e a poligonal de 12 segmentos por canto, igual a da peca).')
    print('STL em moldes/stl/<tam>/ | cortes em moldes/desenhos/ | fichas em moldes/')


if __name__ == '__main__':
    main()
