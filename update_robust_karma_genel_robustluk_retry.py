import re

file_path = "chapters/04_bulgular.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Using regex to replace the text before the tables/figures
pattern = r"## Robustluk ve Bayesçi Doğrulama.*?Robustluk ve duyarlılık özetleri @tbl-apa-robustness ve @tbl-apa-sensitivity\n(içinde sunulmuştur\.)?"

replacement = """## Robustluk ve Bayesçi Doğrulama

**Çoklu evren (specification curve).** Bir sonucun sadece seçilen "tek bir analize" mi bağlı olduğunu, yoksa yöntem ne kadar değiştirilirse değiştirilsin geçerli mi kaldığını sınamak için akla yatkın tüm analiz kombinasyonları (toplam 120 farklı varyasyon) denenmiştir [@simonsohn2020specificationCurve]. Annenin bildirdiği tutumlarda hesaplama yöntemi ne olursa olsun gruplar arasında anlamlı bir fark oluşmadığı teyit edilmiştir (spesifikasyonların %0'ında p < 0,05). Elde edilen sonuçların yöntem değişikliğinden etkilenmediğini gösteren dağılım @fig-specification-curve içinde sunulmuştur.

**Eşdeğerlik (TOST).** Annenin tutumlarında "fark yok" bulgusunun, istatistiksel olarak grupları gerçekten ne kadar "eşit" kıldığı test edilmiştir. Aşırı koruma ve karşılaştırma tutumlarında gruplar "Eşdeğer" (farksız) bulunurken, sıcaklık ve reddetme boyutları daha keskin istatistiksel sınırlarda "Belirsiz" sınıfında kalmıştır (Ek 5, @tbl-apa-tost-sensitivity).

**Ölçülmemiş karıştırıcı dayanıklılığı.** Araştırmaya dâhil edilmemiş, unutulmuş tamamen gizli bir faktörün (örneğin bambaşka bir hastalığın veya koşulun) sonuçları bozup bozamayacağı test edilmiştir. Annelerin tutumlarına dair H3 bulgularının, böylesi gizli bir dış etkiye karşı zayıf-orta düzeyde dayanıklı olduğu görülmüştür (sağlamlık değeri RV_q = 0,04–0,08 ve E-değeri 1,36–1,59). Gizli etkinin taşıması gereken risk gücünün haritası @fig-sensemakr-contour grafiğinde gösterilmiştir.

**Negatif kontrol ve eksik veri sağlamlığı.** Tesadüflerin bizi yanıltıp yanıltmadığını görmek için veri setine rastgele sahte numaralar eklenerek test yapılmış ve sonuçların bu sahtelikten etkilenmediği (başarılı falsifikasyon, sahte katsayılar p > 0,10) saptanmıştır. Ayrıca anketlerdeki "boş bırakılmış (eksik)" soruların hesaba katılma biçimi üç farklı istatistik tekniğiyle değiştirilmiş, ailenin "sosyoekonomik geliri" dört ayrı formülle tekrar tanımlanmış; yine de asıl sonuçların ve yönlerin (en fazla 0,01 SD sapmayla) sabit kaldığı görülmüştür.

Robustluk ve duyarlılık özetleri @tbl-apa-robustness ve @tbl-apa-sensitivity içinde sunulmuştur."""

new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
if count > 0:
    print("Robustluk replaced successfully.")
else:
    print("Robustluk block STILL not found.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

