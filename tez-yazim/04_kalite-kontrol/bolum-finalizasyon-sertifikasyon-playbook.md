# Bölüm Finalizasyon Sertifikasyon Playbook'u

Bu playbook, yazılmış veya yazıma hazır her tez bölümünün final kabulünden
önce çalıştırılacak zorunlu sertifikasyon sürecidir. Amaç, bölüm metninin
yalnız dil açısından değil; kaynak evreni, tam metin erişimi, Zotero
mutabakatı, semantik kanıt değerlendirmesi, resmi kılavuz uyumu, Türkçe
akış ve AI-reliability açısından kapatılmasıdır.

Bir bölüm bu süreç uygulanmadan, sertifika raporu üretilmeden ve uygulama
onayı alınmadan **finalize kabul edilmez**.

## Sertifikasyon Durumları

| Durum | Anlam |
|---|---|
| `draft` | Bölüm yazılıyor; sertifikasyon başlamadı. |
| `certification-running` | Sertifikasyon kapıları çalışıyor; metin final değildir. |
| `blocked` | En az bir kritik kapı başarısız veya eksik. |
| `provisional-pass` | Teknik kapılar geçti; kullanıcı/danışman uygulama onayı bekleniyor. |
| `certified-final` | Tüm kapılar geçti ve açık uygulama onayı alındı. |

## Sertifika Artefaktı

Her bölüm için bir sertifika raporu oluşturulur:

```text
tez-yazim/04_kalite-kontrol/sertifikalar/<bolum-kodu>-sertifika-YYYY-MM-DD.md
```

Örnek:

```text
tez-yazim/04_kalite-kontrol/sertifikalar/01-giris-ve-amac-sertifika-2026-07-01.md
```

Rapor, `bolum-finalizasyon-sertifikasi-sablonu.md` şablonundan üretilir ve
komut çıktıları, kaynak listesi, Zotero key'leri, ledger satırları, AI audit
sonuçları ve nihai karar alanlarını içerir.

## Kapı 0: Kapsam ve Hassasiyet Sınırı

Amaç: Sertifikasyonun hangi bölüm, hangi iddia seti ve hangi veri sınırı için
çalışacağını kesinleştirmek.

1. Bölüm dosyası belirlenir: `chapters/<bolum>.qmd`.
2. İlgili hazırlık briefi okunur:
   `tez-yazim/03_bolum-hazirlik/<bolum>.md`.
3. Resmi kaynaklar okunur:
   `docs/tez-kilavuz/` ve `tez-yazim/00_kaynak-kurallari/`.
4. Kritik kaynak manifesti okunur:
   `tez-yazim/06_kritik-kaynaklar/README.md` ve
   `tez-yazim/06_kritik-kaynaklar/kritik-dosya-manifesti.tsv`.
5. Ham veri, ham transcript, satır düzeyi klinik veri, `.env`, credential ve
   aile düzeyi hassas içerik sertifikasyon bağlamına taşınmaz.

Bloklayıcılar:

- Bölüm dosyası veya hazırlık briefi yok.
- Bölümün hangi resmi ana bölüme karşılık geldiği belirsiz.
- Ham veri veya credential içerik rapora alınmış.

## Kapı 1: Derin Literatür ve Künye Evreni Denetimi

Amaç: Bölümdeki dış literatür iddialarının bağlama uygun tüm ana veri
tabanlarında aranmış, künyelenmiş, elenmiş ve semantik olarak irdelenmiş
olduğunu kanıtlamak.

Zorunlu çekirdek:

- Evidentia `medical-research` D0-D6.
- PubMed/EPMC.
- OpenAlex.
- Semantic Scholar.
- Paper Search.
- PsyArXiv/OSF, eğer preregistration, preprint veya açık bilim bağlamı varsa.
- YÖK Tez, Türkiye bağlamı veya ulusal boşluk iddiası varsa.
- ERIC, okul/eğitim/gelişim/akademik uyum iddiası varsa.
- Mevzuat/TİTCK/terminoloji/life-science araçları yalnız açık görev sinyali
  varsa.

Çıkışlar:

1. `coverage_set`: hangi veri tabanları çalıştı, hangileri görev dışı kaldı.
2. `query_matrix`: Türkçe/İngilizce dar, geniş, lateral ve ölçüm-odaklı
   sorgular.
