# Ek katman — GDM science-skills: Deterministik Bilimsel API Arka Uçları (NSCLC)

> Kapsam: yalnız akciğer kanseri tedavi literatürünün **sistematik derlemesi**;
> yalnız `NSCLC/` alt-ağacı. **Ham/hasta-düzeyi veri yoktur.** Ana playbook:
> [`../NSCLC_PLAYBOOK.md`](../NSCLC_PLAYBOOK.md) §1 (F2 Arama, F4 Çıkarım).

Bu belge, [`google-deepmind/science-skills`](https://github.com/google-deepmind/science-skills)
koleksiyonundaki NSCLC-alakalı skill'leri mevcut **beş-katman doktrinine** eşler.
Bu skill'ler soyut katmanları **açık, telifsiz-öncelikli, deterministik betik
(`uv` + Python CLI)** arka uçlarıyla somutlaştırır: her biri gerçek bir bilimsel
API'yi (ClinicalTrials.gov, PubMed, Europe PMC, OpenAlex, openFDA, Open Targets)
oran-limitli, tekrarlanabilir bir sarmalayıcı ardında sunar.

> **Bağlayıcı süreklilik.** Bu skill'ler **yeni bir katman eklemez**; L1/L2/L5'in
> somut arka uçlarıdır. Kanıt≠bağlam, üç-katman kapı ve uydurma-referans yasağı
> aynen geçerlidir. Skill'lerin `curl`/elle-API yasağı, oran-limiti ve
> "kaynakları listele" kuralı §0 no-fabrication şiarıyla birebir örtüşür.

---

## 0. Katman eşlemesi (hangi skill nereye)

| Skill | Katman | SR rolü | Sayı besler mi |
|-------|:------:|---------|:---:|
| `clinical_trials_database` (ClinicalTrials.gov v2) | **L1 arama** | Yayınlanmamış/devam eden faz-2/3; yayın-yanlılığı denetimi; sponsor portföyü | — (kayıt-lead) |
| `pubmed_database` (NCBI E-utils + PMC BioC) | **L1→L2** | PubMed/MEDLINE arama; PMC tam-metin; künye eşleme; imla | tam-metinden **EVET** |
| `literature_search_europepmc` (Europe PMC) | **L1→L2** | Embase kapsamı + **açık-erişim** tam metin/PDF; atıf listesi | açık-erişim tam-metinden **EVET** |
| `literature_search_openalex` (OpenAlex) | **L1** | Bibliyometrik; DOI/ID çözümleme; açık-erişim PDF; atıf sayısı | — (künye/ID-lead) |
| `literature_search_biorxiv` / `_arxiv` | **L1 lead** | Ön-baskı / gri-literatür; `preprint` etiketi zorunlu | — (kayıt-lead) |
| `openfda_database` (openFDA, 28 uç) | **L5 bağlam** | FDA onay/etiket/advers olay/geri-çağırma/kıtlık; ruhsat arka planı | **HAYIR** |
| `opentargets_database` (Open Targets GraphQL) | **L5 bağlam** | Hedef-hastalık ilişkisi, ilaç mekanizması, tractability | **HAYIR** |
| `credentials` (safe-credentials protokolü) | **çapraz** | API anahtarı `~/.env`'e güvenli yazımı; sır sızmasını önler | — |
| `uv` | **çapraz** | Bağımlılık/çalıştırma zemini (tüm skill'ler `uv run`) | — |

> **Kanıt ≠ bağlam (bağlayıcı, tekrar).** Literatür-arama skill'leri **kayıt/künye
> işaret eder**; bir etki (HR/OS/PFS/ORR/GA) çıkarım tablosuna **yalnız doğrulanmış
> tam metinden** yazılır (L2). `openfda`/`opentargets` **yalnız bağlam**tır (ruhsat,
> mekanizma); sentez metnine veya çıkarım tablosuna **sayı besleyemez** — tıpkı
> `ich`/`titck`/`eudamed` (bkz. [`04_klinik_regulatif_mcp.md`](04_klinik_regulatif_mcp.md) §0).
> Zorlama: `../scripts/context_source_guard.py` (F7 HARD; `source_tier` sütunu).

---

## 1. L1 — Arama arka uçları (kayıt toplama)

evidentia çok-veritabanlı aramasının somut, tekrarlanabilir arka uçları:

- **ClinicalTrials.gov** (`clinical_trials_database`): SR standardı — yayınlanmamış
  ve devam eden çalışmalar yayın-yanlılığı denetiminin kanıtıdır. `--count-total`
  ile hacim, `--fields` ile dar alan; NCT-ID her dahil kayda bağlanır (G-BIB).
- **PubMed/MEDLINE** (`pubmed_database`): birincil kayıt havuzu; `esearch`→`efetch`;
  ayrıca yanlış imlayı düzeltir ve ham künyeyi eşler (citation-matching → G-BIB).
- **Europe PMC** (`literature_search_europepmc`): Embase-benzeri kapsama; script
  her sorguya `OPEN_ACCESS:y` ekler — bu yüzden **kapsamlı arama için yalnız
  başına yeterli değildir**, PubMed/CT.gov ile birlikte kullanılır.
- **OpenAlex** (`literature_search_openalex`): DOI/ID çözümleme, atıf-tabanlı
  snowballing, bibliyometri. Kural: **önce `resolve`, sonra `--filter`**; isimle
  filtre yok; ID/DOI uydurma yok (§0 ile aynı).
- **Ön-baskı** (`literature_search_biorxiv`/`_arxiv`): koşullu gri-lit lead;
  socius-vigil/yok-akademik ile aynı statü — **kayıt işaret eder, sayı vermez**;
  PRISMA "diğer yöntem" (`tanimlanan_kayit_diger_yontem`) olarak kaydedilir.

**Tekrarlanabilirlik (G-REPRO).** Her skill sorgusu için **tam dize + filtre +
tarih + isabet sayısı** `02_search/<konu>_search_log.md`'e yazılır. Skill'ler
`curl`/elle-API'yi yasaklar; yalnız sarmalayıcı CLI kullanılır (oran-limiti +
yeniden-deneme sarmalayıcıda).

---

## 2. L2 — Açık-erişim tam metin (çıkarımı besler)

minerva+openathens erişim zincirine **açık-erişim, telifsiz** bir ön-katman ekler
(legal-first zinciri güçlendirir):

**Güncel erişim zinciri (F4):**
`EPMC/PMC açık-erişim (science-skills) → minerva → openathens (Tier 3) → yayıncı → annas (son çare)`

- `literature_search_europepmc` tam-metin (PMCID → XML/düz metin) ve
  `pubmed_database` PMC BioC tam-metni **açık-erişim** çalışmalar için ilk
  başvurudur; telif riski en düşük yoldur (G-COPYRIGHT).
- Çıkarılan her endpoint **tam-metin lokatörüne** (PMID/DOI/PMCID + tablo/şekil)
  bağlanır (G-RAG); doğrulanmamış değer `unverified` + `gap_log`.
- Deterministik yön kontrolü değişmeden uygulanır:
  `../scripts/extraction_direction_check.py` (`hr>0`, `ci95_lo ≤ hr ≤ ci95_hi`).

> Açık-erişimde bulunamayan tam metin için minerva/openathens'e düşülür; hiçbiri
> erişemezse alan `unverified`. Açık-erişim skill'i erişemedi diye çalışma
> **sentezden düşürülmez** — yalnız kaynak katmanı değişir.

---

## 3. L5 — Klinik/regülatif bağlam arka uçları (sayı beslemez)

`04_klinik_regulatif_mcp.md` L5'inin somut, açık arka uçları:

- **openFDA** (`openfda_database`): FDA onay tarihi, etiket (endikasyon/uyarı),
  advers-olay sinyali, geri-çağırma, kıtlık, 510(k). TR bağlamında `titck` (KÜB)
  ve `eudamed` (cihaz) ile **paralel** çalışır; uygulanabilirlik/güvenlik arka
  planı verir. **Etki-büyüklüğü kaynağı değildir.**
- **Open Targets** (`opentargets_database`): hedef-hastalık ilişkisi, ilaç
  mekanizması, tractability/safety. NSCLC'de biyobelirteç-ilaç mantığını
  (ör. KRAS G12C, EGFR, ALK) çerçeveler; **klinik etkinlik sayısı vermez** —
  bunlar yalnız L2 dahil-çalışma tam metninden gelir.

> **source_tier zorlaması.** Bu iki skill'ten gelen hiçbir değer `extraction.csv`'de
> `source_tier=evidence` satırına yazılmaz. Bağlam notu olarak `06_synthesis/`
> gerekçe metnine (`source_tier=context`) girer. `context_source_guard.py` bunu
> deterministik zorlar (F7 HARD).

---

## 4. Kimlik-bilgisi ve sır güvenliği (bağlayıcı)

- Skill'ler API anahtarını (`FDA_API_KEY`, `NCBI_API_KEY`, `OPENALEX_API_KEY`)
  **`~/.env`**'e yazar — **asla** `NSCLC/` içindeki bir dosyaya, `.mcp.json`'a veya
  commit'e değil. `credentials` skill'inin "safe-credentials protokolü" bu kuralla
  birebir örtüşür.
- Anahtarlar **opsiyoneldir**; tümü anahtarsız çalışır (yalnız oran-limiti düşer).
  Bu SR hattı için anahtar **zorunlu değildir**.
- Hiçbir anahtar/token/URL-anahtarı bu belgeye veya herhangi bir `NSCLC/` belgesine
  yazılamaz (kök AGENTS.md sır-sızması yasağı).

---

## 5. Lisans ve kapsam sınırı (bağlayıcı)

- Her skill ilk kullanımda `.licenses/<skill>_LICENSE.txt` bildirim dosyası ister.
  Kapsam-kilidi ve additive-only gereği bu dosyalar **kök çalışma alanına değil,
  `NSCLC/.licenses/`** altına yazılır; kök ağaç kirletilmez.
- Kullanılan skill çıktıda **belirtilir** ve kullanılan tüm makale URL'leri
  listelenir (skill'lerin "List Sources" kuralı = G-BIB + kaynak-tekilliği).
- Kapsam-dışı skill'ler (genomik/yapısal-biyoloji: alphafold, pdb, foldseek,
  pymol, gnomad, jaspar, encode, gtex, ...) NSCLC tedavi-SR'sinde **çağrılmaz**;
  yalnız yukarıdaki tablo geçerlidir.
- IPD-meta kapsam-dışıdır; bu skill'ler hasta-düzeyi veri getirmez, yalnız
  çalışma-düzeyi künye + açık-erişim tam metin + ruhsat/mekanizma bağlamı sağlar.

---

## 6. Kanıt/araç kapıları (bu katmana özgü ek)

- **G-SKILL-WRAP** — her skill sorgusu sarmalayıcı CLI ile mi (elle-API/`curl` yok)?
- **G-SKILL-SRC** — kullanılan skill + makale URL'leri çıktıda listelendi mi?
- **G-SKILL-TIER** — literatür-arama çıktısı kayıt-lead olarak mı işaretli
  (sayı yalnız doğrulanmış tam-metinden); openFDA/opentargets `source_tier=context` mı?
- **G-SKILL-SECRET** — anahtar `~/.env`'de mi (NSCLC belge/commit'inde değil)?
- **G-SKILL-LIC** — lisans bildirimi `NSCLC/.licenses/` altında mı?

---

## 7. Kurulum notu (opsiyonel, repo-dışı)

Skill'ler `NSCLC/` ağacına **kopyalanmaz**; harici kurulum repo-dışıdır:

```bash
# Antigravity/uyumlu ajan için (kişisel skill dizini; repo dışı)
npx skills add google-deepmind/science-skills/
```

Kurulum kök çalışma alanını kirletmemelidir. Bu SR hattı için skill'ler
**zorunlu değildir**; mevcut evidentia/minerva/L5 doktrini kendi kendine
yeterlidir. science-skills, aynı katmanların **açık, betik-tabanlı, telifsiz-öncelikli**
alternatif arka uçlarını sağlar ve tekrarlanabilirliği (deterministik CLI) artırır.
