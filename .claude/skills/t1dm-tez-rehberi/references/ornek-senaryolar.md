# Örnek Senaryolar — Yaygın Sorgu Akışları

**Ne zaman oku:** Bir sorgu geldiğinde "hangi reference dosyalarını oku, hangi sırada, ne
çıktı üret?" sorusuna hızlı cevap istediğinde. Bu dosya **karar ağacı** değil, on tipik
proje sorgusu için **uçtan uca akış**'tır.

---

## Senaryo 1: "EMBU-C Sıcaklık alt ölçeği için DM ile kontrol arasında fark var mı?"

**Hedef:** H1 birincil çıktı.

**Akış:**

1. **Bağlam sabitle (Faz 0):**
   - Hipotez = H1 (`docs/analiz_planlari/H1-CHILD-PERCEPTION-RUNBOOK.md`)
   - Veri çerçevesi = `df_long_scored` (uzun format, 2 satır/aile)
   - Ön-kayıt = `osf.io/pytfe` confirmatory

2. **Tedbir denetimi (Faz 0.5):** `references/tedbir-ve-hatalar.md` checklist.

3. **Yöntem seçimi:** `references/multilevel-aile-yapisi.md` §H1 — multilevel zorunlu
   (ICC > .05 beklenir).

4. **Yürütme:**
   ```r
   library(targets)
   tar_load(c(df_long_scored, df_family_ses))

   # Eğer hedef tablo zaten cached ise:
   tar_load(h1_primary_fixed_effects_table)
   tar_load(h1_primary_role_pairwise_table)

   # Yoksa direkt çağır:
   tar_make(h1_child_perception_results)
   ```

5. **Yorumlama:**
   - Birincil tahmin: `role_fDM_Hasta_Indeks` katsayısı (Kontrol_Indeks referans).
   - İkincil: `emmeans` pairwise — Holm + H1 FDR (4 outcome ailesi).
   - Etki büyüklüğü: `effectsize::standardize_parameters(m_h1_primary)`.

6. **Raporlama:** `references/raporlama-sablonlari.md` §7 (Multilevel Model şablonu).

7. **Sensitivity:** IRT theta replikasyonu (`h1_irt_theta_fixed_effects_table`),
   three-way interaction (`h1_three_way_tests_table`), Bayesian preflight
   (`h1_bayesian_plan_table`).

**Beklenen tez paragrafı (kısaltılmış):**

> "Aile düzeyinde rastgele kesişim modeli (1 | aile_no_f) ile EMBU-C Sıcaklık alt ölçeği
> üzerinde rol farkı test edilmiş; Kontrol_Indeks referansına göre DM_Hasta_Indeks
> grubunda β = -0.18 (SE = 0.07, t(232.4) = -2.55, p = .011, β_std = -0.21 [-0.37, -0.05])
> düşük ortalama saptanmıştır. H1 ailesi içinde dört outcome FDR düzeltmesi sonrası
> q = .022 ile anlamlı kalmıştır."

---

## Senaryo 2: "Kardeş çatışmasının sıcaklığa etkisini APIM ile test etmek istiyorum."

**Hedef:** H2 APIM çıktısı.

**Akış:**

1. **Yöntem seçimi:**
   - `references/multilevel-aile-yapisi.md` §H2 APIM
   - `references/ileri-yontemler.md` (lavaan dyadic SEM)
   - Runbook: `docs/analiz_planlari/H2-SIBLING-RELATIONSHIPS-RUNBOOK.md`

2. **Veri çerçevesi:** `df_long_scored` (long, child-level) + family-level kovaryatlar
   (`age_gap`, `same_sex`, `ses_latent`).

3. **Yürütme:**
   ```r
   tar_load(h2_apim_fixed_effects_table)
   tar_load(h2_apim_diagnostics_table)
   tar_load(h2_olsen_kenny_fit_measures_table)
   tar_load(h2_olsen_kenny_latent_correlations_table)
   ```

