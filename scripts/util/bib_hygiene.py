#!/usr/bin/env python3
"""Çevrimdışı bib hijyen denetçisi (bağımlılıksız).

references.bib + chapters/*.qmd + referans-denetim-ledgeri.md üzerinde
atıf↔künye↔ledger mutabakatı, AMA-11 alan-tamlığı, DOI/PMID sağlığı ve
yakın-duplikat kontrolü yapar. Ağ çağrısı yapmaz; dosya yazmaz (rapor hariç);
references.bib'i değiştirmez.
"""
from __future__ import annotations

import argparse
import glob as _glob
import json
import pathlib
import re

_ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.MULTILINE)
# citeproc anahtarı: @ ardından harf/rakam ve iç noktalama; e-posta/@handle'ı dışlamak için
# yalnız [@...], @word başı yakalanır.
_CITE_RE = re.compile(r"(?<![A-Za-z0-9])-?@([A-Za-z0-9][\w:.#$%&+?<>~/-]*)")

_DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
_PMID_RE = re.compile(r"^\d{1,9}$")

# Quarto çapraz-referans önekleri (@fig-…, @tbl-…, @sec-…) bibliyografya atfı
# değil crossref'tir; künye mutabakatında "tanımsız atıf" sanılmamalı.
_XREF_PREFIXES = (
    "fig", "tbl", "sec", "eq", "lst", "thm", "lem", "cor",
    "prp", "cnj", "def", "exm", "exr",
)
_XREF_RE = re.compile(r"^(?:%s)[-:]" % "|".join(_XREF_PREFIXES))


def parse_bib(text: str) -> list[dict]:
    """BibTeX metnini entry listesine ayrıştır (basit, brace-dengeli)."""
    entries: list[dict] = []
    for m in _ENTRY_RE.finditer(text):
        etype = m.group(1).lower()
        key = m.group(2)
        line = text.count("\n", 0, m.start()) + 1
        # entry gövdesini brace dengesiyle çek
        i = text.index("{", m.start())
        depth = 0
        j = i
        while j < len(text):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        body = text[i + 1 : j]
        fields = _parse_fields(body)
        entries.append({"type": etype, "key": key, "fields": fields, "line": line})
    return entries


def _parse_fields(body: str) -> dict:
    """entry gövdesinden field=value çiftlerini çıkar (brace veya tırnak değer)."""
    fields: dict[str, str] = {}
    for fm in re.finditer(r"(\w+)\s*=\s*", body):
        name = fm.group(1).lower()
        pos = fm.end()
        if pos >= len(body):
            break
        ch = body[pos]
        if ch == "{":
            depth = 0
            k = pos
            while k < len(body):
                if body[k] == "{":
                    depth += 1
                elif body[k] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                k += 1
            val = body[pos + 1 : k]
        elif ch == '"':
            k = body.index('"', pos + 1)
            val = body[pos + 1 : k]
        else:
            k = pos
            while k < len(body) and body[k] not in ",\n":
                k += 1
            val = body[pos:k].strip()
        fields[name] = " ".join(val.split())
    return fields


def cited_keys(qmd_text: str) -> set[str]:
    """qmd/markdown metninden citeproc anahtarlarını çıkar.

    Quarto çapraz-referansları (@fig-…, @tbl-…, @sec-… vb.) bibliyografya
    atfı olmadığından mutabakat dışı bırakılır.
    """
    return {
        m.group(1)
        for m in _CITE_RE.finditer(qmd_text)
        if not _XREF_RE.match(m.group(1))
    }


def reconcile(bib_entries: list[dict], cited: set[str]) -> dict:
    """Atıflı↔tanımlı fark: undefined (render kırar) + orphan (atıfsız)."""
    defined = {e["key"] for e in bib_entries}
    return {
        "undefined": sorted(cited - defined),
        "orphan": sorted(defined - cited),
    }


REQUIRED_FIELDS: dict[str, list[str]] = {
    "article": ["author", "title", "journal", "year", "volume", "pages"],
    "mastersthesis": ["author", "title", "school", "year", "type"],
    "phdthesis": ["author", "title", "school", "year", "type"],
    "book": ["title", "publisher", "address", "year"],
    "incollection": ["title", "booktitle", "publisher", "year", "pages"],
    "inbook": ["title", "publisher", "year", "pages"],
}


