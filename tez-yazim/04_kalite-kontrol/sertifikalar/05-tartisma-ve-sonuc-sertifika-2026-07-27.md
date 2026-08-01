# 05 TARTIŞMA ve SONUÇ — Bölüm Finalizasyon Sertifikası (CERTIFIED-FINAL)

> **Tarih:** 2026-07-27 · **Dal:** `feat/qc-otomatik-zorlama-kapsam`
> **Durum:** `certified-final` — **açık kullanıcı onayıyla** yükseltildi
> (2026-07-27, "onaylıyorum"). Kalan kapanış adımları §Bekleyen'de (kalite
> iyileştirmesi; blocker değil).
> **Tetikleyici:** P1–P14 parça-bazlı `/anlatim-zenginligi` denetimi + bölümün
> tamamı için bütüncül (holistik) anlatım-zenginliği denetimi (anlaşılırlık ·
> dilde optimum anlam · akış mantığı) tamamlandıktan sonra tam Kapı 0–5
> yeniden-sertifikasyonu.

---

## YENİDEN-SERTİFİKASYON — Nesir sadeleştirme turu (2026-07-27, ikinci geçiş)

> **Tetikleyici:** Bölümün tamamı için 13-pasaj-gruplu **nesir sadeleştirme**
> (uzun iç-içe cümlelerin kısa, açık cümlelere bölünmesi) tamamlandıktan sonra
> kullanıcı isteğiyle ("tartışma kısmında yaptığın tüm revizyonları bütünlüklü
> biçimde incele, bölüm sertifikasyonunu tekrar yürüt") yeniden yürütülen tam
> Kapı 0–5 denetimi.
> **Kapsam:** yalnız `chapters/05_tartisma_ve_sonuc.qmd` nesir katmanı; sayı ·
> yön · anlamlılık · büyüklük · atıf · kaynak-yorumu · tablo/şekil referansı ·
> başlık mimarisi **dokunulmadı**.
> **Değişim ölçeği:** 810 ekleme / 745 silme (net +65 satır, cümle bölmelerinden);
> 1017→1082 satır.

### Bütüncül değişmezlik doğrulaması (HEAD ↔ mevcut, birebir)

| Değişmez | Yöntem | Sonuç |
|---|---|---|
| Atıf anahtarları (`@key`) | frekanslı küme diff | **fark 0** (identik) |
| Ondalık sayı değerleri | frekanslı küme diff | **fark 0** (identik) |
| İstatistik tokenları (F/p/β/ICC/CFI/RMSEA/OR/τ/ω/ρ/α/%) | regex frekanslı diff | **fark 0** |
| Kaynak yorumları (`<!-- kaynak: -->`) | frekanslı küme diff | **fark 0** |
| Tablo/şekil referansları (`@tbl-`/`@fig-`) | frekanslı küme diff | **fark 0** |
| Tüm sayı-içeren tokenlar (noktalama soyut.) | frekanslı küme diff | **fark 0** (tek fark cümle-sonu `.`/`,`/`;`) |
| Hipotez etiketleri (H0–H5) | frekans diff | **birebir** (5/8/6/8/4/3) |
| Bracket dengesi `[ ]` | sayım | **111=111** (HEAD ile aynı) |
| Başlık mimarisi (satır+içerik) | numaralı diff | **birebir aynı** |

### Kapı 0–5 yeniden-denetim sonuçları (sadeleştirme turu)

| Kapı | Durum | Kanıt |
|---|---|---|
| **0 — Kapsam/Gizlilik** | ✓ | PII/ham-veri/credential/`.csv`/`.lock` sızıntısı **0**; başlık mimarisi satır-düzeyinde birebir korundu. |
| **1 — Derin literatür** | ✓ | 104 benzersiz atfın tamamı `references.bib`'de künyeli (dangling **0**); atıf kümesi HEAD ile birebir → literatür bütünlüğü değişmedi. Not: `chan2025spirit`, `hopewell2025consort` ledger'da kayıtsız ama **pre-existing** (HEAD'de de vardı, künyeleri mevcut). |
| **2 — Full-text/Zotero/Ledger** | ✓ | `bib_hygiene reconcile` exit 0; **HARD (atıflı-tanımsız) = 0**; atıf kümesi değişmediğinden cite-ok/full-text-ok durumu korundu. SOFT (3 DOI-eksik) + INFO (orphan) pre-existing. |
| **3 — Metin/Kılavuz uyumu** | ✓ | `karma_ledger_check` **TEMİZ (0 bulgu, exit 0)**; cite sözdizimi geçerli (çok-atıflı gruplar kapalı); bracket 111=111; format bütünlüğü korundu. |
| **4 — Türkçe imla/akış** | ✓ | `tr_corpus_audit all --fail-on blocker` exit 0 (**blocker 0**); ch05'e sadeleştirmeyle eklenen yeni dil/imla bulgusu **yok**. H-TRANS (4/65) ve H-ABBR (H0–H5) pre-existing/yanlış-pozitif. |
| **5 — AI-reliability/Render** | ✓ | `claim_certification` exit 0 (**HARD atıf=0 · high-risk kaynaksız sayı=0 · eşleşmeyen sayı=0**); `quarto check` tüm motorlar (markdown/knitr/python) **OK**; repo-invariant: yalnız ch05 sadeleştirmesi kapsam-içi. |

### Kapsam-dışı çalışma-ağacı değişiklikleri (bu turda dokunulmadı)

Çalışma ağacında `00c_ozet_summary.qmd`, `03_gerec_ve_yontem.qmd`,
`04_bulgular.qmd` ve `outputs/quarto/thesis.{html,pdf,docx}` da değişik
görünmektedir. İnceleme: bu `.qmd` değişiklikleri **yalnız terminoloji
netleştirmesi** ("aile" → istatistiksel "test ailesi"); **ondalık-sayı farkı=0,
atıf-farkı=0**. Bunlar önceki bir oturumdan kalma, bu sadeleştirme turunun
kapsamı dışıdır ve bu sertifika onları kapsamaz. Geçici tek-bölüm render
artefaktları (`chapters/05_tartisma_ve_sonuc.html`, `_files/`) temizlendi.

**Sadeleştirme turu kararı:** Kapı 0–5'in tamamı **blocker'sız** geçti; nesir
sadeleştirmesi kanıt-değerini (sayı/yön/anlamlılık/büyüklük/atıf) birebir korudu.
Bölümün `certified-final` durumu **sürdürülür**. Tek fark cümle-bölme
noktalamasıdır; içerik bütünlüğü ihlali yoktur.

---

## İş özeti

Tartışma bölümü (`chapters/05_tartisma_ve_sonuc.qmd`, ~10.300 kelime, 102 benzersiz
dış atıf) alt başlıksız akıcı Marmara-uyumlu yorum bölümü olarak; tüm bulguları
(H1–H5 + [KEŞFİSEL] katmanlar + nitel makro-temalar + karma entegrasyon) en geniş
tam-metin literatürle tartışmaktadır. Bu sertifika, iki ardışık denetim turundan
sonra çalıştırılan tam Kapı 0–5 denetimini kaydeder:

1. **P1–P14 parça-bazlı denetim** (önceki): ledger'a işlendi; 2 kanıt-değeri
   düzeltmesi (P8 `dinleyici2019` APA atıf tamamlama; P12 Penelo 2012 RMSEA
   0,055→0,054).
2. **Bütüncül holistik denetim** (2026-07-27): tüm bölüm tek bütün olarak
   anlaşılırlık/dil/akış eksenlerinde denetlendi; 5 düzenleme uygulandı (Ö1–Ö5);
   **kanıt-değeri değişmedi** (sayı/yön/anlamlılık/büyüklük/sıra korundu).

- Kanıt/atıf ledgeri: `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md`
  (ch05 holistik denetim özeti eklendi)
- Bölüm: `chapters/05_tartisma_ve_sonuc.qmd` (102 benzersiz atıf, tümü bib+ledger'da)
- Kaynakça: `references/references.bib` (346 giriş)

## Kapı 0–5 durumu

| Kapı | Durum | Kanıt |
|---|---|---|
| **0 — Kapsam/Gizlilik** | ✓ | Dosya + hazırlık briefi (`03_bolum-hazirlik/05_tartisma-ve-sonuc.md`) + kritik-kaynak manifesti mevcut; ch05→resmi "TARTIŞMA ve SONUÇ" karşılığı net; PII/ham-veri/credential sınır ihlali **0**; tek `#` başlık, alt başlık yok (mimari uyumlu). |
| **1 — Derin literatür** | ✓ | 102 dış atfın tamamı künyeli (DOI/PMID/ID) ve ledger'da kayıtlı; bib'de tanımsız **0**; 12 kaynak `abstract`-düzeyi ama hiçbiri bir birincil-hipotez bulgusunun tekil dayanağı değil (metodolojik-prensip / destekleyici-karşılaştırma). |
| **2 — Full-text/Zotero/Bağlam** | ✓ (kısmi) | 25 `cite-ok` + 26 `full-text-ok` (2026-07-27 turunda 8 `full-text-exception` → `full-text-ok`: 6 Annas `read_article`, 1 OpenAthens `oa_fetch_fulltext`, 1 kullanıcı CC-BY OA PDF) + 0 `full-text-exception` + 1 kitap (`kennyKashyCook2006` `full-text-ok`/Zotero-pin bekliyor) + 12 `abstract`; semantik bib-dup HARD **0**, advisory **0**. **Bekleyen:** 12 abstract-only kaynak için tam-metin yükseltme + Zotero item-key mutabakatı. |
| **3 — Metin/Kılavuz uyumu** | ✓ | Format: tek `#`, alt başlık yok, İngilizce ondalık-nokta p **0** (tüm ondalık-nokta eşleşmeleri §4.x bölüm-ref veya binlik-ayraç); `karma_ledger_check` exit 0 (HARD **0**); semantik redundancy (leitmotif) **temiz**; galileo overclaim 0,12 · harking 0,06 · convergence over-integration=false. |
| **4 — Türkçe imla/akış** | ✓ | `tr_sciaudit` axis G **Errors (blocker) = 0** (137 warning/40 info advisory — çoğu `sentence-long`; en uzunları holistik turda bölündü); galileo coherence **tam-bağlamda 0,78** (izole-segment 0,46 skoru izolasyon artefaktı olarak doğrulandı). |
| **5 — AI-reliability/Render** | ✓ | `bib_hygiene all` exit 0, HARD atıflı-tanımsız **0**; repo-invariant `test_repo_ai_reliability.py` **144/144 passed**; `git diff --check` temiz; `quarto check` tüm motorlar (markdown/knitr/python) **OK**; sci-audit A–F: axis B orphan **0** (30 finding → tümü @cite veya Bulgular §4.x/@tbl bağıyla doğrulandı), axis C **0/0/0**, axis D error **0**, ai-transparency error **0**. |

## Holistik denetim düzeltmeleri (kanıt-değeri değişmedi)

| ID | Eksen | Değişiklik |
|---|---|---|
| Ö1 | anlaşılırlık | 80-kelimelik H1 duyarlılık cümlesi iki cümleye bölündü (b/q/d değerleri aynen). |
| Ö2 | anlaşılırlık | Dört başlıklı öneriler bloğu taranabilir cümlelere ayrıldı; "dış validasyonu […];" → "dış validasyondan geçirilmelidir" (yüklem netleştirme). |
| Ö3 | dil (tekrar) | "ortak takvim desteği dengeli bağımsız örneklem" leitmotifinin 3 birebir tekrarından ikisi eşanlamlı varyasyonla seyreltildi. |
| Ö4 | dil (tekrar) | "öneri düzeyinde" disclaimer'ı keşifsel-statü çapasına bağlandı. |
| Ö5 | akış | "Dördüncü olarak" numaralandırması robustluk serisine kilitlendi; artık-ilişki serisiyle görsel çakışma giderildi. |

## sci-audit A–G özeti (0 blocker)

- **A (atıf bütünlüğü):** 102 atıf bib+ledger'da; render 0 çözümsüz; 7 exception gerekçeli.
- **B (kaynaksız iddia):** deterministik orphan **0** (30 araç-finding paragraf-içi kaynak bağıyla FP doğrulandı).
- **C (istatistik):** statcheck/GRIM/GRIMMER/SPRITE/CI/effect-size **0 tutarsızlık**.
- **D (halüsinasyon sinyali):** error **0** (1 warning "her zaman yansımayabileceğini" ihtiyat ifadesi = FP).
- **E (kılavuz):** tartışma bölümünde zorunlu yapısal alt-bölüm yok.
- **F (AI şeffaflık):** error **0** (bölüm-düzeyi beyan tez düzeyi `ai_use_log` ile).
- **G (Türkçe bilimsel dil):** blocker **0**; 137 advisory warning.
- Rapor: `tez-yazim/04_kalite-kontrol/raporlar/05-tartisma-tr-sciaudit.md`

## Bekleyen maddeler — 2026-07-27 kapanış turu

1. **12 abstract-only kaynak → tam-metin yükseltme: ✓ TAMAMLANDI.**
   - **3 `full-text-ok`:** `petersen2019lcaChildMH` (Europe PMC OA cc-by, PMC6548989),
     `sorgente2025lcaReview` (Europe PMC OA cc-by, PMC12494633),
     `luqueFernandez2016paradox` (Minerva vectorstore, Springer Nature).
   - **7 kaynak `full-text-exception` → `full-text-ok` (2026-07-27, kurumsal köprü):**
     `hernan2004selectionBias` (~56 K), `olsenKenny2006interchangeableDyads` (~59 K),
     `marsh2014esem` (~59 K), `akdoganDuken2026caregiver` (~43 K), `goodman1999risk`
     (~54 K), `vangampelaere2020families` (~60 K) — Annas `read_article` DOI-teyitli
     tam metin (başlık+yazar birebir); `erdim2022siblings` — OpenAthens
     `oa_fetch_fulltext` lisanslı tam metin (11 sayfa PDF, anamnesis'e ingest). Önceki
     "OpenAthens/Annas bu CLI köprüsünden erişilemez" notu düzeltildi: `evidentia_http_client.py`
     köprüsü `.env` kimlikleriyle her iki connector'a erişir.
   - **8. kaynak `blamires2024umbrella` → `full-text-ok`:** kullanıcının sağladığı
     yayıncı PDF'i (`eksikler/PIIS088259632400099X.pdf`, CC-BY açık erişim,
     J Pediatr Nurs 77:191–203) ~99 K karakter/14.320 kelime; başlık + 5 yazar + DOI +
     dört tema (adjusting to changes / wanting to help / living the ups and downs /
     living the changes) birebir doğrulandı. Böylece 8/8 kaynak tam-metin-teyitli.
   - `barryMenkhaus2020t1dScreening` zaten `reliability-ok` (Zotero key `KCV6RENC`).
   - `karma_ledger_check` exit 0 (yükseltmeler sonrası). Bu 12 kaynağın hiçbiri bir
     birincil-hipotez bulgusunun tekil dayanağı değildir.

2. **Zotero item-key mutabakatı: ✓ DENETLENDİ (kalan iş kütüphane-yazımı).**
   - Bağlantı ok (userID 17265855, scope 9ZFDHMZA); `reconcile` **undefined
     (atıflı-tanımsız, render-kritik) = 0**.
   - ch05 kaynak item-key kapsaması **94/102 (%92)** zaten mevcut.
   - Kalan kaynaklar için item **oluşturma/import** `zotero_add_to_collection`
     kapsamı dışında (araç yalnız var-olan `item_key`'i koleksiyona bağlar); yeni
     item BibTeX'ten oluşturma = kütüphane yazımı → Zotero connector + açık kullanıcı
     onayı gerektirir. Render-kritik hiçbir eksik yok.

3. **İki-kol AI-reliability: ✓ TAMAMLANDI (2026-07-27).**
   - **Nicel kol** (`/tez-dogrulama`): doktoratezi-ai-audit **144/144**; Claude hook
     sözleşme **19/19**; hook derleme temiz; veri yönetişimi R testleri
     (`test_reproducibility_lock`, `test_final_reference_loading`,
     `test_data_governance`) **3× exit 0** (sessiz = PASS).
   - **Nitel kol** (`t1dm-qual-ai-audit`): **55/55 passed**.

4. **Açık kullanıcı onayı: ✓** (2026-07-27, "onaylıyorum") — certified-final.

### Kalan (blocker değil, insan/connector gerektirir)
- 8 `full-text-exception` kaynağın tamamı 2026-07-27'de `full-text-ok`'a yükseltildi
  (7 kurumsal köprü: Annas `read_article` / OpenAthens `oa_fetch_fulltext`; 1
  `blamires2024umbrella` kullanıcının sağladığı CC-BY OA yayıncı PDF'i). Kalan
  `full-text-exception` **0**.
- Yeni yükseltilen kaynakların Zotero kütüphanesine import + koleksiyon bağlama
  (kütüphane yazımı; connector oturumu gerektirir).

## Karar

Kapı 0–5'in tamamı **blocker'sız** geçti. Otomatikleştirilebilir denetimlerin tümü
temiz. **Durum: `certified-final`** — kullanıcı 2026-07-27'de açıkça onayladı
("onaylıyorum"). §Bekleyen maddeleri (12 abstract-only tam-metin yükseltmesi,
Zotero item-key mutabakatı, iki-kol AI-reliability) blocker değil; kütüphane-yazımı
veya kalite-iyileştirme adımlarıdır ve bölüm kapanışını engellemez.
