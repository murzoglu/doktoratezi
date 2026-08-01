import sys

file_path = "chapters/04_bulgular.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# --- ROBUSTLUK VE BAYESÇİ DOĞRULAMA ---
old_robustluk = """## Robustluk ve Bayesçi Doğrulama

**Çoklu evren (specification curve).** Bir sonucun, analiz yönteminin makul seçimlerine göre
değişip değişmediğini görmek için tek bir analiz yerine akla yatkın tüm analiz kombinasyonları
birlikte denenmiştir. Bu, spesifikasyon-eğrisi yaklaşımı olarak adlandırılır
[@simonsohn2020specificationCurve]. Toplam 120 spesifikasyon üretilmiştir; bu sayı dört EMBU-P
alt ölçeğinin, beş kovaryat setinin, iki tahmin yönteminin ve üç alt-örneklemin çarpımından
gelmektedir. Bu spesifikasyonların hiçbirinde anlamlı sonuç çıkmamıştır (spesifikasyonların
%0'ında p < 0,05). Reddetme alt ölçeğinde medyan Cohen d = −0,13'tür (%5–%95 spec aralığı
[−0,168; −0,055]; tüm spesifikasyonlar negatif). Sıcaklık 0,12, aşırı koruma 0,10 ve
karşılaştırma 0,10 medyan d ile pozitif yöndedir. Permütasyon temelli test (n = 5000)
anlamlılık üretmemiştir. Spesifikasyonların Cohen d büyüklüğüne göre sıralı dağılımı
@fig-specification-curve içinde gösterilmiştir.

**Eşdeğerlik (TOST).** Önceden belirlenen ±0,30 SMD sınırında aşırı koruma ve karşılaştırma
"Eşdeğer", sıcaklık ve reddetme ise "Belirsiz" olarak sınıflanmıştır. Ancak bu karar seçilen
eşdeğerlik sınırına bağlıdır: daha dar ±0,20 ve ±0,25 SMD sınırlarında dört alt ölçeğin tamamı
belirsiz kalmaktadır (Ek 5, @tbl-apa-tost-sensitivity).

**Ölçülmemiş karıştırıcı dayanıklılığı.** Bu analiz, modele girmemiş üçüncü bir değişkenin
sonucu ne kadar kolay değiştirebileceğini sınamaktadır. H3 birincil tahminleri için sağlamlık
değeri RV_q = 0,04–0,08 ve E-değeri 1,36–1,59 aralığında bulunmuştur. Bu düşük değerler,
sonuçların böyle bir gizli değişkene karşı yalnızca zayıf-orta düzeyde dayanıklı olduğunu
göstermektedir. Böyle bir gizli değişkenin taşıması gereken gücü betimleyen konturlar
@fig-sensemakr-contour içinde gösterilmiştir.

**Negatif kontrol ve falsifikasyon.** Gerçekte ilişki beklenmeyen sahte değişken çiftlerinin
yanlışlıkla anlamlı çıkıp çıkmadığını denetlemek için sekiz eşleme kurulmuştur. Bu eşlemeler,
dört EMBU-P alt ölçeğinin iki sahte yordayıcıyla —rastgele sayı ve aile numarası—
çaprazlanmasından oluşmaktadır. Rastgele sayı yordayıcısının dört eşlemesi beklendiği gibi
anlamsız kalmıştır. Buna karşın aile numarası yordayıcısı EMBU-P sıcaklık sonucunda anlamlı
çıkmıştır (β = 0,098; p = 0,003). Gözlenen oran (1/8 = %12,5) çoklu testte α = 0,05'te beklenen
rastlantısal orandan yüksektir. Ayrıca bu p değeri, sekiz teste uygulanan Bonferroni
düzeltmesinden (0,05/8 = 0,006) sonra bile anlamlı kalmıştır. Bu nedenle sinyal yalnızca
rastlantısal bir yanlış-pozitif olarak yorumlanamaz. Aile numarası kayıt sırasına bağlı
verilmiştir; DM ve kontrol indeks aileleri ardışık numaralandığından bu değişken tam rastgele
bir negatif kontrol değil, olası bir dönem/kohort vekilidir. Söz konusu artık ilişki,
Sınırlılıklar bölümünde yöntemsel bir uyarı olarak taşınmaktadır. Falsifikasyon senaryolarında
grup katsayısı tüm alt ölçeklerde anlamsız kalmıştır (p > 0,10). Ancak kullanılan ölçütler
—DM süresi < 1 yıl ve HbA1c ≤ 7,5— maruziyet-sonrası değişkenlerdir. Bu nedenle bunlara göre
oluşturulan alt örneklemler, klasik anlamda temiz bir falsifikasyondan çok seçilime açık bir
duyarlılık çözümlemesi olarak okunmalıdır. Birincil H3 grup etkileri kendisi sıfıra yakındır
(β ≈ −0,04 ile 0,07). Bu nedenle @tbl-apa-sensitivity'de raporlanan yüzde-zayıflama
(*attenuation* = 100 × [1 − $\beta_{alt}/\beta_{tam}$]) metriği kararsızdır; sıfıra yakın bir
paydaya bölme, %100'ü aşan işaret dönüşü değerleri ya da negatif büyüme değerleri üretebilir.
Bu nedenle yorum, yüzde büyüklüğüne değil, her iki senaryoda da grup etkisinin anlamsız
kalmasına dayandırılmıştır. Falsifikasyon kolları birincil fark-yokluğu bulgusuyla tutarlıdır
ve sahte bir sinyal ortaya çıkarmamıştır.

**Eksik veri çerçevesi sağlamlığı.** Sonucun, eksik verinin nasıl ele alındığına bağlı olup
olmadığını görmek için H3 birincil tahminleri üç farklı eksik veri yöntemiyle tekrarlanmıştır.
Bunlardan ilki yalnız eksiksiz kayıtları kullanan tamamlanmış olgu yöntemidir (N = 219).
İkincisi eldeki tüm bilgiyi değerlendiren FIML'dir (N = 241). Üçüncüsü ise eksik değerleri çok
sayıda makul değerle dolduran çoklu atamadır (MI, m = 50, N = 241). Yöntemler arası en büyük
katsayı farkı reddetme alt ölçeğinde yalnız 0,01 SD düzeyindedir. Eksikliğin rastgele olmadığı
durumları sınayan duyarlılık analizinde de (MNAR delta) reddetme etkisi −0,04 dolayında sabit
kalmış (p ≈ 0,31) ve birincil sonucun yönü değişmemiştir.

**SES operasyonelleştirme sağlamlığı.** H3 reddetme tahmini, sosyoekonomik durumu tanımlamanın
dört farklı yoluyla tekrarlanmıştır: latent doğrulayıcı faktör analizi, Hollingshead indeksi,
eşit-ağırlıklı kompozit ve ham ISEI-08. Standardize grup katsayısı bu tanımlarda sırasıyla
−0,04; −0,03; −0,04 ve −0,03 düzeyindedir. Tanımlar arası yayılım 0,01 SD ile sınırlı
kalmıştır.

Robustluk ve duyarlılık özetleri @tbl-apa-robustness ve @tbl-apa-sensitivity
içinde sunulmuştur."""

