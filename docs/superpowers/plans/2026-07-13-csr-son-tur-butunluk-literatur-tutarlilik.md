# CSR Son-Tur: Bütünlük + Literatür + Tutarlılık İmplementasyon Planı

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans (veya subagent-driven-development). Adımlar checkbox (`- [ ]`).

**Goal:** `docs/CLINICAL-STUDY-REPORT-FINAL.qmd`'de son-tur denetiminin (workflow wtl93r3uu + deterministik tarama) doğrulanmış bulgularını kapatmak: (A) hayalet analiz atıflarını gerçek çıktı üreterek + sayısal-yorum çelişkilerini gidererek, (B) 22 tutarlılık + §3 sözlük boşluğunu düzelterek, (C) 8 Tartışma literatür boşluğunu gated citation ile zenginleştirerek.

**Architecture:** WS-A yeni R fonksiyon + `_targets.R` hedef + test + `outputs/tables/*.csv` + CSR chunk/prose (additive; mevcut 60 R-chunk literali byte-korunur). WS-B/WS-C yalnız CSR düzyazı + `references/references.bib`. Kapanış: tar_make + testler + R-literal rebaseline + sci-audit/imla + render + /bolum-sertifika.

**Tech Stack:** R (`targets`, `lm`, `lavaan` FIML, `mice` pool, `ggdag`), Quarto, Python (R-literal guard), evidentia (narratif derin-lit), /referans-kapisi.

## Global Constraints (spec'ten verbatim)

- **Türkçe, edilgen 3. tekil; ondalık VİRGÜL** (`p<0,001`, `d = 0,38`); yazar-yıl **"ve diğerleri"** (0× "ve ark."); AMA-11 kaynakça.
- **Veri sınırı (talimatname §2):** satır-düzeyi içerik bağlama/MCP'ye dökülmez; iş `targets` pipeline + aggregate çıktı üzerinden. Yeni output'lar aggregate `outputs/tables/*.csv`.
- **R-literal invariant:** mevcut 60 R-chunk **byte-korunur** (yeni chunk EKLENİR); mevcut hiçbir istatistik/verdict/kod literali değişmez. Kanıt: orijinal 60 chunk MD5 seti ⊆ yeni set.
- **No-fabrication:** `references.bib`'e giren her künye gerçek PMID/DOI'ye iz sürer (`bib_hygiene.py` HARD=0); doğrulanamayan eklenmez.
- **Kod düzeni:** `R/` saf fonksiyon (I/O yok); `scripts/R/` runner; `tests/` stopifnot; yeni hedef `_targets.R`'de hash-bağımlı.
- **Kanonik baz kilidi:** `data/processed/FINAL_REFERENCE__*` değiştirilmez; yükleme `validate_and_load()` üzerinden.

---

## WS-A — Bütünlük (doğrulanmış real=true + advisory)

### Task A1: Eksik-veri çerçevesi sağlamlığı — CC / FIML / MI(m=50) tahmin karşılaştırması + NMAR delta uygulaması

Denetim (verified real=true): [§8.5:1435](../../CLINICAL-STUDY-REPORT-FINAL.qmd) + §18.4:7017 "üç paralel çerçevede işlenmiştir + NMAR delta ızgarası raporlanmıştır" der ama çıktı yok. `_targets.R`'de `missing_results` + `missing_imputations` (mice m=50/maxit=30) HEDEF var; eksik olan H3 tahmin-karşılaştırması + delta uygulaması.

**Recon düzeltmesi (2026-07-13):** `mi_primary$ses_latent` **0 NA** (CFA pairwise tüm 241 satıra latent skor üretir) → eksikliği taşımaz, delta no-op olur. Eksikliği taşıyan gerçek kovaryat **`aile_isei08`** (22 NA / 241 = %9,1, analitik). Bu nedenle H3 missing-data üçlüsü `aile_isei08` SES kovaryatı üzerinden kurulur: CC N=219 vs FIML/MI N=241; NMAR delta 22 satırı ayarlar. Sinyal-yönü: H3 grup null'unun bu üç çerçeve + delta boyunca değişmemesi (robustluk teyidi).

