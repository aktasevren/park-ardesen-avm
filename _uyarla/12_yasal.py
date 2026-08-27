#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Yasal metinler: KVKK aydınlatma metni, gizlilik ve çerez politikası.

DİKKAT — [DOLDURULACAK] işaretli alanlar işletmenin resmî bilgileridir
(ticari unvan, vergi dairesi/numarası, MERSİS, KEP). Bunlar uydurulamaz;
site yayına alınmadan önce şirket tarafından doldurulmalı ve metinler bir
hukuk danışmanınca gözden geçirilmelidir.
"""
import re, os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YEDEK = os.path.join(ROOT, "_orijinal")

AD = "Park Ardeşen Alışveriş ve Yaşam Merkezi"
KISA = "Park Ardeşen AVM"
UNVAN = "[DOLDURULACAK: işletmenin resmî ticari unvanı]"
ADRES = "Cumhuriyet Mah. Sultan Alparslan Cad. No: 2/1, 53400 Ardeşen / Rize"
TEL = "0464 715 30 30"
EPOSTA = "muhasebe@parkardesen.com"
GUNCELLEME = "Ağustos 2026"

UYARI = ('<p class="pa-yasal-not"><strong>Not:</strong> Bu metin bilgilendirme '
         'amaçlıdır. Yayına almadan önce köşeli parantezle işaretlenmiş '
         'alanları doldurun ve metni hukuk danışmanınızla birlikte gözden '
         'geçirin.</p>')

# ---------------------------------------------------------------- gizlilik
GIZLILIK = """<h2 class="wp-block-heading">Gizlilik Politikası ve KVKK Aydınlatma Metni</h2>
<p class="pa-kucuk">Son güncelleme: {guncelleme}</p>

<h3 class="wp-block-heading">1. Veri sorumlusu</h3>
<p>6698 sayılı Kişisel Verilerin Korunması Kanunu (&ldquo;KVKK&rdquo;) uyarınca veri
sorumlusu sıfatıyla:</p>
<p><strong>Ticari unvan:</strong> {unvan}<br>
<strong>Adres:</strong> {adres}<br>
<strong>Telefon:</strong> <a href="tel:+904647153030">{tel}</a><br>
<strong>E-posta:</strong> <a href="mailto:{eposta}">{eposta}</a><br>
<strong>Vergi dairesi / numarası:</strong> [DOLDURULACAK]<br>
<strong>MERSİS numarası:</strong> [DOLDURULACAK]<br>
<strong>KEP adresi:</strong> [DOLDURULACAK]</p>

<h3 class="wp-block-heading">2. Hangi kişisel verileri işliyoruz?</h3>
<p><strong>Bize kendiniz ilettiğinizde:</strong> ad soyad, e-posta adresi, telefon
numarası ve mesaj içeriği (iletişim formu, e-posta veya telefon yoluyla);
kariyer başvurularında özgeçmişinizde yer alan bilgiler; mağaza kiralama
taleplerinde iletişim ve firma bilgileri.</p>
<p><strong>Siteyi ziyaret ettiğinizde otomatik olarak:</strong> IP adresi,
tarayıcı ve cihaz bilgisi, ziyaret edilen sayfalar ve ziyaret zamanı gibi
teknik kayıtlar (barındırma hizmeti sağlayıcımızın sunucu günlükleri).</p>
<p><strong>Çerezler ve benzeri teknolojiler:</strong> tarayıcınızın yerel
depolama alanında tutulan tercih kayıtları. Ayrıntı için
<a href="../cerez-politikasi/">Çerez Politikası</a> sayfamıza bakın.</p>
<p>Merkezimizde <strong>güvenlik kamerası (CCTV)</strong> bulunmaktadır; bu
kayıtlar fiziksel ziyaretlere ilişkindir ve bu internet sitesi kapsamı
dışındadır. Kamera kayıtlarına ilişkin aydınlatma, merkez girişlerinde
ayrıca yapılmaktadır.</p>

