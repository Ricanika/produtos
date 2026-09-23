# Agentes

Especialistas auto-contidos. Cada arquivo é um papel completo — perfil, habilidades,
método, cálculos, checklists e prompt de sistema — para colar num chat novo sem contexto
anterior.

| Agente | Papel | Entra quando |
|---|---|---|
| [`AGENTE-Injetabilidade.md`](AGENTE-Injetabilidade.md) | Engenheiro de injetabilidade — o que cabe nas 46 injetoras da casa | **Antes de desenhar**: resina, tonelagem, altura, ciclo. Tem calculadora: `injetabilidade/checa-peca.py` |
| [`AGENTE-Projetista-de-Moldes.md`](AGENTE-Projetista-de-Moldes.md) | Projetista de moldes de injeção (ferramentaria) | O produto está desenhado e precisa virar ferramenta: DFM, cavitação, aço, try-out |
| [`../potes-modulares/fatiamento/AGENTE-Kobra3Max-PETG.md`](../potes-modulares/fatiamento/AGENTE-Kobra3Max-PETG.md) | Fatiador FDM (STL → G-code, Kobra 3 Max / PETG) | Protótipo físico antes do molde |

A ordem natural da esteira: **injetabilidade (cabe?) → design do produto → fatiador
(protótipo FDM) → projetista de moldes (ferramenta) → injeção**. O protótipo impresso prova ergonomia e encaixe; ele **não**
prova vedação, contração nem ciclo — isso é do projetista de moldes.
