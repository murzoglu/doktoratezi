import sys

file_path = "chapters/03_gerec_ve_yontem.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    """## Değişkenler ve Tanımları

Çalışmanın değişkenleri, işlevlerine göre grup, sonuç ve eş değişkenler olarak yapılandırılmıştır. Birincil grup değişkeni, indeks ve kardeş çocukları birlikte temsil eden dört düzeyli rol faktörüdür; ikili karşılaştırmalarda tanı grubu (T1DM/kontrol) değişkeni kullanılmıştır. Sonuç değişkenleri; çocuğun algıladığı ebeveynlik tutumu alt ölçekleri, annenin öz-bildirdiği ebeveynlik tutumu alt ölçekleri, kardeş ilişkisi boyutları ve anne depresif belirti düzeyidir. Eş değişkenler (kovaryatlar) çocuk yaşı, çocuk cinsiyeti, anne yaşı, kardeşler arası yaş farkı, ailedeki çocuk sayısı ve sosyoekonomik durumdur. Tüm yaş ve süre alanları, ilgili anket tarihi ile doğum ya da tanı tarihi farkının 365,25'e bölünmesiyle yıl cinsinden türetilmiştir.

Çalışmada katılımcıların sosyoekonomik durumu tek bir değişkene indirgenmek yerine; eğitim, meslek ve maddi varlıkları eşzamanlı olarak kapsayan üç katmanlı bir kompozit (birleşik) yapı üzerinden değerlendirilmiştir. Bu doğrultuda süreç şu adımlarla yürütülmüştür:

**ISEI ve maddi varlık göstergeleri.** İlk aşamada, ebeveynlerin eğitim ve meslek bilgileri evrensel bir standart olan uluslararası sosyoekonomik indekse (*International Socio-Economic Index*, ISEI) dönüştürülmüştür [@ganzeboomTreiman1996isei]. Modele yalnızca mesleki statü değil, ailenin ekonomik durumunu yansıtan maddi varlık göstergeleri de dahil edilmiştir.

**Polikorik temel bileşenler analizi.** Maddi varlıkları ölçen anket maddeleri sıralı (*ordinal*) yapıda olduğundan, puanlar basitçe toplanmamıştır. Bunun yerine, verinin bu sıralı doğasına istatistiksel olarak en uygun yöntem olan polikorik korelasyon matrisine dayalı bir temel bileşenler analizi uygulanarak ağırlıklandırılmış bir maddi varlık indeksi hesaplanmıştır.

**Birincil sosyoekonomik kovaryat.** Çalışmanın asıl istatistiksel çözümlemelerinde, dış değişkenlerin (sosyoekonomik farkların) etkisini kontrol altında tutmak (*adjusting*) için doğrudan bu hesaplanan değerler kullanılmamıştır. Tüm bu göstergeler bir doğrulayıcı faktör analizi modeline sokulmuş ve ölçüm hatalarından arındırılmış bir gizil (*latent*) skor üretilmiştir. Analizlerdeki temel sosyoekonomik kontrol değişkeni (kovaryat) bu gizil skor olmuştur.

**Metodolojik şeffaflık ve duyarlılık kontrolü.** Ulaşılan bulguların, araştırmacının seçtiği spesifik ölçüm veya hesaplama yöntemine bağlı bir yanılsama olmadığını göstermek amacıyla ek duyarlılık (*sensitivity*) analizleri yürütülmüştür. Bu kapsamda veriler; klasik eş-ağırlıklı toplama yöntemiyle ve geleneksel Hollingshead tipi kompozit skorlarla yeniden üretilerek sonuçların dayanıklılığı sınanmıştır [@hollingshead1975].

T1DM grubuna özgü klinik değişkenler tanı tarihi, diyabet süresi ve son ölçülmüş klinik HbA1c yüzdesidir; bu alanlar klinik kayıt üzerinden tamamlanmıştır. HbA1c yalnız T1DM tanılı indeks çocuk satırlarında tanımlıdır; kardeş, kontrol indeks ve kontrol kardeş satırlarında tasarım gereği yapısal olarak eksiktir (*structural missing*). Final veri setinde 120 T1DM indeks çocuğun 39'unda HbA1c değeri kayıtlıdır ve tüm değerler klinik olarak makul aralıktadır. Serbest metin biçimindeki tanımlayıcı olabilecek alanların ele alınışı Etik Hususlar başlığında açıklanmıştır.

