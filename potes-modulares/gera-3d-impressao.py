#!/usr/bin/env python3
"""
Variantes dos STL para PROTOTIPAR em FDM (nao sao as pecas de producao).

O corpo de producao apoia na mesa so pelo anel do pe rebaixado - area pequena
demais para segurar uma peca de 62 mm de altura em qualquer impressora. Aqui
saem duas versoes do 600 ml:

  pote-600-real.stl        a peca como e, fundo rebaixado. Imprima com brim.
  pote-600-fundoplano.stl  elevacao de fundo zerada -> ~20x mais contato. Muda
                           so o volume interno (+19 ml), nao muda encaixe, passo
                           nem a prova da tampa. E a que eu imprimiria primeiro.

As areas de contato sao MEDIDAS na malha, nao digitadas: numero fixo aqui ja
ficou defasado uma vez, quando o footprint mudou de 121,2 para 139,7 mm.
  tampa-pp.stl             tampa de PP com 2 travas de clipe. Imprime em pe.
  tampa-teca.stl           placa macica - so para conferir encaixe (em teca e CNC).
  tampa-bocal.stl          a de bocal, com o gargalo de 14 mm.
  fecho-bocal.stl          o fecho de saia e plug conico. E o par que mais precisa de
                           prototipo: a vedacao e um cone de 1° apertando num
                           furo de 5°, e em FDM a parede sai ~0,1 mm mais
                           grossa - o plug vai assentar mais raso que o nominal.

Uso:  python3 gera-3d-impressao.py
"""
import os
import importlib.util

spec = importlib.util.spec_from_file_location("gera3d",
       os.path.join(os.path.dirname(os.path.abspath(__file__)), "gera-3d.py"))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

SEG = 24          # o dobro do padrao: canto mais liso no prototipo


def altura(tris):
    zs = [v[2] for t in tris for v in t]
    return max(zs) - min(zs)


def contato(tris, tol=1e-6):
    """Area que encosta na mesa: triangulos no z minimo com normal para baixo."""
    z0 = min(v[2] for t in tris for v in t)
    tot = 0.0
    for a, b, c in tris:
        if max(a[2], b[2], c[2]) > z0 + tol:
            continue
        ux, uy, uz = (b[0]-a[0], b[1]-a[1], b[2]-a[2])
        vx, vy, vz = (c[0]-a[0], c[1]-a[1], c[2]-a[2])
        nz = ux*vy - uy*vx
        if nz < 0:
            tot += abs(nz) / 2
    return tot


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(base, 'stl', 'impressao')
    os.makedirs(out, exist_ok=True)

    c, H = g.corpo(1, SEG)
    g.grava_stl(os.path.join(out, 'pote-600-real.stl'), c.tris, 'pote-600-real')
    print(f"pote-600-real.stl        {len(c.tris):5d} tri | altura {H:.1f} mm | "
          f"contato na mesa {contato(c.tris):6.0f} mm2 -> brim de 10 mm obrigatorio")

    elev = g.ELEV[1]
    g.ELEV[1] = 0.0                       # fundo plano so para imprimir
    c2, _ = g.corpo(1, SEG)
    g.ELEV[1] = elev
    g.grava_stl(os.path.join(out, 'pote-600-fundoplano.stl'), c2.tris, 'pote-600-fundoplano')
    print(f"pote-600-fundoplano.stl  {len(c2.tris):5d} tri | altura {H:.1f} mm | "
          f"contato na mesa {contato(c2.tris):6.0f} mm2 "
          f"({contato(c2.tris)/contato(c.tris):.0f}x) -> imprime facil")

    tp = g.tampa_pp(SEG)
    g.grava_stl(os.path.join(out, 'tampa-pp.stl'), tp.tris, 'tampa-pe')
    inv_pp = [[(v[0], -v[1], -v[2]) for v in tri] for tri in tp.tris]
    print(f"tampa-pp.stl             {len(tp.tris):5d} tri | altura {altura(tp.tris):.1f} mm | "
          f"contato {contato(tp.tris):5.0f} mm2 de pe, {contato(inv_pp):5.0f} mm2 invertida"
          f" -> IMPRIME INVERTIDA (de pe apoia so na ponta das 2 travas)")

    tc = g.tampa_teca(SEG)
    g.grava_stl(os.path.join(out, 'tampa-teca.stl'), tc.tris, 'tampa-teca')
    inv = [[(v[0], -v[1], -v[2]) for v in tri] for tri in tc.tris]
    print(f"tampa-teca.stl           {len(tc.tris):5d} tri | altura {altura(tc.tris):.1f} mm | "
          f"contato {contato(tc.tris):5.0f} mm2 de pe, {contato(inv):5.0f} mm2 invertida"
          f" -> placa macica, tanto faz; em producao e CNC em teca")

    tr = g.tampa_bocal(SEG)
    g.grava_stl(os.path.join(out, 'tampa-bocal.stl'), tr.tris, 'tampa-bocal')
    inv_tr = [[(v[0], -v[1], -v[2]) for v in tri] for tri in tr.tris]
    print(f"tampa-bocal.stl          {len(tr.tris):5d} tri | altura {altura(tr.tris):.1f} mm | "
          f"contato {contato(tr.tris):5.0f} mm2 de pe, {contato(inv_tr):5.0f} mm2 invertida"
          f" -> De pe ela fica na ponta das travas. INVERTIDA ela apoia no ARO"
          f" do gargalo, que com a calha fora virou um anel plano de verdade -"
          f" a revisao 13 nao tinha onde apoiar em nenhum dos dois sentidos."
          f" Imprima INVERTIDA: o aro vira a primeira camada e o colar cresce"
          f" como uma torre de 14 mm, que o PETG faz sem suporte.")

    fb = g.fecho_bocal(SEG)
    g.grava_stl(os.path.join(out, 'fecho-bocal.stl'), fb.tris, 'fecho-bocal')
    inv_fb = [[(v[0], -v[1], -v[2]) for v in tri] for tri in fb.tris]
    print(f"fecho-bocal.stl          {len(fb.tris):5d} tri | altura {altura(fb.tris):.1f} mm | "
          f"contato {contato(fb.tris):5.0f} mm2 de pe, {contato(inv_fb):5.0f} mm2 invertida"
          f" -> INVERTIDA (domo para baixo): o planalto do domo vira a base e a"
          f" saia cresce como uma saia, que e exatamente o sentido em que a"
          f" casca abre. De pe seria pior: apoiaria na borda de 1,30 mm da saia"
          f" e o domo ficaria em ponte sobre o vazio. Com o fecho invertido a"
          f" face de vedacao do plug sai lisa, que e a que importa no ensaio.")

    print(f"\nem {out}")
    print("Nenhum dos tres vedantes se imprime em FDM. Para o prototipo: o ARO EM U "
          "(2,80 x 3,10, calcado na lingueta) so existe como perfil extrudado - peca "
          "uma amostra ao fornecedor antes do try-out, porque e ele que decide a "
          "vedacao. A corda da teca (1,4 mm) e o 2o aro (1,2 mm) saem de corda de "
          "silicone comum, cortada no comprimento e colada de topo.")
    print("O plug do fecho veda por CONE, nao por interferencia reta: em FDM ele vai "
          "assentar mais raso que o nominal (parede ~0,1 mm mais grossa). Isso NAO "
          "invalida o teste - o que o prototipo responde e se ele veda, e onde para.")


if __name__ == '__main__':
    main()
