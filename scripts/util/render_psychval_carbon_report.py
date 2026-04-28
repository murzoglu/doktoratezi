#!/usr/bin/env python3
"""Render the integrated psychometric validation report as Carbon-styled HTML."""

from __future__ import annotations

import base64
import csv
import html
import math
import re
from collections import defaultdict
from datetime import date
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "outputs" / "tables"
OUT_DIR = ROOT / "outputs" / "carbon"
SKILL_DIR = Path("/home/mahirkurt/.codex/skills/carbon-html-report")
PAGED_JS = SKILL_DIR / "assets" / "paged.polyfill.js"


NICE_SUBSCALE = {
    "sicaklik": "Sıcaklık",
    "asiri_koruma": "Aşırı koruma",
    "reddetme": "Reddetme",
    "karsilastirma": "Karşılaştırma",
}

NICE_SRQ = {
    "srq_total_mean": "SRQ toplam",
    "sicaklik_yakinlik_mean": "SRQ Sıcaklık/Yakınlık",
    "statu_guc_mean": "SRQ Statü/Güç",
    "catisma_mean": "SRQ Çatışma",
    "rekabet_mean": "SRQ Rekabet",
}

NICE_ITEM_SET = {
    "all_29_items": "29 madde",
    "q12_excluded_28_items": "q12siz 28",
    "q12_excluded_7_rejection_items_binary_1_vs_gt1": "Reddetme binary",
    "all_29_items_binary_1_vs_gt1": "29 madde binary",
    "all_29_items_original_4cat": "29 madde 4 kategori",
}

NICE_FORM = {
    "EMBU-P q12siz Reddetme binary": "EMBU-P q12siz",
    "EMBU-C binary": "EMBU-C bin.",
}

NICE_SCHEME = {
    "binary_1_vs_gt1": "1/>1",
    "original_4cat": "4 kat.",
}

EMBU_SUBSCALE_ITEMS = {
    "sicaklik": [1, 3, 6, 7, 13, 17, 20, 24, 26],
    "asiri_koruma": [4, 8, 14, 15, 19, 23, 25],
    "reddetme": [5, 9, 10, 12, 16, 21, 22, 28],
    "karsilastirma": [2, 11, 18, 27, 29],
}


def read_csv(name: str) -> list[dict[str, str]]:
    path = TABLE_DIR / name
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_csv_path(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def metric_value(metrics: list[dict[str, str]], metric: str) -> float:
    for row in metrics:
        if row.get("metric") == metric:
            return num(row.get("value"))
    return math.nan


def num(value: object) -> float:
    try:
        if value is None or value == "":
            return math.nan
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def fmt(value: object, digits: int = 3) -> str:
    x = num(value)
    if math.isnan(x):
        return "NA"
    return f"{x:.{digits}f}"


def fmt_p(value: object) -> str:
    x = num(value)
    if math.isnan(x):
        return "NA"
    if x < 0.001:
        return "<.001"
    return f"{x:.3f}"


def fmt2(value: object) -> str:
    return fmt(value, 2)


def fmt_pct(value: object, digits: int = 1) -> str:
    x = num(value)
    if math.isnan(x):
        return "NA"
    return f"{x:.{digits}f}%"


def fmt_int(value: object) -> str:
    x = num(value)
    if math.isnan(x):
        return "NA"
    return f"{int(round(x))}"


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def short_text(value: object, width: int = 90) -> str:
    text = " ".join(str(value or "").split())
    return text if len(text) <= width else text[: width - 3] + "..."


def is_missing_text(value: object) -> bool:
    text = str(value or "").strip()
    return text == "" or text.upper() in {"NA", "NAN", "NULL"}


def item_number(value: str) -> int:
    match = re.search(r"q(\d+)", value or "")
    return int(match.group(1)) if match else 0


def item_col(prefix: str, item_no: int) -> str:
    return f"{prefix}_q{item_no:02d}"


def finite(values: list[object]) -> list[float]:
    out = []
    for value in values:
        x = num(value)
        if not math.isnan(x):
            out.append(x)
    return out


def mean(values: list[float]) -> float:
    vals = [v for v in values if not math.isnan(v)]
    if not vals:
        return math.nan
    return sum(vals) / len(vals)


def sample_variance(values: list[float]) -> float:
    vals = [v for v in values if not math.isnan(v)]
    if len(vals) < 2:
        return math.nan
    center = mean(vals)
    return sum((v - center) ** 2 for v in vals) / (len(vals) - 1)


def pearson_pairwise(rows: list[dict[str, str]], col_a: str, col_b: str) -> float:
    pairs = []
    for row in rows:
        a = num(row.get(col_a))
        b = num(row.get(col_b))
        if not math.isnan(a) and not math.isnan(b):
            pairs.append((a, b))
    if len(pairs) < 3:
        return math.nan
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    vx = sample_variance(xs)
    vy = sample_variance(ys)
    if math.isnan(vx) or math.isnan(vy) or vx == 0 or vy == 0:
        return math.nan
    mx = mean(xs)
    my = mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in pairs) / (len(pairs) - 1)
    return cov / math.sqrt(vx * vy)


def cronbach_alpha(rows: list[dict[str, str]], columns: list[str]) -> tuple[float, int]:
    matrix = []
    for row in rows:
        vals = [num(row.get(col)) for col in columns]
        if all(not math.isnan(v) for v in vals):
            matrix.append(vals)
    if len(matrix) < 3 or len(columns) < 2:
        return math.nan, len(matrix)
    item_vars = [sample_variance([row[idx] for row in matrix]) for idx in range(len(columns))]
    total_var = sample_variance([sum(row) for row in matrix])
    if math.isnan(total_var) or total_var == 0 or any(math.isnan(v) for v in item_vars):
        return math.nan, len(matrix)
    k = len(columns)
    alpha = k / (k - 1) * (1 - sum(item_vars) / total_var)
    return alpha, len(matrix)


def bh_fdr(p_values: list[object]) -> list[float]:
    parsed = [(idx, num(value)) for idx, value in enumerate(p_values)]
    valid = sorted(((idx, p) for idx, p in parsed if not math.isnan(p)), key=lambda x: x[1])
    q_values = [math.nan] * len(p_values)
    m = len(valid)
    running = 1.0
    for rank, (idx, p) in reversed(list(enumerate(valid, start=1))):
        running = min(running, p * m / rank)
        q_values[idx] = min(running, 1.0)
    return q_values


def compute_cr_ave(
    loadings: list[dict[str, str]], reliability: list[dict[str, str]]
) -> list[list[object]]:
    grouped: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in loadings:
        if row.get("model") != "four_factor":
            continue
        form = row.get("form", "")
        factor = row.get("factor", "")
        if form not in {"EMBU-P", "EMBU-C"} or factor not in NICE_SUBSCALE:
            continue
        loading = num(row.get("std_loading"))
        if not math.isnan(loading):
            grouped[(form, factor)].append(loading)

    reliability_lookup = {
        (row.get("form"), row.get("subscale")): row
        for row in reliability
        if row.get("form") in {"EMBU-P", "EMBU-C"}
    }
    rows = []
    for form in ["EMBU-P", "EMBU-C"]:
        for subscale in EMBU_SUBSCALE_ITEMS:
            lambdas = grouped.get((form, subscale), [])
            if not lambdas:
                continue
            residuals = [max(0.0, 1 - loading**2) for loading in lambdas]
            numerator = sum(lambdas) ** 2
            cr = numerator / (numerator + sum(residuals)) if numerator + sum(residuals) > 0 else math.nan
            ave = mean([loading**2 for loading in lambdas])
            min_loading = min(lambdas)
            max_loading = max(lambdas)
            rel_row = reliability_lookup.get((form, subscale), {})
            ave_note = "güçlü" if ave >= 0.50 else "sınırda" if ave >= 0.40 else "sınırlı"
            rows.append(
                [
                    form,
                    NICE_SUBSCALE.get(subscale, subscale),
                    fmt2(rel_row.get("alpha_raw")),
                    fmt2(rel_row.get("omega_total")),
                    fmt2(cr),
                    fmt2(ave),
                    f"{fmt2(min_loading)} / {fmt2(max_loading)}",
                    ave_note,
                ]
            )
    return rows


def htmt_for_rows(rows: list[dict[str, str]], prefix: str, form: str) -> list[list[object]]:
    subscale_cols = {
        subscale: [item_col(prefix, item_no) for item_no in item_numbers]
        for subscale, item_numbers in EMBU_SUBSCALE_ITEMS.items()
    }
    out = []
    for left, right in combinations(EMBU_SUBSCALE_ITEMS.keys(), 2):
        hetero = [
            abs(pearson_pairwise(rows, col_a, col_b))
            for col_a in subscale_cols[left]
            for col_b in subscale_cols[right]
        ]
        mono_left = [
            abs(pearson_pairwise(rows, col_a, col_b))
            for col_a, col_b in combinations(subscale_cols[left], 2)
        ]
        mono_right = [
            abs(pearson_pairwise(rows, col_a, col_b))
            for col_a, col_b in combinations(subscale_cols[right], 2)
        ]
        numerator = mean([v for v in hetero if not math.isnan(v)])
        denom_left = mean([v for v in mono_left if not math.isnan(v)])
        denom_right = mean([v for v in mono_right if not math.isnan(v)])
        htmt = numerator / math.sqrt(denom_left * denom_right) if denom_left > 0 and denom_right > 0 else math.nan
        decision = "<.85" if htmt < 0.85 else ".85-.90" if htmt < 0.90 else "yüksek"
        out.append([form, NICE_SUBSCALE[left], NICE_SUBSCALE[right], fmt2(htmt), decision])
    return out


def compute_age_alpha_rows(long_reference: list[dict[str, str]]) -> list[list[object]]:
    bands = [
        ("7-10", 7, 10),
        ("11-13", 11, 13),
        ("14+", 14, math.inf),
    ]
    rows = []
    for label, lo, hi in bands:
        band_rows = []
        for row in long_reference:
            age = num(row.get("cocuk_yas"))
            if math.isnan(age):
                continue
            if age >= lo and age <= hi:
                band_rows.append(row)
        cells = [label, fmt_int(len(band_rows))]
        for subscale, item_numbers in EMBU_SUBSCALE_ITEMS.items():
            alpha, n_complete = cronbach_alpha(band_rows, [item_col("embu_c", item_no) for item_no in item_numbers])
            cells.append(f"{fmt2(alpha)} (n={fmt_int(n_complete)})")
        rows.append(cells)
    return rows


def compute_beck_severity_rows(scores_family: list[dict[str, str]]) -> list[list[object]]:
    categories = [
        ("Minimal", 0, 9),
        ("Hafif", 10, 16),
        ("Orta", 17, 29),
        ("Şiddetli", 30, math.inf),
    ]
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in scores_family:
        group = row.get("group", "NA") or "NA"
        score = num(row.get("beck_total"))
        if not math.isnan(score):
            grouped[group].append(score)
    rows = []
    for group in sorted(grouped.keys()):
        vals = grouped[group]
        denom = len(vals)
        for label, lo, hi in categories:
            count = sum(1 for value in vals if value >= lo and value <= hi)
            pct = count / denom * 100 if denom else math.nan
            rows.append([group, label, fmt_int(count), fmt_pct(pct)])
    return rows


def rejection_item_diagnostics(
    item_desc_p: list[dict[str, str]],
    item_desc_c: list[dict[str, str]],
    item_total: list[dict[str, str]],
    reliability: list[dict[str, str]],
) -> list[list[object]]:
    desc_lookup = {
        (row.get("form"), row.get("item")): row
        for row in item_desc_p + item_desc_c
        if row.get("subscale") == "reddetme"
    }
    itc_lookup = {
        (row.get("form"), row.get("item")): row
        for row in item_total
        if row.get("subscale") == "reddetme"
    }
    alpha_lookup = {
        row.get("form"): num(row.get("alpha_raw"))
        for row in reliability
        if row.get("subscale") == "reddetme" and row.get("form") in {"EMBU-P", "EMBU-C"}
    }
    rows = []
    for form, prefix in [("EMBU-P", "embu_p"), ("EMBU-C", "embu_c")]:
        for item_no in EMBU_SUBSCALE_ITEMS["reddetme"]:
            item = item_col(prefix, item_no)
            desc = desc_lookup.get((form, item), {})
            itc = itc_lookup.get((form, item), {})
            r_drop = num(itc.get("r_drop"))
            floor = num(desc.get("floor_pct"))
            alpha_deleted = num(itc.get("alpha_if_deleted"))
            current_alpha = alpha_lookup.get(form, math.nan)
            flags = []
            if r_drop < 0.20:
                flags.append("düşük CITC")
            if floor >= 80:
                flags.append("taban")
            if not math.isnan(alpha_deleted) and not math.isnan(current_alpha) and alpha_deleted > current_alpha + 0.02:
                flags.append("çıkarınca artış")
            rows.append(
                [
                    form,
                    f"q{item_no:02d}",
                    fmt2(desc.get("mean")),
                    fmt2(desc.get("sd")),
                    fmt2(desc.get("skew")),
                    fmt_pct(floor, 1),
                    fmt2(r_drop),
                    fmt2(alpha_deleted),
                    ", ".join(flags) if flags else "uygun",
                ]
            )
    return rows


