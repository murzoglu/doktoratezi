# Klinisyen Diline Uyarlama — Çalışma Journal'ı

Bu journal, `/klinisyen-diline-uyarlama` yetkinliğinin çalışma günlüğüdür. Amaç: hangi pasajın
klinisyen jüriye uyarlandığını, ne yapıldığını, tez-geneli etkilerini ve **yapılması
gerekenleri** izlemek.

**Ritüel (zorunlu):**

- **Seans başı:** bu journal'ı oku — *Durum panosu* + *Backlog*'a bak; sıradaki işi seç,
  açık takipleri gör.
- **Seans sonu:** işlenen her pasaj için *Seans günlükleri*'ne giriş ekle; *Durum panosu*'nu
  ve *Backlog*'u güncelle.

Kapsam sınırı: bu yetkinlik yalnız **register/anlaşılırlık** uyarlar; sayı/bulgu/yön/anlamlılık/
atıf DOKUNULMAZ (bkz. `.claude/skills/klinisyen-diline-uyarlama/SKILL.md`).

---

## Durum panosu

| Bölüm / Pasaj | Durum | Son dokunuş | Not |
| --- | --- | --- | --- |
| `03_gerec_ve_yontem.qmd` (D1–D8, tam bölüm) | uygulandı | 2026-07-30 | register v2; 10 dipnot; opak coinage 0 |
| `04_bulgular.qmd` (W1–K2 + kapanış) | uygulandı | 2026-07-30 | hibrit de-dup; K5-NUM-03 PASS |
| `05_tartisma_ve_sonuc.qmd` (T1–T6, tam bölüm) | uygulandı | 2026-07-30 | 522/522 span; galileo faithfulness 0,99 |
| `01`, `02`, `00c`, `07` | bekliyor | — | — |

Durum değerleri: `bekliyor` · `işlendi-onay bekliyor` · `uygulandı` · `certified`.

---

## Backlog (yapılacaklar — öncelikli)

Her madde: **pasaj** · **anlaşılırlık sorunu** · **tez-geneli takip** (terim tutarlılığı /
forward-ref / özet-summary yansıması).

- [x] **BÜYÜK İŞ — 3 bölüm tam uyarlama:** `03` + `04` + `05` tamamı (2026-07-30 itibarıyla ÜÇÜ DE
  UYGULANDI). Sistematik plan: **`klinisyen-uyarlama-3bolum-plani.md`** (bu klasör).
- [ ] `05` kapanışı için **tam-tez render** (bkz. GOTCHA: önce `_freeze/thesis` temizlenmeli);
  ardından `/bolum-sertifika` ile ch05 sertifikası tazelenmeli (T-CERT-01 şu an MANUEL).
- [ ] `05` H-TRANS advisory: paragraf bölme sonrası geçiş belirteci oranı 7/115 (0,06) — mutlak
  sayı değişmedi, payda büyüdü. İstenirse `anlatim-zenginligi` kapısında geçiş nesri eklenir
  (bu kapının işi değil — vektör aşağı).
- [ ] `01`, `02`, `00c`, `07` bölümleri için aynı register v2 dalgası.

---

## Altyapı notu

- **Üretim mimarisi: kısıtlı-yeniden-yazım harness'i** `scripts/eval/constrained_rewrite.py`
  (tracked; 15 birim test `tests/test_constrained_rewrite.py`). Kanıt bütünlüğünü modelden alıp
  **deterministik koda** taşır: immutable span (sayı/`@tbl`·`@fig`/`[@cite]`/çekince/etiket) →
  `⟦KDUk⟧` maskele → üret → **verify** (retry) → **splice**. Sayı/atıf/token/çekince düşmesi
  **mekanik imkânsız**; Claude Adım 2 yalnız modelin bağlaç nesrini denetler.