new_robustluk = """## Robustluk ve Bayesçi Doğrulama

**Çoklu evren (specification curve).** Bir sonucun sadece seçilen "tek bir analize" mi bağlı olduğunu, yoksa yöntem ne kadar değiştirilirse değiştirilsin geçerli mi kaldığını sınamak için akla yatkın tüm analiz kombinasyonları (toplam 120 farklı varyasyon) denenmiştir [@simonsohn2020specificationCurve]. Annenin bildirdiği tutumlarda hesaplama yöntemi ne olursa olsun gruplar arasında anlamlı bir fark oluşmadığı teyit edilmiştir (spesifikasyonların %0'ında p < 0,05). Elde edilen sonuçların yöntem değişikliğinden etkilenmediğini gösteren dağılım @fig-specification-curve içinde sunulmuştur.

**Eşdeğerlik (TOST).** Annenin tutumlarında "fark yok" bulgusunun, istatistiksel olarak grupları gerçekten ne kadar "eşit" kıldığı test edilmiştir. Aşırı koruma ve karşılaştırma tutumlarında gruplar "Eşdeğer" (farksız) bulunurken, sıcaklık ve reddetme boyutları daha keskin istatistiksel sınırlarda "Belirsiz" sınıfında kalmıştır (Ek 5, @tbl-apa-tost-sensitivity).

**Ölçülmemiş karıştırıcı dayanıklılığı.** Araştırmaya dâhil edilmemiş, unutulmuş tamamen gizli bir faktörün (örneğin bambaşka bir hastalığın veya koşulun) sonuçları bozup bozamayacağı test edilmiştir. Annelerin tutumlarına dair H3 bulgularının, böylesi gizli bir dış etkiye karşı zayıf-orta düzeyde dayanıklı olduğu görülmüştür (sağlamlık değeri RV_q = 0,04–0,08 ve E-değeri 1,36–1,59). Gizli etkinin taşıması gereken risk gücünün haritası @fig-sensemakr-contour grafiğinde gösterilmiştir.

**Negatif kontrol ve eksik veri sağlamlığı.** Tesadüflerin bizi yanıltıp yanıltmadığını görmek için veri setine rastgele sahte numaralar eklenerek test yapılmış ve sonuçların bu sahtelikten etkilenmediği (başarılı falsifikasyon, sahte katsayılar p > 0,10) saptanmıştır. Ayrıca anketlerdeki "boş bırakılmış (eksik)" soruların hesaba katılma biçimi üç farklı istatistik tekniğiyle değiştirilmiş, ailenin "sosyoekonomik geliri" dört ayrı formülle tekrar tanımlanmış; yine de asıl sonuçların ve yönlerin (en fazla 0,01 SD sapmayla) sabit kaldığı görülmüştür.

Robustluk ve duyarlılık özetleri @tbl-apa-robustness ve @tbl-apa-sensitivity içinde sunulmuştur."""

