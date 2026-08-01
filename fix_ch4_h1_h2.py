import re

def process_file():
    with open("chapters/04_bulgular.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        'Diyabetli ailelerin çocukları (hem diyabetli çocuğun kendisi hem de sağlıklı kardeşi), annelerinden *reddedildikleri* ve annelerinin *aşırı korumacı* olduğuna dair algılarını, sağlıklı kontrol ailelerinin çocuklarına göre küçük ama belirgin şekilde daha yüksek bildirmiştir.': 'DM grubundaki çocuklar (indeks hasta ve sağlıklı kardeşler), kontrol grubundaki yaşıtlarına göre maternal reddetme ve aşırı koruma algılarını küçük ancak istatistiksel olarak anlamlı düzeyde daha yüksek bildirmiştir.',
        'Anneden algılanan "sıcaklık" boyutu, klasik analizlerde sınırda bir fark göstermiş gibi görünse de daha gelişmiş yöntemlerle (Bayesçi analiz) incelendiğinde bunun gerçek ve sağlam bir fark olmadığı anlaşılmıştır.': 'Anneden algılanan sıcaklık boyutunda frekansçı analizler sınırda bir farka işaret etse de, Bayesçi değerlendirme bu farkın yönünü doğrulamamış (fark-yokluğu lehine kanıt) ve etkinin kırılgan olduğunu göstermiştir.',
        'Ortaya çıkan farklılıkların en belirgini "reddetme", ikincisi ise "aşırı koruma" algısıdır. İlginç olan bulgu şudur: Bu algı farklılığı çocukların bireysel hastalık durumundan çok "ailenin genel havasından" kaynaklanmaktadır. Diyabet tanısının olduğu ailelerdeki her iki çocuk da (hem diyabetli olan hem de sağlıklı olan) bu algıları benzer seviyede yüksek hissetmektedir. Kısacası, diyabetli ailenin kendi içinde diyabetli çocuk ile sağlıklı kardeşi arasında annenin ebeveynlik tutumu (EMBU-C) açısından hiçbir fark bulunamamıştır.': 'Algısal ayrışma en belirgin olarak reddetme, ardından aşırı koruma boyutlarında izlenmiştir. Bu ayrışma çocuk düzeyindeki tanı durumundan (hastalık) ziyade, aile düzeyindeki kümelenmeden kaynaklanmaktadır; diyabet hanesindeki her iki çocuk da (hasta ve sağlıklı kardeş) söz konusu ebeveyn tutumlarını benzer seviyede yüksek algılamaktadır. Aile içi analizlerde, indeks çocuk ile sağlıklı kardeş arasında ebeveynlik algısı açısından hiçbir fark saptanmamıştır.',
        '"Reddetme" boyutunda ulaşılan bu sonuç, çocukların yaşından veya cinsiyetinden de etkilenmemiştir.': 'Saptanan grup ana etkisi, modelde yaş ve cinsiyetin kontrol edilmesinden bağımsız olarak sürmüştür.',
        'Anneden algılanan dört farklı ebeveynlik tutumu (sıcaklık, aşırı koruma, reddetme, karşılaştırma) incelenirken, aynı evde yaşayan iki kardeşin birbirine benzer cevaplar verebileceği dikkate alınmış ve 482 çocuğun verisi buna uygun özel bir analiz modeliyle hesaplanmıştır.': 'Dört EMBU-C alt ölçeğine yönelik değerlendirmelerde veri setindeki diadik bağımlılık (aile içi kümelenme) dikkate alınarak, 482 çocuğun algısı aile düzeyinde rastgele kesişimli (random intercept) çok düzeyli bir modelle çözümlenmiştir.',
        'Önceden planlandığı üzere temel değerlendirme ölçütü, diyabetli aileler ile sağlıklı kontrol aileleri arasındaki genel grup farkıdır. Bu fark hesaplanırken, diyabetli çocuk ve sağlıklı kardeş rolleri eşit derecede hesaba katılmış ve çok sayıda karşılaştırma yapıldığı için hata payını düşüren istatistiksel bir düzeltme (BH-FDR) uygulanmıştır': 'Ön-kayıtlı birincil estimand, diyabet ve kontrol aileleri arasındaki grup ana etkisidir; bu etki indeks çocuk ve kardeş rolleri eşit ağırlıkla dengelenerek ve çoklu karşılaştırmalar için BH-FDR düzeltmesi uygulanarak kestirilmiştir',
        'Sonuçların sağlamlığını teyit etmek için kullanılan ikinci ve bağımsız bir yaklaşım (Bayesçi analiz); reddetme boyutundaki farkın "güçlü", aşırı koruma boyutundaki farkın ise "orta düzeyde" kanıta sahip olduğunu doğrulamıştır': 'Bulguları çapraz doğrulamak üzere yürütülen Bayesçi hat; reddetme ana etkisinde "güçlü", aşırı korumada ise "orta düzeyde" kanıt sunmuştur',
        'Sıcaklık boyutunda ise ilk klasik analizin aksine gruplar arasında bir "farkın olmadığı" (BF₁₀ = 0,29) yönünde kanıt sunulmuştur.': 'Sıcaklık boyutunda klasik analizin aksine fark-yokluğu yönünde kanıt (BF₁₀ = 0,29) bulunmuştur.',
        'Karşılaştırma boyutu da yine "fark yokluğu" yönündedir (BF₁₀ = 0,53).': 'Karşılaştırma boyutu için de fark-yokluğu yönünde bulgu elde edilmiştir (BF₁₀ = 0,53).',
        'Ulaşılan en güçlü farklılık "reddetme" boyutundadır': 'En güçlü analitik sinyal reddetme alt ölçeğinde alınmıştır',
        'Ayrıca reddetme farkı, anketlerde puanların bazen en düşük ya da en yüksek seçenekte birikmesi (yığılma) sorununa daha dirençli olan çok daha gelişmiş bir istatistiksel modelle de ayrıca kanıtlanmıştır:': 'Bu bulgu, potansiyel tavan/taban etkilerine karşı dirençli olan sıralı Madde Yanıt Kuramı (IRT) temelli bir paralel analizle de doğrulanmıştır:',
        'Aynı aileden gelen kardeşlerin verdikleri cevaplar arasındaki benzerlik oranı yaklaşık %14\'tür (0,14) ve ortaya çıkan durum çocuğun rolüne, yaşına veya cinsiyetine göre bir değişim göstermemiştir.': 'Aile içi kümelenmeyi yansıtan sınıf-içi korelasyon katsayısı (ICC) 0,14 olarak hesaplanmış olup, ana etkiler rol, yaş veya cinsiyete göre etkileşim göstermemiştir.',
        'Hangi sonuçların sağlıklı çocuktan, hangilerinin diyabetli çocuktan geldiğine dair kırılımlar, doğrulayıcı analizlerin detayları ve ailenin kendi içinde yapılan kardeş kıyaslamaları şu tablolarda detaylıca sunulmuştur:': 'Rol bazlı hücresel ayrıştırmalar, Bayesçi çıktı detayları ve aile-içi keşifsel kontrastlar sırasıyla şu tablolarda sunulmuştur:',
        'H1 ebeveynlik algısı genel fark grafiği (Orman grafiği): Çocukların annelerinden algıladıkları tutumlarda diyabet ve kontrol aileleri arasındaki genel farkı gösterir. Noktalar hesaplanan farkı, yatay çizgiler ise güven aralığını temsil eder. Okuma anahtarı: Kesikli dikey çizgi \'hiç fark olmadığını\' (sıfırı) gösterir. Yatay çizgiler bu kesikli dikey çizgiye dokunmuyor veya onu kesmiyorsa, iki grup arasındaki fark kesindir.': 'H1 çok düzeyli orman grafiği: Dört EMBU-C alt ölçeğinde diyabet ve kontrol grupları arasındaki tahmini ortalama fark (grup ana etkisi) ve %95 güven aralıkları (GA). Sıfır çizgisini kesmeyen aralıklar, çoklu karşılaştırma (BH-FDR) düzeltmesi sonrası istatistiksel olarak anlamlı farklılıklara (q < 0,05) karşılık gelir.',
        
        # H2
        'Kardeşler arasındaki ilişkinin dört temel alanında — yakınlık, güç/baskınlık, çatışma ve rekabet — diyabetli aileler ile sağlıklı kontrol aileleri arasında anlamlı bir fark bulunamamıştır.': 'Kardeş ilişki kalitesinin (KİA) dört alt boyutunda — yakınlık, güç/baskınlık, çatışma ve rekabet — diyabetli ve kontrol aileleri arasında istatistiksel olarak anlamlı bir farklılık saptanmamıştır.',
        'İstatistiksel olarak bu durum, grupların birbirinin "tıpatıp aynısı" olduğu (farkın sıfır olduğu) anlamına gelmese de, elimizdeki verilerle gruplar arasında bir fark tespit edilememiştir. Klinik açıdan yorumlandığında, diyabet tanısının evdeki kardeşler arasındaki ilişki dinamiğini belirgin şekilde değiştirmediği görülmektedir.': 'Frekansçı testlerin yapısı gereği bu bulgu sıfır-farkın kesin kanıtı olmamakla birlikte, mevcut veriler ışığında diyabet tanısının aile içi kardeşlik dinamikleri üzerinde bağımsız ve güçlü bir etki yaratmadığı gözlenmektedir.',
    }

    count = 0
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            count += 1
            print(f"Replaced: {old[:30]}...")
        else:
            print(f"NOT FOUND: {old[:30]}...")

    with open("chapters/04_bulgular.qmd", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Total replaced in part 2: {count}")

process_file()
