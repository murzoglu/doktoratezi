import re

file_path = "chapters/04_bulgular.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Aracılık
content = re.sub(
    r'(#\| tbl-cap: "Aracılık analiz sonuçları:[^"]+hükmedilir\.")',
    r'\1 Sonuç: Bu analiz, depresyon ile çocuğun algısı arasındaki bağın \'annenin kendi tutumu\' üzerinden aktarılmadığını (aracılığın işlemediğini) göstermiştir."',
    content
)

# LPA
content = re.sub(
    r'(#\| tbl-cap: "Aileleri gruplara \(profillere\) ayırma analizi \(LPA/LCA\):[^"]+temiz profiller olduğunu gösterir\.")',
    r'\1 Sonuç: Aileler gizli özelliklerine göre üç temel profile ayrılmış; ancak diyabet tanısının bu profillerden (kötü veya iyi gruptan) herhangi birine düşme ihtimalini değiştirmediği görülmüştür."',
    content
)

# Ağ (Network)
content = re.sub(
    r'(#\| tbl-cap: "Aile içi ilişkilerin istatistiksel ağ \(network\) analizi sonuçları:[^"]+benzer olduğunu göstermektedir\.")',
    r'#| tbl-cap: "Aile içi ilişkilerin istatistiksel ağ (network) analizi sonuçları: Annelerin tutumları, kardeşlerin ilişkileri ve depresyon gibi 9 temel konunun birbiriyle nasıl bir \'örümcek ağı\' gibi bağlandığını özetler. Okuma anahtarı: Hangi özelliğin ağın tam \'merkezinde\' yer aldığını (en çok etkileşen/bağlanan konu) gösterir. Sonuç: Karşılaştırma testi (NCT), bu ilişki ağının diyabetli aileler ile sağlıklı ailelerde (örneğin depresyonun aile içindeki bağları sarsma biçimi açısından) birbirine çok benzediğini göstermiştir."',
    content
)

# Klinik Fayda
content = re.sub(
    r'(#\| tbl-cap: "Anne depresyonu tarama modeli performansı:[^"]+başarıyı temsil eder\.")',
    r'\1 Sonuç: Annelerin ebeveynlik tutumlarına bakarak kimin depresyonda olduğunu tahmin etmek çok zordur; bu modelin klinik olarak net bir teşhis katkısı bulunamamıştır."',
    content
)

# DM Klinik
content = re.sub(
    r'(#\| tbl-cap: "Diyabet klinik bulguları alt-analizi:[^"]+ispatlanamadı\' anlamına gelir\.")',
    r'\1 Sonuç: Çocukların kan şekeri seviyesi veya diyabete yakalandıkları yaş ile annelerinin tutumları arasında istatistiksel olarak gösterilebilen bir bağlantı bulunamamıştır."',
    content
)

# Fix duplicated double quotes at the end of strings just in case
content = content.replace('.""', '."')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Regex-based caption fixes done.")