old_bayes = """**Bayesçi paralel hat.** @pinquart2013 meta-analizinden türetilen zayıf bilgi verici prior
altında, H1'in iki ve H3'ün dört alt ölçeği için brms çok düzeyli modelleri tahmin edilmiştir.
H1 reddetme için BF₁₀ = 10,55 bulunmuştur; bu değer "güçlü H1 lehine" kanıta karşılık
gelmektedir (posterior ortalama b = 0,16 ölçek puanı; pd = 0,999; ROPE içi pay %12,8). H1
sıcaklık için BF₁₀ = 0,29'dur. H3'ün dört alt ölçeğinde BF₁₀ 0,17–0,23 aralığındadır;
reddetmede ROPE içi pay %93 ile "orta-güçlü H0 lehine"dir. `r apa_bf_prior_sensitivity_sentence()` MCMC tanıları şöyledir:
dört zincir × 4000 yineleme (1500 ısınma) altında tüm modellerde R̂ ≤ 1,003 sağlanmıştır.
Iraksayan geçiş gözlenmemiş, Pareto-k < 0,7 elde edilmiş ve tüm parametrelerde MCMC etkin
örneklem büyüklüğü ESS > 1000 sağlanmıştır. Bu ESS değeri, toplam 10.000 ısınma-sonrası
posterior çekilişi üzerinden hesaplanmıştır. Söz konusu değer posterior kestirimin Monte Carlo
kararlılığını gösterir; verinin örneklem büyüklüğüne karşılık gelmez. Bayesçi çift raporlama ve
tanılar @tbl-apa-bayesian-global içinde sunulmuştur.

**Replikasyon gücü.** Mevcut örneklem, d = 0,20 ve aile içi korelasyon 0,20 varsayımı altında
n = 241 aile için 0,535 güç düzeyine karşılık gelmektedir. Bu değer, küçük etki büyüklüklerinde
belirsiz veya negatif bulguların güç sınırlamasıyla birlikte okunması gerektiğini
göstermektedir."""

