#!/usr/bin/env python3
"""Monta conceitos-3d.html: os dez conceitos como SOLIDO, renderizados.

Le conceitos-medidas.json (peso e capacidade medidos no solido) e as imagens
de design/img/. As imagens entram embutidas em base64: o arquivo abre sozinho,
sem pasta ao lado.

Uso:  python3 galeria.py
"""
import base64
import json
import os

DEST = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(DEST, "img")

LEITURA = {
 0: ("A peça de hoje — a referência",
     "Configuração C, a que está pronta para cotação. Tudo abaixo sai daqui."),
 1: ("Some o engradado inteiro",
     "É a mudança que mais transforma a peça, e a mais barata de explicar "
     "para a ferramentaria: menos feição, não mais. Custa <b>15,4 g</b> — a "
     "minha estimativa no croqui dizia 17, e o sólido corrigiu para menos."),
 2: ("Mesma função, outro idioma",
     "A fenda contínua lê como ripa de madeira, não como furo de engradado. "
     "E surpreende na balança: fica <b>7,0 g mais leve</b> que hoje, porque a "
     "nervura horizontal entre as faixas some."),
 3: ("Acabamento, não assinatura",
     "A canelura de 0,7 mm aparece na luz rasante e some na luz chapada — "
     "no render ela quase não se lê. Vale como textura premium ao toque, "
     "não como gesto que se reconhece de longe. E é a mais cara: "
     "<b>+25,9 g</b>."),
 4: ("A mais barata da lista",
     "Fechar só a faixa de cima limpa a linha da borda por <b>+4,5 g</b>. "
     "Mas é discreta: de longe ainda parece o cesto de hoje."),
 5: ("Não convenceu — e o sólido é que mostrou",
     "A frente de hoje <b>já é um recorte</b>: os dois chanfros abrem uma "
     "concha da borda até a meia altura. Somar um arco a ela só aumenta o "
     "buraco. Tentei subir a frente reduzindo o chanfro de topo e o modelo "
     "quebrou duas vezes (o fillet R12 da face frontal, depois a tapa do "
     "rasgo). <b>Este conceito exige redesenhar a frente inteira</b> — é "
     "projeto, não estudo de forma."),
 6: ("Funciona na hora",
     "O oval abaixo da borda lê como produto de casa imediatamente, e ainda "
     "tira <b>2,8 g</b>. O problema continua sendo o da folha anterior: é a "
     "face curta que acopla."),
 7: ("Muda mais visto de cima do que de lado",
     "R40 na base (≈R54 na boca) contra R14 de hoje. De frente quase não se "
     "nota; de cima — que é o ângulo da foto de organização — vira outro "
     "produto. Custa <b>0,14 L</b> (−3,5%) e tira 10,2 g."),
 8: ("A fresta de sombra faz o efeito",
     "Trocar a saia por uma recuada 4 mm dá a linha de sombra sob a peça por "
     "<b>+2,2 g</b>. Foi preciso trocar a saia, não cortá-la: a parede tem "
     "1,4 mm, e cortar 4 mm dela apaga a saia inteira."),
 9: ("Aqui eu errei feio, e o sólido corrigiu",
     "No croqui eu estimei <b>+4 a +8 g</b>. Medido: <b>+53,6 g</b>. Uma "
     "borda de 13 mm de altura dando a volta no perímetro é muita resina — "
     "a peça vai a 232,7 g, 30% mais pesada que hoje. Ou a borda encolhe "
     "muito (5 a 6 mm), ou o conceito está fora."),
 10: ("O único que melhora forma E peso",
      "O rebaixo de 2 mm no topo da parede tira <b>10,7 g</b> — é o conceito "
      "mais leve dos dez. E a sombra só existe com duas peças: por isso a "
      "segunda foto é a torre, que é o produto de verdade deste conceito."),
}
TITULO = {0: "Hoje", 1: "Pele lisa", 2: "Ripado", 3: "Canelado",
          4: "Meia-pele", 5: "Arco frontal", 6: "Pega oval", 7: "Canto R40",
          8: "Plinto", 9: "Borda virada", 10: "Junta celebrada"}
SELO = {5: ("nao", "não convenceu"), 9: ("cuidado", "pesado demais"),
        2: ("bom", "mais leve que hoje"), 10: ("bom", "mais leve que hoje"),
        8: ("bom", "melhor efeito/risco"), 6: ("cuidado", "briga com o acople")}


def vg(x, casas=1):
    return f"{x:.{casas}f}".replace(".", ",")


def b64(caminho):
    with open(caminho, "rb") as f:
        return base64.b64encode(f.read()).decode()


