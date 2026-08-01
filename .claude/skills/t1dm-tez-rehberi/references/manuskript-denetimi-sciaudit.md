# Manüskript Adli Denetimi ve Türkçe Yazım — sci-audit Entegrasyonu

> **Amaç:** Tezin **yazılmış metnini** (üretilen `.qmd`/paragraf) yayın-öncesi adli
> ve dilsel denetimden geçirmek. `t1dm-tez-rehberi` iç-veri analizini üretir,
> `evidentia` dış-kanıtı getirir; **`sci-audit` ise ORTAYA ÇIKAN METNİ denetler.**
> Üç katman birbirini besler, karışmaz.

Bu dosya `t1dm-tez-rehberi` ile **`sci-audit@cureonics-marketplace`** plugin'i
arasındaki köprü protokolüdür. Bir bölüm/paragraf yazıldıktan **sonra**, kapanış
veya sertifikasyon öncesinde **önce bu dosyayı oku**, sonra doğru sci-audit
eksenini/komutunu seç. Yedi eksenin tamamı adım adım, eksiksiz çalıştırılır.

---

## 0. Üç Katman Sınırı (Çakışmaz Görev Dağılımı)

| Katman | Araç | Kapsam | Kapsam DIŞI |
|--------|------|--------|-------------|
| **İç-veri analizi + yazım** | `t1dm-tez-rehberi` (bu skill) | 482-satır kendi verimiz, H1-H5, psikometri, pipeline, tez paragrafı üretimi | Dış literatür getirme; metin adli denetimi |
| **Dış-kanıt getirme/sentez** | `evidentia` | Giriş/Tartışma literatürü, benchmark, prior, citation getirme, tam-metin, KOL, PRISMA | Kendi verimiz; yazılan metnin denetimi |
| **Manüskript adli + dilsel denetim** | **`sci-audit`** (axes A–G) | Yazılan metnin referans bütünlüğü (A), claim grounding (B), istatistik iç-tutarlılığı (C), halüsinasyon sinyalleri (D), raporlama-kılavuzu uyumu (E), AI-şeffaflık (F), **Türkçe imla/yazım (G)** | Ham veri/KVKK sınırı, quote-parity, kanonik kilit (bunlar repo `doktoratezi-ai-audit`'te) |

**Tek cümle kural:** *Veriyi biz üretiriz; kanıtı evidentia getirir; yazdığımızı
sci-audit denetler; ham-veri/gizlilik invaryantını repo ai-audit korur.* Aynı
işlev iki yerde tekrarlanmaz.

**Akış zamanlaması:** sci-audit **üretimden sonra** çalışır. Bir bölüm taslağı
bittiğinde (Faz 3 raporlama sonrası), Kapı 4 (Türkçe imla) ve Kapı 5 (adli
denetim) `bolum-finalizasyon-sertifikasyon-playbook.md` içinde sci-audit ile
kapatılır. Sertifika + açık onay olmadan bölüm `certified-final` olmaz.

---

## 1. Yedi Eksen — Araç Envanteri (EKSİKSİZ)

Her eksen için **komut**, **skill** ve **alt-ajan** birlikte listelenir; ciddi
denetimde eksen atlanmaz.

| Eksen | Ne denetler | Komut | Skill | Alt-ajan(lar) |
|-------|-------------|-------|-------|----------------|
| **A — Referans bütünlüğü** | Uydurma/yanlış-atıf/geri-çekilmiş kaynak; DOI/PMID/arXiv checksum | `/sci-audit:verify-citations` | `sci-audit:citation-forensics` | `citation-verifier` |
| **B — Claim grounding** | Sayısal/olgusal iddia kaynağa gerçekten bağlı mı | (full `audit` kapsar) | `sci-audit:claim-grounding` | `claim-extractor` → `claim-refuter` |
| **C — İstatistik tutarlılığı** | statcheck (p-yeniden hesap), GRIM/GRIMMER, yüzde/altgrup, Türkçe ondalık virgül | `/sci-audit:check-stats` | `sci-audit:stats-forensics` | `stats-checker` |
| **D — Halüsinasyon sinyalleri** | Aşırı-kesinlik dili, uydurma yöntem/varlık adı, ISBN/ORCID checksum, semantik entropi | (full `audit` kapsar) | `sci-audit:hallucination-signals` | `entity-verifier`, `entropy-sampler` |
| **E — Raporlama kılavuzu** | PRISMA/CONSORT/STROBE/COREQ/SRQR/JARS/TRIPOD (+AI) madde-madde uyum | `/sci-audit:guideline-check --type <kılavuz>` | (orchestrator kapsar) | `guideline-mapper` |
| **F — AI-şeffaflık** | ICMJE/COPE/WAME AI-kullanım beyanı var/yok; LLM giveaway; doldurulmamış placeholder | (full `audit` kapsar) | `sci-audit:ai-transparency` | — |
| **G — Türkçe imla/yazım** | Encoding/noktalama, register, nedensellik dili, **ondalık virgül + `p` yazımı (blocker)**, kısaltma tutarlılığı | `/sci-audit:check-turkish` | `sci-audit:turkish-sci-style` | `style-judge` |

**Orkestratör (tümü tek koşumda):** `sci-audit:sci-audit-orchestrator` skill'i
dili sezer (Türkçe → axis G otomatik), bölüm tipini belirler, uzun metni böler,
yedi ekseni fan-out eder ve tek rapora birleştirir.

**Kanonik komutlar:**
- `/sci-audit:audit chapters/<bolum>.qmd --lang tr --strictness certification --type <coreq|strobe|prisma|jars>` — yedi eksen tam koşum.
- `/sci-audit:audit-report --out tez-yazim/04_kalite-kontrol/raporlar/<bolum>-sci-audit.md` — eksen bulgularını tek rapora birleştir.
- `/sci-audit:ai-log "<bölüm> sertifikasyon sci-audit koşumu"` — harici MCP/kanıt kullanımı olduysa AI-use log satırı.

**No-fabrication invaryantı:** her eksen neyi denetlediğini/denetlemediğini beyan
eder; çözülemeyen kaynak `unverified`, asla "geçti" olmaz.

---

## 2. Adım Adım Tam Denetim Protokolü (Eksiksiz — atlanmaz)

Bir bölüm kapanışında sci-audit **yedi ekseni sırayla** kapatır. Kısayol yok;
eksen atlanacaksa gerekçesi sertifika raporuna yazılır.

1. **Kapsam sabitle:** dosya `chapters/<bolum>.qmd`; bölüm tipi (Giriş/Yöntem/
   Bulgular/Tartışma) → uygun `--type` kılavuzu (Yöntem/Bulgular kanıt bölümü için
   COREQ/STROBE/JARS; sistematik derleme kesimi için PRISMA).
2. **Axis A — Referans bütünlüğü:** `/sci-audit:verify-citations` — her DOI/PMID/
   arXiv çözülür, metadata (başlık/yazar/yıl/dergi) eşleşir, geri-çekilme kontrol
   edilir. Uydurma/yanlış künye → `blocker`; evidentia ile düzelt (bkz.
   [`literatur-kanit-evidentia.md`](literatur-kanit-evidentia.md) §6 uydurma-referans yasağı).
3. **Axis B — Claim grounding:** her sayısal/olgusal iddia için `claim-extractor`
   iddiayı çıkarır, `claim-refuter` kaynağın gerçekten desteklediğini adversaryel
   test eder (varsayılan "desteklenmiyor"). Kaynaksız iç-veri iddiası bir repo
   dosyasına (CSR/`_targets`/tablo), dış-iddia bir PMID/DOI'ye bağlanır.
   - **Referans Bütünlük Şiarı (RBŞ — konstitüsyonel; `tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md` §4.1):** Bir referanstan zenginleştirme/analiz yaparken makalenin **bir parçasını değil tamamını geniş bağlamda semantik kavra**, bu bağlamı **rafine ederek** revize et; **hem kaynağın hem tez metninin somut bilimsel iddialarını çarpıtma** (cherry-pick / düzleştirme / abartma yok; kaynak kendi kapsam+koşuluyla aktarılır). RBŞ ihlali = çarpıtma; bu eksende (axis B + Galileo `overclaim_judge`/`claim_source_match`) denetlenir.
4. **Axis C — İstatistik tutarlılığı:** `/sci-audit:check-stats` — raporlanan
   test istatistiklerinden `p` yeniden hesaplanır, GRIM/GRIMMER ortalama tutarlılığı,
   yüzde/altgrup toplamı, imkânsız etki büyüklüğü. Türkçe ondalık virgül desteklidir.
5. **Axis D — Halüsinasyon sinyalleri:** aşırı-kesinlik/evrensel niceleyici dili,
   atıfsız yöntem adı, bozuk ISBN/ORCID/arXiv checksum; kritik tekil iddiada
   `entropy-sampler` ile semantik-entropi tutarlılık kontrolü; ilaç/gen/hastalık
   varlık adları `entity-verifier` ile terminoloji otoritesine karşı doğrulanır.
6. **Axis E — Raporlama kılavuzu:** `/sci-audit:guideline-check --type <kılavuz>` —
   `guideline-mapper` her maddeyi present/missing/partial + konumlandıran alıntı ile
   işaretler. Karma tez için JARS-Mixed + STROBE + COREQ birlikte değerlendirilir.
7. **Axis F — AI-şeffaflık:** ICMJE/COPE AI-kullanım beyanının varlığı, doldurulmamış
   placeholder ve LLM-giveaway sinyalleri. Beyan eksikse Yöntem/teşekkür bölümüne eklenir.
8. **Axis G — Türkçe imla/yazım:** `/sci-audit:check-turkish --strictness certification`
   — deterministik G1-G6 çekirdeği (ağsız, web dahil) + opsiyonel TDK/Zemberek/GECTurk
   provider'ları + `style-judge` alt-ajanı. **İngilizce ondalık-nokta `p` değeri
   Türkçe metinde `blocker`dır (G5).** Detay: [`tez-yazim/04_kalite-kontrol/turkce-bilimsel-yazim-denetimi.md`](../../../../tez-yazim/04_kalite-kontrol/turkce-bilimsel-yazim-denetimi.md).
9. **Birleştir:** `/sci-audit:audit-report --out tez-yazim/04_kalite-kontrol/raporlar/<bolum>-sci-audit.md`; bulgular sertifika raporuna işlenir.
10. **Kabul:** `error`/`blocker` yok; `warning`/`major` düzeltilmiş veya gerekçeli
    kabul edilmiş; harici araç kullanıldıysa `/sci-audit:ai-log` yazılmış.

**Türkçe metinde her koşumda axis G çalışır** (otomatik). Bölüm İngilizce özet
(`SUMMARY`) içeriyorsa o kesim `--lang en` ile ayrı denetlenir.

---

## 3. Tez Artefaktlarına Besleme Haritası

| Denetim ihtiyacı | sci-audit girişi | Beslediği artefakt/kapı |
|------------------|------------------|--------------------------|
| Bölüm kapanış imla/akış | `/sci-audit:check-turkish` | Kapı 4 + `raporlar/<bolum>-tr-sciaudit.md` |
| Bölüm kapanış adli denetim (A–F) | `/sci-audit:audit … --strictness certification` | Kapı 5 + `raporlar/<bolum>-sci-audit.md` |
| `references.bib` uydurma/yanlış künye | `/sci-audit:verify-citations` | `referans-denetim-ledgeri.md` + Kapı 1/2 |
| Bulgular istatistik tutarlılığı | `/sci-audit:check-stats` | Bulgular `.qmd` + tedbir denetimi |
| Yöntem/Bulgular kılavuz uyumu | `/sci-audit:guideline-check --type strobe|coreq|jars` | Yöntem `.qmd` + JARS-Mixed |
| AI-kullanım beyanı | `sci-audit:ai-transparency` | Yöntem/teşekkür + ICMJE beyanı |

Her koşumda harici MCP/kanıt kullanımı varsa `/sci-audit:ai-log` ile iz bırakılır.

---

## 4. Davranış Kuralları (Çiğnenmez)

1. **Metin adli denetimi yalnız sci-audit'te.** Referans/claim/istatistik/
   halüsinasyon/kılavuz/AI-şeffaflık/Türkçe imla bu plugin'de yürür; repo
   ai-audit'te tekrarlanmaz.
2. **Yedi eksen atlanmaz.** Ciddi bölüm kapanışında A–G tam koşulur; atlanan
   eksenin gerekçesi sertifika raporunda yazılır.
3. **Türkçe metinde axis G zorunlu**; ondalık-nokta `p` `blocker`dır.
4. **No-fabrication:** çözülemeyen kaynak/claim `unverified`; asla "geçti" denmez.
5. **Katman karıştırma yok:** ham veri/KVKK/quote-parity sci-audit'e sorulmaz
   (repo `doktoratezi-ai-audit` + `niteliksel/…/t1dm-qual-ai-audit`); dış-kanıt
   getirme sci-audit'e verilmez (evidentia).
6. **sci-audit hook'ları bu projede susturulmuştur** (`.claude/sci-audit.local.md`
   `hooks_enabled: false`) çünkü repo kendi hook katmanını taşır; **skill/komutlar
   normal çalışır** — susturma yalnız plugin'in kendi hook'larını kapsar.
