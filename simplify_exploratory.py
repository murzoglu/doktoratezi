import sys

file_path = "chapters/05_tartisma_ve_sonuc.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    """Buraya kadarki yorum, önceden belirlenmiş beş birincil hipoteze dayanıyordu.
Aşağıdaki genişletilmiş katmanlar farklı bir statüdedir: bunlar, hipotezleri sınamak
için değil yeni hipotezler üretmek için yapılmış keşifsel çözümlemelerdir. Bu nedenle
bulguları kesin sonuç değil, bağımsız örneklemlerde doğrulanması gereken öneriler
olarak okunmalıdır. Her biri aşağıda birincil hipotezlerde izlenen sırayla ele
alınmaktadır: önce bulgunun kendisi, sonra dış literatürdeki karşılığı, en sonda
yorum sınırı.

**Aracılık zincirindeki kırılma.** Beck depresyonu → anne-bildirimli reddetme →
çocuk-algılanan reddetme aracılık zincirinde dolaylı etki anlamsız kalmış, doğrudan
etki ise üç modelde de tutarlı belirmiştir (Bulgular, @tbl-apa-mediation). Bu örüntü,
kesitsel verilerde aracılık kestiriminin yapısal bir zaafıyla birlikte okunmalıdır.
Maxwell ve Cole, tek zaman-noktasında ölçülen dolaylı etkilerin, altta yatan süreç
boylamsal bile olsa gerçek etkiyi ciddi biçimde yanlı tahmin ettiğini göstermiştir;
bu yanlılık çoğu zaman etkiyi olduğundan büyük gösterir ya da yönünü değiştirir
[@maxwellCole2011crossMediation]. Dolayısıyla buradaki "kırılma", aktarımın gerçekten
yokluğuna değil, kesitsel tasarımın dolaylı etkiyi güvenilir kestirmekten yapısal
olarak aciz oluşuna da bağlı olabilir. Imai ve arkadaşlarının duyarlılık çerçevesi de
aynı yöne işaret eder: gözlenmemiş bir karıştırıcı, anlamsız görünen dolaylı etkiyi
maskeliyor olabilir [@imaiKeeleYamamoto2010mediationDuyarlilik]. Bu nedenle bulgu,
"depresyon çocuğa reddetme olarak yansımıyor" biçiminde değil, "bu aktarım yolu ancak
boylamsal bir tasarımla güvenilir sınanabilir" biçiminde okunmalıdır.

**Dağılımın üst ucundaki gizli sinyal.** Ortalamaya dayalı H1 analizinde küçük
görünen reddetme etkisi, dağılımsal modellerde farklı bir yüz göstermiştir: reddetme
sinyali dağılımın üst kuyruğunda belirgin biçimde güçlenmektedir (kuantil regresyonda
τ = 0,75 için β = 0,25; beta regresyonda β = 0,46) (Bulgular, §4.4.6). Bu,
ortalama-merkezli çözümlemenin yaygın bir körlüğüne örnektir. Bir etki, örneklemin
çoğunluğunda zayıf olsa bile en yüksek risk taşıyan alt-grupta yoğunlaşabilir;
ortalama ise bu yoğunlaşmayı seyrelterek gizler. Bulgu bu nedenle, en yüksek reddetme
algısına sahip çocuk alt-grubunun ayrı bir klinik ilgi odağı olabileceği yönünde bir
hipotez üretir. Ancak kuyruk kestirimleri örneklem büyüklüğüne duyarlıdır ve bu
alt-örüntü bağımsız doğrulama beklemektedir.

**Kişi-merkezli ebeveynlik tipolojisi.** Latent profil çözümlemesi üç-profilli bir
ebeveynlik tipolojisi önermiştir. Bu tür kişi-merkezli modellerde en kırılgan karar
kaç sınıf tutulacağıdır; sınıf sayısının Bayesçi bilgi ölçütü ve bootstrap
olabilirlik-oranı testiyle birlikte gerekçelendirilmesi standart gerekliliktir
[@nylund2007sinifSayisi]. Psikolojideki latent sınıf uygulamalarını inceleyen güncel
sistematik derlemeler tam da bu noktada yaygın bir uygulama-kılavuz açığı bulmuş,
birçok çalışmanın model seçim ölçütlerini ve sınıf-ayrışma göstergelerini eksik
raporladığını belgelemiştir [@sorgente2025lcaReview]. Çocuk ruh sağlığı alanındaki
derleme de sınıf sayısının ve profil geçerliğinin dış değişkenlerle
çapraz-doğrulanması gerektiğini vurgular [@petersen2019lcaChildMH]. Bu tez, üç-profilli
çözümü kesin bir tipoloji olarak değil, yukarıda anılan keşifsel statüye ve sözü edilen
kanıt standartlarına uygun biçimde bağımsız örneklemde doğrulanması gereken bir öneri
olarak sunar. Kişi-merkezli ebeveynlik profillerinin çocuk uyumuyla
ilişkilendirilebildiği yaklaşımların [@otonomiEbeveynlikProfilleri2021] Tip 1 diyabet
bağlamında henüz uygulanmamış olması, bu katmanın hipotez-üretici değerini de
göstermektedir.

