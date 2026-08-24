#!/bin/zsh
# Park Ardeşen AVM uyarlama zinciri — sıfırdan yeniden kurar.
set -e
cd "$(dirname "$0")/.."

echo "→ _orijinal/ yedeklerinden sayfa gövdeleri geri yükleniyor"
for f in _orijinal/*.html; do
  b=$(basename "$f" .html)
  case "$b" in
    privacy-policy) cp "$f" dubaioutletmall.com/privacy-policy-2/index.html ;;
    terms)          cp "$f" dubaioutletmall.com/terms-and-conditions/index.html ;;
    *)
      [ -d "www.dubaioutletmall.com/$b" ] && cp "$f" "www.dubaioutletmall.com/$b/index.html"
      [ -d "dubaioutletmall.com/$b" ]     && cp "$f" "dubaioutletmall.com/$b/index.html"
      ;;
  esac
done

for s in 08_cloudflare 01_global 02_anasayfa 03_magazalar 04_sayfalar 05_ek_sayfalar 06_baglantilar 07_font_duzelt; do
  echo "→ $s"
  python3 "_uyarla/$s.py"
done
echo "→ bitti"