7. **`certified-final` yalnız** yedi eksen + repo veri-invaryantı + açık onayla.

---

## 5. Sınırlar

- sci-audit **klinik/bilimsel doğruluk sertifikası vermez**; iç-tutarlılık,
  bütünlük ve dil denetler. Bilimsel geçerlik insan editör + danışman kararıdır.
- İntihal/benzerlik taraması kapsam dışıdır (ayrı araç).
- Deterministik çekirdek metni **dış API'ye göndermez**; yalnız açıkça verilen
  dosya okunur (PreToolUse hook ayrıca zorlar).

---

## 6. Galileo Bağımsız Judge + Semantik Katman (proje-eklentisi, sci-audit'in YANINDA)

sci-audit **Claude-native**; Galileo katmanı **bağımsız GPT-5.4** ile ikinci-görüş
(model-çeşitliliği: tek-model korelasyonlu hatalarını kırar). Minerva↔evidentia deseni,
denetim tarafında: sci-audit plugin'i **düzenlenmez**; köprü `scripts/eval/galileo_bridge.py`
(bağımlılıksız stdio, proje-kök `.mcp.json`'da `galileo-audit`; **ikisi de .gitignore** — iç
Roche altyapısı). Kaynak: Roche-içi **OpenAI-uyumlu AI gateway** `${GALILEO_GATEWAY}`
(eval-SaaS değil). Kimlik `${GALILEO_*}` env/`.env`'den (değer görülmez/commit edilmez).

