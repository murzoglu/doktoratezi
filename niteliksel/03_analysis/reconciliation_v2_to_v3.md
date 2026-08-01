# v2 → v3 Reconciliation Raporu

**Tarih:** 2026-07-29
**Görev:** Task 1.4 — Faz 1 kanon (yeniden-inşa SDD)
**Karar:** Kullanıcı kararı = `new/` v2.0 kanonu geçersiz kılar (new supersedes v2.0)
**Statü:** Yürürlükte

---

## 1. v2.0 → v3.0 Genel Fark Tablosu

| Boyut | v2.0 (arşiv) | v3.0 (yeni kanon) | Değişim |
|---|---|---|---|
| Kanonik belge | `qualitative_canonical_results_report.md` | `theme_architecture_v3.md` + `codebook_v3.md` | Tek MD → iki ayrı belge |
| Codebook | `codebook_v2.md` (23 kod) | `codebook_v3.md` (24 kod) | +1 yeni kod |
| Veri referans biçimi | `quote_id` yalnız (verbatim yok) | `new/triadik_matris_extracted.csv` verbatim + `{aile}_{rol}_q_{eksen}` ID | Verbatim eklendi |
| Analitik yapı | 4 makro × 17 alt (tez) / 6 konu tema (journal) | 4 makro × 17 alt + **8-eksen Rosetta** | Eksen katmanı eklendi |
| Eksen yapısı | Yok (örtük) | 8 triadik eksen: `hastalik_algisi` · `kisit` · `gunluk_sosyal` · `ergenlik` · `kaybetme_korkusu` · `kardes_yasantisi` · `annelik_donusum` · `ihtiyaclar` | Yeni katman |
| Yazım hatası | `AILE_ICI_ADELET` (notlanmış, henüz düzeltilmemiş) | `AILE_ICI_ADALET` | Düzeltildi |
| Yeni kod | — | `KARDES_KORUYUCU_ROLU` | +1 |
| Kaldırılan kod | — | — | Yok |
| Journal tema yapısı | 6 tema (konu-organize, manuscript v2 temeli) | v3 tema mimarisinde 6-tema yapısı henüz güncel değil; tez yapısı (4 makro) kanonik | v3 tez-odaklı |
| Arşiv durumu | `niteliksel/archive/2026-07-29_pre_new_canon/` | — | Arşivde, silinmedi |

---

## 2. Tema Adı Karşılaştırması

### 2.1 Makro Tema Adları

| # | v2.0 Makro Tema Adı | v3.0 Makro Tema Adı | Fark |
|---|---|---|---|
| T1 | GÖLGEDEKİ ÇOCUKLAR — Paylaşılan Kısıtlılık ve Görünmez Yük | Sağlıklı kardeşin görünmeyen yükü | Soyutlama azaltıldı, başlık sadeleşti |
| T2 | ANNELİKTE EKSEN KAYMASI — "Sağlıklı Çocuk Annesi"nden "Tıbbi Bakıcı"ya | Anneliğin tıbbi bakıcıya kayması | Benzer anlam, daha özlü ifade |
| T3 | "HASTALIĞIN İÇİNDEN" — T1DM'li Çocuğun Yaşam Deneyimi | Hastalığın içinden: T1DM'li çocuk | Tırnak kaldırıldı, alt başlık kısaldı |
| T4 | AYNI EV, ÜÇ FARKLI DENEYİM — Triadik Karşılaştırmalı Okuma | Aynı evde üç farklı deneyim (triadik) | Özdeş çekirdek, kısa biçim |

**Not:** Makro tema sayısı (4) ve perspektif örgütleme mantığı değişmedi. v3 adları daha kısa ve doğrudan; v2 adlarının belirgin şekilde öne çıkardığı "BÜYÜK HARF" vurgu tonu terk edildi.

### 2.2 Alt-Tema Sayısı

