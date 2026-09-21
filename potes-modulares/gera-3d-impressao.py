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
  tampa.stl                perfil plug (o da tampa de teca). Imprime invertida.
  tampa-pe.stl             sobretampa de encaixe externo, 100% PE.

Uso:  python3 gera-3d-impressao.py
"""
import os
import importlib.util

spec = importlib.util.spec_from_file_location("gera3d",
       os.path.join(os.path.dirname(os.path.abspath(__file__)), "gera-3d.py"))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

SEG = 24          # o dobro do padrao: canto mais liso no prototipo


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

    tp = g.tampa_pe(SEG)
    g.grava_stl(os.path.join(out, 'tampa-pe.stl'), tp.tris, 'tampa-pe')
    inv_pe = [[(v[0], -v[1], -v[2]) for v in tri] for tri in tp.tris]
    print(f"tampa-pe.stl             {len(tp.tris):5d} tri | altura 10,8 mm | "
          f"contato {contato(tp.tris):5.0f} mm2 de pe, {contato(inv_pe):5.0f} mm2 invertida")

    t = g.tampa(SEG)
    g.grava_stl(os.path.join(out, 'tampa.stl'), t.tris, 'tampa')
    inv = [[(v[0], -v[1], -v[2]) for v in tri] for tri in t.tris]
    print(f"tampa.stl                {len(t.tris):5d} tri | altura 13,5 mm | "
          f"contato {contato(t.tris):5.0f} mm2 de pe, {contato(inv):5.0f} mm2 "
          f"invertida -> imprime invertida, suporte so no poco da bandeja")

    print(f"\nem {out}")
    print("O aro de TPE nao se imprime em FDM. Para o prototipo, use O-ring de "
          "seccao 2,0 mm cortado e colado, ou corda de silicone de 2 mm.")


if __name__ == '__main__':
    main()
