import re

file_path = "chapters/05_tartisma_ve_sonuc.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

pattern = r"Goodman ve arkadaşlarının 193 çalışma ve 80\.851 anne-çocuk ikilisini kapsayan.*?\nolarak doğrulanmıştır \[@goodman2020parentingMediator\]\."
match = re.search(pattern, content, flags=re.DOTALL)
if match:
    print("Found!")
else:
    print("Not found.")
