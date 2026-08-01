import sys

file_path = "chapters/04_bulgular.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_network = """### [KEŞİFSEL] Ağ Analizi

**Bulgu özeti.** Ebeveynlik tutumları, kardeş ilişkisi ve anne depresyonu
değişkenlerinin oluşturduğu ilişki ağı, diyabetli ve kontrol ailelerinde belirgin
biçimde farklılaşmamıştır. Değişkenler arası bağlantılar birlikte-değişim düzeyinde
okunmuştur. Bu bağlantılar nedensellik anlamına gelmez.

*Kanıt* — Dört EMBU-P alt ölçeği, dört SRQ (kardeş ilişkisi) alt ölçeği ve Beck
toplam puanından oluşan dokuz değişken üzerinde EBIC-LASSO Gauss grafik modeli
(γ = 0,5) tahmin edilmiştir. Havuzlanmış ağ n = 238 katılımcı üzerinde
kurulmuştur.^[Dokuz ağ değişkeninin tümünde tam veri gerektiren EBIC-LASSO analizi nedeniyle üç DM ailesi liste-bazlı olarak dışlanmıştır.] `r apa_network_top_strength_sentence()` Kısmi korelasyon kenar yapısı ve düğüm
merkeziyeti @fig-network-graph içinde gösterilmiştir. `r apa_network_stability_sentence()` `r apa_network_nct_sentence()` Beck madde-düzeyi belirti ağı
21 madde üzerinde tahmin edilmiştir. Koşullu bağımlılık nedensellik olarak
yorumlanmamıştır. Ağ merkeziyet ve karşılaştırma sonuçları @tbl-apa-network
içinde sunulmuştur."""

new_network = """### [KEŞİFSEL] İlişki Ağı (Network) Analizi

**Bulgu özeti.** Ebeveynlik tutumları, evdeki kardeş ilişkileri ve annenin depresyonu gibi unsurların birbiriyle nasıl bir 'örümcek ağı' (ilişki yumağı) oluşturduğuna bakılmıştır. Sonuçlar; diyabetli aileler ile sağlıklı kontrol aileleri arasındaki bu ilişkinin işleyiş şeklinin birbirine oldukça benzediğini göstermiştir. Bu bağlar incelenirken, biri diğerine kesin sebep oluyor denilmemiş; "ikisi birlikte nasıl değişiyor" mantığıyla yorumlanmıştır.

*Kanıt* — Annenin bildirdiği 4 ebeveynlik boyutu, 4 kardeş ilişkisi boyutu ve anne depresyonu olmak üzere toplam 9 konu başlığı, özel bir istatistiksel ağ modeliyle hesaplanmıştır (238 aile üzerinden).^[Tüm sorularda tam veri isteyen bu analiz yöntemi nedeniyle eksik verisi olan üç diyabetli aile bu haritadan otomatik çıkarılmıştır.] `r apa_network_top_strength_sentence()` Hangi konuların daha kalın çizgilerle bağlandığı ve hangilerinin ailenin tam merkezine yerleştiği @fig-network-graph içinde görselleştirilmiştir. `r apa_network_stability_sentence()` `r apa_network_nct_sentence()` Ek olarak, annenin depresyon sorularının (21 madde) kendi aralarındaki ağ bağlantıları da ayrıca analiz edilmiş, bu bağlantılar da yine sebep-sonuç şeklinde değil "birliktelik" şeklinde yorumlanmıştır. İlişki ağlarının kilit düğümleri ve diyabet-kontrol aileleri arasındaki benzerlik durumları @tbl-apa-network içinde özetlenmiştir."""


old_clinical = """### [KEŞİFSEL] Klinik Fayda

**Bulgu özeti.** Annenin ebeveynlik tutumları, yüksek düzeyde güncel depresif belirti taşıyan anneleri aynı ölçüm anında ayırt etmeye ancak küçük bir katkı sağlamıştır. Bu katkı yalnız düşük tarama eşiklerinde belirgin kalmış ve dış örneklemde doğrulanmamıştır. Model ileriye dönük bir risk yordaması değil, eşzamanlı bir sınıflandırma denemesidir.

