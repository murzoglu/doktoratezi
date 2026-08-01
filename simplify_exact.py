import sys

file_path = "chapters/05_tartisma_ve_sonuc.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    """Goodman ve arkadaşlarının 193 çalışma ve 80.851 anne-çocuk ikilisini kapsayan
meta-analizinde ise tüm ilişkiler küçüktür (içselleştirme r = 0,23; genel
psikopatoloji r = 0,24). Kritik biçimde, anne-bildirimine dayalı ölçümler etkileri
şişirmektedir [@goodman2011maternalMetaanalytic]. Mevcut çalışmadaki
standartlaştırılmış yolların bu küçük etki bandının üst
sınırında konumlanması hem literatürle tutarlıdır hem de "anne-bildirimi şişirmesi"
uyarısı aracılığıyla H3'teki öz-rapor sınırını pekiştirir. Depresyon → ebeveynlik
(a-yolu) ilişkisinin sağlamlığı, yalnız boylamsal tasarımları birleştiren
Goodman ve arkadaşlarının metaSEM derlemesinde a-yolu için r = 0,15 (%95 GA
0,12-0,17) olarak doğrulanmıştır [@goodman2020parentingMediator].""":
    """Yine Goodman ve ekibinin 80 binden fazla anne-çocuğu incelediği devasa çalışmada, depresyon ile ebeveynlik arasındaki ilişkinin aslında rakamsal olarak küçük (r = 0,23 civarı) olduğu bulunmuştur. İşin ilginç yanı, annelerin anketlerde (kendi beyanlarında) bu etkiyi gereğinden fazla şişirme eğiliminde olmasıdır [@goodman2011maternalMetaanalytic]. Bizim araştırmamızda çıkan sonuçların da tam bu sınırda kalması, annelerin "kendilerine dair anketleri doldururken" (H3) yanıltıcı bir tablo çizebileceği uyarımızı destekler. Depresyonun ebeveynliği etkilediği gerçeği, uzun yıllar süren takiplerle de (r = 0,15) ayrıca kanıtlanmıştır [@goodman2020parentingMediator].""",

    """Bu bağ Tip 1 diyabet bağlamına da taşınmıştır. Jaser ve arkadaşlarının okul çağındaki
Tip 1 diyabetli çocuklar ve anneleriyle yürüttüğü, 108 çocuk ve anneyi kapsayan
çalışmada anne-çocuk depresif belirti ilişkisi güçlüdür (r = 0,44; p < 0,001).
Çocuğun algıladığı aile sıcaklığı bu ilişkide kısmi aracıdır
(standartlaştırılmış katsayı 0,44'ten 0,34'e düşmekte; Sobel z = 2,05; p = 0,04).
Aile bağlılığı ise anlamlı aracı değildir [@jaser2007t1dmMediators].""":
    """Bu durum Tip 1 diyabet dünyası için de geçerlidir. Jaser ve ekibinin 108 diyabetli çocuk ve annesiyle yaptığı araştırmada, annenin depresyonu ile çocuğun depresyonu arasında çok güçlü bir bağ bulunmuştur (r = 0,44). Annenin çocukla kurduğu 'sıcaklık', bu depresyonun çocuğa geçişini engelleyen veya yavaşlatan kısmi bir filtre görevi görmüştür [@jaser2007t1dmMediators].""",

    """Bu yapısal örüntünün bilgi-verici düzlemleri arasında bir köprüsü de vardır.
Keşifsel çözümlemede güncel depresif şiddeti yüksek (Beck ≥ 17) annelerin
çocukları, DM grubu ve antidepresan kullanımından bağımsız olarak daha yüksek
reddetme (b = 0,13; p = 0,004) ve karşılaştırma (b = 0,24; p = 0,003) algısı
bildirmiştir (Bulgular, §4.4.6). Bu bağ, anne depresif yükünün öz-raporlu
ebeveynliğe değil çocuğun algısına yansıyabildiğini göstererek H4 ile H1'i
birbirine bağlar. Aynı bağ, reddetme sinyalinin neden anne öz-bildiriminde değil
çocuk düzleminde belirdiğine ilişkin bir mekanizma da önerir. Örüntü, maternal
psikopatolojinin çocuk çıktısına aktarımını çoklu risk süreçleri üzerinden
modelleyen bütünleştirici çerçeveyle [@goodman1999risk] tutarlıdır; kesitsel
olduğundan mekanizma değil hipotez düzeyinde okunmalıdır.

