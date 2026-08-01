import re

file_path = "chapters/05_tartisma_ve_sonuc.qmd"

def update_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    replacements = [
        (
            r"En güçlü ve en tutarlı sinyal reddetmedir\. Bu nedenle izleyen kuramsal tartışma\nöncelikle reddetme ekseninde yürütülmekte.*?[^\n]\n\n",
            """Bulunan en güçlü ve sağlam sonuç 'reddetme' duygusundaki artıştır. Bu sebeple izleyen tartışma öncelikle bu duygu üzerinde duracak; aşırı koruma bulgusu ise diyabet gibi kronik hastalıklarda kuralların ve denetimin zorunlu olarak artması (hastalık yönetimi) gerçeğiyle birlikte ele alınacaktır.\n\n"""
        ),
        (
            r"İki grup arasındaki reddetme farkı, etki büyüklüğü ölçütlerinde \"küçük ile orta\narasında\" bir konumdadır\..*?\[@funderOzer2019effectSize\]\.\n\n",
            """İki grup çocuk arasındaki 'reddedilmiş hissetme' farkı, istatistiksel ölçülere göre "küçük ile orta arasında" bir boyuttadır (Hedges g ≈ 0,38). Rakamlarla ifade etmek gerekirse, diyabetli çocuklar diğerlerinden yaklaşık üçte bir (1/3) birim daha fazla reddedilmiş hissetmektedir. Bu durum, çocuğun hislerindeki genel değişimin %4'lük (r² ≈ 0,04) küçük bir kısmının doğrudan "diyabet hastası olmakla" ilgili olduğunu gösterir. Etki küçük gibi görünse de bilimsel olarak (Funder ve Ozer'in belirttiği gibi) istikrarlı, tekrar eden ve zamanla birikerek büyüyen bir sonuç olduğu için pratik hayatta son derece ciddiye alınması gereken bir farktır [@funderOzer2019effectSize].\n\n"""
        ),
        (
            r"Bu etkinin literatürdeki karşılığı, Pinquart'ın 325 çalışmayı birleştiren\nrastgele-etkili meta-analizinde görülebilir\..*?\[@pinquart2013\]\.\n\n",
            """Bu sonucun dünyadaki diğer araştırmalarla ne kadar örtüştüğünü görmek için Pinquart'ın 325 farklı çalışmayı birleştirdiği devasa incelemesine (meta-analiz) bakılabilir. O incelemeye göre; kronik hastalığı olan çocukların ailelerinde en çok göze çarpan değişiklik 'aşırı korumacılık' (g = 0,39) iken, onu sırasıyla 'duygusal sıcaklığın azalması' (g = −0,22) ve 'olumsuz ebeveyn-çocuk ilişkisi' (g = −0,16) izler. Bu farklılıklar çoğunlukla küçüktür ve hastalıktan hastalığa değişir. Sadece diyabet hastalarına bakıldığında ise (16 ayrı araştırma), ebeveyn-çocuk ilişkisindeki olumsuzlaşma istatistiksel olarak (g = −0,23) kanıtlanmış durumdadır [@pinquart2013].\n\n"""
        ),
        (
            r"Mevcut çalışmadaki reddetme etkisi \(g ≈ 0,38\) bu tabloya iyi oturmaktadır\..*?tutarlıdır\.\n\n",
            """Bu tezin ulaştığı "reddedilme" etkisi (g ≈ 0,38), dünyadaki bu genel tabloyla çok iyi uyuşmaktadır. Tezin bulduğu etki, dünyadaki diğer diyabet çalışmalarının ortalamasından biraz daha büyük; diğer hastalıklardaki aşırı koruma etkisiyle ise neredeyse aynı boyuttadır. Üstelik bu çalışmada 'aşırı koruma' duygusunun da diyabet grubunda çok net arttığı kanıtlanmıştır (BF₁₀ = 6,93; Bulgular, @tbl-apa-h1-group). Yani hastalığın sürekli şeker ölçümü ve katı kurallar gerektiren zorlayıcı yapısı, ebeveynleri doğal olarak daha korumacı yaparken, çocuklarda bu durumun bir yan etkisi olarak (veya paralelinde) 'reddedilmişlik/anlaşılamama' hissi yaratmaktadır. Bu sonuçlar, dünya literatüründeki "hastalığa uyum sağlansa da bazı kaçınılmaz tutum sapmaları olur" şeklindeki genel kanıyı birebir destekler.\n\n"""
        ),
        (
            r"Ancak bu bulgu tek başına, mutlak bir hastalık etkisi olarak okunmamalıdır\..*?\(ayrıntı Sınırlılıklar bölümünde\)\.\n\n",
            """Ancak ulaşılan bu sonuç, her şeyin tek sorumlusunun kesinlikle 'diyabet' olduğu şeklinde (mutlak bir etki gibi) okunmamalıdır. Araştırmada hastaların geldiği hastane ile anketi doldurdukları yıl bazı noktalarda birbirine girmiş durumdadır. Örneğin grupların zaman açısından en dengeli eşleştiği sadece '2023 yılına ait verilere' bakıldığında, aradaki bu reddetme ve koruma farkı kaybolmaktadır (Bulgular, @tbl-apa-h1-period2023). 2023 yılında bu etkinin sıfırlanması, verilerin azlığından (güç kaybı) da kaynaklanıyor olabilir, ancak yine de başka dış etkenlerin (zaman/hastane gibi) sonucu değiştirme ihtimalini masada bırakır. Bu nedenle, gözlenen farkların bağımsız başka bir grupta, zaman ve mekân etkisinden tamamen arındırılarak tekrar test edilmesi (sınanması) gereklidir.\n\n"""
        ),
        (
            r"Reddetme boyutundaki fark sayısal olarak küçük görünse de, Rohner'ın Ebeveyn\nKabul-Red Kuramı.*?göz ardı edilmemesi\ngereken bir bulgudur\.\n\n",
            """Rakamlara bakıldığında 'reddedilmişlik' hissi küçük bir artış gibi dursa da, Rohner'ın meşhur Ebeveyn Kabul-Red Kuramına (PARTheory) göre bunun psikolojik ağırlığı çok büyüktür. Bu kuram, önemli olanın annenin veya babanın ne yaptığı değil; çocuğun bunu "beni reddediyorlar" şeklinde anlayıp anlamadığı olduğunu savunur. Dünyanın her yerinde, bir çocuğun ruh sağlığını belirleyen en güçlü şey bu şahsi 'reddedilmişlik' hissidir [@rohner2004parAcceptance]. Bu nedenle, farkın sayısal büyüklüğünden ziyade 'yönü' (çocuğun bunu olumsuz hissetmesi) kritiktir. Çocuğun içine attığı küçük ama sürekli bir anlaşılamama hissi, ileride klinik sorunlara dönüşme riski taşır. Dolayısıyla bu, asla küçümsenmemesi gereken bir bulgudur.\n\n"""
        ),
        (
            r"Çocuk bildiriminin birincil ölçüt olarak merkeze alınması, ampirik temellere dayanan.*?doğrudan belirlemektedir\.\n\n",
            """Araştırmada 'çocuğun kendi beyanının' en önemli referans olarak kabul edilmesi tesadüf değil, bilerek seçilmiş bilimsel bir karardır. Çünkü ebeveynlik sorunlarında, "kimin konuştuğunun" sonucu değiştirdiği dünya çapında bilinen bir gerçektir. Pinquart ve Shen'in 569 araştırmayı incelediği çalışmasında; evdeki sorunları anne-baba anlatırsa sorun büyük (g = 0,46), öğretmen anlatırsa orta (g = 0,37), ergenin bizzat kendisi anlatırsa sorun en küçük boyutta (g = 0,17) çıkmaktadır [@pinquart2011behaviorProblems]. Kısacası kime sorduğunuz, alacağınız cevabın boyutunu doğrudan belirlemektedir.\n\n"""
        ),
        (
            r"Bu bilgi-verici bağımlılığının ikinci ayağı, raporlar arası uyumun gelişimsel\npsikopatolojide.*?düzeyinde bulmuştur \[@deLosReyes2015\]\.\n\n",
            """Sorunun kime sorulduğunun (bilgi-verici ayrımının) bir diğer sonucu da anne ile çocuğun verdiği cevapların genelde hiçbir zaman uyuşmamasıdır. Achenbach'ın 119 çalışmalık ünlü raporunda, iki ebeveynin birbiriyle uyumu yüksekken (r = 0,60), ebeveyn ile çocuk arasındaki uyum sadece r = 0,22'de kalmıştır [@achenbach1987crossinformant]. Yakın tarihte De Los Reyes'in 341 araştırmayı (1989-2014) toparladığı dev çalışmada da anne ile çocuk arasındaki genel uyum oranı sadece r = 0,28 olarak doğrulanmıştır [@deLosReyes2015].\n\n"""
        ),
        (
            r"Bu güncel meta-analizin iki moderatörü mevcut çalışma için doğrudan belirleyicidir\..*?doğrudan genişletilebilir\.\n\n",
            """İşte bu uyumsuzluk, bu tezin sonuçlarını anlamak için çok kritik iki kurala işaret eder: Birincisi, yaramazlık gibi 'dışarıdan görünen' sorunlarda anne-çocuk uyumu biraz daha iyiyken (r = 0,30); içe kapanıklık, reddedilme gibi 'çocuğun içinde yaşadığı' duygularda uyum en dibe vurmaktadır (r = 0,25). İkincisi, anne ile baba aynı evde yaşadıkları için birbirleriyle uyumlu cevaplar (0,48-0,58) verirken; anne ile çocuk arasındaki jenerasyon ve rol farkı uyumu neredeyse yarı yarıya (0,26) düşürür. Tezin odağındaki 'reddedilme duygusu' ise tamamen çocuğun iç dünyasıyla ilgilidir ve doğal olarak ebeveyn ile çocuk arasında en büyük fikir ayrılığının yaşandığı, en uyumsuz boyuttur.\n\n"""
        )
    ]

    for pattern, repl in replacements:
        content, count = re.subn(pattern, repl, content, flags=re.DOTALL)
        if count == 0:
            print(f"Warning: Pattern not found:\n{pattern[:50]}...")
        else:
            print(f"Success: Replaced {count} times.")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

update_file(file_path)
print("Second batch done.")
