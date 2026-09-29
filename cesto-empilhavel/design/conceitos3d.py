#!/usr/bin/env python3
"""Constroi os DEZ conceitos B2C como solidos de verdade e renderiza cada um.

ESTUDO DE FORMA, nao peca de producao. Cada conceito sai da peca de hoje
(o ELO P, configuracao C) com uma alteracao aplicada -- por parametro,
quando o modelo ja tem a alavanca, ou por operacao booleana em cima do
solido pronto, quando nao tem. O que NAO foi feito aqui, e esta na folha:
auditoria de extracao, medicao de empilhamento, encaixe e acoplamento. O
solido serve para OLHAR e escolher; depois da escolha e que ele vira peca.

Uso:  python3 conceitos3d.py            (todos)
      python3 conceitos3d.py 1 5 8      (so estes)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "cad"))

from build123d import (Box, Circle, Plane, Pos, Rectangle, RectangleRounded,
                       export_stl, extrude)

import modelo3d as M

DEST = os.path.dirname(os.path.abspath(__file__))
STL = os.path.join(DEST, "stl")


def reset():
    """Volta o modelo para a configuracao C do P, inteira."""
    M.padrao()
    M.VAZADO, M.FUNDO_VAZADO = "listra", False
    M.LIS_W, M.LIS_P, M.LIS_H = 6.0, 11.0, 18.0
    M.LIS_WEB, M.LIS_MIN = 8.0, 9.0
    M.R_PLANTA = 14.0
    M.Z_TOPO = M.ALT - M.H_RIM - 9.0


def planta(z, folga=0.0):
    """Planta EXTERNA da casca na cota z (a casca abre subindo)."""
    return (M.BASE_X + 2 * z * M.TAN + 2 * folga,
            M.BASE_Y + 2 * z * M.TAN + 2 * folga)


def cone(folga=0.0, alt=None):
    """O cone externo da casca, deslocado de `folga` para fora."""
    alt = M.ALT + 40 if alt is None else alt
    return extrude(RectangleRounded(M.BASE_X + 2 * folga, M.BASE_Y + 2 * folga,
                                    M.R_PLANTA + folga), alt, taper=-M.DRAFT)


def anel(z0, z1, d, folga_fora=30.0):
    """Anel prismatico que come `d` da face externa, entre z0 e z1."""
    sx, sy = planta((z0 + z1) / 2)
    fora = RectangleRounded(sx + 2 * folga_fora, sy + 2 * folga_fora,
                            M.R_PLANTA + folga_fora)
    dentro = RectangleRounded(sx - 2 * d, sy - 2 * d,
                              max(M.R_PLANTA - d, 1.0))
    return Pos(0, 0, z0) * extrude(fora - dentro, z1 - z0)


# ---------------------------------------------------------------- conceitos
def c_hoje():
    reset()
    return M.cesto(aba=True)[0], "a peca de hoje, para comparar"


def c_lisa():
    reset()
    M.VAZADO = "nenhum"
    return M.cesto(aba=True)[0], "parede fechada: a superficie e que fala"


def c_ripado():
    reset()
    M.LIS_W, M.LIS_P, M.LIS_H = 9.0, 16.0, 400.0
    M.LIS_MIN, M.LIS_WEB = 9.0, 8.0
    return M.cesto(aba=True)[0], "uma fenda continua por coluna, do pe a borda"


def c_canelado():
    """Nervura vertical em relevo, saindo do cone deslocado: a canelura
    acompanha a saida por construcao e nao afina a parede em canto nenhum.

    As laminas tem de ser CURTAS. Na primeira tentativa cada lamina
    atravessava a peca inteira, e a intersecao com a casca deixou nervura
    solta no ar onde a parede nao existe -- alem da traseira, acima do rim --,
    5 mm a mais de envelope em y e um render com espinho. Agora cada lamina
    cobre so o painel dela.
    """
    reset()
    M.VAZADO = "nenhum"
    p = M.cesto(aba=True)[0]
    casca = cone(0.7, M.ALT - 6) - cone(0.0)
    lam = []
    for xi in _grade(M.LARG - 56, 9.0):          # painel da frente e do fundo
        for sy in (-1, 1):
            lam.append(Pos(xi, sy * M.PROF / 2, M.ALT / 2 + 4) *
                       Box(2.4, 44.0, M.ALT - 8))
    for yi in _grade(M.PROF - 56, 9.0):          # painel das duas laterais
        for sx in (-1, 1):
            lam.append(Pos(sx * M.LARG / 2, yi, M.ALT / 2 + 4) *
                       Box(44.0, 2.4, M.ALT - 8))
    laminas = sum(lam[1:], lam[0])
    # E a SILHUETA que diz onde ha parede. Sem este recorte a nervura da
    # frente fica boiando a 5 mm da face, porque o chanfro recua a frente e
    # o cone (de onde a casca sai) nao sabe disso.
    perfil = extrude(Plane.YZ * M.silhueta(), M.LARG / 2 + 40, both=True)
    return p + (casca & laminas & perfil), "canelura de 0,7 mm, cantos lisos"


def c_meia_pele():
    """Fecha a faixa de cima. Mexer em M.Z_TOPO nao resolve: o cesto() calcula
    o proprio z_topo como variavel LOCAL (ALT - h_rim - 9) e e esse que chega
    nas listras -- a peca saiu identica a de hoje, 179,2 g, na primeira
    tentativa. Entao a troca e na funcao que devolve as faixas."""
    reset()
    orig = M.listras
    M.listras = lambda z=None: [f for f in orig(z) if f[1] <= M.BANDA + 46]
    try:
        p = M.cesto(aba=True)[0]
    finally:
        M.listras = orig
    return p, "vazado so na faixa baixa; o topo fica cego"


def c_arco():
    """Um arco recortado na frente.

    Duas tentativas antes desta falharam, e valem como registro: reduzir o
    chanfro de topo para 6 mm quebra o fillet R12 da face frontal, e reduzi-lo
    para 16 mm quebra a tapa do rasgo. A frente da peca de hoje e uma teia de
    feicoes amarradas ao chanfro -- mexer nele e projeto, nao estudo de forma.
    Entao o arco e cortado na frente COMO ELA E, e GRANDE o bastante para
    encostar na concha: os dois viram uma abertura so, em arco, do pe a
    borda. Um arco pequeno embaixo da concha nao le como arco -- le como
    furo, e foi o primeiro resultado.
    """
    reset()
    M.VAZADO = "nenhum"
    p = M.cesto(aba=True)[0]
    w, h, z0 = 112.0, 34.0, 12.0
    sk = Rectangle(w, h) + Pos(0, h / 2) * Circle(w / 2)
    corte = Pos(0, -M.PROF / 2, z0 + h / 2) * extrude(
        Plane.XZ * sk, 40.0, both=True)
    return p - corte, "o acesso da frente vira um arco"


def c_pega():
    reset()
    p = M.cesto(aba=True)[0]
    w, h = 78.0, 22.0
    zc = M.Z_TOPO - 4.0
    sk = RectangleRounded(w, h, h / 2 - 0.01)
    for s in (-1, 1):
        p -= Pos(s * M.LARG / 2, 0, zc) * extrude(
            Plane.YZ * sk, 30.0, both=True)
    return p, "recorte oval nas duas faces curtas"


def c_r60():
    reset()
    M.R_PLANTA = 40.0
    return M.cesto(aba=True)[0], "planta R40 na base (~R54 na boca)"


def c_plinto():
    """Base recuada. NAO da para fazer cortando a face externa: a parede tem
    1,4 mm, entao tirar 5 mm dela apaga a saia inteira e a peca passa a
    comecar em z = 5. O jeito certo e TROCAR a saia: tira a de hoje e devolve
    uma de mesma espessura, 4 mm mais para dentro."""
    reset()
    p = M.cesto(aba=True)[0]
    z1, d = 4.6, 4.0
    p -= anel(0.0, z1, d)                       # tira a saia de hoje
    saia = cone(-d, alt=6.2) - cone(-d - M.T_PAREDE, alt=6.2)
    return p + saia, "saia recuada 4 mm: fresta de sombra sob a peca"


def c_borda():
    reset()
    p = M.cesto(aba=True)[0]
    # tira a aba plana
    p -= anel(M.ALT - M.ABA_T - 0.4, M.ALT + 2.0, 0.0)
    # e devolve uma borda que desce 13 mm por fora
    sx, sy = planta(M.ALT)
    fora = Pos(0, 0, M.ALT - 13.0) * extrude(
        RectangleRounded(sx + 13.0, sy + 13.0, M.R_PLANTA + M.ALT * M.TAN + 6.5),
        13.0)
    return p + (fora - cone(0.0)), "a aba vira para baixo e some de fora"


def c_junta():
    reset()
    p = M.cesto(aba=True)[0]
    z1 = M.ALT - M.ABA_T - 1.0
    return p - anel(z1 - 7.0, z1, 2.0), "rebaixo de 2 mm: a junta vira sombra"


def _grade(largura, passo):
    """Posicoes simetricas em torno de zero, dentro de `largura`."""
    n = int(largura // passo)
    return [(-n / 2 + 0.5 + i) * passo for i in range(n + 1)]


CONCEITOS = [
    (0, "hoje", c_hoje),
    (1, "lisa", c_lisa),
    (2, "ripado", c_ripado),
    (3, "canelado", c_canelado),
    (4, "meia-pele", c_meia_pele),
    (5, "arco", c_arco),
    (6, "pega", c_pega),
    (7, "r40", c_r60),
    (8, "plinto", c_plinto),
    (9, "borda", c_borda),
    (10, "junta", c_junta),
]


def main(quais=None):
    os.makedirs(STL, exist_ok=True)
    import json
    import time
    saida = {}
    arq = os.path.join(DEST, "conceitos-medidas.json")
    if os.path.exists(arq):
        saida = json.load(open(arq, encoding="utf-8"))
    for n, nome, fn in CONCEITOS:
        if quais and n not in quais:
            continue
        t0 = time.time()
        try:
            p, nota = fn()
            peso = p.volume * M.RHO
            cap = M.capacidade()
            bb = p.bounding_box()
            export_stl(p, os.path.join(STL, f"c{n:02d}-{nome}.stl"))
            saida[str(n)] = {
                "nome": nome, "nota": nota, "peso": peso, "cap": cap,
                "env": [bb.size.X, bb.size.Y, bb.size.Z],
                "seg": round(time.time() - t0, 1)}
            print(f"[{n:2d}] {nome:10} {peso:7.1f} g  {cap:5.2f} L  "
                  f"{bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f}  "
                  f"({time.time()-t0:.0f} s)")
        except Exception as e:
            print(f"[{n:2d}] {nome:10} FALHOU: {type(e).__name__}: {e}")
        json.dump(saida, open(arq, "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:] if a.isdigit()] or None)
