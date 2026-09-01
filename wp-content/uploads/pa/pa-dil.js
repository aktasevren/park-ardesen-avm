/* ============================================================
   Dil katmanı — çalışma anında üretilen metinler
   ------------------------------------------------------------
   Statik sayfa metinleri derleme sırasında çevriliyor (_dil/uret.py).
   Bu dosya, JavaScript'in tarayıcıda ürettiği metinleri (ay adları,
   kat adları, tesis etiketleri, durum rozetleri…) ve panelden girilen
   içerikleri çok dilli hâle getirir.

   paT(tr)      → arayüz metnini aktif dile çevirir
   paMetin(v)   → panel değerini çözer: düz metin ya da {tr,en,ka,ar}
                  nesnesi olabilir; seçilen dil boşsa Türkçesi gösterilir
   ============================================================ */
(function (w) {
  "use strict";

  function aktifDil() {
    var m = document.querySelector('meta[name="pa-dil"]');
    if (m && m.content) return m.content;
    var l = (document.documentElement.lang || "tr").slice(0, 2).toLowerCase();
    return ["tr", "en", "ka", "ar"].indexOf(l) >= 0 ? l : "tr";
  }

  var DIL = aktifDil();

  /* Arayüz sözlüğü: Türkçe metin → diğer diller */
  var S = {
    "Yürüyen merdiven": ["Escalator", "ესკალატორი", "السلم الكهربائي"],
    "Açık teras":        ["Open terrace", "ღია ტერასა", "تراس مفتوح"],
    "AVM Ana Girişi":    ["Main Entrance", "მთავარი შესასვლელი", "المدخل الرئيسي"],
    "Otopark Girişi":    ["Car Park Entrance", "ავტოსადგომის შესასვლელი", "مدخل المواقف"],
    "Konut Girişi":      ["Residence Entrance", "საცხოვრებლის შესასვლელი", "مدخل السكن"],
    "Merdiven":          ["Stairs", "კიბე", "الدرج"],
    "Yönetim Ofisi":     ["Management Office", "ადმინისტრაციის ოფისი", "مكتب الإدارة"],
    "Otopark":           ["Car Park", "ავტოსადგომი", "مواقف السيارات"],
    "kat planı":         ["floor plan", "სართულის გეგმა", "مخطط الطابق"],
    // aylar
    "Ocak":    ["January", "იანვარი", "يناير"],
    "Şubat":   ["February", "თებერვალი", "فبراير"],
    "Mart":    ["March", "მარტი", "مارس"],
    "Nisan":   ["April", "აპრილი", "أبريل"],
    "Mayıs":   ["May", "მაისი", "مايو"],
    "Haziran": ["June", "ივნისი", "يونيو"],
    "Temmuz":  ["July", "ივლისი", "يوليو"],
    "Ağustos": ["August", "აგვისტო", "أغسطس"],
    "Eylül":   ["September", "სექტემბერი", "سبتمبر"],
    "Ekim":    ["October", "ოქტომბერი", "أكتوبر"],
    "Kasım":   ["November", "ნოემბერი", "نوفمبر"],
    "Aralık":  ["December", "დეკემბერი", "ديسمبر"],

    // kat adları
    "Zemin Kat":  ["Ground Floor", "პირველი სართული", "الطابق الأرضي"],
    "Bodrum Kat": ["Basement", "სარდაფი", "الطابق السفلي"],
    "1. Kat":     ["1st Floor", "მე-2 სართული", "الطابق الأول"],
    "2. Kat":     ["2nd Floor", "მე-3 სართული", "الطابق الثاني"],
    "3. Kat":     ["3rd Floor", "მე-4 სართული", "الطابق الثالث"],
    "Diğer":      ["Other", "სხვა", "أخرى"],

    // tesis etiketleri (kat planı)
    "GİRİŞ":   ["ENTRANCE", "შესასვლელი", "المدخل"],
    "WC":      ["WC", "საპირფარეშო", "دورة المياه"],
    "DANIŞMA": ["INFORMATION", "ინფორმაცია", "الاستعلامات"],
    "MESCİT":  ["PRAYER ROOM", "სამლოცველო", "مصلّى"],
    "ASANSÖR": ["LIFT", "ლიფტი", "المصعد"],
    "ATM":     ["ATM", "ბანკომატი", "صرّاف آلي"],

    // kiralama durumları
    "Boş":     ["Available", "თავისუფალი", "متاح"],
    "Rezerve": ["Reserved", "დაჯავშნილი", "محجوز"],
    "Dolu":    ["Occupied", "დაკავებული", "مشغول"],

    // duyuru türleri
    "Çalışma saati":     ["Opening hours", "სამუშაო საათები", "ساعات العمل"],
    "Yeni mağaza":       ["New store", "ახალი მაღაზია", "متجر جديد"],
    "Yakında":           ["Coming soon", "მალე", "قريبًا"],
    "Etkinlik":          ["Event", "ღონისძიება", "فعالية"],
    "Çekiliş":           ["Prize draw", "გათამაშება", "سحب جوائز"],
    "Kampanya":          ["Campaign", "აქცია", "عرض"],
    "Yeni hizmet":       ["New service", "ახალი სერვისი", "خدمة جديدة"],
    "Bakım":             ["Maintenance", "სარემონტო სამუშაოები", "أعمال صيانة"],
    "Ulaşım":            ["Getting here", "ტრანსპორტი", "الوصول"],
    "Sosyal sorumluluk": ["Social responsibility", "სოციალური პასუხისმგებლობა", "المسؤولية الاجتماعية"],
    "Acil duyuru":       ["Urgent notice", "გადაუდებელი შეტყობინება", "إشعار عاجل"],

    // düğme / etiket
    "Detay":          ["Details", "დეტალები", "التفاصيل"],
    "Duyuruyu kapat": ["Close announcement", "განცხადების დახურვა", "إغلاق الإعلان"],
    "Kapat":          ["Close", "დახურვა", "إغلاق"],
    "Tümü":           ["All", "ყველა", "الكل"],
    "Kat":            ["Floor", "სართული", "الطابق"],
    "Kategori":       ["Category", "კატეგორია", "الفئة"],

    // --- boş durum ve şema metinleri (pa-veri.js) ---
    "Şu anda yayımlanmış bir duyuru bulunmuyor.":
      ["There are no published announcements at the moment.",
       "ამჟამად გამოქვეყნებული განცხადება არ არის.",
       "لا توجد إعلانات منشورة في الوقت الحالي."],
    "Şu anda yayımlanmış bir kampanya bulunmuyor.":
      ["There are no published campaigns at the moment.",
       "ამჟამად გამოქვეყნებული აქცია არ არის.",
       "لا توجد عروض منشورة في الوقت الحالي."],
    "Şu anda yayımlanmış boş birim bulunmuyor.":
      ["There are no available units published at the moment.",
       "ამჟამად გამოქვეყნებული თავისუფალი ერთეული არ არის.",
       "لا توجد وحدات شاغرة منشورة في الوقت الحالي."],
    "Fırsat Günleri şu anda yayında değil.":
      ["Deal Days are not running at the moment.",
       "ფასდაკლების დღეები ამჟამად არ მიმდინარეობს.",
       "أيام العروض غير مفعّلة حاليًا."],
    "Kat şeması": ["Floor diagram", "სართულის სქემა", "رسم الطوابق"],
    "Çizim yönlendirme amaçlı şematiktir; birimlerin":
      ["The drawing is schematic and for orientation only; the actual layout and dimensions of the units",
       "ნახაზი სქემატურია და მხოლოდ ორიენტაციისთვისაა; ერთეულების ფაქტობრივი განლაგება და ზომები",
       "الرسم تخطيطي لأغراض التوجيه فقط؛ والتوزيع الفعلي للوحدات وأبعادها"],
    "gerçek yerleşimi ve ölçüleri farklıdır. Kırmızı bant yürüyen merdiveni":
      ["differ. The red band marks the escalator",
       "განსხვავდება. წითელი ზოლი აღნიშნავს ესკალატორს",
       "يختلف. ويشير الشريط الأحمر إلى السلّم المتحرّك"],
    "gösterir.": [".", ".", "."],

    // --- mağaza kategorileri (veri.json) ---
    "Moda & Giyim":      ["Fashion & Clothing", "მოდა და ტანსაცმელი", "الأزياء والملابس"],
    "Ayakkabı & Çanta":  ["Shoes & Bags", "ფეხსაცმელი და ჩანთები", "الأحذية والحقائب"],
    "Ev & Yaşam":        ["Home & Living", "სახლი და ცხოვრება", "المنزل والمعيشة"],
    "Kozmetik & Parfüm": ["Cosmetics & Perfume", "კოსმეტიკა და პარფიუმერია", "مستحضرات التجميل والعطور"],
    "Market":            ["Supermarket", "სუპერმარკეტი", "سوبر ماركت"],
    "Yeme & İçme":       ["Food & Drink", "კვება და სასმელი", "المأكولات والمشروبات"],
    "Eğlence & Çocuk":   ["Entertainment & Kids", "გართობა და ბავშვები", "الترفيه والأطفال"],
    "Hizmet":            ["Service", "მომსახურება", "خدمات"],

    // --- çerez bandı ve ayarlar (pa-cerez.js) ---
    "Çerezleri kullanıyoruz": ["We use cookies", "ჩვენ ვიყენებთ ქუქი-ფაილებს", "نستخدم ملفات تعريف الارتباط"],
    "Sitenin düzgün çalışması için zorunlu çerezleri kullanıyoruz.":
      ["We use essential cookies so the site works properly.",
       "ვიყენებთ აუცილებელ ქუქი-ფაილებს საიტის გამართული მუშაობისთვის.",
       "نستخدم ملفات ارتباط ضرورية ليعمل الموقع بشكل سليم."],
    "Tercih, ölçümleme ve pazarlama çerezleri yalnızca siz izin verirseniz":
      ["Preference, analytics and marketing cookies run only if you allow them",
       "პარამეტრების, ანალიტიკისა და მარკეტინგის ქუქი-ფაილები მუშაობს მხოლოდ თქვენი ნებართვით",
       "ولا تعمل ملفات التفضيلات والتحليلات والتسويق إلا بموافقتكم"],
    "çalışır. Ayrıntılar için": [". For details see", ". დეტალებისთვის იხილეთ", ". وللتفاصيل راجعوا"],
    "KVKK Aydınlatma Metni sayfamıza bakabilirsiniz.":
      ["our Data Protection Notice page.", "მონაცემთა დაცვის შეტყობინების გვერდი.", "صفحة إشعار حماية البيانات."],
    "Tümünü kabul et": ["Accept all", "ყველას მიღება", "قبول الكل"],
    "Tümünü reddet": ["Reject all", "ყველას უარყოფა", "رفض الكل"],
    "Çerez ayarları": ["Cookie settings", "ქუქი-ფაილების პარამეტრები", "إعدادات ملفات الارتباط"],
    "Çerez Ayarları": ["Cookie Settings", "ქუქი-ფაილების პარამეტრები", "إعدادات ملفات الارتباط"],
    "Çerez tercihleri": ["Cookie preferences", "ქუქი-ფაილების პარამეტრები", "تفضيلات ملفات الارتباط"],
    "Hangi çerezlere izin verdiğinizi buradan":
      ["You can choose here which cookies you allow", "აქ შეგიძლიათ აირჩიოთ, რომელ ქუქი-ფაილებს დაუშვებთ", "يمكنكم اختيار ملفات الارتباط التي تسمحون بها من هنا"],
    "seçebilirsiniz. Tercihinizi istediğiniz zaman değiştirebilir ya da":
      [". You can change your preference at any time or", ". თქვენი არჩევანი ნებისმიერ დროს შეგიძლიათ შეცვალოთ ან", "؛ ويمكنكم تغيير تفضيلاتكم في أي وقت أو"],
    "Zorunlu çerezler": ["Essential cookies", "აუცილებელი ქუქი-ფაილები", "ملفات الارتباط الضرورية"],
    "(her zaman açık)": ["(always on)", "(ყოველთვის ჩართული)", "(مفعّلة دائمًا)"],
    "Sitenin çalışması için gereklidir: çerez tercihinizin":
      ["Required for the site to work: remembering your cookie preference",
       "საჭიროა საიტის მუშაობისთვის: თქვენი არჩევანის დამახსოვრება",
       "لازمة لعمل الموقع: تذكّر تفضيلكم بشأن ملفات الارتباط"],
    "hatırlanması ve yönetim paneli oturumu. Kapatılamaz.":
      ["and the management panel session. Cannot be switched off.",
       "და მართვის პანელის სესია. გამორთვა შეუძლებელია.",
       "وجلسة لوحة الإدارة. ولا يمكن تعطيلها."],
    "Tercih çerezleri": ["Preference cookies", "პარამეტრების ქუქი-ფაილები", "ملفات ارتباط التفضيلات"],
    "Kapattığınız duyuru bandı gibi tercihlerinizi hatırlar.":
      ["Remembers your preferences, such as an announcement bar you closed.",
       " იმახსოვრებს თქვენს არჩევანს, მაგალითად დახურულ საინფორმაციო ზოლს.",
       "تتذكّر تفضيلاتكم، مثل شريط إعلان أغلقتموه."],
    "Ölçümleme çerezleri": ["Analytics cookies", "ანალიტიკური ქუქი-ფაილები", "ملفات ارتباط التحليلات"],
    "Sayfaların ne kadar ziyaret edildiğini anonim olarak ölçer.":
      ["Measures anonymously how often pages are visited.",
       "ანონიმურადზომავს გვერდების მონახულების სიხშირეს.",
       "تقيس بشكل مجهول عدد زيارات الصفحات."],
    "Şu anda sitede ölçümleme aracı kullanılmıyor.":
      ["No analytics tool is currently used on the site.",
       "ამჟამად საიტზე ანალიტიკური ხელსაწყო არ გამოიყენება.",
       "لا تُستخدم حاليًا أي أداة تحليلات في الموقع."],
    "Pazarlama çerezleri": ["Marketing cookies", "მარკეტინგული ქუქი-ფაილები", "ملفات ارتباط التسويق"],
    "İlgi alanlarınıza göre reklam gösterimi için kullanılır.":
      ["Used to show advertising based on your interests.",
       "გამოიყენება თქვენი ინტერესების მიხედვით რეკლამის საჩვენებლად.",
       "تُستخدم لعرض إعلانات بحسب اهتماماتكم."],
    "Şu anda sitede pazarlama aracı kullanılmıyor.":
      ["No marketing tool is currently used on the site.",
       "ამჟამად საიტზე მარკეტინგული ხელსაწყო არ გამოიყენება.",
       "لا تُستخدم حاليًا أي أداة تسويق في الموقع."],
    "Seçimimi kaydet": ["Save my choice", "ჩემი არჩევანის შენახვა", "حفظ اختياري"],
    "Park Ardeşen AVM konumu": ["Park Ardeşen AVM location", "Park Ardeşen AVM-ის მდებარეობა", "موقع بارك أرديشن مول"],
    "Gizlilik Politikası ve": ["Privacy Policy and", "კონფიდენციალურობის პოლიტიკა და", "سياسة الخصوصية و"],

    // --- çerez bandı gövdesi (tek metin düğümü hâlinde) ---
    "Sitenin düzgün çalışması için zorunlu çerezleri kullanıyoruz. Tercih, ölçümleme ve pazarlama çerezleri yalnızca siz izin verirseniz çalışır. Ayrıntılar için":
      ["We use essential cookies so the site works properly. Preference, analytics and marketing cookies run only if you allow them. For details see",
       "ვიყენებთ აუცილებელ ქუქი-ფაილებს საიტის გამართული მუშაობისთვის. პარამეტრების, ანალიტიკისა და მარკეტინგის ქუქი-ფაილები მუშაობს მხოლოდ თქვენი ნებართვით. დეტალებისთვის იხილეთ",
       "نستخدم ملفات ارتباط ضرورية ليعمل الموقع بشكل سليم. ولا تعمل ملفات التفضيلات والتحليلات والتسويق إلا بموافقتكم. وللتفاصيل راجعوا"],
    "Gizlilik Politikası ve KVKK Aydınlatma Metni":
      ["Privacy Policy and Data Protection Notice",
       "კონფიდენციალურობის პოლიტიკა და მონაცემთა დაცვის შეტყობინება",
       "سياسة الخصوصية وإشعار حماية البيانات"],
    "sayfamıza bakabilirsiniz.": ["page.", "გვერდი.", "صفحتنا."],

    // --- kat planı ---
    "AVM Girişi": ["Mall Entrance", "ცენტრის შესასვლელი", "مدخل المركز"],
    "Danışma": ["Information", "ინფორმაცია", "الاستعلامات"],
    "Mescit": ["Prayer Room", "სამლოცველო", "مصلّى"],
    "Asansör": ["Lift", "ლიფტი", "المصعد"],
    "Çizim yönlendirme amaçlı şematiktir; birimlerin gerçek yerleşimi ve ölçüleri farklıdır. Kırmızı bant yürüyen merdiveni gösterir.":
      ["The drawing is schematic and for orientation only; the actual layout and dimensions of the units differ. The red band marks the escalator.",
       "ნახაზი სქემატურია და მხოლოდ ორიენტაციისთვისაა; ერთეულების ფაქტობრივი განლაგება და ზომები განსხვავდება. წითელი ზოლი აღნიშნავს ესკალატორს.",
       "الرسم تخطيطي لأغراض التوجيه فقط؛ والتوزيع الفعلي للوحدات وأبعادها يختلف. ويشير الشريط الأحمر إلى السلّم المتحرّك."],

    "Kabul et": ["Accept", "მიღება", "قبول"],
    "Reddet": ["Reject", "უარყოფა", "رفض"],
    "Ayarlar": ["Settings", "პარამეტრები", "الإعدادات"],
    "m²":             ["m²", "მ²", "م²"]
  };

  var SIRA = { en: 0, ka: 1, ar: 2 };

  function paT(tr) {
    if (DIL === "tr") return tr;
    var s = S[tr];
    if (s) return s[SIRA[DIL]] || tr;
    var t = String(tr);
    // "Z-05 · Ayakkabı & Çanta" — yalnız kategori çevrilir
    var p = t.split(" · ");
    if (p.length === 2 && S[p[1]]) return p[0] + " · " + paT(p[1]);
    // "Ayakkabı & Çanta (1)" — sayaç eki korunur
    var m = t.match(/^(.+?)\s*(\(\d+\))$/);
    if (m && S[m[1]]) return paT(m[1]) + " " + m[2];
    return tr;                               // sözlükte yoksa Türkçesi kalır
  }

  /* Panelden girilen değer: düz metin veya {tr,en,ka,ar}.
     Seçilen dil boşsa Türkçesine, o da yoksa ilk dolu değere düşer. */
  function paMetin(v) {
    if (v == null) return "";
    if (typeof v === "string" || typeof v === "number") return String(v);
    if (typeof v !== "object") return "";
    if (v[DIL]) return String(v[DIL]);
    if (v.tr) return String(v.tr);
    for (var k in v) { if (v[k]) return String(v[k]); }
    return "";
  }

  /* Bir öğenin altındaki metin düğümlerini sözlükten çevirir.
     Çerez bandı gibi, HTML şablonu içinde metin taşıyan bileşenler için. */
  function paCevirDom(kok) {
    if (DIL === "tr" || !kok) return;
    var yur = document.createTreeWalker(kok, NodeFilter.SHOW_TEXT, null);
    var n, dugumler = [];
    while ((n = yur.nextNode())) dugumler.push(n);
    dugumler.forEach(function (d) {
      var t = (d.nodeValue || "").trim();
      if (!t) return;
      var y = paT(t);
      if (y !== t) d.nodeValue = d.nodeValue.replace(t, y);
    });
    // çevrilebilir öznitelikler
    ["aria-label", "title", "placeholder"].forEach(function (oz) {
      var ler = kok.querySelectorAll ? kok.querySelectorAll("[" + oz + "]") : [];
      Array.prototype.forEach.call(ler, function (e) {
        var t = e.getAttribute(oz), y = paT(t);
        if (y !== t) e.setAttribute(oz, y);
      });
    });
  }

  /* Çerez bandı, duyuru şeridi, kat planı gibi bileşenler sayfaya sonradan
     ekleniyor. Eklenen düğümleri izleyip sözlükteki metinleri çeviriyoruz.
     Sözlükte yalnızca bilinen Türkçe metinler olduğu için başka içeriğe
     dokunulmuyor; Türkçe sürümde ise gözlemci hiç çalışmıyor. */
  function gozlemciyiKur() {
    if (DIL === "tr") return;
    paCevirDom(document.body);
    new MutationObserver(function (kayitlar) {
      kayitlar.forEach(function (k) {
        Array.prototype.forEach.call(k.addedNodes, function (d) {
          if (d.nodeType === 1) paCevirDom(d);
          else if (d.nodeType === 3) {
            var t = (d.nodeValue || "").trim();
            if (t) {
              var y = paT(t);
              if (y !== t) d.nodeValue = d.nodeValue.replace(t, y);
            }
          }
        });
      });
    }).observe(document.documentElement, { childList: true, subtree: true });
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", gozlemciyiKur);
  else gozlemciyiKur();

  w.paCevirDom = paCevirDom;
  w.paDil = DIL;
  w.paT = paT;
  w.paMetin = paMetin;
})(window);
