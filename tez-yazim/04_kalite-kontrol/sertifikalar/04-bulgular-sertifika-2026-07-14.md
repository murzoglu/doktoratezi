# Bölüm Finalizasyon Sertifikası

Durum: `certified-final`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | 04 — BULGULAR |
| Dosya | `chapters/04_bulgular.qmd` (934 satır, ~7.380 sözcük, 8 üst-bölüm §4.1–4.8, 22 APA tablosu, 9 metot-çapa atıfı) |
| Sertifika tarihi | 2026-07-14 |
| Strictness | `certification` |
| Önceki statü | `blocked` (2026-07-14, aynı gün erken tur) — Kapı 2 `zotero-gap` + Kapı 5 `reliability-gap` |
| Uygulama onayı | Kullanıcı (repo sahibi) açık direktifi: yol-haritası dört kalemini de tamamla ("hepsini yap") |

## Kapsam (bu tur)

Kapsam denetimi + anlatım/mantık geliştirme + hedefli sayısal düzeltme (CSR-izli),
ardından `blocked` turdaki iki teknik gate'in kapatılması. Kullanıcı direktifiyle
dört yol-haritası kalemi tamamlandı.

## Kapı Sonuçları (0-5) — tümü PASS

| Kapı | Kapsam | Kanıt | Sonuç |
|---|---|---|---|
| 0 | Kapsam/gizlilik | Kaynak seti `kritik-dosya-manifesti.tsv` ile eşleşiyor (CSR + nitel kanonik); yalnız aggregate + anonim quote-ID; ham veri/credential bağlama alınmadı | ✅ PASS |
| 1 | Derin literatür/iddia haritası | Findings **yorumsuz**; dış-literatür yalnız 9 metot-çapası (substantif literatür Tartışma'da); repo-içi iddialar CSR/SAP/protokol/veri-haritası/nitel-rapora izli | ✅ PASS |
| 2 | Full-text/Zotero/ledger | **9/9 metot-çapası `cite-ok`**. Bu turda 5'i kapatıldı: 4 Zotero import (`austin2009balanceDiagnostics`→DBZ2HWQJ, `cheungRensvold2002invariance`→A7FD343B, `samejima1969graded`→8BFE3VD5, `simonsohn2020specificationCurve`→5A8AS84M) + 1 mevcut (`benjaminiHochberg1995fdr`→FSDNF6QU); hepsi 9ZFDHMZA koleksiyonunda, ledger'da DOI+Zotero key+claim+`cite-ok (identity-doğrulamalı)` satırıyla | ✅ PASS |
| 3 | Metin/kılavuz uyumu | Başlık yapısı temiz (§4.1–4.8, [KEŞİFSEL] etiketleri doğru); ondalık **virgül** istisnasız; **0 yorum sızıntısı**; H1–H5↔keşifsel↔nitel↔karma karışmıyor; bib HARD=0; 22 APA tablosu + şekiller çift-sunum kuralına uygun | ✅ PASS |
| 4 | Türkçe imla/akış (sci-audit axis G) | `tr_sciaudit.py --strictness certification --fail-on error` → **exit 0**; 0 blocker / 34 warning (gerekçeli kabul; §4.1 paragraph-long çözüldü) | ✅ PASS |
| 5 | AI-reliability + render | Manuskript + repo-invaryant katmanları temiz; tam-tez render exit 0 (aşağıda) | ✅ PASS |

### Kapı 2 detay — bu turda kapatılan 5 metot-çapası

Tümü `references.bib`'de tanımlı klasik istatistik-metodoloji kaynağı; Zotero
9ZFDHMZA import-doi + DOI/Crossref kimlik eşleşmesi + claim notu + iki-kol audit ile
`cite-ok (identity-doğrulamalı)` (klasik-metot precedent: `cicchetti1994`, `hox2017multilevel`).

| Anahtar | DOI | Zotero | Kullanım |
|---|---|---|---|
| austin2009balanceDiagnostics | 10.1002/sim.3697 | DBZ2HWQJ | §4.1 SMD denge eşikleri |
| cheungRensvold2002invariance | 10.1207/S15328007SEM0902_5 | A7FD343B | §4.2/§4.3.4 ΔCFI değişmezlik |
| samejima1969graded | 10.1007/BF03372160 | 8BFE3VD5 | §4.3.1 graded response IRT |
| benjaminiHochberg1995fdr | 10.1111/j.2517-6161.1995.tb02031.x | FSDNF6QU | §4 preamble + H1–H4 FDR |
| simonsohn2020specificationCurve | 10.1038/s41562-020-0912-z | 5A8AS84M | §4.5/§4.4.6 çoklu-evren |

### Kapı 5 delili (birinci-el, bu oturum)

| Kontrol | Sonuç |
|---|---|
| `bib_hygiene.py all` | HARD=0 ("yok"); exit 2 = yalnız SOFT (zahidi2019 pages, sumer2010 DOI — pre-existing, BULGULAR dışı; playbook: SOFT bloklamaz) |
| `karma_ledger_check.py` (BULGULAR ZORUNLU drift-guard) | **TEMİZ — 0 bulgu (exit 0)** |
| `doktoratezi-ai-audit` (repo/veri invaryantı) | **144/144 passed** (önceki 134/142 → 3-tier plugin regresyonu tamamlandı) |
| `t1dm-qual-ai-audit` (nitel kol) | **55/55 passed** |
| `tests/test_claude_hooks.py` (owner hook testi) | **14/14 OK** |
| `git diff --check` (scoped: chapter+bib+ledger+sapma+plugin test) | **CLEAN** |
| `quarto check` | OK (Quarto 1.9.38; Pandoc/Sass/Deno/Typst/LaTeX 2026 ✓) |
| **Tam-tez `quarto render thesis.qmd`** | **exit 0 — `outputs/quarto/thesis.html` üretildi; 0 çözümsüz atıf/hata** |
| **`targets::tar_make()`** | **exit 0 — 310 completed / 235 skipped [9m 10.4s]; sonra `tar_outdated()`=0 (pipeline tam güncel); H1–H5 çekirdek değerleri taze tablolarla doğrulandı** |

### Kapı 5 — pre_tool_use 3-tier plugin regresyonu (bu turda tamamlandı)

`blocked` turdaki 8 FAIL, owner-onaylı **üç-katmanlı veri-yönetişimi revizyonunun
(2026-07-13)** doktoratezi-ai-audit plugin'ine yansıtılmamasındandı. Bu turda
"iki ağaç + tests + plugin regresyonu birlikte güncellenir" kuralı tamamlandı:
- Plugin asset kopyası (`.codex/hooks/pre_tool_use_policy.py`) repo hook'una senkronlandı (materialized-drift + installer-check FAIL'leri kapandı).
- Plugin runtime-deny test beklentileri yeni politikaya güncellendi: Tier-2 de-identified analiz yüzeyi (`data/processed`+`outputs`+`_targets`) display/interpreter'a **AÇIK** (3 test denied→allowed); event-shape parsing kapsamı PII-kaynak yollarıyla korundu; **Tier-3 exfiltrasyon testi eklendi** (processed okunabilir ama kopya/arşiv/encode ile dışarı taşınamaz — güvenlik invaryantı güçlendirildi).
- **Güvenlik-kritik invaryantlar korundu**: PII kaynak (raw/identified/cleaned/backup) + credential + exfiltrasyon DENY testleri değişmedi ve geçiyor.

