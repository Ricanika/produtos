#!/usr/bin/env python3
"""
Memoria de calculo da caixa expositora SORTIDA (os 3 kits na mesma caixa).

CONCEITO
  Caixa tipo WRAP: uma chapa unica da a volta FUNDO -> FRENTE -> TOPO -> TRAS.
  O topo e um painel inteirico preso na traseira - e isso que permite a testeira.

  O picote sobe pela frente a partir de 240 mm, corre pelas duas quinas frontais
  ate o topo e MORRE ali. A peca [frente alta + topo] NAO sai: fica articulada no
  vinco TRAS/TOPO. Para montar o expositor:
     1. o TOPO gira 90 graus e fica em pe, na altura da traseira  -> testeira
     2. a FRENTE ALTA dobra 180 graus sobre ele                   -> parede dupla
     3. o que sobra da frente desce por dentro da caixa           -> travamento

A ALTURA E CONSEQUENCIA DA MECANICA, NAO ESCOLHA:
     H = frente que fica (240) + profundidade (topo) + aba de travamento

ARRANJO
  Uma coluna vertical por kit, tres facings. Cada coluna tem sua propria
  contagem de camadas; um calco nivela os tres topos na mesma altura.

Uso:  python3 calculo-expositora.py
"""
import math

ESP = 5.0                      # espessura da onda C simples (mm)
KITS = {                       # (a, b, altura) em mm
    "A - quadrado":        (235, 255, 105),
    "B - retangular alto": (180, 260, 140),
    "C - retangular baixo":(180, 260,  80),
}
BARRIGA = 3                    # barriga por camada empilhada (mm)

# ----------------------------------------------------------------- geometria
W, D = 780, 580                # frente e profundidade INTERNAS
FRENTE_FICA = 240              # muro de retencao que sobra na frente
ABA_TRAVA = 80                 # aba que desce por dentro e trava a testeira
H = FRENTE_FICA + D + ABA_TRAVA        # 900 - travado pela mecanica
FOLGA_TOPO = 30
DIV = 3                        # espessura da divisoria entre colunas

# coluna: (kit, dim na frente, dim na profundidade)
COLUNAS = [("A - quadrado", 235, 255),
           ("B - retangular alto", 260, 180),
           ("C - retangular baixo", 260, 180)]


