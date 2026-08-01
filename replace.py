import sys

file_path = "chapters/04_bulgular.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_text = """Çalışmaya 241 aile dâhil edilmiştir: 120 diyabet (DM) ailesi ve 121 kontrol ailesi.
Her aileden anne, indeks çocuk ve sağlıklı kardeş katılımıyla uzun-format analiz
tabanına 482 çocuk satırı yazılmıştır. Dört çocuk-rolü hücresi dengelidir:
DM-indeks 120, DM-kardeş 120, kontrol-indeks 121, kontrol-kardeş 121. DM grubunda
indeks çocuk Tip 1 diyabet tanısı taşımakta, kardeş sağlıklı biyolojik kardeştir;
kontrol grubunda hem indeks hem kardeş sağlıklıdır. Taranan ve reddeden ailelerin
saha akışı kanonik analiz kilidinde izlenebilir olmadığından, doğrulanabilir analiz
seti akışı raporlanmış, tarama öncesi akış raporlama sınırlılığı olarak belirtilmiştir.
Kilitlenmiş kanonik veri tabanından aile düzeyi analiz tabanına ve DM klinik alt-analiz
katmanına geçiş @fig-strobe-flow içinde gösterilmiştir.

@tbl-apa-sample-characteristics aile düzeyi sosyodemografik, anne ruh sağlığı, klinik
ve psikolojik göstergeleri DM ve kontrol grupları arasında karşılaştırmaktadır. İki
grubun bir değişkende ne kadar farklılaştığını görmek için standardize ortalama fark
(SMD) kullanılmıştır: bu değer sıfıra ne kadar yakınsa gruplar o kadar benzerdir
[@austin2009balanceDiagnostics] (|SMD| < 0,10 iyi denge; 0,10–0,25 sınırda; 0,25–0,50
dengesiz; ≥ 0,50 ciddi dengesizlik). Ham gözlemde üç değişkende (0,25 üzeri)
dengesizlik saptanmıştır; yani herhangi bir düzeltme yapılmadan, iki grubun bu üç
değişkende belirgin biçimde ayrıştığı görülmüştür: anne antidepresan kullanımı
(DM %29, kontrol %9; SMD = 0,53), anne eğitim düzeyi (SMD = 0,29) ve eş eğitim düzeyi
(SMD = 0,32). Eş (baba) mesleki indeksi (ISEI-08; SMD = 0,23) ile anne yaşı
(medyan DM 38,5 yıl, kontrol 37,3 yıl; SMD = 0,21) sınırda dengesizdir; yani bu iki
göstergede fark daha ılımlı düzeyde kalmıştır. Aile düzeyi ISEI-08, mesleki statü
ISEI-08 baskınlık kuralıyla eş (baba) mesleğinden türetildiğinden eş göstergesiyle
sayısal olarak özdeştir; başka bir deyişle bu iki gösterge aynı değeri taşır ve
@tbl-apa-sample-characteristics içinde tek satır olarak listelenmiştir. Bu üç
sosyoekonomik bileşen latent SES kompozitinde dengelenmiştir (SMD = 0,03); yani üç
gösterge tek bir birleşik SES ölçüsünde toplandığında gruplar arası fark neredeyse
kaybolmaktadır. Bu birleşik latent SES göstergesinin eğitim, mesleki statü ve materyal
(maddi) bileşenlerle korelasyon yapısı @fig-ses-correlation içinde gösterilmiştir.
Nedensel diyagram temelli birincil ayarlama seti (latent SES, kardeş yaş
farkı, aile çocuk sayısı) ham gözlemde maksimum |SMD| = 0,220 (kardeş yaş farkı)
düzeyindeyken, stabilize ters-olasılık ağırlıklandırması (IPTW) sonrası kalan
maksimum |SMD| = 0,004 (latent SES) düzeyine inmiştir; yani analizlerde dikkate
alınan bu değişkenlerin hiçbirinde, dengeyi kuran ağırlıklandırma sonrası kayda değer
bir grup farkı kalmamıştır. Bu değişken bazında denge kazanımı @fig-smd-love içinde
görselleştirilmiştir. Ayarlama setinin dayandığı
nedensel diyagram ve kovaryat ayarlama stratejisi @fig-causal-dag içinde,
DM ve kontrol ailelerinin eğilim skoru dağılımları ile ortak destek (karşılaştırılabilirlik)
aralığı @fig-propensity-overlap içinde gösterilmiştir.

DM klinik profili yalnız DM grubunda raporlanmıştır: HbA1c verisi 39/120 çocukta
mevcuttur (%32,5); HbA1c medyanı %9,0 (ortalama %8,97; en düşük–en yüksek
%5,8–%15,1). HbA1c'si ölçülen 39 çocuğun 8'i (%20,5) %7'nin altında, 11'i (%28,2)
%7–9 aralığında ve 20'si (%51,3) ≥ %9 düzeyinde HbA1c değerine sahiptir. Tanı yaşı
medyanı 7,8 yıl (çeyrekler arası aralık, ÇAA: 5,7–9,3), DM süresi medyanı
3,8 yıl (ÇAA: 2,0–6,0). Tanı yaşı üç strataya ayrıldığında erken (< 5 yaş)
24, okul (5–10 yaş) 69 ve ergen (≥ 10 yaş) 27 aile yer almaktadır. Tüm DM
olgularının tanı yaşı klinik olarak olası aralıktadır (en düşük 0,7 yıl).

