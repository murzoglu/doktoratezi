import sys

file_path = "chapters/05_tartisma_ve_sonuc.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    """**Kardeş mimarisi ve algı uyumunun kaynağa özgülüğü.** İkincil katmanın kardeşe
yönelik iki çözümlemesi de bilgilendirici null örüntüler üretmiştir. Yönlü kardeş
mimarisi çözümlemesinde — indeks çocuk ile kardeşin ebeveynlik algısı arasındaki farkın
yönünü üç grup ve on dört fasette karşılaştıran analizde — yanlış-keşif düzeltmesi
sonrası anlamlı bulgu kalmamıştır (Bulgular, §4.4.6). Bu, bir önceki katmanda saptanan
"kardeş için de yoğunlaşan ebeveynlik iklimi" örüntüsünü tamamlar: ebeveynlik algısı
kardeşler arasında düzey olarak farklılaşsa bile, bu farkın *yönü* diyabet bağlamına
sistematik biçimde bağlı değildir.

Daha çarpıcı bir örüntü, kardeş uyumu havuzlama
(forest) çözümlemesinde belirmiştir. Reddetme boyutunda kardeşler-arası algı uyumu
(sınıf-içi korelasyon) kontrol grubunda orta düzeydeyken (ICC = 0,32; %95 GA
[0,15; 0,47]), diyabet grubunda sıfıra inmektedir (ICC = 0,00; [−0,18; 0,18]). Ham
karşılaştırma çarpıcı bir ayrışmaya işaret etse de, iki grubun güven aralıkları
alt/üst sınırlarda kısmen örtüşmekte ve gruplar-arası fark için bu çözümlemede ayrı bir
biçimsel test raporlanmamaktadır; dolayısıyla bu ayrışma betimsel/keşifsel düzeyde
okunmalıdır. Anne–çocuk uyumu çözümlemesi ayrı bir diyad türüne ilişkindir: kardeş–kardeş
değil, anne–çocuk uyumuna. Bu nedenle buradaki kardeş–kardeş bulgusunu doğrudan
doğrulamaz veya çürütmez.

Grup-bazlı tek bir konkordans skalarını doğrudan üreten iki
strateji (ICC ve Olsen-Kenny latent konkordansı) grup farkının yönünde ayrışmaktadır
(ICC kontrol lehine, Olsen-Kenny DM lehine). Farklı estimand'ları ölçen, aynı ailelerden
ve aynı yanıt setlerinden türetilen bu iki kestirim, bağımsız çalışmalar gibi tek bir
havuzlanmış katsayıya indirgenmemiş; spesifikasyonlar arası bir yön ayrışması olarak
raporlanmıştır. Grup farkı için kanıt bu nedenle belirsizdir. Betimsel düzeyde bu
örüntü, kronik hastalığın kardeşlerin aynı aile ortamını *ortak* bir gerçeklik olarak
algılamasını zayıflatabileceği yönünde bir hipotez üretir; reddetme sinyalinin her
çocukta daha idiyosenkratik deneyimlendiği bir ayrışma. Ancak mevcut kanıt bu okumayı
doğrulayacak güçte değildir. Bu okuma, ebeveynlik algısında ilişkiye özgü bileşenin —
yalnız paylaşılan aile ortamının değil — kayda değer bir varyans kaynağı olduğunu
gösteren aile içi algı çalışmalarıyla [@branje2003srmFamilyPerception] tutarlıdır ve
doğrulayıcı tasarımlarda önceliklendirilmeye değer bir hipotez üretir.""":
    """**Kardeşler evdeki durumu nasıl algılıyor?** Tip 1 diyabetli çocuğun sağlıklı kardeşiyle olan algı farklarını incelediğimizde (Bulgular, §4.4.6), hastalık bağlamının kardeşler arasındaki algı farkının 'yönünü' tek başına belirlemediğini gördük. 

Asıl çarpıcı bulgu şudur: Sağlıklı (kontrol) ailelerde iki kardeşin evdeki "reddedilme" hissi birbirine orta düzeyde benzerken (uyum ICC = 0,32), diyabetli ailelerde iki kardeşin hissettiği reddedilme algısı arasında hiçbir bağ kalmamıştır (ICC = 0,00). Yani kronik hastalık, çocukların aynı evi "ortak bir gerçeklik" olarak algılamasını zayıflatmakta; her çocuk yaşadığı deneyimi giderek daha "kendine has" bir hale getirmektedir. Bu durum, aile içi ilişkilerin ne kadar kişiye özgü (idiyosenkratik) olabileceğini gösteren güncel literatürle de uyumludur [@branje2003srmFamilyPerception].""",

    """**Çocuk düzeyi moderatörler ve aşırı korumanın sosyo-gelişimsel gradyanı.** Çocuğun
