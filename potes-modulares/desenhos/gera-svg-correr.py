#!/usr/bin/env python3
"""Vista de topo das tres posicoes da tampa de correr, e o corte do bico.

As cotas saem de calculo-correr.py, que por sua vez sai de calculo-modular.py.
Desenho com cota que nao sai do calculo mente cedo ou tarde.

Uso:  python3 gera-svg-correr.py [curto|canto|comprido|corte]
"""
import importlib.util, math, os, sys

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location('cc', os.path.join(_BASE, 'calculo-correr.py'))
cc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cc)
cm = cc.cm

DECK_L, DECK_W = cc.DECK_O, cc.DECK_O - cc.DLW
BORDA_L, BORDA_W = cc.COLAR_L, cc.COLAR_W
BAND_L, BAND_W = cc.BANDEJA, cc.BAND_W
R_DECK = cm.raio(DECK_L, cc.COLAR_L)
R_BAND = cc.R_BAND


def rr(L, W, R, cx=0.0, cy=0.0, ang=0.0, n=8):
    """Retangulo de cantos arredondados, como lista de pontos, ja rotacionado."""
    hx, hy = L / 2 - R, W / 2 - R
    p = []
    for ccx, ccy, a0 in ((hx, hy, 0), (-hx, hy, 90), (-hx, -hy, 180), (hx, -hy, 270)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            p.append((ccx + R * math.cos(a), ccy + R * math.sin(a)))
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in p]


