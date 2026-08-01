import sys

file_path = "chapters/05_tartisma_ve_sonuc.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    """**Diyabet klinik ağırlığı ile ebeveynlik algısının bağlantısızlığı.** Diyabet
grubuna özgü klinik alt-analizler, metabolik yükün ebeveynlik algısını biçimlendirip
biçimlendirmediğini üç ayrı eksende sınamış ve tutarlı biçimde null sonuç vermiştir
(Bulgular, §4.4.6). Üç eksenin sonuçları şunlardır:

- HbA1c × ebeveynlik etkileşimi dört EMBU-P alt ölçeğinde anlamsız kalmıştır
  (tümü p > 0,400; R² < 0,25).
- Diyabet süresi ile ebeveynlik ilişkisinde kübik spline doğrusal modele üstünlük
  sağlamamıştır.
- Tanı yaşının üç strataya bölündüğü analizde hiçbir sonuçta F testi anlamlılığa
  ulaşmamıştır (en büyük F = 2,05; p = 0,134; kısmi η² < 0,04).

Bu örüntü iki biçimde okunabilir. Yorum düzeyinde, bulgular çocuğun ve
annenin ebeveynlik iklimini metabolik kontrol göstergesinden görece bağımsız
deneyimlediğini düşündürür: ebeveynlik algısı, hastalığın *biyolojik ağırlığına* değil
aile içi ilişkisel örüntüye bağlı olabilir. Bu okuma, Tip 1 diyabette ebeveynlik ile
glisemik kontrol arasındaki ilişkilerin literatürde tutarsız ve çoğu kez zayıf
kaldığını, ebeveyn cinsiyeti ve çocuk yaşına göre değiştiğini bildiren sistematik
derlemeyle [@trojanowski2021] uyumludur.

Ancak bu null'un ihtiyatla okunması
zorunludur. HbA1c verisi çocukların yalnız %32,5'inde (39/120) mevcuttur ve bu
alt-örneklem küçük-orta etki büyüklükleri için yetersiz güçtedir (power < 0,50).
Dahası, aşağıda ayrıntılandırılan seçilim yapısı gereği HbA1c eksikliği rastgele
değildir; bu da gözlenen bağlantısızlığın gerçek bir yokluk mu yoksa güç ve seçilim
kaynaklı bir maskeleme mi olduğunu ayırt etmeyi olanaksız kılar. Dolayısıyla klinik
ağırlık ile ebeveynlik algısının bağımsızlığı, reddedilemez bir sonuç değil, tam-veri
ve yeterli-güçlü örneklemlerde önceliklendirilmesi gereken bir hipotezdir.

