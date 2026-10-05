"""Arma el atlas de sprites de una criatura a partir de hojas con fondo magenta (#FF00FF).

Uso:
    python3 tools/armar_sprites.py

Edita la lista HOJAS: cada hoja indica qué animaciones contiene y en qué franja
vertical (en píxeles) está cada una. El script:
  1. separa cada cuadro automáticamente (no hace falta grilla),
  2. quita el magenta y su halo rosado,
  3. iguala la escala usando la caminata como referencia,
  4. calcula el punto de los pies de cada cuadro,
  5. guarda assets/<nombre>-sprites.webp y assets/<nombre>-sprites.json.

El JSON tiene, por animación, una lista de cuadros [x, y, ancho, alto, pieX, pieY].
"""
import json
import os

import numpy as np
from PIL import Image
from scipy import ndimage

NOMBRE = "mantis"
ALTURA_REF = 300  # alto en píxeles de la caminata en el atlas
# (archivo, x mínima para ignorar etiquetas de texto, [(animación, y_desde, y_hasta, escala_extra)])
HOJAS = [
    ("hojas/mantis-quieto-caminar.png", 0, [("idle", 0, 388, 1), ("walk", 388, 10000, 1)]),
    ("hojas/mantis-ataques.png", 172, [("atk1", 344, 505, 1), ("atk2", 506, 664, 1), ("atk3", 665, 804, 1),
                                        ("hit", 804, 906, 1.25), ("death", 906, 1020, 1)]),
]
REFERENCIA = {"hojas/mantis-quieto-caminar.png": "walk", "hojas/mantis-ataques.png": "atk1"}


def quitar_magenta(celda, mascara):
    r, g, b = celda[..., 0], celda[..., 1], celda[..., 2]
    magenta = np.minimum(r, b) - g
    alfa = np.clip(1 - (magenta - 40) / 120, 0, 1) * mascara
    alfa[alfa < .15] = 0
    out = celda.copy()
    exceso = np.clip(np.minimum(out[..., 0], out[..., 2]) - g - 15, 0, None)
    out[..., 0] -= exceso
    out[..., 2] -= exceso
    return np.dstack([np.clip(out, 0, 255), alfa * 255]).astype(np.uint8)


def separar(ruta, xmin, franjas):
    a = np.asarray(Image.open(ruta).convert("RGB")).astype(float)
    fg = (np.minimum(a[..., 0], a[..., 2]) - a[..., 1]) < 60
    fg[:, :xmin] = False
    lab, _ = ndimage.label(ndimage.binary_dilation(fg, iterations=5))
    res = {f[0]: [] for f in franjas}
    for i, sl in enumerate(ndimage.find_objects(lab)):
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        if (y1 - y0) * (x1 - x0) < 1800:
            continue
        cy = (y0 + y1) / 2
        for nombre, f0, f1, _ in franjas:
            if f0 <= cy < f1:
                res[nombre].append((x0, x1, y0, y1, i + 1))
                break
    out = {}
    for nombre, lst in res.items():
        lst.sort()
        out[nombre] = [quitar_magenta(a[y0:y1, x0:x1], (lab[y0:y1, x0:x1] == li).astype(float))
                       for (x0, x1, y0, y1, li) in lst]
    return out


def main():
    anims = {}
    for ruta, xmin, franjas in HOJAS:
        cuadros = separar(ruta, xmin, franjas)
        ref = np.median([c.shape[0] for c in cuadros[REFERENCIA[ruta]]])
        base = ALTURA_REF / ref
        for nombre, _, _, extra in franjas:
            lista = []
            for c in cuadros[nombre]:
                im = Image.fromarray(c)
                s = base * extra
                im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
                opaco = np.asarray(im)[..., 3] > 100
                ys, xs = np.where(opaco)
                pie_y = int(ys.max())
                pie_x = int(np.median(xs[ys >= pie_y - max(4, int(.05 * im.height))]))
                lista.append((im, pie_x, pie_y))
            anims[nombre] = lista
    pad = 2
    altos = [max(f[0].height for f in fr) for fr in anims.values()]
    ancho = max(sum(f[0].width + pad for f in fr) for fr in anims.values()) + pad
    alto = sum(altos) + pad * (len(altos) + 1)
    atlas = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    meta, y = {}, pad
    for (nombre, fr), h in zip(anims.items(), altos):
        x, meta[nombre] = pad, []
        for im, px, py in fr:
            atlas.alpha_composite(im, (x, y))
            meta[nombre].append([x, y, im.width, im.height, px, py])
            x += im.width + pad
        y += h + pad
    os.makedirs("assets", exist_ok=True)
    atlas.save(f"assets/{NOMBRE}-sprites.webp", quality=86, method=6)
    with open(f"assets/{NOMBRE}-sprites.json", "w") as f:
        json.dump({"ref": ALTURA_REF, "anims": meta}, f, separators=(",", ":"))
    print("Atlas listo:", {k: len(v) for k, v in meta.items()})


if __name__ == "__main__":
    main()
