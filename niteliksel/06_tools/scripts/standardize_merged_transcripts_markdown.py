import re

input_file = "tum_dokumler.md"
output_file = "tum_dokumler_standardize.md"

def standardize_content():
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Global Typo Fixes
    # Fix "Mellistus" -> "Mellitus"
    content = content.replace("Mellistus", "Mellitus")

    # Fix "Diaybet" -> "Diyabet"
    content = content.replace("Diaybet", "Diyabet")

    # Fix "Dİyabet" -> "Diyabet" (Capital I dot issue if any)
    content = content.replace("Dİyabet", "Diyabet")

    lines = content.splitlines()
    refined_lines = []

    # Regex for Speaker Labels
    # Captures: "**11 numaralı ... :**" or variations
    # We want to standardize to: "**{Number} numaralı Tip 1 Diyabet Mellitus Hastası{Suffix}:**"

    # Matching pattern: starts with ** or nothing, digit, "numaralı" or "no", then text, then : or :**
    # Example: **11 numaralı Tip 1 Diyabet Mellitus Hastasının Kardeşi:**

    speaker_regex = re.compile(r"^\*\*?(\d+)\s*(?:numaralı|no|nolu)\s*Tip\s*1\s*Diyabet\s*Mellitus\s*Hastası(.*?)\*\*?:", re.IGNORECASE)

    for line in lines:
        match = speaker_regex.match(line)
        if match:
            number = match.group(1)
            suffix = match.group(2).strip() # e.g. "nın Kardeşi" or empty or "nın Annesi"

            # Normalize suffix if needed (e.g. remove extra spaces)
            # If suffix is empty, it means just "Hastası"

            # Reconstruct standard label
            # Using "numaralı" as it seems most formal and common in the file
            new_label = f"**{number} numaralı Tip 1 Diyabet Mellitus Hastası{suffix}:**"

            # Append the rest of the line (content)
            # The regex matched the label including the colon.
            # We need to find where the match ended in the original line to get the rest.
            # actually regex match gives the span.
            rest_of_line = line[match.end():].strip()

            refined_lines.append(f"{new_label} {rest_of_line}")
        else:
            # Check for "Doktor" formatting consistency
            if re.match(r"^\*\*?Doktor\*\*?:", line, re.IGNORECASE):
                rest = re.sub(r"^\*\*?Doktor\*\*?:\s*", "", line, flags=re.IGNORECASE)
                refined_lines.append(f"**Doktor:** {rest}")
            else:
                refined_lines.append(line)

    final_content = "\n".join(refined_lines)

    with open(input_file, "w", encoding="utf-8") as f:
        f.write(final_content)

    print(f"Standardized content saved to {input_file}")

if __name__ == "__main__":
    standardize_content()
