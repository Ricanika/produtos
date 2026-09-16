#!/usr/bin/env python3
"""
Modelo 3D parametrico do cesto organizador dobravel empilhavel (linha P/M/G).

ARQUITETURA
  Bandeja de fundo, comum aos tres tamanhos: pe de 5 mm que afunda no berco da
  peca de baixo, chapa SOLIDA, saia de 30 mm com raio de canto R15, berco de
  empilhamento no topo da saia e orelhas de dobradica na face interna.
  Quatro paineis planos articulados no topo da saia: dois laterais iguais, um
  traseiro e um frontal rebaixado. Os paineis sao EMBUTIDOS (mais estreitos que
  a boca da bandeja), entao dobram para DENTRO dela -- e por isso os tres
  tamanhos fecham na mesma altura dobrada.

VAZADO
  Furos redondos em reticulado de passo fixo. O diametro cai D_QUEDA por fila,
  de D_TOPO ate o piso D_BASE. Como a queda e por fila e nao proporcional a
  altura, as filas de cima sao identicas nos tres tamanhos: empilhados, os
  furos alinham e o gradiente le como um degrade continuo na pilha inteira.
  A faixa do pe do painel e CEGA -- e onde o momento da dobradica e a carga de
  empilhamento se concentram, e furo ali seria concentrador de tensao no pior
  lugar possivel. O frontal e cego, so com o recorte de pega, como a referencia.

O peso sai do volume exato do solido.
Saidas: STEP (ferramentaria), STL (visualizacao/impressao) e PNG das vistas.

Uso:  python3 modelo3d.py [P|M|G]     (default P)
"""
import os
import sys
import numpy as np
from build123d import (Align, Box, Compound, Cylinder, Pos, RectangleRounded,
                       Rot, export_step, export_stl, extrude)

RHO = 0.905e-3            # g/mm3 - PP copolimero CP 141 (CODPROD 994)

# --- geometria comum aos tres tamanhos --------------------------------------
EXT_C, EXT_L = 345.0, 285.0     # footprint externo
RAIO         = 15.0             # raio de canto externo
H_PE         = 5.0              # pe (= profundidade do berco de empilhamento)
H_SAIA       = 30.0             # saia acima do pe
T_CHAPA      = 2.2
T_SAIA       = 2.5
T_LIP        = 1.2              # lip externo que sobra no berco
MODULO       = 58.0
TAMANHOS     = {"P": 2, "M": 3, "G": 4}

Z_RIM  = H_PE + H_SAIA          # topo da saia
Z_ART  = Z_RIM - 4.0            # eixo das dobradicas

# --- paineis ----------------------------------------------------------------
T_MOLDURA  = 3.0
T_CAMPO    = 1.8
L_MOLDURA  = 12.0
FOLGA_EMB  = 1.5                # folga do painel embutido
LARG_LONGO = EXT_C - 2 * T_SAIA - 2 * FOLGA_EMB     # traseiro e frontal
LARG_CURTO = EXT_L - 2 * T_SAIA - 2 * FOLGA_EMB     # laterais
FRAC_FRONTAL = 0.55             # altura do frontal / altura do painel

# --- padrao de furos --------------------------------------------------------
PASSO      = 16.0
D_TOPO     = 16.0
D_BASE     = 7.0
BORDA_TOPO = 16.0       # web entre a moldura e a 1a fila
BANDA_CEGA = 16.0       # faixa cega no pe do painel

# --- dobradica --------------------------------------------------------------
R_PINO, L_PINO, R_BERCO = 3.0, 16.0, 3.4


def cavidade(h_ext, h_front):
    """Volume interno: nominal (ate a borda) e util (ate a borda do frontal)."""
    off_x = EXT_C / 2 - T_SAIA - FOLGA_EMB - T_MOLDURA / 2
    off_y = EXT_L / 2 - T_SAIA - FOLGA_EMB - T_MOLDURA / 2
    cx = 2 * (off_x - T_MOLDURA / 2)          # entre faces internas dos laterais
    cy = 2 * (off_y - T_MOLDURA / 2)          # entre faces internas de tras/frente
    z0 = H_PE + T_CHAPA
    nominal = cx * cy * (h_ext - z0) / 1e6
    util = cx * cy * ((Z_ART - 4.0 + h_front) - z0) / 1e6
    return cx, cy, nominal, util


def alt_painel(h_ext):
    return h_ext - (Z_ART - 4.0)


def filas(alt):
    y0 = BORDA_TOPO + PASSO / 2
    n = max(int(np.floor((alt - y0 - BANDA_CEGA) / PASSO)) + 1, 1)
    if n == 1:
        return [(y0, D_TOPO)]
    return [(y0 + i * PASSO, float(d))
            for i, d in enumerate(np.linspace(D_TOPO, D_BASE, n))]


def colunas(larg):
    n = int(np.floor((larg - 2 * L_MOLDURA) / PASSO))
    if n % 2 == 0:
        n -= 1                                   # impar: uma coluna no eixo
    return [(-(n - 1) * PASSO / 2) + i * PASSO for i in range(n)]


