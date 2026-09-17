#!/usr/bin/env python3
"""
Gerador de G-code (FDM) do corpo de 600 ml e da tampa deslizante.

POR QUE FDM, E NAO CNC
  As duas pecas sao cascas de 1,15 a 3,4 mm com rebaixos internos. Usinar isso
  de um bloco nao faz sentido. O objetivo aqui e o item 7 da lista de aberto:
  protótipo na mão, para sentir a entrada do gancho, a puxada da came e o curso.

O QUE O PROTOTIPO IMPRESSO VALIDA - E O QUE NAO VALIDA
  VALIDA   a cinematica: entrada pelas janelas, curso de 18 mm, a came puxando
           2,00 mm, o gancho assentando no patamar, e sobretudo a RETENCAO -
           de cabeca para baixo a tampa nao sai.
  NAO VALIDA
           - vedacao. Linha de camada vaza. Sem o labio de TPE nao ha junta.
           - o clique. As 4 linguetas do detente ficam FORA desta versao: uma
             lingueta de 1,4 mm em PLA nao representa o PP, e sem a junta nao
             ha mola contra a qual o detente trabalhe. O detente e a ultima
             coisa a acertar, e se acerta no try-out do molde.
           - forca de abrir, atrito e fluencia. PLA nao e PP.

ESTRATEGIA DE FATIAMENTO
  Nao fatia STL: gera o caminho direto da geometria parametrica. Cada camada
  sabe exatamente que regioes existem naquele z, entao parede fina sai como
  passe de centro (sem costura de contorno) e a rampa da came sai exata, sem
  degrau de malha.

ORIENTACAO DE IMPRESSAO
  CORPO  de pe, fundo na mesa. O fundo macico da a aderencia. Precisa de suporte
         em dois aneis: sob o degrau do pe embutido, e sob a aba/labio - esse
         segundo e um tubo de parede fina de ~53 mm, estavel porque e fechado.
         O topo do suporte ACOMPANHA A RAMPA da came (funcao teto()).
  TAMPA  de cabeca para baixo, murete na mesa. Nessa posicao as asas dos ganchos
         apontam para cima e ficam auto-sustentadas na ponta do poste. O prato
         pede suporte porque vence 114 mm de vao sobre o murete.

FOLGA DE MONTAGEM
  FIT = 0,22 mm nas faces que se tocam. Sem isso, em PLA, as pecas nao entram.
  Em producao (PP, molde) a folga e outra - esta e folga de impressao.

Uso:  python3 gera-gcode.py [--material pla|petg]
      escreve gcode/corpo-600.gcode e gcode/tampa.gcode
"""
import importlib.util, math, os, sys

