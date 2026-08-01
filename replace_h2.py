import sys

file_path = "chapters/04_bulgular.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_text = """### H2 — Kardeş İlişkisi (KİA / SRQ)

**Bulgu özeti.** Kardeş ilişkisinin dört boyutunda — yakınlık, güç, çatışma
ve rekabet — Tip 1 diyabetli aileler ile kontrol aileleri arasında anlamlı fark
için kanıt bulunmamıştır. Bu, farkın *olmadığının* kanıtı değildir; yalnızca mevcut
örneklemde bir farkın gösterilememesidir. Klinik okumada, diyabet tanısının
kardeşler arasındaki ilişki örüntüsünü belirgin biçimde değiştirdiğine dair bir
işaret elde edilmemiştir.

*Kanıt* — Kardeş İlişkileri Anketi'nin (KİA / SRQ) dört alt ölçeği üç paralel
stratejiyle incelenmiştir. Her ailenin iki kardeşinin ortalaması alınarak yürütülen
aile-ortalama Welch testlerinde (241 aile) dört alt ölçeğin tamamında gruplar arası
fark küçüktür; etki büyüklüğü d < 0,20 düzeyindedir. İki kardeşin karşılıklı etkisini
modelleyen aktör-partner karşılıklı bağımlılık modelinde (APIM) grup, rol ve grup ×
rol etkilerinin hiçbiri anlamlı değildir (FDR-düzeltilmiş p > 0,350). İki kardeşin
yanıtlarını latent düzeyde ilişkilendiren Olsen-Kenny düad modeli kavga-temelli madde
setinde uyum sağlamış; indeks çocuk ile kardeşin bu boyuttaki latent korelasyonu
r = 0,27'dir. Kardeşlerin cinsiyet ve yaş farkına göre moderasyon anlamlı değildir.
Farkın yokluğunu doğrudan sınayan eşdeğerlik testi (TOST) ön-kayıtlı planda yer
almadığından uygulanmamıştır; bu nedenle dört alt ölçek için bulgu "fark yoktur"
değil, "farkın varlığına ilişkin kanıt yetersizdir" biçiminde raporlanmıştır
[@lakens2017equivalence]. Aile-ortalama testleri @tbl-apa-h2-family-mean, APIM sabit
etkileri @tbl-apa-h2-apim, APIM aktör ve partner yolları @fig-h2-apim-path içinde
sunulmuştur.

```{r}
#| label: tbl-apa-h2-family-mean
#| tbl-cap: "H2 aile-ortalama Welch testleri: kardeş ilişkisinin dört boyutunda (yakınlık, güç, çatışma, rekabet) DM ve kontrol aileleri, her ailenin iki kardeşinin ortalaması alınarak (241 aile) karşılaştırılır. Sütunlar grup değerlerini, Welch t sınamasını ve etki büyüklüğünü (Cohen d) verir. Okuma anahtarı: her boyutta grup farkının sıfırdan ayırt edilip edilmediğine ve d'nin büyüklüğüne bakılır; Cohen geleneğinde 0,20'nin altı 'küçük'ün altı olarak yorumlanır."
apa_render_table("t08_h2_family_mean")
```

```{r}
#| label: tbl-apa-h2-apim
#| tbl-cap: "H2 aktör-partner karşılıklı bağımlılık modelinin (APIM) sabit etkileri: iki kardeşin ilişki algısı birbirinden bağımsız olmadığından, model 'kendi algımın kendi çıktımı belirlemesi' (aktör) ile 'kardeşimin algısının benim çıktımı belirlemesi' (partner) etkilerini ayırır ve grup farkını bu yapı içinde sınar. Sütunlar grup, rol ve grup × rol sabit etkilerini katsayı ve %95 güven aralığıyla verir. Okuma anahtarı: bir etkinin güven aralığı sıfırı içeriyorsa o etki sıfırdan ayırt edilemez; aktör ve partner ayrımı kardeşler-arası karşılıklı bağımlılığın kaynağını gösterir."
apa_render_table("t09_h2_apim")
```

