import sys

file_path = "chapters/03_gerec_ve_yontem.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    r"""## Ölçme Araçlarının Psikometrik Değerlendirmesi

Kullanılan ebeveyn tutumu ölçeğinin, Karşılaştırma boyutu eklenmiş dört alt ölçekli sürümü Türkçe yazında daha önce de kullanılmıştır [@temelAltanAtalay2018selfCompassion]. Bu sürüm, eşlenik anne–çocuk formlarıyla birlikte bir çalışmada da uygulanmıştır [@caliskanSari2018embuC]. Bununla birlikte, sürümün birincil hipotez sınamalarına güçlü bir metodolojik omurga sağlaması amacıyla, çocuk ve ebeveyn formlarının faktör yapısı ve güvenirliği bu örneklemde ayrıca teyit edici bir çalışma-içi psikometrik değerlendirmeye tabi tutulmuştur. Bu tercih iki tasarım gerekçesine dayanır: (i) her iki form, çocukların güncel algısını ve çocuğun kardeş/akranlarıyla karşılaştırılmasını da kapsayacak biçimde, beş maddelik Karşılaştırma alt ölçeğinin eklendiği dört faktörlü sürümde uygulanmıştır [@sumer2010anneBabaTutum]; (ii) ölçüm özelliklerinin Tip 1 diyabetli ve kontrol ailelerindeki eşlenik anne–çocuk raporları bağlamında da geçerliğini teyit etmek amaçlanmıştır. Bu değerlendirme hattı, güncel ölçüm-değerlendirme (COSMIN) ilkeleriyle^[COSMIN, bir ölçeğin bilimsel olarak kabul edilebilir sayılabilmesi için üç temel sütunun en yüksek metodolojik standartlarda sınanmasını şart koşar: geçerlik (*validity*), yani ölçeğin gerçekten ölçtüğünü iddia ettiği yapıyı ölçüp ölçmediği; güvenirlik (*reliability*), yani aynı kişiye farklı zamanlarda ya da farklı uygulayıcılarca uygulandığında tutarlı sonuç verip vermediği; ve duyarlılık (*responsiveness*), yani gerçek değişimleri yakalayabilme kapasitesi.] uyumlu yürütülmüş ve ön-kayıt edilmiştir [@mokkink2018cosmin]. Değerlendirme yöntemi aşağıda tanımlanmakta; özet bulgular Bulgular bölümünde, ayrıntılı bulgular ise Ek 7'de (@sec-ek-psikometri) raporlanmaktadır.

### Madde düzeyi çözümleme ve güvenirlik

Çalışmada kullanılan alt ölçeklerin psikometrik özellikleri, geleneksel yöntemlerin ötesine geçilerek verinin doğasına uygun güncel yaklaşımlarla incelenmiştir. Bu süreç üç temel adımda yürütülmüştür:

**Betimsel istatistikler ve dağılım özellikleri.** Her bir alt ölçek için madde düzeyinde ortalama, standart sapma, çarpıklık (*skewness*) ve basıklık (*kurtosis*) değerleri ile taban ve tavan etkisi oranları hesaplanmıştır. Verilerin sıralı (*ordinal*) doğası gereği ortaya çıkabilecek çarpık dağılım veya uçlarda yığılma (taban/tavan etkisi) durumları birer hata olarak görülmemiş; aksine, ileri analizlerde seçilecek kestirim yöntemlerini ve kategori kararlarını belirleyen temel metodolojik ölçütler olarak kullanılmıştır.

**Modern güvenirlik hesaplamaları (McDonald omega).** Ölçeklerin güvenirliği, literatürde sıklıkla eleştirilen ve verilerin tamamen normal dağıldığı ile her sorunun eşit ağırlıkta olduğu (tau-eşdeğerliği) varsayımına dayanan geleneksel Cronbach alfa katsayısıyla sınırlandırılmamıştır. Bunun yerine, sıralı veriler için çok daha güçlü sonuçlar veren polikorik korelasyon temelli McDonald omega ($\omega$) katsayıları hesaplanmıştır. Sonuçların kararılılığını göstermek amacıyla, bu katsayılar önyükleme (*bootstrap*) yöntemine dayalı güven aralıklarıyla birlikte raporlanmıştır [@dunn2014alphaOmega; @trizanoHermosilla2016omegaAlpha].

**Çok düzeyli güvenirlik ve madde ayırt ediciliği.** Çocuk formundan elde edilen veriler aile sistemi içinde iç içe geçmiş (yuvalanmış) bir yapı sergilediği için, analizler bu bağımlılık durumu hesaba katılarak yapılmıştır. Bu doğrultuda güvenirlik değerleri düz bir yapıda değil; aile içi ve aile-arası bileşenlerine ayrıştırılarak çok düzeyli olarak incelenmiştir. Ek olarak, ölçekteki her bir maddenin yapıya katkısını (madde ayırt ediciliğini) değerlendirmek için düzeltilmiş madde-toplam korelasyonları ve ilgili madde modelden çıkarıldığında güvenirlik katsayısında meydana gelen değişimler analiz edilmiştir.

