"""Arma el atlas de la Mantis nueva (con guadaña) por set, a partir de videos de Google Flow
y hojas de Nano Banana con fondo magenta.

Uso:
    python3 tools/armar_mantis_sets.py

Para cada video de caminata ("walking in place"):
  1. lee todos los cuadros,
  2. busca el tramo que cierra en loop (dos pasos) saltando el primer segundo y medio,
  3. toma ~12 cuadros parejos de ese tramo,
  4. quita el magenta y deja solo la figura (componente principal).
De la hoja de combate toma los cuadros por fila/columna (ver HOJA).
Todo se lleva a la misma escala (ALTURA_REF = alto del cuerpo, sin la guadaña) y se calcula el punto de los pies.

Salida: assets/mantis-sets.webp y assets/mantis-sets.json
  {"ref":ALTURA_REF,"sets":{set:{anim:[[x,y,w,h,pieX,pieY],...]}}}
"""
import json
import os
import subprocess
import tempfile

import numpy as np
from PIL import Image
from scipy import ndimage

ALTURA_REF = 250
VIDEOS = {  # set: {anim: archivo}
    "ambar": {"walkF": "hojas/videos/ambar-frente.mp4", "walkB": "hojas/videos/ambar-espalda.mp4"},
    "ciempies": {"walkF": "hojas/videos/ciempies-frente.mp4", "walkB": "hojas/videos/ciempies-espalda.mp4"},
    "dorado": {"walkF": "hojas/videos/dorado-frente.mp4"},  # aspecto del set completo +15 (Gemini)
}
# Hoja de combate: 6 columnas x 5 filas. (anim, [(fila, columna), ...])
HOJA = ("hojas/ciempies-combate.jpg", "ciempies", 6, 5, [
    ("atk1", [(2, 0), (0, 2), (0, 4), (0, 5)]),
    ("atk2", [(2, 0), (2, 1), (2, 2), (2, 3)]),
    ("atk3", [(2, 1), (2, 4), (2, 2), (2, 4), (2, 5)]),
    ("hit", [(3, 1), (3, 1)]),
    ("death", [(4, 2), (4, 3), (4, 4), (4, 5)]),
])
CUADROS_LOOP = 12
# Hojas en grilla con bordes (cuadros en orden de lectura): (archivo, set, anim, xs, ys)
GRILLAS = [("hojas/dorado-espalda.jpg", "dorado", "walkB",
            [(7, 457), (463, 915), (921, 1373), (1379, 1831), (1837, 2288), (2295, 2730)],
            [(1, 502), (508, 1009), (1016, 1483)])]
# Ajuste fino a ojo (la medición automática se confunde con el mango de la guadaña cruzando el cuerpo)
AJUSTE = {("dorado", "walkF"): 1.3, ("dorado", "walkB"): 1.3, ("ciempies", "walkF"): 1.32, ("ciempies", "walkB"): 1.0,
          **{("ciempies", a): 1.24 for a in ("atk1", "atk2", "atk3", "hit", "death")}}


def recortar(a, umbral=60):
    """a: RGB float. Devuelve RGBA uint8 recortado a la figura, sin magenta."""
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mag = np.minimum(r, b) - g
    fg = mag < umbral
    fg = ndimage.binary_opening(fg, iterations=1)
    lab, n = ndimage.label(ndimage.binary_dilation(fg, iterations=6))
    if n == 0:
        return None
    sz = ndimage.sum(fg, lab, range(1, n + 1))
    keep = np.zeros(n + 1, bool)
    big = sz.max()
    keep[1:] = sz > big * .02  # la figura y piezas grandes (la hoja de la guadaña si quedó suelta)
    m = keep[lab] & fg
    ys, xs = np.nonzero(m)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    c = a[y0:y1, x0:x1].copy()
    mk = m[y0:y1, x0:x1].astype(float)
    magc = np.minimum(c[..., 0], c[..., 2]) - c[..., 1]
    alfa = np.clip(1 - (magc - 30) / 110, 0, 1) * mk
    alfa[alfa < .15] = 0
    exceso = np.clip(np.minimum(c[..., 0], c[..., 2]) - c[..., 1] - 2, 0, None)
    c[..., 0] -= exceso
    c[..., 2] -= exceso
    return np.dstack([np.clip(c, 0, 255), alfa * 255]).astype(np.uint8)


def alto_cuerpo(rgba):
    """Alto del cuerpo: de los pies a la coronilla, medido en una franja alrededor del eje del cuerpo
    (así no cuentan la guadaña, que sale hacia los costados, ni las antenas finitas)."""
    al = rgba[..., 3] > 100
    h, w = al.shape
    ys, xs = np.nonzero(al)
    pie = ys.max()
    baja = al[int(h * .35):int(h * .8)]
    cols = baja.sum(0)
    cx = int(np.average(np.arange(w), weights=cols + 1e-6))
    bw = max(6, int(h * .07))
    franja = al[:, max(0, cx - bw):cx + bw]
    llen = franja.mean(1)
    top = np.nonzero(llen > .3)[0].min()
    return pie - top


def leer_video(ruta):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["ffmpeg", "-v", "error", "-i", ruta, os.path.join(d, "f%04d.png")], check=True)
        fs = sorted(os.listdir(d))
        return [np.asarray(Image.open(os.path.join(d, f)).convert("RGB")) for f in fs]


def loop(frames):
    peq = [np.asarray(Image.fromarray(f.astype(np.uint8)).convert("L").resize((240, 135))).astype(float) for f in frames]
    best = None
    for s in range(36, len(peq) - 50):
        for p in range(18, 44):
            if s + p >= len(peq):
                break
            d = np.abs(peq[s] - peq[s + p]).mean() + .15 * np.abs(peq[s + 1] - peq[s + p + 1 if s + p + 1 < len(peq) else s + p]).mean()
            if best is None or d < best[0]:
                best = (d, s, p)
    _, s, p = best
    idx = [s + round(i * p / CUADROS_LOOP) for i in range(CUADROS_LOOP)]
    return idx, best


