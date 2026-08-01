# Şekil 4.1–4.5 — Detaylı İzahat (Ders Anlatır Gibi)

Bu belge, Bulgular bölümünün ilk beş şeklini `data-narrative` skill'iyle, teknik
doğruluğundan ödün vermeden, uzmanı olmayan zeki bir okurun anlayacağı netlikte açıklar.
Her sayı kaynağından birebir teyit edilmiştir; kaynak dosya:satır her başlıkta verilir.
Numara→etiket eşlemesi: 04_bulgular bölümündeki `#| label: fig-` / `{#fig-` sırası.

| Numara | Kanonik etiket | Kaynak (caption) | Öğe ailesi |
|---|---|---|---|
| Şekil 4.1 | `@fig-strobe-flow` | chapters/04_bulgular.qmd:563 | Akış diyagramı |
| Şekil 4.2 | `@fig-causal-dag` | chapters/04_bulgular.qmd:565 | Nedensel DAG |
| Şekil 4.3 | `@fig-smd-love` | chapters/04_bulgular.qmd:567 | Love / SMD denge |
| Şekil 4.4 | `@fig-propensity-overlap` | chapters/04_bulgular.qmd:569 | Eğilim örtüşme (yoğunluk) |
| Şekil 4.5 | `@fig-ses-correlation` | chapters/04_bulgular.qmd:571 | Korelasyon ısı haritası |

---

# Şekil 4.1'i Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.1 = Analitik örneklem akış diyagramı**
Kanonik etiket: `@fig-strobe-flow` · Kaynak: chapters/04_bulgular.qmd:563 (caption) +
:466-475, :507 (gövde metni) · Aile: akış diyagramı.

## Bu diyagram hangi soruna çözüm?

Bir çalışmanın ilk güven sınavı sonuçlarından önce gelir: **analize kim girdi, kim
düştü, neden?** Kaç kişiyle başlanıp kaç kişiyle bitirildiği görünmüyorsa, sonraki
bütün sayılar havada kalır. Akış diyagramı bu soruyu bir **eleme zinciri** olarak
görünür kılar.

Bir akış diyagramını okumanın hamlesi hep aynıdır: **kutulardan aşağı in ve her okta
"nerede, neden, kaç birim düştü?" diye sor.** Bu, çalışmanın seçilim yapısının somut
karşılığıdır.

## Zincir nasıl işliyor?

Manzarayı bir huni gibi düşünün; her kademe bir öncekinden türer:

1. **Kilitlenmiş kanonik veri tabanı** → analiz için dondurulmuş kaynak.
2. **Aile düzeyi analiz tabanı:** çalışmaya **241 aile** dâhil edilmiştir — **120
   diyabet (DM)** ailesi ve **121 kontrol** ailesi [chapters/04_bulgular.qmd:466].
3. **Çocuk düzeyi taban:** her aileden bir indeks çocuk + bir kardeş; toplam **482 çocuk
   satırı** (241 × 2) ve dört rol hücresi (DM-indeks, DM-kardeş, kontrol-indeks,
   kontrol-kardeş) dengelidir [:468].

## Diyagram ne söyledi? — Dürüst bilanço

| Aşama | n | Not |
|---|---|---|
| Aile analiz tabanı | 241 (120 DM + 121 kontrol) | çekirdek örneklem ✓ |
| Çocuk satırı | 482 | 4 rol hücresi dengeli ✓ |

En kritik nokta dürüstçe raporlanır ve **gizlenmez:** tarama aşamasında kaç ailenin
davet edildiği ve kaçının reddettiği "kanonik analiz kilidinde izlenebilir olmadığından",
diyagram yalnız **doğrulanabilir analiz-seti akışını** gösterir; tarama-öncesi akış bir
**raporlama sınırlılığı** olarak belirtilir [:472-475].

**Yanlış okumayı önceden düzeltelim.** Bu diyagram bir **katılım/yanıt oranı** ya da
**temsiliyet** kanıtı değildir — klasik bir STROBE akışının başındaki "taranan → uygun →
katılan" basamakları burada eksiktir. Diyagram "elimizdeki analiz setine nasıl
ulaşıldığını" gösterir, "örneklemin evreni ne kadar temsil ettiğini" değil.

## Bir cümleyle

> Şekil 4.1, 241 aileden (120 DM + 121 kontrol) 482 çocuk satırına uzanan **doğrulanabilir analiz-seti akışını** belgeler; ancak
> tarama-öncesi akış kanonik kilitte izlenemediğinden, bu bir katılım-oranı/temsiliyet
> kanıtı değil, dürüstçe sınırı belirtilmiş bir analiz-seti haritasıdır.

*Komşu öğe:* eksik veri örüntüsü `@fig-missing-pattern` (Şekil 4.6) aynı biçimde açılabilir.

---

# Şekil 4.2'yi Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.2 = Nedensel yönlü asiklik graf (DAG) ve ayarlama stratejisi**
Kanonik etiket: `@fig-causal-dag` · Kaynak: chapters/04_bulgular.qmd:565 (caption) +
chapters/03_gerec_ve_yontem.qmd:139 (yöntem) · Aile: nedensel DAG.

## Bu diyagram hangi soruna çözüm?

Bu bir **deney değil, gözlemsel** çalışma; grupları biz rastgele atamadık. O hâlde
bulduğumuz fark diyabetten mi, yoksa grupların arka plan farklarından mı? DAG (yönlü
asiklik graf) bu ayrımı yapabilmek için önce **varsayımları görünür kılan bir haritadır**:

> Her düğüm bir değişken, her **ok** "şu şunu etkiler" **varsayımıdır** — veriden
> kestirilmez, analizden önce çizilir. Bir okun **yokluğu** da güçlü bir varsayımdır.

Bir DAG'ı okumanın değişmez hamlesi: hangi düğüm **karıştırıcı** (kapatılacak), hangisi
**aracı** (bilerek açık bırakılacak), hangisi **seçilim** düğümü — ve bu tasarımda etki
**tanımlanabilir mi**?

## "Arka kapıları" kapatmak

A'dan (T1DM) B'ye (çocuk algısı) giden ana yol "diyabetin etkisi"dir; ama ortak bir neden
üzerinden uzanan **arka-kapı yolları** da A ile B'yi bağlar. Temiz karşılaştırma için bu
kapıları (ortak nedenleri istatistikle sabitleyerek) kapatmak gerekir; DAG **hangilerini**
söyler. Düğümler üç işe ayrılır:

1. **Karıştırıcılar (kapatılacak):** latent SES, kardeş yaş farkı, aile çocuk sayısı —
   hem T1DM'ye hem çocuk algısı/kardeş ilişkisi çıktısına ok gönderir; birincil modelde
   ayarlanır (ve eğilim skoru bunlar üzerinden kestirilir) [caption :565].
2. **Aracı/duyarlılık (bilerek açık):** Beck (anne depresif belirti) ve antidepresan
   kullanımı maruziyet ile ebeveynlik *arasında* durur; aracıyı ana modele koymak ölçmek
   istediğin etkinin bir parçasını görünmez kılar — bu yüzden ayrı aracılık/duyarlılık
   çözümlemesine bırakılır.
3. **Seçilim düğümü $S$:** merkez ve takvim dönemi ile grup üyeliği birlikte kimin
   örnekleme *girdiğini* belirler; analiz $S=1$'e koşulludur (kesikli gösterilir). Grup
   üyeliği merkez/dönemi nedensel olarak oluşturmaz.

## Diyagram ne söyledi? — Dürüst bilanço

En kritik satır gizlenmez: seçilim yapısı ($S$) üzerinde koşullandığımız için **T1DM'nin
toplam nedensel etkisi bu tasarımda tanımlanamaz** (nokta-tanımlanamaz = nedensel etkinin
tek bir sayısal değeri veriden benzersiz biçimde geri kazanılamaz) [caption :565]. Bu
yüzden raporlanan grup katsayıları "diyabetin nedensel etkisi" değil, **gözlenen
karıştırıcılar için ayarlanmış koşullu ilişkiler** olarak okunur.

**Yanlış okumayı önceden düzeltelim.** DAG'ı bir "veri sonucu" sanma; bir varsayım
haritasıdır. Bir DAG'ın "işe yaraması", her zaman temiz bir etki üretmesi değil, çoğu
zaman **hangi etkinin üretilemeyeceğini** dürüstçe göstermesidir — bu diyagramın esas
katkısı budur.

## Bir cümleyle

> Şekil 4.2, hangi karıştırıcıların kapatıldığını (SES, kardeş yaş farkı, aile çocuk
> sayısı) ve hangilerinin bilerek aracı bırakıldığını (Beck, antidepresan) görünür kılan
> varsayım haritasıdır; ama aynı harita, seçilim düğümü $S$ üzerinde koşullanma nedeniyle
> **T1DM'nin toplam nedensel etkisinin tanımlanamayacağını** belgeler — dolayısıyla grup
> katsayıları "nedensel etki" değil "ayarlanmış koşullu ilişki" olarak okunmalıdır.

*Komşu öğeler:* `@fig-smd-love` (denge kazanımı) ve `@fig-propensity-overlap` (ortak
destek) bu haritanın doğrudan çıktısıdır — aşağıda.

---

# Şekil 4.3'ü Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.3 = Kovaryat denge kazanımı (Love grafiği)**
Kanonik etiket: `@fig-smd-love` · Kaynak: chapters/04_bulgular.qmd:567 (caption) +
:497-501 (gövde) · Aile: Love / SMD denge grafiği.

## Bu grafik hangi soruna çözüm?

Şekil 4.2 hangi arka-kapı karıştırıcılarını kapatmamız gerektiğini söyledi. Peki
**kapatma işlemi gerçekten işe yaradı mı?** İki grubu istatistikle dengelediğimizi
*iddia* etmek yetmez; bunu görsel olarak **kanıtlamak** gerekir. Love grafiği tam bu
kanıttır.

Bir Love grafiğini okumanın hamlesi tektir: **her kovaryat için noktalar
ağırlıklandırmadan *sonra* sıfıra yaklaştı mı?** Öncesi/sonrası kıyası bu grafiğin bütün
mesajıdır.

## Grafik nasıl kurulu?

- Her **satır** birincil ayarlama setindeki bir değişken (latent SES, kardeş yaş farkı,
  aile çocuk sayısı).
- **x ekseni** = mutlak standardize ortalama fark |SMD| — "iki grup bu değişkende ne
  kadar farklı"nın ölçeksiz ölçüsü; sıfıra yakınlık = denge.
- **Renk** = aşama: ağırlık öncesi / IPTW sonrası / eşleştirme sonrası.
- **Kesikli çizgiler** = 0,10 ve 0,25 denge eşikleri.

Eşik okuryazarlığı (Austin 2009/2011; **gelenek, yasa değil**): |SMD| < 0,10 ihmal
edilebilir; 0,10–0,25 sınırda; > 0,25 kayda değer dengesizlik [chapters/04_bulgular.qmd:483].

## İşe yaradı mı? — Kanıt

| Aşama | En büyük grup farkı (\|SMD\|) | Yorum |
|---|---|---|
| **Ham veri** | **0,220** (kardeş yaş farkı) | 0,10 eşiğinin üstünde, ayarlama gerek ⚠️ |
| **IPTW sonrası** | **0,004** (latent SES) | neredeyse sıfır ✓ |

