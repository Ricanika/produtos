"""Monta visualizador-3d.html a partir de malhas.json (saida de geometria.py).

As malhas vao embutidas em binario: vertices int16 em centesimo de mm,
indices uint16 (ou uint32 se a peca passar de 65535 vertices), base64.
"""
import base64
import json
import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(AQUI, 'malhas.json')))
R = json.load(open(os.path.join(AQUI, 'relatorio.json')))

pecas = {}
for nome, d in M.items():
    if not isinstance(d, dict):
        continue
    v = np.array(d['v'], dtype='<i2')
    i = np.array(d['i'])
    tipo = 'u16' if i.max() < 65536 else 'u32'
    i = i.astype('<u2' if tipo == 'u16' else '<u4')
    pecas[nome] = dict(v=base64.b64encode(v.tobytes()).decode(),
                       i=base64.b64encode(i.tobytes()).decode(), t=tipo)

# corte 2D da vedacao, no meio de um lado, a partir dos MESMOS perfis
import geometria as G


def corte_svg():
    H = G.ALTURAS[0]
    u0, u1, z0, z1 = 50.0, 74.0, -19.0, 5.0
    E = 34.0                       # px por mm
    W, Hh = (u1 - u0) * E, (z1 - z0) * E
    X = lambda u: (u - u0) * E
    Y = lambda z: (z1 - z) * E
    def poli(P, dz, cls):
        pts = ' '.join(f'{X(p[1]):.1f},{Y(p[2] + dz):.1f}' for p in P)
        return f'<polygon class="{cls}" points="{pts}"/>'
    corpo = G.corpo(H, 8)[1]
    partes = [poli(corpo, -H, 's-san'), poli(G.tampa_pp(8)[1], 0, 's-pp'), poli(G.fita(8)[1], 0, 's-tpe')]
    zf = -4.0
    uf = G.u_int(zf) - 0.9
    rot = [
        (G.U_I + G.T + 0.8, -12.0, 'SAN 2,0 · saída 2°', 'start'),
        (50.4, 1.0, 'PP', 'start'),
        (50.4, zf + 0.3, 'fita TPE 2 × 10', 'start'),
        (50.4, G.Z_FENDA_PISO + 0.3, 'fenda da fita', 'start'),
        (G.U_BORDA - 2.6, 4.0, 'aba 3,0 sobre a borda', 'middle'),
        (G.U_I + G.T + 0.8, -17.0, 'veda na aleta · 0,15', 'start'),
    ]
    txt = ''.join(f'<text x="{X(u):.1f}" y="{Y(z):.1f}" text-anchor="{a}">{t}</text>' for u, z, t, a in rot)
    return (f'<svg viewBox="0 0 {W:.0f} {Hh:.0f}" role="img" aria-label="Corte da borda, da tampa e da fita, escala 5:1">'
            f'<defs><clipPath id="jan"><rect width="{W:.0f}" height="{Hh:.0f}"/></clipPath></defs>'
            f'<g clip-path="url(#jan)">{"".join(partes)}</g>'
            f'<line class="s-borda" x1="0" x2="{W:.0f}" y1="{Y(0):.1f}" y2="{Y(0):.1f}"/>{txt}</svg>')


dados = dict(pecas=pecas, alturas=M['alturas'], passo=M['passo'], rel=R)
html = open(os.path.join(AQUI, 'visualizador-modelo.html')).read()
html = html.replace('__CORTE__', corte_svg())
html = html.replace('__DADOS__', json.dumps(dados, separators=(',', ':'), ensure_ascii=False))
open(os.path.join(AQUI, 'visualizador-3d.html'), 'w').write(html)
print('visualizador-3d.html', len(html) // 1024, 'KB')
