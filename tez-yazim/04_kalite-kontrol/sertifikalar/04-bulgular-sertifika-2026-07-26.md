# Bölüm Finalizasyon Sertifikası

Durum: `certified-final`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | 04 — BULGULAR |
| Bölüm başlığı | BULGULAR |
| Üretim dosyası | `chapters/04_bulgular.qmd` (1593 satır) |
| Sertifikasyon tarihi | 2026-07-26 |
| Strictness | `certification` |
| Önceki sertifika | `04-bulgular-sertifika-2026-07-16.md` (`certified-final`) |
| Yeniden sertifikasyon nedeni | Bölüm bu oturumda bütünleşik iki-komut zenginleştirme protokolüyle (`/veri-gosterimi-zenginligi` → `/anlatim-zenginligi`) §4.5–4.8 alt bölümlerinde işlendi; ayrıca §4.1–4.4 önceki oturumlarda işlenmişti. Dosya 973 → 1593 satıra genişledi. Kanıt-değeri (sayı/yön/anlamlılık) hiçbir düzenlemede değiştirilmedi. |
| Sertifikasyonu uygulayan | Ona (Claude Opus 4.8) — Kapı 0–5 yeniden denetimi |
| Uygulama onayı | **Kullanıcı açık onayı ("onaylıyorum", 2026-07-26)** — `provisional-pass` → `certified-final` |

## Bu Oturumdaki Değişiklik Envanteri

`chapters/04_bulgular.qmd` üzerinde (git diff: +136/−76 satır) ve `R/29_apa_tables.R` (+23/−… satır) üzerinde:

### §4.5 Robustluk ve Bayesçi Doğrulama (GÖSTERİM + NESİR)
1. **Onaylı drift 1 — R̂ eşiği (§1368):** `R̂ < 1,002` → `R̂ ≤ 1,003`; kaynak CSV
   maksimum değeri 1,00300 (EMBU-C satırı) ile birebir hizalandı.
2. **Onaylı drift 2 — figür altyazısı (§1379):** `Rhat ≤ 1,002` → `≤ 1,003` ve
   `ESS oranı ≥ 0,12` → `≥ 0,09`; her iki değer üretilmiş artefaktla mutabık.
   Altyazı stale-freeze cache'i tam execute-render ile tazelendi.
3. **NESİR:** WC=68 uzun cümle bölündü + paragraf sınırı eklendi (sayı korunur).

### §4.6 Niteliksel Kol Bulguları (NESİR)
4. **NESİR:** İki cümle bölünmesi (`;` → `.`); veri drift YOK, tüm sayımlar
   kaynakla teyitli. Uzun-cümle WC=78/87/176 taramaları markdown tablo-hücresi
   regex artefaktıydı; yalnız 2 gerçek cümle bölmesi uygulandı.

### §4.7 Karma Bulgulara Köprü (Joint Display) (GÖSTERİM)
5. **BETİM 1 — Meta satırı:** Tamamlayıcılık satırına "Nedensellik yok; " öneki
   eklenerek 6/6 satır tutarlılığı sağlandı. Veri drift YOK.

### §4.8 Genel Bulgu Sentezi (GÖSTERİM + NESİR)
6. **ESTETİK 1 — kaynak-tekilliği düzeltmesi:** `R/29_apa_tables.R:1267`
   `"Dual reporting bulgularla uyumlu"` → `"Çift raporlama bulgularla uyumlu"`.
   Düzeltme CSV'ye değil ÜRETİCİ koda uygulandı; tam `tar_make()` ile CSV
   yeniden üretildi; BF değerleri korundu; `tar_outdated = 0`.
7. **NESİR:** WC=164 blok 7 ayrı paragrafa ((a)–(e)) bölündü; sayılar birebir.

Sınır: Ham veri / transcript / demografi satırı / credential sertifikaya
**taşınmadı**; yalnız aggregate + anonim quote-ID bağlama alındı.

## Kapı 0: Kapsam ve Gizlilik — PASS

- [x] Bölüm dosyası + önceki sertifika + oturum değişiklikleri okundu.
- [x] Değişiklik envanteri git diff ile çıkarıldı (yukarıda).
- [x] Gizlilik sınırı: `data/{raw,identified,cleaned,backup}`, `.env`, credential
      dosyalarının hiçbiri değişmedi (git status taraması TEMİZ).
- [x] K5-LIT (`r_generator_literal_audit.py`): **PASS** — üretici kodda gömülü
      istatistik literali yok.

Kapı 0 kararı: **PASS**

## Kapı 1: Derin Literatür ve İddia Haritası — PASS

- Bölümde 15 gerçek atıf (yöntemsel gerekçe/metot-çapası) + `@fig`/`@tbl`
  çapraz-referans; substantif literatür karşılaştırması **Tartışma'ya** ertelenir.
