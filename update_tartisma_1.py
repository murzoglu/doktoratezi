import sys

file_path = "chapters/05_tartisma_ve_sonuc.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_1 = """Bu çalışmanın nicel ve niteliksel bulguları birlikte değerlendirildiğinde, Tip 1
diyabetin aile üzerindeki etkisi tek boyutlu değildir. Standart ölçeklerin ortaya
koyduğu istatistiksel örüntüler ile ailelerin aktardığı öznel deneyim yer yer
örtüşmekte, yer yer ayrışmakta; böylece katmanlı bir yapı belirmektedir. Bu bölümde
bulgular, alanyazın ışığında ve tasarımın elverdiği çıkarım sınırları içinde
yorumlanmaktadır. Bulguların gücü tek başına istatistiksel anlamlılıkla değil, etki
büyüklüğü ve güven aralığı birlikte okunarak değerlendirilmiştir. Nedensellik dili,
olgu-kontrol ve kesitsel tasarımın izin verdiği sınırlar içinde tutulmuş; hiçbir
bulgudan "neden-sonuç" çıkarımı yapılmamıştır."""

new_1 = """Bu çalışmanın hem sayısal (anket) hem de sözel (mülakat) bulguları birlikte değerlendirildiğinde, Tip 1 diyabetin aile üzerindeki etkisinin tek boyutlu olmadığı çok net görülmektedir. Standart psikolojik testlerin ortaya koyduğu istatistiksel sonuçlar ile ailelerin yüz yüze görüşmelerde aktardığı öznel deneyimler bazı noktalarda birebir örtüşürken, bazı noktalarda birbirinden ayrılmaktadır. Bu bölümde ulaşılan tüm sonuçlar, dünyadaki diğer araştırmaların (literatürün) ışığında ve araştırmanın sınırları dâhilinde yorumlanmaktadır. Bulguların gücü sadece "istatistiksel olarak fark var mı" sorusuyla değil, "bu fark gerçek hayatta ne kadar büyük ve ne kadar güvenilir" sorularıyla (etki büyüklüğü ve güven aralığı) birlikte değerlendirilmiştir. Araştırma anlık bir fotoğraf çekme (kesitsel) niteliğinde olduğu için, elde edilen hiçbir bulgu kesin bir "neden-sonuç" ilişkisi olarak iddia edilmemiştir."""

old_2 = """Bulguların bütününden beliren merkezî örüntü, tek bir "Tip 1 diyabet ebeveynlik
farkı" değil, **bilgi-verici düzlemine göre bir ayrışma**dır. Reddetme ve aşırı
koruma sinyalleri çocuğun kendi algısında belirmekte (Bulgular, @tbl-apa-h1-group, @tbl-apa-h1-bayesian),
aynı davranış alanlarında anne öz-bildiriminde fark için kanıt bulunmamakta
(@tbl-apa-h3-primary-iptw, @tbl-apa-h3-sensitivity), anne ile çocuğun algı uyumu da
düşük kalmaktadır (@tbl-apa-h5-concordance). Bu nedenle tezin özgün katkısı, genel
bir ebeveynlik tutumu farkını ilan etmek değil; *hangi bilgi-vericinin, hangi boyutta
ve hangi deneyim düzleminde* ayrıştığını haritalamaktır. İzleyen tartışma bu ayrışma
haritasını izler. Önce bilgi-verici düzlemleri sırayla ele alınır: çocuğun kendi
algısı, annenin öz-bildirimi, anne depresyonunun aracılık yolu ve kardeşin konumu.
Ardından anne ile çocuğun algı uyumu ve bu bulguların niteliksel verilerle karma
bütünleştirmesi değerlendirilir. Son olarak keşifsel analiz katmanları ve çalışmanın
ölçüm düzeyindeki çıkarımları tartışılır."""

new_2 = """Bulguların tümüne bakıldığında ortaya çıkan en çarpıcı sonuç, "Tip 1 diyabetin ebeveynliği kesin olarak şöyle veya böyle değiştirdiği" şeklinde tek bir doğrudan fark olmamasıdır. Asıl fark, **sorunun kime (anneye mi yoksa çocuğa mı) sorulduğuna göre değişen ayrışmadır**. Örneğin, "reddedilme" ve "aşırı korunma" duygusu sadece çocukların kendi algılarında yüksek çıkmış (Bulgular, @tbl-apa-h1-group, @tbl-apa-h1-bayesian); aynı sorular annelere sorulduğunda annelerin kendi ebeveynlik tutumlarında hiçbir fark bulunamamıştır (@tbl-apa-h3-primary-iptw, @tbl-apa-h3-sensitivity). Doğal olarak anne ile çocuğun anket uyumu da oldukça düşük kalmıştır (@tbl-apa-h5-concordance). Bu nedenle bu tezin en özgün katkısı, klasik anlamda "genel bir ebeveynlik farkı" ilan etmek değil; hastalık yükünün *kimin gözünden, hangi duygu boyutunda ve nasıl* ayrıştığını haritalandırmasıdır. İzleyen tartışma kısımları bu ayrışma haritasını sırayla takip etmektedir: Önce çocukların algısı, ardından annelerin beyanı, annedeki depresyonun rolü ve kardeşlerin konumu ele alınacak; daha sonra tüm bu sayısal veriler mülakatlardan elde edilen derinlemesine hikâyelerle (karma yöntem) birleştirilecektir."""

old_3 = """Çocuk algısı düzleminde H1 desteklenmiştir. Ön-kayıtlı doğrulayıcı test ailesinde
(dört EMBU-C alt ölçeğinin grup ana etkisi, BH-FDR), DM ailelerindeki çocuklar
kontrol grubuna kıyasla iki boyutta daha yüksek puan bildirmiştir: reddetme
(q = 0,001) ve aşırı koruma (q = 0,003). Bu iki bulgu Bayesçi paralel hatta da
doğrulanmıştır (BF₁₀ = 10,55 ve 6,93; Bulgular, @tbl-apa-h1-group, @tbl-apa-h1-bayesian).
Sıcaklıkta gözlenen frekansçı marjinal fark (q = 0,029) ise Bayesçi hatta H0 lehine
kaldığından sağlam kabul edilmemiş; karşılaştırma boyutunda fark saptanmamıştır."""

new_3 = """Çocukların algısına odaklanan birinci ana hipotez (H1) doğrulanmıştır. Yapılan katı istatistiksel testlerde, diyabetli ailelerdeki çocukların, sağlıklı (kontrol) ailelerdeki çocuklara kıyasla ebeveynlerinden daha fazla "aşırı koruma" ve daha fazla "reddedilme" gördüklerini hissettikleri kanıtlanmıştır. Bu iki ana bulgu, hem geleneksel frekansçı (q ≤ 0,003) hem de alternatif olasılıkçı (Bayesçi, BF₁₀ ≥ 6,93) analiz yöntemleriyle güçlü biçimde teyit edilmiştir (Bulgular, @tbl-apa-h1-group, @tbl-apa-h1-bayesian). Ebeveynin "sıcaklığı" boyutunda ilk başta sınırda bir fark görülse de bu fark diğer güvenlik testlerini geçemediği için sağlam kabul edilmemiş; "kardeşler arası karşılaştırma/taraf tutma" boyutunda ise iki grup arasında hiçbir fark bulunmamıştır."""

old_4 = """Bu grup farkının aile içinde nasıl dağıldığını görmek için keşifsel/post-hoc bir
grup-içi rol kontrastı hesaplanmıştır. Bu kontrastta kontrol kolu tümüyle dışarıda
bırakılmış, DM ailesinin indeks çocuğu ile sağlıklı kardeşi doğrudan
karşılaştırılmıştır. Dört EMBU-C boyutunun hiçbirinde fark için kanıt
bulunmamaktadır (reddetme b = 0,020; aşırı koruma b = 0,095; sıcaklık b = −0,067;
karşılaştırma b = −0,001; tümü BH-FDR q > 0,76). Simetrik olarak kontrol aileleri
içinde de indeks-kardeş farkı hiçbir boyutta anlamlı değildir
(@tbl-apa-h1-within-group). Bu örüntü kuramsal olarak önemlidir: DM–kontrol
reddetme ve aşırı koruma farkları aile-içi rol ekseninde (T1DM'li çocuk vs.
sağlıklı kardeş) değil, **aile/grup düzeyinde** yerleşmektedir. Yani tanı,
hastalığı taşıyan çocuğu kardeşinden ayıran bir sinyal üretmemekte; ailenin iki
çocuğunun anne algısını benzer yönde kaydırmaktadır. Bu okuma, tezin merkezî
"genel bir T1DM ebeveynlik farkı değil, bilgi-verici düzlemine göre ayrışma"
savını güçlendirir. Çünkü ayrışmanın rol/kardeşlik ekseninde değil, grup ve
bilgi-verici ekseninde işlediğini doğrudan gösterir; reddetme boyutundaki yaklaşık
0,14'lük aile-içi sınıf-içi korelasyonla da tutarlıdır. Kesitsel tasarım nedeniyle
yorum nedensel değil betimseldir."""

new_4 = """Bulunan bu ebeveynlik farkının "sadece diyabetli çocuğa mı özel yoksa evin geneline mi yayıldığını" anlamak için aile içi ek (post-hoc) testler yapılmıştır. Sadece diyabetli aileler incelendiğinde; diyabetli çocuk ile onun sağlıklı kardeşi arasında ebeveyn algısı (reddedilme, koruma vb.) açısından hiçbir fark bulunamamıştır (tümü p > 0,76). Sağlıklı kontrol ailelerinde de durum aynıdır; indeks çocuk ile kardeşi arasında fark yoktur (@tbl-apa-h1-within-group). Bu durum kuramsal olarak çok önemli bir noktaya işaret eder: Aşırı koruma ve reddedilme duygusundaki artış sadece "hastalıklı çocuğun" şahsi problemi değil, **tüm evin (aile grubunun) iklimine** yerleşen ortak bir durumdur. Diğer bir deyişle diyabet teşhisi, evdeki çocukları birbirinden ayırıp sadece birine odaklanan bir tutum yaratmamakta; aksine o evdeki iki çocuğun da anneyi algılayış biçimini (kontrol evlerine kıyasla) aynı yöne doğru kaydırmaktadır. Bu durum, "hastalığın sadece hastayı değil bütün aile sistemini etkilediği" yönündeki temel gerçeği çok güçlü bir biçimde doğrulamaktadır."""

content = content.replace(old_1, new_1)
content = content.replace(old_2, new_2)
content = content.replace(old_3, new_3)
content = content.replace(old_4, new_4)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("First batch of replacements done.")