def main():
    crudos = {}  # set -> anim -> [rgba]
    import pickle
    cache_v = "hojas/.cache-videos.pkl"
    if os.path.exists(cache_v):
        crudos = pickle.load(open(cache_v, "rb"))
    for st, anims in VIDEOS.items():
        for an, ruta in anims.items():
            if an in crudos.get(st, {}):
                continue
            fr = leer_video(ruta)
            idx, best = loop(fr)
            print(st, an, "loop desde", best[1], "periodo", best[2], "dif", round(best[0], 2))
            crudos.setdefault(st, {})[an] = [recortar(fr[i].astype(float)) for i in idx]
            del fr
            pickle.dump(crudos, open(cache_v, "wb"))
    ruta, st, nc, nf, lista = HOJA
    a = np.asarray(Image.open(ruta).convert("RGB")).astype(float)
    H, W = a.shape[:2]
    cache = {}
    for an, celdas in lista:
        out = []
        for (fi, co) in celdas:
            if (fi, co) not in cache:
                cache[(fi, co)] = recortar(a[fi * H // nf:(fi + 1) * H // nf, co * W // nc:(co + 1) * W // nc])
            out.append(cache[(fi, co)])
        crudos[st][an] = out
    for ruta_g, st_g, an_g, xs, ys in GRILLAS:
        a_g = np.asarray(Image.open(ruta_g).convert("RGB")).astype(float)
        crudos[st_g][an_g] = [recortar(a_g[y0 + 4:y1 - 4, x0 + 4:x1 - 4]) for (y0, y1) in ys for (x0, x1) in xs]
    # escala: la caminata de frente de cada set define el alto del cuerpo
    anims = {}
    for st, d in crudos.items():
        ref_v = np.median([alto_cuerpo(c) for c in d["walkF"]])
        ref_h = None
        if st == HOJA[1]:  # cuadros de pie de la hoja (fila 1: 1, 2 y 4) contra la caminata de frente
            ref_h = np.median([alto_cuerpo(recortar(a[0:H // nf, co * W // nc:(co + 1) * W // nc])) for co in (0, 1, 3)])
        for an, cs in d.items():
            ref = ref_v if an.startswith("walk") else ref_h
            if an == "walkB":
                ref = np.median([alto_cuerpo(c) for c in cs]) * 1.0
            s = ALTURA_REF / ref * AJUSTE.get((st, an), 1)
            lst = []
            for c in cs:
                if st == "ciempies" and an.startswith("walk"):  # la luz del video tiñe de rosa el hueso
                    c = c.copy()
                    f = c[..., :3].astype(float)
                    f[..., 2] = np.minimum(f[..., 2], f[..., 1] * .9)
                    f[..., 0] = np.minimum(f[..., 0], f[..., 1] * 1.18 + 8)
                    c[..., :3] = f.clip(0, 255).astype(np.uint8)
                if st == "dorado":  # las alas translúcidas dejan pasar el magenta: tonos salmón -> dorado
                    c = c.copy()
                    f = c[..., :3].astype(float)
                    calido = (f[..., 0] - f[..., 1]) > 28
                    f[..., 2] = np.where(calido, np.minimum(f[..., 2], f[..., 1] * .55), f[..., 2])
                    f[..., 1] = np.where(calido, np.minimum(255, f[..., 1] * 1.06), f[..., 1])
                    c[..., :3] = f.clip(0, 255).astype(np.uint8)
                im = Image.fromarray(c)
                im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
                al = np.asarray(im)[..., 3] > 100
                ys, xs = np.nonzero(al)
                py = int(ys.max())
                px = int(np.median(xs[ys >= py - max(6, int(.06 * im.height))]))
                lst.append((im, px, py))
            if an.startswith("walk"):  # pies del loop alineados: usar la mediana del centro de pies
                mx = int(np.median([p[1] for p in lst]))
                lst = [(im, mx, py) for im, _, py in lst]
            anims[(st, an)] = lst
    # empaquetar en filas
    pad, maxw = 2, 4096
    x = y = pad
    fila_h = 0
    pos = {}
    for k, lst in anims.items():
        for i, (im, px, py) in enumerate(lst):
            if x + im.width + pad > maxw:
                x, y, fila_h = pad, y + fila_h + pad, 0
            pos[(k, i)] = (x, y)
            x += im.width + pad
            fila_h = max(fila_h, im.height)
    atlas = Image.new("RGBA", (maxw, y + fila_h + pad), (0, 0, 0, 0))
    meta = {}
    for k, lst in anims.items():
        st, an = k
        meta.setdefault(st, {})[an] = []
        for i, (im, px, py) in enumerate(lst):
            X, Y = pos[(k, i)]
            atlas.alpha_composite(im, (X, Y))
            meta[st][an].append([X, Y, im.width, im.height, px, py])
    bb = atlas.getbbox()
    atlas = atlas.crop((0, 0, bb[2] + pad, bb[3] + pad))
    os.makedirs("assets", exist_ok=True)
    atlas.save("assets/mantis-sets.webp", quality=84, method=6)
    with open("assets/mantis-sets.json", "w") as f:
        json.dump({"ref": ALTURA_REF, "sets": meta}, f, separators=(",", ":"))
    print("Atlas", atlas.size, os.path.getsize("assets/mantis-sets.webp") // 1024, "KB",
          {st: {an: len(v) for an, v in d.items()} for st, d in meta.items()})


if __name__ == "__main__":
    main()
