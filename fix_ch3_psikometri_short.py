import re

def process_file():
    with open("chapters/03_gerec_ve_yontem.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    # The block to replace:
    start_marker = '## Ölçme Araçlarının Psikometrik Değerlendirmesi'
    end_marker = '## Veri Toplama Süreci ve Veri Yönetimi'

    new_text = """## Ölçme Araçlarının Psikometrik Değerlendirmesi

Kullanılan ebeveyn tutumu anketinin "Karşılaştırma" alt boyutunun da eklendiği dörtlü yapısı Türkçede daha önce kullanılmış olsa da [@temelAltanAtalay2018selfCompassion; @caliskanSari2018embuC], ana hipotez analizlerine geçmeden önce bu ölçek formlarının çalışmaya katılan ailelerde güvenilir sonuçlar verip vermediği özel olarak incelenmiştir. Bu ön hazırlık; anketin ebeveyn ile çocuk raporları için eşlenik olarak tasarlanmış olması ve diyabetli/sağlıklı aile yapısına ne derece uyduğunun teyit edilmesi amacıyla yürütülmüştür [@sumer2010anneBabaTutum; @mokkink2018cosmin].

Psikometrik değerlendirme beş eksende yapılandırılmıştır: madde düzeyinde dağılımlar ve iç tutarlılık (Cronbach α ve McDonald ω katsayıları) [@dunn2014alphaOmega], faktör yapısının sınanması (Doğrulayıcı Faktör Analizi ve Bayesçi çapraz doğrulama) [@li2016ordinalCFA; @muthenAsparouhov2012bsem], farklı hastalık grupları ile bilgi verenler arasında karşılaştırmayı meşru kılan ölçüm eşdeğerliği (measurement invariance) [@putnickBornstein2016measurementInvariance], ölçüt geçerliği ve aynı ailedeki katılımcılar arası ölçüm uyumu [@blandAltman1986]. Buna ek olarak, annelerin bildirimlerinde gözlenen yığılmaların (taban etkisi) bulgulara yansıması eşzamanlı alternatif stratejilerle (çoklu evren analizi) kontrol edilmiştir [@steegen2016multiverse]. 

Tüm bu psikometrik sınamaların matematiksel altyapısı, uygulanan kısıtlama adımları ve ayrıntılı istatistiksel sonuçları metin içinde mükerrerliğe yol açmamak adına **[Ek 7](#sec-ek-psikometri)**'de kapsamlı biçimde sunulmuştur. Bulgular bölümündeki ilgili sonuçlar, söz konusu ekte doğrulanan bu kalite kontrol sınırları dikkate alınarak (örneğin güvenirliği sınırda çıkan veya taban etkisi barındıran alt ölçekler belirtilerek) yorumlanmıştır.

"""

    if start_marker in content and end_marker in content:
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)
        
        updated_content = content[:start_idx] + new_text + content[end_idx:]
        
        with open("chapters/03_gerec_ve_yontem.qmd", "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("Replaced section 3.7 with a condensed version.")
    else:
        print("Markers not found.")

process_file()
