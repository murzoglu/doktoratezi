#!/usr/bin/env python3
"""Tezden atıf-bağlı sayısal/olgusal iddiaları çıkarır.

Bir cümle hem [@key] atıfı hem de sayısal örüntü (%, oran, etki büyüklüğü, n, GA)
içeriyorsa "doğrulanabilir dış-kaynak iddiası" adayıdır. Bu, tam-metin doğrulaması
gereken iddialar kümesidir (iç istatistik çıktıları hariç: onlar CSR trace kapsamı).

Çıktı: JSON — [{file, sentence, keys[], numbers[]}].
"""
import json, os, re, sys

REPO = os.environ.get("CLAUDE_PROJECT_DIR", "/workspaces/T1DM-Tez")
CH = os.path.join(REPO, "chapters")

# Sadece dış-literatür iddialarının bulunduğu bölümler (bulgular = kendi verimiz).
FILES = ["01_giris_ve_amac.qmd", "02_genel_bilgiler.qmd",
         "03_gerec_ve_yontem.qmd", "05_tartisma_ve_sonuc.qmd"]

CITE = re.compile(r"\[@[^\]]+\]")
KEY = re.compile(r"@([A-Za-z0-9_:\-]+)")
# sayısal örüntüler: %12,3 / 12,3 / 0,40 / g=0,39 / n=51 / d = 0,38 / binde/yüz binde
NUM = re.compile(
    r"(%\s?\d[\d.,]*"
    r"|\b(?:g|d|r|β|OR|HR|RR|Mz|M|SD)\s?[=<>≈]\s?-?\d[\d.,]*"
    r"|\bn\s?=\s?\d[\d.,]*"
    r"|\byüz\s?binde\s?\d[\d.,]*|\bbinde\s?\d[\d.,]*"
    r"|\b\d{1,3}(?:\.\d{3})+\b"       # binlik ayraçlı büyük sayı (108.300)
    r"|\b\d+[,.]\d+\b)"               # ondalık
)


def strip_fences(txt):
    out, infence = [], False
    for l in txt.splitlines():
        if l.lstrip().startswith("```"):
            infence = not infence
            continue
        if not infence:
            out.append(l)
    return "\n".join(out)


def sentences(txt):
    # paragrafları koru, cümleye böl
    txt = re.sub(r"\s+", " ", txt)
    return re.split(r"(?<=[.!?])\s+", txt)


def main():
    claims = []
    for f in FILES:
        p = os.path.join(CH, f)
        if not os.path.exists(p):
            continue
        body = strip_fences(open(p, encoding="utf-8").read())
        for s in sentences(body):
            if not CITE.search(s):
                continue
            nums = NUM.findall(s)
            # NUM grupları tuple dönebilir -> düzleştir
            flat = []
            for m in NUM.finditer(s):
                flat.append(m.group(0).strip())
            if not flat:
                continue
            keys = KEY.findall(s)
            # § bölüm referanslarını ve saf yıl atıflarını sayı olarak sayma
            flat = [x for x in flat if not re.fullmatch(r"\d{4}", x)]
            flat = [x for x in flat if x]
            if not flat:
                continue
            claims.append({
                "file": f,
                "keys": sorted(set(keys)),
                "numbers": flat,
                "sentence": s.strip()[:500],
            })
    print(json.dumps({"n": len(claims), "claims": claims}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
