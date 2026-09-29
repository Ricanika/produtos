#!/usr/bin/env python3
"""Gera conceitos-b2c.html -- as 10 possibilidades de design para a virada B2C.

Croqui, nao solido. A regra que vale para todos os dez: UM MOLDE POR TAMANHO,
uma injecao, duas placas, sem gaveta e sem postico movel. Cada conceito diz o
que faz com o peso, com a capacidade e com o sistema ELO (empilhar, encaixar,
acoplar, e o P pousando no M e no G), e o que ainda precisa ser medido.

Os pesos marcados "estimado" sao aritmetica de area x parede x densidade, nao
medicao no solido -- estao marcados como tal em cada linha.

Uso:  python3 conceitos.py
"""
import os

import desenho as D

DEST = os.path.dirname(os.path.abspath(__file__))

# Fechar a parede devolve o plastico dos rasgos: area x 1,4 mm x 0,905 g/cm3
FECHA = {"P": 123 * 6.0 * 18.33 * 1.4 * 0.905e-3,
         "M": 149 * 14.0 * 34.0 * 1.4 * 0.905e-3,
         "G": 337 * 14.0 * 34.0 * 1.4 * 0.905e-3}

OK, ATENCAO, RISCO = "ok", "atencao", "risco"

CONCEITOS = [
 dict(n=1, nome="Pele lisa + textura fosca",
      fam="Pele", tag="tirar o vazado e apostar na superfície",
      frente=lambda: D.frente(extras=D.textura()),
      segundo=lambda: D.planta(raio=28),
      leg2="planta de hoje, R28 na boca",
      gesto="A parede fecha por inteiro e o produto passa a ser lido pela "
            "<b>superfície</b>, não pelo furo. Textura de molde fosca "
            "(granulado fino, VDI 24–30) no corpo inteiro, com a borda e o "
            "fundo lisos para contraste. É a mudança de menor risco técnico e "
            "a de maior efeito na foto: sem furo, o cesto deixa de parecer "
            "engradado e vira objeto.",
      molde=(OK, "Textura é gravação na cavidade, não feição nova. Mas "
                 "<b>textura come saída</b>: a regra de bolso é ~1° a mais "
                 "por 0,025 mm de profundidade. O P tem 6° e aceita bem; o M "
                 "e o G têm 3°, e aí cabe granulado fino, não couro fundo."),
      peso=("P +17 g · M +90 g · G +203 g", "estimado"),
      elo=(OK, "Não mexe em nada: empilha, encaixa, acopla e recebe o P igual."),
      risco="O G vai a ~836 g e passa de 1 kg de miolo de custo — e perde o "
            "argumento de 12,4 g/L, que é o melhor número comercial da linha."),

 dict(n=2, nome="Ripado",
      fam="Pele", tag="a listra vira uma só, do pé à borda",
      frente=lambda: D.frente(rasgos=D.ripas()),
      segundo=lambda: D.frente(rasgos=D.listras()), vb2="0 0 264 212",
      leg2="o vazado de hoje, para comparar",
      gesto="Em vez de 123 rasgos curtos em 3 faixas, <b>9 fendas contínuas "
            "de ponta arredondada</b>, da base à borda. O olho lê ritmo, não "
            "perfuração: é a linguagem de ripa de madeira, não de caixa "
            "plástica. Mesmo furo, mesma função, outro idioma.",
      molde=(OK, "Rasgo passante em parede com saída é exatamente a linha de "
                 "base de extração que o projeto já audita (9.217 mm³ no P). "
                 "Fenda mais longa significa <b>postiço mais esbelto</b> na "
                 "cavidade — pede conferência de rigidez com a ferramentaria."),
      peso=("neutro a −10 g", "depende do vão livre"),
      elo=(OK, "A nervura horizontal entre faixas some; é ela que enrijece a "
               "parede hoje. Precisa medir se a borda sozinha aguenta a pilha."),
      risco="Fenda contínua tira a nervura horizontal. É a única mudança de "
            "pele que mexe em estrutura, e a que mais pede ensaio."),

 dict(n=3, nome="Canelado",
      fam="Pele", tag="relevo em vez de furo — zero perfuração",
      frente=lambda: D.frente(extras=D.canelado()),
      segundo=lambda: D.planta(raio=28),
      leg2="a canelura acompanha a saída",
      gesto="Nenhum furo: <b>nervuras verticais finas em relevo</b> (2 mm de "
            "largura, 0,8 mm de saliência, passo 8 mm) correndo na direção da "
            "desmoldagem. Lê como vidro canelado e cerâmica — o vocabulário "
            "mais 'casa' que existe hoje em utilidade —, esconde marca de "
            "chupagem e dá rigidez de graça.",
      molde=(OK, "Canelura vertical é paralela ao saque: sai sozinha, desde "
                 "que ela também tenha saída. Usinagem de cavidade um pouco "
                 "mais cara, nada mais."),
      peso=("P +21 g · M +104 g · G +230 g", "estimado, fecha a parede e soma "
            "o relevo"),
      elo=(OK, "Não mexe. O relevo fica dentro do envelope da aba."),
      risco="É o conceito mais pesado de todos. Só fecha se o preço B2C "
            "subir junto — e o 047 diz que sobe (R$ 4,58 na fábrica viram "
            "R$ 19,99 a 29,15 na gôndola)."),

 dict(n=4, nome="Meia-pele",
      fam="Pele", tag="topo limpo para a marca, vazado só embaixo",
      frente=lambda: D.frente(rasgos=D.meia_pele()),
      segundo=lambda: D.planta(raio=28),
      leg2="planta inalterada",
      gesto="Duas zonas: <b>metade de cima cega</b> — é onde a foto, o rótulo "
            "e a marca vivem — e <b>uma faixa vazada baixa</b>, onde a carga "
            "realmente pede alívio. Resolve o pior defeito visual de hoje (o "
            "furo sobe até a borda e polui a linha do topo) sem abrir mão do "
            "peso.",
      molde=(OK, "Menos rasgo que hoje, mesma família de feição. Nada novo."),
      peso=("P +9 g · M +45 g · G +101 g", "estimado, ~metade dos rasgos"),
      elo=(OK, "Não mexe."),
      risco="Nenhum técnico. O risco é de gosto: fica no meio do caminho "
            "entre o industrial e o limpo, e meio-termo não vira foto."),

 dict(n=5, nome="Arco frontal",
      fam="Silhueta", tag="um gesto só: alça, acesso e assinatura",
      frente=lambda: D.frente(rasgos=D.arco()),
      segundo=lambda: D.planta(raio=28),
      leg2="a boca não muda",
      gesto="Os dois chanfros a 45° e o rasgo frontal — as feições mais "
            "'bin de picking' da peça — dão lugar a <b>um único arco cortado "
            "na parede da frente</b>. Ele é a alça, é o acesso sem tirar da "
            "prateleira e é a assinatura que se reconhece a três metros. É o "
            "conceito com maior retorno por milímetro mexido.",
      molde=(OK, "Furo passante em parede com saída: mesma família do rasgo. "
                 "<b>O arco tem de parar abaixo da borda</b> — o anel do rim "
                 "é a estrutura da peça (§4.2.1) e não pode ser interrompido."),
      peso=("P −6 g · M −18 g · G −26 g", "estimado, tira material"),
      elo=(ATENCAO, "A frente é onde o P apoia no rim do de baixo. O arco "
                    "precisa nascer acima da linha de apoio, ou a pilha perde "
                    "contato na frente."),
      risco="Mexe na face que hoje resolve o empilhamento. É medição, não "
            "opinião: a cota de apoio já está no modelo."),

 dict(n=6, nome="Pega oval nas laterais",
      fam="Silhueta", tag="o recorte que todo organizador bonito tem",
      frente=lambda: D.frente(rasgos=D.pega_oval()),
      segundo=lambda: D.planta(raio=28),
      leg2="a pega fica na face curta",
      gesto="Um <b>recorte oval logo abaixo da borda</b>, nas duas faces "
            "curtas. É o detalhe mais universal do organizador doméstico "
            "(Muji, Hay, Coza usam variações dele) e resolve pegar o cesto "
            "cheio, que hoje se faz pela borda fina.",
      molde=(OK, "Furo passante, sem gaveta."),
      peso=("P −4 g · M −9 g · G −11 g", "estimado"),
      elo=(RISCO, "<b>A face curta do P é a face do acoplamento</b>: a aba "
                  "vai de 90 a 102 mm do eixo e é ali que duas peças se "
                  "engatam. Pega e engate disputam o mesmo lugar — ou a pega "
                  "desce para o meio da parede, ou o acoplamento muda de face."),
      risco="É o único conceito que colide de frente com o diferencial da "
            "linha. Vale como opção deliberada: 'a versão B2C não acopla'."),

 dict(n=7, nome="Canto R60",
      fam="Silhueta", tag="a planta deixa de ser retângulo",
      frente=lambda: D.frente(),
      segundo=lambda: D.planta(raio=60),
      leg2="R60 no canto (hoje é R14 na base)",
      gesto="Hoje o canto da planta é R14 na base e ~R28 na boca — quase "
            "quadrado, que é o que dá o ar de engradado visto de cima. "
            "Levando a <b>R60</b>, a planta vira um 'soft square' e o produto "
            "ganha o desenho de cima, que é justamente o ângulo da foto de "
            "organização.",
      molde=(OK, "Raio maior é usinagem mais fácil, não mais difícil."),
      peso=("−3% a −5% de capacidade", "estimado, o canto é volume"),
      elo=(ATENCAO, "O acoplamento precisa de um trecho reto de aba para as "
                    "duas peças se encontrarem. Em 180 mm de boca, R60 deixa "
                    "60 mm retos — dá, mas aperta. No M e no G sobra."),
      risco="Come litro, e o P já é o tamanho que perde nesse quesito "
            "(43,9 g/L contra ~37,8 do concorrente)."),

 dict(n=8, nome="Plinto — a peça flutua",
      fam="Silhueta", tag="o pé vira sombra, não vira pé",
      frente=lambda: D.frente(pes=False, plinto=True),
      segundo=lambda: D.frente(pes=True), vb2="0 0 264 212",
      leg2="o tripé de hoje, aparente",
      gesto="Os quatro pezinhos e a saia traseira — puro vocabulário de "
            "caixa — recuam para dentro de uma <b>base rebaixada</b>. De fora "
            "vê-se uma fresta de sombra corrida sob a peça, e ela parece "
            "flutuar. Melhor ainda: o plinto vira <b>espiga de centragem</b>, "
            "e a pilha ganha registro em vez de depender do atrito.",
      molde=(OK, "Rebaixo que abre para baixo sai no macho. É a mesma lógica "
                 "da bolsa cega sob o pé que já existe."),
      peso=("neutro", "redistribui, não soma"),
      elo=(OK, "Melhora: o apoio deixa de ser um tripé de 463 mm² e passa a "
               "ser um anel contínuo, com muito mais contato."),
      risco="Nenhum evidente. É o conceito com melhor relação "
            "efeito/risco da lista."),

 dict(n=9, nome="Borda virada",
      fam="Silhueta", tag="some a aba de caixote; o engate vai para baixo dela",
      frente=lambda: D.frente(aba=False),
      segundo=lambda: D.corte_borda(),
      leg2="corte da borda: o engate escondido",
      gesto="A aba reta de 12 mm que hoje sai para fora — a feição que mais "
            "grita caixa de feira — <b>vira para baixo</b> e forma uma borda "
            "cheia, macia ao toque, com o engate do acoplamento escondido na "
            "parte de dentro dela. De fora some a aba; de dentro a função "
            "continua.",
      molde=(OK, "<b>Isto já existe no projeto</b>: a dobra de 5 mm da aba. "
                 "O canal entre a dobra e a parede abre para baixo, e o aço "
                 "sai por ali — foi o que a auditoria de extração já provou."),
      peso=("+4 a +8 g por tamanho", "estimado"),
      elo=(OK, "O passo acoplado (200/400/600) é dado pela aresta da aba; "
               "virando-a para baixo o passo se mantém, mas <b>precisa ser "
               "remedido</b> — foi exatamente aqui que o passo errado apareceu "
               "uma vez e duas peças ficaram 20 mm interpenetradas."),
      risco="Mexe na cota que define a regra da linha inteira (380 = 2×180 + "
            "2×10). Qualquer mudança aqui obriga a remedir o par e o trio."),

 dict(n=10, nome="Junta celebrada",
      fam="Sistema", tag="a torre é o produto, não o cesto",
      frente=lambda: D.junta(),
      segundo=lambda: D.frente(rasgos=D.ripas(n=7)), vb2="0 0 264 212",
      leg2="a peça sozinha fica sóbria de propósito",
      gesto="Em vez de esconder o empilhamento, <b>desenhá-lo</b>: um rebaixo "
            "de 2 mm no topo da parede cria uma linha de sombra contínua onde "
            "uma peça encontra a outra. Empilhado, o conjunto vira um objeto "
            "só, listrado de sombra — e é a torre, não o cesto, que vai para "
            "a foto. É o único conceito que transforma o diferencial técnico "
            "da linha em argumento visual.",
      molde=(OK, "Rebaixo no topo da parede sai no saque. Zero custo novo."),
      peso=("neutro", "—"),
      elo=(OK, "Reforça: a promessa do 2 P sobre o M e 3 P sobre o G passa a "
               "ser visível na prateleira."),
      risco="Sozinho não resolve — a peça individual continua com a pele de "
            "hoje. É o conceito que <b>combina</b>, não o que substitui."),
]

