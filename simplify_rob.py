import sys

file_path = "chapters/05_tartisma_ve_sonuc.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    """**Robustluk katmanının işlevi.** Son olarak, birincil bulguların analitik kararlara ne
ölçüde bağımlı olduğunu sınamak için dört tamamlayıcı yaklaşım birlikte uygulanmıştır.

- **Eşdeğerlik testi**, bir etkinin yalnız "anlamsız" değil, pratik olarak ihmal
  edilebilir ölçüde küçük olduğunu pozitif biçimde gösterebilmeyi sağlar
  [@lakens2018esdegerlik].
- **E-değeri temelli duyarlılık**, gözlenen bir ilişkiyi tümüyle açıklamak için gereken
  ölçülmemiş karıştırıcının ne kadar güçlü olması gerektiğini niceler
  [@vanderweeleDing2017evalue; @cinelliHazlett2020sensemakr].
- **Çoklu-evren ve spesifikasyon-eğrisi çözümlemesi** ise tek bir "doğru" analiz
  yerine, savunulabilir tüm analiz seçeneklerinin sonuçlarını birlikte sergileyerek bir
  bulgunun araştırmacı kararlarına duyarlılığını şeffaflaştırır
  [@steegen2016multiverse; @simonsohn2020specificationCurve].

Bu dört yaklaşımın sonuncusu, negatif kontrol ve falsifikasyon çözümlemesidir; birincil
etkinin sahte yordayıcı-sonuç eşlemelerinde beklenmedik biçimde belirip belirmediğini
sınamıştır. Sekiz sahte eşlemeden biri (aile numarası → EMBU-P sıcaklık; β = 0,098,
p = 0,003), rastlantısal yanlış-pozitif beklentisinin (%12,5 gözlenen oran, α = 0,05'te
beklenenin üzerinde) ötesinde, sekiz teste Bonferroni düzeltmesi (0,05/8 = 0,006)
sonrasında da anlamlı kalmıştır. Aile numarası kayıt sırasına bağlı bir dönem/kohort
vekili olduğundan, bu sinyal gerçek bir inert negatif kontrol değil, aşağıda ele alınan
dönem/merkez örtüşmesinin bir göstergesi olarak yorumlanmıştır. İki falsifikasyon
senaryosunda (DM süresi < 1 yıl; HbA1c ≤ 7,5) grup etkisi anlamsız kalarak (p > 0,10)
birincil null bulguyla tutarlı kalmıştır (Bulgular, §4.5). Bu dörtlü, birincil
sonuçların yönünü tek bir modelleme tercihine borçlu olmadığını göstermek ve kırılgan
oldukları noktaları açıkça işaretlemek için kullanılmıştır.""":
    """**Sonuçlarımız test yöntemine göre değişiyor mu? (Sağlamlık Kontrolü)** Bir araştırmada aynı veriye farklı istatistiklerle yaklaştığınızda sonuçlar değişiyorsa, o bulguya güvenilmez. Biz de kendi bulgularımızı dört ayrı ve zorlu testten geçirdik: (1) Bir etkinin sıfıra yakın olduğunu ispatlayan eşdeğerlik testleri [@lakens2018esdegerlik], (2) Gözden kaçmış bir dış etkenin (karıştırıcı) bulduğumuz sonucu çökertebilmesi için ne kadar güçlü olması gerektiğini ölçen duyarlılık analizleri [@vanderweeleDing2017evalue; @cinelliHazlett2020sensemakr], (3) "Ya modeli şöyle kursaydık?" sorusuna yanıt olarak binlerce farklı senaryoyu aynı anda çalıştıran çoklu-evren analizleri [@steegen2016multiverse] ve (4) Araştırmanın hata yapma potansiyelini görmek için kurduğumuz "sahte eşleşme" testleri (negatif kontrol ve falsifikasyon).

Tüm bu zorlu sınamalar, ana bulgularımızın tek bir istatistiksel tercihe sırtını dayamadığını, yani sonuçların "kurduğumuz modele" değil, "sahadaki gerçeğe" dayandığını kanıtlamak için yapılmıştır (Bulgular, §4.5). Sadece sekiz sahte testten birinde (kayıt sırasıyla ebeveyn sıcaklığı arasında) ilginç bir bağlantı çıkmış, ancak bunun tesadüf olmadığı, ailelerin farklı zamanlarda/merkezlerde çalışmaya dahil olmasından kaynaklandığı (dönem/kohort etkisi) anlaşılmıştır.""",

    """Artık ilişki yüzeyini inceleyen son keşif katmanı bu hipotez-üretici çerçeveyi üç
