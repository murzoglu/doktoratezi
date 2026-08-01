# Derin İstatistik Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Kanonik veri, targets hattı, üretilmiş CSV sonuçları, H1-H5/Faz II analizleri, CSR/tez raporlaması ve dış kanıt köprüsünü en derin seviyede istatistik doğruluk ve tutarlılık denetiminden geçirmek.

**Architecture:** `R/50_statistical_audit.R` deterministik çekirdek denetçidir; `scripts/R/51_statistical_audit.R` bu çekirdeği kanonik veri ve `outputs/tables/` CSV envanteri üzerinde çalıştırır. Derin plan, bu merkezi denetimi `renv`, data governance, modül runner'ları, `targets::tar_make()`, CSR/tez mapping ve Evidentia literatür kanıt zinciriyle çevreleyen yürütülebilir bir runbook olarak tanımlar.

**Tech Stack:** R, `renv`, `targets`, base R `stopifnot()` testleri, Quarto, CSV artefaktları, Markdown audit raporu.

---

## Dosya Yapısı

| Dosya | Sorumluluk |
|---|---|
| `R/50_statistical_audit.R` | Veri sözleşmesi, CSV okunabilirliği, p-değeri, CI, BH/FDR ve tool registry denetim çekirdeği. |
| `scripts/R/51_statistical_audit.R` | Kanonik veri yükleme, `outputs/tables/` envanteri, audit CSV üretimi ve critical fail kapısı. |
| `tests/test_statistical_audit.R` | Audit çekirdeğinin kontrat ve numeric consistency regresyon testi. |
| `_targets.R` | Rebuild sırasında audit target'larının pipeline graph içinde parse edilmesi. |
| `docs/analiz_planlari/50-denetim-kanonik-dosya-haritasi.md` | Kanonik dosyalar ve türetilmiş/yerel artefakt sınırları. |
| `docs/analiz_planlari/51-istatistik-audit-derin-denetim-plani.md` | Bu derin yürütme planı. |
| `outputs/tables/statistical_audit_findings.csv` | Üretilmiş finding ledger; git dışı kalır. |
| `outputs/tables/statistical_audit_summary.csv` | Audit özet ve kabul kapısı; git dışı kalır. |
| `outputs/tables/statistical_audit_tool_registry.csv` | Aktif/opsiyonel denetim araç envanteri; git dışı kalır. |
| `outputs/reports/statistical_audit_deep_report.md` | Derin denetim teknik raporu; satır-düzeyi veri içermeden üretilir ve git dışı kalır. |

## Değişmez Güvenlik Sınırları

- `.env`, credential JSON, ham veri, kimlikleyici, `data/raw/`, `data/cleaned/`, `data/identified/`, `data/backup/`, satır-düzeyi `data/processed/*.csv`, `_targets/` cache ve tam CSV dump rapora taşınmaz.
- `critical` bulgu varken rapor sonucu "geçti" olarak yazılmaz.
- `review` bulguları rapor bitmeden `kabul edildi`, `düzeltilecek` veya `opsiyonel skip` kararlarından biriyle sınıflandırılır.
- Kanonik CSV doğrudan elle değiştirilmez; düzeltme gerekiyorsa kaynak veri karar zinciri ve lock dosyası üzerinden yapılır.

## Derinlik Seviyeleri

| Seviye | Kapsam | Çıktı |
|---|---|---|
| D0 | Worktree ve gizlilik sınırı | Dirty dosya listesi, hassas dosya stage kontrolü |
| D1 | `renv` ve temel reproducibility testleri | Exit code ledger |
| D2 | Audit aracının kendi regresyon testi | PASS/FAIL |
| D3 | Mevcut CSV artefaktları üzerinde merkezi audit | `statistical_audit_*.csv` |
| D4 | `targets` manifest parse ve audit target görünürlüğü | Manifest OK |
| D5 | Tüm çekirdek modül runner ve test matrisi | Modül bazlı PASS/FAIL |
| D6 | `targets::tar_make()` ile full rebuild | Rebuild exit code ve post-rebuild audit |
| D7 | H1-H5, robustluk ve Faz II derin CSV matrisi | Blok bazlı numeric consistency matrisi |
| D8 | CSR, tez mapping, APA tablo/figür ve rapor metni uyumu | Raporlama risk ledger |
| D9 | Evidentia dış kanıt ve literatür köprüsü | Kanıt-kaynak tutarlılık notu |
| D10 | Nihai teknik rapor ve karar sınıflaması | `outputs/reports/statistical_audit_deep_report.md` |

