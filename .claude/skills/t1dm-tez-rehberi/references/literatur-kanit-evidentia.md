# Literatür Kanıtı ve Sentez — evidentia Entegrasyonu

> **Amaç:** T1DM tezinin **dış literatür kanıtı** ihtiyacını (Giriş taraması, Tartışma
> konumlandırması, benchmark doğrulama, Bayesian prior türetimi, psikometrik referans,
> epidemiyoloji, `references.bib` doğrulama) `evidentia` plug-in'inin yapısal-akademik kanıt
> motoruyla karşılamak. Tezin **iç-veri analizi** (482 satır, H1–H5) bu skill'de kalır; **dış
> kanıt getirme/sentez** `evidentia`'ya delege edilir. İki katman birbirini besler ama
> karışmaz.

Bu dosya, `t1dm-tez-rehberi` (iç-veri/yazım) ile `evidentia` flagship'i `medical-research`
v8.5.0 / plugin v1.7.0 (dış-kanıt/sentez) arasındaki **köprü protokolüdür**. Bir literatür-kanıt ihtiyacı
doğduğunda **önce bu dosyayı oku**, sonra doğru evidentia giriş noktasını seç.

---

## 0. Görev Ayrımı — Hangi Soru Nereye?

| Soru tipi | Nereye | Neden |
|-----------|--------|-------|
| "Verimizde EMBU-C sıcaklık DM↔kontrol farkı?" | **t1dm-tez-rehberi** (iç analiz) | Kendi 482-satır verisi; `targets` hedefi |
| "Alanyazında T1DM çocuklarında ebeveyn aşırı korumacılık ne yönde?" | **evidentia** (`/evidentia`) | Dış literatür sentezi |
| "Pinquart 2013 benchmark değeri hâlâ geçerli mi, güncel meta-analiz var mı?" | **evidentia** → t1dm benchmark dosyası güncellenir | Dış kanıt → iç referans |
| "H4 SEM fit indeksimiz iyi mi?" | **t1dm-tez-rehberi** | İç model |
| "Giriş'e maternal depresyon × ebeveynlik literatürü" | **evidentia** (`evidence-synthesizer` ağır koşum) | Çok-kaynaklı tarama |
| "Bu referans (`references.bib`) gerçek mi, künyesi doğru mu?" | **evidentia** (hedefli lookup) | Citation audit |

