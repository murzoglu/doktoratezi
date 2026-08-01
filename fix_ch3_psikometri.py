import re

def process_file():
    with open("chapters/03_gerec_ve_yontem.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        'Yönteme ilişkin matematiksel altyapı aşağıda ve detaylı sonuçlar [Ek 7](#sec-ek-psikometri)\'de sunulmuştur.': 'Kullanılan istatistiksel stratejilerin kavramsal temeli aşağıda özetlenmiş olup, teknik ayrıntılar ve sayısal sonuçlar [Ek 7](#sec-ek-psikometri)\'de sunulmuştur.',
        'Anket sorularının tutarlılığı (güvenirliği) hesaplanırken sadece en yaygın yöntem (Cronbach alfa) kullanılmamış; sıralı anket yanıtlarında daha doğru sonuç verdiği bilinen ileri düzey katsayılar da (McDonald omega) dikkate alınmıştır': 'İç tutarlılık değerlendirmesinde geleneksel Cronbach α katsayısına ek olarak, sıralı (ordinal) anket verilerinde madde ağırlıklarının eşitliği varsayımına bağımlı olmayan McDonald ω katsayısı kullanılmıştır',
        'Ebeveynlik tutumundaki dört temel kuramsal kavramın (sıcaklık, koruma, reddetme, kıyaslama) veri setinde aynen oluşup oluşmadığı, yapısal eşitlik testleriyle (doğrulayıcı faktör analizi, WLSMV) incelenmiştir': 'Ölçeğin kuramsal dörtlü yapısı (sıcaklık, aşırı koruma, reddetme, karşılaştırma), gözlenen anket sorularından gizil (latent) kavramlar çıkaran Doğrulayıcı Faktör Analizi (CFA) ile test edilmiştir',
        'Kuramsal birleştirme için tek-boyut, dört-boyut veya genel/özgül faktör (bifaktör) modelleri sınanmıştır.': 'Bu süreçte tek-boyutlu, dört-boyutlu ve bir genel faktör ile ondan bağımsız özgül faktörleri aynı anda sınayan bifaktör modelleri karşılaştırılmıştır.',
        'Kurulan faktör yapısının gözlenen veriyle uyumu ise CFI, TLI, RMSEA ve SRMR gibi yerleşik uyum indeksleri kullanılarak değerlendirilmiştir': 'Modelin veriyle olan genel uyumu, yerleşik uyum indeksleri (CFI, TLI, RMSEA ve SRMR) üzerinden incelenmiştir (indeks eşikleri ve formülizasyonu teknik ekte verilmiştir)',
        'Klasik doğrulayıcı analiz, anketin soruları arasındaki bazı küçük (artık/kovaryans) çapraz ilişkileri "kesinlikle sıfır" kabul eder. Bu varsayım küçük çalışma gruplarında hata riski yaratabilir. Söz konusu riski dengelemek amacıyla, bu değerlerin "sıfıra çok yakın" (fakat tam sıfır değil) olduğu esnek önsel beklentilerle çalışan alternatif Bayesçi modelleme (BSEM) ek bir güvenlik testi olarak sisteme dâhil edilmiştir': 'Geleneksel faktör analizinin çapraz madde yüklerini ve hata kovaryanslarını kesin sıfır kabul eden katı yapısını esnetmek amacıyla, Bayesçi Yapısal Eşitlik Modellemesi (BSEM) uygulanmıştır. Bu yöntem, söz konusu artık ilişkilerin sıfıra yakın ancak değişken olabileceğine dair esnek önsel bilgiler (priors) kullanarak model uyumunu ve madde yapılarını çapraz doğrular',
        'Puan karşılaştırması bir ön koşul gerektirir. Ölçek puanlarının farklı tanı grupları ve bilgi verenler arasında karşılaştırılabilirliği, ölçüm eşdeğerliği (measurement invariance) analizleriyle sınanmıştır': 'Anket puanlarının farklı gruplarda (diyabet ve kontrol) aynı kavramı ölçüp ölçmediği, gruplar arası karşılaştırmaların geçerliği için bir ön koşul olan ölçüm eşdeğerliği (measurement invariance) analizleriyle doğrulanmıştır',
        'Sırasıyla yapılandırmasal (aynı faktör deseni), metrik (aynı madde ağırlıkları) ve skalar (sıralı veride aynı madde eşikleri) düzeyler denenmiştir.': 'Analiz, sırasıyla aynı faktör deseninin (yapılandırmasal), aynı madde ağırlıklarının (metrik) ve aynı madde eşiklerinin (skalar) sağlanıp sağlanmadığını test eden basamaklı bir kısıtlama yaklaşımıyla yürütülmüştür.',
        'Bir basamaktan diğerine geçerken uyumun bozulup bozulmadığı yalnız ki-kare farkına bırakılmamış; CFI, RMSEA ve SRMR değişim ölçütleriyle birlikte değerlendirilmiştir. Bozulma ölçütü olarak CFI\'de 0,010\'luk düşüş veya RMSEA\'da 0,015\'lik artış esas alınmıştır.': 'Eşdeğerlik kararı, katı ki-kare (Δχ²) fark testlerinin yanı sıra uyum indekslerindeki değişim (ΔCFI < 0,010 ve ΔRMSEA < 0,015) kriterlerine dayandırılmıştır.',
        'Bilgi veren rolleri arasında (indeks çocuk vs. kardeş) matematiksel eşdeğerliğin bozulduğu noktalar, yalnızca bir "anket ölçüm hatası" olarak değil; aynı evin içindeki farklı çocukların aynı ebeveyni gerçekten "farklı" hissettiğine dair tözsel bir işaret olarak yorumlanmıştır.': 'Roller (indeks çocuk ve kardeş) arasında skalar eşdeğerliğin sağlanamadığı durumlar basit bir ölçüm yanlılığı olarak değil, farklı çocukların aynı ebeveynlik tutumunu kavramsal olarak farklı deneyimlediğine dair yapısal bir bulgu olarak ele alınmıştır.',
        'Anketin gerçekten ölçmek istediğini ölçtüğünü kanıtlamak (ölçüt geçerliği) adına, anne depresif belirtileri ile "beklendiği gibi" ilişki kurup kurmadığı sınanmıştır': 'Ölçeklerin kuramsal olarak ilişkili olması beklenen dış değişkenlerle bağını teyit etmek amacıyla (ölçüt geçerliği), ebeveynlik alt boyutları ile maternal depresif belirtiler (Beck Envanteri) arasındaki korelasyonlar incelenmiştir',
        'Annenin ebeveynlik davranışı hakkında aynı evin içinde indeks çocuk ve kardeşin verdiği iki farklı not arasındaki matematiksel uzlaşma düzeyi, sınıf-içi korelasyon ve klinik tanıya uygun yöntemlerle (Bland-Altman) belirlenmiştir': 'Aynı hanedeki bilgi-vericilerin (anne, indeks çocuk, kardeş) ölçüm tutarlılığı; sınıf-içi korelasyon (ICC) ve mutlak ölçüm uyumunu görselleştiren Bland-Altman analizi ile değerlendirilmiştir',
        'Ebeveyn öz-bildiriminde, özellikle olumsuz muamele maddelerinde gözlenebilecek taban etkisinin (en düşük puanda yığılma) analitik sonuçlar üzerindeki etkisi; kategori daraltma, düşük ayırt edicilikli madde çıkarma ve Bayesçi latent skor gibi farklı stratejilerle paralel olarak modellenmiş ve sonuçların bu seçimlere karşı duyarlılığı (çok-evrenli analiz) sınanmıştır': 'Özellikle ebeveyn öz-bildirimindeki reddetme gibi olumsuz tutum alt boyutlarında gözlenen taban etkisinin (en düşük puanda yığılma) bulguları bozma riski; kategori birleştirme, sorunlu maddelerin dışlanması ve Bayesçi gizil (latent) faktör skorları kullanma gibi alternatif stratejilerle eşzamanlı olarak modellenmiş (çoklu evren duyarlılık analizi) ve ana bulguların bu metodolojik seçimlere direnci test edilmiştir',
        'Verideki "eksik" alanların rastgele mi bırakıldığı kontrol edilmiştir': 'Eksik verilerin Dağılım Mekanizması (MCAR) ayrıca analiz edilmiştir',
        
        'Çözümlemelerin her seferinde birebir aynı orijinal veriden beslenmesini garanti altına almak için, bu ana dosyalara hiçbir şekilde "hesaplanmış ortalama" veya "toplam puan" kaydedilmemiş; bu hesaplamalar her istatistik analizi sırasında kilitli ham puanlar üzerinden otomatik formüllerle üretilmiştir.': 'Analitik yinelenebilirliği (reproducibility) sağlamak adına, bu kanonik baz dosyalarda hiçbir türetilmiş veya toplu skor saklanmamış; tüm alt ölçek ve kompozit puanlar analiz aşamasında ham veri üzerinden dinamik olarak hesaplanmıştır.',
        'Veri güvenliğini doğrulamak amacıyla (veri setinin izinsiz veya tesadüfi değişime uğramadığından emin olmak için), veri tabanının kriptografik özeti (SHA-256) doğrulanarak analizlere başlanmıştır.': 'Veri bütünlüğünü teyit etmek amacıyla, analizlerin her bir koşumunda kanonik veri dosyasının kriptografik sağlama toplamı (SHA-256) doğrulanmıştır.',
        
        'Aynı veri setinde çok sayıda hipotez testi yapıldığında tesadüfen "anlamlı" (yanlış-pozitif) sonuç bulma ihtimali matematiksel olarak arttığı için, bu riski dengelemek adına p-değerleri (Benjamini-Hochberg FDR ve Holm yöntemleriyle) düzeltilerek yeniden hesaplanmıştır': 'Çoklu hipotez sınamalarından kaynaklanan Tip-1 hata artışını (yanlış pozitiflik) kontrol altına almak amacıyla, p-değerleri Benjamini-Hochberg Yanlış Keşif Oranı (FDR) ve gerekli durumlarda Holm-Bonferroni yöntemleriyle düzeltilmiştir',
        'İstatistiksel sonuçların kesinliği %95 Güven Aralığı (GA) ile raporlanmış; gerekli durumlarda bilgisayarın veriyi kendi içinde binlerce kez yeniden örneklemesi (bootstrap) yoluyla güven aralıkları sağlamlaştırılmıştır.': 'Kestirimlerin kesinliği %95 Güven Aralıkları (GA) ile sunulmuş; veri dağılımının parametrik varsayımları karşılamadığı modellemelerde (örn. dolaylı etkiler) yeniden örnekleme (bootstrap) tabanlı güven aralıkları kullanılmıştır.'
    }

    count = 0
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            count += 1
            print(f"Replaced: {old[:30]}...")
        else:
            print(f"NOT FOUND: {old[:30]}...")

    with open("chapters/03_gerec_ve_yontem.qmd", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Total replaced in ch3 part3: {count}")

process_file()
