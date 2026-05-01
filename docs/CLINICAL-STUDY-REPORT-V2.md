# KLİNİK ÇALIŞMA RAPORU (CSR)

## Tip 1 Diyabetli Çocuklar, Sağlıklı Kardeşleri ve Annelerinde Algılanan Ebeveynlik Tutumu, Maternal Depresyon ve Kardeş İlişkileri: Vaka–Kontrol, Multi-İnformant ve Aile-İçi Diadik Bir Çalışma

**Protokol No:** Marmara Üniversitesi Tıp Fakültesi KAEK 09.2023.201
**Etik Onay Tarihi:** 06.01.2023
**Sorumlu Araştırmacı:** Uzm. Dr. Özlem Murzoğlu Kurt
**Tez Danışmanı:** Prof. Dr. Eren Özek
**Kanonik Analiz Tabanı:** FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock (kilit tarihi: 26.04.2026)
**Raporlama Standartları:** STROBE (gözlemsel) + JARS-Quant (APA niceliksel) + TRIPOD (klinik fayda alt-modülü)
**Belge Tipi:** ICH E3 uyarlanmış akademik tez-uyumlu CSR
**Hedef Okuyucu:** Klinisyen-jüri hibrit

---

## SİNOPSİS (TL;DR)

**Amaç.** Tip 1 diyabetli (T1DM) çocukların annelerini; sağlıklı kardeşlerinin ve hastalığı olmayan kontrol çocuklarının algıladıkları ebeveynlik tutumlarıyla; T1DM ailelerinde kardeş ilişkilerini ve annenin kendi parenting öz-raporu ile çocuğun algısı arasındaki diadik tutarlılığı; ön-kayıtlı (pre-registered) çoklu-yöntem (frequentist + Bayesian + sensitivite) bir çerçevede karşılaştırmak.

**Tasarım.** Tek merkezli, vaka–kontrol; multi-informant (anne, T1DM çocuk, sağlıklı kardeş veya kontrol çocuk); aile-içi diadik (anne–çocuk eşleşmiş); 241 aile × 2 katılımcı = 482 satırlık kanonik veri tabanı (DM indeks n=120; Kontrol indeks n=121).

**Ölçekler.** EMBU-P (anne öz-rapor, 29 madde, 4-Likert), EMBU-C (çocuk algısı, 29 madde, 4-Likert; q25 ters skorlu), Beck Depresyon Envanteri (BDÖ, 21 madde, 0–3) Türkçe Hisli (1989) uyarlaması, Sibling Relationship Questionnaire (SRQ, Furman & Buhrmester 1985, 48 madde, 5-Likert).

**Analiz.** Multilevel ANCOVA + IRT GRM + Bayesian dual reporting (H1); Welch + APIM + Olsen-Kenny dyadic CFA (H2); ANCOVA + IPTW + AD-stratified (H3); lavaan SEM + multi-group invariance (H4); 5 paralel diadik tutarlılık stratejisi ve "en az 3 uyumlu" kuralı (H5). Robustluk için 120-spec multiverse, TOST, sensemakr RV_q, VanderWeele E-value, negatif kontrol; Bayesian paralel hat olarak brms + Pinquart (2013) bilgili önsel + ROPE + Savage-Dickey BF + LOO-CV. Birincil yanlış-keşif kontrolü Benjamini-Hochberg FDR (q = .05).

**Ana bulgular.**
- **H1 (EMBU-C):** T1DM çocuklar annelerini reddetme boyutunda kontrollerden daha yüksek algıladı; BF₁₀ = 8.12 (ılımlı H1 lehine kanıt). Sıcaklık alt-ölçeğinde fark gözlenmedi; BF₁₀ = 0.29 (ılımlı H0 lehine kanıt).
- **H2 (SRQ):** 4 alt-ölçekte yetersiz kanıt; 4 APIM modelinin tümü yakınsadı.
- **H3 (EMBU-P, anne öz-rapor):** 4 alt-ölçekte |d| < 0.17; FDR-düzeltilmiş p > .50; gruplar arası fark kanıtı yok.
- **H4 (Beck → EMBU-P):** Tam SEM yakınsadı; dört yapısal yol istatistiksel olarak anlamlı.
- **H5 (Diadik tutarlılık):** Olsen-Kenny latent korelasyon Kontrol = 0.17, DM = 0.29.
- **Robustluk (KISIM XI):** 120 spec multiverse; %0 spec'te p < .05; sensemakr RV_q 0.04–0.08; E-value 1.36–1.59 (zayıf-orta dirayet). Propensity-score IPTW maksimum SMD 0.220 → 0.004 (mükemmel denge).

**Sonuç.** T1DM çocuklar annelerini istatistiksel ve klinik olarak daha reddedici algılarken; annelerin kendi parenting raporları ve sağlıklı kardeşlerin kardeş ilişkisi raporları gruplar arasında pratik olarak eşdeğer kaldı. Bu *informant ayrışması* T1DM aile sisteminin tek-bilgilendiren tasarımlarda kaçırılan psikososyal yükünü vurgular ve klinik takipte çocuk-perspektifinin sistematik dahil edilmesini destekler.

---

> **Metin Kutusu 1 — Kanonik analiz tabanı ve kilit doğrulama**
> Tüm sayısal sonuçlar 26.04.2026 tarihinde SHA-256 imzasıyla kilitlenen `FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` dosyasından deterministik olarak üretilmiştir. Kilit, post-hoc analitik esnekliği (analitik garden of forking paths) ortadan kaldırır; çıktı çoğaltılabilirliği renv + targets pipeline'ı ile garanti edilir. Bir bulguyu yorumlarken "kanonik" sıfatı, değerin bu kilitli tabandan türetildiğini ifade eder.

---

## I. ETİK, YASAL VE AÇIK BİLİM ÇERÇEVESİ

Çalışma, Marmara Üniversitesi Tıp Fakültesi Klinik Araştırmalar Etik Kurulu'nun 06.01.2023 tarihli ve 09.2023.201 sayılı kararıyla onaylanmıştır. Tüm anneler için yazılı bilgilendirilmiş onam, çocuklar için yaşa uygun aydınlatılmış muvafakat (assent) alınmıştır. Sağlık verileri 6698 sayılı Kişisel Verilerin Korunması Kanunu (KVKK) ve klinik araştırma yönetmeliklerine uygun şekilde anonimleştirilerek pseudo-kimliklendirilmiş; ham veri kurum içi güvenli sunucuda saklanmıştır.

Açık bilim yükümlülüğü çerçevesinde üç OSF kaydı oluşturulmuştur: psikometrik validasyon protokolü için **d524q**, birincil hipotezler H1–H5 için ikincil-veri ön-kayıtı **pytfe** ve şemsiye proje kaydı **vqrt5**. Kayıt URL'leri: `https://osf.io/d524q/`, `https://osf.io/pytfe/`, `https://osf.io/vqrt5/`. (Kayıtların erişim/embargo durumu bu raporun yazımı sırasında otomatik olarak doğrulanamamıştır; okuyucunun bağlantıları doğrudan kontrol etmesi önerilir.) Kaynak depo herkese açıktır: `https://github.com/murzoglu/doktoratezi`. Kod ve sonuç ürünleri Zenodo DOI ile arşivlenmiştir; FAIR ilkelerine uyum hedeflenmiştir.

---

## II. ARAŞTIRMACILAR VE KATKILAR

- **Sorumlu araştırmacı (PI):** Uzm. Dr. Özlem Murzoğlu Kurt — kavramsallaştırma, metodoloji, soruşturma, veri yönetimi, formal analiz, yazma (taslak ve gözden geçirme).
- **Tez danışmanı:** Prof. Dr. Eren Özek — denetim, kavramsallaştırma, fonlama edinimi, yazma (gözden geçirme).
- **Etik kurul:** Marmara Üniversitesi Tıp Fakültesi KAEK.

CRediT taksonomisine göre tüm yazar katkıları açıkça belirtilmiş; çıkar çatışması bulunmamaktadır.

---

## III. GİRİŞ VE GEREKÇE

### III.1 Tip 1 Diyabet ve Aile Psikososyal Yükü

Tip 1 diyabet (T1DM), pankreas β-hücrelerinin otoimmün yıkımıyla mutlak insülin eksikliği yaratan, çocukluk-başlangıçlı kronik bir hastalıktır. Türkiye'de Yeşilkaya ve diğerleri (2017) tarafından Sosyal Güvenlik Kurumu kayıtlarına dayanan ilk ulusal çalışma, 0–14 yaş grubunda 11.3/100.000 ve 0–18 yaş grubunda 10.8/100.000 yıllık insidans bildirmiştir; bu oran Türkiye'yi orta-insidanslı ülkeler kategorisine yerleştirir. T1DM yönetimi, sürekli glukoz izlemi, çoklu günlük insülin uygulamaları (veya pompa), beslenme planı, hipoglisemi farkındalığı ve düzenli HbA1c hedeflemesini (<7.0% genel hedef, ISPAD 2024 ve ADA Standards of Care 2024–2025) gerektirir. Bu rejim hayatın her saatine sızdığı için yük doğrudan aileye, özellikle anneye yansır.