**13 araç (9 çekirdek + 4 judge uzantısı):** `galileo_judge` (faithfulness/groundedness/citation_support/marmara_compliance/
hallucination_risk + gerekçe), `galileo_consistency` (bölümler-arası çelişki/tekrar),
`galileo_bib_dedup`, `galileo_claim_source_match`, `galileo_eval_run` (yerel regresyon
harness), `galileo_stats`, **`galileo_heading_cascade`** (Marmara §1.3 başlık kaskadı:
derinlik≤4, ana-başlık büyük-harf/bağlaç-küçük, başlık-sonu-noktalama, düzey-atlama +
§5 bölüm sırası — deterministik, code-fence-aware; R-chunk `#` yorumlarını başlık
saymaz), **`galileo_coherence`** (bitişik paragraf akışı: embedding cosine ile
kopukluk/tekrar — embedding yoksa judge-fallback), **`galileo_reference_prose`**
(atıf yoğunluğu + Tartışma-sıfır-atıf + reporting-verb/trailing-bracket monotonluğu;
tek bölüm veya çok-bölüm `sections`).

**Judge uzantıları (2026-07-21, spec §6 — hepsi SOFT/advisory, "critical friend"):**
`galileo_convergence_judge` (karma joint-display: uyum/tamamlayıcılık/ayrışma/açıklayıcı-
genişleme + aşırı-entegrasyon), `galileo_harking_judge` (veri-sonrası prior / ön-kayıt
sapması), `galileo_overclaim_judge` (korelasyon→nedensellik kayması + multiverse cherry-pick),
`galileo_coherence_judge` (tez-geneli amaç↔bulgu↔sonuç zinciri). `classify_gate` bunları
SOFT/advisory olarak katlar; **HARD asla LLM judge'dan gelmez** (`hard=[]` her zaman).
Ham-vektör tarafı: `scripts/eval/semantic_core.py` (embed/cosine/dedup/redundancy/match +
KVKK tripwire) + CLI `scripts/util/thesis_semantic.py` (`bib-dup`/`redundancy`, embedding
yoksa `bib_hygiene`/CRC32'ye degrade). Ayrıca `karma_ledger_check.py --semantic`
(substring-drift semantik rescue: parafraz-sadık=INFO).

**Yeni üç araç — başlık/tutarlılık/referans-nesri katmanı (advisory):** `bölüm-sertifika`
Kapı 3 (başlık/bölüm-sırası + referans-nesri uzlaştırma) ve Kapı 4 (Türkçe akış/tutarlılık)
gate'lerinin doğal genişlemesidir. Kanonik başlık/sıra otoritesi köprüye **koda gömülü**dür
(kaynak: `tez-yazim/00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` §1.3 + §5);
köprü gitignored/taşınabilir kalsın diye .md drift'ine bağımlı değildir. `heading_cascade`
deterministiktir (embedding/judge gerekmez); `coherence` embedding'i semantik omurga
yapar; `reference_prose` regex + deterministik sayımdır.

**three-tier gate:** **HARD** (sci-audit, değişmez) · **SOFT-block** (Galileo, insan-override'lı —
`certified-final`'i durdurur: groundedness/faithfulness < 0,60; nicel iddia
`citation_support=unsupported`; bölümler-arası çelişki sim≥0,85; büyük Claude↔GPT bütünlük
çelişkisi) · **advisory** (bib-dup, tekrar, üslup). Eşikler `.claude/galileo.local.md`;
`classify_gate()` üretir.

**Durum (2026-07-21):** Judge (GPT-5.4 `/chat/completions`) `GALILEO_GATEWAY` üzerinden
(grounded 0,97 / uydurma 0,05 → soft-block). **RAG-embedding backend'i Azure OpenAI'ye
taşındı:** `text-embedding-3-large` (3072-boyut), Roche Minerva **`azure-openai` Gravitee
gateway** ile — Azure-native yol + Bearer auth
(`POST {GRAVITEE_AZURE_OPENAI_GATEWAY}/openai/deployments/{deployment}/embeddings?api-version={ver}`);
claim-match/consistency `mode:embedding`. Önceki Vertex/`gemini-embedding-001` + Portkey
yolu kaldırıldı. Embedding erişilemezse otomatik judge-fallback. `_load_cfg` `.env`'i
os.environ'a tercih eder (bayat launch-env'i aşmak için).

