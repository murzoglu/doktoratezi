import re

def process_file():
    with open("chapters/05_tartisma_ve_sonuc.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        'Bu durumu iki şekilde yorumlayabiliriz.': 'Bu durum iki temel eksende yorumlanabilir.',
        'Birincisi:': 'Birincisi;',
        'İkincisi (ve daha olası olanı):': 'İkincisi ve kavramsal olarak daha muhtemel olanı;',
        'Hastaneden kan şekeri verisine ulaşabildiğimiz çocuk sayısı çok azdı (sadece 39 çocuk) ve bu eksiklik tesadüfi değildi.': 'Metabolik kontrol (HbA1c) verisine erişilebilen alt örneklem hacminin (n=39) kısıtlılığı ve veri kayıp mekanizmasının tesadüfi olmama olasılığıdır.',
        'Bu nedenle "kesinlikle bağ yoktur" demek yerine "elimizdeki veri bunu kanıtlamaya yetmemiştir" demek daha doğru bir yaklaşımdır.': 'Bu nedenle metabolik kontrol ile tutum arasında bir bağın olmadığı kesin bir iddiadan ziyade, verinin istatistiksel güç sınırlarıyla ilişkilendirilmelidir.',
        'Çalışmamız, bulguların güvenilirliğini artıran güçlü istatistiksel araçlarla (karma yöntemler, aileleri bütün olarak ele alan modeller, Bayes istatistiği) donatılmıştır.': 'Araştırma, bulguların güvenilirliğini destekleyen kapsamlı analitik yaklaşımlar (karma yöntemler, aile düzeyinde analizler, Bayesçi çerçeve) içermektedir.',
        'Tüm analiz süreçlerimiz "Açık Bilim" kuralları gereği adım adım şeffaftır.': 'Tüm analitik süreçler Açık Bilim ilkeleri doğrultusunda yapılandırılmıştır.',
        'Çalışmamız olaylara tek bir zaman diliminde (fotoğraf çeker gibi) bakmıştır.': 'Araştırma kesitsel bir desenle yapılandırılmıştır.',
        'Bu yüzden "diyabet olduğu için reddedilme hissi doğdu" gibi kesin bir sebep-sonuç çıkarılamaz.': 'Dolayısıyla kronik hastalık varlığının ebeveynlik tutumundaki değişimlere doğrudan yol açtığı yönünde kesin bir nedensel çıkarım yapılamaz.',
        'çalışmamız; tek ebeveynli, ebeveynini kaybetmiş veya boşanmış ailelerin yaşadığı çok daha ağır zorlukları kapsamamaktadır.': 'araştırma; tek ebeveynli, kayıp yaşamış veya ayrılmış ailelerin deneyimleyebileceği farklı gelişimsel dinamikleri temsil etmemektedir.',
        'Toplama Zamanı ve Hastane Etkisi:': 'Toplama Zamanı ve Kurum Etkisi:',
        'Yani etki, herkes için küçük olsa da, riskli bir çocuk grubunda gayet yakıcı olabilir.': 'Dolayısıyla genel evrendeki düşük etki büyüklüğü, yüksek riskli alt gruptaki klinik şiddeti maskelememelidir.',
        'İki grubun aynı takvim yılında birleştiği 2023 senesinde': 'İki grubun aynı takvim yılında örtüştüğü 2023 senesinde'
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
