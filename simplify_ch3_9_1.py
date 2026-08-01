import sys

file_path = "chapters/03_gerec_ve_yontem.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    """## İstatistiksel Analiz

Doğrulanmış kanonik veri seti üzerinde yürütülen çıkarımsal çözümlemede anlamlılık düzeyi çift yönlü α = 0,05 olarak belirlenmiştir. Çalışmada çok sayıda hipotez eşzamanlı olarak sınandığından, ortaya çıkabilecek yanlış-pozitif (tip-1 hata) riskini denetlemek amacıyla çözümleme katmanlarına özgü düzeltme stratejileri uygulanmıştır.

Çokluk düzeltmesinin tanımlandığı birim, birlikte değerlendirilen bir hipotez testleri kümesi olan *test ailesidir*. Bu istatistiksel anlamdaki "test ailesi", çalışmanın veri birimi olan sosyal aileden (anne–çocuk–kardeş) farklı ve bağımsız bir kavramdır ve izleyen metinde daima "test ailesi" olarak anılır. Bu doğrultuda iki test aileli bir çokluk düzeltmesi (*multiplicity correction*) stratejisi benimsenmiştir:

**Birincil çözümlemeler (FDR düzeltmesi).** Araştırmanın doğrulayıcı iskeletini oluşturan H1–H4 çözümlemelerinde, gerçek etkileri gözden kaçırmamak ve istatistiksel gücü korumak amacıyla Benjamini-Hochberg yanlış-keşif oranı (FDR) düzeltmesi uygulanmıştır [@benjaminiHochberg1995fdr].

**İkincil ve keşifsel çözümlemeler (Holm düzeltmesi).** Doğrulayıcı H1–H4 hattının dışında kalan keşifsel ve ikincil genişletme katmanları, bu hattın FDR test ailesinden ayrı tutularak ilgili çözümlemenin kendi test ailesi içinde Holm düzeltmesiyle ele alınmıştır [@holm1979]. Holm düzeltmesi, o test ailesinde en az bir yanlış-pozitif çıkma olasılığını (test ailesi düzeyinde hata oranını) denetler.

**Stratejik amaç.** Bu iki test aileli tercih, doğrulama hattında beklenen yanlış-keşif oranını denetleyerek görece daha çok gerçek etkinin yakalanmasını; keşifsel ve ikincil hatta ise test ailesi düzeyinde hata oranını daha sıkı denetleyerek yanlış-pozitif üretiminin sınırlanmasını amaçlar.

**Etki büyüklükleri ve önyükleme.** Etki büyüklükleri %95 güven aralığıyla, Bayesçi paralel hatta ise %95 güvenilir aralığıyla (*credible interval*) birlikte raporlanmıştır. Klasik varsayımların zayıf kalabileceği modellerde sonuçların kararlılığı önyükleme (*bootstrapping*) temelli yeniden örneklemeyle sınanmıştır. Önyükleme temelli güven aralıkları; aracılık ve koşullu süreç çözümlemelerinde dağılımdaki olası asimetriyi düzelten yanlılık düzeltilmiş-hızlandırılmış (BCa) yöntemle 1000 yineleme, ağ ve kalibrasyon çözümlemelerinde 1000 yineleme ve diadik oran kestiriminde 1000 yineleme üzerinden hesaplanmıştır.

### Tanımlayıcı istatistikler ve grup dengesi

Sürekli değişkenler ortalama ve standart sapma ile medyan ve çeyrekler arası aralık, kategorik değişkenler sayı ve yüzde ile özetlenmiştir. T1DM ve kontrol ailelerinin başlangıç özellikleri aile düzeyinde raporlanmıştır. Grup dengesizliği; örneklem büyüklüğüne duyarlı p değerinden bağımsız olarak, iki grubun bir değişkendeki uzaklığını doğrudan etki büyüklüğü ölçeğinde veren standardize ortalama fark (SMD) göstergesiyle değerlendirilmiştir [@austin2009balanceDiagnostics]. Bu tercih, "istatistiksel anlamlılık" ile "pratik denge" ayrımını görünür kılar: küçük bir grup farkı büyük örneklemde anlamlı çıkabilirken SMD, farkın gerçekte ne kadar büyük olduğunu p değerinden bağımsız gösterir.

### Eksik veri yönetimi

