from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .common import AI_SAFETY_STATEMENT, normalize_key, read_csv, safe_write_csv


COREQ_FIELDS = [
    "item_no",
    "domain",
    "item",
    "guiding_question",
    "status",
    "evidence_location",
    "missing_information",
    "recommendation",
    "thesis_location",
    "manuscript_location",
]

ALLOWED_COREQ_STATUSES = {"complete", "partial", "missing", "not_applicable"}

COREQ_ITEMS = [
    (1, "Research team and reflexivity", "Interviewer/facilitator", "Which author conducted the interview or focus group?"),
    (2, "Research team and reflexivity", "Credentials", "What were the researcher’s credentials?"),
    (3, "Research team and reflexivity", "Occupation", "What was their occupation at the time of the study?"),
    (4, "Research team and reflexivity", "Gender", "Was the researcher male or female?"),
    (5, "Research team and reflexivity", "Experience and training", "What experience or training did the researcher have?"),
    (6, "Research team and reflexivity", "Relationship established", "Was a relationship established prior to study commencement?"),
    (7, "Research team and reflexivity", "Participant knowledge of interviewer", "What did participants know about the researcher?"),
    (8, "Research team and reflexivity", "Interviewer characteristics", "What characteristics were reported about the interviewer?"),
    (9, "Study design", "Methodological orientation and theory", "What methodological orientation underpinned the study?"),
    (10, "Study design", "Sampling", "How were participants selected?"),
    (11, "Study design", "Method of approach", "How were participants approached?"),
    (12, "Study design", "Sample size", "How many participants were included?"),
    (13, "Study design", "Non-participation", "How many refused or dropped out and why?"),
    (14, "Study design", "Setting of data collection", "Where was data collected?"),
    (15, "Study design", "Presence of non-participants", "Was anyone else present?"),
    (16, "Study design", "Description of sample", "What are the important sample characteristics?"),
    (17, "Study design", "Interview guide", "Were questions prompts or guides provided and pilot tested?"),
    (18, "Study design", "Repeat interviews", "Were repeat interviews carried out?"),
    (19, "Study design", "Audio/visual recording", "Did the research use audio or visual recording?"),
    (20, "Study design", "Field notes", "Were field notes made during or after interviews?"),
    (21, "Study design", "Duration", "What was the duration of interviews?"),
    (22, "Study design", "Data saturation", "Was data saturation discussed?"),
    (23, "Study design", "Transcripts returned", "Were transcripts returned to participants?"),
    (24, "Analysis and findings", "Number of data coders", "How many data coders coded the data?"),
    (25, "Analysis and findings", "Description of coding tree", "Did authors provide a coding tree?"),
    (26, "Analysis and findings", "Derivation of themes", "Were themes identified in advance or derived from data?"),
    (27, "Analysis and findings", "Software", "What software was used to manage data?"),
    (28, "Analysis and findings", "Participant checking", "Did participants provide feedback on findings?"),
    (29, "Analysis and findings", "Quotations presented", "Were participant quotations presented?"),
    (30, "Analysis and findings", "Data and findings consistent", "Was there consistency between data and findings?"),
    (31, "Analysis and findings", "Clarity of major themes", "Were major themes clearly presented?"),
    (32, "Analysis and findings", "Clarity of minor themes", "Were minor themes or diverse cases described?"),
]

