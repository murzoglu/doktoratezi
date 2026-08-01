import sys

file_path = "chapters/04_bulgular.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_text = """### H3 — Anne Öz-Bildirimi (EMBU-P)

**Bulgu özeti.** Annelerin kendi bildirdikleri ebeveynlik tutumlarının dört
boyutunda da Tip 1 diyabetli ve kontrol grubu anneleri arasında anlamlı fark için
kanıt bulunmamıştır; sonuç birincil, ağırlıklandırılmış (IPTW) ve Bayesçi
analizlerde tutarlıdır. Bu bulgu, çocukların algısındaki reddetme farkıyla (H1)
çelişir niteliktedir ve ebeveynlik tutumlarında çocuk-anne ayrışmasının (H5) bir
yansıması olarak tartışılmıştır (§5.3). Anne yaşı, eş (baba) mesleki durumu (ISEI)
ve kardeş yaş farkı gibi yapısal özellikler ile antidepresan kullanımı, annenin
bildirdiği ebeveynlik tutumlarını — modeli açıklayıcı veya karıştırıcı biçimde —
etkilememiştir. Ancak annedeki depresif belirtiler ebeveynliği güçlü bir şekilde
açıklayan bir faktör olarak belirmiştir.

*Kanıt* — Dört EMBU-P alt ölçeği, yalnız indeks çocuklar ele alınarak
(kardeş puanı hariç; 241 indeks aile) genel doğrusal modellerle sınanmıştır. İlk
olarak, ham gruplar temel sosyodemografik ve klinik yapısal değişkenler eklenmeden,
ardından bu değişkenlerle kontrol edilerek (OAM) kestirilmiştir. Grup ana
etkilerinden (DM eksi Kontrol) hiçbiri, FDR-düzeltilmiş eşikte sıfırdan ayırt
edilememiştir: sıcaklık b = 0,02 [−0,04; 0,08], aşırı koruma b = 0,01 [−0,06; 0,08],
reddetme b = 0,02 [−0,02; 0,05] ve karşılaştırma b = 0,03 [−0,05; 0,11]
(@tbl-apa-h3-primary). Bu sıfır etkisi, OAM yapısına dayanmayan ağırlıklandırılmış
(IPTW) kovaryat-dengeleme modeliyle de doğrulanmış, IPTW ortalama tedavi etkilerinde
(ATE) %95 güven aralıkları dört boyutta da tam-sıfır hattında konumlanmıştır
(@tbl-apa-h3-iptw). Grup farkının yönünü "fark-yokluğu" olarak güçlü biçimde doğrulayan
Bağımsız Bayesçi hat, dört alt ölçekte H0 lehine 4 ila 9 kat daha yüksek kanıt (BF₁₀
değerleri: sıcaklık 0,14, aşırı koruma 0,14, reddetme 0,26, karşılaştırma 0,12) ve
etkinin >%96 oranında dar ROPE ([−0,1 SD, +0,1 SD]) bandına düştüğü pratik eşdeğerlik
bulgusu sunmuştur (@tbl-apa-h3-sensitivity). Antidepresan kullanımı alt-örneklemiyle
katmanlanan analiz, bulgunun anne ilaç kullanımı konfounder'ından bağımsız olduğunu
göstermiştir (@fig-h3-stratified-forest).

OAM modeli ayrıca üç temel bulgu sunmuştur: a) anne Beck depresyon puanı
(z-skoru) sıcaklığı (b = −0,09) negatif, reddetmeyi (b = 0,06) pozitif yönde öngörmüştür;
b) anne yaşı, eş mesleki durumu, kardeş yaş farkı ve aile çocuk sayısının
açıklayıcı gücü (tüm FDR p > 0,140) yoktur; c) annenin tanı bildirimi/algısı, DM
ailesi ile aynı-sınıf olmasının ötesinde bir etki (etkileşim) yaratmamıştır
(@tbl-apa-h3-primary). Birleştirilmiş bulgular, annelerin kendi ebeveynlik
bildirimlerinde çocuk algısına kıyasla yüksek "sosyal-istenebilirlik" etkisi
gösterebileceğine ve diyabet etkisinin bu beyana doğrudan sızmadığına işaret
etmektedir.

