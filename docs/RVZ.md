# T1DM-EBEVEYN CSR v1.0 (Carbon HTML PDF, 541 sayfa) — Sistematik Denetim Raporu

**Denetim tarihi:** 29 Nisan 2026
**Denetim kapsamı:** Format & yapı · Sayısal uyum · Tablo & figür doğruluğu · Anlatım kalitesi · Fazlalıklar
**Denetim dayanağı:** Talimatname v1.2 (§6.5 Quarto chunk, §7 raporlama, §9 dil, Hard-No #8/#10/#11), SAP v3.0 §4 tracker, project knowledge audit kanıtları (`R/19_h4_beck_parenting_sem.R::run_h4_primary()`, `chapters/03_bulgular.qmd`, `apa_t06..t22` aggregate CSV referansları)

---

## 0 · Genel Değerlendirme

PDF, **Carbon Design System tipografisi**, gerçekten gömülü **25 figür** (DAG, forest plot, Bland-Altman grid, DCA eğrisi, sensemakr contour vb.), **22 ana bölüm** ve **238 CSV artefakt** referansıyla **kapsam olarak çok güçlü** bir CSR'dir. STROBE flow diagram, causal DAG, H4 SEM yol diyagramı ve H5 Bland-Altman grid figürleri eksiksiz ve profesyonel kalitede. ICH E3 yapısı (kapak → sinopsis → kısaltmalar → etik → araştırmacılar → giriş → amaç → metodoloji → popülasyon → bulgular → tartışma → sınırlılıklar → sonuç → diseminasyon → referanslar → ekler) sırasıyla doğru kurulmuş.

**Ne var ki PDF, savunma sürümüne ulaşmadan önce dört kritik düzeltme katmanı gerektirmektedir:** (i) kritik sayısal hassasiyet ihlalleri (KISIM IX'da 18 ondalık AUC, H4 tablosunda 15 ondalık β), (ii) bulgular bölümü ile tartışma bölümü arasında H4 için iç tutarsızlık (gerçekte 3/4 yol anlamlı; tartışma "dört yol anlamlı" diyor), (iii) Tablo 1'de antidepresan/Beck/HbA1c satırlarının kesilmiş olması, (iv) "Talimatname Hard-No" gibi proje-içi disiplin terimlerinin CSR metninde sızması.

Aşağıda bulgular, **risk düzeyine göre** dört kategoride sıralanmıştır: 🔴 KRİTİK (savunma öncesi düzeltme zorunlu) · 🟠 YÜKSEK (metin disiplini) · 🟡 ORTA (cilalama) · 🟢 İYİ (övgü).

---

## 1 · CSR FORMATI VE KAPSAMI

### 🟢 İYİ

- **ICH E3 yapısı tam:** 20 ana bölüm + 2 Ek bölümü; gözlemsel-vaka-kontrol uyarlaması doğru kurulmuş.
- **Carbon Design System:** Tipografi, başlık hiyerarşisi, kod bloğu rendering, "Okuma notu" callout'ları profesyonel.
- **Audit-traceable referans:** Her tablo altında `Kaynak: outputs/tables/apa_t<NN>_*.csv · gösterilen satır: N · sütun: M` notu — bu, Talimatname §6.5 cross-ref disiplinine ve OSF reproducibility standardına tam uyum demek.
- **Ek F (sayfa 96-541):** "Tam Analiz Artefaktları, Tablo Atlası ve Veri Sınırı" — satır-düzeyi olmayan tüm CSV artefaktlarının tam tablo olarak verilmesi, satır-düzeyi skor veri setlerinin **mahremiyet sınırı** nedeniyle şema-only belgelenmesi: bu, KVKK + Talimatname §7.5 L0-L3 veri sınıflandırma matrisine **yapıcı bir uygulama**.
- **STROBE flow diagram (sayfa 26)**, **Causal DAG (gömülü figür 1)**, **H1 forest plot (sayfa 42)**, **H4 SEM yol diyagramı (sayfa 52)**, **H5 Bland-Altman grid (sayfa 55)**, **DCA net benefit eğrisi (sayfa 64)** — her biri gerçekten gömülü, profesyonel kalitede üretilmiş.

### 🟠 YÜKSEK — Format Sorunları

#### 1.1 "Okuma notu" tekrar gürültüsü
21 farklı bölümde aynı **"Bu bölüm kaynak CSR metninden eksiltilmeden dönüştürülmüş; varsa ilgili analiz tablosu, figür veya artefakt bloğu aynı bölüm bağlamına eklenmiştir."** cümlesi tekrarlamış. Carbon HTML şablonu her bölümün başına otomatik ekliyor görünüyor. Bu *meta-üretim notu*, bir kez giriş bölümünde verilse yeterlidir; her bölüm başına eklenmesi okurun dikkatini dağıtır ve CSR'ın profesyonel tonunu zayıflatır.

**Düzeltme:** Yalnız Bölüm 1 (Kapak) altına bir kez veya Önsöz bölümüne tek seferlik bir "üretim metodolojisi" notu olarak konulmalı; diğer 20 bölümden kaldırılmalı.

#### 1.2 Sayfa 41'de "11.1.2 Sonuçlar" başlığının altında **boş alan**
H1 birincil bulgu sayfasında alt-başlık veriliyor ama içerik bir sonraki sayfaya kaydırılmış; sayfa 41 alt yarısı boş. Bu Quarto/Paged.js sayfa kırılımı sorunu. Okur "veri eksik mi?" sorusuyla karşılaşır.

**Düzeltme:** `\Needspace{14\baselineskip}` veya CSS `page-break-after: avoid` ile başlık + ilk paragraf birlikte kalmalı.

#### 1.3 Tablo 1 sayfa 28-29 **duplikasyonu**
Sayfa 28'deki Tablo 1 "Aynı cinsiyet kardeş çifti: Farkli" satırına kadar gelip; sayfa 29'da **aynı tablo en baştan tekrar başlıyor**, yalnız son satıra ("Aynı cinsiyet kardeş çifti: Ayni") ulaşmak için. Bu, çok-sayfalı tabloların başlık satırının her sayfada tekrarı için Carbon şablonunun yarattığı yan etki olabilir, ama görsel olarak okuru "iki farklı tablo mu var?" tereddüdüne sokuyor.

**Düzeltme:** Tablo başlığı sadece ilk sayfada görünmeli; takip sayfalarında "Tablo 1 (devam)" üst-bilgisiyle yalnız sütun başlıkları tekrarlanmalı.

#### 1.4 Tablo 1 **ÖNEMLİ EKSİK**: anne antidepresan, Beck, HbA1c satırları kesilmiş
Sayfa 30'da tablo "Ev sahipligi: 1 / Ev oda sayisi / Araba sahipligi: 0" satırlarıyla bitiyor. Tablo altındaki not: **"gösterilen satır: 28 · sütun: 7"**. Yani CSV'de daha fazla satır var ama PDF'e 28'de cap yapılmış. Bu yüzden:

- **Anne antidepresan kullanımı (DM %29 vs Kontrol %9, SMD = 0.53)** — proje knowledge'taki **en güçlü dengesizlik** — Tablo 1'de yok!
- **Beck total ortalama, Beck şiddet kategorisi** — anne mental sağlık yükünün anchor'ı — yok!
- **Anne kronik hastalık varlığı** — yok!
- **DM klinik göstergeleri (HbA1c medyan 9.0%, tanı yaşı 7.8 yıl, DM süresi 3.9 yıl)** — yok!

Bu satırların yokluğu CSR'ın **klinik anchor değerini ciddi biçimde zayıflatır**; Bölüm 9.3 "DM Klinik Profili" alt-bölümünde HbA1c %32.5 tamamlama notu olsa da, ana Tablo 1'de antidepresan dengesizliği görünmediği için sonraki tartışma bölümünde "anne antidepresan dengesizliği" kavramına atıf yaparken okurun **geri dönüp doğrulayacağı sayısal anchor** eksik kalmaktadır.

**Düzeltme:** Carbon HTML şablonunda satır-cap'i 28'den 50'ye çıkarılmalı; alternatif olarak `apa_t01_sample_characteristics.csv` iki tabloya bölünmeli — Tablo 1A (sosyodemografi) + Tablo 1B (klinik + psikolojik göstergeler).

#### 1.5 19. bölüm başlık iddiası vs gerçeklik
"19 · TEMEL REFERANSLAR (160-180 ATIF HEDEFLİ references.bib ÖZETİ)" başlığı 160-180 atıf vaadediyor; ancak bölüm içinde **~30-40 referans** raporlanmış. Bu vaadi karşılayamayan bir başlık.

**Düzeltme:** Başlık "**Temel Referanslar (Çekirdek 30 Atıf, Tam Liste references.bib'te)**" olarak değiştirilmeli; veya tam BibTeX 19. bölüm sonuna ek olarak basılmalı.

---

## 2 · SAYISAL UYUM (PROJE ANALİZLERİ İLE TUTARLILIK)

### 🟢 İYİ — Doğru Raporlanan Anchor'lar

| Anchor | Project knowledge gerçeği | PDF değeri | Durum |
|---|---|---|---|
| H1 EMBU-C reddetme β | 0.16 SD, %95 GA [0.05, 0.26], pd = 0.999 | "β = 0.16 SD [0.05, 0.26], pd = 0.999" | ✅ Tam doğru |
| H1 reddetme BF₁₀ | 8.12 (Moderate H1) | BF₁₀ = 8.12 (moderate H1) | ✅ Tam doğru |
| H1 EMBU-C sıcaklık BF₁₀ | 0.29 (Moderate H0) | 0.29 | ✅ Doğru |
| H3 dört EMBU-P alt ölçek FDR p | > .50 | "FDR p > .50" | ✅ Doğru |
| H3 max SMD redüksiyonu (IPTW) | 0.220 → 0.004 | 0.220 → 0.004 (sayfa 27 dengeleme tablosunda) | ✅ Tam doğru |
| H3 ROPE içi pay reddetme | %92 | %92 | ✅ Doğru |
| H5 Olsen-Kenny latent r | Kontrol = 0.17, DM = 0.29 | 0.17 / 0.29 | ✅ Doğru |
| Tablo 1 anne yaşı SMD | 0.21 | 0.21 | ✅ Doğru |
| Multiverse %0 spec p<.05 | %0 | "%0 spec'te p < .05" | ✅ Doğru |
| Sensemakr RV_q | 0.04–0.08 | 0.04–0.08 | ✅ Doğru |
| E-değeri | 1.36–1.59 | 1.36–1.59 | ✅ Doğru |

### 🔴 KRİTİK — H4 İç Tutarsızlık

PDF içinde **iki farklı yer** H4 hakkında **çelişen** ifade kullanıyor:

**Sayfa 7 (Sinopsis tablosu) — DOĞRU:**
> "Anlamlı yollar için |std. β| = 0.28-0.33; aşırı koruma std. β = 0.08, FDR p = .216"

**Sayfa 52 (Bulgular Bölüm 11.4) — DOĞRU:**
> "Dört yapısal yoldan üçü FDR-düzeltmeli olarak istatistiksel anlamlıdır... Aşırı koruma yolu pozitif yöndedir ancak FDR p = .216 ile anlamlı değildir."

**Sayfa 82 (Tartışma Bölüm 15.4) — YANLIŞ:**
> "Bizim H4 SEM modelimiz... Dört yapısal yolun tümünün anlamlı olması (β = 0.30–0.36, p < .001), Goodman-Gotlib modelinin parenting bileşeninin Türk T1DM örnekleminde ampirik olarak doğrulanması demektir."

> "Bizim standardize yol katsayılarımız (β = 0.30–0.36) Lovejoy'un negatif davranış için raporladığı d = 0.40 değeriyle aynı büyüklük sınıfındadır."

**Tartışma bölümü, bulgu sayısının dördü değil üçü olduğunu kabul etmiyor.** `R/19_h4_beck_parenting_sem.R` ve `chapters/03_bulgular.qmd` belirgin olarak şöyle raporluyor:

| Yol | Standardize β | FDR p | Karar |
|---|---|---|---|
| Beck → Sıcaklık | -0.285 | < .001 | **Anlamlı** |
| Beck → Aşırı Koruma | **0.082** | **.216** | **ANLAMSIZ** |
| Beck → Reddetme | 0.329 | < .001 | **Anlamlı** |
| Beck → Karşılaştırma | 0.285 | < .001 | **Anlamlı** |

**Düzeltme zorunlu:** Tartışma 15.4.1 ve 15.4.2 yeniden yazılmalı:

> "Anne depresyon latent faktörü, EMBU-P sıcaklık (β = -0.29), reddetme (β = 0.33) ve karşılaştırma (β = 0.28) alt ölçeklerinin tümünde FDR-düzeltmeli olarak anlamlı yapısal yollar üretmiştir; aşırı koruma yolu yön olarak pozitif (β = 0.08) ancak FDR p = .216 ile anlamsız kalmıştır. Goodman-Gotlib (1999) modelinin parenting-aracılı transmisyon mekanizması, **dört alt boyutun üçünde** Türk T1DM örnekleminde ampirik olarak desteklenmiş; aşırı koruma boyutunda doğrulanmamıştır. Bu desen, anne depresif belirti yükünün ebeveynlik tutumlarındaki etkisinin alt-boyut-spesifik olduğunu — özellikle olumlu (sıcaklık), reddedici ve karşılaştırıcı boyutlarda işlerken aşırı koruma kanalında bağımsız mekanizmalardan beslendiğini — düşündürmektedir."

### 🟠 H4 standardize β Lovejoy karşılaştırması yanlış kalibrasyon
Tartışma "β = 0.30–0.36 ... Lovejoy'un d = 0.40 değeriyle aynı büyüklük sınıfındadır" diyor. Gerçekte **β = 0.28–0.33** aralığı + 1 anlamsız yol. Karşılaştırma cümlesi "**β = 0.28–0.33**, üç anlamlı yol Lovejoy'un (2000) negatif davranış meta-analitik d = 0.40 değerinin alt sınırı olan orta-büyük etki sınıfında konumlanmaktadır" şeklinde yeniden kalibre edilmeli.

### 🔴 KRİTİK — Sahte Hassasiyet İhlalleri (Hard-No #8 İhlali)

Talimatname §7.1 ve Hard-No #8: *"Cohen's d, ICC, η², ω, α: **2 ondalık + %95 CI**. Yüzdeler 1 ondalık. p-değerleri için < .001 eşiğinin altı < .001 yazılır; 'p = .000' yasaktır."*

**Sayfa 52, H4 Yapısal Yollar tablosu (Bölüm 11.4.3):**

| Yol | PDF (yanlış) | Olması gereken |
|---|---|---|
| Beck → Sıcaklık ham β | -0.298917388332773 | **-0.30** |
| Standardize β | -0.284500359785343 | **-0.28** |
| %95 GA | [-0.446011060023512, -0.151823716642035] | **[-0.45, -0.15]** |
| p-değeri | 0.0000680639580727949 | **< .001** |
| FDR p | 0.000136127916145**5** (sondaki "9" var) | **< .001** |
| Beck → Aşırı Koruma β | 0.0823291351574719 | **0.08** |
| FDR p | 0.215956575171397 | **.216** |

**Sayfa 64, KISIM IX Klinik Fayda metni:**

| Metrik | PDF (yanlış) | Olması gereken |
|---|---|---|
| Temel model AUC | 0.584702797202797 | **0.58** |
| Temel model AUC %95 GA | 0.501302101343267–0.668103493062327 | **[0.50, 0.67]** |
| Optimism-corrected AUC | 0.608974213286713 | **0.61** |
| Genişletilmiş AUC | 0.704020979020979 | **0.70** |
| Genişletilmiş AUC %95 GA | 0.625721179983667–0.782320778058291 | **[0.63, 0.78]** |
| Optimism-corrected AUC | 0.725101835664336 | **0.73** |
| Youden eşik | 0.222230536412307 | **0.22** |
| Sensitivite | 0.753846153846154 | **0.75** |
| Spesifite | 0.607954545454545 | **0.61** |
| PPV | 0.415254237288136 | **0.42** |
| NPV | 0.869918699186992 | **0.87** |

Bu **18 ondalıklı raporlama** Hard-No #8'in en ağır ihlali, APA 7 standardına aykırı, ve bir hakem heyetinin **görüldüğü an reddedeceği** bir form. Carbon HTML şablonu R `tidyverse::tibble` çıktısını ondalık truncation yapmadan basıyor görünüyor.

**Düzeltme:** Quarto chunk'larında `gt::fmt_number(decimals = 2)` veya `knitr::opts_chunk$set(digits = 2)` zorlamalı; tablo üreten R fonksiyonunda `format(x, digits = 2)` kullanılmalı. p-değerleri için `apa_fmt_p()` helper'ı uygulanmalı (`< .001` floor convention).

### 🟡 Türkçe terim tutarsızlığı
- "Çoçuk algısı" / "Çocuk algısı" tutarlı.
- "Dyadic" — Türkçesi "diadik" olarak kullanılmış; bu doğru (Talimatname §9 tutarlı).
- Ama bazı yerlerde "Diadik" başkasında "dyadic" karışık.
- "Multilevel" → bazı yerlerde "çok düzeyli" çevrilmiş, bazı yerlerde İngilizce kalmış. Tutarlılık gerekli.

---

## 3 · TABLOLAR VE GRAFİKLER

### 🟢 İYİ — Yüksek Kaliteli Görseller

- **Causal DAG figürü** (sayfa 24 dolayı): Yön okları, kovaryat sınıflandırması (backdoor / downstream / mediator), açıklayıcı not — DAG-justified ayarlama setinin görsel anchor'ı eksiksiz.
- **STROBE flow** (sayfa 26): Kanonik kilit → analitik aile tabanı → DM/Kontrol kolu → DM klinik alt-analiz akışı; örneklem akışı net.
- **H1 forest plot** (sayfa 42): Üç rol (Kontrol kardeş, DM indeks, DM kardeş) × dört EMBU-C alt ölçeği = 12 nokta tahmini + %95 GA çubukları; tablo ile tam tutarlı.
- **H4 SEM yol diyagramı** (sayfa 52): Renk skalası (kırmızı = negatif β, mavi = pozitif β), yıldız = FDR p < .05; aşırı koruma yolu açıkça yıldızsız (β = 0.08), bilgisel olarak doğru.
- **H5 Bland-Altman grid** (sayfa 55): 3 dyad-tipi (anne-indeks, anne-kardeş, indeks-kardeş) × 4 alt ölçek = 12 panel; %95 limits of agreement çizgili; profesyonel.
- **Klinik DCA eğrisi** (sayfa 64): Geniş risk skoru vs treat-all/treat-none; net benefit yorumu eşik 0.10–0.40 aralığında üstün.

### 🔴 KRİTİK — Tablo Veri Sınırı Sorunu

#### 3.1 Tablo 1 satır kesimi (yukarıda 1.4'te detaylandırıldı)
`apa_t01_sample_characteristics.csv` muhtemelen 35-40 satır içerirken PDF'e 28 satır basılmış. Anne antidepresan dengesizliği (SMD = 0.53) ve Beck total satırları **eksik**.

#### 3.2 Tablo 11 H3 sensitivity satır kesimi
"gösterilen satır: 20 · sütun: 7" — H3 sensitivite tablosu da 20 satırla cap. Antidepresan-stratified sonuçlar muhtemelen daha fazla strata içeriyordu.

### 🟠 YÜKSEK — Tablo Format Sorunları

#### 3.3 H4 yapısal yollar tablosu (sayfa 52)
Yukarıda detaylandırıldı: 15+ ondalık β değerleri, 18+ ondalık p-değerleri. APA standartlarına göre yeniden formatlanmalı. Önceki turdaki markdown'da hazırladığım gerçek değerler:

| Yol | β | %95 GA | p | FDR p |
|---|---|---|---|---|
| Beck → Sıcaklık | -0.28 | [-0.45, -0.15] | < .001 | < .001 |
| Beck → Aşırı Koruma | 0.08 | [-0.05, 0.24] | .216 | .216 |
| Beck → Reddetme | 0.33 | [0.19, 0.53] | < .001 | < .001 |
| Beck → Karşılaştırma | 0.28 | [0.14, 0.49] | < .001 | < .001 |

#### 3.4 Tablo 2 (kovaryat dengesi, sayfa 27)
**Sadece 3 satır** (age_gap, ses_latent, cocuk_sayisi). Talimatname §3.1 birincil ayarlama seti `{AgeGap; FamilySize; SES}` olduğundan bu tablo *tasarım gereği* 3 satırlıktır — ama tablo başlığı "**Kovaryat dengesi**" dendiği için okur "anne antidepresan, eğitim, vb. nerede?" diye sorabilir. Tablo başlığı **"Birincil DAG-justified ayarlama setinin SMD dengesi"** olmalı; "diğer kovaryatlar PS modelinde kontrol edilmiştir, ek detay Tablo 4 propensity model'de" notu eklenmeli.

### 🟡 ORTA — Olumsuz Boş Alan

- Sayfa 27: Tablo 2'nin altında %75 boş alan (1.4'te detaylandırıldı sayfa 30'da da var)
- Sayfa 41: H1 başlığının altında %50 boş alan
- Sayfa 51: H4 başlığının altında benzer

Bunlar tek tek bakıldığında küçük ama 541 sayfalık bir doküman için zaten boyut zorluğu oluşturur. Carbon HTML şablonunda `page-break-after: avoid` ile `Needspace` benzeri kontroller uygulanmalı.

---

## 4 · ANLATIM DÜZEYİ VE İSTATİSTİKSEL İZAHAT

### 🟢 İYİ

- **Bölüm 6 Giriş:** Pinquart 2013, De Los Reyes 2015, ISPAD 2024 / ADA 2025-2026 / NICE NG18 çerçevesi kapsamlı; akademik düzeye uygun.
- **Bölüm 8 Metodoloji:** Yapısal eksiklik kuralları (§8.5), kanonik kilit altı-adım doğrulama zinciri (§8.4), çoklu karşılaştırma disiplini (§8.7), DAG-justified ayarlama seti (§8.8) — istatistiksel disiplin tam belgelendirilmiş.
- **Bölüm 11 Birincil Bulgular:** Her hipotez için (i) birincil model formülü, (ii) sayısal sonuç, (iii) Bayesyen replikasyon, (iv) IRT GRM (H1) veya stratified sensitivity (H3) gibi triangülasyon adımları, (v) karar kutusu — yapı eğitsel ve şeffaf.
- **Bölüm 13 Robustluk:** Multiverse %0, TOST aşırı koruma + karşılaştırma "Equivalent", sensemakr RV_q ≤ 0.08, E-değer 1.36–1.59 — bu dört katmanın birlikte sunumu **ileri istatistik bilgi** seviyesi açısından örnek bir konstüksiyon.
- **Bölüm 15 Tartışma:** Her hipotez için (i) bağlamsallaştırma, (ii) multi-informant çerçevede yorum, (iii) DEVSTATS 7 uyarıcı ilke tarama izi, (iv) klinik implikasyon dört-katmanlı yapı — kuramsal derinlik yüksek.

### 🟠 YÜKSEK — Anlatım Sorunları

#### 4.1 İstatistiksel kavramların okur-tarafı izahatı eksik
ICH E3 CSR'lar genellikle **klinik-yöntem hibrit** okuyucu için yazılır (klinik araştırmacılar + biostatistikçiler + regülasyon kurulları). Bu CSR'da bazı kavramlar **doğrudan teknik adıyla** kullanılıyor, hiç açıklama olmadan:

- "Olsen-Kenny dyadic CFA" (sayfa 53) — bu çerçevenin neyi ölçtüğü, neden ICC'den farklı olduğu izah edilmemiş.
- "RSA Edwards-Parry yüzey eğriliği parametreleri (a1, a2, a3, a4)" (sayfa 54) — bu parametrelerin yorumu yok.
- "k-coefficient APIM" (sayfa 54) — Kenny k-katsayısının ne ölçtüğü açıklanmamış.
- "Robustness Value (RV_q)" (sayfa 71) — yorum kademesi (≤ 0.05 zayıf, 0.05-0.10 orta, ≥ 0.10 güçlü) verilmiş ama çoğunlukla okur Cinelli & Hazlett 2020'i bilmiyor olacaktır.

**Düzeltme önerisi:** Her bölümün başına 1-2 cümlelik **"Yöntem kutusu"** eklenmeli (psikometrik validasyon raporundaki gibi `\methodbox{}` Carbon stil kutuları). Örneğin H5 5.1 başına:

> **Yöntem kutusu:** Olsen-Kenny dyadic CFA, anne ve çocuğun aynı yapı (örneğin "ebeveyn sıcaklığı") hakkında verdikleri puanlar arasındaki latent korelasyonu hesaplar; ICC'den farkı, ölçüm hatasını latent yapıdan ayırarak "saf algı uyumunu" tahmin etmesidir. Latent r = 0.10–0.30 aralığı "düşük-orta non-bağımsızlık" olarak yorumlanır (Kenny ve diğerleri, 2006).

#### 4.2 Negatif bulgu epistemik şeffaflığı asimetrik
H3 için "üç-katmanlı negatif kanıt zinciri" (NHST + BF + TOST) güzel sunulmuş. Ancak H2 için aynı epistemik titizlik yok:

> "Dört SRQ alt ölçeğinde DM × Kontrol fark kanıtı **yetersiz**" (sayfa 47)

Bu, "Indeterminate" konumlanmasıyla bitirilmiş; ama H2 için **TOST eşdeğerlik testi yapılmadığı açıkça belirtilmemiş**. Talimatname §7.4 disiplini gereği, "kanıt yetersizliği ≠ aktif eşdeğerlik" cümlesi yalnız tartışmada (sayfa 80, 15.2.5) söylenmiş; bulgular bölümünde de açıkça belirtilmeli.

#### 4.3 H5 strateji uyumu kararı çelişkili
Sayfa 56 strateji 5 değerlendirmesi:
> "Strateji 1 (ICC + Bland-Altman), Strateji 4 (Olsen-Kenny) ve Strateji 5 (k-coefficient APIM) **uyumlu** olarak sonuçlanmış"

Ne var ki proje knowledge'tan gelen ICC değerleri Kontrol grubunda **0.03-0.20**, DM grubunda **-0.01-0.08** aralığında — yani **DM grubunda Kontrol'den DAHA DÜŞÜK ICC**. Bu, Olsen-Kenny latent korelasyonunun verdiği **DM > Kontrol** yönüyle **çelişir**. CSR'da bu ICC değerleri verilmemiş, yalnız "Bland-Altman ortalama farkı raporlanmıştır" deniyor. Bu, gerçek bulgu desenini gizleyen bir özetlemedir.

**Düzeltme zorunlu:** H5.5.2 stratejilerin uyum analizi yeniden yazılmalı:

> "Strateji 1 ICC[2,1] sonuçları Kontrol grubunda 0.03-0.20, DM grubunda -0.01-0.08 aralığında raporlanmış olup havuzlanmış ortalama 0.00-0.11 aralığında kalmıştır (Cicchetti 1994 'fakir-zayıf' uyum bandı). Strateji 4 Olsen-Kenny latent korelasyon sonuçları (Kontrol 0.17, DM 0.29) ICC'den **yön açısından farklılaşmaktadır**; bu fark, latent çerçevenin ölçüm hatasını ayırması ve manifest ICC'nin alt değerinde tuttuğu sinyali görünür kılmasıdır. Beş stratejinin tam uyum vermemesi, H5 bulgusunu 'güçlü' değil 'metodolojik triangülasyon ile zayıf-orta yön kanıtı' olarak konumlandırmamızı gerektirmektedir; Talimatname §1 Hard-No #11 'en az 3 strateji uyumlu' kuralı yön düzeyinde sağlanmış olsa da büyüklük düzeyinde stratejiler arası belirgin sapma vardır."

---

## 5 · CSR İLE UYUMLU OLMAYAN FAZLALIKLAR

### 🔴 KRİTİK — Proje-İçi Disiplin Terimleri CSR'a Sızmış

CSR profesyonel/regülasyon-uyumlu bir doküman olduğundan içinde **proje-içi yönetim referansları olmamalı**. Mevcut PDF'te aşağıdaki sızıntılar var:

- **"Talimatname §7.5":** sayfa 14, "Veri sınıflandırma matrisi (Talimatname §7.5)"
- **"Talimatname Hard-No #3":** sayfa 15, "yeniden tanımlama riskini sıfıra yaklaştırmak için kontrol-akışı Talimatname Hard-No #3 disipliniyle sürdürülmüştür"
- **"Talimatname §5: L1 t1dm-tez-rehberi × L2 psychdev × devstats × medical-research":** sayfa 16, araştırmacı yönetimi bölümü
- **"Talimatname Hard-No #9":** sayfa 22, "21 maddeden herhangi biri eksikse (Talimatname Hard-No #9)"
- **"Talimatname Hard-No #11":** sayfa 53, "H5 için beş paralel strateji zorunludur"
- **"Hard-No #8 (sahte hassasiyet yasağı), #11 (H5 5-strateji), §9 (nedensel dil yasağı) korunmuştur":** sayfa 95, CSR sonu

Bu terimler **proje-içi yönetim** disiplini için anlamlıdır; ancak hiçbir hakem, danışman veya regülasyon kurulu "Talimatname Hard-No #11" referansını anlamayacaktır. Bu terimler:

(i) Yöntem bölümü için **gerekçe olmadan iddia** olarak görünür.
(ii) CSR'ın **bağımsız belge** olma niteliğini bozar — okur, "Talimatname"i okumadan CSR'ı anlayamaz.
(iii) Akademik/regülasyon raporlama tonunu kırar.

**Düzeltme zorunlu:** Tüm "Talimatname" ve "Hard-No" referansları **kaldırılmalı**, yerlerine **doğrudan kuralın kendisi** yazılmalı:

| PDF'teki ifade | Düzeltme |
|---|---|
| "Veri sınıflandırma matrisi (Talimatname §7.5)" | "Veri sınıflandırma matrisi (L0 = açık metadata, L1 = de-identified analiz verisi, L2 = kaynak/ara veri, L3 = kimlik/credential)" |
| "Talimatname Hard-No #3 disipliniyle" | "veri minimizasyonu prensibiyle" |
| "21 maddeden herhangi biri eksikse (Talimatname Hard-No #9)" | "21 maddeden herhangi biri eksikse beck_total NA olarak işlenir; eksik-tolerans uygulanmaz" |
| "H5 için beş paralel strateji zorunludur (Hard-No #11)" | "Bu çalışmada H5 diadik tutarlılık analizi için beş paralel strateji uygulanmıştır; herhangi bir tek-strateji yorumunun metodolojik zafiyetlerini çapraz triangülasyonla ele almak amacıyla" |
| "Talimatname §5: L1 t1dm-tez-rehberi × L2 psychdev × devstats × medical-research × L3 legacy embu-data-audit × L4 Anthropic varsayılan" | **Tamamen kaldırılmalı**; bu skill orkestrasyon detayı CSR'a uygun değil |
| "Hard-No #8, #11, §9 korunmuştur" | "APA 7 raporlama standardı, çoklu strateji disiplini ve nedensel dil sınırlama kuralları korunmuştur" |

### 🟠 YÜKSEK — Üretim/Build Meta-Yorumları

#### 5.1 PDF sonu üretim notları
Sayfa 95 (CSR sonu):

> "**Çıktı yeri:** outputs/quarto/T1DM_EBEVEYN_CSR_v1.md
> **Render hedefi:** quarto render T1DM_EBEVEYN_CSR_v1.md --to pdf (Carbon HTML şablonu ile)
> **Üretim disiplini:** Talimatname §6.2 Quarto chunk standartları + §7 raporlama standartları..."

Bu **build/render meta-yorumu** CSR içinde **olmamalı**. Render komutu repo README'sinde olur, CSR son sayfasında değil. Bu sızıntı PDF'in "ön-versiyon, henüz cilalanmamış" izlenimi yaratıyor.

**Düzeltme:** Tamamen kaldırılmalı.

#### 5.2 Versiyon kontrol bilgisi gereksiz CSR detayı
Bölüm 1 kapak tablosunda:

> "Veri kilidi tarihi: 26 Nisan 2026"
> "Analitik kilit: data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock (SHA-256 mührü)"

Bu, OSF reproducibility belgeleri için gereklidir, ancak CSR'ın **kapak tablosunda** olması gerekmiyor. Daha uygun yer: Bölüm 8.4 "Veri Yönetimi ve Kanonik Kilit" içinde tek bir teknik referans paragrafı. Kapak tablosunda yalnız "Çalışma protokolü, KAEK onay, PI, danışman" bilgileri kalmalı.

#### 5.3 SAP versiyon, OSF kayıtları kapak tablosunda fazla detay
"SAP sürümü: v3.0 — DEFİNİTİF FİNAL" ve "OSF kayıtları: Layer 1 d524q (...) Layer 2 pytfe (...)" — **kapakta detay seviyesi çok yüksek**. Bu bilgiler:

(i) Bölüm 4.4 "Pre-Registration Disiplini" altında zaten var.
(ii) Kapak tablosunu görsel olarak ağırlaştırıyor.

**Düzeltme:** Kapak tablosundan SAP/OSF satırları çıkarılmalı; yalnız Bölüm 4.4'te kalmalı.

### 🟡 ORTA — Tekrar Eden İçerik

#### 5.4 Sinopsis ile Bölüm 11 arasında %30 örtüşme
Sinopsis 2.4 bulgu tablosu, Bölüm 11 başında her hipotez için tekrar açıklanıyor. Bu, ICH E3 normu için kabul edilebilirdir (sinopsis bağımsız okunabilir olmalı), ancak bazı paragraflar **kelime-kelime aynı**. Sinopsis daha **tablo-yoğun + kısa** olmalı; ayrıntı bulgular bölümüne bırakılmalı.

#### 5.5 KISIM XII Bayesyen Bölüm 14 ile sinopsis 2.4 örtüşmesi
Sinopsis tablosu BF₁₀ değerlerini veriyor; Bölüm 14 aynı tabloyu **birebir** tekrar veriyor. Bölüm 14 daha **diagnostik-yoğun** (R̂, ESS, divergent) olmalı; BF₁₀ özet tablosu sinopsis'e bırakılmalı veya cross-reference edilmeli.

---

## 6 · ÖZET BULGU TABLOSU (RİSK SIRALI)

| # | Risk | Bulgu | Konum | Düzeltme |
|---|---|---|---|---|
| 1 | 🔴 KRİTİK | H4 tartışma "dört yapısal yol anlamlı" — bulgular "üç anlamlı, biri (aşırı koruma) anlamsız" | Sayfa 82, Bölüm 15.4.1, 15.4.2 | Tartışma metni yeniden yazılmalı |
| 2 | 🔴 KRİTİK | H4 tablosu 15+ ondalık β, 18+ ondalık p | Sayfa 52, Tablo 11.4.3 | `gt::fmt_number(decimals=2)` + `apa_fmt_p()` zorlamalı |
| 3 | 🔴 KRİTİK | KISIM IX AUC, sensitivite, spesifite 18 ondalık | Sayfa 64, Bölüm 12.4.2 | Aynı format düzeltmesi |
| 4 | 🔴 KRİTİK | Tablo 1'de antidepresan (SMD = 0.53), Beck total, HbA1c satırları kesilmiş | Sayfa 28-30 | Satır cap'i artırılmalı veya Tablo 1A/1B böl |
| 5 | 🔴 KRİTİK | "Talimatname §X / Hard-No #N" terimleri CSR'a sızmış (5+ yerde) | Sayfa 14, 15, 16, 22, 53, 95 | Doğrudan kural metnine çevrilmeli |
| 6 | 🟠 YÜKSEK | H5 strateji uyumu kararı ICC ile Olsen-Kenny çelişkisini gizliyor | Sayfa 56 | ICC 0.03-0.20 değerleri açıkça raporlanmalı |
| 7 | 🟠 YÜKSEK | "Bu bölüm kaynak CSR metninden eksiltilmeden..." cümlesi 21 kez tekrar | Tüm bölüm başlangıçları | Yalnız Bölüm 1'de tutulmalı |
| 8 | 🟠 YÜKSEK | Build/render meta-notu CSR sonunda | Sayfa 95 | Tamamen kaldırılmalı |
| 9 | 🟠 YÜKSEK | İstatistiksel kavramlar için yöntem kutusu yok (RSA, k-coef, Olsen-Kenny, RV_q) | Bölüm 11.5, 13.3 | `\methodbox{}` Carbon kutuları eklenmeli |
| 10 | 🟠 YÜKSEK | Sayfa 41, 51 vb. boş alanlar (başlık + içerik ayrılmış) | Birden çok yer | CSS page-break / Needspace düzeltilmeli |
| 11 | 🟡 ORTA | Tablo 1 sayfa 28-29 duplikasyonu | Sayfa 28-29 | Çok-sayfalı tablo başlığı tek sefer |
| 12 | 🟡 ORTA | "160-180 atıf hedefli" başlık vs ~30 referans | Bölüm 19 | Başlık değişmeli ya da tam liste eklemeli |
| 13 | 🟡 ORTA | Tablo 2 başlığı "kovaryat dengesi" yanıltıcı (sadece 3 değişken) | Sayfa 27 | "Birincil DAG-justified ayarlama setinin SMD dengesi" yapılmalı |
| 14 | 🟡 ORTA | Sinopsis ↔ Bölüm 14 Bayesyen tablosu birebir tekrar | Sayfa 7 + 75 | Cross-reference yapılmalı |
| 15 | 🟡 ORTA | "Multilevel" / "çok düzeyli" Türkçe-İngilizce karışık | Çeşitli | Tutarlılık |
| 16 | 🟡 ORTA | H2 negatif bulgu için "TOST yapılmadı" şeffaflığı bulgular bölümünde değil tartışmada | Sayfa 47 | Bulgular bölümüne taşınmalı |
| 17 | 🟢 ÖVGÜ | 22 bölüm + 25 gömülü figür + 238 CSV ref + Carbon design + audit-traceable kaynak — **kapsam yapısı çok güçlü** | Genel | — |
| 18 | 🟢 ÖVGÜ | DAG, STROBE flow, H1 forest, H4 SEM diagram, H5 Bland-Altman, DCA — **profesyonel görsel kalite** | Çeşitli | — |

---

## 7 · DÜZELTİLMİŞ V1.1 İÇİN İŞ AKIŞI ÖNERİSİ

CSR'i savunma sürümüne (v1.1) taşımak için aşağıdaki sıra önerilir:

### Sprint A — Kritik düzeltmeler (8-10 saat)
1. **H4 tartışma metnini yeniden yaz** (sayfa 82, Bölüm 15.4.1-15.4.2): "dört yol" → "üç anlamlı + bir anlamsız (aşırı koruma)" düzeltmesi.
2. **R sayısal format düzeltmesi:** `R/29_apa_tables.R` veya `R/30_thesis_mapping.R` içinde `apa_fmt_num()`, `apa_fmt_p()` ve `apa_fmt_ci()` helper'ları **tüm** APA tabloları için tutarlı uygulanmalı; tablo üretim chunk'larında `digits = 2` zorlama.
3. **Tablo 1 yeniden üretimi:** `R/13_table1_smd.R` → `apa_t01_sample_characteristics.csv` satır limiti 50'ye çıkarılmalı; alternatif olarak Tablo 1A (sosyodemografi) + Tablo 1B (klinik) ikiliye ayrılmalı.
4. **"Talimatname / Hard-No" metin sızıntıları:** Tüm CSR markdown kaynağında `grep "Talimatname\|Hard-No"` çalıştırılıp her birine **content rewrite** yapılmalı.

### Sprint B — Anlatım disiplini (4-6 saat)
5. **"Okuma notu" boilerplate:** Carbon HTML şablonunda `{{ if first_section }}` koşulu ile yalnız Bölüm 1'de basılması.
6. **Yöntem kutuları:** Olsen-Kenny, RSA, k-coefficient, RV_q için `\methodbox{}` Carbon stil kutuları (psikometrik validasyon raporundan örnek alınarak).
7. **H5 strateji uyumu:** ICC değerleri açıkça raporlanıp Olsen-Kenny ile farkı tartışılmalı.

### Sprint C — Cilalama (2-3 saat)
8. **Sayfa break düzeltmeleri**, **tablo duplikasyon temizliği**, **sinopsis ↔ Bölüm 14 cross-reference**, **Türkçe terim tutarlılığı**.
9. **CSR sonu meta-yorumu** kaldırılmalı.
10. **Bölüm 19 referans listesi** ya başlığı değişmeli ya tam BibTeX eklenmeli.

### Sprint D — QC ve final render (1-2 saat)
11. Tam pipeline: `Rscript scripts/R/29_apa_tables.R` → `quarto render T1DM_EBEVEYN_CSR_v1.qmd --to pdf` → manuel sayfa-sayfa görsel inceleme.
12. PDF metadata güncellenmesi (creation date, version, author).

**Toplam tahminî efor: 15-21 saat.**

---

## 8 · SONUÇ

**Mevcut PDF, kapsam ve görsel kalite olarak savunma için kullanılabilir bir taban sunuyor; ancak yukarıdaki dört kritik düzeltme (H4 tartışma tutarsızlığı, sayısal hassasiyet ihlalleri, Tablo 1 satır kesimi, proje-içi terim sızıntıları) yapılmadan akademik bir savunma jürisinin önüne çıkarılması ciddi risk taşır.**

Sprint A tamamlandığında PDF, doktora savunması için tam hazır olacaktır. Sprint B + C + D yayın çıktıları (Pediatric Diabetes adaptasyon makalesi, J Pediatric Psychology H1 + H5 makalesi) için ek değer üretecek; ancak savunma ön-koşulu olarak Sprint A yeterlidir.

İçerik olarak güçlü; biçim olarak titiz son cila gerektiren bir CSR.
