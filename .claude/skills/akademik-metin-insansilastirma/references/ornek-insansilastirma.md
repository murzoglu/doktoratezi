# ÇÖZÜMLÜ ÖRNEK — uçtan uca bir insansılaştırma turu

Aşağıdaki tur, kapının beş adımını gerçek komut çıktısıyla gösterir. Sayılar örnektir;
gerçek işte artefakttan teyit edilir.

---

## Adım 0 — Kaynak pasaj ve envanter

**Kaynak (LLM taslağı):**

> Bu bağlamda, ebeveyn reddi ile çocuk depresyon düzeyi arasındaki ilişki kapsamlı bir
> şekilde incelenmiştir.
> Analiz sonuçlarına göre ebeveyn reddi ile depresyon puanı arasında orta düzeyde pozitif
> bir ilişki saptanmıştır (r = 0,38; p < 0,001).
> Bu ilişki, yaş ve cinsiyet kontrol edildikten sonra da anlamlılığını korumuştur
> (β = 0,29; %95 GA [0,12; 0,45]).
> Kontrol grubunda ise aynı ilişki anlamlı bulunmamıştır (r = 0,08; p = 0,412).
> Bulgular @tbl-apa-h1 ve @fig-h1-forest içinde sunulmuştur ve önceki çalışmalarla
> uyumludur [@rohner2005; @dirik2014].
> Çalışma kesitsel olduğundan nedensellik çıkarılamaz ve bulgular dikkatle
> yorumlanmalıdır [KEŞİFSEL].

```bash
python3 scripts/eval/humanize_invariant_guard.py inventory /tmp/kaynak_pasaj.md
```

Envanter (özet): `sayi` 8 · `istatistik` 5 (`r=0,38`, `p<0,001`, `β=0,29`, `r=0,08`,
`p=0,412`) · `aralik` 1 (`%95GA[0,12;0,45]`) · `atif` 2 · `capraz_ref` 2 · `etiket` 1
(`KEŞİFSEL`) · `cekince` 4 · `olumsuzluk` 2.

**Anlamsal öz notu (elle):** ilişki *orta düzeyde ve pozitif*; anlamlılık *kontrol
sonrası* korunuyor; kontrol grubunda ilişki **yok**; tasarım kesitsel; kanıt keşifsel.

---

## Adım 1 — Teşhis

```
cümle=6 sözcük=92 ort=15.33 SS=3.9 cv=0.254 B=-0.594
min/medyan/maks=10/14.0/21 kısa=0.167 uzun=0.0 tekdüze_seri=2/4
klişe=2 (21.74/1000) bağlaç_başı=0.167 MATTR=0.75 TTR=0.75 hapax=0.598
klişe listesi: bu bağlamda×1, kapsamlı bir şekilde×1
```

Okuma: `cv = 0,254` (hedef ≥ 0,40) → **ritim tekdüze**; uzun cümle payı **sıfır**;
klişe yoğunluğu 21,7/1000 (hedef ≤ 2,0) → **kalıp temizliği** gerekli.
`tekdüze_seri=2/4` gözlenen/sınır çiftidir; sınır cümle sayısıyla logaritmik büyür.

---

## Adım 2 — Yeniden yazım (üç katman)

**Aday:**

> Reddedilme, çocuğun ruhsal yükünü nasıl taşıdığını değiştirir.
> Ebeveyn reddi ile depresyon puanı arasında orta düzeyde pozitif bir ilişki
> saptanmıştır (r = 0,38; p < 0,001); bu büyüklük, klinik gözlemin uzun süredir işaret
> ettiği örüntüyü ilk kez bu örneklemde sayısallaştırmaktadır.
> Yaş ve cinsiyet kontrol edildiğinde ilişki ayakta kalmıştır
> (β = 0,29; %95 GA [0,12; 0,45]).
> Kontrol grubunda tablo farklıdır: aynı ilişki anlamlı bulunmamıştır
> (r = 0,08; p = 0,412).
> Ayrıntılar @tbl-apa-h1 ve @fig-h1-forest içinde sunulmuş olup örüntü, reddedilme
> kuramının öngörüsüyle örtüşmektedir [@rohner2005; @dirik2014].
> Yine de tasarım kesitseldir. Nedensellik çıkarılamaz; bulgular dikkatle
> yorumlanmalıdır [KEŞİFSEL].

**Hangi hamle nerede:**

| Hamle | Uygulama |
| --- | --- |
| Klişe silme (Katman C) | "Bu bağlamda" ve "kapsamlı bir şekilde" **silindi**, yerine sözcük konmadı |
| H1 tez+analitik (Katman A) | 6 sözcüklük açılış + 30 sözcüklük analitik cümle |
| H4 bilgi sırası (Katman A) | "Bu ilişki, … korumuştur" → "Yaş ve cinsiyet kontrol edildiğinde …" (koşul önce) |
| İki nokta ile karşıtlık | "Kontrol grubunda tablo farklıdır: …" |
| H3 böl-birleştir | Çekince cümlesi ikiye ayrıldı: kısa + noktalı virgüllü |
| Katman D (ses) | "klinik gözlemin işaret ettiği örüntüyü sayısallaştırmaktadır" — **yeni kanıt yok**, var olanın yorumu |

