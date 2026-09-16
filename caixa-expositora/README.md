# Caixa Expositora Tri-Kit

**Status:** projeto de embalagem · **Revisão 1** · 16/09/2026
**Escopo:** uma única caixa de papelão ondulado que transporta e expõe três kits diferentes

Caixa de transporte que vira expositor de chão no ponto de venda. Picote na frente subindo até o
topo: destaca-se o painel frontal inteiro e dobra-se a aba superior traseira 180° para cima,
virando a **testeira** com a arte da marca.

**Medidas internas recomendadas: 560 × 530 × 720 mm** (frente × profundidade × altura) ·
externo 574 × 544 × 734 mm · onda BC 7 mm · chapa 2248 × 1268 mm.

Todos os números vêm de `calculo-expositora.py` e os desenhos de `gera-desenhos.py`.

---

## 1. Veredito

| Requisito | Situação |
|---|---|
| Uma caixa só para os 3 kits | **Viável** — os três fecham no mesmo footprint |
| Picote frontal até o topo | **Viável**, desde que as abas superiores laterais virem aro de travamento (seção 5) |
| Tampa que dobra e vira expositor | **Viável** — aba superior traseira de 266 mm dobrada 180° = testeira |
| Profundidade interna de **520 mm** | **Corrigir para 530 mm** — dois kits retangulares dão 2 × 260 = 520 exatos, folga zero (seção 3.1) |
| Altura interna de **720 mm** | Funciona. **760 mm rende +10% de kits** pelo mesmo custo de chapa (seção 3.2) |
| Resistência com a frente destacada | **Folgada** com onda BC: 419 kgf contra 300 kgf exigidos (seção 4) |
| Paletização | **Ponto fraco herdado da medida**: 2 caixas por camada no PBR, 52% do palete (seção 8) |
| Peso do kit | **Bloqueio de dado** — a carga de projeto de 30 kg/caixa é estimativa, precisa ser confirmada |

---

## 2. Os três kits

| Kit | Dimensões (cm) | Volume | Por camada | Camadas | Total na caixa |
|---|---|---|---|---|---|
| A — quadrado | 23,5 × 25,5 × 10,5 | 6,29 L | 4 (2 × 2) | 6 | **24 kits** |
| B — retangular alto | 18 × 26 × 14 | 6,55 L | 6 (3 × 2) | 5 | **30 kits** |
| C — retangular baixo | 18 × 26 × 8 | 3,74 L | 6 (3 × 2) | 8 | **48 kits** |

Arranjo na camada — ver `arranjos.svg`:

- **Kit A:** 25,5 cm no eixo da frente (2 × 25,5 = 51, folga 5 cm) e 23,5 cm na profundidade
  (2 × 23,5 = 47, folga 6 cm). Folgas equilibradas; a orientação invertida daria folga de 9 cm num
  eixo só e o kit escorregaria.
- **Kits B e C:** 18 cm na frente (3 × 18 = 54, folga 2 cm) e 26 cm na profundidade
  (2 × 26 = 52, folga 1 cm). É esse arranjo que dimensiona a caixa.

Ocupação volumétrica: 71% (A), 92% (B), 84% (C).

---

## 3. As duas correções de medida

### 3.1 Profundidade 520 → 530 mm (obrigatória)

Os kits B e C têm 26 cm. Só cabem dois lado a lado, e **2 × 26 = 52 cm exatos**. Com profundidade
interna de 520 mm a folga é zero — e caixa de kit em papelão barriga 2 a 3 mm por peça depois de
paletizada. Na prática o segundo kit não entra, ou entra forçado e deforma a caixa expositora.

Se os 520 mm forem medida **externa**, o interno cai para 506 mm e o arranjo simplesmente não existe.

**530 mm internos** resolvem: 10 mm de folga no eixo crítico, 6 mm de custo de chapa. É a única cota
do briefing que não pode ficar como está.

### 3.2 Altura 720 → 760 mm (opcional, mas paga bem)

A altura da caixa só rende kit em degraus — cada camada é indivisível. Varrendo a altura interna
(com 3 mm de barriga por camada empilhada):

| Altura interna | Kit A | Kit B | Kit C | Total de kits | Vazio médio |
|---|---|---|---|---|---|
| 700 mm | 6 cam / 24 | 4 cam / 24 | 8 cam / 48 | 96 | 9,0 cm |
| **720 mm (briefing)** | 6 cam / 24 | 5 cam / 30 | 8 cam / 48 | **102** | 6,3 cm |
| 740 mm | 6 cam / 24 | 5 cam / 30 | 8 cam / 48 | 102 | 8,3 cm |
| 750 mm | 6 cam / 24 | 5 cam / 30 | 9 cam / 54 | 108 | 6,7 cm |
| **760 mm** | **7 cam / 28** | 5 cam / 30 | **9 cam / 54** | **112** | **4,2 cm** |
| 780 mm | 7 cam / 28 | 5 cam / 30 | 9 cam / 54 | 112 | 6,2 cm |