4. **İki çerçeve:**
   - **APIM (lme4)**: `srq_ho_warmth_mean ~ group_f * family_role_f + srq_ho_conflict_mean_partner + age_gap_z + same_sex + (1 | aile_no_f)`
   - **Olsen-Kenny CFA (lavaan)**: quarrel item set üzerinden indeks–kardeş latent
     korelasyonu (ölçüm hatasından arındırılmış).

5. **Raporlama:** `references/raporlama-sablonlari.md` §8 (APIM) + §9 (Olsen-Kenny).

---

## Senaryo 3: "Anne Beck depresyonu EMBU-P alt ölçeklerini ne kadar yordamaktadır?"

**Hedef:** H4 WLSMV ordinal SEM.

**Akış:**

1. **Yöntem seçimi:** `references/ileri-yontemler.md` §H4 (lavaan WLSMV) +
   `references/psikometri-pipeline.md` (ölçüm modeli) + Runbook
   `docs/analiz_planlari/H4-BECK-PARENTING-SEM-RUNBOOK.md`.

2. **Veri çerçevesi:** `df_family_ses` (1 satır/aile, anne öz-rapor).

3. **Yürütme:**
   ```r
   tar_load(h4_latent_sem_fit_measures_table)
   tar_load(h4_latent_sem_structural_paths_table)
   tar_load(h4_multigroup_fit_measures_table)
   tar_load(h4_multigroup_comparison_table)
   ```

4. **Modelin yapısı (`R/19_h4_beck_parenting_sem.R`):**
   - 21 ordinal Beck item → `beck_dep` latent
   - 29 ordinal EMBU-P item → 4 latent (`sicaklik`, `asiri_koruma`, `reddetme`, `karsilastirma`)
   - Yapısal yollar: `sicaklik ~ beck_dep + anne_yas_z + ses_latent_z` (4 alt ölçek için)
   - Estimator: WLSMV; missing: pairwise

5. **Multi-group invariance:**
   - Hedef en az **metric** (parametre `multigroup_max_step = "metric_loadings"`).
   - Sparse ordinal categories: `h4_multigroup_sparse_collapse_map_table`.

6. **Raporlama:** `references/raporlama-sablonlari.md` §12 (SEM yapısal yollar).

7. **Bayesian preflight:** `h4_bayesian_sem_plan_table` (sampling YAPILMAZ; preflight kayıt).

---

## Senaryo 4: "Eksik veri raporunu nasıl yazarım?"

**Hedef:** Bulgular bölümü "Eksik Veri" alt başlığı.

**Akış:**

1. **Yöntem seçimi:** `references/eksik-veri-yonetimi.md`.

2. **Cached target'ları yükle:**
   ```r
   tar_load(missing_variable_summary_table)
   tar_load(missing_block_summary_table)
   tar_load(missing_pattern_summary_table)
   tar_load(missing_mcar_test_table)
   tar_load(missing_mi_diagnostics_table)
   tar_load(missing_nmar_delta_grid_table)
   ```

3. **Kompozisyon:**
   - **Tablo:** `missing_variable_summary_table` → gtsummary olarak format.
   - **MCAR test sonucu:** `missing_mcar_test_table`'dan p-değeri.
   - **Mekanizma kararı:** Yapısal eksiklik (HbA1c, dm_yili) — DM tasarımı kaynaklı,
     imputasyona dahil değil.
   - **Strateji:** Üç çerçeve (FIML, MI m=50/maxit=30, NMAR delta).
   - **NMAR delta:** δ = -0.5, …, +0.5 SD shift sonuçları.

4. **Raporlama:** `references/raporlama-sablonlari.md` §20 (Eksik Veri Tablosu).

---

## Senaryo 5: "Tablo 1'i nasıl üretir, raporlarım?"

**Hedef:** Demografik denge tablosu + SMD.

**Akış:**

1. **Yöntem:** `R/13_table1_smd.R::build_table1_family()` ve runbook
   `docs/analiz_planlari/TABLE1-SMD-RUNBOOK.md`.

