# MCP köprüleri ve exec-üzerinden erişim

Bu dizin, tezin denetim/literatür yığınını Model Context Protocol (MCP) stdio
köprüleri olarak barındırır. Köprüler normalde `.mcp.json` üzerinden Claude Code
istemcisine bağlanır. **Ona ajan oturumunda** bu köprüler yerleşik araç setine
enjekte edilmediğinden, aynı JSON-RPC `tools/call` sözleşmesi `exec` üzerinden
[`mcp_tool_call.py`](mcp_tool_call.py) ile konuşulur.

## Hızlı kullanım

```bash
# Araç listele
python3 scripts/mcp/mcp_tool_call.py <köprü> --list

# Araç çağır (argüman JSON)
python3 scripts/mcp/mcp_tool_call.py <köprü> <araç> '<json_args>'

# Argümanı stdin'den ver
echo '<json_args>' | python3 scripts/mcp/mcp_tool_call.py <köprü> <araç> -
```

`<köprü>` bir kısayol (`minerva`, `galileo`, `zotero`) ya da doğrudan script
yolu olabilir. `.env` otomatik yüklenir (değer basılmaz); interaktif-olmayan
çağrılarda `.bashrc` auto-load devreye girmediği için bu gereklidir.

## Köprüler ve araçları

| Kısayol | Script | Öne çıkan araçlar |
|---------|--------|-------------------|
| `minerva` | `minerva_evidence_bridge.py` | `minerva_literature_search` (D2), `minerva_literature_fulltext_by_doi` / `minerva_rominedb_get_article` (D4) |
| `galileo` | `../eval/galileo_bridge.py` | `galileo_judge`, `galileo_claim_source_match` (SOFT-block); `galileo_coherence`, `galileo_reference_prose` (advisory); `galileo_stats` |
| `zotero` | `zotero_refs_bridge.py` | `zotero_status`, `zotero_reconcile_bib`, `zotero_add_to_collection` |

Tam-metin ingest için `anamnesis_ingest.py` / `anamnesis_client.py` ayrıca
mevcuttur (D4 chunk-alıntı katmanı).

## Zenginleştirme kapısı ↔ araç eşlemesi

`/anlatim-zenginligi` ve `/veri-gosterimi-zenginligi` üç kademeli kapı kullanır.
Ona oturumunda kademeler şu exec yollarıyla karşılanır:

| Kademe | Slash-komut (Claude Code) | Ona exec karşılığı |
|--------|---------------------------|--------------------|
| **HARD** Axis G (TR/ondalık) | `/sci-audit:check-turkish` | `python3 ~/.claude/plugins/cache/cureonics-marketplace/sci-audit/<sürüm>/skills/turkish-sci-style/scripts/tr_sciaudit.py` |
| **HARD** Axis C (istatistik) | `/sci-audit:check-stats` | `.../skills/stats-forensics/scripts/stats_forensics.py` |
| **HARD** Axis A/B (citation/claim) | `/sci-audit:verify-citations` | `.../skills/claim-grounding/scripts/claim_grounding.py` + `scripts/util/bib_hygiene.py` |
| **SOFT-block** | — | `mcp_tool_call.py galileo galileo_judge` / `galileo_claim_source_match` |
| **advisory** | — | `mcp_tool_call.py galileo galileo_coherence` / `galileo_reference_prose` |

Kademe eşikleri: sci-audit (HARD) override edilemez; galileo (SOFT-block)
`.claude/galileo.local.md` eşiklerine bağlıdır; ikisi birbirinin yerine geçmez.

> **Not (sci-audit keşif yolu):** `audit_stack_healthcheck.py` sci-audit'i
> yalnız belirli konumlarda arar; bulamazsa axis-H repo-linter'a düşer. Plugin
> cache'teki (`~/.claude/plugins/cache/.../sci-audit/<sürüm>/`) HARD scriptleri
> yukarıdaki tabloda gösterildiği gibi doğrudan `python3` ile çağrılabilir ve
> tam Axis G/C/A denetimini sağlar. `<sürüm>` dizinini
> `ls ~/.claude/plugins/cache/cureonics-marketplace/sci-audit/` ile doğrulayın.

## Sağlık kontrolü

Tüm yığının erişilebilirliğini tek komutta doğrulamak için:

```bash
python3 scripts/mcp/audit_stack_healthcheck.py
```