RECEITAS = [
 dict(nome="A · A CALMA", itens="1 + 8 + 9 + 10",
      txt="Pele lisa e fosca, base em plinto, borda virada, junta desenhada. "
          "É a mais próxima do que o mercado doméstico chama de bonito hoje, e "
          "a de menor risco técnico — nenhum furo novo, nenhuma cota do "
          "sistema ELO tocada além da borda. <b>Custo: o peso.</b> O G sai de "
          "632,9 g para ~840, e o argumento de 12,4 g/L vai junto.",
      rec=True),
 dict(nome="B · A GRÁFICA", itens="2 + 7 + 8 + 10",
      txt="Ripado contínuo, canto R60, plinto e junta desenhada. Mantém o "
          "vazado (e o peso, e a ventilação), mas troca o idioma dele. É a "
          "receita que <b>preserva os 12,4 g/L</b> e ainda assim muda a "
          "prateleira. Pede o ensaio da parede sem a nervura horizontal."),
 dict(nome="C · O ÍCONE", itens="5 + 1 + 8",
      txt="Arco frontal, pele lisa, plinto. Uma peça de gesto único, que se "
          "reconhece de longe e não precisa de rótulo. É a de maior retorno de "
          "imagem e a que mais mexe na engenharia: o arco cai justamente na "
          "face que hoje resolve o empilhamento."),
]

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--fundo:#faf8f4;--tinta:#1d1813;--gris:#6d645a;--linha:#e7e2da;
      --novo:#c2410c;--ok:#15803d;--at:#b45309;--ri:#b91c1c;--papel:#fffefb}
