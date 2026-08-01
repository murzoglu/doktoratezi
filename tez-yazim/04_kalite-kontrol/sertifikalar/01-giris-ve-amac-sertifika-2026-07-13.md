# Bölüm Finalizasyon Sertifikası

Durum: `provisional-pass`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | 01 — GİRİŞ ve AMAÇ |
| Dosya | `chapters/01_giris_ve_amac.qmd` (21 satır, 10 paragraf, 45 cümle, 1276 sözcük) |
| Sertifika tarihi | 2026-07-13 |
| Strictness | `certification` |
| Önceki sertifika | `provisional-pass` (2026-07-12) — tam-tez render kanıtı bekliyordu |

## Kapsam (bu tur)

Kullanıcı isteğiyle **tam kapsamlı yeniden sertifikasyon** (delta değil, sıfırdan
Kapı 0–5). Bölüm metni (`chapters/01_giris_ve_amac.qmd`) 2026-07-12'den beri
**değişmedi** (git: unmodified); `references/references.bib` ve ledger yalnız
AMA-11 alan-tamamlama (pages/number/volume/address) + bir metodoloji ref'i
(`vehtari2021rhat`, GİRİŞ'te kullanılmıyor) + iki provenance notu (Pinquart
Minerva-404 yeniden doğrulama; OpenAthens MCP kurulumu) taşıyordu — **GİRİŞ
içeriğini etkileyen değişiklik yok**. Bu turda yürütülen tek düzeltme:
`goodman2020parentingMediator` ledger Bölüm-sütun tutarsızlığının kapatılması
(aşağıda Kapı 2).

Yöntem: birinci-el deterministik kanıt (kendim koştum) + 19-ajanlı çok-ajanlı
derin semantik denetim (4 kapı denetçisi + 15 çekişmeli-doğrulama ajanı;
`Workflow` run `wf_91edaae7-3d8`; 0 hata; ~3,99M subagent token).

## Kapı Sonuçları (0-5)

| Kapı | Kapsam | Kanıt | Sonuç |
|---|---|---|---|
| 0 | Kapsam/gizlilik | 20 `@key`, hepsi `references.bib`'de çözülüyor (0 çözümsüz); PII taraması (ad/soyad/e-posta/telefon/TCKN) temiz; kaynak seti `kritik-dosya-manifesti.tsv` L1–L3 katmanlarıyla eşleşiyor; ham veri/credential bağlama alınmadı | ✅ PASS |
| 1 | Derin literatür/iddia haritası | Tüm hedef sayılar ledger claim-notlarıyla **bire bir**: binde 0,75 · yüz binde 10,8 (yesilkaya2016) · ~108.300/~149.500 (ogle2022) · %22,4 genel/%31,5 anne (chen2023) · pinquart2013 g=−0,16/g=0,39 yön+büyüklük. Nedensellik dili hedge'li; ulusal-boşluk "belirgin değildir/sınırlıdır" kalıbında | ✅ PASS |
| 2 | Full-text/Zotero/ledger | 20 anahtarın tamamı @atıflı + ledger satırı + bib künyesi mevcut; **0 blocker** (orphan-citation yok, bib-orphan yok, retired/candidate atıflı kaynak yok). goodman2020 Bölüm-sütunu düzeltildi. İki ref (`eckshtain2010`, `butner2009`) `reliability-ok` — yalnız `certified-final` engeli | ✅ PASS (provisional) |
| 3 | Metin/kılavuz uyumu | 9 eksen temiz: başlık `# GİRİŞ ve AMAÇ` (alt başlık yok, §1.3/§3.3); ondalık **virgül** istisnasız; İngilizce-nokta `p` yok; yazar-yıl atıf (marmara-ama11 CSL); edilgen 3. tekil; hipotez≠araştırma sorusu; **tez-kaynak (yoktez) atfı yok** (§4.2/§3.8.2); amaç=doğrudan hedef; binlik ayraç tutarlı | ✅ PASS |
| 4 | Türkçe imla/akış (sci-audit axis G) | `tr_sciaudit.py --strictness certification --fail-on error` → **exit 0**; 0 blocker / 7 warning / 1 info. Uyarılar bilinen false-pozitif/kabul profili (aşağıda) | ✅ PASS |
| 5 | AI-reliability + render | aşağıda | ✅ PASS (tam-tez render kaydıyla) |

