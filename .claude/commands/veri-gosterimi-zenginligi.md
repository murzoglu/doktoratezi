---
description: Bulgular bölümünün VERİ GÖSTERİMİNİ zenginleştirir — R çıktısı ↔ yazılı bulgu mutabakatı, figür/tablo veri-tutarlılığı + estetik/Türkçe/tasarım denetimi, eksik ama yararlı yeni görsel önerisi, başlık/altyazı optimizasyonu, istatistik betimleme netliği (kanıt DEĞERİ dokunulmaz — yalnız sunum katmanı); sci-audit + galileo kapısından geçirip onaya sunar (dosyaya doğrudan yazmaz)
argument-hint: "[chapters/04_bulgular.qmd konumu / @tbl-* / @fig-* / seçili bulgu bloğu]"
---

# /veri-gosterimi-zenginligi — Veri Gösterimi Zenginleştirme Kapısı

Zenginleştirilecek gösterim: **$ARGUMENTS** — argüman boşsa editör seçimini (`ide_selection`)
kullan; seçim de yoksa `chapters/04_bulgular.qmd` bütününde figür/tablo envanterini çıkar.

Bu araç Bulgular bölümünün **veri-gösterim katmanını** zenginleştirir: yazılı bulgular ile
R script çıktılarının **tam mutabakatı**, figür/tablo/diyagram/grafiklerin **veriyle bire bir
tutarlılığı**, bu görsellerin **estetik + Türkçe + tasarım** kalitesi, **eksik ama yararlı**
yeni görsel/tablo önerisi, tüm figür/tablo **başlık ve altyazılarının** netliği ve istatistik
bulguların (yorum katmadan) **maksimum anlaşılırlıkla** betimlenmesi. **Revizyonu chapter/R
dosyasına DOĞRUDAN yazmaz; sci-audit + galileo kapısından geçirip onaya sunar.**

## Kardeş komut sınırı (çiğnenmez)

`/anlatim-zenginligi` ile **aynı bölümde paralel** çalışır; sınır katmandır:

| | `/anlatim-zenginligi` | `/veri-gosterimi-zenginligi` (bu) |
|---|---|---|
| Çalıştığı bölge | **Nesir** (düzyazı anlatım + referans) | **Veri-gösterim** (figür/tablo/R-çıktı + altyazı + betim cümlesi) |
| DOKUNULMAZ | Sayı/istatistik/bulgu **ve** figür/tablo | Kanıt **değeri**: sayının kendisi, yön, anlamlılık, büyüklük |
| Düzenleyebildiği | Terim izahı + okuyucu bağlamı + atıflı literatür | **Sunum katmanı**: etiket, renk, düzen, font, başlık/altyazı, Türkçe, betim netliği, yeni görsel |

**Ortak anayasa:** ikisi de **kanıt değeri mutasyonunu** yasaklar. Bu komut sunumu
zenginleştirir; **hiçbir sayıyı/yönü/anlamlılığı değiştirmez, yuvarlamaz, güçlendirmez**;
kaynakta olmayan özgüllük (informant "anneden", "klinik açıdan anlamlı", "güçlü/dayanıklı",
nedensellik) **eklemez.** Zenginleştirme = **daha okunur/tutarlı/estetik gösterim** + **daha
anlaşılır betim** + **kanıtlanmış boşluğa yeni görsel** — yeni bir *bulgu* değil.

## Kapsam — DOKUNULMAZ kanıt değeri vs. düzenlenebilir sunum katmanı

- **DOKUNULMAZ (kanıt değeri):** kanonik CSV/model artefaktındaki sayılar; bulgunun yönü/
  anlamlılığı/büyüklüğü; hipotez kararı; `@tbl-*`/`@fig-*`/`[@key]` token'ları; bulgu sırası;
  istatistiksel yöntem. Bunlar **kaynaktan** (`outputs/models/*`, `data/processed/*`,
  `outputs/tables/*`) gelir — koda/altyazıya **gömülmez**.
- **DÜZENLENEBİLİR (sunum katmanı):** figür `labs()` başlık/altyazı/eksen etiketi, tema
  (`apa_plot_theme`), renk/skala (`scale_*`), okunabilirlik (font, taşma, facet düzeni);
  tablo Türkçe kolon başlığı + ondalık virgül + `group_col`/`split_prefix`/`hide_cols` sunumu;
  `tbl-cap`/`fig-cap` metni; bulguyu betimleyen düzyazı cümlesinin **açıklığı** (sayı aynen).

