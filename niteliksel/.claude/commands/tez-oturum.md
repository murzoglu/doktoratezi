---
description: Tez yazım oturumu ritüeli — bridge bağlamını ve tool rotasını sabitler (talimatname zorunlu adımı)
argument-hint: "[oturumun ana sorusu / görevi]"
allowed-tools: Bash(./dmnitel *), Bash(q=*), Bash(head *), Read
---

## Otomatik toplanan bağlam

### AI tool bridge (`./dmnitel ai-context`)
!`./dmnitel ai-context`

### Rota önerisi (`./dmnitel route-tool`)
!`q="$ARGUMENTS"; ./dmnitel route-tool --query "${q:-tez yazım oturumu genel rota}"`

### Canlı durum (TRACKER başı)
!`head -60 00_context/TRACKER.md`

## Görev

Yukarıdaki bağlamla bu tez yazım oturumunu aç. `00_context/TALIMATNAME_TEZ_YAZIM.md`
bu oturumda bağlayıcıdır. Sırasıyla:

1. Kullanıcının sorusunu (`$ARGUMENTS`) üç koldan birine yerleştir ve açıkça söyle:
   **yerel nitel** (dmnitel/RTA/COREQ/alıntı), **dış kanıt** (Evidentia v1.7.0
   `medical-research` v8.5 native-first hattı, no-web-tier, Anna's/full-text kapısı)
   veya **nicel/karma** (paired `doktoratezi` + `t1dm-tez-rehberi`).
2. Tez yazımı/format/bölüm işiyse ana operasyon merkezinin
   `/workspaces/T1DM-Tez/tez-yazim` olduğunu doğrula; oradaki
   `README.md` + `06_kritik-kaynaklar/README.md` + resmi `docs/tez-kilavuz` üst kuraldır.
3. Ham veri sınırını hatırla: `01_raw_data/`, `02_processed/transcripts/`,
   `01_deidentified/`, `00_raw_locked/` açılmaz; alıntı işi `./dmnitel check-quotes` ile yapılır.
4. Route çıktısına göre ilk somut adımı öner ve uygula. Evidentia kullanırsan
   `.claude/evidentia.local.md`, `CONNECTORS.md` ve canonical-cache sözleşmesini
   esas al; ham veri connector'a gitmez. Harici MCP kullanırsan oturum sonunda
   `/ai-kayit` ile günlüğe geçir.
5. Denetim/sci-audit sinyali varsa `sci-audit@cureonics-marketplace` plugin'ini
   doktoratezi `tez-yazim` kurallarıyla kullan: Kapı 4
   `/sci-audit:check-turkish`, Kapı 5 `/sci-audit:audit` + `/sci-audit:audit-report`.
   KVKK/ham veri/quote-parity invaryantları sci-audit'e devredilmez; `dmnitel`
   ve iki-kol ai-audit plugin'inde kalır.
