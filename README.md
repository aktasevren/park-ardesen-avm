# Park Ardeşen AVM — web sitesi

Park Ardeşen Alışveriş ve Yaşam Merkezi (YB Global Group) için hazırlanan statik site.
Tasarım, `dubaioutletmall.com` klonundan birebir korunarak Türkçeleştirildi ve AVM'ye
uyarlandı. Türkçe, İngilizce, Gürcüce ve Arapça olmak üzere dört dilde yayımlanır.

---

## Devir notları — 30 saniyede özet

**Ne bu?** Build gerektirmeyen, tamamen statik bir site. Sunucu tarafında yalnızca tek
bir serverless fonksiyon var (`api/kaydet.js`). İçerik `panel/veri.json` dosyasında
durur; site bu dosyayı **çalışma anında** okuyup ilgili blokları çizer.

| | |
|---|---|
| **Depo** | <https://github.com/aktasevren/park-ardesen-avm> (`main`) |
| **Yayın** | Vercel — `main`'e her push kendiliğinden dağıtılır (~1 dk) |
| **Site** | <https://park-ardesen-avm.vercel.app> |
| **Panel** | <https://park-ardesen-avm.vercel.app/panel> · **şifre: `parkardesen2026`** |
| **Diller** | `/` (tr) · `/en/` · `/ka/` · `/ar/` |
| **Yerel** | `python3 serve.py 8001` → <http://localhost:8001/> |

**Panel şifresini değiştirmek** iki yerde birden yapılmalı, yoksa "Yayınla" çalışmaz:

1. `panel/panel.js` içindeki `var SIFRE = "parkardesen2026";`
2. Vercel → Settings → Environment Variables → `PANEL_SIFRE` (sonra **Redeploy**)

**Bağımlılık yok.** `npm install` yok, `package.json` yok, derleme adımı yok. Site
olduğu gibi servis edilir. Yalnızca *içerik uyarlama betikleri* Python 3 ister
(standart kütüphane + `Pillow` yalnızca `14_harita.py` için).

### Bir içerik değişikliği nasıl yapılır?

1. `/panel` → şifre → soldan bölüm seç → alanları doldur → **Tamam**
2. **Kaydet** — değişiklik *yalnızca sizin tarayıcınıza* yazılır (anında görürsünüz)
3. **Yayınla** — veriyi GitHub'a commit'ler, Vercel yeniden dağıtır, **herkes** görür

Panele ilk girişte Genel Bakış'ta 7 adımlık kısa bir eğitim açılır; "Anladım"
denince kapanır, aynı sayfanın altındaki düğmeyle tekrar açılabilir.

### Bir tasarım/yapı değişikliği nasıl yapılır?

HTML dosyalarını **elle düzenlemeyin** — `_uyarla/*.py` zinciri onları yeniden üretir
ve değişikliğiniz kaybolur. Doğru yol: ilgili betiği düzenleyip zinciri çalıştırmak.

    ./_uyarla/tumunu_calistir.sh

Zincir idempotanttır: iki kez çalıştırınca çıktı bit bit aynı kalır.

### Yayına almadan önce yapılacaklar

- `_uyarla/12_yasal.py` içindeki **`[DOLDURULACAK]`** alanlar: ticari unvan,
  vergi dairesi/numarası, MERSİS numarası, KEP adresi
- Binanın **tam koordinatı** — şu an Cumhuriyet Mahallesi merkezi
  (`41.190868, 40.987404`); `14_harita.py` → `KONUM` ve `11_seo.py` → `ENLEM/BOYLAM`
- Kendi alan adına geçilecekse `11_seo.py` → `SITE_URL`
- Panel şifresinin değiştirilmesi (yukarıdaki iki yer)

---

## Yerel çalıştırma

    python3 serve.py 8001
    # http://localhost:8001/

## Yapı

Site **depo kökünde** duruyor; URL'lerde klasör adı görünmüyor
(`/shops/`, `/duyurular/`, `/gizlilik-politikasi/` …).