def topo(cod):
    p = next(q for q in cc.POSICOES if q['cod'] == cod)
    g = cc.geometria(p)                      # traz layout, recuo e o que cabe
    u, ang = g['u'], math.degrees(math.atan2(g['u'][1], g['u'][0]))
    n = (-u[1], u[0])
    S = 3.1
    W_SVG, H_SVG = 640, 430
    X = lambda x: W_SVG / 2 + x * S
    Y = lambda y: H_SVG / 2 - y * S + 10
    path = lambda pts: 'M ' + ' L '.join('%.1f %.1f' % (X(a), Y(b)) for a, b in pts) + ' Z'
    ao = lambda c, L, W, R: rr(L, W, R, c[0], c[1], ang)

    o = []; a = o.append
    a('      <svg viewBox="0 0 %d %d" role="img" aria-label="Vista de topo da tampa de '
      'correr, %s: bolso, gaveta, janela e a calha em U">' % (W_SVG, H_SVG, p['rot']))
    a('        <defs>')
    a('          <pattern id="gv%s" width="4" height="4" patternTransform="rotate(45)" '
      'patternUnits="userSpaceOnUse">' % cod)
    a('            <line x1="0" y1="0" x2="0" y2="4" stroke="var(--verde)" stroke-width="1.1" opacity=".6"/>')
    a('          </pattern>')
    a('        </defs>')

    # deck, borda (tracejada) e vao da bandeja
    a('        <path d="%s" fill="var(--sheet)" stroke="var(--verde)" stroke-width="1.6"/>'
      % path(rr(DECK_L, DECK_W, R_DECK)))
    a('        <path d="%s" fill="none" stroke="var(--line)" stroke-width=".9" '
      'stroke-dasharray="5 3"/>' % path(rr(BORDA_L, BORDA_W, cm.R_EXT)))
    a('        <path d="%s" fill="none" stroke="var(--verde)" stroke-width="1.2"/>'
      % path(rr(BAND_L, BAND_W, R_BAND)))

    # as duas travas de clipe, nos lados compridos
    tl = cm.TRAVA_FRAC * BORDA_L
    for sy in (1, -1):
        a('        <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="var(--verde)" '
          'opacity=".30"/>' % (X(-tl / 2),
                               Y(BORDA_W / 2 + 2.8) if sy > 0 else Y(-BORDA_W / 2),
                               tl * S, 2.8 * S))
    a('        <text x="%.1f" y="%.1f" text-anchor="middle" font-family="IBM Plex Mono, monospace" '
      'font-size="9" fill="var(--muted)">trava de clipe · %.0f mm</text>'
      % (X(0), Y(BORDA_W / 2 + 5.6), tl))

    # bolso
    a('        <path d="%s" fill="var(--paper)" stroke="var(--verde)" stroke-width="1" '
      'stroke-dasharray="3 2"/>'
      % path(ao(g['bolso'], g['bolso_l'], g['gav_w'] + 2 * cc.GAV_FOLGA, 3.0)))

    # calha em U: da borda externa da janela ate a face do deck
    # a calha so existe FORA da parede da bandeja. Dentro dela o liquido corre
    # no piso raso - e e isso que a travessia mede.
    p0 = (g['base'][0] - u[0] * 2.0, g['base'][1] - u[1] * 2.0)
    p1 = (g['ext'][0] + u[0] * cc.BICO_LIP, g['ext'][1] + u[1] * cc.BICO_LIP)
    bw = p['bico_w'] / 2
    quad = [(p0[0] + n[0] * bw, p0[1] + n[1] * bw), (p1[0] + n[0] * bw, p1[1] + n[1] * bw),
            (p1[0] - n[0] * bw, p1[1] - n[1] * bw), (p0[0] - n[0] * bw, p0[1] - n[1] * bw)]
    a('        <path d="%s" fill="var(--cota)" opacity=".16"/>' % path(quad))
    for sg in (1, -1):
        a('        <path d="M %.1f %.1f L %.1f %.1f" stroke="var(--cota)" stroke-width="2.2" '
          'fill="none"/>' % (X(p0[0] + sg * n[0] * bw), Y(p0[1] + sg * n[1] * bw),
                             X(p1[0] + sg * n[0] * bw), Y(p1[1] + sg * n[1] * bw)))

    # janela aberta
    a('        <path d="%s" fill="var(--pp)" opacity=".55" stroke="var(--pp)" stroke-width="1.3"/>'
      % path(ao(g['jan'], g['jan_d'], g['jan_w'], 3.0)))

    # gaveta RECUADA (o estado que se ve quando se verte) - solida
    a('        <path d="%s" fill="url(#gv%s)" stroke="var(--verde)" stroke-width="1.7"/>'
      % (path(ao(g['gav_ab'], g['gav_l'], g['gav_w'], 3.0)), cod))
    dp = -(g['jan_d'] / 2 + cc.SILL / 2)
    pux = (g['gav_ab'][0] + u[0] * dp, g['gav_ab'][1] + u[1] * dp)
    a('        <path d="%s" fill="var(--verde)" opacity=".6"/>'
      % path(ao(pux, cc.PUXADOR, g['gav_w'] * 0.45, 2.0)))

    # gaveta FECHADA - fantasma, com o 2o aro
    a('        <path d="%s" fill="none" stroke="var(--muted)" stroke-width="1.1" '
      'stroke-dasharray="4 3"/>' % path(ao(g['gav_fec'], g['gav_l'], g['gav_w'], 3.0)))
    a('        <path d="%s" fill="none" stroke="var(--tpe)" stroke-width="2.2"/>'
      % path(ao(g['jan'], g['jan_d'] + 4.0, g['jan_w'] + 4.0, 3.0)))

    # travessia: o trecho de piso de bandeja que o liquido molha
    if g['travessia'] > 0.5:
        q0 = (g['jan'][0] + u[0] * g['jan_d'] / 2, g['jan'][1] + u[1] * g['jan_d'] / 2)
        q1 = (g['base'][0], g['base'][1])
        a('        <path d="M %.1f %.1f L %.1f %.1f" stroke="var(--alerta)" '
          'stroke-width="3.5" stroke-dasharray="5 3" fill="none"/>'
          % (X(q0[0]), Y(q0[1]), X(q1[0]), Y(q1[1])))
        mid = ((q0[0] + q1[0]) / 2, (q0[1] + q1[1]) / 2)
        a('        <text x="%.1f" y="%.1f" font-family="IBM Plex Mono, monospace" '
          'font-size="10" fill="var(--alerta)">travessia %.0f mm</text>'
          % (X(mid[0]) - 76, Y(mid[1]) - 8, g['travessia']))

    a('        <g font-family="IBM Plex Mono, monospace" font-size="10" fill="var(--cota)">')
    a('          <text x="%.1f" y="%.1f" text-anchor="middle">bico %.0f mm</text>'
      % (X(p1[0] + u[0] * 6), Y(p1[1] + u[1] * 6) + 3, p['bico_w']))
    a('        </g>')
    a('        <g font-family="IBM Plex Mono, monospace" font-size="9.5" fill="var(--muted)">')
    a('          <text x="14" y="20" fill="var(--ink-2)" font-size="11">%s</text>' % p['rot'])
    a('          <text x="14" y="36">janela %.0f × %.0f · vazão %.0f mm² · curso %.0f mm</text>'
      % (g['jan_w'], g['jan_d'], g['area'], g['curso']))
    a('          <text x="14" y="50">gaveta %.0f × %.0f × %.2f mm · %.1f g · 2º aro %.0f mm</text>'
      % (g['gav_w'], g['gav_l'], cc.GAV_T, g['gav_g'], g['aro_per']))
    a('          <text x="14" y="%d">gaveta RECUADA (cheia) · - - - fechada · '
      'aro de TPE em laranja</text>' % (H_SVG - 26))
    a('          <text x="14" y="%d">escala %.1f:1 · deck %.1f × %.1f mm</text>'
      % (H_SVG - 12, S, DECK_L, DECK_W))
    a('        </g>')
    a('      </svg>')
    return '\n'.join(o)


