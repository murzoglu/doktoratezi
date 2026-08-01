# NSCLC SR — Deterministik HARD-gate Scriptleri

Bu dizin, sistematik derleme (SR) hattının **deterministik teslim-engeli
kapısını** (HARD) uygular. Doktrin gereği **HARD kapı asla LLM-judge'dan gelmez**;
bu scriptler saf kural-tabanlıdır (playbook F7 Adım 0; sci-audit referansı §0/§3).
Yalnızca Python standart kütüphanesi kullanılır — ek bağımlılık yoktur.

## Denetçiler

| Script | Kaide | Girdi |
|--------|-------|-------|
| `prisma_flow_check.py` | PRISMA akış aritmetiği (identified→…→included) | `03_screening/*_prisma_counts.csv` |
| `extraction_direction_check.py` | Yön-mantığı: `hr>0`, `ci95_lo ≤ hr ≤ ci95_hi`, I²/ORR/p aralık | `04_extraction/*_extraction.csv`, `06_synthesis/*_meta.csv` |
| `context_source_guard.py` | Kanıt≠bağlam: sayısal etki yalnız `source_tier=evidence`'dan | `04_extraction/*_extraction.csv`, `06_synthesis/*_meta.csv` |
| `source_singularity_check.py` | Metin sayıları ↔ artefakt (gömülü literal yasağı) | manüskript + kaynak CSV'ler |
| `turkish_p_check.py` | Türkçe ondalık-virgül imlası (`p = 0.03` blocker) | manüskript |
| `run_hard_gate.py` | Beşini tek kapıda birleştiren orkestratör | tümü |

## Kullanım

```bash
cd NSCLC

# Tek tek
python3 scripts/prisma_flow_check.py 03_screening/<konu>_prisma_counts.csv
python3 scripts/extraction_direction_check.py 04_extraction/<konu>_extraction.csv
python3 scripts/context_source_guard.py 04_extraction/<konu>_extraction.csv
python3 scripts/turkish_p_check.py 07_manuscript/<konu>.md --lang tr
python3 scripts/source_singularity_check.py 07_manuscript/<konu>.md \
    --sources 04_extraction/<konu>_extraction.csv 06_synthesis/<konu>_meta.csv

# Orkestratör (F7 Adım 0) — LLM eksenlerinden ÖNCE
python3 scripts/run_hard_gate.py 07_manuscript/<konu>.md \
    --extraction 04_extraction/<konu>_extraction.csv \
    --meta       06_synthesis/<konu>_meta.csv \
    --prisma     03_screening/<konu>_prisma_counts.csv \
    --lang tr
```

Her script: **blocker varsa exit-kod 1**, temizse 0. Girdi verilmeyen kontrol
orkestratörde SKIP olur (eksik ≠ hata; no-fabrication).

## Konvansiyon

- **CSV ayırıcı `;`**: Türkçe ondalık virgül (`0,72`) veri hücrelerinde kullanıldığı
  için CSV ayırıcı olarak noktalı-virgül önerilir; `_common.py` ayırıcıyı otomatik
  saptar.
- **`unverified` / boş / `NR`**: sayı olarak ayrıştırılmaz, atlanır (çözülemeyen
  kaynak uydurulmaz).
- **`source_tier`**: `04_extraction`/`06_synthesis` CSV'lerinde zorunlu sütun;
  sayısal etki (`hr`/`ci95`/`orr`/`estimate`) taşıyan her satır `evidence` olmalı.
  `context`/`lead` satırları sayı taşıyamaz (kanıt≠bağlam; referans 04 §0).

## Test

```bash
cd NSCLC && python3 scripts/test_hard_gate.py   # 21 test, stdlib unittest
```
