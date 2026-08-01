import re

def process_file():
    with open("chapters/03_gerec_ve_yontem.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    # Find the specific term 'Yanlış Keşif' and replace it with 'Yanlış-Keşif'
    target = 'Yanlış Keşif Oranı'
    replacement = 'Yanlış-Keşif Oranı'
    
    if target in content:
        content = content.replace(target, replacement)
        print(f"Replaced target term.")
    else:
        print(f"Target term NOT FOUND.")

    with open("chapters/03_gerec_ve_yontem.qmd", "w", encoding="utf-8") as f:
        f.write(content)

process_file()
