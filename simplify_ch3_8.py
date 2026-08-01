import sys

file_path = "chapters/03_gerec_ve_yontem.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    """## Veri Toplama Süreci ve Veri Yönetimi

Tüm ölçme araçları, her aileyle tek bir görüşme oturumunda standart bir sırayla uygulanmıştır. Poliklinik başvurusunu izleyen dahil edilme değerlendirmesinden sonra ailelere çalışma tanıtılmış; anneden bilgilendirilmiş gönüllü olur ve çocuktan gelişimsel düzeye uygun muvafakat alınmıştır. Ardından demografik ve tıbbi bilgi formu, her iki çocuğa s-EMBU-C ve Kardeş İlişkileri Anketi, anneye s-EMBU-P ve Beck Depresyon Envanteri uygulanmıştır. Nitel alt örnekleme seçilen ailelerle bireysel görüşmeler yapılmıştır.

Toplanan veriler; standardizasyon ve aile eşleştirmesi aşamalarından geçirilerek çocuk-satırı ve aile-satırı olmak üzere iki referans veri seti biçiminde düzenlenmiştir. Referans veri setleri, madde düzeyi kanonik değerleri (standardizasyon sonrası; s-EMBU-C q25'in belgeli ters puanlaması dâhil) değişmez biçimde kilitlenmiştir. Toplam, ortalama ve alt ölçek skorları referans dosyalarda saklanmamış; çözümleme katmanında üretilmiştir. Bu ilke veri değişmezliğini sağlar ve çözümleme tekrarlanabilirliğini destekler. Alt ölçek toplamları yalnız ilgili tüm maddeler mevcutsa hesaplanmış; alt ölçek ortalamaları ise önceden sabitlenmiş en az %50 madde mevcutluğu eşiğiyle üretilmiştir. Kanonik çözümleme veri setine yalnız, önceden kaydedilmiş özet (SHA-256), satır sayısı ve sütun sayısı doğrulandıktan sonra erişilmiştir; böylece çözümlemenin daima aynı sabit veri tabanı üzerinde yürütülmesi sağlanmıştır.

Tüm veri standardizasyonu ve çıkarımsal çözümleme R ve Quarto ortamında gerçekleştirilmiştir. Çözümleme hattı `targets` iş akışıyla yeniden üretilebilir biçimde orkestre edilmiş, paket sürümleri `renv` ile sabitlenerek bilgisayar ortamları arasında tekrarlanabilirlik sağlanmıştır. Çekirdek çözümlemelerde kullanılan R istatistik yazılım paketleri şunlardır:

- yapısal eşitlik ve doğrulayıcı faktör modelleri için `lavaan` ve `semTools`;
- Bayesçi kestirim için `brms`/`rstan` (arka uçta `cmdstanr`) ve `blavaan`;
- eksik veri ataması için `mice`;
- eğilim skoru ve ağırlıklandırma için `WeightIt`, `MatchIt` ve `twang`;
- madde tepki kuramı için `mirt`;
- ağ çözümlemesi için `qgraph`, `bootnet` ve `NetworkComparisonTest`;
- çok evrenli çözümleme için `specr`;
- ölçülmemiş karıştırıcı duyarlılığı için `sensemakr`;
- eşdeğerlik testi için `TOSTER`;
- latent profil çözümlemesi için `tidyLPA` ve `mclust`;
- sağlam standart hatalar için `sandwich` ve `lmtest`;
- nedensel diyagram işlemleri (kovaryat seti türetme ve diyagramın ima ettiği koşullu bağımsızlıkların veriyle sınanması) için `dagitty`;
- meta-analitik havuzlama için `metafor`.""" :
    """## Veri Toplama Süreci ve Veri Yönetimi

Poliklinik başvurusundan sonra şartları sağlayan ailelere araştırma anlatılmış; hem annenin hem de çocuğun açık rızası alınmıştır. Ardından herkese kendi anketleri tek bir oturumda doldurtulmuştur. Derinlemesine görüşme yapılacak aileler ise ayrı bir odaya alınarak yüz yüze görüşmeler gerçekleştirilmiştir.

Toplanan tüm anket kâğıtlarındaki veriler bilgisayar ortamına girildikten sonra, ileride herhangi bir veri oynaması yapılamaması için tamamen "kilitlenmiştir" (kanonik kilit ve SHA-256 dijital parmak izi). Bu sayede araştırmanın sonuna kadar tüm analizlerin aynı taze ve bozulmamış veri havuzundan çekilmesi garanti altına alınmıştır. Analiz sırasında anket puanları toplanırken, bir alt ölçeğin hesaplanabilmesi için kişinin o bölümdeki soruların en az yarısını (%50) yanıtlamış olması şart koşulmuştur.

Tüm hesaplamalar uluslararası geçerliliği olan "R" istatistik dili ve "Quarto" yayın ortamında kodlanmıştır. Veri analizlerinin adımları; yapısal eşitlik (lavaan), Bayesçi analiz (brms), eksik veri ataması (mice) ve ağ modelleri (qgraph) gibi modern istatistik paketleri aracılığıyla, dışarıdan başka bir araştırmacının da kodları çalıştırıp aynı sonucu bulabileceği (tekrarlanabilir) şekilde sabitlenmiştir (`renv` ve `targets` iş akışlarıyla)."""
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success!")
    else:
        print("Failed to find:\n" + old[:100] + "...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
