#!/usr/bin/env python3
"""semantic_core — ham-vektör embedding beyni (spec: embedding-judge-genisletme §4.1).

Tez sürecinin deterministik semantik-benzerlik primitifi. galileo_bridge'in
`_embed`'ini (Azure OpenAI text-embedding-3-large, Roche Minerva azure-openai
gateway) sarmalar ve üstüne saf-cosine yardımcıları kurar:

  embed(texts)                -> list[list[float]]   (ham vektörler)
  cosine(a, b)                -> float
  dedup_matrix(items, thr)    -> yakın-duplikat çiftleri [(i,j,sim)]
  redundancy_pairs(paras,thr) -> tekrar eden paragraf çiftleri
  match_matrix(rowsA, rowsB)  -> çapraz cosine matrisi (tema↔yapı eşleme)

Tasarım ilkeleri (spec §4.1):
- Bağımlılıksız (yalnız stdlib + galileo_bridge). Torch/sentence-transformers YOK.
- Erişilemezse temiz `EmbeddingUnavailable` — asla çökmez, asla yanlış-HARD üretmez.
  Çağıran taraf degrade eder (string/anamnesis-sıralı), sessiz atlama yok.
- KVKK guard: yalnız manuskript/literatür stringi kabul; katılımcı/transkript/
  aile-düzeyi veri imzası (TC kimlik, ad-soyad kolonu) reddedilir (`KvkkViolation`).

CLI (smoke): `python3 scripts/eval/semantic_core.py` -> galileo_stats + kısa embed.
"""
from __future__ import annotations

import math
import os
import re
import sys

# galileo_bridge aynı dizinde; import edilebilir olması için dizini yola ekle.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import galileo_bridge as _gb  # noqa: E402

# EmbeddingUnavailable'ı yeniden dışa aç: çağıranlar tek yerden yakalar.
EmbeddingUnavailable = _gb.EmbeddingUnavailable

# Kalibre eşikler galileo_bridge'ten miras (tek kaynak; .env/galileo.local.md yönetir).
DEDUP_SIM_MIN = _gb._BIB_DEDUP_SIM_MIN          # near-dup referans
REDUNDANCY_SIM_MIN = _gb._CONTRADICTION_SIM_MIN  # bölüm/paragraf tekrarı (same-topic)

# --- KVKK tripwire: yüksek-özgüllüklü ham-veri imzaları (yanlış-pozitif riski düşük) ---
_TC_KIMLIK_RE = re.compile(r"(?<!\d)\d{11}(?!\d)")          # TC kimlik no
_AD_SOYAD_RE = re.compile(r"ad[ıi]?\s*[-_ ]?\s*soyad", re.IGNORECASE)  # repo PII regex hattı


class KvkkViolation(Exception):
    """Girişte ham/katılımcı veri imzası saptandı — gateway'e gönderilmez."""


def _kvkk_tripwire(texts) -> None:
    """Manuskript/literatür-dışı ham-veri imzası taşıyan girişi reddet (spec §4.1).
    Yalnız çok yüksek-özgüllüklü işaretler (TC kimlik 11-hane, ad-soyad kolonu);
    yayımlanmış manuskript metninde görülmez, bu yüzden meşru embedding'i engellemez."""
    for t in texts:
        s = t if isinstance(t, str) else str(t)
        if _TC_KIMLIK_RE.search(s):
            raise KvkkViolation("giriş TC-kimlik imzası taşıyor — gateway'e gönderilemez")
        if _AD_SOYAD_RE.search(s):
            raise KvkkViolation("giriş ad-soyad kolonu imzası taşıyor — gateway'e gönderilemez")


def embed(texts):
    """Metin listesini ham vektöre çevir. KVKK tripwire + galileo _embed.
    Erişilemezse EmbeddingUnavailable (çağıran degrade eder)."""
    texts = list(texts)
    if not texts:
        return []
    _kvkk_tripwire(texts)
    cfg = _gb._load_cfg()
    return _gb._embed(cfg, texts)


