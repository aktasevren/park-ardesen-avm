#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Park Ardeşen AVM — global uyarlama.
Klonlanan Dubai Outlet Mall aynasındaki her HTML'e uygulanır:
logo, menü, footer, marka adı, iletişim bilgisi, font katmanı, Shop Online kaldırma.
"""
import re, os, glob, shutil, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Site artık depo kökünde duruyor (URL'lerde klasör adı görünmesin diye).
# Aşağıdaki dizinler siteye ait değil, taranmaz.
HARIC = ('_yedek-ayna', '_orijinal', '_uyarla', 'panel', 'api', 'pa-assets', '.git')


def site_dosyalari(desen="*.html"):
    """Sitenin HTML/CSS dosyaları — yardımcı dizinler hariç."""
    out = []
    for kok, dizinler, dosyalar in os.walk(ROOT):
        dizinler[:] = [d for d in dizinler if d not in HARIC]
        for d in dosyalar:
            if glob.fnmatch.fnmatch(d, desen):
                out.append(os.path.join(kok, d))
    return sorted(out)

MARKA      = "Park Ardeşen Alışveriş ve Yaşam Merkezi"
MARKA_KISA = "Park Ardeşen AVM"
TEL_GOSTER = "0464 715 30 30"
TEL_HREF   = "tel:+904647153030"
EPOSTA     = "muhasebe@parkardesen.com"
ADRES_HTML = ("Cumhuriyet Mah. Sultan Alparslan Cad. No: 2/1,<br/>\n"
              "53400 Ardeşen / Rize<br/>\nTürkiye")
ENLEM, BOYLAM = 41.190868, 40.987404
HARITA     = "https://www.google.com/maps/search/?api=1&query=Park+Arde%C5%9Fen+AVM+Cumhuriyet+Mah.+Sultan+Alparslan+Cad.+Arde%C5%9Fen+Rize"
INSTAGRAM  = "https://www.instagram.com/parkardesenavm/"
FACEBOOK   = "https://www.facebook.com/parkardesen"
WHATSAPP   = "https://api.whatsapp.com/send?phone=904647153030"

# ---------------------------------------------------------------- varlıklar
def varliklari_kopyala():
    src = os.path.join(ROOT, "pa-assets")
    dst = os.path.join(ROOT, "wp-content", "uploads", "pa")
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print("  varlıklar → wp-content/uploads/pa/")

def html_dosyalari():
    return site_dosyalari("*.html")

def kok_oneki(dosya):
    """Dosyadan site köküne göreli önek: '', '../', '../../' …"""
    rel = os.path.relpath(ROOT, os.path.dirname(dosya)).replace(os.sep, "/")
    return "" if rel == "." else rel + "/"

# ---------------------------------------------------------------- metin haritaları
MENU_TR = {
    "Home": "Anasayfa",
    "Shops": "Mağazalar",
    "About Us": "Hakkımızda",
    "Mall Brochures": "Broşürler",
    "Contact Us": "İletişim",
    "Careers": "Kariyer",
    "Deals": "Kampanyalar",
    "FAQ&#8217;s": "Sıkça Sorulan Sorular",
    "FAQ’s": "Sıkça Sorulan Sorular",
    "Leasing": "Mağaza Kiralama",
    "Services": "Hizmetlerimiz",
    "Bargain Monday": "Fırsat Günleri",
    "Outlet Plus Card": "Park Kart",
    "Shuttle Services": "Ulaşım",
    "Bus Schedule": "Çalışma Saatleri",
    "Media Center": "Medya Merkezi",
    "Press": "Basında Biz",
    "Mall Map": "Kat Planı",
    "Tourism": "Ulaşım",
    "Privacy policy": "Gizlilik Politikası",
    "Terms and conditions": "Kullanım Koşulları",
    "Shops List": "Mağaza Listesi",
    "Map View": "Kat Planı",
    "Filter": "Filtrele",
    "All": "Tümü",
}

BASLIK_TR = {
    "Dubai Outlet Mall &#8211; Premium brands at amazing bargains":
        MARKA_KISA + " &#8211; Karadeniz&#8217;in buluşma noktası",
    "About Us": "Hakkımızda", "Shops": "Mağazalar", "Services": "Hizmetlerimiz",
    "Contact Us": "İletişim", "FAQ&#8217;s": "Sıkça Sorulan Sorular",
    "Leasing": "Mağaza Kiralama", "Careers": "Kariyer", "Mall Map": "Kat Planı",
    "Mall Brochures": "Broşürler", "Bus Schedule": "Çalışma Saatleri",
    "Tourism": "Ulaşım", "Bargain Monday": "Fırsat Günleri",
    "Outlet Plus Card": "Park Kart", "Media Center": "Medya Merkezi",
    "Press": "Basında Biz", "Deals": "Kampanyalar",
    "Privacy Policy": "Gizlilik Politikası",
    "Terms and Conditions": "Kullanım Koşulları",
}

# ---------------------------------------------------------------- dönüşümler
def dil(s):
    return re.sub(r'(<html[^>]*\slang=")[^"]*(")', r'\1tr-TR\2', s, count=1)

def baslik(s):
    def rep(m):
        t = m.group(1)
        if t in BASLIK_TR:
            yeni = BASLIK_TR[t]
        else:
            yeni = t
        if " &#8211; Dubai Outlet Mall" in t:
            sol = t.split(" &#8211; Dubai Outlet Mall")[0]
            yeni = BASLIK_TR.get(sol, sol) + " &#8211; " + MARKA_KISA
        return "<title>%s</title>" % yeni
    return re.sub(r"<title>(.*?)</title>", rep, s, flags=re.S)

def logolar(s, onek):
    dark = onek + "wp-content/uploads/pa/logo/parkardesen-logo-dark.svg"
    light = onek + "wp-content/uploads/pa/logo/parkardesen-logo-light.svg"
    # footer bloğunda beyaz, geri kalanda koyu sürüm
    i = s.find('class="site-footer-logo"')
    def swap(parca, hedef):
        parca = re.sub(r'[^"\'\s]*wp-content/uploads/2024/05/Dom-Logo\.svg', hedef, parca)
        return parca
    if i > 0:
        j = s.find("</a>", i)
        s = s[:i] + swap(s[i:j], light) + s[j:]
    s = swap(s, dark)
    s = s.replace('alt="Dubai Outlet Mall"', 'alt="%s"' % MARKA)
    return s

SHOP_ONLINE = re.compile(
    r'\s*<a class="btn-reset btn d-none d-md-block"[^>]*>\s*SHOP ONLINE\s*</a>', re.I)

# sitede arama yok; başlıktaki büyüteç yanıltıcıydı
ARAMA = re.compile(r'(?s)\s*<a class="btn-reset btn-search"[^>]*>.*?</a>')

def header(s, onek):
    s = SHOP_ONLINE.sub("", s)
    s = ARAMA.sub("", s)
    s = s.replace("<span>Menu</span>", "<span>Menü</span>")
    s = s.replace("<h2>Menu</h2>", "<h2>Menü</h2>")
    s = s.replace("<span>Map</span>", "<span>Harita</span>")
    s = s.replace('alt="map-icon"', 'alt="harita"')
    s = s.replace("https://goo.gl/maps/VushYrjEDbymymrk7", HARITA)
    return s

SOSYAL = {
    "https://twitter.com/DubaiOutletMall": None,
    "https://www.youtube.com/user/OutletMallDubai": None,
    "https://www.linkedin.com/company/dubai-outlet-mall": None,
    "https://www.tiktok.com/@dubaioutletmall": WHATSAPP,
    "https://www.facebook.com/DubaiOutletMall": FACEBOOK,
    "https://www.instagram.com/dubaioutletmall/": INSTAGRAM,
}

def sosyal(s):
    # hesabı olmayan ağların <li> bloklarını kaldır, olanların adresini değiştir
    def rep(m):
        blok, url = m.group(0), m.group(1)
        if url in SOSYAL:
            hedef = SOSYAL[url]
            if hedef is None:
                return ""
            return blok.replace(url, hedef)
        return blok
    return re.sub(r'<li>\s*<a href="(https://(?:www\.)?(?:twitter|facebook|instagram|youtube|linkedin|tiktok)\.com[^"]*)".*?</li>',
                  rep, s, flags=re.S)


# Daha önceki geçişlerde konmuş Türkçe etiketleri düzelten harita
# (betik tekrar çalıştırıldığında İngilizce kaynak metin artık yok).
DUZELTME = {
    "Servis Hizmetleri": "Ulaşım",
    "Servis Saatleri": "Çalışma Saatleri",
}


# TikTok bağlantısını WhatsApp'a çevirirken ikonu da değiştirmek gerekiyor
WHATSAPP_SVG = (
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" '
    'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    '<path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.46 1.32 4.97L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.18-1.15l-.3-.18-3.11.82.83-3.04-.19-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.23-8.23 2.2 0 4.26.86 5.81 2.41a8.17 8.17 0 0 1 2.41 5.83c0 4.54-3.7 8.23-8.23 8.23Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.25-.64.81-.79.97-.14.17-.29.19-.54.07-.25-.13-1.05-.39-2-1.23-.74-.66-1.24-1.47-1.38-1.72-.15-.25-.02-.39.11-.51.11-.11.25-.29.37-.44.12-.14.16-.25.25-.41.08-.17.04-.31-.03-.44-.06-.12-.56-1.34-.76-1.83-.2-.48-.4-.42-.56-.42-.14 0-.31-.02-.47-.02-.17 0-.43.06-.66.31-.22.25-.85.83-.85 2.02s.87 2.35 1 2.51c.12.17 1.71 2.61 4.14 3.66.58.25 1.03.4 1.38.51.58.19 1.11.16 1.53.1.46-.07 1.42-.58 1.62-1.15.2-.56.2-1.05.14-1.15-.06-.1-.22-.16-.47-.29Z" fill="#171717"/></svg>')


def whatsapp_ikonu(s):
    return re.sub(
        r'(<a href="' + re.escape(WHATSAPP) + r'"[^>]*>\s*<span class="wp-svg-img">)'
        r'<svg.*?</svg>(\s*</span>)',
        lambda m: m.group(1) + WHATSAPP_SVG + m.group(2), s, flags=re.S)

def menuler(s):
    for en, tr in MENU_TR.items():
        s = s.replace(">%s</a>" % en, ">%s</a>" % tr)
        s = s.replace(">%s</span>" % en, ">%s</span>" % tr)
    for eski, yeni in DUZELTME.items():
        s = s.replace(">%s</a>" % eski, ">%s</a>" % yeni)
        s = s.replace(">%s</span>" % eski, ">%s</span>" % yeni)
    # Mağazalar bağlantısı, artık silinmiş olan sayfalı listeye gidiyordu
    s = re.sub(r'href="((?:\.\./)*)shops/page/\d+/index\.html"',
               r'href="\1shops/index.html"', s)
    s = re.sub(r'href="page/\d+/index\.html"', 'href="index.html"', s)
    # çerez bildirimindeki "#" bağlantısı sayfa yoluna yapışmıştı
    s = re.sub(r'href="[^"]*page/\d+/index\.html(#[^"]*)"', r'href="\1"', s)
    return s

YASAL_MENU = (
    '<li><a href="{onek}gizlilik-politikasi/index.html">Gizlilik Politikası ve KVKK</a></li>'
    '<li><a href="{onek}cerez-politikasi/index.html">Çerez Politikası</a></li>'
    '<li><a href="#" data-pa-cerez-ayar>Çerez Ayarları</a></li>'
    '<li><a href="{onek}kullanim-kosullari/index.html">Kullanım Koşulları</a></li>')


# Footer'daki mini harita.
#
# Görünen katman: derleme sırasında üretilmiş yerel bir harita görseli
# (bkz. 14_harita.py). Üçüncü tarafa bağlanmadığı için rıza gerektirmez ve
# herkeste görünür.
# Rıza verildiyse pa-cerez.js bunun yerine etkileşimli Google Haritalar'ı
# yüklüyor. Google gömme haritası çerez bırakıp IP'yi dışarı verdiği için
# rızasız yüklenmiyor.
HARITA_BLOK = (
    '<!--PA-HARITA-->'
    '<div class="pa-mini-harita" data-pa-harita '
    'data-embed="https://maps.google.com/maps?q={enlem},{boylam}&amp;z=16&amp;output=embed">'
    '<a class="pa-harita-onizleme" href="{harita}" target="_blank" rel="noopener" '
    'aria-label="Park Ardeşen AVM konumu — Google Haritalar\'da aç">'
    '<img src="{onek}wp-content/uploads/pa/gorseller/harita.png" '
    'alt="Park Ardeşen AVM\'in Ardeşen, Rize\'deki konumunu gösteren harita" '
    'loading="lazy" decoding="async" width="380" height="190"></a>'
    '<a class="pa-harita-yol" href="{harita}" target="_blank" rel="noopener">Yol tarifi al</a>'
    '<span class="pa-harita-katki">&copy; OpenStreetMap</span>'
    '</div>'
    '<!--/PA-HARITA-->')

ESKI_HARITA = re.compile(r'(?s)<!--PA-HARITA-->.*?<!--/PA-HARITA-->'
                         r'|<div class="pa-mini-harita".*?</div>\s*</div>'
                         r'|<a class="pa-mini-harita".*?</a>')


def footer(s, onek=""):
    s = s.replace("<h2>ABOUT US</h2>", "<h2>KURUMSAL</h2>")
    s = s.replace("<h2>VISITORS INFORMATION</h2>", "<h2>ZİYARETÇİ BİLGİLERİ</h2>")
    s = s.replace("<h2>CONTACT INFO</h2>", "<h2>İLETİŞİM</h2>")
    s = re.sub(r"Dubai Outlet Mall,<br/>\s*Dubai Al-Ain Road \(Route 66\),<br/>\s*Dubai, UAE\.",
               ADRES_HTML, s)
    # adresin hemen altına küçük harita (eski sürüm varsa değiştirilir)
    s = ESKI_HARITA.sub("", s)
    s = s.replace(ADRES_HTML, ADRES_HTML + "\n" +
                  HARITA_BLOK.format(harita=HARITA, onek=onek,
                                     enlem=ENLEM, boylam=BOYLAM), 1)
    s = re.sub(r'<a href="tel:\+971 44234666">\+971 44234666</a>',
               '<a href="%s">%s</a>' % (TEL_HREF, TEL_GOSTER), s)
    s = re.sub(r"©dubaioutletmall \d{4}, All Rights Reserved",
               "© %s %s. Tüm hakları saklıdır." % ("2026", MARKA_KISA), s)
    # footer yasal bağlantıları — çerez ayarları dahil (rıza geri alınabilmeli)
    s = re.sub(r'(?s)(<div class="terms-privacy">\s*<ul>).*?(</ul>)',
               lambda m: m.group(1) + YASAL_MENU.format(onek=onek) + m.group(2), s)
    return s

CF_MAIL = re.compile(
    r'<a href="[^"]*email-protection#[0-9a-f]+"[^>]*>\s*<span class="__cf_email__"[^>]*>.*?</span>\s*</a>',
    re.S)
CF_MAIL_SPAN = re.compile(r'<span class="__cf_email__"[^>]*>.*?</span>', re.S)

def eposta(s):
    s = CF_MAIL.sub('<a href="mailto:%s">%s</a>' % (EPOSTA, EPOSTA), s)
    s = CF_MAIL_SPAN.sub(EPOSTA, s)
    return s

def temizle(s):
    # Cloudflare rocket-loader / email-decode: çevrimdışı çalışmaz, gereksiz istek
    s = re.sub(r'<script[^>]*cdn-cgi/scripts/[^>]*></script>', "", s)
    return s

MARKA_STR = [
    ("Dubai Outlet Mall", MARKA_KISA),
    ("dubai outlet mall", MARKA_KISA),
    ("DUBAI OUTLET MALL", MARKA_KISA.upper()),
    ("Dubai Outlet mall", MARKA_KISA),
    ("+97144234666", TEL_GOSTER),
    ("+971 44234666", TEL_GOSTER),
    ("+971 4 4234 666", TEL_GOSTER),
    ("+971 4423 4666", TEL_GOSTER),
    ("+971 43679009", ""),
    ("+971 4367 9009", ""),
]


COOKIE_TR = ("Deneyiminizi iyileştirmek için çerez kullanıyoruz. Siteyi kullanmaya "
             "devam ettiğinizde çerez kullanımını kabul etmiş sayılırsınız.")

def cerez(s):
    s = s.replace("We use cookies to ensure that we give you the best experience on our "
                  "website. If you continue to use this site we will assume that you are "
                  "happy with it.", COOKIE_TR)
    s = s.replace('aria-label="Cookie Notice"', 'aria-label="Çerez bildirimi"')
    s = s.replace('aria-label="Ok" style="background-color: #00a99d">Ok</a>',
                  'aria-label="Tamam" style="background-color: #00a99d">Tamam</a>')
    s = s.replace('class="cn-close-icon" title="No"', 'class="cn-close-icon" title="Kapat"')
    return s

def marka(s):
    for a, b in MARKA_STR:
        s = s.replace(a, b)
    return s

def enjekte(s, onek):
    """Font katmanı, stil, veri katmanı ve AVM JS dosyalarını ekle.

    pa-veri.js panel/veri.json'u okuyup kampanya, duyuru, kiralama ve mağaza
    içeriğini çalışma anında çiziyor; dosyayı bulabilmesi için sayfanın
    derinliğine göre iki yol meta olarak veriliyor."""
    if "pa-avm.css" in s:
        # daha eski bir sürümle enjekte edilmişse eksikleri tamamla
        if "pa-veri-url" not in s:
            s = s.replace("</head>",
                          '<meta name="pa-veri-url" content="%spanel/veri.json">\n'
                          '<meta name="pa-site-kok" content="%s">\n' % (onek, onek) +
                          "</head>", 1)
        else:
            s = re.sub(r'<meta name="pa-veri-url" content="[^"]*">',
                       '<meta name="pa-veri-url" content="%spanel/veri.json">' % onek, s)
            s = re.sub(r'<meta name="pa-site-kok" content="[^"]*">',
                       '<meta name="pa-site-kok" content="%s">' % onek, s)
        for betik in ("pa-veri.js", "pa-cerez.js"):
            if betik not in s:
                s = s.replace("</body>",
                              '<script src="%swp-content/uploads/pa/%s"></script>\n'
                              % (onek, betik) + "</body>", 1)
        return s
    bas = ('\n<meta name="pa-veri-url" content="%spanel/veri.json">\n'
           '<meta name="pa-site-kok" content="%s">\n'
           '<link rel="stylesheet" href="%swp-content/uploads/pa/fonts/pa-fonts.css">\n'
           '<link rel="stylesheet" href="%swp-content/uploads/pa/pa-avm.css">\n'
           % (onek, onek, onek, onek))
    s = s.replace("</head>", bas + "</head>", 1)
    js = ('\n<script src="%swp-content/uploads/pa/pa-avm.js"></script>\n'
          '<script src="%swp-content/uploads/pa/pa-veri.js"></script>\n'
          '<script src="%swp-content/uploads/pa/pa-cerez.js"></script>\n'
          % (onek, onek, onek))
    s = s.replace("</body>", js + "</body>", 1)
    return s

def main():
    varliklari_kopyala()
    n = 0
    for f in html_dosyalari():
        s0 = open(f, encoding="utf-8", errors="replace").read()
        onek = kok_oneki(f)
        s = s0
        s = dil(s); s = baslik(s); s = logolar(s, onek); s = header(s, onek)
        s = sosyal(s); s = whatsapp_ikonu(s); s = menuler(s)
        s = footer(s, onek); s = eposta(s)
        s = temizle(s); s = cerez(s); s = marka(s); s = enjekte(s, onek)
        if s != s0:
            open(f, "w", encoding="utf-8").write(s)
            n += 1
    print("  %d HTML dosyası güncellendi" % n)

if __name__ == "__main__":
    main()
