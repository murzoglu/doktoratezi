import sys

file_path = "chapters/03_gerec_ve_yontem.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    """## Araştırma Soruları ve Hipotezler

Araştırmanın temel sorusu, T1DM tanılı çocuğu olan ailelerde ebeveynlik tutumu, anne depresif belirtileri ve kardeş ilişkilerinin sağlıklı kontrol ailelerine göre nasıl örüntülendiği ve bu örüntülerin anne, T1DM tanılı çocuk ve sağlıklı kardeş bakış açıları arasında nasıl ayrıştığıdır. Bu soru doğrultusunda önceden beş doğrulayıcı hipotez belirlenmiştir:

- T1DM tanılı çocuklar ile sağlıklı kardeşlerinin algıladığı ebeveynlik tutumları kontrol grubundan farklılaşmaktadır (H1).
- Kardeş ilişkisi sıcaklık/yakınlık, statü/güç, çatışma ve rekabet boyutlarında gruplar arasında farklılaşmaktadır (H2).
- Annelerin öz-bildirdiği ebeveynlik tutumları gruplar arasında farklılaşmaktadır (H3).
- Anne depresif belirti düzeyi ebeveynlik tutumu boyutlarıyla ilişkilidir (H4).
- Anne öz-bildirimi ile çocuk algısı arasındaki diadik tutarlılık düşük düzeydedir (H5).

Bu hipotezlere ilişkin çözümleme modelleri İstatistiksel Analiz başlığında tanımlanmıştır. Nitel bölüm ise bu örüntüleri anne, T1DM tanılı çocuk ve sağlıklı kardeş deneyimleri üzerinden bağlamsallaştırmayı amaçlamıştır.

## Çalışmanın Yeri ve Tarihi

Çalışma çok merkezli olarak iki kurumda yürütülmüştür. Birincil koordinasyon merkezi T.C. Sağlık Bakanlığı Marmara Üniversitesi Eğitim ve Araştırma Hastanesi'dir. Hasta grubu bu kurumun Çocuk Endokrinoloji ve Diyabet Bilim Dalı'ndan, sağlıklı kontrol grubu ise aynı kurumun Hasta Çocuk Kliniği–Genel Pediatri polikliniğinden alınmıştır. İkinci merkez İstanbul Medeniyet Üniversitesi Göztepe Süleyman Yalçın Şehir Hastanesi Çocuk Endokrinoloji Polikliniği'dir; bu merkez yalnız hasta grubu alımına katkı vermiştir. Saha süreci Şubat 2023'te hasta alımıyla başlamış, Aralık 2025'te tamamlanmıştır; verilerin çözümlenmesi bunu izleyen dönemde yürütülmüştür. Anket uygulamaları ve nitel görüşmeler, katılımcıların birbirlerinden ayrı odalarda ölçekleri yanıtlayabilecekleri mahremiyet sağlanarak poliklinik ortamında gerçekleştirilmiştir.""" :
    """## Araştırma Soruları ve Hipotezler

Çalışmamızın ana sorusu şudur: Tip 1 diyabetli ailelerdeki "ebeveynlik algısı", "anne depresyonu" ve "kardeş ilişkileri", sağlıklı ailelere kıyasla nasıl değişmektedir? Ayrıca bu değişim evdeki anne, hasta çocuk ve kardeş arasında nasıl farklı algılanmaktadır? Bu soruyu cevaplamak için en baştan beş temel hipotez belirledik:

- **H1:** Tip 1 diyabetli çocukların (ve sağlıklı kardeşlerinin) ebeveynlik hissi, sağlıklı ailelerin çocuklarından farklıdır.
- **H2:** İki kardeşin birbiriyle ilişkisi (yakınlık, kavga, rekabet veya kimin daha üstün olduğu), hastalık durumuna göre farklılık gösterir.
- **H3:** Annelerin kendileri hakkında anketlere verdikleri "ben şöyle bir anneyim" yanıtları hastalık durumuna göre değişir.
- **H4:** Annenin depresyonda olma ihtimali, ebeveynlik tarzını (sıcaklık, korumacı olma, reddetme gibi) doğrudan etkiler.
- **H5:** Annenin kendi ebeveynliği hakkında düşündükleri ile çocuğun o ebeveynliği hissetme biçimi arasında uyumsuzluk vardır (diadik tutarsızlık).

İstatistik kısmında (bkz. İstatistiksel Analiz) bu 5 ihtimali sayılarla test ettik, ardından yüz yüze görüşmelerle (nitel bölümde) rakamların arkasında yatan aile içi duygusal deneyimleri anlamlandırmaya çalıştık.

## Çalışmanın Yeri ve Tarihi

Bu araştırma İstanbul'da iki büyük devlet hastanesinde yürütülmüştür. Ana merkezimiz Marmara Üniversitesi Eğitim ve Araştırma Hastanesi'dir; burada hem diyabetli hastaları (Çocuk Endokrinoloji) hem de hiçbir hastalığı olmayan kontrol grubu çocukları (Genel Pediatri) araştırmamıza dâhil ettik. İkinci merkezimiz ise Göztepe Süleyman Yalçın Şehir Hastanesi'dir ve buradan sadece diyabetli çocuklar araştırmaya katılmıştır. Ailelerle görüşmeler ve anket doldurma işlemleri Şubat 2023 ile Aralık 2025 arasında yapılmış, tüm bu süreç aile bireylerinin birbirinden etkilenmeden, rahatça kendi başlarına cevap verebilecekleri kapalı poliklinik odalarında gerçekleştirilmiştir."""
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success!")
    else:
        print("Failed to find:\n" + old[:100] + "...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
