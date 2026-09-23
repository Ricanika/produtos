#!/usr/bin/env python3
"""
Geometria da BASE MODULAR para os cestos Rattan G (069) e Rattan G Baixo (261).

REVISAO 2 - cantos arredondados e lombada
  - Montantes com canto externo R14 em planta; o tampo acompanha (R14) e
    ganha a aresta de cima arredondada em R6.
  - A boca do modulo (vista de frente) ganha filete R12 onde o montante
    encontra o piso; a abertura lateral ganha R20 nos cantos de cima.
  - O batente reto da frente (4 mm) e o encosto de tras (20 mm) sairam. No
    lugar, uma LOMBADA arredondada de 12 x 5 mm, IGUAL na frente e atras: o
    modulo fica simetrico, entra na torre de qualquer lado e a gaveta pode ser
    puxada pelos dois lados.
  Nada disso cria gaveta no molde: lombada e filete da boca olham para cima
  (macho), filete da janela olha para baixo por cima do rasgo (cavidade),
  cantos em planta sao verticais.

TRES PECAS, TRES MOLDES, NENHUMA GAVETA
  modulo alto   - recebe o 069.006.003  (38,5 x 28 x 19,0 cm)
  modulo baixo  - recebe o 261.006.003  (38,5 x 28 x  8,3 cm)
  tampo         - fecha o topo da torre (serve em cima dos dois)
  Os dois modulos tem a MESMA planta e a MESMA interface de empilhamento: so
  muda a altura. Qualquer um vai em cima de qualquer um, e o tampo vai em cima
  de qualquer um.

O MODULO E UM "U" ABERTO NA FRENTE, ATRAS E EM CIMA
  piso + duas laterais. O teto de cada modulo e o piso do modulo de cima; o do
  ultimo e o tampo. Por isso o molde abre em Z (para cima) e tudo o que existe
  na peca tem de ser visto OU de cima (macho) OU de baixo (cavidade).

A JANELA LATERAL SEM GAVETA - a regra que desenha a secao da lateral
  Furo em parede vertical normalmente pede gaveta. Aqui a lateral e feita em
  degrau, de dentro para fora:
     x 146,0 -> 149,0   PEITORIL: parede baixa que sobe do piso (feita pelo macho)
     x 149,0 -> 168,0   RASGO no piso, aberto ate embaixo
     x 156,4 -> 168,0   TRAVESSA em U invertido, no alto (feita pela cavidade,
                        que sobe pelo rasgo)
  Em planta o peitoril e a travessa NAO se sobrepoem. O macho e a cavidade se
  encontram dentro da janela num plano inclinado que vai do topo do peitoril
  (x 149,0) ate a base da travessa (x 156,4). O recuo de 7,4 mm e o que da
  3 graus de fechamento (shut-off) nos 142 mm da janela do modulo alto, que e a
  mais alta. x_trav() calcula; os numeros aqui sao so para leitura.

Unidades: mm. Eixos: X = largura (frente do cesto, 280), Y = profundidade
(385, Y=0 e a frente), Z = altura (Z=0 e a base do modulo).
Os tipos de elemento, a malha e o volume estao em solidos.py. Os elementos
podem se sobrepor: o volume e sempre o da uniao.
"""
import math
from solidos import perfil_filete, perfil_lombada

# ---------------------------------------------------------------- o cesto ---
CESTO = {
    "alto":  {"ref": "069.006.003", "L": 280.0, "P": 385.0, "H": 190.0},
    "baixo": {"ref": "261.006.003", "L": 280.0, "P": 385.0, "H": 83.0},
}

# ---------------------------------------------------------------- planta ----
FOLGA_X   = 6.0                    # folga lateral do cesto, por lado
X_IN      = CESTO["alto"]["L"] / 2 + FOLGA_X   # 146,0 face interna do peitoril
PEIT_T    = 3.0                    # espessura do peitoril
X_PEIT    = X_IN + PEIT_T          # 149,0 face externa do peitoril
X_EXT     = 168.0                  # face externa do modulo
LARG      = 2 * X_EXT              # 336,0 largura total
PROF      = 395.0                  # profundidade total
MONT_Y    = 32.0                   # profundidade de cada montante (coluna)
T         = 2.2                    # parede geral
T_NERV    = 1.6                    # nervura (~70% da parede: sem rechupe)