**KVKK:** gateway'e **yalnız manuskript + literatür + references.bib**; ham katılımcı/aile-
düzeyi/transkript/kimlikleyici **asla**. **Faz 3.6'da** sci-audit 7-ekseninden sonra
advisory/soft-block pass olarak çağrılır.

**Durum (2026-07-12, bu ortamda üç-katman uçtan-uca yeniden doğrulandı):**
`claude mcp list` (.env yüklü) → **openathens + annas-reader + minerva-evidence +
galileo-audit + zotero-refs = 5/5 Connected**.

- **Minerva (embedding kanıt katmanı):** 6 araç canlı; vectorstore 25.155.544 makale /
  203.790.110 embedding. `mode:semantic` ve `mode:hybrid` (+`use_hyde`) doğrulandı;
  T1DM/ebeveyn sorgularında 0,85+ isabet. **Operasyonel not:** Türkçe sorgularda
  `mode:semantic` tercih edilir — `mode:hybrid`'in BM25 bileşeni Türkçe "anne" (=mother)
  gibi tokenleri İngilizce özel-ad ("Anne") ile karıştırır; cross-lingual embedding
  (semantic) Türkçe sorguyu İngilizce korpusta doğru eşler. `fulltext_by_doi` tek-obje
  (metadata+content) döndürür (`results[]` sarmalı değil).