3. `candidate_sources`: DOI/PMID/PMCID/OpenAlex ID/YÖK ID dahil aday havuzu.
4. `excluded_sources`: dışlama gerekçeleri.
5. `semantic_adjudication`: popülasyon, yaş, ölçüm, çalışma türü, yöntem
   kalitesi, T1DM uyumu, Türkiye aktarılabilirliği ve çelişki değerlendirmesi.

PASS koşulu:

- Bölümdeki her dış claim en az bir doğrulanmış künye satırına bağlıdır.
- Sadece abstract düzeyinde kalan claim kritik ise Kapı 2'ye full-text adayı
  olarak aktarılmıştır.
- Dışlanan önemli kaynaklar gerekçeli listelenmiştir.

## Kapı 2: Tam Metin, Zotero ve Bağlam Yönetimi Denetimi

Amaç: Her citation adayının tam metninin uygun rota ile bulunması, Zotero'ya
bağlanması ve semantik olarak değerlendirilmesidir.

Tam metin sırası:

1. OpenAthens / Cumhurbaşkanlığı Millet Kütüphanesi kurumsal yayıncı erişimi.
2. Anna's Library / annas-reader.
3. PubMed Central, Europe PMC, OpenAlex/Unpaywall, yayıncı OA sayfası.
4. Kurumsal repository, author accepted manuscript, kütüphane kaynak sağlama
   veya yazar talebi.
5. Hiçbiri başarılı değilse `full-text-exception`; final citation için
   kullanıcı/danışman kararı gerekir.

Zotero kapanışı:

```bash
cd /workspaces/T1DM-Tez
python3 scripts/util/zotero_env_bridge.py status --json
python3 scripts/util/zotero_env_bridge.py import-doi <DOI> \
  --bibtex-key <citation_key> \
  --fulltext-url '<publisher_or_openathens_url>' \
  --attachment-file <local_fulltext_or_snapshot.pdf> \
  --note '<provenance>' \
  --json
```

Bağlam ve semantik inceleme:

- Büyük tam metin veya çok kaynaklı corpus gerekiyorsa Anamnesis/context
  kapısı kullanılır.
- Tam metin RAG'e veya bağlama ham olarak dökülmez; hedefli pasaj, tablo,
  bölüm, endpoint ve yöntem notu çıkarılır.
- `evidence_index`, `fulltext_extracts` veya eşdeğer lokatör tutulur.
- Her claim için "kaynak, popülasyon, ölçüm, sonuç, sınırlılık, tezde kullanım"
  denetimi yapılır.

PASS koşulu:

- Her citation adayı ledger'da DOI/PMID/ID, full-text route, Zotero item key,
  attachment/note key, BibTeX key ve claim notuyla görünür.
- `references/references.bib` içinde kullanılan citation key vardır.
- Tam metin görülmeyen kaynak `cite-ok` değildir.

## Kapı 3: Bölüm Metni, Kılavuz ve İç Tutarlılık Denetimi

Amaç: Bölümün resmi tez kılavuzu, bölüm işlevi ve repo kanıtlarıyla uyumlu
olduğunu kanıtlamak.

Kontrol eksenleri:

1. Resmi başlık ve bölüm sırası.
2. Bölümün beklenen işlevi:
   - `GİRİŞ ve AMAÇ`: problem, boşluk, gerekçe ve amaç.
   - `GENEL BİLGİLER`: kuramsal ve ampirik arka plan.
   - `GEREÇ ve YÖNTEM`: tasarım, örneklem, ölçüm, analiz ve etik.
   - `BULGULAR`: yorumsuz sonuç sunumu.
   - `TARTIŞMA ve SONUÇ`: yorum, literatürle karşılaştırma, sınırlılık,
     sonuç ve öneriler.
3. H1-H5, Faz II/post-hoc, nitel RTA ve karma yöntem amaçlarının karışmaması.
4. Her repo-içi iddianın CSR, protokol, SAP, veri haritası, form veya güvenli
   nitel rapora bağlı olması.
5. Quarto citation biçimi ve `references.bib` mutabakatı.
6. Tablo/şekil başlık, numara, metin içi gönderim ve kaynak uyumu.

PASS koşulu:

- Bölüm resmi işlevini eksiksiz yerine getirir.
- Kılavuzla çelişen başlık, format, sayı yazımı veya kaynak biçimi yoktur.
- Bölüm metni ile ledger, `references.bib` ve kanıt haritası arasında orphan
  citation veya orphan claim kalmaz.

## Kapı 4: Türkçe İmla, Anlam Akışı ve Mantık Denetimi

Amaç: Bölümün Türkçe akademik anlatım, mantık akışı ve okur deneyimi açısından
son okumasını yapmak.

Kontrol eksenleri:

- Yazım ve noktalama.
- Türkçe karakterler, terim tutarlılığı, kısaltma ilk kullanımı.
- Cümle uzunluğu ve belirsiz zamirler.
- Paragraf geçişleri: genelden özele, yöntemden bulguya, bulgudan tartışmaya
  uygun akış.
- Tekrarlı iddia, gereksiz literatür yükü, bölüm dışına taşan içerik.
- Nedensellik, genelleme ve klinik öneri sınırlarının doğru etiketlenmesi.
- Ondalık virgül, `p` yazımı ve istatistik birimlerinin tutarlılığı.

Zorunlu imla/yazım denetimi — **sci-audit plugin axis G** (kanonik araç):

```bash
# İnteraktif (birincil):
/sci-audit:check-turkish chapters/<bolum>.qmd --strictness certification

# Deterministik CLI (CI/rapor üretimi; plugin-bundled tr_sciaudit.py):
SCIA="$(ls -d $HOME/.claude/plugins/cache/cureonics-marketplace/sci-audit/*/ | sort -V | tail -1)"
python3 "${SCIA}skills/turkish-sci-style/scripts/tr_sciaudit.py" chapters/<bolum>.qmd \
  --strictness certification --format md --fail-on error \
  --terms "diyabet,depresyon,ebeveyn,kardeş,ölçek,yöntem" \
  --out tez-yazim/04_kalite-kontrol/raporlar/<bolum>-tr-sciaudit.md
```

Bu, `sci-audit@cureonics-marketplace` plugin'inin axis G (Türkçe bilimsel
yazım/imla) deterministik çekirdeğidir; dış API'ye metin göndermez, her yerde
(claude.ai web dahil) çalışır. Ayrıntı ve provider (TDK/Zemberek/GECTurk/
style-judge) davranışı: `tez-yazim/04_kalite-kontrol/turkce-bilimsel-yazim-denetimi.md`.
İngilizce ondalık-nokta `p` değeri Türkçe metinde **blocker**tır (G5).

PASS koşulu:

- Bölüm okunabilir, tutarlı ve bütünlüklüdür.
- Anlam akışında kopukluk veya çelişki yoktur.
- İmla ve terim tutarlılığı final metin düzeyindedir.
- sci-audit axis G raporunda `error` (blocker) yoktur; `warning` (major)
  bulguları düzeltilmiş veya sertifika raporunda gerekçeli kabul edilmiştir.

## Kapı 5: AI-Reliability, Render ve Repo Doğrulaması

Amaç: Bölümün gizlilik, claim grounding, araç politikası ve üretilebilirlik
açısından otomatik/yarı otomatik denetimlerden geçmesidir.

Bu kapı **iki ayrı, çakışmayan katman** çalıştırır (görev sınırı Bölüm
"AI-Reliability Katman Sınırı"nda):

1. **Manüskript adli denetimi — `sci-audit` plugin (axes A–F).** Bölüm metninin
   referans bütünlüğü, claim grounding, istatistik iç-tutarlılığı, halüsinasyon
   sinyalleri, raporlama-kılavuzu uyumu (COREQ/PRISMA/STROBE…) ve AI-şeffaflık
   denetimi.
2. **Repo/veri invaryant denetimi — repo-özel ai-audit plugin'leri.** KVKK/ham
   veri sınırı, quote-parity, kanonik kilit ve araç politikası — bunlar
   `sci-audit` kapsamı **dışıdır** ve orada tekrarlanmaz.
