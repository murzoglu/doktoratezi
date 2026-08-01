import sys

file_path = "chapters/04_bulgular.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    """#| tbl-cap: "H1 doğrulayıcı grup ana etkisi tablosu: dört EMBU-C (çocuğun algıladığı ebeveynlik) alt ölçeğinin her birinde DM eksi Kontrol grup farkı, ön-kayıtlı doğrulayıcı estimand olarak raporlanır. Fark, indeks çocuk ile sağlıklı kardeş rolleri eşit ağırlıkla ortalanarak, aile düzeyi rastgele kesişimli çok düzeyli modelden ham 1–4 ölçek puanı biriminde kestirilir; sütunlar tahmini farkı (b), %95 güven aralığını ve çokluk düzeltmeli (BH-FDR) anlamlılığı (q) verir. Okuma anahtarı: bir alt ölçeğin %95 güven aralığı sıfırı içermiyor ve BH-FDR q değeri 0,05'in altındaysa o boyutta grup farkı sıfırdan ayırt edilir." """:
    """#| tbl-cap: "H1 çocuk algısı grup farkı tablosu: Çocukların annelerinden algıladıkları dört farklı ebeveynlik tutumunda (sıcaklık, aşırı koruma, reddetme, karşılaştırma) diyabetli aileler ile sağlıklı kontrol aileleri arasındaki farkları gösterir. Okuma anahtarı: Tablodaki 'güven aralığı' sıfırı içermiyorsa ve anlamlılık (q) değeri 0,05'in altındaysa o ebeveynlik boyutunda iki grup arasında belirgin bir fark var demektir." """,

    """#| tbl-cap: "H1 birincil çok düzeyli kovaryans analizinin sabit etkileri: grup ana etkisi, farkın hangi çocuk rolünden (hasta indeks çocuk ya da sağlıklı kardeş) geldiğini görmek üzere rol-özgül hücre kontrastlarına ayrıştırılır. Katsayılar (b) ham EMBU-C ölçek puanı birimindedir; bu hücre kontrastları betimsel ayrıştırmadır, ayrı bir çokluk düzeltmesi ailesi oluşturmaz. Okuma anahtarı: her rol-özgül kontrastta %95 güven aralığının sıfırı içerip içermediğine bakılır; değerler düzeltilmiş anlamlılık iddiası değil, ana etkinin rollere göre yön ve büyüklük dökümüdür." """:
    """#| tbl-cap: "H1 çocuk rollerine göre farklılıklar tablosu: Diyabetli ve kontrol aileleri arasındaki genel farkın, hangi çocuktan (hasta olan indeks çocuktan mı, yoksa sağlıklı kardeşinden mi) geldiğini detaylandıran döküm tablosudur. Okuma anahtarı: Güven aralığının sıfırı içermemesi, o özel eşleşmede dikkate değer bir algı farklılığı olduğunu işaret eder." """,

    """#| tbl-cap: "H1 Bayesçi çift raporlama: dört EMBU-C alt ölçeğinin her birinde DM–Kontrol grup farkı, klasik (frekansçı) analizin yanı sıra bağımsız bir Bayesçi hatla da raporlanır. Sütunlar posterior fark katsayısını (b), %95 güvenilir aralığı, yön olasılığını (pd) ve Bayes faktörünü (BF₁₀) verir. Okuma anahtarı: BF₁₀ Jeffreys ölçeğinde 1–3 zayıf, 3–10 orta, 10–30 güçlü kanıt gösterir; BF₁₀ birden küçükse fark-yokluğu (H0) lehine kanıt anlamına gelir." """:
    """#| tbl-cap: "H1 sağlamlık (Bayes) doğrulama tablosu: Çocukların algısındaki farklılıkların gerçekten var olup olmadığını klasik yöntemlerin ötesinde bağımsız ve daha gelişmiş bir istatistikle (Bayesçi analizle) yeniden test eder. Okuma anahtarı: Tablodaki BF₁₀ değeri 1'den ne kadar büyükse gruplar arasında 'fark olduğuna' dair kanıt o kadar güçlüdür (3-10 arası orta, 10 üzeri güçlü kanıt sayılır). Değer 1'den küçükse 'fark yoktur' ihtimali ağır basar." """,

    """#| tbl-cap: "H1 grup-içi rol kontrastı tablosu (keşifsel/post-hoc): kontrol kolu tümüyle dışarıda bırakılıp yalnız aynı ailenin iki çocuğu — aile içi indeks çocuk eksi sağlıklı kardeş — dört EMBU-C alt ölçeğinde karşılaştırılır. Kontrastlar DM ve kontrol ailelerinde ayrı ayrı, aile içi düzeyde ve BH-FDR düzeltmeli olarak hesaplanır. Okuma anahtarı: her alt ölçekte aile içi indeks–kardeş farkının %95 güven aralığı sıfırı içerip içermediğine ve BH-FDR q değerine bakılır; bu katman grup ana etkisinin değil, aynı aile içindeki rol ayrımının keşifsel sınamasıdır." """:
    """#| tbl-cap: "H1 aile içi kardeşler arası karşılaştırma tablosu: Aynı ailenin içinde yaşayan iki çocuğun (diyabetli indeks çocuk ile sağlıklı kardeşinin) annelerinin ebeveynlik tutumlarını birbirlerine kıyasla farklı algılayıp algılamadıklarını gösterir. Okuma anahtarı: Güven aralığı sıfırı kapsıyorsa aynı evdeki iki kardeş arasında annelerinin tutumuna dair belirgin bir fikir ayrılığı yoktur." """,

    """![H1 orman grafiği — dört EMBU-C alt ölçeğinde (sıcaklık, aşırı koruma, reddetme, karşılaştırma) DM eksi Kontrol grup ana etkisi. Noktalar, aile düzeyi rastgele kesişimli çok düzeyli modelden (482 çocuk-satırı; indeks çocuk ve sağlıklı kardeş rolleri eşit ağırlıkla ortalanmış) kestirilen tahmini ham 1–4 ölçek puanı biriminde; yatay çizgiler %95 güven aralığını, kesikli dikey çizgi sıfır farkı gösterir. Okuma anahtarı: bir alt ölçeğin güven aralığı kesikli çizgiyi kesmiyorsa grup farkı sıfırdan ayırt edilir; çizginin genişliği tahminin kesinliğini yansıtır.](docs/assets/figures/carbon/primary/fig-07-h1-forest.svg){#fig-h1-forest width="96%" fig-align="center"}""":
    """![H1 ebeveynlik algısı genel fark grafiği (Orman grafiği): Çocukların annelerinden algıladıkları tutumlarda diyabet ve kontrol aileleri arasındaki genel farkı gösterir. Noktalar hesaplanan farkı, yatay çizgiler ise güven aralığını temsil eder. Okuma anahtarı: Kesikli dikey çizgi 'hiç fark olmadığını' (sıfırı) gösterir. Yatay çizgiler bu kesikli dikey çizgiye dokunmuyor veya onu kesmiyorsa, iki grup arasındaki fark kesindir.](docs/assets/figures/carbon/primary/fig-07-h1-forest.svg){#fig-h1-forest width="96%" fig-align="center"}"""
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Part 2 replacements done.")
