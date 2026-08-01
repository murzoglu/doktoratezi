# Örnek: Referans-Kalite Şekil Açıklaması (Nedensel DAG)

`ornek-tablo-4-4.md` bir **tabloyu** kalibre eder; bu dosya bir **şekli** kalibre eder.
Farkı gör: bir şekilde açıklama, 5-katman akışından **önce** "öğe tipini tanı → okuma
hamlesi" adımıyla başlar (bkz. `references/gorsel-okuma-rehberi.md`). Okuma hamlesi
altyazının cömertliğinden değil, rehberden gelir.

Kaynak öğe: `chapters/04_bulgular.qmd:565` (`@fig-causal-dag`, altyazı) +
`chapters/03_gerec_ve_yontem.qmd:139` (yöntem). Verili tek sayısal çıpa: anne yaşı
SMD ≈ 0,21 [chapters/03_gerec_ve_yontem.qmd:139].

---

# Şekil 3.2'yi Anlamak — Basitçe, Ama Eksiksiz

**Şekil 3.2 = Nedensel yönlü asiklik graf (DAG) ve ayarlama stratejisi**

## Bu diyagram hangi soruna çözüm?  ← [Neden var + öğe-tipi okuma hamlesi]

Bu bir **deney değil, gözlemsel** çalışma; grupları biz rastgele atamadık. O hâlde
bulduğumuz fark diyabetten mi, yoksa grupların arka plan farklarından mı? DAG (yönlü
asiklik graf) bu ayrımı yapmak için önce **varsayımları görünür kılan bir haritadır**:

> Her düğüm bir değişken, her **ok** "şu şunu etkiler" **varsayımıdır** — veriden
> kestirilmez, analizden önce çizilir. Bir okun **yokluğu** da güçlü bir varsayımdır.

Bir DAG'ı okumanın hamlesi hep aynıdır: hangi düğüm **karıştırıcı** (kapatılacak),
hangisi **aracı** (açık bırakılacak), hangisi **seçilim** düğümü — ve bu tasarımda
etki **tanımlanabilir mi**?

## "Arka kapıları" kapatmak  ← [Somutlaştır]

A'dan B'ye giden ana yol "diyabetin etkisi"dir; ama ortak bir neden üzerinden uzanan
**arka-kapı yolları** da A ile B'yi bağlar. Temiz karşılaştırma için bu kapıları
(ortak nedenleri istatistikle sabitleyerek) kapatmak gerekir; DAG **hangilerini**
söyler.

## Düğümler üç işe ayrılır  ← [Mekanizma, kademeli]

1. **Karıştırıcılar (kapatılacak):** latent SES, kardeş yaş farkı, aile çocuk sayısı —
   hem T1DM'ye hem çocuk algısına ok gönderir; birincil modelde ayarlanır, eğilim skoru
   bunlar üzerinden kestirilir.
2. **Aracı/duyarlılık (bilerek açık):** Beck (anne depresif belirti) ve antidepresan
   kullanımı maruziyet ile ebeveynlik *arasında* durur; aracıyı ana modele koymak
   ölçmek istediğin etkinin bir parçasını görünmez kılar — bu yüzden ayrı aracılık/
   duyarlılık çözümlemesine bırakılır.
3. **Seçilim düğümü $S$:** merkez/dönem ile grup üyeliği birlikte kimin örnekleme
   *girdiğini* belirler; analiz $S=1$'e koşulludur.

*İnce nokta:* anne yaşı H1'de bilerek **konmaz** (etkisi SES/yaş farkı/aile büyüklüğü
aracılığıyla akar), ama H3/H4'te sonuç doğrudan anneye ait olduğundan **ayarlanır**.
Aynı değişkenin farklı hipotezlerde farklı muamele görmesi keyfî değil, grafiğin
dayattığı bir karardır.

## Diyagram ne söyledi? — Dürüst bilanço  ← [Kanıt + dürüstlük kapısı]

| Ne | Grafiğin verdiği | Yorum |
|---|---|---|
| Arka-kapı kümesi | SES + kardeş yaş farkı + aile çocuk sayısı | ayarlanır ✓ |
| Anne yaşı dengesi | SMD ≈ 0,21 (sınırda dengesiz) | çok-evren genişletilmiş kolunda sınanır ✓ |
| Toplam nedensel etki | $S$ üzerinde koşullanma → **nokta-tanımlanamaz** | ❌ |

En kritik satır sonuncusudur ve gizlenmez: **T1DM'nin toplam nedensel etkisi bu
tasarımda tanımlanamaz**; grup katsayıları "nedensel etki" değil, **ayarlanmış koşullu
ilişki** olarak okunur. Bir DAG'ın "işe yaraması", her zaman temiz etki üretmesi değil,
çoğu zaman **hangi etkinin üretilemeyeceğini** dürüstçe göstermesidir.

## Bir cümleyle  ← [Tek-cümle kapanış]

> Şekil 3.2, hangi karıştırıcıların kapatıldığını (SES, kardeş yaş farkı, aile çocuk
> sayısı) ve hangilerinin bilerek aracı bırakıldığını (Beck, antidepresan) görünür
> kılan varsayım haritasıdır; ama aynı harita, seçilim düğümü $S$ üzerinde koşullanma
> nedeniyle **T1DM'nin toplam nedensel etkisinin tanımlanamayacağını** belgeler.

← [Kapanış teklifi: `@fig-smd-love` (denge kazanımı), `@fig-propensity-overlap` (ortak
destek), `@fig-strobe-flow` ($S$'nin somut karşılığı) aynı biçimde açılabilir.]

---

## Bu örnekten çıkarılacak üslup dersleri

1. **Okuma hamlesi en başta.** Şekilde açıklama, 5 katmandan önce "bu bir DAG; okları
   varsayım, ok yokluğunu iddia, düğümleri role göre oku" der — bu skeleti
   `gorsel-okuma-rehberi.md` verir, altyazı değil.
2. **`← [...]` etiketleri görünmez.** Yalnız bu öğretici dosyada var; gerçek çıktıda
   okur akışı hisseder.
3. **Yön ≠ büyüklük ≠ tanımlanabilirlik.** Üçü ayrı söylenir.
4. **Dürüstlük kapısı bir şekilde de işler:** en değerli satır "yapılamayan"dır (❌).
5. **Ölçek uyumu:** DAG karmaşık olduğundan tüm katmanlar açıldı; tek çizgili bir
   histogramda 2 katman yeterdi.
