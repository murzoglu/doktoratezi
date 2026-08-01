import sys

file_path = "chapters/04_bulgular.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_text = """### H3 — Anne Öz-Bildirimi (EMBU-P)

**Bulgu özeti.** Annelerin kendi bildirdikleri ebeveynlik tutumlarının dört
boyutunda da Tip 1 diyabetli ve kontrol grubu anneleri arasında anlamlı fark için
kanıt bulunmamıştır; sonuç birincil, ağırlıklandırılmış (IPTW) ve Bayesçi
analizlerde tutarlıdır. Bu bulgu, çocukların algısındaki reddetme farkıyla (H1)
birlikte okunduğunda, farkın anne öz-bildiriminde *görünür olmadığına* işaret eder:
anneler kendi tutumlarında bir ayrışma bildirmezken, çocuklar bunu algı düzeyinde
dile getirmektedir.

*Kanıt* — Dört EMBU-P alt ölçeği için kovaryans analizi 241 anne üzerinde
kestirilmiştir. Ham grup katsayıları^[Katsayılar standardize edilmemiştir; ham EMBU-P
ölçek puanı birimindedir.] sıcaklık b = 0,06 [−0,07; 0,20], aşırı koruma
b = 0,06 [−0,12; 0,24], reddetme b = −0,05 [−0,12; 0,02] ve karşılaştırma
b = 0,06 [−0,08; 0,20] düzeyindedir; dört alt ölçeğin tamamında fark anlamsızdır
(FDR-düzeltilmiş p > 0,500). Standardize etki de küçüktür: mutlak değerlerin tümü
0,17'nin altındadır ve en büyüğü reddetmededir (β = −0,16). Grup dengesizliğini
düzelten ağırlıklandırma ve daha güvenilir standart hatayla tekrarlanan
modelde^[Stabilize ve uç değerleri budanmış ters-olasılık ağırlıklandırması (IPTW) ile
heteroskedastisiteye dayanıklı standart hata kullanılmıştır.] katsayılar −0,04 ile
0,05 arasında, yine anlamsız düzeyde kalmıştır (FDR p > 0,510). Antidepresan kullanan
(n = 46) ve kullanmayan (n = 195) anneler ayrı incelendiğinde de sonuç, yön ve
büyüklük olarak bütün örneklemden farklılaşmamıştır. Bağımsız Bayesçi hat da fark
yokluğu konumunu destekler: Bayes faktörleri BF₁₀ = 0,17–0,23 aralığındadır (fark-yok
lehine orta düzeyde kanıt). Farkın pratik olarak ihmal edilebilir sayıldığı aralığa
(ROPE) düşen posterior pay sıcaklıkta %68, aşırı korumada %61, reddetmede %93 ve
karşılaştırmada %69'dur. Önceden belirlenmiş en küçük anlamlı fark eşiğinde (±0,30 SD)
eşdeğerlik testi (TOST) aşırı koruma ve karşılaştırmayı "Eşdeğer", sıcaklık ve
reddetmeyi "Belirsiz" sınıflamıştır. Bu karar, seçilen eşdeğerlik sınırına (SESOI)
duyarlıdır: daha muhafazakâr ±0,20 ve ±0,25 SMD bantlarında hiçbir alt ölçekte
biçimsel eşdeğerlik kalmamaktadır (Ek 5, @tbl-apa-tost-sensitivity). Birincil ve IPTW
grup etkileri @tbl-apa-h3-primary-iptw, duyarlılık ve Bayesçi/TOST katmanı
@tbl-apa-h3-sensitivity, antidepresan-katmanlı grup etkileri
@fig-h3-stratified-forest içinde sunulmuştur.

```{r}
#| label: tbl-apa-h3-primary-iptw
#| tbl-cap: "H3 birincil ve ters olasılık ağırlıklı (IPTW) grup etkileri — annelerin kendi bildirdiği (EMBU-P) dört alt ölçekte DM–Kontrol grup farkı, hem birincil model hem de gözlemsel gruplar arası dengeyi ölçüm-öncesi değişkenlere göre yeniden ağırlıklandıran IPTW hattıyla birlikte raporlanır. Sütunlar 241 anne örnekleminde standardize etkiyi (β) ve %95 güven aralığını verir; ham b ölçek puanı katsayıları metinde raporlanmıştır. Okuma anahtarı: bir alt ölçeğin güven aralığı sıfırı içeriyorsa grup farkı sıfırdan ayırt edilemez; birincil ve IPTW satırları yan yana okunarak sonucun ağırlıklandırmaya duyarlı olup olmadığı görülür."
apa_render_table("t10_h3_primary_iptw")
```

