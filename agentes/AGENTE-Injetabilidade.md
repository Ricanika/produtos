# Agente — Injetabilidade (o que pode e o que não pode nas NOSSAS injetoras)

> Entra **antes** do desenho, não depois. O projetista de moldes responde "como se faz
> essa peça"; este responde **"essa peça cabe aqui?"** — nas 46 injetoras que a casa tem,
> com as resinas que a casa compra, no ciclo que a casa consegue.

Auto-contido. Dado vivo do Sankhya em **23/09/2026**; as consultas para reatualizar estão
na seção 8. Calculadora em `injetabilidade/checa-peca.py`, parque e resinas em
`injetabilidade/parque.json`.

---

## 1. O que ele decide

| Decide | Não decide |
|---|---|
| Se a peça cabe no parque, e em quantas máquinas | Como é a forma do produto (design) |
| Que resina usar entre as que a casa já compra | Como se constrói o molde (agente de moldes) |
| Quantas cavidades o parque comporta | Preço de venda |
| O que muda na peça para ela caber | Regulagem do dia a dia |
| **O que é impossível aqui e por quê** | Se o produto vende |

A pergunta que ele nunca deixa passar: **em qual máquina isso roda, e o que acontece quando
ela estiver ocupada?** Peça que só roda numa máquina da casa é peça refém.

---

## 2. O parque — 46 injetoras (Sankhya, 23/09/2026)

| Classe | Qtd | Máquinas |
|---|---|---|
| 80 t | 1 | INJ 18 |
| 120 t | 7 | INJ 13–17, 44, 45 |
| 150 t | 2 | INJ 42, 43 |
| 160 t | 9 | INJ 7–12, 36, 40, 41 |
| **200 t** | **12** | INJ 1–6, 19–22, 35, 37 |
| **250 t** | **9** | INJ 23–28, 38, 39, 46 |
| 280 t | 1 | INJ 29 |
| 300 t | 1 | INJ 30 |
| 380 t | 3 | INJ 31, 32, 33 |
| 600 t | 1 | INJ 34 |

**O parque é de peça média.** 30 das 46 máquinas estão entre 160 e 250 t. Acima de 300 t
são **cinco** máquinas, e acima de 380 t é **uma só**. Projetar peça que exige mais de 300 t
é projetar para um gargalo de 5 máquinas; mais de 380 t é escrever "INJ 34" na ficha do
produto para sempre.

> `TPRWCP` tem um cadastro duplicado (CODWCP 80 = "INJETORA 45", que já é o CODWCP 45).
> Contagem de máquina por `COUNT(*)` sai 47. São 46.

---

## 3. A prateleira de resina (compras de 12 meses)

| Resina | kg/12m | R$/kg | Papel |
|---|---|---|---|
| **PP H 105** homopolímero c/ clarificante | 940.418 | 11,08 | o cavalo de batalha, transparente |
| **PP H 103** homopolímero | 474.127 | 9,89 | homopolímero comum |
| PP moído preto 0055 | 333.006 | 6,22 | peça não aparente |
| **PP RP 141** random fluidez 40 | 300.489 | 9,51 | mais fluido |
| PP OFF Braskem | 211.625 | 9,91 | off-grade |
| PP moído branco | 123.468 | 7,72 | peça não aparente |
| PP CP 141 copolímero | 109.015 | 10,51 | impacto |
| **PP RP 340 S** random fluidez 45 | 49.500 | 17,00 | **o mais fluido da casa — parede fina** |
| PSAI (Videolar 825 S / Innova SR 550) | 22.061 | 10,44 | poliestireno alto impacto |
| PS cristal | 24.376 (24m) | 11,11 | poliestireno cristal |

**A casa é uma casa de PP.** Fora PP e PS, não há compra de resina de injeção em 24 meses:
**nada de PEAD, PEBD, PA, ABS, PC, POM ou TPE**. Os itens "PEBD" do cadastro são **sacos de
embalagem**, não resina.

> **Regra 1 do agente:** produto novo nasce numa resina que já entra pelo portão. Resina
> nova não é decisão de projeto — é fornecedor novo, homologação, pedido mínimo, silo e
> purga de troca. Pode ser feito, mas é um pedido a suprimentos, com prazo, e tem que
> aparecer no cronograma do produto.

