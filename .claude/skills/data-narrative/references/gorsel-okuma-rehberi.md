# Görsel/Öğe Okuma Rehberi — Öğe Tipini Tanı, Doğru Hamleyle Aç

Bir tabloyu, bir orman grafiğini, bir nedensel diyagramı ve bir yanıt yüzeyini
**aynı** kalıpla açıklamak, okura yanlış okumayı öğretir. Her öğe ailesinin kendi
geometrisi vardır: eksenler ne, işaretler ne, **gözün önce nereye bakması gerekir**,
ve o ailede en sık yapılan **okuma hatası** nedir.

Bu dosya, açıklamaya başlamadan önce yapılacak **"öğe tipini tanı → okuma hamlesini
uygula"** adımının kaynağıdır. Zengin bir altyazı bu hamleyi bazen kendiliğinden
verir; ama açıklama bu rehbere dayanmalı, altyazının cömertliğine değil. Altyazı
inceyse (ör. yalnız "yanıt yüzeyi; kesikli çizgi uyum hattı") okuma hamlesini
**buradan** getir.

## Kullanım

1. Öğenin hangi aileye girdiğini belirle (aşağıdaki tablo).
2. O ailenin **"önce şuna bak"** hamlesini açıklamanın ilk kanıt cümlesi yap.
3. O ailenin **tipik yanılgısını** kavram-yanılgısı kapısında (SKILL.md) önle.
4. Aile listede yoksa, en sondaki **genel yöntemi** uygula.

---

## Şekil aileleri (bu tezdeki gerçek karşılıklarıyla)

