/* Park Ardeşen AVM — uyarlama katmanı (istemci tarafı davranışlar).
   Tema JS'ine dokunmuyoruz; burada yalnızca statik klonda sunucu
   gerektiren işlevlerin (mağaza arama/filtre) yerine geçen kod var. */
(function () {
  "use strict";

  /* --- Mağazalar: arama + kategori filtresi ---------------------------
     Orijinal site filtreyi ?shop-category= sorgusuyla sunucuda yapıyordu.
     Statik klonda sorgu dizesi çalışmaz; aynı işi tarayıcıda yapıyoruz. */
  function magazaFiltresi() {
    var grid = document.querySelector("[data-pa-magaza-grid]");
    if (!grid) return;

    var kartlar = [].slice.call(grid.querySelectorAll("[data-pa-kategori]"));
    var arama = document.querySelector('.shops-search input[name="search"]');
    var baglar = [].slice.call(document.querySelectorAll(".shops-filter .dropdown-menu-inner a"));
    var bos = document.querySelector(".pa-magaza-yok");
    var kategori = "";

    function normalize(t) {
      return (t || "")
        .toLocaleLowerCase("tr")
        .replace(/ı/g, "i").replace(/ğ/g, "g").replace(/ü/g, "u")
        .replace(/ş/g, "s").replace(/ö/g, "o").replace(/ç/g, "c");
    }

    function uygula() {
      var q = normalize(arama ? arama.value : "");
      var gorunen = 0;
      kartlar.forEach(function (k) {
        var kat = k.getAttribute("data-pa-kategori");
        var ad = normalize(k.getAttribute("data-pa-ad"));
        var uyar = (!kategori || kat === kategori) && (!q || ad.indexOf(q) !== -1);
        k.style.display = uyar ? "" : "none";
        if (uyar) gorunen++;
      });
      if (bos) bos.classList.toggle("acik", gorunen === 0);
    }

    baglar.forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        kategori = a.getAttribute("data-pa-kategori") || "";
        baglar.forEach(function (b) { b.classList.remove("pa-aktif"); });
        a.classList.add("pa-aktif");
        uygula();
        var dd = a.closest(".dropdown-menu");
        if (dd) dd.classList.remove("show");
      });
    });

    if (arama) {
      arama.addEventListener("input", uygula);
      var form = arama.closest("form");
      if (form) form.addEventListener("submit", function (e) { e.preventDefault(); uygula(); });
    }

    uygula();
  }


  /* --- Menü: dışarı tıklayınca kapansın ------------------------------
     Tema yalnızca hamburger düğmesi ve menü içindeki çarpı ile kapanmayı
     destekliyor. Menü açıkken sayfanın geri kalanına yarı saydam bir örtü
     koyup ona gelen tıklamayı kapatma olarak işliyoruz. Örtü olmadan
     "dışarı tıklama" altta kalan bağlantıyı tetikleyebiliyor.

     Örtünün görünürlüğünü CSS'teki `.nav-on` ataya bırakmak yerine
     doğrudan JS'ten sürüyoruz; tema `nav-on` sınıfını <html> üzerinde
     değiştirdiği için MutationObserver ile takip etmek yeterli ve
     davranış stil sırasından bağımsız hâle geliyor. */
  function menuKapatma() {
    var html = document.documentElement;

    var ortu = document.createElement("div");
    ortu.className = "pa-menu-ortu";
    ortu.setAttribute("aria-hidden", "true");
    document.body.appendChild(ortu);

    function acikMi() { return html.classList.contains("nav-on"); }

    function esitle() {
      var acik = acikMi();
      ortu.style.opacity = acik ? "1" : "0";
      ortu.style.visibility = acik ? "visible" : "hidden";
      ortu.style.pointerEvents = acik ? "auto" : "none";
    }

    function kapat() {
      html.classList.remove("nav-on");
      var t = document.querySelector(".nav-toggle");
      if (t) t.classList.remove("on");
      esitle();
    }

    esitle();
    if (window.MutationObserver) {
      new MutationObserver(esitle).observe(html, {
        attributes: true, attributeFilter: ["class"]
      });
    }

    ortu.addEventListener("click", kapat);

    // örtünün yakalayamadığı alanlar için yedek (ör. sabit başlık şeridi)
    document.addEventListener("click", function (e) {
      if (!acikMi()) return;
      if (e.target.closest(".site-header-open")) return;   // menünün içi
      if (e.target.closest(".nav-toggle")) return;         // açma düğmesi
      kapat();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && acikMi()) kapat();
    });
  }

  /* --- İletişim formu -----------------------------------------------
     Site statik; sunucuya form gönderilemiyor. Alanları doğrulayıp
     kullanıcının kendi e-posta uygulamasında hazır bir mesaj açıyoruz —
     böylece form gerçekten işe yarıyor, "gönderildi" yalanı olmuyor. */
  function iletisimFormu() {
    var f = document.querySelector("[data-pa-iletisim]");
    if (!f) return;
    var durum = f.querySelector(".pa-form-durum");

    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var eksik = [];
      ["ad", "eposta", "mesaj"].forEach(function (ad) {
        var el = f.elements[ad];
        el.classList.toggle("pa-hata", !el.value.trim());
        if (!el.value.trim()) eksik.push(ad);
      });
      var kvkk = f.elements.kvkk;
      kvkk.closest(".pa-form-onay").classList.toggle("pa-hata", !kvkk.checked);
      if (!kvkk.checked) eksik.push("kvkk");

      var ep = f.elements.eposta;
      if (ep.value.trim() && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(ep.value.trim())) {
        ep.classList.add("pa-hata");
        eksik.push("eposta-bicim");
      }

      if (eksik.length) {
        durum.textContent = eksik.indexOf("kvkk") >= 0 && eksik.length === 1
          ? "Devam etmek için aydınlatma metnini onaylayın."
          : "Lütfen işaretli alanları doldurun.";
        durum.className = "pa-form-durum hata";
        return;
      }

      var d = f.elements;
      var govde = [
        "Ad Soyad : " + d.ad.value.trim(),
        "E-posta  : " + d.eposta.value.trim(),
        "Telefon  : " + (d.telefon.value.trim() || "-"),
        "Konu     : " + d.konu.value,
        "", d.mesaj.value.trim(), "",
        "— parkardesen.com iletişim formu"
      ].join("\n");

      var hedef = "muhasebe@parkardesen.com";
      var konu = "[Park Ardeşen AVM] " + d.konu.value + " — " + d.ad.value.trim();
      window.location.href = "mailto:" + hedef +
        "?subject=" + encodeURIComponent(konu) +
        "&body=" + encodeURIComponent(govde);

      durum.textContent = "E-posta uygulamanız açılıyor. Açılmazsa " + hedef +
                          " adresine yazabilirsiniz.";
      durum.className = "pa-form-durum basarili";
    });

    f.addEventListener("input", function (e) {
      e.target.classList.remove("pa-hata");
      var o = e.target.closest(".pa-form-onay");
      if (o) o.classList.remove("pa-hata");
    });
  }

  /* --- Sayfa içi bağlantı düzeltmeleri -------------------------------
     Klonda kalan ?shop-category=... bağlantılarını mağaza listesine yönlendir. */
  function bagDuzelt() {
    [].slice.call(document.querySelectorAll('a[href*="shop-category="]')).forEach(function (a) {
      a.setAttribute("href", a.getAttribute("href").split("?")[0] || "#");
    });
  }

  function hazir(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else { fn(); }
  }

  hazir(function () { magazaFiltresi(); bagDuzelt(); menuKapatma(); iletisimFormu(); });

  /* pa-veri.js mağaza ızgarasını ve kategori listesini yeniden çizdiğinde
     filtrenin olay bağları kopuyor; yeniden kuruyoruz. */
  document.addEventListener("pa:veri-cizildi", function () {
    magazaFiltresi();
    bagDuzelt();
  });
})();