| Yol | Ne |
|---|---|
| `index.html`, `shops/`, `duyurular/`, `wp-content/` … | **Site** |
| `gizlilik-politikasi/`, `kullanim-kosullari/` | Yasal metinler (Türkçe adreslerle) |
| `pa-assets/` | Park Ardeşen'e ait varlıkların **kaynağı**: logo, mağaza logoları, fotoğraflar, `pa-avm.css`, `pa-avm.js`, `pa-veri.js`, fontlar |
| `panel/` | Yönetim paneli + `veri.json` (site içeriğinin tek kaynağı) |
| `api/` | Vercel serverless fonksiyonu (`kaydet.js` — panelden gelen veriyi GitHub'a commit'ler) |
| `_uyarla/` | Uyarlama betikleri (aşağıya bakın) — dağıtıma girmez |
| `_dil/` | Dil çıkarma/üretme araçları ve `sozluk.json` — dağıtıma girmez |
| `_orijinal/` | Büyük ölçüde yeniden yazılan sayfaların **klon hâlindeki** yedekleri + orijinal site ikonları ve fontları |
| `serve.py` | Yerel geliştirme sunucusu |

`pa-assets/` her çalıştırmada `*/wp-content/uploads/pa/` altına kopyalanır. **Varlıkları
`pa-assets/` içinde düzenleyin**, aynaların içindekiler üzerine yazılır.

## Uyarlama betikleri

Tamamı yeniden çalıştırılabilir. Zinciri baştan kurmak için:

    ./_uyarla/tumunu_calistir.sh

