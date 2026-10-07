#!/usr/bin/env python3
"""Corte ampliado da borda nova: dente, degrau, lingueta, aro em U e trava.

Tudo sai de calculo-modular.py. So a metade direita da secao, e sem a saida de
0,5 graus - em 10 mm de borda ela vale 0,09 mm, que nesta escala e a espessura
do traco.
"""
import importlib.util, math, os
CALC = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'calculo-modular.py')
spec = importlib.util.spec_from_file_location('cm', CALC)
cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)

p = cm.linha(cm.footprint())
p0 = p[0]
h = lambda v: v / 2.0

COLAR, CORPO, BOCA = p0['colar_l'], p0['corpo_l'], p0['boca']
SAIA_O  = BOCA - 2 * cm.SAIA_FOLGA
LING_O  = SAIA_O - 2 * cm.RECUO
LING_I  = LING_O - 2 * cm.LING_T
DECK_U  = SAIA_O - 2 * cm.SAIA_T
TAMPA_O = COLAR + 2 * cm.TRAVA_FOLGA
U_OO    = LING_O + 2 * cm.ARO_PAR
U_II    = LING_I - 2 * cm.ARO_PAR
PTA_O   = LING_O + 2 * cm.DENTE_ARO       # lingueta na farpa
PTA_I   = LING_I - 2 * cm.DENTE_ARO
BOL_O   = LING_O + 2 * (cm.DENTE_ARO + 0.05)
BOL_I   = LING_I - 2 * (cm.DENTE_ARO + 0.05)
BASE600 = p0['base_ext']
W       = cm.WALL[1]
ZD      = cm.Z_DENTE               # face de baixo do web = o DENTE
ZG      = cm.Z_DEGRAU              # face de cima do web = o DEGRAU
ZL      = cm.Z_DECK_B              # topo da lingueta / da banda do aro
ZLF     = ZL - cm.LING_H           # ponta da lingueta
ZOMB    = ZL - (cm.LING_H - cm.DENTE_ARO_H - cm.DENTE_ARO_R)   # ombro da farpa
ZFIM    = ZOMB - cm.DENTE_ARO_H
ZUF     = ZL - cm.ARO_H            # fundo do U
ZUV     = ZUF + cm.ARO_FUNDO       # teto do vao do U

S, R0, Z0 = 22.0, 69.0, 117.0      # escala, origem em x, origem em y
X = lambda v: (h(v) - R0) * S + 62
Y = lambda z: Z0 - z * S
pt = lambda v, z: '%.1f %.1f' % (X(v), Y(z))
CUT = 2 * R0                       # o quadro corta aqui, a esquerda

o = []; a = o.append
a('      <svg viewBox="0 0 600 490" role="img" aria-label="Corte ampliado da borda de '
  '8 mm: dente, degrau interno, lingueta com o aro de silicone em U e a trava de clipe">')
a('        <defs>')
a('          <pattern id="hb" width="5" height="5" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">')
a('            <line x1="0" y1="0" x2="0" y2="5" stroke="var(--pp)" stroke-width="1" opacity=".5"/>')
a('          </pattern>')
a('        </defs>')

# ---- tampa de PP (desenhada primeiro; os contornos dos potes ficam por cima) ----
seq = [(CUT, cm.Z_MOD), (DECK_U, cm.Z_MOD), (DECK_U, cm.PP_FLANGE),
       (TAMPA_O, cm.PP_FLANGE), (TAMPA_O, 0.0), (SAIA_O, 0.0),
       (SAIA_O, ZL),
       (LING_O, ZL), (LING_O, ZOMB), (PTA_O, ZOMB), (PTA_O, ZFIM),   # a FARPA
       (LING_O, ZLF), (LING_I, ZLF),
       (PTA_I, ZFIM), (PTA_I, ZOMB), (LING_I, ZOMB), (LING_I, ZL),
       (DECK_U, ZL), (CUT, ZL)]
d = 'M ' + ' L '.join(pt(v, z) for v, z in seq) + ' Z'
a('        <path d="%s" fill="var(--verde)" opacity=".55"/>' % d)
a('        <path d="%s" fill="none" stroke="var(--verde)" stroke-width="1.5"/>' % d)

# trava de clipe: gancho sob o DENTE + rabo para o dedo
F, TT = cm.TRAVA_FOLGA, cm.TRAVA_T
# mesma correcao de gera-3d.py: a farpa e cotada da face da borda NA ALTURA DO
# DENTE, nao no topo.
FA = cm.TRAVA_FARPA + cm.BORDA_H * cm.T
BU, RA = cm.TRAVA_BULGE, cm.TRAVA_RABO
tv = [(COLAR + 2 * F,                 cm.PP_FLANGE),
      (COLAR + 2 * F,                 ZD),
      (COLAR - 2 * FA,                ZD),
      (COLAR - 2 * FA,                ZD - 0.50),
      (COLAR + 2 * (F + 0.20),        ZD - 1.70),
      (COLAR + 2 * (F + BU),          ZD - RA),
      (COLAR + 2 * (F + BU + TT),     ZD - RA + 0.9),
      (COLAR + 2 * (F + TT),          ZD - 0.80),
      (COLAR + 2 * (F + TT),          cm.PP_FLANGE)]
dt = 'M ' + ' L '.join(pt(v, z) for v, z in tv) + ' Z'
a('        <path d="%s" fill="var(--verde)" opacity=".8"/>' % dt)
a('        <path d="%s" fill="none" stroke="var(--verde)" stroke-width="1.5"/>' % dt)

