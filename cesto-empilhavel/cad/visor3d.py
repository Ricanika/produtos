#!/usr/bin/env python3
"""Atualiza cad/visor3d.html a partir do solido -- malha e numeros.

A pagina em si e escrita a mao (WebGL2 proprio, sem biblioteca externa, para
ser autossuficiente E testavel no sandbox). O que este script faz e o que nao
se pode fazer a mao: reempacotar a MALHA e reescrever os NUMEROS medidos, para
que o visor nao envelheca calado a cada mudanca no modelo.

Formato da malha (o mesmo que decodifica() na pagina espera):
    float32 min[3] | float32 escala[3] | uint32 nv | uint32 nf
    uint16 posicoes quantizadas[nv*3] | uint16 indices[nf*3]
Quantizar em uint16 da 1/65535 da caixa -- 0,003 mm nesta peca -- e o arquivo
cai de 3,6 MB de STL para ~650 kB de binario. Os indices tambem sao uint16,
entao nv tem de caber em 65536: e por isso que os vertices sao SOLDADOS antes.

Uso:  python3 visor3d.py
"""
import base64
import os
import re
import struct

import numpy as np
import trimesh
from build123d import Box, Pos

import modelo3d as M

DEST = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(DEST, "visor3d.html")
STL = os.path.join(DEST, "cesto-aba.stl")


def vg(x, casas=1):
    return f"{x:.{casas}f}".replace(".", ",")


def empacota(m):
    """Solda os vertices, quantiza em uint16 e devolve o base64."""
    m = m.copy()
    m.merge_vertices()
    v, f = np.asarray(m.vertices, float), np.asarray(m.faces, np.uint32)
    if len(v) > 65535:
        raise SystemExit(f"{len(v)} vertices: nao cabe em indice uint16")
    mn, mx = v.min(0), v.max(0)
    esc = np.where(mx > mn, (mx - mn) / 65535.0, 1.0)
    q = np.rint((v - mn) / esc).astype(np.uint16)
    buf = struct.pack("<6f2I", *mn, *esc, len(v), len(f))
    buf += q.tobytes() + f.astype(np.uint16).tobytes()
    print(f"malha: {len(v)} vertices, {len(f)} faces, {len(buf)/1024:.0f} kB "
          f"(STL {os.path.getsize(STL)/1024:.0f} kB) · resolucao "
          f"{esc.max():.4f} mm")
    return base64.b64encode(buf).decode("ascii")


def medidas():
    """Os numeros que vao na pagina, medidos no solido -- nao digitados."""
    M.set_draft(12.0)
    p, n = M.cesto(aba=True)

    def vol(a, b):
        try:
            return (a & b).volume
        except Exception:
            return 0.0

    def passo(dy, tol=0.01):
        lo, hi = 0.0, 145.0
        while hi - lo > tol:
            mid = (lo + hi) / 2
            if vol(p, Pos(0, dy, mid) * p) > 2.0:
                lo = mid
            else:
                hi = mid
        return hi

    pn, pe = passo(0.0), passo(M.DESLOC)
    inter = p & (Pos(0, M.DESLOC, pe - 0.3) * p)
    ap = sorted((s.volume / 0.3 for s in inter.solids() if s.volume > 0.002),
                reverse=True)
    return dict(pn=pn, pe=pe, peso=p.volume * M.RHO, cap=M.capacidade(),
                furos=n, apoios=ap, interf=vol(p, Pos(0, M.DESLOC, 130.0) * p))


def troca(s, velho, novo, o_que):
    if velho not in s:
        raise SystemExit(f"nao achei no html: {o_que} ({velho[:60]!r})")
    print(f"  {o_que}: {velho[:58]}  ->  {novo[:58]}")
    return s.replace(velho, novo, 1)


def main():
    d = medidas()
    b64 = empacota(trimesh.load(STL))
    s = open(HTML).read()

    s = re.sub(r"var MALHA = '[^']*';", "var MALHA = '" + b64 + "';", s,
               count=1)
    print("  malha embutida trocada")

    # os numeros. Cada um formatado sozinho: replace(".", ",") em paragrafo
    # transforma ponto de frase em virgula (ja aconteceu duas vezes).
    s = re.sub(r"var PASSO_ENCAIXE = [\d.]+, PASSO_PILHA = [\d.]+",
               f"var PASSO_ENCAIXE = {d['pn']:.1f}, PASSO_PILHA = "
               f"{d['pe']:.1f}", s, count=1)
    s = re.sub(r"saída 12°/lado · [\d,]+ g",
               f"saída 12°/lado · {vg(d['peso'])} g", s, count=1)
    s = re.sub(r"\['peso', '[\d,]+ g'\]", f"['peso', '{vg(d['peso'])} g']", s,
               count=1)
    s = re.sub(r"\['capacidade', '[\d,]+ L'\]",
               f"['capacidade', '{vg(d['cap'], 2)} L']", s, count=1)
    s = re.sub(r"\['contato', '\d+ mm²'\]",
               f"['contato', '{sum(d['apoios']):.0f} mm²']", s, count=1)
    s = re.sub(r"\['passo', '[\d,]+ mm'\], \['desloca em y'",
               f"['passo', '{vg(d['pe'])} mm'], ['desloca em y'", s, count=1)
    s = re.sub(r"\['passo', '[\d,]+ mm'\], \['6 peças', '\d+ mm'\], "
               r"\['12 peças', '\d+ mm'\]",
               f"['passo', '{vg(d['pn'])} mm'], "
               f"['6 peças', '{132.5 + 5 * d['pn']:.0f} mm'], "
               f"['12 peças', '{132.5 + 11 * d['pn']:.0f} mm']", s, count=1)
    s = re.sub(r"\d+ peças em \d+ mm de caixa",
               f"12 peças em {132.5 + 11 * d['pn']:.0f} mm de caixa", s)
    s = re.sub(r"[\d,]+ mm³ de interferência a [\d,]+ mm",
               f"{d['interf']:.3f}".replace(".", ",") +
               f" mm³ de interferência a {vg(d['pe'])} mm", s, count=1)

    open(HTML, "w").write(s)
    print(f"visor3d.html: {os.path.getsize(HTML)/1024:.0f} kB")


if __name__ == "__main__":
    main()
