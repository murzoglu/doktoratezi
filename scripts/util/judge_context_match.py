#!/usr/bin/env python3
"""Kademe 2: GPT-5.4 judge, tez cumlesi + sayilarin KAYNAK BAGLAM PENCERELERI ile.

Onceki judge turlari kaynak metnin ilk 6K'sini veriyordu. Bu tur, her hedef icin
ctx_results'tan cikan pencere metinlerini KANIT olarak toplayip judge'a verir; boylece
skorlar sayilarin GERCEK gectigi baglama dayanir (tesadufi substring degil).

Cikti: JSON — {key, score, mode, n_windows}.
"""
import json, os, sys
from pathlib import Path

REPO = os.environ.get("CLAUDE_PROJECT_DIR") or str(Path(__file__).resolve().parents[2])
sys.path.insert(0, os.path.join(REPO, "scripts", "eval"))
import galileo_bridge as G

ctx = json.load(open("/tmp/ctx_results.json"))["results"]
tgt = {(t["key"]): t for t in json.load(open("/tmp/ctx_targets.json"))}
# ayni key birden fazla cumlede olabilir -> ilk eslesen sent yeter (judge cümle-bazli)
sent_by_key = {}
for t in json.load(open("/tmp/ctx_targets.json")):
    sent_by_key.setdefault(t["key"], t["sent"])


def main():
    out = []
    for rec in ctx:
        k = rec["key"]
        # tum pencere metinlerini KANIT olarak birlestir
        wins = []
        for num, ws in rec["nums"].items():
            for w in ws:
                wins.append("[%s] %s" % (num, w["window"]))
        if not wins:
            out.append({"key": k, "score": None, "mode": "no-window",
                        "n_windows": 0, "layer": rec["layer"]})
            print("%-32s no-window (layer=%s)" % (k[:32], rec["layer"]), file=sys.stderr)
            continue
        evidence = "\n---\n".join(wins[:20])
        claim = sent_by_key.get(k, "")
        try:
            r = G.t_galileo_claim_source_match({"claim": claim, "source_text": evidence[:8000]})
            out.append({"key": k, "score": r.get("score"), "mode": r.get("mode"),
                        "n_windows": len(wins), "layer": rec["layer"]})
            print("%-32s score=%s n_win=%d" % (k[:32], r.get("score"), len(wins)),
                  file=sys.stderr)
        except Exception as e:
            out.append({"key": k, "score": None, "mode": "err:" + str(e)[:50],
                        "n_windows": len(wins), "layer": rec["layer"]})
            print("%-32s ERR %s" % (k[:32], str(e)[:50]), file=sys.stderr)
    scored = [o["score"] for o in out if isinstance(o.get("score"), (int, float))]
    summ = {"n": len(out), "scored": len(scored),
            "mean": round(sum(scored) / len(scored), 3) if scored else None,
            "min": min(scored) if scored else None,
            "max": max(scored) if scored else None,
            "below_065": [o["key"] for o in out if isinstance(o.get("score"), (int, float)) and o["score"] < 0.65]}
    json.dump({"summary": summ, "results": out},
              open("/tmp/judge_ctx.json", "w"), ensure_ascii=False, indent=2)
    print(json.dumps(summ, ensure_ascii=False))


if __name__ == "__main__":
    main()
