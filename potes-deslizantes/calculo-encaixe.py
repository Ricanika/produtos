#!/usr/bin/env python3
"""
Tampa de ENCAIXE POR ESTALO sobre bordinha engrossada.

O pedido
  Bordinha de 2,0 mm em toda a borda superior do corpo. A tampa abraca essa
  bordinha e prende com um CLIQUE. De cabeca para baixo nao vaza. Aro de TPE
  na tampa.

O que este arquivo decide
  1. a geometria do estalo (quanto engata, quanto a saia flexiona);
  2. o que LIMITA o engate - e a deformacao do PP, nao a forca;
  3. as tres forcas que importam: montar, abrir descascando um canto, e
     arrancar reto;
  4. de cabeca para baixo: passa com folga;
  5. A QUEDA: aqui esta o limite honesto desta tampa, e ele e duro.

O corpo e o mesmo da linha 1 do ombro para baixo. Muda so a borda.

Uso:  python3 calculo-encaixe.py
"""
import importlib.util, math, os

_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calculo-deslizante.py")
_s = importlib.util.spec_from_file_location("base", _p)
K = importlib.util.module_from_spec(_s); _s.loader.exec_module(K)

FP = K.footprint()
POTES = K.linha(FP)
L0, W0 = FP, FP / K.ASP
DIF = L0 - W0
W_BORDA = K.W_BORDA                 # parede constante no alto: 1,40 nos quatro
BOCA_L = L0 - 2 * W_BORDA

# ---------------- a bordinha ----------------
BORDA_P = 2.00                      # quanto a bordinha avanca para fora da parede
BORDA_H = 7.00                      # ALTURA da bordinha. Nao e cota livre: e ela que
                                    # define o balanco que a saia tem para flexionar,
                                    # e portanto quanto o labio pode engatar.
BORDA_L = L0 + 2 * BORDA_P
BORDA_W = W0 + 2 * BORDA_P
BORDA_R = K.R_EXT + BORDA_P
ANG_ENTRADA = 30.0                  # chanfro de cima: facilita pousar
ANG_RETENCAO = 35.0                 # face de baixo: e ela que decide abrir x segurar

# ---------------- a saia da tampa ----------------
SAIA_T = 1.60                       # espessura da saia
LABIO_T = 1.20                      # espessura do labio do estalo
SAIA_L = BORDA_H + LABIO_T          # AMARRADO a bordinha: o labio fica logo abaixo dela
ENGATE = 0.55                       # quanto o labio avanca por baixo da bordinha
FOLGA = 0.15                        # folga radial fora da zona do aro
E_PP = 900.0
EPS_CICLO = 2.0                     # % de deformacao admissivel em ciclagem

# ---------------- o aro ----------------
ARO_SEC = (2.4, 1.8)
ARO_CAN = 0.60                      # profundidade da canaleta na face interna da saia
ARO_COMP = 0.20                     # compressao radial contra a face externa da bordinha
MU_SECO, MU_SABAO = 0.30, 0.08
L_DESCASCA = 30.0                   # quanto de perimetro trabalha ao levantar um canto


def perim(a, b, r):
    return 2 * (a + b) - (8 - 2 * math.pi) * r


def sep(t):
    print("\n" + t + "\n" + "-" * len(t))


def f_radial_mm(L, e, t=SAIA_T):
    """Forca radial por mm de perimetro para abrir a saia de e mm."""
    I = t ** 3 / 12
    return 3 * E_PP * I * e / L ** 3


def eps(L, e, t=SAIA_T):
    return 3 * t * e / (2 * L ** 2) * 100


def fator(ang, mu):
    ta = math.tan(math.radians(ang))
    return (ta + mu) / (1 - mu * ta)


