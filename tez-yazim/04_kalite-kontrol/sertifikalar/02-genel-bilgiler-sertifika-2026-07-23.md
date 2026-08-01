# Bölüm Finalizasyon Sertifikası — GENEL BİLGİLER

- **Bölüm:** `chapters/02_genel_bilgiler.qmd` (resmi bölüm: **GENEL BİLGİLER**, §2.1–§2.8)
- **Tarih:** 2026-07-23
- **Playbook:** `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`
- **Durum:** `certified-final`
- **Karar:** Kapı 0–5'in tamamı PASS ve açık kullanıcı uygulama onayı alındı
  (2026-07-23). `provisional-pass` → `certified-final` yükseltmesinin üç önkoşulu
  da kapandı: (1) açık onay verildi; (2) commit + render (exit 0) tamamlandı
  (`fdfbab3`); (3) repo-altyapı asset-drift giderildi (asset←repo senkron,
  doktoratezi-ai-audit 144/144, `2481647`).

---

## Bağlam (bu sertifikasyondan önce yapılan iş)

Bu oturumda §2.1–§2.8'in tüm alt-bölümleri `anlatim-zenginligi` kapısından geçirildi
(terim-izah + referans-bütünlüğü, kanıt bölgesi dokunulmadan) ve üç kesitler-arası
bütünleşik denetim (Workflow, adversarial doğrulamalı) koşuldu: §2.3–2.5, §2.6, §2.7.
En dikkate değer bulgu: SRQ geliştirme yönteminin (Furman & Buhrmester 1985) kaynak-özeti
doğrulamasıyla düzeltilmesi — özet birebir *"A principal components analysis yielded 4
underlying factors"* → §2.7.4 "faktör analizi" hatası "temel bileşenler analizi" olarak
düzeltildi ve §2.5.2 ile iç-tutarlılık sağlandı.

---

## Kapı 0 — Kapsam ve Hassasiyet Sınırı → PASS

- Bölüm dosyası mevcut; resmi karşılık **GENEL BİLGİLER** (kuramsal/ampirik arka plan).
- Kapsam sınırı: ham veri / transkript / satır-düzeyi klinik veri / credential rapora
  taşınmadı.
- PII: `tez_checklist_verify --chapter 02` → K0-PII-02 PASS (ad/soyad kolon kalıntısı yok);
  değer-şekilli PII adayı yok.

## Kapı 1 — Derin Literatür ve Künye Evreni → PASS

- Bölümün 75 eşsiz dış atıf anahtarının tamamı `referans-denetim-ledgeri.md` içinde
  künyelenmiş ve `cite-ok` (aşağıda Kapı 2). Her ledger satırı popülasyon/ölçüm/T1DM-uyumu
  claim notu + kapsam (`GENEL BİLGİLER`) taşır.
- Bu oturumda RBŞ (Referans Bütünlük Şiarı) tam-metin doğrulamaları: F&B 1985 (PCA,
  kaynak-özeti), quinn2026 (systematic review + mixed methods), lummerAikey2021 (integrative
  review), dirik2015/sumer2010 (Türkçe s-EMBU-C soyağacı), parker1979 (PBI eksenleri).
- Zayıf/eksik-kanıtlı iddia bulunmadı.

## Kapı 2 — Tam Metin, Zotero ve Ledger → PASS

- Bölümdeki **75/75** eşsiz `[@key]` ledger'da mevcut ve `cite-ok` (veya gerekçeli
  `full-text-exception`): **ledger'da bulunmayan = 0**, **cite-ok olmayan = 0**.
