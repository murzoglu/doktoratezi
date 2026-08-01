import sys

file_path = "chapters/05_tartisma_ve_sonuc.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    """Diadik tutarlılık, bu karma tezin birincil katkısının bütünleştiği düzlemdir. H5
kapsamında anne ↔ indeks çocuk uyumu beş paralel strateji ile değerlendirilmiş,
ön-kayıtlı üçgenleme koşulu karşılanmamış ve baskın manifest kanıt dört boyutun
tamamında uyumun düşük seyrettiğini göstermiştir (Bulgular, @tbl-apa-h5-concordance).
Nicel kol bu ayrışmanın *ne* ve *ne kadar* olduğunu ölçer; niteliksel kol *neden ve
nasıl*'ını yanıtlar. Nicel taraftaki bulgu alanyazınla büyük ölçüde tutarlıdır. Korelitz
ve Garber'in 85 çalışma ve 476 etki büyüklüğünü birleştiren meta-analizinde
ebeveyn-çocuk ebeveynlik-algısı uyumu yalnız ılımlı-düşüktür (kabul boyutunda anne-çocuk
r = 0,28, davranışsal kontrolde r = 0,23, psikolojik kontrolde r = 0,27). Ebeveynler
kendilerini çocuklarından sistematik biçimde daha olumlu bildirir (kabulde g = −0,21,
psikolojik kontrolde g = 0,54). Dahası uyum klinik örneklemlerde daha da düşer (kabulde
r = 0,09) [@korelitz2016congruence]. Achenbach ve arkadaşlarının 119 çalışmalık klasik
meta-analizinde farklı tür bilgi-vericiler arası uyum ortalama r = 0,28, özne ile
diğerleri arası r = 0,22 düzeyindedir; yazarlar bu düşük uyumu geçersizlik değil
"durumsal özgüllük" olarak yorumlar [@achenbach1987crossinformant]. Bu nedenle mevcut
çalışmadaki düşük uyum salt bir ölçüm başarısızlığına indirgenemez ve bilgi-verici
ayrışmasına ilişkin kuramsal beklentiyle uyumludur. Bununla birlikte ölçüm güvenirliği,
madde/eşik işleyişi ve yanıt süreçlerindeki farklılıkların katkısı bu tasarımda
dışlanamaz [@deLosReyes2015].""":
    """Çalışmamızın belki de en önemli bulgularından biri, anne ile çocuğun aynı evdeki 'ebeveynliği' ne kadar farklı algıladıklarıdır (H5). Beş farklı yöntemle yaptığımız inceleme, annenin kendi ebeveynliği ile çocuğun bunu nasıl hissettiği arasındaki uyumun son derece düşük olduğunu göstermiştir (Bulgular, @tbl-apa-h5-concordance). Sayısal veriler bize uyumun ne kadar kopuk olduğunu gösterirken, tezin niteliksel tarafı bunun nedenlerini açıklar. 

