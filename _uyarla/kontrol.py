#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Yerel sunucudaki sayfaların kırık referanslarını bulur."""
import re, sys, urllib.parse, urllib.request

BASE = "http://127.0.0.1:8001/www.dubaioutletmall.com/"
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
BELLEK = {}

def durum(url):
    if url in BELLEK: return BELLEK[url]
    try:
        c = OPENER.open(urllib.request.Request(url, method="HEAD"), timeout=15).getcode()
    except Exception as e:
        c = getattr(e, "code", type(e).__name__)
    BELLEK[url] = c
    return c

def kontrol(sayfa):
    u = BASE + sayfa
    try:
        s = OPENER.open(u, timeout=20).read().decode("utf-8", "replace")
    except Exception as e:
        return None, [("(sayfanın kendisi)", getattr(e, "code", e))]
    refs = set()
    for m in re.finditer(r'(?:href|src|data-src)="([^"]+)"', s):
        r = m.group(1)
        if r.startswith(("data:", "#", "mailto:", "tel:", "javascript:", "http")): continue
        refs.add(r)
    for m in re.finditer(r'url\(([^)]+)\)', s):
        r = m.group(1).strip('\'"')
        if not r.startswith(("data:", "http")): refs.add(r)
    bad = [(r, durum(urllib.parse.urljoin(u, r))) for r in sorted(refs)]
    return len(refs), [b for b in bad if b[1] != 200]

if __name__ == "__main__":
    sayfalar = sys.argv[1:] or ["index.html"]
    toplam = 0
    for p in sayfalar:
        n, bad = kontrol(p)
        toplam += len(bad)
        print("%-26s %s referans, %d kırık" % (p, n, len(bad)))
        for r, c in bad[:15]:
            print("   ", c, r)
    sys.exit(1 if toplam else 0)
