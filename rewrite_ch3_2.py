import re

def process_file():
    with open("chapters/03_gerec_ve_yontem.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        # Araştırma Soruları
        """## Araştırma Soruları ve Hipotezler

Araştırmanın temel sorusu, T1DM tanılı çocuğu olan ailelerde ebeveynlik tutumu, anne depresif belirtileri ve kardeş ilişkilerinin sağlıklı kontrol ailelerine göre nasıl örüntülendiği ve bu örüntülerin anne, T1DM tanılı çocuk ve sağlıklı kardeş bakış açıları arasında nasıl ayrıştığıdır. Bu soru doğrultusunda önceden beş doğrulayıcı hipotez belirlenmiştir:

- T1DM tanılı çocuklar ile sağlıklı kardeşlerinin algıladığı ebeveynlik tutumları kontrol grubundan farklılaşmaktadır (H1).
- Kardeş ilişkisi sıcaklık/yakınlık, statü/güç, çatışma ve rekabet boyutlarında gruplar arasında farklılaşmaktadır (H2).
- Annelerin öz-bildirdiği ebeveynlik tutumları gruplar arasında farklılaşmaktadır (H3).
- Anne depresif belirti düzeyi ebeveynlik tutumu boyutlarıyla ilişkilidir (H4).
- Anne öz-bildirimi ile çocuk algısı arasındaki diadik tutarlılık düşük düzeydedir (H5).

Bu hipotezlere ilişkin çözümleme modelleri İstatistiksel Analiz başlığında tanımlanmıştır. Nitel bölüm ise bu örüntüleri anne, T1DM tanılı çocuk ve sağlıklı kardeş deneyimleri üzerinden bağlamsallaştırmayı amaçlamıştır.

## Çalışmanın Yeri ve Tarihi""":
        
        """## Araştırma Soruları ve Hipotezler

Çalışmanın birincil araştırma sorusu; T1DM tanılı çocuğa sahip ailelerdeki ebeveynlik tutumlarının, kardeş ilişkilerinin ve anne depresif belirtilerinin sağlıklı kontrol aileleriyle karşılaştırıldığında nasıl bir değişim gösterdiği ve bu klinik durumun aile içindeki farklı aktörler (anne, indeks çocuk, kardeş) tarafından nasıl farklı algılandığıdır. Bu temel soru bağlamında beş adet doğrulayıcı hipotez formüle edilmiştir:

- **H1:** Tip 1 diyabetli çocukların ve sağlıklı kardeşlerinin algıladıkları ebeveynlik tutumu boyutları, sağlıklı kontrol ailelerinden farklılaşmaktadır.
- **H2:** Kardeşler arası ilişkinin niteliği (sıcaklık/yakınlık, statü/güç, çatışma ve rekabet alt boyutlarında) hastalık durumuna göre anlamlı bir grup farklılığı göstermektedir.
- **H3:** Annelerin öz-bildirimlerine dayanan ebeveynlik tutumları, diyabet ve kontrol grupları arasında farklılaşmaktadır.
- **H4:** Anne depresif belirti düzeyi ile ebeveynlik tutumu alt boyutları (sıcaklık, aşırı koruma, reddetme vb.) arasında doğrudan bir ilişki bulunmaktadır.
- **H5:** Annenin öz-bildirimi ile çocuğun algıladığı ebeveynlik tutumu arasındaki uyum (diadik tutarlılık) hastalık bağlamına göre zayıf ya da kopukluk göstermektedir.

İstatistiksel Analiz başlığında bu beş temel hipoteze yönelik nicel çözümleme modelleri açıklanmış olup; nitel veri seti ise bu istatistiksel sonuçların arkasında yatan aile içi duygusal yaşantıları ve anlamlandırma süreçlerini incelemeye odaklanmıştır.

## Çalışmanın Yeri ve Tarihi"""
    }

    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            print("Successfully replaced section 3.2!")
        else:
            print("Failed to replace section 3.2!")

    with open("chapters/03_gerec_ve_yontem.qmd", "w", encoding="utf-8") as f:
        f.write(content)

process_file()
