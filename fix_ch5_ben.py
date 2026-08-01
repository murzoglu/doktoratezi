import re

def process_file():
    with open("chapters/05_tartisma_ve_sonuc.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    # Find the sentence and replace it to eliminate 'ben'
    target = '- **İlk olarak**, annenin anketlerde "ben çocuğuma şöyle davranıyorum" demesi ile çocuğun "annem bana böyle davranıyor" demesi arasındaki bağ çok zayıftır.'
    replacement = '- **İlk olarak**, annenin kendi tutumuna yönelik beyanı ile çocuğun algıladığı ebeveynlik arasındaki korelasyon zayıftır.'
    
    if target in content:
        content = content.replace(target, replacement)
        print("Replaced target sentence.")
    else:
        print("NOT FOUND.")

    with open("chapters/05_tartisma_ve_sonuc.qmd", "w", encoding="utf-8") as f:
        f.write(content)

process_file()
