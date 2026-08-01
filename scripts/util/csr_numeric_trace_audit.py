#!/usr/bin/env python3
"""Trace CSR numeric claims to generated CSV outputs.

This audit intentionally avoids row-level output. It indexes generated CSV values
at file/column level, excludes identifier-like columns, and writes only aggregate
claim/match metadata.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import math
import re
from dataclasses import dataclass
from pathlib import Path


STAT_LINE_RE = re.compile(
    r"(?i)(\bp\s*[<=>≈=]|p[_ -]?(holm|bh|fdr)|\bq\s*[<=>≈=]|"
    r"\bci\b|%95\s*ga|95%\s*ga|\bga\b|icc|smd|\bor\b|"
    r"\bbeta\b|β|std[_ -]?β|std[_ -]?beta|\bb\s*=|\bd\s*=|\br\s*=|"
    r"χ|chi|cram|v\s*=|η|eta|r²|r2|Δr²|aic|bic|bf|pd\s*=|"
    r"\bn\s*=|\bn≈|\bn\s*≥|\bn\s*<=|\bn\s*<|\bn\s*>|"
    r"fisher|welch|holm|fdr|tost|ess|se\s*=|"
    r"alpha|cronbach|κ|kappa|lr\s*χ|lrt)"
)

NUMBER_RE = re.compile(r"(?<![\w])[-+]?(?:\d+[.,]\d+|\d+|[.,]\d+)(?:e[-+]?\d+)?", re.I)
SCI_UNICODE_RE = re.compile(
    r"(?P<base>[-+]?(?:\d+[.,]\d+|\d+|[.,]\d+))\s*[×x]\s*10(?P<exp>[⁻−-]?[⁰¹²³⁴⁵⁶⁷⁸⁹0-9]+)"
)
SUPERSCRIPT = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻−", "0123456789--")

ID_COL_RE = re.compile(r"(?i)(^|_)(id|aile_no|cocuk_no|çocuk_no|sira|sıra|row|index)(_|$)|kimlik|tc")
DATE_OR_SECTION_RE = re.compile(r"(?i)(doi|pmid|isbn|§|tablo|şekil|figure|chapter|bölüm)")
MODEL_FIT_CONTEXT_RE = re.compile(r"(?i)\b(aic|bic|caic|sabic|icl|loglik)\b")


@dataclass(frozen=True)
class CsvEntry:
    value: float
    source: str
    column: str


@dataclass
class ClaimNumber:
    token: str
    value: float
    decimals: int
    is_percent: bool
    context: str
    excluded_reason: str = ""


def normalize_decimal(token: str) -> str:
    token = token.strip()
    if token.startswith(","):
        token = "0" + token
    if token.startswith("-.") or token.startswith("+,"):
        pass
    if token.startswith("."):
        token = "0" + token
    return token.replace(",", ".")


def normalize_signs(text: str) -> str:
    return text.replace("−", "-").replace("–", "-")


def normalize_unicode_scientific(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        base = normalize_decimal(match.group("base"))
        exp = match.group("exp").translate(SUPERSCRIPT)
        return f"{base}e{exp}"

    return normalize_signs(SCI_UNICODE_RE.sub(repl, text))


def decimals_in_token(token: str) -> int:
    mantissa = token.lower().split("e", 1)[0]
    if "," in mantissa:
        return len(mantissa.rsplit(",", 1)[1])
    if "." in mantissa:
        return len(mantissa.rsplit(".", 1)[1])
    return 0


def parse_float(token: str) -> float | None:
    try:
        return float(normalize_decimal(token))
    except ValueError:
        return None


def numeric_tolerance(number: ClaimNumber) -> float:
    if "e" in number.token.lower():
        return max(abs(number.value) * 0.08, 1e-300)
    if number.decimals == 0:
        if MODEL_FIT_CONTEXT_RE.search(number.context):
            return 0.5000001
        return 0.5000001 if number.is_percent else 1e-9
    return (0.5 * (10 ** (-number.decimals))) + 1e-9


def is_year_like(value: float, context: str) -> bool:
    if not float(value).is_integer():
        return False
    year = int(value)
    if not 1900 <= year <= 2099:
        return False
    return True


def should_exclude_number(token: str, value: float, context: str, start_pos: int, end_pos: int) -> str:
    low = context.lower()
    start = max(0, start_pos - 14)
    end = min(len(context), end_pos + 14)
    local = context[start:end]
    if is_year_like(value, context):
        return "year_like"
    if re.search(r"(?i)meta-analiz|literatür|çerçevesinde|standardında|çalışmasıyla|belgelenmiştir|yöntemsel paralellik", low):
        if re.search(r"(?i)(araştırma|çalışma|katılımc|ergen|düad|standardında)", local):
            return "literature_context"
    if re.search(r"(§|tablo|şekil|figure|bölüm|chapter)\s*$", local, re.I) or re.search(
        r"(?i)(§|tablo|şekil|figure|bölüm|chapter)\s*$", context[max(0, start_pos - 12):start_pos]
    ):
        return "section_or_table_number"
    if "§" in local and re.fullmatch(r"\d+(?:[.,]\d+)?", token):
        return "section_reference"
    if "doi" in low or "pmid" in low:
        # Keep explicit statistical claims in citation-heavy lines, but drop likely
        # bibliographic identifiers.
        if abs(value) > 1000:
            return "bibliographic_identifier"
    if abs(value) > 100000 and not re.search(r"(?i)(n\s*=|rows|satır|gözlem)", context):
        return "large_nonstat_identifier"
    return ""


def extract_claim_numbers(line: str) -> list[ClaimNumber]:
    normalized = normalize_unicode_scientific(line)
    out: list[ClaimNumber] = []
    for match in NUMBER_RE.finditer(normalized):
        token = match.group(0)
        value = parse_float(token)
        if value is None or not math.isfinite(value):
            continue
        left = normalized[max(0, match.start() - 2):match.start()]
        right = normalized[match.end():min(len(normalized), match.end() + 2)]
        is_percent = "%" in left or "%" in right
        number = ClaimNumber(
            token=token,
            value=value,
            decimals=decimals_in_token(token),
            is_percent=is_percent,
            context=normalized,
        )
        number.excluded_reason = should_exclude_number(token, value, normalized, match.start(), match.end())
        out.append(number)
    return out


def read_csv_entries(csv_paths: list[Path], root: Path) -> list[CsvEntry]:
    entries: list[CsvEntry] = []
    for path in csv_paths:
        rel = path.relative_to(root).as_posix()
        try:
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                if not reader.fieldnames:
                    continue
                fields = [field for field in reader.fieldnames if field and not ID_COL_RE.search(field)]
                for row in reader:
                    for field in fields:
                        raw = row.get(field, "")
                        if raw is None:
                            continue
                        raw = str(raw).strip()
                        if not raw or raw.upper() in {"NA", "NAN", "NULL", "INF", "-INF"}:
                            continue
                        candidates = [raw]
                        if not re.fullmatch(r"[-+]?(?:\d+[.,]\d+|\d+|[.,]\d+)(?:e[-+]?\d+)?", raw, re.I):
                            candidates = [m.group(0) for m in NUMBER_RE.finditer(normalize_unicode_scientific(raw))]
                        for candidate in candidates:
                            value = parse_float(candidate)
                            if value is None or not math.isfinite(value):
                                continue
                            entries.append(CsvEntry(value=value, source=rel, column=field))
        except UnicodeDecodeError:
            with path.open("r", encoding="latin-1", newline="") as handle:
                reader = csv.DictReader(handle)
                if not reader.fieldnames:
                    continue
                fields = [field for field in reader.fieldnames if field and not ID_COL_RE.search(field)]
                for row in reader:
                    for field in fields:
                        raw = str(row.get(field, "")).strip()
                        value = parse_float(raw)
                        if value is not None and math.isfinite(value):
                            entries.append(CsvEntry(value=value, source=rel, column=field))
    return entries


def read_lock_constants(root: Path) -> list[CsvEntry]:
    """Kanonik analiz baz kilidinden tasarım sabitlerini (family_rows,
    long_rows, *_columns) izlenebilir kaynak olarak oku.

    Bu sabitler (ör. n=241 aile, n=482 çocuk-satırı) hesaplanmış çıktı değil,
    tasarım girdisidir; hiçbir outputs/tables hücresine düşmezler. Kilit dosyası
    tek kanonik doğruluk kaynağı olduğundan, düzyazıda geçen bu sabitlerin
    'kaynaksız yüksek-risk' olarak işaretlenmesini önlemek için burada
    kaydedilirler."""
    lock = root / "data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock"
    if not lock.exists():
        return []
    rel = lock.relative_to(root).as_posix()
    entries: list[CsvEntry] = []
    key_re = re.compile(r"(?P<key>[A-Za-z_]+)\s*=\s*(?P<val>\d+)")
    for line in lock.read_text(encoding="utf-8", errors="ignore").splitlines():
        for m in key_re.finditer(line):
            val = parse_float(m.group("val"))
            if val is None or not math.isfinite(val):
                continue
            entries.append(CsvEntry(value=val, source=rel, column=m.group("key")))
    return entries


def build_sorted_index(entries: list[CsvEntry]) -> tuple[list[float], list[CsvEntry]]:
    sorted_entries = sorted(entries, key=lambda item: item.value)
    return [item.value for item in sorted_entries], sorted_entries


def find_matches(number: ClaimNumber, values: list[float], entries: list[CsvEntry], limit: int = 8) -> list[CsvEntry]:
    targets = [number.value]
    if number.is_percent:
        targets.append(number.value / 100.0)
    elif abs(number.value) <= 1:
        targets.append(number.value * 100.0)

    matches: list[CsvEntry] = []
    seen: set[tuple[str, str]] = set()
    for target in targets:
        tol = numeric_tolerance(number)
        if "e" in number.token.lower():
            tol = max(abs(target) * 0.08, tol)
        left = bisect.bisect_left(values, target - tol)
        right = bisect.bisect_right(values, target + tol)
        for entry in entries[left:right]:
            key = (entry.source, entry.column)
            if key in seen:
                continue
            seen.add(key)
            matches.append(entry)
            if len(matches) >= limit:
                return matches
    return matches


def iter_visible_csr_lines(csr_path: Path) -> list[tuple[int, str]]:
    visible: list[tuple[int, str]] = []
    in_comment = False
    in_reference_block = False
    in_code_fence = False
    for lineno, line in enumerate(csr_path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        # Fenced kod bloğu (```{r}, ```python, ```) sınırı: içerideki sayılar
        # analiz iddiası değil kod-literalidir (ör. figür koordinatı, inline
        # tribble verisi). Kaynaksız-sayı izlemesi düzyazı iddialarını hedefler;
        # kod-literalleri high-risk saymamak için bu bloklar atlanır.
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue
        if stripped.startswith("# 21."):
            in_reference_block = True
        elif stripped.startswith("# 22."):
            in_reference_block = False
        if "<!--" in stripped:
            in_comment = True
        if not in_comment and not in_reference_block and stripped:
            if stripped.startswith("#"):
                if "-->" in stripped:
                    in_comment = False
                continue
            if re.match(r"^\*\*Tablo\s+\d", stripped, re.I):
                continue
            visible.append((lineno, stripped))
        if "-->" in stripped:
            in_comment = False
    return visible


_CITATION_RE = re.compile(
    r"\([A-ZÇĞİÖŞÜ][\wçğıöşü]+(?:\s+ve\s+diğerleri)?[^)]*,\s*\d{4}\)"
    r"|\b[A-ZÇĞİÖŞÜ][\wçğıöşü]+\s+ve\s+diğerleri(?:’n[ie])?\s*\(\d{4}\)",
    re.IGNORECASE,
)
_THRESHOLD_RE = re.compile(r"eşi[kğ]|threshold|kesme\s*değer|cut[- ]?off", re.IGNORECASE)

# Atıf tanıma (paragraf ölçeğinde): hem pandoc köşeli/bare `@key` hem de yazar-tarih
# düzyazısı. `is_cited_threshold_constant`'ın satır-içi `_CITATION_RE`'sinden farkı,
# sarılı (hard-wrapped) paragraflarda atıfın komşu fiziksel satıra düşebilmesidir.
_PARA_CITATION_RE = re.compile(
    r"@[\w:.\-]+"
    r"|\([A-ZÇĞİÖŞÜ][\wçğıöşü]+(?:\s+ve\s+diğerleri)?[^)]*,\s*\d{4}\)"
    r"|\b[A-ZÇĞİÖŞÜ][\wçğıöşü]+\s+ve\s+(?:arkadaşlar|diğerleri)",
    re.IGNORECASE,
)
# Cümlede bir DIŞ çalışma betimleyicisi (örneklem/kohort/meta-analiz vb.).
_EXTERNAL_STUDY_RE = re.compile(
    r"(?i)çalışma|araştırma|meta-?analiz|örneklem|katılımc|arkadaşlar|diğerleri|"
    r"kohort|derleme|öğrenci|hastayla|hasta-eş|çiftinde|çifti|kardeşiyle|aileyi|"
    r"ailesiyle|yürüt|kapsayan|karşılaştıran|bildirmiş|göstermiş|raporlamış|"
    r"ortaya koymuş|tekrarlanmış|geliştiril|evlat edinil"
)
# Sayının HEMEN yanında bir 'kendi sonucumuz' işaretçisi varsa dış-literatür sayma.
_OWN_RESULT_RE = re.compile(
    r"(?i)çalışmamız|bulgumuz|bulgular[ıi]m[ıi]z|örneklemimiz|analizimiz|"
    r"modelimiz|tezimiz|verimiz|bulduğumuz|gösterdiğimiz"
)
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.;:])\s+(?=[A-ZÇĞİÖŞÜ0-9@])")


def build_paragraph_map(path: Path) -> dict[int, str]:
    """Satır numarasını, onu içeren boş-satır-ayraçlı paragrafın tam metnine eşle.

    Kod çitleri (```...```) atlanır; içlerindeki sayılar analiz iddiası değildir.
    Sarılı paragraflarda atıf komşu fiziksel satıra düşebildiğinden, dış-literatür
    ayrımı satır değil paragraf ölçeğinde yapılır.
    """
    line_para: dict[int, str] = {}
    cur: list[str] = []
    cur_lines: list[int] = []
    in_fence = False

    def flush() -> None:
        if not cur:
            return
        text = " ".join(cur)
        for ln in cur_lines:
            line_para[ln] = text

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not stripped:
            flush()
            cur.clear()
            cur_lines.clear()
            continue
        cur.append(stripped)
        cur_lines.append(lineno)
    flush()
    return line_para


def is_cited_external_literature(num: "ClaimNumber", paragraph: str) -> bool:
    """Sayı, atıflı bir dış-çalışma yeniden-ifadesi mi (kendi çıktımız değil)?

    ch04→ch05/CSR yeniden-ifade sürüklenmesini bir kapıya bağlarken yanlış-pozitifi
    önler: Tartışma paragrafları kendi bulgularımızı literatürle iç içe anlatır ve
    literatür sayıları (Pinquart g, PedsQL 75,1 vb.) hiçbir outputs/tables hücresine
    düşmez. Ölçüt üçlüdür: (1) paragrafta atıf var, (2) sayının cümlesinde bir dış-
    çalışma betimleyicisi var, (3) sayının HEMEN yanında (±70 karakter) 'kendi
    sonucumuz' işaretçisi YOK. Üçü birden sağlanırsa dış-literatür sayılır; kendi
    sonucumuzun sürüklenmesi (atıfsız ya da 'çalışmamız/bulgumuz' yakınında) etkilenmez.
    """
    if not paragraph or not _PARA_CITATION_RE.search(paragraph):
        return False
    tok = num.token
    sentence = paragraph
    for cand in _SENTENCE_SPLIT_RE.split(paragraph):
        if tok in cand:
            sentence = cand
            break
    pos = sentence.find(tok)
    window = sentence[max(0, pos - 70): pos + len(tok) + 70] if pos >= 0 else sentence
    if _OWN_RESULT_RE.search(window):
        return False
    return bool(_EXTERNAL_STUDY_RE.search(sentence))


def is_cited_threshold_constant(num: "ClaimNumber", line: str) -> bool:
    """Atıfla desteklenen metodolojik eşik sabiti mi?

    Örn. 'yaygın 1,05 eşiğinin altında (Vehtari ve diğerleri, 2021)': bu bir
    çalışma çıktısı değil, literatürden alınmış yakınsama/karar eşiğidir; hiçbir
    outputs/tables hücresine düşmez. Satırda hem bir eşik anahtarı hem de bir
    atıf varsa ve token eşik kelimesine yakınsa yüksek-risk sayılmaz."""
    if not (_THRESHOLD_RE.search(line) and _CITATION_RE.search(line)):
        return False
    # token, 'eşik' kelimesinin yakınında mı? (aynı satırda, ≤ 25 karakter)
    tok = re.escape(num.token)
    return bool(re.search(tok + r"[^0-9]{0,25}eşi[kğ]", line, re.I)
                or re.search(r"eşi[kğ][^0-9]{0,25}" + tok, line, re.I))


def claim_scope(line: str) -> str:
    keys = []
    for label, regex in [
        ("p_value", r"(?i)\bp\s*[<=>≈=]|p[_ -]?(holm|bh|fdr)"),
        ("ci_ga", r"(?i)\bci\b|%95\s*ga|95%\s*ga|\bga\b"),
        ("effect", r"(?i)\bor\b|β|beta|\bb\s*=|\bd\s*=|\br\s*=|smd|icc|η|r²|Δr²|κ"),
        ("sample", r"(?i)\bn\s*=|\bn≈|\bn\s*[<>≥≤]|gözlem|aile|satır"),
        ("model", r"(?i)aic|bic|bf|pd|ess|lr\s*χ|χ²|fisher|welch"),
    ]:
        if re.search(regex, line):
            keys.append(label)
    return ";".join(keys) if keys else "stat_line"


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csr", default="docs/CLINICAL-STUDY-REPORT-FINAL.md")
    parser.add_argument("--tables", default="outputs/tables")
    parser.add_argument("--out-claims", default="outputs/tables/csr_numeric_trace_claims.csv")
    parser.add_argument("--out-numbers", default="outputs/tables/csr_numeric_trace_numbers.csv")
    parser.add_argument("--out-report", default="outputs/reports/csr_numeric_trace_audit.md")
    args = parser.parse_args()

    root = Path.cwd()
    csr_path = root / args.csr
    csv_paths = [
        path for path in sorted((root / args.tables).glob("*.csv"))
        if not path.name.startswith("csr_numeric_trace_")
    ]
    entries = read_csv_entries(csv_paths, root)
    entries.extend(read_lock_constants(root))
    values, sorted_entries = build_sorted_index(entries)
    paragraph_map = build_paragraph_map(csr_path)

    claim_rows: list[dict[str, object]] = []
    number_rows: list[dict[str, object]] = []
    for lineno, line in iter_visible_csr_lines(csr_path):
        if not STAT_LINE_RE.search(line):
            continue
        numbers = extract_claim_numbers(line)
        auditable = [num for num in numbers if not num.excluded_reason]
        if not auditable:
            continue
        matched = 0
        high_risk_unmatched = 0
        paragraph = paragraph_map.get(lineno, line)
        for num in auditable:
            matches = find_matches(num, values, sorted_entries)
            cited_threshold = False
            cited_literature = False
            if matches:
                matched += 1
            else:
                cited_threshold = is_cited_threshold_constant(num, line)
                cited_literature = is_cited_external_literature(num, paragraph)
                if cited_threshold:
                    # atıflı metodolojik eşik: çalışma çıktısı değil, izlenmiş sayılır
                    matched += 1
                elif cited_literature:
                    # atıflı dış-literatür yeniden-ifadesi: kendi çıktımız değil,
                    # outputs/tables'a düşmez; yüksek-risk sürüklenme sayılmaz.
                    matched += 1
                elif re.search(
                    r"(?i)(p|or|β|beta|ga|ci|icc|smd|χ|η|r²|bf|pd|ess)", line
                ):
                    high_risk_unmatched += 1
            number_rows.append(
                {
                    "line": lineno,
                    "claim_scope": claim_scope(line),
                    "token": num.token,
                    "value": f"{num.value:.15g}",
                    "is_percent": num.is_percent,
                    "match_status": (
                        "matched" if matches
                        else "cited_threshold" if cited_threshold
                        else "cited_literature" if cited_literature
                        else "unmatched"
                    ),
                    "match_count_capped": len(matches),
                    "matched_sources": "; ".join(f"{m.source}::{m.column}" for m in matches),
                    "claim_excerpt": line[:700],
                }
            )
        if matched == len(auditable):
            status = "traced_all"
        elif matched > 0:
            status = "partial_trace"
        else:
            status = "untraced"
        claim_rows.append(
            {
                "line": lineno,
                "claim_scope": claim_scope(line),
                "status": status,
                "auditable_numbers": len(auditable),
                "matched_numbers": matched,
                "unmatched_numbers": len(auditable) - matched,
                "high_risk_unmatched_numbers": high_risk_unmatched,
                "claim_excerpt": line[:900],
            }
        )

    write_csv(
        root / args.out_claims,
        claim_rows,
        [
            "line",
            "claim_scope",
            "status",
            "auditable_numbers",
            "matched_numbers",
            "unmatched_numbers",
            "high_risk_unmatched_numbers",
            "claim_excerpt",
        ],
    )
    write_csv(
        root / args.out_numbers,
        number_rows,
        [
            "line",
            "claim_scope",
            "token",
            "value",
            "is_percent",
            "match_status",
            "match_count_capped",
            "matched_sources",
            "claim_excerpt",
        ],
    )

    total = len(claim_rows)
    traced = sum(1 for row in claim_rows if row["status"] == "traced_all")
    partial = sum(1 for row in claim_rows if row["status"] == "partial_trace")
    untraced = sum(1 for row in claim_rows if row["status"] == "untraced")
    high_risk = sum(int(row["high_risk_unmatched_numbers"]) for row in claim_rows)
    unmatched_numbers = sum(1 for row in number_rows if row["match_status"] == "unmatched")
    matched_numbers = sum(1 for row in number_rows if row["match_status"] == "matched")

    top_untraced = [row for row in claim_rows if row["status"] != "traced_all"][:25]
    report_lines = [
        "# CSR Numeric Trace Audit",
        "",
        "Scope: visible lines in `docs/CLINICAL-STUDY-REPORT-FINAL.md` containing statistical markers were checked against generated `outputs/tables/*.csv` values.",
        "Privacy: no row-level values, identifiers, or raw data are reported; matches are file/column level only.",
        "",
        "## Summary",
        "",
        f"- CSV files indexed: {len(csv_paths)}",
        f"- Numeric CSV entries indexed: {len(entries)}",
        f"- Statistical claim lines checked: {total}",
        f"- Claim lines fully traced: {traced}",
        f"- Claim lines partially traced: {partial}",
        f"- Claim lines untraced: {untraced}",
        f"- Number tokens matched: {matched_numbers}",
        f"- Number tokens unmatched: {unmatched_numbers}",
        f"- High-risk unmatched number tokens: {high_risk}",
        "",
        "## Review Queue",
        "",
    ]
    if not top_untraced:
        report_lines.append("No non-fully-traced claim lines found by this automated pass.")
    else:
        for row in top_untraced:
            report_lines.append(
                f"- line {row['line']} `{row['status']}` "
                f"matched {row['matched_numbers']}/{row['auditable_numbers']}: "
                f"{row['claim_excerpt']}"
            )
    (root / args.out_report).parent.mkdir(parents=True, exist_ok=True)
    (root / args.out_report).write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"claims={total} traced_all={traced} partial={partial} untraced={untraced}")
    print(f"numbers_matched={matched_numbers} numbers_unmatched={unmatched_numbers} high_risk_unmatched={high_risk}")
    print(f"claims_csv={args.out_claims}")
    print(f"numbers_csv={args.out_numbers}")
    print(f"report={args.out_report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