def check_fields(bib_entries: list[dict]) -> list[dict]:
    """AMA-11 zorunlu alan eksiklerini raporla (WARN düzeyi)."""
    issues: list[dict] = []
    for e in bib_entries:
        req = REQUIRED_FIELDS.get(e["type"])
        if not req:
            continue
        f = e["fields"]
        missing = [r for r in req if not f.get(r)]
        # Cilt (volume) muafiyeti: bazı dergiler (ör. sayı-esaslı Türkçe
        # dergiler, derleme veritabanları) cilt numarası kullanmaz. Sayı
        # (number/issue) + sayfa/madde-no varsa APA-7/AMA künyeyi tam sayar;
        # bu meşru künyeler volume-eksik SOFT'unu tetiklememelidir.
        if (
            e["type"] == "article"
            and "volume" in missing
            and f.get("number")
            and f.get("pages")
        ):
            missing.remove("volume")
        # author|editor: en az biri olmalı
        if e["type"] in ("book", "incollection", "inbook") and not (
            f.get("author") or f.get("editor")
        ):
            missing.append("author|editor")
        if missing:
            issues.append({"key": e["key"], "type": e["type"], "missing": missing})
    return issues


def check_ids(bib_entries: list[dict]) -> dict:
    """DOI biçim geçerliği, atıflı makalede DOI eksikliği ve yinelenen DOI."""
    bad_doi: list[dict] = []
    missing_doi: list[str] = []
    # DOI'si olmayan ama PMID/URL ile erişilebilir meşru makaleler (ör. eski
    # ya da Türkçe dergiler DOI atamamış olabilir). Bunlar eksik değildir;
    # SOFT kapısını tetiklememeleri için ayrı listelenir.
    no_doi_accessible: list[str] = []
    doi_map: dict[str, list[str]] = {}
    for e in bib_entries:
        f = e["fields"]
        doi = (f.get("doi") or "").strip()
        pmid = (f.get("pmid") or "").strip()
        url = (f.get("url") or "").strip()
        if doi:
            if not _DOI_RE.match(doi):
                bad_doi.append({"key": e["key"], "doi": doi})
            doi_map.setdefault(doi.lower(), []).append(e["key"])
        elif e["type"] == "article":
            if pmid or url:
                no_doi_accessible.append(e["key"])
            else:
                missing_doi.append(e["key"])
        if pmid and not _PMID_RE.match(pmid):
            bad_doi.append({"key": e["key"], "doi": f"pmid:{pmid}"})
    dup_doi = [
        {"doi": d, "keys": sorted(ks)} for d, ks in doi_map.items() if len(ks) > 1
    ]
    return {
        "bad_doi": bad_doi,
        "missing_doi": sorted(missing_doi),
        "no_doi_accessible": sorted(no_doi_accessible),
        "dup_doi": dup_doi,
    }


def _norm_tokens(s: str) -> set[str]:
    """Başlık/yazar metnini küçük harf token'lerine ayrıştır."""
    return set(re.findall(r"[a-z0-9]+", s.lower()))


def _jaccard(a: set[str], b: set[str]) -> float:
    """İki token seti arasında Jaccard benzerliğini hesapla."""
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def check_dedup(bib_entries: list[dict], threshold: float = 0.85) -> list[dict]:
    """Başlık(+ilk yazar soyadı) Jaccard benzerliğiyle yakın-duplikat çiftleri."""
    sigs = []
    for e in bib_entries:
        f = e["fields"]
        first_author = re.split(r"\s+and\s+", f.get("author", ""))[0]
        surname = _norm_tokens(first_author.split(",")[0])
        title = _norm_tokens(f.get("title", ""))
        sigs.append((e["key"], title | surname))
    pairs: list[dict] = []
    for i in range(len(sigs)):
        for j in range(i + 1, len(sigs)):
            sim = _jaccard(sigs[i][1], sigs[j][1])
            if sim >= threshold:
                pairs.append({"a": sigs[i][0], "b": sigs[j][0], "sim": round(sim, 3)})
    pairs.sort(key=lambda p: p["sim"], reverse=True)
    return pairs


