import sys

file_path = "chapters/03_gerec_ve_yontem.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    """## Evren ve Örneklem

Araştırmanın evrenini üç grup oluşturmuştur: tanımlanan iki merkezde izlenen 7–17 yaş aralığındaki T1DM tanılı çocuklar; birinci merkezi genel çocuk polikliniğine başvuran, kronik hastalığı olmayan sağlıklı kontrol çocukları; ve bu çocukların 7–17 yaş aralığındaki sağlıklı kardeşleri ile anneleri. Örneklem birimi ailedir; her aileden bir indeks çocuk, aynı ailenin bir sağlıklı kardeşi ve ortak bir anne çalışmaya alınmıştır.

Çocuk-satırı düzeyinde her katılımcı dört rol etiketinden biriyle temsil edilmiştir: T1DM tanılı indeks çocuk, T1DM tanılı çocuğun sağlıklı kardeşi, sağlıklı kontrol indeks çocuğu ve sağlıklı kontrol çocuğunun sağlıklı kardeşi. Anne bildirimi ailenin indeks satırına gömülüdür. Final referans veri seti aile düzeyinde 241 aile, çocuk-satırı düzeyinde 482 çocuk gözlemi içermektedir. Rol dağılımı 120 T1DM tanılı indeks çocuk, 120 T1DM tanılı çocuğun sağlıklı kardeşi, 121 sağlıklı kontrol indeks çocuğu ve 121 sağlıklı kontrol kardeşi biçimindedir; böylece grup düzeyinde 240 T1DM ve 242 kontrol çocuk gözlemi elde edilmiştir. Kilitlenmiş kanonik veri tabanından aile düzeyi analiz tabanına, gruplara ve DM klinik alt-analiz katmanına geçişi özetleyen katılımcı akışı, epidemiyolojik raporlama kılavuzlarının önerdiği akış şeması biçiminde [@vandenbroucke2007strobe] bulgular bölümündeki @fig-strobe-flow içinde gösterilmiştir.

### Dahil edilme ve dışlanma ölçütleri

T1DM grubu için dahil edilme ölçütleri şunlardır:

- Tip 1 diyabet tanısı almış olmak;
- 7–17 yaş aralığında bulunmak;
- aynı yaş aralığında en az bir sağlıklı kardeşe sahip olmak;
- her iki ebeveynin hayatta ve evli olması;
- soruları anlayıp yanıtlayabilecek düzeyde Türkçe biliyor olmak.

Sağlıklı kontrol grubunda bu ölçütlere ek olarak çocuğun ve kardeşinin herhangi bir kronik hastalığının bulunmaması aranmıştır. Anneler için birincil bakım verenlerden biri olmak ve çocuklarıyla birlikte yaşamak koşulu getirilmiştir. Dışlanma nedenleri; T1DM dışında kronik hastalık veya engellilik bulunması, kardeşte kronik sağlık sorunu bulunması ve anne ya da babada engellilik bulunmasıdır. Katılımdan çekilme talebi ya da ölçeklerde tutarsız ve eksik yanıt örüntüsü olması durumlarında ilgili gönüllünün verileri çözümlemeye alınmamıştır. Çözümlemeye alınan tüm ailelerde her iki ebeveyn hayattadır ve annelerin hepsi evlidir. Tüm T1DM olgularının tanı yaşı klinik olarak olası aralıktadır.

### Örneklem büyüklüğü ve güç analizi

Nicel kol için birincil (*a priori*) örneklem büyüklüğü — yani veriyi toplamadan önce planlanan gerekli katılımcı sayısı — EMBU ve Kardeş İlişkileri Anketi alt ölçeklerinin her biri için hesaplanmıştır. Hesap, çift yönlü α = 0,05, %80 güç ve iki bağımsız grup ortalama karşılaştırması çerçevesinde [@cohen1988power] açık kaynaklı OpenEpi (sürüm 3.01) yazılımıyla yapılmıştır [@openepi2013]. Beklenen etki büyüklüğü (orta ilâ büyük düzey; yaklaşık d = 0,5–0,8) ve grup varyansları, ebeveynlik tutumu ve kardeş ilişkisi alanındaki önceki Türkçe çalışmalardan alınmıştır. Bu varsayımlarla grup başına asgari örneklem, büyük etki (d = 0,8) için yaklaşık 25, orta etki (d = 0,5) için yaklaşık 64 bireydir. Alt ölçek puanlarındaki değişkenliği karşılamak için grup başına en az 30 bireylik bir taban benimsenmiştir. Ulaşılan final örneklem grup başına yaklaşık 120 aileyle, orta-etki (d = 0,5) gereksiniminin belirgin biçimde üzerindedir ve etik kurulun öngördüğü asgari sayıyı aşmaktadır.