**Seçilim yapısı bir bulgu olarak: dönemsel örtüşme ve birincil etkinin
kırılganlığı.** İkincil katmanın belki de yöntemsel olarak en öğretici bulgusu, grup
üyeliğinin veri toplama dönemiyle neredeyse tam örtüşmesidir (toplama yılı × grup
Cramér V = 0,59). Bu yalnız bir sınırlılık kaydı değil, birincil bulgunun sağlamlığı
hakkında doğrudan bilgi taşıyan keşifsel bir sonuçtur. İki grubun en geniş ortak takvim
desteğine sahip olduğu 2023 alt-örnekleminde, H1'in temel bulgusu olan çocuk-algılı
reddetme farkı belirgin biçimde zayıflamaktadır (d = 0,38'den yaklaşık sıfıra). Her iki
grup 2023, 2024 ve 2025 yıllarında da temsil edilmekle birlikte ortak destek
dengesizdir; 2023 tek ortak yıl değil, en geniş ortak temsile sahip dönemdir. Bu
attenüasyon, birincil etkinin bir kısmının grup ile dönemin ayrıştırılamamasından
kaynaklanabileceğini niceliksel olarak gösterir; yani gerçek bir grup etkisinden çok,
farklı dönemlerde toplanan katılımcıların bileşim farkından.

HbA1c erişilebilirliğinin
gözlenen özelliklere göre seçici olması (erişilebilirlik ~ antidepresan kullanımı;
OR = 4,56; p < 0,001) bu tabloyu tamamlar. Hem eksik veri hem de dönemsel bileşim,
örneklemin ortak-etki (collider) üzerinden koşullanmış olabileceğine işaret eder; bu
da karıştırıcılıktan mekanistik olarak ayrı bir yanlılık kaynağıdır
[@hernan2004selectionBias]. Bu örüntü rastgele-olmayan eksiklik (MNAR) olasılığıyla
uyumludur; ancak gözlenmeyen HbA1c değeri ile eksik olma olasılığı arasındaki ilişki
ayrıca modellenmediğinden, tek başına MNAR mekanizmasını tanımlamaz. Bu bulgunun
yorumsal değeri, birincil sonuca ilişkin ihtiyatı somut bir sayıya bağlamasıdır:
çocuk-algısı örüntüsü teorik olarak anlamlı ve çok-kaynaklı desenle tutarlı kalsa da,
ortak takvim desteği dengeli bağımsız bir örneklemde yinelenene dek etki büyüklüğü
kesin kabul edilmemelidir. Bu keşifsel seçilim çözümlemesinin birincil yorumu nasıl
sınırladığı, aşağıda sınırlılıklar bölümünde ayrıca ele alınmaktadır.""" :
    """**Hastalığın ciddiyeti (kan şekeri) ile ebeveynlik hissi arasında bağ bulamadık.** Sadece diyabetli ailelere bakıp, çocuğun kan şekeri kontrolü (HbA1c), hastalığın süresi veya tanı konan yaş gibi 'tıbbi ölçütlerin' ebeveynlik algısını nasıl etkilediğini inceledik (Bulgular, §4.4.6). Üç farklı testin üçünde de sonuç aynıydı: Çocuğun kan şekerinin yüksek veya düşük olması, annenin ebeveynlik anketlerini veya çocuğun hissettiği reddedilme algısını belirgin biçimde değiştirmemektedir. 

Bu durumu iki şekilde yorumlayabiliriz. Birincisi: Aile içindeki ebeveynlik ilişkisi, hastalığın "biyolojik ciddiyetinden" çok, ailenin kendi dinamiğine bağlıdır [@trojanowski2021]. İkincisi (ve daha olası olanı): Hastaneden kan şekeri verisine ulaşabildiğimiz çocuk sayısı çok azdı (sadece 39 çocuk) ve bu eksiklik tesadüfi değildi. Bu nedenle "kesinlikle bağ yoktur" demek yerine "elimizdeki veri bunu kanıtlamaya yetmemiştir" demek daha doğru bir yaklaşımdır.

**Veri toplama zamanlarındaki farklar sonuçları etkilemiş olabilir.** Araştırmanın zayıf karnını dürüstçe test ettiğimizde şunu gördük: Sağlıklı aileler ile diyabetli ailelerin büyük bir kısmı hastaneye aynı yıl veya dönemde gelmemiştir. Veriyi sadece 'iki grubun en yoğun olarak bir arada olduğu' 2023 yılına daralttığımızda, H1'de bulduğumuz o temel "reddedilmişlik hissi" farkı neredeyse sıfıra inmektedir. Bu durum bize şunu söyler: Bulduğumuz farkın küçük bir bölümü hastalıkla değil, anketlerin farklı yıllarda ve mevsimlerde toplanmış olmasıyla ilgili olabilir [@hernan2004selectionBias]. O yüzden elde ettiğimiz istatistiksel sonuçlar kavramsal olarak çok tutarlı olsa da, daha büyük ve zamanı denk gruplarla tekrarlanana kadar bu etkinin büyüklüğüne şüphe payı bırakılmalıdır."""
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success!")
    else:
        print("Failed to find:\n" + old[:100] + "...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
