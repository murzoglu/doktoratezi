# Tasarım Belgesi — Tezin Niteliksel Kolunun Baştan İnşası

- **Tarih:** 2026-07-29
- **Dal:** feat/qc-otomatik-zorlama-kapsam
- **Süreç:** superpowers:brainstorming → (bu spec) → superpowers:writing-plans
- **Alan skill:** niteliksel-arastirma-rehberi-t1dm (otör-yetkinlik kapısı)
- **Bağlayıcı talimatname:** `tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md`

## 1. Amaç ve bağlam

Tezin niteliksel kolu (Tip 1 Diyabet & ebeveynlik tutumu; anne–T1DM'li çocuk–sağlıklı
kardeş triadı) `niteliksel/new/` altına yeni eklenen kaynak materyaller ışığında **baştan
aşağı** yeniden kurulacaktır. Yeni ilkeler:

1. **COREQ tam uyum** (32 madde; 30 tam + 2 kısmi şeffaf raporlama).
2. **Orijinal alıntılara sadakat** — `quote_id` ankrajları yerine **verbatim alıntı**
   (KVKK sınırı, aşağıda tanımlı de-identify zemininde gevşetilir).
3. **Triadik tasarımın öne çıkarılması** — `triadik tablo.xlsx` (21 bilgi verici × 8 eksen)
   within-case/cross-case omurga olarak.

### 1.1 Kaynak materyaller (`niteliksel/new/`)

| Dosya | Rol |
|---|---|
| `triadik tablo.xlsx` | 21 bilgi verici (7 aile × 3) × 8 tematik eksen **verbatim alıntı matrisi** (omurga) |
| `nitel ana.docx` | Ana niteliksel makale taslağı: Yöntem + Bulgular (4 makro tema, 17 alt-tema) |
| `nitel chat.docx` | İkiz taslak (YORUM/TARTIŞMA blokları eklenmiş); `ana` ile tekilleştirilecek |
| `nitel coreq uyumlu.docx` | COREQ-tam Yöntem (13 başlık); etik onay 09.2023.201; 06.07.2023–25.10.2023 |
| `Niteliksel demografik.docx` | Aile künyesi (7 aile: 11/14/19/20/26/201/202); doğum+tanı tarihleri içerir |
| `Niteliksel Araştırma Soruları.docx` | Görüşme rehberi (ana + rol-başı sorular); planlama metni "6 aile" der (eski) |
| `covid nitel.pdf` | Şenkal ve ark. 2023, DOI 10.1111/cch.13099 — aynı grubun referans/örnek makalesi |

### 1.2 Tezde niteliksel içeriğin mevcut konumu

- `chapters/03_gerec_ve_yontem.qmd:181` — "Nitel Kol" (6 alt-bölüm; metodolojik olarak sağlam, atıflı).
- `chapters/04_bulgular.qmd:1376` — "Niteliksel Kol Bulguları": Tema 1–4 **özet tablo + `quote_id`
  ankrajı** (verbatim YOK) + Joint Display (`:1530`).
- `chapters/05_tartisma_ve_sonuc.qmd` — temalar dokulu (özel başlık yok).
- `chapters/02_genel_bilgiler.qmd` — nitel arka plan.
- `chapters/07_ekler.qmd` — nitel ek yok/eksik.

### 1.3 Mevcut kanon (`niteliksel/`)

`qualitative_canonical_results_report.md` (v2.0, 1127 satır), `03_analysis/codebook/codebook_v2.md`
(23 kod × 5 kategori × 4 makro/6 journal tema), `03_analysis/methodology/*` (COREQ-32, audit-trail,
positionality OM/BA, information power, defense arguments, LLM statement). Bu kanon **ham veri olmadan,
`quote_id` bazlı** kuruldu.

## 2. Kilit kararlar (kullanıcı onaylı)

| # | Karar | Seçim |
|---|---|---|
| K1 | **Alıntı etiketi** | Verbatim + **(Aile no, rol, yaş)** — ör. `(Aile 11, sağlıklı kardeş, 9 yaş)`. Gerçek ad/doğum tarihi hiçbir yerde yayımlanmaz (onam anonimlik taahhüdü zemini). |
| K2 | **Kanon ilişkisi** | **`new/` v2.0 kanonu geçersiz kılar.** v2.0 arşive; tema mimarisi/kod yapısı `new/`'den yeniden kurulur; v2↔v3 farkı raporlanır. |
| K3 | **Kapsam** | ch02 + ch03 + ch04 + ch05 + ch07 (tam tez niteliksel + ek). |
| K4 | **Demografi sunumu** | Yayımlanan tezde **türetilmiş yaş/süre** (tarih yok). Analiz katmanında (`niteliksel/`) tam veri korunur. |

## 3. Mimari (iki katman, tek doğruluk kaynağı `new/`)

```
new/ (ham kaynak) ─▶ KANON KATMANI (niteliksel/, provenance) ─▶ TEZ KATMANI (chapters/, yayımlanan)
```

