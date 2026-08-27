#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arama motoru ve paylaşım etiketleri.

Yerel SEO odaklı: Park Ardeşen AVM Rize'nin Ardeşen ilçesinde bir alışveriş
merkezi. Başlık ve açıklamalarda "Ardeşen", "Rize" geçiyor; yapısal veride
(schema.org ShoppingCenter) adres, koordinat, telefon ve çalışma saatleri
yer alıyor.

SITE_URL değiştiğinde (kendi alan adına geçildiğinde) yalnızca aşağıdaki
sabiti güncellemek yeterli.
"""
import re, os, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://park-ardesen-avm.vercel.app"      # kendi alan adına geçince değiştirin
HARIC = ('_yedek-ayna', '_orijinal', '_uyarla', 'panel', 'api', 'pa-assets', '.git')

AD = "Park Ardeşen AVM"
TAM_AD = "Park Ardeşen Alışveriş ve Yaşam Merkezi"
TEL = "+904647153030"
TEL_YAZI = "0464 715 30 30"
EPOSTA = "muhasebe@parkardesen.com"
ADRES = "Cumhuriyet Mah. Sultan Alparslan Cad. No: 2/1"
ILCE, IL, PK = "Ardeşen", "Rize", "53400"
ENLEM, BOYLAM = 41.190868, 40.987404      # Cumhuriyet Mah., Ardeşen (yaklaşık)
GORSEL = "/wp-content/uploads/pa/gorseller/avm-dis-cephe.jpg"
INSTAGRAM = "https://www.instagram.com/parkardesenavm/"
FACEBOOK = "https://www.facebook.com/parkardesen"

# sayfa yolu -> (başlık, açıklama)
SAYFALAR = {
    "": ("Park Ardeşen AVM — Ardeşen'in Alışveriş ve Yaşam Merkezi | Rize",
         "Rize Ardeşen'de LC Waikiki, Migros, FLO, Madame Coco ve daha fazlası. "
         "Yeme-içme katı, çocuk oyun alanı ve bowling salonuyla ailenizle keyifli "
         "bir gün. Her gün 10:00–22:00, ücretsiz otopark."),

    "shops": ("Mağazalar — Park Ardeşen AVM | Ardeşen, Rize",
              "Park Ardeşen AVM'deki tüm mağazalar: moda, ayakkabı, market, "
              "kozmetik, yeme-içme ve eğlence. Kat ve mağaza numaralarıyla "
              "güncel mağaza rehberi."),

    "mall-map": ("Kat Planı — Park Ardeşen AVM | Ardeşen, Rize",
                 "Park Ardeşen AVM kat planı. Zemin, 1. ve 2. kattaki mağazaları "
                 "numaralarıyla görün, ziyaretinizi önceden planlayın."),

    "deals": ("Kampanyalar ve İndirimler — Park Ardeşen AVM | Ardeşen",
              "Park Ardeşen AVM mağazalarındaki güncel kampanyalar, indirimler ve "
              "fırsatlar. LC Waikiki, FLO, Migros, Madame Coco ve diğer markalar."),

    "bargain-monday": ("Fırsat Günleri — Park Ardeşen AVM | Ardeşen, Rize",
                       "Her ayın ilk haftası Park Ardeşen AVM'de Fırsat Günleri: "
                       "indirimli ürünlerin üzerine ekstra indirim."),

    "duyurular": ("Duyurular — Park Ardeşen AVM | Ardeşen, Rize",
                  "Çalışma saati değişiklikleri, yeni mağaza açılışları, etkinlik ve "
                  "çekiliş duyuruları. Park Ardeşen AVM'den güncel haberler."),

    "about-dom": ("Hakkımızda — Park Ardeşen AVM | Ardeşen, Rize",
                  "Park Ardeşen Alışveriş ve Yaşam Merkezi, Rize'nin Ardeşen "
                  "ilçesinde üç kata yayılan mağazaları, yeme-içme katı ve eğlence "
                  "alanlarıyla ilçenin buluşma noktası."),

    "services": ("Hizmetlerimiz — Park Ardeşen AVM | Ardeşen, Rize",
                 "Ücretsiz otopark, mescit, anne-bebek odası, engelli erişimi, ATM, "
                 "ilk yardım ve daha fazlası. Park Ardeşen AVM'deki tüm olanaklar."),

    "contact-us": ("İletişim — Park Ardeşen AVM | Ardeşen, Rize",
                   "Park Ardeşen AVM adres, telefon ve çalışma saatleri. "
                   "Cumhuriyet Mah. Sultan Alparslan Cad. No: 2/1, Ardeşen / Rize. "
                   "Tel: " + TEL_YAZI + "."),

    "faq": ("Sıkça Sorulan Sorular — Park Ardeşen AVM | Ardeşen, Rize",
            "Park Ardeşen AVM nerede, çalışma saatleri, otopark, mağazalar, "
            "çocuk oyun alanı ve Wi-Fi hakkında merak edilenler."),

    "leasing": ("Mağaza Kiralama — Park Ardeşen AVM | Ardeşen, Rize",
                "Ardeşen'in en işlek caddesinde mağaza, kiosk ve reklam alanı "
                "kiralama fırsatları. Güncel boş birimler ve iletişim bilgileri."),

    "careers": ("Kariyer — Park Ardeşen AVM | Ardeşen, Rize",
                "Park Ardeşen AVM'de açık pozisyonlar ve iş başvurusu. "
                "Özgeçmişinizi bize iletin."),

    "tourism": ("Ulaşım — Park Ardeşen AVM | Ardeşen, Rize",
                "Park Ardeşen AVM'ye nasıl gidilir? Karadeniz Sahil Yolu, dolmuş ve "
                "otobüs hatları, ücretsiz otopark ve çevre ilçelere uzaklıklar."),


    "outlet-plus-card": ("Park Kart — Park Ardeşen AVM | Ardeşen, Rize",
                         "Park Kart ile katılımcı mağazalarda ekstra indirim. "
                         "Ücretsiz kartınızı zemin kattaki danışma bankosundan alın."),




    "gizlilik-politikasi": ("Gizlilik Politikası ve KVKK Aydınlatma Metni — " + AD,
                            "Park Ardeşen AVM internet sitesinde kişisel verilerin "
                            "işlenmesi, çerez kullanımı ve KVKK kapsamındaki "
                            "haklarınız."),

    "cerez-politikasi": ("Çerez Politikası — " + AD,
                         "Park Ardeşen AVM internet sitesinde kullanılan çerezler, "
                         "kategorileri ve çerez tercihlerinizi nasıl "
                         "yönetebileceğiniz."),

    "kullanim-kosullari": ("Kullanım Koşulları — " + AD,
                           "Park Ardeşen AVM internet sitesinin kullanım koşulları, "
                           "içerik doğruluğu ve fikri mülkiyet bilgileri."),
}

MENU_ADI = {
    "shops": "Mağazalar", "mall-map": "Kat Planı", "deals": "Kampanyalar",
    "bargain-monday": "Fırsat Günleri", "duyurular": "Duyurular",
    "about-dom": "Hakkımızda", "services": "Hizmetlerimiz",
    "contact-us": "İletişim", "faq": "Sıkça Sorulan Sorular",
    "leasing": "Mağaza Kiralama", "careers": "Kariyer", "tourism": "Ulaşım",
     "outlet-plus-card": "Park Kart",
     
     "gizlilik-politikasi": "Gizlilik Politikası",
    "kullanim-kosullari": "Kullanım Koşulları",
    "cerez-politikasi": "Çerez Politikası",
}


def isletme_verisi():
    """schema.org/ShoppingCenter — Google'ın işletmeyi tanıması için."""
    return {
        "@context": "https://schema.org",
        "@type": "ShoppingCenter",
        "@id": SITE_URL + "/#avm",
        "name": TAM_AD,
        "alternateName": AD,
        "url": SITE_URL + "/",
        "image": SITE_URL + GORSEL,
        "logo": SITE_URL + "/wp-content/uploads/pa/logo/parkardesen-logo-dark.svg",
        "telephone": TEL,
        "email": EPOSTA,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": ADRES,
            "addressLocality": ILCE,
            "addressRegion": IL,
            "postalCode": PK,
            "addressCountry": "TR",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": ENLEM, "longitude": BOYLAM},
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday",
                          "Friday", "Saturday", "Sunday"],
            "opens": "10:00", "closes": "22:00",
        }],
        "sameAs": [INSTAGRAM, FACEBOOK],
        "areaServed": [
            {"@type": "AdministrativeArea", "name": "Ardeşen"},
            {"@type": "AdministrativeArea", "name": "Rize"},
            {"@type": "AdministrativeArea", "name": "Fındıklı"},
            {"@type": "AdministrativeArea", "name": "Pazar"},
            {"@type": "AdministrativeArea", "name": "Çamlıhemşin"},
        ],
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": a, "value": True}
            for a in ("Ücretsiz otopark", "Mescit", "Anne ve bebek odası",
                      "Engelli erişimi", "Ücretsiz Wi-Fi", "ATM",
                      "Çocuk oyun alanı", "İlk yardım odası")
        ],
    }


