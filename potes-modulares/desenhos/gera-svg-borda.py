#!/usr/bin/env python3
"""Corte ampliado da borda: colar, trava, friso com filete e plano modular.

Tudo sai de calculo-modular.py. So a metade direita da secao.
"""
import importlib.util, math, os
CALC = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'calculo-modular.py')
spec = importlib.util.spec_from_file_location('cm', CALC)
cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)

p = cm.linha(cm.footprint())
p0 = p[0]
T = math.tan(math.radians(cm.SAIDA))
h = lambda w: w / 2.0                      # meia-largura

COLAR, CORPO, BOCA = p0['colar_l'], p0['corpo_l'], p0['boca']
PLUG   = BOCA - 2 * cm.PLUG_FOLGA
FRISO  = PLUG - 2 * cm.FRISO_PROF
FILETE = PLUG - 2 * cm.FRISO_PROF + 2 * cm.FILETE_D
BANDEJA = PLUG - 2 * cm.PE_PLUG_PAR
BASE600 = p0['base_ext']
DECK_O = COLAR + 2 * 3.10
ABA_I  = COLAR + 2 * 0.30
ABA_O  = ABA_I + 2 * cm.ABA_T
FARPA  = COLAR - 2 * 1.85

S, R0, Z0 = 13.0, 65.0, 250.0
X = lambda w: (h(w) - R0) * S + 44
Y = lambda z: Z0 - z * S
pt = lambda w, z: '%.1f %.1f' % (X(w), Y(z))
CUT = 128.0                                 # o quadro corta aqui, a esquerda

o = []; a = o.append
a('      <svg viewBox="0 0 770 420" role="img" aria-label="Corte ampliado da borda: '
  'colar liso, aresta de engate da trava, friso com filete de TPE e o plano modular">')
a('        <defs>')
a('          <pattern id="hb" width="5" height="5" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">')
a('            <line x1="0" y1="0" x2="0" y2="5" stroke="var(--pp)" stroke-width="1" opacity=".5"/>')
a('          </pattern>')
a('        </defs>')

# ---- tampa PE (desenhada primeiro; os contornos dos potes ficam por cima) ----
seq = [(CUT, -cm.BASE_T), (BANDEJA, -cm.BASE_T), (BANDEJA, cm.PE_DECK),
       (DECK_O, cm.PE_DECK), (DECK_O, 0.0), (ABA_I, 0.0), (PLUG, 0.0),
       (PLUG, -3.0), (FRISO, -3.0), (FRISO, -4.4), (PLUG, -4.4),
       (PLUG, -5.5), (PLUG - 2.0, -6.0), (BANDEJA, -6.0),
       (BANDEJA, -cm.BASE_T - cm.PE_DECK), (CUT, -cm.BASE_T - cm.PE_DECK)]
d = 'M ' + ' L '.join(pt(w, z) for w, z in seq) + ' Z'
a('        <path d="%s" fill="var(--verde)" opacity=".55"/>' % d)
a('        <path d="%s" fill="none" stroke="var(--verde)" stroke-width="1.5"/>' % d)

# aba de trava, com a farpa sob o colar
aba = [(ABA_I, 0.5), (ABA_I, -cm.COLAR_H), (FARPA, -cm.COLAR_H - 0.6),
       (ABA_I, -cm.COLAR_H - 1.6), (ABA_I, -11.0), (ABA_O, -11.0), (ABA_O, 0.5)]
da = 'M ' + ' L '.join(pt(w, z) for w, z in aba) + ' Z'
a('        <path d="%s" fill="var(--verde)" opacity=".75"/>' % da)
a('        <path d="%s" fill="none" stroke="var(--verde)" stroke-width="1.5"/>' % da)

# filete de TPE, na medida livre (invade 0,20 mm a boca - e a interferencia)
fl = [(FRISO, -3.0), (FILETE, -3.0), (FILETE, -4.4), (FRISO, -4.4)]
a('        <path d="M %s Z" fill="var(--tpe)"/>' % ' L '.join(pt(w, z) for w, z in fl))