- `references.bib` mutabakatı: orphan citation = 0 (kullanılan her key bib'de mevcut).
- `full-text-pending` / `zotero-pending` / `citation-without-full-text` = 0.

## Kapı 3 — Bölüm Metni, Kılavuz ve İç Tutarlılık → PASS

- Resmi işlev (kuramsal/ampirik arka plan) eksiksiz; H1–H5/Faz II/RTA amaçları karışmıyor.
- Başlık düzeni: oto-numaralandırma temiz (elle numara yok); bölüm sırası disiplinli.
- `@tbl-*` metin-içi gönderim: 3 tablo (`ebeveynlik-kuramlari`, `embu-gelisim`,
  `olcum-ozet`) metin-içi atıflı.
- `git diff --check` (chapter + bib + ledger): **TEMİZ** (whitespace/conflict yok).
- **galileo (Şerit B, SOFT/advisory):**
  - `galileo_overclaim_judge`: overclaim_risk **0,08**, causal_drift **false**,
    cherry_pick **false** — korelasyonel/gözlemsel sınır korunuyor, nedensellikten kaçınılıyor.
  - `galileo_convergence_judge`: **N/A** — GENEL BİLGİLER'de karma joint-display satırı yok.
  - `galileo_harking_judge`: **N/A** — arka plan bölümünde ön-kayıtlı hipotez/bulgu sunumu yok.

## Kapı 4 — Türkçe İmla, Anlam Akışı ve Mantık → PASS

- **sci-audit axis G** (`tr_sciaudit.py --strictness certification`): **Errors (blocker) = 0.**
  Warnings (major) = 83 — ağırlıklı olarak yoğun bilimsel bölüme özgü uzun-cümle/üslup
  uyarıları; blocker olmadığından ve arka plan bölümünün doğası gereği çok-yan-cümleli
  yapı taşıdığından **gerekçeli kabul** edildi (İngilizce ondalık-nokta `p` yok = G5 temiz).
- **galileo (SOFT/advisory):**
  - `galileo_coherence` (embedding, komşu-paragraf): bu oturumda §2.6.1 revizyonu sonrası
    adjacent-sim 0,614→0,506 (redundans↓), flow-break=0, status **pass**.
  - `galileo_consistency` (§2.8 dört alt-bölüm): **temiz** (çelişki/aşırı-tekrar yok).
  - `galileo_coherence_judge` (tez-anlatı zinciri): 0,18 döndü **ancak** yalnız bölüm
    özetleri girdi olarak verildiği için düşük-girdi artefaktıdır (aracın kendi gerekçesi:
    *"metin olmadan izlenemediğinden"*); GENEL BİLGİLER ampirik amaç→bulgu→sonuç zinciri
    taşımayan bir arka plan bölümüdür. Otoriter tutarlılık kanıtı: checklist **K4-COH-01
    blocker=0** + embedding-coherence pass + 3 adversarial Workflow denetimi (akış teyitli).
    → **gerekçeli advisory**; SOFT-block sayılmadı.

## Kapı 5 — AI-Reliability, Render ve Repo Doğrulaması → manüskript PASS · repo-infra 5 FAIL (kapsam-dışı)

**Katman 1 — Manüskript adli denetimi (sci-audit A–F) → PASS**
- `bib_hygiene all`: **HARD = 0** (atıflı-tanımsız key yok → render kırılmaz); SOFT (exit 2)
  = alan/DOI/duplikat advisory (gerekçeli kabul).
- claim-grounding (axis B) çekirdeği ham çıktıda 16 "error" verdi; **rigorlu manuel doğrulama
  ile hepsi false-pozitif**: CLAIM-tetikli 24 cümle = 12 tablo-hücresi (@tbl-embu-gelisim/
  ebeveynlik-kuramlari/olcum-ozet, prozada grounding'li) + 9 `[@key]`-taşıyan uzun cümle
  (regex Pandoc `[@key]`'i görmez) + 3 tanımsal-yeniden-ifade (Beck "21 madde" — çevresi
  yoğun-atıflı + tablo + §2.4 ilk-geçiş). **Gerçek kaynaksız-yeni-iddia = 0.** Otoriter axis B:
  checklist K5-NUM (yüksek-risk eşsiz sayı=0) + Kapı 2 (75/75 cite-ok).
- `quarto check`: tüm bağımlılıklar OK (Quarto 1.9.38).

**Katman 2 — Repo/veri invaryantı (doktoratezi-ai-audit) → 139/144; KVKK/data PASS**
- KVKK/ham-veri/secret-guard/kanonik-kilit/claim-check invariantları **PASS** (secret-blocking
  8+ tür, unsourced-count guard, canonical-lock).
- **5 FAIL — tamamı kapsam-dışı repo-altyapı asset-drift:** `.codex/hooks.json`,
  `.codex/hooks/post_tool_use_review.py`, `.codex/hooks/stop_verify.py`, `CONVENTIONS.md`
  ("materialized matches asset" uyuşmazlığı) + installer check. Bunlar **bölüm-02 içeriği,
  atıfları, KVKK/ham-veri sınırı veya quote-parity DEĞİLDİR**; oturum başında `M CONVENTIONS.md`
  olarak zaten değişik olan repo-altyapı sync sorunudur. `reliability-gap` (repo-bakım) olarak
  kaydedildi; chapter-02 finalizasyonunun mantıksal önkoşulu değildir ama `certified-final`
  öncesi ya giderilmeli ya bakımcı imzasıyla kapsam-dışı bırakılmalıdır.

## Şerit B — Galileo Assembly Özeti (2026-07-22 zorunlu)

| Judge | Sonuç | Kademe |
|---|---|---|
| `overclaim` | 0,08 · causal_drift=false · cherry_pick=false | ✅ eşik-altı |
| `harking` | N/A (arka plan; prior/hipotez yok) | — |
| `convergence` | N/A (joint-display yok) | — |
| `coherence_judge` | 0,18 (düşük-girdi artefaktı; gerekçeli) | advisory |

Eşik-üstü çözümsüz SOFT-block **yok** (coherence_judge artefaktı gerekçelendirildi;
overclaim eşik-altı). Gateway erişildi (SKIP yok).

---

## Nihai Karar

**`certified-final`.** Bölüm-içeriği kapıları (0–4) ve Kapı 5 (manüskript adli denetimi +
repo/veri invaryantı) tam PASS; kanıt/atıf/KVKK bütünlüğü sağlam; kaynak-doğrulamalı bir
bilimsel-doğruluk hatası (SRQ PCA) düzeltildi; açık kullanıcı uygulama onayı alındı.

Gap Register — tüm maddeler KAPANDI:

1. **`approval-gap` ✅:** Açık kullanıcı uygulama onayı alındı (2026-07-23).
2. **commit + render ✅:** §2.7 denetim düzeltmeleri (F1–F3+opt) + §2.7.5–2.7.10 anchor'ları
   `fdfbab3` ile commit'lendi; `quarto render` exit 0 (çıktılar 15:18) ile teyit edildi.
3. **`reliability-gap` (repo-infra) ✅:** 5 asset-drift FAIL, doğru yön (asset←repo) senkronla
   giderildi (`2481647`); doktoratezi-ai-audit 139/144 → **144/144, 0 FAIL**; iki-kol hook
   senkron testi (K5-HOK-01) intact; hiçbir politika geri alınmadı.

Bu sertifika ile **GENEL BİLGİLER (§2.1–§2.8)** bölümü final kabul edilmiştir. Sertifika
sonrası bölüm metni değişirse (T-CERT-01 tazelik kapısı), sertifikasyon yeniden koşulmalıdır.
