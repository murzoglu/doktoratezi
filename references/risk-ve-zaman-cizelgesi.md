# Risk ve Zaman Çizelgesi

Bu dosya KISIM XV/44 risk yönetimi ve KISIM XVI/45 24-haftalık plan için yürürlükteki referans planıdır.

## Risk Yönetimi

Risk matrisi 14 ana riski kapsar. Niteliksel veri bu proje kapsamından çıkarıldığı için niteliksel doygunluk veya inter-coder reliability riski bu matriste yer almaz.

Aktif izlem gerektiren başlıklar:

- **R03:** EMBU-P reddetme zayıf psikometri. Savunma: BSEM/latent yorum, multiverse, TOST, açık sınırlılık.
- **R06:** HbA1c tamamlanma oranı düşük. Savunma: HbA1c keşifsel, `dm_yili` tam veri klinik süre göstergesi.
- **R08:** Antidepresan kullanımı yorum kaydırıcı olabilir. Savunma: stratified sensitivity ve total-effect dil sınırı.
- **R12:** Klinik karar ağacı/RF overfit riski. Savunma: calibration, DCA, optimism correction ve dış validasyon notu.

## 24 Haftalık Plan

Hafta 1-22 analiz, APA figür/tablo üretimi ve tez eşlemesiyle doğrulanmıştır. Hafta 23 yayın hazırlığı ve açık bilim paketinin sonlaştırılmasıdır. Hafta 24 final QC ve savunma hazırlığıdır.

## Denetlenebilir Çıktılar

Bu plan `R/31_final_plans.R`, `scripts/R/32_final_plans_audit.R` ve `tests/test_final_plans.R` ile denetlenir. Aggregate CSV çıktıları `outputs/tables/final_plan_risk_matrix.csv`, `outputs/tables/final_plan_timeline_24_week.csv` ve manifest dosyaları altında üretilir.