def top_modification_rows(modification_indices: list[dict[str, str]], per_form: int = 8) -> list[list[object]]:
    rows = []
    for form in ["EMBU-P", "EMBU-C"]:
        form_rows = [
            row
            for row in modification_indices
            if row.get("form") == form and row.get("model") == "four_factor" and is_missing_text(row.get("error"))
        ]
        form_rows = sorted(form_rows, key=lambda row: num(row.get("mi")), reverse=True)[:per_form]
        for row in form_rows:
            kind = "artık kovaryans" if row.get("op") == "~~" else "çapraz yük" if row.get("op") == "=~" else row.get("op", "")
            rows.append(
                [
                    form,
                    kind,
                    f"{row.get('lhs')} {row.get('op')} {row.get('rhs')}",
                    fmt(row.get("mi"), 1),
                    fmt2(row.get("sepc.all")),
                ]
            )
    return rows


def pct_width(value: float, lo: float, hi: float) -> float:
    if math.isnan(value) or hi == lo:
        return 0.0
    return max(0.0, min(100.0, ((value - lo) / (hi - lo)) * 100.0))


def svg_icon(name: str, class_name: str = "cds-inline-icon") -> str:
    paths = {
        "document": [
            'M25.7 9.3l-7-7A.908.908 0 0 0 18 2H8a2 2 0 0 0-2 2v24a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V10a.91.91 0 0 0-.3-.7zM18 4.4l5.6 5.6H18zM24 28H8V4h8v6a2 2 0 0 0 2 2h6z'
        ],
        "analytics": [
            "M4 2h2v28H4zm6 14h2v14h-2zm6-8h2v22h-2zm6 12h2v10h-2z"
        ],
        "chart-line": [
            "M30 27V5h2v24H4v-2z",
            "M30 8l-8 8-4-4-12 12-1.4-1.4L18 9.2l4 4 8-8z",
        ],
        "chart-eval": [
            "M28 6h-4v2h4v16H4V8h4V6H4c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h24c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2z",
            "M7 20l7.5-7.5 4 4L28 6.1 24 2h8v8l-4-4-9 9-4-4-6 6z",
        ],
        "check": [
            "M16 2A14 14 0 1 0 30 16 14 14 0 0 0 16 2zm-2 19.59-5-5L10.59 15 14 18.41 21.41 11 23 12.42z"
        ],
        "warning": [
            "M16 2 1 29h30zm0 4.2L27.5 27h-23zm-1 8.8v7h2v-7zm1 10a1.25 1.25 0 1 0 1.25 1.25A1.25 1.25 0 0 0 16 25z"
        ],
        "info": [
            "M16 2a14 14 0 1 0 14 14A14 14 0 0 0 16 2zm0 26a12 12 0 1 1 12-12 12 12 0 0 1-12 12z",
            "M17 22h-2v-8h-2v-2h4v10z",
            'M16 7.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z',
        ],
        "shield": [
            "M16 2 4 6v10.09c0 5.28 4.36 10.37 12 13.9 7.64-3.53 12-8.62 12-13.9V6zm10 14.09c0 4.33-3.72 8.7-10 11.87-6.28-3.18-10-7.54-10-11.87V7.38l10-3.4 10 3.4z",
            "m14 21.59-5-5L10.41 15 14 18.59 21.59 11 23 12.41 14 21.59z",
        ],
        "people": [
            "M11 16a5 5 0 1 1 5-5 5 5 0 0 1-5 5zm0-8a3 3 0 1 0 3 3 3 3 0 0 0-3-3zm10 10a4 4 0 1 1 4-4 4 4 0 0 1-4 4zm0-6a2 2 0 1 0 2 2 2 2 0 0 0-2-2z",
            "M2 30h2v-4a5 5 0 0 1 10 0v4h2v-4a7 7 0 0 0-14 0zm15 0h2v-3a4 4 0 0 1 8 0v3h2v-3a6 6 0 0 0-12 0z",
        ],
        "microscope": [
            "M24 28v-2h-3.68a6.93 6.93 0 0 0 1.68-5c0-1.43-.06-3.25-1.15-4.71a6.79 6.79 0 0 1-1.36-4.94 3.31 3.31 0 0 0-.87-2.94 5.38 5.38 0 0 0-.95-.65L16 2l-1.67 5.76a5.38 5.38 0 0 0-.95.65 3.31 3.31 0 0 0-.87 2.94 6.79 6.79 0 0 1-1.36 4.94c-1.09 1.46-1.15 3.28-1.15 4.71a6.93 6.93 0 0 0 1.68 5H8v2zm-7-2h-2v-2h2zm-5-5c0-1.33.05-2.57.75-3.51a8.59 8.59 0 0 0 1.77-6.13c0-.73.27-1.13.82-1.21a2.66 2.66 0 0 0 1.66-1 2.66 2.66 0 0 0 1.66 1c.55.08.82.48.82 1.21a8.59 8.59 0 0 0 1.77 6.13c.7.94.75 2.18.75 3.51a4.88 4.88 0 0 1-4 4.88V19h-2v2.88A4.88 4.88 0 0 1 12 17z"
        ],
    }
    body = "".join(f'<path d="{p}"/>' for p in paths.get(name, paths["document"]))
    return f'<svg class="{class_name}" viewBox="0 0 32 32" fill="currentColor" aria-hidden="true">{body}</svg>'


def stat_tile(value: str, label: str, context: str, icon: str) -> str:
    return f"""
    <div class="stat-tile">
      <div class="stat-tile-header">{svg_icon(icon, "stat-tile-icon")}</div>
      <div class="stat-value">{esc(value)}</div>
      <div class="stat-label">{esc(label)}</div>
      <div class="stat-context">{esc(context)}</div>
    </div>
    """


def callout(title: str, body: str, severity: str = "info") -> str:
    icon_name = "warning" if severity in {"warning", "critical"} else "info"
    return f"""
    <aside class="cds-callout cds-callout-{severity}">
      {svg_icon(icon_name, "cds-callout-icon")}
      <div class="cds-callout-body">
        <div class="cds-callout-title">{esc(title)}</div>
        <p>{esc(body)}</p>
      </div>
    </aside>
    """


def table_html(
    caption: str,
    columns: list[str],
    rows: list[list[object]],
    numeric_cols: set[int] | None = None,
    fixed: bool = False,
    col_widths: list[int] | None = None,
    delta_cols: set[int] | None = None,
    extra_class: str = "",
) -> str:
    numeric_cols = numeric_cols or set()
    delta_cols = delta_cols or set()
    table_attrs = 'class="cds-table"'
    if fixed:
        table_attrs = 'class="cds-table" data-layout="cds-table--fixed"'
    colgroup = ""
    if fixed and col_widths:
        colgroup = "<colgroup>" + "".join(f'<col style="width: {w}%;">' for w in col_widths) + "</colgroup>"
    head = "".join(f'<th scope="col">{esc(col)}</th>' for col in columns)
    body_rows = []
    for row in rows:
        cells = []
        for idx, value in enumerate(row):
            classes_td = []
            content = esc(value)
            if idx in numeric_cols:
                classes_td.append("cds-numeric")
            if idx in delta_cols:
                classes_td.append("cds-delta-cell")
                width = min(100, abs(num(value)) * 1000) if not math.isnan(num(value)) else 0
                content = f'<span>{content}</span><span class="delta-bar" style="width: {width:.0f}%;"></span>'
            class_attr = f' class="{" ".join(classes_td)}"' if classes_td else ""
            cells.append(f"<td{class_attr}>{content}</td>")
        body_rows.append("<tr>" + "".join(cells) + "</tr>")
    wrapper_class = "cds-table-wrapper" + (f" {extra_class}" if extra_class else "")
    return f"""
    <div class="{wrapper_class}">
      <div class="cds-table-caption"><span class="cds-table-caption-label">{esc(caption)}</span></div>
      <table {table_attrs}>
        {colgroup}
        <thead><tr>{head}</tr></thead>
        <tbody>{''.join(body_rows)}</tbody>
      </table>
    </div>
    """


def bar_row(label: str, value: float, max_value: float = 1.0, variant: str = "blue", fmt_digits: int = 3) -> str:
    width = 0 if max_value <= 0 else max(0, min(100, value / max_value * 100))
    return f"""
    <div class="bar-row">
      <div class="bar-label">{esc(label)}</div>
      <div class="bar-track"><div class="bar-fill bar-fill-{variant}" style="width: {width:.1f}%;"></div></div>
      <div class="bar-value">{fmt(value, fmt_digits)}</div>
    </div>
    """


def figure_block(title: str, note: str, inner: str) -> str:
    return f"""
    <figure class="cds-figure">
      <figcaption>{esc(title)}</figcaption>
      <div class="figure-body">{inner}</div>
      <p class="figure-note">{esc(note)}</p>
    </figure>
    """


def section_header(n: int, title: str) -> str:
    sid = f"bolum-{n:02d}"
    return f"""
    <div class="section-header-group">
      <span class="section-number">BÖLÜM {n:02d}</span>
      <h2 id="{sid}">{esc(title)}</h2>
    </div>
    """


def section_banner(n: int, title: str, eyebrow: str) -> str:
    return f"""
    <div class="cds-section-banner">
      {svg_icon("document", "cds-banner-icon")}
      <div class="cds-section-banner-eyebrow">{esc(eyebrow)} · Bölüm {n:02d}</div>
      <h2 id="bolum-{n:02d}" class="cds-section-banner-title">{esc(title)}</h2>
    </div>
    """


def reliability_figure(reliability: list[dict[str, str]]) -> str:
    rows = []
    for metric, title in [("alpha_raw", "Cronbach alpha"), ("omega_total", "McDonald omega")]:
        parts = [f'<div class="mini-panel"><h3>{esc(title)}</h3>']
        for form in ["EMBU-P", "EMBU-C"]:
            parts.append(f'<div class="panel-kicker">{esc(form)}</div>')
            for row in reliability:
                if row.get("form") == form:
                    label = NICE_SUBSCALE.get(row.get("subscale", ""), row.get("subscale", ""))
                    variant = "blue" if form == "EMBU-P" else "teal"
                    parts.append(bar_row(label, num(row.get(metric)), 1.0, variant))
        parts.append("</div>")
        rows.append("".join(parts))
    note = "Kesikli .70 eşiği pratik bir uyarı düzeyidir; EMBU-C Reddetme bu çizgiye ulaşırken EMBU-P Reddetme belirgin biçimde aşağıda kalır."
    return figure_block("Güvenilirlik katsayıları", note, '<div class="two-col-figure">' + "".join(rows) + "</div>")


def floor_figure(item_desc_p: list[dict[str, str]], item_desc_c: list[dict[str, str]]) -> str:
    rows = []
    for form, data in [("EMBU-P", item_desc_p), ("EMBU-C", item_desc_c)]:
        cells = []
        for row in sorted(data, key=lambda r: item_number(r.get("item", ""))):
            floor = num(row.get("floor_pct"))
            subscale = row.get("subscale", "")
            sub = subscale.replace("asiri_koruma", "asiri").replace("karsilastirma", "kars")
            cells.append(f'<span class="floor-cell floor-{sub}" title="{esc(row.get("item"))}: {fmt(floor, 1)}%" style="height: {max(8, min(42, floor * .42)):.1f}px;"></span>')
        rows.append(f'<div class="floor-strip-row"><div class="floor-strip-label">{esc(form)}</div><div class="floor-strip">{''.join(cells)}</div></div>')
    note = "Yüksek sütunlar en düşük yanıt kategorisinde yığılmayı gösterir; özellikle olumsuz ebeveynlik maddelerinde varyans daralması yaratır."
    return figure_block("Madde düzeyi taban etkisi", note, '<div class="floor-panel">' + "".join(rows) + "</div>")


