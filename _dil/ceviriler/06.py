import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ekle import ekle
K = lambda t: {"en": t, "ka": t, "ar": t}
# Kat/mağaza numaraları: yalnız kategori adı çevrilir, numara aynı kalır
KAT = {"Zemin Kat": ("Ground Floor", "პირველი სართული", "الطابق الأرضي"),
       "1. Kat": ("1st Floor", "მე-2 სართული", "الطابق الأول"),
       "2. Kat": ("2nd Floor", "მე-3 სართული", "الطابق الثاني")}
KAT_KATEGORI = {
 "Market": ("Supermarket", "სუპერმარკეტი", "سوبر ماركت"),
 "Moda & Giyim": ("Fashion & Clothing", "მოდა და ტანსაცმელი", "الأزياء والملابس"),
 "Ayakkabı & Çanta": ("Shoes & Bags", "ფეხსაცმელი და ჩანთები", "الأحذية والحقائب"),
 "Kozmetik & Parfüm": ("Cosmetics & Perfume", "კოსმეტიკა და პარფიუმერია", "مستحضرات التجميل والعطور"),
 "Yeme & İçme": ("Food & Drink", "კვება და სასმელი", "المأكولات والمشروبات"),
 "Hizmet": ("Service", "მომსახურება", "خدمات"),
 "Ev & Yaşam": ("Home & Living", "სახლი და ცხოვრება", "المنزل والمعيشة"),
 "Eğlence & Çocuk": ("Entertainment & Kids", "გართობა და ბავშვები", "الترفيه والأطفال"),
}
v = {}
# "Z-00 · Market" biçimindekiler
for no_on, kats in (("Z-00","Market"),("Z-01","Moda & Giyim"),("Z-05","Ayakkabı & Çanta"),
                    ("Z-08","Kozmetik & Parfüm"),("Z-12","Yeme & İçme"),("Z-20","Hizmet"),
                    ("1-02","Ev & Yaşam"),("1-04","Moda & Giyim"),("1-07","Moda & Giyim"),
                    ("1-11","Moda & Giyim"),("2-01","Yeme & İçme"),("2-02","Yeme & İçme"),
                    ("2-05","Yeme & İçme"),("2-08","Yeme & İçme"),("2-10","Yeme & İçme"),
                    ("2-15","Eğlence & Çocuk"),("2-20","Eğlence & Çocuk")):
    e, g, a = KAT_KATEGORI[kats]
    v["%s · %s" % (no_on, kats)] = {"en":"%s · %s"%(no_on,e), "ka":"%s · %s"%(no_on,g), "ar":"%s · %s"%(no_on,a)}
# "Zemin Kat · No: Z-01" biçimindekiler
for kat, no_on in (("Zemin Kat","Z-01"),("1. Kat","1-04"),("1. Kat","1-07"),("1. Kat","1-11"),
                   ("Zemin Kat","Z-05"),("1. Kat","1-02"),("Zemin Kat","Z-08"),("Zemin Kat","Z-00"),
                   ("2. Kat","2-01"),("2. Kat","2-02"),("2. Kat","2-05"),("2. Kat","2-08"),
                   ("2. Kat","2-10"),("Zemin Kat","Z-12"),("2. Kat","2-15"),("2. Kat","2-20"),
                   ("Zemin Kat","Z-20")):
    e, g, a = KAT[kat]
    v["%s · No: %s" % (kat, no_on)] = {"en":"%s · No: %s"%(e,no_on), "ka":"%s · №%s"%(g,no_on), "ar":"%s · رقم %s"%(a,no_on)}
for kat,(e,g,a) in KAT.items():
    v[kat] = {"en":e,"ka":g,"ar":a}
# kategori sayaçları
import json as _json
_mevcut = _json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sozluk.json"), encoding="utf-8"))
for kats,(e,g,a) in KAT_KATEGORI.items():
    for n in range(1,20):
        anahtar = "%s (%d)" % (kats, n)
        if anahtar in _mevcut:
            v[anahtar] = {"en":"%s (%d)"%(e,n), "ka":"%s (%d)"%(g,n), "ar":"%s (%d)"%(a,n)}