- **Galileo (bağımsız judge + embedding):** 9 araç canlı; `galileo_stats` →
  `judge_ok:true, embedding_ok:true, embedding_model:text-embedding-3-large`. `galileo_judge`
  Pinquart iddiasını grounded 0,99 / uydurma 0,03 (supported); `eval_run` uydurma "900
  çalışma"yı faithfulness 0,05 / hallucination 0,96 (unsupported) ile ayırt etti.
  `claim_source_match`/`consistency`/`coherence`/`bib_dedup` hepsi `mode:embedding`.
  **Onarım:** `galileo_bib_dedup` yalnız `{title,key}` dict listesi kabul edip düz-string
  girdide ham `AttributeError` sızdırıyordu; string entry `{title:str,key:idx}`'e normalize
  edilerek dayanıklılaştırıldı (honest-degrade ilkesi; davranış değişmez, çökme engellendi).
  Köprü gitignored olduğundan düzeltme yerelde kalıcı, versiyonlanmaz.
- **sci-audit (axis G, Türkçe stil):** `tr_sciaudit.py` doktrin komutuyla
  (`--strictness certification --format md --fail-on error --enable-tdk --terms ...`)
  gerçek `chapters/*.qmd` üzerinde çalıştı: Ateşman skoru + `decimal-dot`/`p-value`/
  `repeated-word`/`abbreviation-review` bulguları + TDK provider **canlı** (`sozluk.gov.tr`
  sorgusu `status:ok`). Zemberek/GECTurk/style-judge opsiyonel katmanları safe-degrade.

