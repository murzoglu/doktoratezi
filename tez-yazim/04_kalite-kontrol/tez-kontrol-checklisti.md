# Tez Kontrol Checklisti (Kapsamlı)

> **Amaç:** Tezin tümü ve her `chapters/*.qmd` bölümü için **tek yerden**
> denetlenebilir, her maddesi bir **kontrol mekanizmasına** ve **araca** bağlı
> kapsamlı kontrol listesi. Bu belge **kanonik kural tanımlamaz**; her madde
> ilgili kanonik otoriteye (marmara §, talimatname §, playbook Kapı) pointer
> verir ve `scripts/util/tez_checklist_verify.py` kayıt kaydındaki bir kontrole
> **birebir** karşılık gelir.
>
> **Otomasyon:** Bu belgedeki her madde ID'si (ör. `K3-FIG-01`) doğrulama
> orkestratöründeki bir kontrolle eşleşir. Senkronu doğrulamak için:
> `python3 scripts/util/tez_checklist_verify.py --audit-doc` (yetim madde /
> eksik kontrol = exit 1). Kayıt otoritesi **script'tir**; bu belge onun
> insan-okunur yansımasıdır.
>
> **Merkez süreç:** `bolum-finalizasyon-sertifikasyon-playbook.md` (Kapı 0–5).
> **Klasör haritası:** `04_kalite-kontrol/README.md`. **Öncelik zinciri:**
> kullanıcı/danışman → resmi `docs/tez-kilavuz/` → `00_kaynak-kurallari` →
> playbook → operasyonel checklist.

## Nasıl kullanılır

```bash
# Tüm tez, tam denetim (ağır kontroller dahil: render, PDF, renv, targets)
python3 scripts/util/tez_checklist_verify.py

# Hızlı ön-uçuş (ağır kontroller SKIP)
python3 scripts/util/tez_checklist_verify.py --fast

# Tek eksen veya ID öneki
python3 scripts/util/tez_checklist_verify.py --section K3
python3 scripts/util/tez_checklist_verify.py --section Format

# Tek bölüm (yalnız bölüm-düzeyi A maddeleri anlamlı)
python3 scripts/util/tez_checklist_verify.py --chapter chapters/04_bulgular.qmd

# Kayıt listesi + belge senkron denetimi
python3 scripts/util/tez_checklist_verify.py --list
python3 scripts/util/tez_checklist_verify.py --audit-doc
```

**Statü sözlüğü:** `PASS` geçti · `FAIL` teslim engeli (otomatik) · `SKIP`
önkoşul yok (ör. render çıktısı yok / `--fast`) · `MANUEL` script karar veremez,
elle doğrula. Exit kodu: herhangi `FAIL` varsa `1`, yoksa `0`.

---

## A. Bölüm-düzeyi kontroller (her `chapters/*.qmd` için)

Bir bölüm final kabul edilmeden önce bu maddeler o bölüm üzerinde temiz olmalı.
`--chapter <yol>` ile tek bölüme daraltılır.

### A-K0 · Kapsam & Gizlilik

- [ ] **K0-PII-02** — Bölüm metninde ham veri `ad_soyad`/`adSoyad` kolon
  kalıntısı yok.
  - **Mekanizma:** `chapters/*.qmd` gövdesinde kolon-adı regex taraması
    (boşluklu resmi "Ad Soyad" jüri/imza alanı kapsam dışı).
  - **Araç:** `tez_checklist_verify.py` → `chk_pii_no_names`.
  - **Kanonik:** `talimatname-claude-code.md` §2 (veri sınırı).

### A-K3 · Format & Kılavuz uyumu

- [ ] **K3-NUM-01** — Ondalık ayırıcı virgül; gövde metninde nokta-ondalık
  istatistik (`p=0.038`, `0.16`) yok (kod blokları hariç).
  - **Mekanizma:** kod-fence/inline-code çıkarılmış gövdede nokta-ondalık
    regex adayı taraması.
  - **Araç:** `tez_checklist_verify.py` → `chk_decimal_comma`.
  - **Kanonik:** marmara §1.4 · `format-kontrol-listesi.md`.
- [ ] **K3-HDG-01** — Başlıkta elle numara yok (`number-sections` oto-numarası
  ile çift numaralanma üretmez).
  - **Mekanizma:** `^#{1,6}\s+\d+(\.\d+)*` başlık deseni taraması.
  - **Araç:** `tez_checklist_verify.py` → `chk_heading_numbering`.
  - **Kanonik:** marmara §1.3 (başlık) + `_quarto.yml number-sections`.
- [ ] **K3-FIG-01** — Her `{#fig-...}` etiketine gövdede en az bir `@fig-`
  metin-içi atıfı var.
  - **Mekanizma:** etiket kümesi ↔ `@fig-` atıf kümesi farkı.
  - **Araç:** `tez_checklist_verify.py` → `chk_fig_refs`.
  - **Kanonik:** marmara §1.6 (şekil).
