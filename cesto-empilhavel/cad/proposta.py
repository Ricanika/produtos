import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
import numpy as np

TINTA, LINHA = "#1f2328", "#3d444d"
PECA, PECA2 = "#e8e2d9", "#cfd6dd"
NOVO, CINZA = "#c2410c", "#6b7280"
FUNDO = "#fbfaf8"

fig = plt.figure(figsize=(16, 11.6), facecolor=FUNDO)
fig.text(0.5, 0.975, "Cesto organizador empilhável — refino do pé e acoplamento lateral",
         ha="center", va="top", fontsize=19.5, color=TINTA, weight="bold")
fig.text(0.5, 0.947, "Proposta para validação · 17/09/2026 · cotas em mm · parede de 1,4 mm",
         ha="center", va="top", fontsize=11.5, color=LINHA)

def eixo(rect, num, titulo, sub=""):
    ax = fig.add_axes(rect); ax.set_facecolor("white")
    for s in ax.spines.values():
        s.set_color("#e3e0da"); s.set_linewidth(1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.text(0.0, 1.085, f"{num} · {titulo}", transform=ax.transAxes,
            fontsize=13, color=TINTA, weight="bold", va="bottom")
    if sub:
        ax.text(0.0, 1.022, sub, transform=ax.transAxes, fontsize=9.6,
                color=CINZA, va="bottom")
    return ax

def cota(ax, p0, p1, txt, d=0, vert=False, fs=9):
    x0,y0 = p0; x1,y1 = p1
    if vert:
        x = x0+d
        ax.annotate("",(x,y0),(x,y1),arrowprops=dict(arrowstyle="<->",color=NOVO,lw=1.1,shrinkA=0,shrinkB=0))
        ax.plot([x0,x],[y0,y0],color=NOVO,lw=.6); ax.plot([x1,x],[y1,y1],color=NOVO,lw=.6)
        ax.text(x+(2 if d>=0 else -2),(y0+y1)/2,txt,fontsize=fs,color=NOVO,
                ha="left" if d>=0 else "right",va="center")
    else:
        y = y0+d
        ax.annotate("",(x0,y),(x1,y),arrowprops=dict(arrowstyle="<->",color=NOVO,lw=1.1,shrinkA=0,shrinkB=0))
        ax.plot([x0,x0],[y0,y],color=NOVO,lw=.6); ax.plot([x1,x1],[y1,y],color=NOVO,lw=.6)
        ax.text((x0+x1)/2,y+(2 if d>=0 else -2),txt,fontsize=fs,color=NOVO,
                ha="center",va="bottom" if d>=0 else "top")

def nota(ax, xy, txt, xytext, cor=TINTA, fs=9.2, ha="left"):
    ax.annotate(txt, xy=xy, xytext=xytext, fontsize=fs, color=cor, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", color="#9aa0a6", lw=.9,
                                connectionstyle="arc3,rad=0.15"))

# ---------------------------- 1 · PE ATUAL --------------------------------
ax = eixo([0.045,0.565,0.255,0.315], "1", "Pé atual", "quatro blocos de canto")
ax.set_xlim(-6,80); ax.set_ylim(-20,44)
ax.add_patch(Polygon([(6,0),(7.6,0),(9.6,40),(8,40)],closed=True,facecolor=PECA,edgecolor=LINHA,lw=1.4))
ax.add_patch(Rectangle((7.6,0),60,2.0,facecolor=PECA,edgecolor=LINHA,lw=1.4))
ax.add_patch(Rectangle((0,0),12,6,facecolor="#f8ddcd",edgecolor=NOVO,lw=1.6))
ax.plot([-6,80],[0,0],color="#b9bec4",lw=1,ls=(0,(6,4)))
ax.text(76,2.6,"piso",fontsize=8.5,color="#9aa0a6",ha="right")
nota(ax,(2,6.5),"bloco 32 × 32 × 6:\naparece na lateral e\nquebra a linha da parede",(18,26),NOVO)
cota(ax,(0,0),(12,0),"32",d=-9)

# ---------------------------- 2 · PE PROPOSTO -----------------------------
ax = eixo([0.345,0.565,0.29,0.315], "2", "Pé proposto — saia contínua",
          "a parede desce até o piso; o apoio some por baixo")
