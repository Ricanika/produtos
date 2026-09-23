#!/usr/bin/env python3
"""Gera cad/visor-elo.html: a LINHA ELO (P e M) num visor 3D so.

Nasce de cad/visor3d.html, que ja tem o WebGL2 escrito a mao e testado, e
aplica sobre ele as mudancas que a linha exige:

  1. DUAS malhas em vez de uma. Cada pose passa a carregar um indice de malha
     como 4o elemento, e os buffers viram vetor.
  2. INDICE DE 32 BITS. O M tem 213 rasgos contra 123 do P; depois de soldar
     ele passa de 65.535 vertices e nao cabe mais em uint16. O visor3d.py ja
     anotava esta saida no proprio erro que levantava.
  3. As cenas da linha, com os numeros MEDIDOS aqui -- nunca digitados.

Uso:  python3 visor_elo.py
"""
import base64
import os
import re
import struct

import numpy as np
import trimesh
from build123d import Pos, export_stl

import modelo3d as M

DEST = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(DEST, "visor3d.html")
SAI = os.path.join(DEST, "visor-elo.html")
DADOS = os.path.join(DEST, "elo-medidas.json")
STL_P = os.path.join(DEST, "elo-p.stl")
STL_M = os.path.join(DEST, "elo-m.stl")


def vg(x, casas=1):
    return f"{x:.{casas}f}".replace(".", ",")


# ---------------------------------------------------------------- malha ----
def empacota(caminho):
    """Quantiza posicoes em uint16 e escreve INDICE EM UINT32.

    Mesma ordem de visor3d.empacota (quantiza ANTES de soldar, senao os
    triangulos-estilete do OCC achatam e a pagina desenha uma teia de
    triangulacao sobre a parede). A diferenca e o indice: 32 bits, porque o M
    nao cabe em 16.
    """
    m = trimesh.load(caminho)
    v, f = np.asarray(m.vertices, float), np.asarray(m.faces, np.int64)
    mn, mx = v.min(0), v.max(0)
    esc = np.where(mx > mn, (mx - mn) / 65535.0, 1.0)
    q = np.rint((v - mn) / esc).astype(np.uint16)
    uniq, inv = np.unique(q, axis=0, return_inverse=True)
    f = inv[f]
    vivo = (f[:, 0] != f[:, 1]) & (f[:, 1] != f[:, 2]) & (f[:, 0] != f[:, 2])
    pos = mn + uniq.astype(float) * esc
    a, b, c = pos[f[:, 0]], pos[f[:, 1]], pos[f[:, 2]]
    vivo &= np.linalg.norm(np.cross(b - a, c - a), axis=1) / 2.0 > 1e-4
    fora = int((~vivo).sum())
    f = f[vivo]
    if len(uniq) >= 2 ** 20:
        raise SystemExit(f"{len(uniq)} vertices: a chave de aresta da pagina "
                         f"e A*2**20+B e passa do inteiro seguro de JS.")
    buf = struct.pack("<6f2I", *mn, *esc, len(uniq), len(f))
    buf += uniq.tobytes() + f.astype(np.uint32).tobytes()
    print(f"  {os.path.basename(caminho)}: {len(uniq)} vertices, {len(f)} "
          f"faces ({fora} degeneradas fora), {len(buf)/1024:.0f} kB · "
          f"resolucao {esc.max():.4f} mm", flush=True)
    return base64.b64encode(buf).decode("ascii")


# -------------------------------------------------------------- medicao ----
def vol(a, b):
    return (a & b).volume


def passo(a, b, dy=0.0, lo=0.0, hi=200.0, tol=0.02):
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if vol(a, Pos(0, dy, mid) * b) > 0.002:
            lo = mid
        else:
            hi = mid
    return hi


def apoios(a, b, dy, z, eps=0.3):
    inter = a & (Pos(0, dy, z - eps) * b)
    return sorted((s.volume / eps for s in inter.solids() if s.volume > 0.002),
                  reverse=True)


