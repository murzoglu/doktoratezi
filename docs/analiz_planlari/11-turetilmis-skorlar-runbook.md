# Türetilmiş Skor Ekosistemi Runbook

**Kapsam:** KISIM II / 6  
**Uygulama:** `R/10_derived_scores.R`, `scripts/R/11_derive_scores_audit.R`  
**Son güncelleme:** 2026-04-27

## 1. Kapsam

Bu katman final CSV dosyalarını değiştirmez. Türetilmiş skorlar analiz belleğinde ve `_targets/` cache'inde üretilir; satır-düzeyi skorlanmış CSV yazılmaz.

Skorlanan bloklar:

| Dosya düzeyi | Bloklar |
|---|---|
| Family | EMBU-P, EMBU-C index, EMBU-C sibling, SRQ index, SRQ sibling, Beck/BDI |
| Long | EMBU-C, SRQ, Beck/BDI |

## 2. Skor Kuralları

| Ölçek | Kural |
|---|---|
| EMBU | 4 alt ölçek: `sicaklik`, `asiri_koruma`, `reddetme`, `karsilastirma` |
| SRQ/KIA | 16 birincil boyut + 4 üst düzey boyut: `warmth`, `status`, `conflict`, `rivalry` |
| Beck/BDI | `beck_total` yalnız 21 itemın tamamı mevcutsa hesaplanır |

EMBU-C `q25` final CSV'de ters skorlanmış olduğu için bu katmanda yeniden ters skorlama yapılmaz.

Alt ölçeklerde iki skor üretilir:

- `*_sum_complete`: tüm itemlar mevcutsa toplam; herhangi bir eksik item varsa `NA`.
- `*_mean`: madde kümesinin en az %50'si mevcutsa mevcut itemların ortalaması.

Ayrıca her alt ölçek için `*_valid_n` ve `*_missing_n` üretilir.

## 3. Komutlar

```bash
Rscript tests/test_derived_scores.R
Rscript scripts/R/11_derive_scores_audit.R
Rscript -e 'targets::tar_make()'
```

Runner çıktıları:

- `outputs/tables/derived_score_dictionary.csv`
- `outputs/tables/derived_score_range_audit.csv`
- `outputs/tables/derived_score_coverage.csv`
- `outputs/tables/derived_score_audit_summary.csv`

Bu dosyalar aggregate/metadata düzeyindedir ve git dışıdır.

## 4. Targets

| Target | İçerik |
|---|---|
| `derived_score_dictionary_table` | Skor tanımları ve item kümeleri |
| `derived_score_range_audit` | Item aralık denetimi |
| `derived_score_range_ok` | Range audit fail-fast hedefi |
| `df_family_scored` | Family düzeyi skorlanmış analiz nesnesi |
| `df_long_scored` | Long düzeyi skorlanmış analiz nesnesi |
| `derived_score_target_summary` | Eklenen kolon ve boyut özeti |

`df_family_scored` ve `df_long_scored` satır-düzeyi nesnelerdir. Bu nedenle yalnız `_targets/` cache'inde tutulur ve public OSF/Git kapsamına girmez.

KISIM II / 7, `df_family_scored` nesnesini girdi alarak `df_family_ses` hedefini üretir.
