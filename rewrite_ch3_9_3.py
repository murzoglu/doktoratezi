import re

def process_file():
    with open("chapters/03_gerec_ve_yontem.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        # Duyarlılık ve sağlamlık çözümlemeleri
        """### Duyarlılık ve sağlamlık çözümlemeleri {#sec-cok-evren}

H1–H4 birincil bulguları için çok yönlü bir sağlamlık taraması standart gereksinim olarak uygulanmıştır. Tek bir spesifikasyona dayanan sonuç kırılgan olabileceğinden, çok evrenli (*multiverse*) çözümleme; alt ölçek, kovaryat seti, kestirim yöntemi ve alt örneklem seçimlerinin makul tüm birleşimlerini sistematik biçimde kurup etki büyüklüğü ve p değeri dağılımlarını özetlemiştir [@steegen2016multiverse]. Anne öz-bildirimi (H3/EMBU-P) çok-evren çözümlemesinde kovaryat boyutu, giderek genişleyen beş iç-içe kovaryat setinden oluşur:

- *asgari* — yalnız anne yaşı;
- *+SES* — anne yaşı ve sosyoekonomik durum;
- *+yaş farkı* — buna kardeş yaş farkının eklenmesi;
- *+aile büyüklüğü* — buna çocuk sayısının eklenmesi;
- *tam set* — buna anne antidepresan kullanımının eklenmesi.

Bu kovaryat boyutu, kestirim yöntemi (en küçük kareler [EKK] ve dirençli robust regresyon) ve alt örneklem (tümü, iki+ çocuklu aileler, antidepresan kullanmayanlar) boyutlarıyla çaprazlanır. Çocuk algısı (H1/EMBU-C) tarafında ise kovaryat boyutu üç iç-içe setten oluşur:

- *asgari* (yaş, cinsiyet);
- *DAG-gerekçeli* (birincil H1 kovaryat seti: yaş, cinsiyet, SES, yaş farkı, çocuk sayısı);
- *genişletilmiş* (birincil sete anne yaşı ve anne depresif belirti düzeyinin eklenmesi).

Bu son kol P1-14 kapsamında anne yaşı ayarının H1 sonucuna etkisini doğrudan sınayan duyarlılık koludur. Anlamsız bir p değeri "fark yok" demek olmadığından eşdeğerlik testi kullanılmıştır. Bu test, etkiyi önceden belirlenen en küçük anlamlı etki büyüklüğü (±0,30 SMD) bandı içinde tutarak "pratikte eşdeğer" iddiasını aktif biçimde sınayan iki tek-yönlü test (TOST) işlemiyle önemsizlik/eşdeğerlik kararlarını vermiştir [@lakens2017equivalence]. Eşdeğerlik sınırı (SESOI) olarak, ebeveynlik yazınında küçük etkinin alt eşiği kabul edilen ve @pinquart2013 meta-analitik büyüklükleriyle uyumlu ±0,30 SMD Cohen konvansiyonu esas alınmıştır; EMBU alt ölçekleri için ampirik doğrulanmış, ölçeğe özgü bir klinik anlamlılık eşiği bulunmadığından bu sınır ihtiyatlı bir varsayılan olarak konumlanır. TOST işlemi iki grubun ham (kovaryat-ayarsız) standardize ortalama farkı üzerinde işletildiğinden H3 birincil/IPTW modelinin kovaryat-ayarlı standardize katsayısıyla (β) birebir aynı tahmin-hedefini (*estimand*) taşımaz; eşdeğerlik kararları bu nedenle ayarlı model bulgularıyla birlikte, tamamlayıcı bir kanıt katmanı olarak yorumlanır. Gözlemsel tasarımda her karıştırıcı ölçülemeyeceğinden, ölçülmemiş bir karıştırıcının bulguyu silebilmek için ulaşması gereken gücü niceleyen sağlamlık değeri (RV) ve E-değeri birlikte raporlanmıştır [@cinelliHazlett2020sensemakr; @vanderweeleDing2017evalue]. Etkinin kuramsal olarak beklenmediği yerde sahte sinyal üretilip üretilmediğini sınayan negatif kontrol [@lipsitch2010negativeControls] ve önceden belirlenmiş yanlışlama (*falsification*) testleri yapısal yanlılık taramasını tamamlamıştır. İki merkezli alım nedeniyle olası parti (*batch*)/dönem etkisi ve seçilim yanlılığı ayrı bir geçerlik denetimiyle incelenmiştir. Merkez bilgisi analiz veri setinde ayrı bir değişken olarak kodlanmadığından bu denetim merkeze göre katmanlı yürütülememiş; bunun yerine alım yılı (*recruitment year*) üzerinden dönem/parti duyarlılığı ve HbA1c erişilebilirliğine bağlı olası seçilim etkisi değerlendirilmiştir.

### Bayesçi paralel hat

H1 ve H3 birincil bulguları, frekansçı raporlamaya ek olarak Bayesçi paralel hatla da değerlendirilmiştir. Frekansçı yaklaşım "etki yoktur" sonucunu doğrudan ifade edemediğinden, Bayesçi hat "kanıt yetersizliği" ile "etki-yokluğu lehine kanıt" ayrımını netleştirmek amacıyla eklenmiştir. Çok düzeyli Bayesçi modeller, ebeveynlik ve kronik hastalık alanındaki meta-analitik etki büyüklüklerinden esinlenen zayıf bilgi verici önseller kullanmıştır [@pinquart2013].

Sonuç değişkenleri ham EMBU alt ölçek puanı (1–4) birimindedir; dolayısıyla önseller ve grup katsayıları da bu ham ölçek puanı biriminde tanımlıdır. @pinquart2013 meta-analizindeki etkiler standardize (Cohen d/Hedges g) birimde olduğundan, önsel merkezleri yön ve kaba büyüklük bilgisini yansıtan zayıf bilgi verici çıpalar olarak kullanılmıştır. Standardize etkinin ham ölçeğe birebir cebirsel dönüşümü (g × sonuç SD) uygulanmamış; bunun yerine gözlenen alt ölçek dağılımlarıyla uyumlu, sıfır çevresinde geniş kütle bırakan Normal(·; 0,50) önselleri tercih edilmiştir. Bu genişlik (SD = 0,50), 1–4 ham ölçeğinde |0| ile |1| puanlık grup farkları arasındaki geniş bir aralığa gözle görülür önsel olasılık atar; dolayısıyla önsel, keskin bir nokta-tahmin dayatmayan genel amaçlı zayıf bilgi verici bir önsel olarak nitelenir.

Grup katsayısı, kontrol grubu referans alınarak DM grubunu karşılaştıran farkı temsil eder; her alt ölçekte yüksek puan ilgili yapının (sıcaklık, aşırı koruma, reddetme, karşılaştırma) daha yüksek düzeyini gösterir. Bu katsayı için önsel, H1'de sıfıra yakın hafif pozitif merkezli Normal(0,20; 0,50) olarak tanımlanmıştır. H3'te ise literatürden esinlenen zayıf bilgi verici çıpalar kullanılmıştır: sıcaklık 0,20; aşırı koruma 0,30; reddetme −0,15; karşılaştırma 0,10; tümünde standart sapma 0,50. Bu merkezlerden aşırı korumanın pozitif yönü, kronik hastalıkta artan aşırı koruma bulgusuyla doğrudan uyumludur (@pinquart2013; g ≈ 0,39). Buna karşılık sıcaklık için seçilen sıfıra yakın hafif pozitif çıpa, @pinquart2013'ün bildirdiği küçük negatif sıcaklık etkisinin (g ≈ −0,22) tersi yönde olup Pinquart yönünün birebir aktarımı değil, T1DM ailelerinde telafi edici sıcaklık/destek beklentisini yansıtan tözsel bir tercihtir. SD = 0,50 genişliği her iki yöne de geniş olasılık bıraktığından bu çıpalar veriyle kolayca güncellenir; nitekim önsel-genişliği duyarlılığı (aşağıda) sonucun bu seçime kararlılığını göstermektedir.

Savage-Dickey Bayes faktörü önsel genişliğine duyarlı olduğundan, H1 reddetme bulgusu için önsel standart sapması 0,25, 0,50 ve 1,00 değerlerinde yeniden hesaplanarak Bayes faktörünün önsel genişliğine göre kararlılığı raporlanmıştır. Önsel genişliğine ek olarak, önsel merkezine duyarlılık da sınanmıştır: H1 reddetme, H3 sıcaklık ve H3 reddetme için grup katsayısı önseli üç merkezde (skeptik 0; literatür yönü; ters yön) yeniden kestirilmiş ve BF₁₀ ile sonsal yön olasılığının bu seçime kararlılığı raporlanmıştır (Ek 6, @tbl-apa-prior-center). Diğer regresyon katsayıları için sıfır merkezli Normal(0; 0,50), kesişimler için Normal(0; 2) ve varyans/ölçek parametreleri için student-t(3; 0; 2,5) önselleri kullanılmıştır.

Bayes faktörü, sıfır noktasında önsel ile sonsal yoğunluğun oranına dayanan Savage-Dickey yoğunluk oranıyla [@wagenmakers2010] (önsel standart sapma 0,50) hesaplanmıştır. Kestirim dört zincir, zincir başına 4000 yineleme (ilk 1500 yineleme ısınma) ile Stan arka ucu üzerinden yürütülmüştür [@burkner2017brms]. Her model için sonsal dağılım, %95 güvenilir aralık, etkinin önemsiz sayılan bir bant içinde kalma payını veren pratik eşdeğerlik bölgesi (ROPE) payı [@kruschke2018rope], sonsal yön olasılığı, verinin "etki var" hipotezini "etki yok" hipotezine göre kaç kat daha olası kıldığını niceleyen Bayes faktörü ve model karşılaştırma ölçütleri raporlanmıştır. Yakınsama kontrolü; zincirlerin uzlaşmasını ölçen, rank-normalize edilmiş uzlaşma istatistiği (R̂ < 1,01) [@vehtari2021rhat], ıraksayan geçiş (*divergent transition*)^[Iraksayan geçiş (*divergent transition*): örnekleyicinin sonsal dağılımın yüksek eğrilikli bir bölgesini güvenilir biçimde tarayamadığını işaret eden, kestirim güvenilirliğine ilişkin uyarı sinyali.] yokluğu ve tanı eşikleriyle yapılmıştır.

### Tamamlayıcı ve keşifsel çözümleme katmanları

Aşağıdaki çözümleme katmanları birincil hipotez sınamalarına değil, örüntülerin derinleştirilmesine yöneliktir; tümü **keşifsel/post-hoc** olarak etiketlenmiş, hiçbiri doğrulayıcı çekirdeği değiştirmez ve korelasyonel dille sınırlıdır. Bu tamamlayıcı çözümleme beş temel aile altında toplanır. *Aracılık* hattı, anne depresif belirti düzeyinden ebeveynlik alt ölçeklerine giden dolaylı yolları — bir ilişkinin üçüncü bir değişken üzerinden aktarılıp aktarılmadığını — tek-aracılı, çok düzeyli ve koşullu süreç modelleriyle değerlendirmiştir [@hayes2018introduction]. Bu dolaylı yolların ölçülmemiş bir aracı-sonuç karıştırıcısına duyarlılığı ayrıca sınanmıştır [@imaiKeeleYamamoto2010mediationDuyarlilik]. *Latent tipoloji* hattı, benzer yanıt örüntülerine sahip latent anne alt gruplarını arayan latent profil çözümlemesi ve bifaktör (*bifactor*) modelle incelenmiştir. *Ağ* hattı, değişkenler arasındaki koşullu (diğer tüm değişkenler sabit tutulduğunda kalan) bağımlılık yapısını gösteren düzenlileştirilmiş kısmi korelasyon ağları ve grup karşılaştırma testiyle yürütülmüştür; koşullu bağımlılık nedensellik olarak yorumlanmamıştır. *Klinik fayda* hattı, yüksek depresif belirti düzeyinin *eşzamanlı* (kesitsel) sınıflandırması için lojistik sınıflandırma modeli, ayrım gücünü ölçen ROC ve klinik net faydayı değerlendiren karar-eğrisi çözümlemesiyle [@vickersElkin2006dca] tarama/sınıflandırma modelleri üretmiştir; belirteçler ile sonuç aynı ölçüm anında toplandığından bu bir ileriye dönük risk yordama modeli değildir. Belirleyicilerin göreli önemini betimlemek için ayrıca sınıflandırma-regresyon ağacı (CART) ve rastgele orman (*random forest*) çözümlemeleri tamamlayıcı olarak uygulanmıştır. Son olarak *DM'ye özgü* keşifsel alt çözümlemeler, HbA1c ile ebeveynlik etkileşimini, diyabet süresinin doğrusal olmayan biçimini ve tanı yaşı katmanlarını incelemiştir. HbA1c verisinin yalnız 39 T1DM indeks çocukta bulunması nedeniyle bu çözümlemeler atama uygulanmaksızın ve sınırlı örneklem uyarısıyla, yalnız betimsel olarak raporlanmıştır.

Bu beş aile, mevcut değişkenler arasındaki örüntüleri içerik düzeyinde derinleştirir. İkinci bir küme ise örüntüleri değil ölçüm modelinin kendisini genişletmeye odaklanır. Bu ön-kayıtlı ölçüm-genişletme katmanları; çoklu bilgi verici ortak ölçüm modelini (trifaktör), keşfedici yapısal eşitlik modelini, taban etkisine duyarlı madde tepki kuramını, hiyerarşik/iki-faktörlü güvenirlik genellemesini, latent bilgi verici uyumsuzluğu modelini, nedensel aracılık duyarlılığı ile nedensel diyagramın ima ettiği koşullu bağımsızlıkların veriyle sınanmasını, çok-özellikli çok-yöntemli diadik modeli ve sosyal katmanlaşma, maternal komorbidite, aile yapısı ile seçilim/merkez geçerliği çözümlemelerini kapsar. Bu genişletme çözümlemelerinin ayrıntılı tanımı ve çıktıları Bulgular bölümünün keşifsel katmanında sunulmuştur (bkz. [-@sec-kesifsel-genisletme]).""":
        
        """### Duyarlılık ve sağlamlık çözümlemeleri {#sec-cok-evren}

Birincil hipotezlerin (H1-H4) bulgularını güvenceye almak amacıyla, sonuçların yalnızca seçilen bir analiz formülüne bağlı kalıp kalmadığını test eden "çok evrenli" (multiverse) analizler yürütülmüştür [@steegen2016multiverse]. Bu analizlerde; hesaplamaya yaşın veya gelir durumunun eklenmesi, farklı varsayımların veya farklı hasta alt gruplarının kullanılması gibi binlerce olası kombinasyon sistematik olarak aynı anda test edilmiştir.

Klasik p-değeri, anlamlı bir fark bulunamadığında iki grubun "tamamen eşit" olduğunu kanıtlamaz; yalnızca farkın kanıtlanamadığını söyler. Bunu aşmak ve gruplar arasında gerçekten klinik olarak anlamlı bir fark olmadığını pozitif bir şekilde göstermek amacıyla, istatistiksel eşdeğerlik (TOST) testleri de uygulanmıştır [@lakens2017equivalence]. Eşdeğerlik için alt sınır olarak ebeveynlik literatüründe "küçük etki" olarak kabul edilen ±0,30 SMD değeri (yaklaşık %30 standart sapma farkı) kullanılmıştır [@pinquart2013]. 

Ayrıca, dışarıdan gelen ve ankette ölçülmemiş gizli bir değişkenin mevcut sonuçları bozabilmesi için ne kadar güçlü olması gerektiğini saptayan sağlamlık (E-değeri) ölçümleri yapılmıştır [@cinelliHazlett2020sensemakr; @vanderweeleDing2017evalue]. Ailelerin anket doldurdukları zaman dilimi veya merkez farklarının genel tabloyu bulandırma olasılığı da ayrıca sınanmıştır [@lipsitch2010negativeControls].

### Bayesçi paralel hat

Klasik (frekansçı) istatistik, "gruplar arasında fark yoktur" sonucunu doğrudan ifade edemediği için, bu boşluğu kapatmak adına birincil hipotezler Bayesçi modellerle de paralel olarak sınanmıştır. Bayesçi yöntem, T1DM ve ebeveynlik konusundaki güncel dünya literatürünü modele bir "ön bilgi" (zayıf bilgi verici önsel) olarak dâhil eder [@pinquart2013]. Modeller (Stan arka ucu kullanılarak) binlerce kez simüle edildikten sonra; farkların "güvenilir bir aralıkta" kalıp kalmadığı, etki olmamasının "pratikte eşitlik" (ROPE) bölgesine ne kadar düştüğü ve verilerin "fark yoktur" olasılığını ne ölçüde desteklediği Bayes Faktörü (BF) ile kesin olarak raporlanmıştır [@wagenmakers2010; @burkner2017brms; @kruschke2018rope; @vehtari2021rhat].

### Tamamlayıcı ve keşifsel çözümleme katmanları

Aşağıda belirtilen analiz katmanları temel soruları doğrulamak için değil, örüntülerin daha derinine inerek yeni klinik ipuçları aramak (keşifsel/post-hoc) amacıyla tasarlanmıştır. Çıkan sonuçlar doğrudan nedensellik kurmaz, korelasyon düzeyi öneriler sunar:

- **Aracılık (Mediation):** Annenin diyabet tanısı nedeniyle yaşadığı depresyonun, doğrudan mı yoksa annenin reddedici tutumlarını artırarak mı çocuğu etkilediğini test eden "köprü/aktarım" yolları incelenmiştir [@hayes2018introduction; @imaiKeeleYamamoto2010mediationDuyarlilik].
- **Latent Tipoloji:** Annelerin anketlere verdikleri yanıtlardan yola çıkarak, anneleri benzer tutum profillerine göre gruplara ayıran sınıflandırma modelleri kurulmuştur.
- **Ağ (Network) Çözümlemesi:** Farklı duyguların (örneğin depresyon, sıcaklık, rekabet) diğer tüm dış etkenler sabitlendiğinde dahi birbirini nasıl etkilediğini gösteren çoklu bağ haritaları oluşturulmuştur.
- **Klinik Fayda ve Karar Eğrisi:** Poliklinikte sadece ebeveynlik tutumlarına bakarak annenin belirgin bir depresif risk taşıyıp taşımadığını tahmin eden sınıflandırma (ROC ve Karar Eğrisi) algoritmaları geliştirilmiştir [@vickersElkin2006dca].
- **DM'ye Özgü Etkiler:** İndeks çocuğun HbA1c düzeyinin veya diyabet süresinin ailenin hissettiği ebeveynliği nasıl etkilediği, sadece kan şekeri verisi bulunan 39 ailelik dar grupta keşifsel olarak değerlendirilmiştir.

Bunun yanı sıra, testlerin sadece ilişkileri değil ölçüm modelinin kendisini de genişlettiği ileri psikometrik (Örn. trifaktör modeller, güvenirlik genellemesi) analizler uygulanmıştır. Elde edilen tüm keşifsel bulgular, çalışmanın yan çıktıları olarak Bulgular bölümünün keşifsel katmanında (bkz. [-@sec-kesifsel-genisletme]) detaylandırılmaktadır."""
    }

    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            print("Successfully replaced section 3.9 last parts!")
        else:
            print("Failed to replace section 3.9 last parts!")

    with open("chapters/03_gerec_ve_yontem.qmd", "w", encoding="utf-8") as f:
        f.write(content)

process_file()
