import re

def process_file():
    with open("chapters/05_tartisma_ve_sonuc.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        'öz-rapor': 'öz-bildirim',
        'öz-raporlu': 'öz-bildirimli',
        'öz-rapora': 'öz-bildirime',
        'öz-rapordaki': 'öz-bildirimdeki',
        'devasa meta-analizinde': 'kapsamlı meta-analizinde',
        'bizde sorun yok': 'farklılık bildirmemesi',
    }

    count = 0
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            count += 1
            print(f"Replaced: {old} -> {new}")
        else:
            print(f"NOT FOUND: {old}")

    with open("chapters/05_tartisma_ve_sonuc.qmd", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Total replaced in ch5: {count}")

process_file()
