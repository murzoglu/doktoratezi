# Yazım Öncesi Preflight Raporu

Tarih: 2026-06-30

Kapsam: `tez-yazim` resmi kılavuz mimarisi, iki-kol entegrasyon hattı,
dmnitel tool bridge, MCP/Zotero yüzeyi, Quarto/R ortamı ve AI reliability
kapıları.

## Sonuç

Tez yazımına kontrollü biçimde başlanabilir. Bloklayıcı teknik eksik
saptanmadı. Final metin üretiminde resmi kaynak sırası korunmalıdır:

1. `docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf`
2. `docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx`
3. `tez-yazim/README.md`
4. `tez-yazim/00_kaynak-kurallari/format-kontrati.md`
5. Repo içi kanıt ve testlenmiş analiz artefaktları

## Kontrol Edilen Mimari

| Alan | Durum | Kanıt |
|---|---|---|
| Resmi kılavuz dosyaları | PASS | `test -f` ile PDF, DOCX ve `tez-yazim/README.md` bulundu. |
| Yazım mimarisi | PASS | `tez-yazim/` altında 19 dosyalık kaynak-kural, mimari, şablon, bölüm hazırlık, kalite kontrol ve entegrasyon yapısı mevcut. |
| Route kararı | PASS | `./dmnitel route-tool --query "Marmara tez yazım formatı, joint display ve kaynakça kontrolü"` Marmara official thesis guide + Zotero gate seçti. |
| AI context | PASS | `./dmnitel ai-context --output 07_reports/t1dm_ai_tool_bridge.md` yeniden üretildi. |
| Cross-repo status | PASS | `./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md` yeniden üretildi. |
| Nitel entegrasyon kopyası | PASS | Nitel upstream rapor ile `niteliksel/qualitative_canonical_results_report.md` bire bir aynı. |

## Araç Yüzeyi

| Araç / kapı | Durum | Yazım süreci kararı |
|---|---|---|
| `dmnitel` local toolkit | PASS | Tez yazımında route, cross-repo status, quote/codebook/coreq kontrolleri için kullanılacak. |
| MCP roster redacted kontrol | PASS | İki repoda da tokenlar maskelenerek roster alındı; raw `codex mcp list` kullanılmayacak. |
| Evidentia MCP çekirdeği | HAZIR | Dış literatür, tam metin, citation audit, YÖK/OSF/KOL gerektiğinde açılacak. |
| Zotero Web API bridge | PASS | `.env` anahtarı yazdırılmadan yüklendi; Zotero write/import açık onay gerektirir. |
| Zotero Desktop local API | NOT RUNNING | Lokal attachment/full-text işleri için Zotero Desktop açılmadan kullanılmaz; yazımı bloke etmez. |
| Quarto | PASS | `quarto check` geçti; Quarto 1.6.43, LaTeX, R ve knitr hazır. |
| R/renv | PASS | `renv::status()` tutarlı; sorun yok. |
| AI audit skills | PASS | Nitel ve nicel skill validasyonları geçti. |

## Çalıştırılan Komutlar

| Komut | Sonuç |
|---|---|
| `./dmnitel route-tool --query "Marmara tez yazım formatı, joint display ve kaynakça kontrolü"` | PASS |
| `./dmnitel ai-context --output 07_reports/t1dm_ai_tool_bridge.md` | PASS |
| `./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md` | PASS |
| `python3 .codex/tools/codex_mcp_roster_redacted.py` | PASS, iki repoda da secret redaction korundu |
| `python3 scripts/util/zotero_env_bridge.py status --json` | PASS |
| `python3 .../zotero.py status --json` | Desktop local API kapalı |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` | PASS, 31/31 |
| `PYTHONDONTWRITEBYTECODE=1 python3 plugins/t1dm-qual-ai-audit/skills/t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py` | PASS, 55/55 |
| `PYTHONDONTWRITEBYTECODE=1 python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/test_repo_ai_reliability.py` | PASS, 142/142 |
| `python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/install_repo_ai_reliability.py --check` | PASS |
| `Rscript tests/test_reproducibility_lock.R && Rscript tests/test_final_reference_loading.R && Rscript tests/test_data_governance.R` | PASS |
| `quarto check` | PASS |
| `npx promptfoo@latest eval -c reliability/evals/promptfooconfig.yaml` | PASS, nitel 4/4 ve nicel 4/4 |
| `Rscript -e 'renv::status()'` | PASS, no issues |

## Yazımda Uyulacak Gate

1. Format veya bölüm sırası sorusunda önce `tez-yazim/00_kaynak-kurallari/`.
2. İçerik iddiasında önce repo içi kaynak ve testlenmiş aggregate artefakt.
3. Dış literatürde Evidentia D0-D6, ardından Zotero kaynakça mutabakatı.
4. Karma yorumda nitel tema ile nicel estimate ayrı kanıt türleri olarak kalır.
5. Harici MCP/plugin sonucu tez cümlesini etkilerse nitel kol AI use log'a kayıt düşülür.

## Bloklayıcı Olmayan Açık Noktalar

- Zotero Desktop local API kapalı; yalnız lokal full-text/attachment işi gelirse Zotero Desktop açılmalı.
- Bazı MCP roster satırları `Not logged in` veya `Unsupported` auth etiketi taşıyor; bu araçlar yalnız gerektiğinde ayrıca doğrulanmalı.
- Quarto render çalıştırılmadı; bu preflight `thesis.qmd` veya `chapters/` içeriğini değiştirmediği için `quarto check` ile sınırlı tutuldu.
- Nitel reliability raporundaki araştırmacı kararı gerektiren noktalar devam ediyor: beş codebook placeholder quote ID uyarısı, COREQ 16/31 kısmi durumu ve final alıntıların kaynak metinle bire bir kontrolü.
- Worktree önceki işlerden geniş ölçüde dirty/untracked durumda; bu rapor yalnız yazım mimarisi ve tool preflight yüzeyini değerlendirir.

## Hazır Başlangıç Sırası

1. `tez-yazim/03_bolum-hazirlik/01_giris-ve-amac.md`
2. `tez-yazim/03_bolum-hazirlik/02_genel-bilgiler.md`
3. `tez-yazim/03_bolum-hazirlik/03_gerec-ve-yontem.md`
4. `tez-yazim/05_entegrasyon/nitel-nicel-joint-display-plan.md`
5. İlgili `chapters/*.qmd` dosyasına kontrollü aktarım
