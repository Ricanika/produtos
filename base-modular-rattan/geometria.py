#!/usr/bin/env python3
"""
Geometria da BASE MODULAR para os cestos Rattan G (069) e Rattan G Baixo (261).

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
  Os montantes (colunas) sao caixas ocas abertas por baixo.

Unidades: mm. Eixos: X = largura (frente do cesto, 280), Y = profundidade
(385, Y=0 e a frente), Z = altura (Z=0 e a base do modulo).

Cada peca e uma lista de elementos:
   ("caixa", x0, x1, y0, y1, z0, z1, grupo)
   ("tubo",  xc, yc, z0, z1, r_ext, r_int, grupo)   eixo vertical
As caixas podem se sobrepor: volume e area projetada saem da UNIAO
(uniao_volume / area_projetada), nunca da soma.
"""
import math

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
BATENTE_F = 4.0                    # batente da frente, acima do piso
BATENTE_T = 20.0                   # encosto de tras, acima do piso
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


def _espelha(elems):
    out = []
    for e in elems:
        out.append(e)
        if e[0] == "caixa":
            _, x0, x1, y0, y1, z0, z1, g = e
            out.append(("caixa", -x1, -x0, y0, y1, z0, z1, g))
        else:
            _, xc, yc, z0, z1, re, ri, g = e
            out.append(("tubo", -xc, yc, z0, z1, re, ri, g))
    return out


def _montante(y0, y1, P):
    """Caixa oca aberta por baixo, com tampa em cima e guia do pino embaixo."""
    x0, x1 = X_IN, X_EXT
    e = [("caixa", x0, x1, y0, y0 + T, 0, P, "montante"),
         ("caixa", x0, x1, y1 - T, y1, 0, P, "montante"),
         ("caixa", x0, x0 + T, y0, y1, 0, P, "montante"),
         ("caixa", x1 - T, x1, y0, y1, 0, P, "montante"),
         ("caixa", x0, x1, y0, y1, P - 3.0, P, "montante")]
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
    e = []
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
    # batentes de frente e de tras (sao tambem as vigas de frente/tras do piso)
    frente = [("caixa", -X_IN, X_IN, 0, T + 0.8, 0, PISO_H + BATENTE_F, "piso")]
    tras   = [("caixa", -X_IN, X_IN, PROF - T - 0.8, PROF, 0, PISO_H + BATENTE_T, "piso")]
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
    lado += _montante(0.0, MONT_Y, P)
    lado += _montante(PROF - MONT_Y, PROF, P)
    return e_piso + nerv + frente + tras + _espelha(lado), n_furos


def tampo():
    H, pele = TAMPO_H, TAMPO_PELE
    e = [("caixa", -X_EXT, X_EXT, 0, PROF, H - pele, H, "tampo")]
    # saia de perimetro
    e += [("caixa", -X_EXT, X_EXT, 0, T, 0, H, "tampo"),
          ("caixa", -X_EXT, X_EXT, PROF - T, PROF, 0, H, "tampo"),
          ("caixa", -X_EXT, -X_EXT + T, 0, PROF, 0, H, "tampo"),
          ("caixa", X_EXT - T, X_EXT, 0, PROF, 0, H, "tampo")]
    # grelha de nervuras por baixo
    y = 50.0
    while y < PROF - 20:
        e.append(("caixa", -X_EXT, X_EXT, y - T_NERV / 2, y + T_NERV / 2, 0, H - pele, "tampo"))
        y += 50.0
    for xc in (-112.0, -56.0, 0.0, 56.0, 112.0):
        e.append(("caixa", xc - T_NERV / 2, xc + T_NERV / 2, 0, PROF, 0, H - pele, "tampo"))
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


# ----------------------------------------------------------- uniao exata ----
def _cortes(vals):
    return sorted(set(round(v, 4) for v in vals))


def uniao_volume(elems):
    """Volume exato da uniao das caixas (varredura em Z com compressao em XY)
    + volume analitico dos tubos (os tubos nao se sobrepoem a caixas)."""
    caixas = [e for e in elems if e[0] == "caixa"]
    tubos = [e for e in elems if e[0] == "tubo"]
    xs = _cortes([c[1] for c in caixas] + [c[2] for c in caixas])
    ys = _cortes([c[3] for c in caixas] + [c[4] for c in caixas])
    zs = _cortes([c[5] for c in caixas] + [c[6] for c in caixas])
    ix = {v: i for i, v in enumerate(xs)}
    iy = {v: i for i, v in enumerate(ys)}
    dx = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    dy = [ys[j + 1] - ys[j] for j in range(len(ys) - 1)]
    vol = 0.0
    for k in range(len(zs) - 1):
        za, zb = zs[k], zs[k + 1]
        zm = (za + zb) / 2
        grade = [bytearray(len(dy)) for _ in dx]
        for c in caixas:
            if c[5] < zm < c[6]:
                for i in range(ix[round(c[1], 4)], ix[round(c[2], 4)]):
                    row = grade[i]
                    a, b = iy[round(c[3], 4)], iy[round(c[4], 4)]
                    row[a:b] = b"\x01" * (b - a)
        area = 0.0
        for i, row in enumerate(grade):
            if any(row):
                area += dx[i] * sum(dy[j] for j in range(len(row)) if row[j])
        vol += area * (zb - za)
    for t in tubos:
        _, xc, yc, z0, z1, re, ri, _ = t
        vol += math.pi * (re * re - ri * ri) * (z1 - z0)
    return vol


def area_projetada(elems):
    """Area da sombra da peca em planta (o que a forca de fechamento empurra)."""
    caixas = [e for e in elems if e[0] == "caixa"]
    xs = _cortes([c[1] for c in caixas] + [c[2] for c in caixas])
    ys = _cortes([c[3] for c in caixas] + [c[4] for c in caixas])
    ix = {v: i for i, v in enumerate(xs)}
    iy = {v: i for i, v in enumerate(ys)}
    grade = [bytearray(len(ys) - 1) for _ in range(len(xs) - 1)]
    for c in caixas:
        a, b = iy[round(c[3], 4)], iy[round(c[4], 4)]
        for i in range(ix[round(c[1], 4)], ix[round(c[2], 4)]):
            grade[i][a:b] = b"\x01" * (b - a)
    area = 0.0
    for i, row in enumerate(grade):
        w = xs[i + 1] - xs[i]
        area += w * sum(ys[j + 1] - ys[j] for j in range(len(row)) if row[j])
    return area
