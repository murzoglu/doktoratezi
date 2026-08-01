---
description: Zorunlu 7-adımlı referans kapısı — DOI/tam metin/Zotero/claim/iki-kol AI-reliability kapanmadan citation yok
argument-hint: "[referans künyesi veya DOI/PMID]"
---

Aşağıdaki referans için zorunlu referans kapısını işlet: **$ARGUMENTS**

Ledger: `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` — kapı
sırası sabittir, hiçbir adım atlanamaz:

0. **Otomatik ön-mutabakat** — `python3 scripts/util/bib_hygiene.py all` koş;
   HARD (atıflı-tanımsız) varsa kapı açılmaz; SOFT (alan/DOI/dup) ledger'a not düşülür.
   Ek (advisory, embedding CANLI): `python3 scripts/util/thesis_semantic.py bib-dup` —
   semantik yakın-duplikat (Jaccard'ın kaçırdığı çeviri/parafraz/transliterasyon dup);
   embedding yoksa `bib_hygiene` Jaccard'a degrade eder.

1. **Bağlam** — referans hangi bölümde hangi iddiayı destekleyecek? Tek cümle.
2. **Bibliyografik kimlik** — DOI/PMID/PMCID/OpenAlex/YÖK ID doğrula
   (PubMed/OpenAlex/Semantic Scholar/Paper Search MCP'leri; TR tezi için `yoktez-mcp`).
3. **Tam metin kanıtı** — kaskad: PMC/OA (`pubmed_fetch_fulltext`) → OpenAthens
   (lisanslı) → **Minerva (Roche korpus: `minerva_literature_fulltext_by_doi` /
   `minerva_rominedb_get_article`, annas ÖNCESİ)** → annas-reader (son çare) →
   repository → Zotero eki. Üç tam-metin kaynağı (OpenAthens/Minerva/annas)
   deterministik yardımcıyla birlikte denenebilir:
   `python3 scripts/mcp/fulltext_cascade.py --doi <DOI> --title "..."`
   (varsayılan tier: `pubmed,openathens,minerva,annas`). Minerva tam metni
   anamnesis'e ingest edilir, teze verbatim kopyalanmaz (telif; KVKK: yalnız
   DOI/başlık gönderilir). OA/lisanslı/Minerva yolları tüketilmeden
   `full-text-exception` yazılamaz ve istisna gerekçesi ledger'a girer.
4. **Zotero mutabakatı** — item key + BibTeX citation key (ikisi FARKLIDIR;
   hangisi kullanıldı belirt) + `references/references.bib` uyumu. Zotero'ya
   yazma/import açık onay ister; API anahtarı asla yazdırılmaz.
5. **Claim/pasaj notu** — iddiayı destekleyen sayfa/pasaj kanıtı. İsteğe bağlı
   `galileo_claim_source_match` (claim↔kaynak semantik groundedness skoru; SOFT/advisory)
   ile iddia-kaynak temellendirmesi teyit edilebilir.
6. **Ledger satırı + iki-kol AI-reliability** — kolonlar: `Citation key |
   DOI/PMID/ID | Zotero item key | Tam metin kanıtı | Kullanılan iddia | Bölüm |
   Nitel AI | Nicel AI | Durum | Not`. Referanslı bölüm kapanışında
   `/tez-dogrulama` (bu repo) + `t1dm-qual-ai-audit` (nitel kol) birlikte koşulur.

Durum sözlüğü: `candidate → full-text-ok/full-text-exception → zotero-ok →
reliability-ok → cite-ok` (gerekirse `retired`). Kapı kapanmadan referans tez
metnine GİRMEZ. Harici MCP tez içeriğini etkilediyse nitel kolda kayıt düş:
`cd niteliksel && ./dmnitel log-ai-use … --external-api-used yes`.

**Referans Bütünlük Şiarı (RBŞ — konstitüsyonel; `tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md` §4.1):** Bir referanstan zenginleştirme/analiz yaparken makalenin **bir parçasını değil tamamını geniş bağlamda semantik kavra**, bu bağlamı **rafine ederek** revize et; **hem kaynağın hem tez metninin somut bilimsel iddialarını çarpıtma** (cherry-pick / düzleştirme / abartma yok; kaynak kendi kapsam+koşuluyla aktarılır).
