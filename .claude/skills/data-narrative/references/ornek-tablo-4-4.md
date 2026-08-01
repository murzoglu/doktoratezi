# Örnek: Referans-Kalite Açıklama (Tablo 4.4)

Bu, `data-narrative` skill'inin ürettiği altın-standart bir açıklamadır. Yeni bir
açıklama yazmadan önce **ton/üslup/akış kalibrasyonu** için oku. 5-katman akışının
görünmez biçimde nasıl işlediğine, sayıların kanıt olarak nasıl kullanıldığına ve
tek-cümle kapanışa dikkat et.

Kaynak öğe: `chapters/04_bulgular.qmd:552` (`tbl-apa-propensity-model`), üreten
`R/15_propensity_score.R` + `R/29_apa_tables.R`. Numara→etiket: 04_bulgular'daki
`#| label: tbl-` sırasında 4. tablo.

---

# Tablo 4.4'ü Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.4 = Eğilim Skoru Modeli ve Ortak Destek**

## Önce: Bu tablo hangi soruna çözüm?  ← [Katman 1: Neden var?]

Çalışmamız bir **deney değil, gözlemsel** çalışma. Yani diyabetli ve kontrol
ailelerini biz rastgele atamadık — onlar zaten öyleydiler. Bu bir tuzak yaratır:

> İki grup, diyabet dışında da **başka açılardan** farklı olabilir (gelir, aile
> büyüklüğü, kardeş yaş farkı). O zaman bulduğumuz fark diyabetten mi, yoksa bu
> diğer farklardan mı kaynaklanıyor? Bilemeyiz.

Buna **karıştırıcı (confounder)** sorunu denir.

## Çözümün mantığı: "Sanki rastgele atanmış gibi" yapmak  ← [Katman 2: Somutlaştır]

Rastgele atama yapamadığımız için, istatistikle taklit ediyoruz. Üç aşama:

### 1. Eğilim skoru nedir?  ← [Katman 3: Mekanizma, kademeli]
Her aile için tek bir sayı: **"Bu ailenin diyabet grubunda olma olasılığı, arka
plan özelliklerine bakarak ne?"** Bunu bir **lojistik regresyon** ile yapıyoruz.
Girdiler (DAG'dan): latent SES, kardeş yaş farkı, aile çocuk sayısı. Tablonun üst
kısmı bu modelin katsayılarıdır (OR, %95 GA).

### 2. Ağırlıklandırma (IPTW)
Skoru kullanarak aileleri yeniden ağırlıklandırıyoruz — iki grubu arka plan
açısından birbirinin dengi hale getiriyoruz. Orta kısım ağırlık özetidir.

### 3. Ortak destek (common support)
İki grubun eğilim skorlarının **çakıştığı** aralık. Alt kısım bunu özetler.

## Tablo işe yaradı mı? — Kanıt  ← [Katman 4: Gerçek sayılarla]

| Aşama | En büyük grup farkı (\|SMD\|) | Yorum |
|---|---|---|
| **Ham veri** | **0,220** (kardeş yaş farkı) | Kayda değer dengesizlik ⚠️ |
| **IPTW sonrası** | **0,004** (latent SES) | Neredeyse sıfır ✓ |

**0,220 → 0,004.** Ağırlıklandırmadan önce gruplar arka planda farklıydı; sonra
fark **pratik olarak yok oldu**. Karşılaştırma "elmayla elma" oldu.

## Bir cümleyle  ← [Katman 5: Tek-cümle kapanış]

> Tablo 4.4, diyabetli ve kontrol ailelerini arka plan özellikleri açısından
> **istatistiksel olarak eşitleyen** modeli ve bu eşitlemenin **başarılı olduğunu**
> (kalan fark ≈ 0) belgeler — böylece sonraki bulgular "gerçekten diyabetin etkisi"
> olarak yorumlanabilir.

← [Kapanış teklifi: komşu tabloları (4.2 denge, 4.5 SES) açma önerisi]

---

## Bu örnekten çıkarılacak üslup dersleri

1. **Katman etiketleri görünmez.** Yukarıda `← [Katman N]` yalnız bu öğretici
   dosyada var; gerçek çıktıda okur akışı hisseder, iskeleti görmez.
2. **Motivasyon her şeyden önce.** İlk paragraf teknik terim değil, "tuzak" anlatır.
3. **Jargon daima parantezli.** confounder, IPTW, ortak destek, |SMD| — hepsi ilk
   geçişte günlük karşılığıyla.
4. **Sayı = kanıt.** 0,220→0,004 kıyası açıklamanın kalbidir; "yorum" sütunu şart.
5. **Tek-cümle kapanış** okurun tek başına okuyabileceği damıtımdır.
6. **Ölçek uyumu.** Bu karmaşık bir tablo olduğu için 5 katman da açıldı; basit bir
   öğede (ör. tek bir α değeri) 2-3 katman yeterdi.