## Veri Toplama Araçları

Veriler, araştırmacı tarafından hazırlanan bir demografik ve tıbbi bilgi formu ile dört standart ölçme aracıyla toplanmıştır. Ölçeklerin madde metinleri telif nedeniyle burada tam olarak aktarılmamış; her aracın ne ölçtüğü, kim tarafından yanıtlandığı ve puanlama yapısı tanımlanmıştır. Basılı ölçek formları eklerde listelenmiştir.

### Demografik ve tıbbi bilgi formu

Form; kimlik ve rol alanlarını, tarih ve türetilmiş süre alanlarını ve çocuk ile kardeş yapısına ilişkin bilgileri (çocuk sayısı, doğum sırası, cinsiyet) kapsar. Sosyoekonomik kovaryatlar (anne ve eş eğitim ve çalışma durumu, ev sahipliği, oda sayısı, araç sahipliği) ve tıbbi/klinik alanlar (annede ve eşte kronik hastalık, anne antidepresan kullanımı ve T1DM grubunda tanı tarihi, diyabet süresi, HbA1c) da forma dâhil edilmiştir. Serbest metin biçimindeki meslek ve hastalık/engel alanları, çözümleme öncesinde standart meslek ve hastalık kategorilerine dönüştürülmüştür.

### Kısaltılmış Algılanan Ebeveyn Tutumları Ölçeği – Çocuk Formu (s-EMBU-C)

Çocuğun algıladığı anne tutumunu ölçen s-EMBU-C, kısaltılmış EMBU'nun çocuk-bildirim formudur [@arrindell2005sembu; @castro1993embuChildren]. Formun Karşılaştırma alt ölçeğini içermeyen üç faktörlü sürümü, yetişkinlerin çocukluk dönemini anımsamasına dayalı retrospektif çerçevede Dirik ve arkadaşları tarafından Türkçeye kazandırılmış ve geçerlik-güvenirlik kanıtı sağlanmıştır [@dirik2015sEmbuTurkish]. Bu çalışmada ise form, ebeveyn tutumunu çocukların güncel algısı üzerinden ölçecek biçimde güncel zaman ifadesiyle uygulanmıştır. Ölçek 29 maddeden oluşur ve dörtlü Likert biçiminde (1 = en düşük sıklık; 4 = en yüksek sıklık) yanıtlanır; yüksek puan ilgili özelliğin daha güçlü algılandığını gösterir. Ölçek dört alt ölçek sunar: Duygusal Sıcaklık (9 madde), Aşırı Koruma (7 madde), Reddetme (8 madde) ve Karşılaştırma (5 madde).

Özgün kısaltılmış EMBU üç alt ölçek (duygusal sıcaklık, reddetme, aşırı koruma) ve 23 madde içerir [@arrindell1999sembu; @arrindell2005sembu]. Bu Türkçe uyarlamada söz konusu üç alt ölçek 24 maddeye karşılık gelir (Duygusal Sıcaklık 9, Aşırı Koruma 7, Reddetme 8). Çocuğu akranları ve kardeşleriyle —ağırlıklı olarak akademik/sosyal başarı ekseninde— karşılaştıran karşılaştırmacı ebeveyn tutumunu ölçen beş maddelik Karşılaştırma alt ölçeğinin Sümer, Gündoğdu-Aktürk ve Helvacı tarafından eklenmesiyle ölçek 24 + 5 = 29 maddeye ve dört alt ölçeğe genişler [@sumer2010anneBabaTutum]. Ebeveynin çocuğu akran ve kardeşleriyle kıyaslamasını değerlendiren bu boyut, kardeş ilişkilerinin de incelendiği bu tasarımda karşılaştırmacı ebeveyn tutumunun ölçülmesine olanak tanıdığından forma dâhil edilmiştir.

