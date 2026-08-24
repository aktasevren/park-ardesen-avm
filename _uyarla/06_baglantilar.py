#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kalan mutlak dubaioutletmall.com adreslerini yerel göreli yollara çevirir."""
import re, os, glob, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOSTS = ["www.dubaioutletmall.com", "dubaioutletmall.com"]

MUTLAK = re.compile(r'https?://(?:www\.)?dubaioutletmall\.com/[^"\'\s)<>]*')


def coz(url):
    p = urllib.parse.urlsplit(url)
    yol = urllib.parse.unquote(p.path)
    yol = re.sub(r'/{2,}', '/', yol)          # //deals/ → /deals/
    adaylar = []
    for h in ([p.netloc] + [x for x in HOSTS if x != p.netloc]):
        t = os.path.join(ROOT, h, yol.lstrip('/'))
        adaylar += [t, os.path.join(t, "index.html")]
    for a in adaylar:
        if os.path.isfile(a):
            return a
    # Kaynak sitede bazı <link rel=preload> adresleri sayfa yolunu da içeriyor
    # (ör. /shops/wp-content/themes/.../logo-decor.svg). wp-content veya
    # wp-includes'tan itibaren kesip yeniden dene.
    m = re.search(r'(wp-(?:content|includes)/.*)$', yol)
    if m:
        for h in HOSTS:
            t = os.path.join(ROOT, h, m.group(1))
            if os.path.isfile(t):
                return t
    return None


def main():
    tot = dosya = 0
    dosyalar = []
    for h in HOSTS:
        dosyalar += glob.glob(os.path.join(ROOT, h, "**", "*.html"), recursive=True)
        dosyalar += glob.glob(os.path.join(ROOT, h, "**", "*.css"), recursive=True)
    for f in sorted(dosyalar):
        s0 = open(f, encoding="utf-8", errors="replace").read()
        d = os.path.dirname(f)
        sayac = [0]

        def rep(m):
            hedef = coz(m.group(0))
            if not hedef:
                return m.group(0)
            sayac[0] += 1
            return os.path.relpath(hedef, d).replace(os.sep, "/")

        s = MUTLAK.sub(rep, s0)
        if s != s0:
            open(f, "w", encoding="utf-8").write(s)
            tot += sayac[0]; dosya += 1
    print("  %d dosyada %d mutlak bağlantı yerelleştirildi" % (dosya, tot))


if __name__ == "__main__":
    main()
