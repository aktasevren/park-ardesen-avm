#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Golos Text'in bozuk ğ/Ğ gliflerini onarır.

Temanın (ve Google Fonts'taki üst kaynağın) Golos Text sürümünde
`gbreve` ve `Gbreve` yalnızca `g` / `G` bileşenini içeriyor; breve
işareti eksik. Sonuç: Türkçe metinde "mağaza" yerine "magaza" görünüyor.
Fontta breve glifi (uni0306 / uni0306.case) mevcut olduğu için eksik
bileşeni yerine ekliyoruz.
"""
import os, glob, shutil
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphComponent
from fontTools.pens.boundsPen import BoundsPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESEN = "*/wp-content/themes/dubaioutletmall/assets/css/fonts/GolosText-*.woff*"


def merkez(gs, ad):
    bp = BoundsPen(gs)
    gs[ad].draw(bp)
    x0, _, x1, _ = bp.bounds
    return (x0 + x1) / 2.0


def onar(yol):
    t = TTFont(yol)
    glyf, gs = t["glyf"], t.getGlyphSet()
    ordu = set(t.getGlyphOrder())
    ornek = glyf["abreve"].components[1]           # bayrakları kopyalamak için
    degisti = []
    for hedef, taban, aksan in (("gbreve", "g", "uni0306"),
                                ("Gbreve", "G", "uni0306.case")):
        if hedef not in ordu or aksan not in ordu:
            continue
        gl = glyf[hedef]
        if gl.isComposite() and len(gl.components) > 1:
            continue                                # zaten sağlam
        dx = merkez(gs, taban) - merkez(gs, aksan)
        c = GlyphComponent()
        c.glyphName = aksan
        c.x, c.y = int(round(dx)), 0
        c.flags = ornek.flags
        gl.components = [gl.components[0], c]
        degisti.append(hedef)
    if degisti:
        t.flavor = "woff2" if yol.endswith(".woff2") else "woff"
        t.save(yol)
    return degisti


def main():
    n = 0
    for f in sorted(glob.glob(os.path.join(ROOT, DESEN))):
        d = onar(f)
        if d:
            n += 1
            print("  %-26s onarıldı: %s" % (os.path.basename(f), ", ".join(d)))
    if not n:
        print("  onarılacak font bulunamadı (zaten düzeltilmiş olabilir)")



if __name__ == "__main__":
    main()
