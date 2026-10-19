#!/usr/bin/env python3
"""
CUBAGEM NA CAIXA MASTER DA NATURA/AVON - 460 x 210 x 286 mm.

A caixa master deixa de ser consequencia do produto e passa a ser COTA DE
ENTRADA dele. Isso inverte o solver: hoje calculo-modular.py recebe (aspecto,
modulo) e devolve a borda que fecha 600 ml; aqui a caixa FORCA os tres de uma
vez - o passo vem da altura, o aspecto e a borda vem do piso - e a capacidade
e o que sobra para ser lida, nao escolhida.

AS TRES COISAS QUE NAO CABEM JUNTAS
  1. a caixa fecha exata (sem espacinho);
  2. as capacidades sao 600 / 1200 / 1800 / 2400 ml redondos;
  3. o footprint continua 147,5 x 84,3 com aspecto 1,75.
  Sao tres equacoes e dois graus de liberdade. Uma cede, e a escolha de QUAL
  cede e a decisao comercial - nao tecnica. Este arquivo mostra o preco de
  cada uma.

O QUE A ALGEBRA MODULAR JA DA DE GRACA
  Pilha de S modulos tem altura S*M + BASE_T, seja ela um pote de 4 modulos,
  dois de 2, ou quatro de 1. Entao basta a ALTURA UTIL DA CAIXA ser um numero
  inteiro de modulos mais 2,00 mm:

      286 = S * M + 2   ->   M = 284 / S

  e QUALQUER combinacao dos quatro tamanhos fecha a altura exata. Isso ja e um
  argumento de venda para a Natura: uma caixa master, qualquer mix, sempre
  cheia. Nenhum concorrente de parede reta tem isso sem o dente modular.

A MEDIDA QUE MANDA NAO E A DO POTE
  Malha medida: pote 147,45 x 84,25 | tampa de PP 148,06 x 89,47. Quem empilha
  na caixa e o CONJUNTO, entao o modulo de cubagem e 148,06 x 89,47 - e a
  largura e maior que a do pote porque as duas travas ficam nos lados
  compridos. A ficha publicava 149,7 x 89,5 (supondo trava nos quatro lados);
  1,6 mm de erro em cubagem vira caixa a menos no caminhao.

Uso:  python3 calculo-cubagem.py
"""
import importlib.util, math, os

_BASE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('cm', os.path.join(_BASE, 'calculo-modular.py'))
cm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cm)

# ---- a caixa ----
CX, CY, CZ = 460.0, 210.0, 286.0        # como o Ricardo passou, em mm
# Folga de manuseio. "Sem sobrar nenhum espacinho" nao pode ser zero literal:
# o pote injetado tem +-0,3 mm, a caixa de ondulado tem +-2 mm, e produto que
# entra sem folga tambem nao SAI. Projeto-se para o nominal com esta folga, e
# ela e por EIXO (metade de cada lado).
FOLGA = 2.0

# ---- o que a tampa acrescenta ao pote, por lado ----
# comprimento: so a folga da trava sobre a face externa da borda (a aba)
# largura: folga + espessura da trava + o rabo de abrir
OVER_L = cm.TRAVA_FOLGA
OVER_W = cm.TRAVA_FOLGA + cm.TRAVA_T + cm.TRAVA_BULGE

DIV_X = [1, 2, 3, 4, 5, 6, 7, 8]
DIV_Y = [1, 2, 3, 4, 5, 6]

# ---- o que e um pote de mantimento, e o que nao e ----
# Sem estes limites o enumerador "resolve" a caixa com um pote de 457 mm de
# borda e 20 mm de passo - fecha a conta e nao e produto.
LIM_L   = (100.0, 200.0)    # borda, no comprimento
LIM_W   = (55.0, 130.0)     # borda, na largura
LIM_ASP = (1.35, 2.15)      # aspecto; hoje e 1,75 ("frente estreita")
LIM_MOD = (40.0, 95.0)      # passo: o pote de 1 modulo tem passo + 2 de altura
ALVOS   = [50 * k for k in range(8, 17)]   # modulos redondos: 400 a 800 ml


