import sys

file_path = "chapters/03_gerec_ve_yontem.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    """Tip 1 diyabetin aile içindeki etkisi yalnız gruplar arası farklarla değil, aynı ailenin farklı üyelerinin deneyimiyle de görülebileceğinden, araştırma tasarımı hem karşılaştırmalı hem de aile içi bir bakışı birlikte taşır. Bu araştırma, T1DM tanılı çocuğu olan aileleri sağlıklı kontrol aileleriyle ebeveynlik tutumu, anne depresif belirtileri ve kardeş ilişkileri ekseninde karma yöntemle incelemektedir; karşılaştırma hem gruplar arası hem de aile içi deneyim düzeyinde yapılmıştır.

## Araştırma Tasarımı

Araştırma, eşzamanlı karma yöntem (yakınsak; *convergent*) tasarımıyla planlanmıştır [@creswellPlanoClark2018]. Bu tasarımda baskın olan nicel desendir; nitel bileşen bu desenin içine yerleştirilmiştir (*embedded*). Her iki kolun verisi aynı saha döneminde toplanmış, bütünleştirme yorum aşamasında yapılmıştır. Baskın nicel bileşen, aile-kümeli bir olgu–kontrol kesitsel anket çalışmasıdır; her ailede bir indeks çocuk ve bir sağlıklı kardeş yer alır. Kontrol grubu, indeks çocukların yaş ve cinsiyet dağılımı bakımından karşılaştırılabilir ailelerden ardışık örneklemeyle oluşturulmuştur. Birebir eşleştirme algoritması uygulanmamış; gruplar arası denge, çözümleme aşamasında eğilim skoru temelli ağırlıklandırma (bir ailenin ilgili gruba düşme olasılığına göre ağırlık verme) ve kovaryat ayarlamasıyla sağlanmıştır (bkz. §3.9). Nitel bileşen, aynı klinik bağlamdan seçilen bir alt örneklemle yürütülen bireysel yarı yapılandırılmış görüşmelere dayanır. Nicel kolun önceliği, önceden belirlenmiş beş hipotezin sınanmasıdır; nitel kolun işlevi ise bu örüntüleri anne, Tip 1 diyabet (T1DM) tanılı çocuk ve sağlıklı kardeş deneyimleri üzerinden bağlamsallaştırmaktır. Nitel bulgular, nicel sonuçları doğrulayan ikincil kanıt olarak değil; ölçeklerin yakalayamayabileceği role dayalı deneyim katmanlarını açıklayan tamamlayıcı bir kanıt türü olarak konumlandırılmıştır.

Bu çalışmanın veri seti, doğası gereği iç içe geçmiş (hiyerarşik) bir yapıya sahiptir. Araştırma tasarımı; anne, indeks çocuk (hasta) ve sağlıklı kardeşten elde edilen bildirimlerin tek bir "aile kümesi" altında toplanmasına dayanmaktadır. Aynı aileye mensup bireylerin paylaşılan genetik, çevresel ve sosyoekonomik faktörler nedeniyle benzer yanıtlar verme eğiliminde olması, klasik istatistiksel testlerin temelini oluşturan "gözlemlerin bağımsızlığı" varsayımını ihlal etmektedir.

Bu metodolojik kısıtlılığı aşmak ve istatistiksel hata (tip-1 hata) riskini önlemek amacıyla çıkarımsal analizlerde sıradan testler yerine, aile içi yanıt benzerliğini (sınıf-içi korelasyon; ICC) hesaba katan çok düzeyli modeller (*multilevel modeling*) ve aile bazında kümelenmiş standart hata tahminleri (*cluster-robust standard errors*) kullanılmıştır.

**Çoklu bilgi kaynağı (*multi-informant*) değerlendirmesi.** Çalışmada, aynı aile ikliminin ve ebeveynlik davranışlarının evdeki farklı bireyler tarafından nasıl algılandığını bütüncül olarak görebilmek için çoklu bilgi kaynağı yaklaşımı benimsenmiştir. Güncel alanyazınla uyumlu olarak, katılımcıların (anne, hasta çocuk, kardeş) verdikleri yanıtlar arasındaki düşük veya orta düzeyli uyuşmazlıklar basit bir "ölçüm hatası" olarak ele alınmamıştır. Aksine bu farklılıklar, her bir bireyin aile sistemi içindeki farklı rolünü ve kendi penceresinden algıladığı gerçekliği yansıtan, bağlama özgü geçerli bilgiler olarak kabul edilmiştir [@deLosReyes2015; @ferro2022informantAgreement].