**Yapılmayanlar:** hiçbir sayı yuvarlanmadı; "orta düzeyde" ve "pozitif" nitelemeleri
korundu; "anlamlı bulunmamıştır" olumsuzlaması aynen kaldı; `[KEŞİFSEL]` etiketi ve
dört çekince imleci taşındı; terim değiştirilmedi.

---

## Adım 3 — Mekanik kapı

```bash
python3 scripts/eval/humanize_invariant_guard.py all \
  --source /tmp/kaynak_pasaj.md --candidate /tmp/aday_pasaj.md
```

```
ÖZ KARŞILAŞTIRMASI — kaynak span=31 · aday span=30

SOFT (inceleme gerektirir — meşru olabilir, gerekçelendir):
  ~ [düştü] yon: 'anlamlı'

RİTİM/ÇEŞİTLİLİK — KAYNAK
  cümle=6 sözcük=92 ort=15.33 SS=3.9 cv=0.254 B=-0.594
  ...
RİTİM/ÇEŞİTLİLİK — ADAY
  cümle=7 sözcük=96 ort=13.71 SS=8.86 cv=0.646 B=-0.215
  min/medyan/maks=4/14/32 kısa=0.429 uzun=0.143 tekdüze_seri=2/4
  klişe=0 (0.0/1000) bağlaç_başı=0.0 MATTR=0.844 TTR=0.844 hapax=0.75

ÜSLUP HEDEFİ:
  hedefler karşılandı
```

**HARD yok.** Tek SOFT satırı: kaynakta iki kez geçen "anlamlı" kökü adayda bir kez
geçiyor ("anlamlılığını korumuştur" → "ayakta kalmıştır").
**Gerekçe:** anlamlılık bilgisi cümlede `p` ve `%95 GA` ile zaten taşınıyor; kontrol
grubundaki "anlamlı bulunmamıştır" olumsuzlaması korunmuş durumda. Kabul edilir.

**Ritim kazancı:** `cv` 0,254 → **0,646**; klişe 21,7/1000 → **0**; MATTR 0,750 → **0,844**;
uzun cümle payı 0 → 0,143.

---

## Adım 4 — Karşı örnek: neyin reddedildiği

Aynı pasaj "agresif humanizer" mantığıyla yeniden yazılsaydı:

> Reddedilme çocuğun ruhsal yükünü **belirlemektedir**. … güçlü pozitif bir ilişki
> saptanmıştır (**r = 0.42**; p < 0,001). … Kontrol grubunda aynı ilişki **de anlamlı
> bulunmuştur** … Bulgular @tbl-apa-h1 içinde sunulmuştur [@rohner2005]. Bu sonuçlar
> reddedilmenin depresyona neden olduğunu **kesinlikle kanıtlamaktadır**.

Guard çıktısı (kısaltılmış):

```
HARD İHLAL (teslim engeli — öz değişmiş):
  ! [DÜŞTÜ] aralik: '%95GA[0,12;0,45]'
  ! [DÜŞTÜ] atif: '@dirik2014'
  ! [DÜŞTÜ] capraz_ref: '@fig-h1-forest'
  ! [DÜŞTÜ] cekince: 'kesitsel' / 'nedensellik çıkarılamaz' / 'dikkatle yorumlan'
  ! [DÜŞTÜ] etiket: 'KEŞİFSEL'
  ! [DÜŞTÜ] istatistik: 'r=0,38'
  ! [DÜŞTÜ] olumsuzluk: 'anlamlı bulunmamış'
  ! [UYDURULDU] istatistik: 'r=0.42'
  ! [KESİNLİK ENFLASYONU] kesinlik: 'kesinlikle' / 'kanıtlamaktadır' / 'belirlemektedir'
exit 1
```

Yedi ayrı öz ihlali: mutasyon (`0,38`→`0.42`, üstelik ondalık nokta), yön ters çevirme
(olumsuzlama kaybı), atıf/çapraz-referans düşmesi, çekince ve kanıt-düzeyi etiketi
kaybı, nedensellik yükseltmesi. **Override yoktur.**

---

## Adım 5 — Onaya sunum iskeleti

```
1) DIFF        : (eski → yeni), cümle bazında
2) GUARD       : HARD 0 · SOFT 1 (yon:'anlamlı' — gerekçe: p ve %95 GA cümlede duruyor)
3) RİTİM       : cv 0,254→0,646 · klişe 21,7→0,0/1000 · MATTR 0,750→0,844 · uzun 0,00→0,14
4) ANLAMSAL ÖZ : yön (pozitif/orta) ✓ · kapsam (kontrol sonrası) ✓ · kontrol grubu
                 olumsuzluğu ✓ · kesinlik derecesi ✓ · atfetme ✓ · [KEŞİFSEL] ✓
5) REPO KAPILARI: tr_corpus_audit ✓ · terim_tutarlilik ✓ · bib_hygiene ✓ ·
                 claim_certification ✓ · galileo_judge (SOFT) ✓
6) YAZAR NOTU  : yok
=> Onay bekleniyor. Onaysız Edit/commit yok.
```
