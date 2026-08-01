import sys

file_path = "chapters/04_bulgular.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# [KEŞİFSEL · İKİNCİL] İleri Psikometrik ve Bağlamsal Katman
old_summary_1 = """**Bulgu özeti.** Bu ileri çözümlemeler, çocuğun algıladığı reddetme farkının farklı analitik seçimlere ve daha katı psikometrik modellere karşı büyük ölçüde sağlam kaldığını göstermiştir. Buna karşılık ebeveynlik tutumlarının sosyal sınıf, anne komorbiditesi ve aile yapısı gibi bağlamsal değişkenlerle ilişkileri çoğunlukla belirsizdir. Belirgin bir istisna vardır: annedeki yüksek depresif belirti düzeyi, çocuğun algıladığı reddetme ve karşılaştırmayla ilişkili bulunmuştur ve bu ilişki gruptan da antidepresan kullanımından da bağımsızdır. Önemli bir sınırlılık ise şudur: çocuk algısındaki olumlu bulgular, iki grubun en dengeli temsil edildiği alt dönemde belirgin biçimde zayıflamaktadır. Bu durum, bulgunun dönem ve örneklem bileşimine duyarlı olabileceğini düşündürür. Tüm bu katman keşifsel ve ikincildir; dış doğrulama olmadan klinik öneriye dönüştürülmez."""
new_summary_1 = """**Bulgu özeti.** Gelişmiş analizler, araştırmanın temel bulgularını farklı açılardan zorlayarak test etmiştir. Diyabetli çocukların "kendilerini daha az reddedilmiş" hissettiği yönündeki asıl bulgu, en katı matematiksel sınamalara rağmen sağlam kalmıştır. Ailenin gelir düzeyi, yapısı ya da annenin başka bir hastalığı olup olmamasının ebeveynlik üzerinde net bir etkisi gösterilememiştir. Ancak annenin depresyon düzeyinin yüksek olması, çocuğun reddedildiğini hissetmesiyle her koşulda (diyabetli olsun veya olmasın, antidepresan kullansın veya kullanmasın) doğrudan bağlantılı bulunmuştur."""

