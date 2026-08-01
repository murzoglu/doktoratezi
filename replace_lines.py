import sys

file_path = "chapters/03_gerec_ve_yontem.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_content = """### Duyarlılık ve sağlamlık çözümlemeleri (Ne kadar eminiz?) {#sec-cok-evren}

Temel analizlerin sonuçları tek bir formüle bel bağlamasın diye, "Acaba yaş yerine eğitimi alsaydık ne olurdu?" gibi binlerce olası hesaplama kombinasyonu aynı anda çalıştırılmıştır (çok-evrenli analiz) [@steegen2016multiverse]. Klasik matematikte bir sonucun "anlamsız" çıkması, o konunun "tamamen etkisiz" olduğunu kanıtlamaz. Bu yüzden biz, o etkinin pratikte sıfıra yakın (önemsiz) olduğunu pozitif bir şekilde kanıtlayan eşdeğerlik (TOST) testleri de kullandık [@lakens2017equivalence]. 

Dışarıdan gelebilecek ve bizim ölçemediğimiz bir gizli etkinin bulgularımızı çökertebilmesi için ne kadar güçlü olması gerektiğini matematiksel olarak hesapladık (E-değeri) [@cinelliHazlett2020sensemakr; @vanderweeleDing2017evalue]. Ayrıca ailelerin anketlere dahil olma sırasıyla sıcaklık hissi arasında bilerek sahte bağlantılar aradık (negatif kontrol); burada sahte bir bağlantı tespit etmemiz, hastaların farklı aylarda veya yıllarda çalışmaya alınmasının veriyi biraz etkileyebildiğini dürüstçe bize gösterdi [@lipsitch2010negativeControls].

### Bayesçi paralel hat (İkinci bir görüş)

Temel istatistikler, "fark var" diyebilir ama "kesinlikle fark yok" diyemez. Sırf bu eksikliği kapatmak ve "farkın olmadığını" da kanıtlayabilmek için tüm temel hipotezler Bayesçi istatistik denilen alternatif bir evrende baştan sona tekrar test edilmiştir [@pinquart2013]. Bu yöntemde, dünyadaki mevcut literatürün ne söylediği denklemin içine "ön bilgi" (önsel) olarak dâhil edilir. Binlerce kez tekrarlanan simülasyonların sonucunda (Stan arka ucu ile), çıkan farkların "güvenilir bir aralıkta" olup olmadığı kanıtlanmıştır [@wagenmakers2010; @burkner2017brms; @kruschke2018rope; @vehtari2021rhat].

### Tamamlayıcı ve keşifsel çözümleme katmanları (İleri İpuçları)

Aşağıdaki kısımlar, temel sorularımızı (hipotezleri) test etmek için değil, gelecekteki araştırmalara ışık tutması (yeni ipuçları bulması) amacıyla veri denizinin biraz daha derinlerine daldığımız kısımlardır. Hiçbirisi kesin kanıt iddia etmez, sadece korelasyon ve öneri boyutundadır:

- **Aracılık:** Annenin depresyonu doğrudan mı çocuğu etkiler yoksa annenin davranışları (ebeveynliği) bozularak mı çocuğu etkiler diye köprü (aracı) arayan yollar [@hayes2018introduction; @imaiKeeleYamamoto2010mediationDuyarlilik].
- **Tiplere ayırma (Latent tipoloji):** Annelerin anketlere verdiği cevaplardan onları "benzer özelliklere sahip ebeveyn gruplarına" bölen modeller.
- **Ağ (Network):** Değişkenlerin uzayda birbirini nasıl çektiğini veya ittiğini gösteren örümcek ağı benzeri haritalamalar.
- **Klinik fayda ve sınıflandırma:** "Birkaç anket sorusuna bakarak annenin depresyonda olup olmadığını tespit edebilir miyiz?" diye düşündüğümüz ve "bu testin klinikte kullanılmasının zararı/yararı ne olur" diye tarttığımız risk tarama modelleri [@vickersElkin2006dca]. 
- **Diyabetin tıbbi ağırlığı (Klinik faktörler):** Çocuğun kan şekerinin (HbA1c) veya diyabet süresinin ebeveynlik algısını bozup bozmadığına baktığımız ancak veri sayısı çok az (39 çocuk) olduğu için "kesin kanıt" diyemediğimiz bölüm.

Bunların yanında istatistiksel modellerin kendisini zorlayan birtakım ölçüm genişletmeleri de yapılmıştır (Örneğin güvenilirliğin iki faktöre bölünmesi, taban etkisine hassas kuramlar, diyagram doğrulamaları vb. bkz. [-@sec-kesifsel-genisletme]). Son olarak, arka planda kalan diğer dış etkenlerin (sosyal durumun, aile kalabalıklığının veya çocuğun yaşının) genel tabloyu bozup bozmadığı da hata payları düzeltilerek ayrıca raporlanmıştır.
"""

# Replace lines 215 to 267 (index 214 to 267)
lines[214:267] = [new_content]

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(lines)
    
print("Replaced lines successfully!")