Değerler [chapters/04_bulgular.qmd:497-501]. **0,220 → 0,004.** Ağırlıklandırmadan önce
ayarlama setindeki en büyük fark sınırın üstündeydi; sonra fark **pratik olarak yok
oldu** (0,004 ≈ "elmayla elma").

**Yanlış okumayı önceden düzeltelim — iki tuzak:**
- Bu grafik **ayarlama setinin** dengesini gösterir, Tablo 1'deki *tüm* değişkenlerin
  değil. Örneğin anne antidepresan kullanımının ham dengesizliği büyüktür (SMD = 0,53,
  [:485]) ama o bir **aracı** olduğundan (Şekil 4.2) bilerek ayarlanmaz ve bu grafiğe
  girmez — "eksik" değil, tasarım gereğidir.
- Denge kazanımı bir **nedensellik** kanıtı değildir; yalnız gözlenen karıştırıcılarda
  karşılaştırmayı "elmayla elma"ya yaklaştırır. Ölçülmemiş karıştırıcılar hâlâ olabilir.

## Bir cümleyle

> Şekil 4.3, birincil ayarlama setindeki en büyük grup farkının ağırlıklandırmayla
> 0,220'den 0,004'e — yani denge eşiğinin belirgin altına — indiğini belgeler; böylece bu
> değişkenlerde karşılaştırma "elmayla elma" hâline gelir, ama bu bir nedensellik değil,
> yalnız gözlenen karıştırıcılarda denge kanıtıdır.

*Komşu öğe:* tam sayısal denge tablosu `@tbl-apa-covariate-balance` (Tablo 4.2) aynı
biçimde açılabilir.

---

# Şekil 4.4'ü Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.4 = Eğilim skoru ortak destek dağılımı**
Kanonik etiket: `@fig-propensity-overlap` · Kaynak: chapters/04_bulgular.qmd:569 (caption)
+ :503-505 (gövde) · Aile: eğilim skoru yoğunluk-örtüşme grafiği.

## Bu grafik hangi soruna çözüm?

İki grubu adilce karşılaştırabilmek için önce onların **karşılaştırılabilir** olması
gerekir. Eğer bazı aileler o kadar "belirgin DM tipi" ya da "belirgin kontrol tipi" ki
öbür grupta hiç benzeri yoksa, o ailelerde karşılaştırma yapılamaz. Bu grafik, **hangi
bölgede karşılaştırmanın geçerli** olduğunu gösterir.

Bir örtüşme grafiğini okumanın hamlesi: **iki dağılım çakışıyor mu, çakışan bölge
(ortak destek) ne kadar geniş?**

## Grafik nasıl kurulu?

- **Eğilim skoru** = "bu ailenin, arka plan özelliklerine (latent SES, kardeş yaş farkı,
  aile çocuk sayısı) bakılarak DM grubunda olma olasılığı" — DAG ayarlama setinden
  kestirilen bir lojistik regresyonun çıktısı (model katsayıları:
  `@tbl-apa-propensity-model`).
- Grafik, DM ailelerinin ve kontrol ailelerinin eğilim skoru **yoğunluk dağılımlarını**
  üst üste çizer; çakışan alan = **ortak destek** (karşılaştırılabilirlik aralığı)
  [caption :569; :503-505].

## Grafik ne söyledi? — Dürüst okuma

İki dağılım geniş bir bölgede **çakışıyorsa**, karşılaştırma bu ortak destek aralığında
geçerlidir; çakışmayan uçlar (yalnız bir gruba özgü aşırı skorlar) karşılaştırılamaz
bölgedir. Dağılımların tam çakışma oranı ve ortak destek sınırları, üretilmiş model
artefaktında (`@tbl-apa-propensity-model` ve gitignored `outputs/`) tutulur; bu izahatta
kaynağında görünmeyen bir çakışma yüzdesi **uydurulmaz**.

**Yanlış okumayı önceden düzeltelim — en sık karışıklık burada:** *örtüşme ≠ denge.*
- **Örtüşme (bu şekil, 4.4):** grupların karşılaştırılabilir *olup olmadığı* — ön koşul.
- **Denge (Şekil 4.3, Love grafiği):** karşılaştırılabilir gruplar arka planda gerçekten
  *eşitlendi mi* — sonuç.
İki dağılım kusursuz çakışsa bile gruplar dengesiz olabilir; ikisi ayrı sorudur ve ayrı
şekillerle yanıtlanır.

## Bir cümleyle

> Şekil 4.4, DM ve kontrol ailelerinin eğilim skoru dağılımlarının çakıştığı **ortak
> destek** aralığını — yani karşılaştırmanın geçerli olduğu bölgeyi — gösterir; bu bir
> karşılaştırılabilirlik ön koşuludur, dengenin kendisi değildir (dengeyi Şekil 4.3
> belgeler).

*Komşu öğe:* eğilim skoru modelinin katsayıları `@tbl-apa-propensity-model` (Tablo 4.4)
aynı biçimde açılabilir.

---

# Şekil 4.5'i Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.5 = Latent SES kompozit bileşen korelasyon matrisi (ısı haritası)**
Kanonik etiket: `@fig-ses-correlation` · Kaynak: chapters/04_bulgular.qmd:571 (caption) +
:487-495 (gövde), :559 (SES kompozit tablo caption) · Aile: korelasyon ısı haritası.

## Bu ısı haritası hangi soruna çözüm?

Sosyoekonomik durumu (SES) tek bir ham göstergeyle ölçmek kırılgandır. Nitekim üç ham
SES göstergesi gruplar arasında **ayrı ayrı dengesizdir:** anne eğitimi (SMD = 0,29), eş
eğitimi (SMD = 0,32) ve eş mesleki indeksi ISEI-08 (SMD = 0,23) [chapters/04_bulgular.qmd:487-491].
Bu üçünü tek bir **birleşik (latent) SES** ölçüsünde topladığımızda gruplar arası fark
neredeyse kayboluyor (SMD = 0,03) [:493]. Peki bu birleşik ölçü, bileşenlerini gerçekten
tutarlı biçimde temsil ediyor mu? Isı haritası bunu gösterir.

Bir ısı haritasını okumanın hamlesi: **en koyu (en güçlü) hücrelere ve renk skalasının
verdiği işarete bak** — hangi bileşenler kompozitle güçlü ve hangi yönde ilişkili?

## Isı haritası nasıl kurulu?

- **Hücre** = iki gösterge (ya da gösterge ↔ latent SES) çifti; **renk** = korelasyonun
  **büyüklüğü ve işareti**.
- Bileşenler: eğitim, mesleki statü (ISEI-08) ve materyal (maddi) gösterge; artı birleşik
  latent SES [caption :571].
- İyi bir kompozit, bileşenleriyle **güçlü ve pozitif** korele olmalıdır — ısı
  haritasında bu, kompozit satır/sütununda koyu, aynı yönlü hücreler demektir.

## Isı haritası ne söyledi? — Dürüst okuma

- **Bütünleştirme geçerliği:** latent SES göstergesinin doğrulayıcı faktör analizi (CFA)
  iyi uyum vermiştir; tablo dipnotu, birden büyük TLI değerlerinin örneklem oynamasından
  geldiğini ve iyi uyuma işaret ettiğini, bazı yazılımların 1,00'a sınırladığını belirtir
  [chapters/04_bulgular.qmd:559]. (Uyum eşikleri Hu–Bentler 1999 geleneğidir; ayrıntılı
  değerler `@tbl-apa-ses-composite`.)
- **Denge kazanımı:** ham bileşenler dengesiz (0,29 / 0,32 / 0,23) iken birleşik ölçü
  dengelidir (0,03) — kompozitin işe yaradığının kanıtı budur ✓.
- Bileşenler-arası tam korelasyon değerleri (ısı haritasının hücreleri) üretilmiş
  artefakttadır; kaynağında sayı olarak görünmeyen hücre değerleri burada **uydurulmaz**.
  Korelasyon büyüklüğü geleneği için (Cohen: 0,10 küçük / 0,30 orta / 0,50 büyük) hücreleri
  `@tbl-apa-ses-composite` ile birlikte oku.

**Yanlış okumayı önceden düzeltelim:**
- Renk **yoğunluğu büyüklüktür, anlamlılık değil** — koyu hücre "istatistiksel olarak
  anlamlı" demek değil, "güçlü ilişki" demektir.
- Bileşenlerin kompozitle yüksek korelasyonu, kompozitin **iç tutarlılığını** destekler;
  ama "SES'i kusursuz ölçtük" ya da "SES nedensel etkendir" anlamına **gelmez**.

## Bir cümleyle

> Şekil 4.5, latent SES kompozitinin eğitim, mesleki statü ve materyal bileşenleriyle
> tutarlı (güçlü, pozitif) bir korelasyon yapısı kurduğunu görselleştirir; bu tutarlılık,
> tek tek dengesiz olan ham SES göstergelerini (SMD 0,29/0,32/0,23) grup dengesi sağlayan
> (SMD 0,03) tek bir geçerli ölçüde birleştirmenin gerekçesini belgeler.

*Komşu öğe:* SES kompozit bileşenleri ve CFA uyum ölçütleri `@tbl-apa-ses-composite`
(Tablo 4.5) aynı biçimde açılabilir.

---

# Şekil 4.6'yı Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.6 = Birincil analiz değişkenlerinde analitik eksik veri örüntüsü**
Kanonik etiket: `@fig-missing-pattern` · Kaynak: chapters/04_bulgular.qmd:573 (caption) +
:515-524 (gövde) · Aile: eksik veri örüntüsü haritası.

## Bu harita hangi soruna çözüm?

Bir analizin güvenilirliği, kullanılan verinin **ne kadarının gerçekten toplanabildiğine**
bağlıdır. Çok fazla boşluk varsa ve boşluklar rastgele değilse, sonuçlar yanlı olabilir.
Bu harita, hangi değişkende ne kadar boşluk olduğunu ve boşlukların nerede kümelendiğini
gösterir.

Bir eksik-veri haritasını okumanın hamlesi: **hangi değişkende, ne oranda boşluk var, ve
bu boşluk analitik mi yoksa tasarım kaynaklı mı?**

## Harita nasıl kurulu?

- Görsel, **yalnız gerçekten toplanamayan (analitik) eksikliği** gösterir; FIML/çoklu
  atama çerçevesine giren değişken düzeyinde eksiklik oranlarıdır (toplam ≈ **%0,3**)
  [caption :573].
- **Kritik ayrım:** tasarım gereği hiç gözlenmeyen hücreler (kontrol grubunda DM yılı) bu haritaya **dâhil değildir** — bunlar "eksik" değil, tanım gereği yok
  [caption :573].

## Harita ne söyledi? — Kanıt

| Değişken | Analitik eksiklik | Not |
|---|---|---|
| ISEI-08 mesleki indeks | %9,1 | en yüksek analitik eksiklik ⚠️ |
| Beck toplam puanı | %1,2 | düşük ✓ |
| Maddi gösterge | %0,4 | ihmal edilebilir ✓ |

Değerler [chapters/04_bulgular.qmd:516-517]. Genel analitik eksiklik düşüktür.

