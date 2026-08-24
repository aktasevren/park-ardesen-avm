#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gizlilik, kullanım koşulları, medya merkezi, servis saatleri ve
wget'in ürettiği yedek anasayfa/mağaza kopyaları."""
import re, os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YEDEK = os.path.join(ROOT, "_orijinal")
PA = "wp-content/uploads/pa/"
TEL, EPOSTA = "0464 715 30 30", "muhasebe@parkardesen.com"


def yedekle(f, ad):
    os.makedirs(YEDEK, exist_ok=True)
    h = os.path.join(YEDEK, ad)
    if not os.path.exists(h):
        shutil.copy2(f, h)


GIZLILIK = """<h2 class="wp-block-heading">Gizlilik Politikası</h2>
<p>Bu politika, Park Ardeşen Alışveriş ve Yaşam Merkezi'ne ait internet sitesini
ziyaret ettiğinizde kişisel verilerinizin nasıl işlendiğini açıklar.</p>

<h3 class="wp-block-heading">Hangi verileri topluyoruz?</h3>
<p><strong>İletişim formu:</strong> Bize yazdığınızda paylaştığınız ad soyad, e-posta
adresi, telefon numarası ve mesaj içeriği.</p>
<p><strong>Otomatik toplanan veriler:</strong> Ziyaret ettiğiniz sayfalar, tarayıcı ve
cihaz bilgisi ile IP adresi gibi teknik kayıtlar.</p>
<p><strong>Çerezler:</strong> Sitenin düzgün çalışması ve tercihlerinizin hatırlanması
için çerez kullanıyoruz. Tarayıcı ayarlarınızdan çerezleri her zaman
silebilir veya engelleyebilirsiniz.</p>

<h3 class="wp-block-heading">Verileri hangi amaçla kullanıyoruz?</h3>
<p>Talep ve sorularınızı yanıtlamak, kiralama ve kariyer başvurularını değerlendirmek,
site kullanımını ölçmek ve iyileştirmek, yasal yükümlülüklerimizi yerine getirmek.</p>

<h3 class="wp-block-heading">Verileri kimlerle paylaşıyoruz?</h3>
<p>Kişisel verileriniz üçüncü kişilere satılmaz. Yalnızca hizmet aldığımız barındırma ve
altyapı sağlayıcılarıyla, hizmetin gerektirdiği ölçüde ve yetkili kamu kurumlarıyla
mevzuatın zorunlu kıldığı hâllerde paylaşılır.</p>

<h3 class="wp-block-heading">Saklama süresi</h3>
<p>Verileriniz, toplanma amacının gerektirdiği süre boyunca ve ilgili mevzuatta öngörülen
saklama süreleri sonuna kadar muhafaza edilir; sürenin sonunda silinir veya anonim hâle
getirilir.</p>

<h3 class="wp-block-heading">Haklarınız</h3>
<p>6698 sayılı Kişisel Verilerin Korunması Kanunu'nun 11. maddesi uyarınca; kişisel
verilerinizin işlenip işlenmediğini öğrenme, bilgi talep etme, düzeltilmesini veya
silinmesini isteme ve işlemeye itiraz etme haklarına sahipsiniz.</p>

<h3 class="wp-block-heading">İletişim</h3>
<p>Taleplerinizi <a href="mailto:{eposta}">{eposta}</a> adresine iletebilir ya da
<a href="tel:+904647153030">{tel}</a> numaralı telefondan bize ulaşabilirsiniz.<br>
Adres: Cumhuriyet Mah. Sultan Alparslan Cad. No: 2/1, 53400 Ardeşen / Rize</p>

<p class="pa-kucuk">Bu metin bilgilendirme amaçlıdır; yayına almadan önce hukuk
danışmanınızla birlikte gözden geçirmeniz önerilir.</p>"""

