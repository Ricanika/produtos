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


def bico():
    """A tampa de bico: o furo e furo, o plug aperta, a calha nao corta a aba."""
    import importlib.util
    sp = importlib.util.spec_from_file_location('cb', os.path.join(BASE, 'calculo-bico.py'))
    cb = importlib.util.module_from_spec(sp); sp.loader.exec_module(cb)

    L = ler('tampa-bico.stl')
    F = ler('fecho-bico.stl')
    ok = True

    def diz(rot, cond, txt):
        nonlocal ok
        ok = ok and cond
        print('  %-38s %s  %s' % (rot, 'OK ' if cond else 'FALHA', txt))

    print('\n=== TAMPA DE BICO ===')

    print('\n11) O GARGALO E FURO MESMO')
    dentro = intervalos(raio_z(L, cb.X_GARG, 0.0))
    parede = intervalos(raio_z(L, cb.X_GARG, cb.GARG_W / 2 + cb.GARG_PAR / 2))
    print('   raio no eixo do furo:', dentro)
    print('   raio na parede do colar:', parede)
    diz('nada de tampa no eixo do furo', not dentro,
        'o furo atravessa o deck inteiro')
    diz('o colar sobe ate +%.2f' % cb.Z_COL,
        bool(parede) and abs(parede[-1][1] - cb.Z_COL) < 0.01,
        'topo do colar em %+.2f' % (parede[-1][1] if parede else 0))
    diz('e desce ate a face de baixo do deck',
        bool(parede) and abs(parede[0][0] - cm_Z_DECK_B) < 0.01,
        'pe em %+.2f' % (parede[0][0] if parede else 0))

    print('\n12) O PLUG APERTA DENTRO DO GARGALO')
    # na BOCA o plug entra folgado; no PE ele aperta. Medir nos dois.
    for nome, d, sinal in (('boca', 0.3, -1), ('pe', cb.PLUG_H - 0.3, +1)):
        z = cb.Z_COL - d
        g = cruzamentos(L, z, 'x', 0.0)
        pg = cruzamentos(F, z, 'x', 0.0)
        # Nessa altura o raio pega o colar, o piso da calha e a aba. Pegar "o
        # maior cruzamento" entregava a ABA, nao o furo. A face do furo e a que
        # cai perto de X_GARG + GARG_L/2 - selecionar por posicao, nao por ordem.
        alvo = cb.X_GARG + cb.GARG_L / 2
        perto = lambda v: min((q for q in v if abs(q - alvo) < 1.5),
                              key=lambda q: abs(q - alvo))
        furo, plug = perto(g), perto(pg)
        delta = plug - furo
        print('   em %-4s (z=%+.2f): furo %.3f | plug %.3f -> %+.3f'
              % (nome, z, furo, plug, delta))
        if sinal < 0:
            diz('na boca o plug entra folgado', delta < 0,
                '%.3f mm/lado de folga (pedia %.2f)' % (-delta, cb.PLUG_BOCA))
        else:
            diz('no pe o plug aperta', delta > 0.1,
                '%.3f mm/lado de interferencia' % delta)

    print('\n13) A CALHA NAO CORTA A ABA, E O LABIO NAO PINGA NO POTE')
    # medir no MEIO DO CURSO, e pedindo as cotas a secao_calha(): a calha abre
    # 6% ate aqui, entao a parede nao esta mais onde estava na raiz. Metade do
    # curso cai numa estacao da varredura, logo nao ha interpolacao na medida.
    xm = cb.X_RAIZ + (cb.X_LABIO - cb.X_RAIZ) * 0.5
    sc = cb.secao_calha(xm)
    eixo = intervalos(raio_z(L, xm, 0.0))
    lado = intervalos(raio_z(L, xm, sc['y_par']))
    print('   previsto em x=%.2f: piso %+.2f/%+.2f, parede %+.2f, canal %.2f'
          % (xm, sc['piso_fundo'], sc['piso_topo'], sc['parede'], sc['alt']))
    print('   raio no meio da calha, no eixo:', eixo)
    print('   raio na parede da calha (y=%.2f):' % sc['y_par'], lado)
    diz('o piso da calha fica acima da aba', bool(eixo) and eixo[-1][0] > cm_PP_FLANGE,
        'face de baixo do piso em %+.2f, aba em %+.2f'
        % (eixo[-1][0] if eixo else 0, cm_PP_FLANGE))
    diz('o piso esta onde a varredura promete', bool(eixo)
        and abs(eixo[-1][0] - sc['piso_fundo']) < 0.10
        and abs(eixo[-1][1] - sc['piso_topo']) < 0.10,
        'medido %+.2f/%+.2f contra %+.2f/%+.2f previsto'
        % ((eixo[-1][0] if eixo else 0, eixo[-1][1] if eixo else 0,
            sc['piso_fundo'], sc['piso_topo'])))
    diz('a parede sobe acima do piso', bool(lado) and bool(eixo)
        and lado[-1][1] > eixo[-1][1] + 1.0,
        '%.2f mm de canal aberto (previsto %.2f)'
        % ((lado[-1][1] - eixo[-1][1]) if eixo and lado else 0, sc['alt']))
    diz('a parede esta na altura prevista', bool(lado)
        and abs(lado[-1][1] - sc['parede']) < 0.15,
        'topo medido %+.2f contra %+.2f previsto'
        % (lado[-1][1] if lado else 0, sc['parede']))
    xl = cb.X_LABIO - 0.4
    sl = cb.secao_calha(xl)
    labio = intervalos(raio_z(L, xl, 0.0))
    print('   raio no labio:', labio)
    diz('o labio fica acima da aba', bool(labio) and labio[0][0] > cm_PP_FLANGE,
        'ponta do labio em %+.2f' % (labio[0][0] if labio else 0))
    diz('o labio e mais fino que o piso', bool(labio)
        and (labio[0][1] - labio[0][0]) < cb.CALHA_T * 0.5,
        '%.2f mm contra %.2f do piso (a varredura preve %.2f)'
        % ((labio[0][1] - labio[0][0]) if labio else 0, cb.CALHA_T, sl['esp']))
    # a calha e balanco: por baixo dela, fora da projecao do colar, nao pode
    # haver mais nenhum apoio - e o que deixa a peca lavavel com um pano.
    sob = [iv for iv in lado if iv[0] < cm_PP_FLANGE - 0.05]
    print('   o que existe sob a parede, abaixo da aba:', sob)
    diz('nada desce da calha ate a aba', not sob,
        'balanco limpo: %d solido(s) sob a parede' % len(sob))

    print('\n14) O FECHO: DOMO OCO, DESLOCADO, E SEM BATER NA CALHA')
    meio = intervalos(raio_z(F, cb.FECHO_CX, 0.0))
    print('   raio no alto do domo:', meio)
    diz('o domo sobe ate a crista', bool(meio)
        and abs(meio[-1][1] - cb.Z_DOMO) < 0.05,
        'crista medida %+.2f, prevista %+.2f'
        % (meio[-1][1] if meio else 0, cb.Z_DOMO))
    diz('o domo e OCO, nao macico', bool(meio)
        and abs((meio[-1][1] - meio[-1][0]) - cb.FECHO_DOMO) < 0.05,
        '%.2f mm de PP no meio do tampo (macico daria %.2f)'
        % ((meio[-1][1] - meio[-1][0]) if meio else 0,
           cb.FECHO_TOPO + cb.FECHO_DOMO))
    # a unha: o tampo passa da face do colar em -X, e e so la que ele passa
    unha = intervalos(raio_z(F, cb.FECHO_X0 + 0.4, 0.0))
    # o que tem de faltar debaixo da unha e o COLAR, nao o deck: o deck passa
    # por baixo de todo o tampo, e e justamente nele que a unha se apoia
    colar = [iv for iv in intervalos(raio_z(L, cb.FECHO_X0 + 0.4, 0.0))
             if iv[1] > cb.Z_MOD + 0.1]
    print('   raio na aba de unha: fecho', unha, '| colar', colar)
    diz('ha tampo onde nao ha colar', bool(unha) and not colar,
        'a unha pega %.2f mm de aba livre, com o deck por baixo' % cb.FECHO_ABA)
    # e a interferencia que importa: a raiz da parede da calha
    sc0 = cb.secao_calha(cb.X_RAIZ + 0.2)
    bate_f = intervalos(raio_z(F, cb.X_RAIZ + 0.2, sc0['y_par']))
    bate_l = intervalos(raio_z(L, cb.X_RAIZ + 0.2, sc0['y_par']))
    print('   na raiz da parede: fecho', bate_f, '| calha', bate_l)
    diz('o fecho nao invade a raiz da calha', bool(bate_l) and not bate_f,
        'a calha ocupa, o fecho nao: %.2f mm de folga em X' % cb.FECHO_FOLGA)
    diz('o tampo cobre o furo em todo o perimetro', cb.cobre_o_furo(),
        'sobra %.2f mm no pior ponto do perimetro' % cb.margem_do_tampo())
    return ok


cm_Z_DECK_B = -3.50
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

    ok2 = bico()
    print('\nMONTAGEM:', 'OK' if (ok and ok2) else 'FALHOU')
    return 0 if (ok and ok2) else 1


if __name__ == '__main__':
    sys.exit(main())
