# NSCLC Sistematik Derleme Playbook'u — evidentia · minerva · sci-audit · aijudge

> **Kapsam kilidi (konstitüsyonel).** Bu playbook **yalnızca akciğer kanseri
> (öncelikli: küçük hücreli dışı akciğer kanseri — NSCLC) tedavi alanında bir
> SİSTEMATİK DERLEME (SR) / kanıt sentezi süreci** içindir ve **yalnızca `NSCLC/`
> alt-ağacında** yürütülür. **Ham/hasta-düzeyinde veri YOKTUR**; birincil analiz
> değil, **yayınlanmış literatürün sistematik sentezidir**. T1DM/EMBU/Beck/KİA
> bağlamı taşınmaz; kök tez artefaktları (`../data/`, `../outputs/`, `../_targets.R`,
> `../chapters/`, `../references/`) okunmaz/değiştirilmez. Ayrıntı:
> [`../00_context/KAPSAM_BEYANI.md`](../00_context/KAPSAM_BEYANI.md).

Bu belge, T1DM tez sürecinde olgunlaşan bilimsel araç proseslerini — evidentia
(çok-kaynaklı arama), minerva+openathens (telif-kapılı tam-metin), sci-audit
(PRISMA-merkezli adli denetim), aijudge/galileo (bağımsız LLM-judge + semantik) ve
klinik/regülatif bağlam katmanı (ich · titck · eudamed · yok-akademik · oecd) —
**PRISMA 2020 uyumlu bir sistematik derleme hattına** dizer. Amaç: aramadan
sentez ve raporlamaya kadar her adımın **önceden-kayıtlı**, **tekrarlanabilir**,
**izlenebilir** ve **bağımsız ikinci-görüşle sınanmış** olması.

---

## 0. Beş-katman mimarisi (SR fazlarına eşlenmiş)

| Katman | Süreç / sunucu | SR'deki rolü | Sayı besler mi | Ana çıktı |
|--------|----------------|--------------|:---:|-----------|
| **L1 — Arama** | **evidentia** (+ socius-vigil, yok-akademik = arama-lead) | Çok-veritabanlı sistematik arama; kayıt toplama; tekilleştirme; gri-lit lead | — | `search_log`, `records` |
| **L2 — Tam metin** | **minerva** + **openathens** + annas + anamnesis RAG | Dahil çalışmaların telif-kapılı tam metni; veri çıkarımı | **EVET** | `extraction_table` |
| **L3 — Denetim** | **sci-audit** | PRISMA/RoB/GRADE uyumu; claim grounding; istatistik; dil | — | eksen raporları + sertifika |
| **L4 — Bağımsız judge** | **aijudge / galileo** | HARD/SOFT/advisory; overclaim/HARKing/coherence; near-dup | — | judge JSON + advisory |
| **L5 — Klinik/regülatif bağlam** | **ich · titck · eudamed · yok-akademik · oecd/health-policy** | Metodoloji (estimand/GCP), TR ruhsat/uygulanabilirlik, tanı-testi/cihaz, epidemiyoloji arka plan | **HAYIR** | bağlam notları |

