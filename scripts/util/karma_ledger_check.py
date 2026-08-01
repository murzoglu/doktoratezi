#!/usr/bin/env python3
"""Karma kanıt-ledger drift-guard.

Ledger'daki her ankrajın (`dosya#ankraj`) kaynak dosyada var olduğunu ve ilgili
verdikt/örüntü alıntısının kaynakta hâlâ geçtiğini doğrular. Ağsız, stdlib.

Exit: 0 temiz · 1 HARD (kayıp ankraj / kayıp dosya) · 2 SOFT (alıntı drift /
geçersiz ilişki türü). HARD, SOFT'a baskındır.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

_HERE = os.path.abspath(__file__)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
DEFAULT_LEDGER = "tez-yazim/05_entegrasyon/karma-kanit-ledgeri.tsv"
ILISKI_TURLERI = {"uyum", "tamamlayıcılık", "ayrışma", "açıklayıcı-genişleme"}
COLUMNS = [
    "id", "odak",
    "nicel_verdikt_ozet", "nicel_ankraj",
    "nitel_oruntu_ozet", "nitel_ankraj",
    "iliski_turu", "karma_yorum_siniri",
]

_WS = re.compile(r"\s+")


def _norm(text):
    return _WS.sub(" ", text).strip()


def parse_ledger(text):
    """TSV metnini satır sözlüklerine çevir. Başlık COLUMNS ile eşleşmeli."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        raise ValueError("ledger boş")
    header = lines[0].split("\t")
    if header != COLUMNS:
        raise ValueError(
            "ledger başlığı beklenen sütunlarla eşleşmiyor:\n"
            f"  beklenen: {COLUMNS}\n  bulunan:  {header}"
        )
    rows = []
    for i, ln in enumerate(lines[1:], start=2):
        cells = ln.split("\t")
        if len(cells) != len(COLUMNS):
            raise ValueError(f"satır {i}: {len(cells)} hücre, beklenen {len(COLUMNS)}")
        rows.append(dict(zip(COLUMNS, cells)))
    return rows


def _split_anchor(ref):
    """`dosya#ankraj` → (dosya, ankraj). Son `#` bölme noktasıdır."""
    if "#" not in ref:
        return ref, ""
    idx = ref.rfind("#")
    return ref[:idx], ref[idx + 1:]


def _get_semantic():
    """semantic_core'u tembel yükle (scripts/eval yolda değilse ekle).
    Testler bu fonksiyonu monkeypatch'ler."""
    evald = os.path.join(REPO_ROOT, "scripts", "eval")
    if evald not in sys.path:
        sys.path.insert(0, evald)
    import semantic_core  # noqa: PLC0415
    return semantic_core


def _best_window_sim(sc, ozet, text):
    """ozet ile kaynak pencereleri (paragraf) arası en yüksek cosine (tek embed çağrısı)."""
    wins = [w.strip() for w in re.split(r"\n\s*\n", text) if len(w.strip()) >= 20]
    if not wins:
        wins = [text]
    vecs = sc.embed([ozet] + [w[:2000] for w in wins])
    ov = vecs[0]
    return max(sc.cosine(ov, v) for v in vecs[1:])


def _semantic_drift_verdict(kol, ozet, text, rescue_min):
    """Substring-drift bulgusunu semantik rescue ile derecelendir.
    Dönen: (sev, msg). Parafraz-sadıksa INFO'ya indir; temellendirilmemişse SOFT;
    embedding yoksa SOFT + not (asla sessiz atlama / çökme)."""
    try:
        sc = _get_semantic()
        sim = _best_window_sim(sc, ozet, text)
        if sim >= rescue_min:
            return ("INFO", f"{kol}: parafraz-sadık (semantik≈{sim:.2f}); substring drift ama temellendirilmiş: {ozet[:40]!r}")
        return ("SOFT", f"{kol}: alıntı kaynakta geçmiyor (drift; semantik≈{sim:.2f}): {ozet[:40]!r}")
    except Exception as e:  # EmbeddingUnavailable dahil → deterministik SOFT'a düş
        return ("SOFT", f"{kol}: alıntı kaynakta geçmiyor (drift; semantik yok: {str(e)[:40]}): {ozet[:40]!r}")


def check(ledger_path, root=REPO_ROOT, semantic=False, rescue_min=0.75):
    """Ledger'ı doğrula → (severity, findings). severity: 0/1/2.

    semantic=True: substring-drift bulguları semantik rescue'dan geçer — parafraz-
    sadık özet INFO'ya iner (severity'yi yükseltmez), temellendirilmemiş SOFT kalır.
    Default False → davranış bit-aynı (offline, ağsız)."""
    with open(ledger_path, encoding="utf-8") as fh:
        rows = parse_ledger(fh.read())

    findings = []
    cache = {}

    def _load(rel):
        if rel not in cache:
            path = os.path.join(root, rel)
            cache[rel] = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        return cache[rel]

    for row in rows:
        rid = row["id"]
        if row["iliski_turu"] not in ILISKI_TURLERI:
            findings.append(("SOFT", rid, f"geçersiz ilişki türü: {row['iliski_turu']!r}"))
        for kol, ank_col, ozet_col in (
            ("nicel", "nicel_ankraj", "nicel_verdikt_ozet"),
            ("nitel", "nitel_ankraj", "nitel_oruntu_ozet"),
        ):
            rel, anchor = _split_anchor(row[ank_col])
            text = _load(rel)
            if text is None:
                findings.append(("HARD", rid, f"{kol}: kaynak dosya yok: {rel}"))
                continue
            if not anchor or ("{#" + anchor + "}") not in text:
                findings.append(("HARD", rid, f"{kol}: ankraj bulunamadı: #{anchor} ({rel})"))
            ozet = row[ozet_col].strip()
            if ozet and _norm(ozet) not in _norm(text):
                if semantic:
                    sev, msg = _semantic_drift_verdict(kol, ozet, text, rescue_min)
                    findings.append((sev, rid, msg))
                else:
                    findings.append(("SOFT", rid, f"{kol}: alıntı kaynakta geçmiyor (drift): {ozet[:40]!r}"))

    # severity yalnız HARD/SOFT'tan (INFO raporlanır ama kapıyı yükseltmez).
    if any(sev == "HARD" for sev, _, _ in findings):
        severity = 1
    elif any(sev == "SOFT" for sev, _, _ in findings):
        severity = 2
    else:
        severity = 0
    return severity, findings


def _render(severity, findings):
    label = {0: "TEMİZ", 1: "HARD", 2: "SOFT"}[severity]
    out = [f"karma-ledger-check: {label} ({len(findings)} bulgu)"]
    for sev, rid, msg in findings:
        out.append(f"  [{sev}] {rid}: {msg}")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Karma kanıt-ledger drift-guard")
    ap.add_argument("--ledger", default=os.path.join(REPO_ROOT, DEFAULT_LEDGER))
    ap.add_argument("--root", default=REPO_ROOT)
    ap.add_argument("--semantic", action="store_true",
                    help="substring-drift'i semantik rescue'dan geçir (parafraz-sadık=INFO)")
    ap.add_argument("--rescue-min", type=float, default=0.75)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    severity, findings = check(args.ledger, root=args.root,
                               semantic=args.semantic, rescue_min=args.rescue_min)
    if args.json:
        print(json.dumps(
            {"severity": severity,
             "findings": [{"sev": s, "id": i, "msg": m} for s, i, m in findings]},
            ensure_ascii=False, indent=2))
    else:
        print(_render(severity, findings))
    return severity


if __name__ == "__main__":
    sys.exit(main())
