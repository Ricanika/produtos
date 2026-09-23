#!/usr/bin/env python3
"""Auditoria de EXTRACAO: o que um molde de duas placas nao consegue formar.

Pergunta do cliente (23/09): "pensando nas nossas injetoras, essa borda
superior para dentro possivelmente nao conseguira fazer a extracao, confere?"

Nao e pergunta de opiniao. Num molde de duas placas, com o MACHO saindo em +z
e a CAVIDADE em -z:

  MACHO    -- um ponto do vao interno so e formavel se NAO HOUVER MATERIAL
              ACIMA dele na mesma coluna (x, y). Se houver, o macho fica preso
              debaixo da saliencia: contra-saida, e ali precisa de macho
              colapsavel ou gaveta.
  CAVIDADE -- a silhueta externa nao pode DIMINUIR subindo, senao a cavidade
              nao desce sem raspar a peca.

Como mede. Corta os solidos cota por cota e trabalha em shapely:
  * o VAO INTERNO vem do CAD, nao dos furos do corte. Com a parede vazada, um
    corte em z = 100 nao e uma coroa: sao ~60 ilhas, as nervuras entre
    listras, e "furo do poligono" ali nao significa nada. O vao vem do solido
    (fora & silhueta) - peca, componente que contem (0, 0, 100).
  * a SOMBRA DESCENDENTE S(z) = material(z) U S(z+dz) diz onde ha material
    acima. Contra-saida do macho = vao(z) inteserctado com S(z).
  * a SILHUETA vem da peca remontada com parede cheia mais o vao -- um bloco
    macico cuja fronteira e a superficie externa.

Depende de networkx e rtree (dependencias opcionais do trimesh, usadas por
Path2D.polygons_full): `pip install networkx rtree`.

Uso:  python3 extracao.py
"""
import os

import numpy as np
import trimesh
from build123d import (Box, Plane, Pos, RectangleRounded, export_stl,
                       extrude)
from shapely.geometry import Polygon
from shapely.ops import unary_union

import modelo3d as M

DEST = os.path.dirname(os.path.abspath(__file__))
DZ = 1.0


def solidos():
    """(peca, vao interno, envelope macico) -- os tres solidos da auditoria."""
    fora = extrude(RectangleRounded(M.BASE_X, M.BASE_Y, 14.0), M.ALT,
                   taper=-M.DRAFT)
    sil = extrude(Plane.YZ * M.silhueta(), M.LARG / 2 + 30, both=True)
    p, _ = M.cesto(aba=True)

    vazio = (fora & sil) - p
    dentro = None
    for s in vazio.solids():
        b = s.bounding_box()
        if b.min.Z < 100.0 < b.max.Z and abs(b.center().X) < 40:
            dentro = s if dentro is None else dentro + s
    if dentro is None:
        raise SystemExit("nao achei o vao interno em (0, 0, 100)")

    guarda = M.VAZADO
    M.VAZADO = "nenhum"
    try:
        cheia, _ = M.cesto(aba=True)
    finally:
        M.VAZADO = guarda
    return p, dentro, cheia + dentro


def planta(m, z):
    """Poligono shapely do corte de `m` na cota z, em coordenadas do MUNDO.

    ATENCAO: `to_2D()` do trimesh escolhe o referencial do plano por conta e
    aplica uma TRANSLACAO diferente em cada corte (medido: -45,4 mm em
    z = 57 e +20,2 mm em z = 128,5). Com ela as cotas ficam desalinhadas
    entre si e qualquer acumulo cota a cota -- como a sombra descendente
    daqui -- sai lixo. Por isso `to_planar` com a IDENTIDADE: assim x e y
    sao os do mundo em todas as cotas.
    """
    s = m.section(plane_normal=[0, 0, 1], plane_origin=[0, 0, float(z)])
    if s is None:
        return None
    p2 = s.to_planar(to_2D=np.eye(4), check=False)[0]
    polis = list(p2.polygons_full)
    return unary_union(polis) if polis else None


