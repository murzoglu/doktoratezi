# Üç Bölümü Klinisyen Diline Uyarlama — Sistematik Yürütme Planı

**Kapsam:** `chapters/03_gerec_ve_yontem.qmd` · `chapters/04_bulgular.qmd` ·
`chapters/05_tartisma_ve_sonuc.qmd` bölümlerinin **tamamını** `klinisyen-diline-uyarlama`
skill'iyle (kısıtlı-yeniden-yazım harness'i) Sosyal Pediatri klinisyen jürisine yeniden
üsluplamak.

**Değişmez ilke (çiğnenmez):** Bu yalnız **register/anlaşılırlık** uyarlamasıdır. Sayı · bulgu ·
yön · anlamlılık · atıf · `@tbl`/`@fig` token · `[KEŞİFSEL]`/`[POST-HOC]` etiketi · çekince
**DOKUNULMAZ** (harness `verify` ile mekanik korunur). Yeniden **çerçeveleme** (bir bulgunun
yorumunu/argüman yönünü değiştirmek) bu skill'in kapsamı DIŞIDIR → görülürse dur, `data-narrative`/
`anlatim-zenginligi`'ye devret (bkz. §9 Scope-exit). Otorite: `.claude/skills/klinisyen-diline-
uyarlama/SKILL.md`; sayısal bütünlük `AGENTS.md` "Sayısal Bütünlük Kaideleri".

Ölçümler (`grep`/`wc` ile alındı, `git` tarihli): 03 = 242 satır / ~34 alt-birim / 98 atıf;
04 = 1603 satır / 27 R-chunk / 72 tbl-fig-ref / 13 faz-etiket; 05 = 1045 satır / 65 blok /
12 kalın-etiket alt-bölüm / 94 atıf.

---

## 1. Bölüm profilleri ve neden farklı ele alınmalı

| Eksen | 03 Gereç-Yöntem | 04 Bulgular | 05 Tartışma-Sonuç |
|---|---|---|---|
| Karakter | saf nesir, jargon+atıf yoğun | nesir + 27 R-chunk, sayı yoğun | saf nesir, yorumlayıcı, uzun paragraf |
| Baskın risk | atıf bütünlüğü; terim tutarlılığı | sayısal iz; KEŞİFSEL/POST-HOC | **aşırı-iddia (overclaim)**; korelasyon→neden; sıfır-atıf tartışma |
| Kritik HARD kapı | `verify-citations` | `csr_numeric_trace_audit` | (HARD yok) |
| Kritik SOFT kapı | galileo faithfulness | galileo groundedness | **galileo overclaim + harking** |
| Rol (tez içi) | **terim-tanımlayıcı** (glossları burada sabitle) | terim-tüketici | terim + bulgu-tüketici |
| Harness zorluğu | orta (jargon çevirisi) | **yüksek** (H5 kalibre edildi) | orta-yüksek (uzun paragraf bölme) |

**Sonuç:** Sıra **03 → 04 → 05**. Gerekçe: 03'te her metodolojik terimin **tek klinik karşılığı**
sabitlenir (pre-registered glossary); 04 ve 05 aynı glossary'den okur → terim tutarlılığı
inşa gereği sağlanır. 05 en sona kalır çünkü hem 03 terimlerine hem 04 bulgularına atıf yapar
ve en yüksek overclaim riskini taşır (yorum katmanı).

---

## 2. Kanonik tur mekaniği (her alt-birim için sabit)

Skill'in Adım 0–2 akışı, alt-birim başına:

1. **Adım 0 — doğrula + envanter.** Alt-birimin gerçek `dosya:satır`ını `grep` ile bul. DOKUNULMAZ
   envanteri çıkar → **spec'e sınıfla** (`spans`=atomik sayı/token/etiket; `caveats`=**tam-cümle**
   çekince + **tam-yüklemli kapsam öbeği**; `glossary`=yalnız yabancı psikometrik model; `note`).
   Her sayıyı üreten artefakttan teyit et.
2. **Adım 1 — harness üret.** `python3 scripts/eval/constrained_rewrite.py < spec.json`.
   mask (`⟦KDUk⟧`) → üret (GPT-5.5) → **verify/retry** → splice. Her paragraf `verify.ok` olmalı;
   `failed` → paragrafı yeniden kur.
3. **Adım 2 — Claude değerlendir.** `verify.ok`'a güven (kanıt mekanik garanti); **bağlaç nesrini**
   denetle: F1 abartı/kapsam · F2 eklenen iddia/gloss · F3 pasif 3. tekil · F4 terim (partner→eş
   yok) · İSTATİSTİK-META (p/GA tanımı/filler yok) · register ("poliklinikte" yok, ondalık virgül) ·
   **dikiş** (run-on, büyük-harf maske önü, nokta düşmesi) · note-echo. 1–4 kelimelik ihlali elle
   onar; büyük ihlalde spec düzelt + yeniden koş (≤2–3 koşu); ısrarlı → reddet.
4. **Tur-yerel kapı → onay → Edit → journal satırı.** (Kapı seti §4.)

**Nihai metin = harness çıktısı + Claude Adım-2 elle onarımı.** Bir tur = bir alt-birim
(veya 05'te bir kalın-etiket bloğu). Bir turun çıktısı **onaysız teze yazılmaz**.

---

## 3. Birim hiyerarşisi

| Birim | Tanım | Bitişte ne olur |
|---|---|---|
| **Tur** | 1 alt-birim (§ veya kalın-etiket bloğu) | tur-yerel kapı + onay + Edit + journal satırı |
| **Dalga** | ilişkili alt-birimler kümesi (ör. "Veri Toplama Araçları"nın 5 alt-başlığı) | dalga-kapısı: çapraz-ref + terim audit + (04) numeric-trace bölgesel |
| **Bölüm kapanışı** | tüm bölüm bitince | tam kapanış kapısı + `/bolum-sertifika` |
| **Global kapanış** | üç bölüm bitince | çapraz-bölüm tutarlılık + `/tez-dogrulama` |

---

## 4. Kontrol noktaları — hangi kapı ne zaman

| Kapı | Araç | Tur | Dalga | Bölüm | Global |
|---|---|:--:|:--:|:--:|:--:|
| verify (kanıt bütünlüğü) | harness `verify.ok` | ✅ | | | |
| Adım-2 F1–F5 + dikiş + register | Claude | ✅ | | | |
| Türkçe imla + ondalık virgül (HARD) | `sci-audit:check-turkish --strictness certification` | ✅ | | ✅ | |
| Atıf bütünlüğü (HARD) | `sci-audit:verify-citations` | (03/05) | ✅ | ✅ | |
| İstatistik tutarlılığı (HARD) | `sci-audit:check-stats` | (04) | ✅ | ✅ | |
| Sayısal iz (HARD, yalnız 04) | `csr_numeric_trace_audit.py` (yüksek-risk eşsiz=0) | | ✅ | ✅ | |
| Terim tutarlılığı (HARD) | `terim_tutarlilik_audit.py` | | ✅ | ✅ | ✅ |
| Aşırı-iddia/groundedness (SOFT) | `galileo_judge` (evidence=orijinal+artefakt) | ✅ | | ✅ | |
| Overclaim + HARKing (SOFT, 05) | `galileo_overclaim_judge` · `galileo_harking_judge` | (05) | ✅ | ✅ | |
| Akış/tekrar (advisory) | `galileo_coherence` · `galileo_reference_prose` | | ✅ | ✅ | |
| Bib hijyeni | `bib_hygiene.py` | | | ✅ | ✅ |
| Çapraz-ref haritası (ileri/geri, özet/summary) | manuel + grep | | ✅ | ✅ | ✅ |
| Render (freeze temizle) | `quarto render` (bkz. §8 freeze) | | | ✅ | ✅ |
| Bölüm sertifikası | `/bolum-sertifika` (Kapı 0–5) | | | ✅ | |
| Kapsamlı checklist | `tez_checklist_verify.py --chapter` | | | ✅ | ✅ |
| Kapanış doğrulama | `/tez-dogrulama` | | | | ✅ |

**Kural:** herhangi **HARD FAIL = tur/dalga durur**, düzelt-ve-tekrar. **SOFT-block** bölüm
sertifikasını durdurur (insan-override'lı). Kapı sırası: harness verify → Adım 2 → tur-yerel HARD →
onay → Edit → dalga/bölüm kapıları.

---

## 5. Faz 0 — Ön-uçuş (yürütmeden ÖNCE, bir kez)

1. **Kanonik klinik-karşılık glossary'sini pre-register et.** Üç bölümün jargon envanterini çıkar
   (`grep` ile terim listesi) × `hedef-kitle-personasi.md` × `docs/tez-kilavuz/terim-sozlugu.yaml`.
   Her metodolojik terim için **tek** klinik karşılık + parantez-özgün-ad sabitle
   (ör. IPTW, eğilim skoru, DAG, SEM, ESEM, IRT, ICC, Bland-Altman, RSA, latent profil, ağ analizi,
   Bayes faktörü). Çıktı: `docs/tez-kilavuz/klinik-karsilik-sozlugu.md` (glossary asset). Bu, her
   turun spec `glossary`'sine beslenir → **terim tutarlılığı inşa gereği**.
   - **Uyum:** eklenen glosslar `terim-sozlugu.yaml` yasak-varyantlarını **ihlal etmemeli**
     (ör. "gizil" değil "latent"). Faz 0 sonunda + her dalgada `terim_tutarlilik_audit.py` HARD.
2. **Eşgüdüm kontrolü.** `bulgular-zenginlestirme-esgudum-playbook.md`: klinisyen-uyarla **son
   okunabilirlik geçişidir**; bir bölgede `anlatim-zenginligi` (literatür) hâlâ bekliyorsa **önce o**
   yapılır. Üç bölüm için "zenginleştirme tamamlandı mı?" durumunu işaretle (özellikle 05 tartışma).
3. **Temiz baseline anlık görüntüsü.** Yürütmeden önce koş: `tez_checklist_verify.py --fast` +
   `csr_numeric_trace_audit.py` (04) + `terim_tutarlilik_audit.py` + `bib_hygiene.py all`. Var olan
   FAIL'ler **bilinir kılınır** (uyarlamaya atfedilmesin). Baseline journal'a yazılır.
4. **Freeze/render hijyeni notu.** Bölüm render'ından önce `_freeze/` + `outputs/quarto/thesis*`
   ilgili girdileri temizlenir (yoksa değişiklik yansımaz — bilinen tuzak).
5. **Karar noktaları onayı** (§10) alınır. Faz 0 bitmeden hiçbir tur başlamaz.

---

## 6. Dalga planı — bölüm bölüm

### 6.1 Bölüm 03 (terim-tanımlayıcı; ~8 dalga, ~20–24 tur)
Sıra jargon-yükü ve terim-önceliğine göre; **glossları burada sabitle**.

| Dalga | Alt-birimler | Not |
|---|---|---|
| D1 | Araştırma Tasarımı · Sorular/Hipotezler · Yer/Tarih | hafif; ısınma + hipotez dili |
| D2 | Evren-Örneklem (+ dahil/dışlama · güç analizi · örnekleme) | güç analizi sayıları DOKUNULMAZ |
| D3 | Değişkenler · Veri Toplama Araçları (5 ölçek alt-başlığı) | s-EMBU/KİA/Beck glossları sabitlenir |
| D4 | Psikometrik Değerlendirme (madde · faktör · Bayes · eşdeğerlik · geçerlik · taban etkisi) | **en jargon-yoğun**; ESEM/IRT/invariance glossary |
| D5 | Veri Toplama Süreci · İstatistiksel Analiz (tanımlayıcı · eksik veri) | |
| D6 | Nedensel çıkarım · Hipotez modelleri · Duyarlılık/çok-evren · Bayes hattı · keşifsel katman | **DAG/IPTW/SEM/multiverse**; H1-H5 model dili (04'e köprü) |
| D7 | Nitel kol (desen · veri toplama · analiz · karma entegrasyon · refleksivite) | KVKK: yöntem metni uygundur; ham veri YOK |
| D8 | Raporlama std · Açık bilim/ön-kayıt · Etik · YZ araç | atıf/std yoğun; sapma beyanı DOKUNULMAZ |

**03 kritik kapı:** her dalgada `verify-citations` (98 atıf) + `terim_tutarlilik_audit`.

### 6.2 Bölüm 04 (sayı-tanımlayıcı; ~7 dalga, ~25–30 tur)
H5 zaten kalibre (v5 taslağı mevcut — `/tmp/kdu_h5_out5.json`; uygulama turunda yeniden üretilir).

| Dalga | Alt-birimler | Not |
|---|---|---|
| D1 | Örneklem/Tanımlayıcı · Ölçek/Veri Kalitesi | §4.1 kalibre edildi (26/26 span) |
| D2 | H1 · H2 · H3 | çoklu alt-ölçek; yön/anlamlılık DOKUNULMAZ |
| D3 | H4 (Beck→EMBU-P SEM) · H5 (diadik) | SEM/RSA formülleri → teknik ek; H5 kalibre |
| D4 | KEŞİFSEL: Aracılık · LPA · Ağ · Klinik Fayda | `[KEŞİFSEL]` etiketi korunur |
| D5 | KEŞİFSEL: DM alt · İleri Psikometrik · Artık İlişki · Gelişimsel-Diadik | `[POST-HOC]` korunur |
| D6 | Robustluk/Bayes · Nitel kol (örneklem + Tema 1–4 + çapraz + negatif vaka) | Bayes faktörü sayıları; KVKK nitel |
| D7 | Joint Display · Genel Bulgu Sentezi | karma köprü; çapraz-ref yoğun |

**04 kritik kapı:** her dalgada `csr_numeric_trace_audit` (yüksek-risk eşsiz=0) + `check-stats`;
R-chunk'lar (echo:false) **yeniden yazılmaz** — yalnız çevreleyen nesir. Yeniden sıralama olursa
tam `tar_make` + numeric-trace.

### 6.3 Bölüm 05 (yorum; ~4 dalga, ~12–16 tur)
Alt-birim = kalın-etiket bloğu + çevreleyen anlatı (başlık yok, tema-bazlı batch).

| Dalga | Bloklar | Not |
|---|---|---|
| D1 | Giriş anlatısı + H1/bilgi-verici düzlem tartışması | overclaim izle |
| D2 | Aracılık kırılması · üst-uç sinyal · tipoloji · ağ · ayrım-fayda | keşifsel bulgu tartışması; harking izle |
| D3 | Ölçüm/latent · robustluk · kardeş mimarisi · moderatör · DM bağlantısızlığı | korelasyon→neden kayması izle |
| D4 | Boylamsal yorum · sınırlılıklar · sonuç/çıkarım | **sıfır-atıf tartışma** + sonuç iddiaları |

**05 kritik kapı:** her turda `galileo_overclaim_judge` + `galileo_harking_judge` (SOFT-block);
her dalgada `verify-citations` (94 atıf). Reframe riski en yüksek → §9 scope-exit sıkı uygulanır.

---

## 7. Tur sayısı ve kadans

- **Toplam ≈ 60–70 tur / ~19 dalga** (03: ~22, 04: ~28, 05: ~14) + 3 bölüm-kapanışı + 1 global.
- **Kadans önerisi:** oturum başına **1 dalga** (birkaç tur) — Adım-2 elle dikiş-onarımı her turda
  insan-hızı gerektirir; toplu-otomasyon kalite düşürür. ~19 çalışma oturumu + kapanışlar.
- **Her dalga kendi içinde atomik:** yarım bırakılırsa bölüm tutarsız kalmaz (tur = en küçük
  onaylı-uygulanabilir birim). Dalga bitmeden bölüm render'ı yapılmaz.

---

## 8. Yürütme disiplini (her tur/dalga/bölüm)

- **Tur:** spec üret → harness → Adım 2 → tur-yerel HARD (check-turkish; 03/05 verify-citations;
  04 check-stats) → galileo SOFT → **onaya sun** (diff eski→yeni + F# + kapı özeti + dikiş onarımları)
  → onay → Edit → journal satırı.
- **Dalga:** dalga turları bitince → `terim_tutarlilik_audit` + çapraz-ref revalidasyonu +
  (04) bölgesel numeric-trace → dalga kapanış notu journal'a.
- **Bölüm:** tüm dalgalar bitince → (04 reorder ise `tar_make`) → tam `csr_numeric_trace_audit`
  (04) → `_freeze`/`thesis*` temizle → `quarto render` → `sci-audit:audit chapters/<b>.qmd --lang tr`
  → tam galileo → `tez_checklist_verify.py --chapter <b>` → `/bolum-sertifika`.
- **Global:** üç bölüm bitince → çapraz-bölüm terim tutarlılığı (03↔04↔05) + ileri/geri atıf
  zinciri (03 yöntem → 04 bulgu → 05 yorum) + özet/summary (00c) senkronu + `bib_hygiene` +
  `tez_checklist_verify` (tam) → `/tez-dogrulama`.

---

## 9. Scope-exit — DUR ve devret (register sınırını aşan durum)

Klinisyen-uyarla **yalnız register**; şunlar görülürse **turu durdur**, uygun kapıya devret:
- Bir bulgunun **yorumunu/argüman yönünü** değiştirme ihtiyacı (özellikle 05) → bu bir
  **reframe**'dir; klinisyen-uyarla yapmaz. Not düş, kullanıcıya bildir (gerekirse ayrı iş).
- **Yeni literatür/atıf** eklemek gerekiyorsa → `anlatim-zenginligi` · `referans-kapisi`.
- **Figür/tablo sunumu** düzeltmesi → `veri-gosterimi-zenginligi`.
- **Ayrı açıklama** (metni değiştirmeden) → `data-narrative`.
- **Recert maliyeti:** register-only değişim K5-NUM/K5-LIT immutability'yi tetiklememeli; 05'te
  yeniden-çerçeveleme yapılırsa **tam recert** gerekir → bu yüzden reframe yasak (memory:
  ch05 reframe → full-recert).

---

## 10. Karar noktaları — ✅ KİLİTLENDİ (2026-07-29, kullanıcı onayı)

1. **Sıra:** ✅ **03 → 04 → 05** (terim-önce).
2. **Derinlik:** ✅ **Tamamı, ölçek-uyumlu** — her nesir alt-birimi; skill basit pasajda hafif
   dokunuş, ağır jargon pasajında tam yeniden kurma yapar.
3. **Eşgüdüm:** ✅ **Zenginleştirme tamamlandı** — doğrudan klinisyen-uyarla (önce-zenginleştir
   şartı bu bölgelerde karşılanmış sayılır; yine de bir turda literatür ihtiyacı çıkarsa §9
   scope-exit → `anlatim-zenginligi`).
4. **Kadans:** ✅ **Oturum başına 1 dalga** (varsayılan; kalite-hız dengesi).
5. **Faz 0 glossary:** ✅ **`docs/tez-kilavuz/klinik-karsilik-sozlugu.md` pre-register edilecek**
   (terim tutarlılığının belkemiği; her tura beslenir).

**Sonraki adım:** Faz 0 (§5) — glossary pre-register + baseline snapshot + eşgüdüm teyidi;
ardından 03/D1'den turlar başlar. Faz 0 kullanıcı "başla" deyince yürütülür.

---

## 11. Dokümantasyon ve izleme

- Bu plan: `tez-yazim/04_kalite-kontrol/klinisyen-uyarlama-3bolum-plani.md` (bu dosya).
- Her tur/dalga/bölüm ilerlemesi **journal**'a (`klinisyen-diline-uyarlama-journal.md`):
  Durum panosu satırı (Bölüm/Pasaj · Durum · Son dokunuş · Not) + Seans günlüğü girdisi
  (pasaj · üretici model + tur sayısı · F# bulguları + karar · dikiş onarımları · kapı sonucu ·
  tez-geneli bağlam etkisi · açık takipler).
- Durum değerleri: `bekliyor → işlendi-onay bekliyor → uygulandı → certified`.
- Glossary güncellemeleri (yeni terim) → `klinik-karsilik-sozlugu.md` + backlog.

---

## 12. Özet akış (tek bakış)

```
Faz 0 (bir kez): glossary pre-register · eşgüdüm kontrol · baseline snapshot · freeze hijyen · karar onayı
   ↓
03 (D1..D8)  →  04 (D1..D7)  →  05 (D1..D4)
  her DALGA:  [ her TUR: spec→harness(verify)→Adım2→HARD+SOFT kapı→onay→Edit→journal ]
              →  dalga kapısı: terim audit + çapraz-ref (+04 numeric-trace)
   ↓ (bölüm bitince)
Bölüm kapanışı: (tar_make) · numeric-trace · freeze-temizle+render · sci-audit:audit · galileo · checklist --chapter · /bolum-sertifika
   ↓ (üç bölüm bitince)
Global kapanış: çapraz-bölüm terim + atıf zinciri + özet/summary senkron · bib_hygiene · checklist(tam) · /tez-dogrulama
```
