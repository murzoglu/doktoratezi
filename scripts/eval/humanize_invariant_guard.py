#!/usr/bin/env python3
"""Akademik metin insansılaştırma — DOKUNULMAZLIK bekçisi + ritim ölçer (salt-okuma).

`/akademik-metin-insansilastirma` kapısının mekanik zorlama katmanıdır. İki soruyu
deterministik yanıtlar:

1. **Öz korundu mu?** Kaynak metin ile insansılaştırılmış aday metnin
   DOKUNULMAZ envanterini (sayı, birimli sayı, istatistik ifadesi, güven aralığı,
   atıf anahtarı, çapraz-referans, bölüm referansı, kanıt-düzeyi etiketi, çekince,
   olumsuzlama, YZ-kullanım beyanı) çokluk (multiset) olarak karşılaştırır.
   Düşme/mutasyon/uydurma-ekleme = HARD FAIL.
2. **Üslup gerçekten insansılaştı mı?** Cümle uzunluğu dağılımı (burstiness),
   sözcük çeşitliliği (perplexity vekili), LLM imza kalıbı yoğunluğu ve paragraf
   tekdüzeliği için ölçüm üretir; kaynak↔aday karşılaştırmasını raporlar.

Bu betik metni DEĞİŞTİRMEZ, dosyaya yazmaz, ağa çıkmaz. Yalnız stdlib kullanır.

Ölçüm notu: burstiness/perplexity vekilleri **sezgisel**dir; bir AI-dedektör
skorunu taklit etmez, yalnız "tekdüze LLM nesri" imzasını görünür kılar. Eşikler
CONFIG'te açık ve gerekçelidir.

Kullanım:
  python3 scripts/eval/humanize_invariant_guard.py inventory KAYNAK.md
  python3 scripts/eval/humanize_invariant_guard.py guard   --source K.md --candidate A.md
  python3 scripts/eval/humanize_invariant_guard.py metrics ADAY.md [--source K.md]
  python3 scripts/eval/humanize_invariant_guard.py all     --source K.md --candidate A.md [--json]

Exit: 0 = temiz · 1 = HARD (öz ihlali; teslim engeli) · 2 = SOFT (inceleme gerektirir)
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import statistics
import sys
from collections import Counter

_HERE = os.path.abspath(__file__)
_REPO = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
_UTIL = os.path.join(_REPO, "scripts", "util")
if _UTIL not in sys.path:
    sys.path.insert(0, _UTIL)

try:  # repo primitive'lerini yeniden kullan (kopyalama yok)
    from tr_corpus_audit import strip_fenced, tr_lower  # type: ignore
except Exception:  # pragma: no cover - bağımsız çalıştırma yedeği

    def tr_lower(s: str) -> str:
        return s.replace("I", "ı").replace("İ", "i").lower()

    def strip_fenced(text: str):
        out, in_fence, in_comment, tok = [], False, False, ""
        for i, line in enumerate(text.splitlines(), start=1):
            st = line.strip()
            if in_fence:
                if st.startswith(tok):
                    in_fence = False
                continue
            if in_comment:
                if "-->" in line:
                    in_comment = False
                continue
            if st.startswith("<!--"):
                if "-->" not in line:
                    in_comment = True
                continue
            if st.startswith("```") or st.startswith("~~~"):
                in_fence, tok = True, st[:3]
                continue
            if st.startswith("#|"):
                continue
            out.append((i, line))
        return out


# ---------------------------------------------------------------------------
# Veri yönetişimi: korumalı yollar bu araca girmez (KVKK sınırı)
# ---------------------------------------------------------------------------
BLOCKED_PREFIXES = (
    "data/raw",
    "data/identified",
    "data/cleaned",
    "data/backup",
    "_targets",
)


def assert_safe_path(path: str) -> None:
    """Ham/kimliklenebilir veri ve targets deposu bu bekçiye beslenemez."""
    real = os.path.realpath(path)
    try:
        rel = os.path.relpath(real, _REPO).replace(os.sep, "/")
    except ValueError:  # pragma: no cover - farklı sürücü
        return
    if rel.startswith(".."):
        return
    for pref in BLOCKED_PREFIXES:
        if rel == pref or rel.startswith(pref + "/"):
            raise SystemExit(
                f"REDDEDILDI: korumali veri yolu bu araca beslenemez -> {rel}"
            )


# ---------------------------------------------------------------------------
# CONFIG — eşikler ve sözlükler (açık + gerekçeli; hepsi sezgisel)
# ---------------------------------------------------------------------------
CONFIG = {
    # Burstiness: cümle uzunluğu varyasyon katsayısı (SS/ortalama).
    # Tekdüze LLM nesri tipik olarak 0,25-0,35 bandında toplanır.
    "cv_min": 0.40,
    # Goh-Barabasi burstiness indeksi B = (sigma-mu)/(sigma+mu); -1 tam düzenli.
    "burstiness_min": -0.45,
    # Kısa (<=10 sözcük) ve uzun (>=28 sözcük) cümle payı: ritim asimetrisi.
    "short_ratio_min": 0.10,
    "long_ratio_min": 0.10,
    # Ortalamanın +-%20 bandında ARDIŞIK cümle serisi: tekdüzelik imzası.
    # Eşik metin uzunluğuyla logaritmik büyür (uzun metinde uzun seri şansa bağlıdır):
    # esik = max(max_uniform_run_min, ceil(log2(cümle sayısı)))
    "max_uniform_run_min": 4,
    # LLM imza kalıbı yoğunluğu (1000 sözcük başına).
    "cliche_per_1000_max": 2.0,
    # Bağlaç/geçiş ifadesiyle BAŞLAYAN cümle payı.
    "connective_start_max": 0.25,
    # Sözcük çeşitliliği (perplexity vekili): MATTR (200 sözcüklük kayan pencere).
    # Ham TTR metin uzadıkça mekanik olarak düşer; eşik bu yüzden MATTR'a bağlıdır.
    "mattr_min": 0.60,
    "mattr_window": 200,
}

# LLM imza kalıpları — Türkçe akademik nesirde en sık "makine kokusu" veren
# geçiş/klişe öbekleri. Yasak değil; YOĞUNLUĞU ölçülür.
CLICHE_PATTERNS = [
    r"kapsamlı bir şekilde",
    r"kapsamlı bir biçimde",
    r"önem arz et",
    r"büyük önem taşı",
    r"dikkat çekicidir",
    r"göze çarpmaktadır",
    r"giderek artan bir (?:ilgi|önem)",
    r"son yıllarda (?:artan|giderek)",
    r"bu bağlamda",
    r"bu doğrultuda",
    r"bu çerçevede",
    r"genel olarak değerlendirildiğinde",
    r"özetle ifade etmek gerekirse",
    r"sonuç olarak (?:ifade|söylemek|belirtmek)",
    r"unutulmamalıdır ki",
    r"vurgulanması gereken",
    r"literatürde(?:ki)? çalışmalar (?:incelendiğinde|göz önüne)",
    r"çok boyutlu bir (?:yapı|olgu|süreç)",
    r"dinamik bir (?:yapı|süreç|etkileşim)",
    r"kritik bir rol oyna",
    r"hayati bir öneme sahip",
    r"yalnızca .{0,40} değil,? aynı zamanda",
    r"hem .{0,30} hem de .{0,30} açısından",
    r"derinlemesine bir (?:anlayış|kavrayış)",
    r"ışık tutmaktadır",
    r"kapı aralamaktadır",
    r"göz ardı edilmemelidir",
    r"dikkate değer bir biçimde",
    r"bütüncül bir (?:yaklaşım|bakış|perspektif)",
    r"paradigma değişimi",
]

# Cümle BAŞI bağlaç/geçiş kalıpları (tekdüze akış imzası)
CONNECTIVE_STARTS = [
    "ayrıca",
    "bununla birlikte",
    "buna ek olarak",
    "bunun yanı sıra",
    "diğer taraftan",
    "öte yandan",
    "sonuç olarak",
    "özetle",
    "bu bağlamda",
    "bu doğrultuda",
    "bu çerçevede",
    "dolayısıyla",
    "bu nedenle",
    "böylece",
    "nitekim",
    "ilk olarak",
    "son olarak",
    "genel olarak",
]

# ---------------------------------------------------------------------------
# DOKUNULMAZ sınıflar
# ---------------------------------------------------------------------------
CROSSREF_PREFIXES = ("tbl", "fig", "sec", "eq", "thm", "lst")

# Kanıt-düzeyi / ön-kayıt etiketleri
LABEL_TOKENS = [
    "KEŞİFSEL",
    "KESIFSEL",
    "POST-HOC",
    "POST HOC",
    "DOĞRULAYICI",
    "DOGRULAYICI",
    "ÖN-KAYITLI",
    "ON-KAYITLI",
    "TEYİT EDİCİ",
]

# İstatistik sembolleri (op + değer ile birlikte yakalanır)
STAT_SYMBOLS = [
    "p", "d", "g", "r", "rho", "tau", "R2", "R²", "β", "beta", "b", "B",
    "OR", "RR", "HR", "AUC", "ICC", "α", "alpha", "ω", "omega", "CFI", "TLI",
    "RMSEA", "SRMR", "BF10", "BF₁₀", "BF01", "χ2", "χ²", "t", "F", "z", "N",
    "n", "M", "SD", "SS", "SE", "IQR", "η2", "η²", "ε²", "W", "U", "Q", "I2", "I²",
]

# Çekince / sınırlılık imleçleri — DÜŞMESİ HARD ihlaldir
HEDGE_TERMS = [
    "sınırlılık", "sınırlıdır", "nedensellik çıkarılamaz", "nedensel çıkarım",
    "kesitsel", "genellenemez", "genelleme yapılamaz", "dikkatle yorumlan",
    "ihtiyatla", "temkinli", "keşifsel", "post-hoc", "post hoc",
    "düzeltilmemiş", "çoklu karşılaştırma", "yanlılık", "yanlı",
    "örneklem büyüklüğü sınırlı", "güç analizi", "doğrulanmalıdır",
    "replikasyon", "ön bulgu", "kanıt düzeyi", "olabilir", "olabileceği",
    "düşündürmektedir", "işaret etmektedir", "önerilmektedir",
]

# Olumsuzlama imleçleri — DÜŞMESİ bulgunun yönünü ters çevirir (HARD)
NEGATION_TERMS = [
    "değildir", "değildi", "değil", "bulunmamıştır", "saptanmamıştır",
    "gözlenmemiştir", "gözlenmedi", "farklılık göstermemiştir",
    "anlamlı bulunmamış", "ilişki bulunmamış", "etki bulunmamış",
    "desteklenmemiştir", "doğrulanmamıştır", "yoktur", "izlenmemiştir",
    "ulaşmamıştır", "sağlanamamıştır",
]

# Kesinlik enflasyonu / nedensellik yükseltmesi — EKLENMESİ HARD ihlaldir
OVERCLAIM_TERMS = [
    "kesinlikle", "kesin olarak", "kuşkusuz", "şüphesiz", "tartışmasız",
    "kanıtlamaktadır", "kanıtlamıştır", "kanıtlanmıştır", "ispatlamaktadır",
    "her zaman", "her durumda", "istisnasız", "tamamen", "tümüyle",
    "neden olmaktadır", "neden olduğu gösterilmiştir", "yol açmaktadır",
    "belirlemektedir", "garanti etmektedir", "açıkça göstermektedir",
    "net biçimde göstermektedir", "hiçbir şekilde", "mutlak",
]

# Yön/polarite imleçleri — SOFT (yeniden ifade meşru olabilir, ama raporlanır)
DIRECTION_TERMS = [
    "artmış", "artmakta", "artış", "yüksek", "daha yüksek", "fazla",
    "azalmış", "azalmakta", "azalış", "düşük", "daha düşük", "az",
    "pozitif", "negatif", "olumlu", "olumsuz", "anlamlı", "anlamsız",
    "güçlü", "zayıf", "orta düzey",
]

# YZ-kullanım beyanı imleçleri — kaynakta varsa adayda KALMALIDIR (HARD)
AI_DISCLOSURE_TERMS = [
    "yapay zeka", "yapay zekâ", "büyük dil modeli", "dil modeli",
    "generative ai", "chatgpt", "gpt-", "claude", "gemini", "llm",
]

HARD_CLASSES = (
    "sayi",
    "birimli_sayi",
    "istatistik",
    "aralik",
    "atif",
    "capraz_ref",
    "bolum_ref",
    "etiket",
    "cekince",
    "olumsuzluk",
)
# Bu sınıflarda EKLEME de HARD'dır (uydurma veri/kaynak).
NO_ADD_CLASSES = ("sayi", "birimli_sayi", "istatistik", "aralik", "atif", "capraz_ref")

UNIT_PATTERN = (
    r"%|‰|mg/dL|mmol/mol|mmol/L|mg/dl|kg/m²|kg/m2|kg|cm|mm|ml|mL|IU|Ü|"
    r"yıl|ay|hafta|gün|saat|dakika|puan|kez|kişi|aile|birim|SS|SD|point"
)


# ---------------------------------------------------------------------------
# Metin hazırlama
# ---------------------------------------------------------------------------
def read_text(path: str) -> str:
    assert_safe_path(path)
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def body_text(text: str) -> str:
    """YAML front-matter, kod-çiti, `#|` ve HTML yorumları düşer."""
    if text.startswith("---"):
        parts = text.split("\n---", 2)
        if len(parts) >= 2:
            rest = text.split("\n", 1)[1] if "\n" in text else ""
            m = re.search(r"^---\s*$", rest, flags=re.M)
            if m:
                text = rest[m.end():]
    return "\n".join(line for _, line in strip_fenced(text))


def _norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _norm_num(s: str) -> str:
    """Unicode eksi/tire ve ince boşluk normalize; ondalık ayraç KORUNUR."""
    return (
        s.replace("\u2212", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u00a0", "")
        .replace("\u202f", "")
        .replace(" ", "")
    )


# ---------------------------------------------------------------------------
# Envanter çıkarımı
# ---------------------------------------------------------------------------
def extract_inventory(text: str) -> Counter:
    """DOKUNULMAZ span çokluğu (Counter[(sinif, normalize_deger)])."""
    body = body_text(text)
    low = tr_lower(body)
    bag: Counter = Counter()

    # 1) Atıflar: [@key; @key2, s. 12] blokları + blok DIŞI satır-içi @key
    #    Blok içi anahtarlar bir kez sayılır; blok maskelenerek çift sayım önlenir.
    outside = body
    for m in re.finditer(r"\[(?:[^\]\[]*?@[^\]\[]+)\]", body):
        block = _norm_ws(m.group(0))
        keys = re.findall(r"@([A-Za-z][\w:.#$%&\-+?<>~/]*)", block)
        if not keys:
            continue
        bag[("atif_blok", block)] += 1
        for k in keys:
            if k.split("-")[0] not in CROSSREF_PREFIXES:
                bag[("atif", "@" + k.rstrip(".,;:"))] += 1
        outside = outside.replace(m.group(0), " " * len(m.group(0)), 1)
    for m in re.finditer(r"(?<![\w@])@([A-Za-z][\w:.#$%&\-+?<>~/]*)", outside):
        key = m.group(1)
        if key.split("-")[0] in CROSSREF_PREFIXES:
            continue
        bag[("atif", "@" + key.rstrip(".,;:"))] += 1

    # 2) Çapraz referanslar (@tbl-/@fig-/@sec-/@eq-)
    for m in re.finditer(
        r"@(?:%s)-[A-Za-z0-9_\-]+" % "|".join(CROSSREF_PREFIXES), body
    ):
        bag[("capraz_ref", m.group(0).rstrip(".,;:"))] += 1

    # 3) Bölüm referansları
    for m in re.finditer(r"§\s*[0-9]+(?:\.[0-9]+)*", body):
        bag[("bolum_ref", _norm_num(m.group(0)))] += 1

    # 4) Kanıt-düzeyi etiketleri
    for tok in LABEL_TOKENS:
        n = len(re.findall(re.escape(tr_lower(tok)), low))
        if n:
            bag[("etiket", tok.upper())] += n

    # 5) Güven aralıkları / aralık gösterimleri
    interval = (
        r"(?:%\s*9[05]\s*(?:GA|CI)|GA|CI)\s*[:=]?\s*"
        r"[\[\(]?\s*[−\-]?\d+(?:[.,]\d+)?\s*(?:[;,]|–|—|-|ile)\s*[−\-]?\d+(?:[.,]\d+)?\s*[\]\)]?"
    )
    for m in re.finditer(interval, body, flags=re.I):
        bag[("aralik", _norm_num(m.group(0)).upper())] += 1

    # 6) İstatistik ifadeleri (sembol + operatör + değer)
    sym = "|".join(sorted((re.escape(s) for s in STAT_SYMBOLS), key=len, reverse=True))
    stat = rf"(?<![\wğüşıöçĞÜŞİÖÇ])({sym})\s*(?:\([^)]{{0,20}}\))?\s*([<>=≤≥±]+)\s*([−\-]?\d+(?:[.,]\d+)?)"
    for m in re.finditer(stat, body):
        bag[("istatistik", _norm_num(f"{m.group(1)}{m.group(2)}{m.group(3)}"))] += 1

    # 7) Birimli sayılar (%12,4 · 7,8 yıl · 42 mg/dL)
    for m in re.finditer(rf"(%|‰)\s*(\d+(?:[.,]\d+)?)", body):
        bag[("birimli_sayi", _norm_num(m.group(1) + m.group(2)))] += 1
    for m in re.finditer(rf"([−\-]?\d+(?:[.,]\d+)?)\s*({UNIT_PATTERN})(?![\wğüşıöçĞÜŞİÖÇ])", body):
        bag[("birimli_sayi", _norm_num(m.group(1)) + " " + m.group(2))] += 1

    # 8) Çıplak sayılar (atıf yılı dahil; tüm sayısal öz)
    for m in re.finditer(r"(?<![A-Za-z0-9ğüşıöçĞÜŞİÖÇ])[−\-]?[0-9]+(?:[.,][0-9]+)*(?![0-9])", body):
        bag[("sayi", _norm_num(m.group(0)))] += 1

    # 9) Çekince / olumsuzlama / kesinlik / yön / YZ beyanı sözlükleri
    for cls, terms in (
        ("cekince", HEDGE_TERMS),
        ("olumsuzluk", NEGATION_TERMS),
        ("kesinlik", OVERCLAIM_TERMS),
        ("yon", DIRECTION_TERMS),
        ("yz_beyani", AI_DISCLOSURE_TERMS),
    ):
        for term in terms:
            n = len(re.findall(r"(?<![\wğüşıöçĞÜŞİÖÇ])" + re.escape(tr_lower(term)), low))
            if n:
                bag[(cls, term)] += n

    return bag


# ---------------------------------------------------------------------------
# Ritim / çeşitlilik ölçümü
# ---------------------------------------------------------------------------
_ABBREV = {
    "vb", "vd", "bkz", "ör", "örn", "ss", "s", "no", "dr", "prof", "doç",
    "yrd", "md", "age", "agm", "çev", "ed", "eds", "yay", "haz", "krş", "yak",
}


def split_sentences(text: str) -> list[str]:
    """Türkçe-duyarlı cümle bölme: ondalık virgül, kısaltma ve @token korumalı."""
    body = body_text(text)
    body = re.sub(r"^\s{0,3}#{1,6}\s.*$", " ", body, flags=re.M)  # başlıklar
    body = re.sub(r"^\s*[:\|].*$", " ", body, flags=re.M)  # tablo/div satırları
    body = _norm_ws(body)
    if not body:
        return []
    out, buf = [], ""
    tokens = re.split(r"(?<=[.!?…])\s+", body)
    for tok in tokens:
        buf = (buf + " " + tok).strip() if buf else tok
        tail = re.sub(r"[\"'»）\)\]]+$", "", buf).rstrip()
        last_word = tr_lower(re.split(r"[\s(]", tail)[-1]).rstrip(".!?…")
        if last_word in _ABBREV:
            continue
        if re.search(r"\b[0-9]+\.$", tail):  # "1." gibi liste/ordinal
            continue
        if tail.endswith((".", "!", "?", "…")):
            out.append(buf.strip())
            buf = ""
    if buf.strip():
        out.append(buf.strip())
    return [s for s in out if len(s.split()) >= 2]


def _words(s: str) -> list[str]:
    s = re.sub(r"\[[^\]]*@[^\]]*\]", " ", s)  # atıf blokları sayılmaz
    return re.findall(r"[\wğüşıöçĞÜŞİÖÇ%]+", s)


def _mattr(words: list[str], window: int) -> float:
    """Kayan pencere tür/belirteç oranı (Covington & McFall 2010).

    Ham TTR metin uzunluğuna mekanik olarak bağımlıdır (uzun metinde düşer);
    MATTR sabit pencereyle bu yanlılığı giderir. Pencereden kısa metinlerde
    ham TTR'ye düşer.
    """
    n = len(words)
    if n == 0:
        return 0.0
    if n <= window:
        return len(set(words)) / n
    vals = []
    counts: Counter = Counter(words[:window])
    vals.append(len(counts) / window)
    for i in range(window, n):
        out_w, in_w = words[i - window], words[i]
        counts[out_w] -= 1
        if counts[out_w] == 0:
            del counts[out_w]
        counts[in_w] += 1
        vals.append(len(counts) / window)
    return statistics.fmean(vals)


def _uniform_run_limit(n_sentences: int) -> int:
    """Tekdüze ardışık seri eşiği: uzun metinde uzun seri şansa bağlıdır."""
    if n_sentences < 2:
        return CONFIG["max_uniform_run_min"]
    return max(CONFIG["max_uniform_run_min"], math.ceil(math.log2(n_sentences)))


def compute_metrics(text: str) -> dict:
    sents = split_sentences(text)
    lens = [len(_words(s)) for s in sents]
    words = [tr_lower(w) for s in sents for w in _words(s)]
    n_s, n_w = len(sents), len(words)
    body_low = tr_lower(body_text(text))

    if n_s == 0:
        return {"n_sentence": 0, "n_word": 0, "note": "cümle bulunamadı"}

    mu = statistics.fmean(lens)
    sd = statistics.pstdev(lens) if n_s > 1 else 0.0
    cv = sd / mu if mu else 0.0
    burst = (sd - mu) / (sd + mu) if (sd + mu) else -1.0

    # ardışık tekdüzelik serisi: |len - mu| <= %20 mu
    band = 0.20 * mu
    run = best = 0
    for L in lens:
        if abs(L - mu) <= band:
            run += 1
            best = max(best, run)
        else:
            run = 0

    cliche = []
    for pat in CLICHE_PATTERNS:
        for m in re.finditer(pat, body_low):
            cliche.append(_norm_ws(m.group(0)))
    conn = sum(
        1
        for s in sents
        if any(tr_lower(s).lstrip("*_—-– ").startswith(c) for c in CONNECTIVE_STARTS)
    )
    types = len(set(words))
    hapax = sum(1 for _, c in Counter(words).items() if c == 1)
    mattr = _mattr(words, CONFIG["mattr_window"])

    paras = [p for p in re.split(r"\n\s*\n", body_text(text)) if len(p.split()) > 15]
    para_sc = [len(split_sentences(p)) for p in paras]
    para_cv = (
        statistics.pstdev(para_sc) / statistics.fmean(para_sc)
        if len(para_sc) > 1 and statistics.fmean(para_sc)
        else 0.0
    )

    return {
        "n_sentence": n_s,
        "n_word": n_w,
        "mean_len": round(mu, 2),
        "sd_len": round(sd, 2),
        "cv": round(cv, 3),
        "burstiness_index": round(burst, 3),
        "median_len": statistics.median(lens),
        "min_len": min(lens),
        "max_len": max(lens),
        "short_ratio": round(sum(1 for L in lens if L <= 10) / n_s, 3),
        "long_ratio": round(sum(1 for L in lens if L >= 28) / n_s, 3),
        "max_uniform_run": best,
        "max_uniform_run_limit": _uniform_run_limit(n_s),
        "cliche_hits": len(cliche),
        "cliche_per_1000": round(1000 * len(cliche) / n_w, 2) if n_w else 0.0,
        "cliche_list": sorted(Counter(cliche).items()),
        "connective_start_ratio": round(conn / n_s, 3),
        "ttr": round(types / n_w, 3) if n_w else 0.0,
        "mattr": round(mattr, 3),
        "hapax_ratio": round(hapax / n_w, 3) if n_w else 0.0,
        "paragraph_len_cv": round(para_cv, 3),
        "sentence_lengths": lens,
    }


def metric_findings(m: dict) -> list[str]:
    """CONFIG eşiklerine göre SOFT bulgular (üslup hedefi tutmadı)."""
    if not m.get("n_sentence"):
        return ["metrik hesaplanamadı (cümle yok)"]
    f = []
    if m["cv"] < CONFIG["cv_min"]:
        f.append(f"burstiness düşük: cv={m['cv']} < {CONFIG['cv_min']}")
    if m["burstiness_index"] < CONFIG["burstiness_min"]:
        f.append(
            f"burstiness indeksi düşük: B={m['burstiness_index']} < {CONFIG['burstiness_min']}"
        )
    if m["short_ratio"] < CONFIG["short_ratio_min"]:
        f.append(f"kısa cümle payı düşük: {m['short_ratio']} < {CONFIG['short_ratio_min']}")
    if m["long_ratio"] < CONFIG["long_ratio_min"]:
        f.append(f"uzun cümle payı düşük: {m['long_ratio']} < {CONFIG['long_ratio_min']}")
    if m["max_uniform_run"] > m["max_uniform_run_limit"]:
        f.append(
            f"tekdüze ardışık cümle serisi: {m['max_uniform_run']} > {m['max_uniform_run_limit']}"
        )
    if m["cliche_per_1000"] > CONFIG["cliche_per_1000_max"]:
        f.append(
            f"LLM imza kalıbı yoğun: {m['cliche_per_1000']}/1000 > {CONFIG['cliche_per_1000_max']}"
        )
    if m["connective_start_ratio"] > CONFIG["connective_start_max"]:
        f.append(
            f"bağlaçla başlayan cümle payı yüksek: {m['connective_start_ratio']} > {CONFIG['connective_start_max']}"
        )
    if m["mattr"] < CONFIG["mattr_min"]:
        f.append(f"sözcük çeşitliliği düşük: MATTR={m['mattr']} < {CONFIG['mattr_min']}")
    return f


# ---------------------------------------------------------------------------
# Karşılaştırma
# ---------------------------------------------------------------------------
def compare(source: str, candidate: str) -> dict:
    src, cnd = extract_inventory(source), extract_inventory(candidate)
    missing, added = src - cnd, cnd - src

    hard: list[tuple] = []
    soft: list[tuple] = []

    for (cls, val), n in sorted(missing.items()):
        if cls in HARD_CLASSES or cls == "yz_beyani":
            hard.append(("DÜŞTÜ", cls, val, n))
        else:
            soft.append(("düştü", cls, val, n))
    for (cls, val), n in sorted(added.items()):
        if cls in NO_ADD_CLASSES:
            hard.append(("UYDURULDU", cls, val, n))
        elif cls == "kesinlik":
            hard.append(("KESİNLİK ENFLASYONU", cls, val, n))
        else:
            soft.append(("eklendi", cls, val, n))

    return {
        "source_spans": sum(src.values()),
        "candidate_spans": sum(cnd.values()),
        "hard": hard,
        "soft": soft,
        "src_bag": src,
        "cnd_bag": cnd,
    }


# ---------------------------------------------------------------------------
# Raporlama
# ---------------------------------------------------------------------------
def print_inventory(bag: Counter) -> None:
    print(f"DOKUNULMAZ ENVANTER — toplam span: {sum(bag.values())}")
    for cls in sorted({c for c, _ in bag}):
        items = sorted((v, n) for (c, v), n in bag.items() if c == cls)
        total = sum(n for _, n in items)
        flag = "HARD" if cls in HARD_CLASSES or cls == "yz_beyani" else "SOFT"
        print(f"\n[{flag}] {cls} ({total})")
        for val, n in items:
            print(f"    {val}" + (f" x{n}" if n > 1 else ""))


def print_compare(res: dict) -> None:
    print(
        f"ÖZ KARŞILAŞTIRMASI — kaynak span={res['source_spans']} · aday span={res['candidate_spans']}"
    )
    if res["hard"]:
        print("\nHARD İHLAL (teslim engeli — öz değişmiş):")
        for kind, cls, val, n in res["hard"]:
            print(f"  ! [{kind}] {cls}: {val!r}" + (f" x{n}" if n > 1 else ""))
    if res["soft"]:
        print("\nSOFT (inceleme gerektirir — meşru olabilir, gerekçelendir):")
        for kind, cls, val, n in res["soft"]:
            print(f"  ~ [{kind}] {cls}: {val!r}" + (f" x{n}" if n > 1 else ""))
    if not res["hard"] and not res["soft"]:
        print("PASS: düşme yok, mutasyon yok, uydurma yok.")


def print_metrics(m: dict, title: str) -> None:
    print(f"\nRİTİM/ÇEŞİTLİLİK — {title}")
    if not m.get("n_sentence"):
        print("  (cümle bulunamadı)")
        return
    print(
        f"  cümle={m['n_sentence']} sözcük={m['n_word']} ort={m['mean_len']} "
        f"SS={m['sd_len']} cv={m['cv']} B={m['burstiness_index']}"
    )
    print(
        f"  min/medyan/maks={m['min_len']}/{m['median_len']}/{m['max_len']} "
        f"kısa={m['short_ratio']} uzun={m['long_ratio']} "
        f"tekdüze_seri={m['max_uniform_run']}/{m['max_uniform_run_limit']}"
    )
    print(
        f"  klişe={m['cliche_hits']} ({m['cliche_per_1000']}/1000) "
        f"bağlaç_başı={m['connective_start_ratio']} MATTR={m['mattr']} "
        f"TTR={m['ttr']} hapax={m['hapax_ratio']}"
    )
    if m["cliche_list"]:
        print("  klişe listesi: " + ", ".join(f"{v}×{n}" for v, n in m["cliche_list"]))


def main() -> int:
    ap = argparse.ArgumentParser(
        description="İnsansılaştırma dokunulmazlık bekçisi + ritim ölçer (salt-okuma)"
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_inv = sub.add_parser("inventory", help="DOKUNULMAZ envanteri çıkar (Adım 0)")
    p_inv.add_argument("file")

    p_guard = sub.add_parser("guard", help="kaynak↔aday öz karşılaştırması (HARD kapı)")
    p_guard.add_argument("--source", required=True)
    p_guard.add_argument("--candidate", required=True)

    p_met = sub.add_parser("metrics", help="ritim/çeşitlilik ölçümü")
    p_met.add_argument("file")
    p_met.add_argument("--source", help="karşılaştırma için kaynak metin")

    p_all = sub.add_parser("all", help="guard + metrics")
    p_all.add_argument("--source", required=True)
    p_all.add_argument("--candidate", required=True)

    for p in (p_inv, p_guard, p_met, p_all):
        p.add_argument("--json", action="store_true", help="makine-okunur çıktı")

    args = ap.parse_args()

    if args.cmd == "inventory":
        bag = extract_inventory(read_text(args.file))
        if args.json:
            print(json.dumps({f"{c}|{v}": n for (c, v), n in bag.items()},
                             ensure_ascii=False, indent=2))
        else:
            print_inventory(bag)
        return 0

    if args.cmd == "metrics":
        m = compute_metrics(read_text(args.file))
        find = metric_findings(m)
        payload = {"candidate": m, "findings": find}
        if args.source:
            payload["source"] = compute_metrics(read_text(args.source))
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            if args.source:
                print_metrics(payload["source"], f"KAYNAK ({args.source})")
            print_metrics(m, f"ADAY ({args.file})")
            print("\nÜSLUP HEDEFİ:")
            for f in find or ["  hedefler karşılandı"]:
                print(f"  - {f}" if find else f)
        return 2 if find else 0

    src_txt, cnd_txt = read_text(args.source), read_text(args.candidate)
    res = compare(src_txt, cnd_txt)
    exit_code = 1 if res["hard"] else (2 if res["soft"] else 0)

    if args.cmd == "all":
        m_src, m_cnd = compute_metrics(src_txt), compute_metrics(cnd_txt)
        find = metric_findings(m_cnd)
        if args.json:
            print(json.dumps(
                {
                    "hard": res["hard"],
                    "soft": res["soft"],
                    "metrics_source": m_src,
                    "metrics_candidate": m_cnd,
                    "style_findings": find,
                    "exit": exit_code if exit_code else (2 if find else 0),
                },
                ensure_ascii=False, indent=2,
            ))
        else:
            print_compare(res)
            print_metrics(m_src, "KAYNAK")
            print_metrics(m_cnd, "ADAY")
            print("\nÜSLUP HEDEFİ:")
            if find:
                for f in find:
                    print(f"  - {f}")
            else:
                print("  hedefler karşılandı")
        if exit_code == 0 and find:
            exit_code = 2
        return exit_code

    if args.json:
        print(json.dumps({"hard": res["hard"], "soft": res["soft"], "exit": exit_code},
                         ensure_ascii=False, indent=2))
    else:
        print_compare(res)
    return exit_code


if __name__ == "__main__":
    try:
        _code = main()
    except BrokenPipeError:  # `| head` gibi kesilen borular sessiz geçilir
        os._exit(0)
    raise SystemExit(_code)
