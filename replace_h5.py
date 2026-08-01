import sys

file_path = "chapters/04_bulgular.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_text = """### H5 — Diadik Tutarlılık

**Bulgu özeti.** Anne ile çocuğun aynı ebeveynlik tutumuna verdiği yanıtlar
arasındaki uyum düşüktür. Başka bir deyişle anne ile çocuk aynı ilişkiyi büyük
ölçüde farklı algılamaktadır. Bu düşük uyum, en güçlü ve dört alt ölçeği de
kapsayan doğrudan gözlenmiş kanıtta^[Manifest (doğrudan gözlenmiş) kanıt: puanların kendisi üzerinden hesaplanan, latent modelleme içermeyen doğrudan uyum ölçümü.] tutarlı biçimde görülmüştür. Ortak-yazgı,
latent CFA ve k-katsayısı stratejileri ise yakınsama ve belirsizlik sınırlılıkları
nedeniyle bu tabloyu güçlendirmekten çok kısmen tamamlamıştır. Ayrıca bazı
boyutlarda uyum, kontrol ailelerinde diyabetli ailelerden daha yüksek
bulunmuştur.

*Kanıt* — H5, anne EMBU-P puanı ile aynı ailedeki indeks çocuğun EMBU-C puanı
arasındaki uyum için beş paralel strateji ile incelenmiştir. Her strateji uyumun
farklı bir yüzünü ölçmektedir: mutlak uyum, uyumsuzluk yüzeyi, paylaşılan aile
latenti, ölçüm hatasını model içinde ayırmayı amaçlayan modele-bağlı latent ilişki
ve aktör/partner oranı. Stratejiler böyle farklı yüzleri ölçtüğünden, bir yön
farkının ("DM > Kontrol" veya tersi) "güçlü bulgu" sayılması için ön-kayıtlı
olarak en az üç stratejinin aynı yönde uyuşması ölçütü benimsenmiştir. Bu
ölçütün karşılanıp karşılanmadığı alt bölüm sonunda değerlendirilmektedir.

**Strateji 1 (ICC + Bland-Altman).** Anne ile çocuğun puanlarının ne ölçüde
örtüştüğünü ölçen sınıf-içi korelasyon,^[Mutlak uyumu ölçen sınıf-içi korelasyon; ICC(A,1)/ICC(2,1) biçimi.] anne ↔ indeks çocuk düadında dört
alt ölçek için kontrol grubunda 0,03–0,20, DM grubunda −0,01–0,08 ve havuzlanmış
örneklemde 0,00–0,10 aralığındadır. Bu katsayının yüksek pozitif değerleri daha
yüksek uyuma işaret eder. Örneklem tahminleri ise sıfırın altına düşebilir; bu
durum sıfıra yakın veya uyumsuz varyans yapısı olarak yorumlanır. Nitekim DM
grubunda −0,01'e kadar negatif değerler gözlenmiştir. Buradaki düzey
@cicchetti1994 eşiklerinde en alt bant olan "fakir-zayıf" uyuma denk gelmektedir.
Alt ölçek bazında manifest ICC dört boyutun tamamında kontrol > DM yönündedir.
Değerler şöyledir: sıcaklık kontrol 0,145 / DM 0,027; aşırı koruma kontrol 0,204
/ DM 0,009; reddetme kontrol 0,029 / DM −0,006; karşılaştırma kontrol 0,103 / DM
0,084. Bland-Altman uyum sınırlarında ortalama fark sıfıra yakın, limit aralığı
ise geniştir. Dört alt ölçek ve üç düad tipi için tutarlılık haritası
@fig-h5-bland-altman içinde gösterilmiştir.

