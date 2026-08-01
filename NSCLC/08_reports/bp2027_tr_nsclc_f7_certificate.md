# F7 Formal Denetim Sertifikası — BP2027 TR NSCLC değerlendirme paketi

> **Kapsam.** problem.md (BP27/BP2027 atezolizumab TR) değerlendirmesinin çıktı paketi: baz-defteri
> [`bp2027_tr_nsclc_baz_veri_varsayim_defteri.md`](bp2027_tr_nsclc_baz_veri_varsayim_defteri.md),
> tam-metin dossier [`bp27_atezolizumab_tr_fulltext_dossier.md`](bp27_atezolizumab_tr_fulltext_dossier.md),
> zenginleştirme [`bp27_atezolizumab_tr_science_skills_enrichment.md`](bp27_atezolizumab_tr_science_skills_enrichment.md),
> sentez [`../06_synthesis/bp27_atezolizumab_tr_synthesis.md`](../06_synthesis/bp27_atezolizumab_tr_synthesis.md).
>
> **Doktrin (invaryant):** HARD = deterministik (sci-audit/script), teslim engeli, **asla LLM-judge'dan gelmez**;
> SOFT-block = galileo/LLM eşikleri, insan-override'lı; advisory = bilgilendirici. Tarih: 2026-07-27.
> HARD: `scripts/*` (self-test 21/21 OK). LLM katmanı: Workflow `wykmnr4w2` (galileo-audit canlı: judge_ok+embedding_ok).

## 1. HARD — deterministik kapı

| Denetçi | Girdi | Sonuç |
|---|---|---|
| extraction_direction_check | `04_extraction/…extraction.csv` | ✅ temiz (0) |
| context_source_guard (kanıt≠bağlam) | extraction.csv | ✅ temiz (0) |
| turkish_p_check (ondalık/imla) | 3 belge | ✅ temiz (0) — düzeltme sonrası tekrar doğrulandı |
| prisma_flow_check | — | SKIP (narratif-derin-lit; formal PRISMA taraması yapılmadı — no-fabrication) |
| source_singularity_check | baz-defteri ↔ tek extraction.csv | **N/A-kapsam** — bu denetçi *F8 manuskript ↔ tek extraction+meta* içindir; 08_reports **çok-kaynaklı sentez**tir (GLOBOCAN API, EXPRESS DOI, SUT RG 32952, §I) ve her sayı **satır-içi kaynak-bağlı** (DOI/RG/corpus). İzlenebilirlik RBŞ ile inline sağlanır; PRISMA-özgü tek-CSV kaidesi bu moda uygulanmaz. |
| test_hard_gate.py | — | ✅ 21/21 OK |

**HARD sonucu: PASS** (uygulanan tüm deterministik kaideler temiz; PRISMA-özgü ikisi kapsam-dışı, dürüstçe işaretli).

## 2. LLM katmanı — sci-audit eksenleri + galileo SOFT (Workflow `wykmnr4w2`)

| Eksen | Verdict | Özet |
|---|---|---|
| **A — Atıf gerçekliği** | ✅ **PASS** | 15/15 yük-taşıyan kimlik (11 DOI + 3 NCT + RG 32952) **gerçek + doğru atıflı** (OpenAlex/CT.gov/Resmî Gazete API). Uydurma/yanlış-atıf yok. 1 advisory: TOG Alan (`10.3390/medicina61071160`) çift claim-tipi kullanımı → B eksenine. |
| **B/D — Claim grounding + overclaim** | ⚠️ SOFT (0 blocker) | Groundedness yüksek (galileo_judge 0,78–0,84; GLOBOCAN düzeltmesi 0,806 en yüksek). SOFT: PD-L1 "TR≈global" **payda-uyuşmazlığı** (overclaim 0,72, causal_drift+cherry_pick). |
| **C — Aritmetik tutarlılık** | ⚠️ SOFT (0 blocker) | Tüm türev sayılar **yeniden-hesapla uyuşuyor** (sürücü-neg 71,7; cinsiyet 80,5/19,5; Evre III 6.565–8.719; PD-L1 27,5/58,7; 1L IO 11,5; pazar-payı 91,2/39,9/50/24,5/12,3; GLOBOCAN 37,88=ASR). SOFT: §5'te hatalı prevalans 49.303 propagasyonu. |
| **G — Türkçe + coherence** | ✅ **PASS** | galileo_coherence PASS (0,506; flow-break yok, tekrar yok). Ondalık virgül tekdüze; tier [E]/[C]/[L] tam + **[C]/[L]→[E] sızıntısı yok**; payda disiplini örnek; nedensel aşırılık yok. |