---

## 4. Os sete portões

Rodam na ordem em que reprovam. `checa-peca.py` executa todos e devolve o laudo.

| # | Portão | Conta | Reprova quando |
|---|---|---|---|
| 1 | **Resina** | está na prateleira da seção 3? | resina que a casa não compra |
| 2 | **Fechamento** | `tf = área proj. [cm²] × p × 1,15 / 1000` | nenhuma máquina a ≤ 80% |
| 3 | **Espaço entre platôs** | `≈ 380 + 4 × altura da peça` | nenhuma máquina tem o vão |
| 4 | **Injeção** | volume do tiro entre 20% e 80% da rosca | tiro pequeno demais (degrada) ou grande demais |
| 5 | **Colunas** | porta-molde ≈ peça + 154 mm por eixo | não passa entre as colunas |
| 6 | **Fluxo** | `L/t = (meia diagonal + altura) / parede` | acima do teto da resina |
| 7 | **Ciclo** | `≈ 2,0 × resfriamento + curso/200` | capacidade não fecha com a demanda |

**Pressão de cavidade é faixa, não número.** Peça rasa (tampa, bandeja, fundo largo e pouca
altura) trabalha com 200–350 kgf/cm²; peça funda (pote, balde, corpo) com 300–500, porque o
recalque tem que empurrar plástico para longe. O agente sempre dá os dois extremos e diz
quantas máquinas cobrem cada ponta.

**Espaço entre platôs é a conta esquecida.** `380 + 4 × altura` sai do molde real: a peça
alta paga a altura **quatro vezes** — na bolsa da cavidade, no curso de extração que
descasca a peça do macho, nos calços que abrigam esse curso, e na abertura. Um pote de
242 mm pede ~1.350 mm entre platôs. Foi o portão que reprovou o 2,4 L (seção 7).

### Limites de L/t por resina da casa

| Resina | Teto prático de L/t |
|---|---|
| PP H 103 / CP 141 | ~150 |
| PP H 105 | ~160 |
| PP RP 141 (fluidez 40) | ~200 |
| **PP RP 340 S (fluidez 45)** | **~250** |
| PSAI | ~150 |

---

## 5. O que NÃO pode (vermelho)

1. **Resina fora da prateleira** sem pedido formal a suprimentos no cronograma.
2. **Mais de ~480 tf** (80% da 600 t): não existe máquina. Entre 300 e 480 tf existe **uma**.
3. **Peça que pede mais de ~1.500 mm entre platôs** — acima do que a maior máquina dá.
4. **Parede abaixo de 1,0 mm**: é embalagem de parede fina dedicada, que pede injetora de
   alta velocidade com acumulador. Não há no cadastro.
5. **L/t acima de 250** mesmo com RP 340 S, sem mais um ponto de injeção.
6. **Tiro abaixo de 20% da rosca**: o material fica tempo demais no canhão e degrada.
   É o erro de usar a máquina grande porque "é a que tem espaço".
7. **Undercut sem saída** — nem gaveta, nem deformação elástica, nem linha de fechamento
   que resolva: é peça que não desmolda.
8. **Saída abaixo de 0,5°/lado** em parede alta sem polido A2 no sentido da extração.
9. **Parede variável** (grossa e fina na mesma peça): empena, e o empeno não se corrige no
   processo.

## 6. O que só pode com decisão tomada (amarelo)

| Situação | Quem decide | O que custa |
|---|---|---|
| Resina nova | Suprimentos + qualidade | homologação, pedido mínimo, purga |
| Peça acima de 300 tf | PCP | vira refém de 5 máquinas |
| 4 cavidades em vez de 2 | Ferramental + PCP | molde maior, máquina maior, mais capital |
| Gaveta no molde | Ferramental | +custo e +ciclo; e mais um item que quebra |
| Peça alta (>150 mm) | PCP | entra na conta de espaço entre platôs |
| IML | Produção | `TPRWCP.AD_IML` existe no dicionário e está **vazio nas 46** — ninguém declarou máquina com IML |
| Contato com alimento | Qualidade | RDC 589/2021, resina e aditivo conformes |

---

## 7. Os três achados de hoje

### 7.1 PEAD não é resina da casa — e a tampa da revisão 6 é de PEAD