# ---- pote de baixo: boca, colar e o rebaixo da trava ----
pb = [(BOCA, 0.0), (COLAR - 2 * 0.5, 0.0), (COLAR, -0.5),
      (COLAR, -cm.COLAR_H), (CORPO, -cm.COLAR_H), (CORPO, -16.0),
      (CORPO - 2 * cm.WALL[1], -16.0), (CORPO - 2 * cm.WALL[1], -cm.COLAR_H),
      (BOCA - 2 * cm.COLAR_H * T, -cm.COLAR_H)]
a('        <path d="M %s Z" fill="url(#hb)" stroke="var(--pp)" stroke-width="1.8"/>'
  % ' L '.join(pt(w, z) for w, z in pb))

# ---- pote de cima: fundo RETO pousando na bandeja ----
pc = [(BASE600, -cm.BASE_T), (BASE600, 12.0), (CUT, 12.0), (CUT, -cm.BASE_T)]
a('        <path d="M %s Z" fill="url(#hb)" stroke="var(--pp)" stroke-width="1.8"/>'
  % ' L '.join(pt(w, z) for w, z in pc))

# ---- chamadas ----
CH = [(COLAR, -cm.COLAR_H, 74, 'ARESTA DE ENGATE',
       'face de baixo do colar, %.2f mm/lado' % (cm.REB - cm.COLAR_H * T),
       'nao e canaleta: o molde abre sem gaveta'),
      (FARPA, -cm.COLAR_H - 0.6, 140, 'FARPA DA ABA',
       'avanca 1,85 mm sob o colar', 'sao 6 abas; cada uma fecha com ~2 kgf'),
      (FILETE, -3.7, 206, 'FILETE DE TPE',
       'comprime %.2f mm/lado contra a boca' % (cm.FILETE_SOB - cm.PLUG_FOLGA),
       'o MESMO filete na teca, num friso 2,0 mm mais fundo'),
      (BANDEJA, -cm.BASE_T, 278, 'PLANO MODULAR',
       'piso da bandeja, 2,0 mm abaixo da borda',
       'recebe o FUNDO RETO do pote de cima - nao ha pe'),
      (CORPO, -12.0, 344, 'CORPO RETO',
       '%.1f mm, secao constante ate o fundo' % CORPO,
       'e o que o IML pede')]
a('        <g stroke="var(--cota)" stroke-width=".9" fill="none">')
for w, z, yy, _t, _a, _b in CH:
    a('          <path d="M %.1f %.1f L 352 %.1f L 362 %.1f"/>' % (X(w), Y(z), Y(z), yy - 4))
a('        </g>')
a('        <g fill="var(--cota)">')
for w, z, yy, _t, _a, _b in CH:
    a('          <circle cx="%.1f" cy="%.1f" r="3"/>' % (X(w), Y(z)))
a('        </g>')
a('        <g font-family="IBM Plex Mono, monospace" font-size="12">')
for w, z, yy, t, s1, s2 in CH:
    a('          <text x="368" y="%d" fill="var(--cota)">%s</text>' % (yy, t))
    a('          <text x="368" y="%d" font-size="11" fill="var(--ink-2)">%s</text>' % (yy + 15, s1))
    if s2:
        a('          <text x="368" y="%d" font-size="10.5" fill="var(--muted)">%s</text>' % (yy + 29, s2))
a('        </g>')
a('        <g font-family="IBM Plex Mono, monospace" font-size="11" fill="var(--muted)">')
a('          <text x="50" y="%.0f">POTE DE CIMA</text>' % Y(10.0))
a('          <text x="50" y="%.0f" fill="var(--verde)">TAMPA</text>' % Y(-2.6))
a('          <text x="50" y="%.0f">POTE DE BAIXO</text>' % Y(-14.5))
a('        </g>')
a('        <text x="44" y="26" font-family="IBM Plex Mono, monospace" font-size="10.5" '
  'fill="var(--muted)">CORTE NA BORDA · escala %d:1 · só a metade direita</text>' % S)
a('      </svg>')
print('\n'.join(o))
