import os
import glob
import sys

try:
    from docx import Document
except ImportError:
    print("Error: python-docx library is not installed.")
    print("Please run: pip install python-docx")
    sys.exit(1)

def convert_docx_to_md():
    output_file = "tum_dokumler.md"
    # Find all docx files in current directory
    docx_files = glob.glob("*.docx")

    if not docx_files:
        print("No .docx files found in the current directory.")
        return

    print(f"Found {len(docx_files)} .docx files.")

    with open(output_file, "w", encoding="utf-8") as md_file:
        for docx_file in docx_files:
            print(f"Converting: {docx_file}")

            # Write filename as a header
            md_file.write(f"# {docx_file}\n\n")

            try:
                doc = Document(docx_file)
                for para in doc.paragraphs:
                    text = para.text.strip()
                    if text:
                        # Simple markdown conversion: just preserving paragraphs
                        md_file.write(f"{text}\n\n")

                # Add a separator between files
                md_file.write("---\n\n")

            except Exception as e:
                error_msg = f"Error reading {docx_file}: {str(e)}"
                print(error_msg)
                md_file.write(f"> {error_msg}\n\n")

    print(f"Values have been collected in {output_file}")

if __name__ == "__main__":
    convert_docx_to_md()
