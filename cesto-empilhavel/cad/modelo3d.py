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
LARG   = 215.0            # X - largura da boca
PROF   = 200.0            # Y - profundidade
ALT    = 130.0            # Z - altura
DRAFT  = 3.5              # graus por lado: saida de molde e folga de encaixe

# --- silhueta lateral, na proporcao do STL de referencia --------------------
CHANFRO   = 52.0          # 40% da altura, a 45 graus
FRENTE_H  = ALT - 2 * CHANFRO      # 26 mm - face frontal, na meia-altura
R_CANTO   = 20.0          # raio nas duas pontas dos chanfros (o pedido)
R_FRENTE  = 12.0          # raio nas duas quinas da face frontal

# --- paredes ----------------------------------------------------------------
T_PAREDE = 1.4
T_FUNDO  = 2.0
T_RIM    = 3.2            # parede engrossada na faixa do rim
H_RIM    = 10.0
H_PE     = 6.0

# --- vazado -----------------------------------------------------------------
PASSO   = 15.0
D_TOPO  = 14.0
D_BASE  = 6.0
Z_TOPO  = ALT - H_RIM - 9.0
BANDA   = 40.0            # faixa cega no pe da parede
FOLGA_S = 9.0             # folga entre furo e a silhueta

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
        (yf, CHANFRO),                   # face frontal
        (yf + CHANFRO, 0.0),             # chanfro do pe, 45 graus
    ]
    sk = make_face(Polyline(*pts, close=True))
    # pontas dos chanfros
    sk = fillet(sk.vertices().filter_by_position(Axis.X, yf + CHANFRO - 1,
                                                 yf + CHANFRO + 1), R_CANTO)
    # quinas da face frontal
    sk = fillet(sk.vertices().filter_by_position(Axis.X, yf - 1, yf + 1), R_FRENTE)
    return sk


def z_silhueta(y):
    """Cota do topo da silhueta em y -- usada para recortar o campo de furos."""
    yf = -PROF / 2
    if y >= yf + CHANFRO:
        return ALT
    return (ALT - CHANFRO) + (y - yf)      # a 45 graus


def filas():
    n = int((Z_TOPO - BANDA) // PASSO) + 1
    ds = np.linspace(D_TOPO, D_BASE, n)
    return [(Z_TOPO - i * PASSO, float(ds[i])) for i in range(n)]


def grade(extensao, passo):
    n = int(np.floor(extensao / passo))
    if n % 2 == 0:
        n -= 1
    return [(-(n - 1) * passo / 2) + i * passo for i in range(n)]


def cesto():
    # casca tronco-piramidal
    fora = extrude(RectangleRounded(BASE_X, BASE_Y, 14.0), ALT, taper=-DRAFT)
    p = fora - Pos(0, 0, T_FUNDO) * extrude(
        RectangleRounded(BASE_X - 2 * T_PAREDE, BASE_Y - 2 * T_PAREDE, 12.0),
        ALT, taper=-DRAFT)

    # faixa do rim: parede engrossada no alto
    cheio = fora - Pos(0, 0, T_FUNDO) * extrude(
        RectangleRounded(BASE_X - 2 * T_RIM, BASE_Y - 2 * T_RIM, 11.0),
        ALT, taper=-DRAFT)
    p += cheio & Pos(0, 0, ALT - H_RIM) * extrude(
        RectangleRounded(LARG + 40, PROF + 40, 0.1), H_RIM + 10)

    # recorta pela silhueta: e isso que da a forma do STL de referencia
    p = p & extrude(Plane.YZ * silhueta(), LARG / 2 + 30, both=True)

    # --- vazado ---
    furos, n = [], 0
    for z, d in filas():
        mx, my = secao(z, T_RIM)
        for x in grade(mx - d - 30, PASSO):                  # parede do fundo
            furos.append(Pos(x, 0, z) * Rot(90, 0, 0) * Cylinder(d / 2, PROF + 60))
            n += 1
        for y in grade(my - d - 30, PASSO):                  # laterais
            if z + d / 2 + FOLGA_S > z_silhueta(y):
                continue
            furos.append(Pos(0, y, z) * Rot(0, 90, 0) * Cylinder(d / 2, LARG + 60))
            n += 2
    p -= furos

    # --- pes de canto: alcancam a medida da boca e assentam no rim de baixo ---
    y_pe_f = -PROF / 2 + CHANFRO + 16
    for sx in (-1, 1):
        for y_pe in (y_pe_f, PROF / 2 - 16):
            c = Pos(sx * (LARG / 2 - 16), y_pe, H_PE / 2)
            p += c * Box(32, 32, H_PE)
            p -= c * Pos(0, 0, -1.6) * Box(28, 28, H_PE)
    return p, n


def capacidade():
    cav = Pos(0, 0, T_FUNDO) * extrude(
        RectangleRounded(BASE_X - 2 * T_PAREDE, BASE_Y - 2 * T_PAREDE, 12.0),
        ALT - T_FUNDO, taper=-DRAFT)
    cav = cav & extrude(Plane.YZ * silhueta(), LARG / 2 + 30, both=True)
    return cav.volume / 1e6


def main():
    dest = os.path.dirname(os.path.abspath(__file__))
    p, n = cesto()
    bb = p.bounding_box()
    print("CESTO ORGANIZAVEL EMPILHAVEL - forma adaptada do STL de referencia")
    print(f"Boca {LARG:.0f} x {PROF:.0f} mm | base {BASE_X:.1f} x {BASE_Y:.1f} mm "
          f"| altura {ALT:.0f} mm | saida {DRAFT:.1f} deg/lado")
    print(f"Silhueta: chanfros de {CHANFRO:.0f} mm a 45 deg, face frontal de "
          f"{FRENTE_H:.0f} mm | pontas R{R_CANTO:.0f} e R{R_FRENTE:.0f}")
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