Gerçekten toplanamayan (eksik) veri oranı genel olarak düşüktür; en yüksek eksiklik
ISEI-08 mesleki indeksindedir (%9,1), onu Beck toplam puanı (%1,2) ve maddi gösterge
(%0,4) izler. DM süresi ve HbA1c yalnız DM tanılı çocuklarda ölçüldüğü için kontrol
ailelerinde bu değerlerin bulunmaması bir eksiklik değil, çalışma tasarımının doğal
sonucudur. DM süresindeki boşlukların tamamı bu tasarım kaynaklı durumdan gelir (aile
düzeyinde %50,2). HbA1c'de ise buna, DM tanılı çocukların bir kısmında ölçüm kaydının
hiç bulunmaması eklenir (120 çocuğun yalnız 39'unda mevcut); bu boşluklar rastgele
dağılmadığından (MNAR) aile düzeyinde toplam eksiklik %83,8'e ulaşır. Tasarım kaynaklı
ve rastgele olmayan bu boşlukların hiçbiri tahminle doldurulmamış (imputasyon
yapılmamış); HbA1c yalnızca eldeki 39 ailelik alt-örneklemde betimsel olarak
kullanılmıştır (ayrıntılı denetim §4.4.6). Değişken düzeyindeki eksiklik oranları ve
tasarım kaynaklı boş hücreler @fig-missing-pattern içinde gösterilmiştir. Ayrıntılı
sosyodemografik ve klinik betimleyiciler @tbl-apa-sample-characteristics, kovaryat dengesi
@tbl-apa-covariate-balance, eksik veri özeti @tbl-apa-missing-data, eğilim skoru modeli ve
ortak destek @tbl-apa-propensity-model ve sosyoekonomik durum kompozit bileşenleri
@tbl-apa-ses-composite içinde sunulmuştur."""

new_text = """Çalışmaya toplam 241 aile katılmıştır. Bunların 120'si çocuklarından birinde Tip 1 diyabet (DM) olan aileler, 121'i ise tüm çocukları sağlıklı olan (kontrol) ailelerdir. Her aileden anne, bir çocuk (indeks çocuk) ve bir sağlıklı kardeş araştırmaya dâhil edilmiştir. Böylece veri setinde toplam 482 çocuk değerlendirilmiştir. Gruplar şu şekilde dengeli dağılmıştır: 120 diyabetli çocuk, 120 sağlıklı kardeş; 121 sağlıklı kontrol çocuğu, 121 sağlıklı kontrol kardeşi. Diyabet grubunda ilk çocuk (indeks) diyabetli, kardeşi ise sağlıklıdır. Kontrol grubunda ise her iki çocuk da sağlıklıdır. Araştırmanın başında davet edilip katılmayı reddeden ailelerin sayısı veri setinde tam olarak izlenemediği için, yalnızca araştırmaya kesin olarak katılan ailelerin akışı verilmiş ve bu durum bir sınırlılık olarak belirtilmiştir. Verilerin araştırma boyunca nasıl şekillendiği ve analiz aşamasına nasıl getirildiği @fig-strobe-flow içinde gösterilmiştir.

@tbl-apa-sample-characteristics tablosu; sosyodemografik özellikleri, annenin ruh sağlığını, klinik ve psikolojik verileri diyabetli aileler ile sağlıklı aileler arasında karşılaştırmaktadır. İki grubun birbirine ne kadar benzediğini ölçmek için "standardize ortalama fark (SMD)" adı verilen bir değer kullanılmıştır. Bu değer sıfıra ne kadar yakınsa gruplar birbirine o kadar çok benziyor demektir [@austin2009balanceDiagnostics]. Standartlara göre 0,10'dan küçük değerler iyi bir dengeyi (benzerliği), 0,10-0,25 arası sınırda bir farkı, 0,25-0,50 arası dengesizliği ve 0,50 üzeri ise ciddi bir farklılığı gösterir.

İlk bakışta (herhangi bir düzeltme yapılmadan), gruplar arasında üç temel özellikte belirgin farklılıklar (0,25 üzeri SMD) görülmüştür. Bunlar; annenin antidepresan kullanımı (diyabetli grupta %29, kontrol grubunda %9; SMD = 0,53), annenin eğitim düzeyi (SMD = 0,29) ve babanın (eş) eğitim düzeyidir (SMD = 0,32). Babanın mesleki durumu (SMD = 0,23) ve annenin yaşı (diyabetli grupta ortanca değer 38,5 yıl, kontrol grubunda 37,3 yıl; SMD = 0,21) ise sınırda farklılık göstermiştir; yani daha kabul edilebilir düzeydedir. Ailenin genel sosyoekonomik durumu babanın mesleğinden hesaplandığı için tabloda aynı satırda gösterilmiştir.

Gruplar arasındaki eğitim ve gelir gibi sosyoekonomik farklar "gizli (latent) SES kompoziti" adı verilen tek bir birleşik puan üzerinden hesaplandığında, iki grup arasındaki fark neredeyse tamamen ortadan kalkmıştır (SMD = 0,03). Bu birleşik puanın eğitim, meslek ve gelir gibi diğer bileşenlerle olan ilişkisi @fig-ses-correlation içinde verilmiştir.

Araştırmada adil bir karşılaştırma yapabilmek için ailelerin sosyoekonomik düzeyi, kardeşler arası yaş farkı ve çocuk sayısı gibi özellikler matematiksel olarak eşitlenmiştir (buna ağırlıklandırma denir). Başlangıçta bu özellikler açısından en yüksek fark 0,220 (kardeş yaş farkı) iken, ağırlıklandırma işleminden sonra bu fark 0,004'e (latent SES) kadar düşmüştür. Yani gruplar arasında analizleri etkileyecek kayda değer bir fark kalmamıştır. Bu dengeleme süreci @fig-smd-love içinde, yapılan düzeltmelerin arka planındaki nedensel strateji @fig-causal-dag içinde, iki grubun birbiriyle ne kadar karşılaştırılabilir olduğu ise @fig-propensity-overlap içinde gösterilmiştir.

Diyabet (DM) ile ilgili klinik bulgular doğal olarak yalnızca diyabetli çocuklarda incelenmiştir. Kan şekeri kontrolünü gösteren HbA1c verisi 120 diyabetli çocuğun 39'unda (%32,5) mevcuttur. Bu çocukların ortalama HbA1c değeri %8,97 (ortanca/medyan %9,0) olup, değerler %5,8 ile %15,1 arasında değişmektedir. Ölçüm yapılan 39 çocuğun 8'inde (%20,5) ideal kabul edilen %7'nin altında, 11'inde (%28,2) %7-9 arasında ve 20'sinde (%51,3) ise %9 veya üzerinde (yüksek) bulunmuştur.

Diyabetli çocukların hastalığa yakalanma (tanı) yaşının medyanı (ortancası) 7,8 yıl (çeyrekler arası aralık: 5,7–9,3), hastalık sürelerinin medyanı ise 3,8 yıldır (çeyrekler arası aralık: 2,0–6,0). Tanı konulma yaşına göre çocuklar sınıflandırıldığında; 24 çocuk erken dönemde (5 yaşından önce), 69 çocuk okul çağında (5-10 yaş arası) ve 27 çocuk ise ergenlik döneminde (10 yaş ve üzeri) tanı almıştır. Tüm çocukların tanı aldıkları yaş, tıbbi olarak beklenen doğal yaş aralıklarındadır (en erken tanı alan çocuk 0,7 yaşındadır).

Araştırma boyunca toplanması planlanan ancak ulaşılamayan verilerin (eksik veri) oranı genel olarak oldukça düşüktür. En fazla eksiklik babanın meslek bilgisinde (%9,1) görülmüş; bunu Beck depresyon toplam puanı (%1,2) ve maddi durum göstergesi (%0,4) izlemiştir. Hastalık süresi ve kan şekeri (HbA1c) gibi veriler doğal olarak sağlıklı çocuklarda (kontrol grubu) bulunmadığı için, bu kısımların onlarda boş kalması bir veri kaybı değil, araştırmanın yapısının doğal bir sonucudur. Diyabet süresindeki tüm eksiklikler (%50,2) bu tasarım kaynaklı durumdan gelmektedir.

Ancak HbA1c değeri için farklı bir durum söz konusudur. 120 diyabetli çocuğun yalnızca 39'unda ölçüm kaydı bulunabilmiştir. Hem kontrol grubunda zaten bulunmaması hem de bazı diyabetli çocuklarda değerin olmaması nedeniyle, toplam eksiklik oranı aile düzeyinde %83,8'e ulaşmıştır (rastgele olmayan eksiklik). Araştırmada eksik olan bu veriler için istatistiksel herhangi bir tahmin (imputasyon) yöntemi kullanılmamış, boş bırakılmıştır. HbA1c değeri yalnızca verisi olan 39 ailelik grupta durumu özetlemek için kullanılmıştır (ayrıntılı denetim için bkz. §4.4.6). Hangi değişkenlerde eksiklik olduğu ve araştırmanın tasarımından kaynaklı boş kalan kısımlar @fig-missing-pattern içinde gösterilmiştir.

Son olarak; tüm örneklemin detaylı sosyodemografik ve klinik özellikleri @tbl-apa-sample-characteristics, gruplar arasındaki dengenin sayısal değerleri @tbl-apa-covariate-balance, eksik verilerin özeti @tbl-apa-missing-data, dengeleme hesaplamaları (eğilim skoru) @tbl-apa-propensity-model ve sosyoekonomik durumu oluşturan bileşenler @tbl-apa-ses-composite tablolarında detaylı biçimde sunulmuştur."""

if old_text in content:
    content = content.replace(old_text, new_text)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replace successful!")
else:
    print("Text not found in the file. Check for exact match.")