## İtem 3 — tar_make TAMAMLANDI (pipeline güncel; çekirdek değerler doğrulandı)

`targets::tar_make()` bu oturumda kullanıcı direktifiyle koşuldu ve başarıyla
tamamlandı: **`ended pipeline [9m 10.4s, 310 completed, 235 skipped]`** (kaynak:
`/tmp/tar_make.log`). Hiçbir hedef fail etmedi; 3 hedef standart istatistik uyarısı
üretti (vcov→qr fallback; lavaan nonunique/extreme-order — hepsi tamamlandı).
Koşum sonrası `targets::tar_outdated()` = **0** (313 → 0; pipeline tam güncel).

**H1–H5 çekirdek değerleri yeniden üretilen aggregate tablolarla doğrulandı — bölümle birebir:**
- H1 EMBU-C reddetme β = 0,16 (`apa_t06`) — korundu.
- H4 SEM (`apa_t12`): Beck→reddetme 0,329 [0,191; 0,530]; Beck→sıcaklık −0,285 [−0,446; −0,152]; Beck→karşılaştırma 0,285 [0,138; 0,491]; Beck→aşırı koruma 0,082 [−0,054; 0,237] ns — bölümdeki 0,33 / −0,28 / 0,28 / 0,08 (ns) değerleriyle özdeş.

Faz V/VI eklemeleri (R/64, R/65) ve R/21/27/30 revizyonları **doğrulayıcı H1–H5
çekirdeğini değiştirmedi** (keşifsel katmanlar çekirdeğe dokunmaz — beklendiği gibi).
Böylece pipeline güncelliği tam kapatıldı; BULGULAR'ın her sayısı hem CSR kanonik
değerine hem de taze `outputs/tables/*.csv` artefaktına izlidir.