<h3 class="wp-block-heading">3. İşleme amaçları ve hukuki sebepleri</h3>
<p><strong>Talep ve sorularınızı yanıtlamak</strong> &mdash; KVKK m.5/2-c
(sözleşmenin kurulması veya ifasıyla doğrudan ilgili olması) ve m.5/2-f
(meşru menfaat).</p>
<p><strong>Kariyer ve kiralama başvurularını değerlendirmek</strong> &mdash;
KVKK m.5/2-c ve m.5/2-f.</p>
<p><strong>Sitenin güvenliğini ve düzgün çalışmasını sağlamak</strong> &mdash;
KVKK m.5/2-ç (hukuki yükümlülük) ve m.5/2-f.</p>
<p><strong>İsteğe bağlı çerezlerle site kullanımını ölçmek</strong> &mdash;
yalnızca <strong>açık rızanız</strong> varsa (KVKK m.5/1).</p>
<p><strong>Yasal yükümlülüklerimizi yerine getirmek</strong> &mdash; KVKK m.5/2-ç.</p>

<h3 class="wp-block-heading">4. Kişisel verilerin aktarılması</h3>
<p>Kişisel verileriniz üçüncü kişilere satılmaz, pazarlama amacıyla
paylaşılmaz. Yalnızca şu hâllerde ve gerektiği ölçüde aktarılır:</p>
<ul>
<li>Sitenin barındırıldığı altyapı ve teknik hizmet sağlayıcıları
(sunucu günlükleri kapsamında).</li>
<li>Yetkili kamu kurum ve kuruluşlarına, mevzuatın zorunlu kıldığı hâllerde.</li>
</ul>
<p>Barındırma hizmeti yurt dışında sunulabildiğinden, teknik kayıtlar
bakımından KVKK m.9 kapsamında yurt dışına aktarım söz konusu olabilir.
Bu aktarım, mevzuatın öngördüğü güvenceler çerçevesinde yapılır.</p>

<h3 class="wp-block-heading">5. Toplama yöntemi</h3>
<p>Kişisel verileriniz; internet sitesi üzerindeki formlar, e-posta, telefon
ve otomatik sunucu kayıtları aracılığıyla, kısmen otomatik ve otomatik
olmayan yollarla toplanır.</p>

<h3 class="wp-block-heading">6. Saklama süresi</h3>
<p>Verileriniz, işlendikleri amacın gerektirdiği süre boyunca ve ilgili
mevzuatta öngörülen zamanaşımı süreleri sonuna kadar saklanır. Sürenin
sonunda silinir, yok edilir veya anonim hâle getirilir.</p>

<h3 class="wp-block-heading">7. KVKK m.11 kapsamındaki haklarınız</h3>
<p>Kişisel verilerinizle ilgili olarak;</p>
<ul>
<li>işlenip işlenmediğini öğrenme, işlenmişse bilgi talep etme,</li>
<li>işlenme amacını ve amacına uygun kullanılıp kullanılmadığını öğrenme,</li>
<li>yurt içinde veya yurt dışında aktarıldığı üçüncü kişileri bilme,</li>
<li>eksik veya yanlış işlenmişse düzeltilmesini isteme,</li>
<li>şartları oluştuğunda silinmesini veya yok edilmesini isteme,</li>
<li>düzeltme, silme ve yok etme işlemlerinin aktarıldığı üçüncü kişilere
bildirilmesini isteme,</li>
<li>münhasıran otomatik sistemlerle analiz edilmesi suretiyle aleyhinize bir
sonuç doğmasına itiraz etme,</li>
<li>kanuna aykırı işleme sebebiyle zarara uğramanız hâlinde zararın
giderilmesini talep etme</li>
</ul>
<p>haklarına sahipsiniz.</p>

<h3 class="wp-block-heading">8. Başvuru</h3>
<p>Taleplerinizi, &ldquo;Veri Sorumlusuna Başvuru Usul ve Esasları Hakkında
Tebliğ&rdquo;e uygun şekilde; yazılı olarak <strong>{adres}</strong> adresine,
kayıtlı elektronik posta (KEP) adresimize ya da sistemimizde kayıtlı
e-posta adresinizden <a href="mailto:{eposta}">{eposta}</a> adresine
iletebilirsiniz. Başvurunuz en geç <strong>30 gün</strong> içinde
sonuçlandırılır.</p>

<h3 class="wp-block-heading">9. Değişiklikler</h3>
<p>Bu metin gerektiğinde güncellenir; güncel sürüm her zaman bu sayfada
yayımlanır.</p>