noktada genişletmiştir (Bulgular, §4.4.7).

- **İlk olarak**, anne öz-bildirimli ebeveynlik ile çocuğun algıladığı ebeveynlik
  arasındaki bağ (b-yolu) tüm alt ölçeklerde zayıf kalmıştır. Bu, anne depresyonu ile
  anne-bildirimli ebeveynlik arasındaki ilişkinin çocuk algısına doğrudan
  yansımadığını ve aracılık zincirlerindeki kırılmanın bu aktarım yolunda
  gerçekleştiğini düşündürmektedir.
- **İkinci olarak**, anne-bildirimli aşırı koruma esas olarak sosyo-demografik bir
  gradyanla ilişkilidir: daha genç ve daha düşük sosyoekonomik konumdaki annelerde daha
  yüksektir; hane kalabalıklığı bu yaş ve konumdan bağımsız bir katkı sağlamamıştır.
- **Üçüncü olarak**, anne depresyonu kardeş ilişki kalitesini yanlış-keşif düzeltmesi
  sonrası yordamamıştır; bu da kardeş ilişkisinin birincil çözümlemede (H2) grup farkı
  için kanıt bulunamamış örüntüyle tutarlıdır (eşdeğerlik sınanmadığından bir
  korunma/direnç kastedilmez).

Düzeltme sonrası ayakta
kalan tek ilişki, eşler-arası eğitim farkı ile anne reddetmesi arasındadır. Bağlamsal
moderatör taramasında ise yanlış-keşif düzeltmesi sonrası ayakta kalan bir etki
bulunmamıştır. Ebeveyn ayrımcı davranışı meta-analitik olarak yaygın bir olgu olmakla
birlikte [@buist2013siblingMeta], burada yalnız düzeltilmemiş düzeyde ve baba-kayırma
yönünde belirmiştir (d = −0,27); sosyal katmanlaşma, maternal komorbidite ve
maruziyet-yoğunluğu göstergeleri anlamlı ilişki üretmemiştir (Bulgular, §4.4.6). Bu
bulguların tümü küçük etkili, kesitsel ve öneri düzeyindedir.""" :
    """**Arka planda kalan diğer ince detaylar (Artık İlişki Yüzeyi).** (Bulgular, §4.4.7)
- **İlk olarak**, annenin anketlerde "ben çocuğuma şöyle davranıyorum" demesi ile çocuğun "annem bana böyle davranıyor" demesi arasındaki bağ çok zayıftır. Bu kopukluk, anne depresyonunun çocukta neden doğrudan reddedilme hissi olarak belirdiğini (aradaki ebeveynlik köprüsünün neden yıkıldığını) açıklamaktadır.
- **İkinci olarak**, annelerin çocuklarını "aşırı koruma" eğilimi, hastalığın kendisinden ziyade annenin yaşı ve sosyoekonomik durumuyla bağlantılı bulunmuştur. Daha genç ve gelir durumu daha düşük olan anneler, çocuklarını aşırı korumaya daha meyillidir. Evin kalabalık olması ise bu duruma ekstra bir etki yapmamaktadır.
- **Üçüncü olarak**, annenin depresyon düzeyinin kardeşler arasındaki ilişkinin kalitesini bozduğuna dair bir kanıt bulunamamıştır. Bu da sağlıklı kardeşin ilişki boyutunda diyabetten pek etkilenmemesi (H2) bulgumuzla uyumludur.

Tüm bu ikincil faktörleri, hatalı bulgu üretmemek için katı istatistik süzgeçlerinden geçirdiğimizde (yanlış-keşif düzeltmesi), ayakta kalan tek yan bulgu "anne-baba arasındaki eğitim farkının, annedeki reddetme davranışıyla ilişkisi" olmuştur. Yani geri kalan sosyo-demografik veya sağlıkla ilgili değişkenler ana bulguları değiştirecek güçte değildir [@buist2013siblingMeta]."""
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success!")
    else:
        print("Failed to find:\n" + old[:100] + "...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