İçeriği izin verme yönünde olan tek çocuk-form maddesi (kanonik kodlamada `q25`; "Annen evin uzağında oynamana izin verir mi?"), aşırı koruma alt ölçeğiyle yön tutarlılığı sağlanacak biçimde ters puanlanarak saklanmıştır. Ebeveyn formunda (s-EMBU-P) karşılık gelen madde ise sözel olarak *zaten* aşırı koruma yönünde yazıldığından ("Oynarken evin yakınından ayrılmasına hiç izin vermem") final kanonda ters puanlanmadan doğrudan kaydedilmiştir; iki formda da yüksek final puan daha yüksek aşırı korumaya karşılık gelir. Bu iki maddenin sözel yönü, ham kodlaması ve ters puanlama kararı @tbl-q25-yon içinde belgelenmiştir. Ölçek indeks ve kardeş çocuklarına ayrı ayrı uygulanmıştır. Bu dört alt ölçekli sürümün bu örneklemdeki faktör yapısı ve güvenirliği, birincil hipotez sınamalarından önce ayrı bir çalışma-içi psikometrik değerlendirme hattıyla incelenmiştir (bkz. Ölçme Araçlarının Psikometrik Değerlendirmesi).

| Madde | Form | Alt ölçek | Sözel yön | Ham kodlama | Ters puanlama | Yüksek final puanın anlamı |
|-------|------|-----------|-----------|-------------|---------------|-----------------------------|
| q25 | Çocuk (s-EMBU-C) | Aşırı Koruma | İzin verme ("…izin verir mi?") | 1–4 | Var ($5-x$) | Daha yüksek aşırı koruma |
| q25 | Ebeveyn (s-EMBU-P) | Aşırı Koruma | Kısıtlama ("…hiç izin vermem") | 1–4 | Yok | Daha yüksek aşırı koruma |