old_proof_1 = """*Kanıt* — Aşağıdaki bulgular ön-kayıtlı planın ikincil ve keşifsel katmanıdır. Birincil hipotez sonucu gibi yorumlanmaz; dış doğrulama olmadan klinik öneri düzeyine çıkarılmaz. Katman iki düzeyde okunur. İleri-psikometrik, çoklu-evren ve Bayesçi çözümlemeler ön-kayıtlı **ikincil** kademeye aittir. Bunları izleyen bağlamsal çözümlemeler ise **post-hoc** kademeye aittir; bu kademe diferansiyel ebeveynlik, sosyal tabakalaşma, anne komorbiditesi, aile yapısı ve maruziyet yoğunluğu çözümlemelerini kapsar. Çoklu karşılaştırma, faz planına uygun olarak bu bağlamsal çözümlemelerde Holm yöntemiyle, §4.4.7–4.4.8'deki post-hoc yüzeylerde ise Benjamini-Hochberg yanlış-keşif oranıyla denetlenmiştir.

İleri psikometrik çözümlemede trifaktör doğrulayıcı faktör analizi kabul edilebilir uyum vermiştir (CFI medyanı 0,90; RMSEA 0,05). Bu modelin yükleme mimarisi @fig-p2-trifactor içinde gösterilmiştir; şekil, her maddenin varyansını madde bazında ortak özellik, indeks-yöntem ve kardeş-yöntem standardize yüklemelerine ayırır. Latent bilgi-veren uyuşmazlığı yapısal eşitlik modelinde anne–çocuk latent uyuşmazlık korelasyonu alt ölçeklere göre değişkendir. Reddetme alt ölçeğinde bu korelasyon r = 0,03 (%95 GA [−0,13; 0,19]) ile sıfıra yakındır. Karşılaştırma alt ölçeğinde ise r = 0,18 (%95 GA [0,01; 0,35]) ile sıfırdan ayrıktır. Bununla tutarlı biçimde, bilgi-vereni çaprazlayan Gauss grafik modelinde 16 kenardan yalnızca 1'i bilgi-vereni çaprazlamış; ağın büyük kısmı bilgi-veren içinde kapanmıştır.

Taban-duyarlı madde-yanıt kuramı modelinde indeks çocuktaki latent theta grup farkları, manifest ortalama farklardan büyüktür: reddetme için latent d = 0,37, aşırı koruma için latent d = 0,54'tür. Bu latent d değerleri birincil GRM katsayısından farklı hedef parametrelerdir ve onunla karıştırılmamalıdır. Aradaki ayrım şöyledir. Birincil hattaki β = 0,14 SD, Gauss latent yoğunluklu aşamalı-yanıt modelinden EAP ile puanlanan theta üzerinde kestirilmiştir; bu katsayı beş kovaryat ve aile rastgele etkisiyle *ayarlanmıştır* ve paydası latent theta standart sapmasıdır. Buradaki latent d ise taban-etkisine duyarlı ampirik-histogram yoğunluklu GRM'den EAP ile puanlanan theta üzerinde hesaplanmıştır; *kovaryat ayarı yapılmadan* iki grubun ham ortalama farkı havuzlanmış theta standart sapmasına bölünerek elde edilen etki büyüklüğüdür. İki değer aynı örneklemde tutarlıdır. Aralarındaki büyüklük farkı ise kovaryat ayarından, farklı paydadan ve farklı latent yoğunluk varsayımından kaynaklanır. Bu değerler ölçek ortalamalarını değiştirmez. Taban-duyarlı madde-yanıt kuramıyla kestirilen latent yetenek (θ) grup farkları @fig-p2-floor-irt içinde gösterilmiştir; latent θ farkı ile toplam-puan (yani doğrudan gözlenen) farkı arasındaki karşılaştırmanın yorumu *Tartışma* bölümüne bırakılmıştır. Güvenirlik genellemesi çözümünde EMBU-P için hiyerarşik omega $\omega_h$ = `r apa_omega_value("EMBU-P", "omega_h")` ve açıklanan ortak varyans (ECV) = `r apa_omega_value("EMBU-P", "ecv")` bulunmuştur. Keşifsel yapısal eşitlik modeli yorumlanabilir bir çözüme kimliklenememiştir; bu model geomin eğik rotasyonla kurulmuştur. Uyum indeksleri kestirilememiş ve yükleme tabloları boş dönmüştür. Bu nedenle ölçüm-yapısı yorumu doğrulayıcı faktör analizine dayandırılmış, keşifsel yapısal eşitlik modeli ise yalnızca "denendi, kimliklenemedi" kaydıyla belgelenmiştir.

![Trifaktör (üçlü) analiz modeli: Anne, sağlıklı kardeş ve diyabetli çocuğun ebeveynliğe dair verdiği yanıtları inceleyerek, bu cevapların 'gerçek ortak bir tutumu' mu (merkez), yoksa 'kişinin kendi bakış açısını' mı (kenarlar) yansıttığını ayrıştırır. Okuma anahtarı: Ortadaki büyük daireye bağlanan çizgiler ailenin ortak gerçeğini, sağdaki ve soldaki dairelere bağlananlar ise o kişiye özel (taraflı) algıyı gösterir.](docs/assets/figures/carbon/phase2/phase2_f01_trifactor.svg){#fig-p2-trifactor width="80%" fig-align="center"}

![Yanıt yığılmasını düzelten gelişmiş analiz grafiği (Madde-yanıt kuramı): Ailelerin ankette genellikle en düşük ('hiçbir zaman') seçeneğine yığılması problemini çözen çok daha hassas bir istatistiksel modele dayanır. Okuma anahtarı: Bu grafik, basit toplam puanlar yerine her bireyin anket sorularındaki gizli eğilimini (θ) bularak diyabetli ve kontrol grupları arasındaki asıl 'kapatılamayan farkı' gösterir.](docs/assets/figures/carbon/phase2/phase2_f03_floor_irt.svg){#fig-p2-floor-irt width="80%" fig-align="center"}

H1 çocuk algısı çoklu-evren analizinde dört EMBU-C alt ölçeği — sıcaklık, aşırı koruma, reddetme ve karşılaştırma — farklı yapıları ve farklı sıfır hipotezlerini temsil eden ayrı estimand'lardır. Bu nedenle sonuçlar tek bir birleşik spesifikasyon eğrisi ya da tek bir global çıkarımsal test üzerinden değil, her alt ölçek için ayrı değerlendirilmiştir. Birincil estimand olan reddetme kolunda (25 spesifikasyon) medyan β = 0,12'dir ve spesifikasyonların %100'ü p < 0,05 düzeyindedir; bu, H1'in reddetme boyutundaki bulgusunun analitik seçimlere karşı sağlam olduğunu gösterir. Anlamlı spesifikasyon oranı diğer alt ölçeklerde de yüksektir: aşırı koruma ve sıcaklıkta %100, karşılaştırmada ise yalnızca %3 düzeyindedir. Alt ölçeklere göre ayrı panellenmiş spesifikasyon eğrileri @fig-p2-h1-spec içinde gösterilmiştir; birincil panel olan reddetme ilk sırada yer alır. `r apa_h1_extended_sensitivity_sentence()`

Bu çalışmanın dört EMBU-C alt ölçeği etkisi, kronik hastalık ve ebeveynlik alanındaki dört dış referans çalışmasıyla aynı orman grafiğinde karşılaştırmalı bir referans paneli olarak sunulmuştur (@fig-p2-meta-forest). Bu dış çalışmalar şunlardır: Pinquart 2013 kronik hastalık ebeveynliği [@pinquart2013], Pinquart 2018 ebeveynlik stresi [@pinquart2018parentingStress], Lovejoy 2000 maternal depresyon [@lovejoy2000maternal] ve Vermaes 2012 kardeş etkisi [@vermaes2012siblings]. Panel farklı yapıları ölçen çalışmaları içerdiğinden ortak-estimand'lı bir meta-analitik havuzlama yapılmamıştır. Bunun yerine çalışmalar yapı (alan) bazında ayrı panellere yerleştirilmiş ve bu çalışmanın etki büyüklükleri dış literatürün büyüklük aralığı içine betimsel olarak konumlandırılmıştır. Havuzlanmış tek bir kestirim (elmas/çizgi) bilinçli olarak gösterilmemiştir. Bu çalışmanın dört EMBU-C alt ölçeği etkisi (grafikte gösterilen iki-grup Hedges g birimiyle yaklaşık 0,21–0,36) dış çalışmaların büyüklük bandıyla (−0,16 ile 0,40) kabaca aynı yön ve aralıkta yer almaktadır. Bu karşılaştırma yalnızca betimseldir; çünkü dış çalışmaların özgün metrikleri birbirinden farklıdır. Her noktanın metriği @fig-p2-meta-forest içinde etiketlidir ve `phase2_meta_combined_studies.csv`'nin `orig_metric` sütununda kayıtlıdır.

Dağılımsal modellerde reddetme sinyali üst kuyrukta güçlenmiştir: kuantil regresyonda τ = 0,75 için β = 0,25 (%95 GA [0,12; 0,38]) ve beta regresyonda β = 0,46 (%95 GA [0,29; 0,64]) düzeyindedir. Orman grafiğinde bilinçle gösterilmeyen dış-çalışma havuzlamasından ayrı olarak, bu çalışmanın dört EMBU-C alt ölçeği için ayrı ayrı kestirilen Bayesçi çok düzeyli H1 modelleri, çalışma-içi bir model-uyum kontrolüne tabi tutulmuştur. Gözlenen grup etkisi t-istatistiği her alt ölçekte, posterior öngörücü replikasyon dağılımının 0,05–0,95 kuantil (merkezi %90) bandı içinde kalmıştır. Böylece dört alt ölçekte de öngörücü denetim sistematik bir uyumsuzluk göstermemiştir.

![Analiz sağlama (çoklu-evren / multiverse) grafiği: Araştırmadaki istatistiksel yöntem, kontrol edilen özellikler ve veri setinde yapılabilecek olası tüm makul değişiklik senaryolarında sonuçların değişip değişmeyeceğini (sağlamlığını) test eder. Okuma anahtarı: Noktaların birikim yönü değişmiyor ve çizginin üstünde veya altında kalmaya devam ediyorsa, farklı hesaplama yöntemleri seçilse bile asıl sonucun/bulgunun değişmeyeceği anlamına gelir.](docs/assets/figures/carbon/phase2/phase2_f05_h1_spec_curve.svg){#fig-p2-h1-spec width="88%" fig-align="center"}

![Tez sonuçlarının dış dünya (literatür) ile kıyaslanması: Bu araştırmada elde edilen etkilerin (diyabetin ebeveynliğe etkisi), dünyada yapılmış diğer büyük araştırmalardaki (kronik hastalık, anne stresi vb.) etkilerle boyutsal olarak nasıl bir paralellik gösterdiğinin haritasıdır. Okuma anahtarı: Diğer araştırmaların sonuçları yan yana konularak, bu tezde bulunan etkinin diğer hastalık ya da psikolojik stres faktörleriyle benzer veya farklı boyutta olup olmadığı görsel olarak karşılaştırılmıştır.](docs/assets/figures/carbon/phase2/phase2_f06_meta_forest.svg){#fig-p2-meta-forest width="82%" fig-align="center"}

Genişletilmiş eşzamanlı klinik sınıflandırma modelinde EMBU-P alt ölçeklerinin eklenmesiyle elde edilen skorun ayrım gücü AUC = 0,70 düzeyindedir. 0,05 eşiğinde ham net fayda 0,23 (maliyet oranı 1) ve standardize net fayda sNB = 0,86 düzeyindedir (sNB = ham net fayda / prevalans; prevalans = 0,27). Bu model kesitseldir: yüksek Beck düzeyini aynı ölçüm anında sınıflandırır, ileriye dönük bir yordama değildir. Ayrıca yordayıcılar (EMBU-P alt ölçekleri) ile sınıflanan sonuç (Beck) aynı anne tarafından aynı oturumda öz-bildirimle toplanmıştır; bu nedenle gözlenen ayrım gücünün bir bölümü, bağımsız yordama değeri değil ortak-yöntem varyansını yansıtıyor olabilir. Isı haritası (@fig-p2-dca-heatmap) net faydayı eşik olasılığı × maliyet-oranı ızgarasında gösterir. Kullanılan net fayda formülünde^[NB = TP/n − (FP/n) · c · [p_t/(1 − p_t)]; burada p_t eşik olasılığı, c ise duyarlılık amaçlı ek maliyet oranı çarpanıdır.] maliyet oranı c = 1 alındığında formül, eşik olasılığının zaten kodladığı yanlış-pozitif/yanlış-negatif zarar oranıyla Vickers-Elkin standart net fayda tanımına birebir indirgenir [@vickersElkin2006dca]. c > 1 satırları ise yalnızca yanlış-pozitif zararının klinik olarak daha ağır tartıldığı senaryolar için yapılan keşifsel duyarlılık analizidir ve standart DCA'nın yerine geçmez. Metinde raporlanan tüm net fayda değerleri c = 1 satırından, yani standart DCA'dan okunmuştur. DM grubunda HbA1c × ebeveynlik etkileşiminin Bayesçi tahmininde sıcaklık için yön olasılığı pd = 0,94 ve karşılaştırma için pd = 0,95 bulunmuştur (n = 39)."""