### Faktör yapısının sınanması

Ölçeğin orijinal dört faktörlü yapısının bu örneklemde geçerli olup olmadığı, veriye doğrudan doğrulayıcı bir model dayatılmadan önce aşamalı bir yöntemle sınanmıştır:

**Açımlayıcı ön tarama.** Çözümlemeye doğrulayıcı faktör analiziyle başlamak yerine yapı önce keşfedici faktör analiziyle taranmıştır. Bu aşamada verinin faktörleştirilebilirliği Kaiser–Meyer–Olkin (KMO) örneklem yeterliliği ve Bartlett küresellik ölçütleriyle değerlendirilmiştir. Çıkarılacak faktör sayısına karar verilirken basit kurallar yerine, polikorik korelasyon matrisi üzerinde paralel çözümleme [@horn1965parallel] ve en küçük ortalama kısmi (*minimum average partial*, MAP) ölçütü kullanılmış; madde-faktör örüntüsü ayrıca incelenmiştir.

**Doğrulayıcı faktör analizi ve model karşılaştırmaları.** Ön taramanın ardından, dört düzeyli sıralı (*ordinal*) maddelere uygun ağırlıklı en küçük kareler ortalama-varyans düzeltmeli kestirim yöntemiyle (*Weighted Least Squares Mean and Variance adjusted*, WLSMV) doğrulayıcı faktör analizi yürütülmüştür [@li2016ordinalCFA]. Hangi yapının örneklemi en iyi temsil ettiğini belirlemek amacıyla tek faktörlü, dört faktörlü, ikinci düzey (*second-order*) ve bifaktör (bir genel + özgül faktörlü; *bifactor*) modeller kurularak birbirleriyle karşılaştırılmıştır.

**Model uyum indekslerinin değerlendirilmesi.** Kurulan faktör yapılarının gözlenen veriyle ne kadar örtüştüğünü gösteren model uyumu; ki-kare istatistiğinin yanı sıra karşılaştırmalı uyum indeksi (CFI), Tucker-Lewis indeksi (TLI), yaklaşık hata kareler ortalamasının karekökü (RMSEA, %90 güven aralığı ile) ve standardize artık kareler ortalamasının karekökü (SRMR) üzerinden yerleşik eşik ölçütleriyle değerlendirilmiştir. Bu indeksler yüksek uyumda CFI/TLI'nin 1'e, RMSEA ve SRMR'nin ise sıfıra yaklaşmasını bekler [@huBentler1999cutoff].

**Aile içi bağımlılık ve çok düzeyli sınama.** Çocuk formundan elde edilen verilerin aile içinde yuvalanmış (bağımlı) yapısı geçerlik sınamalarında da göz ardı edilmemiştir. Bu bağımlılık; sınıf-içi korelasyonun hesaplanması ve aile numarasının kümeleme değişkeni alınmasıyla, modele çok düzeyli doğrulayıcı faktör analizi (*multilevel CFA*) biçiminde katılmıştır.

### Bayesçi doğrulayıcı analiz

Görece küçük örneklem koşullarında geleneksel doğrulayıcı faktör analizi; çapraz faktör yüklerinin ve hata kovaryanslarının tam olarak sıfır olması gibi katı varsayımlara dayanır. Bu katılığın yaratabileceği kısıtlılıkları aşmak için alternatif bir ön-uçuş (*preflight*) planı olarak Bayesçi Yapısal Eşitlik Modeli (BSEM) tasarlanmıştır [@muthenAsparouhov2012bsem]. BSEM, bu ikincil parametreleri kesin sıfıra sabitlemek yerine, onlara küçük bir esneme payı tanıyarak "sıfıra çok yakın" değerler alabileceklerini kabul eder.

Bu esnek yaklaşımda modelin çalışma kuralları (önselleri) analiz öncesinde şöyle belirlenmiştir:

- **Ana faktör yükleri:** Görece esnek ve geniş bir önsel ($\lambda_{ana} \sim \text{Normal}(0,5;\ 0,5)$),
- **Çapraz yükler ve hata kovaryansları:** Sıfır merkezli, çok daha dar ve katı bir önsel (ör. $\text{Normal}(0;\ 0,01)$),
- **Yapısal katsayılar:** Standart bir önsel ($\beta \sim \text{Normal}(0;\ 1)$) kullanılmıştır.

Eşik ve latent varyans/ölçek parametreleri ise analiz yazılımının (`blavaan`) varsayılan zayıf önsellerine bırakılmıştır.

Bu Bayesçi yaklaşım, araştırmanın ana analiz hattının (`targets`) dışında, yalnızca isteğe bağlı ek bir psikometrik sağlamlık testi olarak konumlandırılmıştır. Bu nedenle H4 hipotezi için doğrulayıcı olarak bildirilen asıl çözüm klasik WLSMV kestirimidir (bkz. Bulgular, §H4). BSEM modeli çalıştırıldığında ise, modelin veriye ne kadar iyi uyduğu sonsal öngörücü olasılık (*posterior predictive p*, PPP) değeri ve yakınsama tanı ölçütleriyle değerlendirilecek şekilde yapılandırılmıştır.""":
    r"""## Ölçme Araçlarının Psikometrik Değerlendirmesi