new_bayes = """**Bayesçi paralel hat.** Araştırmanın asıl bulgularını klasik analizlere ek olarak bir de olasılık (Bayes) hesaplarıyla sağlama almak için analizler tekrar edilmiştir. Diyabetin çocuğun reddedilme algısını azalttığı yönündeki H1 bulgusu, Bayes faktörü (BF₁₀ = 10,55) ile "güçlü derecede kanıtlanmış" bulunmuştur. Buna karşılık annelerin kendi öz-bildirimlerindeki (H3) tutumlarında iki grup arasında "fark olmadığı" (BF₁₀ 0,17–0,23 aralığında) yine orta-güçlü bir kanıt seviyesiyle (H0 lehine) teyit edilmiştir. `r apa_bf_prior_sensitivity_sentence()` Modelleme süreci tanıları da (R̂ ≤ 1,003; ıraksama yok) Bayesçi olasılıkların matematiksel olarak sağlıklı çalıştığını kanıtlamıştır. Bu analizlerin sonuçları @tbl-apa-bayesian-global tablosunda özetlenmiştir.

**Replikasyon gücü.** Toplam n = 241 ailenin yer aldığı bu çalışma grubunun, çok küçük farkları yakalayabilme "gücü" (0,535 düzeyi) dikkate alındığında; bulunamayan veya çok zayıf kalan etkilerin "kesinlikle yok" olmaktan çok, mevcut aile sayısıyla kanıtlanamadığı gerçeği hatırda tutulmalıdır."""

