# T1DM Niteliksel Tez — Yapılanlar/Yapılacaklar Tracker

**Son güncelleme:** 2026-05-04 (v7) — **FAZ A TAMAMLANDI**
**Yol haritası kaynağı:** [ROADMAP_v1.md](ROADMAP_v1.md)
**Skill:** `niteliksel-arastirma-rehberi-t1dm`

> Bu belge **canlı tracker**. Her ilerleme/karar sonrası güncellenir; sürüm günü ile birlikte alttaki "Update Log" bölümüne kaydedilir.
>
> **2026-08-01 kanon notu:** Güncel codebook `03_analysis/codebook/codebook_v3.md`'dir. Aşağıdaki v1/v2 kayıtları tarihsel ilerleme izidir; ilgili dosyalar `99_archive/2026-07-29_pre_new_canon/` altında korunur.

---

## Özet Metrik

| Metrik | Sayı |
|---|---|
| ✅ DONE | 32 (14 önceden + 8 karar + 10 Faz A paketi) |
| 🔄 WIP | 0 |
| ⏸ BLOCKED | 0 |
| 📋 TODO | 17 (Faz B/Cf/D) |
| **Toplam paket** | **49** |

**Legend:** ✅ DONE · 🔄 WIP · ⏸ BLOCKED · 📋 TODO · ⚠️ RISK · 🚫 N/A

---

## C — Karar Noktaları (öncelik 0; A başlamadan netleşmeli)

| # | Soru | Status | Yanıt | Etki |
|---|---|---|---|---|
| C.1 | Tez teslim takvimi? | ✅ | **Kalite öncelikli** (sıkı takvim yok) | Faz süreleri esnek; her paket uzayabilir |
| C.2 | Niteliksel kol için OSF kaydı? | ✅ | **Tez sonrası** planlanıyor | A.7 KVKK DMP iç-kullanım için yapılacak; D.1 tez sonrası |
| C.3 | Pediatric Diabetes manuscript? | ✅ | **Hazırlanıyor** (henüz submit edilmemiş) | D.2 paralel olarak revize edilebilir; tez bulguları + manuscript birlikte gelişir |
| C.4 | LLM kullanımı? | ✅ | **Yazım yardımcısı** (kodlama değil, metin yazımı) | **A.8 zorunlu** — LLM Use Statement gerekli (kodlama beyan değil ama yazım beyan zorunlu) |
| C.5 | OSF planı? | ✅ | **Ayrı niteliksel proje** | D.1: t1dm-tez-rehberi'ye cross-link; tez sonrası ayrı OSF açılacak |
| C.6 | Tez yapısı? | ✅ | **KARMA** (nicel + niteliksel birlikte) | **B.1 + B.2 önemli ima**: t1dm-tez-rehberi skill'i ile **koordineli** çalışmak gerek; nicel arm da Giriş/Bulgular/Tartışma'da yer alacak |
| C.7 | Member-checking? | ✅ | **Yapıldı, dokümante edilmedi** (görüşme-içi özetleme yapılmış; tarihli kayıt yok) | A.5 audit trail'de "in-interview member reflection" olarak konumlandırılacak; B.5 tartışmada açık sınır + uygulanan strateji birlikte raporlanacak |
| C.8 | Tez tema yapısı? | ✅ | **Hibrit** (6 tema ↔ 4 makro tema mapping) | A.6 codebook v2 mapping üretmeli; B.4 yapısı: 4 makro şemsiye + 6 alt-tema iç içe |

---

## A — Kalite Pekiştirme (~2-3 hafta · 10 paket)