## Task 1: Preflight ve Worktree Güvenliği

**Files:**
- Read: `AGENTS.md`
- Read: `CLAUDE.md`
- Read: `docs/analiz_planlari/50-denetim-kanonik-dosya-haritasi.md`
- Generate: `outputs/reports/statistical_audit_deep_report.md`

- [ ] **Step 1: Worktree durumunu kaydet**

Run:

```bash
git status --short --branch
```

Expected:

```text
## main...origin/main
```

Dirty worktree varsa dosyaları sınıflandır: audit ile ilgili, kullanıcı-local, türetilmiş artefakt, hassas dosya. Revert yapma.

- [ ] **Step 2: Hassas dosya stage kapısını kontrol et**

Run:

```bash
git diff --cached --name-only
```

Expected: `.env`, `credentials.json`, `client_secret`, `data/raw/`, `data/cleaned/`, `data/identified/`, `data/backup/`, `data/processed/*.csv`, `_targets/` veya `outputs/` görünmemeli.

- [ ] **Step 3: Rapor dosyası iskeletini oluştur**

`outputs/reports/statistical_audit_deep_report.md` içine şu başlıkları yaz:

```markdown
# Derin İstatistik Audit Raporu

## Komut Ledger

## Audit Özeti

## Critical Bulgular

## Review Karar Ledger

## Modül Matrisi

## Targets Rebuild

## CSR ve Tez Raporlama Uyumu

## Evidentia Kanıt Zinciri

## Kalan Riskler
```

Bu dosya git dışı artefakttır; commit'e alınmaz.

## Task 2: Reprodüktiblik ve Veri Governance Kapısı

**Files:**
- Test: `tests/test_reproducibility_lock.R`
- Test: `tests/test_final_reference_loading.R`
- Test: `tests/test_data_governance.R`
- Read: `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock`
- Read: `docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md`

- [ ] **Step 1: `renv` durumunu doğrula**

Run:

```bash
Rscript -e 'renv::status()'
```

Expected: `No issues found` ve exit 0.

- [ ] **Step 2: Kanonik lock testini çalıştır**

Run:

```bash
Rscript tests/test_reproducibility_lock.R
```

Expected: exit 0.

- [ ] **Step 3: Final referans yükleme testini çalıştır**

Run:

```bash
Rscript tests/test_final_reference_loading.R
```

Expected: exit 0.

- [ ] **Step 4: Data governance testini çalıştır**

Run:

```bash
Rscript tests/test_data_governance.R
```

Expected: exit 0.

- [ ] **Step 5: Fail olursa durdurma kararını uygula**

Herhangi bir komut exit 0 dönmezse merkezi audit çalıştırma. Raporun `Critical Bulgular` bölümüne yalnız dosya yolu, komut ve hata sınıfı yaz; ham veri veya credential içeriği ekleme.

## Task 3: Audit Çekirdeği Regresyon Kapısı

**Files:**
- Test: `tests/test_statistical_audit.R`
- Read: `R/50_statistical_audit.R`
- Read: `scripts/R/51_statistical_audit.R`

- [ ] **Step 1: Audit kontrat testini çalıştır**

Run:

```bash
Rscript tests/test_statistical_audit.R
```

Expected:

```text
[PASS] Statistical audit contract and numeric consistency checks
```

- [ ] **Step 2: Fail olursa audit'i durdur**

`tests/test_statistical_audit.R` fail ederse `scripts/R/51_statistical_audit.R` çalıştırma. Önce `R/50_statistical_audit.R` içindeki veri sözleşmesi, p-değeri, CI veya FDR hesap kapısı düzeltilir ve test yeniden PASS yapılır.

## Task 4: Mevcut Artefaktlar Üzerinde Merkezi Audit

**Files:**
- Run: `scripts/R/51_statistical_audit.R`
- Generate: `outputs/tables/statistical_audit_findings.csv`
- Generate: `outputs/tables/statistical_audit_summary.csv`
- Generate: `outputs/tables/statistical_audit_tool_registry.csv`

- [ ] **Step 1: Merkezi audit'i çalıştır**

Run:

```bash
Rscript scripts/R/51_statistical_audit.R
```

Expected: exit 0. Konsol özeti `critical=0` içermeli.

- [ ] **Step 2: Summary kapısını doğrula**

Run:

```bash
Rscript -e 'x <- utils::read.csv("outputs/tables/statistical_audit_summary.csv"); stopifnot(x$critical_findings[[1]] == 0); print(x)'
```

Expected: `critical_findings` değeri 0.

- [ ] **Step 3: Findings dosyasını severity düzeyinde say**

Run:

```bash
Rscript -e 'x <- utils::read.csv("outputs/tables/statistical_audit_findings.csv"); print(table(x$severity, useNA = "ifany"))'
```

Expected: `critical` satırı yok. `review` varsa Task 9'da karar ledger'ına alınır.

## Task 5: Targets Manifest ve Full Graph Görünürlüğü

**Files:**
- Read: `_targets.R`

- [ ] **Step 1: Manifest parse kapısını çalıştır**

Run:

```bash
Rscript -e 'targets::tar_manifest(fields = command); cat("targets manifest OK\n")'
```

Expected:

```text
targets manifest OK
```

- [ ] **Step 2: Audit target'larının graph içinde göründüğünü doğrula**

Run:

```bash
Rscript -e 'm <- targets::tar_manifest(fields = command); print(m[grepl("statistical_audit", m$name), c("name", "command")])'
```

Expected: `statistical_audit_findings`, `statistical_audit_summary` veya eşdeğer audit target adları görünür. Görünmüyorsa `_targets.R` entegrasyonu eksik sayılır.

## Task 6: Çekirdek Modül Test ve Runner Matrisi

**Files:**
- Run: `tests/test_*.R`
- Run: `scripts/R/08_ethics_data_governance_audit.R`
- Run: `scripts/R/09_reporting_standards_audit.R`
- Run: `scripts/R/11_derive_scores_audit.R`
- Run: `scripts/R/12_derive_ses_audit.R`
- Run: `scripts/R/13_missing_data_audit.R`
- Run: `scripts/R/14_table1_smd_audit.R`
- Run: `scripts/R/15_causal_dag_audit.R`
- Run: `scripts/R/16_propensity_score_audit.R`
- Run: `scripts/R/17_h1_child_perception_audit.R`
- Run: `scripts/R/18_h2_sibling_relationships_audit.R`
- Run: `scripts/R/19_h3_parent_self_report_audit.R`
- Run: `scripts/R/20_h4_beck_parenting_sem_audit.R`
- Run: `scripts/R/21_h5_dyadic_concordance_audit.R`
- Run: `scripts/R/22_robustness_sensitivity_audit.R`
- Run: `scripts/R/23_bayesian_parallel_audit.R`
- Run: `scripts/R/24_mediation_audit.R`
- Run: `scripts/R/25_latent_profile_audit.R`
- Run: `scripts/R/26_clinical_utility_audit.R`
- Run: `scripts/R/27_network_audit.R`
- Run: `scripts/R/28_dm_subanalyses_audit.R`
- Run: `scripts/R/29_apa_figures_audit.R`
- Run: `scripts/R/30_apa_tables_audit.R`
- Run: `scripts/R/31_thesis_mapping_audit.R`
- Run: `scripts/R/32_final_plans_audit.R`

- [ ] **Step 1: Reprodüktiblik runbook test setini çalıştır**

Run the commands listed in `docs/analiz_planlari/19-reproduktivite-runbook.md` under `Yerel Doğrulama`, excluding `targets::tar_make()` and `quarto render thesis.qmd` for this task.

Expected: Her test ve runner exit 0. Opsiyonel paket eksikliği nedeniyle bilinçli skip varsa runner `status` veya `skip_reason` çıktısı üretmeli.

- [ ] **Step 2: Modül ledger'ını rapora işle**

Her komut için şu alanları yaz:

```text
command | exit_code | expected_output | decision
```

Allowed `decision` değerleri: `pass`, `critical`, `review/optional_skip`, `review/fix_needed`.

## Task 7: Phase II ve Extension Runner Matrisi

**Files:**
- Run: `scripts/R/33_trifactor_model_audit.R`
- Run: `scripts/R/34_informant_discrepancy_audit.R`
- Run: `scripts/R/35_cross_informant_network_audit.R`
- Run: `scripts/R/36_floor_aware_irt_audit.R`
- Run: `scripts/R/37_reliability_generalization_audit.R`
- Run: `scripts/R/38_esem_embu_audit.R`
- Run: `scripts/R/39_antidepressant_pathway_audit.R`
- Run: `scripts/R/40_h5_extensions_audit.R`
- Run: `scripts/R/42_causal_mediation_audit.R`
- Run: `scripts/R/43_dag_pc_fci_audit.R`
- Run: `scripts/R/44_distributional_audit.R`
- Run: `scripts/R/45_multiverse_extension_audit.R`
- Run: `scripts/R/46_bayesian_meta_audit.R`
- Run: `scripts/R/47_clinical_dx_extension_audit.R`
- Run: `scripts/R/48_power_replication_audit.R`
- Run: `scripts/R/49_phase2_apa_outputs_audit.R`
- Run: `scripts/R/50_phase2_thesis_mapping_audit.R`

