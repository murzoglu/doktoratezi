# L1/L2 — evidentia + minerva: SR Arama & Çıkarım Katmanı (NSCLC)

> Kapsam: yalnız akciğer kanseri tedavi literatürünün **sistematik derlemesi**;
> yalnız `NSCLC/` alt-ağacı. **Ham/hasta-düzeyi veri yoktur.** Ana playbook:
> [`../NSCLC_PLAYBOOK.md`](../NSCLC_PLAYBOOK.md) §1 (F2 Arama, F4 Çıkarım).

Bu katman, evidentia tam-yığın orkestrasyonunu bir **PRISMA 2020 sistematik arama
+ tam-metin veri çıkarımı** hattına uyarlar. Fark: SR'de arama **kapsamlı,
tekrarlanabilir ve önceden-kayıtlıdır**; "yeterince kaynak" değil, "protokoldeki
tüm kaynaklar sistematik" hedeflenir.

---

## 0. Görev ayrımı — hangi soru nereye?

| SR fazı | Katman | Örnek (NSCLC) |
|---------|--------|---------------|
| Arama dizesi + kapsam | evidentia çok-db | "1L KRAS G12C için tüm RCT'ler" |
| Aktif/tamamlanmış çalışma | ClinicalTrials.gov | Yayınlanmamış/devam eden faz-3 |
| Standart bakım bağlamı | Kılavuz (NCCN/ESMO/ASCO) | Tartışma çerçevesi |
| Tam-metin veri çıkarımı | minerva tam-metin | Her dahil çalışmanın HR/OS/PFS'i |
| Çok-belge sentez desteği | anamnesis GraphRAG | Dahil çalışmalar arası örüntü |

---

## 1. F2 — Sistematik arama (çok-veritabanı)

Her dış-kanıt sorgusunda **önce router çalışır**. SR'de aşağıdaki katmanlar
**varsayılan açıktır** (kapsam kapsamlılığı PRISMA gereğidir):

| Veritabanı / katman | Durum | SR amacı |
|---------------------|-------|----------|
| PubMed/MEDLINE, EPMC (Embase kapsamı), Semantic Scholar | **açık** | Birincil kayıt havuzu |
| **Cochrane CENTRAL** | **açık** | RCT kaydı (SR standart kaynağı) |
| **ClinicalTrials.gov** | **açık** | Yayınlanmamış/devam eden çalışma; yayın-yanlılığı denetimi |
| Kılavuz: NCCN, ESMO, ASCO | **açık** | Bağlam + snowballing tohumu |
| bioRxiv/medRxiv | koşullu | Gri literatür; `preprint` etiketi zorunlu |
| **socius-vigil** (gri-lit çok-motor) | koşullu | Konferans özeti (ASCO/ESMO/WCLC), ön-baskı, yayımlanmamış sinyal — **arama-lead** (bkz. §1.1) |
| **yok-akademik** | koşullu | TR tez/akademik kapsama (TR ağı) — arama-lead |
| Terminoloji: HGNC, RxNorm, ATC, MeSH | koşullu | Arama eşanlamlı genişletme (`terminology_map`) |
| openFDA / EMA | koşullu | Onay bağlamı |
| minerva (Roche korpus) + OpenAthens | tam metin | F4 veri çıkarımı |
| anamnesis RAG/GraphRAG | derin okuma | Dahil çalışmalar arası sentez desteği |

**Tekrarlanabilirlik (G-REPRO):** her veritabanı için **tam dize + filtre + tarih +
isabet sayısı** `02_search/<konu>_search_log.md`'e yazılır
([`../templates/02_search_strategy_template.md`](../templates/02_search_strategy_template.md)).

**Kapsam kapısı:** NSCLC-dışı katmanlar (T1DM, pediatri-psikososyal) bağlama alınmaz.