# ---------------------------------------------------------------- piso ------
PISO_H    = 18.0                   # do Z=0 ao topo do piso
PISO_PELE = 2.2
LOMB_W    = 12.0                   # lombada: largura na base (frente e tras)
LOMB_H    = 5.0                    # lombada: altura acima do piso
PEIT_H    = 30.0                   # peitoril, acima do piso
FUROS     = {"passo_y": 20.0, "furo_y": 12.0, "passo_x": 48.0, "furo_x": 40.0,
             "margem": 18.0}       # furacao do piso (oblongos)

# ---------------------------------------------------------------- lateral ---
SHUTOFF_GRAUS = 3.0                # angulo minimo de fechamento na janela
TRAV_TOPO = 3.0                    # espessura da mesa da travessa
TRAV_H    = {"alto": 30.0, "baixo": 20.0}

# ---------------------------------------------------------------- passo -----
# Passo do alto = 2 x passo do baixo: duas torres lado a lado alinham
# (dois baixos = um alto).
PASSO = {"alto": 220.0, "baixo": 110.0}

# ---------------------------------------------------------------- encaixe ---
PINO_R, PINO_RI, PINO_H = 6.0, 4.0, 8.0     # pino no topo de cada montante
GUIA_RI = PINO_R + 0.3                      # folga radial 0,3 no encaixe
GUIA_RE = GUIA_RI + 2.0
GUIA_H  = 12.0
PINO_XC = (X_IN + X_EXT) / 2               # centro do pino no montante
PINO_YC = MONT_Y / 2

# ---------------------------------------------------------------- tampo -----
TAMPO_H, TAMPO_PELE = 12.0, 2.5
TAMPO_RF  = 6.0                    # aresta de cima do tampo arredondada

# ---------------------------------------------------------------- raios ------
R_CANTO    = 14.0                  # canto externo do montante e do tampo, em planta
R_CANTO_IN = 3.0                   # canto do montante voltado para a boca
R_BOCA     = 12.0                  # filete montante -> piso, visto de frente
R_JANELA   = 20.0                  # filete montante -> travessa, visto de lado


def x_trav(modelo="alto"):
    """Face interna da travessa: onde a regra do shut-off deixa ela comecar.

    A janela vai do topo do peitoril ate a base da travessa. O fechamento
    macho/cavidade corre nesse vao inclinado; a menor inclinacao aparece na
    janela mais alta, que e a do modulo alto. A travessa usa o MESMO x nos dois
    modulos: planta e interface identicas."""
    h_jan = PASSO["alto"] - TRAV_H["alto"] - (PISO_H + PEIT_H)
    return round(X_PEIT + h_jan * math.tan(math.radians(SHUTOFF_GRAUS)), 1)


def janela(modelo):
    z0 = PISO_H + PEIT_H
    z1 = PASSO[modelo] - TRAV_H[modelo]
    return z0, z1


def _espelha_x(e):
    k = e[0]
    if k == "caixa":
        _, x0, x1, y0, y1, z0, z1, g = e
        return ("caixa", -x1, -x0, y0, y1, z0, z1, g)
    if k == "tubo":
        _, xc, yc, z0, z1, re, ri, g = e
        return ("tubo", -xc, yc, z0, z1, re, ri, g)
    if k == "prisma":
        _, eixo, a0, a1, pf, g = e
        if eixo == "x":
            return ("prisma", "x", -a1, -a0, pf, g)
        return ("prisma", "y", a0, a1, [(-u, v) for u, v in pf], g)
    if k == "rr":
        _, x0, x1, y0, y1, z0, z1, r, t, g = e
        return ("rr", -x1, -x0, y0, y1, z0, z1, (r[1], r[0], r[3], r[2]), t, g)
    raise ValueError(k)


def _espelha_y(e):
    """Espelha na profundidade: frente <-> tras (Y -> PROF - Y)."""
    k = e[0]
    if k == "caixa":
        _, x0, x1, y0, y1, z0, z1, g = e
        return ("caixa", x0, x1, PROF - y1, PROF - y0, z0, z1, g)
    if k == "tubo":
        _, xc, yc, z0, z1, re, ri, g = e
        return ("tubo", xc, PROF - yc, z0, z1, re, ri, g)
    if k == "prisma":
        _, eixo, a0, a1, pf, g = e
        if eixo == "y":
            return ("prisma", "y", PROF - a1, PROF - a0, pf, g)
        return ("prisma", "x", a0, a1, [(PROF - u, v) for u, v in pf], g)
    if k == "rr":
        _, x0, x1, y0, y1, z0, z1, r, t, g = e
        return ("rr", x0, x1, PROF - y1, PROF - y0, z0, z1, (r[3], r[2], r[1], r[0]), t, g)
    raise ValueError(k)


