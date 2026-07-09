# Tez Yazım Ana Planı

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans`
> to implement this plan task-by-task. For independent literature, methods,
> results, and appendix work packages, `superpowers:subagent-driven-development`
> may be used with one fresh subagent per package, followed by main-agent review.
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resmi Marmara tez kılavuzu, nicel `doktoratezi` repo kanıtları ve
nitel `T1DM Niteliksel` repo çıktılarıyla uyumlu, kaynak izlenebilir, gizlilik
sınırı korunmuş ve Quarto ile üretilebilir bir karma doktora tezi yazım süreci
kurmak.

**Architecture:** Yazım süreci L0 resmi kılavuz, L1 nicel repo, L2 nitel repo,
L3 dış kanıt ve L4 teknik doğrulama katmanlarına ayrılır. Her bölüm önce
`tez-yazim/03_bolum-hazirlik/` içinde planlanır, sonra ilgili `chapters/*.qmd`
dosyasına kontrollü aktarılır. Her aktarım repo kanıt haritası, kaynakça
mutabakatı, gizlilik kontrolü, Quarto/R doğrulaması ve bölüm finalizasyon
sertifikasıyla kapatılır.

**Tech Stack:** Quarto, R, `targets`, `renv`, `dmnitel`, Anamnesis/context
management gate, Evidentia MCP çekirdeği, PubMed/OpenAlex/Paper Search,
OpenAthens kurumsal yayıncı erişimi, Anna's Library full-text fallback,
Zotero Web API bridge, bölüm finalizasyon sertifikasyon playbook'u, iki repo
AI-reliability kontrolü, promptfoo, Marmara resmi tez kılavuzu ve şablonları.

---

## 0A. Ana Çalışma Merkezi Kararı

1. Tez yazım süreci bundan sonra `/mnt/thunderbolt/workspaces/doktoratezi`
   reposunda yürütülür.
2. Ana operasyon alanı `tez-yazim/`; gerçek üretim hedefleri `thesis.qmd`
   ve `chapters/*.qmd` dosyalarıdır.
3. Nitel repo yetkinlikleri yalnız nitel kolun ilgili tez kesimleri
   yazılırken açılır: yöntem, bulgular, joint display, tartışma, ekler,
   COREQ/audit trail, anonim alıntı bütünlüğü ve nitel AI-reliability.
4. Doktoratezi içine transfer edilmiş kanonik nitel sonuç raporu, nitel
   repoyu temsil eden varsayılan kaynak katmanıdır.
5. Dış literatürde Evidentia paketi en geniş kapsamlı ana kanıt motorudur;
   OpenAthens full-text, Anna's fallback, PubMed/OpenAlex/Paper Search, Zotero
   ve referans ledger kapıları bu hattı tamamlar.
6. Klinik/nitel sonuç raporları, protokol, ham/kilitli veri ve ölçek-form
   dosyaları `tez-yazim/06_kritik-kaynaklar/` manifesti üzerinden seçilir;
   bu dosyalar yazım alanına kopyalanmaz.

## 0. Ana İlkeler

1. Resmi yazım otoritesi `docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf` ve
   `docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx` dosyalarıdır.
2. Repo içi analiz, yöntem ve veri yönetişimi kararlarında `CLAUDE.md`,
   `AGENTS.md`, `_targets.R`, `docs/protokol/`, `docs/analiz_planlari/`,
   `docs/niteliksel/` ve `chapters/` kaynakları kullanılır.
3. Nitel repo yalnız güvenli türetilmiş çıktı, tema, COREQ/audit trail, LLM
   beyanı ve araştırmacı-onaylı anonim alıntı katmanında kullanılır.
4. Dış literatür iddiaları Evidentia D0-D6 kaskadıyla doğrulanır; her dış
   referans için önce OpenAthens/kurumsal yayıncı erişimi, başarısızsa
   Anna's Library, ardından PMC/OA/repository ve diğer kanıtlı rotalar
   çalışır.
5. Tam metni görülmemiş, DOI/PMID veya güvenilir bibliyografik kimliği
   doğrulanmamış ve Zotero/BibTeX kaydı mutabıklaştırılmamış kaynak tez
   metnine citation olarak girmez.
6. Referans içeren her bölüm değişikliği iki AI-reliability kapısından geçer:
   nitel repo `t1dm-qual-ai-audit` ve nicel repo `doktoratezi-ai-audit`.
7. Bağlam yönetimi için `dmnitel ai-context`, Anamnesis ve bellek/Qdrant
   araçları yalnız anonim/türetilmiş proje bağlamında kullanılır; bağlam
   çıktısı ham veri yerine karar ve kanıt düzeyinde tutulur.
8. Ham veri, transcript, satır düzeyi içerik, aile düzeyi hassas ayrıntı,
   `.env` ve credential içerikleri tez-yazım alanına taşınmaz.
9. Yazım dili Türkçedir; Summary ve gerekirse İngilizce anahtar sözcükler
   resmi şablona göre ayrıca hazırlanır.
10. Sayısal yazımda ondalık virgül kullanılır: `p=0,038`, `p<0,001`.
11. Bulgular yorumsuz; tartışma yorumlayıcı ve literatürle karşılaştırmalı
   yazılır.
12. Nitel tema nicel etki tahmini veya nedensel mekanizma gibi sunulmaz.
13. Her bölüm tamamlandığında bölüm-gate checklist’i işaretlenmeden sonraki
    bölüme geçilmez.
14. Her bölüm final kabul edilmeden önce
    `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`
    eksiksiz uygulanır, bölüm sertifika raporu üretilir ve açık uygulama
    onayı alınır. Bu üç koşul olmadan bölüm `certified-final` sayılmaz.

## 1. Dosya ve Sorumluluk Haritası

### 1.1 Plan ve Hazırlık Dosyaları

| Dosya | Rol | Dokunma biçimi |
|---|---|---|
| `tez-yazim/01_mimari/tez-yazim-ana-plani.md` | Bu ana plan. | Bu turda oluşturuldu; bölüm planları üretildikçe güncellenebilir. |
| `tez-yazim/03_bolum-hazirlik/01_giris-ve-amac.md` | Giriş ve amaç bölüm briefi. | Detay plan turunda bölüm kaynak haritasıyla genişletilecek. |
| `tez-yazim/03_bolum-hazirlik/02_genel-bilgiler.md` | Genel bilgiler bölüm briefi. | Literatür omurgası ve alt başlık kararları eklenecek. |
| `tez-yazim/03_bolum-hazirlik/03_gerec-ve-yontem.md` | Gereç ve yöntem bölüm briefi. | Nicel/nitel/karma yöntem alt planları eklenecek. |
| `tez-yazim/03_bolum-hazirlik/04_bulgular.md` | Bulgular bölüm briefi. | Tablo/şekil/joint display envanteriyle genişletilecek. |
| `tez-yazim/03_bolum-hazirlik/05_tartisma-ve-sonuc.md` | Tartışma ve sonuç bölüm briefi. | Karma yorum ve sınırlılık stratejisi eklenecek. |
| `tez-yazim/03_bolum-hazirlik/06_kaynaklar-ekler.md` | Kaynaklar ve ekler briefi. | Ek listesi, COREQ/LLM beyanı, kaynakça kontrolü eklenecek. |
| `tez-yazim/05_entegrasyon/nitel-nicel-joint-display-plan.md` | Karma yorum/joint display planı. | Bulgular ve tartışma planlarıyla eşleştirilecek. |
| `tez-yazim/06_kritik-kaynaklar/README.md` | Klinik/nitel rapor, protokol, veri ve ölçek-form kaynak haritası. | Her bölüm başlangıcında kaynak seçimi için okunacak. |
| `tez-yazim/06_kritik-kaynaklar/kritik-dosya-manifesti.tsv` | Makine-okunabilir kritik dosya manifesti. | Hash, erişim ve doğrulama durumları güncellendikçe yenilenecek. |
| `tez-yazim/04_kalite-kontrol/yazim-oncesi-preflight-2026-06-30.md` | Başlangıç preflight kanıtı. | Yeni preflight komutları çalışırsa tarihli ek rapor üretilecek. |
| `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md` | Her bölüm için zorunlu finalizasyon sertifikasyon süreci. | Bölüm final kabulünden önce eksiksiz uygulanacak. |
| `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasi-sablonu.md` | Doldurulabilir bölüm sertifika raporu şablonu. | `sertifikalar/<bolum>-sertifika-YYYY-MM-DD.md` raporlarına kopyalanacak. |

### 1.2 Üretim Dosyaları

| Dosya | Resmi hedef bölüm | Planlanan işlem |
|---|---|---|
| `thesis.qmd` | Kök Quarto belge | Resmi bölüm sırası ile include sırası arasındaki farklar için ayrı karar verilecek. |
| `chapters/01_giris.qmd` | `GİRİŞ ve AMAÇ` | Başlık, amaç ve literatür boşluğu resmi kılavuza göre yeniden yapılandırılacak. |
| `chapters/02_yontem.qmd` | `GEREÇ ve YÖNTEM` | Nicel/nitel/karma yöntem alt yapısı resmi bölüm diline göre düzenlenecek. |
| `chapters/03_bulgular.qmd` | `BULGULAR` | Yorumsuz bulgu sunumu, nitel bulgular ve joint display ayrımı netleştirilecek. |
| `chapters/04_tartisma.qmd` | `TARTIŞMA ve SONUÇ` | Tartışma ve sonuç resmi şablon mantığına göre birleştirme/ayırma kararı verilecek. |
| `chapters/05_sonuc.qmd` | `TARTIŞMA ve SONUÇ` veya sonuç alt bloku | Resmi kılavuz `TARTIŞMA ve SONUÇ` tek bölümünü istediği için yerleşim kararı verilecek. |
| `chapters/06_post_hoc_genisleme.qmd` | Ek / keşifsel ek / tartışma alt katkısı | Resmi ana bölüm sırası içinde ayrı ana bölüm kalıp kalmayacağı kararlaştırılacak. |

### 1.3 Kanıt Dosyaları

| Kanıt | Kullanım |
|---|---|
| `tez-yazim/06_kritik-kaynaklar/README.md` | Klinik/nitel rapor, protokol, ham/kilitli veri, ölçek-form ve kalite kapısı üst haritası. |
| `docs/CLINICAL-STUDY-REPORT-FINAL.md` | Nicel sonuç, örneklem, analiz ve yorum kanıtı. |
| `docs/analiz_planlari/03-sap-ana-plan.md` | Birincil SAP ve hipotez hattı. |
| `docs/analiz_planlari/04-sap-faz2-posthoc.md` | Faz II/post-hoc sınırları. |
| `docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md` | Veri ve değişken sözleşmesi. |
| `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` | Varlık/hash kontratı; satır içeriği yazıya taşınmaz. |
| `docs/niteliksel/qualitative_canonical_results_report.md` | Nicel repodaki güvenli nitel entegrasyon raporu. |
| `T1DM Niteliksel/07_reports/cross_repo_thesis_bridge_status.md` | Cross-repo güncel kaynak haritası. |
| `T1DM Niteliksel/07_reports/ai_reliability_qualitative_canonical_results_report.md` | Nitel rapor güvenilirlik ve açık nokta kanıtı. |
| `tez-yazim/00_kaynak-kurallari/tam-metin-erisim-kaskadi.md` | OpenAthens -> Anna -> PMC/OA/repository -> Zotero tam metin erişim kapısı. |
| `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` | Her citation için DOI/PMID, OpenAthens/Anna/full-text, Zotero ve iki AI-reliability durumu. |

## 2. Global Araç Orkestrasyonu

> **Tek-otorite devri (2026-07-06):** Oturum ritüeli, araç seçim matrisi ve
> referans kapısı bu bölümde artık **tam metniyle tekrarlanmaz**; kanonik
> otoritelerine işaret edilir (duplikasyon önleme — `01_mimari/README.md`).
> Kanonik kaynaklar:
> - **Oturum ritüeli** → `00_kaynak-kurallari/talimatname-claude-code.md` §1 (`/tez-oturum`).
> - **Araç/MCP/skill/plugin matrisi** → `01_mimari/yetkinlik-ve-arac-mimarisi.md`.
> - **Dış literatür kaskadı** → `01_mimari/evidentia-entegrasyon-cercevesi.md`.
> - **Tam metin erişimi** → `00_kaynak-kurallari/tam-metin-erisim-kaskadi.md`.
> - **Referans kapısı sırası** → `talimatname-claude-code.md` §4; ledger şeması → `02_kanit-haritalari/referans-denetim-ledgeri.md`.
> - **Veri sınırı (KVKK)** → `talimatname-claude-code.md` §2.
>
> Aşağıda yalnız **bu plana özgü yürütme adımları** kalır.

### 2.1 Oturum başlangıcı — bu plana özgü preflight

Kanonik oturum ritüeli `talimatname-claude-code.md` §1'dedir ve `/tez-oturum`
onu çalıştırır. Bu planın yürütmesi için asgari preflight:

- [ ] **Step 1: Resmi kaynak + operasyon dosyalarının varlığı**

```bash
cd /mnt/thunderbolt/workspaces/doktoratezi
test -f tez-yazim/README.md
test -f tez-yazim/06_kritik-kaynaklar/kritik-dosya-manifesti.tsv
test -f docs/tez-kilavuz/'TEZ YAZIM KLAVUZU-2025.pdf'
test -f docs/tez-kilavuz/'TEZ ŞABLONLARI-2026-2RV.docx'
```

Expected: Komut sessiz exit 0 verir.

- [ ] **Step 2: Cross-repo kaynak haritası + araç rotası + bağlam** (karma/nitel kesim)

```bash
cd /mnt/thunderbolt/workspaces/T1DM\ Niteliksel
./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md
./dmnitel route-tool --query "Bu oturumda yazılacak bölüm için araç seçimi"
./dmnitel ai-context
```

Expected: `cross_repo_thesis_bridge_status.md` yazılır; `route-tool` gate sırasını
verir; `ai-context` anonim/türetilmiş bağlam üretir (ham veri/`.env` taşımaz).
Araç seçimi ve kapanış kanıtı `yetkinlik-ve-arac-mimarisi.md` matrisine göre
bölüm notuna işlenir.

- [ ] **Step 3: Harici kaynak kullanılacaksa AI use log** (talimatname §6 kapanış koşulu)

```bash
cd /mnt/thunderbolt/workspaces/T1DM\ Niteliksel
./dmnitel log-ai-use \
  --tool "Anamnesis/Evidentia/OpenAthens/Anna's Library/Zotero/Codex" \
  --model "tool-specific" \
  --purpose "tez bölümü bağlam, dış kanıt, tam metin ve kaynakça desteği" \
  --data-type "anonim/türetilmiş" \
  --external-api-used yes
```

Expected: AI use log satırı eklenir; raw/identifiable bayrakları `no` kalır.

### 2.2 Araç seçim matrisi → tek otorite

Kullanılacak local tool, MCP, skill, plugin ve doğrulama kapılarının **tam
matrisi** (gelişmiş kullanım · ne zaman açılır · kapanış kanıtı · sınır) tek
kanonik yerdedir: **`01_mimari/yetkinlik-ve-arac-mimarisi.md`** ("Varsayılan
Tool Gate" + "Kullanılacak Yetkinlikler"). Burada tekrarlanmaz. Bu planda en
çok kullanılan kapıların otorite eşlemesi:

| Kapı | Kanonik otorite |
|---|---|
| Bağlam (`dmnitel ai-context`, Anamnesis) | `yetkinlik-ve-arac-mimarisi.md` |
| Dış literatür (Evidentia + PubMed/OpenAlex/Paper Search) | `evidentia-entegrasyon-cercevesi.md` §1–3 |
| Tam metin (OpenAthens → Anna's → PMC/OA → Zotero) | `00_kaynak-kurallari/tam-metin-erisim-kaskadi.md` |
| Kaynakça (Zotero item key ≠ BibTeX key) | `yetkinlik-ve-arac-mimarisi.md` + `02_kanit-haritalari/referans-denetim-ledgeri.md` |
| Çift AI-reliability + sci-audit (imla/adli) | `talimatname-claude-code.md` §6 |
| YÖK/ERIC · mevzuat · klinik terminoloji · teknik teslim | `yetkinlik-ve-arac-mimarisi.md` (koşullu kapılar) |

### 2.3 Zorunlu referans kapısı → tek otorite

Referans kapısının **sırası** `talimatname-claude-code.md` §4'tedir
(`/referans-kapisi`); **kanıt/tam-metin detayı** `evidentia-entegrasyon-cercevesi.md`
§5'te; **ledger satır şeması ve durum makinesi** (candidate → cite-ok)
`02_kanit-haritalari/referans-denetim-ledgeri.md` dosyasındadır. Burada
tekrarlanmaz. Özet sıra:

bağlam → bibliyografik kimlik (DOI/PMID/PMCID/OpenAlex/YÖK) → tam metin →
Zotero mutabakatı (item key ≠ BibTeX key) → claim/pasaj notu → ledger + çift
AI-reliability. Kapı kapanmadan referans `chapters/*.qmd` veya
`references/references.bib`'e girmez.

## 3. Faz 0 — Resmi Yapı ve Bölüm Yerleşimi

**Amaç:** Mevcut Quarto bölüm yapısını Marmara resmi bölüm sırası ile hizalamak.

**Files:**
- Read: `docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf`
- Read: `docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx`
- Read: `thesis.qmd`
- Read: `chapters/*.qmd`
- Modify later: `thesis.qmd`
- Modify later: `chapters/01_giris.qmd`
- Modify later: `chapters/02_yontem.qmd`
- Modify later: `chapters/04_tartisma.qmd`
- Modify later: `chapters/05_sonuc.qmd`
- Modify later: `chapters/06_post_hoc_genisleme.qmd`

- [ ] **Step 1: Resmi bölüm sırası kararını yaz**

Create or update a section in the next detailed plan with this decision:

```text
Resmi ana metin sırası: ÖZET, SUMMARY, GİRİŞ ve AMAÇ, GENEL BİLGİLER,
GEREÇ ve YÖNTEM, BULGULAR, TARTIŞMA ve SONUÇ, KAYNAKLAR, ÖZGEÇMİŞ,
BİLİMSEL FAALİYETLER, EKLER.
```

- [ ] **Step 2: Mevcut Quarto uyumsuzluklarını işaretle**

Record these current mismatches before editing:

```text
chapters/01_giris.qmd: "# Giriş" -> official target "GİRİŞ ve AMAÇ".
chapters/02_yontem.qmd: "# Yöntem" -> official target "GEREÇ ve YÖNTEM".
chapters/04_tartisma.qmd + chapters/05_sonuc.qmd: official guide expects
"TARTIŞMA ve SONUÇ"; split/merge decision needed.
chapters/06_post_hoc_genisleme.qmd: official main-section list does not include
separate post-hoc chapter; appendix or labeled sub-section decision needed.
```

- [ ] **Step 3: Bölüm yerleşim kararını kullanıcı onayına sun**

Recommended decision:

```text
Quarto source files may stay split for maintainability, but rendered headings
must follow official Marmara section names. Post-hoc expansion should be
clearly labeled exploratory and either integrated into BULGULAR/TARTIŞMA or
moved to EKLER, depending on supervisor preference.
```

- [ ] **Step 4: Bu fazı kapat**

Run:

```bash
cd /mnt/thunderbolt/workspaces/doktoratezi
quarto check
```

Expected: Quarto installation check passes.

## 4. Faz 1 — Kanıt Haritası ve Kaynak Havuzu

**Amaç:** Her bölümde kullanılacak iddia-kaynak eşleşmesini kurmak.

**Files:**
- Create later: `tez-yazim/02_kanit-haritalari/giris-ve-amac-kanit-haritasi.md`
- Create later: `tez-yazim/02_kanit-haritalari/genel-bilgiler-kanit-haritasi.md`
- Create later: `tez-yazim/02_kanit-haritalari/gerec-ve-yontem-kanit-haritasi.md`
- Create later: `tez-yazim/02_kanit-haritalari/bulgular-kanit-haritasi.md`
- Create later: `tez-yazim/02_kanit-haritalari/tartisma-ve-sonuc-kanit-haritasi.md`
- Create later: `tez-yazim/02_kanit-haritalari/kaynaklar-ekler-kanit-haritasi.md`
- Maintain: `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md`
- Read: `docs/CLINICAL-STUDY-REPORT-FINAL.md`
- Read: `docs/analiz_planlari/03-sap-ana-plan.md`
- Read: `docs/analiz_planlari/04-sap-faz2-posthoc.md`
- Read: `docs/niteliksel/qualitative_canonical_results_report.md`

- [ ] **Step 1: Kanıt haritası klasörünü oluştur**

```bash
cd /mnt/thunderbolt/workspaces/doktoratezi
mkdir -p tez-yazim/02_kanit-haritalari
```

- [ ] **Step 2: Her bölüm için aynı tablo şablonunu kullan**

```markdown
| İddia | Kaynak dosya | Kanıt türü | Yazım yeri | Doğrulama |
|---|---|---|---|---|
| T1DM aile sistemini etkileyen kronik durumdur. | dış literatür + CSR | dış kanıt + repo bağlamı | GİRİŞ ve AMAÇ | Evidentia + OpenAthens/Anna full-text + Zotero + iki AI-reliability |
| Kanonik veri 241 aile x 2 katılımcı yapısındadır. | docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md + lock | repo kanıtı | GEREÇ ve YÖNTEM | R data governance tests |
| Nitel kol dört makro tema sunar. | docs/niteliksel/qualitative_canonical_results_report.md | türetilmiş nitel kanıt | BULGULAR | nitel + nicel AI-reliability |
```

- [ ] **Step 3: Dış literatür arama sorularını bölüm bazında ayır**

Use these initial Evidentia query blocks:

```text
GİRİŞ: pediatric type 1 diabetes family functioning parenting depression sibling relationship mixed methods
GENEL BİLGİLER: type 1 diabetes siblings healthy siblings parental differential treatment family systems
GEREÇ VE YÖNTEM: reflexive thematic analysis COREQ mixed methods joint display multi-informant pediatric chronic illness
TARTIŞMA: parental perception discrepancy child chronic illness diabetes family systems depression parenting
```

- [ ] **Step 4: OpenAthens-first tam metin kapısını çalıştır**

Her aday dış kaynak için MCP seviyesinde bu akışı kullan:

```text
1. DOI/PMID/OpenAlex kimliğini Evidentia akademik çekirdeğiyle doğrula.
2. OpenAthens/Millet Kütüphanesi üzerinden resmi yayıncı HTML/PDF tam metni dene.
3. OpenAthens başarısızsa Anna's Library `article_search` ve `read_article`
   ile Crossref doğrulamalı tam metni dene.
4. Kitap/tez/PDF gerekiyorsa Anna `_book_search`, `_get_document_info`,
   `_read_document` veya `_search_in_document` ile sayfa/pasaj kanıtı çıkar.
5. Bunlar başarısızsa PubMed Central, Europe PMC, yayıncı OA, repository,
   author accepted manuscript veya Zotero attachment kullan; yoksa ledger
   durumunu `full-text-exception` yap ve citation eklemeden önce karar iste.
```

Expected: Her citation adayında tam metin durumu `cite-ok` veya açık
`full-text-exception` olarak ledger'a yazılır.

- [ ] **Step 5: Zotero mutabakatı yap**

Run after verified sources are selected:

```bash
cd /mnt/thunderbolt/workspaces/doktoratezi
python3 scripts/util/zotero_env_bridge.py status --json
python3 scripts/util/zotero_env_bridge.py export-bibtex --out references/references.bib
```

Expected: `status --json` has `"ok": true`; BibTeX export writes
`references/references.bib`. Do not import/write new records without explicit
approval.

- [ ] **Step 6: Referans ledger'ını iki AI-reliability kapısıyla kapat**

```bash
cd /mnt/thunderbolt/workspaces/T1DM\ Niteliksel
PYTHONDONTWRITEBYTECODE=1 python3 plugins/t1dm-qual-ai-audit/skills/t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py

cd /mnt/thunderbolt/workspaces/doktoratezi
PYTHONDONTWRITEBYTECODE=1 python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/test_repo_ai_reliability.py
```

Expected: Nitel ve nicel AI-reliability kontrolleri geçer; ledger'da
`full-text-pending`, `zotero-pending` veya `reliability-pending` satırı kalmaz.

## 5. Faz 2 — GİRİŞ ve AMAÇ

**Amaç:** Tezin bilimsel boşluğunu, karma yöntem gerekçesini, nicel H1-H5
hattını ve nitel triadik kolun katkısını tek resmi bölümde kurmak.

**Files:**
- Read: `tez-yazim/03_bolum-hazirlik/01_giris-ve-amac.md`
- Read: `docs/CLINICAL-STUDY-REPORT-FINAL.md`
- Read: `docs/analiz_planlari/03-sap-ana-plan.md`
- Read: `docs/niteliksel/qualitative_canonical_results_report.md`
- Modify later: `chapters/01_giris.qmd`
- Create later: `tez-yazim/02_kanit-haritalari/giris-ve-amac-kanit-haritasi.md`

- [ ] **Step 1: Mevcut metni resmi başlık hedefiyle karşılaştır**

Check:

```bash
cd /mnt/thunderbolt/workspaces/doktoratezi
sed -n '1,160p' chapters/01_giris.qmd
```

Expected: Current heading and structure visible; official target is
`GİRİŞ ve AMAÇ`.

- [ ] **Step 2: Literatür boşluğu iddialarını dış kanıta bağla**

Use Anamnesis for non-sensitive context, Evidentia for external retrieval,
OpenAthens first for publisher full text, Anna's Library as fallback, and
Zotero for citation-key/full-text reconciliation. Keep these output fields:

```markdown
| Claim | Source | Evidence level | Full-text route | Zotero key | Use in paragraph |
|---|---|---|---|---|---|
| Pediatric T1DM has family-system psychosocial burden. | PMID/DOI | review/guideline/cohort | pass | key | Opening frame |
| Parent-child perception discrepancy matters in chronic illness. | PMID/DOI | primary/review | pass | key | Gap paragraph |
| Healthy sibling experience is underrepresented. | PMID/DOI | qualitative/mixed review | pass | key | Mixed-method rationale |
```

- [ ] **Step 3: Amaç cümlelerini resmi kılavuza göre sadeleştir**

Draft target:

```text
Bu çalışmanın amacı, Tip 1 diyabet tanılı çocuklar, sağlıklı kardeşleri ve
annelerinde ebeveynlik tutumu algısı, anne depresif belirti düzeyi ve kardeş
ilişkisi örüntülerini nicel ve nitel verilerle birlikte incelemektir.
```

- [ ] **Step 4: Araştırma soruları ve hipotezleri ayır**

Use this structure:

```markdown
Nicel hipotezler H1-H5 olarak; nitel araştırma soruları ise triadik aile
deneyimi, sağlıklı kardeş yükü, annenin bakım rolü ve T1DM tanılı çocuğun
içeriden hastalık deneyimi etrafında ayrı sunulacaktır.
```

- [ ] **Step 5: Bölüm sonu kontrolü yap**

Checklist:

```text
Alt başlık kullanımı resmi şablonla uyumlu mu?
Amaç doğrudan ve ölçülebilir mi?
Nitel kol nicel hipotezin açıklaması gibi yazılmadı mı?
Tüm dış iddialar kaynaklı mı?
```

## 6. Faz 3 — GENEL BİLGİLER

**Amaç:** Tezin teorik ve literatür zeminini yorumsuz, genelden özele ve resmi
kılavuz dilinde sunmak.

**Files:**
- Read: `tez-yazim/03_bolum-hazirlik/02_genel-bilgiler.md`
- Create later: `tez-yazim/02_kanit-haritalari/genel-bilgiler-kanit-haritasi.md`
- Modify later: new or existing Quarto section decision depends on Faz 0

- [ ] **Step 1: Alt başlık omurgasını sabitle**

Use this official-friendly outline:

```markdown
1. Tip 1 diyabetin çocukluk çağı bağlamı
2. Kronik hastalık ve aile sistemi
3. Ebeveynlik tutumları ve çocuk algısı
4. Anne depresif belirtileri ve bakım yükü
5. Kardeş ilişkisi ve sağlıklı kardeş deneyimi
6. Triadik ve karma yöntem aile araştırmaları
```

- [ ] **Step 2: Literatür kaynaklarını üç halkaya ayır**

```text
Halka A: Klinik/T1DM rehber ve epidemiyoloji kaynakları
Halka B: Ebeveynlik, depresyon, kardeş ilişkisi psikososyal kaynakları
Halka C: Nitel/karma yöntem, triadik aile ve multi-informant kaynakları
```

- [ ] **Step 3: Araç seçimi**

Run route:

```bash
cd /mnt/thunderbolt/workspaces/T1DM\ Niteliksel
./dmnitel route-tool --query "Genel bilgiler T1DM aile sistemi kardeş ilişkisi literatür taraması"
```

Expected: Anamnesis context management gate, Evidentia external evidence gate,
OpenAthens/Anna's full-text gate, Zotero reference manager gate and dual
AI-reliability gate. If school/education appears, `eric-mcp`; if
biology/pathway appears, `life-science-research`.

- [ ] **Step 4: Yazım sınırı**

Use this rule:

```text
GENEL BİLGİLER bölümünde çalışma bulguları yorumlanmaz. Bulgulara hazırlık
yapan kavramsal zemin kurulur; yorum TARTIŞMA ve SONUÇ bölümüne bırakılır.
```

## 7. Faz 4 — GEREÇ ve YÖNTEM

**Amaç:** Nicel, nitel ve karma yöntemleri tekrarlanabilir, etik ve şeffaf
biçimde yazmak.

**Files:**
- Read: `tez-yazim/03_bolum-hazirlik/03_gerec-ve-yontem.md`
- Read: `_targets.R`
- Read: `docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md`
- Read: `docs/analiz_planlari/03-sap-ana-plan.md`
- Read: `docs/analiz_planlari/04-sap-faz2-posthoc.md`
- Read: `docs/niteliksel/qualitative_canonical_results_report.md`
- Modify later: `chapters/02_yontem.qmd`

- [ ] **Step 1: Nicel yöntem bloklarını ayır**

Use this order:

```markdown
1. Araştırma tasarımı
2. Evren ve örneklem
3. Veri toplama araçları
4. Değişkenler ve ölçüm
5. Veri yönetimi ve kanonik analiz bazı
6. İstatistiksel analiz planı
7. Etik kurul ve veri güvenliği
```

- [ ] **Step 2: Nitel yöntem bloklarını ayır**

Use this order:

```markdown
1. Nitel desen
2. Katılımcılar ve bilgi gücü
3. Veri toplama
4. Refleksif tematik analiz
5. Triadik analiz çerçevesi
6. COREQ/SRQR/JARS-Qual uyumu
7. AI/LLM kullanım beyanı
```

- [ ] **Step 3: Karma yöntem bloklarını ekle**

Use this language rule:

```text
Nicel ve nitel kollar aynı araştırma programının farklı kanıt türleri olarak
sunulur. Nitel kol nicel sonucu doğrulayan veya nedensel mekanizma kanıtı
üreten bir ek analiz gibi yazılmaz.
```

- [ ] **Step 4: Veri governance testlerini çalıştır**

```bash
cd /mnt/thunderbolt/workspaces/doktoratezi
Rscript tests/test_reproducibility_lock.R
Rscript tests/test_final_reference_loading.R
Rscript tests/test_data_governance.R
```

Expected: Sessiz exit 0.

- [ ] **Step 5: COREQ kontrolünü hazırla**

When methods draft exists:

```bash
cd /mnt/thunderbolt/workspaces/T1DM\ Niteliksel
./dmnitel audit-coreq --methods <methods-draft.md> --results <results-draft.md>
```

Expected: COREQ item evidence status; partial/missing items explicitly handled.

## 8. Faz 5 — BULGULAR

**Amaç:** Nicel ve nitel bulguları yorum yapmadan, resmi tablo/şekil kuralları
ve gizlilik sınırıyla sunmak.

**Files:**
- Read: `tez-yazim/03_bolum-hazirlik/04_bulgular.md`
- Read: `chapters/03_bulgular.qmd`
- Read: `docs/niteliksel/qualitative_canonical_results_report.md`
- Modify later: `chapters/03_bulgular.qmd`
- Modify later: `tez-yazim/05_entegrasyon/nitel-nicel-joint-display-plan.md`

- [ ] **Step 1: Bulgular sırasını sabitle**

Use this order:

```markdown
1. Örneklem ve tanımlayıcılar
2. Ölçek/psikometrik durum
3. H1-H5 birincil nicel bulgular
4. Faz II/post-hoc bulgular, açık etiketle
5. Nitel bulgular: dört makro tema
6. Joint display hazırlık tablosu
```

- [ ] **Step 2: Tablo/şekil envanteri çıkar**

Create later:

```markdown
| No | Tablo/Şekil | Kaynak | Bölüm | Resmi format notu |
|---|---|---|---|---|
| Tablo 1 | Sosyodemografik denge | outputs/tables veya chapter source | BULGULAR | Başlık üstte |
| Şekil 1 | Akış diyagramı | docs/assets/figures | BULGULAR | Başlık altta |
```

- [ ] **Step 3: Nitel bulgular için güvenli alıntı kontrolü**

Before adding any quote text:

```bash
cd /mnt/thunderbolt/workspaces/T1DM\ Niteliksel
./dmnitel check-quotes \
  --source 02_processed/cleaned_text/thesis_qualitative_cleaned_current.md \
  --quotes 06_manuscript_outputs/quotes_used.csv \
  --output 07_reports/quote_integrity_report.md
```

Expected: Critical findings absent; quote IDs match source.

- [ ] **Step 4: Bulgular dili kontrolü**

Use this rule:

```text
BULGULAR bölümünde "göstermektedir", "düşündürmektedir", "açıklamaktadır"
gibi yorumlayıcı ifadeler azaltılır. "Saptandı", "bulundu", "raporlandı" gibi
tarafsız sunum dili kullanılır.
```

## 9. Faz 6 — JOINT DISPLAY ve Karma Entegrasyon

**Amaç:** Nicel ve nitel kanıtları yan yana getirmek, fakat kanıt türlerini
karıştırmadan karma yorum zemini oluşturmak.

> **Otorite:** Joint display alan tanımları, ilişki türü sözlüğü ve gizlilik
> kuralı tek kanonik yerdedir: `05_entegrasyon/nitel-nicel-joint-display-plan.md`
> + `05_entegrasyon/nitel-cikti-cercevesi.md`. Aşağıdaki adımlar bu planın
> yürütmesi içindir; alan tanımı çakışırsa 05 otoritesi esastır.

**Files:**
- Modify later: `tez-yazim/05_entegrasyon/nitel-nicel-joint-display-plan.md`
- Read: `docs/niteliksel/qualitative_canonical_results_report.md`
- Read: `chapters/03_bulgular.qmd`
- Modify later: `chapters/03_bulgular.qmd`
- Modify later: `chapters/04_tartisma.qmd`

- [ ] **Step 1: Joint display alanlarını sabitle**

```markdown
| Araştırma odağı | Nicel bulgu | Nitel tema/örüntü | İlişki türü | Karma yorum sınırı |
|---|---|---|---|---|
| H1 | aggregate sonuç | tema/rol örüntüsü | uyum/tamamlayıcılık/ayrışma/açıklayıcı genişleme | nedensellik yok |
```

- [ ] **Step 2: İlişki türü sözlüğünü kullan**

```text
Uyum: İki kanıt türü aynı yönde okuma sağlar.
Tamamlayıcılık: Biri diğerinin kapsamını genişletir.
Ayrışma: Bulgular farklı veya gerilimli yönler gösterir.
Açıklayıcı genişleme: Nitel veri nicel örüntünün deneyimsel bağlamını açar.
```

- [ ] **Step 3: Gizlilik ve nedensellik kontrolü**

Checklist:

```text
Aile düzeyi ayrıntı yok.
Ham quote yok.
Nitel tema nicel mekanizma gibi yazılmadı.
Nicel estimate nitel doğrulama gibi yazılmadı.
Post-hoc bulgu birincil hipotez gibi etiketlenmedi.
```

## 10. Faz 7 — TARTIŞMA ve SONUÇ

**Amaç:** Bulguları literatürle karşılaştırmak, karma yorum üretmek, sınırları
ve önerileri resmi `TARTIŞMA ve SONUÇ` bölüm mantığında yazmak.

**Files:**
- Read: `tez-yazim/03_bolum-hazirlik/05_tartisma-ve-sonuc.md`
- Read: `chapters/04_tartisma.qmd`
- Read: `chapters/05_sonuc.qmd`
- Modify later: `chapters/04_tartisma.qmd`
- Modify later: `chapters/05_sonuc.qmd` or merge/include decision from Faz 0

- [ ] **Step 1: Tartışma omurgasını sabitle**

```markdown
1. Ana bulguların kısa sentezi
2. Nicel H1-H5 bulgularının literatürle karşılaştırması
3. Nitel temaların literatürle karşılaştırması
4. Joint display üzerinden karma yorum
5. Güçlü yönler
6. Sınırlılıklar
7. Klinik ve araştırma önerileri
8. Sonuç
```

- [ ] **Step 2: Dış literatür kanıtını yenile**

Use Anamnesis/context for the discussion frame, Evidentia for retrieval,
OpenAthens first for publisher full text, and Anna's Library as fallback for
full-text claim verification:

```text
parent child perception discrepancy type 1 diabetes chronic illness family systems
maternal depression parenting pediatric diabetes family functioning
healthy siblings type 1 diabetes qualitative family burden
mixed methods joint display pediatric chronic illness family research
```

- [ ] **Step 3: Sonuç cümlelerini kapsamla sınırla**

Use this rule:

```text
Sonuçlar bu örneklem, kullanılan ölçekler, karma yöntem tasarımı ve post-hoc
sınırları içinde yazılır. Klinik karar veya nedensellik iddiaları dış validasyon
gerektiren öneri olarak etiketlenir.
```

## 11. Faz 8 — ÖZET ve SUMMARY

**Amaç:** Resmi şablona uygun, bir sayfayı aşmayan, kaynak içermeyen Türkçe
Özet ve İngilizce Summary hazırlamak.

**Files:**
- Read: `tez-yazim/02_sablonlar/ozet-summary-sablonu.md`
- Create or modify later: official front matter source decision
- Possible modify later: `thesis.qmd` or separate front matter qmd files

- [ ] **Step 1: Türkçe özet yapısını doldur**

```markdown
Amaç:
Gereç ve Yöntem:
Bulgular:
Sonuç:
Anahtar Sözcükler:
```

- [ ] **Step 2: İngilizce Summary çevirisini üret**

Rule:

```text
Summary Türkçe özetle aynı içerik mantığını izler. Yeni iddia eklemez,
kaynak içermez, en fazla beş keywords verir.
```

- [ ] **Step 3: Sayısal formatı kontrol et**

Checklist:

```text
Türkçe özette ondalık virgül.
İngilizce Summary'de Enstitü şablonuyla uyumlu yazım.
p değerleri kılavuz formatında.
Anahtar sözcük sayısı en fazla beş.
```

## 12. Faz 9 — KAYNAKLAR, EKLER ve Ön Bölümler

**Amaç:** Resmi kaynakça, ekler, beyan, kısaltmalar, tablo/şekil listeleri ve
bilimsel faaliyetler paketini hazırlamak.

**Files:**
- Read: `tez-yazim/03_bolum-hazirlik/06_kaynaklar-ekler.md`
- Read: `tez-yazim/02_sablonlar/on-bolumler-sablonu.md`
- Read: `references/references.bib`
- Modify later: `references/references.bib`
- Create later: front matter qmd/docx conversion decision

- [ ] **Step 1: Kaynakça stil kararını doğrula**

Rule:

```text
Final kaynak listesi Marmara Enstitü AMA-11 özel formatına göre alfabetik
sıralanır. Repo içindeki APA/CSL notları final formatta resmi kılavuzun
altında kalır.
```

- [ ] **Step 2: OpenAthens/Anna full-text ledger ve Zotero mutabakatı**

Before export, every cited item must have DOI/PMID/ID, full-text evidence,
claim/passage note and status in `referans-denetim-ledgeri.md`.

```bash
cd /mnt/thunderbolt/workspaces/doktoratezi
python3 scripts/util/zotero_env_bridge.py status --json
python3 scripts/util/zotero_env_bridge.py export-bibtex --out references/references.bib
```

Expected: Web API status OK; export succeeds. Import/write only after explicit
approval.

- [ ] **Step 3: Ek listesi**

Use this initial appendix list:

```markdown
Ek 1. Etik kurul onayı
Ek 2. Veri toplama araçları ve ölçekler
Ek 3. COREQ/SRQR/JARS-Qual özeti
Ek 4. LLM kullanım beyanı
Ek 5. Ek tablo ve şekiller
Ek 6. Faz II/post-hoc ayrıntılı analiz paketleri
```

- [ ] **Step 4: Liste kontrolleri**

Checklist:

```text
Kısaltmalar alfabetik.
Tablo listesinde yalnız numara, başlık, sayfa no.
Şekil listesinde yalnız numara, başlık, sayfa no.
Ön bölüm sayfa numaralandırması resmi kılavuza uygun.
```

## 13. Faz 10 — Render, Audit ve Teslim Öncesi Paket

**Amaç:** Tez metninin üretilebilir, kaynaklı, gizlilik sınırı korunmuş ve
resmi formatla uyumlu olduğunu doğrulamak.

**Files:**
- Read/modify as needed: `thesis.qmd`
- Read/modify as needed: `chapters/*.qmd`
- Read: `tez-yazim/04_kalite-kontrol/*.md`
- Output: `outputs/quarto/` veya Quarto render hedefi

- [ ] **Step 1: Hafif teknik kontroller**

```bash
cd /mnt/thunderbolt/workspaces/doktoratezi
quarto check
Rscript -e 'renv::status()'
```

Expected: Quarto check passes; renv has no issues.

- [ ] **Step 2: Veri-governance kontrolleri**

```bash
cd /mnt/thunderbolt/workspaces/doktoratezi
Rscript tests/test_reproducibility_lock.R
Rscript tests/test_final_reference_loading.R
Rscript tests/test_data_governance.R
```

Expected: Sessiz exit 0.

- [ ] **Step 3: Referans tam metin ve Zotero kapanış kapısı**

```bash
cd /mnt/thunderbolt/workspaces/doktoratezi
test -f tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md
rg -n 'full-text-pending|zotero-pending|reliability-pending|citation-without-full-text' tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md
python3 scripts/util/zotero_env_bridge.py status --json
python3 scripts/util/zotero_env_bridge.py export-bibtex --out references/references.bib
```

Expected: `test` exit 0; `rg` exit 1 because unresolved reference states do
not exist; Zotero status is OK and BibTeX export succeeds.

- [ ] **Step 4: AI/policy regression**

```bash
cd /mnt/thunderbolt/workspaces/T1DM\ Niteliksel
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 python3 plugins/t1dm-qual-ai-audit/skills/t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py
npx promptfoo@latest eval -c reliability/evals/promptfooconfig.yaml

cd /mnt/thunderbolt/workspaces/doktoratezi
PYTHONDONTWRITEBYTECODE=1 python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/test_repo_ai_reliability.py
npx promptfoo@latest eval -c reliability/evals/promptfooconfig.yaml
```

Expected: Nitel unit tests pass, nitel AI audit passes, nicel AI audit passes,
promptfoo nitel/nicel 4/4 passes.

- [ ] **Step 5: Full render**

Run only after chapter structure is stable:

```bash
cd /mnt/thunderbolt/workspaces/doktoratezi
quarto render thesis.qmd
```

Expected: Render exits 0 and writes configured output. If render fails, capture
the first error block and fix only the implicated file.

- [ ] **Step 6: Final gap register**

Create later:

```text
tez-yazim/04_kalite-kontrol/final-gap-register-YYYY-MM-DD.md
```

Required headings:

```markdown
# Final Gap Register

## Blockers
## Supervisor Decisions
## Source/Citation Gaps
## Formatting Gaps
## Privacy/Governance Gaps
## Resolved Items
```

- [ ] **Step 7: Bölüm sertifikalarını kapat**

Her ana bölüm için sertifikasyon playbook'u ayrı raporla çalıştırılır:

```bash
cd /mnt/thunderbolt/workspaces/doktoratezi
test -f tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md
test -f tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasi-sablonu.md
mkdir -p tez-yazim/04_kalite-kontrol/sertifikalar
```

Expected: Her yazılmış bölüm için
`tez-yazim/04_kalite-kontrol/sertifikalar/<bolum>-sertifika-YYYY-MM-DD.md`
oluşur. Sertifikada Kapı 0-5 `PASS`, nihai durum `certified-final` ve açık
uygulama onayı yoksa bölüm final kabul edilmez.

## 14. Bölüm Detay Planları (kapsamlı talimatnameler)

Her bölümün detay planı, ayrı bir detay-plan dosyası olarak değil,
`03_bolum-hazirlik/` (+ `02_sablonlar/`, `05_entegrasyon/`) altında **kapsamlı
yürütme talimatnamesi** olarak yazılmıştır (2026-07-06). Klasör otorite
haritası: `03_bolum-hazirlik/README.md`.

| Sıra | Kapsamlı talimatname | Üretim hedefi |
|---:|---|---|
| 1 | `tez-yazim/03_bolum-hazirlik/01_giris-ve-amac.md` | GİRİŞ ve AMAÇ |
| 2 | `tez-yazim/03_bolum-hazirlik/02_genel-bilgiler.md` | GENEL BİLGİLER |
| 3 | `tez-yazim/03_bolum-hazirlik/03_gerec-ve-yontem.md` | GEREÇ ve YÖNTEM |
| 4 | `tez-yazim/03_bolum-hazirlik/04_bulgular.md` | BULGULAR |
| 5 | `tez-yazim/05_entegrasyon/nitel-nicel-joint-display-plan.md` | Nitel-nicel entegrasyon |
| 6 | `tez-yazim/03_bolum-hazirlik/05_tartisma-ve-sonuc.md` | TARTIŞMA ve SONUÇ |
| 7 | `tez-yazim/02_sablonlar/ozet-summary-sablonu.md` | ÖZET ve SUMMARY |
| 8 | `tez-yazim/03_bolum-hazirlik/06_kaynaklar-ekler.md` | KAYNAKLAR ve EKLER |
| 9 | `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md` | Final render ve teslim (Kapı 5) |
| 10 | `tez-yazim/04_kalite-kontrol/sertifikalar/*.md` | Her bölüm için finalizasyon sertifikası ve uygulama onayı |

## 15. Çalışma Paketleri — Durum

Bölüm detay planları **kapsamlı yürütme talimatnamesi** olarak yazıldı
(`03_bolum-hazirlik/`, `02_sablonlar/`, `05_entegrasyon/`; 2026-07-06). Sıradaki
adım, bu talimatnameleri uygulayarak `chapters/*.qmd` üretimini yapmaktır.
`GİRİŞ ve AMAÇ` yürütme talimatnamesi `03_bolum-hazirlik/01_giris-ve-amac.md`
şu kararları kapsar:

1. `chapters/01_giris.qmd` başlığının resmi `GİRİŞ ve AMAÇ` hedefine nasıl
   dönüştürüleceği.
2. Literatür boşluğu için Evidentia sorgu seti.
3. OpenAthens-first tam metin kaskadı, Anna fallback, Zotero ve referans
   ledger kapılarının giriş literatürüne nasıl uygulanacağı.
4. H1-H5 ve nitel triadik araştırma sorularının aynı bölümde nasıl ayrılacağı.
5. Amaç cümlesinin resmi kılavuzdaki doğrudan ve kısa yazım beklentisine göre
   nasıl kurulacağı.
6. Bölüm sonunda hangi kaynakça, format, Anamnesis/context ve çift
   AI-reliability kontrollerinin çalışacağı.
7. Bölümün hangi sertifika raporuyla `certified-final` statüsüne geçeceği ve
   onay bekliyorsa neden `provisional-pass` kalacağı.

## 16. Self-Review

- Spec coverage: Resmi kılavuz, iki-repo entegrasyon, araç mimarisi, bölüm
  sırası, kanıt haritası, Anamnesis/context yönetimi, OpenAthens/Anna
  full-text, literatür, Zotero, bölüm sertifikasyonu, R/Quarto, çift
  AI-reliability ve final render gereksinimleri bu plana bağlandı.
- Placeholder scan: Bu planda boş bırakılmış uygulama veya karar alanı
  bırakılmadı. Araştırmacı/danışman kararı gerektiren noktalar açık karar
  adımı olarak yazıldı.
- Type/command consistency: Komutlar mevcut repo köklerine göre yazıldı;
  `dmnitel` komutları nitel repo kökünde, R/Quarto komutları nicel repo
  kökünde çalışacak biçimde ayrıldı.
