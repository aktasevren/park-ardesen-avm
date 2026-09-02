#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Footer'daki mini haritayı derleme sırasında bir görsel olarak üretir.

Neden gömme (iframe) değil de görsel?
  * Gömme harita her ziyarette üçüncü taraf sunucuya bağlanır; KVKK/GDPR
    açısından rıza gerektirir ve ziyaretçinin IP'sini dışarı verir.
  * OpenStreetMap'in yeni gömme haritası WebGL istiyor; WebGL'i olmayan
    cihaz/tarayıcılarda hata metni görünüyor.
Karo görüntüleri burada bir kez indirilip birleştiriliyor; sitede yalnızca
yerel bir PNG var. Tıklanınca Google Haritalar'da yol tarifi açılıyor.

Koordinat Cumhuriyet Mahallesi merkezidir (Nominatim). Binanın tam konumu
Google Haritalar'daki kayıtlı mekândan alındı.
"""
import math, os, io, urllib.request

KONUM = (41.1913335, 40.9864215)   # PARKARDEŞEN AVM — Google Haritalar
ZOOM = 16
GEN, YUK = 760, 380                # 2x retina; sitede 380x190 gösteriliyor
UA = {"User-Agent": "ParkArdesenAVM-SiteBuild/1.0 (muhasebe@parkardesen.com)"}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEDEF = os.path.join(ROOT, "pa-assets", "gorseller", "harita.png")


def karo(lat, lon, z):
    n = 2 ** z
    lat_r = math.radians(lat)
    return ((lon + 180.0) / 360.0 * n,
            (1.0 - math.log(math.tan(lat_r) + 1 / math.cos(lat_r)) / math.pi) / 2.0 * n)


def main():
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("  Pillow yok, harita üretilemedi (mevcut görsel korunuyor)")
        return

    lat, lon = KONUM
    x, y = karo(lat, lon, ZOOM)
    sol, ust = x * 256 - GEN / 2, y * 256 - YUK / 2
    x0, y0 = int(sol // 256), int(ust // 256)
    x1, y1 = int((sol + GEN) // 256), int((ust + YUK) // 256)

    tuval = Image.new("RGB", ((x1 - x0 + 1) * 256, (y1 - y0 + 1) * 256))
    for tx in range(x0, x1 + 1):
        for ty in range(y0, y1 + 1):
            u = "https://tile.openstreetmap.org/%d/%d/%d.png" % (ZOOM, tx, ty)
            try:
                d = urllib.request.urlopen(
                    urllib.request.Request(u, headers=UA), timeout=30).read()
            except Exception as e:
                print("  karo indirilemedi (%s); mevcut görsel korunuyor" % e)
                return
            tuval.paste(Image.open(io.BytesIO(d)).convert("RGB"),
                        ((tx - x0) * 256, (ty - y0) * 256))

    im = tuval.crop((int(sol - x0 * 256), int(ust - y0 * 256),
                     int(sol - x0 * 256) + GEN, int(ust - y0 * 256) + YUK))

    d = ImageDraw.Draw(im, "RGBA")
    cx, cy = GEN // 2, YUK // 2
    d.ellipse([cx - 16, cy + 6, cx + 16, cy + 16], fill=(0, 0, 0, 60))
    d.polygon([(cx - 9, cy - 6), (cx + 9, cy - 6), (cx, cy + 12)],
              fill=(225, 31, 38, 255))
    d.ellipse([cx - 15, cy - 31, cx + 15, cy - 1], fill=(225, 31, 38, 255),
              outline=(255, 255, 255, 255), width=3)
    d.ellipse([cx - 6, cy - 22, cx + 6, cy - 10], fill=(255, 255, 255, 255))

    os.makedirs(os.path.dirname(HEDEF), exist_ok=True)
    im.save(HEDEF, optimize=True)
    print("  harita görseli: %dx%d, %d KB (© OpenStreetMap katkıcıları)"
          % (im.width, im.height, os.path.getsize(HEDEF) // 1024))


if __name__ == "__main__":
    main()
