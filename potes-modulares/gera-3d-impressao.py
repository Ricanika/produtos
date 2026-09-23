#!/usr/bin/env python3
"""
Variantes dos STL para PROTOTIPAR em FDM (nao sao as pecas de producao).

O corpo de producao apoia na mesa so pelo anel do pe rebaixado - area pequena
demais para segurar uma peca de 62 mm de altura em qualquer impressora. Aqui
saem duas versoes do 600 ml:

  pote-600-real.stl        a peca como e, fundo rebaixado. Imprima com brim.
  pote-600-fundoplano.stl  elevacao de fundo zerada -> ~20x mais contato. Muda
                           so o volume interno (+19 ml), nao muda encaixe, passo
                           nem a prova da tampa. E a que eu imprimiria primeiro.

As areas de contato sao MEDIDAS na malha, nao digitadas: numero fixo aqui ja
ficou defasado uma vez, quando o footprint mudou de 121,2 para 139,7 mm.
  tampa-pp.stl             tampa de PP com 2 travas de clipe. Imprime em pe.
  tampa-teca.stl           placa macica - so para conferir encaixe (em teca e CNC).
  tampa-correr.stl         a de correr, com a janela e a calha em U.
  gaveta.stl               o painel que corre. E o par que mais precisa de
                           prototipo: a folga de projeto e 0,25 mm por lado, e
                           nenhuma FDM entrega isso sem ajuste - conte com
                           lixar a gaveta ou reimprimir com escala.

Uso:  python3 gera-3d-impressao.py
"""
import os
import importlib.util

spec = importlib.util.spec_from_file_location("gera3d",
       os.path.join(os.path.dirname(os.path.abspath(__file__)), "gera-3d.py"))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

SEG = 24          # o dobro do padrao: canto mais liso no prototipo


def altura(tris):
    zs = [v[2] for t in tris for v in t]
    return max(zs) - min(zs)


def contato(tris, tol=1e-6):
    """Area que encosta na mesa: triangulos no z minimo com normal para baixo."""
    z0 = min(v[2] for t in tris for v in t)
    tot = 0.0
    for a, b, c in tris:
        if max(a[2], b[2], c[2]) > z0 + tol:
            continue
        ux, uy, uz = (b[0]-a[0], b[1]-a[1], b[2]-a[2])
        vx, vy, vz = (c[0]-a[0], c[1]-a[1], c[2]-a[2])
        nz = ux*vy - uy*vx
        if nz < 0:
            tot += abs(nz) / 2
    return tot


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(base, 'stl', 'impressao')
    os.makedirs(out, exist_ok=True)

    c, H = g.corpo(1, SEG)
    g.grava_stl(os.path.join(out, 'pote-600-real.stl'), c.tris, 'pote-600-real')
    print(f"pote-600-real.stl        {len(c.tris):5d} tri | altura {H:.1f} mm | "
          f"contato na mesa {contato(c.tris):6.0f} mm2 -> brim de 10 mm obrigatorio")

    elev = g.ELEV[1]
    g.ELEV[1] = 0.0                       # fundo plano so para imprimir
    c2, _ = g.corpo(1, SEG)
    g.ELEV[1] = elev
    g.grava_stl(os.path.join(out, 'pote-600-fundoplano.stl'), c2.tris, 'pote-600-fundoplano')
    print(f"pote-600-fundoplano.stl  {len(c2.tris):5d} tri | altura {H:.1f} mm | "
          f"contato na mesa {contato(c2.tris):6.0f} mm2 "
          f"({contato(c2.tris)/contato(c.tris):.0f}x) -> imprime facil")

    tp = g.tampa_pp(SEG)
    g.grava_stl(os.path.join(out, 'tampa-pp.stl'), tp.tris, 'tampa-pe')
    inv_pp = [[(v[0], -v[1], -v[2]) for v in tri] for tri in tp.tris]
    print(f"tampa-pp.stl             {len(tp.tris):5d} tri | altura {altura(tp.tris):.1f} mm | "
          f"contato {contato(tp.tris):5.0f} mm2 de pe, {contato(inv_pp):5.0f} mm2 invertida"
          f" -> IMPRIME INVERTIDA (de pe apoia so na ponta das 2 travas)")

    tc = g.tampa_teca(SEG)
    g.grava_stl(os.path.join(out, 'tampa-teca.stl'), tc.tris, 'tampa-teca')
    inv = [[(v[0], -v[1], -v[2]) for v in tri] for tri in tc.tris]
    print(f"tampa-teca.stl           {len(tc.tris):5d} tri | altura {altura(tc.tris):.1f} mm | "
          f"contato {contato(tc.tris):5.0f} mm2 de pe, {contato(inv):5.0f} mm2 invertida"
          f" -> placa macica, tanto faz; em producao e CNC em teca")

    tr = g.tampa_correr(SEG)
    g.grava_stl(os.path.join(out, 'tampa-correr.stl'), tr.tris, 'tampa-correr')
    inv_tr = [[(v[0], -v[1], -v[2]) for v in tri] for tri in tr.tris]
    print(f"tampa-correr.stl         {len(tr.tris):5d} tri | altura {altura(tr.tris):.1f} mm | "
          f"contato {contato(tr.tris):5.0f} mm2 de pe, {contato(inv_tr):5.0f} mm2 invertida"
          f" -> INVERTIDA, mas com SUPORTE: apoia so nas 2 paredes da calha e o"
          f" deck fica 2,5 mm no ar")

    gv = g.gaveta(SEG)
    g.grava_stl(os.path.join(out, 'gaveta.stl'), gv.tris, 'gaveta')
    inv_gv = [[(v[0], -v[1], -v[2]) for v in tri] for tri in gv.tris]
    print(f"gaveta.stl               {len(gv.tris):5d} tri | altura {altura(gv.tris):.1f} mm | "
          f"contato {contato(gv.tris):5.0f} mm2 de pe, {contato(inv_gv):5.0f} mm2 invertida"
          f" -> INVERTIDA deixa o friso do 2o aro para cima, sem suporte")

    print(f"\nem {out}")
    print("O filete de TPE e o 2o aro nao se imprimem em FDM. Para o prototipo, use "
          "corda de silicone de 1,4 mm (filete) e de 1,2 mm (2o aro), cortada no "
          "comprimento e colada de topo.")
    print("A gaveta corre com 0,25 mm de folga por lado - folga de INJECAO. Em FDM "
          "ela vai sair apertada: imprima a gaveta a 99% em X e Y antes de lixar.")


if __name__ == '__main__':
    main()
