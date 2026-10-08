#!/usr/bin/env python3
"""Conferencia de MONTAGEM: mede nas MALHAS, nao nas constantes.

Na revisao 7 o filete saiu 0,40 mm aquem da boca. Malha estanque, normais
certas, volume positivo - nenhuma checagem de malha acusa, porque a peca
sozinha esta perfeita. O que estava errado era a RELACAO entre duas pecas.
Este script lanca um raio pelo meio de cada lado e lista onde ele atravessa
material, em cada peca, na mesma altura. E a unica conferencia que pega isso.

Uso:  python3 verifica-montagem.py
"""
import os, struct, sys

BASE = os.path.dirname(os.path.abspath(__file__))


def ler(nome):
    b = open(os.path.join(BASE, 'stl', nome), 'rb').read()
    n = struct.unpack('<I', b[80:84])[0]
    T = []
    for i in range(n):
        o = 84 + i * 50 + 12
        T.append(tuple(struct.unpack('<3f', b[o + k * 12:o + k * 12 + 12]) for k in range(3)))
    return T


def cruzamentos(T, z, eixo, desvio=0.0):
    """X (ou Y) onde o raio, na altura z, atravessa a casca.

    eixo 'x': raio ao longo de X com y=desvio (corta o lado CURTO).
    eixo 'y': raio ao longo de Y com x=desvio (corta o lado COMPRIDO).

    O desvio precisa existir desde que a tampa ganhou nervuras: ha uma nervura
    em cima de cada eixo, e um raio passando por cima dela sai com cruzamentos
    degenerados - a medida da lingueta vinha com a nervura no meio.
    """
    a, b = (0, 1) if eixo == 'x' else (1, 0)
    out = []
    for tri in T:
        # segmento da interseccao do triangulo com o plano z
        p = []
        for i in range(3):
            q, r = tri[i], tri[(i + 1) % 3]
            dq, dr = q[2] - z, r[2] - z
            if dq == 0.0:
                p.append(q)
            elif dq * dr < 0:
                f = dq / (dq - dr)
                p.append(tuple(q[k] + f * (r[k] - q[k]) for k in range(3)))
        if len(p) < 2:
            continue
        s, e = p[0], p[1]
        # onde esse segmento cruza a linha do raio (coordenada b = 0).
        # Um vertice EM CIMA da linha (b == 0) e caso comum aqui, porque as
        # faces das travas sao quads partidos ao meio: testar so o produto de
        # sinais perde essas faces e a peca parece nao ter gancho nenhum.
        sb, eb = s[b] - desvio, e[b] - desvio
        if sb == 0.0:
            out.append(s[a])
        elif eb == 0.0:
            out.append(e[a])
        elif sb * eb < 0:
            f = sb / (sb - eb)
            out.append(s[a] + f * (e[a] - s[a]))
    return sorted({round(v, 3) for v in out if v > 0})


def raio_z(T, x0, y0):
    """z onde uma reta vertical em (x0,y0) atravessa a casca, ordenados.

    E a unica maneira honesta de perguntar "aqui tem furo?" a uma malha: se a
    janela estiver fechada, o raio cruza; se estiver aberta, nao cruza.
    """
    out = []
    for a, b, c in T:
        # coordenadas baricentricas no plano XY
        d = ((b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1]))
        if abs(d) < 1e-12:
            continue
        l1 = ((b[1] - c[1]) * (x0 - c[0]) + (c[0] - b[0]) * (y0 - c[1])) / d
        l2 = ((c[1] - a[1]) * (x0 - c[0]) + (a[0] - c[0]) * (y0 - c[1])) / d
        l3 = 1.0 - l1 - l2
        if l1 < 1e-9 or l2 < 1e-9 or l3 < 1e-9:
            continue
        out.append(l1 * a[2] + l2 * b[2] + l3 * c[2])
    return sorted(out)


def intervalos(zs):
    return [(round(zs[i], 2), round(zs[i + 1], 2)) for i in range(0, len(zs) - 1, 2)]