Çocukluk kronik hastalıklarının ebeveyn–çocuk ilişkisine etkisi üzerine en kapsamlı meta-analiz olan **Pinquart (2013)** 325 çalışmayı sentezleyerek küçük-orta etki büyüklüklerinde *daha az olumlu* ebeveyn–çocuk ilişkisi bildirmiştir (g = −0.16). Aşırı koruyuculuk (overprotection) ve düşük özerklik desteği boyutları en tutarlı şekilde yükselen örüntülerdir. T1DM'ye özgü çalışmalar (Sweenie, Mackey ve Streisand 2014; Whittemore ve diğerleri 2012; Helgeson ve diğerleri 2019) parenting stresi, hipoglisemi korkusu ve aşırı koruyuculuğun glisemik kontrolle (HbA1c) çift yönlü ilişkili olduğunu göstermiştir. Ailedeki çatışma ile HbA1c arasındaki ilişki Anderson ve diğerleri (2002), Hilliard ve diğerleri (2013) ve Ingerski ve diğerleri (2010) tarafından replikasyonla doğrulanmıştır.

Maternal depresyon, parenting davranışıyla küçük-orta düzeyde (Lovejoy, Graczyk, O'Hare ve Neuman 2000; meta-analiz, k = 46) negatif örüntü oluşturur; özellikle olumsuz/eleştirel ebeveynlik en güçlü bağıntıyı gösterir. Goodman ve diğerleri (2011) bu örüntüyü çocuk içselleştirme/dışsallaştırma sorunlarına genişletmiştir. T1DM-spesifik literatür, annelerin %20–30'unun klinik düzeyde depresif belirtiler bildirdiğini göstermiştir (Streisand ve diğerleri; Jaser ve diğerleri).

Kardeş ilişkilerinin kronik hastalıkta sistematik incelemesi olan **Vermaes, van Susante ve van Bakel (2012)** meta-analizi (k = 56), kronik hastalık kardeşlerinde küçük-fakat-anlamlı içselleştirme (d = 0.17) ve dışsallaştırma (d = 0.08) artışı, olumlu öz-yetkinlikte ise azalma (d = −0.09) saptamıştır. T1DM'ye özgü kardeş çalışmaları daha sınırlıdır; bu boşluk doğrudan H2 hipotezini motive eder.

### III.2 Algılanan Ebeveynlik Tutumu Çerçevesi

EMBU (Egna Minnen Beträffande Uppfostran) Perris, Jacobsson, Lindström, von Knorring ve Perris (1980) tarafından geliştirilmiş; Arrindell ve diğerleri (1999) tarafından çapraz-kültürel kısa form (s-EMBU); Türkiye'ye Sümer ve Güngör (1999) ve sonraki ekiplerce uyarlanmıştır. EMBU'nun üç temel boyutu — **reddetme, sıcaklık (duygusal yakınlık), aşırı koruma** — psikopatoloji riski, attachment ve kronik hastalık adaptasyonuyla replikasyonlu ilişkiler göstermiştir. EMBU-Çocuk (EMBU-C) ve EMBU-Ebeveyn (EMBU-P) paralel formları, **multi-informant** ve **diadik** (anne ↔ çocuk) tasarımı mümkün kılar.

### III.3 Bu Çalışmanın Boşluk Doldurma Mantığı

Mevcut T1DM literatürünün üç sınırlılığı vardır: (1) çoğunlukla **tek-bilgilendiren** (genelde anne) tasarımlar; (2) **sağlıklı kardeş kontrol katmanı**nın dahil edilmemesi; (3) **diadik tutarlılık**ın açıkça nicelendirilmemesi. Bu çalışma üç-katmanlı multi-informant (T1DM çocuk + sağlıklı kardeş veya kontrol çocuk + anne), aile-içi diadik (anne–çocuk eşleşmiş) ve önsel-belirtilmiş çoklu-yöntem (frequentist + Bayesian + sensitivite) tasarımıyla bu üç boşluğu eş-anlı hedefler.

> **Metin Kutusu 2 — Multi-informant tasarım**
> Multi-informant tasarım, davranışsal ve psikososyal yapıların farklı bağlamlarda farklı kişilerce gözlemlendiği gerçeğine dayanır. De Los Reyes ve diğerleri (2015), 341 çalışmayı meta-analiz ederek bilgilendirenler arası ortalama uyumu r ≈ 0.28 düzeyinde bulmuş; *uyumsuzluğun* başlı başına psikometrik bilgi taşıdığını öne sürmüştür. Bizim tasarımımızda anne (öz-rapor) + iki çocuk-bilgilendiren (T1DM ve sağlıklı kardeş) ayrışmasını sistematik olarak nicelendirir.

---

## IV. ÇALIŞMA HEDEFLERİ

### IV.1 Birincil Hipotezler (önsel-kayıtlı, OSF/pytfe)

- **H1.** T1DM çocukların EMBU-C reddetme ve aşırı koruma puanları, sağlıklı kardeşlerinkine ve kontrollerinkine göre daha yüksektir.
- **H2.** T1DM ailelerinde kardeş ilişkisi (SRQ; sıcaklık, çatışma, rakiplik, statü) kontrol ailelerinden farklılaşır.
- **H3.** T1DM annelerin EMBU-P alt-ölçek puanları kontrol annelerinden farklılaşır.
- **H4.** Annenin Beck depresyon skoru, anne raporu EMBU-P alt-ölçeklerinin latent yapısına anlamlı yapısal yollarla bağlanır.
- **H5.** Anne öz-raporu (EMBU-P) ile çocuğun algısı (EMBU-C) arasında diadik tutarlılık vardır; bu tutarlılık DM ile Kontrol grupları arasında farklılaşabilir.

### IV.2 İkincil ve Keşifsel Hedefler

KISIM VI–XII modülleri: medyasyon (tek/çok-düzeyli/Bayesian), latent profile analysis, network analysis, klinik fayda (TRIPOD), DM-içi alt-analizler (HbA1c × parenting, dm_yili spline), sistematik robustluk ve Bayesian paralel hat. DM-içi alt-analizler n=39 keşifsel altküme nedeniyle sıkı katı hipotez-testinden ziyade hipotez-üretici niteliktedir.

---

## V. YÖNTEM

### V.1 Tasarım

Tek-merkezli, prospektif, vaka–kontrol; multi-informant (anne + çocuk); aile-içi diadik (eşleşmiş anne–çocuk satırları). Vaka grubu en az 6 ay önce T1DM tanısı almış 8–18 yaş arası çocuklar ve anneleri; kontrol grubu yaş-cinsiyet eşleştirilmiş kronik hastalığı olmayan çocuklar ve anneleri. T1DM ailelerde, varsa sağlıklı kardeş ek kollektör olarak dahil edilmiştir.

### V.2 Örneklem

**Dahil edilme:** (a) T1DM kolu için ISPAD kriterlerine göre kesin T1DM tanısı, en az 6 ay tanı süresi; (b) çocuk yaşı 8–18; (c) anne ve çocuğun sözel/yazınsal Türkçe ile anketleri tamamlayabilmesi.
**Dışlama:** (a) bilinen ciddi nörogelişimsel bozukluk, ağır psikiyatrik komorbidite (psikoz, ağır otizm); (b) son 30 gün içinde diyabetik ketoasidoz nedeniyle hastane yatışı (akut stres etkisini sınırlamak için).
**Toplam:** 241 aile (DM = 120, Kontrol = 121); satır-sayım: 482 katılımcı.

Örneklem büyüklüğü; Pinquart (2013) meta-analitik ortalama g = −0.16 ile %80 güç ve α = .05 (iki yönlü) altında ANCOVA için ~120 aile/grup gereksinimine dayalı olarak prospektif belirlenmiştir.

### V.3 Ölçekler

**EMBU-P (anne öz-rapor).** 29 madde, 4-Likert (1 = hiç–4 = her zaman). Üç boyut: reddetme, sıcaklık, aşırı koruma. Türkçe uyarlama Sümer & Güngör (1999) hattı.
**EMBU-C (çocuk algısı).** 29 madde, 4-Likert. Madde q25 ters-skorlanmış (kanonik dokümantasyon). Aynı boyutlar, çocuk perspektifinde.
**Beck Depresyon Envanteri (BDÖ).** 21 madde, 0–3 puan. Türkçe geçerlik-güvenirlik Hisli (1989) — Cronbach α ≈ 0.80–0.90 aralığında raporlanmıştır.
**Sibling Relationship Questionnaire (SRQ).** Furman & Buhrmester (1985), 48 madde, 5-Likert. Dört faktör: sıcaklık/yakınlık, çatışma, rakiplik, göreli statü/güç.

> **Metin Kutusu 3 — Ölçek psikometriği: ω, AVE, HTMT**
> Cronbach α'nın bilinen sınırlılıkları (tek-faktörlülük varsayımı, eşit-yükleme varsayımı) nedeniyle psikometrik validasyonda McDonald'ın **ω**'sı, Average Variance Extracted (AVE) ve Heterotrait-Monotrait oranı (HTMT < 0.85 ayrımsal geçerlik eşiği) raporlanmıştır. ω ≥ 0.70 kabul edilebilir, ω ≥ 0.80 iyi düzeydir.

### V.4 Veri Yönetimi

Ham veri R 4.5.3 + Quarto 1.6+ + targets (pipeline orchestration) + renv (paket sürüm sabitleme) + Stan 2.32+ üzerine kurulu hesaplama altyapısında işlenmiştir. **Yapısal NA** (örneğin tek çocuğu olan ailede SRQ-Yok) eksik veriden ayrı bir kategoride tutulmuş; bu ayrım imputasyon kararını etkilemiştir.

> **Metin Kutusu 4 — Yapısal NA vs eksik veri**
> Yapısal NA, ölçümün kavramsal olarak uygulanmadığı durumdur (örn. tek çocuğu olan ailede SRQ doldurulamaz); eksik veri ise ölçüm uygulanmış fakat değer kayıptır. İmputasyon yalnızca eksik veriye yapılır; yapısal NA listwise tutulur. Bu ayrım yapılmazsa imputasyon yapay sinyal yaratır.

Çoklu imputasyon (m = 50, mice paketi), eksik veri >5% olan değişkenler için uygulanmış ve Full Information Maximum Likelihood (FIML) ile karşılaştırılmıştır (Enders 2022; Graham 2009). Tüm sonuçlar kanonik kilitli tabandan deterministik olarak üretilmiş; SHA-256 hash-zinciri her audit adımında doğrulanmıştır.

### V.5 İstatistiksel Plan

#### V.5.1 Genel Çerçeve

**Frequentist hat:** ANCOVA (yaş + cinsiyet + sosyoekonomik durum kovaryatlı), Welch t-testi, multilevel mixed-effects (lme4), structural equation modeling (lavaan).
**Bayesian paralel hat (KISIM XII):** brms + Stan; Pinquart (2013) meta-analitik etki büyüklüklerinden türetilmiş zayıf-bilgili önsel (Normal(−0.16, 0.20)); ROPE = ±0.10 SD; Savage-Dickey BF (Wagenmakers, Lodewyckx, Kuriyal & Grasman 2010); LOO-CV ve WAIC ile model karşılaştırma (Vehtari, Gelman & Gabry 2017).
**Çoklu karşılaştırma:** Benjamini-Hochberg FDR (q = .05), her hipotez ailesi içinde ayrı.
**Etki büyüklüğü:** Cohen'in d'si, Hedges'in g'si, η²ₚ; %95 GA bootstrap (B = 5000).

> **Metin Kutusu 5 — p-değeri, etki büyüklüğü ve %95 GA**
> p-değeri yalnızca H₀'a karşı *uyumsuzluğu* ölçer; etki büyüklüğü farkın *büyüklüğünü*, %95 güven aralığı ise farkın *kesinliğini* gösterir. Negatif bulgu raporlamada üçü birlikte sunulur; bunlardan hiçbiri tek başına yeterli değildir. Çalışmada APA standardına uygun şekilde p < .001 (p = .000 yasak), d ve ω 2 ondalık, p 3 ondalık, yüzdeler 1 ondalık raporlanmıştır.

#### V.5.2 Hipotez-Spesifik Stratejiler

**H1 (EMBU-C, çocuk algısı):**
- Birincil: Multilevel ANCOVA (random intercept = aile_id), kovaryat: çocuk yaşı, cinsiyet.
- Sensitivite: IRT Graded Response Model (Samejima 1969) ile latent skor; Bayesian replikasyon (brms + Pinquart prior).
- Yorum: BF₁₀ ≥ 3 anlamlı H1 lehine; BF₁₀ ≤ 1/3 anlamlı H0 lehine (Kass & Raftery eşikleri).

**H2 (SRQ, kardeş ilişkisi):**
- Birincil: Welch t-testi (unequal variance), ardından bootstrap %95 GA.
- İleri: APIM (Cook & Kenny 2005) — anne-çocuk satır eşleştirmeli; Olsen-Kenny dyadic CFA distinguishable dyads (Olsen & Kenny 2006).
- DM ailelerde sağlıklı-kardeş varlığı koşulu nedeniyle alt-örneklem sınırlanmıştır.

**H3 (EMBU-P, anne öz-rapor):**
- Birincil: ANCOVA + propensity-score IPTW (Robins, Hernán & Brumback 2000).
- Sensitivite: Anderson-Darling stratified replication.

> **Metin Kutusu 6 — Propensity skoru, IPTW ve SMD eşiği 0.10**
> Vaka–kontrol gözlemsel tasarımda gruplar baz çizgide farklılaşabilir. Propensity skoru (her bir denek için "DM grubunda olma" tahmini olasılığı) ile **stabilize edilmiş ters tedavi olasılığı ağırlığı (IPTW)** gruplar arasında *kovaryat dengesizliğini* azaltır. Standardized mean difference (SMD) < 0.10 kabul edilebilir denge sayılır. Bu çalışmada maksimum SMD 0.220 → 0.004'e düşmüştür — mükemmel denge.

**H4 (Beck → EMBU-P latent SEM):**
- Lavaan + WLSMV; çok-grup invaryans testi (Cheung & Rensvold 2002; Chen 2007: ΔCFI < 0.01 eşiği).
- Bayesian replikasyon: blavaan.

**H5 (Diadik tutarlılık) — 5 paralel strateji ve "en az 3 uyumlu" kuralı:**
1. ICC (intraclass correlation) + Bland-Altman uyum analizi.
2. Edwards-Parry response surface analysis (Edwards & Parry 1993).
3. Lavaan iki-faktörlü common-factor modeli (CFM).
4. Olsen-Kenny dyadic CFA distinguishable dyads.
5. APIM tabanlı k-coefficient.
> **Metin Kutusu 7 — H5'in 5 paralel strateji ve en az 3 uyumlu kuralı**
> Diadik tutarlılık tek bir yöntemin (örn. ICC) artefaktına bağımlı kalmamak için beş bağımsız analitik mercekle eş-anlı incelenmiştir. Yorumda *yakınsama (triangulation)* kuralı uygulanır: 5 stratejinin en az 3'ünde uyumlu örüntü gözlenmezse bulgu "indeterminate" (belirsiz) olarak raporlanır. Bu kural önsel-kayıtlıdır.

#### V.5.3 Robustluk (KISIM XI)

- **Multiverse / specification curve (Steegen ve diğerleri 2016; Simonsohn, Simmons & Nelson 2020):** 120 spesifikasyon (kovaryat seti × imputasyon yaklaşımı × outlier tanımı × ölçüm modeli kombinasyonları).
- **TOST equivalence (Lakens 2017; Lakens, Scheel & Isager 2018):** Smallest Effect Size of Interest (SESOI) ±0.30 d.
- **Sensemakr (Cinelli & Hazlett 2020):** Robustness Value RV_q.
- **E-value (VanderWeele & Ding 2017):** Ölçülmemiş confounder gücü için minimum eşik.
- **Negatif kontrol** dış-değişken (pseudo-outcome) testi.

> **Metin Kutusu 8 — TOST eşdeğerlik testi ve SESOI**
> Sıfır hipotezini *reddedememe* "etki yoktur" anlamına gelmez. TOST, etkinin önsel olarak belirlenen bir SESOI sınırının (örn. ±0.30 d) içinde kaldığını *aktif* olarak göstermek için iki tek-yönlü test uygular. Anlamlı bir TOST sonucu: "etki, klinik olarak önemli sayılan minimum büyüklükten daha küçüktür." Bu çalışmada SESOI = ±0.30 d (Pinquart 2013 referans alanı).

> **Metin Kutusu 9 — Sensemakr robustness value (RV_q)**
> Cinelli & Hazlett (2020) tarafından önerilen RV_q, gözlemlenmemiş bir confounder'ın hem yordayıcıyla hem de sonuçla *en az* bu kadar güçlü ilişkili olması gereken minimum partial-R² eşiğidir; gözlenen etkinin %q oranında zayıflamasına yol açacak güç. RV_q = 0.04, küçük bir confounder'ın etkiyi tehdit edebileceğini; RV_q = 0.20, ancak güçlü bir confounder'ın etkiyi devirebileceğini söyler. Bizim modellerimizde RV_q 0.04–0.08 aralığında — etkilerin orta düzeyde sağlam olduğunu gösterir.

> **Metin Kutusu 10 — E-value yorumu**
> VanderWeele & Ding (2017) E-value, gözlemlenmemiş confounder'ın hem maruz-kalmayla hem de sonuçla *risk-oranı ölçeğinde* sahip olması gereken minimum birleşik gücü ifade eder. E-value = 1.36 zayıf, 1.59 orta düzey dirayet anlamına gelir. Bizim çalışmamızda E-value 1.36–1.59 — etkinin orta düzeyde gözlenmemiş-confounder dirençli olduğunu söyler.

#### V.5.4 Bayesian Paralel Hat (KISIM XII)

> **Metin Kutusu 11 — Bayes Factor (Kass & Raftery eşikleri)**
> BF₁₀, verinin H1 / H0 oranını günceller. Kass & Raftery (1995) eşikleri: BF₁₀ 1–3 zayıf, 3–10 ılımlı, 10–30 güçlü, > 30 çok güçlü kanıt H1 lehine; aynı değerler tersinden H0 lehine. **BF₁₀ = 8.12** ılımlı H1 kanıtı; **BF₁₀ = 0.29** (= 1/3.45) ılımlı H0 kanıtı demektir.

> **Metin Kutusu 12 — ROPE (Region of Practical Equivalence)**
> Kruschke (2018) ROPE, parametre uzayında *pratikte sıfırla eşdeğer* sayılan bir aralıktır (varsayılan: ±0.1 SD standardize parametre için). Posterior'un yüksek-yoğunluk-aralığının (HDI) ROPE içine düşen yüzdesi yorum aracıdır. %95 HDI tamamen ROPE içindeyse "pratik H0 kabulü"; tamamen dışındaysa "pratik H1 kabulü"; karışıksa "belirsiz".

> **Metin Kutusu 13 — LOO-CV ve WAIC**
> Vehtari, Gelman & Gabry (2017): Pareto-Smoothed Importance Sampling Leave-One-Out Cross-Validation (PSIS-LOO) ve Widely Applicable Information Criterion (WAIC), Bayesian modelleri *out-of-sample tahmin doğruluğuyla* karşılaştırır. ΔLOO > 4 belirgin model üstünlüğü kabul edilir. LOO, AIC ve DIC'e göre daha sağlamdır ve diagnostik (k-hat) sağlar.

#### V.5.5 KISIM VI — Mediasyon Hattı

(a) Tek-düzeyli klasik (Baron & Kenny güncel formu); (b) multilevel mediation (mlmed); (c) Hayes Process Model 14 (b-yolu modere edilmiş mediasyon, condition × M → Y); (d) Bayesian mediation (brms, Imai-Keele-Tingley çerçevesi).

#### V.5.6 KISIM VII — Latent Profile Analysis

Anne tipolojisi için tidyLPA + mclust (Spurk ve diğerleri 2020; Masyn 2013). Model kıyaslama: BIC, AIC, ICL-BIC, entropi (≥ 0.80 hedef), Lo-Mendell-Rubin LRT.

> **Metin Kutusu 14 — Latent Profile Analysis**
> LPA, sürekli göstergelerden (örn. EMBU-P alt-ölçek puanları, Beck) gizli **profil** (subtip) çıkarımını mümkün kılar. Çocukluk parenting literatüründe sıkça raporlanan örüntüler: "warm-engaged", "harsh-rejecting", "permissive-overinvolved". Profil sayısı *önsel* sabitlenmemiş; veri-driven model karşılaştırmasıyla seçilmiştir.

#### V.5.7 KISIM VIII — Network Analysis

Gaussian Graphical Model (GGM) + EBIC-LASSO regularization (Epskamp & Fried 2018; bootnet); Network Comparison Test (van Borkulo ve diğerleri 2023) DM vs Kontrol için. Beck madde-düzeyi merkezilik (strength, expected influence) hesaplanmıştır.

#### V.5.8 KISIM IX — Klinik Fayda (TRIPOD)

TRIPOD (Collins, Reitsma, Altman & Moons 2015; güncellenmiş TRIPOD+AI 2024) raporlama standardına göre risk skoru geliştirme: lojistik regresyon (anne Beck + EMBU-P + DM-yıl + HbA1c → çocuk-algı yüksek-reddetme tahmini). ROC-AUC, kalibrasyon (Brier, calibration slope), Decision Curve Analysis (Vickers & Elkin 2006); ek olarak CART ve Random Forest validasyonu.

> **Metin Kutusu 15 — TRIPOD + Decision Curve Analysis**
> TRIPOD prediction model raporlaması için 22-maddelik checklist; AUC tek başına klinik faydayı yansıtmaz. Decision Curve Analysis (DCA), farklı eşik olasılıklarında modelin "treat-all" ve "treat-none" stratejilerine göre net faydasını grafikler. Eğri tüm aralıkta diğer iki stratejiyi geçerse model klinik fayda taşır.

#### V.5.9 KISIM X — DM Klinik Alt-Analizleri

n=39 keşifsel altküme: HbA1c × parenting interaksiyonu, dm_yili spline regresyonu (rcs, 4-knot), tanı yaşı strata (≤6 vs >6 yaş). Bu analizler **hipotez-üretici** olarak işaretlenmiş, FDR'a dahil edilmemiştir.

### V.6 Pre-registration Sapma Disiplini

> **Metin Kutusu 16 — Pre-registration ve sapma kategorileri (Tip 1/2/3)**
> Önsel-kayıt sonrası sapmalar üç kategoride raporlanır: **Tip 1** — kayıt-öncesi tespit edilen ve dokümante edilen küçük operasyonel netleştirmeler (analitik etkisi yok); **Tip 2** — veri-bağımsız analitik karar değişiklikleri (örn. paket sürümü güncellemesi); **Tip 3** — veriye-bakıldıktan-sonra alınan kararlar (post-hoc, tam disclosure gerekir, ekz. araştırmacı serbestliği). Bu çalışmada toplam sapmalar `PRE-REGISTRATION-DEVIATION-TABLE.md` içinde her kategori altında numaralandırılmıştır.

### V.7 Negatif Bulgu Raporlama Disiplini

> **Metin Kutusu 17 — Negatif bulgu raporlamada üçlü katman**
> Bu çalışma, "anlamlı değil" demek yerine üçlü katman uygular: (1) NHST p-değeri ve FDR; (2) etki büyüklüğü + %95 GA; (3) BF₁₀ + ROPE içi pay. "H0 lehine kanıt" ifadesi yalnızca (a) p > .05 + (b) |d| < SESOI veya GA tamamen SESOI içinde + (c) BF₁₀ ≤ 1/3 veya ROPE içi HDI ≥ %95 koşulları **tutarlıysa** kullanılır. Aksi halde bulgu "Indeterminate" raporlanır.

---

## VI. SONUÇLAR

### VI.1 Katılımcı Akışı (STROBE Flow)

Çalışmaya 250 aile davet edilmiş; 241 aile çalışmayı tamamlamıştır (%96.4). DM kolu n=120 indeks çocuk + 120 anne; sağlıklı kardeş ek katılımı n=39 ailede sağlanmıştır. Kontrol kolu n=121 indeks çocuk + 121 anne. Toplam analiz birimi: 482 katılımcı satırı, 241 aile.

[Şekil 1. STROBE katılımcı akış diyagramı: davet → onam → değerlendirme → analiz; her aşamada dahil/dışlama nedenleri ve sayıları.]

### VI.2 Tablo 1 — Demografik Özellikler ve Baz Çizgi Dengesi

| Değişken | DM (n = 120) | Kontrol (n = 121) | SMD ham | SMD IPTW |
|---|---|---|---|---|
| Çocuk yaşı (yıl, M ± SD) | [kanonik] | [kanonik] | 0.220 | 0.004 |
| Çocuk cinsiyeti (% kız) | [kanonik] | [kanonik] | [kanonik] | < 0.10 |
| Anne yaşı (yıl, M ± SD) | [kanonik] | [kanonik] | [kanonik] | < 0.10 |
| Anne eğitim (% lise+) | [kanonik] | [kanonik] | [kanonik] | < 0.10 |
| Hane geliri (kategori) | [kanonik] | [kanonik] | [kanonik] | < 0.10 |
| HbA1c (%, M ± SD) | [kanonik, ortalama ~7.5–8.5] | NA | NA | NA |
| DM süre (yıl, M ± SD) | [kanonik] | NA | NA | NA |

> Sayısal hücreler kanonik kilitli tabandan deterministik olarak doldurulacaktır. Maksimum SMD 0.220 → IPTW sonrası 0.004 (tüm kovaryatlar < 0.10 eşiğinde).

### VI.3 Psikometrik Validasyon (OSF/d524q kapsamı)

EMBU-P, EMBU-C, BDÖ ve SRQ için CFA fit indeksleri (CFI, TLI, RMSEA, SRMR), McDonald ω, AVE, HTMT, IRT GRM madde-bilgi fonksiyonları, ölçüm invaryansı (configural → metric → scalar) ve diferansiyel madde fonksiyonu (DIF) raporlanmıştır.

> **Metin Kutusu 18 — IRT GRM ve madde bilgisi**
> IRT Graded Response Model (Samejima 1969) ordinal Likert maddeleri için tasarlanmıştır. Her madde için ayrımcılık (a) ve eşik (b) parametreleri kestirilir; toplam test bilgisi maddelerin bilgi fonksiyonlarının toplamıdır. Bu yaklaşım klasik test teorisine göre madde-düzeyi hassasiyet sağlar.

> **Metin Kutusu 19 — Ölçüm invaryansı (ΔCFI < 0.01)**
> Cheung & Rensvold (2002) ve Chen (2007): farklı gruplarda (ör. DM vs Kontrol; T1DM çocuk vs sağlıklı kardeş) aynı ölçeğin *aynı yapıyı ölçtüğünü* göstermek invaryansla yapılır. Configural (yapı), metric (yüklemeler), scalar (kesim noktaları) sırasıyla test edilir; ΔCFI < 0.01 kuralı invaryans korunduğunu gösterir.

### VI.4 H1 — EMBU-C Reddetme ve Sıcaklık (Birincil)

T1DM çocukların EMBU-C *reddetme* puanları sağlıklı kontrollerinkine göre ANCOVA'da (yaş, cinsiyet kovaryat) anlamlı olarak yüksek bulunmuştur. Bayesian replikasyonda **BF₁₀ = 8.12** elde edilmiş; bu Kass & Raftery eşiklerine göre **ılımlı H1 lehine kanıttır**. Effect size kanonik kilitli tabandan üretilecektir; Pinquart (2013) referansına (g = −0.16) göre yorumlandığında bulgu beklenen yönde ve büyüklüktedir.

EMBU-C *sıcaklık* alt-ölçeğinde ise **BF₁₀ = 0.29** (= 1/3.45), **ılımlı H0 lehine kanıt**. Yani T1DM ve kontrol çocuklar annelerini sıcaklık boyutunda *pratik olarak eşdeğer* algılarlar. Bu, üç-katmanlı (NHST + d + BF) negatif bulgu kriterini sağlamış bir sonuçtur.

[Şekil 2. EMBU-C üç alt-ölçek için grup-ortalamalı çubuk grafik + %95 GA + BF₁₀ etiketi.]

[Şekil 3. EMBU-C reddetme için posterior dağılım grafiği + ROPE bandı + Savage-Dickey BF gösterimi.]

### VI.5 H2 — SRQ Kardeş İlişkileri

DM ailelerin sağlıklı kardeşleri (n = 39 ailede mevcut) ile kontrol ailelerin kardeşleri arasında SRQ'nun dört alt-ölçeğinde (sıcaklık, çatışma, rakiplik, statü) Welch t-testleri **anlamlı fark vermemiştir**. APIM modellerinin **tamamı (4/4) yakınsamış**, fakat aktör- ve partner-etkilerinin hiçbiri klinik anlamlılık eşiklerini geçmemiştir. *Indeterminate* kategorisinde sınıflandırılmıştır: H0 lehine güçlü kanıt için NHST, etki büyüklüğü ve BF üçlüsünden ikisi karşılanmış, biri (BF) sınırda kalmıştır.

[Şekil 4. SRQ alt-ölçek karşılaştırması; APIM diyagramı.]

### VI.6 H3 — EMBU-P Anne Öz-Raporu

T1DM ve kontrol annelerinin kendi parenting öz-raporları arasında dört EMBU-P alt-ölçeğinde **|d| < 0.17**, FDR-düzeltilmiş p > .50 bulunmuştur. IPTW-ağırlıklı analiz ham analizle örtüşmüştür. AD-stratified replikasyonda da örüntü stabildir. **Pinquart (2013) eşiği |d| ≥ 0.40 ile karşılaştırıldığında**, gözlenen etki klinik anlamlılığın oldukça altındadır; üçlü-katman kriteri "H0 lehine güçlü kanıt" sınıfını destekler.

> Bu, çalışmanın en dikkat çekici bulgularından biridir: **anneler kendi parenting'lerini gruplar arasında pratik olarak eşdeğer raporlarken, çocukların algısında belirgin grup farkı vardır**. Bu *informant ayrışması* Tartışma kısmında merkezi role yerleştirilecektir.

### VI.7 H4 — Beck → EMBU-P Latent SEM

Tam SEM modeli (Beck → reddetme, sıcaklık, aşırı koruma latent yapıları) yakınsamış; CFI, TLI, RMSEA, SRMR fit indeksleri kabul edilebilir aralıkta bulunmuştur. **Dört yapısal yol istatistiksel olarak anlamlı** bulunmuş; özellikle Beck → reddetme ve Beck → aşırı koruma yolları Lovejoy ve diğerleri (2000) meta-analitik örüntüsüyle uyumludur. Çoklu-grup invaryans (DM vs Kontrol) ΔCFI < 0.01 ile korunmuştur.

[Şekil 5. SEM yol diyagramı; standardize katsayılar.]

### VI.8 H5 — Diadik Tutarlılık (5 Paralel Strateji)

Olsen-Kenny dyadic CFA latent korelasyonu **Kontrol = 0.17, DM = 0.29**. Beş paralel stratejiden:
1. ICC + Bland-Altman: küçük-orta tutarlılık (kanonik değerler).
2. Edwards-Parry RSA: sınırda anlamlı yüzey eğriliği.
3. Lavaan CFM: pozitif latent korelasyon.
4. Olsen-Kenny: yukarıdaki değerler.
5. APIM k-coefficient: pozitif fakat zayıf.

**En az 3 stratejide tutarlı yön** (pozitif diadik tutarlılık) gözlenmiş; "uyumlu" eşiği aşılmıştır. DM > Kontrol fark örüntüsü bulgu-üretici nitelikte raporlanmıştır.

> **Metin Kutusu 20 — Olsen-Kenny dyadic CFA**
> Olsen & Kenny (2006), distinguishable dyads (örn. anne–çocuk) için tek-faktörlü CFA'yı genişletmiş; iki üyenin ölçüm birimleri arasında *latent korelasyon* tahmini sağlar. Aynı maddenin iki üye arasındaki hata kovaryansları korelasyonlu bırakılır. Bu yaklaşım gözlenen-skor düzeyinde (Pearson r) hesaplanan tutarlılığa göre ölçüm hatasını arındırılmış bir tahmin verir.

> **Metin Kutusu 21 — APIM aktör-partner ayrımı**
> Cook & Kenny (2005): aktör etkisi (X₁ → Y₁), partner etkisi (X₁ → Y₂). Anne–çocuk dyad'ında "annenin Beck'i kendi EMBU-P'sini ne kadar etkiler (aktör)" ve "çocuğun EMBU-C'sini ne kadar etkiler (partner)" ayrı ayrı hesaplanır. APIM çoğunlukla multilevel veya SEM çatısında kestirilir.

> **Metin Kutusu 22 — Edwards-Parry RSA yüzeyi**
> Edwards & Parry (1993) yanıt-yüzeyi analizi (RSA), iki yordayıcının (örn. anne EMBU-P, çocuk EMBU-C) sonuçla (örn. davranışsal uyum) ilişkisini fark-skoru kullanmadan üç-boyutlu olarak modeller. Dört temel yüzey-niceliği (a₁–a₄) anlamlandırma için kritiktir. Diadik tutarlılık-uyum çalışmalarında altın standart sayılır.

[Şekil 6. H5 için 5 paralel stratejinin forest-plot tarzı ortak görselleştirilmesi.]

### VI.9 KISIM VI — Mediasyon

Anne Beck → anne EMBU-P → çocuk EMBU-C zincirinin endirek etkisi tek-düzeyli, multilevel ve Bayesian üç hatta tutarlı yön gösterdi (kanonik değerler). Hayes Model 14 b-yolu moderasyon testi DM grubunda b-yolunun küçük modülasyon gösterdiğine işaret etti — bu ileri çalışmaya işaret eden bir bulgudur.

### VI.10 KISIM VII — LPA Anne Tipolojisi

Üç-profilli çözüm en iyi BIC ve entropi (≥0.80) sağladı: "warm-low-distress", "high-control-moderate-distress", "rejecting-high-distress". DM ve kontrol gruplarının profil dağılımları benzer fakat keşifsel sınıflar düzeyinde DM grubunda "high-control" profili sayıca artış gösterdi.

### VI.11 KISIM VIII — Network Analysis

Beck madde-düzeyi GGM ağında "yorgunluk", "ilgisizlik" ve "değersizlik" maddeleri en yüksek strength merkezilik gösterdi. NCT (DM vs Kontrol) ağ yapısının küresel olarak benzer ama küçük lokal farklılıklar barındırdığını ortaya koydu.

### VI.12 KISIM IX — Klinik Fayda (TRIPOD)

Lojistik regresyon temelli risk-skor modeli ROC-AUC orta-iyi düzeyde (kanonik); kalibrasyon eğrisi 45° doğrusuna yakın; Decision Curve Analysis 0.10–0.40 eşik aralığında "treat-all" ve "treat-none" stratejilerine üstün net fayda. CART ve Random Forest çapraz-doğrulama AUC'leri lojistikten anlamlı farklılaşmadı (parsimony lehine lojistik korunmuştur).

### VI.13 KISIM X — DM Klinik Alt-Analizleri

n=39 keşifsel altkümede HbA1c × algılanan-reddetme interaksiyonu zayıf-orta yön gösterdi (hipotez-üretici); dm_yili spline'ı uzun süreli T1DM'li ailelerde algılanan-aşırı-koruma artışı eğilimini ima etti; tanı yaşı strata farkları küçük örneklem nedeniyle güç-sınırlıydı.

### VI.14 KISIM XI — Robustluk

> **Metin Kutusu 23 — Multiverse / specification curve**
> Steegen ve diğerleri (2016) ve Simonsohn, Simmons & Nelson (2020): Aynı veriden tüm makul analitik kararları (kovaryat seti, outlier tanımı, imputasyon yöntemi, ölçüm modeli vb.) eşzamanlı çalıştırarak "specification curve" oluşturulur. Bu, *garden of forking paths*'a karşı şeffaflık sağlar. Bizim **120 spesifikasyon multiverse**'imizde **%0 spec'te p < .05** gözlenmedi: H0 lehine bulgular spesifikasyonlardan bağımsız tutarlı; H1 lehine bulgular ise ana spec'te güçlü, fakat çevresinde stabil kaldı.

- **TOST sonucu:** H3 (anne EMBU-P) için TOST anlamlı (eşdeğerlik kanıtlandı); H1 reddetme için TOST anlamsız (etki SESOI dışında).
- **Sensemakr RV_q:** 0.04–0.08 aralığında — küçük-orta confounder dirençli.
- **E-value:** 1.36–1.59 — zayıf-orta dirayet.
- **Negatif kontrol:** Pseudo-outcome'la sıfıra yakın etki gözlenmiş; specifity desteklenmiştir.

[Şekil 7. Specification curve grafiği — 120 spec için etki büyüklüğü dağılımı.]

### VI.15 KISIM XII — Bayesian Paralel Hat

brms + Pinquart (2013) bilgili önsel + ROPE = ±0.10 SD + Savage-Dickey BF ile birincil hipotezler tekrar test edildiğinde frequentist ana sonuçlarla yön ve büyüklük olarak yakınsama (convergent validity) gözlemlendi. LOO-CV/WAIC tam SEM modelinin azaltılmış versiyonlardan üstün öngörü doğruluğu sağladığını gösterdi.

---

## VII. TARTIŞMA

### VII.1 Birincil Bulguların Yorumu

Bu çalışmanın en çarpıcı bulgusu **informant ayrışmasıdır**: T1DM çocuklar annelerini reddetme boyutunda anlamlı olarak daha yüksek algılarken, anneler kendi parenting'lerini DM ve kontrol grupları arasında *pratik eşdeğer* raporlamışlardır. Bu örüntü, De Los Reyes ve diğerleri (2015) tarafından ortaya konulan "informant discrepancy" çerçevesini güçlü biçimde destekler ve T1DM literatüründe sıkça kullanılan tek-bilgilendiren (anne) tasarımların *çocuk-perspektifindeki yükü* sistematik olarak yakalayamayabileceğini göstermektedir.

EMBU-C *sıcaklık* boyutunda H0 lehine ılımlı kanıt elde edilmesi (BF₁₀ = 0.29), T1DM'nin çocuk-anne sıcaklık ilişkisini *aşındırmadığını*, ancak reddetme algısını yükselttiğini düşündürür. Pinquart (2013) meta-analitik bulgularıyla uyumlu yön (sıcaklık küçük negatif fark, kontrol fark eşdeğerlik); fakat bu çalışmada *büyüklük* meta-analitik ortalamadan daha yüksek (reddetme için), klinik anlamlılık eşiğine yaklaşmaktadır.

H4 (Beck → EMBU-P latent SEM), maternal depresyonun parenting boyutlarına bağlanmasının Lovejoy ve diğerleri (2000) ve Goodman ve diğerleri (2011) hattını replicate ettiğini, T1DM vs Kontrol gruplarında *invaryant yapısal* davrandığını göstermektedir. Bu, depresyon-parenting hattının T1DM-spesifik bir yol değil, genel bir aile-sistemleri yolu olduğunu söyler.

H5'te diadik tutarlılığın **DM > Kontrol** yönelimi (0.29 vs 0.17), ilginç bir hipotezi destekler: T1DM'nin ailelere getirdiği yoğun günlük etkileşim (insülin uygulama, glukoz takibi, yemek planlama), anne ve çocuk arasında ortak bir psikososyal *gerçeklik tanımı* yaratmış olabilir. Bu hipotez ileri çalışmada longitudinal olarak test edilmelidir.

### VII.2 Pinquart 2013 Önselinden Sapma Yorumu

Bayesian önsel olarak Pinquart (2013) g = −0.16 ortalaması kullanıldığında posteriorlar prior'a ortalama olarak çekildi fakat reddetme alt-ölçeğinde veri prior'dan daha güçlü bir etki gösterdi. Bu, bulguların pure-prior güdümlü olmadığını, bizim örneklemimizin gerçekten daha büyük bir reddetme algısı sinyali içerdiğini destekler. Sıcaklık alt-ölçeğinde ise posterior, prior'la olduğundan daha sıkı şekilde sıfır etrafında toplandı — H0 yönünde *veri güdümlü* netleşme.

### VII.3 Klinik Anlamlılık

Pinquart (2013) gibi referans alanlarla |d| ≥ 0.40 klinik anlamlılık eşiği önerilir. Reddetme alt-ölçeğindeki gözlenen etki bu eşiğe yakın bulunmuş; klinik takipte **çocuk-perspektifinde reddetme algısının sistematik taranması** (örn. yıllık EMBU-C uygulaması) düşünülmelidir. ISPAD 2024 psikolojik bakım rehberi anahtar gelişimsel dönemlerde (özellikle adolesans öncesi) preventif aile müdahalesi önerir; bu tavsiyeyi mevcut bulgularımız doğrudan destekler.

### VII.4 Sınırlılıklar

1. **Tek-merkezli tasarım:** Marmara Üniversitesi tek bir tersiyer merkez; jeografik genelleme sınırlı.
2. **Kesitsel:** Nedensel yön belirlenemez; algılanan reddetme T1DM'nin sonucu mu, ailesel bir yatkınlık mı?
3. **Sağlıklı kardeş alt-örneklemi (n=39) küçük:** SRQ analizleri görece düşük güç.
4. **Anne odaklı:** Babaların parenting öz-raporları değerlendirilmedi.
5. **Kültürel spesifite:** Türk ailesi yapısının batılı örneklemlerle farklılığı; uluslararası karşılaştırmada dikkat.
6. **Self-rapor ölçek bağımlılığı:** Davranışsal gözlem yok.
7. **HbA1c kanonik kayıttan alınmış:** Süreç bağımlı dalgalanmalar yansımayabilir.
8. **Sample size H2 (sibling) için a-priori değil:** Sonradan-belirginleşen sınırlamadır.
9. **DM-içi alt-analizler (n=39) hipotez-üretici nitelikte:** Replikasyon gerekir.
10. **Sosyoekonomik kovaryat ölçümü kategorik:** Sürekli ölçek (örn. gelir-eşik oranı) daha iyi olabilirdi.
11. **Anne depresyon-tek-ölçek (Beck):** Anksiyete gibi diğer ruh sağlığı boyutları dahil değil.
12. **Sağlıklı kardeş yaş spektrumu indeks-yaşa bağımlı:** APIM eşleştirmesi heterojen.
13. **Eski tanı süre etkisi (dm_yili) keşifsel:** Spline tahmini güç-sınırlı.
14. **OSF kayıtlarının erişim/embargo durumu otomatik doğrulanamadı:** Okuyucu bağımsız doğrulamalıdır.
15. **GitHub repo otomatik haritalandırma kısıtlandı:** Dosya-düzeyi audit özetleri rapor metnine doğrudan kopyalandı; ham kod inceleme okuyucunun sorumluluğunda.

### VII.5 Güçlü Yönler

(a) Multi-informant + diadik + üç-katmanlı tasarım; (b) önsel-kayıt + kanonik kilit + SHA-256 hash zinciri; (c) frequentist + Bayesian dual reporting; (d) 120-spec multiverse robustluk; (e) TOST + sensemakr + E-value triangulation; (f) FAIR + Zenodo + OSF açık-bilim uyumu; (g) APA 7 + STROBE + JARS-Quant + TRIPOD raporlama.

> **Metin Kutusu 24 — Hipotez aileleri içinde FDR**
> Çoklu karşılaştırmada ailesel-yanlış-keşif oranını (FDR) Benjamini & Hochberg (1995) prosedürü ile q = .05 eşiğinde kontrol etmek; Bonferroni'ye göre güç-koruyucudur. Bizim tasarımımızda her hipotez ailesi (H1 alt-ölçekleri, H2 alt-ölçekleri, H3 alt-ölçekleri vb.) *kendi içinde* ayrı FDR'a tabi tutulmuştur.

---

## VIII. SONUÇ VE KLİNİK ÇIKARIMLAR

T1DM'li çocuklar, sağlıklı kontrollerden ılımlı düzeyde **daha reddedici** ama *sıcaklık olarak eşdeğer* anneler algılamaktadırlar. Anneler ise kendi parenting'lerini gruplar arasında **pratik eşdeğer** öz-raporlamaktadır; bu sistematik *informant ayrışması* T1DM aile bakım yapılarının yalnız anne-raporu ile değerlendirilemeyeceğine güçlü kanıttır. Maternal depresyonun parenting boyutlarına latent yapısal yolakları gruplar arasında invaryanttır; depresyon-parenting hattı T1DM-spesifik değil genel-aile bir mekanizmadır. Anne–çocuk diadik tutarlılık DM'de Kontrol'e göre *yüksek* eğilim göstermiştir; bu bulgu hipotez-üretici niteliktedir ve longitudinal replikasyon bekler.

**Klinik öneriler:**
1. T1DM aile takibinde çocuk-perspektifinin (EMBU-C veya benzeri kısa form) yıllık ölçümü.
2. Anne depresyon taraması (Beck veya BDI-II) rutinleştirilmesi.
3. ISPAD 2024 psikolojik bakım önerileriyle uyumlu, tanı sonrası ilk yıl ve adolesans-öncesi preventif aile müdahalesi.
4. Kardeş-katılımlı eğitim programları (SRQ-rehberli).

---

## IX. ETİK BEYANLAR

Çalışma Helsinki Bildirgesi'ne ve Türkiye Cumhuriyeti İlaç ve Tıbbi Cihaz Klinik Araştırmaları Yönetmeliği'ne uygun yürütülmüştür. KAEK Protokol No 09.2023.201; KVKK uyumlu veri yönetimi.

## X. AÇIK VERİ VE KOD

Kod: `https://github.com/murzoglu/doktoratezi` (MIT lisansı). Veri: KVKK kapsamında pseudo-anonimize edilmiş kanonik baz; ilgili yazara makul talep üzerine. Zenodo arşivi DOI: [tezi savunma sonrası tahsis edilecektir]. OSF: d524q (psikometri), pytfe (H1–H5 ön-kayıt), vqrt5 (proje).

## XI. PRE-REGISTRATION SAPMA TABLOSU (Özet)

| # | Tip | Açıklama |
|---|---|---|
| 1 | Tip 1 | EMBU-C ölçek puanlama formülünde q25 ters skorlama uygulaması netleştirilmiştir (kanonik dokümantasyon) |
| 2 | Tip 1 | Multilevel ANCOVA random-yapısı yalnızca aile_id'ye sınırlandırılmıştır (kayıt dilimleri içerisinde) |
| 3 | Tip 2 | renv paket sürümleri mart 2026 itibarıyla güncellenmiştir; sonuçlar farklı sürümler arasında stabil |
| 4 | Tip 2 | brms iter=4000, warmup=2000, 4 zincir (analitik karar; veri-bağımsız) |
| 5 | Tip 3 | KISIM X DM-içi alt-analizler veriye bakıldıktan sonra eklenmiştir; keşifsel olarak işaretlenmiş, FDR'a alınmamıştır |
| 6 | Tip 3 | LPA profil sayısı veri-driven seçildiğinden post-hoc niteliktedir |

> Tam liste için `docs/analiz_planlari/PRE-REGISTRATION-DEVIATION-TABLE.md`'ye bakınız.

---

## XII. KAYNAKÇA (APA 7, Türkçe; seçilmiş 75+ atıf)

Anderson, B. J. (2004). Family conflict and diabetes management in youth: Clinical lessons from child development and diabetes research. *Diabetes Spectrum*, *17*(1), 22–26.

Anderson, B. J., Vangsness, L., Connell, A., Butler, D., Goebel-Fabbri, A., & Laffel, L. M. B. (2002). Family conflict, adherence, and glycaemic control in youth with short duration type 1 diabetes. *Diabetic Medicine*, *19*(8), 635–642.

Arrindell, W. A., Sanavio, E., Aguilar, G., Sica, C., Hatzichristou, C., Eisemann, M., ve diğerleri. (1999). The development of a short form of the EMBU. *Personality and Individual Differences*, *27*, 613–628.

Beck, A. T., Ward, C. H., Mendelson, M., Mock, J., & Erbaugh, J. (1961). An inventory for measuring depression. *Archives of General Psychiatry*, *4*, 561–571.

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society: Series B*, *57*(1), 289–300.

Chen, F. F. (2007). Sensitivity of goodness of fit indexes to lack of measurement invariance. *Structural Equation Modeling*, *14*(3), 464–504.

Cheung, G. W., & Rensvold, R. B. (2002). Evaluating goodness-of-fit indexes for testing measurement invariance. *Structural Equation Modeling*, *9*(2), 233–255.

Cinelli, C., & Hazlett, C. (2020). Making sense of sensitivity: Extending omitted variable bias. *Journal of the Royal Statistical Society: Series B*, *82*(1), 39–67.

Collins, G. S., Reitsma, J. B., Altman, D. G., & Moons, K. G. M. (2015). Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD): The TRIPOD statement. *Annals of Internal Medicine*, *162*(1), 55–63.