def analisa():
    carga = H - FOLGA_TOPO
    larg_usada = sum(c[1] for c in COLUNAS) + DIV * (len(COLUNAS) - 1)
    print(f"Interno {W} x {D} x {H} mm   |   externo "
          f"{W+2*ESP:.0f} x {D+2*ESP:.0f} x {H+2*ESP:.0f} mm")
    print(f"H = {FRENTE_FICA} (frente que fica) + {D} (topo) + {ABA_TRAVA} "
          f"(aba de travamento) = {H} mm\n")
    print(f"{'coluna':<24}{'facing':<10}{'fundos':<10}{'/camada':<10}{'camadas':<10}"
          f"{'kits':<8}{'pilha':<10}{'calco'}")
    tot, vol, alturas = {}, 0.0, []
    for nome, fr, pf in COLUNAS:
        a, b, h = KITS[nome]
        ny = int((D - 10) // pf)
        cam = int((carga + 1e-9) // (h + BARRIGA))
        n = ny * cam
        pilha = cam * h
        alturas.append(pilha)
        tot[nome] = n
        vol += n * a * b * h
        print(f"{nome:<24}{fr:<10}{ny:<10}{ny:<10}{cam:<10}{n:<8}{pilha:<10}", end="")
        print("")
    nivel = max(alturas)
    print()
    for (nome, fr, pf), pilha in zip(COLUNAS, alturas):
        print(f"  calco da coluna {nome[0]}: {nivel - pilha:>3.0f} mm  "
              f"-> topo da carga nivelado em {nivel:.0f} mm")
    print(f"\nlargura usada pelas colunas + {len(COLUNAS)-1} divisorias: "
          f"{larg_usada} mm de {W} (folga {W - larg_usada} mm)")
    print(f"TOTAL: {sum(tot.values())} kits  |  "
          f"{' + '.join(f'{v} {k[0]}' for k, v in tot.items())}  |  "
          f"{min(tot.values())} trios completos")
    print(f"Volume de produto {vol/1e6:.1f} L de {W*D*H/1e6:.1f} L internos "
          f"-> ocupacao {vol/(W*D*H)*100:.0f}%")
    return tot, vol


def chapa():
    """Wrap: FUNDO | FRENTE | TOPO | TRAS | aba de cola."""
    pw = W + ESP
    paineis = [("FUNDO", D + ESP), ("FRENTE", H + ESP),
               ("TOPO", D + ESP), ("TRAS", H + ESP), ("aba de cola", 80)]
    comp = sum(p[1] for p in paineis)
    aba_lat = D / 2 + 25                  # laterais se sobrepoem 50 mm
    larg = pw + 2 * aba_lat
    print(f"\n{'-'*88}\nCHAPA (wrap, onda C 5 mm)")
    for nome, v in paineis:
        print(f"  {nome:<14}{v:>7.0f} mm")
    print(f"  {'aba lateral':<14}{aba_lat:>7.0f} mm (x2, sobrepoem 50 mm no meio da lateral)")
    print(f"  {'painel':<14}{pw:>7.0f} mm de largura")
    print(f"  CHAPA {comp:.0f} x {larg:.0f} mm = {comp*larg/1e6:.2f} m2")
    for g, nome in ((0.50, "onda C simples"), (0.70, "onda BC dupla")):
        print(f"    peso da caixa em {nome}: {comp*larg/1e6*g:.1f} kg")
    return comp, larg


def mckee(ect, t, derate=1.0):
    Z = 2 * (W + D) / 10
    return 5.87 * ect * math.sqrt(t / 10 * Z) * derate


def resistencia(peso_bruto):
    print(f"\n{'-'*88}\nCOMPRESSAO (McKee) - perimetro {2*(W+D)/10:.0f} cm")
    print(f"{'papel':<32}{'ECT':<8}{'esp.':<8}{'BCT fechada':<16}{'margem p/ 2 alturas'}")
    exigido = peso_bruto * 5          # fator 5: 6 meses, UR 80%
    for nome, ect, t in (("onda C simples K180/K180", 5.2, 5.0),
                         ("onda C simples K200/K200", 6.8, 5.0),
                         ("onda BC dupla 175/150/175", 10.5, 7.0)):
        b = mckee(ect, t)
        print(f"{nome:<32}{ect:<8.1f}{t:<8.1f}{b:<16.0f}{b/exigido:.1f}x")
    print(f"\n  Em TRANSPORTE a caixa esta inteira - o picote nao rompeu, os 4 paineis")
    print(f"  trabalham. O derate de painel aberto da Rev.1 nao se aplica mais.")
    print(f"  Carga: 1 caixa sobre a outra = {peso_bruto:.0f} kg; fator 5 -> "
          f"{exigido:.0f} kgf exigidos.")


def palete():
    we, de, he = W + 2*ESP, D + 2*ESP, H + 2*ESP
    print(f"\n{'-'*88}\nPALETE")
    print(f"  meio-palete EUR 800 x 600: caixa {we:.0f} x {de:.0f} -> "
          f"folga {800-we:.0f} / {600-de:.0f} mm  (1 caixa, 100% do meio-palete)")
    print(f"  altura do display: {he:.0f} (caixa) + {D} (testeira) + 144 (palete) "
          f"= {he+D+144:.0f} mm")
    print(f"  2 meios-paletes = 800 x 1200 mm -> cabem num PBR 1000 x 1200 (80% do piso)")


if __name__ == "__main__":
    print("=" * 88)
    print("CAIXA EXPOSITORA SORTIDA - 3 KITS NA MESMA CAIXA")
    print("=" * 88)
    tot, vol = analisa()
    chapa()
    # peso bruto estimado: densidade de embalagem de utilidade domestica em plastico
    peso = vol / 1e6 * 0.12 + 2.2
    print(f"\n  peso bruto estimado: {vol/1e6:.0f} L x 0,12 kg/L + 2,2 kg de caixa "
          f"= {peso:.0f} kg  (ESTIMATIVA - confirmar)")
    resistencia(peso)
    palete()