**760 mm é o ponto ótimo**: +4 kits no A (+17%), +6 no C (+12,5%), e o menor vazio médio da faixa.
Custa 40 mm a mais de largura de chapa (~3%) e sobe o externo para 774 mm — ainda dá duas caixas
empilhadas por palete dentro de 1,62 m.

De 740 a 780 mm não muda nada em relação a 760: quem escolher a altura por outro critério (gôndola,
caminhão) deve escolher **760 ou 720**, nunca um valor no meio.

### 3.3 Calço de fundo — uma caixa, três alturas de carga

Como as camadas são indivisíveis, cada kit para numa altura diferente e a caixa fica com um vazio no
topo. Um **calço de fundo em papelão** empurra a carga para cima e faz o expositor parecer cheio nos
três casos (caixa interna de 720 mm):

| Kit | Camadas | Carga | Calço |
|---|---|---|---|
| A — quadrado | 6 | 630 mm | **90 mm** |
| B — retangular alto | 5 | 700 mm | **20 mm** |
| C — retangular baixo | 8 | 640 mm | **80 mm** |

É um berço simples de onda C dobrada, sem faca dedicada. Sem ele, o kit A fica 9 cm abaixo da borda
e o expositor lê como "já acabou o produto".

---

## 4. Papelão e resistência

**Onda BC (dupla parede), 7 mm, canaletas VERTICAIS.** A composição da canaleta vertical não é
detalhe de acabamento: é ela que sustenta os 720 mm de altura em compressão.

Composição sugerida: **175 K / miolo 130 / 150 / miolo 130 / 175 K**, ECT ≥ 10 kgf/cm.

BCT por McKee (`BCT = 5,87 × ECT × √(t × perímetro)`, perímetro 218 cm, t 0,7 cm):

| Papel | ECT | BCT fechada | BCT com a frente destacada (−45%) |
|---|---|---|---|
| Onda C simples K180/K180 | 5,2 | 377 kgf | 207 kgf |
| Onda C simples K200/K200 | 6,8 | 493 kgf | 271 kgf |
| **Onda BC dupla 175/150/175** | **10,5** | **761 kgf** | **419 kgf** |
| Onda BC dupla K200/K200 | 13,0 | 943 kgf | 518 kgf |

Carga de projeto: 3 caixas empilhadas × 30 kg = **60 kg** na de baixo. Com fator 5 (6 meses de
estoque, umidade relativa 80%) exige-se **300 kgf**; com fator 7, 420 kgf.

O derate de 45% é o custo de destacar a frente: com um painel a menos, a caixa perde perto de metade
da capacidade de compressão. **Onda C simples não fecha a conta** depois do destaque — é por isso que
a especificação é BC e não C.

Peso estimado da caixa vazia: **2,0 kg** (2,85 m² de chapa a ~700 g/m²).

---

## 5. Construção

Peça única, emenda colada, **abas superiores desiguais**. Ver `faca-expositora.svg`.

Painéis na chapa, da esquerda para a direita:

| | Largura |
|---|---|
| Aba de cola | 40 mm |
| Traseira | 567 mm |
| Lateral | 537 mm |
| Frente | 567 mm |
| Lateral | 537 mm |
| **Chapa** | **2248 mm** |

| Abas | Altura |
|---|---|
| Inferiores das laterais (camada interna, se encontram na frente) | 281,5 mm |
| Inferiores da frente/traseira (camada externa, se encontram na profundidade) | 266,5 mm |
| Superiores da frente/traseira (fecham o transporte) | 266,5 mm |
| Superiores das laterais (**aro de travamento**) | 100 mm |
| **Chapa** | **1268 mm** |

**O fundo é total** — as duas camadas se encontram, cobertura dupla. É onde a caixa apanha: 30 kg de
kit sobre uma caixa de 0,3 m² de base.

**O aro de travamento é o que viabiliza o picote até o topo.** Quando a frente sai, a caixa deixa de
ser um tubo fechado e as duas laterais tendem a abrir. As abas superiores laterais de 100 mm dobradas
para dentro amarram uma lateral na outra e seguram a geometria. Sem elas o expositor barriga sob
carga. Elas ficam a 100 mm de cada lado, deixando 330 mm livres de abertura superior — folgado para
passar qualquer um dos três kits (o maior tem 260 mm).

---

## 6. Geometria do picote

Cotas medidas a partir do vinco inferior da frente (painel de 567 × 720 mm):

| Elemento | Cota |
|---|---|
| Altura da frente que fica (muro de retenção), nas quinas | **240 mm** |
| Flecha do arco no centro | **40 mm** (frente de 200 mm no centro) |
| Raio do arco | **R 1025 mm** |
| Recuo do picote vertical para dentro da lateral | **15 mm** |
| Picote vertical | de 240 mm até o vinco superior (o "até o topo" do briefing) |
| Dedeira de início do destaque, corte real | **Ø 35 mm**, centrada no ponto baixo do arco |
| Tipo de picote | **zíper** (dupla linha desencontrada) — obrigatório em onda dupla |