def bocal():
    """A tampa de bocal: o furo e furo, o colar sobe, o plug aperta, a saia
    do fecho veste o colar sem bater nele e sem bater no deck."""
    import importlib.util
    sp = importlib.util.spec_from_file_location('cb', os.path.join(BASE, 'calculo-bocal.py'))
    cb = importlib.util.module_from_spec(sp); sp.loader.exec_module(cb)

    L = ler('tampa-bocal.stl')
    F = ler('fecho-bocal.stl')
    ok = True

    def diz(rot, cond, txt):
        nonlocal ok
        ok = ok and cond
        print('  %-38s %s  %s' % (rot, 'OK ' if cond else 'FALHA', txt))

    print('\n=== TAMPA DE BOCAL ===')

    print('\n11) O GARGALO E FURO MESMO, E SOBE OS 14 mm')
    dentro = intervalos(raio_z(L, cb.X_GARG, 0.0))
    # a parede do colar e inclinada 3°: medir no meio dela, na altura do aro,
    # e perguntar a cb onde ela esta - nao supor que esta onde estava embaixo
    y_par = (cb.GARG_W / 2 + cb.colar_ext(cb.Z_COL)[1] / 2) / 2
    parede = intervalos(raio_z(L, cb.X_GARG, y_par))
    print('   raio no eixo do furo:', dentro)
    print('   raio na parede do colar (y=%.2f):' % y_par, parede)
    diz('nada de tampa no eixo do furo', not dentro,
        'o furo atravessa o deck inteiro')
    diz('o colar sobe ate %+.2f' % cb.Z_COL,
        bool(parede) and abs(parede[-1][1] - cb.Z_COL) < 0.01,
        'aro do colar em %+.2f (eram +5,50 na revisao 13)'
        % (parede[-1][1] if parede else 0))
    diz('e desce ate a face de baixo do deck',
        bool(parede) and abs(parede[0][0] - cm_Z_DECK_B) < 0.01,
        'pe em %+.2f' % (parede[0][0] if parede else 0))
    # os 3° de saida: a face externa tem de ser MAIS LARGA embaixo
    topo = cruzamentos(L, cb.Z_COL - 0.3, 'x', 0.0)
    base = cruzamentos(L, Z_MOD + 0.3, 'x', 0.0)
    alvo = cb.X_GARG + cb.GARG_L / 2 + cb.GARG_PAR
    perto = lambda v, a: min((q for q in v if abs(q - a) < 2.5),
                             key=lambda q: abs(q - a)) if v else 0.0
    xt, xb = perto(topo, alvo), perto(base, alvo + 1.0)
    esperado = (cb.colar_ext(Z_MOD + 0.3)[0] - cb.colar_ext(cb.Z_COL - 0.3)[0]) / 2
    print('   face externa do colar: %.3f no aro, %.3f no pe (+%.3f)'
          % (xt, xb, xb - xt))
    diz('a face externa tem os 3° de saida', abs((xb - xt) - esperado) < 0.05,
        'alarga %.3f mm do aro ao pe; a conta pede %.3f' % (xb - xt, esperado))

    print('\n12) O PLUG APERTA DENTRO DO GARGALO')
    # no ARO o plug entra folgado; no fim do curso ele aperta. Medir nos dois.
    for nome, d, sinal in (('aro', 0.3, -1), ('fim', cb.PLUG_H - 0.3, +1)):
        z = cb.Z_COL - d
        g = cruzamentos(L, z, 'x', 0.0)
        pg = cruzamentos(F, z, 'x', 0.0)
        # Nessa altura o raio pega o colar e a saia do fecho. A face do furo e
        # a que cai perto de X_GARG + GARG_L/2 - selecionar por POSICAO, nao
        # por ordem: pegar "o maior cruzamento" entregava a saia.
        alvo = cb.X_GARG + cb.GARG_L / 2
        furo, plug = perto(g, alvo), perto(pg, alvo)
        delta = plug - furo
        print('   em %-4s (z=%+.2f): furo %.3f | plug %.3f -> %+.3f'
              % (nome, z, furo, plug, delta))
        if sinal < 0:
            diz('no aro o plug entra folgado', delta < 0,
                '%.3f mm/lado de folga (pedia %.2f)' % (-delta, cb.PLUG_BOCA))
        else:
            diz('no fim do curso o plug aperta', delta > 0.1,
                '%.3f mm/lado de interferencia' % delta)

    print('\n13) A SAIA DO FECHO VESTE O COLAR SEM ENCOSTAR')
    # no meio da saia: a saia do fecho e a parede do colar tem de aparecer
    # como dois solidos SEPARADOS no mesmo raio horizontal
    zm = (cb.Z_COL + cb.Z_SAIA) / 2
    xs_f = cruzamentos(F, zm, 'x', 0.0)
    xs_l = cruzamentos(L, zm, 'x', 0.0)
    # Nesta altura o raio pega QUATRO faces do fecho (plug por dentro e por
    # fora, saia por dentro e por fora) e duas do colar. Pegar por ordem
    # entrega o plug no lugar da saia - a primeira versao desta conferencia
    # mediu exatamente isso e acusou folga negativa de 3 mm. Selecionar por
    # POSICAO, com a posicao vindo de cb: a mesma licao de secao_calha().
    p_col = cb.X_GARG + cb.colar_ext(zm)[0] / 2
    p_si = cb.X_GARG + cb.saia_int(zm)[0] / 2
    p_se = cb.X_GARG + cb.saia_ext(zm)[0] / 2
    col, si, se = perto(xs_l, p_col), perto(xs_f, p_si), perto(xs_f, p_se)
    print('   em z=%+.2f: colar %.3f | saia %.3f por dentro, %.3f por fora'
          % (zm, col, si, se))
    diz('ha folga entre a saia e o colar', (si - col) > 0.05,
        '%.3f mm de folga (a conta pede %.2f)' % (si - col, cb.FECHO_FOLGA))
    diz('a saia tem a parede prevista', abs((se - si) - cb.FECHO_PAR) < 0.06,
        '%.3f mm de parede contra %.2f previsto' % (se - si, cb.FECHO_PAR))
    # a borda de baixo da saia nao pode chegar no deck
    diz('a borda da saia para acima do deck',
        abs(min(v[2] for t in F for v in t) - cb.Z_SAIA) < 0.01
        and cb.Z_SAIA > Z_MOD + 1.0,
        'borda em %+.2f, deck em %+.2f: %.2f mm de pescoco a vista'
        % (cb.Z_SAIA, Z_MOD, cb.PESCOCO))

    print('\n14) O FECHO: ARO PLANO DE BATENTE, DOMO OCO, SEM VAZIO FECHADO')
    meio = intervalos(raio_z(F, cb.X_GARG, 0.0))
    print('   raio no alto do domo:', meio)
    diz('o domo sobe ate o planalto', bool(meio)
        and abs(meio[-1][1] - cb.Z_DOMO) < 0.05,
        'planalto medido %+.2f, previsto %+.2f'
        % (meio[-1][1] if meio else 0, cb.Z_DOMO))
    diz('o domo e OCO, nao macico', bool(meio)
        and abs((meio[-1][1] - meio[-1][0]) - cb.FECHO_TOPO) < 0.05,
        '%.2f mm de PP no planalto, igual a casca' % (meio[-1][1] - meio[-1][0]))
    diz('abre para baixo: nada de vazio fechado', len(meio) == 1,
        'um solido so no eixo - vazio fechado apareceria como dois')
    # o ARO PLANO: no meio do aro do colar, o fecho tem de ter material
    # exatamente EM CIMA de Z_COL, que e o batente
    y_aro = (cb.GARG_W / 2 + cb.colar_ext(cb.Z_COL)[1] / 2) / 2
    bat_f = intervalos(raio_z(F, cb.X_GARG, y_aro))
    bat_l = intervalos(raio_z(L, cb.X_GARG, y_aro))
    print('   sobre o aro do colar (y=%.2f): fecho %s | colar %s'
          % (y_aro, bat_f, bat_l))
    diz('o fecho assenta no aro do colar', bool(bat_f) and bool(bat_l)
        and abs(bat_f[0][0] - cb.Z_COL) < 0.01
        and abs(bat_l[-1][1] - cb.Z_COL) < 0.01,
        'as duas faces se encontram em %+.2f - o fecho para no aro, nao no fundo'
        % cb.Z_COL)
    diz('e a altura do fecho e de pegar', (cb.Z_DOMO - cb.Z_SAIA) >= 10.0,
        '%.2f mm de fecho (eram 8,60 na revisao 13)' % (cb.Z_DOMO - cb.Z_SAIA))
    return ok


