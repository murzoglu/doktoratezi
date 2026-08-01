# NSCLC — Akciğer Kanseri Tedavisi Sistematik Derleme

Akciğer kanseri (öncelik: küçük hücreli dışı akciğer kanseri — NSCLC) tedavi
alanında **PRISMA 2020 uyumlu sistematik derleme (SR) / kanıt sentezi** çalışma
alanı. Kök doktora tezinden (T1DM & Ebeveynlik Tutumu) **tam yalıtılmış** bir
alt-ağaç.

> **Ham/hasta-düzeyi veri yoktur.** Bu bir kanıt sentezidir: yalnızca yayınlanmış
> literatürden künye + çalışma-düzeyi çıkarılmış veri (HR/OS/PFS/ORR + %95 GA)
> izlenir. IPD-meta kapsam dışıdır.

## Sınırlar (özet)

- **Konu:** yalnız akciğer kanseri tedavisi.
- **Tür:** sistematik derleme — birincil çalışma değil.
- **Dizin:** yalnız `NSCLC/`; kök tez artefaktları okunmaz/değiştirilmez.
- **Bağlam:** T1DM/EMBU/Beck/KİA taşınmaz.

Konstitüsyonel ayrıntı: [`00_context/KAPSAM_BEYANI.md`](00_context/KAPSAM_BEYANI.md).

## Dizin yapısı

```
NSCLC/
├── 00_context/          Kapsam beyanı (konstitüsyonel sınırlar)
├── 01_protocol/         F1 · önceden-kayıtlı protokol (PICOTS, dahil/hariç)
├── 02_search/           F2 · arama logu + kayıtlar (records.csv)
├── 03_screening/        F3 · tarama logu + PRISMA akış sayıları
├── 04_extraction/       F4 · çıkarım tablosu
│   └── fulltext/        (telif, git-dışı)
├── 05_appraisal/        F5 · yanlılık riski (RoB 2 / ROBINS-I / QUADAS-2)
├── 06_synthesis/        F6 · kanıt sentezi (± meta) + GRADE
├── 07_manuscript/       F8 · manüskript taslağı
├── 08_reports/          F7/F8 · sci-audit + galileo + sertifika
├── 09_ai_use_log/       Yapay zekâ kullanım kütüğü
├── scripts/             Deterministik HARD-gate denetçileri (F7 Adım 0)
│   ├── run_hard_gate.py           Orkestratör (5 denetçi)
│   ├── prisma_flow_check.py       PRISMA akış aritmetiği
│   ├── extraction_direction_check.py  Yön-mantığı (HR/GA/I²/ORR/p)
│   ├── context_source_guard.py        Kanıt≠bağlam (bağlam/lead sayı veremez)
│   ├── source_singularity_check.py    Metin↔artefakt (gömülü literal)
│   ├── turkish_p_check.py         Türkçe ondalık-virgül imlası
│   └── test_hard_gate.py          Regresyon testleri (15 test)
├── playbook/
│   ├── NSCLC_PLAYBOOK.md          İş rehberi (8 faz)
│   ├── references/                Katman derin protokolleri
│   │   ├── 01_evidentia_onkoloji.md      L1/L2 arama + tam metin (openathens 6 araç)
│   │   ├── 02_sciaudit_onkoloji.md       L3 PRISMA/RoB/GRADE denetimi
│   │   ├── 03_aijudge_galileo_onkoloji.md L4 bağımsız judge
│   │   ├── 04_klinik_regulatif_mcp.md    L5 ich/titck/eudamed/yok-akademik/socius-vigil
│   │   └── 05_science_skills_onkoloji.md GDM science-skills deterministik arka uçlar
│   └── templates/                Faz şablonları (protokol, arama, tarama,
│                                  çıkarım, RoB, GRADE SoF, PRISMA akış)
├── AGENTS.md            Ajan sözleşmesi
├── CLAUDE.md            Proje özeti + iş akışı
└── .gitignore
```

## SR iş akışı — sekiz faz

```
Soru → [F1 Protokol] → [F2 Arama] → [F3 Tarama] → [F4 Çıkarım]
     → [F5 RoB] → [F6 Sentez±meta] → [F7 sci-audit+galileo] → [F8 Rapor+PRISMA]
```

Tam faz açıklamaları ve komutlar: [`playbook/NSCLC_PLAYBOOK.md`](playbook/NSCLC_PLAYBOOK.md).

## Beş-katman araç doktrini

- **L1 evidentia** — çok-veritabanlı sistematik arama (+ socius-vigil/yok-akademik = gri-lit/TR lead)
- **L2 minerva + openathens + annas** — telif-kapılı tam metin → çıkarım *(tek "sayı besleyen" katman)*
- **L3 sci-audit** — PRISMA/RoB/GRADE + claim grounding (HARD)
- **L4 aijudge/galileo** — bağımsız judge (SOFT/advisory)
- **L5 ich · titck · eudamed · yok-akademik · oecd** — klinik/regülatif bağlam (metodoloji, TR ruhsat, tanı-testi, epidemiyoloji)

Kapı doktrini: HARD (deterministik) / SOFT-block (galileo) / advisory. **HARD asla
LLM-judge'dan gelmez.** **Kanıt ≠ bağlam:** yalnız L2 çıkarım/sentez'e sayı besler;
L5 + lead yalnız metodoloji/uygulanabilirlik verir (`context_source_guard` ile zorlanır).

**Deterministik açık arka uçlar (GDM science-skills):** L1/L2/L5 için açık, `uv`+Python
CLI skill'leri — ClinicalTrials.gov · PubMed · Europe PMC · OpenAlex (arama/tam-metin),
openFDA · Open Targets (bağlam). Eşleme: [`playbook/references/05_science_skills_onkoloji.md`](playbook/references/05_science_skills_onkoloji.md).

## Başlangıç

1. [`00_context/KAPSAM_BEYANI.md`](00_context/KAPSAM_BEYANI.md) — sınırları oku.
2. [`playbook/NSCLC_PLAYBOOK.md`](playbook/NSCLC_PLAYBOOK.md) — iş akışını oku.
3. [`playbook/templates/01_protocol_template.md`](playbook/templates/01_protocol_template.md)
   ile F1 protokolü başlat.