**Por que 240 mm.** É a altura que retém a pilha depois que a frente sai, e casa com os três kits:
2 camadas do kit A (210 mm), 3 camadas do kit C (240 mm exatos), e mais de meia camada do kit B
(140 mm + 100 de sobra). Abaixo de 200 mm o produto de cima empurra a pilha para fora; acima de
280 mm o kit fica escondido e a caixa deixa de vender.

**Por que o picote vertical entra 15 mm na lateral** em vez de correr sobre o vinco da quina: picote
em cima de vinco rasga torto e deixa fiapo. Correndo em área plana, 15 mm para dentro, o destaque sai
reto. O que sai é a frente inteira + 15 mm de cada lateral + a aba superior da frente.

**Picote em zíper, não perfuração simples.** Em onda BC a linha de corte simples atravessa o miolo
sem controle e o rasgo foge. O zíper força o caminho.

---

## 7. Conversão em expositor

Ver `conversao.svg`. Cinco movimentos, sem ferramenta:

1. Abrir as abas superiores (fita ou hot-melt).
2. Enfiar o dedo na dedeira Ø 35 e puxar a frente para cima pelo picote. Sai o painel inteiro com a
   aba superior da frente junto.
3. Dobrar as duas abas superiores laterais **para dentro** — é o aro de travamento.
4. Dobrar a aba superior traseira **180° para cima**: vira a testeira de 266 mm com a arte da marca.
5. Encaixar o cartaz promocional nas duas fendas de 60 × 4 mm da testeira.

O vinco da testeira dobra ao contrário do fechamento de transporte. Pedir ao fornecedor **vinco
reverso** nessa linha, senão ela racha na dobra.

---

## 8. Paletização

Externo 574 × 544 mm (com a correção de profundidade).

| Palete | Por camada | Aproveitamento |
|---|---|---|
| PBR 100 × 120 cm | 2 caixas | 52% |
| Meio-palete 60 × 80 cm | 1 caixa | serve como display de chão pronto |

Duas caixas empilhadas: 2 × 734 + 145 de palete = **1613 mm**. Quatro caixas por PBR.

**O aproveitamento de 52% é herdado das medidas, não da construção.** Para caber 4 no PBR o externo
teria que fechar em 500 × 600 mm, o que baixa o interno para 486 mm e quebra o arranjo 2 × 260 dos
kits B e C — passaria de 6 para 4 kits por camada, −33%. **O footprint 530 × 560 está certo para os
kits; o custo é o palete.** Se o frete for o gargalo, o caminho é meio-palete, não mudar a caixa.

---

## 9. Checklist para o fornecedor

- [ ] Onda **BC dupla**, 7 mm, **canaletas verticais**, ECT ≥ 10 kgf/cm
- [ ] Chapa **2248 × 1268 mm** — confirmar o formato máximo da máquina. Se não passar, dividir em
      duas peças com duas abas de cola (2 × ~1125 × 1268)
- [ ] Fundo total (as duas camadas se encontram), colagem hot-melt + fita H
- [ ] Abas superiores laterais de **100 mm** — não substituir por aba RSC padrão
- [ ] **Vinco reverso** na aba superior traseira (testeira)
- [ ] Picote **em zíper**, não perfuração simples
- [ ] Dedeira Ø 35 mm em **corte real**, não picote
- [ ] Duas fendas de 60 × 4 mm na testeira para o cartaz
- [ ] Impressão: definir flexo pós-impressa × litho laminada (a frente destacável leva arte de alta
      cobertura; flexo direto em BC dá risco de lavadeira)
- [ ] Amostra física antes da faca definitiva, com o teste de destaque feito por quem vai repor a
      gôndola, não pelo engenheiro

---

## 10. O que falta confirmar

| Dado | Por que importa |
|---|---|
| **Peso de cada kit** | A carga de projeto de 30 kg/caixa é estimativa. Se o kit A pesar mais de 1,25 kg, a conta de BCT precisa ser refeita |
| **520 / 560 / 720 são internas ou externas?** | Este estudo tratou como internas. Se forem externas, o arranjo dos kits B e C não existe (seção 3.1) |
| **Qual face é a frente** | Adotada a de 560 mm (maior frontagem). Trocar para a de 530 não muda a contagem de kits, só espelha a faca |
| **Altura: 720 ou 760?** | Decisão comercial. 760 rende +10 kits (seção 3.2) |
| **Formato máximo de chapa do fornecedor** | Define se a caixa sai em uma peça ou duas |

---

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `calculo-expositora.py` | Memória de cálculo: arranjo, camadas, McKee, chapa, palete |
| `gera-desenhos.py` | Gerador dos SVGs |
| `faca-expositora.svg` | Planificação 1:1 com vincos, cortes e picote |
| `arranjos.svg` | Vista superior do arranjo de cada kit na camada |
| `conversao.svg` | As três etapas: caixa fechada → destaque → expositor |
