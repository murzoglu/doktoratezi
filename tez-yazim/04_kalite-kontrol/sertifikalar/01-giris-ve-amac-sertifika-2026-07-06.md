# Bölüm Finalizasyon Sertifikası

Durum: `provisional-pass`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | `01-giris-ve-amac` |
| Bölüm başlığı | `GİRİŞ ve AMAÇ` |
| Üretim dosyası | `chapters/01_giris.qmd` |
| Hazırlık briefi | `tez-yazim/03_bolum-hazirlik/01_giris-ve-amac.md` |
| Sertifikasyon tarihi | 2026-07-06 |
| Sertifikasyonu uygulayan | Claude Code (Opus 4.8, 1M) |
| Uygulama onayı | `bekleniyor` (kullanıcı görevi: "anlatım mantıksal akışını iyileştir; sertifikasyon yap") |
| Önceki sertifika | `01-giris-ve-amac-sertifika-2026-07-05.md` (`certified-final`) |

## Bu Sürümün Kapsamı — Anlatım/Mantıksal Akış Revizyonu

2026-07-06 oturumunda bölüm **yalnız anlatım ve mantıksal akış** ekseninde
revize edildi. **Atıf seti, sayısal iddialar ve kanıt içeriği değişmedi**:
hiçbir dış referans eklenmedi, çıkarılmadı veya anlamı değiştirilmedi; 18 dış
atfın tamamı 2026-07-05 `certified-final` sürümündeki künye/claim/tam metin
zincirini aynen korur. Değişiklik prose-akış revizyonuyla sınırlıdır.

Uygulanan akış iyileştirmeleri:

1. **Aşırı-yüklü iki paragraf bölündü.** Önceki denetimde `paragraph-long`
   işaretlenen iki paragraf ayrıştırıldı:
   - Eski P1 (epidemiyoloji + "aile olayı" çerçevesi) → yeni P1 (epidemiyoloji)
     + P2 (T1DM'nin aile-düzeyi yeniden düzenleyici etkisi + `whittemore2012`).
   - Eski P6 (Türkiye bağlamı + boşluk + araştırma sorusu + önem) → yeni P7
     (Türkiye bağlamı + ulusal/uluslararası boşluk) + P8 (araştırma sorusu +
     önem/katkı).
2. **Üç-eksen köprüsü eklendi.** Çoklu bilgi kaynağı paragrafı (yeni P6), zayıf
   "bir diğer gerekçe" bağlacı yerine, önceki üç yapı paragrafını (ebeveynlik
   tutumu / anne depresif belirtileri / kardeş ilişkisi) açıkça "bu üç eksen"
   olarak toparlayan sentezleyici bir açılış cümlesiyle bağlandı; triadik
   desenin gerekçesi mantıksal olarak öne çekildi.
3. **Pre-emption giderildi.** Eski P2'nin sonunda depresif belirti eksenine
   yapılan erken gönderim kaldırıldı; ebeveynlik paragrafı artık çocuk-algısı +
   anne-bildirimi ikilisinde kapanıyor, depresif belirti ekseni kendi
   paragrafında (P4) açılıyor.
4. **Uzun cümleler sadeleştirildi.** Önceki denetimde `sentence-too-long`
   (>55 kelime) işaretlenen iki cümle (ulusal literatür cümlesi ve H1-H5
   sayımı) yeniden yapılandırıldı; H1-H5 alt amaçları "gruplar arası
   karşılaştırma (H1-H3)" ve "aile içi ilişki (H4-H5)" mantıksal kümelerine
   ayrıldı.
5. **Tense tutarlılığı.** Karma tasarım paragrafında `kullanılacaktır` (gelecek)
   → `kullanılmaktadır` (geniş zaman) olarak bölümün genel zamanıyla
   uyumlandı.

Ölçülen etki (Kapı 4, tr_sciaudit `certification`):

| Metrik | 2026-07-05 baseline | 2026-07-06 revizyon |
|---|---:|---:|
| Errors (blocker) | 0 | 0 |
| Warnings (major) | 12 | 7 |
| `paragraph-long` | 2 | 0 |
| `sentence-too-long` (>55 söz) | 2 | 0 |
| Ateşman skoru | -7,08 | 3,9 |
| Ort. kelime/cümle | 32,36 | 28,3 |
| Paragraf / cümle | 8 / 36 | 10 / 43 |

## Kapı 0: Kapsam ve Gizlilik

- [x] Bölüm dosyası ve hazırlık briefi okundu.
- [x] Resmi kaynaklar ve `format-kontrati.md` bağlamı korundu.
- [x] Ham veri, ham transcript, satır düzeyi veri, `.env`, token veya credential
      rapora taşınmadı. GİRİŞ yalnız dış literatür iddiaları içerir; katılımcı
      satır verisi kullanılmaz. `./dmnitel ai-context` korumalı alan sınırlarını
      doğruladı.

Kapı 0 kararı: `PASS`

## Kapı 1: Derin Literatür ve Künye Evreni

Bu revizyon **yeni dış retrieval içermez**; iddia haritası 2026-07-05
sürümüyle aynıdır. Bölümdeki 18 dış atfın tamamı `referans-denetim-ledgeri.md`
içinde doğrulanmış künye satırına (DOI/PMID/PMCID/OpenAlex/YÖK ID) bağlı ve
`cite-ok` durumundadır. Otomatik denetim (bölüm atıfları ↔ ledger): `cite-ok: 18
| orphan claim: yok`. Atıf-taşıyan her cümle taşınırken kendi künyesiyle aynı
paragrafta tutuldu; sayısal iddialar (`108.300`/`149.500`, `binde 0,75`,
`yüz binde 10,8`, `%22,4`, `%31,5`) atıflarıyla aynı cümlede korundu.

Kapı 1 kararı: `PASS`

## Kapı 2: Full-Text, Zotero ve Bağlam

Zotero Web API erişimi doğrulandı (`status`: ok, key_loaded, userID 17265855).
18 referansın tamamı 2026-07-05 sürümündeki künye-ID + Zotero item key +
`references/references.bib` mutabakatını korur; bu sürümde Zotero'da değişiklik
yapılmadı. Bölümdeki 18 citation key'in tamamı `references.bib` içinde çözülüyor
(orphan citation: 0).

Kapı 2 kararı: `PASS`

## Kapı 3: Bölüm Metni ve Resmi Kılavuz Uyumu

- [x] Resmi başlık doğru: `# GİRİŞ ve AMAÇ`.
- [x] Alt başlık yok (§1.3 uyumlu); akış paragraf düzeyinde kuruldu.
- [x] Bölüm işlevi korundu ve güçlendirildi: epidemiyoloji → aile olayı → üç
      eksen (ebeveynlik/anne depresif belirti/kardeş) → çoklu bilgi kaynağı →
      boşluk → araştırma sorusu → önem → karma tasarım → amaç → H1-H5.
- [x] Tablo/şekil/cross-reference yok; istatistik/`p` değeri yok.
- [x] İngilizce ondalık-nokta `p` değeri yok (G5 blocker taraması temiz).
- [x] Ondalık virgül kuralı korundu; `108.300`/`149.500` binlik ayırıcılı sayım
      değerleridir ve `ogle2022idfAtlas` atfıyla aynı cümlededir.
- [x] Orphan claim/citation yok (18/18 çözüldü).

Kapı 3 kararı: `PASS`

## Kapı 4: Türkçe İmla, Akış ve Mantık

Kanonik araç — sci-audit axis G (`tr_sciaudit.py` v0.2.0):

```text
python3 <sci-audit>/skills/turkish-sci-style/scripts/tr_sciaudit.py \
  chapters/01_giris.qmd --strictness certification --format md --fail-on error \
  --terms "diyabet,depresyon,ebeveyn,kardeş,ölçek,yöntem" \
  --out tez-yazim/04_kalite-kontrol/raporlar/01-giris-tr-sciaudit.md
EXIT: 0 | Errors: 0 | Warnings: 7 | Info: 1
```

Kalan 7 uyarı bloklayıcı değildir ve gerekçeli kabul edilmiştir:
`decimal-dot` (2× — `108.300`/`149.500` binlik ayırıcı, ondalık değil sayım;
denetimin identifier istisnası kapsamında), `abbreviation-review` (IDF, ilk
kullanımda açık), `sentence-long` (4× — tez giriş registeri için beklenen; bu
sürümde daha ağır `sentence-too-long` sınıfı sıfıra indi), `readability-very-hard`
(Ateşman -7,08 → 3,9'a yükseldi; tez registeri için beklenen "very-hard" etiketi
korunuyor). Uyarı sayısı önceki sertifikalı baseline'a göre 12'den 7'ye düştü.

Kapı 4 kararı: `PASS`

## Kapı 5: AI-Reliability ve Teknik Doğrulama

| Komut | Sonuç |
|---|---|
| `./dmnitel ai-context` | PASS; korumalı alan sınırları doğrulandı. |
| Nitel `t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py` | PASS; `55/55 passed`; roster token redaction PASS. |
| Nicel `doktoratezi-ai-audit/scripts/test_repo_ai_reliability.py` | PASS; `142/142 passed`. |
| `python3 scripts/util/zotero_env_bridge.py status --json` | PASS; key_loaded. |
| `git diff --check -- chapters/01_giris.qmd` | PASS; çıktı yok. |
| `quarto check` | PASS; Quarto 1.6.43, Pandoc 3.4.0, Dart Sass/Deno/Typst OK. |
| Atıf çözümü (`quarto pandoc … --citeproc --bibliography … --csl references/apa.csl`) | PASS; exit 0, çözülmemiş `?@`/`???` yok, 18/18 `csl-entry` üretildi. |

**sci-audit manüskript adli denetimi (axes A–F) — carry-forward gerekçesi:**
Bu revizyon prose-akış ile sınırlıdır; hiçbir referans, sayısal değer veya
ampirik iddia eklenmedi/çıkarılmadı/anlamı değiştirilmedi. Referans bütünlüğü
(A), claim grounding (B), istatistik (C), halüsinasyon (D), raporlama-kılavuzu
(E) ve AI-şeffaflık (F) eksenleri 2026-07-05 `certified-final` baseline'ından
içerik-özdeş olarak taşınır. Akış revizyonundan etkilenen tek eksen olan axis G
(Türkçe yazım) Kapı 4'te yeniden koşuldu. Diff-kanıtı: 18 citation key ve tüm
sayısal iddialar bayt düzeyinde korundu.

Kapı 5 kararı: `PASS`

## Bloklayıcılar ve Çözüm

| Bloklayıcı | Durum | Not |
|---|---|---|
| `approval-gap` | Açık | Teknik kapılar (0-5) PASS; `certified-final` için açık uygulama onayı bekleniyor. |

Bunun dışında açık bloklayıcı yoktur (`format-gap`, `full-text-gap`,
`zotero-gap`, `orphan-claim`, `orphan-citation`, `privacy-gap`,
`reliability-gap`: yok).

## Nihai Sertifika Kararı

| Alan | Değer |
|---|---|
| Kapı 0 | `PASS` |
| Kapı 1 | `PASS` |
| Kapı 2 | `PASS` |
| Kapı 3 | `PASS` |
| Kapı 4 | `PASS` |
| Kapı 5 | `PASS` |
| Nihai durum | `provisional-pass` |

Final notu:

```text
chapters/01_giris.qmd anlatım/mantıksal akış revizyonu; Kapı 0-5 teknik olarak
kapalı (tr_sciaudit 12→7 uyarı, 0 hata; nitel 55/55 + nicel 142/142; atıf
çözümü 18/18; git diff temiz). Atıf seti ve ampirik iddialar 2026-07-05
certified-final baseline'dan değişmedi. Playbook karar kuralı gereği, açık
uygulama onayı verilene kadar durum provisional-pass'tir; onay üzerine
certified-final'a yükseltilebilir ve bu sertifika 2026-07-05 sürümünü supersede
eder.
```