KOSULLAR = """<h2 class="wp-block-heading">Kullanım Koşulları</h2>
<p>Bu internet sitesini kullanarak aşağıdaki koşulları kabul etmiş olursunuz.</p>

<h3 class="wp-block-heading">Sitenin kullanımı</h3>
<p>Site, Park Ardeşen Alışveriş ve Yaşam Merkezi hakkında bilgi vermek amacıyla
yayımlanmaktadır. Siteyi hukuka aykırı biçimde, sistemlere zarar verecek şekilde veya
başkalarının haklarını ihlal edecek amaçlarla kullanamazsınız.</p>

<h3 class="wp-block-heading">İçeriğin doğruluğu</h3>
<p>Mağaza listesi, kat yerleşimi, çalışma saatleri ve kampanya bilgileri değişebilir.
Bilgileri güncel tutmak için çaba göstersek de kesin bilgi için danışma bankomuzdan
teyit almanızı öneririz.</p>

<h3 class="wp-block-heading">Kampanyalar ve mağaza uygulamaları</h3>
<p>Sitede yer alan kampanyalar ilgili mağazalar tarafından yürütülür. İndirim oranları,
stok durumu, iade ve değişim koşulları her mağazanın kendi politikasına tabidir;
Park Ardeşen AVM bu koşullar üzerinde belirleyici değildir.</p>

<h3 class="wp-block-heading">Fikri mülkiyet</h3>
<p>Sitede yer alan metin, görsel ve logolar ilgili hak sahiplerine aittir. Mağaza
logoları yalnızca tanıtım amacıyla kullanılmakta olup ilgili markaların mülkiyetindedir.
İzinsiz kopyalanamaz ve çoğaltılamaz.</p>

<h3 class="wp-block-heading">Dış bağlantılar</h3>
<p>Site, üçüncü taraflara ait adreslere bağlantı verebilir. Bu adreslerin içeriğinden
Park Ardeşen AVM sorumlu değildir.</p>

<h3 class="wp-block-heading">Değişiklik hakkı</h3>
<p>Bu koşullar önceden haber verilmeksizin güncellenebilir. Güncel metin her zaman bu
sayfada yayımlanır.</p>

<h3 class="wp-block-heading">İletişim</h3>
<p><a href="tel:+904647153030">{tel}</a> &middot;
<a href="mailto:{eposta}">{eposta}</a></p>

<p class="pa-kucuk">Bu metin bilgilendirme amaçlıdır; yayına almadan önce hukuk
danışmanınızla birlikte gözden geçirmeniz önerilir.</p>"""

SERVIS = """<h4 class="wp-block-heading">Çalışma saatlerimiz</h4>
<p>Park Ardeşen AVM haftanın yedi günü <strong>10:00 &ndash; 22:00</strong> saatleri
arasında açıktır. Market ve yeme-içme birimlerinin saatleri farklılık gösterebilir.</p>
<p>Ramazan ayı, resmî bayramlar ve özel günlerde saatler değişebilir; güncel bilgi için
<a href="tel:+904647153030">{tel}</a> numaralı telefondan bize ulaşabilirsiniz.</p>

<h4 class="wp-block-heading">Otopark</h4>
<p>Ziyaretçilerimiz için ücretsiz otopark bulunmaktadır. Otopark, merkezin açık olduğu
saatler boyunca hizmet verir.</p>

<h4 class="wp-block-heading">Servis ve ulaşım</h4>
<p>Merkezimiz Ardeşen ilçe merkezinde, dolmuş ve otobüs güzergâhının üzerinde yer alır;
bu nedenle ayrıca ring servisi işletilmemektedir. Ulaşım seçeneklerinin tamamı için
<a href="{onek}tourism/index.html">Ulaşım</a> sayfamıza bakabilirsiniz.</p>
<p>Grup ziyaretleri ve tur organizasyonları için servis talebinizi
<a href="mailto:{eposta}">{eposta}</a> adresine iletebilirsiniz.</p>"""