v.update({
 "Park Ardeşen AVM Kiralama Ekibi":{"en":"Park Ardeşen AVM Leasing Team","ka":"Park Ardeşen AVM-ის საიჯარო გუნდი","ar":"فريق التأجير في بارك أرديشن مول"},
 "Telefon: 0464 715 30 30":{"en":"Phone: 0464 715 30 30","ka":"ტელეფონი: 0464 715 30 30","ar":"الهاتف: 0464 715 30 30"},
 "Ardeşen'in en işlek caddesinde mağaza, kiosk":{"en":"Store, kiosk and advertising space leasing opportunities on Ardeşen's busiest street. See currently available units.","ka":"მაღაზიის, კიოსკისა და სარეკლამო ფართის იჯარის შესაძლებლობები არდეშენის ყველაზე მოძრავ ქუჩაზე. იხილეთ ამჟამად თავისუფალი ერთეულები.","ar":"فرص تأجير المتاجر والأكشاك والمساحات الإعلانية في أكثر شوارع أرديشن حركة. اطّلعوا على الوحدات المتاحة حاليًا."},
 "mailto:muhasebe@parkardesen.com": K("mailto:muhasebe@parkardesen.com"),
 "Kat Planı — Park Ardeşen AVM":{"en":"Floor Plan — Park Ardeşen AVM | Ardeşen, Rize","ka":"სართულის გეგმა — Park Ardeşen AVM | არდეშენი, რიზე","ar":"مخطط الطوابق — بارك أرديشن مول | أرديشن، ريزة"},
 "planı":{"en":"plan","ka":"გეგმა","ar":"المخطط"},
 "Mağaza Listesi":{"en":"Store List","ka":"მაღაზიების სია","ar":"قائمة المتاجر"},
 "Filtrele":{"en":"Filter","ka":"ფილტრი","ar":"تصفية"},
 "Tümü":{"en":"All","ka":"ყველა","ar":"الكل"},
 "Kat kat mağaza listesi":{"en":"Store list by floor","ka":"მაღაზიების სია სართულების მიხედვით","ar":"قائمة المتاجر حسب الطابق"},
 "Kat ve mağaza numaraları temsilidir":{"en":"Floor and store numbers are indicative; for the exact layout please ask at the mall information desk.","ka":"სართულებისა და მაღაზიების ნომრები საორიენტაციოა; ზუსტი განლაგებისთვის მიმართეთ ცენტრის საინფორმაციო სტენდს.","ar":"أرقام الطوابق والمتاجر إرشادية؛ وللتوزيع الدقيق يرجى السؤال في مكتب استعلامات المركز."},
 "Kat şeması":{"en":"Floor diagram","ka":"სართულის სქემა","ar":"رسم الطوابق"},
 "Park Ardeşen AVM kat planı. Zemin":{"en":"Park Ardeşen AVM floor plan. See the stores on the ground, first and second floors with their numbers and plan your visit.","ka":"Park Ardeşen AVM-ის სართულის გეგმა. იხილეთ მაღაზიები პირველ, მე-2 და მე-3 სართულზე ნომრებით და დაგეგმეთ ვიზიტი.","ar":"مخطط طوابق بارك أرديشن مول. اطّلعوا على متاجر الطابق الأرضي والأول والثاني بأرقامها وخطّطوا لزيارتكم."},
 "Mağaza ara":{"en":"Search stores","ka":"მაღაზიის ძებნა","ar":"ابحث عن متجر"},
 "Park Kart — Park Ardeşen AVM":{"en":"Park Card — Park Ardeşen AVM | Ardeşen, Rize","ka":"Park ბარათი — Park Ardeşen AVM | არდეშენი, რიზე","ar":"بطاقة بارك — بارك أرديشن مول | أرديشن، ريزة"},
 "Park Kart nedir?":{"en":"What is the Park Card?","ka":"რა არის Park ბარათი?","ar":"ما هي بطاقة بارك؟"},
 "Park Kart, Park Ardeşen AVM ziyaretçilerine":{"en":"The Park Card is a free discount card created for Park Ardeşen AVM visitors. It gives you extra discounts and privileges at participating stores.","ka":"Park ბარათი უფასო ფასდაკლების ბარათია Park Ardeşen AVM-ის სტუმრებისთვის. ის გაძლევთ დამატებით ფასდაკლებებსა და პრივილეგიებს მონაწილე მაღაზიებში.","ar":"بطاقة بارك بطاقة خصم مجانية أُعدّت لزوّار بارك أرديشن مول. وتمنحكم خصومات ومزايا إضافية في المتاجر المشاركة."},
 "Nasıl alınır?":{"en":"How do I get one?","ka":"როგორ მივიღო?","ar":"كيف أحصل عليها؟"},
 "Zemin kattaki danışma bankosuna uğramanız":{"en":"Just stop by the information desk on the ground floor. With your card you will also receive the list of participating stores valid that day.","ka":"საკმარისია ეწვიოთ პირველ სართულზე არსებულ საინფორმაციო სტენდს. ბარათთან ერთად მიიღებთ იმ დღეს მოქმედი მონაწილე მაღაზიების სიას.","ar":"يكفي أن تمرّوا بمكتب الاستعلامات في الطابق الأرضي. وستتسلّمون مع البطاقة قائمة المتاجر المشاركة السارية ذلك اليوم."},
 "Nerede geçerli?":{"en":"Where is it valid?","ka":"სად მოქმედებს?","ar":"أين تُقبل؟"},
 "Katılımcı mağaza listesi kampanya":{"en":"The list of participating stores changes with each campaign period. The current list is published at the information desk and on","ka":"მონაწილე მაღაზიების სია იცვლება აქციის პერიოდის მიხედვით. მიმდინარე სია ქვეყნდება საინფორმაციო სტენდზე და","ar":"تتغيّر قائمة المتاجر المشاركة بحسب فترة العرض. وتُنشر القائمة الحالية في مكتب الاستعلامات وعلى"},
 "Instagram hesabımızda":{"en":"our Instagram account","ka":"ჩვენს Instagram ანგარიშზე","ar":"حسابنا على إنستغرام"},
 "yayımlanır.":{"en":".","ka":".","ar":"."},
 "Ayrıntılı bilgi için:":{"en":"For more information:","ka":"დამატებითი ინფორმაციისთვის:","ar":"لمزيد من المعلومات:"},
 "Hizmetlerimiz — Park Ardeşen AVM":{"en":"Our Services — Park Ardeşen AVM | Ardeşen, Rize","ka":"ჩვენი სერვისები — Park Ardeşen AVM | არდეშენი, რიზე","ar":"خدماتنا — بارك أرديشن مول | أرديشن، ريزة"},
 "Park Ardeşen AVM'de alışverişinizi kolaylaştıran":{"en":"Below are the services that make your shopping easier and your visit more enjoyable at Park Ardeşen AVM.","ka":"ქვემოთ მოცემულია სერვისები, რომლებიც აადვილებს თქვენს შოპინგს და ვიზიტს უფრო სასიამოვნოს ხდის Park Ardeşen AVM-ში.","ar":"في ما يلي الخدمات التي تسهّل تسوّقكم وتجعل زيارتكم أكثر متعة في بارك أرديشن مول."},
 "Ücretsiz otopark, mescit, anne-bebek":{"en":"Free parking, a prayer room, a mother and baby room, accessible facilities, an ATM, first aid and more at Park Ardeşen AVM.","ka":"უფასო პარკინგი, სამლოცველო, დედისა და ბავშვის ოთახი, ადაპტირებული გარემო, ბანკომატი, პირველადი დახმარება და სხვა Park Ardeşen AVM-ში.","ar":"موقف مجاني ومصلّى وغرفة للأم والطفل ومرافق مهيّأة وصرّاف آلي وإسعافات أولية وغيرها في بارك أرديشن مول."},
 "Mağazalar — Park Ardeşen AVM":{"en":"Stores — Park Ardeşen AVM | Ardeşen, Rize","ka":"მაღაზიები — Park Ardeşen AVM | არდეშენი, რიზე","ar":"المتاجر — بارك أرديشن مول | أرديشن، ريزة"},
 "Mağaza":{"en":"Store","ka":"მაღაზიების","ar":"دليل"},
 "rehberi":{"en":"guide","ka":"გზამკვლევი","ar":"المتاجر"},
 "Aramanıza uygun mağaza bulunamadı.":{"en":"No store matched your search.","ka":"თქვენს ძიებას შესაბამისი მაღაზია ვერ მოიძებნა.","ar":"لم يُعثر على متجر يطابق بحثكم."},
 "Park Ardeşen AVM'deki tüm mağazalar":{"en":"All the stores at Park Ardeşen AVM: fashion, footwear, groceries, cosmetics, dining and entertainment. Search by floor and category.","ka":"ყველა მაღაზია Park Ardeşen AVM-ში: მოდა, ფეხსაცმელი, სასურსათო, კოსმეტიკა, კვება და გართობა. მოძებნეთ სართულისა და კატეგორიის მიხედვით.","ar":"جميع المتاجر في بارك أرديشن مول: أزياء وأحذية وبقالة ومستحضرات تجميل ومطاعم وترفيه. ابحثوا حسب الطابق والفئة."},
 "Ulaşım — Park Ardeşen AVM":{"en":"Getting Here — Park Ardeşen AVM | Ardeşen, Rize","ka":"როგორ მოვიდეთ — Park Ardeşen AVM | არდეშენი, რიზე","ar":"كيفية الوصول — بارك أرديشن مول | أرديشن، ريزة"},
 "Nerede?":{"en":"Where is it?","ka":"სად მდებარეობს?","ar":"أين يقع؟"},
 "Park Ardeşen AVM, Ardeşen ilçe merkezinde":{"en":"Park Ardeşen AVM is in the centre of Ardeşen, at Cumhuriyet Mahallesi Sultan Alparslan Caddesi No: 2/1.","ka":"Park Ardeşen AVM მდებარეობს არდეშენის ცენტრში, მისამართზე Cumhuriyet Mahallesi Sultan Alparslan Caddesi No: 2/1.","ar":"يقع بارك أرديشن مول في وسط أرديشن، في حي جمهوريت، شارع سلطان ألب أرسلان، رقم 2/1."},
 "Özel araçla":{"en":"By car","ka":"ავტომობილით","ar":"بالسيارة"},
 "Rize'den yaklaşık 50 km":{"en":"We are about 50 km from Rize, 20 km from Pazar, 15 km from Fındıklı and 20 km from Çamlıhemşin. Free parking is available.","ka":"ჩვენ ვიმყოფებით რიზედან დაახლოებით 50 კმ-ში, ფაზარიდან 20 კმ-ში, ფინდიკლიდან 15 კმ-ში და ჩამლიჰემშინიდან 20 კმ-ში. ხელმისაწვდომია უფასო პარკინგი.","ar":"نبعد نحو 50 كم عن ريزة، و20 كم عن بازار، و15 كم عن فيندكلي، و20 كم عن تشامليهمشين. ويتوفّر موقف مجاني."},
 "Toplu taşımayla":{"en":"By public transport","ka":"საზოგადოებრივი ტრანსპორტით","ar":"بالنقل العام"},
 "Ardeşen ilçe içi dolmuş hatları":{"en":"Minibus routes within Ardeşen and the coast road buses running between Rize and Hopa stop near our centre.","ka":"არდეშენის შიდა მიკროავტობუსების ხაზები და რიზე – ჰოფას სანაპირო გზის ავტობუსები ჩერდება ჩვენს ცენტრთან ახლოს.","ar":"تتوقّف بالقرب من مركزنا خطوط الميني باص داخل أرديشن وحافلات طريق الساحل بين ريزة وهوبا."},
 "Yakın çevre":{"en":"Nearby","ka":"სიახლოვეს","ar":"في الجوار"},
 "Ayder Yaylası, Çamlıhemşin, Fırtına":{"en":"You can take care of your needs before setting off for Ayder Plateau, Çamlıhemşin, the Fırtına Valley and the Zilkale route.","ka":"შეგიძლიათ საჭიროებები მოაგვაროთ Ayder-ის პლატოზე, ჩამლიჰემშინში, ფირთინას ხეობასა და ზილკალეს მარშრუტზე გამგზავრებამდე.","ar":"يمكنكم تلبية احتياجاتكم قبل الانطلاق إلى هضبة آيدر وتشامليهمشين ووادي فيرتينا ومسار زيلكاله."},
 "Sefer saatleri ve güncel ulaşım":{"en":"For timetables and up-to-date travel information:","ka":"განრიგისა და მიმდინარე სატრანსპორტო ინფორმაციისთვის:","ar":"لمواعيد الرحلات ومعلومات النقل المحدَّثة:"},
 "Park Ardeşen AVM'ye nasıl gidilir?":{"en":"How do I get to Park Ardeşen AVM? Black Sea coast road, minibus and bus routes, free parking.","ka":"როგორ მივიდეთ Park Ardeşen AVM-ში? შავი ზღვის სანაპირო გზა, მიკროავტობუსისა და ავტობუსის ხაზები, უფასო პარკინგი.","ar":"كيف أصل إلى بارك أرديشن مول؟ طريق ساحل البحر الأسود، وخطوط الميني باص والحافلات، وموقف مجاني."},
})
ekle(v)
