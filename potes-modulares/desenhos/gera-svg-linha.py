#!/usr/bin/env python3
"""Gera o SVG da elevacao da linha a partir de calculo-modular.py.

Desenhar a mao foi o que deixou o degrau do pe em 3,55 no desenho e 3,86 no
calculo, na revisao 5. Desenho com cota que nao sai do calculo mente cedo ou
tarde.
"""
import importlib.util, os
CALC = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'calculo-modular.py')
spec = importlib.util.spec_from_file_location('cm', CALC)
cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)

potes = cm.linha(cm.footprint())
p0 = potes[0]
COLAR, CORPO = p0['colar_l'], p0['corpo_l']
PERNA = p0['boca'] + 2 * cm.W_IN          # face externa da perna de dentro
Y0, PASSO, X0, TH = 300.0, 152.0, 52.0, 9.0

br = lambda v: ('%.1f' % v).replace('.', ',')
o = []
a = o.append
a('      <svg viewBox="0 0 700 340" role="img" aria-label="Elevacao em escala dos '
  'quatro potes de parede reta com borda alta e oca e rodape reto, sobre a malha '
  'modular de 60 milimetros">')
a('        <defs>')
a('          <pattern id="hatch" width="6" height="6" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">')
a('            <line x1="0" y1="0" x2="0" y2="6" stroke="var(--pp)" stroke-width="1.1" opacity=".45"/>')
a('          </pattern>')
a('        </defs>')
a('')
a('        <g stroke="var(--line)" stroke-width=".8" stroke-dasharray="5 4">')
a('          <line x1="47" y1="240" x2="688" y2="240"/><line x1="47" y1="180" x2="688" y2="180"/>')
a('          <line x1="47" y1="120" x2="688" y2="120"/><line x1="47" y1="60"  x2="688" y2="60"/>')
a('        </g>')
a('        <line x1="47" y1="300" x2="688" y2="300" stroke="var(--ink)" stroke-width="1.4"/>')
a('        <g font-family="IBM Plex Mono, monospace" font-size="10.5" fill="var(--cota)">')
a('          <text x="43" y="244" text-anchor="end">60</text><text x="43" y="184" text-anchor="end">120</text>')
a('          <text x="43" y="124" text-anchor="end">180</text><text x="43" y="64" text-anchor="end">240</text>')
a('          <text x="43" y="304" text-anchor="end">0</text>')
a('        </g>')
a('')

rot = {1: '600 ml', 2: '1,2 L', 3: '1,8 L', 4: '2,4 L'}
for p in potes:
    x = X0 + (p['n'] - 1) * PASSO          # x e a face ESQUERDA do corpo reto
    H = p['H']
    yt = Y0 - H
    y_body = Y0 - p['z_body']              # topo da parede reta
    y_bord = Y0 - p['z_bord']              # fim do flare / comeco da borda
    y_saia = yt + cm.SAIA_H                # aresta de baixo da saia
    base = p['base_ext']
    tap = (CORPO - base) / 2
    dp = (PERNA - CORPO) / 2               # quanto o flare abre
    ds = (COLAR - CORPO) / 2               # quanto a saia sobressai
    # contorno horario: fundo reto -> parede -> flare -> perna -> saia ->
    # topo arredondado -> saia -> perna -> flare -> parede -> fundo
    pts = [(x + tap,              Y0),
           (x,                    y_body),
           (x - dp,               y_bord),
           (x - dp,               y_saia),
           (x - ds,               y_saia),
           (x - ds,               yt + 1.2),
           (x - ds + 1.2,         yt),
           (x + CORPO + ds - 1.2, yt),
           (x + CORPO + ds,       yt + 1.2),
           (x + CORPO + ds,       y_saia),
           (x + CORPO + dp,       y_saia),
           (x + CORPO + dp,       y_bord),
           (x + CORPO,            y_body),
           (x + CORPO - tap,      Y0)]
    d = 'M ' + ' L '.join('%.1f %.1f' % q for q in pts) + ' Z'
    a('        <!-- %s -->' % rot[p['n']])
    a('        <path d="%s" fill="url(#hatch)" stroke="var(--pp)" stroke-width="1.3"/>' % d)
    # o canal, tracejado, dos dois lados
    for xx in (x - ds + cm.W_SAIA, x + CORPO + ds - cm.W_SAIA):
        a('        <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--cota)" '
          'stroke-width=".7" stroke-dasharray="3 2"/>' % (xx, yt + cm.TOPO_T, xx, y_saia))
    # tampa, pousada no topo da borda
    a('        <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="var(--verde)"/>'
      % (x - ds - cm.PP_DECK_FORA, yt - TH, CORPO + 2 * ds + 2 * cm.PP_DECK_FORA, TH))
    a('        <text x="%.1f" y="320" text-anchor="middle" font-family="Barlow Condensed, sans-serif" '
      'font-weight="700" font-size="15" fill="var(--ink)">%s</text>' % (x + CORPO / 2, rot[p['n']]))
    a('        <text x="%.1f" y="332" text-anchor="middle" font-family="IBM Plex Mono, monospace" '
      'font-size="9.5" fill="var(--muted)">%d M · %s mm</text>' % (x + CORPO / 2, p['n'], br(H)))
    a('')

# cota da borda sobre o maior
x4 = X0 + 3 * PASSO
ds = (COLAR - CORPO) / 2
a('        <g stroke="var(--cota)" stroke-width="1">')
a('          <line x1="%.1f" y1="40" x2="%.1f" y2="40"/><line x1="%.1f" y1="36" x2="%.1f" y2="44"/>'
  '<line x1="%.1f" y1="36" x2="%.1f" y2="44"/>'
  % (x4 - ds, x4 + CORPO + ds, x4 - ds, x4 - ds, x4 + CORPO + ds, x4 + CORPO + ds))
a('        </g>')
a('        <text x="%.1f" y="32" text-anchor="middle" font-family="IBM Plex Mono, monospace" '
  'font-size="10" fill="var(--cota)">borda %s mm</text>' % (x4 + CORPO / 2, br(COLAR)))
a('        <text x="52" y="32" font-family="IBM Plex Mono, monospace" font-size="10" '
  'fill="var(--muted)">corpo reto %s mm · rodapé reto (IML)</text>' % br(CORPO))
a('        <text x="52" y="44" font-family="IBM Plex Mono, monospace" font-size="9.5" '
  'fill="var(--muted)">borda %s mm de altura + flare %s · saia livre desce %s</text>'
  % (br(cm.BORDA_H), br(cm.FLARE), br(cm.SAIA_H)))
a('      </svg>')
print('\n'.join(o))