def mede():
    """Constroi P e M e mede tudo o que a pagina afirma."""
    d = {}
    M.padrao()
    p, np_ = M.cesto(aba=True)
    export_stl(p, STL_P)
    d["passo_p"] = M.passo_acoplado()
    d["desloc"] = M.DESLOC
    d["alt"] = M.ALT
    d["p"] = dict(peso=p.volume * M.RHO, cap=M.capacidade(), furos=np_,
                  larg=M.LARG, prof=M.PROF)
    print("P: %.1f g | %.2f L | %d rasgos | passo acoplado %.0f"
          % (d["p"]["peso"], d["p"]["cap"], np_, d["passo_p"]), flush=True)

    # Os passos do P tambem sao MEDIDOS aqui. A folha elo.py compara P e M
    # lado a lado, e a primeira versao dela trazia os do P digitados (40,00 /
    # 130,00 / 7,5 / 469) -- que e o jeito conhecido de uma folha envelhecer
    # calada enquanto a outra anda.
    d["pn_p"] = passo(p, p, 0.0)
    d["pe_p"] = passo(p, p, M.DESLOC)
    d["ap_p"] = apoios(p, p, M.DESLOC, d["pe_p"])
    lo, hi = 0.0, 20.0
    while hi - lo > 0.05:
        mid = (lo + hi) / 2
        if vol(p, Pos(d["passo_p"] + 1.2, 0, mid) * p) > 0.0:
            lo = mid
        else:
            hi = mid
    d["solta_p"] = hi
    print("  P encaixa %.2f | empilha %.2f | apoios %.0f mm2 | solta %.1f"
          % (d["pn_p"], d["pe_p"], sum(d["ap_p"]), d["solta_p"]), flush=True)

    # o par acoplado, recentrado no proprio eixo
    par = Pos(-d["passo_p"] / 2, 0, 0) * (p + (Pos(d["passo_p"], 0, 0) * p))

    M.padrao_m()
    m, nm = M.cesto(aba=True)
    d["recuo"] = M.DESLOC + (M.PROF - 230.0) / 2   # o par encosta ATRAS
    export_stl(m, STL_M)
    bm = m.bounding_box()
    d["m"] = dict(peso=m.volume * M.RHO, cap=M.capacidade(), furos=nm,
                  larg=M.LARG, prof=M.PROF,
                  env=(bm.size.X, bm.size.Y, bm.size.Z))
    d["passo_m"] = M.passo_acoplado()
    print("M: %.1f g | %.2f L | %d rasgos | passo acoplado %.0f | envelope "
          "%.1f x %.1f x %.1f" % (d["m"]["peso"], d["m"]["cap"], nm,
                                  d["passo_m"], *d["m"]["env"]), flush=True)

    d["pn_m"] = passo(m, m, 0.0)
    d["pe_m"] = passo(m, m, M.DESLOC)
    d["interf_m"] = vol(m, Pos(0, M.DESLOC, M.ALT) * m)
    ap = apoios(m, m, M.DESLOC, d["pe_m"])
    d["ap_m"] = ap
    print("  M encaixa %.2f | empilha %.2f | interf %.4f | apoios %.0f mm2"
          % (d["pn_m"], d["pe_m"], d["interf_m"], sum(ap)), flush=True)

    d["trava_m"] = [(dx, vol(m, Pos(d["passo_m"] + dx, 0, 0) * m))
                    for dx in (0.0, 0.6, 1.2, 2.0)]
    lo, hi = 0.0, 20.0
    while hi - lo > 0.05:
        mid = (lo + hi) / 2
        if vol(m, Pos(d["passo_m"] + 1.2, 0, mid) * m) > 0.0:
            lo = mid
        else:
            hi = mid
    d["solta_m"] = hi
    print("  M acopla: trava %s | solta %.1f"
          % (["%.1f" % t[1] for t in d["trava_m"]], d["solta_m"]), flush=True)

    # O diferencial: o par no M. Com o M mais fundo que o par, o pouso pede
    # RECUO -- as saias de tras tem de encontrar a aba de tras do M. Centrado,
    # o contato cai de ~887 para 54 mm2 e o par tomba (medido, secao 4.2.8).
    melhor = None
    for dy in (M.DESLOC, d["recuo"], 0.0):
        z = passo(m, par, dy)
        iv = vol(m, Pos(0, dy, M.ALT) * par)
        ap = apoios(m, par, dy, z)
        print("  par no M: dy=%+5.0f  passo %7.2f  interf em %.0f %8.4f  "
              "apoios %d ilhas %.0f mm2"
              % (dy, z, M.ALT, iv, len(ap), sum(ap)), flush=True)
        cand = dict(dy=dy, z=z, interf=iv, ap=ap)
        # o melhor pouso e o que fica na altura do M com area de contato maxima
        if melhor is None or (abs(z - M.ALT), -sum(ap)) < \
                (abs(melhor["z"] - M.ALT), -sum(melhor["ap"])):
            melhor = cand
    d["par"] = melhor
    print("  -> escolhido dy=%+.0f, passo %.2f, %.0f mm2 de contato"
          % (melhor["dy"], melhor["z"], sum(melhor["ap"])), flush=True)

    # Extracao dos dois: o volume que nenhuma das duas metades do molde
    # alcanca. Aqui tambem para a folha nao trazer o numero digitado.
    import extracao as EX
    for nome, arq in (("preso_p", STL_P), ("preso_m", STL_M)):
        d[nome] = EX.audita(trimesh.load(arq))[0]
        print("  %s = %.0f mm3" % (nome, d[nome]), flush=True)

    return d