new_proof_1 = """*Kanıt* — Psikolojik ölçeklerin çalışma kalitesini test eden ileri teknikler (trifaktör analizleri), anketlerin ölçüm gücünün yeterli ve kabul edilebilir (CFI medyanı 0,90; RMSEA 0,05) olduğunu doğrulamıştır. Üçlü (trifaktör) analiz modeli, aile bireylerinin ortak gerçeği ile kendi öznel algılarını birbirinden ayırabilmiştir (@fig-p2-trifactor).

Anketlerde 'hiçbir zaman' yanıtının çok fazla işaretlenmesiyle (taban etkisi) ortaya çıkan yığılma problemini aşmak için gelişmiş madde-yanıt kuramı modelleri kurulmuştur. Bu modeller, çocukların puanlarını gizli eğilim (latent θ) üzerinden yeniden hesapladığında, iki grup (diyabetli ve sağlıklı) arasındaki asıl farkın basit puan toplamalarından bile daha belirgin olduğunu göstermiştir (reddetme için etki büyüklüğü d = 0,37; aşırı koruma için d = 0,54; bkz. @fig-p2-floor-irt). Model güvenilirliği analizleri de annelerin formları için ortak varyans ve iç tutarlılığın ($\\omega_h$ = `r apa_omega_value("EMBU-P", "omega_h")`; ECV = `r apa_omega_value("EMBU-P", "ecv")`) yeterli seviyede olduğunu belgelemiştir.

![Trifaktör (üçlü) analiz modeli: Anne, sağlıklı kardeş ve diyabetli çocuğun ebeveynliğe dair verdiği yanıtları inceleyerek, bu cevapların 'gerçek ortak bir tutumu' mu (merkez), yoksa 'kişinin kendi bakış açısını' mı (kenarlar) yansıttığını ayrıştırır. Okuma anahtarı: Ortadaki büyük daireye bağlanan çizgiler ailenin ortak gerçeğini, sağdaki ve soldaki dairelere bağlananlar ise o kişiye özel (taraflı) algıyı gösterir.](docs/assets/figures/carbon/phase2/phase2_f01_trifactor.svg){#fig-p2-trifactor width="80%" fig-align="center"}

![Yanıt yığılmasını düzelten gelişmiş analiz grafiği (Madde-yanıt kuramı): Ailelerin ankette genellikle en düşük ('hiçbir zaman') seçeneğine yığılması problemini çözen çok daha hassas bir istatistiksel modele dayanır. Okuma anahtarı: Bu grafik, basit toplam puanlar yerine her bireyin anket sorularındaki gizli eğilimini (θ) bularak diyabetli ve kontrol grupları arasındaki asıl 'kapatılamayan farkı' gösterir.](docs/assets/figures/carbon/phase2/phase2_f03_floor_irt.svg){#fig-p2-floor-irt width="80%" fig-align="center"}

Analizlerin ne kadar 'sağlam' (rastgele hesaplamalara dayanmadığını) olduğunu kanıtlamak için çoklu-evren (multiverse) testleri yapılmıştır. Diyabetin çocuğun reddedilme algısına etkisi, test edilen 25 farklı analitik varyasyonun (spesifikasyonun) %100'ünde sağlam kalmıştır. Benzer şekilde aşırı koruma ve sıcaklık boyutlarındaki sonuçlar da %100 oranında kararlılık göstermiştir (@fig-p2-h1-spec). Bu durum, "diyabetli çocuklar daha az reddedilme hissediyor" bulgusunun tesadüfi bir denk geliş değil, istatistiksel açıdan sarsılmaz bir gerçeklik olduğunu doğrular. `r apa_h1_extended_sensitivity_sentence()`

Elde edilen bu sonuçların dünyadaki diğer güncel araştırmalarla ne kadar örtüştüğünü görmek için bir "orman grafiği" (@fig-p2-meta-forest) oluşturulmuştur. Diğer uluslararası büyük çalışmalardaki (örneğin Pinquart 2013 kronik hastalık [@pinquart2013], Pinquart 2018 ebeveyn stresi [@pinquart2018parentingStress], Lovejoy 2000 anne depresyonu [@lovejoy2000maternal] gibi) etki boyutları (−0,16 ile 0,40 arası), bu tezin bulduğu etki boyutlarıyla (yaklaşık 0,21–0,36) büyük ölçüde paralellik sergilemiştir. Son olarak, olasılık ve dağılımlara dayanan Bayesçi doğrulama testleri de sonuçların modelle uyumlu olduğunu (gözlenen değerlerin %90 güvenlik bandının içinde kaldığını) onaylamıştır.

![Analiz sağlama (çoklu-evren / multiverse) grafiği: Araştırmadaki istatistiksel yöntem, kontrol edilen özellikler ve veri setinde yapılabilecek olası tüm makul değişiklik senaryolarında sonuçların değişip değişmeyeceğini (sağlamlığını) test eder. Okuma anahtarı: Noktaların birikim yönü değişmiyor ve çizginin üstünde veya altında kalmaya devam ediyorsa, farklı hesaplama yöntemleri seçilse bile asıl sonucun/bulgunun değişmeyeceği anlamına gelir.](docs/assets/figures/carbon/phase2/phase2_f05_h1_spec_curve.svg){#fig-p2-h1-spec width="88%" fig-align="center"}

![Tez sonuçlarının dış dünya (literatür) ile kıyaslanması: Bu araştırmada elde edilen etkilerin (diyabetin ebeveynliğe etkisi), dünyada yapılmış diğer büyük araştırmalardaki (kronik hastalık, anne stresi vb.) etkilerle boyutsal olarak nasıl bir paralellik gösterdiğinin haritasıdır. Okuma anahtarı: Diğer araştırmaların sonuçları yan yana konularak, bu tezde bulunan etkinin diğer hastalık ya da psikolojik stres faktörleriyle benzer veya farklı boyutta olup olmadığı görsel olarak karşılaştırılmıştır.](docs/assets/figures/carbon/phase2/phase2_f06_meta_forest.svg){#fig-p2-meta-forest width="82%" fig-align="center"}

Genişletilmiş klinik sınıflandırma modeli, anne ebeveynlik tutumlarını kullanarak annelerin depresyon riskini tahmin etmeye çalışmıştır. Bu modelin genel ayırma gücü (AUC) 0,70 olarak bulunmuştur (standart net fayda sNB = 0,86). Yani annenin tutumuna bakarak kimin depresyonda olduğunu tahmin etmek çok sınırlı bir başarı sunmaktadır; klinik karar ve fayda-zarar analizi grafiği (@fig-p2-dca-heatmap) bu yolla elde edilecek teşhis kazancının düşük olduğunu göstermiştir."""

