/* ------------------------------------------------------------------
   Park Ardeşen AVM — çerez rıza bandı

   KVKK (6698) ve GDPR açısından "sadece Tamam" düğmesi yeterli değil:
   rıza açık, bilgilendirilmiş ve **geri alınabilir** olmalı; reddetmek
   kabul etmek kadar kolay olmalı. Bu yüzden bant üç seçenek sunuyor:
   Kabul et · Reddet · Ayarlar.

   Zorunlu çerezler sitenin çalışması için gerekli olanlardır (rıza kaydı,
   panel oturumu) ve rıza gerektirmez. İsteğe bağlı kategoriler varsayılan
   olarak KAPALIDIR; kullanıcı açmadıkça hiçbir ölçümleme/pazarlama kodu
   yüklenmez.

   Şu an sitede üçüncü taraf ölçümleme yok. Sonradan eklenirse:
       if (window.paCerezIzni("olcumleme")) { ...kodu yükle... }
   ile koşullandırın; kullanıcı rızasını geri çekince sayfa yenilenir.
   ------------------------------------------------------------------ */
(function () {
  "use strict";

  var ANAHTAR = "pa-cerez-izni";
  var SURUM = 1;                       // metin/kategori değişince artırın

  var KATEGORILER = [
    { id: "zorunlu", ad: "Zorunlu çerezler", kilitli: true,
      aciklama: "Sitenin çalışması için gereklidir: çerez tercihinizin " +
                "hatırlanması ve yönetim paneli oturumu. Kapatılamaz." },
    { id: "tercih", ad: "Tercih çerezleri", kilitli: false,
      aciklama: "Kapattığınız duyuru bandı gibi tercihlerinizi hatırlar." },
    { id: "olcumleme", ad: "Ölçümleme çerezleri", kilitli: false,
      aciklama: "Sayfaların ne kadar ziyaret edildiğini anonim olarak ölçer. " +
                "Şu anda sitede ölçümleme aracı kullanılmıyor." },
    { id: "pazarlama", ad: "Pazarlama çerezleri", kilitli: false,
      aciklama: "İlgi alanlarınıza göre reklam gösterimi için kullanılır. " +
                "Şu anda sitede pazarlama aracı kullanılmıyor." }
  ];

  function izinOku() {
    try {
      var v = JSON.parse(localStorage.getItem(ANAHTAR) || "null");
      return v && v.surum === SURUM ? v : null;
    } catch (e) { return null; }
  }

  function izinYaz(secim) {
    try {
      localStorage.setItem(ANAHTAR, JSON.stringify({
        surum: SURUM, tarih: new Date().toISOString(), secim: secim
      }));
    } catch (e) {}
    // duyuru penceresi gibi diğer bileşenler rıza kararını bekliyor
    document.dispatchEvent(new CustomEvent("pa:cerez-secildi", { detail: secim }));
  }

  /* dışarıya açık: window.paCerezIzni("olcumleme") */
  window.paCerezIzni = function (kategori) {
    if (kategori === "zorunlu") return true;
    var v = izinOku();
    return !!(v && v.secim && v.secim[kategori]);
  };

  function hepsi(deger) {
    var o = {};
    KATEGORILER.forEach(function (k) { o[k.id] = k.kilitli ? true : deger; });
    return o;
  }

  function kok() {
    var m = document.querySelector('meta[name="pa-site-kok"]');
    return m ? m.getAttribute("content") : "";
  }

  function bantGoster() {
    var el = document.createElement("div");
    el.className = "pa-cerez";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-label", "Çerez tercihleri");
    el.innerHTML =
      '<div class="pa-cerez-ic">' +
        '<div class="pa-cerez-metin">' +
          "<strong>Çerezleri kullanıyoruz</strong>" +
          "<p>Sitenin düzgün çalışması için zorunlu çerezleri kullanıyoruz. " +
          "Tercih, ölçümleme ve pazarlama çerezleri yalnızca siz izin verirseniz " +
          "çalışır. Ayrıntılar için " +
          '<a href="' + kok() + 'gizlilik-politikasi/">Gizlilik Politikası ve ' +
          "KVKK Aydınlatma Metni</a> sayfamıza bakabilirsiniz.</p>" +
        "</div>" +
        '<div class="pa-cerez-dugmeler">' +
          '<button class="pa-cerez-btn ikincil" data-pa-cerez="ayar">Ayarlar</button>' +
          '<button class="pa-cerez-btn ikincil" data-pa-cerez="ret">Reddet</button>' +
          '<button class="pa-cerez-btn birincil" data-pa-cerez="kabul">Kabul et</button>' +
        "</div>" +
      "</div>";
    document.body.appendChild(el);
    requestAnimationFrame(function () { el.classList.add("acik"); });

    el.addEventListener("click", function (e) {
      var d = e.target.closest("[data-pa-cerez]");
      if (!d) return;
      var t = d.getAttribute("data-pa-cerez");
      if (t === "kabul") { izinYaz(hepsi(true)); kapat(el); }
      else if (t === "ret") { izinYaz(hepsi(false)); kapat(el); }
      else { kapat(el); ayarGoster(); }
    });
  }

  function kapat(el) {
    el.classList.remove("acik");
    setTimeout(function () { el.remove(); }, 300);
  }

  function ayarGoster() {
    var v = izinOku();
    var secim = (v && v.secim) || hepsi(false);
    var ortu = document.createElement("div");
    ortu.className = "pa-cerez-ortu";
    ortu.innerHTML =
      '<div class="pa-cerez-panel" role="dialog" aria-modal="true" aria-label="Çerez ayarları">' +
        '<button class="pa-cerez-kapat" aria-label="Kapat">&times;</button>' +
        "<h2>Çerez ayarları</h2>" +
        '<p class="pa-cerez-giris">Hangi çerezlere izin verdiğinizi buradan ' +
        "seçebilirsiniz. Tercihinizi istediğiniz zaman değiştirebilir ya da " +
        "geri alabilirsiniz.</p>" +
        KATEGORILER.map(function (k) {
          return '<label class="pa-cerez-satir">' +
            '<input type="checkbox" data-k="' + k.id + '"' +
              (k.kilitli || secim[k.id] ? " checked" : "") +
              (k.kilitli ? " disabled" : "") + ">" +
            "<span><strong>" + k.ad + (k.kilitli ? " (her zaman açık)" : "") +
            "</strong><em>" + k.aciklama + "</em></span></label>";
        }).join("") +
        '<div class="pa-cerez-panel-alt">' +
          '<button class="pa-cerez-btn ikincil" data-pa-ayar="ret">Tümünü reddet</button>' +
          '<button class="pa-cerez-btn ikincil" data-pa-ayar="kabul">Tümünü kabul et</button>' +
          '<button class="pa-cerez-btn birincil" data-pa-ayar="kaydet">Seçimimi kaydet</button>' +
        "</div>" +
      "</div>";
    document.body.appendChild(ortu);
    requestAnimationFrame(function () { ortu.classList.add("acik"); });

    function kapatPanel() {
      ortu.classList.remove("acik");
      setTimeout(function () { ortu.remove(); }, 300);
    }

    ortu.addEventListener("click", function (e) {
      if (e.target === ortu || e.target.closest(".pa-cerez-kapat")) {
        kapatPanel();
        if (!izinOku()) bantGoster();      // seçim yapılmadıysa bant geri gelsin
        return;
      }
      var d = e.target.closest("[data-pa-ayar]");
      if (!d) return;
      var t = d.getAttribute("data-pa-ayar");
      if (t === "kabul") izinYaz(hepsi(true));
      else if (t === "ret") izinYaz(hepsi(false));
      else {
        var o = { zorunlu: true };
        [].slice.call(ortu.querySelectorAll("[data-k]")).forEach(function (c) {
          o[c.getAttribute("data-k")] = c.disabled ? true : c.checked;
        });
        izinYaz(o);
      }
      kapatPanel();
      location.reload();                    // rıza değişti: sayfayı tazele
    });
  }

  /* Footer'daki "Çerez Ayarları" bağlantısı paneli açar */
  function baglantiyiBagla() {
    document.addEventListener("click", function (e) {
      var a = e.target.closest("[data-pa-cerez-ayar]");
      if (!a) return;
      e.preventDefault();
      ayarGoster();
    });
  }

  function basla() {
    baglantiyiBagla();
    if (!izinOku()) bantGoster();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", basla);
  } else { basla(); }
})();
