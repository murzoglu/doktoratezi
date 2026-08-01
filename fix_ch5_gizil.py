import re

def process_file():
    with open("chapters/05_tartisma_ve_sonuc.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    # Find the sentence and replace it to eliminate 'gizil'
    target = 'Bunun yerine "gizli (latent) yapı" kurduğumuzda, etkinin gerçekte daha güçlü olduğunu gördük'
    target2 = 'Bunun yerine latent (gizil) yapı modelleri kurulduğunda, gözlenen etkinin daha yüksek olduğu saptanmıştır'
    
    if target in content:
        content = content.replace(target, 'Bunun yerine latent yapı modelleri kurulduğunda, gözlenen etkinin daha yüksek olduğu saptanmıştır')
        print("Replaced target1.")
    elif target2 in content:
        content = content.replace(target2, 'Bunun yerine latent yapı modelleri kurulduğunda, gözlenen etkinin daha yüksek olduğu saptanmıştır')
        print("Replaced target2.")
    else:
        print("NOT FOUND.")

    with open("chapters/05_tartisma_ve_sonuc.qmd", "w", encoding="utf-8") as f:
        f.write(content)

process_file()
