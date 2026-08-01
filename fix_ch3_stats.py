import re

def process_file():
    with open("chapters/03_gerec_ve_yontem.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        'ne kadar "denk" olduğu sadece geleneksel p-değeriyle değil, gruplar arasındaki mesafeyi katılımcı sayısından bağımsız, mutlak bir büyüklük olarak gösteren standardize ortalama fark (SMD) değeriyle kanıtlanmıştır': 'başlangıçtaki dağılım dengesi, örneklem büyüklüğüne duyarlı olan geleneksel p-değerine ek olarak, gruplar arası farkın mutlak büyüklüğünü gösteren standardize ortalama fark (SMD) ile değerlendirilmiştir',
        
        'sonucu yanıltabilecek (karıştırıcı) etkenleri temizlemek amacıyla, istatistiksel modeller kurulmadan önce değişkenler arasındaki ilişkileri gösteren bir Nedensel Diyagram (DAG) oluşturulmuştur': 'karıştırıcı (confounding) etkenlerin etkisini kontrol altına almak amacıyla, modelleme öncesinde değişkenler arası ilişkileri tanımlayan bir Nedensel Diyagram (DAG) oluşturulmuştur',
        
        'Hastalık ile sonuç arasındaki sahte bağları koparmak için ailenin gelir düzeyi, kardeş yaş farkı ve evdeki toplam çocuk sayısı istatistiksel "kovaryat" olarak hesaptan düşülmüştür.': 'Maruziyet ile sonuç arasındaki nedensel olmayan yolları kapatmak üzere; ailenin gelir düzeyi, kardeş yaş farkı ve evdeki toplam çocuk sayısı modellere kovaryat olarak eklenmiştir.',
        
        'hangi ailenin diyabet grubuna dâhil olmaya demografik olarak daha eğilimli olduğunu hesaplayan "eğilim skoru ağırlıklandırması" (IPTW) da kullanılmıştır': 'tanı grubuna atanma olasılığını dengelemeyi amaçlayan eğilim skoru ağırlıklandırması (IPTW) kullanılmıştır',
        
        'Bu "çift korumalı" (doubly robust) yaklaşım, çalışmayı tam bir deneysel (randomize) yapıya çevirmese de': 'Çift korumalı (doubly robust) bu yaklaşım, gözlemsel tasarım sınırları içinde',
        
        'verilerin "aynı aile içinden toplanmış olması" hiyerarşisine uygun yöntemlerle sınanmıştır': 'verilerin aile içi kümelenme gösteren hiyerarşik yapısına uygun yöntemlerle sınanmıştır',
        
        'sadece anneyi ilgilendiren sonuçlarda düz aile analizleri; kardeşler arasındaki ilişkilerde ise karşılıklı bağımlılığı ölçen aktör-partner modelleri (APIM) kullanılmıştır.': 'yalnızca anneyi ilgilendiren sonuçlarda tek düzeyli analizler; kardeşler arası ilişkilerde ise diadik bağımlılığı modelleyen aktör-partner bağımlılık modelleri (APIM) kullanılmıştır.',
        
        'Aynı evdeki iki çocuğun (indeks ve kardeş) ebeveynlik algısı birbirinden tam bağımsız olmadığı için klasik testler yanıltıcıdır (p-değerini yapay olarak düşürür). Bu nedenle gruplar, "aile numarasını" hesaplamanın içine alan rastgele etkili çok düzeyli bir model üzerinden kıyaslanmıştır': 'Aynı hanedeki çocukların (indeks ve kardeş) bildirimleri bağımsızlık varsayımını ihlal ettiğinden, tip-1 hata artışını önlemek amacıyla grup karşılaştırmaları aile düzeyinde rastgele kesişim (random intercept) içeren çok düzeyli modellerle yürütülmüştür',
        
        'taban etkisinden kurtulmak için algı puanları doğrudan değil Madde Tepki Kuramı (IRT) ile "gizil yetenek" (θ) skorlarına dönüştürülmüş': 'madde düzeyindeki olası taban etkisini denetlemek amacıyla, algı puanları Madde Yanıt Kuramı (IRT) temelli gizil özellik (θ) skorlarıyla yeniden tahmin edilmiş',
        
        'doğrudan "aynı evdeki diyabetli çocuk ile kardeşi arasındaki" rol farklılıkları da keşifsel olarak sorgulanmıştır.': 'aynı hanedeki indeks çocuk ile kardeş arasındaki rol odaklı farklılıklar dış kontrol grubu olmaksızın keşifsel olarak incelenmiştir.',
        
        'sadece düz ortalamalara (Welch t-testi) bağlanmamış; her çocuğun kendi yapısından gelen ("aktör") ve kardeşinden kaynaklanan ("partner") etkiyi matematiksel olarak ayıran APIM karma modelleri ve diadik faktör analizi gibi üç ayrı istatistiksel yolla güvence altına alınmıştır': 'yalnızca Welch t-testi ile sınırlı kalmamış; aktör ve partner etkilerini ayrıştıran APIM karma modelleri ve diadik yapısal eşitlik modellemesi kullanılarak üç koldan analiz edilmiştir',
        
        'Annelerin kendi beyanları tek bir aile satırında toplandığı için, sonuçlar doğrudan kovaryans analizi (ANCOVA) ve ağırlıklandırma yardımıyla sınanmıştır.': 'Annelerin öz-bildirimleri aile düzeyinde bağımsız veri noktaları oluşturduğundan, temel analiz kovaryans analizi (ANCOVA) ve ağırlıklandırma üzerinden yürütülmüştür.',
        
        'Annedeki antidepresan kullanımının sonucu doğrudan değiştirebileceği bilindiğinden, bu etken modele sabit bir değişken olarak konmak yerine ayrı bir duyarlılık alt analizinde test edilmiştir.': 'Antidepresan kullanımının olası etkisi, temel modele eklenmek yerine yapısal bir duyarlılık analizinde ayrıca sınanmıştır.',
        
        'doğrudan toplanan puanlardan ziyade, bu anket maddelerinin arka planda işaret ettiği "depresyon" ve "reddetme" gibi gizli (latent) yapıları hesaplayan Yapısal Eşitlik Modeli (SEM) ile sınanmıştır.': 'toplam puanlar yerine, ilgili anket maddelerinin yüklediği gizil (latent) faktörleri eşzamanlı kestiren Yapısal Eşitlik Modellemesi (SEM) kullanılarak sınanmıştır.',
        
        'Aynı evin içindeki annenin kendini görüş biçimiyle, çocuğun onu görüş biçimi arasındaki "uyumsuzluk", araştırmanın en kritik metodolojik parçasıdır.': 'Anne öz-bildirimi ile çocuk algısı arasındaki diadik uyuşmazlık düzeyi, araştırmanın temel araştırma odaklarındandır.',
        
        'Uyumsuzluğu kanıtlamak için basit puan farklarından öte beş ayrı matematiksel strateji (sınıf-içi korelasyon, uyum yüzeyi modeli, ortak yazgı denklemleri, diadik CFA ve Kenny oranı) uygulanmıştır': 'Bu yapıyı tek bir ölçüte bağlamamak amacıyla sınıf-içi korelasyon, uyum yüzeyi modeli, ortak yazgı denklemleri, diadik CFA ve Kenny k oranı olmak üzere beş ayrı strateji uygulanmıştır',
        
        'binlerce olası kombinasyon sistematik olarak aynı anda test edilmiştir.': 'kombinasyonlar eşzamanlı olarak değerlendirilmiştir.',
        
        'Klasik (frekansçı) istatistik, "gruplar arasında fark yoktur" sonucunu doğrudan ifade edemediği için, bu boşluğu kapatmak adına': 'Frekansçı yaklaşımın "etki yokluğu" yönünde doğrudan kanıt sunamaması kısıtlılığını aşmak amacıyla',
        
        'Bayesçi yöntem, T1DM ve ebeveynlik konusundaki güncel dünya literatürünü modele bir "ön bilgi" (zayıf bilgi verici önsel) olarak dâhil eder': 'Bayesçi modellemede, ilgili literatür önsel bilgi (weakly informative prior) olarak sürece dâhil edilmiştir',
        
        'Modeller (Stan arka ucu kullanılarak) binlerce kez simüle edildikten sonra; farkların "güvenilir bir aralıkta" kalıp kalmadığı, etki olmamasının "pratikte eşitlik" (ROPE) bölgesine ne kadar düştüğü': 'Kestirimler Markov Zinciri Monte Carlo (MCMC) simülasyonlarıyla elde edilmiş; etkilerin pratik eşdeğerlik bölgesine (ROPE) ne ölçüde düştüğü',
        
        'Aşağıda belirtilen analiz katmanları temel soruları doğrulamak için değil, örüntülerin daha derinine inerek yeni klinik ipuçları aramak (keşifsel/post-hoc) amacıyla tasarlanmıştır.': 'Aşağıdaki analiz katmanları, birincil hipotezlerin ötesinde, veri setindeki ilişkisel örüntüleri derinleştirmek ve keşifsel bulgular sunmak (post-hoc) amacıyla tasarlanmıştır.',
        
        'Çıkan sonuçlar doğrudan nedensellik kurmaz, korelasyon düzeyi öneriler sunar:': 'Bu bulgular nedensel sonuçlardan ziyade ilişkisel yönelimlere işaret eder:',
        
        'Annenin diyabet tanısı nedeniyle yaşadığı depresyonun, doğrudan mı yoksa annenin reddedici tutumlarını artırarak mı çocuğu etkilediğini test eden "köprü/aktarım" yolları incelenmiştir': 'Anne depresyonu ile çocuk algısı arasındaki ilişkide annenin reddedici tutumlarının olası aracı (mediator) rolü incelenmiştir',
        
        'Annelerin anketlere verdikleri yanıtlardan yola çıkarak, anneleri benzer tutum profillerine göre gruplara ayıran sınıflandırma modelleri kurulmuştur.': 'Annelerin madde düzeyindeki yanıt örüntüleri temel alınarak, ebeveynlik tutumlarına göre gizil alt grupları belirleyen yapısal modeller (LCA/LPA) kurulmuştur.',
        
        'Farklı duyguların (örneğin depresyon, sıcaklık, rekabet) diğer tüm dış etkenler sabitlendiğinde dahi birbirini nasıl etkilediğini gösteren çoklu bağ haritaları oluşturulmuştur.': 'Değişkenler arası çoklu koşullu bağımlılıkları, diğer tüm düğümler (nodes) kontrol edildikten sonra inceleyen istatistiksel ağ modelleri oluşturulmuştur.',
        
        'Poliklinikte sadece ebeveynlik tutumlarına bakarak annenin belirgin bir depresif risk taşıyıp taşımadığını tahmin eden sınıflandırma (ROC ve Karar Eğrisi) algoritmaları geliştirilmiştir': 'Ebeveynlik tutumu puanlarının annedeki olası depresif riski saptamadaki klinik geçerliliği ROC analizi ve karar eğrisi (DCA) ile değerlendirilmiştir',
        
        'sadece kan şekeri verisi bulunan 39 ailelik dar grupta keşifsel olarak değerlendirilmiştir.': 'HbA1c verisi mevcut olan dar bir alt örneklemde (n = 39) betimsel olarak incelenmiştir.'
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