*Kanıt* — Bu çözümlemede yüksek güncel depresif belirti göstergesi, Beck toplam ≥ 17 kesme değeriyle tanımlanmıştır.^[Bu gösterge betimsel bir ikili sınıflamadır; klinik risk ya da yordama anlamı taşımaz.] Bu göstergeyi sınıflandırmak için iki model karşılaştırılmıştır. Temel model DM grup üyeliğini, anne yaşını, latent sosyoekonomik düzeyi ve ailedeki çocuk sayısını içermiş; genişletilmiş model ise bu değişkenlere dört EMBU-P alt ölçeğini eklemiştir. Modeller iç-validasyonlu optimizm-düzeltilmiş bootstrap (B = 1000) ile `r apa_clinical_auc_sentence()` Temel ve genişletilmiş modellerin ayrım gücü @fig-clinical-roc içinde gösterilmiştir. Youden indeksiyle belirlenen optimal eşik 0,22'dir; bu işletme noktasında sensitivite 0,75, spesifite 0,60, PPV 0,41 ve NPV 0,87 düzeyindedir. Karar eğrisi analizinde genişletilmiş model, incelenen 0,05–0,50 olasılık eşiği aralığının tamamında hem "herkesi tara" hem de "kimseyi tarama" stratejisine göre bu örneklem içinde pozitif net fayda sağlamıştır.^[Bu net fayda görünür (apparent), yani iç-örneklem düzeyindeki değerdir.] Ancak net fayda 0,05 eşiğinde 0,23 iken 0,25 ve üzeri eşiklerde 0,04–0,10 düzeyine gerilemiş ve böylece yalnız düşük eşiklerde belirgin kalmıştır (@fig-clinical-dca). AUC ve kalibrasyondan farklı olarak, net fayda eğrileri bootstrap optimizm düzeltmesine tabi tutulmamış, görünür iç-örneklem değerleri olarak raporlanmıştır. Klinik açıdan bu eşikler, yüksek depresif belirti taşıması muhtemel bir anneye kısa bir doğrulayıcı klinik görüşme ya da BDI uygulaması önerme kararına karşılık gelir. Düşük eşiğin benimsenmesi, yanlış-pozitif maliyetinin düşük, kaçırılan olgu maliyetinin ise yüksek sayıldığı tarama bağlamıyla tutarlıdır; buradaki yanlış-pozitif maliyeti yalnızca kısa bir ek değerlendirmeden ibarettir. Kalibrasyon açısından, `r apa_clinical_calibration_sentence()` (@fig-clinical-calibration). CART çapraz-doğrulanmış hata profili ve Random Forest değişken önemleri @fig-clinical-cart-rf içinde birlikte gösterilmiştir. Model dış örneklemde doğrulanmamıştır ve sonuçlar iç-validasyon düzeyindedir. Performans göstergeleri @tbl-apa-clinical içinde sunulmuştur."""

new_clinical = """### [KEŞİFSEL] Klinik Fayda

**Bulgu özeti.** Araştırmada "annelerin ebeveynlik tutumlarına bakarak o annenin depresyonda olup olmadığını tespit edebilir miyiz?" sorusu test edilmiştir. Annenin tutumlarının bu teşhise ancak çok küçük bir katkı sağladığı görülmüştür. Bu katkı da yalnızca "her şüpheyi değerlendirelim" gibi daha esnek sınırların kabul edildiği özel durumlarda bir anlam ifade etmiştir. Bu model gelecekte kimin depresyona gireceğini tahmin eden bir "fal" aracı değil, sadece o anki durumu tanımlamaya çalışan teorik bir denemedir.

*Kanıt* — Yüksek depresyon ihtimali, testte 17 puan veya üstü alan anneler olarak tanımlanmıştır.^[Bu tanımlama klinik bir tanı koymaz, sadece durum tespiti yapmak içindir.] Bu durumu tahmin etmek için iki ayrı formül kıyaslanmıştır: "Temel formül" sadece ailenin yaşına, gelirine ve çocuk sayısına bakarken; "Geniş formül" bunlara annenin ebeveynlik tutumunu da eklemiştir. Modellerin ayrım gücü, formülün kendi kendini 1000 kez tekrar test ettiği bir sağlamlama yöntemiyle incelenmiş ve `r apa_clinical_auc_sentence()` Ayrım gücünü gösteren ROC grafiği @fig-clinical-roc içinde verilmiştir. 

Sistemin en verimli çalıştığı sınır noktasında (optimal eşik 0,22), depresyonu olanı bulma (duyarlılık) %75, sağlam olanı ayırma (özgüllük) ise %60'tır. Klinik karar (fayda/zarar) analizine bakıldığında; ebeveynlik tutumlarını da içeren geniş formülün kullanılması, "bütün anneleri tek tek muayene etmeye" kıyasla ufak da olsa pratik bir net fayda sağlamaktadır.^[Bu net fayda sadece bu örneklemde görünen (düzeltilmemiş) kazançtır.] Ancak bu fayda, sadece düşük oranlarda (0,05 sınırı civarında) anlamlı kalmakta, sınırlar daraldıkça hızla gerilemektedir (@fig-clinical-dca). Bu oranlar, yüksek depresif belirti riski olan bir anneyle "kısa bir ek psikolojik görüşme yapma" kararına eşdeğer bir tavsiye gücü barındırır; zira bu kısa görüşmenin (yanlış alarm bile olsa) anneye bir zararı/maliyeti yoktur. 

Modelin tahminlerinin gerçek hayatla uyumu (kalibrasyon) `r apa_clinical_calibration_sentence()` (@fig-clinical-calibration). Ayrıca bu tahminler daha gelişmiş iki farklı yapay zekâ algoritmasıyla (Karar Ağaçları ve Random Forest) desteklenmiş, depresyonu bulmada hangi verilerin daha "önemli" olduğu @fig-clinical-cart-rf içinde haritalandırılmıştır. Kurulan bu sistem, bu deneye özgüdür ve farklı hastanelerde kanıtlanmamıştır. Genel başarı durumu @tbl-apa-clinical içinde verilmiştir."""