# aro em U, CALCADO na lingueta e na medida livre: a perna de fora passa
# ARO_COMP por lado alem da boca, e e essa a interferencia.
ZP = ZUV + cm.ARO_BOLSA_H                 # teto da bolsa
u = [(U_OO, ZL), (U_OO, ZUF), (U_II, ZUF), (U_II, ZL),
     (LING_I, ZL), (LING_I, ZP), (BOL_I, ZP), (BOL_I, ZUV),
     (BOL_O, ZUV), (BOL_O, ZP), (LING_O, ZP), (LING_O, ZL)]
a('        <path d="M %s Z" fill="var(--tpe)"/>' % ' L '.join(pt(v, z) for v, z in u))

# ---- nervura sob o deck, no recorte da esquerda ----
nv = cm.nervuras(DECK_U, DECK_U - (p0['colar_l'] - p0['colar_w']))
xn = CUT + 2 * 6.0                        # uma nervura a 6 mm do recorte
nerv = ([(xn - 2 * w, ZL - h) for w, h in nv['perfil']]
        + [(xn + 2 * w, ZL - h) for w, h in reversed(nv['perfil'][:-1])])
a('        <path d="M %s Z" fill="var(--verde)" opacity=".8" stroke="var(--verde)" '
  'stroke-width="1.2"/>' % ' L '.join(pt(v, z) for v, z in nerv))

# ---- pote de baixo: a borda em L, com a meia-cana no topo ----
pb = [(BOCA, ZG), (BOCA, -cm.ARRED)]
for k in range(1, 8):                       # meia-cana do topo
    ang = math.radians(180 - 180 * k / 8)
    pb.append((COLAR - 2 * cm.ARRED + 2 * cm.ARRED * math.cos(ang),
               -cm.ARRED + cm.ARRED * math.sin(ang)))
pb += [(COLAR, -cm.ARRED), (COLAR, ZD), (CORPO, ZD), (CORPO, ZD - 6.0),
       (CORPO - 2 * W, ZD - 6.0), (CORPO - 2 * W, ZG)]
a('        <path d="M %s Z" fill="url(#hb)" stroke="var(--pp)" stroke-width="1.8"/>'
  % ' L '.join(pt(v, z) for v, z in pb))

# ---- pote de cima: fundo RETO pousando no deck ----
pc = [(BASE600, cm.Z_MOD), (BASE600, 3.5), (CUT, 3.5), (CUT, cm.Z_MOD)]
a('        <path d="M %s Z" fill="url(#hb)" stroke="var(--pp)" stroke-width="1.8"/>'
  % ' L '.join(pt(v, z) for v, z in pc))

# ---- chamadas ----
CH = [(COLAR - cm.DENTE, ZD, 48, 'O DENTE',
       'face de BAIXO do web, %.2f mm/lado' % cm.DENTE,
       'a parede da borda esta em cima dele: e material, nao aba flutuando'),
      (BOCA, ZG, 112, 'DEGRAU INTERNO',
       'face de CIMA do web, %.2f mm/lado' % (cm.DENTE + W - cm.BORDA_PAR),
       'e nele que a placa de teca pousa - e isso fixa os %.2f mm dela' % cm.TECA_ESP),
      (COLAR - 2 * FA, ZD - 0.25, 178, 'GANCHO DA TRAVA',
       'avanca %.2f mm sob o dente (%.0f%% dele)'
       % (cm.TRAVA_FARPA, 100 * cm.TRAVA_FARPA / cm.DENTE),
       '2 travas de %.0f mm, uma por lado comprido' % (cm.TRAVA_FRAC * COLAR)),
      (U_OO, (ZL + ZUF) / 2, 244, 'ARO EM U DE SILICONE',
       'comprime %.2f mm/lado contra a parede da boca' % cm.ARO_COMP,
       'calcado na lingueta: nao e colado, ele abraca'),
      (PTA_O, (ZOMB + ZFIM) / 2, 300, 'FARPA + BOLSA',
       'farpa de %.2f/face; o U tem bolsa e RELAXA em cima dela' % cm.DENTE_ARO,
       'entra por rampa de 36°, sai por degrau de 90°'),
      (xn + cm.NERV_T, ZL - cm.NERV_H / 2, 356, 'MINI LOMBADA',
       '%.2f na raiz, %.2f na ponta, crista R%.2f'
       % (cm.NERV_T, nv['t_pta'], nv['raio']),
       'grade %dx%d, saida de %.0f° por face, I sobe %.2fx'
       % (len(nv['xs']), len(nv['ys']), cm.SAIDA_NERV, nv['ganho'])),
      (DECK_U, cm.Z_MOD, 404, 'PLANO MODULAR',
       'topo do deck, %.1f mm abaixo do topo da borda' % cm.BASE_T,
       'recebe o FUNDO RETO do pote de cima - nao ha pe'),
      (CORPO, ZD - 4.0, 436, 'CORPO RETO',
       '%.1f mm, secao constante ate o fundo' % CORPO,
       'saida de 0,5° - ver SAIDA DE EXTRACAO no calculo')]
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
a('          <text x="66" y="%.0f">POTE DE CIMA</text>' % Y(3.4))
a('          <text x="66" y="%.0f" fill="var(--verde)">TAMPA PP</text>' % Y(-2.9))
a('          <text x="66" y="%.0f">POTE DE BAIXO</text>' % Y(ZD - 4.2))
a('        </g>')
a('        <text x="62" y="22" font-family="IBM Plex Mono, monospace" font-size="10.5" '
  'fill="var(--muted)">CORTE NA BORDA · escala %d:1 · só a metade direita · sem a saída de 0,5°</text>' % S)
a('      </svg>')
print('\n'.join(o))
