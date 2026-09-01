/* Park Ardeşen AVM — kat planı
   Geometri, mimari projedeki kat planlarından (1/50) çıkarıldı ve
   ziyaretçiye göre sadeleştirildi: metrekare, dükkân numarası gibi teknik
   bilgi yok. Kiralanmamış birimler gri ve isimsiz. */
(function () {
  "use strict";
  var NS = "http://www.w3.org/2000/svg";
  function el(a, o, e) {
    var x = document.createElementNS(NS, a);
    for (var k in o) if (o[k] != null) x.setAttribute(k, o[k]);
    if (e) e.appendChild(x);
    return x;
  }
  var CEVIRME = { WC: 1 };          // tabelalarda evrensel, olduğu gibi kalsın
  function T(s) { return (window.paT && !CEVIRME[s]) ? paT(s) : s; }

  /* --------------------------------------------------------------- katlar
     b : birimler — [ad, x, y, en, boy]  ·  ad boşsa kiralanmamış
     p : çokgen birimler — [ad, "x,y x,y …"]
     o : ortak alan  ·  t : teras  ·  i : işaretler [tür, x, y, etiket] */
  var KATLAR = [
    { ad: "Zemin Kat", kod: "zemin",
      b: [["Gratis",        277,  40, 156, 127],
          ["Gloria Jean's", 571,  40, 389, 127],
          ["Kokoş",         571, 178, 148,  62],
          ["Bargello",      571, 247, 148,  45],
          ["Migros",        719, 178, 241, 482],
          ["Long Street",   321, 387, 107,  96]],
      p: [["LC Waikiki", "40,40 277,40 277,240 241,240 241,660 40,660", 140, 430]],
      o: [[241, 240, 330, 147, "yurumerdiven"], [321, 483, 339, 177, "cekirdek"]],
      i: [["giris", 502,  58, "AVM Ana Girişi"],
          ["asansor", 470, 520, ""], ["merdiven", 360, 560, ""],
          ["otopark", 392, 642, "Otopark Girişi"], ["konut", 629, 642, "Konut Girişi"]] },

    { ad: "1. Kat", kod: "k1",
      b: [["Paul & Mark", 571,  40, 389, 208],
          ["Paul & Mark", 712, 248, 248, 163],
          ["Paul & Mark", 571, 411, 389, 249]],
      p: [["LC Waikiki", "40,40 571,40 571,248 254,248 254,660 40,660", 150, 480]],
      o: [[254, 248, 317, 149, "yurumerdiven"], [417, 397, 154, 263, "cekirdek"]],
      i: [["wc", 494, 470, ""], ["asansor", 494, 545, ""], ["merdiven", 494, 615, ""]] },

    { ad: "2. Kat", kod: "k2",
      b: [["",             40,  40, 667, 215],
          ["Berru Park",  707,  40, 253, 620],
          ["Madame Coco",  40, 255, 218, 291],
          ["",             40, 546, 359, 114]],
      p: [],
      o: [[258, 255, 313, 142, "yurumerdiven"], [399, 397, 172, 263, "cekirdek"]],
      i: [["wc", 485, 460, ""], ["asansor", 485, 535, ""], ["merdiven", 485, 605, ""],
          ["ofis", 485, 640, "Yönetim Ofisi"]] },

    { ad: "3. Kat", kod: "k3",
      b: [["Defne Cafe",       40,  40, 214, 190],
          ["Chocolate Lounge",746,  40, 214, 190],
          ["",                 45, 250, 201, 292],
          ["",                246, 542, 171, 118],
          ["Popeyes",         571, 411, 188, 107],
          ["Burger King",     759, 250, 201, 245],
          ["",                660, 542, 300, 118]],
      p: [],
      t: [[254, 40, 492, 190]],
      o: [[246, 250, 325, 149, "yurumerdiven"], [417, 399, 154, 261, "cekirdek"]],
      i: [["wc", 494, 470, ""], ["asansor", 494, 545, ""], ["merdiven", 494, 615, ""]] },
  ];

  var ISARET = {
    giris:    { r: "#e11f26", s: "M12 20V7M6 12l6-6 6 6" },
    otopark:  { r: "#3c3a37", s: "M9 18V6h4a4 4 0 010 8H9" },
    konut:    { r: "#3c3a37", s: "M4 12l8-7 8 7M6 11v8h12v-8" },
    wc:       { r: "#1580c4", s: "M5 6v12M5 12h5M13 6l3 12 3-12" },
    asansor:  { r: "#5a5a61", s: "M7 4h10v16H7zM12 8l-2 2h4zM12 16l-2-2h4z" },
    merdiven: { r: "#5a5a61", s: "M4 20v-4h4v-4h4V8h4V4h4" },
    ofis:     { r: "#5a5a61", s: "M4 20V9l8-5 8 5v11M10 20v-6h4v6" }
  };
    var ETIKET = { wc: "WC", asansor: "Asansör", merdiven: "Merdiven",
                 yurumerdiven: "Yürüyen merdiven" };

  function ikon(g, tur, x, y, olcek) {
    var d = ISARET[tur]; if (!d) return;
    var k = el("g", { transform: "translate(" + (x-12*olcek) + "," + (y-12*olcek) +
                      ") scale(" + olcek + ")" }, g);
    el("path", { d: d.s, fill: "none", stroke: d.r, "stroke-width": 2,
                 "stroke-linecap": "round", "stroke-linejoin": "round" }, k);
  }

  function katCiz(kat) {
    var svg = el("svg", { viewBox: "0 0 1000 700", role: "img",
      "aria-label": T(kat.ad) + " " + T("kat planı") });

    el("rect", { x: 0, y: 0, width: 1000, height: 700, fill: "#fbfaf8" }, svg);

    // teras (açık alan)
    (kat.t || []).forEach(function (t) {
      el("rect", { x: t[0], y: t[1], width: t[2], height: t[3], rx: 3,
        fill: "#eaf0e6", stroke: "#c3d2b8", "stroke-dasharray": "6 4" }, svg);
      var y = el("text", { x: t[0]+t[2]/2, y: t[1]+t[3]/2+5, "text-anchor": "middle",
        class: "pa-kp-ortak" }, svg);
      y.textContent = T("Açık teras");
    });

    // ortak alanlar
    (kat.o || []).forEach(function (o) {
      el("rect", { x: o[0], y: o[1], width: o[2], height: o[3], rx: 3,
        fill: "#eef1f4", stroke: "#cfd7df", "stroke-width": 1.2 }, svg);
      if (o[4] === "yurumerdiven") {
        var mx = o[0]+o[2]/2, my = o[1]+o[3]/2;
        for (var i = 0; i < 2; i++) {
          var bx = mx - 62 + i*64;
          el("rect", { x: bx, y: my-26, width: 58, height: 52, rx: 2,
            fill: "#fff", stroke: "#c3ccd6" }, svg);
          for (var j = 0; j < 7; j++)
            el("path", { d: "M" + (bx+5) + " " + (my-20+j*7) + " h48",
              stroke: "#c3ccd6", "stroke-width": 1.4 }, svg);
        }
        var e = el("text", { x: mx, y: my+44, "text-anchor": "middle", class: "pa-kp-ortak" }, svg);
        e.textContent = T("Yürüyen merdiven");
      }
    });

    // birimler
    function birim(ad, x, y, en, boy) {
      var bos = !ad;
      el("rect", { x: x, y: y, width: en, height: boy, rx: 3,
        fill: bos ? "#eceae7" : "#fff",
        stroke: bos ? "#dcd8d3" : "#2b2b2e",
        "stroke-width": bos ? 1 : 1.6 }, svg);
      if (bos) return;
      var t = el("text", { x: x+en/2, y: y+boy/2, "text-anchor": "middle",
        class: "pa-kp-ad" }, svg);
      var kelime = ad.split(" "), satir = [], gecici = "";
      kelime.forEach(function (k) {
        if ((gecici + " " + k).trim().length * 8.4 > en - 16 && gecici) {
          satir.push(gecici); gecici = k;
        } else gecici = (gecici + " " + k).trim();
      });
      if (gecici) satir.push(gecici);
      satir.forEach(function (s, i) {
        var ts = el("tspan", { x: x+en/2, dy: i === 0 ? -(satir.length-1)*8 : 17 }, t);
        ts.textContent = s;
      });
    }
    (kat.b || []).forEach(function (b) { birim(b[0], b[1], b[2], b[3], b[4]); });
    (kat.p || []).forEach(function (p) {
      el("polygon", { points: p[1], fill: "#fff", stroke: "#2b2b2e", "stroke-width": 1.6 }, svg);
      // L biçimli birimde ağırlık merkezi çentiğe düşüyor; konum elle veriliyor
      var cx = p[2], cy = p[3];
      if (cx == null) {
        var n = p[1].split(" ").map(function (c) { return c.split(",").map(Number); });
        cx = n.reduce(function (a, c) { return a + c[0]; }, 0) / n.length;
        cy = n.reduce(function (a, c) { return a + c[1]; }, 0) / n.length;
      }
      var t = el("text", { x: cx, y: cy, "text-anchor": "middle", class: "pa-kp-ad" }, svg);
      t.textContent = T(p[0]);
    });

    // çekirdek içi işaretler ve girişler
    (kat.i || []).forEach(function (o) {
      var tur = o[0], x = o[1], y = o[2], etiket = o[3] || ETIKET[tur] || "";
      var giris = tur === "giris" || tur === "otopark" || tur === "konut";
      if (giris) {
        el("circle", { cx: x, cy: y, r: 15, fill: "#fff",
          stroke: ISARET[tur].r, "stroke-width": 2 }, svg);
        ikon(svg, tur, x, y, .8);
        // alt kenardaki girişlerin etiketi yukarıda, üsttekilerin aşağıda dursun
        var t = el("text", { x: x, y: y + (y > 350 ? -24 : 32), "text-anchor": "middle",
          class: "pa-kp-giris" }, svg);
        t.textContent = T(etiket);
      } else {
        ikon(svg, tur, x - 26, y, .75);
        var t2 = el("text", { x: x - 10, y: y + 5, class: "pa-kp-ic" }, svg);
        t2.textContent = T(etiket);
      }
    });
    return svg;
  }

  function kur() {
    var hedef = document.querySelector("[data-pa-kat3d]");
    if (!hedef || hedef.dataset.paKp === "1") return;
    hedef.dataset.paKp = "1";
    hedef.innerHTML = "";

    var sekme = document.createElement("div");
    sekme.className = "pa-kp-sekmeler";
    var tuval = document.createElement("div");
    tuval.className = "pa-kp-tuval";

    var aktif = 0, dugmeler = [];
    function goster(i) {
      aktif = i;
      dugmeler.forEach(function (d, j) { d.classList.toggle("secili", i === j); });
      tuval.innerHTML = "";
      tuval.appendChild(katCiz(KATLAR[i]));
    }
    KATLAR.forEach(function (k, i) {
      var d = document.createElement("button");
      d.type = "button"; d.className = "pa-kp-sekme"; d.textContent = T(k.ad);
      d.addEventListener("click", function () { goster(i); });
      sekme.appendChild(d); dugmeler.push(d);
    });

    var lejant = document.createElement("ul");
    lejant.className = "pa-kp-lejant";
    [["giris", "AVM Ana Girişi"], ["wc", "WC"], ["asansor", "Asansör"],
     ["merdiven", "Merdiven"], ["otopark", "Otopark"]].forEach(function (o) {
      var li = document.createElement("li");
      var s = el("svg", { viewBox: "0 0 24 24", class: "pa-kp-lejant-ikon" });
      el("path", { d: ISARET[o[0]].s, fill: "none", stroke: ISARET[o[0]].r,
        "stroke-width": 2, "stroke-linecap": "round", "stroke-linejoin": "round" }, s);
      li.appendChild(s);
      li.appendChild(document.createTextNode(T(o[1])));
      lejant.appendChild(li);
    });

    hedef.appendChild(sekme);
    hedef.appendChild(tuval);
    hedef.appendChild(lejant);
    goster(0);
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", kur);
  else kur();
})();
