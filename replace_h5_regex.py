import re

file_path = "chapters/04_bulgular.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Using regex to find the section and replace it
pattern = re.compile(r"### H5 — Diadik Tutarlılık.*?fig-13-h5-rsa-surface\.png\)\{#fig-h5-rsa-surface width=\"96%\" fig-align=\"center\"\}", re.DOTALL)

new_text = """### H5 — Diadik Tutarlılık (Anne-Çocuk Uyumu)

**Bulgu özeti.** Aynı evde yaşayıp aynı ilişkiyi deneyimlemelerine rağmen, "anne" ile "çocuğun" ebeveynlik tutumlarına verdikleri cevaplar arasındaki uyum oldukça düşüktür. Yani ebeveynlik ilişkisini anne farklı bir pencereden, çocuk bambaşka bir pencereden algılamakta; ikisi birbiriyle uzlaşamamaktadır. Ulaşılan bu uyumsuzluk, analiz edilen dört alt alanın (sıcaklık, koruma, reddetme, karşılaştırma) tamamında net biçimde görülmüştür. Dahası; diyabetli ailelerdeki anne-çocuk anlaşmazlığı ve uyumsuzluğu, kontrol ailelerindekine kıyasla bazı tutumlarda daha da belirgindir (yani kontrol grubunda uyum diyabete kıyasla nispeten daha yüksektir).

*Kanıt* — Anne ile çocuk arasındaki ilişkinin bu iki cepheden nasıl göründüğü (uyum), beş farklı ve karmaşık istatistiksel yöntemle incelenmiştir. Her bir yöntem uyumun farklı bir cephesine bakar: puanların birebir tutarlılığı, uyumsuzluğun bir yüzey haritasındaki yeri, ailenin ortak dokusu vb. Araştırma başlamadan önce belirlenen kurala göre, diyabet ve kontrol grupları arasında "net bir fark" olduğunun söylenebilmesi için bu beş yöntemden en az üçünün aynı yönü işaret etmesi gerekmiştir. Sonuçlar şu şekildedir:

**Strateji 1 (Doğrudan Puan Uyumu).** Anne ile çocuğun verdiği ham anket puanlarının ne kadar örtüştüğüne bakılmıştır. Bu yöntemle ölçülen tutarlılık puanı 0,00 ile 0,10 arasında çok düşük çıkmıştır; bu bilimsel eşiklerde "zayıf/yetersiz uyum" anlamına gelir. Hatta diyabetli ailelerde puanlar sıfırın altına bile inmiştir (yani anne ile çocuğun verdiği yanıtlar birbirinden tamamen kopuktur). Genel olarak kontrol grubundaki anne-çocuk tutarlılığı, diyabetli gruba göre tüm alt başlıklarda (sıcaklık, koruma, reddetme, karşılaştırma) daha yüksektir. Uyum oranlarının görsel haritası @fig-h5-bland-altman içinde sunulmuştur.

**Strateji 2 (Yanıt Yüzeyi Analizi).** Annenin ve çocuğun puanlarının nasıl farklılaştığını ve bunun annenin depresyonuyla olan ilişkisini bir "3 boyutlu harita" gibi çizen bu yöntemde, çok ilginç bir bulgu ortaya çıkmıştır: Diyabetli grupta, anne ile çocuğun reddetme algısı zıtlaştıkça (örneğin anne "çocuğumu reddetmiyorum", çocuk ise "annem beni reddediyor" dedikçe) annenin depresyon skoru belirgin biçimde artmaktadır. Bu örüntü sağlıklı kontrol grubunda hiç görülmemiştir. İlgili haritalar @fig-h5-rsa-surface içinde yer almaktadır.

**Strateji 3 (Ortak Yazgı / Aile Doku Modeli).** Aile bireylerinin "ortak tek bir aile ruhu" etrafında toplanıp toplanmadığına bakılmıştır. Sıcaklık dışında, reddetme ve karşılaştırmada bu "ortak doku" puanları o kadar düşüktür ki, istatistiksel sistem hatası vermiştir. Diyabetli ailelerin "ortak doku/uyum" puanı kontrol ailesinden de düşüktür; bu da diyabetli ailelerde "tek ve ortak bir tutum/algı" varsayımının geçersiz olduğunu kanıtlar.

**Strateji 4 (Saf / Gizli Uyum Modeli).** Testlerin kendi ölçüm hataları matematiksel olarak temizlenip aradaki "saf ilişkiye" bakıldığında; kontrol grubundaki anneler ile çocukların tutumları arasındaki pozitif uyum (örneğin sıcaklıkta 0,26, korumada 0,55) diyabetli gruba göre hep daha yüksek kalmıştır. Yine de veri yapısı nedeniyle bazı katsayılar çok dalgalanmış ve bu modelden çıkan kesin sonuçlara ihtiyatla yaklaşılmıştır.

**Strateji 5 (Anlam Ortaklığı / Kenny k-Katsayısı).** İki kişinin gerçekte ne ölçüde aynı şeyden bahsettiğini ifade eden bu oranda; sıcaklıkta (0,19'a karşı 0,02), aşırı korumada (0,36'ya karşı 0,08) ve karşılaştırmada (0,20'ye karşı 0,09) kontrol grubunun uyumu, diyabetli gruba kıyasla bariz şekilde daha yüksek bulunmuştur.

**Sentez.** Baştaki kuralımız olan "bir tutumda uyum var demek için en az 3 strateji onaylamalıdır" şartı hiçbir grupta ve hiçbir durumda sağlanamamıştır. Yani anne-çocuk ikilisindeki ebeveynlik algısı uyumu genel olarak çok zayıftır. Daha da önemlisi; denenen 5 yöntemin tamamında (5/5) ve tüm alt boyutlarda, diyabetli anne-çocuk ikilisinin fikir ayrılığı kontrol grubuna göre çok daha belirgindir. Başka bir ifadeyle Tip 1 diyabet, ebeveynlik algısı konusunda anne ile çocuk arasındaki makası sağlıklı ailelere kıyasla daha da açmıştır.

Tüm bu karmaşık stratejilerin özet sayısal dökümü @tbl-apa-h5-concordance içinde verilmiştir.

```{r}
#| label: tbl-apa-h5-concordance
#| tbl-cap: "H5 anne-çocuk uyumu (tutarlılık) tablosu: Annenin ebeveynlik anketi puanı ile çocuğun aynı ankete verdiği puan arasındaki uyum; sınıf-içi korelasyon, yüzey haritası, ortak yazgı, saf uyum ve Kenny anlam ortaklığı gibi her biri farklı bir açıya bakan 5 istatistiksel strateji ile özetlenmiştir. Okuma anahtarı: Her strateji grubun uyum veya uyumsuzluğuna dair yön belirtir (diyabet > kontrol veya kontrol > diyabet gibi). 5 stratejinin tamamına bakıldığında, kontrol grubundaki uyumun diyabete göre daha yüksek olduğu net biçimde görülür."
apa_render_table("t13_h5_concordance", group_col = "Strateji")
```

![H5 Puan tutarlılığı haritası: Anne ile çocuğun aynı soruya verdiği puanların uyumu (Bland-Altman grafiği). Ortadaki kalın çizgi puan farkının sıfır olduğunu, noktalar ise ailelerin cevaplarını gösterir. Okuma anahtarı: Noktalar yatay sıfır çizgisi etrafında ne kadar dar (sıkı) bir alanda toplanıyorsa, anne ile çocuğun verdiği cevaplar o kadar aynıdır (uyumludur). Sınırların geniş olması aradaki fikir ayrılığının/uyumsuzluğun büyük olduğunu gösterir.](docs/assets/figures/carbon/primary/fig-12-h5-ba-grid.svg){#fig-h5-bland-altman width="96%" fig-align="center"}

![H5 uyumsuzluk (yanıt yüzeyi) 3D haritası: Annenin ebeveynlik puanı ile çocuğun puanı arasındaki uyumun/uyumsuzluğun annenin depresyonuyla (zemin yüksekliği) ilişkisini gösteren grafik. Sadece sıcaklık ve reddetme boyutları için çizilmiştir. Tabandaki kesik çizgi, anne ile çocuğun tam olarak aynı puanı verdiği "uyum hattı"dır. Okuma anahtarı: Sağdaki grafikte (diyabet reddetme), kesik çizgiye dik olan hatta (anne ve çocuğun fikirleri zıtlaştıkça) yüzeyin yukarı kıvrıldığı (depresyonun arttığı) görülmektedir. Bu tehlikeli zıtlaşma örüntüsü kontrol grubunda yoktur.](docs/assets/figures/carbon/primary/fig-13-h5-rsa-surface.png){#fig-h5-rsa-surface width="96%" fig-align="center"}"""

if pattern.search(content):
    content = pattern.sub(new_text, content)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replace successful!")
else:
    print("Pattern not found in the file.")
