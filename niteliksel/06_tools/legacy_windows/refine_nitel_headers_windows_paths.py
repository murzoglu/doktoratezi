import re
import os

input_path = r"c:\Users\ozlem\OneDrive - marmara.edu.tr\Masaüstü\dökümler\nitel_ana_duzenlenmis.md"
# We overwrite the same file
output_path = input_path

def upgrade_headers():
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Dictionary of specific lines to promote to headers
    # "Search String": "Replacement"
    header_map = {
        "**YÖNTEM (METHODS)**": "## YÖNTEM (METHODS)",
        "**Araştırma Tasarımı (Study Design)**": "### Araştırma Tasarımı (Study Design)",
        "**Araştırma Ortamı ve Katılımcılar (Setting and Participants)**": "### Araştırma Ortamı ve Katılımcılar (Setting and Participants)",
        "**Örneklem Seçimi (Sampling)**": "### Örneklem Seçimi (Sampling)",
        "**Veri Toplama (Data Collection)**": "### Veri Toplama (Data Collection)",
        "**Araştırmacı Özellikleri ve Refleksivite (Researcher Characteristics and Reflexivity)**": "### Araştırmacı Özellikleri ve Refleksivite (Researcher Characteristics and Reflexivity)",
        "**Veri Analizi (Data Analysis)**": "### Veri Analizi (Data Analysis)",
        "**Geçerlik ve Güvenirlik (Rigor)**": "### Geçerlik ve Güvenirlik (Rigor)",
        "**Etik Hususlar (Ethical Considerations)**": "### Etik Hususlar (Ethical Considerations)",
        "**Katılımcı Özellikleri (Participant Characteristics)**": "### Katılımcı Özellikleri (Participant Characteristics)"
    }

    # 1. Promote specific known headers
    for key, value in header_map.items():
        # Pattern: exact line match, possibly with whitespace
        # Escape the key for regex
        pattern = r"^\s*" + re.escape(key) + r"\s*$"
        content = re.sub(pattern, value, content, flags=re.MULTILINE)

    # 2. Ensure "Alt Tema" headers are consistent.
    # Some might be "**Alt Tema..." without ##.
    # Pattern: **Alt Tema ...** -> ### Alt Tema ...
    # Currently in the file they seem to be "## **Alt Tema..." or just "### **Alt Tema...".
    # Let's standardize to "### Alt Tema..." (removing the inside bolding if it's in a header)
    # Actually, Markdown headers with bolding inside `## **Title**` are valid but redundant. `## Title` is cleaner.

    # Convert `## **Title**` to `## Title`
    # Convert `### **Title**` to `### Title`
    content = re.sub(r"^(#+)\s*\*\*(.*?)\*\*\s*$", r"\1 \2", content, flags=re.MULTILINE)

    # Also standardize speaker bolding if needed, but previous check showed they were fine.

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Refined structure saved to: {output_path}")

if __name__ == "__main__":
    upgrade_headers()