**Files:**
- Create: `R/63_missing_h3_robustness.R`
- Create: `scripts/R/63_missing_h3_robustness_audit.R`
- Create: `tests/test_missing_h3_robustness.R`
- Modify: `_targets.R` (source + 5 hedef, `missing_imputations` sonrası ~satır 127)
- Modify: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` (yeni §13.5 chunk+prose; §8.5/§18.4 prose "işlenmiştir" → gerçek çıktıya bağla)

**Interfaces:**
- Consumes: `derive_missing_data_frames()` çıktısı (`missing_results`), `run_missing_imputation_set()` çıktısı (`missing_imputations$primary` = mids), `apply_nmar_delta_adjustment()`, `nmar_delta_grid()` (hepsi R/12).
- Produces: `run_h3_missing_robustness(df_family_ses, missing_results, missing_imputations)` → `list(framework_comparison, nmar_delta_sensitivity, summary)`.

- [ ] **Step 1: Failing test yaz** — `tests/test_missing_h3_robustness.R`

```r
source("R/00_paths.R"); source("R/01_io.R"); source("R/11_ses_composites.R")
source("R/12_missing_data_frames.R"); source("R/18_h3_parent_self_report.R")
source("R/63_missing_h3_robustness.R")

base <- validate_and_load()                 # kanonik family baz
df_family_ses <- derive_ses_composites(add_family_scores(base$family))$data  # gerçek isimlerle uyarla
mr <- derive_missing_data_frames(df_family_ses)
imp <- run_missing_imputation_set(mr, m = 5L, maxit = 5L)   # test hızı: küçük m
res <- run_h3_missing_robustness(df_family_ses, mr, imp)

fc <- res$framework_comparison
stopifnot(all(c("outcome","framework","estimate","ci_low","ci_high","p_value","n") %in% names(fc)))
stopifnot(setequal(unique(fc$framework), c("complete_case","fiml","mi_pooled")))
stopifnot(nrow(fc) == 4L * 3L)                       # 4 outcome × 3 çerçeve
stopifnot(all(is.finite(fc$estimate)))
# reddetme grup etkisi üç çerçevede yakın (SES kovaryat imputasyonu null'ı bozmaz)
red <- fc[fc$outcome == "embu_p_reddetme_mean", ]
stopifnot(max(red$estimate) - min(red$estimate) < 0.10)

ds <- res$nmar_delta_sensitivity
stopifnot(setequal(unique(ds$delta), c(-1,-0.5,0,0.5,1)))
stopifnot(nrow(ds) == 4L * 5L)                       # 4 outcome × 5 delta
# delta=0 ≈ mi_pooled
z <- ds[ds$delta == 0 & ds$outcome=="embu_p_reddetme_mean","estimate"]
m <- fc[fc$framework=="mi_pooled" & fc$outcome=="embu_p_reddetme_mean","estimate"]
stopifnot(abs(z - m) < 1e-6)
cat("test_missing_h3_robustness PASS\n")
```

- [ ] **Step 2: Testi çalıştır → FAIL** (`Rscript tests/test_missing_h3_robustness.R` → "could not find function run_h3_missing_robustness"). Ayrıca `add_family_scores`/`validate_and_load` gerçek isimlerini `R/01_io.R` + `R/10_derived_scores.R`'den doğrula, testi bunlarla hizala.

- [ ] **Step 3: `R/63_missing_h3_robustness.R` yaz**

```r
# H3 (EMBU-P grup etkisi) eksik-veri çerçevesi sağlamlığı:
# complete-case vs FIML (lavaan) vs MI-pooled (mice), + NMAR delta ızgarası.
# Kovaryat seti imputasyon çerçevesinde mevcut olanlarla sınırlıdır (ses_latent = impute edilen kovaryat).

