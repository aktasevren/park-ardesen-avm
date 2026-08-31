#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""İç sayfaların içeriğini Park Ardeşen AVM'ye uyarlar."""
import re, os, json, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VERI = json.load(open(os.path.join(ROOT, "pa-assets", "magazalar.json"), encoding="utf-8"))
MAG = {m["slug"]: m for m in VERI["magazalar"]}
YEDEK = os.path.join(ROOT, "_orijinal")
PA = "wp-content/uploads/pa/"

TEL = "0464 715 30 30"
EPOSTA = "muhasebe@parkardesen.com"
ADRES = "Cumhuriyet Mah. Sultan Alparslan Cad. No: 2/1, 53400 Ardeşen / Rize"

def yedekle(f, ad):
    os.makedirs(YEDEK, exist_ok=True)
    h = os.path.join(YEDEK, ad)
    if not os.path.exists(h):
        shutil.copy2(f, h)

def oku(f): return open(f, encoding="utf-8").read()
def yaz(f, s): open(f, "w", encoding="utf-8").write(s)

# =====================================================================
# ORTAK BLOKLAR — birden çok sayfada tekrar eden bölümler
# =====================================================================

BANNER_H1 = {
    "About Us": "Hakkımızda", "Services": "Hizmetlerimiz", "Contact Us": "İletişim",
    "FAQ&#8217;s": "Sıkça Sorulan Sorular", "Leasing": "Mağaza Kiralama",
    "Careers": "Kariyer", "Mall Brochures": "Broşürler",
    "Bus Schedule": "Çalışma Saatleri ve Servis", "Tourism": "Ulaşım",
    "Bargain Monday": "Fırsat Günleri", "Outlet Plus Card": "Park Kart",
    "Media Center": "Medya Merkezi", "Press": "Basında Biz", "Deals": "Kampanyalar",
    "Privacy Policy": "Gizlilik Politikası", "Terms and Conditions": "Kullanım Koşulları",
}

ISTATISTIK = [
    ("17", "Mağaza ve marka"),
    ("3", "Kat"),
    ("6", "Kafe ve restoran"),
    ("2", "Eğlence noktası"),
    ("7/7", "Haftanın her günü açık"),
]

# Ardeşen ölçeğinde gerçekçi olmayanlar (vale, oto yıkama, döviz bürosu,
# fotoğraf stüdyosu, internet kafe, emanet dolabı) listeden çıkarıldı.
OLANAK_TR = {
    "Gift Vouchers": "Hediye Çeki",
    "Outlet Plus Card": "Park Kart",
    "Mother &amp; Baby Room": "Anne &amp; Bebek Odası",
    "Wheelchair": "Tekerlekli Sandalye",
    "Baby Changing Room": "Bebek Bakım Odası",
    "Customer Services": "Danışma / Müşteri Hizmetleri",
    "Praying Rooms": "Mescit",
    "Baby Carts": "Bebek Arabası",
    "First Aid Room": "İlk Yardım Odası",
    "ATM Cash Machines": "ATM",
    "Lost &amp; Found Property": "Kayıp Eşya",
    "Lost Child Assistance": "Kayıp Çocuk Yardımı",
    "Mobile Charging Stations": "Telefon Şarj Noktası",
    "Mall Directory": "AVM Rehberi",
    "Dedicated Toilets": "Engelli Tuvaleti",
    "Parking Spots": "Ücretsiz Otopark",
}
OLANAK_SIL = ["Internet Cafes", "Valet Parking", "Photo Studio",
              "Luggage Storage Room", "Money Exchange", "Car Wash Service"]

HEDIYE_CEKI_TR = """<p>Ne alacağınıza karar veremediğiniz her durumda Park Ardeşen AVM hediye çeki
işinizi görür. Moda, ayakkabı, ev tekstili, kozmetik ya da yeme-içme &mdash; hediye çeki
merkezimizdeki katılımcı mağazaların tamamında geçerlidir.</p>
<p>Hediye çekleri 250 TL, 500 TL, 1.000 TL ve 2.500 TL değerlerinde hazırlanır ve
düzenlendiği tarihten itibaren bir yıl boyunca geçerlidir.</p>
<p>Hediye çeki almak için zemin kattaki danışma bankosuna uğrayabilir ya da
%s numaralı telefondan bilgi alabilirsiniz.</p>""" % TEL


def galeri_slider(onek):
    gorseller = [
        ("gorseller/avm-dis-cephe.jpg", "Park Ardeşen AVM dış cephe"),
        ("gorseller/ic-mekan-1.webp", "Park Ardeşen AVM iç mekân"),
        ("gorseller/ic-mekan-2.webp", "Park Ardeşen AVM iç mekân"),
    ]
    return "\n".join(
        '<div class="photo-gallery-slider-item">'
        '<img src="%s%s%s" alt="%s" loading="lazy" decoding="async"></div>'
        % (onek, PA, p, a) for p, a in gorseller)




