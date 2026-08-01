#!/usr/bin/env python3
"""Birleşik claim-sertifikasyon kapısı — dört denetçiyi tek karara indirger.

Bu kapı, tez/CSR metnindeki iddiaların yayına hazırlık düzeyini tek bir
PASS/WARN/FAIL kararında toplar. Dört bağımsız katmanı orkestre eder:

  1. csr_numeric_trace_audit — sayısal iddiaların üretilmiş CSV'lere izlenmesi
     (high-risk unmatched = kaynaksız sayı riski).
  2. csr_causal_label_audit — nedensel dil disiplini + keşifsel/post-hoc etiket
     bütünlüğü (H1-H4 doğrulayıcı hattında yanlış nedensellik = revize).
  3. galileo_judge (opsiyonel, --with-judge) — bağımsız GPT-5.4 groundedness/
     halüsinasyon ikinci-görüşü; örneklenmiş yüksek-riskli iddialarda.
  4. bib_hygiene — atıf↔künye↔ledger mutabakatı + DOI/PMID sağlığı; tanımsız
     atıf render'ı kırar (HARD).

KVKK: Tüm katmanlar yalnız türetilmiş/metin düzeyinde çalışır; satır düzeyi
katılımcı verisi okunmaz, dışarı gönderilmez. galileo_judge yalnız yayımlanmış
literatür/metin parçalarını dış servise iletir.

Karar mantığı:
  FAIL  — bib HARD (tanımsız atıf) VEYA causal_revise>0 VEYA judge halüsinasyon.
  WARN  — high-risk unmatched sayı, causal_review, label_error/review, bib SOFT.
  PASS  — hepsi temiz.

Çıkış kodu: 0=PASS, 2=WARN, 1=FAIL (render-kırıcı). CI'de 1 bloklar, 2 uyarır.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UTIL = ROOT / "scripts" / "util"
GALILEO = ROOT / "scripts" / "eval" / "galileo_bridge.py"
PROTO = "2025-06-18"

# WARN/FAIL eşikleri — doktrin ile hizalı, --strict ile sıkılaştırılabilir.
DEFAULT_THRESHOLDS = {
    "high_risk_unmatched_warn": 1,      # ≥1 kaynaksız yüksek-risk sayı → WARN
    "high_risk_unmatched_fail": 250,    # aşırı yüksek → FAIL (regresyon koruması)
    "causal_revise_fail": 1,            # H1-H4'te nedensel revize → FAIL
    "causal_review_warn": 1,            # nedensel gözden-geçir → WARN
    "label_error_fail": 1,              # keşifsel etiket hatası → FAIL
    "judge_hallucination_fail": 0.5,    # judge halüsinasyon riski ≥ eşik → FAIL
    "judge_groundedness_warn": 0.7,     # groundedness < eşik → WARN
}


def _load_dotenv() -> None:
    envf = ROOT / ".env"
    if not envf.exists():
        return
    for line in envf.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _run(cmd: list[str], timeout: int = 150) -> tuple[int, str, str]:
    env = dict(os.environ)
    env["CLAUDE_PROJECT_DIR"] = str(ROOT)
    try:
        p = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, cwd=str(ROOT), env=env
        )
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except Exception as e:  # noqa: BLE001
        return 125, "", "%s: %s" % (type(e).__name__, str(e)[:160])


def _parse_kv(text: str) -> dict:
    """`k=v` token'larını sözlüğe çevir (int'e zorla, olmazsa string).

    Denetçiler tek satırda birden çok `k=v` basabilir
    (ör. `claims=394 traced_all=250 partial=117`), bu yüzden satır değil
    boşlukla ayrık token bazında ayrıştırılır. Yol içeren değerler
    (ör. `report=outputs/...`) string kalır.
    """
    out: dict = {}
    for tok in text.split():
        if "=" not in tok:
            continue
        k, v = tok.split("=", 1)
        k = k.strip()
        if not k:
            continue
        try:
            out[k] = int(v)
        except ValueError:
            out[k] = v
    return out


# ---------- katman 1: sayısal iz ----------
def layer_numeric(csr: str) -> dict:
    rc, out, err = _run([sys.executable, str(UTIL / "csr_numeric_trace_audit.py"), "--csr", csr])
    kv = _parse_kv(out)
    return {
        "ok": rc == 0,
        "claims": kv.get("claims", 0),
        "traced_all": kv.get("traced_all", 0),
        "partial": kv.get("partial", 0),
        "untraced": kv.get("untraced", 0),
        "high_risk_unmatched": kv.get("high_risk_unmatched", 0),
        "numbers_unmatched": kv.get("numbers_unmatched", 0),
        "raw_rc": rc,
        "err": err.strip()[:200] if rc != 0 else "",
    }


# ---------- katman 2: nedensel dil + etiket ----------
def layer_causal(csr: str) -> dict:
    rc, out, err = _run([sys.executable, str(UTIL / "csr_causal_label_audit.py"), "--csr", csr])
    kv = _parse_kv(out)
    return {
        "ok": rc == 0,
        "causal_rows": kv.get("causal_rows", 0),
        "causal_revise": kv.get("causal_revise", 0),
        "causal_review": kv.get("causal_review", 0),
        "label_rows": kv.get("label_rows", 0),
        "label_errors": kv.get("label_errors", 0),
        "label_reviews": kv.get("label_reviews", 0),
        "raw_rc": rc,
        "err": err.strip()[:200] if rc != 0 else "",
    }


# ---------- katman 4: bib hijyen ----------
def layer_bib() -> dict:
    rc, out, err = _run([sys.executable, str(UTIL / "bib_hygiene.py"), "all", "--json"])
    try:
        d = json.loads(out)
    except (json.JSONDecodeError, ValueError):
        return {"ok": False, "err": (err or out)[:200], "hard": [], "soft_fields": 0}
    rec = d.get("reconcile", {})
    ids = d.get("ids", {})
    return {
        "ok": True,
        "undefined": rec.get("undefined", []),      # HARD — render kırar
        "orphan": len(rec.get("orphan", [])),
        "soft_fields": len(d.get("fields", [])),
        "missing_doi": len(ids.get("missing_doi", [])),
        "bad_doi": len(ids.get("bad_doi", [])),
        "dup_doi": len(ids.get("dup_doi", [])),
        "dedup": len(d.get("dedup", [])),
    }


# ---------- katman 3: galileo judge (opsiyonel) ----------
def _galileo_judge(text: str, evidence: str, section_type: str = "genel") -> dict | None:
    """galileo_bridge.py'yi stdio MCP olarak çağır; judge skorlarını döndür."""
    if not GALILEO.exists():
        return None
    env = dict(os.environ)
    env["CLAUDE_PROJECT_DIR"] = str(ROOT)
    lines = [
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                    "params": {"protocolVersion": PROTO, "capabilities": {},
                               "clientInfo": {"name": "claim-cert", "version": "1.0"}}}),
        json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                    "params": {"name": "galileo_judge",
                               "arguments": {"text": text, "evidence": evidence,
                                             "section_type": section_type}}}),
    ]
    try:
        p = subprocess.run(
            [sys.executable, str(GALILEO)],
            input="\n".join(lines) + "\n",
            capture_output=True, text=True, timeout=120, env=env,
        )
    except Exception:  # noqa: BLE001
        return None
    for line in p.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            d = json.loads(line, strict=False)
        except json.JSONDecodeError:
            continue
        if d.get("id") == 2:
            c = d.get("result", {}).get("content", [])
            if c:
                try:
                    return json.loads(c[0].get("text", "{}"))
                except json.JSONDecodeError:
                    return None
    return None


