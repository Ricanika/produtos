# Linha 2 — potes modulares com tampa deslizante de came

**Derivado do Projeto 115 (linha 1, pasta `potes-modulares/`).**
Muda o topo do corpo e a tampa. Corpo, footprint, modularidade e parque de injeção seguem.

Memória de cálculo: `calculo-deslizante.py` (roda sozinho, sem dependência).

---

## 1. O problema que motivou o projeto

A linha 1 fechou com tampa *plug* de vedação radial: um aro de TPE trabalhando contra a
parede interna do pote. Funciona, é lisa, dispensa trava — e serve para mantimento.

Não serve para **sabão líquido**. A tampa com bico precisa de duas coisas que a plug não dá:

1. **Não pode sair se o pote virar.** Vedação radial segura por atrito (5,8 kgf para arrancar
   reto). Isso segura o líquido, mas não segura a tampa contra um tombo com 2,4 L dentro.
2. **Não pode depender do usuário apertar.** É por isso que todo pote retangular hermético do
   mercado tem trava de orelha: vedação axial num retângulo pede força permanente, e alguém
   tem que fazer essa força.

O pedido foi: hermético, que não saia de cabeça para baixo, **sem as travas do mercado**, com
macho na tampa e fêmea no corpo, e que a tampa **deslize** para fechar.

---

## 2. O mecanismo

A tampa não é empurrada para baixo e não rosqueia. Ela pousa deslocada 16 mm e é **empurrada
no sentido do comprimento**. Nesse curso acontecem quatro coisas, nesta ordem:

```
    posição de pouso                        posição travada
    (tampa 14 mm para fora, 2,0 mm alta)    (rente à aba, junta comprimida)

         ┌───────────────┐                    ┌───────────────┐
    ═════╪═══════════════╡  ← folga          ═╪═══════════════╪═  ← junta encostada
    ┌────┴───┐                                ┌───────────────┐
    │  pote  │                                │     pote      │
```

1. **Entram os ganchos.** Seis ganchos em L na face de baixo da tampa (3 por lado longo)
   descem pelas janelas abertas no lábio da aba. É o macho; o lábio rampado é a fêmea.
2. **A came puxa a tampa para baixo.** A came é a **aresta de baixo do lábio descendente da
   aba**, rampada.
   Conforme o gancho avança, a rampa desce e **arrasta a tampa junto** — 2,00 mm em 6 mm
   (18,4°). Esses 2,00 mm não são número livre: são 1,00 mm de folga de pouso + 1,00 mm de
   compressão da junta. A junta só encosta nos últimos 8 mm do curso — durante o deslizamento
   ela não raspa em nada.
3. **Patamar.** Os últimos 10 mm do lábio são planos. É ali que o gancho assenta de face
   inteira (34,0 mm²) em vez de apoiar numa linha.
4. **Clique.** Quatro linguetas flexíveis caem num rebaixo no fim do patamar. **É o detente
   que segura o fecho** — não o atrito da rampa.

Abrir é o mesmo caminho ao contrário: empurra, e **a came levanta a tampa enquanto ela sai**.
Isso quebra a sucção sozinho — não existe o "briga com o pote para tirar a tampa".

### Por que isso resolve o que a trava do mercado não resolve

| | Trava de orelha | Came deslizante |
|---|---|---|
| O que segura na queda | a trava, em **flexão** | o gancho, em **esmagamento/cisalhamento** |
| Como falha | a carga gira a trava e ela **desarma sozinha** (camagem) | não tem como: a fuga do gancho é **perpendicular** à carga |
| Se a peça cansar | abre | continua fechada, só perde o clique e vedação |
| Estética | orelha saliente, dois pontos de quebra | nada aparece: o mecanismo mora embaixo da aba |
| Sinal de "está fechado" | visual da orelha | a tampa fica **rente**; 14 mm para fora = aberta |

O último ponto é de graça e é o melhor deles: **o estado do fecho é a própria posição da
tampa**. Não tem o que interpretar.

---

## 3. As três decisões difíceis (e onde eu quase errei)

### a) Nada pode entrar na boca do pote

