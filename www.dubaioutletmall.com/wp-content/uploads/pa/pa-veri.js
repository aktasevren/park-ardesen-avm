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

  /* sayfadan sitenin (www.dubaioutletmall.com) köküne göreli önek */
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
  var TURLER = {
    saat:     { ad: "Çalışma saati", ikon: "🕒" },
    acilis:   { ad: "Yeni mağaza",   ikon: "🎉" },
    yakinda:  { ad: "Yakında",       ikon: "🚧" },
    etkinlik: { ad: "Etkinlik",      ikon: "🎈" },
    cekilis:  { ad: "Çekiliş",       ikon: "🎁" },
    kampanya: { ad: "Kampanya",      ikon: "🏷️" },
    hizmet:   { ad: "Yeni hizmet",   ikon: "✨" },
    bakim:    { ad: "Bakım",         ikon: "🛠️" },
    ulasim:   { ad: "Ulaşım",        ikon: "🅿️" },
    sosyal:   { ad: "Sosyal sorumluluk", ikon: "❤️" },
    acil:     { ad: "Acil duyuru",   ikon: "⚠️" }
  };
  function tur(t) { return TURLER[t] || { ad: "Duyuru", ikon: "📢" }; }

  /* ---------------------------------------------------------- veri */
  function yerelVeri() {
    try {
      var ham = localStorage.getItem(ANAHTAR);
      return ham ? JSON.parse(ham) : null;
    } catch (e) { return null; }
  }

  function veriGetir() {
    var yerel = yerelVeri();
    if (yerel) return Promise.resolve(yerel);
    return fetch(veriUrl(), { cache: "no-store" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; });
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
    el.className = "pa-serit pa-onem-" + (d.onem || "normal");
    el.innerHTML =
      '<div class="pa-serit-ic">' +
        '<span class="pa-serit-ikon">' + tur(d.tur).ikon + "</span>" +
        '<span class="pa-serit-metin"><strong>' + kacis(d.baslik) + "</strong></span>" +
        (d.bagUrl ? '<a class="pa-serit-bag" href="' + kacis(sayfa(d.bagUrl)) + '">' +
                    kacis(d.bagLabel || "Detay") + "</a>" : "") +
        '<button class="pa-serit-kapat" aria-label="Duyuruyu kapat">&times;</button>' +
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
        '<button class="pa-pencere-kapat" aria-label="Kapat">&times;</button>' +
        (d.gorsel ? '<div class="pa-pencere-gorsel"><img src="' + varlik(d.gorsel) +
                    '" alt=""></div>' : "") +
        '<div class="pa-pencere-govde">' +
          '<span class="pa-etiket">' + tur(d.tur).ikon + " " + kacis(tur(d.tur).ad) + "</span>" +
          "<h2>" + kacis(d.baslik) + "</h2>" +
          "<p>" + kacis(d.metin) + "</p>" +
          (d.bagUrl ? '<a class="btn" href="' + kacis(sayfa(d.bagUrl)) + '">' +
                      kacis(d.bagLabel || "Detay") + "</a>" : "") +
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
    return '<article class="pa-duyuru pa-onem-' + (d.onem || "normal") + '">' +
      '<div class="pa-duyuru-ust">' +
        '<span class="pa-etiket">' + t.ikon + " " + kacis(t.ad) + "</span>" +
        '<time>' + kacis(tarihYaz(d.baslangic)) + "</time>" +
      "</div>" +
      "<h3>" + kacis(d.baslik) + "</h3>" +
      "<p>" + kacis(d.metin) + "</p>" +
      (d.bagUrl ? '<a class="pa-duyuru-bag" href="' + kacis(sayfa(d.bagUrl)) + '">' +
                  kacis(d.bagLabel || "Detay") + " &rarr;</a>" : "") +
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
          '<div class="pa-magaza-bilgi"><span>' + kacis(k.baslik) + "</span>" +
          (!kisa && k.aciklama ? "<span>" + kacis(k.aciklama) + "</span>" : "") +
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

    // anasayfadaki şerit: öne çıkanlar (yoksa ilk 8)
    var anaRow = q(".home-deals .row");
    if (anaRow) {
      var one = hepsi.filter(function (k) { return k.oneCikar; });
      if (!one.length) one = hepsi.slice(0, 8);
      anaRow.innerHTML = one.slice(0, 8).map(function (k) {
        return kampanyaKarti(k, mag, true);
      }).join("");
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
        "<p>" + kacis(f.aciklama) + "</p>" +
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
  var DURUM = { bos: "Boş", rezerve: "Rezerve", dolu: "Dolu" };

  function kiralama(v) {
    var hedef = q("[data-pa-kiralama]");
    var k = v.kiralama;
    if (!hedef || !k) return;
    var birimler = (k.birimler || []).filter(function (b) { return b.yayinda !== false; });
    hedef.innerHTML =
      (k.girisMetni ? "<p>" + kacis(k.girisMetni) + "</p>" : "") +
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
              (b.aciklama ? "<p>" + kacis(b.aciklama) + "</p>" : "") +
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
            '<div class="pa-magaza-bilgi"><span>' + kacis(m.kat) +
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
      var SIRA = ["Zemin Kat", "1. Kat", "2. Kat"];
      var katlar = {};
      mag.forEach(function (m) {
        (katlar[m.kat || "Diğer"] = katlar[m.kat || "Diğer"] || []).push(m);
      });
      var adlar = SIRA.filter(function (k) { return katlar[k]; })
        .concat(Object.keys(katlar).filter(function (k) { return SIRA.indexOf(k) < 0; }));
      plan.innerHTML = adlar.map(function (k) {
        var satir = katlar[k].sort(function (a, b) {
          return String(a.no).localeCompare(String(b.no));
        }).map(function (m) {
          return "<li><span>" + kacis(m.ad) + "</span><em>" + kacis(m.no) +
                 " &middot; " + kacis(katAd[m.kategori] || "") + "</em></li>";
        }).join("");
        return '<div class="pa-kat"><h3>' + kacis(k) + "</h3><ul>" + satir + "</ul></div>";
      }).join("");
    }
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