def kirinti_verisi(yol, ad):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Anasayfa",
             "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": ad,
             "item": SITE_URL + "/" + yol + "/"},
        ],
    }


def sss_verisi():
    """SSS sayfasındaki soruları yapısal veriye çevirir (zengin sonuç)."""
    f = os.path.join(ROOT, "faq", "index.html")
    if not os.path.isfile(f):
        return None
    s = open(f, encoding="utf-8").read()
    ogeler = []
    for m in re.finditer(r'(?s)<div class="faq-item">.*?<h3>(.*?)</h3>.*?'
                         r'<div class="faq-content">(.*?)</div>', s):
        soru = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        cevap = html.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))
        cevap = re.sub(r"\s+", " ", cevap).strip()
        if soru and cevap:
            ogeler.append({"@type": "Question", "name": soru,
                           "acceptedAnswer": {"@type": "Answer", "text": cevap}})
    if not ogeler:
        return None
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": ogeler}


def jsonld(veri):
    return ('<script type="application/ld+json">%s</script>'
            % json.dumps(veri, ensure_ascii=False, separators=(",", ":")))


def bas_etiketleri(yol, baslik, aciklama):
    tam = SITE_URL + ("/" if not yol else "/" + yol + "/")
    e = html.escape
    p = ['<meta name="description" content="%s">' % e(aciklama),
         '<link rel="canonical" href="%s">' % tam,
         '<meta name="robots" content="index, follow, max-image-preview:large">',
         '<meta name="theme-color" content="#e11f26">',
         '<meta name="author" content="%s">' % e(TAM_AD),
         '<meta name="geo.region" content="TR-53">',
         '<meta name="geo.placename" content="%s, %s">' % (ILCE, IL),
         '<meta name="geo.position" content="%s;%s">' % (ENLEM, BOYLAM),
         '<meta name="ICBM" content="%s, %s">' % (ENLEM, BOYLAM),
         '<meta property="og:type" content="website">',
         '<meta property="og:site_name" content="%s">' % e(AD),
         '<meta property="og:locale" content="tr_TR">',
         '<meta property="og:title" content="%s">' % e(baslik),
         '<meta property="og:description" content="%s">' % e(aciklama),
         '<meta property="og:url" content="%s">' % tam,
         '<meta property="og:image" content="%s">' % (SITE_URL + GORSEL),
         '<meta property="og:image:alt" content="%s dış cephe">' % e(AD),
         '<meta name="twitter:card" content="summary_large_image">',
         '<meta name="twitter:title" content="%s">' % e(baslik),
         '<meta name="twitter:description" content="%s">' % e(aciklama),
         '<meta name="twitter:image" content="%s">' % (SITE_URL + GORSEL)]
    return "\n".join(p)