def pos_art(larg):
    n = 3 if larg > 300 else 2
    passo = (larg - 70) / max(n - 1, 1)
    return [(i - (n - 1) / 2) * passo for i in range(n)]


def painel(larg, alt, cego=False, pega=False):
    """Painel plano no plano XY, espessura em +Z, origem no centro da face."""
    p = extrude(RectangleRounded(larg, alt, 8.0), T_MOLDURA)
    p -= Pos(0, 0, T_CAMPO) * extrude(
        RectangleRounded(larg - 2 * L_MOLDURA, alt - 2 * L_MOLDURA, 8.0),
        T_MOLDURA - T_CAMPO + 1)

    cortes, n_furos = [], 0
    if not cego:
        for y_topo, d in filas(alt):
            y = alt / 2 - y_topo
            for x in colunas(larg):
                cortes.append(Pos(x, y, -1) * Cylinder(
                    d / 2, T_MOLDURA + 3,
                    align=(Align.CENTER, Align.CENTER, Align.MIN)))
                n_furos += 1
    if pega:
        h_pega = min(0.34 * alt, 26.0)
        cortes.append(Pos(0, alt * 0.10, -1) * extrude(
            RectangleRounded(0.42 * larg, h_pega, h_pega / 2 - 0.5),
            T_MOLDURA + 3))
    if cortes:
        p -= cortes

    # nos de dobradica: eixo paralelo a aresta inferior
    for x in pos_art(larg):
        p += Pos(x, -alt / 2 + 4.0, T_MOLDURA / 2) * Rot(0, 90, 0) * \
             Cylinder(R_PINO, L_PINO)
    return p, n_furos


def fundo():
    ext = RectangleRounded(EXT_C, EXT_L, RAIO)
    inte = RectangleRounded(EXT_C - 2 * T_SAIA, EXT_L - 2 * T_SAIA, RAIO - T_SAIA)
    anel = RectangleRounded(EXT_C - 2 * T_LIP, EXT_L - 2 * T_LIP, RAIO - T_LIP) - inte

    f = Pos(0, 0, H_PE) * extrude(ext, H_SAIA)                    # saia
    f -= Pos(0, 0, H_PE + T_CHAPA) * extrude(inte, H_SAIA)        # cava
    f -= Pos(0, 0, Z_RIM - H_PE) * extrude(anel, H_PE + 1)        # berco
    f += extrude(anel, H_PE)                                      # pe

    # orelhas de dobradica na face interna da saia + furo do pino
    orelhas, furos = [], []
    for x in pos_art(LARG_LONGO):
        for s in (-1, 1):
            y = s * (EXT_L / 2 - T_SAIA - 2.5)
            orelhas.append(Pos(x, y, Z_ART - 1) * Box(L_PINO + 8, 5.0, 14.0))
            furos.append(Pos(x, y, Z_ART) * Rot(0, 90, 0) *
                         Cylinder(R_BERCO, L_PINO + 12))
    for y in pos_art(LARG_CURTO):
        for s in (-1, 1):
            x = s * (EXT_C / 2 - T_SAIA - 2.5)
            orelhas.append(Pos(x, y, Z_ART - 1) * Box(5.0, L_PINO + 8, 14.0))
            furos.append(Pos(x, y, Z_ART) * Rot(90, 0, 0) *
                         Cylinder(R_BERCO, L_PINO + 12))
    f += orelhas
    f -= furos
    return f


def erguer(p, alt, aresta, sinal):
    """Roda o painel para a vertical e o assenta no eixo das dobradicas."""
    q = Pos(0, 0, Z_ART - 4.0 + alt / 2) * (Rot(90, 0, 0) * p)
    if aresta == "longa":                   # traseiro / frontal, em +-Y
        if sinal < 0:
            q = Rot(0, 0, 180) * q
        return Pos(0, sinal * (EXT_L / 2 - T_SAIA - FOLGA_EMB - T_MOLDURA / 2), 0) * q
    q = Rot(0, 0, 90 * sinal) * q           # laterais, em +-X
    return Pos(sinal * (EXT_C / 2 - T_SAIA - FOLGA_EMB - T_MOLDURA / 2), 0, 0) * q


def modelo(tam="P"):
    h_ext = TAMANHOS[tam] * MODULO
    alt = alt_painel(h_ext)
    h_front = round(FRAC_FRONTAL * alt / 5) * 5

    f = fundo()
    lat, n_lat = painel(LARG_CURTO, alt)
    tras, n_tras = painel(LARG_LONGO, alt)
    front, n_front = painel(LARG_LONGO, h_front, cego=True, pega=True)

    pecas = {"fundo": (f, 1, 0), "lateral": (lat, 2, n_lat),
             "traseira": (tras, 1, n_tras), "frontal": (front, 1, n_front)}
    conj = [f,
            erguer(lat, alt, "curta", +1), erguer(lat, alt, "curta", -1),
            erguer(tras, alt, "longa", +1), erguer(front, h_front, "longa", -1)]
    return pecas, conj, h_ext, alt, h_front