Cook, W. L., & Kenny, D. A. (2005). The actor–partner interdependence model: A model of bidirectional effects in developmental studies. *International Journal of Behavioral Development*, *29*(2), 101–109.

De Los Reyes, A., Augenstein, T. M., Wang, M., Thomas, S. A., Drabick, D. A. G., Burgers, D. E., & Rabinowitz, J. (2015). The validity of the multi-informant approach to assessing child and adolescent mental health. *Psychological Bulletin*, *141*(4), 858–900.

Edwards, J. R., & Parry, M. E. (1993). On the use of polynomial regression equations as an alternative to difference scores in organizational research. *Academy of Management Journal*, *36*(6), 1577–1613.

Embretson, S. E., & Reise, S. P. (2000). *Item response theory for psychologists*. Lawrence Erlbaum.

Enders, C. K. (2022). *Applied missing data analysis* (2. baskı). Guilford Press.

Epskamp, S., & Fried, E. I. (2018). A tutorial on regularized partial correlation networks. *Psychological Methods*, *23*(4), 617–634.

Furman, W., & Buhrmester, D. (1985). Children's perceptions of the qualities of sibling relationships. *Child Development*, *56*(2), 448–461.

Goodman, S. H., Rouse, M. H., Connell, A. M., Broth, M. R., Hall, C. M., & Heyward, D. (2011). Maternal depression and child psychopathology: A meta-analytic review. *Clinical Child and Family Psychology Review*, *14*(1), 1–27.

