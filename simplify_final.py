import sys

file_path = "chapters/05_tartisma_ve_sonuc.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    """Çalışmanın güçlü yönleri, yorumun güvenini destekleyen tasarım özellikleridir.
Karma yöntem tasarımı, nicel örüntülerin deneyimsel bağlamını doğrudan
erişilemeyecek biçimde görünür kılmıştır. Triadik çok-bilgi-verici yapı, aile içi
ayrışmayı tek bir bilgi-verici perspektifine indirgemeden haritalamıştır. Aile
düzeyinde nesteli veri yapısının çok düzeyli modellemeyle ele alınması
[@hox2017multilevel], aile içi bağımlılıktan kaynaklanabilecek standart hata
yanlılığını önlemiştir. Sensitivite üçlüsü ile Bayesçi çift raporlama, küçük etki
büyüklüğü ve sınır-altı psikometrik koşullar altında null bulguları daha temkinli ve
şeffaf yorumlamayı mümkün kılmıştır (eşdeğerlik H3'te dört alt ölçeğin yalnız ikisinde
biçimsel olarak gösterilmiş, ikisinde belirsiz kalmıştır). Açık bilim çıktıları —
ön-kayıt, paket kilidi, hash zinciri ve kanonik veri kilidi — çalışmanın hesaplama
düzeyindeki izlenebilirliğini ve tekrarlanabilirliğini desteklemiştir.""" :
    """**Araştırmamızın Güçlü Yönleri:**
Çalışmamız, bulguların güvenilirliğini artıran güçlü istatistiksel araçlarla (karma yöntemler, aileleri bütün olarak ele alan modeller, Bayes istatistiği) donatılmıştır. Anne, diyabetli çocuk ve kardeşin "üçlü" olarak değerlendirilmesi, aile içindeki kopuklukları daha net göstermiştir. Tüm analiz süreçlerimiz "Açık Bilim" kuralları gereği adım adım şeffaftır.""",

    """Çalışmanın sınırlılıkları yorumu çerçevelemektedir. Tasarım kesitsel ve ilişkiseldir;
hiçbir bulgudan nedensel sonuç çıkarılamaz. Örneklem büyüklüğü bazı çok düzeyli ve
diadik analizler için sınırda kalmıştır. Nicel kol 241 aileye, niteliksel kol yedi
aileye dayanmaktadır ve bu iki kol karıştırılmamalıdır: niteliksel kol aktarılabilirlik
sunar, istatistiksel genellenebilirlik değil. Niteliksel bulgular, katılımcının kendi
sözlerine sadık kimliksizleştirilmiş doğrudan alıntılarla desteklenmekle birlikte,
mahremiyet gereği ham görüşme dökümünün bütünü paylaşılmadığından tema ile tüm ham veri
arasındaki bağ okuyucu tarafından uçtan uca denetlenememektedir. Bu nedenle niteliksel
temalar tek başına nedensel kanıt değil, seçilmiş alıntılarla desteklenen tamamlayıcı bir
kanıt katmanı olarak konumlanır.

Ölçüm ağırlıkla öz-bildirime dayandığından
sosyal istenirlik ve bilgi-verici yanlılığı yorumu sınırlar; EMBU-P reddetme alt
ölçeğinin düşük iç tutarlılığı ilgili bulguların gücünü azaltmıştır. HbA1c veri
tamamlanma oranının düşüklüğü Tip 1 diyabet klinik alt-analizlerini güç-sınırlı kılmış
ve bu bulgular imputasyona alınmamıştır.

Çalışma iki merkezden katılımcı almış olmakla
birlikte kontrol grubu yalnız birincil merkezden, ikinci merkez ise yalnız T1DM
grubundan katılımcı sağlamıştır. Bu nedenle merkez, tanı grubu ve takvim zamanı bu
örneklemde kısmen örtüşmüş ve grup etkisinin merkez/dönem etkisinden tam
ayrıştırılmasını engellemiştir. Merkez bilgisi kanonik analiz veri setinde ayrı bir
değişken olarak kodlanmadığından, merkeze göre katmanlı bir duyarlılık analizi bu
veriyle mümkün olmamıştır; bu, bulgunun grup ile takvim zamanının ayrıştığı çok-merkezli
bir örneklemde yinelenmesini gerektiren bir sınırlılıktır. Çalışma ayrıca tek-kültürel
bağlamda yürütülmüştür. Keşifsel katmanlarda paragraf-içi yanlış-keşif düzeltmesi
uygulanmış olmakla birlikte, tüm keşifsel batarya boyunca biriken çalışma-geneli çokluk
yükü biçimsel olarak denetlenmemiştir. Ayrıca negatif kontrol çözümlemesinde aile
numarasının EMBU-P sıcaklık ile beklenmedik ilişkisi (β = 0,098; p = 0,003), aile
numarasının kayıt sırasına bağlı bir dönem/kohort vekili olabileceğini ve yukarıda
anılan dönem/merkez örtüşmesini pekiştirdiğini düşündürmektedir.