Bu bağın Tip 1 diyabete özgü karşılığı yeni Türk kanıtıyla da desteklenir. 129
anne-çocuk diyadıyla yürütülen yapısal eşitlik çalışmasında annelerin depresyon,
anksiyete ve bakım yükü düzeyleri çocukların duygusal-davranışsal güçlükleriyle
güçlü biçimde ilişkili bulunmuştur (r = 0,51-0,77). Aynı çalışmada bakım yükü →
ebeveyn sıkıntısı → çocuk hastalık algısı yolu anlamlı çıkmıştır (β = 0,52-0,66)
[@akdoganDuken2026caregiver]. Tip 1 diyabetli 390 ergen-anne örnekleminde ise
klinik düzeyde depresif belirti gösteren annelerin ergenlerinde daha yüksek HbA1c
gözlenmiştir (%9,6'ya karşı %8,6; d = 0,48) [@abadula2024maternalDepr]. Algı
düzleminde, Türkiye'nin de dahil olduğu dokuz ülkeden 1219 diyadı beş yıl izleyen
çalışmada anneler ergenlerden sistematik olarak daha yüksek sıcaklık
bildirmiştir. Algı tutarsızlığının büyüklüğü ise ergen içselleştirme
belirtileriyle ilişkili bulunmuştur [@esposito2025discrepancy]; bu, çocuk
algısının indirgenemez önemini pekiştirir.""":
    """Daha da önemlisi, annenin hissettiği depresyon sadece kendi psikolojisinde kalmamakta, çocuğun algısına doğrudan sıçramaktadır. Bu çalışmada (ek analizlerde); depresyon testinden yüksek (Beck ≥ 17) puan alan annelerin çocukları, -hastalıktan veya annenin ilaç kullanıp kullanmamasından bağımsız olarak- kendilerini bariz biçimde daha fazla 'reddedilmiş' (p = 0,004) ve diğer çocuklarla 'kıyaslanmış' (p = 0,003) hissettiklerini beyan etmiştir. Bu bulgu, H4 (annenin depresyonu) ile H1 (çocuğun reddedilme hissi) arasındaki kayıp köprüyü kurar. Annenin ruhsal sıkıntısı anketlerdeki kendi beyanına yansımasa bile, çocuğun omuzlarına 'reddedilmişlik hissi' olarak doğrudan çökmektedir [@goodman1999risk].

Annenin ruh hali ile diyabetli çocuğun durumu arasındaki bu geçişgenlik, yeni Türkiye verileriyle de desteklenmektedir. 129 anne-çocukla yapılan bir araştırmada; annedeki depresyon, kaygı ve bakım yükünün çocuğun duygusal/davranışsal sorunlarıyla doğrudan bağlantılı olduğu kanıtlanmıştır [@akdoganDuken2026caregiver]. Hatta 390 ergen ve anneyi kapsayan başka bir çalışmada, annesi klinik düzeyde depresyonda olan çocukların kan şekeri (HbA1c) kontrollerinin bile diğerlerinden daha kötü (%9,6'ya karşı %8,6) olduğu gösterilmiştir [@abadula2024maternalDepr]. 1219 ailenin beş yıl izlendiği uluslararası bir projede ise annelerin sürekli kendilerini 'ergenlerden daha sıcak ebeveynler' olarak görmesi, çocukların içsel sorunlar yaşamasını engelleyememiştir [@esposito2025discrepancy]. Kısacası, anne 'ben sıcak bir anneyim' dese de önemli olan çocuğun bunu nasıl hissettiğidir."""
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success!")
    else:
        print("Failed to find:\n" + old[:100] + "...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
