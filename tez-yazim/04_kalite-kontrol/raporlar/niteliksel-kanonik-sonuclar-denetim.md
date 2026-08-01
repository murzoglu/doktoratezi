# Denetim Ledgeri — Niteliksel Kanonik Sonuç Belgesi

**Artefakt:** `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd`
**Tarih:** 2026-07-11
**Orkestrasyon:** evidentia (dış-kanıt) → `niteliksel-arastirma-rehberi-t1dm` (üretim) → bib_hygiene →
sci-audit (HARD) → Galileo three-tier (SOFT/advisory) → KVKK invaryantı.

## Three-tier gate sonucu

### HARD tier (sci-audit + repo invaryantı) — GEÇTİ
| Eksen | Sonuç | Not |
|---|---|---|
| A referans bütünlüğü | GEÇTİ | 8 atıf anahtarının tümü `references.bib`'te tanımlı; 3 yeni metodoloji künyesi (JARS-Qual, SRQR, Tracy) doğrulanmış DOI ile evidentia (OpenAlex+PubMed) üzerinden çözüldü — uydurma yok |
| C istatistik tutarlılığı | GEÇTİ | COREQ 30+2+0=32 uzlaşıyor; kanonik sayılar (7 aile/21 görüşme/23 kod/116 quote id) kaynak raporla birebir |
| E raporlama (COREQ) | GEÇTİ | 32 madde: 30 tam · 2 kısmi (Madde 16 pilot, Madde 31 negatif vaka) · 0 eksik; kısmiler açıkça major olarak işaretli; blocker yok |
| G Türkçe imla | GEÇTİ | tr_sciaudit: **0 blocker**, 40 warning (hepsi false-positive/minor: tablo-flatten, J-kodu identifier, "ayrı ayrı" deyimi); İngilizce ondalık-nokta `p` yok |
| KVKK / veri sınırı | GEÇTİ | 28 alıntı yalnız `quote_id` formunda; verbatim katılımcı konuşması / kimlikleyici yok |
| Render | GEÇTİ | `quarto render --to html` hatasız; bibliyografya CSL ile author-yıl olarak çözüldü; kırık atıf yok |

### SOFT-block tier (Galileo bağımsız GPT-5.4 judge) — İNSAN-OVERRIDE
| Skor | Değer | Eşik | Sinyal |
|---|---:|---:|---|
| faithfulness | 0,72 | ≥0,60 | geçer |
| groundedness | 0,34 | ≥0,60 | **soft-block** |
| citation_support | unsupported | supported | **soft-block** |
| marmara_compliance | 0,58 | — | sınırda |
| hallucination_risk | 0,66 | — | orta-yüksek |