- [ ] **K3-TBL-01** — Her `tbl-` etiketine gövdede en az bir `@tbl-` metin-içi
  atıfı var.
  - **Mekanizma:** etiket kümesi ↔ `@tbl-` atıf kümesi farkı.
  - **Araç:** `tez_checklist_verify.py` → `chk_tbl_refs`.
  - **Kanonik:** marmara §1.7 (tablo).

### A-T · Ön/Arka bölüm & retorik

- [ ] **T-RHET-01** — Retorik akış / thick-description insan-Türkçesi (yapay
  kalıp, şablon tekrarı yok). **[MANUEL]**
  - **Mekanizma:** elle okuma; üretim tarafı playbook rehberliğinde.
  - **Araç:** `insan-turkcesi-retorik-playbook.md` + Kapı 4 sci-audit axis G.
  - **Kanonik:** marmara §1–§5 register.

---

## B. Tez-düzeyi kontroller (tüm tez)

Tezin bütünü üzerinde çalışır; `--chapter` verilse de tam tez kapsamında
değerlendirilir.

### B-K0 · Kapsam & Gizlilik

- [ ] **K0-PII-01** — PII ağaçları `.gitignore` kapsamında ve git-izlenmiyor
  (`data/raw|identified|cleaned|backup`).
  - **Mekanizma:** `git check-ignore` (düz + sonda `/` biçimi) + `git ls-files
    --error-unmatch`.
  - **Araç:** `tez_checklist_verify.py` → `chk_pii_gitignore`.
  - **Kanonik:** `talimatname-claude-code.md` §2 · `.gitignore`.
- [ ] **K0-POL-01** — `.claude/settings.json` deny listesi PII ağaçlarını
  kapsıyor.
  - **Mekanizma:** deny listesinde dört PII ağacının varlığı.
  - **Araç:** `tez_checklist_verify.py` → `chk_deny_policy`.
  - **Kanonik:** `.claude/settings.json` `permissions.deny`.
- [ ] **K0-LCK-01** — Kanonik analiz baz kilidi mevcut
  (`FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock`).
  - **Mekanizma:** kilit dosyası varlık kontrolü.
  - **Araç:** `tez_checklist_verify.py` → `chk_canonical_lock`.
  - **Kanonik:** `docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md`.
- [ ] **K0-PII-03** — Değer-şekilli PII (11-hane T.C., gg.aa.yyyy doğum tarihi,
  hasta/protokol/dosya no, telefon) tüm manuskript yüzeyinde yok.
  - **Mekanizma:** `pii_value_scan.py` dar-desen taraması (bölümler + CSR;
    kaba yıl/n-sayısı kapsam dışı). `chk_pii_no_names` kolon-adı kalıntısını,
    bu madde DEĞER biçimini yakalar.
  - **Araç:** `tez_checklist_verify.py` → `chk_pii_value_scan` → `pii_value_scan.py`.
  - **Kılavuz-zorunlu alan muafiyeti:** Marmara SBE tez şablonu
    (`TEZ ŞABLONLARI-2026-2RV.docx`) §9 ÖZGEÇMİŞ tablosu **Doğum Tarihi** ve
    **Tel** alanlarını zorunlu kılar. Bunlar araştırmacının kendi bilgisidir,
    katılımcı PII'si değildir → `pii_value_scan.py` `ALLOWLIST` kaydıyla muaf.
    Muafiyet **dar**dır: yalnız *dosya + PII sınıfı + satır bağlam deseni*
    (`**Tel**` / `**Doğum Tarihi**` etiketi) üçlüsü birden tutarsa uygulanır;
    aynı dosyadaki etiketsiz bir telefon yine yakalanır. `NON_EXEMPTIBLE`
    (**T.C. kimlik no**, **hasta/protokol no**) hiçbir kayıtla muaf edilemez.
    Muaf bulgular sessizce yutulmaz, `MUAF …` satırı olarak raporlanır ve
    checklist PASS mesajında sayılır; `--strict` tüm muafiyetleri yok sayıp
    tam görünürlük verir. Sözleşme testi: `tests/test_qc_coverage.py` →
    `PiiExemptionScopeTests`.
  - **Kanonik:** `talimatname-claude-code.md` §2 (KVKK veri sınırı).

### B-K1 · Kanıt & Literatür

- [ ] **K1-BIB-01** — Bib hijyeni: atıf ↔ künye ↔ ledger + DOI/PMID; tanımsız
  atıf (HARD) render'ı kırar → HARD=0 zorunlu.
  - **Mekanizma:** `bib_hygiene.py all` (exit 1=HARD, 2=SOFT).
  - **Araç:** `tez_checklist_verify.py` → `chk_bib_hygiene` → `bib_hygiene.py`.
  - **Kanonik:** `02_kanit-haritalari/referans-denetim-ledgeri.md` + marmara AMA-11.
