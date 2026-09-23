#!/usr/bin/env python3
"""
Solidos da base modular: teste de "dentro", malha e volume.

TIPOS DE ELEMENTO (tuplas; o ultimo campo e sempre o grupo)
  ("caixa",  x0, x1, y0, y1, z0, z1, g)
  ("tubo",   xc, yc, z0, z1, r_ext, r_int, g)            eixo Z
  ("prisma", eixo, a0, a1, perfil, g)
        eixo "x": perfil em (y, z), extrudado de x=a0 a x=a1
        eixo "y": perfil em (x, z), extrudado de y=a0 a y=a1
        O perfil tem de ser ESTRELADO a partir do primeiro ponto (a tampa e
        feita em leque a partir dele). Filete: primeiro ponto = o canto.
  ("rr",     x0, x1, y0, y1, z0, z1, raios, t, g)
        retangulo de cantos arredondados extrudado em Z. raios na ordem
        (x0y0, x1y0, x1y1, x0y1). t=None -> macico; t=numero -> casca aberta
        em cima e embaixo, parede t.
  ("casca_tampo", x0, x1, y0, y1, H, R, Rf, t, pele, g)
        placa de cantos R com a aresta de cima arredondada em Rf, oca por
        baixo: saia t, e a face interna acompanha a curva (raio Rf-t, mesmo
        centro). Use pele = t para a casca ter espessura constante.

VOLUME
  As caixas se sobrepoem de proposito (mesa e abas da travessa, por exemplo),
  entao o volume e o da UNIAO. Com curvas no meio, a uniao exata por
  compressao de coordenadas nao serve mais: volume_area() sorteia um ponto em
  cada celula de lado h e conta os que caem dentro de algum elemento.

  ARMADILHA JA PAGA: a primeira versao sorteava UM deslocamento por eixo.
  Parecia estratificado, mas uma pele plana inteira passava a depender das
  mesmas 8 cotas em Z, e o erro CRESCIA ao refinar a grade (+5% no tampo a
  0,3 mm). Sorteio ponto a ponto resolve.

  uniao_caixas() e a conta exata antiga (so caixas e tubos). valida.py
  compara as duas nas partes retas de cada peca: tem de dar < 0,1%.
"""
import math
import numpy as np

SEG_CANTO = 10     # pontos por canto arredondado na malha
SEG_ARCO = 14      # pontos por arco de filete


# =============================================================== contornos ==
def contorno_rr(x0, x1, y0, y1, raios, n=SEG_CANTO):
    """Pontos do retangulo arredondado, anti-horario visto de cima.
    Cada canto recebe n+1 pontos, mesmo com raio ~0: aneis de mesmo tamanho
    podem ser costurados em faixas."""
    r0, r1, r2, r3 = [max(r, 1e-3) for r in raios]
    cs = [((x0 + r0, y0 + r0), r0, math.pi, 1.5 * math.pi),
          ((x1 - r1, y0 + r1), r1, 1.5 * math.pi, 2 * math.pi),
          ((x1 - r2, y1 - r2), r2, 0.0, 0.5 * math.pi),
          ((x0 + r3, y1 - r3), r3, 0.5 * math.pi, math.pi)]
    pts = []
    for (cx, cy), r, a0, a1 in cs:
        for k in range(n + 1):
            a = a0 + (a1 - a0) * k / n
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def perfil_filete(canto, du, dv, R, n=SEG_ARCO):
    """Filete de raio R num canto em L. canto=(u,v); du, dv = +1/-1 dizem para
    que lado ficam as duas paredes. Primeiro ponto = o canto (leque)."""
    u, v = canto
    cu, cv = u + du * R, v + dv * R            # centro do arco
    pts = [(u, v), (cu, v)]
    for k in range(n + 1):
        a = k / n * (math.pi / 2)
        pts.append((cu - du * R * math.sin(a), cv - dv * R * math.cos(a)))
    pts.append((u, cv))
    # remove pontos repetidos nas pontas do arco
    out = [pts[0]]
    for p in pts[1:]:
        if abs(p[0] - out[-1][0]) > 1e-6 or abs(p[1] - out[-1][1]) > 1e-6:
            out.append(p)
    return out


def perfil_lombada(u0, largura, z0, altura, sentido=+1, n=SEG_ARCO * 2):
    """Segmento de circulo: lombada de `largura` na base e `altura` no alto,
    a partir de u0 no sentido dado. Convexo."""
    w, h = largura, altura
    R = (w * w / 4 + h * h) / (2 * h)
    uc, zc = u0 + sentido * w / 2, z0 + h - R
    a = math.asin((w / 2) / R)
    pts = []
    for k in range(n + 1):
        t = -a + 2 * a * k / n
        pts.append((uc + sentido * R * math.sin(t), zc + R * math.cos(t)))
    return pts


