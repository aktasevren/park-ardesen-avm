#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Klondan kalan WordPress/Dubai Outlet Mall artıklarını sayfalardan siler.

Kaldırılan eklentilerin (WooCommerce, Gravity Forms, Mapplic, Insta Gallery,
WP Job Openings) etiketleri sayfalarda duruyordu; dosyalar silindiği için
404 üretiyorlardı. Ayrıca sitede hiçbir işe yaramayan WordPress uçları
(feed, xmlrpc, wp-json, oEmbed, emoji, generator) da temizleniyor —
hem gereksiz istek hem de "bu bir WordPress klonu" izi.
"""
import re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HARIC = ('_yedek-ayna', '_orijinal', '_uyarla', 'panel', 'api', 'pa-assets', '.git', '_dil', 'en', 'ka', 'ar')

# cookie-notice eklentisi yalnızca "Tamam" düğmesi sunuyordu; KVKK/GDPR
# için reddetme seçeneği şart olduğundan yerine kendi rıza bandımız geçti
# (pa-avm.js → cerezBandi).
OLU_EKLENTILER = ("woocommerce", "gravityforms", "mapplic", "insta-gallery",
                  "wp-job-openings", "cookie-notice")

DESENLER = [
    # kaldırılan eklentilerin stil/betik etiketleri
    (re.compile(r'\s*<link[^>]*plugins/(?:%s)/[^>]*>' % "|".join(OLU_EKLENTILER), re.I), ""),
    (re.compile(r'\s*<script[^>]*plugins/(?:%s)/[^>]*>\s*</script>' % "|".join(OLU_EKLENTILER), re.I), ""),
    (re.compile(r'(?s)\s*<style[^>]*id=[\'"](?:woocommerce|gform)[^\'"]*[\'"][^>]*>.*?</style>', re.I), ""),
    (re.compile(r'(?s)\s*<script[^>]*id=[\'"](?:woocommerce|gform|awsm)[^\'"]*[\'"][^>]*>.*?</script>', re.I), ""),

    # WordPress uçları — statik klonda hiçbiri çalışmıyor
    (re.compile(r'\s*<link[^>]*rel=[\'"]alternate[\'"][^>]*(?:/feed/|comments/feed|oembed)[^>]*>', re.I), ""),
    (re.compile(r'\s*<script[^>]*googletagmanager[^>]*>\s*</script>', re.I), ""),
    (re.compile(r'\s*<link[^>]*(?:xmlrpc\.php|api\.w\.org|wp-json)[^>]*>', re.I), ""),
    (re.compile(r'\s*<link[^>]*rel=[\'"](?:shortlink|wlwmanifest|pingback)[\'"][^>]*>', re.I), ""),
    (re.compile(r'\s*<meta[^>]*name=[\'"]generator[\'"][^>]*>', re.I), ""),
    (re.compile(r'(?s)\s*<script[^>]*wp-emoji[^>]*>.*?</script>', re.I), ""),
    (re.compile(r'(?s)\s*<script[^>]*id=[\'"]wp-emoji[^\'"]*[\'"][^>]*>.*?</script>', re.I), ""),
    (re.compile(r'(?s)\s*<script[^>]*>\s*window\._wpemojiSettings.*?</script>', re.I), ""),
    (re.compile(r'(?s)\s*<style[^>]*id=[\'"]wp-emoji[^\'"]*[\'"][^>]*>.*?</style>', re.I), ""),

    # üçüncü taraf bağlantı ipuçları
    (re.compile(r'\s*<link[^>]*(?:preconnect|dns-prefetch)[^>]*google[^>]*>', re.I), ""),
    # WooCommerce'ten kalan gövde sınıfı ve noscript stili
    (re.compile(r'(?s)\s*<noscript><style>\.woocommerce[^<]*</style></noscript>', re.I), ""),
    (re.compile(r'class="([^"]*)"'),
     lambda m: 'class="%s"' % re.sub(
         r'\s*\b(?:woocommerce-no-js|woocommerce-js|cookies-not-set|'
         r'wp-theme-dubaioutletmall|theme-dubaioutletmall)\b', '', m.group(1)).strip()),
    # eski/bozuk canonical — doğrusu SEO adımında yazılıyor
    (re.compile(r'\s*<link[^>]*rel=["\']canonical["\'][^>]*>', re.I), ""),
    # kaynak haritası yorumlarındaki eski alan adı
    (re.compile(r'/\*# sourceURL=https?://[^*]*dubaioutletmall[^*]*\*/', re.I), ""),
    # eski çerez bildirimi işaretlemesi
    (re.compile(r'(?s)\s*<!-- Cookie Notice plugin.*?<!-- / Cookie Notice plugin -->'), ""),
    (re.compile(r'(?s)\s*<div id="cookie-notice".*?</div>\s*</div>'), ""),
    # kaldırılan izleme kodundan geriye kalan yorumlar
    (re.compile(r'\s*<!--\s*Google tag[^>]*-->', re.I), ""),
    (re.compile(r'\s*<!--\s*End Google tag[^>]*-->', re.I), ""),
    (re.compile(r'\s*<!--[^>]*Site Kit[^>]*-->', re.I), ""),
    # boşalan yorum satırları
    # Google Tag Manager noscript iframe'i
    (re.compile(r'(?s)\s*<noscript>\s*<iframe[^>]*googletagmanager[^>]*>.*?</noscript>', re.I), ""),
    # temadan kalan eleman kimlikleri
    (re.compile(r'id=([\'"])dubaioutletmall-([^\'"]*)\1'), r'id=\1park-ardesen-\2\1'),
    # Dubai kiralama portalına giden canlı bağlantı
    (re.compile(r'https://leasing\.dubaioutletmall\.com/?'), "mailto:muhasebe@parkardesen.com"),
    # üçüncü taraf bağlantı ipuçları
    (re.compile(r'\s*<link[^>]*(?:preconnect|dns-prefetch)[^>]*google[^>]*>', re.I), ""),
    # WooCommerce'ten kalan gövde sınıfı ve noscript stili
    (re.compile(r'(?s)\s*<noscript><style>\.woocommerce[^<]*</style></noscript>', re.I), ""),
    (re.compile(r'class="([^"]*)"'),
     lambda m: 'class="%s"' % re.sub(
         r'\s*\b(?:woocommerce-no-js|woocommerce-js|cookies-not-set|'
         r'wp-theme-dubaioutletmall|theme-dubaioutletmall)\b', '', m.group(1)).strip()),
    # eski/bozuk canonical — doğrusu SEO adımında yazılıyor
    (re.compile(r'\s*<link[^>]*rel=["\']canonical["\'][^>]*>', re.I), ""),
    # kaynak haritası yorumlarındaki eski alan adı
    (re.compile(r'/\*# sourceURL=https?://[^*]*dubaioutletmall[^*]*\*/', re.I), ""),
    # eski çerez bildirimi işaretlemesi
    (re.compile(r'(?s)\s*<!-- Cookie Notice plugin.*?<!-- / Cookie Notice plugin -->'), ""),
    (re.compile(r'(?s)\s*<div id="cookie-notice".*?</div>\s*</div>'), ""),
    # kaldırılan izleme kodundan geriye kalan yorumlar
    (re.compile(r'\s*<!--\s*Google tag[^>]*-->', re.I), ""),
    (re.compile(r'\s*<!--\s*End Google tag[^>]*-->', re.I), ""),
    (re.compile(r'\s*<!--[^>]*Site Kit[^>]*-->', re.I), ""),
    # boşalan yorum satırları
    (re.compile(r'\n{3,}'), "\n\n"),
]


EMOJI_ANAHTAR = ("wp-emoji-settings", "_wpemojiSettings", "wpEmojiSettingsSupports")

# Klonda kalan izleme/üçüncü taraf kodları. Bunlar hem "orijinal site
# kırıntısı" hem de ciddi bir gizlilik sorunu: ziyaretçi verisi, siteyle
# ilgisi olmayan bir Google Tag Manager kapsayıcısına gidiyordu.
# WordPress'in "cookies-not-set" gövde sınıfını silen betiği; çerez
# eklentisiyle birlikte anlamını yitirdi
OLU_BETIK_ANAHTAR = ("document.body.className",)

IZLEME_ANAHTAR = ("googletagmanager", "google-analytics", "dataLayer",
                  "gtag(", "GTM-", "cnArgs", "wc_add_to_cart_params",
                  "woocommerce_params", "wc_order_attribution",
                  "mapplic", "dubaioutletmall.com")


def betik_bloklarini_sil(s, anahtarlar):
    """İçinde verilen anahtarlardan biri geçen <script> bloklarını kaldırır."""
    out, i = [], 0
    while True:
        b = s.find("<script", i)
        if b < 0:
            out.append(s[i:]); break
        e = s.find("</script>", b)
        if e < 0:
            out.append(s[i:]); break
        e += len("</script>")
        out.append(s[i:b] if any(a in s[b:e] for a in anahtarlar) else s[i:e])
        i = e
    return "".join(out)


def emoji_betigini_sil(s):
    """Emoji yükleyici, ayrı bir <script id="wp-emoji-settings"> JSON bloğunu
    okuyor. O blok silindiğinde yükleyici hata veriyor; ikisini birlikte
    kaldırmak gerekiyor."""
    out, i = [], 0
    while True:
        b = s.find("<script", i)
        if b < 0:
            out.append(s[i:]); break
        e = s.find("</script>", b)
        if e < 0:
            out.append(s[i:]); break
        e += len("</script>")
        blok = s[b:e]
        if any(a in blok for a in EMOJI_ANAHTAR):
            out.append(s[i:b])          # bloğu atla
        else:
            out.append(s[i:e])
        i = e
    return "".join(out)


def dosyalar():
    out = []
    for kok, dz, ds in os.walk(ROOT):
        dz[:] = [d for d in dz if d not in HARIC]
        out += [os.path.join(kok, d) for d in ds if d.endswith(".html")]
    return sorted(out)


def main():
    n = toplam = 0
    for f in dosyalar():
        s0 = open(f, encoding="utf-8", errors="replace").read()
        s = emoji_betigini_sil(s0)
        s = betik_bloklarini_sil(s, IZLEME_ANAHTAR + OLU_BETIK_ANAHTAR)
        if s != s0:
            toplam += 1
        for desen, yerine in DESENLER:
            s, k = desen.subn(yerine, s)
            toplam += k
        if s != s0:
            open(f, "w", encoding="utf-8").write(s)
            n += 1
    print("  %d sayfadan %d WordPress/eklenti artığı temizlendi" % (n, toplam))


if __name__ == "__main__":
    main()
