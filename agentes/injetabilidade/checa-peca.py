#!/usr/bin/env python3
"""
Checa se uma peca cabe no parque de injetoras da casa. O que pode e o que nao pode.

  python3 checa-peca.py --l 145.7 --w 85.8 --h 242 --parede 1.40 --peso 142.5 --cav 2
  python3 checa-peca.py --l 300 --w 200 --h 120 --parede 2.2 --peso 410 --cav 1 --resina PSAI

Sete portoes, na ordem em que reprovam:
  1 resina    a casa compra essa resina?
  2 fechamento   area projetada x pressao -> quais maquinas tem tonelagem
  3 platos    altura de molde + abertura -> quais tem espaco (ESTIMADO, ver parque.json)
  4 injecao   volume do tiro contra a capacidade da rosca (ESTIMADO)
  5 colunas   o molde passa entre as colunas? (ESTIMADO)
  6 fluxo     L/t contra a fluidez da resina
  7 ciclo     estimativa grosseira e o que ela vale

Veredito por portao: OK (verde), ATENCAO (amarelo), NAO (vermelho).
Todo portao que depende do envelope estimado nunca passa de ATENCAO — a ficha
real das injetoras (AD_INJETORAFICHA) esta vazia.
"""
import argparse, json, math, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(BASE, 'parque.json')))

# Pressao media na cavidade. Nao ha um numero: depende do recalque, e o recalque
# depende de o que a peca e. Por isso o portao 2 trabalha com FAIXA, nao com valor.
#   rasa  = tampa, bandeja, peca de fundo largo e pouca altura, injecao central
#   funda = pote, balde, corpo - o recalque tem que empurrar plastico para longe
FAIXA_P = {'rasa': (200.0, 350.0), 'funda': (300.0, 500.0)}

K_SEG = 1.15
USO_MAX = 0.80          # nao passar de 80% do fechamento nominal
DENS = {'PP': 0.905, 'PS': 1.05, 'PSAI': 1.04}
ALFA = {'PP': 0.09, 'PS': 0.08, 'PSAI': 0.08}     # difusividade mm2/s
LT_LIMITE = {'PP H 103': 150, 'PP H 105': 160, 'PP CP 141': 150,
             'PP RP 141': 200, 'PP RP 340 S': 250, 'PSAI': 150, 'PS': 180}

# Ancoras: pecas que a casa JA produz, com peso do cadastro e a maquina da ficha.
# Servem para o engenheiro conferir se a estimativa esta no mundo real.
ANCORAS = [
    ('TAMPA DA LIXEIRA DE 16 LTS', 115, 'INJ 2', 200, 24.9),
    ('TAMPA LIXEIRA JUTA RETANGULAR 12 L', 72, 'INJ 7', 160, 30.5),
    ('CORPO NITRONBOX MEDIO 6 LTS', 232, 'INJ 2', 200, 28.5),
    ('CORPO DA FRASQUEIRA MEDIA', 116, 'INJ 1', 200, 21.0),
    ('CORPO DO CESTO RATTAN PP C/ TAMPA', 103, 'INJ 1', 200, 21.2),
    ('CORPO DO POTE ACOPLADO REDONDO 2 L', 81, 'INJ 19', 200, 26.2),
    ('CORPO DO RALADOR 4 FACES', 89, 'INJ 8', 160, 30.3),
    ('CORPO DO POTE HERMETICO COM TRAVA PEQ.', 33, 'INJ 13', 120, 16.7),
]