# ================================================================ dentro ====
def _dentro_rr(X, Y, x0, x1, y0, y1, raios):
    m = (X >= x0) & (X <= x1) & (Y >= y0) & (Y <= y1)
    r0, r1, r2, r3 = raios
    for (cx, cy, r, sx, sy) in ((x0 + r0, y0 + r0, r0, -1, -1), (x1 - r1, y0 + r1, r1, 1, -1),
                                (x1 - r2, y1 - r2, r2, 1, 1), (x0 + r3, y1 - r3, r3, -1, 1)):
        if r <= 0:
            continue
        q = (sx * (X - cx) > 0) & (sy * (Y - cy) > 0)
        m &= ~(q & ((X - cx) ** 2 + (Y - cy) ** 2 > r * r))
    return m


def _dentro_poligono(U, V, pts):
    dentro = np.zeros(U.shape, dtype=bool)
    n = len(pts)
    for i in range(n):
        u1, v1 = pts[i]
        u2, v2 = pts[(i + 1) % n]
        if v1 == v2:
            continue
        cruza = ((v1 > V) != (v2 > V))
        ui = u1 + (V - v1) * (u2 - u1) / (v2 - v1)
        dentro ^= cruza & (U < ui)
    return dentro


def recuo_filete(R, z0, z):
    """Quanto um contorno recua na altura z por causa de um filete de raio R
    que comeca em z0 (0 abaixo de z0, R em z0+R)."""
    z = np.asarray(z, dtype=float)
    zz = np.clip(z - z0, 0, R)
    return R - np.sqrt(np.maximum(R * R - zz * zz, 0))


def insets_tampo(H, Rf, z):
    """Recuo da face externa do tampo (aresta de cima arredondada em Rf)."""
    return recuo_filete(Rf, H - Rf, z)


def insets_cavidade(H, Rf, t, z):
    """Recuo da face interna: filete CONCENTRICO de raio Rf-t, parede t
    constante na curva (sem isso a aresta curva afinava para 1 mm)."""
    return t + recuo_filete(Rf - t, H - Rf, z)


def caixa_limite(e):
    k = e[0]
    if k == "caixa":
        return e[1], e[2], e[3], e[4], e[5], e[6]
    if k == "tubo":
        _, xc, yc, z0, z1, re, ri, _ = e
        return xc - re, xc + re, yc - re, yc + re, z0, z1
    if k == "prisma":
        _, eixo, a0, a1, pf, _ = e
        us = [p[0] for p in pf]
        vs = [p[1] for p in pf]
        if eixo == "x":
            return a0, a1, min(us), max(us), min(vs), max(vs)
        return min(us), max(us), a0, a1, min(vs), max(vs)
    if k == "rr":
        return e[1], e[2], e[3], e[4], e[5], e[6]
    if k == "casca_tampo":
        return e[1], e[2], e[3], e[4], 0.0, e[5]
    raise ValueError(k)


def dentro(e, X, Y, Z):
    k = e[0]
    if k == "caixa":
        return (X >= e[1]) & (X <= e[2]) & (Y >= e[3]) & (Y <= e[4]) & (Z >= e[5]) & (Z <= e[6])
    if k == "tubo":
        _, xc, yc, z0, z1, re, ri, _ = e
        d2 = (X - xc) ** 2 + (Y - yc) ** 2
        return (d2 <= re * re) & (d2 >= ri * ri) & (Z >= z0) & (Z <= z1)
    if k == "prisma":
        _, eixo, a0, a1, pf, _ = e
        if eixo == "x":
            return (X >= a0) & (X <= a1) & _dentro_poligono(Y, Z, pf)
        return (Y >= a0) & (Y <= a1) & _dentro_poligono(X, Z, pf)
    if k == "rr":
        _, x0, x1, y0, y1, z0, z1, raios, t, _ = e
        m = (Z >= z0) & (Z <= z1) & _dentro_rr(X, Y, x0, x1, y0, y1, raios)
        if t is not None:
            ri = [max(r - t, 0) for r in raios]
            m &= ~_dentro_rr(X, Y, x0 + t, x1 - t, y0 + t, y1 - t, ri)
        return m
    if k == "casca_tampo":
        _, x0, x1, y0, y1, H, R, Rf, t, pele, _ = e
        d = insets_tampo(H, Rf, Z)
        fora = (Z >= 0) & (Z <= H) & _dentro_rr_var(X, Y, x0, x1, y0, y1, R, d)
        dc = insets_cavidade(H, Rf, t, Z)
        oco = (Z < H - pele) & _dentro_rr_var(X, Y, x0, x1, y0, y1, R, dc)
        return fora & ~oco
    raise ValueError(k)