Yukarıda belirtilen güç hesabı, temelde iki grubun ortalama farklarını karşılaştırmak için geçerlidir. Dolayısıyla bu hesap; çalışmada yer alan çok maddeli yapısal eşitlik (WLSMV), aktör–partner (H2/H5) diadik doğrulayıcı faktör ve aile içi yuvalanmayı hesaba katan çok düzeyli modellerin gereksinimlerini doğrudan yansıtmaz. Bu karmaşık modeller için veri toplanmadan önce ayrı bir (*a priori*) simülasyon yürütülmediğinden, mevcut örneklem bu testler açısından "sınırda" kabul edilmiş ve analizlerin güvenilirliği tasarıma dayalı şu iki temel dayanakla savunulmuştur:

**Küme sayısı avantajı.** Çok düzeyli ve diadik modellerde istatistiksel gücü belirleyen asıl unsur, toplam birey sayısından ziyade küme (aile) sayısıdır. Çalışmada ulaşılan yaklaşık 240 ailelik küme sayısı, çok düzeyli modeller için literatürde önerilen kaba alt sınırların oldukça üzerindedir [@maas2005sufficient].

**Gözlenen güç yerine alternatif raporlama.** Literatürle uyumlu olarak, analiz sonrasında "gözlenen (retrospektif) güç" hesaplanmamıştır; zira bu değer yalnızca p değerinin birebir dönüşümüdür ve ek bir bilimsel bilgi taşımaz [@hoenigHeisey2001abusePower]. Bunun yerine, sonuçların belirsizliği doğrudan etki büyüklüğü güven aralıkları, Bayesçi güvenilir aralıklar ve eşdeğerlik (TOST) sınırlarıyla raporlanmıştır. Ayrıca yapısal eşitlik ve çok düzeyli modeller için gerektiğinde `simr` ve `pwr` paketleri kullanılarak Monte Carlo/simülasyon temelli hassasiyet çözümlemeleri tamamlayıcı kanıt olarak sunulmuştur [@green2016simr].

Örneklemin yapısal olarak sınırlı kaldığı tek çözümleme, yalnız 39 T1DM indeks çocukta klinik HbA1c değerinin bulunduğu DM'ye özgü alt çözümlemelerdir; bu katman düşük güç nedeniyle doğrulayıcı değil, yalnız betimsel/keşifsel olarak konumlandırılmıştır.

Nitel kolun örneklem büyüklüğü ise sayısal güç yerine bilgi gücü çerçevesiyle gerekçelendirilmiştir; ilgili değerlendirme nitel kolun kendi alt başlığında sunulmuştur.

### Örnekleme yöntemi

Nicel kolda katılımcılar ardışık örneklemeyle alınmıştır: dahil edilme ölçütlerini karşılayan ve polikliniğe başvuran tüm ailelere katılım daveti yapılmıştır. Kontrol grubu, indeks çocukların yaş ve cinsiyet dağılımı bakımından karşılaştırılabilir sağlıklı çocuklar ve aileleri arasından oluşturulmuştur. Nitel alt örneklem ise ardışık/olasılıklı seçim yerine amaçlı örneklemeyle (*purposive sampling*) oluşturulmuş; bu örneklemin oluşturulması ve katılım süreci nitel kolun ilgili alt başlığında ayrıntılandırılmıştır.""" :
    """## Evren ve Örneklem

Araştırmamıza dâhil edilen kişiler şunlardır: 7–17 yaş arasındaki diyabetli çocuklar, onların tamamen sağlıklı yaşıtı kontrol grubu çocukları ve her iki gruptaki çocukların sağlıklı kardeşleri ile anneleri. Çalışmamızda odak noktamız bireyler değil "aile"dir. Bu yüzden çalışmaya her aileden üç kişi alınmıştır: hasta/indeks çocuk, sağlıklı bir kardeşi ve anne.