# regras de molde, iguais as de potes-modulares/moldes/gera-molde.py
def molde(H, L, W, ncav):
    """Altura de molde, curso de abertura e footprint, a partir da peca."""
    alt = 294.0 + 2.0 * H
    abertura = 2.0 * H + 85.0
    fl = L + 2 * (32 + 45)
    fw = W + 2 * (32 + 45)
    if ncav > 1:                       # cavidades lado a lado no menor eixo
        fw = ncav * (W + 64) + (ncav - 1) * 60 + 90
    return alt, abertura, fl, fw


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--l', type=float, required=True, help='maior dimensao no plano de fechamento (mm)')
    a.add_argument('--w', type=float, required=True, help='menor dimensao no plano de fechamento (mm)')
    a.add_argument('--h', type=float, required=True, help='altura da peca (mm)')
    a.add_argument('--parede', type=float, required=True, help='espessura de parede (mm)')
    a.add_argument('--peso', type=float, help='peso da peca (g)')
    a.add_argument('--volume', type=float, help='volume da peca (cm3), se nao tiver o peso')
    a.add_argument('--cav', type=int, default=1)
    a.add_argument('--resina', default='PP H 105')
    a.add_argument('--saida', type=float, default=None, help='saida por lado (graus)')
    a.add_argument('--json', action='store_true')
    o = a.parse_args()

    fam = 'PSAI' if 'PSAI' in o.resina.upper() else ('PS' if o.resina.upper().startswith('PS') else 'PP')
    dens = DENS[fam]
    peso = o.peso if o.peso else (o.volume or 0) * dens
    vol_cm3 = peso / dens
    L, W, H, t = o.l, o.w, o.h, o.parede
    forma = 'rasa' if H < 0.35 * math.sqrt(L * W) else 'funda'
    laudo, notas = [], []

    # 1 - resina ------------------------------------------------------------
    achou = [r for r in D['resinas'] if o.resina.upper()[:8] in r['nome'].upper()]
    if achou:
        r = achou[0]
        kg = r.get('kg_12m', r.get('kg_24m', 0))
        g1, det1 = 'OK', f"{r['nome']} - R$ {r['preco']:.2f}/kg, {kg:,} kg comprados".replace(',', '.')
    else:
        g1 = 'NAO'
        det1 = (f"'{o.resina}' NAO aparece nas compras dos ultimos 12 meses. Resina nova = "
                f"fornecedor novo, pedido minimo, silo e purga - decisao de suprimentos, nao de projeto. "
                + D['_sem_compra'])
    laudo.append(('1 resina', g1, det1))

    # 2 - fechamento (faixa, nao valor) -------------------------------------
    area = L * W / 100.0 * o.cav * 1.05         # cm2, envolvente + canais
    p0, p1 = FAIXA_P[forma]
    tf0 = area * p0 * K_SEG / 1000.0
    tf1 = area * p1 * K_SEG / 1000.0
    seguro = [m for m in D['maquinas'] if tf1 <= USO_MAX * m['t']]
    talvez = [m for m in D['maquinas'] if tf0 <= USO_MAX * m['t']]
    g2 = 'OK' if len(seguro) >= 3 else ('ATENCAO' if talvez else 'NAO')
    laudo.append(('2 fechamento', g2,
                  f"peca {forma} - area projetada {area:.0f} cm² x {p0:.0f} a {p1:.0f} kgf/cm² = "
                  f"**{tf0:.0f} a {tf1:.0f} tf**; {len(seguro)} maquinas cobrem o topo da faixa, "
                  f"{len(talvez)} cobrem o piso"))
    cand = talvez

    # 3 a 5: envelope ESTIMADO, maquina por maquina -------------------------
    alt_molde, abertura, fl, fw = molde(H, L, W, o.cav)
    preciso = alt_molde + abertura
    tiro = vol_cm3 * o.cav * 1.05

    def env(m): return D['envelope_estimado'][str(m['t'])]
    ok3 = [m for m in cand if env(m)['abertura'] + env(m)['molde_max'] >= preciso
           and env(m)['molde_min'] <= alt_molde <= env(m)['molde_max']]
    ok4 = [m for m in cand if 0.20 * env(m)['injecao_cm3'] <= tiro <= 0.80 * env(m)['injecao_cm3']]
    ok5 = [m for m in cand if max(fl, fw) <= env(m)['colunas']]

    laudo.append(('3 platos', 'ATENCAO' if ok3 else 'NAO',
                  f"molde ~{alt_molde:.0f} mm + abertura ~{abertura:.0f} mm = **{preciso:.0f} mm entre platos** -> "
                  f"{len(ok3)} maquinas ({', '.join(sorted({str(m['t']) + ' t' for m in ok3})) or 'nenhuma'})"))
    laudo.append(('4 injecao', 'ATENCAO' if ok4 else 'NAO',
                  f"peca {peso:.1f} g = {vol_cm3:.0f} cm³; tiro com {o.cav} cav + canais = **{tiro:.0f} cm³** -> "
                  f"{len(ok4)} maquinas com a rosca entre 20 e 80% "
                  f"({', '.join(sorted({str(m['t']) + ' t' for m in ok4})) or 'nenhuma'})"))
    laudo.append(('5 colunas', 'ATENCAO' if ok5 else 'NAO',
                  f"porta-molde estimado {fl:.0f} x {fw:.0f} mm -> {len(ok5)} maquinas com vao suficiente"))

    # 6 - fluxo -------------------------------------------------------------
    lt = (math.hypot(L / 2, W / 2) + H) / t
    lim = next((v for k, v in LT_LIMITE.items() if k.upper() in o.resina.upper()), 160)
    g6 = 'OK' if lt <= lim * 0.85 else ('ATENCAO' if lt <= lim else 'NAO')
    laudo.append(('6 fluxo', g6,
                  f"L/t = **{lt:.0f}** contra o teto de ~{lim} desta resina"
                  + ('' if lt <= lim else '. Acima do teto: parede maior, PP RP 340 S (teto ~250), '
                                          'ou mais um ponto de injecao')))

    # 7 - ciclo -------------------------------------------------------------
    tres = (t ** 2 / (math.pi ** 2 * ALFA[fam])) * math.log((4 / math.pi) * (230 - 20) / (90 - 20))
    ciclo = 2.0 * max(tres, 8.0) + 2 * abertura / 200.0
    laudo.append(('7 ciclo', 'ATENCAO',
                  f"resfriamento teorico {tres:.1f} s; a casa nao regula abaixo de 8 s. Regra tirada das "
                  f"14 fichas: ciclo ~ 2,0 x resfriamento (desvio 0,3). Com o curso, **ciclo ~ {ciclo:.0f} s** "
                  f"(+-30%; o numero bom vem da ficha de uma peca parecida)"))

    # interseccao -----------------------------------------------------------
    codigos = {m['cod'] for m in ok3} & {m['cod'] for m in ok4} & {m['cod'] for m in ok5}
    passam = sorted((m for m in cand if m['cod'] in codigos), key=lambda m: (m['t'], m['cod']))

    if o.saida is not None and o.saida < 0.5:
        notas.append(f'Saida de {o.saida}°/lado abaixo de 0,5°: exige polido A2 no sentido da extracao, '
                     'e mesmo assim a peca nao aninha para o frete.')
    if t < 1.0:
        notas.append('Parede abaixo de 1,0 mm e embalagem de parede fina dedicada: pede maquina de alta '
                     'velocidade com acumulador, que nao aparece no cadastro da casa.')
    if not ok3 and cand:
        notas.append('Tem tonelagem e nao tem espaco entre platos: e o caso da peca alta. Saidas - extracao '
                     'em dois estagios, calcos menores, molde mais baixo, ou a 600 t (INJ 34).')
    if ok3 and not ok4:
        notas.append('A maquina que tem espaco tem rosca grande demais para o tiro: o material fica tempo '
                     'demais no canhao e degrada. Ou aumenta a cavitacao, ou muda o conceito do molde.')

    # ---- saida -------------------------------------------------------------
    if o.json:
        print(json.dumps(dict(peso=peso, forma=forma, tf=[tf0, tf1], lt=lt, entre_platos=preciso,
                              ciclo=ciclo, maquinas=[m['nome'] for m in passam],
                              laudo=laudo, notas=notas), ensure_ascii=False, indent=2))
        return
    pior = 'NAO' if any(g == 'NAO' for _, g, _ in laudo) else (
        'ATENCAO' if any(g == 'ATENCAO' for _, g, _ in laudo) else 'OK')
    print(f'\nPECA {L:.1f} x {W:.1f} x {H:.1f} mm | parede {t:.2f} | {peso:.1f} g | '
          f'{o.cav} cav | {o.resina} | forma {forma}')
    print('=' * 104)
    for nome, g, det in laudo:
        print(f'[{g:^8}] {nome:<14} {det}')
    print('-' * 104)
    if passam:
        print(f'MAQUINAS QUE ATENDEM OS SETE PORTOES ({len(passam)}): '
              + ', '.join(f"{m['nome'].replace('INJETORA ', 'INJ ')} ({m['t']} t)" for m in passam[:12])
              + (' ...' if len(passam) > 12 else ''))
    else:
        print('NENHUMA MAQUINA ATENDE OS SETE PORTOES COM OS DADOS DE HOJE.')
    for n in notas:
        print('  * ' + n)
    print('-' * 104)
    print('Ancoras da casa (peca / peso de cadastro / maquina da ficha / ciclo):')
    for nome, pg, inj, ton, cic in ANCORAS[:4]:
        print(f'  {nome[:42]:<42} {pg:>4} g  {inj:<7} {ton:>3} t  {cic:>5.1f} s')
    print('=' * 104)
    print(f'VEREDITO: {pior}   (portoes 3, 4 e 5 rodam em ESTIMATIVA de catalogo - '
          f'AD_INJETORAFICHA esta vazia, entao nenhum deles passa de ATENCAO)')
    print()


if __name__ == '__main__':
    main()
