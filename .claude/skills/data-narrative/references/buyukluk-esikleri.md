# Büyüklük Okuryazarlığı — "Bu Değer İyi mi?" Sorusunu Kaynaklı Yanıtlamak

Bir sayı ("CFI = 0,887", "α = 0,45", "BF₁₀ = 6,93", "|SMD| = 0,004") tek başına
anlamsızdır; anlamı **kendi ölçeğindeki geleneksel eşiğe** göre doğar. Okura "iyi mi?"
sorusunun yanıtını verememek, açıklamanın en sık eksiğidir. Bu dosya, o yanıtı
**kaynaklı, gelenek-olarak-çerçevelenmiş ve tezin kendi kullanımıyla bağlanmış**
biçimde vermenin kaynağıdır.

## Üç değişmez kural (önce bunlar)

1. **Eşik yasa değil, gelenektir.** Her eşiği **kökeniyle** ver (kim önerdi) ve "kesin
   sınır değil, yaygın gelenek" diye çerçevele. Tez gerekçeli olarak sapabilir; sapma
   varsa gizleme, gerekçesini aktar.
2. **Tek indekse indirgeme.** Bir modelin "iyiliği" tek sayıdan okunmaz; indeksler
   çelişebilir (bkz. sonda H4 örneği) — hepsini birlikte oku, çelişkiyi açıkla.
3. **Sayısal bütünlük (AGENTS.md).** Eşiği ve tezdeki fiili değeri **birebir**, ondalık-
   virgülle aktar; yuvarlama/uydurma yok. Tezdeki değeri kaynağından (dosya:satır /
   CSV / model artefaktı) teyit et.

---

## Eşik tabloları (kaynak + tezdeki çıpa)

### Etki büyüklüğü — Cohen (1988) gelenekleri
| Ölçüt | Küçük | Orta | Büyük |
|---|---|---|---|
| Cohen d / Hedges g | 0,20 | 0,50 | 0,80 |
| Korelasyon r | 0,10 | 0,30 | 0,50 |
- Kaynak: @cohen1988power. **Gelenek**, alan-bağımlı değil; ebeveynlik/kronik hastalık
  alanında küçük-orta etkiler normdur.
- Tez çıpası: güç hesabı d = 0,5–0,8 üzerinden [chapters/03_gerec_ve_yontem.qmd:38];
  Pinquart meta-etkileri g ≈ 0,39 (aşırı koruma), g ≈ −0,22 (sıcaklık)
  [chapters/03_gerec_ve_yontem.qmd:171].
- Numeracy: d = 0,2 → gruplar ~%85 örtüşür (küçük); d = 0,8 → belirgin ayrışma.

### Model uyumu (CFA/SEM) — Hu & Bentler (1999)
| İndeks | İyi | Kabul edilebilir | Zayıf |
|---|---|---|---|
| CFI, TLI | ≥ 0,95 | ≥ 0,90 | < 0,90 |
| RMSEA | ≤ 0,06 | ≤ 0,08 | ≥ 0,10 |
| SRMR | ≤ 0,08 | — | > 0,10 |
- Kaynak: @huBentler1999cutoff (tezde atıflı).
- **Uyarılar (öğret):** (a) **RMSEA büyük serbestlik derecesinde yanıltıcı biçimde
  düşük** çıkabilir — çok maddeli/yüksek-sd modelde tek başına "iyi" kanıtı sayma;
  (b) χ² örneklem büyüklüğüne aşırı duyarlıdır; (c) iyi uyum **doğru model** ya da
  **nedensellik** demek değildir, yalnız "veri deseniyle bağdaşır" demektir.
- Tez çıpası: H4 CFI 0,887 / TLI 0,890 / RMSEA 0,027 / SRMR 0,127
  [chapters/04_bulgular.qmd:777]; tezin kendi karışık-uyum ifadesi [:783].

### Ölçüm değişmezliği — Cheung & Rensvold (2002); Chen (2007)
- ΔCFI ≤ 0,010 ve ΔRMSEA ≤ 0,015 → değişmezlik desteklenir.
- Tez çıpası: metric/scalar |ΔCFI| eşik içinde, ama mutlak uyum sınırlı (CFI ≈ 0,82)
  [chapters/04_bulgular.qmd:791; :797].

### İç tutarlılık güvenirliği
- α / ω ≥ 0,70 kabul; ≥ 0,80 iyi; < 0,70 dikkat.
- **Uyarı:** α **az maddeli / kısaltılmış** ölçekte ve tau-eşitsizliğinde düşük çıkar;
  ω (McDonald) daha sağlamdır. Düşük α'yı **gizleme**; ne yapıldığını söyle.
- Tez çıpası: EMBU-P **reddetme α = 0,45** (zayıf; dürüstçe raporlanır)
  [chapters/04_bulgular.qmd:583]; ω polikorik temelli hesaplanmış
  [chapters/03_gerec_ve_yontem.qmd:95].

### Uyum / sınıf-içi korelasyon (ICC) — Koo & Li (2016)
| ICC | Yorum |
|---|---|
| < 0,50 | zayıf |
| 0,50–0,75 | orta |
| 0,75–0,90 | iyi |
| > 0,90 | mükemmel |
- Bu tezde ICC(2,1) / ICC(A,1) (mutlak uyum, iki yönlü rastgele etkiler)
  [chapters/03_gerec_ve_yontem.qmd:163]. Uyum ayrıca Bland–Altman (@blandAltman1986) ve
  Gwet AC1 (@gwet2008ac1) ile [:111].
