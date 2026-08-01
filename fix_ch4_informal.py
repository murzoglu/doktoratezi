import re

def process_file():
    with open("chapters/04_bulgular.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        'bizim ulaştığımız sonuç': 'mevcut model kestirimi',
        'bizimki': 'mevcut modelin',
        '"Bizim evde her şey aynı, hastalık bir şeyi değiştirmedi" deme refleksi (normalleştirme)': 'Hastalıktan etkilenmeme beyanı (normalleştirme refleksi)',
        'Yukarıdaki tabloya bakıldığında sayısal analizler "durumun boyutunu (ne kadar?)", sözlü analizler ise "duygusal arka planı (neden/nasıl?)" aydınlatmaktadır.': 'Bütünleştirme matrisi incelendiğinde nicel çözümleme etki boyutunu hedeflerken, nitel analiz bağlamsal mekanizmayı aydınlatmaktadır.',
        'anketlerdeki tablo derin duygularla anlam kazanır.': 'öz-bildirim ölçeklerindeki sayısal yapı psikolojik dinamiklerle bağlamsallaşır.',
        'H1\'de çocukların anketlerdeki durumu, mülakatlarda dile getirdikleri şu "normalleştirme/idare etme" psikolojisiyle okunmalıdır': 'H1 bulgusunda çocuk algısındaki farklılaşma, görüşmelerdeki normalleştirme başa çıkma (coping) mekanizması ekseninde değerlendirilmelidir',
        'H3\'te annelerin anketlerde fark göstermemesi, bakımı tamamen kendi doğal ve ahlaki sorumluluğu olarak kabullenmesiyle uyuşur': 'H3 bulgusunda anne öz-bildiriminde fark gözlenmemesi, ağır tıbbi bakımın içselleştirilmiş bir annelik sorumluluğu olarak algılanmasıyla örtüşür',
        'anketlerin yeterince yakalayamadığı detayları sözlü beyanlar gün yüzüne çıkarır; kardeşin ankette fark edilmeyen yalnızlık yükü mülakatta netleşir': 'nicel araçların saptamakta sınırlı kaldığı nüanslar nitel beyanlarla derinleşir; kardeş algısındaki yük mülakatlarda belirginleşir',
        'annenin depresyonu ile ebeveynlik hataları arasındaki istatistiksel bağ, mülakatlarda yaşanan "suçluluk/çaresizlik" hisleriyle eşleşir': 'maternal depresif belirtiler ile olumsuz ebeveynlik örüntüleri arasındaki istatistiksel ilişki, mülakatlardaki suçluluk ve çaresizlik temalarıyla desteklenir',
        'Son olarak "kimin gözünden bakıldığına" dair ayrışmada (H5 ve Meta), çocuğun rutinleştirdiği durumu annenin nasıl bir korkuyla taşıdığı açığa çıkar': 'Son olarak bilgi-verici (informant) ayrışmasında (H5), indeks çocuğun rutin kabul ettiği hastalığın ebeveyn perspektifinde belirgin bir anksiyete kaynağı olarak işlendiği görülür',
        'Bu farklılıklar basit bir "anket hatası" değil, evin içindeki gerçek yaşamın ta kendisidir.': 'Bu bağlamda bilgi-vericiler arası ölçüm uyuşmazlığı (discrepancy) bir yöntem hatasından ziyade, aile-içi çoklu gerçekliğin yapısal bir yansımasıdır.',
        'tezin asıl kararını bozması matematiksel olarak pek olası değildir.': 'çalışmanın nedensel çıkarımını zayıflatması istatistiksel olarak düşük olasılıklıdır.'
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
    
    print(f"Total replaced in ch4: {count}")

process_file()
