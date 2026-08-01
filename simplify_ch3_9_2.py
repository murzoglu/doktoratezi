import sys

file_path = "chapters/03_gerec_ve_yontem.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    """### Hipotez temelli modeller

Beş hipotezin çözümleme düzeyi, Araştırma Tasarımı başlığında tanımlanan iç içe aile yapısına göre belirlenmiştir. Çocuk-satırı gözlemlerinin aynı aile içinde yuvalandığı modellerde aile rastgele etkisi ya da aile bazında kümelenmiş standart hata zorunlu tutulmuştur. Aile düzeyinde tanımlı yapılar (anne öz-bildirimi gibi) doğrudan aile-satırında modellenmiştir. Çift-içi karşılıklı bağımlılık ise aktör–partner çerçevesinde ele alınmıştır. Aşağıdaki alt başlıklar her hipotezin birincil modelini ve genişletme hattını bu düzey kararıyla tutarlı biçimde tanımlar. @tbl-analiz-plani, beş doğrulayıcı hipotezin çözümleme düzeyini, birincil modelini, temel kovaryatlarını ve çoklu karşılaştırma düzeltmesini tek bakışta özetlemektedir; her satırın ayrıntılı gerekçesi izleyen alt başlıklardadır.

| Hipotez | Sonuç değişkeni | Birincil model | Temel kovaryatlar | Çoklu düzeltme |
|---|---|---|---|---|
| **H1** | s-EMBU-C (çocuk algısı) | Çok düzeyli model (aile rastgele etkisi) | Rol, yaş, cinsiyet, SES, yaş farkı, çocuk sayısı | BH-FDR |
| **H2** | KİA 4 boyut (kardeş ilişkisi) | Welch t + APIM karma model + diadik CFA | Yaş farkı, aynı cinsiyet | BH-FDR |
| **H3** | s-EMBU-P (anne öz-bildirimi) | Kovaryans analizi + eğilim skoru (HC3 sağlam standart hata) | Grup, anne yaşı, SES, yaş farkı, çocuk sayısı | BH-FDR |
| **H4** | Anne depresyonu ↔ ebeveynlik | WLSMV ordinal SEM (latent) | Anne yaşı, SES | BH-FDR |
| **H5** | Anne–çocuk diadik uyum | 5 paralel strateji (ICC/Bland-Altman, yüzey tepki, ortak yazgı, diadik CFA, Kenny k [APIM türevi aktör/partner oranı]) | Diyad türü, alt ölçek | Aile içi (≥3 strateji ölçütü) |