Primeira tentativa: manter a bandeja da linha 1 (piso 2,0 mm **abaixo** da borda, formado por
um plug que desce na boca). Não funciona — **qualquer coisa que entre na boca trava o curso
horizontal**. A tampa não teria por onde deslizar.

A bandeja virou um **murete acima do prato**: vão interno 114,4 × 85,9 mm, altura 3,5 mm.
Nada da tampa entra na boca, e o curso de 14 mm fica livre.

Isso custou altura: o passo agora é `altura externa do corpo = 60n − 2,0` em vez de
`60n + 2,0`. **O corpo ficou 4,0 mm mais baixo em cada tamanho**, e a perda pesa mais no pote
pequeno (6,9% da altura do 600 ml contra 1,7% da do 2,4 L).

Foi o que mudou quem manda no footprint: na linha 1 era o 2,4 L; **aqui é o 600 ml**.

### b) Como o passo virou cota externa, o fundo ficou livre

Na linha 1 o fundo tinha que ser 2,0 mm igual nos quatro — era ele que travava o passo.
Aqui o passo é travado pela **altura externa do corpo**, que é uma cota direta e muito mais
fácil de segurar na ferramenta. O fundo saiu da equação.

Então o fundo virou a variável que fecha as quatro capacidades num footprint só: 1,60 mm no
600 ml, 2,50 mm nos outros três — que é exatamente onde o pote grande quer rigidez de qualquer
jeito. Sem fundo falso em nenhum deles.

### c) O comprimento do gancho não é livre

Essa só apareceu ao montar o sólido em 3D — nos cortes 2D ela fica invisível. Para o gancho
assentar **inteiro** no patamar no fim do curso:

```
comprimento do gancho + comprimento da rampa  ≤  curso
```

Com os 6 ganchos de 14 mm e rampa de 10 que eu tinha, dá 24 contra 14 de curso: no fim do curso
o gancho ficaria montado **meio na rampa, meio no patamar**, apoiado numa linha em vez de numa
face — e toda a conta de queda da seção 6 cairia junto.

Virou **gancho de 10 mm com rampa de 6, curso 16**.

### c-bis) O trilho só cabe no trecho reto do lado longo

Essa apareceu ao escrever o fatiador de G-code, e é a mais dura das três. Com canto **R18**, a
aba só alcança a linha do trilho (y = ±50,45) enquanto **|x| ≤ 43,7 mm**. Fora disso ela já
curvou para dentro e **não existe material sobre o gancho**.

Ou seja: o trilho tem **87,4 mm por lado, não 129,4**. Com 3 células:

```
célula 29,13 = janela 11,0 + trilho 18,13     e o trilho precisa de >= curso (16)
```

É isso que fixa o curso em 16 e a rampa em 6. Antes disso eu estava distribuindo as células
sobre os 129,4 mm inteiros — os dois ganchos das pontas simplesmente não teriam trilho.

### d) O sobre-centro na nervura não fecha — e foi onde eu errei primeiro

A ideia inicial era um **sobre-centro na própria came**: uma depressão de 0,8 mm que a tampa
teria de re-descer para voltar. Barreira de energia pura, sem peça extra. Elegante e errada.

O gancho tem **14 mm de topo plano**, e um topo plano **não entra numa depressão mais curta
que ele** — faz ponte. Para o gancho passar da depressão inteira, o curso teria de dobrar para
~29 mm. Rampar o topo do gancho para acompanhar o perfil daria uma cunha de 2,8 mm de altura,
que bate na aba.

Virou **uma função por peça**: a rampa puxa, o detente segura. O patamar plano dos últimos
9 mm é o que dá ao gancho os 30,0 mm² de apoio de face inteira — sem ele o contato seria uma
linha, e toda a conta de queda da seção 6 cairia.

### e) Sabão é lubrificante — não dá para contar com atrito

Numa versão anterior a rampa era de 11,3° e era auto-travante a seco — a conta fechava bonito
na bancada. Só que **µ do PP com filme de sabão cai para ~0,08**, e aí a rampa não trava mais.
O produto *é* um pote de sabão: amarrar o travamento a um coeficiente que o próprio conteúdo
derruba 4× seria projetar para a bancada, não para a pia.

