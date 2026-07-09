import re

file_path = r"c:\Users\ozlem\OneDrive - marmara.edu.tr\Masaüstü\dökümler\tez_yazim_kilavuzu.md"

def refine_guide_headers():
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    new_lines = []

    for line in lines:
        stripped = line.strip()

        # Match "1. TITLE" -> "# 1. TITLE"
        # Match "2. TITLE" ...
        if re.match(r"^\d+\.\s+[A-ZÇĞİÖŞÜ ]+$", stripped):
            line = f"# {stripped}"

        # Match "1.1. Title" -> "## 1.1. Title"
        elif re.match(r"^\d+\.\d+\.\s+", stripped):
            line = f"## {stripped}"

        # Match "1.1.1. Title" -> "### 1.1.1. Title"
        elif re.match(r"^\d+\.\d+\.\d+\.?\s+", stripped):
            line = f"### {stripped}"

        # Match specific Sections like "İÇİNDEKİLER", "KAYNAKLAR", "EKLER", "ÖZGEÇMİŞ" if they appear alone
        elif stripped in ["İÇİNDEKİLER", "KAYNAKLAR", "EKLER", "ÖZGEÇMİŞ", "TEZ KAPAĞI", "TEZ ONAYI", "BEYAN", "TEŞEKKÜR", "TÜRKÇE ÖZET", "İNGİLİZCE ÖZET"]:
            line = f"# {stripped}"

        new_lines.append(line)

    # Re-join
    output = "\n".join(new_lines)

    # Cleaning up excessive newlines (optional but good)
    output = re.sub(r"\n{3,}", "\n\n", output)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(output)

    print("Headers refined.")

if __name__ == "__main__":
    refine_guide_headers()