Nicel kolun raporlanmasında olgu–kontrol çalışmaları için STROBE^[STROBE: kohort, olgu–kontrol ve kesitsel araştırma desenleri gibi gözlemsel çalışmaların metodolojik kalitesini ve raporlama şeffaflığını artırmak için oluşturulmuş uluslararası bildirim yönergesidir.] [@vandenbroucke2007strobe], nicel psikolojik araştırma için JARS-Quant^[JARS-Quant: Amerikan Psikoloji Birliği (APA) tarafından, nicel araştırmaların veri, yöntem ve bulgularının şeffaf, eksiksiz ve standart bir biçimde raporlanması amacıyla geliştirilen kılavuzdur.] [@appelbaum2018jarsQuant] ve öngörü/risk modelleri için TRIPOD^[TRIPOD: bir tanının ya da gelecekteki bir sonucun olasılığını birden çok değişkeni birlikte kullanarak kestiren öngörü modellerinin geliştirilmesini, doğrulanmasını ve güncellenmesini şeffaf biçimde raporlamak için oluşturulmuş 22 maddelik uluslararası bildirim yönergesidir. Yönerge; modelin hangi değişkenlerle ve nasıl kurulduğunun, hangi örneklemde sınandığının ve başarımının hem ayırt etme (*discrimination*) hem de kalibrasyon boyutuyla nasıl değerlendirildiğinin açıkça bildirilmesini gerektirir.] [@collins2015tripod] çerçeveleri esas alınmıştır. Nitel kolun raporlanmasında COREQ [@tong2007coreq], SRQR^[SRQR: nitel araştırmaların yöntemsel titizliğini, şeffaflığını ve bulguların inandırıcılığını artırmayı hedefleyen 21 maddelik standart raporlama çerçevesidir.] [@obrien2014srqr] ve JARS-Qual [@levitt2018jarsQual] çerçeveleri kullanılmıştır. Karma bütünleştirmenin raporlanmasında ise GRAMMS^[GRAMMS: karma yöntem (nitel ve nicel bileşenleri birleştiren) araştırmaların bilimsel kalitesini ve metodolojik bütünleşmesini şeffaf biçimde raporlamak için kullanılan iyi uygulama çerçevesidir.] [@ocathain2008gramms] çerçevesi esas alınmıştır.""" :
    """Tip 1 diyabetin bir aileyi nasıl etkilediğini anlamak için sadece hastalarla sağlıklıları karşılaştırmak yetmez; aynı evin içindeki farklı kişilerin (anne, hasta çocuk, sağlıklı kardeş) yaşadıklarını da görmek gerekir. Bu nedenle araştırmamız, hem hastalıklı ile sağlıklı aileleri karşılaştıran hem de aynı evdeki üyelerin hislerini anlamaya çalışan "karma yöntemli" (sayılar + yüz yüze görüşmeler) bir tasarıma sahiptir.

## Araştırma Tasarımı

Bu araştırma, aynı anda yürütülen sayılar (nicel) ve görüşmelerden (nitel) oluşan karma bir tasarımla yapılmıştır [@creswellPlanoClark2018]. Çalışmanın ana omurgasını anketlerle toplanan sayılar oluşturur; derinlemesine görüşmeler ise bu anketlerin ardındaki hikayeyi anlatmak için tasarımın içine yerleştirilmiştir. Araştırmaya katılan her aileden bir çocuk ve onun sağlıklı bir kardeşi ile anneleri sürece dâhil edilmiştir. Hasta çocuklar ile tamamen sağlıklı ailelerin çocukları (kontrol grubu) seçilirken yaş ve cinsiyet gibi konularda birbirlerine benzer olmalarına dikkat edilmiş; aralarındaki ufak tefek farklar ise analiz aşamasında istatistiksel ağırlıklandırma ve ayarlamalarla (bkz. §3.9) eşitlenmiştir.

Araştırmanın istatistik (nicel) kısmı, "Ebeveynlik nasıldır? Depresyon çocukları nasıl etkiler?" gibi baştan belirlediğimiz 5 temel soruyu (hipotezi) test eder. Yüz yüze görüşme (nitel) kısmı ise bu sorulara verilen cevapların "anne, diyabetli çocuk ve sağlıklı kardeşin hayatında gerçekte ne anlama geldiğini" açıklar. Yani nitel bulgularımız, anketleri "kanıtlamak" için değil, anketlerin ölçemediği o derin yaşantıları göstermek içindir.

Ayrıca bu çalışmada elde ettiğimiz veriler "iç içe geçmiş" yapıdadır. Anne, çocuk ve kardeşin cevapları tesadüfi kişilerden gelmemektedir; hepsi aynı evin içinde (aynı genetik, aynı gelir, aynı çevre) aynı "aile sepetindedir". Aynı evdeki kişilerin benzer cevaplar verme ihtimali, sıradan istatistiksel testlerin yanılmasına (hatalı sonuç vermesine) neden olabilir. Biz bu yanılgıyı aşmak için, sıradan testler yerine aynı evin içindeki benzerliği hesaba katan gelişmiş yöntemler (çok düzeyli modeller ve aile kümeli standart hatalar) kullandık.

**Herkesin kendi penceresinden olaylara bakması (Çoklu bilgi kaynağı):** Aynı evdeki ebeveynliği anne, çocuk ve kardeşin farklı algılaması bir "anket veya ölçüm hatası" değil, herkesin olaylara kendi rolü ve kendi penceresinden bakmasının doğal bir sonucudur [@deLosReyes2015; @ferro2022informantAgreement]. Biz de aynı evdeki bu uyuşmazlıkları "hata" olarak değil, farklı gerçeklikler olarak kabul ettik.

Bu araştırma, istatistikler ve anket raporlamaları için tıp dünyasındaki STROBE [@vandenbroucke2007strobe], JARS-Quant [@appelbaum2018jarsQuant] ve öngörü modelleri için TRIPOD [@collins2015tripod] uluslararası kurallarına tam uyumlu olarak yazılmıştır. Görüşme (nitel) kısmı COREQ [@tong2007coreq], SRQR [@obrien2014srqr] ve JARS-Qual [@levitt2018jarsQual] standartlarına; ikisinin harmanlandığı yerler ise GRAMMS [@ocathain2008gramms] kılavuzuna sadık kalarak raporlanmıştır."""
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success!")
    else:
        print("Failed to find:\n" + old[:100] + "...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
