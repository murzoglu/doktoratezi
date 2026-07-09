import re
import os

input_path = r"C:\Users\ozlem\OneDrive - marmara.edu.tr\Masaüstü\nitel ana.md"
output_dir = r"c:\Users\ozlem\OneDrive - marmara.edu.tr\Masaüstü\dökümler"
output_filename = "nitel_ana_duzenlenmis.md"
output_path = os.path.join(output_dir, output_filename)

def refine_markdown():
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove Empty Headers (## acting as spacers)
    # Replace "## \n" or "##\n" with nothing, or handle careful spacing
    content = re.sub(r"^##\s*$", "", content, flags=re.MULTILINE)

    # 2. Remove internal Notes
    # Remove (*burada düzelteme...*)
    content = re.sub(r"\(\*burada düzelteme.*?\*\)", "", content, flags=re.IGNORECASE)

    # Remove **YORUM: (TARTIŞMAYA ALINIR)** block and the duplicate text following it if it's identical
    # The duplicate text in the file (lines 515-517) repeats lines 513-514.
    # We can just remove the specific block starting with **YORUM: ...** until the end of that paragraph.
    # Regex to catch the specific comment block
    content = re.sub(r"\*\*YORUM:\s*\(TARTIŞMAYA ALINIR\)\*\*.*?(?=\n\n|\Z)", "", content, flags=re.DOTALL)

    # 3. Clean up specific typos
    # **(power dynamics).”** -> (power dynamics).
    content = content.replace("**(power dynamics).”**", "(power dynamics).")

    # Fix double dots ".. " -> ". " but be careful with ellipsis "..."
    # We will replace ".." with "." if it is NOT "..."
    # Negative lookahead/behind is useful here, or just simple replacement of ".." with "." and then fix "..." -> "..." handled by manual check or simple ignore if not frequent.
    # Actually, simpler distinct fixes are safer.
    content = content.replace(".. ", ". ")
    content = content.replace("? ..", "?")
    content = content.replace(".,", ",")
    content = content.replace(" .", ".")

    # Restore ellipsis if we broke them (e.g. . . . -> ...)
    content = content.replace(". . .", "...")

    # Fix spacing around parens "( text )" -> "(text)"
    content = re.sub(r"\(\s+", "(", content)
    content = re.sub(r"\s+\)", ")", content)

    # 4. Standardize Headers
    # Ensure all headings H1-H6 have one empty line before them.
    # Identify headers: ^#+
    lines = content.splitlines()
    refined_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # If line is header, ensure preceding empty line (unless it's the first line)
        if stripped.startswith("#"):
            if refined_lines and refined_lines[-1].strip() != "":
                refined_lines.append("")

        # Add the line
        refined_lines.append(line)

    content = "\n".join(refined_lines)

    # 5. Fix multiple empty lines (max 2)
    content = re.sub(r"\n{3,}", "\n\n", content)

    # 6. Specific fix for "Mellistus" or other typos if present (reusing knowledge from previous task)
    content = content.replace("Mellistus", "Mellitus")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Refined file saved to: {output_path}")

if __name__ == "__main__":
    refine_markdown()