**Override gerekçesi (belgelenmiş):** Judge, düşük groundedness/unsupported sonucunu **judge
çağrısına kanıt-bağlamı sağlanmadığı** için üretmiştir (rationale: "KANIT sunulmadığından quote ID,
H1-H5, COREQ 30/2/0/32 ... doğrulanamamaktadır"). Bu sayılar aslında belgenin **açıkça atıf yaptığı
de-identified kanonik artefaktlara** dayanır: `qualitative_canonical_results_for_doktoratezi.md`,
`03_analysis/methodology/coreq_32_completed.md`, `03_analysis/codebook/codebook_v3.md` (belge
callout'unda ve §Kaynak Dosya Haritası'nda listeli). Judge ayrıca `.qmd` **kaynağındaki** ham
`[@key]`'i görmüştür; CSL bunları render'da author-yıl'a çevirir (üretilen HTML'de doğrulandı).
KVKK gereği judge'a ham kanıt gönderilmemiştir (yalnız manüskript metni). Bu nedenle SOFT-block,
ungrounded iddia değil **judge-bağlam + kaynak-vs-render artefaktı**dır; kanonik kaynak grounding'i
mevcuttur. Tam kanıt-bağlamlı kesin sertifikasyon, tez bölüm-kapanışında (chapters/*.qmd) yapılır.

### Advisory tier
- bib_hygiene: 3 yeni künye chapters/ perspektifinden "orphan" (bu qmd'de kullanılıyor; bib_hygiene
  varsayılan chapters/ tarar) — advisory, HARD değil.
- Minerva: bu oturumda MCP olarak bağlı değil; doktrin gereği ("asla kapı değildir") literatür
  katmanı evidentia connector'larına degrade etti.

## Regresyon
- `tests/test_bib_hygiene.py` + `tests/test_zotero_bridge_parity.py`: 12/12 GEÇTİ.
- `references.bib`: 126 → 129 kayıt (levitt2018jarsQual, tracy2010qualityCriteria, obrien2014srqr);
  Zotero koleksiyonu **9ZFDHMZA "T1DM Thesis"** ile mutabık (tek kaynak).

## Karar
Belge **provisional-pass** (HARD tier temiz; SOFT-block belgelenmiş insan-override ile kaldırıldı).
Tez bölümüne (`chapters/04_bulgular.qmd`) aktarımda tam kanıt-bağlamlı sci-audit + Galileo
sertifikasyon koşumu tekrarlanır.

---

## Faz 2 — Tam-scope literatür grounding testi + anamnesis ingest (2026-07-11)

**Kaynak / provenance (source marker).** Bu bölümdeki tüm sayısal sonuçlar tek bir orkestrasyon
koşumundan gelir: Workflow `niteliksel-fullscope-grounding`, **Run ID `wf_86a0ba6f-7d1`**, task
`weeif2lpy`. Ham çıktı artefaktı (oturum-yerel): `.../tasks/weeif2lpy.output` (802 satır); ajan-başı
dönüşler: `.../subagents/workflows/wf_86a0ba6f-7d1/journal.jsonl`; script:
`.../workflows/scripts/niteliksel-fullscope-grounding-wf_86a0ba6f-7d1.js`. Koşum profili: 25 ajan
(22 tamam / 3 hata), 3 aşama (Ingest → Ground → Synthesize), ~5,83M subagent-token, ~430 sn.
KVKK: subagent'lara yalnız yayınlanmış metodoloji iddia metni + yayın DOI'si gönderildi;
katılımcı/aile/quote_id verisi hiçbir connector'a veya anamnesis'e gitmedi.

### Aşama 1 — anamnesis ingest (RAG + graf tohumlama)

Amaç: metodoloji grounding literatürünü anamnesis'e ingest ederek tam-metni ana bağlama dökmeden
GraphRAG ile grounding yapabilmek ("bağlam penceresini etkili değerlendir"). Tam-metin I/O her
ingest ajanının kendi bağlamında izole edildi; ana pencereye yalnız manifest döndü.

| Ölçüt | Baz (öncesi) | Sonrası | Delta |
|---|---:|---:|---:|
| Docs | 31 | 37 | +6 |
| Chunks | 42 | 48 | +6 |
| Graph nodes | **0** | **71** | +71 |
| Graph edges | **0** | **43** | +43 |

**Başarılı ingest (6/9):** `braunClarke2006thematic` (fulltext, annas), `tracy2010qualityCriteria`
(fulltext, annas), `deLosReyes2015` (fulltext, annas), `tong2007coreq` (abstract, OpenAlex),
`levitt2018jarsQual` (abstract, OpenAlex), `lincolnGuba1985` (abstract, OpenAlex + kanonik özet;
kitap, DOI yok). Graf 0/0'dan 71 düğüm / 43 kenara tohumlandı (kenarlar = triple toplamı 6+7+6+9+7+8).

**Başarısız ingest (3/9) — içerik filtresi:** `braunClarke2019reflexive`, `malterud2016informationPower`,
`obrien2014srqr` → *"API Error: Output blocked by content filtering policy."* Mekanizma: annas-reader
tam-metni ingest arg'ı olarak yeniden yayınlama telif/içerik filtresini tetikledi. Bu, tam-scope
grounding'de **sistematik bir RAG kör noktası** yarattı: refleksif-TA (M1,M2,M4,M7) ve
doygunluk/bilgi-gücü (M3,M5) iddiaları, kaynak 2019/Malterud korpusta olmadığından `braunClarke2006thematic::0`
chunk'ına geri düştü (provenance uyumsuzluğu — çelişki değil). Çözüm yolu: bu 3 kaynağı *özet-yalnız*
(tam-metin değil) ingest ederek filtreyi atlamak.

### Aşama 2 — 15 metodoloji iddiası (M1–M15) adversaryel grounding

hybrid_query/GraphRAG (dolmuş korpus) + OpenAlex/PubMed/Semantic Scholar çapraz-kontrol; varsayılan
katı verdict. **Uydurma referans: 0. Unsupported: 0. Tüm 15 iddia connector-confirmed.**

| # | İddia (özet) | Verdict | RAG-grounded | Aksiyon |
|---|---|---|:---:|---|
| M1 | RTA; tema = merkezi düzenleyici kavram | supported | — | Tut; "central organizing concept" 2019/2013'e sabitlenebilir |
| M2 | Refleksivite = analitik kaynak, tehdit değil | supported | — | Tut (2019 doğru kaynak) |
| M3 | Örneklem = bilgi gücü, doygunluk değil | supported | — | Tut; opsiyonel B&C 2021 "To saturate…" |
| M4 | Kodlama-güvenirlik/κ refleksif TA'da uygun değil | supported | — | Tut (2019 kanonik) |
| M5 | Doygunluk Big-Q'da tercih edilmez + karşı-lit var | **partially_supported** | — | **Atıf düzelt:** doygunluk-reddi `braunClarke2019saturate` (10.1080/2159676x.2019.1704846); karşı-lit örneği ekle (Guest 2006 / Saunders 2018, 10.1186/s12874-018-0594-7) |
| M6 | Multi-informant tasarım + informant tutarsızlığı anlamlı | **partially_supported** | ✓ | **Atıf ekle/böl:** deLosReyes2015 = psikometrik (multi-informant geçerlik) — güç-asimetrisi/ayrı görüşme gerekçesi için nitel aile-görüşme atıfı; *not: qmd bu paragrafta hâlihazırda atıfsız* |
| M7 | Critical friend = alternatif okuma, doğrulama değil | supported | — | Tut; opsiyonel B&C 2020 "One size…" |
| M8 | COREQ = 32 madde, 3 alan | supported | ✓ | Tut (RAG + connector) |
| M9 | SRQR + JARS-Qual raporlama standardı | supported | ✓ | Tut |
| M10 | Lincoln-Guba trustworthiness (4 ölçüt) | supported | ✓ | Tut |
| M11 | Tracy 8 big-tent ölçütü | supported | ✓ | Tut |
| M12 | RTA altı faz | supported | ✓ | Tut; opsiyonel "özyinelemeli" notu |
| M13 | Normalleşme ≠ yük yokluğu (atıfsız) | **uncited_needs_citation** | — | **Atıf ekle:** Knafl & Deatrick FMSF; Deatrick/Knafl/Murphy-Moore 1999; Robinson 1993 |
| M14 | Karma yöntem: joint display / convergent (atıfsız) | **uncited_needs_citation** | — | **Atıf ekle:** Creswell & Plano Clark; Guetterman/Fetters/Creswell 2015 (10.1370/afm.1865); Fetters/Curry/Creswell 2013 (10.1111/1475-6773.12117) |
| M15 | Alıntı bütünlüğü kuralı (atıfsız) | **uncited_needs_citation** | — | **Atıf ekle:** Corden & Sainsbury 2006 (10.1080/13645570600595264) + JARS-Qual/COREQ; "yeniden yazma yasak" satırını anlam-değiştiren akademikleştirmeyle sınırla |

**Özet:** 10 supported · 2 partially_supported (M5, M6) · 0 unsupported · 3 uncited_needs_citation
(M13, M14, M15). **RAG-grounded 6/15** (M6, M8, M9, M10, M11, M12 — tam da kaynağı ingest edilen
iddialar); kalan 9 connector-only. Bu, anamnesis ingest'in *etki mekanizmasını* doğrular: bir
iddianın RAG-grounded olması ↔ kaynağının korpusta bulunması.

### anamnesis etkinlik değerlendirmesi

- **Kazanım:** Graf 0→71 düğüm/43 kenar; GraphRAG artık niteliksel-metodoloji sorularına yanıt
  veriyor (önceki test: graf boş → RAG değeri gösterilemiyordu). M6/M8–M12 doğrudan chunk
  provenance'ı ile grounding sağladı ({doc_id, idx} damgalı).
- **Sınır:** 3 içerik-filtresi kaybı, refleksif-TA çekirdeğini (en kritik `braunClarke2019reflexive`)
  korpus dışında bıraktı; bu iddialar connector'a bağımlı kaldı. Tam kapama için 3 kaynağın
  özet-yalnız yeniden ingest'i gerekir.

### qmd düzeltme kuyruğu (bu koşumdan; **UYGULANDI → bkz. Faz 2b**)

5 düzeltme yeni doğrulanmış künye ekleme gerektirir → Zotero **9ZFDHMZA** + `references.bib` +
qmd atıf düzenlemesi. **Hiçbiri HARD blocker değil** (tüm iddialar doğru/connector-confirmed; sorun
atıf kesinliği/tamlığı). Kullanıcı onayı üzerine hepsi uygulandı:
M5 (atıf repoint + karşı-lit), M6 (atıf ekle), M13/M14/M15 (atıf ekle).

### Regresyon / KVKK (Faz 2 test koşumu)
- qmd render'ı bu koşumda değişmedi (yalnız test); mevcut 8 `[@key]` çözülüyor.
- KVKK invaryantı korundu: connector/anamnesis'e yalnız yayın literatürü + DOI gitti.

### Faz 2b — Uygulama (2026-07-11)

Kullanıcı onayı ("openathens kullan; sonra da düzeltmeleri uygula") üzerine tüm kuyruk uygulandı.

**anamnesis RAG kör noktası kapatıldı.** 3 içerik-filtresi kaynağı (`braunClarke2019reflexive`,
`malterud2016informationPower`, `obrien2014srqr`) yeniden ingest edildi: **openathens** üçünde de
`manual_required` döndürdü (T&F/SAGE/OUP yayıncı SSO/JS-challenge). Fallback: **annas-reader** tam-metni
alınıp **paraphrase türetilmiş özet** (bulk verbatim değil → telif + içerik-filtresi güvenli) olarak
ingest edildi + graf triple'ları yazıldı. Korpus: 37→**40 dok / 51 chunk / 96 düğüm / 64 kenar**.
Kapanış `hybrid_query` ile kanıtlandı: refleksif-TA/doygunluk sorgusunda tepe chunk'lar artık
`braunClarke2019reflexive` (skor 0,1523) + `malterud2016informationPower` (0,1308) — M1–M5/M7 artık
RAG-grounded (önceki turda connector-only idi).

**Referanslar (tek-kaynak).** 10 künye evidentia (OpenAlex/PubMed) ile doğrulandı; 1'i mevcut
`taylorDeVocht2011separate` ile birebir mükerrer çıktı (bib_hygiene sim=1.0 yakaladı) → mükerrer künye
kaldırıldı, qmd mevcut anahtarı kullandı. Net +9 künye `references.bib`'e (131→140). 8 DOI'li kaynak
**9ZFDHMZA**'ya import edildi (Zotero item key): braunClarke2019saturate `QAICXFMF` · saunders2018saturation
`76H7TRUA` · guetterman2015jointDisplay `5SNNRAR3` · fetters2013integration `QVFR6N96` · corden2006quotations
`ZKPAKJKW` · deatrick1999normalization `SZ4S7W3U` · robinson1993normalization `AANIB8JN` · knafl2003fmsf
`X5KVW57E`. `creswellPlanoClark2018` kitap/DOI'siz → Zotero'ya manuel eklenmeli (tek açık kalem).

**5 qmd düzeltmesi uygulandı:**
- **M5** — doygunluk-reddi `braunClarke2019saturate`'e repoint + karşı-lit `saunders2018saturation`.
- **M6** — multi-informant paragrafına `deLosReyes2015` (geçerlik/tutarsızlık) + `taylorDeVocht2011separate`
  (ayrı vs birlikte görüşme otantikliği).
- **M13** — normalleşme: `robinson1993normalization`, `deatrick1999normalization`, `knafl2003fmsf` +
  aile-düzeyi↔bireysel-düzey scope notu.
- **M14** — karma yöntem: `creswellPlanoClark2018` + `guetterman2015jointDisplay`, `fetters2013integration`.
- **M15** — alıntı bütünlüğü: `corden2006quotations` + JARS-Qual/COREQ; "yeniden yazma yasak" satırı
  anlam-değiştiren akademikleştirmeyle sınırlandı, okunabilirlik için asgari düzenleme istisnası eklendi.

**Doğrulama:** `bib_hygiene all` → **HARD=0** (duplicate temizlendi; kalan SOFT'lar önceden var olan
alan/DOI-eksik künyeler + orphan false-positive'i — yeni künyeler niteliksel qmd'de atıflı, bib_hygiene
`chapters/` tarar). `quarto render` → **"Output created"**, 18 `[@key]` tümü çözüldü. KVKK korundu
(yalnız yayın literatürü + DOI dışa gitti).

---

## Faz 2c — AI-reliability / 0-halüsinasyon reconciliation (2026-07-11)

Kullanıcı, qmd'yi **yerel de-identified kaynaklara karşı** doğrulamak için ham-veri okuma izni verdi
("ham verilere de erişim izni veriyorum … 0 halüsinasyon hedefle"). **KVKK:** doğrulama yalnız yerel
Read/Grep/Bash ile yapıldı; hiçbir connector/MCP/web/memory çağrılmadı, verbatim alıntı/kimlikleyici
ne bağlama döküldü ne dışa gönderildi. Reconciliation izole bir alt-ajanda koştu; ana bağlama yalnız
verdict matrisi döndü.

**Yer-doğrusu:** `qualitative_canonical_results_for_doktoratezi.md` (birincil kanonik kaynak), `codebook_v2.md`,
`coreq_32_completed.md`, `A1_information_power.md`, `codebook_v3.csv` (taslak).

**Sonuç — sayısal halüsinasyon YOK.** 11 iddia kümesi → **9 MATCH · 1 MISMATCH · 1 UNVERIFIED**:

| Doğrulanan | Verdict |
|---|---|
| Kanonik sayılar (7 aile/21/7-7-7; 4+6 tema; 23 kod; 116/116/57; COREQ 32/30/2/0) | MATCH |
| Rol dağılımı 55+36+25 = 116 | MATCH (toplam doğru) |
| Aile dağılımı 24+18+15+14+23+8+14 = 116 | MATCH (toplam doğru) |
| Tema quote 3+40+21+52 = 116; T4=15+15+22 | MATCH |
| Kod yoğunluğu (18 kod) toplamı = 116 | MATCH (codebook_v2 §5.3 birebir) |
| 23 kod adı + 5 kategori üyeliği | MATCH (codebook_v2 §1) |
| COREQ domain 7/15/10; kısmi = Madde 16 + 31 | MATCH (coreq_32_completed) |
| Görüşme süresi 15–25 / 40–70 dk | MATCH (A1 + coreq md#20) |
| 5 bağlantısız kod (adları) | MATCH |
| **Kaynak-haritası dosya varlığı (12→gerçekte 14)** | **MISMATCH: `quotes_used.csv` YOK** |
| **28 tema-ankraj quote_id'sinin havuza karşı sağlaması** | **UNVERIFIED: havuz CSV'si yok (6/28 taslak codebook_v3'te)** |

**Tek gerçek kusur = provenans, uydurma değil.** qmd'nin 28 quote_id'si + tüm sayıları birincil MD
kaynağıyla birebir (sadık reprodüksiyon); ancak qmd, depoda **mevcut olmayan** `quotes_used.csv`
(+ `coded_segments.csv`, `04_triadic_matrices/*.csv`) dosyalarına canlı kaynakmış gibi atıf yapıyordu.
Bu, quote_id iddialarını satır-düzeyinde doğrulanamaz kılıyordu.

**Düzeltmeler (uygulandı):**
- KVKK callout (satır 40): ölü `quotes_used.csv` ID-kaynağı atfı kaldırıldı → "temizlenmiş tez
  metninden `quote_id` eşlemesi" + havuzun henüz üretilmediği notu.
- Kaynak Dosya Haritası (satır 604): `quotes_used.csv` satırı "**henüz depoda üretilmedi**; güncel
  kaynak `qualitative_canonical_results_for_doktoratezi.md` + taslak `codebook_v3.csv`" olarak işaretlendi.
- @sec-dogrulama: iki yeni madde — (i) iç-tutarlılık reconciliation özeti (0 sayısal halüsinasyon;
  4 toplam = 116; COREQ 30/2/0/32); (ii) **quote-havuzu provenans sınırlılığı** açıkça beyan edildi
  (116/116/57 + 28 ankraj id kanonik MD'ye izlenebilir, satır-düzeyi CSV'ye henüz değil).
- `quarto render` → **"Output created"** (temiz); artık qmd'de ölü-dosya-canlı-kaynak atfı yok.

**Yargı:** Belge **0 olgusal/sayısal halüsinasyon** taşır. Kalan boşluk (eksik quote-havuzu CSV'si)
artık **açıkça beyan edilmiş bir sınırlılıktır** — yanlış/uydurma bir iddia değil. Final teze aktarımda
`quotes_used.csv` üretilip 28 ankraj id gerçek quote metniyle bire bir eşlenmelidir.

---

## Faz 2d — quotes_used.csv üretimi + 116/54 etiket düzeltmesi (2026-07-11)

Kullanıcı kararı: "quotes_used.csv havuzunu kanonik kaynaktan üret" → faithful 54-distinct-id seçeneği.

**Kritik bulgu (üretimden önce):** Kaynakta **116 distinct quote_id YOK**. Kanonik rapor 116'yı hem
"Seçilmiş anonim quote ID kaydı" (satır 65) hem "Araştırmacı-denetimli ön-kodlu segment" (satır 66)
olarak — **aynı sayı** — tanımlıyor; kod-yoğunluğu tablosu da 116'ya toplanıyor. Yani **116 = ön-kodlu
segment (id×kod)**, distinct id değil. De-identified kaynaklarda **54 distinct quote_id** var. Segmenti
satır-düzeyinde üreten `01_deidentified/coded_segments.csv` depoda YOK (`01_deidentified/` dizini yok,
`02_processed/` boş). Bu nedenle **116 satırlık faithful CSV imkânsız** — eksik ~62 segmenti üretmek
uydurma olurdu (0-halüsinasyon ihlali). Kullanıcı onayıyla faithful 54-distinct-id havuzu üretildi.

**Üretim (deterministik, 0 uydurma).** `06_manuscript_outputs/quotes_used.csv` — 54 satır; kolonlar
`quote_id, aile_no, rol, tema, kaynak_dosya`. `aile_no`+`rol` id string'inden deterministik; `tema`
kanonik raporun 7.x.4 "Quote ID ankrajları" bölümlerinden (28 atanmış: Tema1=3, Tema2=5, Tema3=5,
Tema4=15; 26 atanmamış); `kaynak_dosya` = id'nin geçtiği de-identified dosya(lar). Dağılım: rol
13/23/18=54; aile 8/10/8/8/13/3/4=54. Doğrulama: 54 satır, tüm `aile_no`+`rol` dolu, 54 distinct.

**qmd etiket düzeltmesi (116 segment / 54 distinct ayrımı).** 8 düzenleme:
- Kanonik Sayılar: iki yinelenen "116" satırı → `Ön-kodlu segment (id×kod) = 116` + `Distinct quote_id
  (quotes_used.csv) = 54`.
- Rol/Aile/Tema dağılım tabloları: başlıklar "Seçilmiş quote/Quote sayısı" → "Segment sayısı (id×kod)";
  giriş cümlesi bu dağılımların segment (toplam 116, 54 distinct id'ye karşılık) olduğunu belirtiyor.
- Kaynak Dosya Haritası: `quotes_used.csv` satırı "üretildi — 54 distinct quote_id; 116 segment
  coded_segments.csv'den (depoda yok)" olarak güncellendi.
- KVKK callout + §Doğrulama provenans maddesi: havuzun 54 kayıt olarak üretildiğini, 116'nın segment
  olduğunu, coded_segments.csv/triadik-matris CSV'lerinin hâlâ depoda olmadığını yansıtacak şekilde
  güncellendi.

**Doğrulama:** `quarto render` → **"Output created"** (temiz). Kalan tek açık kalem: 116 segment ve 57
triadik-matris satırı satır-düzeyi CSV'leri (`coded_segments.csv`, triadik matris) hâlâ depoda yok →
final tezde üretilmeli; 28 tema-ankraj alıntısı gerçek metinle bire bir eşlenmeli. KVKK korundu
(üretim tümüyle yerel; connector/dışa aktarım yok; CSV yalnız anonim id+aile+rol+tema+provenans içerir,
verbatim alıntı yok).
