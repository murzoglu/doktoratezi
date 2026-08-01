---
description: 'Bulgular bölümünün VERİ GÖSTERİMİNİ zenginleştirir — R çıktısı ↔ yazılı bulgu mutabakatı, figür/tablo veri-tutarlılığı + estetik/Türkçe/tasarım, eksik-ama-yararlı yeni görsel, başlık/altyazı + betim netliği (kanıt DEĞERİ dokunulmaz); repo-yerel denetim + galileo-audit MCP kapısından geçirip onaya sunar (dosyaya doğrudan yazmaz)'
mode: agent
---

# /veri-gosterimi-zenginligi — Veri Gösterimi Zenginleştirme Kapısı (Copilot ikizi)

Zenginleştirilecek gösterim: **${input:hedef:chapters/04_bulgular.qmd konumu / @tbl-* / @fig-* / seçili bulgu bloğu}** —
boşsa editör seçimini kullan; o da yoksa `chapters/04_bulgular.qmd` figür/tablo envanterini çıkar.

Bu prompt, Claude komutu [.claude/commands/veri-gosterimi-zenginligi.md](../../.claude/commands/veri-gosterimi-zenginligi.md)
ve eşgüdüm playbook'u [tez-yazim/04_kalite-kontrol/bulgular-zenginlestirme-esgudum-playbook.md](../../tez-yazim/04_kalite-kontrol/bulgular-zenginlestirme-esgudum-playbook.md)
ile **aynı doktrinin** Copilot/VS Code ikizidir; ikisi **bağlayıcıdır**. `sci-audit` plugin'i
`~/.claude/plugins/marketplaces/cureonics-marketplace` altında **kuruludur** (skilleri otomatik tetiklenir;
slash komutları Copilot'ta yok, scriptleri doğrudan çalıştırılır).

## Kardeş komut sınırı (çiğnenmez)

[anlatim-zenginligi.prompt.md](anlatim-zenginligi.prompt.md) ile **aynı bölümde paralel** çalışır; sınır katmandır:

| | `/anlatim-zenginligi` | `/veri-gosterimi-zenginligi` (bu) |
|---|---|---|
| Çalıştığı bölge | **Nesir** (düzyazı + referans) | **Veri-gösterim** (figür/tablo/R-çıktı + altyazı + betim) |
| DOKUNULMAZ | Sayı/istatistik/bulgu **ve** figür/tablo | Kanıt **değeri**: sayının kendisi, yön, anlamlılık, büyüklük |
| Düzenleyebildiği | Terim izahı + bağlam + atıflı literatür | **Sunum katmanı**: etiket, renk, düzen, font, başlık/altyazı, Türkçe, betim netliği, yeni görsel |

**Ortak anayasa:** kanıt değeri mutasyonu YASAK — hiçbir sayı/yön/anlamlılık/büyüklük değişmez,
yuvarlanmaz, güçlendirilmez; kaynakta olmayan özgüllük eklenmez. Zenginleştirme = daha okunur/
tutarlı/estetik gösterim + daha anlaşılır betim + kanıtlanmış boşluğa yeni görsel — yeni *bulgu* değil.

## Kapsam

- **DOKUNULMAZ (kanıt değeri):** kanonik CSV/model artefaktındaki sayılar (`outputs/models/*`,
  `data/processed/*`, `outputs/tables/*`); yön/anlamlılık/büyüklük; hipotez kararı; `@tbl-*`/`@fig-*`/
  `[@key]` token'ları; bulgu sırası; yöntem. Bunlar kaynaktan gelir — koda/altyazıya **gömülmez**.
- **DÜZENLENEBİLİR (sunum):** figür `labs()` başlık/altyazı/eksen; tema (`apa_plot_theme`); renk/skala;
  okunabilirlik; tablo Türkçe kolon başlığı + ondalık virgül; `tbl-cap`/`fig-cap`; betim cümlesinin
  açıklığı (sayı aynen).

## Yürütme (sıra sabittir)

1. **Bağlamı sabitle — TAHMİN ETME.** Hedef ID'yi `grep -n "@tbl-<id>\|@fig-<id>" chapters/04_bulgular.qmd`
   ile ara; üretici zinciri bul (tablo → `apa_render_table` → `R/29_apa_tables.R` → `outputs/tables/<id>.csv`;
   figür → `R/28_apa_figures.R` → `scripts/R/39_export_carbon_svg_figures.R` → `docs/assets/figures/carbon/**`).
   Kanonik kilit [data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock](../../data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock).
2. **Eksen 1 — R çıktısı ↔ yazılı bulgu mutabakatı (HARD):**
   - `python3 scripts/util/csr_numeric_trace_audit.py --csr chapters/04_bulgular.qmd --out-report outputs/reports/ch04_numeric_trace_audit.md` → yüksek-risk eşsiz = **0** (K5-NUM-03).
   - `python3 scripts/util/r_generator_literal_audit.py --fail-on-find` → gömülü istatistik literali = **0** (K5-LIT-01).
   - Metin bir tablo/figür değerini yanlış aktarıyorsa **metni kaynağa hizala** — sayı asla uydurulmaz; kanonik tarafı artefakttan doğrula.
3. **Eksen 2 — figür/tablo denetimi + iyileştirme (yalnız sunum):**
   - **Veri-tutarlılığı:** `python3 scripts/util/targets_file_tracking_audit.py` (K5-TRK-01; `format="file"` izleme → stale gösterim önlenir). Aynı büyüklüğü raporlayan metin↔tablo↔figür özdeş sıra/değer.
   - **Türkçe/tasarım:** `labs`/eksen/kolon başlığı/`tbl-cap`/`fig-cap` **ondalık virgül** + terim tutarlılığı; snake_case → `apa_humanize_code`; Carbon paleti + IBM Plex Sans (`apa_plot_theme`); grup renkleri sabit (DM `#0f62fe`, Kontrol gri); renk-körü ayrılabilirliği. **Kanıt-değeri renk/etiketle yeniden anlamlandırılmaz.**
   - **Eksik-ama-yararlı yeni görsel (dikkatli):** yalnız kanonik artefaktta zaten var olan büyüklüğü görselleştir; yeni analiz/sayı üretme.
4. **Denetle — UYGULAMADAN ÖNCE.** Yukarıdaki HARD scriptlere ek Türkçe/ondalık kapısı
   `python3 scripts/util/tez_checklist_verify.py --fast` + `turkish-sci-style` skill'i (altıyazı/kolon başlığı
   Türkçesi). SOFT-block: `galileo-audit` MCP `galileo_judge` (betim cümlesi) + `galileo_coherence` (advisory).
   Herhangi HARD FAIL → düzelt-ve-tekrar.
5. **Onaya sun.** (a) diff (eski→yeni; figür kodu/altyazı/tablo sunumu), (b) mutabakat + kapı özeti
   (K5-NUM-03/LIT-01/TRK-01 + galileo), (c) yeni görsel önerisi + gerekçesi. **Açık kullanıcı onayı
   olmadan Edit/commit yok.** Kanıt değeri (sayı/yön/anlamlılık) her adımda değişmeden korunur.
