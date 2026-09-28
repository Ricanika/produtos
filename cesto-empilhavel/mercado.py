#!/usr/bin/env python3
"""Pesquisa de mercado da linha ELO: estamos dentro ou fora do preco?

O QUE E DADO, O QUE E PREMISSA E O QUE E ESTIMATIVA -- a conta inteira
depende de nao confundir os tres:

- DADO. Peso, capacidade, dimensao e preco de vitrine dos comparaveis, na
  data de coleta abaixo. Quase todo vendedor deste setor publica o PESO, e
  e isso que permite comparar por grama e nao por foto.
- DADO. O preco de fabrica do NOSSO 047 (R$ 4,58, TGFCUS x TGFITE) e o
  preco dele na gondola (R$ 19,99 a 29,15). A razao entre os dois e o
  unico multiplo de canal MEDIDO nesta analise -- e e medido no nosso
  proprio produto.
- PREMISSA. O multiplo do canal B2B (loja de embalagem que vende direto ao
  usuario final). Adotei 1,6 a 2,2. E a premissa mais fraca da analise, e
  o veredito contra o cesto expositor depende dela: por isso o relatorio
  imprime, para cada comparacao, o multiplo de EMPATE. Acima dele estamos
  caros, abaixo estamos baratos, e quem resolve isso nao e busca na web --
  e uma cotacao de distribuidor.
- ESTIMATIVA. A capacidade do cesto bin de referencia, que o vendedor nao
  publica. Sai do envelope dele com o fator de enchimento do nosso P.

Os precos foram coletados por BUSCA, sem abrir as paginas: a politica de
rede do ambiente bloqueia esses dominios. Cada linha carrega a fonte.

Uso:  python3 mercado.py            (relatorio)
      python3 mercado.py --folha    (relatorio + mercado.png)
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cad"))

COLETA = "28/09/2026"

K_B2B = (1.6, 2.2)          # premissa: loja de embalagem -> fabrica
K_DOM = (4.36, 6.36)        # MEDIDO no 047: 19,99/4,58 e 29,15/4,58

# ref, produto, tier, (alt, larg, comp) cm, litros, kg, preco, fonte, nota
MERCADO = [
    ("bin-10", "Cesto Mini / caixa bin (kit de 10)", "expositor",
     (13.0, 21.5, 25.0), None, 0.170, 6.20, "caixasplasticaseta.com.br",
     "kit de 10 a R$ 62,00 · carga 5 kg, empilha 8 · O GEMEO DO NOSSO P"),
    ("bin-amz", "Cesto Caixa Bin 13x21,5 (kit de 10)", "expositor",
     (13.0, 21.5, 25.0), None, 0.170, 6.04, "amazon.com.br",
     "kit de 10 a R$ 60,44"),
    ("exp-30", "Cesto expositor pequeno 30 L", "expositor",
     (20.0, 34.0, 44.0), 30.0, 0.600, 12.00, "caixasplasticaseta.com.br",
     "carga 10 kg, empilha 60 kg"),
    ("exp-35", "Cesto expositor pequeno 35 L", "expositor",
     (24.0, 37.0, 43.5), 35.0, 0.850, 10.57, "caixasplasticaseta.com.br",
     "kit de 10 a R$ 115,80 (R$ 11,58/un)"),
    ("exp-55", "Cesto expositor medio 55 L", "expositor",
     (29.0, 41.0, 58.0), 55.0, 0.950, 19.10, "caixasplasticaseta.com.br",
     "carga 11,1 kg, empilha 8 (88,8 kg) · atacado R$ 16,00/un; "
     "kit 12 R$ 222,10 (18,51); 20 un no ML R$ 456,30 (22,82)"),
    ("agr-20", "Caixa agricola hortifruti ETA 20HF", "agricola",
     (17.0, 30.0, 48.5), 20.0, 0.885, 24.89, "caixasplasticaseta.com.br",
     "encaixavel, carga 15 kg"),
    ("agr-50e", "Caixa agricola ETA31 ECX 50,5 L", "agricola",
     (31.5, 36.0, 56.0), 50.5, 1.700, 40.65, "caixasplasticaseta.com.br",
     "empilhavel E encaixavel, carga 30 kg · O GEMEO FUNCIONAL DO G"),
    ("agr-50t", "Caixa agricola ETA31TAS 50 L", "agricola",
     (31.0, 36.5, 55.0), 50.0, 1.600, 34.89, "caixasplasticaseta.com.br",
     "vazada, empilhavel"),
    ("agr-ab50", "Caixa agricola ABelt AB-50L", "agricola",
     (31.0, 36.5, 55.0), 50.0, None, 46.90, "abelt-loja.com.br",
     "PEAD virgem, carga 35 kg · peso nao publicado"),
]

# O nosso 047 nos DOIS niveis -- a ponte entre fabrica e gondola
N047 = {"ref": "047/P", "desc": "Cesto Organizador Vime 7 L (NOSSO)",
        "litros": 7.0, "kg": 0.213, "fabrica": 4.58, "varejo": (19.99, 29.15),
        "fonte": "ERP + biglarutilidades / nichele / nitron.com.br"}

# Referencia do canal DOMESTICO no tamanho do M (gondola de marketplace)
DOM25 = {"ref": "arq-25", "litros": 25.0,
         "desc": "Caixa organizadora 25 L c/ tampa (Arqplast, reciclado)",
         "varejo": (42.05, 75.90), "fonte": "magazineluiza.com.br"}

CUSTO_KG = {"moido": 11.50, "virgem": 15.00}   # R$/kg de peca (economia.py)
PRECO_KG_047 = N047["fabrica"] / N047["kg"]    # R$ 21,50/kg -- ancora da casa

# Comparacoes que interessam: cada tamanho contra os gemeos dele
DUELOS = {"ELO P": ["bin-10", "bin-amz"],
          "ELO M": ["exp-30", "exp-35", "agr-20"],
          "ELO G": ["exp-55", "agr-50t", "agr-50e"]}


CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "mercado-medidas.json")


def nossa_linha(rapido=False):
    """Peso, capacidade e envelope das tres configuracoes, do proprio solido.

    Com --rapido le o cache: construir os tres solidos leva minutos, e mexer
    no texto da folha ou no preco de um concorrente nao muda a geometria.
    """
    if rapido and os.path.exists(CACHE):
        return json.load(open(CACHE, encoding="utf-8"))
    import modelo3d as M
    saida = []
    for nome, fn in (("ELO P", M.padrao), ("ELO M", M.padrao_m),
                     ("ELO G", M.padrao_g)):
        fn()
        p, furos = M.cesto(aba=True)
        bb = p.bounding_box()
        saida.append({
            "nome": nome,
            # RHO esta em g/mm3: volume*RHO ja e GRAMA, e /1000 da kg.
            "kg": p.volume * M.RHO / 1000,
            "litros": M.capacidade(),
            "env": (bb.size.Z / 10, bb.size.X / 10, bb.size.Y / 10),  # cm
            "furos": furos,
        })
    json.dump(saida, open(CACHE, "w", encoding="utf-8"), indent=1)
    return saida


def litros_bin(linha):
    """Capacidade do cesto bin, que o vendedor nao publica.

    Envelope dele (13 x 21,5 x 25) vezes o fator de enchimento do nosso P,
    que e a razao entre a capacidade medida e o envelope medido. O bin tem
    parede mais reta e menos chanfro, entao esse fator e um PISO: da o
    numero mais favoravel a ele que eu consigo justificar.
    """
    p = linha[0]
    fator = p["litros"] / (p["env"][0] * p["env"][1] * p["env"][2] / 1000)
    env = 13.0 * 21.5 * 25.0 / 1000
    return env * fator, env * 0.75, fator


def fab(preco, k):
    """Preco de fabrica equivalente: [preco/kmax, preco/kmin]."""
    return preco / k[1], preco / k[0]


def relatorio(linha):
    est, est_alto, fator = litros_bin(linha)
    print(f"PESQUISA DE MERCADO DA LINHA ELO -- coleta de {COLETA}")
    print("=" * 78)

    print("\n1. A NOSSA LINHA, medida no solido")
    print(f"   {'':7} {'litros':>7} {'peso':>8} {'g/L':>6} "
          f"{'custo moido':>12} {'custo virgem':>13} {'por kg da casa':>15}")
    for it in linha:
        print(f"   {it['nome']:7} {it['litros']:7.2f} {it['kg']*1000:7.1f}g "
              f"{it['kg']*1000/it['litros']:6.1f} "
              f"{it['kg']*CUSTO_KG['moido']:12.2f} "
              f"{it['kg']*CUSTO_KG['virgem']:13.2f} "
              f"{it['kg']*PRECO_KG_047:15.2f}")

    print("\n2. O MERCADO")
    print(f"   {'ref':9} {'litros':>7} {'peso':>8} {'g/L':>6} {'vitrine':>8} "
          f"{'R$/L':>6} {'R$/kg':>6}  fabrica equiv.   R$/kg na fabrica")
    for ref, _, _, _, lt, kg, pr, _, _ in MERCADO:
        lt_ = lt if lt else est
        marca = " " if lt else "~"
        gl = f"{kg*1000/lt_:6.1f}" if kg else "     -"
        rk = f"{pr/kg:6.2f}" if kg else "     -"
        lo, hi = fab(pr, K_B2B)
        fkg = f"{lo/kg:5.2f} a {hi/kg:5.2f}" if kg else "        -"
        print(f"   {ref:9} {lt_:6.1f}{marca} {kg*1000 if kg else 0:7.1f}g "
              f"{gl} {pr:8.2f} {pr/lt_:6.2f} {rk}  "
              f"R$ {lo:5.2f} a {hi:5.2f}   {fkg}")
    print(f"   (~) capacidade do bin nao publicada: {est:.2f} L pelo "
          f"envelope x fator de enchimento do P ({fator:.3f});")
    print(f"       a {0.75:.2f} de enchimento daria {est_alto:.2f} L, "
          "e o g/L dele melhoraria na mesma proporcao.")

    print(f"\n3. A PONTE DE CANAL -- {N047['desc']}")
    lo, hi = N047["varejo"]
    f0 = N047["fabrica"]
    print(f"   fabrica R$ {f0:.2f} (ERP)  ->  gondola R$ {lo:.2f} a {hi:.2f}"
          f"   =>  multiplo {lo/f0:.2f}x a {hi/f0:.2f}x")
    print(f"   {N047['kg']*1000:.0f} g / {N047['litros']:.0f} L = "
          f"{N047['kg']*1000/N047['litros']:.1f} g/L · na fabrica "
          f"R$ {f0/N047['litros']:.2f}/L e R$ {f0/N047['kg']:.2f}/kg")
    dlo, dhi = DOM25["varejo"]
    a, b = fab(dlo, K_DOM)[0], fab(dhi, K_DOM)[1]
    print(f"   referencia domestica de 25 L: {DOM25['desc']}")
    print(f"      gondola R$ {dlo:.2f} a {dhi:.2f}  ->  fabrica equivalente "
          f"R$ {a:.2f} a {b:.2f} (pelo multiplo do 047)")

    print("\n4. A LEI DO R$/kg: quanto MAIOR a peca, MENOS o mercado paga")
    print("   por quilo de plastico -- e e por isso que peca leve e grande")
    print("   e o lugar mais dificil de ganhar dinheiro por kg:")
    ladder = sorted([(kg, ref, fab(pr, K_B2B)) for ref, _, _, _, _, kg, pr, _, _
                     in MERCADO if kg], key=lambda x: x[0])
    for kg, ref, (lo_, hi_) in ladder:
        print(f"      {ref:9} {kg*1000:6.0f} g  ->  R$ {lo_/kg:5.2f} a "
              f"{hi_/kg:5.2f} /kg na fabrica")
    print(f"      {'047 (nosso)':9} {N047['kg']*1000:6.0f} g  ->  "
          f"R$ {PRECO_KG_047:5.2f} /kg  (MEDIDO, nao estimado)")
    print(f"   Nosso custo de peca: R$ {CUSTO_KG['moido']:.2f}/kg em moido e "
          f"R$ {CUSTO_KG['virgem']:.2f}/kg em virgem.")

    print("\n5. DENTRO OU FORA -- tudo em PRECO DE FABRICA EQUIVALENTE")
    for it in linha:
        nosso = it["kg"] * PRECO_KG_047
        print(f"\n   {it['nome']}: {it['litros']:.2f} L · "
              f"{it['kg']*1000:.1f} g · {it['kg']*1000/it['litros']:.1f} g/L")
        print(f"      custo R$ {it['kg']*CUSTO_KG['moido']:.2f} (moido) a "
              f"{it['kg']*CUSTO_KG['virgem']:.2f} (virgem) · "
              f"preco pelo R$/kg da casa R$ {nosso:.2f}")
        for g in DUELOS[it["nome"]]:
            row = next(x for x in MERCADO if x[0] == g)
            pr = row[6]
            lo_, hi_ = fab(pr, K_B2B)
            pos = ("DENTRO" if nosso <= hi_ else "ACIMA")
            if nosso <= lo_:
                pos = "ABAIXO"
            dif = nosso / hi_ - 1
            print(f"      {row[1][:42]:43} vitrine {pr:6.2f} -> fabrica "
                  f"{lo_:5.2f}-{hi_:5.2f}  {pos:6} "
                  f"({dif*100:+5.1f}% do teto) · empata se k = {pr/nosso:.2f}")
        if it["nome"] == "ELO P":
            print(f"      {'...e pelo preco ADOTADO no README (R$ 4,58)':43} "
                  f"                                  "
                  f"empata se k = {6.20/4.58:.2f}")


def main():
    linha = nossa_linha("--rapido" in sys.argv)
    relatorio(linha)
    if "--folha" in sys.argv:
        import folha_mercado
        folha_mercado.desenhar(linha, MERCADO, N047, DOM25, K_B2B, K_DOM,
                               CUSTO_KG, PRECO_KG_047, COLETA, litros_bin(linha))


if __name__ == "__main__":
    main()