**Yanlış okumayı önceden düzeltelim — en sık karışıklık:** *analitik eksiklik ≠ tasarım
kaynaklı boşluk.* DM süresi gibi yalnız DM bağlamında anlamlı olan zamanlama değişkenleri kontrol ailelerinde tanım gereği yoktur. Bu tür tasarım kaynaklı boşluklar analitik eksiklik sayılmaz ve grup karşılaştırmalı imputasyonla doldurulmaz; haritayı "veri kalitesi kötü" diye okuma tuzağına düşme: analitik eksiklik gerçekte çok düşüktür.

## Bir cümleyle

> Şekil 4.6, birincil analiz değişkenlerindeki gerçek (analitik) eksikliğin çok düşük
> olduğunu (toplam ≈ %0,3; en yüksek ISEI-08 %9,1) gösterir; tasarım gereği yalnız DM
> DM bağlamına özgü zamanlama boşlukları ise analitik eksiklik değildir ve
> bilerek haritanın dışında tutulmuştur.

*Komşu öğe:* eksik veri özeti tablosu `@tbl-apa-missing-data` (Tablo 4.3) aynı biçimde
açılabilir.

---

# Şekil 4.7'yi Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.7 = H1 dört EMBU-C alt ölçeğinde grup ana etkisi (orman grafiği)**
Kanonik etiket: `@fig-h1-forest` · Kaynak: chapters/04_bulgular.qmd:704 (caption) +
:605-650 (gövde) · Aile: orman grafiği (forest).

## Bu grafik hangi soruna çözüm?

H1'in asıl sorusu: DM ailelerindeki **çocuklar**, kontrol çocuklarına kıyasla annelerinden
farklı bir ebeveynlik mi algılıyor? Dört boyutta (sıcaklık, aşırı koruma, reddetme,
karşılaştırma) grup farkını ve o farkın **ne kadar kesin** olduğunu tek bakışta görmek
gerekir. Orman grafiği bunu yapar.

Bir orman grafiğini okumanın hamlesi tektir: **her boyut için güven aralığı (yatay çizgi)
kesikli sıfır çizgisini kesiyor mu?** Kesiyorsa fark sıfırdan ayırt edilemiyor; kesmiyorsa
yön belirginleşiyor. Çizginin genişliği = kesinlik.

## Grafik nasıl kurulu?

- **Nokta** = DM eksi Kontrol grup ana etkisi (ham 1–4 ölçek puanı biriminde; indeks ve
  kardeş rolleri eşit ağırlıkla ortalanır) [caption :704].
- **Yatay çizgi** = %95 güven aralığı; **kesikli dikey çizgi** = sıfır fark.
- Tahminler, aile düzeyi rastgele kesişimli çok düzeyli modelden (482 çocuk satırı)
  gelir [:605].

## Grafik ne söyledi? — Kanıt

| Alt ölçek | b (ölçek puanı) | %95 GA | BH-FDR q | Sıfırı kesiyor mu? |
|---|---|---|---|---|
| **Reddetme** | 0,14 | [0,07; 0,22] | 0,001 | Hayır → DM daha yüksek ✓ |
| **Aşırı koruma** | 0,19 | [0,07; 0,30] | 0,003 | Hayır → DM daha yüksek ✓ |
| **Sıcaklık** | 0,14 | [0,02; 0,25] | 0,029 | Hayır (sınırda) ⚠️ |
| **Karşılaştırma** | 0,13 | [−0,01; 0,26] | 0,069 | Evet → ayırt edilemiyor ❌ |

Değerler [chapters/04_bulgular.qmd:611-616]. Reddetme en güçlü tekil sinyaldir
(tamamlayıcı Hedges g ≈ 0,38; küçük-orta) [:620].

**Yanlış okumayı önceden düzeltelim — anlamlı ≠ sağlam.** Sıcaklık frekansçı olarak sınırda
anlamlı (q = 0,029) *görünse de*, bağımsız Bayesçi hat onu **doğrulamaz** — hatta H0 lehine
orta kanıt verir (BF₁₀ = 0,29). Buna karşılık reddetme (BF₁₀ = 10,55; Jeffreys ölçeğinde
"güçlü") ve aşırı koruma (BF₁₀ = 6,93; "orta") iki çerçevede de doğrulanır [:621-624]. Ders:
tek bir p değeri "sağlam bulgu" demek değildir; iki çerçevenin uzlaşması aranır. Dolayısıyla
sağlam sonuç yalnız **reddetme ve aşırı korumadır**; sıcaklık çerçeveler-arası ayrışma
nedeniyle sağlam sayılmaz, karşılaştırma null'dür.

## Bir cümleyle

> Şekil 4.7, DM ailelerindeki çocukların annelerinden daha yüksek **reddetme** (b = 0,14)
> ve **aşırı koruma** (b = 0,19) algıladığını — güven aralıkları sıfırı kesmeden ve Bayesçi
> hatla da doğrulanarak (BF₁₀ 10,55 ve 6,93) — belgeler; sıcaklık sinyali Bayes'te erir,
> karşılaştırma ise null'dür.

*Komşu öğeler:* `@tbl-apa-h1-primary` (rol-özgül) ve `@tbl-apa-h1-bayesian` (çift raporlama)
aynı biçimde açılabilir.

---

# Şekil 4.8'i Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.8 = H2 aktör-partner karşılıklı bağımlılık modeli (APIM) yol diyagramı**
Kanonik etiket: `@fig-h2-apim-path` · Kaynak: chapters/04_bulgular.qmd:744 (caption) +
:707-735 (gövde) · Aile: yol/SEM diyagramı (APIM).

## Bu diyagram hangi soruna çözüm?

İki kardeşin ilişki algısı birbirinden bağımsız değildir — biri "kardeşimle çatışıyorum"
derken öbürü de etkilenir. Basit bir grup karşılaştırması bu **karşılıklı etkiyi**
görmezden gelir. APIM, "kendi algım kendi çıktımı ne kadar belirliyor (**aktör**)" ile
"kardeşimin algısı benim çıktımı ne kadar belirliyor (**partner**)" etkilerini ayırır.

Bir yol diyagramını okumanın hamlesi: **hangi oklar aktör, hangileri partner?** Sonra
katsayı işareti ve büyüklüğüne bak. Çift yönlü eğri = kovaryans (yön iddiası yok).

## Diyagram ne söyledi? — Kanıt

Kardeş İlişkileri Anketi'nin dört boyutunda (yakınlık, güç, çatışma, rekabet):

- **Aile-ortalama Welch testleri** (241 aile): dört boyutun tamamında grup farkı küçük
  (etki büyüklüğü **d < 0,20**) [chapters/04_bulgular.qmd:714-716].
- **APIM**: grup, rol ve grup × rol etkilerinin hiçbiri anlamlı değil
  (FDR-düzeltilmiş **p > 0,350**) [:718-720].
- **Olsen-Kenny latent düad CFA**: indeks çocuk ile kardeşin çatışma/kavga boyutundaki
  latent korelasyonu **r = 0,27** [:723].

**Yanlış okumayı önceden düzeltelim — anlamsız ≠ etki yok.** Fark bulunamaması, "kardeş
ilişkisinde grup farkı **yoktur**" demek değildir; bu, "mevcut örneklemde bir farkın
**gösterilememesi**"dir (kanıt yokluğu ≠ yokluk kanıtı) [:709-710]. Farkın yokluğunu
doğrudan test edecek eşdeğerlik sınaması (TOST) ön-kayıtlı planda olmadığından
uygulanmamıştır; bu yüzden bulgu bilinçli olarak "fark yoktur" değil **"farkın varlığına
ilişkin kanıt yetersizdir"** diliyle raporlanır [:730-733].

## Bir cümleyle

> Şekil 4.8, kardeşlerin karşılıklı etkisini modelleyen APIM'de grup/rol/grup × rol
> etkilerinin hiçbirinin anlamlı olmadığını (aile-ortalama d < 0,20; APIM FDR p > 0,350)
> gösterir; ancak bu, kardeş ilişkisinde grup farkının *yokluğunun kanıtı* değil, mevcut
> örneklemde farkın *gösterilemediği* (kanıt yetersizliği) biçiminde okunmalıdır.

*Komşu öğeler:* `@tbl-apa-h2-family-mean` ve `@tbl-apa-h2-apim` aynı biçimde açılabilir.

---

# Şekil 4.9'u Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.9 = H3 antidepresan-katmanlı grup etkisi (EMBU-P, katmanlı orman grafiği)**
Kanonik etiket: `@fig-h3-stratified-forest` · Kaynak: chapters/04_bulgular.qmd:789 (caption)
+ :755-778 (gövde) · Aile: katmanlı orman grafiği.

## Bu grafik hangi soruna çözüm?

H1'de **çocuklar** DM ailelerinde daha çok reddetme/aşırı koruma algıladı. Peki
**annelerin kendileri** aynı farkı bildiriyor mu? Ve bu, antidepresan kullanan/kullanmayan
annelerde değişiyor mu? Katmanlı orman grafiği, grup etkisini üç katmanda (kullanan,
kullanmayan, tüm örneklem) yan yana gösterir.

Okuma hamlesi: **her panelde güven aralığı sıfırı kesiyor mu**, ve katmanlar arasında
yön/büyüklük tutarlı mı?

## Grafik ne söyledi? — Kanıt

Dört EMBU-P alt ölçeği, 241 anne, birincil model (ham b, ölçek puanı) [chapters/04_bulgular.qmd:756-760]:

| Alt ölçek | b | %95 GA | Sıfırı kesiyor mu? |
|---|---|---|---|
| Sıcaklık | 0,06 | [−0,07; 0,20] | Evet ❌ |
| Aşırı koruma | 0,06 | [−0,12; 0,24] | Evet ❌ |
| Reddetme | −0,05 | [−0,12; 0,02] | Evet ❌ |
| Karşılaştırma | 0,06 | [−0,08; 0,20] | Evet ❌ |

Dördü de anlamsız (FDR p > 0,500); standardize etki küçük (|β| < 0,17). IPTW ile tekrarda
katsayılar −0,04 ile 0,05 arası, yine anlamsız (p > 0,510). Antidepresan kullanan (n = 46)
ve kullanmayan (n = 195) katmanlarda sonuç yön/büyüklük olarak değişmez [:762-767].

**Büyüklük okuryazarlığı — "yokluk kanıtı" ile "kanıt yokluğu"nu ayır.** Bayesçi hat burada
kritik: BF₁₀ = 0,17–0,23 (H0 lehine orta kanıt) ve ROPE payları yüksek (reddetme %93,
sıcaklık %68, karşılaştırma %69, aşırı koruma %61) [:768-772]. TOST eşdeğerlik: aşırı koruma
ve karşılaştırma "Eşdeğer", sıcaklık ve reddetme "Belirsiz"; ama bu karar **eşdeğerlik
sınırına (SESOI) duyarlıdır** — daha katı ±0,20/±0,25 SMD bantlarında hiçbir alt ölçekte
biçimsel eşdeğerlik kalmaz [:772-776]. Yani "eşdeğer" iddiası koşulludur, mutlak değil.

