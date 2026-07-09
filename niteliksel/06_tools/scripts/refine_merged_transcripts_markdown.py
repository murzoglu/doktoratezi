import re

input_file = "tum_dokumler.md"
output_file = "tum_dokumler_duzenlenmis.md"

def refine_markdown():
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    refined_lines = []

    # Regex to identify speaker labels (e.g., "Doktor:", "11 numaralı ... Hastası:")
    # We look for lines starting with a capital letter or number, followed by text, ending with a colon.
    speaker_pattern = re.compile(r"^(\d+\s+numaralı.*?|Doktor|[\w\s]+):", re.IGNORECASE)

    for line in lines:
        line = line.strip()

        # Skip empty lines, we will manage spacing manually or keep them if just one
        if not line:
            refined_lines.append("")
            continue

        # Check for speaker pattern
        match = speaker_pattern.match(line)
        if match:
            # Bold the speaker part
            speaker = match.group(0)
            rest = line[len(speaker):].strip()
            # refined_line = f"**{speaker}** {rest}"
            # Actually, let's keep the colon inside the bold or outside? usually inside is fine "Doktor:" -> "**Doktor:**"
            refined_line = f"**{speaker}** {rest}"
        else:
            refined_line = line

        # Fix capitalization or common issues if any (basic cleanup)
        # e.g. fix spacing inside parens "( text )" -> "(text)"
        refined_line = re.sub(r"\(\s+", "(", refined_line)
        refined_line = re.sub(r"\s+\)", ")", refined_line)

        refined_lines.append(refined_line)

    # Reassemble with proper spacing (max 2 newlines)
    final_content = "\n".join(refined_lines)
    final_content = re.sub(r"\n{3,}", "\n\n", final_content)

    with open(input_file, "w", encoding="utf-8") as f:
        f.write(final_content)

    print(f"Refined content saved to {input_file}")

if __name__ == "__main__":
    refine_markdown()