ax.set_xlim(-8,92); ax.set_ylim(-22,44)
ax.add_patch(Polygon([(10,0),(11.4,0),(13.4,40),(12,40)],closed=True,facecolor=PECA,edgecolor=LINHA,lw=1.4))
ax.add_patch(Rectangle((11.4,6),56,2.0,facecolor=PECA,edgecolor=LINHA,lw=1.4))
ax.add_patch(Rectangle((10,0),1.4,6,facecolor="#f8ddcd",edgecolor=NOVO,lw=1.8))
ax.add_patch(Polygon([(3.4,-20),(4.8,-20),(7.0,-2.0),(2.0,-2.0)],closed=True,facecolor=PECA2,edgecolor=LINHA,lw=1.3))
ax.add_patch(Rectangle((4.8,-5.6),8.0,3.6,facecolor="#dbe3ea",edgecolor=LINHA,lw=1.2))
ax.plot([-8,92],[-20,-20],color="#b9bec4",lw=1,ls=(0,(6,4)))
nota(ax,(10.8,3),"saia: a parede continua\n6 mm abaixo da chapa —\né ela que toca o piso",(24,30),NOVO)
nota(ax,(12.2,-3.8),"berço no rim da peça de baixo:\n4 orelhas internas 30 × 9 × 5,\ninvisíveis de fora",(28,-14))
cota(ax,(10,0),(10,6),"6",d=-6,vert=True)
ax.text(88,42,"de fora: só a parede\nencontrando o piso",fontsize=9.2,color=NOVO,
        ha="right",va="top",style="italic")

# ---------------------------- 3 · ACOPLAMENTO -----------------------------
ax = eixo([0.685,0.565,0.27,0.315], "3", "Acoplamento — seção horizontal",
          "engrossa para dentro; face externa no plano")
ax.set_xlim(-6,66); ax.set_ylim(-30,34)
ax.add_patch(Rectangle((8,-22),3.0,44,facecolor=PECA,edgecolor=LINHA,lw=1.4))
ax.add_patch(Rectangle((11.0,-9),3.0,26,facecolor="#efe9df",edgecolor=LINHA,lw=1.0))
ax.add_patch(Rectangle((5.0,-5),3.0,18,facecolor="white",edgecolor=NOVO,lw=1.3))
ax.add_patch(Polygon([(5.0,-1.0),(8.0,-2.6),(8.0,10.6),(5.0,9.0)],closed=True,
                     facecolor="#f8ddcd",edgecolor=NOVO,lw=1.7))
ax.text(9.5,30,"peça A",fontsize=10,color=TINTA,ha="center",weight="bold")
ax.add_patch(Rectangle((46,-22),3.0,44,facecolor=PECA2,edgecolor=LINHA,lw=1.4))
ax.add_patch(Rectangle((49,-9),3.0,26,facecolor="#e2e9ef",edgecolor=LINHA,lw=1.0))
ax.add_patch(Polygon([(46,-1.0),(49,-2.6),(49,10.6),(46,9.0)],closed=True,
                     facecolor="white",edgecolor=NOVO,lw=1.7))
ax.text(47.5,30,"peça B",fontsize=10,color=TINTA,ha="center",weight="bold")
ax.annotate("",(22,4),(40,4),arrowprops=dict(arrowstyle="->",color=NOVO,lw=2))
ax.text(31,8,"encaixa\ndeslizando",fontsize=9.2,color=NOVO,ha="center")
ax.text(2,-16,"MACHO\nponta rente à face externa",fontsize=8.6,color=NOVO,ha="left",va="top")
ax.text(64,-16,"FÊMEA\nbolso com ressalto",fontsize=8.6,color=NOVO,ha="right",va="top")
ax.text(30,24,"parede engrossa\n3 mm PARA DENTRO",fontsize=8.6,color=TINTA,ha="center",va="top")
cota(ax,(5.0,-5),(8.0,-5),"3",d=-4)

# ---------------------------- 4 · LATERAIS --------------------------------
ax = eixo([0.045,0.10,0.50,0.345], "4", "Onde ficam os pares",
          "hermafrodita: qualquer peça acopla em qualquer peça, dos dois lados")
ax.set_xlim(-20,470); ax.set_ylim(-34,166)
def silhueta(dx):
    ax.add_patch(Polygon([(dx,0),(dx,130),(dx+148,130),(dx+200,78),(dx+200,52),(dx+148,0)],
                 closed=True,facecolor=PECA,edgecolor=LINHA,lw=1.6))
    ax.add_patch(Rectangle((dx,0),200,6,facecolor="#f8ddcd",edgecolor=NOVO,lw=1.0))
