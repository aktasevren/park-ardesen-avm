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

  hazir(function () { magazaFiltresi(); bagDuzelt(); });
})();
