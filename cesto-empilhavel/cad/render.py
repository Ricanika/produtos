"""Rasterizador ortografico simples, sem display: z-buffer + sombreamento plano.

Existe porque a sessao nao tem display nem OpenGL, e o painters algorithm do
matplotlib quebra em geometria que se interpenetra (painel dentro do berco).
"""
import numpy as np


def _normalizar(v):
    n = np.linalg.norm(v, axis=-1, keepdims=True)
    return v / np.where(n == 0, 1, n)


def camera(alvo, direcao, up=(0, 0, 1)):
    d = _normalizar(np.asarray(direcao, float))
    up = np.asarray(up, float)
    dir_x = _normalizar(np.cross(up, d))
    dir_y = _normalizar(np.cross(d, dir_x))
    return np.asarray(alvo, float), np.stack([dir_x, dir_y, d])


def render(meshes, direcao=(-1.0, -1.6, -0.75), largura=1400, margem=0.06,
           fundo=(0.965, 0.962, 0.955), luz=(-0.35, -0.5, 0.79),
           contorno=True):
    """meshes: lista de (trimesh, cor rgb 0-1). Devolve array HxWx3 uint8."""
    verts, faces, cores = [], [], []
    off = 0
    for m, cor in meshes:
        verts.append(np.asarray(m.vertices, float))
        faces.append(np.asarray(m.faces, int) + off)
        cores.append(np.tile(np.asarray(cor, float), (len(m.faces), 1)))
        off += len(m.vertices)
    V = np.concatenate(verts)
    F = np.concatenate(faces)
    C = np.concatenate(cores)

    alvo = (V.min(0) + V.max(0)) / 2
    _, base = camera(alvo, direcao)
    P = (V - alvo) @ base.T                      # x,y na tela; z profundidade

    x0, y0 = P[:, 0].min(), P[:, 1].min()
    x1, y1 = P[:, 0].max(), P[:, 1].max()
    esc = largura * (1 - 2 * margem) / max(x1 - x0, 1e-9)
    altura = int(round((y1 - y0) * esc / (1 - 2 * margem)))
    px = (P[:, 0] - x0) * esc + largura * margem
    py = (y1 - P[:, 1]) * esc + altura * margem
    pz = P[:, 2]

    img = np.tile(np.asarray(fundo, float), (altura, largura, 1))
    zbuf = np.full((altura, largura), np.inf)

    # normais no espaco do objeto, para a luz nao girar com a camera
    tri = V[F]
    nrm = _normalizar(np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]))
    L = _normalizar(np.asarray(luz, float))
    difusa = np.abs(nrm @ L)
    tom = 0.30 + 0.70 * difusa                   # ambiente + difusa
    # profundidade media so para ordenar de tras para frente
    ordem = np.argsort(-pz[F].mean(1))

    sx, sy, sz = px[F], py[F], pz[F]
    for i in ordem:
        ax, bx, cx = sx[i]
        ay, by, cy = sy[i]
        area = (bx - ax) * (cy - ay) - (cx - ax) * (by - ay)
        if abs(area) < 1e-9:
            continue
        xi0 = max(int(np.floor(min(ax, bx, cx))), 0)
        xi1 = min(int(np.ceil(max(ax, bx, cx))) + 1, largura)
        yi0 = max(int(np.floor(min(ay, by, cy))), 0)
        yi1 = min(int(np.ceil(max(ay, by, cy))) + 1, altura)
        if xi0 >= xi1 or yi0 >= yi1:
            continue
        gx, gy = np.meshgrid(np.arange(xi0, xi1) + 0.5,
                             np.arange(yi0, yi1) + 0.5)
        w0 = ((bx - ax) * (gy - ay) - (gx - ax) * (by - ay)) / area
        w1 = ((gx - ax) * (cy - ay) - (cx - ax) * (gy - ay)) / area
        dentro = (w0 >= 0) & (w1 >= 0) & (w0 + w1 <= 1)
        if not dentro.any():
            continue
        z = sz[i][0] + w1 * (sz[i][1] - sz[i][0]) + w0 * (sz[i][2] - sz[i][0])
        alvo_z = zbuf[yi0:yi1, xi0:xi1]
        mask = dentro & (z < alvo_z)
        if not mask.any():
            continue
        alvo_z[mask] = z[mask]
        img[yi0:yi1, xi0:xi1][mask] = C[i] * tom[i]

    if contorno:
        vazio = ~np.isfinite(zbuf)
        borda = np.zeros_like(vazio)
        borda[1:, :] |= vazio[1:, :] ^ vazio[:-1, :]
        borda[:, 1:] |= vazio[:, 1:] ^ vazio[:, :-1]
        img[borda & ~vazio] *= 0.55

    return (np.clip(img, 0, 1) * 255).astype(np.uint8)


def salvar(img, caminho):
    from PIL import Image
    Image.fromarray(img).save(caminho, quality=94)
    return caminho
