"""Separa la guadaña del cuerpo en los cuadros base de la Mantis para poder animar el arma por código.

Uso:
    python3 tools/armar_armas.py        (después de tools/armar_mantis_sets.py)

Para cada arte sin hoja de combate propia toma el cuadro 0 de la caminata (frente y espalda) y:
  1. arma una máscara del arma: una franja a lo largo del mango (de la punta inferior a la cabeza)
     más un polígono alrededor de la hoja,
  2. CUERPO: borra esa máscara y rellena el hueco (inpaint) para que quede el insecto sin arma,
  3. ARMA: recorta la hoja original y dibuja el mango completo (aunque el cuerpo lo tapaba),
  4. guarda el punto de agarre (la mano) para girar el arma desde ahí.

Salida: assets/mantis-armas.webp y assets/mantis-armas.json
  {"art":{"walkF":{"body":[x,y,w,h],"weap":[x,y,w,h],"grip":[gx,gy]}}}  (coordenadas del cuadro original)
"""
import json
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw

# arte, anim: mango (punta inferior, cabeza), medio ancho, polígono de la hoja, agarre
ARMAS = {
    ("ambar", "walkF"): dict(p0=(2, 224), p1=(244, 58), hw=6,
                             hoja=[(225, 0), (329, 0), (329, 200), (288, 200), (255, 70), (225, 64)], grip=(182, 100)),
    ("ambar", "walkB"): dict(p0=(5, 230), p1=(258, 48), hw=6,
                             hoja=[(215, 15), (310, 15), (310, 188), (282, 188), (245, 70), (215, 40)], grip=(180, 107)),
    ("dorado", "walkF"): dict(p0=(335, 255), p1=(60, 90), hw=6,
                              hoja=[(15, 0), (190, 0), (190, 18), (110, 30), (80, 70), (60, 95), (25, 95)], grip=(150, 135)),
    ("dorado", "walkB"): dict(p0=(332, 260), p1=(32, 66), hw=6,
                              hoja=[(15, 0), (210, 0), (210, 20), (150, 45), (110, 70), (60, 100), (15, 100)], grip=(110, 110)),
    ("ciempies", "walkB"): dict(p0=(292, 235), p1=(7, 55), hw=6,
                                hoja=[(0, 0), (160, 0), (160, 20), (110, 35), (70, 70), (30, 100), (0, 100)], grip=(90, 110)),
}


def mascara(w, h, d):
    m = Image.new("L", (w, h), 0)
    g = ImageDraw.Draw(m)
    g.line([d["p0"], d["p1"]], fill=255, width=int(d["hw"] * 2 + 1))
    g.polygon(d["hoja"], fill=255)
    return np.asarray(m) > 0


def main():
    A = Image.open("assets/mantis-sets.webp").convert("RGBA")
    M = json.load(open("assets/mantis-sets.json"))["sets"]
    piezas, meta = [], {}
    for (art, an), d in ARMAS.items():
        x, y, w, h, ax, ay = M[art][an][0]
        fr = np.asarray(A.crop((x, y, x + w, y + h))).copy()
        mk = mascara(w, h, d)
        # cuerpo sin arma: se rellena color y transparencia desde alrededor
        rgb = cv2.cvtColor(fr[..., :3], cv2.COLOR_RGB2BGR)
        mk8 = (mk * 255).astype(np.uint8)
        mk8 = cv2.dilate(mk8, np.ones((5, 5), np.uint8))
        rgb2 = cv2.inpaint(rgb, mk8, 7, cv2.INPAINT_TELEA)
        # transparencia: el hueco se rellena solo donde hay cuerpo de los dos lados (cierre morfológico)
        resto = np.where(mk8 > 0, 0, fr[..., 3]).astype(np.uint8)
        k = int(d["hw"] * 2 + 9)
        cerrado = cv2.morphologyEx(resto, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
        al2 = np.where(mk8 > 0, cerrado, fr[..., 3]).astype(np.uint8)
        cuerpo = np.dstack([cv2.cvtColor(rgb2, cv2.COLOR_BGR2RGB), al2])
        # arma: hoja original + mango completo dibujado
        hoja_m = np.asarray(Image.new("L", (w, h), 0)) > 0
        hm = Image.new("L", (w, h), 0)
        ImageDraw.Draw(hm).polygon(d["hoja"], fill=255)
        hoja_m = np.asarray(hm) > 0
        arma = np.zeros_like(fr)
        arma[hoja_m] = fr[hoja_m]
        # color del mango: mediana de los píxeles visibles cerca de la punta inferior
        p0, p1 = np.array(d["p0"], float), np.array(d["p1"], float)
        cols = []
        for t in np.linspace(0, .18, 40):
            px, py = (p0 + (p1 - p0) * t).astype(int)
            if 0 <= px < w and 0 <= py < h and fr[py, px, 3] > 200:
                cols.append(fr[py, px, :3])
        base = np.median(cols, 0) if cols else np.array([80, 55, 40])
        im = Image.fromarray(arma)
        g = ImageDraw.Draw(im)
        ww = int(d["hw"] * 2)
        osc = tuple(int(c * .45) for c in base) + (255,)
        g.line([d["p0"], d["p1"]], fill=osc, width=ww + 2)
        g.line([d["p0"], d["p1"]], fill=tuple(int(c) for c in base) + (255,), width=ww)
        lu = tuple(int(min(255, c * 1.5 + 20)) for c in base) + (255,)
        v = (p1 - p0) / np.linalg.norm(p1 - p0)
        nrm = np.array([-v[1], v[0]]) * (ww * .25)
        g.line([tuple(p0 + nrm), tuple(p1 + nrm)], fill=lu, width=max(1, ww // 3))
        # la hoja va encima del mango
        arr = np.asarray(im).copy()
        arr[hoja_m & (fr[..., 3] > 30)] = fr[hoja_m & (fr[..., 3] > 30)]
        arma_im = Image.fromarray(arr)
        bb = arma_im.getbbox()
        arma_c = arma_im.crop(bb)
        piezas.append(((art, an, "body"), Image.fromarray(cuerpo), (0, 0)))
        piezas.append(((art, an, "weap"), arma_c, (bb[0], bb[1])))
        meta.setdefault(art, {})[an] = {"grip": list(d["grip"]), "woff": [bb[0], bb[1]]}
    pad, x, y, fila, maxw = 2, 2, 2, 0, 2048
    pos = {}
    for k, im, _ in piezas:
        if x + im.width + pad > maxw:
            x, y, fila = pad, y + fila + pad, 0
        pos[k] = (x, y)
        x += im.width + pad
        fila = max(fila, im.height)
    atlas = Image.new("RGBA", (maxw, y + fila + pad), (0, 0, 0, 0))
    for k, im, _ in piezas:
        atlas.alpha_composite(im, pos[k])
        art, an, kind = k
        meta[art][an][kind] = [pos[k][0], pos[k][1], im.width, im.height]
    bb = atlas.getbbox()
    atlas = atlas.crop((0, 0, bb[2] + pad, bb[3] + pad))
    atlas.save("assets/mantis-armas.webp", quality=86, method=6)
    json.dump(meta, open("assets/mantis-armas.json", "w"), separators=(",", ":"))
    print("Armas:", atlas.size, os.path.getsize("assets/mantis-armas.webp") // 1024, "KB")


if __name__ == "__main__":
    main()
