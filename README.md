# Park Ardeşen AVM — web sitesi

Park Ardeşen Alışveriş ve Yaşam Merkezi (YB Global Group) için hazırlanan statik site.
Tasarım, `dubaioutletmall.com` klonundan birebir korunarak Türkçeleştirildi ve AVM'ye uyarlandı.

## Yerel çalıştırma

    python3 serve.py 8001
    # http://localhost:8001/

Kök dizin `www.dubaioutletmall.com/index.html`'e yönlendirir.

## Yapı

| Yol | Ne |
|---|---|
| `www.dubaioutletmall.com/` | Ana ayna — **uyarlanmış site burası** |
| `dubaioutletmall.com/` | wget'in ürettiği ikinci ayna (aynı uyarlamalar burada da uygulanır); `privacy-policy-2/` ve `terms-and-conditions/` yalnızca burada |
| `pa-assets/` | Park Ardeşen'e ait varlıkların **kaynağı**: logo, mağaza logoları, fotoğraflar, `magazalar.json`, `pa-avm.css`, `pa-avm.js`, fontlar |
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

## Mağaza verisi

`pa-assets/magazalar.json` tek kaynak. Mağaza eklemek/çıkarmak için bu dosyayı düzenleyip
`03_magazalar.py`, `02_anasayfa.py` ve `04_sayfalar.py`'yi yeniden çalıştırın.

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
- `dubaioutletmall.com/images/`, `videos/` — wget'in indirdiği anasayfa kopyaları

Menüden erişilen sayfaların tamamı uyarlandı; bunlar menüde yer almıyor.

## Vercel

Statik site, build gerektirmez.