**OpenAthens tam-metin (Tier 3, lisanslı):** connector kuruldu (`OPENATHENS_MCP_API_KEY`
`.env`'e eklendi; `MCP-TALIMATLAR.md` `.gitignore`'a alındı). `oa_server_info` →
Millet Kütüphanesi SAML aktif; `oa_resolve` redirector üretir. Anti-bot yayıncılarda
(OUP/Wiley/Elsevier) `oa_fetch_fulltext` → `manual_required` (Shibboleth JS-challenge);
bu doktrinseldir, interaktif SSO deep-link'i birincil kalır.

**Yığın sağlık kontrolü + birleşik claim kapısı (2026-07-12, eklendi):**

- **`scripts/mcp/audit_stack_healthcheck.py`** — tek komutta beş katman:
  MINERVA (embedding kanıt) · GALILEO (judge+embedding) · SCI-AUDIT (axis G) ·
  **ANAMNESIS (GraphRAG korpus — `corpus_stats` doc/edge eşiği)** · **CLAIM-CERT
  (4-katman kapı geçerli karar üretiyor mu)**. Tümü PASS → exit 0. KVKK: yalnız
  sabit test terimleri. `.env`'i kendi yükler (non-interaktif).
- **`scripts/util/claim_certification.py`** — dört bağımsız denetçiyi tek
  PASS/WARN/FAIL kararına indirger: `csr_numeric_trace_audit` (kaynaksız sayı) +
  `csr_causal_label_audit` (nedensel dil + keşifsel etiket) + `bib_hygiene`
  (atıf/DOI HARD/SOFT) + opsiyonel `galileo_judge` (`--with-judge`; nedensel-tarama
  CSV'sinden yüksek-riskli excerpt örneklemi). Çıkış kodu: 0=PASS, 2=WARN,
  1=FAIL(render-kırıcı). `--strict` WARN'ları FAIL'e yükseltir (yayın-öncesi son
  kapı). Regresyon: `tests/test_claim_certification.py` (11), `tests/test_graphrag_query.py` (6).

---

**Tek cümlelik özet:** Yazılan her tez bölümü, kapanıştan önce sci-audit'in yedi
ekseninden (A referans, B claim, C istatistik, D halüsinasyon, E kılavuz, F
AI-şeffaflık, G Türkçe imla) **adım adım, eksiksiz** geçer; evidentia dış-kanıtı
getirir, sci-audit yazılanı denetler, repo ai-audit veri sınırını korur.