def corte():
    """Corte no eixo do bico. O mesmo nas tres posicoes - so muda onde ele cai."""
    pz = next(q for q in cc.POSICOES if q['cod'] == 'curto')
    g = cc.geometria(pz)
    S = 11.0
    W_SVG, H_SVG = 900, 350
    x0 = 34.0
    X = lambda v: (v - x0) * S + 34
    Y = lambda z: 176 - z * S
    path = lambda seq: 'M ' + ' L '.join('%.1f %.1f' % (X(v), Y(z)) for v, z in seq) + ' Z'

    hb = cc.BANDEJA / 2                      # parede da bandeja, face interna
    hp = cc.PLUG / 2                         # face externa do plug
    hbo = cc.BOCA / 2                        # boca do pote
    hc = cc.COLAR_L / 2                      # face externa da saia da borda
    hs = hc - cm.W_SAIA
    hperna = hbo + cm.W_IN
    hd = cc.DECK_O / 2
    zb, zbf = cc.Z_BOLSO, cc.Z_BOLSO - cm.PP_DECK
    zm, zs, zt = cc.Z_MOD, cc.Z_SEL, cc.Z_TOPO
    fri = hp - cm.FRISO_PROF
    fil = fri + cm.FILETE_D
    zf0, zf1 = -3.0, -3.0 - cm.FILETE_D
    # ao longo do eixo do bico, medindo do centro
    d_jan = cc.BANDEJA / 2 - g['rec']
    jan_i, jan_o = d_jan - g['jan_d'] / 2, d_jan + g['jan_d'] / 2
    bolso_o = g['bolso'][0] + g['bolso_l'] / 2   # fim do bolso ('curto': eixo X)

    o = []; a = o.append
    a('      <svg viewBox="0 0 %d %d" role="img" aria-label="Corte no eixo do bico: a gaveta '
      'no bolso, a janela, e a calha em U subindo por cima do plano de vedacao">'
      % (W_SVG, H_SVG))
    a('        <defs>')
    a('          <pattern id="hcx" width="5" height="5" patternTransform="rotate(45)" '
      'patternUnits="userSpaceOnUse">')
    a('            <line x1="0" y1="0" x2="0" y2="5" stroke="var(--pp)" stroke-width="1" opacity=".5"/>')
    a('          </pattern>')
    a('        </defs>')

    # ---- o pote: borda oca (desenhado primeiro, a tampa cobre) ----
    pot = [(hbo, -cm.BORDA_H), (hbo, -cm.CHANF), (hbo + cm.CHANF, 0.0),
           (hc - cm.ARRED, 0.0), (hc, -cm.ARRED), (hc, -cm.SAIA_H),
           (hs, -cm.SAIA_H), (hs, -cm.TOPO_T), (hperna, -cm.TOPO_T),
           (hperna, -cm.BORDA_H)]
    a('        <path d="%s" fill="url(#hcx)" stroke="var(--pp)" stroke-width="1.7"/>' % path(pot))

    # ---- tampa, parte de FORA da janela: batente, rampa, bico, deck, plug ----
    # o piso da calha: rampa mansa ate o piso da bandeja, depois o VERTEDOURO
    fora = [(jan_o, zb), (bolso_o, zb), (hb, zm),
            (hb + cm.PP_PLUG_PAR + 2.0, zs), (hd, zs),
            (hd + cc.BICO_LIP, zs), (hd + cc.BICO_LIP, zs - 0.7),
            (hd, zs - 0.7), (hd, 0.0), (hp, 0.0),
            (hp, zf0), (fri, zf0), (fri, zf1), (hp, zf1),
            (hp, -cm.PP_PLUG_H + 0.5), (hp - 1.0, -cm.PP_PLUG_H),
            (hb, -cm.PP_PLUG_H), (hb, zbf), (jan_o, zbf)]
    a('        <path d="%s" fill="var(--verde)" opacity=".55"/>' % path(fora))
    a('        <path d="%s" fill="none" stroke="var(--verde)" stroke-width="1.6"/>' % path(fora))

    # ---- tampa, parte de DENTRO da janela: piso do bolso ----
    dentro = [(x0 - 1, zb), (jan_i, zb), (jan_i, zbf), (x0 - 1, zbf)]
    a('        <path d="%s" fill="var(--verde)" opacity=".55"/>' % path(dentro))
    a('        <path d="%s" fill="none" stroke="var(--verde)" stroke-width="1.6"/>' % path(dentro))

    # paredes da calha, atras do corte (o U visto de perfil)
    a('        <path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f" fill="none" '
      'stroke="var(--cota)" stroke-width="1.3" stroke-dasharray="4 3"/>'
      % (X(hb), Y(zm), X(hb), Y(zt), X(hd + cc.BICO_LIP), Y(zt)))
    a('        <text x="%.1f" y="%.1f" font-family="IBM Plex Mono, monospace" '
      'font-size="9.5" fill="var(--cota)">paredes da calha</text>'
      % (X(hb) + 4, Y(zt) - 6))

    # ---- filete de TPE na boca (o que veda o pote) ----
    a('        <path d="%s" fill="var(--tpe)"/>'
      % path([(fri, zf0), (fil, zf0), (fil, zf1), (fri, zf1)]))

    # ---- gaveta fechada, com o 2o aro nos dois lados da janela ----
    gi, go = jan_i - cc.SILL, jan_o + cc.SILL
    a('        <path d="%s" fill="var(--verde)" opacity=".9" stroke="var(--verde)" '
      'stroke-width="1.4"/>' % path([(gi, zm), (go, zm), (go, zm - cc.GAV_T),
                                     (gi, zm - cc.GAV_T)]))
    for xa in (jan_i - 2.0, jan_o + 2.0):
        a('        <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="var(--tpe)"/>'
          % (X(xa - cc.ARO2_D / 2), Y(zm - cc.GAV_T + cc.ARO2_PROF),
             cc.ARO2_D * S, (cc.ARO2_D - cc.ARO2_PROF + cc.ARO2_COMP) * S))

    # ---- chamadas ----
    CH = [((jan_i + jan_o) / 2, zbf, 44, 'JANELA',
           '%.0f × %.0f mm · %.0f mm² de vazão' % (g['jan_w'], g['jan_d'], g['area']),
           'furo no fundo do bolso — a gaveta corre por cima'),
          (jan_o + 2.0, zm - cc.GAV_T, 108, '2º ARO DE TPE',
           'corda de %.2f mm, friso na face de BAIXO da gaveta' % cc.ARO2_D,
           'viaja com ela; só encosta nos últimos %.1f mm de curso' % cc.CUNHA),
          (hb, zm, 172, 'VERTEDOURO',
           'sobe %+.2f mm em %.1f mm — %.0f°' % (g['vert'], g['run2'], g['rampa2']),
           'não pode ser manso: abaixo dele está o friso do filete'),
          (fil, (zf0 + zf1) / 2, 236, 'FILETE INTEIRO',
           'a calha passa ACIMA de z = 0 e do friso',
           'se cortasse, a tampa não vedaria nem com a gaveta fechada'),
          (hd + cc.BICO_LIP, zs - 0.35, 300, 'LÁBIO DE CORTE',
           '%.2f mm de aresta viva na ponta' % cc.BICO_LIP,
           'quebra o filme: a gota solta em vez de escorrer pela face')]
    a('        <g stroke="var(--cota)" stroke-width=".9" fill="none">')
    for v, z, yy, _t, _a, _b in CH:
        a('          <path d="M %.1f %.1f L 470 %.1f L 482 %.1f"/>' % (X(v), Y(z), Y(z), yy - 4))
    a('        </g>')
    a('        <g fill="var(--cota)">')
    for v, z, yy, _t, _a, _b in CH:
        a('          <circle cx="%.1f" cy="%.1f" r="3"/>' % (X(v), Y(z)))
    a('        </g>')
    a('        <g font-family="IBM Plex Mono, monospace" font-size="11.5">')
    for v, z, yy, t, s1, s2 in CH:
        a('          <text x="490" y="%d" fill="var(--cota)">%s</text>' % (yy, t))
        a('          <text x="490" y="%d" font-size="10.5" fill="var(--ink-2)">%s</text>' % (yy + 14, s1))
        a('          <text x="490" y="%d" font-size="10" fill="var(--muted)">%s</text>' % (yy + 27, s2))
    a('        </g>')
    a('        <g font-family="IBM Plex Mono, monospace" font-size="10" fill="var(--muted)">')
    a('          <text x="34" y="22">CORTE NO EIXO DO BICO · escala %d:1 · o mesmo nas três posições</text>' % S)
    a('          <text x="34" y="%d">verde: tampa e gaveta · laranja: TPE · hachura: o pote</text>'
      % (H_SVG - 12))
    a('        </g>')
    a('      </svg>')
    return '\n'.join(o)


if __name__ == '__main__':
    q = sys.argv[1] if len(sys.argv) > 1 else 'curto'
    print(corte() if q == 'corte' else topo(q))