**Deterministik açık arka uçlar (GDM science-skills).** Yukarıdaki katmanların
açık, oran-limitli, betik-tabanlı (`uv`+Python CLI) somut arka uçları vardır:
ClinicalTrials.gov→`clinical_trials_database`, PubMed→`pubmed_database`,
EPMC→`literature_search_europepmc`, OpenAlex→`literature_search_openalex`;
bağlam (sayı beslemez): openFDA→`openfda_database`, Open Targets→`opentargets_database`.
Tam eşleme + kapılar: [`05_science_skills_onkoloji.md`](05_science_skills_onkoloji.md).

### 1.1 Arama-lead ≠ kanıt (bağlayıcı)

socius-vigil ve yok-akademik **arama-lead** katmanıdır: aday kayıt/çalışma işaret
eder, ama çıktısı **doğrudan kanıt veya sayı değildir** (socius-vigil bir
LLM-sentez motorudur). İşaret edilen her kayıt F3 taramasına girer; sayısı yalnız
F4'te birincil tam-metinden çıkarılır. Gri-literatür bulguları PRISMA akışında
"diğer yöntem" olarak kaydedilir (`tanimlanan_kayit_diger_yontem`). Ayrıntı:
[`04_klinik_regulatif_mcp.md`](04_klinik_regulatif_mcp.md) §5, §0.

---

## 2. F3 — Tarama desteği (screening)

- evidentia çıktısı `02_search/<konu>_records.csv` → tekilleştirme →
  `03_screening/<konu>_screening.csv`.
- **Zotero (`zotero-refs`) referans yönetimi:** toplanan künyeler bir Zotero
  koleksiyonuna alınır; tekilleştirme Zotero ile **çapraz-doğrulanır** (aynı
  çalışmanın çoklu yayını tek çalışmaya katlanır — çalışma ≠ rapor). F8'de atıf/
  bibliyografya bu koleksiyondan üretilir.
- Her dışlama **PRISMA neden koduyla** kaydedilir; **PRISMA akış sayıları**
  ([`../templates/07_prisma_flow_template.csv`](../templates/07_prisma_flow_template.csv))
  buradan türetilir ve `scripts/prisma_flow_check.py` ile aritmetik doğrulanır.
- İki-bağımsız-tarayıcı simülasyonu + anlaşmazlık notu.

---

## 3. F4 — minerva tam-metin veri çıkarımı (L2)

Dahil edilen **her** çalışmanın verisi **tam metinden** çıkarılır (özetten tahmin
değil).

1. **Tam-metin erişim zinciri (sıra bağlayıcı, legal-first):**
   EPMC/PMC (açık erişim) → `minerva_literature_fulltext_by_doi` /
   `minerva_rominedb_get_article` (Roche korpus) → **openathens (Tier 3, Wiley'den
   ÖNCE)** → yayıncı → **annas-reader** (yalnız **son çare**). Hiçbiri erişemezse
   `gap_log`'a gerekçe + `unverified` yazılır; annas varsayılan değil, istisnadır.
   Komut sarmalayıcı: `/evidentia:evidentia-fulltext`.

   **openathens 6 aracı** (kurumsal paywall kapısı, SAML; 309 lisanslı DB):
   - `oa_server_info` / `oa_list_databases` — erişilebilir kaynak envanteri.
   - `oa_resolve` — DOI/PMID → lisanslı tam-metin URL çözümü.
   - `oa_fetch_fulltext` — tek makale tam metni (çıkarım için).
   - `oa_batch_submit` / `oa_batch_result` — çok sayıda dahil çalışma için toplu
     tam-metin (F4 verimli işler). Toplu erişim önerilir: dahil listesi büyükse
     tek tek yerine batch.
   Erişilen tam metin `04_extraction/fulltext/` (git-dışı, telif); yalnız
   yapılandırılmış alanlar çıkarılır (G-COPYRIGHT).
2. **Copyright kapısı (G-COPYRIGHT):** tam metin çıkarım içindir; toptan verbatim
   çoğaltma yasaktır. Yalnız yapılandırılmış alanlar alınır.