![H2 aktör-partner karşılıklı bağımlılık modeli (APIM) yol diyagramı: kardeş ilişkisinin bir boyutunda indeks çocuk ile sağlıklı kardeşin Kardeş İlişkileri Anketi (KİA / SRQ) yanıtları arasındaki karşılıklı etki gösterilir. Düğümler iki kardeşin yanıtlarını; düz oklar aktör (kendi algı → kendi çıktı) ve partner (kardeşin algısı → kendi çıktı) etkilerini; çift yönlü eğri ise yön iddiası taşımayan kovaryansı temsil eder. Okuma anahtarı: hangi okun aktör hangisinin partner olduğu ayırt edilir, ardından katsayının işaret ve büyüklüğüne bakılır; çift yönlü eğri bir etki değil birlikte-değişimdir.](docs/assets/figures/carbon/primary/fig-09-h2-apim-path.svg){#fig-h2-apim-path width="96%" fig-align="center"}"""

new_text = """### H2 — Kardeş İlişkisi (KİA / SRQ)

**Bulgu özeti.** Kardeşler arasındaki ilişkinin dört temel alanında — yakınlık, güç/baskınlık, çatışma ve rekabet — diyabetli aileler ile sağlıklı kontrol aileleri arasında anlamlı bir fark bulunamamıştır. İstatistiksel olarak bu durum, grupların birbirinin "tıpatıp aynısı" olduğu (farkın sıfır olduğu) anlamına gelmese de, elimizdeki verilerle gruplar arasında bir fark tespit edilememiştir. Klinik açıdan yorumlandığında, diyabet tanısının evdeki kardeşler arasındaki ilişki dinamiğini belirgin şekilde değiştirmediği görülmektedir.

*Kanıt* — Çocuklara uygulanan Kardeş İlişkileri Anketi'nin (KİA / SRQ) sonuçları üç farklı yöntemle incelenmiştir. Öncelikle her evdeki iki kardeşin anket puanlarının ortalaması alınarak aile düzeyinde bir değerlendirme yapılmıştır (241 aile üzerinden). Bu analizde gruplar arasındaki fark, istatistiksel açıdan "çok küçük" (etki büyüklüğü d < 0,20) kalmıştır.

İkinci olarak, evdeki bir çocuğun kardeş algısının diğer çocuğu da etkileyeceği gerçeğinden yola çıkılarak kardeşlerin birbirlerine olan etkileri hesaplanmış (karşılıklı bağımlılık modeli) ve burada da gruplar veya çocukların rolü (hasta ya da sağlıklı olması) açısından bir fark bulunamamıştır (p > 0,350). Son olarak, kardeşlerin kavga/çatışma davranışları gizli (latent) bağlarla incelendiğinde kardeşler arası ilişkinin r = 0,27 düzeyinde olduğu bulunmuş; bu ilişkinin çocukların cinsiyetine ya da aralarındaki yaş farkına göre değişmediği anlaşılmıştır. 

Farkın "hiç olmadığını" doğrudan kanıtlayan özel bir istatistiksel yöntem (eşdeğerlik testi - TOST), araştırmanın başında planlanmadığı için sonradan kullanılmamış, bu sebeple sonuç bilimsel bir dille "fark yoktur" şeklinde değil "farkın varlığına dair yeterli kanıt yoktur" şeklinde ifade edilmiştir [@lakens2017equivalence]. Aile ortalamaları ile yapılan testlerin sonuçları @tbl-apa-h2-family-mean içinde, kardeşlerin birbirini nasıl etkilediğinin (aktör/partner modeli) sayısal verileri @tbl-apa-h2-apim içinde ve bunun görsel haritası ise @fig-h2-apim-path içinde sunulmuştur.

```{r}
#| label: tbl-apa-h2-family-mean
#| tbl-cap: "H2 kardeş ilişkisi aile ortalamaları tablosu: Kardeş ilişkisinin dört boyutunda (yakınlık, güç, çatışma, rekabet), her ailedeki iki kardeşin puanlarının ortalaması alınarak diyabetli aileler ile kontrol aileleri (toplam 241 aile) karşılaştırılmıştır. Tabloda grupların değerleri, yapılan istatistiksel testin (Welch t) sonucu ve ortaya çıkan farkın büyüklüğü (Cohen d) verilmiştir. Okuma anahtarı: Farkın büyüklüğünü gösteren 'd' değerinin 0,20'nin altında olması, var olan farkın pratikte 'çok küçük / önemsiz' kabul edildiğini gösterir."
apa_render_table("t08_h2_family_mean")
```

```{r}
#| label: tbl-apa-h2-apim
#| tbl-cap: "H2 kardeşlerin karşılıklı etkileşim modeli (APIM): Evdeki iki kardeşin ilişki algısı birbirinden bağımsız değildir. Bu model, 'benim düşüncem kendi sonucumu nasıl etkiliyor' (aktör etkisi) ile 'kardeşimin düşüncesi benim sonucumu nasıl etkiliyor' (partner etkisi) durumlarını birbirinden ayırarak inceler. Tabloda diyabet/kontrol grubu, çocuğun hasta/sağlıklı rolü ve bunların birbirleriyle olan etkileşimine dair güven aralıkları verilir. Okuma anahtarı: Bir değerin %95 güven aralığı sıfırı kapsıyorsa, bu o sonucun istatistiksel olarak sıfırdan ayırt edilemeyeceği, yani anlamlı bir etki olmadığı anlamına gelir."
apa_render_table("t09_h2_apim")
```

![H2 kardeş etkileşimi (APIM) yol haritası: Kardeş İlişkileri Anketi'ne (KİA / SRQ) verilen yanıtlarda, diyabetli çocuk ile sağlıklı kardeşin birbirini nasıl etkilediğini gösteren diyagramdır. Düz oklar kişinin kendi düşüncesinin kendisini (aktör) veya kardeşinin düşüncesinin kendisini (partner) nasıl etkilediğini gösterir. Çift yönlü kavisli çizgiler ise bir etki veya neden-sonuç değil, iki durumun birlikte nasıl hareket ettiğini (korelasyonunu) temsil eder.](docs/assets/figures/carbon/primary/fig-09-h2-apim-path.svg){#fig-h2-apim-path width="96%" fig-align="center"}"""

if old_text in content:
    content = content.replace(old_text, new_text)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replace successful!")
else:
    print("Text not found in the file. Check for exact match.")
