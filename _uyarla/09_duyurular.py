#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Duyurular sayfasını üretir ve menüye ekler.

İçerik panelden geliyor; sayfa yalnızca pa-veri.js'in dolduracağı bir
kap (data-pa-duyurular) barındırıyor. Şablon olarak dönüştürülmüş
`press/index.html` kullanılıyor (aynı başlık/breadcrumb yapısı)."""
import re, os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HARIC = ('_yedek-ayna', '_orijinal', '_uyarla', 'panel', 'api', 'pa-assets', '.git', '_dil', 'en', 'ka', 'ar')


def site_dosyalari(desen=("*.html",)):
    """Sitenin dosyaları — yardımcı dizinler hariç."""
    import fnmatch
    out = []
    for kok, dizinler, dosyalar in os.walk(ROOT):
        dizinler[:] = [d for d in dizinler if d not in HARIC]
        for d in dosyalar:
            if any(fnmatch.fnmatch(d, x) for x in desen):
                out.append(os.path.join(kok, d))
    return sorted(out)


GOVDE = '''<div class="container container-small">
<div data-pa-duyurular>
  <p class="pa-bos">Duyurular yükleniyor…</p>
</div>
</div>'''

MENU_OGE = ('<li id="menu-item-pa-duyuru" class="menu-item menu-item-type-post_type '
            'menu-item-object-page menu-item-pa-duyuru">'
            '<a href="{onek}duyurular/index.html">Duyurular</a></li>\n')


def sayfayi_uret():
    """Sayfayı press/ şablonundan üretir.

    press/ siteden kaldırıldığı için şablon artık yok; duyurular/index.html
    ise depoda duruyor ve zincirin geri kalanı (başlık, altbilgi, temizlik,
    SEO, dil sürümleri) onu her koşuda güncelliyor. O yüzden sayfa varsa
    üretim adımı atlanır — eksik bir şey değil."""
    hedef_dosya = os.path.join(ROOT, "duyurular", "index.html")
    kaynak = os.path.join(ROOT, "press", "index.html")
    if not os.path.isfile(kaynak):
        return "mevcut" if os.path.isfile(hedef_dosya) else False
    s = open(kaynak, encoding="utf-8").read()
    s = s.replace("<h1>Basında Biz</h1>", "<h1>Duyurular</h1>")
    s = re.sub(r"<title>[^<]*</title>",
               "<title>Duyurular &#8211; Park Ardeşen AVM</title>", s, count=1)
    s = s.replace("<span>Basında Biz</span>", "<span>Duyurular</span>")
    s = re.sub(r'(?s)(</div><!-- \.breadcrumbs -->).*?(</main>)',
               lambda m: m.group(1) + "\n" + GOVDE + "\n" + m.group(2), s, count=1)
    hedef = os.path.join(ROOT, "duyurular")
    os.makedirs(hedef, exist_ok=True)
    open(os.path.join(hedef, "index.html"), "w", encoding="utf-8").write(s)
    return True


def menuye_ekle():
    n = 0
    for f in site_dosyalari():
        s = open(f, encoding="utf-8", errors="replace").read()
        if "menu-item-pa-duyuru" in s or "primary-menu" not in s:
            continue
        m = re.search(r'<meta name="pa-site-kok" content="([^"]*)">', s)
        onek = m.group(1) if m else ""
        yeni = re.sub(r'(<li[^>]*>\s*<a[^>]*>Kampanyalar</a>\s*</li>\s*)',
                      lambda mm: mm.group(1) + MENU_OGE.format(onek=onek),
                      s, count=1)
        if yeni != s:
            open(f, "w", encoding="utf-8").write(yeni)
            n += 1
    return n


def menuyu_duzelt():
    """Duyurular sayfasının kendi menü öğesini onarır.

    Sayfa press/ klonundan geldiği için menüde "Basında Biz" etiketli, sayfanın
    kendisine giden bir öğe kalmıştı: hem yanlış ad hem de menüye ayrıca eklenen
    "Duyurular" öğesiyle çift kayıt. Eskisi silinip "içinde bulunulan sayfa"
    işareti doğru öğeye taşınıyor — diğer sayfalarda olduğu gibi."""
    f = os.path.join(ROOT, "duyurular", "index.html")
    if not os.path.isfile(f):
        return 0
    s = open(f, encoding="utf-8").read()
    s0 = s
    # press'ten kalan öğeyi sil
    s = re.sub(r'<li[^>]*current-menu-item[^>]*>\s*<a[^>]*>Basında Biz</a>\s*</li>\s*',
               "", s)
    # geçerli sayfa işaretini "Duyurular" öğesine ver
    s = s.replace(
        '<li id="menu-item-pa-duyuru" class="menu-item menu-item-type-post_type '
        'menu-item-object-page menu-item-pa-duyuru">'
        '<a href="../duyurular/index.html">Duyurular</a></li>',
        '<li id="menu-item-pa-duyuru" class="menu-item menu-item-type-post_type '
        'menu-item-object-page menu-item-pa-duyuru current-menu-item current_page_item">'
        '<a href="index.html" aria-current="page">Duyurular</a></li>')
    if s != s0:
        open(f, "w", encoding="utf-8").write(s)
        return 1
    return 0


def main():
    uretilen = sayfayi_uret()
    eklenen = menuye_ekle()
    menuyu_duzelt()
    durum = {True: "üretildi", "mevcut": "yerinde (şablon gerekmedi)",
             False: "ÜRETİLEMEDİ"}[uretilen]
    print("  duyurular sayfası: %s | menüye eklenen: %d dosya" % (durum, eklenen))


if __name__ == "__main__":
    main()
