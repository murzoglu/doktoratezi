# Kanonik Klinik-Karşılık Sözlüğü — klinisyen-diline-uyarlama (Faz 0 pre-register)

Bu sözlük, `03`/`04`/`05` bölümlerinin klinisyen-diline uyarlanmasında **her metodolojik/
psikometrik terimin tek klinik karşılığını** sabitler. Amaç: bölümler-arası terim tutarlılığını
**inşa gereği** sağlamak — her turun harness spec'inde `glossary` alanına bu sözlükten beslenir
(harness yalnız o paragrafta GEÇEN terimi modele verir).

**Kaynak:** `.claude/skills/klinisyen-diline-uyarlama/references/hedef-kitle-personasi.md`
(vetted klinik-karşılık tablosu) + 3 bölümün deterministik jargon envanteri (grep, ilk-geçiş) +
`docs/tez-kilavuz/terim-sozlugu.yaml` (kanonik biçim/yasak-varyant uyumu).

**Değişmezlik:** Bu sözlük yalnız **terim-dilini** düzenler; hiçbir sayı/istatistik/yön/atıf
kararını etkilemez. Gloss ≠ mutasyon: metriğin tanımı açıklanır; **bu sonucun** büyüklük/yön
etiketi kaynakta yoksa eklenmez (F1/F2).

## Kullanım kuralları (harness register'ıyla uyumlu)

1. **İlk geçişte** gloss: klinik karşılık + parantezde özgün ad; sonraki geçişlerde yalın ad.
2. **Yalnız yabancı** psikometrik model glosslanır. Klinisyenin bildiği (p, %95 GA, medyan/ÇAA,
   OR/RR, duyarlılık/özgüllük, karıştırıcı) **glosslanmaz, tanımlanmaz** (İSTATİSTİK-META yasağı).
3. **Formül metne girmez** → "(formülizasyon/katsayı tanımları teknik ekte)"; formül **teknik eke**
   (Ekler bölümü) taşınır. Sonuç değerleri (p, katsayı, r) metinde kalır.
4. **latent-anlamlı "gizli" YASAK** → `latent` (terim-sozlugu A1). "gizli" yalnız confounder/
   gizlilik/gizli-algı anlamında muaf; latent düzey/değişken/uyum bağlamında **latent** yazılır.
5. **Kanonik biçim** (terim-sozlugu): `latent` (gizil değil), `aşırı koruma` (A2), `reddetme`/
   `reddedilme` (A3) — gloss metni bu biçimleri kullanır.
6. Tabloda olmayan terim çıkarsa: klinik karşılığını üret, kullan, **bu sözlüğe + journal
   backlog'una ekle** (tez-geneli tek karşılık).

---

## 1. Denge ve nedensel çıkarım (ağırlıkla 03, 04)

| Terim (özgün ad) | Klinik karşılık (ilk-geçiş glossu) | Geçiş |
|---|---|---|
| SMD (standardize ortalama fark) | iki grup farkının ortak cetvele vurulmuş hâli; sıfıra yakın = benzer (etki-büyüklüğü gibi) | 03·04·05 |
| latent SES kompoziti | eğitim+meslek+maddi göstergeyi tek bir latent "sosyoekonomik düzey" ölçüsünde birleştirme | 04 |
| eğilim skoru (propensity) | bir ailenin ilgili gruba (ör. DM) düşme olasılığı; gözlemsel veriyi dengelemek için | 03·04·05 |
| IPTW (ters-olasılık ağırlıklandırma) | eğilim skoruna göre ağırlık verip grupları "sanki denk dağıtılmış gibi" kıyaslanır kılma | 03·04 |
| ortak destek (common support) | grupların örtüştüğü, gerçekten karşılaştırılabilir olduğu aralık | 04·05 |
| yönlü asiklik graf (DAG) | değişkenler arası neden-sonuç yönlerini gösteren ok şeması; hangi karıştırıcının düzeltileceğini belirler | 03·04·05 |
| E-değeri (E-value) | gözlenen ilişkiyi silmek için ölçülmemiş bir karıştırıcının ne kadar güçlü olması gerektiği (sağlamlık) | 03·04·05 |

## 2. Ölçüm ve psikometri (ağırlıkla 03)

| Terim | Klinik karşılık | Geçiş |
|---|---|---|
| ICC (sınıf-içi korelasyon) | aynı aileden ölçümlerin ne kadar benzediği; aile-içi bağımlılık ("kardeşler bağımsız değil") | 03·04·05 |
| çok düzeyli model | iç içe veriyi (çocuk-içinde-aile) aile-içi benzerliği hesaba katarak analiz eden model | 03·04·05 |
| Cronbach α / McDonald ω | ölçek maddelerinin aynı şeyi ne kadar tutarlı ölçtüğü (ölçeğin güvenilirliği) | 03·04·05 |
| CFA / SEM | gözlenen sorulardan latent bir kavramı (ör. reddetme algısı) ölçen + kavramlar arası ilişkiyi test eden model | 03·04·05 |
| ESEM (keşifsel yapısal eşitlik) | CFA'nın "her madde tek faktör" katılığını gevşeten, maddelerin birden çok faktöre yüklenmesine izin veren melez ölçüm modeli | 04·05 |
| uyum indeksi (CFI/RMSEA/SRMR) | modelin veriye ne kadar uyduğunu özetleyen not (gelenek eşikleri, yasa değil) | 03·04·05 |
| ölçüm değişmezliği (invariance) | aynı ölçeğin farklı gruplarda aynı şeyi ölçtüğünün kanıtı; olmadan grup kıyası yanıltıcı | 03·04·05 |
| IRT / GRM | her sorunun zorluk + ayırt ediciliğini modelleyen ölçüm yaklaşımı | 03·04·05 |
| bifaktör | bir genel faktör + ondan bağımsız özgül faktörleri aynı anda modelleme | 03·04·05 |
| taban etkisi (floor) | puanların alt sınıra yığılması; ortalama-temelli analizi zayıflatır, madde-yanıt kuramı bu yığılmayı hesaba katar | 03·04·05 |
| güç analizi / örneklem büyüklüğü | belirli bir etkiyi saptayabilmek için gereken örneklem ve istatistiksel güç hesabı | 03·04·05 |