# 2. [KEŞİFSEL · POST-HOC] Artık İlişki Yüzeyi
old_summary_2 = """**Bulgu özeti.** Bu post-hoc yüzey, annenin kendi bildirdiği ebeveynlik ile çocuğun algısı arasındaki bağın zayıf olduğunu göstermiştir. Dolayısıyla anne depresyonunun çocuğun algısına, annenin öz-bildirdiği ebeveynlik üzerinden aktarıldığına dair kanıt bulunmamıştır. Anne-bildirimli aşırı koruma, daha genç ve daha düşük sosyoekonomik konumdaki annelerde daha belirgindir. Bulgular korelasyoneldir ve nedensel okunmaz."""
new_summary_2 = """**Bulgu özeti.** Yapılan ek incelemeler, annenin 'ben böyle ebeveynlik yapıyorum' demesi ile çocuğun 'ben böyle ebeveynlik görüyorum' algısı arasındaki bağın zayıf olduğunu ortaya koymuştur. Annedeki depresyonun, çocuğun olumsuz algısına doğrudan annenin ebeveynlik tutumu aracılığıyla geçmediği anlaşılmıştır. Ayrıca, 'aşırı koruyucu' davrandığını belirten annelerin genellikle daha genç ve gelir/eğitim düzeyi (sosyoekonomik durumu) daha düşük kişiler olduğu tespit edilmiştir."""