BANNER_GORSEL = re.compile(
    r'(?:https?://)?(?:\.\./)*(?:www\.)?(?:dubaioutletmall\.com/)?'
    r'wp-content/uploads/\d{4}/\d{2}/[A-Za-z0-9._-]+\.(?:jpg|jpeg|png|webp)')


def banner_gorseli(s, onek):
    """Üst banner'daki Dubai fotoğrafını AVM fotoğrafıyla değiştirir.
    src / data-src / srcset / data-srcset ve <noscript> kopyası dahil."""
    i = s.find('<section class="common-banner">')
    if i < 0:
        return s
    j = s.find('</section>', i)
    blok = s[i:j]
    hedef = onek + PA + "gorseller/avm-dis-cephe.jpg"
    yeni = BANNER_GORSEL.sub(hedef, blok)
    yeni = re.sub(r'(srcset|data-srcset)="[^"]*"', r'\1="%s"' % hedef, yeni)
    return s[:i] + yeni + s[j:]

def olanaklari_ele(s):
    """Olanaklar bölümündeki kartları tek tek ayırıp, ilçe ölçeğinde gerçekçi
    olmayanları çıkarır. (Tek bir büyük regex kart bloklarını birbirine
    karıştırdığı için blok blok işliyoruz.)"""
    i = s.find('<section class="amenities">')
    if i < 0:
        return s
    j = s.find('</div><!-- .row -->', i)
    if j < 0:
        return s
    r0 = s.find('<div class="row">', i)
    govde = s[r0 + len('<div class="row">'):j]
    AYRAC = '<div class="col-12 col-sm-6 col-md-3">'
    parcalar = govde.split(AYRAC)
    bas, kartlar = parcalar[0], parcalar[1:]
    tutulan = []
    for k in kartlar:
        m = re.search(r"<h3>(.*?)</h3>", k)
        if m and m.group(1).strip() in OLANAK_SIL:
            # kartı at ama peşindeki modal/parçaları koru
            kalan = k[k.find("</div>", k.find("</h3>")):]
            kalan = kalan[kalan.find("</div>") + 6:]
            son = kalan[kalan.find("</div>") + 6:] if "</div>" in kalan else ""
            tutulan.append(son)
            continue
        tutulan.append(AYRAC + k)
    return s[:r0 + len('<div class="row">')] + bas + "".join(tutulan) + s[j:]

def ortak(s, onek):
    # --- üst banner başlığı + görseli ---------------------------------
    DUZELT_H1 = {"Ulaşım ve Servis": "Çalışma Saatleri ve Servis"}

    def bh(m):
        t = m.group(1).strip()
        t = DUZELT_H1.get(t, t)
        return "<h1>%s</h1>" % BANNER_H1.get(t, t)
    s = re.sub(r"<h1>([^<]*)</h1>", bh, s, count=1)
    s = banner_gorseli(s, onek)

    # --- istatistik şeridi ---------------------------------------------
    s = s.replace("<h2 class=\"h2\">DISCOVER WHY OUR MALL IS THE TOP CHOICE</h2>",
                  "<h2 class=\"h2\">NEDEN PARK ARDEŞEN AVM?</h2>")
    eski_ist = [("90%", "Fun, Happiness, Emotions"), ("98%", "Food and Drinks"),
                ("80%", "Shopping and Discounts"),
                ("100%", "Experience Unforgettable Entertainment"),
                ("92%", "Unforgettable Family Weekends")]
    for (h3, p), (y3, yp) in zip(eski_ist, ISTATISTIK):
        s = s.replace("<h3>%s</h3>\n                            <p>%s</p>" % (h3, p),
                      "<h3>%s</h3>\n                            <p>%s</p>" % (y3, yp))
        s = s.replace("<h3>%s</h3>" % h3, "<h3>%s</h3>" % y3)
        s = s.replace("<p>%s</p>" % p, "<p>%s</p>" % yp)

    # --- iki kolonlu kartlar -------------------------------------------
    s = re.sub(r"<h3 class=\"h2\">Leasing Opportunities at [^<]*</h3>",
               "<h3 class=\"h2\">Park Ardeşen AVM'de mağaza kiralama</h3>", s)
    s = re.sub(r"(?s)<p><p><span data-sheets-value=.*?</span></p>\s*</p>",
               "<p>Ardeşen'in en yoğun caddesinde, ilçenin ve çevre beldelerin "
               "buluşma noktasında yer alın. Boş mağaza, kiosk ve reklam alanları "
               "için kiralama ekibimizle görüşebilirsiniz.</p>", s)
    s = s.replace("<h3 class=\"h2\">Outlet Plus Card</h3>",
                  "<h3 class=\"h2\">Park Kart</h3>")
    s = re.sub(r"<p><p>Unlock exclusive savings with the Outlet Plus Card at [^<]*</p>\s*</p>",
               "<p>Park Kart ile katılımcı mağazalarda ekstra indirim ve ayrıcalıklardan "
               "yararlanın. Kartınızı zemin kattaki danışma bankosundan ücretsiz alabilirsiniz.</p>", s)
    s = s.replace(">View More</a>", ">Detaylı bilgi</a>")

    # --- fotoğraf galerisi ---------------------------------------------
    s = s.replace("<h2 class=\"h2\">Photo Gallery</h2>", "<h2 class=\"h2\">Fotoğraf Galerisi</h2>")
    # "Tümünü gör" düğmesi orijinalde Medya Merkezi'ne gidiyordu; o sayfa
    # kaldırıldı ve galerinin tamamı zaten bu şeritte görünüyor.
    s = re.sub(r'\s*<a href="[^"]*media-center/?"[^>]*class="btn"[^>]*>View more</a>', "", s)
    s = re.sub(r'(?s)(<div class="photo-gallery-slider">).*?(</div><!-- \.row -->)',
               lambda m: m.group(1) + "\n" + galeri_slider(onek) + "\n" + m.group(2), s)

    # --- olanaklar ------------------------------------------------------
    for v in ("Amenities &amp; Services", "Amenities & Services"):
        s = s.replace('<h2 class="h2">%s</h2>' % v,
                      '<h2 class="h2">Olanaklar ve Hizmetler</h2>')
    s = olanaklari_ele(s)
    for en, tr in OLANAK_TR.items():
        for v in (en, en.replace("&amp;", "&")):
            s = s.replace("<h3>%s</h3>" % v, "<h3>%s</h3>" % tr)
    s = re.sub(r"<h2 class=\"h2\">[^<]*Gift Vouchers: The Perfect Gift for Every Occasion!</h2>",
               "<h2 class=\"h2\">Park Ardeşen AVM Hediye Çeki</h2>", s)
    s = re.sub(r"(?s)(<h2 class=\"h2\">Park Ardeşen AVM Hediye Çeki</h2>\s*<div>).*?(</div>)",
               lambda m: m.group(1) + "\n" + HEDIYE_CEKI_TR + "\n" + m.group(2), s, count=1)
    s = s.replace("<span>Close</span>", "<span>Kapat</span>")

    # --- iletişim kısayolları ------------------------------------------
    s = s.replace("<h2 class=\"h2\">You can reach out to us directly</h2>",
                  "<h2 class=\"h2\">Bize doğrudan ulaşın</h2>")
    return s