- [ ] **Step 1: Phase II runner'larını sırayla çalıştır**

Run:

```bash
for f in scripts/R/3*_audit.R scripts/R/4*_audit.R scripts/R/50_phase2_thesis_mapping_audit.R; do
  echo "RUN $f"
  Rscript "$f"
done
```

Expected: Her runner exit 0. Bilinçli skip durumunda `status` veya `skip_reason` içeren aggregate CSV üretilir.

- [ ] **Step 2: Boş CSV ve skip reason bağını denetle**

Run:

```bash
Rscript -e 'files <- list.files("outputs/tables", pattern = "\\.csv$", full.names = TRUE); sizes <- file.info(files)$size; print(data.frame(file = basename(files), size = sizes)[sizes == 0 | is.na(sizes), ])'
```

Expected: Boş CSV yok. Varsa ilgili runner ve status/skip_reason dosyası ile `review/csv_io` olarak sınıflandır.

## Task 8: Full Rebuild ve Post-Rebuild Audit

**Files:**
- Run: `_targets.R`
- Run: `scripts/R/51_statistical_audit.R`
- Test: `tests/test_statistical_audit.R`

- [ ] **Step 1: Full rebuild kararını kaydet**

Bu planın varsayılanı en derin audit olduğu için full rebuild çalıştırılır. Yalnız hızlı mevcut-artefakt audit'i istenirse bu task raporda `not_run/scope_limited` olarak işaretlenir.

- [ ] **Step 2: Targets full rebuild çalıştır**

Run:

```bash
Rscript -e 'targets::tar_make()'
```

Expected: exit 0.

- [ ] **Step 3: Rebuild sonrası merkezi audit'i tekrar çalıştır**

Run:

```bash
Rscript scripts/R/51_statistical_audit.R
Rscript tests/test_statistical_audit.R
Rscript -e 'renv::status()'
```

Expected: audit exit 0, test PASS, `renv::status()` clean.

- [ ] **Step 4: Pre/post audit farkını raporla**

Compare:

```bash
Rscript -e 'print(utils::read.csv("outputs/tables/statistical_audit_summary.csv"))'
```

Expected: Rebuild sonrası `critical_findings == 0`. Review sayısı değiştiyse hangi target veya runner'ın artefakt setini değiştirdiğini yaz.

## Task 9: H1-H5, Robustluk ve Faz II Numeric Consistency Matrisi

**Files:**
- Read: `outputs/tables/*.csv`
- Read: `docs/analiz_planlari/03-sap-ana-plan.md`
- Read: `docs/analiz_planlari/04-sap-faz2-posthoc.md`
- Read: `docs/analiz_planlari/05-osf-layer3-faz2-amendment.md`

- [ ] **Step 1: Blok listesine göre CSV envanteri çıkar**

Run:

```bash
Rscript -e 'files <- list.files("outputs/tables", pattern = "\\.csv$", full.names = FALSE); blocks <- c("h1_", "h2_", "h3_", "h4_", "h5_", "robust", "phase2_"); print(files[Reduce(`|`, lapply(blocks, grepl, x = files))])'
```

Expected: H1-H5, robustness ve Phase II çıktı dosyaları listelenir.

- [ ] **Step 2: Her blok için numeric consistency kararını yaz**

Kontrol matrisi:

| Blok | Kontrol |
|---|---|
| H1 `h1_primary_*`, `h1_three_way_*` | p aralığı, t/z p-değeri, CI-estimate, FDR, expected contrast sayısı |
| H2 `h2_family_mean_*`, `h2_apim_*` | family mean satır sayısı, dyadic role tutarlılığı, p/CI/FDR |
| H3 `h3_primary_*`, `h3_iptw_*`, `h3_antidepressant_*` | IPTW/HC3 ayrımı, antidepresan stratification, p/CI/FDR |
| H4 `h4_latent_sem_*`, `h4_multigroup_*` | model_type bazlı FDR, SEM fit kolonları, configural/metric status |
| H5 `h5_icc_*`, `h5_k_*`, `h5_inconsistency_*` | ICC aralığı, k coefficient aralığı, dyadic inconsistency aggregate |
| Robust/Faz II `robust_*`, `phase2_*` | status/skip_reason, optional package, boş CSV, numeric contract |