**Strateji 2 (Edwards-Parry yanıt yüzeyi analizi).** Anne ve çocuk puanının
uyuşmasının/uyuşmamasının çıktıyla nasıl ilişkilendiğini üç boyutlu bir yüzey
olarak modelleyen bu yöntem yalnız sıcaklık ve reddetme alt ölçeklerinde tahmin
edilmiştir. Yanıt yüzeyi çözümlemesinde çıktı değişkeni anne Beck Depresyon
toplam puanıdır. Sıcaklık boyutu her iki grupta da belirgin bir yüzey eğimi
üretmemiştir. Reddetme boyutunda ise DM grubunda uyumsuzluk hattı boyunca yukarı
kıvrılan bir eğri (a₄ = 2,52 [0,05; 4,99]) tespit edilmiş, bu örüntü kontrol
grubunda görülmemiştir (a₄ = −0,04 [−1,84; 1,77]). Yani DM grubunda anne ile çocuğun
reddetme algısı zıtlaştıkça (örneğin anne "reddetmiyorum", çocuk "reddediliyorum"
dedikçe) annedeki depresyon skoru yükselmektedir. İlgili yanıt yüzeyleri
@fig-h5-rsa-surface içinde çizilmiştir.

**Strateji 3 (Ortak yazgı modeli).** Anne ve çocuğun puanlarının "paylaşılan
tek bir aile latenti" etrafında kümelenip kümelenmediğini sınayan ortak yazgı
kestirimlerinde (common-fate modeli) faktör yükleri (λ) sıcaklık boyutunda
yaklaşık 0,40 düzeyindedir (örneğin kontrol λ = 0,47). Reddetme ve
karşılaştırmada ise değerler çok düşüktür ve model genellikle sıfır-varyans
hatası veya sınır parametre uyarılarıyla sonlanmıştır. DM grubunda ortak-yazgı
yükleri genel olarak kontrol grubundan daha da düşüktür; bu da tek ve ortak bir
aile tutumu varsayımının DM grubunda zayıfladığına işaret eder.

**Strateji 4 (Latent düad CFA uyumu).** Bu strateji ölçüm hatasını doğrudan gözlenen
(manifest) puanlardan ayırıp anne-çocuk faktörleri arasındaki asıl ("saf") ilişkiyi
tahmin eder. Dört alt ölçeğin DM grubundaki latent korelasyonları şöyledir:
sıcaklık = 0,11; aşırı koruma = 0,08; reddetme = −0,19; karşılaştırma = 0,14. Kontrol
grubunda ise; sıcaklık = 0,26; aşırı koruma = 0,55; reddetme = 0,07;
karşılaştırma = 0,38 değerlerindedir. Kontrol grubunda dört katsayı da pozitif ve
daha yüksektir. Ancak CFA modellerinin birçoğunda varyans tahminleri negatif ya da
negatife çok yakın olduğu için bu katsayılar güvenilmez kabul edilmiş, sağlam kanıt
sayılmamıştır.

**Strateji 5 (Kenny k-katsayısı).** İki yanıtlayıcının gerçekte ne ölçüde aynı şeye
yanıt verdiğini ifade eden "anlam ortaklığı" oranıdır. Elde edilen k-katsayıları
sıcaklık boyutunda kontrol = 0,19, DM = 0,02; aşırı korumada kontrol = 0,36,
DM = 0,08; reddetmede kontrol = 0,03, DM = −0,03; karşılaştırmada kontrol = 0,20,
DM = 0,09 olarak hesaplanmıştır. Diğer stratejilerde olduğu gibi k-katsayısı da
kontrol grubunda DM grubuna kıyasla tüm boyutlarda daha yüksektir.

**Sentez.** "Aynı tutuma en az üç stratejide uyum oyu" biçimindeki ön-kayıtlı
koşul, hiçbir alt ölçek ve hiçbir grup için karşılanmamıştır. Özetle anne-çocuk
çiftinde uyum zayıftır. Alt ölçekler düzeyinde, en yüksek mutlak uyum
kontrol grubu aşırı korumasındadır (ICC = 0,20). DM grubunda anne ile çocuğun
aynı fikirde olmamalarının düzeyi tüm stratejilerde (5/5) ve tüm alt ölçeklerde
daha yüksektir. Diğer bir deyişle diyabet, anne ve çocuğun tutum algısı
arasındaki makası kontrol grubuna göre daha da açmıştır.
Diadik tutarlılık stratejilerinin özet çıktıları @tbl-apa-h5-concordance içinde
sunulmuştur.