def entry(s, ic):
    """`.entry-content` bloğunun içeriğini değiştirir."""
    return re.sub(r'(?s)(<div class="entry-content[^"]*">).*?(</div><!-- \.entry-content -->)',
                  lambda m: m.group(1) + "\n" + ic + "\n" + m.group(2), s, count=1)


# =====================================================================
# SAYFA İÇERİKLERİ
# =====================================================================

HAKKIMIZDA = """<div class="wp-block-media-text alignwide is-stacked-on-mobile is-vertically-aligned-top">
<figure class="wp-block-media-text__media">
<img src="{onek}{pa}gorseller/avm-dis-cephe.jpg" alt="Park Ardeşen AVM" loading="lazy" decoding="async">
</figure>
<div class="wp-block-media-text__content">
<h4 class="wp-block-heading">Park Ardeşen Alışveriş ve Yaşam Merkezi</h4>
<p>Park Ardeşen AVM, Rize'nin Ardeşen ilçesinde, Cumhuriyet Mahallesi Sultan Alparslan
Caddesi üzerinde hizmet veriyor. Alışverişi, yeme-içmeyi ve eğlenceyi tek çatı altında
toplayan merkez; ilçe sakinlerinin, çevre beldelerin ve bölgeye gelen misafirlerin
buluşma noktası.</p>
<p>Üç kata yayılan 17 mağazada moda, ayakkabı, ev tekstili, kozmetik ve market
ihtiyaçlarınızın tamamını karşılayabilirsiniz. LC Waikiki, Migros, FLO, Madame Coco ve
Bargello gibi Türkiye'nin sevilen markaları merkezimizde yan yana.</p>
<p>İkinci kattaki yeme-içme bölümünde Burger King, Popeyes, Gloria Jean's Coffees,
Defne Cafe &amp; Bar ve 1887'den bu yana geleneğini sürdüren Helvacı Yakub Efendi yer alıyor;
Sıroğlu Çikolata ise zemin katta hediyelik çikolatalarıyla sizi bekliyor.</p>
<p>Çocuklar için Berru Park oyun alanı, arkadaş grupları ve aileler için Grand Bowling
salonu merkezimizde. Ücretsiz otopark, mescit, bebek bakım odası ve engelli erişimi
ziyaretinizi kolaylaştırıyor.</p>
<p>Park Ardeşen AVM, inşaat ve turizm alanında faaliyet gösteren
<strong>YB Global Group</strong> bünyesinde işletilmektedir.</p>
</div></div>"""

