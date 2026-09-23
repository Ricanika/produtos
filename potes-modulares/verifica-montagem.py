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

    print('\n10) O VERTEDOURO NAO CORTA O FILETE')
    plug = intervalos(raio_z(L, ccr.PLUG / 2 - 0.3, 0.0))
    print('   raio na parede do plug, no eixo do bico:', plug)
    diz('parede do plug some acima do friso', bool(plug) and plug[-1][1] < -0.9,
        'topo do plug no entalhe em %+.2f (friso comeca em -3,00)' % plug[-1][1])
    diz('plug inteiro abaixo do friso', bool(plug) and plug[0][0] < -4.4,
        'vai ate %+.2f' % plug[0][0])
    return ok


cm_PP_DECK = 1.50


def main():
    P = ler('pote-600.stl')
    L = ler('tampa-pp.stl')
    F = ler('filete-tpe.stl')
    H = max(v[2] for t in P for v in t)
    dz = lambda z: H + z
    ok = True

    def diz(rot, cond, txt):
        nonlocal ok
        ok = ok and cond
        print('  %-38s %s  %s' % (rot, 'OK ' if cond else 'FALHA', txt))

    print('pote 600: topo da borda em z = %.1f mm' % H)

    print('\n1) FILETE x BOCA  (z = -3,7 mm, lado curto)')
    pot = cruzamentos(P, dz(-3.7), 'x')
    fil = cruzamentos(F, -3.7, 'x')
    print('   pote:', pot, '\n   filete:', fil)
    boca = min(pot)                       # face interna da boca
    # o filete e de secao constante e a boca tem saida: a 3,7 mm do topo a boca
    # ja fechou 0,03 mm/lado, e a interferencia sobe na mesma medida.
    alvo = 0.20 + 3.7 * 0.008727
    diz('filete invade a boca', abs((max(fil) - boca) - alvo) < 0.02,
        '%.3f mm/lado (alvo %.3f com a saida)' % (max(fil) - boca, alvo))

    print('\n2) GANCHO x ARESTA DE ENGATE  (z = -10 mm, lado comprido)')
    acima = cruzamentos(P, dz(-9.9), 'y')
    abaixo = cruzamentos(P, dz(-10.1), 'y')
    gancho = cruzamentos(L, -10.25, 'y')
    print('   pote acima da aresta:', acima, '\n   pote abaixo:', abaixo,
          '\n   tampa no gancho:', gancho)
    saia_o, saia_i = max(acima), sorted(acima)[-2]
    gancho_i = min(gancho)
    diz('aresta de engate', abs((saia_o - saia_i) - 1.20) < 0.06,
        '%.2f mm/lado (alvo 1,20)' % (saia_o - saia_i))
    diz('gancho entra sob a aresta', saia_o - gancho_i > 0.7,
        'avanca %.2f mm da face da saia (aresta tem %.2f)'
        % (saia_o - gancho_i, saia_o - saia_i))
    diz('gancho nao bate na perna', gancho_i >= max(abaixo) - 0.01,
        'perna em %.2f, ponta do gancho em %.2f' % (max(abaixo), gancho_i))

    print('\n3) TRAVA x FACE EXTERNA DA BORDA  (z = -5 mm, lado comprido)')
    pot5 = cruzamentos(P, dz(-5.0), 'y')
    tam5 = cruzamentos(L, -5.0, 'y')
    print('   pote:', pot5, '\n   tampa:', tam5)
    # a trava e a primeira face da tampa que fica FORA da borda; as menores
    # sao o plug e a parede da bandeja, que estao dentro.
    trava_i = min(v for v in tam5 if v > max(pot5))
    diz('folga da trava sobre a borda', 0.28 <= (trava_i - max(pot5)) <= 0.45,
        '%.2f mm (0,30 no topo, mais o que a saida abre)' % (trava_i - max(pot5)))

    print('\n4) DECK x TOPO DA BORDA  (z = -0,5 mm, lado curto)')
    topo = cruzamentos(P, dz(-0.5), 'x')
    deck = cruzamentos(L, 0.75, 'x')
    print('   pote:', topo, '\n   tampa (deck):', deck)
    diz('deck cobre a borda inteira', max(deck) > max(topo),
        'deck %.2f x borda %.2f' % (max(deck), max(topo)))

    print('\n5) BANDEJA x FUNDO DO POTE DE CIMA  (lado curto)')
    fundo = max(cruzamentos(P, 0.05, 'x'))
    band = cruzamentos(L, -1.9, 'x')
    print('   fundo do pote: %.2f' % fundo, '\n   bandeja:', band)
    # a bandeja tem duas faces: a de DENTRO (onde o fundo encosta) e a de fora.
    diz('folga do fundo na bandeja', 0.5 < (min(band) - fundo) < 1.2,
        '%.2f mm/lado' % (min(band) - fundo))

    print('\n6) PLANO MODULAR')
    piso = cruzamentos(L, -2.0, 'x')
    diz('piso da bandeja existe em z=-2,00', bool(piso), '2,0 mm abaixo do topo da borda')

    ok2 = correr()
    print('\nMONTAGEM:', 'OK' if (ok and ok2) else 'FALHOU')
    return 0 if (ok and ok2) else 1


if __name__ == '__main__':
    sys.exit(main())
