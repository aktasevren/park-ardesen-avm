#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Duyurular sayfasını üretir ve menüye ekler.

İçerik panelden geliyor; sayfa yalnızca pa-veri.js'in dolduracağı bir
kap (data-pa-duyurular) barındırıyor. Şablon olarak dönüştürülmüş
`press/index.html` kullanılıyor (aynı başlık/breadcrumb yapısı)."""
import re, os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOSTS = ["www.dubaioutletmall.com", "dubaioutletmall.com"]

GOVDE = '''<div class="container container-small">
<div data-pa-duyurular>
  <p class="pa-bos">Duyurular yükleniyor…</p>
</div>
</div>'''

MENU_OGE = ('<li id="menu-item-pa-duyuru" class="menu-item menu-item-type-post_type '
            'menu-item-object-page menu-item-pa-duyuru">'
            '<a href="{onek}duyurular/index.html">Duyurular</a></li>\n')


def sayfayi_uret(host):
    kaynak = os.path.join(ROOT, host, "press", "index.html")
    if not os.path.isfile(kaynak):
        return False
    s = open(kaynak, encoding="utf-8").read()
    s = s.replace("<h1>Basında Biz</h1>", "<h1>Duyurular</h1>")
    s = re.sub(r"<title>[^<]*</title>",
               "<title>Duyurular &#8211; Park Ardeşen AVM</title>", s, count=1)
    s = s.replace("<span>Basında Biz</span>", "<span>Duyurular</span>")
    s = re.sub(r'(?s)(</div><!-- \.breadcrumbs -->).*?(</main>)',
               lambda m: m.group(1) + "\n" + GOVDE + "\n" + m.group(2), s, count=1)
    hedef = os.path.join(ROOT, host, "duyurular")
    os.makedirs(hedef, exist_ok=True)
    open(os.path.join(hedef, "index.html"), "w", encoding="utf-8").write(s)
    return True


def menuye_ekle():
    n = 0
    for host in HOSTS:
        for dizin, _, dosyalar in os.walk(os.path.join(ROOT, host)):
            for d in dosyalar:
                if d != "index.html" and not d.endswith(".html"):
                    continue
                f = os.path.join(dizin, d)
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


def main():
    uretilen = sum(1 for h in HOSTS if sayfayi_uret(h))
    eklenen = menuye_ekle()
    print("  duyurular sayfası: %d ayna | menüye eklenen: %d dosya" % (uretilen, eklenen))


if __name__ == "__main__":
    main()