```{r}
#| label: tbl-apa-h3-sensitivity
#| tbl-cap: "H3 duyarlılık ve çift raporlama — H3 grup-farkı sonucunun sağlamlığı üç ayrı katmanda sınanır: antidepresan kullanımına göre alt-örneklem, bağımsız bir Bayesçi hat (Bayes faktörü BF₁₀ ve pratik eşdeğerlik bölgesi ROPE payı) ve eşdeğerlik sınaması (TOST). Satırlar analiz katmanına göre gruplanmıştır. Okuma anahtarı: BF₁₀ Jeffreys ölçeğinde 1'in altındaysa fark-yokluğu (H0) lehine kanıt anlamına gelir; ROPE payı puanların pratik-eşdeğerlik bandına düşme oranını verir; TOST kararı seçilen eşdeğerlik sınırına (SESOI) bağlı olduğundan sınırla birlikte okunur."
apa_render_table("t11_h3_sensitivity", group_col = "Katman")
```

![H3 antidepresan-katmanlı orman grafiği — annelerin kendi bildirdiği (EMBU-P) dört alt ölçekte DM–Kontrol grup ana etkisi, üç katman halinde yan yana sunulur. Paneller antidepresan kullanan, kullanmayan ve tüm örneklem katmanlarını; noktalar birincil modelden kestirilen grup etkisini (ham ölçek puanı birimi), yatay çizgiler %95 güven aralığını göstermektedir. Okuma anahtarı: bir katmanda güven aralığı dikey sıfır çizgisini kesmiyorsa o katmanda grup farkı sıfırdan ayırt edilir; üç katman karşılaştırılarak etkinin antidepresan kullanımına göre değişip değişmediği izlenir.](docs/assets/figures/carbon/primary/fig-10-h3-stratified-forest.svg){#fig-h3-stratified-forest width="96%" fig-align="center"}

### H4 — Anne Depresyonu → EMBU-P Latent Yapısal Eşitlik Modeli

**Bulgu özeti.** Annedeki depresyon belirtileri arttıkça, annenin bildirdiği
sıcaklık azalmakta; reddetme ve karşılaştırma ise artmaktadır. Bu ilişkiler
istatistiksel olarak anlamlıdır; ancak çalışmanın kesitsel tasarımı gereği
*neden-sonuç* değil, birlikte-değişim (eş-değişim) düzeyinde okunmalıdır. Ayrıca
modelin genel uyumu sınırlı olduğundan, bulgu "iyi oturan bir modelin çıktısı"
olarak değil, bu model koşullarında gözlenen anne-bildirimli birlikte-değişimler
olarak ihtiyatla yorumlanmalıdır.

*Kanıt* — Anne depresyonu ile ebeveynlik tutumları arasındaki ilişkiler, 21 Beck ve
29 EMBU-P maddesini içeren elli ordinal gösterge üzerinde tek bir yapısal eşitlik
modeliyle kestirilmiştir.^[Sıralı (Likert) yanıtlara uygun WLSMV kestirim yöntemi
kullanılmıştır. Model, elli maddede tam veriye sahip 237 ailede kestirilmiştir
(analitik gruplar: kontrol 121, DM 116); 241 aileden 4'ü, WLSMV'nin varsayılan
liste-bazlı eksik veri işlemi nedeniyle tam-vaka örneklemine girmemiştir.] Model
yakınsamıştır (CFI = 0,887; TLI = 0,890; RMSEA = 0,027; SRMR = 0,127). Dört yapısal
yoldan üçü FDR-düzeltmeli olarak anlamlıdır: Beck → sıcaklık β = −0,28 [−0,45; −0,15],
Beck → reddetme β = 0,33 [0,19; 0,53] ve Beck → karşılaştırma β = 0,28 [0,14; 0,49]
(hepsinde FDR p < 0,001). Beck → aşırı koruma yolu pozitif ancak anlamlı değildir
(β = 0,08; FDR p = 0,22). Bu yollar kesitseldir ve eş-değişim düzeyinde okunur. Modelin
genel uyumu karışıktır: RMSEA düşük olsa da CFI ve TLI yaygın 0,90/0,95 eşiklerinin
altında, SRMR ise 0,08 ölçütünün üzerindedir. Bu nedenle "yordar" ya da "mekanizmayla
açıklar" değil, "bu model koşullarında birlikte değişmektedir" dili benimsenmiştir.
Modelin DM ve kontrol gruplarında aynı işleyip işlemediği, daraltılmış bir madde
setiyle (13 EMBU-P + 6 Beck) çok-grup değişmezlik taramasıyla sınanmıştır. En temel
iki düzey — yapılandırmasal ve yük değişmezliği — sağlanmıştır (ΔCFI < 0,010;
ΔRMSEA < 0,015); en katı kesişim düzeyinde bazı gruplardaki boş yanıt kategorileri
birleştirilerek çözüm elde edilmiştir. Düzey-bazlı uyum indeksleri @tbl-apa-h4-invariance
içindedir. Değişim ölçütleri eşik içinde kalsa da mutlak model uyumu üç düzeyde de
sınırlı olduğundan, sonuç tam değişmezliğin güçlü kanıtı değil, ihtiyatla okunması
gereken bir eşdeğerlik göstergesidir. Yöntemde tanımlanan "yaklaşık sıfır" önsellü
Bayesçi SEM yalnızca önceden sabitlenmiş bir ön-uçuş (preflight) planı düzeyinde
bırakıldığından doğrulayıcı bir çözüm raporlanmamakta; H4 kestirimi yukarıdaki WLSMV
çözümüne dayanır. Standardize yollar @tbl-apa-h4-sem içinde sunulmuştur.

```{r}
#| label: tbl-apa-h4-sem
#| tbl-cap: "H4 Beck → EMBU-P latent yapısal eşitlik modeli — annedeki depresyon (Beck, 21 madde) ile annenin bildirdiği ebeveynlik tutumları (EMBU-P, 29 madde) arasındaki dört yapısal yol, sıralı yanıtlara uygun WLSMV kestirim yöntemiyle 237 ailede tek modelde tahmin edilir. Tablo iki bölümdür: yapısal yol katsayıları (standardize β, %95 güven aralığı, FDR-düzeltilmiş p) ve modelin global uyum indeksleri (CFI, TLI, RMSEA, SRMR). Okuma anahtarı: her yolun β işareti ilişkinin yönünü, güven aralığının sıfırı içerip içermemesi ise ayırt edilebilirliğini gösterir; uyum indeksleri tek bir indekse bakılarak değil hepsi birlikte okunarak değerlendirilir."
apa_render_table("t12_h4_sem")
```

```{r}
#| label: tbl-apa-h4-invariance
#| tbl-cap: "H4 çok-grup (DM vs Kontrol) ölçüm değişmezliği — H4 modelinin ölçüm cetvelinin iki grupta aynı işleyip işlemediği, giderek kısıtlanan üç düzeyde (yapılandırmasal, yük/metrik, kesişim/scalar) daraltılmış madde setiyle sınanır. Tablo her düzeyin mutlak uyum indekslerini ve düzeyler arası değişim ölçütlerini (ΔCFI/ΔRMSEA) verir. Okuma anahtarı: iki ayrı soru iki ayrı sütun grubundan okunur — 'cetvel iki grupta benzer mi?' düzeyler arası Δ sütunlarından (Cheung-Rensvold ihlal sınırı ΔCFI ≤ −0,010 / ΔRMSEA ≥ 0,015), 'model uyumu iyi mi?' ise her satırın mutlak CFI/RMSEA/SRMR sütunlarından yanıtlanır."
apa_render_table("t12b_h4_multigroup_invariance")
```"""

new_text = """### H3 — Anne Öz-Bildirimi (EMBU-P)

**Bulgu özeti.** Annelerin kendi ebeveynlik tutumları hakkındaki değerlendirmelerinde (sıcaklık, aşırı koruma, reddetme ve karşılaştırma), diyabetli çocuk anneleri ile kontrol grubu anneleri arasında anlamlı bir fark bulunmamıştır. Bu "fark yokluğu" sonucu, pek çok farklı analiz yöntemiyle doğrulanmıştır. Ancak hatırlanacağı üzere çocukların kendi değerlendirmelerinde (H1) annelerinden reddedilme algılarında bir farklılık çıkmıştı; annelerin kendi bildirimlerinde böyle bir fark çıkmaması, anne ile çocuğun ebeveynlik tutumunu farklı algıladığını gösteren ilgi çekici bir çelişkidir. Annenin tutumunda böyle bir farkın görülmeyip çocukların algısında görülmesi tartışma bölümünde ele alınmıştır.

*Kanıt* — Annelerin bildirdiği dört tutum 241 anne üzerinden incelenmiştir. Ham verilerle yapılan karşılaştırmalarda diyabetli anneler ile kontrol anneleri arasında sıfırdan ayırt edilebilir bir farka rastlanmamıştır (p > 0,500).^[Katsayılar standardize edilmemiştir; ham EMBU-P ölçek puanı birimindedir.] Bu sonuç, sonradan aileler arası eşitsizlikleri düzelten daha gelişmiş istatistiksel bir ağırlıklandırmayla (IPTW) test edildiğinde de değişmemiştir (p > 0,510). Dahası; annesi antidepresan kullanan aileler (n = 46) kendi içlerinde özel olarak incelendiğinde de sonuç değişmemiş, bulgunun anne psikolojisindeki farklılıklardan kaynaklanmadığı doğrulanmıştır. 

Klasik yöntemlerin ötesinde bağımsız bir doğrulama yöntemi olarak kullanılan Bayesçi analiz de, gruplar arasında bir fark *olmadığına* dair güçlü (H0 lehine) kanıtlar sunmuştur. Ayrıca, aradaki farkın uygulamada hiçbir önem taşımayacak kadar küçük olduğunu gösteren eşdeğerlik testi (TOST) de, annelerin verdikleri cevapların temelde "eşdeğer" olduğunu ya da birbirlerinden ayırt edilemeyecek kadar yakın olduğunu göstermiştir (Ek 5, @tbl-apa-tost-sensitivity). Çeşitli model sonuçları, ağırlıklandırmalar ve antidepresan durumuna göre kırılımlar şu tablo ve grafiklerde detaylandırılmıştır: @tbl-apa-h3-primary-iptw, @tbl-apa-h3-sensitivity ve @fig-h3-stratified-forest.

```{r}
#| label: tbl-apa-h3-primary-iptw
#| tbl-cap: "H3 EMBU-P (annenin kendi bildirdiği ebeveynlik) değerlendirme tablosu: Annelerin dört ebeveynlik tutumunda diyabet ve kontrol grupları arası fark, önce yalın (birincil model) olarak, ardından ailelerin bazı özellikleri (sosyoekonomik vb.) istatistiksel olarak 'eşitlenip ağırlıklandırılarak' (IPTW) verilmiştir. Tabloda etkinin boyutu (β) ve %95 güven aralığı sunulmuştur. Okuma anahtarı: Temel olarak güven aralığının sıfırı içerip içermediğine (sıfır varsa gruplar arası fark yoktur) bakılır; ağırlıklandırma (IPTW) yapıldığında da sonucun değişmediği görülür."
apa_render_table("t10_h3_primary_iptw")
```

```{r}
#| label: tbl-apa-h3-sensitivity
#| tbl-cap: "H3 sağlamlık (duyarlılık) kontrolleri tablosu: Annelerin ebeveynlik farkı bulunmayışı bulgusu üç ayrı yolla yeniden sınanmıştır: antidepresan kullanım durumu, Bayesçi analiz ve eşdeğerlik sınaması (TOST). Okuma anahtarı: Bayes kanıtı (BF₁₀) değerinin 1'in altında olması gruplar arası 'fark olmadığı' yönündeki kanıtı destekler; TOST kararı ise belirlenen sınırlara göre grupların pratikte eşdeğer (aynı) kabul edilip edilemeyeceğini gösterir."
apa_render_table("t11_h3_sensitivity", group_col = "Katman")
```

![H3 antidepresan durumuna göre ayrıştırılmış orman grafiği: Annelerin bildirdiği dört ebeveynlik tutumunda gruplar (diyabet-kontrol) arası farkın antidepresan kullanıp kullanmamaya göre değişip değişmediğini gösterir. Noktalar tahmini etkiyi, yatay çizgiler ise güven aralığını ifade eder. Dikey kalın çizgi "sıfır fark" (fark yok) çizgisidir. Okuma anahtarı: Bir katmandaki yatay çizgi dikey sıfır çizgisine dokunuyor veya kesiyorsa, o durumda gruplar arasında anlamlı bir fark yoktur.](docs/assets/figures/carbon/primary/fig-10-h3-stratified-forest.svg){#fig-h3-stratified-forest width="96%" fig-align="center"}

### H4 — Anne Depresyonu ve Ebeveynlik İlişkisi

**Bulgu özeti.** Annedeki depresyon belirtileri arttıkça, annenin çocuğuna gösterdiğini belirttiği "sıcaklık" azalmakta; buna karşılık "reddetme" ve "karşılaştırma" tutumları artmaktadır. İstatistiksel olarak ortaya konan bu ilişki, çalışmanın ölçüm yöntemi (zaman içindeki takibi değil, tek bir andaki fotoğrafı çekmesi) nedeniyle kesin bir "neden-sonuç" ilişkisi olarak değil, bu iki durumun "birlikte değiştiği" yönünde yorumlanmalıdır. İstatistiksel model mükemmel bir uyum göstermediği için ulaşılan sonuç kesin bir kuraldan ziyade bu grubun genel bir gözlemi olarak okunmalıdır.

*Kanıt* — Anne depresyonu (21 soru) ile ebeveynlik tutumları (29 soru) arasındaki ilişki toplam 50 soruluk karmaşık bir istatistiksel ağ modeliyle (yapısal eşitlik) analiz edilmiştir.^[Verilerin türüne uygun bir tahmin yöntemi kullanılarak tam cevap vermiş 237 ailenin verisiyle analiz yapılmıştır.] Dört ilişki yolundan üçü istatistiksel olarak anlamlı çıkmıştır: Depresyon puanı arttıkça, sıcaklığın düştüğü (β = −0,28), reddetmenin (β = 0,33) ve karşılaştırmanın (β = 0,28) arttığı görülmüştür (hepsi için p < 0,001). Aşırı korumada ise artış yönünde bir eğilim olsa da bu sonuç istatistiksel olarak anlamlı bulunmamıştır.

Modelin genel geçerliliğine dair uyum indekslerine bakıldığında (CFI = 0,887; TLI = 0,890; RMSEA = 0,027; SRMR = 0,127); hata oranları (RMSEA) düşük olsa da genel uyum eşiklerinin bilimsel olarak istenen altın standartların tam anlamıyla karşılanmadığı görülmüştür. Bu yüzden sonuçları aktarırken "depresyon reddetmeye yol açar" gibi iddialı bir neden-sonuç dili yerine "depresyon ve reddetme birlikte görülmektedir" dili tercih edilmiştir. Modelin diyabetli ve kontrol ailelerinde aynı şekilde çalışıp çalışmadığına bakıldığında büyük ölçüde iki grubun da bu kuralları (depresyon-tutum ilişkisini) adil ve benzer biçimde yaşadığı doğrulanmıştır. Detaylı istatistik yolları @tbl-apa-h4-sem tablosunda özetlenmiştir.

```{r}
#| label: tbl-apa-h4-sem
#| tbl-cap: "H4 Anne depresyonu ve ebeveynlik ilişkisi modeli: Annenin depresyon düzeyi (Beck) ile annenin ebeveynlik tutumları (EMBU-P) arasındaki yapısal ilişkilerin tablosudur. Tabloda etkinin gücü/yönü (β), güven aralığı ve anlamlılık (p) değerleri ile birlikte bu analiz modelinin genel uyum performansı sunulmuştur. Okuma anahtarı: β değerinin başında eksi (-) varsa o iki durumun zıt yönlü (biri artarken diğeri azalır), eksi yoksa aynı yönlü (ikisi birlikte artar) hareket ettiğini gösterir."
apa_render_table("t12_h4_sem")
```

```{r}
#| label: tbl-apa-h4-invariance
#| tbl-cap: "H4 gruplar arası ölçüm adilliği tablosu: H4 modelinin, diyabetli annelerde ayrı kontrol grubu annelerinde ayrı mı davrandığı (taraflı ölçüm), yoksa her ikisinde de benzer kurallarla mı işlediği (adil cetvel) analiz edilmiştir. Üç farklı kısıtlama seviyesinde cetvelin gruplar arasında tutarlılığı test edilmiştir. Okuma anahtarı: İlgili Δ sütunlarının eksi veya artı değerlerde çok küçük (0,01 sınırında) kalması ölçüm cetvelinin gruplar arasında adil olduğuna (benzerliğe) işaret eder."
apa_render_table("t12b_h4_multigroup_invariance")
```"""

if old_text in content:
    content = content.replace(old_text, new_text)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replace successful!")
else:
    print("Text not found in the file. Check for exact match.")