# ---------------------------------------------------------------------------
# Task 5: CLI + rapor + desired-scheme + exit-code
# ---------------------------------------------------------------------------

# Anahtar+keywords+BAŞLIK semantik-etiket -> alt-koleksiyon (9ZFDHMZA şeması).
# Sıra = öncelik (düşük→yüksek); son eşleşen token kazanır, böylece özgül temalar
# (kardeş/embu/maternal/ölçek) genel diyabet token'larını ezer.
_TAG_TO_SUBCOLLECTION = {
    # genel T1DM (düşük öncelik)
    "diabet": "T1DM Psikososyal",
    "t1d": "T1DM Psikososyal",
    "type 1": "T1DM Psikososyal",
    "glycemic": "T1DM Psikososyal",
    "glycaemic": "T1DM Psikososyal",
    "hba1c": "T1DM Psikososyal",
    "ispad": "T1DM Psikososyal",
    "psychosocial": "T1DM Psikososyal",
    "distress": "T1DM Psikososyal",
    "hypoglyc": "T1DM Psikososyal",
    # KİA / Yaşam Kalitesi
    "quality of life": "KİA / Yaşam Kalitesi",
    "qol": "KİA / Yaşam Kalitesi",
    "well-being": "KİA / Yaşam Kalitesi",
    "wellbeing": "KİA / Yaşam Kalitesi",
    "kia": "KİA / Yaşam Kalitesi",
    # Ölçek Geçerlik / COSMIN
    "cosmin": "Ölçek Geçerlik / COSMIN",
    "psychometric": "Ölçek Geçerlik / COSMIN",
    "validation": "Ölçek Geçerlik / COSMIN",
    "validity": "Ölçek Geçerlik / COSMIN",
    "reliability": "Ölçek Geçerlik / COSMIN",
    "factor analysis": "Ölçek Geçerlik / COSMIN",
    "measurement": "Ölçek Geçerlik / COSMIN",
    "ölçek": "Ölçek Geçerlik / COSMIN",
    "geçerlik": "Ölçek Geçerlik / COSMIN",
    # EMBU / Ebeveynlik Tutumu
    "embu": "EMBU / Ebeveynlik Tutumu",
    "parenting": "EMBU / Ebeveynlik Tutumu",
    "parental": "EMBU / Ebeveynlik Tutumu",
    "rearing": "EMBU / Ebeveynlik Tutumu",
    "ebeveyn": "EMBU / Ebeveynlik Tutumu",
    # Maternal Depresyon / Beck
    "maternal": "Maternal Depresyon / Beck",
    "depress": "Maternal Depresyon / Beck",
    "beck": "Maternal Depresyon / Beck",
    "bdi": "Maternal Depresyon / Beck",
    "anxiety": "Maternal Depresyon / Beck",
    # Kardeş Uyumu (yüksek öncelik)
    "sibling": "Kardeş Uyumu",
    "kardeş": "Kardeş Uyumu",
    "kardes": "Kardeş Uyumu",
}


def desired_scheme(bib_entries: list[dict]) -> dict:
    """Her künye için istenen alt-koleksiyon + etiketleri key+keywords+BAŞLIK'tan türet (ÇEVRİMDIŞI)."""
    scheme: dict = {}
    for e in bib_entries:
        f = e["fields"]
        hay = " ".join([e["key"], f.get("keywords", ""), f.get("title", "")]).lower()
        sub = "Genel"
        for token, subcol in _TAG_TO_SUBCOLLECTION.items():
            if token in hay:
                sub = subcol
        if e["type"] in ("mastersthesis", "phdthesis") or "yoktez" in e["key"].lower():
            sub = "Türkiye / YÖK Tez"
        tags: set[str] = set()
        if any(t in hay for t in ("sibling", "kardeş", "kardes")):
            tags.add("sibling")
        if any(t in hay for t in ("embu", "parent", "rearing", "ebeveyn")):
            tags.add("embu")
        if any(t in hay for t in ("maternal", "depress", "beck", "bdi")):
            tags.add("maternal-depression")
        if any(t in hay for t in ("cosmin", "psychometric", "validation", "validity",
                                   "reliability", "measurement", "ölçek", "geçerlik")):
            tags.add("measurement")
        if any(t in hay for t in ("turkiye", "türkiye", "turkish")) or e["type"] in ("mastersthesis", "phdthesis"):
            tags.add("turkiye")
        scheme[e["key"]] = {"subcollection": sub, "tags": sorted(tags) or ["t1dm"]}
    return scheme