**Üç-katman kapı doktrini (T1DM'den devralınan invaryant):**
`HARD` (sci-audit deterministik) / `SOFT-block` (galileo eşikleri, insan-override'lı)
/ `advisory` (critical friend). **HARD kapı asla LLM-judge'dan gelmez.**

> **Somut arka uçlar (GDM science-skills).** L1/L2/L5 katmanları, açık ve
> deterministik (`uv`+Python CLI) bilimsel API skill'leriyle somutlaştırılabilir:
> ClinicalTrials.gov · PubMed · Europe PMC · OpenAlex (L1/L2), openFDA · Open
> Targets (L5). Bunlar yeni katman değildir; aynı kanıt≠bağlam ve kapı doktrinine
> tabidir. Eşleme:
> [`references/05_science_skills_onkoloji.md`](references/05_science_skills_onkoloji.md).

> **Kanıt ≠ bağlam (bağlayıcı).** Yalnız **L2 (kanıt katmanı)** çıkarım tablosuna
> ve sentez metnine sayı (HR/OS/PFS/ORR/GA) besleyebilir. **L5 (bağlam)** ve
> arama-lead (socius-vigil/yok-akademik) yalnız metodoloji, uygulanabilirlik veya
> tam-metne yönlendirme sağlar; sayı veremez. Deterministik zorlama:
> `scripts/context_source_guard.py` (F7 HARD). Detay:
> [`references/04_klinik_regulatif_mcp.md`](references/04_klinik_regulatif_mcp.md) §0.

> **SR ↔ birincil-çalışma farkı.** Burada "veri" = *çalışma-düzeyi çıkarılmış
> bulgular* (her dahil edilen yayının HR/OS/PFS/ORR + tasarımı), hasta-düzeyi ham
> veri değil. "Analiz" = *kanıt sentezi* (meta-analiz varsa çalışma-düzeyi etki
> havuzlama; yoksa yapılandırılmış narratif sentez). IPD-meta-analizi kapsam
> dışıdır (hasta-düzeyi veri gerektirir).

---

## 1. SR iş akışı — PRISMA 2020 uyumlu sekiz faz

Bir NSCLC derleme sorusu şu **sekiz fazdan** geçer. Her faz bir katmanı devreye
alır ve `NSCLC/<faz-klasörü>/` altında bir artefakt bırakır; hiçbir faz atlanmaz,
atlanırsa gerekçe rapora yazılır.

```
Soru → [F1 Protokol] → [F2 Arama] → [F3 Tarama] → [F4 Çıkarım]
     → [F5 Yanlılık/RoB] → [F6 Sentez±meta] → [F7 sci-audit+galileo] → [F8 Rapor+PRISMA]
```

### F1 — Protokol (önceden-kayıt) · `01_protocol/`
- PICOTS + dahil/hariç kriterleri + arama stratejisi taslağı + planlı sentez
  yöntemi + planlı RoB aracı + planlı GRADE. **HARKing'e karşı ön-taahhüt.**
- **PROSPERO kaydı zorunlu adım:** kayıt ID protokole yazılır; kayıt sonrası her
  sapma tarih + gerekçe ile protokole işlenir (PRISMA-P; F8 sertifikasında denetlenir).
- **Araç:** `/evidentia:evidentia-protocol` (PICO + arama stratejisi taslağı,
  evidentia P0–P1).
- **Metodoloji çerçevesi (bağlam):** `ich_search` ile **E9(R1) estimand** (popülasyon
  · tedavi · endpoint · intercurrent-event stratejisi · popülasyon-özeti),
  **E8(R1)** tasarım tipolojisi, **E6(R2)** GCP beklentisi protokole işlenir
  (bkz. [`references/04_klinik_regulatif_mcp.md`](references/04_klinik_regulatif_mcp.md) §1).
- Şablon: [`templates/01_protocol_template.md`](templates/01_protocol_template.md).
- Çıktı: `01_protocol/<konu>_protocol.md`.

### F2 — Sistematik arama (L1 evidentia) · `02_search/`
- Çok-veritabanlı arama: PubMed/MEDLINE, Embase (EPMC), Cochrane CENTRAL,
  **ClinicalTrials.gov**, kılavuz katmanı (NCCN/ESMO/ASCO). Her veritabanı için
  **tam arama dizesi + tarih + isabet sayısı** kaydedilir (tekrarlanabilirlik).
- Gri literatür + ileri/geri atıf taraması (snowballing) opsiyonel, kayıtlı.
- **Araçlar:** önce `/evidentia:evidentia-connectors` (connector preflight +
  G-PROBE), ardından `/evidentia:evidentia` veya `/evidentia:medical-research`
  (getirim→tarama→çıkarım, P0–P7); tekil arama tool'u `minerva_literature_search`.
  Toplanan künyeler `zotero-refs` koleksiyonuna alınır (F3 tekilleştirme dayanağı).
- **Gri-literatür & yerel kapsama (arama-lead):** `socius-vigil` (ASCO/ESMO/WCLC
  konferans özeti, ön-baskı, yayımlanmamış sinyal) + `yok-akademik` (TR tez/akademik).
  Bunlar **kayıt işaret eder, sayı vermez**; bulgular PRISMA "diğer yöntem"
  (`tanimlanan_kayit_diger_yontem`) olarak kaydedilir. Sınır:
  [`references/04_klinik_regulatif_mcp.md`](references/04_klinik_regulatif_mcp.md) §0, §5.
- **Deterministik arama arka uçları (GDM science-skills):** ClinicalTrials.gov
  (`clinical_trials_database` — yayınlanmamış/devam eden çalışma, yayın-yanlılığı),
  PubMed (`pubmed_database`), Europe PMC (`literature_search_europepmc`), OpenAlex
  (`literature_search_openalex` — DOI/ID çözümleme + atıf snowballing). Tümü
  `curl`/elle-API yerine oran-limitli sarmalayıcı CLI kullanır (G-REPRO); ön-baskı
  skill'leri (`_biorxiv`/`_arxiv`) arama-lead statüsündedir. Eşleme:
  [`references/05_science_skills_onkoloji.md`](references/05_science_skills_onkoloji.md) §1.
- Şablon: [`templates/02_search_strategy_template.md`](templates/02_search_strategy_template.md).
- Çıktı: `02_search/<konu>_search_log.md` + `02_search/<konu>_records.csv`.

### F3 — Tarama (screening) · `03_screening/`
- Tekilleştirme → başlık/özet taraması → tam-metin uygunluk. Her dışlama **PRISMA
  neden koduyla** kaydedilir. İki-bağımsız-tarayıcı simülasyonu + anlaşmazlık notu.
- Tekilleştirme `zotero-refs` koleksiyonuyla çapraz-doğrulanır (aynı çalışmanın
  çoklu yayını = tek çalışma; çalışma ≠ rapor).
- **PRISMA akış sayıları** burada üretilir (identified → screened → eligible →
  included); deterministik kontrol: `scripts/prisma_flow_check.py`.
- Şablon: [`templates/03_screening_log_template.csv`](templates/03_screening_log_template.csv).
- Çıktı: `03_screening/<konu>_screening.csv` + `03_screening/<konu>_prisma_counts.csv`.

### F4 — Veri çıkarımı (L2 minerva) · `04_extraction/`
- Dahil edilen her çalışmanın **tam metninden** yapılandırılmış çıkarım: popülasyon
  (histoloji/evre/belirteç/hat), müdahale/komparatör, endpoint (OS/PFS/ORR + HR +
  %95 GA + olay/örneklem), takip, fon/çıkar-çatışması. Kaynak lokatörü (PMID/DOI +
  tablo/şekil) zorunlu.
- **Araçlar:** `/evidentia:evidentia-fulltext`; tam-metin tool'ları
  `minerva_literature_fulltext_by_doi` / `minerva_rominedb_get_article`. Erişim
  zinciri legal-first: **EPMC/PMC açık-erişim → minerva → openathens (Tier 3) →
  yayıncı → annas-reader (son çare)** (bkz. referans §3). Açık-erişim ilk-başvuru
  arka uçları (GDM science-skills): `literature_search_europepmc` (PMCID→XML) ve
  `pubmed_database` (PMC BioC) — telif riski en düşük yol (G-COPYRIGHT). Dahil
  listesi büyükse openathens toplu erişimi (`oa_batch_submit`/`oa_batch_result`)
  kullanılır; hiçbiri erişemezse alan `unverified` + `gap_log`. Eşleme:
  [`references/05_science_skills_onkoloji.md`](references/05_science_skills_onkoloji.md) §2.
- **Deterministik yön kontrolü:** `scripts/extraction_direction_check.py`
  (`ci95_lo ≤ hr ≤ ci95_hi`, `hr > 0`, ORR ∈ [0,%100]).
- Şablon: [`templates/04_extraction_template.csv`](templates/04_extraction_template.csv).
- Çıktı: `04_extraction/<konu>_extraction.csv` (git-izli); tam metin
  `04_extraction/fulltext/` (git-dışı, telif).

### F5 — Yanlılık riski (RoB) · `05_appraisal/`
- Çalışma tipine göre araç: RCT→**RoB 2**, gözlemsel→**ROBINS-I**, tanısal→QUADAS-2.
- Alan-alan yargı + gerekçe + kaynak alıntı. **Sentezden önce tamamlanır.**
- **Araç:** `/evidentia:evidentia-appraise` (RoB2/ROBINS-I/QUADAS-2/NOS/PROBAST +
  GRADE, evidentia P5–P6) çıktısı `05_appraisal/<konu>_rob.csv`'ye normalize edilir.
- **Bağlam desteği:** endpoint/ölçüm standardı `ich_search` (ör. onkoloji
  endpoint tanımı); SR sorusu biyobelirteç **tanı testi/cihaz** içeriyorsa
  QUADAS-2 bağlamı için `eudamed` (MDR/IVDR; olgunluk `_caveat`'ı zorunlu). Bunlar
  **yargı gerekçesi** verir, duyarlılık/özgüllük sayısı vermez.
- Şablon: [`templates/05_rob_template.csv`](templates/05_rob_template.csv).
- Çıktı: `05_appraisal/<konu>_rob.csv`.

### F6 — Kanıt sentezi (± meta-analiz) · `06_synthesis/`
- **Meta-analiz uygunsa:** çalışma-düzeyi etki havuzlama (rastgele/sabit etki),
  heterojenite (I²/τ²), forest/funnel, alt-grup/meta-regresyon (önceden-planlı).
- **Uygun değilse (heterojenite/az çalışma):** SWiM ilkeleriyle yapılandırılmış
  narratif sentez. **Vote-counting yerine yön + kesinlik.**
- **GRADE** kanıt profili: her endpoint için kesinlik (yüksek→çok düşük) + gerekçe.
- **Araç:** `/evidentia:evidentia-synthesize` (graph-RAG derin sentez, P4+P6).
- **TR uygulanabilirlik / dış geçerlik (bağlam):** ajanın TR ruhsat/KÜB durumu
  `titck` (kamu yüzü `titck-cache`, anahtarsız); akciğer kanseri yükü/politika arka
  planı `oecd`/`health-policy`. FDA onay/etiket/güvenlik arka planı `openfda`
  (`openfda_database`); biyobelirteç-ilaç mekanizması `opentargets`
  (`opentargets_database`). Bunlar **sentez havuzuna sayı katmaz**
  (`source_tier=context`); ayrı "TR'ye uygulanabilirlik" alt-başlığına yazılır
  (bkz. referans §2, §6 ve [`references/05_science_skills_onkoloji.md`](references/05_science_skills_onkoloji.md) §3).
- Şablon: [`templates/06_grade_sof_template.csv`](templates/06_grade_sof_template.csv).
- Çıktı: `06_synthesis/<konu>_synthesis.md` + `06_synthesis/<konu>_grade.csv`
  (+ meta varsa `06_synthesis/<konu>_meta.csv`).

### F7 — Denetim + bağımsız judge (L3+L4) · `08_reports/`
- **HARD (deterministik önce):** `scripts/run_hard_gate.py` → PRISMA-akış
  aritmetiği + çıkarım yön-mantığı + kaynak-tekilliği + **bağlam-kaynak koruması
  (`context_source_guard`: bağlam/lead sunucudan sayı = blocker)** + Türkçe `p`
  imlası. Ardından sci-audit 7 eksen (PRISMA-merkezli, §3).
- **SOFT/advisory (HARD temiz olmadan koşulmaz):** galileo tool'ları
  `galileo_claim_source_match` (groundedness/faithfulness), `galileo_overclaim_judge`,
  `galileo_harking_judge`, `galileo_coherence`, `galileo_bib_dedup`; tam-tez için
  `galileo_full_thesis_judge`.
- Çıktı: `08_reports/<konu>_sci-audit.md` + `08_reports/<konu>_galileo.md`.

### F8 — Manüskript + PRISMA raporlama · `07_manuscript/` + `08_reports/`
- Taslak PRISMA 2020 27-madde + PRISMA akış diyagramı sayılarıyla yazılır.
- Atıf/bibliyografya `zotero-refs` koleksiyonundan üretilir.
- Yerelleştirme/TR-bağlam: `titck` (ruhsat) + `yok-akademik` (TR literatür) tartışma
  bölümünü besler (yalnız bağlam, sayı değil).
- Sertifika: HARD temiz + SOFT düzeltilmiş/gerekçeli + **PROSPERO kayıt-sapma
  kontrolü (PRISMA-P)** + AI-use log yazılmış.
- Çıktı: `07_manuscript/<konu>.md` + `08_reports/<konu>_certificate.md`.

---

## 2. Katman referansları (derin protokoller)

- **L1/L2 evidentia+minerva (SR arama & çıkarım):**
  [`references/01_evidentia_onkoloji.md`](references/01_evidentia_onkoloji.md)
- **L3 sci-audit (PRISMA/RoB/GRADE denetimi):**
  [`references/02_sciaudit_onkoloji.md`](references/02_sciaudit_onkoloji.md)
- **L4 aijudge/galileo (bağımsız judge):**
  [`references/03_aijudge_galileo_onkoloji.md`](references/03_aijudge_galileo_onkoloji.md)
- **L5 klinik/regülatif bağlam (ich·titck·eudamed·yok-akademik·oecd):**
  [`references/04_klinik_regulatif_mcp.md`](references/04_klinik_regulatif_mcp.md)

---

## 3. Denetim özeti — SR'ye özgü kapılar

### 3.1 Kanıt/arama kapıları (L1/L2)
- **G-COVERAGE:** çok-veritabanı (PubMed+Embase+Cochrane+ClinicalTrials+kılavuz)
  kapsandı mı; her biri için arama dizesi+tarih+isabet kayıtlı mı?
- **G-REPRO:** arama tam olarak tekrarlanabilir mi (dize + filtre + tarih)?
- **G-PRISMA-FLOW:** identified/screened/eligible/included sayıları tutarlı;
  dışlama nedenleri kodlu mu?
- **G-RAG:** her çıkarılmış endpoint tam-metin lokatörüne bağlı mı?
- **G-NSCLC:** histoloji/evre/belirteç/hat/komparatör/endpoint + transfer sınırı açık mı?
- **G-COPYRIGHT:** tam metin hedefli; toptan verbatim yok.
- **G-HARKING:** alt-grup/sentez kararı protokolde önceden mi tanımlı (post-hoc işaretli)?

### 3.2 sci-audit yedi ekseni (PRISMA-merkezli — detay §referans)
A referans bütünlüğü · B claim grounding · C istatistik (HR↔GA↔p, I², havuzlama) ·
D halüsinasyon · **E raporlama-kılavuzu (PRISMA 2020 + RoB + GRADE)** · F AI-şeffaflık ·
G Türkçe imla.

---

## 4. Sayısal bütünlük kaideleri (SR uyarlaması, zorunlu)

Bir sayısal sonuç (havuzlanmış HR, I², tekil çalışma OS/PFS/ORR, GRADE kesinliği)
üreten her adımda bağlayıcı:

1. **Kaynak-tekilliği:** tekil çalışma sayısı `04_extraction/<konu>_extraction.csv`'den;
   havuzlanmış sayı `06_synthesis/<konu>_meta.csv`'den okunur — metne gömülü literal
   taşınmaz.
2. **Yön-mantığı:** koruyucu etki HR<1; GA alt ≤ üst; I² ∈ [0,%100]; ORR ∈ [0,%100].
3. **Yeniden-ifade tutarlılığı:** aynı havuzlanmış etki özette, forest'ta ve SoF
   tablosunda aynı değeri gösterir.
4. **İzlenebilirlik:** her tekil sayı PMID/DOI+lokatöre; her havuzlanmış sayı
   çıkarım tablosu + sentez artefaktına kadar izlenir.

---

## 5. Kullanım — hızlı başlangıç

```bash
# F1 Protokol   → /evidentia:evidentia-protocol       → 01_protocol/<konu>_protocol.md (PICOTS + PROSPERO ID)
# F2 Arama      → /evidentia:evidentia-connectors (preflight)
#                 → /evidentia:evidentia "<SR sorusu>" → 02_search/<konu>_search_log.md + records.csv
#                 (tool: minerva_literature_search; künyeler → zotero-refs)
# F3 Tarama     → 03_screening/<konu>_screening.csv + prisma_counts.csv
#                 python3 scripts/prisma_flow_check.py 03_screening/<konu>_prisma_counts.csv
# F4 Çıkarım    → /evidentia:evidentia-fulltext <DOI/PMID/NCT>  → 04_extraction/<konu>_extraction.csv
#                 (tool: minerva_literature_fulltext_by_doi; zincir minerva→openathens→annas)
#                 python3 scripts/extraction_direction_check.py 04_extraction/<konu>_extraction.csv
# F5 RoB        → /evidentia:evidentia-appraise        → 05_appraisal/<konu>_rob.csv (RoB2/ROBINS-I/GRADE)
# F6 Sentez     → /evidentia:evidentia-synthesize      → 06_synthesis/<konu>_synthesis.md + grade.csv (+ meta.csv)
# F7 Denetim    → python3 scripts/run_hard_gate.py 07_manuscript/<konu>.md \
#                       --extraction 04_extraction/<konu>_extraction.csv \
#                       --meta 06_synthesis/<konu>_meta.csv \
#                       --prisma 03_screening/<konu>_prisma_counts.csv        (HARD; deterministik)
#                 → /sci-audit:audit 07_manuscript/<konu>.md --lang tr --type prisma  (HARD; eksen)
#                 → galileo_claim_source_match / _overclaim_judge / _harking_judge   (SOFT/advisory)
# F8 Rapor      → 07_manuscript/<konu>.md + 08_reports/<konu>_certificate.md
#                 (atıflar: zotero-refs; sertifikada PROSPERO kayıt-sapma kontrolü)
```

---

## 6. Sınırlar ve yasaklar (özet)

- **Kapsam:** yalnız akciğer kanseri tedavisi; yalnız `NSCLC/` alt-ağacı; **SR/kanıt
  sentezi** (birincil klinik çalışma değil).
- **Ham veri yok:** hasta-düzeyi veri toplanmaz/saklanmaz; IPD-meta kapsam dışı.
- **Telif:** tam metin hedefli çıkarım; toptan verbatim çoğaltma yasak (G-COPYRIGHT).
- **No-fabrication:** çözülemeyen kaynak/sayı `unverified`; uydurma NCT/PMID/DOI/endpoint yasak.
- **Önceden-kayıt:** sentez/alt-grup kararları protokolde; post-hoc açıkça işaretli (G-HARKING).
- **HARD kapı yalnız deterministik:** LLM-judge yalnız SOFT/advisory.
- **Kök teze sızma yasağı:** NSCLC çıktıları T1DM tez artefaktlarına yazılmaz.

---

*Bu playbook, beş-katman bilimsel araç doktrinini (evidentia · minerva/openathens ·
sci-audit · aijudge/galileo · klinik-regülatif bağlam) akciğer kanseri tedavi alanında
PRISMA 2020 uyumlu bir sistematik derleme hattına uyarlayan kanonik NSCLC iş
rehberidir. Katmanların açık/deterministik arka uçları (GDM science-skills:
ClinicalTrials.gov · PubMed · Europe PMC · OpenAlex · openFDA · Open Targets)
[`references/05_science_skills_onkoloji.md`](references/05_science_skills_onkoloji.md)'de
eşlenir. Derin protokoller `references/`, şablonlar `templates/` altındadır.*
