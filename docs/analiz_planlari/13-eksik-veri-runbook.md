# Eksik Veri Çoklu-Çerçeve Runbook

**Kapsam:** KISIM II / 8  
**Uygulama:** `R/12_missing_data_frames.R`, `scripts/R/13_missing_data_audit.R`  
**Son güncelleme:** 2026-04-27

## 1. Kapsam

Bu katman final CSV dosyalarını değiştirmez ve satır-düzeyi imputed veri yazmaz. Eksik veri nesneleri `_targets/` cache'inde tutulur; runner yalnız aggregate/metadata tabloları ve eksiklik paterni figürü üretir.

## 2. Çerçeveler

| Frame | İçerik | Kullanım |
|---|---|---|
| `fiml_primary` | Birincil analiz değişkenleri, eksikler korunmuş | SEM/FIML ve model-içi missing handling |
| `complete_case_primary` | Birincil frame üzerinde complete-case alt küme | Tanımlayıcı kayıp kıyası; birincil analiz değil |
| `mi_primary` | Structural eksik içermeyen birincil MI frame | MAR varsayımı altında ana MI nesnesi |
| `mi_clinical_sensitivity` | `mi_primary` + `hba1c`, `dm_yili` | DM-klinik duyarlılık analizleri |

`hba1c` ve `dm_yili` kontrol grubunda structural missing kabul edilir. Bu kolonlar primary MI frame'e alınmaz; klinik sensitivity frame'inde `mice` `where` matrisi ile yalnız DM grubundaki analitik eksikler imputasyona açılır.

## 3. Özetler

| Tablo | İçerik |
|---|---|
| `missing_variable_summary.csv` | Değişken bazında toplam, structural ve analitik eksiklik |
| `missing_block_summary.csv` | Demografi, SES, EMBU, SRQ, Beck ve klinik blok özetleri |
| `missing_group_summary.csv` | Grup bazında eksiklik oranları |
| `missing_pattern_summary.csv` | Primary frame için aggregate eksiklik paterni |
| `missing_frame_manifest.csv` | Frame satır/sütun ve missing-cell özeti |
| `missing_mcar_test.csv` | Little MCAR taraması |
| `missing_mice_method_plan.csv` | `mice` method, predictor ve where planı |
| `missing_mi_diagnostics.csv` | Çalıştırılan MI nesnelerinin m/maxit ve imputed hücre özeti |
| `missing_nmar_delta_grid.csv` | NMAR delta-adjustment duyarlılık şablonu |

## 4. Komutlar

```bash
Rscript tests/test_missing_data_frames.R
Rscript scripts/R/13_missing_data_audit.R
Rscript -e 'targets::tar_make()'
```

Audit runner varsayılan olarak `m = 50`, `maxit = 30` ile primary ve DM-klinik sensitivity MI nesnelerini çalıştırır. Hızlı smoke test gerektiğinde:

```bash
MISSING_MI_M=2 MISSING_MI_MAXIT=1 Rscript scripts/R/13_missing_data_audit.R
```

## 5. Targets

| Target | İçerik |
|---|---|
| `missing_results` | Frame, özet, MCAR ve MI method planı |
| `df_family_missing_fiml` | Primary FIML frame |
| `df_family_missing_complete_case` | Primary complete-case frame |
| `df_family_missing_mi_primary` | Primary MI frame |
| `df_family_missing_mi_clinical_sensitivity` | DM-klinik sensitivity MI frame |
| `missing_imputations` | `mice` primary + clinical sensitivity `mids` nesneleri |
| `missing_mi_diagnostics_table` | MI diagnostic özeti |
| `missing_*_table` | Aggregate eksiklik, frame ve sensitivity tabloları |

## 6. Raporlama Kararı

Complete-case sonuçlar bilgi kaybını göstermek için raporlanır; birincil strateji MAR altında MI ve SEM modellerinde FIML'dir. NMAR delta-adjustment H1-H5 modelleri eklendikten sonra model-spesifik sensitivity olarak çalıştırılacaktır.