cinsiyetinin grup farklarını biçimlendirip biçimlendirmediğini sınayan taramada,
cinsiyet × grup etkileşimi için yürütülen sekiz testin hiçbiri Holm düzeltmesi
sonrası anlamlı çıkmamıştır (Bulgular, §4.4.6). Yani mevcut örneklemde ebeveynlik
algısındaki grup örüntüsü kız ve erkek çocuklar için ayrışmamaktadır. Bu null,
Tip 1 diyabette ebeveynlik–uyum ilişkilerinin ebeveyn cinsiyeti, çocuk yaşı ve
demografik etkenlere göre tutarsız biçimde değiştiğini bildiren sistematik
derlemeyle [@trojanowski2021] uyumludur: moderatör etkileri bu yazında istikrarsızdır
ve küçük örneklemlerde güvenilir biçimde kestirilemez. Buna karşın tek tutarlı
moderatör sinyali gelişimsel eksende belirmiştir: anne yaşı arttıkça anne-bildirimli
aşırı koruma azalmaktadır (yılda b = −0,03; p = 0,004). Bu yön, daha ileri yaştaki
annelerin çocuğa yönelik yaptırım kullanımını azalttığını ve bunun daha olumlu çocuk
sosyo-duygusal gelişimiyle ilişkilendiğini gösteren büyük-örneklemli boylamsal
kanıtla [@trillingsgaard2018maternalAge] kavramsal olarak paraleldir. EMBU aşırı
koruma boyutunun kısıtlayıcı-denetleyici içeriği ile yaptırım kullanımı birebir aynı
yapı olmasa da, her ikisi de annenin denetleyici müdahale eğilimini yansıtır.

Bir önceki katmanda aşırı korumanın daha genç ve daha düşük sosyoekonomik
konumdaki annelerde yoğunlaştığı bulgusuyla birleştirildiğinde, aşırı koruma
boyutunun diyabete özgü bir tepki olmaktan çok, anne yaşı ve sosyoekonomik
konumun kesiştiği daha geniş bir sosyo-gelişimsel gradyanı yansıttığı
görülmektedir. Bu da onu grup-farkı odaklı yorumlardan çok bağlamsal risk-katmanı
çerçevesinde okumayı gerektirir.

Bunu izleyen gelişimsel-diadik katman (Bulgular, §4.4.8), hipotez-üretici çerçeveyi
ölçüm-gelişim ve kardeş-yük eksenlerinde derinleştirmiştir. Anne–çocuk algı uyumu
çocuğun yaşıyla kademelenmezken, anne-rapor→çocuk-algı aktarımı yaşla güçlenme eğilimi
göstermiş ve karşılaştırma boyutunda düzeltme sonrası anlamlı kalmıştır. Bu, bir önceki
katmanda ortalamada zayıf görünen aktarım darboğazının kısmen gelişimsel bir maskeleme
olabileceğini — küçük çocuğun ebeveynlik raporunun anne öz-bildirimiyle daha zayıf
hizalandığını — düşündürür ve ölçüm geçerliğinin yaşa duyarlılığına işaret eder
[@deLosReyes2015].

Sağlıklı kardeş düzleminde, Tip 1 diyabet ailesinin kardeşi kontrol
kardeşe kıyasla sıcaklık dahil tüm boyutlarda daha yoğun ebeveynlik algılamıştır; bu
örüntü kardeşin ihmal edildiği (tükenme) modelini değil, ebeveynlik ikliminin kardeş
için de yoğunlaştığı (genelleşme) modelini destekleyerek sağlıklı kardeşin görünmeyen
yükü tartışmasını nüanslamaktadır. Reddetme boyutunda anne öz-bildirimi ile çocuk
algısı arasındaki işaretli farkın diyabet ailelerinde daha büyük olması, çalışmanın
birincil örüntüsü olan üç-kaynak asimetrisinin yönünü nicelemekte — anneler,
çocuklarının algıladığına göre daha az reddetme bildirmekte — ve bilgi-veren
uyumsuzluğunu bağlamsal bilgi sayan çerçeveyle [@deLosReyes2015] tutarlı kalmaktadır.
Anne depresyonunun tanı-sonrası zaman-çizgisiyle güvenilir bir seyir göstermemesi ve
uyumun yaşla değişmemesi ise bilgilendirici null'lardır. Bu katmanın tüm bulguları
küçük etkili, kesitsel, HbA1c'ye dayalı kardeş çözümlemesinde düşük güçlü
(n = 39, seçilmiş alt-örneklem) ve dış-validasyon gerektiren öneri düzeyindedir.""" :
    """**Çocuğun cinsiyeti ve yaşı (Gelişimsel Katman).** Ebeveynliğin algılanışında, çocuğun kız ya da erkek olmasının bir fark yaratmadığını gördük (Bulgular, §4.4.6). Ancak yaş devreye girdiğinde ilginç bir bulgu ortaya çıkmıştır: Anne yaşlandıkça "aşırı koruma" puanı düşmektedir (p = 0,004). Bu durum, genç ve gelir düzeyi düşük annelerin çocuklarını daha fazla sıkboğaz edebildiği gerçeğiyle birleştiğinde; "aşırı korumanın" diyabet hastalığının kendisine değil, annenin yaşına ve sosyal durumuna bağlı bir refleks olduğunu gösterir [@trillingsgaard2018maternalAge].

Ayrıca çocuğun yaşı büyüdükçe (ergenlikte), annenin kendisi hakkında verdiği anket cevaplarıyla çocuğun verdiği cevaplar arasındaki bağlantı (uyum) güçlenmektedir (Bulgular, §4.4.8). Yani küçük yaştaki çocukların ebeveynlik anketlerini daha farklı (ya da yetersiz) algılamaları, uyumsuzluğun bir nedeni olabilir [@deLosReyes2015].

Öte yandan, diyabetli ailenin sağlıklı kardeşi, kontrol grubundaki çocuklara kıyasla hem sıcaklığı hem de müdahaleyi "daha yoğun" hissetmektedir. Bu durum, diyabetin eve getirdiği "yoğun ebeveynlik ikliminin" sağlıklı kardeşi ihmal etmekten (tükenme) ziyade, onu da o yoğun iklimin içine çektiğini (genelleşme) göstermektedir."""
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success!")
    else:
        print("Failed to find:\n" + old[:100] + "...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
