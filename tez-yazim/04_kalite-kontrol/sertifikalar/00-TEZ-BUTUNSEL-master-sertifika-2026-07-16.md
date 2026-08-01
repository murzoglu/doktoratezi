# Tez Bütünsel (Tez-Düzeyi) Finalizasyon Sertifikası

Durum: `certified-final`

## Kapsam

Bu belge, **tezin bütününü** (tüm bölümler + bölümler-arası tutarlılık + tam-tez
render + repo değişmezleri) tek bir tez-düzeyi denetime tabi tutar. Bölüm-bazlı
sertifikaların üstünde, yalnız bütünde görülebilen eksenleri (çapraz-tutarlılık,
tez-geneli atıf evreni, tam-tez çapraz-referans çözünürlüğü, iki-repo değişmez
testleri) doğrular.

| Alan | Değer |
|---|---|
| Kök belge | `thesis.qmd` (10 include: 00a–00c + 01–07) |
| Sertifikasyon tarihi | 2026-07-16 |
| Strictness | `certification` (tez-düzeyi) |
| Sertifikasyonu uygulayan | Ona (Claude Opus 4.8) |
| Dal | `ona/advisory-uyum-iyilestirme` |
| Uygulama onayı | **Kullanıcı açık onayı ("Uygun", 2026-07-16)** — bütünsel `certified-final`. |

## Bölüm Sertifika Durumu (kaynak-of-truth)

| Bölüm | En güncel sertifika | Durum |
|---|---|---|
| 00c — Özet / Summary | `00c-...-2026-07-16.md` | **certified-final** |
| 01 — Giriş ve Amaç | `01-...-2026-07-16.md` | **certified-final** |
| 02 — Genel Bilgiler | `02-...-2026-07-16.md` | **certified-final** |
| 03 — Gereç ve Yöntem | `03-...-2026-07-16.md` | **certified-final** |
| 04 — Bulgular | `04-...-2026-07-16.md` | **certified-final** |
| 05 — Tartışma ve Sonuç | `05-...-2026-07-16.md` | **certified-final** |
| 06 — Özgeçmiş/Faaliyetler | `06-...-2026-07-14.md` | **certified-final** |
| 07 — Ekler | `07-...-2026-07-14.md` | **certified-final** |

Not: 00a (ön bölümler) ve 00b (kısaltmalar) yapısal/dizin bölümleridir; bağımsız
içerik sertifikası taşımaz, tez-düzeyi kontrollere (render + kısaltma senkronu)
dahil edilmiştir.

## Eksen A: Bölümler-Arası Çapraz-Tutarlılık — PASS

Aynı sayısal iddiaların Özet ↔ Bulgular ↔ Tartışma boyunca senkronu doğrulandı:

| İddia | Değer | Bölümler-arası |
|---|---|---|
| H1 çocuk reddetme β + GA | β = 0,16; [0,05; 0,26] | 00c/04 senkron; 05 yorumsal |
| H1 BF | BF₁₀ = 10,55 | 00c/04 senkron |
| H4 SEM (sıcaklık/reddetme/karşılaştırma) | β = −0,28 / 0,33 / 0,28 | 00c/04 senkron |
| H5 diadik reddetme ICC | 0,00 (DM) / 0,32 (kontrol) | 00c/04/05 senkron |
| Antidepresan | %29 vs %9; SMD = 0,53 | 00c/04/05 senkron |
| Örneklem | 241 aile (120 DM, 121 kontrol; 482) | tüm bölümlerde tutarlı |

- **Bu oturumda giderilen tutarsızlık:** 05'te `SMD=0,53` (boşluksuz) →
  `SMD = 0,53` olarak Özet/Bulgular standardına hizalandı.
- **Kısaltma senkronu** (`tr_corpus --abbrev 00b`): tez-geneli **0 blocker**;
  H-ABBR uyarıları artefakt (HTML-yorum dosya adları `CLINICAL/FINAL/...`,
  tire-ekli parçalar `DM-/E-/FDR-`, hipotez notasyonu `H0-H5`). 7 ABBR-UNUSED
  advisory düzeyi (çoğu tireli formlarda kullanımda).

Eksen A kararı: **PASS**

## Eksen B: Tez-Geneli Atıf Evreni — PASS

`bib_hygiene reconcile` (00c + 01–05 birlikte):

- **HARD (atıflı ama tanımsız — render kırar) = 0.** Hiçbir atıf tanımsız değil.
- SOFT AMA-11 eksik: 1 (`simonsohn2015specification` volume/pages) — baseline,
  bu oturumda dokunulmadı (git diff ile kanıtlı).