Örneklemin oluşturulma ölçütleri ayrıca bir sosyal ve ailesel seçilim sınırı
taşımaktadır. Dâhil edilme koşulları — aynı yaş aralığında en az bir sağlıklı biyolojik
kardeşin bulunması, her iki ebeveynin hayatta ve evli olması ve anneden veri alınabilmesi —
gereği örneklem yapısal olarak iki çocuklu, iki ebeveynli (ağırlıklı olarak çekirdek) ve
anneden veri sağlanabilen aileleri temsil eder. Bu nedenle tek çocuklu aileler, kardeşi
bu yaş aralığı dışında kalan aileler, tek ebeveynli, ebeveyn kaybı yaşamış ya da
ebeveynleri boşanmış aileler
ve daha yüksek tıbbi/sosyal karmaşıklık taşıyan aile yapıları örneklem dışında
kalmıştır. Sosyal pediatri perspektifinden bu durum yalnız istatistiksel bir
genellenebilirlik kısıtı değildir; aile kırılganlığının belirli biçimlerinin bulgular
kapsamına girmemesi anlamına da gelir. Dolayısıyla aktarılabilirlik bu aile yapılarına
genişletilmemelidir.

Kritik bir seçilim sınırlılığı, veri toplama dönemi ile grup üyeliğinin bu örneklemde
neredeyse tam örtüşmesidir (toplama yılı × grup Cramér V = 0,59). İki grubun en geniş
ortak takvim desteğine sahip olduğu 2023 alt-örnekleminde H1 çocuk-reddetme farkı
belirgin biçimde zayıflamaktadır (d = 0,38'den yaklaşık sıfıra). HbA1c erişilebilirliği
ise gözlenen özelliklere göre seçici bulunmaktadır (OR = 4,56; p < 0,001; MNAR
olasılığıyla uyumlu, ancak mekanizmayı tek başına tanımlamayan bir örüntü)
(Bulgular, §4.4.6). Her
iki grup üç yılın tümünde temsil edilmekle birlikte ortak destek belirgin biçimde
dengesizdir (@tbl-yil-grup); 2023 iki grubun bulunduğu tek yıl değil, en geniş ortak
temsile sahip dönemdir. Bu nedenle "iki grubun ortak temsil edildiği dönem" ölçütü,
mutlak varlık değil yeterli ortak destek (pozitiflik) temelinde tanımlanmalıdır.

| Yıl | DM | Kontrol | Toplam |
|---|---|---|---|
| 2023 | 108 | 40 | 148 |
| 2024 | 6 | 36 | 42 |
| 2025 | 6 | 45 | 51 |

: Veri toplama yılı × grup dağılımı. Her iki grup üç yılda da bulunur; ortak destek 2023'te en geniştir. {#tbl-yil-grup}

Bu yapı, karıştırıcılıktan ayrı bir seçilim yanlılığı mekanizması olarak
değerlendirilmelidir. Her iki grubun ortak temsil edildiği dönem dışındaki katılımcılar
üzerinde koşullanma, ortak-etki üzerinden yanlılık üretebilir [@hernan2004selectionBias].
Nitekim bir grup farkının örneklem seçilim yapısı dengelendiğinde büyüklüğünü yitirmesi
ya da yön değiştirmesi epidemiyolojik olarak belgelenmiş bir örüntüdür
[@luqueFernandez2016paradox]. Bu örüntü, birincil çocuk-algısı bulgusunun dönemsel
karışmadan bağımsız gücünü sınırlamakta ve bulgunun grup ile dönemin dengeli dağıldığı
bağımsız bir örneklemde yinelenmesini zorunlu kılmaktadır. Ön-kayıt prospektif/reflektif
hibrit olarak kabul edilmiş; doğrulayıcı ve validasyon ayrımı önceden belirlenmiş biçimde
korunmuştur. Replikasyon gücü küçük etkiler için sınırlıdır ve ölçülmemiş karıştırıcıya
duyarlılık zayıf-orta düzeydedir (Bulgular, §4.5); bu nedenle belirsiz veya negatif
bulgular güç sınırlamasıyla birlikte okunmalıdır. Tüm sapma kararları şeffaf biçimde
raporlanmıştır.""" :
    """**Araştırmamızın Zayıf Yönleri (Sınırlılıklar):**
Bulgularımız dikkatle okunmalıdır çünkü:
- **Sebep-Sonuç İlişkisi Yoktur:** Çalışmamız olaylara tek bir zaman diliminde (fotoğraf çeker gibi) bakmıştır. Bu yüzden "diyabet olduğu için reddedilme hissi doğdu" gibi kesin bir sebep-sonuç çıkarılamaz.
- **Anketlerin Yanıltıcılığı:** Anneler "iyi görünmek" amacıyla, hissettiklerini tam yansıtmamış olabilir. Ayrıca verilerimizde (örneğin reddetme ölçeğinde) anket sorularının güvenilirliği sınırda kalmıştır. Kan şekeri (HbA1c) bilgilerine çok az çocukta ulaşılabilmiştir.
- **Toplama Zamanı ve Hastane Etkisi:** Sağlıklı çocukları tek bir hastaneden, diyabetli çocukları ise daha çok başka bir hastaneden (ve çoğunlukla farklı yıllarda) topladık. İki grubun aynı takvim yılında birleştiği 2023 senesinde farkın azaldığını gördük (bkz. @tbl-yil-grup). Bu durum, bulduğumuz bazı farkların hastalıktan değil, hastaneden veya o dönemin şartlarından kaynaklanmış olabileceğini gösterir [@hernan2004selectionBias; @luqueFernandez2016paradox].
- **Örneklemin "İdeal Aile" Olması:** Araştırmaya dâhil olmak için ailelerin boşanmamış olması ve en az iki çocuğu olması gerekiyordu. Bu nedenle çalışmamız; tek ebeveynli, ebeveynini kaybetmiş veya boşanmış ailelerin yaşadığı çok daha ağır zorlukları kapsamamaktadır.

| Yıl | DM | Kontrol | Toplam |
|---|---|---|---|
| 2023 | 108 | 40 | 148 |
| 2024 | 6 | 36 | 42 |
| 2025 | 6 | 45 | 51 |

: Veri toplama yılı × grup dağılımı. Her iki grup üç yılda da bulunur; ortak destek 2023'te en geniştir. {#tbl-yil-grup}""",

    """Bu doktora tezi, Tip 1 diyabetli çocuklar, sağlıklı kardeşleri ve anneleri ile sağlıklı
kontrol grubu arasındaki ebeveynlik tutumu algı örüntüsünü çoklu kaynaklı, aile düzeyinde
nesteli ve karma bir tasarımda incelemiştir. Varılan temel sonuç şudur: bu örneklemde
gözlenen rol-temelli algı örüntüsü Tip 1 diyabet ile ilişkili görünmekte, ebeveynlik
tutumları gözlem düzlemine göre değişen bir örüntü göstermekte ve reddetme sinyali anne
öz-bildiriminde değil çocuk algısında belirmektedir. Ancak bu farkın dönem/merkez
örtüşmesinden bağımsız, T1DM'ye özgü bir grup etkisi olduğu gösterilememiştir. Bu
tablonun teorik katkısı, aile içi ayrışmanın bilgi-verici, boyut ve deneyim düzlemlerinde
haritalanabileceğini ve diadik konkordans ölçümünün psikometrik adaptasyon
çalışmalarında değerli bir tamamlayıcı olabileceğini göstermesidir. Klinik katkısı, anne
öz-bildiriminin tek başına bütün perspektifleri temsil etmeyebileceği, uygun klinik
bağlamlarda çocuk algısının ve diadik tutarlılığın da değerlendirmeye eklenebileceği
önerisidir. Metodolojik katkısı ise sensitivite üçlüsü ile Bayesçi çift raporlamanın
taşıdığı değeri göstermesidir: küçük etki büyüklüğü ve sınır-altı psikometrik koşullar
altında null bulguları kanıt türü ve derecesine göre ayrımlı, temkinli ve şeffaf
yorumlamayı mümkün kılar (ör. H3'te eşdeğerlik dört alt ölçeğin yalnız ikisinde biçimsel
olarak gösterilmiş, ikisinde belirsiz kalmış; H2'de biçimsel eşdeğerlik kurulamamıştır).
Böylece çalışmanın amacı — bu üç aile rolünün ebeveynlik tutumunu nasıl algıladığını çok
kaynaklı ve karma bir çerçevede anlamlandırmak — büyük ölçüde gerçekleştirilmiştir.

Bulgulardan doğrudan türeyen öneriler üç başlıkta toplanmaktadır. Klinik ve aile
düzeyinde: Tip 1 diyabetli çocuk ailelerinde anne öz-raporu tek başına klinik karar
kaynağı olarak alınmamalı; uygun olduğunda çocuğun perspektifi yapılandırılmış biçimde
değerlendirilerek tabloya eklenmelidir. Anne depresif belirti düzeyi ile anne-bildirimli
ebeveynlik tutumları arasında sınırlı global uyuma sahip modelde gözlenen model-koşullu
ilişki göz önüne alınarak, anne ruhsal iyilik hâlinin izlenmesi ve gerektiğinde
psikososyal desteğe yönlendirme diyabet bakım hizmetine entegre edilmelidir. Bu, çocuk
ve gençlerin diyabet bakımında psikososyal değerlendirmeyi standart öneren uluslararası
klinik kılavuzlarla [@deWit2022ispadPsychological] uyumludur. Anne ↔ çocuk algı
tutarsızlığı örüntüleri klinik psikoeğitim hedefidir. Kardeş ilişkisi boyutlarında
gruplar arası fark için kanıt yetersiz kalmış olsa da, bu fark yokluğu sağlıklı kardeşin
etkilenmediği anlamına gelmez; görünmeyen yüke yönelik kardeş-spesifik değerlendirme
fırsatları mevcuttur. Bu öneriler, aile-odaklı ekip temelli diyabet bakım modelinin
[@laffel2003teamwork] güçlendirilmesiyle uyumludur.

Araştırma düzeyinde öneriler dört başlıkta toplanmaktadır.

**Replikasyon ve
genelleştirme** açısından, Anadolu ve Doğu Anadolu Tip 1 diyabet merkezlerini kapsayan
çok-merkezli bir replikasyon sosyokültürel genelleştirilebilirlik için önceliklidir.
Ayrıca Türk Tip 1 diyabet örnekleminde EMBU çocuk formu ve diadik konkordans ölçümleri
ileri psikometrik adaptasyon çalışmasıyla güçlendirilmelidir. Bu adaptasyon, mevcut
kesitsel tasarımda elde edilemeyen test-tekrar test (zamansal kararlılık) güvenirliğini
iki-üç haftalık bir ara ile raporlamalı ve özellikle iç tutarlılığı zayıf çıkan ebeveyn
reddetme alt ölçeği için madde havuzunun kültürel-klinik uygunluğunu gözden geçirmelidir.

**Boylamsal yapı** açısından, anne depresyonu → ebeveynlik tutumu → çocuk algısı
zincirinin zamansal yönü en az iki, tercihen üç dalgalı bir izlem kohortunda
sınanmalıdır. Burada klasik çapraz gecikmeli panel modeli yalnız karşılaştırmalı
duyarlılık modeli olarak kullanılmalı; ana yön testi, ailelere özgü sabit farklılıkları
ayırabilen rassal-aralık çapraz gecikmeli panel modeli (RI-CLPM) ile yapılmalıdır
[@hamaker2015clpm]. Çünkü klasik model bu farklılıkları ayıramadığında yanıltıcı yön
çıkarımı üretebilir.

**Metodolojik genişletme** açısından üç öncelik öne çıkmaktadır.
Geliştirilen klinik
fayda modeli, bağımsız bir kohortta TRIPOD raporlama standardı ve yerleşik dış validasyon
çerçevesi (ayrım ve kalibrasyonun birlikte değerlendirilmesi) uyarınca dış validasyondan
geçirilmelidir [@collins2015tripod; @steyerbergVergouwe2014]. Mevcut anne-odaklı tasarım,
baba paralel kohortuyla genişletilerek baba-çocuk ve anne-baba düadik tutarlılığı da
Olsen-Kenny çerçevesinde test edilmelidir. Son olarak, keşifsel nitelikteki HbA1c
(n = 39) örneklemi, beklenen etki büyüklüğü, model karmaşıklığı, merkez kümelenmesi ve
HbA1c eksikliği dikkate alınarak a priori güç analizi veya simülasyonla belirlenen
yeterli büyüklükte bağımsız bir DM kohortunda hem ortalama hem varyans düzeyinde
doğrulanmalıdır.

**Müdahale** düzeyinde ise aile-temelli/anne-distresi odaklı psikososyal
müdahalelerin — özellikle yüksek depresif belirti veya diyabet-distresi taşıyan
ailelerde — yeterli güçte çok-merkezli randomize kontrollü tasarımlarla sınanması
gerekir. Bu tasarımların protokolü SPIRIT 2025'e göre hazırlanmalı, katılımcı alımından
önce kamuya açık bir klinik araştırma kayıt sisteminde prospektif olarak kaydedilmeli ve
sonuçları CONSORT 2025'e göre raporlanmalıdır [@chan2025spirit; @hopewell2025consort]. Bu
tasarımlarda birincil çıktı bakım veren distresi ve aile çatışması, metabolik çıktı ise
HbA1c olarak önceden tanımlanmalı; HbA1c'de küçük/kısa vadeli etki olasılığı ve seçilim
riski hesaba katılmalıdır [@jansen2025parenting; @wakelin2025familyInterventions].

Sosyal
istenirlik kompansasyonunun derinlemesine incelenmesi ise ayrı bir niteliksel/karma
yöntem araştırma projesi olarak yürütülmelidir; bu son çalışma mevcut tezin kapsamı
dışındadır ve ayrı bir araştırma hattı olarak planlanmaktadır.""" :
    """**Sonuç ve Genel Öneriler**

Bu tezin ulaştığı en çarpıcı gerçek şudur: Aynı kronik hastalığı ve aynı evi paylaşsalar bile; anne, sağlıklı kardeş ve diyabetli çocuk ebeveynliği bambaşka şekillerde tecrübe etmektedir. Ebeveynliğe dair potansiyel sorunlar (örneğin reddedilme hissi), annenin anketlerindeki yanıtlarında değil, doğrudan çocuğun algısında gün yüzüne çıkmaktadır. Ancak elimizdeki veriler bu farklılığın "sadece ve kesinlikle diyabetten" kaynaklandığını kanıtlamak için yetersiz kalmıştır.

Bu sonuçların ışığında klinik pratikte ve gelecekteki araştırmalarda şunları öneriyoruz:

1. **Klinik Öneriler:** Poliklinik muayenelerinde çocukların psikolojik durumu sadece "annelere sorularak" değerlendirilmemeli; doğrudan çocuğun dünyası da dinlenmelidir. Ayrıca annedeki depresif eğilimlerin diyabet yönetimine zararlı etkileri göz önüne alınarak, hastanelerde annelere yönelik standart psikososyal destek birimleri kurulmalıdır [@deWit2022ispadPsychological; @laffel2003teamwork].
2. **Gelecek Araştırmalar İçin Öneriler:**
   - **Genişletme:** Çalışma tek bir merkeze sıkışmaktan kurtarılıp Anadolu'daki daha geniş kitlelerle ve "babaları" da dâhil ederek tekrarlanmalıdır.
   - **Zamanı İzleme (Boylamsal):** Bu tezdeki gibi "tek seferlik" değil, aileyi teşhis anından itibaren en az üç dalga hâlinde yıllarca izleyen araştırmalar yapılmalıdır [@hamaker2015clpm].
   - **Müdahale Testleri:** Sıkıntı çeken annelere verilecek psikolojik destek eğitimlerinin, diyabetli çocuğun kan şekerine ve evdeki huzura gerçekten fayda sağlayıp sağlamadığını net olarak ölçen büyük klinik deneyler (randomize kontrollü tasarımlar) planlanmalıdır [@chan2025spirit; @hopewell2025consort; @wakelin2025familyInterventions].

Bu tezin asıl başarıya ulaştığı yer, bir ailenin diyabet karşısında nasıl aynı anda hem omuz omuza verip hem de üç farklı yalnızlık yaşayabileceğini bilimsel ve insani bir dengede ortaya koyması olmuştur."""
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success!")
    else:
        print("Failed to find:\n" + old[:100] + "...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
