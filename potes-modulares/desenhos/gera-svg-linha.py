#!/usr/bin/env python3
"""Gera o SVG da elevacao da linha a partir de calculo-modular.py.
Desenhar a mao foi o que deixou o degrau em 3,55 no desenho e 3,86 no calculo."""
import importlib.util, sys, os
CALC = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'calculo-modular.py')
spec = importlib.util.spec_from_file_location('cm', CALC)
cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)

potes = cm.linha(cm.footprint())
p0 = potes[0]
PE = cm.pe_l(p0['ext_l'])
W  = p0['ext_l']; ABA = cm.ABA_W; TAMPA_W = W + 2*ABA
Y0 = 300.0           # linha de base
PASSO = 150.0        # espacamento entre potes no desenho
X0 = 62.0
TH = 12.5            # altura visual da tampa

br = lambda v: ('%.1f' % v).replace('.', ',')   # decimal brasileiro

o = []
a = o.append
a('      <svg viewBox="0 0 700 340" role="img" aria-label="Elevacao em escala dos '
  'quatro potes de parede reta sobre a malha modular de 60 milimetros, com vista de '
  'topo mostrando os cantos arredondados de R%.0f">' % cm.R_EXT)
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
# ---- vista de topo, no espaco livre acima do menor ----
tv_y = 96.0
a('        <!-- vista de topo, no espaco livre acima do menor -->')
a('        <g>')
a('          <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" ry="%.1f" '
  'fill="url(#hatch)" stroke="var(--pp)" stroke-width="1.3"/>'
  % (X0, tv_y, W, p0['ext_w'], cm.R_EXT, cm.R_EXT))
pe_w = PE - (p0['ext_l'] - p0['ext_w'])
r_pe = cm.R_EXT - (W - PE)/2
a('          <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" ry="%.1f" '
  'fill="none" stroke="var(--cota)" stroke-width=".9" stroke-dasharray="4 3"/>'
  % (X0 + (W-PE)/2, tv_y + (p0['ext_w']-pe_w)/2, PE, pe_w, max(r_pe,0.5), max(r_pe,0.5)))
a('          <text x="%.1f" y="%.1f" text-anchor="middle" font-family="IBM Plex Mono, monospace" '
  'font-size="10" fill="var(--muted)">VISTA DE TOPO · R%.0f de canto</text>'
  % (X0 + W/2, tv_y - 8, cm.R_EXT))
a('          <text x="%.1f" y="%.1f" text-anchor="middle" font-family="IBM Plex Mono, monospace" '
  'font-size="9.5" fill="var(--cota)">pé embutido %s × %s</text>'
  % (X0 + W/2, tv_y + p0['ext_w'] + 15, br(PE), br(pe_w)))
a('        </g>')
a('')
# ---- elevacoes ----
rot = {1:'600 ml', 2:'1,2 L', 3:'1,8 L', 4:'2,4 L'}
for p in potes:
    x  = X0 + (p['n']-1)*PASSO
    H  = p['H']
    yt = Y0 - H
    tap = (p['ext_l'] - p['ext_base'])/2
    deg = (p['ext_base'] - PE)/2
    ype = Y0 - cm.PE_H
    d = ('M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f '
         'L %.1f %.1f L %.1f %.1f L %.1f %.1f Z' % (
        x, yt,  x+tap, ype,  x+tap+deg, ype,  x+tap+deg, Y0,
        x+tap+deg+PE, Y0,  x+tap+deg+PE, ype,  x+p['ext_l']-tap, ype,  x+p['ext_l'], yt))
    a('        <!-- %s -->' % rot[p['n']])
    a('        <path d="%s" fill="url(#hatch)" stroke="var(--pp)" stroke-width="1.3"/>' % d)
    a('        <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="var(--verde)"/>'
      % (x-ABA, yt-TH-1.5, TAMPA_W, TH))
    a('        <text x="%.1f" y="320" text-anchor="middle" font-family="Barlow Condensed, sans-serif" '
      'font-weight="700" font-size="15" fill="var(--ink)">%s</text>' % (x+W/2, rot[p['n']]))
    a('        <text x="%.1f" y="332" text-anchor="middle" font-family="IBM Plex Mono, monospace" '
      'font-size="9.5" fill="var(--muted)">%d M · %s mm</text>'
      % (x+W/2, p['n'], br(H)))
    a('')
# cota da tampa sobre o maior
x4 = X0 + 3*PASSO
a('        <g stroke="var(--cota)" stroke-width="1">')
a('          <line x1="%.1f" y1="42" x2="%.1f" y2="42"/><line x1="%.1f" y1="38" x2="%.1f" y2="46"/>'
  '<line x1="%.1f" y1="38" x2="%.1f" y2="46"/>'
  % (x4-ABA, x4-ABA+TAMPA_W, x4-ABA, x4-ABA, x4-ABA+TAMPA_W, x4-ABA+TAMPA_W))
a('        </g>')
a('        <text x="%.1f" y="34" text-anchor="middle" font-family="IBM Plex Mono, monospace" '
  'font-size="10" fill="var(--cota)">tampa %s mm</text>' % (x4-ABA+TAMPA_W/2, br(TAMPA_W)))
a('      </svg>')
print('\n'.join(o))