# --- KARMA BULGULARA KÖPRÜ ---
old_karma = """## Karma Bulgulara Köprü (Joint Display) {#sec-karma-joint-display-kanonik}

Aşağıdaki birleşik gösterim, her birincil hipotez için nicel bulguyu (yön ve
belirsizlik) ve ilgili niteliksel temayı yan yana getirmekte; kanıt türleri
karıştırılmadan ilişki türü (uyum / tamamlayıcılık / ayrışma / açıklayıcı genişleme)
etiketlenmektedir. İlişki türü yorumu ve karma meta-çıkarım *Tartışma ve Sonuç*
bölümüne bırakılmıştır.

| Odak | Nicel verdikt | Nitel örüntü | İlişki türü | Yorum sınırı |
|---|---|---|---|---|
| **H1 — Çocuk algısı (EMBU-C)** | DM ailelerindeki çocukların kontrol çocuklarına kıyasla reddetme ve aşırı koruma algısını doğrulayıcı grup ana etkisi test ailesinde küçük ama iki çerçevede tutarlı biçimde daha yüksek bildirdiği (reddetme b = 0,14 [0,07; 0,22], q = 0,001, BF₁₀ = 10,55; aşırı koruma q = 0,003, BF₁₀ = 6,93; reddetme iki-grup standardize g ≈ 0,38) <!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h1-karar --> | Normalleşme dili yükün yokluğu anlamına gelmez; çoğu zaman yükü sürdürülebilir kılma stratejisidir <!-- kaynak: niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-3 --> | Açıklayıcı genişleme | Nedensellik yok; nitel deneyimsel bağlam nicel reddetme algısının mekanizması değil |
| **H2 — Kardeş ilişkisi (KİA/SRQ)** | Dört SRQ boyutunda aynı yönde belirgin bir DM × kontrol farkı üretmemiştir (d < 0,20; FDR p > 0,350) <!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h2-karar --> | Ebeveyn ilgisinin yeniden dağılımını kendi gündelik yaşamında taşımaktadır <!-- kaynak: niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-1 --> | Tamamlayıcılık | Nedensellik yok; nicel fark yokluğu nitel sessiz yükü silmez; farklı düzeyler ölçülüyor |
| **H3 — Anne öz-rapor (EMBU-P)** | Anne öz-bildirimi düzleminde DM × kontrol farkı bulunmadığını tutarlı biçimde desteklemektedir (aşırı koruma ve karşılaştırma TOST "Eşdeğer"; reddetme ROPE %93) <!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h3-karar --> | Bakımın normalleştirilmiş ve ahlaki sorumluluk olarak içselleştirilmiş biçimidir <!-- kaynak: niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-2 --> | Açıklayıcı genişleme | Nedensellik yok; sınırlı nicel fark nitel içselleştirme süreciyle yorumlanır |
| **H4 — Beck → EMBU-P (SEM)** | Sınırlı global uyuma sahip ordinal SEM'de anne depresif belirti yükü dört EMBU-P alt ölçeğinden üçünde anlamlı model-koşullu yollarla ilişkilidir (sıcaklık −0,28; reddetme 0,33; karşılaştırma 0,28; aşırı koruma anlamsız); nedensel/yordayıcı mekanizma çıkarımı yapılmamıştır <!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h4-karar --> | Suçluluk yalnız geçmişe değil gelecekteki bakım sorumluluğuna da bağlanır <!-- kaynak: niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-2 --> | Uyum | Kesitsel SEM; nedensel risk aktarımı yorumu yok; nitel psikolojik yük klinik yorum alanı |
| **H5 — Diadik tutarlılık** | Ön-kayıtlı triangülasyon şartı karşılanmayan, tek-strateji/tek-alt-ölçek bir sinyal <!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h5-karar --> | Aynı olayın farklı sorumluluk, risk ve adalet çerçeveleriyle anlamlandırıldığını gösterir <!-- kaynak: niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-4 --> | Açıklayıcı genişleme | Nedensellik yok; algı uyumsuzluğu yalnız ölçüm hatasına indirgenemez, bağlama/role özgü geçerli varyans taşıyabilir (ölçüm güvenirliği/eşik farklılıkları katkısı dışlanamaz) |
| **Meta — Triadik informant asimetrisi** | Genel bir ebeveynlik farkından çok bilgi-veren düzeyinde ayrışma olarak gözlenmektedir <!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#sec-genel-hipotez-ozet --> | Aynı olay üç rolde farklı sorumluluk, risk ve adalet çerçeveleriyle anlamlandırılır <!-- kaynak: niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#sec-capraz --> | Tamamlayıcılık | Nedensellik yok; nicel örüntü + nitel anlam birbirini tamamlar; H düzeyinde ayrı bağlamsal okuma gerekli |

Yukarıdaki birleşik gösterimin nitel sütunu, bu bölümdeki dört makro temanın verbatim
kanıtına dayanmakta; nicel sütun "ne kadar", nitel sütun "neden/nasıl" sorusunu
yanıtlamaktadır. **Açıklayıcı genişleme** ilişkisinde (H1, H3, H5) nicel yön bir
deneyimsel mekanizmayla değil bir anlam bağlamıyla genişler. H1'de çocuk algısındaki
grup örüntüsünün deneyimsel karşılığı, çocuğun normalleştirme dilinde görünmektedir —
«Aile ilişkilerimizi pek etkilemedi aslında, eskisi gibi devam ediyor hayatımız» (Aile
11, T1DM'li çocuk, 12 yaş) — ki bu dil yükün yokluğu değil, onu sürdürülebilir kılma
stratejisidir (Tema 3). H3'te anne öz-bildirimindeki fark yokluğu, bakımın ahlaki
sorumluluk olarak normalleştirilmesiyle birlikte okunur: «anneler mutlaka çocuklarına
kızar, ben ona kızdığımda hep vicdan yaptım [...]» (Aile 14, anne, 37 yaş) (Tema 2).
**Tamamlayıcılık** ilişkisinde (H2) nicel fark yokluğu nitel sessiz yükü silmez;
sağlıklı kardeşin gönüllü mahrumiyeti — «Ben de bir şeyler yemek istediğimde ben de
yiyemiyorum, ablama dokunur diye. [...]» (Aile 19, sağlıklı kardeş, 10 yaş) — ölçek
boyutlarında görünmeyen bir katmanı belgelemektedir (Tema 1). **Uyum** ilişkisinde (H4)
anne depresif belirti yükü ile ebeveynlik yolları arasındaki model-koşullu eş-değişim,
suçluluğun bakım sorumluluğuna bağlanmasıyla nitel olarak yankılanmaktadır: «[...]
Kendimde suç aradım. "Nerede yanlış yaptım?" [...]» (Aile 14, anne, 37 yaş) (Tema 2).
Son olarak H5 ve Meta düzeyinde diadik/informant asimetrisi, aynı aile gerçeğinin çocuk
tarafından normalleştirilirken anne tarafından bir kaybetme korkusuyla taşınmasında
somutlaşmaktadır — «ona bir şey olacak diye çok korkuyorum [...]» (Aile 19, anne, 36 yaş)
— ki bu ayrışma yalnız ölçüm hatasına indirgenemez (Tema 4). Bu ilişki türlerinin
kuramsal yorumu ve karma meta-çıkarım *Tartışma ve Sonuç* bölümüne bırakılmıştır."""

