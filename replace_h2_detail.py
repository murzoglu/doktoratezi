import sys

file_path = "chapters/04_bulgular.qmd"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_text = """İkinci olarak, evdeki bir çocuğun kardeş algısının diğer çocuğu da etkileyeceği gerçeğinden yola çıkılarak kardeşlerin birbirlerine olan etkileri hesaplanmış (karşılıklı bağımlılık modeli) ve burada da gruplar veya çocukların rolü (hasta ya da sağlıklı olması) açısından bir fark bulunamamıştır (p > 0,350). Son olarak, kardeşlerin kavga/çatışma davranışları gizli (latent) bağlarla incelendiğinde kardeşler arası ilişkinin r = 0,27 düzeyinde olduğu bulunmuş; bu ilişkinin çocukların cinsiyetine ya da aralarındaki yaş farkına göre değişmediği anlaşılmıştır."""

new_text = """İkinci olarak, evdeki bir çocuğun kardeş algısının diğer çocuğu da etkileyeceği gerçeğinden yola çıkılarak kardeşlerin birbirlerine olan etkileri hesaplanmış (karşılıklı bağımlılık modeli) ve burada da gruplar veya çocukların rolü (hasta ya da sağlıklı olması) açısından bir fark bulunamamıştır (p > 0,350). Son olarak, doğrudan anket puanları yerine, bu puanların altındaki gerçek yapıyı matematiksel olarak ayrıştıran özel bir modelle (Olsen-Kenny düad modeli) kardeşlerin kavga/çatışma davranışları incelenmiştir. Bu gizli (latent) bağ analizinde, kardeşler arasındaki çatışma algısının r = 0,27 düzeyinde pozitif bir ilişki (korelasyon) gösterdiği bulunmuştur; yani bir kardeş çatışma bildirdiğinde, diğeri de benzer oranda çatışma bildirme eğilimindedir. Dikkat çekici olan, bu karşılıklı ilişkinin çocukların her ikisinin de aynı veya farklı cinsiyette olmasına ya da aralarındaki yaş farkının büyüklüğüne göre bir değişim göstermemiş olmasıdır."""

if old_text in content:
    content = content.replace(old_text, new_text)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Replace successful!")
else:
    print("Text not found in the file. Check for exact match.")
