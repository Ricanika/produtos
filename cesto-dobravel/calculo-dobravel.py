#!/usr/bin/env python3
"""
Memoria de calculo da linha de cestos organizadores dobraveis empilhaveis em PP.

Arquitetura: fundo unico (comum aos 3 tamanhos) + 4 paineis planos articulados
(2 laterais, 1 traseiro, 1 frontal rebaixado comum). Os paineis dobram sobre o
fundo, o conjunto achata, e a peca empilha pelo pe que assenta no berco do rim.

Regra de empilhamento: a altura externa de cada tamanho e multiplo inteiro do
modulo M, entao qualquer combinacao empilhada fecha em altura redonda e duas
P somam exatamente uma G.

Regra da dobra (a que restringe o projeto): um painel articulado na aresta de
comprimento E tomba sobre a dimensao oposta. Os laterais (articulados nas
arestas longas) tombam sobre a LARGURA interna -- logo a altura do painel nao
pode passar da largura interna, ou a peca nao achata.

Uso:  python3 calculo-dobravel.py [--largura 285]
"""
import sys

RHO       = 0.905e-3    # g/mm3 - PP
EXT_C     = 345.0       # comprimento externo do fundo (mm)
EXT_L     = 285.0       # largura externa do fundo (mm)
T_FUNDO   = 2.2         # parede do fundo (mm)
T_PAINEL  = 1.8         # parede de campo do painel (mm)
T_MOLDURA = 3.0         # moldura perimetral do painel (mm)
H_MOLDURA = 12.0        # altura da moldura perimetral (mm)
T_RIM     = 4.5         # recuo do conjunto rim+coluna de canto por lado (mm)
T_SAIA    = 2.5         # parede da saia do fundo (mm)
H_RIM     = 30.0        # altura do rim/saia do fundo (mm)
VAZADO    = 0.35        # fracao de area aberta no painel
MODULO    = 54.0        # passo de empilhamento (mm)
NMOD      = {"P": 2, "M": 3, "G": 4}
H_FRONTAL = 70.0        # painel frontal rebaixado, comum aos 3 (mm)
T_FRONTAL = 2.0

PRES_PLANO  = 0.40      # t/cm2 - canal frio, peca plana de parede fina
PRES_VALVUL = 0.32      # t/cm2 - camara quente com bico valvulado sequencial
CANAL       = 1.10      # acrescimo de canal/galho no fechamento

CUSTO_KG  = 19.50       # R$/kg de peca acabada - media dos organizadores (TGFCUS)
PRECO_KG  = 36.00       # R$/kg - preco medio de venda da linha (TGFITE 12 meses)
CUBAGEM   = 300.0       # kg/m3 - fator de cubagem rodoviaria


def interno():
    return EXT_C - 2 * T_RIM, EXT_L - 2 * T_RIM


def peso_fundo():
    """Fundo: chapa + saia perimetral + pes/berco de empilhamento e dobradicas."""
    chapa = EXT_C * EXT_L * T_FUNDO
    saia = 2 * (EXT_C + EXT_L) * H_RIM * T_SAIA
    # colunas de canto (o raio externo do produto) + pes + bercos de dobradica
    colunas = 4 * (T_RIM * T_RIM * 2.2) * H_RIM / T_RIM
    extras = 0.12 * (chapa + saia)           # pes, berco de empilhamento, bossas
    return (chapa + saia + colunas + extras) * RHO


def peso_painel(larg, alt, t_campo=T_PAINEL, vazado=VAZADO, t_mold=T_MOLDURA):
    campo = larg * alt * (1 - vazado) * t_campo
    moldura = 2 * (larg + alt) * H_MOLDURA * t_mold
    return (campo + moldura) * RHO


def area_efetiva(larg, alt, vazado):
    """Area projetada que conta no fechamento (o vazado nao conta)."""
    return larg * alt * (1 - vazado) / 100.0     # cm2


def linha():
    ic, il = interno()
    out = []
    for nome, n in NMOD.items():
        h_ext = n * MODULO
        h_int = h_ext - T_FUNDO
        vol = ic * il * h_int / 1e6                      # litros
        p_lat = peso_painel(EXT_L, h_ext)
        p_tras = peso_painel(EXT_C, h_ext)
        p_front = peso_painel(EXT_C, H_FRONTAL, T_FRONTAL, 0.20, T_MOLDURA)
        p_fundo = peso_fundo()
        peso = p_fundo + 2 * p_lat + p_tras + p_front
        dobra_ok = h_ext <= il - 6.0        # traseira sobre a largura: restritiva
        h_dobrado = H_RIM + 4 * T_RIM
        out.append(dict(nome=nome, n=n, h_ext=h_ext, vol=vol, peso=peso,
                        p_fundo=p_fundo, p_lat=p_lat, p_tras=p_tras,
                        p_front=p_front, dobra_ok=dobra_ok,
                        h_dobrado=h_dobrado))
    return out