def layer_judge(sample: list[dict], th: dict) -> dict:
    """Örneklenmiş yüksek-riskli iddialarda judge ikinci-görüşü.

    sample: [{"text":..,"evidence":..,"section_type":..}]
    """
    _load_dotenv()
    results, worst_hall, min_ground = [], 0.0, 1.0
    for item in sample:
        j = _galileo_judge(item.get("text", ""), item.get("evidence", ""),
                           item.get("section_type", "genel"))
        if not j:
            continue
        sc = j.get("scores", j)
        hall = _numf(sc.get("hallucination_risk"), 0.0)
        ground = _numf(sc.get("groundedness"), 1.0)
        worst_hall = max(worst_hall, hall)
        min_ground = min(min_ground, ground)
        results.append({
            "text": item.get("text", "")[:80],
            "hallucination_risk": hall,
            "groundedness": ground,
        })
    return {
        "ok": bool(results),
        "n": len(results),
        "worst_hallucination": round(worst_hall, 3),
        "min_groundedness": round(min_ground, 3),
        "results": results,
    }


def _numf(x, default: float) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def _judge_sample_from_scan(limit: int = 6) -> list[dict]:
    """Nedensel-tarama CSV'sinden yüksek-riskli (revise/review) excerpt'ler örnekle.

    Sadece CSR metin excerpt'i ve tespit edilen desen (evidence olarak) iletilir;
    satır düzeyi katılımcı verisi yoktur.
    """
    scan = ROOT / "outputs" / "tables" / "csr_causal_language_scan.csv"
    if not scan.exists():
        return []
    picks: list[dict] = []
    try:
        with scan.open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except OSError:
        return []
    # revise'ları önceliklendir, sonra review.
    ordered = [r for r in rows if r.get("adjudication") == "revise"] + \
        [r for r in rows if r.get("adjudication") == "review"]
    for r in ordered[:limit]:
        exc = (r.get("excerpt") or "").strip()
        if not exc:
            continue
        picks.append({
            "text": exc,
            "evidence": "tespit edilen desen: %s | bölüm=%s | rationale: %s" % (
                r.get("patterns", ""), r.get("section", ""), (r.get("rationale") or "")[:120]),
            "section_type": "tartisma" if "discussion" in (r.get("scope") or "") else "sonuclar",
        })
    return picks


