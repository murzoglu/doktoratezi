import re

def process_file():
    with open("chapters/03_gerec_ve_yontem.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        # Evren ve Örneklem
        """## Evren ve Örneklem

Araştırmanın evrenini üç grup oluşturmuştur: tanımlanan iki merkezde izlenen 7–17 yaş aralığındaki T1DM tanılı çocuklar; aynı kurumlara başvuran, kronik hastalığı olmayan sağlıklı kontrol çocukları; ve bu çocukların 7–17 yaş aralığındaki sağlıklı kardeşleri ile anneleri. Örneklem birimi ailedir; her aileden bir indeks çocuk, aynı ailenin bir sağlıklı kardeşi ve ortak bir anne çalışmaya alınmıştır.

Çocuk-satırı düzeyinde her katılımcı dört rol etiketinden biriyle temsil edilmiştir: T1DM tanılı indeks çocuk, T1DM tanılı çocuğun sağlıklı kardeşi, sağlıklı kontrol indeks çocuğu ve sağlıklı kontrol çocuğunun sağlıklı kardeşi. Anne bildirimi ailenin indeks satırına gömülüdür. Final referans veri seti aile düzeyinde 241 aile, çocuk-satırı düzeyinde 482 çocuk gözlemi içermektedir. Rol dağılımı 120 T1DM tanılı indeks çocuk, 120 T1DM tanılı çocuğun sağlıklı kardeşi, 121 sağlıklı kontrol indeks çocuğu ve 121 sağlıklı kontrol kardeşi biçimindedir; böylece grup düzeyinde 240 T1DM ve 242 kontrol çocuk gözlemi elde edilmiştir. Kilitlenmiş kanonik veri tabanından aile düzeyi analiz tabanına, gruplara ve DM klinik alt-analiz katmanına geçişi özetleyen katılımcı akışı, epidemiyolojik raporlama kılavuzlarının önerdiği akış şeması biçiminde [@vandenbroucke2007strobe] bulgular bölümündeki @fig-strobe-flow içinde gösterilmiştir.

### Dahil edilme ve dışlanma ölçütleri

T1DM grubu için dahil edilme ölçütleri şunlardır:

- Tip 1 diyabet tanısı almış olmak;
- 7–17 yaş aralığında bulunmak;
- aynı yaş aralığında en az bir sağlıklı kardeşe sahip olmak;
- her iki ebeveynin hayatta olması;
- soruları anlayıp yanıtlayabilecek düzeyde Türkçe biliyor olmak.

Sağlıklı kontrol grubunda bu ölçütlere ek olarak çocuğun ve kardeşinin herhangi bir kronik hastalığının bulunmaması aranmıştır. Anneler için birincil bakım verenlerden biri olmak ve çocuklarıyla birlikte yaşamak koşulu getirilmiştir. Dışlanma nedenleri; T1DM dışında kronik hastalık veya engellilik bulunması, kardeşte kronik sağlık sorunu bulunması ve anne ya da babada engellilik bulunmasıdır. Katılımdan çekilme talebi, tutarsız yanıt örüntüsü ya da araştırmacı kararıyla çıkarılma durumlarında ilgili gönüllünün verileri çözümlemeye alınmamıştır. Çözümlemeye alınan tüm ailelerde her iki ebeveyn hayattadır ve annelerin büyük çoğunluğu evlidir; yalnızca iki ailede anne boşanmıştır. Tüm T1DM olgularının tanı yaşı klinik olarak olası aralıktadır.

### Örneklem büyüklüğü ve güç analizi

Nicel kol için birincil (*a priori*) örneklem büyüklüğü — yani veriyi toplamadan önce planlanan gerekli katılımcı sayısı — EMBU ve Kardeş İlişkileri Anketi alt ölçeklerinin her biri için hesaplanmıştır. Hesap, çift yönlü α = 0,05, %80 güç ve iki bağımsız grup ortalama karşılaştırması çerçevesinde [@cohen1988power] açık kaynaklı OpenEpi (sürüm 3.01) yazılımıyla yapılmıştır [@openepi2013]. Beklenen etki büyüklüğü (orta ilâ büyük düzey; yaklaşık d = 0,5–0,8) ve grup varyansları, ebeveynlik tutumu ve kardeş ilişkisi alanındaki önceki Türkçe çalışmalardan alınmıştır. Bu varsayımlarla grup başına asgari örneklem, büyük etki (d = 0,8) için yaklaşık 25, orta etki (d = 0,5) için yaklaşık 64 bireydir. Alt ölçek puanlarındaki değişkenliği karşılamak için grup başına en az 30 bireylik bir taban benimsenmiştir. Ulaşılan final örneklem grup başına yaklaşık 120 aileyle, orta-etki (d = 0,5) gereksiniminin belirgin biçimde üzerindedir ve etik kurulun öngördüğü asgari sayıyı aşmaktadır. Bu hesap iki grup ortalama farkı içindir; çok maddeli yapısal eşitlik (WLSMV), diadik doğrulayıcı faktör ve çok düzeyli modeller için ayrı bir *a priori* güç simülasyonu yürütülmediğinden, örneklem bu daha karmaşık modeller açısından sınırda kabul edilmelidir.

Bu birincil güç hesabı iki grup ortalama farkı içindir; çalışmanın çok düzeyli (aile içi yuvalanma), yapısal eşitlik (H4) ve aktör–partner (H2/H5 diadik) modellerinin örneklem gereksinimini doğrudan yansıtmaz. Bu karmaşık modeller için ayrı bir *a priori* güç hesabı yerine, tasarıma dayalı iki dayanak esas alınmıştır. Birincisi, çok düzeyli ve diadik modellerde asıl belirleyici toplam birey sayısından çok küme (aile) sayısıdır; yaklaşık 240 aileyle sağlanan küme sayısı, çok düzeyli modeller için önerilen kaba alt sınırların üzerindedir [@maas2005sufficient]. İkincisi, tek bir etki için gözlenen (retrospektif) güç hesaplamak yerine — gözlenen güç p değerinin birebir dönüşümü olduğundan ek bilgi taşımaz [@hoenigHeisey2001abusePower] — sonuçların belirsizliği doğrudan etki büyüklüğü güven aralıkları, Bayesçi güvenilir aralıklar ve eşdeğerlik (TOST) sınırlarıyla raporlanmıştır. Yapısal eşitlik ve çok düzeyli modeller için gerektiğinde `simr` ve `pwr` paketleriyle Monte Carlo/simülasyon temelli hassasiyet çözümlemesi tamamlayıcı olarak değerlendirilmiştir [@green2016simr]. Örneklemin yapısal olarak sınırlı kaldığı tek çözümleme, yalnız 39 T1DM indeks çocukta klinik HbA1c değerinin bulunduğu DM'ye özgü alt çözümlemelerdir; bu katman düşük güç nedeniyle doğrulayıcı değil, yalnız betimsel/keşifsel olarak konumlandırılmıştır.

Nitel kolun örneklem büyüklüğü ise sayısal güç yerine bilgi gücü çerçevesiyle gerekçelendirilmiştir; ilgili değerlendirme nitel kolun kendi alt başlığında sunulmuştur.

### Örnekleme yöntemi

Nicel kolda katılımcılar ardışık örneklemeyle alınmıştır: dahil edilme ölçütlerini karşılayan ve polikliniğe başvuran tüm ailelere katılım daveti yapılmıştır. Kontrol grubu, indeks çocukların yaş ve cinsiyet dağılımı bakımından karşılaştırılabilir sağlıklı çocuklar ve aileleri arasından oluşturulmuştur. Nitel alt örneklem ise ardışık/olasılıklı seçim yerine amaçlı örneklemeyle (*purposive sampling*) oluşturulmuş; bu örneklemin oluşturulması ve katılım süreci nitel kolun ilgili alt başlığında ayrıntılandırılmıştır.

## Değişkenler ve Tanımları""":
        
        """## Evren ve Örneklem

Araştırmanın hedef evrenini; belirtilen iki merkezde takip edilen 7–17 yaş aralığındaki T1DM tanılı çocuklar, eşdeğer yaş ve demografik özelliklere sahip sağlıklı kontrol çocukları ve bu çocukların 7–17 yaş aralığındaki sağlıklı kardeşleri ile anneleri oluşturmaktadır. Örneklem birimi doğrudan ailedir; her aileden bir indeks çocuk, bir sağlıklı kardeş ve aileyi temsil eden bir anne çalışmaya dâhil edilmiştir.

Veri setinde her katılımcı çocuğun pozisyonu dört rolden biri ile etiketlenmiştir: T1DM tanılı indeks çocuk, T1DM çocuğun sağlıklı kardeşi, sağlıklı kontrol indeks çocuğu ve sağlıklı kontrol çocuğunun sağlıklı kardeşi. Annenin bildirimleri indeks çocuk satırına entegre edilmiştir. Nihai çalışma grubunda toplam 241 aile ve bu ailelere ait 482 çocuk gözlemi yer almaktadır. Gruplar 120 diyabet ailesi ve 121 kontrol ailesi olacak şekilde dağılmış; toplam 240 diyabet ve 242 kontrol çocuk gözlemine ulaşılmıştır. Katılımcıların çalışmaya dâhil edilme aşamaları ve alt-analiz gruplarına ayrılma akışı epidemiyoloji standartlarına uygun olarak [@vandenbroucke2007strobe] @fig-strobe-flow şemasında sunulmuştur.

### Dahil edilme ve dışlanma ölçütleri

Tip 1 diyabetli ailelerin araştırmaya dâhil edilme koşulları şunlardır:

- Çocuğun Tip 1 diyabet tanısı almış olması,
- İndeks çocuğun 7–17 yaş aralığında bulunması,
- Aynı ailede ve aynı yaş aralığında kronik hastalığı bulunmayan en az bir sağlıklı kardeşin varlığı,
- Çocuğun her iki ebeveyninin de hayatta olması,
- Katılımcıların Türkçe anket sorularını anlayıp yanıtlayabilecek dil yetkinliğine sahip olması.

Sağlıklı kontrol grubunda bu şartlara ilaveten indeks çocukta ve kardeşte herhangi bir kronik hastalık bulunmaması ölçütü aranmıştır. Anneler için temel koşul, birincil bakım veren olarak çocuklarıyla aynı evde yaşamalarıdır. Tip 1 diyabet dışındaki ek kronik hastalıklar, engellilik durumları veya ebeveynlerdeki engellilik halleri dışlanma nedeni sayılmıştır. Ayrıca eksik ya da tutarsız anket dolduran katılımcıların verileri güvenlik amacıyla çözümleme dışı bırakılmıştır. Çalışmaya kabul edilen tüm ailelerde ebeveynler hayattadır; annelerin neredeyse tamamı evlidir (yalnızca iki ailede anne boşanmıştır). T1DM grubundaki çocukların tanı yaşları klinik literatürle tam uyumludur.

### Örneklem büyüklüğü ve güç analizi

Çalışmanın ihtiyaç duyduğu asgari aile sayısı, veri toplanmaya başlanmadan önce OpenEpi (sürüm 3.01) yazılımı kullanılarak hesaplanmıştır [@openepi2013; @cohen1988power]. Literatürdeki benzer ebeveynlik araştırmalarına dayanılarak, iki grup arasında orta veya büyük düzeyde bir fark saptanabilmesi için grup başına en az 64 ailenin yeterli olacağı öngörülmüştür. Gerçekleşen nihai katılım ise grup başına yaklaşık 120 aile ile bu asgari hedefin oldukça üzerine çıkarak etik kurulun onayladığı sayıyı aşmıştır.

Çok düzeyli (multilevel) ve yapısal eşitlik (SEM) gibi daha karmaşık veri modellemeleri, toplam katılımcı sayısından ziyade küme (aile) sayısına duyarlıdır. Ulaşılan ~240 ailelik havuz, bu tür karmaşık modellerin çalıştırılabilmesi için önerilen kaba alt sınırların güvenle üzerindedir [@maas2005sufficient]. Geriye dönük p-değeri bazlı güç hesapları genellikle yanıltıcı olduğundan [@hoenigHeisey2001abusePower], bu çalışmada istatistiksel sonuçların belirsizlik payları güven aralıkları (GA), Bayesçi aralıklar ve pratikte eşdeğerlik (TOST) sınırlarıyla daha dürüst bir yaklaşımla raporlanmıştır. Çalışmada örneklem hacminin yetersiz kaldığı tek kısım, çocukların kan şekeri kontrol (HbA1c) verisinin yalnızca 39 T1DM indeks çocukta bulunabildiği diyabete özgü klinik ek incelemelerdir; bu nedenle ilgili bölüm "kesin yargı" değil "keşifsel/betimsel bulgu" olarak raporlanmıştır. Nitel (yüz yüze görüşme) bölümünün kişi sayısı ise istatistiksel matematik kurallarına göre değil, görüşmelerin ürettiği niteliksel "bilgi gücüne" göre belirlenmiş ve kendi alt başlığında açıklanmıştır.

### Örnekleme yöntemi

Nicel kısımdaki katılımcılar, dahil edilme şartlarını sağlayan ve ilgili dönemde polikliniğe başvuran uygun hastalardan (ardışık örneklem) seçilmiştir. Kontrol grubu ise hasta gruptaki çocukların yaşlarına ve cinsiyetlerine benzer özellikler gösteren sağlıklı çocuklardan eşleştirilerek oluşturulmuştur. Görüşmelerin yapıldığı nitel alt örneklemde ise rastgele bir alım yerine "farklı hastalık sürelerine ve aile yapılarına" ışık tutacak zengin bir profil hedeflendiği için özel seçim (amaçlı örneklem) uygulanmıştır.

## Değişkenler ve Tanımları"""
    }

    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            print("Successfully replaced section 3.3!")
        else:
            print("Failed to replace section 3.3!")

    with open("chapters/03_gerec_ve_yontem.qmd", "w", encoding="utf-8") as f:
        f.write(content)

process_file()