h3mr_outcomes <- function() {
  c("embu_p_sicaklik_mean","embu_p_asiri_koruma_mean",
    "embu_p_reddetme_mean","embu_p_karsilastirma_mean")
}
h3mr_formula <- function(outcome) {
  stats::as.formula(paste(outcome, "~ group_dm + anne_yas + ses_latent + cocuk_sayisi"))
}
h3mr_group_row <- function(est, se, dfree, outcome, framework, n) {
  mult <- stats::qt(0.975, df = dfree)
  data.frame(outcome = outcome, framework = framework, n = n,
    estimate = est, std_error = se, df = dfree,
    ci_low = est - mult*se, ci_high = est + mult*se,
    p_value = 2*stats::pt(abs(est/se), df = dfree, lower.tail = FALSE),
    stringsAsFactors = FALSE)
}

# complete-case: lm na.omit
h3mr_complete_case <- function(frame, outcome) {
  fml <- h3mr_formula(outcome)
  d <- frame[stats::complete.cases(frame[all.vars(fml)]), , drop = FALSE]
  m <- stats::lm(fml, data = d); s <- summary(m)$coefficients
  h3mr_group_row(s["group_dm","Estimate"], s["group_dm","Std. Error"],
                 stats::df.residual(m), outcome, "complete_case", nrow(d))
}

# FIML: lavaan sem, fixed.x=FALSE, missing="fiml" (sürekli kovaryatlarda MVN yaklaşımı)
h3mr_fiml <- function(frame, outcome) {
  if (!requireNamespace("lavaan", quietly = TRUE)) stop("lavaan gerekli", call. = FALSE)
  fml <- h3mr_formula(outcome); vars <- all.vars(fml)
  d <- frame[vars]; d$group_dm <- as.numeric(d$group_dm)
  model <- paste0(outcome, " ~ b*group_dm + anne_yas + ses_latent + cocuk_sayisi")
  fit <- lavaan::sem(model, data = d, missing = "fiml", fixed.x = FALSE, meanstructure = TRUE)
  pe <- lavaan::parameterEstimates(fit)
  row <- pe[pe$label == "b", ]
  n <- lavaan::lavInspect(fit, "nobs")
  data.frame(outcome = outcome, framework = "fiml", n = as.integer(n),
    estimate = row$est, std_error = row$se, df = NA_real_,
    ci_low = row$ci.lower, ci_high = row$ci.upper, p_value = row$pvalue,
    stringsAsFactors = FALSE)
}

# MI-pooled: with(mids, lm) + mice::pool
h3mr_mi_pooled <- function(mids, outcome) {
  if (!requireNamespace("mice", quietly = TRUE)) stop("mice gerekli", call. = FALSE)
  fml <- h3mr_formula(outcome)
  fits <- with(mids, stats::lm(eval(fml)))
  pooled <- mice::pool(fits); s <- summary(pooled, conf.int = TRUE)
  gr <- s[s$term == "group_dm", ]
  data.frame(outcome = outcome, framework = "mi_pooled", n = as.integer(mids$m),
    estimate = gr$estimate, std_error = gr$std.error, df = gr$df,
    ci_low = gr[["2.5 %"]], ci_high = gr[["97.5 %"]], p_value = gr$p.value,
    stringsAsFactors = FALSE)
}

# NMAR delta: ses_latent'e originally-missing satırlarda delta ekle, her imputasyonda refit, pool
h3mr_delta_row <- function(mids, original_frame, outcome, delta) {
  long <- mice::complete(mids, "long", include = FALSE)
  adj <- apply_nmar_delta_adjustment(long, original_frame, "ses_latent", delta, id_column = ".id")
  imp_list <- split(adj, adj$.imp)
  fml <- h3mr_formula(outcome)
  ests <- lapply(imp_list, function(d) stats::lm(fml, data = d))
  pooled <- mice::pool(as.mira(ests)); s <- summary(pooled, conf.int = TRUE)
  gr <- s[s$term == "group_dm", ]
  data.frame(outcome = outcome, delta = delta, estimate = gr$estimate,
    std_error = gr$std.error, ci_low = gr[["2.5 %"]], ci_high = gr[["97.5 %"]],
    p_value = gr$p.value, stringsAsFactors = FALSE)
}

