import re

def process_file():
    with open("chapters/03_gerec_ve_yontem.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        # Ölçme Araçlarının Psikometrik Değerlendirmesi
        """## Ölçme Araçlarının Psikometrik Değerlendirmesi

Kullanılan ebeveyn tutumu ölçeğinin, Karşılaştırma boyutu eklenmiş dört alt ölçekli sürümü Türkçe yazında daha önce de kullanılmıştır [@temelAltanAtalay2018selfCompassion]. Bu sürüm, eşlenik anne–çocuk formlarıyla birlikte bir çalışmada da uygulanmıştır [@caliskanSari2018embuC]. Bununla birlikte, sürümün birincil hipotez sınamalarına güçlü bir metodolojik omurga sağlaması amacıyla, çocuk ve ebeveyn formlarının faktör yapısı ve güvenirliği bu örneklemde ayrıca teyit edici bir çalışma-içi psikometrik değerlendirmeye tabi tutulmuştur. Bu tercih iki tasarım gerekçesine dayanır: (i) her iki form, çocukların güncel algısını ve çocuğun kardeş/akranlarıyla karşılaştırılmasını da kapsayacak biçimde, beş maddelik Karşılaştırma alt ölçeğinin eklendiği dört faktörlü sürümde uygulanmıştır [@sumer2010anneBabaTutum]; (ii) ölçüm özelliklerinin Tip 1 diyabetli ve kontrol ailelerindeki eşlenik anne–çocuk raporları bağlamında da geçerliğini teyit etmek amaçlanmıştır. Bu değerlendirme hattı, güncel ölçüm-değerlendirme (COSMIN) ilkeleriyle uyumlu yürütülmüş ve ön-kayıt edilmiştir [@mokkink2018cosmin]. Değerlendirme yöntemi aşağıda tanımlanmakta; özet bulgular Bulgular bölümünde, ayrıntılı bulgular ise Ek 7'de (@sec-ek-psikometri) raporlanmaktadır.

### Madde düzeyi çözümleme ve güvenirlik

Her alt ölçek için madde düzeyinde ortalama, standart sapma, çarpıklık, basıklık ile taban ve tavan etkisi oranları hesaplanmıştır. Sıralı verilerde çarpık dağılım ve taban/tavan yığılması, sonraki kestirim ve kategori kararlarını belirleyen ölçütler olarak kullanılmıştır. Güvenirlik yalnız Cronbach alfa katsayısıyla sınırlandırılmamıştır; tau-eşitliği varsayımına daha az bağımlı olan McDonald omega katsayıları, sıralı maddeler için polikorik korelasyon temelinde hesaplanmış ve önyükleme (*bootstrap*) temelli güven aralıklarıyla raporlanmıştır [@dunn2014alphaOmega; @trizanoHermosilla2016omegaAlpha]. Çocuk formunun aile içinde yuvalanmış yapısı nedeniyle güvenirlik ayrıca aile içi ve aile-arası bileşenlerine ayrıştırılarak incelenmiştir. Madde ayırt ediciliği, düzeltilmiş madde-toplam korelasyonları ve madde çıkarıldığında güvenirlikteki değişimle değerlendirilmiştir.

### Faktör yapısının sınanması

Dört faktörlü yapının bu örneklemde geçerli olup olmadığı, doğrulayıcı analiz doğrudan dayatılmadan önce keşfedici faktör analiziyle taranmıştır. Bu tarama; faktörleştirilebilirlik (Kaiser–Meyer–Olkin [KMO] örneklem yeterliliği ve Bartlett küresellik ölçütleri), faktör sayısı (polikorik korelasyon matrisi üzerinde paralel çözümleme [@horn1965parallel] ve en küçük ortalama kısmi ölçütü) ve madde-faktör örüntüsünü kapsamıştır. Ardından, dört düzeyli sıralı maddelere uygun ağırlıklı en küçük kareler ortalama-varyans düzeltmeli kestirim yöntemiyle (*Weighted Least Squares Mean and Variance adjusted*, WLSMV) doğrulayıcı faktör analizi yürütülmüştür [@li2016ordinalCFA]. Tek faktörlü, dört faktörlü, ikinci düzey ve bifaktör (bir genel + özgül faktörlü; *bifactor*) modeller birbirleriyle karşılaştırılmıştır. Kurulan faktör yapısının gözlenen veriyle ne kadar örtüştüğünü gösteren model uyumu; ki-kare istatistiğinin yanı sıra karşılaştırmalı uyum indeksi (CFI), Tucker-Lewis indeksi (TLI), yaklaşık hata kareler ortalamasının karekökü (RMSEA, %90 güven aralığı ile) ve standardize artık kareler ortalamasının karekökü (SRMR) üzerinden yerleşik eşik ölçütleriyle değerlendirilmiştir. Bu indeksler yüksek uyumda CFI/TLI'nin 1'e, RMSEA ve SRMR'nin ise sıfıra yaklaşmasını bekler [@huBentler1999cutoff]. Çocuk formundaki aile içi bağımlılık; sınıf-içi korelasyonun hesaplanması ve aile numarasının kümeleme değişkeni alındığı çok düzeyli doğrulayıcı analizle ele alınmıştır.

### Bayesçi doğrulayıcı analiz

Görece küçük örneklem koşullarında, çapraz yüklemeleri ve hata kovaryanslarını kesin sıfır sayan klasik doğrulayıcı analizin kısıtları göz önünde bulundurulmuştur. Bu koşullarda söz konusu ikincil parametreleri kesin sıfıra sabitlemek yerine, sıfır merkezli ve çok küçük varyanslı bilgi verici önsellerle "yaklaşık sıfıra" çeken Bayesçi yapısal eşitlik modeli (BSEM), bir *ön-uçuş* (preflight) planı olarak tanımlanmıştır [@muthenAsparouhov2012bsem]. Bu planda önsel sınıfları ayrıştırılmıştır: birincil (ana) faktör yükleri için görece geniş bir bilgi verici önsel (λ_ana ∼ Normal(0,5; 0,5)); çapraz yükler ve artık (hata) kovaryanslar için ise sıfır merkezli, dar varyanslı "yaklaşık sıfır" önselleri (ör. Normal(0; 0,01)) öngörülmüştür. Yapısal katsayılar için β ∼ Normal(0; 1); eşik ile latent varyans/ölçek parametreleri için `blavaan` varsayılan zayıf bilgi verici önselleri kullanılacak biçimde, model sözdizimi ve yakınsama ölçütleri analiz öncesinde sabitlenmiştir. Bu hat, yeniden üretilebilir varsayılan çözümleme hattının (`targets`) dışında yalnız isteğe bağlı bir psikometrik sağlamlık adımı olarak konumlandırılmış; bu nedenle H4 için doğrulayıcı olarak raporlanan çözüm WLSMV kestirimidir (bkz. Bulgular, §H4). BSEM örneklemesi yürütüldüğünde model uyumu sonsal öngörücü olasılık (*posterior predictive p*, PPP) değeriyle değerlendirilecek ve yakınsama tanı ölçütleriyle denetlenecek biçimde tasarlanmıştır.

### Ölçüm eşdeğerliği

Ölçek puanlarının farklı alt gruplar ve bilgi verenler arasında karşılaştırılabilirliği, üç eksende ölçüm eşdeğerliği (*measurement invariance*) sınamasıyla değerlendirilmiştir: tanı grubu (T1DM/kontrol), bilgi verici rolü (indeks çocuk/kardeş) ile yaş ve cinsiyet. Yapılandırmasal, metrik ve skalar (sıralı verilerde eşik temelli) düzeyler sırayla sınanmıştır. Düzeyler arası geçişler yalnız ki-kare farkıyla değil; CFI, RMSEA ve SRMR değişim ölçütleriyle de değerlendirilmiştir [@putnickBornstein2016measurementInvariance; @chen2007invariance]. Bilgi verici rolü ekseninde skalar eşdeğerliğin sağlanmaması, aynı ebeveyn davranışının indeks çocuk ile sağlıklı kardeş tarafından sistematik olarak farklı algılandığına ilişkin yapısal bir ayrışmaya işaret edebilir. Ancak bu tasarımda ölçüm düzeyindeki eşitsizlik (madde eşiklerinin gruplar arası kayması) ile gerçek algı ayrışması birbirinden tam olarak ayrıştırılamadığından, bulgu her iki olası kaynağı da açık tutacak biçimde yorumlanır (bkz. Tartışma). Bu sınırlı ayrım, tezin aile içi algı farklılıklarına ilişkin çerçevesiyle ilişkilidir.

### Geçerlik ve raporcular arası uyum

Yakınsak ve ayırt edici geçerlik; ortalama açıklanan varyans, bileşik güvenirlik ve Fornell-Larcker ölçütü çerçevesinde değerlendirilmiştir [@fornellLarcker1981]. Ölçüt geçerliği için ebeveynlik alt ölçekleriyle anne depresif belirti düzeyi arasındaki kuramsal olarak beklenen ilişkiler sınanmıştır (duygusal sıcaklık ile negatif; reddetme ve karşılaştırma ile pozitif). Ayrıca Karşılaştırma alt ölçeği ile Kardeş İlişkileri Anketi'nin rekabet boyutu arasındaki eşzamanlı geçerlik ilişkisi incelenmiştir. Aynı annenin tutumunu paralel biçimde bildiren indeks ve kardeş çocuk raporları arasındaki uyum; sınıf-içi korelasyon, Bland-Altman uyum sınırları [@blandAltman1986] ve Gwet AC1 katsayısıyla [@gwet2008ac1] değerlendirilmiştir.

### Taban etkisi yönetimi ve sağlamlık

Ebeveyn öz-bildiriminde özellikle olumsuz muamele maddelerinde beklenebilecek taban etkisinin bulgular üzerindeki etkisi, tek bir işleme kararına bağlı kalınmadan çok evrenli (*multiverse*) çözümlemeyle ele alınmıştır. Bu çözümlemede tam ölçek, kategori daraltma, düşük ayırt edicilikli madde çıkarma ve Bayesçi latent skor stratejileri paralel işletilmiş ve sonuçlar spesifikasyon eğrisiyle özetlenmiştir [@steegen2016multiverse]. Gruplar arası farkın anlamlı bulunmadığı durumlarda "fark yok" iddiası, önceden belirlenmiş en küçük anlamlı etki büyüklüğü eşiğiyle iki tek-yönlü test (*two one-sided tests*, TOST) işlemi üzerinden değerlendirilmiştir [@lakens2017equivalence]. Eksik veri mekanizması Little MCAR sınamasıyla incelenmiştir [@little1988mcar]. Tüm ölçek doğrulama çözümlemeleri kanonik veri seti üzerinde, açık kaynaklı istatistik ortamında yürütülmüştür.

## Veri Toplama Süreci ve Veri Yönetimi""":
        
        """## Ölçme Araçlarının Psikometrik Değerlendirmesi

Kullanılan ebeveyn tutumu anketinin "Karşılaştırma" alt boyutunun da eklendiği dörtlü yapısı Türkçede daha önce kullanılmış olsa da [@temelAltanAtalay2018selfCompassion; @caliskanSari2018embuC], ana hipotez analizlerine geçmeden önce bu ölçek formlarının çalışmaya katılan ailelerde güvenilir sonuçlar verip vermediği özel olarak incelenmiştir. Bu ön hazırlık; anketin ebeveyn ile çocuk raporları için eşlenik olarak tasarlanmış olması ve diyabetli/sağlıklı aile yapısına ne derece uyduğunun teyit edilmesi amacıyla yürütülmüştür [@sumer2010anneBabaTutum; @mokkink2018cosmin]. Yönteme ilişkin matematiksel altyapı aşağıda ve detaylı sonuçlar Ek 7'de (@sec-ek-psikometri) sunulmuştur.

### Madde düzeyi çözümleme ve güvenirlik

Her alt ölçek için "Herkes 1 mi demiş?" (taban etkisi) veya "Çoğunluk çok mu yüksek puan vermiş?" (tavan etkisi) şeklinde dağılımlar kontrol edilmiştir. Anket sorularının tutarlılığı (güvenirliği) hesaplanırken sadece en yaygın yöntem (Cronbach alfa) kullanılmamış; sıralı anket yanıtlarında daha doğru sonuç verdiği bilinen ileri düzey katsayılar da (McDonald omega) dikkate alınmıştır [@dunn2014alphaOmega; @trizanoHermosilla2016omegaAlpha].

### Faktör yapısının sınanması

Ebeveynlik tutumundaki dört temel kuramsal kavramın (sıcaklık, koruma, reddetme, kıyaslama) veri setinde aynen oluşup oluşmadığı, yapısal eşitlik testleriyle (doğrulayıcı faktör analizi, WLSMV) incelenmiştir [@li2016ordinalCFA]. Kuramsal birleştirme için tek-boyut, dört-boyut veya genel/özgül faktör (bifaktör) modelleri sınanmış ve "Beklenen modelle elde edilen verinin uyumu ne kadardır?" sorusuna çeşitli indeksler (CFI, TLI, RMSEA, SRMR) kullanılarak yanıt aranmıştır [@huBentler1999cutoff]. Formlarda aynı ailedeki çocukların cevaplarının birbirine benzeme (yuvalanma) potansiyeli ayrıca göz önünde bulundurulmuştur.

### Bayesçi doğrulayıcı analiz

Doğrulayıcı analizde, anketin soruları arasındaki bazı küçük (artık/kovaryans) çapraz ilişkileri "kesinlikle sıfır" kabul etmenin küçük çalışma gruplarında yaratabileceği hata riskini dengelemek amacıyla, bu değerlerin "sıfıra çok yakın" (fakat tam sıfır değil) olduğu esnek önsel beklentilerle çalışan alternatif Bayesçi modelleme (BSEM) ek bir güvenlik testi olarak sisteme dâhil edilmiştir [@muthenAsparouhov2012bsem].

### Ölçüm eşdeğerliği

Puan karşılaştırmasının sağlıklı olabilmesi için, "Diyabet ailesindeki çocuk ile sağlıklı ailedeki çocuk, aynı anket sorusundan aynı anlamı mı çıkarıyor?" sorusu, eşdeğerlik (measurement invariance) analiziyle sınanmıştır [@putnickBornstein2016measurementInvariance; @chen2007invariance]. Bilgi veren rolleri arasında (indeks çocuk vs. kardeş) matematiksel eşdeğerliğin bozulduğu noktalar, yalnızca bir "anket ölçüm hatası" olarak değil; aynı evin içindeki farklı çocukların aynı ebeveyni gerçekten "farklı" hissettiğine dair tözsel bir işaret olarak yorumlanmıştır.

### Geçerlik ve raporcular arası uyum

Anketin gerçekten ölçmek istediğini ölçtüğünü kanıtlamak (ölçüt geçerliği) adına, anne depresif belirtileri ile "beklendiği gibi" ilişki kurup kurmadığına (örneğin depresyon artınca sıcaklık hissinin düşmesi) bakılmıştır [@fornellLarcker1981]. Annenin ebeveynlik davranışı hakkında aynı evin içinde indeks çocuk ve kardeşin verdiği iki farklı not arasındaki matematiksel uzlaşma düzeyi, sınıf-içi korelasyon ve klinik tanıya uygun yöntemlerle (Bland-Altman) belirlenmiştir [@blandAltman1986; @gwet2008ac1].

### Taban etkisi yönetimi ve sağlamlık

Annelerin çoğunun "Ben asla kötü bir ebeveyn değilim" diyerek olumsuz maddelere doğrudan "1" (en düşük) vermesi (taban yığılması) sonucu oluşabilecek matematiksel çöküntüler, farklı çözümleme senaryolarıyla (kategori daraltma, sorunlu madde çıkarma vb.) paralel olarak yürütülmüş ve sonuçların bu seçimlere karşı duyarlılığı (çok-evrenli analiz) sınanmıştır [@steegen2016multiverse]. Verideki "eksik" alanların rastgele mi bırakıldığı kontrol edilmiştir [@little1988mcar].

## Veri Toplama Süreci ve Veri Yönetimi"""
    }

    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            print("Successfully replaced section 3.7!")
        else:
            print("Failed to replace section 3.7!")

    with open("chapters/03_gerec_ve_yontem.qmd", "w", encoding="utf-8") as f:
        f.write(content)

process_file()
