import re

def process_file():
    with open("chapters/03_gerec_ve_yontem.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        'Araştırma, nitel bileşenin nicel desenin içine gömüldüğü eşzamanlı karma yöntem (yakınsak; *convergent*) tasarımıyla yürütülmüştür': 'Araştırma, eşzamanlı karma yöntem tasarımıyla yürütülmüştür',
        'Baskın nicel kol, aile üyelerinin kümelendiği olgu–kontrol kesitsel bir anket çalışması olarak yapılandırılmış;': 'Nicel araştırma kolu, olgu-kontrol kesitsel anket çalışması olarak yapılandırılmış;',
        'Çıkarımsal analizler, bu yapısal bağımlılığı (sınıf-içi korelasyon) modelleyebilen çok düzeyli (*multilevel*) regresyon teknikleri ve aile-bazlı kümelenmiş standart hatalarla yürütülmüştür.': 'Aynı haneden toplanan verilerin bağımlı doğası gereği, grup analizlerinde aile içi benzerliği hesaba katan çok düzeyli modeller kullanılmıştır.',
        'Çok düzeyli (multilevel) ve yapısal eşitlik (SEM) gibi daha karmaşık veri modellemeleri, toplam katılımcı sayısından ziyade küme (aile) sayısına duyarlıdır. Ulaşılan ~240 ailelik havuz, bu tür karmaşık modellerin çalıştırılabilmesi için önerilen kaba alt sınırların güvenle üzerindedir': 'Aile içi değerlendirmeler ve yapısal modellemeler, birey sayısından ziyade ailenin bir küme olarak ele alınmasına (küme sayısına) duyarlıdır. Ulaşılan ~240 ailelik havuz, bu tür istatistiksel modellerin gerektirdiği alt sınırları güvenle karşılamaktadır',
        'Bu modellerin duyarlılığı ayrıca simülasyon (Monte Carlo) temelli bir hassasiyet çözümlemesiyle tamamlanmıştır; `simr` ve `pwr` paketleriyle yürütülen bu çözümleme, belirli bir aile sayısında hangi büyüklükteki etkilerin yakalanabileceğini kestirmeye yarar': 'Bu kapasite, verinin bilgisayar ortamında simüle edilerek test edildiği güç analizleriyle de doğrulanmıştır',
        'Geriye dönük p-değeri bazlı güç hesapları genellikle yanıltıcı olduğundan [@hoenigHeisey2001abusePower], bu çalışmada istatistiksel sonuçların belirsizlik payları güven aralıkları (GA), Bayesçi aralıklar ve pratikte eşdeğerlik (TOST) sınırlarıyla daha dürüst bir yaklaşımla raporlanmıştır.': 'Klinik çalışmaların raporlama standartlarına uygun olarak, bulguların kesinliği yalnız p-değeriyle değil, farklı istatistiksel güven aralıklarıyla (GA ve Bayesçi aralıklar) sunulmuştur.',
        'Temel modellerde bu değişken, doğrulayıcı faktör analizine dayalı bir gizil (latent) skor olarak kullanılmış; duyarlılık kontrollerinde ise literatürde bilinen eş-ağırlıklı diğer indeks formülleriyle de sağlaması yapılmıştır': 'Temel modellerde bu bileşenler tek bir "sosyoekonomik düzey" (SES) skorunda birleştirilmiş; ikincil çözümlemelerde ise alternatif formüllerle sonuçların sağlaması yapılmıştır',
        'Verilerdeki açık uçlu kişisel bilgilerin nasıl anonimleştirildiği Etik Hususlar bölümünde detaylandırılmıştır.': 'Verilerin anonimleştirilmesi Etik Hususlar bölümünde detaylandırılmıştır.',
        'Nicel kolun raporlanmasında olgu–kontrol çalışmaları için STROBE [@vandenbroucke2007strobe], nicel psikolojik araştırma için JARS-Quant [@appelbaum2018jarsQuant] ve öngörü/risk modelleri için TRIPOD [@collins2015tripod] çerçeveleri esas alınmıştır. Nitel kolun raporlanmasında COREQ [@tong2007coreq], SRQR [@obrien2014srqr] ve JARS-Qual [@levitt2018jarsQual] çerçeveleri kullanılmıştır. Karma bütünleştirmenin raporlanmasında ise GRAMMS [@ocathain2008gramms] çerçevesi esas alınmıştır.': 'Raporlamada olgu-kontrol tasarımları için STROBE [@vandenbroucke2007strobe], nicel veriler için JARS-Quant [@appelbaum2018jarsQuant] ve nitel veriler için COREQ [@tong2007coreq] standartları kılavuz alınmıştır.'
    }

    count = 0
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            count += 1
            print(f"Replaced: {old[:30]}...")
        else:
            print(f"NOT FOUND: {old[:30]}...")

    with open("chapters/03_gerec_ve_yontem.qmd", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Total replaced in ch3 early sections: {count}")

process_file()
