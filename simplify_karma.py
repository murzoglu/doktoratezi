import sys

file_path = "chapters/05_tartisma_ve_sonuc.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    """- **Açıklayıcı genişleme**, niteliksel kolun bir nicel bulgunun deneyimsel bağlamını
  sunmasıdır; bu bağlamı sunar ama nedenini kanıtlamaz.
- **Tamamlayıcılık**, iki kolun aynı olgunun farklı düzeylerini ölçmesi ve birlikte
  daha tam bir tablo vermesidir.
- **Uyum** ise her iki kolun aynı olguyu aynı yönde işaret etmesidir: nicel kol
  mertebe ve yönü ölçer, niteliksel kol aynı örüntünün anlatısal çerçevesini
  betimler.

Bulguların bu çerçevede eşleştirilmiş sunumu için birleşik gösterim tablosuna
bakılabilir (Bulgular, @tbl-apa-result-synthesis, birleşik gösterim).

H1 çocuk-reddetme sinyali ile Tip 1 diyabetli çocuğun içeriden deneyimi arasında
açıklayıcı genişleme ilişkisi vardır: niteliksel normalleştirme dili, nicel reddetme
algısının deneyimsel bağlamını sunar ancak onun mekanizması değildir.
<!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h1-karar -->

H2 kardeş null
bulgusu ile sağlıklı kardeşin görünmeyen yükü arasında tamamlayıcılık ilişkisi
bulunur: grup puanı düzeyinde görünmeyen yük, niteliksel kolda gündelik yaşamda
taşınan biçimiyle görünür olur. İki kol farklı düzeyleri ölçmektedir. Bu ayrışma,
Dinleyici ve arkadaşlarının çocuk-ebeveyn algı farkıyla (%30,4'e karşı %15,1)
[@dinleyici2019siblingQoLTurkiye] dış örneklemde de örtüşmektedir.
<!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h2-karar -->

H3 anne öz-rapor
eşdeğerliği ile anneliğin tıbbi bakıcıya kayması arasında açıklayıcı genişleme
ilişkisi vardır: sınırlı öz-rapor farkı, psikolojik yük yokluğunun değil, bakımın
ahlaki zorunluluk olarak içselleştirilmesinin ve öz-bildirime doğrudan
yansımamasının olası bağlamsal kanıtı olarak okunur.
<!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h3-karar -->

H4 yapısal yolları ile
aynı temanın suçluluk ve sürekli tetikte olma örüntüsü arasında uyum ilişkisi vardır:
nicel kol ilişkinin mertebe ve yönünü ölçer, niteliksel kol aynı deneyim alanının
anlatısal çerçevesini betimler. <!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h4-karar -->

H5 diadik uyumsuzluğu ile aynı evde üç farklı deneyim teması arasında açıklayıcı
genişleme ilişkisi vardır: algı ayrışması büyük ölçüde rol-temelli deneyim farkının
nicel yansımasıdır; ölçüm ve eşik işleyişi farklılıklarının katkısı ise bu tasarımda
tümüyle dışlanamaz. <!-- kaynak: niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-4 -->

Bu bütünleştirmelerin toplamı, triadik bilgi-verici asimetrisinin bu çalışmanın
birincil katkısı olduğunu göstermektedir: ayrışma analitik gürültü değil, iki
tasarımın birlikte kurulmasıyla üretilen bilimsel bir sonuçtur. Ayrışmanın bir
"hata" değil teorik katkı olarak okunması, karma yöntem disiplininin gereğidir.
Örneklem asimetrisi (nicel 241 aile — nitel 7 aile), bu bütünleşik okumayı
istatistiksel bir genelleme değil tamamlayıcı bir kanıt sunumu olarak
konumlandırmaktadır.""":
    """- **Açıklayıcı genişleme**: Anketlerin (sayıların) bize gösterdiği durumun 'gerçek hayatta nasıl yaşandığını' derinlemesine görüşmelerin anlatmasıdır.
- **Tamamlayıcılık**: Sayıların bir açıyı, görüşmelerin ise eksik kalan diğer açıyı ölçerek yapbozu tamamlamasıdır.
- **Uyum**: Her iki yöntemin de aynı şeyi söylemesidir; sayılar etkinin şiddetini gösterirken, görüşmeler bu etkinin hikayesini anlatır.

Bu üç kavram ışığında bulguları bir araya getirdiğimizde şu manzara ortaya çıkmaktadır (ayrıca bkz. @tbl-apa-result-synthesis):

**Çocukların reddedilme hissi (H1) ile "çocuğun iç dünyası" arasındaki ilişki (Genişletme):** Sayılarda gördüğümüz o hafif reddedilmişlik hissinin ardında, çocukların kendilerini "hasta" değil "normal" gösterme çabası ve ailelerinin müdahalelerini kısıtlama olarak görmeleri yatar. 
<!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h1-karar -->

**Kardeşlerin anketlerde fark göstermemesi (H2) ile "görünmeyen yük" teması (Tamamlayıcılık):** Anket sonuçlarına bakılırsa diyabetli kardeş ile sağlıklı kardeşin hisleri arasında fark yoktur. Ancak derinlemesine görüşmeler, sağlıklı kardeşin hayatının baştan aşağı değiştiğini ve gizli bir bakım yükü taşıdığını ortaya çıkarmıştır. İki yöntem birbirini tamamlayarak görünmez olanı görünür kılmıştır. Bu durum, Türkiye'deki diğer araştırmaların (örneğin Dinleyici ve ekibi, ebeveyn-çocuk algısında %30'a karşı %15'lik fark) bulgularıyla da örtüşmektedir [@dinleyici2019siblingQoLTurkiye].
<!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h2-karar -->

**Annelerin "bizde sorun yok" demesi (H3) ile "tıbbi bakıcıya dönüşme" teması (Genişletme):** Annelerin anketlerde kontrol grubuyla aynı puanları alması, ortada bir yük olmadığı anlamına gelmez. Görüşmeler göstermiştir ki anneler bu ağır bakım işini bir "annelik görevi" olarak o kadar içselleştirmiştir ki, bunu bir şikayet unsuru olarak anketlere yansıtmamaktadır.
<!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h3-karar -->

**Depresyonun etkisi (H4) ile "sürekli tetikte olma ve suçluluk" teması (Uyum):** Anketlerin gösterdiği "annenin depresyonu çocuğu etkiler" bulgusu, görüşmelerdeki annelerin "geceleri sürekli şeker ölçme, uyuyamama ve çocuğuma yetemiyorum suçluluğu" anlatılarıyla birebir örtüşmüştür. Sayılarla hikaye burada tam olarak hizalanmıştır.
<!-- kaynak: docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h4-karar -->

**Anne-çocuk uyuşmazlığı (H5) ile "aynı evde farklı dünyalar" teması (Genişletme):** Anketlerde anne ve çocuğun cevaplarının birbirini tutmamasının nedeni anketin hatalı olması değil; anne, diyabetli çocuk ve kardeşin hastalık sürecini bambaşka pencerelerden yaşamalarıdır.
<!-- kaynak: niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-4 -->

Tüm bu birleşimler bize şunu söyler: Çalışmamızın en büyük katkısı, "anne ve çocuk farklı şeyler söylüyor, demek ki veriler hatalı" demek yerine; "bu fark, olayın ta kendisidir" gerçeğini ortaya koymasıdır. Elbette niteliksel çalışmadaki 7 aileyi, anket yaptığımız 241 aileye matematiksel olarak genellemiyoruz; sadece rakamların ardındaki ruhu anlamak için tamamlayıcı bir kanıt olarak sunuyoruz."""
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success!")
    else:
        print("Failed to find:\n" + old[:100] + "...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
