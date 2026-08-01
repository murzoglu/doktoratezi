# Referans-kalite örnek — SMD/IPTW denge pasajı (F1–F5 uyumlu)

Kaynak: `chapters/04_bulgular.qmd` (örneklem/denge paragrafı). Yeni işten önce **üslup
kalibrasyonu** için oku: neyin korunduğunu, neyin çevrildiğini, neyin ASLA eklenmediğini gör.

## Öncesi (orijinal — jargon yoğun)

> İki grubun bir değişkende ne kadar farklılaştığını görmek için standardize ortalama fark
> (SMD) kullanılmıştır … Nedensel yönlü asiklik graf temelli birincil ayarlama seti (latent
> SES, kardeş yaş farkı, aile çocuk sayısı) ham gözlemde maksimum |SMD| = 0,220 (kardeş yaş
> farkı) düzeyindeyken, stabilize ters-olasılık ağırlıklandırması (IPTW) sonrası kalan maksimum
> |SMD| = 0,004 (latent SES) düzeyine inmiştir; yani analizlerde dikkate alınan bu değişkenlerin
> hiçbirinde … kayda değer bir grup farkı kalmamıştır.

## Sonrası (klinisyen diline uyarlanmış — kabul edilebilir taslak)

> İki grubun bir özellikte ne kadar ayrıştığı, standardize ortalama fark (iki grup ortalaması
> arasındaki farkın ortak bir cetvele vurulmuş hâli; SMD) ile ölçülmüştür; değer sıfıra
> yaklaştıkça gruplar o özellikte birbirine benzer demektir [@austin2009balanceDiagnostics].
> … Hangi değişkenler için düzeltme yapılacağı, değişkenler arası neden–sonuç yönlerini gösteren
> bir şemayla (yönlü asiklik graf) belirlenmiş; birincil ayarlama seti latent SES, kardeş yaş
> farkı ve aile çocuk sayısından oluşmuştur. Ham gözlemde bu değişkenlerdeki en büyük dengesizlik
> |SMD| = 0,220 (kardeş yaş farkı) iken, her aileye grup dengesini kuran bir ağırlık verilerek
> (stabilize ters-olasılık ağırlıklandırması; gözlemsel veride "sanki denk dağıtılmış gibi"
> karşılaştırma sağlar; IPTW) uygulandıktan sonra kalan en büyük dengesizlik |SMD| = 0,004
> (latent SES) düzeyine inmiştir; yani analizlerde dikkate alınan bu değişkenlerin hiçbirinde
> ağırlıklandırma sonrası kayda değer bir grup farkı kalmamıştır.

## Neden kabul edilebilir (Adım 2 kontrolü)
- **Sayı/token/atıf birebir:** 0,220 → 0,004, `[@austin2009balanceDiagnostics]` korunmuş. ✔
- **F1 yok:** "analizlerde dikkate alınan bu değişkenlerin hiçbirinde" kapsamı korunmuş;
  "eşitlendi/tamamen/tüm özelliklerde" YOK. ✔
- **F2 yok:** eklenen tek şey terim glossları (SMD, DAG, IPTW klinik karşılığı) — yeni
  gerekçe/nedensellik iddiası YOK. ✔
- **F3 yok:** "ölçülmüştür / belirlenmiş / inmiştir" — pasif 3. tekil. ✔
- **F4 yok:** "medyan" gibi mevcut terimler korunur (bu blokta yok ama kural geçerli). ✔
- **Amaç:** jargon (SMD/DAG/IPTW) klinik karşılıkla açılmış, cümleler bölünmüş, akış klinisyen
  için izlenebilir. ✔

## Karşı-örnek — BU taslak reddedilir (Gemini üretirse Adım 2 yakalar)
- ✗ "…ağırlıklandırma sonrası **iki grup tüm özellikler bakımından pratikte eşitlendi**." → F1
  (kapsam genişletme + abartı; kaynak yalnız *ayarlama-seti* değişkenlerini söylüyor).
- ✗ "Baştaki farklar, **sonuçların hastalığa mı yoksa sosyoekonomik farka mı bağlı olduğunu
  belirsizleştirir**." → F2 (kaynakta olmayan nedensel-çıkarım gerekçesi).
- ✗ "…dengeyi kurmak için **her aileye ağırlık verdik**." → F3 (1. şahıs).
- ✗ "**ortanca** … " (kaynak "medyan") → F4 (terim kayması).