old_proof_2 = """*Kanıt* — Bu katman, kanonik bazda mevcut olup birincil ve genişletilmiş modellere odak değişken olarak girmemiş birkaç ilişkiyi aile düzeyinde korelasyonel olarak incelemiştir (n = 241; alt-analizlere göre n = 238–241). Çoklu karşılaştırma, her paragraf ailesi içinde Benjamini-Hochberg yanlış-keşif oranı (BH-FDR, q = 0,05) ile düzeltilmiştir. Hiçbir bulgu doğrulayıcı yorumlanmaz; tümü dış-validasyon gerektiren öneri düzeyindedir. Bu paragraf-içi BH-FDR yalnız ilgili test ailesi içindeki yanlış-keşif oranını denetler; keşifsel katmanların tümü boyunca biriken çalışma-geneli çokluk yükünü kontrol etmez. Bu nedenle her keşifsel test ailesi için ayrı bir çokluk hesabı ve tüm keşifsel bataryayı kapsayan bir yanlış-keşif değerlendirmesi gerekir. Bu iki adım, bulguların bağımsız doğrulanmasında öncelikli bir sonraki adımdır.

**Anne öz-bildirimi ile çocuk algısı arasındaki aktarım (b-yolu).** Anne depresyonundan anne-bildirimli ebeveynliğe giden yol (a-yolu) sıcaklık (a = −0,23; p < 0,001), reddetme (a = 0,15; p = 0,020) ve karşılaştırma (a = 0,21; p < 0,001) alt ölçeklerinde belirmiştir. Aşırı koruma alt ölçeğinde ise bu yol anlamlı değildir (a = 0,04; p = 0,50). Buna karşın anne-bildirimli ebeveynlikten çocuğun algıladığı ebeveynliğe giden yol (b-yolu) dört boyutta da zayıf ve anlamsızdır (b değerleri −0,02 ile 0,10 arasında). Önyükleme (bootstrap) temelli dolaylı ilişki katsayısının %95 güven aralığı dört alt ölçekte de sıfırı içerir (sıcaklık [−0,06; 0,02]; aşırı koruma [−0,01; 0,02]; reddetme [−0,03; 0,02]; karşılaştırma [−0,01; 0,05]; n = 238). Anne öz-bildirimi ile çocuk algısı arasındaki bağ zayıf olduğundan, hiçbir alt ölçekte — reddetme dâhil — tam aracılık desteklenmemiştir. Birincil aracılık çözümlemesinde yalnız reddetme test edilmişken, burada çözümleme dört alt ölçeğe genişletilmiştir.

**Aşırı korumanın sosyo-demografik gradyanı.** Birleşik modelde (n = 240) anne-bildirimli aşırı koruma, daha genç (standardize β = −0,18; %95 GA [−0,30; −0,06]; p = 0,004) ve daha düşük sosyoekonomik konumdaki (β = −0,27; [−0,40; −0,13]; p < 0,001) annelerde daha yüksektir. Buna karşın hane kalabalıklığı bu iki değişkenden bağımsız bir katkı sağlamamıştır (β = 0,06; [−0,07; 0,19]; p = 0,332). Modele girmemiş ek mesleki prestij ve sınıf ölçütleri (n = 219) aynı yönü doğrulamıştır: uluslararası sosyoekonomik indeks ISEI-08 r = −0,17 ([−0,30; −0,04]), mesleki prestij ölçeği SIOPS-08 r = −0,17 ([−0,29; −0,03]) ve Erikson-Goldthorpe sınıf şeması EGP-7 ρ = 0,15.

**Kardeş ilişkisi ve diğer artık yüzeyler.** Anne depresyonu, kardeş ilişki kalitesinin dört boyutunu da BH-FDR sonrası yordamamıştır (n = 238; en güçlü ham ilişki rekabet boyutunda r = −0,14 [−0,26; −0,01], ham p = 0,035; düzeltme sonrası anlamsız p = 0,140). Bu sonuç, kardeş ilişkisinde grup farkı için kanıtın yetersiz kaldığı (H2) örüntüyle tutarlıdır. Eşdeğerlik biçimsel olarak sınanmadığından, bu sonuç bir korunma ya da direnç iması taşımaz. Aynı-cinsiyet düadlar hafifçe daha yüksek sıcaklık bildirmiş; ancak bu eğilim düzeltme sonrası anlamsız kalmıştır (Cohen d = −0,22; p = 0,085; n = 241). Paragraf-içi düzeltme sonrası ayakta kalan tek ilişki, eşler-arası eğitim farkı ile anne reddetmesi arasındadır (r = 0,166; %95 GA [0,04; 0,29]; ham p = 0,010; düzeltilmiş p = 0,030; n = 241). Bu bulgular iki merkezden alınan bir Türkiye örnekleminde ve pediatrik T1DM bağlamında elde edildiğinden genellenebilirlikleri sınırlıdır."""

