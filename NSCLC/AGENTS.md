# AGENTS.md — NSCLC Sistematik Derleme Ajan Rehberi

Bu alt-ağaç, akciğer kanseri (NSCLC) tedavi alanında **PRISMA 2020 uyumlu bir
sistematik derleme (SR)** yürütür. Kök doktora tezinden (T1DM & Ebeveynlik
Tutumu) **tam yalıtılmıştır**. İşe başlamadan önce
[`00_context/KAPSAM_BEYANI.md`](00_context/KAPSAM_BEYANI.md) (konstitüsyonel
sınırlar) ve [`playbook/NSCLC_PLAYBOOK.md`](playbook/NSCLC_PLAYBOOK.md) (iş akışı)
okunur.

## Değişmez sınırlar (özet)

- **Konu:** yalnız akciğer kanseri tedavisi (öncelik NSCLC). Başka alan yok.
- **Tür:** sistematik derleme / kanıt sentezi — **birincil çalışma değil**.
- **Ham veri yok:** hasta-düzeyi veri toplanmaz; yalnız yayınlanmış literatürden
  künye + çalışma-düzeyi çıkarılmış veri izlenir. **IPD-meta kapsam dışı.**
- **Dizin:** yalnız `NSCLC/`. Kök artefaktlar (`../data/`, `../outputs/`,
  `../_targets.R`, `../chapters/`, `../R/`, `../references/`, `../thesis.qmd`,
  `../tez-yazim/`, `../niteliksel/`) **okunmaz/değiştirilmez**.
- **Sızma yok:** NSCLC çıktıları kök tez artefaktlarına yazılmaz.
- **T1DM bağlamı taşınmaz.**

## Kanonik dizin haritası

| Dizin | Faz | Çıktı |
|-------|-----|-------|
| `00_context/` | — | `KAPSAM_BEYANI.md` |
| `01_protocol/` | F1 | `<konu>_protocol.md` |
| `02_search/` | F2 | `<konu>_search_log.md`, `<konu>_records.csv` |
| `03_screening/` | F3 | `<konu>_screening.csv`, `<konu>_prisma_counts.csv` |
| `04_extraction/` | F4 | `<konu>_extraction.csv`; `fulltext/` (git-dışı) |
| `05_appraisal/` | F5 | `<konu>_rob.csv` |
| `06_synthesis/` | F6 | `<konu>_synthesis.md`, `<konu>_grade.csv`, `<konu>_meta.csv` |
| `07_manuscript/` | F8 | `<konu>.md` |
| `08_reports/` | F7/F8 | `<konu>_sci-audit.md`, `<konu>_galileo.md`, `<konu>_certificate.md` |
| `09_ai_use_log/` | — | `ai_use_log.csv` |
| `scripts/` | F7 | `run_hard_gate.py` + 4 deterministik denetçi + testler |
| `playbook/` | — | `NSCLC_PLAYBOOK.md`, `references/`, `templates/` |

## Beş-katman araç doktrini

| Katman | Süreç / sunucu | SR rolü | Sayı besler |
|--------|----------------|---------|:---:|
| L1 Arama | **evidentia** (+ socius-vigil, yok-akademik = lead) | Çok-veritabanlı arama + tekilleştirme + gri-lit lead | — |
| L2 Tam metin | **minerva** + **openathens** + annas | Telif-kapılı tam metin → çıkarım | **EVET** |
| L3 Denetim | **sci-audit** | PRISMA/RoB/GRADE + claim grounding + istatistik | — |
| L4 Judge | **aijudge/galileo** | Bağımsız LLM-judge (SOFT/advisory) | — |
| L5 Bağlam | **ich · titck · eudamed · yok-akademik · oecd** | Metodoloji (estimand/GCP), TR ruhsat, tanı-testi, epidemiyoloji | **HAYIR** |

**Kanıt ≠ bağlam (bağlayıcı):** yalnız L2 çıkarım/sentez'e sayı besler; L5 + lead
yalnız metodoloji/uygulanabilirlik/yönlendirme verir. Zorlama:
`scripts/context_source_guard.py`. Detay:
[`playbook/references/04_klinik_regulatif_mcp.md`](playbook/references/04_klinik_regulatif_mcp.md).

**Deterministik açık arka uçlar (GDM science-skills):** L1/L2/L5 katmanları,
açık ve betik-tabanlı (`uv`+Python CLI) bilimsel API skill'leriyle somutlaştırılır —
ClinicalTrials.gov · PubMed · Europe PMC · OpenAlex (L1/L2), openFDA · Open Targets
(L5 bağlam). Yeni katman değildir; aynı kanıt≠bağlam + kapı doktrinine tabidir.
Eşleme: [`playbook/references/05_science_skills_onkoloji.md`](playbook/references/05_science_skills_onkoloji.md).