## 3. Latent birey-merkezli ve ağ (ağırlıkla 04)

| Terim | Klinik karşılık | Geçiş |
|---|---|---|
| LPA / LCA (latent profil/sınıf) | bireyleri gözlenmeyen alt-gruplara (profillere) ayırma; "veriden fenotip çıkarma" gibi | 03·04·05 |
| ağ analizi (GGM) / merkeziyet | değişkenleri düğüm, ilişkileri kenar yapan ağ; merkezî düğüm en bağlantılı | 03·04·05 |
| aracılık (mediation) | bir etkinin ara bir değişken üzerinden dolaylı iletilmesi (A→ara→B) | 03·04·05 |
| moderatör (düzenleyici) | bir ilişkinin gücünü/yönünü değiştiren üçüncü değişken (etkileşim) | 03·04·05 |

## 4. Diadik uyum (anne–çocuk) (ağırlıkla 04)

| Terim | Klinik karşılık | Geçiş |
|---|---|---|
| RSA / yanıt yüzeyi (Edwards-Parry) | anne ve çocuk puanının uyum/uyumsuzluğunun bir çıktıyla ilişkisini üç boyutlu bir yüzeyle modelleme (mutlak değil işaret/örüntü yorumlanır) | 03·04·05 |
| ortak yazgı modeli (common fate) | anne ve çocuğun paylaştığı ortak "aile algısı" bileşenini ayıran model | 03·04 |
| APIM / latent düad (Olsen–Kenny) | çift verisinde kişinin kendi ve partnerinin etkisini ayıran, ölçüm hatasını latent düzeyde ayıklayan model | 03·04·05 |
| k-katsayısı (Kenny k) | kişinin kendi algısının partnerinkine oranı (algı baskınlığı/dengesi) | 03·04 |
| Bland–Altman | iki ölçümün/bildirenin mutlak uyumu (fark ± sınırlar); yüksek korelasyon ≠ uyum | 03·04·05 |
| konkordans | uyum, örtüşme | 03·04·05 |
| raporcular arası uyum (informant) | aynı olguyu farklı bildirenlerin (anne/çocuk) ne kadar örtüşük raporladığı | 03·04·05 |

## 5. Bayes, robustluk, eksik veri, tanı-model (03/04/05)

| Terim | Klinik karşılık | Geçiş |
|---|---|---|
| Bayes faktörü (BF) / ROPE | verinin hangi hipotezi ne kadar desteklediğinin oranı / pratik-olarak-sıfır bandı | 03·04·05 |
| multiverse / spesifikasyon eğrisi | makul tüm analiz seçeneklerini birden koşup sonucun sağlamlığını görme | 03·04·05 |
| TOST / eşdeğerlik | "fark yok"u değil "fark önemsiz küçük"ü test eden yaklaşım | 03·04·05 |
| FIML / çoklu atama (MI) | eksik veriyi silmeden, tüm bilgiyi kullanarak analiz etme | 03·04·05 |
| AUC / kalibrasyon / DCA | risk modelinin ayırt ediciliği / tahmin doğruluğu / klinik yararı (optimizm-düzeltilmiş = aşırı-iyimserlikten arındırılmış) | 03·04·05 |
| FDR | çok sayıda test yapınca yanlış-pozitifleri kontrol eden düzeltme | 03·04·05 |

---

## Kapsam notu (deterministik envanter, grep ilk-geçiş)

- **03 Gereç-Yöntem:** 31/34 terim geçiyor — en yoğun psikometri/nedensel yöntem katmanı;
  glossların **burada sabitlendiği** referans bölüm (D3/D4/D6 yoğun).
- **04 Bulgular:** 34/34 terim — tüm ailenin bulgu karşılığı; RSA/APIM/ICC/LPA/ağ burada somutlaşır.
- **05 Tartışma:** 28/34 terim — yorum katmanı; terimler 03/04'ten türetildiği için yeni gloss
  nadir (çoğu tekrar).

## Bakım

Yeni terim / karşılık değişikliği → bu dosya + `klinisyen-diline-uyarlama-journal.md` backlog.
Her dalga sonunda `terim_tutarlilik_audit.py` ile kanonik-biçim uyumu doğrulanır (latent/aşırı
koruma/reddetme yasak-varyant sıfır).