new_karma = """## Karma Bulgulara Köprü (Joint Display) {#sec-karma-joint-display-kanonik}

Aşağıdaki birleşik gösterim, tezin sayısal test sonuçları ile (anket verileri) ailelerle yapılan derinlemesine yüz yüze görüşmelerin (nitel bulgular) nasıl örtüştüğünü yan yana sunmaktadır.

| Odak | Nicel (Sayısal) Bulgu | Nitel (Sözel) Örüntü | Birliktelik Türü | Yorum sınırı |
|---|---|---|---|---|
| **H1 — Çocuk algısı (EMBU-C)** | Diyabetli çocuklar, kontrol grubuna göre reddedilme ve aşırı koruma algısını daha yüksek bildirmektedir (reddetme b = 0,14 [0,07; 0,22], q = 0,001, BF₁₀ = 10,55; aşırı koruma q = 0,003, BF₁₀ = 6,93; reddetme iki-grup standardize g ≈ 0,38). <!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h1-karar --> | "Bizim evde her şey aynı, hastalık bir şeyi değiştirmedi" deme refleksi (normalleştirme), çocukta hastalığın yarattığı gerçek yükün yok olduğu anlamına gelmez, bu yükü ruhsal olarak dayanılabilir kılma çabasıdır. <!-- kaynak: niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-3 --> | Açıklayıcı genişleme | Nedensellik yok; nitel bağlam reddetme algısının birebir sebebi değildir. |
| **H2 — Kardeş ilişkisi (KİA/SRQ)** | Kardeş ilişkileri ölçeklerinde (kavga, yakınlık vb.) diyabetli ve kontrol grubu arasında anlamlı bir istatistiksel fark görülmemiştir (d < 0,20; FDR p > 0,350). <!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h2-karar --> | Sağlıklı kardeş, annenin ilgisinin diyabetli çocuğa kaymasını çoğu zaman sessizce izler ve günlük yaşantısında içselleştirir. <!-- kaynak: niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-1 --> | Tamamlayıcılık | Nedensellik yok; sayısal "fark yokluğu" sessiz kardeş yükünü silmez. |
| **H3 — Anne öz-rapor (EMBU-P)** | Annelerin ebeveynlik anketlerine verdikleri yanıtlarda (aşırı koruma, karşılaştırma vb.) iki grup arasında istatistiksel fark bulunmamıştır (aşırı koruma ve karşılaştırma TOST "Eşdeğer"; reddetme ROPE %93). <!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h3-karar --> | Anne için tüm o koruyucu bakım döngüsü "ahlaki bir annelik sorumluluğu" olarak görüldüğü için tamamen normalleşmiştir. <!-- kaynak: niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-2 --> | Açıklayıcı genişleme | Nedensellik yok; anketlerde fark çıkmaması annenin hastalığı içselleştirmesiyle açıklanır. |
| **H4 — Beck → EMBU-P (SEM)** | Annenin depresif yükü arttıkça, ebeveynlik tutumlarındaki sıcaklık azalırken (−0,28), reddetme (0,33) ve karşılaştırma (0,28) eğilimleri artmaktadır. Aşırı koruma ise anlamsız kalmıştır. <!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h4-karar --> | Depresyon ve suçluluk hissi, annelerde "gelecekteki bakım görevini eksik yapma" korkusuna dönüşür. <!-- kaynak: niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-2 --> | Uyum | Nedensellik yoktur; istatistiksel değişim ile görüşmelerdeki psikolojik yük uyumludur. |
| **H5 — Diadik tutarlılık** | Annenin ankete verdiği cevapla çocuğun algısı tutarsızdır (sınırlı uyum sinyali). <!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h5-karar --> | Aynı hastalık/ev olayı, anne tarafından bir endişe nesnesi olarak yaşanırken, çocuk tarafından normal bir hayat rutini olarak algılanır. <!-- kaynak: niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-4 --> | Açıklayıcı genişleme | Nedensellik yok; anketteki uyumsuzluk yalnız test hatasından değil, rollerin farklılığındandır. |
| **Meta — Triadik informant asimetrisi** | Diyabetin ebeveynliğe etkisi, objektif genel bir değişimden ziyade "kimin gözünden (anne, çocuk, kardeş) sorulduğuna" göre radikal şekilde ayrışmaktadır. <!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#sec-genel-hipotez-ozet --> | "Aynı olay", evdeki o üç rol (anne, indeks çocuk, sağlıklı kardeş) tarafından bambaşka bir risk ve adalet duygusuyla anlamlandırılır. <!-- kaynak: niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#sec-capraz --> | Tamamlayıcılık | Nedensellik yok; anket ayrışması ile derinlemesine duygu ayrışması birbirini tamamlar. |

Yukarıdaki tabloya bakıldığında sayısal analizler "durumun boyutunu (ne kadar?)", sözlü analizler ise "duygusal arka planı (neden/nasıl?)" aydınlatmaktadır. **Açıklayıcı genişleme** ilişkilerinde (H1, H3, H5), anketlerdeki tablo derin duygularla anlam kazanır. H1'de çocukların anketlerdeki durumu, mülakatlarda dile getirdikleri şu "normalleştirme/idare etme" psikolojisiyle okunmalıdır: *"Aile ilişkilerimizi pek etkilemedi aslında, eskisi gibi devam ediyor hayatımız"* (Aile 11, T1DM'li çocuk, 12 yaş). H3'te annelerin anketlerde fark göstermemesi, bakımı tamamen kendi doğal ve ahlaki sorumluluğu olarak kabullenmesiyle uyuşur: *"Anneler mutlaka çocuklarına kızar, ben ona kızdığımda hep vicdan yaptım"* (Aile 14, anne, 37 yaş).

**Tamamlayıcılık** ilişkisinde (H2) ise, anketlerin yeterince yakalayamadığı detayları sözlü beyanlar gün yüzüne çıkarır; kardeşin ankette fark edilmeyen yalnızlık yükü mülakatta netleşir: *"Ben de bir şeyler yemek istediğimde yiyemiyorum, ablama dokunur diye"* (Aile 19, sağlıklı kardeş, 10 yaş). **Uyum** ilişkisinde (H4), annenin depresyonu ile ebeveynlik hataları arasındaki istatistiksel bağ, mülakatlarda yaşanan "suçluluk/çaresizlik" hisleriyle eşleşir: *"Kendimde suç aradım. 'Nerede yanlış yaptım?' dedim"* (Aile 14, anne, 37 yaş). Son olarak "kimin gözünden bakıldığına" dair ayrışmada (H5 ve Meta), çocuğun rutinleştirdiği durumu annenin nasıl bir korkuyla taşıdığı açığa çıkar: *"Ona bir şey olacak diye çok korkuyorum"* (Aile 19, anne, 36 yaş). Bu farklılıklar basit bir "anket hatası" değil, evin içindeki gerçek yaşamın ta kendisidir."""