## Bu turda uygulanan içerik düzeltmeleri (CSR-izli)

1. §4.1 HbA1c yapısal/MNAR çerçeve düzeltmesi + glisemik hedef-bandı (CSR §9.4/§16).
2. §4.4.6 floor-IRT etiket hatası (reddetme d=0,37 + aşırı koruma d=0,54 ikisi de latent; CSR §15.4).
3. §4.4.6 karşılaştırma latent uyuşmazlığı r=0,18 + cross-informant GGM 1/16 (CSR §15.3).
4. §4.4.6 2023-only reddetme d=0,38→≈0 (CSR §18).
5. §4.4.1 aracılık GA 0,0019; §4.3.2 SRQ "sıcaklık/yakınlık, statü/güç" kanonik ad.
6. §4.4.6 intro post-hoc/ikincil + Holm/BH-FDR notu; §4.1 akış ayrımı.
7. Metot-çapaları `@benjaminiHochberg1995fdr` + `@simonsohn2020specificationCurve`.

**Adversarial doğrulama:** iki yanlış-pozitif reddedildi — H1 çoklu-evren "240"
(kanonik 120, CSR §15.9); MTMM H5 varyansı (çıktı diskte yok, CSR'de raporsuz);
aşırı koruma 2023-only değeri (CSR'de yok) eklenmedi.

## Bu turda değiştirilen izlenen dosyalar

- `chapters/04_bulgular.qmd` — kapsam düzeltmeleri + anlatım akışı
- `docs/analiz_planlari/02-sapma-tablosu.md` — ESEM kimliklenememe Tip-2 kaydı (#7)
- `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` — 5 metot-çapa cite-ok satırı + EOF normalize
- `plugins/doktoratezi-ai-audit/.../scripts/test_repo_ai_reliability.py` — 3-tier politika test güncellemesi + Tier-3 exfiltrasyon testi
- `plugins/doktoratezi-ai-audit/.../assets/ai-reliability/.codex/hooks/pre_tool_use_policy.py` — asset senkron
- `tez-yazim/04_kalite-kontrol/raporlar/04-bulgular-tr-sciaudit.md` — axis G çıktısı (exit 0)
- `tez-yazim/04_kalite-kontrol/sertifikalar/04-bulgular-sertifika-2026-07-14.md` — bu sertifika

## Galileo bağımsız judge (ai-judge) incelemesi — 2026-07-14

Kullanıcı talebiyle `galileo-audit` (bağımsız GPT-5.4 judge + gemini-embedding-001
semantik) `scripts/eval/galileo_bridge.py` üzerinden koşuldu (KVKK: gateway'e yalnız
manuskript metni).

**Deterministik + embedding katmanı — hepsi PASS:** heading_cascade (Marmara §1.3) 29
başlık 0 hata; coherence 103 paragraf, ortalama komşu-benzerlik 0,729, 0 akış-kopukluğu
0 tekrar; reference_prose 0 bulgu; judge skorları groundedness 0,74 / faithfulness 0,86
/ marmara 0,78 / halüsinasyon 0,28; **three-tier gate: hard=[] soft_block=[] advisory=[]**.

**Hedefli 4-soru judge (advisory):** mantıksal-sıralama 8/10, anlaşılırlık 6/10,
marmara 5/10, insani-Türkçe 5/10 (verdikt "büyük-revizyon"). Adjudikasyon: judge
verdikti advisory katmandadır; deterministik katman (sci-audit axis G 0 blocker +
heading/coherence/reference-prose PASS + three-tier temiz) çatışmada üstündür.

**Uygulanan judge-önerili küçük revizyon (6 hedefli düzeltme):** §4.4.4 "prototip olarak
konumlandırılmıştır" → "iç-validasyon düzeyindedir" (betimsel); §4.4.6 floor-IRT
"bastırma olasılığını gösterir" → latent/manifest yorumu Tartışma'ya devredildi +
yoğun paragraf bölündü; §4.4.8 "tükenme değil genelleşme işaret etmektedir" ve
"üç-kaynak asimetrisinin yönünü nicelemektedir" → betimsel + Tartışma-devri;
§4.4.1 "yorum düzlemi … triangülasyonuna kaydırılmış" ve §4.4.2 "öneri-düzeyi keşifsel"
→ doğallaştırıldı. Sonuç: axis G warning 34→33, 0 blocker; kilit sayılar (β=0,16,
d=0,37/0,54, d=−0,396 vb.) korundu; git diff --check CLEAN.

**Kovalanmayan kalan judge bulguları (gerekçeli):** (1) judge stokastik (koşumlar arası
±1-2 skor oynaması); (2) net yanlış-pozitif — judge Pandoc `[@key]` atıf **kaynak
sözdizimini** "Marmara'ya aykırı" sandı (CSL render'ı Marmara-AMA üretir; render exit 0
kanıtlı); (3) savunulabilir istatistik dili ("kanıt yetersizdir", "triangülasyon şartı
karşılanmadı" — doğru findings ifadeleri); (4) yöntem-açıklayıcı preamble cümleleri
okunabilirlik için bilinçli tasarım (silinmesi judge'ın anlaşılırlık eleştirisiyle
çelişir). Bu kalemler certified-final'i etkilemez; opsiyonel tasarım kararı olarak
kullanıcıya bırakılmıştır (preamble sadeleştirme / §4.4.6-4.4.8 kapsam daraltma).

## Karar

Kapı 0–5 tümü PASS; doğrulanmış blocker=0; iki-kol AI-reliability (144/144 + 55/55),
tam-tez render (exit 0) ve **tam `tar_make()` (313→0 outdated; H1–H5 çekirdek değerleri
taze tablolarla birebir doğrulandı)** geçti; kullanıcı (repo sahibi) açık direktifi
mevcut. Yol-haritası dört kalemi de tamamlandı; açık teknik istisna kalmadı. Statü
**`certified-final`**.

---

## Ek Tur — Şekil/Tablo Crossref Standardizasyonu (2026-07-14, ikinci tur)

**Kapsam:** `spec.md` R1–R2 gereksinimleri. Format kontratı §1.6 ihlalinin
(gövde metninde 0 şekil atıfı) giderilmesi ve tablo atıf stilinin manuel
"Tablo N"den Quarto-native `@tbl-` crossref'e taşınması.

**Uygulanan değişiklikler:**

- **R1 — Şekil crossref:** 26 şeklin her birine (`fig-strobe-flow` … `fig-sensemakr-contour`)
  içeriğiyle anlam-uyumlu paragrafa **birer** `@fig-<id>` metin-içi atıf eklendi.
  `{#fig-...}` etiketleri korundu; ID değişmedi. Yeni bilimsel iddia/atıf eklenmedi;
  yalnız mevcut şeklin tartışıldığı cümleye bağlaç eklendi.
- **R2 — Tablo crossref:** 22 tablonun manuel "Tablo N (`apa_tNN`)" çağrıları
  `@tbl-<id>` crossref'e çevrildi. Numara↔tanım sırası eşleşmesi korundu;
  numaralandırma artık Quarto tarafından dosya sırasına göre otomatik üretiliyor.
  Kalan manuel "Tablo N" / "Şekil N" ifadesi: **0** (04 içinde).

**Kapı sonuçları (bu tur) — tümü PASS:**

| Kapı | Kanıt | Sonuç |
|---|---|---|
| 0 | Kapsam değişmedi; yalnız crossref söz-dizimi; ham veri/credential bağlama alınmadı | ✅ PASS |
| 1 | Yeni iddia/atıf yok; yalnız görsel-referans bağlacı | ✅ PASS |
| 2 | `bib_hygiene.py all` HARD=0 (exit 0); yeni citation eklenmedi | ✅ PASS |
| 3 | 26/26 `@fig-` + 22/22 `@tbl-` çözümlendi; 0 manuel "Tablo N/Şekil N" kaldı | ✅ PASS |
| 4 | Metin akışı korundu; ondalık virgül/etiket bütünlüğü değişmedi | ✅ PASS |
| 5 | `quarto render thesis.qmd` **exit 0**; HTML'de 0 çözümsüz `?@`, 0 literal `@fig-/@tbl-` sızıntısı, 0 kırık atıf; `karma_ledger_check.py` TEMİZ (exit 0) | ✅ PASS |

**Doğrulama delili (birinci-el, bu oturum):**

- Render HTML: `Şekil&nbsp;1`–`Şekil&nbsp;26` ve `Tablo&nbsp;1`–`Tablo&nbsp;22`
  bağlı crossref olarak üretildi; `?@`/literal sızıntı taraması boş.
- Tüm `@tbl-`/`@fig-` etiketleri `#| label:` / `{#fig-}` tanımlarıyla birebir eşleşti.
- 9 metot-çapa citation'ı korundu; `.bib` mutabakatı bozulmadı.

Statü **`certified-final`** (crossref standardizasyonu dahil).