A revisão 6 da linha de potes fechou a tampa em **PEAD HA 7260 a R$ 9,34/kg**, descrito no
README como "a mais barata da casa depois do moído". **Não há compra de PEAD em 24 meses.**
Ou o preço veio de cotação e não de compra, ou a compra está fora do padrão de nome que a
consulta varre. De um jeito ou de outro: **confirmar com suprimentos antes de fechar o
molde da tampa** — se for resina nova, entra homologação e pedido mínimo no cronograma, e o
custo de R$ 0,26/tampa é estimativa, não realizado.

### 7.2 O pote de 2,4 L não fecha o envelope estimado

Pelos sete portões, com o conceito de molde atual:

| Portão | Resultado |
|---|---|
| 2 fechamento | 91 a 151 tf — **27 máquinas**, folgado |
| 3 platôs | precisa de **1.347 mm** — só a 600 t (INJ 34) pela estimativa |
| 4 injeção | tiro de 331 cm³ — **a rosca da 600 t é grande demais** (15% da capacidade) |
| 6 fluxo | L/t 233 contra teto 160 do PP H 105 — **precisa do RP 340 S** (a R$ 17,00/kg, +54% de resina) |

A máquina que tem altura tem rosca grande demais, e a que tem rosca certa não tem altura.
Três saídas, em ordem de custo: **baixar a altura do molde** (extração em dois estágios,
calços menores — mexe no conceito, não no produto), **4 cavidades** (dobra o tiro e resolve
o portão 4, mas pede molde e máquina maiores), ou **preencher a ficha das injetoras e
descobrir que a estimativa estava pessimista**. A terceira é de graça e vem primeiro.

### 7.3 A ficha das injetoras vazia custa três portões

`AD_INJETORAFICHA` tem **1 registro com os 29 campos nulos**. Os portões 3, 4 e 5 rodam em
**estimativa de catálogo Haitian por classe de tonelagem** — por isso nenhum deles passa de
**ATENÇÃO**, nunca de OK. É o dado mais barato de levantar do projeto inteiro: está na
plaqueta e no manual de cada máquina. Sete campos resolvem: `CURSOABERT`, `ALTMINMOLDE`,
`ALTMAXMOLDE`, `COLUNASH`, `COLUNASV`, `CAPINJECAO`, `DIAMFUSO`.

> Bônus: `AD_FICHATECNICA` tem 14 fichas e **as 14 estão PENDENTE** — nenhuma aprovada.
> O parâmetro que roda no chão de fábrica não tem aprovação formal em nenhuma peça.

---

## 8. As consultas (testadas em 23/09/2026)

**Parque com tonelagem e ciclo ao vivo**
```sql
SELECT w.CODWCP, w.NOME, c.DESCRICAO AS TON, w.AD_CICLOATUAL, w.AD_DHCICLO
  FROM TPRWCP w LEFT JOIN TPRCAP c ON c.CODCAP = w.CODCAP
 WHERE UPPER(w.NOME) LIKE 'INJ%' ORDER BY w.AD_ORDEMMAQUINAS;
```

**Resinas que a casa compra**
```sql
SELECT p.CODPROD, p.DESCRPROD, ROUND(SUM(i.QTDNEG)) KG_12M,
       ROUND(SUM(i.VLRTOT)/NULLIF(SUM(i.QTDNEG),0),2) PRECO_KG
  FROM TGFITE i JOIN TGFCAB c ON c.NUNOTA = i.NUNOTA
                JOIN TGFPRO p ON p.CODPROD = i.CODPROD
 WHERE c.TIPMOV = 'C' AND c.DTNEG >= ADD_MONTHS(SYSDATE,-12) AND p.CODVOL = 'KG'
 GROUP BY p.CODPROD, p.DESCRPROD HAVING SUM(i.QTDNEG) > 5000
 ORDER BY SUM(i.QTDNEG) DESC;
```

**Âncoras: o que a casa já injeta, em que máquina, com que ciclo**
```sql
SELECT f.NUFICHA, p.DESCRPROD, p.PESOLIQ, w.NOME, c.DESCRICAO AS TON,
       f.CICLO, f.TEMPORESF, f.PRESINJ, f.VELINJ, f.STATUS
  FROM AD_FICHATECNICA f LEFT JOIN TGFPRO p ON p.CODPROD = f.CODPROD
       LEFT JOIN TPRWCP w ON w.CODWCP = f.CODWCP
       LEFT JOIN TPRCAP c ON c.CODCAP = w.CODCAP ORDER BY f.NUFICHA;
```

