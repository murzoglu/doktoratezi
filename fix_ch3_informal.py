import re

def process_file():
    with open("chapters/03_gerec_ve_yontem.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        # Section 3.6
        'Çocuğun "Dışarıda oynamama izin verir mi?" sorusu gibi olumlu yöndeki ifadeler (q25)': 'Çocuk formunda izin verme yönünde ifade edilen tek madde (kanonik kodlamada `q25`)',
        'Annenin "kendini ebeveyn olarak nasıl değerlendirdiğini" ölçen s-EMBU-P formu': 'Annenin kendi ebeveynlik tutumunu öz-bildirimle değerlendiren s-EMBU-P formu',
        '"çocuğun algısı ile annenin kendi bildirimi" (diadik) arasındaki uyuşmazlığın matematiksel olarak (doğrudan) kıyaslanabilmesini sağlamaktadır': 'anne öz-bildirimi ile çocuk algısı arasındaki diadik tutarlılık veya uyuşmazlık düzeyinin doğrudan çözümlenmesine olanak tanımaktadır',
        '"kardeşler ebeveynlerini paylaşırken ne hissediyor" eksenindeki yönlü sorular istatistiksel hesaplamalarda dikkatle işlenmiştir': 'Ebeveyn karşılaştırmasını göreli yönde soran maddeler, puanlamada bu yön dikkate alınarak işlenmiştir',
        'Klinik olarak kimin "hafif", kimin "ağır" depresyonda olduğu şeklinde yapay sınıflandırmalar': 'Ayrık şiddet bantlarına dayalı kategorik sınıflandırmalar',
        '"hangi anne grubunun daha riskli/farklı bir ebeveynliğe sahip olduğunu" anlamak amacıyla, literatürdeki operasyonel sınır (toplam ≥ 17 puan) bir uyarı/ayıraç noktası olarak alınmıştır': 'güncel depresif belirti yükünün görece yüksek olduğu grubu belirlemek amacıyla, literatürdeki operasyonel kesme puanı (toplam ≥ 17) keşifsel bir ayıraç olarak kullanılmıştır',

        # Section 3.7
        '"Herkes 1 mi demiş?" (taban etkisi) veya "Çoğunluk çok mu yüksek puan vermiş?" (tavan etkisi) şeklinde dağılımlar kontrol edilmiştir.': 'madde düzeyinde ortalama, standart sapma, çarpıklık ve basıklık değerleri ile taban ve tavan etkisi oranları incelenmiştir.',
        '"Beklenen modelle elde edilen verinin uyumu ne kadardır?" sorusuna çeşitli indeksler (CFI, TLI, RMSEA, SRMR) kullanılarak yanıt aranmıştır': 'Kurulan faktör yapısının gözlenen veriyle uyumu; CFI, TLI, RMSEA ve SRMR gibi yerleşik uyum indeksleri kullanılarak değerlendirilmiştir',
        '"Diyabet ailesindeki çocuk ile sağlıklı ailedeki çocuk, aynı anket sorusundan aynı anlamı mı çıkarıyor?" sorusu, eşdeğerlik (measurement invariance) analiziyle sınanmıştır': 'Ölçek puanlarının farklı tanı grupları ve bilgi verenler arasında karşılaştırılabilirliği, ölçüm eşdeğerliği (measurement invariance) analizleriyle sınanmıştır',
        '(örneğin depresyon artınca sıcaklık hissinin düşmesi) bakılmıştır': 'sınanmıştır',
        'Annelerin çoğunun "ben asla kötü bir ebeveyn değilim" diyerek olumsuz maddelere doğrudan "1" (en düşük) vermesi (taban yığılması) sonucu oluşabilecek matematiksel çöküntüler, farklı çözümleme senaryolarıyla (kategori daraltma, sorunlu madde çıkarma vb.) paralel olarak yürütülmüş': 'Ebeveyn öz-bildiriminde, özellikle olumsuz muamele maddelerinde gözlenebilecek taban etkisinin (en düşük puanda yığılma) analitik sonuçlar üzerindeki etkisi; kategori daraltma, düşük ayırt edicilikli madde çıkarma ve Bayesçi latent skor gibi farklı stratejilerle paralel olarak modellenmiş',

        # Section 3.8
        '(kazara bir rakamın değişmediğinden emin olmak için), veri setinin parmak izi (SHA-256) doğrulanarak analize başlanmıştır': '(veri setinin izinsiz veya tesadüfi değişime uğramadığından emin olmak için), veri tabanının kriptografik özeti (SHA-256) doğrulanarak analizlere başlanmıştır',
        '(Genişletilmiş analizlerde; çok düzeyli modellemeler için `lavaan`, Bayesçi tahminler için `brms`/`blavaan`, kayıp veri yönetimi için `mice`, eşitleme işlemleri için `WeightIt` gibi alanının önde gelen algoritmaları kullanılmıştır).': 'Çekirdek analizlerde; çok düzeyli modellemeler için `lavaan`, Bayesçi tahminler için `brms`/`blavaan`, eksik veri yönetimi için `mice`, ağırlıklandırma işlemleri için `WeightIt` paketleri kullanılmıştır.',

        # Section 3.9
        'boş bırakan kişilerin verileri doğrudan silinip çöpe atılmamıştır (bu durum büyük bir bilgi kaybına yol açar). Bunun yerine, eksik hücrelerin diğer doldurulmuş yanıtlardan yola çıkılarak yapay zekâ/istatistiksel tahmin algoritmalarıyla "ne olabileceği" hesaplanmış': 'boş bırakan katılımcıların verileri doğrudan analizden çıkarılmamış; bunun yerine eksik hücreler, diğer mevcut yanıtlar üzerinden istatistiksel tahmin algoritmalarıyla atanmış',
        'dış etkenlerin sis perdesini en aza indirerek grup farklarının diyabet bağlamına atfedilme gücünü artırmıştır': 'gözlenen karıştırıcı etkenlerin etkisini azaltarak, grup farklarının diyabet bağlamına atfedilebilme gücünü artırmıştır',
        'Anne "çocuğumu çok seviyorum" derken çocuğun "annem beni anlamıyor" demesi gibi kopukluklar, tezin en önemli katkısıdır. Bu durumu sadece bir hesaplamaya bırakmamak için; aradaki basit puan farkından tutun da puanların arkasındaki gizli duyguların uyuşmazlığına kadar': 'Anne ile çocuk algısı arasındaki tutarlılık veya uyuşmazlık durumu, tezin temel araştırma odaklarındandır. Bu yapıyı tek bir ölçüte bağlamamak amacıyla, mutlak puan farklarından başlayarak latent yapı düzeyindeki uyuşmazlıklara kadar',
        'İstatistikler "ne kadar uyuşmazlık olduğunu" yanıtlarken, bu uyuşmazlığın "nasıl ve neden" kaynaklandığı nitel görüşme analizlerine bırakılmıştır.': 'İstatistiksel stratejiler uyuşmazlığın niceliksel boyutunu değerlendirirken, bu uyuşmazlığın kaynakları ve bağlamı nitel görüşmelerle ele alınmıştır.',
        '"Acaba yaş yerine eğitimi alsaydık ne olurdu?" gibi binlerce olası hesaplama kombinasyonu aynı anda çalıştırılmıştır': 'alt ölçek, kovaryat seti, kestirim yöntemi ve alt örneklem seçimlerinin makul tüm birleşimleri sistematik biçimde kurularak çalıştırılmıştır',
        '"tamamen eşit" olduğunu kanıtlamaz; yalnızca farkın kanıtlanamadığını söyler. Bunu aşmak ve gruplar arasında gerçekten klinik olarak anlamlı bir fark olmadığını pozitif bir şekilde göstermek amacıyla': '"etki yoktur" sonucunu doğrudan ifade edemez; yalnızca farkın istatistiksel olarak gösterilemediğine işaret eder. Bu durumu aşmak ve gruplar arasında klinik olarak anlamlı bir farkın bulunmadığını (pratikte eşdeğerlik) kanıtlayabilmek amacıyla',
        '"fark yoktur" olasılığını ne ölçüde desteklediği Bayes Faktörü (BF) ile kesin olarak raporlanmıştır': '"etki yok" hipotezini ne ölçüde desteklediği Bayes Faktörü (BF) ile raporlanmıştır',
    }

    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            print(f"Replaced: {old[:30]}...")
        else:
            print(f"NOT FOUND: {old[:30]}...")

    with open("chapters/03_gerec_ve_yontem.qmd", "w", encoding="utf-8") as f:
        f.write(content)

process_file()
