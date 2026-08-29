#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Türkçe sayfalardan /en/, /ka/, /ar/ dil sürümlerini üretir (Park Ardeşen AVM).

Derleme zincirinin (tumunu_calistir.sh) son adımıdır: Türkçe sayfalar
oluştuktan sonra çalışır ve dil klasörlerini sıfırdan yazar.
"""
import html, json, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diller import DILLER, VARSAYILAN, dil as dil_bul   # noqa: E402
from bayraklar import BAYRAK                            # noqa: E402

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOZLUK_YOL = os.path.join(KOK, "_dil", "sozluk.json")
SITE_ADRES = "https://park-ardesen-avm.vercel.app"

HARIC = ("_orijinal", "_uyarla", "_dil", ".git", "panel", "en", "ka", "ar", "node_modules")

OZNITELIK = ("alt", "placeholder", "aria-label", "title", "value")
KORUMALI = re.compile(r'(?is)<(script|style|noscript|svg)\b.*?</\1>')
DIS = ("http://", "https://", "//", "data:", "mailto:", "tel:", "#", "javascript:")


def sayfalar():
    out = []
    for kok, dizinler, dosyalar in os.walk(KOK):
        dizinler[:] = [d for d in dizinler if d not in HARIC]
        for d in dosyalar:
            if d.endswith(".html"):
                out.append(os.path.relpath(os.path.join(kok, d), KOK))
    return sorted(out)


SAYFALAR = sayfalar()
SAYFA_KUMESI = set(SAYFALAR)


# ------------------------------------------------------------------ yardımcı
def korumali_araliklar(s):
    return [(m.start(), m.end()) for m in KORUMALI.finditer(s)]


def korumada_mi(araliklar, i):
    for a, b in araliklar:
        if a <= i < b:
            return True
    return False


def kacir(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def kacir_oz(t):
    return kacir(t).replace('"', "&quot;")


# ------------------------------------------------------------------ çeviri
def cevir(s, sozluk, kod):
    araliklar = korumali_araliklar(s)

    def bak(t):
        v = sozluk.get(t)
        return v.get(kod) if v else None

    parcalar, son = [], 0
    for m in re.finditer(r'>([^<>]+)<', s):
        if korumada_mi(araliklar, m.start()):
            continue
        ham = m.group(1)
        duz = re.sub(r'\s+', ' ', html.unescape(ham)).strip()
        if not duz:
            continue
        yeni = bak(duz)
        if not yeni:
            continue
        onek = ham[:len(ham) - len(ham.lstrip())]
        sonek = ham[len(ham.rstrip()):]
        parcalar.append(s[son:m.start() + 1])
        parcalar.append(onek + kacir(yeni) + sonek)
        son = m.end() - 1
    parcalar.append(s[son:])
    s = "".join(parcalar)

    def title_ce(m):
        duz = re.sub(r'\s+', ' ', html.unescape(m.group(1))).strip()
        y = bak(duz)
        return "<title>%s</title>" % kacir(y) if y else m.group(0)
    s = re.sub(r'(?is)<title>(.*?)</title>', title_ce, s)

    def meta_ce(m):
        etiket = m.group(0)
        c = re.search(r'content="([^"]*)"', etiket)
        if not c:
            return etiket
        y = bak(html.unescape(c.group(1)).strip())
        if not y:
            return etiket
        return etiket[:c.start(1)] + kacir_oz(y) + etiket[c.end(1):]
    s = re.sub(r'<meta[^>]*\b(?:name|property)="(?:description|og:title|og:description'
               r'|twitter:title|twitter:description)"[^>]*>', meta_ce, s)

    for oz in OZNITELIK:
        araliklar = korumali_araliklar(s)
        parcalar, son = [], 0
        for m in re.finditer(r'\b' + oz + r'="([^"]*)"', s):
            if korumada_mi(araliklar, m.start()):
                continue
            y = bak(html.unescape(m.group(1)).strip())
            if not y:
                continue
            parcalar.append(s[son:m.start(1)])
            parcalar.append(kacir_oz(y))
            son = m.end(1)
        parcalar.append(s[son:])
        s = "".join(parcalar)
    return s


# ------------------------------------------------------------------ yollar
def yollari_duzelt(s, klasor, sayfa):
    """Göreli yolları kök-mutlak yapar; sayfa bağlantılarını dil klasörüne alır."""
    dizin = os.path.dirname(sayfa)
    onek = "/" + klasor + "/" if klasor else "/"

    def duzelt(deger):
        if not deger or deger.startswith(DIS) or deger.startswith("/"):
            return deger
        yol, _, capa = deger.partition("#")
        capa = ("#" + capa) if capa else ""
        if not yol:
            return deger
        mutlak = os.path.normpath(os.path.join(dizin, yol))
        if mutlak in SAYFA_KUMESI:
            return onek + mutlak + capa
        return "/" + mutlak.replace(os.sep, "/") + capa

    # çift ve tek tırnaklı öznitelikler
    s = re.sub(r'((?:src|href|poster|data-src)=")([^"]*)(")',
               lambda m: m.group(1) + duzelt(m.group(2)) + m.group(3), s)
    s = re.sub(r"((?:src|href|poster|data-src)=')([^']*)(')",
               lambda m: m.group(1) + duzelt(m.group(2)) + m.group(3), s)

    def url_ce(m):
        d = m.group(2).strip()
        if d.startswith("#") or d.startswith("%23"):
            return m.group(0)
        return m.group(1) + duzelt(d) + m.group(3)
    s = re.sub(r'(url\(\s*["\']?)([^"\')]+)(["\']?\s*\))', url_ce, s)

    def srcset_ce(m):
        parts = []
        for p in m.group(2).split(","):
            p = p.strip()
            if not p:
                continue
            a = p.split()
            a[0] = duzelt(a[0])
            parts.append(" ".join(a))
        return m.group(1) + ", ".join(parts) + m.group(3)
    s = re.sub(r'(srcset=")([^"]*)(")', srcset_ce, s)

    # panel verisi ve site kökü artık kök-mutlak
    s = re.sub(r'(<meta name="pa-veri-url" content=")[^"]*(")', r'\g<1>/panel/veri.json\g<2>', s)
    s = re.sub(r'(<meta name="pa-site-kok" content=")[^"]*(")', r'\g<1>/\g<2>', s)
    return s


# ------------------------------------------------------------------ baş etiketleri
def html_kokunu_ayarla(s, d):
    def ce(m):
        etiket = m.group(0)
        etiket = re.sub(r'\slang="[^"]*"', '', etiket)
        etiket = re.sub(r'\sdir="[^"]*"', '', etiket)
        return etiket[:-1].rstrip() + ' lang="%s" dir="%s">' % (d["lang"], d["yon"])
    return re.sub(r'<html\b[^>]*>', ce, s, count=1)


def hreflang_ekle(s, sayfa):
    baglar = []
    for d in DILLER:
        yol = ("/" + d["klasor"] + "/" if d["klasor"] else "/") + sayfa
        baglar.append('<link rel="alternate" hreflang="%s" href="%s%s"/>' % (d["lang"], SITE_ADRES, yol))
    baglar.append('<link rel="alternate" hreflang="x-default" href="%s/%s"/>' % (SITE_ADRES, sayfa))
    s = re.sub(r'<link rel="alternate" hreflang="[^"]*"[^>]*>', '', s)
    return s.replace("</head>", "".join(baglar) + "</head>", 1)


def canonical_ayarla(s, klasor, sayfa):
    tam = SITE_ADRES + ("/" + klasor + "/" if klasor else "/") + sayfa
    if re.search(r'<link rel="canonical"', s):
        return re.sub(r'(<link rel="canonical"[^>]*href=")[^"]*(")',
                      lambda m: m.group(1) + tam + m.group(2), s)
    return s.replace("</head>", '<link rel="canonical" href="%s"/></head>' % tam, 1)


def og_url_ayarla(s, klasor, sayfa):
    tam = SITE_ADRES + ("/" + klasor + "/" if klasor else "/") + sayfa
    return re.sub(r'(<meta[^>]*property="og:url"[^>]*content=")[^"]*(")',
                  lambda m: m.group(1) + tam + m.group(2), s)


# ------------------------------------------------------------------ dil seçici
def secici_html(aktif_kod, sayfa):
    ak = dil_bul(aktif_kod)
    ogeler = []
    for d in DILLER:
        yol = ("/" + d["klasor"] + "/" if d["klasor"] else "/") + sayfa
        secili = ' aria-current="true"' if d["kod"] == aktif_kod else ''
        ogeler.append('<li><a href="%s" hreflang="%s" lang="%s"%s>'
                      '<span class="yb-bayrak">%s</span><span>%s</span></a></li>'
                      % (yol, d["lang"], d["lang"], secili, BAYRAK[d["kod"]], d["ad"]))
    return ('<div class="yb-dil" data-yb-dil>'
            '<button type="button" class="yb-dil-btn" aria-haspopup="listbox" '
            'aria-expanded="false" aria-label="%s"><span class="yb-bayrak">%s</span>'
            '<span class="yb-dil-kod">%s</span></button>'
            '<ul class="yb-dil-liste" role="listbox">%s</ul></div>'
            % (ak["ad"], BAYRAK[aktif_kod], ak["kisa"], "".join(ogeler)))


def seciciyi_yerlestir(s, kod, sayfa):
    s = re.sub(r'<div class="yb-dil"[^>]*>.*?</ul></div>', '', s, flags=re.S)
    blok = secici_html(kod, sayfa)
    m = re.search(r'(<div class="site-header-right">)', s)
    if m:
        return s[:m.end()] + blok + s[m.end():]
    return s


def pa_dil_betigi(s, klasor):
    """pa-dil.js'i pa-veri.js'ten ÖNCE yerleştirir (paT/paMetin orada tanımlı).
    Derleme zincirinin ara adımları sayfaları yeniden üretebildiği için bu iş
    en sona, buraya alındı."""
    s = re.sub(r'\s*<script src="[^"]*pa-dil\.js"></script>', '', s)
    onek = "/" if klasor else ""
    # Türkçe kökte göreli, dil klasörlerinde kök-mutlak yollar kullanılıyor
    m = re.search(r'<script src="([^"]*)pa-veri\.js"></script>', s)
    if not m:
        return s
    yol = m.group(1) + "pa-dil.js"
    return s[:m.start()] + '<script src="%s"></script>\n' % yol + s[m.start():]


def varliklari_ekle(s, d):
    ek = '<link rel="stylesheet" href="/wp-content/uploads/pa/dil.css"/>'
    if d["kod"] in ("ka", "ar"):
        ek += '<link rel="stylesheet" href="/wp-content/uploads/pa/yazitipi-%s.css"/>' % d["kod"]
    if d["yon"] == "rtl":
        ek += '<link rel="stylesheet" href="/wp-content/uploads/pa/rtl.css"/>'
    ek += '<meta name="pa-dil" content="%s"/>' % d["kod"]
    s = re.sub(r'<meta name="pa-dil"[^>]*>', '', s)
    s = s.replace("</head>", ek + "</head>", 1)
    return s.replace("</body>", '<script src="/wp-content/uploads/pa/dil.js"></script></body>', 1)





def temizle_onceki(s):
    s = re.sub(r'<div class="yb-dil"[^>]*>.*?</ul></div>', '', s, flags=re.S)
    s = re.sub(r'<link rel="stylesheet" href="/wp-content/uploads/pa/(?:dil|rtl|yazitipi-[a-z]{2})\.css"/>', '', s)
    s = re.sub(r'<meta name="pa-dil"[^>]*>', '', s)
    s = s.replace('<script src="/wp-content/uploads/pa/dil.js"></script>', '')
    return s


# ------------------------------------------------------------------ ana akış
def main():
    sozluk = json.load(open(SOZLUK_YOL, encoding="utf-8"))
    eksik = [k for k, v in sozluk.items() if not all(v.get(x) for x in ("en", "ka", "ar"))]
    if eksik:
        print("  UYARI: %d metnin çevirisi eksik" % len(eksik))

    for d in DILLER:
        if d["kod"] == VARSAYILAN:
            for sayfa in SAYFALAR:
                yol = os.path.join(KOK, sayfa)
                s0 = open(yol, encoding="utf-8").read()
                s = temizle_onceki(s0)
                s = seciciyi_yerlestir(s, "tr", sayfa)
                s = pa_dil_betigi(s, "")
                s = varliklari_ekle(s, d)
                s = hreflang_ekle(s, sayfa)
                s = canonical_ayarla(s, "", sayfa)
                s = og_url_ayarla(s, "", sayfa)
                if s != s0:
                    open(yol, "w", encoding="utf-8").write(s)
            print("  tr  → kök (%d sayfa)" % len(SAYFALAR))
            continue

        hedef = os.path.join(KOK, d["klasor"])
        if os.path.isdir(hedef):
            shutil.rmtree(hedef)
        for sayfa in SAYFALAR:
            s = open(os.path.join(KOK, sayfa), encoding="utf-8").read()
            s = temizle_onceki(s)
            s = cevir(s, sozluk, d["kod"])
            s = yollari_duzelt(s, d["klasor"], sayfa)
            s = html_kokunu_ayarla(s, d)
            s = seciciyi_yerlestir(s, d["kod"], sayfa)
            s = pa_dil_betigi(s, d["klasor"])
            s = varliklari_ekle(s, d)
            s = hreflang_ekle(s, sayfa)
            s = canonical_ayarla(s, d["klasor"], sayfa)
            s = og_url_ayarla(s, d["klasor"], sayfa)
            cikti = os.path.join(hedef, sayfa)
            os.makedirs(os.path.dirname(cikti), exist_ok=True)
            open(cikti, "w", encoding="utf-8").write(s)
        print("  %-3s → /%s/ (%d sayfa)" % (d["kod"], d["klasor"], len(SAYFALAR)))


if __name__ == "__main__":
    main()
