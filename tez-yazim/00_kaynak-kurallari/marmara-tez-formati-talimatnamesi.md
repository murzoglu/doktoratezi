# MARMARA TEZ FORMATI TALİMATNAMESİ (Kanonik)

Sürüm: 1.0 · 2026-07-06 · Kapsam: Marmara Üniversitesi Sağlık Bilimleri
Enstitüsü doktora tezinin **tüm biçim, bölüm, başlık, tablo/şekil, sayısal
yazım, atıf ve kaynakça** kararları.

Bu belge bir öneri değil, **tüm tez yazım süreçlerinde zorunlu uyulması gereken
kanonik format talimatnamesidir**. `chapters/*.qmd`, `thesis.qmd`, ön bölümler
ve her türetilmiş çıktı bu talimatnameye uymak zorundadır. Biçim uyuşmazlığı
bölüm finalizasyonunu bloke eder (Bölüm 12).

## 0. Kaynak otoritesi ve öncelik

Bu talimatname iki resmi Marmara kaynağından **eksiksiz** olarak çıkarılmıştır.
Her kural aşağıdaki birincil kaynaklara izlenebilir:

| Kaynak | Rol |
|---|---|
| `docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf` | Genel biçim, sayfa düzeni, başlık, tablo/şekil, özet, bölüm içeriği, kaynakça (AMA-11) ve ekler için **birincil biçim otoritesi**. |
| `docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx` | Kapak, beyan, içindekiler, listeler, özet/summary alanları, ana bölüm sırası, başlık numaralandırma düzeni, özgeçmiş ve faaliyet için **birincil şablon otoritesi**. |

**Öncelik zinciri (çakışmada):** (1) kullanıcının/danışmanın açık talimatı →
(2) resmi `docs/tez-kilavuz` dosyaları → (3) bu talimatname → (4) repo içi eski
yazım notları. Repo içinde geçen APA 7, nokta ondalık ayırıcı veya alternatif
Quarto format notları bu talimatname ile çakıştığında **resmi kılavuz üstündür**
(bkz. Bölüm 11 override notu).

Analiz, veri yapısı ve hipotez kararlarında ise repo içi kanıt ve testlenmiş
pipeline (`_targets.R`, `docs/protokol/`, `docs/analiz_planlari/`) üstündür; bu
talimatname yalnız **biçim** otoritesidir.

---

## 1. BİÇİM ve YAZIM STANDARTLARI

### 1.1. Sayfa tasarımı

- Sayfa boyutu **A4 (21 × 29,7 cm)**; teslim biçimi **PDF**.
- Sayfa arka planı **beyaz**, **tek sütun** (sütun kullanılmaz).
- Kenar boşlukları: **sol ve sağ 2,5 cm**, **üst ve alt 2 cm**. Yazılar bu
  çerçevenin dışına taşmaz.

### 1.2. Yazı, satır aralıkları ve paragraflar

- Ana metin: **Times New Roman, 12 punto, siyah, 1,5 satır aralığı**.
- İstisnalar (aşağıda ilgili bölümlerde tanımlı): başlıklar (1.3), şekil
  başlıkları (1.6), tablo başlıkları (1.7), kaynakça (Bölüm 4.1).
- **Paragraf girintisi yapılmaz.** Paragraflar arasında **6 nk** (0,5 satıra
  karşılık gelen) boşluk bırakılır.
- Satır sonlarında kelimeler **bölünmez**.
- Metin **iki yana yaslanır** (justify).
- Sayfa sonuna gelen başlık/alt başlıktan sonra **en az iki satır yazı** bulunur
  (başlık sayfa sonunda yalnız bırakılmaz).
- **Maddeleme:** yalnızca açıklamayı kolaylaştırmak için kullanılır. İşaretler
  yalnız klasik dolu yuvarlak nokta (**•**) veya tire (**–**) olabilir.
  Maddeleme **en fazla iki düzey**; ikinci düzeyin altına yeni madde açılmaz.
  (Not: metin gövdesindeki bu iki-düzey sınırı, başlık numaralandırmasından —
  Bölüm 1.3 — ayrıdır.)

### 1.3. Başlıklar

