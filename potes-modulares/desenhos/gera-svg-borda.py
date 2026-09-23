#!/usr/bin/env python3
"""Corte ampliado da borda oca: flare, perna, canal, saia, aresta e trava.

Tudo sai de calculo-modular.py. So a metade direita da secao, e sem a saida
de 0,5 graus - em 16 mm de borda ela vale 0,14 mm, que nesta escala e a
espessura do traco.
"""
import importlib.util, os
CALC = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'calculo-modular.py')
spec = importlib.util.spec_from_file_location('cm', CALC)
cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)

p = cm.linha(cm.footprint())
p0 = p[0]
h = lambda v: v / 2.0

COLAR, CORPO, BOCA = p0['colar_l'], p0['corpo_l'], p0['boca']
PERNA   = BOCA + 2 * cm.W_IN
PLUG    = BOCA - 2 * cm.PLUG_FOLGA
FRISO   = PLUG - 2 * cm.FRISO_PROF
FILETE  = PLUG - 2 * cm.FRISO_PROF + 2 * cm.FILETE_D
BANDEJA = PLUG - 2 * cm.PP_PLUG_PAR
DECK_O  = COLAR + 2 * cm.PP_DECK_FORA
BASE600 = p0['base_ext']
W       = cm.WALL[1]
ZB      = -cm.BORDA_H              # fim da boca / comeco do flare
ZF      = ZB - cm.FLARE            # pe do flare = topo da parede reta
ZS      = -cm.SAIA_H               # aresta de engate

S, R0, Z0 = 14.0, 68.4, 120.0      # escala, origem em x, origem em y
X = lambda v: (h(v) - R0) * S + 62
Y = lambda z: Z0 - z * S
pt = lambda v, z: '%.1f %.1f' % (X(v), Y(z))
CUT = 136.9                        # o quadro corta aqui, a esquerda

o = []; a = o.append
a('      <svg viewBox="0 0 600 450" role="img" aria-label="Corte ampliado da borda oca: '
  'flare, perna de dentro, canal, saia livre, aresta de engate e a trava de clipe da tampa">')
a('        <defs>')
a('          <pattern id="hb" width="5" height="5" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">')
a('            <line x1="0" y1="0" x2="0" y2="5" stroke="var(--pp)" stroke-width="1" opacity=".5"/>')
a('          </pattern>')
a('        </defs>')

# ---- tampa de PP (desenhada primeiro; os contornos dos potes ficam por cima) ----
seq = [(CUT, -cm.BASE_T), (BANDEJA, -cm.BASE_T), (BANDEJA, cm.PP_DECK),
       (DECK_O, cm.PP_DECK), (DECK_O, 0.0), (PLUG, 0.0),
       (PLUG, -3.0), (FRISO, -3.0), (FRISO, -4.4), (PLUG, -4.4),
       (PLUG, -cm.PP_PLUG_H + 0.5), (PLUG - 2.0, -cm.PP_PLUG_H),
       (BANDEJA, -cm.PP_PLUG_H),
       (BANDEJA, -cm.BASE_T - cm.PP_DECK), (CUT, -cm.BASE_T - cm.PP_DECK)]
d = 'M ' + ' L '.join(pt(v, z) for v, z in seq) + ' Z'
a('        <path d="%s" fill="var(--verde)" opacity=".55"/>' % d)
a('        <path d="%s" fill="none" stroke="var(--verde)" stroke-width="1.5"/>' % d)

# trava de clipe: gancho sob a aresta da saia + rabo para o dedo
F, TT = cm.TRAVA_FOLGA, cm.TRAVA_T
# mesma correcao de gera-3d.py: a farpa e cotada da face da borda NA ALTURA
# DA ARESTA, nao no topo.
FA = cm.TRAVA_FARPA + cm.SAIA_H * cm.T
BU, RA = cm.TRAVA_BULGE, cm.TRAVA_RABO
tv = [(COLAR + 2 * F,                 cm.PP_DECK),
      (COLAR + 2 * F,                 ZS),
      (COLAR - 2 * FA,                ZS),
      (COLAR - 2 * FA,                ZS - 0.50),
      (COLAR + 2 * (F + 0.20),        ZS - 1.70),
      (COLAR + 2 * (F + BU),          ZS - RA),
      (COLAR + 2 * (F + BU + TT),     ZS - RA + 0.9),
      (COLAR + 2 * (F + TT),          ZS - 0.80),
      (COLAR + 2 * (F + TT),          cm.PP_DECK)]
dt = 'M ' + ' L '.join(pt(v, z) for v, z in tv) + ' Z'
a('        <path d="%s" fill="var(--verde)" opacity=".8"/>' % dt)
a('        <path d="%s" fill="none" stroke="var(--verde)" stroke-width="1.5"/>' % dt)

# filete de TPE, na medida livre (invade 0,20 mm a boca - e a interferencia)
fl = [(FRISO, -3.0), (FILETE, -3.0), (FILETE, -4.4), (FRISO, -4.4)]
a('        <path d="M %s Z" fill="var(--tpe)"/>' % ' L '.join(pt(v, z) for v, z in fl))