**Ağ yapısında grup farkı için kanıt elde edilmemesi.** Ağ çözümlemesinde iki grubun
(diyabet ve kontrol) ağ yapıları küresel güç ve ağ yapısı bakımından anlamlı biçimde
ayrışmamıştır (Bulgular, @tbl-apa-network). Bu sonucun yöntemsel çerçevesi iki
katmanlıdır: değişkenler arası ilişkiler düzenlileştirilmiş Gauss grafik modeliyle
kestirilmiş [@epskampFried2018ggm], grup farkı ise permütasyon temelli ağ-karşılaştırma
testiyle sınanmıştır [@vanBorkulo2022nct]. Bu keşifsel analizde global strength ya da
ağ yapısı farkı lehine kanıt bulunmamıştır. Ağ-karşılaştırma testinin anlamlı çıkmaması,
grupların yerel (kenar ya da düğüm düzeyi) farkları bulunduğunu göstermez; yalnızca
global fark lehine kanıt elde edilmediğini gösterir. Ayrıca merkeziyet kararlılığı
katsayısı tercih edilen 0,50 düzeyinin altında kalmıştır (CS[0,7] = 0,28); bu nedenle
düğüm merkeziyet sıralamaları kırılgandır ve ihtiyatla yorumlanmalıdır. Ağ psikometrisi
literatürü de küçük-orta örneklemlerde kenar-düzeyi kestirimlerin geniş güven aralıkları
taşıdığını ve tekrarlanabilirliğin sınırlı olduğunu vurgular. Bu nedenle ağ bulguları
bütünüyle doğrulayıcı değil keşifsel düzeyde tutulmuştur.

**Ayrım gücü ile klinik fayda ayrışması.** Bu model, kesitsel veride yüksek depresif
belirti düzeyini *eşzamanlı* olarak sınıflandıran bir tarama/sınıflandırma modelidir;
ileriye dönük bir risk yordama modeli değildir. Belirteçler ile sonuç aynı ölçüm
anında toplandığından zamansal öncelik kurulamaz. Bu genişletilmiş eşzamanlı
sınıflandırma modeli, temel modele göre ayrım gücünü (AUC) artırmıştır. Karar-eğrisi
analizinde incelenen tüm eşik aralığında (0,05–0,50), "herkesi tara" ve "kimseyi
tarama" stratejilerine göre pozitif net fayda sağlamış; ancak bu fayda yalnız düşük
eşiklerde (≈0,05) belirginken daha yüksek eşiklerde marjinal düzeye gerilemiştir
(Bulgular, @tbl-apa-clinical). Bu ayrışma, karar-eğrisi analizinin geliştirildiği temel
gözlemi doğrudan örnekler: bir modelin istatistiksel ayrım gücünü artırması, o modelin
gerçek karar eşiklerinde hastaya net klinik yarar sağlayacağı anlamına gelmez. Net
fayda, doğru ve yanlış pozitiflerin klinik maliyetini birlikte tartan ayrı bir
ölçüttür [@vickersElkin2006dca]. Nitekim optimizm-düzeltilmiş kalibrasyon eğiminin
nokta kestirimi 1'in altındadır (Bulgular, @tbl-apa-clinical); bu değer iç-validasyonda
beklenen hafif aşırı-uyum eğilimiyle uyumludur. Ancak güven aralığının 1'i içermesi
nedeniyle ideal kalibrasyondan istatistiksel olarak ayırt edilememekte ve bu belirsizlik
dış-validasyon gereksinimini pekiştirmektedir. Dolayısıyla genişletilmiş model, iç
geçerliği vaat eden ancak dış-validasyon, yeniden-kalibrasyon ve maliyet-duyarlı eşik
seçimi bekleyen bir prototip olarak konumlandırılmalıdır.""":
    """Buraya kadarki yorumlar, çalışmanın en başında belirlediğimiz temel soruların (5 birincil hipotezin) yanıtlarıydı. Aşağıda bahsedeceğimiz bulgular ise "kesin sonuç" değil, verilerin içine daha derinlemesine daldığımızda karşımıza çıkan ve gelecekteki araştırmalara ışık tutabilecek "yeni ipuçlarıdır". Her bir ipucunu önce kendi verimizde ne anlama geldiği, sonra literatürde nasıl göründüğü, en son da neden dikkatle okunması gerektiği çerçevesinde ele alıyoruz.

