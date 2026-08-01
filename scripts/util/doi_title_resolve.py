#!/usr/bin/env python3
"""DOI -> Crossref baslik cozunurlugu ile yanlis-atif denetimi.

Her bib anahtari icin: bibteki title ile DOI'nin Crossref'te cozdugu gercek
title'i token-Jaccard benzerligiyle karsilastirir. Dusuk benzerlik = potansiyel
yanlis-atif (DOI baska esere isaret ediyor).

Cikti: JSON — {key, doi, bib_title, crossref_title, jaccard, flag}.
KVKK: yalniz yayin metadata (baslik) sorgulanir.
"""
import json, os, re, sys, time, urllib.request

REPO = os.environ.get("CLAUDE_PROJECT_DIR", "/workspaces/T1DM-Tez")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36 (mailto:tez@local)")


def norm(t):
    t = re.sub(r"\{|\}", "", t or "")
    t = re.sub(r"[^\w\s]", " ", t.lower())
    return set(w for w in t.split() if len(w) > 2)


def jaccard(a, b):
    A, B = norm(a), norm(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def crossref_title(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=30))
        t = d["message"].get("title", [""])
        return t[0] if t else ""
    except Exception as e:
        return "ERR:" + str(e)[:50]


def main():
    targets = json.load(open("/tmp/ctx_targets.json", encoding="utf-8"))
    bib = open(os.path.join(REPO, "references", "references.bib"), encoding="utf-8").read()

    def bibtitle(key):
        m = re.search(r"@\w+\{" + re.escape(key) + r",(.*?)\n\}", bib, re.S)
        if not m:
            return ""
        mm = re.search(r"title\s*=\s*[{\"](.+?)[}\"]\s*,?\s*\n", m.group(1), re.S)
        return mm.group(1) if mm else ""

    seen, out = set(), []
    for t in targets:
        k = t["key"]
        if k in seen or not t.get("doi"):
            continue
        seen.add(k)
        bt = bibtitle(k)
        ct = crossref_title(t["doi"])
        j = jaccard(bt, ct) if not ct.startswith("ERR") else None
        flag = "OK" if (j is not None and j >= 0.4) else (
            "CHECK" if j is not None else "CROSSREF_ERR")
        out.append({"key": k, "doi": t["doi"], "bib_title": bt[:80],
                    "crossref_title": ct[:80], "jaccard": round(j, 3) if j is not None else None,
                    "flag": flag})
        print("%-34s j=%s %-6s %s" % (k[:34], j, flag, ct[:55]), file=sys.stderr)
        time.sleep(0.6)
    json.dump({"n": len(out), "results": out},
              open("/tmp/doi_resolve.json", "w"), ensure_ascii=False, indent=2)
    flags = [o for o in out if o["flag"] != "OK"]
    print(json.dumps({"n": len(out), "non_ok": len(flags),
                      "flagged": [f["key"] for f in flags]}, ensure_ascii=False))


if __name__ == "__main__":
    import urllib.parse
    main()
