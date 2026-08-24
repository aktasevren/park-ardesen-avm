#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bir sayfanın görünen metnini dökümler (kontrol amaçlı)."""
import re, sys, html
for p in sys.argv[1:]:
    s = open('%s/index.html' % p if p != '.' else 'index.html',
             encoding='utf-8').read()
    i = s.find('<main'); j = s.find('<footer')
    b = re.sub(r'(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>', ' ', s[i:j])
    t = html.unescape(re.sub(r'(?s)<[^>]+>', '\n', b))
    L = [l.strip() for l in re.sub(r'[ \t\xa0]+', ' ', t).split('\n') if l.strip()]
    print("=" * 60); print("###", p, "—", len(L), "satır"); print("=" * 60)
    print('\n'.join(L))
