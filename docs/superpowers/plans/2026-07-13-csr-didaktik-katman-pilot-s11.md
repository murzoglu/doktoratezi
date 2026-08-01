# CSR Didaktik Açıklama Katmanı — Pilot §11 Uygulama Planı

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** CSR §11 (Birincil Hipotez Bulguları, H1–H5) içindeki her istatistik tekniğine 3-parçalı etiketli mini-blok (Bilimsel soru → Yöntem & tatbik → Nasıl değerlendirilir) ekleyerek pilot uygulamayı tamamlamak.

**Architecture:** `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` in-place düzenlenir. Her teknik başlığının hemen altına, ilgili R-chunk/sonuç bloğundan ÖNCE bir mini-blok eklenir. Mevcut `> Yöntem kutusu` blockquote'ları mini-bloğun "Yöntem & tatbik" parçasına dönüştürülür. Bölüm-sonu `Karar Kutusu` blokları (verdict) DEĞİŞMEDEN kalır. Hiçbir R-chunk literali veya mevcut istatistik değeri değiştirilmez.

**Tech Stack:** Quarto (.qmd), Türkçe Marmara format sözleşmesi, sci-audit (axis G/A/B), galileo advisory, `references/references.bib` (mevcut atıflar).

## Global Constraints

Her task'ın gereksinimleri bu bölümü örtük içerir (kaynak: `docs/superpowers/specs/2026-07-13-csr-didaktik-aciklama-katmani-design.md`):

