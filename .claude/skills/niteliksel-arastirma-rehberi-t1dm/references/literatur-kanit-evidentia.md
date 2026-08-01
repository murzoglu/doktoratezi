# Niteliksel Metodoloji Literatürü — evidentia Köprüsü

> **Amaç:** Niteliksel kolun **dış metodoloji ve konumlandırma literatürünü** (RTA epistemolojisi,
> COREQ/SRQR/JARS, bilgi gücü, multi-informant discrepancy, trustworthiness, pediatrik kronik
> hastalık aile yükü) `evidentia` ile getirmek. **İç niteliksel analiz** (bu kolun 21 görüşmesi,
> kodlama, tema) bu skill'de kalır; **dış kanıt/sentez** evidentia'ya delege edilir.

Bu dosya `niteliksel-arastirma-rehberi-t1dm` ↔ `evidentia` köprü protokolüdür. Kalıp,
`t1dm-tez-rehberi/references/literatur-kanit-evidentia.md` ile aynıdır; farkı **niteliksel
metodoloji odağı** ve `niteliksel-enrichment-layer.md`'nin tetiklenmesidir.

## 0. Görev Ayrımı — Hangi Soru Nereye?

| Soru tipi | Nereye | Neden |
|---|---|---|
| "Bizim 21 görüşmede kardeş yükü nasıl kodlandı?" | **bu skill** (iç analiz) | Kendi verimiz |
| "RTA'da doygunluk mu bilgi gücü mü — güncel doktrin?" | **evidentia** → `gecerlik-ve-degerlendirme.md` güncellenir | Dış metodoloji |
| "T1DM kardeşlerinde görünmez yük literatürde nasıl?" | **evidentia** (narratif derin-lit) | Dış konumlandırma |
| "Bu COREQ maddesi bizde kapalı mı?" | **bu skill** → `raporlama-coreq-jars.md` | İç raporlama |
| "Braun & Clarke 2022 künyesi doğru mu / DOI?" | **evidentia** (hedefli lookup) | Citation audit |

**Tek cümle kural:** *Kendi 21 görüşmemizden çıkan her şey burada; dünyadan gelen metodoloji/
konumlandırma kanıtı evidentia'da.* İkisi bir paragrafta buluşur (ör. "Bizim triadik ayrışma
bulgumuz [iç], multi-informant discrepancy literatürü [evidentia] ile uyumludur").

## 1. Varsayılan Mod — Narratif Derin-Lit (SR değil)

`.claude/evidentia.local.md` gereği repo varsayılanı **narratif derin-lit**; PRISMA akış/RoB/GRADE
yalnız açık "sistematik/kapsam derleme" talebinde. Niteliksel metodoloji taraması için de
narratif-mod esastır.

## 2. Derinlik Kaskadı (D0-D6) — niteliksel odak
- **D0** kapsam ayrıştırma: metodoloji mi (RTA/COREQ/bilgi gücü) yoksa konumlandırma mı (T1DM aile
  yükü) — `niteliksel-enrichment-layer.md` tetikleyicileri.
- **D1** geniş tarama: PubMed/EPMC, OpenAlex, Semantic Scholar; **YÖK Akademik / YÖK Tez** Türkçe
  niteliksel tez katmanı için değerli.
- **D2** semantik genişletme + **`minerva_literature_search`** (bağlıysa). **⚠️ ZORUNLU:**
  niteliksel iş çoğunlukla Türkçe → **Türkçe sorguda `mode:semantic`** (hibrit DEĞİL; BM25
  bileşeni "anne"/"yas"/"kan" gibi TR sözcükleri İngilizce token'la karıştırır). İngilizce
  sorguda `hybrid` serbest. Kanonik gerekçe: `t1dm-tez-rehberi/.../literatur-kanit-evidentia.md` §1.2.
- **D3** eleme: TA-ailesi + paradigma + transfer edilebilirlik (bizim triadik RTA bağlamımıza).
- **D4** tam metin: EPMC/PMC → copyright gate → **minerva `..._fulltext_by_doi`** → openathens →
  annas-reader → anamnesis ingest/hybrid_query.
- **D5** çapraz-doğrulama: çelişki/terminoloji/transfer riski.
- **D6** temiz-kopya: `[@key]` + `references.bib` + ilgili reference/`.qmd`.

## 3. KVKK (sert)
Connector'lara/RAG'e **yalnız literatür arama terimi** gider. Ham transkript, katılımcı/aile satırı,
`quote_id` içeriği, demografik/kimlikleyici veri **asla** gönderilmez. Bu, evidentia'nın kendi KVKK
kuralıyla (`.claude/evidentia.local.md`) örtüşür.

## 4. Uydurma Referans Yasağı
Çözülemeyen kaynak `gap` olarak yazılır; **asla uydurma künye/DOI üretilmez** (sci-audit axis A ayrı
denetler). Her getirilen referans DOI/PMID ile doğrulanır, `references.bib`'e semantik key ile girer,
Zotero 9ZFDHMZA koleksiyonuyla mutabık kalır (bkz. Zotero tek-kaynak akışı).

## 5. Tez Artefaktı Besleme
| İhtiyaç | evidentia çıktısı → artefakt |
|---|---|
| Metodoloji doktrini güncelleme | `gecerlik-ve-degerlendirme.md` / `rta-ve-analiz.md` |
| Konumlandırma (Giriş/Tartışma) | kanonik `.qmd` §Tartışma + `references.bib` |
| Citation audit | `references.bib` + Zotero 9ZFDHMZA |

## Çapraz referanslar
- Enrichment katmanı → `niteliksel-enrichment-layer.md`
- Denetim → `manuskript-denetimi-sciaudit.md`
- Nicel köprü kalıbı → `t1dm-tez-rehberi/references/literatur-kanit-evidentia.md`
