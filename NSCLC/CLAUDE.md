# CLAUDE.md — NSCLC Sistematik Derleme

Akciğer kanseri (NSCLC) tedavi alanında **PRISMA 2020 uyumlu sistematik derleme
(SR)**. Kök doktora tezinden (T1DM & Ebeveynlik Tutumu) **tam yalıtılmış** bir
alt-ağaç. **Ham/hasta-düzeyi veri yoktur**; yayınlanmış literatürden kanıt
sentezidir.

> İşe başlamadan önce [`00_context/KAPSAM_BEYANI.md`](00_context/KAPSAM_BEYANI.md)
> (konstitüsyonel sınırlar) okunur. Ajan sözleşmesi:
> [`AGENTS.md`](AGENTS.md). İş akışı: [`playbook/NSCLC_PLAYBOOK.md`](playbook/NSCLC_PLAYBOOK.md).

## Ne / ne değil

- **Ne:** yalnız akciğer kanseri tedavisi; SR/kanıt sentezi; yalnız `NSCLC/`.
- **Ne değil:** birincil klinik çalışma değil; ham/IPD veri yok; T1DM bağlamı yok;
  kök tez artefaktlarına dokunulmaz.

## SR iş akışı — sekiz faz (PRISMA 2020)

```
Soru → [F1 Protokol] → [F2 Arama] → [F3 Tarama] → [F4 Çıkarım]
     → [F5 RoB] → [F6 Sentez±meta] → [F7 sci-audit+galileo] → [F8 Rapor+PRISMA]
```

| Faz | Dizin | Katman | Çıktı |
|-----|-------|--------|-------|
| F1 Protokol | `01_protocol/` | L5 ich (estimand/GCP) | önceden-kayıtlı protokol (PICOTS) |
| F2 Arama | `02_search/` | L1 evidentia (+ CT.gov/PubMed/EPMC/OpenAlex skill; socius-vigil/yok-akademik lead) | search_log + records.csv |
| F3 Tarama | `03_screening/` | — | screening.csv + prisma_counts.csv |
| F4 Çıkarım | `04_extraction/` | L2 minerva + openathens (+ EPMC/PMC açık-erişim skill) | extraction.csv (fulltext git-dışı) |
| F5 RoB | `05_appraisal/` | L5 ich/eudamed (bağlam) | rob.csv (RoB 2 / ROBINS-I) |
| F6 Sentez | `06_synthesis/` | L5 titck/oecd/openfda/opentargets (uygulanabilirlik) | synthesis.md + grade.csv (+ meta.csv) |
| F7 Denetim | `08_reports/` | L3+L4 | sci-audit.md + galileo.md |
| F8 Rapor | `07_manuscript/` + `08_reports/` | L5 titck/yok-akademik | manüskript + certificate.md |

## Komutlar (hızlı başlangıç)

```bash
# F1 Protokol   → /evidentia:evidentia-protocol         → 01_protocol/<konu>_protocol.md (+PROSPERO ID)
#                 (bağlam: ich_search E9 estimand / E6 GCP / E8 tasarım)
# F2 Arama      → /evidentia:evidentia-connectors → /evidentia:evidentia → 02_search/<konu>_records.csv
#                 (tool: minerva_literature_search; künyeler → zotero-refs)
#                 (lead: socius-vigil gri-lit + yok-akademik TR → "diğer yöntem")
# F3 Tarama     → 03_screening/<konu>_screening.csv + prisma_counts.csv
#                 python3 scripts/prisma_flow_check.py 03_screening/<konu>_prisma_counts.csv
# F4 Çıkarım    → /evidentia:evidentia-fulltext <DOI/PMID/NCT> → 04_extraction/<konu>_extraction.csv
#                 (EPMC→minerva→openathens[oa_batch]→annas; source_tier=evidence ZORUNLU)
#                 python3 scripts/extraction_direction_check.py + context_source_guard.py ...
# F5 RoB        → /evidentia:evidentia-appraise          → 05_appraisal/<konu>_rob.csv
#                 (bağlam: ich endpoint standardı; eudamed tanı-testi ise)
# F6 Sentez     → /evidentia:evidentia-synthesize        → 06_synthesis/<konu>_synthesis.md + grade.csv
#                 (bağlam: titck TR ruhsat/uygulanabilirlik; oecd arka plan)
# F7 Denetim    → python3 scripts/run_hard_gate.py 07_manuscript/<konu>.md \
#                     --extraction ... --meta ... --prisma ... --lang tr   (HARD; deterministik)
#                 → /sci-audit:audit 07_manuscript/<konu>.md --lang tr --type prisma  (HARD; eksen)
#                 → galileo_claim_source_match / _overclaim_judge / _harking_judge   (SOFT/advisory)
# F8 Rapor      → 07_manuscript/<konu>.md + 08_reports/<konu>_certificate.md  (atıflar: zotero-refs)
```

## Üç-katman kapı doktrini

- **HARD** (sci-audit deterministik) — teslim engeli; asla LLM-judge'dan gelmez.
- **SOFT-block** (galileo) — insan-override'lı.
- **advisory** — bilgilendirici.

## Sayısal bütünlük (özet)

- Tekil sayı `04_extraction/*.csv`'den; havuzlanmış sayı `06_synthesis/*_meta.csv`'den
  okunur — gömülü literal yok.
- Yön-mantığı: HR<1 koruyucu; GA alt ≤ üst; I²/ORR ∈ [0,%100].
- İzlenebilirlik: her sayı PMID/DOI+lokatöre kadar.
- **Kanıt ≠ bağlam:** sayı yalnız `source_tier=evidence` (minerva/openathens/annas)
  satırından gelebilir; ich/titck/eudamed/oecd (bağlam) ve socius-vigil/yok-akademik
  (lead) sayı besleyemez (`context_source_guard`).
- Uydurma yasak; çözülemeyen `unverified`. Ondalık virgül; APA 7 + PRISMA.

## Ayrıntı

Tam iş rehberi, katman referansları ve şablonlar için:
[`playbook/NSCLC_PLAYBOOK.md`](playbook/NSCLC_PLAYBOOK.md).

Katmanların açık/deterministik arka uçları (GDM science-skills: ClinicalTrials.gov ·
PubMed · Europe PMC · OpenAlex · openFDA · Open Targets):
[`playbook/references/05_science_skills_onkoloji.md`](playbook/references/05_science_skills_onkoloji.md).
