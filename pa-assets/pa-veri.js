/* ------------------------------------------------------------------
   Park Ardeşen AVM — içerik katmanı

   Site statik dosyalardan oluşuyor; kampanya, duyuru, fırsat günleri,
   kiralama birimleri ve mağaza listesi tek bir JSON'dan (panel/veri.json)
   çalışma anında okunup sayfaya çiziliyor. Böylece panelden yapılan
   değişiklik için sayfaların yeniden üretilmesi gerekmiyor.

   Veri kaynağı sırası:
     1) localStorage['pa-veri']  → panelde yapılan, henüz yayımlanmamış
        değişiklikler (aynı tarayıcıda anında görünür)
     2) panel/veri.json          → yayımlanmış hâli

   HTML'de hazır duran içerik (build sırasında üretilen kartlar) JS
   çalışmazsa da anlamlı kalsın diye yerinde bırakılıyor; veri gelince
   üzerine yazılıyor.
   ------------------------------------------------------------------ */
(function () {
  "use strict";

  var ANAHTAR = "pa-veri";
  var KOK = null;   // sitenin kök dizinine göreli önek (ör. "../")

  /* ---------------------------------------------------------- yardımcı */
  function q(sel, kok) { return (kok || document).querySelector(sel); }
  function qa(sel, kok) { return [].slice.call((kok || document).querySelectorAll(sel)); }

  function kacis(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function veriUrl() {
    var m = q('meta[name="pa-veri-url"]');
    return m ? m.getAttribute("content") : "panel/veri.json";
  }

  function kokOnek() {
    if (KOK !== null) return KOK;
    // veriUrl "…/panel/veri.json" biçiminde; site köküne kadar olan kısım
    KOK = veriUrl().replace(/panel\/veri\.json$/, "");
    return KOK;
  }

  /* sayfadan site köküne göreli önek */
  function siteKok() {
    var m = q('meta[name="pa-site-kok"]');
    return m ? m.getAttribute("content") : "";
  }

  function varlik(yol) { return siteKok() + "wp-content/uploads/pa/" + yol; }
  function sayfa(yol) { return siteKok() + yol; }

  /* ---------------------------------------------------------- tarih */
  function bugun() {
    var d = new Date();
    return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) +
           "-" + ("0" + d.getDate()).slice(-2);
  }

  function aralikta(o) {
    var b = bugun();
    if (o.baslangic && o.baslangic > b) return false;
    if (o.bitis && o.bitis < b) return false;
    return true;
  }

  function aktif(o) { return o && o.yayinda !== false && aralikta(o); }

  var AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
               "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"];

  function tarihYaz(g) {
    if (!g) return "";
    var p = g.split("-");
    if (p.length !== 3) return g;
    return Number(p[2]) + " " + AYLAR[Number(p[1]) - 1] + " " + p[0];
  }

  /* ---------------------------------------------------------- duyuru türleri */
  /* Şerit rengi ayrı bir "önem" alanı yerine türden türetiliyor —
     panelde bir alan eksilsin diye. */
  var DIKKAT_TURLERI = ["acil", "bakim"];

  var TURLER = {
    saat:     { ad: paT("Çalışma saati"), ikon: "🕒" },
    acilis:   { ad: "Yeni mağaza",   ikon: "🎉" },
    yakinda:  { ad: "Yakında",       ikon: "🚧" },
    etkinlik: { ad: "Etkinlik",      ikon: "🎈" },
    cekilis:  { ad: "Çekiliş",       ikon: "🎁" },
    kampanya: { ad: "Kampanya",      ikon: "🏷️" },
    hizmet:   { ad: "Yeni hizmet",   ikon: "✨" },
    bakim:    { ad: "Bakım",         ikon: "🛠️" },
    ulasim:   { ad: "Ulaşım",        ikon: "🅿️" },
    sosyal:   { ad: paT("Sosyal sorumluluk"), ikon: "❤️" },
    acil:     { ad: "Acil duyuru",   ikon: "⚠️" }
  };
  function tur(t) { return TURLER[t] || { ad: paT("Duyuru"), ikon: "📢" }; }

  /* Kat adları panelde elle girilebildiği için "1", "1.kat", "Birinci"
     gibi yazımlar oluşabiliyor; hepsini tek biçime indiriyoruz. */
  function katAdi(k) {
    var t = String(k == null ? "" : k).trim();
    if (!t) return paT("Diğer");
    var l = t.toLocaleLowerCase("tr");
    if (/^(z|zemin|0\b|giri[sş])/.test(l)) return paT("Zemin Kat");
    if (/bodrum/.test(l)) return paT("Bodrum Kat");
    if (/birinci/.test(l)) return paT("1. Kat");
    if (/ikinci/.test(l)) return paT("2. Kat");
    if (/[uü][cç][uü]nc[uü]/.test(l)) return paT("3. Kat");
    var m = l.match(/(\d+)/);
    return m ? m[1] + ". " + paT("Kat") : t;
  }

  /* ---------------------------------------------------------- veri */
  function yerelVeri() {
    try {
      var ham = localStorage.getItem(ANAHTAR);
      return ham ? JSON.parse(ham) : null;
    } catch (e) { return null; }
  }

  /* Panelde kaydedilen kopya tarayıcıda tutuluyor ve yayımlanmış dosyadan
     önce geliyor. Ancak siteye sonradan yeni bir alan eklendiğinde (ör.
     "tesisler") eski kopyada o alan hiç bulunmuyor ve içerik görünmez
     oluyordu. Bu yüzden iki kaynağı birleştiriyoruz: paneldeki alanlar
     kazanır, panelde hiç olmayan alanlar dosyadan gelir. */
  function veriGetir() {
    var yerel = yerelVeri();
    return fetch(veriUrl(), { cache: "no-store" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; })
      .then(function (dosya) {
        if (!dosya) return yerel;
        if (!yerel) return dosya;
        // Yayımlanan sürüm daha yeniyse tarayıcıdaki kopya tamamen bırakılır.
        // İçerik sıfırlandığında/toplu değiştiğinde eski kopyanın dosyayı
        // ezmeye devam etmesini böyle engelliyoruz.
        if ((dosya.veriSurumu || 0) > (yerel.veriSurumu || 0)) {
          try { localStorage.setItem(ANAHTAR, JSON.stringify(dosya)); } catch (e) {}
          return dosya;
        }
        var sonuc = {};
        Object.keys(dosya).forEach(function (k) { sonuc[k] = dosya[k]; });
        Object.keys(yerel).forEach(function (k) { sonuc[k] = yerel[k]; });
        return sonuc;
      });
  }

  /* ---------------------------------------------------------- parçalar */
  function magazaHaritasi(v) {
    var h = {};
    (v.magazalar || []).forEach(function (m) { h[m.slug] = m; });
    return h;
  }

  function markaGorsel(m, sinif) {
    if (!m) return "";
    if (m.logo) {
      return '<img src="' + varlik("markalar/" + m.logo) + '" alt="' + kacis(m.ad) +
             '" loading="lazy" decoding="async" class="' + (sinif || "pa-marka-logo") + '">';
    }
    return '<div class="pa-marka-yazi">' + kacis(m.ad) + "</div>";
  }

  /* ============================================================ ÜST ŞERİT */
  function ustSerit(v) {
    var liste = (v.duyurular || []).filter(function (d) {
      return aktif(d) && (d.yerler || []).indexOf("ust-serit") >= 0;
    });
    if (!liste.length) return;
    var d = liste[0];
    var kapatildi;
    try { kapatildi = localStorage.getItem("pa-serit-kapali") === d.id; } catch (e) {}
    if (kapatildi) return;

    var el = document.createElement("div");
    el.className = "pa-serit" +
      (DIKKAT_TURLERI.indexOf(d.tur) >= 0 ? " pa-serit-dikkat" : "");
    el.innerHTML =
      '<div class="pa-serit-ic">' +
        '<span class="pa-serit-ikon">' + tur(d.tur).ikon + "</span>" +
        '<span class="pa-serit-metin"><strong>' + kacis(paMetin(d.baslik)) + "</strong></span>" +
        (d.bagUrl ? '<a class="pa-serit-bag" href="' + kacis(sayfa(d.bagUrl)) + '">' +
                    kacis(paMetin(d.bagLabel) || paT("Detay")) + "</a>" : "") +
        '<button class="pa-serit-kapat" aria-label="' + kacis(paT("Duyuruyu kapat")) + '">&times;</button>' +
      "</div>";
    document.body.insertBefore(el, document.body.firstChild);
    document.documentElement.classList.add("pa-serit-var");
    q(".pa-serit-kapat", el).addEventListener("click", function () {
      el.remove();
      document.documentElement.classList.remove("pa-serit-var");
      try { localStorage.setItem("pa-serit-kapali", d.id); } catch (e) {}
    });
  }

  /* ======================================================= AÇILIŞ PENCERESİ */
  function acilisPenceresi(v) {
    // yalnızca anasayfada. (Tema, iç sayfalarda da <main class="home">
    // kullanıyor; bu yüzden anasayfaya özel duyuru bölümünü işaret alıyoruz.)
    if (!q("[data-pa-duyuru-bolum]")) return;

    // Çerez rıza bandı açıkken duyuru penceresini göstermiyoruz; iki
    // pencere aynı anda çıkınca ikisi de okunmuyor.
    var izinVerildi = false;
    try { izinVerildi = !!localStorage.getItem("pa-cerez-izni"); } catch (e) {}
    if (!izinVerildi) {
      document.addEventListener("pa:cerez-secildi", function () {
        setTimeout(function () { acilisPenceresi(v); }, 400);
      }, { once: true });
      return;
    }
    var liste = (v.duyurular || []).filter(function (d) {
      return aktif(d) && (d.yerler || []).indexOf("acilis-penceresi") >= 0;
    });
    if (!liste.length) return;
    var d = liste[0];
    try { if (sessionStorage.getItem("pa-pencere") === d.id) return; } catch (e) {}

    var ortu = document.createElement("div");
    ortu.className = "pa-pencere-ortu";
    ortu.innerHTML =
      '<div class="pa-pencere" role="dialog" aria-modal="true" aria-label="Duyuru">' +
        '<button class="pa-pencere-kapat" type="button" aria-label="' + paT("Kapat") + '">' +
          '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
            '<path d="M6 6l12 12M18 6L6 18"/></svg>' +
        "</button>" +
        (d.gorsel ? '<div class="pa-pencere-gorsel"><img src="' + varlik(d.gorsel) +
                    '" alt=""></div>' : "") +
        '<div class="pa-pencere-govde">' +
          '<span class="pa-etiket">' + tur(d.tur).ikon + " " + kacis(tur(d.tur).ad) + "</span>" +
          "<h2>" + kacis(paMetin(d.baslik)) + "</h2>" +
          "<p>" + kacis(paMetin(d.metin)) + "</p>" +
          (d.bagUrl ? '<a class="btn" href="' + kacis(sayfa(d.bagUrl)) + '">' +
                      kacis(paMetin(d.bagLabel) || paT("Detay")) + "</a>" : "") +
        "</div>" +
      "</div>";
    document.body.appendChild(ortu);
    requestAnimationFrame(function () { ortu.classList.add("acik"); });

    function kapat() {
      ortu.classList.remove("acik");
      setTimeout(function () { ortu.remove(); }, 300);
      try { sessionStorage.setItem("pa-pencere", d.id); } catch (e) {}
    }
    q(".pa-pencere-kapat", ortu).addEventListener("click", kapat);
    ortu.addEventListener("click", function (e) { if (e.target === ortu) kapat(); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.contains(ortu)) kapat();
    });
  }

  /* ============================================================ DUYURULAR */
  function duyuruKarti(d) {
    var t = tur(d.tur);
    return '<article class="pa-duyuru' +
      (DIKKAT_TURLERI.indexOf(d.tur) >= 0 ? " pa-duyuru-dikkat" : "") + '">' +
      '<div class="pa-duyuru-ust">' +
        '<span class="pa-etiket">' + t.ikon + " " + kacis(t.ad) + "</span>" +
        '<time>' + kacis(tarihYaz(d.baslangic)) + "</time>" +
      "</div>" +
      "<h3>" + kacis(paMetin(d.baslik)) + "</h3>" +
      "<p>" + kacis(paMetin(d.metin)) + "</p>" +
      (d.bagUrl ? '<a class="pa-duyuru-bag" href="' + kacis(sayfa(d.bagUrl)) + '">' +
                  kacis(paMetin(d.bagLabel) || paT("Detay")) + " &rarr;</a>" : "") +
      "</article>";
  }

  function duyuruListesi(v) {
    var hedef = q("[data-pa-duyurular]");
    if (!hedef) return;
    var liste = (v.duyurular || []).filter(function (d) {
      return aktif(d) && (d.yerler || []).indexOf("duyurular") >= 0;
    });
    hedef.innerHTML = liste.length
      ? '<div class="pa-duyuru-listesi">' + liste.map(duyuruKarti).join("") + "</div>"
      : '<p class="pa-bos">Şu anda yayımlanmış bir duyuru bulunmuyor.</p>';
  }

  /* ============================================================ KAMPANYALAR */
  function kampanyaKarti(k, mag, kisa) {
    var m = mag[k.magaza];
    return '<div class="col-12 col-sm-6 col-md-3">' +
      '<div class="card card-shop pa-kampanya">' +
        "<div>" +
          '<div class="pa-logo-kutu pa-magaza-logo">' + markaGorsel(m) + "</div>" +
          "<h2>" + kacis(m ? m.ad : k.magaza) + "</h2>" +
          '<div class="pa-magaza-bilgi"><span>' + kacis(paMetin(k.baslik)) + "</span>" +
          (!kisa && paMetin(k.aciklama) ? "<span>" + kacis(paMetin(k.aciklama)) + "</span>" : "") +
          (!kisa && k.bitis ? '<span class="pa-tarih">' + kacis(tarihYaz(k.bitis)) +
                              " tarihine kadar</span>" : "") +
          "</div>" +
        "</div>" +
      "</div>" +
    "</div>";
  }

  function kampanyalar(v) {
    var mag = magazaHaritasi(v);
    var hepsi = (v.kampanyalar || []).filter(aktif);

    // Anasayfa şeridi: en fazla 8 kart. Önce "öne çıkar" işaretliler,
    // kalan yer varsa diğer kampanyalarla dolduruluyor — böylece panelden
    // eklenen yeni bir kampanya işaretlenmemiş olsa da anasayfada görünüyor.
    var anaRow = q(".home-deals .row");
    if (anaRow) {
      var one = hepsi.filter(function (k) { return k.oneCikar; });
      var digerleri = hepsi.filter(function (k) { return !k.oneCikar; });
      var gosterilecek = one.concat(digerleri).slice(0, 8);
      anaRow.innerHTML = gosterilecek.length
        ? gosterilecek.map(function (k) { return kampanyaKarti(k, mag, true); }).join("")
        : "";
      var bolum = anaRow.closest(".home-deals");
      if (bolum) {
        bolum.style.display = gosterilecek.length ? "" : "none";
        // kart yoksa üstündeki başlık bloğu da gizlensin, öksüz kalmasın
        var baslik = bolum.previousElementSibling;
        if (baslik && baslik.classList.contains("tdb")) {
          baslik.style.display = gosterilecek.length ? "" : "none";
        }
      }
    }

    // Kampanyalar sayfası
    var sayfaRow = q("main.deals .row");
    if (sayfaRow) {
      sayfaRow.setAttribute("data-pa-kampanya-grid", "");
      sayfaRow.innerHTML = hepsi.length
        ? hepsi.map(function (k) { return kampanyaKarti(k, mag, false); }).join("")
        : '<p class="pa-bos">Şu anda yayımlanmış bir kampanya bulunmuyor.</p>';
    }
  }

  /* ========================================================= FIRSAT GÜNLERİ */
  function firsatGunleri(v) {
    var f = v.firsatGunleri;
    var ana = q("main.bargain-monday");
    if (!ana || !f) return;

    var metin = q(".wrap-left-right .col-12", ana) || q(".wrap-left-right", ana);
    if (metin) {
      metin.innerHTML =
        (f.donem ? '<span class="pa-etiket">' + kacis(f.donem) + "</span>" : "") +
        "<p>" + kacis(paMetin(f.aciklama)) + "</p>" +
        (f.yayinda === false
          ? '<p class="pa-bos">Fırsat Günleri şu anda yayında değil.</p>' : "");
    }

    var mag = magazaHaritasi(v);
    var row = qa(".row", ana).filter(function (r) {
      return !r.classList.contains("wrap-left-right");
    })[0];
    if (row) {
      row.innerHTML = (f.katilimcilar || []).map(function (k) {
        var m = mag[k.magaza];
        return '<div class="col-12 col-sm-6 col-md-3">' +
          '<div class="card card-shop">' +
            "<div>" +
              '<div class="pa-logo-kutu pa-magaza-logo">' + markaGorsel(m) + "</div>" +
              "<h2>" + kacis(m ? m.ad : k.magaza) + "</h2>" +
              '<div class="pa-magaza-bilgi"><span>' + kacis(k.teklif) + "</span></div>" +
            "</div>" +
          "</div>" +
        "</div>";
      }).join("");
    }
  }

  /* ============================================================ KİRALAMA */
  var DURUM = { bos: paT("Boş"), rezerve: paT("Rezerve"), dolu: paT("Dolu") };

  function kiralama(v) {
    var hedef = q("[data-pa-kiralama]");
    var k = v.kiralama;
    if (!hedef || !k) return;
    var birimler = (k.birimler || []).filter(function (b) { return b.yayinda !== false; });
    hedef.innerHTML =
      (birimler.length
        ? '<div class="pa-birimler">' + birimler.map(function (b) {
            return '<div class="pa-birim pa-durum-' + kacis(b.durum) + '">' +
              '<div class="pa-birim-ust">' +
                "<h4>" + kacis(b.birim) + "</h4>" +
                '<span class="pa-rozet">' + kacis(DURUM[b.durum] || b.durum) + "</span>" +
              "</div>" +
              '<dl class="pa-birim-bilgi">' +
                "<dt>Kat</dt><dd>" + kacis(b.kat) + "</dd>" +
                "<dt>Alan</dt><dd>" + kacis(b.m2) + " m²</dd>" +
                "<dt>Uygun kategori</dt><dd>" + kacis(b.kategori) + "</dd>" +
              "</dl>" +
              (paMetin(b.aciklama) ? "<p>" + kacis(paMetin(b.aciklama)) + "</p>" : "") +
            "</div>";
          }).join("") + "</div>"
        : '<p class="pa-bos">Şu anda yayımlanmış boş birim bulunmuyor.</p>');
  }

  /* ============================================================ MAĞAZALAR */
  function magazalar(v) {
    var mag = (v.magazalar || []);
    var katAd = {};
    (v.kategoriler || []).forEach(function (k) { katAd[k.slug] = k.ad; });

    var grid = q("[data-pa-magaza-grid]");
    if (grid) {
      grid.innerHTML = mag.map(function (m) {
        return '<div class="col-12 col-sm-6 col-md-3" data-pa-kategori="' +
          kacis(m.kategori) + '" data-pa-ad="' + kacis(m.ad) + '">' +
          '<div class="card card-shop"><div>' +
            '<div class="pa-logo-kutu pa-magaza-logo">' + markaGorsel(m) + "</div>" +
            "<h2>" + kacis(m.ad) + "</h2>" +
            '<div class="pa-magaza-bilgi"><span>' + kacis(katAdi(m.kat)) +
              " &middot; No: " + kacis(m.no) + "</span><span>" +
              kacis(katAd[m.kategori] || "") + "</span></div>" +
          "</div></div></div>";
      }).join("");

      var menu = q(".shops-filter .dropdown-menu-inner");
      if (menu) {
        var html = '<a href="#" class="pa-aktif" data-pa-kategori="">Tümü</a>';
        (v.kategoriler || []).forEach(function (k) {
          var n = mag.filter(function (m) { return m.kategori === k.slug; }).length;
          if (n) html += '<a href="#" class="cat" data-pa-kategori="' + kacis(k.slug) +
                         '">' + kacis(k.ad) + " (" + n + ")</a>";
        });
        menu.innerHTML = html;
      }
    }

    var plan = q(".pa-kat-plani");
    if (plan) {
      // Kat listesi mimari plandan geliyor; panel verisiyle güncellenmiyor.
      plan.innerHTML = PLAN_KATLAR.slice().reverse().map(function (kat) {
        var satir = kat.m.filter(function (m) { return !m.bos; })
          .map(function (m) { return "<li><span>" + kacis(paT(m.ad)) + "</span></li>"; })
          .join("");
        return '<div class="pa-kat"><h3>' + kacis(paT(kat.ad)) + "</h3><ul>" +
               satir + "</ul></div>";
      }).join("");
    }
  }


  /* ====================================================== İZOMETRİK KAT PLANI
     Kat Planı sayfasında, katları üst üste gösteren şematik bir çizim.
     Mağaza verisinden üretiliyor; panelden mağaza eklenip çıkarıldığında
     plan da kendiliğinden güncelleniyor.

     Gerçek mimari proje değil, yönlendirme amaçlı şematik bir gösterimdir —
     sayfadaki not bunu açıkça söylüyor. */


  /* ------------------------------------------------------- kat planı verisi
     Mimari projedeki 1/50 kat planlarından alındı. Kat şeması bu tabloyu
     kullanıyor; mağaza rehberindeki panel verisiyle karıştırılmıyor.
     Birim adı boşsa henüz kiralanmamış: gri çizilir, listede yer almaz. */
  /* Birimler: [x, y, en, derinlik] — mimari plandaki 1/50 çizimden 16x13'lük
     ızgaraya ölçeklendi. y ekseni çevrildi ki AVM ana girişi izometrik
     görünümde öne düşsün. Adı olmayan birim kiralanmamıştır. */
  var PLAN_KATLAR = [
    { ad: "3. Kat",
      m: [{ ad: "Defne Cafe",       k: "yeme-icme", r: [0,    8.65, 3.72, 4.35] },
          { ad: "Chocolate Lounge", k: "yeme-icme", r: [12.80,8.65, 3.20, 4.35] },
          { ad: "Burger King",      k: "yeme-icme", r: [12.51,3.73, 3.49, 4.77] },
          { ad: "Popeyes",          k: "yeme-icme", r: [9.23, 2.98, 3.28, 2.24] },
          { bos: 1, r: [0.22, 2.54, 3.50, 5.96] },
          { bos: 1, r: [3.72, 0,    2.98, 2.54] },
          { bos: 1, r: [10.72,0,    5.28, 2.54] }],
      teras: [3.72, 8.65, 9.08, 4.35],
      yurumerdiven: [4.55, 5.90],
      t: [{ tur: "wc",      ad: "WC",      r: [6.90, 3.70, 2.0, 1.1] },
          { tur: "asansor", ad: "Asansör", r: [6.90, 2.10, 2.2, 1.1] }] },

    { ad: "2. Kat",
      m: [{ ad: "Berru Park",  k: "eglence",  r: [11.61,0,    4.39, 13.0] },
          { ad: "Madame Coco", k: "ev-yasam", r: [0,    2.39, 3.79, 6.11] },
          { bos: 1, r: [0, 8.50, 11.61, 4.50] },
          { bos: 1, r: [0, 0,     6.25, 2.39] }],
      yurumerdiven: [4.60, 5.95],
      t: [{ tur: "wc",      ad: "WC",             r: [6.55, 3.70, 2.0, 1.1] },
          { tur: "asansor", ad: "Asansör",        r: [6.55, 2.10, 2.2, 1.1] },
          { tur: "ofis",    ad: "Yönetim Ofisi",  r: [6.55, 0.50, 2.4, 1.1] }] },

    { ad: "1. Kat",
      m: [{ ad: "LC Waikiki",  k: "moda", r: [0,    8.65, 9.23, 4.35], ek: [0, 0, 3.72, 8.65] },
          { ad: "Paul & Mark", k: "moda", r: [9.23, 8.65, 6.77, 4.35] },
          { ad: "Paul & Mark", k: "moda", r: [11.68,5.22, 4.32, 3.43] },
          { ad: "Paul & Mark", k: "moda", r: [9.23, 0,    6.77, 5.22] }],
      yurumerdiven: [4.55, 5.95],
      t: [{ tur: "wc",      ad: "WC",      r: [6.80, 3.70, 2.0, 1.1] },
          { tur: "asansor", ad: "Asansör", r: [6.80, 2.10, 2.2, 1.1] }] },

    { ad: "Zemin Kat",
      m: [{ ad: "LC Waikiki",    k: "moda",      r: [0,    0,    3.50, 13.0] },
          { ad: "Migros",        k: "market",    r: [11.80,0,    4.20, 10.10] },
          { ad: "Bargello",      k: "kozmetik",  r: [9.20, 7.70, 2.60, 0.95] },
          { ad: "Kokoş",         k: "moda",      r: [9.20, 8.80, 2.60, 1.30] },
          { ad: "Gratis",        k: "kozmetik",  r: [4.10, 10.30,2.70, 2.70] },
          { ad: "Gloria Jean's", k: "yeme-icme", r: [9.20, 10.30,6.80, 2.70] },
          { ad: "Long Street",   k: "moda",      r: [4.90, 3.70, 1.90, 2.00] }],
      yurumerdiven: [4.55, 5.95],
      giris: [7.60, 10.30],
      t: [{ tur: "asansor", ad: "Asansör",        r: [7.00, 1.90, 2.2, 1.1] },
          { tur: "otopark", ad: "Otopark Girişi", r: [4.55, 0.30, 2.4, 1.1] }] }
  ];


  var KAT_RENK = {
    moda:      "#4C7FE0", ayakkabi: "#7A5AF8", "ev-yasam": "#E08A3C",
    kozmetik:  "#D6489B", market:   "#E4572E", "yeme-icme": "#2FA36B",
    eglence:   "#F2B705", hizmet:   "#7A8794"
  };
  /* Mağaza dışı birimler: giriş, WC, danışma… Koridora yerleştiriliyor. */
  var TESIS = {
    giris:   { etiket: paT("GİRİŞ"),   renk: "#e11f26", genis: 2.6 },
    wc:      { etiket: paT("WC"),      renk: "#4a4a55", genis: 1.7 },
    danisma: { etiket: paT("DANIŞMA"), renk: "#1580c4", genis: 2.4 },
    mescit:  { etiket: paT("MESCİT"),  renk: "#3f8f2c", genis: 2.2 },
    asansor: { etiket: paT("ASANSÖR"), renk: "#7a5af8", genis: 2.2 },
    atm:     { etiket: paT("ATM"),     renk: "#8a8a94", genis: 1.7 },
    otopark: { etiket: paT("OTOPARK"), renk: "#3c3a37", genis: 2.4 },
    teras:   { etiket: paT("TERAS"),   renk: "#3f8f2c", genis: 2.2 },
    ofis:    { etiket: paT("OFİS"),    renk: "#7a8794", genis: 2.0 }
  };
  function tesisTur(t) {
    return TESIS[t] || { etiket: String(t || "").toLocaleUpperCase("tr"),
                         renk: "#8a8a94", genis: 2.2 };
  }

  var U = 32;                       // birim boy (piksel)
  var GENISLIK = 16, DERINLIK = 13; // plan ızgarası (mimari plan oranı)

  function koyu(hex, oran) {
    var n = parseInt(hex.slice(1), 16);
    var r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
    return "rgb(" + [r, g, b].map(function (c) {
      return Math.round(c * oran);
    }).join(",") + ")";
  }

  function iso(x, y, z) {
    return [(x - y) * U, (x + y) * U * 0.5 - (z || 0) * U];
  }
  function nokta(p) { return p[0].toFixed(1) + "," + p[1].toFixed(1); }

  /* İzometrik kutu: üst yüz + iki yan yüz */
  function kutu(x, y, w, d, h, renk) {
    var ust = [iso(x, y, h), iso(x + w, y, h), iso(x + w, y + d, h), iso(x, y + d, h)];
    var sol = [iso(x, y + d, h), iso(x + w, y + d, h), iso(x + w, y + d, 0), iso(x, y + d, 0)];
    var sag = [iso(x + w, y, h), iso(x + w, y + d, h), iso(x + w, y + d, 0), iso(x + w, y, 0)];
    return '<polygon points="' + sol.map(nokta).join(" ") + '" fill="' + koyu(renk, 0.66) + '"/>' +
           '<polygon points="' + sag.map(nokta).join(" ") + '" fill="' + koyu(renk, 0.82) + '"/>' +
           '<polygon points="' + ust.map(nokta).join(" ") + '" fill="' + renk +
           '" stroke="rgba(255,255,255,.55)" stroke-width="1"/>';
  }

  function dortgen(x, y, w, d, dolgu, cizgi) {
    var p = [iso(x, y, 0), iso(x + w, y, 0), iso(x + w, y + d, 0), iso(x, y + d, 0)];
    return '<polygon points="' + p.map(nokta).join(" ") + '" fill="' + dolgu +
           '" stroke="' + (cizgi || "none") + '" stroke-width="1.2"/>';
  }

  function rozet(x, y, sira) {
    var p = iso(x, y, 0.95);
    return '<g class="pa-kat3d-no"><circle cx="' + p[0].toFixed(1) + '" cy="' +
      p[1].toFixed(1) + '" r="11" fill="#fff" stroke="rgba(0,0,0,.18)"/>' +
      '<text x="' + p[0].toFixed(1) + '" y="' + (p[1] + 4).toFixed(1) +
      '" text-anchor="middle" font-size="13" font-weight="700" fill="#2b2b2e">' +
      sira + "</text></g>";
  }

  /* Koridordaki tesis plakası: alçak kutu + üstünde etiket */
  function tesisPlakasi(x, y, w, d, tur) {
    var t = tesisTur(tur);
    var g = kutu(x, y, w, d, 0.28, t.renk);
    var p = iso(x + w / 2, y + d / 2, 0.3);
    g += '<text x="' + p[0].toFixed(1) + '" y="' + (p[1] + 4).toFixed(1) +
         '" text-anchor="middle" font-size="12" font-weight="700" ' +
         'fill="#fff" class="pa-kat3d-etiket">' + kacis(t.etiket) + "</text>";
    return g;
  }

  /* Giriş oku — ön cepheden içeri doğru */
  function girisOku(x, y) {
    var a = iso(x, y + 1.9, 0.05), b = iso(x, y, 0.05);
    return '<line x1="' + nokta(a).replace(",", '" y1="') + '" x2="' +
      nokta(b).replace(",", '" y2="') +
      '" stroke="#e11f26" stroke-width="3" stroke-dasharray="6 4" ' +
      'marker-end="url(#paOk2)"/>';
  }

  /* Yürüyen merdiven — referans çizimdeki gibi kırmızı */
  function merdiven(x, y) {
    var g = dortgen(x, y, 3.4, 1.6, "#e11f26", "rgba(0,0,0,.15)");
    for (var i = 0; i < 6; i++) {
      var a = iso(x + 0.35 + i * 0.5, y + 0.3, 0.02);
      var b = iso(x + 0.35 + i * 0.5, y + 1.3, 0.02);
      g += '<line x1="' + nokta(a).replace(",", '" y1="') + '" x2="' +
           nokta(b).replace(",", '" y2="') + '" stroke="rgba(255,255,255,.75)" stroke-width="1.6"/>';
    }
    var u1 = iso(x + 0.6, y + 0.8, 0.06), u2 = iso(x + 2.9, y + 0.8, 0.06);
    g += '<line x1="' + nokta(u1).replace(",", '" y1="') + '" x2="' +
         nokta(u2).replace(",", '" y2="') +
         '" stroke="#fff" stroke-width="2.4" marker-end="url(#paOk)"/>';
    return g;
  }

  function katCizimi(kat) {
    var parcalar = [], rozetler = [], yerlesim = [], sira = 0;

    // zemin plakası
    parcalar.push(dortgen(0, 0, GENISLIK, DERINLIK, "#ececed", "rgba(0,0,0,.18)"));
    if (kat.teras) {
      var tr = kat.teras;
      parcalar.push(dortgen(tr[0], tr[1], tr[2], tr[3], "#e4ede0", "rgba(63,143,44,.35)"));
    }

    /* İzometrik görünümde x+y büyüdükçe öğe öne gelir; doğru örtüşme için
       uzaktan yakına çiziyoruz. */
    var cizilecek = [];
    (kat.m || []).forEach(function (m) {
      var renk = m.bos ? "#d7d5d1" : (KAT_RENK[m.k] || "#8a8a94");
      var yuk = m.bos ? 0.5 : 0.9;
      if (!m.bos) { sira++; yerlesim.push({ no: sira, ad: m.ad, renk: renk }); }
      var no = m.bos ? 0 : sira;
      cizilecek.push({ r: m.r, renk: renk, yuk: yuk, no: no });
      if (m.ek) cizilecek.push({ r: m.ek, renk: renk, yuk: yuk, no: 0 });
    });
    (kat.t || []).forEach(function (t) {
      cizilecek.push({ r: t.r, tesis: t.tur });
    });
    if (kat.yurumerdiven)
      cizilecek.push({ r: [kat.yurumerdiven[0], kat.yurumerdiven[1], 3.4, 1.6], ym: 1 });

    cizilecek.sort(function (a, b) {
      return (a.r[0] + a.r[1]) - (b.r[0] + b.r[1]);
    });
    cizilecek.forEach(function (o) {
      var r = o.r;
      if (o.ym) { parcalar.push(merdiven(r[0], r[1])); return; }
      if (o.tesis) { parcalar.push(tesisPlakasi(r[0], r[1], r[2], r[3], o.tesis)); return; }
      parcalar.push(kutu(r[0], r[1], r[2], r[3], o.yuk, o.renk));
      if (o.no) rozetler.push(rozet(r[0] + r[2] / 2, r[1] + r[3] / 2, o.no));
    });

    // ana giriş — ön cephenin dışında
    var girisVar = false;
    if (kat.giris) {
      girisVar = true;
      parcalar.push(tesisPlakasi(kat.giris[0], DERINLIK + 0.55, 2.6, 1.1, "giris"));
      parcalar.push(girisOku(kat.giris[0] + 1.3, DERINLIK - 0.6));
    }

    var ekDerin = DERINLIK + (girisVar ? 1.7 : 0);
    var minx = iso(0, ekDerin, 0)[0], maxx = iso(GENISLIK, 0, 0)[0];
    var miny = iso(0, 0, 1)[1], maxy = iso(GENISLIK, ekDerin, 0)[1];
    var p = 34;
    var vb = [minx - p, miny - p, (maxx - minx) + p * 2, (maxy - miny) + p * 2];

    return {
      svg: '<svg viewBox="' + vb.map(function (n) { return n.toFixed(1); }).join(" ") +
        '" role="img" aria-label="' + kacis(paT("Kat şeması")) + '">' +
        '<defs><marker id="paOk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" ' +
        'markerHeight="5" orient="auto"><path d="M0,1 L9,5 L0,9 z" fill="#fff"/></marker>' +
        '<marker id="paOk2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" ' +
        'markerHeight="4" orient="auto"><path d="M0,1 L9,5 L0,9 z" fill="#e11f26"/></marker>' +
        "</defs>" + parcalar.join("") + rozetler.join("") + "</svg>",
      yerlesim: yerlesim
    };
  }

  function katPlani3D(v) {
    var hedef = q("[data-pa-kat3d]");
    if (!hedef) return;

    // Şema mimari plandan çiziliyor; mağaza rehberi panel verisinden gelir.
    hedef.innerHTML = PLAN_KATLAR.map(function (kat) {
      var c = katCizimi(kat);
      return '<article class="pa-kat3d-satir">' +
        '<div class="pa-kat3d-gorsel">' + c.svg + "</div>" +
        '<div class="pa-kat3d-bilgi"><h3>' + kacis(paT(kat.ad)) + "</h3>" +
        '<ol class="pa-kat3d-liste">' +
          c.yerlesim.map(function (o) {
            return '<li><span class="pa-kat3d-rozet" style="background:' + o.renk + '">' +
              o.no + '</span><span class="pa-kat3d-ad">' + kacis(paT(o.ad)) +
              "</span></li>";
          }).join("") +
        "</ol>" +
        ((kat.t || []).length
          ? '<ul class="pa-kat3d-tesis">' + kat.t.map(function (t) {
              var b = tesisTur(t.tur);
              return '<li><span class="pa-kat3d-tesis-rozet" style="background:' +
                b.renk + '">' + kacis(b.etiket) + "</span>" + kacis(paT(t.ad)) + "</li>";
            }).join("") + "</ul>"
          : "") +
        "</div></article>";
    }).join("") +
    '<p class="pa-kat-not">' + paT("Çizim mimari kat planından uyarlanmıştır; " +
      "yönlendirme amaçlı şematik bir görünümdür. Gri bloklar henüz kiralanmamış " +
      "birimlerdir.") + "</p>";
  }

  /* ============================================================ ÇALIŞTIR */
  function ciz(v) {
    if (!v) return;
    try { ustSerit(v); } catch (e) { console.warn("[pa] üst şerit", e); }
    try { acilisPenceresi(v); } catch (e) { console.warn("[pa] pencere", e); }
    try { duyuruListesi(v); } catch (e) { console.warn("[pa] duyurular", e); }
    try { kampanyalar(v); } catch (e) { console.warn("[pa] kampanyalar", e); }
    try { firsatGunleri(v); } catch (e) { console.warn("[pa] fırsat günleri", e); }
    try { kiralama(v); } catch (e) { console.warn("[pa] kiralama", e); }
    try { magazalar(v); } catch (e) { console.warn("[pa] mağazalar", e); }
    try { katPlani3D(v); } catch (e) { console.warn("[pa] kat planı", e); }
    document.dispatchEvent(new CustomEvent("pa:veri-cizildi", { detail: v }));
  }

  function basla() {
    veriGetir().then(ciz);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", basla);
  } else { basla(); }

  // panel aynı tarayıcıda kaydettiğinde açık sekmeler kendini yenilesin
  window.addEventListener("storage", function (e) {
    if (e.key === ANAHTAR) location.reload();
  });
})();
