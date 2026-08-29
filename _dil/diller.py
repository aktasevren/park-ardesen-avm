#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dil tanımları — iki sitede de aynı."""

# kod, klasör, HTML lang, yön, ad (kendi dilinde), bayrak dosyası
DILLER = [
    {"kod": "tr", "klasor": "",   "lang": "tr-TR", "yon": "ltr", "ad": "Türkçe",   "kisa": "TR"},
    {"kod": "en", "klasor": "en", "lang": "en",    "yon": "ltr", "ad": "English",  "kisa": "EN"},
    {"kod": "ka", "klasor": "ka", "lang": "ka",    "yon": "ltr", "ad": "ქართული",  "kisa": "KA"},
    {"kod": "ar", "klasor": "ar", "lang": "ar",    "yon": "rtl", "ad": "العربية",   "kisa": "AR"},
]

VARSAYILAN = "tr"
DIL_KODLARI = [d["kod"] for d in DILLER]


def dil(kod):
    for d in DILLER:
        if d["kod"] == kod:
            return d
    raise KeyError(kod)
