#!/usr/bin/env python3
"""Corte ampliado do encaixe da tampa PE, gerado das cotas reais."""
import importlib.util, math, os
CALC = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'calculo-modular.py')
sp = importlib.util.spec_from_file_location('cm', CALC)
cm = importlib.util.module_from_spec(sp); sp.loader.exec_module(cm)
p = cm.linha(cm.footprint()); p0 = p[0]
T = math.tan(math.radians(cm.SAIDA))
h = lambda w: w / 2.0                      # meia-largura
EXT, ABA, WB = p0['ext_l'], cm.ABA_W, cm.W_BORDA
labio, boca = EXT + 2*ABA, EXT - 2*WB
PEL = cm.pe_l(EXT)
saia_i, saia_o = labio + 2*cm.PE_FOLGA_SAIA, labio + 2*cm.PE_FOLGA_SAIA + 2*cm.PE_PAR_SAIA
garra_i = saia_i - 2*cm.PE_GARRA
aba_o   = saia_o + 2*cm.PE_ABA_PEGA
bandeja = boca - 2*cm.PLUG_FOLGA - 2*cm.PLUG_PAR
poco    = bandeja + 2*cm.PE_POCO_PAR
z_lab, z_gar = -(cm.ABA_T + cm.LIP_H), -(cm.ABA_T + cm.LIP_H) + cm.PE_PRECARGA
z_pe = z_gar - cm.PE_GARRA_H - 0.90
z_rep = 4.00 - cm.PE_FOLGA_REP

S, R0, Z0 = 15.0, 64.5, 232.0
X = lambda w: (h(w) - R0) * S + 46
Y = lambda z: Z0 - z * S
pt = lambda w, z: '%.1f %.1f' % (X(w), Y(z))

o = []; a = o.append
a('      <svg viewBox="0 0 760 400" role="img" aria-label="Corte ampliado do encaixe da tampa PE: '
  'a saia desce por fora da borda e a garra engata sob o labio da aba em U">')
a('        <defs>')
a('          <pattern id="hpe" width="5" height="5" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">')
a('            <line x1="0" y1="0" x2="0" y2="5" stroke="var(--pp)" stroke-width="1" opacity=".5"/>')
a('          </pattern>')
a('        </defs>')

# ---- tampa PE (desenhada primeiro: os contornos dos potes ficam por cima) ----
# ---- tampa PE ----
CUT = 124.0   # a peca segue para a esquerda; o quadro corta aqui
seq = [(CUT,-2.00),(bandeja,-2.00),(bandeja,z_rep),(poco+2.3,z_rep),(poco+4.9,cm.PE_DECK),
       (saia_o,cm.PE_DECK),(saia_o,z_pe+cm.PE_ABA_T),(aba_o,z_pe+cm.PE_ABA_T),(aba_o,z_pe),
       (saia_i,z_pe),(garra_i,z_gar-cm.PE_GARRA_H),(garra_i,z_gar),(saia_i,z_gar),
       (saia_i,0.0),(labio-5.8,0.0),(labio-6.3,-cm.PE_CORDAO),(labio-6.8,0.0),
       (boca,0.0),(poco,z_rep-cm.PE_DECK),(poco,-2.00-cm.PE_DECK),(CUT,-2.00-cm.PE_DECK)]
d3 = 'M ' + ' L '.join(pt(w, z) for w, z in seq) + ' Z'
a('        <path d="%s" fill="var(--verde)" opacity=".55"/>' % d3)
a('        <path d="%s" fill="none" stroke="var(--verde)" stroke-width="1.6"/>' % d3)

# ---- pote de baixo: parede + aba em U com labio ----
corpo_z = lambda z: EXT - 2 * (-z) * T * 0   # parede praticamente reta neste zoom
d = ('M %s L %s L %s L %s L %s L %s L %s L %s L %s Z' % (
    pt(boca, 0), pt(labio, 0), pt(labio, z_lab), pt(labio - 2*1.20, z_lab),
    pt(labio - 2*1.20, -cm.ABA_T), pt(EXT, -cm.ABA_T), pt(EXT, -9.0),
    pt(boca - 2*0.0, -9.0), pt(boca, -9.0)))
a('        <path d="%s" fill="url(#hpe)" stroke="var(--pp)" stroke-width="1.8"/>' % d)
a('        <text x="52" y="%.0f" font-family="IBM Plex Mono, monospace" font-size="11" '
  'fill="var(--muted)">POTE DE BAIXO</text>' % Y(-8.4))

# ---- pote de cima: pe na bandeja + anel do degrau ----
d2 = ('M %s L %s L %s L %s L %s L %s Z' % (
    pt(PEL, -2.00), pt(PEL, 4.00), pt(EXT - 2*(p[0]['H']-cm.PE_H)*T, 4.00),
    pt(EXT - 2*(p[0]['H']-cm.PE_H)*T, 9.5), pt(124.0, 9.5), pt(124.0, -2.00)))
a('        <path d="%s" fill="url(#hpe)" stroke="var(--pp)" stroke-width="1.8"/>' % d2)
a('        <text x="52" y="%.0f" font-family="IBM Plex Mono, monospace" font-size="11" '
  'fill="var(--muted)">POTE DE CIMA</text>' % Y(8.6))
a('        <text x="52" y="%.0f" font-family="IBM Plex Mono, monospace" font-size="11" '
  'fill="var(--verde)">TAMPA PE</text>' % Y(-5.0))

# ---- cotas e chamadas ----
CH = [(labio,            z_lab,            72, 'GARRA', 'engata %.2f mm sob o lábio da aba' % ((labio-garra_i)/2),
       'o lábio já existia para enrijecer a boca'),
      (labio-6.3,        -cm.PE_CORDAO,   132, 'CORDÃO', 'aperta %.2f mm contra o topo da borda' % cm.PE_CORDAO,
       'a garra dá %.2f mm de pré-carga' % cm.PE_PRECARGA),
      (aba_o,            z_pe+0.6,        192, 'ABA DE PEGA', 'é por onde se descasca um canto', ''),
      (bandeja,          -2.00,           252, 'PISO DA BANDEJA', 'z = −2,00 — o plano modular', ''),
      (poco+1.0,         z_rep,           312, 'REPISA', 'z = +3,80, batente do anel do pote de cima',
       '0,20 mm abaixo dele: nunca define o passo')]
a('        <g stroke="var(--cota)" stroke-width=".9" fill="none">')
for w, z, yy, _t, _s1, _s2 in CH:
    a('          <path d="M %.1f %.1f L 336 %.1f L 346 %.1f"/>' % (X(w), Y(z), Y(z), yy - 4))
a('        </g>')
a('        <g fill="var(--cota)">')
for w, z, yy, _t, _s1, _s2 in CH:
    a('          <circle cx="%.1f" cy="%.1f" r="3"/>' % (X(w), Y(z)))
a('        </g>')
a('        <g font-family="IBM Plex Mono, monospace" font-size="12">')
for w, z, yy, t, s1, s2 in CH:
    a('          <text x="352" y="%d" fill="var(--cota)">%s</text>' % (yy, t))
    a('          <text x="352" y="%d" font-size="11" fill="var(--ink-2)">%s</text>' % (yy + 15, s1))
    if s2:
        a('          <text x="352" y="%d" font-size="10.5" fill="var(--muted)">%s</text>' % (yy + 29, s2))
a('        </g>')
a('        <text x="46" y="30" font-family="IBM Plex Mono, monospace" font-size="10.5" '
  'fill="var(--muted)">CORTE NA BORDA · escala %d:1 · só a metade direita</text>' % S)
a('      </svg>')
print('\n'.join(o))