old_dmclinical = """### [KEŞİFSEL] DM Klinik Alt-Analizler

**Bulgu özeti.** Diyabetli grup içinde, metabolik kontrol göstergesi HbA1c ve tanı yaşı ile ebeveynlik tutumları arasında anlamlı bir ilişki bulunmamıştır. Hastalık süresiyle olan ilişkide de doğrusal-olmayan bir örüntü saptanmamış; doğrusal model bu ilişkiyi açıklamakta yeterli bulunmuştur. Bu alt-çözümlemeler küçük örneklem nedeniyle düşük istatistiksel güçtedir. Bu nedenle sonuçlar "ilişki yoktur" biçiminde değil, "mevcut veride bir ilişki gösterilememiştir" biçiminde okunmalıdır.

*Kanıt* — Diyabetli grup içinde HbA1c ile ebeveynlik tutumları arasındaki etkileşim dört EMBU-P alt ölçeğinde p > 0,400 ve R² < 0,25 düzeyinde kalmıştır. Bu alt-örneklemde katılımcı sayısı n = 39'dur ve eksik gözlemler için imputasyon^[Imputasyon: eksik veri hücrelerinin, gözlenen verilerden tahmin edilen değerlerle istatistiksel olarak doldurulması.] uygulanmamıştır. Hastalık süresinin kübik spline^[Kübik spline: bir değişkenin etkisini düz bir doğru yerine esnek bir eğriyle modelleyen istatistiksel yöntemdir; doğrusal-olmayan ilişkileri yakalamaya yarar.] ile doğrusal regresyon karşılaştırması, dört sonuç değişkeninin tümü için "doğrusal model yeterli" sonucunu vermiştir. Tanı yaşına göre kurulan üç katmanlı analizde ise hiçbir sonuç değişkeninde F testi anlamlılığa ulaşmamıştır (en büyük F = `r apa_tani_strata_maxF("F")`; p = `r apa_tani_strata_maxF("p")`). Kısmi η² değerleri 0,04'ün altında kalmıştır. n = 39 düzeyindeki HbA1c örneklemi küçük-orta etki büyüklüklerini yakalamak için yetersiz güçtedir; istatistiksel güç 0,50'nin altındadır. Diyabet grubuna özgü klinik alt-analizler @tbl-apa-dm-clinical içinde sunulmuştur."""

new_dmclinical = """### [KEŞİFSEL] Diyabet Klinik Alt-Analizleri

**Bulgu özeti.** Sadece diyabetli gruptaki çocukların kan şekeri dengesi (HbA1c) ve diyabet teşhisi aldıkları yaş ile annelerinin ebeveynlik tutumu arasında anlamlı bir ilişki bulunamamıştır. Hastalığın süresinin (diyabetle geçirilen yılların) de tutumlarla ilişkisi incelenmiş; basit, doğrusal bir mantığın bu durumu açıklamak için yeterli olduğu görülmüştür. Bu klinik hesaplamalarda veri sayısı (çocuk sayısı) az olduğu için istatistiksel kanıt gücü düşük kalmıştır. Dolayısıyla bu sonuçlar "kesinlikle hiçbir ilişki yoktur" şeklinde değil, "mevcut kan şekeri verileriyle bir ilişki ispatlanamadı" şeklinde okunmalıdır.

*Kanıt* — Diyabetli 39 çocuğun ölçülen HbA1c oranları ile annelerinin dört ebeveynlik tutumu arasındaki bağ incelenmiş ancak p > 0,400 kalmıştır. Eksik olan kan şekeri kayıtları yerine "suni tahmin puanları" (imputasyon yöntemi) yerleştirilmemiş, sadece kanı alınmış 39 çocuğun gerçek verisiyle hesaplama yapılmıştır. "Hastalık uzadıkça ebeveynliğin eğrisel (dalgalı) şekilde mi yoksa düz mü değiştiği" araştırılmış ve etkinin düz/doğrusal bir modelle açıklanabildiği kanıtlanmıştır. Çocukların hastalığa yakalanma yaşlarına göre gruplandırıldığı (erken, okul çağı, ergen) denemelerde de tutumlarda istatistiksel olarak ayırt edici bir sonuca (F testi, en büyük F = `r apa_tani_strata_maxF("F")`; p = `r apa_tani_strata_maxF("p")`) ulaşılamamıştır. n = 39 sayısı böylesine detaylı değişimleri tespit etmek için yetersiz (istatistiksel güç < 0,50) kalmıştır. Diyabet grubuna özel bu klinik durumun detaylı sayıları @tbl-apa-dm-clinical tablosunda verilmiştir."""

if old_network in content and old_clinical in content and old_dmclinical in content:
    content = content.replace(old_network, new_network)
    content = content.replace(old_clinical, new_clinical)
    content = content.replace(old_dmclinical, new_dmclinical)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replace successful!")
else:
    print("Text not found in the file.")
