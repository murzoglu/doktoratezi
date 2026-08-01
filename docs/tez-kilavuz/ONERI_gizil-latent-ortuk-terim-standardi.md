# ÖNERİ: "gizil / latent / gizli / örtük" Terim Standardı

> **UYGULAMA KARARI (2026-07-29):** Kullanıcı, aşağıdaki öneride tavsiye edilen
> *gizil-kanonik* yönün **AKSİNE**, kanonik biçimin **`latent`** olmasına karar
> verdi. Bu kararın Marmara `lang: tr` (Türkçe tercih) kuralına aykırı olduğu
> kullanıcıya açıkça bildirildi ve kullanıcı tarafından kabul edildi.
>
> **Uygulanan:** Tüm `gizil*` → `latent*` (gizil profil/yetenek/değişken/
> konkordans/yapı dahil, ~15 gövde kullanımı) ve latent anlamındaki `gizli*`
> kullanımları → `latent`. **Dokunulmadı:** `gizli` (confounder, 04:1281-1282),
> `gizlilik` (KVKK/privacy), `gizli sinyal` (metafor, 05:604). Kanonik sözlük
> `docs/tez-kilavuz/terim-sozlugu.yaml` A1 bu karara göre ters çevrildi
> (kanonik=latent, yasak=gizil/örtük); `K4-TERM-01` kapısı bu yönü zorlar.
> Aşağıdaki analiz, kararın *öncesindeki* durumu ve gerekçe tartışmasını
> tarihsel bağlam olarak korur.

Durum: **öneri + uygulama notu** — öneri kısmı gizil-kanonik tavsiye ediyordu;
uygulama kararı yukarıdadır (latent-kanonik).
Oluşturma tarihi: 2026-07-29
Kapsam: `chapters/02_genel_bilgiler.qmd`, `chapters/03_gerec_ve_yontem.qmd`,
`chapters/04_bulgular.qmd`, `chapters/05_tartisma_ve_sonuc.qmd`

---

## 1. Sorun

Aynı istatistiksel kavram (*latent variable* — doğrudan gözlenemeyen, birden çok
gözlenen maddeyle temsil edilen yapı) tez boyunca **dört ayrı kelimeyle** anılıyor:

| Kelime | Toplam kullanım | Not |
|---|---:|---|
| `latent` (İngilizce) | 50 | En baskın; çoğu Bulgular'da |
| `gizil` | 19 | Türkçe tercih; çoğu Yöntem'de |
| `gizli` | 14 | Karışık — bir kısmı **farklı kavram** (bkz. §3) |
| `örtük` | 4 | Çoğu **istatistik dışı**, gündelik anlam (bkz. §3) |

Buna ek olarak zıt kavram (*manifest / observed*) da iki biçimde geçiyor:
`manifest` (İngilizce, ~10) ve `gözlenen` (Türkçe). Karmaşa çift yönlüdür.

**Dosya bazında dağılım:**

| Dosya | latent | gizil | gizli | örtük |
|---|---:|---:|---:|---:|
| 02_genel_bilgiler | 2 | 0 | 0 | 1 |
| 03_gerec_ve_yontem | 2 | 16 | 1 | 1 |
| 04_bulgular | 38 | 2 | 7 | 1 |
| 05_tartisma_ve_sonuc | 8 | 1 | 6 | 1 |

Sonuç: Yöntem bölümü büyük ölçüde **gizil**, Bulgular bölümü büyük ölçüde
**latent** kullanıyor. Bölümler arası tutarsızlık okuyucu için kavram
sürekliliğini bozuyor.

---

## 2. Önerilen Standart

### Kural 1 — Tek Türkçe terim: **"gizil"**
İstatistiksel *latent variable* kavramı için tez boyunca tek terim **gizil**
olsun. Gerekçe:
- Türk psikometri/istatistik yazınında *latent variable* karşılığı olarak
  **"gizil değişken"** yerleşik ve tercih edilen terimdir (ör. gizil profil
  analizi, gizil sınıf analizi çevirileri).
