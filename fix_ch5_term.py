import re

def process_file():
    with open("chapters/05_tartisma_ve_sonuc.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    # Find the specific sentence with the word "gizil" and replace it
    target = 'Örneklemdeki annelerin ebeveynlik tutum yanıtları üzerinden üç alt profilli bir gizil sınıflandırma (LPA) denenmiştir.'
    replacement = 'Örneklemdeki annelerin ebeveynlik tutum yanıtları üzerinden üç alt profilli bir latent sınıflandırma (LPA) denenmiştir.'
    
    if target in content:
        content = content.replace(target, replacement)
        print(f"Replaced target sentence.")
    else:
        # Fallback to direct replace
        content = content.replace('gizil sınıflandırma', 'latent sınıflandırma')
        print(f"Direct replaced 'gizil'.")

    with open("chapters/05_tartisma_ve_sonuc.qmd", "w", encoding="utf-8") as f:
        f.write(content)

process_file()
