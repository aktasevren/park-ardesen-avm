/* ------------------------------------------------------------------
   Park Ardeşen AVM — yönetim paneli

   Tek sayfa, bağımlılıksız. Veriyi panel/veri.json'dan okur; düzenlemeler
   önce tarayıcıya (localStorage) yazılır — site aynı tarayıcıda anında
   günceldir. "Yayınla" düğmesi veriyi /api/kaydet uç noktasına gönderir;
   o da GitHub'a commit'leyip Vercel dağıtımını tetikler.
   ------------------------------------------------------------------ */
(function () {
  "use strict";

  var SIFRE = "parkardesen2026";      // panel giriş şifresi
  var girilenSifre = "";              // yayınlarken sunucuya gönderilen
  var ANAHTAR = "pa-veri";            // site ile ortak localStorage anahtarı
  var API = "/api/kaydet";

  var veri = null;
  var kirli = false;
  var aktif = "ozet";
  var duzenlenen = null;              // { bolum, id, yeni }

  /* ---------------------------------------------------------- yardımcı */
  function $(s, k) { return (k || document).querySelector(s); }
  function $$(s, k) { return [].slice.call((k || document).querySelectorAll(s)); }
  function kacis(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function yeniId(on) { return on + "-" + Math.random().toString(36).slice(2, 8); }
  function bugun() { return new Date().toISOString().slice(0, 10); }

  var AYLAR = ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos",
               "Eylül","Ekim","Kasım","Aralık"];
  function tarihYaz(g) {
    if (!g) return "—";
    var p = String(g).split("-");
    return p.length === 3 ? Number(p[2]) + " " + AYLAR[Number(p[1]) - 1] + " " + p[0] : g;
  }

  function bildir(mesaj, tip) {
    var b = $("#bildirim");
    b.textContent = mesaj;
    b.className = "bildirim acik " + (tip || "");
    clearTimeout(bildir._z);
    bildir._z = setTimeout(function () { b.className = "bildirim " + (tip || ""); }, 3800);
  }

  var TURLER = {
    saat:     "🕒 Çalışma saati",
    acilis:   "🎉 Yeni mağaza açılışı",
    yakinda:  "🚧 Yakında açılıyor",
    etkinlik: "🎈 Etkinlik",
    cekilis:  "🎁 Çekiliş / hediye",
    kampanya: "🏷️ Kampanya duyurusu",
    hizmet:   "✨ Yeni hizmet",
    bakim:    "🛠️ Bakım / geçici kapanış",
    ulasim:   "🅿️ Ulaşım & otopark",
    sosyal:   "❤️ Sosyal sorumluluk",
    acil:     "⚠️ Acil duyuru"
  };
  var ONEMLER = { normal: "Normal", onemli: "Önemli", acil: "Acil" };
  var YERLER = {
    "ust-serit": "Üst şerit (tüm sayfalar)",
    "acilis-penceresi": "Açılış penceresi (anasayfa)",
    "duyurular": "Duyurular listesi"
  };
  var DURUMLAR = { bos: "Boş", rezerve: "Rezerve", dolu: "Dolu" };

  var BOLUMLER = [
    { id: "ozet",       ad: "Genel Bakış",     ikon: "📊" },
    { id: "duyurular",  ad: "Duyurular",       ikon: "📢" },
    { id: "kampanyalar",ad: "Kampanyalar",     ikon: "🏷️" },
    { id: "firsat",     ad: "Fırsat Günleri",  ikon: "⭐" },
    { id: "kiralama",   ad: "Mağaza Kiralama", ikon: "🏬" },
    { id: "magazalar",  ad: "Mağazalar",       ikon: "🛍️" }
  ];

  /* ---------------------------------------------------------- durum */
  function magazaAdi(slug) {
    var m = (veri.magazalar || []).filter(function (x) { return x.slug === slug; })[0];
    return m ? m.ad : slug;
  }
  function magaza(slug) {
    return (veri.magazalar || []).filter(function (x) { return x.slug === slug; })[0];
  }

  function yayinDurumu(o) {
    if (o.yayinda === false) return { sinif: "kapali", ad: "Kapalı" };
    var b = bugun();
    if (o.baslangic && o.baslangic > b) return { sinif: "bekliyor", ad: "Bekliyor" };
    if (o.bitis && o.bitis < b) return { sinif: "gecti", ad: "Süresi doldu" };
    return { sinif: "yayinda", ad: "Yayında" };
  }

  function kirlet() {
    kirli = true;
    $("#durum").textContent = "Kaydedilmedi";
    $("#durum").classList.add("kirli");
  }

  /* Değişiklikler kendiliğinden kaydedilsin: "Tamam" dedikten sonra ayrıca
     "Kaydet"e basmayı beklemek, değişikliğin sitede görünmemesine yol
     açıyordu. Kaydet düğmesi yine duruyor (elle yedekleme/güven için). */
  function otoKaydet() { kirlet(); kaydet(true); }

  function kaydet(sessiz) {
    veri.guncelleme = new Date().toISOString();
    try {
      localStorage.setItem(ANAHTAR, JSON.stringify(veri));
    } catch (e) {
      bildir("Tarayıcıya kaydedilemedi: " + e.message, "hata");
      return false;
    }
    kirli = false;
    $("#durum").textContent = "Kaydedildi";
    $("#durum").classList.remove("kirli");
    $("#son-kayit").textContent = "Son kayıt: " +
      new Date(veri.guncelleme).toLocaleString("tr-TR");
    if (!sessiz) bildir("Değişiklikler tarayıcıya kaydedildi. Site anında güncel.", "basarili");
    return true;
  }

  /* ---------------------------------------------------------- form parçaları */
  function metinAlani(ad, etiket, deger, genis, ipucu) {
    return '<div class="alan' + (genis ? " genis" : "") + '"><label>' + kacis(etiket) +
      '</label><input data-a="' + ad + '" value="' + kacis(deger || "") + '">' +
      (ipucu ? '<span class="ipucu">' + kacis(ipucu) + "</span>" : "") + "</div>";
  }
  function sayiAlani(ad, etiket, deger) {
    return '<div class="alan"><label>' + kacis(etiket) +
      '</label><input type="number" data-a="' + ad + '" value="' + kacis(deger || "") + '"></div>';
  }
  function tarihAlani(ad, etiket, deger) {
    return '<div class="alan"><label>' + kacis(etiket) +
      '</label><input type="date" data-a="' + ad + '" value="' + kacis(deger || "") + '"></div>';
  }
  function yaziAlani(ad, etiket, deger) {
    return '<div class="alan genis"><label>' + kacis(etiket) +
      '</label><textarea data-a="' + ad + '">' + kacis(deger || "") + "</textarea></div>";
  }
  function secim(ad, etiket, deger, secenekler, genis) {
    var o = Object.keys(secenekler).map(function (k) {
      return '<option value="' + kacis(k) + '"' + (k === deger ? " selected" : "") + ">" +
        kacis(secenekler[k]) + "</option>";
    }).join("");
    return '<div class="alan' + (genis ? " genis" : "") + '"><label>' + kacis(etiket) +
      '</label><select data-a="' + ad + '">' + o + "</select></div>";
  }
  function onay(ad, etiket, deger) {
    return '<div class="alan"><label>&nbsp;</label><label class="kutucuk">' +
      '<input type="checkbox" data-a="' + ad + '"' + (deger ? " checked" : "") + "> " +
      kacis(etiket) + "</label></div>";
  }
  function cokluSecim(ad, etiket, secili, secenekler) {
    secili = secili || [];
    var k = Object.keys(secenekler).map(function (v) {
      return '<label class="kutucuk"><input type="checkbox" data-c="' + ad +
        '" value="' + kacis(v) + '"' + (secili.indexOf(v) >= 0 ? " checked" : "") + "> " +
        kacis(secenekler[v]) + "</label>";
    }).join("");
    return '<div class="alan genis"><label>' + kacis(etiket) +
      '</label><div class="kutucuklar">' + k + "</div></div>";
  }
  function magazaSecimi(ad, etiket, deger) {
    var s = {};
    (veri.magazalar || []).forEach(function (m) { s[m.slug] = m.ad; });
    return secim(ad, etiket, deger, s);
  }
  function logoOnizleme(m) {
    if (m && m.logo) {
      return '<span class="logo"><img src="/pa-assets/markalar/' + kacis(m.logo) + '" alt=""></span>';
    }
    return '<span class="logo"><span>' + kacis(m ? m.ad : "?") + "</span></span>";
  }

  /* formdaki değerleri nesneye yaz */
  function formuOku(kok, hedef) {
    $$("[data-a]", kok).forEach(function (el) {
      var ad = el.getAttribute("data-a");
      if (el.type === "checkbox") hedef[ad] = el.checked;
      else if (el.type === "number") hedef[ad] = el.value === "" ? "" : Number(el.value);
      else hedef[ad] = el.value;
    });
    var gruplar = {};
    $$("[data-c]", kok).forEach(function (el) {
      var ad = el.getAttribute("data-c");
      (gruplar[ad] = gruplar[ad] || []);
      if (el.checked) gruplar[ad].push(el.value);
    });
    Object.keys(gruplar).forEach(function (ad) { hedef[ad] = gruplar[ad]; });
    return hedef;
  }

  /* ---------------------------------------------------------- liste kabuğu */
  function kartKabugu(baslik, rozet, icerik, islemler) {
    return '<div class="kutu"><div class="kutu-ust"><h3>' + baslik + "</h3>" +
      (rozet || "") + '<div class="islem">' + (islemler || "") + "</div></div>" +
      icerik + "</div>";
  }

  function duzenleDugmeleri(bolum, id) {
    return '<button class="dugme kucuk" data-duzenle="' + bolum + "|" + id + '">Düzenle</button>' +
      '<button class="dugme kucuk tehlike" data-sil="' + bolum + "|" + id + '">Sil</button>';
  }
  function formDugmeleri() {
    return '<button class="dugme ana kucuk" data-tamam>Tamam</button>' +
      '<button class="dugme kucuk" data-iptal>İptal</button>';
  }

  /* ============================================================ bölümler */

  function ciz_ozet() {
    var d = (veri.duyurular || []).filter(function (x) { return yayinDurumu(x).sinif === "yayinda"; });
    var k = (veri.kampanyalar || []).filter(function (x) { return yayinDurumu(x).sinif === "yayinda"; });
    var b = ((veri.kiralama || {}).birimler || []).filter(function (x) {
      return x.yayinda !== false && x.durum === "bos"; });
    var kutu = function (sayi, etiket) {
      return '<div class="kutu"><div class="sayi">' + sayi + '</div><div class="etiket">' +
        etiket + "</div></div>"; };
    return '<div class="ozet">' +
      kutu(d.length, "Yayındaki duyuru") +
      kutu(k.length, "Yayındaki kampanya") +
      kutu((veri.magazalar || []).length, "Mağaza") +
      kutu(b.length, "Boş kiralık birim") +
      "</div>" +
      kartKabugu("Kaydet ile Yayınla arasındaki fark", "",
        "<p><strong>Kaydet</strong> — değişikliği <em>bu tarayıcıya</em> yazar. " +
        "Siteyi aynı tarayıcıda açtığınızda anında görürsünüz. Her düzenlemeden " +
        "sonra kendiliğinden çalışır. Sunum için tek gereken budur.</p>" +
        "<p><strong>Yayınla</strong> — aynı veriyi <em>sunucuya</em> gönderir, " +
        "böylece siteyi açan <em>herkes</em> görür: başka bilgisayarlar, telefonlar, " +
        "müşteriler. Veri depoya kaydedilir ve site ~1 dakika içinde yeniden " +
        "yayımlanır.</p>" +
        "<p class=\"ipucu\">Yani &ldquo;kaydettim, sitede görüyorum ama Yayınla hata " +
        "verdi&rdquo; durumunda değişiklik gerçektir &mdash; ama yalnızca sizin " +
        "tarayıcınızdadır. Başkaları henüz göremez.</p>" +
        "<p><strong>JSON indir / yükle</strong> ile veriyi yedekleyebilir ya da " +
        "başka bir bilgisayara taşıyabilirsiniz.</p>", "") +
      kartKabugu("Adresler", "",
        '<div class="satir"><div class="govde"><strong>Panel</strong><small>' +
          kacis(location.origin + location.pathname.replace(/[^/]*$/, "")) + "</small></div></div>" +
        '<div class="satir"><div class="govde"><strong>Site</strong><small>' +
          kacis(location.origin + "/") +
          "</small></div></div>" +
        '<p class="ipucu" style="margin-top:12px">Tarayıcıya kaydedilen değişiklikler ' +
        '<strong>yalnızca aynı adres</strong> üzerinde görünür. Siteyi ' +
        '<code>localhost</code> ile açtıysanız paneli de <code>localhost</code> ile açın ' +
        '(<code>127.0.0.1</code> ile karıştırmayın). En güvenlisi yukarıdaki ' +
        '<strong>Siteyi önizle</strong> düğmesini kullanmaktır.</p>', "") +
      kartKabugu("Son değişiklikler", "",
        '<div class="satir"><div class="govde"><strong>Son kayıt</strong>' +
        "<small>" + (veri.guncelleme
          ? new Date(veri.guncelleme).toLocaleString("tr-TR") : "—") + "</small></div></div>", "");
  }

  function ciz_duyurular() {
    var liste = veri.duyurular || [];
    var html = '<div style="margin-bottom:16px"><button class="dugme ana" data-ekle="duyurular">+ Yeni duyuru</button></div>';
    if (!liste.length) html += '<div class="kutu bos">Henüz duyuru yok.</div>';
    liste.forEach(function (d) {
      var s = yayinDurumu(d);
      var rozet = '<span class="rozet ' + s.sinif + '">' + s.ad + "</span>";
      if (duzenlenen && duzenlenen.bolum === "duyurular" && duzenlenen.id === d.id) {
        html += kartKabugu("Duyuru düzenle", rozet,
          '<div class="alanlar" data-form>' +
            secim("tur", "Tür", d.tur, TURLER) +
            secim("onem", "Önem", d.onem, ONEMLER) +
            onay("yayinda", "Yayında", d.yayinda !== false) +
            metinAlani("baslik", "Başlık", d.baslik, true) +
            yaziAlani("metin", "Metin", d.metin) +
            tarihAlani("baslangic", "Başlangıç") .replace('value=""', 'value="' + kacis(d.baslangic || "") + '"') +
            tarihAlani("bitis", "Bitiş").replace('value=""', 'value="' + kacis(d.bitis || "") + '"') +
            cokluSecim("yerler", "Nerede gösterilsin?", d.yerler, YERLER) +
            metinAlani("bagLabel", "Buton yazısı", d.bagLabel, false, "Boş bırakılırsa buton çıkmaz") +
            metinAlani("bagUrl", "Buton bağlantısı", d.bagUrl, false, "Örn. shops/ veya duyurular/") +
            secim("gorsel", "Görsel (açılış penceresi için)", d.gorsel || "",
                  gorselSecenekleri(), true) +
          "</div>", formDugmeleri());
      } else {
        html += kartKabugu(kacis(d.baslik || "(başlıksız)"), rozet,
          '<div class="satir"><div class="govde">' +
            "<small>" + kacis(TURLER[d.tur] || d.tur) + " &middot; " +
            kacis(ONEMLER[d.onem] || "Normal") + " &middot; " +
            tarihYaz(d.baslangic) + " – " + tarihYaz(d.bitis) + "</small>" +
            "<small>" + (d.yerler || []).map(function (y) { return YERLER[y] || y; }).join(", ") +
            "</small></div></div>" +
          "<p>" + kacis(d.metin || "") + "</p>",
          duzenleDugmeleri("duyurular", d.id));
      }
    });
    return html;
  }

  function gorselSecenekleri() {
    var s = { "": "— görselsiz —" };
    (veri.gorseller || []).forEach(function (g) { s[g] = g.split("/").pop(); });
    return s;
  }

  function ciz_kampanyalar() {
    var liste = veri.kampanyalar || [];
    var html = '<div style="margin-bottom:16px"><button class="dugme ana" data-ekle="kampanyalar">+ Yeni kampanya</button></div>';
    if (!liste.length) html += '<div class="kutu bos">Henüz kampanya yok.</div>';
    liste.forEach(function (k) {
      var s = yayinDurumu(k), m = magaza(k.magaza);
      var rozet = '<span class="rozet ' + s.sinif + '">' + s.ad + "</span>" +
        (k.oneCikar ? ' <span class="rozet">Anasayfada</span>' : "");
      if (duzenlenen && duzenlenen.bolum === "kampanyalar" && duzenlenen.id === k.id) {
        html += kartKabugu("Kampanya düzenle", rozet,
          '<div class="alanlar" data-form>' +
            magazaSecimi("magaza", "Mağaza", k.magaza) +
            onay("yayinda", "Yayında", k.yayinda !== false) +
            onay("oneCikar", "Anasayfada öne çıkar", !!k.oneCikar) +
            metinAlani("baslik", "Kampanya başlığı", k.baslik, true,
                       "Örn. Sezon sonunda %50'ye varan indirim") +
            yaziAlani("aciklama", "Açıklama", k.aciklama) +
            tarihAlani("baslangic", "Başlangıç").replace('value=""', 'value="' + kacis(k.baslangic || "") + '"') +
            tarihAlani("bitis", "Bitiş").replace('value=""', 'value="' + kacis(k.bitis || "") + '"') +
            '<div class="alan genis"><span class="ipucu">Bitiş boş bırakılırsa kampanya ' +
            'süresiz yayında kalır. Anasayfada en fazla 8 kampanya gösterilir; ' +
            'önce &ldquo;öne çıkar&rdquo; işaretliler sıralanır.</span></div>' +
          "</div>", formDugmeleri());
      } else {
        html += kartKabugu(kacis(k.baslik || "(başlıksız)"), rozet,
          '<div class="satir">' + logoOnizleme(m) +
          '<div class="govde"><strong>' + kacis(magazaAdi(k.magaza)) + "</strong>" +
          "<small>" + tarihYaz(k.baslangic) + " – " + tarihYaz(k.bitis) + "</small>" +
          (k.aciklama ? "<small>" + kacis(k.aciklama) + "</small>" : "") +
          "</div></div>", duzenleDugmeleri("kampanyalar", k.id));
      }
    });
    return html;
  }

  function ciz_firsat() {
    var f = veri.firsatGunleri = veri.firsatGunleri || { katilimcilar: [] };
    var html = kartKabugu("Fırsat Günleri ayarları",
      '<span class="rozet ' + (f.yayinda === false ? "kapali" : "yayinda") + '">' +
        (f.yayinda === false ? "Kapalı" : "Yayında") + "</span>",
      '<div class="alanlar" data-form-firsat>' +
        metinAlani("baslik", "Başlık", f.baslik) +
        metinAlani("donem", "Dönem", f.donem, false, "Örn. Her ayın ilk haftası") +
        onay("yayinda", "Yayında", f.yayinda !== false) +
        yaziAlani("aciklama", "Açıklama", f.aciklama) +
      "</div>" +
      '<div style="margin-top:10px"><button class="dugme ana kucuk" data-firsat-kaydet>Ayarları uygula</button></div>', "");

    html += '<div style="margin:20px 0 14px"><button class="dugme ana" data-ekle="katilimci">+ Katılımcı mağaza ekle</button></div>';
    (f.katilimcilar || []).forEach(function (k, i) {
      var m = magaza(k.magaza);
      if (duzenlenen && duzenlenen.bolum === "katilimci" && duzenlenen.id === String(i)) {
        html += kartKabugu("Katılımcı düzenle", "",
          '<div class="alanlar" data-form>' +
            magazaSecimi("magaza", "Mağaza", k.magaza) +
            metinAlani("teklif", "Fırsat", k.teklif, true, "Örn. Sepette ek %20 indirim") +
          "</div>", formDugmeleri());
      } else {
        html += kartKabugu(kacis(magazaAdi(k.magaza)), "",
          '<div class="satir">' + logoOnizleme(m) +
          '<div class="govde"><strong>' + kacis(k.teklif || "") + "</strong></div></div>",
          duzenleDugmeleri("katilimci", String(i)));
      }
    });
    return html;
  }

  function ciz_kiralama() {
    var kr = veri.kiralama = veri.kiralama || { birimler: [] };
    var html = kartKabugu("Sayfa metni", "",
      '<div class="alanlar" data-form-kiralama>' +
        yaziAlani("girisMetni", "Giriş metni", kr.girisMetni) +
        metinAlani("iletisimAd", "İletişim kişisi / ekip", kr.iletisimAd, true) +
      "</div>" +
      '<div style="margin-top:10px"><button class="dugme ana kucuk" data-kiralama-kaydet>Metni uygula</button></div>', "");

    html += '<div style="margin:20px 0 14px"><button class="dugme ana" data-ekle="birim">+ Yeni birim</button></div>';
    (kr.birimler || []).forEach(function (b) {
      var rozet = '<span class="rozet ' + (b.yayinda === false ? "kapali" :
        b.durum === "bos" ? "yayinda" : b.durum === "rezerve" ? "bekliyor" : "") + '">' +
        (b.yayinda === false ? "Listede değil" : (DURUMLAR[b.durum] || b.durum)) + "</span>";
      if (duzenlenen && duzenlenen.bolum === "birim" && duzenlenen.id === b.id) {
        html += kartKabugu("Birim düzenle", rozet,
          '<div class="alanlar" data-form>' +
            metinAlani("birim", "Birim no", b.birim, false, "Örn. Z-14") +
            metinAlani("kat", "Kat", b.kat, false, "Zemin Kat / 1. Kat / 2. Kat") +
            sayiAlani("m2", "Alan (m²)", b.m2) +
            metinAlani("kategori", "Uygun kategori", b.kategori) +
            secim("durum", "Durum", b.durum, DURUMLAR) +
            onay("yayinda", "Sitede göster", b.yayinda !== false) +
            yaziAlani("aciklama", "Açıklama", b.aciklama) +
          "</div>", formDugmeleri());
      } else {
        html += kartKabugu(kacis(b.birim || "(numarasız)"), rozet,
          '<div class="satir"><div class="govde">' +
          "<strong>" + kacis(b.kat || "") + " &middot; " + kacis(b.m2 || "?") + " m²</strong>" +
          "<small>" + kacis(b.kategori || "") + "</small>" +
          (b.aciklama ? "<small>" + kacis(b.aciklama) + "</small>" : "") +
          "</div></div>", duzenleDugmeleri("birim", b.id));
      }
    });
    return html;
  }

  function ciz_magazalar() {
    var kat = {};
    (veri.kategoriler || []).forEach(function (k) { kat[k.slug] = k.ad; });
    var logolar = { "": "— logosuz —" };
    (veri.logolar || []).forEach(function (l) { logolar[l] = l; });

    var html = '<div style="margin-bottom:16px"><button class="dugme ana" data-ekle="magaza">+ Yeni mağaza</button></div>';
    (veri.magazalar || []).forEach(function (m) {
      if (duzenlenen && duzenlenen.bolum === "magaza" && duzenlenen.id === m.slug) {
        html += kartKabugu("Mağaza düzenle", "",
          '<div class="alanlar" data-form>' +
            metinAlani("ad", "Mağaza adı", m.ad) +
            metinAlani("slug", "Kısa ad (slug)", m.slug, false, "Benzersiz olmalı") +
            secim("kategori", "Kategori", m.kategori, kat) +
            metinAlani("kat", "Kat", m.kat) +
            metinAlani("no", "Mağaza no", m.no) +
            secim("logo", "Logo", m.logo || "", logolar) +
            yaziAlani("aciklama", "Açıklama", m.aciklama) +
          "</div>", formDugmeleri());
      } else {
        html += kartKabugu(kacis(m.ad), '<span class="rozet">' + kacis(kat[m.kategori] || "") + "</span>",
          '<div class="satir">' + logoOnizleme(m) +
          '<div class="govde"><strong>' + kacis(m.kat || "") + " &middot; No: " +
          kacis(m.no || "") + "</strong><small>" + kacis(m.aciklama || "") + "</small></div></div>",
          duzenleDugmeleri("magaza", m.slug));
      }
    });
    return html;
  }

  /* ============================================================ çizim */
  var CIZ = {
    ozet: ciz_ozet, duyurular: ciz_duyurular, kampanyalar: ciz_kampanyalar,
    firsat: ciz_firsat, kiralama: ciz_kiralama, magazalar: ciz_magazalar
  };

  function sayilar(id) {
    if (id === "duyurular") return (veri.duyurular || []).length;
    if (id === "kampanyalar") return (veri.kampanyalar || []).length;
    if (id === "firsat") return ((veri.firsatGunleri || {}).katilimcilar || []).length;
    if (id === "kiralama") return ((veri.kiralama || {}).birimler || []).length;
    if (id === "magazalar") return (veri.magazalar || []).length;
    return "";
  }

  function ciz() {
    $("#menu").innerHTML = BOLUMLER.map(function (b) {
      var s = sayilar(b.id);
      return '<a href="#" class="bolum' + (b.id === aktif ? " aktif" : "") +
        '" data-bolum="' + b.id + '"><span>' + b.ikon + "</span>" + b.ad +
        (s !== "" ? '<span class="sayi">' + s + "</span>" : "") + "</a>";
    }).join("");
    var b = BOLUMLER.filter(function (x) { return x.id === aktif; })[0];
    $("#baslik").textContent = b ? b.ad : "";
    $("#govde").innerHTML = (CIZ[aktif] || ciz_ozet)();
  }

  /* ============================================================ olaylar */
  function listeVe(bolum) {
    if (bolum === "duyurular") return veri.duyurular;
    if (bolum === "kampanyalar") return veri.kampanyalar;
    if (bolum === "katilimci") return veri.firsatGunleri.katilimcilar;
    if (bolum === "birim") return veri.kiralama.birimler;
    if (bolum === "magaza") return veri.magazalar;
    return null;
  }
  function ogeBul(bolum, id) {
    var l = listeVe(bolum);
    if (bolum === "katilimci") return l[Number(id)];
    var alan = bolum === "magaza" ? "slug" : "id";
    return l.filter(function (x) { return String(x[alan]) === String(id); })[0];
  }

  function yeniOge(bolum) {
    if (bolum === "duyurular") return { id: yeniId("d"), tur: "etkinlik", onem: "normal",
      baslik: "", metin: "", baslangic: bugun(), bitis: "", yayinda: true,
      yerler: ["duyurular"], bagLabel: "", bagUrl: "", gorsel: "" };
    if (bolum === "kampanyalar") return { id: yeniId("k"),
      magaza: (veri.magazalar[0] || {}).slug, baslik: "", aciklama: "",
      baslangic: bugun(), bitis: "", yayinda: true, oneCikar: false };
    if (bolum === "katilimci") return { magaza: (veri.magazalar[0] || {}).slug, teklif: "" };
    if (bolum === "birim") return { id: yeniId("b"), birim: "", kat: "Zemin Kat", m2: 0,
      kategori: "", durum: "bos", aciklama: "", gorsel: "", yayinda: true };
    if (bolum === "magaza") return { ad: "Yeni mağaza", slug: yeniId("m"),
      kategori: (veri.kategoriler[0] || {}).slug, kat: "Zemin Kat", no: "",
      logo: "", aciklama: "" };
    return {};
  }

  function bolumAdi(bolum) {
    return bolum === "katilimci" ? "firsat" :
           bolum === "birim" ? "kiralama" :
           bolum === "magaza" ? "magazalar" : bolum;
  }

  document.addEventListener("click", function (e) {
    var t = e.target;

    var men = t.closest("[data-bolum]");
    if (men) { e.preventDefault(); aktif = men.getAttribute("data-bolum");
      duzenlenen = null; ciz(); return; }

    var ekle = t.closest("[data-ekle]");
    if (ekle) {
      var bl = ekle.getAttribute("data-ekle");
      var o = yeniOge(bl);
      var liste = listeVe(bl);
      // yeni kayıt listenin başına: hem panelde önce görünür hem de
      // anasayfa gibi sınırlı alanlarda ilk sıraya girer
      liste.unshift(o);
      duzenlenen = { bolum: bl, yeni: true,
        id: bl === "katilimci" ? "0"
          : (bl === "magaza" ? o.slug : o.id) };
      aktif = bolumAdi(bl);
      ciz(); return;
    }

    var duz = t.closest("[data-duzenle]");
    if (duz) {
      var p = duz.getAttribute("data-duzenle").split("|");
      duzenlenen = { bolum: p[0], id: p[1] }; ciz(); return;
    }

    var sil = t.closest("[data-sil]");
    if (sil) {
      var q = sil.getAttribute("data-sil").split("|");
      if (!confirm("Bu kayıt silinsin mi?")) return;
      var l = listeVe(q[0]);
      if (q[0] === "katilimci") l.splice(Number(q[1]), 1);
      else {
        var alan = q[0] === "magaza" ? "slug" : "id";
        var i = l.findIndex(function (x) { return String(x[alan]) === q[1]; });
        if (i >= 0) l.splice(i, 1);
      }
      duzenlenen = null; otoKaydet(); ciz();
      bildir("Kayıt silindi.", "basarili");
      return;
    }

    if (t.closest("[data-iptal]")) {
      if (duzenlenen && duzenlenen.yeni) {          // yeni kayıt vazgeçildi
        var yl = listeVe(duzenlenen.bolum);
        if (duzenlenen.bolum === "katilimci") yl.splice(Number(duzenlenen.id), 1);
        else {
          var al = duzenlenen.bolum === "magaza" ? "slug" : "id";
          var ix = yl.findIndex(function (x) { return String(x[al]) === duzenlenen.id; });
          if (ix >= 0) yl.splice(ix, 1);
        }
      }
      duzenlenen = null; ciz(); return;
    }

    if (t.closest("[data-tamam]")) {
      var form = $("[data-form]");
      var oge = ogeBul(duzenlenen.bolum, duzenlenen.id);
      if (form && oge) formuOku(form, oge);
      duzenlenen = null; otoKaydet(); ciz();
      bildir("Kaydedildi. Site aynı tarayıcıda güncellendi.", "basarili");
      return;
    }

    if (t.closest("[data-firsat-kaydet]")) {
      formuOku($("[data-form-firsat]"), veri.firsatGunleri);
      otoKaydet(); ciz(); bildir("Fırsat Günleri ayarları kaydedildi.", "basarili"); return;
    }
    if (t.closest("[data-kiralama-kaydet]")) {
      formuOku($("[data-form-kiralama]"), veri.kiralama);
      otoKaydet(); ciz(); bildir("Kiralama metni kaydedildi.", "basarili"); return;
    }
  });

  /* ---------------------------------------------------------- üst çubuk */
  function baglaUst() {
    $("#btn-kaydet").addEventListener("click", function () { kaydet(); });

    $("#btn-onizle").addEventListener("click", function () {
      if (kirli) kaydet(true);
      window.open("/", "_blank");
    });

    $("#btn-indir").addEventListener("click", function () {
      var b = new Blob([JSON.stringify(veri, null, 2)], { type: "application/json" });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(b);
      a.download = "veri.json";
      a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    });

    $("#btn-yukle").addEventListener("click", function () { $("#dosya").click(); });
    $("#dosya").addEventListener("change", function (e) {
      var f = e.target.files[0];
      if (!f) return;
      var r = new FileReader();
      r.onload = function () {
        try {
          veri = JSON.parse(r.result);
          kaydet(true); duzenlenen = null; ciz();
          bildir("Dosya yüklendi.", "basarili");
        } catch (err) { bildir("Dosya okunamadı: " + err.message, "hata"); }
      };
      r.readAsText(f);
      e.target.value = "";
    });

    $("#btn-test").addEventListener("click", function () {
      var d = $("#btn-test");
      d.disabled = true; d.textContent = "Deneniyor…";
      fetch(API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sifre: girilenSifre || SIFRE, test: true })
      }).then(function (r) {
        return r.json().catch(function () {
          return { hata: "Sunucu yanıtı okunamadı (HTTP " + r.status + ")" };
        });
      }).then(function (y) {
        if (y && y.tamam) bildir(y.mesaj || "Bağlantı çalışıyor.", "basarili");
        else bildir((y && y.hata) || "Bilinmeyen hata", "hata");
      }).catch(function () {
        bildir("Yayınlama uç noktasına ulaşılamadı. Yerelde çalışırken bu normaldir; " +
               "site Vercel'e alındığında etkinleşir.", "hata");
      }).then(function () {
        d.disabled = false; d.textContent = "Bağlantıyı test et";
      });
    });

    $("#btn-yayinla").addEventListener("click", function () {
      if (!confirm("Veri sunucuya gönderilip herkes için yayımlanacak. Devam edilsin mi?")) return;
      if (kirli) kaydet(true);
      var d = $("#btn-yayinla");
      d.disabled = true; d.textContent = "Yayınlanıyor…";
      fetch(API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sifre: girilenSifre || SIFRE, veri: veri })
      }).then(function (r) {
        return r.json().catch(function () { return { hata: "Sunucu yanıtı okunamadı (HTTP " + r.status + ")" }; });
      }).then(function (y) {
        if (y && y.tamam) {
          bildir("Yayımlandı. Vercel dağıtımı ~1 dakika içinde tamamlanır.", "basarili");
        } else if (y && /şifre hatalı/i.test(y.hata || "")) {
          bildir("Yayımlanamadı: Vercel'deki PANEL_SIFRE değişkeni panel şifresiyle " +
                 "aynı olmalı.", "hata");
        } else {
          bildir((y && y.hata) || "Yayımlanamadı: bilinmeyen hata", "hata");
        }
      }).catch(function () {
        bildir("Yayınlama uç noktasına ulaşılamadı. Yerelde çalışırken bu normaldir; " +
               "site Vercel'e alındığında etkinleşir.", "hata");
      }).then(function () {
        d.disabled = false; d.textContent = "Yayınla";
      });
    });

    window.addEventListener("beforeunload", function (e) {
      if (kirli) { e.preventDefault(); e.returnValue = ""; }
    });
  }

  /* ---------------------------------------------------------- başlat */
  function veriYukle() {
    var yerel = null;
    try { yerel = JSON.parse(localStorage.getItem(ANAHTAR) || "null"); } catch (e) {}
    if (yerel) return Promise.resolve(yerel);
    return fetch("/panel/veri.json", { cache: "no-store" }).then(function (r) { return r.json(); });
  }

  function ac() {
    $("#giris").style.display = "none";
    $("#uygulama").classList.add("acik");
    veriYukle().then(function (v) {
      veri = v;
      // eksik alanları tamamla
      veri.duyurular = veri.duyurular || [];
      veri.kampanyalar = veri.kampanyalar || [];
      veri.magazalar = veri.magazalar || [];
      veri.kategoriler = veri.kategoriler || [];
      veri.firsatGunleri = veri.firsatGunleri || { katilimcilar: [] };
      veri.kiralama = veri.kiralama || { birimler: [] };
      $("#son-kayit").textContent = veri.guncelleme
        ? "Son kayıt: " + new Date(veri.guncelleme).toLocaleString("tr-TR") : "—";
      ciz();
      baglaUst();
    }).catch(function (e) {
      $("#govde").innerHTML = '<div class="kutu">Veri yüklenemedi: ' + kacis(e.message) + "</div>";
    });
  }

  $("#giris-form").addEventListener("submit", function (e) {
    e.preventDefault();
    if ($("#sifre").value === SIFRE) {
      girilenSifre = $("#sifre").value;
      try {
        sessionStorage.setItem("pa-panel", "1");
        sessionStorage.setItem("pa-panel-s", girilenSifre);
      } catch (err) {}
      ac();
    } else {
      $("#giris-hata").textContent = "Şifre hatalı.";
      $("#sifre").value = "";
    }
  });

  try {
    if (sessionStorage.getItem("pa-panel") === "1") {
      girilenSifre = sessionStorage.getItem("pa-panel-s") || "";
      ac();
    }
  } catch (e) {}
})();