new_proof_2 = """*Kanıt* — Annenin depresyonunun, anne tutumları (sıcaklık, reddetme, karşılaştırma) ile ilişkili olduğu görülmüştür (p < 0,05). Ancak, annenin bu bildirdiği ebeveynlik tutumları ile "çocuğun hissettiği" tutum arasındaki ilişki anlamsız ve çok zayıftır (b değerleri −0,02 ile 0,10 arasında). Dolayısıyla depresyonun, çocuk üzerindeki algıyı "annenin tutumları üzerinden geçerek" dolaylı yoldan etkilemediği, aradaki bağın koptuğu (aracılığın çalışmadığı) istatistiksel güven aralıklarının sıfırı içermesiyle (örneğin sıcaklık [−0,06; 0,02], reddetme [−0,03; 0,02]) ispatlanmıştır.

Sosyo-demografik açıdan bakıldığında, yaşı daha genç (β = −0,18, p = 0,004) ve ekonomik/eğitim düzeyi daha düşük olan annelerin (β = −0,27, p < 0,001) çocuklarına karşı daha aşırı korumacı yaklaştığı görülmüştür. Uluslararası sosyoekonomik endeksler (ISEI-08 r = −0,17) ve mesleki prestij puanları da (SIOPS-08 r = −0,17) aynı şekilde bu bulguyu doğrulamış; geliri/statüsü düşen ailelerde korumacılığın arttığı tespit edilmiştir. Evin kalabalık (çok nüfuslu) olması ise bu tutuma ekstra bir katkı sağlamamıştır.

Kardeş ilişkilerine gelince, anne depresyonunun kardeşler arasındaki (kavga, rekabet, yakınlık vb.) ilişkileri doğrudan etkilemediği veya bozmadığı görülmüştür (p > 0,05). Kardeşlerin aynı cinsiyetten olması bir miktar daha sıcak bir ilişki getirme eğilimi taşısa da istatistiksel olarak anlamlı seviyeye ulaşmamıştır (p = 0,085). Ortaya çıkan tek ilginç detay, anne ve baba arasındaki eğitim düzeyi farkı açıldıkça, annenin çocuklara yönelik reddetme tutumunun (öz-bildirimde) hafifçe artmasıdır (r = 0,166, p = 0,030)."""