- Tez ana dili Türkçedir (`lang: tr`); İngilizce `latent` birincil metin terimi
  olmamalıdır.
- `gizil`, tezde zaten "gizil profil analizi" (LPA) için tutarlı kullanılıyor;
  bu terimle uyum sağlar.

### Kural 2 — İlk geçişte İngilizce karşılık parantezle verilsin
Kavramın **her bölümdeki ilk kullanımında** İngilizce özgün terim italik
parantezle eklensin, sonraki kullanımlarda yalnız Türkçesi kalsın:

> gizil (*latent*) değişken … [sonraki geçişler] … gizil yapı, gizil skor, gizil korelasyon

Bu, tezdeki mevcut İngilizce-karşılık verme biçimiyle (`WLSMV`, `bifactor`,
`multiverse` vb.) tutarlıdır.

### Kural 3 — Zıt kavram için tek Türkçe terim: **"gözlenen"**
*Manifest / observed* için tez boyunca **gözlenen** kullanılsın; ilk geçişte
`gözlenen (*manifest*)`. Böylece **gizil ↔ gözlenen** karşıtlığı Türkçe bir
çift olarak tutarlı kurulur (şu an `gizil ↔ manifest` gibi dil-karışık çiftler
var).

### Kural 4 — Türetilmiş ifadeler sabitlensin
Tek bir kalıp seti kullanılsın:

| Kavram | Önerilen sabit ifade |
|---|---|
| latent variable | gizil değişken |
| latent construct/structure | gizil yapı |
| latent score | gizil skor |
| latent factor | gizil faktör |
| latent correlation | gizil korelasyon |
| latent level ("at the latent level") | gizil düzeyde |
| latent concordance | gizil konkordans |
| latent ability (θ) | gizil yetenek (θ) |
| manifest / observed | gözlenen |

---

## 3. ÖNEMLİ İSTİSNALAR — bunları DEĞİŞTİRMEYİN

Aşağıdaki kullanımlar `latent variable` kavramı **değildir**; standardizasyon
bunlara dokunmamalıdır. Bunları körlemesine "gizil"e çevirmek **anlam hatası**
yaratır.

### 3.1 "gizli değişken" = ölçülmemiş karıştırıcı (unmeasured confounder)
`chapters/04_bulgular.qmd` sat. 1322–1323:
> "…sonuçların böyle bir **gizli değişkene** karşı yalnızca zayıf-orta düzeyde
> dayanıklı olduğunu gösterir. Böyle bir **gizli değişkenin** taşıması gereken…"

Bu, sensemakr duyarlılık analizindeki *unmeasured/omitted confounder* anlamındadır
— *latent variable* değil. **Öneri:** buradaki ifadeyi "gizil"e çevirmeyin;
tersine, karışıklığı önlemek için **"ölçülmemiş (gizli) karıştırıcı"** veya
"ölçülmemiş üçüncü değişken" biçimine netleştirin. Bu, gizil-değişken kavramıyla
karışmasını tamamen engeller.

### 3.2 "örtük / gizli" = gündelik/mecazi anlam
Bunlar istatistik terimi değildir, olduğu gibi kalmalıdır:

| Yer | İfade | Anlam |
|---|---|---|
| 03_gerec sat. 209 | "yarı **örtük** tıbbi gözlem" | gündelik: üstü kapalı |
| 04_bulgular sat. 1430 | "gerilimini **örtük** taşıma" | gündelik: açığa vurulmayan |
| 05_tartisma sat. 353 | "daha **örtük** veya hastalığa-özgü" | gündelik: gizli/belirsiz |
| 04_bulgular sat. 604 | "dağılımın üst ucundaki **gizli** sinyal" | mecazi: fark edilmeyen |
| 03_gerec sat. 175 | "**gizli** anne alt grupları" | LPA bağlamı — bu "gizil"e çevrilebilir (§3.3) |