def cfa_figure(cfa_fit: list[dict[str, str]], cluster_cfa: list[dict[str, str]]) -> str:
    labels = {"one_factor": "Tek faktör", "four_factor": "Dört faktör", "bifactor": "Bifaktör"}
    rows = []
    for metric, max_value, direction in [("cfi_scaled", 1.0, "yüksek iyi"), ("rmsea_scaled", 0.20, "düşük iyi"), ("srmr", 0.20, "düşük iyi")]:
        parts = [f'<div class="mini-panel"><h3>{metric.replace("_scaled", "").upper()}</h3><div class="panel-kicker">{direction}</div>']
        for row in cfa_fit:
            if row.get("model") not in labels:
                continue
            label = f'{row.get("form")} · {labels[row.get("model")]}'
            variant = "blue" if row.get("form") == "EMBU-P" else "teal"
            parts.append(bar_row(label, num(row.get(metric)), max_value, variant))
        if cluster_cfa:
            row = cluster_cfa[0]
            key = "cfi_robust" if metric == "cfi_scaled" else "rmsea_robust" if metric == "rmsea_scaled" else "srmr"
            parts.append(bar_row("EMBU-C cluster MLR", num(row.get(key)), max_value, "orange"))
        parts.append("</div>")
        rows.append("".join(parts))
    note = "Tek faktör çözümleri zayıf kalır; dört faktör çözümü daha anlamlıdır fakat CFI/SRMR profili tam doğrulanmış model iddiasını desteklemez."
    return figure_block("CFA ve cluster duyarlılığı", note, '<div class="three-col-figure">' + "".join(rows) + "</div>")


def invariance_figure(invariance: list[dict[str, str]]) -> str:
    scalar = [r for r in invariance if r.get("level") == "scalar" and is_missing_text(r.get("error"))]
    parts = ['<div class="mini-panel wide-panel"><h3>Scalar CFI</h3>']
    for row in sorted(scalar, key=lambda r: num(r.get("cfi_scaled")), reverse=True):
        label = f'{NICE_FORM.get(row.get("form", ""), row.get("form", ""))} · {row.get("group_var")} · {NICE_ITEM_SET.get(row.get("item_set", ""), row.get("item_set", ""))}'
        parts.append(bar_row(label, num(row.get("cfi_scaled")), 1.0, "blue"))
    parts.append("</div>")
    note = "DM-Kontrol ve aile rolü modelleri raporlanabilir çizgi verir; yaş/cinsiyet duyarlılıkları binary daraltma üzerinden destek analizi olarak okunmalıdır."
    return figure_block("Ölçüm değişmezliği scalar CFI", note, "".join(parts))


def icc_figure(icc: list[dict[str, str]], concordance: list[dict[str, str]]) -> str:
    rows = []
    parts = ['<div class="mini-panel"><h3>Aile içi ICC</h3>']
    for row in icc:
        label = NICE_SUBSCALE.get(row.get("score", "").replace("_mean", ""), row.get("score", ""))
        parts.append(bar_row(label, num(row.get("icc_adjusted")), 0.6, "teal"))
    parts.append("</div>")
    rows.append("".join(parts))
    parts = ['<div class="mini-panel"><h3>İndeks-kardeş ICC(2,1)</h3>']
    for row in concordance:
        label = NICE_SUBSCALE.get(row.get("subscale", ""), row.get("subscale", ""))
        parts.append(bar_row(label, num(row.get("icc_2_1_agreement")), 0.6, "blue"))
    parts.append("</div>")
    rows.append("".join(parts))
    note = "Sıcaklık en yüksek, Reddetme en düşük indeks-kardeş anlaşmasını verir; bu örüntü aile içi farklılaşma yorumunu güçlendirir."
    return figure_block("Aile içi ICC ve kardeş anlaşması", note, '<div class="two-col-figure">' + "".join(rows) + "</div>")


def validity_figure(validity: list[dict[str, str]]) -> str:
    rows = []
    for row in validity:
        if row.get("analysis") == "EMBU-P vs Beck total":
            label = f'EMBU-P {NICE_SUBSCALE.get(row.get("x", "").replace("_mean", ""), row.get("x", ""))} x Beck'
            family = "blue"
        elif "EMBU-C comparison" in row.get("analysis", ""):
            label = f'EMBU-C Karşılaştırma x {NICE_SRQ.get(row.get("y", ""), row.get("y", ""))}'
            family = "teal"
        else:
            label = f'EMBU-P Karşılaştırma x {NICE_SRQ.get(row.get("y", ""), row.get("y", ""))}'
            family = "orange"
        rho = num(row.get("spearman_rho"))
        left = pct_width(rho, -0.35, 0.35)
        sig = "sig" if num(row.get("p_value")) < 0.05 else "nonsig"
        rows.append(f"""
        <div class="rho-row">
          <div class="rho-label">{esc(short_text(label, 42))}</div>
          <div class="rho-track"><span class="rho-zero"></span><span class="rho-dot rho-{family} rho-{sig}" style="left: {left:.1f}%;"></span></div>
          <div class="rho-value">{fmt(rho)}</div>
        </div>
        """)
    note = "Noktaların sıfırdan uzaklığı etki büyüklüğünü gösterir; dolu noktalar p < .05 sonuçlarını temsil eder."
    return figure_block("Nomolojik geçerlik korelasyonları", note, '<div class="rho-panel">' + "".join(rows) + "</div>")


def multiverse_figure(multiverse: list[dict[str, str]]) -> str:
    names = {
        "S1_full_8_item_4_category": "8 madde / 4 kategori",
        "S2_collapsed_3_category": "8 madde / 3 kategori",
        "S3_low_citc_removed_4_item": "Düşük CITC çıkarılmış",
        "BSEM_latent_factor": "BSEM latent faktör",
    }
    rows = []
    lo, hi = -0.25, 0.15
    for row in multiverse:
        estimate = num(row.get("estimate_dm_minus_kontrol"))
        se = num(row.get("se"))
        ci_low = estimate - 1.96 * se
        ci_high = estimate + 1.96 * se
        left = pct_width(ci_low, lo, hi)
        width = max(1.0, pct_width(ci_high, lo, hi) - left)
        dot = pct_width(estimate, lo, hi)
        rows.append(f"""
        <div class="ci-row">
          <div class="ci-label">{esc(names.get(row.get("strategy", ""), row.get("strategy", "")))}</div>
          <div class="ci-track"><span class="rho-zero"></span><span class="ci-bar" style="left: {left:.1f}%; width: {width:.1f}%;"></span><span class="ci-dot" style="left: {dot:.1f}%;"></span></div>
          <div class="ci-value">{fmt(estimate)}</div>
        </div>
        """)
    note = "Tüm stratejiler negatif yönde olsa da güven aralıkları sıfırı keser; güçlü ve kararlı grup farkı kanıtı oluşmaz."
    return figure_block("Reddetme multiverse eğrisi", note, '<div class="ci-panel">' + "".join(rows) + "</div>")


