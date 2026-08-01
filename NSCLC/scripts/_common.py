"""NSCLC SR HARD-gate ortak yardımcıları (stdlib-only).

Bu modül, deterministik denetçilerin paylaştığı küçük yardımcıları tutar:
bulgu tipi, Türkçe ondalık-virgül farkında sayı ayrıştırma, gecikmeli CSV
okuma (virgül/noktalı-virgül ayırıcı otomatik saptama). LLM yoktur; her karar
kural-tabanlıdır (HARD kapı doktrini: bkz. playbook §3, sci-audit referansı §0).
"""

from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass, field


@dataclass
class Finding:
    """Tek bir denetim bulgusu. level: 'blocker' | 'warning'."""

    check: str
    level: str
    message: str
    locator: str = ""

    def render(self) -> str:
        loc = f" [{self.locator}]" if self.locator else ""
        return f"  - [{self.level.upper()}] ({self.check}){loc} {self.message}"


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)

    def add(self, *args, **kwargs) -> None:
        self.findings.append(Finding(*args, **kwargs))

    @property
    def blockers(self) -> list[Finding]:
        return [f for f in self.findings if f.level == "blocker"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.level == "warning"]

    def ok(self) -> bool:
        return len(self.blockers) == 0


# "0,72" | "0.72" | "1.234,5" -> float; boş/eksik -> None
_NUM_RE = re.compile(r"^-?\d{1,3}(?:[.\s]\d{3})*(?:,\d+)?$|^-?\d+(?:[.,]\d+)?$")


def to_float(raw: str | None):
    """Türkçe ondalık virgül farkında sayı ayrıştırma.

    Kabul: '0,72' -> 0.72 ; '0.72' -> 0.72 ; '12' -> 12.0 ; '' -> None.
    Belirsiz/uydurma-olmayan-sayı için None döndürür (çağıran karar verir).
    """
    if raw is None:
        return None
    s = raw.strip()
    if s == "" or s.lower() in {"na", "n/a", "nr", "unverified", "-"}:
        return None
    if not _NUM_RE.match(s):
        return None
    # binlik ayırıcı olarak nokta/boşluk + ondalık virgül (tr) -> normalize
    if "," in s and "." in s:
        s = s.replace(".", "").replace(" ", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def sniff_delimiter(sample: str) -> str:
    """Ayırıcıyı sapta: Türkçe ondalıklı veri CSV'leri ';' önerilir; başlık
    satırındaki ';' varsa onu, yoksa ',' kullan."""
    first = sample.splitlines()[0] if sample else ""
    if first.count(";") >= 1:
        return ";"
    return ","


def read_rows(path: str) -> list[dict]:
    """CSV -> dict listesi; '#' ile başlayan yorum satırları atlanır."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    delim = sniff_delimiter(text)
    lines = [ln for ln in text.splitlines() if not ln.lstrip().startswith("#")]
    reader = csv.DictReader(io.StringIO("\n".join(lines)), delimiter=delim)
    return [dict(r) for r in reader]


def print_report(name: str, report: Report) -> int:
    """Raporu yazdır; blocker varsa exit-kod 1, yoksa 0 döndür."""
    if report.findings:
        print(f"[{name}] {len(report.blockers)} blocker, "
              f"{len(report.warnings)} warning:")
        for f in report.findings:
            print(f.render())
    else:
        print(f"[{name}] temiz (0 bulgu)")
    return 1 if report.blockers else 0
