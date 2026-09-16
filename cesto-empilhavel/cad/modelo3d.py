#!/usr/bin/env python3
"""
Modelo 3D parametrico do cesto mini organizador empilhavel e encaixavel.

PECA UNICA injetada -- sem dobradica, sem painel, sem montagem. Referencia:
cesto mini organizador empilhavel de 21,5 x 20 x 13 cm.

GEOMETRIA
  Caixa tronco-piramidal com saida de DRAFT por lado (e a saida que permite o
  encaixe: a base e menor que a boca, entao uma peca afunda na outra). A parede
  frontal e rebaixada e a aresta superior das laterais desce do fundo para a
  frente numa curva -- e essa curva que deixa a peca entrar inclinada na de
  baixo para encaixar, e que da acesso frontal quando empilhada.

DOIS MODOS
  Empilhado: a peca de cima assenta nas quatro ORELHAS externas logo abaixo do
  rim; passo = altura da peca, e a frente fica acessivel sem desempilhar.
  Encaixado: inclina para a frente, os pes passam ao lado das orelhas e o corpo
  afunda -- passo de encaixe muito menor.

VAZADO
  Furos redondos em bandas horizontais de Z fixo, com o diametro caindo de cima
  para baixo (D_TOPO -> D_BASE). Nas laterais as filas sao recortadas pela curva
  da aresta, entao o campo de furos acompanha o rebaixo. Fundo SOLIDO e faixa
  cega no pe da peca. A frente rebaixada e solida, com ripado vertical externo.

Uso:  python3 modelo3d.py
"""
import os
import numpy as np
from build123d import (Align, Box, Cylinder, Plane, Polyline, Pos, Rot,
                       RectangleRounded, export_step, export_stl, extrude,
                       make_face, Line)

RHO = 0.905e-3            # g/mm3 - PP copolimero

# --- envelope (cotas da referencia) -----------------------------------------
LARG      = 215.0         # X - largura frontal
PROF      = 200.0         # Y - profundidade
ALT       = 130.0         # Z - altura no fundo
ALT_FRENTE = 45.0         # altura da parede frontal rebaixada
RAIO      = 14.0          # raio de canto em planta
DRAFT     = 4.0           # graus por lado - saida de molde E folga de encaixe

T_PAREDE  = 1.4
T_FUNDO   = 2.0
T_RIM     = 3.2           # espessura da parede na faixa do rim
H_RIM     = 10.0          # altura da faixa engrossada do rim
H_PE      = 6.0           # pe
EXPO      = 1.7           # expoente da curva do rebaixo (1 = reta, >1 = concava)

# --- rebordo da base: o apoio do empilhamento -------------------------------
# A peca e tronco-piramidal (boca maior que a base), entao uma afunda na outra.
# O rebordo da base e alargado ate a medida da boca: nivelada, a peca de cima
# assenta nele; inclinada ~14 graus, o rebordo passa livre pela frente
# rebaixada e a peca afunda -- que e o encaixe das fotos da referencia.
H_FLANGE = 8.0
T_FLANGE = 2.5

# --- pega lateral (a aba que aparece na foto, para puxar a peca empilhada) ---
PG_L, PG_H, PG_P = 46.0, 9.0, 11.0

# --- vazado -----------------------------------------------------------------
PASSO   = 15.0
D_TOPO  = 14.0
D_BASE  = 6.0
Z_TOPO  = ALT - H_RIM - 8.0           # centro da 1a fila
BANDA   = 30.0                        # faixa cega no pe
FOLGA_C = 7.0                         # folga entre furo e a curva do rebaixo


TAN = np.tan(np.radians(DRAFT))
BASE_X = LARG - 2 * ALT * TAN          # medida da base (menor que a boca)
BASE_Y = PROF - 2 * ALT * TAN


def secao(z, folga=0.0):
    """Planta externa na cota z (boca = LARG x PROF no topo)."""
    return (BASE_X + 2 * z * TAN - 2 * folga,
            BASE_Y + 2 * z * TAN - 2 * folga)


