# Desenhos da ficha técnica

Os dois SVG da `ficha-tecnica.html` que carregam cota **saem do cálculo**, não são
desenhados à mão:

```
python3 desenhos/gera-svg-linha.py      # elevação dos quatro potes (seção 01)
python3 desenhos/gera-svg-tampa-pe.py   # corte do encaixe da tampa PE (seção 04)
```

Cada um escreve o bloco `<svg>…</svg>` na saída padrão; ele substitui o bloco
correspondente na ficha. Mudou uma cota em `calculo-modular.py`? Roda de novo.

**Por que existem.** Na revisão 5 o desenho da elevação tinha degrau de pé de 3,55 mm
enquanto o script calculava 3,86 — o desenho tinha sido feito à mão e derivou sozinho.
Desenho com cota que não sai do cálculo mente cedo ou tarde.