Hoje a rampa é de 18,4° e **não trava nem seca**. Isso deixou de ser problema e virou a ordem
certa: rampa livre significa que fechar e abrir custam pouco, e a retenção fica inteira com o
detente, que é geométrico e funciona com µ = 0.

| µ | ângulo de atrito | vs. rampa de 18,4° |
|---|---|---|
| 0,30 (seco) | 16,7° | **NÃO TRAVA** |
| 0,15 | 8,5° | **NÃO TRAVA** |
| **0,08 (ensaboado)** | **4,6°** | **NÃO TRAVA** |

Por isso quem segura o fecho é o **detente**, que é geométrico e funciona com µ = 0. O atrito
virou coadjuvante — entra na conta do esforço do polegar, não na do travamento. É a diferença entre um projeto que funciona na bancada e um que funciona na pia.

---

## 4. A linha

Footprint **123,4 × 94,9 mm** · canto R18 · saída 0,5°/lado · módulo 60 mm ·
pé embutido 112,4 × 83,9 × 6 mm igual nos quatro

| | Altura ext. | Passo | Fundo | Elev. piso | Parede | Peso corpo | Resina (H 105) |
|---|---|---|---|---|---|---|---|
| 600 ml | 58,0 mm | 60 | 1,60 mm | 0,0 mm | 1,15 mm | 40,7 g | R$ 0,45 |
| 1,2 L | 118,0 mm | 120 | 2,50 mm | 3,2 mm | 1,20 mm | 73,9 g | R$ 0,82 |
| 1,8 L | 178,0 mm | 180 | 2,50 mm | 5,3 mm | 1,30 mm | 105,2 g | R$ 1,16 |
| 2,4 L | 238,0 mm | 240 | 2,50 mm | 5,4 mm | 1,40 mm | 140,3 g | R$ 1,55 |

Empilhamento confere: `600×4` = `1,2 L×2` = `600+600+1,2 L` = `600+1,8 L` = `2,4 L` = 240 mm.

Contra a linha 1: footprint +2,2 mm, corpo 4,0 mm mais baixo, peso do corpo grande +5 g.
É o preço do mecanismo, e é barato.

---

## 5. A tampa

**129,4 × 100,9 mm, rente à aba. 32,4 g em PP RP 141. R$ 0,31 de resina.**

```
prato ............ 2,00 mm, com 3 nervuras de 1,2 × 5,0 mm no piso da bandeja
murete ........... 3,5 mm de altura, 1,5 mm de parede, vão 114,4 × 85,9
saia ............. 7,0 mm × 1,6 mm, por fora do corpo (esconde o mecanismo)
ganchos .......... 6 em L, 10 mm, poste 3,2 mm, asa 3,4 mm sob o lábio
linguetas ........ 4 (2 por lado), 9 × 16 × 1,4 mm, deflexão 0,60 mm, face de saída 35°
lábio de TPE ..... 1,30 mm de espessura, 4,0 mm de balanço, 2,6 g, perímetro 412 mm
curso ............ 16 mm = 6 de rampa (desce 2,00) + 10 de patamar plano
célula ........... 29,13 mm por gancho = janela 11,0 + trilho 18,13,
                   distribuídas nos 87,4 mm de TRECHO RETO do lado longo
```

### A vedação: lábio flexível, não aro esmagado

O que veda é um **lábio de TPE na face de baixo da tampa**, apoiado na face de cima da aba.
É vedação **axial** — a mesma que eu tinha descartado na linha 1. A diferença é que lá o aro
era esmagado entre duas faces rígidas; aqui é um lábio que **flexiona**.

| | Força de fechamento | Consequência |
|---|---|---|
| Aro esmagado axial (linha 1, rev. 2) | **32 kgf permanentes** | precisa de trava; o PP flui embaixo dela |
| **Lábio flexível (aqui)** | **1,26 kgf** | a came segura sem esforço, o PP não flui |

**25× menos força.** É isso que torna a came viável — e é a ordem certa de projetar: primeiro
baixar a força, depois inventar quem a segura. Ao contrário não fecha.