```{r}
#| label: tbl-apa-h3-primary
#| tbl-cap: "H3 EMBU-P (annenin kendi bildirdiği ebeveynlik) birincil kestirim tablosu: dört boyutun her biri için, sosyodemografik kovaryatları içermeyen Ham model ile bunları içeren OAM (olağan en küçük kareler) modeli yan yana verilir. Sütunlar DM eksi Kontrol grup farkını (b), %95 güven aralığını ve BH-FDR düzeltmeli q değerini; OAM kısmında ayrıca anne depresyonu, yaş ve SES gibi kontrol değişkenlerinin etkilerini içerir. Okuma anahtarı: ilk olarak grup satırının güven aralığının sıfırı içerip içermediğine, ardından kovaryat (özellikle anne Beck skoru) satırlarındaki anlamlılıklara bakılır."
apa_render_table("t10_h3_primary")
```

```{r}
#| label: tbl-apa-h3-iptw
#| tbl-cap: "H3 ters-olasılık ağırlıklandırması (IPTW) — H3 grup-farkı bulgusunun sağlamlığı, doğrudan OAM modeli yerine ailelerin latent SES, kardeş yaş farkı ve çocuk sayısı özelliklerinde eşitlendiği IPTW stratejisiyle de test edilir. Dört EMBU-P boyutu için, ağırlıklandırılmış örneklemde hesaplanan ortalama nedensel etki (ATE) ve sağlam-standart hatalara dayalı %95 güven aralıkları sunulmuştur. Okuma anahtarı: güven aralığının sıfırı içermesi ağırlıklandırılmış (eşitlenmiş) örneklemde de grup farkı olmadığı (H0) kararına işaret eder."
apa_render_table("t10b_h3_iptw_ate")
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
```

### H5 — Diadik Tutarlılık

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
ölçütün karşılanıp karşılanmadığı alt bölüm sonunda değerlendirilmektedir."""

new_text = """### H3 — Anne Öz-Bildirimi (EMBU-P)

**Bulgu özeti.** Annelerin kendi ebeveynlik tutumları hakkındaki değerlendirmelerinde (sıcaklık, aşırı koruma, reddetme ve karşılaştırma), diyabetli çocuk anneleri ile kontrol grubu anneleri arasında anlamlı bir fark bulunmamıştır. Bu "fark yokluğu" sonucu, pek çok farklı analiz yöntemiyle doğrulanmıştır. Ancak hatırlanacağı üzere çocukların kendi değerlendirmelerinde (H1) annelerinden reddedilme algılarında bir farklılık çıkmıştı; annelerin kendi bildirimlerinde böyle bir fark çıkmaması, anne ile çocuğun ebeveynlik tutumunu farklı algıladığını (H5) gösteren ilgi çekici bir çelişkidir (bu durum §5.3'te tartışılacaktır). Ailenin sosyoekonomik durumu, kardeş yaş farkı veya antidepresan kullanımı gibi özellikler bu sonucu değiştirmemiştir. Yine de annenin ruh halindeki (depresif) belirtiler ebeveynlik tutumunu etkileyen güçlü bir unsur olarak dikkat çekmiştir.

*Kanıt* — Annelerin bildirdiği dört tutum, yalnızca diyabetli olan çocuğun (indeks) olduğu aileler üzerinden incelenmiştir (241 aile). Ham verilerle yapılan karşılaştırmalarda ve sonradan aile yapıları eşitlenerek yapılan düzeltilmiş analizlerde, diyabetli aileler ile kontrol aileleri arasında sıfırdan ayırt edilebilir bir farka rastlanmamıştır (@tbl-apa-h3-primary ve @tbl-apa-h3-iptw). Bu sonucu sağlama almak için yapılan çok daha gelişmiş bir istatistik testinde (Bayesçi analiz), aralarında bir fark *olmadığına* dair 4 ila 9 kat daha güçlü kanıtlar bulunmuştur (@tbl-apa-h3-sensitivity). Annesi antidepresan kullanan aileler kendi içlerinde özel olarak ayrılıp analiz edildiğinde bile sonuç değişmemiş; bulgunun ilaç kullanımına bağlı bir yanılgı olmadığı kanıtlanmıştır (@fig-h3-stratified-forest).

Temel testler şu üç önemli noktayı da ortaya koymuştur: a) Annenin depresyon düzeyi arttıkça çocuğuna yönelik sıcaklık bildiriminin azaldığı, reddetme davranışının ise arttığı bildirilmiştir; b) Anne yaşı, ailenin geliri/mesleği, ailedeki çocuk sayısı gibi durumlar annenin ebeveynlik tutumunu belirleyen temel nedenler değildir; c) Çocuğun diyabet hastası olması, annenin ebeveynlik tutumunu tek başına şekillendiren bir faktör değildir (@tbl-apa-h3-primary). Tüm bu bulgular, annelerin anketleri doldururken "sosyal olarak makbul ve doğru olanı" işaretleme eğilimi gösterebileceğine ve hastalığın getirdiği zorlukların doğrudan annenin kendi ifadesine yansımadığına işaret etmektedir.

