#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Klon artıklarını temizler: Cloudflare Rocket Loader + ölü eklenti dosyaları.

Kaynak site Cloudflare Rocket Loader kullanıyordu: tüm <script> etiketlerinin
type'ı `type="<hash>-text/javascript"` olarak değiştirilmiş ve satır içi olay
işleyicilerinin başına `if (!window.__cfRLUnblockHandlers) return false;`
eklenmişti. Bu betikleri normalde `rocket-loader.min.js` geri çeviriyordu;
o dosya klonda yok (ve zaten çevrimdışı çalışmazdı), dolayısıyla hiçbir JS
çalışmıyordu: menü açılmıyor, lazyload devreye girmediği için ikon ve
görseller boş kalıyordu.
"""
import re, os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOSTS = ["www.dubaioutletmall.com", "dubaioutletmall.com"]

TIP = re.compile(r'type="[0-9a-fA-F]{16,}-(text/javascript|module|application/json)"')
GUARD = re.compile(r'if \(!window\.__cfRLUnblockHandlers\) return false;\s*')
NITELIK = re.compile(r'\s*data-cf-modified-[0-9a-fA-F]*-?=""')
ROCKET = re.compile(r'<script[^>]*cdn-cgi/scripts/[^>]*>\s*</script>')

# insta-gallery eklentisinin dosyaları kaynak sunucuda da 404 dönüyor ve
# Instagram akışının yerine kendi galerimizi koyduk; etiketleri kaldırıyoruz.
INSTA = re.compile(
    r'\s*<(?:link|script)[^>]*insta-gallery[^>]*?(?:/>|>\s*</script>|>)', re.I)
INSTA_INLINE = re.compile(
    r'\s*<script[^>]*id=["\']qligg-[^"\']*["\'][^>]*>.*?</script>', re.I | re.S)
INSTA_VAR = re.compile(
    r'\s*<script[^>]*>\s*var qligg[^<]*</script>', re.I | re.S)


def main():
    dosyalar = []
    for h in HOSTS:
        dosyalar += glob.glob(os.path.join(ROOT, h, "**", "*.html"), recursive=True)
    n = toplam = 0
    for f in sorted(dosyalar):
        s0 = open(f, encoding="utf-8", errors="replace").read()
        s = TIP.sub(lambda m: 'type="%s"' % m.group(1), s0)
        s = GUARD.sub("", s)
        s = NITELIK.sub("", s)
        s = ROCKET.sub("", s)
        s = INSTA_INLINE.sub("", s)
        s = INSTA_VAR.sub("", s)
        s = INSTA.sub("", s)
        if s != s0:
            open(f, "w", encoding="utf-8").write(s)
            n += 1
            toplam += len(TIP.findall(s0)) + len(GUARD.findall(s0))
    print("  %d dosyada %d Rocket Loader izi temizlendi" % (n, toplam))


if __name__ == "__main__":
    main()