def medya_galeri(onek):
    gorseller = [
        ("gorseller/avm-dis-cephe.jpg", "Park Ardeşen AVM dış cephe"),
        ("gorseller/ic-mekan-1.webp", "Park Ardeşen AVM iç mekân"),
        ("gorseller/ic-mekan-2.webp", "Park Ardeşen AVM iç mekân"),
    ]
    kartlar = "\n".join(
        '<figure class="pa-medya-kart">'
        '<img src="%s%s%s" alt="%s" loading="lazy" decoding="async">'
        '<figcaption>%s</figcaption></figure>' % (onek, PA, p, a, a)
        for p, a in gorseller)
    return ('<div class="container container-small">\n'
            '<h2 class="h2">Fotoğraflar</h2>\n'
            '<div class="pa-medya">\n%s\n</div>\n'
            '<h2 class="h2">Videolar</h2>\n'
            '<p>Video içeriklerimiz hazırlanıyor. Güncel paylaşımlar için '
            '<a href="https://www.instagram.com/parkardesenavm/" target="_blank" '
            'rel="noopener">Instagram hesabımızı</a> takip edebilirsiniz.</p>\n'
            '<p class="pa-kucuk">Basın kullanımı için yüksek çözünürlüklü görsel '
            'taleplerinizi <a href="mailto:%s">%s</a> adresine iletebilirsiniz.</p>\n'
            '</div>' % (kartlar, EPOSTA, EPOSTA))


def bicim(t, onek=""):
    return t.format(onek=onek, tel=TEL, eposta=EPOSTA)


H1_TR = {
    "Privacy policy": "Gizlilik Politikası",
    "Privacy Policy": "Gizlilik Politikası",
    "Terms and conditions": "Kullanım Koşulları",
    "Terms and Conditions": "Kullanım Koşulları",
    "Media Center": "Medya Merkezi",
    "Bus Schedule": "Çalışma Saatleri ve Servis",
}


def govde_degistir(f, ic, onek):
    """Breadcrumb'dan </main>'e kadar olan bölümü değiştirir."""
    s = open(f, encoding="utf-8").read()
    yeni = re.sub(r'(?s)(</div><!-- \.breadcrumbs -->).*?(</main>)',
                  lambda m: m.group(1) + "\n" + ic + "\n" + m.group(2), s, count=1)
    for en, tr in H1_TR.items():
        yeni = yeni.replace("<h1>%s</h1>" % en, "<h1>%s</h1>" % tr)
    # üst banner görselini de AVM fotoğrafıyla değiştir
    i = yeni.find('<section class="common-banner">')
    if i >= 0:
        j = yeni.find('</section>', i)
        hedef = onek + PA + "gorseller/avm-dis-cephe.jpg"
        blok = re.sub(r'(?:https?://)?(?:\.\./)*(?:www\.)?(?:dubaioutletmall\.com/)?'
                      r'wp-content/uploads/\d{4}/\d{2}/[A-Za-z0-9._-]+\.(?:jpg|jpeg|png|webp)',
                      hedef, yeni[i:j])
        blok = re.sub(r'(srcset|data-srcset)="[^"]*"', r'\1="%s"' % hedef, blok)
        yeni = yeni[:i] + blok + yeni[j:]
    if yeni != s:
        open(f, "w", encoding="utf-8").write(yeni)
        return True
    return False


def main():
    n = 0
    hedefler = [
        ("gizlilik-politikasi/index.html", "privacy-policy.html", bicim(GIZLILIK, "../")),
        ("kullanim-kosullari/index.html", "terms.html", bicim(KOSULLAR, "../")),
        ("media-center/index.html", None, medya_galeri("../")),
        ("bus-schedule/index.html", None, bicim(SERVIS, "../")),
    ]
    for rel, yedek_ad, ic in hedefler:
        f = os.path.join(ROOT, rel)
        if not os.path.isfile(f):
            print("   atlandı (yok):", rel); continue
        if yedek_ad:
            yedekle(f, yedek_ad)
        sarmal = '<div class="container container-small entry-content">\n%s\n</div>\n</div>' % ic
        if govde_degistir(f, sarmal, "../"):
            n += 1
    print("  ek sayfalar: %d dosya güncellendi" % n)


if __name__ == "__main__":
    main()