### 3.3 Sınırda vaka — "gizli sınıf / gizli alt grup"
`gizli anne alt grupları`, `gizli profil` gibi LPA/LCA bağlamındaki "gizli"
aslında *latent*'tir ve **"gizil"e çevrilmelidir** (Kural 1). Yani bu bir istisna
değil, standardın kapsamındadır — yalnızca §3.2'deki gündelik "gizli"den
ayrılmalıdır.

---

## 4. Uygulama İçin Somut Değişiklik Listesi

Standart benimsenirse yapılacak değişiklikler (kavram-latent olanlar):

**A. `latent` → `gizil` (İngilizce terimi Türkçeleştir).** 50 kullanım.
Öneri: ilk-geçiş parantezleri hariç tümü `gizil`. Örnekler:
- 04_bulgular: "latent SES" → "gizil SES", "latent d = 0,37" → "gizil d = 0,37",
  "latent korelasyon" → "gizil korelasyon", "latent θ skorları" → "gizil θ
  skorları", "H4 … Latent Yapısal Eşitlik Modeli" → "…Gizil Yapısal Eşitlik Modeli".
- 05_tartisma: "latent (gizli-değişken) etki" → "gizil değişken etki",
  "gizli-değişken modelleri" → "gizil değişken modelleri".

**B. `manifest` → `gözlenen`.** ~10 kullanım (çoğu 04_bulgular H5).
- "manifest kanıt" → "gözlenen kanıt", "manifest ICC" → "gözlenen ICC",
  "manifest ortalama farklar" → "gözlenen ortalama farklar",
  "manifest (toplam-puan)" → "gözlenen (toplam-puan)".

**C. `gizli` (latent anlamında) → `gizil`.** ~7 kullanım (04_bulgular, 05_tartisma).
- "gizli (latent) düzeyde" → "gizil düzeyde", "gizli korelasyonu" → "gizil
  korelasyonu", "ortak … gizli bir …" → "ortak … gizil bir …", "gizli uzay" →
  "gizil uzay".

**D. `gizli değişken` (confounder) → NETLEŞTİR, gizil'e çevirme.** 2 kullanım
(04_bulgular sat. 1322–1323). "ölçülmemiş (gizli) karıştırıcı" biçimine.

**E. `örtük` / `gizli` (gündelik) → DOKUNMA.** 4–5 kullanım. Bkz. §3.2.

**F. İlk-geçiş parantezi ekle.** Her bölümün ilk gizil-değişken geçişine
`gizil (*latent*)`, ilk gözlenen geçişine `gözlenen (*manifest*)`.

---

## 5. Neden Bu Yön? (kısa gerekçe)

- **"gizil" > "latent":** Tez Türkçedir; Türkçe psikometri yazını "gizil değişken"i
  yerleştirmiştir; tez zaten "gizil profil"i kullanır.
- **"gizil" > "gizli":** "gizli" çok anlamlıdır (mahrem/saklı) ve tezde bir yerde
  *confounder* için de kullanılmıştır; "gizil" ise neredeyse yalnız teknik
  bağlamda kullanılır, karışma riski düşüktür.
- **"gizil" > "örtük":** "örtük" tezde ağırlıkla gündelik anlamda kullanılıyor;
  teknik terim olarak yüklenmesi bu gündelik kullanımlarla çatışır.
- **"gözlenen" > "manifest":** gizil'in Türkçe zıttı olarak simetri kurar; okuyucu
  için kavram çifti tek dilde tutarlı olur.

---

## 6. Denetim Notu

Bu standart benimsenip uygulanırsa, uygulama sonrası şu kontrol önerilir:
- `grep -niE "\blatent\b|\bmanifest\b" chapters/*.qmd` → yalnız ilk-geçiş
  parantezlerinde İngilizce terim kalmalı.
- `grep -niE "\bgizli\b" chapters/*.qmd` → kalan her "gizli" ya §3.2 gündelik
  ya §3.4 netleştirilmiş "ölçülmemiş (gizli) karıştırıcı" olmalı.
- Sayı/istatistik değeri değişmez; bu yalnız terim-dili düzenlemesidir
  (kanıt-değeri dokunulmaz).