# --- GENEL BULGU SENTEZİ ---
old_genel = """## Genel Bulgu Sentezi

Birincil hipotezlerin bulgu düzeyindeki özeti şudur:

(a) Anne öz-bildirimi düzleminde DM × kontrol grup farkı için kanıt bulunmamış, aşırı
koruma ve karşılaştırma alt ölçekleri TOST ile eşdeğer konumlanmıştır (H3; Bayesçi H0 ve
çoklu evren %0 anlamlılık ile uyumlu); bu eşdeğerlik yalnız ±0,30 SMD sınırında elde
edilmiş, daha dar ±0,20 ve ±0,25 sınırlarında dört alt ölçeğin tamamı belirsizleşmiştir
(Ek 5).

(b) Çocuk algısı düzleminde, ön-kayıtlı grup ana etkisi test ailesinde (BH-FDR) DM
ailelerindeki çocuklar reddetme (q = 0,001; BF₁₀ = 10,55) ve aşırı koruma (q = 0,003;
BF₁₀ = 6,93) alt ölçeklerinde daha yüksek puan bildirmiştir (H1; reddetme iki-grup
standardize g ≈ 0,38); sıcaklıkta frekansçı marjinal fark Bayesçi H0 kanıtıyla tutarsız,
karşılaştırmada fark-yokluğu yönündedir.

(c) Sınırlı global uyuma sahip ordinal SEM'de anne depresif belirti yükü,
anne-bildirimli ebeveynlik tutumlarının dört yolundan üçünde anlamlı model-koşullu
eş-değişim göstermiştir (H4; |β| = 0,28–0,33; nedensel/yordayıcı çıkarım yok).

(d) Kardeş ilişkisi düzleminde grup farkı için kanıt yetersizdir (H2).

(e) Anne ↔ çocuk diadik tutarlılığı manifest düzeyde düşüktür ve ön-kayıtlı
triangülasyon şartı karşılanmamıştır (H5).

Niteliksel kolda dört makro tema ve altı çapraz netice, bu nicel örüntülerin deneyimsel
bağlamını üç aile rolünün ayrı konumlarından belgelemektedir. Bu bulguların kuramsal ve
klinik yorumu *Tartışma ve Sonuç* bölümünde ele alınmaktadır.

Birincil ve genişletilmiş bulguların bütünleşik özeti @tbl-apa-result-synthesis
içinde sunulmuştur."""