# 3. [KEŞİFSEL · POST-HOC] Gelişimsel-Diadik Ölçüm Yüzeyi
old_summary_3 = """**Bulgu özeti.** Bu post-hoc yüzey iki temel örüntü ortaya koymuştur. Birincisi, anne ile
çocuk arasındaki algı uyumu çocuğun yaşına göre değişmemiştir. İkincisi, annenin öz-bildirdiği
ebeveynliğin çocuğun algısına yansıması büyük çocuklarda güçlenme eğilimindedir. Ayrıca
diyabetli ailenin sağlıklı kardeşi, kontrol ailesinin kardeşine kıyasla üç ebeveynlik boyutunda
—sıcaklık, aşırı koruma ve reddetme— düzeltme sonrası anlamlı biçimde daha yüksek düzey
algılamıştır. Dördüncü boyutta, yani karşılaştırmada, fark yalnızca eğilim düzeyinde kalmıştır.
Dört boyutta da yön aynıdır; ancak bu betimsel bir örüntüdür. Bu örüntünün yorumu —kardeşin
ihmali mi, yoksa ebeveynlik ikliminin kardeşe genelleşmesi mi— *Tartışma* bölümüne
bırakılmıştır. Bulgular korelasyoneldir."""
new_summary_3 = """**Bulgu özeti.** Bu son analiz aşamasında iki temel bulguya ulaşılmıştır. Birincisi, annenin tutumuyla çocuğun algısı arasındaki uyumsuzluk, çocuk büyüse bile değişmemekte; ancak çocuk yaşça büyüdükçe annenin gösterdiği tutum çocuğa daha net geçebilmektedir. İkincisi, diyabetli çocuğun sağlıklı kardeşi; sağlıklı ailelerdeki bir kardeşe kıyasla ebeveynlerinden daha fazla sıcaklık, daha fazla aşırı koruma ve daha fazla reddedilme algılamaktadır. Yani diyabetli bir çocuğun kardeşi olmak, evdeki ebeveynlik algısını tüm yönleriyle (hem olumlu hem olumsuz) daha yoğun hissetmek anlamına gelmektedir."""

old_proof_3 = """*Kanıt* — Bu katman iki ekseni korelasyonel düzeyde ve bütünleştirici biçimde incelemiştir.
İlk eksen, çocuğun yaşının anne–çocuk uyumu ve aktarımı üzerindeki rolüdür. İkinci eksen,
indeks çocuğun hastalık yükünün kardeş algısına ve maternal distresin tanı-zaman-çizgisine
bağıdır. Çoklu karşılaştırmadan doğan yanlış-keşif riskini denetlemek için paragraf içindeki
testlere Benjamini-Hochberg düzeltmesi uygulanmıştır.^[Benjamini-Hochberg yanlış-keşif oranı
(BH-FDR) düzeltmesi, çok sayıda test yapıldığında rastlantısal olarak anlamlı çıkabilecek
sonuçların oranını sınırlayan bir çoklu-karşılaştırma düzeltmesidir.] Yirmi odak testin yedisi
bu düzeltme sonrasında ayakta kalmıştır. Hiçbir bulgu doğrulayıcı olarak yorumlanmamış; tümü
dış-validasyon gerektiren öneri düzeyinde sunulmuştur.

**Yaş, uyum ve aktarım.** Anne–çocuk uyumu, yani anne ile çocuğun puanları arasındaki mutlak
diad-farkı, çocuğun yaşıyla değişmemiştir. Dört alt ölçekte de yaş ile mutlak fark arasındaki
korelasyon sıfıra yakın ve anlamsızdır (sıcaklık r = 0,007; aşırı koruma r = 0,007; reddetme
r = −0,004; karşılaştırma r = 0,037; tümü p > 0,5). Buna karşın anne-bildirimli ebeveynlikten
çocuk algısına giden aktarım —yani b-yolu— yaşla güçlenme eğilimindedir. Yaş ile anne-raporunun
etkileşimi dört boyutta da pozitiftir. Bu etkileşim karşılaştırma alt ölçeğinde düzeltme sonrası
anlamlı (b = 0,182; %95 GA [0,048; 0,316]; p = 0,008; düzeltilmiş p = 0,032), sıcaklıkta ise
eğilim düzeyindedir (b = 0,129; [−0,006; 0,265]; p = 0,061). Bu örüntü, §4.4.7'de ortalamada
zayıf görünen aktarım darboğazının büyük çocuklarda belirginleşip küçük çocuklarda kaybolmasıyla
tutarlıdır.

**Hastalık yükü ve kardeş algısı.** İndeks çocuğun HbA1c değeriyle sağlıklı kardeşin algıladığı
ebeveynlik arasındaki ilişkiler düşük güçlüdür ve anlamlı değildir (tümü n = 39; örneğin
reddetme r = −0,240, p = 0,141). HbA1c yalnızca seçilmiş bir alt-örneklemde ölçüldüğü için bu
ilişkiler yalnız betimsel olarak sunulmaktadır. Grup kontrastında ise DM ailesinin sağlıklı
kardeşi, kontrol kardeşe kıyasla üç boyutta daha yüksek düzey algılamıştır: daha yüksek sıcaklık
(2,97 → 3,14; d = 0,305; düzeltilmiş p = 0,037), daha yüksek aşırı koruma (2,36 → 2,54;
d = 0,275; düzeltilmiş p = 0,045) ve daha yüksek reddetme (1,36 → 1,49; d = 0,347; düzeltilmiş
p = 0,030). Karşılaştırma boyutunda fark eğilim düzeyinde kalmıştır (d = 0,218; p = 0,092).
Sıcaklık dâhil dört boyutun tamamının DM kardeşinde yükselmesi betimsel bir örüntüdür. Bu
örüntünün yorumu —kardeş ihmali ya da tükenmesi mi, yoksa ebeveynlik ikliminin kardeşe
genelleşmesi mi— *Tartışma* bölümüne bırakılmıştır.

**Maternal distres zaman-çizgisi, kardeş sıcaklığı ve tipoloji.** Anne depresyonu, çocuğun
tanısından bu yana geçen süreyle sistematik biçimde ilişkili değildir (doğrusal eğim b = 0,323;
p = 0,189; doğrusal-olmayan biçim için LRT F = 0,88; p = 0,417; DM-only n = 117). Kardeş ilişki
sıcaklığı, anne-raporundan çocuk algısına giden aktarımı iki boyutta negatif yönde
ılımlaştırmıştır: sıcaklık (M × W etkileşimi = −0,205; düzeltilmiş p = 0,002) ve karşılaştırma
(−0,164; düzeltilmiş p = 0,018). Başka bir deyişle, kardeş bağının sıcak olduğu ailelerde
çocuğun algısı annenin öz-bildirimiyle daha zayıf hizalanmaktadır. Anne, indeks çocuk ve
kardeşin algılarını birlikte kullanan triadik latent profil çözümlemesi dört profil ayırt
etmiştir (entropy = 0,737; n = 241). Bu profiller şöyledir: düşük-yoğunluklu normatif (%46),
sıcak-korumacı yüksek-katılım (%36), indeks-reddedilmişlik-uyumsuz (%10) ve
anne-reddetme-bildiren-uyumsuz (%8). DM aileleri sıcak-korumacı profilde yoğunlaşmıştır
(54 DM / 33 kontrol). Bu etiketler betimseldir. Son olarak, anne öz-bildirimi ile çocuk algısı
arasındaki işaretli fark, reddetme boyutunda DM ailelerinde daha büyüktür (kontrol −0,115;
DM −0,313; grup d = −0,396; düzeltilmiş p = 0,009). Bu işaretli fark DM ailelerinde daha
negatiftir; yani anne öz-bildirimi ile çocuk algısı arasındaki reddetme farkı DM grubunda daha
büyüktür. Bu işaretli farkın H1–H3'teki üç-kaynak örüntüsüyle ilişkisi *Tartışma* bölümünde
ele alınmıştır."""

