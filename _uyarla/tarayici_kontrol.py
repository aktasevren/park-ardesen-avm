#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Her sayfayı gerçek bir tarayıcı motorunda (Playwright'ın headless
Chromium'u) açar; JS hatalarını, yüklenemeyen kaynakları ve menünün
açılıp açılmadığını raporlar. Kullanıcının Chrome penceresine dokunmaz."""
import os, re, sys, glob, json, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABAN = "http://127.0.0.1:8001/"
HS = os.path.expanduser(
    "~/Library/Caches/ms-playwright/chromium_headless_shell-1194/chrome-mac/headless_shell")

PROBE_HEAD = """<script>
window.__h=[];
window.addEventListener('error',function(e){
  var t=e.target||{};
  window.__h.push(t.tagName?(t.tagName+' '+(t.src||t.href||'')):('JS: '+e.message+' @'+(e.filename||'').split('/').pop()+':'+e.lineno));
},true);
window.addEventListener('unhandledrejection',function(e){window.__h.push('PROMISE: '+e.reason);});
</script>"""

PROBE_BODY = """<script>
window.addEventListener('load',function(){
  // sayfayı baştan sona kaydırarak tembel yüklenen görselleri tetikle
  var y=0, adim=400;
  var kaydir=setInterval(function(){
    y+=adim; window.scrollTo(0,y);
    if(y>document.body.scrollHeight+1200){ clearInterval(kaydir); bitir(); }
  },30);
  function bitir(){ setTimeout(function(){
    var t=document.querySelector('.nav-toggle'); if(t) t.click();
    var menuAcik = document.documentElement.classList.contains('nav-on');
    var kirik=[].slice.call(document.querySelectorAll('img')).filter(function(i){
      return i.complete && i.naturalWidth===0;
    }).map(function(i){return (i.currentSrc||i.src||'').split('/').pop();});
    var lazyKalan=[].slice.call(document.querySelectorAll('img.lazyload')).map(function(i){
      return (i.getAttribute('data-src')||'').split('/').pop();
    });
    console.log('RAPOR '+JSON.stringify({menu:menuAcik,
      lazy:lazyKalan.length, lazyOrnek:lazyKalan.slice(0,4),
      kirik:kirik.slice(0,6), kirikSayi:kirik.length,
      hata:window.__h}));
  },900); }
});
</script>"""


def probe_kopyasi(rel):
    src = os.path.join(ROOT, rel)
    s = open(src, encoding="utf-8").read()
    s = s.replace("<head>", "<head>" + PROBE_HEAD, 1)
    s = s.replace("</body>", PROBE_BODY + "</body>", 1)
    hedef = os.path.join(os.path.dirname(src), "_test.html")
    open(hedef, "w", encoding="utf-8").write(s)
    return hedef, os.path.relpath(hedef, ROOT).replace(os.sep, "/")


def calistir(url):
    p = subprocess.run(
        [HS, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
         "--window-size=1440,1000", "--virtual-time-budget=8000",
         "--dump-dom", url],
        capture_output=True, text=True, timeout=90)
    m = re.search(r'RAPOR (\{.*?\})", source', p.stderr, re.S)
    if not m:
        m = re.search(r'RAPOR (\{.*?\})', p.stderr, re.S)
    if not m:
        return None
    return json.loads(m.group(1).replace('\\"', '"'))


def main():
    sayfalar = sys.argv[1:]
    if not sayfalar:
        sayfalar = ["www.dubaioutletmall.com/index.html"] + sorted(
            os.path.relpath(f, ROOT).replace(os.sep, "/")
            for f in glob.glob(os.path.join(ROOT, "www.dubaioutletmall.com", "*", "index.html")))
        sayfalar += ["dubaioutletmall.com/privacy-policy-2/index.html",
                     "dubaioutletmall.com/terms-and-conditions/index.html"]
    sorunlu = 0
    for rel in sayfalar:
        if not os.path.isfile(os.path.join(ROOT, rel)):
            continue
        tmp, turl = probe_kopyasi(rel)
        try:
            r = calistir(TABAN + turl)
        finally:
            os.remove(tmp)
        ad = rel.replace("www.dubaioutletmall.com/", "").replace("/index.html", "") or "anasayfa"
        if r is None:
            print("%-24s RAPOR ALINAMADI" % ad); sorunlu += 1; continue
        bayrak = []
        if r["menu"] is not True: bayrak.append("MENÜ AÇILMADI")
        if r["hata"]: bayrak.append("%d hata" % len(r["hata"]))
        if r["kirikSayi"]: bayrak.append("%d KIRIK görsel" % r["kirikSayi"])
        print("%-24s menü:%-5s %s"
              % (ad, "ok" if r["menu"] else "HAYIR",
                 " | ".join(bayrak) if bayrak else "temiz"))
        for x in r.get("kirik", [])[:4]:
            print("      kırık:", x)
        if r["lazy"]:
            print("      (görüş alanı dışında %d tembel görsel — kaydırınca yükleniyor)"
                  % r["lazy"])
        for h in r["hata"][:6]:
            print("      -", h)
        if bayrak: sorunlu += 1
    print("\nsorunlu sayfa: %d / %d" % (sorunlu, len(sayfalar)))
    return 1 if sorunlu else 0


if __name__ == "__main__":
    sys.exit(main())