3. **Bağımsız judge — `galileo-audit` (model çeşitliliği).** Katman 1'in yanında,
   Roche-içi GPT-5.4 judge + gemini-embedding-001 semantik-tutarlılık bağımsız bir
   ikinci-görüş verir (tek-model korelasyonlu hatalarını kırar). **three-tier gate:**
   **HARD** (sci-audit A–G ve repo invaryantları — değişmez) / **SOFT-block**
   (groundedness/faithfulness < 0,60 · `citation_support=unsupported` · bölümler-arası
   çelişki · büyük Claude↔GPT bütünlük çelişkisi → bölüm en fazla `provisional-pass`;
   `certified-final` yalnız düzeltme **veya** sertifika-defterine yazılan açık insan
   **override gerekçesiyle**) / **advisory** (bib-dup, tekrar, üslup — yalnız rapor).
   KVKK: gateway'e yalnız manuskript/literatür. Doktrin: `manuskript-denetimi-sciaudit.md` §6;
   yapılandırma `.claude/galileo.local.md`.

Zorunlu komutlar, bölümün temasına göre daraltılmadan çalıştırılır:

```bash
# 0) Bib-hijyen denetimi — three-tier gate:
#    HARD (atıflı-tanımsız key → render kırar): kapı açılmaz
#    SOFT (alan/DOI/dup eksikliği): not düşülür, devam edilir
#    advisory (orphan key): yalnız rapor
python3 scripts/util/bib_hygiene.py all

# 1) Manüskript adli denetimi (sci-audit — axes A-F; Türkçe ise G Kapı 4'te koşuldu)
/sci-audit:audit chapters/<bolum>.qmd --lang tr --strictness certification --type <coreq|strobe|prisma|jars>
# ardından raporu birleştir:
/sci-audit:audit-report --out tez-yazim/04_kalite-kontrol/raporlar/<bolum>-sci-audit.md
# harici MCP/kanıt kullanımı olduysa:
/sci-audit:ai-log "<bolum> sertifikasyon sci-audit koşumu"

# 2) Repo/veri invaryant denetimi (KVKK, ham veri, quote-parity — sci-audit DIŞI)
cd /workspaces/T1DM-Tez/niteliksel
./dmnitel ai-context
./dmnitel route-tool --query "<bolum> sertifikasyon kaynak ve araç kapıları"
PYTHONDONTWRITEBYTECODE=1 python3 plugins/t1dm-qual-ai-audit/skills/t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py

cd /workspaces/T1DM-Tez
PYTHONDONTWRITEBYTECODE=1 python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/test_repo_ai_reliability.py
python3 scripts/util/zotero_env_bridge.py status --json
git diff --check -- chapters/<bolum>.qmd references/references.bib tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md
quarto check
```

Koşullu komutlar:

- `quarto render thesis.qmd`: bölüm değişikliği citation, cross-reference,
  tablo/şekil, front matter veya render çıktısını etkiliyorsa.
- `Rscript tests/test_*.R`: bölümde nicel sonuç, tablo, veri kilidi veya analiz
  iddiası değiştiyse.
- `./dmnitel check-quotes`, `./dmnitel audit-coreq`: nitel alıntı, COREQ,
  RTA yöntem veya nitel bulgu metni değiştiyse.
- `npx promptfoo@latest eval -c reliability/evals/promptfooconfig.yaml`:
  AI guardrail, prompt, policy veya reliability dosyası değiştiyse.

**BULGULAR (`04_bulgular.qmd`) ve TARTIŞMA (`05_tartisma_ve_sonuc.qmd`) bölümlerine
özel — karma sentez drift-guard (zorunlu):**

```bash
# Karma kanıt-ledger drift-guard — BULGULAR ve TARTIŞMA bölüm sertifikasyonu için ZORUNLU
PYTHONDONTWRITEBYTECODE=1 python3 scripts/util/karma_ledger_check.py
```

Çıkış kodu yorumu:

| Çıkış kodu | Anlam | Sertifikasyon kararı |
|---|---|---|
| `0` | Temiz — HARD bulgu yok | Devam edilir |
| `1` | **HARD bulgu var** (severity=1) | **Bölüm sertifikasyona KAPALI** — ledger/sentez belgesi düzeltilmeden PASS yok |
| `2` | SOFT bulgu var (severity=2), HARD yok | `provisional-pass` mümkün; her SOFT bulgusu sertifika raporunda gerekçelendirilir |