- **Uyarı:** ICC bağlama duyarlıdır; "uyum" (agreement) ile "tutarlılık" (consistency)
  farklıdır — hangisinin raporlandığını belirt.

### Kovaryat denge / SMD — Austin (2011)
- |SMD| < 0,10 ihmal edilebilir; 0,10–0,25 tolere edilebilir; > 0,25 kayda değer
  dengesizlik.
- Tez çıpası: Love grafiği eşikleri 0,10 / 0,25 [`@fig-smd-love` altyazısı];
  ham |SMD| 0,220 → IPTW 0,004 [`references/ornek-tablo-4-4.md`].

### Bayes faktörü — Jeffreys / Lee & Wagenmakers ölçeği
| BF₁₀ | Kanıt (H1 lehine) |
|---|---|
| 1–3 | zayıf (anecdotal) |
| 3–10 | orta |
| 10–30 | güçlü |
| 30–100 | çok güçlü |
| > 100 | aşırı |
- **BF₁₀ < 1 → H0 lehine** oku (resiprokal: BF₁₀ = 0,29 ≈ BF₀₁ ≈ 3,4, yani "H0 lehine
  orta"). "Kanıt yetersizliği" (BF ≈ 1) ile "H0 lehine kanıt" (BF₁₀ ≪ 1) **farklıdır**.
- Tez çıpası: H1 reddetme BF₁₀ = 10,55 ("güçlü"), aşırı koruma 6,93 ("orta"), sıcaklık
  0,29 (H0 lehine); H3 aralığı 0,17–0,23 [chapters/04_bulgular.qmd:621; :1328].
- Kaynak: @wagenmakers2010 (Savage–Dickey).

### ROPE (pratik eşdeğerlik) — Kruschke (2018)
- Sonsalın ROPE içindeki payı yüksekse "etki pratikte önemsiz" lehine kanıt.
- Tez çıpası: H3 reddetme ROPE içi pay %93 ("orta-güçlü H0 lehine")
  [chapters/04_bulgular.qmd:1330].

### Sınıflandırma — AUC (Hosmer–Lemeshow gelenekleri)
| AUC | Yorum |
|---|---|
| 0,50 | şans |
| 0,70–0,80 | kabul edilebilir |
| 0,80–0,90 | mükemmel |
| > 0,90 | üstün |
- **Uyarı:** görünür (apparent) AUC **iyimserdir**; optimizm-düzeltilmiş değer daha
  dürüsttür. Kesitsel eşzamanlı sınıflandırma ≠ ileriye dönük risk yordaması.

### Eşdeğerlik sınırı (SESOI) / TOST — Lakens (2017)
- Bu tezde ±0,30 SMD (Pinquart-uyumlu, ihtiyatlı varsayılan)
  [chapters/03_gerec_ve_yontem.qmd:167]. Ölçeğe özgü ampirik eşik yoksa bunu belirt.

### Duyarlılık — E-değeri / RV (VanderWeele & Ding 2017; Cinelli & Hazlett 2020)
- Büyük E-değeri / RV = ölçülmemiş karıştırıcıya karşı **sağlam** bulgu.

### LPA/gizil profil — entropi
- Entropi ≥ 0,80 iyi sınıf ayrımı (yol gösterici, kesin eşik değil). Model seçimi tek
  eşiğe değil, parsimoni kuralına (ΔBIC≤2) ve yorumlanabilirliğe bağlanır.

---

## Sayıyı günlük dile çevirme (numeracy)

- **OR = 1,8** → "olasılık kabaca 1,8 kat"; ama düşük taban oranında riske **eşit
  değildir**, abartma.
- **Standardize β = 0,33** → "yordayıcıda 1 SS artış, sonuçta ~0,33 SS değişimle birlikte
  gider" (nedensellik değil, birlikte-değişim).
- **d = 0,50** → "ortalama fark yaklaşık yarım standart sapma; belirgin ama örtüşme çok".
- **r = 0,30** → "ortak varyans ≈ r² = %9".
- **|SMD| = 0,004** → "neredeyse sıfır fark; elmayla elma".
- **küçük p** ≠ **büyük etki**: p "sıfırdan ayırt edilebilir mi", etki büyüklüğü "ne
  kadar" sorusudur. İkisini daima ayrı söyle.

---

## Worked örnek — karışık uyum karnesini dürüstçe okumak (H4)

Komite "bu uyum değerleri yeterince iyi mi?" diye sorarsa, yanıt **tek kelime değildir**:

| İndeks | Değer | Eşik | Karne |
|---|---|---|---|
| RMSEA | 0,027 | ≤ 0,06 | mükemmel *görünüyor* ⚠️ |
| SRMR | 0,127 | ≤ 0,08 | eşiğin belirgin üstünde ❌ |
| CFI | 0,887 | ≥ 0,90 (ideal 0,95) | altında ⚠️ |
| TLI | 0,890 | ≥ 0,90 | altında ⚠️ |

Değerler [chapters/04_bulgular.qmd:777]. Öğretilecek incelik: **RMSEA yüksek serbestlik
derecesinde yanıltıcı biçimde düşer**; bu yüzden 0,027 tek başına "iyi model" kanıtı
değildir — SRMR ve CFI/TLI daha ihtiyatlı hikâyeyi anlatır. Dürüst yanıt: uyum
geleneksel ölçütlere göre **karışık ve sınırlıdır**; tez de bunu saklamaz ve yolları
"yordar/açıklar" değil **"bu model koşullarında birlikte değişir"** diliyle raporlar
[chapters/04_bulgular.qmd:783]. **Ders:** eşiği ver, kökenini belirt, çelişkiyi açıkla,
tek parlak indekse kanma.
