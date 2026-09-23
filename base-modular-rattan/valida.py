#!/usr/bin/env python3
"""
Confere a geometria antes de qualquer numero sair para a ficha.

1. AMOSTRAGEM x CONTA EXATA: nas partes retas (caixas e tubos) de cada peca,
   volume_area() tem de bater com uniao_caixas() dentro de 0,1%.
2. MALHA x TESTE DE DENTRO: para cada elemento curvo (rr, prisma, casca do
   tampo), o volume da malha (o que aparece no 3D e no STL) tem de bater com
   o volume amostrado pelo teste de "dentro" (o que vai para o peso) dentro
   de 1%. Se um dos dois estiver errado, eles discordam.
3. MALHA FECHADA: toda aresta de cada elemento aparece uma vez em cada
   sentido (volume assinado nao pega normal invertida sozinho).

Uso:  python3 valida.py      (sai com erro se algo falhar)
"""
import sys
from collections import Counter
import geometria as g
import solidos as s

falhas = 0
for nome, f in g.PECAS.items():
    el = f()
    retas = [e for e in el if e[0] in ("caixa", "tubo")]
    v_ex = s.uniao_caixas(retas)
    v_am, _ = s.volume_area(retas, h=0.35)
    d = (v_am / v_ex - 1) * 100
    ok = abs(d) < 0.1
    falhas += not ok
    print(f"{nome:13s} partes retas: amostrado {v_am/1000:8.2f} cm3  exato {v_ex/1000:8.2f} cm3  {d:+.3f}%  {'ok' if ok else 'FALHOU'}")
    vistos = set()
    for e in el:
        if e[0] in ("caixa", "tubo"):
            continue
        chave = (e[0], round(s.caixa_limite(e)[1] - s.caixa_limite(e)[0], 3), round(s.caixa_limite(e)[5] - s.caixa_limite(e)[4], 3))
        if chave in vistos:          # espelhos: mesmo volume
            continue
        vistos.add(chave)
        tris = s.malha(e)
        v_m = s._vol_assinado(tris)
        v_d, _ = s.volume_area([e], h=0.15 if e[0] == "prisma" else 0.25, so_x_positivo=False)
        dd = (v_d / v_m - 1) * 100
        arestas = Counter()
        for a, b, c in tris:
            for p, q in ((a, b), (b, c), (c, a)):
                arestas[(tuple(round(x, 5) for x in p), tuple(round(x, 5) for x in q))] += 1
        fechada = all(arestas[(q, p)] == n for (p, q), n in arestas.items())
        ok = abs(dd) < 1.0 and fechada
        falhas += not ok
        print(f"   {e[0]:11s} {e[-1]:9s} malha {v_m/1000:8.3f} cm3  dentro {v_d/1000:8.3f} cm3  {dd:+.2f}%  "
              f"{'fechada' if fechada else 'ABERTA'}  {'ok' if ok else 'FALHOU'}")
print("\nTUDO CONFERE" if not falhas else f"\n{falhas} FALHA(S)")
sys.exit(1 if falhas else 0)