cm_Z_DECK_B = -3.50
Z_MOD = -2.00
cm_PP_FLANGE = 1.20
cm_PP_DECK = 1.50


def main():
    import importlib.util
    sp = importlib.util.spec_from_file_location('cm', os.path.join(BASE, 'calculo-modular.py'))
    cm = importlib.util.module_from_spec(sp); sp.loader.exec_module(cm)
    T05 = 0.008727                       # tan(0,5°)

    p = cm.linha(cm.footprint())[0]
    P = ler('pote-600.stl')
    L = ler('tampa-pp.stl')
    U = ler('aro-u.stl')
    K = ler('tampa-teca.stl')
    H = max(v[2] for t in P for v in t)
    dz = lambda z: H + z
    ok = True

    def diz(rot, cond, txt):
        nonlocal ok
        ok = ok and cond
        print('  %-38s %s  %s' % (rot, 'OK ' if cond else 'FALHA', txt))

    print('pote 600: topo da borda em z = %.1f mm' % H)

    print('\n1) ARO EM U x BOCA  (z = -5,0 mm, lado curto)')
    pot = cruzamentos(P, dz(-5.0), 'x')
    aro = cruzamentos(U, -5.0, 'x')
    print('   pote:', pot, '\n   aro em U:', aro)
    boca = min(pot)                       # face interna da boca
    # a boca tem saida: a 5 mm do topo ela ja fechou 0,04 mm/lado, e a
    # interferencia sobe na mesma medida.
    alvo = cm.ARO_COMP + 5.0 * T05
    diz('o U invade a boca', abs((max(aro) - boca) - alvo) < 0.02,
        '%.3f mm/lado (alvo %.3f com a saida)' % (max(aro) - boca, alvo))
    diz('o U e OCO: quatro faces no raio', len(aro) == 4,
        'perna de fora, vao da lingueta e perna de dentro')

    print('\n2) GANCHO x DENTE  (z = -8 mm, lado comprido)')
    acima = cruzamentos(P, dz(-7.9), 'y')
    abaixo = cruzamentos(P, dz(-8.1), 'y')
    gancho = cruzamentos(L, -8.25, 'y')
    print('   pote acima do dente:', acima, '\n   pote abaixo:', abaixo,
          '\n   tampa no gancho:', gancho)
    borda_o, corpo_o = max(acima), max(abaixo)
    gancho_i = min(gancho)
    # O alvo NAO e DENTE cheio: entre -7,9 e -8,1 a saida ja tirou 7,8*tan(0,5°)
    # da face da borda. E a malha e facetada - anel() nao poe vertice a 90°, so
    # pontas de arco, entao a corda do meio do lado comprido passa ~0,04 mm por
    # DENTRO da superficie real, e tanto mais quanto maior o raio do canto. Os
    # dois efeitos sao da ordem da cota que se esta medindo; ignorar qualquer um
    # faz a conferencia reprovar uma peca certa.
    alvo_dente = cm.DENTE - 7.8 * T05
    diz('o dente existe e tem a largura certa',
        abs((borda_o - corpo_o) - alvo_dente) < 0.05,
        '%.3f mm/lado (alvo %.3f: dente %.2f menos a saida)'
        % (borda_o - corpo_o, alvo_dente, cm.DENTE))
    # mesma faceta do lado do pote; a trava e prisma reto e nao tem faceta.
    diz('gancho entra sob o dente',
        abs((borda_o - gancho_i) - cm.TRAVA_FARPA) < 0.06,
        'avanca %.3f mm da face da borda (alvo %.2f)'
        % (borda_o - gancho_i, cm.TRAVA_FARPA))
    diz('gancho nao bate no corpo', gancho_i >= corpo_o - 0.01,
        'corpo em %.2f, ponta do gancho em %.2f' % (corpo_o, gancho_i))

    print('\n3) TRAVA x FACE EXTERNA DA BORDA  (z = -5 mm, lado comprido)')
    pot5 = cruzamentos(P, dz(-5.0), 'y')
    tam5 = cruzamentos(L, -5.0, 'y')
    print('   pote:', pot5, '\n   tampa:', tam5)
    trava_i = min(v for v in tam5 if v > max(pot5))
    diz('folga da trava sobre a borda', 0.28 <= (trava_i - max(pot5)) <= 0.45,
        '%.2f mm (%.2f no topo, mais o que a saida abre)'
        % (trava_i - max(pot5), cm.TRAVA_FOLGA))

    print('\n4) ABA x MEIA-CANA DO TOPO  (lado curto)')
    topo = cruzamentos(P, dz(-0.3), 'x')
    aba = cruzamentos(L, 0.6, 'x')
    print('   pote junto ao topo:', topo, '\n   tampa (aba):', aba)
    diz('a aba cobre a borda inteira', max(aba) > max(topo),
        'aba %.2f x borda %.2f' % (max(aba), max(topo)))
    diz('a aba pousa na meia-cana', min(aba) < (max(topo) + min(topo)) / 2,
        'a aba chega a %.2f, o apice da meia-cana esta em %.2f'
        % (min(aba), (max(topo) + min(topo)) / 2))

    print('\n5) DECK x FUNDO DO POTE DE CIMA  (lado curto)')
    fundo = max(cruzamentos(P, 0.05, 'x'))
    band = cruzamentos(L, -1.9, 'x')
    print('   fundo do pote: %.2f' % fundo, '\n   saia da tampa:', band)
    diz('folga do fundo dentro da saia', 0.4 < (min(band) - fundo) < 1.3,
        '%.2f mm/lado (pedia %.2f)' % (min(band) - fundo, cm.BANDEJA_FE))

    print('\n6) PLANO MODULAR')
    piso = cruzamentos(L, -2.0 + 0.05, 'x')
    diz('o deck existe em z=-2,00', bool(piso), '2,0 mm abaixo do topo da borda')

    print('\n7) A PLACA DE TECA POUSA NO DEGRAU  (lado curto)')
    z_teca = min(v[2] for t in K for v in t)
    z_top_teca = max(v[2] for t in K for v in t)
    # o degrau do pote: a boca acima dele, o corpo abaixo
    acima_d = cruzamentos(P, dz(cm.Z_DEGRAU + 0.3), 'x')
    abaixo_d = cruzamentos(P, dz(cm.Z_DEGRAU - 0.3), 'x')
    print('   placa de %.2f a %.2f | boca acima do degrau %.2f | corpo abaixo %.2f'
          % (z_teca, z_top_teca, min(acima_d), min(abaixo_d)))
    diz('a placa chega ao degrau', abs(z_teca - cm.Z_DEGRAU) < 0.01,
        'fundo da placa em %+.2f, degrau em %+.2f' % (z_teca, cm.Z_DEGRAU))
    diz('e o topo dela cai no plano modular', abs(z_top_teca - cm.Z_MOD) < 0.01,
        'topo em %+.2f' % z_top_teca)
    teca_x = max(cruzamentos(K, -4.0, 'x'))
    diz('a placa nao passa pelo degrau', teca_x > min(abaixo_d),
        'placa %.2f contra o corpo %.2f: ela POUSA, nao cai' % (teca_x, min(abaixo_d)))

    print('\n8) A FARPA QUE SEGURA O ARO  (lado comprido, fora das nervuras)')
    z_omb = cm.Z_DECK_B - (cm.LING_H - cm.DENTE_ARO_H - cm.DENTE_ARO_R)
    z_far = z_omb - cm.DENTE_ARO_H / 2            # meio do trecho cheio da farpa
    DES = 12.0                                    # desvio do raio: ha nervura no eixo
    # nessa altura o raio pega TRES coisas: nervuras, a lingueta e a trava.
    # Pegar os dois ultimos cruzamentos entrega a TRAVA. A lingueta e o par em
    # volta de LING_O - selecionar por posicao, nao por ordem.
    LING_O = p['boca'] - 2 * cm.SAIA_FOLGA - 2 * cm.RECUO
    alvo = (LING_O - p['dLW']) / 2
    par = lambda v: [q for q in v if alvo - 1.5 <= q <= alvo + 1.0]
    cima = par(cruzamentos(L, z_omb + 0.20, 'y', DES))
    farpa = par(cruzamentos(L, z_far, 'y', DES))
    print('   lingueta acima do ombro:', cima, '\n   na farpa:', farpa)
    esp_cima = cima[-1] - cima[0]
    esp_farpa = farpa[-1] - farpa[0]
    diz('lingueta tem %.2f mm acima do ombro' % cm.LING_T,
        abs(esp_cima - cm.LING_T) < 0.03, '%.3f mm' % esp_cima)
    diz('e %.2f mm na farpa' % (cm.LING_T + 2 * cm.DENTE_ARO),
        abs(esp_farpa - cm.LING_T - 2 * cm.DENTE_ARO) < 0.03, '%.3f mm' % esp_farpa)
    diz('o degrau avanca %.2f por face' % cm.DENTE_ARO,
        abs((farpa[-1] - cima[-1]) - cm.DENTE_ARO) < 0.04,
        '%.3f mm - e esta face que o aro tem de vencer para cair'
        % (farpa[-1] - cima[-1]))
    vao_cima = cruzamentos(U, z_omb + 0.20, 'y', DES)
    vao_farpa = cruzamentos(U, z_far, 'y', DES)
    print('   vao do U acima do ombro:', vao_cima, '\n   na farpa:', vao_farpa)
    # o vao e o par do MEIO (as quatro faces sao: perna de dentro, vao, perna
    # de fora). vao_farpa[1]-vao_farpa[0] seria a espessura da perna.
    s_cima = vao_cima[2] - vao_cima[1]
    s_farpa = vao_farpa[2] - vao_farpa[1]
    diz('o vao do U abre na BOLSA',
        len(vao_farpa) >= 4 and len(vao_cima) >= 4
        and s_farpa > s_cima + 2 * cm.DENTE_ARO - 0.05,
        'de %.2f para %.2f mm: o silicone RELAXA em cima da farpa'
        % (s_cima, s_farpa))

    print('\n9) AS NERVURAS SOB O DECK')
    nv = cm.nervuras(DECK_U := (p['boca'] - 2 * cm.SAIA_FOLGA - 2 * cm.SAIA_T),
                     (p['boca'] - 2 * cm.SAIA_FOLGA - 2 * cm.SAIA_T) - p['dLW'])
    col = intervalos(raio_z(L, nv['xs'][1], 2.0))
    livre = intervalos(raio_z(L, (nv['xs'][1] + nv['xs'][2]) / 2, 2.0))
    print('   raio em cima de uma nervura:', col, '\n   raio no meio da celula:', livre)
    diz('a nervura desce ate %+.2f' % (cm.Z_DECK_B - cm.NERV_H),
        bool(col) and abs(col[0][0] - (cm.Z_DECK_B - cm.NERV_H)) < 0.01,
        'fundo da nervura em %+.2f' % (col[0][0] if col else 0))
    diz('fora dela so ha o deck', bool(livre)
        and abs((livre[0][1] - livre[0][0]) - cm.PP_DECK) < 0.01,
        'deck de %.2f mm' % (livre[0][1] - livre[0][0] if livre else 0))
    diz('a nervura nao alcanca o degrau do pote',
        bool(col) and col[0][0] > cm.Z_DEGRAU,
        '%.2f mm de folga para o degrau em %+.2f'
        % ((col[0][0] - cm.Z_DEGRAU) if col else 0, cm.Z_DEGRAU))

    ok2 = bocal()
    print('\nMONTAGEM:', 'OK' if (ok and ok2) else 'FALHOU')
    return 0 if (ok and ok2) else 1


if __name__ == '__main__':
    sys.exit(main())