**Değişmez ilke:** Tez metnindeki her verbatim alıntı, kanon katmanındaki alıntı kayıt
defterinden bir `quote_id` ile izlenebilir (COREQ M25 + audit-trail + quote-parity).

## 4. Kanon katmanı yeniden inşası (`niteliksel/`, tez metninden önce)

1. **Alıntı kayıt defteri** — `niteliksel/03_analysis/quotes/quotes_used_v3.csv`:
   `quote_id` (ör. `011_mother_hastalik_algisi_01`), `verbatim_tr`, `aile_no`, `rol`
   (mother/patient/healthy_sibling), `yas`, `triadik_eksen`, `kod(lar)`, `makro_tema`.
   Kaynak: `triadik tablo.xlsx` dolu hücreleri + `nitel ana` gövde alıntıları; `ana`/`chat`
   çakışmaları tekilleştirilir.
2. **Yapılandırılmış triadik matris** — `niteliksel/03_analysis/quotes/triadik_matris_v3.{csv,md}`:
   7 aile × 3 rol × 8 eksen; within-case (aile içi 3 ses) + cross-case (aileler arası) okuma.
3. **Tema mimarisi v3** — `new/`'e göre 4 makro tema + 17 alt-tema; **8 triadik eksene "Rosetta"
   haritası**. `codebook_v3.md` (kod ↔ eksen ↔ makro-tema). `reconciliation_v2_to_v3.md` v2↔v3
   farkını (K2 gereği) açıkça raporlar.
4. **COREQ-32 + trustworthiness** — `new/ coreq uyumlu.docx`'ten tazelenir; positionality OM/BA,
   audit-trail, LLM beyanı new/ ile uyumlanır.
5. **v2.0 arşivleme** — `qualitative_canonical_results_report.md` + `codebook_v2.md` →
   `niteliksel/archive/2026-07-29_pre_new_canon/` ("supersededby: new/" notuyla).

## 5. Tema mimarisi (somut; `new/ nitel ana`'dan)

**4 makro tema / 17 alt-tema** (perspektif-örgütlü), 8 triadik eksene bağlı:

| Makro tema | Alt-temalar | Baskın eksen(ler) |
|---|---|---|
| **T1 — Sağlıklı kardeşin görünmeyen yükü** | 1.1 gönüllü mahrumiyet/vekâleten üzüntü · 1.2 erken olgunlaşma/nöbetçi kardeş · 1.3 algılanan adaletsizlik/hasta otoritesi | Sağlıklı kardeşin yaşantısı; Kısıt |
| **T2 — Anneliğin tıbbi bakıcıya kayması** | 2.1 suçluluk/sarsılan kimlik · 2.2 sürekli nöbet/tıbbi bakıcı · 2.3 kaybetme korkusu · 2.4 ergenlik-otonomi · 2.5 mahremiyet/eş rolü · 2.6 kardeşte adalet ikilemi | Anneliğin dönüşümü; Kaybetme korkusu; Ergenlik |
| **T3 — Hastalığın içinden: T1DM'li çocuk** | 3.1 normalleştirme/avantaja çevirme · 3.2 canım acıyor/tedavi yükü · 3.3 farklılık/utanç/stigma · 3.4 el üstünde tutulma/kontrol | Hastalık algısı; Günlük-sosyal hayat; Kısıt |
| **T4 — Aynı evde üç farklı deneyim (triadik)** | 4.1 diyabetik düzen · 4.2 "bir şey olacak" korkusu · 4.3 ilgi/adalet/kontrol gerilimi · 4.4 küçük bakıcılar/hasta otoritesi | 8 eksenin triadik kesişimi (within-case) |

**İnce örüntüler** (Ergenlik 8/21, İhtiyaçlar 8/21) ve `İhtiyaçlar` ekseni (ör. insülin pompası
talebi) → **negatif-vaka / "gelecek ve ihtiyaçlar"** alt-başlığı olarak açıkça raporlanır (COREQ M31).
Frekans önemi belirlemez; tema merkezi düzenleyici işleviyle değerlendirilir.

## 6. Tez bölümleri (bölüm bölüm değişiklik)

- **ch03 (Yöntem):** Mevcut 6 alt-bölüm korunur, `new/ coreq`'e tam hizalanır. Eklenecek: uzman
  paneli/uzmanlık triangülasyonu, yansıtmalı senaryo-sorusu protokol revizyonu (M17), gözlemci BA
  rolü, 21 davet → 7 kabul akışı, veri güvenliği/şifreli saklama. Düzeltme: "6 aile" → **7 aile**.
- **ch04 (Bulgular):** Çekirdek iş. Her makro tema: özet tablo + **verbatim alıntılar (K1 etiketi)**
  + **triadik within-case okuma**. `quote_id` ankrajları → kayıt defterinden gerçek verbatim.
  Joint Display H5 çekirdeğiyle korunur, nitel tarafı verbatim'le beslenir.
