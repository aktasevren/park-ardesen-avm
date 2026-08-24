#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Anasayfa içeriğini Park Ardeşen AVM'ye uyarlar."""
import re, os, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOSTS = ["www.dubaioutletmall.com", "dubaioutletmall.com"]
VERI = json.load(open(os.path.join(ROOT, "pa-assets", "magazalar.json"), encoding="utf-8"))
MAG = {m["slug"]: m for m in VERI["magazalar"]}

PA = "wp-content/uploads/pa/"

# ---- vitrin mağazaları (anasayfadaki 5 büyük kart) ----------------------
VITRIN = ["lc-waikiki", "migros", "flo", "burger-king", "grand-bowling"]

# ---- kategori kartları: temanın 8 ikonundan 7'sini kullanıyoruz ---------
KATEGORI_SIRA = [
    ("fashion",            "moda",      "Moda &amp; Giyim"),
    ("shoes-footwear",     "ayakkabi",  "Ayakkabı &amp; Çanta"),
    ("food",               "yeme-icme", "Yeme &amp; İçme"),
    ("accessories-jewelry","kozmetik",  "Kozmetik &amp; Parfüm"),
    ("entertainment-toys", "eglence",   "Eğlence &amp; Çocuk"),
    ("homeware",           "ev-yasam",  "Ev &amp; Yaşam"),
    ("electronics",        "market",    "Market"),
]

# ---- kampanya kartları --------------------------------------------------
KAMPANYA = [
    ("lc-waikiki",    "Sezon sonunda %50'ye varan indirim"),
    ("flo",           "İkinci çiftte %40 indirim"),
    ("migros",        "Money'e özel haftanın fırsatları"),
    ("madame-coco",   "Ev tekstilinde %40 indirim"),
    ("bargello",      "3 al 2 öde"),
    ("burger-king",   "Menüde ikinci ürün hediye"),
    ("popeyes",       "Çıtır menülerde %25 indirim"),
    ("berru-park",    "Hafta içi oyun kartında %30 indirim"),
]


def logo_yolu(slug, onek):
    m = MAG.get(slug) or {}
    if m.get("logo"):
        return onek + PA + "markalar/" + m["logo"]
    return None


def img(src, alt, sinif=""):
    return ('<img src="%s" alt="%s" class="%s" loading="lazy" decoding="async">'
            % (src, alt, sinif))


def vitrin_html(onek):
    parcalar = []
    for i, slug in enumerate(VITRIN):
        m = MAG[slug]
        kol = "col-12 col-md-4" if i < 3 else "col-12 col-md-6"
        lg = logo_yolu(slug, onek)
        gorsel = (img(lg, m["ad"], "pa-marka-logo") if lg
                  else '<div class="pa-marka-yazi">%s</div>' % m["ad"])
        parcalar.append(
            '<div class="col %s">\n'
            '  <a href="%sshops/index.html">\n'
            '    <div class="featured-shops-img pa-logo-kutu">%s</div>\n'
            '    <h2>%s</h2>\n'
            '  </a>\n'
            '</div><!-- .col -->' % (kol, onek, gorsel, m["ad"]))
    return "\n".join(parcalar)


def kampanya_html(onek):
    parcalar = []
    for slug, baslik in KAMPANYA:
        m = MAG[slug]
        lg = logo_yolu(slug, onek)
        gorsel = (img(lg, m["ad"], "pa-marka-logo") if lg
                  else '<div class="pa-marka-yazi">%s</div>' % m["ad"])
        parcalar.append(
            '<div class="col-12 col-md-3">\n'
            '  <a class="card" href="%sdeals/index.html">\n'
            '    <div class="card-inner pa-logo-kutu">\n'
            '      %s\n'
            '      <h3>%s</h3>\n'
            '    </div>\n'
            '  </a>\n'
            '</div><!-- .col-12 -->' % (onek, gorsel, baslik))
    return "\n".join(parcalar)


def galeri_html(onek):
    gorseller = [
        ("gorseller/avm-dis-cephe.jpg", "Park Ardeşen AVM dış cephe"),
        ("gorseller/ic-mekan-1.webp", "Park Ardeşen AVM iç mekân"),
        ("gorseller/ic-mekan-2.webp", "Park Ardeşen AVM iç mekân"),
        ("markalar/" + MAG["lc-waikiki"]["logo"], "LC Waikiki"),
        ("markalar/" + MAG["migros"]["logo"], "Migros"),
        ("markalar/" + MAG["burger-king"]["logo"], "Burger King"),
    ]
    kartlar = "\n".join(
        '<div class="pa-galeri-kart">%s</div>' % img(onek + PA + p, a)
        for p, a in gorseller)
    return ('<!--PA-GALERI--><div class="pa-galeri">\n%s\n</div><!--/PA-GALERI-->'
            % kartlar)