def capacidade(colar_l, asp, modulo, n, elev=0.0):
    """Capacidade REAL de um pote de n modulos, com o piso ELEV acima do fundo.

    Mesma conta de linha() em calculo-modular.py - os dois troncos, o do corpo
    e o da borda. La o elev e resolvido para forcar n*600; aqui ele e argumento,
    porque e justamente ele o grau de liberdade que falta.
    """
    colar_w = colar_l / asp
    dLW = colar_l - colar_w
    corpo_l = colar_l - 2 * cm.DENTE
    boca = colar_l - 2 * cm.BORDA_PAR
    w, H = cm.WALL[n], n * modulo + cm.BASE_T
    z_dente = H - cm.BORDA_H
    z_degrau = z_dente + cm.WEB_T
    piso = cm.BASE_T + elev
    if z_degrau <= piso or corpo_l <= 4 * w or colar_w <= 4 * w:
        return None
    corpo_z = lambda z: corpo_l - 2 * (z_dente - z) * cm.T
    if corpo_z(piso) - dLW - 2 * w <= 0:
        return None
    return (cm.tronco(corpo_z(piso) - 2 * w, corpo_z(z_degrau) - 2 * w,
                      z_degrau - piso, colar_l, dLW)
            + cm.tronco(boca - 2 * (H - z_degrau) * cm.T, boca,
                        cm.BORDA_H - cm.WEB_T, colar_l, dLW)) / 1e3


def resolve_elev(colar_l, asp, modulo, n, alvo):
    """Quanto o piso tem de subir para o pote fechar ALVO ml. None se nao da."""
    if (capacidade(colar_l, asp, modulo, n) or 0.0) < alvo:
        return None
    lo, hi = 0.0, modulo * n
    for _ in range(40):
        e = (lo + hi) / 2
        v = capacidade(colar_l, asp, modulo, n, e)
        lo, hi = (e, hi) if (v is not None and v > alvo) else (lo, e)
    return (lo + hi) / 2


def candidatos():
    """Todo arranjo em GRADE que fecha a caixa exata, com o que ele produz.

    So grade, e de proposito: arranjo com pecas giradas no meio da caixa e
    instrucao de montagem que ninguem segue. Grade o montador acerta de olho.

    Para cada arranjo a caixa FORCA tres coisas - passo, borda e aspecto - e
    sobra uma so: o ALVO de capacidade, limitado pela casca do maior pote.
    O piso elevado (elev) faz o resto fechar redondo.
    """
    out = []
    ux, uy, uz = CX - FOLGA, CY - FOLGA, CZ - FOLGA
    for eixo_h, (Ah, A1, A2) in (('Z', (uz, ux, uy)),
                                 ('X', (ux, uy, uz)),
                                 ('Y', (uy, ux, uz))):
        for S in range(2, 13):
            modulo = (Ah - cm.BASE_T) / S
            if not LIM_MOD[0] <= modulo <= LIM_MOD[1]:
                continue
            # de pe, o maior pote da linha (4 modulos) tem de caber na coluna
            if eixo_h == 'Z' and S < 4:
                continue
            for n1 in DIV_X:
                for n2 in DIV_Y:
                    for girado in (False, True):
                        pk1, pk2 = A1 / n1, A2 / n2
                        pl, pw = (pk1, pk2) if not girado else (pk2, pk1)
                        colar_l, colar_w = pl - 2 * OVER_L, pw - 2 * OVER_W
                        if not LIM_L[0] <= colar_l <= LIM_L[1]:
                            continue
                        if not LIM_W[0] <= colar_w <= LIM_W[1]:
                            continue
                        asp = colar_l / colar_w
                        if not LIM_ASP[0] <= asp <= LIM_ASP[1]:
                            continue
                        casca = [capacidade(colar_l, asp, modulo, n)
                                 for n in (1, 2, 3, 4)]
                        if any(v is None or v <= 0 for v in casca):
                            continue
                        # o maior modulo REDONDO que a casca aguenta nos quatro
                        alvo = 0
                        for a in ALVOS:
                            if all(casca[n - 1] >= a * n - 1e-9 for n in (1, 2, 3, 4)):
                                alvo = a
                        if not alvo:
                            continue
                        elev = [resolve_elev(colar_l, asp, modulo, n, alvo * n)
                                for n in (1, 2, 3, 4)]
                        out.append(dict(eixo=eixo_h, S=S, modulo=modulo,
                                        n1=n1, n2=n2, girado=girado,
                                        pl=pl, pw=pw, colar_l=colar_l,
                                        colar_w=colar_w, asp=asp, casca=casca,
                                        alvo=alvo, elev=elev,
                                        colunas=n1 * n2, mods=n1 * n2 * S,
                                        litros=n1 * n2 * S * alvo / 1000.0))
    return out