def img(base, vista):
    caminho = os.path.join(IMG, f"{base}-{vista}.png")
    if not os.path.exists(caminho):
        return ""
    return f'<img src="data:image/png;base64,{b64(caminho)}" alt="">'


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--fundo:#f7f5f1;--papel:#fffefc;--tinta:#1d1813;--gris:#6d645a;
      --linha:#e7e2da;--novo:#c2410c;--bom:#15803d;--cui:#b45309;--nao:#b91c1c}
body{background:var(--fundo);color:var(--tinta);
     font:16px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,
     "Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:1160px;margin:0 auto;padding:56px 24px 100px}
h1{font-size:clamp(30px,4.6vw,46px);line-height:1.1;letter-spacing:-.024em;
   font-weight:700;max-width:17ch}
.sub{color:var(--gris);font-size:17px;margin-top:14px;max-width:64ch}
.aviso{margin-top:26px;padding:15px 19px;border-left:3px solid var(--novo);
       background:#fdf3ec;font-size:14.5px;max-width:72ch;
       border-radius:0 8px 8px 0}
.ref{margin:52px 0 12px;background:var(--papel);border:1px solid var(--linha);
     border-radius:20px;overflow:hidden;display:grid;
     grid-template-columns:1.25fr 1fr}
.tabela{margin:56px 0 12px;background:var(--papel);border:1px solid var(--linha);
        border-radius:16px;padding:22px 24px;overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:13.6px}
th{text-align:right;font-size:11px;letter-spacing:.09em;text-transform:uppercase;
   color:var(--gris);font-weight:700;padding:0 10px 9px;white-space:nowrap}
th:first-child,td:first-child{text-align:left}
td{padding:7px 10px;border-top:1px solid var(--linha);text-align:right;
   white-space:nowrap}
td.n{font-weight:600}
.mais{color:var(--cui)} .menos{color:var(--bom)}
h2{font-size:13px;letter-spacing:.14em;text-transform:uppercase;
   color:var(--gris);font-weight:700;margin:64px 0 18px}
.card{background:var(--papel);border:1px solid var(--linha);border-radius:20px;
      overflow:hidden;display:grid;grid-template-columns:1.25fr 1fr;
      margin-bottom:22px}
@media(max-width:880px){.card,.ref{grid-template-columns:1fr}}
.fotos.duas{padding:10px 6px}
.fotos{background:#f9f7f3;display:grid;grid-template-columns:1fr;gap:0;
       align-content:center}
.fotos.duas{grid-template-columns:1.35fr 1fr;align-items:center}
.fotos img{width:100%;height:auto;display:block}
.txt{padding:28px 30px 30px}
.num{font-size:12px;font-weight:700;color:var(--novo);letter-spacing:.1em}
h3{font-size:26px;letter-spacing:-.018em;margin:6px 0 4px;font-weight:700}
.tag{color:var(--gris);font-size:15px;margin-bottom:16px}
.leitura{font-size:14.6px;margin-bottom:18px}
.cotas{display:flex;gap:26px;border-top:1px solid var(--linha);padding-top:15px;
       flex-wrap:wrap}
.cota b{display:block;font-size:11px;letter-spacing:.08em;color:var(--gris);
        text-transform:uppercase;font-weight:700;margin-bottom:3px}
.cota span{font-size:19px;font-weight:600;letter-spacing:-.01em}
.selo{display:inline-block;font-size:10.5px;font-weight:700;padding:3px 10px;
      border-radius:99px;letter-spacing:.06em;text-transform:uppercase;
      margin-bottom:10px}
.selo.bom{background:#e7f6ec;color:var(--bom)}
.selo.cuidado{background:#fdf1de;color:var(--cui)}
.selo.nao{background:#fdeaea;color:var(--nao)}
.fim{margin-top:56px;padding:24px 26px;border:1px dashed #d9d2c6;
     border-radius:16px;font-size:15px;max-width:78ch;background:var(--papel)}
.fim b{color:var(--novo)}
"""


def main():
    d = json.load(open(os.path.join(DEST, "conceitos-medidas.json"),
                       encoding="utf-8"))
    p0 = d["0"]["peso"]

    def base(n):
        return f"c{n:02d}-{d[str(n)]['nome']}"

    def delta(n):
        x = d[str(n)]["peso"] - p0
        if abs(x) < 0.05:
            return '<span>=</span>'
        cls = "mais" if x > 0 else "menos"
        return f'<span class="{cls}">{x:+.1f} g</span>'.replace(".", ",")

    linhas = ""
    for n in sorted(map(int, d)):
        it = d[str(n)]
        linhas += (
            f'<tr><td class="n">{TITULO[n]}</td>'
            f'<td>{it["peso"]:.1f}</td><td>{delta(n)}</td>'
            f'<td>{it["cap"]:.2f}</td>'
            f'<td>{it["peso"]/it["cap"]:.1f}</td></tr>').replace(".", ",")
    linhas = linhas.replace("</td><td>", "</td><td>")

    cards = ""
    for n in sorted(map(int, d)):
        if n == 0:
            continue
        it = d[str(n)]
        tit, leitura = LEITURA[n]
        selo = ""
        if n in SELO:
            cls, txt = SELO[n]
            selo = f'<div class="selo {cls}">{txt}</div>'
        fotos = img(base(n), "34") + (img(base(n), "torre") if n == 10
                                      else img(base(n), "topo"))
        cards += f"""<article class="card">
  <div class="fotos duas">{fotos}</div>
  <div class="txt">{selo}
    <div class="num">{n:02d}</div>
    <h3>{TITULO[n]}</h3>
    <div class="tag">{tit}</div>
    <p class="leitura">{leitura}</p>
    <div class="cotas">
      <div class="cota"><b>peso</b><span>{vg(it['peso'])} g</span></div>
      <div class="cota"><b>contra hoje</b><span>{delta(n)}</span></div>
      <div class="cota"><b>capacidade</b>
        <span>{vg(it['cap'], 2)} L</span></div>
      <div class="cota"><b>g por litro</b>
        <span>{vg(it['peso']/it['cap'])}</span></div>
    </div>
  </div>
</article>""".replace("g</span>", "g</span>")

    html = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ELO B2C · os dez conceitos em 3D</title>
<style>{CSS}</style></head><body><div class="wrap">
<h1>Os dez conceitos, agora em sólido</h1>
<p class="sub">Cada peça foi construída de verdade a partir do ELO P e
<b>pesada no sólido</b> — não é desenho, é geometria. As imagens são renders
do próprio modelo, sempre do mesmo ângulo e na mesma escala.</p>
<div class="aviso"><b>O que isto é e o que não é.</b> É estudo de forma: serve
para olhar e escolher. <b>Não</b> passou por auditoria de extração, nem por
medição de empilhamento, encaixe e acoplamento — essas três só valem a pena
depois que o desenho estiver escolhido, porque cada uma custa minutos de
booleano por peça.</div>

<div class="ref">
  <div class="fotos duas">{img(base(0), '34')}{img(base(0), 'torre')}</div>
  <div class="txt">
    <div class="num">00</div><h3>Hoje</h3>
    <div class="tag">A peça de hoje, e a torre dela — a referência de tudo</div>
    <p class="leitura">Configuração C, a que está pronta para cotação de
    ferramental. Todos os dez conceitos abaixo saem daqui, com uma alteração
    cada.</p>
    <div class="cotas">
      <div class="cota"><b>peso</b><span>{vg(p0)} g</span></div>
      <div class="cota"><b>capacidade</b>
        <span>{vg(d['0']['cap'], 2)} L</span></div>
      <div class="cota"><b>g por litro</b>
        <span>{vg(p0/d['0']['cap'])}</span></div>
    </div>
  </div>
</div>

<div class="tabela">
<table><thead><tr><th>conceito</th><th>peso (g)</th><th>contra hoje</th>
<th>capacidade (L)</th><th>g/L</th></tr></thead>
<tbody>{linhas}</tbody></table>
</div>

<h2>Um por um</h2>
{cards}

<div class="fim">
<b>Duas coisas que só apareceram porque virou sólido.</b> A <b>borda virada</b>
eu estimei em +4 a +8 g no croqui e o sólido deu <b>+53,6 g</b> — eu errei por
um fator de sete, e é o tipo de erro que só a medição pega. E o <b>arco
frontal</b>, que eu tinha eleito como o de maior retorno, <b>não funciona</b>
sobre a frente de hoje: ela já é um recorte, e o arco vira só um buraco maior.
Para ele existir, a frente inteira precisa ser redesenhada.
<br><br>
<b>Os três que eu levaria adiante:</b> <b>ripado</b> (−7,0 g, muda o idioma
sem custar peso), <b>plinto</b> (+2,2 g, o efeito mais forte pelo menor risco)
e <b>junta celebrada</b> (−10,7 g, o único que melhora forma e peso ao mesmo
tempo). Os três combinam entre si e nenhum toca a cota que define a linha.
<br><br>
Diga quais e eu fecho o 3D com auditoria de extração e medição de
empilhamento, encaixe e acoplamento — e aí sobe para o M e o G.
</div>
</div></body></html>"""
    caminho = os.path.join(DEST, "conceitos-3d.html")
    open(caminho, "w", encoding="utf-8").write(html)
    print(f"gerado {caminho} ({len(html)/1024/1024:.1f} MB)")


if __name__ == "__main__":
    main()
