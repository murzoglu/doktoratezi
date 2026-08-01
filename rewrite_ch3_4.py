import re

def process_file():
    with open("chapters/03_gerec_ve_yontem.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        # Değişkenler ve Tanımları
        """## Değişkenler ve Tanımları

Çalışmanın değişkenleri, işlevlerine göre grup, sonuç ve eş değişkenler olarak yapılandırılmıştır. Birincil grup değişkeni, indeks ve kardeş çocukları birlikte temsil eden dört düzeyli rol faktörüdür; ikili karşılaştırmalarda tanı grubu (T1DM/kontrol) değişkeni kullanılmıştır. Sonuç değişkenleri; çocuğun algıladığı ebeveynlik tutumu alt ölçekleri, annenin öz-bildirdiği ebeveynlik tutumu alt ölçekleri, kardeş ilişkisi boyutları ve anne depresif belirti düzeyidir. Eş değişkenler (kovaryatlar) çocuk yaşı, çocuk cinsiyeti, anne yaşı, kardeşler arası yaş farkı, ailedeki çocuk sayısı ve sosyoekonomik durumdur. Tüm yaş ve süre alanları, ilgili anket tarihi ile doğum ya da tanı tarihi farkının 365,25'e bölünmesiyle yıl cinsinden türetilmiştir.

Sosyoekonomik durum; eğitim ve mesleğe dayalı uluslararası sosyoekonomik indeks (*International Socio-Economic Index*, ISEI) [@ganzeboomTreiman1996isei] ile maddi varlık göstergelerini birlikte kullanan üç katmanlı bir kompozit hattıyla üretilmiştir. Maddi varlık indeksi, sıralı değişkenlere uygun bir temel bileşen analiziyle (polikorik) hesaplanmıştır. Şeffaflık amaçlı duyarlılık değişkenleri eş-ağırlıklı ve Hollingshead tipi kompozitlerle üretilmiş [@hollingshead1975]; birincil sosyoekonomik kovaryat ise doğrulayıcı faktör analizine dayalı bir latent skorla temsil edilmiştir.

T1DM grubuna özgü klinik değişkenler tanı tarihi, diyabet süresi ve son ölçülmüş klinik HbA1c yüzdesidir. HbA1c yalnız T1DM tanılı indeks çocuk satırlarında tanımlıdır; kardeş, kontrol indeks ve kontrol kardeş satırlarında tasarım gereği yapısal olarak eksiktir (*structural missing*). Final veri setinde 120 T1DM indeks çocuğun 39'unda HbA1c değeri kayıtlıdır ve tüm değerler klinik olarak makul aralıktadır. Serbest metin biçimindeki tanımlayıcı olabilecek alanların ele alınışı Etik Hususlar başlığında açıklanmıştır.

## Veri Toplama Araçları""":
        
        """## Değişkenler ve Tanımları

Çalışmanın değişken seti; grup (bağımsız), sonuç (bağımlı) ve eş değişkenler (kovaryatlar) olarak üç temel eksende yapılandırılmıştır. Analizlerdeki ana grup değişkeni, çocuğun rolünü (T1DM indeks, T1DM kardeş, kontrol indeks, kontrol kardeş) tanımlayan dört düzeyli bir faktördür; grup karşılaştırmalarında ise tanı grubu (T1DM / kontrol) kullanılmıştır. Sonuç değişkenleri; çocuğun algıladığı ebeveynlik tutumu boyutları, annenin kendi ebeveynliğine dair bildirimleri, kardeşler arası ilişkinin niteliği ve anne depresif belirti düzeyi olarak belirlenmiştir. Sonuçlar üzerinde karıştırıcı etki yaratabilecek yaş, cinsiyet, anne yaşı, kardeş yaş farkı, evdeki çocuk sayısı ve sosyoekonomik durum (SES) değişkenleri ise istatistiksel modellerde kovaryat olarak kontrol edilmiştir.

Sosyoekonomik durum (SES); ebeveynlerin eğitim ve meslek bilgilerine dayanan uluslararası bir dizin (ISEI) [@ganzeboomTreiman1996isei] ile ailenin maddi varlık göstergelerinin birleştirilmesiyle elde edilen üç katmanlı bir birleşik puan (kompozit skor) ile hesaplanmıştır. Temel modellerde bu değişken, doğrulayıcı faktör analizine dayalı bir gizil (latent) skor olarak kullanılmış; duyarlılık kontrollerinde ise literatürde bilinen eş-ağırlıklı diğer indeks formülleriyle de sağlaması yapılmıştır [@hollingshead1975].

Diyabet grubuna özgü klinik değişkenler; tanı süresi ve hastanın son ölçülmüş üç aylık kan şekeri (HbA1c) ortalamasıdır. Çalışma tasarımı gereği sağlıklı kardeşler ile kontrol grubunda HbA1c bulunmadığından, bu veri setindeki eksiklik "yapısal eksik veri" olarak tanımlanmış ve yalnızca HbA1c kaydı olan 39 T1DM hastasındaki keşifsel analizlerde kullanılmıştır. Verilerdeki açık uçlu kişisel bilgilerin nasıl anonimleştirildiği Etik Hususlar bölümünde detaylandırılmıştır.

## Veri Toplama Araçları"""
    }

    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            print("Successfully replaced section 3.5!")
        else:
            print("Failed to replace section 3.5!")

    with open("chapters/03_gerec_ve_yontem.qmd", "w", encoding="utf-8") as f:
        f.write(content)

process_file()