- **Format:** Türkçe edilgen 3. tekil; ondalık **virgül** (`p<0,001`, `β=0,16`); mini-blok **başlık değil** `**bold**` etiket (başlık kaskadı ≤4 bozulmaz).
- **R-literal koruması:** ` ```{r ` … ` ``` ` blokları **byte-düzeyinde değişmez**. Yalnız blok DIŞINA düzyazı eklenir.
- **Kanonik sayı koruması:** hiçbir mevcut istatistik değeri, β, GA, BF, p, verdict değiştirilmez.
- **Yinelenme yok:** mini-blok parça 3 = a-priori ÖLÇÜT; bölüm-sonu `Karar Kutusu` = VERDICT (dokunulmaz). Bulgu sayıları mini-blokta tekrar edilmez.
- **Atıf:** yalnız §11'de ZATEN geçen künyeler + `references/references.bib` yeniden kullanılır. Yeni künye gerekirse metne girmeden önce `/referans-kapisi`; uydurma yasağı mutlak.
- **Veri sınırı:** yalnız aggregate; satır/PII yok.
- **Nedensellik:** kesitsel → ilişkisel/betimsel dil; nedensel dil yok. Keşifsel analizde `[KEŞİFSEL]` korunur.
- **Anchor kuralı:** düzenleme yukarıdan aşağıya; executor **metin-çapalı** Edit kullanır (satır no değil — edit'ler alt çapaları kaydırır).

---

### Task 0: Çalışma-ağacı baseline'ı

**Files:**
- Modify (yalnız değerlendirme): `docs/CLINICAL-STUDY-REPORT-FINAL.qmd`

**Interfaces:**
- Produces: temiz baseline + R-chunk imza (`N_CHUNKS`, `CHUNK_HASH`) — sonraki tüm task'ların literal-koruma testi bu imzaya karşı yürür.

- [ ] **Step 1: Pre-existing CSR diff'ini kullanıcıya sun**

CSR.qmd oturum öncesi zaten `M` (132 ins / 106 del). Bu ÖNCEKİ iştir. Executor kullanıcıya sorar: (a) bu önceki değişiklikleri ayrı bir "baseline" commit'i yap, sonra pilot temiz üstüne binsin; (b) pilotla bundle et. Onay alınmadan pilot commit'i atılmaz.

Run: `git diff --stat -- docs/CLINICAL-STUDY-REPORT-FINAL.qmd`
Expected: pre-existing diff görünür; kullanıcı (a) veya (b) seçer.

- [ ] **Step 2: R-chunk imzasını kaydet (baseline)**

```bash
python3 - <<'PY'
import re, hashlib
t = open("docs/CLINICAL-STUDY-REPORT-FINAL.qmd", encoding="utf-8").read()
blocks = re.findall(r'^```\{r.*?^```', t, re.M | re.S)
print("N_CHUNKS =", len(blocks))
print("CHUNK_HASH =", hashlib.md5("".join(blocks).encode()).hexdigest())
PY
```
Expected: `N_CHUNKS = 60` (veya güncel sayı) + bir hash. Bu iki değer NOT EDİLİR; her task sonunda değişmemeli.

- [ ] **Step 3: Commit (yalnız (a) seçilirse — baseline)**

```bash
git add docs/CLINICAL-STUDY-REPORT-FINAL.qmd
git commit -m "chore(csr): pilot öncesi CSR baseline (önceki commit'siz iş)"
```

---

### Task 1: H1 mini-blokları (§11.1 — çocuk algısı)

**Files:**
- Modify: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` (§11.1, ~4 teknik)

**Interfaces:**
- Consumes: Task 0 `CHUNK_HASH`.
- Produces: H1'de 4 mini-blok; §11.1.5 Karar Kutusu değişmez.

- [ ] **Step 1: 11.1 birincil (çok düzeyli model+ICC) — mevcut `> Yöntem kutusu`'nu mini-bloğa dönüştür**

Çapa: `## 11.1 H1 — Çocuk Algısı (EMBU-C × Dört Alt Ölçek)` başlığının hemen altındaki `> **Yöntem kutusu — Çok düzeyli model...` blockquote'unun TAMAMINI şununla değiştir:

```markdown
**Bilimsel soru.** Tip 1 diyabet tanısı ve aile-içi rol (indeks çocuk / kardeş), çocuğun algıladığı ebeveyn tutumu boyutlarını (EMBU-C sıcaklık, aşırı koruma, reddetme, karşılaştırma) yorduyor mu? Örneklem 482 çocuk = 241 aile × 2 gözlemden oluştuğundan (kaynak: veri haritası, `docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md`) aynı aileden gelen iki gözlem istatistiksel olarak bağımsız değildir; soru aile-içi bağımlılığı hesaba katan bir çerçeve gerektirir.

**Yöntem & tatbik.** Her alt ölçek için rastgele aile-kesişimli çok düzeyli kovaryans analizi (`lme4`) kestirilmiştir. Sınıf-içi korelasyon (ICC), aile-içi benzerliğin toplam değişkenliğe oranıdır; ihmal edilirse standart hatalar küçük tahmin edilir ve yanlış-pozitif riski artar — bu nedenle aile rastgele kesişimi zorunludur. Sabit etkiler: dört düzeyli rol (`role_f`, ref. Kontrol-İndeks), çocuk yaşı, cinsiyet, latent SES, kardeş yaş farkı ve aile çocuk sayısı; çoklu karşılaştırma FDR ile düzeltilmiştir.

**Nasıl değerlendirilir.** Sonuç "p<0,05" ile değil, standardize β + %95 güven aralığının sıfırdan ayrık olup olmadığı ve etki büyüklüğünün mertebesiyle okunur. Küçük etkiler bağlama bağlı ve birikimli anlam taşıyabilir (Funder ve Ozer, 2019; Schäfer ve Schwarz, 2019); büyüklük Pinquart'ın (2013) kronik hastalık ailelerinde bildirdiği özet değerle kalibre edilir. Kesitsel tasarım nedeniyle yorum ilişkiseldir, nedensel değildir.
```

- [ ] **Step 2: 11.1.2 Bayesçi katman — kompakt mini-blok ekle**

Çapa: `### 11.1.2 Bayesçi paralel kanıt katmanı` başlığının hemen ALTINA (sonraki paragraftan önce) ekle:

```markdown
**Bilimsel soru.** Klasik anlamlılık, "etki yok" ile "kanıt yetersiz"i ayırmaz; H1 sinyali sıfır-hipoteze karşı ne kadar destek taşıyor?

**Yöntem & tatbik.** Aynı model brms ile Bayesçi kestirimle tekrarlanır; posterior medyan β, %95 güvenilir aralık, yön olasılığı (pd) ve Savage-Dickey Bayes faktörü (BF₁₀) raporlanır (prior türetimi ön-kayıt anında Pinquart-temelli; bkz. `references/bayesci-paralel-hat.md`).

**Nasıl değerlendirilir.** BF₁₀ > 3 H1 lehine, < 1/3 H0 lehine orta düzey kanıttır (Jeffreys ölçeği); güvenilir aralığın sıfırı içerip içermemesi klasik GA ile üçgenlenir.
```

- [ ] **Step 3: 11.1.3 IRT GRM — kompakt mini-blok ekle**

Çapa: `### 11.1.3 Madde-yanıt teorisi doğrulaması` başlığının hemen ALTINA ekle:

```markdown
**Bilimsel soru.** Reddetme bulgusu, ölçeğin madde havuzundaki taban etkilerinden mi kaynaklanıyor yoksa latent yapı düzeyinde de duruyor mu?

**Yöntem & tatbik.** Reddetme alt ölçeği Samejima graded response modeliyle (IRT GRM) latent θ skoruna dönüştürülür; grup farkı θ düzleminde yeniden kestirilir. IRT, ölçek-toplamı yerine madde-bilgi fonksiyonlarını kullanarak taban/tavan etkilerine karşı dayanıklıdır.

**Nasıl değerlendirilir.** Latent θ farkının ölçek-düzeyi etkinin büyük bölümünü koruması, bulgunun ölçüm artefaktı olmadığının kanıtıdır (yakınlık ne kadar yüksekse o kadar sağlam).
```

- [ ] **Step 4: 11.1.4 Üçlü etkileşim — kompakt mini-blok ekle**

Çapa: `### 11.1.4 Üçlü etkileşim (yaş × cinsiyet × rol)` başlığının hemen ALTINA ekle:

```markdown
**Bilimsel soru.** Reddetme bulgusu tüm alt gruplarda mı geçerli, yoksa belirli yaş/cinsiyet kesimlerine mi özgü (Simpson-tipi maskeleme)?

**Yöntem & tatbik.** Modele rol × yaş × cinsiyet üçlü etkileşimi eklenerek FDR-düzeltilmiş olarak sınanır; bu, ana etkinin alt-grup homojenliğini denetler.

**Nasıl değerlendirilir.** Etkileşimin anlamlı çıkmaması, ana bulgunun alt gruplar arası homojen (genellenebilir) olduğunu destekler; anlamlı çıkması ana etkinin koşullu yorumlanmasını gerektirir.
```

- [ ] **Step 5: R-literal + yapı doğrula**

```bash
python3 - <<'PY'
import re, hashlib
t = open("docs/CLINICAL-STUDY-REPORT-FINAL.qmd", encoding="utf-8").read()
b = re.findall(r'^```\{r.*?^```', t, re.M | re.S)
print("N_CHUNKS =", len(b), "CHUNK_HASH =", hashlib.md5("".join(b).encode()).hexdigest())
PY
git diff docs/CLINICAL-STUDY-REPORT-FINAL.qmd | grep -E '^\+' | grep -c '\*\*Bilimsel soru\.\*\*'
```
Expected: `N_CHUNKS`/`CHUNK_HASH` Task 0 baseline ile AYNI (R literalleri değişmedi); "Bilimsel soru." sayısı = 4.

- [ ] **Step 6: Commit**

```bash
git add docs/CLINICAL-STUDY-REPORT-FINAL.qmd
git commit -m "docs(csr): §11.1 H1 didaktik mini-bloklar (çok düzeyli/Bayesçi/IRT/etkileşim)"
```

---

### Task 2: H2 mini-blokları (§11.2 — kardeş ilişkisi)

**Files:**
- Modify: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` (§11.2, 3 teknik)

**Interfaces:**
- Consumes: Task 0 `CHUNK_HASH`. Produces: H2'de 3 mini-blok; §11.2.4 Karar Kutusu değişmez.

- [ ] **Step 1: 11.2 APIM birincil — `> Yöntem kutusu`'nu mini-bloğa dönüştür**

Çapa: `## 11.2 H2 …` altındaki `> **Yöntem kutusu — Aktör-partner...` blockquote'unu şununla değiştir:

```markdown
**Bilimsel soru.** T1DM kardeş çiftlerinin ilişki değerlendirmeleri (KİA/SRQ: sıcaklık, statü, çatışma, rekabet) Kontrol'den farklı mı? İki kardeşin raporu karşılıklı bağımlı olduğundan soru, düad-içi bağımlılığı çözen bir çerçeve ister.

**Yöntem & tatbik.** Aktör-partner bağımlılık modeli (APIM) her çocuğun raporunu hem kendi (aktör) hem kardeşinin (partner) özelliklerinden gelen etkiye ayırır; sıradan regresyon bu bağımlılığı yok sayarak yanlı sonuç verir. Üç paralel strateji kullanılır: aile-ortalama Welch d, APIM grup × rol etkisi ve aile-içi FDR.

**Nasıl değerlendirilir.** Etki büyüklüğü (Hedges g) + %95 GA ve ±0,20 SD önemsizlik bandı birlikte okunur; üç stratejinin yön birliği aranır. Fark bulunamaması "fark yoktur" değil, "fark için kanıt yetersiz" olarak yorumlanır (aktif eşdeğerlik ayrı test ister; Lakens, 2017).
```

- [ ] **Step 2: 11.2.1 Olsen-Kenny düad CFA — kompakt mini-blok ekle**

Çapa: `### 11.2.1 Üç paralel strateji ile birincil bulgular` başlığının hemen ALTINA ekle:

```markdown
**Bilimsel soru.** Kardeşlerin çatışma/ilişki değerlendirmelerinin ortak latent yapısı ve indeks–kardeş uyumu nedir?

**Yöntem & tatbik.** Olsen-Kenny ayırt edilebilir (distinguishable) düad doğrulayıcı faktör analizi, indeks ve kardeş rollerini ayrı ama bağlı latent değişkenler olarak modelleyip gerçek latent korelasyonu (ölçüm hatasından arındırılmış) verir.

**Nasıl değerlendirilir.** Model yakınsaması + kabul edilebilir uyum altında latent r büyüklüğü, düad-içi ortak algının gücünü betimler (yön kanıtı değil, yapı betimlemesi).
```

- [ ] **Step 3: 11.2.3 TOST (uygulanmadı) — kompakt mini-blok ekle**

Çapa: `### 11.2.3 Eşdeğerlik testi durumu` başlığının hemen ALTINA ekle:

```markdown
**Bilimsel soru.** "Fark yok" sonucu, gerçek eşdeğerlik kanıtı mı yoksa yalnızca kanıt yetersizliği mi?

**Yöntem & tatbik.** İki-tek-yanlı test (TOST) prosedürü, etkiyi önceden tanımlı bir SESOI bandı içinde tutarak aktif eşdeğerlik sınar. H2 ailesinde TOST ön-kayıtlı planda bulunmadığından **uygulanmamıştır**; bu şeffaflık kararı burada açıkça belirtilir.

**Nasıl değerlendirilir.** TOST yokluğunda sonuç "indeterminate" (kanıt yetersiz) olarak raporlanır; "eşdeğer/korunmuş" iddiası edilmez (epistemik ayrım; Lakens, 2017).
```

- [ ] **Step 4: R-literal + yapı doğrula**

```bash
python3 - <<'PY'
import re, hashlib
t = open("docs/CLINICAL-STUDY-REPORT-FINAL.qmd", encoding="utf-8").read()
b = re.findall(r'^```\{r.*?^```', t, re.M | re.S)
print("CHUNK_HASH =", hashlib.md5("".join(b).encode()).hexdigest())
PY
```
Expected: `CHUNK_HASH` baseline ile AYNI.

- [ ] **Step 5: Commit**

```bash
git add docs/CLINICAL-STUDY-REPORT-FINAL.qmd
git commit -m "docs(csr): §11.2 H2 didaktik mini-bloklar (APIM/düad CFA/TOST-durumu)"
```

---

### Task 3: H3 mini-blokları (§11.3 — anne öz-bildirimi)

**Files:**
- Modify: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` (§11.3, 4 teknik)

**Interfaces:**
- Consumes: Task 0 `CHUNK_HASH`. Produces: H3'te 4 mini-blok; §11.3.6 Karar Kutusu değişmez.

- [ ] **Step 1: 11.3 IPTW ANCOVA birincil — `> Yöntem kutusu`'nu mini-bloğa dönüştür**

Çapa: `## 11.3 H3 …` altındaki `> **Yöntem kutusu — Eğilim skoru...` blockquote'unu şununla değiştir:

```markdown
**Bilimsel soru.** T1DM anneleri, kendi bildirdikleri ebeveynlik tutumlarında (EMBU-P dört alt ölçek) Kontrol annelerinden sistematik olarak farklı mı? Grup ataması rastgele olmadığından soru, gözlenen sosyodemografik dengesizliği düzelten bir çerçeve gerektirir.

**Yöntem & tatbik.** Birincil kovaryans analizinin yanında eğilim skoru + ters-olasılık ağırlıklandırması (IPTW) kullanılır: eğilim skoru gözlenen kovaryatlardan grup üyeliği olasılığını kestirir, IPTW bu skorla ağırlıklandırarak grupları ölçülen değişkenlerde dengeler. Stabilize + 99. persentilde trim'li ağırlıklar ve heteroskedastisite-tutarlı standart hata uygulanır. IPTW ölçülmemiş karıştırıcıları gideremez — bu yüzden duyarlılık analizleriyle birlikte okunur.

**Nasıl değerlendirilir.** Ham β + %95 GA ile standardize etki büyüklüğü birlikte; birincil ANCOVA ile IPTW sonuçlarının yön ve büyüklük olarak örtüşmesi bulgunun modele-duyarsız (dayanıklı) olduğunu gösterir.
```

- [ ] **Step 2: 11.3.3 antidepresan-katmanlı duyarlılık — kompakt mini-blok ekle**

Çapa: `### 11.3.3 Antidepresan-katmanlı duyarlılık analizleri` başlığının hemen ALTINA ekle:

```markdown
**Bilimsel soru.** Gruplar arası antidepresan kullanım dengesizliği (Tablo 1C), EMBU-P grup karşılaştırmasını maskeliyor olabilir mi?

**Yöntem & tatbik.** Analiz, antidepresan kullanan ve kullanmayan annelere ayrı strata içinde tekrarlanır ve antidepresan durumu kovaryata eklenir; bu, potansiyel karıştırıcının etkisini izole eder.

**Nasıl değerlendirilir.** Stratifiye ve tam-örneklem sonuçların yön/büyüklük olarak farklılaşmaması, dengesizliğin bulguyu çarpıtmadığını doğrular.
```

- [ ] **Step 3: 11.3.4 Bayesçi ROPE/BF — kompakt mini-blok ekle**

Çapa: `### 11.3.4 Bayesçi paralel kanıt katmanı` başlığının hemen ALTINA ekle:

```markdown
**Bilimsel soru.** Negatif sonuç gerçek bir "fark yok" kanıtı mı, yoksa yalnız güç yetersizliği mi?

**Yöntem & tatbik.** Her alt ölçek için BF₁₀ ve pratik-eşdeğerlik bölgesi (ROPE) içindeki posterior payı hesaplanır; ROPE, etkiyi önemsiz kabul edilen bir bant içinde tutar.

**Nasıl değerlendirilir.** BF₁₀ < 1/3 H0 lehine orta kanıt; yüksek ROPE-içi pay (ör. reddetmede yüksek oran) sıfıra-yakınlığı etkin biçimde destekler ve sonucu salt güç açıklamasından uzaklaştırır.
```

- [ ] **Step 4: 11.3.5 TOST eşdeğerlik — kompakt mini-blok ekle**

Çapa: `### 11.3.5 Eşdeğerlik testi sonuçları` başlığının hemen ALTINA ekle:

```markdown
**Bilimsel soru.** Hangi alt ölçeklerde etki, önceden tanımlı önemsizlik bandı (±0,30 SD) içinde kesin biçimde eşdeğerdir?

**Yöntem & tatbik.** TOST, iki tek-yanlı testi birleştirerek etkinin ±SESOI sınırları içinde kaldığını aktif olarak sınar; H2'den farklı olarak burada ön-kayıtlı olduğundan uygulanır.

**Nasıl değerlendirilir.** "Equivalent" kararı aktif sıfır kanıtı; "indeterminate" ne fark ne eşdeğerlik. Böylece negatif bulgu "kanıt yetersiz" ve "kesin eşdeğer" olarak ayrıştırılır.
```

- [ ] **Step 5: R-literal doğrula + Commit**

```bash
python3 - <<'PY'
import re, hashlib
t = open("docs/CLINICAL-STUDY-REPORT-FINAL.qmd", encoding="utf-8").read()
b = re.findall(r'^```\{r.*?^```', t, re.M | re.S)
print("CHUNK_HASH =", hashlib.md5("".join(b).encode()).hexdigest())
PY
git add docs/CLINICAL-STUDY-REPORT-FINAL.qmd
git commit -m "docs(csr): §11.3 H3 didaktik mini-bloklar (IPTW/strata/Bayesçi ROPE/TOST)"
```
Expected: `CHUNK_HASH` baseline ile AYNI, sonra commit.

---

### Task 4: H4 mini-blokları (§11.4 — anne depresyonu → EMBU-P SEM)

**Files:**
- Modify: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` (§11.4, 2 teknik — **kutu eksik, eklenir**)

**Interfaces:**
- Consumes: Task 0 `CHUNK_HASH`. Produces: H4'te 2 mini-blok; §11.4.4 Karar Kutusu değişmez. Not: H4'te mevcut `> Yöntem kutusu` YOKTUR — sıfırdan eklenir.

- [ ] **Step 1: 11.4.1 WLSMV ordinal SEM birincil — mini-blok EKLE (kutu eksikti)**

Çapa: `### 11.4.1 Model uyumu` başlığının hemen ALTINA ekle:

```markdown
**Bilimsel soru.** Anne depresif belirti yükü (Beck), annenin ebeveynlik tutumu latent boyutlarını (EMBU-P sıcaklık, aşırı koruma, reddetme, karşılaştırma) yorduyor mu — ve bu ilişki ölçüm hatasından arındırıldığında hangi boyutlara özgü?

**Yöntem & tatbik.** 50 ordinal madde (21 Beck + 29 EMBU-P) üzerinde WLSMV kestirimcisiyle yapısal eşitlik modeli kurulur. WLSMV, sıralı (ordinal) Likert maddeleri için normal-teori ML'ye üstündür; polikorik korelasyon temelinde çalışır. Uyum CFI/TLI/RMSEA/SRMR ile değerlendirilir.

**Nasıl değerlendirilir.** Uyum indeksleri eşiklere göre okunur (RMSEA<0,05 iyi; CFI/TLI≈0,90 sınır; SRMR>0,08 yüksek artık); karmaşık ordinal modelde yorum uyumun MUTLAK değil GÖRELİ iyileşmesi akılda tutularak yapılır. Yapısal β'lar ancak kabul edilebilir uyum altında yorumlanır.
```

- [ ] **Step 2: 11.4.3 çoklu-grup ölçüm değişmezliği — kompakt mini-blok ekle**

Çapa: `### 11.4.3 Çoklu-grup ölçüm değişmezliği` başlığının hemen ALTINA ekle:

```markdown
**Bilimsel soru.** Beck→EMBU-P yolları DM ve Kontrol gruplarında aynı biçimde mi tahmin ediliyor — yani T1DM bağlamı bu ilişkiyi modere ediyor mu?

**Yöntem & tatbik.** İndirgenmiş madde setiyle configural → metrik (yük) → skalar (eşik) düzeyinde çoklu-grup ölçüm değişmezliği taranır; her düzey bir öncekine kısıt ekler. Karar ΔCFI<0,010 (Cheung ve Rensvold, 2002) ve ΔRMSEA<0,015 (Chen, 2007) eşikleriyle verilir.

**Nasıl değerlendirilir.** Değişmezliğin kurulması, yolların gruplar arası karşılaştırılabilir olduğunu; T1DM'in ek moderasyon sinyali üretmediğini gösterir. Skalar düzeyde kategori birleştirme gibi ön-kayıt-sonrası kararlar sapma tablosuna işlenir.
```

- [ ] **Step 3: R-literal doğrula + Commit**

```bash
python3 - <<'PY'
import re, hashlib
t = open("docs/CLINICAL-STUDY-REPORT-FINAL.qmd", encoding="utf-8").read()
b = re.findall(r'^```\{r.*?^```', t, re.M | re.S)
print("CHUNK_HASH =", hashlib.md5("".join(b).encode()).hexdigest())
PY
git add docs/CLINICAL-STUDY-REPORT-FINAL.qmd
git commit -m "docs(csr): §11.4 H4 didaktik mini-bloklar (WLSMV SEM + ölçüm değişmezliği; eksik kutu eklendi)"
```
Expected: `CHUNK_HASH` baseline ile AYNI.

---

### Task 5: H5 mini-blokları (§11.5 — diadik tutarlılık, 5 strateji)

**Files:**
- Modify: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` (§11.5, 5 strateji + üst mini-blok)

**Interfaces:**
- Consumes: Task 0 `CHUNK_HASH`. Produces: H5'te 1 üst + 5 strateji mini-bloğu; §11.5.8 Karar Kutusu değişmez.

- [ ] **Step 1: 11.5 üst mini-blok — `> Yöntem kutusu`'nu dönüştür**

Çapa: `## 11.5 H5 …` altındaki `> **Yöntem kutusu — Yüzey-tepki...` blockquote'unu şununla değiştir:

```markdown
**Bilimsel soru.** T1DM bağlamında anne ile çocuğun aynı ebeveynlik boyutuna ilişkin algıları ne ölçüde uyuşuyor; uyum/uyuşmazlık DM ve Kontrol'de farklı mı?

**Yöntem & tatbik.** Tek bir uyum ölçütü kırılgan olacağından **beş paralel strateji** ile çapraz üçgenleme yapılır (ICC+Bland-Altman, RSA, CFM, Olsen-Kenny latent CFA, k-katsayısı). Bilgi-verenler arası sistematik fark, ölçüm hatası değil geçerli bir perspektif bilgisidir (Diverging/Operations Triad çerçevesi; De Los Reyes ve ark., 2015).

**Nasıl değerlendirilir.** Ön-kayıtlı kural: bir yön iddiası ("DM>Kontrol") ancak **en az üç strateji** aynı yönde uyuşursa "güçlü bulgu" sayılır; aksi halde tek-strateji sinyal olarak, tutarsızlık şeffaf raporlanarak sunulur.
```

- [ ] **Step 2: 11.5.1 ICC+Bland-Altman — kompakt mini-blok ekle**

Çapa: `### 11.5.1 Strateji 1: ICC + Bland-Altman Uyum Sınırları` başlığının hemen ALTINA ekle:

```markdown
**Bilimsel soru.** Anne ↔ çocuk aynı-boyut puanları ne kadar uyuşuyor ve fark sistematik mi?

**Yöntem & tatbik.** Düadik ICC ortak varyans oranını (mutlak uyum), Bland-Altman ise ortalama fark ± 1,96×SD uyum sınırlarını (bias + saçılım) verir. Dört alt ölçek × üç düad tipi × iki grup + havuz raporlanır.

**Nasıl değerlendirilir.** ICC büyüklüğü kaba psikometrik bantlarla (Cicchetti, 1994; klinik standart değil betimleme) ve çapraz-bilgi-veren r≈0,28 referansıyla (Achenbach ve ark., 1987; De Los Reyes ve ark., 2015) okunur; geniş Bland-Altman sınırı zayıf birey-düzeyi uyuma işaret eder.
```

- [ ] **Step 3: 11.5.2 RSA — kompakt mini-blok ekle**

Çapa: `### 11.5.2 Strateji 2: Yanıt Yüzeyi Analizi (Edwards-Parry RSA)` başlığının hemen ALTINA ekle:

```markdown
**Bilimsel soru.** Uyum/uyuşmazlık, ham fark skorunun gizlediği eğim ve eğrilik örüntülerine sahip mi?

**Yöntem & tatbik.** RSA, anne ve çocuk skorlarını ayrı yordayıcı tutup polinom yüzey (kareler + çapraz terim) kestirir; a1–a5 parametreleri uyum hattı ve uyumsuzluk ekseninin eğim/eğriliğidir. Ham fark skorunun güvenilirlik kaybını önler.

**Nasıl değerlendirilir.** RSA tekil bir "DM>Kontrol uyum skoru" ÜRETMEZ; parametreler yüzey terimleridir. Bu nedenle tek başına yön kanıtı sayılmaz — üçgenlemeye yüzey-biçimi katkısı verir.
```

- [ ] **Step 4: 11.5.3 CFM — kompakt mini-blok ekle**

Çapa: `### 11.5.3 Strateji 3: Ortak Yazgı Modeli (CFM)` başlığının hemen ALTINA ekle:

```markdown
**Bilimsel soru.** Anne ve çocuk raporlarının paylaştığı bir "ortak aile latent'i" var mı ve bu ortak yapı gruba göre değişiyor mu?

**Yöntem & tatbik.** Ortak Yazgı Modeli, her iki bildirimi tek bir latent ortak nedenin göstergeleri olarak modelleyip grup etkisini bu latent üzerinde test eder.

**Nasıl değerlendirilir.** Yalnız yakınsayan ve uygun (Heywood-olmayan) çözümler yorumlanır; yakınsamayan alt ölçek (ör. reddetme) geçersiz sayılır ve yön kanıtı olarak kullanılmaz.
```

- [ ] **Step 5: 11.5.4 Olsen-Kenny latent CFA — kompakt mini-blok ekle**

Çapa: `### 11.5.4 Strateji 4: Olsen-Kenny Ayırt Edilebilir Düad Doğrulayıcı Faktör Analizi` başlığının hemen ALTINA ekle:

```markdown
**Bilimsel soru.** Ölçüm hatasından arındırılmış gerçek (latent) anne–çocuk uyumu nedir ve gruba göre ayrışıyor mu?

**Yöntem & tatbik.** Olsen-Kenny ayırt edilebilir düad CFA, anne ve çocuğu ayrı ama bağlı latent faktörler olarak modelleyip latent korelasyonu (true concordance) verir; manifest ICC'nin ölçüm-hatası zayıflatmasını düzeltir.

**Nasıl değerlendirilir.** Latent r ancak kabul edilebilir model uyumu altında güvenilir; zayıf uyum (yüksek RMSEA/SRMR) altındaki bir asimetri kırılgan/hipotez-üretici sayılır (Kenny ve ark., 2006), doğrulayıcı değil.
```

- [ ] **Step 6: 11.5.5 k-katsayısı — kompakt mini-blok ekle**

Çapa: `### 11.5.5 Strateji 5: Kenny k-katsayısı` başlığının hemen ALTINA ekle:

```markdown
**Bilimsel soru.** Düad-düzeyi non-bağımsızlık (benzeşme), sıfır ankraja göre anlamlı mı?

**Yöntem & tatbik.** Kenny k-katsayısı düadik benzeşmeyi ölçer; bootstrap güven aralıklarıyla raporlanır.

**Nasıl değerlendirilir.** Sıfırı içeren geniş aralıklar örneklemin düadik bootstrap için sınırda olduğunu gösterir; yalnız havuzlanmış kestirildiğinden DM-vs-Kontrol yön kanıtı vermez, k=0 ankraj olarak okunur.
```

- [ ] **Step 7: R-literal doğrula + Commit**

```bash
python3 - <<'PY'
import re, hashlib
t = open("docs/CLINICAL-STUDY-REPORT-FINAL.qmd", encoding="utf-8").read()
b = re.findall(r'^```\{r.*?^```', t, re.M | re.S)
print("N_CHUNKS =", len(b), "CHUNK_HASH =", hashlib.md5("".join(b).encode()).hexdigest())
PY
git add docs/CLINICAL-STUDY-REPORT-FINAL.qmd
git commit -m "docs(csr): §11.5 H5 didaktik mini-bloklar (5 diadik strateji + üst çerçeve)"
```
Expected: `N_CHUNKS`/`CHUNK_HASH` baseline ile AYNI.

---

### Task 6: §11 denetim kapısı

**Files:**
- Read/verify: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd`
- Create: `tez-yazim/04_kalite-kontrol/raporlar/11-birincil-hipotez-sci-audit.md`

**Interfaces:**
- Consumes: Task 1–5 çıktısı. Produces: denetim raporu + pilot onay paketi.

- [ ] **Step 1: R-literal bütünlüğü (final)**

```bash
python3 - <<'PY'
import re, hashlib
t = open("docs/CLINICAL-STUDY-REPORT-FINAL.qmd", encoding="utf-8").read()
b = re.findall(r'^```\{r.*?^```', t, re.M | re.S)
print("N_CHUNKS =", len(b), "CHUNK_HASH =", hashlib.md5("".join(b).encode()).hexdigest())
PY
```
Expected: Task 0 baseline `N_CHUNKS`/`CHUNK_HASH` ile AYNI (hiçbir R literali/verdict değişmedi).

- [ ] **Step 2: sci-audit yedi eksen (özellikle A/B/C/G)**

Run: `/sci-audit:audit docs/CLINICAL-STUDY-REPORT-FINAL.qmd --lang tr --strictness certification`
Expected: axis G ondalık-nokta `p` blocker = 0; axis A uydurma/yanlış künye = 0 (yeni atıf eklenmediyse); axis B kaynaksız yeni claim = 0. `error`/`blocker` sıfır.

- [ ] **Step 3: Türkçe imla ayrı koşum**

Run: `/sci-audit:check-turkish docs/CLINICAL-STUDY-REPORT-FINAL.qmd --strictness certification`
Expected: ondalık virgül tutarlı; mini-bloklarda İngilizce ondalık-nokta yok.

- [ ] **Step 4: Galileo advisory (referans-nesri + tutarlılık)**

Run: `python3 scripts/mcp/audit_stack_healthcheck.py` (yığın canlı mı) + galileo `reference_prose`/`coherence` §11 üzerinde.
Expected: healthcheck PASS; advisory bulgular kayıt altına alınır (soft-block yok).

- [ ] **Step 5: Yeni-atıf kontrolü**

```bash
git diff docs/CLINICAL-STUDY-REPORT-FINAL.qmd | grep -E '^\+' | grep -oE '\[@[a-zA-Z0-9_:-]+\]' | sort -u
```
Expected: yeni `[@key]` yoksa çıktı boş (mini-bloklar mevcut künyeleri düz-metin yazar-yıl olarak kullandı). Yeni `[@key]` varsa her biri `/referans-kapisi`'nden geçmiş + `references.bib`'de olmalı.

- [ ] **Step 6: Denetim raporunu yaz + commit**

```bash
git add tez-yazim/04_kalite-kontrol/raporlar/11-birincil-hipotez-sci-audit.md
git commit -m "docs(csr): §11 pilot denetim raporu (sci-audit + literal-koruma + advisory)"
```

- [ ] **Step 7: Pilot onay paketi (kullanıcıya)**

`git diff`'i özetle; kullanıcıdan format/ton/derinlik onayı iste. Onay gelirse kalan 22 bölüme yayılım AYRI plan + AYRI onayla başlar (bu planın kapsamı dışında).

---

## Self-Review

**1. Spec coverage:** Spec'in her bölümü bir task'a düşüyor —
- Mini-blok şablonu → Task 1–5 (her mini-blok 3 parça).
- Yinelenme önleme (ölçüt-baş/verdict-son) → tüm task'larda Karar Kutusu dokunulmaz; parça 3 = ölçüt (Global Constraints + her step).
- Pilot §11 ~19 teknik → Task 1 (4) + Task 2 (3) + Task 3 (4) + Task 4 (2) + Task 5 (6=1 üst+5 strateji) = 19.
- Atıf akışı → Global Constraints + Task 6 Step 5.
- Guardrail'ler (format, R-literal, veri sınırı, nedensellik) → Global Constraints + her task literal-check.
- Denetim kapıları → Task 6.
- Baseline (önceki CSR diff) → Task 0.

**2. Placeholder scan:** Somut olmayan placeholder yok; her mini-blok tam metinle verildi; `[YENİ ATIF]` gibi belirsizlik yok (atıflar mevcut künyelerden).

**3. Type/anchor consistency:** Tüm çapalar §11 gerçek başlık metinleriyle eşleşti (doğrulandı: awk taraması). `CHUNK_HASH`/`N_CHUNKS` imzası Task 0'da tanımlı, her task'ta aynı ada karşı kontrol edilir.

**Not:** H5 6 mini-blok (1 üst + 5 strateji) içerir; envanterdeki "5 strateji" + üst çerçeve = 6 birim. Toplam §11 = 20 mini-blok (spec'teki ~19 tahmini ± üst çerçeve).