HIZMETLER_GIRIS = """<p>Park Ardeşen AVM'de alışverişinizi kolaylaştıran ve ziyaretinizi
keyifli kılan hizmetleri aşağıda bulabilirsiniz. Sorularınız için zemin kattaki danışma
bankosuna uğrayabilir ya da {tel} numaralı telefondan bize ulaşabilirsiniz.</p>"""

ILETISIM = """<div class="pa-iletisim">
  <div class="pa-iletisim-kart">
    <h3>Adres</h3>
    <p>Cumhuriyet Mah. Sultan Alparslan Cad. No: 2/1<br>53400 Ardeşen / Rize</p>
    <a class="btn" href="{harita}" target="_blank" rel="noopener">Yol tarifi al</a>
  </div>
  <div class="pa-iletisim-kart">
    <h3>Telefon</h3>
    <p><a href="tel:+904647153030">{tel}</a></p>
    <h3>E-posta</h3>
    <p><a href="mailto:{eposta}">{eposta}</a></p>
  </div>
  <div class="pa-iletisim-kart">
    <h3>Çalışma saatleri</h3>
    <p>Pazartesi &ndash; Pazar<br>10:00 &ndash; 22:00</p>
    <p class="pa-kucuk">Resmî tatillerde ve özel günlerde saatler değişebilir.</p>
  </div>
</div>"""

SSS = [
 ("Park Ardeşen AVM nerede?",
  "<p>Merkezimiz Rize'nin Ardeşen ilçesinde, Cumhuriyet Mahallesi Sultan Alparslan Caddesi "
  "No: 2/1 adresinde yer alıyor. İlçe merkezinin tam ortasında, sahil yoluna yürüme mesafesinde.</p>"),
 ("Çalışma saatleriniz nedir?",
  "<p>Haftanın yedi günü 10:00 &ndash; 22:00 saatleri arasında hizmet veriyoruz. "
  "Ramazan ayı, bayramlar ve özel günlerde saatler değişebilir; güncel bilgi için "
  "%s numaralı telefondan bize ulaşabilirsiniz.</p>" % TEL),
 ("Otopark var mı?",
  "<p>Evet. Ziyaretçilerimiz için ücretsiz otopark bulunuyor.</p>"),
 ("Merkezde kaç mağaza var?",
  "<p>Üç kata yayılan 17 mağaza, kafe ve eğlence noktası bulunuyor. "
  "Güncel listeyi Mağazalar sayfasından görebilirsiniz.</p>"),
 ("Hangi markalar var?",
  "<p>LC Waikiki, Migros, FLO, Madame Coco, Bargello, Long Street, Paul &amp; Mark ve Lux "
  "başlıca mağazalarımız. Yeme-içme tarafında Burger King, Popeyes, Gloria Jean's Coffees, "
  "Defne Cafe &amp; Bar, Helvacı Yakub Efendi ve Sıroğlu Çikolata yer alıyor.</p>"),
 ("Çocuklar için oyun alanı var mı?",
  "<p>Evet. İkinci katta Berru Park oyun alanı ve Grand Bowling salonu bulunuyor.</p>"),
 ("Mescit ve bebek bakım odası var mı?",
  "<p>Her ikisi de mevcut. Ayrıca ilk yardım odası, engelli tuvaleti, bebek arabası ve "
  "telefon şarj noktaları hizmetinizde.</p>"),
 ("İade ve değişim nasıl yapılıyor?",
  "<p>İade ve değişim koşulları her mağazanın kendi politikasına tabidir. "
  "Park Ardeşen AVM mağazaların uyguladığı koşullar üzerinde belirleyici değildir.</p>"),
 ("Ücretsiz Wi-Fi var mı?",
  "<p>Evet, merkez genelinde ücretsiz Wi-Fi kullanabilirsiniz.</p>"),
 ("Mağaza kiralamak istiyorum, kiminle görüşmeliyim?",
  "<p>Mağaza, kiosk ve reklam alanı talepleriniz için %s numaralı telefondan ya da "
  "<a href=\"mailto:%s\">%s</a> adresinden kiralama ekibimize ulaşabilirsiniz.</p>"
  % (TEL, EPOSTA, EPOSTA)),
 ("Kayıp eşyamı nasıl bulabilirim?",
  "<p>Zemin kattaki danışma bankosuna başvurabilir ya da %s numaralı telefondan "
  "bilgi alabilirsiniz.</p>" % TEL),
 ("Hediye çeki satın alabilir miyim?",
  "<p>Evet. Hediye çekleri 250 TL, 500 TL, 1.000 TL ve 2.500 TL değerlerinde, zemin kattaki "
  "danışma bankosundan temin edilebilir ve bir yıl boyunca geçerlidir.</p>"),
]

