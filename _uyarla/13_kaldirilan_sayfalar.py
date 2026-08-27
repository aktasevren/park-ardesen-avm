#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Siteden çıkarılan sayfaları menülerden ve iç bağlantılardan temizler.

Broşürler, Basında Biz, Medya Merkezi ve Çalışma Saatleri sayfaları
kaldırıldı. Çalışma saatleri bilgisi zaten İletişim ve SSS sayfalarında,
ulaşım bilgisi de Ulaşım sayfasında duruyor.
"""
import re, os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HARIC = ('_orijinal', '_uyarla', 'panel', 'api', 'pa-assets', '.git')

KALDIRILAN = ["brochure", "press", "media-center", "bus-schedule"]

# Kaldırılan sayfalara giden bağlantıların yerine geçecek sayfalar
YONLENDIR = {
    "media-center": "shops",       # görseller yerine mağaza rehberi
    "press":        "duyurular",
    "brochure":     "mall-map",    # broşür yerine kat planı
    "bus-schedule": "contact-us",  # çalışma saatleri kartı burada
}


def dosyalar():
    out = []
    for kok, dz, ds in os.walk(ROOT):
        dz[:] = [d for d in dz if d not in HARIC]
        out += [os.path.join(kok, d) for d in ds if d.endswith(".html")]
    return sorted(out)


def menuden_cikar(s):
    """Kaldırılan sayfalara işaret eden <li> menü öğelerini siler."""
    n = 0
    for ad in KALDIRILAN:
        desen = re.compile(
            r'<li[^>]*>\s*<a[^>]*href="[^"]*(?:^|/)?%s/index\.html"[^>]*>.*?</a>\s*</li>\s*'
            % re.escape(ad), re.S)
        s, k = desen.subn("", s)
        n += k
    return s, n


def baglantilari_yonlendir(s, onek):
    """Menü dışında kalan bağlantıları (kart, buton) hedef sayfaya çevirir."""
    n = 0
    for eski, yeni in YONLENDIR.items():
        desen = re.compile(r'href="((?:\.\./)*)%s/index\.html"' % re.escape(eski))
        s, k = desen.subn(lambda m: 'href="%s%s/index.html"' % (m.group(1), yeni), s)
        n += k
    return s, n


def iletisim_kartlari(s):
    """İletişim sayfasındaki 'Bize doğrudan ulaşın' kartlarının başlıkları."""
    s = s.replace("<h3>Medya Merkezi</h3>", "<h3>Mağazalar</h3>")
    s = s.replace("<h3>Basında Biz</h3>", "<h3>Duyurular</h3>")
    return s


def veri_json():
    """Panelde girilen duyuruların kaldırılan sayfaya işaret eden
    bağlantılarını düzeltir."""
    p = os.path.join(ROOT, "panel", "veri.json")
    if not os.path.isfile(p):
        return 0
    d = json.load(open(p, encoding="utf-8"))
    n = 0
    for duyuru in d.get("duyurular", []):
        bag = (duyuru.get("bagUrl") or "").strip("/")
        if bag in YONLENDIR:
            duyuru["bagUrl"] = YONLENDIR[bag] + "/"
            n += 1
    if n:
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return n


def main():
    menu = bag = 0
    for f in dosyalar():
        s0 = open(f, encoding="utf-8", errors="replace").read()
        s, a = menuden_cikar(s0)
        s, b = baglantilari_yonlendir(s, "")
        s = iletisim_kartlari(s)
        if s != s0:
            open(f, "w", encoding="utf-8").write(s)
        menu += a; bag += b
    v = veri_json()
    print("  kaldırılan sayfa bağlantıları: %d menü öğesi, %d bağlantı, "
          "%d duyuru bağlantısı" % (menu, bag, v))


if __name__ == "__main__":
    main()
