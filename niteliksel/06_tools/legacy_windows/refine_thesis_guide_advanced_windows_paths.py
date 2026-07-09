import re

file_path = r"c:\Users\ozlem\OneDrive - marmara.edu.tr\Masaüstü\dökümler\tez_yazim_kilavuzu.md"

def refine_guide_advanced():
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Format URLs to Markdown links
    # Pattern: http://... or https://... -> [URL](URL)
    # Be careful not to double link if already linked (though unlikely in this raw file)
    url_pattern = r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'
    content = re.sub(url_pattern, r'[\1](\1)', content)

    # 2. Format Lists
    # Look for lines starting with "* " or "- " or specific patterns like "1. ", "2. " (that are not headers)
    # In this file, lists seem to be mostly implied by paragraphs.
    # However, lines 9-20 (Title page) and 269-281 (Cover page template) are lists of lines.
    # Let's fix the specific "Şekil 1.1" diagram text (lines ~49-59) to be a code block for clarity.

    diagram_start = "3 cm"
    diagram_end = "Şekil 1.1. Tezin yazılabileceği kâğıt boyutları ve kenar boşlukları."

    if diagram_start in content and diagram_end in content:
        # Regex to capture the block
        # We look for the block starting with "3 cm" and ending before "Şekil 1.1"
        pattern = r"(3 cm\s*\n\s*29,7 cm.*?)(Şekil 1.1)"
        replacement = r"```text\n\1```\n\2"
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # 3. Format References (Kaynaklar)
    # They usually look like: "Karolewicz B, ..." or "Underwood LE..."
    # We can indent them or put them as a list.
    # Let's try to detect lines that look like references in the references section.
    # The references section starts at "### 3.2.8. Kaynaklar"

    parts = content.split("### 3.2.8. Kaynaklar")
    if len(parts) > 1:
        pre_refs = parts[0]
        refs_part = parts[1]

        # In refs_part, we try to make lines that look like citations into a list.
        # But simply putting a "*" at start of paragraphs in this section might work best.
        # Check if next section exists: "### 3.2.9. Ekler"
        ref_sections = refs_part.split("### 3.2.9. Ekler")
        actual_refs = ref_sections[0]
        post_refs = "### 3.2.9. Ekler" + ref_sections[1] if len(ref_sections) > 1 else ""

        # Split actual_refs by double newlines to get blocks
        ref_blocks = actual_refs.split("\n\n")
        new_ref_blocks = []
        for block in ref_blocks:
            block = block.strip()
            if not block: continue
            # If it's a sub-header like "Orijinal makale:", keep it bold or specific
            if block.endswith(":") or block.lower() in ["tez:", "kitap:", "çeviri kitap:", "orijinal makale:", "resmi gazete’de yayınlanan yasa ve yönetmelikler:", "dergi eki (supplement):"]:
                new_ref_blocks.append(f"**{block}**")
            else:
                # Else assume it's a citation, make it a list item
                new_ref_blocks.append(f"* {block}")

        content = pre_refs + "### 3.2.8. Kaynaklar\n\n" + "\n\n".join(new_ref_blocks) + "\n\n" + post_refs

    # 4. Clean formatting for Title Page lines (Start of file)
    # Just wrap lines 3-13 in a blockquote or bold them?
    # Actually, Markdown just treats them as text. Let's make them bold for emphasis.
    # Target specific start lines.
    content = content.replace("TÜRKİYE CUMHURİYETİ", "**TÜRKİYE CUMHURİYETİ**")
    content = content.replace("MARMARA ÜNİVERSİTESİ", "**MARMARA ÜNİVERSİTESİ**")
    content = content.replace("SAĞLIK BİLİMLERİ ENSTİTÜSÜ", "**SAĞLIK BİLİMLERİ ENSTİTÜSÜ**")

    # 5. Fix bullet points that are plain text
    # e.g. "* Ailede Tip 1..." (lines 11-19 in step 290, but different file now)
    # The file "tez_yazim_kilavuzu.md" has lines like "1.1. Amaç..."
    # But let's look for manually typed bullets if any.
    # In step 322 view, look at lines 27-29. No obvious list there.
    # Look at step 322 lines 103-107: "21.1.1989...", "21.6.2002..." inside "Standart kısaltmalar..."
    # These should be list items.

    # Generic fix: double newlines to single if > 2
    content = re.sub(r"\n{3,}", "\n\n", content)

    # 6. Blockquote for the "BEYAN" text (lines ~307)
    # "Bu tez çalışmasının..."
    if "Bu tez çalışmasının kendi çalışmam olduğunu" in content:
        content = content.replace("Bu tez çalışmasının kendi çalışmam olduğunu", "> Bu tez çalışmasının kendi çalışmam olduğunu")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Advanced formatting applied.")

if __name__ == "__main__":
    refine_guide_advanced()