| Betik | İş |
|---|---|
| `01_global.py` | Logo, menü, footer, marka adı, iletişim bilgisi, sosyal medya, çerez bildirimi, Shop Online'ın kaldırılması, font/CSS/JS enjeksiyonu — **tüm HTML'lere** |
| `02_anasayfa.py` | Anasayfa: hero, vitrin mağazaları, kategoriler, kampanyalar, galeri; online mağaza bölümünün kaldırılması |
| `03_magazalar.py` | Mağaza rehberi ve kat planı (mağaza listesi `panel/veri.json`'dan) |
| `04_sayfalar.py` | Hakkımızda, Hizmetlerimiz, İletişim, SSS, Kiralama, Kariyer, Ulaşım, Fırsat Günleri, Park Kart, Kampanyalar + ortak bloklar |
| `05_ek_sayfalar.py` | Gizlilik, Kullanım Koşulları |
| `06_baglantilar.py` | Kalan mutlak `dubaioutletmall.com` adreslerini yerel göreli yollara çevirir |
| `07_font_duzelt.py` | Golos Text'in bozuk `ğ/Ğ` gliflerini onarır |
| `08_cloudflare.py` | Cloudflare Rocket Loader izlerini ve ölü eklenti dosyalarını temizler (zincirde **ilk** çalışır) |
| `09_duyurular.py` | `duyurular/` sayfasını menüye ekler ve sayfanın kendi menü öğesini onarır |
| `10_temizlik.py` | Kaldırılan eklentilerin ölü etiketlerini ve WordPress uçlarını (feed, xmlrpc, wp-json, emoji, izleme kodları) siler |
| `11_seo.py` | Başlık/açıklama, canonical, Open Graph, Twitter, coğrafi meta, JSON-LD (ShoppingCenter, BreadcrumbList, FAQPage), `sitemap.xml`, `robots.txt` |
| `12_yasal.py` | KVKK aydınlatma metni, gizlilik ve çerez politikası, iletişim sayfasındaki işletme bilgileri |
| `13_kaldirilan_sayfalar.py` | Siteden çıkarılan sayfaları menülerden ve iç bağlantılardan (göreli **ve mutlak**) temizler |
| `14_harita.py` | Footer'daki mini harita görselini OpenStreetMap karolarından üretir (zincirde **ilk** çalışır) |

Yardımcılar (sunucu 8001'de açıkken):

- `kontrol.py` / `kontrol_hepsi.py` — kırık bağlantı taraması
- `tarayici_kontrol.py` — her sayfayı gerçek tarayıcı motorunda açar; JS hatası,
  kırık görsel ve menünün açılıp açılmadığını raporlar
- `ekran.py` — tam sayfa ekran görüntüsü
- `metin.py` — sayfanın görünen metnini dökümler
- `onizleme.py` — JS'siz (WebKit) hızlı önizleme

`tarayici_kontrol.py` ve `ekran.py`, Playwright'ın önbelleğindeki **headless Chromium**
ikilisini kullanır (`~/Library/Caches/ms-playwright/...`); kullanıcının Chrome
penceresine dokunmaz.

## Yönetim paneli

    http://localhost:8001/panel/          (yayında: <site>/panel)
    şifre: parkardesen2026

Üst çubuk: **Kaydet** (tarayıcıya — her düzenlemeden sonra kendiliğinden çalışır),
**Bağlantıyı test et** (jeton/depo sınaması), **Yayınla** (sunucuya, herkes için).

Genel Bakış'ta ilk girişte **7 adımlık panel eğitimi** açılır (ne kaydedilir, nerede
görünür, Kaydet ile Yayınla farkı, dört dil, yayın öncesi kontrol listesi). Kapatınca
`localStorage`'a yazılır; sayfanın altındaki düğmeyle tekrar açılabilir.

Panelden yönetilenler:

| Bölüm | Sitede nereye çıkar |
|---|---|
| **Duyurular** | Üst şerit (tüm sayfalar), anasayfa açılış penceresi, anasayfa duyuru bölümü, `duyurular/` sayfası |
| **Kampanyalar** | Anasayfa kampanya şeridi (öne çıkanlar) + `deals/` sayfası |
| **Fırsat Günleri** | `bargain-monday/` sayfası (metin + katılımcı mağazalar) |
| **Mağaza Kiralama** | `leasing/` sayfasındaki "Güncel boş birimler" listesi (yalnızca birim girilir; sayfanın kendi metni sabittir) |
| **Mağazalar** | `shops/` mağaza rehberi, `mall-map/` kat planı, kampanya/fırsat kartlarındaki logolar |

Duyuru türleri: çalışma saati, yeni mağaza açılışı, yakında açılıyor, etkinlik, çekiliş,
kampanya, yeni hizmet, bakım, ulaşım & otopark, sosyal sorumluluk, acil duyuru.
Her duyurunun tarih aralığı var; süresi dolan duyuru siteden kendiliğinden düşer.

Panel formları bilerek sade tutuldu:

- Ayrı bir "önem" alanı yok; şerit rengi türden türetiliyor (acil ve bakım
  kırmızı, diğerleri koyu).
- **"Nerede gösterilsin?"** üç küçük site maketiyle gösteriliyor — üst şerit,
  açılış penceresi, duyurular listesi. Metin okumadan da anlaşılıyor.
- Buton bağlantısı serbest metin değil, **site sayfalarından seçim**. Buton
  yazısı boş bırakılırsa sayfanın adı kullanılır.
- Her bölümün başında ne işe yaradığını anlatan kısa bir açıklama var.

### Veri akışı

`panel/veri.json` tek kaynak. Site `pa-veri.js` ile bu dosyayı **çalışma anında** okur ve
ilgili blokları çizer — içerik değişince sayfaların yeniden üretilmesi gerekmez.

Okuma sırası: `panel/veri.json` okunur, üzerine `localStorage['pa-veri']`
bindirilir — **panelde bulunan alanlar kazanır, panelde hiç olmayan alanlar
dosyadan gelir**. Bu birleştirme şart: siteye sonradan yeni bir alan
eklendiğinde (ör. `tesisler`) tarayıcıda duran eski kopyada o alan
bulunmadığı için içerik görünmez oluyor, üstelik ilk "Yayınla"da dosyadan
da siliniyordu. Aynı birleştirme panelde de yapılıyor.

`veri.json` içindeki **`veriSurumu`** alanı bu kuralın üstündedir: yayımlanan
sürüm tarayıcıdaki kopyadan yeniyse yerel kopya tamamen bırakılır ve dosya
kullanılır. İçeriği toplu değiştirmek/sıfırlamak için `veriSurumu` değerini
artırmak yeterli; ziyaretçilerin ve yöneticinin tarayıcısındaki eski kopya
kendiliğinden güncellenir. Panel de "Yayınla"da bu değeri artırır.

Panelde **Kaydet**'e basınca aynı tarayıcıdaki site anında güncellenir
(sunum için yeterli). **Yayınla**
düğmesi veriyi `/api/kaydet` uç noktasına gönderir; o da `panel/veri.json`'u GitHub'a
commit'ler ve Vercel dağıtımı (~1 dk) herkes için yayımlar.

### Yayınla için Vercel ayarı

Vercel → Settings → Environment Variables:

| Değişken | Değer |
|---|---|
| `PANEL_SIFRE` | panelin giriş şifresiyle **aynı** olmalı |
| `GITHUB_TOKEN` | depoya yazma yetkisi olan kişisel erişim jetonu |
| `GITHUB_REPO` | (isteğe bağlı) varsayılan `aktasevren/park-ardesen-avm` |
| `GITHUB_DAL` | (isteğe bağlı) varsayılan `main` |

Bu değişkenler tanımlanmadan da panel ve site tamamen çalışır; yalnızca "Yayınla"
düğmesi devre dışı kalır. Şifreyi değiştirmek için `panel/panel.js` içindeki `SIFRE`
sabitini ve `PANEL_SIFRE` değişkenini birlikte güncelleyin.

**Jeton nasıl üretilir**

- *Klasik jeton* — <https://github.com/settings/tokens/new> · kapsam: **`repo`**
- *İnce ayarlı jeton* — <https://github.com/settings/personal-access-tokens/new> ·
  Repository access: **Only select repositories → park-ardesen-avm** ·
  Permissions → Repository permissions → **Contents: Read and write**

Değişkeni her güncellediğinizde Vercel'de **Redeploy** gerekir; ortam değişkenleri
yalnızca yeni dağıtımlara uygulanır.

Panelde **Bağlantıyı test et** düğmesi, hiçbir şey yazmadan jetonu ve depo erişimini
sınar; sorun varsa ne yapılacağını söyler.

## Mağaza verisi

Mağazalar artık `panel/veri.json` içinde ve panelden yönetiliyor.
`pa-assets/magazalar.json` build sırasında (JS'siz gösterim için) kullanılan yedek kaynak
olarak duruyor; kalıcı değişiklikleri panelden yapın.

Marka listesi ve logoları `parkardesen.com/referanslar` sayfasından, Grand Bowling ile
V&K Prestij ise AVM dış cephe fotoğrafındaki tabelalardan alındı.
**Kat ve mağaza numaraları temsilidir.**

## SEO

`11_seo.py` içindeki **`SITE_URL`** sabiti canonical, Open Graph ve sitemap
adreslerini belirler. Kendi alan adına geçildiğinde **yalnızca bu satırı**
güncelleyip zinciri yeniden çalıştırmak yeterli:

    SITE_URL = "https://park-ardesen-avm.vercel.app"

Yapısal veri (schema.org `ShoppingCenter`) adres, koordinat, telefon, çalışma
saatleri ve hizmet verilen ilçeleri içerir. SSS sayfasındaki 12 soru `FAQPage`
olarak işaretlenir (Google'da zengin sonuç).

Koordinatlar yaklaşıktır (`41.190868, 40.987404` — Cumhuriyet Mah. merkezi);
kesin konum için Google Haritalar'dan alınan değerle `14_harita.py` → `KONUM` ve
`11_seo.py` → `ENLEM/BOYLAM` birlikte güncellenmeli.

## Kat planı şeması

`mall-map/` sayfasındaki izometrik kat şeması `pa-veri.js` içinde
(`katPlani3D`) **mağaza verisinden çizilir** — panelden mağaza eklenip
çıkarıldığında şema da kendiliğinden güncellenir. Blok renkleri kategoriye,
numaralar yandaki listeye karşılık gelir; kırmızı bant yürüyen merdivendir.
Yönlendirme amaçlı şematik bir çizimdir, mimari proje değildir; sayfadaki
not bunu belirtiyor.

Mağaza dışı birimler (AVM girişi, WC, danışma, mescit, asansör, ATM)
`panel/veri.json` içindeki **`tesisler`** dizisinde tutulur ve şemada
koridora yerleştirilir; giriş, ön cephenin dışına oka bağlı olarak çizilir.
Yeni birim eklemek için diziye `{"id","ad","tur","kat"}` eklemek yeterli
(`tur`: `giris` · `wc` · `danisma` · `mescit` · `asansor` · `atm`).
Bu bölümün panel arayüzü henüz yok; şimdilik JSON'dan düzenleniyor.

Kat adları panelde açılır listeden seçilir (Zemin Kat / 1. Kat / 2. Kat).
Eski kayıtlarda "1" gibi serbest yazımlar olabildiği için site tarafında
`katAdi()` ile normalleştirilir; aksi hâlde her yazım ayrı bir kat grubu
oluşturuyordu.

## Footer haritası

İki katmanlı:

- **Varsayılan** — derleme sırasında üretilmiş yerel bir harita görseli
  (`14_harita.py`, OpenStreetMap karolarından). Dış bağlantı gerektirmez,
  herkeste görünür, WebGL istemez. Tıklanınca Google Haritalar'da yol tarifi açılır.
- **Tercih çerezlerine izin verildiyse** — yerine etkileşimli **Google Haritalar**
  yüklenir (`pa-cerez.js`). Google gömme haritası çerez bırakıp ziyaretçinin
  IP'sini Google'a ilettiği için rızasız yüklenmiyor; çerez politikasında
  üçüncü taraf olarak listelenmiştir.

**Koordinat** `14_harita.py` içindeki `KONUM` sabitinde ve `11_seo.py` içindeki
`ENLEM/BOYLAM` değerlerinde tanımlı. Şu an Cumhuriyet Mahallesi merkezidir
(41.190868, 40.987404 — Nominatim). Binanın tam konumunu Google Haritalar'dan
alıp iki yeri de güncelleyin.

## Yasal

| Sayfa | İçerik |
|---|---|
| `gizlilik-politikasi/` | KVKK aydınlatma metni: veri sorumlusu, işlenen veriler, amaçlar ve hukuki sebepler, aktarım, saklama, KVKK m.11 hakları, başvuru usulü |
| `cerez-politikasi/` | Çerez kategorileri ve sitede kullanılan her kaydın tablosu (ad, amaç, süre, taraf) |
| `kullanim-kosullari/` | Sitenin kullanımı, içerik doğruluğu, kampanyalar, fikri mülkiyet |
| `contact-us/` | Resmî işletme bilgileri tablosu |

**Çerez rızası** (`pa-cerez.js`): Kabul et / Reddet / Ayarlar. Zorunlu dışındaki
kategoriler varsayılan olarak kapalı; rıza footer'daki "Çerez Ayarları"
bağlantısından geri alınabilir. Üçüncü taraf araç eklenirse
`window.paCerezIzni("olcumleme")` ile koşullandırın.

**İletişim formu** e-posta uygulamasını açar (arka uç yok, sahte "gönderildi"
mesajı yok) ve KVKK açık rıza kutusu içerir.

### ⚠️ Yayın öncesi doldurulması gerekenler

Metinlerde `[DOLDURULACAK]` olarak işaretli alanlar işletmenin resmî
bilgileridir ve uydurulamaz:

- Ticari unvan · Vergi dairesi ve numarası · MERSİS numarası · KEP adresi

Bunlar `_uyarla/12_yasal.py` başındaki sabitlerde tanımlı. Metinlerin yayına
alınmadan önce bir hukuk danışmanınca gözden geçirilmesi önerilir.

## Fontlar

- **Golos Text** — temanın kendi dosyaları kullanılıyor. Bu sürümde `gbreve`/`Gbreve`
  glifleri bozuktu (breve işareti yok, "mağaza" yerine "magaza" çiziyordu);
  `07_font_duzelt.py` eksik bileşeni ekliyor. Orijinaller `_orijinal/fonts/` altında.
- **linotype-didot** (başlıklar) — Adobe Typekit'ten geliyordu, Türkçe glifleri yok ve
  yerelde dış bağlantı gerektiriyordu. Yerine **Bodoni Moda** (Google Fonts, tam Türkçe,
  tek parça woff2) konuldu: `pa-assets/fonts/`.
- Tema başlıklarda `line-height:1` ve `.79` kullanıyor; Türkçe diyakritikler için
  `pa-avm.css` içinde açıldı.

## Tasarıma eklenenler

Orijinal temada menü yalnızca hamburger düğmesi ve içindeki çarpı ile kapanıyordu.
`pa-avm.js` menü açıkken sayfanın geri kalanına yarı saydam bir örtü (`.pa-menu-ortu`)
koyuyor: örtüye tıklamak veya <kbd>Esc</kbd> menüyü kapatıyor. Örtü olmadan "dışarı
tıklama" altta kalan bağlantıyı yanlışlıkla tetikleyebiliyordu.

Örtünün görünürlüğü CSS'teki `.nav-on` ataya bırakılmayıp JS'ten sürülüyor
(MutationObserver ile `<html>` sınıfı izleniyor); böylece davranış stil sırasından
bağımsız kalıyor.

## Klon artıkları (düzeltildi)

Kaynak site Cloudflare **Rocket Loader** kullanıyordu: tüm `<script>` etiketlerinin
`type`'ı `type="<hash>-text/javascript"` yapılmış, satır içi olay işleyicilerinin başına
`if (!window.__cfRLUnblockHandlers) return false;` eklenmişti. Bunları normalde
`rocket-loader.min.js` geri çeviriyordu; o dosya klonda yok. Sonuç: **hiçbir JS
çalışmıyordu** — menü açılmıyor, lazysizes devreye girmediği için harita ikonu ve
görseller boş kalıyordu. `08_cloudflare.py` bu izleri temizliyor.

Anasayfadaki "Ailenizle keyifli bir gün" kayan şeridi de bomboştu: slick karuseli
görselleri görüş alanının dışına taşıdığı için tembel yükleme hiç tetiklenmiyordu.
Şerit artık kendi fotoğraflarımızla, tembel yükleme olmadan doluyor.

## Orijinal klondan silinenler

Uyarlanmayan orijinal sayfaların tamamı depodan çıkarıldı: `shop/*` (13 mağaza
detayı), `deal/*` (8 kampanya detayı), `shops/page/2..12` (sayfalı listeler) ve
wget'in ürettiği ikinci ayna `_yedek-ayna/`. Depo 269 MB'tan 27 MB'a indi.

## Siteden çıkarılan sayfalar

Broşürler, Basında Biz, Medya Merkezi ve Çalışma Saatleri sayfaları
kaldırıldı. Bunlara giden bağlantılar `13_kaldirilan_sayfalar.py` tarafından
şu sayfalara yönlendirilir: Medya Merkezi → Mağazalar, Basında Biz →
Duyurular, Broşürler → Kat Planı, Çalışma Saatleri → İletişim (çalışma
saatleri kartı orada).

Menüden erişilen sayfaların tamamı uyarlandı; bunlar menüde yer almıyor.

## Depo ve dağıtım

Özel GitHub deposu: <https://github.com/aktasevren/park-ardesen-avm> (`main`)

`.gitignore` ile depo dışında bırakılanlar (diskte duruyorlar):

- `*.log` — `wget.log`, `serve.log`
- `**/wp-content/uploads/2023/08/Video-for-website-Final.mp4` — klondan gelen 34 MB'lık
  Dubai tanıtım videosu; hero artık Park Ardeşen fotoğrafı kullandığı için hiçbir
  sayfadan referans verilmiyor (iki aynada toplam 68 MB).

### Vercel

Statik site, build gerektirmez. Framework: **Other**, build komutu yok, output dizini
depo kökü. Site kökte olduğu için ek yönlendirme gerekmiyor.

`vercel.json`: `panel/veri.json` için `no-store` (yayımlanan içerik CDN'de takılmasın),
`/panel` kısayolu ve panel için `X-Robots-Tag: noindex`.

Commit yazarının e-postası GitHub hesabına bağlı olmalı; aksi hâlde Vercel dağıtımı
reddediyor. Bu depoda `evrenaktas@yahoo.com` kullanılıyor.

## Dört dilli yayın

Site Türkçe (varsayılan), İngilizce, Gürcüce ve Arapça yayımlanır:

    /               → Türkçe
    /en/            → English
    /ka/            → ქართული
    /ar/            → العربية   (sağdan sola)

Dil sürümleri derleme zincirinin **son adımında** üretilir:

    bash _uyarla/tumunu_calistir.sh     # … → _dil/cikar.py → _dil/uret.py

`en/`, `ka/`, `ar/` klasörleri üretilen çıktıdır; elle düzenlenmez. Türkçe
sayfayı ya da `_dil/sozluk.json`'u düzeltip zinciri yeniden çalıştırın.
Ara adımlar sayfaları yeniden ürettiği için dil klasörleri tüm `_uyarla`
betiklerinin `HARIC` listesindedir.

### İki katman

1. **Statik metinler** — sayfa gövdesi, başlıklar, meta etiketler ve
   `alt`/`aria-label` gibi öznitelikler derleme sırasında `_dil/sozluk.json`
   üzerinden çevrilir.
2. **Çalışma anında üretilen metinler** — `pa-assets/pa-dil.js`. Ay adları,
   kat adları, tesis etiketleri, kiralama durumları, duyuru türleri, çerez
   bandı ve boş durum mesajları buradaki sözlükten çevrilir. Sayfaya sonradan
   eklenen bileşenler bir MutationObserver ile yakalanır.
   `paT(metin)` arayüz metnini, `paMetin(deger)` panel içeriğini çözer.

### Panel içeriği

Panelde kampanya/duyuru/kiralama metin alanlarında **TR · EN · KA · AR**
sekmeleri vardır. Boş bırakılan dil sitede Türkçesini gösterir. Yalnızca
Türkçe doldurulmuşsa veri düz metin olarak saklanır; böylece `veri.json`
gereksiz yere şişmez. Eski (tek dilli) kayıtlar olduğu gibi çalışmaya devam
eder.

### Dil seçici

Başlığın sağ bölümünde (`.site-header-right`) yuvarlak bayraklı düğme;
Arapçada sola geçer. Bayraklar satır içi SVG'dir — dış istek yoktur.

### SEO

`sitemap.xml` 68 adres içerir (17 sayfa × 4 dil) ve her adres tüm dillere
`xhtml:link hreflang` bağlantısı taşır. Sayfalara `hreflang` ve dil başına
`canonical` etiketi konur.

### Yazı tipleri

Gürcüce ve Arapça için Noto Sans Georgian / Noto Sans Arabic yerel olarak
barındırılır (`pa-assets/yazitipi/`, ~200 KB) ve yalnızca ilgili dilde yüklenir.
Site hiçbir dilde dış sunucuya istek atmaz.

---

## Yapılan işin özeti (kronolojik)

Bu bölüm, siteyi devralan geliştirici için "ne yapıldı, neden yapıldı" kaydıdır.

### 1. Klonun çalışır hâle getirilmesi

Kaynak site Cloudflare Rocket Loader kullanıyordu; klonda `rocket-loader.min.js`
olmadığı için **hiçbir JS çalışmıyordu**. `08_cloudflare.py` bu izleri temizledi.
Ardından WordPress/eklenti artıkları (WooCommerce, Gravity Forms, Mapplic,
Insta Gallery, WP Job Openings, cookie-notice), feed/xmlrpc/wp-json/oEmbed/emoji
uçları ve üçüncü taraf izleme kodları (Google Tag Manager, Analytics) `10_temizlik.py`
ile kaldırıldı. **Site hiçbir dilde hiçbir dış sunucuya istek atmıyor.**

### 2. İçeriğin Türkçeleştirilmesi ve AVM'ye uyarlanması

Tüm sayfa metinleri, menüler, meta etiketler ve `alt`/`aria-label` öznitelikleri
Türkçeleştirildi; Dubai'ye özgü içerik (para birimi, mağaza listesi, kampanyalar,
turizm bilgisi, kiralama portalı) Park Ardeşen verisiyle değiştirildi. Bozuk
`ğ/Ğ` glifleri font dosyasında onarıldı (`07_font_duzelt.py`); Türkçe glifi olmayan
başlık fontu (Adobe Typekit `linotype-didot`) yerine **Bodoni Moda** yerel olarak
barındırıldı.

### 3. Yönetim paneli

`panel/` — bağımlılıksız, tek sayfalık bir yönetim arayüzü. İçerik `panel/veri.json`
dosyasında tutulur, site `pa-veri.js` ile bunu çalışma anında okur. `api/kaydet.js`
(Vercel serverless) panelden gelen JSON'u GitHub'a commit'ler; Vercel dağıtımı
tetiklenir.

### 4. Yasal metinler ve çerez rızası

KVKK aydınlatma metni, çerez politikası (kayıt tablosuyla), kullanım koşulları ve
resmî işletme bilgileri tablosu yazıldı. Kabul/Reddet/Ayarlar sunan kendi rıza
bandımız (`pa-cerez.js`) konuldu; Google Haritalar yalnızca tercih çerezlerine izin
verilirse yükleniyor.

### 5. Dört dilli yayın

Türkçe (varsayılan), İngilizce, Gürcüce, Arapça. Statik metinler derleme sırasında
`_dil/sozluk.json` üzerinden, çalışma anında üretilen metinler `pa-dil.js` üzerinden
çevrilir. Arapça için tam RTL (`dir="rtl"`) düzen; Gürcüce ve Arapça yazı tipleri
yerel olarak barındırılır. `sitemap.xml` 68 adres ve `hreflang` bağlantıları taşır.
Panel metin alanlarına TR/EN/KA/AR sekmeleri eklendi.

### 6. Son temizlik turu

- İletişim sayfasındaki **"Mağazalar"** kartı ve Hakkımızda'daki galeri düğmesi hâlâ
  `dubaioutletmall.com/media-center/` adresine gidiyordu. Kök neden:
  `06_baglantilar.py` hedef dosya yoksa mutlak adresi olduğu gibi bırakıyordu.
  `13_kaldirilan_sayfalar.py` artık kaldırılmış sayfaların mutlak adreslerini de
  yönlendiriyor.
- Duyurular sayfası `press/` klonundan geldiği için menüsünde **"Basında Biz"**
  etiketli, çift kayıt oluşturan bir öğe kalmıştı; silindi ve "bulunulan sayfa"
  işareti doğru öğeye taşındı.
- Kaldırılan rıza eklentisinden kalan boş yorum çifti ve işlevsiz `gmpg.org`
  XFN bağlantısı temizlendi.
- `10_temizlik.py` içindeki birebir kopyalanmış desen bloğu tekilleştirildi.

### 7. Arayüz düzeltmeleri (son tur)

| Ne | Neden |
|---|---|
| **WhatsApp bağlantısı kaldırıldı** (başlık + altbilgi, tüm diller) | İstenmedi. Kalan sosyal ağlar: Facebook, Instagram |
| **Anasayfa marka şeridinde isimler kaldırıldı** | Logonun altına adını bir daha yazmak tekrardı. Erişilebilir ad logonun `alt` metninden geliyor |
| **Açılış penceresinin kapatma düğmesi** | `&times;` karakteri tema yazı tipinde ufak ve kaçık duruyordu; yerine flex ile ortalanmış, çizilmiş bir X ikonu |
| **Panele 7 adımlık eğitim** | Panel devredilirken "önce ne yapmalı" sorusunu karşılıyor |
| **"Siteyi önizle" düğmesi kaldırıldı** | Üst çubuğu kalabalıklaştırıyordu; adresler zaten Genel Bakış'ta yazılı |
| **Fırsat Günleri yayın anahtarı** | İçerik girilip bölüm kapalıyken sayfada "yayında değil" notu çıkıyor, sebebi anlaşılmıyordu. Artık anahtar formun başında; içerik varken kapalıysa tek tıkla "Yayına al" öneren bir uyarı çıkıyor |
| **Mağaza Kiralama'da "Sayfa metni" kartı kaldırıldı** | Yalnızca birim girilmesi isteniyordu; kullanılmayan `girisMetni`/`iletisimAd` alanları da verisiyle birlikte silindi |

## Doğrulama

Her değişiklikten sonra çalıştırılanlar:

    python3 _uyarla/kontrol_hepsi.py      # kırık bağlantı taraması
    ./_uyarla/tumunu_calistir.sh          # iki kez → çıktı bit bit aynı olmalı

Ayrıca 68 sayfanın (17 × 4 dil) tamamı headless Chromium'da açılıp konsol hatası,
başarısız istek ve **dış istek** yönünden tarandı.

Son durum: **68/68 sayfa temiz · 1195 referans, 0 kırık bağlantı · dış istek yok ·
zincir idempotan**.
