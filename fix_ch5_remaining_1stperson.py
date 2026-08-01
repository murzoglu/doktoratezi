import re

def process_file():
    with open("chapters/05_tartisma_ve_sonuc.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        'Tüm diyabetli çocukların ortalamasına baktığımızda "reddedilme" hissi pek dikkat çekici durmuyordu. Ancak gelişmiş istatistiklerle verinin en uç noktalarına (en fazla risk altındaki çocuklara) büyüteç tuttuğumuzda, orada reddedilme hissinin çok daha güçlü (neredeyse iki katı) olduğunu gördük': 
        'Tüm klinik örneğin merkezi eğilimine bakıldığında "reddedilme" algısı görece düşük düzeyde kalmaktadır. Ne var ki zayıf zemin ve zemin etkisine duyarlı istatistiksel modellemelerle (IRT ve latent özellikler) dağılımın uç noktalarına (en yüksek risk altındaki çocuklara) odaklanıldığında, bu alt grupta reddedilme hissinin çok daha şiddetli (neredeyse iki katı) olduğu saptanmıştır',
        
        'Bu nedenle o küçük grup için daha yakın bir klinik inceleme öneriyoruz.':
        'Bu nedenle, söz konusu özgül risk grubu için daha duyarlı bir klinik değerlendirme önerilmektedir.',
        
        'Diyabetli aileler ile sağlıklı ailelerin anket cevaplarını birbirine bağlayan "ağ modellerini" kurduğumuzda, iki ağın şekilsel olarak birbirinden belirgin biçimde ayrışmadığını gördük':
        'Örneklem içi anket yanıtları üzerinden oluşturulan ağ (network) modelleri incelendiğinde, tanı ve kontrol gruplarına ait ağ yapılarının şekilsel olarak birbirinden belirgin biçimde ayrışmadığı görülmüştür',
        
        'Tabii ki bu, arada hiçbir fark olmadığı anlamına gelmez':
        'Kuşkusuz bu durum, gruplar arası yapısal farkların bütünüyle yokluğu şeklinde yorumlanmamalıdır',
        
        'Ayrıca örneklem sayımız sınırlı olduğundan':
        'Ayrıca mevcut örneklem hacmi sınırlı olduğundan',
        
        'Bunun yerine "gizli (latent) yapı" kurduğumuzda, etkinin gerçekte daha güçlü olduğunu gördük':
        'Bunun yerine latent (gizil) yapı modelleri kurulduğunda, gözlenen etkinin daha yüksek olduğu saptanmıştır',
        
        'Ayrıca anne, çocuk ve kardeşin cevaplarını tek bir büyük modelde (trifaktör) birleştirmeyi denesek de':
        'Ayrıca anne, çocuk ve kardeş bildirimleri tek bir kapsamlı modelde (trifaktör) birleştirilmeye çalışılsa da',
        
        'Sonuçlarımız test yöntemine göre değişiyor mu?':
        'Bulgular test yöntemine göre değişiyor mu?',
        
        'Biz de kendi bulgularımızı dört ayrı ve zorlu testten geçirdik':
        'Mevcut analizlerde temel bulgular dört ayrı duyarlılık/robustluk testinden geçirilmiştir',
        
        'bulduğumuz sonucu çökertebilmesi için ne kadar güçlü olması gerektiğini ölçen':
        'gözlenen etkiyi geçersiz kılması için ne kadar güçlü olması gerektiğini hesaplayan',
        
        'kurduğumuz "sahte eşleşme" testleri':
        'kurgulanan "sahte eşleşme" testleri',
        
        'Tip 1 diyabetli çocuğun sağlıklı kardeşiyle olan algı farklarını incelediğimizde (Bulgular, §4.4.6), hastalık bağlamının kardeşler arasındaki algı farkının \'yönünü\' tek başına belirlemediğini gördük.':
        'Tip 1 diyabetli indeks çocuğun sağlıklı kardeşiyle arasındaki algı farkları incelendiğinde (Bulgular, §4.4.6), klinik hastalık bağlamının kardeşler arası algısal uyuşmazlığın yönünü tek başına belirlemediği saptanmıştır.',
        
        'Sağlıklı çocukları tek bir hastaneden, diyabetli çocukları ise daha çok başka bir hastaneden (ve çoğunlukla farklı yıllarda) topladık. İki grubun aynı takvim yılında birleştiği 2023 senesinde farkın azaldığını gördük (bkz. @tbl-yil-grup). Bu durum, bulduğumuz bazı farkların hastalıktan değil':
        'Kontrol grubu tek bir merkezden, tanı grubu ise çoğunlukla farklı bir merkezden ve kısmen farklı yıllarda örneklenmiştir. Grupların aynı takvim yılında örtüştüğü 2023 alt-örnekleminde ana etkinin azaldığı görülmüştür (bkz. @tbl-yil-grup). Bu bulgu, saptanan bazı varyansların doğrudan hastalık bağlamından ziyade'
    }

    count = 0
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            count += 1
            print(f"Replaced: {old[:30]}...")
        else:
            print(f"NOT FOUND: {old[:30]}...")

    with open("chapters/05_tartisma_ve_sonuc.qmd", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Total replaced in ch5: {count}")

process_file()
