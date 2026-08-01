---
description: 'Nicel repo doğrulama paketi — veri yönetişimi + AI-reliability + hook derlemesi (bölüm kapanış kapısı)'
mode: agent
---

## Hızlı doğrulamalar (otomatik)

Şu komutları terminalde çalıştır ve çıktılarını değerlendir:

```bash
# doktoratezi-ai-audit regresyon paketi
PYTHONDONTWRITEBYTECODE=1 python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/test_repo_ai_reliability.py 2>&1 | tail -8

# Hook derleme + Claude hook sözleşme testleri
python3 -m py_compile .codex/hooks/*.py .claude/hooks/*.py && PYTHONDONTWRITEBYTECODE=1 python3 tests/test_claude_hooks.py 2>&1 | tail -5
```

## Görev

1. Yukarıdaki hızlı katmanların sonucunu PASS/FAIL olarak raporla.
2. Veri yönetişimi R testlerini çalıştır ve sonuçları ekle (stopifnot tabanlı;
   sessiz bitiş = PASS):

```bash
Rscript tests/test_reproducibility_lock.R
Rscript tests/test_final_reference_loading.R
Rscript tests/test_data_governance.R
```

3. Bölüm/render işi kapanıyorsa `quarto render` exit 0 kanıtını ekle.
4. Herhangi bir katman FAIL ise işi "tamam" İLAN ETME; teşhis et, düzelt,
   yeniden koş. Tümü PASS ise talimatnamedeki iş bitirme kriterlerini
   (dosya-yolu izlenebilirliği, veri sınırı, ledger güncelliği, commit
   yapılmamış olması) tek tek doğrula ve bildir.
5. Referanslı bölüm kapanışında nitel taraftaki çift kapıyı hatırlat:
   `cd niteliksel && PYTHONDONTWRITEBYTECODE=1 python3 plugins/t1dm-qual-ai-audit/skills/t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py`