KIRALAMA = """<h4 class="wp-block-heading">Park Ardeşen AVM'de yerinizi alın</h4>
<p>Park Ardeşen AVM, Ardeşen'in en yoğun caddesinde; ilçe sakinlerinin, çevre beldelerin ve
bölgeye gelen misafirlerin buluştuğu noktada yer alıyor. Üç kata yayılan merkezimizde
perakende mağaza, kiosk ve reklam alanları kiralanabilir.</p>
<h4 class="wp-block-heading">Mağaza kiralama</h4>
<p>Moda, ayakkabı, ev tekstili, kozmetik, elektronik ve yeme-içme kategorilerinde farklı
metrekarelerde mağaza seçenekleri sunuyoruz. Zemin kat cadde cepheli birimler, üst katlar
ise geniş kullanım alanı arayan markalar için uygundur.</p>
<h4 class="wp-block-heading">Kiosk, stant ve reklam alanları</h4>
<p>Kısa süreli tanıtım standı, kiosk, araç teşhiri, dijital ekran ve ATM yerleşimi gibi
esnek kullanım seçenekleri için de görüşebiliriz.</p>
<h4 class="wp-block-heading">Güncel boş birimler</h4>
<div data-pa-kiralama><p class="pa-bos">Birim listesi yükleniyor…</p></div>

<h4 class="wp-block-heading">İletişim</h4>
<p>Telefon: <a href="tel:+904647153030">{tel}</a><br>
E-posta: <a href="mailto:{eposta}">{eposta}</a><br>
Adres: {adres}</p>"""

KARIYER = """<p>Park Ardeşen AVM yönetim ekibinde şu anda açık pozisyon bulunmuyor.</p>
<p>Merkezimizde yer alan mağazaların personel ilanları için doğrudan ilgili mağazaya
başvurabilirsiniz. Yönetim ekibimizde değerlendirilmek üzere özgeçmişinizi
<a href="mailto:{eposta}">{eposta}</a> adresine gönderebilirsiniz; uygun bir pozisyon
açıldığında sizinle iletişime geçeriz.</p>"""

ULASIM = """<h4 class="wp-block-heading">Nerede?</h4>
<p>Park Ardeşen AVM, Ardeşen ilçe merkezinde, Cumhuriyet Mahallesi Sultan Alparslan Caddesi
No: 2/1 adresindedir. Karadeniz Sahil Yolu'ndan (D010) Ardeşen çıkışını kullanarak birkaç
dakikada merkeze ulaşabilirsiniz.</p>
<h4 class="wp-block-heading">Özel araçla</h4>
<p>Rize'den yaklaşık 50 km, Pazar'dan 20 km, Fındıklı'dan 15 km, Çamlıhemşin'den 20 km
mesafedeyiz. Ziyaretçilerimiz için ücretsiz otopark bulunuyor.</p>
<h4 class="wp-block-heading">Toplu taşımayla</h4>
<p>Ardeşen ilçe içi dolmuş hatları ve Rize &ndash; Hopa arasında çalışan sahil yolu
otobüsleri merkezimizin bulunduğu caddeden geçiyor. İlçe otogarına yürüme mesafesindeyiz.</p>
<h4 class="wp-block-heading">Yakın çevre</h4>
<p>Ayder Yaylası, Çamlıhemşin, Fırtına Vadisi ve Zilkale rotasına çıkmadan önce
ihtiyaçlarınızı karşılayabileceğiniz son duraklardan biriyiz.</p>
<p class="pa-kucuk">Sefer saatleri ve güncel ulaşım bilgisi için
<a href="tel:+904647153030">{tel}</a> numaralı telefondan bize ulaşabilirsiniz.</p>"""

FIRSAT = """<p>Her ayın ilk haftası Park Ardeşen AVM'de <strong>Fırsat Günleri</strong>!
Katılımcı mağazalarımız, hâlihazırda indirimli ürünlerin üzerine ekstra indirim uyguluyor.
Mağaza önlerine çıkarılan fırsat reyonlarında sezonun en iyi fiyatlarını bulabilirsiniz.</p>
<p>Güncel kampanyaları <a href="{onek}deals/index.html">Kampanyalar</a> sayfasından takip
edebilir, duyurular için <a href="https://www.instagram.com/parkardesenavm/" target="_blank"
rel="noopener">Instagram hesabımızı</a> izleyebilirsiniz.</p>"""

PARK_KART = """<h4 class="wp-block-heading">Park Kart nedir?</h4>
<p>Park Kart, Park Ardeşen AVM ziyaretçilerine özel hazırlanmış ücretsiz bir indirim kartıdır.
Katılımcı mağazalarımızda, mevcut indirimlerin üzerine ek avantajlar sunar.</p>
<h4 class="wp-block-heading">Nasıl alınır?</h4>
<p>Zemin kattaki danışma bankosuna uğramanız yeterli. Kartınızla birlikte o gün geçerli olan
katılımcı mağaza listesini de sizinle paylaşıyoruz.</p>
<h4 class="wp-block-heading">Nerede geçerli?</h4>
<p>Katılımcı mağaza listesi kampanya dönemine göre değişir. Güncel liste danışma bankosunda
ve <a href="https://www.instagram.com/parkardesenavm/" target="_blank" rel="noopener">Instagram
hesabımızda</a> yayımlanır.</p>
<p class="pa-kucuk">Ayrıntılı bilgi için: <a href="tel:+904647153030">{tel}</a> &middot;
<a href="mailto:{eposta}">{eposta}</a></p>"""