Eksik veri, tek bir algoritmaya bağlı kalınmadan üç çerçeveyle ele alınmıştır [@littleRubin2019missing]. Bu çoklu çerçevenin gerekçesi; eksik verinin nasıl işlendiğine ilişkin varsayımı görünür kılmak ve üç yöntemin aynı sonuca ulaşmasını, bulgunun eksik veri kararına duyarsızlığını gösteren bir sağlamlık kanıtı olarak kullanmaktır. Süreç şu adımlarla yürütülmüştür:

**Birincil çözümleme: tam bilgi maksimum olabilirlik ve çoklu atama.** Ana çözümlemeler, rastgele eksiklik (MAR) varsayımı altında tam bilgi maksimum olabilirlik (FIML)^[FIML: eksik satırları çözümlemeden atmak yerine tüm gözlemlerdeki mevcut bilgiyi kullanarak kestirim yapan yöntem.] [@endersBandalos2001fiml] ve çoklu atama (*multiple imputation*)^[Çoklu atama (*multiple imputation*): her eksik değeri tek bir tahminle değil, kestirim belirsizliğini yansıtacak biçimde çok sayıda olası değerle dolduran ve sonuçları birleştiren yöntem.] çerçeveleriyle yürütülmüştür. Çoklu atama, zincirli denklemlerle [@vanBuuren2011mice] 50 atanmış veri seti (m = 50) ve otuz iterasyon üzerinden yürütülmüştür. Atama yöntemleri rastgele değil, değişken türüne göre eşlenmiştir: sürekli değişkenlerde öngörücü ortalama eşleme^[Öngörücü ortalama eşleme: atanacak değeri yalnız parametrik bir modelden çekmek yerine, kestirilen değere en yakın gözlenen olgulardan çekerek değişkenin gözlenen dağılımını koruyan yöntem.], ikili değişkenlerde lojistik regresyon, sıralı değişkenlerde orantılı olasılıklar regresyonu. Yeniden üretilebilirlik için atama algoritmasında sabit bir tohum değeri kullanılmıştır.

**Tam-vaka karşılaştırması.** Eksik veri içeren gözlemlerin çözümlemeden tümüyle çıkarıldığı tam-vaka sonuçları birincil çözümleme olarak değil; bu yaklaşımın yol açtığı bilgi kaybını göstermek amacıyla tamamlayıcı olarak sunulmuştur.

**Rastgele olmayan eksikliğe karşı delta duyarlılığı.** MAR varsayımının ihlal edilmesi, yani verinin rastgele olmayan (MNAR) bir sistematikle eksik kalmış olması olasılığına karşı ek bir dayanıklılık sınaması yapılmıştır. Atanmış değerlere önceden tanımlı sistematik kaymalar (delta) eklenerek sonucun bu kaymalara duyarlılığını ölçen delta tabanlı duyarlılık çözümlemesi uygulanmıştır.

**Yapısal eksiklik kısıtı.** Tasarım gereği kontrol grubunda bulunmayan HbA1c ve diyabet süresi alanları bir veri kaybı değil, yapısal eksik (*structural missing*) kabul edilmiştir. Mantıksal tutarsızlığa yol açmamak için bu alanlarda atama tüm örnekleme değil, yalnız T1DM grubundaki çözümsel eksik hücrelerle sınırlandırılmıştır.

### Nedensel çıkarım çerçevesi