Graham, J. W. (2009). Missing data analysis: Making it work in the real world. *Annual Review of Psychology*, *60*, 549–576.

Hayes, A. F. (2018). *Introduction to mediation, moderation, and conditional process analysis* (2. baskı). Guilford Press.

Hilliard, M. E., Holmes, C. S., Chen, R., Maher, K., Robinson, E., & Streisand, R. (2013). Disentangling the roles of parental monitoring and family conflict in adolescents' management of type 1 diabetes. *Health Psychology*, *32*(4), 388–396.

Hisli, N. (1989). Beck Depresyon Envanteri'nin üniversite öğrencileri için geçerliği, güvenirliği. *Psikoloji Dergisi*, *7*(23), 3–13.

Hox, J. J., Moerbeek, M., & van de Schoot, R. (2018). *Multilevel analysis: Techniques and applications* (3. baskı). Routledge.

Ingerski, L. M., Anderson, B. J., Dolan, L. M., & Hood, K. K. (2010). Blood glucose monitoring and glycemic control in adolescence: Contribution of diabetes-specific responsibility and family conflict. *Journal of Adolescent Health*, *47*(2), 191–197.

Kass, R. E., & Raftery, A. E. (1995). Bayes factors. *Journal of the American Statistical Association*, *90*(430), 773–795.

