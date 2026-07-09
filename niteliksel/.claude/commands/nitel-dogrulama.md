---
description: Nitel kol doğrulama paketi — sci-audit kapısı + unittest + AI-reliability audit + hook derlemesi
allowed-tools: Bash(PYTHONDONTWRITEBYTECODE=1 python3 *), Bash(python3 *), Bash(npx promptfoo@latest *)
---

## Ön koşul — tez bölüm metni değiştiyse

Manüskript adli denetimi ve Türkçe bilimsel yazım/imla yalnız
`sci-audit@cureonics-marketplace` plugin'inde yürür; repo/veri invaryantı bu
komutun aşağıdaki local testlerinde kalır.

```text
Kapı 4: /sci-audit:check-turkish <nitel-bolum>.md --strictness certification
Kapı 5: /sci-audit:audit <nitel-bolum>.md --lang tr --strictness certification --type coreq
Rapor:  /sci-audit:audit-report --out <rapor>.md
```

Doktoratezi `tez-yazim` kuralları üst kuraldır:
`tez-yazim/04_kalite-kontrol/turkce-bilimsel-yazim-denetimi.md` ve
`tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`.

## Doğrulama çıktıları (otomatik)

### 1. Toolkit unittest paketi
!`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests 2>&1 | tail -15`

### 2. t1dm-qual-ai-audit regresyon paketi
!`PYTHONDONTWRITEBYTECODE=1 python3 plugins/t1dm-qual-ai-audit/skills/t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py 2>&1 | tail -10`

### 3. Hook derleme kontrolü (Codex + Claude ikiz ağaçları)
!`python3 -m py_compile .codex/hooks/*.py .claude/hooks/*.py .codex/tools/codex_mcp_roster_redacted.py && echo "py_compile: PASS"`

## Görev

Yukarıdaki üç doğrulama katmanının sonucunu PASS/FAIL tablosu olarak raporla.

- Herhangi bir katman FAIL ise: işi "tamam" İLAN ETME; hatayı teşhis et, düzelt,
  paketi yeniden çalıştır (`superpowers:systematic-debugging` yaklaşımı).
- Tümü PASS ise: `00_context/TALIMATNAME_TEZ_YAZIM.md` "İş Bitirme Kriterleri"
  listesine göre kalan maddeleri (dosya yolu izlenebilirliği, ham veri sınırı,
  `99_ai_use_log` güncelliği, commit yapılmamış olması) tek tek doğrula ve bildir.
- Promptfoo offline gate'i yalnız AI/policy dosyaları değiştiyse çalıştır:
  `npx promptfoo@latest eval -c reliability/evals/promptfooconfig.yaml`