def dobrado(pecas, alt, h_front):
    """Paineis deitados DENTRO da bandeja, em camadas de 3,8 mm."""
    z0 = H_PE + T_CHAPA
    cam = T_MOLDURA + 0.8
    f = pecas["fundo"][0]
    lat = pecas["lateral"][0]
    out = [f]
    for i, s in enumerate((+1, -1)):                      # laterais
        dx = s * (EXT_C / 2 - T_SAIA - FOLGA_EMB - alt / 2)
        out.append(Pos(dx, 0, z0 + i * cam) * (Rot(0, 0, 90) * lat))
    for i, (p, a, s) in enumerate(((pecas["traseira"][0], alt, +1),
                                   (pecas["frontal"][0], h_front, -1))):
        dy = s * (EXT_L / 2 - T_SAIA - FOLGA_EMB - a / 2)
        out.append(Pos(0, dy, z0 + (2 + i) * cam) * p)
    return out


def main():
    tam = (sys.argv[1].upper() if len(sys.argv) > 1 else "P")
    pecas, conj, h_ext, alt, h_front = modelo(tam)
    dest = os.path.dirname(os.path.abspath(__file__))

    cx, cy, vol, vol_util = cavidade(h_ext, h_front)
    print(f"TAMANHO {tam} | altura externa {h_ext:.0f} mm | painel {alt:.0f} mm "
          f"| frontal {h_front:.0f} mm | footprint {EXT_C:.0f} x {EXT_L:.0f} R{RAIO:.0f}")
    print(f"Cavidade interna {cx:.0f} x {cy:.0f} mm | volume nominal {vol:.2f} L "
          f"| util ate a borda do frontal {vol_util:.2f} L")
    fl = filas(alt)
    print(f"Furos: reticulado {PASSO:.0f} mm, {len(fl)} filas, "
          f"D {' / '.join(f'{d:.1f}' for _, d in fl)} mm | banda cega {BANDA_CEGA:.1f} mm")
    print(f"Paineis embutidos: {LARG_LONGO:.0f} mm (traseiro/frontal), "
          f"{LARG_CURTO:.0f} mm (laterais) | "
          f"{len(colunas(LARG_CURTO))} e {len(colunas(LARG_LONGO))} colunas\n")

    print(f"{'peca':10} {'qtd':>4} {'volume':>12} {'peso':>9} {'furos':>7}")
    total = furos = 0.0
    for nome, (m, n, nf) in pecas.items():
        peso = m.volume * RHO
        total += n * peso
        furos += n * nf
        print(f"{nome:10} {n:4} {m.volume/1000:9.1f} cm3 {peso:7.1f} g {nf:7}")
    print(f"{'CONJUNTO':10} {5:4} {'':12} {total:7.1f} g {int(furos):7}")

    for nome, (m, _, _) in pecas.items():
        export_step(m, os.path.join(dest, f"{tam}-{nome}.step"))
        export_stl(m, os.path.join(dest, f"{tam}-{nome}.stl"))
    montado = Compound(children=list(conj))
    export_step(montado, os.path.join(dest, f"{tam}-conjunto.step"))

    bb = montado.bounding_box()
    dob_s = dobrado(pecas, alt, h_front)
    bd = Compound(children=list(dob_s)).bounding_box()
    print(f"\nEnvelope montado: {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm")
    print(f"Envelope dobrado: {bd.size.X:.1f} x {bd.size.Y:.1f} x {bd.size.Z:.1f} mm"
          f"   compactacao {bb.size.Z/bd.size.Z:.1f}x")

    import trimesh
    import render

    def malhas(solidos):
        out = []
        for i, s in enumerate(solidos):
            tmp = os.path.join(dest, f".t{i}.stl")
            export_stl(s, tmp)
            out.append((trimesh.load(tmp),
                        (0.78, 0.33, 0.10) if i == 0 else (0.92, 0.47, 0.17)))
            os.remove(tmp)
        return out

    mc, md = malhas(conj), malhas(dob_s)
    pilha = list(mc)
    for mm, c in mc:
        t = mm.copy()
        t.apply_translation([0, 0, h_ext])
        pilha.append((t, c))

    expl = []
    desloc = [(0, 0, 0), (150, 0, 60), (-150, 0, 60), (0, 150, 60), (0, -150, 60)]
    for (mm, c), dd in zip(mc, desloc):
        t = mm.copy()
        t.apply_translation(list(dd))
        expl.append((t, c))

    for arq, cena, d in [(f"01-montado-{tam}.png", mc, (-1.0, -1.5, -0.8)),
                         (f"05-explodido-{tam}.png", expl, (-1.0, -1.5, -0.85)),
                         (f"02-frontal-{tam}.png", mc, (0.06, -1.0, -0.19)),
                         (f"03-dobrado-{tam}.png", md, (-1.0, -1.4, -1.0)),
                         (f"04-pilha-{tam}.png", pilha, (-1.0, -1.5, -0.6))]:
        render.salvar(render.render(cena, direcao=d, largura=1500),
                      os.path.join(dest, arq))
        print("gerado", arq)


if __name__ == "__main__":
    main()