**Aracılık zincirindeki kırılma.** "Annenin depresyonu ebeveynliğini bozar, bozulan ebeveynlik de çocuğa reddedilme hissi olarak geçer" teorisini test ettiğimizde (Bulgular, @tbl-apa-mediation), sayılar bize "anne depresyonu doğrudan çocuğa geçiyor" dedi; ortadaki "ebeveynlik" bir köprü (aracı) görevi görmedi. Ancak bilim insanları (Maxwell ve Cole), bizimki gibi "tek seferlik" anket çalışmalarının bu zincirleme ilişkileri doğru tespit etmekte çoğu zaman yetersiz kaldığını gösterir [@maxwellCole2011crossMediation]. Dolayısıyla bu bulguyu "kesinlikle böyle bir geçiş yok" şeklinde değil, "bu geçişi kanıtlamak için aileleri yıllarca izleyen uzun vadeli (boylamsal) çalışmalara ihtiyaç var" şeklinde okumak daha doğru olur [@imaiKeeleYamamoto2010mediationDuyarlilik].

**Ortalamanın arkasına saklanan gizli sinyal.** Tüm diyabetli çocukların ortalamasına baktığımızda "reddedilme" hissi pek dikkat çekici durmuyordu. Ancak gelişmiş istatistiklerle verinin en uç noktalarına (en fazla risk altındaki çocuklara) büyüteç tuttuğumuzda, orada reddedilme hissinin çok daha güçlü (neredeyse iki katı) olduğunu gördük (Bulgular, §4.4.6). Bu bulgu, araştırmacıların her zaman ortalamaya odaklanmasının ne kadar yanıltıcı olabileceğini gösterir. Yani etki, herkes için küçük olsa da, riskli bir çocuk grubunda gayet yakıcı olabilir. Bu nedenle o küçük grup için daha yakın bir klinik inceleme öneriyoruz.

**Ebeveynleri profilleme (Tipoloji).** Anneleri anket cevaplarına göre üç farklı "ebeveynlik profiline" ayırmayı denedik. Psikoloji dünyasında bu tarz profillemeler çok meşhur olsa da, araştırmacıların "kaç profil olmalı" kararını verirken kurallara tam uymadığı bilinmektedir [@sorgente2025lcaReview; @petersen2019lcaChildMH]. Biz kendi modelimizde üç grubu istatistiksel testlerle (Bayesçi ölçütler) savunsak da [@nylund2007sinifSayisi], bunu kesin ve değişmez bir yasa gibi değil, ilerideki çalışmaların test etmesi için sunduğumuz bir "ilk taslak" olarak değerlendiriyoruz.

**Kardeşler arası ağ (Network) yapısında fark bulamadık.** Diyabetli aileler ile sağlıklı ailelerin anket cevaplarını birbirine bağlayan "ağ modellerini" kurduğumuzda, iki ağın şekilsel olarak birbirinden belirgin biçimde ayrışmadığını gördük (Bulgular, @tbl-apa-network) [@epskampFried2018ggm; @vanBorkulo2022nct]. Tabii ki bu, arada hiçbir fark olmadığı anlamına gelmez; sadece elimizdeki verinin "büyük resimde" bir fark kanıtlamaya yetmediğini gösterir. Ayrıca örneklem sayımız sınırlı olduğundan, bu ağdaki noktaların yerlerinin değişme ihtimali yüksektir.

**İyi bir istatistik her zaman "klinik fayda" sağlamaz.** Annelik ve ebeveynlik özelliklerine bakarak "bu annenin depresyonu var mıdır" diye tarama yapan bir model geliştirdik. Bu model istatistiksel olarak başarılı oldu (ayrım gücü arttı). Ancak pratikte (klinikte) bunu "tarama testi" olarak kullanırsak sağlayacağı net fayda, daha yüksek eşiklerde yetersiz kaldı (Bulgular, @tbl-apa-clinical). Tıp literatürü de şunu söyler: İstatistiği ne kadar güçlü olursa olsun, bir testin klinikte hastaya fayda sağlayıp sağlamayacağı, o testin yanlış alarm verme maliyetine bağlıdır [@vickersElkin2006dca]. Dolayısıyla bu modelimiz, şimdilik sadece laboratuvarda çalışan ama sahaya inmeden önce üzerinde ince ayarlar yapılması gereken bir prototiptir."""
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success!")
    else:
        print("Failed to find:\n" + old[:100] + "...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