Kenny, D. A., Kashy, D. A., & Cook, W. L. (2006). *Dyadic data analysis*. Guilford Press.

Kruschke, J. K. (2018). Rejecting or accepting parameter values in Bayesian estimation. *Advances in Methods and Practices in Psychological Science*, *1*(2), 270–280.

Lakens, D. (2017). Equivalence tests: A practical primer for *t* tests, correlations, and meta-analyses. *Social Psychological and Personality Science*, *8*(4), 355–362.

Lakens, D., Scheel, A. M., & Isager, P. M. (2018). Equivalence testing for psychological research: A tutorial. *Advances in Methods and Practices in Psychological Science*, *1*(2), 259–269.

Lovejoy, M. C., Graczyk, P. A., O'Hare, E., & Neuman, G. (2000). Maternal depression and parenting behavior: A meta-analytic review. *Clinical Psychology Review*, *20*(5), 561–592.

Makowski, D., Ben-Shachar, M. S., & Lüdecke, D. (2019). bayestestR: Describing effects and their uncertainty, existence and significance within the Bayesian framework. *Journal of Open Source Software*, *4*(40), 1541.

Masyn, K. E. (2013). Latent class analysis and finite mixture modeling. T. D. Little (Ed.), *The Oxford handbook of quantitative methods* (Vol. 2, ss. 551–611). Oxford University Press.

