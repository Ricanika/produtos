"""Miniatura 230x110 para o gcode da Anycubic.

O PrusaSlicer em linha de comando nao renderiza a miniatura (precisa da GUI),
e o perfil da Anycubic pede uma de 230x110. Este script desenha a peca a
partir do STL e injeta o bloco "thumbnail begin/end" (base64 PNG, o mesmo
formato que o OrcaSlicer escreve) no cabecalho do gcode.

    python3 miniatura.py cesto-P-petg-anycubic.gcode
"""
import base64, io, sys
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

W, H = 230, 110
STL = "/home/user/produtos/cesto-empilhavel/cad/cesto-aba.stl"

m = trimesh.load(STL)
V, F = m.vertices, m.faces
c = (V.min(0) + V.max(0)) / 2.0
V = V - c

# camera: isometrica olhando de cima-frente
elev, azim = 24.0, -58.0
er, ar = np.radians(elev), np.radians(azim)
eye = np.array([np.cos(er)*np.cos(ar), np.cos(er)*np.sin(ar), np.sin(er)])

n = m.face_normals
# descarta faces de costas para a camera
vis = n @ eye > 0.0
F, n = F[vis], n[vis]

tri = V[F]
# profundidade para ordenar (painter)
d = (tri.mean(1) @ eye)
o = np.argsort(d)
tri, n = tri[o], n[o]

# sombreamento lambertiano simples com luz um pouco acima da camera
luz = eye + np.array([0.0, 0.0, 0.55])
luz /= np.linalg.norm(luz)
i = np.clip(n @ luz, 0.0, 1.0)
base = np.array([0.36, 0.62, 0.90])       # azul do PETG
cor = (0.16 + 0.84 * i)[:, None] * base[None, :]
cor = np.clip(cor, 0.0, 1.0)

fig = plt.figure(figsize=(W/100.0, H/100.0), dpi=100)
ax = fig.add_subplot(111, projection="3d")
ax.add_collection3d(Poly3DCollection(tri, facecolors=cor, linewidths=0, shade=False))
r = np.abs(V).max()
ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r)
ax.set_box_aspect((1, 1, 1))
ax.view_init(elev=elev, azim=azim)
ax.set_axis_off()
fig.patch.set_alpha(0.0)
fig.subplots_adjust(0, 0, 1, 1)

buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=100, transparent=True)
png = buf.getvalue()
print("png bytes:", len(png))

b64 = base64.b64encode(png).decode("ascii")
linhas = [b64[k:k + 78] for k in range(0, len(b64), 78)]
bloco = [";\n", f"; thumbnail begin {W}x{H} {len(b64)}\n"]
bloco += [f"; {l}\n" for l in linhas]
bloco += ["; thumbnail end\n", ";\n"]
bloco = "".join(bloco)

alvo = sys.argv[1] if len(sys.argv) > 1 else "cesto-P-petg-anycubic.gcode"
texto = open(alvo).read()
if "thumbnail begin" in texto:
    sys.exit(f"{alvo} ja tem miniatura -- nada a fazer")

# entra depois do bloco de comentarios do cabecalho, antes do primeiro comando
marca = "; first layer extrusion width"
i = texto.index(marca)
i = texto.index("\n", i) + 1
open(alvo, "w").write(texto[:i] + bloco + texto[i:])
print(f"{alvo}: miniatura de {len(png)} bytes ({len(linhas)} linhas base64) injetada")