### Kapı 4 uyarı profili (0 blocker; 7 warning + 1 info gerekçeli kabul)

| Kod | Sayı | Gerekçe |
|---|---|---|
| `decimal-dot` | 2 | `108.300` / `149.500` — Türkçe **binlik ayracı** (ondalık değil); araç false-pozitifi |
| `abbreviation-review` | 1 (info) | IDF ilk kullanımda açık: "Uluslararası Diyabet Federasyonu (*International Diabetes Federation*, IDF)" |
| `sentence-long` | 4 | Satır 7/11/17/21 — yoğun akademik Türkçe; önceki turla aynı profil, kabul |
| `readability-very-hard` | 1 | Ateşman 3,03 — bilimsel yoğunlukla gerekçeli |

### Kapı 5 delili (birinci-el, bu oturum)

| Kontrol | Sonuç |
|---|---|
| `bib_hygiene.py all` | **exit 0** (HARD atıflı-tanımsız = 0) |
| `doktoratezi-ai-audit` (repo/veri invaryantı, KVKK/kilit/araç politikası) | **142/142 passed** |
| `t1dm-qual-ai-audit` (nitel kol çift kapı) | **55/55 passed** |
| `git diff --check` (chapter+bib+ledger) | **CLEAN** |
| `quarto check` | OK (Quarto 1.9.38; Pandoc 3.8.3 / Dart Sass / Deno / Typst / LaTeX 2026 / R 4.5.3 / Knitr — tümü ✓) |
| İzole GİRİŞ render (`--to html`, `references.bib` + `marmara-ama11.csl`) | **exit 0**; 17 metin-içi atıf linki + 23 kaynakça girdisi; **0 çözümsüz atıf** |
| Tam-tez `quarto render thesis.qmd` | **bloklu** — `outputs/tables/t01_sample_characteristics.csv` (gitignored, `targets::tar_make()` üretir) yok; **GİRİŞ dışı** (GİRİŞ'te R chunk yok) |

## Çok-ajanlı derin denetim (Workflow `wf_91edaae7-3d8`)

4 kapı denetçisi → her bulgu bağımsız skeptik ajanla çekişmeli doğrulama (15 ajan).

| Kapı | Denetçi verdiği | Çekişmeli doğrulama sonrası |
|---|---|---|
| Kapı 1 | PASS + 2 minor + 1 info | 2 minor → **false-positive** (Asya/Avrupa yorumu = yesilkaya2016'nın *kendi* manşet sonucu, birebir; "yaratmak" projenin `csr_causal_label_audit.py` nedensel-fiil register'ında **değil**); 1 info = state-machine notu |
| Kapı 2 | CONCERN + 3 major + 1 info | goodman2020 Bölüm-sütunu → **CONFIRMED (düzeltildi)**; eckshtain2010 + butner2009 `reliability-ok` → **CONFIRMED** (certified-final engeli); orphan/bib taraması info = temiz |
| Kapı 3 | PASS + 1 info | H-numaralandırma info → **false-positive** (R/16–20 kanonik H1–H5 eşlemesiyle uyumlu) |
| Kapı 5-A | PASS + minor/info | A–F temiz; **kritik teyit**: `butler2009→eckshtain2010` yanlış-atıf düzeltmesi doğru; P4 eckshtain / P6 butner **doğru bağlamda, karışmamış**; 2 claim-grounding minor → **false-positive** |

**Sonuç: doğrulanmış blocker = 0; doğrulanmış somut kusur = 1 (goodman2020 Bölüm-sütunu, bu turda kapatıldı).** Kalan tüm bulgular false-positive veya bilgi-düzeyi temiz-rapor.

## sci-audit 7-eksen bağlamı

Bölüm metni 2026-07-12'den beri değişmediğinden `01_giris_ve_amac-sci-audit.md`
(gerçek blocker=0) geçerliliğini korur; bu turda Kapı 5-A çok-ajanlı A–F yeniden
denetimi bağımsız olarak **0 blocker/major** teyit etti (no-fabrication
invaryantı her eksende beyan edildi).

## Neden `provisional-pass` (certified-final DEĞİL)

Tüm teknik/dil/referans/format kapıları PASS ve tek somut kusur kapatıldı.
`certified-final`'i engelleyen **iki koşul** kaldı:

1. **Tam-tez render + iki ref promosyonu.** `eckshtain2010parentDepression` ve
   `butner2009discrepancy` ledger'da `reliability-ok`; `cite-ok`'a yükselme
   koşulu (2026-07-12'de sabitlendi) = `targets::tar_make()` tamamlanıp tam-tez
   `quarto render thesis.qmd` exit 0 vermesi. Render bu ortamda Bulgular
   bölümündeki gitignored artefakt (`outputs/tables/t01_sample_characteristics.csv`)
   eksikliği nedeniyle durur; **GİRİŞ içeriğiyle ilgisizdir** (izole GİRİŞ render
   exit 0). Playbook Kapı 2, her referansın `cite-ok` olmasını şart koşar.
2. **Açık kullanıcı onayı.** Davranış kuralı #21 + playbook Nihai Karar #5:
   `certified-final` yalnız açık uygulama onayıyla ilan edilir.

**`certified-final`'e yükseltme koşulu:** `targets::tar_make()` + tam-tez
`quarto render thesis.qmd` exit 0 → ledger'da `eckshtain2010` + `butner2009`
`reliability-ok`→`cite-ok` taşınır → kullanıcı açık onay verir → bu sertifika
`certified-final`'e güncellenir.

## Bu turda değiştirilen izlenen dosyalar

- `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` —
  `goodman2020parentingMediator` Bölüm sütunu `GENEL BİLGİLER` →
  `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` (GİRİŞ 4. paragraf atıfını yansıtır; doğrulanan tek somut kusur)
- `tez-yazim/04_kalite-kontrol/raporlar/01_giris_ve_amac-tr-sciaudit.md` — axis G resmi çıktı (bu tur, exit 0)
- `tez-yazim/04_kalite-kontrol/sertifikalar/01-giris-ve-amac-sertifika-2026-07-13.md` — bu sertifika

## Bekleyen çapraz-bölüm notu (bu turda düzeltilmedi)

`sharpe2002siblings` ledger Bölüm sütunu `GİRİŞ ve AMAÇ, TARTIŞMA` diyor ancak
kaynak GİRİŞ metninde **atıflı değildir** (2026-07-05'te GİRİŞ'ten çıkarılmış;
durum `full-text-exception`). Bu bir TARTIŞMA-alanı ref'i olduğundan ve
commit'lenmemiş başka-bölüm düzenlemesi taşıdığından bu GİRİŞ turunda
düzeltilmedi; **TARTIŞMA bölümü sertifikasyonunda** Bölüm sütunundan
`GİRİŞ ve AMAÇ` çıkarılmalıdır.

## Karar

Teknik kapılar (0–5) PASS; doğrulanmış blocker=0; tek somut kusur kapatıldı.
Playbook Nihai Karar #3 (`cite-ok` şartı, 2 ref) ve #5 (açık onay)
sağlanmadığından statü **`provisional-pass`**'tir. `certified-final` için
tam-tez render + iki ref `cite-ok` promosyonu + açık kullanıcı onayı gerekir.
