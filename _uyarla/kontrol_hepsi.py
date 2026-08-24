#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tüm sayfalardaki yerel referansları tarar ve kırık olanları listeler."""
import re, os, glob, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABAN = "http://127.0.0.1:8001/"
ACICI = urllib.request.build_opener(urllib.request.ProxyHandler({}))
BELLEK = {}


def durum(url):
    if url not in BELLEK:
        try:
            BELLEK[url] = ACICI.open(urllib.request.Request(url, method="HEAD"), timeout=15).getcode()
        except Exception as e:
            BELLEK[url] = getattr(e, "code", type(e).__name__)
    return BELLEK[url]


def main():
    dosyalar = []
    for h in ("www.dubaioutletmall.com", "dubaioutletmall.com"):
        dosyalar += glob.glob(os.path.join(ROOT, h, "**", "*.html"), recursive=True)
    toplam = kirik = 0
    for f in sorted(dosyalar):
        rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
        u = TABAN + urllib.parse.quote(rel)
        s = open(f, encoding="utf-8", errors="replace").read()
        refs = set()
        for m in re.finditer(r'(?:href|src|data-src)="([^"]+)"', s):
            r = m.group(1)
            if r.startswith(("data:", "#", "mailto:", "tel:", "javascript:", "http")):
                continue
            refs.add(r.split("&quot;")[0])
        for m in re.finditer(r'url\(([^)]+)\)', s):
            r = m.group(1).strip('\'"')
            if not r.startswith(("data:", "http")):
                refs.add(r)
        bad = []
        for r in refs:
            hedef = urllib.parse.urljoin(u, r)
            hedef = urllib.parse.quote(hedef, safe=":/?#[]@!$&'()*+,;=%~")
            c = durum(hedef)
            if c != 200:
                bad.append((r, c))
        toplam += len(refs); kirik += len(bad)
        if bad:
            print("%s  (%d kırık)" % (rel, len(bad)))
            for r, c in sorted(bad)[:8]:
                print("    ", c, r)
    print("\n%d dosya, %d referans, %d kırık" % (len(dosyalar), toplam, kirik))
    return 1 if kirik else 0


if __name__ == "__main__":
    sys.exit(main())