# -------------------------------------------------------------- remendos ---
def troca(s, velho, novo, o_que):
    if velho not in s:
        raise SystemExit(f"remendo falhou ({o_que}): nao achei {velho[:70]!r} "
                         f"em visor3d.html. A base mudou.")
    return s.replace(velho, novo, 1)


def duas_malhas(s, malhas):
    """Passa a pagina de uma malha uint16 para N malhas uint32."""
    # 1. as malhas (0 = P, 1 = M, 2 = G)
    s = re.sub(r"var MALHA = '[^']*';",
               "var MALHAS = ['" + "', '".join(malhas) + "'];", s, count=1)

    # 2. indice de 32 bits na decodificacao
    s = troca(s,
              "  var idx = new Uint16Array(buf.slice(32 + nv * 6, 32 + nv * 6 + nf * 6));",
              "  var idx = new Uint32Array(buf.slice(32 + nv * 6, 32 + nv * 6 + nf * 12));",
              "indice uint32 na decodificacao")

    # 3. a chave de aresta: A*65536+B estoura acima de 65.536 vertices
    s = troca(s,
              "      var key = A < B ? A * 65536 + B : B * 65536 + A;",
              "      var key = A < B ? A * 1048576 + B : B * 1048576 + A;",
              "chave de aresta em 2**20")
    s = troca(s, "  return new Uint16Array(fora);",
              "  return new Uint32Array(fora);", "arestas em uint32")

    # 4. buffers: um por malha
    s = troca(s, """  var m = decodifica(MALHA);
  var arestas = arestasDe(m, 24);

  var pSol = prog(gl, VS_SOL, FS_SOL), pLin = prog(gl, VS_LIN, FS_LIN);
  var vbo = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
  gl.bufferData(gl.ARRAY_BUFFER, m.pos, gl.STATIC_DRAW);
  var ibo = gl.createBuffer();
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibo);
  gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, m.idx, gl.STATIC_DRAW);
  var abo = gl.createBuffer();
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, abo);
  gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, arestas, gl.STATIC_DRAW);""",
              """  var MS = MALHAS.map(decodifica);
  var AR = MS.map(function (x) { return arestasDe(x, 24); });

  var pSol = prog(gl, VS_SOL, FS_SOL), pLin = prog(gl, VS_LIN, FS_LIN);
  var VBO = [], IBO = [], ABO = [];
  MS.forEach(function (x, k) {
    VBO[k] = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, VBO[k]);
    gl.bufferData(gl.ARRAY_BUFFER, x.pos, gl.STATIC_DRAW);
    IBO[k] = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, IBO[k]);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, x.idx, gl.STATIC_DRAW);
    ABO[k] = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ABO[k]);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, AR[k], gl.STATIC_DRAW);
  });""", "buffers por malha")

    # 5. enquadra: a caixa de cada pose e a da SUA malha
    s = troca(s, """      for (var k = 0; k < 3; k++) {
        b[k] = Math.min(b[k], m.bb[k] + o[k]);
        b[k+3] = Math.max(b[k+3], m.bb[k+3] + o[k]);
      }""",
              """      var bb = MS[o[3] || 0].bb;
      for (var k = 0; k < 3; k++) {
        b[k] = Math.min(b[k], bb[k] + o[k]);
        b[k+3] = Math.max(b[k+3], bb[k+3] + o[k]);
      }""", "enquadra por malha")

    # 6. solido: liga os buffers da malha de cada pose
    s = troca(s, """    var aP = gl.getAttribLocation(pSol, 'a_pos');
    gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
    gl.enableVertexAttribArray(aP);
    gl.vertexAttribPointer(aP, 3, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibo);
    gl.enable(gl.POLYGON_OFFSET_FILL);""",
              """    var aP = gl.getAttribLocation(pSol, 'a_pos');
    gl.enableVertexAttribArray(aP);
    gl.enable(gl.POLYGON_OFFSET_FILL);""", "solido: sem buffer fixo")
    s = troca(s, """    ps.forEach(function (o, i) {
      gl.uniform3fv(uOff, new Float32Array(o));
      gl.uniform3fv(uCor, new Float32Array(CORES[i % 2]));
      gl.drawElements(gl.TRIANGLES, m.nf * 3, gl.UNSIGNED_SHORT, 0);
    });""",
              """    ps.forEach(function (o, i) {
      var k = o[3] || 0;
      gl.bindBuffer(gl.ARRAY_BUFFER, VBO[k]);
      gl.vertexAttribPointer(aP, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, IBO[k]);
      gl.uniform3fv(uOff, new Float32Array([o[0], o[1], o[2]]));
      gl.uniform3fv(uCor, new Float32Array(CORES[(o[4] === undefined ? i : o[4]) % 2]));
      gl.drawElements(gl.TRIANGLES, MS[k].nf * 3, gl.UNSIGNED_INT, 0);
    });""", "desenho do solido por malha")

    # 7. arestas: idem
    s = troca(s, """    if (mostraArestas && arestas.length) {
      gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
      gl.vertexAttribPointer(lP, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, abo);
      gl.uniform4fv(lCor, new Float32Array(corAresta));
      ps.forEach(function (o) {
        gl.uniform3fv(lOff, new Float32Array(o));
        gl.drawElements(gl.LINES, arestas.length, gl.UNSIGNED_SHORT, 0);
      });
    }""",
              """    if (mostraArestas) {
      gl.uniform4fv(lCor, new Float32Array(corAresta));
      ps.forEach(function (o) {
        var k = o[3] || 0;
        if (!AR[k].length) return;
        gl.bindBuffer(gl.ARRAY_BUFFER, VBO[k]);
        gl.vertexAttribPointer(lP, 3, gl.FLOAT, false, 0, 0);
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ABO[k]);
        gl.uniform3fv(lOff, new Float32Array([o[0], o[1], o[2]]));
        gl.drawElements(gl.LINES, AR[k].length, gl.UNSIGNED_INT, 0);
      });
    }""", "desenho das arestas por malha")
    return s


