#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Çevirileri sözlüğe işler ve anahtarları doğrular.
Kullanım: bir sözlük (dict) verip ekle(...) çağırılır."""
import json, os, re, sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOZLUK = os.path.join(KOK, "_dil", "sozluk.json")


def ekle(yeni):
    """Anahtar ya tam Türkçe metin ya da sözlükteki 1 tabanlı sıra numarası."""
    d = json.load(open(SOZLUK, encoding="utf-8"))
    sira = list(d)
    cozulmus = {}
    for k, v in yeni.items():
        if isinstance(k, int):
            # NOT: sıra numarası, sözlük yeniden çıkarıldığında kayar.
            # Yalnızca aynı oturumda güvenlidir; tercih edilen yol metin önekidir.
            if not (1 <= k <= len(sira)):
                print("!! sıra dışı numara:", k); sys.exit(1)
            cozulmus[sira[k - 1]] = v
        elif k in d:
            cozulmus[k] = v
        else:
            # metin öneki ile benzersiz eşleşme
            adaylar = [t for t in sira if t.startswith(k)]
            if len(adaylar) == 1:
                cozulmus[adaylar[0]] = v
            elif len(adaylar) > 1:
                print("!! önek birden çok metne uyuyor (%d): %r" % (len(adaylar), k[:60]))
                for a in adaylar[:6]:
                    print("     aday: %r" % a[:110])
                sys.exit(1)
            else:
                cozulmus[k] = v   # aşağıda "bilinmeyen" olarak raporlanır
    yeni = cozulmus
    bilinmeyen = [k for k in yeni if k not in d]
    if bilinmeyen:
        print("!! sözlükte olmayan anahtar (%d):" % len(bilinmeyen))
        for k in bilinmeyen[:10]:
            print("   ", repr(k[:80]))
        sys.exit(1)
    # Yazım denetimi: Gürcüce/Arapça metinde Latin harf, yerel harfe
    # AYIRAÇSIZ yapışmışsa bu bir yazım hatasıdır (ör. "კოლიაska").
    # Marka adları boşluk/tire ile ayrıldığı için doğal olarak elenir.
    # yalnız HARFLER: Arapça noktalama (،؛؟) ve rakamlar hariç
    YEREL = r'\u10A0-\u10FF\u1C90-\u1CBF\u0621-\u063A\u0641-\u064A\u0671-\u06D3'
    YAPISIK = re.compile(r'[A-Za-z][' + YEREL + r']|[' + YEREL + r'][A-Za-z]')
    kirli = []
    for k, v in yeni.items():
        for d2 in ("ka", "ar"):
            t = v.get(d2)
            if t and YAPISIK.search(t):
                kirli.append((d2, k[:40], YAPISIK.search(t).group(0), t[:70]))
    if kirli:
        print("!! Latin harf yerel harfe yapışmış (%d):" % len(kirli))
        for d2, k, p2, t in kirli[:8]:
            print("   [%s] %r  …%s…  → %s" % (d2, k, p2, t))
        sys.exit(1)

    n = 0
    for k, v in yeni.items():
        for dil in ("en", "ka", "ar"):
            if v.get(dil):
                if d[k].get(dil) != v[dil]:
                    n += 1
                d[k][dil] = v[dil]
    json.dump(d, open(SOZLUK, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    kalan = sum(1 for v in d.values() if not all(v.get(x) for x in ("en", "ka", "ar")))
    print("işlenen çeviri: %d | eksik kalan metin: %d / %d" % (n, kalan, len(d)))