## Yürütme (sıra sabittir)

1. **Bağlamı sabitle — DOSYA ADI TAHMİN ETME.** Hedef figür/tablo ID'sini bölümde ara
   (`grep -n "@tbl-<id>\|@fig-<id>\|{#tbl-<id>}\|{#fig-<id>}" chapters/04_bulgular.qmd`) ve
   gerçek konum + üretici zinciri bul: tablo → `apa_render_table("<csv_id>")` (sunum yardımcısı,
   ch04 `apa-table-helpers` chunk'ında) → tablo kurucular `R/29_apa_tables.R` (`apa_table_*`) →
   `outputs/tables/<csv_id>.csv`; figür → `R/28_apa_figures.R` `apa_plot_*` → 
   `scripts/R/39_export_carbon_svg_figures.R` → `docs/assets/figures/carbon/**/<dosya>`. Kanonik
   analiz kilidini (`data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock`) hatırla.
   t1dm-tez-rehberi **Faz 0** kapsam + **Faz 0.5** tedbir kapısı geçmezse dur.

2. **Eksen 1 — R çıktısı ↔ yazılı bulgu mutabakatı (spec #1).** Yazılı Bulgular'daki her
   denetlenebilir sayıyı üretilmiş artefakta bağla; **hata/eksik/sürüklenme (drift)** yakala:
   - `python3 scripts/util/csr_numeric_trace_audit.py --csr chapters/04_bulgular.qmd
     --out-claims outputs/tables/ch04_numeric_trace_claims.csv
     --out-numbers outputs/tables/ch04_numeric_trace_numbers.csv
     --out-report outputs/reports/ch04_numeric_trace_audit.md` → **yüksek-risk eşsiz = 0**
     olmalı (K5-NUM-03 kapısı). Eşsiz/kaynaksız her sayı bir bulgu-mutabakat hatasıdır.
   - `python3 scripts/util/r_generator_literal_audit.py --fail-on-find` → R üretici kodda
     **gömülü istatistik literali = 0** (K5-LIT-01; kaynak-tekilliği). Bulgu varsa değeri
     artefakttan-okur biçime çevir (literal gömme).
   - Metin bir tablo/figür değerini yanlış aktarıyorsa (ör. tablo β = 0,16 iken metin 0,18):
     **metni kaynağa hizala** — sayıyı asla uydurma; hangi tarafın kanonik olduğunu artefakttan
     doğrula. Metinde raporlanan ama hiçbir tabloda/figürde görünmeyen değer için: ya kaynağa
     bağla ya da onaya "eksik gösterim" olarak taşı (bkz. Eksen 2.3).

3. **Eksen 2 — figür/tablo denetimi + iyileştirme + yeni görsel + altyazı (spec #2).**
   - **2.1 Veri-tutarlılığı:** Her figür/tablonun okuduğu artefaktın (`outputs/tables/*.csv`,
     model RDS) `_targets.R`'de `format = "file"` ile izlendiğini doğrula
     (`python3 scripts/util/targets_file_tracking_audit.py`; K5-TRK-01) — stale gösterim önlenir.
     Figür ile aynı büyüklüğü raporlayan tablo/metin **özdeş sırayı ve değeri** göstermeli
     (ör. ağ merkeziyeti metin↔`@tbl-apa-network`↔`@fig-network-graph` aynı kaynaktan).
   - **2.2 Estetik/Türkçe/tasarım denetimi + iyileştirme (yalnız sunum):**
     - *Türkçe:* `labs(title/subtitle/caption)`, eksen etiketi, tablo kolon başlığı, `tbl-cap`/
       `fig-cap` — **ondalık virgül**, terim tutarlılığı (tez genelinde tek karşılık), İngilizce
       sızıntısı yok. Marmara sözleşmesi (`tez-yazim/00_kaynak-kurallari/`) bağlayıcı.
     - *Düzen/okunabilirlik:* uzun snake_case/boşluksuz kod etiketleri `apa_humanize_code`/sözlük
       ile okunur Türkçeye; sayfa-kenarı taşması, facet dengesi, eksen sıralaması, açıklama
       (legend) yeri; çok-katmanlı tabloda `group_col`/`split_prefix`/`hide_cols` ile okunur
       alt-bloklar (bilgi kaybı yoksa; kaybolan kolon `tbl-cap`/dipnotta özetlenir).
     - *Renk/font:* Carbon paleti + IBM Plex Sans tutarlılığı (`apa_plot_theme`,
       `scale_color_manual`/`scale_fill_gradientn`); grup renkleri tez boyunca sabit (ör.
       DM `#0f62fe`, Kontrol gri); renk-körü ayrılabilirliği; kanıt-değeri renk kodlamasını
       değiştirmeden yalnız algısal netlik.
     - **Kanıt-değeri asla değişmez:** yeni renk/etiket bir sayıyı/yönü yeniden anlamlandırmaz.
   - **2.3 Eksik ama yararlı yeni görsel/tablo önerisi (dikkatli):** Bulgu zaten kanonik
     artefaktta **mevcut ama görselleştirilmemiş/tablolaştırılmamışsa** ve okuyucu için değer
     katıyorsa öner. Kural: (a) yeni görsel **yalnız var olan** artefakt değerinden türetilir
     (yeni analiz/yeni sayı YOK); (b) üretici `R/28`/`R/29` desenine uyar ve artefakttan okur
     (literal yok); (c) `_targets.R` file-tracking'e bağlanır; (d) `[KEŞİFSEL]`/`[POST-HOC]`
     bloğundaki bir bulgunun görseli aynı etiketi taşır. Öneriyi **onaya taşı** — onaysız
     üretme.
   - **2.4 Başlık/altyazı optimizasyonu:** Her `tbl-cap`/`fig-cap` ve figür `labs` başlığını
     gözden geçir; **kendi kendine yeten** (stand-alone), ne-gösterildiğini + birim/örneklem +
     okuma anahtarını (renk/panel/kesikli çizgi ne demek) veren, **yorumsuz** bir altyazıya
     getir. Sonuç iddiası ("DM daha yüksek") altyazıya girmez; altyazı *ne çizildiğini* söyler,
     *ne anlama geldiğini* değil.

4. **Eksen 3 — istatistik betimleme netliği (spec #3; yorum YASAK).** Bulguyu betimleyen
   düzyazıyı, sayıyı **aynen koruyarak** daha anlaşılır kıl: metriğin **tanımını** kısaca izah
   et (ör. "SMD, iki grubun standardize edilmiş ortalama farkıdır; sıfıra yakınlık benzerlik
   gösterir"), okuyucuyu teknik dilde boğmadan; ama **etki büyüklüğü etiketi** ("küçük/orta/
   güçlü"), yön güçlendirme, "anlamlı değildi"→"eğilim" yumuşatma, korelasyon→neden **eklenmez**
   (bunlar Bulgular yazım kuralı gereği yorumdur). Nesir kalitesi:
   `tez-yazim/04_kalite-kontrol/insan-turkcesi-retorik-playbook.md`. Not: saf düzyazı-akış işi
   `/anlatim-zenginligi`'ye aittir; bu eksen yalnız **gösterimi tamamlayan betim netliği** ile
   sınırlıdır (bkz. eşgüdüm playbook'u).

5. **Denetle — UYGULAMADAN ÖNCE, üç kademeli kapı (araç-rol tablosu aşağıda).** Aday değişikliği
   (R üretici / `tbl-cap`/`fig-cap` / betim cümlesi) bir önizleme parçasına yaz; **sci-audit
   (HARD)** + Türkçe denetimini koştur; **galileo**'yu doğrudan aday altyazı/betim metni üzerinde
   koştur. Yeni/değişen figür varsa `scripts/R/39_export_carbon_svg_figures.R`'yi (yalnız etkilenen
   figür) çalıştırıp görsel çıktıyı gözle doğrula. Denetimi render/onay sonrasına **ERTELEME**.
   Herhangi HARD bulgu = düzelt-ve-tekrar; onaya çıkma.

6. **Onaya sun.** Sun: (a) diff (eski → yeni: R `labs`/renderer argümanı, `tbl-cap`/`fig-cap`,
   betim cümlesi), (b) etkilenen figür için önizleme görseli (varsa), (c) kapı özeti
   (numeric-trace yüksek-risk sayısı, literal-audit, targets-tracking, HARD/SOFT/advisory +
   galileo skorları), (d) yeni görsel önerileri + gerekçesi. **Açık kullanıcı onayı olmadan
   Edit/commit yok.** Onay sonrası: Edit uygula → değişen figür için tam `tar_make()` +
   `39_export_carbon_svg_figures.R` → kapanışta `/sci-audit:audit chapters/04_bulgular.qmd
   --lang tr` + bölüm kapanıyorsa `/tez-dogrulama`.

## Denetim araç-rol tablosu (araçları KARIŞTIRMA)

| Kademe | Araç | Rol |
|---|---|---|
| **HARD** | `csr_numeric_trace_audit.py` (ch04) | Eksen 1: yazılı bulgu ↔ CSV izi; yüksek-risk eşsiz = 0 (K5-NUM-03) |
| **HARD** | `r_generator_literal_audit.py --fail-on-find` | Eksen 1: R üretici kodda gömülü literal = 0 (K5-LIT-01) |
| **HARD** | `targets_file_tracking_audit.py` | Eksen 2.1: figür/tablo kaynağı `format=file` izli (K5-TRK-01) |
| **HARD** | `/sci-audit:check-turkish … --strictness certification` | Altyazı/etiket Türkçe imla + ondalık-virgül (nokta-`p` = blocker) |
| **HARD** | `/sci-audit:check-stats` | Betim cümlesindeki istatistik ↔ tablo tutarlılığı (Axis C) |
| **SOFT-block** | `galileo_judge` (`text`, `section_type=results`, `evidence`) | Altyazı/betim **metninin** faithfulness / groundedness / overclaim |
| **advisory** | `galileo_coherence` | Figür↔metin↔tablo anlatı zinciri tutarlılığı |
| **advisory** | görsel gözden geçirme (39_export → SVG/PNG) | Estetik/düzen/renk/taşma — insan gözü + betim |

Kademe anlamı (eşikler `.claude/galileo.local.md`): **HARD** değişmez, override yok; **SOFT-block**
`certified-final`'ı durdurur, insan-override'lı (groundedness/faithfulness < 0,60; overclaim);
**advisory** bloklamaz.

## Devir (scope guard)
- Nesir/düzyazı zenginleştirme → `/anlatim-zenginligi` · Yeni referans → `/referans-kapisi`
- Bölüm finalizasyonu → `/bolum-sertifika` · Kapanış doğrulaması → `/tez-dogrulama`
- Eşgüdüm sırası ve devir protokolü:
  `tez-yazim/04_kalite-kontrol/bulgular-zenginlestirme-esgudum-playbook.md`

## Bağlayıcı (çiğnenmez)
- **Kanıt değeri DOKUNULMAZ:** sayı/istatistik ve bulgunun yönü/anlamlılığı/büyüklüğü/sırası
  **aynen** kalır; yeniden-yorum, yuvarlama, güçlendirme yok. Odak: **sunum katmanı** (gösterim
  tutarlılığı + estetik + Türkçe + altyazı + betim netliği) — **çalışmanın bulguları değişmez.**
- **Kırmızı bayraklar (kanıt mutasyonu → çıkar):** altyazıya/etikete sonuç iddiası ("DM daha
  yüksek", "güçlü ilişki") koyma; renk/panel ile bir yönü yeniden-anlamlandırma; betimde etki
  büyüklüğü etiketi ekleme; "anlamlı değildi" → "eğilim" yumuşatma; korelasyonu neden yapma;
  metin sayısını tabloya uydurmak için sayıyı **değiştirme** (yalnız kaynağa **hizala**).
- **Kaynak-tekilliği:** her gösterilen sayı üretilmiş artefakttan gelir; R üretici koda veya
  altyazıya **literal gömülmez** (K5-LIT-01). Değişen model/veri → **tam `tar_make()`** +
  ilgili figür yeniden-export; `tar_outdated()` boş.
- **Yeni görsel = ADAY (uydurma YASAK):** yalnız var olan artefakt değerinden türetilir; yeni
  analiz/yeni sayı üretmez; onaysız üretilmez; file-tracking'e bağlanır.
- **Dosyaya doğrudan yazmadan önce onaya sun; denetimi onaydan sonraya erteleme.**
- **sci-audit (HARD) atlanamaz;** `tez_checklist_verify` onun YERİNE, `galileo` da sci-audit'in
  yerine geçmez — üçü ayrı kademedir.
- **`[@key]`/`@tbl-*`/`@fig-*` token, ondalık virgül, `[KEŞİFSEL]`/`[POST-HOC]` etiketleri ve
  başlık yapısı aynen korunur.**
- **KVKK:** dış gateway'e (galileo/minerva) yalnız literatür terimi + aggregate altyazı metni;
  katılımcı/ham/aile-düzeyi veri asla gönderilmez.