Allowed kararlar: `pass`, `critical`, `review/data_contract`, `review/csv_io`, `review/tool_registry`, `review/reporting`.

## Task 10: Review Bulgularını Klinik ve İstatistik Karara Bağlama

**Files:**
- Read: `outputs/tables/statistical_audit_findings.csv`
- Read: `outputs/tables/statistical_audit_tool_registry.csv`
- Generate: `outputs/reports/statistical_audit_deep_report.md`

- [ ] **Step 1: Review ledger taslağını üret**

Run:

```bash
Rscript -e 'x <- utils::read.csv("outputs/tables/statistical_audit_findings.csv"); y <- subset(x, severity == "review"); print(y[, intersect(c("check_id", "table_id", "column", "row_index", "detail"), names(y))], row.names = FALSE)'
```

Expected: Review bulguları satır-düzeyi içerik dökmeden listelenir.

- [ ] **Step 2: Her review için karar ver**

Karar kuralları:

| Finding tipi | Karar kuralı |
|---|---|
| `csv_readable` / boş CSV | İlgili runner `status` veya `skip_reason` ile opsiyonel olduğunu gösteriyorsa `opsiyonel skip`, aksi halde `düzeltilecek`. |
| `tool_registry` optional unavailable | Plan için zorunlu değilse `kabul edildi`; derin genişleme için gerekiyorsa `düzeltilecek`. |
| Raporlama mismatch | CSR/tez metni düzeltilene kadar `düzeltilecek`. |

- [ ] **Step 3: Review ledger'ı rapora ekle**

Her satır şu formatta olmalı:

```text
check_id | table_id | severity | sınıf | karar | gerekçe | aksiyon_sahibi
```

`gerekçe` alanında ham satır, kimlikleyici veya tam CSV içeriği bulunmaz.

## Task 11: CSR, Tez Mapping ve APA Çıktı Uyumu

**Files:**
- Read: `docs/CLINICAL-STUDY-REPORT-FINAL.md`
- Read: `thesis.qmd`
- Read: `chapters/*.qmd`
- Read: `outputs/tables/apa_*.csv`
- Read: `outputs/tables/thesis_mapping_*.csv`
- Read: `outputs/tables/reporting_standards_*.csv`

- [ ] **Step 1: Reporting standards ve thesis mapping audit'lerini çalıştır**

Run:

```bash
Rscript scripts/R/09_reporting_standards_audit.R
Rscript scripts/R/29_apa_figures_audit.R
Rscript scripts/R/30_apa_tables_audit.R
Rscript scripts/R/31_thesis_mapping_audit.R
```

Expected: exit 0 ve aggregate reporting/mapping tabloları üretilir.

- [ ] **Step 2: CSR sayısal iddialarını audit summary ile karşılaştır**


- [ ] **Step 3: Tez bölüm referanslarını mapping tablolarıyla karşılaştır**

`thesis_mapping_*` tablolarındaki eksik figür, tablo veya chapter referanslarını rapora işle. Eksik referans final metni etkiliyorsa `review/reporting`; render kırıyorsa `critical` say.

## Task 12: Evidentia Literatür ve Kanıt Zinciri

**Files:**
- Read: `.claude/skills/t1dm-tez-rehberi/SKILL.md`
- Read: `.claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md`
- Read: `docs/CLINICAL-STUDY-REPORT-FINAL.md`

- [ ] **Step 1: Kanıt köprüsü dosyalarını varlık ve kapsam açısından doğrula**

Run:

```bash
test -s .claude/skills/t1dm-tez-rehberi/SKILL.md
test -s .claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md
```

Expected: iki komut exit 0.

- [ ] **Step 2: Literatür iddialarını kaynak sınıfına ayır**

CSR ve tezdeki dış kanıt iddiaları şu sınıflara ayrılır:

```text
guideline | systematic_review | primary_study | local_analysis | expert_interpretation
```

Her iddianın yerel analiz sonucu ile karışmadığını doğrula. Yerel CSV'den gelen istatistikler dış literatür bulgusu gibi sunulmaz; literatürden gelen oran veya etki büyüklüğü yerel analiz sonucu gibi sunulmaz.

