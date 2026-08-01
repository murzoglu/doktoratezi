import re

def process_file():
    with open("chapters/03_gerec_ve_yontem.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        """### Demografik ve tıbbi bilgi formu

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

Nitel kolun yarı yapılandırılmış görüşme rehberi bir ölçme aracı niteliğinde olmadığından, nitel veri toplama sürecinin bir parçası olarak ilgili alt başlıkta tanımlanmıştır (bkz. Nitel Veri Toplama).""":
        
        """### Demografik ve tıbbi bilgi formu

Araştırmacı tarafından geliştirilen bu form, aile üyelerinin kimlik ve iletişim bilgileri ile çocuk sayısı ve yaş sırası gibi demografik özellikleri içermektedir. Ailenin eğitim, meslek, konut durumu gibi sosyoekonomik göstergeleri ile ebeveyne veya diyabetli çocuğa ait klinik (tanı tarihi, diyabet süresi, HbA1c vb.) bilgiler de aynı formla toplanmıştır. Form üzerindeki açık uçlu metin (meslek vb.) girişleri, analizlerden önce standart kategorik değişkenlere kodlanmıştır.

### Kısaltılmış Algılanan Ebeveyn Tutumları Ölçeği – Çocuk Formu (s-EMBU-C)

Çocuğun kendi annesinin ebeveynlik tutumunu nasıl hissettiğini ölçen s-EMBU-C, özgün yapısı Dirik ve arkadaşları [@dirik2015sEmbuTurkish] tarafından Türkçeye uyarlanmış bir ölçüm aracıdır [@arrindell2005sembu; @castro1993embuChildren]. Ölçek bu araştırmada, çocukların güncel ebeveynlik hissini doğrudan puanlayabilmeleri için şimdiki zaman kipiyle uygulanmıştır. Toplam 29 sorudan oluşan anket, çocukların 1 ("en düşük sıklık") ile 4 ("en yüksek sıklık") arasında puanlama yapması (Likert) esasına dayanır; yüksek puan ilgili ebeveynlik özelliğinin (örneğin sıcaklık) daha yoğun hissedildiğine işaret eder. Ölçek toplamda dört tutum boyutu sunar: Duygusal Sıcaklık (9 soru), Aşırı Koruma (7 soru), Reddetme (8 soru) ve Sümer ve arkadaşları tarafından eklendiği üzere [@sumer2010anneBabaTutum] çocuğun diğer kardeş veya akranlarla akademik/sosyal olarak mukayese edildiğini yansıtan Karşılaştırma (5 soru).

Çocuğun "Dışarıda oynamama izin verir mi?" sorusu gibi olumlu yöndeki ifadeler (q25), analiz aşamasında aşırı koruma temasıyla uyumlu olacak şekilde tersten (matematiksel olarak) çevrilerek puanlanmıştır. Böylece hem anne formunda hem de çocuk formunda, alınan yüksek puan "yüksek düzeyde aşırı korumayı" göstermektedir (bkz. @tbl-q25-yon). Ölçek bu çalışmadaki indeks çocuklara ve kardeşlere uygulanmış olup, araştırma grubuna uygun olarak ne kadar güvenilir ölçüm yaptığı ayrı bir ön-analiz sürecinden (psikometrik değerlendirme) geçirilmiştir (bkz. Ölçme Araçlarının Psikometrik Değerlendirmesi).

| Madde | Form | Alt ölçek | Sözel yön | Ham kodlama | Ters puanlama | Yüksek final puanın anlamı |
|-------|------|-----------|-----------|-------------|---------------|-----------------------------|
| q25 | Çocuk (s-EMBU-C) | Aşırı Koruma | İzin verme ("…izin verir mi?") | 1–4 | Var ($5-x$) | Daha yüksek aşırı koruma |
| q25 | Ebeveyn (s-EMBU-P) | Aşırı Koruma | Kısıtlama ("…hiç izin vermem") | 1–4 | Yok | Daha yüksek aşırı koruma |

: q25 maddesinin çocuk ve ebeveyn formlarında sözel yönü ve ters puanlama kararı. İki formda sözel yön zıt olduğundan yalnız çocuk maddesi ters puanlanır; her iki formda yüksek final puan daha yüksek aşırı korumayı gösterir. {#tbl-q25-yon}

### Kısaltılmış Algılanan Ebeveyn Tutumları Ölçeği – Ebeveyn Formu (s-EMBU-P)

Annenin "kendini ebeveyn olarak nasıl değerlendirdiğini" ölçen s-EMBU-P formu [@arrindell2005sembu], çocuk formundaki 29 sorunun birebir aynısını annenin kendi gözünden sormaktadır. Anne, anketi indeks (temel) çocuk üzerinden yanıtlamıştır. Çocuk ile anne sorularının aynı olması, "çocuğun algısı ile annenin kendi bildirimi" (diadik) arasındaki uyuşmazlığın matematiksel olarak (doğrudan) kıyaslanabilmesini sağlamaktadır. Anne formu da çalışma örneklemine uygunluğu teyit edilmek üzere güvenilirlik sınamalarından geçmiştir.

### Kardeş İlişkileri Anketi

Kardeşler arası ilişkinin doğasını ölçen bu anket [@furmanBuhrmester1985srq], Apalaçi (1996) tarafından Türkçeye uyarlanmıştır [@apalaci1996yoktez]. Toplam 48 sorudan oluşan ölçek; 1 ("hemen hemen hiç") ile 5 ("çok çok fazla") arasında yanıtlanır ve "Sıcaklık/Yakınlık", "Statü/Güç", "Çatışma", "Rekabet" olmak üzere dört temel boyut sunar. Anket hem indeks çocuğa hem de sağlıklı kardeşe verilmiş olup, "kardeşler ebeveynlerini paylaşırken ne hissediyor" eksenindeki yönlü sorular istatistiksel hesaplamalarda dikkatle işlenmiştir (bkz. [@aktas2017kardesIliskileriOlcegi]).

### Beck Depresyon Envanteri

Annenin psikolojik duygu durumunu ölçen envanter, Hisli'nin (1989) Türkçe uyarlaması temel alınarak kullanılmıştır [@hisli1989bdiTurkishUniversity]. Anket 21 sorudan oluşur, her soru 0 ile 3 puan arasında değerlendirilir ve toplam puan en fazla 63 olabilir. Analizlerde bu puan sürekli (kesintisiz) bir değer olarak kullanılmıştır. Klinik olarak kimin "hafif", kimin "ağır" depresyonda olduğu şeklinde yapay sınıflandırmalar, Türkiye örnekleminde kesinleşmiş tek bir standart olmaması nedeniyle doğrudan (raporlama amacıyla) kullanılmamıştır. Ancak keşifsel (ikincil) analizlerde, "hangi anne grubunun daha riskli/farklı bir ebeveynliğe sahip olduğunu" anlamak amacıyla, literatürdeki operasyonel sınır (toplam ≥ 17 puan) bir uyarı/ayıraç noktası olarak alınmıştır [@hisli1988bdiClinical]; bu puan seviyesi doğrudan bir psikiyatrik tanıyı işaret etmez.

Nitel (yüz yüze) kolda kullanılan açık uçlu sorular (yarı yapılandırılmış rehber), klasik bir ölçek formundan ziyade bir mülakat rotası olduğundan ilgili başlık altında ayrıntılandırılmıştır (bkz. Nitel Veri Toplama)."""
    }

    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            print("Successfully replaced section 3.6!")
        else:
            print("Failed to replace section 3.6!")

    with open("chapters/03_gerec_ve_yontem.qmd", "w", encoding="utf-8") as f:
        f.write(content)

process_file()