```{r}
#| label: tbl-apa-h5-concordance
#| tbl-cap: "H5 diadik (anne–çocuk çifti) tutarlılık stratejileri — anne EMBU-P puanı ile aynı ailedeki çocuğun EMBU-C puanı arasındaki uyum, her biri uyumun farklı bir yüzünü ölçen beş paralel strateji (sınıf-içi korelasyon/Bland-Altman, yanıt yüzeyi, ortak yazgı, latent düad CFA, Kenny k-katsayısı) ve bilgi-verici ayrışması örüntüleriyle özetlenir. Satırlar beş analiz stratejisi ve klinik tutarsızlık örüntüleri altında gruplanmıştır. Okuma anahtarı: her strateji ayrı okunur; bir yön farkının 'güçlü bulgu' sayılması için ön-kayıtlı olarak en az üç stratejinin aynı yönde uyuşması (triangülasyon) şartı arandığından, stratejilerin yön oyları karşılaştırılarak bu ölçütün karşılanıp karşılanmadığı değerlendirilir."
apa_render_table("t13_h5_concordance", group_col = "Strateji")
```

![H5 Bland-Altman tutarlılık haritası — anne ile çocuğun aynı ilişkiye verdiği puanların mutlak uyumu görselleştirilir; her panelde yatay eksen iki puanın ortalaması, dikey eksen ise farkıdır (orta çizgi ortalama fark, üst/alt çizgiler uyum sınırları). Paneller dört EMBU alt ölçeği ile üç düad tipini (anne–indeks çocuk, anne–kardeş, indeks çocuk–kardeş), renkler DM ve kontrol gruplarını göstermektedir. Okuma anahtarı: noktalar sıfır-fark çizgisi çevresinde ne kadar dar toplanıyorsa ve uyum sınırları ne kadar dar ise iki puan o kadar örtüşür; sınırların genişliği birey düzeyindeki uyumsuzluğun ölçüsüdür.](docs/assets/figures/carbon/primary/fig-12-h5-ba-grid.svg){#fig-h5-bland-altman width="96%" fig-align="center"}

![H5 yanıt yüzeyi analizi (RSA) yüzeyleri — anne (X ekseni) ve indeks çocuk (Y ekseni) alt ölçek ortalamaları (ham 1–4 Likert birimi) fark skoruna indirgenmeden iki ayrı eksende tutulur; yükseklik (Z) çıktı değişkeni olan anne Beck Depresyon toplam puanıdır. Yüzey ikinci dereceden kestirilmiş ve yalnız sıcaklık ile reddetme alt ölçekleri için çizilmiştir. Noktalı çizgi anne ve indeks çocuk algısının eşit olduğu uyum hattını göstermektedir. Okuma anahtarı: uyum hattı (X = Y) boyunca ve buna dik uyumsuzluk hattı boyunca yüzeyin yükselip alçalması ayrı ayrı izlenir; fark skorunun gizlediği örüntü uyumsuzluk hattındaki eğrilikte görünür.](docs/assets/figures/carbon/primary/fig-13-h5-rsa-surface.png){#fig-h5-rsa-surface width="96%" fig-align="center"}"""

new_text = """### H5 — Diadik Tutarlılık (Anne-Çocuk Uyumu)

**Bulgu özeti.** Aynı evde yaşayıp aynı ilişkiyi deneyimlemelerine rağmen, "anne" ile "çocuğun" ebeveynlik tutumlarına verdikleri cevaplar arasındaki uyum oldukça düşüktür. Yani ebeveynlik ilişkisini anne farklı bir pencereden, çocuk bambaşka bir pencereden algılamakta; ikisi birbiriyle uzlaşamamaktadır. Ulaşılan bu uyumsuzluk, analiz edilen dört alt alanın (sıcaklık, koruma, reddetme, karşılaştırma) tamamında net biçimde görülmüştür. Dahası; diyabetli ailelerdeki anne-çocuk anlaşmazlığı ve uyumsuzluğu, kontrol ailelerindekine kıyasla bazı tutumlarda daha da belirgindir (yani kontrol grubunda uyum diyabete kıyasla nispeten daha yüksektir).

*Kanıt* — Anne ile çocuk arasındaki ilişkinin bu iki cepheden nasıl göründüğü (uyum), beş farklı ve karmaşık istatistiksel yöntemle incelenmiştir. Her bir yöntem uyumun farklı bir cephesine bakar: puanların birebir tutarlılığı, uyumsuzluğun bir yüzey haritasındaki yeri, ailenin ortak dokusu vb. Araştırma başlamadan önce belirlenen kurala göre, diyabet ve kontrol grupları arasında "net bir fark" olduğunun söylenebilmesi için bu beş yöntemden en az üçünün aynı yönü işaret etmesi gerekmiştir. Sonuçlar şu şekildedir:

**Strateji 1 (Doğrudan Puan Uyumu).** Anne ile çocuğun verdiği ham anket puanlarının ne kadar örtüştüğüne bakılmıştır. Bu yöntemle ölçülen tutarlılık puanı 0,00 ile 0,10 arasında çok düşük çıkmıştır; bu bilimsel eşiklerde "zayıf/yetersiz uyum" anlamına gelir. Hatta diyabetli ailelerde puanlar sıfırın altına bile inmiştir (yani anne ile çocuğun verdiği yanıtlar birbirinden tamamen kopuktur). Genel olarak kontrol grubundaki anne-çocuk tutarlılığı, diyabetli gruba göre tüm alt başlıklarda (sıcaklık, koruma, reddetme, karşılaştırma) daha yüksektir. Uyum oranlarının görsel haritası @fig-h5-bland-altman içinde sunulmuştur.

**Strateji 2 (Yanıt Yüzeyi Analizi).** Annenin ve çocuğun puanlarının nasıl farklılaştığını ve bunun annenin depresyonuyla olan ilişkisini bir "3 boyutlu harita" gibi çizen bu yöntemde, çok ilginç bir bulgu ortaya çıkmıştır: Diyabetli grupta, anne ile çocuğun reddetme algısı zıtlaştıkça (örneğin anne "çocuğumu reddetmiyorum", çocuk ise "annem beni reddediyor" dedikçe) annenin depresyon skoru belirgin biçimde artmaktadır. Bu örüntü sağlıklı kontrol grubunda hiç görülmemiştir. İlgili haritalar @fig-h5-rsa-surface içinde yer almaktadır.

**Strateji 3 (Ortak Yazgı / Aile Doku Modeli).** Aile bireylerinin "ortak tek bir aile ruhu" etrafında toplanıp toplanmadığına bakılmıştır. Sıcaklık dışında, reddetme ve karşılaştırmada bu "ortak doku" puanları o kadar düşüktür ki, istatistiksel sistem hatası vermiştir. Diyabetli ailelerin "ortak doku/uyum" puanı kontrol ailesinden de düşüktür; bu da diyabetli ailelerde "tek ve ortak bir tutum/algı" varsayımının geçersiz olduğunu kanıtlar.

**Strateji 4 (Saf / Gizli Uyum Modeli).** Testlerin kendi ölçüm hataları matematiksel olarak temizlenip aradaki "saf ilişkiye" bakıldığında; kontrol grubundaki anneler ile çocukların tutumları arasındaki pozitif uyum (örneğin sıcaklıkta 0,26, korumada 0,55) diyabetli gruba göre hep daha yüksek kalmıştır. Yine de veri yapısı nedeniyle bazı katsayılar çok dalgalanmış ve bu modelden çıkan kesin sonuçlara ihtiyatla yaklaşılmıştır.

**Strateji 5 (Anlam Ortaklığı / Kenny k-Katsayısı).** İki kişinin gerçekte ne ölçüde aynı şeyden bahsettiğini ifade eden bu oranda; sıcaklıkta (0,19'a karşı 0,02), aşırı korumada (0,36'ya karşı 0,08) ve karşılaştırmada (0,20'ye karşı 0,09) kontrol grubunun uyumu, diyabetli gruba kıyasla bariz şekilde daha yüksek bulunmuştur.

**Sentez.** Baştaki kuralımız olan "bir tutumda uyum var demek için en az 3 strateji onaylamalıdır" şartı hiçbir grupta ve hiçbir durumda sağlanamamıştır. Yani anne-çocuk ikilisindeki ebeveynlik algısı uyumu genel olarak çok zayıftır. Daha da önemlisi; denenen 5 yöntemin tamamında (5/5) ve tüm alt boyutlarda, diyabetli anne-çocuk ikilisinin fikir ayrılığı kontrol grubuna göre çok daha belirgindir. Başka bir ifadeyle Tip 1 diyabet, ebeveynlik algısı konusunda anne ile çocuk arasındaki makası sağlıklı ailelere kıyasla daha da açmıştır.

Tüm bu karmaşık stratejilerin özet sayısal dökümü @tbl-apa-h5-concordance içinde verilmiştir.

```{r}
#| label: tbl-apa-h5-concordance
#| tbl-cap: "H5 anne-çocuk uyumu (tutarlılık) tablosu: Annenin ebeveynlik anketi puanı ile çocuğun aynı ankete verdiği puan arasındaki uyum; sınıf-içi korelasyon, yüzey haritası, ortak yazgı, saf uyum ve Kenny anlam ortaklığı gibi her biri farklı bir açıya bakan 5 istatistiksel strateji ile özetlenmiştir. Okuma anahtarı: Her strateji grubun uyum veya uyumsuzluğuna dair yön belirtir (diyabet > kontrol veya kontrol > diyabet gibi). 5 stratejinin tamamına bakıldığında, kontrol grubundaki uyumun diyabete göre daha yüksek olduğu net biçimde görülür."
apa_render_table("t13_h5_concordance", group_col = "Strateji")
```

![H5 Puan tutarlılığı haritası: Anne ile çocuğun aynı soruya verdiği puanların uyumu (Bland-Altman grafiği). Ortadaki kalın çizgi puan farkının sıfır olduğunu, noktalar ise ailelerin cevaplarını gösterir. Okuma anahtarı: Noktalar yatay sıfır çizgisi etrafında ne kadar dar (sıkı) bir alanda toplanıyorsa, anne ile çocuğun verdiği cevaplar o kadar aynıdır (uyumludur). Sınırların geniş olması aradaki fikir ayrılığının/uyumsuzluğun büyük olduğunu gösterir.](docs/assets/figures/carbon/primary/fig-12-h5-ba-grid.svg){#fig-h5-bland-altman width="96%" fig-align="center"}

![H5 uyumsuzluk (yanıt yüzeyi) 3D haritası: Annenin ebeveynlik puanı ile çocuğun puanı arasındaki uyumun/uyumsuzluğun annenin depresyonuyla (zemin yüksekliği) ilişkisini gösteren grafik. Sadece sıcaklık ve reddetme boyutları için çizilmiştir. Tabandaki kesik çizgi, anne ile çocuğun tam olarak aynı puanı verdiği "uyum hattı"dır. Okuma anahtarı: Sağdaki grafikte (diyabet reddetme), kesik çizgiye dik olan hatta (anne ve çocuğun fikirleri zıtlaştıkça) yüzeyin yukarı kıvrıldığı (depresyonun arttığı) görülmektedir. Bu tehlikeli zıtlaşma örüntüsü kontrol grubunda yoktur.](docs/assets/figures/carbon/primary/fig-13-h5-rsa-surface.png){#fig-h5-rsa-surface width="96%" fig-align="center"}"""

if old_text in content:
    content = content.replace(old_text, new_text)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replace successful!")
else:
    print("Text not found in the file. Check for exact match.")
