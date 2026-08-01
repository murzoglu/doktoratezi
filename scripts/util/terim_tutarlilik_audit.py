#!/usr/bin/env python3
"""Terim tutarlılık denetçisi — kanonik terim sözlüğü zorlaması.

`docs/tez-kilavuz/terim-sozlugu.yaml` kanonik sözlüğünü okur ve `chapters/*.qmd`
gövdesinde her `yasak_varyantlar` kaydını tarar. Muafiyet dışı her bulgu
`zorlama: hard` girişlerinde HARD (teslim engeli), aksi hâlde INFO üretir.

Tasarım ilkesi (docs/tez-kilavuz/ONERI_terim-sozlugu-ve-denetim-tasarimi.md):
mevcut `tr_corpus_audit.py` primitive'lerini (strip_fenced, tr_lower,
_strip_citations) YENİDEN KULLANIR — kopyalamaz. Yeni paralel sistem kurmaz.

Muafiyet katmanları (yalancı-pozitif önleme):
  1. global dosya öneki      — İngilizce özet (00c) tamamen muaf
  2. bölüm başlığı           — # SUMMARY / # ABSTRACT sonrası metin muaf
  3. kod-çiti / HTML-yorum   — strip_fenced ile zaten dışlanır
  4. atıf                    — [@key]/@key _strip_citations ile temizlenir
  5. ilk-geçiş parantezi     — "kanonik (*ingilizce*)" muaf (İng. terim tanıtımı)
  6. bağlamsal_muafiyet      — terime özgü regex (ör. gizli=confounder, Dirik terimi)

Salt-okuma: hiçbir tez dosyasını değiştirmez. Sayı/istatistik/atıf/yön kararına
DOKUNMAZ; yalnız terim-dili biçimini denetler.

Exit: 0 = HARD bulgu yok · 1 = ≥1 HARD bulgu (muafiyet dışı yasak varyant).
"""
from __future__ import annotations

import argparse
import glob as _glob
import os
import pathlib
import re
import sys

# tr_corpus_audit primitive'lerini yeniden kullan (kopyalama yok).
_HERE = os.path.abspath(__file__)
_UTIL = os.path.dirname(_HERE)
if _UTIL not in sys.path:
    sys.path.insert(0, _UTIL)
from tr_corpus_audit import (  # noqa: E402
    _strip_citations,
    strip_fenced,
    tr_lower,
)

REPO_ROOT = os.path.dirname(os.path.dirname(_UTIL))
DEFAULT_SOZLUK = "docs/tez-kilavuz/terim-sozlugu.yaml"
DEFAULT_CHAPTERS = ["chapters/*.qmd"]


# ---------------------------------------------------------------------------
# Sözlük yükleme — PyYAML varsa onu, yoksa gömülü mini-parser'ı kullan.
# terim-sozlugu.yaml düzenli biçimde tutulur (inline liste, sabit girinti) ki
# her iki yol da aynı sonucu versin.
# ---------------------------------------------------------------------------

def load_sozluk(path: str) -> dict:
    text = pathlib.Path(path).read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return _mini_yaml(text)


def _mini_yaml(text: str) -> dict:
    """terim-sozlugu.yaml şemasına özel gömülü ayrıştırıcı (PyYAML yoksa).

    Desteklenen: yorum/boş satır atlanır; top-level `key:` mapping ve `key:` list;
    2-boşluk girintili mapping; `- key: val` liste öğesi; inline `[a, b]` liste;
    tırnaklı/tırnaksız skaler. Yalnız bu dosyanın (düzenli) biçimi için yeterlidir.
    """
    global_muafiyet: dict = {}
    terimler: list[dict] = []
    section = None            # "global_muafiyet" | "terimler"
    cur: dict | None = None

    for raw in text.splitlines():
        line = raw.split(" #", 1)[0].rstrip() if not raw.lstrip().startswith("#") else ""
        if not line.strip():
            continue
        # top-level anahtar (girintisiz)
        if re.match(r"^[A-Za-z_]\w*:", line):
            key = line.split(":", 1)[0].strip()
            rest = line.split(":", 1)[1].strip()
            if key == "global_muafiyet":
                section, cur = "global_muafiyet", None
            elif key == "terimler":
                section, cur = "terimler", None
            else:
                section, cur = None, None
            if rest:  # top-level skaler (bu şemada yok ama tolere et)
                pass
            continue
        if section == "global_muafiyet":
            m = re.match(r"^\s+([A-Za-z_]\w*):\s*(.*)$", line)
            if m:
                global_muafiyet[m.group(1)] = _scalar(m.group(2))
            continue
        if section == "terimler":
            m_item = re.match(r"^\s*-\s+([A-Za-z_]\w*):\s*(.*)$", line)
            if m_item:
                cur = {}
                terimler.append(cur)
                cur[m_item.group(1)] = _scalar(m_item.group(2))
                continue
            m_kv = re.match(r"^\s+([A-Za-z_]\w*):\s*(.*)$", line)
            if m_kv and cur is not None:
                cur[m_kv.group(1)] = _scalar(m_kv.group(2))
            continue
    return {"global_muafiyet": global_muafiyet, "terimler": terimler}