**HARD=0 (exit 0 veya exit 2) olmadan bölüm `certified-final` sayılmaz.** SOFT
bulguları (exit 2) sertifika defterinde madde madde gerekçeli kabul edilirse
`provisional-pass` verilebilir; `certified-final` için düzeltme gereklidir.
Checker referans dosyaları: `tez-yazim/05_entegrasyon/karma-kanit-ledgeri.tsv`
(kanıt-ledger) ve `tez-yazim/05_entegrasyon/karma-sentez-kanonik.md` (sentez
belgesi); bu iki dosya değişirse checker yeniden çalıştırılır.

PASS koşulu:

- **sci-audit** axes A–F raporunda blocker yok; her eksen ne denetlediğini/neyi
  denetlemediğini beyan etmiş (no-fabrication invaryantı).
- Nitel ve nicel **repo/veri** AI-reliability komutları (KVKK/ham veri/quote-
  parity) geçer.
- `git diff --check` temizdir.
- `quarto check` geçer; gerekli durumda render geçer.
- Harici MCP/plugin kullanımı varsa AI-use log güncellenmiştir (`/sci-audit:ai-log`
  ve/veya `./dmnitel log-ai-use`).

## AI-Reliability Katman Sınırı (duplikasyon önleme)

| Katman | Araç | Kapsam | Kapsam DIŞI |
|---|---|---|---|
| Manüskript adli denetimi | `sci-audit@cureonics-marketplace` (axes A–G) | Referans bütünlüğü (A), claim grounding (B), istatistik iç-tutarlılığı (C), halüsinasyon sinyalleri (D), raporlama-kılavuzu uyumu (E), AI-şeffaflık (F), **Türkçe imla/yazım (G)** | Ham veri/KVKK sınırı, quote-parity, kanonik kilit — bunları denetlemez |
| Repo/veri invaryantı | `t1dm-qual-ai-audit` + `doktoratezi-ai-audit` | KVKK/ham veri guard, quote-parity, kanonik lock, repo araç politikası | Manüskript metni adli denetimi (citation/claim/stat/imla) — bunları denetlemez |

İki katman **çakışmaz**: metin adli denetimi yalnız `sci-audit`'te, veri/gizlilik
invaryantı yalnız repo plugin'lerinde yürür. Aynı işlev iki yerde tekrarlanmaz.

## Nihai Karar Kuralı

Bir bölüm yalnız şu koşulların tamamı sağlanırsa `certified-final` olur:

1. Kapı 0-5 tamamı PASS.
2. Sertifika raporu oluşturuldu.
3. Ledger'da ilgili bölüm için `full-text-pending`, `zotero-pending`,
   `reliability-pending`, `citation-without-full-text` kalmadı.
4. Bölümdeki her citation `references.bib` ve Zotero ile mutabık.
5. Kullanıcı/danışman uygulama onayı açıkça verildi.

Uygulama onayı yoksa en iyi durum `provisional-pass`tir; bölüm final kabul
edilmez.

## Bloklayıcı Hata Sözlüğü

| Bloklayıcı | Çözüm |
|---|---|
| `coverage-gap` | Eksik veri tabanı veya koşullu MCP çalıştırılır; gerekçe yazılmadan PASS yok. |
| `full-text-gap` | OpenAthens/Anna/OA/repository sırası tekrar denenir veya kaynak dışlanır. |
| `zotero-gap` | Item, attachment/note ve BibTeX key tamamlanır. |
| `orphan-claim` | Claim kaynakla bağlanır veya metinden çıkarılır. |
| `orphan-citation` | Citation ledger/BibTeX/Zotero zincirine bağlanır veya çıkarılır. |
| `format-gap` | Resmi kılavuz ve format kontratıyla düzeltilir. |
| `privacy-gap` | Ham veri, transcript, credential veya hassas ayrıntı çıkarılır. |
| `reliability-gap` | AI-reliability bulgusu düzeltilir ve test yeniden çalıştırılır. |
| `approval-gap` | Açık uygulama onayı alınmadan final statüsü verilmez. |
| `karma-ledger-hard` | BULGULAR/TARTIŞMA: `karma_ledger_check.py` exit 1 (HARD bulgu). Ledger ve/veya sentez belgesi düzeltilir; checker yeniden çalıştırılır, exit 0 olmadan PASS yok. |
