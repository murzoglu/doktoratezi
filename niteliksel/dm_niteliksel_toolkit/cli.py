from __future__ import annotations

import argparse
from pathlib import Path

from .anonymization import assert_not_protected_write
from .audit_log import append_ai_use, write_ai_log_template
from .codebook import lint_codebook, write_codebook_report, write_codebook_template
from .common import safe_write_text
from .coreq import audit_coreq, write_coreq_template
from .cross_repo import build_cross_repo_status, write_cross_repo_status
from .quote_integrity import check_quotes, write_quote_report
from .reporting import find_negative_cases
from .tool_bridge import build_bridge_context, render_route, route_query, write_or_print
from .triadic_matrix import build_triadic_matrix, write_triadic_template


MEMO_TEMPLATE = """# Refleksif Memo

## Tarih

## Bağlam

## Araştırmacı Konumu

## Analitik Gözlem

## Alternatif Yorum / Negatif Vaka Olasılığı

## Araştırmacı Kararı
"""


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ValueError as exc:
        parser.exit(2, f"error: {exc}\n")
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dmnitel", description="DM niteliksel araştırma yardımcı CLI aracı.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Güvenli proje klasörleri ve şablonları oluşturur.")
    init_parser.add_argument("--root", default=".", help="Proje kökü. Varsayılan: bulunduğun dizin.")
    init_parser.set_defaults(func=cmd_init)

    bridge_parser = subparsers.add_parser("ai-context", help="Dmnitel + Evidentia + t1dm-tez bridge bağlamını güvenli biçimde yazdırır.")
    bridge_parser.add_argument("--format", default="markdown", choices=["markdown", "json"])
    bridge_parser.add_argument("--output", help="Bağlam paketini dosyaya yaz.")
    bridge_parser.set_defaults(func=cmd_ai_context)

    route_parser = subparsers.add_parser("route-tool", help="Soruya göre dmnitel, Evidentia veya t1dm-tez akışını seçer.")
    route_parser.add_argument("--query", required=True)
    route_parser.add_argument("--format", default="markdown", choices=["markdown", "json"])
    route_parser.add_argument("--output", help="Route raporunu dosyaya yaz.")
    route_parser.set_defaults(func=cmd_route_tool)

    cross_repo_parser = subparsers.add_parser(
        "cross-repo-status",
        help="Nitel ve nicel repo arasındaki karma tez yazım köprüsünü güvenli biçimde raporlar.",
    )
    cross_repo_parser.add_argument("--format", default="markdown", choices=["markdown", "json"])
    cross_repo_parser.add_argument("--output", help="Cross-repo durum raporunu dosyaya yaz.")
    cross_repo_parser.set_defaults(func=cmd_cross_repo_status)

    codebook_parser = subparsers.add_parser("lint-codebook", help="Kod kitabı tutarlılık denetimi yapar.")
    codebook_parser.add_argument("codebook")
    codebook_parser.add_argument("--output", default="07_reports/codebook_lint_report.md")
    codebook_parser.set_defaults(func=cmd_lint_codebook)

    triadic_parser = subparsers.add_parser("build-triadic-matrix", help="Kodlu segmentlerden triadik matris taslağı üretir.")
    triadic_parser.add_argument("--coded-data", required=True)
    triadic_parser.add_argument("--output", required=True)
    triadic_parser.set_defaults(func=cmd_build_triadic_matrix)

    quotes_parser = subparsers.add_parser("check-quotes", help="Kullanılan alıntıların kaynak dökümle bütünlüğünü kontrol eder.")
    quotes_parser.add_argument("--source", required=True)
    quotes_parser.add_argument("--quotes", required=True)
    quotes_parser.add_argument("--output", default="07_reports/quote_integrity_report.md")
    quotes_parser.set_defaults(func=cmd_check_quotes)

    coreq_parser = subparsers.add_parser("audit-coreq", help="COREQ 32 madde için metin içi kanıt denetimi yapar.")
    coreq_parser.add_argument("--methods", required=True)
    coreq_parser.add_argument("--results", required=True)
    coreq_parser.add_argument("--output", default="05_coreq_audit/coreq_audit_report.md")
    coreq_parser.set_defaults(func=cmd_audit_coreq)

    negative_parser = subparsers.add_parser("find-negative-cases", help="Tema için olası negatif vaka adaylarını listeler.")
    negative_parser.add_argument("--coded-data", required=True)
    negative_parser.add_argument("--theme", required=True)
    negative_parser.add_argument("--output")
    negative_parser.set_defaults(func=cmd_find_negative_cases)

    log_parser = subparsers.add_parser("log-ai-use", help="AI/MCP kullanım günlüğüne satır ekler.")
    log_parser.add_argument("--tool", required=True)
    log_parser.add_argument("--model", required=True)
    log_parser.add_argument("--purpose", required=True)
    log_parser.add_argument("--data-type", required=True)
    log_parser.add_argument("--output-summary", required=True)
    log_parser.add_argument("--researcher-decision", default="")
    log_parser.add_argument("--contains-raw-data", default="no", choices=["yes", "no"])
    log_parser.add_argument("--contains-identifiable-data", default="no", choices=["yes", "no"])
    log_parser.add_argument("--external-api-used", default="no", choices=["yes", "no"])
    log_parser.add_argument("--log", default="99_ai_use_log/ai_use_log.csv")
    log_parser.set_defaults(func=cmd_log_ai_use)

    return parser


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.root)
    dirs = [
        "00_raw_locked",
        "01_deidentified",
        "02_codebook",
        "03_memos",
        "04_triadic_matrices",
        "05_coreq_audit",
        "06_manuscript_outputs",
        "07_reports",
        "99_ai_use_log",
    ]
    for directory in dirs:
        (root / directory).mkdir(parents=True, exist_ok=True)

    created = []
    skipped = []
    actions = [
        (root / "02_codebook/codebook_template.csv", write_codebook_template),
        (root / "05_coreq_audit/coreq_32_template.csv", write_coreq_template),
        (root / "99_ai_use_log/ai_use_log.csv", write_ai_log_template),
        (root / "04_triadic_matrices/triadic_matrix_template.csv", write_triadic_template),
    ]
    for path, writer in actions:
        if writer(path):
            created.append(path)
        else:
            skipped.append(path)

    memo_path = root / "03_memos/reflexive_memo_template.md"
    if safe_write_text(memo_path, MEMO_TEMPLATE):
        created.append(memo_path)
    else:
        skipped.append(memo_path)

    print(f"Oluşturulan dosya: {len(created)}")
    for path in created:
        print(f"created: {path}")
    for path in skipped:
        print(f"exists: {path}")
    return 0


