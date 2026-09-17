#!/usr/bin/env python3
"""
Variantes dos STL para PROTOTIPAR em FDM (nao sao as pecas de producao).

O corpo de producao apoia na mesa por um anel de 1,15 mm de largura - 421 mm2
para segurar uma peca de 62 mm de altura. E pouco para qualquer impressora.
Aqui saem duas versoes do 600 ml:

  pote-600-real.stl        a peca como e, fundo rebaixado. Imprima com brim.
  pote-600-fundoplano.stl  elevacao de fundo zerada -> 9.320 mm2 de contato,
                           22x mais. Muda so o volume interno (+19 ml), nao muda
                           encaixe, passo nem a prova da tampa. E a que eu
                           imprimiria primeiro.
  tampa.stl                a mesma da producao (imprime de cabeca para baixo).

Uso:  python3 gera-3d-impressao.py
"""
import os
import importlib.util

spec = importlib.util.spec_from_file_location("gera3d",
       os.path.join(os.path.dirname(os.path.abspath(__file__)), "gera-3d.py"))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

SEG = 24          # o dobro do padrao: canto mais liso no prototipo


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(base, 'stl', 'impressao')
    os.makedirs(out, exist_ok=True)

    c, H = g.corpo(1, SEG)
    g.grava_stl(os.path.join(out, 'pote-600-real.stl'), c.tris, 'pote-600-real')
    print(f"pote-600-real.stl        {len(c.tris):5d} tri | altura {H:.1f} mm | "
          f"contato na mesa  421 mm2 -> brim de 10 mm obrigatorio")

    elev = g.ELEV[1]
    g.ELEV[1] = 0.0                       # fundo plano so para imprimir
    c2, _ = g.corpo(1, SEG)
    g.ELEV[1] = elev
    g.grava_stl(os.path.join(out, 'pote-600-fundoplano.stl'), c2.tris, 'pote-600-fundoplano')
    print(f"pote-600-fundoplano.stl  {len(c2.tris):5d} tri | altura {H:.1f} mm | "
          f"contato na mesa 9320 mm2 -> imprime facil")

    t = g.tampa(SEG)
    g.grava_stl(os.path.join(out, 'tampa.stl'), t.tris, 'tampa')
    print(f"tampa.stl                {len(t.tris):5d} tri | altura 13,5 mm | "
          f"de cabeca para baixo, suporte so no poco da bandeja")

    print(f"\nem {out}")
    print("O aro de TPE nao se imprime em FDM. Para o prototipo, use O-ring de "
          "seccao 2,0 mm cortado e colado, ou corda de silicone de 2 mm.")


if __name__ == '__main__':
    main()