- [ ] **Step 3: Evidentia notunu rapora ekle**

Rapor formatı:

```text
claim_area | source_class | local_result_link | external_evidence_link | decision
```

Tam makale metni, uzun alıntı veya telifli pasaj rapora kopyalanmaz.

## Task 13: Nihai Kabul Kapısı

**Files:**
- Read: `outputs/tables/statistical_audit_summary.csv`
- Read: `outputs/reports/statistical_audit_deep_report.md`

- [ ] **Step 1: Hard acceptance koşullarını doğrula**

Run:

```bash
Rscript -e 'x <- utils::read.csv("outputs/tables/statistical_audit_summary.csv"); stopifnot(x$critical_findings[[1]] == 0); stopifnot(x$status[[1]] %in% c("pass", "review")); cat("statistical audit acceptance OK\n")'
```

Expected:

```text
statistical audit acceptance OK
```

- [ ] **Step 2: Review kararlarının tam olduğunu doğrula**

Raporun `Review Karar Ledger` bölümünde her `severity == "review"` finding için bir karar satırı bulunmalı. Kararsız review varsa rapor `geçti` sayılmaz.

- [ ] **Step 3: Gizlilik son kontrolünü çalıştır**

Run:

```bash
git status --short
git diff --cached --name-only
```

Expected: `.env`, credential JSON, raw/identified/processed row-level veri, `_targets/` ve `outputs/` staged olmamalı.

- [ ] **Step 4: Nihai sonucu yaz**

Kabul ifadeleri:

| Durum | Yazılacak sonuç |
|---|---|
| `critical_findings == 0`, tüm review kararları tamam | `Derin istatistik audit: review kararlarıyla geçti.` |
| `critical_findings > 0` | `Derin istatistik audit: geçmedi; critical bulgular düzeltilmeli.` |
| Rebuild çalışmadı | `Derin istatistik audit: mevcut artefaktlarla sınırlı; full rebuild yapılmadı.` |
| Review kararı eksik | `Derin istatistik audit: sonuç beklemede; review ledger tamamlanmalı.` |

## Hata Politikası

- `renv::status()` temiz değilse paket ortamı düzeltilmeden full rebuild yapılmaz.
- `tests/test_statistical_audit.R` fail ederse merkezi audit sonucu güvenilir kabul edilmez.
- `critical` finding varsa ilk critical satırdan başlanır; sonraki review bulguları ikincil önceliktedir.
- p-değeri veya FDR farkı varsa önce kaynak fonksiyonun adjusted/unadjusted kolon semantiği doğrulanır.
- Boş CSV varsa önce ilgili runner'ın opsiyonel paket, sample-size veya `skip_reason` davranışı doğrulanır.
- Veri sözleşmesi bulgusu varsa `FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` ve `FINAL_REFERENCE_VERI_HARITASI.md` referans alınır.
- Ham veri veya credential sızıntısı şüphesi varsa audit durdurulur; yalnız dosya yolu ve severity düzeyinde raporlanır.

## Nihai Kabul Kriterleri

- `Rscript tests/test_statistical_audit.R` exit 0.
- `Rscript scripts/R/51_statistical_audit.R` exit 0.
- `outputs/tables/statistical_audit_summary.csv` içinde `critical_findings == 0`.
- `targets::tar_manifest()` exit 0.
- En derin modda `Rscript -e 'targets::tar_make()'` exit 0.
- Rebuild sonrası audit tekrar `critical_findings == 0`.
- Tüm `review` bulguları `kabul edildi`, `düzeltilecek` veya `opsiyonel skip` olarak sınıflandırıldı.
- `outputs/reports/statistical_audit_deep_report.md` içinde komut ledger, summary, review ledger, module matrix, rebuild sonucu, CSR/tez uyumu ve kalan riskler var.
- Git stage alanında hassas veya satır-düzeyi veri yok.

## Self-Review Checklist

- [ ] Plan D0-D10 derinlik seviyelerinin tamamını kapsıyor.
- [ ] Her task için dosya yolu, komut ve beklenen sonuç yazıldı.
- [ ] `critical` ve `review` karar politikası açık.
- [ ] Full rebuild ve post-rebuild audit ayrı kapılarla tanımlı.
- [ ] CSR/tez mapping ve Evidentia kanıt zinciri merkezi numeric audit'ten ayrı ama bağlı ele alındı.
- [ ] Gizlilik sınırları her raporlama aşamasında korunuyor.
