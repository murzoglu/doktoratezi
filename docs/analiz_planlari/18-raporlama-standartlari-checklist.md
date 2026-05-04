# Reporting Standards Checklist

**Kapsam:** KISIM I / 4 reporting standardı  
**Çerçeveler:** STROBE + JARS-Quant + TRIPOD  
**Audit runner:** `scripts/R/09_reporting_standards_audit.R`  
**Son güncelleme:** 2026-04-28

## 1. Uygulama Kararı

Bu çalışma gözlemsel, aile-eşleşmeli ikincil nicel veri analizidir. Niteliksel/karma yöntem analizi bu projenin kapsamı dışındadır ve ayrı bir araştırma projesi olarak yürütülecektir. Reporting standardı bu nedenle üç çerçeve ile sınırlandırılmıştır:

| Çerçeve | Kullanım sınırı | Üretilmesi gereken kanıt |
|---|---|---|
| STROBE | Gözlemsel vaka-kontrol ve kesitsel analiz raporlama omurgası | Yöntem, bulgular, tartışma ve sınırlılık eşlemesi |
| JARS-Quant | APA uyumlu nicel raporlama (APA 2020) | Ölçüm, örneklem, etik, açık bilim notları |
| TRIPOD | Klinik tahmin modeli (KISIM IX risk skoru) raporlama | Internal validation, calibration, NRI/IDI |

## 2. Durum Sözlüğü

| Durum | Anlam |
|---|---|
| `planned` | Tez/çıktı içinde yeri ayrıldı, ancak içerik üretilmedi |
| `drafted` | SAP, yöntem veya plan dokümanında taslaklandı |
| `implemented` | Tez metnine veya output artefaktına işlendi |
| `verified` | Audit/test ile doğrulandı |
| `not_applicable` | Bu çalışma için gerekçeli biçimde uygulanmaz |

## 3. Minimum Kontrol Seti

| Çerçeve | Zorunlu domain | Tez/artefakt konumu | İlk durum |
|---|---|---|---|
| STROBE | Tasarım, örneklem, değişkenler, bias, istatistiksel yöntem, katılımcı akışı, ana sonuçlar, sınırlılıklar | `chapters/02_yontem.qmd`, `chapters/03_bulgular.qmd`, `chapters/04_tartisma.qmd` | `drafted`/`implemented` |
| JARS-Quant | Tasarım, katılımcı rolleri, ölçüm araçları, ön-kayıt, etik, açık bilim, sapma raporlaması | `chapters/02_yontem.qmd`, `chapters/04_tartisma.qmd`, `docs/analiz_planlari/` | `drafted`/`implemented` |
| TRIPOD | Risk skor geliştirme, internal validation, calibration, sensitivity, dış validasyon notu | `outputs/tables/clinical_*.csv`, `chapters/03_bulgular.qmd` (KISIM IX) | `implemented` |

Makine-okunur ayrıntılı liste `R/09_reporting_standards.R` içindeki `reporting_standards_checklist()` fonksiyonunda tutulur.

## 4. Audit Komutları

```bash
Rscript tests/test_reporting_standards.R
Rscript scripts/R/09_reporting_standards_audit.R
```

Runner üç git-dışı çıktı üretir:

- `outputs/tables/reporting_standards_checklist.csv`
- `outputs/tables/reporting_standards_summary.csv`
- `outputs/tables/reporting_standards_findings.csv`

Audit, şema hatası veya geçersiz durum değeri varsa durur. Tez henüz yazım aşamasında olduğu için `planned` ve `drafted` zorunlu maddeler kritik hata değil, `review` bulgusudur.

## 5. Definition of Done

KISIM I / 4 tamamlanmış sayılmadan önce:

- Her zorunlu STROBE maddesi `implemented` veya `verified` durumuna çekilir.
- Katılımcı akış şeması `outputs/figures/strobe_flow.*` olarak üretilir.
- KISIM IX risk skoru için TRIPOD calibration ve internal validation raporlanır.
- Etik, veri yönetimi ve OSF sınırları yöntem bölümünde açıkça raporlanır.
- `scripts/R/09_reporting_standards_audit.R` çıktısında zorunlu `review` bulgusu kalmaz.