- **ch05 (Tartışma):** 4 tema literatürle yorumlanır (FMSF, treatment burden, sibling burden,
  stigma, informant discrepancy); karma convergence/complementarity/discordance/expansion anlatısı
  verbatim örüntülerle güçlendirilir. Nitel tema hiçbir zaman nicel etki/nedensellik gibi sunulmaz.
- **ch02 (Genel Bilgiler):** Nitel arka plan (RTA, multi-informant, triadik gelenek) güncellenir.
- **ch07 (Ekler):** COREQ-32 tablosu; **codebook/kod ağacı** (M25); **de-identify katılımcı künyesi**
  (aile no·rol·yaş yıl+ay·cinsiyet·tanı süresi·anne eğitimi — **tarih yok**, K4); görüşme rehberi.

## 7. Yönetişim / KVKK / provenance

- **Yayımlanan tez:** verbatim + `(Aile 11, sağlıklı kardeş, 9 yaş)`; gerçek ad/doğum/tanı tarihi yok;
  künyede türetilmiş yaş/süre.
- **Analiz katmanı (`niteliksel/`):** tam veri + kayıt defteri; **dış MCP/connector'a (evidentia/
  minerva/pipeworx) katılımcı verisi/alıntı ASLA gitmez** — oraya yalnız literatür arama terimi.
  Ajan hafızasına kimliksel veri yazılmaz.
- Her verbatim → `quotes_used_v3.csv` `quote_id` eşlemesi (quote-parity testi).

## 8. Doğrulama, tutarlılık, yürütme

- **Denetim kapıları:** `sci-audit:guideline-check --type coreq` (+ karma için `--type jars`),
  axis A referans, axis B claim-grounding, axis G Türkçe imla; ardından Galileo three-tier.
  Yeni **quote-parity testi** (tezdeki her verbatim ↔ kayıt defteri). `quarto render` +
  `python3 scripts/util/tez_checklist_verify.py`.
- **Tutarlılık düzeltmeleri:** 6→7 aile; `ana`+`chat` → tek kanon; cross-ref/bib; joint-display H5 hizası.
- **Yürütme (ultracode):** ağır fan-out'lar (verbatim çıkarımı, tema-başı yeniden yazım, eksen-başı
  denetim) **yerel Workflow** ile; alt-ajanlar yalnız repo dosyalarında çalışır, **katılımcı verisi
  dış araca gitmez**; literatür zenginleştirme evidentia (yalnız literatür terimi, RBŞ disiplini).

## 9. Kapsam dışı (YAGNI)

- Journal (6-tema) manuskript sürümünün yeniden üretimi — tez odaklıdır; yalnız codebook Rosetta'sı korunur.
- Nicel kol (H1–H5, R pipeline) değişmez; yalnız Joint Display kesişimi hizalanır.
- Yeni görüşme/veri toplama yok; mevcut 7 aile / 21 görüşme sabittir.
- Inter-coder kappa/AC1 **üretilmez** (RTA epistemolojisi; critical-friend + refleksivite raporlanır).

## 10. Riskler

- **Geri-tanımlama:** küçük örneklem + tek klinik → K1/K4 de-identify zemini + türetilmiş künye ile azaltılır.
- **v2↔v3 sapması:** `reconciliation_v2_to_v3.md` ile şeffaf raporlanır; v2.0 silinmez, arşive alınır.
- **Alıntı çeviri/kırpma bütünlüğü:** verbatim aynen; izin verilen tek müdahale `[…]` kesme + `[açıklama]`;
  quote-parity testi bunu korur.
- **Render/freeze:** chapter düzenlemelerinde `_freeze/`+`outputs/quarto/thesis` temizliği gerekli
  (bkz. memory: render-freeze-include-gotcha).

## 11. Başarı ölçütü (Definition of Done)

1. Kanon katmanı: `quotes_used_v3.csv`, `triadik_matris_v3`, `codebook_v3`, COREQ-32 tazelenmiş,
   v2.0 arşivde, `reconciliation_v2_to_v3.md` yazılmış.
2. ch02/03/04/05/07 niteliksel içerik `new/`'den yeniden yazılmış; ch04 verbatim (K1) + triadik okuma.
3. Her verbatim `quote_id` ile eşli (quote-parity testi GREEN).
4. `sci-audit --type coreq` HARD=0; Galileo advisory geçildi; `quarto render` temiz; `tez_checklist_verify.py` FAIL yok.
5. Yayımlanan tezde tarih/ad yok; künye türetilmiş yaş/süre.

## 12. Uygulama sıralaması (writing-plans girdisi)

1. Kanon katmanı (Bölüm 4) — kayıt defteri + matris + tema v3 + COREQ + arşiv.
2. ch03 (Yöntem) COREQ hizası.
3. ch04 (Bulgular) verbatim + triadik yeniden yazım — çekirdek.
4. ch05 (Tartışma) + karma entegrasyon.
5. ch02 arka plan + ch07 ekler.
6. Doğrulama paketi (Bölüm 8) + tutarlılık düzeltmeleri.