{uyari}"""

# ---------------------------------------------------------------- çerez
CEREZ = """<h2 class="wp-block-heading">Çerez Politikası</h2>
<p class="pa-kucuk">Son güncelleme: {guncelleme}</p>

<h3 class="wp-block-heading">Çerez nedir?</h3>
<p>Çerezler, bir internet sitesini ziyaret ettiğinizde tarayıcınıza kaydedilen
küçük metin dosyalarıdır. Bu sitede, klasik çerezlerin yanı sıra aynı işlevi
gören <strong>yerel depolama (localStorage / sessionStorage)</strong>
teknolojileri kullanılmaktadır. Bu politikada ikisi birlikte
&ldquo;çerez&rdquo; olarak anılmaktadır.</p>

<h3 class="wp-block-heading">Rızanız</h3>
<p>Zorunlu çerezler sitenin çalışması için gereklidir ve rıza gerektirmez.
Diğer tüm kategoriler <strong>varsayılan olarak kapalıdır</strong>; yalnızca
siz izin verdiğinizde çalışır. Tercihinizi dilediğiniz zaman sayfa altındaki
<a href="#" data-pa-cerez-ayar><strong>Çerez Ayarları</strong></a>
bağlantısından değiştirebilir veya rızanızı geri alabilirsiniz.</p>

<h3 class="wp-block-heading">Kullanılan çerezler</h3>
<div class="pa-tablo-sar">
<table class="pa-tablo">
<thead><tr><th>Ad</th><th>Kategori</th><th>Amaç</th><th>Süre</th><th>Taraf</th></tr></thead>
<tbody>
<tr><td>pa-cerez-izni</td><td>Zorunlu</td>
    <td>Çerez tercihinizi kaydeder; bandın tekrar tekrar çıkmasını önler</td>
    <td>Kalıcı (siz silene kadar)</td><td>Birinci taraf</td></tr>
<tr><td>pa-serit-kapali</td><td>Tercih</td>
    <td>Kapattığınız duyuru bandının tekrar açılmamasını sağlar</td>
    <td>Kalıcı</td><td>Birinci taraf</td></tr>
<tr><td>pa-pencere</td><td>Tercih</td>
    <td>Açılış duyuru penceresinin aynı oturumda tekrar gösterilmemesi</td>
    <td>Oturum süresi</td><td>Birinci taraf</td></tr>
<tr><td>pa-panel, pa-panel-s</td><td>Zorunlu</td>
    <td>Yönetim paneli oturumu (yalnızca yetkili personel)</td>
    <td>Oturum süresi</td><td>Birinci taraf</td></tr>
<tr><td>Google Haritalar gömme</td><td>Tercih</td>
    <td>Sayfa altındaki harita. <strong>Yalnızca tercih çerezlerine izin
        verdiyseniz</strong> yüklenir; izin yoksa yerine dış bağlantı
        gerektirmeyen bir harita görseli gösterilir. Yüklendiğinde Google
        çerez bırakabilir.</td>
    <td>Google'ın politikasına tabi</td><td>Üçüncü taraf (Google)</td></tr>
<tr><td>pa-veri</td><td>Zorunlu</td>
    <td>Yönetim panelinde düzenlenen site içeriğinin geçici kaydı
        (yalnızca yetkili personel)</td>
    <td>Kalıcı</td><td>Birinci taraf</td></tr>
</tbody>
</table>
</div>
<p>Bu sitede <strong>üçüncü taraf ölçümleme veya reklam çerezi
kullanılmamaktadır</strong>. Tek üçüncü taraf içerik, sayfa altındaki Google
Haritalar gömme haritasıdır ve yalnızca tercih çerezlerine izin verdiğinizde
yüklenir. İleride başka araç eklenmesi hâlinde bu tablo güncellenecek ve söz
konusu çerezler yalnızca açık rızanızla çalıştırılacaktır.</p>

<h3 class="wp-block-heading">Tarayıcı ayarları</h3>
<p>Çerezleri tarayıcı ayarlarınızdan da silebilir veya engelleyebilirsiniz.
Zorunlu çerezleri engellemeniz hâlinde sitenin bazı bölümleri düzgün
çalışmayabilir.</p>

