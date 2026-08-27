#!/bin/zsh
# Park Ardeşen AVM uyarlama zinciri — sıfırdan yeniden kurar.
set -e
cd "$(dirname "$0")/.."

echo "→ _orijinal/ yedeklerinden sayfa gövdeleri geri yükleniyor"
for f in _orijinal/*.html; do
  b=$(basename "$f" .html)
  case "$b" in
    privacy-policy) cp "$f" gizlilik-politikasi/index.html ;;
    terms)          cp "$f" kullanim-kosullari/index.html ;;
    *) [ -d "$b" ] && cp "$f" "$b/index.html" ;;
  esac
done

for s in 08_cloudflare 01_global 02_anasayfa 03_magazalar 04_sayfalar 05_ek_sayfalar 09_duyurular 06_baglantilar 10_temizlik 11_seo 12_yasal 07_font_duzelt; do
  echo "→ $s"
  python3 "_uyarla/$s.py"
done
echo "→ bitti"
