# RİTİM MÜHENDİSLİĞİ — burstiness'i öze dokunmadan üretmek

LLM nesrinin en güçlü imzası sözcük seçimi değil **tekdüzeliktir**: benzer uzunlukta
cümleler, benzer yapıda paragraflar, aynı bilgi sırası. İyi haber: ritim, metnin
*bilgi içeriğinden bağımsız* katmandır — burada özgürce çalışabilirsin.

---

## 1. Ölçüt ve hedefler

| Metrik | Ne ölçer | LLM tipiği | Hedef (`CONFIG`) |
| --- | --- | --- | --- |
| `cv` | cümle uzunluğu varyasyon katsayısı (SS/ort) | 0,25–0,35 | **≥ 0,40** |
| `burstiness_index` `B` | (σ−μ)/(σ+μ); −1 = tam düzenli | ≤ −0,55 | **≥ −0,45** |
| `short_ratio` | ≤10 sözcüklük cümle payı | ~0,03 | **≥ 0,10** |
| `long_ratio` | ≥28 sözcüklük cümle payı | ~0,05 | **≥ 0,10** |
| `max_uniform_run` | ort ±%20 bandında ardışık cümle | sınırı aşar | **≤ ⌈log₂ n⌉** (min 4) |
| `mattr` | 200 sözcüklük kayan pencerede tür/belirteç | düşük | **≥ 0,60** |
| `paragraph_len_cv` | paragraf uzunluğu değişkenliği | düşük | yükselt |

Bu eşikler **sezgiseldir**; bir dedektör skorunu taklit etmez. Amaç sayıyı tutturmak
değil, sayının işaret ettiği **tekdüzeliği** kırmaktır.

**Uzunluk yanlılığına dikkat:** ham `ttr` metin uzadıkça mekanik olarak düşer — bir
tez bölümünde TTR ≈ 0,30 normaldir. Eşik bu yüzden `mattr`'a bağlıdır; `ttr` yalnız
bilgi olarak raporlanır. Aynı nedenle tekdüze seri sınırı da cümle sayısıyla
logaritmik büyür ve raporda `tekdüze_seri=6/10` biçiminde **gözlenen/sınır** olarak
gösterilir.

---

## 2. Dört ritim hamlesi

### H1 — Tez cümlesi + analitik cümle (en etkili ikili)

Kısa ve iddialı bir cümle, ardından uzun ve koşullu bir cümle.

> Kardeşler bu tabloda görünmez değildir. Kardeş örnekleminde de duygusal sıcaklık
> ile depresyon puanı arasında anlamlı bir ilişki saptanmış, ancak bu ilişki indeks
> çocuklardakinden daha zayıf kalmıştır (r = 0,21; p = 0,014).

Neden işe yarar: 6 sözcük + 27 sözcük → tek hamlede `cv` sıçrar, `short_ratio` dolar.

### H2 — Zinciri kır

"…, ayrıca …, bunun yanı sıra …" zincirlerini iki-üç cümleye ayır. Her cümle tek
iş yapsın. Sayı ve koşulu **birlikte** taşı.

### H3 — Cılızları birleştir

Ardışık iki kısa bildirim cümlesini noktalı virgülle tek düşünceye bağla:

> "Ölçüm kesitseldir. Bu nedenle nedensellik çıkarılamaz."
> → "Ölçüm kesitseldir; bu nedenle nedensellik çıkarılamaz."

### H4 — Bilgi sırasını değiştir

Aynı bilgi, farklı giriş noktası:

- koşul-önce: "Yaş ve cinsiyet kontrol edildiğinde ilişki korunmuştur (β = 0,29)."
- bulgu-önce: "İlişki, yaş ve cinsiyet kontrol edildikten sonra da korunmuştur (β = 0,29)."
- karşıtlık-önce: "Kontrol grubunda tablo farklıdır: aynı ilişki anlamlı bulunmamıştır."

**Kural:** sıra değişir, bileşenler (sayı + koşul + yön) hiçbir zaman ayrılmaz.

---

## 3. Paragraf mimarisi

LLM paragrafı: *konu cümlesi → 3 benzer destek → özet.* Kırma yolları:

- **Açılışı değiştir:** paragrafı bulguyla, gerilimle veya karşıtlıkla başlat.
- **Kapanışı düşür:** paragrafların yaklaşık yarısında özet cümlesi olmasın.
- **Uzunluğu dalgalandır:** 6 cümlelik bir paragrafın ardına 2 cümlelik bir geçiş
  paragrafı. Aynı bölümde 4-5-4-5 cümlelik paragraf dizisi imzadır.
- **Bir paragraf = bir iş:** ikinci bir iş varsa böl; bölünce ritim de değişir.

---

## 4. Ritim şablonu (bir bulgu paragrafı için)

| Sıra | İşlev | Hedef uzunluk |
| --- | --- | --- |
| 1 | çıpa/iddia | 5–9 sözcük |
| 2 | ana bulgu + sayı + koşul | 25–40 sözcük |
| 3 | ikincil bulgu ya da karşıtlık | 12–18 sözcük |
| 4 | yorum / mekanizma (kaynakta varsa) | 20–30 sözcük |
| 5 | çekince (bağlandığı bulgunun yanında) | 10–20 sözcük |

Bu şablon **her paragrafta tekrarlanmaz** — tekrarlanırsa yeni bir tekdüzelik doğar.
Bölüm içinde en az iki farklı iskelet kullan.

---

## 5. Türkçe'ye özgü ritim araçları

- **Devrik cümle** ölçülü kullanılır; akademik Türkçede seyrek ama etkilidir. Yoğun
  kullanım register'ı bozar (Marmara sözleşmesi: pasif/nominal 3. tekil).
- **Noktalı virgül** iki bağımsız yargıyı bağlar → uzun cümle üretmenin en güvenli yolu.
- **İki nokta** karşıtlık/açıklama kurar: "Kontrol grubunda tablo farklıdır: …".
- **Ulaç/sıfat-fiil yığılmasından kaçın** ("-arak … -ip … -dıkça" zinciri) — hem
  okunurluğu hem de doğallığı düşürür.
- **Retorik soru ve eksiltili cümle kullanılmaz** (tez register'ı dışıdır).

---

## 6. Ritimle özü bozan üç tuzak

1. **Sayıyı koşulundan ayırmak.** Uzun cümleyi bölerken "yaş ve cinsiyet kontrol
   edildiğinde" öbeğini ayrı cümleye atarsan, sayı koşulsuz okunur = kapsam ihlali.
2. **Çekinceyi ayrı paragrafa sürüklemek.** Ritim adına yapılırsa bulgu çekincesiz
   okunur = öz ihlali.
3. **Kısa cümle üretmek için yüklem zayıflatmak.** "…saptanmıştır" → "…vardır"
   kipsel bilgiyi düşürür.

---

## 7. Ölçüm döngüsü

```bash
# yeniden yazmadan önce teşhis
python3 scripts/eval/humanize_invariant_guard.py metrics /tmp/kaynak.md

# yazdıktan sonra: öz + ritim birlikte
python3 scripts/eval/humanize_invariant_guard.py all \
  --source /tmp/kaynak.md --candidate /tmp/aday.md
```

`sentence_lengths` dizisini (JSON çıktısında) gözle tara: `[14, 15, 14, 16, 15]`
düzenidir; `[6, 31, 14, 27, 9]` insan ritmidir.
