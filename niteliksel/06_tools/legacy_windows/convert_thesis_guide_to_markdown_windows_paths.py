import os
from docx import Document

input_path = r"C:\Users\ozlem\OneDrive - marmara.edu.tr\Masaüstü\dökümler\tez yazim kılavuzu.docx"
output_path = r"C:\Users\ozlem\OneDrive - marmara.edu.tr\Masaüstü\dökümler\tez_yazim_kilavuzu.md"

def convert_docx_to_md():
    if not os.path.exists(input_path):
        print(f"Error: File not found at {input_path}")
        return

    try:
        doc = Document(input_path)
        content = []

        # Add title based on filename
        content.append(f"# Tez Yazım Kılavuzu\n")

        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                # Basic header detection based on style or just bold logic could be added,
                # but for now, we'll keep it simple as plain text paragraphs.
                # If the user wants better formatting later, we can refine it.
                content.append(text + "\n")

        markdown_text = "\n".join(content)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_text)

        print(f"Successfully converted to: {output_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    convert_docx_to_md()
