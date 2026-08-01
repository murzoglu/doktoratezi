# LLM İMZA KALIPLARI — Türkçe akademik nesirde "makine kokusu" haritası

Amaç: kalıbı **tanı**, kaldır ya da anlamla değiştir. Kural: **klişenin karşılığı çoğu
zaman boşluktur, eşanlamlı değil.** Sözcük değiştirerek perplexity avlamak metni
"kelime salatasına" çevirir; hakem bunu dedektörden önce fark eder.

---

## 1. Boş geçiş kalıpları — SİL (yerine sözcük koyma)

| Kalıp | Doğru hamle |
| --- | --- |
| "Bu bağlamda, …" / "Bu doğrultuda, …" / "Bu çerçevede, …" | **Sil.** Cümle zaten bağlamın içinde. |
| "Genel olarak değerlendirildiğinde, …" | **Sil** veya asıl yargıyı öne al. |
| "Özetle ifade etmek gerekirse, …" | **Sil**; özet cümlesi zaten özet. |
| "Sonuç olarak ifade edilebilir ki …" | Doğrudan yargıyı yaz: "Bulgular X'e işaret etmektedir." |
| "Unutulmamalıdır ki …" / "Göz ardı edilmemelidir ki …" | **Sil**; ardındaki cümle zaten uyarı. |
| "Vurgulanması gereken bir diğer nokta ise …" | **Sil**; noktayı vurgulamak yerine söyle. |

**Ölçüt:** cümleyi kalıpsız okuduğunda anlam kaybı var mı? Yoksa kalıp fazlalıktır.

---

## 2. Şişirme sıfat/yüklem kalıpları — DARALT

| Kalıp | Sorun | Hamle |
| --- | --- | --- |
| "kapsamlı bir şekilde incelenmiştir" | "kapsamlı" ölçülemez ve genelde yanlış | "incelenmiştir" · ya da neyin incelendiğini söyle |
| "önem arz etmektedir" / "büyük önem taşımaktadır" | değersiz vurgu | **neden** önemli olduğunu tek yan cümlede söyle |
| "kritik bir rol oynamaktadır" | mekanizmayı gizler | "…'yi yordamaktadır" gibi ölçülebilir ifade (**yalnız kaynakta varsa**) |
| "dinamik/çok boyutlu bir yapı" | içi boş | somut boyutları say (**yalnız kaynakta varsa**) |
| "derinlemesine bir anlayış sunmaktadır" | öz-övgü | ne öğrendiğimizi söyle |
| "ışık tutmaktadır" / "kapı aralamaktadır" | metafor enflasyonu | düz yüklem |

> **Dikkat:** daraltma sırasında bir *bilgi* eklenemez. "Neden önemli" cevabı metinde
> yoksa cümleyi kısalt, uydurma.

---

## 3. Şablon retorik figürleri — KIR

- **Tricolon / ikili paralellik:** "yalnızca X değil, aynı zamanda Y", "hem A hem de B
  açısından" — LLM'in en sevdiği iki kalıptır. Birini bırak, kalanını düz cümleye çevir.
- **Üçlü sıralama tutkusu:** her listeyi üç öğeye tamamlama eğilimi. Kaynakta iki öğe
  varsa iki kalır; üçüncüyü **uydurma**.
- **Karşıtlık şablonu:** "Bir yandan …, diğer yandan …" ardışık paragraflarda
  tekrarlanıyorsa birini kaldır.
- **Kapanış refleksi:** her paragrafı özetleyen son cümle. Paragrafların yarısında
  kaldır; okur özeti zaten taşıyor.

---

## 4. Cümle başı bağlaç bağımlılığı — ORANI DÜŞÜR

`connective_start_ratio > 0,25` ise metin bağlaçla yürüyor demektir:
"Ayrıca / Bununla birlikte / Buna ek olarak / Öte yandan / Dolayısıyla / Bu nedenle /
Böylece / Nitekim / İlk olarak / Son olarak".

Hamle sırası:

1. **Bağı anlamla kur:** "Ayrıca kardeşlerde de benzer örüntü görülmüştür." →
   "Benzer örüntü kardeş örnekleminde de yinelenmiştir."
2. Gerçekten karşıtlık varsa bağlacı **cümle içine** al: "Kardeş örnekleminde ise …".
3. Bağlaç yalnız mantık gerçekten dönüyorsa cümle başında kalsın.

---

## 5. Ölçü birimi olmayan nicelik dili — SAKIN DÜZELTME

"Önemli ölçüde", "büyük oranda", "kayda değer biçimde" gibi ifadeler LLM imzasıdır
**ama** bunlar çoğu kez bir istatistiksel iddiaya bağlıdır. Kaldırmadan önce sor:
bu ifade bir etki büyüklüğünü mü niteliyor? Niteliyorsa **dokunma** — anlamlılık/
büyüklük dili özün parçasıdır. Yalnız süsleme ise sil.

---

## 6. ASLA DEĞİŞTİRİLMEYECEK sözcükler (eşanlamlı yasağı)

| Kategori | Örnek | Neden |
| --- | --- | --- |
| Kanonik terim sözlüğü | `docs/tez-kilavuz/terim-sozlugu.yaml` girdileri (ör. "ortanca") | `terim_tutarlilik_audit.py` HARD |
| İstatistik terimi | anlamlı, korelasyon, regresyon, etki büyüklüğü, güven aralığı, yordama | teknik tanım |
| Ölçek/alt ölçek adı | EMBU, Beck Depresyon Envanteri, KİA, "duygusal sıcaklık" | ölçüm kimliği |
| Tanı/klinik terim | Tip 1 diyabet, HbA1c, ketoasidoz | tıbbi kesinlik |
| Değişken/grup adı | DM grubu, kontrol grubu, indeks çocuk, kardeş | analiz kimliği |
| Yöntem adı | IPTW, WLSMV, çok düzeyli model, APIM | yöntem kimliği |
| Rol adı | anne, ebeveyn, bakım veren, eş | **kayma tuzağı**: "eş" ↔ "partner" ↔ "ebeveyn" farklı kümelerdir |

Kural: **terminoloji sabit, sözdizimi serbest.** Perplexity artışı cümle kurgusundan
gelir; terim oynatmaktan değil.

---

## 7. Kesinlikle yapılmayacaklar

- Bağlam gözetmeyen otomatik eşanlamlı/parafraz motoru çıktısını metne koymak.
- Görünmez karakter, homoglif (Latin/Kiril karışımı), sıfır-genişlik boşluk, gizli
  yazı tipi hilesi eklemek → bu **metin manipülasyonudur**, üslup düzeltmesi değil.
- Nadir/arkaik sözcük serpiştirerek "yapay perplexity" üretmek → hakem kaybı.
- Yapay zeka kullanım beyanını silmek/örtmek.
- Kaynakta olmayan örnek, veri, tarih, kurum, kişi eklemek.

---

## 8. Kalıp yoğunluğunu ölçme

```bash
python3 scripts/eval/humanize_invariant_guard.py metrics /tmp/aday.md
# cliche_hits + cliche_list → hangi kalıp, kaç kez
```

Hedef: `cliche_per_1000 ≤ 2,0`. Sıfır zorunlu değildir — bir akademik metinde birkaç
geçiş ifadesi doğaldır; **yoğunluk** imzadır, tek kullanım değil.