# ---------- karar toplayıcı ----------
def certify(csr: str, with_judge: bool, strict: bool, th: dict) -> dict:
    layers = {
        "numeric": layer_numeric(csr),
        "causal": layer_causal(csr),
        "bib": layer_bib(),
    }
    fails: list[str] = []
    warns: list[str] = []

    num = layers["numeric"]
    if not num["ok"]:
        fails.append("numeric denetçi çalışmadı (rc=%s)" % num.get("raw_rc"))
    hr = num.get("high_risk_unmatched", 0)
    if hr >= th["high_risk_unmatched_fail"]:
        fails.append("high-risk kaynaksız sayı=%d (≥%d)" % (hr, th["high_risk_unmatched_fail"]))
    elif hr >= th["high_risk_unmatched_warn"]:
        warns.append("high-risk kaynaksız sayı=%d" % hr)

    cau = layers["causal"]
    if not cau["ok"]:
        fails.append("causal denetçi çalışmadı (rc=%s)" % cau.get("raw_rc"))
    if cau.get("causal_revise", 0) >= th["causal_revise_fail"]:
        fails.append("H1-H4 nedensel-revize=%d" % cau["causal_revise"])
    if cau.get("label_errors", 0) >= th["label_error_fail"]:
        fails.append("keşifsel-etiket hatası=%d" % cau["label_errors"])
    if cau.get("causal_review", 0) >= th["causal_review_warn"]:
        warns.append("nedensel-gözden-geçir=%d" % cau["causal_review"])
    if cau.get("label_reviews", 0):
        warns.append("etiket-gözden-geçir=%d" % cau["label_reviews"])

    bib = layers["bib"]
    if not bib["ok"]:
        fails.append("bib denetçi çalışmadı: %s" % bib.get("err", ""))
    if bib.get("undefined"):
        fails.append("tanımsız atıf (render kırar): %s" % ", ".join(bib["undefined"][:5]))
    soft = bib.get("soft_fields", 0) + bib.get("missing_doi", 0) + bib.get("bad_doi", 0) + \
        bib.get("dup_doi", 0) + bib.get("dedup", 0)
    if soft:
        warns.append("bib SOFT sorun=%d (alan/DOI/duplikat)" % soft)

    if with_judge:
        sample = _judge_sample_from_scan()
        layers["judge"] = layer_judge(sample, th)
        j = layers["judge"]
        if j.get("ok"):
            if j.get("worst_hallucination", 0.0) >= th["judge_hallucination_fail"]:
                fails.append("judge halüsinasyon riski=%.2f (≥%.2f)" % (
                    j["worst_hallucination"], th["judge_hallucination_fail"]))
            if j.get("min_groundedness", 1.0) < th["judge_groundedness_warn"]:
                warns.append("judge groundedness=%.2f (<%.2f)" % (
                    j["min_groundedness"], th["judge_groundedness_warn"]))

    # strict modda WARN'lar da FAIL sayılır (yayın-öncesi son kapı).
    verdict = "PASS"
    if fails:
        verdict = "FAIL"
    elif warns:
        verdict = "FAIL" if strict else "WARN"

    return {
        "verdict": verdict,
        "csr": csr,
        "strict": strict,
        "with_judge": with_judge,
        "fails": fails,
        "warns": warns,
        "layers": layers,
    }