**En önemli ders — H1 ile H3'ün birlikte okunması (bilgi-verici ayrışması):** çocuklar
reddetme farkı bildirirken (H1) anneler bildirmiyor (H3). Bu çelişki değil, **bilgi
vericiye özgü geçerli bilgidir**; farkın anne öz-bildiriminde *görünür olmadığına* işaret
eder [:752-754].

## Bir cümleyle

> Şekil 4.9, annelerin kendi bildirdikleri dört ebeveynlik boyutunda DM–kontrol farkının
> birincil, IPTW ve Bayesçi analizlerde tutarlı biçimde anlamsız kaldığını (BF₁₀ 0,17–0,23,
> H0 lehine) gösterir; çocukların bildirdiği reddetme farkıyla (H1) birlikte okunduğunda
> bu, farkın anne öz-bildiriminde görünür olmadığına — bir bilgi-verici ayrışmasına —
> işaret eder.

*Komşu öğeler:* `@tbl-apa-h3-primary-iptw` ve `@tbl-apa-h3-sensitivity` aynı biçimde
açılabilir.

---

# Şekil 4.10'u Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.10 = H5 Bland-Altman tutarlılık haritası (Strateji 1: ICC + Bland-Altman)**
Kanonik etiket: `@fig-h5-bland-altman` · Kaynak: chapters/04_bulgular.qmd:929 (caption) +
:872-887 (gövde) · Aile: Bland-Altman uyum haritası.

## Bu harita hangi soruna çözüm?

H5'in asıl sorusu: anne ile çocuk **aynı** ebeveynlik ilişkisini benzer mi algılıyor?
Basit refleks korelasyona bakmaktır — ama korelasyon yanıltır. Bland-Altman, **mutlak
uyumu** (iki tarafın aynı puanı verip vermediğini) doğrudan ölçer.

Bir Bland-Altman haritasını okumanın hamlesi: **noktalar sıfır-fark çizgisi etrafında ne
kadar dağınık, uyum sınırları (LoA) ne kadar geniş?** Geniş = düşük uyum. Yanında ICC
(sınıf-içi korelasyon) mutlak uyumu tek sayıya özetler.

## Harita nasıl kurulu?

- Paneller = dört EMBU alt ölçeği × üç düad tipi (anne↔indeks, anne↔kardeş, indeks↔kardeş);
  renkler = DM ve kontrol [caption :929].
- Her panelde x = iki puanın ortalaması, y = **farkları**; orta çizgi = ortalama fark,
  üst/alt çizgiler = uyum sınırları.

## Harita ne söyledi? — Dürüst bilanço

Anne ↔ indeks çocuk ICC(A,1)/ICC(2,1) (mutlak uyum), dört alt ölçek: kontrol 0,03–0,20,
DM −0,01–0,08, havuz 0,00–0,10 [chapters/04_bulgular.qmd:872-875]. Bu düzey Cicchetti
(1994) eşiklerinde en alt bant — **"fakir-zayıf" uyum**. Alt ölçek bazında dörtte dördü
kontrol > DM yönünde:

| Alt ölçek | Kontrol ICC | DM ICC |
|---|---|---|
| Sıcaklık | 0,145 | 0,027 |
| Aşırı koruma | 0,204 | 0,009 |
| Reddetme | 0,029 | −0,006 |
| Karşılaştırma | 0,103 | 0,084 |

Değerler [chapters/04_bulgular.qmd:880-883]. Bland-Altman'da ortalama fark sıfıra yakın,
**uyum sınırları geniştir** — yani sistematik yanlılık yok ama birey düzeyinde uyum düşük.

**Yanlış okumayı önceden düzeltelim — iki tuzak:**
- *Korelasyon ≠ uyum.* Anne ve çocuk puanları yüksek korele olsa bile biri diğerinden
  sistematik kayabilir; Bland-Altman/ICC bunu yakalar, korelasyon yakalamaz. Bu haritanın
  varlık nedeni budur.
- *Negatif ICC "imkânsız/hata" değildir;* sıfıra yakın veya uyumsuz varyans yapısını
  yansıtır (DM'de −0,006'ya kadar). Yüksek pozitif = yüksek uyum; sıfır civarı/negatif =
  uyum yok.

Dürüstlük kapısı: bu strateji H5'in **en güçlü, dört boyutu da kapsayan manifest
kanıtıdır** ve uyumun **düşük** olduğunu (annenin ve çocuğun aynı ilişkiyi büyük ölçüde
farklı algıladığını) tutarlı biçimde gösterir; ön-kayıtlı "en az üç strateji aynı yön"
triangülasyon şartı karşılanmamıştır [:850-855].

## Bir cümleyle