def _espelha(elems):
    out = []
    for e in elems:
        out += [e, _espelha_x(e)]
    return out


def _montante(P):
    """Montante da FRENTE, lado +X: casca de cantos arredondados, aberta por
    baixo, com tampa em cima, guia do pino embaixo e o pino no topo. O de tras
    sai por _espelha_y."""
    x0, x1, y0, y1 = X_IN, X_EXT, 0.0, MONT_Y
    raios = (R_CANTO_IN, R_CANTO, 0.0, 0.0)          # (x0y0, x1y0, x1y1, x0y1)
    e = [("rr", x0, x1, y0, y1, 0, P - 3.0, raios, T, "montante"),
         ("rr", x0, x1, y0, y1, P - 3.0, P, raios, None, "montante")]
    yc = (y0 + y1) / 2
    e.append(("tubo", PINO_XC, yc, 0, GUIA_H, GUIA_RE, GUIA_RI, "encaixe"))
    # duas nervuras ligando a guia as paredes do montante
    e.append(("caixa", PINO_XC - T_NERV / 2, PINO_XC + T_NERV / 2, y0 + T, yc - GUIA_RE,
              0, GUIA_H, "encaixe"))
    e.append(("caixa", PINO_XC - T_NERV / 2, PINO_XC + T_NERV / 2, yc + GUIA_RE, y1 - T,
              0, GUIA_H, "encaixe"))
    e.append(("tubo", PINO_XC, yc, P, P + PINO_H, PINO_R, PINO_RI, "encaixe"))
    return e


