import re

def process_file():
    with open("chapters/03_gerec_ve_yontem.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        # İstatistiksel Analiz giriş, Tanımlayıcı, Eksik Veri
        """## İstatistiksel Analiz

Doğrulanmış kanonik veri seti üzerinde yürütülen çıkarımsal çözümlemede anlamlılık düzeyi çift yönlü α = 0,05 olarak belirlenmiştir. Birincil H1–H4 çözümlemelerinde çoklu karşılaştırma için Benjamini-Hochberg yanlış-keşif oranı (FDR) düzeltmesi uygulanmıştır [@benjaminiHochberg1995fdr]. Çokluk düzeltmesinin tanımlandığı birim, birlikte değerlendirilen bir hipotez testleri kümesi olan *test ailesidir*. Bu istatistiksel anlamdaki "test ailesi", çalışmanın veri birimi olan sosyal aileden (anne–çocuk–kardeş) farklı ve bağımsız bir kavramdır ve izleyen metinde daima "test ailesi" olarak anılır. Keşifsel ve ikincil genişletme katmanlarında çoklu karşılaştırma, doğrulayıcı H1–H4 hattının FDR test ailesinden ayrı tutularak, ilgili analizin test ailesi içinde Holm düzeltmesiyle ele alınmıştır [@holm1979]; Holm düzeltmesi, o test ailesinde en az bir yanlış-pozitif çıkma olasılığını (test ailesi düzeyinde hata oranını) denetler. Bu iki test aileli tercih, doğrulama hattında beklenen yanlış-keşif oranını denetleyerek görece daha çok gerçek etkinin yakalanmasını; keşifsel ve ikincil hatta ise test ailesi düzeyinde hata oranını daha sıkı denetleyerek yanlış-pozitif üretiminin sınırlanmasını amaçlar. Etki büyüklükleri %95 güven aralığıyla, Bayesçi paralel hatta ise %95 güvenilir aralığıyla birlikte raporlanmıştır. Önyükleme temelli güven aralıkları; aracılık ve koşullu süreç çözümlemelerinde yanlılık düzeltilmiş-hızlandırılmış (BCa) yöntemle 1000 yineleme, ağ ve kalibrasyon çözümlemelerinde 1000 yineleme ve diadik oran kestiriminde 1000 yineleme üzerinden hesaplanmıştır.

### Tanımlayıcı istatistikler ve grup dengesi

Sürekli değişkenler ortalama ve standart sapma ile medyan ve çeyrekler arası aralık, kategorik değişkenler sayı ve yüzde ile özetlenmiştir. T1DM ve kontrol ailelerinin başlangıç özellikleri aile düzeyinde raporlanmıştır. Grup dengesizliği; örneklem büyüklüğüne duyarlı p değerinden bağımsız olarak, iki grubun bir değişkendeki uzaklığını doğrudan etki büyüklüğü ölçeğinde veren standardize ortalama fark (SMD) göstergesiyle değerlendirilmiştir [@austin2009balanceDiagnostics]. Bu tercih, "istatistiksel anlamlılık" ile "pratik denge" ayrımını görünür kılar: küçük bir grup farkı büyük örneklemde anlamlı çıkabilirken SMD, farkın gerçekte ne kadar büyük olduğunu p değerinden bağımsız gösterir.

### Eksik veri yönetimi

Eksik veri üç çerçeveyle ele alınmıştır [@littleRubin2019missing]. Bu çoklu çerçevenin gerekçesi; eksik verinin nasıl işlendiğine ilişkin varsayımı görünür kılmak ve üç yöntemin aynı sonuca ulaşmasını, bulgunun eksik veri kararına duyarsızlığını gösteren bir sağlamlık kanıtı olarak kullanmaktır. Birincil çözümleme, tam bilgi maksimum olabilirlik (FIML)^[FIML: eksik satırları çözümlemeden atmak yerine tüm gözlemlerdeki mevcut bilgiyi kullanarak kestirim yapan yöntem.] [@endersBandalos2001fiml] ve çoklu atama (*multiple imputation*)^[Çoklu atama (*multiple imputation*): her eksik değeri tek bir tahminle değil, kestirim belirsizliğini yansıtacak biçimde çok sayıda olası değerle dolduran ve sonuçları birleştiren yöntem.] çerçeveleri altında rastgele eksiklik (MAR) varsayımıyla yürütülmüştür. Tam-vaka sonuçlar, bilgi kaybını göstermek için tamamlayıcı olarak sunulmuştur. Çoklu atama, zincirli denklemlerle [@vanBuuren2011mice] 50 atanmış veri seti (m = 50) ve otuz iterasyon üzerinden yürütülmüştür. Atama yöntemleri değişken türüne göre eşlenmiştir: sürekli değişkenlerde öngörücü ortalama eşleme^[Öngörücü ortalama eşleme: atanacak değeri yalnız parametrik bir modelden çekmek yerine, kestirilen değere en yakın gözlenen olgulardan çekerek değişkenin gözlenen dağılımını koruyan yöntem.], ikili değişkenlerde lojistik, sıralı değişkenlerde orantılı olasılıklar regresyonu. Yeniden üretilebilirlik için sabit bir tohum değeri kullanılmıştır. Rastgele olmayan eksikliğe (MNAR) karşı dayanıklılık; atanmış değerlere önceden tanımlı sistematik kaymalar (delta) eklenerek sonucun bu kaymalara duyarlılığını ölçen delta tabanlı duyarlılık çözümlemesiyle sınanmıştır. Kontrol grubunda tasarım gereği bulunmayan HbA1c ve diyabet süresi alanları yapısal eksik kabul edilmiş; bu alanlarda atama yalnız T1DM grubundaki çözümsel eksik hücrelerle sınırlandırılmıştır.

### Nedensel çıkarım çerçevesi""":
        
        """## İstatistiksel Analiz

Doğrulanmış ham veri üzerinden yapılan çıkarımsal analizlerde, klinik araştırmaların genel standardı olan p<0,05 anlamlılık sınırı benimsenmiştir. Aynı veri setinde çok sayıda hipotez testi yapıldığında tesadüfen "anlamlı" (yanlış-pozitif) sonuç bulma ihtimali matematiksel olarak arttığı için, bu riski dengelemek adına p-değerleri (Benjamini-Hochberg FDR ve Holm yöntemleriyle) düzeltilerek yeniden hesaplanmıştır [@benjaminiHochberg1995fdr; @holm1979]. İstatistiksel sonuçların kesinliği %95 Güven Aralığı (GA) ile raporlanmış; gerekli durumlarda bilgisayarın veriyi kendi içinde binlerce kez yeniden örneklemesi (bootstrap) yoluyla güven aralıkları sağlamlaştırılmıştır.

### Tanımlayıcı istatistikler ve grup dengesi

Örneklemin demografik ve tıbbi özellikleri; sürekli veriler için ortalama ve standart sapma, kategorik veriler için sayı ve yüzde gibi temel özetlerle sunulmuştur. İki grubun başlangıç özelliklerinin (örneğin yaş veya gelir) ne kadar "denk" olduğu sadece geleneksel p-değeriyle değil, gruplar arasındaki mesafeyi katılımcı sayısından bağımsız, mutlak bir büyüklük olarak gösteren standardize ortalama fark (SMD) değeriyle kanıtlanmıştır [@austin2009balanceDiagnostics].

### Eksik veri yönetimi

Analizlerde, anketin bazı sorularını boş bırakan kişilerin verileri doğrudan silinip çöpe atılmamıştır (bu durum büyük bir bilgi kaybına yol açar). Bunun yerine, eksik hücrelerin diğer doldurulmuş yanıtlardan yola çıkılarak yapay zekâ/istatistiksel tahmin algoritmalarıyla "ne olabileceği" hesaplanmış (Çoklu Atama ve FIML) ve tüm analizler bu doldurulmuş tam-veri havuzları üzerinde yürütülmüştür [@littleRubin2019missing; @endersBandalos2001fiml; @vanBuuren2011mice]. Sağlıklı ailelerin tasarım gereği sahip olmadığı diyabet süresi ve HbA1c verileri ise eksiklik olarak değil, "yapısal yokluk" olarak işaretlenmiştir.

### Nedensel çıkarım çerçevesi"""
    }

    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            print("Successfully replaced section 3.9 intro!")
        else:
            print("Failed to replace section 3.9 intro!")

    with open("chapters/03_gerec_ve_yontem.qmd", "w", encoding="utf-8") as f:
        f.write(content)

process_file()