COREQ_KEYWORDS = {
    1: ["interviewer", "görüşmeyi", "görüşmeci"],
    2: ["credential", "unvan", "derece", "doktor"],
    3: ["occupation", "meslek", "görev"],
    4: ["gender", "cinsiyet", "kadın", "erkek"],
    5: ["training", "nitel veri analizi konusunda eğitim", "klinik deneyime", "experience and training"],
    6: ["relationship established", "önceden bir klinik tedavi ilişkisi", "ilişki kurul"],
    7: ["participant knowledge", "katılımcılara çalışmanın amacı", "araştırmacıların rolü", "hekim kimliği açıklan"],
    8: ["interviewer characteristics", "refleksivite", "positionality"],
    9: ["methodological orientation", "reflexive thematic analysis", "refleksif tematik analiz"],
    10: ["sampling", "örneklem", "amaçlı"],
    11: ["approached", "davet", "yaklaşıldı"],
    12: ["sample size", "21", "7 aile"],
    13: ["refused", "drop", "redd", "katılmayan"],
    14: ["setting", "poliklinik", "hastane", "görüşme ortamı"],
    15: ["non-participants", "başka kimse", "eşlik eden", "herhangi bir aile üyesi veya sağlık personelinin bulunmadığı"],
    16: ["sample characteristics", "örneklem özellikleri", "demografik"],
    17: ["interview guide", "görüşme rehberi", "pilot"],
    18: ["repeat interviews", "tekrar görüşme"],
    19: ["audio", "recording", "ses kaydı", "ses kaydına"],
    20: ["field notes", "saha not"],
    21: ["duration", "görüşmelerin süresi", "görüşme süresi", "dakika"],
    22: ["saturation", "doygunluk", "bilgi gücü"],
    23: ["transcripts returned", "transkript", "katılımcıya geri"],
    24: ["coders", "kodlayıcı", "birinci araştırmacı", "ikinci araştırmacı", "kodlama ve tema geliştirme sürecinin ana sorumluluğunu"],
    25: ["coding tree", "kod ağacı", "codebook"],
    26: ["themes derived", "tümevarım", "tümdengelim", "katılımcı anlatılarına yakın", "önceden kapalı"],
    27: ["software", "yazılım", "word", "excel"],
    28: ["participant checking", "member checking", "katılımcı kontrol"],
    29: ["quotation", "alıntı"],
    30: ["data and findings", "veri ile bulgular", "bulguların veriyle", "veri-bulgu tutarlılığı"],
    31: ["major themes", "bulgular, tez yazımı için dört ana tema", "ana tema / makro tema"],
    32: ["minor themes", "alt tema", "negatif vaka", "diverse cases"],
}


@dataclass(frozen=True)
class CoreqAuditRow:
    item_no: int
    domain: str
    item: str
    guiding_question: str
    status: str
    evidence_location: str
    missing_information: str
    recommendation: str
    thesis_location: str = ""
    manuscript_location: str = ""


def default_coreq_rows() -> list[dict[str, str]]:
    rows = []
    for item_no, domain, item, question in COREQ_ITEMS:
        rows.append(
            {
                "item_no": str(item_no),
                "domain": domain,
                "item": item,
                "guiding_question": question,
                "status": "missing",
                "evidence_location": "",
                "missing_information": "",
                "recommendation": "",
                "thesis_location": "",
                "manuscript_location": "",
            }
        )
    return rows


def write_coreq_template(path: Path) -> bool:
    return safe_write_csv(path, COREQ_FIELDS, default_coreq_rows())


def load_coreq_rows(path: Path) -> list[dict[str, str]]:
    rows = read_csv(path)
    for row in rows:
        status = row.get("status", "")
        if status not in ALLOWED_COREQ_STATUSES:
            raise ValueError(f"Geçersiz COREQ status: {status!r}")
    return rows


def audit_coreq(methods_path: Path, results_path: Path, output: Path) -> list[CoreqAuditRow]:
    corpus = _load_markdown_corpus([methods_path, results_path])
    audit_rows: list[CoreqAuditRow] = []
    for item_no, domain, item, question in COREQ_ITEMS:
        evidence = _find_evidence(corpus, COREQ_KEYWORDS.get(item_no, []))
        if evidence:
            status = "complete"
            missing = ""
            recommendation = "Kanıt konumu araştırmacı tarafından doğrulanmalıdır."
        else:
            status = "missing"
            missing = "Metin içinde doğrudan kanıt bulunamadı."
            recommendation = "Bu madde için doğrudan kanıt eklenip eklenmeyeceği araştırmacı tarafından değerlendirilmelidir."
        audit_rows.append(
            CoreqAuditRow(
                item_no=item_no,
                domain=domain,
                item=item,
                guiding_question=question,
                status=status,
                evidence_location=evidence,
                missing_information=missing,
                recommendation=recommendation,
            )
        )
    write_coreq_report(audit_rows, output)
    return audit_rows


def write_coreq_report(rows: list[CoreqAuditRow], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# COREQ 32 Madde Uyum Denetimi",
        "",
        AI_SAFETY_STATEMENT,
        "",
        "| No | Domain | Madde | Durum | Kanıt | Öneri |",
        "|---:|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row.item_no} | {row.domain} | {row.item} | {row.status} | "
            f"{row.evidence_location or 'Kanıt bulunamadı'} | {row.recommendation} |"
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _load_markdown_corpus(paths: list[Path]) -> list[tuple[Path, int, str]]:
    corpus: list[tuple[Path, int, str]] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), start=1):
            corpus.append((path, line_no, line))
    return corpus


def _find_evidence(corpus: list[tuple[Path, int, str]], keywords: list[str]) -> str:
    keyword_keys = [normalize_key(keyword) for keyword in keywords]
    for path, line_no, line in corpus:
        line_key = normalize_key(line)
        if any(keyword and keyword in line_key for keyword in keyword_keys):
            return f"{path}:{line_no}"
    return ""
