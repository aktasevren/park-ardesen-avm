#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tam sayfa ekran görüntüsü (Playwright'ın headless Chromium'u ile).
Kullanım: python3 _uyarla/ekran.py <yol> [yükseklik]"""
import os, sys, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIKTI = os.environ.get("EKRAN_DIZIN", "/tmp")
TABAN = "http://127.0.0.1:8001/"
HS = os.path.expanduser(
    "~/Library/Caches/ms-playwright/chromium_headless_shell-1194/chrome-mac/headless_shell")

EK = """<style>
*{transition:none!important;animation:none!important}
.home-banner,.home-banner .container{min-height:700px!important}
</style>
<script>
window.addEventListener('load',function(){
  var y=0;
  var t=setInterval(function(){
    y+=300; window.scrollTo(0,y);
    if(y>document.body.scrollHeight+1000){clearInterval(t);window.scrollTo(0,0);}
  },20);
});
</script>"""


def main():
    rel = sys.argv[1]
    h = sys.argv[2] if len(sys.argv) > 2 else "5000"
    src = os.path.join(ROOT, rel)
    s = open(src, encoding="utf-8").read().replace("</head>", EK + "</head>", 1)
    tmp = os.path.join(os.path.dirname(src), "_ekran.html")
    open(tmp, "w", encoding="utf-8").write(s)
    url = TABAN + os.path.relpath(tmp, ROOT).replace(os.sep, "/")
    out = os.path.join(CIKTI, rel.replace("/", "_") + ".png")
    subprocess.run([HS, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    "--window-size=1440,%s" % h, "--virtual-time-budget=12000",
                    "--screenshot=%s" % out, url],
                   capture_output=True, timeout=120)
    os.remove(tmp)
    print(out)


if __name__ == "__main__":
    main()