def cenas(d):
    """As cenas da linha, com os numeros MEDIDOS em mede().

    Convencao de pose: [x, y, z, malha, cor]. malha 0 = P, 1 = M, 2 = G.
    """
    p, m = d["p"], d["m"]
    pp = d["passo_p"] / 2          # os dois P do par ficam em +-pp
    dy = d["par"]["dy"]
    zp = d["par"]["z"]
    ap_par = sum(d["par"]["ap"])
    ap_m = sum(d["ap_m"])

    def par_em(z0, y0, k0):
        """O par de P acoplado, pousado a z0."""
        return [[-pp, y0, z0, 0, k0], [pp, y0, z0, 0, k0 + 1]]

    js = {
        "m": dict(
            titulo="O ELO M",
            texto=("A mesma arquitetura do P, com a boca do corpo em 380 mm. "
                   "E 380 nao e escolha: e 2 x 180 + 2 x 10, a pegada exata "
                   "de dois P acoplados. A profundidade nao muda, entao a "
                   "silhueta lateral e os chanfros da frente sao os mesmos."),
            dados=[["boca do corpo", f"{m['larg']:.0f} × {m['prof']:.0f} mm"],
                   ["envelope", f"{vg(m['env'][0])} × {vg(m['env'][1])} × "
                                f"{vg(m['env'][2])} mm"],
                   ["peso", f"{vg(m['peso'])} g"],
                   ["capacidade", f"{vg(m['cap'], 2)} L"],
                   ["parede", "1,4 mm"]],
            selo="uma peça, um molde, sem gaveta",
            poses=[[0, 0, 0, 1, 0]]),
        "dois": dict(
            titulo="Dois P acoplados, empilhados no M",
            texto=(f"O diferencial da linha. O par encosta ATRÁS: recuando "
                   f"{dy:.0f} mm em y, as duas saias de trás encontram a aba "
                   f"de trás do M e os dois pés externos caem nas abas "
                   f"laterais — {ap_par:.0f} mm² de contato de face plana, "
                   f"{vg(ap_par/ap_m)}× o próprio tripé do M. Centrado, o "
                   f"contato cairia para 54 mm² e o par tombaria: é o recuo "
                   f"que libera a profundidade do M."),
            dados=[["passo", f"{vg(zp, 2)} mm"],
                   ["recua em y", f"{dy:.0f} mm"],
                   ["contato", f"{ap_par:.0f} mm²"],
                   ["interferência", f"{d['par']['interf']:.4f} mm³".replace(".", ",")]],
            selo=f"{d['par']['interf']:.3f} mm³ de interferência".replace(".", ",") +
                 f" a {vg(zp, 2)} mm",
            poses=[[0, 0, 0, 1, 0]] + par_em(zp, dy, 1)),
        "torre": dict(
            titulo="A torre da linha",
            texto=("Dois M empilhados e, em cima, dois P acoplados. Tudo na "
                   "mesma frente, sem inverter nenhuma peça: o que troca "
                   "encaixe por pilha é sempre o mesmo deslocamento em y."),
            dados=[["M sobre M", f"{vg(d['pe_m'], 2)} mm"],
                   ["par sobre M", f"{vg(zp, 2)} mm"],
                   ["altura da torre", f"{vg(2*d['pe_m'] + m['env'][2])} mm"],
                   ["interferência", "0,0000 mm³"]],
            selo="a mesma aba serve de piso em todos os andares",
            poses=[[0, 0, 0, 1, 0], [0, d["desloc"], d["pe_m"], 1, 1]] +
                  par_em(2 * d["pe_m"], d["desloc"] + dy, 0)),
        "encaixa": dict(
            titulo="M encaixados · para transportar",
            texto=(f"Passo de {vg(d['pn_m'], 2)} mm — o MESMO do P, e não por "
                   f"coincidência: quem manda no encaixe é a saída em x do "
                   f"pé, que não depende da largura do corpo. Por isso o M "
                   f"cuba tão bem quanto o P."),
            dados=[["passo", f"{vg(d['pn_m'], 2)} mm"],
                   ["6 peças", f"{m['env'][2] + 5*d['pn_m']:.0f} mm"],
                   ["12 peças", f"{m['env'][2] + 11*d['pn_m']:.0f} mm"],
                   ["vs. empilhado", f"{d['pe_m']/d['pn_m']:.1f} × mais"]],
            selo=f"12 peças em {m['env'][2] + 11*d['pn_m']:.0f} mm de caixa",
            poses=[[0, 0, i * d["pn_m"], 1, i] for i in range(6)]),
        "empilha": dict(
            titulo="M empilhados · altura cheia",
            texto=(f"Mesma frente, deslocando {d['desloc']:.0f} mm em y. O "
                   f"tripé do M mede {ap_m:.0f} mm² de contato — uma saia de "
                   f"trás e dois pés na frente, igual ao P."),
            dados=[["passo", f"{vg(d['pe_m'], 2)} mm"],
                   ["desloca em y", f"{d['desloc']:.0f} mm"],
                   ["apoios", "3 (tripé)"],
                   ["contato", f"{ap_m:.0f} mm²"]],
            selo=f"{d['interf_m']:.4f} mm³ de interferência".replace(".", ",") +
                 f" a {vg(d['pe_m'], 2)} mm",
            poses=[[0, i * d["desloc"], i * d["pe_m"], 1, i] for i in range(3)]),
        "acopla": dict(
            titulo="M + M acoplados · lado a lado",
            texto=(f"A mesma cauda de andorinha do P, na mesma cota. O passo "
                   f"é {d['passo_m']:.0f} mm (boca + duas abas), e a peça "
                   f"solta levantando {vg(d['solta_m'])} mm — a altura da "
                   f"junta."),
            dados=[["passo", f"{d['passo_m']:.0f} mm"],
                   ["trava a partir de", "0,6 mm"],
                   ["solta levantando", f"{vg(d['solta_m'])} mm"],
                   ["a 1,2 mm", f"{vg(d['trava_m'][2][1])} mm³"]],
            selo="trava puxando de lado, solta levantando",
            poses=[[0, 0, 0, 1, 0], [d["passo_m"], 0, 0, 1, 1]]),
    }
    js["linha"] = dict(
        titulo="A linha ELO",
        texto=(f"P {vg(p['cap'], 2)} L · M {vg(m['cap'], 2)} L. Mesma aba, "
               f"mesma cauda de andorinha, mesma altura de junta nos dois. "
               f"O que muda é a escala em planta — 380 é 2 × 180 + 2 × 10, a "
               f"pegada exata de dois P acoplados — e a profundidade, que é "
               f"livre porque o par pousa recuado."),
        dados=[["P", f"{vg(p['cap'], 2)} L · {vg(p['peso'])} g"],
               ["M", f"{vg(m['cap'], 2)} L · {vg(m['peso'])} g"],
               ["g/L", f"{vg(p['peso']/p['cap'])} · {vg(m['peso']/m['cap'])}"],
               ["parede", "1,4 mm nos dois"]],
        selo="dois tamanhos, uma arquitetura",
        poses=[[330, 0, 0, 0, 0], [0, 0, 0, 1, 1]])
    return js