def run_all(bib_path: str, chapters: list[str]) -> dict:
    """Tüm çevrimdışı kontrolleri koştur, birleşik sonuç döndür."""
    bib_text = pathlib.Path(bib_path).read_text(encoding="utf-8")
    entries = parse_bib(bib_text)
    cited: set[str] = set()
    for c in chapters:
        for p in _glob.glob(c):
            cited |= cited_keys(pathlib.Path(p).read_text(encoding="utf-8"))
    return {
        "counts": {"entries": len(entries), "cited": len(cited)},
        "reconcile": reconcile(entries, cited),
        "fields": check_fields(entries),
        "ids": check_ids(entries),
        "dedup": check_dedup(entries),
    }


def _severity(res: dict) -> int:
    if res["reconcile"]["undefined"]:
        return 1  # HARD: render kırar
    soft = res["fields"] or res["ids"]["missing_doi"] or res["ids"]["bad_doi"] or res["dedup"]
    return 2 if soft else 0


def _render_report(res: dict) -> str:
    r = res["reconcile"]
    lines = ["# Bib Hijyen Raporu", "",
             f"- Künye: {res['counts']['entries']} · Atıflı anahtar: {res['counts']['cited']}", ""]
    lines += ["## HARD — Atıflı ama tanımsız (render kırar)"]
    lines += [f"- `{k}`" for k in r["undefined"]] or ["- (yok)"]
    lines += ["", "## SOFT — AMA-11 alan eksik"]
    lines += [f"- `{i['key']}` ({i['type']}): {', '.join(i['missing'])}" for i in res["fields"]] or ["- (yok)"]
    lines += ["", "## SOFT — DOI eksik/bozuk + yinelenen"]
    lines += [f"- eksik DOI: `{k}`" for k in res["ids"]["missing_doi"]] or ["- eksik yok"]
    lines += [f"- bozuk: `{d['key']}` = {d['doi']}" for d in res["ids"]["bad_doi"]]
    nda = res["ids"].get("no_doi_accessible") or []
    if nda:
        lines += ["", "## BİLGİ — DOI yok ama PMID/URL ile erişilebilir (SOFT değil)"]
        lines += [f"- `{k}`" for k in nda]
    lines += [f"- yinelenen DOI {d['doi']}: {', '.join(d['keys'])}" for d in res["ids"]["dup_doi"]]
    lines += ["", "## SOFT — yakın-duplikat"]
    lines += [f"- `{p['a']}` ↔ `{p['b']}` (sim={p['sim']})" for p in res["dedup"]] or ["- (yok)"]
    lines += ["", "## INFO — orphan (tanımlı, atıfsız)"]
    lines += [f"- `{k}`" for k in r["orphan"]] or ["- (yok)"]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Çevrimdışı bib hijyen denetçisi")
    p.add_argument("command", choices=["reconcile", "fields", "ids", "dedup", "all", "desired-scheme"])
    p.add_argument("--bib", default="references/references.bib")
    p.add_argument("--chapters", nargs="*", default=["chapters/*.qmd"])
    p.add_argument("--json", action="store_true")
    p.add_argument("--out")
    a = p.parse_args(argv)
    bib_text = pathlib.Path(a.bib).read_text(encoding="utf-8")
    entries = parse_bib(bib_text)
    if a.command == "desired-scheme":
        out = desired_scheme(entries)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    res = run_all(a.bib, a.chapters)
    if a.out:
        pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(a.out).write_text(_render_report(res), encoding="utf-8")
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(_render_report(res))
    return _severity(res)


if __name__ == "__main__":
    raise SystemExit(main())
