#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Türkçe sayfalardan çevrilecek metinleri çıkarır (Park Ardeşen AVM).

Panel yönetim aracıdır, çevrilmez.
"""
import json, os, re, sys, glob, html, collections

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOZLUK = os.path.join(KOK, "_dil", "sozluk.json")

HARIC_DIZIN = ("_orijinal", "_uyarla", "_dil", ".git", "panel", "en", "ka", "ar")


# Mağaza/marka adları çevrilmez
MARKALAR = ['Bargello', 'Berru Park', 'Burger King', 'Defne Cafe & Bar', 'FLO', "Gloria Jean's Coffees", 'Grand Bowling', 'Helvacı Yakub Efendi', 'LC Waikiki', 'Long Street', 'Lux', 'Madame Coco', 'Migros', 'Money', 'Park Kart', 'Paul & Mark', 'Popeyes', 'Sıroğlu Çikolata', 'V&K Prestij', 'İstanbul Gümrk Store']

ATLA_TAM = {
    "Park Ardeşen AVM", "Park Ardeşen", "AVM", "Instagram", "Facebook", "YouTube",
    "OpenStreetMap", "© OpenStreetMap", "Ardeşen", "Rize", "Ardeşen / Rize",
    "YB Global Group", "muhasebe@parkardesen.com", "info@parkardesen.com",
} | set(MARKALAR)
ATLA_DESEN = [
    re.compile(r'^[\d\s.,:+/()\-–—×%°]+$'),
    re.compile(r'^TR\d[\d\s]+$'),
    re.compile(r'^[\w.+-]+@[\w-]+\.[\w.]+$'),
    re.compile(r'^https?://'),
    re.compile(r'^[A-Za-z0-9_-]{20,}$'),
    re.compile(r'^[.]{0,2}/|\.html?$|\.(?:png|jpe?g|svg|webp|css|js)$'),   # yol/dosya adı
    re.compile(r'^\s*$'),
]

ATLA_ETIKET = re.compile(r'(?is)<(script|style|noscript|svg)\b.*?</\1>')
OZNITELIK = ("alt", "placeholder", "aria-label", "title", "value")


def sayfalar():
    out = []
    for kok, dizinler, dosyalar in os.walk(KOK):
        dizinler[:] = [d for d in dizinler if d not in HARIC_DIZIN]
        for d in dosyalar:
            if d.endswith(".html"):
                out.append(os.path.relpath(os.path.join(kok, d), KOK))
    return sorted(out)


def cevrilir_mi(m):
    m = m.strip()
    if not m or m in ATLA_TAM:
        return False
    if not re.search(r'[A-Za-zÇĞİÖŞÜçğıöşü]', m):
        return False
    if any(d.search(m) for d in ATLA_DESEN):
        return False
    return True


def metinleri_cikar(s):
    s = re.sub(r'<div class="yb-dil"[^>]*>.*?</ul></div>', '', s, flags=re.S)
    bulunan = []
    govde = ATLA_ETIKET.sub(lambda m: " " * len(m.group(0)), s)

    for m in re.finditer(r'>([^<>]+)<', govde):
        t = re.sub(r'\s+', ' ', html.unescape(m.group(1))).strip()
        if cevrilir_mi(t):
            bulunan.append((t, "metin"))

    for m in re.finditer(r'(?is)<title>(.*?)</title>', s):
        t = re.sub(r'\s+', ' ', html.unescape(m.group(1))).strip()
        if cevrilir_mi(t):
            bulunan.append((t, "title"))

    for m in re.finditer(r'<meta[^>]*\b(?:name|property)="(?:description|og:title|og:description|twitter:title|twitter:description)"[^>]*>', s):
        c = re.search(r'content="([^"]*)"', m.group(0))
        if c:
            t = html.unescape(c.group(1)).strip()
            if cevrilir_mi(t):
                bulunan.append((t, "meta"))

    for oz in OZNITELIK:
        for m in re.finditer(r'\b' + oz + r'="([^"]*)"', govde):
            t = html.unescape(m.group(1)).strip()
            if cevrilir_mi(t):
                bulunan.append((t, oz))
    return bulunan


def main():
    liste = sayfalar()
    sayac = collections.Counter()
    hepsi = collections.OrderedDict()
    for yol in liste:
        s = open(os.path.join(KOK, yol), encoding="utf-8", errors="replace").read()
        for t, tur in metinleri_cikar(s):
            hepsi.setdefault(t, None)
            sayac[tur] += 1

    eski = json.load(open(SOZLUK, encoding="utf-8")) if os.path.exists(SOZLUK) else {}
    yeni = collections.OrderedDict()
    for t in hepsi:
        yeni[t] = eski.get(t, {"en": "", "ka": "", "ar": ""})
    json.dump(yeni, open(SOZLUK, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    bos = sum(1 for v in yeni.values() if not all(v.get(k) for k in ("en", "ka", "ar")))
    print("sayfa           :", len(liste))
    print("benzersiz metin :", len(yeni))
    print("çevirisi eksik  :", bos)
    for tur, n in sayac.most_common():
        print("   %-12s %d" % (tur, n))


if __name__ == "__main__":
    main()