def main():
    global EXT_L
    if "--largura" in sys.argv:
        EXT_L = float(sys.argv[sys.argv.index("--largura") + 1])

    ic, il = interno()
    print(f"Footprint externo   : {EXT_C:.0f} x {EXT_L:.0f} mm")
    print(f"Footprint interno   : {ic:.0f} x {il:.0f} mm  ({ic*il/100:.0f} cm2)")
    print(f"Modulo empilhamento : {MODULO:.0f} mm  (P={NMOD['P']}M, M={NMOD['M']}M, G={NMOD['G']}M)")
    print(f"Limite da dobra     : painel lateral <= {il-6:.0f} mm (largura interna - folga)\n")

    L = linha()

    print("TAMANHOS")
    print(f"{'':4} {'alt.ext':>8} {'volume':>8} {'peso':>8} {'dobra':>7} {'dobrado':>8} {'compact':>8}")
    for r in L:
        print(f"{r['nome']:4} {r['h_ext']:7.0f}mm {r['vol']:6.2f} L {r['peso']:6.0f} g "
              f"{'ok' if r['dobra_ok'] else 'FALHA':>7} {r['h_dobrado']:6.0f}mm "
              f"{r['h_ext']/r['h_dobrado']:6.1f}x")

    print("\nDECOMPOSICAO DE PESO (g)")
    print(f"{'':4} {'fundo':>7} {'lateral':>8} {'x2':>7} {'traseira':>9} {'frontal':>8} {'total':>7}")
    for r in L:
        print(f"{r['nome']:4} {r['p_fundo']:7.0f} {r['p_lat']:8.0f} {2*r['p_lat']:7.0f} "
              f"{r['p_tras']:9.0f} {r['p_front']:8.0f} {r['peso']:7.0f}")

    print("\nFECHAMENTO POR PECA (t)")
    a_fundo = EXT_C * EXT_L / 100.0
    def linha_fech(rot, area, cavs):
        cel = "  ".join(f"{n}cav {area*PRES_PLANO*CANAL*n:4.0f}/{area*PRES_VALVUL*CANAL*n:4.0f} t"
                        for n in cavs)
        print(f"{rot:12} area {area:5.0f} cm2   {cel}")

    print("  (frio/valvulado)")
    linha_fech("fundo", a_fundo, [1])
    for r in L:
        linha_fech(f"lateral {r['nome']} x2", area_efetiva(EXT_L, r['h_ext'], VAZADO), [1, 2])
        linha_fech(f"traseira {r['nome']}", area_efetiva(EXT_C, r['h_ext'], VAZADO), [1, 2])
    linha_fech("frontal", area_efetiva(EXT_C, H_FRONTAL, 0.20), [1, 2, 4])

    print("\nCUBAGEM E FRETE (fator {:.0f} kg/m3)".format(CUBAGEM))
    print(f"{'':4} {'montado':>10} {'p.cubado':>9} {'dobrado':>10} {'p.cubado':>9} {'ganho':>7}")
    for r in L:
        v_m = EXT_C * EXT_L * r['h_ext'] / 1e9           # m3
        v_d = EXT_C * EXT_L * r['h_dobrado'] / 1e9
        pc_m = max(v_m * CUBAGEM, r['peso'] / 1000)
        pc_d = max(v_d * CUBAGEM, r['peso'] / 1000)
        print(f"{r['nome']:4} {v_m*1000:7.1f} dm3 {pc_m:7.2f}kg {v_d*1000:7.1f} dm3 "
              f"{pc_d:7.2f}kg {pc_m/pc_d:6.1f}x")

    print("\nCUSTO E PRECO (R$/kg de peca: custo {:.2f} / preco {:.2f})".format(CUSTO_KG, PRECO_KG))
    print(f"{'':4} {'custo':>8} {'preco':>8} {'margem':>8} {'R$/L':>7}")
    tot_c = tot_p = 0
    for r in L:
        c = r['peso'] / 1000 * CUSTO_KG
        p = r['peso'] / 1000 * PRECO_KG
        tot_c += c
        tot_p += p
        print(f"{r['nome']:4} {c:7.2f}  {p:7.2f}  {(p-c)/p*100:6.1f}% {p/r['vol']:6.2f}")
    print(f"kit  {tot_c:7.2f}  {tot_p:7.2f}  {(tot_p-tot_c)/tot_p*100:6.1f}%")

    print("\nALOCACAO DE MAQUINA (valvulado, limite de 80% do fechamento)")
    PARQUE = [(120, "13-17, 44, 45"), (150, "42, 43"), (160, "7-12, 36, 40, 41"),
              (200, "1-6, 19-22, 35, 37"), (250, "23-28, 38, 39, 46"), (280, "29"),
              (300, "30"), (380, "31, 32, 33"), (600, "34")]

    def aloca(rot, area, cav_pref):
        for cav in cav_pref:
            t = area * PRES_VALVUL * CANAL * cav
            for ton, maqs in PARQUE:
                if t <= 0.80 * ton:
                    print(f"{rot:14} {cav} cav  {t:5.0f} t -> {ton:4.0f} t "
                          f"({t/ton*100:2.0f}%)  INJ {maqs}")
                    return
        print(f"{rot:14} nao cabe no parque")

    aloca("fundo", a_fundo, [1])
    for r in L:
        aloca(f"lateral {r['nome']} x2", area_efetiva(EXT_L, r['h_ext'], VAZADO), [2, 1])
        aloca(f"traseira {r['nome']}", area_efetiva(EXT_C, r['h_ext'], VAZADO), [2, 1])
    aloca("frontal", area_efetiva(EXT_C, H_FRONTAL, 0.20), [4, 2, 1])

    print("\nCOMBINACOES EMPILHADAS (passo {:.0f} mm)".format(MODULO))
    h = {r['nome']: r['h_ext'] for r in L}
    for combo in (("P", "P"), ("P", "M"), ("M", "M"), ("P", "P", "P"),
                  ("P", "M", "G"), ("G", "G")):
        tot = sum(h[c] for c in combo)
        igual = [k for k, v in h.items() if v == tot]
        nota = f"= {igual[0]}" if igual else ""
        print(f"  {'+'.join(combo):12} {tot:5.0f} mm   {tot/MODULO:.0f} M  {nota}")