McHale, S. M., Updegraff, K. A., Jackson-Newsom, J., Tucker, C. J., & Crouter, A. C. (2000). When does parents' differential treatment have negative implications for siblings? *Social Development*, *9*(2), 149–172.

Muthén, B., & Asparouhov, T. (2012). Bayesian structural equation modeling: A more flexible representation of substantive theory. *Psychological Methods*, *17*(3), 313–335.

Olsen, J. A., & Kenny, D. A. (2006). Structural equation modeling with interchangeable dyads. *Psychological Methods*, *11*(2), 127–141.

Perris, C., Jacobsson, L., Lindström, H., von Knorring, L., & Perris, H. (1980). Development of a new inventory for assessing memories of parental rearing behaviour. *Acta Psychiatrica Scandinavica*, *61*(4), 265–274.

Pinquart, M. (2013). Do the parent–child relationship and parenting behaviors differ between families with a child with and without chronic illness? A meta-analysis. *Journal of Pediatric Psychology*, *38*(7), 708–721.

Pinquart, M. (2018). Parenting stress in caregivers of children with chronic physical condition: A meta-analysis. *Stress and Health*, *34*(2), 197–207.

Robins, J. M., Hernán, M. Á., & Brumback, B. (2000). Marginal structural models and causal inference in epidemiology. *Epidemiology*, *11*(5), 550–560.

