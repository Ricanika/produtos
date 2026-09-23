#!/usr/bin/env python3
"""
Gera o 3D da base modular a partir de geometria.py (via solidos.malha).

Saidas:
  stl/modulo-alto.stl, stl/modulo-baixo.stl, stl/tampo.stl
      malha para VISUALIZAR: cada elemento e um solido fechado, mas eles se
      sobrepoem (nao e uniao booleana). Abre em qualquer visualizador; NAO
      serve para fatiar nem para o projetista do molde - ele parte do CAD.
  malhas.json
      a mesma malha para a pagina: posicoes em Float32 e normais em Int8,
      em base64. As normais sao suaves nas curvas e vivas nas arestas de
      caixa (vinco de 35 graus, calculado por elemento).

Uso:  python3 gera-3d.py
"""
import base64, json, math, os, struct
import numpy as np
import geometria as g
import solidos as s


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
    aqui = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(aqui, "stl"), exist_ok=True)
    saida = {}
    for nome, f in g.PECAS.items():
        tris, nrm = [], []
        for e in f():
            t = s.malha(e)
            tris += t
            nrm.append(s.normais_suaves(t))
        grava_stl(os.path.join(aqui, "stl", nome + ".stl"), tris, "base modular rattan " + nome)
        pos = np.array(tris, dtype=np.float32).reshape(-1)
        nor = np.clip(np.round(np.concatenate(nrm).reshape(-1) * 127), -127, 127).astype(np.int8)
        saida[nome] = {"pos": base64.b64encode(pos.tobytes()).decode(),
                       "nor": base64.b64encode(nor.tobytes()).decode()}
        print(f"{nome:13s} {len(tris):6d} triangulos")
    with open(os.path.join(aqui, "malhas.json"), "w") as fp:
        json.dump(saida, fp, separators=(",", ":"))


if __name__ == "__main__":
    main()