body{background:var(--fundo);color:var(--tinta);
     font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,
     "Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:1180px;margin:0 auto;padding:56px 24px 96px}
h1{font-size:clamp(28px,4.4vw,44px);line-height:1.12;letter-spacing:-.022em;
   font-weight:700;max-width:19ch}
.sub{color:var(--gris);font-size:17px;margin-top:14px;max-width:62ch}
.regra{margin-top:26px;padding:14px 18px;border-left:3px solid var(--novo);
       background:#fdf3ec;font-size:14.5px;max-width:70ch;border-radius:0 8px 8px 0}
h2{font-size:13px;letter-spacing:.14em;text-transform:uppercase;
   color:var(--gris);font-weight:700;margin:64px 0 18px}
.hoje{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
      gap:12px}
.hoje div{background:var(--papel);border:1px solid var(--linha);
          border-radius:12px;padding:14px 16px;font-size:14px}
.hoje b{display:block;font-size:12px;letter-spacing:.08em;color:var(--novo);
        text-transform:uppercase;margin-bottom:5px}
.grid{display:grid;gap:22px}
.card{background:var(--papel);border:1px solid var(--linha);border-radius:18px;
      overflow:hidden;display:grid;grid-template-columns:1fr 1.05fr}
@media(max-width:860px){.card{grid-template-columns:1fr}}
.arte{background:linear-gradient(170deg,#f6f2ea,#fbf8f2);padding:18px;
      display:grid;grid-template-columns:1fr 1fr;gap:10px;align-content:start}
.arte figure{background:var(--papel);border-radius:12px;padding:4px;
             border:1px solid #efeae1}
.arte figcaption{font-size:10.5px;color:var(--gris);text-align:center;
                 padding:0 4px 7px;line-height:1.35}
svg{width:100%;height:auto;display:block}
.corpo{fill:none;stroke:var(--tinta);stroke-width:2.6;stroke-linejoin:round}
.ln{fill:none;stroke:var(--tinta);stroke-width:2;stroke-linejoin:round}
.ln.tenue{stroke:#cdc6ba;stroke-width:1.4}
.furo{fill:var(--novo);fill-opacity:.16;stroke:var(--novo);stroke-width:1.8}
.canel{stroke:#b9b1a4;stroke-width:1.5}
.tex{fill:#cfc7b9}
.sombra{stroke:#cdc6ba;stroke-width:3;stroke-linecap:round}
.sombra.forte{stroke:var(--novo);stroke-width:3.4;stroke-linecap:round}
.cota{font:11px sans-serif;fill:var(--gris)}
.txt{padding:24px 26px 26px}
.num{font-size:12px;font-weight:700;color:var(--novo);letter-spacing:.1em}
.fam{font-size:11px;color:var(--gris);letter-spacing:.1em;text-transform:uppercase}
h3{font-size:23px;letter-spacing:-.015em;margin:6px 0 2px;font-weight:700}
.tag{color:var(--gris);font-size:14.5px;margin-bottom:14px}
.gesto{font-size:14.5px;margin-bottom:16px}
.linhas{display:grid;gap:9px;font-size:13.2px;border-top:1px solid var(--linha);
        padding-top:14px}
.linhas>div{display:grid;grid-template-columns:96px 1fr;gap:12px;
            align-items:start}
.rot{color:var(--gris);font-size:11px;letter-spacing:.08em;
     text-transform:uppercase;padding-top:2px}
.pill{display:inline-block;font-size:10.5px;font-weight:700;padding:2px 8px;
      border-radius:99px;letter-spacing:.06em;text-transform:uppercase;
      margin-right:7px;vertical-align:1px}
.ok{background:#e7f6ec;color:var(--ok)}
.atencao{background:#fdf1de;color:var(--at)}
.risco{background:#fdeaea;color:var(--ri)}
.est{color:var(--gris);font-size:11.5px}
.rec{display:grid;gap:14px}
.rec article{background:var(--papel);border:1px solid var(--linha);
             border-radius:16px;padding:20px 22px}
.rec article.top{border-color:#f0c8ae;background:#fffaf6}
.rec h4{font-size:15px;letter-spacing:.04em}
.rec .it{color:var(--novo);font-weight:700;font-size:13px;margin:2px 0 8px}
.rec p{font-size:14px}
.fim{margin-top:56px;padding:22px 24px;border:1px dashed #d9d2c6;
     border-radius:14px;font-size:14.5px;max-width:78ch;background:#fdfcf9}
.fim b{color:var(--novo)}
"""

HOJE = [
 ("o vazado", "123 rasgos curtos em 3 faixas, subindo até a borda: é a "
              "assinatura visual de engradado."),
 ("a aba para fora", "12 mm de aba reta em todo o perímetro — a borda de "
                     "caixa de feira, e a peça mais visível do conjunto."),
 ("os chanfros a 45°", "vieram do bin de picking da referência. Resolvem "
                       "acesso, mas desenham um objeto de estoque."),
 ("o tripé aparente", "quatro pezinhos e uma saia corrida, à mostra sob a "
                      "chapa."),
 ("a planta quase quadrada", "R14 na base. Visto de cima — o ângulo da foto "
                             "— lê retângulo duro."),
 ("o acabamento", "liso brilhante, laranja de sinalização. Nada de textura, "
                  "nada de paleta."),
]


def card(c):
    def linha(rot, conteudo):
        return f'<div><span class="rot">{rot}</span><span>{conteudo}</span></div>'
    st_m, tx_m = c["molde"]
    st_e, tx_e = c["elo"]
    peso, nota = c["peso"]
    return f"""<article class="card">
  <div class="arte">
    <figure><svg viewBox="0 0 264 212">{c['frente']()}</svg>
      <figcaption>o gesto, na frente</figcaption></figure>
    <figure><svg viewBox="{c.get('vb2', '0 0 200 192')}">{c['segundo']()}</svg>
      <figcaption>{c['leg2']}</figcaption></figure>
  </div>
  <div class="txt">
    <div class="num">{c['n']:02d} <span class="fam">· {c['fam']}</span></div>
    <h3>{c['nome']}</h3>
    <div class="tag">{c['tag']}</div>
    <p class="gesto">{c['gesto']}</p>
    <div class="linhas">
      {linha("molde", f'<span class="pill {st_m}">1 molde, 2 placas</span>{tx_m}')}
      {linha("peso", f'{peso} <span class="est">({nota})</span>')}
      {linha("sistema elo", f'<span class="pill {st_e}">'
             f'{"mantém" if st_e == OK else "atenção" if st_e == ATENCAO else "conflito"}'
             f'</span>{tx_e}')}
      {linha("risco", c['risco'])}
    </div>
  </div>
</article>"""


def main():
    hoje = "".join(f"<div><b>{t}</b>{d}</div>" for t, d in HOJE)
    cards = "".join(card(c) for c in CONCEITOS)
    recs = "".join(
        f'<article class="{"top" if r.get("rec") else ""}">'
        f'<h4>{r["nome"]}</h4><div class="it">conceitos {r["itens"]}</div>'
        f'<p>{r["txt"]}</p></article>' for r in RECEITAS)
    html = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ELO B2C · 10 possibilidades de design</title>
<style>{CSS}</style></head><body><div class="wrap">
<h1>Dez maneiras de tirar o caixote da linha ELO</h1>
<p class="sub">Croquis de proporção certa — a silhueta sai das cotas reais do
P (boca 180 × 230, altura 130, saída 6°, envelope 204 com a aba). Nenhum destes
desenhos é sólido: o 3D vem depois da escolha.</p>
<div class="regra"><b>A regra que vale para os dez:</b> um molde por tamanho,
uma injeção, duas placas, sem gaveta e sem postiço móvel. Nenhum conceito aqui
pede segunda peça, segunda cor de injeção ou montagem — se pedisse, estaria
fora do briefing.</div>

<h2>O que hoje grita B2B</h2>
<div class="hoje">{hoje}</div>

<h2>As dez possibilidades</h2>
<div class="grid">{cards}</div>

<h2>Três receitas — porque eles combinam</h2>
<div class="rec">{recs}</div>

<h2>A camada que não é geometria</h2>
<div class="fim">
Cor e acabamento não custam molde e mudam mais a foto do que metade desta
lista. <b>Um mesmo molde entrega quantas cores a produção quiser</b> — e o
acabamento pode ser diferente em faces diferentes da mesma cavidade: corpo
fosco, borda e fundo polidos. O que <b>não</b> dá, dentro do briefing, é
bicolor na mesma peça: isso é bi-injeção, e bi-injeção é um segundo molde.
<br><br>
A conta de preço da pesquisa de mercado sustenta a virada: na prateleira
doméstica o nosso próprio 047 sai a <b>R$ 4,58 de fábrica e chega à gôndola
entre R$ 19,99 e R$ 29,15</b>. É essa prateleira que paga textura, raio grande
e grama a mais — a prateleira de loja, que paga R$ 6,20 pelo cesto de 170 g,
não paga.
</div>

<div class="fim">
<b>O que eu preciso de você antes do 3D:</b> escolher entre 1 e 3 conceitos (ou
uma das receitas), e decidir uma coisa que nenhum desenho decide sozinho —
<b>o sistema ELO continua sendo obrigatório na versão B2C?</b> Se continuar, o
conceito 6 cai e o 9 exige remedição. Se a versão B2C puder abrir mão do
acoplamento lateral, o espaço de desenho dobra.
</div>
</div></body></html>"""
    caminho = os.path.join(DEST, "conceitos-b2c.html")
    open(caminho, "w", encoding="utf-8").write(html)
    print(f"gerado {caminho} ({len(html)/1024:.1f} kB)")


if __name__ == "__main__":
    main()