def _pele_furada(x0, x1, y0, y1, z0, z1, g):
    """Pele do piso com oblongos: montada como barras (sem subtracao)."""
    f = FUROS
    m = f["margem"]
    e = [("caixa", x0, x1, y0, y0 + m, z0, z1, g),
         ("caixa", x0, x1, y1 - m, y1, z0, z1, g),
         ("caixa", x0, x0 + m, y0, y1, z0, z1, g),
         ("caixa", x1 - m, x1, y0, y1, z0, z1, g)]
    ia, ib = x0 + m, x1 - m
    ja, jb = y0 + m, y1 - m
    ny = int((jb - ja + (f["passo_y"] - f["furo_y"])) // f["passo_y"])
    sobra_y = (jb - ja) - (ny * f["passo_y"] - (f["passo_y"] - f["furo_y"]))
    y = ja + sobra_y / 2
    # barras transversais entre as fileiras
    if sobra_y > 0:
        e.append(("caixa", ia, ib, ja, y, z0, z1, g))
    nx = int((ib - ia + (f["passo_x"] - f["furo_x"])) // f["passo_x"])
    sobra_x = (ib - ia) - (nx * f["passo_x"] - (f["passo_x"] - f["furo_x"]))
    for k in range(ny):
        yf0, yf1 = y, y + f["furo_y"]
        x = ia + sobra_x / 2
        if sobra_x > 0:
            e.append(("caixa", ia, x, yf0, yf1, z0, z1, g))
            e.append(("caixa", ib - sobra_x / 2, ib, yf0, yf1, z0, z1, g))
        for i in range(nx - 1):
            xb = x + (i + 1) * f["passo_x"] - (f["passo_x"] - f["furo_x"])
            e.append(("caixa", xb, xb + f["passo_x"] - f["furo_x"], yf0, yf1, z0, z1, g))
        y = yf1
        yb1 = min(y + f["passo_y"] - f["furo_y"], jb)
        if k < ny - 1 or yb1 < jb:
            e.append(("caixa", ia, ib, y, jb if k == ny - 1 else yb1, z0, z1, g))
        y = yb1
    return e, nx * ny


def nervuras_y():
    """Centro das barras cheias entre fileiras de oblongos do piso."""
    pele, _ = _pele_furada(-X_IN, X_IN, T, PROF - T, 0, 1, "x")
    ys = sorted({round((e[3] + e[4]) / 2, 3) for e in pele[4:]
                 if e[1] == -X_IN + FUROS["margem"] and e[2] == X_IN - FUROS["margem"]})
    return ys


def modulo(modelo):
    P = PASSO[modelo]
    xt = x_trav()
    zp0 = PISO_H - PISO_PELE
    # piso: pele inteira de peitoril a peitoril, oblongos so no miolo
    e_piso, n_furos = _pele_furada(-X_IN, X_IN, T, PROF - T, zp0, PISO_H, "piso")
    # nervuras sob o piso: uma transversal (vao em X) sob CADA barra cheia entre
    # fileiras de oblongos - a barra vira a mesa do T - e 3 longitudinais
    nerv = []
    for y in nervuras_y():
        nerv.append(("caixa", -X_IN, X_IN, y - T_NERV / 2, y + T_NERV / 2, 0, zp0, "piso"))
    for xc in (-X_IN / 2, 0.0, X_IN / 2):
        nerv.append(("caixa", xc - T_NERV / 2, xc + T_NERV / 2, T, PROF - T, 0, zp0, "piso"))
    # frente: aba (viga do piso) + lombada arredondada em cima dela.
    # A de tras e o espelho: o modulo e simetrico frente/tras.
    frente = [("caixa", -X_IN, X_IN, 0, T + 0.8, 0, PISO_H, "piso"),
              ("prisma", "x", -X_IN, X_IN,
               perfil_lombada(0.0, LOMB_W, PISO_H, LOMB_H, +1), "lombada")]
    lado = []
    # peitoril: do Z=0 ate PISO_H + PEIT_H, entre os montantes
    lado.append(("caixa", X_IN, X_PEIT, MONT_Y, PROF - MONT_Y, 0, PISO_H + PEIT_H, "lateral"))
    # travessa em U invertido
    zt = P - TRAV_H[modelo]
    lado += [("caixa", xt, X_EXT, MONT_Y, PROF - MONT_Y, P - TRAV_TOPO, P, "lateral"),
             ("caixa", xt, xt + T, MONT_Y, PROF - MONT_Y, zt, P, "lateral"),
             ("caixa", X_EXT - T, X_EXT, MONT_Y, PROF - MONT_Y, zt, P, "lateral")]
    # uma nervura transversal no meio da travessa (fecha o U)
    ym = PROF / 2
    lado.append(("caixa", xt, X_EXT, ym - T_NERV / 2, ym + T_NERV / 2, zt, P, "lateral"))
    canto_frente = _montante(P)
    # filete da janela (vista de lado): montante -> travessa. Olha para baixo,
    # por cima do rasgo: a cavidade forma.
    canto_frente.append(("prisma", "x", xt, X_EXT,
                         perfil_filete((MONT_Y, zt), +1, -1, R_JANELA), "lateral"))
    # filete da boca (vista de frente): montante -> piso. Olha para cima: macho.
    canto_frente.append(("prisma", "y", 0.0, MONT_Y,
                         perfil_filete((X_IN, PISO_H), -1, +1, R_BOCA), "montante"))
    lado += canto_frente + [_espelha_y(e) for e in canto_frente]
    frente_tras = frente + [_espelha_y(e) for e in frente]
    return e_piso + nerv + frente_tras + _espelha(lado), n_furos


def tampo():
    H, pele = TAMPO_H, TAMPO_PELE
    e = [("casca_tampo", -X_EXT, X_EXT, 0.0, PROF, H, R_CANTO, TAMPO_RF, pele, pele, "tampo")]
    # grelha de nervuras por baixo, dentro da saia
    xi, yi = X_EXT - pele, pele
    y = 50.0
    while y < PROF - 20:
        e.append(("caixa", -xi, xi, y - T_NERV / 2, y + T_NERV / 2, 0, H - pele, "tampo"))
        y += 50.0
    for xc in (-112.0, -56.0, 0.0, 56.0, 112.0):
        e.append(("caixa", xc - T_NERV / 2, xc + T_NERV / 2, yi, PROF - yi, 0, H - pele, "tampo"))
    # quatro soquetes que recebem os pinos
    for sx in (-1, 1):
        for yc in (PINO_YC, PROF - PINO_YC):
            e.append(("tubo", sx * PINO_XC, yc, 0, H - pele, GUIA_RE, GUIA_RI, "encaixe"))
    return e


PECAS = {
    "modulo-alto":  lambda: modulo("alto")[0],
    "modulo-baixo": lambda: modulo("baixo")[0],
    "tampo":        tampo,
}