def cosine(a, b) -> float:
    """İki vektör arası kosinüs benzerliği (galileo_bridge._cos ile aynı)."""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def is_available() -> bool:
    """galileo embedding şu an canlı mı (ping)."""
    try:
        embed(["ping"])
        return True
    except EmbeddingUnavailable:
        return False


def _texts_of(items):
    """items: [{...}] veya [str]. (key, text) çiftleri döndür."""
    out = []
    for idx, it in enumerate(items):
        if isinstance(it, dict):
            key = it.get("key", idx)
            txt = it.get("text") or it.get("title") or ""
        else:
            key, txt = idx, str(it)
        out.append((key, txt))
    return out


def dedup_matrix(items, threshold: float | None = None):
    """Yakın-duplikat çiftleri: her item çifti için cosine >= threshold.
    items: [{key,title|text}] veya [str]. threshold: None -> DEDUP_SIM_MIN.
    Dönen: [{"a":keyA,"b":keyB,"sim":round}] (azalan sim). EmbeddingUnavailable propager."""
    thr = DEDUP_SIM_MIN if threshold is None else threshold
    pairs = _texts_of(items)
    keys = [k for k, _ in pairs]
    vecs = embed([t[:1000] for _, t in pairs])
    out = []
    for i in range(len(vecs)):
        for j in range(i + 1, len(vecs)):
            sim = cosine(vecs[i], vecs[j])
            if sim >= thr:
                out.append({"a": keys[i], "b": keys[j], "sim": round(sim, 3)})
    out.sort(key=lambda d: d["sim"], reverse=True)
    return out


def redundancy_pairs(paras, threshold: float | None = None, adjacent_only: bool = False):
    """Tekrar eden paragraf çiftleri: cosine >= threshold.
    adjacent_only=True -> yalnız komşu (i, i+1); aksi halde tüm çiftler.
    Dönen: [{"a":i,"b":j,"sim":round}] (azalan). EmbeddingUnavailable propager."""
    thr = REDUNDANCY_SIM_MIN if threshold is None else threshold
    paras = [p for p in paras]
    vecs = embed([p[:6000] for p in paras])
    out = []
    n = len(vecs)
    for i in range(n):
        js = [i + 1] if adjacent_only else range(i + 1, n)
        for j in js:
            if j >= n:
                continue
            sim = cosine(vecs[i], vecs[j])
            if sim >= thr:
                out.append({"a": i, "b": j, "sim": round(sim, 3)})
    out.sort(key=lambda d: d["sim"], reverse=True)
    return out


def match_matrix(rows_a, rows_b):
    """Çapraz cosine matrisi (tema↔yapı eşleme). rows_a/rows_b: [str] veya [{text|title}].
    Dönen: {"matrix": [[sim...]...], "best": [{"a":i,"b":argmax,"sim":round}...]}.
    EmbeddingUnavailable propager."""
    ta = [t for _, t in _texts_of(rows_a)]
    tb = [t for _, t in _texts_of(rows_b)]
    if not ta or not tb:
        return {"matrix": [], "best": []}
    va = embed([t[:6000] for t in ta])
    vb = embed([t[:6000] for t in tb])
    matrix, best = [], []
    for i, ai in enumerate(va):
        row = [round(cosine(ai, bj), 3) for bj in vb]
        matrix.append(row)
        j = max(range(len(row)), key=lambda k: row[k]) if row else -1
        best.append({"a": i, "b": j, "sim": row[j] if j >= 0 else None})
    return {"matrix": matrix, "best": best}


if __name__ == "__main__":
    import json
    st = _gb.t_galileo_stats()
    print("galileo embedding_ok=%s model=%s" % (
        st.get("embedding_ok"), st.get("embedding_model")))
    if st.get("embedding_ok"):
        demo = dedup_matrix([
            {"key": "a", "title": "Parental overprotection in type 1 diabetes"},
            {"key": "b", "title": "Overprotective parenting among children with T1DM"},
            {"key": "c", "title": "Glycemic control and HbA1c variability"},
        ], threshold=0.5)
        print(json.dumps({"dedup_demo": demo}, ensure_ascii=False))
    else:
        print("embedding erişilemez:", st.get("embedding_note"))
