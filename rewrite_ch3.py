import re

def process_file():
    with open("chapters/03_gerec_ve_yontem.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        # Araştırma Tasarımı
        """Tip 1 diyabetin aile içindeki etkisi yalnız gruplar arası farklarla değil, aynı ailenin farklı üyelerinin deneyimiyle de görülebileceğinden, araştırma tasarımı hem karşılaştırmalı hem de aile içi bir bakışı birlikte taşır. Bu araştırma, T1DM tanılı çocuğu olan aileleri sağlıklı kontrol aileleriyle ebeveynlik tutumu, anne depresif belirtileri ve kardeş ilişkileri ekseninde karma yöntemle incelemektedir; karşılaştırma hem gruplar arası hem de aile içi deneyim düzeyinde yapılmıştır.

## Araştırma Tasarımı

Araştırma, eşzamanlı karma yöntem (yakınsak; *convergent*) tasarımıyla planlanmıştır [@creswellPlanoClark2018]. Bu tasarımda baskın olan nicel desendir; nitel bileşen bu desenin içine yerleştirilmiştir (*embedded*). Her iki kolun verisi aynı saha döneminde toplanmış, bütünleştirme yorum aşamasında yapılmıştır. Baskın nicel bileşen, aile-kümeli bir olgu–kontrol kesitsel anket çalışmasıdır; her ailede bir indeks çocuk ve bir sağlıklı kardeş yer alır. Kontrol grubu, indeks çocukların yaş ve cinsiyet dağılımı bakımından karşılaştırılabilir ailelerden ardışık örneklemeyle oluşturulmuştur. Birebir eşleştirme algoritması uygulanmamış; gruplar arası denge, çözümleme aşamasında eğilim skoru temelli ağırlıklandırma (bir ailenin ilgili gruba düşme olasılığına göre ağırlık verme) ve kovaryat ayarlamasıyla sağlanmıştır (bkz. §3.9). Nitel bileşen, aynı klinik bağlamdan seçilen bir alt örneklemle yürütülen bireysel yarı yapılandırılmış görüşmelere dayanır. Nicel kolun önceliği, önceden belirlenmiş beş hipotezin sınanmasıdır; nitel kolun işlevi ise bu örüntüleri anne, Tip 1 diyabet (T1DM) tanılı çocuk ve sağlıklı kardeş deneyimleri üzerinden bağlamsallaştırmaktır. Nitel bulgular, nicel sonuçları doğrulayan ikincil kanıt olarak değil; ölçeklerin yakalayamayabileceği role dayalı deneyim katmanlarını açıklayan tamamlayıcı bir kanıt türü olarak konumlandırılmıştır.

Çalışmanın veri yapısı iç içe geçmiş (hiyerarşik) özelliktedir. Her aile bir indeks çocuğu, bir kardeşi ve ortak anne bildirimini içerir. Aynı aileye ait çocuk satırları aile düzeyi değişkenleri paylaştığından, gözlemlerin bağımsızlığı varsayımı karşılanmaz. Bu nedenle çıkarımsal çözümlemeler, aile içi benzerliği (sınıf-içi korelasyon; ICC) hesaba katan çok düzeyli (*multilevel*) modellerle ya da aile bazında kümelenmiş standart hatalarla yürütülmüştür. Aynı ebeveynlik davranışı farklı aile üyelerince farklı konumlardan raporlanabildiğinden, çalışma çoklu bilgi kaynağı (*multi-informant*) yaklaşımını benimsemiştir. Bu yaklaşımda bilgi verenler arasındaki düşük veya orta düzeyde örtüşme, yalnız ölçüm hatası değil; bağlama ve role özgü geçerli bilgi olarak da değerlendirilir [@deLosReyes2015; @ferro2022informantAgreement].""":
        
        """Tip 1 diyabetin psikososyal etkisi yalnız hasta çocuk ile sağlıklı bireyler arasındaki farklarla değil, aile üyelerinin karşılıklı deneyimleriyle de şekillenmektedir. Bu nedenle çalışma tasarımı, hem gruplar arası klinik karşılaştırmayı hem de aile içi çoklu-bakış açısını bütünleştiren bir yapıda kurgulanmıştır. Araştırma, T1DM tanılı çocukların bulunduğu aileleri sağlıklı kontrol aileleriyle ebeveynlik tutumu, anne depresif belirtileri ve kardeş ilişkileri ekseninde karma yöntemle incelemektedir.

## Araştırma Tasarımı

Araştırma, nitel bileşenin nicel desenin içine gömüldüğü eşzamanlı karma yöntem (yakınsak; *convergent*) tasarımıyla yürütülmüştür [@creswellPlanoClark2018]. Baskın nicel kol, aile üyelerinin kümelendiği olgu–kontrol kesitsel bir anket çalışması olarak yapılandırılmış; her aileden bir indeks çocuk, bir sağlıklı kardeş ve anne sürece dâhil edilmiştir. Kontrol grubu, indeks çocukların yaş ve cinsiyet özellikleri bakımından benzer sağlıklı ailelerden ardışık örneklemeyle seçilmiş; temel farklar analiz aşamasında eğilim skoru temelli ağırlıklandırma (IPTW) ve kovaryat ayarlaması ile istatistiksel olarak dengelenmiştir (bkz. §3.9). Nitel bileşen ise nicel çalışma grubundan seçilen bir alt örneklemle, aynı zaman diliminde yürütülen bireysel yarı-yapılandırılmış görüşmelere dayanır. Burada nicel veriler önceden belirlenmiş hipotezlerin sınanması işlevini görürken; nitel bulgular anket verilerini doğrulamak için değil, standart ölçeklerin ölçemediği derinlemesine aile içi dinamikleri ve rol temelli anlamlandırmaları açıklayan tamamlayıcı bir katman olarak konumlandırılmıştır.

Çalışmanın örneklem yapısı iç içe geçmiş (hiyerarşik) özellik taşır. Aynı ailenin üyelerinden toplanan veriler ortak genetik ve sosyoekonomik özellikleri paylaştığı için istatistiksel olarak birbirinden tam bağımsız kabul edilmemiştir. Çıkarımsal analizler, bu yapısal bağımlılığı (sınıf-içi korelasyon) modelleyebilen çok düzeyli (*multilevel*) regresyon teknikleri ve aile-bazlı kümelenmiş standart hatalarla yürütülmüştür. Ayrıca çalışmada anne, indeks çocuk ve sağlıklı kardeşten eş zamanlı veri toplanarak çoklu bilgi kaynağı (*multi-informant*) yaklaşımı izlenmiştir. Aile üyelerinin bildirimleri arasındaki olası uyumsuzluklar salt bir "ölçüm hatası" olarak görülmemiş; aksine, ailenin her bir üyesinin kendi rolünden algıladığı geçerli ve anlamlı deneyim farklılıkları olarak çözümlenmiştir [@deLosReyes2015; @ferro2022informantAgreement]."""
    }

    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            print("Successfully replaced section 3.1!")
        else:
            print("Failed to replace section 3.1!")

    with open("chapters/03_gerec_ve_yontem.qmd", "w", encoding="utf-8") as f:
        f.write(content)

process_file()
