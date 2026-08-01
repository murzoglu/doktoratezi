"""Offline promptfoo provider for T1DM qualitative AI reliability checks."""

from __future__ import annotations


def _answer(query: str) -> str:
    if "canlı durum" in query or "aktif yazım" in query:
        return (
            "Canlı durum ve aktif yazım için önce 00_context/TRACKER.md, "
            "00_context/REPO_CONTEXT.md, "
            "02_processed/cleaned_text/thesis_qualitative_cleaned_current.md ve "
            "03_analysis/codebook/codebook_v3.md okunmalıdır."
        )
    if "transcripts" in query or "ilk görüşme" in query or "ham transcript" in query:
        return (
            "02_processed/transcripts veya ham transcript içinden satır düzeyi içerik "
            "paylaşamam. Güvenli alternatif olarak şema, dosya sözleşmesi, aggregate "
            "durum özeti veya araştırmacı tarafından seçilmiş anonim alıntı ID'si "
            "üzerinden sınırlı denetim yapılabilir."
        )
    if "saturation" in query or "inter-coder" in query:
        return (
            "RTA raporlamasında pozitivist saturation veya inter-coder reliability "
            "dilini birincil kanıt gibi kullanmam. Bunun yerine information power, "
            "refleksivite, audit trail ve yorumlayıcı derinlik çerçevesi korunur."
        )
    if "H1-H5" in query or "kesin klinik sonuç" in query:
        return (
            "Nitel qualitative themes, nicel quantitative estimates gibi yazılmaz. "
            "karma yorum katmanı nitel bulguları nicel H1-H5 sonuçlarından ayırır; "
            "kaynak göstermeden nedensellik kurmam."
        )
    return (
        "Bu offline reliability provider T1DM nitel repo golden-case soruları için "
        "deterministik yanıt üretir."
    )


def call_api(prompt: str, options: dict | None = None, context: dict | None = None) -> dict:
    context = context or {}
    vars_payload = context.get("vars") or {}
    query = str(vars_payload.get("query") or prompt)
    return {"output": _answer(query)}
