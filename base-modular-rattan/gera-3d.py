#!/usr/bin/env python3
"""
Gera o 3D da base modular a partir de geometria.py.

Saidas:
  stl/modulo-alto.stl, stl/modulo-baixo.stl, stl/tampo.stl
      malha para VISUALIZAR (caixas e tubos sobrepostos, nao e uniao
      booleana). Abre em qualquer visualizador; NAO serve para fatiar nem para
      o projetista do molde - ele parte do CAD parametrico.
  pecas.json
      a mesma lista de elementos, lida pelo visualizador da pagina.

Uso:  python3 gera-3d.py [--seg 24]    (--seg = setores por tubo)
"""
import json, math, os, struct, sys
import geometria as g


def tri_caixa(x0, x1, y0, y1, z0, z1):
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    q = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (1, 2, 6, 5), (3, 0, 4, 7)]
    out = []
    for a, b, c, d in q:
        out += [(v[a], v[b], v[c]), (v[a], v[c], v[d])]
    return out


def tri_tubo(xc, yc, z0, z1, re, ri, n):
    out = []
    for k in range(n):
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        pe0 = (xc + re * math.cos(a0), yc + re * math.sin(a0))
        pe1 = (xc + re * math.cos(a1), yc + re * math.sin(a1))
        pi0 = (xc + ri * math.cos(a0), yc + ri * math.sin(a0))
        pi1 = (xc + ri * math.cos(a1), yc + ri * math.sin(a1))
        E0, E1 = (*pe0, z0), (*pe1, z0)
        E2, E3 = (*pe1, z1), (*pe0, z1)
        I0, I1 = (*pi0, z0), (*pi1, z0)
        I2, I3 = (*pi1, z1), (*pi0, z1)
        out += [(E0, E1, E2), (E0, E2, E3)]          # face externa
        out += [(I1, I0, I3), (I1, I3, I2)]          # face interna
        out += [(E3, E2, I2), (E3, I2, I3)]          # topo
        out += [(E1, E0, I0), (E1, I0, I1)]          # base
    return out


def normal(a, b, c):
    u = [b[i] - a[i] for i in range(3)]
    w = [c[i] - a[i] for i in range(3)]
    n = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
    m = math.sqrt(sum(x * x for x in n)) or 1.0
    return tuple(x / m for x in n)


def grava_stl(caminho, tris, nome):
    with open(caminho, "wb") as f:
        f.write(nome.encode()[:80].ljust(80, b" "))
        f.write(struct.pack("<I", len(tris)))
        for t in tris:
            f.write(struct.pack("<3f", *normal(*t)))
            for p in t:
                f.write(struct.pack("<3f", *p))
            f.write(b"\0\0")


def main():
    seg = int(sys.argv[sys.argv.index("--seg") + 1]) if "--seg" in sys.argv else 24
    aqui = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(aqui, "stl"), exist_ok=True)
    saida = {}
    for nome, f in g.PECAS.items():
        el = f()
        tris = []
        for e in el:
            tris += tri_caixa(*e[1:7]) if e[0] == "caixa" else tri_tubo(*e[1:7], seg)
        grava_stl(os.path.join(aqui, "stl", nome + ".stl"), tris, "base modular rattan " + nome)
        saida[nome] = [[e[0]] + [round(v, 3) if isinstance(v, float) else v for v in e[1:]]
                       for e in el]
        print(f"{nome:13s} {len(el):4d} elementos  {len(tris):6d} triangulos")
    with open(os.path.join(aqui, "pecas.json"), "w") as fp:
        json.dump(saida, fp, separators=(",", ":"))


if __name__ == "__main__":
    main()