# --- ferramental -------------------------------------------------------------
# Benchmark do proprio parque de moldes (AD_MOLDE + AD_ORCAMENTO, valores FOB USD):
#   283-C corpo lixeira 12 L : 720x770x690 mm, 3.000 kg, 380 t -> USD 36.900 (12,3 USD/kg)
#   284-U organizador limpeza: 600x550x600 mm, 1.556 kg, 280 t -> USD 20.100 (12,9 USD/kg)
#   214-U organizador duplo  : 450x550x580 mm, 1.128 kg, 250 t -> USD 18.900 (16,8 USD/kg)
ACO_KG_DM3 = 7.85          # kg/dm3 do bloco de aco
USD_KG     = 14.00         # USD/kg - media dos 3 moldes acima
CAMARA     = 11000.0       # USD - camara quente 4 bicos valvulados (fundo)
INSERTO    = 4000.0        # USD - jogo de inserto de altura por tamanho

MOLDES = [  # rotulo, bloco CxLxA (mm), camara quente?, jogos de inserto
    ("fundo 1 cav",     (620, 540, 520), True,  0),
    ("lateral 2 cav",   (700, 460, 420), False, 2),
    ("traseira 2 cav",  (700, 460, 420), False, 2),
    ("frontal 4 cav",   (620, 420, 360), False, 0),
]


def ferramental():
    print("\nFERRAMENTAL (FOB USD, a %.0f USD/kg de bloco)" % USD_KG)
    total = 0
    for rot, (c, l, a), camara, insertos in MOLDES:
        kg = c * l * a / 1e6 * ACO_KG_DM3
        v = kg * USD_KG + (CAMARA if camara else 0) + insertos * INSERTO
        total += v
        extra = []
        if camara:
            extra.append("camara quente")
        if insertos:
            extra.append(f"{insertos} jogos de inserto")
        print(f"  {rot:16} bloco {c}x{l}x{a}  {kg:5.0f} kg  USD {v:8,.0f}"
              f"   {', '.join(extra)}")
    print(f"  {'TOTAL FOB':16} {'':34} USD {total:8,.0f}")
    return total


def payback(total_usd, cambio=5.45, landed=1.30, un_ano_por_tam=21500):
    L = linha()
    contrib = sum((r['peso'] / 1000) * (PRECO_KG - CUSTO_KG) for r in L)
    receita = un_ano_por_tam * contrib
    invest = total_usd * cambio * landed
    print(f"\nPAYBACK (cambio R$ {cambio:.2f}/USD, nacionalizacao +{(landed-1)*100:.0f}%)")
    print(f"  investimento nacionalizado   R$ {invest:12,.0f}")
    print(f"  margem de contribuicao/kit   R$ {contrib:12,.2f}")
    print(f"  volume assumido              {un_ano_por_tam:,} un/ano por tamanho")
    print(f"  contribuicao anual           R$ {receita:12,.0f}")
    print(f"  payback                      {invest/receita*12:12.1f} meses")


if __name__ == "__main__":
    main()
    payback(ferramental())