- Tez şu ana başlıklara bölünür (resmi sıra Bölüm 10'da tam listelenir): tez
  onayı, beyan, teşekkür, içindekiler, kısaltmalar, şekiller, tablolar, özet,
  summary, giriş ve amaç, genel bilgiler, gereç ve yöntem, bulgular, tartışma ve
  sonuç, kaynaklar, özgeçmiş, bilimsel faaliyetler, ekler.
- Her ana başlık **ayrı sayfadan** başlar; ana başlıktan sonra **bir satır
  boşluk** bırakılır.
- Ana ve alt başlıklar **sol satır başına** dayanır.
- Büyük harf kuralı:
  - **Ana başlıkların tamamı** büyük harf.
  - **Birinci düzey alt başlıkların** her sözcüğünün ilk harfi büyük.
  - **İkinci ve sonraki düzey alt başlıklarda** yalnız birinci sözcüğün ilk
    harfi büyük.
  - Bağlaçlar (**ve**, **ile**, **veya** vb.) her durumda küçük harf.
- Punto/kalınlık:
  - **Bölüm (ana) başlıkları: kalın (bold), 14 punto.**
  - **Diğer tüm başlıklar: kalın (bold), 12 punto.**
- Başlık sonunda **noktalama işareti bulunmaz**.
- Bir paragraf bitiminde yeni bir (alt) başlığa geçilecekse **bir satır boşluk**
  bırakılır.
- **Başlık numaralandırma düzeni** (şablon DOCX esas): ana bölümler `3.`, `4.`,
  `5.` … biçiminde; alt başlıklar ondalık hiyerarşi ile `4.1.`, `4.1.1.`,
  `4.1.1.1.` (en çok dört düzey). `GİRİŞ ve AMAÇ` ile `TARTIŞMA ve SONUÇ`
  bölümlerinde şablon **alt başlık kullanmamayı** önerir; bu bölümlerde alt
  başlık gerekiyorsa danışman/onay gerektiren taslak kararı olarak işaretlenir.
  `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM`, `BULGULAR` alt başlıkla yapılandırılabilir.

### 1.4. Anlatım ve sayısal yazım

- Dil **Türkçe**; anlatım sade, açık, Türk dil bilgisi kurallarına uygun,
  **üçüncü şahıs edilgen** (yapıldı, görüldü, bulundu vb.).
- Türkçeleştirilmemiş yabancı sözcüklerden kaçınılır.
- İmla/yazım otoritesi: **TDK Güncel Türkçe Sözlük** (sozluk.gov.tr) ve **TDK
  İmla Kılavuzu** son baskısı.
- Birimler: mümkün olduğunca **SI temel birimleri** (mol/l, mmol/l, µmol/l vb.).

**Sayısal yazım kuralları (bu hattın en sık ihlal edilen kuralı):**

- Yöntem ve bulgulara ilişkin sayısal değerler **ondalıklı** verilir.
- **Ondalık ayırıcı virgüldür** — nokta değil (örn. `62.4` değil `62,4`).
- Tanımlayıcı değerler (ortalama, yüzde) genellikle **bir ondalık basamak**
  (örn. `62,38` değil `62,4`); yalnız bilimsel açıdan anlamlı fark gerektiğinde
  ikinci basamak.
- Analitik test istatistikleri (z, t, F, χ²) ve oranlar (OR, HR, RR) **iki
  ondalık basamak** (örn. `RR: 0,65; %95 GA: 0,41-0,82`).
- **p-değerleri:** virgül öncesinde **mutlaka `0`**, virgülden sonra **üç
  basamak** (örn. `p=0,038`). Çok küçük değerler yuvarlanıp `<` ile: `p<0,001`.
- Ondalık virgülden önce daima sıfır bulunur (`0,018`).

### 1.5. Kısaltmalar

- Birden fazla sözcükten oluşan ve **sık kullanılan** terimler baş harflerle
  kısaltılır; **Kısaltmalar** bölümünde **alfabetik** sıralanır.
- Tez içinde az tekrar eden sözcük kısaltılmaz.
- İlk geçtiği yerde açık ad + parantez içinde kısaltma; sonraki her yerde yalnız
  kısaltma.
- Türkçe karşılığı yerleşik olmayan, evrensel kavramlarda Türkçe karşılığın
  ardından **italik orijinal** yazılır.
- TÜBİTAK, AIDS, HIV, ACTH gibi yerleşik standart kısaltmalar açık ad
  yazılmadan kullanılabilir.
- Yaygın/temel birim kısaltmaları (cm, kg, m, µmol/l, ng/dl) özel gerekçe
  olmadıkça açık yazılmaz ve Kısaltmalar bölümüne eklenmez.

### 1.6. Şekiller

- Tablo dışındaki her grafik, çizim, çizelge, diyagram, resim, şema = **Şekil**.
- Başka kaynaktan hazırlanan şekiller atıf yapılarak ve **Türkçeleştirilerek**
  kullanılır (örn. *Şekil 1. Albüminin yapı ve fonksiyonları (Balack ve ark.,
  2011'den yararlanılarak hazırlanmıştır)*).
- Fotoğrafta katılımcı varsa **kimlik deşifre edilmez**; yazılı izin + yüz
  anonimleştirme zorunlu. (Bu tezde KVKK gereği katılımcı fotoğrafı kullanılmaz.)
- Metinde ilk geçtiği yerde ilk harfi büyük (Şekil 3a, Şekil 8).
- Şekil, atıf yapılan metnin bulunduğu veya takip eden sayfada; metin akışı
  kesilmeden, gereksiz boşluk oluşturulmadan yerleştirilir.
- Metin bloğundan dar şekiller **ortalanır**.
- Numaralandırma **Arap rakamı**, geçiş sırasına göre; alt gruplar Şekil 1,
  Şekil 1a biçiminde.
- **Şekil başlığı şeklin ALT kenarının bir satır altına**, sol alt köşe
  hizasından yazılır. **12 punto, tek satır aralığı**.
- `Şekil 1.`, `Şekil 2a.` etiketleri **kalın**, devamı normal punto. Başlık
  kısa ve öz; sonrasında bir satır boşluk.

### 1.7. Tablolar

- Metinde ilk geçtiği yerde ilk harfi büyük (Tablo 1, Tablo 3).
- Tablo, atıf yapılan veya takip eden sayfada; genişliği **metin bloğu ile
  aynı**; yatay/dikey çerçeve dışına taşmaz.
- Dikey taşmada diğer sayfaya geçilir; **her sayfaya tablo başlığı (numara +
  sütun başlıkları) tekrar** eklenir ve başlık sonrası parantez içinde `(devam)`
  yazılır. Yatay taşmada ilgili sayfa **yatay (landscape)** kullanılabilir.
- Numaralandırma **Arap rakamı**, geçiş sırasına göre.
- **Tablo başlığı tablonun ÜST kenarının bir satır üstüne**, sol üst köşe
  hizasından yazılır. **12 punto, tek satır aralığı**, tümce düzeninde, kısa/öz.
- `Tablo 1.`, `Tablo 8.` etiketleri **kalın**, devamı normal punto.
- Başlık satırından **önce bir satır boş** bırakılır.
- Tüm kısaltma açıklamaları ve yıldız/sembol işaretlemeleri tablonun son
  çizgisinin **altında dipnot** olarak verilir. Başka kaynaktan hazırlanan
  tablolar dipnotta atıflanır.

### 1.8. Metin içinde kaynak gösterme

- **Yazar-Tarih** stili, Türkçeleştirilmiş:
  - İki yazar: soyadları arasında **ve** (örn. *John ve Marquez, 2017*).
  - Üç ve daha fazla yazar: ilk yazar soyadı + **ve ark.** (örn. *Smith ve
    ark., 2024*).
- Yazar ve tarih **virgül** ile ayrılır; birden fazla kaynakta bloklar
  arasında **noktalı virgül** (örn. `(Smith ve ark., 2024; John ve Marquez,
  2017)`).
- Yıl daima **parantez içinde**. Cümle sonu: `(Smith ve ark., 2024)`; cümle
  içi: `Smith ve ark. (2024)`.
- Aynı yazarın aynı yıla ait birden fazla kaynağı: yıla harf eklenir
  (`2017a`, `2017b`).
- Doğrudan alıntı: ifade **tırnak** içinde, ardından parantezde yazar, yıl ve
  **sayfa no**.

### 1.9. Sayfa numaralandırması

- Sayfa numarası **altta ortalanmış**.
- Dış/iç kapak, tez onayı, beyan, teşekkür ve içindekiler sayfaları
  **numaralandırılmaz**.
- Numaralandırma içindekiler bittikten sonra **Kısaltmalar**dan başlar.
- **Kısaltmalar, Şekiller, Tablolar** sayfaları **Romen rakamı** (i, ii, iii).
- **Özet**ten itibaren **Arap rakamı** (1, 2, 3).

---

## 2. İÇERİK STANDARTLARI — Ön Bölümler

Tüm ön bölümler `docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx` düzenine tam
uyumlu hazırlanır. Şablon örneği için `02_sablonlar/on-bolumler-sablonu.md`.

### 2.1. Tez kapağı

- Şablonun düzen ve ölçülerine tam uyum.
- Üst orta bölümde **2×2 cm Marmara Üniversitesi logosu (mavi)**.
- Logo altında sırasıyla: üniversite ve enstitü adı, tez başlığı, öğrenci adı,
  yüksek lisans/doktora tezi, danışman ünvan+ad soyad, program adı, varsa ikinci
  danışman, şehir ve yıl.
- **Tez başlığı: kalın 14 punto, en çok 20 kelime.** Diğer tüm yazılar 12 punto.
- **Bütün yazılar büyük harf.**
- **İç kapak** içerik ve düzen olarak dış kapağın aynısı.

### 2.2. Beyan

Şablondaki içerikte olmalı ve **imzalanmalıdır**.

### 2.3. Teşekkür

Katkı sunan kişi/kuruluşlara teşekkür. Proje/fon desteği varsa sayfanın alt
kısmında ayrı bölümde proje adı, kuruluş ve **proje numarası** ile beyan edilir
(örn. *"Bu tez Marmara Üniversitesi Bilimsel Araştırma Projeleri Komisyonu
Başkanlığı tarafından No.'lu proje ile desteklenmiştir"*).

### 2.4. İçindekiler

Şablon düzenine uygun, teşekkür sayfasından sonra.

### 2.5. Kısaltmalar (ön bölüm listesi)

Kısaltma ve açık yazılışı; **alfabetik**; kısaltma, noktalama (`:`) ve açıklama
şablona uygun hizalı.

### 2.6. Şekiller (ön bölüm listesi)

Her şekil: numara + başlık + sayfa numarası, hizalı. Başlık devamındaki
açıklama/kısaltma bu listede **yer almaz**. Şekil ve numarası **kalın**.

### 2.7. Tablolar (ön bölüm listesi)

Her tablo: numara + başlık + sayfa numarası, hizalı. Arka sayfaya taşan tablonun
`(devam)` kısmı listede belirtilmez. Tablo ve numarası **kalın**.

---

## 3. TEZ METNİ — Bölüm İçerik Kuralları

### 3.1. Başlık

Tez önerisinde kabul edilen başlıkla **aynı**; yabancı sözcük, marka adı, özel/
resmi kurum adı ve kısaltmadan kaçınılır.

### 3.2. Özet / Summary

- Şablon düzenine uygun, **bir sayfayı aşmaz**, paragraf girintisiz, **kaynak
  verilmez**.
- İlk bölümde tez başlığı, öğrenci, danışman, program **ayrı satırlar** halinde.
- Yapılandırma sırası: **Amaç → Gereç ve Yöntem → Bulgular → Sonuç** (her biri
  bir paragraf, alt başlık altında).
  - **Amaç:** çalışmanın neden yapıldığı; literatür taraması/ayrıntılı gerekçe
    yok.
  - **Gereç ve Yöntem:** tasarım, gereç/veri kaynakları, ölçüm-değerlendirme,
    temel analiz yaklaşımı; öz.
  - **Bulgular:** en önemli nicel ve nitel bulgular; sayı/yüzdeler istatistikle
    birlikte, **yorumsuz**.
  - **Sonuç:** temel bilimsel çıktı; kapsam dışı genelleme yok.
- **Anahtar sözcükler: en fazla 5**, virgülle ayrılır; ilki dışında her sözcük
  (özel isim/kısaltma hariç) küçük harfle başlar.
- **Summary** ayrı sayfada, Türkçe özetle **birebir aynı içerik** ve aynı
  kurallar. (Keywords: ilki büyük harfle başlar.)

### 3.3. Giriş ve Amaç

- Konuya genel çerçeve; temel kavramlara atıfla mevcut bilgi birikimi ve
  bilinmeyen yönler **özet** biçimde.
- Araştırmanın önemi ve literatüre katkısı açıkça ortaya konur.
- Temel araştırma sorusu net tanımlanır ve gerekçelendirilir.
- **Amaç:** açık, ölçülebilir, gerçekçi, ulaşılabilir; girişteki bilimsel
  boşlukla uyumlu; tek ya da birkaç cümle.
- **Bu bölümde alt başlık kullanılmaz** (şablon kuralı; Bölüm 1.3).

### 3.4. Genel Bilgiler

- Konunun teorik ve pratik temelleri, **genelden özele** akış; gerektiğinde alt
  başlıklar.
- Güncel literatür özetlenir; **yorum ve sonuç çıkarımından kaçınılır**.
- Güncel, güvenilir, akademik kaynaklar; mümkün oldukça son yıllar.
- Doğal olarak `Gereç ve Yöntem`e geçişi hazırlar.

### 3.5. Gereç ve Yöntem

- **Tekrarlanabilirlik** düzeyinde ayrıntı; alt başlıklarla.
- İçerik: çalışmanın yeri ve tarihi, araştırma tipi, evren ve örneklem,
  örnekleme yöntemi, araştırma sorusu/soruları ve varsa hipotez(ler),
  değişkenler + tanımları + ölçüm biçimleri, veri toplama araç ve yöntemi,
  kullanılan cihaz/kimyasal, **istatistiksel değerlendirme yöntemleri**.
- **Etik:** etik kurul izni **tarih ve sayı** ile bu bölümde belirtilir; onay
  belgesi **Ekler**de yer alır.

### 3.6. Bulgular

- Amaçlar doğrultusunda tüm veriler açık, düzenli, **tarafsız** ve **yorumsuz**
  sunulur.
- Araştırma soruları/hipotezlerle uyumlu sırada; önce metinde özet, ayrıntı
  tablo/şekille.
- Tanımlayıcı veriler → ölçüm/değerlendirme sonuçları → temel karşılaştırmalar
  (yöntem + analiz bulgusuyla). Anlamlılık düzeyi belirtilir; program çıktılarının
  tamamı eklenmez.
- Gereksiz tekrar ve çelişki yok. **Aynı bulgu hem tablo hem şekil olarak
  sunulmaz.** Tablo/şekiller konu edildikleri yerde, kısaltma/simge/test/p
  değerleri dipnotta.

### 3.7. Tartışma ve Sonuç

- **Yorum bölümüdür, literatür özeti değildir.** Bulgular diğer araştırmalarla
  karşılaştırılır; benzer/farklı yönler ve uyan/uymayan sonuçlar muhtemel
  nedenleriyle tartışılır; bulguların anlamı yorumlanır.
- **Hipotez(ler)in desteklenip desteklenmediği** açıkça belirtilir.
- Bulgu tekrarı yapılmaz (tablo/şekle atıf yeterli); istatistik test sonucu
  tekrarlanmaz. `Giriş ve Amaç` / `Genel Bilgiler` bilgileri tekrar edilmez.
- Sonunda **Sonuç:** varılan sonuçlar açık/kısa/anlaşılır; amacın ne ölçüde
  gerçekleştiği ve **öneriler** (amaç ve sonuçlarla doğrudan bağlantılı).
- **Bu bölümde alt başlık kullanılmaz** (şablon kuralı; Bölüm 1.3).

### 3.8. Özgeçmiş

Öğrencinin kısa özgeçmişi, şablon formatında, **tek sayfa**.

### 3.9. Bilimsel Faaliyetler

Kayıt tarihinden itibaren proje, toplantı, patent, makale vb.; **kaynak yazımı
formatında**. Mezuniyet koşulu sağlayan yayın/sunumların tam dokümanları ayrı
portfolyo olarak enstitüye teslim edilir, **teze eklenmez**. Dergide basılmayan
bildiriler için şablondaki örnek biçim kullanılır.

### 3.10. Ekler

Gerekli tüm ekler (örnek hesaplama, formül çıkarımı, geniş deney verisi, anket
formu, ek çizelge, **etik kurul onay yazısı** vb.) metindeki sıraya göre
**Ek 1, Ek 2, Ek 3** biçiminde, her biri **ayrı sayfada**.

---

## 4. KAYNAKÇA — AMA-11 Özel Formatı

Kaynaklar, **American Medical Association (AMA)-11** kılavuzuna dayanan Enstitü
özel formatına göre yazılır. Referans yönetim yazılımı kullananlar Enstitü
stil dosyalarını
`https://saglik.marmara.edu.tr/ogrenci/formlar-ve-prosedurler/tez-yazim-kilavuzu`
adresinden alır.

### 4.1. Format

- Kaynaklarda **italik veya kalın punto kullanılmaz**.
- Her kaynak **1 satır aralıklı** ve **0,5 cm asılı (hanging)**; kaynaklar
  arasında **6 nk** boşluk.
- **Yazar soyadına göre alfabetik** sıralama.
- Genel sıralama: **Yazar. Yayın Başlığı. Yayıncı. Cilt;(Sayı):Sayfa Aralığı.
  doi** (kaynağa özgü istisnalar Bölüm 4.3).
- Yazar sayısı **altıdan fazlaysa** ilk altı yazar + **et al.** (Türkçe
  kaynaklarda **ve ark.**).
- Yayın başlığında tümce düzeni; ilk harf ve özel isim/kısaltma dışında büyük
  harf yok.
- Dergi isimleri **kısaltılmış** versiyonuyla.

### 4.2. İçerik

- Mümkün oldukça güncel, kanıt değeri yüksek **araştırma/derleme makaleleri** ve
  başvuru niteliğinde **kitap bölümleri**.
- **Bildiri özetleri** yalnız savunma tarihinden önceki **üç yıl** içinde
  sunulmuş ve bir dergide **genişletilmiş konferans özeti (Proceedings)** olarak
  yayımlanmışsa; başka bildiriye atıf yapılmaz.
- **Web sayfaları:** yalnız **.gov, .int, .eu** uzantılı resmi kurum/kuruluş
  sayfalarına sınırlı atıf; **toplam web kaynağı tüm kaynakların %5'ini geçmez**.
  `.com`, `.net` vb. kaynak olarak kullanılmaz.
- **Lisans, yüksek lisans ve doktora tezleri kaynak olarak kullanılmaz.** (Resmi
  kılavuz PDF numaralandırmasında bu kural §3.8.2'dir; kanonik talimatnamede §4.2 —
  repo genelinde her iki numara da bu kurala işaret eder.)

### 4.3. Kaynak yazım örnekleri (resmi Tablo 1)

**Makaleler** — sıralama: Yazar. Yayın Başlığı. Dergi Adı. Cilt;(Sayı):Sayfa.
doi (bölümler `.` ile ayrılır):

- **≤6 yazarlı:** `Fadini GP, Del Prato S, Avogaro A, Solini A. Challenges and
  opportunities in real-world evidence on the renal effects of sodium-glucose
  cotransporter-2 inhibitors. Diabetes Obes Metab. 2022;24(2):177-186.
  https://doi.org/doi:10.1111/dom.14599`
- **>6 yazarlı:** `Xie Y, Shi X, Sheng K, Han G, Li W, Zhao Q, et al. PI3K/Akt
  signaling transduction pathway, erythropoiesis and glycolysis in hypoxia. Mol
  Med Rep. 2019;19(2):783-791. https://doi.org/doi:10.3892/mmr.2018.9713`
- **>6 yazarlı (Türkçe):** `Dilek B, Songür K, Erdinç Gündüz N, Ellidokuz H,
  Başçı O, Gülbahar S ve ark. Lateral epikondilit tanılı hastalarda klinik ve
  ultrasonografik bulgular ile tedavi değişimi arasındaki ilişki: 6 aylık
  sonuçlar. DEU Tıp Derg. 2024;38(3):251-262.`
- **Erken erişimli:** `… Nat Rev Neurosci. 2023;24(12):Epub ahead of print.
  https://doi.org/…`
- **Düzeltme yapılan:** `… N Engl J Med. 2001;345(7):494-502. Erratum in: N Engl
  J Med. 2001;345(20):1506. https://doi.org/…`

**Kitap bölümleri** — editörlü/editörsüz, İngilizce/Türkçe:

- **İngilizce/Editörlü:** `Nestler EJ, Hyman SE. Molecular mechanisms of
  antidepressant action. In: Brunton LL, Hilal-Dandan R, Knollmann BC, editors.
  Goodman & Gilman's Pharmacological Basis of Therapeutics. 13th ed. New York:
  McGraw-Hill; 2018. p. 257-276.`
- **İngilizce/Editörsüz:** `Kandel ER. Principles of neural science: Molecular
  mechanisms of learning and memory. 5th ed. New York: McGraw-Hill; 2013. p.
  1221-1250.`
- **Türkçe/Editörlü:** `Kalyoncu AF, Karakaya G. Mesleksel astım. İçinde:
  Özyardımcı N, editör. Göğüs Hastalıkları. 2. Baskı. Ankara: Güneş Tıp
  Kitabevleri; 2012. s. 457-468.`
- **Türkçe/Editörsüz:** `Aycan K. Kas-iskelet sistemi anatomisi. İnsan
  Anatomisi. 3. Baskı. Ankara: GATA Basımevi; 2005. s. 215-249.`
- Editörü olmayan veya bölüm yazarı = editör olan kitaplarda yazar/editör
  tekrarı gerekmez. Elektronik kitap bölümlerinde **doi** eklenir.

**Diğer tipler:**

- **Bildiri (Proceedings):** `… Eur Heart J. 2024;45(Suppl 1):ehae666.028.
  https://doi.org/doi:10.1093/eurheartj/ehae666.028`
- **Web sitesi (.int/.gov/.eu):** `World Health Organization. [Internet] Global
  report on diabetes (Atıf Tarihi: 11.02.25; Erişim Tarihi: 25.08.25). Available
  from: https://www.who.int/publications/i/item/9789241565257`
- **Resmi rapor:** `European Medicines Agency. Committee for Medicinal Products
  for Human Use. Guideline on clinical evaluation of vaccines.
  EMA/CHMP/VWP/164653/05 Rev. 1. London; 2019 (Accessed: 15.08.25). https://…`
- **Veri tabanı:** `U.S. Food and Drug Administration. FDA Adverse Event
  Reporting System (FAERS) Public Dashboard. [Database] … (Son Güncelleme Tarihi:
  30.06.2025; Erişim Tarihi: 25.08.2025). Available from: https://…`

> Bu tezde `references.bib` + Zotero hattı Enstitü AMA-11 çıktısına
> dönüştürülür. Zotero'da Enstitü CSL/stil dosyası kullanılır; hiçbir künye
> Evidentia-doğrulaması ve referans ledgeri kapanmadan kaynakçaya girmez
> (`01_mimari/evidentia-entegrasyon-cercevesi.md`, Bölüm 5 referans kapısı).

---

## 5. RESMİ BÖLÜM SIRASI (değiştirilemez)

`docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx` sırası:

1. Tez onayı
2. Beyan
3. Teşekkür
4. İçindekiler
5. Kısaltmalar
6. Şekiller
7. Tablolar
8. Özet
9. Summary
10. Giriş ve Amaç
11. Genel Bilgiler
12. Gereç ve Yöntem
13. Bulgular
14. Tartışma ve Sonuç
15. Kaynaklar
16. Özgeçmiş
17. Bilimsel Faaliyetler
18. Ekler

Ana bölüm başlıkları büyük harf; `GİRİŞ ve AMAÇ`, `GEREÇ ve YÖNTEM`, `TARTIŞMA
ve SONUÇ` yazımında şablondaki bağlaç biçimi korunur.

---

## 6. KARMA TEZ İÇİN BÖLÜM-KAYNAK-KAPI HARİTASI

Bu tez **karma yöntem**tir; her bölüm nicel (kök) ve nitel (nitel kol, niteliksel/)
kolun ilgili kesimini birleştirir. Ayrıntılı kaynak/kapı için
`01_mimari/iki-repo-entegrasyon-plani.md` ve
`05_entegrasyon/nitel-cikti-cercevesi.md`.

| Bölüm | Nicel kaynak | Nitel kaynak (türetilmiş) | Dış literatür |
|---|---|---|---|
| Giriş ve Amaç | `03_bolum-hazirlik/01_giris-ve-amac.md` | Kanonik nitel rapor (arka plan) | Evidentia (Bölüm 4 kapısı) |
| Genel Bilgiler | `03_bolum-hazirlik/02_genel-bilgiler.md` | — | Evidentia |
| Gereç ve Yöntem | `03_bolum-hazirlik/03_gerec-ve-yontem.md`, `_targets.R` | COREQ, audit trail, positionality, LLM beyanı | — |
| Bulgular | `04_bulgular` / H1–H5 | Kanonik nitel sonuç raporu, 4 makro tema | — |
| Tartışma ve Sonuç | `05_tartisma-ve-sonuc.md` | Negatif vaka, refleksivite, triadik yorum | Evidentia |
| Kaynaklar / Ekler | `06_kaynaklar-ekler.md`, `references.bib` | COREQ, codebook, audit trail | Referans ledgeri + Zotero |

**Kanıt ayrımı (ihlal edilemez):** Nitel bulgu nicel etki tahmini gibi
yazılmaz; nicel sonuç nitel temanın nedensel/mekanistik kanıtı yapılmaz; joint
display iki kolu yan yana getirir ve **kanıt türünü açık yazar** (uyum /
tamamlayıcılık / ayrışma / açıklayıcı genişleme ayrı etiketlenir).

---

## 7. NİTEL BULGULAR — Biçim Kuralları

- Nitel bulgular **tema, alt tema, örüntü ve rol karşılaştırması** olarak
  yazılır.
- **Ham alıntı dökümü yapılmaz**; yalnız araştırmacı onaylı **anonim alıntı**
  (aile no + rol etiketi) veya **quote ID** kullanılır.
- Triadik yorumda anne, T1DM tanılı çocuk ve sağlıklı kardeş deneyimleri **ayrı
  kanıt türleri** olarak korunur.
- Nitel tema, nicel etki büyüklüğü/nedensel mekanizma gibi sunulmaz.
- **Tez = 4 makro tema, journal = 6 tema** — karıştırılmaz (yeniden yazımdan
  önce hedef çıktı netleştirilir).

---

## 8. İSTATİSTİK YAZIM Kuralları (biçim)

- Bulgular **yorumsuz** sunulur; yorum `Tartışma ve Sonuç`a kalır.
- Tanımlayıcılarda ölçek, birim, payda ve **eksik veri notu** açık tutulur.
- `p` değerleri: `p=0,038` veya `p<0,001` (Bölüm 1.4).
- Aynı sonuç metin/tablo/şekil arasında gereksiz tekrarlanmaz.
- Post-hoc / Faz II bulgular **birincil hipotez sonucu gibi yazılmaz**
  (`[KEŞİFSEL]` ayrımı korunur).

---

## 9. QUARTO / TEKNİK ÜRETİM Notları

- Üretim dosyaları: `thesis.qmd` + `chapters/*.qmd`; render `carbon-quarto-
  scientific` skill'i ile.
- Quarto YAML: `lang: tr`. Sayısal çıktı ondalık **virgül**; tablo/şekil
  numaralandırma ve başlık konumu bu talimatnameye uydurulur (Quarto varsayılan
  İngilizce format notları **override edilir**).
- gt/gtsummary tabloları ve ggplot2 figürleri Bölüm 1.6–1.7 biçim kurallarına
  (başlık konumu, kalın etiket, dipnot) çevrilir.
- **Otomatik imla/sayısal denetim:** Bölüm 1.4 sayısal yazım (ondalık virgül,
  `p` biçimi) ve Türkçe imla, `sci-audit@cureonics-marketplace` plugin **axis G**
  ile makine düzeyinde denetlenir (`/sci-audit:check-turkish`; Türkçe metinde
  İngilizce ondalık-nokta `p` değeri **blocker**). Manüskript adli denetimi
  (referans/claim/istatistik/kılavuz/AI-şeffaflık) axes A–F'dedir. Kanonik
  kullanım: `04_kalite-kontrol/turkce-bilimsel-yazim-denetimi.md`.
- Render sonrası **format kontrolü** (Bölüm 12) yapılmadan bölüm final sayılmaz.

---

## 10. BAĞLAYICILIK ve DOĞRULAMA

- Bu talimatname, `tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md`
  (zorunlu süreç talimatnamesi) ile birlikte çalışır; süreç talimatnamesi
  **rota/kapı/gizlilik**, bu talimatname **biçim** otoritesidir.
- `00_kaynak-kurallari/format-kontrati.md` bu talimatnamenin **kısa
  operasyonel özeti**dir; ayrıntı çakışırsa bu kanonik talimatname esastır.
- Her bölüm kapanışında
  `04_kalite-kontrol/format-kontrol-listesi.md` + Bölüm 12 checklist'i geçilir;
  ardından `04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`
  Kapı 3 (metin/kılavuz uyumu) bu talimatnameye referansla, Kapı 4 (imla/yazım)
  ve Kapı 5 (AI-reliability) `sci-audit` plugin ile doldurulur.

---

## 11. BU PROJE İÇİN OVERRIDE NOTU

Repo içindeki eski yazım notlarında **APA 7**, **nokta ondalık ayırıcı** veya
alternatif Quarto format kararı geçen yerler bulunabilir. Bu tez yazım hattında
resmi `docs/tez-kilavuz` dosyaları **üstündür**:

- Kaynakça: **Enstitü AMA-11 özel formatı** (APA 7 değil).
- Sayısal yazım: **ondalık virgül** (nokta değil).
- Metin içi atıf: **yazar-yıl, "ve"/"ve ark."** (Türkçeleştirilmiş).
- Bölüm sırası: **şablon DOCX resmi sırası** (Bölüm 5).

---

## 12. FORMAT KONTROL CHECKLIST (bölüm kapanışı)

Her `chapters/*.qmd` bölümü final öncesi:

- [ ] Sayfa: A4, beyaz, tek sütun; kenar boşlukları 2,5/2,5/2/2 cm.
- [ ] Ana metin Times New Roman 12 punto, 1,5 aralık; paragraf girintisiz + 6 nk.
- [ ] Metin iki yana yaslı; kelime bölünmesi yok; başlık sayfa sonunda yalnız değil.
- [ ] Başlıklar: ana 14 punto kalın, alt 12 punto kalın; kapitalizasyon ve
      bağlaç kuralı; başlık sonu noktalama yok.
- [ ] `GİRİŞ ve AMAÇ` / `TARTIŞMA ve SONUÇ` alt başlıksız (veya onaylı taslak notu).
- [ ] Sayısal yazım: ondalık virgül; ortalama/yüzde 1 basamak; test/oran 2
      basamak; `p=0,038` / `p<0,001`; ondalık öncesi sıfır.
- [ ] Şekil başlığı **altta**, 12 punto tek aralık, `Şekil N.` kalın; Arap numara.
- [ ] Tablo başlığı **üstte**, 12 punto tek aralık, `Tablo N.` kalın; dipnotlar
      son çizgi altında; aynı bulgu hem tablo hem şekil değil.
- [ ] Metin içi atıf yazar-yıl; iki yazar "ve", 3+ "ve ark."; çoklu kaynak `;`.
- [ ] Kaynakça AMA-11: alfabetik, italik/kalın yok, 0,5 cm asılı, 6 nk; >6 yazar
      "et al./ve ark."; dergi kısaltması; web ≤%5 ve yalnız .gov/.int/.eu; tez
      kaynağı yok.
- [ ] Sayfa numaralandırma: kısaltmalar–tablolar Romen, özetten Arap.
- [ ] Nitel/nicel kanıt türü karışmamış; ham alıntı yok; anahtar sözcük ≤5.
- [ ] Bölüm sırası şablona uygun.
- [ ] `sci-audit` axis G (imla/decimal) + axes A–F (manüskript adli) koşuldu,
      blocker yok.

Bu checklist geçmeden bölüm en fazla **taslak/`provisional-pass`**; final için
sertifikasyon playbook'u + açık uygulama onayı gerekir.