def build_report() -> str:
    data_audit = read_csv("psychval_data_audit.csv")
    summary_metrics = read_csv("psychval_summary_metrics.csv")
    reliability = read_csv("psychval_reliability.csv")
    item_desc_p = read_csv("psychval_item_descriptives_embu_p.csv")
    item_desc_c = read_csv("psychval_item_descriptives_embu_c.csv")
    cfa_fit = read_csv("psychval_cfa_fit.csv")
    cluster_cfa = read_csv("psychval_cluster_cfa_sensitivity.csv")
    invariance = read_csv("psychval_measurement_invariance.csv")
    category_audit = read_csv("psychval_invariance_category_audit.csv")
    icc = read_csv("psychval_icc_embu_c.csv")
    concordance = read_csv("psychval_within_family_concordance.csv")
    validity = read_csv("psychval_validity_correlations.csv")
    multiverse = read_csv("psychval_rejection_multiverse.csv")
    tost = read_csv("psychval_rejection_tost.csv")
    bsem_status = read_csv("psychval_bsem_status.csv")
    bsem_fit = read_csv("psychval_bsem_fit_measures.csv")
    bsem_conv = read_csv("psychval_bsem_convergence.csv")
    cfa_loadings = read_csv("psychval_cfa_loadings.csv")
    modification_indices = read_csv("psychval_modification_indices.csv")
    item_total = read_csv("psychval_item_total.csv")
    scores_family = read_csv("psychval_scores_family.csv")
    final_family = read_csv_path(ROOT / "data" / "processed" / "FINAL_REFERENCE__analysis_base_family.csv")
    final_long = read_csv_path(ROOT / "data" / "processed" / "FINAL_REFERENCE__analysis_base_long.csv")

    family_rows = metric_value(summary_metrics, "family_rows")
    long_rows = metric_value(summary_metrics, "long_rows")
    p_rej_alpha = metric_value(summary_metrics, "embu_p_reddetme_alpha_raw")
    c_rej_alpha = metric_value(summary_metrics, "embu_c_reddetme_alpha_raw")
    dyad_rej_icc = metric_value(summary_metrics, "index_sibling_reddetme_icc_2_1")

    p_rej_omega = next((num(r.get("omega_total")) for r in reliability if r.get("form") == "EMBU-P" and r.get("subscale") == "reddetme"), math.nan)
    c_rej_omega = next((num(r.get("omega_total")) for r in reliability if r.get("form") == "EMBU-C" and r.get("subscale") == "reddetme"), math.nan)
    bsem_ppp = next((num(r.get("value")) for r in bsem_fit if r.get("analysis") == "EMBU-P four_factor BSEM full_29" and r.get("measure") == "ppp"), math.nan)

    summary_rows = [
        ["EMBU-P Reddetme güvenilirliği", f"alpha = {fmt(p_rej_alpha)}"],
        ["EMBU-C Reddetme güvenilirliği", f"alpha = {fmt(c_rej_alpha)}"],
        ["İndeks-kardeş Reddetme uyumu", f"ICC(2,1) = {fmt(dyad_rej_icc)}"],
        ["BSEM full model PPP", f"PPP = {fmt(bsem_ppp)}"],
        [
            "Cluster duyarlılık CFA",
            f"CFI = {fmt(cluster_cfa[0].get('cfi_robust') if cluster_cfa else math.nan)}, RMSEA = {fmt(cluster_cfa[0].get('rmsea_robust') if cluster_cfa else math.nan)}, SRMR = {fmt(cluster_cfa[0].get('srmr') if cluster_cfa else math.nan)}",
        ],
        ["Yaş/cinsiyet binary MI", "Binary MI raporlanabilir"],
    ]

    audit_rows = [
        [
            "family CSV" if "family" in row.get("file", "") else "long CSV",
            fmt_int(row.get("rows")),
            fmt_int(row.get("columns")),
            row.get("hash_ok", ""),
        ]
        for row in data_audit
    ]

    reliability_rows = [
        [
            row.get("form"),
            NICE_SUBSCALE.get(row.get("subscale", ""), row.get("subscale", "")),
            fmt2(row.get("alpha_raw")),
            fmt2(row.get("omega_total")),
            fmt2(row.get("omega_h")),
        ]
        for row in reliability
        if row.get("form") in {"EMBU-P", "EMBU-C"}
    ]
    cr_ave_rows = compute_cr_ave(cfa_loadings, reliability)
    rejection_rows = rejection_item_diagnostics(item_desc_p, item_desc_c, item_total, reliability)
    htmt_rows = htmt_for_rows(final_family, "embu_p", "EMBU-P") + htmt_for_rows(final_long, "embu_c", "EMBU-C")
    age_alpha_rows = compute_age_alpha_rows(final_long)
    beck_severity_rows = compute_beck_severity_rows(scores_family)
    modification_rows = top_modification_rows(modification_indices)

    cfa_rows = [
        [
            row.get("form"),
            {"one_factor": "Tek faktör", "four_factor": "Dört faktör", "bifactor": "Bifaktör"}.get(row.get("model"), row.get("model")),
            fmt(row.get("cfi_scaled")),
            fmt(row.get("rmsea_scaled")),
            fmt(row.get("srmr")),
        ]
        for row in cfa_fit
        if row.get("model") in {"one_factor", "four_factor", "bifactor"}
    ]

    cluster_rows = [
        [
            row.get("method"),
            fmt_int(row.get("n_obs")),
            fmt_int(row.get("n_clusters")),
            fmt(row.get("cfi_robust")),
            fmt(row.get("rmsea_robust")),
            fmt(row.get("srmr")),
            row.get("converged"),
        ]
        for row in cluster_cfa
    ]

    audit_grouped: dict[tuple[str, str, str], dict[str, float]] = {}
    for row in category_audit:
        key = (row.get("group_var", ""), row.get("item_set", ""), row.get("scheme", ""))
        rec = audit_grouped.setdefault(key, {"empty_items": 0, "empty_cells": 0, "min_cell": math.inf})
        rec["empty_items"] += 1 if str(row.get("has_empty_cell", "")).upper() == "TRUE" else 0
        rec["empty_cells"] += num(row.get("empty_cell_count")) if not math.isnan(num(row.get("empty_cell_count"))) else 0
        min_cell = num(row.get("min_cell"))
        if not math.isnan(min_cell):
            rec["min_cell"] = min(rec["min_cell"], min_cell)
    category_rows = [
        [
            key[0],
            NICE_ITEM_SET.get(key[1], key[1]),
            NICE_SCHEME.get(key[2], key[2]),
            fmt_int(val["empty_items"]),
            fmt_int(val["empty_cells"]),
            fmt_int(val["min_cell"]),
        ]
        for key, val in sorted(audit_grouped.items())
    ]

    inv_success_rows = [
        [
            NICE_FORM.get(row.get("form", ""), row.get("form", "")),
            row.get("group_var"),
            NICE_ITEM_SET.get(row.get("item_set", ""), row.get("item_set", "")),
            row.get("level"),
            fmt(row.get("cfi_scaled")),
            fmt(row.get("rmsea_scaled")),
            fmt(row.get("srmr")),
            "NA" if row.get("delta_cfi", "") == "" else fmt(row.get("delta_cfi")),
        ]
        for row in invariance
        if is_missing_text(row.get("error"))
    ]
    inv_failure_rows = [
        [
            NICE_FORM.get(row.get("form", ""), row.get("form", "")),
            row.get("group_var"),
            NICE_ITEM_SET.get(row.get("item_set", ""), row.get("item_set", "")),
            short_text(row.get("error"), 76),
        ]
        for row in invariance
        if not is_missing_text(row.get("error"))
    ]
    inv_failure_rows_p = [row for row in inv_failure_rows if str(row[0]).startswith("EMBU-P")]
    inv_failure_rows_c = [row for row in inv_failure_rows if str(row[0]).startswith("EMBU-C")]

    concordance_rows = [
        [
            NICE_SUBSCALE.get(row.get("subscale", ""), row.get("subscale", "")),
            fmt_int(row.get("n_pairs")),
            fmt(row.get("icc_2_1_agreement")),
            fmt(row.get("mean_difference_idx_minus_sib")),
            fmt(row.get("loa_lower")),
            fmt(row.get("loa_upper")),
        ]
        for row in concordance
    ]

    validity_rows = []
    validity_q_values = bh_fdr([row.get("p_value") for row in validity])
    for row, q_value in zip(validity, validity_q_values):
        if row.get("analysis") == "EMBU-P vs Beck total":
            label = f'EMBU-P {NICE_SUBSCALE.get(row.get("x", "").replace("_mean", ""), row.get("x", ""))} x Beck'
        elif "EMBU-C comparison" in row.get("analysis", ""):
            label = f'EMBU-C Karşılaştırma x {NICE_SRQ.get(row.get("y", ""), row.get("y", ""))}'
        else:
            label = f'EMBU-P Karşılaştırma x {NICE_SRQ.get(row.get("y", ""), row.get("y", ""))}'
        validity_rows.append([short_text(label, 52), fmt_int(row.get("n")), fmt2(row.get("spearman_rho")), fmt_p(row.get("p_value")), fmt_p(q_value)])

    strategy_names = {
        "S1_full_8_item_4_category": "8 madde/4 kat.",
        "S2_collapsed_3_category": "8 madde/3 kat.",
        "S3_low_citc_removed_4_item": "Düşük CITC çıkar.",
        "BSEM_latent_factor": "BSEM latent",
    }
    multiverse_rows = [
        [
            strategy_names.get(row.get("strategy", ""), row.get("strategy", "")),
            fmt_int(row.get("n")),
            fmt(row.get("estimate_dm_minus_kontrol")),
            fmt(row.get("se")),
            fmt_p(row.get("p_value")),
            fmt(row.get("cohens_d_dm_minus_kontrol")),
        ]
        for row in multiverse
    ]

    tost_rows = [
        [
            strategy_names.get(row.get("strategy", ""), row.get("strategy", "")),
            f'{fmt_int(row.get("n_dm"))}/{fmt_int(row.get("n_kontrol"))}',
            fmt(row.get("hedges_g")),
            f'[{fmt(row.get("g_ci_lower_90"))}, {fmt(row.get("g_ci_upper_90"))}]',
            fmt_p(row.get("tost_lower_p")),
            fmt_p(row.get("tost_upper_p")),
            "Evet" if str(row.get("equivalent_at_smd_030", "")).upper() == "TRUE" else "Hayır",
        ]
        for row in tost
    ]

    conv_by_key = {(r.get("analysis"), r.get("item_set")): r for r in bsem_conv}
    bsem_diag_rows = []
    for row in bsem_status:
        conv = conv_by_key.get((row.get("analysis"), row.get("item_set")), {})
        bsem_diag_rows.append(
            [
                "q12siz BSEM" if "q12" in row.get("analysis", "") else "full BSEM",
                NICE_ITEM_SET.get(row.get("item_set", ""), row.get("item_set", "")),
                row.get("status"),
                fmt_int(row.get("n_chains")),
                fmt_int(row.get("burnin")),
                fmt_int(row.get("sample")),
                fmt_int(row.get("seed")),
                fmt(conv.get("max_rhat")),
                fmt(conv.get("min_neff")),
            ]
        )

    bsem_fit_rows = [
        [
            "q12siz BSEM" if "q12" in row.get("analysis", "") else "full BSEM",
            NICE_ITEM_SET.get(row.get("item_set", ""), row.get("item_set", "")),
            row.get("measure", "").upper(),
            fmt(row.get("value")),
        ]
        for row in bsem_fit
        if row.get("measure") in {"ppp", "dic", "waic", "looic"}
    ]

    sample_size_rows = [
        [
            "Family tabanı",
            fmt_int(family_rows),
            "EMBU-P, Beck, aile düzeyi SRQ",
            "Aile başına tek gözlem; grup karşılaştırmaları ve anne bildirimi için ana taban.",
        ],
        [
            "Long taban",
            fmt_int(long_rows),
            "EMBU-C, kardeş konkordansı, HTMT",
            "İki çocuk satırı/aile yapısı korunur; bağımsızlık varsayımı ICC ve cluster duyarlılıkla kontrol edilir.",
        ],
        [
            "CFA gözlem/madde oranı",
            f"{fmt_int(long_rows)}/29",
            "EMBU-C dört faktör",
            "Ordinal CFA için örneklem büyüklüğü raporlanabilir; seyrek kategori riski MI bölümünde ayrıca denetlenir.",
        ],
        [
            "Reddetme item tanısı",
            "8+8 madde",
            "EMBU-P ve EMBU-C",
            "Düşük CITC, taban etkisi ve alpha-if-deleted aynı tabloda birlikte yorumlanır.",
        ],
    ]

    compliance_rows = [
        ["ITC çeviri/adaptasyon", "Kısmi", "Bu PDF psikometrik kanıta odaklanır; dilsel eşdeğerlik ve uzman panel süreci yöntem metninde ayrı referanslanmalıdır."],
        ["COSMIN iç tutarlılık", "Tam", "Alpha, omega, madde-toplam korelasyonu, taban/tavan etkisi ve alt ölçek düzeyinde n raporlandı."],
        ["COSMIN yapı geçerliği", "Tam", "CFA, CR/AVE, HTMT, modification index ve dış ölçüt korelasyonları birlikte sunuldu."],
        ["COSMIN ölçüm değişmezliği", "Kısmi", "DM/Kontrol ve aile rolü raporlanabilir; yaş/cinsiyet özgün kategorilerde seyrek hücre nedeniyle destek analizi olarak kaldı."],
        ["Açık bilim/reprodüksiyon", "Tam", "Kanonik veri kilidi, SHA doğrulaması, script tabanlı HTML/PDF üretimi ve sabit çıktı yolları kullanıldı."],
    ]

    evidence_rows = [
        ["EMBU-C iç tutarlılık", "Orta-yüksek", "Alpha/omega Reddetme ve Karşılaştırma için kabul edilebilir; Aşırı koruma daha sınırlı."],
        ["EMBU-P Reddetme", "Düşük", "Alpha/omega düşük, taban etkisi yoğun, CITC bazı maddelerde zayıf."],
        ["Faktör yapısı", "Orta", "Dört faktör tek faktöre üstün; ancak uyum indeksleri tam doğrulanmış model iddiasını desteklemez."],
        ["Aile içi farklılaşma", "Orta", "Kardeş konkordansı ve LoA parental differential treatment yorumunu destekler."],
        ["Nomolojik ağ", "Orta", "Beklenen yönler korunur; etki büyüklükleri küçük-orta aralığındadır ve FDR ile ayrıca işaretlenmiştir."],
    ]

    today = date.today().strftime("%d.%m.%Y")
    toc_items = [
        "Yönetici Özeti",
        "Veri Kilidi ve Kapsam",
        "Güvenilirlik ve Madde Davranışı",
        "Faktör Yapısı ve Model Uyumu",
        "Ölçüm Değişmezliği",
        "Aile İçi Yapı ve Kardeş Konkordansı",
        "Nomolojik Ağ: Beck ve SRQ/KIA",
        "Reddetme Multiverse, TOST ve BSEM Duyarlılığı",
        "Yorum ve Raporlama Kararı",
    ]

    css = build_css()
    html_parts = [
        "<!DOCTYPE html>",
        '<html lang="tr">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>Psikometrik Validasyon Bütünleşik Raporu - Carbon</title>",
        f"<style>{css}</style>",
        '<script src="https://unpkg.com/pagedjs/dist/paged.polyfill.js"></script>',
        "</head>",
        "<body>",
        f"""
        <div class="cover-page">
          {svg_icon("analytics", "cover-pictogram")}
          {svg_icon("shield", "cover-pictogram-badge")}
          <div class="cover-header">
            <div class="cover-eyebrow">Carbon HTML Report · Psikometrik Validasyon</div>
            <span class="cover-issue-chip">Kilitli final veri</span>
          </div>
          <div class="cover-title-block">
            <h1 class="cover-title">Psikometrik Validasyon Bütünleşik Raporu</h1>
            <p class="cover-subtitle">EMBU-P / EMBU-C, Beck Depresyon Envanteri ve KIA/SRQ sonuçları</p>
          </div>
          <div class="cover-meta-grid">
            <div class="cover-meta-item"><div class="cover-meta-label">Analiz tabanı</div><div class="cover-meta-value">{fmt_int(family_rows)} aile · {fmt_int(long_rows)} çocuk satırı</div></div>
            <div class="cover-meta-item"><div class="cover-meta-label">Tasarım</div><div class="cover-meta-value">Kardeşli dyadic yapı</div></div>
            <div class="cover-meta-item"><div class="cover-meta-label">Stil kaynağı</div><div class="cover-meta-value">IBM Carbon v11</div></div>
          </div>
          <div class="cover-footer">
            <div class="cover-classification">Metodolojik ek · adaptasyon makalesi</div>
            <div class="cover-date">{today}</div>
          </div>
        </div>
        """,
        """
        <div class="toc-page">
          <h2>İçindekiler</h2>
          <ol class="toc-list">
        """,
    ]
    for idx, title in enumerate(toc_items, 1):
        html_parts.append(f'<li><span class="toc-number">{idx:02d}</span><a href="#bolum-{idx:02d}">{esc(title)}</a></li>')
    html_parts.append("</ol></div>")

    html_parts.append(f"""
    <section id="s1" class="report-section">
      {section_banner(1, "Yönetici Özeti", "Ana karar yüzeyi")}
      <div class="executive-summary">
        <p>Bu rapor, kilitli final referans veri üzerinde üretilen psikometrik validasyon sonuçlarını tek Carbon PDF yüzeyinde birleştirir. Analiz tabanı <strong>{fmt_int(family_rows)} aile</strong> ve <strong>{fmt_int(long_rows)} çocuk satırı</strong>dır; ham veri veya kimliklenebilir alan kullanılmamıştır.</p>
        <p>Raporun amacı tek bir geçti/kaldı kararı üretmek değil, EMBU-P ve EMBU-C formlarının bu örneklemde hangi kanıt türlerinde güçlü, hangi kanıt türlerinde kırılgan davrandığını açık biçimde göstermektir.</p>
      </div>
      <div class="stat-grid stat-grid-4">
        {stat_tile(fmt_int(family_rows), "Aile", "family CSV analiz tabanı", "people")}
        {stat_tile(fmt_int(long_rows), "Çocuk satırı", "indeks çocuk + kardeş long taban", "document")}
        {stat_tile(fmt(c_rej_alpha), "EMBU-C Reddetme alpha", "çocuk bildiriminde kabul edilebilir sinyal", "analytics")}
        {stat_tile(fmt(p_rej_alpha), "EMBU-P Reddetme alpha", "anne öz-bildiriminde sınırlı iç tutarlılık", "warning")}
      </div>
      {table_html("Ana sonuçların kısa yorumu", ["Alan", "Bulgu"], summary_rows, fixed=True, col_widths=[48, 52])}
      <p>Ana bulgu örüntüsü nettir: EMBU-C, özellikle Reddetme ve Karşılaştırma eksenlerinde daha kullanılabilir psikometrik sinyal verirken EMBU-P Reddetme alt ölçeği düşük iç tutarlılık ve yoğun taban etkisi nedeniyle metodolojik ekte sınırlılık olarak ele alınmalıdır. BSEM duyarlılığı, klasik toplam puan sonuçlarını tamamlayan latent değişken kontrolü olarak sunulmuştur.</p>
    </section>
    """)

    html_parts.append(f"""
    <section id="s2" class="report-section">
      {section_header(2, "Veri Kilidi ve Kapsam")}
      <p>Kanonik veri kilidi, bu rapordaki sayısal sonuçların hangi analiz tabanından üretildiğini doğrular. family CSV aile düzeyindeki tekil satırları, long CSV ise indeks çocuk ve kardeş satırlarını taşır. SHA-256 uyumunun TRUE olması, sonuçların kilitli final referans dosyalarına bağlı kaldığını gösterir.</p>
      {callout("İstatistik yöntem kutusu: analiz birimi ve veri kilidi", "Temel analiz birimi soruya göre değişir. Aile düzeyi sonuçlarda 241 ailelik family tabanı, çocuk ve kardeş algılarını içeren psikometrik sonuçlarda 482 satırlık long taban kullanılır. Kardeş satırları aynı aileden geldiği için bağımsızlık varsayımı sınırlıdır; bu nedenle aile içi ICC, indeks-kardeş konkordansı ve cluster duyarlılık analizleri ayrıca raporlanır.", "info")}
      {table_html("Kanonik veri kilidi doğrulaması", ["Dosya", "Satır", "Kolon", "SHA-256 uyumu"], audit_rows, numeric_cols={1, 2}, fixed=True, col_widths=[34, 18, 18, 30])}
      {table_html("Örneklem, analiz birimi ve raporlama kapsamı", ["Taban", "n", "Kullanım", "Yorum"], sample_size_rows, numeric_cols={1}, fixed=True, col_widths=[18, 12, 26, 44])}
      <p>Bu kapsam, kardeşli tasarımın iki düzeyli yapısını korur: aile düzeyi karşılaştırmalar family CSV üzerinden, çocuk/kardeş düzeyi psikometrik ve konkordans bulguları long CSV üzerinden okunmalıdır. Bu ayrım özellikle EMBU-C, SRQ/KIA ve aile içi ICC yorumlarında bağımsız gözlem varsayımını gereksiz yere güçlendirmemek için önemlidir.</p>
    </section>
    """)

    html_parts.append(f"""
    <section id="s3" class="report-section">
      {section_header(3, "Güvenilirlik ve Madde Davranışı")}
      <p>Güvenilirlik bölümü iki tamamlayıcı soruya yanıt verir. Birincisi, alt ölçek puanlarının iç tutarlılığı kabul edilebilir düzeyde mi; ikincisi, madde yanıt dağılımları bu iç tutarlılığı destekleyecek kadar varyans içeriyor mu? Bu nedenle alpha ve omega katsayıları madde düzeyi taban etkisiyle birlikte yorumlanmıştır.</p>
      {callout("İstatistik yöntem kutusu: alpha, omega ve taban etkisi", "Cronbach alpha maddelerin ortak varyansını klasik test kuramı içinde özetler; McDonald omega ise faktör yüklerine dayalı daha esnek bir iç tutarlılık ölçüsüdür. Alpha ve omega birlikte düşükse sorun yalnız alpha varsayımlarından değil, madde havuzunun zayıf ortak sinyal üretmesinden kaynaklanabilir.", "warning")}
      {reliability_figure(reliability)}
      <p>EMBU-C Reddetme için alpha {fmt(c_rej_alpha)} ve omega {fmt(c_rej_omega)} iken EMBU-P Reddetme için alpha {fmt(p_rej_alpha)} ve omega {fmt(p_rej_omega)} düzeyindedir. Bu ayrışma, reddedici ebeveynlik içeriğinin çocuk bildiriminde daha tutarlı yakalandığını, anne öz-bildiriminde ise aynı madde havuzunun daha zayıf sinyal ürettiğini düşündürür.</p>
      {floor_figure(item_desc_p, item_desc_c)}
      <p>Toplam {sum(1 for r in item_desc_p + item_desc_c if num(r.get("floor_pct")) >= 80)} madde-form noktası yüzde 80 veya üzerinde taban etkisi göstermektedir; bu nedenle Reddetme sonuçları yalnız toplam puan düzeyinde değil, madde dağılımı düzeyinde de temkinli okunmalıdır.</p>
      {table_html("Ana güvenilirlik katsayıları", ["Form", "Alt ölçek", "alpha", "omega", "omega_h"], reliability_rows, numeric_cols={2, 3, 4}, fixed=True, col_widths=[18, 28, 18, 18, 18])}
      <p>Omega değerleri alpha ile aynı yönlü olduğu için düşük Reddetme bulgusunu yalnız alpha varsayımlarına bağlamak doğru değildir; sorun daha temel olarak madde havuzunun bu örneklemde ürettiği varyans ve faktör homojenliğiyle ilişkilidir.</p>
      {table_html("Reddetme maddeleri: dağılım ve corrected item-total correlation", ["Form", "Madde", "M", "SS", "Skew", "Taban", "CITC", "alpha silinirse", "İşaret"], rejection_rows, numeric_cols={2, 3, 4, 5, 6, 7}, fixed=True, col_widths=[11, 8, 8, 8, 8, 10, 9, 14, 24])}
      <p>Madde tanısı EMBU-P tarafında iki soruna işaret eder: yanıtların büyük kısmı en düşük kategoride toplanır ve bazı maddeler ölçek toplamıyla zayıf ilişki kurar. EMBU-C'de taban etkisi yine görünür olsa da CITC değerleri daha tutarlı bir ortak faktör sinyali verir.</p>
      {table_html("EMBU-C yaş kademelerine göre alpha", ["Yaş", "n", "Sıcaklık", "Aşırı koruma", "Reddetme", "Karşılaştırma"], age_alpha_rows, fixed=True, col_widths=[10, 10, 20, 20, 20, 20])}
      <p>Yaş kademeli alpha tablosu, çocuk bildiriminin yalnız toplam örneklemde değil yaş alt gruplarında da izlenebilir olup olmadığını gösterir. Hücreler alpha değerini ve ilgili alt ölçekte eksiksiz madde yanıtı veren çocuk sayısını birlikte verir; küçük yaş kademelerinde yorum güveni örneklem büyüklüğüyle sınırlıdır.</p>
    </section>
    """)

    html_parts.append(f"""
    <section id="s4" class="report-section">
      {section_banner(4, "Faktör Yapısı ve Model Uyumu", "Latent yapı")}
      <p>Faktör yapısı bölümünde tek faktör, dört faktör ve bifaktör çözümler karşılaştırılmıştır. Dört faktör çözümü teorik alt ölçek yapısını temsil eder; bifaktör çözüm genel ebeveynlik tonu ile alt boyutların aynı anda taşınıp taşınamadığını sınar. EMBU-C için ayrıca aile kümelenmesine duyarlı sürekli-MLR CFA duyarlılığı rapora eklenmiştir.</p>
      {callout("İstatistik yöntem kutusu: CFA ve uyum indeksleri", "Doğrulayıcı faktör analizi, maddelerin kuramsal alt ölçeklere ne ölçüde uyduğunu sınar. CFI gözlenen modelin bağımsız modele göre göreli uyumunu, RMSEA yaklaşık model hatasını, SRMR ise standartlaştırılmış artıkların büyüklüğünü özetler. Cluster duyarlılık CFA, kardeşlerin aynı aile içinde kümelenmesini dikkate alan ek bir sağlamlık kontrolüdür.", "info")}
      {cfa_figure(cfa_fit, cluster_cfa)}
      <p>Tek faktör çözümlerinin düşük CFI değerleri ölçeğin tek boyutlu okunmasını desteklemez. Dört faktör çözümü EMBU-P ve EMBU-C için daha anlamlıdır, ancak EMBU-P'de SRMR'nin yüksek kalması ve EMBU-C'de CFI'nin sınırda seyretmesi sonuçların tam doğrulanmış model yerine kullanılabilir ama sınırlı faktör kanıtı olarak raporlanmasını gerektirir.</p>
      {table_html("CFA model karşılaştırmaları", ["Form", "Model", "CFI", "RMSEA", "SRMR"], cfa_rows, numeric_cols={2, 3, 4}, fixed=True, col_widths=[20, 28, 17, 17, 18])}
      {table_html("Yakınsak geçerlik: CR ve AVE", ["Form", "Alt ölçek", "alpha", "omega", "CR", "AVE", "Yük min/maks", "AVE yorumu"], cr_ave_rows, numeric_cols={2, 3, 4, 5}, fixed=True, col_widths=[12, 20, 9, 9, 9, 9, 16, 16])}
      <p>CR ve AVE, faktör yüklerinden türetilen yakınsak geçerlik göstergeleridir. AVE değeri .50'ye yaklaştıkça maddelerin aynı latent yapıya daha fazla ortak varyans taşıdığı kabul edilir; EMBU-P Reddetme'nin düşük AVE/CR profili, güvenilirlik bulgusuyla aynı sınırlılık yönünde birleşir.</p>
      {table_html("Ayırt edici geçerlik: HTMT madde korelasyonu oranları", ["Form", "Boyut 1", "Boyut 2", "HTMT", "Karar"], htmt_rows, numeric_cols={3}, fixed=True, col_widths=[12, 23, 23, 14, 28])}
      <p>HTMT değerleri alt ölçeklerin birbirinden ayrışabilirliğini madde korelasyonları üzerinden denetler. .85 altında kalan çiftler ayırt edici geçerlik açısından daha rahat yorumlanır; daha yüksek değerler alt ölçekler arasında kavramsal ya da madde içerik örtüşmesi olabileceğini gösterir.</p>
      {table_html("Aile-kümelenmesi için sürekli-MLR duyarlılık CFA", ["Yöntem", "n gözlem", "n aile", "CFI", "RMSEA", "SRMR", "Yakınsadı"], cluster_rows, numeric_cols={1, 2, 3, 4, 5}, fixed=True, col_widths=[34, 12, 12, 10, 12, 10, 10]) if cluster_rows else ""}
      {table_html("Dört faktör CFA için en yüksek modification index sinyalleri", ["Form", "Tür", "Önerilen parametre", "MI", "Std EPC"], modification_rows, numeric_cols={3, 4}, fixed=True, col_widths=[12, 20, 44, 10, 14])}
      <p>Modification index listesi modelin iyileştirilebileceği yerleri gösterir, ancak bu liste otomatik model revizyonu için kullanılmamıştır. Raporlama amacı, özellikle EMBU-C q09-q10 artığı ve EMBU-P'de çapraz yük sinyalleri gibi kırılgan noktaları açıkça görünür kılmaktır.</p>
      <p>Cluster duyarlılık sonucu, aile içi bağımlılığın tamamen görmezden gelinmediğini gösteren tamamlayıcı bir kontroldür. Bu model klasik ordinal CFA'nın yerini almaktan çok, kardeşli tasarımda model uyumunun aile kümelenmesine ne kadar duyarlı olduğunu göstermek için eklenmiştir.</p>
    </section>
    """)

    html_parts.append(f"""
    <section id="s5" class="report-section">
      {section_header(5, "Ölçüm Değişmezliği")}
      <p>Ölçüm değişmezliği analizleri, aynı madde setinin gruplar arasında benzer ölçüm anlamı taşıyıp taşımadığını sınar. Bu raporda configural, metric ve scalar düzeyler birlikte izlenmiştir; scalar düzey özellikle grup ortalaması karşılaştırmalarının daha savunulabilir olmasını sağlar.</p>
      {callout("İstatistik yöntem kutusu: ölçüm değişmezliği", "Configural düzey aynı faktör yapısının gruplarda kurulabildiğini, metric düzey madde yüklerinin benzerliğini, scalar düzey ise eşik veya intercept benzerliğini sınar. Scalar düzey sağlanmadan grup ortalamalarını doğrudan karşılaştırmak daha zayıf bir kanıta dayanır.", "warning")}
      {invariance_figure(invariance)}
      <p>DM-Kontrol ve aile rolü eksenindeki EMBU-C modelleri raporlanabilir bir çizgi verirken, yaş ve cinsiyet için özgün dört kategorili yanıt yapısı bazı maddelerde boş hücre ürettiği için doğrudan kullanılamaz. Binary 1/>1 daraltması bu seyrekliği azaltır; bu nedenle yaş/cinsiyet duyarlılıkları birincil sonuç değil, metodolojik destek analizi olarak ele alınmalıdır.</p>
      {table_html("Yaş/cinsiyet MI için kategori seyrekliği denetimi", ["Grup", "Set", "Şema", "Boş madde", "Boş hücre", "Min hücre"], category_rows, numeric_cols={3, 4, 5}, fixed=True, col_widths=[17, 26, 15, 14, 14, 14])}
      {table_html("Başarılı ölçüm değişmezliği modelleri", ["Form", "Grup", "Set", "Düzey", "CFI", "RMSEA", "SRMR", "Delta CFI"], inv_success_rows, numeric_cols={4, 5, 6, 7}, fixed=True, col_widths=[18, 15, 20, 13, 9, 9, 8, 8], delta_cols={7}, extra_class="page-break-before")}
      {table_html("Tahmin edilemeyen ölçüm değişmezliği modelleri: EMBU-P", ["Form", "Grup", "Set", "Hata"], inv_failure_rows_p, fixed=True, col_widths=[20, 15, 18, 47])}
      {table_html("Tahmin edilemeyen ölçüm değişmezliği modelleri: EMBU-C", ["Form", "Grup", "Set", "Hata"], inv_failure_rows_c, fixed=True, col_widths=[20, 15, 18, 47])}
      <p>Başarısız modellerin çoğu teorik uyumsuzluktan çok kategori seyrekliği ve bazı yanıt düzeylerinin küçük alt gruplarda hiç gözlenmemesiyle ilişkilidir. Bu nedenle raporda ölçüm değişmezliği yok gibi genel bir yargı yerine, hangi grup ve hangi madde kodlamasında tahminin mümkün olduğu açıkça ayrıştırılmalıdır.</p>
    </section>
    """)

    html_parts.append(f"""
    <section id="s6" class="report-section">
      {section_header(6, "Aile İçi Yapı ve Kardeş Konkordansı")}
      <p>Kardeşli tasarım, her çocuk satırını bağımsız kabul etmeyi uygun kılmaz. Bu bölüm aile içi benzerliğin ve indeks-kardeş anlaşmasının alt ölçeklere göre ne kadar değiştiğini gösterir. ICC değerleri yüksek bir mutlak seviye beklemekten çok, hangi alt ölçeklerin aile içinde daha ortak algılandığını görmek için kullanılmıştır.</p>
      {callout("İstatistik yöntem kutusu: ICC ve LoA", "Intraclass correlation coefficient, aynı aile içindeki ya da indeks-kardeş çiftindeki puanların ne kadar benzer olduğunu özetler. ICC(2,1), tek ölçüm düzeyinde mutlak anlaşmaya odaklanan iki yönlü rastgele etkiler yaklaşımıdır. Bland-Altman limits of agreement ise kardeşler arasındaki farkların pratik aralığını verir.", "info")}
      {icc_figure(icc, concordance)}
      <p>Reddetme için ICC(2,1) {fmt(dyad_rej_icc)} düzeyindedir; bu düşük değer, aynı ailedeki iki çocuğun reddedilme algısının tam olarak örtüşmediğini ve parental differential treatment yorumuna alan açtığını gösterir. Bu bulgu, EMBU-C'nin yalnız bireysel algıyı değil, aile içi farklılaşmayı da taşıyabildiğini destekler.</p>
      {callout("Kuramsal yorum kutusu: parental differential treatment", "Kardeşlerin aynı aile içinde aynı ebeveynlik deneyimini otomatik olarak paylaştığı varsayımı bu veriyle sınırlıdır. Düşük Reddetme konkordansı, ebeveyn davranışının çocuklar tarafından farklı algılanabildiğini ya da farklı çocuklara farklı biçimde yöneldiğini gösteren metodolojik bir sinyal olarak raporlanmalıdır.", "info")}
      {table_html("İndeks-kardeş konkordansı", ["Alt ölçek", "n çift", "ICC(2,1)", "Ortalama fark", "LoA alt", "LoA üst"], concordance_rows, numeric_cols={1, 2, 3, 4, 5}, fixed=True, col_widths=[25, 12, 16, 19, 14, 14])}
      <p>LoA aralıklarının genişliği, kardeşler arasındaki farkların bazı ailelerde klinik olarak anlamlı olabilecek ölçüde açılabildiğini gösterir. Bu yüzden indeks-kardeş karşılaştırmaları yalnız ortalama fark üzerinden değil, anlaşma ve dağılım genişliği üzerinden de raporlanmalıdır.</p>
    </section>
    """)

    html_parts.append(f"""
    <section id="s7" class="report-section">
      {section_header(7, "Nomolojik Ağ: Beck ve SRQ/KIA")}
      <p>Nomolojik ağ bölümü, EMBU alt ölçeklerinin beklenen dış ölçütlerle aynı yönde ilişki verip vermediğini sınar. Beck Depresyon toplamı anne bildirimiyle, SRQ/KIA alt boyutları ise kardeş ilişkisi alanıyla bağlanmıştır. Bu bölümde p-değerleri yalnız işaretleyici olarak kullanılmış, yorumun ana ekseni etki yönü ve büyüklüğü olmuştur.</p>
      {callout("İstatistik yöntem kutusu: Spearman korelasyonu ve nomolojik ağ", "Spearman rho, değişkenler arasındaki monoton ilişkiyi sıra bilgisi üzerinden ölçer ve Likert temelli ya da çarpık dağılımlı puanlarda Pearson korelasyonuna göre daha dayanıklı bir özet sağlar. Nomolojik ağ yaklaşımında amaç yalnız p-değeri üretmek değildir; kuramsal olarak ilişkili olması beklenen alanların beklenen yönde ve makul büyüklükte ilişki verip vermediği değerlendirilir.", "info")}
      {validity_figure(validity)}
      <p>Beklenen örüntü büyük ölçüde korunmaktadır: EMBU-P Karşılaştırma ve Reddetme Beck ile pozitif, Sıcaklık Beck ile negatif ilişkilidir; EMBU-C Karşılaştırma ise SRQ Çatışma ve Rekabet ile pozitif, SRQ Sıcaklık/Yakınlık ile negatif ilişki verir. Bu yönsel tutarlılık, özellikle EMBU-C Karşılaştırma boyutunun kardeş ilişkisi bağlamında nomolojik geçerlik sinyali taşıdığını gösterir.</p>
      {table_html("Kriter ve eşzamanlı geçerlik korelasyonları", ["Karşılaştırma", "n", "rho", "p", "q(BH)"], validity_rows, numeric_cols={1, 2, 3, 4}, fixed=True, col_widths=[56, 10, 11, 11, 12])}
      <p>q(BH) sütunu aynı korelasyon ailesi içinde Benjamini-Hochberg düzeltmesiyle hesaplanan yanlış keşif oranını gösterir. Bu ek sütun, çoklu korelasyon sunumunda yalnız ham p-değerine dayanma riskini azaltır.</p>
      {table_html("Beck Depresyon Envanteri şiddet sınıfları", ["Grup", "Sınıf", "n", "%"], beck_severity_rows, numeric_cols={2, 3}, fixed=True, col_widths=[25, 35, 18, 22])}
      <p>Beck sınıflandırması, anne depresyonu dağılımının yalnız ortalama puanla özetlenmemesi için eklenmiştir. DM ve kontrol gruplarında minimal-hafif düzeyler baskın olmakla birlikte, orta ve şiddetli aralıkta kalan katılımcılar da bulunduğundan Beck ilişkileri klinik heterojenlik bağlamında yorumlanmalıdır.</p>
      <p>Korelasyon büyüklükleri çoğunlukla küçük-orta aralıktadır; bu psikososyal ölçeklerde beklenen bir durumdur ve tek başına zayıflık olarak yorumlanmamalıdır. Daha önemli olan, teorik olarak beklenen işaretlerin korunması ve aynı örüntünün anne depresyonu ile kardeş ilişkisi alanlarında ayrışabilir biçimde görünmesidir.</p>
    </section>
    """)

    html_parts.append(f"""
    <section id="s8" class="report-section">
      {section_header(8, "Reddetme Multiverse, TOST ve BSEM Duyarlılığı")}
      <p>Bu bölüm, EMBU-P Reddetme bulgusunun tek bir skor kodlamasına bağlı olup olmadığını sınar. Multiverse analizinde madde sayısı, kategori daraltma, düşük corrected item-total correlation çıkarımı ve BSEM latent faktör tahmini aynı eksende karşılaştırılmıştır. TOST eşdeğerlik analizi ise DM-Kontrol farkının pratik olarak ihmal edilebilir aralıkta kabul edilip edilemeyeceğini test eder.</p>
      {callout("İstatistik yöntem kutusu: multiverse, TOST ve BSEM", "Multiverse analiz, aynı araştırma sorusunu makul alternatif skor kodlamalarıyla tekrar ederek sonucun analitik kararlara bağımlılığını gösterir. TOST eşdeğerlik testi, anlamlı fark bulunmamasından farklıdır; önceden belirlenen pratik eşdeğerlik bandı içinde kalındığını ayrıca sınar. Bayesian SEM ise klasik CFA'nın katı sıfır kısıtlarını yumuşatan tamamlayıcı latent değişken kontrolüdür.", "warning")}
      {multiverse_figure(multiverse)}
      <p>Tüm stratejilerde DM-Kontrol tahmini negatif yöndedir, ancak güven aralıkları sıfırı kesmektedir. Bu, EMBU-P Reddetme için tutarlı ve güçlü bir grup farkı kanıtı olmadığını gösterir. BSEM latent faktör tahmininin de aynı genel bölgede kalması, sonucun yalnız klasik toplam puan kodlamasına bağlı olmadığını düşündürür.</p>
      {table_html("Reddetme multiverse sonuçları", ["Strateji", "n", "DM-Kontrol", "SE", "p", "Cohen d"], multiverse_rows, numeric_cols={1, 2, 3, 4, 5}, fixed=True, col_widths=[34, 10, 16, 12, 12, 16])}
      {table_html("TOST eşdeğerlik duyarlılığı", ["Strateji", "n DM/K", "g", "90% CI", "p alt", "p üst", "Eşd"], tost_rows, numeric_cols={2, 4, 5}, fixed=True, col_widths=[25, 13, 10, 22, 10, 10, 10])}
      <p>TOST sonuçlarında eşdeğerlik kararı Hayır kalmaktadır; yani grup farkı anlamlı bulunmamakla birlikte, bu farkın önceden tanımlanan pratik eşdeğerlik bandı içinde kaldığı da güçlü biçimde gösterilememiştir. Bu ayrım önemlidir: anlamlı fark yok sonucu, otomatik olarak gruplar eşdeğer sonucuna çevrilmemelidir.</p>
      {table_html("BSEM yakınsama özeti", ["Analiz", "Set", "Durum", "Chain", "Burnin", "Sample", "Seed", "Max Rhat", "Min ESS"], bsem_diag_rows, numeric_cols={3, 4, 5, 6, 7, 8}, fixed=True, col_widths=[16, 14, 14, 8, 8, 8, 12, 10, 10]) if bsem_diag_rows else ""}
      {table_html("BSEM fit ve bilgi ölçütleri", ["Analiz", "Set", "Ölçüt", "Değer"], bsem_fit_rows, numeric_cols={3}, fixed=True, col_widths=[25, 25, 18, 32]) if bsem_fit_rows else ""}
      <p>Yakınsama özeti, BSEM tahminlerinin teknik olarak kullanılabilir olduğunu gösterir: Rhat değerleri 1'e çok yakındır ve etkili örneklem büyüklükleri raporlanabilir düzeydedir. Bununla birlikte posterior predictive p-value değerlerinin sınırda kalması, BSEM'in EMBU-P Reddetme sorununu tamamen çözmediğini gösterir.</p>
    </section>
    """)

    html_parts.append(f"""
    <section id="s9" class="report-section">
      {section_banner(9, "Yorum ve Raporlama Kararı", "Son raporlama dili")}
      <p>Bu psikometrik validasyon, EMBU-P ve EMBU-C formlarının aynı kavramsal alanı eşit güçte taşımadığını göstermektedir. En güçlü ve tutarlı kanıt, çocuk bildirimi üzerinden elde edilen EMBU-C sonuçlarında toplanmaktadır: Reddetme ve Karşılaştırma alt ölçekleri kabul edilebilir iç tutarlılık üretmekte, madde dağılımları anne formuna göre daha kullanılabilir varyans sunmakta, nomolojik ağ bulguları beklenen yönde seyretmekte ve kardeşli tasarım içinde aile içi farklılaşmayı yakalayabilmektedir. Bu nedenle ana analiz metninde EMBU-C, ebeveynlik algısı ve kardeşler arası farklılaşma için birincil psikometrik kaynak olarak konumlandırılmalıdır.</p>
      <div class="cds-pattern-7 cds-pattern-7--compact">
        <div class="cds-pattern-7-tile">{svg_icon("check", "cds-pattern-7-icon-corner")}<div class="cds-pattern-7-term">Birincil kaynak</div><div class="cds-pattern-7-def">EMBU-C, ebeveynlik algısı ve kardeşler arası farklılaşma için daha güçlü psikometrik zemin sağlar.</div></div>
        <div class="cds-pattern-7-tile">{svg_icon("warning", "cds-pattern-7-icon-corner")}<div class="cds-pattern-7-term">Sınırlı kaynak</div><div class="cds-pattern-7-def">EMBU-P Reddetme, düşük alpha/omega ve taban etkisi nedeniyle ana hipotez taşıyıcısı yapılmamalıdır.</div></div>
        <div class="cds-pattern-7-tile">{svg_icon("analytics", "cds-pattern-7-icon-corner")}<div class="cds-pattern-7-term">Grup karşılaştırması</div><div class="cds-pattern-7-def">Anlamlı fark yokluğu eşdeğerlik değildir; TOST kararı bu nedenle ayrı raporlanmalıdır.</div></div>
        <div class="cds-pattern-7-tile">{svg_icon("people", "cds-pattern-7-icon-corner")}<div class="cds-pattern-7-term">Kuramsal katkı</div><div class="cds-pattern-7-def">Kardeşli tasarım, aileyi homojen çevre sayan yorumların yetersiz kalabileceğini gösterir.</div></div>
      </div>
      <p>EMBU-P için daha sınırlı ve seçici bir raporlama dili gereklidir. Özellikle Reddetme alt ölçeği, düşük alpha/omega değerleri, yoğun taban etkisi, CFA/MI kırılganlığı ve multiverse/BSEM duyarlılıklarında zayıf grup farkı sinyali nedeniyle bu örneklemde güçlü bir yapı geçerliği kanıtı üretmemektedir. Bu bulgu anne formu geçersizdir ya da reddetme kavramı yoktur şeklinde yorumlanmamalıdır. Daha doğru ifade, anne öz-bildiriminde reddedici ebeveynlik maddelerinin bu örneklemde düşük varyans ürettiği ve mevcut madde havuzunun Reddetme boyutunu ayırt etmekte sınırlı kaldığıdır.</p>
      <p>Grup karşılaştırmaları açısından sonuçlar iki ayrı ilkeyle raporlanmalıdır. Birincisi, anlamlı fark bulunmaması grupların eşdeğer olduğu anlamına gelmez; TOST sonuçları EMBU-P Reddetme için pratik eşdeğerliği güçlü biçimde göstermemektedir. İkincisi, ölçüm değişmezliği kanıtı olmayan ya da kategori seyrekliği nedeniyle tahmin edilemeyen modellerde grup ortalaması yorumları sınırlı tutulmalıdır.</p>
      {table_html("Kanıt gücü özeti", ["Alan", "Kanıt düzeyi", "Gerekçe"], evidence_rows, fixed=True, col_widths=[27, 18, 55])}
      {table_html("Raporlama ve yöntem uyumu kontrolü", ["Çerçeve", "Durum", "Rapor içi karşılık"], compliance_rows, fixed=True, col_widths=[28, 14, 58])}
      <div class="cds-recommendation-stack">
        <div class="cds-recommendation-group">
          <div class="cds-recommendation-group-label">Raporlama kararı</div>
          <div class="cds-recommendation-card"><strong>EMBU-C ana metinde birincil psikometrik kaynak olarak raporlanmalı.</strong><span>Reddetme ve Karşılaştırma boyutları iç tutarlılık, dağılım ve nomolojik ağ kanıtı bakımından daha tutarlı sonuç verir.</span></div>
          <div class="cds-recommendation-card"><strong>EMBU-P Reddetme metodolojik ekte sınırlılık odaklı sunulmalı.</strong><span>Taban etkisi, düşük güvenilirlik, model kırılganlığı ve multiverse/BSEM sonuçları birlikte gösterilmelidir.</span></div>
          <div class="cds-recommendation-card"><strong>Kardeşli tasarım kuramsal katkı olarak yazılmalı.</strong><span>ICC, LoA ve indeks-kardeş konkordansı yalnız teknik düzeltme değil, parental differential treatment yorumunun ampirik yüzeyidir.</span></div>
        </div>
      </div>
      <p>Metodolojik ekin ana mesajı, anne bildirimi ve çocuk bildirimi arasındaki psikometrik performans farkı olmalıdır. Psikometrik adaptasyon makalesinin pozitif katkısı ise EMBU-C'nin Türkçe örneklemde kardeşli ve dyadic tasarımlarda kullanılabilirliğini göstermesidir. Sonuç cümlesi şu eksende kurulabilir: EMBU-C, bu örneklemde ebeveynlik algısı ve kardeşler arası farklılaşmayı değerlendirmek için daha güçlü ve yorumlanabilir bir araçtır; EMBU-P ise özellikle Reddetme boyutunda temkinli, sınırlılık odaklı ve destekleyici düzeyde raporlanmalıdır.</p>
      <div class="cds-recommendation-card closing-statement"><strong>Sonuç cümlesi</strong><span>Çocuk bildirimi, bu veri setinde ebeveynlik algısı ve kardeşler arası farklılaşma için ana psikometrik kanıtı taşır; anne bildirimi ise özellikle reddedici ebeveynlik maddelerinde düşük varyans ve sınırlı iç tutarlılık nedeniyle destekleyici ve sınırlılık odaklı raporlanmalıdır.</span></div>
    </section>
    """)

    html_parts.extend(["</body>", "</html>"])
    return "\n".join(html_parts)