BASIN = """<p>Park Ardeşen AVM ile ilgili basın bültenleri ve haberler bu sayfada yayımlanır.
Şu anda görüntülenecek bir içerik bulunmuyor.</p>
<p>Basın mensupları görsel, bilgi ve röportaj talepleri için
<a href="mailto:{eposta}">{eposta}</a> adresine yazabilir ya da
<a href="tel:+904647153030">{tel}</a> numaralı telefondan bize ulaşabilir.</p>"""

BROSUR = """<p>Park Ardeşen AVM kat planı ve mağaza rehberi broşürü hazırlanıyor.
Hazır olduğunda bu sayfadan indirebileceksiniz.</p>
<p>Bu arada mağazalarımızın tam listesine
<a href="{onek}shops/index.html">Mağazalar</a> sayfasından,
kat yerleşimine ise <a href="{onek}mall-map/index.html">Kat Planı</a> sayfasından
ulaşabilirsiniz.</p>"""


KAMPANYA = [
    ("lc-waikiki",  "Sezon sonunda %50'ye varan indirim"),
    ("flo",         "İkinci çiftte %40 indirim"),
    ("migros",      "Money'e özel haftanın fırsatları"),
    ("madame-coco", "Ev tekstilinde %40 indirim"),
    ("bargello",    "3 al 2 öde"),
    ("burger-king", "Menüde ikinci ürün hediye"),
    ("popeyes",     "Çıtır menülerde %25 indirim"),
    ("berru-park",  "Hafta içi oyun kartında %30 indirim"),
]


def marka_gorsel(slug, onek):
    m = MAG[slug]
    if m.get("logo"):
        return ('<img src="%s%smarkalar/%s" alt="%s" loading="lazy" '
                'decoding="async" class="pa-marka-logo">' % (onek, PA, m["logo"], m["ad"]))
    return '<div class="pa-marka-yazi">%s</div>' % m["ad"]


def kampanya_kartlari(onek):
    return "\n".join(
        '<div class="col-12 col-sm-6 col-md-3">\n'
        '  <div class="card card-shop">\n'
        '    <div>\n'
        '      <div class="pa-logo-kutu pa-magaza-logo">%s</div>\n'
        '      <h2>%s</h2>\n'
        '      <div class="pa-magaza-bilgi"><span>%s</span></div>\n'
        '    </div>\n'
        '  </div>\n'
        '</div>' % (marka_gorsel(slug, onek), MAG[slug]["ad"], baslik)
        for slug, baslik in KAMPANYA)


def sss_html():
    return "\n".join(
        '<div class="faq-item">\n'
        '  <div class="faq-head"><div class="faq-icon"></div><h3>%s</h3></div>\n'
        '  <div class="faq-content">%s</div>\n'
        '</div>' % (s, c) for s, c in SSS)


def bicim(t, onek=""):
    return t.format(onek=onek, pa=PA, tel=TEL, eposta=EPOSTA, adres=ADRES,
                    harita=("https://www.google.com/maps/search/?api=1&query="
                            "Park+Arde%C5%9Fen+AVM+Arde%C5%9Fen+Rize"))


def entry2(s, ic):
    """`container … entry-content` (kapanış yorumu olmayan) blok."""
    return re.sub(r'(?s)(<div class="container container-small entry-content">).*?(</div>\s*</div>)',
                  lambda m: m.group(1) + "\n" + ic + "\n" + m.group(2), s, count=1)