def slider_html(onek):
    """Anasayfadaki 'Ailenizle keyifli bir gün' kayan şeridi.
    Orijinalde Dubai'de çekilmiş 12 fotoğraf vardı ve hepsi tembel
    yükleniyordu; slick karuseli görünür alanın dışına taşıdığı için
    lazysizes hiç tetiklenmiyor, şerit bomboş kalıyordu. Kendi
    fotoğraflarımızı doğrudan (tembel yükleme olmadan) koyuyoruz."""
    gorseller = [
        ("gorseller/avm-dis-cephe.jpg", "Park Ardeşen AVM dış cephe"),
        ("gorseller/ic-mekan-1.webp", "Park Ardeşen AVM iç mekân"),
        ("gorseller/ic-mekan-2.webp", "Park Ardeşen AVM iç mekân"),
    ]
    # şerit dolu görünsün diye iki tur
    return "\n".join(
        '<div class="home-slider-img-wrap">'
        '<img src="%s%s%s" alt="%s" decoding="async"></div>'
        % (onek, PA, p, a)
        for p, a in gorseller * 2)

def uyarla(s, onek):
    # ---- 1. hero ---------------------------------------------------------
    s = re.sub(
        r'(?is)<video playsinline.*?</video>',
        '<div class="home-banner-video pa-hero" style="background-image:url(%s)"></div>'
        % (onek + PA + "gorseller/avm-dis-cephe.jpg"),
        s, count=1)
    s = s.replace(
        "<h1>Premium brands<span>&nbsp;at amazing bargains</span></h1>",
        "<h1>Ardeşen'in kalbinde<span>&nbsp;alışverişin yeni adresi</span></h1>")

    # ---- 2. ilk tanıtım bloğu -------------------------------------------
    s = s.replace("<h2>Luxury <br/>Made<span>affordable</span></h2>",
                  "<h2>Alışveriş <br/>ve keyif<span>bir arada</span></h2>")
    s = s.replace(
        "<p>Over 300 brands offer a minimum of 40% off across their collections.</p>",
        "<p>Moda, market, yeme-içme ve eğlence; sevdiğiniz markalar tek çatı altında.</p>")
    s = re.sub(r'<a href="[^"]*" class="btn">Explore the brands</a>',
               '<a href="%sshops/index.html" class="btn">Markaları keşfet</a>' % onek, s)

    # ---- 3. vitrin mağazaları -------------------------------------------
    s = re.sub(r'(?s)(<div class="featured-shops">\s*<div class="container">\s*<div class="row">).*?'
               r'(</div><!-- \.row -->)',
               lambda m: m.group(1) + "\n" + vitrin_html(onek) + "\n" + m.group(2),
               s, count=1)

    # ---- 4. "içeride neler var" -----------------------------------------
    s = s.replace("<h2>What’s <br>inside</h2>", "<h2>İçeride <br>neler var</h2>")
    s = re.sub(r"<p>There are over 200 shops at [^<]*</p>",
               "<p>Park Ardeşen AVM'de %d mağaza, kafe ve eğlence noktası sizi bekliyor.</p>"
               % len(VERI["magazalar"]), s)
    s = re.sub(r'<a href="[^"]*" class="btn">Explore the Shops</a>',
               '<a href="%sshops/index.html" class="btn">Mağazaları gör</a>' % onek, s)

    # ---- 5. kategori kartları -------------------------------------------
    for en_slug, tr_slug, tr_ad in KATEGORI_SIRA:
        s = re.sub(r'href="[^"]*shop-category=%s"' % en_slug,
                   'href="%sshops/index.html#%s"' % (onek, tr_slug), s)
    for en, tr in (("Fashion", "Moda &amp; Giyim"),
                   ("Shoes &amp; Footwear", "Ayakkabı &amp; Çanta"),
                   ("Food", "Yeme &amp; İçme"),
                   ("Accessories &amp; Jewelry", "Kozmetik &amp; Parfüm"),
                   ("Entertainment &amp; Toys", "Eğlence &amp; Çocuk"),
                   ("Homeware", "Ev &amp; Yaşam"),
                   ("Electronics", "Market")):
        s = s.replace("<h3>%s</h3>" % en, "<h3>%s</h3>" % tr)
    # 8. kart (Sportswear) — karşılığı yok, kaldır
    s = re.sub(r'(?s)<div class="col-12 col-sm-6 col-md-3">\s*<a href="[^"]*sportswear-goods[^"]*"[^>]*>.*?</a>\s*</div><!-- \.col-12 -->',
               "", s, count=1)

    # ---- 6. aile bölümü --------------------------------------------------
    s = s.replace("<h2>Your family<br>destination for<span>style and savings</span></h2>",
                  "<h2>Ailenizle<br>keyifli bir<span>gün</span></h2>")
    s = re.sub(r'(?s)(<div class="home-slider">).*?(</div><!-- \.home-slider -->)',
               lambda m: m.group(1) + "\n" + slider_html(onek) + "\n" + m.group(2),
               s, count=1)

    # ---- 7. kampanyalar --------------------------------------------------
    s = s.replace("<h2>Dom<br>Exclusive <span>deals</span></h2>",
                  "<h2>Park Ardeşen<br>kampanya <span>fırsatları</span></h2>")
    s = re.sub(r"<p>Discover 100\+ exclusive offers and deals:[^<]*</p>",
               "<p>Mağazalarımızdaki güncel indirim ve fırsatların tamamı burada.</p>", s)
    s = re.sub(r'<a href="[^"]*" class="btn">View all deals</a>',
               '<a href="%sdeals/index.html" class="btn">Tüm kampanyalar</a>' % onek, s)
    s = re.sub(r'(?s)(<div class="home-deals">\s*<div class="container">\s*<div class="row">).*?'
               r'(</div><!-- \.row -->)',
               lambda m: m.group(1) + "\n" + kampanya_html(onek) + "\n" + m.group(2),
               s, count=1)

    # ---- 8. kat planı ----------------------------------------------------
    s = s.replace("<h2>Explore<br>the outlet <span>mall</span></h2>",
                  "<h2>Kat planını<br>keşfet<span></span></h2>")
    s = s.replace("<p>Effortlessly navigate your visit: Utilize our map to plan your trip to every store</p>",
                  "<p>Ziyaretinizi kolayca planlayın: kat planıyla aradığınız mağazaya doğrudan gidin.</p>")
    s = re.sub(r'<a href="[^"]*" class="btn">View interactive map</a>',
               '<a href="%small-map/index.html" class="btn">Kat planına bak</a>' % onek, s)

    # ---- 9. Shop Online bloğunu tamamen kaldır ---------------------------
    i = s.find('<div class="online-shop-wrap">')
    if i >= 0:
        j = s.find('<div class="insta-feed-wrap">', i)
        if j > i:
            s = s[:i] + s[j:]

    # ---- 10. Instagram ---------------------------------------------------
    s = s.replace("<h2>DOM @<br>Instagram</h2>",
                  "<h2>Park Ardeşen @<br>Instagram</h2>")
    s = re.sub(r'<a href="https://www\.instagram\.com/dubaioutletmall/" class="btn">Follow us</a>',
               '<a href="https://www.instagram.com/parkardesenavm/" class="btn" target="_blank" rel="noopener">Takip et</a>', s)
    yeni_galeri = galeri_html(onek)
    if "<!--PA-GALERI-->" in s:
        s = re.sub(r'(?s)<!--PA-GALERI-->.*?<!--/PA-GALERI-->', yeni_galeri, s, count=1)
    elif 'instagram-gallery-feed-0' in s:
        s = re.sub(r'(?s)<div id="instagram-gallery-feed-0".*?</div>',
                   yeni_galeri, s, count=1)
    else:
        # feed bloğu daha önce kaldırılmışsa galeriyi .insta-feed içine ekle
        i = s.find('<div class="insta-feed">')
        if i >= 0:
            j = s.find('</div><!-- .fsc-wrap -->', i)
            j = j if j > 0 else s.find('</main>', i)
            k = s.rfind('</div>', i, j)          # .insta-feed kapanışı
            k = s.rfind('</div>', i, k)          # .container kapanışı
            if k > i:
                s = s[:k] + yeni_galeri + "\n" + s[k:]
    return s


def main():
    n = 0
    hedefler = [(h, "index.html", "") for h in HOSTS]
    # wget, /images/ ve /videos/ adreslerinde de anasayfayı indirmiş
    hedefler += [("dubaioutletmall.com", os.path.join(a, "index.html"), "../")
                 for a in ("images", "videos")]
    hedefler += [("dubaioutletmall.com", "shops.html", "")]
    for h, rel, onek in hedefler:
        f = os.path.join(ROOT, h, rel)
        if not os.path.isfile(f):
            continue
        s0 = open(f, encoding="utf-8").read()
        s = uyarla(s0, onek)
        if s != s0:
            open(f, "w", encoding="utf-8").write(s)
            n += 1
    print("  anasayfa: %d dosya güncellendi" % n)


if __name__ == "__main__":
    main()