## 3. Uygulanan düzeltmeler (SOFT → çözüldü)

| Bulgu (eksen) | Düzeltme | Dosya |
|---|---|---|
| PD-L1 "TR≈global" payda-uyuşmazlığı (B/D) | Payda-eşleşmeli hale getirildi: TR all-comer 22C3 %27,5 vs **global all-comer 22C3 %22 (EXPRESS)** → TR üst uçta; global EGFR-WT %27 ayrı-payda çapa (TR-özgü EGFR-WT yok, karıştırılmaz) | baz-defteri §2/§I; enrichment §I.4; synthesis Eksen 6 |
| Hatalı prevalans 49.303 (C) | GLOBOCAN 2022 **54.335** ile değiştirildi (§1 düzeltmesiyle tutarlı) | baz-defteri §5 |
| Kapital "P=" (G) | Küçük "p=" normalize | enrichment §I.3 |
| 5-yıl sağkalım baz "<%15" vs üst %19,4 (C-advisory) | "çoğu kayıtta <%15" | baz-defteri §1 |
| ESTIMATE 1L partisyon %104,7 (C-advisory) | F7-C notu eklendi (Table 2 transkripsiyon artefaktı; yük-taşıyan %11,5 etkilenmez) | enrichment §G.1 |

**Doğrulama:** düzeltme sonrası turkish_p temiz (3/3); kapital P kalmadı; hatalı 49.303 baz-defteride yok.

## 4. Kalan advisory (bilgilendirici — teslim engeli değil)

- **TOG Alan çift-kullanım (A→B):** `10.3390/medicina61071160` hem tanı-evre dağılımı (§1) hem 2L nivolumab PFS (§3) için;
  gerçek+doğru-atıflı ama evre figürlerinin bu DOI'nin kohort-baseline'ından mı geldiği tam-metinle teyit edilmeli.
  (Evre için Cangir ulusal çapası da var; I/II zaten "düşük güven".)
- **~3,15 ay [L] priörü:** OAK 3,4 / TAIL 3,2'nin ortalaması değil; tilde-işaretli ve [L] "ödünç/değiştirilecek" sütununda
  ([E] etki-sayısı olarak sunulmuyor) → advisory; ~3,3'e yuvarlama veya provenance dipnotu önerilir.
- **"%35 küçümser" türev nicel:** hesap zinciri (27,5−17,8)/27,5 ≈ %35 açıkça yazılabilir.
- **Synthesis §0 "kozmetik" çerçevesi vs D3 "Yüksek" düzeltme:** hafif iç-gerilim; §0 D3'ü istisna tutabilir (çerçeveleme).

## 5. Genel hüküm

> **HARD PASS + LLM 0-blocker; SOFT bulgular çözüldü; advisory dokümante.** Değerlendirme paketi bütünlük
> (atıf-gerçekliği, claim-grounding, aritmetik, Türkçe/coherence) açısından **provisional-pass**tır. Sayısal
> çekirdek temiz; kanıt≠bağlam ve RBŞ payda-disiplini korunmuş; en yüksek-riskli iddialar (atezo 1L+2L
> geri-ödeme, PD-L1 TR-vs-global, GLOBOCAN düzeltmesi) primer/L2 kaynakla temellendirilmiş ve galileo-doğrulanmıştır.
>
> **certified-final yalnız açık kullanıcı onayıyla** verilir (bölüm-sertifika doktrini). Kalıcı kanonik doğrulama
> için önerilen tek adım: RG 32952 taranmış PDF'inin OCR-çekilmiş regülatif değerlerinin (c)3 / c)2 / retail fiyat)
> ham nüsha ile bir kez daha göz-teyidi (belge bunu zaten "kanonik nüsha RG 32952 esastır" ile işaretliyor).

*Denetim izleri: HARD `scripts/*` + Workflow `wykmnr4w2` (galileo-audit). Tüm bulgular kaynak-bağlı; uydurma yok.*