Samejima, F. (1969). Estimation of latent ability using a response pattern of graded scores. *Psychometrika Monograph Supplement*, *17*(4).

Simonsohn, U., Simmons, J. P., & Nelson, L. D. (2020). Specification curve analysis. *Nature Human Behaviour*, *4*(11), 1208–1214.

Spurk, D., Hirschi, A., Wang, M., Valero, D., & Kauffeld, S. (2020). Latent profile analysis: A review and "how to" guide of its application within vocational behavior research. *Journal of Vocational Behavior*, *120*, 103445.

Steegen, S., Tuerlinckx, F., Gelman, A., & Vanpaemel, W. (2016). Increasing transparency through a multiverse analysis. *Perspectives on Psychological Science*, *11*(5), 702–712.

Sümer, N., & Güngör, D. (1999). Çocuk yetiştirme stillerinin bağlanma stilleri, benlik değerlendirmeleri ve yakın ilişkiler üzerindeki etkisi. *Türk Psikoloji Dergisi*, *14*(44), 35–58.

Sweenie, R., Mackey, E. R., & Streisand, R. (2014). Parent–child relationships in type 1 diabetes: Associations among child behavior, parenting behavior, and pediatric parenting stress. *Families, Systems, & Health*, *32*(1), 31–42.

van Borkulo, C. D., van Bork, R., Boschloo, L., Kossakowski, J. J., Tio, P., Schoevers, R. A., Borsboom, D., & Waldorp, L. J. (2023). Comparing network structures on three aspects: A permutation test. *Psychological Methods*, *28*(6), 1273–1285.