| Makro Tema | v2.0 Alt-tema | v3.0 Alt-tema | Fark |
|---|---|---|---|
| T1 | 3 alt + 4 boyut | 3 alt | Boyut → eksen katmanına taşındı |
| T2 | 6 alt | 6 alt | Değişmedi |
| T3 | 4 alt | 4 alt | Değişmedi |
| T4 | 4 alt | 4 alt | Değişmedi |
| **Toplam** | **17 alt** | **17 alt** | **Aynı** |

### 2.3 Journal Tema Yapısı

v2.0'da manuscript v2 için 6 konu-organize tema (J1-J6) ayrıca belgelenmişti. v3.0 tez-odaklı olup 4 makro tema + 8-eksen Rosetta'ya odaklanmıştır; 6-tema journal yapısı v3.0 mimarisine henüz aktarılmamıştır. Bu açık nokta Task 1.5+ kapsamındadır.

---

## 3. Kod Farkları

### 3.1 Yeni Kod: KARDES_KORUYUCU_ROLU

| Alan | İçerik |
|---|---|
| **Kod ID** | `KARDES_KORUYUCU_ROLU` |
| **Kategori** | Kategori 4 — Aile İlişkileri ve Rollerin Dönüşümü |
| **Gerekçe** | v2.0'da "Nöbetçi Kardeş" rolü T1 alt-tema 1.2 olarak tema düzeyinde tanımlanmıştı; ancak bu örüntü kod düzeyinde ayrı bir kimlik gerektiriyordu. Triadik CSV'de `kardes_yasantisi` ve `kaybetme_korkusu` eksenlerinde sağlıklı kardeşin aktif koruyucu davranışları (uyarı, takip, acil müdahale) KARDES_GORUNMEZ_YUK'tan analitik olarak ayrıştırılabilir biçimde ortaya çıktı. |
| **v2.0'daki durumu** | v2.0 "v3'te yeni kod olarak düşünülebilir" notuna yer veriyordu; Task 1.3'te hayata geçirildi. |

### 3.2 Yazım Düzeltmesi: AILE_ICI_ADELET → AILE_ICI_ADALET

v2.0'da yazım hatası fark edilmiş ve "v3'te düzeltilecek" notu düşülmüştü. v3.0'da kanonik ID `AILE_ICI_ADALET` olarak güncellendi. Kod tanımı ve kapsamı değişmedi.

### 3.3 Tam Kod Sayısı

- **v2.0:** 23 kod (5 kategori)
- **v3.0:** 24 kod (5 kategori) — net +1 (KARDES_KORUYUCU_ROLU eklendi, kaldırılan yok)

---

## 4. Veri Referans Biçimi Farkı

### v2.0: quote_id-only

v2.0 kanonik raporu KVKK gereği yalnız `quote_id` (ör. `020_mother_q001`) referans veriyordu; verbatim alıntı dosyaya eklenmemişti. Verbatim içerik yalnız temizlenmiş transkript dosyalarında bulunuyordu.

### v3.0: verbatim + yapılandırılmış eksen kolonu

`new/triadik_matris_extracted.csv` şu kolonları taşır: `aile_no`, `rol`, `triadik_eksen`, `verbatim_tr`. Bu yapı:

- Her satır bir birim (katılımcı × eksen gözlemi)
- `quote_id` biçimi: `{aile_no}_{rol}_q_{eksen}` (ör. `019_mother_q_gunluk_sosyal`)
- `triadik_eksen` sütunu analitik navigasyonu sağlar
- Verbatim verisi çalışma dosyasında kalmakta; tez metnine yalnız seçilmiş ve anonimleştirilmiş alıntılar girmektedir

**KVKK notu:** Bu verbatim veri özel nitelikli sağlık + çocuk verisidir. CSV dosyası repo dışına çıkmaz; harici MCP/connector'a gönderilmez.

---

## 5. "new supersedes" Gerekçesi

Kullanıcı kararı (2026-07-29 Task 1.4 brief) olarak:

> "Kullanıcı kararı = 'new/ v2.0 kanonu geçersiz kılar.'"

Teknik gerekçe:

1. **Verbatim varlığı:** `new/triadik_matris_extracted.csv` gerçek görüşme gözlemlerini eksen-yapılandırmalı olarak içermektedir; v2.0'ın yalnızca quote_id içeren statik raporundan analitik olarak daha zengindir.
2. **Eksen tutarlılığı:** 8-eksen Rosetta, kodlar ile tema alt-bölümleri arasında doğrudan navigasyon sağlar; v2.0'da bu bağlantı örtüktü.
3. **Kod tamamlanması:** KARDES_KORUYUCU_ROLU v2.0'da vaat edilen ama hayata geçirilmemiş bir koddu; v3.0 bunu tamamladı.
4. **Yazım bütünlüğü:** AILE_ICI_ADALET düzeltmesi v3.0'da hayata geçirildi.
5. **Tek gerçeklik kaynağı:** İki paralel kanonik belge (v2.0 + v3.0) çakışma riski oluşturur; arşivleme bu riski kaldırır.

---

## 6. Korunan v2.0 Kararları (Arşive GİTMEYEN)

Aşağıdaki kararlar v2.0'a ait olup `niteliksel/03_analysis/methodology/` altında kalmaya devam etmektedir. Bu kararlar "v2.0 metodoloji paketi" olarak kanonik değerini korur:

| Karar | Dosya | Neden korunuyor |
|---|---|---|
| COREQ-32 metodoloji denetimi (30 tam / 2 kısmi) | `methodology/coreq_checklist.md` | Raporlama standardı değişmedi |
| Positionality beyanı (OM birinci kodlayıcı / BA critical friend) | `methodology/positionality_statement.md` | Araştırmacı rolleri değişmedi |
| Audit trail kayıtları | `methodology/audit_trail.md` | Lincoln-Guba güvenilirliği için zorunlu |
| Inter-coder reliability hesaplanmamasının gerekçesi | `methodology/inter_coder_rationale.md` | RTA epistemoloji kararı değişmedi |
| LLM kullanım beyanı (ICMJE/COPE) | `methodology/llm_use_statement.md` | AI şeffaflık yükümlülüğü devam ediyor |

**Özet:** Metodoloji kararları v2.0'ın kurumsal mirasıdır ve v3.0 tarafından geçersiz kılınmamıştır. Yalnızca analitik çıktı (tema mimarisi + codebook) yenilendi.

---

## 7. Eski Yolların Durumu

| Eski yol | Yeni durum |
|---|---|
| `niteliksel/qualitative_canonical_results_report.md` | `niteliksel/archive/2026-07-29_pre_new_canon/qualitative_canonical_results_report.md` |
| `niteliksel/03_analysis/codebook/codebook_v2.md` | `niteliksel/archive/2026-07-29_pre_new_canon/codebook_v2.md` |

Eski yollara yapılan referanslar (`niteliksel/CLAUDE.md`, `SKILL.md`, `codebook_v2.md` doğrudan referanslar) bu görev kapsamında güncellendi.

---

## 8. Açık Noktalar / Sonraki Görevler

1. **Journal tema (6 tema) v3 entegrasyonu:** v2.0'daki J1-J6 konu-organize yapısının v3 Rosetta eksen tablosuyla eşleşmesi Task 1.5+ kapsamındadır.
2. **COREQ denetim güncellemesi:** v3 kanonik belgesiyle COREQ 32 madde uyum durumu teyit edilmelidir.
3. **Negatif vaka kayıtları:** v3'e negatif vaka / sınırlayıcı örüntü bölümü eklenmesi (v2.0 Bölüm 9 muadili).
4. **Quote havuzu senkronizasyonu:** v2.0'daki 116 quote_id havuzunun `{aile}_{rol}_q_{eksen}` biçimine dönüşümü.

---

*Bu belge Task 1.4 çıktısıdır. Metodoloji kararları için `03_analysis/methodology/`; kanonik analitik kaynaklar için `03_analysis/codebook/codebook_v3.md` ve `03_analysis/codebook/theme_architecture_v3.md` esastır.*