def _scalar(v: str):
    """Tırnaklı/tırnaksız skaler ya da inline liste `[a, "b"]` çöz."""
    v = v.strip()
    if v == "" :
        return ""
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [_unquote(x.strip()) for x in _split_inline(inner)]
    return _unquote(v)


def _split_inline(inner: str) -> list[str]:
    """Inline liste öğelerini virgülle böl (tırnak-içi virgülü koru)."""
    out, buf, q = [], [], None
    for ch in inner:
        if q:
            if ch == q:
                q = None
            buf.append(ch)
        elif ch in "\"'":
            q = ch
            buf.append(ch)
        elif ch == ",":
            out.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        out.append("".join(buf))
    return out


def _unquote(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


# ---------------------------------------------------------------------------
# Tarama
# ---------------------------------------------------------------------------

class Bulgu:
    __slots__ = ("term_id", "kanonik", "variant", "file", "line", "text",
                 "level", "reason")

    def __init__(self, term_id, kanonik, variant, file, line, text, level, reason):
        self.term_id = term_id
        self.kanonik = kanonik
        self.variant = variant
        self.file = file
        self.line = line
        self.text = text
        self.level = level      # "HARD" | "INFO"
        self.reason = reason


# ilk-geçiş parantezi: "kanonik (*ingilizce*)" — İngilizce terim tanıtımı muaf
def _firstuse_re(ingilizce: str) -> re.Pattern | None:
    if not ingilizce:
        return None
    return re.compile(r"\(\s*\*?" + re.escape(tr_lower(ingilizce)) + r"\*?\s*\)")


def _rel(path: str) -> str:
    try:
        return os.path.relpath(path, REPO_ROOT)
    except ValueError:
        return path


def _file_exempt(relpath: str, onekler: list[str]) -> bool:
    rp = relpath.replace("\\", "/")
    return any(rp.startswith(pre) for pre in onekler)


def _paragraph_window(all_lines: list[str], lineno: int) -> str:
    """Bulgu satırını içeren paragrafı (boş-satır sınırlı) döndür.

    Bağlamsal muafiyet satır değil PARAGRAF düzeyinde aranır: 'gizli değişken'in
    confounder anlamı çoğu zaman paragraf başlığında/önceki cümlede geçer
    (ör. 'Ölçülmemiş karıştırıcı ...'). idx 1-tabanlı.
    """
    n = len(all_lines)
    i = lineno - 1
    if i < 0 or i >= n:
        return all_lines[i] if 0 <= i < n else ""
    start = i
    while start > 0 and all_lines[start - 1].strip():
        start -= 1
    end = i
    while end + 1 < n and all_lines[end + 1].strip():
        end += 1
    return "\n".join(all_lines[start:end + 1])


def scan_file(path: str, terimler: list[dict], global_muaf: dict) -> list[Bulgu]:
    relpath = _rel(path)
    onekler = global_muaf.get("muaf_dosya_onekleri") or []
    if _file_exempt(relpath, onekler):
        return []
    basliklar = [tr_lower(b) for b in (global_muaf.get("muaf_bolum_basliklari") or [])]

    text = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    all_lines = text.splitlines()
    findings: list[Bulgu] = []
    in_muaf_bolum = False
    heading_re = re.compile(r"^\s*#{1,6}\s*(.+?)\s*$")

    # strip_fenced: kod-çiti/HTML-yorum/cell-option DIŞI (1-tabanlı) satırlar
    for lineno, line in strip_fenced(text):
        # bölüm-başlığı muafiyeti (# SUMMARY / # ABSTRACT sonrası)
        hm = heading_re.match(line)
        if hm:
            htitle = tr_lower(hm.group(1))
            in_muaf_bolum = any(htitle.startswith(b) for b in basliklar)
            continue
        if in_muaf_bolum:
            continue

        low = tr_lower(line)
        cleaned = tr_lower(_strip_citations(line))  # atıf gürültüsünü at

        for t in terimler:
            if (t.get("zorlama") or "").strip() != "hard":
                continue
            variants = t.get("yasak_varyantlar") or []
            if not variants:
                continue
            for var in variants:
                vlow = tr_lower(var)
                if vlow not in cleaned:
                    continue
                # ilk-geçiş parantezi muafiyeti (satır düzeyi)
                fu = _firstuse_re(t.get("ingilizce") or "")
                if fu and fu.search(low):
                    findings.append(Bulgu(
                        t.get("id", "?"), t.get("kanonik", ""), var,
                        relpath, lineno, line.strip(), "INFO",
                        "ilk-geçiş parantezi (İngilizce terim tanıtımı)"))
                    continue
                # bağlamsal muafiyet regex — PARAGRAF penceresinde ara
                ctx = t.get("baglamsal_muafiyet") or ""
                if ctx:
                    window = _paragraph_window(all_lines, lineno)
                    if re.search(ctx, window, re.IGNORECASE):
                        findings.append(Bulgu(
                            t.get("id", "?"), t.get("kanonik", ""), var,
                            relpath, lineno, line.strip(), "INFO",
                            "bağlamsal muafiyet (kaynak-terimi/farklı-kavram)"))
                        continue
                findings.append(Bulgu(
                    t.get("id", "?"), t.get("kanonik", ""), var,
                    relpath, lineno, line.strip(), "HARD",
                    f"kanonik biçim: '{t.get('kanonik','')}'"))
    return findings


def resolve_chapters(patterns: list[str]) -> list[str]:
    files: list[str] = []
    for pat in patterns:
        p = pat if os.path.isabs(pat) else os.path.join(REPO_ROOT, pat)
        files += sorted(_glob.glob(p))
    return files


# ---------------------------------------------------------------------------
# Rapor + CLI
# ---------------------------------------------------------------------------

def _render(findings: list[Bulgu], sozluk: dict, json_out: bool) -> str:
    hard = [f for f in findings if f.level == "HARD"]
    info = [f for f in findings if f.level == "INFO"]
    if json_out:
        import json
        return json.dumps({
            "hard": [_fd(f) for f in hard],
            "info": [_fd(f) for f in info],
            "ozet": {"hard": len(hard), "info": len(info),
                     "terim_sayisi": len(sozluk.get("terimler") or [])},
        }, ensure_ascii=False, indent=2)

    lines = ["=" * 70, "TERİM TUTARLILIK DENETİMİ", "=" * 70]
    hard_terms = sum(1 for t in (sozluk.get("terimler") or [])
                     if (t.get("zorlama") or "") == "hard")
    lines.append(f"Sözlük: {len(sozluk.get('terimler') or [])} terim "
                 f"({hard_terms} zorlanan · hard)")
    if hard:
        lines.append("")
        lines.append(f"HARD ({len(hard)}) — muafiyet dışı yasak varyant [teslim engeli]:")
        for f in hard:
            lines.append(f"  ✗ [{f.term_id}] {f.file}:{f.line} — '{f.variant}' → {f.reason}")
            lines.append(f"      {f.text[:100]}")
    if info:
        lines.append("")
        lines.append(f"INFO ({len(info)}) — muaf (bilgi amaçlı):")
        for f in info[:20]:
            lines.append(f"  · [{f.term_id}] {f.file}:{f.line} — '{f.variant}' ({f.reason})")
        if len(info) > 20:
            lines.append(f"  … ve {len(info) - 20} ek muaf bulgu")
    lines.append("")
    lines.append("-" * 70)
    if hard:
        lines.append(f"SONUÇ: FAIL — {len(hard)} HARD bulgu (kanonik terime hizala).")
    else:
        lines.append(f"SONUÇ: PASS — HARD bulgu yok ({len(info)} muaf INFO).")
    return "\n".join(lines)


def _fd(f: Bulgu) -> dict:
    return {"id": f.term_id, "kanonik": f.kanonik, "variant": f.variant,
            "file": f.file, "line": f.line, "level": f.level,
            "reason": f.reason, "text": f.text[:120]}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Kanonik terim tutarlılık denetçisi")
    ap.add_argument("--sozluk", default=DEFAULT_SOZLUK,
                    help="Kanonik terim sözlüğü YAML")
    ap.add_argument("--chapters", nargs="*", default=DEFAULT_CHAPTERS,
                    help="Taranacak bölüm glob'ları")
    ap.add_argument("--json", action="store_true", help="JSON çıktı")
    ap.add_argument("--fail-on", choices=["hard", "none"], default="hard",
                    help="hard: HARD bulgu → exit 1 (varsayılan); none: her zaman 0")
    args = ap.parse_args(argv)

    sozluk_path = args.sozluk if os.path.isabs(args.sozluk) \
        else os.path.join(REPO_ROOT, args.sozluk)
    if not os.path.exists(sozluk_path):
        print(f"HATA: sözlük yok: {args.sozluk}", file=sys.stderr)
        return 2
    sozluk = load_sozluk(sozluk_path)
    terimler = sozluk.get("terimler") or []
    global_muaf = sozluk.get("global_muafiyet") or {}

    files = resolve_chapters(args.chapters)
    if not files:
        print("HATA: taranacak bölüm bulunamadı", file=sys.stderr)
        return 2

    findings: list[Bulgu] = []
    for fn in files:
        findings += scan_file(fn, terimler, global_muaf)

    print(_render(findings, sozluk, args.json))

    hard = [f for f in findings if f.level == "HARD"]
    if args.fail_on == "none":
        return 0
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