ILETISIM_FORM = """<div class="pa-form-kutu">
  <h2 class="h2">Bize yazın</h2>
  <p class="pa-form-giris">Formu doldurduğunuzda mesajınız e-posta uygulamanızda
  hazır hâlde açılır; göndermek için tek yapmanız gereken &ldquo;Gönder&rdquo;
  demek. Dilerseniz doğrudan <a href="mailto:{eposta}">{eposta}</a> adresine de
  yazabilirsiniz.</p>
  <form class="pa-form" data-pa-iletisim novalidate>
    <div class="pa-form-satir">
      <label><span class="pa-form-etiket">Ad Soyad <b>*</b></span>
        <input name="ad" required autocomplete="name" placeholder="Adınız ve soyadınız">
      </label>
      <label><span class="pa-form-etiket">E-posta <b>*</b></span>
        <input name="eposta" type="email" required autocomplete="email"
               placeholder="ornek@eposta.com">
      </label>
    </div>
    <div class="pa-form-satir">
      <label><span class="pa-form-etiket">Telefon</span>
        <input name="telefon" type="tel" autocomplete="tel" placeholder="05xx xxx xx xx">
      </label>
      <label><span class="pa-form-etiket">Konu</span>
        <select name="konu">
          <option>Genel bilgi</option>
          <option>Mağaza kiralama</option>
          <option>Kariyer / iş başvurusu</option>
          <option>Kayıp eşya</option>
          <option>Öneri ve şikâyet</option>
          <option>Basın</option>
        </select>
      </label>
    </div>
    <label class="pa-form-genis">Mesajınız <span aria-hidden="true">*</span>
      <textarea name="mesaj" rows="6" required placeholder="Mesajınızı yazın"></textarea>
    </label>
    <label class="pa-form-onay">
      <input type="checkbox" name="kvkk" required>
      <span><a href="{onek}gizlilik-politikasi/">Gizlilik Politikası ve KVKK
      Aydınlatma Metni</a>ni okudum; mesajımı yanıtlayabilmeniz için kişisel
      verilerimin işlenmesini kabul ediyorum.</span>
    </label>
    <div class="pa-form-alt">
      <button type="submit" class="btn">Mesajı hazırla</button>
      <span class="pa-form-durum" role="status"></span>
    </div>
  </form>
</div>"""


SAYFALAR = {}

def sayfa(ad):
    def sar(fn):
        SAYFALAR[ad] = fn
        return fn
    return sar


@sayfa("about-dom")
def _(s, onek):
    return entry(s, bicim(HAKKIMIZDA, onek))


@sayfa("services")
def _(s, onek):
    return entry(s, bicim(HIZMETLER_GIRIS, onek))


@sayfa("contact-us")
def _(s, onek):
    s = entry(s, bicim(ILETISIM, onek))
    # Gravity Forms formu sunucusuz klonda çalışmıyordu ve KVKK açık rıza
    # kutusu yoktu; yerine e-posta uygulamasını açan kendi formumuz geçiyor.
    s = re.sub(r'(?s)(<div class="contact-form">).*?(</div>\s*</div>\s*</div>)',
               lambda m: m.group(1) + "\n" +
               ILETISIM_FORM.format(eposta=EPOSTA, onek=onek) + "\n" + m.group(2),
               s, count=1)
    for en, tr in (("Full Name", "Ad Soyad"), ("Email Address", "E-posta adresi"),
                   ("Phone Number", "Telefon"), ("Do you have any questions?", "Konu"),
                   ("Message", "Mesajınız")):
        s = s.replace(">%s</label>" % en, ">%s</label>" % tr)
    for en, tr in (("Enter name", "Adınız ve soyadınız"), ("Enter email address", "E-posta adresiniz"),
                   ("Enter number", "Telefon numaranız"), ("Ask", "Konu başlığı"),
                   ("Type message", "Mesajınızı yazın")):
        s = s.replace("placeholder='%s'" % en, "placeholder='%s'" % tr)
    s = s.replace("value='Send message'", "value='Gönder'")
    # statik klonda form gönderilemez; kullanıcıyı telefon/e-postaya yönlendir
    for en, tr in (("Careers", "Kariyer"), ("Media Center", "Medya Merkezi"),
                   ("Press", "Basında Biz")):
        s = s.replace("<h3>%s</h3>" % en, "<h3>%s</h3>" % tr)
    return s


@sayfa("faq")
def _(s, onek):
    return re.sub(r'(?s)(<section class="faq">\s*<div class="container container-small">).*?'
                  r'(</div><!-- \.container -->)',
                  lambda m: m.group(1) + "\n" + sss_html() + "\n" + m.group(2), s, count=1)


KIRALAMA_KART_1 = """<p>Ardeşen'in en işlek noktasında, cadde cepheli ve üst kat
mağaza birimleriyle markanıza uygun alanı bulabilirsiniz. Moda, ayakkabı, ev tekstili,
kozmetik, elektronik ve yeme-içme kategorilerinin tamamına uygun birimlerimiz mevcut.</p>
<p>Merkezimiz ilçe sakinlerinin yanı sıra Fındıklı, Pazar, Çamlıhemşin ve Ayder yolundaki
ziyaretçilerin de uğrak noktası; bu da mağazanız için istikrarlı bir müşteri akışı demek.</p>"""

KIRALAMA_KART_2 = """<p>Kısa süreli kullanım için kiosk, tanıtım standı, araç teşhir alanı,
dijital ekran ve ATM yerleşimi seçeneklerimiz var.</p>
<p>Sezonluk kampanya, lansman ve etkinlik alanı ihtiyaçlarınız için ekibimizle birlikte
size özel bir çözüm oluşturabiliriz.</p>"""