- Üretici: **portkey-galileo gateway modeli** (şu an `@org-azure-general-us2-001-001` /
  `gpt-5.5-2026-04-24`), köprü `scripts/eval/gemini_reformulate.py` (gitignored). Config `.env`
  `GALILEO_GEMINI_CONFIG`. gpt-5.x yalnız varsayılan `temperature`(1); köprü göndermez. (Önceki
  gemini-3.5-flash izni yoktu — HTTP 412; GPT-5.5 config'iyle çözüldü.)
- **`default_system` = klinik hekim register'ı** (hekim = KDT altyapılı klinisyen): sayı KALIR,
  matematiksel formül→teknik ek, klinik "so-what" önce, kısa cümle, gloss yalnız yabancı
  psikometrik model.
- **3 guardrail (kirlenme sınıfları için):** (1) paragraf-bazlı glossary süzme + EK-BİLGİ yasağı
  (dump'ı keser); (2) META-NOT/note-echo yasağı ("(klinik-kesme çekincesi)" gibi echo'yu keser);
  (3) İSTATİSTİK-META yasağı (p/%95 GA'yı tanımlayan/"…ile raporlanır" genel filler'ı keser).
- **Maskeleme granülerliği doktrini:** çekince/kapsam sınırı + **tam-yüklemli kapsam öbeği** TAM
  CÜMLE maskelenir (parça maskesi run-on dikişi doğurur — H5 ¶4 dersi); kalın etiket maskelenir.
- **Register düzeltmesi (2026-07-29, kullanıcı):** klinik-lead **"poliklinikte" gibi klinik-ortam
  ifadesi KULLANMAZ** (yanlış register) → "klinik olarak / klinik açıdan / aile değerlendirmesinde".

---

## Seans günlükleri (ters-kronolojik)

<!-- Şablon — her giriş için kopyala:
### YYYY-AA-GG — <pasaj kısa adı>
- **Pasaj:** dosya:satır (ör. chapters/04_bulgular.qmd:496-505)
- **Üretici:** Gemini <model> · <tur sayısı> tur
- **Ne yapıldı:** <kısa özet: hangi terimler çevrildi, hangi cümleler bölündü>
- **Yeniden sıralama:** yok | <var → gerekçe>
- **Çıkan F# bulguları + karar:** <ör. F1 tur-1'de yakalandı → yeniden yönlendirildi → tur-2 temiz>
- **Kapı sonucu:** sci-audit HARD <0/…> · galileo_judge groundedness/faithfulness <…> · advisory <…>
- **Tez-geneli bağlam etkisi:** <terim tutarlılığı / çapraz-ref / özet-summary / tekrar>
- **Açık takipler:** <backlog'a eklenenler>
-->

### 2026-07-29b — Register yeniden-kalibrasyonu + Claude-authored pivot (H5 pilot, test modu)

- **Kullanıcı geri bildirimi zinciri:** (1) hâlâ kompleks, daha da sadeleştir; (2) "poliklinikte"
  yanlış register; (3) sadeleştirme Marmara'ya uymalı; (4) v6 üretici-zorlaması ¶8'de kaynağa-
  aykırı verdikt HALÜSİNE etti → **mimari pivot: Claude YAZAR, harness DOĞRULAR**.
- **Register (default_system) eklendi:** MARMARA-resmi (retorik soru/eksiltili YOK), MANŞET/GRID
  (grid→@tbl), YÖNTEM MEKANİĞİ→teknik ek, "poliklinik" yasağı.
- **Yeni fonksiyon:** `verify_authored_spans(authored, required)` — Claude-yazımı metinde
  DOKUNULMAZ span (sayı/token/atıf/**verdikt-verbatim**) düşme/mutasyonunu mekanik yakalar
  (halüsinasyonu değil → Adım 2/galileo). 16 birim test yeşil.
- **H5 v6 (üretici):** grid-excision + yön-guard tuttu AMA ¶8 verdikt halüsinasyonu + ¶3 mekanik
  geri-ekleme → üretici-zorlaması tavan. **H5 v7 (Claude-authored):** 8/8 span PASS (47 span),
  halüsinasyon yok, verdikt verbatim, grid→tablo, yöntem→ek, Marmara-sade → **kullanıcı onayladı**.
- **Tablo kapsamı doğrulandı:** `apa_table_h5_concordance` (Tablo 13) ICC'yi alt ölçek×grup üretir
  → ¶3 grid→tablo veri-kaybı değil.
- **Kural:** çekince + **verdikt VERBATIM** (parafraz yasak); yalnız bağlaç/çerçeve sadeleşir.
- **Açık takip:** ¶3 ICC(A,1)/ICC(2,1) + ¶4 formül/a4 türetimi teze uygulanırken **Ekler**'e eklenecek.

### 2026-07-29 — Harness inşa + kalibrasyon (test modu; teze uygulama YOK)

- **Kapsam:** yetkinliğin üretim çekirdeği kuruldu; tez metnine dokunulmadı (kalibrasyon).
- **Ne yapıldı:** `constrained_rewrite.py` (mask/splice/verify/rewrite_section) + 15 birim test;
  klinik hekim register'ı (`default_system`); §4.1 kalibrasyon (26/26 span sıfır kayıp) ve
  **§4.3.5 H5** (8 paragraf, RSA/χ²/formül/çıplak-atıf; en zor pasaj) v1→v5 koşuldu.
- **Guardrail turları (H5):** v3 → glossary-dump + note-echo + dikiş tespit; v4 → Guardrail 1+2
  (5 kirlenme sınıfı temizlendi); v5 → Guardrail 3 (p/%95 GA meta-filler beş paragraftan da
  silindi). Her koşuda **8/8 `verify.ok`** (sayı/atıf/çekince/etiket sıfır kayıp).
- **Doktrin:** maskeleme granülerliği (tam-cümle çekince + tam-yüklemli kapsam öbeği → run-on'u
  önler); harness kanıtı garanti eder, üslup-dikişi = Claude Adım-2 payı (1–4 kelime elle onarım).
- **Register düzeltmesi (kullanıcı):** "poliklinikte" ifadesi register'dan çıkarıldı.
- **Kalan Adım-2 payı (H5 v5):** ¶4 run-on · ¶8 "Triangülasyonda Bir" dikişi · ¶3 fazla gloss ·
  ¶7 "eşler" terim kayması — dördü de uygulamada elle onarılır (mekanik kayıp değil).
- **Açık takipler:** ilk gerçek uygulama pasajı seçilince (backlog) tam akış (spec→harness→Adım 2
  →kapı→onay) uçtan uca koşulacak; SKILL/references/command/journal + harness + testler commit'lendi.

---

### 2026-07-30 · 03/D5 — Veri Toplama Süreci + İstatistiksel Analiz (UYGULANDI)

- **Pasaj:** `chapters/03_gerec_ve_yontem.qmd` ¶121, ¶127, ¶131, ¶135 (§Veri Toplama Süreci ve Veri Yönetimi + §İstatistiksel Analiz + alt başlıklar).
- **Değişmeyen (kasıtlı):** ¶119 (işe alım; "Poliklinik başvurusu" = provenans, yasaklı register değil), ¶123 (R paket listesi; zaten parantezli işlev açıklamalı).
- **Yöntem:** Claude-authored (üretici çağrılmadı). `verify_authored_spans` → 24 span PASS.
- **4-mercek adversaryal (paralel subagent):** sadakat-RBŞ TEMİZ · eklenen-iddia TEMİZ · Marmara-register TEMİZ · DOKUNULMAZ-tamlık TEMİZ. Karar: revizyonsuz kabul.
- **Niteliği:** yalnız uzun iç-içe cümlelerin noktalı-virgülden bölünmesi ("hafif dokunuş"); jargon-çevirisi eklenmedi (terimler zaten parantezli klinik-karşılıkla tanımlı).
- **DOKUNULMAZ (grep-teyit, _new):** α=0,05 · FDR/Holm/test-ailesi ayrımı · *test ailesidir* · %95 güven/güvenilir aralığı · BCa · 1000 yineleme ×3 · SMD · SHA-256 · %50 eşiği · s-EMBU-C q25 · FIML/*multiple imputation*/MAR/MNAR/delta · m=50 · otuz iterasyon · 6 atıf token'ı → hepsi korundu. 1. şahıs sızıntısı 0.
- **Hedef dosya:** `.claude/worktrees/niteliksel-kol-rebuild/chapters/03_gerec_ve_yontem_new.qmd` (ana dosya git-temiz, dokunulmadı).
- **Bağlam etkisi:** yeni terim yok; özet/summary sayıları değişmedi → İngilizce özet senkronu gerektirmez.
- **Sıradaki:** D6 (Nedensel çıkarım çerçevesi + Hipotez temelli modeller + Duyarlılık + Bayesçi hat + keşifsel katmanlar).

---

### 2026-07-30 · 03/D6-A — Nedensel çıkarım çerçevesi + H1–H5 modelleri (UYGULANDI)

- **Pasaj:** `chapters/03` ¶139 (nedensel çerçeve) + ¶155 H1 + ¶157 H2 + ¶159 H3 (¶161 H4/¶163 H5 = zaten okunur → değişmedi; ¶143 + @tbl-analiz-plani dokunulmadı).
- **Yöntem:** Claude-authored. `verify_authored_spans` 6/6 PASS (61 span; ¶139 geliştirilmiş 20 span).
- **4-mercek adversaryal:** 4/4 TEMİZ (55/55 token birebir). Mercek-3 soft advisory: ¶139 anne-yaşı gerekçe cümlesi uzun kalmış → ek bölme uygulandı (governing fiil "varsayılmıştır" ×2, yeni iddia yok).
- **Niteliği:** dev tek-zincir cümle bölme (¶139 ~450 kelime → ~13 cümle). Jargon zaten parantezli; çeviri eklenmedi.
- **DOKUNULMAZ (grep-teyit):** 8 atıf token'ı · DAG/backdoor/selection-node/point-identified/propensity/doubly-robust/genişletilmiş/algıladığı italikleri · @fig-causal-dag · @tbl-apa-sample-characteristics · §sec-cok-evren · SMD≈0,21 · IPTW 99.persentil · θ/graded-response · keşifsel-post-hoc estimand · Welch/Hedges g · APIM · HC3 · çekinceler (nokta-tanımlanamaz/koşullu-ilişki/nedensellik-iddiası-yok/anne-yaşı H1-dışla↔H3H4-ayarla) → hepsi korundu. 1. şahıs 0.
- **Hedef:** `03_gerec_ve_yontem_new.qmd`; ana dosya git-temiz.
- **Sıradaki:** D6-B (¶167 duyarlılık/sağlamlık + ¶171 Bayesçi paralel hat + ¶175–179 keşifsel katmanlar) — en yüksek sayı/prior yoğunluğu.

---

### 2026-07-30 · Register Standardı v2 + ¶139-rev (UYGULANDI) — kullanıcı geri bildirimi

- **Tetik:** kullanıcı ¶139 üzerine "çok uzun cümleler, çok fazla parantez tanımı, çizge gibi anlamsız kelimeler" + "bu ilkeleri D1–D5'e de uygula".
- **Standart v2** (`klinisyen-uyarlama-register-standardi.md`): (1) opak coinage sadeleştir — çizge→nedensel diyagram, kestirimci→kestirim yöntemi, yordam→işlem/yöntem (kovaryat KALIR); (2) ağır italik-glossa→Quarto dipnotu (`^[...]`, yalnız kaynağın MEVCUT tanımını birebir taşır — RBŞ; kaynakta tanım yoksa dipnot açılmaz); (3) uzun cümle (~45k) böl. Kullanıcı iki kararı onayladı (AskUserQuestion): term "nedensel diyagram (DAG)", glossa→dipnot; coinage kapsamı çizge+kestirimci+yordam.
- **¶139-rev:** çizge→nedensel diyagram (gövde çizge=0), 3 glossa dipnota (backdoor set/point-identified/propensity score — birebir), selection node/doubly robust gövdede (kaynakta tanımsız/inline). `verify_authored_spans` PASS (20 span). 4-mercek 4/4 TEMİZ (25/25 DOKUNULMAZ; 2 mercek "ortak nedenleri kapatmak" gövde-gevşemesi advisory → gövde girişi mekanizmayı bırakıp dipnota devredecek şekilde sıkılaştırıldı). Uygulandı; ana dosya git-temiz.
- **Sıradaki:** D-REV dalgası — standart v2'yi D1–D6-A'ya propagasyon (hedefler: ¶135 multiple-imputation/FIML glossa→dipnot; uzun cümleler demografik/Beck/psikometrik-intro/¶123 R-liste/¶135/¶143; coinage kestirimci×2+yordam×1+çizge×2@¶123). Sonra D6-B + D7 + D8 standart v2 ile.

### 2026-07-30 · D-REV (UYGULANDI) — standart v2 propagasyonu D1–D6-A

- 7 birim: DREV-1 ¶73 demografik (böl), DREV-2 ¶114 + DREV-7 ¶176 (kestirimci→kestirim yöntemi), DREV-3 ¶130 (yordam→işlem), DREV-4 ¶123 (R-paket run-on→13-madde liste + çizge→nedensel diyagram ×2), DREV-5 ¶150 (FIML/MI/PMM→3 dipnot + böl), DREV-6 ¶158 (hipotez intro böl).
- verify_authored_spans 7/7 PASS; 4-mercek 4/4 TEMİZ (kalan uzun cümle 0, opak coinage 0, 23/23 paket, dipnot birebir, sıfır overclaim).
- Grep-teyit: çizge/kestirimci/yordam = 0 (D1–D6-A); 6 dipnot (¶139:3+¶150:3); @tbl-analiz-plani kuyrukta korundu; ana dosya git-temiz.
- Sıradaki: D6-B (¶167/¶171/¶175–179) doğrudan v2 ile (¶182 yordam + çizge@¶177 dahil).

### 2026-07-30 · D6-B (UYGULANDI) — standart v2; Bölüm 03 nicel kolu D1–D6 TAMAM

- 5 birim: D6B-1 ¶167 (yordam→işlem · multiverse 5-set + H1 3-set madde-liste · TOST böl), D6B-2 ¶171 Bayesçi (dev-¶→5 paragraf · divergent transition dipnot · MERKEZİNE→merkezine), D6B-3 ¶175 (aracılık satır-içi verbatim · böl), D6B-4 ¶177 (çizge→nedensel diyagram · böl), D6B-5 ¶179 (iki yüzey madde-liste, "şunları").
- verify_authored_spans 5/5 PASS; 4-mercek 4/4 TEMİZ (¶200 30+ nicel öğe tek tek: −0,15/−0,22 eksi işaretleri + tüm önseller korundu). 4-mercek sonrası 3 fidelity-artırıcı sıkılaştırma (D6B-3 gösterir kalktı, D6B-5 şu-ilişkileri→şunları+liste, D6B-1 3-set liste).
- Grep-teyit: çizge/kestirimci=0; TOST yordamı→işlem; "yordama modeli"(prediction) korundu; 7 dipnot; ana dosya git-temiz.
- Sıradaki: D7 (Nitel kol ¶181+) + D8 (Raporlama/Etik/YZ) standart v2 ile.

### 2026-07-30 · İŞ AKIŞI DEĞİŞİKLİĞİ + Ch03 _new→kaynak promosyonu (kullanıcı talimatı)

- **Promosyon:** `03_gerec_ve_yontem_new.qmd` içeriği `03_gerec_ve_yontem.qmd`'ye kopyalandı (D7+ birebir aynı doğrulandı; 43 hunk yalnız D1–D6), `_new` silindi. Bundan sonra D7/D8 doğrudan esas dosyada.
- **Onay akışı kaldırıldı:** artık onay-taslağı/onay-kapısı yok; değişiklikler doğrudan uygulanır. DOKUNULMAZ güvenceleri (verify_authored_spans + 4-mercek + register v2) korunur.

### 2026-07-30 · D7 Nitel Kol (UYGULANDI — doğrudan kaynak dosyada, onay kapısı yok)

- 7 hedefli cümle-bölme (S1-S7) + 1 dipnot (*qualitative descriptive* def). Coinage yok. S7 risk-önlemleri madde-listesi ("şunlarla" — mercek-2 "önlem" toplayıcı-etiketini işaretledi → nötr zamire sıkılaştırıldı).
- verify_authored_spans 7/7 PASS; 4-mercek: sadakat 7/7, DOKUNULMAZ 7/7, register 7/7, eklenen-iddia 6/7→S7 düzeltildi. S6 iki "beyan etmiştir" (reflexive çerçeve), S5 çift-yön korundu; OM/BA/EO baş harfleri, tarih/sayı/atıf birebir.
- Doğrudan `chapters/03_gerec_ve_yontem.qmd`'ye işlendi (artık _new yok). 8 dipnot toplam.
- Sıradaki: D8 (Raporlama/Açık bilim/Etik/YZ) — Bölüm 03'ün son dalgası.

### 2026-07-30 · D8 Raporlama/Açık bilim/Etik/YZ (UYGULANDI) — BÖLÜM 03 TAMAM (D1–D8)

- 4 hedefli birim: R1 COREQ tam-ad→dipnot, R2 trustworthiness 111-kelime→intro+4-ölçüt(3 madde; dep+conf ortak-yöntem katlaması) madde-liste, R3 HARKing→dipnot, R4 YZ (i)-(vi)→madde-liste.
- verify_authored_spans 4/4 PASS; 4-mercek 4/4 TEMİZ (R2 ortak-yöntem eşleşmesi "bu iki ölçüt" ile doğru; üstünlük atfı yok; "şunlardır" nötr). COREQ 32/30/2/0, tarih/protokol kodları, 7–17 yaş, @tbl-ai-kullanim birebir.
- Doğrudan kaynağa işlendi. Toplam 10 dipnot; opak coinage 0; 1. şahıs 0.
- **Bölüm 03 (Gereç ve Yöntem) klinisyen-diline-uyarlama TAM: D1(giriş/tasarım)…D8(raporlama/etik/YZ).** Sıradaki: 03 kapanış denetim kapısı → Ch04 → Ch05.

### 2026-07-30 · KONSOLİDASYON — worktree kaldırıldı, tek ana ağaç

- niteliksel-kol-rebuild (12 commit ileri; gelişmiş ch02/04/05 + ch03 reformülasyonum 21fb151) → feat/qc- ana ağacına temiz merge (953ca89, ort, çakışma yok, +782 satır). Oturum dokümanları dfa1711'de.
- sub-worktree `git worktree remove` ile kaldırıldı; niteliksel-kol-rebuild DALI yedek. Ana ağaç render ortamına sahip.
- Bundan sonra: ch04/ch05 doğrudan chapters/*'ta, YALNIZ klinisyen-diline register düzeltmesi (analiz değişimi yok).

### 2026-07-30 · Tam tez PDF render (güncel içerik)

- İlk render freeze/include gotcha'ya takıldı: `freeze:auto` thesis.qmd hash'ine baktığından (değişmedi) eski ch03'ü (çizge'li) üretti. Düzeltme: `_freeze/thesis` + eski `thesis.tex` silindi → yeniden render.
- 1. render: 61 chunk yeniden yürütüldü (R env ana ağaçta), 3 format üretildi. PDF doğrulandı: nedensel diyagram=3, çizge=0, kestirim yöntemi=4, D7/D8 madde-listeleri + DOKUNULMAZ (SMD≈0,21, otuz iterasyon, backdoor-set dipnotu) PDF'te mevcut.
- Çıktı: outputs/quarto/thesis.{pdf(3,86MB),docx,html} — hepsi 2026-07-30 09:46-47. LaTeX hatası yok.
- GOTCHA notu: bundan sonra bölüm-metni değişince tam-tez render öncesi `_freeze/thesis` temizlenmeli.

### 2026-07-30 · ch04 dalga: §Örneklem/Ölçek + H1/H4/H5 (UYGULANDI) — Bulgular-stratejisi (hibrit de-dup)

- §Örneklem: topladığımızda→toplandığında (1.şahıs), "nedensel yönlü asiklik graf"→"nedensel diyagram" (ch03 hizası, ×3 gövde+altyazı).
- H4: WLSMV kestirimci→kestirim yöntemi (×2), 54-kelime veri-kısıtı cümlesi 4 cümleye bölündü (237/121/116/241/4 + listwise korundu).
- H5: RSA yüzey formülü (Z=b0+…) ve a4=b3−b4+b5 → dipnota (register: formül→dipnot); cümleler bölündü; −13,96/−15,93/−7,07 + p'ler + çekince korundu.
- H1: grup-içi rol kontrastı (keşifsel/post-hoc) 16-hücreli grid NESİRDEN ÇIKARILDI → @tbl-apa-h1-within-group'a devredildi (hibrit de-dup); headline (2 bold önerme + "tümü q>0,76" ×2 + tablo-işaret) + birincil headline (reddetme b=0,14 [0,07;0,22] q=0,001 BF₁₀=10,55 vb.) NESİRDE. De-dup kayıpsızlığı R/29_apa_tables.R:554 (t06d tanımı) + 4-mercekle doğrulandı.
- 4-mercek: sadakat 5/5, eklenen 5/5, DOKUNULMAZ+de-dup 5/5, register 4/5→W4 dipnot yalnız-formüle indirildi. verify_authored_spans 5/5.
- Sıradaki: keşifsel katmanlar (grid→tablo de-dup) + tablo/şekil açıklamaları (kaynak: `raporlar/DETAYLI-IZAHAT-BIRLESIK.md`).

### 2026-07-30 · ch04 keşifsel dalga-1 (UYGULANDI) — hibrit de-dup + formül→dipnot

- W6: 2023 dönem-duyarlılığı 89-kelime cümlesi bölündü + 4-alt-ölçek b-gridi @tbl-apa-h1-period2023'e de-dup (headline "hiçbirinde kanıt yok (tümü q≥0,61)" + birincil karşılaştırma b=0,14/0,19 "sönümlenmektedir" + tablo-işaret KALDI). Kayıpsızlık: R/29 t06c tanımı + 4-mercek.
- W7: DCA cümlesi 3'e bölündü (AUC=0,70/net fayda 0,23/sNB=0,86/prevalans=0,27 + kesitsel + ortak-yöntem çekincesi korundu).
- W8: NB=TP/n−(FP/n)·c·[p_t/(1−p_t)] formülü dipnota (c=1→Vickers-Elkin mantığı+atıf gövdede). Render-notu: iç-içe [ ] dipnotu ch04 kapanış render'ında göz-teyidi.
- 4-mercek: sadakat/eklenen/DOKUNULMAZ+de-dup/register 4/4 TEMİZ. verify_authored_spans 3/3.
- KALAN keşifsel: artık-ilişki (L1188+) + gelişimsel-diadik (L1236+) yüzeyleri + meta-forest uzun cümlesi (L1114-1115) + within-case gloss (L1410, nitel intro). Sonra nitel Tema1-4 + joint-display + sentez → ch04 kapanış kapısı.

### 2026-07-30 · ch04 K2 + KAPANIŞ (TAMAM) — Bölüm 04 klinisyen-uyarlaması bitti

- K2: within-case/cross-case eşli glossaları tek dipnota (verbatim). Artık-ilişki (phase5) + gelişimsel-diadik (phase6) RENDER TABLOSU YOK → de-dup EDİLMEDİ (kayıpsızlık; bold-alt-başlıklı, uzun-cümle taşımıyor). Nitel Tema1-4/joint/sentez register-hedefsiz temiz (coinage 0, ağır gloss 0, ≥45-cümle 0; katılımcı alıntıları DOKUNULMAZ).
- KAPANIŞ KAPISI: K5-NUM-03 ch04 sayısal iz PASS (yüksek-risk eşsiz=0 → DE-DUP KAYIPSIZ, otomatik kanıt); K5-CAU PASS; K3-NUM ondalık-virgül PASS; K3-TBL tablo çapraz-ref PASS; K4 Türkçe 4/4 PASS; K1-BIB HARD=0 PASS.
  - K1-CLM-01 FAIL: MİRAS bib SOFT (references.bib alan/DOI/dup=3) — register değişimiyle İLGİSİZ (ch04 öncesi de vardı, atıf dokunulmadı); ayrı bib-hijyen işi.
- RENDER teyit (freeze/thesis temizlendi): kestirimci 0, çizge 0, within/cross-case dipnot render, W8 iç-içe-[] NB dipnotu KIRILMADI, de-dup gridleri tablolarda görünüyor (H1 within-group 8×, 2023 12×), birincil headline nesirde (BF₁₀=10,55 12×). PDF 3,86MB.
- **Bölüm 04 klinisyen-uyarlaması TAM.** Sıradaki: ch05 Tartışma.

### 2026-07-30 · ch04 v3 YENİDEN — H1 emsal (TAMAM)

- Kullanıcı hibrit'i de karmaşık buldu → v3 "iki-blok" (Klinik bulgu sayısız anlatı + demarke *Kanıt* satırı). Belge+bellek: bulgular-stratejisi §v3.
- H1 emsal (chapters/04_bulgular.qmd §H1): Özetle→**Klinik bulgu** (sayısız; yorum absorbe); 4 sayı-yüklü paragraf→tek ***Kanıt*** satırı (grup-ana-etki headline b/CI/q + 4 BF + Hedges g + graded θ + ICC + etkileşim-null Kanıt'ta kaldı; rol-hücre kontrastları + Bayesçi posterior means + grup-içi 16-hücre grid → @tbl-apa-h1-primary/bayesian/within-group'a devredildi, kayıpsız). Nesir 6431→2899 kr.
- Mekanik verify_authored_spans: 36/36 nesir-kalan DOKUNULMAZ birebir; tabloya-taşınan 7/7 nesirden çıktı.
- 4-mercek adversaryal (paralel subagent): (1) sadakat-RBŞ 1 SOFT → "tanı…kaydırmakta/ayırmamaktadır" ilişkisel→nedensel-ton (kaynakta vardı ama anlatı merkezinde güçleniyor; H1 estimand ilişkisel) → ilişkiselleştirildi; (2) overclaim TEMİZ ("küçük ama tutarlı" meşru/hafif underclaim); borderline "asıl önemli"→vurgusuz; (3) Marmara register TEMİZ 6/6 + 4 opsiyonel (verbatim-tekrar→nitel, latent θ köprü, son cümle böl, aile/grup→aile ya da grup); (4) DOKUNULMAZ-tamlık PASS de-dup kayıpsız 27/27 headline birebir + hedef @tbl korundu.
- Tüm mercek düzeltmeleri konsolide → final re-verify 36/36 PASS → UYGULANDI. Tablo/figure DOKUNULMAZ.
- **Emsal format kilitlendi.** Sıradaki: H2→H3→H4→H5→keşifsel aynı iki-blok'a. De-dup kısıtı NOT: H3 ham-b tabloda YOK (tbl-cap "ham b metinde") → H3 ham-b Kanıt'ta KALIR (de-dup edilemez).

### 2026-07-30 · ch04 v3 — H2–H5 iki-blok (TAMAM)

- H2 (grid yok): Özetle→Klinik bulgu + Kanıt; 4-mercek 4/4 TEMİZ; nesir 1760→1622. Tüm sayı (241, d<0,20, p>0,350, r=0,27) Kanıt'ta.
- H3 (de-dup YOK — tbl-cap "ham b metinde"): anlatı sayısızlaştırıldı, TÜM ham-b+ROPE+BF Kanıt'ta; 4-mercek 4/4 TEMİZ (18/18 sayı+4/4 token); "%95 GA" etiketi register-sadeleşti (aralık değerleri korundu). 2406→2334.
- H4 (kısmi de-dup: invariance düzey-detayı→@tbl-apa-h4-invariance): 3 yol-β + global uyum + n Kanıt'ta; 4-mercek 4/4 TEMİZ, nedensel-dil disiplini (eş-değişim, "yordar değil") korundu; advisory invariance-cümlesi noktalı-virgülden bölündü; re-verify 28/28. 4077→2584.
- H5 (de-dup YOK — apa_table_h5_concordance ICC 2-ondalık, nesir 3-ondalık → tabloda birebir yok): minimal v3 — Özetle→Klinik bulgu (sayısız) + giriş paragrafına *Kanıt* öncülü; 5 strateji gövdesi + TÜM sayı byte-değişmez; "beklenenin tersine" eklenen-yorum kaldırıldı (RBŞ). 5 strateji bold başlığı korundu.
- Within-group ekleme talebi (araya girdi): CSR .qmd/.md + ch03/ch05/karma tutarlı teyit edildi; ch04'te v3 de-dup'la @tbl-apa-h1-within-group'a devredilmişti (çakışma yok). BF drift (8,12→10,55) .md'de düzeltilmiş, kalıntı=0.
- **ch04 birincil H1–H5 v3 TAM (5+5 blok).** Sıradaki: keşifsel katman kapsam kararı.

### 2026-07-30 · ch04 v3 keşifsel batch-1 (TAMAM)

- Kullanıcı keşifsel için de TAM iki-blok seçti. Keşifsel alt-bölümlerde "Özetle" YOK + değerlerin çoğu inline-R + grid tablo-teyidi yok → model: sayısız **Klinik bulgu** manşeti (yeni üretim) + mevcut çerçeve/ilk-paragrafa ***Kanıt* —** öncülü; gövde+sayı+inline-R BYTE-DEĞİŞMEZ (de-dup yok).
- Batch-1 (5): Aracılık, LPA, Ağ, Klinik Fayda, DM alt-analiz. Manşet-sadakat merceği (manşetler yeni üretim → overclaim/nedensellik odaklı): Aracılık/LPA/Ağ 3/3 TEMİZ (LPA 2 rötuş: sınıf/profil + "profil örüntüleri"); Klinik Fayda TEMİZ ("küçük katkı" kaynak-destekli underclaim); DM DÜZELT → "hastalık süresi anlamlı ilişki yok" kaynağı ("doğrusal model yeterli"=model-biçimi) aşıyordu → "doğrusal-olmayan örüntü saptanmamıştır"e hizalandı.
- UYGULANDI 5/5 (ch04 10 Klinik bulgu + 10 Kanıt); sayı gövdesi spot-teyit değişmez.
- Batch-2/3 manşetleri (İleri Psikometrik + Artık İlişki + Gelişimsel-Diadik) yazıldı, mercek sürüyor.

### 2026-07-30 · ch04 v3 keşifsel batch-2/3 + nitel/sentez kapsam kararı

- Batch-3 manşet-sadakat: Artık İlişki TEMİZ (b-yolu zayıf→aktarım kanıtı yok + aşırı koruma genç/düşük-SES; korelasyonel korundu). Gelişimsel-Diadik DÜZELT → "dört boyutta da daha yüksek algılamış" karşılaştırmanın eğilim (p=0,092) + kaynağın "betimsel örüntü" nitelemesini yutuyordu → "üç boyut anlamlı + karşılaştırma eğilim + betimsel örüntü" restore; "kardeş ihmali/genelleşme" çerçevesi kaynakta var, korundu.
- Batch-2 (İleri Psikometrik) manşet merceği sürüyor.
- **Nitel Tema1–4 + Çapraz + Negatif Vaka: v3 KAPSAM DIŞI** (kullanıcı kararı: nitel dokunulmaz). Tarama: coinage/graf=0 (register-temiz); ~87 katılımcı alıntısı DOKUNULMAZ. Kapanışta yalnız ondalık/Türkçe teyidi.
- **Joint-Display (L1984) + Genel Bulgu Sentezi (L2024): v3 KAPSAM DIŞI** — üst-sentez anlatısı (tek hipotez birimi değil; nicel↔nitel köprü + uyum/tamamlayıcılık/ayrışma etiketleri DOKUNULMAZ). coinage=0, ≥45-kelime=2 (sınırda, bloklamaz). Register-temiz.
- Nokta-ondalık taraması: nesirde kirlenme YOK (3 eşleşme R-kod/kod-yorum/binlik-ayraç "10.000").

### 2026-07-30 · ch04 v3 YAPISAL KAPANIŞ (TAMAM) + yeni görev: caption zenginleştirme

- ch04 v3 iki-blok TAM: birincil H1–H5 (5+5) + keşifsel batch-1/2/3 (8 Klinik bulgu + 8 Kanıt) = 13 Klinik bulgu + 13 Kanıt. Nitel/joint-display/sentez kapsam-dışı (register-temiz).
- KAPANIŞ kapıları PASS: K5-NUM-03 "yüksek-risk eşsiz=0" (v3 de-dup KAYIPSIZ — otomatik kanıt); K5-CAU-01, K3-NUM-01, K4-TRG-01, K4-TERM-01 PASS. Render (freeze temizli) BİTTİ: Output created, PDF 3,86MB 11:26, LaTeX hatası yok.
- **YENİ GÖREV (kullanıcı):** ch04 tüm tablo(@tbl-*)+şekil(@fig-*) caption/betimlerini `raporlar/DETAYLI-IZAHAT-BIRLESIK.md`'den yararlanıp sade+anlaşılır dille ZENGİNLEŞTİR. → skill: veri-gosterimi-zenginligi (onay-mandate + galileo SOFT-block). Kapsam: 26 tbl-cap + 27 fig. Bu raporda Tablo 4.1-4.20 + Şekil 4.1-4.18 açıklaması var (tam eşleşme).
- Kural: caption YORUMSUZ (ne-çizildiği + birim/örneklem + okuma-anahtarı; sonuç/yön İDDİASI YOK); DETAYLI'dan yalnız bağlam/okuma-anahtarı, "Bir cümleyle"nin sonuç kısmı DIŞARIDA (kanıt-değeri DOKUNULMAZ).

### 2026-07-30 · ch04 kullanıcı-3-istek + caption zenginleştirme (TAMAM)

- Kullanıcı 3 istek: (1) "Klinik bulgu" başlığı klinik-havası veriyor → nötr "Bulgu özeti." (13 yer, replace_all). (2) Ölçek ve Veri Kalitesi kavram/detay zenginleştirme (iç tutarlılık, Cronbach α/McDonald ω farkı, taban etkisi, ölçüm değişmezliği, ölçüt geçerliği, madde-yanıt) — galileo faithfulness 0,98/ground 0,97; DOKUNULMAZ α=0,45 korundu. (3) Kanıt blokları çok karışık (12-29 parantez) → akıcılaştır (parantez→dipnot/cümle, uzun-cümle böl).
- Kanıt akıcılaştırma: H1 emsal (2-mercek DOKUNULMAZ 33/33 + akıcılık PASS; parantez 12→7, 4 dipnot; null→fark-yokluğu, floor/GRM→dipnot). H2 (10/10, parantez 6→5), H3 (28/28, 14→12, 2 dipnot), H4 (26/26, 12→8, invariance de-dup korundu). Tüm nesir "null" (3) → fark-yokluğu/anlamsız (İngilizce sızıntı temizliği).
- **Caption zenginleştirme (veri-gosterimi-zenginligi skill):** 53 caption (26 tbl + 27 fig). Workflow 5 grup fan-out (DETAYLI-IZAHAT context-ekonomisi); emsal 3 galileo PASS + kullanıcı onayı. Bağımsız doğrulama: 53/53 id eşleşti, [KEŞİFSEL]/[POST-HOC] korundu, yeni-sayı=0, ondalık virgül, sonuç-iddiası=0 (2 "güçlü" flag = BF Jeffreys ölçeği + triangülasyon ölçütü, okuma-anahtarı). Kalıp: ne-çizildiği + birim/örneklem + "Okuma anahtarı"; sonuç/yön DIŞARIDA. İlk uygulama re.S/DOTALL BOZDU (backup restore); satır-bazlı script 53/53 temiz uyguladı.
- KAPANIŞ: K5-NUM-03 eşsiz=0 (akıcılaştırma+caption sonrası de-dup/sayı bütünlüğü KORUNDU); K5-CAU-01, K3-NUM-01, K3-TBL-01, K4-TRG-01, K4-TERM-01 PASS. Render sırada.

### 2026-07-30 · ch04 render teyit (TAMAM) — H1-H4 Kanıt + başlık + Ölçek + 53 caption

- Freeze-temizli tam render BİTTİ (PDF 3,91 MB, LaTeX hatası yok). pdftotext teyit: Bulgu özeti 13/Klinik bulgu 0; Kanıt satırı 13; caption "Okuma anahtarı:" 100× (tırnak bozulması yok); McDonald ω + taban etkisi render; null 0/çizge 0/kestirimci 0; DOKUNULMAZ BF₁₀=10,55(11)/α=0,45(7)/b=0,14(37); ham dipnot ^[ = 0 (akıcılaştırma dipnotları düzgün).
- **KALAN (kullanıcı "benzer nitelikteki diğer kısımlar" kapsamı):** H5 Kanıt (5-strateji gövdesi) + keşifsel Kanıt gövdeleri (Aracılık/LPA/Ağ/Klinik Fayda/DM/İleri Psik/Artık/Gelişimsel) akıcılaştırılmadı — H1-H4 birincil Kanıt + başlık + Ölçek + caption yapıldı.

### 2026-07-30 · Tablo sayfa-kesinti tespit + FIX (kullanıcı: Tablo 4.1 kesilmiş)

- TEŞHİS: apa_render_table gt kullanıyor; gt varsayılan LaTeX çıktısı tabloları `\begin{table}` FLOAT ortamına koyuyordu (26 float, 0 longtable). Float tablolar sayfa-KIRILAMAZ → uzun tablolar (Tablo 4.1 örneklem ~116 satır; ayrıca h5-concordance ~42, dm-clinical ~30, h3-sensitivity ~26) tek sayfaya sığmayınca kesiliyordu. Şekiller sorunsuz (tüm includegraphics ≤0,96\linewidth; Overfull=0).
- FIX (sunum katmanı, kanıt-değeri değişmez): apa_render_table gt::tab_options'a `latex.use_longtable = TRUE` eklendi → tüm gt tabloları longtable'a döndü.
- RENDER TEYİT (freeze-temizli): thesis.tex float=0/tabular=0/longtable=49 (öncesi float=26); endhead=23 (başlık-tekrar aktif); Tablo 4.1 PDF'te 4 sayfaya bölündü, başlık her sayfada tekrar, son data satırı ("Şiddetli...") tam → KESİNTİ YOK. PDF 3,92 MB.
- Kalan: H5+8 keşifsel Kanıt akıcılaştırma (Workflow üretiyor) → verify+uygula+final render.

### 2026-07-30 · H5 + 8 keşifsel Kanıt akıcılaştırma (TAMAM)

- Workflow 9/9 blok (H5 + Aracılık/LPA/Ağ/Klinik Fayda/DM/İleri Psik/Artık/Gelişimsel); uzun cümle böl + açıklama parantezi→dipnot/cümle. Mekanik verify 9/9 PASS: inline-R karakter-karakter aynı (Aracılık 12 inline-R dâhil — render-kırma riski geçti), sayı seti korundu, @tbl/@fig/[@key] token + [KEŞİFSEL] etiketi + R-chunk birebir.
- TESPİT+ÇÖZÜM: IleriPsik subagent'i 7 galileo-onaylı figür caption'ımı da akıcılaştırmıştı (içerik/sayı korundu ama onaylı çıktı). "En güncel-en doğru baz" → figür caption'da en-doğru=galileo-onaylı hâlim, Kanıt gövdesinde en-doğru=subagent akıcılaştırma. Uygulamada tüm bloklarda figür caption'lar onaylı-hâle sabitlendi (7 geri-sabit), Kanıt gövdesi akıcı alındı.
- Uygulama-sonrası: inline-R set-eşit (25=25), düşen sayı=0, nesir null=0 (17 'null' hepsi R-kod is.null), K5-NUM-03 eşsiz=0. Yapı: 13 Bulgu özeti + 13 Kanıt + 53 caption + 5 strateji + 27 R-chunk. **ch04 TAM.**

### 2026-07-30 · ch05 TARTIŞMA ve SONUÇ — tam bölüm uyarlaması (UYGULANDI) — **Bölüm 05 TAMAM**
- **Pasaj:** `chapters/05_tartisma_ve_sonuc.qmd` tamamı (66 paragraf → 115 paragraf). Doğrudan
  kaynak dosyada (onay kapısı kaldırılmış iş akışı).
- **Yöntem:** Claude-authored (üretici model çağrılmadı). Mekanik bekçi: **yeni**
  `scripts/eval/ch05_span_guard.py` — HEAD ile çalışma ağacı arasında sayı/atıf/`@tbl|fig|sec`/`§`
  span çokluğunu (multiset) karşılaştırır; satır-sarması normalize edilir. **522/522 span PASS,
  düşme 0, ekleme 0** (her dalgadan sonra koşuldu).
- **6 dalga:** T1 giriş+H1 · T2 bilgi-verici literatürü+H3 · T3 **H4 mega-paragraf** (678 kelime
  tek satır → 10 paragraf; kelime sayısı 678→678) · T4 H2+H5+nitel temalar · T5 karma
  bütünleştirme + keşifsel katmanlar · T6 ölçüm+sınırlılık+sonuç/öneriler.
- **Niteliği (register standardı v2):** (1) uzun cümle bölme — **≥45 kelime cümle 23 → 0**
  (kalan 5 tespit liste-birleştirme artefaktı); (2) dev paragraf bölme — **≥230 kelime paragraf
  5 → 0**; (3) enümerasyon → madde listesi (5 dönüşüm: SRM üç kaynak `(a)(b)(c)`, karma yöntem
  üç ilişki türü, robustluk üç yaklaşım, artık-ilişki İlk/İkinci/Üçüncü, DM klinik üç eksen);
  (4) `Araştırma önerileri` dört kalın başlık → dört ayrı paragraf; (5) joint-display bloğu H1–H5
  için beş ayrı paragraf (`<!-- kaynak: … -->` provenans yorumları korundu); (6) iki mega tek-satır
  paragraf (1063 ve 2432 karakter) yeniden sarıldı.
- **Terim/yazım:** `informant` → **bilgi-verici** (tez-geneli tek karşılık, F4); yazım hatası
  **Keşfisel → Keşifsel**. Opak coinage (çizge/kestirimci) ch05'te zaten 0; `yordama modeli`
  (prediction) korundu.
- **4-mercek adversaryal (paralel subagent, diff üzerinden):** Mercek-1 sadakat **TEMİZ**
  (25+ hunk, 5 liste dönüşümü tek tek karşılaştırıldı); Mercek-2 eklenen-iddia **TEMİZ**
  (tek işaret `[@esposito2025discrepancy]` → HEAD'de zaten var, grep ile kapatıldı);
  Mercek-3 register/Türkçe **TEMİZ** (1. şahıs 0, "poliklinikte" 0, ondalık virgül tam,
  markdown liste/atıf/HTML-yorum yapısı geçerli); Mercek-4 DOKUNULMAZ = mekanik bekçi.
- **Kapı sonuçları (HARD hepsi PASS):** `tr_corpus_audit all --fail-on blocker` → **HARD=0**
  (ch05'te yalnız 1 advisory: H-TRANS) · `bib_hygiene all` → tanımsız atıf **0** ·
  `csr_numeric_trace_audit` → untraced 0, high-risk unmatched **0** · `csr_causal_label_audit`
  → causal_revise **0**, label_errors **0** · `claim_certification` → kaynaksız sayı **0** ·
  `tez_checklist_verify --fast` → **FAIL=0** (28 PASS / 6 SKIP / 5 MANUEL; K5-CAU-02 ch05 PASS).
- **SOFT-block galileo (bağımsız GPT-5.4 judge, H4 bloğu; evidence = orijinal pasaj):**
  faithfulness **0,99** · groundedness **0,99** · citation_support **supported** ·
  marmara_compliance **0,95** · hallucination_risk **0,03**. `galileo_overclaim_judge`
  (liste dönüşümleri): overclaim_risk **0,14**, causal_drift **false**, cherry_pick **false**.
- **Judge bulgusu üzerine tek düzeltme:** "Böylece … mekanizma önerir" → "**Aynı bağ**, … bir
  mekanizma **da** önerir" (nedensel bağlaç → nötr eklemeli yapı; kaynağın `ve` bağlacına daha
  yakın). Ayrıca H4 bloğunda düzensiz satır sarmaları toparlandı.
- **Doğrulama artıkları:** pandoc parse OK; 16 çapraz-referansın tamamı tanımlı; 103 atıf
  anahtarının tamamı `references.bib`'de; madde listelerinden önce boş satır eksiği 0;
  `@tbl-yil-grup` tablo bloğu bozulmadı. Net kelime farkı **+11** (yalnız cümle bölmenin
  gerektirdiği özne/bağlaç yinelemeleri).
- **Tez-geneli bağlam etkisi:** yeni terim yok, sayı değişmedi → özet/summary ve kısaltmalar
  listesi senkronu gerekmiyor. `informant` sözcüğü tez genelinde tarandı; ch05 dışında gövde
  kullanımı kalmadı.
- **Açık takipler:** (i) tam-tez render (önce `_freeze/thesis` temizliği — GOTCHA);
  (ii) ch05 `/bolum-sertifika` tazelemesi (T-CERT-01 MANUEL); (iii) H-TRANS advisory'si
  `anlatim-zenginligi` kapısına devredildi.
