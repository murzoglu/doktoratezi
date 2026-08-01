# Niteliksel Manüskript Denetimi — sci-audit Köprüsü

> **Amaç:** Yazılan niteliksel `.qmd`/paragrafı yayın-öncesi adli + dilsel denetimden geçirmek.
> Bu skill niteliksel metni **üretir**; `evidentia` dış metodoloji kanıtını **getirir**;
> **`sci-audit` ortaya çıkan metni denetler**; repo `t1dm-qual-ai-audit` + `dmnitel` ham-veri/
> KVKK/quote-parity sınırını korur. Dört katman birbirini besler, karışmaz.

Kalıp `t1dm-tez-rehberi/references/manuskript-denetimi-sciaudit.md` ile aynıdır; farkı **niteliksel
kola özgü eksen vurgusudur**: axis E'de kılavuz **COREQ/JARS-Qual** (STROBE/PRISMA değil).

## 0. Katman sınırı

| Katman | Araç | Kapsam |
|---|---|---|
| İç niteliksel analiz + yazım | `niteliksel-arastirma-rehberi-t1dm` | 21 görüşme, kodlama, tema, yorum, `.qmd` üretimi |
| Dış metodoloji kanıtı | `evidentia` | RTA/COREQ/bilgi gücü kaynakları, konumlandırma, citation |
| Metin adli + dilsel denetim | **`sci-audit`** (A-G) | Yazılan metnin referans/claim/istatistik/halüsinasyon/kılavuz/AI-şeffaflık/Türkçe imla |
| Ham-veri/KVKK/quote-parity | repo `t1dm-qual-ai-audit` + `dmnitel` | Anonimlik, quote_id parity, KVKK sınırı |

## 1. Yedi Eksen — Niteliksel Vurgu

| Eksen | Ne denetler | Komut | Niteliksel not |
|---|---|---|---|
| **A referans** | Uydurma/yanlış-atıf/geri-çekilme; DOI/PMID checksum | `/sci-audit:verify-citations` | Braun-Clarke/Tong/Malterud künyeleri doğrulanır |
| **B claim grounding** | İddia kaynağa bağlı mı | (full `audit`) | İç-veri iddiası kanonik rapora; dış-iddia PMID/DOI'ye |
| **C istatistik** | statcheck/GRIM, yüzde/altgrup, ondalık virgül | `/sci-audit:check-stats` | COREQ tabloları (30/2/0), kod yoğunluğu, quote sayıları tutarlı mı |
| **D halüsinasyon** | Aşırı-kesinlik, uydurma yöntem/varlık | (full `audit`) | "Kanıtlar/neden olur" gibi genelleme/nedensellik dili yakalanır |
| **E raporlama** | **COREQ / JARS-Qual** madde-madde | `/sci-audit:guideline-check --type coreq` (+`jars`) | **Birincil eksen** — 32 madde + karma için JARS |
| **F AI-şeffaflık** | ICMJE/COPE AI beyanı | (full `audit`) | LLM-use statement var mı (kanonik rapor §4) |
| **G Türkçe imla** | Encoding, ondalık virgül, register | `/sci-audit:check-turkish` | İngilizce ondalık-nokta `p` **blocker**; Türkçe otomatik |

**Orkestratör:** `/sci-audit:audit <qmd> --lang tr --strictness certification --type coreq` yedi
ekseni tek koşumda; `/sci-audit:audit-report --out tez-yazim/04_kalite-kontrol/raporlar/<ad>-sci-audit.md`.

## 2. Niteliksel-özgü kontroller (axis E odaklı)
- COREQ Madde 16 (pilot) ve 31 (negatif vaka) kapatma durumu metinde açık mı?
- Tema = analitik iddia mı (domain-summary değil)?
- Örneklem gerekçesi bilgi gücü mü (doygunluk dili yanlış kullanılmamış mı)?
- Inter-coder/kappa **yanlışlıkla** raporlanmış mı? (RTA'da olmamalı — `gecerlik-ve-degerlendirme.md §3`)
- Verbatim alıntı sızmış mı? (yalnız `quote_id` olmalı — KVKK).

## 3. Galileo three-tier (sci-audit'in yanında)
sci-audit Claude-native; **Galileo** bağımsız GPT-5.4 ikinci görüş (9 araç: `galileo_judge`,
`galileo_consistency`, `galileo_bib_dedup`, `galileo_claim_source_match`, `galileo_eval_run`,
`galileo_stats` + başlık/tutarlılık/referans-nesri katmanı `galileo_heading_cascade` [Marmara
§1.3+§5, deterministik, code-fence-aware], `galileo_coherence` [gemini-embedding paragraf akışı],
`galileo_reference_prose` [atıf yoğunluğu/monotonluk/Tartışma-sıfır-atıf]). **HARD** = sci-audit A-G (değişmez); **SOFT-block** = Galileo
(groundedness/faithfulness < 0,60; nicel/olgusal claim `citation_support=unsupported`; bölümler-arası
çelişki; insan-override'lı); **advisory** = bib-dup/tekrar/üslup. Faz 3.6'da 7-eksenden sonra çağrılır.
KVKK: gateway'e yalnız manüskript + literatür + `references.bib`; ham/kimlikleyici asla.

## 4. Davranış kuralları
1. Metin adli denetimi yalnız sci-audit'te; repo ai-audit'te tekrarlanmaz.
2. Yedi eksen atlanmaz; niteliksel kapanışta **axis E COREQ** zorunlu.
3. Türkçe metinde axis G zorunlu; ondalık-nokta `p` blocker.
4. No-fabrication: çözülemeyen `unverified`.
5. Ham-veri/KVKK/quote-parity sci-audit'e sorulmaz (`dmnitel` + repo ai-audit).

## Çapraz referanslar
- Raporlama standardı → `raporlama-coreq-jars.md`
- Dış kanıt → `literatur-kanit-evidentia.md`
- Nicel köprü kalıbı → `t1dm-tez-rehberi/references/manuskript-denetimi-sciaudit.md`