> Şekil 4.10, anne ile çocuğun aynı ebeveynlik tutumunu büyük ölçüde farklı algıladığını —
> mutlak uyumun ("fakir-zayıf" bandında; kontrolde 0,03–0,20, DM'de −0,01–0,08) ve geniş
> Bland-Altman uyum sınırlarıyla — dört boyutun tamamında kontrol > DM yönünde belgeler;
> bu, korelasyonun gizleyeceği düşük mutlak uyumu açığa çıkaran en güçlü manifest kanıttır.

*Komşu öğeler:* `@fig-h5-rsa-surface` (Şekil 4.11, yanıt yüzeyi) ve `@tbl-apa-h5-concordance`
(beş stratejinin yön oyları) aynı biçimde açılabilir.

---

# Şekil 4.11'i Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.11 = H5 yanıt yüzeyi analizi (RSA) yüzeyleri**
Kanonik etiket: `@fig-h5-rsa-surface` · Kaynak: chapters/04_bulgular.qmd:931 (caption) +
:876-887 (gövde) · Aile: yanıt yüzeyi (RSA).

## Bu şekil hangi soruna çözüm?

Elimizde aynı konu için **iki ayrı algı** var: annenin ve indeks çocuğun puanı. Basit
refleks farkı (anne − çocuk) tek sayıya indirmektir; ama fark skoru iki bilgiyi ezer —
"anne 4 / çocuk 2" ile "anne 2 / çocuk 4" aynı |2| farkı verir, oysa bunlar bambaşka aile
durumlarıdır. Yanıt yüzeyi, iki algıyı **ezmeden iki ayrı eksende** tutup çıktının her
kombinasyonda nasıl değiştiğini üç boyutlu bir tepe/vadi manzarası olarak çizer.

Bir RSA yüzeyini okumanın hamlesi: **iki hatta ayrı ayrı bak** — (1) iki algının eşit
olduğu **uyum hattı** (X = Y, noktalı çizgi) boyunca; (2) zıt yönde ayrıştıkları
**uyumsuzluk hattı** boyunca. Fark skorunun sakladığı örüntü ikinci hattadır.

## Yüzey nasıl kurulu?

- **X ekseni** = anne puanı, **Y ekseni** = indeks çocuk puanı (ham 1–4 Likert ortalaması,
  merkezlenmiş-ölçeklenmemiş); **Z (yükseklik)** = **anne Beck Depresyon toplam puanı**
  [chapters/04_bulgular.qmd:884].
- Yüzey ikinci derecedendir: Z = b₀ + b₁X + b₂Y + b₃X² + b₄XY + b₅Y²; kareli/çarpımlı
  terimler yüzeyin bükülmesine (tepe/vadi/eyer) izin verir.
- Yalnız **sıcaklık ve reddetme** alt ölçeklerinde kestirilmiştir [:883].

## Yüzey ne söyledi? — Dürüst bilanço

Uyumsuzluk hattı boyunca eğriliği özetleyen **a₄ = b₃ − b₄ + b₅**, reddetme alt ölçeği
[chapters/04_bulgular.qmd:884]:

| Kesim | a₄ | p | Okuma (Fisher, p < 0,05) |
|---|---|---|---|
| Havuzlanmış | −13,96 | 0,012 | sıfırdan ayırt edilebilir ✓ |
| Kontrol | −15,93 | 0,064 | sınırda, "anlamlı değil" ⚠️ |
| DM | −7,07 | 0,430 | ayırt edilemiyor ❌ |

**Yanlış okumayı önceden düzeltelim — büyüklük yanıltıcıdır.** a₄ birimi "Beck / EMBU-
ortalama-karesi"dir; ölçeğe duyarlı, tuhaf bir birim. Bu yüzden −13,96 "büyük etki" demek
**değildir**; yalnız "eğrilik sıfır değil, negatif" demektir — tez de "mutlak büyüklükleri
değil işaret/anlamlılık örüntüsü yorumlanmalıdır" der [:884]. −13,96 ile −7,07'yi büyüklük
olarak kıyaslamak da anlamsızdır. Ayrıca sinyal havuzda anlamlıyken gruplarda erir; bu
strateji tek bir grup-uyum skoru üretmediğinden "DM mi kontrol mü daha uyumlu" sorusuna
**yanıt vermez** [:885].

## Bir cümleyle

> Şekil 4.11, anne ve çocuk reddetme/sıcaklık algısını fark skoruna ezmeden iki eksende
> tutup çıktı olarak anne depresyonunu bir yüzey olarak çizer; uyumsuzluk hattı eğriliği a₄
> reddetmede havuz düzeyinde anlamlıdır (−13,96, p = 0,012) ama gruplarda erir ve birim
> ölçeğe duyarlı olduğundan yalnız işaret/anlamlılık olarak — yönlü grup sonucu iddia
> etmeden — okunur.

*Komşu öğe:* `@fig-h5-bland-altman` (Şekil 4.10, mutlak uyum haritası) tamamlayıcısıdır.

---

# Şekil 4.12'yi Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.12 = [KEŞİFSEL] Latent profil analizi model seçim tanıları**
Kanonik etiket: `@fig-lpa-fit-indices` · Kaynak: chapters/04_bulgular.qmd:985 (caption) +
:968-982 (gövde) · Aile: LPA/LCA model-seçim tanısı.

## Bu şekil hangi soruna çözüm?

Aileleri, ruh sağlığı ve ebeveynlik göstergelerine göre **kaç doğal gruba (profile)**
ayırabiliriz? Latent profil analizi (LPA) bunu veriden çıkarır; ama "kaç profil?" sorusunun
tek bir mekanik yanıtı yoktur. Bu şekil, profil sayısına göre üç model-seçim tanısını
(BIC, entropi, BLRT p) yan yana koyarak seçimi görünür kılar.

Okuma hamlesi: **BIC minimumu nerede — ama parsimoni kuralı ve yorumlanabilirlik ne
diyor?** Sayısal minimum tek başına seçim değildir.

## Şekil ne söyledi? — Dürüst bilanço

- BIC sayısal minimumu **4-profildedir** ve bu çözüm daha düşük BIC, hafifçe daha yüksek
  entropi ve anlamlı BLRT verir; **yine de 3-profil çözümü benimsenmiştir** — çünkü ΔBIC≈2
  parsimoni eşiği (Raftery 1995 geleneği) ve yorumlanabilirlik, 3–4 profil arası model-seçim
  belirsizliğine işaret eder [caption :985].
- Kategorik göstergeli poLCA duyarlılığı 2-sınıf çözümü destekler (BIC = 2641,0; sınıf
  oranları %63,4 / %36,6; **entropi = 0,60**); modal sınıf regresyonunda DM grubu üyeliği
  anlamlı değiştirmez (OR = 0,99; %95 GA [0,57; 1,71]; p = 0,962) [:977-980].

**Yanlış okumayı önceden düzeltelim:**
- *En düşük BIC otomatik kazanan değildir.* Seçim kuralı (ΔBIC≤2 parsimoni) tablo ve metinde
  aynı profil sayısını göstermek zorundadır (AGENTS.md seçim-kuralı tutarlılığı); burada
  bilinçle 4 değil 3 seçilmiştir.
- Entropi 0,60, iyi sınıf ayrımı için yol gösterici 0,80 eşiğinin **altındadır** → profiller
  keskin ayrışmıyor; çözüm temkinli okunmalı.
- **[KEŞİFSEL] uyarısı:** bu bir doğrulayıcı bulgu değildir; profil yapısı önceden
  hipotezlenmemiş, veriden keşfedilmiştir.

## Bir cümleyle

> Şekil 4.12, LPA'da BIC'in sayısal minimumu 4-profilde olsa da parsimoni (ΔBIC≈2) ve
> yorumlanabilirlik gereği keşifsel olarak 3-profil çözümünün benimsendiğini gösterir; poLCA
> 2-sınıf çözümünde de (entropi 0,60, sınırlı ayrım) DM üyeliği sınıfı anlamlı değiştirmez
> (OR = 0,99) — yani en düşük BIC tek başına seçim değildir.

*Komşu öğe:* sayısal model-seçim tanıları `@tbl-apa-lpa-bifactor` (Tablo 4.12) aynı biçimde
açılabilir.

---

# Şekil 4.13'ü Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.13 = [KEŞİFSEL] EBIC-LASSO Gauss grafik modeli (ağ)**
Kanonik etiket: `@fig-network-graph` · Kaynak: chapters/04_bulgular.qmd:1003 (caption) +
:989-998 (gövde) · Aile: Gauss grafik modeli (GGM) ağı.

## Bu ağ hangi soruna çözüm?

Ebeveynlik, kardeş ilişkisi ve anne depresyonu göstergeleri birbirine bağlıdır; ama hangi
ikili **doğrudan** (diğer her şey sabitken) bağlı, hangisi yalnız üçüncü bir değişken
üzerinden dolaylı bağlı? Ağ analizi, bu doğrudan bağlantı iskeletini çizer.

Okuma hamlesi: **en kalın kenarlarla bağlı ve en büyük (merkezî) düğümler hangileri?**
Kenar **yokluğu** = koşullu bağımsızlık iddiası.

## Ağ nasıl kurulu?

- **Dokuz değişken:** dört EMBU-P + dört SRQ alt ölçeği + Beck total; EBIC-LASSO (γ = 0,5),
  havuzlanmış n = 238 [chapters/04_bulgular.qmd:990-991].
- **Kenar** = kısmi korelasyon (diğer tüm değişkenler sabitken kalan ilişki); **kenar
  kalınlığı** = mutlak güç; **düğüm boyutu** = strength merkeziyeti [caption :1003].

## Ağ ne söyledi? — Dürüst okuma

En güçlü kenarlar, en merkezî düğümler ve ağ kararlılık (case-dropping bootstrap) katsayısı,
üretilmiş artefakttan metne yansıtılır (`@tbl-apa-network`); bu izahatta kaynağında
sayı olarak görünmeyen kenar değerleri **uydurulmaz**.

**Yanlış okumayı önceden düzeltelim:**
- *Kenar nedensel ok değildir.* Tez açıkça der: "koşullu bağımlılık nedensellik olarak
  yorumlanmamıştır" [:996]. GGM yönsüz ve **[KEŞİFSEL]**dir.
- Kenar yoğunluğu = ilişki gücü, anlamlılık değil; ağın kararlılığı (bootstrap CS-katsayısı)
  ayrıca yorumlanmalıdır.

## Bir cümleyle

> Şekil 4.13, dokuz ebeveynlik/kardeş/depresyon göstergesi arasındaki **doğrudan** (kısmi
> korelasyon) bağlantı iskeletini ve merkezî düğümleri keşifsel olarak haritalar; kenarlar
> koşullu bağımlılıktır, nedensel ok değildir.

*Komşu öğeler:* `@fig-network-nct` (Şekil 4.14, grup karşılaştırması) ve `@tbl-apa-network`
aynı biçimde açılabilir.

---

# Şekil 4.14'ü Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.14 = [KEŞİFSEL] Ağ Karşılaştırma Testi (NCT) sonuçları**
Kanonik etiket: `@fig-network-nct` · Kaynak: chapters/04_bulgular.qmd:1005 (caption) +
:994-996 (gövde) · Aile: ağ karşılaştırma (NCT) görseli.

## Bu şekil hangi soruna çözüm?

Şekil 4.13 havuzlanmış ağı çizdi. Peki DM ailelerinin ağı, kontrol ailelerinin ağından
**yapısal olarak farklı mı**? Ağ Karşılaştırma Testi (NCT), iki ağı bir bütün olarak
karşılaştırır.

Okuma hamlesi: **iki ağ arasındaki fark istatistiksel olarak anlamlı mı?** İki eksen
sorulur: ağ invaryansı (bağlantı yapısı) ve global strength (toplam bağlantı gücü).

## Şekil ne söyledi? — Dürüst okuma

NCT'nin ağ invaryans ve global strength p değerleri, **DM ve kontrol ağlarının anlamlı
düzeyde ayrışmadığını** gösterir [caption :1005]; exact p değerleri `@tbl-apa-network`
içinde raporlanır (kaynak metinde sayı olarak görünmeyen p'ler burada uydurulmaz).

**Yanlış okumayı önceden düzeltelim — anlamsız ≠ özdeş.** "Anlamlı ayrışma yok", "iki ağ
aynıdır" demek **değildir**; iki ağın farkını göstermek için mevcut örneklemin gücü
yetersiz kalmış olabilir (kanıt yokluğu ≠ yokluk kanıtı). Ayrıca bu **[KEŞİFSEL]** bir
karşılaştırmadır.

## Bir cümleyle

> Şekil 4.14, DM ve kontrol ailelerinin ebeveynlik/depresyon ağlarının — invaryans ve
> global güç eksenlerinde — anlamlı düzeyde ayrışmadığını gösterir; bu, ağların *özdeş
> olduğunun* kanıtı değil, mevcut örneklemde bir farkın *gösterilemediğidir*.

*Komşu öğe:* `@fig-network-graph` (Şekil 4.13) ve `@tbl-apa-network` aynı biçimde açılabilir.

---

# Şekil 4.15'i Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.15 = [KEŞİFSEL] Yüksek Beck belirti düzeyi için eşzamanlı sınıflandırma ROC eğrisi**
Kanonik etiket: `@fig-clinical-roc` · Kaynak: chapters/04_bulgular.qmd:1034 (caption) +
:1010-1024 (gövde) · Aile: ROC eğrisi.

## Bu eğri hangi soruna çözüm?

Elimizdeki bilgilerle (demografi/SES; ve ek olarak ebeveynlik tutumları), yüksek depresif
belirti taşıyan anneleri **ayırt edebilir miyiz**? ROC eğrisi, bir sınıflandırma modelinin
"gerçek pozitifleri yakalama" ile "yanlış alarm verme" dengesini tüm eşiklerde gösterir.

Okuma hamlesi: **eğri sol-üst köşeye ne kadar yakın** (AUC = eğri altı alan)? Köşegen = şans.

## Eğri nasıl kurulu?

- **Temel model** = DM grup üyeliği + anne yaşı + latent SES + aile çocuk sayısı;
  **genişletilmiş model** = temel + dört EMBU-P alt ölçeği [chapters/04_bulgular.qmd:1011-1012].
- İç-validasyonlu **optimizm-düzeltilmiş bootstrap** (B = 1000) kullanılmıştır [:1013].

## Eğri ne söyledi? — Dürüst bilanço

Youden indeksiyle optimal işletme noktası [chapters/04_bulgular.qmd:1015-1016]:

| Ölçüt | Değer | Okuma |
|---|---|---|
| Eşik | 0,22 | düşük eşik (tarama bağlamı) |
| Duyarlılık | 0,75 | olguların ~%75'i yakalanır |
| Özgüllük | 0,60 | yanlış alarm görece yüksek ⚠️ |
| PPV / NPV | 0,41 / 0,87 | pozitif tahmin sınırlı, negatif tahmin iyi |

Modellerin AUC değerleri optimizm-düzeltilmiş olarak `@tbl-apa-clinical` içinde raporlanır;
kaynak metinde sayı olarak görünmeyen AUC burada uydurulmaz (AUC geleneği için: 0,70–0,80
kabul, 0,80–0,90 mükemmel — Hosmer-Lemeshow).

**Yanlış okumayı önceden düzeltelim — üç kritik uyarı (caption ve metin açıkça der):**
- *Eşzamanlı sınıflandırma ≠ ileriye dönük risk yordaması* [caption :1034]. Model, "gelecekte
  kim depresyon geliştirir"i değil, "şu an kimde yüksek belirti eşlik ediyor"u sınıflar.
- *Görünür (apparent) ≠ optimizm-düzeltilmiş.* AUC/kalibrasyon optimizm-düzeltilmiştir; ama
  karar-eğrisi net faydası görünür (iç-örneklem) değerdir ve yalnız düşük eşiklerde belirgin
  kalır (0,05 eşiğinde 0,23 → 0,25+ eşiklerde 0,04–0,10) [:1018-1020].
- **[KEŞİFSEL]** ve **dış örneklemde doğrulanmamıştır**; sonuçlar iç-validasyon düzeyindedir
  [:1024].

## Bir cümleyle

> Şekil 4.15, ebeveynlik tutumu eklenen modelin yüksek depresif belirtiyi eşzamanlı olarak
> orta düzeyde ayırt ettiğini (Youden noktasında duyarlılık 0,75 / özgüllük 0,60) gösterir;
> ama bu kesitsel bir sınıflandırmadır (ileriye dönük yordama değil), optimizm-düzeltilmiş ve
> dış-doğrulanmamış keşifsel bir bulgudur.

*Komşu öğeler:* `@fig-clinical-dca` (karar eğrisi) ve `@fig-clinical-calibration`
(kalibrasyon) aynı biçimde açılabilir.

---

# Şekil 4.16'yı Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.16 = [KEŞİFSEL] Klinik karar eğrisi analizi (DCA)**
Kanonik etiket: `@fig-clinical-dca` · Kaynak: chapters/04_bulgular.qmd:1036 (caption) +
:1017-1021 (gövde) · Aile: karar eğrisi (DCA).

## Bu eğri hangi soruna çözüm?

Bir sınıflandırma modeli "doğru" olabilir ama **klinik olarak yararlı** mı? Yani bu skoru
kullanarak karar vermek, "herkesi tara" ya da "kimseyi tarama" gibi basit stratejilerden
daha mı iyi? Karar eğrisi analizi (DCA) bunu, fayda-zarar dengesini eşiğe göre tartarak
yanıtlar.

Okuma hamlesi: **model eğrisi, "herkesi tara" ve "kimseyi tarama" kıyas çizgilerinin
üstünde hangi eşik aralığında kalıyor?** Klinik değer o aralıktadır.

## Eğri ne söyledi? — Dürüst bilanço

Geniş model, 0,05–0,50 eşik aralığının tamamında iki kıyas stratejisine göre **görünür
(apparent, iç-örneklem) pozitif net fayda** sağlar; ama net fayda 0,05 eşiğinde 0,23 iken
0,25 ve üzeri eşiklerde 0,04–0,10 düzeyine geriler — yani yalnız **düşük eşiklerde**
belirgindir [chapters/04_bulgular.qmd:1017-1020].

**Yanlış okumayı önceden düzeltelim:**
- *Net fayda ≠ doğruluk.* DCA, "kaç doğru bildi"yi değil, "bu skorla karar vermenin net
  klinik kazancı"nı ölçer.
- *Görünür ≠ optimizm-düzeltilmiş.* AUC/kalibrasyondan farklı olarak net fayda eğrileri
  bootstrap optimizm düzeltmesine tabi tutulmamıştır; iç-örneklem (iyimser) değerlerdir
  [caption :1036]. **[KEŞİFSEL].**

## Bir cümleyle

> Şekil 4.16, ebeveynlik-eklenen skorun yalnız **düşük tarama eşiklerinde** (≈0,05'te net
> fayda 0,23) "herkesi tara/kimseyi tarama"ya göre görünür bir klinik kazanç sağladığını,
> yüksek eşiklerde bu kazancın eridiğini gösterir; değerler optimizm-düzeltilmemiş
> iç-örneklem faydalarıdır.

*Komşu öğeler:* `@fig-clinical-roc` (Şekil 4.15) ve `@fig-clinical-calibration` (Şekil 4.17).

---

# Şekil 4.17'yi Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.17 = [KEŞİFSEL] Geniş sınıflandırma skorunun (görünür) kalibrasyon grafiği**
Kanonik etiket: `@fig-clinical-calibration` · Kaynak: chapters/04_bulgular.qmd:1038 (caption)
+ :1021-1022 (gövde) · Aile: kalibrasyon grafiği.

## Bu grafik hangi soruna çözüm?

Bir model "%30 olasılık" dediğinde, gerçekten o gruptakilerin yaklaşık %30'unda mı sonuç
görülüyor? Ayrım gücü (AUC) yüksek olsa bile tahminler sistematik yüksek/düşük olabilir.
Kalibrasyon grafiği, **tahmin edilen olasılık ile gözlenen oranın** ne kadar örtüştüğünü
gösterir.

Okuma hamlesi: **noktalar kesikli köşegenin (kusursuz kalibrasyon) üstünde mi?** Sapma,
tahminlerin sistematik kaymasını gösterir.

## Grafik ne söyledi? — Dürüst okuma

Grafikteki bin'ler **görünür (optimizm-düzeltilmemiş)** tahminlerden üretilmiştir;
optimizm-düzeltilmiş eğim/sabit ve %95 güven aralıkları `@tbl-apa-clinical` içinde
raporlanır [caption :1038]. Kaynak metinde sayı olarak görünmeyen eğim/sabit değerleri
burada **uydurulmaz**.

**Yanlış okumayı önceden düzeltelim:** *görünür kalibrasyon nihai değildir.* İç-örneklemde
model kendi verisine "fazla iyi" uyar; dürüst değerlendirme optimizm-düzeltilmiş eğim/sabittir
(tabloda). **[KEŞİFSEL]** ve dış-doğrulanmamıştır.

## Bir cümleyle

> Şekil 4.17, geniş skorun tahmin ettiği olasılıklar ile gözlenen oranların uyumunu görünür
> (iç-örneklem) düzeyde gösterir; nihai yargı için optimizm-düzeltilmiş eğim/sabit
> `@tbl-apa-clinical`'te okunmalıdır — grafik tek başına kalibrasyonu kanıtlamaz.

*Komşu öğe:* performans göstergeleri `@tbl-apa-clinical` (Tablo 4.19) aynı biçimde açılabilir.

---

# Şekil 4.18'i Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.18 = [KEŞİFSEL] Klinik model tamamlayıcıları (CART + Random Forest)**
Kanonik etiket: `@fig-clinical-cart-rf` · Kaynak: chapters/04_bulgular.qmd:1040 (caption)
· Aile: CART hata profili + RF değişken önemi.

## Bu şekil hangi soruna çözüm?

Lojistik model doğrusal bir varsayımla çalışır. Peki veriyi **doğrusal olmayan/etkileşimli**
yöntemler nasıl görüyor? Bu şekil iki tamamlayıcı bakış sunar: bir karar ağacı (CART) ve
onun topluluk hâli (Random Forest) değişken önemleri.

Okuma hamlesi: **CART çapraz-doğrulanmış hata nerede en düşük** (ağaç ne kadar karmaşık
olmalı) ve **RF'de hangi değişkenler en yüksek önemde**?

## Şekil ne söyledi? — Dürüst okuma

CART çapraz-doğrulanmış hata profili (ağaç budama/karmaşıklık seçimi) ile RF değişken önem
sıralaması bu şekilde birlikte gösterilir; sayısal önem değerleri üretilmiş artefakttadır
ve kaynak metinde sayı olarak görünmediğinden burada **uydurulmaz**.

**Yanlış okumayı önceden düzeltelim:** *değişken önemi nedensellik değildir.* Yüksek RF
önemi "bu değişken sonucu belirliyor" demek değil, "bu örneklemde sınıflandırmaya katkı
sağlıyor" demektir. **[KEŞİFSEL]**, dış-doğrulanmamış; ana çıkarım lojistik/DCA hattındadır.

## Bir cümleyle

> Şekil 4.18, klinik sınıflandırmayı doğrusal-olmayan iki yöntemle (CART hata profili + RF
> değişken önemi) tamamlar; bu bir nedensel önem sıralaması değil, keşifsel bir sağlamlık
> bakışıdır.

*Komşu öğe:* `@tbl-apa-clinical` (Tablo 4.19) aynı biçimde açılabilir.

---

# Şekil 4.19'u Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.19 = [KEŞİFSEL · İKİNCİL] Trifaktör CFA yükleme mimarisi**
Kanonik etiket: `@fig-p2-trifactor` · Kaynak: chapters/04_bulgular.qmd:1099 (caption) +
:1069-1078 (gövde) · Aile: faktör yükleme mimarisi (CFA).

## Bu şekil hangi soruna çözüm?

Aynı ebeveynlik tutumunu anne, indeks çocuk ve kardeş rapor eder. Ölçülen fark, gerçek bir
**ortak özellik (trait)** farkı mı, yoksa "kim rapor ediyor"a bağlı bir **yöntem/bilgi-veren
etkisi** mi? Trifaktör model, her maddenin varyansını ortak özellik + indeks-yöntem +
kardeş-yöntem bileşenlerine ayırır.

Okuma hamlesi: **maddeler ortak özelliğe mi, yoksa yöntem (bilgi-veren) bileşenine mi daha
çok yükleniyor?**

## Şekil ne söyledi? — Dürüst okuma

- Trifaktör CFA kabul edilebilir uyum vermiştir (CFI medyanı 0,90; RMSEA 0,05 — Hu-Bentler
  geleneğinde kabul bandı) [chapters/04_bulgular.qmd:1068].
- Şekil **madde bazında ortak özellik / indeks-yöntem / kardeş-yöntem standardize
  yüklemelerini** gösterir; caption açıkça uyarır: **model uyum indeksleri değil, yükleme
  mimarisidir** [caption :1099].
- Bununla tutarlı bilgi-verici ayrışması: anne–çocuk latent uyuşmazlık korelasyonu alt
  ölçeğe göre heterojen — reddetmede r = 0,03 (%95 GA [−0,13; 0,19], sıfıra yakın),
  karşılaştırmada r = 0,18 ([0,01; 0,35], sıfırdan ayrık) [:1075-1077]; bilgi-vereni
  çaprazlayan ağda 16 kenardan yalnız 1'i bilgi-vereni çaprazlar [:1077-1078].

**Yanlış okumayı önceden düzeltelim:** bu şekil bir **uyum kanıtı değildir** (uyum ayrı
raporlanır); yüksek yöntem yüklemesi, farkın önemli bir kısmının "kim rapor ediyor"dan
gelebileceğini gösterir — yani bilgi-veren ayrışması bir hata değil, role özgü geçerli
bilgidir. **[KEŞİFSEL · İKİNCİL].**

## Bir cümleyle

> Şekil 4.19, ebeveynlik maddelerinin varyansını ortak özellik ile bilgi-verene özgü yöntem
> bileşenlerine ayırarak, anne–çocuk ayrışmasının (özellikle reddetmede r ≈ 0,03) önemli
> ölçüde yöntem/role bağlı olduğunu gösteren bir yükleme mimarisidir — bir model-uyum
> grafiği değildir.

*Komşu öğe:* taban-duyarlı IRT `@fig-p2-floor-irt` (Şekil 4.20) aynı biçimde açılabilir.

---

# Şekil 4.20'yi Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.20 = [KEŞİFSEL · İKİNCİL] Taban-duyarlı IRT latent yetenek (θ) grup farkları**
Kanonik etiket: `@fig-p2-floor-irt` · Kaynak: chapters/04_bulgular.qmd:1101 (caption) +
:1080-1092 (gövde) · Aile: IRT latent yetenek (θ) farkı.

## Bu şekil hangi soruna çözüm?

Reddetme maddeleri **tabana yığılır** (çoğu düşük puan verir); ham toplam puan bu tavanı/tabanı
kötü ölçer. Dereceli-yanıt madde-yanıt kuramı (GRM), tabana duyarlı biçimde her bireye bir
**latent yetenek (θ)** atar ve grup farkını bu latent ölçekte gösterir.

Okuma hamlesi: **θ dağılımları tabanda mı yığılmış, ve latent grup farkı manifest (ham)
farktan büyük mü?**

## Şekil ne söyledi? — Dürüst bilanço

Taban-duyarlı GRM'de indeks çocukta latent θ grup farkları **manifest ortalama farklardan
büyüktür:** reddetme için latent d = 0,37, aşırı koruma için latent d = 0,54
[chapters/04_bulgular.qmd:1080-1081]. Yani taban etkisi, ham puanda farkı **küçük
gösteriyordu**; latent ölçekte fark daha belirgin.

**Yanlış okumayı önceden düzeltelim — en kritik karışıklık:** bu latent d, birincil hattaki
GRM katsayısıyla (β = 0,14 SD) **aynı şey değildir ve karıştırılmamalıdır.**
- **Birincil β = 0,14 SD:** beş kovaryat + aile rastgele etkisiyle **ayarlanmış** çok düzeyli
  regresyon katsayısı [:1082-1085].
- **Latent d = 0,37 / 0,54:** **kovaryat ayarı olmaksızın** iki-grup ham ortalama farkının
  havuzlanmış θ SD'sine bölünmesi [:1085-1088].
İki değer aynı örneklemde tutarlıdır; fark kovaryat ayarı + farklı payda + farklı latent
yoğunluk varsayımından gelir. Latent θ ile manifest fark karşılaştırmasının yorumu bilinçle
**Tartışma'ya bırakılmıştır** [:1090-1091]. **[KEŞİFSEL · İKİNCİL].**

## Bir cümleyle

> Şekil 4.20, taban etkisine duyarlı IRT ile ölçüldüğünde reddetme/aşırı koruma latent grup
> farklarının (d = 0,37 / 0,54) ham puan farklarından büyük çıktığını gösterir; ancak bu
> ayarsız latent-d, birincil hattaki kovaryat-ayarlı β = 0,14 SD ile **farklı bir hedef
> parametredir** ve onunla karıştırılmamalıdır.

*Komşu öğe:* trifaktör mimari `@fig-p2-trifactor` (Şekil 4.19) aynı biçimde açılabilir.

---

# Şekil 4.21'i Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.21 = [KEŞİFSEL · İKİNCİL] H1 çocuk algısı çoklu-evren spesifikasyon eğrisi**
Kanonik etiket: `@fig-p2-h1-spec` · Kaynak: chapters/04_bulgular.qmd:1124 (caption) +
:1105-1112 (gövde) · Aile: spesifikasyon eğrisi (çoklu-evren).

## Bu eğri hangi soruna çözüm?

Bir bulgu, araştırmacının analitik seçimlerine (hangi kovaryat, hangi yöntem, hangi alt
örneklem) bağlı olabilir. Tek bir spesifikasyona dayanan sonuç kırılgan olabilir.
Çoklu-evren (multiverse) çözümlemesi, makul tüm seçim birleşimlerini kurup etkinin
**seçimler boyunca ne kadar sağlam** kaldığını gösterir.

Okuma hamlesi: **etki, spesifikasyonlar boyunca yönünü/işaretini koruyor mu?** Bu bir
**dağılım**dır — tek bir p değeri değil.

## Eğri ne söyledi? — Kanıt

Dört EMBU-C alt ölçeği ayrı estimand olduğundan **ayrı panellerde**; birleşik tek eğri ya
da tek global test **üretilmez** [caption :1124]. Alt ölçeklere göre anlamlı spesifikasyon
oranı [chapters/04_bulgular.qmd:1107-1112]:

| Alt ölçek | Anlamlı spec oranı | Yorum |
|---|---|---|
| **Reddetme** (birincil) | %100 (25 spec, medyan β = 0,12) | seçimlere karşı sağlam ✓ |
| Aşırı koruma | %100 | sağlam ✓ |
| Sıcaklık | %100 | frekansçı olarak sağlam ⚠️ |
| Karşılaştırma | %3 | kırılgan ❌ |

**Yanlış okumayı önceden düzeltelim — iki nokta:**
- *Panelleri tek eğride birleştirme;* estimand'lar farklı yapılar ve farklı sıfır
  hipotezleridir.
- *Sıcaklık %100'ü, "sıcaklık sağlam bulgu" demek değildir.* Bu **frekansçı** sağlamlıktır;
  doğrulayıcı Bayesçi hat (Şekil 4.7) sıcaklık için H0 lehine kanıt verdiğinden çerçeveler
  ayrışır ve sıcaklık genel olarak sağlam sayılmaz. **[KEŞİFSEL · İKİNCİL].**

## Bir cümleyle

> Şekil 4.21, H1 reddetme bulgusunun analitik seçimlere karşı sağlam olduğunu (25
> spesifikasyonun %100'ü anlamlı, medyan β = 0,12) alt ölçek-panelli bir dağılım olarak
> gösterir; karşılaştırma kırılgandır (%3) ve estimand'lar tek eğride birleştirilmez.

*Komşu öğe:* birincil orman grafiği `@fig-h1-forest` (Şekil 4.7) aynı biçimde açılabilir.

---

# Şekil 4.22'yi Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.22 = [KEŞİFSEL · İKİNCİL] Referans etki-büyüklüğü grafiği (dış literatürle kıyas)**
Kanonik etiket: `@fig-p2-meta-forest` · Kaynak: chapters/04_bulgular.qmd:1126 (caption) +
:1113-1120 (gövde) · Aile: referans orman grafiği (biçimsel meta-analiz *değil*).

## Bu grafik hangi soruna çözüm?

Bu çalışmanın etki büyüklükleri, alandaki dış literatürün büyüklük aralığına göre **nerede
duruyor**? Grafik, bu çalışmanın dört EMBU-C etkisini dört dış referans çalışmasıyla yan
yana koyar.

Okuma hamlesi: **bu çalışmanın noktaları dış literatürün büyüklük bandıyla aynı yön ve
aralıkta mı?** — yön/büyüklük *bandı* kıyası için, biçimsel havuzlama için değil.

## Grafik ne söyledi? — Dürüst okuma

- Bu çalışmanın dört EMBU-C etkisi (iki-grup Hedges g ≈ **0,21–0,36**), dış çalışmaların
  büyüklük bandıyla (**−0,16 ile 0,40**) kabaca aynı yön ve aralıkta yer alır
  [chapters/04_bulgular.qmd:1118-1119].
- Dış çalışmalar: Pinquart 2013 (kronik hastalık ebeveynliği), Pinquart 2018 (ebeveyn
  stresi), Lovejoy 2000 (maternal depresyon), Vermaes 2012 (kardeş etkisi) [:1113-1115].
- Reddetme sinyali dağılımsal modellerde üst kuyrukta güçlenir: kuantil τ = 0,75 için
  β = 0,25 [0,12; 0,38]; beta regresyonda β = 0,46 [0,29; 0,64] [:1119].

**Yanlış okumayı önceden düzeltelim — bu bir meta-analiz DEĞİLDİR.** Farklı yapılar
ölçüldüğünden ortak-estimand'lı **havuzlama yapılmamış**; havuzlanmış elmas/dikey çizgi
**bilinçle gösterilmemiştir**. Noktaların özgün metrikleri farklıdır (Hedges g / Cohen d /
r→d) ve her noktanın yanında etiketlidir. Panel yalnız **betimsel konumlandırma** için
okunur. **[KEŞİFSEL · İKİNCİL].**

## Bir cümleyle

> Şekil 4.22, bu çalışmanın dört EMBU-C etkisini (Hedges g ≈ 0,21–0,36) dış literatürün
> büyüklük bandına (−0,16 ile 0,40) betimsel olarak konumlandırır; farklı yapılar ölçüldüğü
> için bilinçle havuzlama yapılmamış bir referans grafiğidir, biçimsel bir meta-analiz
> değildir.

*Komşu öğe:* çoklu-evren eğrisi `@fig-p2-h1-spec` (Şekil 4.21) aynı biçimde açılabilir.

---

# Şekil 4.23'ü Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.23 = [KEŞİFSEL · İKİNCİL] Genişletilmiş klinik model net fayda ısı haritası**
Kanonik etiket: `@fig-p2-dca-heatmap` · Kaynak: chapters/04_bulgular.qmd:1148 (caption) +
:1128-1140 (gövde) · Aile: ısı haritası (DCA duyarlılık ızgarası).

## Bu harita hangi soruna çözüm?

Standart karar eğrisi (Şekil 4.16) net faydayı yalnız **eşik olasılığına** göre verir. Peki
yanlış-pozitif zararını daha ağır tartarsak (farklı maliyet oranları) fayda nasıl değişir?
Isı haritası, net faydayı **eşik × maliyet-oranı** ızgarasında gösterir.

Okuma hamlesi: **hangi eşik × maliyet-oranı hücrelerinde net fayda pozitif?** Ve
**c = 1 satırı** standart DCA'dır; onu esas al.

## Harita ne söyledi? — Dürüst bilanço

- Genişletilmiş modelin ayrım gücü **AUC = 0,70**; 0,05 eşiğinde ham net fayda 0,23
  (maliyet oranı c = 1) ve standardize net fayda **sNB = 0,86** (sNB = ham NB / prevalans;
  prevalans = 0,27) [chapters/04_bulgular.qmd:1133-1135].
- Formül: NB = TP/n − (FP/n)·c·[p_t/(1−p_t)]. **c = 1 satırı** Vickers-Elkin standart
  DCA'ya birebir indirgenir; **c > 1 satırları** yalnız yanlış-pozitif zararının daha ağır
  tartıldığı **keşifsel duyarlılık** senaryolarıdır ve standart DCA'nın yerine geçmez
  [caption :1148; :1135-1139].

**Yanlış okumayı önceden düzeltelim — kritik dürüstlük noktası:** yordayıcılar (EMBU-P) ile
sınıflanan sonuç (Beck) **aynı anne tarafından aynı oturumda** öz-bildirimle toplandığından,
gözlenen ayrım gücünün bir bölümü bağımsız yordama değeri değil **ortak-yöntem varyansını**
yansıtıyor olabilir [:1128-1132]. Ayrıca kesitsel eşzamanlı sınıflandırmadır (ileriye dönük
yordama değil) ve **[KEŞİFSEL · İKİNCİL]**dir.

## Bir cümleyle

> Şekil 4.23, genişletilmiş modelin net faydasını eşik × maliyet-oranı ızgarasında gösterir
> (standart c = 1 satırında AUC = 0,70, 0,05 eşiğinde sNB = 0,86); ancak yordayıcı ile sonuç
> aynı bilgi-veren tarafından toplandığından ayrım gücünün bir kısmı ortak-yöntem varyansı
> olabilir ve c > 1 satırları yalnız keşifsel duyarlılıktır.

*Komşu öğe:* standart karar eğrisi `@fig-clinical-dca` (Şekil 4.16) aynı biçimde açılabilir.

---

# Şekil 4.24'ü Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.24 = [KEŞİFSEL · İKİNCİL] Diferansiyel ebeveynlik (PDT) yön ve etki büyüklüğü profili**
Kanonik etiket: `@fig-expl-pdt` · Kaynak: chapters/04_bulgular.qmd:1168 (caption) +
:1150-1158 (gövde) · Aile: işaretli etki büyüklüğü profili.

## Bu şekil hangi soruna çözüm?

Anne, aynı ailedeki iki çocuğa (indeks vs kardeş) **farklı mı** davranıyor? Diferansiyel
ebeveynlik testi (PDT), aile içi yön farkını dört EMBU boyutunda ölçer.

Okuma hamlesi: **her alt ölçekte işaretli etki sıfırın hangi yanında ve ne büyüklükte?**

## Şekil ne söyledi? — Dürüst bilanço

Aile içi yön testi, dört EMBU alt ölçeği işaretli d [chapters/04_bulgular.qmd:1152-1154]:

| Alt ölçek | d | Holm sonrası |
|---|---|---|
| Sıcaklık | −0,08 | anlamsız |
| Aşırı koruma | +0,15 | anlamsız |
| Reddetme | +0,03 | anlamsız |
| Karşılaştırma | +0,01 | anlamsız |

**16 karşılaştırmanın hiçbiri Holm düzeltmesi sonrası anlamlı değildir** [:1150-1151].

**Yanlış okumayı önceden düzeltelim:** ayrı bir kayırma (favoritism) kanalında DM grubunda
indeks çocuğa baba kayırması **düzeltilmemiş** düzeyde d = −0,27 ([−0,52; −0,01]; p = 0,039)
gözlenir; ama bu kontrast **bu şeklin dört alt ölçek profiline dâhil değildir** ve
düzeltilmemiştir [:1155-1158] — figürden okunmamalıdır. **[KEŞİFSEL · İKİNCİL].**

## Bir cümleyle

> Şekil 4.24, annenin iki çocuğa yönelik dört boyuttaki yön farkını işaretli etki büyüklüğü
> olarak gösterir; dört etkinin (ve 16 karşılaştırmanın) hiçbiri Holm sonrası anlamlı
> değildir — ayrı çözümlenen baba-kayırması sinyali (düzeltilmemiş d = −0,27) bu profilin
> dışındadır.

*Komşu öğe:* anne komorbidite ilişkisi `@fig-expl-comorbidity` (Şekil 4.25) aynı biçimde
açılabilir.

---

# Şekil 4.25'i Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.25 = [KEŞİFSEL · İKİNCİL] Anne komorbiditesi ve depresif belirti ilişkisi**
Kanonik etiket: `@fig-expl-comorbidity` · Kaynak: chapters/04_bulgular.qmd:1170 (caption) +
:1160-1165 (gövde) · Aile: bağlamsal ilişki görseli.

## Bu şekil hangi soruna çözüm?

Annenin başka bir sağlık komorbiditesi taşıması, depresif belirti düzeyiyle ilişkili mi?
Ve gruplar antidepresan kullanımı açısından farklı mı? Bu bağlamsal katman, anne ruh
sağlığı çevresini betimler.

Okuma hamlesi: **komorbidite ile Beck puanı arasındaki ilişki ne yönde/büyüklükte, ve
gruplar arası kompozisyon farkı var mı?**

## Şekil ne söyledi? — Dürüst bilanço

- Komorbidite, Beck puanıyla **d = 0,29** düzeyinde ilişkilidir — ama Holm düzeltmesi
  sonrası **anlamsızdır** [chapters/04_bulgular.qmd:1161-1162].
- Antidepresan kullanımı gruplar arası belirgin farklıdır: DM %29,2, kontrol %9,1
  (χ²(1) = 14,45; p < 0,001; Cramér V = 0,25) [:1162-1164].

**Yanlış okumayı önceden düzeltelim:** d = 0,29 keşifsel ve Holm-anlamsızdır — "komorbidite
depresyonu artırıyor" diye okunamaz. Antidepresan farkı ise anlamlıdır, ama bu bir **grup
kompozisyon** gerçeğidir (Şekil 4.2'de neden antidepresanın aracı düğüm olarak ele
alındığını hatırlatır), bir etki büyüklüğü değil. **[KEŞİFSEL · İKİNCİL].**

## Bir cümleyle

> Şekil 4.25, anne komorbiditesinin depresif belirtiyle yalnız zayıf ve Holm-anlamsız bir
> ilişki (d = 0,29) gösterdiğini, buna karşılık antidepresan kullanımının DM grubunda
> belirgin biçimde daha yüksek olduğunu (%29,2'ye %9,1; Cramér V = 0,25) betimler.

*Komşu öğe:* nedensel harita `@fig-causal-dag` (Şekil 4.2) antidepresanın neden aracı
düğüm olduğunu gösterir.

---

# Şekil 4.26'yı Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.26 = Çoklu evren spesifikasyon eğrisi (birincil sağlamlık)**
Kanonik etiket: `@fig-specification-curve` · Kaynak: chapters/04_bulgular.qmd:1350 (caption)
+ :1298-1303 (gövde) · Aile: spesifikasyon eğrisi (çoklu-evren).

## Bu eğri hangi soruna çözüm?

Birincil bir bulgu, tek bir analiz seçimine bağlı olmamalı. Çoklu-evren çözümlemesi, alt
ölçek/kovaryat/yöntem/alt örneklem seçimlerinin makul tüm birleşimlerini kurar ve etkinin
seçimler boyunca dağılımını gösterir. (Bu, 4.21'in İKİNCİL H1-özel eğrisinden farklı olarak
birincil H1–H4 sağlamlık katmanıdır.)

Okuma hamlesi: **spesifikasyonlar büyüklüğe göre sıralandığında etki hangi yönde toplanıyor,
ve renkle işaretli nominal anlamlılık örüntüsü ne?** Bu bir **dağılım**dır, tek test değil.

## Eğri ne söyledi? — Kanıt (H3 anne öz-bildirim örneği)

- Spesifikasyonlar Cohen d büyüklüğüne göre sıralı; nominal anlamlılık renkle gösterilir
  [caption :1350].
- Anne öz-bildirim (H3) tarafında medyan d küçük ve pozitif kalır (aşırı koruma 0,10,
  karşılaştırma 0,10) [chapters/04_bulgular.qmd:1298-1301].
- **Permütasyon temelli test (n = 5000) anlamlılık üretmemiştir** [:1301-1302] — yani H3'ün
  null bulgusu analitik seçimlere karşı sağlamdır.

**Yanlış okumayı önceden düzeltelim:** *renkle işaretli nominal anlamlılık, çokluk-
düzeltilmiş anlamlılık değildir.* Dürüst global yargı, tek tek renkli noktalar değil,
permütasyon testidir (burada anlamsız). Bir "anlamlı" spesifikasyon görmek, bulgunun
sağlam olduğu anlamına gelmez.

## Bir cümleyle

> Şekil 4.26, birincil etkilerin analitik seçimler boyunca dağılımını büyüklüğe göre sıralı
> gösterir; anne öz-bildiriminde (H3) medyan etkiler küçük kalır ve permütasyon testi
> (n = 5000) anlamlılık üretmez — yani null bulgu spesifikasyon seçimlerine karşı sağlamdır.

*Komşu öğe:* robustluk özeti `@tbl-apa-robustness` (Tablo 4.21) aynı biçimde açılabilir.

---

# Şekil 4.27'yi Anlamak — Basitçe, Ama Eksiksiz

**Şekil 4.27 = Ölçülmemiş karıştırıcı duyarlılık konturu (sensemakr)**
Kanonik etiket: `@fig-sensemakr-contour` · Kaynak: chapters/04_bulgular.qmd:1352 (caption)
+ :1307-1312 (gövde) · Aile: duyarlılık konturu (sensemakr).

## Bu şekil hangi soruna çözüm?

Gözlemsel tasarımda her karıştırıcıyı ölçemeyiz; **ölçülmemiş** bir üçüncü değişken hâlâ
sonucu değiştiriyor olabilir. Bu şekil, "bir gizli değişkenin bulguyu değiştirebilmek için
**ne kadar güçlü** olması gerektiğini" niceler — sonucun gizli karıştırıcıya karşı ne kadar
dayanıklı olduğunu gösterir.

Okuma hamlesi: **bulguyu sıfırlamak/değiştirmek için gizli karıştırıcının maruziyet ve
sonuçla ilişkisi ne kadar güçlü olmalı?** Yüksek eşik = sağlam; düşük eşik = kırılgan.

## Şekil ne söyledi? — Dürüst bilanço

H3 birincil tahminleri için [chapters/04_bulgular.qmd:1308-1311]:

| Ölçüt | Değer | Yorum |
|---|---|---|
| Robustness Value RV_q | 0,04–0,08 | düşük ⚠️ |
| E-değeri | 1,36–1,59 | düşük ⚠️ |

Bu **düşük** değerler, sonuçların böyle bir gizli değişkene karşı yalnız **zayıf-orta**
düzeyde dayanıklı olduğunu gösterir; noktalar EMBU-P alt ölçekleri için grup (T1DM
maruziyeti) kısmi R² ile RV_q kesişimini, arka plan konturları ortak karıştırıcı gücünü
gösterir [caption :1352].

**Yanlış okumayı önceden düzeltelim:**
- *"treatment" ekseni bir müdahale değildir.* sensemakr çerçevesinin "treatment"ı bu
  gözlemsel tasarımda **grup/maruziyet göstergesidir** [caption :1352] — nedensellik iddiası
  taşımaz.
- Düşük RV/E "sonuç yanlış" demek değil; "gizli bir karıştırıcı görece kolay değiştirebilir,
  bu yüzden temkinli oku" demektir. (H3 birincil etkileri zaten sıfıra yakın olduğundan bu
  duyarlılık, bulguları güçlü bir nedensel iddiaya dönüştürmeye karşı bir frendir.)

## Bir cümleyle

> Şekil 4.27, H3 tahminlerinin ölçülmemiş bir karıştırıcıya karşı yalnız zayıf-orta düzeyde
> dayanıklı olduğunu (RV_q = 0,04–0,08; E-değeri 1,36–1,59) gösterir; "treatment" ekseni bir
> müdahaleyi değil grup/maruziyet göstergesini temsil eder, dolayısıyla sonuçlar nedensel
> değil, gizli karıştırıcıya duyarlı koşullu ilişkiler olarak okunmalıdır.

*Komşu öğe:* duyarlılık özeti `@tbl-apa-sensitivity` (Tablo 4.22) ve nedensel harita
`@fig-causal-dag` (Şekil 4.2) aynı biçimde açılabilir.

---

## Notlar

- Bu belge Bulgular bölümünün **27 şeklinin tamamını (Şekil 4.1–4.27)** kapsar.
- Tüm sayılar chapters/04_bulgular.qmd ve chapters/03_gerec_ve_yontem.qmd kaynaklarından
  birebir alınmıştır; ondalık-virgül biçimi korunmuştur.
- Bazı görsellerin (4.4/4.5/4.6/4.10 hücre-düzeyi; 4.13 kenar; 4.14 NCT p; 4.15 AUC;
  4.17 eğim/sabit; 4.18 RF önem) ayrıntılı değerleri gitignored `outputs/` artefaktlarında
  ve inline-R ile üretilen cümlelerde tutulduğundan, kaynak metinde sayı olarak görünmeyen
  bu değerler bilinçle **uydurulmamıştır** (sayısal bütünlük kaidesi, AGENTS.md); metinde
  raporlanan özet değerler kullanılmış, gerisi ilgili tabloya yönlendirilmiştir.
- Katman etiketleri: **4.1–4.11 ve 4.26–4.27 birincil**; **4.12–4.18 [KEŞİFSEL]**;
  **4.19–4.25 [KEŞİFSEL · İKİNCİL]**. Keşifsel/ikincil şekiller doğrulayıcı hipotez sonucu
  gibi yorumlanmaz.
- Sık karışan ayrımlar: 4.20 latent d (0,37/0,54) ↔ birincil β = 0,14 SD **farklı hedef
  parametre**; 4.21/4.26 spec eğrileri **dağılımdır, tek test değildir**; 4.3 denge ↔ 4.4
  örtüşme **ayrı sorular**; 4.23'te **ortak-yöntem varyansı** uyarısı; 4.22 biçimsel
  meta-analiz **değildir**; 4.27 "treatment" ekseni **müdahale değil** grup göstergesidir.
- Şekil numaralandırması bölüm-görelidir (04_bulgular = 4.N); bazı eski şekiller
  çıkarıldığından etiket→numara sırası `#| label:`/`{#fig-` görünme sırasına göredir.
- IDE'de görünen markdown-lint uyarıları (MD060 tablo boşluğu, MD032 liste-etrafı boş satır,
  `[...]` "link" uyarıları) yalnız **stil/kozmetik**tir; içerik/sayısal doğruluk etkilenmez.
- Bu belge yalnız var olanı izah eder; hiçbir analizi/sonucu değiştirmez.