# ---- pote de baixo: a borda OCA ----
pb = [(BOCA, ZB), (BOCA, -cm.CHANF), (BOCA + 2 * cm.CHANF, 0.0),
      (COLAR - 2 * cm.ARRED, 0.0), (COLAR, -cm.ARRED),
      (COLAR, ZS), (COLAR - 2 * cm.W_SAIA, ZS),
      (COLAR - 2 * cm.W_SAIA, -cm.TOPO_T), (PERNA, -cm.TOPO_T), (PERNA, ZB),
      (CORPO, ZF), (CORPO, ZF - 6.0),
      (CORPO - 2 * W, ZF - 6.0), (CORPO - 2 * W, ZF)]
a('        <path d="M %s Z" fill="url(#hb)" stroke="var(--pp)" stroke-width="1.8"/>'
  % ' L '.join(pt(v, z) for v, z in pb))

# ---- pote de cima: fundo RETO pousando na bandeja ----
pc = [(BASE600, -cm.BASE_T), (BASE600, 6.0), (CUT, 6.0), (CUT, -cm.BASE_T)]
a('        <path d="M %s Z" fill="url(#hb)" stroke="var(--pp)" stroke-width="1.8"/>'
  % ' L '.join(pt(v, z) for v, z in pc))

# ---- chamadas ----
CH = [(COLAR - cm.W_SAIA, ZS, 52, 'ARESTA DE ENGATE',
       'face de baixo da saia livre, %.2f mm/lado' % cm.W_SAIA,
       'a saia e livre: e material, nao um anel flutuando'),
      (COLAR - cm.W_SAIA - cm.CANAL, -cm.SAIA_H / 2, 118, 'CANAL',
       '%.2f mm de largura, %.1f mm de profundidade' % (cm.CANAL, cm.SAIA_H - cm.TOPO_T),
       'nervura de aco de %.1f:1 no molde' % ((cm.SAIA_H - cm.TOPO_T) / cm.CANAL)),
      (COLAR - 2 * FA, ZS - 0.25, 184, 'GANCHO DA TRAVA',
       'avanca %.2f mm sob a aresta (%.0f%% de engate)'
       % (cm.TRAVA_FARPA, 100 * cm.TRAVA_FARPA / cm.W_SAIA),
       '2 travas de %.0f mm, uma por lado comprido' % (cm.TRAVA_FRAC * COLAR)),
      (FILETE, -3.7, 250, 'FILETE DE TPE',
       'comprime %.2f mm/lado contra a boca' % (cm.FILETE_SOB - cm.PLUG_FOLGA),
       'o MESMO filete na teca, num friso 2,0 mm mais fundo'),
      (BANDEJA, -cm.BASE_T, 316, 'PLANO MODULAR',
       'piso da bandeja, 2,0 mm abaixo do topo da borda',
       'recebe o FUNDO RETO do pote de cima - nao ha pe'),
      (PERNA, ZB + 1.0, 372, 'PERNA DE DENTRO',
       'parede %.2f mm, faz a boca de %.1f mm' % (cm.W_IN, BOCA),
       'o flare abre %.2f mm/lado em %.1f mm' % ((PERNA - CORPO) / 2, cm.FLARE)),
      (CORPO, ZF - 4.0, 412, 'CORPO RETO',
       '%.1f mm, secao constante ate o fundo' % CORPO,
       'e o que o IML pede')]
a('        <g stroke="var(--cota)" stroke-width=".9" fill="none">')
for v, z, yy, _t, _a, _b in CH:
    a('          <path d="M %.1f %.1f L 250 %.1f L 262 %.1f"/>' % (X(v), Y(z), Y(z), yy - 4))
a('        </g>')
a('        <g fill="var(--cota)">')
for v, z, yy, _t, _a, _b in CH:
    a('          <circle cx="%.1f" cy="%.1f" r="3"/>' % (X(v), Y(z)))
a('        </g>')
a('        <g font-family="IBM Plex Mono, monospace" font-size="12">')
for v, z, yy, t, s1, s2 in CH:
    a('          <text x="268" y="%d" fill="var(--cota)">%s</text>' % (yy, t))
    a('          <text x="268" y="%d" font-size="11" fill="var(--ink-2)">%s</text>' % (yy + 15, s1))
    if s2:
        a('          <text x="268" y="%d" font-size="10.5" fill="var(--muted)">%s</text>' % (yy + 29, s2))
a('        </g>')
a('        <g font-family="IBM Plex Mono, monospace" font-size="11" fill="var(--muted)">')
a('          <text x="66" y="%.0f">POTE DE CIMA</text>' % Y(4.2))
a('          <text x="66" y="%.0f" fill="var(--verde)">TAMPA PP</text>' % Y(-3.0))
a('          <text x="66" y="%.0f">POTE DE BAIXO</text>' % Y(ZF - 4.2))
a('        </g>')
a('        <text x="62" y="22" font-family="IBM Plex Mono, monospace" font-size="10.5" '
  'fill="var(--muted)">CORTE NA BORDA · escala %d:1 · só a metade direita · sem a saída de 0,5°</text>' % S)
a('      </svg>')
print('\n'.join(o))
