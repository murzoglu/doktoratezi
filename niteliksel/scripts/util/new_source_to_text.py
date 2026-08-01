#!/usr/bin/env python3
"""new/ docx+pdf -> düz metin (yerel, gitignored). KVKK: dış araca gitmez."""
import subprocess, pathlib
SRC = pathlib.Path(__file__).resolve().parents[2] / "new"
OUT = SRC / "_extracted"; OUT.mkdir(exist_ok=True)
for f in sorted(SRC.glob("*.docx")):
    subprocess.run(["pandoc", str(f), "-t", "plain", "-o", str(OUT / (f.stem + ".txt"))], check=True)
for f in sorted(SRC.glob("*.pdf")):
    subprocess.run(["pdftotext", str(f), str(OUT / (f.stem + ".txt"))], check=True)
print("OK ->", OUT)
