# L4 — aijudge / galileo: Bağımsız Judge + Semantik Katman (NSCLC SR)

> Kapsam: yalnız akciğer kanseri tedavi **sistematik derleme** manüskriptleri;
> yalnız `NSCLC/` alt-ağacı. Ana playbook:
> [`../NSCLC_PLAYBOOK.md`](../NSCLC_PLAYBOOK.md) §0, §3.

Bu katman, sci-audit'in (deterministik HARD) **yanında** çalışan **bağımsız
LLM-judge + semantik-tutarlılık** ikinci-görüşüdür. **Doktrin gereği HARD kapı asla
buradan gelmez** (`hard=[]`); yalnız **SOFT-block** (eşik-tabanlı, insan-override'lı)
ve **advisory** (critical friend) üretir.

---

## 0. Üç-katman kapı (three-tier gate)

| Katman | Kaynak | Karar | SR'de |
|--------|--------|-------|-------|
| **HARD** | sci-audit (deterministik) | Teslim engeli | PRISMA madde eksiği, akış tutarsızlığı, kaynaksız havuzlanmış etki, TR `p` |
| **SOFT-block** | galileo eşikleri | İnsan-override'lı | Düşük groundedness/faithfulness; overclaim; HARKing |
| **advisory** | judge critical friend | Bilgilendirme | Sentez anlatısı, kanıt-güç uyumsuzluğu, cherry-pick sinyali |

---

## 1. SOFT-block eşikleri (SR kalibrasyonu)

Her sinyal `.mcp.json` `galileo-audit` sunucusundaki **gerçek bir tool'a** bağlıdır;
eşikler o tool'un skorlarına uygulanır.

| Sinyal | Gerçek tool | Eşik (başlangıç) | SR anlamı |
|--------|-------------|------------------|-----------|
| `groundedness_min` | `galileo_claim_source_match` | 0,60 | Her sentez cümlesi dahil çalışma/meta sonucuna bağlı mı |
| `faithfulness_min` | `galileo_claim_source_match` | 0,60 | Dahil çalışma çarpıtmadan aktarılıyor mu (RBŞ) |
| `contradiction_sim_min` | `galileo_consistency` | 0,82 | Sentez-içi çelişki (aynı havuzlanmış etki farklı yerde farklı) |
| `bib_dedup_sim_min` | `galileo_bib_dedup` | 0,96 | Near-dup: aynı çalışmanın çoklu yayınını yanlış birleştirmez |
| `overclaim_min` | `galileo_overclaim_judge` | 0,60 | Kanıt gücünü aşan sonuç dili |
| `harking_min` | `galileo_harking_judge` | 0,60 | Post-hoc alt-grup/sonucu önceden-planlıymış gibi sunma |
| `coherence_min` | `galileo_coherence` / `galileo_coherence_judge` | 0,60 | Giriş→yöntem→sentez→tartışma zinciri tutarlı mı |
| `citation_support_required` | `galileo_reference_prose` | true | Her atıf ilgili sentez cümlesini destekliyor mu |

**Toplu koşum:** tam-tez taraması `galileo_full_thesis_judge`; çok-sinyal batch
`galileo_eval_run`; skorlama istatistikleri `galileo_stats`.

---

## 1.1 Doktrin — SOFT asla HARD'a terfi etmez

galileo tool'ları yalnız **eşik-altı skorla SOFT-block** veya **advisory** üretir.
Bir galileo bulgusu ne kadar güçlü olursa olsun teslimi tek başına engelleyemez;
teslim engeli (HARD) yalnız `scripts/run_hard_gate.py` + sci-audit deterministik
eksenlerinden gelir (bkz. sci-audit referansı §0, §3 Adım 0).

## 2. SR-özel judge örüntüleri

### 2.1 Overclaim (aşırı-iddia)
- Havuzlanmış PFS yararını OS yararı gibi sunma.
- Yüksek heterojenite (yüksek I²) varken kesin havuzlanmış sonuç ilan etme.
- Düşük GRADE kesinliğine rağmen güçlü öneri dili.
- Az sayıda çalışma / geniş GA'yı gizleyip kesinlik ima etme.
- Tek RCT'lik "sentezi" meta-analiz kesinliğiyle sunma.

### 2.2 HARKing (post-hoc)
- Protokolde olmayan alt-grubu (histoloji × belirteç) önceden-planlı gibi.
- Birincil sonuç anlamsızken keşifsel sonuca odak kayması.
- Etkileşim testi anlamsızken alt-grup farkını vurgulama.

### 2.3 Cherry-pick / seçici sentez (RBŞ) — advisory
- Yalnız olumlu çalışmaları öne çıkarma; yüksek-RoB çalışmaların ağırlığını gizleme.
- Heterojenite kaynağını (popülasyon/etnisite/hat) belirtmeden havuzlama.
- Yayın yanlılığı sinyalini (funnel asimetri) atlama.

### 2.4 Kanıt-güç uyumsuzluğu — advisory
- Gözlemsel/gerçek-yaşam kanıtını RCT kesinliğiyle nedensel sunma.
- Preprint/konferans özetini tam-yayın kesinliğiyle sunma.

---

## 3. Semantik katman (ham-vektör, judge-dışı)

- **near-dup referans:** `bib-dup` — aynı NSCLC çalışmasının ilk + uzun-takip
  yayınlarını **distinct tutar**, yanlış birleştirmez (SR'de çalışma≠rapor kritik).
- **bölüm-tekrarı:** `redundancy` — Tartışma/Giriş aşırı tekrar.
- **coherence:** bitişik paragraf akışı cosine.

**HARD asla semantik/judge'dan gelmez;** `--strict` + cosine ≥ eşik yalnız SOFT.

---

## 4. Gizlilik / telif tripwire (zorunlu)

- **Ham/hasta-düzeyi veri yoktur** (SR); gateway'e yalnız manüskript + literatür +
  künye + özet-düzeyi çıkarım gider.
- Telifli tam metin gateway'e toptan gönderilmez (yalnız yapılandırılmış çıkarım).
- Credential/secret gönderimi tripwire ile reddedilir.

---

## 5. Judge koşum sırası (F7)

1. **HARD önce:** `scripts/run_hard_gate.py` + sci-audit temiz olmadan galileo
   koşulmaz.
2. `galileo_claim_source_match` (groundedness + faithfulness) +
   `galileo_reference_prose` (citation_support) → SOFT-block.
3. `galileo_overclaim_judge` + `galileo_harking_judge` + `galileo_coherence`
   → SOFT/advisory.
4. `galileo_bib_dedup` + `redundancy` → SOFT (`--strict`) / advisory.
5. (Opsiyonel) tam-tez: `galileo_full_thesis_judge`; batch: `galileo_eval_run`.
6. Çıktı: judge JSON + `08_reports/<konu>_galileo.md`.
7. SOFT bulgular: düzelt **veya** insan-override gerekçesiyle sertifikaya işle.

---

## 6. Kabul kriteri (F8 ile birlikte)

- HARD (sci-audit): `error`/`blocker` **yok**.
- SOFT (galileo): eşik-altı bulgular **düzeltilmiş veya gerekçeli override**.
- advisory: değerlendirilmiş.
- Harici gateway/MCP kullanıldıysa **AI-use log satırı** yazılmış
  (`09_ai_use_log/ai_use_log.csv`).