run_h3_missing_robustness <- function(df_family_ses, missing_results, missing_imputations,
                                      outcomes = h3mr_outcomes(),
                                      delta_values = c(-1,-0.5,0,0.5,1)) {
  frame <- missing_results$frames$mi_primary       # group_dm, anne_yas, ses_latent, cocuk_sayisi, embu_p_*_mean
  mids  <- if (inherits(missing_imputations, "mids")) missing_imputations else missing_imputations$primary
  fc <- do.call(rbind, lapply(outcomes, function(o) rbind(
    h3mr_complete_case(frame, o), h3mr_fiml(frame, o), h3mr_mi_pooled(mids, o))))
  ds <- do.call(rbind, lapply(outcomes, function(o)
    do.call(rbind, lapply(delta_values, function(dl) h3mr_delta_row(mids, frame, o, dl)))))
  list(
    framework_comparison = fc,
    nmar_delta_sensitivity = ds,
    summary = data.frame(
      n_outcomes = length(outcomes),
      max_reddetme_spread = {
        r <- fc[fc$outcome=="embu_p_reddetme_mean","estimate"]; max(r)-min(r) },
      stringsAsFactors = FALSE))
}
```

- [ ] **Step 4: Testi çalıştır → PASS** (`Rscript tests/test_missing_h3_robustness.R`; `as.mira` mice'tan gelir, gerekirse `mice::as.mira`).

- [ ] **Step 5: `_targets.R` wiring** — `source("R/63_missing_h3_robustness.R")` ekle (source bloğu); `missing_imputations` hedefinden (~127) sonra:

```r
  tar_target(h3_missing_robustness_results,
    run_h3_missing_robustness(df_family_ses, missing_results, missing_imputations)),
  tar_target(h3_missing_framework_comparison_table, h3_missing_robustness_results$framework_comparison),
  tar_target(h3_nmar_delta_sensitivity_table, h3_missing_robustness_results$nmar_delta_sensitivity),
  tar_target(h3_missing_framework_comparison_csv,
    save_apa_table_csv(h3_missing_framework_comparison_table,
      "outputs/tables/h3_missing_framework_comparison.csv"), format = "file"),
  tar_target(h3_nmar_delta_sensitivity_csv,
    save_apa_table_csv(h3_nmar_delta_sensitivity_table,
      "outputs/tables/h3_nmar_delta_sensitivity.csv"), format = "file"),
```

- [ ] **Step 6: `scripts/R/63_...audit.R` runner** — pipeline dışı hızlı doğrulama (mevcut runner desenini izle; `tar_load` ile iki tabloyu yazdır, aggregate).

- [ ] **Step 7: `tar_make()` alt-küme** — `Rscript -e 'targets::tar_make(names=c("h3_missing_framework_comparison_csv","h3_nmar_delta_sensitivity_csv"))'`; iki CSV üretilir.

- [ ] **Step 8: CSR §13.5 chunk + prose** — §13.4 sonrası (satır ~4015) yeni `## 13.5 Eksik-Veri Çerçevesi Sağlamlığı`: didaktik mini-blok (Bilimsel soru→Yöntem&tatbik→Nasıl değerlendirilir) + `{r}` chunk iki CSV'yi okuyup APA tablo(lar) render eder (mevcut apa table deseni). §8.5:1435 + §18.4:7017 "işlenmiştir/raporlanmıştır" ifadeleri "§13.5'te FIML/MI(m=50)/tamamlanmış-durum karşılaştırması ve NMAR delta ızgarası olarak raporlanmıştır" biçiminde gerçek çıktıya bağlanır.