def cmd_ai_context(args: argparse.Namespace) -> int:
    if args.output:
        assert_not_protected_write(Path(args.output))
    write_or_print(build_bridge_context(args.format), args.output)
    return 0


def cmd_route_tool(args: argparse.Namespace) -> int:
    if args.output:
        assert_not_protected_write(Path(args.output))
    write_or_print(render_route(route_query(args.query), args.format), args.output)
    return 0


def cmd_cross_repo_status(args: argparse.Namespace) -> int:
    write_cross_repo_status(build_cross_repo_status(args.format), args.output)
    return 0


def cmd_lint_codebook(args: argparse.Namespace) -> int:
    assert_not_protected_write(Path(args.output))
    issues = lint_codebook(Path(args.codebook))
    write_codebook_report(issues, Path(args.output))
    print(f"Rapor yazıldı: {args.output}")
    return 1 if any(issue.severity == "critical" for issue in issues) else 0


def cmd_build_triadic_matrix(args: argparse.Namespace) -> int:
    assert_not_protected_write(Path(args.output))
    rows = build_triadic_matrix(Path(args.coded_data), Path(args.output))
    print(f"Triadik matris yazıldı: {args.output} ({len(rows)} satır)")
    return 0


def cmd_check_quotes(args: argparse.Namespace) -> int:
    assert_not_protected_write(Path(args.output))
    issues = check_quotes(Path(args.source), Path(args.quotes))
    write_quote_report(issues, Path(args.output))
    print(f"Rapor yazıldı: {args.output}")
    return 1 if any(issue.severity == "critical" for issue in issues) else 0


def cmd_audit_coreq(args: argparse.Namespace) -> int:
    assert_not_protected_write(Path(args.output))
    rows = audit_coreq(Path(args.methods), Path(args.results), Path(args.output))
    missing = sum(1 for row in rows if row.status == "missing")
    print(f"COREQ raporu yazıldı: {args.output} (missing={missing})")
    return 0


def cmd_find_negative_cases(args: argparse.Namespace) -> int:
    output = Path(args.output) if args.output else None
    if output is not None:
        assert_not_protected_write(output)
    report = find_negative_cases(Path(args.coded_data), args.theme, output)
    print(f"Rapor yazıldı: {report}")
    return 0


def cmd_log_ai_use(args: argparse.Namespace) -> int:
    assert_not_protected_write(Path(args.log))
    append_ai_use(
        Path(args.log),
        tool=args.tool,
        model=args.model,
        purpose=args.purpose,
        data_type=args.data_type,
        output_summary=args.output_summary,
        researcher_decision=args.researcher_decision,
        contains_raw_data=args.contains_raw_data,
        contains_identifiable_data=args.contains_identifiable_data,
        external_api_used=args.external_api_used,
    )
    print(f"AI kullanım günlüğü güncellendi: {args.log}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
