import sys

file_path = "chapters/04_bulgular.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_mediation = """### [KEŞİFSEL] Aracılık

**Bulgu özeti.** Anne depresyonu ile çocuğun algıladığı reddetme arasındaki ilişki incelenmiştir. Bu ilişkinin, annenin kendi bildirdiği reddetme üzerinden geçen bir aracılık zinciriyle açıklandığına dair kanıt bulunmamıştır. Dolaylı etki her modelde belirsiz kalmıştır. Buna karşılık anne depresyonunun çocuğun reddetme algısıyla doğrudan ilişkisi tutarlı biçimde ortaya çıkmıştır. Kesitsel tasarım nedeniyle bu örüntü nedensel değil, betimsel olarak okunmalıdır.

*Kanıt* — Beck → EMBU-P reddetme → EMBU-C reddetme zinciri üç katmanda test edilmiştir. Tek-aracı modeli, güven aralıklarını yeniden örneklemeyle kestiren BCa bootstrap yöntemiyle ve n = 1000 yinelemeyle kurulmuştur.^[BCa (yanlılık düzeltilmiş ve hızlandırılmış) bootstrap, güven aralığını dağılımın yanlılığı ve çarpıklığı için düzelten bir yeniden örnekleme yöntemidir.] Bu modelde a-yolu anlamlı bulunmuştur: β = `r apa_mediation_value("Tek aracılı", "a (X→M)", "est")` (p = `r apa_mediation_value("Tek aracılı", "a (X→M)", "p")`). Buna karşılık b-yolu anlamsız kalmıştır: β = `r apa_mediation_value("Tek aracılı", "b (M→Y)", "est")` (p = `r apa_mediation_value("Tek aracılı", "b (M→Y)", "p")`). Dolaylı etki ise β = `r apa_mediation_value("Tek aracılı", "Dolaylı (a×b)", "est")` olarak hesaplanmış; bu etkinin %95 güven aralığı (`r apa_mediation_value("Tek aracılı", "Dolaylı (a×b)", "ci")`) sıfırı içermiştir.

