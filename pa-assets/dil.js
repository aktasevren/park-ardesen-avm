/* Dil seçici: açılır listeyi yönetir. Bağlantılar gerçek adreslerdir,
   JS kapalıyken de çalışır — burada yalnızca açma/kapama var. */
(function () {
  function kur() {
    document.querySelectorAll("[data-yb-dil]").forEach(function (kap) {
      if (kap.dataset.ybKurulu) return;
      kap.dataset.ybKurulu = "1";
      var dugme = kap.querySelector(".yb-dil-btn");
      if (!dugme) return;

      function ayarla(acik) {
        if (acik) kap.setAttribute("data-acik", "");
        else kap.removeAttribute("data-acik");
        dugme.setAttribute("aria-expanded", acik ? "true" : "false");
      }

      dugme.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        ayarla(!kap.hasAttribute("data-acik"));
      });

      document.addEventListener("click", function (e) {
        if (!kap.contains(e.target)) ayarla(false);
      });

      /* Dil bağlantıları tam sayfa yüklemesi yapmalı.
         Site sayfa geçişlerini barba.js ile yapıyor; barba yalnızca içerik
         kabını değiştirdiği için <html lang>, başlık ve altbilgi eski dilde
         kalıyordu. Tıklamayı yakalama aşamasında kesip adresi doğrudan
         değiştiriyoruz. */
      kap.querySelectorAll(".yb-dil-liste a").forEach(function (a) {
        a.addEventListener("click", function (e) {
          e.preventDefault();
          e.stopImmediatePropagation();
          window.location.assign(a.getAttribute("href"));
        }, true);
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") ayarla(false);
      });
    });
  }
  kur();
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", kur);
  // sayfa geçişlerinde (barba) yeniden kur
  new MutationObserver(kur).observe(document.documentElement,
    { childList: true, subtree: true });
})();
