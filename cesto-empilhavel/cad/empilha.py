#!/usr/bin/env python3
"""Mede, NO SOLIDO, o passo de empilhamento e de encaixe.

Busca binaria do menor deslocamento vertical em que duas copias da peca nao
se interpenetram -- na mesma orientacao e girada 180 graus. E a unica forma
honesta de saber se a peca encaixa: a conta da conicidade ignora os bercos,
o chanfro do pe e o chanfro de topo.
"""
import sys

from build123d import Pos, Rot

import modelo3d as M


def passo(p, girada=False, lo=0.0, hi=140.0, tol=0.25, tol_v=2.0):
    q = (Rot(0, 0, 180) * p) if girada else p
    while hi - lo > tol:
        mid = (lo + hi) / 2
        v = (p & (Pos(0, 0, mid) * q)).volume
        if v > tol_v:
            lo = mid
        else:
            hi = mid
    return hi


def main(letras):
    for L in letras:
        acopl = None if L == "0" else L
        kw = {}
        if L == "0s":
            acopl, kw = None, {"h_rim": M.H_BANDA}
        p, _ = M.cesto(acopl, **kw)
        pe = passo(p, False)
        pg = passo(p, True)
        print(f"{L:3}  peso {p.volume*M.RHO:6.1f} g | "
              f"passo mesma orientacao {pe:6.1f} mm | girada 180 {pg:6.1f} mm")


if __name__ == "__main__":
    main(sys.argv[1:] or ["D"])