def ocupacao(c):
    """Quanto do volume da caixa e capacidade util de pote.

    E a conta que o cliente faz. Parede reta NAO ANINHA - este projeto trocou
    aninhamento por empilhamento modular de proposito -, entao a unica alavanca
    de cubagem e fazer as medidas da caixa serem multiplos inteiros da peca.
    Nao ha um terceiro caminho.
    """
    return c['litros'] * 1e6 / (CX * CY * CZ)


def palete(px=1000.0, py=1200.0, pz=1800.0):
    """Caixas por palete PBR, em grade simples nas duas orientacoes."""
    melhor = (0, '')
    for a, b, rot in ((CX, CY, ''), (CY, CX, ' girada')):
        n = int(px // a) * int(py // b)
        if n > melhor[0]:
            melhor = (n, '%d x %d%s' % (int(px // a), int(py // b), rot))
    camadas = int(pz // CZ)
    return melhor[0], melhor[1], camadas, melhor[0] * camadas


def conflito_bocal(c):
    """A tampa de BOCAL fura a pilha - quanto, e quanto isso custa.

    O colar sobe 14 mm do deck e o deck esta em -2,00, entao a tampa de bocal
    montada passa 16,10 mm acima do aro do pote. A algebra modular nao cobre
    isso: ela garante que QUALQUER combinacao de potes fecha a altura, mas a
    tampa de bocal nao e um pote. Nao e defeito novo - "esta versao nao
    empilha" esta escrito desde a revisao 12 -, e so que agora tem preco em
    caixa master.
    """
    sobra = 16.10
    util = CZ - FOLGA - cm.BASE_T
    mods_cheios = int((util - sobra) // c['modulo'])
    return dict(sobra=sobra, mods=mods_cheios,
                perde=util - sobra - mods_cheios * c['modulo'] + sobra,
                custa=c['S'] - mods_cheios)


def tabela(linhas, titulo, n=8):
    print('\n' + titulo)
    print('  arranjo       passo   borda x larg    asp   modulo   a linha (ml)        '
          'piso sobe      L/cx')
    print('  ' + '-' * 103)
    for c in linhas[:n]:
        arr = '%dx%d x%d%s' % (c['n1'], c['n2'], c['S'], 'g' if c['girado'] else '')
        a = c['alvo']
        print('  %-13s %5.1f  %6.1f x %5.1f  %5.3f  %4d ml  %4d/%4d/%4d/%4d  '
              '%4.1f..%4.1f mm  %5.1f'
              % (arr, c['modulo'], c['colar_l'], c['colar_w'], c['asp'], a,
                 a, 2 * a, 3 * a, 4 * a,
                 min(c['elev']), max(c['elev']), c['litros']))


def hoje():
    """O que a linha de hoje faz nesta caixa."""
    p = cm.linha(cm.footprint())
    pl, pw = p[0]['colar_l'] + 2 * OVER_L, p[0]['colar_w'] + 2 * OVER_W
    nx, ny = int((CX - FOLGA) // pl), int((CY - FOLGA) // pw)
    nx2, ny2 = int((CX - FOLGA) // pw), int((CY - FOLGA) // pl)
    if nx2 * ny2 > nx * ny:
        nx, ny, pl, pw = nx2, ny2, pw, pl
    S = int((CZ - FOLGA - cm.BASE_T) // cm.M)
    return dict(pl=pl, pw=pw, nx=nx, ny=ny, S=S,
                sobra_x=CX - FOLGA - nx * pl, sobra_y=CY - FOLGA - ny * pw,
                sobra_z=CZ - FOLGA - (S * cm.M + cm.BASE_T),
                litros=nx * ny * S * 600 / 1000.0)


def main():
    print('=' * 97)
    print('CUBAGEM NA CAIXA MASTER DA NATURA/AVON - %.0f x %.0f x %.0f mm'
          % (CX, CY, CZ))
    print('=' * 97)
    print('Hipotese: as medidas sao INTERNAS da caixa. Se forem externas, desconte')
    print('a parede do ondulado (3 mm/lado em onda simples, 6 em dupla) e rode de novo -')
    print('e so mudar CX, CY, CZ no topo deste arquivo.')
    print('Folga de manuseio reservada: %.1f mm por eixo (produto sem folga nao SAI).'
          % FOLGA)
    print('Modulo de cubagem = pote + TAMPA DE PP: %.2f x %.2f mm na malha.'
          % (cm.footprint() + 2 * OVER_L, cm.footprint() / cm.ASP + 2 * OVER_W))

    h = hoje()
    print('\nA LINHA DE HOJE NESTA CAIXA (revisao 14, 148,06 x 89,47, passo 60)')
    print('  %d x %d por camada x %d empilhados = %d potes de 600 ml = %.1f L'
          % (h['nx'], h['ny'], h['S'], h['nx'] * h['ny'] * h['S'], h['litros']))
    print('  SOBRA: %.1f mm no comprimento, %.1f na largura, %.1f na altura'
          % (h['sobra_x'], h['sobra_y'], h['sobra_z']))
    vazio = 1 - (h['nx'] * h['pl'] * h['ny'] * h['pw']
                 * (h['S'] * cm.M + cm.BASE_T)) / (CX * CY * CZ)
    print('  %.0f%% do volume da caixa e ar fora do produto - e a altura e o pior:'
          % (100 * vazio))
    print('  %.1f mm perdidos, porque 284 nao e multiplo de 60.' % h['sobra_z'])

    C = candidatos()
    print('\n%d arranjos em grade fecham a caixa EXATA nos tres eixos E dao um pote'
          % len(C))
    print('de mantimento de verdade (borda 100-200, aspecto 1,35-2,15, passo 40-95).')

    Z = [c for c in C if c['eixo'] == 'Z']
    tabela(sorted(Z, key=lambda c: (-c['alvo'], abs(c['asp'] - cm.ASP))),
           'A. POTE DE PE, ordenado pelo MODULO que a casca aguenta')
    tabela(sorted([c for c in Z if c['alvo'] >= 600],
                  key=lambda c: abs(c['asp'] - cm.ASP)),
           'B. POTE DE PE com modulo >= 600 ml, ordenado por aspecto mais perto de 1,75')
    tabela(sorted(Z, key=lambda c: -c['litros']),
           'C. POTE DE PE, ordenado por LITROS POR CAIXA')
    tabela(sorted([c for c in C if c['eixo'] != 'Z'],
                  key=lambda c: (-c['alvo'], -c['litros'])),
           'D. POTE DEITADO (a pilha entra de lado) - mais litros, montagem pior')

    print('\n' + '=' * 97)
    print('OS DOIS QUE EU RECOMENDO, EM DETALHE')
    print('=' * 97)
    hoje_oc = h['litros'] * 1e6 / (CX * CY * CZ)
    nc, pat, cam, tot = palete()
    print('Caixas por palete PBR 1,00 x 1,20 m, altura util 1,80 m: %d por camada'
          % nc, '(%s), %d camadas = %d caixas.' % (pat, cam, tot))
    print('Isso vale para qualquer opcao - a caixa nao muda, so o que vai dentro.')
    print('\nHoje a caixa leva %.1f L de capacidade = %.0f%% do volume dela.'
          % (h['litros'], 100 * hoje_oc))
    for alvo in (700, 500):
        c = [x for x in Z if x['alvo'] == alvo and x['n1'] == 3 and x['n2'] == 2]
        if not c:
            continue
        c = c[0]
        cb_ = conflito_bocal(c)
        print('\n--- passo %.1f mm -> linha %d / %d / %d / %d ml ---'
              % (c['modulo'], alvo, 2 * alvo, 3 * alvo, 4 * alvo))
        print('  borda do pote ........ %.2f x %.2f mm (hoje 147,46 x 84,27)'
              % (c['colar_l'], c['colar_w']))
        print('  modulo de cubagem .... %.2f x %.2f mm (pote + tampa de PP)'
              % (c['pl'], c['pw']))
        print('  aspecto .............. %.3f (hoje %.2f)' % (c['asp'], cm.ASP))
        print('  alturas dos quatro ... %.1f / %.1f / %.1f / %.1f mm'
              % tuple(n * c['modulo'] + cm.BASE_T for n in (1, 2, 3, 4)))
        print('  piso elevado ......... %.1f a %.1f mm (quanto o fundo sobe para'
              ' fechar redondo)' % (min(c['elev']), max(c['elev'])))
        print('  na caixa ............. %d colunas x %d modulos = %d modulos'
              % (c['colunas'], c['S'], c['mods']))
        print('  capacidade por caixa . %.1f L = %.0f%% do volume da caixa '
              '(hoje %.1f L, %.0f%%)'
              % (c['litros'], 100 * ocupacao(c), h['litros'], 100 * hoje_oc))
        # so pares em que OS DOIS lados existem na linha (1 a 4 modulos)
        pares = ['%d+%d mod (%.1f + %.1f L)' % (a, c['S'] - a, a * alvo / 1000,
                                                (c['S'] - a) * alvo / 1000)
                 for a in range(min(4, c['S'] - 1), (c['S'] - 1) // 2, -1)
                 if 1 <= c['S'] - a <= 4]
        print('  kits de 2 potes ...... ' + (' | '.join(pares) or 'nenhum: a coluna '
              'pede 3 potes ou mais'))
        a_corpo = cm.area(c['colar_l'], c['colar_w'], cm.R_EXT) / 100
        print('  area projetada ....... %.0f cm2 (hoje 123) -> fechamento %.0f a %.0f t'
              % (a_corpo, a_corpo * cm.PRES[1] * 2 * 1.10,
                 a_corpo * cm.PRES[4] * 2 * 1.10))
        H4 = 4 * c['modulo'] + cm.BASE_T
        print('  curso do maior ....... %.0f mm, altura de molde ~%.0f mm '
              '(hoje 532 e 432)' % (2.2 * H4, H4 + 190))
        print('  vao curto da boca .... %.1f mm (hoje 84,3) -> painel %.2fx mais '
              'flexivel' % (c['colar_w'], (c['colar_w'] / 84.27) ** 3))
        print('  TAMPA DE BOCAL ....... passa %.2f mm do aro: a coluna leva %d'
              ' modulos em vez de %d' % (cb_['sobra'], cb_['mods'], c['S']))


if __name__ == '__main__':
    main()