: q25 maddesinin çocuk ve ebeveyn formlarında sözel yönü ve ters puanlama kararı. İki formda sözel yön zıt olduğundan yalnız çocuk maddesi ters puanlanır; her iki formda yüksek final puan daha yüksek aşırı korumayı gösterir. {#tbl-q25-yon}

### Kısaltılmış Algılanan Ebeveyn Tutumları Ölçeği – Ebeveyn Formu (s-EMBU-P)

Annenin kendi ebeveynlik tutumunu öz-bildirimle değerlendiren s-EMBU-P, çocuk formuyla aynı madde sırasını ve dörtlü Likert biçimini paylaşan 29 maddelik ebeveyn-bildirim formudur ve aynı dört alt ölçeği (Duygusal Sıcaklık, Aşırı Koruma, Reddetme, Karşılaştırma) üretir [@arrindell2005sembu]. Form aile/indeks düzeyinde, anketi getiren indeks çocuk hedef alınarak yanıtlanmıştır. Ebeveyn ve çocuk formlarının madde düzeyinde eşlenik yapısı, anne öz-bildirimi ile çocuk algısı arasındaki diadik (anne ↔ çocuk) tutarlılık çözümlemesini doğrudan olanaklı kılar. Ebeveyn formu da çocuk formuyla eşlenik dört alt ölçekli yapısıyla bu örneklemde ayrı bir çalışma-içi psikometrik değerlendirmeye tabi tutulmuştur (bkz. Ölçme Araçlarının Psikometrik Değerlendirmesi).

### Kardeş İlişkileri Anketi

Kardeş ilişkisinin niteliğini çocuğun bakış açısından değerlendiren Kardeş İlişkileri Anketi, özgün olarak Furman ve Buhrmester (1985) tarafından geliştirilmiştir [@furmanBuhrmester1985srq]. Ölçeğin Türkçeye uyarlaması Apalaçi (1996) tarafından yapılmış ve çalışmada bu Türkçe uyarlama kullanılmıştır [@apalaci1996yoktez]. Türkçe kardeş ilişkileri ölçümüne ilişkin ek/karşılaştırmalı bir kaynak için ayrıca bkz. [@aktas2017kardesIliskileriOlcegi]. Ölçek 48 maddeden oluşur ve beşli Likert biçiminde (1 = hemen hemen hiç; 5 = çok çok fazla) yanıtlanır; anketi hem indeks hem kardeş çocuk kendi bakış açısından doldurmuştur. Ölçek dört üst düzey boyut sunar: Sıcaklık/Yakınlık, Statü/Güç, Çatışma ve Rekabet. Ebeveyn karşılaştırmasını göreli yönde soran maddeler, puanlamada bu yön dikkate alınarak işlenmiştir.

### Beck Depresyon Envanteri

Annenin son bir haftadaki depresif belirti düzeyini ölçen Beck Depresyon Envanteri, Türkçe geçerlik ve güvenirlik çalışması temel alınarak uygulanmıştır [@hisli1989bdiTurkishUniversity]. Envanter 21 maddeden oluşur; her madde 0–3 arası puanlanır ve toplam puan 0–63 aralığındadır. Toplam puan tüm maddeler yanıtlandığında hesaplanmış, herhangi bir madde eksik olduğunda toplam puan eksik bırakılmıştır. Çözümlemelerde Beck toplam puanı öncelikle **sürekli** değişken olarak kullanılmıştır. Ayrık şiddet bantları (ör. minimal/hafif/orta/şiddetli), Türkçe literatürde tek bir yerleşik eşik kümesine dayanmadığından ve mevcut geçerlik kanıtı anne örneklemine doğrudan aktarılamadığından raporlanmamıştır. Yalnız keşifsel klinik-fayda çözümlemelerinde, Hisli'nin psikiyatri polikliniği örneklemindeki klinik ayırt etme çalışmasında kullanılan Beck toplam ≥ 17 kesme puanı [@hisli1988bdiClinical] operasyonel bir **ikili gösterge** olarak alınmıştır; bu gösterge klinik tanı veya ileriye dönük risk anlamı taşımaz, yalnız güncel depresif belirti yükünün görece yüksek olduğu grubu betimsel olarak işaretler ve keşifsel yorumlanır.

Nitel kolun yarı yapılandırılmış görüşme rehberi bir ölçme aracı niteliğinde olmadığından, nitel veri toplama sürecinin bir parçası olarak ilgili alt başlıkta tanımlanmıştır (bkz. Nitel Veri Toplama).""" :
    """## Değişkenler ve Tanımları

Çalışmamızdaki veriler gruplara göre (diyabet / sağlıklı kontrol), hedeflediğimiz sonuçlara göre (ebeveynlik algısı, kardeş ilişkisi, annenin depresyonu) ve kontrol etmemiz gereken dış etkenlere göre (yaş, cinsiyet, sosyoekonomik durum vb.) üç gruba ayrılmıştır. Tüm çocukların ve annelerin yaşları, anket formunun doldurulduğu tarih ile doğum tarihi arasındaki tam süre hesaplanarak küsuratlı yıla çevrilmiştir.

Ailelerin sosyoekonomik durumunu belirlerken tek bir basit "gelir durumu" sorusuyla yetinilmemiş; ebeveynlerin eğitimi, meslekleri, ev sahipliği ve araba sahipliği gibi unsurlar tek bir bütüncül modelde (maddi varlık indeksi) kaynaştırılmıştır. Aileler arası analizler yapılırken dış değişkenlerin istatistiği yanıltmaması adına, ölçüm hatalarından arındırılmış bir sosyoekonomik gizil (latent) skor kullanılmıştır [@ganzeboomTreiman1996isei]. Çalışmanın bulgularının tamamen bu hesaplama yöntemine sırtını dayamadığını göstermek için de klasik formüllerle (Hollingshead yöntemi vb.) hesaplanan skorlarla da ekstra testler (sağlamlık kontrolleri) yapılmıştır [@hollingshead1975].

Diyabetli çocuklara ait kan şekeri (HbA1c), hastalığın süresi ve tanı tarihi gibi tüm tıbbi bilgiler anketle değil doğrudan poliklinikteki hasta dosyalarından teyit edilerek alınmıştır. Aile yapısını deşifre edebilecek isim, meslek veya açık hastalık adı gibi veriler gizlilik gereği analizler başlamadan standart kategorilere çevrilerek kimliksizleştirilmiştir.

## Veri Toplama Araçları

Kullandığımız demografik bilgi formuna ek olarak ailelere dört ana anket (ölçek) verilmiştir. Telif haklarından dolayı soruların tüm metinleri rapora eklenmese de anketlerin neyi, nasıl puanladığı aşağıda açıklanmıştır:

### Demografik ve tıbbi bilgi formu

Araştırmacılar tarafından hazırlanan bu form; anne ve babanın mesleği/eğitimi, araba veya ev sahipliği, diyabetin ne zaman başladığı ve annenin antidepresan kullanıp kullanmadığı gibi tıbbi ve sosyal temel bilgileri içermektedir.

### Kısaltılmış Algılanan Ebeveyn Tutumları Ölçeği – Çocuk Formu (s-EMBU-C)

Çocuğun "annesi tarafından nasıl davranıldığını" hissettiğini ölçen bu form [@arrindell2005sembu; @castro1993embuChildren], Türkiye'deki kültürümüze ve dilimize uygun hâle getirilmiş 29 sorudan oluşmaktadır [@dirik2015sEmbuTurkish]. Sorular "1 = hiçbir zaman"dan "4 = her zaman"a kadar dört şıkla puanlanır; puan yükseldikçe çocuk o ebeveynlik tutumunu daha fazla hissediyor demektir. Çocuklara uygulanan bu form 4 ayrı bölümü değerlendirir: Duygusal Sıcaklık, Aşırı Koruma, Reddetme ve (çocuğu bir başkasıyla rekabet ettiren) Karşılaştırma [@sumer2010anneBabaTutum]. 

Çocuklar için hazırlanan "Annen evin uzağında oynamana izin verir mi?" sorusu, anne formundaki "Oynarken evin uzağına gitmesine izin vermem" sorusuyla zıt yönde olduğu için, anket verileri bilgisayara girilirken çocuk formundaki puanlar tersten işlenmiş, böylece her iki formda da "yüksek puanın = aşırı korumacı anneyi" ifade etmesi sağlanmıştır (@tbl-q25-yon).

| Madde | Form | Alt ölçek | Sözel yön | Ham kodlama | Ters puanlama | Yüksek final puanın anlamı |
|-------|------|-----------|-----------|-------------|---------------|-----------------------------|
| q25 | Çocuk (s-EMBU-C) | Aşırı Koruma | İzin verme ("…izin verir mi?") | 1–4 | Var ($5-x$) | Daha yüksek aşırı koruma |
| q25 | Ebeveyn (s-EMBU-P) | Aşırı Koruma | Kısıtlama ("…hiç izin vermem") | 1–4 | Yok | Daha yüksek aşırı koruma |

: q25 maddesinin çocuk ve ebeveyn formlarında sözel yönü ve ters puanlama kararı. İki formda sözel yön zıt olduğundan yalnız çocuk maddesi ters puanlanır; her iki formda yüksek final puan daha yüksek aşırı korumayı gösterir. {#tbl-q25-yon}

### Kısaltılmış Algılanan Ebeveyn Tutumları Ölçeği – Ebeveyn Formu (s-EMBU-P)

Çocuk formundaki aynı 29 sorunun, bu kez annenin kendi penceresinden değerlendirildiği formdur [@arrindell2005sembu]. Sorular tamamen eşleştiği için, annenin "ben çocuğuma böyle davranıyorum" demesiyle çocuğun "annem bana böyle davranıyor" hissini istatistiksel olarak doğrudan çarpıştırmamıza (uyum analizlerine) imkân tanımıştır. Form, annenin direkt olarak T1DM tanılı indeks çocuğu baz alarak yanıtlaması amacıyla verilmiştir.

### Kardeş İlişkileri Anketi

Kardeşler arasındaki ilişkinin kalitesini çocuğun kendi bakış açısından ölçen bu anket, hem indeks çocuğa hem de kardeşe ayrı ayrı doldurtulmuştur [@furmanBuhrmester1985srq; @apalaci1996yoktez; @aktas2017kardesIliskileriOlcegi]. Beş şıklı (1= hiç, 5= çok fazla) 48 sorudan oluşan ölçek, kardeşler arası Sıcaklık, Güç/Statü, Çatışma ve Rekabet boyutlarını puanlamaktadır. 

### Beck Depresyon Envanteri

Annenin son bir haftadaki ruh hâlini, üzüntü veya çökkünlük durumunu saptayan dünyaca ünlü ve Türkiye geçerliliği sağlanmış 21 soruluk bir envanterdir [@hisli1989bdiTurkishUniversity]. Ölçekten en fazla 63 puan alınabilir. Biz analizlerimizde puanları "şu aralıktaysa hastadır" diyerek klinik bir damgalama yapmamayı seçtik; bunun yerine annenin depresif şiddetini istatistiklere sürekli bir puan olarak kattık. Yalnızca spesifik bir incelemede "puanı 17 ve üzerinde olanlar" riskli sayılarak geçici bir operasyonel gruplama yapılmıştır [@hisli1988bdiClinical].

Yüz yüze yürütülen derinlemesine görüşmeler (nitel kol) için bir anket kâğıdı kullanılmadığı için, soruların kapsamı nitel kısımdaki "Veri Toplama" başlığı altında anlatılmıştır."""
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success!")
    else:
        print("Failed to find:\n" + old[:100] + "...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
