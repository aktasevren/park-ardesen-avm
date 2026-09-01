#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mağazalar (shops) ve Kat Planı (mall-map) sayfaları."""
import re, os, json, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VERI = json.load(open(os.path.join(ROOT, "pa-assets", "magazalar.json"), encoding="utf-8"))
KAT_SIRA = ["Zemin Kat", "1. Kat", "2. Kat"]
YEDEK = os.path.join(ROOT, "_orijinal")


def yedekle(yol, ad):
    os.makedirs(YEDEK, exist_ok=True)
    h = os.path.join(YEDEK, ad)
    if not os.path.exists(h):
        shutil.copy2(yol, h)


def kat_adi(m):
    return m.get("kat") or "Diğer"


def logo_img(m, onek):
    if m.get("logo"):
        return ('<img src="%swp-content/uploads/pa/markalar/%s" alt="%s" '
                'loading="lazy" decoding="async" class="pa-marka-logo">'
                % (onek, m["logo"], m["ad"]))
    return '<div class="pa-marka-yazi">%s</div>' % m["ad"]


def kartlar(onek):
    kat_ad = {k["slug"]: k["ad"] for k in VERI["kategoriler"]}
    out = []
    for m in VERI["magazalar"]:
        out.append(
            '<div class="col-12 col-sm-6 col-md-3" data-pa-kategori="%s" data-pa-ad="%s">\n'
            '  <div class="card card-shop">\n'
            '    <div>\n'
            '      <div class="pa-logo-kutu pa-magaza-logo">%s</div>\n'
            '      <h2>%s</h2>\n'
            '      <div class="pa-magaza-bilgi">'
            '<span>%s &middot; No: %s</span><span>%s</span></div>\n'
            '    </div>\n'
            '  </div>\n'
            '</div>'
            % (m["kategori"], m["ad"], logo_img(m, onek), m["ad"],
               kat_adi(m), m.get("no", "-"), kat_ad.get(m["kategori"], "")))
    return "\n".join(out)


def filtre_menusu(onek):
    bags = ['<a href="#" class="pa-aktif" data-pa-kategori="">Tümü</a>']
    for k in VERI["kategoriler"]:
        sayi = sum(1 for m in VERI["magazalar"] if m["kategori"] == k["slug"])
        if not sayi:
            continue
        bags.append('<a href="#" class="cat" data-pa-kategori="%s">%s (%d)</a>'
                    % (k["slug"], k["ad"], sayi))
    return "\n".join(bags)


# Mimari projedeki 1/50 kat planlarından alınan yerleşim. Mağaza rehberi
# panel verisinden gelir; kat planı bu tablodan çizilir. Adı olmayan birimler
# henüz kiralanmamıştır — listede yer almaz, şemada gri görünür.
PLAN = [
    ("Zemin Kat", ["LC Waikiki", "Gratis", "Gloria Jean's", "Kokoş",
                   "Bargello", "Migros", "Long Street"]),
    ("1. Kat",    ["LC Waikiki", "Paul & Mark", "Paul & Mark", "Paul & Mark"]),
    ("2. Kat",    ["Madame Coco", "Berru Park"]),
    ("3. Kat",    ["Defne Cafe", "Chocolate Lounge", "Popeyes", "Burger King"]),
]


def kat_plani(onek):
    bloklar = []
    for kat, magazalar in PLAN:
        satirlar = "\n".join("<li><span>%s</span></li>" % m for m in magazalar)
        bloklar.append('<div class="pa-kat"><h3>%s</h3><ul>%s</ul></div>' % (kat, satirlar))
    return ('<div class="container">\n'
            '<h2 class="h2 pa-kat-liste-baslik">Kat kat mağaza listesi</h2>\n'
            '<div class="pa-kat-plani">\n%s\n</div>\n'
            # izometrik şema (pa-veri.js çiziyor); JS yoksa yukarıdaki liste kalır
            '<h2 class="h2 pa-kat-liste-baslik pa-sema-baslik">Kat şeması</h2>\n'
            '<div class="pa-kat3d" data-pa-kat3d></div>\n'
            '</div>' % "\n".join(bloklar))


ORTAK = [
    ("<h1 class=\"page-title\">Shops<br>directory</h1>",
     "<h1 class=\"page-title\">Mağaza<br>rehberi</h1>"),
    ('placeholder="Search shops"', 'placeholder="Mağaza ara"'),
]


def form_duzelt(s, onek, aktif):
    for a, b in ORTAK:
        s = s.replace(a, b)
    # sekmeler
    s = re.sub(r'<a href="[^"]*shops/(?:index\.html)?" class="[^"]*">Mağaza Listesi</a>',
               '<a href="%sshops/index.html" class="%s">Mağaza Listesi</a>'
               % (onek, "active" if aktif == "liste" else ""), s)
    s = re.sub(r'<a href="[^"]*mall-map/(?:index\.html)?" class="[^"]*">Kat Planı</a>',
               '<a href="%small-map/index.html" class="%s">Kat Planı</a>'
               % (onek, "active" if aktif == "plan" else ""), s)
    # filtre listesi
    s = re.sub(r'(?s)(<div class="dropdown-menu-inner">).*?(</div>)',
               lambda m: m.group(1) + "\n" + filtre_menusu(onek) + "\n" + m.group(2),
               s, count=1)
    return s


def magazalar(f, onek):
    s = open(f, encoding="utf-8").read()
    s = form_duzelt(s, onek, "liste")
    yeni = ('<div class="row" data-pa-magaza-grid>\n%s\n</div>\n'
            '<div class="pa-magaza-yok">Aramanıza uygun mağaza bulunamadı.</div>\n'
            % kartlar(onek))
    # </form> ile </main> arasındaki her şeyi (kart ızgarası + sayfalama)
    # kendi ızgaramızla değiştir. Tekrar çalıştırılabilir olsun diye
    # aralığın tamamını hedefliyoruz.
    s = re.sub(r'(?s)(</form>).*?(</div>\s*</main>)',
               lambda m: m.group(1) + "\n" + yeni + m.group(2), s, count=1)
    open(f, "w", encoding="utf-8").write(s)


def kat_plani_sayfa(f, onek):
    s = open(f, encoding="utf-8").read()
    s = form_duzelt(s, onek, "plan")
    s = s.replace("<h1 class=\"page-title\">Mağaza<br>rehberi</h1>",
                  "<h1 class=\"page-title\">Kat<br>planı</h1>")
    # bu sayfada kart ızgarası yok; arama/filtre kutusunun işlevi de yok
    s = s.replace('<div class="shops-filter-search">',
                  '<div class="shops-filter-search pa-gizle">')
    # mapplic interaktif haritası Dubai'nin kat planını çiziyor; yerine
    # kendi kat rehberimizi koyuyoruz (orijinali _orijinal/ altında duruyor).
    s = re.sub(r'(?s)<div class="mall-map" id="map">.*?</div>\s*</div>\s*</div>',
               '<div class="mall-map" id="map">\n%s\n</div>' % kat_plani(onek),
               s, count=1)
    open(f, "w", encoding="utf-8").write(s)


def main():
    for alt, isim, fn in (("shops", "shops.html", magazalar),
                          ("mall-map", "mall-map.html", kat_plani_sayfa)):
        f = os.path.join(ROOT, alt, "index.html")
        if not os.path.isfile(f):
            continue
        yedekle(f, isim)
        fn(f, "../")
    print("  mağazalar + kat planı güncellendi (%d mağaza)" % len(VERI["magazalar"]))


if __name__ == "__main__":
    main()