- [ ] **Step 9: Commit** — `git add R/63_* scripts/R/63_* tests/test_missing_h3_robustness.R _targets.R docs/CLINICAL-STUDY-REPORT-FINAL.qmd && git commit -m "feat(csr): §13.5 eksik-veri üçlüsü (CC/FIML/MI m=50) + NMAR delta — hayalet atıf gerçek çıktıyla kapatıldı"`

### Task A2: Hollingshead İki-Faktör paralel H3 SES-ölçüm sağlamlığı (yüzeye çıkar)

Denetim (verified real=true): §8.7:1451 "Hollingshead … paralel raporlanmıştır" ama çıktı yok. R/11:283 `ses_hollingshead` ZATEN hesaplı; `ses_correlation_summary_table` hollingshead↔latent r içeriyor. §16.4 ISEI/SIOPS/EGP ölçüm-yarışı yapıyor (R/52).

**Files:** Modify `R/52_social_stratification.R` (veya R/63'e ek fonksiyon) — ilk adım R/52'yi oku, mevcut ölçüm-yarışı fonksiyonunu bul; `ses_hollingshead` 4. operasyonelleştirme olarak ekle. Modify `_targets.R` (gerekirse), `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` (§8.7 cümlesi + §16.4 tablo/not).

- [ ] **Step 1:** `R/52_social_stratification.R` oku; §16.4 H3-per-SES-measure fonksiyon imzasını doğrula.
- [ ] **Step 2:** Failing test — H3 grup etkisi `ses_hollingshead_z` ile de üretiliyor; latent ile |fark| < 0,10 (aynı null).
- [ ] **Step 3:** Fonksiyonu ses_hollingshead içerecek şekilde genişlet (mevcut ISEI/SIOPS/EGP satırlarına 4. satır).
- [ ] **Step 4:** Test PASS + `tar_make` ilgili hedef.
- [ ] **Step 5:** CSR §8.7:1451 → "SES ölçüm sağlamlığı §16.4'te latent + ISEI/SIOPS/EGP + Hollingshead İki-Faktör (3·eğitim + 5·ISEI)/8 karşılaştırmasıyla ele alınmıştır (r_{Hollingshead,latent} ve paralel H3 grup etkisi tabloda)." §16.4 tablo/notuna Hollingshead satırı.
- [ ] **Step 6:** Commit.

### Task A3: §8.6 nedensel DAG diyagram figürü (advisory)

- [ ] **Step 1:** `R/14_causal_dag.R` oku; DAG dagitty/kenar tanımını bul.
- [ ] **Step 2:** `R/28_apa_figures.R`'ye `apa_plot_causal_dag()` ekle (`ggdag` mevcutsa; değilse guarded fallback → §8.6 metnine "DAG diyagramı OSF ön-kayıt ekinde (`osf.io/pytfe`) sunulmuştur" referansı). ggdag renv'de değilse fallback yolunu seç (yeni paket ekleme).
- [ ] **Step 3:** Target + save png (§15.8 deseni) + §8.6 chunk. Commit.

> **Karar:** ggdag renv.lock'ta yoksa A3 = OSF-referans prose'a indirgenir (yeni bağımlılık eklenmez).

### Task A4: Floor-IRT reddetme yorumu — sayısal hizalama (prose, real=true)

Denetim: latent d=0,372 < manifest d=0,380 → "yükseltti/maskeledi" yanlış; masking yalnız aşırı korumada (0,543>0,370). Konumlar: §15.2 Tablo 15.1 (satır ~4184), §15.4 (satır ~4488), Tablo 15.3 (~4498), §17.7 (~6959), Makale 5 planı (~7108).

- [ ] **Step 1:** Bu 5 konumdaki reddetme cümlelerini düzelt: floor-aware latent d (0,372) manifest d (0,380) ile **pratikte eşit**; reddetmede taban-etkisi maskeleme kanıtı **zayıf**; masking sinyali **aşırı koruma**da gerçek (latent 0,543 > manifest 0,370). Sayısal literaller (R-chunk) DEĞİŞMEZ; yalnız yorum düzyazısı. Commit.

### Task A5: §19.2 H1 alım-dönemi çekincesi (prose, real=true)

- [ ] **Step 1:** §19.2 H1 maddesine (satır ~7034) ekle: "…ancak bu fark dönem-dengeli 2023-only alt-örneklemde ≈0'a inmektedir (d = 0,38 → ≈ 0; §16.14; §18.1); bu nedenle H1 dönem-dengeli bağımsız kohortta doğrulanmayı bekleyen temkinli-olumlu bir bulgudur." Commit.

---

## WS-B — Tutarlılık (22) + §3 Sözlük

Kaynak: denetim raporu `tez-yazim/04_kalite-kontrol/raporlar/` (bu tur) — her madde location + suggested_fix taşır. Hepsi düzyazı/tablo-etiketi; R-literal korunur.

### Task B1: 22 minor/advisory akış düzeltmesi
Öncelik sırasıyla (major-benzeri önce): §11.4.1 uyum-kuralı yumuşatma (CFI 0,887/SRMR 0,127); §17.4(c)/§17.7 "120 spesifikasyon" H3-null↔H1-pozitif etiketleme; §17.2/§17.7 iki IRT tahmini (β=0,14 GRM vs d=0,372 floor) uzlaştırma; §12.4↔§15.10 AUC yuvarlama (0,585 sabit); §12.4↔§15.12 DCA net-fayda tekleştir; §16 figür başlık sürekliliği (cf-f16_09+ numaralı başlık); §12/§15/§16 [KEŞİFSEL] ön-planlı↔post-hoc ayrımı; §11.4.2 std-β/std-olmayan-GA etiketi; §11.5.4 CFI 0,984 açıklaması; §11.5.6 PDT ekseni ayrımı; §16 alt-başlık [KEŞİFSEL] inline tutarlılık; §17.9 SMD "orta↔ciddi" uzlaştırma; §6.2 atıf yerleşimi; §6.4 aracılık keşifsel etiketi; §6.5 "5 boşluk" mantığı; §8.10 FDR aile ↔ §11.5.2; §9.4 ISPAD eşik; §16.8 LPA/LCA atıf; §15.9 multiverse/meta bağımsızlık notu; §17.3 PDT [KEŞİFSEL] etiketi.
- [ ] Her maddeyi denetim raporundaki suggested_fix ile uygula; 4-6 maddelik commit'ler.

### Task B2: §3 sözlük tamamlama + terminoloji birleştirme
- [ ] **Ekle** (§3): E-değer, taban etkisi, GRM, ESEM, Bland-Altman, k (Kenny), Olsen-Kenny düad CFA, çoklu evren/specification curve, SD (standart sapma), SE (standart hata), CSR, MCAR, LCA, BIC, AIC, KVKK, ISCO-08, VIF, REML, ROC, BLRT, MCMC, LOO, EGP, SIOPS, ESS.
- [ ] **Terminoloji birleştir:** MNAR standardına birle (gövde 9× MNAR; §3 NMAR→MNAR, MAR/MCAR/MNAR üçlüsü tamamla, "(NMAR eşdeğer)" notu); IPW↔IPTW ilişkisini §3'te bağla; prose'da İng. "CI" → "GA".
- [ ] **Kullanılmayanları çöz:** HTMT, AVE, CR, BSEM, NRI/IDI (tanımlı, gövdede yok) → ya §3'ten çıkar ya (varsa ilgili bulgu) kullan. Varsayılan: §3'ten çıkar (raporlanmadıkları için).
- [ ] Commit.

---

## WS-C — Literatür (8 boşluk, gated)

Her yeni atıf **/referans-kapisi** 7 adımından geçer (bib_hygiene Adım 0 → bağlam → bibliyografik kimlik → tam metin → Zotero 9ZFDHMZA → claim/pasaj → ledger + iki-kol AI-reliability). Mod: **narratif derin-lit** (SR değil). HARKing: Tartışma literatürü post-hoc serbest.

### Task C1: Narratif derin-lit taraması (evidentia)
- [ ] 8 boşluk için aday kaynak + tam-metin çıkarım (evidentia → pubmed-epmc/openalex/semantic-scholar; Türkçe sorgu → Minerva mode:semantic):
  1. §17.4 **H3-null ↔ Pinquart parent-report benchmark** ayrışması (Pinquart 2013 hastalık-türü/raportör heterojenliği; s-EMBU overprotection operasyonelleştirmesi).
  2. §17.4(b) kaynaksız **kültürel-homojenlik** mekanizması (Türk/kolektivist ebeveynlik normları değişkenliği; kronik hastalıkta kültürel ebeveynlik esnekliği).
  3. §17.5 H4 **aşırı-koruma yolunun depresyondan kopması** (depresyon-vs-anksiyete diferansiyel ebeveynlik; T1DM'de hastalık-yönetimi kaynaklı aşırı koruma).
  4. §19.3 Öneri 3 **BFST-D hedef-uyumsuzluğu** → Cuijpers 2015 maternal-depresyon-tedavisi→çocuk-çıktısı hattına yeniden bağla.
  5. §17.2 H1 **child-report reddetme benchmark** (çocuk-perspektifli algılanan ebeveynlik / diyabet örneklemi).
  6. §17.7 **antidepresan prevalans benchmark** (T1DM bakım-vereni maternal depresyon/antidepresan yaygınlığı).
  7. §17.3 H2 **kardeş-null** güncel diyabet/kronik hastalık kardeş uyum literatürü.
  8. §17.8 **Conger Family Stress Model** belirli künye/yıl çapası.

### Task C2: /referans-kapisi + entegrasyon
- [ ] Doğrulanan künyeler → `references/references.bib` (bib_hygiene HARD=0); §17/§19 prose'a "ve diğerleri" + ondalık-virgül ile entegre; ledger güncelle. Doğrulanamayan → "VERİ BULUNAMADI", eklenmez.
- [ ] Commit(ler).

---

## Finalizasyon (F)

- [ ] **F1:** `Rscript -e 'targets::tar_make()'` (yeni hedefler) exit 0; `Rscript tests/test_missing_h3_robustness.R` + değişen R modüllerinin `tests/test_*.R`'leri PASS.
- [ ] **F2: R-literal rebaseline** — Python guard: orijinal 60 chunk MD5 seti (cbed6d5…) ⊆ yeni chunk MD5 seti (mevcut hiçbiri değişmedi; yalnız EKLEME); yeni N + hash kaydet.
- [ ] **F3:** `/sci-audit:audit docs/CLINICAL-STUDY-REPORT-FINAL.qmd --lang tr --strictness certification` + `check-turkish` → BLOCKER YOK; rapor `tez-yazim/04_kalite-kontrol/raporlar/csr-son-tur-sci-audit.md`.
- [ ] **F4:** `quarto render docs/CLINICAL-STUDY-REPORT-FINAL.qmd` exit 0.
- [ ] **F5:** `/bolum-sertifika` Kapı 0–5; `certified-final` yalnız kullanıcı açık onayıyla.

## Self-Review
- Spec coverage: WS-A (5 real=true/advisory) + WS-B (22 flow + sözlük) + WS-C (8 lit) = denetimin tüm aksiyon-alınabilir bulguları. Çürütülen 3 (real=false) bilinçli kapsam dışı.
- Placeholder: A2/A3 ilk adımı "ilgili R modülünü oku" (imza doğrulama) — meşru recon adımı, kod A1'de tam.
- Tip tutarlılığı: `run_h3_missing_robustness` çıktı kolonları test + target + CSR chunk boyunca sabit.
