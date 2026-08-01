---
description: Zorunlu 6-adımlı referans kapısı — DOI/tam metin/Zotero/claim/iki-kol AI-reliability kapanmadan citation yok
argument-hint: "[referans künyesi veya DOI/PMID]"
---

Aşağıdaki referans için zorunlu referans kapısını işlet: **$ARGUMENTS**

Kapı sırası (`doktoratezi/tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md`
sözleşmesi; hiçbir adım atlanamaz, sıra değişmez):

1. **Bağlam** — referans hangi bölümde hangi iddiayı destekleyecek? Tek cümleyle yaz.
2. **Bibliyografik kimlik** — DOI/PMID/PMCID/OpenAlex/YÖK ID doğrula
   (PubMed/OpenAlex/Semantic Scholar MCP'leri; Türkiye tezi için `yoktez-mcp`).
3. **Tam metin kanıtı** — Evidentia v1.7.0 sırası: PubMed/EPMC PMC-OA →
   copyright status → `pubmed-epmc` legal-OA/Unpaywall → Paper Search full text →
   Anna's Library/annas-reader (copyright-gated fallback) → Wiley/OpenAthens veya
   Zotero eki. Büyük tam metni bağlama dökme; gerekirse anamnesis `corpus_stats`
   → tek `ingest_document` → çok-sorgulu `hybrid_query`. Tam metne ulaşılamıyorsa
   `full-text-exception` olarak açıkça işaretle; istisna gerekçesi ledger'a yazılır.
4. **Zotero mutabakatı** — item key + BibTeX citation key
   (`python3 scripts/util/zotero_env_bridge.py status --json` ile köprüyü doğrula;
   anahtar değeri asla yazdırılmaz). Item key ≠ citation key; hangisini
   kullandığını belirt. Zotero'ya yazma/import açık onay ister.
5. **Claim/pasaj notu** — iddiayı destekleyen sayfa/pasaj kanıtını not et;
   claim tam metinden doğrulanmadan citation yazılmaz.
6. **Ledger kaydı + iki-kol AI-reliability** — satırı
   `doktoratezi/tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` tablosuna
   ekle (kolonlar: Citation key | DOI/PMID/ID | Zotero item key | Tam metin kanıtı |
   Kullanılan iddia | Bölüm | Nitel AI | Nicel AI | Durum | Not). Referanslı bölüm
   kapanışında iki audit birlikte koşulur: bu kolda (niteliksel/) `/nitel-dogrulama`, nicel
   kökte `doktoratezi-ai-audit` scripti.

Durum sözlüğü: `candidate → full-text-ok/full-text-exception → zotero-ok →
reliability-ok → cite-ok` (gerekirse `retired`). Kapı kapanmadan referans tez
metnine GİRMEZ; `full-text-exception` tek başına final citation değildir. Harici
MCP kullandıysan bitişte `/ai-kayit` çalıştır.