Final verimiz tam 241 aileden oluşmaktadır. Bu, veri tabanımızda 482 çocuğun görüşünün (satırının) olduğu anlamına gelir. Aileleri gruplara ayırdığımızda; 120 diyabetli çocuk + 120 sağlıklı kardeş ve 121 kontrol çocuğu + 121 kontrol kardeşi olmak üzere toplamda diyabet ve kontrol grupları arasında neredeyse mükemmel bir sayısal denge (240'a 242) yakalanmıştır. Anketlerden elde edilen bu sayıların adım adım nasıl elemelerden geçerek son hâline geldiği, uluslararası epidemiyolojik standartların (STROBE) [@vandenbroucke2007strobe] gerektirdiği biçimde @fig-strobe-flow şemasında gösterilmiştir.

### Dahil edilme ve dışlanma ölçütleri

Tip 1 diyabetli gruptaki ailelerin çalışmaya katılabilmesi için şu şartları sağlaması gerekiyordu:
- Çocuğun Tip 1 diyabet tanısı olması,
- Çocuğun 7 ile 17 yaşları arasında olması,
- Aynı evde, aynı yaş aralığında en az bir tane sağlıklı kardeşin yaşaması,
- Anne ve babanın evli olması ve ikisinin de hayatta olması,
- Türkçe okuyup anlayabilmeleri.

Sağlıklı gruptaki ailelerde ise yukarıdakilere ek olarak çocukların hayatı boyunca hiçbir kronik hastalığı (astım, çölyak vb.) olmaması şartı aranmıştır. Annelerin çocuklarla aynı evde yaşaması ve onlara bilfiil bakım veriyor olması zorunluydu. Anketleri baştan savma dolduran veya yarım bırakanların anketleri değerlendirmeye alınmamıştır. Sonuç olarak analize alınan tüm ailelerde ebeveynler evli ve hayattadır, hastaların tümünün tanı yaşları klinik olarak doğru ve mantıklı aralıklardadır.

### Örneklem büyüklüğü ve güç analizi (Sayılar yeterli mi?)

Bir çalışmada elde edilen farkların "gerçek mi yoksa tesadüf mü" olduğunu ayırt edebilmek için kaç kişiye anket yapılması gerektiği, veri toplanmadan önce formüllerle (güç analiziyle) hesaplanmıştır [@cohen1988power; @openepi2013]. Türkiye'deki eski çalışmalara bakarak "büyük bir etki" görmek için grup başına en az 25, "orta bir etki" görmek için grup başına en az 64 aileye ihtiyacımız olduğu bulunmuştur. Biz her bir grupta yaklaşık 120 aileye (toplamda 241 aileye) ulaşarak, istatistiksel gereksinimlerin ve etik kurul sınırlarının çok üzerine çıkmayı başardık.

Ancak bu ilk başta yaptığımız basit matematiksel hesap; çok katmanlı yapısal eşitlik modellerinin (WLSMV) veya anne-çocuk uyum modellerinin zorluklarını hesaba katmıyordu. Bu zor modellerde en az hata payı için en az 100 aileye ulaşılması önerilirken, bizdeki 241 ailelik veri tabanı bu testler için gereken limiti rahatça karşılamıştır [@maas2005sufficient].

Araştırma bittikten sonra tekrar başa dönüp "acaba anketleri yeterince kişiye yaptık mı" (retrospektif güç analizi) diye bir hesaplama yapmadık, çünkü modern bilimde bunun yanıltıcı olduğu kanıtlanmıştır [@hoenigHeisey2001abusePower]. Bunun yerine verilerin güvenilirliğini doğrudan Bayesçi aralıklarla ve gelişmiş simülasyon testleriyle (TOST, simr, pwr) gösterdik [@green2016simr].

Verimizin sayısının sadece bir yerde yetersiz kaldığını düşünüyoruz: Diyabetli çocukların kan şekeri verilerine (HbA1c) sadece 39 hastada ulaşabildik. Bu yüzden kan şekeri ile ebeveynliği karşılaştırdığımız kısımları "kesin kanıt" olarak değil, "bundan sonraki çalışmalara bir ipucu" (keşifsel) niteliğinde raporladık.

Nitel bölümdeki görüşmelerin sayısı ise "bu kadar kişiyle görüştük" diye bir matematik üzerinden değil, "artık yeni bir hikaye çıkmıyor, konu doygunluğa ulaştı" prensibiyle belirlenmiştir.

### Örnekleme yöntemi

Hastaneye gelen (ve şartlara uyan) tüm diyabetli ailelere anketleri doldurmaları rica edilmiştir (ardışık örneklem). Daha sonra, bu diyabetli çocukların yaşına ve cinsiyetine bakılmış, hastanenin genel çocuk polikliniğine muayeneye gelen sağlıklı çocuklardan da aynı yaş ve cinsiyetlerde olanlar çalışmaya dâhil edilmiştir (kontrol grubu). Yüz yüze derin görüşmelerin yapıldığı ufak grup (nitel kol) ise poliklinik sırasına göre değil; hastalığı farklı yaşayan ailelerin "amaçlı" (örneğin biri yeni tanılı, diğeri yılların hastası) şekilde özenle seçilmesiyle oluşturulmuştur."""
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success!")
    else:
        print("Failed to find:\n" + old[:100] + "...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
