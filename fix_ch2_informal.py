import re

def process_file():
    with open("chapters/02_genel_bilgiler.qmd", "r", encoding="utf-8") as f:
        content = f.read()

    replacements = {
        'Kaynak farklılıkları aileleri basitçe "avantajlı" veya "dezavantajlı" olarak etiketlemek için değil': 'Kaynak farklılıkları aileleri indirgemeci bir yaklaşımla "avantajlı" veya "dezavantajlı" olarak etiketlemek için değil',
        'Kısacası T1DM\'nin aile sistemindeki anlamı zamanla değişir.': 'Dolayısıyla T1DM\'nin aile sistemindeki bağlamsal anlamı ve yükü zamanla değişim göstermektedir.'
    }

    count = 0
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            count += 1
            print(f"Replaced: {old[:30]}...")
        else:
            print(f"NOT FOUND: {old[:30]}...")

    with open("chapters/02_genel_bilgiler.qmd", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Total replaced in ch2: {count}")

process_file()