Çok düzeyli modelde a-yolu yeniden anlamlı çıkmıştır (β = `r apa_mediation_value("Çok düzeyli aracılık", "a (X→M)", "est")`; p = `r apa_mediation_value("Çok düzeyli aracılık", "a (X→M)", "p")`). Dolaylı etki ise bu modelde de anlamsızdır. Koşullu süreç modelinde^[Hayes'in 14 numaralı şablon modeli; aracılık yolunun sonuç ayağının grup değişkeniyle etkileşime girip girmediğini sınar.] grup moderasyonu da (a3 = `r apa_mediation_value("Koşullu süreç", "a3", "est")`; p = `r apa_mediation_value("Koşullu süreç", "a3", "p")`) aracılı moderasyon indeksi de (IMM = `r apa_mediation_value("Koşullu süreç", "Aracılı moderasyon indeksi", "est")`; p = `r apa_mediation_value("Koşullu süreç", "Aracılı moderasyon indeksi", "p")`) anlamlı bulunmamıştır.

Imai-Keele-Tingley duyarlılık çözümlemesinde tüm sonuç değişkenlerinde kritik ρ < 0,05 düzeyinde kalmıştır. Bu nedenle dolaylı etki yerine `c'` ile gösterilen doğrudan etki değerlendirilmiştir. Reddetme yolunda üç modelin üçünde de (3/3) pozitif ve anlamlı bir doğrudan etki bulunmuştur. Aracılık sonuçları @tbl-apa-mediation içinde sunulmuştur."""

new_mediation = """### [KEŞİFSEL] Aracılık (Dolaylı Etki Modeli)

**Bulgu özeti.** Anne depresyonunun, çocuğun hissettiği "reddedilme" algısıyla olan ilişkisi incelenmiştir. Araştırmada "Acaba annenin depresyonu önce annenin kendi ebeveynlik tutumunu bozuyor, çocuk da bunu mu hissediyor?" şeklinde bir "aracı zincir" test edilmiş ancak bu zincirin çalışmadığı görülmüştür. Başka bir ifadeyle; annenin depresyonunun çocuğu etkilemesi, annenin bildirdiği "reddedici tutumu" üzerinden dolaylı olarak gerçekleşmemektedir. Buna karşılık, annenin depresyonu ile çocuğun "reddedildiğini" hissetmesi arasında dolaysız (doğrudan) bir bağlantı bulunmuştur. Bu veri belirli bir anın fotoğrafını çektiği için kesin bir "neden-sonuç" kuralı olarak değil, genel bir gözlem olarak okunmalıdır.

*Kanıt* — "Anne Depresyonu → Annenin Tutumu → Çocuğun Algısı" zincirleme modeli üç farklı yaklaşımla test edilmiştir. Temel modelde (1000 tekrarlı güven aralığı hesaplamasıyla), deprosonun annenin tutumunu etkilediği o ilk "köprü" anlamlı çıkmıştır: β = `r apa_mediation_value("Tek aracılı", "a (X→M)", "est")` (p = `r apa_mediation_value("Tek aracılı", "a (X→M)", "p")`). Ancak annenin tutumunun çocuğa geçişi olan ikinci köprü anlamsız kalmıştır: β = `r apa_mediation_value("Tek aracılı", "b (M→Y)", "est")` (p = `r apa_mediation_value("Tek aracılı", "b (M→Y)", "p")`). Bu iki köprünün birleşimi olan zincirleme (dolaylı) etki de sıfırdan farksız bulunmuştur: β = `r apa_mediation_value("Tek aracılı", "Dolaylı (a×b)", "est")` (`r apa_mediation_value("Tek aracılı", "Dolaylı (a×b)", "ci")`).

Aile içi katmanlı modellerde ve hastalığın durumuna göre yapılan analizlerde de zincirin çalışmadığı teyit edilmiştir. Zincirin kopuk olması nedeniyle "dolaylı etki" yerine doğrudan etkilere bakılmıştır. Her üç modelin tamamında (3/3), anne depresyonunun doğrudan çocuğun reddedilme hissini artırdığı (pozitif anlamlı etki) tespit edilmiştir. Tüm bu ilişki sonuçları @tbl-apa-mediation içinde özetlenmiştir."""

old_lpa = """### [KEŞİFSEL] Latent Profil ve Sınıf Analizi

**Bulgu özeti.** Anne depresyonu, ebeveynlik tutumları ve sosyoekonomik göstergeler gizli sınıf ve profillere ayrıldığında, diyabet tanısı bir sınıfa ait olma olasılığını belirgin biçimde değiştirmemiştir. Başka bir deyişle aileler, tanı grubuna göre birbirinden ayrı profil örüntülerine düşmemektedir.

*Kanıt* — Beck toplam puanı, dört EMBU-P alt ölçeği ve latent sosyoekonomik düzey göstergeleri üzerinde tidyLPA ile 1–5 profil karşılaştırması yürütülmüştür.^[Kestirimde mclust arka ucu; eşit varyanslı ve sıfır kovaryanslı bir model kullanılmıştır.] Bu kestirim, model-temelli hiyerarşik başlangıç ataması kullanır. Söz konusu atama deterministiktir; rastgele başlangıçlara bağlı yerel-maksimum riski taşımaz. Bu nedenle log-olabilirlik en iyi çözümde tektir. Kategorik göstergeli poLCA duyarlılık çözümlemesinde ise farklı bir yol izlenmiştir. Burada en iyi log-olabilirliğin tekrarlanabilir olması ve yerel-maksimumdan kaçınılması için sınıf başına 30 rastgele başlangıç uygulanmıştır (nrep = 30).
`r apa_lpa_selection_sentence()`
`r apa_lpa_profile_report_sentence()`
Kategorik göstergeli poLCA analizinde BIC, 2-sınıf çözümünü desteklemiştir (BIC = 2641,0; sınıf oranları %63,4 ve %36,6; entropy = 0,60). Modal sınıf regresyonunda DM grubu, sınıf üyeliğini anlamlı biçimde değiştirmemiştir (OR = 0,99; %95 GA [0,57; 1,71]; p = 0,962). Bifaktör S-1 modeli sınır altı uyum vermiştir; bu nedenle yalnızca keşifsel düzeyde raporlanmıştır. BIC, entropi ve BLRT p değerlerinin profil sayısına göre örüntüsünü gösteren model-seçim tanıları @fig-lpa-fit-indices içinde görselleştirilmiştir. Sayısal model-seçim tanıları ise @tbl-apa-lpa-bifactor içinde sunulmuştur."""

new_lpa = """### [KEŞİFSEL] Gizli Profil Ayırma Analizi (LPA)

**Bulgu özeti.** Aileler "annelerin depresyonu, ebeveynlik tutumları ve sosyoekonomik düzeylerine" göre kendi içinde doğal tiplere/profillere ayrıldığında; ailenin diyabetli olması bu gruplardan birine girmeyi tetikleyen özel bir unsur olarak öne çıkmamıştır. Başka bir ifadeyle, diyabetli ailelerin kendine has, farklı ve izole bir profil kalıbı yoktur.

*Kanıt* — Aileleri doğal gruplara ayırmak için 1'den 5'e kadar farklı gruplama denemesi (LPA) yapılmıştır. Yapılan bu matematiksel ayırma işleminde, aileleri rastgele ayırmak yerine en isabetli kümeyi bulan bir algoritma kullanılmıştır.
`r apa_lpa_selection_sentence()`
`r apa_lpa_profile_report_sentence()`
Alternatif bir kontrol sağlama algoritmasında veriler 2 ana profile ayrılmıştır (Sınıfların oranları %63,4'e %36,6). Yapılan geriye dönük kontrollerde, bir ailenin diyabet tanısına sahip olmasının, onu bu farklı profillerden birine (iyi veya kötü profiline) itmede hiçbir belirleyici (anlamlı) etkisinin olmadığı teyit edilmiştir (p = 0,962). Aileleri bu gizli profillere bölerken sistemin uyum ve başarı oranları @fig-lpa-fit-indices grafiğinde görselleştirilmiş, matematiksel detayları ise @tbl-apa-lpa-bifactor tablosunda verilmiştir."""

if old_mediation in content and old_lpa in content:
    content = content.replace(old_mediation, new_mediation)
    content = content.replace(old_lpa, new_lpa)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replace successful!")
else:
    print("Text not found in the file.")