ESKI_META = re.compile(
    r'\s*<(?:meta|link)[^>]*(?:name|property|rel)=["\']'
    r'(?:description|robots|theme-color|author|geo\.\w+|ICBM|canonical|'
    r'og:[\w:]+|twitter:\w+)["\'][^>]*>', re.I)
ESKI_JSONLD = re.compile(r'(?s)\s*<script type="application/ld\+json">.*?</script>')


def sayfa_yaz(yol, baslik, aciklama, ek_veri):
    f = os.path.join(ROOT, yol, "index.html") if yol else os.path.join(ROOT, "index.html")
    if not os.path.isfile(f):
        return False
    s = open(f, encoding="utf-8").read()
    s = ESKI_META.sub("", s)
    s = ESKI_JSONLD.sub("", s)
    # başlıkta kesme işaretini kaçırmaya gerek yok (yalnızca & < > yeterli)
    s = re.sub(r"<title>.*?</title>",
               lambda m: "<title>%s</title>" % html.escape(baslik, quote=False),
               s, count=1, flags=re.S)
    blok = "\n" + bas_etiketleri(yol, baslik, aciklama) + "\n"
    for v in ek_veri:
        blok += jsonld(v) + "\n"
    s = s.replace("</head>", blok + "</head>", 1)
    open(f, "w", encoding="utf-8").write(s)
    return True


def site_haritasi(yollar):
    from datetime import date
    bugun = date.today().isoformat()
    satir = []
    for yol in yollar:
        tam = SITE_URL + ("/" if not yol else "/" + yol + "/")
        oncelik = "1.0" if not yol else ("0.9" if yol in
                  ("shops", "deals", "duyurular", "mall-map") else "0.7")
        sik = "daily" if yol in ("", "deals", "duyurular") else "weekly"
        satir.append("  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
                     "    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n"
                     "  </url>" % (tam, bugun, sik, oncelik))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(satir) + "\n</urlset>\n")


def main():
    yollar = [y for y in SAYFALAR
              if os.path.isfile(os.path.join(ROOT, y, "index.html") if y
                                else os.path.join(ROOT, "index.html"))]
    sss = sss_verisi()
    n = 0
    for yol in yollar:
        baslik, aciklama = SAYFALAR[yol]
        ek = [isletme_verisi()] if not yol else [kirinti_verisi(yol, MENU_ADI.get(yol, yol))]
        if yol == "faq" and sss:
            ek.append(sss)
        if sayfa_yaz(yol, baslik, aciklama, ek):
            n += 1

    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        site_haritasi(yollar))
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /panel/\n"
        "Disallow: /api/\n"
        "Disallow: /_orijinal/\n"
        "\n"
        "Sitemap: %s/sitemap.xml\n" % SITE_URL)

    print("  %d sayfaya SEO etiketleri yazıldı · sitemap.xml (%d adres) · robots.txt"
          % (n, len(yollar)))


if __name__ == "__main__":
    main()
