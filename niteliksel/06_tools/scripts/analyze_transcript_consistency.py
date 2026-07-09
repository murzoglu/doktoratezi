import re
from collections import Counter

input_file = "tum_dokumler.md"

def analyze_content():
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    speakers = Counter()
    typos = []

    # Regex to capture what looks like a speaker label (bolded or not, but we bolded them before)
    # Pattern: **Name:** or Name:
    speaker_pattern = re.compile(r"^\*\*?(.*?)\*\*?:")

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        match = speaker_pattern.match(line)
        if match:
            speaker_name = match.group(1).strip()
            speakers[speaker_name] += 1

        # Simple check for the specific typo seen in previous turns "Mellistus"
        if "Mellistus" in line:
            typos.append(f"Line {i+1}: Mellistus (Should be Mellitus)")

    print("--- SPEAKER LABELS FOUND ---")
    for speaker, count in sorted(speakers.items()):
        print(f"{count}x : {speaker}")

    print("\n--- POTENTIAL TYPOS ---")
    for typo in typos[:20]: # Show first 20
        print(typo)

    if len(typos) > 20:
        print(f"...and {len(typos) - 20} more.")

if __name__ == "__main__":
    analyze_content()