_spec = importlib.util.spec_from_file_location(
    "calc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "calculo-deslizante.py"))
K = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(K)

# ---------------------------------------------------------------- impressao
MAT = 'petg' if '--material' in sys.argv and 'petg' in sys.argv else 'pla'
TEMP, BED = (240, 80) if MAT == 'petg' else (210, 60)
FILA_A  = math.pi * (1.75 / 2) ** 2      # mm2 de secao do filamento
NOZZLE, LAYER, LAYER1 = 0.40, 0.20, 0.28
EW      = 0.42                            # largura de extrusao padrao
EW_MAX  = 0.75                            # largura maxima num passe so
V_L1, V_PER, V_FILL, V_SUP, V_TRAV = 20, 35, 45, 50, 120
RETRACT, V_RET = 1.0, 35
BED_X, BED_Y = 220, 220
FIT = 0.22
SUP_GAP, SUP_W, SUP_PITCH = 0.25, 0.42, 1.6

# ---------------------------------------------------------------- cotas
FP     = K.footprint()
FND    = K.fundos(FP)
POTE   = K.linha(FP, FND)[0]                       # o 600 ml
L0, W0 = POTE['ext_l'], POTE['ext_w']
WALL   = POTE['w']
FUNDO  = POTE['fundo']
POT_H  = POTE['H_ext']
DIF    = L0 - W0
PE_L, PE_W, PE_H = K.PE_L, K.PE_L - DIF, K.PE_H
DEGRAU = POTE['degrau']
R      = K.R_EXT
ABA_L, ABA_W2, ABA_T = L0 + 2 * K.ABA_W, W0 + 2 * K.ABA_W, K.ABA_T
ABA_R  = R + K.ABA_W
MO_L, MO_W, MO_R = L0 - 2 * WALL, W0 - 2 * WALL, R - WALL

CAME_T = K.CAME_T
SK_FUNDO, SK_RASO = 5.1, 3.1                      # labio: profundo e raso
assert abs((SK_FUNDO - SK_RASO) - K.RAMPA_DZ) < 1e-9, "a rampa tem de fechar a queda"
SKIRT_T = 1.2                                      # labio dos lados curtos
NH      = K.GANCHO_N // 2
RETO    = ABA_L - 2 * ABA_R        # so o trecho RETO do lado longo recebe trilho:
                                   # fora dele a aba ja curvou e nao ha material
                                   # sobre o gancho.
CELL    = RETO / NH
WIN     = K.GANCHO_W + 1.0
HOOK, HOOK_P = K.GANCHO_W, K.GANCHO_P
CURSO, RAMPA_L = K.CURSO, K.RAMPA_L
assert HOOK + RAMPA_L <= CURSO + 1e-9, "gancho nao assenta inteiro no patamar"

PRATO, MUR_H, MUR_T, MUR_I = K.PRATO_T, K.MURETE_H, K.MURETE_T, K.PE_L + 2 * K.FOLGA_PE
LID_L, LID_W = ABA_L + 2 * HOOK_P, ABA_W2 + 2 * HOOK_P
LID_R, SAIA_H = ABA_R + HOOK_P, K.SAIA_H

Z_ABA_B = POT_H - ABA_T                            # face de baixo da aba
Z_SK_B  = POT_H - SK_FUNDO                         # base do labio no patamar
Z_SK_R  = POT_H - SK_RASO                          # base do labio na ponta rasa


def rail_start(k):
    return -RETO / 2 + k * CELL + WIN


def rail_bottom(u):
    """z da aresta de baixo do labio, a u mm do inicio do trilho."""
    return Z_SK_R - (K.RAMPA_DZ / RAMPA_L) * min(max(u, 0.0), RAMPA_L)


assert CELL - WIN >= CURSO - 1e-9, (
    f"trilho de {CELL-WIN:.2f} mm nao comporta curso de {CURSO}")
assert HOOK + RAMPA_L <= CURSO + 1e-9, "gancho nao assenta inteiro no patamar"
assert abs((SK_FUNDO - SK_RASO) - K.RAMPA_DZ) < 1e-9, "a rampa tem de fechar a queda"


def teto(x, y):
    """z da face de baixo da peca acima do ponto (x, y) - define ate onde sobe
    o suporte. E ela que faz o topo do suporte ACOMPANHAR a rampa da came."""
    if abs(y) > W0 / 2 and abs(x) <= RETO / 2 + 1e-6:
        for k in range(NH):
            u = x - rail_start(k)
            if -1e-6 <= u <= CELL - WIN + 1e-6:
                return rail_bottom(u)
        return Z_ABA_B
    if abs(y) <= ABA_W2 / 2 - ABA_R and abs(x) >= ABA_L / 2 - SKIRT_T - 0.5:
        return Z_SK_B
    return Z_ABA_B


# ---------------------------------------------------------------- geometria
def rr(L, W, rad, seg=16):
    """Retangulo de cantos arredondados, fechado."""
    l, w, p = L / 2 - rad, W / 2 - rad, []
    for cx, cy, a0 in ((l, -w, -math.pi / 2), (l, w, 0.0),
                       (-l, w, math.pi / 2), (-l, -w, math.pi)):
        for i in range(seg + 1):
            a = a0 + (math.pi / 2) * i / seg
            p.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    p.append(p[0])
    return p


def rect(x0, x1, y0, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]


def densify(loop, step=1.0):
    out = [loop[0]]
    for a, b in zip(loop, loop[1:]):
        d = math.dist(a, b)
        k = max(1, int(d / step))
        for i in range(1, k + 1):
            out.append((a[0] + (b[0] - a[0]) * i / k, a[1] + (b[1] - a[1]) * i / k))
    return out


def grow(loop, d):
    """Afasta o poligono do proprio centroide por d (d<0 encolhe). Serve para as
    formas usadas aqui - retangulos arredondados e caixas, todas estreladas."""
    cx = sum(p[0] for p in loop[:-1]) / (len(loop) - 1)
    cy = sum(p[1] for p in loop[:-1]) / (len(loop) - 1)
    out = []
    for (x, y) in loop:
        r = math.hypot(x - cx, y - cy)
        s = (r + d) / r if r > 1e-9 else 0.0
        out.append((cx + (x - cx) * s, cy + (y - cy) * s))
    return out


def scanlines(loops, spacing, angle):
    """Preenchimento: corta as loops com retas a `angle`, pares alternados."""
    ca, sa = math.cos(-angle), math.sin(-angle)
    rot = [[(x * ca - y * sa, x * sa + y * ca) for (x, y) in lp] for lp in loops]
    ys = [p[1] for lp in rot for p in lp]
    if not ys:
        return []
    out, y = [], math.floor(min(ys) / spacing) * spacing + spacing
    ba, bs = math.cos(angle), math.sin(angle)
    flip = False
    while y < max(ys):
        xs = []
        for lp in rot:
            for i in range(len(lp) - 1):
                (x1, y1), (x2, y2) = lp[i], lp[i + 1]
                if (y1 <= y < y2) or (y2 <= y < y1):
                    xs.append(x1 + (x2 - x1) * (y - y1) / (y2 - y1))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            if xs[i + 1] - xs[i] > 0.35:
                a = (xs[i] * ba - y * bs, xs[i] * bs + y * ba)
                b = (xs[i + 1] * ba - y * bs, xs[i + 1] * bs + y * ba)
                out.append([b, a] if flip else [a, b])
        flip = not flip
        y += spacing
    return out


# ---------------------------------------------------------------- emissor
class GC:
    def __init__(self, titulo, nota):
        self.L, self.e, self.z, self.pos, self.ret = [], 0.0, None, None, False
        self.dist, self.nlayer = 0.0, 0
        self.L += [f"; {titulo}",
                   f"; {nota}",
                   "; gerado por gera-gcode.py - projeto potes-deslizantes",
                   f"; material {MAT.upper()}  bico {NOZZLE} mm  camada {LAYER} mm",
                   f"; folga de montagem entre as pecas: {FIT} mm",
                   "; sem skirt/brim: o proprio suporte faz a primeira camada de ancoragem",
                   "M82", "G21", "G90",
                   f"M104 S{TEMP}", f"M140 S{BED}", "G28",
                   f"M190 S{BED}", f"M109 S{TEMP}", "G92 E0", "M107",
                   "; purga",
                   f"G1 Z{LAYER1:.2f} F600", "G1 X5 Y20 F3000",
                   "G1 X5 Y180 E12.0 F1200", "G1 X5.6 Y180 F3000",
                   "G1 X5.6 Y20 E24.0 F1200", "G92 E0",
                   "G1 E-1.0 F2100", "G1 Z2.0 F600"]
        self.pos = (5.6 - BED_X / 2, 20 - BED_Y / 2)
        self.ret = True

    def mark(self, tipo):
        """Marca o trecho no G-code. Deixa o suporte identificavel no laminador
        e permite conferir, camada a camada, se o topo dele segue a rampa."""
        self.L.append(f"; tipo={tipo}")

    def layer(self, z, fan):
        self.nlayer += 1
        self.z = z
        self.L.append(f"; ---- camada {self.nlayer}  z={z:.2f}")
        self.L.append("; tipo=peca")
        self.L.append(f"G1 Z{z:.3f} F900")
        self.L.append(f"M106 S{fan}")

    def path(self, pts, w, v):
        if len(pts) < 2:
            return
        h = LAYER1 if self.nlayer <= 1 else LAYER
        v = V_L1 if self.nlayer <= 1 else v
        if math.dist(self.pos, pts[0]) > 1.5 and not self.ret:
            self.L.append(f"G1 E{self.e - RETRACT:.5f} F{V_RET*60:.0f}")
            self.ret = True
        self.L.append(f"G1 X{pts[0][0]+BED_X/2:.3f} Y{pts[0][1]+BED_Y/2:.3f} "
                      f"F{V_TRAV*60:.0f}")
        self.pos = pts[0]
        if self.ret:
            self.L.append(f"G1 E{self.e:.5f} F{V_RET*60:.0f}")
            self.ret = False
        k = w * h / FILA_A
        for p in pts[1:]:
            d = math.dist(self.pos, p)
            if d < 1e-6:
                continue
            self.e += d * k
            self.dist += d
            self.L.append(f"G1 X{p[0]+BED_X/2:.3f} Y{p[1]+BED_Y/2:.3f} "
                          f"E{self.e:.5f} F{v*60:.0f}")
            self.pos = p

    def ring_rr(self, L, W, rad, t, v=V_PER):
        """Parede fina: n passes concentricos de t/n, a partir da face externa."""
        n = max(1, math.ceil(t / EW_MAX))
        w = t / n
        for i in range(n):
            d = (i + 0.5) * w
            self.path(rr(L - 2 * d, W - 2 * d, max(0.6, rad - d)), w, v)

    def solid(self, outer, holes, ang):
        self.path(outer, EW, V_PER)
        for hl in holes:
            self.path(hl, EW, V_PER)
        self.path(grow(outer, -EW), EW, V_PER)
        for hl in holes:
            self.path(grow(hl, EW), EW, V_PER)
        region = [grow(outer, -1.9 * EW)] + [grow(hl, 1.9 * EW) for hl in holes]
        for seg in scanlines(region, EW * 0.97, ang):
            self.path(seg, EW, V_FILL)

    def box(self, x0, x1, y0, y1, ang):
        if x1 - x0 < 0.5 or y1 - y0 < 0.5:
            return
        o = rect(x0, x1, y0, y1)
        self.path(o, EW, V_PER)
        if min(x1 - x0, y1 - y0) > 2.6:
            self.solid(o, [], ang)
        else:
            self.path(grow(o, -EW), EW, V_PER)

    def save(self, path):
        self.L += [f"G1 E{self.e - RETRACT:.5f} F2100", "M104 S0", "M140 S0", "M107",
                   f"G1 Z{(self.z or 0) + 20:.2f} F900", "G1 X0 Y200 F3000", "M84",
                   f"; camadas {self.nlayer}  filamento {self.e/1000:.2f} m"]
        open(path, 'w').write("\n".join(self.L) + "\n")
        vol = self.e * FILA_A / 1000.0                      # cm3
        return dict(layers=self.nlayer, m=self.e / 1000, g=vol * 1.24,
                    h=self.dist / ((V_PER + V_FILL) / 2) / 3600 * 1.5)


def camadas(h):
    z, n = LAYER1, 1
    while z < h - 1e-6:
        yield n, z, (LAYER1 if n == 1 else LAYER)
        z += LAYER
        n += 1


def fan(n):
    if n <= 1:
        return 0
    if n == 2:
        return 100
    return 120 if MAT == 'petg' else 255


def ang(n):
    return math.pi / 4 if n % 2 else 3 * math.pi / 4


# ---------------------------------------------------------------- CORPO
def corpo(g):
    R_PE = R - DEGRAU
    for n, z, h in camadas(POT_H):
        g.layer(z, fan(n))
        zm = z - h / 2
        if zm < FUNDO:
            g.solid(rr(PE_L, PE_W, R_PE), [], ang(n))
        elif zm < PE_H:
            g.ring_rr(PE_L, PE_W, R_PE, WALL)
        if PE_H <= zm < PE_H + WALL:
            g.solid(rr(L0, W0, R),
                    [rr(PE_L - 2 * WALL, PE_W - 2 * WALL, max(0.6, R_PE - WALL))], ang(n))
        elif PE_H + WALL <= zm < Z_ABA_B:
            g.ring_rr(L0, W0, R, WALL)
        if Z_ABA_B <= zm < POT_H:
            g.solid(rr(ABA_L, ABA_W2, ABA_R), [rr(MO_L, MO_W, MO_R)], ang(n))
        if Z_SK_B <= zm < Z_ABA_B:
            ylim = ABA_W2 / 2 - ABA_R
            for sx in (-1, 1):
                a, b = sx * ABA_L / 2, sx * (ABA_L / 2 - SKIRT_T)
                g.box(min(a, b), max(a, b), -ylim, ylim, ang(n))
            slope = K.RAMPA_DZ / RAMPA_L
            for sy in (-1, 1):
                for k in range(NH):
                    umin = max(0.0, (Z_SK_R - zm) / slope)
                    if umin < CELL - WIN - 0.4:
                        x0 = rail_start(k) + umin
                        x1 = rail_start(k) + (CELL - WIN)
                        a, b = sy * W0 / 2, sy * ABA_W2 / 2
                        g.box(x0, x1, min(a, b), max(a, b), ang(n))
        sup_corpo(g, zm)


def sup_corpo(g, zm):
    """Dois aneis de suporte. O de baixo e largo e segura o degrau do pe; o de
    cima e um tubo fino de parede unica, estavel por ser fechado, e seu topo
    acompanha a rampa da came ponto a ponto."""
    g.mark("suporte")
    if zm < PE_H - SUP_GAP:
        d = 0.8
        while ABA_L - 2 * d > PE_L + 2.0:
            g.path(rr(ABA_L - 2 * d, ABA_W2 - 2 * d, max(0.6, ABA_R - d)), SUP_W, V_SUP)
            d += SUP_PITCH
        return
    for d in (0.7, 2.3, 3.9):
        if ABA_L - 2 * d < L0 + 1.4:
            continue
        loop = densify(rr(ABA_L - 2 * d, ABA_W2 - 2 * d, max(0.6, ABA_R - d)), 1.2)
        run = []
        for p in loop:
            if teto(*p) - SUP_GAP > zm:
                run.append(p)
            else:
                if len(run) > 2:
                    g.path(run, SUP_W, V_SUP)
                run = []
        if len(run) > 2:
            g.path(run, SUP_W, V_SUP)


# ---------------------------------------------------------------- TAMPA
WING_T = 1.8
Z_PRATO0 = MUR_H
Z_PRATO1 = MUR_H + PRATO
Z_SAIA1 = Z_PRATO1 + SAIA_H
Z_WING0 = Z_PRATO1 + SK_FUNDO + FIT
SAIA_IN_L, SAIA_IN_W = ABA_L + 2 * FIT, ABA_W2 + 2 * FIT
WING_Y0, WING_Y1 = W0 / 2 + FIT, ABA_W2 / 2 + FIT
HOOK_X = [rail_start(k) + CURSO - HOOK / 2 for k in range(NH)]
MUR_O, MUR_RO = MUR_I + 2 * MUR_T, 14.0


def tampa(g):
    for n, z, h in camadas(Z_SAIA1):
        g.layer(z, fan(n))
        zm = z - h / 2
        if zm < Z_PRATO0:
            g.ring_rr(MUR_O, MUR_O - DIF, MUR_RO, MUR_T)
        elif zm < Z_PRATO1:
            g.solid(rr(LID_L, LID_W, LID_R), [], ang(n))
        else:
            g.ring_rr(LID_L, LID_W, LID_R, HOOK_P - FIT)
            if zm >= Z_WING0:
                for sy in (-1, 1):
                    for xc in HOOK_X:
                        g.box(xc - HOOK / 2, xc + HOOK / 2,
                              sy * WING_Y1 if sy < 0 else WING_Y0,
                              sy * WING_Y0 if sy < 0 else WING_Y1, ang(n))
        sup_tampa(g, zm, n)


def sup_tampa(g, zm, n):
    g.mark("suporte")
    if zm < Z_PRATO0 - SUP_GAP:
        fino = zm > Z_PRATO0 - SUP_GAP - 0.5
        pitch = 1.3 if fino else 3.0
        d = 0.8
        while LID_L - 2 * d > 9.0:
            Ld = LID_L - 2 * d
            if not (MUR_I - 1.3 < Ld < MUR_O + 1.3):
                g.path(rr(Ld, LID_W - 2 * d, max(0.6, LID_R - d)), SUP_W, V_SUP)
            d += pitch
    elif Z_PRATO1 <= zm < Z_WING0 - SUP_GAP:
        for sy in (-1, 1):
            for xc in HOOK_X:
                y0, y1 = WING_Y0 + 0.35, WING_Y1 - 0.35
                a, b = (sy * y1, sy * y0) if sy < 0 else (y0, y1)
                g.path(rect(xc - HOOK / 2 + 0.6, xc + HOOK / 2 - 0.6,
                            min(a, b), max(a, b)), SUP_W, V_SUP)


# ---------------------------------------------------------------- main
def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gcode")
    os.makedirs(out, exist_ok=True)
    print(f"Material {MAT.upper()} | bico {NOZZLE} | camada {LAYER} | folga {FIT} mm")
    print(f"Corpo {L0:.1f} x {W0:.1f} x {POT_H:.1f} mm | "
          f"Tampa {LID_L:.1f} x {LID_W:.1f} x {Z_SAIA1:.1f} mm")
    print(f"Trilho: {NH} celulas de {CELL:.2f} = janela {WIN:.1f} + trilho {CELL-WIN:.2f} "
          f"(curso {CURSO:.0f}, rampa {RAMPA_L:.0f})")
    print(f"Ganchos em x = " + ", ".join(f"{x:+.2f}" for x in HOOK_X) + " (nos dois lados)\n")

    for nome, fn, titulo, nota in (
        ("corpo-600.gcode", corpo, "Pote modular 600 ml - corpo",
         "de pe, fundo na mesa; suporte em 2 aneis, o de cima acompanha a rampa"),
        ("tampa.gcode", tampa, "Tampa deslizante de came",
         "de cabeca para baixo, murete na mesa; suporte sob o prato e sob as asas")):
        g = GC(titulo, nota)
        fn(g)
        st = g.save(os.path.join(out, nome))
        print(f"{nome:>16}  {st['layers']:>4} camadas  {st['m']:>6.2f} m de filamento  "
              f"~{st['g']:>5.0f} g  ~{st['h']:.1f} h")
    print(f"\nArquivos em {out}/")


if __name__ == '__main__':
    main()
