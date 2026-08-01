# Derin İddia Doğrulaması — Bağlam-Penceresi + DOI Çözünürlüğü + İki-Kademeli Judge

**Tarih:** 2026-07-16
**Tetik:** "İddiaları daha derinlikli incele." Önceki turlar (2026-07-15) *sayı-varlığı*
düzeyinde çalışıyordu (kaynak metninde rakam geçiyor mu). Bu tur üç yeni derinlik
ekseni açar: (1) **bağlam-körlüğü** — sayı doğru yapı/yön/örneklem için mi geçiyor,
(2) **DOI→başlık çözünürlüğü** — atıf-anahtarı doğru esere mi işaret ediyor (yanlış-atıf),
(3) **bağlam-beslemeli judge** — GPT-5.4'e genel metin yerine sayının gerçek geçiş
penceresi verilir.

---

## Yönetici Özeti

| Sonuç | Değer |
|---|---|
| 🔴 **Çelişki** (kaynak farklı değer) | **0** |
| 🟠 **Yanlış-atıf** (DOI yanlış esere) | **0** |
| İncelenen atıf-bağlı sayısal iddia | **48** (39 dış-literatür hedefi) |
| DOI→başlık çözünürlüğü | **36/36 doğru esere** (5 "CHECK" = başlık-kesim artefaktı, hepsi birebir) |
| Bağlam-penceresi denetimi | tesadüfi substring yok; eşleşen sayılar doğru bağlamda |
| GPT-5.4 judge (bağlam-pencere) | 28 skor · ort **0,785** · min 0,700 · <0,65=**0** |
| GPT-5.4 judge (no-window gövde) | 10 skor · ort **0,758** · min 0,682 · <0,65=**0** |
| Toplam judge kapsamı | **38 kaynak · hiçbiri çelişki eşiğinin altında değil** |

**Karar:** Derin denetim hiçbir çelişki veya yanlış-atıf ortaya çıkarmadı. Bağlam-
penceresi analizi, önceki turun "matched" bulgularının tesadüfi substring değil gerçek-
bağlam eşleşmeleri olduğunu doğruladı. Bağlam-beslemeli judge ortalaması (0,785) genel-
metin turundan (0,752) yüksek çıktı — sayıların doğru bağlamda kullanıldığının bağımsız
teyidi. **Tez tarafında düzeltme gerekmedi.**

---

## Eksen 1 — Bağlam-Körlüğü Denetimi (yeni)

`scripts/util/context_window_audit.py`: her tez-sayısının kaynak tam-metnindeki tüm
geçişlerinin ±180 karakter penceresini çıkarır. Amaç: `0,001`, `%95` gibi yaygın
değerlerin **doğru cümlede** mi yoksa tesadüfen mi eşleştiğini görünür kılmak.

**Öne çıkan bağlam doğrulamaları:**

- **ziegler2013**: `%69,7 (95% CI 65,1–74,3)` → kaynakta "Progression to type 1 diabetes
  at 10-year follow-up ... 69.7% (95% CI, 65.1%-74.3%)" — CI yapısı birebir doğru bağlamda.
- **chen2023**: `%22,4 / %31,5 / %16,3 / %32,3` → "pooled prevalence 22.4% ... higher among
  mothers (31.5%) than fathers (16.3%) ... children (<12) (32.3%)" — tüm alt-grup değerleri
  doğru yapıda.
- **haugstvedt2011**: `r=0,25–0,37` → "reported the burden 0.25–0.37) with emotional
  distress ... only in mothers" — korelasyon aralığı ve "yalnız annelerde anlamlı" yönü doğru.
  Tablo hücresi `0,37` (Social restrictions 0.37, p<0.001) ile karışmadı; tez cümlesi
  aralığı doğru kaynaktan alıyor.
- **abadula2024**: `%9,6 vs %8,6; d=0,48` → "clinically significant depressive symptoms had
  higher mean HbA1c (9.6±2.4%) than ... not depressed (8.6±...)" — karşılaştırma yönü doğru.
- **dinleyici2019**: `75,1 / 83,4 / p<0,001` → kronik hastalık kardeşlerinde anlamlı düşük
  QoL, doğru bağlam.

**Sonuç:** Bağlam-penceresi taranan tüm eşleşmeler doğru yapı/yön/örneklem bağlamında;
tesadüfi substring eşleşmesi bulunmadı.

---

## Eksen 2 — DOI→Başlık Çözünürlüğü (yeni; yanlış-atıf denetimi)

`scripts/util/doi_title_resolve.py`: her hedefin bib-başlığını DOI'nin Crossref'te
çözdüğü gerçek başlıkla token-Jaccard karşılaştırır. Amaç: atıf-anahtarının **yanlış
esere** işaret edip etmediğini tespit (en ciddi hata sınıfı).

**36/36 DOI doğru esere çözündü.** 5 "CHECK" (Jaccard<0,4) manuel incelendi ve **hepsi
başlık-kesim artefaktı** çıktı (bib-title regex'i takip eden `journal=` alanını da
yakalıyordu; Crossref 80-char kesiyordu). Gerçek başlıklar birebir eşleşti:

| Anahtar | Durum | Not |
|---|---|---|
| goodman2011maternalMetaanalytic | ✅ birebir | "Maternal Depression and Child Psychopathology: A Meta-Analytic Review" |
| dinleyici2019siblingQoLTurkiye | ✅ birebir | "Quality-of-Life Evaluation of Healthy Siblings..." |
| kirchhofer2025sibsRiskModel | ✅ birebir | "Siblings in families of children with chronic disorders: a model of risk..." |
| barryMenkhaus2020t1dScreening | ✅ birebir | "Special Considerations in the Systematic Psychosocial Screening of Youth..." |
| webster2018siblingcaringroles | ✅ birebir | "Siblings' caring roles in families with a child with epilepsy" |

`dirik2015` DOI'siz (PMID 26111288 + Türk Psikiyatri URL ile önceki turda doğrulandı).
**Yanlış-atıf sıfır.**

> Not: Denetim sürecinde `kirchhofer2025` için manuel bir ara-testte yanlış bir DOI
> (`10.1007/s00787-025-02664-2`, Chen ve ark., Çin) elle girildiğinde judge farklı
> makaleye çözündü — bu, aracın hatalı-DOI'yi *yakaladığını* gösteren pozitif kontrol
> oldu. Bib'teki gerçek DOI (`10.1093/jpepsy/jsaf017`) doğru esere çözünüyor.

---

## Eksen 3 — İki-Kademeli Doğrulama

### Kademe 1 — Opus 4.8 elle bağlam (bu tur genişletildi)

- **zahidi2019** (önceki turda `layer=none`): Georgia Southern OA landing sayfasından
  tam abstract çekildi. Dört değer birebir: affection `r=−.03..06`, involvement
  `r=−.05..08`, "none statistically significant", n=133 Metro-Atlanta drug court,
  alt-grup non-sig. **Tam doğrulandı.**
- **arrindell1999** (`layer=none`): ScienceDirect noVNC challenge (otomasyon-dışı).
  arrindell2005 tam-metni "1950 students from Australia, Spain, and Venezuela" +
  üç-faktör yapısı (Rejection/Warmth/Overprotection) ile dolaylı destekliyor.
- **kirchhofer2025**: full-text path C narratifi doğru (düşük baba depresyonu → daha
  iyi kardeş QoL, p<.001; anne depresyonu anlamsız). Spesifik `B=−6,98`/`0,47`
  katsayıları Table 3/4 hücrelerinde (PMC gövdesinde render olmadı) — yön/yapı doğru,
  tablo-değeri erişim-dışı.

### Kademe 2 — GPT-5.4 judge, bağlam-beslemeli (yeni yaklaşım)

Bu tur judge'a genel metin yerine **sayının gerçek geçiş pencereleri** KANIT olarak
verildi (`scripts/util/judge_context_match.py`).

- Pencere-bulunan 28 kaynak: ort **0,785** · min 0,700 · max 0,883 · <0,65=**0**.
- no-window 11 kaynak tam gövdeyle ayrıca judge'landı: 10 skor · ort **0,758** ·
  min 0,682 · <0,65=**0** (arrindell1999 no-source).

**Toplam 38 kaynak judge'landı, hiçbiri 0,65 çelişki eşiğinin altında değil.** Bağlam-
beslemeli ortalama (0,785), önceki genel-metin turundan (0,752) yüksek — sayıların doğru
bağlamda kullanıldığının bağımsız işareti.

---

## İki-Kademeli Mutabakat

Opus 4.8 elle inceleme "DOĞRULANDI/bağlam-doğru" derken GPT-5.4 bağlam-beslemeli judge
tümünü ≥0,68 skorla teyit etti. **Uyuşmazlık yok** — convergent validity korundu.

---

## Kalan Sınırlar (çelişki kanıtı değil)

- **arrindell1999**: ScienceDirect noVNC challenge (otomasyon-dışı); arrindell2005 +
  başlıkla dolaylı desteklendi.
- **kirchhofer2025 / Pinquart×2 / Sharpe / Lovejoy**: meta-analiz/SEM tablo-değerleri
  PMC gövdesinde render olmayan tablolarda; yönü/yapısı/kümesi doğrulandı, spesifik
  etki-büyüklüğü erişim-dışı. `full-text-exception` statüsüyle tutarlı.

---

## Üretilen Araçlar (kalıcı)

- `scripts/util/context_window_audit.py` — bağlam-penceresi çıkarıcı (tesadüfi substring
  ayıklama).
- `scripts/util/doi_title_resolve.py` — DOI→Crossref başlık çözünürlüğü (yanlış-atıf
  denetimi).
- `scripts/util/judge_context_match.py` — bağlam-beslemeli GPT-5.4 judge Kademe 2.

**Ham çıktılar:** `2026-07-16-derin-baglam-pencere-ham.json`,
`2026-07-16-doi-baslik-cozunurluk-ham.json`, `2026-07-16-judge-baglam-pencere-ham.json`,
`2026-07-16-judge-nowindow-ham.json`.