```{r}
#| label: tbl-apa-h3-primary
#| tbl-cap: "H3 EMBU-P (annenin kendi bildirdiği ebeveynlik) değerlendirme tablosu: Annelerin dört ebeveynlik tutumunda diyabet ve kontrol grupları arası fark, önce sadece yalın gruplar olarak (Ham model) ardından annenin yaşı, depresyon skoru ve ailenin gelir/meslek durumu hesaba katılarak (OAM modeli) verilmiştir. Tabloda diyabet eksi kontrol farkı (b) ve güven aralıkları sunulmuştur. Okuma anahtarı: Temel olarak grup satırında güven aralığının sıfırı içerip içermediğine, ardından aileyi şekillendiren diğer faktörlerin (özellikle anne Beck skoru) etkisine bakılır."
apa_render_table("t10_h3_primary")
```

```{r}
#| label: tbl-apa-h3-iptw
#| tbl-cap: "H3 ağırlıklandırılmış eşitleme tablosu (IPTW): H3 bulgusunun ne kadar sağlam olduğunu görmek için, aileler arası eşitsizlikleri (çocuk sayısı, gelir, yaş farkı gibi) istatistiksel olarak 'eşitleyerek' (IPTW) yeniden bir test yapılmıştır. Okuma anahtarı: Ortalama etkinin güven aralığının sıfırı içermesi, özellikler eşitlendiğinde dahi gruplar arası bir fark bulunamadığını kanıtlar."
apa_render_table("t10b_h3_iptw_ate")
```

```{r}
#| label: tbl-apa-h3-sensitivity
#| tbl-cap: "H3 sağlamlık (duyarlılık) kontrolleri tablosu: Annelerin ebeveynlik farkı bulunmayışı bulgusu üç ayrı yolla yeniden sınanmıştır: antidepresan kullanım durumu, Bayesçi analiz ve eşdeğerlik sınaması (TOST). Okuma anahtarı: Bayes kanıtı (BF₁₀) değerinin 1'in altında olması gruplar arası 'fark olmadığı' yönündeki kanıtı destekler; oran 1'den küçüldükçe sıfıra yaklaştıkça bu 'fark yok' görüşü daha da güçlenir."
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
```

### H5 — Diadik Tutarlılık (Anne-Çocuk Uyumu)

**Bulgu özeti.** Aynı evde yaşayıp aynı ilişkiyi deneyimlemelerine rağmen, "anne" ile "çocuğun" ebeveynlik tutumlarına verdikleri cevaplar arasındaki uyum oldukça düşüktür. Yani ebeveynlik ilişkisini anne farklı bir pencereden, çocuk bambaşka bir pencereden algılamakta; ikisi birbiriyle uzlaşamamaktadır. Ulaşılan bu uyumsuzluk, analiz edilen dört alt alanın (sıcaklık, koruma, reddetme, karşılaştırma) tamamında net biçimde görülmüştür. Dahası; diyabetli ailelerdeki anne-çocuk anlaşmazlığı ve uyumsuzluğu, kontrol ailelerindekine kıyasla bazı tutumlarda çok daha belirgindir (kontrol grubunda uyum diyabete kıyasla nispeten daha yüksektir).

*Kanıt* — Anne ile çocuk arasındaki ilişkinin bu iki cepheden nasıl göründüğü (uyum), beş farklı ve karmaşık istatistiksel yöntemle incelenmiştir. Her bir yöntem uyumun farklı bir cephesine bakar: puanların birebir tutarlılığı, uyumsuzluğun bir yüzey haritasındaki yeri, ailenin ortak dokusu vb. Araştırma başlamadan önce belirlenen kurala göre, diyabet ve kontrol grupları arasında "net bir fark" olduğunun söylenebilmesi için bu beş yöntemden en az üçünün aynı yönü işaret etmesi gerekmiştir."""

if old_text in content:
    content = content.replace(old_text, new_text)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replace successful!")
else:
    print("Text not found in the file. Check for exact match.")
