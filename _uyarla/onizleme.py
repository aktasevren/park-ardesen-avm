#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qlmanage ile tam sayfa önizleme üretir (Chrome kullanmadan).
Kullanım: python3 _uyarla/onizleme.py shops/index.html [zoom]"""
import re, os, sys, subprocess, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIKTI = os.environ.get("ONIZLEME_DIZIN", tempfile.gettempdir())


def hazirla(rel, zoom):
    src = os.path.join(ROOT, "www.dubaioutletmall.com", rel)
    s = open(src, encoding="utf-8").read()
    s = s.replace("</head>",
                  "<style>html{zoom:%s}.home-banner,.home-banner .container"
                  "{min-height:640px!important}</style></head>" % zoom)
    # tembel yükleme JS'siz çalışmaz; data-src'yi src'ye taşı
    s = re.sub(r'src="data:image[^"]*"\s+([^>]*?)data-src="([^"]+)"',
               lambda m: 'src="%s" %s' % (m.group(2), m.group(1)), s)
    s = re.sub(r'data-src="([^"]+)"([^>]*?)\s+src="data:image[^"]*"',
               lambda m: 'src="%s"%s' % (m.group(1), m.group(2)), s)
    s = re.sub(r'(?is)<noscript>.*?</noscript>', '', s)
    hedef = os.path.join(os.path.dirname(src), "_onizleme.html")
    open(hedef, "w", encoding="utf-8").write(s)
    return hedef


def main():
    rel = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    zoom = sys.argv[2] if len(sys.argv) > 2 else ".30"
    tmp = hazirla(rel, zoom)
    png = os.path.join(CIKTI, "_onizleme.html.png")
    if os.path.exists(png):
        os.remove(png)
    subprocess.run(["qlmanage", "-t", "-s", "1400", "-o", CIKTI, tmp],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(tmp)
    ad = os.path.join(CIKTI, rel.replace("/", "_") + ".png")
    if os.path.exists(png):
        os.replace(png, ad)
        print(ad)
    else:
        print("önizleme üretilemedi")


if __name__ == "__main__":
    main()