3. **Çıkarım tablosu** → `04_extraction/<konu>_extraction.csv`
   ([`../templates/04_extraction_template.csv`](../templates/04_extraction_template.csv)):
   çalışma kimliği, tasarım, popülasyon (histoloji/evre/belirteç/hat), müdahale/
   komparatör, endpoint (OS/PFS/ORR + HR + %95 GA + p + olay/örneklem), takip,
   fon/COI, **kaynak lokatörü (PMID/DOI + tablo/şekil)**.
4. **Yön kontrolü:** `hr` ve GA sınırları `scripts/extraction_direction_check.py`
   ile F4'te doğrulanır; F6/F7'de yeniden sınanır (koruyucu HR<1; ci95_lo ≤ hr ≤
   ci95_hi). Bu tablo, ana playbook §4 "kaynak-tekilliği" için tekil-çalışma sayı
   kaynağıdır.
5. Tam metin dosyaları `04_extraction/fulltext/` (git-dışı, telif).

---

## 4. anamnesis RAG — retrieve-don't-dump (sentez desteği)

1. `corpus_stats` kontrol; `docs == 0` ise önce ingest, "kanıt yok" deme.
2. SR sorusunu alt-yönlere böl: popülasyon/belirteç, müdahale, komparatör,
   endpoint, alt-grup, coğrafya/etnisite.
3. Dahil çalışmaların tam metni ingest → `hybrid_query`; ham metin bağlama dökülmez.
4. Bayat belge → `forget_document(doc_id)`.

---

## 5. Kanonik artefaktlar (SR)

| Artefakt | Faz | Konum |
|----------|-----|-------|
| `search_log` + `records.csv` | F2 | `02_search/` |
| `screening.csv` + `prisma_counts.csv` | F3 | `03_screening/` |
| `extraction.csv` (+ `fulltext/` git-dışı) | F4 | `04_extraction/` |
| `terminology_map` | F2 | `02_search/` |
| Zotero koleksiyonu (künye + atıf) | F3/F8 | `zotero-refs` (repo-dışı) |
| `evidence_index` (RAG) | F4 | anamnesis (repo-dışı) |

---

## 6. Kanıt/arama zekası kapıları — SR (G-*)

- **G-COVERAGE** — çok-veritabanı (PubMed+Embase+Cochrane+ClinicalTrials+kılavuz)
  kapsandı mı; koşullu katman tetiklenmediyse `router_decision`, erişilemediyse
  gerekçeli `gap_log`?
- **G-REPRO** — arama tam tekrarlanabilir mi (dize+filtre+tarih)?
- **G-PRISMA-FLOW** — akış sayıları tutarlı; dışlama nedenleri kodlu mu?
- **G-RAG** — her çıkarılmış endpoint tam-metin lokatörüne bağlı mı?
- **G-XVAL** — kritik havuzlanmış etki ≥2 kaynak/otoriter kılavuzla tutarlı mı?
- **G-BIB** — her kaynak PMID/DOI/NCT/OpenAlex-ID ile izlenebilir mi?
- **G-NSCLC** — histoloji/evre/belirteç/hat/komparatör/endpoint + transfer sınırı açık mı?
- **G-COPYRIGHT** — tam metin hedefli; toptan verbatim yok.
- **G-HARKING** — alt-grup/sentez kararı protokolde önceden mi (post-hoc işaretli)?

---

## 7. Uydurma-referans yasağı (no-fabrication)

- Var olmayan NCT/PMID/DOI **asla** üretilmez; çözülemeyen künye `unverified`.
- Bir çalışmanın endpoint'i tam metinde doğrulanmadan çıkarım tablosuna yazılmaz.
- Geri-çekilmiş çalışmalar (Retraction Watch / PubMed) axis A'da işaretlenir;
  sentezden düşülür veya açıkça notlanır.
- Referans Bütünlük Şiarı (RBŞ): kaynak kendi kapsam+koşuluyla aktarılır
  (etki hangi alt-grupta/takipte geçerli); cherry-pick/düzleştirme/abartma yok.