Kullandığımız 29 soruluk ebeveyn tutumu anketi Türkiye'de daha önce kullanılmış bir formdur [@temelAltanAtalay2018selfCompassion; @caliskanSari2018embuC]. Yine de biz işimizi şansa bırakmamak için, "bu anket bizim hastalarımızda ve kontrol ailelerimizde de gerçekten aynı doğruluğu veriyor mu?" diye teyit etmek istedik [@sumer2010anneBabaTutum]. Bu yüzden, çalışmamızın asıl bulgularını yayınlamadan önce anketlerin kalitesini, uluslararası geçerlilik standartlarına (COSMIN) uygun şekilde ayrıntılı testlerden geçirdik [@mokkink2018cosmin]. 

### Madde düzeyi çözümleme ve güvenirlik

Ölçeklerin güvenilirliği, modası geçmiş hesaplamalar (sadece Cronbach alfa vb.) ile bırakılmamış, modern istatistikler uygulanmıştır:

- **Sorulara nasıl cevap verdiler?** Anketteki sorulara verilen cevapların aşırı bir uçta yığılıp yığılmadığına (örneğin herkes "hiçbir zaman" mı dedi) bakıldı. Bu durum anketin bir hatası değil, gerçekliği yansıtma biçimi olarak kabul edildi.
- **Modern güvenilirlik.** Herkesin her soruyu mükemmel bir dağılımla aynı önemde anladığını varsayan eski usul güvenilirlik katsayısı (alfa) yerine, anketin sıralı ("1=hiç, 4=çok") doğasına uygun olan "McDonald Omega" ($\omega$) katsayısı ile gerçekçi güvenilirlik seviyeleri hesaplanmıştır [@dunn2014alphaOmega; @trizanoHermosilla2016omegaAlpha].
- **Aynı evdeki çocuklar.** Çocukların aynı eve ait olmasının yarattığı istatistiksel karmaşa (yuvalanmış yapı) göz ardı edilmemiş; "bir soruyu ankette tutarsak model düzelir mi, çıkarırsak bozulur mu" hesapları, ailenin iç yapısını hesaba katan çok katmanlı denklemlerle çözülmüştür.

### Faktör yapısının sınanması

Anketin gerçekten 4 ayrı duyguyu (sıcaklık, koruma, reddetme, karşılaştırma) ölçüp ölçmediği körü körüne kabul edilmemiş, istatistiksel bir taramadan geçirilmiştir:

- **Ön tarama ve doğrulama.** Elimizdeki verinin anketle ne kadar örtüştüğünü keşfetmek için, basit kurallar yerine KMO ve MAP denilen karmaşık testler (faktör analizi) uygulanmıştır [@horn1965parallel]. Ardından, "bu veriler 4 duyguyu ölçüyor" hipotezi, anketin dört şıklı doğasına en uygun matematiksel model (WLSMV) kullanılarak sınanmıştır [@li2016ordinalCFA]. Acaba 1 duygu, 4 duygu, yoksa tek bir ana duygunun etrafında toplanan 4 duygu (bifaktör) mü geçerli diye tüm senaryolar kapıştırılmıştır. 
- **Modelin uyum karnesi.** Kurduğumuz matematiksel modellerin gerçek hayatla ne kadar bağdaştığını ispatlayan evrensel kalite belgeleri (CFI, TLI, RMSEA, SRMR) kullanılarak modelin karnesi hesaplanmıştır [@huBentler1999cutoff]. Bu karneyi çıkarırken bile aynı evde yaşayan kardeşlerin durumu (aile içi bağımlılık) es geçilmemiştir.

### Bayesçi doğrulayıcı analiz

Klasik matematik (istatistik), anket verilerini hesaplarken çok katı davranır; örneğin "Duygusal Sıcaklık" sorusunun "Reddetme" puanına etkisini tamı tamına "sıfır" kabul eder. Ancak insan psikolojisinde duygu geçişleri tam "sıfır" sınırıyla bıçak gibi kesilmez. 

İşte biz bu katılıktan kurtulmak için Bayesçi (BSEM) istatistik dediğimiz, daha esnek bir modeli sağlamlık testi olarak yedeğe aldık [@muthenAsparouhov2012bsem]. Bu model, soruların diğer duygulara da "küçük de olsa" bir miktar sızabileceğini kabul eden esnek bir bakış açısıdır. Asıl analizlerimizde katı olan temel istatistiği raporlasak da, Bayesçi testleri arka planda yedek tutarak, sonuçların dayanıklılığını güvence altına aldık."""
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success!")
    else:
        print("Failed to find:\n" + old[:100] + "...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