def audita(peca, dz=DZ):
    """Volume que NENHUMA das duas metades alcanca, cota por cota.

    O teste e um so: um ponto do espaco vazio e formavel se nao houver
    material ACIMA dele (o macho chega de cima) OU nao houver material ABAIXO
    (a cavidade chega de baixo). O que tem material dos dois lados e nao e
    material precisa de gaveta, macho colapsavel ou postico:

        preso(z) = sombra_de_cima(z) ^ sombra_de_baixo(z) - material(z)

    Isso trata certo o chanfro de topo: na frente do cesto, acima da borda
    baixa, nao ha material nenhum na coluna, entao aquele espaco e do MACHO --
    e por isso que o macho desta peca tem um lobo que desce na frente da
    parede baixa e fecha contra a cavidade na propria aresta da borda (linha
    de fechamento acompanhando o rim, que e o normal em caixaria).

    FALSO POSITIVO conhecido: um furo PASSANTE na parede entra na conta, pois
    tem material acima e abaixo. Mas ali o fechamento e na propria superficie
    com saida da parede, e a profundidade presa e so a espessura dela --
    1,4 mm, que zera depois de 1,4/tg(12) = 6,6 mm de curso. E por isso que
    caixaria tem centenas de rasgos e se faz em molde de duas placas. Para
    separar: rode tambem sem a feicao suspeita e compare.
    """
    zs = np.arange(dz / 2, peca.bounds[1][2], dz)
    mats = {z: planta(peca, z) for z in zs}
    bloco = unary_union([m for m in mats.values() if m is not None]).convex_hull

    cima, acum = {}, None
    for z in reversed(zs):
        m_ = mats.get(z)
        if m_ is not None and not m_.is_empty:
            acum = m_ if acum is None else unary_union([acum, m_])
        cima[z] = acum
    baixo, acum = {}, None
    for z in zs:
        m_ = mats.get(z)
        if m_ is not None and not m_.is_empty:
            acum = m_ if acum is None else unary_union([acum, m_])
        baixo[z] = acum

    presa = {}
    for z in zs:
        a, b, m_ = cima.get(z), baixo.get(z), mats.get(z)
        if a is None or b is None:
            continue
        r = a.intersection(b)
        if m_ is not None:
            r = r.difference(m_)
        if not r.is_empty:
            presa[z] = (r.area, bloco.area)
    return sum(a for a, _ in presa.values()) * dz, presa


def relatorio(nome, vol, presa, dz=DZ):
    print(f"\n{nome}: volume preso = {vol:8.0f} mm3")
    pts = [(z, a) for z, (a, _) in presa.items() if a > 0.5]
    if not pts:
        print("  nada preso -- as duas metades saem retas")
        return
    z0, z1 = min(z for z, _ in pts), max(z for z, _ in pts)
    print(f"  faixa z {z0:.1f} a {z1:.1f} mm")
    for z, a in sorted(pts, key=lambda t: -t[1])[:5]:
        print(f"    z={z:6.1f}: {a:8.1f} mm2")


def main():
    M.padrao()
    res = {}
    for nome, com_aba in (("peca como esta", True), ("SEM a aba", False)):
        if not com_aba:
            guarda = M._aba
            M._aba = lambda fora, interno: Pos(0, 0, -50) * Box(1, 1, 1)
        try:
            p, _ = M.cesto(aba=True)
        finally:
            if not com_aba:
                M._aba = guarda
        arq = os.path.join(DEST, f"ext-{'com' if com_aba else 'sem'}.stl")
        export_stl(p, arq)
        vol, presa = audita(trimesh.load(arq))
        res[nome] = vol
        relatorio(nome, vol, presa)
    a, b = res["peca como esta"], res["SEM a aba"]
    print(f"\n=> a ABA responde por {a-b:.0f} mm3 dos {a:.0f}; "
          f"os {b:.0f} restantes sao os rasgos passantes da parede,")
    print(f"   que travam so a espessura dela (1,4 mm) e liberam em 6,6 mm "
          f"de curso -- fechamento normal.")
    # A cota que decide e a da aba para DENTRO: quanto ela avanca sobre a
    # boca. Com ABA_DIR = +1 a aba nem entra na boca, entao aqui a conta e
    # CONTRAFACTUAL -- o que a mesma peca prenderia se a aba fosse virada
    # para dentro. Imprimir isso como se fosse a peca atual, como a primeira
    # versao fazia, e afirmar o contrario do que a peca e.
    x_int = M.BASE_X / 2 + M.TAN * (M.ALT - M.ABA_T) - M.T_RIM
    avanco = x_int - (M.LARG / 2 - M.ABA_W)
    if M.ABA_DIR > 0:
        print(f"\nA COTA QUE DECIDE (contrafactual -- a aba desta peca esta "
              f"para FORA):")
        print(f"   virada para DENTRO ela avancaria {avanco:.2f} mm sobre a "
              f"face interna da parede,")
    else:
        print(f"\nA COTA QUE DECIDE: a aba avanca {avanco:.2f} mm para "
              f"DENTRO da face interna da parede,")
    print(f"   numa boca interna de {2*x_int:.1f} mm -> "
          f"{100*avanco/x_int:.1f}% por lado, "
          f"em degrau de {M.ABA_T} mm continuo.")


if __name__ == "__main__":
    main()
