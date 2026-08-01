---
hooks_enabled: false
lang: tr
gate_unsourced_numeric: true
gate_tr_pvalue_dot: true
---

# sci-audit proje yapılandırması — T1DM-Tez

**`hooks_enabled: false`** — sci-audit'in beş hook'u (SessionStart /
UserPromptSubmit / PreToolUse / PostToolUse / Stop) bu projede **susturulmuştur**.

**Neden:** Bu repo zaten kendi eşdeğer hook katmanını çalıştırıyor
(`.claude/hooks/` + `.claude/settings.json` `permissions.deny` — bkz. CLAUDE.md
"Claude Code katmanı"). sci-audit hook'ları aynı işlevleri (sır taraması, Bash
deny-list, çıktı incelemesi, kaynaksız-sayı Stop kapısı) tekrarlayıp çift
kontrol / çakışma yaratıyordu.

sci-audit'in **skill'leri ve MCP sunucuları** (pubmed, pubmed-epmc, openalex,
semantic-scholar) bu ayardan **etkilenmez**; denetim komutları normal çalışır.

`lang`/`gate_*` alanları hook'lar yeniden etkinleştirilirse (`hooks_enabled:
true`) devreye girer. Env ile de kapatılabilir: `SCI_AUDIT_HOOKS=off`.