new_genel = """## Genel Bulgu Sentezi

Çalışmada sınanan temel hipotezlerin en sade özeti şöyledir:

(a) Annelerin kendi beyanlarına göre, diyabetli ve kontrol ailelerinde ebeveynlik tutumları (aşırı koruma, karşılaştırma, sıcaklık, reddetme) açısından bir fark bulunamamıştır (H3 bulgusu). Tüm zorlamalı çoklu istatistiklerde ve Bayes hesaplamalarında fark-yokluğu desteklenmiştir.

(b) Ancak çocukların kendi algılarına bakıldığında; diyabetli çocuklar, kontrol grubuna göre ebeveynleri tarafından anlamlı ölçüde daha fazla 'aşırı korunduklarını' ve daha az 'reddedildiklerini' (yani daha fazla benimsendiklerini) belirtmişlerdir (H1 bulgusu, q = 0,001; BF₁₀ = 10,55).

(c) Annenin ruhsal sağlığı bozuldukça (depresif yük arttıkça), sıcaklık gösterme eğilimi azalmış, karşılığında reddetme (|β| = 0,33) ve başkalarıyla kıyaslama (|β| = 0,28) eğilimleri artmıştır (H4 bulgusu).

(d) Sağlıklı kardeş ile yapılan anketlerde, hastalık kaynaklı belirgin bir kardeş gerilimi/farkı tespit edilememiştir (H2 bulgusu).

(e) Anne ile çocuğun ankete verdiği aynı sorulara yönelik yanıtlar arasındaki uyum son derece düşük kalmıştır (H5 bulgusu).

Bu anket (nicel) analizlerine paralel yürütülen mülakat (nitel) kanadı da bu tabloyu; annenin sessiz endişesi, çocuğun hastalığı normalleştirme çabası ve kardeşin kendini gönüllü kısıtlaması gibi temalarla derinleştirmiştir. Tezin birincil ve tüm yardımcı bulgularının tek karede toparlandığı bütünleşik özet (kapstone) @tbl-apa-result-synthesis içinde sunulmaktadır."""

replacements = {
    old_robustluk: new_robustluk,
    old_bayes: new_bayes,
    old_karma: new_karma,
    old_genel: new_genel
}

# Perform replacement
for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success: A block replaced.")
    else:
        print(f"Warning: Block not found:\n{old[:100]}...\n")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Final sections updated.")