**Tek cümle kural:** *Kendi verimizden çıkan her şey burada; dünyadan gelen her şey evidentia'da.*
İki katman bir paragrafta buluşur (ör. Tartışma: "Bizim ICC = .14 bulgumuz [iç], Pinquart 2013
r ≈ .19 [evidentia] ile uyumludur").

### 0.1 Yüzey Eşlemesi — Claude Code vs Codex

| Çalışma yüzeyi | evidentia kullanımı | Not |
|----------------|---------------------|-----|
| Claude Code | `/evidentia:*` slash-command'leri + `medical-research` skill | Plugin-native giriş. |
| Codex | `evidentia-skills` MCP'deki `medical-research` talimatı + doğrudan MCP'ler | Slash-command bekleme; tool-first çalış. |

Codex preflight:
1. `codex mcp list` içinde en az `evidentia-skills`, `pubmed-epmc`, `openalex`,
   `semantic-scholar`, `yoktez-mcp`, `anamnesis`, `evidentia-kb`, `annas-reader`, `openfda`,
   `mevzuat`, `pophive` ve `med-terminologies` görünmeli.
2. Gated connector'lar için ortam değişkenleri eksiksiz olmalı: `ANAMNESIS_MCP_API_KEY`,
   `EVIDENTIA_KB_MCP_API_KEY`, `ANNAS_MCP_API_KEY`; gerekiyorsa `OPENFDA_MCP_API_KEY`.
3. `.claude/evidentia.local.md` okunur ve bu dosyadaki kapsam kapısı uygulanır.
4. Hasta/aile PII, ham satır verisi, transkript veya kimlikleyici connector'a/RAG'e gönderilmez.

Codex'te `academic-archival-distiller` yoksa YÖK Tez için doğrudan `yoktez-mcp` akışı kullan:
`search_yok_tez_detailed` → `get_yok_tez_thesis_details` → gerekirse
`get_yok_tez_document_markdown`. Anabilim dalı daraltması gerektiğinde önce
`list_yok_tez_anabilim_dali`, sonra `search_yok_tez_by_anabilim_dali`.

### 0.2 Ana Gate Kuralı — T1DM Önce, Evidentia Sonra

Bu repoda **ana gate her zaman `t1dm-tez-rehberi`dir**. evidentia bir üst-akıl değil,
T1DM gate'in çağırdığı **dış-kanıt ve tam-metin altyapısıdır**. Bu nedenle her dış-literatür
koşumu şu sırayla yürür:

1. **T1DM gate:** hipotez/SAP kısmı, hedef artefakt, OSF durumu, PII sınırı, psikososyal kapsam.
2. **Kaskad derinleştirme:** ciddi literatür sorularında D0→D6 hattını sırayla çalıştır (§0.3).
3. **Connector koşumu:** kaskadın gerektirdiği tüm akademik, semantik ve tam-metin araçlarını çağır;
   ham çıktı dökme, ama kanıt matrisinde ayrıntıyı koru.
4. **Üst-akıl semantik değerlendirme:** kanıtları ölçüm uyumu, popülasyon transferi, yöntem kalitesi,
   çelişki ve tez artefaktı açısından tart.
5. **T1DM geri-alım:** kanıtı tez dili, APA 7, HARKing ve tedbir denetiminden geçir.
6. **Artefakta işleme:** bulguyu `chapters/*.qmd`, `references.bib` veya ilgili reference dosyasına bağla.

Evidentia'nın bağlam yönetimi burada şu şekilde uygulanır:
- **Aktif bağlam:** token ekonomisi için değil, doğruluk için küratörlenir. Yapay kaynak/claim üst
  sınırı koyma; karar-kritik tüm kaynak kimlikleri, sayısal sonuçlar, çelişkiler ve dışlanan önemli
  adaylar aktif kanıt matrisinde tutulur.
- **Karalama defteri:** arama varyantları, dışlanan kaynaklar, geçici tool çıktıları; final yanıta
  ham olarak taşınmaz; ancak semantik değerlendirmeyi etkileyen her seçim `retrieval_summary` veya
  `gap_log` içinde iz bırakır.
- **Kalıcı kayıt:** doğrulanmış kaynak kimlikleri, tez artefaktı kararı, sapma/gap notu, tam-metin
  lokatörü ve çıkarılan sayısal endpoint'lerdir.
  Ham transkript, hasta/aile satırı, tam metin kopyası veya uzun alıntı kalıcılaştırılmaz.

### 0.3 Derinlik Kaskadı — Maksimum Doğruluk ve Ayrıntı

Ciddi literatür görevi için varsayılan rota **kısa yoldan çıkış değil, kanıt doygunluğuna kadar
kaskad derinleştirme**dir. Yalnız açıkça mekanik işler (tek DOI doğrulama gibi) D0-D1'de kalabilir.

| Aşama | Amaç | Araç kapsamı | Çıkış |
|-------|------|--------------|-------|
| **D0 Preflight + kapsam ayrıştırma** | Roster, auth, PICO/PECO, ölçüm, yöntem, coğrafya, OSF/HARKing | `evidentia-skills:start`, `medical-research` Adım 0, `.claude/evidentia.local.md` | coverage_set, preflight durumu, kapsam kararı |
| **D1 Bibliyografik geniş tarama** | Konunun yayın evrenini yakala | PubMed/EPMC, Paper Search, ClinicalTrials, bioRxiv/medRxiv, PsyArXiv/OSF, OpenAlex, Semantic Scholar, YÖK Tez | `evidence_corpus`, aday kaynak havuzu, dedupe ID'ler |
| **D2 Semantik genişletme + KB booster** | Terim, citation graph, KB ve benzer çalışma boşluklarını kapat | OpenAlex concepts/citations, S2 graph, MeSH, evidentia-kb `kb_search`, anamnesis gerekirse | ek kaynaklar, semantic_expansion_steps |
| **D3 Eleme, rerank, AFF/TR matriksi** | En güçlü, ilgili ve transfer edilebilir kaynakları seç | çalışma tipi, örneklem, ölçüm, yaş, T1DM uyumu, TR bağlamı, EPMC AFF country loop | kanıt matrisi, dışlanan önemli adaylar |
| **D4 Tam-metin + RAG/GraphRAG** | Abstract'ın vermediği ayrıntıyı al | EPMC/PMC → copyright gate → pubmed-epmc legal OA → Paper Search → `annas-reader` → anamnesis ingest/hybrid_query | `evidence_index`, sayısal endpoint, tablo/lokatör |
| **D5 Çapraz-doğrulama + Extended Tier-K** | Çelişki, terminoloji, kodlama ve transfer riskini çöz | med-terminologies, nih-clinicaltables, nlm-rxnorm, iuphar-gtopdb, openfda/ICD-11, PopHIVE US-only | claim-level confidence, terminology_map, conflict log |
| **D6 Temiz-kopya + tez entegrasyonu** | Kanıtı tez artefaktına çevir | APA 7, `references.bib`, ilgili `.qmd`/reference, OPS/VIZ/sidecar disiplini | yazılabilir paragraf, BibTeX, gap/sapma kaydı |

Derinlik kuralı: amaç token tasarrufu değil **kanıt doygunluğu ve semantik güven**dir. D1'de bulunan
az sayıda iyi kaynakla yetinme; D2 citation/semantic genişletmeyi, D3 metodolojik eleme ve D5
çapraz-doğrulamayı özellikle benchmark, Giriş/Tartışma ve psikometri sorularında varsayılan kabul et.
Tam metin D4, "son çare" değil; kritik ayrıntı gerekiyorsa erken kullanılır. Her durma veya
yükseltme kararı `evidence_packet.depth_decision` içinde gerekçelenir.

### 0.4 Kaskad Literatür Sorgulama — Retrieve, Expand, Adjudicate

1. **Sorguyu ayrıştır:** popülasyon (`child/adolescent type 1 diabetes`), yapı (`parenting`,
   `overprotection`, `EMBU`, `maternal depression`, `sibling relationship`), sonuç (`adjustment`,
   `internalizing`, `family functioning`), yöntem (`meta-analysis`, `validation`, `dyadic`) ve
   coğrafya (`Turkey`, `Turkish sample`) facet'lerine böl.
2. **Sorgu varyantı üret:** dar, geniş, lateral, ölçüm-odaklı ve Türkiye-odaklı varyantları ayrı
   çalıştır. Örnek: `type 1 diabetes parenting overprotection`, `EMBU adolescent validation`,
   `maternal depression parenting diabetes child`, `sibling relationship chronic illness Turkey`.
3. **Bibliyografik census yap:** PubMed/EPMC exact terminoloji, OpenAlex/S2 citation graph, YÖK
   yerel tez, ClinicalTrials/bioRxiv-medRxiv ve psikoloji/preprint/preregistration sinyalinde
   PsyArXiv/OSF katmanlarını ayrı ayrı tara.
4. **Semantik genişlet:** seminal makalelerin cited-by/reference ağından, MeSH/keyword/concept
   varyantlarından ve ölçüm aracı adlarından yeni adaylar çıkar. Sadece ilk arama sonuçlarıyla yetinme.
5. **Dedupe ve sınıflandır:** adayları çalışma tipi (meta-analiz, review, primer çalışma, validation,
   tez), popülasyon yaşı, T1DM özgüllüğü, ölçüm aracı, ülke ve tarih alanlarıyla etiketle.
6. **Rerank ve önceliklendir:** meta-analizler, sistematik derlemeler, T1DM-özgül primer çalışmalar,
   EMBU/ölçek validasyonları, Türkiye verileri ve son 10 yıl güncellemeleri ayrı kulvarlarda
   değerlendir. Eski ama seminal kaynakları sadece tarih nedeniyle düşürme.
7. **Tam-metin tetikle:** abstract'ta sayısal endpoint, alt grup, ölçek güvenirliği, faktör yapısı,
   örneklem tanımı veya ölçüm ayrıntısı eksikse D4'e geç.
8. **Üst-akıl semantik hakemlik:** kaynakları yalnız özetleme; çelişkileri çöz, hangi kanıtın tez
   iddiasına gerçekten transfer edilebilir olduğunu tart, `claim_ledger` güven düzeyini belirle.
9. **Claim ledger üret:** her esaslı iddiayı kaynak kimliğine bağla; kaynak yoksa iddiayı çıkar
   veya "VERİ BULUNAMADI" yaz.

Codex'te tool adı kullanırken discovery sonrası doğrulanmış **tam-nitelikli `server:tool` adını**
not et; bilinmeyen tool adını tahmin etme.

### 0.5 Tam-Metin / `annas-reader` Kullanım Kapısı

Tam metin **doğruluk ve ayrıntı artırma katmanıdır**. Şu koşullardan biri varsa D4'e erken geç:
- Abstract/künye sayısal endpoint'i vermiyor: etki büyüklüğü, GA, alt-grup, ölçek güvenirliği,
  faktör yükü, cut-off, örneklem alt kırılımı.
- Tezde kullanılacak kritik iddia yalnız yöntem/ek tablo/tartışma bölümünde doğrulanabiliyor.
- Citation audit'te künye var ama çalışma türü, örneklem veya ölçüm aracı belirsiz.
- Bir kaynak tezde benchmark, prior, psikometrik referans veya kritik tartışma dayanağı olacak.
- Bir meta-analiz veya review içindeki alt-grup/operasyonel tanım abstract'ta görünmüyor.

Kademeli sıra:
1. PubMed/EPMC metadata + varsa PMCID/legal OA.
2. Copyright durumunu kontrol et; uygun açık erişimde ilgili bölüm/tabloyu hedefli oku.
3. Uygun değilse `annas-reader` yalnız **analiz amaçlı, hedefli çıkarım** için kullanılır; tam metin
   kopyalanmaz, uzun alıntı yapılmaz.
4. Tam metinden yalnız hedefli alanları çıkar: örneklem, yaş aralığı, ölçüm aracı, çalışma tasarımı,
   etki büyüklüğü/GA, alt-grup, faktör/güvenirlik, sınırlılıklar, tablo/ek lokatörü.
5. Çıkış formatı: kaynak ID, bölüm/sayfa/tablo ipucu, çıkarılan sayı/ifade, tezde kullanılacağı claim,
   kısa yorum, telif/gap notu.

Yasaklar: tam metni bağlama dökmek, PDF'i kalıcı belleğe aktarmak, uzun verbatim pasaj üretmek,
erişilemeyen tam metinden sayı uydurmak.

### 0.6 İki-Aşamalı Üretim ve Doğrulama

Muhakeme yoğun sentezde önce serbest biçimli derin sentez üret, sonra yapılandır:

1. **Derin draft sentez:** konu haritası, ana bulgular, çelişkiler, yöntem kalitesi, ölçüm uyumu,
   Türkiye/çocuk/T1DM transferi ve tam-metin ayrıntılarıyla Türkçe kanıt anlatısı.
2. **Semantik hakemlik:** her claim için "hangi kaynak, hangi popülasyon, hangi ölçüm, hangi sayısal
   değer, hangi sınırlılık" sorularını yanıtla; zayıf claim'i düşür veya düşük güvenle işaretle.
3. **Yapılandırma:** aynı içeriği `evidence_packet` şemasına indir; ayrıntıyı `claim_ledger`,
   `candidate_sources`, `fulltext_extracts` ve `semantic_adjudication` alanlarında koru.
4. **Gate kontrolü:** T1DM kapsamı, HARKing, uydurma referans, telif, PII, artefakt eşleşmesi.
5. **Revizyon:** gate başarısızsa sorunlu claim/source satırlarını düzelt; gerekirse D2-D4'e geri dön.

### 0.7 Evidentia Tam-Yığın Orkestrasyon — Bu Repo İçin

Her dış-kanıt sorgusunda **tüm araç havuzu önce düşünülür**; ilgili katman maksimum derinlikte
çalıştırılır, ilgisiz/kapalı/auth eksik olanlar ise `gap_log` veya görünmez OPS notuna yazılır.
Bu, "her araç körlemesine çağrılır" değil; **üst-akıl coverage_set tüm araçları değerlendirir,
ilgili olanları kaskada enjekte eder** demektir.

| Katman | Varsayılan kullanım | Bu tezdeki özel amaç |
|--------|---------------------|----------------------|
| `start` skill | Roster/preflight, yüzey ayrımı, eksik connector notu | Her ciddi literatür koşumunda zihinsel D0; Codex'te `codex mcp list` + `.claude/evidentia.local.md` |
| `medical-research` skill | Adım 0–5, semantic scope scan, §1–21 iç iskele | T1DM kapsam kapısıyla dış-kanıt üst-aklı |
| Akademik çekirdek | PubMed/EPMC, Paper Search, OpenAlex, Semantic Scholar, PsyArXiv/OSF, YÖK Tez, ClinicalTrials/bioRxiv varsa | Giriş, Tartışma, benchmark, psikometri, citation audit, preregistration kontrolü |
| Türkiye katmanı | YÖK Tez, YÖK Akademik, EPMC `AFF:"Turkey"`, TİTCK Cache; Mevzuat yalnız kapsam sinyali varsa | TR tez boşluğu, Türk örneklem ve KOL haritası |
| Epidemiyoloji | ICD-11 için openfda; PopHIVE yalnız ABD; global/TR native yoksa boşluk | T1DM arka planı; PopHIVE ABD dışına genellenmez |
| Extended Tier-K | med-terminologies, NIH Clinical Tables, NLM RxNorm, IUPHAR | Kod/terim normalizasyonu, mekanizma/ilaç sinyali varsa çapraz doğrulama |
| Tam metin | EPMC/PMC, pubmed-epmc legal OA, Paper Search, `annas-reader`, Wiley varsa | Etki büyüklüğü, GA, ölçek/faktör/güvenirlik, alt-grup ve yöntem ayrıntısı |
| RAG/GraphRAG | anamnesis `corpus_stats` → ingest → multi-query `hybrid_query`/`semantic_search` | Tam metinleri ve büyük çıktıları ham dökmeden derin semantik değerlendirme |
| KOL haritası | OpenAlex → Semantic Scholar → EPMC → YÖK Akademik | Jüri/hakem/ortak yazar ve literatür otoritesi |
| Sidecar/temiz-kopya | `evidence_packet`, `evidence_corpus`, `evidence_index`, `sources_summary`, OPS/VIZ ayrımı | Tez paragrafı + izlenebilir denetim izi |

Kapsam kapısı bu katmanları **daraltmaz**, yalnız gürültüyü önler: farma/HTA/regülatuar/ilaç-DDI
katmanları T1DM psikososyal soruda zorlanmaz; ama kullanıcı klinik, epidemiyolojik, ilaç, kodlama
veya mevzuat sorarsa ilgili Evidentia ekseni tam derinlikte açılır.

### 0.8 Kanonik Artefakt ve Retrieve-Don't-Dump

Evidentia sistematiğindeki tek-sefer kuralı bu repo için de zorunlu:

| Artefakt | Ne zaman oluşur | Repo kullanımı |
|----------|-----------------|----------------|
| `evidence_corpus` | İlk akademik/bibliyografik tarama | Sentez, citation audit, KOL ve tam-metin adayları |
| `evidence_index` | Tam metin veya büyük çıktı anamnesis'e ingest edilince | `hybrid_query` ile derin semantik arama; ham metin bağlama dökülmez |
| `terminology_map` | Kod/terim/ölçek/ilaç normalizasyonu gerektiğinde | ICD/MeSH/ATC/RxNorm/ölçek terimi uyumu |
| `kol_graph` | KOL veya jüri/hakem sorusunda | OpenAlex/S2/EPMC/YÖK Akademik yazar ağı |
| `sources_summary` | Her koşum sonunda | `references.bib`, `chapters/*.qmd`, gap/sapma kararları |

Connector davranış kuralları:
1. ICD-11 metin araması **daima** `openfda.icd11_search`; `med-terminologies.icd11_search`
   çağrılmaz. `med-terminologies` whitelist'i: `atc_classify`, `map_icd10_to_icd11`,
   SNOMED/LOINC/RxNorm/MeSH/ATC çapraz yürüyüşleri.
2. `semantic-scholar` ikincildir. 429/500 = paylaşımlı gateway limiti/arıza; 1 retry + exponential
   backoff sonrası yine hata varsa sessiz başarı varsayma, `gap_log` yaz ve OpenAlex citation graph +
   PubMed-EPMC ile devam et.
3. `pophive` yalnız ABD için kullanılır. Precomputed kanıt aynen aktarılır; global/Türkiye yükü
   PopHIVE'dan türetilmez, native kaynak yoksa belgelenmiş boşluk olarak kalır.
4. Primer Türkiye mevzuatı `mevzuat`; `mevzuat-bilgisi` ikincil çapraz-kontrol ve kanun numarası/
   gerekçe araması içindir.

anamnesis kullanımı:
1. `corpus_stats` kontrol et; `docs == 0` ise "kanıt yok" deme, önce ilgili belgeyi ingest et.
2. Tek sorgu kullanma; T1DM sorusunu alt-yönlere bölüp `queries[]` ile çok-sorgulu
   `hybrid_query` çalıştır: popülasyon, ölçüm, sonuç, yöntem, ülke ve kritik endpoint.
3. Gerekirse LLM-in-the-loop ilişki çıkarımıyla `upsert_triples`, sonra `graph_neighbors`/`subgraph`.
4. Bayat/test belge varsa `forget_document(doc_id)` ile temizle; boş üstüne yazma.

### 0.9 Minimum Profesyonel Kanıt Zekası Kapıları

Bir cevap "derin tıbbi profesyonel düzey" sayılmadan önce şu kapılardan geçer:

- **G-COVERAGE:** coverage_set tüm ilgili Evidentia katmanlarını kapsadı mı? Kapsanmayan katman
  gerekçesi `gap_log` içinde mi?
- **G-RAG:** tam metin/RAG kullanılan her claim, `evidence_index` veya tam-metin lokatörüne bağlı mı?
- **G-XVAL:** kritik klinik/terminolojik/sayısal iddia en az iki bağımsız kaynakla veya otoriter
  kaynakla çapraz doğrulandı mı?
- **G-COPYRIGHT:** tam metin analizi hedefli mi; uzun verbatim/toptan çoğaltma yok mu?
- **G-BIB:** her kaynak PMID/DOI/NCT/YÖK-ID/OpenAlex-ID veya açık künye ile izlenebilir mi?
- **G-T1DM:** popülasyon, yaş, ölçüm aracı, psikososyal kapsam ve Türkiye/transfer sınırlılıkları
  açık mı?
- **G-HARKING:** prior/benchmark confirmatory kararı etkiliyorsa OSF zamanlama/sapma notu var mı?

---

## 1. evidentia Giriş Noktaları — Tez İçin Hangisi

| evidentia girişi | Ne yapar | Tezdeki kullanım |
|------------------|----------|------------------|
| `/evidentia <soru>` | Tam çok-kaynaklı kanıt sentezi (Adım 0–5) | Tek konu/benchmark/odaklı tarama |
| `/evidentia-synthesize <soru> [DOI'ler]` | Graph-temelli derin sentez (anamnesis RAG/GraphRAG, retrieve-don't-dump) | Giriş/Tartışma literatür-review düzeyi, çok-belge |
| `/evidentia-fulltext <DOI/PMID/PMCID>` | Copyright-kapılı tam-metin kademesi | Kritik makaleden sayısal endpoint çıkarma (HR, CI, etki büyüklüğü) |
| `/evidentia-kol <alan/konu>` | KOL/uzman ağı (OpenAlex→S2→EPMC→NPI→YÖK Akademik) | Jüri/hakem önerisi, ortak-yazar, alan otoriteleri |
| `evidence-synthesizer` (alt-ajan) | Ağır fan-out izolasyon ajanı | ≥3 eksen / çok-belge / izole derin semantik değerlendirme gerektiğinde |
| `academic-archival-distiller` (alt-ajan) | YÖK Tez + Scholar (non-medical) damıtıcı | TR psikoloji/gelişim tezleri, arşiv literatürü; Codex'te yoksa `yoktez-mcp` doğrudan akışı |

**Ağır-koşum kararı:** Giriş'in tamamı gibi çok-belge + çok-tema getiren işler için
`evidence-synthesizer` alt-ajanını çağır; amaç bağlam tasarrufu değil, ayrı bir pencerede daha
derin kaynak tarama, çelişki çözümü ve tam-metin çıkarımı yapmaktır. Tek benchmark/odaklı soru
doğrudan `/evidentia` ile başlayabilir, ancak D2 semantik genişletme ve D4 tam-metin kapısı yine
açıktır. **Türkçe psikoloji/gelişim alanyazını + YÖK tezleri** ağırlıklıysa
`academic-archival-distiller` daha isabetli (evidentia'nın medikal ağırlığı yerine). Codex'te alt-ajan
yoksa aynı işi `yoktez-mcp` doğrudan akışıyla yap.

---

## 2. KAPSAM KAPISI (ZORUNLU) — T1DM Psikososyal Coverage Gate

evidentia medikal/farma/regülatuar katmanları da içeren geniş bir araç havuzudur. **Bu tez
gelişimsel/psikososyal**: diyabet medikal çapadır ama çekirdek **ebeveynlik tutumu, depresyon,
kardeş ilişkisi**dir. Bu nedenle T1DM ana gate, araç kapatma mekanizması değil
**coverage_set tabanlı üst-akıl filtresidir**: tüm katmanlar önce değerlendirilir, ilgili olanlar
maksimum derinlikte çalıştırılır, ilgisiz/auth eksik/latency nedeniyle çalışmayanlar `gap_log`
içinde gerekçelendirilir.

### Varsayılan yüksek öncelikli katmanlar
- **Akademik çekirdek:** PubMed/EuropePMC, Consensus, ClinicalTrials.gov (T1DM psikososyal RCT'ler
  için), bioRxiv/medRxiv, **PsyArXiv/OSF** (psikoloji preprint + preregistration), **YÖK Tez /
  yoktez-mcp** (TR tezler), **OpenAlex**, **Semantic Scholar**.
- **Tam-metin kademesi:** EPMC PMC → copyright → annas → Unpaywall (sayısal benchmark çıkarımı).
- **KOL haritası:** alan otoriteleri (Streisand, Monaghan, Pinquart, Furman, Perris/EMBU geleneği).
- **0.5.K Epidemiyoloji:** T1DM insidans/prevalans (Türkiye + global; ICD-11 kodu E10).
- **Türkiye katmanı (AFF:"Turkey" + YÖK):** TR örneklemli ebeveynlik/EMBU/diyabet çalışmaları.

### Koşullu açılan katmanlar
- **AdisInsight ilaç pipeline (0.5.I):** ilaç/molekül/müdahale sorusu varsa.
- **TİTCK ruhsat/fiyat/geri ödeme, Mevzuat/SUT:** Türkiye erişim, ruhsat, geri ödeme veya mevzuat
  sorusu varsa.
- **HTA/ICER/QALY (0.5.D), Regülatuar onay (0.5.C):** sağlık-teknolojisi veya onay sorusu varsa.
- **DDI, RxNorm, IUPHAR, openFDA, klinik terminoloji:** ilaç güvenliği, ATC/RxNorm, ICD/SNOMED
  veya mekanizma sorusu varsa.
- **Onko/Heme/İmmün/Nöro/Nadir hastalık eksenleri:** yalnız gerçek çapraz-endikasyon veya yöntemsel
  benchmark sinyali varsa.
- **Pediatrik diyabet klinik bağlamı (ISPAD HbA1c eşikleri):** KISIM X DM alt-analizi ve klinik
  yorum gerektiğinde; bkz. [`dm-klinik-altanalizler.md`](dm-klinik-altanalizler.md).

**Pratik uygulama:** evidentia'ya soru verirken konuyu **psikososyal çerçevele**
("type 1 diabetes parenting overprotection child adjustment", "EMBU short form factor structure
adolescents", "maternal depression parenting behavior meta-analysis"). Molekül/ilaç/ATC dili
yalnız soru gerçekten gerektiriyorsa kullanılır; gereksiz fan-out `gap_log` içinde bastırılır.

> **Opsiyonel proje-ayarı (`.claude/evidentia.local.md`):** Tez deposu kökünde bu dosya
> evidentia'nın Adım 0.1'inde okunur. Tez için önerilen frontmatter — T1DM ana gate'i ve D0-D6
> kaskadını sabitler:
> ```yaml
> ---
> enabled: true
> evidence_mode: maximum_depth_uncapped
> default_cascade: D0-D6
> auto_ingest_rag: true
> fulltext_tier: copyright_gated
> completeness_gate: standard
> ---
> # Not: Psikososyal tez — tüm katmanlar coverage_set ile değerlendirilir;
> # ilgisiz katmanlar gerekçesiyle gap_log'a düşer, açık sinyalde tam derinlikte açılır.
> ```
> Bu dosya yoksa evidentia varsayılanla çalışır; oluşturmak istenirse kullanıcıya sorulur
> (tez deposuna dokunur).

---

## 3. Tez Artefaktlarına Besleme Haritası

Her evidentia koşumu bir tez çıktısına **bağlanır**. "Araştırdım" yetmez; sonuç bir artefakta işlenir.

| Literatür ihtiyacı | evidentia girişi | Beslediği tez artefaktı | t1dm reference |
|--------------------|------------------|--------------------------|----------------|
| Giriş literatür temeli | `evidence-synthesizer` (ağır) | `chapters/01_giris.qmd` + `references/references.bib` | `tez-yazim-rehberi.md` |
| Tartışma — bulgu konumlandırma | `/evidentia` (bulgu başına) | `chapters/05_tartisma.qmd` | `raporlama-sablonlari.md` |
| Pinquart 2013 benchmark doğrula/güncelle | `/evidentia` (hedefli meta-analiz) | `etki-buyuklugu-ve-guc.md` benchmark tablosu | `etki-buyuklugu-ve-guc.md` |
| Bayesian prior türetimi (Pinquart-temelli) | `/evidentia` → etki-büyüklüğü dağılımı | brms prior + `bayesci-paralel-hat.md` | `bayesci-paralel-hat.md` |
| H5 beklenen diadik örüntü (Streisand & Monaghan) | `/evidentia` (diadik uyum lit.) | `h5-diadik-tutarlilik.md` beklenen-örüntü | `h5-diadik-tutarlilik.md` |
| EMBU psikometrik benchmark (α/ω, faktör, invariance) | `/evidentia` + `/evidentia-fulltext` | `psikometri-pipeline.md` + Yöntem | `psikometri-pipeline.md` |
| T1DM Türkiye epidemiyoloji | `/evidentia` (0.5.K + AFF:"Turkey") | Giriş gerekçe paragrafı | — |
| Citation audit (`references.bib` doğrula) | `/evidentia` (hedefli künye lookup) | `references/references.bib` + tedbir denetimi | `tedbir-ve-hatalar.md` |
| TR benzer tez konumlandırma (özgünlük) | `academic-archival-distiller` (YÖK Tez) | Giriş "literatürdeki boşluk" | `diseminasyon-ve-yayin.md` |
| TR tez taraması / YÖK-ID doğrulama (Codex) | `yoktez-mcp` doğrudan akışı | Giriş literatür boşluğu + citation audit | `tez-yazim-rehberi.md` |
| Yayın stratejisi — hakem/dergi/ortak yazar | `/evidentia-kol` | 3-makale plan | `diseminasyon-ve-yayin.md` |

---

## 4. Kanıt Akışı — Uçtan Uca Protokol

### Adım A — İhtiyacı sınıfla
Soru **iç-veri** mi (burada kal) **dış-kanıt** mı (evidentia)? Karışıksa ikiye böl: iç parçayı
sen yürüt, dış parçayı evidentia'ya ver, paragrafta birleştir.

### Adım B — Çerçeveyi psikososyal kur (KAPSAM KAPISI §2)
Soruyu İngilizce + psikososyal terimlerle yaz; `coverage_set` tüm araçları değerlendirir, ilgisiz
fan-out gerekçesiyle `gap_log` içinde bastırılır.

### Adım C — Giriş noktasını seç (§1 tablosu)
Tek konu → `/evidentia`; çok-belge derin → `/evidentia-synthesize` veya `evidence-synthesizer`;
tam metin → `/evidentia-fulltext`; TR tez → `academic-archival-distiller` veya Codex'te
`yoktez-mcp`; KOL → `/evidentia-kol`.

### Adım D — evidentia'yı çalıştır, kanonik artefaktı al
evidentia `evidence_corpus` + numaralı sentez + provenance (PMID/DOI/NCT/YÖK-ID) döner. Codex'te
kapanış çıktısı en az şu `evidence_packet` alanlarını taşımalı:

```yaml
question: "<soru>"
surface: codex
scope_gate: psychosocial_t1dm
preflight:
  evidentia_skills: ["start", "medical-research"]
  mcp_roster_checked: true
  missing_or_unavailable: []
coverage_set:
  t1dm_refs: []
  evidentia_layers: []
  excluded_layers_with_reason: []
depth_decision:
  reached: D0|D1|D2|D3|D4|D5|D6
  rationale: "<neden bu derinlikte duruldu veya neden tam metne çıkıldı>"
connectors_used: []
source_ids:
  pmid: []
  doi: []
  nct: []
  yok_tez_no: []
  openalex_id: []
  psyarxiv_id: []
  osf_registration_id: []
retrieval_summary:
  query_variants: []
  databases_searched: []
  semantic_expansion_steps: []
  rerank_basis: []
  excluded_sources: []
canonical_artifacts:
  evidence_corpus: ""
  evidence_index: ""
  terminology_map: ""
  kol_graph: ""
  sources_summary: ""
candidate_sources:
  - source_id: ""
    study_type: ""
    population_fit: "direct|partial|indirect"
    measurement_fit: "direct|partial|indirect"
    reason_for_inclusion: ""
fulltext_extracts:
  - source_id: ""
    access_route: "pmc|legal_oa|annas-reader|unavailable"
    locator: "page/section/table"
    extracted_fact: ""
findings: []
claim_ledger:
  - claim: ""
    source_ids: []
    confidence: "high|moderate|low"
    transfer_notes: ""
semantic_adjudication:
  conflicts: []
  strongest_evidence: []
  weakest_links: []
  decision: ""
validation_gates:
  G_COVERAGE: "pass|partial|fail"
  G_RAG: "pass|partial|fail|not_applicable"
  G_XVAL: "pass|partial|fail"
  G_COPYRIGHT: "pass|partial|fail|not_applicable"
  G_BIB: "pass|partial|fail"
  G_T1DM: "pass|partial|fail"
  G_HARKING: "pass|partial|fail|not_applicable"
thesis_integration: []
gap_log: []
```

Ham connector çıktısı dökme; damıtılmış bulgu + izlenebilir kimlikleri taşı. **Sessiz atlama yok** —
"VERİ BULUNAMADI" varsa olduğu gibi taşı.

### Adım E — Tedbir denetimi (ZORUNLU — iç analizdeki gibi)
Dış kanıta da [`tedbir-ve-hatalar.md`](tedbir-ve-hatalar.md) uygulanır:
- [ ] **Tek meta-analiz mutlak değildir** — en az iki bağımsız kaynakla üçgenle.
- [ ] **Etki büyüklüğü + GA** taşındı mı (sadece "anlamlı" değil)?
- [ ] **Yayın yanlılığı** (publication bias) sorgulandı mı (funnel/Egger varsa)?
- [ ] **Popülasyon transferi** geçerli mi? (Erişkin → çocuk, batı → TR örneklem farkı not edilir.)
- [ ] **Korelasyon ≠ nedensellik** — gözlemsel literatür nedensel dile çevrilmedi.
- [ ] **Uydurma referans yok** — her künye evidentia-dönüşlü gerçek PMID/DOI/NCT/YÖK-ID'ye iz sürer.

### Adım F — Tez artefaktına işle (§3 haritası)
APA 7'ye çevir, `references.bib`'e ekle, ilgili `.qmd` / reference dosyasını güncelle.

### Adım G — Açık bilim çapraz kontrolü (§5)
Bu kanıt confirmatory bir kararı (özellikle **prior**) etkiliyorsa zamanlama/ön-kayıt denetimi.

---

## 5. Açık Bilim Bütünlüğü — Prior ve HARKing Tuzağı (KRİTİK)

> **EN ÖNEMLİ ENTEGRASYON KURALI.** Literatürden türetilen **Bayesian prior**'lar (Pinquart-temelli,
> bkz. [`bayesci-paralel-hat.md`](bayesci-paralel-hat.md)) **veriyi görmeden, ön-kayıt anında**
> türetilmeli ve OSF'e (`osf.io/pytfe`) kaydedilmelidir. evidentia ile sonradan literatür çekip
> "prior'ı güçlendirmek" → **HARKing** (Hypothesizing After Results Known) ve garden-of-forking
> ihlalidir.

Uygulama kuralları:
- **Confirmatory (H1–H4) prior'lar:** Yalnız ön-kayıtta sabitlenen literatür temeline dayanır.
  evidentia ile *sonradan* bulunan bir meta-analiz prior'ı **değiştiremez**; ancak `[KEŞİFSEL]`
  duyarlılık analizi olarak ek prior denenebilir — ön-kayıttakinin yerine geçmez.
- **Tartışma için literatür:** Sonradan getirmek serbesttir (bulgu zaten üretildi) — Tartışma
  *yorumdur*, hipotez-testi değil.
- **Benchmark güncelleme:** Pinquart 2013 yerine daha güncel bir meta-analiz bulunursa, bu
  **yöntemsel sapma** olarak tez deposundaki `docs/analiz_planlari/PRE-REGISTRATION-DEVIATION-TABLE.md`
  satırına yazılır; sessizce değiştirilmez.
- **Keşifsel etiket:** evidentia ile keşfedilen ve ön-kayıtta olmayan her literatür-temelli iddia
  `[KEŞİFSEL]` etiketlenir.

---

## 6. APA 7 / `references.bib` Köprüsü

evidentia çıktısı **Vancouver/Türkçe temiz-kopya** üretir (PMID/DOI/NCT + erişim tarihi); tez ise
**APA 7 + `references.bib` + `apa.csl`** kullanır. Dönüşüm zorunlu:

1. evidentia'nın döndürdüğü her kaynağı **PMID/DOI/NCT/YÖK-ID** ile yakala.
2. YÖK tezlerinde `thesis_no`, `detail_page_url` ve `get_yok_tez_thesis_details` künye çıktısını
   koru; DOI yoksa DOI uydurma.
3. BibTeX künyesi üret: DOI'li makale için `@article{...}`, tez için `@phdthesis{...}` veya
   `@mastersthesis{...}`; `references/references.bib`'e ekle — **çift kayıt yapma** (mevcut
   anahtarları kontrol et).
4. `.qmd` içinde `[@anahtar]` ile atıfla; Quarto `apa.csl` ile APA 7 render eder.
5. **Türkçe terim disiplini:** Gövde metni Türkçe; İngilizce terim sadece parantezde
   (bkz. ana SKILL terim sözlüğü). evidentia İngilizce/Türkçe karışık döndürürse Türkçeye elden çevir.

**Uydurma referans yasağı (mutlak):** `references.bib`'e giren her kayıt evidentia-doğrulamalı
gerçek bir PMID/DOI/NCT/YÖK-ID'ye iz sürmelidir. evidentia bir künyeyi doğrulayamıyorsa o referans
**eklenmez**; "VERİ BULUNAMADI" notuyla kullanıcıya bildirilir.

---

## 7. Tipik Senaryolar (Uçtan Uca)

**Senaryo 1 — Giriş literatür temeli (ağır):**
> "Giriş'e T1DM çocuklarda ebeveyn aşırı korumacılık ve uyum literatürü."
1. `evidence-synthesizer` alt-ajanını çağır (çok-belge, kaskad derinlik, semantik hakemlik).
2. Çerçeve: psikososyal (§2); ilgili tüm katmanlar `coverage_set` ile seçilir, ilgisizler gerekçelenir.
3. Dönen sentez + provenance → tedbir denetimi (§4-E).
4. APA 7'ye çevir, `references.bib` doldur, `chapters/01_giris.qmd` yaz.

**Senaryo 2 — Pinquart benchmark doğrulama:**
> "Pinquart 2013 r ≈ .19 hâlâ en iyi benchmark mı?"
1. `/evidentia "parenting behavior child internalizing meta-analysis effect size"`
2. Güncel meta-analiz var mı? Etki büyüklüğü + GA + heterojenlik (I²).
3. Bulgu → `etki-buyuklugu-ve-guc.md` benchmark tablosu güncellenir; sapma varsa deviation tablosu.
4. **Prior etkisi varsa §5 zamanlama denetimi.**

**Senaryo 3 — Tartışma bulgu konumlandırma:**
> "H5 diadik tutarsızlığımız (anne > çocuk algı) literatürle uyumlu mu?"
1. `/evidentia "parent child dyadic concordance discrepancy parenting perception"`
2. Streisand & Monaghan beklenen örüntüyle karşılaştır (bkz. `h5-diadik-tutarlilik.md`).
3. Uyum/çelişki Tartışma'da açık raporlanır (sosyal istenirlik kompansasyonu yorumu).

**Senaryo 4 — Kritik makaleden sayısal çıkarım:**
> "Şu meta-analizin alt-grup HR'leri lazım."
1. `/evidentia-fulltext <DOI>` — copyright kademesi.
2. CC-BY ise tam metin; değilse künye + kısa alıntı + yönlendirme.
3. Sayısal endpoint → tez tablosu/benchmark.

**Senaryo 5 — Citation audit:**
> "`references.bib`'teki şu 5 künye gerçek mi?"
1. Her künyeyi `/evidentia` ile PMID/DOI üzerinden doğrula.
2. Eşleşmeyenler işaretlenir; düzeltilir veya çıkarılır (uydurma referans yasağı §6).

**Senaryo 6 — TR tez konumlandırma / YÖK-ID doğrulama (Codex):**
> "Türkiye'de T1DM çocuklarında ebeveyn tutumu veya kardeş ilişkisi üzerine benzer tez var mı?"
1. `yoktez-mcp.search_yok_tez_detailed` ile başla; `keyword` alanını psikososyal terimlerle daralt.
2. Aşırı geniş sonuçta `list_yok_tez_anabilim_dali` → `search_yok_tez_by_anabilim_dali` ile
   psikoloji, çocuk sağlığı, hemşirelik veya rehberlik/PDR anabilimlerine in.
3. Aday tezlerde `get_yok_tez_thesis_details`; izinliyse yalnız gerektiği kadar
   `get_yok_tez_document_markdown`.
4. `evidence_packet.source_ids.yok_tez_no` + kısa özgünlük/boşluk sentezi üret; DOI uydurma.

**Senaryo 7 — PsyArXiv/OSF preprint ve preregistration kontrolü (Codex):**
> "T1DM ebeveynlik/uyum alanında PsyArXiv preprint veya OSF preregistration var mı?"
1. Geniş recall için önce OpenAlex/Semantic Scholar/Paper Search ile `type 1 diabetes parenting`
   ve ölçüm-terim varyantlarını tara.
2. OSF-native doğrulama için `psyarxiv-osf.psyarxiv_search_preprints` kullan; `query` yalnız başlık
   eşleşmesi olduğu için dar title terimleriyle, `tags`/`subjects` ile ve tarih filtresiyle ayrı koş.
3. Adaylarda `psyarxiv_get_preprint` ile yazar, tarih, DOI, OSF linki, withdrawn/tombstone ve tag
   alanlarını doğrula; tam metin gerekiyorsa `psyarxiv_get_full_text` yalnız download URL/lokatör verir.
4. Preregistration/protocol ihtiyacında `osf_search_registrations` ile başlık/tag üzerinden ara;
   `source_ids.psyarxiv_id` ve `source_ids.osf_registration_id` alanlarını doldur. Preprint'leri
   peer-reviewed kanıt gibi sunma; claim ledger'da preprint/preregistration statüsünü açık etiketle.

---

## 8. Sınırlar ve Devir

- evidentia **klinik karar/öneri üretmez** — kanıt sentezler, belirsizliği işaretler. Tez de
  betimsel/çıkarımsal kalır.
- **DDI/ilaç-etkileşim, ruhsat, geri ödeme** bu tezin varsayılan psikososyal kapsamında düşük
  önceliklidir; açık klinik/ilaç/mevzuat sinyali varsa tam derinlikte çağrılır (§2).
- **OSINT/web rekabet istihbaratı** evidentia v1.4.0'da kaldırıldı; gerekmez.
- **Niteliksel kol** (RTA, dyadik görüşme) literatürü için `niteliksel-arastirma-rehberi-t1dm`
  skill'i + evidentia akademik-çekirdek birlikte; metodoloji derinliği o skill'de.
- evidentia bir kaynağı getiremezse **sessizce atlamaz**; "VERİ BULUNAMADI" + denenen sorgular
  taşınır ve tez metninde de boşluk dürüstçe belirtilir.

---

**Tek cümlelik özet:** Tezin dış-kanıt ihtiyacı (Giriş, Tartışma, benchmark, prior, psikometrik
referans, epidemiyoloji, citation audit) **T1DM psikososyal coverage_set** ile yönetilen evidentia
koşumlarına delege edilir; dönen kanıt tedbir denetiminden + açık-bilim zamanlama kontrolünden
geçer, APA 7'ye çevrilip `references.bib` ve ilgili `.qmd`/reference dosyasına işlenir — iç-veri
analizi her zaman bu skill'de kalır.