O lábio **abre para dentro do pote**: pressão interna empurra o lábio contra a sede
(auto-energizado). Pressão de contato 67 kPa contra 2,4 kPa de coluna de sabão no 2,4 L
invertido — **de cabeça para baixo a vedação melhora, não piora**.

### A came é o lábio da borda, não a aba

A linha 1 já tinha um **lábio descendente de 3,5 mm** na ponta da aba — ele é o que fecha a
seção em U e dá à borda 235× a inércia da parede simples. Aqui ele ganha uma segunda função:
engrossado de 1,2 para **2,4 mm na zona de trabalho, a aresta de baixo dele é a rampa**.

Engrossar a **aba** para fazer a rampa daria rechupe **exatamente na face que veda**. O lábio
é saia escondida — rechupe nele não importa. A aba fica com 1,6 mm uniformes.

O poste do gancho desce **por fora** do lábio e a asa volta para dentro, por baixo dele. Com
isso o gancho inteiro cabe num corte transversal só, e a saia de 7 mm da tampa esconde tudo.

Apoio por gancho: **34,0 mm² (10 × 3,4)**.

### O batente que fecha o passo

O prato **encosta na aba** — o lábio de TPE mora numa canaleta na face de baixo do prato e
desce num rebaixo da aba. Quando o prato bate, a compressão é exatamente 1,00 mm. Esse batente
rígido faz três coisas: define a vedação sem depender de tolerância de came, carrega a pilha, e
é ele que faz o passo dar **58 + 2 = 60 mm** exatos. Se a tampa apoiasse *sobre* o lábio, o
passo daria 61,2 mm e a modularidade cairia.

---

## 6. As contas que decidem o produto

### Esforço do polegar

| µ | Detente | Arrasto da junta | Total |
|---|---|---|---|
| 0,08 (ensaboado) | 26,9 N | 1,0 N | **2,8 kgf** |
| 0,15 | 30,9 N | 1,9 N | **3,3 kgf** |
| 0,30 (seco) | 41,2 N | 3,7 N | **4,6 kgf** |

Janela alvo 2 a 4 kgf — seco fica 0,6 kgf acima, e é justamente o que o try-out acerta. Abaixo disso abre na bolsa; acima, o usuário acha que quebrou.
**A interferência da lingueta é a cota que se tira aço no try-out** até o toque ficar certo —
e nenhuma outra cota do conjunto se mexe junto. Deformação na raiz da lingueta: 1,56%
(PP aguenta ~2% em ciclagem).

**Degradação segura:** se o detente cansar, a tampa **não sai** — os ganchos são geométricos.
Perde-se o clique e um pouco de vedação, não o fecho. Trava de mercado que quebra perde tudo
de uma vez.

### Queda com o 2,4 L cheio de sabão (2,61 kg), em cima da tampa

| Altura | Parada | Força | Por gancho | Apoio | Poste | |
|---|---|---|---|---|---|---|
| 0,50 m | 8 mm | 1.602 N | 267 N | 7,9 MPa | 8,3 MPa | OK |
| 0,75 m | 8 mm | 2.402 N | 400 N | 11,8 MPa | 12,5 MPa | OK |
| 1,00 m | 8 mm | 3.203 N | 534 N | 15,7 MPa | 16,7 MPa | OK |
| 1,00 m | 5 mm | 5.125 N | 854 N | 25,1 MPa | 26,7 MPa | OK |

Limite do PP: 30 MPa. Passar de 8 para 6 dentes tirou 25% dos apoios: foi o que obrigou o
lábio a engrossar de 3,0 para 3,4 mm e o poste de 2,6 para 3,2 mm. A 3,2 mm o poste já pede
alma vazada ou nervura no molde, senão rechupa na saia. Ainda assim é caso a **medir**.

### Fluência, que é o que mata vedação de PP a longo prazo

Em repouso cada gancho carrega 2,1 N → **0,061 MPa** de esmagamento. A essa tensão o PP não
flui. Com os 32 kgf da vedação axial rígida seriam ~1,6 MPa e a junta perderia contato em
poucos meses. **Foi por isso que o lábio flexível teve de vir antes da came.**

