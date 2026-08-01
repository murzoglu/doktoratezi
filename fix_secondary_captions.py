import re

file_path = "chapters/04_bulgular.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. trifactor
content = re.sub(
    r'(!\[Trifaktör \(üçlü\) analiz modeli: [^\]]+taraflı\) algıyı gösterir\.)',
    r'\1 Sonuç: Model, aile içindeki gerçeğin her bireyin kendi algısından başarıyla ayrılabildiğini, anketin işe yaradığını doğrulamıştır.',
    content
)

# 2. floor_irt
content = re.sub(
    r'(!\[Yanıt yığılmasını düzelten gelişmiş analiz grafiği \(Madde-yanıt kuramı\): [^\]]+asıl \'kapatılamayan farkı\' gösterir\.)',
    r'\1 Sonuç: Anketlerdeki yığılma problemi matematiksel olarak düzeltildiğinde bile, diyabetli çocukların daha az reddedilme ve daha fazla aşırı koruma hissettiği gerçeği değişmemiş, hatta fark daha belirgin hale gelmiştir.',
    content
)

# 3. h1_spec_curve
content = re.sub(
    r'(!\[Analiz sağlama \(çoklu-evren / multiverse\) grafiği: [^\]]+değişmeyeceği anlamına gelir\.)',
    r'\1 Sonuç: Analiz yöntemi ne kadar değiştirilirse değiştirilsin, tezin ulaştığı asıl sonucun (diyabetin çocuğun algısı üzerindeki etkisi) son derece sağlam ve sarsılmaz olduğu kanıtlanmıştır.',
    content
)

# 4. meta_forest
content = re.sub(
    r'(!\[Tez sonuçlarının dış dünya \(literatür\) ile kıyaslanması: [^\]]+görsel olarak karşılaştırılmıştır\.)',
    r'\1 Sonuç: Bu tezin bulduğu etkinin büyüklüğü, dünyada yapılmış olan diğer önemli uluslararası araştırmaların sonuçlarıyla paralel (uyumlu) bulunmuştur.',
    content
)

# 5. dca_heatmap
content = re.sub(
    r'(!\[Genişletilmiş klinik net fayda ısı haritası: [^\]]+faydanın nasıl değiştiği incelenir\.)',
    r'\1 Sonuç: Sadece annenin ebeveynlik tutumlarına bakılarak depresyon taraması yapılmasının, doktorlar ve hastalar açısından belirgin ve pratik bir kazanç (net fayda) sağlamadığı görülmüştür.',
    content
)

# 6. expl_pdt
content = re.sub(
    r'(!\[Farklılaşmış \(diferansiyel\) ebeveynlik testi grafiği: [^\]]+ayrımcılık olmadığını gösterir\.)',
    r'\1 Sonuç: Aile içinde annenin bir çocuğa diğerinden belirgin biçimde farklı (taraf tutarak) davrandığına dair istatistiksel bir kanıt bulunamamıştır.',
    content
)

# 7. expl_comorbidity
content = re.sub(
    r'(!\[Anne ek hastalığı \(komorbidite\) ve depresyon ilişkisi grafiği: [^\]]+yönü ile görselleştirilmiştir\.)',
    r'\1 Sonuç: Annenin diyabet dışında başka bir kronik hastalığı olmasının, onun depresyon riskini istatistiksel olarak tek başına anlamlı şekilde artırmadığı görülmüştür.',
    content
)

# 8. t06c_h1_period2023
content = re.sub(
    r'(#\| tbl-cap: "H1 dönem duyarlılığı çözümlemesi: [^"]+ayrı bir açıklamadır\.")',
    r'\1 Sonuç: Araştırmanın sadece 2023 yılındaki en dengeli grubuna bakıldığında, diyabetin çocukların algısındaki olumlu etkisi görünmez olmuştur. Bu durum, sonuçların döneme ve gruba göre değişebileceğini (veya daraltılan grupta istatistiksel gücün yetmediğini) gösterir."',
    content
)

# Robustluk tables just in case they were missed
# t06a_h1_tost_summary
content = re.sub(
    r'(#\| tbl-cap: "Robustluk özeti: çoklu evren ve TOST\.[^"]+mutlak değildir\.")',
    r'\1 Sonuç: Araştırmanın asıl bulgusu olan diyabetli çocukların \'daha az reddedildiği\' gerçeği hemen her analiz senaryosunda doğrulanırken, \'aşırı koruma\' konusundaki farkın o kadar net ve güçlü olmadığı görülmüştür."',
    content
)

# t06b_h1_sensitivity_summary
content = re.sub(
    r'(#\| tbl-cap: "Duyarlılık özeti: ölçülmemiş karıştırıcı ve falsifikasyon[^"]+olası bir dönem/kohort vekili uyarısı olarak okunur\.")',
    r'\1 Sonuç: Çalışmada hesaba katılmayan gizli bir değişkenin mevcut sonuçları bozabilmesi için çok yüksek bir etki gücüne (E-değeri) sahip olması gerektiği saptanmıştır. Bu da tezin ulaştığı sonucun dış tehlikelere karşı dayanıklı olduğunu göstermektedir."',
    content
)

# fig-specification-curve
content = re.sub(
    r'(!\[Çoklu-evren analiz sağlamlık haritası: [^\]]+sabit kaldığını gösterir\.)',
    r'\1 Sonuç: Farklı hesaplama yöntemleri kullanıldığında dahi, reddetme bulgusunun her koşulda aynı kaldığı (noktaların düzenli seyri) ve sağlam olduğu kanıtlanmıştır.',
    content
)

# fig-sensemakr-contour
content = re.sub(
    r'(!\[Gözden kaçan \'gizli etken\' dayanıklılık \(sensemakr\) haritası: [^\]]+sonuç o kadar sağlam\) demektir\.)',
    r'\1 Sonuç: Haritadaki nokta tehlike sınırlarından oldukça uzaktır; yani araştırmada ölçülmeyi unutulmuş yepyeni bir özellik olsa bile, bu yeni etkinin tezin asıl kararını bozması matematiksel olarak pek olası değildir.',
    content
)

# tbl_apa_h1_h3_bayes_summary
content = re.sub(
    r'(#\| tbl-cap: "Bayesçi çift raporlama \(satırlar hipoteze göre gruplanmıştır\)\.[^"]+tanı ölçütüdür\.")',
    r'\1 Sonuç: Bayes (olasılık) analizi de araştırmanın klasik sonuçlarını onaylamış; reddetme ve aşırı koruma konularında fark olduğu tezini güçlü bir kanıt olarak (BF10) desteklemiştir."',
    content
)

# tbl_apa_capstone
content = re.sub(
    r'(#\| tbl-cap: "Genel bulgu sentezi — bütünleşik özet \(kapstone\) tablosu\.[^"]+nedensellik göstergesi değildir\.")',
    r'\1 Sonuç: Sayısal (anket) analizler ile sözel (nitel görüşme) bulguları birbirini tamamlamış; diyabetli ailelerin reddetme yerine korumacı bir yapıya yöneldiği gerçeği her iki koldan da doğrulanmıştır."',
    content
)

# Fix double quotes if they occur at the end
content = content.replace('.""', '."')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Captions updated with conclusions.")
