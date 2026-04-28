# KISIM XVI–XVII — Risk Yönetimi ve Zaman Çizelgesi

> SAP v3.0 §47–48. 15-risk matrisi (her riske yedek strateji) + 24-haftalık çalıştırma planı.

## Risk Matrisi (KISIM XVI)

| # | Risk | Olasılık | Etki | Yedek Strateji |
|---|---|---|---|---|
| 1 | H1 grup farkı çıkmaz (Sıcaklık/Aşırı Koruma'da) | Orta | Birincil hipotez red | TOST eşdeğerlik + Bayesian BF + multiverse savunması |
| 2 | H2 sibling APIM convergence fail | Düşük | Aile düzeyi t-test'e geri dön | Yedek hazır (`run_h2_family_mean`) |
| 3 | H3 EMBU-P Reddetme zayıf psikometri | **Yüksek** | Bilinen sorun | BSEM latent factor + multiverse + 3-strata sensitivity |
| 4 | H4 SEM identification fail | Düşük | Latent factor sayısı azalt | Reddetme sum score yedek + path analysis fallback |
| 5 | H5 RSA convergence fail | Orta | Polynomial regression yedek | Mutlak fark + Bland-Altman birincil; RSA exploratory |
| 6 | HbA1c %32.5 mevcut → power yetersiz | **KESIN** | Klinik moderasyon zayıf | dm_yili (n=120 tam) birincil; HbA1c sensitive |
| 7 | Niteliksel doygunluk yok (n=6) | Düşük | Görüşme sayısı artır | Protokol gereği esneklik var |
| 8 | renv lock bozulur | Düşük | Reprodüksiyon kaybı | Docker container yedek + GitHub immutable history |
| 9 | Antidepresan confounder ana etkiyi siler | **YÜKSEK** | H3 hipotezi başka yorumlanmalı | Multiple frame: "Hastalığın anne ruh sağlığına etkisi" |
| 10 | ISEI tek kovaryat olarak yetersiz | Orta | SES ayrımı belirsiz | Latent SES + Hollingshead + sensitivity |
| 11 | LPA convergence fail | Düşük | Tipoloji yapısı kayıp | k-means yedek + cluster validity |
| 12 | Network EBIC-LASSO çıktı belirsiz | Orta | Ağ yorumu zayıf | Pearson partial correlation yedek + bootstrapped edges |
| 13 | Karar ağacı overfit | Yüksek | Klinik öneri güvenilirsiz | Cross-validation + Random Forest comparison |
| 14 | Bayesian Stan compile fail | Düşük | Bayesian hat çalışmaz | rstanarm fallback + manual Stan model |
| 15 | papaja render fail (LaTeX errors) | Orta | Final rapor yok | apaquarto fallback + Word docx tek format |

### Risk önceliklendirme (etki × olasılık)

| Öncelik | Risk #'leri | İlk eylem |
|---|---|---|
| **Kritik** (yüksek×yüksek) | 3, 6, 9 | Multiverse, dm_yili, multi-frame interpretation |
| **Yüksek** (orta×yüksek) | 1, 13 | Equivalence + RF comparison |
| **Orta** | 5, 10, 12, 15 | Yedek strateji aktif |
| **Düşük** | 2, 4, 7, 8, 11, 14 | İzle, gerekirse aktive |

> **Genel kural:** Riskten önce her primary analizin yedek planı `_targets.R`'da `tar_target` olarak
> hazır olmalı; analiz başarısız olursa doğrudan yedek hedef çalıştırılır.

## 24-Haftalık Plan (KISIM XVII)

| Hafta | Faz | Çıktı | Mevcut durum |
|---|---|---|---|
| 1 | Faz 0: Setup + paket + renv | renv.lock, Dockerfile | ✅ Tamamlandı |
| 2 | Faz 1: Veri yükleme + skor türetme | RDS skorlanmış | ✅ Tamamlandı |
| 3 | Faz 2: Tablo 1 + SMD + DAG + propensity | Tablo 1, Şekil 2-4 | ✅ Tamamlandı |
| 4 | Faz 13: SES kompozit | `ses_latent` + Tablo 4 | ✅ Tamamlandı |
| 5 | Faz 7: Eksik veri MI (m=50) | imp objesi | ✅ Tamamlandı |
| 6 | Faz 11: H1 multilevel + 3-way + IRT | Tablo 5, Şekil 6-7 | ✅ Aktif (`R/16`) |
| 7 | Faz 12: H2 family-mean + APIM + dyadic CFA | Tablo 6, Şekil 8 | ✅ Aktif (`R/17`) |
| 8 | Faz 13: H3 main + stratified + IPTW | Tablo 7, Şekil 9 | ✅ Aktif (`R/18`) |
| 9-10 | Faz 14: H4 latent SEM + invariance + Bayesian | Tablo 8, Şekil 10 | ✅ Aktif (`R/19`) |
| 11-12 | Faz 15: H5 ICC + Bland-Altman + RSA + CFM + dyadic CFA | Tablo 9, Şekil 11-12 | ⏳ Gelecek faz |
| 13 | Faz 16-19: Mediation | Tablo 10, Şekil 13 | ⏳ Keşifsel |
| 14 | Faz 21: LPA — anne tipoloji | Tablo 11, Şekil 14 | ⏳ Keşifsel |
| 15 | Faz 22-23: LCA + Bifactor S-1 | Sensitivity tabloları | ⏳ Keşifsel |
| 16 | Faz 24-26: Network analiz + NCT + Beck item-network | Tablo 12, Şekil 15-16 | ⏳ Keşifsel |
| 17 | Faz 27-29: ROC + DCA + CART + RF + Calibration | Tablo 13, Şekil 17, 20 | ⏳ İleri faz |
| 18 | Faz 30-32: Klinik alt-analizler (HbA1c + DM süresi spline + tanı yaşı) | Tablo 14-15 | ⏳ İleri faz / DM-only |
| 19 | Faz 33-36: Multiverse + TOST + Sensemakr + Negative control | Tablo 16, Şekil 18-19 | ⏳ Kısmen aktif |
| 20-21 | Faz 37-39: Tüm Bayesian analizler (H1-H5) + WAIC/LOO | Tablo 17, Şekil 21-22 | ⏳ H1 aktif, gerisi gelecek |
| 22 | Faz 40-41: Niteliksel tematik analiz + Joint display | Tablo 18 | ⏳ Keşifsel |
| 23 | Faz 42-43: APA tablo + papaja + tez bölüm eşleme | Final Quarto rapor | ⏳ Aktif (paralel) |
| 24 | Faz 44-45: Yayın hazırlığı + OSF + Zenodo | Yayın taslakları | ⏳ Tez sonrası |

**Toplam:** 24 hafta ≈ 6 ay analiz fazı.
**Tez yazımı paralel:** 12. haftadan itibaren bulgular yazımı başlar.

## Aktif sprint kontrol listesi

Her hafta sonu (Pazar) şunları kontrol et:

- [ ] `targets::tar_make()` clean run (hata yok)
- [ ] `renv::status()` temiz
- [ ] `Rscript scripts/R/09_reporting_standards_audit.R` PASS
- [ ] `Rscript scripts/R/08_ethics_data_governance_audit.R` PASS
- [ ] OSF deviation tablosu güncel
- [ ] Git commit'lendi (Türkçe mesaj, açıklayıcı)
- [ ] Cache hash'leri (`_targets/meta`) tutarlı

## Risk-Tetiklendiğinde Akış

```
ANALİZ BAŞARISIZ
    ↓
1. Hata türünü saptama (convergence / identification / data quality / package version)
    ↓
2. Risk Matrisi'nde karşılığını bul (yukarıdaki #1-15)
    ↓
3. Yedek strateji aktive et:
   - tar_target yedek hedefi var mı? Çalıştır.
   - R modülü yeniden yazılması gerekiyorsa, aşamalı testle.
    ↓
4. OSF deviation tablosuna kaydet
    ↓
5. Tezde "Sınırlılıklar ve Yedek Stratejiler" bölümünde belge
```

## Tedbir denetimi

- [ ] Her risk için yedek strateji **kod olarak** mevcut (`R/` veya `_targets.R` içinde)
- [ ] Risk tetikleme kriterleri quantitative (örn. "convergence fail" = "iterations > 1000 + warning")
- [ ] OSF deviation table risk-tetiklendiğinde otomatik güncelleniyor
- [ ] Sprint sonunda `targets::tar_outdated()` boş
- [ ] Hafta 12'de tez yazımı paralel başladı (kanonik sıra)

## Çapraz referanslar

- Pipeline durum izleme → [`pipeline-mimarisi.md`](pipeline-mimarisi.md)
- OSF deviation tablosu → [`diseminasyon-ve-yayin.md`](diseminasyon-ve-yayin.md)
- Yedek strateji testleri → `tests/` altındaki dosyalar