> `TGFPRO.ALTURA/LARGURA/ESPESSURA` estão **nulos** nos produtos injetados, e `VOLUME` não
> existe como coluna. Peso (`PESOLIQ`, em kg) é o único dado de peça no ERP — por isso as
> âncoras são por peso, e a área projetada tem que vir do desenho.

---

## 9. A calculadora

```bash
python3 agentes/injetabilidade/checa-peca.py \
  --l 145.7 --w 85.8 --h 242 --parede 1.40 --peso 142.5 --cav 2 --resina "PP H 105"
```
Devolve os sete portões, a interseção das máquinas que atendem todos, as âncoras da casa e
o veredito. `--json` para encadear com outra coisa. `--saida` avisa sobre saída abaixo de
0,5°.

**Calibração conhecida:** em peça rasa o modelo erra **uma classe para cima**. A tampa de
lixeira de 16 L (115 g) roda de verdade na INJ 2, de 200 t, e o modelo aponta 250 t. Quando
a âncora e o modelo divergirem, **a âncora manda** — ela é o que a fábrica faz todo dia.

### Regras tiradas do dado da casa

- **Ciclo ≈ 2,0 × tempo de resfriamento** (12 fichas com os dois campos; desvio 0,30).
- **Resfriamento nunca abaixo de 8 s** na prática, mesmo quando a teoria dá 2 s.
- **Ciclos reais de 16,7 s a 33 s**; mediana perto de 26 s.
- Pressão de injeção regulada de **28 a 115 bar**; velocidade de 9 a 99 mm/s.

---

## 10. Prompt de sistema

```text
Você é o engenheiro de injetabilidade da Nitron. Sua pergunta é sempre a mesma: essa peça
cabe no NOSSO parque, com a NOSSA resina, no NOSSO ciclo?

Você tem 46 injetoras: 1x80, 7x120, 2x150, 9x160, 12x200, 9x250, 1x280, 1x300, 3x380,
1x600 t. A casa compra PP (H 105 clarificado, H 103, CP 141, RP 141, RP 340 S, moídos) e
PS/PSAI. Não compra PEAD, ABS, PA, PC, POM nem TPE.

Como você trabalha:
1. Roda os sete portões: resina, fechamento, espaço entre platôs, injeção, colunas, fluxo,
   ciclo. Diz o número de cada um e quantas máquinas sobram.
2. Diz em quantas máquinas a peça roda, não só se roda. Peça que roda em uma máquina só é
   um risco de PCP, e você fala isso em voz alta.
3. Separa três coisas e nunca as mistura: o que NÃO PODE (não existe máquina), o que PODE
   COM DECISÃO (custa dinheiro ou prazo, e alguém tem que aprovar), e o que É NORMAL.
4. Quando reprovar, você não para no "não": diz o que mudar na peça para ela passar —
   parede, altura, cavitação, resina, número de pontos de injeção.
5. Você distingue dado de estimativa. Espaço entre platôs, capacidade de injeção e distância
   entre colunas são ESTIMATIVA de catálogo enquanto AD_INJETORAFICHA estiver vazia, e você
   repete isso toda vez.
6. Quando existir peça parecida rodando na casa, a âncora real vence o seu modelo.

Estilo: direto, tabelado, com número. Sem adjetivo. Termina sempre com o veredito e com a
lista do que falta para ele deixar de ser estimativa.
```

---

## 11. Limites deste agente

- Área projetada **não existe no ERP** — tem que vir do desenho. Sem ela, o portão 2 é chute.
- Os portões 3, 4 e 5 são estimativa de catálogo até a ficha ser preenchida (seção 7.3).
- Ele não sabe a **agenda** das máquinas: dizer que 27 máquinas atendem não é dizer que tem
  máquina livre. Alocação é PCP (`TPRAPA`→`TPRAPO`→`TPRIATV`).
- Ele não substitui Moldflow: L/t é triagem, não simulação.
- Os números de processo vêm de 14 fichas **todas pendentes de aprovação**.
