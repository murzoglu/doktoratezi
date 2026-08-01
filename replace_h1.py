import sys

file_path = "chapters/04_bulgular.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_text = """### H1 — Çocuk Algısı (EMBU-C)

**Bulgu özeti.** T1DM'den etkilenen ailelerin çocukları — hem hasta indeks
çocuk hem de sağlıklı kardeş — annelerinden *reddedilme* ve *aşırı koruma*
algısını, kontrol ailelerinin çocuklarına kıyasla küçük ama tutarlı biçimde daha
yüksek bildirmiştir; bu iki boyut hem klasik hem de Bayesçi analizde doğrulanır.
Sıcaklık boyutundaki sınırdaki frekansçı sinyal Bayesçi analizde doğrulanmadığından
sağlam kabul edilmez; karşılaştırma boyutunda ise gruplar arasında anlamlı fark için
kanıt bulunmamıştır. İki boyuttan reddetme en belirgin olanıdır, aşırı koruma ikinci
sıradadır. Bu fark aile ya da grup düzeyinde yerleşir: tanının eşlik ettiği ailelerde
her iki çocuğun da algısı benzer yönde daha yüksektir; fark, indeks çocuğu sağlıklı
kardeşinden ayırt etmez — aynı ailenin indeks çocuğu ile kardeşi arasında hiçbir
EMBU-C boyutunda fark için kanıt yoktur. Reddetme bulgusu, madde tabanındaki
yığılmaya daha dayanıklı bir psikometrik çözümlemeyle de doğrulanmış ve çocuğun yaşı
ile cinsiyetine göre değişmemiştir.

*Kanıt* — Dört EMBU-C alt ölçeği için, aynı aileden gelen iki kardeşin
birbirine bağımlı yanıtlarını hesaba katan çok düzeyli bir kovaryans analizi 482
çocuk-satırı üzerinde kestirilmiştir.^[Model sabit etkileri: dört düzeyli rol, çocuk
yaşı ve cinsiyeti, latent SES, kardeş yaş farkı ve aile çocuk sayısı. Katsayılar ham
1–4 ölçek puanı birimindedir; havuzlanmış SD = 0,40.] Ön-kayıtlı doğrulayıcı ölçüt,
dört alt ölçeğin grup ana etkisidir: DM ile kontrol grubu arasındaki fark, indeks
çocuk ve sağlıklı kardeş rolleri eşit ağırlıkla ortalanarak verilir ve çoklu
karşılaştırma için BH-FDR ile düzeltilir (@tbl-apa-h1-group). Grup farkı, reddetme
b = 0,14 [0,07; 0,22], q = 0,001 ve aşırı koruma b = 0,19 [0,07; 0,30], q = 0,003 alt
ölçeklerinde belirgindir; sıcaklıkta sınırdadır (b = 0,14 [0,02; 0,25], q = 0,029) ve
karşılaştırmada anlamlı değildir (b = 0,13 [−0,01; 0,26], q = 0,069). Bağımsız Bayesçi
hat reddetmeyi güçlü, aşırı korumayı orta düzeyde doğrular; BF₁₀ değerleri sırasıyla
10,55 ve 6,93'tür. Sıcaklık için ise, frekansçı sinyalin tersine, fark-yokluğu lehine
kanıt verir (BF₁₀ = 0,29); karşılaştırmada ise fark-yokluğu yönündedir (BF₁₀ = 0,53). En güçlü tekil
sinyal reddetmedir; tamamlayıcı iki-grup etki büyüklüğü Hedges g ≈ 0,38
düzeyindedir.^[Bu değer, indeks çocukların iki-grup karşılaştırmasından hesaplanan
betimsel bir ölçüttür ve birincil eşit-rol ölçütünden ayrıdır.] Reddetme farkı, alternatif bir psikometrik yöntemle latent düzeyde de
doğrulanmıştır: β = 0,14 SD [0,04; 0,25] [@samejima1969graded].^[Bu doğrulama, yanıtların
ölçek tabanına yığıldığı durumlara daha dayanıklı olan aşamalı-yanıt (graded response)
madde-yanıt kuramı modeliyle yapılmıştır.] Aynı aileye ait
kardeşlerin benzerliğini gösteren sınıf-içi korelasyon yaklaşık 0,14'tür ve rol × yaş
× cinsiyet etkileşimi anlamlı değildir (FDR p > 0,200). Rol-özgül hücre kontrastları,
Bayesçi çift raporlama ve aile içi indeks-kardeş grup-içi kontrastının ayrıntıları
ilgili tablolarda sunulmuştur: @tbl-apa-h1-primary, @tbl-apa-h1-bayesian ve
@tbl-apa-h1-within-group.^[Grup-içi kontrast keşifsel/post-hoc niteliktedir; hem DM
hem kontrol ailelerinde tüm alt ölçeklerde q > 0,76.] Dört alt ölçeğin grup ana
etkisi @fig-h1-forest içinde gösterilmiştir."""

new_text = """### H1 — Çocuk Algısı (EMBU-C)

**Bulgu özeti.** Diyabetli ailelerin çocukları (hem diyabetli çocuğun kendisi hem de sağlıklı kardeşi), annelerinden *reddedildikleri* ve annelerinin *aşırı korumacı* olduğuna dair algılarını, sağlıklı kontrol ailelerinin çocuklarına göre küçük ama belirgin şekilde daha yüksek bildirmiştir. Bu iki boyuttaki farklılık, birden çok istatistiksel yöntemle test edilmiş ve hepsinde doğrulanmıştır. Anneden algılanan "sıcaklık" boyutu, klasik analizlerde sınırda bir fark göstermiş gibi görünse de daha gelişmiş yöntemlerle (Bayesçi analiz) incelendiğinde bunun gerçek ve sağlam bir fark olmadığı anlaşılmıştır. Taraf tutma/karşılaştırma boyutunda ise iki grup arasında anlamlı hiçbir fark bulunamamıştır. 