| # | Paket | Status | Bağımlılık | Skill ref | Çıktı |
|---|---|---|---|---|---|
| A.1 | "Doygunluk" → "bilgi gücü" reframe (Malterud) | ✅ | — | `02-orneklem-bilgi-gucu.md` | **Tamamlandı:** [`A1_information_power.md`](../03_analysis/methodology/A1_information_power.md) deliverable + cleaned thesis text 2 yer (Örneklem Seçimi, Veri Toplama) revize edildi + Tablo X.X eklendi |
| A.2 | COREQ 32-madde **doldurulmuş** kontrol listesi | ✅ | A.1 | `assets/coreq-32-madde-tr.md` | **Tamamlandı:** [`coreq_32_completed.md`](../03_analysis/methodology/coreq_32_completed.md) — 30/32 tam + 2 kısmi (Madde 16 pilot, Madde 31 negatif vaka) + boşluk doldurma planı; Domain 1: 7/7, Domain 2: 14/15+1, Domain 3: 9/10+1 |
| A.3 | Positionality statement (TR + EN; OM + BA) | ✅ | — | `assets/positionality-tr.md` | **Tamamlandı:** [`positionality_OM.md`](../03_analysis/methodology/positionality_OM.md) + [`positionality_BA.md`](../03_analysis/methodology/positionality_BA.md) — TR+EN paralel, kişiselleştirme alanları `{KÖŞELİ AYRAÇ}` ile işaretli |
| A.4 | Refleksif günlük örnekleri (n=3-5 anonim girdi) | ✅ | — | `assets/refleksif-gunluk-sablonu-tr.md` | **Tamamlandı:** [`journal_excerpts.md`](../03_analysis/reflexive/journal_excerpts.md) — şablon + 3 örnek girdi (post-interview / post-coding / critical-friend) + Durum Beyanı (formel günlük yok, mental+memo+ekip tartışması var; A.5 audit trail'a referans + sınırlılık raporlama önerisi) |
| A.5 | Audit trail tablosu (codebook revizyon + OM-BA tartışma) | ✅ | A.6 | `assets/audit-trail-log-tr.md` | **Tamamlandı:** [`audit_trail.md`](../03_analysis/methodology/audit_trail.md) — 15 metodolojik karar (MK.01-15) + codebook v1→v2 sürüm geçmişi + 4 critical friend tartışma özeti (CF.01-04) + 10 açık konu (AÇ.01-10) + güncelleme protokolü |
| A.6 | Codebook v2 + tema-kod-aile haritası (hibrit 6↔4 mapping) | ✅ | — | `04-rta-6-faz-derinlemesine.md` | **Tamamlandı:** [`codebook_v2.md`](../99_archive/2026-07-29_pre_new_canon/codebook_v2.md) — 23 kod × 6 journal tema × 4 thesis makro tema mapping + 22 alt-tema Rosetta + aile×tema odak matrisi + B.4 yazım yönergesi |
| A.7 | KVKK Veri Yönetim Planı | ✅ | — | `09-etik-kvkk-refleksivite.md` | **Tamamlandı:** [`kvkk_data_management_plan.md`](../01_raw_data/ethics_protocol/kvkk_data_management_plan.md) — özel nitelikli sağlık + çocuk verisi için 9 bölümlü DMP (yaşam döngüsü, anonimleştirme, k-anonymity, erişim kontrolü, breach response, çocuk için ek korumalar, onam uyumu, sürüm) |
| A.8 | LLM kullanım beyanı (yazım için) | ✅ | — | `assets/llm-kullanim-beyani-tr.md` + `06-llm-destekli-kodlama.md` | **Tamamlandı:** [`llm_use_statement.md`](../03_analysis/methodology/llm_use_statement.md) — TR+EN açık beyan, kapsam (yazım yardımcısı, ham veri yok), KVKK uyum, halüsinasyon kontrol protokolü, OSF prompt log mimarisi, APA/COPE uyumluluk |
| A.9 | Triadic methodology literatürü ekleme | ✅ | — | `12-t1dm-tezi-spesifik-uyarlamalar.md` | **Tamamlandı:** [`A9_triadic_methodology_literature.md`](../03_analysis/methodology/A9_triadic_methodology_literature.md) — 14 atıf (Eisikovits & Koren, Morgan, Taylor & de Vocht, Patton, Carter, Sullivan-Bolyai, Smaldone, Whittemore, Streisand, Loeb, Voltelen, Phelps & Mok, Braun & Clarke, Flick). Cleaned thesis text'te 2 paragraf güncellendi (Araştırma Tasarımı + Veri Analizi) |
| A.10 | Jüri savunma argümanları taslağı | ✅ | A.1 + A.2 | `11-yazim-ve-jurinin-soracaklari.md` | **Tamamlandı:** [`defense_arguments.md`](../03_analysis/methodology/defense_arguments.md) — 15 olası soru × çekirdek argüman + 3-slayt savunma haritası + tonlama stratejisi + Boyatzis-tipi karşı argüman + pre-savunma kontrol listesi |

---

## B — Tez Bölüm Yazımı (~4-6 hafta · 6 bölüm)

| # | Bölüm | Status | Bağımlılık | Tahmini süre |
|---|---|---|---|---|
| B.1 | Giriş & Amaç | 📋 | C.6 | 1 hafta |
| B.2 | Genel Bilgiler (literatür) | 📋 | — | 1.5 hafta |
| B.3 | Yöntem (genişletilmiş) | 📋 | A.1-A.10 | 1 hafta |
| B.4 | Bulgular (4-makro-tema veya 6-tema) | 📋 | A.6 + C.8 | 2 hafta |
| B.5 | Tartışma & Sonuç | 📋 | B.4 + C.7 | 1.5 hafta |
| B.6 | Türkçe + İngilizce Özet | 📋 | B.1-B.5 | 0.5 hafta |

---

## Cf — Format & Compliance (~2-3 hafta · 6 paket)

| # | Paket | Status | Bağımlılık |
|---|---|---|---|
| Cf.1 | Marmara şablonu (kapak, onay, beyan, içindekiler) | 📋 | B son |
| Cf.2 | Kaynakça (Marmara stilinde) | 📋 | B son |
| Cf.3 | Ekler (görüşme rehberi, COREQ tablo, codebook, demografik tablo, positionality, refleksif günlük örnekleri, audit trail) | 📋 | A son + B son |
| Cf.4 | Tablolar + şekiller (görsel kalite kontrol) | 📋 | B son |
| Cf.5 | Yazım denetimi + Türkçe APA 7 | 📋 | B son |
| Cf.6 | JARS-Qual + SRQR ek kontrol listeleri | 📋 | A.2 |

---

## D — Yayım & Savunma (paralel + son · 5 paket)

| # | Paket | Status | Bağımlılık |
|---|---|---|---|
| D.1 | OSF kaydı + ön-kayıt sapma tablosu (retrospektif) | 📋 | C.2 + C.5 |
| D.2 | Pediatric Diabetes manuscript revizyon | 📋 | A.1-A.5 |
| D.3 | Tez ön-savunma (ön savunma feedback toplama + düzeltme) | 📋 | C tamamlanması |
| D.4 | Tez esas savunma | 📋 | D.3 |
| D.5 | Yayım stratejisi (sağlıklı kardeş + triadic karşılaştırma makaleleri) | 📋 | D.4 sonrası |

---

---

## 🎯 FAZ A ÖZETİ (2026-05-04 günü tamamlandı)

**Üretilen belgeler (10):**
1. [`A1_information_power.md`](../03_analysis/methodology/A1_information_power.md) — Malterud bilgi gücü 5-boyut tablosu + reframe paragrafları
2. [`codebook_v2.md`](../99_archive/2026-07-29_pre_new_canon/codebook_v2.md) — 23 kod × 6 journal × 4 thesis hibrit master
3. [`positionality_OM.md`](../03_analysis/methodology/positionality_OM.md) — TR+EN
4. [`positionality_BA.md`](../03_analysis/methodology/positionality_BA.md) — TR+EN
5. [`journal_excerpts.md`](../03_analysis/reflexive/journal_excerpts.md) — şablon + 3 örnek + Durum Beyanı
6. [`A9_triadic_methodology_literature.md`](../03_analysis/methodology/A9_triadic_methodology_literature.md) — 14 atıf, 4 grup
7. [`kvkk_data_management_plan.md`](../01_raw_data/ethics_protocol/kvkk_data_management_plan.md) — 9 bölüm DMP
8. [`llm_use_statement.md`](../03_analysis/methodology/llm_use_statement.md) — TR+EN açık beyan
9. [`coreq_32_completed.md`](../03_analysis/methodology/coreq_32_completed.md) — 30/32 tam + 2 kısmi
10. [`audit_trail.md`](../03_analysis/methodology/audit_trail.md) — 15 MK + sürüm + 4 CF + 10 AÇ
11. [`defense_arguments.md`](../03_analysis/methodology/defense_arguments.md) — 15 soru + 3 slayt

**Cleaned thesis text güncellemeleri (4 yer):**
- Yöntem § Örneklem Seçimi: bilgi gücü gerekçelendirme paragrafı + Tablo X.X (A.1)
- Yöntem § Veri Toplama: "veri doygunluğu" paragrafı yeniden yazıldı (A.1)
- Yöntem § Araştırma Tasarımı: Eisikovits-Morgan-Taylor-Sullivan-Bolyai atıf paragrafı (A.9)
- Yöntem § Veri Analizi: Patton-Carter-Braun&Clarke atıfları + RTA-uyumlu triangulation çerçevesi (A.9)

**Açık tutulan konular (Faz B/C/D'ye taşınanlar):**
- AÇ.01-10 audit trail'da listelenmiş (görüşme rehberi pilot, 4 doğrulanmamış aile odağı, prompt log paylaşım kararı vb.)
- Codebook v3 önerileri: yazım hatası düzelti, performatif normallik alt-katmanı, T1.3 boyutlarının ayrıştırılması
- COREQ kısmi maddeler (16, 31): B.4'te güçlendirme

---

## ✅ Yapılanlar (önceden tamamlanmış · 14 paket)

| # | Çıktı | Konum |
|---|---|---|
| ✅1 | Etik protokol (DM Parenting Attitudes 2023-02) | `01_raw_data/ethics_protocol/dm_parenting_attitudes_ethics_protocol_2023_02.docx` |
| ✅2 | Görüşme rehberi (anne/hasta/kardeş) | `01_raw_data/interview_guides/qualitative_interview_questions.docx` |
| ✅3 | Demografik form | `01_raw_data/demographics/qualitative_demographics.docx` |
| ✅4 | 21 görüşme transkripti (DOCX) | `01_raw_data/interviews_docx/family_{011,014,019,020,026,201,202}/` |
| ✅5 | Birleştirilmiş transkript (Markdown) | `02_processed/transcripts/all_transcripts_merged.md` |
| ✅6 | Cleaned thesis YÖNTEM taslağı (~12k kelime) | `02_processed/cleaned_text/thesis_qualitative_cleaned_current.md` |
| ✅7 | Codebook v1 (24 kod, 5 kategori) | `03_analysis/codebook/codebook_draft_v1.md` |
| ✅8 | COREQ-uyumlu Method iskeleti (skeleton) | `03_analysis/methodology/methodology_skeleton_coreq.md` |
| ✅9 | 6 tema triadic matrix v3 (theme_01-06) | `03_analysis/triadic_matrices/` |
| ✅10 | Theme comparison spreadsheet | `03_analysis/spreadsheets/theme_comparison.ods` + `triadic_table.xlsx` |
| ✅11 | Mother thematic memo | `03_analysis/thematic_memos/mother_theme_memo.docx` |
| ✅12 | Pediatric Diabetes manuscript v2 (Results+Discussion, journal-ready) | `04_manuscripts/journal_pediatric_diabetes/pediatric_diabetes_results_discussion_draft_v2_journal_ready.docx` |
| ✅13 | Refleksif notlar (Method metninde gömülü) | `02_processed/cleaned_text/...` (ayrı dosya yok ⚠️) |
| ✅14 | Critical friend süreci (BA) | Method metninde belgelenmiş; tarihli audit trail yok ⚠️ |

---

## Update Log

- **2026-05-04 v1** — İlk tracker; ROADMAP_v1.md temel alındı; 14 yapılan + 35 yapılacak paket envanterlendi; C.1-C.8 karar soruları kullanıcıya yöneltildi.
- **2026-05-04 v2** — C.1-C.8 yanıtları alındı: kalite öncelikli, tez sonrası OSF, manuscript hazırlanıyor, LLM yazım yardımcısı, ayrı niteliksel OSF, **karma tez**, member-checking yapılmış (in-interview, tarihli kayıt yok), **hibrit tema yapısı**. A.7 ve A.8 unblock oldu. A.1 başlatıldı (🔄 WIP). Karma tez kararı B.1+B.2'ye `t1dm-tez-rehberi` skill koordinasyonu ekledi.
- **2026-05-04 v3** — **A.1 ✅** — `A1_information_power.md` deliverable üretildi (~1500 kelime, Malterud 5-boyut tablosu + 2 paragraf revize + atıflar + jüri savunma çekirdek argümanları). Cleaned thesis text'e iki Edit uygulandı: (a) Örneklem Seçimi sonuna bilgi gücü gerekçelendirme paragrafı + Tablo X.X eklendi; (b) Veri Toplama'daki "veri doygunluğu" paragrafı tamamen yeniden yazıldı. "Tematik doygunluk" / "veri doygunluğuna ulaşıldı" ifadeleri kaldırıldı; Braun-Clarke 2021 epistemik tutum + Malterud 2016 bilgi gücü çerçevesine geçildi. **A.6 başlatıldı (🔄 WIP)** — codebook v1 + 6 tema triadic matrices + 4 makro tema arası hibrit mapping üretilecek.
- **2026-05-04 v4** — **A.6 ✅** — `codebook_v2.md` üretildi: 23 kod (v1'de 24 sayım hatası düzeltildi) × 6 journal tema × 4 thesis makro tema hibrit master mapping. Triadic matrices'ten 6 journal tema + 22 alt-tema isimleri çıkarıldı. Journal-Thesis "Rosetta" tablosu (alt-tema karşılığı) + Aile×Tema odak matrisi (A11/A14/A19/A20/A26/A201/A202) eklendi. Bilinen düzelti: `AILE_ICI_ADELET` → `AILE_ICI_ADALET` (v3'te uygulanacak). 4 odak ailenin belirsiz olduğu sub-temalar (J2.1, J2.2, J3.3, J5.4) A.5 audit trail için flag'lendi. **A.3 başlatıldı (🔄 WIP)** — OM ve BA için positionality statement (TR+EN).
- **2026-05-04 v5** — **A.3 ✅** — `positionality_OM.md` ve `positionality_BA.md` üretildi (TR+EN paralel). OM: hekim+sosyal pediatri doktora, klinik bakış açısı, empatik aşırı-yorum, kuramsal yatkınlıklar (Bowen+pediatrik kronik hastalık), önlüksüz görüşme stratejisi. BA: gözlemci+critical friend ikili rolü, disiplin-içi paylaşılan kör nokta riski, paralinguistik kayıt seçim etkisi, eleştirel arkadaş yorumlarının ikincilliği. Her iki belgede `{KÖŞELİ AYRAÇ}` ile kişiselleştirme alanları işaretlendi (yıl, doğum/anne durumu, danışman ismi vb. kullanıcı tarafından doldurulacak). **A.4 başlatıldı (🔄 WIP)** — refleksif günlük örnekleri (n=3-5 anonim girdi).
- **2026-05-04 v6** — **A.4 ✅ + A.9 ✅** — A.4: `journal_excerpts.md` üretildi (şablon + 3 örnek girdi + Durum Beyanı; formel tarihli günlük tutulmamış olduğunu dürüst raporlama önerisi A.5 ve B.5'e bağlandı). A.9: `A9_triadic_methodology_literature.md` üretildi (14 atıf 4 grupta: multi-informant family / triadic-dyadic interview / triangulation / pediatrik T1DM literatürü); cleaned thesis text'te 2 paragraf güncellendi (Araştırma Tasarımı'na Eisikovits-Morgan-Taylor-Sullivan-Bolyai-Whittemore atıfları + Veri Analizi'na Patton-Carter-Braun&Clarke atıfları + RTA-uyumlu triangulation çerçevesi). **A.7 başlatıldı (🔄 WIP)** — KVKK Veri Yönetim Planı.
- **2026-05-04 v7** — **🎯 FAZ A TAMAMLANDI** — A.7 (KVKK DMP, 9 bölüm), A.8 (LLM beyan TR+EN), A.2 (COREQ 30/32+2 kısmi), A.5 (audit trail: 15 MK + codebook geçmişi + 4 CF + 10 AÇ), A.10 (15 olası soru + 3 slayt + tonlama). **Tüm 10 Faz A paketi ✅**. Faz A sentezi: niteliksel kolun metodolojik altyapısı (örneklem yeterliliği gerekçesi, hibrit tema yapısı, refleksivite belgeleri, etik+KVKK uyumu, raporlama standartları, savunma hazırlığı) tamamen kuruldu. Cleaned thesis text 4 noktada güncellendi (A.1: 2 paragraf, A.9: 2 paragraf). 9 yeni belge `03_analysis/methodology/` ve `01_raw_data/ethics_protocol/` ve `03_analysis/codebook/` ve `03_analysis/reflexive/` altında. **Faz B (Tez Bölüm Yazımı, ~4-6 hafta) için zemin hazır.**