### A borda entre ganchos

Ganchos a cada 29 mm. A seção em U da aba dá I = 54 mm⁴/mm (parede simples de 1,40 mm daria
0,23 — **235×**). Levantamento máximo no meio do vão: **4 µm** contra 1.000 µm de deflexão do
lábio. A junta acompanha de sobra; não há por onde vazar entre ganchos.

---

## 7. Molde — onde a complexidade foi parar, e por quê

**Corpo: extração 100% reta, zero gaveta, nos quatro tamanhos.**
O canal da aba abre para baixo, as nervuras da came penduram para baixo, as janelas de entrada
são interrupções nessas nervuras. Toda superfície é vista de cima ou de fora/baixo.

**Tampa: 2 gavetas laterais** (uma por lado longo), que formam as asas dos 8 ganchos.

Essa alocação é deliberada. São **quatro moldes de corpo** — fundos, caros, USD 25–40 mil cada
— e **um molde de tampa** raso e barato. Pôr as gavetas na tampa custa ~USD 3–4 mil uma vez;
pôr no corpo custaria oito gavetas espalhadas por quatro ferramentas.

A alternativa sem gaveta nenhuma seria fazer os ganchos em lingueta flexível, que desmoldam
por arranque. Descartada: lingueta que flexiona para desmoldar também flexiona em serviço, e
o gancho é justamente o que não pode ceder. **Gancho rígido, gaveta na tampa.**

### Injeção — o parque não muda

| | A proj. | Fecham. 2 cav | Máquina | Curso | L/t |
|---|---|---|---|---|---|
| 600 ml | 135 cm² | 125 t | 200 t | 128 mm | 104 |
| 1,2 L | 135 cm² | 134 t | 200 t | 260 mm | 150 |
| 1,8 L | 135 cm² | 143 t | 250 t | 392 mm | 184 |
| 2,4 L | 135 cm² | 149 t | 380 t | 524 mm | 214 |
| tampa | 135 cm² | 238 t (4 cav) | 250/280 t | — | — |

Mesmas máquinas da linha 1. O **L/t 214 do 2,4 L** continua no limite: câmara quente com 2
pontos ou parede de 1,5 mm — decidir no Moldflow, igual à linha 1. **INJ 32 (380 t)**, que
estava parada, segue como candidata ao try-out.

---

## 8. A tampa dosadora — a que motivou tudo

Mesmo casco, mesma came, mesmos ganchos, mesmo lábio. Muda só o miolo do prato:

1. Furo de vazão **26 × 16 mm** no canto, encostado no murete.
2. Entalhe de 14 mm no murete — o canto R18 já faz a curva, não se molda bico.
3. **Lábio de corte de 0,4 mm** na aresta de saída: quebra o filme de sabão, a gota se solta
   em vez de escorrer pela parede.
4. Caimento de 3° no piso para o furo: o que respinga volta para dentro pelo mesmo furo.
5. Tampinha com dobradiça viva e **bujão cônico** (6° de conicidade, 0,15 mm de interferência
   em 3 mm de engate).

De cabeça para baixo, quem veda o furo é o bujão, e a carga nele é ridícula — **1,00 N
(0,10 kgf) no 2,4 L**. Um bujão cônico de PP segura isso com folga.

**Respiro:** 2,4 L saindo por um furo de 26 × 16 vai gluglejar. Avaliar respiro de 6 mm no
canto oposto sob a mesma dobradiça. **Medir no protótipo antes de decidir** — sabão líquido é
viscoso e pode não precisar.

---

## 9. Patente — fazer a busca antes de mostrar para alguém

Tampa deslizante existe (caixa de pão, estojo, alguns bentôs). Fecho por came existe. Junta de
lábio existe. **O que parece não existir é a combinação**: retangular, rente, sem saliência,
com a came gerando a carga de vedação no próprio curso de fechamento e a retenção vertical
saindo de ganchos geométricos, sem depender de atrito nem de trava saliente.

Isso **não é uma afirmação de que é inédito** — é uma hipótese que precisa de busca:

