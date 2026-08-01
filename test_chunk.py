import sys

file_path = "chapters/05_tartisma_ve_sonuc.qmd"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

match = re.search(r"(\*\*Ölçüm katmanı: latent etki\.\*\*.*?\*\*Robustluk katmanının işlevi\.\*\*)", content, re.DOTALL)
if match:
    print(match.group(1)[:500] + "\n...\n" + match.group(1)[-500:])
else:
    print("Not found")

