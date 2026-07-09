#!/usr/bin/env python3
"""Audit CSR causal-language discipline and exploratory-label integrity.

The script is text-only: it reads the CSR markdown, does not inspect row-level
data, and emits only CSR line excerpts plus classification metadata.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
SECTION_NUMBER_RE = re.compile(r"^(\d+(?:\.\d+)*)\b")

EXPLORATORY_LABEL_RE = re.compile(
    r"(?i)(\[ *(?:KEŞİFSEL|KESIFSEL).*?(?:İKİNCİL|IKINCIL)?.*?\]|"
    r"(?:keşifsel|kesifsel|post[- ]hoc|hipotez[- ]üretici|"
    r"doğrulayıcı +değil|dogrulayici +degil|external validation|"
    r"dış[- ]validasyon|dis[- ]validasyon))"
)

H1_H4_RE = re.compile(r"\bH[1-4]\b")
HYPOTHESIS_RE = re.compile(r"\bH[1-5]\b")

CAUSAL_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "direct_causal_verb",
        re.compile(
            r"(?i)(neden +ol|yol +aç|sebep +ol|sonucunda|dolayısıyla|"
            r"art[ıi]r(?:makta|maktadır|ır|an|dı|dığı|dığını)|"
            r"azalt(?:makta|maktadır|ır|an|tı|tığı|tığını)|"
            r"düşür|düsür|yükselt|yukselt|tetikle|"
            r"(?<!sabit )(?<!rastgele )\betkiler\b|"
            r"etkile(?:mekte|mektedir|miştir|miş|mis|yen|yi|yip|diği|digi|diğini|digini)|"
            r"etki(?:si|nin|yi)? +(?:üzerinde|uzerinde|iletil|aktar|yoluyla))"
        ),
    ),
    (
        "mechanism_transfer_language",
        re.compile(
            r"(?i)(mekanizma|arac[ıi]|dolaylı +etki|risk +aktar[ıi]m|"
            r"transmisyon|zincir|taşın|tasin|iletilmemektedir|iletilmektedir)"
        ),
    ),
    (
        "proof_or_confirmation_language",
        re.compile(
            r"(?i)(kanıtla|kanitla|ispat|ampirik +olarak +doğrula|"
            r"ampirik +olarak +dogrula|kısmi +doğrulan|kismi +dogrulan|"
            r"doğrulamaktadır|dogrulamaktadir|doğrular|dogrular|ortaya +koy)"
        ),
    ),
    (
        "clinical_action_language",
        re.compile(
            r"(?i)(zorunludur|hedeflemelidir|gerektiği +çıkarımı|"
            r"gerektigi +cikarimi|sağlayabilir|saglayabilir|net +fayda)"
        ),
    ),
]

EXPLICIT_CAVEAT_RE = re.compile(
    r"(?i)(kesitsel|korelasyonel|gözlemsel|gozlemsel|nedensel +(?:yön|yon)|"
    r"nedensel[^.]{0,80}(?:değil|degil|kurmaz|çıkarım|cikarim|yapılmam|yapilmam)|"
    r"nedensel +okunmaz|hipotez[- ]üretici|hipotez[- ]uretici|"
    r"keşifsel|kesifsel|doğrulayıcı +değil|dogrulayici +degil|"
    r"dış[- ]validasyon|dis[- ]validasyon|external validation|replikasyon|"
    r"temkin|not +treatment +effect|causal +validation +değildir|"
    r"causal +validation +degildir)"
)

SOFT_ASSOCIATION_RE = re.compile(
    r"(?i)(ilişki|iliski|ilişkili|iliskili|örüntü|oruntu|sinyal|"
    r"işaret|isaret|düşündür|dusundur|olabilir|yordan|bağımlı|bagimli)"
)

STATISTICAL_TERMINOLOGY_RE = re.compile(
    r"(?i)(sabit +etkiler|rastgele +(?:kesişim|kesisim|etkiler)|"
    r"etki +büyüklüğü|etki +buyuklugu|standardize +etki|"
    r"a-yolu|b-yolu|a × b|a x b|yapısal +yol|yapisal +yol|"
    r"dolaylı +\(?(?:indirect)?\)? *etki|indirect +effect|"
    r"moderate +aracılık +indeksi|aracılık +modeli|aracılık +analizi|"
    r"nedensel +graf|causal +dag|dag|kanıt +zinciri|kanit +zinciri|"
    r"çözümleme|cozumleme|modeli +kurul|tahmin +edil)"
)

DISCURSIVE_INTERPRETATION_RE = re.compile(
    r"(?i)(sonuç:|sonuc:|klinik +anlam|yorum\.|bu +(?:desen|örüntü|oruntu|bulgu|sonuç|sonuc)|"
    r"yani:|göstermektedir|gostermektedir|göstermiştir|gostermistir|"
    r"işaret +etmektedir|isaret +etmektedir|düşündürmektedir|dusundurmektedir|"
    r"sergilemektedir|mevcuttur|öneri|oner[iı]|çıkarılmaktadır|cikarilmaktadir|"
    r"hedeflemelidir|zorunludur|sağlayabilir|saglayabilir)"
)

UNSAFE_CAUSAL_CLAIM_RE = re.compile(
    r"(?i)(etkilemekte|etkilemektedir|art[ıi]rmakta|art[ıi]rmaktadır|"
    r"azaltmakta|azaltmaktadır|tetikle|risk +aktar[ıi]m|transmisyon|"
    r"evrensel +bir +mekanizma|psikolojik +mekanizma|mekanizma +olarak|"
    r"doğrulan|dogrulan|kanıtla|kanitla|"
    r"sağlayabilir|saglayabilir|hedeflemelidir|zorunludur|net +fayda)"
)

HTML_COMMENT_START_RE = re.compile(r"<!--")
HTML_COMMENT_END_RE = re.compile(r"-->")


@dataclass
class CsrLine:
    line_no: int
    text: str
    section: str
    heading: str
    parent_exploratory_label: bool
    line_exploratory_label: bool


def normalize_excerpt(text: str, limit: int = 520) -> str:
    collapsed = re.sub(r"\s+", " ", text).strip()
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[: limit - 1].rstrip() + "…"


def section_prefixes(section: str) -> list[str]:
    parts = section.split(".") if section else []
    return [".".join(parts[:idx]) for idx in range(len(parts), 0, -1)]


def major_section(section: str) -> str:
    return section.split(".", 1)[0] if section else ""


def iter_visible_lines(csr_path: Path) -> list[CsrLine]:
    lines: list[CsrLine] = []
    current_section = ""
    current_heading = ""
    exploratory_section_labels: dict[str, bool] = {}
    in_comment = False

    for line_no, raw_line in enumerate(csr_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.rstrip("\n")
        if in_comment:
            if HTML_COMMENT_END_RE.search(line):
                in_comment = False
            continue
        if HTML_COMMENT_START_RE.search(line):
            if not HTML_COMMENT_END_RE.search(line):
                in_comment = True
            continue

        heading_match = HEADING_RE.match(line.strip())
        if heading_match:
            heading_text = heading_match.group(2).strip()
            section_match = SECTION_NUMBER_RE.match(heading_text)
            if section_match:
                current_section = section_match.group(1)
            current_heading = heading_text
            if current_section:
                exploratory_section_labels[current_section] = bool(EXPLORATORY_LABEL_RE.search(heading_text))

        parent_label = any(
            exploratory_section_labels.get(prefix, False) for prefix in section_prefixes(current_section)
        )
        line_label = bool(EXPLORATORY_LABEL_RE.search(line))
        lines.append(
            CsrLine(
                line_no=line_no,
                text=line,
                section=current_section,
                heading=current_heading,
                parent_exploratory_label=parent_label,
                line_exploratory_label=line_label,
            )
        )
    return lines


def classify_scope(line: CsrLine) -> str:
    section = line.section
    major = major_section(section)
    text = line.text

    if major in {"12", "15", "16"}:
        return "exploratory_secondary_section"
    if section.startswith("20.4"):
        return "exploratory_secondary_publication_plan"
    if section.startswith(("17.7", "17.8", "17.9", "19.3")):
        return "exploratory_or_application_discussion"
    if section.startswith(("11.1", "11.2", "11.3", "11.4")):
        return "confirmatory_h1_h4_results"
    if section.startswith(("17.2", "17.3", "17.4", "17.5")):
        return "confirmatory_h1_h4_discussion"
    if major == "19" and H1_H4_RE.search(text):
        return "confirmatory_h1_h4_conclusion"
    if major == "20" and H1_H4_RE.search(text):
        return "confirmatory_h1_h4_publication_plan"
    if section.startswith(("11.5", "17.6")) or re.search(r"\bH5\b", text):
        return "primary_h5"
    if major in {"13", "14"}:
        return "robustness_or_bayesian_support"
    if major in {"4", "5", "6", "7", "8", "9", "10", "11"}:
        return "methods_or_results"
    if major in {"17", "18", "19", "20"}:
        return "discussion_limitations_or_conclusion"
    return "front_matter_or_background"


def detect_causal_patterns(text: str) -> list[str]:
    hits = [name for name, pattern in CAUSAL_PATTERNS if pattern.search(text)]
    if hits and re.search(r"(?i)etki +büyüklüğü|etki +buyuklugu", text):
        non_effect_hits = [name for name in hits if name != "direct_causal_verb"]
        if non_effect_hits:
            return non_effect_hits
        return []
    return hits


def adjudicate_causal(line: CsrLine, scope: str, pattern_names: list[str]) -> tuple[str, str]:
    has_caveat = bool(EXPLICIT_CAVEAT_RE.search(line.text))
    has_soft_association = bool(SOFT_ASSOCIATION_RE.search(line.text))
    is_heading = bool(HEADING_RE.match(line.text.strip()))
    is_artifact_reference = line.text.lstrip().startswith("![")
    is_model_terminology = bool(STATISTICAL_TERMINOLOGY_RE.search(line.text))
    is_discursive = bool(DISCURSIVE_INTERPRETATION_RE.search(line.text))
    is_unsafe_claim = bool(UNSAFE_CAUSAL_CLAIM_RE.search(line.text))
    text_lower = line.text.casefold()

    if not pattern_names:
        return "not_flagged", "Causal/proof/action pattern not detected."
    if is_artifact_reference:
        return "ok_artifact_reference", "Figür/artefakt referansı; bulgu yorumu olarak okunmuyor."
    if is_heading and scope not in {
        "confirmatory_h1_h4_discussion",
        "confirmatory_h1_h4_conclusion",
        "confirmatory_h1_h4_publication_plan",
    }:
        return "ok_section_heading", "Bölüm başlığı veya yöntem etiketi; iddia cümlesi değil."
    if line.text.lstrip().startswith("> **Yöntem kutusu"):
        return "ok_method_definition", "Yöntem tanımı; bulgu yorumu olarak okunmuyor."
    if "denetimi zorunludur" in text_lower:
        return "ok_model_terminology", "Yöntem/diagnostik zorunluluğu; klinik aksiyon iddiası değil."
    if is_model_terminology and not is_discursive:
        return "ok_model_terminology", "İstatistiksel model terimi; nedensel sonuç iddiası değil."
    if has_caveat and "clinical_action_language" not in pattern_names:
        return "ok_caveated", "Aynı satırda kesitsel/korelasyonel veya keşifsel sınırlama var."
    if scope.startswith("exploratory") and not has_caveat and is_unsafe_claim:
        return "revise", "Keşifsel/ikincil bağlamda nedensel, mekanizma veya aksiyon dili yerel caveat olmadan kullanılmış."
    if scope.startswith("exploratory") and line.parent_exploratory_label:
        return "review", "Keşifsel etiket kapsamı var; yine de güçlü model/mekanizma dili yerel cümlede kontrol edilmeli."
    if scope.startswith("confirmatory_h1_h4") and is_unsafe_claim:
        return "revise", "H1-H4 doğrulayıcı olsa da tasarım kesitsel; nedensel/mekanizma dili ilişki veya yol katsayısı diline çekilmeli."
    if scope.startswith("confirmatory_h1_h4") and "mechanism_transfer_language" in pattern_names:
        return "review", "H1-H4 bağlamında mekanizma/zincir dili var; istatistiksel yol diliyle sınırlı kaldığı doğrulanmalı."
    if scope.startswith("confirmatory_h1_h4") and "proof_or_confirmation_language" in pattern_names:
        return "review", "Doğrulama/kanıt dili sonuç kesinliğini büyütebilir; 'destekledi/uyumlu' daha güvenli olabilir."
    if "clinical_action_language" in pattern_names and "external validation" not in text_lower and "dış" not in text_lower:
        return "review", "Klinik aksiyon dili dış-validasyon caveat'i olmadan güçlü olabilir."
    if has_soft_association:
        return "ok_associational", "Satır ilişki/sinyal/örüntü diliyle sınırlı."
    return "review", "Bağlam okuması gerektiren güçlü yorum dili."


def scan_causal_language(lines: list[CsrLine]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line in lines:
        text = line.text.strip()
        if not text:
            continue
        pattern_names = detect_causal_patterns(text)
        if not pattern_names:
            continue
        scope = classify_scope(line)
        status, rationale = adjudicate_causal(line, scope, pattern_names)
        rows.append(
            {
                "line_no": line.line_no,
                "section": line.section,
                "heading": line.heading,
                "scope": scope,
                "patterns": ";".join(pattern_names),
                "has_explicit_caveat": bool(EXPLICIT_CAVEAT_RE.search(text)),
                "has_soft_association_language": bool(SOFT_ASSOCIATION_RE.search(text)),
                "parent_exploratory_label": line.parent_exploratory_label,
                "line_exploratory_label": line.line_exploratory_label,
                "adjudication": status,
                "rationale": rationale,
                "excerpt": normalize_excerpt(text),
            }
        )
    return rows


def label_status(line: CsrLine, scope: str) -> tuple[str, str]:
    text = line.text.strip()
    is_heading = bool(HEADING_RE.match(text))
    h1_h4 = bool(H1_H4_RE.search(text))
    has_label = line.line_exploratory_label
    covered_by_parent = line.parent_exploratory_label

    if h1_h4 and scope.startswith("confirmatory_h1_h4") and has_label:
        return "error_confirmatory_mislabeled", "H1-H4 doğrulayıcı iddia keşifsel etiket taşımamalı."
    if h1_h4 and scope.startswith("confirmatory_h1_h4"):
        return "ok_confirmatory_unlabeled", "H1-H4 doğrulayıcı iddia keşifsel etiketlenmemiş."
    if scope == "primary_h5" and has_label:
        return "ok_primary_h5_tempered", "Kullanıcı gate'i H1-H4 için; H5 satırı temkin/keşifsel yorumla sınırlanmış."
    if scope == "exploratory_secondary_section" and (has_label or covered_by_parent):
        return "ok_exploratory_labeled", "Keşifsel/ikincil bölüm başlığı veya satırı etiket kapsamı sağlıyor."
    if scope == "exploratory_secondary_section":
        return "error_missing_exploratory_label", "Keşifsel/ikincil bölümde etiket kapsamı yok."
    if scope == "exploratory_or_application_discussion" and has_label:
        return "ok_local_exploratory_label", "Tartışma/uygulama satırı yerel keşifsel etiket taşıyor."
    if scope == "exploratory_or_application_discussion" and is_heading:
        return "review_heading_label", "Keşifsel bulgu tartışma başlığı; yerel etiket veya kesit referansı gerekebilir."
    if scope == "exploratory_or_application_discussion" and detect_causal_patterns(text):
        return "review_local_label_or_caveat", "Keşifsel/uygulama tartışmasında güçlü dil var; yerel etiket/caveat kontrol edilmeli."
    if has_label:
        return "ok_label_elsewhere", "Keşifsel/ikincil etiket doğrulayıcı H1-H4 kapsamı dışında."
    return "not_label_relevant", "Etiket disiplini açısından hedef satır değil."


def scan_label_integrity(lines: list[CsrLine]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line in lines:
        text = line.text.strip()
        if not text:
            continue
        scope = classify_scope(line)
        interesting = (
            line.line_exploratory_label
            or line.parent_exploratory_label
            or HYPOTHESIS_RE.search(text)
            or scope.startswith("exploratory")
            or scope.startswith("confirmatory_h1_h4")
        )
        if not interesting:
            continue
        status, rationale = label_status(line, scope)
        rows.append(
            {
                "line_no": line.line_no,
                "section": line.section,
                "heading": line.heading,
                "scope": scope,
                "mentions_h1_h4": bool(H1_H4_RE.search(text)),
                "mentions_any_hypothesis": bool(HYPOTHESIS_RE.search(text)),
                "line_exploratory_label": line.line_exploratory_label,
                "parent_exploratory_label": line.parent_exploratory_label,
                "label_status": status,
                "rationale": rationale,
                "excerpt": normalize_excerpt(text),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> list[str]:
    if not rows:
        return ["_Yok._"]
    out = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|")
            cells.append(value)
        out.append("| " + " | ".join(cells) + " |")
    return out


def write_report(
    path: Path,
    csr_path: Path,
    causal_rows: list[dict[str, object]],
    label_rows: list[dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    causal_counts = Counter(str(row["adjudication"]) for row in causal_rows)
    label_counts = Counter(str(row["label_status"]) for row in label_rows)
    causal_revise = [row for row in causal_rows if row["adjudication"] == "revise"]
    causal_review = [row for row in causal_rows if row["adjudication"] == "review"]
    label_review = [
        row
        for row in label_rows
        if str(row["label_status"]).startswith(("error", "review"))
    ]

    lines = [
        "# CSR Denetim 3: Nedensel Dil + Keşifsel Etiket Bütünlüğü",
        "",
        f"- Kaynak CSR: `{csr_path.as_posix()}`",
        "- Kapsam: yalnız CSR markdown metni; ham veri, row-level kayıt ve PII okunmadı.",
        "- Tarama 1: nedensel/mekanizma/kanıt/klinik-aksiyon dili.",
        "- Tarama 2: `[KEŞİFSEL · İKİNCİL]` kapsamı ve H1-H4 doğrulayıcı etiket bütünlüğü.",
        "",
        "## Özet",
        "",
        f"- Nedensel dil adayı: {len(causal_rows)} satır.",
        f"- Revize edilmesi gereken nedensel dil: {causal_counts.get('revise', 0)} satır.",
        f"- Bağlam incelemesi gereken nedensel dil: {causal_counts.get('review', 0)} satır.",
        f"- Etiket taraması kapsamındaki satır: {len(label_rows)}.",
        f"- Etiket hatası: {sum(count for key, count in label_counts.items() if key.startswith('error'))}.",
        f"- Etiket review: {sum(count for key, count in label_counts.items() if key.startswith('review'))}.",
        "",
        "## Nedensel Dil Adjudikasyonu: Revize Edilecek Satırlar",
        "",
        *markdown_table(
            causal_revise,
            ["line_no", "section", "scope", "adjudication", "patterns", "rationale", "excerpt"],
        ),
        "",
        "## Nedensel Dil Adjudikasyonu: Bağlam Review Satırları",
        "",
        *markdown_table(
            causal_review,
            ["line_no", "section", "scope", "adjudication", "patterns", "rationale", "excerpt"],
        ),
        "",
        "## Etiket Bütünlüğü Adjudikasyonu",
        "",
        *markdown_table(
            label_review,
            ["line_no", "section", "scope", "label_status", "rationale", "excerpt"],
        ),
        "",
        "## Sayaçlar",
        "",
        "### Nedensel Dil",
        "",
        *markdown_table(
            [{"status": key, "n": value} for key, value in sorted(causal_counts.items())],
            ["status", "n"],
        ),
        "",
        "### Etiket",
        "",
        *markdown_table(
            [{"status": key, "n": value} for key, value in sorted(label_counts.items())],
            ["status", "n"],
        ),
        "",
        "## Yorumlama Notu",
        "",
        "- `revise`: CSR metninde yerel ifade düzeltmesi önerilir.",
        "- `review`: satır bağlamı kabul edilebilir olabilir; yine de editör/adjudicator kontrolü gerekir.",
        "- `ok_caveated` / `ok_exploratory_labeled`: otomatik tarama isabeti var, fakat bağlam disiplini yeterli göründü.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csr", default="docs/CLINICAL-STUDY-REPORT-FINAL.md")
    parser.add_argument("--out-causal", default="outputs/tables/csr_causal_language_scan.csv")
    parser.add_argument("--out-labels", default="outputs/tables/csr_exploratory_label_scan.csv")
    parser.add_argument("--out-report", default="outputs/reports/csr_causal_label_audit.md")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    root = Path.cwd()
    csr_path = root / args.csr
    lines = iter_visible_lines(csr_path)
    causal_rows = scan_causal_language(lines)
    label_rows = scan_label_integrity(lines)

    write_csv(
        root / args.out_causal,
        causal_rows,
        [
            "line_no",
            "section",
            "heading",
            "scope",
            "patterns",
            "has_explicit_caveat",
            "has_soft_association_language",
            "parent_exploratory_label",
            "line_exploratory_label",
            "adjudication",
            "rationale",
            "excerpt",
        ],
    )
    write_csv(
        root / args.out_labels,
        label_rows,
        [
            "line_no",
            "section",
            "heading",
            "scope",
            "mentions_h1_h4",
            "mentions_any_hypothesis",
            "line_exploratory_label",
            "parent_exploratory_label",
            "label_status",
            "rationale",
            "excerpt",
        ],
    )
    write_report(root / args.out_report, Path(args.csr), causal_rows, label_rows)

    causal_counts = Counter(str(row["adjudication"]) for row in causal_rows)
    label_counts = Counter(str(row["label_status"]) for row in label_rows)
    print(f"causal_rows={len(causal_rows)}")
    print(f"causal_revise={causal_counts.get('revise', 0)}")
    print(f"causal_review={causal_counts.get('review', 0)}")
    print(f"label_rows={len(label_rows)}")
    print(f"label_errors={sum(count for key, count in label_counts.items() if key.startswith('error'))}")
    print(f"label_reviews={sum(count for key, count in label_counts.items() if key.startswith('review'))}")
    print(f"causal_csv={args.out_causal}")
    print(f"labels_csv={args.out_labels}")
    print(f"report={args.out_report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