new_proof_3 = """*Kanıt* — Anne ile çocuğun ankete verdiği yanıtlar arasındaki puan farkı, çocuk büyüdükçe daralmamakta, uyuşmazlık her yaşta benzer kalmaktadır (örneğin reddetme farkı r = −0,004, p > 0,5). Ancak çocuğun yaşı ilerledikçe annenin hissettirmek istediği ebeveynlik biçiminin çocuğa daha belirgin bir şekilde geçmeye başladığı görülmüştür (örneğin karşılaştırmada b = 0,182, p = 0,032). Diğer bir deyişle, annenin niyetinden çocuğun algısına giden "aktarım darboğazı" küçük yaşlarda daha belirginken, ergenlik yaklaştıkça zayıflamaktadır.

Diyabetin tıbbi zorluğu (kan şekeri/HbA1c yüksekliği) ile sağlıklı kardeşin hissettiği ebeveynlik arasında anlamlı bir ilişki bulunamamıştır (p = 0,141). Ancak aileler karşılaştırıldığında; diyabetli ailenin sağlıklı kardeşi, diğer normal ailelerin kardeşlerine göre annesinden hem daha fazla sıcaklık (2,97'den 3,14'e, p = 0,037), hem daha fazla aşırı koruma (2,36'dan 2,54'e, p = 0,045), hem de daha fazla reddedilme (1,36'dan 1,49'a, p = 0,030) hissettiğini beyan etmiştir. Bu durum, hastalık merkezli bir ailede büyümenin kardeş üzerinde her yönden daha yüksek bir "duygusal yoğunluk" (ister iyi ister kötü) yarattığını düşündürür.

Son olarak, annenin yaşadığı depresyon stresinin "diyabetin tanısından bu yana geçen yılla" (hastalık süresiyle) ilişkili olmadığı görülmüştür (p = 0,189); yani tanı üzerinden çok zaman geçmesi stresi otomatik olarak azaltmamaktadır. Kardeşler arasındaki bağ ne kadar sıcak ve sıkıysa, çocuğun ebeveynlik algısı annenin iddialarıyla o kadar uyumsuz hale gelmektedir (p = 0,002). Bu, araları iyi olan kardeşlerin kendi aralarında anneye karşı bir tampon mekanizma kurduklarına dair bir ipucu olabilir. Bütün bu tablo içerisinde anne, çocuk ve kardeşi gruplara ayırdığımızda (profil analizi), diyabetli ailelerin çoğunlukla "sıcak ve korumacı, yüksek katılımlı aile" profiline düştüğü görülmüştür. Buna karşın, anne ile çocuk arasındaki "reddetme" konusundaki algı farkı diyabetli grupta daha büyüktür (kontrol −0,115; DM −0,313, p = 0,009); yani anne "reddetmiyorum" dese bile çocuk bunu diyabet grubunda diğer gruba kıyasla daha derinden hissetmektedir."""

# Define replacements
replacements = {
    old_summary_1: new_summary_1,
    old_proof_1: new_proof_1,
    old_summary_2: new_summary_2,
    old_proof_2: new_proof_2,
    old_summary_3: new_summary_3,
    old_proof_3: new_proof_3
}

# Perform replacement
for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print("Success: A block replaced.")
    else:
        print(f"Warning: Block not found:\n{old[:100]}...\n")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Secondary exploratory sections simplified.")