def main():
    PER = perim(BORDA_L, BORDA_W, BORDA_R)

    sep("1. A BORDINHA")
    print(f"Corpo (linha 1, inalterado do ombro para baixo): {L0:.1f} x {W0:.1f} mm")
    print(f"Parede no alto {W_BORDA:.2f} mm IGUAL nos quatro -> boca {BOCA_L:.1f} mm nos quatro,")
    print(f"  que e o que deixa UMA tampa servir os quatro tamanhos.")
    print(f"\nBordinha: avanca {BORDA_P:.2f} mm para fora, altura {BORDA_H:.2f} mm")
    print(f"  face externa da bordinha {BORDA_L:.1f} x {BORDA_W:.1f} mm, canto R{BORDA_R:.0f}")
    print(f"  perimetro {PER:.0f} mm")
    print(f"  chanfro de cima {ANG_ENTRADA:.0f}° (para pousar) | face de baixo "
          f"{ANG_RETENCAO:.0f}° (para segurar)")
    print(f"  o aro de TPE mora dentro dessa altura: canaleta a 1,5-3,9 mm abaixo do topo")
    print(f"\nA face de baixo a {ANG_RETENCAO:.0f}° e a cota mais importante da peca:")
    print(f"  a 90° a tampa nao sai mais nem com alicate; a 20° ela pula sozinha.")

    sep("2. QUEM MANDA E A ALTURA DA BORDINHA, NAO A ESPESSURA")
    print("A saia so flexiona no trecho que vai do prato ate o labio, e esse trecho E a")
    print("altura da bordinha. Entao a altura da bordinha decide tudo:")
    print(f"      balanco L = altura da bordinha + {LABIO_T:.1f} mm")
    print(f"      eps = 3 . t . engate / (2 . L^2)   ->   engate maximo cresce com L^2")
    print(f"\nA espessura de {BORDA_P:.1f} mm que voce pediu e a PROJECAO - ela define o")
    print(f"quanto o labio tem por baixo para agarrar. A ALTURA eu tive de escolher, e e")
    print(f"ela que faz o compromisso abaixo.")
    m24 = 2400 * 1.03 / 1000 + POTES[3]['peso'] / 1000
    print(f"\n{'bordinha':>9} {'balanco':>8} {'engate':>8} {'F radial':>9} {'abrir um':>10} "
          f"{'arrancar':>10} {'queda':>7}")
    print(f"{'altura':>9} {'L (mm)':>8} {'max(mm)':>8} {'(N/mm)':>9} {'canto':>10} "
          f"{'reto':>10} {'limite':>7}")
    for H in (4.0, 5.0, 6.0, 7.0, 9.0, 12.0):
        L = H + LABIO_T
        e = EPS_CICLO / 100 * 2 * L ** 2 / (3 * SAIA_T)
        fr = f_radial_mm(L, e)
        fd = fr * L_DESCASCA * fator(ANG_RETENCAO, MU_SECO)
        fa = fr * PER * fator(ANG_RETENCAO, MU_SECO)
        h = fa * 0.008 / (m24 * 9.81)
        marca = "  <- escolhido" if abs(H - BORDA_H) < 0.01 else ""
        print(f"{H:>8.1f}mm {L:>8.1f} {e:>8.2f} {fr:>9.3f} {fd/9.81:>9.1f}kgf "
              f"{fa/9.81:>9.0f}kgf {h*100:>6.0f}cm{marca}")
    print(f"\nBordinha BAIXA da saia curta, que e RIGIDA: segura mais na queda mas custa")
    print(f"mais para abrir. Bordinha alta faz o contrario. Nao existe altura que melhore")
    print(f"as duas - e o mesmo compromisso que aparece na secao 5, visto por outro lado.")
    print(f"\nEscolhido {BORDA_H:.1f} mm de altura, engate de {ENGATE:.2f} mm "
          f"(eps {eps(SAIA_L, ENGATE):.2f}%):")
    print(f"  abrir um canto fica em torno de 3,5 kgf, que e a janela boa para a mao,")
    print(f"  e a bordinha de {BORDA_H:.1f} mm ainda le como detalhe de borda, nao como faixa.")

    sep("3. AS TRES FORCAS")
    fr = f_radial_mm(SAIA_L, ENGATE)
    print(f"Forca radial para abrir a saia {ENGATE:.2f} mm: {fr:.3f} N por mm de perimetro")
    print(f"  ({fr*PER:.0f} N se o perimetro inteiro abrisse junto)")
    print(f"\n{'':>26} {'mu=0,08':>12} {'mu=0,30':>12}")
    for nome, comp, ang in (("MONTAR (pousa e aperta)", PER / 3, ANG_ENTRADA),
                            ("ABRIR descascando um canto", L_DESCASCA, ANG_RETENCAO),
                            ("ARRANCAR reto", PER, ANG_RETENCAO)):
        vals = []
        for mu in (MU_SABAO, MU_SECO):
            F = fr * comp * fator(ang, mu)
            vals.append(f"{F/9.81:>8.1f} kgf")
        print(f"  {nome:<24} {vals[0]:>12} {vals[1]:>12}")
    print(f"\n  MONTAR supoe que so 1/3 do perimetro encaixa por vez - e como se poe tampa")
    print(f"  de pote: aperta um lado, depois o outro. Apertar tudo junto seria 3x isso.")
    print(f"  A diferenca entre ABRIR e ARRANCAR e o perimetro que trabalha: "
          f"{PER/L_DESCASCA:.0f}x.")
    print(f"  E dessa razao que sai o produto - e tambem o seu limite, na secao 5.")

    sep("4. DE CABECA PARA BAIXO: PASSA COM FOLGA")
    a_boca = K.area(BOCA_L, BOCA_L - DIF, K.R_EXT - W_BORDA) / 1e2
    fa = fr * PER * fator(ANG_RETENCAO, MU_SECO)
    print(f"Area da boca {a_boca:.0f} cm2. Coluna de sabao (rho 1,03) empurrando a tampa:")
    for p in POTES:
        dp = 1030 * 9.81 * (p['H_ext'] / 1000) / 1000
        F = dp * 1000 * a_boca / 1e4
        print(f"  {p['cap']:>5} ml -> {dp:4.1f} kPa -> {F:5.1f} N = {F/9.81:4.2f} kgf "
              f"| margem {fa/F:>5.0f}x")
    print(f"\nO pedido 'de cabeca para baixo nao vaza' esta atendido com folga enorme.")
    print(f"Quem veda e o aro (secao 6); o estalo so precisa nao deixar a tampa subir.")

    sep("5. A QUEDA: O LIMITE HONESTO DESTA TAMPA")
    print(f"Capacidade de arranque reto: {fa:.0f} N. Agora a queda do 2,4 L cheio "
          f"({m24:.2f} kg):")
    print(f"\n{'altura':>8} {'parada':>8} {'forca':>10} {'vs capacidade':>15}")
    for h, d in ((0.10, 0.008), (0.14, 0.008), (0.30, 0.008), (0.75, 0.008), (1.00, 0.008)):
        F = m24 * 9.81 * h / d
        print(f"{h:>7.2f}m {d*1000:>7.0f}mm {F:>9.0f} N {('SEGURA' if F < fa else 'ABRE'):>15}")
    hlim = fa * 0.008 / (m24 * 9.81)
    print(f"\n  Limite: cerca de {hlim*100:.0f} cm. Acima disso a tampa sai.")
    print(f"\nPOR QUE NAO DA PARA CONSERTAR ISSO SO MEXENDO NA COTA:")
    print(f"  arrancar / descascar = {PER/L_DESCASCA:.0f}x, e essa razao e geometrica -")
    print(f"  depende do perimetro, nao da rigidez. Se eu engrossar a saia ou aumentar o")
    print(f"  angulo de retencao, as DUAS sobem juntas: a queda melhora e abrir com a mao")
    print(f"  piora na mesma proporcao. Para segurar 0,75 m precisaria de face a ~68°, e ai")
    print(f"  abrir um canto pediria mais de 15 kgf.")
    print(f"\n  E exatamente por isso que pote retangular hermetico do mercado tem TRAVA.")
    print(f"  A trava desacopla as duas coisas; o estalo, nao.")
    print(f"\n  COMPARANDO com a tampa de came deste mesmo projeto:")
    print(f"    came com ganchos ..... segura 1,00 m (a carga entra em esmagamento)")
    print(f"    estalo na bordinha ... segura {hlim*100:.0f} cm")
    print(f"  Nao e defeito de dimensionamento, e a natureza do fecho. O estalo e o fecho")
    print(f"  certo para 600 ml e 1,2 L e para mantimento; a came e para o 2,4 L de liquido.")

    sep("6. A VEDACAO: O ARO NO PROPRIO ABRACO")
    print(f"O aro NAO vai esmagado entre a tampa e a borda. Ele vai numa canaleta na face")
    print(f"INTERNA da saia, trabalhando RADIALMENTE contra a face externa da bordinha -")
    print(f"ou seja, o abraco que prende e o mesmo que veda.")
    print(f"\n  canaleta {ARO_CAN:.2f} mm de profundidade | aro {ARO_SEC[0]:.1f} x "
          f"{ARO_SEC[1]:.1f} mm")
    print(f"  sobra {ARO_SEC[1]-ARO_CAN:.2f} mm -> comprime {ARO_COMP:.2f} mm contra a bordinha")
    print(f"  perimetro do aro {PER:.0f} mm")
    E_TPE_R, FORMA, MU_TPE = 1.8, 1.8, 0.75
    pres = E_TPE_R * (ARO_COMP / ARO_SEC[1]) * FORMA
    larg = 0.9 * math.sqrt(ARO_SEC[1] * ARO_COMP)
    F_aro = MU_TPE * pres * PER * larg
    print(f"  atrito do aro: arrancar reto {F_aro/9.81:.1f} kgf | descascando um canto "
          f"{F_aro/9.81/6:.1f} kgf")
    print(f"\nPOR QUE RADIAL E NAO AXIAL - e a razao vale o projeto inteiro:")
    print(f"  o prato da tampa EMPENA sob pressao interna (secao 7). Aro axial perde contato")
    print(f"  no meio do lado longo quando isso acontece. Aro radial acompanha a parede: a")
    print(f"  bordinha nao se move, e o aro esta preso nela, nao no prato que empena.")

    sep("7. O EMPENAMENTO DO PRATO")
    for t in (1.5, 2.0, 2.5):
        D = E_PP * t ** 3 / (12 * (1 - 0.42 ** 2))
        q = 1030 * 9.81 * (POTES[3]['H_ext'] / 1000) / 1e6      # N/mm2
        b = BOCA_L - DIF
        w_ss = 0.0084 * q * b ** 4 / D
        w_cl = 0.00126 * q * b ** 4 / D
        marca = "  <- o estalo segura a borda, entao o real fica perto do engastado" if t == 2.0 else ""
        print(f"  prato {t:.1f} mm -> apoiado {w_ss:5.2f} mm | engastado {w_cl:5.2f} mm{marca}")
    print(f"\n  Com aro radial nenhum desses valores vaza. Com aro axial, o de 'apoiado'")
    print(f"  vazaria. E o argumento da secao 6 em numero.")

    sep("8. MOLDE")
    print(f"CORPO: a face de baixo da bordinha olha para baixo e para fora -> EXTRACAO RETA.")
    print(f"  Mesma situacao do labio da came: nenhuma gaveta, nos quatro tamanhos.")
    print(f"TAMPA: o labio do estalo e contra-saida, mas a saia ABRE {ENGATE:.2f} mm para")
    print(f"  desmoldar - por arranque, sem gaveta. A mesma flexao que faz o clique.")
    print(f"  Deformacao no arranque = deformacao no uso = {eps(SAIA_L, ENGATE):.2f}%. Isso e")
    print(f"  bom e e ruim: nao ha gaveta nenhuma na linha, mas a peca que desmolda flexionando")
    print(f"  tambem flexiona em servico. E o motivo fisico do limite da secao 5.")

    sep("9. O QUE FICA ABERTO")
    abertos = [
        ["Medir o atrito PP/PP com filme de sabao: a janela de abrir depende dele."],
        ["Ciclagem: 2.000 aberturas medindo a perda de engate (o labio 'cansa')."],
        ["Queda instrumentada para achar a altura real - a conta usa parada em 8 mm,",
         "que e estimativa, e o resultado e proporcional a ela."],
        ["Estanqueidade: agua colorida, 24 h, deitado e invertido."],
        ["Decidir a aplicacao por tamanho: estalo nos menores, came no 2,4 L de liquido."],
    ]
    for i, linhas in enumerate(abertos, 1):
        print(f"  {i:>2}. {linhas[0]}")
        for extra in linhas[1:]:
            print(f"      {extra}")


if __name__ == '__main__':
    main()