- [ ] **K1-LED-01** — Karma kanıt ledger drift-guard temiz.
  - **Mekanizma:** `karma_ledger_check.py` (exit 0=temiz).
  - **Araç:** `tez_checklist_verify.py` → `chk_karma_ledger` → `karma_ledger_check.py`.
  - **Kanonik:** `02_kanit-haritalari/` ledger.
- [ ] **K1-CLM-01** — Birleşik claim kapısı (sayı izi + nedensel + bib)
  PASS/WARN (FAIL bloklar).
  - **Mekanizma:** `claim_certification.py` (exit 0=PASS, 2=WARN, 1=FAIL).
  - **Araç:** `tez_checklist_verify.py` → `chk_claim_cert` → `claim_certification.py`.
  - **Kanonik:** playbook Kapı 1–5 + CSR belgesi.
- [ ] **K1-KAR-01** — Karma cross-arm aşırı-iddia yok: bir kol (nitel/nicel)
  diğerini "doğrular/kanıtlar/ispatlar" biçiminde sunmaz; ilişki yakınsama/
  tamamlayıcılık diliyle kurulur (JARS-Mixed). `karma_ledger_check` yalnız 6
  ledger satırını korurdu; bu madde §2-§5 + ch05 nesrine yayar (Türkçe isim/fiil
  homografı ve olumsuzlama muaf — yanlış-pozitif koruması).
  - **Mekanizma:** `cross_arm_rhetoric_audit.py` (cümlede confirm-fiil + nitel +
    nicel birlikte, olumsuzlama yok → bulgu; exit 0=temiz).
  - **Araç:** `tez_checklist_verify.py` → `chk_cross_arm` → `cross_arm_rhetoric_audit.py`.
  - **Kanonik:** `05_entegrasyon/karma-sentez-kanonik.md` + JARS-Mixed.
- [ ] **K1-DOI-01** — references.bib DOI'leri Crossref başlığıyla eşleşir
  (yanlış-atıf yok). **[--closing; ağ-bağımlı]** DOI-başına Crossref sorgusu →
  yalnız `--closing` modunda koşar; ağ erişilemezse SKIP (uydurma yok), yalnız
  jaccard<0.4 CHECK (gerçek yanlış-atıf) FAIL. KVKK: yalnız yayın başlığı/DOI.
  - **Mekanizma:** references.bib DOI'leri → `/tmp/ctx_targets.json` →
    `doi_title_resolve.py` → `/tmp/doi_resolve.json` CHECK/OK/CROSSREF_ERR ayrımı.
  - **Araç:** `tez_checklist_verify.py` → `chk_doi_title` → `doi_title_resolve.py`.
  - **Kanonik:** `02_kanit-haritalari/referans-denetim-ledgeri.md` + Crossref.

### B-K3 · Format & Kılavuz (bölüm sırası)

- [ ] **K3-SEQ-01** — Bölüm sırası + başlık disiplini (resmi sıra, tr headings
  blocker=0).
  - **Mekanizma:** `tr_corpus_audit.py` headings ekseni.
  - **Araç:** `tez_checklist_verify.py` → `chk_tr_headings` → `tr_corpus_audit.py`.
  - **Kanonik:** marmara bölüm sırası + sci-audit axis G.

### B-K4 · Türkçe imla, akış, mantık

- [ ] **K4-COH-01** — Türkçe akış/tutarlılık denetimi (blocker=0).
  - **Mekanizma:** `tr_corpus_audit.py` coherence ekseni.
  - **Araç:** `tez_checklist_verify.py` → `chk_tr_coherence` → `tr_corpus_audit.py`.
  - **Kanonik:** Kapı 4 · `turkce-bilimsel-yazim-denetimi.md`.
- [ ] **K4-REF-01** — Yazar-tarih atıf düzyazısı disiplini (§1.8).
  - **Mekanizma:** `tr_corpus_audit.py` reference-prose ekseni.
  - **Araç:** `tez_checklist_verify.py` → `chk_tr_refprose` → `tr_corpus_audit.py`.
  - **Kanonik:** marmara §1.8.