Ortaya çıkan farklılıkların en belirgini "reddetme", ikincisi ise "aşırı koruma" algısıdır. İlginç olan bulgu şudur: Bu algı farklılığı çocukların bireysel hastalık durumundan çok "ailenin genel havasından" kaynaklanmaktadır. Diyabet tanısının olduğu ailelerdeki her iki çocuk da (hem diyabetli olan hem de sağlıklı olan) bu algıları benzer seviyede yüksek hissetmektedir. Kısacası, diyabetli ailenin kendi içinde diyabetli çocuk ile sağlıklı kardeşi arasında annenin ebeveynlik tutumu (EMBU-C) açısından hiçbir fark bulunamamıştır. "Reddetme" boyutunda ulaşılan bu sonuç, çocukların yaşından veya cinsiyetinden de etkilenmemiştir.

*Kanıt* — Anneden algılanan dört farklı ebeveynlik tutumu (sıcaklık, aşırı koruma, reddetme, karşılaştırma) incelenirken, aynı evde yaşayan iki kardeşin birbirine benzer cevaplar verebileceği dikkate alınmış ve 482 çocuğun verisi buna uygun özel bir analiz modeliyle hesaplanmıştır.^[Bu modelde çocukların rolü, yaşı, cinsiyeti, ailenin genel sosyoekonomik durumu (latent SES), kardeşler arasındaki yaş farkı ve ailedeki çocuk sayısı gibi faktörler de hesaba katılmıştır. Katsayılar, 1'den 4'e kadar puanlanan anketin ham puanları cinsindendir; genel sapma SD = 0,40'tır.] Önceden planlandığı üzere temel değerlendirme ölçütü, diyabetli aileler ile sağlıklı kontrol aileleri arasındaki genel grup farkıdır. Bu fark hesaplanırken, diyabetli çocuk ve sağlıklı kardeş rolleri eşit derecede hesaba katılmış ve çok sayıda karşılaştırma yapıldığı için hata payını düşüren istatistiksel bir düzeltme (BH-FDR) uygulanmıştır (@tbl-apa-h1-group). 

Gruplar arasındaki fark; reddetme (b = 0,14 [0,07; 0,22], q = 0,001) ve aşırı koruma (b = 0,19 [0,07; 0,30], q = 0,003) alt boyutlarında net biçimde görülmektedir. Sıcaklık boyutu sınırda çıkmış (b = 0,14 [0,02; 0,25], q = 0,029), karşılaştırmada ise anlamlı bir farklılık saptanmamıştır (b = 0,13 [−0,01; 0,26], q = 0,069). 

Sonuçların sağlamlığını teyit etmek için kullanılan ikinci ve bağımsız bir yaklaşım (Bayesçi analiz); reddetme boyutundaki farkın "güçlü", aşırı koruma boyutundaki farkın ise "orta düzeyde" kanıta sahip olduğunu doğrulamıştır (kanıta dayalı güç oranları sırasıyla BF₁₀ = 10,55 ve 6,93'tür). Sıcaklık boyutunda ise ilk klasik analizin aksine gruplar arasında bir "farkın olmadığı" (BF₁₀ = 0,29) yönünde kanıt sunulmuştur. Karşılaştırma boyutu da yine "fark yokluğu" yönündedir (BF₁₀ = 0,53). Ulaşılan en güçlü farklılık "reddetme" boyutundadır (iki grup arasındaki genel etkinin büyüklüğü Hedges g ≈ 0,38 olarak hesaplanmıştır).^[Bu etki büyüklüğü (Hedges g), doğrudan grupların birbirine oranlanmasıyla elde edilen özet betimsel bir ölçüttür ve ana analizimizden farklı bir mantıkla hesaplanmıştır.] Ayrıca reddetme farkı, anketlerde puanların bazen en düşük ya da en yüksek seçenekte birikmesi (yığılma) sorununa daha dirençli olan çok daha gelişmiş bir istatistiksel modelle de ayrıca kanıtlanmıştır: β = 0,14 SD [0,04; 0,25] [@samejima1969graded].^[Bu doğrulama, yanıtların anket tabanına (en düşük puanlara) yığıldığı durumlara karşı daha dayanıklı olan aşamalı-yanıt (graded response) madde-yanıt kuramı modeli kullanılarak yapılmıştır.] 

Aynı aileden gelen kardeşlerin verdikleri cevaplar arasındaki benzerlik oranı yaklaşık %14'tür (0,14) ve ortaya çıkan durum çocuğun rolüne, yaşına veya cinsiyetine göre bir değişim göstermemiştir. Hangi sonuçların sağlıklı çocuktan, hangilerinin diyabetli çocuktan geldiğine dair kırılımlar, doğrulayıcı analizlerin detayları ve ailenin kendi içinde yapılan kardeş kıyaslamaları şu tablolarda detaylıca sunulmuştur: @tbl-apa-h1-primary, @tbl-apa-h1-bayesian ve @tbl-apa-h1-within-group.^[Aynı ailenin çocuklarını (indeks çocuk ve sağlıklı kardeş) birbiriyle kıyaslayan bu grup-içi analizde, hem diyabetli hem de kontrol ailelerindeki kardeşler arasında tüm ebeveynlik boyutlarında anlamlı bir fark bulunmamıştır (q > 0,76).] Dört ebeveynlik boyutunun diyabetli ve kontrol aileleri arasındaki genel fark özeti de grafik olarak @fig-h1-forest içinde gösterilmiştir."""

if old_text in content:
    content = content.replace(old_text, new_text)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replace successful!")
else:
    print("Text not found in the file. Check for exact match.")