- Marmara §3.6 yorum-sınırı taraması: eşleşen tüm satırlar ya metodolojik
  okuma-uyarısı ("temkinli yorumlanmalıdır", "yorumlanmamıştır") ya da açık
  *Tartışma*'ya erteleme; literatür-karşılaştırması sızıntısı **YOK**.
- Keşifsel meta-forest (§1129/1136) "betimsel olarak" etiketli; resmi yorum
  ertelenmiş.
- `bib_hygiene reconcile` (04): **HARD undefined = 0** (render kırılmaz).

Kapı 1 kararı: **PASS**

## Kapı 2: Tam Metin / DOI / Ledger Mutabakatı — PASS

- Bu oturumda eklenen satırlarda **yeni doğrulanmamış atıf YOK**.
- `@cheungRensvold2002invariance` diff'te görünse de bib'te tam künyeli ve
  `referans-denetim-ledgeri.md`'de DOI `10.1207/S15328007SEM0902_5` +
  identity-doğrulamalı (`cite-ok`, 55/55 + 144/144 passed, 2026-07-14 Kapı 2).

Kapı 2 kararı: **PASS**

## Kapı 3: Bölüm Metni + Resmi Kılavuz Uyumu (Marmara §3.6) — PASS

- Tablo/figür referans bütünlüğü: 57 referans → tümü tanımlı (inline `{#...}` +
  chunk `#| label:` + Ek bölümü tanımları). `@tbl-apa-invariance` (Ek 3) ve
  `@tbl-apa-tost-sensitivity` (Ek 5) `chapters/07_ekler.qmd`'de tanımlı;
  Quarto cross-book çözer — kırılma YOK.
- Orphan görsel (tanım var, referans yok): **YOK**.
- Tablo başlıkları betimsel; Bulgular yorumsuz (Marmara §3.6 uyumlu).

Kapı 3 kararı: **PASS**

## Kapı 4: Türkçe İmla/Anlam (sci-audit axis G) — PASS

- `tr_sciaudit.py` (sci-audit axis G): **Errors (blocker) = 0**.
- 83 SOFT warning (advisory): uzun cümleler evidence-korumalı; tüm `decimal-dot`
  bulguları false-positive — hepsi bölüm/kılavuz referansı (§1.6, §1.7, §3.6,
  §4.4, §4.7) veya binlik ayraç (`10.000` MCMC çekilişi). Gerçek istatistikler
  (ör. `BF₁₀ = 10,55`) Türkçe ondalık virgülü kullanıyor.

Kapı 4 kararı: **PASS**

## Kapı 5: AI-Güvenilirlik (sci-audit A-F + repo invaryant) — PASS

- `stats_forensics.py` (sci-audit axis C — statcheck/GRIM/GRIMMER/SPRITE/CI/
  yüzde/altgrup/etki-büyüklüğü): **error = 0, warning = 0**.
- `karma_ledger_check.py`: **TEMİZ (0 bulgu)**.
- `r_generator_literal_audit.py` (K5-LIT): **PASS**.
- `tests/test_apa_tables.R`: **PASS** (R/29 "Çift raporlama" düzeltmesi testi
  bozmadı).
- Tam senkron: hedefli `tar_make()` sonrası **`tar_outdated() = 0`** (5 stale
  hedef — `thesis_mapping_*` + `thesis_html_file` — güncellendi; sayısal-içerik
  hedefi değil, bölüm↔hedef eşleme + render meta-hedefleri).
- Galileo faithfulness (oturum boyu §4.5–4.8): ≥ 0,60 PASS eşiğini karşıladı
  (0,62–0,72 aralığı).

Kapı 5 kararı: **PASS**

## Nihai Karar

| Kapı | Sonuç |
|---|---|
| Kapı 0 — Kapsam/Gizlilik | PASS |
| Kapı 1 — Literatür/İddia | PASS |
| Kapı 2 — DOI/Ledger | PASS |
| Kapı 3 — Metin/Kılavuz (Marmara §3.6) | PASS |
| Kapı 4 — Türkçe İmla/Anlam | PASS |
| Kapı 5 — AI-Güvenilirlik | PASS |

**Durum: `certified-final`** — Kapı 0–5'in tümü otomatik/salt-okuma denetimde
PASS ve kullanıcı açık onayı ("onaylıyorum", 2026-07-26) ile `provisional-pass`
→ `certified-final` yükseltildi. Kanıt-değeri (sayı/yön/anlamlılık) bu oturumda
değiştirilmedi; yalnız gösterim (Çift raporlama, Meta öneki, R̂/ESS altyazı) ve
nesir (paragraf/cümle bölmeleri) katmanı düzenlendi.
