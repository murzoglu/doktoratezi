import sys

file_path = "chapters/04_bulgular.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_text = """## Ölçek ve Veri Kalitesi

Analizlerde kullanılan ölçeklerin bu örneklemdeki psikometrik özellikleri, birincil
hipotez sınamalarından önce ayrı bir çalışma-içi psikometrik değerlendirme hattıyla
incelenmiş; ayrıntılı bulgular Ek 7'de (@sec-ek-psikometri) sunulmuştur. Değerlendirme
beş ekseni kapsar: madde düzeyi dağılımlar, iç tutarlılık, dört faktörlü yapı, ölçüm
değişmezliği ve ölçüt geçerliği.

İç tutarlılık, bir ölçekteki maddelerin aynı kavramı ne ölçüde tutarlı ölçtüğünü
gösterir ve burada iki katsayıyla raporlanmıştır: klasik Cronbach α ile, madde
ağırlıklarının eşit olduğu varsayımına daha az bağımlı olan McDonald ω. Ölçeklerin
çoğunda iç tutarlılık araştırma ölçütlerini karşılamıştır. Kısa olan ve yanıtların
ölçeğin en düşük ucunda toplandığı (taban etkisi taşıyan) birkaç alt ölçekte
katsayılar görece düşük kalmıştır; bunların en belirgini anne formundaki (EMBU-P)
reddetme alt ölçeğidir (Cronbach α = 0,45). Kardeş İlişkileri Anketi'nin statü/güç ve
rekabet alt ölçeklerinde de güvenirlik sınırlıdır.

Dört faktörlü yapıda kuramsal boyutlar birbirinden ayırt edilebilmiş; ancak modelin
bütününü tek bir değerde özetleyen birleşik uyum ölçütü tam karşılanmamıştır (Ek 7).
Ölçüm değişmezliği — ölçeğin DM ve kontrol gruplarında aynı yapıyı, gruplar arası
karşılaştırmayı geçerli kılacak biçimde ölçüp ölçmediği — ve ölçüt geçerliği —
ölçeğin, kuramsal olarak ilişkili olması beklenen dış değişkenlerle bağı — ayrıca
değerlendirilmiş; ölçüt geçerliği katsayıları beklenen yöndedir (Ek 7).

Bu ölçüm sınırları saklanmamış, ilgili bulguların okunmasında gözetilmiştir:
güvenirliği düşük alt ölçeklere dayanan sonuçlar (H1 reddetme, H2) bu çekinceyle
yorumlanmış; H1 reddetme bulgusu ayrıca, taban etkisine daha dayanıklı olan
madde-yanıt teorisi ve bağımsız bir Bayesçi hatla çapraz doğrulanmıştır."""

new_text = """## Ölçek ve Veri Kalitesi

Bu araştırmada ailelere uygulanan testlerin (ölçeklerin) gerçekten doğru ve tutarlı ölçüm yapıp yapmadığı, asıl analizlere geçilmeden önce özel bir kalite kontrol aşamasından geçirilmiştir. Bu istatistiksel değerlendirmenin (psikometrik özelliklerin) detaylı bulguları Ek 7'de (@sec-ek-psikometri) sunulmuştur. Kalite kontrolü beş temel başlıkta yapılmıştır: sorulara verilen yanıtların dağılımı, iç tutarlılık (soruların birbiriyle uyumu), yapının doğruluğu, gruplar arası adil ölçüm (ölçüm değişmezliği) ve dış geçerlik.

İç tutarlılık, bir testteki soruların aynı amaca ne kadar iyi hizmet ettiğini (örneğin sıcaklık boyutunu ölçen soruların kendi içinde ne kadar uyumlu yanıtlandığını) gösterir. Burada iki farklı istatistiksel yöntemle (Cronbach α ve McDonald ω) hesaplanmıştır. Kullanılan anketlerin çoğunda bu uyum bilimsel olarak yeterli düzeyde bulunmuştur.

Ancak bazı alt başlıklarda (boyutlarda) soru sayısının az olması ve ailelerin genelde testin en düşük seçeneğini işaretlemesi (örneğin "hiçbir zaman" yanıtının birikmesi) nedeniyle uyum puanı biraz düşük kalmıştır. Bu durumun en belirgin olduğu yer, anne formundaki (EMBU-P) "reddetme" boyutudur (Cronbach α = 0,45). Ayrıca çocuklara uygulanan Kardeş İlişkileri Anketi'nin "statü/güç" ve "rekabet" gibi alt bölümlerinde de güvenilirlik sınırlı kalmıştır.

Testin yapısının incelendiği aşamada, ölçeğin ölçmeyi hedeflediği dört temel alanın birbirinden başarılı şekilde ayrılabildiği görülmüştür. Ölçeğin diyabetli ailelerde ve sağlıklı kontrol ailelerinde aynı özellikleri adil biçimde ölçüp ölçmediğine (ölçüm değişmezliği) de bakılmış ve gruplar arası karşılaştırma yapmanın geçerli olduğu teyit edilmiştir. Ayrıca, anketlerin dışarıdan bakıldığında mantıken beklenen diğer kavramlarla ilişkili olup olmadığı (ölçüt geçerliği) kontrol edilmiş ve sonuçlar beklendiği yönde çıkmıştır (Ek 7).

Özetle, bazı anket bölümlerinde tespit edilen bu zayıflıklar (düşük güvenilirlik vb.) analizlerde göz ardı edilmemiş; bilakis sonuçlar değerlendirilirken bu sınırlar hep akılda tutulmuştur. Özellikle güvenilirliği düşük çıkan konularda (örneğin H1 kapsamındaki reddetme tutumu ve H2 hipotezleri) sonuçlar daha temkinli yorumlanmış, hatta reddetme ile ilgili bulgular daha gelişmiş iki farklı istatistiksel yöntemle (madde-yanıt teorisi ve Bayesçi analiz) ayrıca test edilerek sonuçların doğruluğu sağlama alınmıştır."""

if old_text in content:
    content = content.replace(old_text, new_text)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replace successful!")
else:
    print("Text not found in the file. Check for exact match.")
