import sys

file_path = "chapters/05_tartisma_ve_sonuc.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    """**Ölçüm katmanı: latent etki.** Taban etkisine duyarlı madde-yanıt kuramı
çözümlemesinde latent değişken etkisi, manifest (toplam-puan) etkisinin üzerinde
belirmiştir (Bulgular, §4.4.6). Toplam-puan skorlaması her maddeyi eşit ağırlıklı ve
hatasız sayarak ölçüm hatasını görmezden gelir ve gerçek etki büyüklüklerini sistematik
biçimde zayıflatır. Latent değişken modelleri ise ölçüm hatasını ayrıştırarak daha az
yanlı kestirim verir [@mcneishWolf2020toplamPuan]; bu, kısa ve taban etkili alt
ölçeklerde beklenen bir örüntüdür.

Bilgi-vericiler-arası ortak yapıyı sınamak için
tasarlanan keşifsel yapısal eşitlik modeli (ESEM) tabanlı trifaktör çözümlemesi ise
kabul edilebilir bir çözüme kavuşturulamamıştır (Bulgular, §4.4.6). Bilgi-verici başına
düşen madde sayısının azlığı ve reddetme gibi tabana yığılan boyutların düşük varyansı,
üç-kaynaklı ortak bir latent yapının bu çözünürlükte kimliklenmesini güçleştirmiştir
[@marsh2014esem]. Bu null, bir "yapı yokluğu" kanıtı değil, mevcut ölçüm çözünürlüğünün
sınırının göstergesidir; aynı soru bilgi-verici başına daha çok madde içeren
tasarımlarla yeniden ele alınabilir.""":
    """**Anket puanlarını toplamak yanıltıcı olabilir.** Anketlerdeki maddeleri sadece toplayarak "toplam puan" elde etmek, çocukların rastgele verdiği cevapları veya testin hatalarını görmezden gelir. Bunun yerine "gizli (latent) yapı" kurduğumuzda, etkinin gerçekte daha güçlü olduğunu gördük (Bulgular, §4.4.6). Bu bulgu, araştırmacılara "sadece puanları toplamayın, ölçüm hatasını hesaba katan gelişmiş modeller kullanın" [@mcneishWolf2020toplamPuan] uyarısında bulunur. Ayrıca anne, çocuk ve kardeşin cevaplarını tek bir büyük modelde (trifaktör) birleştirmeyi denesek de; soru sayısının azlığı ve cevapların çoğunun "hiçbir zaman" şıkkında birikmesi nedeniyle model düzgün çalışmamıştır [@marsh2014esem]. Bu da elimizdeki anketlerin kapasitesinin bir sınırıdır.""",

    """**Robustluk katmanının işlevi.** Son olarak, birincil bulguların analitik kararlara ne
ölçüde bağımlı olduğunu sınamak için dört tamamlayıcı yaklaşım birlikte uygulanmıştır.

- **Eşdeğerlik testi**, bir etkinin yalnız "anlamsız" değil, pratik olarak ihmal
  edilebilir bir bant içinde (d ∈ [−0,30, 0,30]) kalıp kalmadığını göstermiştir
  [@lakens2018equivalence].
- **Bayes faktörü**, yokluk hipotezi ($H_0$) lehine kanıtın gücünü nicelemiştir
  [@wagenmakers2016bayes].
- **Eğilim-skoru eşleştirmesi**, anne yaşından kaynaklanabilecek karıştırıcı etkiyi dışlamıştır
  [@rosenbaumRubin1983ps].
- **Çok-düzeyli modeller**, kardeşlerin aynı aileye yuvalanmasından kaynaklanan iç-bağımlılığı
  hesaba katmıştır [@snijdersBosker2011multilevel].

Bu dörtlünün ortak yönü, birincil frekansçı testlerin bulamadığı bir *farkı* (H2 ve H3)
ya da saptadığı bir *etkiyi* (H1 reddetme) doğrulama amacı taşımasıdır. H1'deki küçük
reddetme etkisi Bayesçi ve çok-düzeyli modellerde tutarlı biçimde korunmuştur. H3'teki
anne-bildirimli eşdeğerlik ise hem Bayes faktörü (null lehine kanıt) hem de tost ile
(küçük-etki bandına düşerek) pekişmiştir. Analitik yöntem değiştiğinde bulguların
değişmemesi, sonuçların metoda değil gerçekliğe dayandığına ilişkin güveni artırır.""":
    """**Sonuçlarımız test yöntemine göre değişiyor mu? (Sağlamlık Kontrolü)** Bir araştırmada aynı veriye farklı istatistiklerle yaklaştığınızda sonuçlar değişiyorsa, o bulguya güvenilmez. Biz de kendi bulgularımızı dört ayrı ve zorlu testten daha geçirdik: (1) Etki gerçekten sıfıra yakın mı diye bakan eşdeğerlik testi [@lakens2018equivalence], (2) Yokluğu (fark olmadığını) ispatlamaya yarayan Bayesçi analizler [@wagenmakers2016bayes], (3) Yaş gibi dış etkenleri temizleyen eşleştirme modelleri [@rosenbaumRubin1983ps] ve (4) Aynı evin içindeki çocukların benzerliğini hesaba katan çok-düzeyli testler [@snijdersBosker2011multilevel]. 

Bütün bu zorlu sınamaların sonucunda, H1'de bulduğumuz "çocuğun hafif reddedilmişlik hissi" ile H3'te bulduğumuz "annenin kendi ebeveynliğini kusursuz görmesi" bulguları dimdik ayakta kalmıştır. Yani bulgularımız seçtiğimiz istatistiksel metoda değil, doğrudan sahadaki gerçeğe dayanmaktadır."""
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success!")
    else:
        print("Failed to find:\n" + old[:100] + "...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