<h3 class="wp-block-heading">İletişim</h3>
<p>Çerez kullanımıyla ilgili sorularınız için
<a href="mailto:{eposta}">{eposta}</a> adresine yazabilir ya da
<a href="tel:+904647153030">{tel}</a> numaralı telefondan bize
ulaşabilirsiniz. Kişisel verilerinizle ilgili haklarınız için
<a href="../gizlilik-politikasi/">Gizlilik Politikası ve KVKK Aydınlatma
Metni</a> sayfamıza bakabilirsiniz.</p>

{uyari}"""


# ---------------------------------------------------------------- işletme bilgisi
ISLETME = """<h3 class="wp-block-heading">İşletme bilgileri</h3>
<div class="pa-tablo-sar">
<table class="pa-tablo">
<tbody>
<tr><th>Ticari unvan</th><td>{unvan}</td></tr>
<tr><th>Adres</th><td>{adres}</td></tr>
<tr><th>Telefon</th><td><a href="tel:+904647153030">{tel}</a></td></tr>
<tr><th>E-posta</th><td><a href="mailto:{eposta}">{eposta}</a></td></tr>
<tr><th>Vergi dairesi / numarası</th><td>[DOLDURULACAK]</td></tr>
<tr><th>MERSİS numarası</th><td>[DOLDURULACAK]</td></tr>
<tr><th>KEP adresi</th><td>[DOLDURULACAK]</td></tr>
</tbody>
</table>
</div>"""


def bicim(t):
    return t.format(unvan=UNVAN, adres=ADRES, tel=TEL, eposta=EPOSTA,
                    guncelleme=GUNCELLEME, uyari=UYARI, ad=AD, kisa=KISA)


def govde_degistir(f, ic):
    s = open(f, encoding="utf-8").read()
    yeni = re.sub(r'(?s)(</div><!-- \.breadcrumbs -->).*?(</main>)',
                  lambda m: m.group(1) + "\n" +
                  '<div class="container container-small entry-content">\n%s\n</div>\n</div>' % ic +
                  "\n" + m.group(2), s, count=1)
    if yeni == s:
        return False
    open(f, "w", encoding="utf-8").write(yeni)
    return True


def cerez_sayfasi():
    """Çerez Politikası sayfasını kullanım koşulları şablonundan üretir."""
    kaynak = os.path.join(ROOT, "kullanim-kosullari", "index.html")
    if not os.path.isfile(kaynak):
        return False
    s = open(kaynak, encoding="utf-8").read()
    s = s.replace("<h1>Kullanım Koşulları</h1>", "<h1>Çerez Politikası</h1>")
    s = s.replace("<span>Kullanım Koşulları</span>", "<span>Çerez Politikası</span>")
    hedef = os.path.join(ROOT, "cerez-politikasi")
    os.makedirs(hedef, exist_ok=True)
    f = os.path.join(hedef, "index.html")
    open(f, "w", encoding="utf-8").write(s)
    return govde_degistir(f, bicim(CEREZ))


def iletisime_isletme_bilgisi():
    """İletişim sayfasına resmî işletme bilgilerini ekler."""
    f = os.path.join(ROOT, "contact-us", "index.html")
    if not os.path.isfile(f):
        return False
    s = open(f, encoding="utf-8").read()
    if "pa-isletme" in s:
        s = re.sub(r'(?s)<div class="pa-isletme">.*?</div>\s*<!--/pa-isletme-->', "", s)
    blok = ('<div class="pa-isletme">\n' + bicim(ISLETME) +
            '\n</div>\n<!--/pa-isletme-->')
    s = re.sub(r'(</div><!-- \.entry-content -->)',
               lambda m: blok + "\n" + m.group(1), s, count=1)
    open(f, "w", encoding="utf-8").write(s)
    return True


def main():
    n = 0
    f = os.path.join(ROOT, "gizlilik-politikasi", "index.html")
    if os.path.isfile(f) and govde_degistir(f, bicim(GIZLILIK)):
        n += 1
    if cerez_sayfasi():
        n += 1
    if iletisime_isletme_bilgisi():
        n += 1
    print("  yasal sayfalar: %d güncellendi (gizlilik/KVKK, çerez politikası, "
          "iletişim işletme bilgileri)" % n)


if __name__ == "__main__":
    main()
