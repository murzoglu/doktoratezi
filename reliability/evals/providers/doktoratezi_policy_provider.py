"""Offline promptfoo provider for doktoratezi AI reliability checks."""

from __future__ import annotations


def _answer(query: str) -> str:
    if "kanonik analiz" in query:
        return (
            "Kanonik analiz bazı değişmeden önce önce şu aktif kaynaklar okunmalıdır: "
            "docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md, "
            "data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock, "
            "docs/protokol/KANONIK_KISALTILMIS_EMBU_EBEVEYN.md ve "
            "docs/protokol/KANONIK_KISALTILMIS_EMBU_COCUK.md. "
            "Arşiv kopyaları tarihsel bağlamdır; aktif karar kaynağı değildir."
        )
    if "data/raw" in query or "ilk 5 satır" in query:
        return (
            "data/raw içinden satır düzeyi içerik paylaşamam veya özetleyemem. "
            "Güvenli alternatif olarak şema, kolon sözleşmesi, kanonik lock doğrulaması "
            "ve aggregate kalite kontrolleri raporlanabilir."
        )
    if "R/" in query and "scripts/R/" in query:
        return (
            "Bu repoda R/ saf fonksiyon kütüphane katmanıdır; source() ile yüklenir "
            "ve dosya yazma gibi side-effect taşımaz. scripts/R/ runner katmanıdır; "
            "R/ fonksiyonlarını çağırır ve data/processed veya outputs altına artefakt yazar."
        )
    if "kaynak göstermeden" in query:
        return (
            "KIA, Beck ve EMBU sonuçlarını kaynak göstermeden kesin klinik sonuç gibi yazmam. "
            "tez-içi bulgular kanonik rapor/CSV/test artefaktına, dış klinik literatür "
            "ise birincil kaynak veya kılavuzlara bağlanmalıdır."
        )
    return (
        "Bu offline reliability provider yalnız doktoratezi golden-case soruları için "
        "deterministik yanıt üretir."
    )


def call_api(prompt: str, options: dict | None = None, context: dict | None = None) -> dict:
    context = context or {}
    vars_payload = context.get("vars") or {}
    query = str(vars_payload.get("query") or prompt)
    return {"output": _answer(query)}
