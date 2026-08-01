---
description: 'Zorunlu 7-adımlı referans kapısı — DOI/tam metin/Zotero/claim/iki-kol AI-reliability kapanmadan citation yok'
mode: agent
---

Aşağıdaki referans için zorunlu referans kapısını işlet: **${input:referans:referans künyesi veya DOI/PMID}**

Ledger: `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` — kapı
sırası sabittir, hiçbir adım atlanamaz:

0. **Otomatik ön-mutabakat** — `python3 scripts/util/bib_hygiene.py all` koş;
   HARD (atıflı-tanımsız) varsa kapı açılmaz; SOFT (alan/DOI/dup) ledger'a not düşülür.

1. **Bağlam** — referans hangi bölümde hangi iddiayı destekleyecek? Tek cümle.
2. **Bibliyografik kimlik** — DOI/PMID/PMCID/OpenAlex/YÖK ID doğrula
   (PubMed/OpenAlex/Semantic Scholar/Paper Search MCP'leri; TR tezi için `yoktez-mcp`).
3. **Tam metin kanıtı** — kaskad: OpenAthens → PMC/OA (`pubmed_fetch_fulltext`,
   Paper Search `download_*`) → repository → Zotero eki. Anna's Library kapısı bu
   harness'ta bağlı değilse Codex oturumunda kapatılır; OA yolları tüketilmeden
   `full-text-exception` yazılamaz ve istisna gerekçesi ledger'a girer.
4. **Zotero mutabakatı** — item key + BibTeX citation key (ikisi FARKLIDIR;
   hangisi kullanıldı belirt) + `references/references.bib` uyumu. Zotero'ya
   yazma/import açık onay ister; API anahtarı asla yazdırılmaz.
5. **Claim/pasaj notu** — iddiayı destekleyen sayfa/pasaj kanıtı.
6. **Ledger satırı + iki-kol AI-reliability** — kolonlar: `Citation key |
   DOI/PMID/ID | Zotero item key | Tam metin kanıtı | Kullanılan iddia | Bölüm |
   Nitel AI | Nicel AI | Durum | Not`. Referanslı bölüm kapanışında
   `/tez-dogrulama` (bu repo) + `t1dm-qual-ai-audit` (nitel kol) birlikte koşulur.

Durum sözlüğü: `candidate → full-text-ok/full-text-exception → zotero-ok →
reliability-ok → cite-ok` (gerekirse `retired`). Kapı kapanmadan referans tez
metnine GİRMEZ. Harici MCP tez içeriğini etkilediyse nitel kolda kayıt düş:
`cd niteliksel && ./dmnitel log-ai-use … --external-api-used yes`.