def _dentro_rr_var(X, Y, x0, x1, y0, y1, R, d):
    """Retangulo arredondado com recuo d (array, varia com z)."""
    m = (X >= x0 + d) & (X <= x1 - d) & (Y >= y0 + d) & (Y <= y1 - d)
    r = np.maximum(R - d, 0)
    for cx, cy, sx, sy in ((x0 + R, y0 + R, -1, -1), (x1 - R, y0 + R, 1, -1),
                           (x1 - R, y1 - R, 1, 1), (x0 + R, y1 - R, -1, 1)):
        q = (sx * (X - cx) > 0) & (sy * (Y - cy) > 0)
        m &= ~(q & ((X - cx) ** 2 + (Y - cy) ** 2 > r * r))
    return m


# ================================================================ volume ====
def volume_area(elems, h=0.4, semente=7, so_x_positivo=True):
    """Volume da uniao (mm3) e area projetada (mm2) por amostragem.

    Um ponto sorteado dentro de cada celula de lado h (estratificado: sem
    vies, e o erro de uma pele plana nao depende de meia duzia de cotas em Z,
    que foi o que um deslocamento so por eixo fazia). A area projetada usa
    um ponto sorteado por coluna (x, y).
    so_x_positivo: a peca e simetrica em X; amostra x>=0 e dobra."""
    rng = np.random.default_rng(semente)
    bb = np.array([caixa_limite(e) for e in elems])
    xmin = 0.0 if so_x_positivo else bb[:, 0].min()
    xmax, ymin, ymax = bb[:, 1].max(), bb[:, 2].min(), bb[:, 3].max()
    zmin, zmax = bb[:, 4].min(), bb[:, 5].max()
    nx = int(math.ceil((xmax - xmin) / h))
    ny = int(math.ceil((ymax - ymin) / h))
    nz = int(math.ceil((zmax - zmin) / h))
    conta = 0
    passo = max(1, int(4e6 // (nx * ny)))
    ii = np.arange(nx, dtype=np.float32)[:, None, None]
    jj = np.arange(ny, dtype=np.float32)[None, :, None]
    for k0 in range(0, nz, passo):
        k1 = min(nz, k0 + passo)
        kk = np.arange(k0, k1, dtype=np.float32)[None, None, :]
        sh = (nx, ny, k1 - k0)
        X = xmin + (ii + rng.random(sh, dtype=np.float32)) * h
        Y = ymin + (jj + rng.random(sh, dtype=np.float32)) * h
        Z = zmin + (kk + rng.random(sh, dtype=np.float32)) * h
        za, zb = zmin + k0 * h, zmin + k1 * h
        cheio = np.zeros(sh, dtype=bool)
        for e, (a0, a1, b0, b1, c0, c1) in zip(elems, bb):
            if c1 < za or c0 > zb or a1 < xmin:
                continue
            i0, i1 = max(0, int((a0 - xmin) // h)), min(nx, int((a1 - xmin) // h) + 1)
            j0, j1 = max(0, int((b0 - ymin) // h)), min(ny, int((b1 - ymin) // h) + 1)
            q0, q1 = max(0, int((c0 - za) // h)), min(k1 - k0, int((c1 - za) // h) + 1)
            if i1 <= i0 or j1 <= j0 or q1 <= q0:
                continue
            s_ = (slice(i0, i1), slice(j0, j1), slice(q0, q1))
            cheio[s_] |= dentro(e, X[s_], Y[s_], Z[s_])
        conta += int(cheio.sum())
    # area projetada: um ponto por coluna, testado contra a sombra de cada elemento
    X2 = xmin + (np.arange(nx)[:, None] + rng.random((nx, ny))) * h
    Y2 = ymin + (np.arange(ny)[None, :] + rng.random((nx, ny))) * h
    sombra = np.zeros((nx, ny), dtype=bool)
    for e in elems:
        sombra |= _sombra(e, X2, Y2)
    f = 2.0 if so_x_positivo else 1.0
    return conta * h ** 3 * f, int(sombra.sum()) * h * h * f


def _sombra(e, X, Y):
    """Projecao do elemento no plano XY."""
    k = e[0]
    if k in ("caixa", "rr") or k == "casca_tampo":
        x0, x1, y0, y1 = e[1:5]
        if k == "caixa":
            return (X >= x0) & (X <= x1) & (Y >= y0) & (Y <= y1)
        raios = e[7] if k == "rr" else [e[6]] * 4
        return _dentro_rr(X, Y, x0, x1, y0, y1, raios)
    if k == "tubo":
        _, xc, yc, z0, z1, re, ri, _ = e
        d2 = (X - xc) ** 2 + (Y - yc) ** 2
        return (d2 <= re * re) & (d2 >= ri * ri)
    if k == "prisma":
        a0, a1, b0, b1 = caixa_limite(e)[:4]
        return (X >= a0) & (X <= a1) & (Y >= b0) & (Y <= b1)
    raise ValueError(k)


# ======================================================= uniao exata =======
def _cortes(vals):
    return sorted(set(round(v, 4) for v in vals))


def uniao_caixas(elems):
    """Volume EXATO da uniao de caixas (varredura em Z com compressao em XY)
    + tubos analiticos (tubos nao se sobrepoem a caixas). Referencia para
    validar volume_area()."""
    caixas = [e for e in elems if e[0] == "caixa"]
    tubos = [e for e in elems if e[0] == "tubo"]
    xs = _cortes([c[1] for c in caixas] + [c[2] for c in caixas])
    ys = _cortes([c[3] for c in caixas] + [c[4] for c in caixas])
    zs = _cortes([c[5] for c in caixas] + [c[6] for c in caixas])
    ix = {v: i for i, v in enumerate(xs)}
    iy = {v: i for i, v in enumerate(ys)}
    dx = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    dy = [ys[j + 1] - ys[j] for j in range(len(ys) - 1)]
    vol = 0.0
    for k in range(len(zs) - 1):
        za, zb = zs[k], zs[k + 1]
        zm = (za + zb) / 2
        grade = [bytearray(len(dy)) for _ in dx]
        for c in caixas:
            if c[5] < zm < c[6]:
                a, b = iy[round(c[3], 4)], iy[round(c[4], 4)]
                for i in range(ix[round(c[1], 4)], ix[round(c[2], 4)]):
                    grade[i][a:b] = b"\x01" * (b - a)
        area = 0.0
        for i, row in enumerate(grade):
            if any(row):
                area += dx[i] * sum(dy[j] for j in range(len(row)) if row[j])
        vol += area * (zb - za)
    for t in tubos:
        _, xc, yc, z0, z1, re, ri, _ = t
        vol += math.pi * (re * re - ri * ri) * (z1 - z0)
    return vol


# ================================================================= malha ====
def _quad(t, a, b, c, d):
    t.append((a, b, c))
    t.append((a, c, d))


def _vol_assinado(tris):
    v = 0.0
    for a, b, c in tris:
        v += (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) +
              a[2] * (b[0] * c[1] - b[1] * c[0]))
    return v / 6.0


def _faixa(t, A, B):
    """Costura dois aneis fechados de mesmo tamanho."""
    n = len(A)
    for i in range(n):
        j = (i + 1) % n
        _quad(t, A[i], A[j], B[j], B[i])


def _leque(t, anel, inverte=False):
    c = tuple(sum(p[i] for p in anel) / len(anel) for i in range(3))
    n = len(anel)
    for i in range(n):
        a, b = anel[i], anel[(i + 1) % n]
        t.append((c, b, a) if inverte else (c, a, b))


def malha(e, seg_tubo=24):
    """Triangulos de um elemento, orientados para fora (confere pelo volume
    assinado e inverte se preciso - cada elemento e fechado)."""
    k = e[0]
    t = []
    if k == "caixa":
        x0, x1, y0, y1, z0, z1 = e[1:7]
        v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
             (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        for a, b, c, d in [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (1, 2, 6, 5), (3, 0, 4, 7)]:
            _quad(t, v[a], v[b], v[c], v[d])
    elif k == "tubo":
        _, xc, yc, z0, z1, re, ri, _ = e
        n = seg_tubo
        E0 = [(xc + re * math.cos(2 * math.pi * i / n), yc + re * math.sin(2 * math.pi * i / n), z0) for i in range(n)]
        E1 = [(p[0], p[1], z1) for p in E0]
        I0 = [(xc + ri * math.cos(2 * math.pi * i / n), yc + ri * math.sin(2 * math.pi * i / n), z0) for i in range(n)]
        I1 = [(p[0], p[1], z1) for p in I0]
        _faixa(t, E0, E1)
        _faixa(t, I1, I0)
        _faixa(t, E1, I1)
        _faixa(t, I0, E0)
    elif k == "prisma":
        _, eixo, a0, a1, pf, _ = e
        if eixo == "x":
            P0 = [(a0, u, v) for u, v in pf]
            P1 = [(a1, u, v) for u, v in pf]
        else:
            P0 = [(u, a0, v) for u, v in pf]
            P1 = [(u, a1, v) for u, v in pf]
        n = len(pf)
        for i in range(1, n - 1):                       # tampas em leque
            t.append((P0[0], P0[i + 1], P0[i]))
            t.append((P1[0], P1[i], P1[i + 1]))
        _faixa(t, P0, P1)
    elif k == "rr":
        _, x0, x1, y0, y1, z0, z1, raios, esp, _ = e
        c = contorno_rr(x0, x1, y0, y1, raios)
        A0 = [(x, y, z0) for x, y in c]
        A1 = [(x, y, z1) for x, y in c]
        _faixa(t, A0, A1)
        if esp is None:
            _leque(t, A1)
            _leque(t, A0, inverte=True)
        else:
            ri = [max(r - esp, 1e-3) for r in raios]
            ci = contorno_rr(x0 + esp, x1 - esp, y0 + esp, y1 - esp, ri)
            B0 = [(x, y, z0) for x, y in ci]
            B1 = [(x, y, z1) for x, y in ci]
            _faixa(t, B1, B0)
            _faixa(t, A1, B1)
            _faixa(t, B0, A0)
    elif k == "casca_tampo":
        _, x0, x1, y0, y1, H, R, Rf, esp, pele, _ = e
        zs = [0.0, H - Rf] + [H - Rf + Rf * math.sin(math.pi / 2 * i / 8) for i in range(1, 9)]
        aneis = []
        for z in zs:
            d = float(insets_tampo(H, Rf, z))
            c = contorno_rr(x0 + d, x1 - d, y0 + d, y1 - d, [max(R - d, 1e-3)] * 4)
            aneis.append([(x, y, z) for x, y in c])
        for i in range(len(aneis) - 1):
            _faixa(t, aneis[i], aneis[i + 1])
        _leque(t, aneis[-1])
        zc = [0.0, H - Rf] + [H - Rf + (Rf - esp) * math.sin(math.pi / 2 * i / 8) for i in range(1, 9)]
        zc = [z for z in zc if z <= H - pele + 1e-9]
        if zc[-1] < H - pele - 1e-6:
            zc.append(H - pele)
        cav = []
        for z in zc:
            d = float(insets_cavidade(H, Rf, esp, z))
            c = contorno_rr(x0 + d, x1 - d, y0 + d, y1 - d, [max(R - d, 1e-3)] * 4)
            cav.append([(x, y, z) for x, y in c])
        for i in range(len(cav) - 1):
            _faixa(t, cav[i + 1], cav[i])
        _faixa(t, cav[0], aneis[0])
        _leque(t, cav[-1], inverte=True)
    else:
        raise ValueError(k)
    if _vol_assinado(t) < 0:
        t = [(a, c, b) for a, b, c in t]
    return t


def normais_suaves(tris, vinco_graus=35.0):
    """Normal por vertice, media das faces vizinhas dentro do angulo de vinco.
    Curva fica lisa; aresta de caixa continua viva."""
    T = np.array(tris, dtype=np.float64)                 # (n,3,3)
    fn = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])  # peso = 2x area
    nrm = np.linalg.norm(fn, axis=1, keepdims=True)
    fu = fn / np.where(nrm == 0, 1, nrm)
    chave = np.round(T.reshape(-1, 3) * 1000).astype(np.int64)
    _, idx = np.unique(chave, axis=0, return_inverse=True)
    idx = idx.reshape(-1)
    face_de = np.repeat(np.arange(len(T)), 3)
    grupos = {}
    for v, f in zip(idx.tolist(), face_de.tolist()):
        grupos.setdefault(v, []).append(f)
    cosv = math.cos(math.radians(vinco_graus))
    out = np.zeros((len(T) * 3, 3))
    for p, (v, f) in enumerate(zip(idx.tolist(), face_de.tolist())):
        viz = grupos[v]
        s = np.zeros(3)
        for g in viz:
            if fu[g] @ fu[f] >= cosv:
                s += fn[g]
        m = np.linalg.norm(s)
        out[p] = s / m if m > 0 else fu[f]
    return out