def marca(dx,x,y,tipo):
    ax.add_patch(Rectangle((dx+x,y),50,17,facecolor="white",edgecolor=NOVO,lw=1.4))
    if tipo=="M":
        ax.add_patch(Rectangle((dx+x+7,y+4),36,9,facecolor="#f8ddcd",edgecolor=NOVO,lw=1.1))
    ax.text(dx+x+25,y+8.5,"macho" if tipo=="M" else "fêmea",fontsize=8.8,color=NOVO,
            ha="center",va="center",weight="bold")
silhueta(0);   marca(0,112,84,"M");  marca(0,30,84,"F")
silhueta(250); marca(250,112,84,"F"); marca(250,30,84,"M")
ax.text(100,158,"LATERAL DIREITA",fontsize=10.5,color=TINTA,ha="center",weight="bold")
ax.text(350,158,"LATERAL ESQUERDA",fontsize=10.5,color=TINTA,ha="center",weight="bold")
ax.text(100,-16,"macho na frente · fêmea atrás",fontsize=9.4,color=NOVO,ha="center")
ax.text(350,-16,"fêmea na frente · macho atrás",fontsize=9.4,color=NOVO,ha="center")
ax.text(225,152,"rebaixo 50 × 17 × 3:\nde fora lê como linha\nde painel, não ferragem",
        fontsize=8.8,color=TINTA,ha="center",va="top")
ax.text(4,-28,"saia do pé corre no perímetro todo",fontsize=8.8,color=NOVO,ha="left")

# ---------------------------- 5 · PLANTA ----------------------------------
ax = eixo([0.585,0.265,0.37,0.18], "5", "Duas peças acopladas — planta")
ax.set_xlim(-14,446); ax.set_ylim(-14,214)
for dx,cor,nm in [(0,PECA,"A"),(215,PECA2,"B")]:
    ax.add_patch(Rectangle((dx,0),215,200,facecolor=cor,edgecolor=LINHA,lw=1.6))
    ax.text(dx+107,186,f"peça {nm}",fontsize=10,color=TINTA,ha="center",weight="bold")
ax.plot([215,215],[0,200],color=NOVO,lw=2.4)
for y,t in [(140,"M → F"),(56,"F ← M")]:
    ax.add_patch(Rectangle((198,y-11),34,22,facecolor="#f8ddcd",edgecolor=NOVO,lw=1.4))
    ax.text(215,y,t,fontsize=8.6,color=NOVO,ha="center",va="center",weight="bold")
ax.text(310,140,"macho de A dentro\nda fêmea de B",fontsize=8.8,color=TINTA,ha="left",va="center")
ax.text(310,56,"fêmea de A recebe\no macho de B",fontsize=8.8,color=TINTA,ha="left",va="center")
ax.text(107,14,"sozinha, a lateral lê LISA",fontsize=9.2,color=NOVO,ha="center",style="italic")

# ---------------------------- PESO ----------------------------------------
bx = fig.add_axes([0.585,0.10,0.37,0.135]); bx.axis("off")
bx.set_xlim(0,1); bx.set_ylim(0,1)
bx.add_patch(Rectangle((0,0),1,1,transform=bx.transAxes,facecolor="#fdf6f1",
                       edgecolor="#f0d3c2",lw=1.3))
bx.text(0.035,0.90,"PESO CALCULADO",fontsize=11,color=NOVO,weight="bold",va="top")
linhas = [("Peça atual","155,4 g",TINTA,"bold"),
          ("− 4 blocos de canto (32×32×6, ocos)","− 5,2 g",CINZA,"normal"),
          ("+ saia do pé (perímetro 766 × 6 × 1,4)","+ 5,8 g",CINZA,"normal"),
          ("+ 4 berços no rim (30×9×5)","+ 4,9 g",CINZA,"normal"),
          ("+ acoplamento (4 engrossamentos − 4 bolsos)","+ 3,6 g",CINZA,"normal"),
          ("Peça proposta","164,5 g",NOVO,"bold")]
for i,(k,v,c,w) in enumerate(linhas):
    y = 0.74 - i*0.117
    bx.text(0.035,y,k,fontsize=8.8,color=c,va="top",weight=w)
    bx.text(0.965,y,v,fontsize=8.8,color=c,va="top",ha="right",weight=w)
bx.plot([0.035,0.965],[0.115,0.115],color="#f0d3c2",lw=1)
bx.text(0.035,0.085,"capacidade 4,50 → 4,29 L · a saia consome 6 mm de fundo",
        fontsize=8.4,color=CINZA,va="top")

fig.savefig("/home/user/produtos/cesto-empilhavel/cad/proposta-pe-acoplamento.png",
            dpi=135,facecolor=FUNDO)
print("ok")