- Orphan (bib'de tanımlı, atıfsız): 120 / 333 künye. Bib arşiv/gelecek kullanım
  için geniş tutulmuş; **render'ı etkilemez** (HARD=0). Tüm qmd'lerde 213
  benzersiz atıf kullanımda. Not: nihai teslimden önce orphan budaması isteğe
  bağlı bir temizliktir, kalite engeli değildir.

Eksen B kararı: **PASS**

## Eksen C: Tam-Tez Render ve Çapraz-Referans — PASS

`quarto render thesis.qmd` (freeze:auto cache kullanıldı):

| Format | Sonuç |
|---|---|
| HTML | **exit 0** — `outputs/quarto/thesis.html` (986 KB) |
| DOCX (Marmara teslim) | **exit 0** — `outputs/quarto/thesis.docx` (3,7 MB) |

- **Çözünmemiş çapraz-referans (`??`) = 0.**
- **Çözünmemiş atıf (`[@...]`) = 0** (tüm sitasyonlar AMA-11 numaralı basıldı).
- Yapı: 59 başlık (h1/h2), 34 figür (img), 36 tablo — hepsi çözüldü.
- Quarto 1.9.38; `lang: tr`, `csl: marmara-ama11.csl`.

Eksen C kararı: **PASS**

## Eksen D: Repo Değişmezleri (İki-Repo AI-Reliability) — PASS

| Süit | Sonuç |
|---|---|
| Nicel: `plugins/doktoratezi-ai-audit/.../test_repo_ai_reliability.py` | **144/144 passed** |
| Nitel: `niteliksel/plugins/t1dm-qual-ai-audit/.../test_repo_ai_reliability.py` (niteliksel/ dizininden) | **55/55 passed** |
| Sır redaksiyonu (OpenAI key, GitHub token) | PASS |
| `git diff --check` | temiz |
| Render çıktıları (`outputs/`) | gitignore'da (commit'e sızmıyor) |

Eksen D kararı: **PASS**

## Eksen E: AI-Reliability (Galileo/GPT-5.4) — PASS

Bu oturumda üç bölümde (04, 05, 00c) yürütülen AI-hakem yargıları:

| Bölüm | Groundedness | Citation | Halüsinasyon |
|---|---|---|---|
| 04 Bulgular (H1 pasajı, gerçek kanıt) | 0,84 | supported | 0,22 |
| 05 Tartışma (3 pasaj) | 0,90–0,94 | supported | 0,12–0,14 |
| 00c Özet (bulgular pasajı) | **0,98** | supported | **0,08** |

Coherence (bitişik paragraf semantik akış): 04 → 0,731; 05 → 0,760; 00c → 0,734;
tümünde flow_breaks 0, redundant_pairs 0.

Eksen E kararı: **PASS**

## Bu Oturumun Değişiklik Envanteri (tez-düzeyi)

git diff HEAD (içerik dosyaları): 8 dosya, +576 / −62.

- `chapters/00c_ozet_summary.qmd` — Özet/Summary Marmara §3.2 yeniden yapılandırma
  (istatistikli bulgular, net örneklem, TR↔EN eşlik).
- `chapters/04_bulgular.qmd` — 8 hipotez figürü + kapsam cümlesi + 120-spesifikasyon
  etiketleri + H1 GA dizgi düzeltmesi (§265/§994 → [0,05; 0,26]).
- `chapters/05_tartisma_ve_sonuc.qmd` — negatif kontrol/falsifikasyon sağlamlık
  ailesi (üç→dört) + SMD format hizalama.
- `chapters/02`, `chapters/03`, `chapters/00b` — önceki oturum düzenlemeleri.
- `references/references.bib` — metot + klasik künye eklemeleri (HARD=0 korundu).
- `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` — ledger senkronu.

## Nihai Bütünsel Karar

| Eksen | Karar |
|---|---|
| A — Bölümler-arası çapraz-tutarlılık | PASS |
| B — Tez-geneli atıf evreni (HARD=0) | PASS |
| C — Tam-tez render + çapraz-referans (HTML+DOCX; ??=0) | PASS |
| D — Repo değişmezleri (144/144 + 55/55) | PASS |
| E — AI-reliability (groundedness 0,84–0,98) | PASS |
| Bölüm sertifikaları | 8 certified-final (00c, 01, 02, 03, 04, 05, 06, 07) |
| **Nihai bütünsel durum** | **`certified-final`** |

**Karar gerekçesi:** Beş tez-düzeyi eksenin tümü PASS verdi. Tez bütünü teknik
olarak teslime hazır bir bütünlük gösteriyor: tam-tez HTML+DOCX render'ı sıfır
çözünmemiş çapraz-referans/atıfla üretiliyor, tez-geneli atıf evreninde tanımsız
künye yok, bölümler-arası sayısal iddialar senkron ve iki-repo değişmez testleri
tam geçiyor.

**`certified-final` koşulları karşılandı:** Playbook uyarınca bütünsel
`certified-final` için gereken (1) kullanıcının açık onayı ("Uygun", 2026-07-16)
ve (2) tüm bölüm sertifikalarının `certified-final` durumu sağlandı. Bu belge ve
tüm bölüm sertifikaları (00c, 01, 02, 03, 04, 05, 06, 07) `certified-final`
durumundadır.
