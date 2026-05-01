# OSF Layer 3 Amendment — Faz II Post-Hoc Exploratory Plan

**T1DM-EBEVEYN Çalışması** — Çalışma-Sonu Verilerle Hipotez-Üretici Analiz Hattı

| Alan | İçerik |
|---|---|
| **Amendment tarihi** | 2026-05-01 |
| **Submit hedefi** | 2026-05-08 |
| **Layer adı** | Layer 3 — Post-Hoc Exploratory Amendment |
| **OSF kayıt tipi** | Open-Ended Registration |
| **Bağlanılan kayıtlar** | Layer 1 (`d524q` — psikometrik validasyon) + Layer 2 (`pytfe` — H1-H5 secondary data preregistration) + Proje (`vqrt5`) |
| **Tetikleyici belgeler** | `docs/CLINICAL-STUDY-REPORT.md` v1.1 (2026-04-29); `docs/CLINICAL-STUDY-REPORT-V2.md` (2026-05-01) |
| **Plan belgesi** | `docs/analiz_planlari/STATISTICAL-ANALYSIS-PLAN-PHASE-2.md` v1.0 |
| **Sapma kaydı** | `docs/analiz_planlari/PRE-REGISTRATION-DEVIATION-TABLE.md` satır #1 (Tip 3, post-hoc bütünleşik amendment) |
| **Veri kilidi** | `FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` (2026-04-26) — **DEĞİŞMEZ** |
| **Embargo** | Tez savunma sonrası otomatik açılım (Layer 1 + Layer 2 ile eş zamanlı) |
| **Amendment commit anchor** | (submit anında `git rev-parse HEAD` çıktısı eklenir) |

---

## 1. Amendment Niçin Açılıyor?

İki katmanlı OSF ön-kayıt stratejisi (Layer 1 ve Layer 2), psikometrik validasyon ve birincil hipotezler (H1–H5) için doğrulayıcı bir çerçeve sundu. Bu çerçeve içinde tüm birincil bulgular `STATISTICAL-ANALYSIS-PLAN.md` v3.0'a sadık kalınarak yürütüldü ve `CLINICAL-STUDY-REPORT.md` v1.1 ile `CLINICAL-STUDY-REPORT-V2.md` belgelerinde raporlandı.

Çalışma sonu verileri **on üç bilimsel boşluk** ortaya çıkardı; bu boşluklar tezsel yorumun derinliği ve yayın hattının güvenilirliği için ek analizler gerektirmektedir. Bu amendment, söz konusu post-hoc analizlerin **şeffaf, ön-kayıtlı bir hipotez-üretici çerçeve** içinde yürütülmesini sağlamak amacıyla açılmıştır.

> **Epistemik beyan:** Faz II'nin tek bir analizi bile **doğrulayıcı (confirmatory) kanıt** üretmez. Tüm bulgular `[KEŞİFSEL · POST-HOC]` etiketiyle raporlanır ve hipotez-üretici niteliktedir. Klinik öneri seviyesine yükseltme, bağımsız bir Türk kohortunda dış-validasyon olmadan yapılmaz.

---

## 2. Tetikleyici On Üç Boşluk

Aşağıdaki tablo, çalışma-sonu CSR'larında belgelenen ve Faz II'yi tetikleyen boşlukları kaynak referansıyla listeler.