- [ ] **K4-TRG-01** — Bilimsel-yazım Ekseni G çekirdeği (G1-G6; nokta-ondalık-p
  blocker dahil) her Türkçe bölümde temiz. "Zorunlu/kanonik" işaretli axis-G
  28-madde paketinde yoktu (İngilizce SUMMARY/00c ondalık-nokta kullandığından
  kapsam dışı — yanlış-pozitif koruması).
  - **Mekanizma:** sci-audit `tr_sciaudit.py <bölüm> --fail-on error` (her
    `chapters/*.qmd`; çekirdek bulunamazsa closing'de FAIL, normalde SKIP).
  - **Araç:** `tez_checklist_verify.py` → `chk_axis_g` → `tr_sciaudit.py`.
  - **Kanonik:** sci-audit axis G + marmara §1.4 (ondalık virgül).

- [ ] **K4-TERM-01** — Kanonik terim sözlüğü tutarlılığı: tez genelinde tercih
  edilen tek biçim korunur; yasak varyant (ör. `latent değişken`→`gizil değişken`,
  `yanlış keşif`→`yanlış-keşif`) muafiyet dışı kullanıldığında HARD = teslim engeli.
  Muafiyetler: İngilizce özet (00c), ilk-geçiş parantezi `(*latent*)`, confounder
  paragraf-bağlamı (`gizli`=gözlenmeyen karıştırıcı), Dirik/Arrindell kaynak-terimi
  (`aşırı koruyuculuk`/`reddedicilik`), kod-çiti ve atıf. Yalnız terim-dili;
  sayı/istatistik/yön DEĞİŞMEZ.
  - **Mekanizma:** `terim_tutarlilik_audit.py --sozluk docs/tez-kilavuz/terim-sozlugu.yaml
    --chapters 'chapters/*.qmd' --fail-on hard`; HARD bulgu → exit 1. Sözlük/araç
    yoksa closing'de FAIL, normalde SKIP.
  - **Araç:** `tez_checklist_verify.py` → `chk_term_consistency` →
    `terim_tutarlilik_audit.py` (mevcut `tr_corpus_audit.py` primitive'lerini
    yeniden kullanır).
  - **Kanonik:** `docs/tez-kilavuz/terim-sozlugu.yaml` (A1-A7); tespit raporu
    `docs/tez-kilavuz/TERIM_TUTARLILIK_TARAMASI.md`.

### B-K5 · AI-reliability & teknik

- [ ] **K5-NUM-01** — Sayısal iddia → CSV izi (yüksek-risk eşsiz sayı izlenir).
  - **Mekanizma:** `csr_numeric_trace_audit.py` (yüksek-risk eşsiz=0 → temiz).
  - **Araç:** `tez_checklist_verify.py` → `chk_numeric_trace` → `csr_numeric_trace_audit.py`.
  - **Kanonik:** playbook AI-reliability + CSR.
- [ ] **K5-NUM-02** — ch05 Tartışma sayısal yeniden-ifade → CSV izi (sürüklenme
  kapısı). ch05, ch04 Bulgular'daki kendi sonuçlarımızı (β/ICC/p) yeniden
  ifade eder; yeniden-ifadede sayı sürüklenmesi olmamalı. Atıflı dış-literatür
  değerleri (Pinquart g, PedsQL vb.) `is_cited_external_literature` ayrımıyla muaf;
  yalnız kaynağı CSV olması gereken kendi sonuçlarımızın kaynaksız kalması yüksek-risktir.
  - **Mekanizma:** `csr_numeric_trace_audit.py --csr chapters/05_tartisma_ve_sonuc.qmd`
    (yüksek-risk eşsiz=0 → temiz).
  - **Araç:** `tez_checklist_verify.py` → `chk_numeric_trace_discussion` → `csr_numeric_trace_audit.py`.
  - **Kanonik:** AGENTS.md Sayısal Bütünlük Kaideleri (kaynak-tekilliği; ch04→ch05 tutarlılık).
- [ ] **K5-NUM-03** — ch04 Bulgular sayısal iddia → CSV izi. Bulgular tezin
  KENDİ sonuçlarının (β/ICC/AUC/BF) yaşadığı bölümdür; K5-NUM-01 CSR'ı,
  K5-NUM-02 ch05'i izliyordu — ch04 gövdesi izlenmiyordu (BF-drift sınıfı boşluk).
  - **Mekanizma:** `csr_numeric_trace_audit.py --csr chapters/04_bulgular.qmd`
    (yüksek-risk eşsiz=0 → temiz).
  - **Araç:** `tez_checklist_verify.py` → `chk_numeric_trace_bulgular` → `csr_numeric_trace_audit.py`.
  - **Kanonik:** AGENTS.md Sayısal Bütünlük Kaideleri (kaynak-tekilliği).
- [ ] **K5-CAU-01** — Nedensel dil + keşifsel/post-hoc etiket disiplini.
  - **Mekanizma:** `csr_causal_label_audit.py` (exit 0=temiz).
  - **Araç:** `tez_checklist_verify.py` → `chk_causal_label` → `csr_causal_label_audit.py`.
  - **Kanonik:** Faz II keşifsel/post-hoc etiketleme kuralı.
- [ ] **K5-CAU-02** — ch05 Tartışma nedensel dil + etiket disiplini. Nedensel/
  keşifsel-etiket denetimi yalnız CSR'de koşuyordu; asıl Tartışma bölümü (ch05)
  kapsam dışıydı → denetim gerçek metne yayıldı.
  - **Mekanizma:** `csr_causal_label_audit.py --csr chapters/05_tartisma_ve_sonuc.qmd`
    (exit 0=temiz).
  - **Araç:** `tez_checklist_verify.py` → `chk_causal_label_discussion` → `csr_causal_label_audit.py`.
  - **Kanonik:** Faz II keşifsel/post-hoc etiketleme kuralı + marmara nedensellik dili.
- [ ] **K5-HOK-01** — İki-kol hook ağacı (`.claude/hooks` + `.codex/hooks`)
  senkron + hook testi PASS.
  - **Mekanizma:** dosya kümesi eşitliği + `tests/test_claude_hooks.py`.
  - **Araç:** `tez_checklist_verify.py` → `chk_hooks_twin`.
  - **Kanonik:** AGENTS.md Claude Code katmanı.
- [ ] **K5-LIT-01** — R üretici kodda gömülü istatistik literali yok
  (kaynak-tekilliği). APA tablo/metin üreten `R/` fonksiyonları BF/beta/ICC/AUC/
  CFI/entropi gibi değerleri gömülü literal olarak taşımaz; değeri üretilmiş
  model/CSV artefaktından okur.
  - **Mekanizma:** `r_generator_literal_audit.py --include-chapters` (R/ +
    scripts/R yanı sıra `chapters/*.qmd` inline `{r}` chunk'ları; exit 0=temiz).
  - **Araç:** `tez_checklist_verify.py` → `chk_r_generator_literal` →
    `r_generator_literal_audit.py`.
  - **Kanonik:** AGENTS.md Sayısal Bütünlük Kaideleri (kaynak-tekilliği).
- [ ] **K5-TRK-01** — `_targets.R` `format="file"` dosya-izleme (Kaide-2). Bir
  hedef `data/processed/*` veya `outputs/*` altındaki türetilmiş bir yolu
  DOĞRUDAN LİTERAL okuyorsa `format="file"` ile izlenmeli; yoksa stale değer
  okunabilir (içerik-hash geçersizlemesi tetiklenmez).
  - **Mekanizma:** `targets_file_tracking_audit.py` (exit 0=temiz; dengeli-
    parantez `tar_target` blok taraması, yardımcı-fonksiyon okumaları muaf).
  - **Araç:** `tez_checklist_verify.py` → `chk_targets_file_tracking` → `targets_file_tracking_audit.py`.
  - **Kanonik:** AGENTS.md Sayısal Bütünlük Kaideleri (dosya-izleme; Kaide-2).
- [ ] **K5-GAL-01** — Galileo tam-tez judge koşumu güncel. **[ADVISORY; HARD
  değil]** En derin cross-document QC (galileo convergence/harking/overclaim/
  coherence) yalnız opt-in koşuyordu; bu madde tam-tez judge artefaktının
  varlığını + tazeliğini raporlar (atlanmış/eskimiş koşum görünür). Asla FAIL
  üretmez (HARD asla judge'dan gelmez).
  - **Mekanizma:** `outputs/reports/galileo_full_thesis_judge.json` varlığı +
    bölümlerden yeni mi (mtime). Yok/eski → MANUEL.
  - **Araç:** `tez_checklist_verify.py` → `chk_galileo_logged`;
    üretici `scripts/eval/run_full_thesis_judge.py --out ...`.
  - **Kanonik:** `manuskript-denetimi-sciaudit.md` §galileo + `bolum-sertifika` Kapı 3/4.

### B-P · Pipeline & üretilebilirlik

- [ ] **P-ENV-01** — `renv::status()` paket ortamı senkron. **[ağır · --fast SKIP]**
  - **Mekanizma:** `Rscript -e 'renv::status()'` senkron kalıbı.
  - **Araç:** `tez_checklist_verify.py` → `chk_renv_status`.
  - **Kanonik:** `renv.lock`.
- [ ] **P-TAR-01** — `targets`: outdated hedef yok (tar_make taze).
  **[ağır · --fast SKIP]**
  - **Mekanizma:** `targets::tar_outdated()` boş küme.
  - **Araç:** `tez_checklist_verify.py` → `chk_targets_fresh`.
  - **Kanonik:** `_targets.R`.

### B-R · Render & çıktı bütünlüğü

- [ ] **R-RND-01** — `quarto render thesis.qmd` exit 0. **[ağır · --fast SKIP]**
  - **Mekanizma:** `quarto render --to html` alt-süreç exit kodu.
  - **Araç:** `tez_checklist_verify.py` → `chk_render_exit`.
  - **Kanonik:** `render-bagimliliklari.md`.
- [ ] **R-XRF-01** — Render çıktısında 0 çözülmemiş crossref / kırık atıf / ham
  `@fig|@tbl|@sec` sızıntısı.
  - **Mekanizma:** HTML çıktısında `?@`, `[?]`, ham atıf sayımı.
  - **Araç:** `tez_checklist_verify.py` → `chk_render_crossref`.
  - **Kanonik:** marmara §1.6–1.7 crossref.
- [ ] **R-PDF-01** — PDF Marmara ölçüleri: A4 + gömülü Times-uyumlu font.
  **[ağır · --fast SKIP]**
  - **Mekanizma:** `pymupdf`/`fitz` ile sayfa boyutu + gömülü font taraması.
  - **Araç:** `tez_checklist_verify.py` → `chk_pdf_format`.
  - **Kanonik:** marmara §1 + `tex/marmara-preamble.tex`.
- [ ] **R-SVG-01** — librsvg (`rsvg-convert`) render önkoşulu. SVG figürü olan
  bir tezde `rsvg-convert` yoksa figürler sessizce boş rasterize olur ("render
  success" yanıltıcıdır) → önkoşul denetlenir.
  - **Mekanizma:** `chapters/`+`docs/assets` altında `.svg` varlığı → `which
    rsvg-convert`; yoksa FAIL.
  - **Araç:** `tez_checklist_verify.py` → `chk_svg_preflight`.
  - **Kanonik:** `render-bagimliliklari.md` (librsvg build bağımlılığı).

### B-T · Ön/Arka bölümler & teslim

- [ ] **T-ABS-01** — ÖZET kelime sınırı + Anahtar Sözcükler satırı var.
  - **Mekanizma:** `00c_ozet_summary.qmd` kelime sayımı + anahtar sözcük regex.
  - **Araç:** `tez_checklist_verify.py` → `chk_abstract_wordcount`.
  - **Kanonik:** marmara özet/summary kuralı.
- [ ] **T-PLC-01** — `00a`/`06`/`07` resmi-kişisel alan/yer-tutucu netliği
  (jüri/CV/tarih doldurulmuş). **[MANUEL]**
  - **Mekanizma:** `[YER TUTUCU]` taraması + elle doğrulama.
  - **Araç:** `tez_checklist_verify.py` → `chk_placeholder_scan`.
  - **Kanonik:** marmara ön/arka bölüm şablonu.
- [ ] **T-KVK-01** — Katılımcı fotoğrafı/kimlik ifşası yok. **[MANUEL]**
  - **Mekanizma:** elle KVKK doğrulaması.
  - **Araç:** `tez_checklist_verify.py` → `chk_manual` (KVKK).
  - **Kanonik:** repo ai-audit KVKK katmanı + `talimatname` §2.
- [ ] **T-CERT-01** — Bölüm sertifikaları güncel: bir `chapters/NN.qmd`
  sertifikalandıktan (`sertifikalar/`) sonra değişmişse eski sertifika geçersiz
  sayılır. `sertifikalar/` yoksa MANUEL (bölümler henüz sertifikalanmadı);
  `--closing` modunda değişen-bölüm FAIL.
  - **Mekanizma:** `chapters/NN.qmd` mtime ↔ eşleşen `sertifikalar/*` mtime karşılaştırması.
  - **Araç:** `tez_checklist_verify.py` → `chk_cert_freshness`.
  - **Kanonik:** `talimatname-claude-code.md` §5 + `bolum-finalizasyon-sertifikasyon-playbook.md`.

---

## Kapsama matrisi (madde → eksen → katman → araç)

| ID | Eksen | Katman | Kontrol mekanizması | Araç / uygulayıcı |
|---|---|---|---|---|
| K0-PII-01 | Kapsam/Gizlilik | B (tez) | git check-ignore + ls-files | `chk_pii_gitignore` |
| K0-PII-02 | Kapsam/Gizlilik | A (bölüm) | kolon-adı regex | `chk_pii_no_names` |
| K0-POL-01 | Kapsam/Gizlilik | B (tez) | deny listesi kapsamı | `chk_deny_policy` |
| K0-LCK-01 | Kapsam/Gizlilik | B (tez) | kilit dosyası varlığı | `chk_canonical_lock` |
| K0-PII-03 | Kapsam/Gizlilik | B (tez) | değer-şekilli PII taraması | `chk_pii_value_scan` → `pii_value_scan.py` |
| K1-BIB-01 | Kanıt/Literatür | B (tez) | bib hijyen exit 1/2 | `chk_bib_hygiene` → `bib_hygiene.py` |
| K1-LED-01 | Kanıt/Literatür | B (tez) | ledger drift-guard | `chk_karma_ledger` → `karma_ledger_check.py` |
| K1-CLM-01 | Kanıt/Literatür | B (tez) | birleşik claim kapısı | `chk_claim_cert` → `claim_certification.py` |
| K1-KAR-01 | Kanıt/Literatür | B (tez) | karma cross-arm aşırı-iddia | `chk_cross_arm` → `cross_arm_rhetoric_audit.py` |
| K1-DOI-01 | Kanıt/Literatür | B (tez) | DOI↔Crossref yanlış-atıf [--closing] | `chk_doi_title` → `doi_title_resolve.py` |
| K3-NUM-01 | Format/Kılavuz | A (bölüm) | nokta-ondalık regex (kod hariç) | `chk_decimal_comma` |
| K3-HDG-01 | Format/Kılavuz | A (bölüm) | elle-numara başlık regex | `chk_heading_numbering` |
| K3-FIG-01 | Format/Kılavuz | A (bölüm) | fig etiket ↔ atıf farkı | `chk_fig_refs` |
| K3-TBL-01 | Format/Kılavuz | A (bölüm) | tbl etiket ↔ atıf farkı | `chk_tbl_refs` |
| K3-SEQ-01 | Format/Kılavuz | B (tez) | tr headings ekseni | `chk_tr_headings` → `tr_corpus_audit.py` |
| K4-COH-01 | Türkçe/Akış | B (tez) | coherence ekseni | `chk_tr_coherence` → `tr_corpus_audit.py` |
| K4-REF-01 | Türkçe/Akış | B (tez) | reference-prose ekseni | `chk_tr_refprose` → `tr_corpus_audit.py` |
| K4-TRG-01 | Türkçe/Akış | B (tez) | axis-G çekirdek (G1-G6) | `chk_axis_g` → `tr_sciaudit.py` |
| K4-TERM-01 | Türkçe/Akış | B (tez) | kanonik terim sözlüğü (yasak-varyant) | `chk_term_consistency` → `terim_tutarlilik_audit.py` |
| K5-NUM-01 | AI-reliability/Teknik | B (tez) | sayısal iz denetimi (CSR) | `chk_numeric_trace` → `csr_numeric_trace_audit.py` |
| K5-NUM-02 | AI-reliability/Teknik | B (tez) | ch05 yeniden-ifade iz denetimi | `chk_numeric_trace_discussion` → `csr_numeric_trace_audit.py --csr chapters/05_tartisma_ve_sonuc.qmd` |
| K5-NUM-03 | AI-reliability/Teknik | B (tez) | ch04 Bulgular iz denetimi | `chk_numeric_trace_bulgular` → `csr_numeric_trace_audit.py --csr chapters/04_bulgular.qmd` |
| K5-CAU-01 | AI-reliability/Teknik | B (tez) | nedensel-etiket denetimi | `chk_causal_label` → `csr_causal_label_audit.py` |
| K5-CAU-02 | AI-reliability/Teknik | B (tez) | ch05 nedensel-etiket denetimi | `chk_causal_label_discussion` → `csr_causal_label_audit.py --csr chapters/05_tartisma_ve_sonuc.qmd` |
| K5-HOK-01 | AI-reliability/Teknik | B (tez) | hook küme eşitliği + test | `chk_hooks_twin` |
| K5-LIT-01 | AI-reliability/Teknik | B (tez) | R üretici literal denetimi | `chk_r_generator_literal` → `r_generator_literal_audit.py` |
| K5-TRK-01 | AI-reliability/Teknik | B (tez) | targets format=file izleme | `chk_targets_file_tracking` → `targets_file_tracking_audit.py` |
| K5-GAL-01 | AI-reliability/Teknik | B (tez) | galileo judge tazeliği (advisory) | `chk_galileo_logged` → `run_full_thesis_judge.py --out` |
| P-ENV-01 | Pipeline | B (tez) | renv::status() | `chk_renv_status` |
| P-TAR-01 | Pipeline | B (tez) | tar_outdated() | `chk_targets_fresh` |
| R-RND-01 | Render/Çıktı | B (tez) | quarto render exit | `chk_render_exit` |
| R-XRF-01 | Render/Çıktı | B (tez) | HTML crossref/sızıntı sayımı | `chk_render_crossref` |
| R-PDF-01 | Render/Çıktı | B (tez) | pymupdf A4 + font | `chk_pdf_format` |
| R-SVG-01 | Render/Çıktı | B (tez) | rsvg-convert önkoşulu | `chk_svg_preflight` |
| T-ABS-01 | Ön/Arka/Teslim | B (tez) | ÖZET kelime + anahtar sözcük | `chk_abstract_wordcount` |
| T-PLC-01 | Ön/Arka/Teslim | B (tez) | yer-tutucu tarama + elle | `chk_placeholder_scan` |
| T-KVK-01 | Ön/Arka/Teslim | B (tez) | elle KVKK | `chk_manual` |
| T-CERT-01 | Ön/Arka/Teslim | B (tez) | sertifika tazeliği (mtime) | `chk_cert_freshness` |
| T-RHET-01 | Ön/Arka/Teslim | A (bölüm) | elle retorik okuma | `chk_manual` |

**Toplam:** 39 kontrol · 8 eksen (Kapsam/Gizlilik, Kanıt/Literatür,
Format/Kılavuz, Türkçe/Akış, AI-reliability/Teknik, Pipeline, Render/Çıktı,
Ön/Arka/Teslim). **K1-DOI-01** yalnız `--closing` (ağ), **K5-GAL-01** advisory
(MANUEL) — ikisi de teslim-modu/derin-katman kapsamıdır. **K4-TERM-01** (kanonik
terim sözlüğü) 2026-07-29'da eklendi.

> **2026-07-22 kapsam genişletme (plan `docs/superpowers/plans/2026-07-22-qc-otomatik-zorlama.md`):**
> +8 madde. **P1 kapsam (gövdeye yay):** **K0-PII-03** (değer-şekilli PII tüm
> manuskript), **K5-NUM-03** (ch04 Bulgular sayı izi — kendi sonuçlarımızın
> kaynak-tekilliği), **K5-CAU-02** (ch05 Tartışma nedensel dil). **P2 (orphan
> bağla):** **K5-TRK-01** (`_targets.R` Kaide-2 dosya-izleme), **R-SVG-01**
> (librsvg render önkoşulu), **K4-TRG-01** (bilimsel-yazım Ekseni G çekirdeği).
> **P3 (derin katman/teslim):** **K1-KAR-01** (karma cross-arm aşırı-iddia),
> **T-CERT-01** (bölüm sertifika tazeliği).
> Ayrıca otomatik-ateşleme: `tez_checklist_verify.py --closing` modu (teslimde
> `--fast` reddi + eksik araç/CSR SKIP→FAIL gate-presence invariant),
> `stop_verify` §1.4 nokta-ondalık-p turn-end blocker (iki hook ağacı),
> references.bib PostToolUse bib-hijyen kapısı, ve `install_git_hooks.sh`
> pre-commit kurucu (ana kapıyı commit sınırında zorlar; opt-in).

### Advisory semantik/judge araçları (checklist DIŞI · opt-in · ağ-bağımlı)

Aşağıdakiler 28 HARD/SOFT maddeye dahil DEĞİLDİR (K-ID yok; `tez_checklist_verify.py`
deterministik/offline kalır). Şerit B embedding CANLI (Azure `text-embedding-3-large`)
olduğunda elle koşulan **advisory** katmandır; embedding yoksa string/CRC32'ye degrade eder:

| Araç | Kapsam | İlgili kapı/eksen |
|---|---|---|
| `scripts/util/thesis_semantic.py bib-dup` | semantik yakın-duplikat referans (Jaccard'ın kaçırdığı) | Kapı 2 / K1-BIB (advisory; HARD yalnız `--strict`) |
| `scripts/util/thesis_semantic.py redundancy` | bölümler-arası semantik paragraf tekrarı | Kapı 4 / K4-COH (advisory) |
| `karma_ledger_check.py --semantic` | karma-ledger drift semantik rescue (parafraz-sadık=INFO) | karma sentez |
| `galileo-audit` judge uzantıları (`convergence`/`harking`/`overclaim`/`coherence_judge`) | joint-display uyum, HARKing, aşırı-iddia, anlatı-tutarlılık | Kapı 3/4 (SOFT-block, insan-override) |

Doktrin: `.claude/galileo.local.md` + `.claude/skills/t1dm-tez-rehberi/references/manuskript-denetimi-sciaudit.md` §galileo.
**HARD asla LLM judge'dan gelmez.**

---

## Kapı ↔ eksen ↔ operasyonel checklist haritası

| Kapı | Bu belgedeki eksen(ler) | Operasyonel checklist | Kanonik otorite |
|---|---|---|---|
| Kapı 0 | Kapsam/Gizlilik (K0-*) | `kanit-ve-gizlilik-kontrol-listesi.md` (Gizlilik) | `talimatname-claude-code.md` §2 |
| Kapı 1–2 | Kanıt/Literatür (K1-*) | `kanit-ve-gizlilik-kontrol-listesi.md` (Kanıt) | `02_kanit-haritalari/` ledger |
| Kapı 3 | Format/Kılavuz (K3-*) | `format-kontrol-listesi.md` | marmara §12 (+ §1–§5, §8) |
| Kapı 4 | Türkçe/Akış (K4-*) | `turkce-bilimsel-yazim-denetimi.md` · `insan-turkcesi-retorik-playbook.md` | sci-audit axis G |
| Kapı 5 | AI-reliability/Teknik (K5-*) | `ai-mcp-kullanim-kontrol-listesi.md` | sci-audit axes A–F + repo ai-audit |
| — (üretilebilirlik) | Pipeline (P-*) · Render (R-*) | `render-bagimliliklari.md` | `renv.lock` · `_targets.R` · marmara §1 |
| — (teslim) | Ön/Arka/Teslim (T-*) | (playbook ön/arka + KVKK) | marmara ön/arka şablonu + repo ai-audit KVKK |

## Bakım kuralı

- **Tek doğruluk kaynağı `scripts/util/tez_checklist_verify.py` kayıt
  kaydıdır.** Yeni kontrol eklenince önce script'e `add(...)` ile girer, sonra
  bu belgeye ID + mekanizma + araç satırı işlenir.
- Her değişiklikten sonra `python3 scripts/util/tez_checklist_verify.py
  --audit-doc` **0 yetim** vermelidir (CI/pre-commit koşulabilir).
- Bu belge **kural tanımlamaz**; kural değişikliği önce kanonik otoriteye
  (marmara §, talimatname §, playbook) yazılır, buraya yalnız pointer düşer.