### Orman grafiği (forest) — ör. `@fig-h1-forest`, `@fig-h3-stratified-forest`
- **Ne:** nokta = tahmin; yatay çizgi = %95 güven aralığı; dikey referans çizgisi =
  sıfır fark (ya da OR/RR'de 1).
- **Önce şuna bak:** güven aralığı **referans çizgisini kesiyor mu?** Kesiyorsa etki
  sıfırdan ayırt edilemiyor; kesmiyorsa yön belirginleşiyor. Çizginin **genişliği** =
  kesinlik (dar = kesin).
- **Tipik yanılgı:** "nokta sıfırdan uzak = güçlü etki" sanmak. Uzaklık büyüklüktür,
  ayırt edilebilirlik değil; ikisini ayrı söyle.

### Yol / SEM diyagramı (APIM dâhil) — ör. `@fig-h2-apim-path`
- **Ne:** kutular = gözlenen değişken, elipsler = gizil (latent) değişken; **tek yönlü
  ok** = yönlü etki (aktör = kendi geçmişi→kendi çıktısı; partner = eşin→kendi çıktısı),
  **çift yönlü ok/eğri** = kovaryans (ortak değişim, yön iddiası yok); sayılar
  standardize yükleme/katsayı.
- **Önce şuna bak:** hangi oklar **aktör**, hangileri **partner**? Diadik modelde asıl
  soru budur. Sonra katsayı işaretine ve büyüklüğüne bak.
- **Tipik yanılgı:** çift yönlü eğriyi "etki" sanmak; o yalnız birlikte-değişimdir.

### Nedensel yönlü asiklik graf (DAG) — ör. `@fig-causal-dag`
- **Ne:** düğüm = değişken; ok = **"şu şunu etkiler" varsayımı** (veriden kestirilmez,
  analizden **önce** çizilir); **ok yokluğu** da bir varsayımdır (güçlü bir iddia).
  Seçilim düğümü ($S$) üzerinde koşullanma tanımlanabilirliği bozabilir.
- **Önce şuna bak:** hangi düğümler **arka-kapı karıştırıcısı** (kapatılacak), hangileri
  **aracı** (bilerek açık bırakılan), hangisi **seçilim** düğümü? Sonra: bu tasarımda
  etki **tanımlanabilir mi**?
- **Tipik yanılgı:** DAG'ı "veri sonucu" sanmak. DAG bir varsayım haritasıdır; en değerli
  çıktısı çoğu zaman **hangi etkinin üretilemeyeceğini** dürüstçe göstermesidir.
- Ayrıntılı üslup örneği: `references/ornek-sekil-dag.md`.

### Kovaryat denge / Love grafiği (SMD) — ör. `@fig-smd-love`
- **Ne:** her satır bir kovaryat; x = mutlak standardize ortalama fark |SMD|; renk =
  aşama (ağırlık öncesi / IPTW / eşleştirme); kesikli çizgiler = 0,10 ve 0,25 eşikleri.
- **Önce şuna bak:** noktalar ağırlıktan **sonra** sıfıra yaklaştı mı? Öncesi/sonrası
  kıyası bu grafiğin bütün mesajıdır. Eşik yorumu: `references/buyukluk-esikleri.md`.
- **Tipik yanılgı:** tek bir dengesiz kovaryattan "denge başarısız" sonucu çıkarmak;
  bütün örüntüye ve eşiğe bak.

### Eğilim skoru örtüşme (yoğunluk) — ör. `@fig-propensity-overlap`
- **Ne:** iki grubun eğilim skoru dağılımları; çakışan alan = **ortak destek**.
- **Önce şuna bak:** dağılımlar **çakışıyor mu**? Çakışmayan uçlar karşılaştırılamaz
  bölgedir.
- **Tipik yanılgı:** örtüşmeyi "denge" sanmak; örtüşme karşılaştırılabilirliğin ön
  koşuludur, dengenin kendisi değil (dengeyi Love grafiği gösterir).

### Bland–Altman uyum haritası — ör. `@fig-h5-bland-altman`
- **Ne:** x = iki ölçümün ortalaması; y = **farkları**; orta çizgi = ortalama sapma
  (bias); üst/alt çizgiler = uyum sınırları (±1,96 SS).
- **Önce şuna bak:** noktalar sıfır fark çizgisinin etrafında **ne kadar dağınık** ve
  uyum sınırları **ne kadar geniş**? Geniş = düşük uyum.
- **Tipik yanılgı:** "yüksek korelasyon = yüksek uyum" sanmak. Korelasyon sıralamayı,
  Bland–Altman **mutlak uyumu** ölçer; iki taraf sistematik kayabilir ama korelasyon
  yine yüksek çıkar.

### Yanıt yüzeyi (RSA) — ör. `@fig-h5-rsa-surface`
- **Ne:** 3B yüzey; iki yatay eksen iki bildiricinin algısı; dikey eksen sonuç; noktalı
  çizgi = **uyum hattı** (iki algının eşit olduğu doğru, x=y).
- **Önce şuna bak:** uyum hattı **boyunca** yüzey nasıl davranıyor, uyumsuzluk (hattan
  sapma) yönünde nasıl? Fark skorunun gizlediği örüntü buradadır.
- **Tipik yanılgı:** yüzeyi basit "fark = kötü" gibi okumak; asimetri (kim daha yüksek)
  önemli olabilir.

### Ağ grafiği (Gauss grafik modeli, GGM) — ör. `@fig-network-graph`
- **Ne:** düğüm = değişken; kenar = **kısmi korelasyon** (diğer tüm değişkenler
  sabitken kalan ilişki); kenar kalınlığı = güç; düğüm boyutu = merkeziyet (strength).
- **Önce şuna bak:** hangi düğümler **en kalın kenarlarla** bağlı ve hangileri
  merkezî? Kenar **yokluğu** koşullu bağımsızlık iddiasıdır.
- **Tipik yanılgı:** kenarı nedensel ok sanmak; GGM yönsüzdür ve keşifseldir.

### ROC eğrisi — ör. `@fig-clinical-roc`
- **Ne:** x = 1−özgüllük (yanlış alarm); y = duyarlılık (yakalama); köşegen = şans;
  AUC = eğri altı alan.
- **Önce şuna bak:** eğri sol-üst köşeye **ne kadar yakın**? AUC yorumu:
  `references/buyukluk-esikleri.md`.
- **Tipik yanılgı:** görünür (apparent) AUC'yi nihai performans sanmak; iç-örneklem
  AUC iyimserdir, optimizm-düzeltilmiş değeri iste.

### Karar eğrisi (DCA) — ör. `@fig-clinical-dca`
- **Ne:** x = eşik olasılık; y = **net fayda**; kıyas çizgileri = "herkesi tara" ve
  "kimseyi tarama".
- **Önce şuna bak:** model eğrisi, iki kıyas stratejisinin **üstünde** hangi eşik
  aralığında kalıyor? Klinik değer buradadır.
- **Tipik yanılgı:** net faydayı doğruluk sanmak; DCA fayda-zarar dengesini eşiğe göre
  tartar.

### Kalibrasyon grafiği — ör. `@fig-clinical-calibration`
- **Ne:** x = tahmin edilen olasılık; y = gözlenen oran; köşegen = kusursuz kalibrasyon.
- **Önce şuna bak:** noktalar köşegen **üstünde mi**? Sapma, tahminlerin sistematik
  yüksek/düşük olduğunu gösterir.
- **Tipik yanılgı:** görünür kalibrasyonu nihai sanmak; optimizm-düzeltilmiş eğim/sabit
  ayrı raporlanır.

### Spesifikasyon eğrisi (çoklu-evren) — ör. `@fig-specification-curve`, `@fig-p2-h1-spec`
- **Ne:** her nokta bir **analiz spesifikasyonu** (kovaryat/yöntem/alt örneklem seçimi);
  büyüklüğe göre sıralı; renk = nominal anlamlılık.
- **Önce şuna bak:** etki **spesifikasyonlar boyunca** yönünü/işaretini koruyor mu?
  Sağlamlık budur.
- **Tipik yanılgı:** eğriyi tek bir test gibi okumak; bu bir **dağılım**tır, tek p
  değeri değil. Paneller ayrı estimand'sa birleştirme.

### Duyarlılık konturu (sensemakr) — ör. `@fig-sensemakr-contour`
- **Ne:** eksenler ölçülmemiş bir karıştırıcının maruziyet ve sonuçla kısmî R²'si;
  konturlar bulguyu silmek için gereken karıştırıcı gücü; RV = sağlamlık değeri.
- **Önce şuna bak:** bulguyu sıfırlamak için karıştırıcının **ne kadar güçlü** olması
  gerekir? Yüksek eşik = sağlam bulgu.
- **Tipik yanılgı:** "treatment" eksenini müdahale sanmak; gözlemsel tasarımda grup/
  maruziyet göstergesidir.

### Isı haritası (korelasyon vb.) — ör. `@fig-ses-correlation`, `@fig-p2-dca-heatmap`
- **Ne:** renk = değerin **işareti ve büyüklüğü**; hücre = değişken çifti/parametre
  hücresi.
- **Önce şuna bak:** en koyu (en güçlü) hücreler nerede ve **hangi yönde** (renk skalası)?
- **Tipik yanılgı:** renk yoğunluğunu anlamlılık sanmak; yoğunluk büyüklüktür.

### Akış diyagramı (STROBE) — ör. `@fig-strobe-flow`
- **Ne:** kutular = aşamalar; oklar = geçiş; sayılar = her aşamadaki n ve kayıp/dışlama.
- **Önce şuna bak:** nerede, **neden**, kaç birim düştü? Seçilimin somut karşılığı budur.

### Faktör yükleme mimarisi (CFA/trifaktör) — ör. `@fig-p2-trifactor`
- **Ne:** madde→faktör yüklemeleri (ortak özellik/trait vs yöntem/bildiren bileşenleri).
- **Önce şuna bak:** maddeler ortak özelliğe mi yoksa yönteme mi daha çok yükleniyor?
  (bu **uyum indeksi değil**, yapı mimarisidir.)

### IRT yetenek (θ) — ör. `@fig-p2-floor-irt`
- **Ne:** gizil yetenek θ dağılımı / grup farkları; taban etkisine duyarlı kestirim.
- **Önce şuna bak:** dağılımlar **tabanda mı yığılmış**? Taban etkisi θ farkını
  bozabilir.

### LPA/LCA model seçim tanıları — ör. `@fig-lpa-fit-indices`
- **Ne:** profil sayısına göre BIC, entropi, BLRT p; model seçimi tanıları.
- **Önce şuna bak:** BIC minimumu nerede, **ama** parsimoni kuralı (ΔBIC≤2) ve
  yorumlanabilirlik ne diyor? Sayısal minimum tek başına seçim değildir.
- **Tipik yanılgı:** en düşük BIC'i mutlak kazanan sanmak; seçim kuralı tutarlılığı
  (AGENTS.md) tablo↔metin aynı profil sayısını göstermeli.

---

## Tablo aileleri

- **Betimsel/Tablo 1 (örneklem özellikleri):** her satır bir değişken; gruplara göre
  ortalama/SS veya n/%; genelde bir denge/fark sütunu (SMD). **Önce:** hangi satırlar
  gruplar arası **dengesiz** (SMD eşiği)?
- **Hipotez sonuç tablosu (β/OR/GA/p):** **önce yön ve GA'nın sıfırı içerip
  içermediği**, sonra büyüklük (`references/buyukluk-esikleri.md`), en son p.
- **Uyum indeksi tablosu (CFI/TLI/RMSEA/SRMR):** tek indekse bakma; **hepsini birlikte**
  oku, çelişkiyi açıkla (`references/ornek-sekil-dag.md` kardeşi: benchmark örneği
  `buyukluk-esikleri.md` sonundadır).
- **Bayesçi tablo (BF₁₀/pd/ROPE/GüvenilirAralık):** BF₁₀ etiketini Jeffreys ölçeğiyle,
  BF₁₀<1'i **H0 lehine** oku (`buyukluk-esikleri.md`).

---

## Genel yöntem (listede olmayan öğe)

1. **Eksenleri/işaretleri adlandır:** her eksen ne, her işaret (nokta/çizgi/renk/kalınlık)
   neyi kodluyor? Referans/eşik çizgisi var mı, ne demek?
2. **Tek "önce şuna bak" hamlesi belirle:** okur gözünü ilk nereye koymalı, o hareket
   neyi ortaya çıkarır?
3. **Yönü büyüklükten, büyüklüğü ayırt-edilebilirlikten ayır.**
4. **O öğede en olası yanlış okumayı** açıkça önle (kavram-yanılgısı kapısı).
5. Emin değilsen üreten R modülünü/CSV'yi izle (`references/kaynak-dogrulama.md`);
   uydurma.
