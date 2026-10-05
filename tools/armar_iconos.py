"""Arma el atlas de íconos de objetos a partir de hojas 3x2 con fondo magenta (#FF00FF).

Uso:
    python3 tools/armar_iconos.py

Cada hoja (hojas/iconos-<set>.jpg) tiene 6 íconos en 3 columnas x 2 filas. El script separa cada
objeto (aunque tenga partes sueltas, como las dos grebas), quita el magenta y su halo, lo centra
en un cuadrado y guarda assets/iconos.webp más el mapa de posiciones assets/iconos.json.
"""
import json
import os

import numpy as np
from PIL import Image
from scipy import ndimage

TAM = 144  # lado de cada ícono en el atlas
HOJAS = {
    "ciempies": ["arma_mantis", "arma_polilla", "casco", "coraza", "patas", "amuleto"],
    "hierro": ["arma_mantis", "arma_polilla", "casco", "coraza", "patas", "amuleto"],
    "extras": ["alas", "ambar", "icor", "pocion", "oro", "vela"],
}


def quitar_magenta(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    magenta = np.minimum(r, b) - g
    alfa = np.clip(1 - (magenta - 50) / 110, 0, 1)
    alfa[alfa < .12] = 0
    out = a.copy()
    exceso = np.clip(np.minimum(out[..., 0], out[..., 2]) - g - 12, 0, None)
    out[..., 0] -= exceso
    out[..., 2] -= exceso
    return np.dstack([np.clip(out, 0, 255), alfa * 255]).astype(np.uint8)


def separar(ruta):
    a = np.asarray(Image.open(ruta).convert("RGB")).astype(float)
    h, w = a.shape[:2]
    fg = (np.minimum(a[..., 0], a[..., 2]) - a[..., 1]) < 70
    lab, n = ndimage.label(ndimage.binary_dilation(fg, iterations=4))
    celdas = [[] for _ in range(6)]
    for i, sl in enumerate(ndimage.find_objects(lab)):
        if sl is None:
            continue
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        if (y1 - y0) * (x1 - x0) < 600:
            continue
        cy, cx = (y0 + y1) / 2, (x0 + x1) / 2
        celdas[int(cy // (h / 2)) * 3 + int(cx // (w / 3))].append(i + 1)
    rgba = quitar_magenta(a)
    out = []
    for ids in celdas:
        m = np.isin(lab, ids)
        ys, xs = np.where(m)
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        rec = rgba[y0:y1, x0:x1].copy()
        rec[..., 3] = (rec[..., 3] * m[y0:y1, x0:x1]).astype(np.uint8)
        im = Image.fromarray(rec)
        lado = max(im.size)
        lienzo = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
        lienzo.alpha_composite(im, ((lado - im.width) // 2, (lado - im.height) // 2))
        out.append(lienzo.resize((int(TAM * .9),) * 2, Image.LANCZOS))
    return out


def main():
    total = sum(len(v) for v in HOJAS.values())
    cols = 6
    atlas = Image.new("RGBA", (cols * TAM, ((total + cols - 1) // cols) * TAM), (0, 0, 0, 0))
    mapa, k = {}, 0
    for hoja, nombres in HOJAS.items():
        ruta = f"hojas/iconos-{hoja}.jpg"
        if not os.path.exists(ruta):
            continue
        for nombre, ic in zip(nombres, separar(ruta)):
            x, y = (k % cols) * TAM, (k // cols) * TAM
            atlas.alpha_composite(ic, (x + (TAM - ic.width) // 2, y + (TAM - ic.height) // 2))
            mapa.setdefault(hoja, {})[nombre] = [x, y]
            k += 1
    atlas.save("assets/iconos.webp", quality=88, method=6)
    with open("assets/iconos.json", "w") as f:
        json.dump({"tam": TAM, "iconos": mapa}, f, separators=(",", ":"))
    print("Íconos:", {h: len(v) for h, v in mapa.items()})


if __name__ == "__main__":
    main()