## Üç-katman kapı doktrini (invaryant)

- **HARD** — sci-audit deterministik. Teslim engeli. **Asla LLM-judge'dan gelmez.**
- **SOFT-block** — galileo eşikleri; insan-override'lı.
- **advisory** — critical friend; bilgilendirici.

## SR'ye özgü kapılar

- **G-COVERAGE:** PubMed+Embase+Cochrane+ClinicalTrials+kılavuz kapsandı; her biri
  arama dizesi+tarih+isabet ile kayıtlı.
- **G-REPRO:** arama tam tekrarlanabilir (dize + filtre + tarih).
- **G-PRISMA-FLOW:** identified/screened/eligible/included tutarlı; dışlama nedenleri kodlu.
- **G-RAG:** her çıkarılmış endpoint tam-metin lokatörüne (PMID/DOI + tablo/şekil) bağlı.
- **G-NSCLC:** histoloji/evre/belirteç/hat/komparatör/endpoint + transfer sınırı açık.
- **G-COPYRIGHT:** hedefli çıkarım; toptan verbatim yok.
- **G-HARKING:** sentez/alt-grup kararı protokolde önceden; post-hoc işaretli.

## Sayısal bütünlük kaideleri (zorunlu)

Havuzlanmış HR, I², tekil çalışma OS/PFS/ORR veya GRADE kesinliği üreten her adımda:

1. **Kaynak-tekilliği:** tekil sayı `04_extraction/<konu>_extraction.csv`'den;
   havuzlanmış sayı `06_synthesis/<konu>_meta.csv`'den okunur — metne gömülü literal yok.
2. **Yön-mantığı:** koruyucu etki HR<1; GA alt ≤ üst; I² ∈ [0,%100]; ORR ∈ [0,%100].
3. **Yeniden-ifade tutarlılığı:** aynı etki özette, forest'ta ve SoF tablosunda aynı.
4. **İzlenebilirlik:** tekil sayı PMID/DOI+lokatöre; havuzlanmış sayı çıkarım+sentez
   artefaktına kadar izlenir.

## Deterministik HARD-gate (F7 Adım 0)

LLM eksenlerinden **önce** koşulur; teslim engeli yalnız buradan + sci-audit'ten
gelir (galileo asla HARD üretmez):

```bash
python3 scripts/run_hard_gate.py 07_manuscript/<konu>.md \
    --extraction 04_extraction/<konu>_extraction.csv \
    --meta 06_synthesis/<konu>_meta.csv \
    --prisma 03_screening/<konu>_prisma_counts.csv --lang tr
```

Denetçiler: PRISMA akış aritmetiği · çıkarım yön-mantığı · **bağlam-kaynak koruması
(kanıt≠bağlam)** · kaynak-tekilliği · Türkçe `p` imlası. Detay:
[`scripts/README.md`](scripts/README.md).

## No-fabrication

- Uydurma NCT/PMID/DOI/endpoint/HR **yasak**. Çözülemeyen kaynak/sayı `unverified`.
- Ondalık ayırıcı virgül; APA 7 + PRISMA 2020.

## Onay gerektiren durumlar

Kapsamı genişletmek · `NSCLC/` dışına yazmak · ham/IPD veri · HARD'ı LLM-judge'a
dayandırmak · commit/push/PR — **açık onay olmadan yapılmaz**.

## Bağlantılar

- Kapsam beyanı: [`00_context/KAPSAM_BEYANI.md`](00_context/KAPSAM_BEYANI.md)
- İş rehberi: [`playbook/NSCLC_PLAYBOOK.md`](playbook/NSCLC_PLAYBOOK.md)
- L1/L2 evidentia+minerva: [`playbook/references/01_evidentia_onkoloji.md`](playbook/references/01_evidentia_onkoloji.md)
- L3 sci-audit: [`playbook/references/02_sciaudit_onkoloji.md`](playbook/references/02_sciaudit_onkoloji.md)
- L4 aijudge/galileo: [`playbook/references/03_aijudge_galileo_onkoloji.md`](playbook/references/03_aijudge_galileo_onkoloji.md)
- L5 klinik/regülatif bağlam: [`playbook/references/04_klinik_regulatif_mcp.md`](playbook/references/04_klinik_regulatif_mcp.md)
- GDM science-skills deterministik arka uçlar: [`playbook/references/05_science_skills_onkoloji.md`](playbook/references/05_science_skills_onkoloji.md)
- Şablonlar: [`playbook/templates/`](playbook/templates/)