Birincil ayarlanmış (koşullu-ilişki) modellerde hangi değişkenlerin istatistiksel olarak kontrol edileceği, önceden çizilen bir nedensel diyagramla (*Directed Acyclic Graph*, DAG) belirlenmiştir [@textor2017dagitty]. Bu diyagram, ayarlanması gereken değişken kümesini —arka-kapı kümesini— tanımlar.^[Arka-kapı kümesi (*backdoor set*): maruziyet ile sonuç arasında ortak-neden üzerinden uzanan nedensel-olmayan yolları kapatmak için ayarlanması gereken kovaryat kümesi.] Buradaki "toplam-etki" nitelemesi, bu kümenin ayarlanması anlamındadır. Ancak merkez ve veri toplama dönemi, grup üyeliğiyle örtüşen bir seçilim düğümü (*selection node*, S) oluşturur. Çözümleme bu seçilim yapısı üzerinde koşullandığından, T1DM'nin toplam nedensel etkisi bu tasarımda nokta-tanımlanabilir değildir.^[Nokta-tanımlanabilir (*point-identified*) olmak: nedensel etkinin tek bir sayısal değerinin veriden benzersiz biçimde geri kazanılabilmesi.] Merkez ve dönem, klasik anlamda ortak-neden bir karıştırıcıdan çok, üzerinde koşullanılan bir seçilim mekanizması gibi davranır (bkz. @fig-causal-dag). Bu nedenle raporlanan grup katsayıları, tanımlanmış bir toplam nedensel etki değil, gözlenen karıştırıcılar için ayarlanmış koşullu ilişkiler olarak okunmalıdır. Uygulanan diyagramda sosyoekonomik durum, kardeşler arası yaş farkı ve aile büyüklüğü başlangıç/tasarım karıştırıcıları olarak ele alınmıştır. Anne antidepresan kullanımı, anne depresif belirti düzeyi ve ebeveynlik tutumu ise birincil ayarlanmış modellerde ayarlanmamış, aracılık ve duyarlılık çözümlemelerinde ayrıca değerlendirilmiştir. Anne yaşı, H1 çocuk-algısı birincil ayarlanmış modelinin kovaryat setine bilinçli olarak dâhil edilmemiştir. Uygulanan diyagramda, anne yaşının çocuğun *algıladığı* ebeveynlik üzerindeki etkisinin sosyoekonomik durum, kardeş yaş farkı ve aile büyüklüğü aracılığıyla taşındığı varsayılmıştır. Bu üç ardıl (aracı) değişken ayarlandığında anne yaşının çocuk algısı ile grup arasında açık bırakılmış bir arka-kapı yolu oluşturmadığı varsayılmıştır. Buna karşılık H3 (anne öz-bildirimi) ve H4 (anne depresyonu ↔ ebeveynlik) modellerinde sonuç doğrudan anneye ait olduğundan anne yaşı olası bir ortak-neden konumundadır ve bu iki modelde kovaryat olarak ayarlanmıştır. Anne yaşı örneklemde sınırda dengesiz olduğundan (SMD ≈ 0,21; Bulgular, @tbl-apa-sample-characteristics), H1 sonucunun bu karara duyarlılığı, çoklu-evren (multiverse) çözümlemesinin anne yaşı ve anne depresif belirti düzeyini ekleyen *genişletilmiş* kovaryat kolunda ayrıca sınanmıştır (bkz. §@sec-cok-evren). Aynı diyagram kararına bağlı olarak bir eğilim skoru hattı kurulmuştur [@rosenbaumRubin1983propensity; @austin2011propensityIntro].^[Eğilim skoru (*propensity score*): gözlenen kovaryatlar verildiğinde bir ailenin T1DM grubunda yer alma olasılığı.] Birincil modelde bu olasılık sosyoekonomik durum, yaş farkı ve çocuk sayısı üzerinden kestirilmiştir. Grupları ölçülen değişkenlerde dengelemek için bu olasılığın tersiyle ağırlıklandıran kararlılaştırılmış ters-olasılık ağırlıkları (IPTW), uç eğilim skorlu birkaç ailenin aşırı büyük ağırlıklarının kestirim varyansını şişirmesini sınırlamak amacıyla 99. persentilde budanmıştır [@austinStuart2015iptw]. Birebir en yakın komşu eşleştirmesi lojit skor üzerinde değerlendirilmiştir. Hem ağırlıklandırmayı hem kovaryat ayarlamasını birlikte kullanarak model yanlış belirlenmesine karşı ek koruma sağlayan çift-sağlam (*doubly robust*) kovaryat ve ağırlık planı önceden belirlenmiştir. Bu hat nedensellik iddiası kurmaz ve randomizasyon üretmez; gözlemsel karşılaştırmada yalnız gözlenen karıştırıcıların etkisini azaltmaya yönelik bir tasarım katmanıdır.""" :
    """## İstatistiksel Analiz

Bulguların anlamlılığını belirlerken standart istatistiksel sınır (p < 0,05) kullanılmıştır. Ancak bu çalışmada bir sürü iddiayı (hipotezi) aynı anda test ettiğimiz için, sırf tesadüf eseri bazı sonuçların "anlamlı" çıkma ihtimali (yanlış-pozitif) yüksektir. İstatistiğin kendi kendini kandırmasını engellemek için, ana hipotezleri (H1–H4) topluca test ederken özel bir "yanlış-keşif" düzeltme filtresi (FDR) kullanılmıştır [@benjaminiHochberg1995fdr]. İkincil veya "merak edip baktığımız" (keşifsel) analizler ise bu ana gruptan ayrılarak, tamamen kendi içlerinde daha da sıkı bir teste (Holm düzeltmesi) tabi tutulmuşlardır [@holm1979]. 

Bulduğumuz farkların sadece "var" olduğunu söylemekle yetinmeyip, gerçekte "ne kadar büyük" olduklarını göstermek için %95 güven aralıkları (ya da Bayesçi güvenilir aralıklar) sunulmuştur. Formüllerin veya klasik yöntemlerin şüpheli kalabileceği zor modellerde ise, bilgisayara veriyi 1000 kez yeniden dağıtıp hesaplatarak (bootstrap yöntemi) sonuçların tesadüf olmadığı kesinleştirilmiştir.

### Tanımlayıcı istatistikler ve grup dengesi

Hastaların yaşları ve anket puanları gibi sayısal değerler ortalamalarla, meslek gibi kategorik veriler ise yüzdelerle özetlenmiştir. İki grubun (diyabetli ve sağlıklı aileler) birbirine başlangıçta ne kadar denk olduğunu ölçmek için basit p değerlerine güvenilmemiş; direkt olarak "aralarındaki fark istatistiksel olarak ne kadar büyük" (SMD) olduğuna bakılmıştır [@austin2009balanceDiagnostics]. Çünkü kocaman bir örneklemde, zerre kadar bir fark bile sırf kalabalıktan dolayı "anlamlı" çıkabilir. SMD bu yanılsamayı önler.

### Eksik veri yönetimi

Anketlerde bazı soruların boş bırakılması (eksik veri) sık rastlanan bir sorundur. Biz bu boşlukları tek bir yöntemle değil, tam üç farklı yöntemle [@littleRubin2019missing] sınayarak sonuçların değişmediğini teyit ettik:
1. **İleri düzey tamamlama:** Boşluklar basitçe ortalamayla doldurulmamış, verinin geri kalan yapısına bakılarak her eksik için 50 farklı mantıklı tahmin (çoklu atama) üretilmiştir [@vanBuuren2011mice; @endersBandalos2001fiml].
2. **Eksikleri atma (Tam-vaka):** Boşluk bırakan aileler tamamen silinmiş ve sadece "her soruyu dolduran" ailelerle analiz tekrarlanmıştır.
3. **Kötü senaryo (MNAR) testi:** "Ya bu eksikler tesadüf değilse ve belirli bir sebepten gizlenmişse?" varsayımıyla, atanan değerler zorla kötüleştirilerek (delta) analizin çöküp çökmediği sınanmıştır.

*Not: Sağlıklı çocukların kan şekeri (HbA1c) sorusunu boş bırakması bir "veri kaybı" değil, grubun doğasıdır (yapısal eksiklik). O yüzden bu tarz durumlar boş veri sayılmamıştır.*

### Nedensel çıkarım çerçevesi

Diyabetin çocuk üzerindeki etkisini ararken, aslında farkı yaratan şey diyabet değil de "annenin daha yaşlı veya gelirin daha düşük olması" çıkmasın diye, sürece etki eden her şey bir Nedensel Diyagram (DAG) haritasında baştan çizilmiştir [@textor2017dagitty]. Hastalık ile çocuk arasındaki, diyabet dışı o sinsi ve yanıltıcı yollar (arka-kapı kümesi) bu sayede kapatılmıştır. 

Bunu yapmak için, ailelerin gelir durumu, kardeşlerin yaş farkı ve evdeki toplam çocuk sayısı "karıştırıcı dış etken" (kovaryat) kabul edilip hesaptan düşülmüştür. Annenin yaşı, çocuğun kendi hislerini pek etkilemediği için çocuk testlerine dâhil edilmemiş; ancak annenin "kendi hakkındaki beyanlarında" anneyi etkileyebileceği için anne anketlerinin hesabında dengelenmiştir.

Üstelik bu düzeltmeler sadece değişken ekleyerek bırakılmamış; hangi ailenin diyabet grubunda olmaya ne kadar "meyilli" olduğunu (eğilim skoru) hesaplayan ikinci bir istatistik zırhı daha kullanılmıştır [@rosenbaumRubin1983propensity; @austin2011propensityIntro]. Yani "çift korumalı" (hem ağırlıklandırma hem de değişken ayarlama) bir hesaplama yapılarak, farkların sadece diyabet durumundan kaynaklandığı büyük ölçüde güvenceye alınmıştır [@austinStuart2015iptw]. Tabi ki bu hiçbir zaman kusursuz bir "sebep-sonuç" ispatı değildir, sadece dış etkenlerin sis perdesini en aza indiren bir gözlem stratejisidir."""
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success!")
    else:
        print("Failed to find:\n" + old[:100] + "...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
