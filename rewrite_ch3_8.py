import re

def process_file():
    with open("chapters/03_gerec_ve_yontem.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        """## Veri Toplama Süreci ve Veri Yönetimi

Tüm ölçme araçları, her aileyle tek bir görüşme oturumunda standart bir sırayla uygulanmıştır. Poliklinik başvurusunu izleyen dahil edilme değerlendirmesinden sonra ailelere çalışma tanıtılmış; anneden bilgilendirilmiş gönüllü olur ve çocuktan gelişimsel düzeye uygun muvafakat alınmıştır. Ardından demografik ve tıbbi bilgi formu, her iki çocuğa s-EMBU-C ve Kardeş İlişkileri Anketi, anneye s-EMBU-P ve Beck Depresyon Envanteri uygulanmıştır. T1DM grubunda ek olarak tanı tarihi, diyabet süresi ve klinik HbA1c değeri kayıt üzerinden tamamlanmıştır. Nitel alt örnekleme seçilen ailelerle bireysel görüşmeler yapılmıştır.

Toplanan veriler; standardizasyon ve aile eşleştirmesi aşamalarından geçirilerek çocuk-satırı ve aile-satırı olmak üzere iki referans veri seti biçiminde düzenlenmiştir. Referans veri setleri, madde düzeyi kanonik değerleri (standardizasyon sonrası; s-EMBU-C q25'in belgeli ters puanlaması dâhil) değişmez biçimde kilitler. Toplam, ortalama ve alt ölçek skorları referans dosyalarda saklanmaz; çözümleme katmanında üretilir. Bu ilke veri değişmezliğini sağlar ve çözümleme tekrarlanabilirliğini destekler. Alt ölçek toplamları yalnız ilgili tüm maddeler mevcutsa hesaplanmış; alt ölçek ortalamaları ise önceden sabitlenmiş en az %50 madde mevcutluğu eşiğiyle üretilmiştir. Kanonik çözümleme veri setine yalnız, önceden kaydedilmiş özet (SHA-256), satır sayısı ve sütun sayısı doğrulandıktan sonra erişilmiştir; böylece çözümlemenin daima aynı sabit veri tabanı üzerinde yürütülmesi sağlanmıştır.

Tüm veri standardizasyonu ve çıkarımsal çözümleme R ve Quarto ortamında gerçekleştirilmiştir. Çözümleme hattı `targets` iş akışıyla yeniden üretilebilir biçimde orkestre edilmiş, paket sürümleri `renv` ile sabitlenerek bilgisayar ortamları arasında tekrarlanabilirlik sağlanmıştır. Çekirdek çözümlemelerde kullanılan paketler şunlardır:

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
- meta-analitik havuzlama için `metafor`.

## İstatistiksel Analiz""":
        
        """## Veri Toplama Süreci ve Veri Yönetimi

Poliklinik randevusu sırasında şartları sağlayan ailelere çalışma hakkında bilgi verilmiş, annelerden yazılı onam, çocuklardan ise yaşlarına uygun sözlü veya yazılı rıza alınmıştır. Formlar ve ölçekler her aileyle tek bir oturumda uygulanmıştır. Diyabetli gruba ait klinik bilgiler (HbA1c, tanı tarihi) doğrudan hasta dosyalarından teyit edilmiştir. Özel olarak seçilen küçük bir grupla (alt örneklem) aynı gün içinde yüz yüze nitel görüşmeler de tamamlanmıştır.

Araştırma verileri dijital ortama aktarılırken "çocuk düzeyinde" ve "aile düzeyinde" iki ayrı kilitli dosya (kanonik veri tabanı) oluşturulmuştur. Çözümlemelerin her seferinde birebir aynı orijinal veriden beslenmesini garanti altına almak için, bu ana dosyalara hiçbir şekilde "hesaplanmış ortalama" veya "toplam puan" kaydedilmemiş; bu hesaplamalar her istatistik analizi sırasında kilitli ham puanlar üzerinden otomatik formüllerle üretilmiştir. Veri güvenliğini doğrulamak amacıyla (kazara bir rakamın değişmediğinden emin olmak için), veri setinin parmak izi (SHA-256) doğrulanarak analize başlanmıştır.

Tüm istatistiksel işlemler, analiz kodlarının uluslararası bilim standartlarına uygun biçimde dondurulduğu (paket sürümlerinin sabitlendiği) R ve Quarto yazılım ortamlarında yürütülmüştür. (Genişletilmiş analizlerde; çok düzeyli modellemeler için `lavaan`, Bayesçi tahminler için `brms`/`blavaan`, kayıp veri yönetimi için `mice`, eşitleme işlemleri için `WeightIt` gibi alanının önde gelen algoritmaları kullanılmıştır).

## İstatistiksel Analiz"""
    }

    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            print("Successfully replaced section 3.8!")
        else:
            print("Failed to replace section 3.8!")

    with open("chapters/03_gerec_ve_yontem.qmd", "w", encoding="utf-8") as f:
        f.write(content)

process_file()
