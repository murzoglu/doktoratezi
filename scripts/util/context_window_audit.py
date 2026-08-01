#!/usr/bin/env python3
"""Baglam-penceresi denetimi: her tez-sayisinin kaynak tam-metninde AYNI yapi/yon
icin gecip gecmedigini gorunur kilar.

Onceki tur (verify_claims_fulltext) yalniz substring varligini test ediyordu;
tesadufi eslesme (0,001 / %95 gibi yaygin degerler) yanlis-pozitif uretebilir.
Bu arac her hedef sayinin kaynak metindeki TUM gecislerinin +-cwin karakter
penceresini dumper -> Opus 4.8 elle baglam yargisi verebilir.

Cikti: JSON — her hedef icin {num: [pencere,...]}. KVKK: yalniz yayin metni.
"""
import json, os, re, sys, time

REPO = os.environ.get("CLAUDE_PROJECT_DIR", "/workspaces/T1DM-Tez")
sys.path.insert(0, os.path.join(REPO, "scripts", "mcp"))
import fulltext_cascade as FC
sys.path.insert(0, os.path.join(REPO, "scripts", "util"))
from verify_claims_fulltext import cascade, norm_variants

CWIN = 180


def windows(num, src, cwin=CWIN, maxhit=4):
    """Sayinin tum normalize varyantlari icin kaynak metinde pencere listesi."""
    outs, seen = [], set()
    for v in norm_variants(num):
        for m in re.finditer(r"(?<![\d])" + re.escape(v) + r"(?![\d])", src):
            a = max(0, m.start() - cwin)
            b = min(len(src), m.end() + cwin)
            w = re.sub(r"\s+", " ", src[a:b]).strip()
            key = w[:60]
            if key in seen:
                continue
            seen.add(key)
            outs.append({"variant": v, "window": w})
            if len(outs) >= maxhit:
                return outs
    return outs


def main():
    targets = json.load(open("/tmp/ctx_targets.json", encoding="utf-8"))
    results = []
    for i, t in enumerate(targets):
        src, layer = cascade(t.get("doi", ""), t.get("pmid", ""), t.get("key", ""))
        rec = {"key": t["key"], "layer": layer, "src_len": len(src), "nums": {}}
        for num in t["numbers"]:
            rec["nums"][num] = windows(num, src)
        results.append(rec)
        n_found = sum(1 for v in rec["nums"].values() if v)
        print("[%d/%d] %-30s layer=%-9s ctx-found=%d/%d" % (
            i + 1, len(targets), t["key"][:30], layer, n_found, len(t["numbers"])),
            file=sys.stderr)
        time.sleep(1.2)
    json.dump({"n": len(results), "results": results},
              open("/tmp/ctx_results.json", "w"), ensure_ascii=False, indent=2)
    print(json.dumps({"n": len(results)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