@sayfa("leasing")
def _(s, onek):
    s = entry(s, bicim(KIRALAMA, onek))
    s = re.sub(r'<h3 class="h2">Retail Leasing\s*</h3>',
               '<h3 class="h2">Mağaza kiralama</h3>', s)
    s = re.sub(r'<h3 class="h2">Specialty Leasing\s*</h3>',
               '<h3 class="h2">Kiosk ve reklam alanları</h3>', s)
    s = re.sub(r'(?s)(<h3 class="h2">Mağaza kiralama</h3>\s*<p>).*?(</p>\s*)(?=<a|</div>)',
               lambda m: m.group(1) + KIRALAMA_KART_1 + m.group(2), s, count=1)
    s = re.sub(r'(?s)(<h3 class="h2">Kiosk ve reklam alanları</h3>\s*<p>).*?(</p>\s*)(?=<a|</div>)',
               lambda m: m.group(1) + KIRALAMA_KART_2 + m.group(2), s, count=1)
    s = s.replace(">Apply ONLINE LEASING APPLICATION</a>", ">Kiralama başvurusu</a>")
    s = s.replace("CONTACT INFORMATION FOR LEASING &#8211;", "KİRALAMA İLETİŞİM")
    s = s.replace("CONTACT INFORMATION FOR LEASING –", "KİRALAMA İLETİŞİM")
    s = re.sub(r"Ena Marwah \(Head of Leasing\)", "Park Ardeşen AVM Kiralama Ekibi", s)
    s = s.replace("Phone:", "Telefon:").replace("Email:", "E-posta:")
    s = re.sub(r"Fax:\s*(<br\s*/?>)?", "", s)
    return s


@sayfa("careers")
def _(s, onek):
    return re.sub(r'(?s)<div class="jobs-none-container">.*?</div>',
                  '<div class="jobs-none-container">%s</div>' % bicim(KARIYER, onek), s, count=1)


@sayfa("brochure")
def _(s, onek):
    return entry2(s, bicim(BROSUR, onek))


@sayfa("tourism")
def _(s, onek):
    return entry2(s, bicim(ULASIM, onek))


@sayfa("bus-schedule")
def _(s, onek):
    # Dubai RTA otobüs tarifeleri yerine gerçek ulaşım bilgisi.
    yeni = ('<div class="container container-small">\n%s\n</div>'
            % bicim(ULASIM, onek))
    return re.sub(r'(?s)(</div><!-- \.breadcrumbs -->).*?(</main>)',
                  lambda m: m.group(1) + "\n" + yeni + "\n" + m.group(2), s, count=1)


@sayfa("bargain-monday")
def _(s, onek):
    s = re.sub(r'(?s)(<div class="col-12 col-md-6">\s*)<p>Unleash extra savings.*?</p>',
               lambda m: m.group(1) + bicim(FIRSAT, onek), s, count=1)
    return re.sub(r'(?s)(<div class="row">(?!\s*wrap)).*?(</div><!-- \.row -->)',
                  lambda m: m.group(1) + "\n" + kampanya_kartlari(onek) + "\n" + m.group(2),
                  s, count=1) if 'card-shop' in s else s


@sayfa("outlet-plus-card")
def _(s, onek):
    yeni = ('<div class="container container-small entry-content">\n%s\n</div>'
            % bicim(PARK_KART, onek))
    return re.sub(r'(?s)(</div><!-- \.breadcrumbs -->).*?(</main>)',
                  lambda m: m.group(1) + "\n" + yeni + "\n" + m.group(2), s, count=1)


@sayfa("press")
def _(s, onek):
    return re.sub(r'(?s)(<div class="entry-content container">).*?(</div><!-- \.entry-content -->)',
                  lambda m: m.group(1) + '\n<div class="container container-small">%s</div>\n'
                  % bicim(BASIN, onek) + m.group(2), s, count=1)


@sayfa("media-center")
def _(s, onek):
    s = s.replace("<p>Images</p>", "<p>Fotoğraflar</p>")
    s = s.replace("<p>Videos</p>", "<p>Videolar</p>")
    return s


@sayfa("deals")
def _(s, onek):
    return re.sub(r'(?s)(</div><!-- \.breadcrumbs -->\s*)<div class="row">.*?(</main>)',
                  lambda m: m.group(1) + '\n<div class="row">\n' + kampanya_kartlari(onek)
                  + '\n</div>\n</div>\n' + m.group(2), s, count=1)


def main():
    n = 0
    for ad, fn in SAYFALAR.items():
        f = os.path.join(ROOT, ad, "index.html")
        if not os.path.isfile(f):
            continue
        yedekle(f, ad + ".html")
        s0 = oku(f)
        s = ortak(s0, "../")
        s = fn(s, "../")
        if s != s0:
            yaz(f, s); n += 1
    print("  iç sayfalar: %d dosya güncellendi (%d sayfa şablonu)" % (n, len(SAYFALAR)))


if __name__ == "__main__":
    main()
