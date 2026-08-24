/* ------------------------------------------------------------------
   POST /api/kaydet   —  panelden gelen veriyi yayımlar

   Panel, düzenlenen JSON'u buraya gönderir; bu fonksiyon dosyayı
   GitHub'daki `panel/veri.json` üzerine commit'ler. Vercel deposu
   izlediği için yeni dağıtım kendiliğinden başlar (~1 dk).

   Gerekli ortam değişkenleri (Vercel → Settings → Environment Variables):
     PANEL_SIFRE   panelin giriş şifresiyle aynı olmalı
     GITHUB_TOKEN  depoya yazma yetkisi olan kişisel erişim jetonu
     GITHUB_REPO   "kullanici/depo" (varsayılan: aktasevren/park-ardesen-avm)
     GITHUB_DAL    hedef dal (varsayılan: main)
   ------------------------------------------------------------------ */
const DOSYA = "panel/veri.json";

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ hata: "Yalnızca POST" });
  }

  const { PANEL_SIFRE, GITHUB_TOKEN } = process.env;
  const depo = process.env.GITHUB_REPO || "aktasevren/park-ardesen-avm";
  const dal = process.env.GITHUB_DAL || "main";

  if (!PANEL_SIFRE || !GITHUB_TOKEN) {
    return res.status(500).json({
      hata: "Sunucu yapılandırılmamış: PANEL_SIFRE ve GITHUB_TOKEN tanımlı değil."
    });
  }

  let govde = req.body;
  if (typeof govde === "string") {
    try { govde = JSON.parse(govde); } catch (e) {
      return res.status(400).json({ hata: "Geçersiz JSON" });
    }
  }
  if (!govde || govde.sifre !== PANEL_SIFRE) {
    return res.status(401).json({ hata: "Şifre hatalı" });
  }
  if (!govde.veri || typeof govde.veri !== "object") {
    return res.status(400).json({ hata: "Veri eksik" });
  }

  const icerik = JSON.stringify(govde.veri, null, 2) + "\n";
  const b64 = Buffer.from(icerik, "utf8").toString("base64");
  const url = `https://api.github.com/repos/${depo}/contents/${DOSYA}`;
  const baslik = {
    Authorization: `Bearer ${GITHUB_TOKEN}`,
    Accept: "application/vnd.github+json",
    "User-Agent": "park-ardesen-panel",
    "X-GitHub-Api-Version": "2022-11-28"
  };

  try {
    // mevcut dosyanın sha'sı (yoksa ilk kez oluşturulur)
    let sha;
    const mevcut = await fetch(`${url}?ref=${encodeURIComponent(dal)}`, { headers: baslik });
    if (mevcut.ok) {
      sha = (await mevcut.json()).sha;
    } else if (mevcut.status !== 404) {
      const m = await mevcut.text();
      return res.status(502).json({ hata: `GitHub okunamadı (${mevcut.status}): ${m.slice(0, 200)}` });
    }

    const zaman = new Date().toISOString().replace("T", " ").slice(0, 16);
    const yaz = await fetch(url, {
      method: "PUT",
      headers: { ...baslik, "Content-Type": "application/json" },
      body: JSON.stringify({
        message: `Panel: site içeriği güncellendi (${zaman})`,
        content: b64,
        branch: dal,
        ...(sha ? { sha } : {})
      })
    });

    if (!yaz.ok) {
      const m = await yaz.text();
      return res.status(502).json({ hata: `GitHub'a yazılamadı (${yaz.status}): ${m.slice(0, 200)}` });
    }

    const sonuc = await yaz.json();
    return res.status(200).json({
      tamam: true,
      commit: sonuc.commit && sonuc.commit.sha ? sonuc.commit.sha.slice(0, 7) : null
    });
  } catch (e) {
    return res.status(500).json({ hata: e.message });
  }
};
