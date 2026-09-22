#!/usr/bin/env python3
"""Gera o SVG da elevacao da linha a partir de calculo-modular.py.

Desenhar a mao foi o que deixou o degrau do pe em 3,55 no desenho e 3,86 no
calculo, na revisao 5. Desenho com cota que nao sai do calculo mente cedo ou
tarde.
"""
import importlib.util, sys, os
CALC = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'calculo-modular.py')
spec = importlib.util.spec_from_file_location('cm', CALC)
cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)

potes = cm.linha(cm.footprint())
p0 = potes[0]
COLAR, CORPO = p0['colar_l'], p0['corpo_l']
Y0, PASSO, X0, TH = 300.0, 152.0, 60.0, 11.0

br = lambda v: ('%.1f' % v).replace('.', ',')
o = []
a = o.append
a('      <svg viewBox="0 0 700 340" role="img" aria-label="Elevacao em escala dos '
  'quatro potes de parede reta com colar de borda e rodape reto, sobre a malha '
  'modular de 60 milimetros">')
a('        <defs>')
a('          <pattern id="hatch" width="6" height="6" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">')
a('            <line x1="0" y1="0" x2="0" y2="6" stroke="var(--pp)" stroke-width="1.1" opacity=".45"/>')
a('          </pattern>')
a('        </defs>')
a('')
a('        <g stroke="var(--line)" stroke-width=".8" stroke-dasharray="5 4">')
a('          <line x1="55" y1="240" x2="688" y2="240"/><line x1="55" y1="180" x2="688" y2="180"/>')
a('          <line x1="55" y1="120" x2="688" y2="120"/><line x1="55" y1="60"  x2="688" y2="60"/>')
a('        </g>')
a('        <line x1="55" y1="300" x2="688" y2="300" stroke="var(--ink)" stroke-width="1.4"/>')
a('        <g font-family="IBM Plex Mono, monospace" font-size="10.5" fill="var(--cota)">')
a('          <text x="51" y="244" text-anchor="end">60</text><text x="51" y="184" text-anchor="end">120</text>')
a('          <text x="51" y="124" text-anchor="end">180</text><text x="51" y="64" text-anchor="end">240</text>')
a('          <text x="51" y="304" text-anchor="end">0</text>')
a('        </g>')
a('')

rot = {1: '600 ml', 2: '1,2 L', 3: '1,8 L', 4: '2,4 L'}
for p in potes:
    x = X0 + (p['n'] - 1) * PASSO
    H = p['H']
    yt = Y0 - H
    z_col = H - cm.COLAR_H
    base = p['base_ext']
    tap = (CORPO - base) / 2                       # o que a saida estreita
    # contorno, no sentido horario: fundo reto -> corpo -> colar -> topo
    # arredondado -> colar -> corpo -> fundo. x e a face ESQUERDA do corpo.
    pts = [(x + tap,                 Y0),
           (x,                       Y0 - z_col),
           (x - cm.REB,              Y0 - z_col),   # aresta de engate da trava
           (x - cm.REB,              yt + 1.0),
           (x - cm.REB + 1.0,        yt),           # arredondamento de cima
           (x + CORPO + cm.REB - 1.0, yt),
           (x + CORPO + cm.REB,      yt + 1.0),
           (x + CORPO + cm.REB,      Y0 - z_col),
           (x + CORPO,               Y0 - z_col),
           (x + CORPO - tap,         Y0)]
    d = 'M ' + ' L '.join('%.1f %.1f' % q for q in pts) + ' Z'
    a('        <!-- %s -->' % rot[p['n']])
    a('        <path d="%s" fill="url(#hatch)" stroke="var(--pp)" stroke-width="1.3"/>' % d)
    # tampa, rente ao colar
    a('        <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="var(--verde)"/>'
      % (x - cm.REB, yt - TH - 1.0, CORPO + 2 * cm.REB, TH))
    a('        <text x="%.1f" y="320" text-anchor="middle" font-family="Barlow Condensed, sans-serif" '
      'font-weight="700" font-size="15" fill="var(--ink)">%s</text>' % (x + CORPO / 2, rot[p['n']]))
    a('        <text x="%.1f" y="332" text-anchor="middle" font-family="IBM Plex Mono, monospace" '
      'font-size="9.5" fill="var(--muted)">%d M · %s mm</text>' % (x + CORPO / 2, p['n'], br(H)))
    a('')

# cota do colar sobre o maior
x4 = X0 + 3 * PASSO
a('        <g stroke="var(--cota)" stroke-width="1">')
a('          <line x1="%.1f" y1="40" x2="%.1f" y2="40"/><line x1="%.1f" y1="36" x2="%.1f" y2="44"/>'
  '<line x1="%.1f" y1="36" x2="%.1f" y2="44"/>'
  % (x4 - cm.REB, x4 + CORPO + cm.REB, x4 - cm.REB, x4 - cm.REB,
     x4 + CORPO + cm.REB, x4 + CORPO + cm.REB))
a('        </g>')
a('        <text x="%.1f" y="32" text-anchor="middle" font-family="IBM Plex Mono, monospace" '
  'font-size="10" fill="var(--cota)">colar %s mm</text>' % (x4 + CORPO / 2, br(COLAR)))
a('        <text x="60" y="32" font-family="IBM Plex Mono, monospace" font-size="10" '
  'fill="var(--muted)">corpo %s mm · rodapé reto (IML)</text>' % br(CORPO))
a('      </svg>')
print('\n'.join(o))