def _render(pkg: dict) -> str:
    v = pkg["verdict"]
    icon = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}[v]
    lines = ["# Claim Sertifikasyon Raporu", ""]
    lines.append("**Karar:** %s %s%s" % (icon, v, " (strict)" if pkg["strict"] else ""))
    lines.append("**CSR:** %s" % pkg["csr"])
    lines.append("")

    n = pkg["layers"]["numeric"]
    lines.append("## 1. Sayısal İz (csr_numeric_trace)")
    lines.append("- iddia=%d · tam-izli=%d · kısmi=%d · izsiz=%d" % (
        n.get("claims", 0), n.get("traced_all", 0), n.get("partial", 0), n.get("untraced", 0)))
    lines.append("- high-risk kaynaksız sayı=%d · eşleşmeyen sayı=%d" % (
        n.get("high_risk_unmatched", 0), n.get("numbers_unmatched", 0)))

    c = pkg["layers"]["causal"]
    lines.append("")
    lines.append("## 2. Nedensel Dil + Etiket (csr_causal_label)")
    lines.append("- nedensel satır=%d · revize=%d · gözden-geçir=%d" % (
        c.get("causal_rows", 0), c.get("causal_revise", 0), c.get("causal_review", 0)))
    lines.append("- etiket satır=%d · hata=%d · gözden-geçir=%d" % (
        c.get("label_rows", 0), c.get("label_errors", 0), c.get("label_reviews", 0)))

    b = pkg["layers"]["bib"]
    lines.append("")
    lines.append("## 3. Bib Hijyen (bib_hygiene)")
    lines.append("- tanımsız atıf (HARD)=%d · orphan=%d" % (
        len(b.get("undefined", [])), b.get("orphan", 0)))
    lines.append("- SOFT: alan-eksik=%d · DOI-eksik=%d · bozuk-DOI=%d · dup-DOI=%d · yakın-dup=%d" % (
        b.get("soft_fields", 0), b.get("missing_doi", 0), b.get("bad_doi", 0),
        b.get("dup_doi", 0), b.get("dedup", 0)))

    if "judge" in pkg["layers"]:
        j = pkg["layers"]["judge"]
        lines.append("")
        lines.append("## 4. Galileo Judge (ikinci-görüş)")
        lines.append("- örneklenen=%d · en-kötü-halüsinasyon=%.3f · en-düşük-groundedness=%.3f" % (
            j.get("n", 0), j.get("worst_hallucination", 0.0), j.get("min_groundedness", 1.0)))

    if pkg["fails"]:
        lines.append("")
        lines.append("## ❌ FAIL Nedenleri")
        lines += ["- %s" % f for f in pkg["fails"]]
    if pkg["warns"]:
        lines.append("")
        lines.append("## ⚠️ WARN Nedenleri")
        lines += ["- %s" % w for w in pkg["warns"]]
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csr", default="docs/CLINICAL-STUDY-REPORT-FINAL.md")
    ap.add_argument("--with-judge", action="store_true",
                    help="Galileo GPT judge ikinci-görüşünü ekle (ağ + API gerektirir)")
    ap.add_argument("--strict", action="store_true",
                    help="WARN'ları da FAIL say (yayın-öncesi son kapı)")
    ap.add_argument("--json", action="store_true", help="ham JSON çıktı")
    ap.add_argument("--out", help="markdown rapor yolu")
    args = ap.parse_args()

    th = dict(DEFAULT_THRESHOLDS)
    pkg = certify(args.csr, args.with_judge, args.strict, th)

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(_render(pkg), encoding="utf-8")
    if args.json:
        print(json.dumps(pkg, ensure_ascii=False, indent=2))
    else:
        print(_render(pkg))

    return {"PASS": 0, "WARN": 2, "FAIL": 1}[pkg["verdict"]]


if __name__ == "__main__":
    raise SystemExit(main())
