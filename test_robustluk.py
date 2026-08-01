import sys

file_path = "chapters/05_tartisma_ve_sonuc.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re
match = re.search(r"\*\*Robustluk katmanının işlevi\.\*\*.*?olarak yorumlanmaktadır\.", content, re.DOTALL)
if match:
    print(match.group(0))
else:
    print("Not found")