2. **Cached target'lar:**
   ```r
   tar_load(c(table1_family_summary_table,
              table1_smd_balance_table,
              table1_balance_action_table,
              table1_group_counts_table))
   ```

3. **gtsummary üretimi:** `references/raporlama-sablonlari.md` §18.

4. **SMD eşiği:** Bu projede **0.10**. SMD > 0.10 olan kovaryatlar PS modeline dahil edilir
   (zaten DAG-temelli adjustment set'te var).

5. **Tez yerine yerleştirme:** `chapters/03_bulgular.qmd` ilk Tablo olarak.

---

## Senaryo 6: "Bir psikometrik validasyon paragrafı yazmam gerekiyor — EMBU-C Sıcaklık için."

**Hedef:** Yöntem (ya da Bulgular §Psikometri) içinde.

**Akış:**

1. **Yöntem:** `references/psikometri-pipeline.md` 8-adımlı pipeline.

2. **Hedeflerden veri:**
   - `psychval_*` çıktıları `outputs/tables/` altında (psikometrik validation
     `R/06_psychometric_validation.R` üretir).
   - Reliability tablosu: ω, α, n_complete, CITC.
   - CFA fit indeksleri: CFI, TLI, RMSEA [%95 GA], SRMR.
   - Invariance: ΔCFI, ΔRMSEA tablo.

3. **Şablon paragraf:** `references/raporlama-sablonlari.md` §10 (CFA + ω) + §11
   (Ölçüm Değişmezliği).

4. **Çapraz kontrol:** `docs/analiz_planlari/PSIKOMETRIK-VALIDASYON-FINAL-ONERI.md` ile
   çelişki yok.

---

## Senaryo 7: "DM grubu için sensemakr Robustness Value raporu eklemek istiyorum."

**Hedef:** H3 sensitivity bölümü.

**Akış:**

1. **Yöntem:** `references/nedensellik-ve-ps.md` §sensemakr.

2. **Yürütme:**
   ```r
   library(sensemakr)
   tar_load(df_family_ses)

   m_h3 <- lm(embu_p_reddetme_mean ~ group_dm + ses_latent_z + age_gap_z + cocuk_sayisi
              + anne_yas_z, data = df_family_ses)

   s <- sensemakr(m_h3, treatment = "group_dm",
                  benchmark_covariates = "ses_latent_z",
                  kd = 1:3)
   summary(s)
   plot(s)
   ```

3. **Raporlama:** `references/raporlama-sablonlari.md` §15 (Sensemakr Robustness Value).

4. **Tartışmaya entegrasyon:** `chapters/04_tartisma.qmd` §Sınırlamalar.

---

## Senaryo 8: "Quarto render hatası alıyorum — `_freeze` cache problemi olabilir."

**Hedef:** Reproducibility recovery.

**Akış:**

1. **İlk teşhis:** `quarto check` çıktısını oku.

2. **Yaygın çözümler (`references/tez-yazim-rehberi.md` §Hızlı Komutlar):**
   ```bash
   # Cache temizle
   rm -rf _freeze/ .quarto/

   # Renv durum
   Rscript -e 'renv::status()'

   # Targets sağlık
   Rscript -e 'targets::tar_outdated()'
   ```

3. **Targets `meta` hash'i:** `Rscript -e 'targets::tar_meta() |> dplyr::filter(!is.na(error))'`
   — hata olan target'ı tespit et.

4. **Kanonik kilit:** Eğer `lock_file` veya `family_csv` invalid ise pipeline durdu;
   `references/pipeline-mimarisi.md` §Kanonik Kilit Doğrulama Zinciri.

5. **Render tekrar:**
   ```bash
   quarto render thesis.qmd
   ```

---

## Senaryo 9: "H3 IPTW analizinde antidepresan kullanan annelerle kullanmayanlar farklı mı?"

**Hedef:** Stratified sensitivity analizi (KEŞİFSEL veya pre-registered duyarlılık?).

**Akış:**

1. **Ön-kayıt kontrolü:** H3 runbook §2 (Duyarlılık Katmanları) — bu analiz **pre-registered**
   AD-stratified duyarlılığın parçası.

2. **Cached target'lar:**
   ```r
   tar_load(c(h3_antidepressant_counts_table,
              h3_antidepressant_stratified_group_effects_table))
   ```

3. **Sayı kontrolü:** `h3_antidepressant_counts_table` → her stratada n ≥ 5 mi?
   - DM AD kullanan: 35 → kabul
   - Kontrol AD kullanan: 11 → kabul (eşik 5)
   - Toplam AD = 46 / 241 = %19

4. **Yorumlama (H3 runbook §5):**
   > "Primary ve IPTW group_fDM etkilerinde H3 içinde FDR < .05 sonuç yoktur. Bu bulgu
   > klinik veya nedensel yokluk iddiası olarak değil, SAP'de tanımlı total-effect model
   > altında gözlenen küçük ve belirsiz grup farkları olarak raporlanmalıdır."

5. **TOST gerekli mi?** "Yok" yorumu için EVET — `references/etki-buyuklugu-ve-guc.md`
   §TOST. ±0.20 SD bound.

6. **Raporlama:** `references/raporlama-sablonlari.md` §14 (IPTW + ANCOVA).

---

## Senaryo 10: "Bayesian model ekleyebilir miyiz? brms ile H1 üzerinde."

**Hedef:** H1 Bayesian augmentation (KEŞİFSEL ya da preflight).

**Akış:**

1. **Ön-kayıt durumu:** H1 runbook §4 — Bayesian sampling default audit/targets içinde
   ÇALIŞTIRILMAZ. Bu nedenle `[KEŞİFSEL]` etiketi.

2. **Prior türetimi:** `references/etki-buyuklugu-ve-guc.md` §Pinquart 2013 — Normal(-0.20, 0.10)
   role_fDM_Hasta_Indeks katsayısı için.

3. **Yürütme:** `references/ileri-yontemler.md` §Bayesian Regresyon brms örneği.

4. **MCMC diagnostics:** R-hat ≤ 1.01, n_eff ≥ 0.10 ratio, divergence = 0. Aksi halde
   `adapt_delta = 0.99`.

5. **Yorumlama:**
   - `describe_posterior(m_h1_brms, ci = 0.95)` → posterior median + 95% CrI
   - `rope(m_h1_brms, range = c(-0.10, 0.10))` → ROPE testi
   - `pp_check(m_h1_brms, type = "stat_grouped", group = "role_f")` → posterior predictive

6. **Raporlama:** `references/raporlama-sablonlari.md` §17 (Bayesian Posterior).

7. **Etiketleme:** `[KEŞİFSEL]`. Ön-kayıttan sapma `PRE-REGISTRATION-DEVIATION-TABLE.md`'ye
   yazılır.

---

## Senaryo 11: "Bir runbook güncellemesi yapmam lazım — H2 yaş farkı moderasyonu."

**Akış:**

1. **Hedef:** `docs/analiz_planlari/H2-SIBLING-RELATIONSHIPS-RUNBOOK.md` güncellenir.

2. **Üç yerde eş zamanlı update:**
   - Runbook (yöntem detayı)
   - `R/17_h2_sibling_relationships.R` (kod, parametre)
   - `_targets.R` (target tanımı, eğer yeni hedef ekleniyorsa)
   - `tests/test_h2_sibling_relationships.R` (assertion)

3. **Audit yenile:**
   ```bash
   Rscript scripts/R/18_h2_sibling_relationships_audit.R
   ```

4. **Reporting standards denetimi:**
   ```bash
   Rscript scripts/R/09_reporting_standards_audit.R
   ```

5. **Tez paragrafı:** `references/raporlama-sablonlari.md` §8 ile uyumlu kal.

---

## Senaryo 12: "Kanonik veri yüklemede hash uyumsuzluğu hatası alıyorum."

**Hedef:** Pipeline recovery.

**Akış:**

1. **Hata mesajını oku:** `validate_and_load()` hangi adımda durdu?
   - SHA-256 mismatch?
   - Lock file parse hatası?
   - CSV path lock'ta yok?

2. **Tanı:**
   ```bash
   Rscript -e 'targets::tar_load(final_reference_manifest); print(final_reference_manifest)'
   ```

3. **Reproducibility verifier çalıştır:**
   ```bash
   Rscript scripts/R/07_verify_reproducibility.R
   ```

4. **Eğer kasıtlı bir CSV güncellemesi varsa:**
   - Yeni hash'i hesapla: `Rscript -e 'library(digest); digest::digest("data/processed/FINAL_REFERENCE__analysis_base_family.csv", file = TRUE, algo = "sha256")'`
   - Lock dosyasını güncelle (manuel — bu büyük karar; runbook'a yaz)
   - **Kanonik kilit kırılması = ön-kayıt sapması** → `PRE-REGISTRATION-DEVIATION-TABLE.md`

5. **Eğer hata istem dışı (ör. CSV byte-bazlı silindirik bozulma):**
   - `git diff data/processed/...` (eğer CSV git'te ise — yok aslında, `.gitignore`'da)
   - Backup'tan geri yükle (eğer varsa)

6. **Pipeline yeniden:**
   ```bash
   Rscript -e 'targets::tar_invalidate(everything()); targets::tar_make()'
   ```

   **DİKKAT:** `tar_invalidate(everything())` tüm cache'i siler — uzun sürer (saatler).

---

## Hızlı Karar Tablosu

| Sorgu Tipi | Hangi reference (öncelik sırası) |
|------------|----------------------------------|
| "H1/H2/H3/H4 sonucu nasıl yorumlanır?" | runbook + raporlama-sablonlari + tedbir-ve-hatalar |
| "Hangi etki büyüklüğü?" | etki-buyuklugu-ve-guc + raporlama-sablonlari |
| "Eksik veri ne yapacağım?" | eksik-veri-yonetimi |
| "Multilevel mi single-level mi?" | multilevel-aile-yapisi + tedbir-ve-hatalar |
| "DAG'a hangi kovaryat girer?" | nedensellik-ve-ps |
| "CFA hangi indeksleri raporla?" | psikometri-pipeline |
| "SEM kurtarma — hangi indeks alarmı?" | psikometri-pipeline + ileri-yontemler |
| "Bayesian preflight nasıl?" | ileri-yontemler + etki-buyuklugu-ve-guc (Pinquart prior) |
| ".qmd düzenleme" | tez-yazim-rehberi |
| "Türkçe APA paragraf" | raporlama-sablonlari |
| "Targets target ekleme" | pipeline-mimarisi |
| "Hash hatası" | pipeline-mimarisi + bu dosya §12 |
| "Kitap atfı" | kaynak-kitaplar-haritasi |
| "Sınırlamaları nasıl yazayım?" | tedbir-ve-hatalar + raporlama-sablonlari §21 |
| "Mediation modeli" | ileri-yontemler + raporlama-sablonlari §13 |
| "TOST eşdeğerlik" | etki-buyuklugu-ve-guc + nedensellik-ve-ps |
| "sensemakr RV" | nedensellik-ve-ps |
| "Multiverse" | nedensellik-ve-ps |
| "Yeni .R modülü ekleme" | pipeline-mimarisi §Yeni Hedef Eklerken |

---

## "Yapma" Sinyalleri (Hızlı Kontrol)

Aşağıdaki ifadeleri görürsen DUR ve düzelt:

- "DM neden olur..." → korelasyon dilbilgisi (`tedbir-ve-hatalar.md` §1)
- "Anlamlı fark yoktur" → TOST gerekli (`etki-buyuklugu-ve-guc.md`)
- "Listwise deletion ile..." → eksik veri çerçeveleri (`eksik-veri-yonetimi.md`)
- "Tek-düzey t-test ile..." → multilevel zorunlu (`multilevel-aile-yapisi.md`)
- "%50 madde varsa Beck toplamı..." → Beck için TÜM 21 madde tam olmalı (`psikometri-pipeline.md`)
- "alpha .55 yeter..." → ω + CFA + invariance pipeline'ı bypass (`psikometri-pipeline.md`)
- "antidepresanı kovaryat yap..." → AD post-treatment, kovaryat değil (`nedensellik-ve-ps.md`)
- "HbA1c'yi tüm örnekleme imput..." → yapısal eksiklik ihlali (`eksik-veri-yonetimi.md`)
- "modification indices ile fit'i şişir..." → teori gerektirir (`psikometri-pipeline.md`)
- "p < .05 → büyük etki..." → effect size + GA + benchmark (`etki-buyuklugu-ve-guc.md`)
- "ön-kayıtta vardı sayılır..." → `[KEŞİFSEL]` etiketi gerekli (`tedbir-ve-hatalar.md`)
- "kanonik CSV'ye küçük edit..." → hash zinciri kırılır (`pipeline-mimarisi.md`)

---

## Hızlı Komutlar (Sık Tekrar Edilenler)

```bash
# Tek hipotez sonuçlarını yükle ve incele
Rscript -e 'library(targets); tar_load(c(h1_primary_fixed_effects_table, h1_primary_role_pairwise_table)); print(h1_primary_fixed_effects_table); print(h1_primary_role_pairwise_table)'

# Targets durumunu gör
Rscript -e 'targets::tar_visnetwork()'   # interaktif graph
Rscript -e 'targets::tar_outdated()'      # eskimiş target listesi

# Belirli bir target'ı yeniden çalıştır
Rscript -e 'targets::tar_make(h2_apim_fixed_effects_table)'

# Tüm tabloları outputs/ altına yaz (eğer hedef tanımlı ise)
Rscript -e 'targets::tar_make(starts_with("h"))'

# Tezi sadece bir bölüm render et
quarto render chapters/03_bulgular.qmd

# Audit zinciri (sırayla)
Rscript scripts/R/07_verify_reproducibility.R
Rscript scripts/R/08_ethics_data_governance_audit.R
Rscript scripts/R/09_reporting_standards_audit.R
```

---

## Genişletilmiş Senaryolar — SAP v3.0 KISIM V-XVII

### Senaryo 13: "H5 — anne-çocuk EMBU-P/EMBU-C uyumunu nasıl test ederim?"

**Hedef:** H5 5-strateji paralel.

**Akış:**
1. Önce oku → [`h5-diadik-tutarlilik.md`](h5-diadik-tutarlilik.md) (5 stratejinin **tümü** zorunlu)
2. Veri çerçevesi: `df_family_scored` (anne + indeks + kardeş aynı satırda)
3. Yürütme sırası:
   - Strateji 1 (ICC + Bland-Altman) — temel görsel
   - Strateji 4 (Olsen-Kenny dyadic CFA) — true latent concordance
   - Strateji 2 (RSA Edwards-Parry) — keşifsel: tutarsızlık → outcome
   - Strateji 3 (CFM lavaan) — aile-içi ortak yapı vs idiyosenkrazi
   - Strateji 5 (k-coefficient APIM) — actor/partner yapısı
4. Triangulation kuralı: **en az 3 strateji uyumlu** → güçlü bulgu; aksi halde discrepant tartışmada açık raporlanır
5. Raporlama → [`raporlama-sablonlari.md`](raporlama-sablonlari.md) APA + paragrafının H5 versiyonu skill'in `h5-diadik-tutarlilik.md` sonundaki şablonu

> **[KEŞİFSEL]** etiketi: H5 *yapı olarak* OSF kayıtlı ama mevcut `_targets.R`'da implement değil; gelecek faz. Tezde Bölüm 3.10 master mapping'de.

### Senaryo 14: "DM ile Kontrol arasında EMBU-P Reddetme'de 'fark yok' gibi görünüyor — nasıl raporlamalıyım?"

**Hedef:** Null sonuç savunulabilir hale getirme.

**Akış:**
1. → [`robustluk-ve-sensitivite.md`](robustluk-ve-sensitivite.md) §2 TOST + üçlü karar matrisi
2. SESOI = ±0.30 SMD (Pinquart-temelli; *önceden tanımlı*, post-hoc değil)
3. Üç paralel test:
   ```r
   # Frequentist NHST
   t_h3 <- t.test(embu_p_reddetme_mean ~ group_f, data = df_family)

   # TOST equivalence
   tost_h3 <- TOSTER::tsum_TOST(...)

   # Bayesian ROPE
   rope_h3 <- bayestestR::rope(h3_bayesian_model, range = c(-0.10, 0.10))
   ```
4. Üçlü karar matrisi → **INDETERMINATE** (psikometrik validasyon raporu sonucu)
5. Raporlamada "anlamlı fark yoktur" demek **yasak** — "fark kanıtı yetersiz" demek

> Multiverse `[KEŞİFSEL]` ama H1-H4 birincil bulgular için TOST + sensemakr **standart gereksinim**dir.

### Senaryo 15: "H1 için Bayesian preflight nasıl çalıştırılır?"

**Hedef:** H1 frequentist + Bayesian dual report.

**Akış:**
1. → [`bayesci-paralel-hat.md`](bayesci-paralel-hat.md)
2. Pinquart-prior: *N*(0.30, 0.50) for `role_fDM_Hasta_Indeks`
3. brms multilevel:
   ```r
   m_h1_bayes <- brms::brm(
     embu_c_reddetme_mean ~ role_f + scale(cocuk_yas) + cinsiyet_f +
                              scale(ses_latent) + scale(age_gap) +
                              (1 | aile_no_f),
     data = df_long_scored, family = gaussian(),
     prior = c(prior(normal(0.30, 0.50), class = b, coef = "role_fDM_Hasta_Indeks"),
               prior(normal(0, 1), class = b),
               prior(student_t(3, 0, 2.5), class = sd),
               prior(student_t(3, 0, 2.5), class = sigma)),
     chains = 4, iter = 4000, warmup = 1500, seed = 20260427,
     control = list(adapt_delta = 0.99, max_treedepth = 15),
     sample_prior = "yes"
   )
   ```
4. Convergence: R̂ < 1.01, ESS_bulk > 1000, divergent = 0
5. Posterior: ROPE [-0.10, 0.10], pd, BF Savage-Dickey
6. Dual reporting tablosu (tezde standart): F + p + p_FDR + BF + ROPE% + pd

### Senaryo 16: "Anne tipolojilerini LPA ile nasıl çıkarırım?"

**Hedef:** Klinik müdahale hedeflemesi için anne profilleri.

**Akış:**
1. → [`latent-degisken-yontemleri.md`](latent-degisken-yontemleri.md) §1 LPA
2. Veri: `df_family_scored` (Beck + EMBU-P 4 alt + SES_latent), z-skor
3. tidyLPA 1-6 profil; karar kriterleri (BIC + entropy + LMR-LRT + BLRT)
4. Beklenen 4 profil: Adapte / Aşırı Koruyucu / Tükenmiş / Standart
5. Profil × DM/Kontrol χ² (DM lehine "Tükenmiş" beklentisi)
6. **[KEŞİFSEL]** — tezin 3.12 bulgular bölümünde

### Senaryo 17: "Bir mediation hipotezini test etmek istiyorum: Beck → EMBU-P → EMBU-C"

**Hedef:** Üç-aşamalı mediation.

**Akış:**
1. → [`mediation-modelleri.md`](mediation-modelleri.md)
2. Veri: aile-düzeyi (df_family) + kardeş ortalaması (df_long_summary)
3. lavaan + BCa bootstrap (n = 5000)
4. Multilevel uzantı: 1-1-1 (level-2 mediator), `cluster = "aile_no"`
5. Bayesian alternatif: brms ile path-by-path posterior, indirect distribution + ROPE
6. **Sensitivity:** sensemakr ile mediator-outcome confounder Robustness Value
7. **[KEŞİFSEL]** — KISIM VI keşifsel; OSF kayıtta yok

### Senaryo 18: "Risk skoru türetip klinik kullanılabilirliği nasıl gösteririm?"

**Hedef:** "Yüksek-risk anne" tahmin modeli.

**Akış:**
1. → [`klinik-fayda.md`](klinik-fayda.md)
2. Outcome: Beck ≥ 17 (yüksek-risk binary)
3. Logistic regression (group_f + demografik + SES + AD)
4. ROC + Youden's J + AUC %95 CI
5. **DCA Vickers-Elkin** — net benefit threshold range
6. Calibration plot (bootstrap-corrected, B = 1000)
7. NRI/IDI: maternal mental health belirteçlerinin marjinal katkısı
8. **[KEŞİFSEL/İLERİ FAZ]** — KISIM IX

### Senaryo 19: "DM süresi ile parenting arasında doğrusal olmayan ilişki var mı?"

**Hedef:** Spline modeli.

**Akış:**
1. → [`dm-klinik-altanalizler.md`](dm-klinik-altanalizler.md) §2
2. **DM-only** alt-analiz (n = 120 aile)
3. `splines::ns(dm_yili, knots = quartile)`
4. Linear vs spline LRT (anlamlı → nonlinear var)
5. Predict + plot (CI bandı)
6. **[KEŞİFSEL]** — DM-only, kontrol grubuyla karşılaştırılmaz

### Senaryo 20: "Niteliksel görüşme sonuçlarını nicel bulgularla nasıl entegre ederim?"

**Hedef:** Joint display tablosu.

**Akış:**
1. → [`karma-yontem.md`](karma-yontem.md)
2. RTA (Braun-Clarke 2022) 6-faz; iki kodlayıcı Gwet AC1 ≥ .60
3. Convergent / Complementary / Discrepant 3-tip tablo
4. Discrepant bulgular tezde **renklendirilmiş** ve detaylı tartışılır
5. Tezin Bölüm 3.18 bulgular kısmında

### Senaryo 21: "Tezin yayın stratejisi nasıl olmalı?"

**Hedef:** 3-makale planı.

**Akış:**
1. → [`diseminasyon-ve-yayin.md`](diseminasyon-ve-yayin.md) §6
2. **Makale 1:** H1 + H5 → *Pediatric Diabetes* / *J Pediatr Psychol*
3. **Makale 2:** H3 + H4 + Mediation → *Diabetic Medicine* / *J Family Psychology*
4. **Makale 3:** Psikometrik validasyon → *Methods in Psychology*
5. FAIR/Zenodo: tez kabulü sonrası

### Senaryo 22: "Pipeline'da bir analiz başarısız oldu — ne yaparım?"

**Hedef:** Risk matrisi → yedek strateji.

**Akış:**
1. → [`risk-ve-zaman-cizelgesi.md`](risk-ve-zaman-cizelgesi.md)
2. Hata türünü saptama (15-risk matrisinde karşılığı)
3. Yedek strateji aktive et (`tar_target` yedek hedefi var)
4. OSF deviation tablosuna kaydet
5. Tezde "Sınırlılıklar" bölümünde belge

### Senaryo 23: "OSF kayıtlı analizden saparken nasıl raporlarım?"

**Hedef:** Sapma şeffaflığı.

**Akış:**
1. `[KEŞİFSEL]` etiketi (`tedbir-ve-hatalar.md`)
2. `docs/analiz_planlari/PRE-REGISTRATION-DEVIATION-TABLE.md` güncellenir:
   - Sapma türü (post-hoc karar / yedek strateji / ek keşifsel)
   - Gerekçe
   - Sonuca etkisi
3. Tezde Ek B'ye eklenir, Bulgular paragrafında bahsedilir
4. → [`diseminasyon-ve-yayin.md`](diseminasyon-ve-yayin.md) (FAIR şeffaflık)