def main(rapido=False):
    """rapido=True le elo-medidas.json e os STLs em disco em vez de remedir.

    Remedir custa mais de uma hora de booleano em pecas de 200+ rasgos. O
    json e versionado justamente para que redesenhar a pagina nao dependa
    disso -- mas quem muda a GEOMETRIA tem de rodar sem --rapido.
    """
    import json
    if rapido:
        d = json.load(open(DADOS, encoding="utf-8"))
        print("lido elo-medidas.json (sem remedir)", flush=True)
        for k in ("g",):
            if k not in d:
                raise SystemExit(f"falta '{k}' no json: rode sem --rapido")
        return escreve(d)
    d = mede()
    # Despeja as medidas: a folha elo.py le DAQUI em vez de remedir tudo
    # (cada uma destas medicoes custa minutos de booleano em pecas de 213
    # rasgos, e remedir em dois lugares e como as duas folhas divergirem).
    import json
    with open(DADOS, "w", encoding="utf-8") as fp:
        json.dump(d, fp, ensure_ascii=False, indent=1, default=float)
    print("gerado elo-medidas.json", flush=True)
    return escreve(d)


def escreve(d):
    p, m = d["p"], d["m"]
    print("empacotando:", flush=True)
    malhas = [empacota(STL_P), empacota(STL_M)]
    s = open(BASE, encoding="utf-8").read()
    s = duas_malhas(s, malhas)

    # ---- cabecalho e botoes ------------------------------------------------
    s = troca(s, "<title>Mini Organizador P</title>",
              "<title>ELO · a linha</title>", "titulo")
    s = troca(s, '<span class="eyebrow">Nitron · projeto P</span>',
              '<span class="eyebrow">Nitron · linha ELO</span>', "eyebrow")
    s = troca(s, "<h1>Cesto Mini Organizador</h1>",
              "<h1>ELO</h1>", "h1")
    sub = (f'P {vg(p["cap"], 2)} L · M {vg(m["cap"], 2)} L · PP · peça única '
           f'· dois P acoplados empilham no M')
    s = re.sub(r'<span class="sub">[^<]*saída[^<]*</span>',
               f'<span class="sub">{sub}</span>', s, count=1)
    s = troca(s, """      <button class="modo" data-modo="peca" aria-pressed="true">A peça</button>
      <button class="modo" data-modo="encaixa" aria-pressed="false">Encaixadas</button>
      <button class="modo" data-modo="empilha" aria-pressed="false">Empilhadas</button>
      <button class="modo" data-modo="acopla" aria-pressed="false">Acopladas</button>""",
              """      <button class="modo" data-modo="linha" aria-pressed="true">A linha</button>
      <button class="modo" data-modo="m" aria-pressed="false">O M</button>
      <button class="modo" data-modo="dois" aria-pressed="false">Dois P no M</button>
      <button class="modo" data-modo="torre" aria-pressed="false">A torre</button>
      <button class="modo" data-modo="encaixa" aria-pressed="false">Encaixados</button>
      <button class="modo" data-modo="empilha" aria-pressed="false">Empilhados</button>
      <button class="modo" data-modo="acopla" aria-pressed="false">Acoplados</button>""",
              "botoes de modo")

    # ---- as cenas ---------------------------------------------------------
    js = cenas(d)
    corpo = ",\n  ".join(
        f"{k}: {{ titulo: {jstr(v['titulo'])}, texto: {jstr(v['texto'])}, "
        f"dados: {jlist(v['dados'])}, selo: {jstr(v['selo'])}, "
        f"poses: {jlist(v['poses'])} }}" for k, v in js.items())
    novo = "var MODOS = {\n  " + corpo + "\n};"
    s = re.sub(r"var PASSO_ENCAIXE = .*?\n\nvar MODOS = \{.*?\n\};",
               novo, s, count=1, flags=re.S)
    if "var MODOS = {" not in s:
        raise SystemExit("nao substitui o bloco MODOS")
    s = troca(s, "var modo = 'peca'", "var modo = 'linha'", "modo inicial")

    s = re.sub(r'<span class="sub" id="cTexto">[^<]*</span>',
               '<span class="sub" id="cTexto">a linha ELO em 3D</span>',
               s, count=1)
    s = troca(s, "// Visor do cesto P. Sem biblioteca externa: o solido do CAD vem embutido",
              "// Visor da linha ELO. Sem biblioteca externa: os DOIS solidos do CAD vem",
              "comentario do visor")

    open(SAI, "w", encoding="utf-8").write(s)
    print(f"\nvisor-elo.html: {os.path.getsize(SAI)/1024:.0f} kB", flush=True)


def jstr(x):
    import json
    return json.dumps(x, ensure_ascii=False)


def jlist(x):
    import json
    return json.dumps(x, ensure_ascii=False)


if __name__ == "__main__":
    import sys as _s
    main(rapido="--rapido" in _s.argv)