- **INPI** e **Espacenet**, classificações **B65D 43/20** (tampas deslizantes),
  **B65D 45/16** (fechos por came) e **B65D 53/02** (juntas).
- O perfil é de **Modelo de Utilidade** (15 anos, mais barato, exige disposição nova com
  melhoria funcional) mais do que de patente de invenção.
- **Fazer a busca antes de qualquer divulgação, feira ou catálogo.** Divulgação prévia derruba
  a novidade — no Brasil há período de graça de 12 meses, na Europa não há.

---

## 10. O que fica aberto

1. **Busca de anterioridade** (item 9), antes de divulgar.
2. **Atrito real PP/PP com filme de sabão** — medir, não estimar. Toda a janela do detente
   depende disso.
3. **Retenção do lábio de TPE** na canaleta da tampa: 500 aberturas, ver se migra.
4. **Estanqueidade**: água colorida, 24 h, deitado e invertido, com e sem ciclagem térmica
   (geladeira → bancada). Só depois disso se fala em promessa de vedação na embalagem.
5. **Queda de 0,75 m** com o 2,4 L cheio, sobre a tampa e sobre o canto.
6. **Fluência**: 90 dias fechado a 40 °C, medir a deflexão residual do lábio.
7. **Protótipo impresso** do 600 ml + tampa: o curso da came e o clique só se avaliam na mão.
8. Recotar o **TPE Karinprene 45** (CODPROD 997, sem compra há 4 anos) — agora como perfil
   extrudado, não como aro moldado.

---

## 11. Herdado da linha 1, sem repetir aqui

Material (PP H 105 no corpo, RP 141 na tampa, e por que PE foi descartado), parque de 46
injetoras e a armadilha do `TPRCAP.DESCRICAO`, Projeto 115 no ERP com molde 115/1 já orçado em
USD 47.100, ordem de grandeza de USD 140–190 mil de ferramental, histórico de vendas da linha
modular. Está tudo em `../potes-modulares/README.md` e vale igual.

**Ferramental desta linha:** 4 moldes de corpo + 2 de tampa (padrão e dosadora, com 2 gavetas
cada) + o perfil extrudado de TPE = **6 ferramentas de injeção + 1 matriz de extrusão**.
Uma a menos que a linha 1, porque o aro moldado virou perfil extrudado.

---

## 12. Arquivos

| Arquivo | O que é |
|---|---|
| `README.md` | este estudo |
| `calculo-deslizante.py` | memória de cálculo: linha, vedação, came, detente, ganchos, queda, injeção |
| `mecanismo-came.html` | cópia da página publicada: dois cortes interativos do curso de fechamento |
| `modelo-3d.html` | cópia da página publicada: modelo 3D orbitável, com corte e a sequência animada |
| `verifica-modelo-3d.js` | roda o motor do modelo 3D fora do navegador e confere que todos os estados desenham dentro do quadro |
| `gera-gcode.py` | fatiador paramétrico → G-code de FDM, direto da geometria (não de STL) |
| `gcode/corpo-600.gcode` | corpo de 600 ml, 289 camadas, ~88 g, ~7,8 h |
| `gcode/tampa.gcode` | tampa, 62 camadas, ~60 g, ~5,4 h |

Páginas publicadas:
- Modelo 3D: https://claude.ai/artifact/26MfzdTdy4EnPUfbYnEejP
- Cortes 2D do mecanismo: https://claude.ai/artifact/6MLM4LeKMsvPn62wexfApX

**O modelo 3D não usa WebGL.** A primeira versão usava Three.js e ficava em branco em qualquer
navegador sem WebGL — sem nem avisar. Hoje o desenho é Canvas 2D com projeção própria,
ordenação por profundidade e corte de polígono no plano; não depende de CDN nem de placa de
vídeo. `verifica-modelo-3d.js` roda esse motor no Node com um canvas falso e confere, estado a
estado, quantas faces são pintadas e se caem dentro do quadro.

O cálculo roda sozinho: `python3 calculo-deslizante.py`. A integração de volume usa Simpson de
3 pontos, que é **exata** aqui (a seção é quadrática em z), não aproximação numérica.