def z_aresta(y):
    """Cota da aresta superior da lateral, no ponto y (curva do rebaixo)."""
    t = (y + PROF / 2) / PROF                      # 0 na frente, 1 no fundo
    return ALT_FRENTE + (ALT - ALT_FRENTE) * t ** EXPO


def filas():
    """(z, diametro) de cada banda horizontal, de cima para baixo."""
    n = int((Z_TOPO - BANDA) // PASSO) + 1
    ds = np.linspace(D_TOPO, D_BASE, n)
    return [(Z_TOPO - i * PASSO, float(ds[i])) for i in range(n)]


def grade(extensao, passo):
    n = int(np.floor(extensao / passo))
    if n % 2 == 0:
        n -= 1
    return [(-(n - 1) * passo / 2) + i * passo for i in range(n)]


def corte_rebaixo():
    """Solido acima da curva do rebaixo, atravessando toda a largura."""
    ys = np.linspace(-PROF / 2 - 2, PROF / 2 + 2, 40)
    pts = [(float(y), float(z_aresta(min(max(y, -PROF / 2), PROF / 2))))
           for y in ys]
    pts += [(PROF / 2 + 2, ALT + 40), (-PROF / 2 - 2, ALT + 40)]
    perfil = make_face(Polyline(*[(p[0], p[1]) for p in pts], close=True))
    s = extrude(Plane.YZ * perfil, LARG / 2 + 30, both=True)
    return s


def cesto():
    fora = extrude(RectangleRounded(BASE_X, BASE_Y, RAIO), ALT, taper=-DRAFT)
    p = fora - Pos(0, 0, T_FUNDO) * extrude(
        RectangleRounded(BASE_X - 2 * T_PAREDE, BASE_Y - 2 * T_PAREDE,
                         RAIO - T_PAREDE), ALT, taper=-DRAFT)

    # rebordo da base, alargado ate a medida da boca
    fl = extrude(RectangleRounded(LARG, PROF, RAIO), H_FLANGE)
    p += fl - Pos(0, 0, -1) * extrude(
        RectangleRounded(LARG - 2 * T_FLANGE, PROF - 2 * T_FLANGE,
                         RAIO - T_FLANGE), H_FLANGE + 2 - T_FUNDO)

    # faixa do rim: parede engrossada, acompanhando a curva do rebaixo
    cheio_rim = fora - Pos(0, 0, T_FUNDO) * extrude(
        RectangleRounded(BASE_X - 2 * T_RIM, BASE_Y - 2 * T_RIM, RAIO - T_RIM),
        ALT, taper=-DRAFT)
    corte = corte_rebaixo()
    banda_rim = Pos(0, 0, -H_RIM) * corte - corte
    p += cheio_rim & banda_rim

    # rebaixo frontal
    p -= corte

    # --- vazado ---
    furos, n = [], 0
    for z, d in filas():
        # parede do fundo (normal em Y)
        meia_larg = secao(z, T_RIM)[0] / 2
        for x in grade(2 * meia_larg - d - 2 * RAIO - 8, PASSO):
            furos.append(Pos(x, 0, z) * Rot(90, 0, 0) * Cylinder(d / 2, PROF + 40))
            n += 1
        # paredes laterais (normal em X), recortadas pela curva
        meia_prof = secao(z, T_RIM)[1] / 2
        for y in grade(2 * meia_prof - d - 2 * RAIO - 8, PASSO):
            if z + d / 2 + FOLGA_C > z_aresta(y):
                continue
            furos.append(Pos(0, y, z) * Rot(0, 90, 0) * Cylinder(d / 2, LARG + 40))
            n += 2
    p -= furos

    # --- pega lateral: a aba da foto, para puxar a peca empilhada ---
    for sx in (-1, 1):
        y_pg = -PROF / 2 + 52
        z_pg = z_aresta(y_pg) - PG_H / 2 - 3
        x_pg = secao(z_pg)[0] / 2
        p += Pos(sx * (x_pg + PG_P / 2 - 1), y_pg, z_pg) * \
            Box(PG_P + 2, PG_L, PG_H)

    # --- pes sob o rebordo, ocos (aro de 2 mm) ---
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = Pos(sx * (LARG / 2 - 20), sy * (PROF / 2 - 20), -H_PE / 2)
            p += c * Box(32, 32, H_PE + 1)
            p -= c * Pos(0, 0, -1.5) * Box(28, 28, H_PE + 1)

    # --- ripado vertical na frente rebaixada ---
    yf = secao(ALT_FRENTE / 2)[1] / 2
    for x in grade(secao(ALT_FRENTE / 2)[0] - 70, 9.0):
        p += Pos(x, -yf - 1.0, ALT_FRENTE / 2 + 1) * \
            Box(3.2, 2.6, ALT_FRENTE - H_FLANGE - 6)

    p.label = "cesto"
    return p, n


def capacidade():
    """Volume interno ate a borda do rebaixo frontal, em litros."""
    planta = RectangleRounded(BASE_X - 2 * T_PAREDE, BASE_Y - 2 * T_PAREDE,
                              RAIO - T_PAREDE)
    cav = Pos(0, 0, T_FUNDO) * extrude(planta, ALT - T_FUNDO, taper=-DRAFT)
    nominal = cav.volume / 1e6
    util = (cav - corte_rebaixo()).volume / 1e6
    return nominal, util


def main():
    dest = os.path.dirname(os.path.abspath(__file__))
    p, n = cesto()
    nominal, util = capacidade()
    peso = p.volume * RHO
    bb = p.bounding_box()

    print(f"CESTO MINI ORGANIZADOR EMPILHAVEL - peca unica")
    print(f"Boca (rim)    {LARG:.1f} x {PROF:.1f} mm | base {BASE_X:.1f} x {BASE_Y:.1f} mm")
    print(f"Envelope      {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm "
          f"(inclui as pegas laterais)")
    print(f"Altura frente {ALT_FRENTE:.0f} mm | saida {DRAFT:.0f} deg/lado | "
          f"parede {T_PAREDE:.1f} mm | fundo {T_FUNDO:.1f} mm")
    print(f"Capacidade    {nominal:.2f} L nominal | {util:.2f} L ate a borda frontal")
    print(f"Peso          {peso:.1f} g   (volume {p.volume/1000:.1f} cm3)")
    fl = filas()
    print(f"Vazado        {len(fl)} bandas, D "
          f"{' / '.join(f'{d:.1f}' for _, d in fl)} mm | {n} furos | "
          f"faixa cega {BANDA:.0f} mm")
    proj = LARG * PROF / 100.0
    print(f"Area projetada {proj:.0f} cm2")

    export_step(p, os.path.join(dest, "cesto.step"))
    export_stl(p, os.path.join(dest, "cesto.stl"))

    import trimesh
    import render
    m = trimesh.load(os.path.join(dest, "cesto.stl"))
    cor = (0.93, 0.44, 0.13)

    def cena_pilha(k, dz):
        out = []
        for i in range(k):
            t = m.copy()
            t.apply_translation([0, 0, i * dz])
            out.append((t, tuple(c * (1 - 0.05 * (i % 2)) for c in cor)))
        return out

    def cena_encaixe(k, dz, dy):
        out = []
        for i in range(k):
            t = m.copy()
            t.apply_transform(trimesh.transformations.rotation_matrix(
                np.radians(-14), [1, 0, 0]))
            t.apply_translation([0, i * dy, i * dz])
            out.append((t, tuple(c * (1 - 0.05 * (i % 2)) for c in cor)))
        return out

    vistas = [("01-cesto.png", [(m, cor)], (-1.0, -1.35, -0.62)),
              ("02-frente.png", [(m, cor)], (0.05, -1.0, -0.30)),
              ("03-empilhado.png", cena_pilha(3, ALT), (-1.0, -1.3, -0.5)),
              ("04-encaixado.png", cena_encaixe(8, 26, 7), (-1.0, -1.2, -0.42))]
    for arq, cena, d in vistas:
        render.salvar(render.render(cena, direcao=d, largura=1500),
                      os.path.join(dest, arq))
        print("gerado", arq)


if __name__ == "__main__":
    main()