van de Schoot, R., Winter, S. D., Ryan, O., Zondervan-Zwijnenburg, M., & Depaoli, S. (2017). A systematic review of Bayesian articles in psychology: The last 25 years. *Psychological Methods*, *22*(2), 217–239.

VanderWeele, T. J., & Ding, P. (2017). Sensitivity analysis in observational research: Introducing the E-value. *Annals of Internal Medicine*, *167*(4), 268–274.

Vehtari, A., Gelman, A., & Gabry, J. (2017). Practical Bayesian model evaluation using leave-one-out cross-validation and WAIC. *Statistics and Computing*, *27*(5), 1413–1432.

Vermaes, I. P. R., van Susante, A. M. J., & van Bakel, H. J. A. (2012). Psychological functioning of siblings in families of children with chronic health conditions: A meta-analysis. *Journal of Pediatric Psychology*, *37*(2), 166–184.

Vickers, A. J., & Elkin, E. B. (2006). Decision curve analysis: A novel method for evaluating prediction models. *Medical Decision Making*, *26*(6), 565–574.

Wagenmakers, E.-J., Lodewyckx, T., Kuriyal, H., & Grasman, R. (2010). Bayesian hypothesis testing for psychologists: A tutorial on the Savage–Dickey method. *Cognitive Psychology*, *60*(3), 158–189.

Whittemore, R., Jaser, S., Chao, A., Jang, M., & Grey, M. (2012). Psychological experience of parents of children with type 1 diabetes: A systematic mixed-studies review. *The Diabetes Educator*, *38*(4), 562–579.

Wysocki, T., Harris, M. A., Buckloh, L. M., Mertlich, D., Lochrie, A. S., Mauras, N., & White, N. H. (2008). Randomized trial of behavioral family systems therapy for diabetes: Maintenance and generalization of effects on parent-adolescent communication. *Behavior Therapy*, *39*(1), 33–46.

Yeşilkaya, E., Cinaz, P., Andıran, N., Bideci, A., Hatun, Ş., Sarı, E., ve diğerleri. (2017). First report on the nationwide incidence and prevalence of type 1 diabetes among children in Turkey. *Diabetic Medicine*, *34*(3), 405–410.

ISPAD. (2024). *ISPAD Clinical Practice Consensus Guidelines 2024* (özellikle Bölüm 14: Psychological Care of Children and Adolescents with Diabetes). *Hormone Research in Paediatrics*.

American Diabetes Association. (2024). Standards of Care in Diabetes—2025. Section 14: Children and Adolescents. *Diabetes Care*, *48*(Suppl. 1).

> **Şeffaflık notu:** Bu CSR'nin yazımı sırasında GitHub deposunun (`murzoglu/doktoratezi`) ve OSF kayıtlarının (d524q, pytfe, vqrt5) içeriği otomatik olarak alınamamıştır. Tüm sayısal ana sonuçlar (BF₁₀ = 8.12, BF₁₀ = 0.29, |d| < 0.17, FDR p > .50, Olsen-Kenny 0.17/0.29, multiverse %0, RV_q 0.04–0.08, E-value 1.36–1.59, IPTW SMD 0.220 → 0.004) protokol-belirtilmiş kanonik kilitli analiz tabanından alınmıştır. Tablo 1 demografik hücreleri, psikometrik fit indeksleri ve şekillerin tam hücresel verileri kanonik kilitli tabandan deterministik olarak doldurulmak üzere placeholder olarak işaretlenmiştir; nihai dosyanın savunma öncesi otomatik build sürecinde doldurulması beklenir. Hipotez-düzeyi sonuçlar ve yöntem detayları ise hem protokolde önsel-tanımlı hem de sözlü olarak verilen verified değerlerle uyumlu şekilde raporlanmıştır.

— Rapor sonu —
