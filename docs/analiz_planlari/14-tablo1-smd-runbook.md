# Tablo 1 ve SMD Runbook

**Kapsam:** KISIM III / 9  
**Uygulama:** `R/13_table1_smd.R`, `scripts/R/14_table1_smd_audit.R`  
**Son güncelleme:** 2026-04-27

## 1. Kapsam

Bu katman `df_family_ses` üzerinde aile-düzeyi DM-Kontrol karakteristiklerini özetler. Final CSV dosyalarını değiştirmez ve satır-düzeyi veri yazmaz.

## 2. Çıktılar

| Çıktı | İçerik |
|---|---|
| `table1_family_summary.csv` | Overall, DM ve Kontrol özet satırları; p, q ve SMD |
| `table1_smd_balance.csv` | Değişken düzeyi SMD, yöntem ve denge sınıfı |
| `table1_balance_action.csv` | SMD >= 0.10 olan kovaryat/duyarlılık aksiyonları |
| `table1_group_counts.csv` | DM/Kontrol n |
| `table1_target_summary.csv` | Target satır/sütun özeti |

## 3. Değişken Seti

Tablo 1 aile düzeyi demografi, SES, aile yapısı, materyal kaynak ve anne klinik değişkenlerini içerir:

- Demografi: `anne_yas`, `calisma_durumu`, `es_calisma_durumu`
- SES: `egitim_durumu`, `es_egitim_durumu`, `es_isei08`, `aile_isei08`, `ses_latent`
- Aile yapısı: `cocuk_sayisi`, `age_gap`, `same_sex`
- Materyal: `ev_sahipligi`, `ev_oda_sayisi`, `arabaniz_var_mi`
- Klinik: `kronik_hastalik_durumu`, `anne_antidepresan`, `beck_total`, `beck_severity`

`hba1c` ve `dm_yili` kontrol grubunda structural missing olduğu için Tablo 1 DM-Kontrol SMD dengesine dahil edilmez; DM-klinik duyarlılık hattında ele alınır.

## 4. SMD Kuralları

| Değişken tipi | SMD yöntemi |
|---|---|
| Continuous | DM-Kontrol ortalama farkı / pooled SD |
| Binary | DM-Kontrol oran farkı / pooled binomial SD |
| Çok düzeyli kategori | Level bazlı binary SMD'lerin maksimum mutlak değeri |

Eşikler:

| SMD | Sınıf | Aksiyon |
|---|---|---|
| <0.10 | `iyi_denge` | Standart analiz |
| 0.10-0.20 | `sinirda` | Kovaryat ayarı |
| 0.20-0.40 | `dengesiz` | IPTW + kovaryat ayarı |
| >0.40 | `ciddi_dengesizlik` | Stratified sensitivity |

## 5. Komutlar

```bash
Rscript tests/test_table1_smd.R
Rscript scripts/R/14_table1_smd_audit.R
Rscript -e 'targets::tar_make()'
```

## 6. Targets

| Target | İçerik |
|---|---|
| `table1_results` | Tablo 1 sonuç listesi |
| `table1_family_summary_table` | Formatted Tablo 1 satırları |
| `table1_smd_balance_table` | SMD denge tablosu |
| `table1_balance_action_table` | SMD eşik aksiyonları |
| `table1_group_counts_table` | Grup n |
| `table1_target_summary` | Target özeti |
