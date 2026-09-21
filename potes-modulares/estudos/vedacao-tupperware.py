#!/usr/bin/env python3
"""Vedacao tipo Tupperware aplicada ao pote retangular: orcamento e forcas.

ESTUDO DE REFERENCIA - NAO IMPLEMENTADO na linha. Ver secao 13 do README.
Rode com:  python3 estudos/vedacao-tupperware.py
"""
import importlib.util, math, os
CALC = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'calculo-modular.py')
sp = importlib.util.spec_from_file_location('cm', CALC)
cm = importlib.util.module_from_spec(sp); sp.loader.exec_module(cm)
p = cm.linha(cm.footprint()); p0 = p[0]
T = math.tan(math.radians(cm.SAIDA))
EXT, W = p0['ext_l'], p0['ext_w']
dLW = EXT - W
boca, labio = EXT - 2*cm.W_BORDA, EXT + 2*cm.ABA_W
bandeja = boca - 2*cm.PLUG_FOLGA - 2*cm.PLUG_PAR
poco = bandeja + 2*cm.PE_POCO_PAR
per = lambda L: cm.perim(L, L - dLW, cm.R_EXT + (L - EXT)/2)

def labio_flex(t, L, d, E, Lw, mu=0.30):
    """Labio como viga engastada: forca normal por mm e arranque axial."""
    I1 = t**3 / 12.0
    w  = 3 * E * I1 * d / L**3          # N/mm de perimetro
    N  = w * per(Lw)
    return w, N, mu * N / 9.81          # kgf

print('=' * 78)
print('GEOMETRIA DISPONIVEL NA BORDA ATUAL')
print('=' * 78)
print(f'  boca (furo) .............. {boca:.1f}   parede da borda {cm.W_BORDA:.2f} mm')
print(f'  corpo .................... {EXT:.1f}')
print(f'  labio da aba ............. {labio-2*1.20:.1f} a {labio:.1f}, desce de z=-{cm.ABA_T:.2f} a z=-{cm.ABA_T+cm.LIP_H:.2f}')
print(f'  topo da borda (face plana) {boca:.1f} a {labio:.1f}  ->  {(labio-boca)/2:.2f} mm/lado de mesa livre')
print(f'  canaleta em U do POTE .... {EXT - 2*(cm.ABA_T+cm.LIP_H)*T:.1f} a {labio-2*1.20:.1f}, '
      f'{(labio-2*1.20-(EXT-2*(cm.ABA_T+cm.LIP_H)*T))/2:.2f} mm/lado, ABRE PARA BAIXO')
print('  -> uma tampa que vem de cima NAO alcanca essa canaleta. O topo da borda')
print('     e plano: nao ha cordao em pe para o canal da tampa agarrar dos dois lados.')

print('\n' + '=' * 78)
print('CAMINHO A - sem tocar no pote: 2o labio pendurado no PISO DA BANDEJA')
print('=' * 78)
LAB_T, LAB_Z = 0.60, -6.80
bore_z = boca - 2 * abs(LAB_Z) * T
for d in (0.20, 0.30, 0.40):
    pta = bore_z + 2*d
    comp = math.hypot((pta - poco)/2, abs(LAB_Z) - (2.00 + cm.PE_DECK))
    for nome, E in (('PEAD', 1000.0), ('PEBD', 200.0)):
        w, N, kgf = labio_flex(LAB_T, comp, d, E, pta)
        if nome == 'PEAD':
            print(f'  interferencia {d:.2f} mm/lado -> ponta {pta:.2f} | labio {comp:.2f} mm de '
                  f'comprimento x {LAB_T:.2f}')
        print(f'      {nome}: {w:.3f} N/mm | normal {N:.0f} N | arranque reto {kgf:5.1f} kgf | '
              f'descascando um canto {kgf/6:.1f} kgf')
print(f'  O labio nasce na aresta do piso da bandeja (z=-{2.00+cm.PE_DECK:.2f}), nao ao lado da')
print(f'  parede do poco: por isso NAO precisa da fenda de 0,95 mm que nao cabia na revisao 6.')
print(f'  A reacao fecha no proprio anel do piso da bandeja, que e um aro em compressao.')

print('\n' + '=' * 78)
print('CAMINHO B - Tupperware de verdade: cordao EM PE no topo da borda do pote')
print('=' * 78)
CB_I, CB_O, CB_H = 140.0, 142.0, 2.20
print(f'  cordao do pote: {CB_I:.1f} a {CB_O:.1f} ({(CB_O-CB_I)/2:.2f} mm/lado), {CB_H:.2f} mm em pe')
print(f'  sobra na mesa da borda: {(CB_I-boca)/2:.2f} mm por dentro, {(labio-CB_O)/2:.2f} por fora')
for t, L, d in ((0.70, 2.60, 0.15), (0.55, 3.50, 0.12), (0.55, 3.50, 0.20)):
    pi_, po_ = CB_I + 2*d, CB_O - 2*d
    w1, N1, k1 = labio_flex(t, L, d, 1000.0, pi_)
    w2, N2, k2 = labio_flex(t, L, d, 1000.0, po_)
    print(f'  paredes {t:.2f} x {L:.2f} mm, interferencia {d:.2f}/lado  ->  '
          f'PEAD: arranque reto {k1+k2:5.1f} kgf | canto {(k1+k2)/6:.1f} kgf')
    print(f'      parede interna: face externa livre {pi_:.2f} (folga ao furo '
          f'{(pi_-2*t-boca)/2:.2f} mm) | externa: face interna livre {po_:.2f} '
          f'(sobra {(labio-(po_+2*t))/2:.2f} ate o labio)')
print('  Aqui as duas paredes apertam FACES OPOSTAS do mesmo cordao: as forcas se')
print('  fecham dentro do canal da tampa. Nao dependem do deck ficar plano - que e')
print('  exatamente o problema em aberto da revisao 6.')
print('  PRECO: muda a borda dos QUATRO moldes de corpo.')

print('\n' + '=' * 78)
print('COMPARACAO com o que a linha ja tem')
print('=' * 78)
print('  tampa de teca, aro de TPE radial no furo, 0,20 mm ........ 6,1 kgf reto / 1,0 canto')
print('  tampa PE rev.6, cordao axial + garra ..................... trava geometrica')
print('  A patente US2487400 (1949) e NONSNAP: so atrito. Nosso caso tem garra,')
print('  entao o labio extra e VEDACAO, nao retencao - some o risco de abrir sozinho.')
