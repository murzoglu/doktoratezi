import re

file_path = "chapters/05_tartisma_ve_sonuc.qmd"

def update_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    replacements = [
        (
            r"Anne depresif belirti yükü ile anne-bildirimli ebeveynlik tutumları arasındaki.*?\nçıkarımı yapılmamıştır\.\n\n",
            """Annenin hissettiği depresyon (ruhsal çöküntü) yükü ile kendi ebeveynlik tutumu arasındaki ilişkiye odaklanan dördüncü ana hipotez (H4) kısmen doğrulanmıştır. Yapılan matematiksel modellemede, annenin depresyonu arttıkça ebeveynlik tarzının dört boyutundan üçünün (sıcaklık, reddetme, karşılaştırma) olumsuz etkilendiği görülmüştür (Bulgular, @tbl-apa-h4-sem). Ancak modelin bütünsel uyum gücü (CFI/TLI vb.) istatistiksel eşiklerin altında kaldığı için, bu sonuçlar "depresyon kesin olarak şu ebeveynliğe yol açar" şeklinde kesin bir neden-sonuç mekanizması olarak değil; sadece "bu iki durum aynı anda kötüleşme eğiliminde" şeklinde okunmalıdır.\n\n"""
        ),
        (
            r"Bu örüntünün yönü ve göreli büyüklük sırası meta-analitik kanıtla uyumludur\..*?\nörtüşmektedir\.\n\n",
            """Bu ilişkinin yönü ve büyüklüğü, dünya çapındaki diğer büyük araştırmalarla tam uyum içindedir. Örneğin Lovejoy ve arkadaşlarının 46 çalışmayı birleştirdiği analizinde; annedeki depresyonun en çok "olumsuz/düşmanca ebeveynlik" ile (r = −0,44) bağlantılı olduğu kanıtlanmıştır. Annenin olumlu davranışları (sıcaklık gibi) ise depresyondan çok daha az etkilenmektedir [@lovejoy2000maternal]. Bu tezde de annenin depresyonu arttığında şefkatin/sıcaklığın azalmasından ziyade, 'reddetme' tutumunun çok daha sert bir şekilde artması, dünyadaki bu eğilimle birebir örtüşmektedir.\n\n"""
        ),
        (
            r"Goodman ve arkadaşlarının 193 çalışma ve 80\.851 anne-çocuk ikilisini kapsayan.*?\nolarak doğrulanmıştır \[@goodman2020parentingMediator\]\.\n\n",
            """Yine Goodman ve ekibinin 80 binden fazla anne-çocuğu incelediği devasa çalışmada, depresyon ile ebeveynlik arasındaki ilişkinin aslında rakamsal olarak küçük (r = 0,23 civarı) olduğu bulunmuştur. İşin ilginç yanı, annelerin anketlerde (kendi beyanlarında) bu etkiyi gereğinden fazla şişirme eğiliminde olmasıdır [@goodman2011maternalMetaanalytic]. Bizim araştırmamızda çıkan sonuçların da tam bu sınırda kalması, annelerin "kendilerine dair anketleri doldururken" (H3) yanıltıcı bir tablo çizebileceği uyarımızı destekler. Depresyonun ebeveynliği etkilediği gerçeği, uzun yıllar süren takiplerle de (r = 0,15) ayrıca kanıtlanmıştır [@goodman2020parentingMediator].\n\n"""
        ),
        (
            r"Bu bağ Tip 1 diyabet bağlamına da taşınmıştır\..*?\naracı değildir \[@jaser2007t1dmMediators\]\.\n\n",
            """Bu durum Tip 1 diyabet dünyası için de geçerlidir. Jaser ve ekibinin 108 diyabetli çocuk ve annesiyle yaptığı araştırmada, annenin depresyonu ile çocuğun depresyonu arasında çok güçlü bir bağ bulunmuştur (r = 0,44). Annenin çocukla kurduğu 'sıcaklık', bu depresyonun çocuğa geçişini engelleyen veya yavaşlatan kısmi bir filtre görevi görmüştür [@jaser2007t1dmMediators].\n\n"""
        ),
        (
            r"Bu yapısal örüntünün bilgi-verici düzlemleri arasında bir köprüsü de vardır\..*?\nhipotez düzeyinde okunmalıdır\.\n\n",
            """Daha da önemlisi, annenin hissettiği depresyon sadece kendi psikolojisinde kalmamakta, çocuğun algısına doğrudan sıçramaktadır. Bu çalışmada (ek analizlerde); depresyon testinden yüksek (Beck ≥ 17) puan alan annelerin çocukları, -hastalıktan veya annenin ilaç kullanıp kullanmamasından bağımsız olarak- kendilerini bariz biçimde daha fazla 'reddedilmiş' (p = 0,004) ve diğer çocuklarla 'kıyaslanmış' (p = 0,003) hissettiklerini beyan etmiştir. Bu bulgu, H4 (annenin depresyonu) ile H1 (çocuğun reddedilme hissi) arasındaki kayıp köprüyü kurar. Annenin ruhsal sıkıntısı anketlerdeki kendi beyanına yansımasa bile, çocuğun omuzlarına 'reddedilmişlik hissi' olarak doğrudan çökmektedir [@goodman1999risk].\n\n"""
        ),
        (
            r"Bu bağın Tip 1 diyabete özgü karşılığı yeni Türk kanıtıyla da desteklenir\..*?\nindirgenemez önemini pekiştirir\.\n\n",
            """Annenin ruh hali ile diyabetli çocuğun durumu arasındaki bu geçişgenlik, yeni Türkiye verileriyle de desteklenmektedir. 129 anne-çocukla yapılan bir araştırmada; annedeki depresyon, kaygı ve bakım yükünün çocuğun duygusal/davranışsal sorunlarıyla doğrudan bağlantılı olduğu kanıtlanmıştır [@akdoganDuken2026caregiver]. Hatta 390 ergen ve anneyi kapsayan başka bir çalışmada, annesi klinik düzeyde depresyonda olan çocukların kan şekeri (HbA1c) kontrollerinin bile diğerlerinden daha kötü (%9,6'ya karşı %8,6) olduğu gösterilmiştir [@abadula2024maternalDepr]. 1219 ailenin beş yıl izlendiği uluslararası bir projede ise annelerin sürekli kendilerini 'ergenlerden daha sıcak ebeveynler' olarak görmesi, çocukların içsel sorunlar yaşamasını engelleyememiştir [@esposito2025discrepancy]. Kısacası, anne 'ben sıcak bir anneyim' dese de önemli olan çocuğun bunu nasıl hissettiğidir.\n\n"""
        ),
        (
            r"Aşırı koruma yolunun anlamsız kalması ise bir çelişki değil, ayırt edici bir\nbulgudur:.*?\[@pinquart2017parentingDimensions\]\. Bu örüntü, mevcut modelde reddetme yolunun\nsıcaklık yolundan daha belirgin çıkmasıyla örtüşmektedir\.\n\n",
            """Modelde 'aşırı koruma' ile depresyon arasında bir bağ bulunamaması ise aslında bir çelişki değil, çok değerli bir ipucudur. Çünkü diyabetli bir ailede aşırı korumacılık, annenin depresyonundan değil doğrudan 'hastalığın kendisinden' kaynaklanmaktadır [@pinquart2013]. Yani anne depresyonda olmasa bile, hastalığın zorunlu kuralları (şeker takibi vb.) anneyi aşırı korumacı yapmaktadır. Öte yandan, 1.435 çalışmayı inceleyen dev meta-analizde gösterildiği gibi, reddetme veya sert kontrol gibi özellikler doğrudan çocuğun psikolojisini bozan dışa vurumlarla (hırçınlık vb.) ilişkilidir [@pinquart2017parentingDimensions].\n\n"""
        ),
        (
            r"Yine de yorum kesitsel tasarımın sınırları içinde kalmalıdır: tek dalgalı kesitsel\nveriden hesaplanan.*?nedensel risk aktarımı yorumu yapılmamıştır\.\n\n",
            """Bütün bu ilişkiler yorumlanırken araştırmanın anlık bir kesit (fotoğraf) olduğu unutulmamalıdır. Tek bir seferde toplanan verilerle "annenin depresyonu çocuğun reddedilme hissini yaratır" diyemeyiz, sadece "bu iki durum aynı anda, el ele kötüleşir" (eş-değişim) diyebiliriz [@maxwellCole2011crossMediation]. Bu sebeple nedensel bir risk aktarımı iddiasında bulunulmamıştır.\n\n"""
        )
    ]

    for pattern, repl in replacements:
        content, count = re.subn(pattern, repl, content, flags=re.DOTALL)
        if count == 0:
            print(f"Warning: Pattern not found:\n{pattern[:50]}...")
        else:
            print(f"Success: Replaced {count} times.")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

update_file(file_path)
print("Third batch done.")