: Doğrulayıcı hipotezlerin çözümleme planı özeti (birincil hat). Genişletme/keşifsel katmanlar için bkz. bulgular bölümü. {#tbl-analiz-plani}

**H1 – Çocuk algısı.** Çocuğun algıladığı ebeveynlik tutumu (s-EMBU-C alt ölçekleri), çocuk-satırı uzun formatında modellenmiştir. Aynı aileden iki çocuk gözlemi geldiği için bu gözlemler istatistiksel olarak bağımsız değildir. Birincil model bu nedenle rol, çocuk yaşı, cinsiyet, sosyoekonomik durum, kardeşler arası yaş farkı ve çocuk sayısı sabit etkilerini ve aile içi bağımlılığı yapının içine alan aile numarasını rastgele etki olarak içeren çok düzeyli bir modeldir [@hox2017multilevel]. Bu yapı kullanılmadığında standart hatalar olduğundan küçük kestirilerek yanlış-pozitif riski artacağı için aile rastgele etkisi zorunlu görülmüştür. Genişletme hattında rol × yaş × cinsiyet etkileşimi ile reddetme alt ölçeği için, ölçek toplam puanı yerine madde-bilgi fonksiyonlarını kullanarak taban/tavan etkilerine dayanıklı bir latent yetenek (θ) skoru üreten dereceli yanıt (*graded response*) madde tepki kuramı modeli değerlendirilmiştir [@samejima1969graded]. Aynı genişletme hattında, ön-kayıtlı grup ana etkisinden ayrı, keşifsel/post-hoc bir estimand olarak grup-içi (aile-içi) rol kontrastı da tanımlanmıştır: kontrol kolu dışlanarak aynı ailenin indeks çocuğu ile sağlıklı kardeşi doğrudan karşılaştırılmakta, simetrik olarak kontrol ailesi içindeki indeks-kardeş farkı da kestirilmektedir. Bu kontrastlar aynı çok düzeyli modelin dört düzeyli rol faktöründen türetilir ve doğrulayıcı düzeltilmiş anlamlılık iddiası taşımaz.

**H2 – Kardeş ilişkisi.** Kardeş İlişkileri Anketi'nin sıcaklık/yakınlık, statü/güç, çatışma ve rekabet boyutları kullanılmış; grup farkı tek bir modele bağlı bırakılmayıp üç paralel stratejiyle değerlendirilmiştir. Aile-ortalaması karşılaştırmaları, klasik Student t-testinin iki grupta eşit varyans (varyans homojenliği) varsayımını gerektirmediğinden gruplar farklı yayılıma sahip olsa da geçerliliğini koruyan Welch t-testi ve Hedges g etki büyüklüğüyle yürütülmüştür. Aynı çiftteki iki kardeşin raporu birbirinden bağımsız olmadığından, çocuk-satırı diadik çözümlemeler; her çocuğun kendi (aktör) ve kardeşinin (partner) özelliğinden gelen etkiyi ayıran aktör–partner karşılıklı bağımlılık modeli çizgisinde karma modelle ele alınmıştır [@kennyKashyCook2006]. Kardeş yaş farkı ve aynı cinsiyet düzenleyici etkileri aile-ortalaması doğrusal modeliyle değerlendirilmiştir. Ayırt edilebilir diyad doğrulayıcı faktör analizi ise indeks ve kardeş rollerini ayrı ama bağlı latent değişkenler olarak modelleyip aralarındaki ilişkiyi, ölçüm hatasının ayrı bir bileşen olarak modellenmeye çalışıldığı latent düzeyde raporlamıştır [@olsenKenny2006interchangeableDyads].

**H3 – Anne öz-bildirimi.** Annenin öz-bildirdiği ebeveynlik tutumu (s-EMBU-P alt ölçekleri) aile düzeyinde modellenmiştir. Birincil kovaryans analizi grup, anne yaşı, sosyoekonomik durum, yaş farkı ve çocuk sayısını içermiştir. Antidepresan kullanımı, grup etkisiyle ebeveynlik arasında aracı konumda olabileceği için birincil ayarlanmış modele kovaryat olarak eklenmemiştir (aracı bir değişkeni ana modele koymak etkinin bir kısmını görünmez kılabilir). Bunun yerine antidepresan ayarlı model ve kullanan/kullanmayan alt gruplarla duyarlılık çözümlemeleri yürütülmüştür. Eğilim skoru sürümü, budanmış ağırlık ve gözlemler arası değişen varyansa dayanıklı HC3 sağlam standart hatalarıyla raporlanmıştır.

**H4 – Anne depresyonu ve ebeveynlik.** Anne depresif belirti düzeyi ile ebeveynlik tutumu boyutları latent değişken düzeyinde modellenmiştir. Anketlerin her maddesi gözlenen bir ölçümdür; oysa ilgilenilen "depresyon" ya da "reddetme" yapıları doğrudan gözlenemez. Birincil model bu gözlenen maddelerden latent yapıları kestiren ve aralarındaki yolları eşzamanlı sınayan yapısal eşitlik modelidir; sıralı (ordinal) Likert maddeleri için normallik varsaymadan polikorik korelasyon temelinde çalışan WLSMV kestirim yöntemi kullanılmıştır. Depresyon latent faktöründen ebeveynlik alt ölçeklerine giden yollar anne yaşı ve sosyoekonomik durum ayarlı raporlanmıştır. Yolların gruplar arası karşılaştırılabilirliğini desteklemek için ölçüm eşdeğerliği taraması yapılandırmasal ve metrik düzeyde çalıştırılmıştır; yük (metrik) eşdeğerliği, latent yapılar arası yol/regresyon ilişkilerinin gruplar arası karşılaştırılabilmesi için gereken düzeyi sağladığından tarama bu düzeyde konumlandırılmıştır. Grup-spesifik boş sıralı kategoriler yalnız bu duyarlılık çerçevesinde açık eşleme ile birleştirilmiştir [@putnickBornstein2016measurementInvariance; @li2016ordinalCFA].

**H5 – Diadik tutarlılık.** Anne ile çocuk algısı arasındaki tutarlılık, tezin birincil özgün katkısını oluşturur; tek bir uyum ölçütü kırılgan olacağından beş paralel stratejiyle çözümlenmiş ve en az üç stratejinin yön düzeyinde uyuşması önceden "güçlü bulgu" ölçütü olarak belirlenmiştir. İlk strateji, üç diyad türü (anne ↔ indeks çocuk, anne ↔ kardeş, indeks ↔ kardeş) ve dört EMBU alt ölçeği için mutlak uyumu — anne ile çocuğun aynı puanı verip vermediğini — sınıf-içi korelasyon ve Bland-Altman uyum sınırlarıyla [@blandAltman1986] grup bazında raporlamıştır. Sınıf-içi korelasyon, iki yönlü rastgele etkiler modeliyle, mutlak uyum (*absolute agreement*) tanımı ve tek ölçüm birimi üzerinden hesaplanmıştır; bu, Shrout-Fleiss gösteriminde ICC(2,1), McGraw-Wong gösteriminde ICC(A,1)'e karşılık gelir [@koo2016iccGuideline]. İkinci strateji, ham fark skorunun gizleyebildiği uyum/uyumsuzluk yüzeyini çözen yüzey tepki çözümlemesiyle (*response surface analysis*) [@edwardsParry1993rsa] anne–çocuk algı yüzeyini anne depresif belirti düzeyine bağlamıştır. Üçüncü strateji, anne ve çocuk yanıtlarını birlikte yönlendiren paylaşılan bir aile içi latenti ortak yazgı modeli (*common fate model*) olarak kurmuştur. Dördüncü strateji, diadik doğrulayıcı faktör analiziyle anne ve çocuk latentleri arasındaki, ölçüm hatasının ayrı bir bileşen olarak modellenmeye çalışıldığı, modele bağlı latent konkordansı raporlamıştır. Beşinci strateji, aktör ve partner etkilerinin oranını dirençli önyükleme (*bootstrap*) güven aralığıyla vermiştir. Bu tutarlılık örüntülerinin "ne kadar/hangi boyutta" yanıtı nicel kolda kalırken, "neden/nasıl" boyutu nitel kol ve karma yorumla ele alınmıştır.""" :
    """### Beş Temel Hipotezin İstatistiksel Testleri

Araştırmanın beş temel sorusu (hipotezi), ailenin kimin penceresinden incelendiğine göre farklı düzeylerde (örneğin çocuğu doğrudan ilgilendirenler ayrı, aileyi bir bütün olarak ilgilendirenler ayrı) ele alınmıştır. Testlerde çocukların aynı evde yaşadığı (aile içi bağlılık) her zaman denkleme katılmış ve bir ebeveynin davranışı hem kendisini hem de karşı tarafı nasıl etkiliyor diye (aktör-partner modelleri) bakılmıştır. Aşağıdaki @tbl-analiz-plani bu teknik kararların özetini sunar:

| Hipotez | Neyi Ölçüyor? | Ana Test Yöntemi | Temizlenen Dış Etkenler |
|---|---|---|---|
| **H1** | Çocuğun hissettiği ebeveynlik | Aynı eve ait olma hesabını katan çok düzeyli model | Yaş, cinsiyet, gelir/eğitim (SES), kardeşler arası yaş farkı, çocuk sayısı |
| **H2** | Kardeş ilişkileri | Grup farkı testleri (Welch t) ve çiftler arası modeller | Kardeş yaş farkı, cinsiyet benzerliği |
| **H3** | Annenin hissettiği ebeveynlik | Eğilim skoru ve kovaryans analizleri | Aile grubu, anne yaşı, SES, yaş farkı, çocuk sayısı |
| **H4** | Annenin depresyonu ↔ ebeveynliği | Gelişmiş yapısal eşitlik modelleri (WLSMV SEM) | Anne yaşı, SES |
| **H5** | Anne ve çocuğun aynı eylemi farklı anlaması (Uyum) | Beş farklı bakış açısı stratejisi (ICC, ortak yazgı, diadik modeller) | Anket türü, ilişki boyutu |

: Beş temel soru için uygulanan ana istatistiksel plan. {#tbl-analiz-plani}

**H1 – Çocuğun hisleri:** Her aileden iki çocuk (indeks ve kardeş) anket doldurduğu için bu iki çocuğun verisi istatistikte birbirinden "tamamen bağımsız iki kişi" gibi kabul edilemez. Birbirlerini veya aynı evi paylaştıkları için, bu durumu hesaba katan özel bir hesap (çok düzeyli model) kullanılmıştır [@hox2017multilevel]. Aksi hâlde istatistikler yalan söyleyerek aslında olmayan farkları varmış gibi gösterebilirdi.

**H2 – Kardeş ilişkisi:** İki kardeşin aralarındaki bağ, sadece sıradan grup testleriyle değil; "bu kardeş diğerini nasıl etkiliyor" ve "kendisi nasıl etkileniyor" mantığını (aktör-partner) çözen gelişmiş aile testleriyle değerlendirilmiştir [@kennyKashyCook2006; @olsenKenny2006interchangeableDyads].

**H3 – Annenin kendi ebeveynliğini nasıl anlattığı:** Annenin kendi hakkındaki düşünceleri; yaş, gelir durumu ve evdeki çocuk sayısı gibi etkenlerden arındırılarak sadece diyabet üzerinden karşılaştırılmıştır. Annenin antidepresan kullanması zaten depresyonun veya ebeveynlik hissinin bir parçası olabileceği için, dışarıdan etki eden bir faktör olarak ana testin içine karıştırılmamış, ayrıca incelenmiştir.

**H4 – Depresyon ve ebeveynlik:** Anketteki her soru aslında sadece kâğıt üzerinde bir işarettir, asıl merak ettiğimiz "depresyon" ruh hâlinin kendisidir. Bu sebeple "bu kâğıttaki puanların arkasında yatan asıl hissi" (gizil-latent yapı) bulup çıkaran ve gruplar arasında bu hissin benzer şekilde okunup okunmadığını (ölçüm eşdeğerliği) doğrulayan modeller kullanılmıştır [@putnickBornstein2016measurementInvariance; @li2016ordinalCFA].

**H5 – Aynı evde birbirini anlamama durumu (Uyum):** Anne "çocuğumu çok seviyorum" derken çocuğun "annem beni anlamıyor" demesi gibi kopukluklar, tezin en önemli katkısıdır. Bu durumu sadece bir hesaplamaya bırakmamak için; aradaki basit puan farkından tutun da puanların arkasındaki gizli duyguların uyuşmazlığına kadar tam 5 farklı matematiksel strateji ile bakılmıştır [@blandAltman1986; @koo2016iccGuideline; @edwardsParry1993rsa]. İstatistikler bu uyumsuzluğun "ne kadar" olduğunu bulurken, işin "neden" kısmı nitel (yüz yüze) görüşmelerdeki sözlere bırakılmıştır."""
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success!")
    else:
        print("Failed to find:\n" + old[:100] + "...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
