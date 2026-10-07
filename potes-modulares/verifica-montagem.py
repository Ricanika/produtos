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


def cruzamentos(T, z, eixo):
    """X (ou Y) onde o raio pelo centro, na altura z, atravessa a casca.

    eixo 'x': raio ao longo de X com y=0 (corta o lado CURTO).
    eixo 'y': raio ao longo de Y com x=0 (corta o lado COMPRIDO).
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
        if s[b] == 0.0:
            out.append(s[a])
        elif e[b] == 0.0:
            out.append(e[a])
        elif s[b] * e[b] < 0:
            f = s[b] / (s[b] - e[b])
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


def correr():
    """A tampa de correr: furo, calha e gaveta, medidos na malha."""
    import importlib.util
    sp = importlib.util.spec_from_file_location('ccr', os.path.join(BASE, 'calculo-correr.py'))
    ccr = importlib.util.module_from_spec(sp); sp.loader.exec_module(ccr)
    pz = next(q for q in ccr.POSICOES if q['cod'] == 'curto')
    g = ccr.geometria(pz)
    jan_cx = ccr.BANDEJA / 2 - g['rec']
    bol_cx = jan_cx - g['curso'] / 2

    L = ler('tampa-correr.stl')
    G = ler('gaveta.stl')
    A = ler('aro2-tpe.stl')
    P = ler('pote-600.stl')
    H = max(v[2] for t in P for v in t)
    ok = True

    def diz(rot, cond, txt):
        nonlocal ok
        ok = ok and cond
        print('  %-38s %s  %s' % (rot, 'OK ' if cond else 'FALHA', txt))

    print('\n=== TAMPA DE CORRER ===')
    print('\n7) A JANELA E FURO MESMO')
    jan = intervalos(raio_z(L, jan_cx, 0.0))
    fora = intervalos(raio_z(L, bol_cx - g['bolso_l'] / 2 + 3.0, 0.0))
    print('   raio no centro da janela:', jan)
    print('   raio no bolso, fora da janela:', fora)
    diz('nada de tampa no eixo da janela', not jan, 'o furo atravessa o piso')
    diz('piso existe fora da janela', any(abs(b - a - cm_PP_DECK) < 0.05 for a, b in fora),
        'espessura %.2f mm' % (fora[0][1] - fora[0][0] if fora else 0))

    print('\n8) A GAVETA FECHA A JANELA')
    gav = intervalos(raio_z(G, jan_cx, 0.0))
    print('   raio no centro da janela, na gaveta:', gav)
    diz('gaveta cobre a janela', len(gav) == 1 and abs(gav[0][1] - gav[0][0] - ccr.GAV_T) < 0.05,
        'painel de %.2f mm no eixo da janela' % (gav[0][1] - gav[0][0] if gav else 0))
    diz('topo da gaveta no plano modular', bool(gav) and abs(gav[0][1] - ccr.Z_MOD) < 0.01,
        'topo em %+.2f' % (gav[0][1] if gav else 0))
    aro = intervalos(raio_z(A, jan_cx + g['jan_d'] / 2 + 2.0, 0.0))
    diz('2o aro sobra do friso', bool(aro) and
        abs((ccr.Z_MOD - ccr.GAV_T) - aro[0][0] - ccr.ARO2_SOB) < 0.02,
        'sobra %.2f mm abaixo da gaveta' % ((ccr.Z_MOD - ccr.GAV_T) - aro[0][0] if aro else 0))

    print('\n9) A CALHA EM U')
    eixo = intervalos(raio_z(L, ccr.DECK_O / 2 - 1.0, 0.0))
    lado = intervalos(raio_z(L, ccr.DECK_O / 2 - 1.0, pz['bico_w'] / 2 + ccr.BICO_PAR / 2))
    print('   raio no eixo do bico, junto a ponta:', eixo)
    print('   raio na parede da calha:', lado)
    diz('piso da calha em +%.2f' % ccr.Z_SEL,
        bool(eixo) and abs(eixo[-1][1] - ccr.Z_SEL) < 0.01,
        'topo do piso em %+.2f' % (eixo[-1][1] if eixo else 0))
    diz('parede da calha chega a +%.2f' % ccr.Z_TOPO,
        bool(lado) and abs(lado[-1][1] - ccr.Z_TOPO) < 0.01,
        'topo da parede em %+.2f' % (lado[-1][1] if lado else 0))
    diz('canal aberto em cima', bool(eixo) and bool(lado) and eixo[-1][1] < lado[-1][1] - 2.0,
        '%.2f mm de profundidade util' % ((lado[-1][1] - eixo[-1][1]) if eixo and lado else 0))

    print('\n10) O VERTEDOURO NAO CORTA A LINGUETA NEM O ARO')
    import importlib.util as _il
    _s2 = _il.spec_from_file_location('cm2', os.path.join(BASE, 'calculo-modular.py'))
    cm = _il.module_from_spec(_s2); _s2.loader.exec_module(cm)
    saia_o = ccr.PLUG
    ling = intervalos(raio_z(L, saia_o / 2 - cm.RECUO - cm.LING_T / 2, 0.0))
    print('   raio no meio da lingueta, NO EIXO DO BICO:', ling)
    print('   (era aqui que a revisao 9 cortava o friso do filete)')
    fundo_ling = cm.Z_DECK_B - cm.LING_H
    diz('a lingueta existe inteira sob o bico', bool(ling)
        and ling[0][0] <= fundo_ling + 0.01 and ling[-1][1] >= cm.Z_DECK_B - 0.01,
        'de %+.2f a %+.2f (lingueta vai de %+.2f a %+.2f)'
        % (ling[0][0], ling[-1][1], fundo_ling, cm.Z_DECK_B))
    diz('o piso da calha fica ACIMA da banda do aro',
        ccr.Z_SEL > cm.Z_DECK_B,
        'calha em %+.2f, topo do aro em %+.2f: %.2f mm de distancia'
        % (ccr.Z_SEL, cm.Z_DECK_B, ccr.Z_SEL - cm.Z_DECK_B))
    return ok


cm_PP_DECK = 1.50


def main():
    import importlib.util
    sp = importlib.util.spec_from_file_location('cm', os.path.join(BASE, 'calculo-modular.py'))
    cm = importlib.util.module_from_spec(sp); sp.loader.exec_module(cm)
    T05 = 0.008727                       # tan(0,5°)

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

    ok2 = correr()
    print('\nMONTAGEM:', 'OK' if (ok and ok2) else 'FALHOU')
    return 0 if (ok and ok2) else 1


if __name__ == '__main__':
    sys.exit(main())
