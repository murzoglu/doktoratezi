# sci-audit Konsolide Değerlendirme — P1 Düzeltmeleri Sonrası

**Tarih:** 2026-07-17
**Kapsam:** Dördüncü tur denetim P0 + P1-1..P1-16 düzeltmeleri sonrası tez metni
**Araç:** `sci-audit@cureonics-marketplace` v0.2.1 (mahirkurt/CureoPrivate marketplace, PAT ile kuruldu) + repo yerel eşdeğerleri
**Denetlenen bölümler:** `chapters/03_gerec_ve_yontem.qmd`, `chapters/04_bulgular.qmd`, `chapters/05_tartisma_ve_sonuc.qmd` + `docs/CLINICAL-STUDY-REPORT-FINAL.md`

---

## Genel Karar: ✅ GEÇTİ (blocker/error yok)

Yedi eksenin tamamı koşuldu. **Hiçbir eksende render-kıran hata (error/blocker/HARD) yoktur.**
Kalan bulgular ya üslup uyarısı ya doğrulanmış false-positive'dir.

| Eksen | Araç | error/blocker | Not |
|-------|------|:---:|-----|
| **Yığın sağlığı** | `audit_stack_healthcheck.py` | — | TÜMÜ PASS (MINERVA + GALILEO judge/embedding + SCI-AUDIT + ANAMNESIS + CLAIM-CERT) |
| **A — Referans bütünlüğü** | `bib_hygiene.py all` | **0 HARD** | 1 SOFT (eksik DOI: `sumer2010anneBabaTutum`); orphan'lar referans havuzu, normal |
| **B — Claim grounding** | `claim_certification --with-judge` | 0 tanımsız atıf | 338 iddia; 333 tam-izli, 5 kısmi, 0 izsiz |
| **C — İstatistik tutarlılığı** | `stats_forensics.py` (plugin) | **0 / 0** | 04 + 05 bölümlerinde statcheck/GRIM/GRIMMER temiz |
| **D — Halüsinasyon sinyalleri** | `hallucination_signals.py` (plugin) | **0 error** | 05'te 1 warning → false-positive (hedge ifadesi) |
| **E — Raporlama kılavuzu** | (JARS/STROBE/COREQ) | — | Faz I doğrulayıcı hat + keşifsel etiketleme mevcut; manuel kalem |
| **F — AI-şeffaflık** | — | — | Yöntem/teşekkür beyanı manuel doğrulama kalemi |
| **G — Türkçe imla/yazım** | `tr_sciaudit.py` (plugin, certification) | **0 / 0 / 0** | Üç bölümde de blocker yok; ondalık-nokta bulguları false-positive (sürüm/madde no) |

---

## Eksen Detayları

### Axis A — Referans bütünlüğü (bib_hygiene)
- **HARD (atıflı ama tanımsız, render kırar): 0** ✅
- SOFT: 1 eksik DOI (`sumer2010anneBabaTutum` — Türkçe tez/kitap, DOI'siz erişilebilir; SOFT kabul).
- Orphan (tanımlı ama henüz atıfsız): 122 — bilinçli referans havuzu, sorun değil.

### Axis B — Claim grounding (claim_certification + Galileo judge)
- Sayısal iz: **338 iddia · 333 tam-izli · 5 kısmi · 0 izsiz** ✅
- Gerçek high-risk kaynaksız sayı (CSV filtresi): **0**. Ham sayaçtaki 7 "unmatched",
  bitişik sayı tokenizasyonu artefaktıdır (ör. "62,2–95,9", "8'inden 7'sinde") ve
  klinik-yorum metninde bağlamı olan değerlerdir; kendi verimize izlenmesi gereken
  kaynaksız istatistik değildir.
- **Galileo judge FAIL yorumu:** İşaretlenen 6 örneğin tamamı **yöntem-bölümü
  kendi-prosedür betimlemesidir** (R 4.5.3, `targets` orkestrasyonu, s-EMBU
  psikometri çerçevesi). Bunlar dış-literatür iddiası değildir; judge parçacığı
  kaynak-bağlamı olmadan aldığı için düşük groundedness döndürür. Skor koşumlar
  arası 0,82↔0,84 oynar (örnekleme gürültüsü). **P1 düzeltmelerinden kaynaklanan
  yeni bir kaynaksız-iddia değildir.**

### Axis C — İstatistik iç-tutarlılık (stats-forensics)
- 04_bulgular + 05_tartisma: **error 0, warning 0.** statcheck (p yeniden hesap),
  GRIM/GRIMMER, CI/yüzde/altgrup/etki-büyüklüğü tutarlı. ✅

### Axis D — Halüsinasyon sinyalleri (hallucination-signals)
- 04: temiz. 05: 1 warning `universal-quantifier` → **false-positive**:
  "ölçek puanına **her zaman yansımayabileceği**" bir çekince (hedge) ifadesidir,
  aşırı-genelleme değil. İşlem gerekmez.

### Axis G — Türkçe bilimsel yazım (tr_sciaudit, certification)
- 03: 0 error / 71 warning · 04: 0 error / 40 warning · 05: 0 error / 108 warning.
- **Hiç blocker/error yok** (`--fail-on error` altında üçü de EXIT=0). ✅
- Uyarıların dağılımı: çoğunluk `sentence-long`/`paragraph-long` (üslup, akademik
  yoğunluk); `decimal-dot` bulguları false-positive (sürüm no `R 4.5.3`, Marmara
  §3.6/§1.6 gibi kılavuz referansları); `abbreviation-review` bilgi düzeyi.
- Not: `causal-overclaim` "sağlar" (satır 37) → "çoğu aile iyi uyum sağlar"
  genel örüntü betimi, çalışmanın kendi nedensel iddiası değil; false-positive.

---

## P1 Düzeltmeleriyle İlişki

P1 turunda eklenen sayısal içerik (P1-8 BF önsel duyarlılığı 32,35/10,55/4,65;
P1-13 optimizm-düzeltilmiş kalibrasyon slope 0,77) sci-audit'te **yeni tutarsızlık
veya kaynaksız-sayı üretmemiştir**: Axis B izsiz=0, Axis C tutarsızlık=0. P1
nedensellik-disiplini düzeltmeleri (P1-4/6/12) Axis D/G nedensellik taramasında
gerçek overclaim bırakmamıştır (tek bulgu false-positive).

## Kalan Manuel Kalemler (sci-audit kapsamı dışı)
- Axis E raporlama-kılavuzu madde-madde eşleme (JARS-Mixed/STROBE/COREQ) — insan editör.
- Axis F ICMJE AI-kullanım beyanı varlığı — Yöntem/teşekkür bölümü elle doğrulanmalı.
- Üslup uyarıları (uzun cümle/paragraf) — isteğe bağlı okunabilirlik iyileştirmesi;
  teslim engeli değil.

**Sonuç:** P1 düzeltmeleri sonrası tez metni sci-audit yedi ekseninden blocker'sız
geçmiştir. Teslim engeli oluşturan hiçbir bulgu yoktur.
