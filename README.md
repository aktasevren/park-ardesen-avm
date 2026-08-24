# Park Ardeşen AVM — web sitesi

Park Ardeşen Alışveriş ve Yaşam Merkezi (YB Global Group) için hazırlanan statik site.
Tasarım, `dubaioutletmall.com` klonundan birebir korunarak Türkçeleştirildi ve AVM'ye uyarlandı.

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
| `_yedek-ayna/` | wget'in ürettiği ikinci (kopya) ayna — dağıtıma girmez, yalnızca yedek |
| `pa-assets/` | Park Ardeşen'e ait varlıkların **kaynağı**: logo, mağaza logoları, fotoğraflar, `pa-avm.css`, `pa-avm.js`, `pa-veri.js`, fontlar |
| `panel/` | Yönetim paneli + `veri.json` (site içeriğinin tek kaynağı) |
| `api/` | Vercel serverless fonksiyonu (`kaydet.js` — panelden gelen veriyi GitHub'a commit'ler) |
| `_uyarla/` | Uyarlama betikleri (aşağıya bakın) |
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
| `03_magazalar.py` | Mağaza rehberi (17 mağaza) ve kat planı |
| `04_sayfalar.py` | Hakkımızda, Hizmetlerimiz, İletişim, SSS, Kiralama, Kariyer, Broşürler, Ulaşım, Fırsat Günleri, Park Kart, Basın, Medya, Kampanyalar + ortak bloklar |
| `05_ek_sayfalar.py` | Gizlilik, Kullanım Koşulları, Medya Merkezi galerisi, Çalışma Saatleri |
| `06_baglantilar.py` | Kalan mutlak `dubaioutletmall.com` adreslerini yerel göreli yollara çevirir |
| `07_font_duzelt.py` | Golos Text'in bozuk `ğ/Ğ` gliflerini onarır |
| `08_cloudflare.py` | Cloudflare Rocket Loader izlerini ve ölü eklenti dosyalarını temizler (zincirde **ilk** çalışır) |
| `09_duyurular.py` | `duyurular/` sayfasını üretir ve menüye ekler |

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

Üst çubuk: **Kaydet** (tarayıcıya — otomatik çalışır), **Siteyi önizle**,
**Bağlantıyı test et** (jeton/depo sınaması), **Yayınla** (sunucuya).

Panelden yönetilenler:

| Bölüm | Sitede nereye çıkar |
|---|---|
| **Duyurular** | Üst şerit (tüm sayfalar), anasayfa açılış penceresi, anasayfa duyuru bölümü, `duyurular/` sayfası |
| **Kampanyalar** | Anasayfa kampanya şeridi (öne çıkanlar) + `deals/` sayfası |
| **Fırsat Günleri** | `bargain-monday/` sayfası (metin + katılımcı mağazalar) |
| **Mağaza Kiralama** | `leasing/` sayfasındaki "Güncel boş birimler" listesi |
| **Mağazalar** | `shops/` mağaza rehberi, `mall-map/` kat planı, kampanya/fırsat kartlarındaki logolar |

Duyuru türleri: çalışma saati, yeni mağaza açılışı, yakında açılıyor, etkinlik, çekiliş,
kampanya, yeni hizmet, bakım, ulaşım & otopark, sosyal sorumluluk, acil duyuru.
Her duyurunun tarih aralığı var; süresi dolan duyuru siteden kendiliğinden düşer.

### Veri akışı

`panel/veri.json` tek kaynak. Site `pa-veri.js` ile bu dosyayı **çalışma anında** okur ve
ilgili blokları çizer — içerik değişince sayfaların yeniden üretilmesi gerekmez.

Okuma sırası: `localStorage['pa-veri']` → `panel/veri.json`. Yani panelde **Kaydet**'e
basınca aynı tarayıcıdaki site anında güncellenir (sunum için yeterli). **Yayınla**
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

## Bilinçli olarak dokunulmayanlar

Kullanıcı isteğiyle uyarlanamayan orijinal sayfalar **silinmedi**:

- `shop/*` — Dubai Outlet Mall mağaza detay sayfaları (13 adet)
- `deal/*` — orijinal kampanya detay sayfaları (8 adet)
- `shops/page/2..12` — orijinal sayfalı mağaza listeleri
- `_yedek-ayna/` — wget'in ürettiği ikinci aynanın tamamı (dağıtıma girmez)

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