| # | Boşluk | CSR kaynağı | Faz II yanıt KISIM'i |
|---|---|---|---|
| 1 | EMBU-P reddetme alt ölçeği α=.45 ω=.48; %62-%95 madde-düzeyi taban etkisi (floor effect) | CSR §10.1, §10.3 | **XXI** — Floor-aware Tobit IRT, ω_h/ECV |
| 2 | H4 SEM CFI=.887 ve SRMR=.127 Hu-Bentler birleşik kriteri altında | CSR §11.4.2 | **XXI** — ESEM cross-loading + Beck cognitive vs somatic bifactor |
| 3 | Anne antidepresan kullanımı SMD=0.53 (DM %29 vs Kontrol %9) — yalnız stratifiye, aracı/moderator değil | CSR §9.2, §11.3.4 | **XXII** — AD mediator + moderator + Beck × AD latent etkileşim |
| 4 | H5 beş diadik tutarlılık stratejisi yön düzeyinde uyumlu, **büyüklük düzeyinde sistematik sapma** | CSR §11.5.6 | **XXIII** — MTMM CT-C(M-1), Bayesian strateji pooling |
| 5 | `negctrl_aile_no → EMBU-P Sıcaklık` β=0.098 p=.003 zayıf flag; 3-level varyans yapısı test edilmedi | CSR §13.5 | **XXV** — 3-level (yıl × aile × satır) varyans modeli |
| 6 | HbA1c × ebeveynlik n=39 yetersiz güç; Bayesian bilgi-verici prior ile re-analiz yok | CSR §12.5.1, §16.3 | **XXIV** — HbA1c × parenting Bayesian joint model |
| 7 | H1 multiverse yapılmadı (CSR §13.6 paradoksu); H3 multiverse %0 anlamlı, H1 doğrulanmadı | CSR §13.6 | **XXVII** — H1 multiverse 240-spec + SCA inferential |
| 8 | Kesitsel tasarım — sequential ignorability kırılganlığı için Imai-Keele ρ duyarlılığı yok | CSR §16.1 | **XXV** — Imai-Keele causal mediation sensitivity |
| 9 | H2 için TOST eşdeğerlik testi ön-kayıtta yer almadı; "fark yok" yerine "kanıt yetersiz" demek zorunda kalındı | CSR §11.2.2 | **XXX** + **XXIII** — Post-hoc TOST + APIM equivalence |
| 10 | H1 Bayesian R̂=1.012-1.013 sıkı 1.01 eşiğinin hafif üzerinde — reparametrize gerekiyor | CSR §14.1 | **XXVII** + **XXVIII** — H1 multiverse + posterior predictive replication |
| 11 | Multi-informant trifactor / latent discrepancy SEM uygulanmadı; De Los Reyes 2023 Operations Triad teorik düzeyde kaldı | CSR §15.1.2 | **XX** — Trifactor T-CFA, latent discrepancy SEM, LDS, cross-informant network |
| 12 | Pinquart 2013 + Lovejoy 2000 ile formal Bayesian meta-analytic pooling yok | CSR §15.1.1, §15.4.2 | **XXVIII** — Bayesian random-effects meta-pooling |
| 13 | Yüksek-risk anne klinik tahmin modeli iç-validasyonlu; dış-validasyon protokolü yok | CSR §12.4.6, §17.4 | **XXIX** — TRIPOD-Cluster hazırlık + sNB + DCA threshold heatmap |

---

## 3. Amendment'in Kapsamı (Faz II SAP'nin Özeti)

`STATISTICAL-ANALYSIS-PLAN-PHASE-2.md` v1.0, **17 KISIM (XIX–XXXV)** ve **45 post-hoc analiz hedefi** içerir. Bu amendment'in kapsamı söz konusu plan belgesindeki tüm KISIM'leri kucaklar:

- **KISIM XIX** — Sapma disiplini ve OSF Layer 3 (bu doküman)
- **KISIM XX** — Multi-informant yapısal genişletme (4 analiz: T-CFA, LDS, latent discrepancy SEM, cross-informant network)
- **KISIM XXI** — Psikometrik robustleştirme (4 analiz: Tobit IRT, ω_h/ECV, Beck bifactor, ESEM)
- **KISIM XXII** — Antidepresan ve mental sağlık yükü (3 analiz: mediator, moderator, latent etkileşim)
- **KISIM XXIII** — H5 diadik tutarlılık genişletmesi (4 analiz: MTMM, Beck × group moderation, sibling concordance, Bayesian pooling)
- **KISIM XXIV** — Klinik stratifikasyon (4 analiz: HbA1c joint, tanı yaşı spline, glycemic trajectory pilot, ISPAD logistic)
- **KISIM XXV** — Nedensel aracılık sensitivitesi (4 analiz: Imai-Keele, PC algorithm + FCI, c' triangulation, 3-level varyans)
- **KISIM XXVI** — Distribüsyonel yaklaşımlar (3 analiz: quantile, distributional, beta regression)
- **KISIM XXVII** — Multiverse genişletme (4 analiz: H1 240-spec, H4 SEM multiverse, BMA, SCA inferential)
- **KISIM XXVIII** — Meta-analitik birleştirme (3 analiz: Bayesian pooling, PPC replication, EB shrinkage)
- **KISIM XXIX** — Klinik karar modeli dış validasyon hazırlığı (4 analiz: TRIPOD-Cluster, sNB, DCA heatmap, recalibration)
- **KISIM XXX** — Power ve replikasyon planlaması (4 analiz: simr, APIM SS, Bayesian SSD, replication protocol)
- **KISIM XXXI** — Karma yöntem (koşullu; kantitatif convergence joint display)
- **KISIM XXXII** — Çıktı entegrasyonu (12 yeni APA tablo + 8 figür + tez Bölüm 6 + Makale 4-6)
- **KISIM XXXIII–XXXV** — Risk matrisi, 12 hafta sprint plan, uygulama tracker'ı

Tüm 45 hedef için R/32 ila R/49 modülleri (`docs/analiz_planlari/STATISTICAL-ANALYSIS-PLAN-PHASE-2.md` Tablo F2-01..F2-45) tanımlıdır; her biri için test, audit script ve `_targets.R` entegrasyonu planlanmıştır.

---

## 4. Reproducibility Çapaları

Faz II analizleri kanonik veri kilidinin bütünlüğünü **tehlikeye atmaz**; tüm yeni analizler kilitli baz üzerinde işler:

- **Veri kilidi:** `FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` SHA-256 imzası DEĞİŞMEZ.
- **Yeni türetmeler:** `outputs/processed/phase2_*.rds` altında izole edilir; mevcut `data/processed/` kanonik CSV'lerine müdahale edilmez.
- **`renv.lock`:** Yeni paket eklemeleri (`mediation`, `pcalg`, `mokken`, `gamlss`, `quantreg`, `betareg`, `metafor`, `bain`, `simr`, `MOTE`) `renv::install()` + `renv::snapshot()` zinciriyle commit edilir.
- **`_targets.R`:** Yeni hedefler `phase2_*` prefix'iyle deklare edilir; mevcut hedefler değiştirilmez.
- **Audit zinciri:** Her yeni R/ modülü için `tests/test_<modül>.R` (stopifnot) + `scripts/R/<numara>_<modül>_audit.R` (CSV smoke-test) zorunludur.

---

## 5. Replikasyon Zorunluluğu

Faz II'den çıkacak hiçbir bulgu, **bağımsız bir Türk kohortunda dış-validasyon yapılmadan** klinik öneri seviyesine yükseltilmez. Faz II ile birlikte planlanan dış-validasyon protokolü:

- **Hedef merkezler:** Hacettepe Üniversitesi (Ankara), Ege Üniversitesi (İzmir), Karadeniz Teknik Üniversitesi (Trabzon), Diyabet Vakfı periferik klinikleri
- **Sample size:** Toplam 600 aile (300 DM + 300 Kontrol), merkez başına ≥ 100 aile
- **Pre-registration:** OSF Layer 4 (replication preregistration), Faz II veri analizi sonrası
- **Analiz çerçevesi:** TRIPOD-Cluster + multilevel meta-analysis (`metafor`)
- **Plan iskeleti:** `docs/analiz_planlari/REPLICATION-PROTOCOL-DRAFT.md` (Faz II içinde alt-doküman)

---

## 6. Raporlama Disiplini

Faz II bulguları aşağıdaki disiplin altında raporlanır:

1. **Etiketleme:** Her tablo, şekil ve paragraf başlığı `[KEŞİFSEL · POST-HOC]` prefiksini taşır.
2. **Konumlandırma:** Tezde **Bölüm 6: Post-Hoc Genişleme** altında raporlanır; Bölüm 5 (CSR'a paralel ana sonuçlar) ile karıştırılmaz.
3. **Dil:** "Doğruladı / desteklendi" ifadeleri kullanılmaz; bunun yerine "tutarlı yön gösterdi", "hipotez-üretici işaret üretti", "post-hoc keşifsel olarak gözlendi" tercih edilir.
4. **Sapma çapraz-referansı:** Her Faz II bulgu raporu altında `PRE-REGISTRATION-DEVIATION-TABLE.md` satır #1'e açıkça atıfta bulunulur.
5. **OSF GUID atfı:** Layer 3 GUID submit edildiğinde tüm Faz II raporlama belgelerine yansır.

---

## 7. 12-Haftalık Çalıştırma Çizelgesi

Faz II SAP §KISIM XXXIV'te detaylanan 12-haftalık sprint planı:

- **Hafta 1** — Sprint A1: KISIM XIX (bu amendment + reproducibility setup)
- **Hafta 1-2** — Sprint A2: KISIM XX (Multi-informant yapısal genişletme)
- **Hafta 3** — Sprint A3: KISIM XXI (Psikometrik robustleştirme)
- **Hafta 4** — Sprint A4: KISIM XXII (Antidepresan)
- **Hafta 5** — Sprint B1: KISIM XXIII (H5 ext)
- **Hafta 6** — Sprint B2: KISIM XXIV (HbA1c joint)
- **Hafta 7** — Sprint B3: KISIM XXV (Causal mediation + DAG)
- **Hafta 8** — Sprint B4: KISIM XXVI (Distributional)
- **Hafta 9** — Sprint C1: KISIM XXVII (Multiverse extension)
- **Hafta 10** — Sprint C2: KISIM XXVIII (Bayesian meta)
- **Hafta 11** — Sprint C3: KISIM XXIX–XXX (Clinical + Power)
- **Hafta 12** — Sprint D: KISIM XXXII (APA + thesis mapping)

Tetikleyici tarih: **2026-05-01**. Planlı bitiş: **2026-07-24**.

---

## 8. Amendment Doğrulama Akışı

```
1. Faz II SAP commit edildi → git SHA al (amendment'in son satırına eklenir)
2. Faz II veri kilidi durumu doğrulandı (kanonik lock SHA-256 değişmemiş)
3. PRE-REGISTRATION-DEVIATION-TABLE.md → Tip 3 satırı eklendi (#1)
4. OSF Layer 3 amendment formu hazırlandı (bu doküman)
5. OSF Open-Ended Registration olarak submit edildi
6. OSF GUID alındı → bu dokümanın metadata tablosuna yansıtıldı
7. STATISTICAL-ANALYSIS-PLAN-PHASE-2.md başlığında OSF GUID referans alındı
8. Faz II analiz hattı sprint A1'den itibaren başladı
```

---

## 9. Onay ve İletişim

- **PI:** Uzm.Dr. Özlem Murzoğlu Kurt (drmahirkurt@gmail.com)
- **Tez danışmanı:** Prof.Dr. Eren Özek (gözden geçirme; submit önce onay)
- **TİK:** Prof.Dr. Perran Boran, Prof.Dr. Nalan Karabayır (bilgilendirme)

---

**Tek cümlelik özet:** Bu amendment, T1DM-EBEVEYN çalışmasının çalışma-sonu verileri ışığında belirlenen 13 bilimsel boşluğu kapatmak amacıyla `STATISTICAL-ANALYSIS-PLAN-PHASE-2.md` v1.0'da tanımlı 45 post-hoc keşifsel analiz hedefini OSF Layer 3 olarak şeffaflaştırır; tüm bulgular `[KEŞİFSEL · POST-HOC]` etiketi altında, kanonik veri kilidi bütünlüğüyle ve dış-validasyon zorunluluğu beyanıyla raporlanır.