def build_css() -> str:
    return r"""
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Serif:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
  --cds-white: #ffffff;
  --cds-black: #000000;
  --cds-gray-10: #f4f4f4;
  --cds-gray-20: #e0e0e0;
  --cds-gray-30: #c6c6c6;
  --cds-gray-40: #a8a8a8;
  --cds-gray-50: #8d8d8d;
  --cds-gray-60: #6f6f6f;
  --cds-gray-70: #525252;
  --cds-gray-80: #393939;
  --cds-gray-90: #262626;
  --cds-gray-100: #161616;
  --cds-blue-10: #edf5ff;
  --cds-blue-20: #d0e2ff;
  --cds-blue-30: #a6c8ff;
  --cds-blue-40: #78a9ff;
  --cds-blue-50: #4589ff;
  --cds-blue-60: #0f62fe;
  --cds-blue-70: #0043ce;
  --cds-blue-80: #002d9c;
  --cds-blue-90: #001d6c;
  --cds-blue-100: #001141;
  --cds-teal-10: #d9fbfb;
  --cds-teal-20: #9ef0f0;
  --cds-teal-30: #3ddbd9;
  --cds-teal-40: #08bdba;
  --cds-teal-50: #009d9a;
  --cds-teal-60: #007d79;
  --cds-teal-70: #005d5d;
  --cds-teal-80: #004144;
  --cds-support-error: #da1e28;
  --cds-support-success: #24a148;
  --cds-support-warning: #f1c21b;
  --cds-support-info: #0043ce;
  --cds-support-error-bg: #fff1f1;
  --cds-support-success-bg: #defbe6;
  --cds-support-warning-bg: #fcf4d6;
  --cds-support-info-bg: #edf5ff;
  --cds-background: #ffffff;
  --cds-layer-01: #f4f4f4;
  --cds-layer-02: #ffffff;
  --cds-layer-accent-01: #edf5ff;
  --cds-text-primary: #161616;
  --cds-text-secondary: #525252;
  --cds-text-helper: #6f6f6f;
  --cds-text-on-color: #ffffff;
  --cds-border-subtle-00: #e0e0e0;
  --cds-border-subtle-01: #c6c6c6;
  --cds-border-strong-01: #8d8d8d;
  --cds-border-interactive: #0f62fe;
  --cds-button-primary: #0f62fe;
  --cds-link-primary: #0f62fe;
  --cds-font-sans: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  --cds-font-serif: 'IBM Plex Serif', Georgia, 'Times New Roman', serif;
  --cds-font-mono: 'IBM Plex Mono', 'Courier New', monospace;
  --cds-spacing-01: 0.125rem;
  --cds-spacing-02: 0.25rem;
  --cds-spacing-03: 0.5rem;
  --cds-spacing-04: 0.75rem;
  --cds-spacing-05: 1rem;
  --cds-spacing-06: 1.5rem;
  --cds-spacing-07: 2rem;
  --cds-spacing-08: 2.5rem;
  --cds-spacing-09: 3rem;
  --cds-spacing-10: 4rem;
}

@page {
  size: A4;
  margin: 18mm 16mm 18mm 16mm;
  @top-left {
    content: "Psikometrik Validasyon · Carbon";
    font-family: var(--cds-font-sans);
    font-size: 8pt;
    color: var(--cds-text-secondary);
    padding-top: 8mm;
  }
  @top-right {
    content: "EMBU-P / EMBU-C · Beck · KIA/SRQ";
    font-family: var(--cds-font-sans);
    font-size: 8pt;
    color: var(--cds-text-secondary);
    padding-top: 8mm;
  }
  @bottom-left {
    content: "Kilitli final referans veri";
    font-family: var(--cds-font-sans);
    font-size: 8pt;
    color: var(--cds-text-secondary);
    padding-bottom: 8mm;
  }
  @bottom-right {
    content: "Sayfa " counter(page) " / " counter(pages);
    font-family: var(--cds-font-sans);
    font-size: 8pt;
    color: var(--cds-text-secondary);
    padding-bottom: 8mm;
  }
}

@page cover {
  margin: 0;
  @top-left { content: none; }
  @top-right { content: none; }
  @bottom-left { content: none; }
  @bottom-right { content: none; }
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; -webkit-font-smoothing: antialiased; }
body {
  font-family: var(--cds-font-sans);
  font-size: 10pt;
  line-height: 1.55;
  color: var(--cds-text-primary);
  background: var(--cds-background);
  font-weight: 400;
}
h1, h2, h3, h4 { font-family: var(--cds-font-sans); color: var(--cds-text-primary); break-after: avoid; page-break-after: avoid; }
h1 { font-weight: 300; font-size: 34pt; line-height: 1.1; }
h2 { font-weight: 400; font-size: 20pt; line-height: 1.2; margin-bottom: var(--cds-spacing-05); }
h3 { font-weight: 400; font-size: 12pt; line-height: 1.25; margin-bottom: var(--cds-spacing-03); }
p { margin-bottom: var(--cds-spacing-05); text-align: justify; hyphens: auto; orphans: 4; widows: 4; }
strong { font-weight: 600; color: var(--cds-text-primary); }

.cover-page {
  width: 210mm;
  height: 297mm;
  color: var(--cds-white);
  position: relative;
  overflow: hidden;
  page: cover;
  page-break-after: always;
  display: grid;
  grid-template-columns: 120mm 70mm;
  grid-template-rows: 58mm auto 1fr auto;
  padding: 20mm;
  background: linear-gradient(135deg, var(--cds-blue-90) 0%, var(--cds-teal-80) 55%, var(--cds-teal-70) 100%);
}
.cover-page::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 80mm;
  height: 4mm;
  background: var(--cds-blue-50);
}
.cover-pictogram {
  position: absolute;
  right: -30mm;
  bottom: -30mm;
  width: 160mm;
  height: 160mm;
  opacity: 0.06;
  color: var(--cds-blue-30);
  z-index: 1;
}
.cover-pictogram-badge {
  grid-column: 2;
  grid-row: 1;
  justify-self: end;
  align-self: start;
  width: 48mm;
  height: 48mm;
  color: var(--cds-blue-30);
  opacity: 0.92;
  z-index: 3;
}
.cover-header { grid-column: 1; grid-row: 1; z-index: 3; padding-top: var(--cds-spacing-03); }
.cover-eyebrow {
  font-family: var(--cds-font-mono);
  font-size: 9pt;
  font-weight: 600;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--cds-blue-30);
  margin-bottom: var(--cds-spacing-04);
}
.cover-issue-chip {
  display: inline-flex;
  padding: var(--cds-spacing-02) var(--cds-spacing-04);
  background: var(--cds-blue-80);
  border: 1px solid var(--cds-blue-40);
  color: var(--cds-white);
  font-size: 8pt;
  font-family: var(--cds-font-mono);
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.cover-title-block { grid-column: 1 / -1; grid-row: 2; z-index: 3; padding-top: var(--cds-spacing-07); padding-bottom: var(--cds-spacing-05); max-width: 170mm; }
.cover-title { color: var(--cds-white); font-weight: 300; max-width: 170mm; }
.cover-subtitle {
  font-size: 12pt;
  font-weight: 400;
  line-height: 1.4;
  color: var(--cds-blue-20);
  max-width: 150mm;
  font-family: var(--cds-font-serif);
  font-style: italic;
}
.cover-meta-grid {
  grid-column: 1 / -1;
  grid-row: 3;
  align-self: end;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--cds-spacing-05);
  z-index: 3;
  margin-bottom: var(--cds-spacing-07);
}
.cover-meta-item { border-left: 2px solid var(--cds-blue-50); padding-left: var(--cds-spacing-04); }
.cover-meta-label {
  font-size: 7.5pt;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--cds-blue-30);
  margin-bottom: var(--cds-spacing-02);
}
.cover-meta-value { font-size: 10pt; font-weight: 400; color: var(--cds-white); line-height: 1.3; }
.cover-footer {
  grid-column: 1 / -1;
  grid-row: 4;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding-top: var(--cds-spacing-05);
  border-top: 1px solid var(--cds-blue-40);
  z-index: 3;
}
.cover-classification { font-size: 8pt; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; color: var(--cds-blue-30); }
.cover-date { font-size: 9pt; color: var(--cds-blue-20); font-family: var(--cds-font-mono); font-variant-numeric: tabular-nums; }

.toc-page { page-break-after: always; }
.toc-list { list-style: none; margin-left: 0; margin-top: var(--cds-spacing-05); }
.toc-list li { display: flex; align-items: baseline; padding: var(--cds-spacing-04) 0; border-bottom: 1px solid var(--cds-border-subtle-00); font-size: 10pt; }
.toc-number { font-family: var(--cds-font-mono); font-size: 9pt; color: var(--cds-blue-60); font-weight: 500; min-width: 32pt; flex-shrink: 0; }
.toc-list a { flex-grow: 1; color: var(--cds-text-primary); text-decoration: none; display: flex; align-items: baseline; }
.toc-list a::after { content: target-counter(attr(href), page); font-family: var(--cds-font-mono); font-size: 9pt; color: var(--cds-text-secondary); margin-left: auto; padding-left: var(--cds-spacing-03); }

.report-section { break-before: page; }
.section-number {
  font-family: var(--cds-font-mono);
  font-size: 9pt;
  color: var(--cds-blue-60);
  font-weight: 500;
  letter-spacing: 0.08em;
  margin-bottom: var(--cds-spacing-02);
  display: block;
  break-after: avoid !important;
  page-break-after: avoid !important;
  break-inside: avoid;
}
.section-number + h2 { margin-top: 0; break-before: avoid !important; page-break-before: avoid !important; }
.section-header-group { break-inside: avoid; page-break-inside: avoid; margin-top: var(--cds-spacing-08); margin-bottom: var(--cds-spacing-05); }
.section-header-group h2 { margin-top: var(--cds-spacing-02); margin-bottom: 0; }
.cds-section-banner {
  background: var(--cds-layer-accent-01);
  color: var(--cds-text-primary);
  padding: var(--cds-spacing-06) var(--cds-spacing-07);
  margin: var(--cds-spacing-08) 0 var(--cds-spacing-06) 0;
  position: relative;
  border-left: 4px solid var(--cds-border-interactive);
  break-inside: avoid;
  page-break-inside: avoid;
  break-after: avoid;
  page-break-after: avoid;
}
.cds-banner-icon { width: 24px; height: 24px; color: var(--cds-blue-60); float: right; margin-left: var(--cds-spacing-04); }
.cds-section-banner-eyebrow { font-size: 8pt; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: var(--cds-text-secondary); margin-bottom: var(--cds-spacing-02); }
.cds-section-banner-title { font-size: 20pt; font-weight: 300; line-height: 1.2; color: var(--cds-text-primary); margin: 0; }
.executive-summary { background: var(--cds-blue-10); padding: var(--cds-spacing-06); margin-bottom: var(--cds-spacing-06); border-left: 4px solid var(--cds-blue-60); break-inside: avoid; page-break-inside: avoid; }

.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--cds-spacing-03); margin: var(--cds-spacing-06) 0; }
.stat-tile {
  background: var(--cds-layer-01);
  padding: var(--cds-spacing-05);
  border-top: 2px solid var(--cds-blue-60);
  display: flex;
  flex-direction: column;
  min-height: 38mm;
  break-inside: avoid;
  page-break-inside: avoid;
}
.stat-tile-header { display: flex; align-items: flex-start; justify-content: space-between; gap: var(--cds-spacing-03); margin-bottom: var(--cds-spacing-03); }
.stat-tile-icon { width: 28px; height: 28px; color: var(--cds-blue-60); flex-shrink: 0; }
.stat-value { font-size: 22pt; font-weight: 300; line-height: 1.1; color: var(--cds-blue-70); font-family: var(--cds-font-sans); margin-bottom: var(--cds-spacing-02); }
.stat-label { font-size: 8pt; font-weight: 600; letter-spacing: 0.04em; color: var(--cds-text-secondary); text-transform: uppercase; line-height: 1.3; margin-bottom: var(--cds-spacing-02); }
.stat-context { font-size: 7.5pt; color: var(--cds-text-helper); line-height: 1.3; margin-top: auto; }

.cds-callout { display: flex; gap: var(--cds-spacing-04); padding: var(--cds-spacing-05); margin: var(--cds-spacing-05) 0; border-left: 3px solid; break-inside: avoid; page-break-inside: avoid; }
.cds-callout-info { background: var(--cds-support-info-bg); border-left-color: var(--cds-support-info); }
.cds-callout-warning { background: var(--cds-support-warning-bg); border-left-color: var(--cds-support-warning); }
.cds-callout-critical { background: var(--cds-support-error-bg); border-left-color: var(--cds-support-error); }
.cds-callout-icon { width: 20px; height: 20px; flex-shrink: 0; margin-top: 4px; }
.cds-callout-info .cds-callout-icon { color: var(--cds-support-info); }
.cds-callout-warning .cds-callout-icon { color: #8e6a00; }
.cds-callout-critical .cds-callout-icon { color: var(--cds-support-error); }
.cds-callout-body { flex-grow: 1; font-size: 9.5pt; line-height: 1.5; }
.cds-callout-title { font-weight: 600; margin-bottom: var(--cds-spacing-02); font-size: 10pt; }
.cds-callout-body p { margin: 0; text-align: left; }

.cds-table-wrapper { margin: var(--cds-spacing-06) 0; break-inside: avoid; page-break-inside: avoid; }
.page-break-before { break-before: page; page-break-before: always; }
.cds-table-caption { font-size: 9pt; font-weight: 600; color: var(--cds-blue-70); margin-bottom: var(--cds-spacing-03); break-after: avoid; }
.cds-table { width: 100%; border-collapse: collapse; font-size: 8.2pt; line-height: 1.35; margin-bottom: var(--cds-spacing-05); }
[data-layout="cds-table--fixed"] { table-layout: fixed; }
.cds-table th { background: var(--cds-gray-90); color: var(--cds-white); font-weight: 600; text-align: left; padding: var(--cds-spacing-03); border-bottom: 1px solid var(--cds-border-strong-01); overflow-wrap: break-word; hyphens: auto; }
.cds-table td { padding: var(--cds-spacing-03); border-bottom: 1px solid var(--cds-border-subtle-00); vertical-align: top; overflow-wrap: break-word; hyphens: auto; }
.cds-table tbody tr:nth-child(even) { background: var(--cds-layer-01); }
.cds-table .cds-numeric { font-family: var(--cds-font-mono); font-variant-numeric: tabular-nums; text-align: right; }
[data-layout="cds-table--fixed"] .cds-numeric { white-space: normal; }
.cds-delta-cell { position: relative; }
.cds-delta-cell span:first-child { position: relative; z-index: 2; }
.delta-bar { display: block; height: 4px; background: var(--cds-blue-30); margin-top: var(--cds-spacing-02); }

.cds-figure { margin: var(--cds-spacing-06) 0; break-inside: avoid; page-break-inside: avoid; border: 1px solid var(--cds-border-subtle-00); background: var(--cds-layer-02); }
.cds-figure figcaption { font-size: 10pt; font-weight: 600; color: var(--cds-text-primary); background: var(--cds-layer-01); padding: var(--cds-spacing-04) var(--cds-spacing-05); border-bottom: 1px solid var(--cds-border-subtle-00); }
.figure-body { padding: var(--cds-spacing-05); }
.figure-note { font-size: 8.5pt; line-height: 1.45; color: var(--cds-text-secondary); padding: 0 var(--cds-spacing-05) var(--cds-spacing-05); text-align: left; }
.two-col-figure { display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--cds-spacing-05); }
.three-col-figure { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--cds-spacing-05); }
.mini-panel { background: var(--cds-layer-01); padding: var(--cds-spacing-04); }
.wide-panel { max-width: 100%; }
.panel-kicker { font-size: 8pt; font-weight: 600; color: var(--cds-text-secondary); margin: var(--cds-spacing-03) 0 var(--cds-spacing-02); text-transform: uppercase; letter-spacing: 0.04em; }
.bar-row, .rho-row, .ci-row { display: grid; grid-template-columns: minmax(32mm, 1fr) 1.7fr 12mm; gap: var(--cds-spacing-03); align-items: center; margin-bottom: var(--cds-spacing-03); break-inside: avoid; }
.bar-label, .rho-label, .ci-label { font-size: 8pt; color: var(--cds-text-secondary); line-height: 1.25; }
.bar-track, .rho-track, .ci-track { height: 8px; background: var(--cds-gray-20); position: relative; }
.bar-fill { display: block; height: 8px; }
.bar-fill-blue { background: var(--cds-blue-60); }
.bar-fill-teal { background: var(--cds-teal-60); }
.bar-fill-orange { background: var(--cds-support-warning); }
.bar-value, .rho-value, .ci-value { font-family: var(--cds-font-mono); font-size: 8pt; text-align: right; color: var(--cds-text-primary); }
.floor-panel { display: grid; gap: var(--cds-spacing-05); }
.floor-strip-row { display: grid; grid-template-columns: 18mm 1fr; gap: var(--cds-spacing-04); align-items: end; }
.floor-strip-label { font-family: var(--cds-font-mono); font-size: 8pt; color: var(--cds-text-secondary); }
.floor-strip { height: 44px; display: grid; grid-template-columns: repeat(29, 1fr); gap: 2px; align-items: end; border-bottom: 1px solid var(--cds-border-subtle-01); }
.floor-cell { display: block; min-height: 8px; background: var(--cds-blue-60); }
.floor-sicaklik { background: var(--cds-teal-60); }
.floor-asiri { background: var(--cds-support-warning); }
.floor-reddetme { background: var(--cds-support-error); }
.floor-kars { background: var(--cds-blue-60); }
.rho-panel, .ci-panel { display: grid; gap: var(--cds-spacing-01); }
.rho-track, .ci-track { height: 10px; }
.rho-zero { position: absolute; left: 50%; top: -4px; width: 1px; height: 18px; background: var(--cds-gray-60); }
.rho-dot, .ci-dot { position: absolute; top: 50%; width: 8px; height: 8px; margin-left: -4px; margin-top: -4px; border-radius: 50%; border: 1px solid var(--cds-white); }
.rho-blue, .ci-dot { background: var(--cds-blue-60); }
.rho-teal { background: var(--cds-teal-60); }
.rho-orange { background: var(--cds-support-warning); }
.rho-nonsig { background: var(--cds-layer-02); border: 1px solid var(--cds-gray-60); }
.ci-bar { position: absolute; top: 4px; height: 2px; background: var(--cds-blue-60); }

.cds-pattern-7 { display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--cds-spacing-04); margin: var(--cds-spacing-06) 0; }
.cds-pattern-7-tile { position: relative; background: var(--cds-layer-01); border-left: 3px solid var(--cds-blue-60); padding: var(--cds-spacing-05); min-height: 32mm; break-inside: avoid; page-break-inside: avoid; }
.cds-pattern-7-icon-corner { width: 22px; height: 22px; color: var(--cds-blue-60); float: right; margin-left: var(--cds-spacing-03); }
.cds-pattern-7-term { font-weight: 600; margin-bottom: var(--cds-spacing-03); color: var(--cds-text-primary); }
.cds-pattern-7-def { font-size: 9pt; color: var(--cds-text-secondary); line-height: 1.45; }
.cds-recommendation-stack { display: grid; gap: var(--cds-spacing-05); margin: var(--cds-spacing-06) 0; }
.cds-recommendation-group { border-left: 4px solid var(--cds-blue-60); background: var(--cds-layer-01); padding: var(--cds-spacing-05); }
.cds-recommendation-group-label { font-family: var(--cds-font-mono); font-size: 8pt; letter-spacing: 0.08em; text-transform: uppercase; color: var(--cds-blue-70); margin-bottom: var(--cds-spacing-04); }
.cds-recommendation-card { background: var(--cds-layer-02); border: 1px solid var(--cds-border-subtle-00); padding: var(--cds-spacing-04); margin-bottom: var(--cds-spacing-03); break-inside: avoid; }
.cds-recommendation-card strong { display: block; margin-bottom: var(--cds-spacing-02); }
.cds-recommendation-card span { color: var(--cds-text-secondary); font-size: 9pt; }

section > .section-header-group { break-after: avoid; page-break-after: avoid; }
.section-header-group + *, h3 + *, .cds-section-banner + * { break-before: avoid; page-break-before: avoid; }
.cds-table thead { display: table-header-group; }
.cds-table tbody tr { break-inside: avoid; page-break-inside: avoid; }
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html_path = OUT_DIR / "psikometrik-validasyon-butunlesik-rapor-carbon.html"
    html_path.write_text(build_report(), encoding="utf-8")
    print(html_path)


if __name__ == "__main__":
    main()