Aslında bu kopukluk bilimsel literatürün de beklediği bir durumdur. Korelitz ve Garber'in 85 araştırmayı özetlediği çalışmasında, anne-çocuk arasındaki algı uyumunun genellikle zayıf olduğu (r = 0,23-0,28 bandında) saptanmıştır. Dahası, anneler her zaman kendilerini çocuklarının onları gördüğünden daha 'olumlu' değerlendirme eğilimindedir. Diyabet gibi hastalıkların olduğu klinik gruplarda ise bu uyum neredeyse sıfıra yaklaşmaktadır [@korelitz2016congruence]. Ünlü araştırmacı Achenbach da bu durumu "birinin yalan söylemesi veya ölçümün yanlış olması" olarak değil, "herkesin o durumu kendi penceresinden (durumsal özgüllük) haklı olarak farklı yaşaması" biçiminde açıklamıştır [@achenbach1987crossinformant]. Kısacası, anne ve çocuğun farklı şeyler söylemesi anketin bir hatası değil, gerçekliğin kendisidir [@deLosReyes2015].""",

    """De Los Reyes ve Kazdin'in geliştirdiği Atıf-Yanlılığı Bağlam Modeli'ne göre, farklı
bilgi-vericiler aynı çocuğu farklı ortamlarda (ev, okul) gözler ve gözledikleri
davranışın nedenini farklı kaynaklara bağlar; bu nedenle raporları arasındaki fark,
birinin "yanılması" değil, her birinin kendi bağlamına özgü geçerli bilgiyi taşımasıdır.
Aynı yazarların "operasyonlar üçlüsü" ilkesi de bir yapıyı farklı yöntemlerle ölçmenin
sonuçları zorunlu olarak yakınsatmayacağını belirtir; yöntemler ıraksadığında bu
yalnızca ölçüm hatası değil, "ıraksayan operasyonlar" olarak da değerlendirilebilir. Bu
çerçevede, mevcut çalışmada beş farklı uyum stratejisinin aynı yönde birleşmemesi bir
başarısızlık değil, beklenen bir sonuçtur [@deLosReyesKazdin2005;
@deLosReyes2021needsGoals]; düşük uyumun bir ölçüm-değişmezliği ihlali gibi okunmaması
gerektiği de vurgulanmıştır [@delosReyes2022discrepancies].""":
    """De Los Reyes ve Kazdin, annenin, çocuğun veya öğretmenin aynı çocuğa bakıp bambaşka sonuçlar çıkarmasını şöyle açıklar: Her biri çocuğu farklı bir bağlamda, farklı amaçlarla gözlemler. Çocuğun evdeki tavrı ile okul veya hastanedeki tavrı aynı olamaz. Dolayısıyla ifadeler uyuşmadığında kimse 'yanılmaz', aksine her biri kendi bulunduğu bağlamın doğrusunu söyler [@deLosReyesKazdin2005; @deLosReyes2021needsGoals]. Bu gözle bakıldığında, araştırmamızda annelerin ve çocukların cevaplarının birleşmemesi bir ölçüm veya anket hatası değil, gayet beklenen, doğal bir bulgudur [@delosReyes2022discrepancies].""",

    """Bu ayrışmanın kaynağını, Branje ve arkadaşlarının 288 Hollandalı aileyi dört üye
üzerinden inceleyen çalışması aydınlatır. Bu çalışma "Sosyal İlişkiler Modeli" adı
verilen bir yöntem kullanır. Yöntem, bir kişinin bir başkasına ilişkin yargısını üç
kaynağa ayırır:

- yargılayanın genel eğilimi (başkalarını olumlu ya da olumsuz değerlendirmeye
  yönelik istikrarlı yatkınlık);
- hedef kişinin herkeste uyandırdığı ortak izlenim;
- yalnız o iki kişi arasındaki ilişkiye özgü, kimseyle paylaşılmayan bileşen.

Sonuçlar, ebeveynlerin yargılarının %60'ının bu kaynaklarla açıklanabildiğini,
ergenlerde bu oranın %46'ya düştüğünü göstermiştir; dahası ilişkiye-özgü bileşen
ebeveynlerde (%29) ergenlerden (%12) çok daha ağır basmaktadır
[@branje2003srmFamilyPerception]. Dolayısıyla anne ile çocuk aynı ilişkiyi büyük ölçüde
farklı kaynaklardan beslenerek algılamaktadır; bu da düşük uyumun neden beklenen bir
sonuç olduğunu yapısal düzeyde açıklar.

Tezin özgün katkısı bu noktada belirginleşir:
aynı aile gerçekliğinin üç rol tarafından farklı biçimde deneyimlendiğini gösteren
niteliksel triadik okuma, düşük diadik uyumun ölçüm hatasına indirgenemeyecek,
rol-temelli bir deneyim farkını yansıttığını düşündürür. Anne düzen ve güvenlik dilini,
T1DM'li çocuk beden-özerklik ve sosyal görünürlük dilini, sağlıklı kardeş ise kısıtlanma
ve adalet dilini öne çıkarmaktadır. Böylece bu çalışmanın birincil katkısı tek bir
"T1DM ebeveynlik farkı" tanımlaması değil; ayrışmanın hangi bilgi-verici, hangi boyut ve
hangi deneyim düzleminde gerçekleştiğinin haritalanmasıdır — bu harita yalnız
çok-bilgi-verici nicel tasarım ile triadik nitel tasarımın birlikte kurulmasıyla
üretilebilir. Nitel kolun burada nicel uyumu *açıkladığı*, *kanıtlamadığı* disiplini""":
    """Bu algı farkının kökeni, Branje ve ekibinin 288 aileyi inceleyen araştırmasında daha iyi anlaşılır. Bir insanın başkası hakkındaki düşüncesi sadece karşıdakinden değil; kendi huyundan, toplumun o kişi hakkındaki genel izleniminden ve ikisi arasındaki "bize özel" dediğimiz sırdan oluşur. Annelerin çocuklarına bakışı ağırlıklı olarak "sadece ikimize özel bağ" üzerinden şekillenirken, çocuklar bu duruma daha farklı pencerelerden bakarlar [@branje2003srmFamilyPerception].

Tam da bu sebeple tezimizin en özgün tarafı şudur: "Neden anne ve çocuk uyuşmuyor?" sorusunun cevabını niteliksel derin görüşmelerimiz vermiştir. Diyabetli bir ailede anne "düzen, güvence ve tıbbi sorumluluk" diliyle konuşurken, diyabetli çocuk "bedenime müdahale etme, arkadaşlarım bana acımasın" diliyle, sağlıklı kardeş ise "hep ona odaklanıyorsunuz, bana haksızlık yapılıyor" diliyle konuşur. Bu üç rol, aynı evde yaşasa da aslında üç farklı dünya yaşamaktadır. Bizim tezimiz basitçe "ebeveynler diyabetli çocuğa nasıl davranır" demek yerine, "aynı eylemin bu üç kişi tarafından nasıl bambaşka anlaşıldığını" haritalandırmaktadır. Rakamların bize gösterdiği bu 'uyumsuzluğun', derinlemesine görüşmelerle ruhunu bulduğu yer burasıdır."""
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success!")
    else:
        print("Failed to find:\n" + old[:100] + "...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
