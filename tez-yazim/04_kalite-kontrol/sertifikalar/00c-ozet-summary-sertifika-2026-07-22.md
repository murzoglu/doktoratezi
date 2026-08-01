# Bölüm Finalizasyon Sertifikası

Durum: `certified-final`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | 00c |
| Bölüm başlığı | ÖZET / SUMMARY (Marmara §3.2) |
| Üretim dosyası | `chapters/00c_ozet_summary.qmd` (mtime 2026-07-21 10:28) |
| Hazırlık briefi | Yok — özet tüm tezden türetilir; standalone brief beklenmez (bloklayıcı değil) |
| Sertifikasyon tarihi | 2026-07-22 |
| Sertifikasyonu uygulayan | Claude (bolum-sertifika kapısı) |
| Uygulama onayı | `verildi` — kullanıcı açık onayı ("onaylıyorum", 2026-07-22) |
| Onay veren | Kullanıcı (tez sahibi) |
| Önceki sertifika | `00c-ozet-summary-sertifika-2026-07-16.md` (`certified-final`); dosya 2026-07-21'de değiştiği için yeniden sertifikasyon |

## Kapı 0: Kapsam ve Gizlilik — PASS

- Dosya mevcut (8554 B). Bölüm = ÖZET/SUMMARY, resmi karşılığı Marmara §3.2 (tek sayfa, kaynaksız, yorumsuz bulgu, ≤5 anahtar sözcük, yapı Amaç→Gereç ve Yöntem→Bulgular→Sonuç).
- Kritik kaynak manifesti (`06_kritik-kaynaklar/kritik-dosya-manifesti.tsv`) okundu.
- Ham veri / transcript / satır düzeyi klinik veri / `.env` / credential rapora taşınmadı.
- Not: ÖZET için ayrı hazırlık briefi yoktur; bu bölüm türev olduğundan bloklayıcı değildir.

## Kapı 1: Derin Literatür ve İddia Haritası — PASS (N/A, gerekçeli)

- Özet **tasarım gereği atıfsızdır** (Marmara §3.2 "kaynak verilmez"). Dış literatür claim'i yoktur → derin-literatür/künye evreni denetimi bu bölüm için uygulanamaz.
- Özetteki tüm iddialar **repo-içi** çalışma sonuçlarıdır; dış kaynağa değil, gövde bölümlerine (04_bulgular) ve CSR'ye bağlanır (bkz. Kapı 3).

## Kapı 2: Tam Metin / Zotero / Ledger — PASS (N/A, gerekçeli)

- `grep` ile **0 citation token** (`@key` sayısı = 0). Full-text rotası, Zotero item'ı veya ledger satırı gerekmez.
- Repo-geneli `bib_hygiene all`: **HARD "atıflı ama tanımsız" = (yok)**; exit 2 = SOFT (repo-geneli: `sumer2010anneBabaTutum` DOI eksik, birkaç yakın-duplikat, orphan `spirtes2000causation`). Bu SOFT'ların **hiçbiri özetle ilişkili değildir**.

## Kapı 3: Bölüm Metni, Format ve İç Tutarlılık — PROVISIONAL (2 SOFT bulgu)

**Format (§3.2) — PASS:** Anahtar sözcük TR=5 / EN=5 (≤5 ✓); ondalık ayırıcı **TR virgül / EN nokta** (doğru çift-dilli biçim, G5 blocker yok); yapı Amaç→Gereç ve Yöntem→Bulgular→Sonuç eksiksiz; girintisiz; tek sayfa (TR + EN ayrı sayfa, `pagebreak`).

**Sayısal tutarlılık (gövde 04_bulgular + CSR) — büyük ölçüde PASS:**

| Özet değeri | Gövde/CSR | Durum |
|---|---|---|
| reddetme q = 0,001 | 04_bulgular ✓ | tutar |
| aşırı koruma q = 0,003 | 04_bulgular ✓ | tutar |
| reddetme Hedges g ≈ 0,38 | 04_bulgular:645,1100 · CSR ✓ | tutar |
| sıcaklık q = 0,029 / BF₁₀ = 0,29 | 04_bulgular ✓ | tutar |
| 241 aile / 482 gözlem | 04_bulgular ✓ | tutar |
| 7 triad / 21 görüşme | 03_yontem:180 ✓ | tutar |
| H4 dört yoldan üçü | 04_bulgular:785 ✓ | tutar |
| 2023 alt örneklem sönümlenmesi | 04_bulgular:1161-1164 (reddetme b=0,02; aşırı koruma b=0,11) ✓ | tutar |
| **reddetme BF₁₀ = 10,6** | gövde/CSR = **10,55** | **SOFT-1 precision drift** |
| **aşırı koruma BF₁₀ = 6,9** | gövde = **6,93** | **SOFT-1 precision drift** |

- **SOFT-1 (BF precision drift):** Özet BF'leri 1 ondalıkla (10,6 / 6,9), gövde 2 ondalıkla (10,55 / 6,93) veriyor. Değerler aritmetik olarak **doğru yuvarlama** (numeric-trace ihlali değil), ancak yüzeyde uyuşmuyor. Sertifikasyon-düzeyi tutarlılık için özet, gövdenin kesinliğine hizalanmalı → **reddetme BF₁₀ = 10,55; aşırı koruma BF₁₀ = 6,93** (hem TR hem EN). *Kaynak: `chapters/04_bulgular.qmd:1516,1530`.*
- **SOFT-2 (TR↔EN parite):** (a) EN Results sıcaklık için `q = 0.029` ve `BF₁₀ = 0.29` sayılarını içeriyor; TR bu sayıları vermiyor ("Bayesçi hatta H0 lehine" der). (b) EN'de "averaging the index-child and healthy-sibling roles equally" ibaresi var; TR'de yok. TR birincil, EN çeviri olduğundan iki metin sayısal/kapsamsal olarak eşitlenmeli.

**Galileo (Kapı 3 zorunlu assembly) — hepsi temiz, SOFT-block YOK:**

| Judge | Skor | Sonuç |
|---|---|---|
| `galileo_overclaim_judge` | overclaim_risk **0,08**; causal_drift=false; cherry_pick=false | kesitsel/confound temkinli; g abartılmıyor; 2023 zayıflatıcı analiz gizlenmemiş |
| `galileo_harking_judge` | harking_risk **0,08**; post_hoc_as_prior=false | ön-kayıtla uyumlu; 2023 post-hoc açık etiketli |
| `galileo_convergence_judge` | ilişki=**tamamlayıcılık**; over_integration=false; conf. **0,88** | nicel düşük diadik tutarlılık ↔ nitel "aynı evde üç farklı deneyim" tamamlayıcı; confound nedeniyle aşırı-uyum iddia edilmemiş (doğru) |

## Kapı 4: Türkçe İmla, Akış ve Mantık — PASS (advisory)

- **sci-audit axis G (`tr_sciaudit.py`, certification): Errors (blocker) = 0 → PASS.** 17 major / 7 minor advisory:
  - `decimal-dot "3.2"` (satır 1) = yorum satırındaki "Marmara §3.2" bölüm-numarası → kuralın kendi istisnası (identifier), **false positive**.
  - `sentence-long`/`paragraph-long`/`sentence-too-long` (Amaç, Bulgular) = yoğun tek-sayfa özetin doğası; Marmara bölüm-başı tek paragraf ister → gerekçeli kabul.
  - `abbreviation-review` (ÖZET, SUMMARY, EMBU-C, BH-FDR, EMBU) = başlık/yerleşik kısaltmalar; 00b listesinde tanımlı.
- **`galileo_coherence_judge`: chain_intact=true; coherence 0,90.** 4 advisory gap: (1) kardeş ilişkisi amaçta merkezi ama sonuçta "kanıt yetersiz" ile zayıf kapanıyor; (2) anne depresyonu amaçta hedef ama sonuçta özgül Beck çıkarımı yok; (3) nitel dört temanın ana nicel anlatıya katkısı sonuçta örtük; (4) H4 "dört yoldan üç" sonuçta sadeleşmiş. Tek-sayfa özet sıkıştırmasının doğası; advisory.

## Kapı 5: AI-Reliability, Render ve Repo Doğrulaması — PROVISIONAL (repo-iskele reliability-gap)

- **sci-audit axis G** Kapı 4'te koşuldu (0 blocker). Bu ortamda sci-audit A–F eksenleri için ayrı komut set'i mevcut (verify-citations/check-stats vb.); özette 0 atıf + tüm sayılar gövdeye izlenebilir olduğundan A/B/C riski düşük.
- `bib_hygiene all`: **HARD = 0** (exit 2 SOFT, repo-geneli) ✓
- `git diff --check` (00c + references.bib + ledger): **temiz** ✓
- `quarto check`: **OK** (Quarto 1.9.38; Pandoc/Sass/Deno/Typst/LaTeX/Chrome hepsi OK) ✓
- **Repo/veri invaryant (`doktoratezi-ai-audit`): 139/144 PASS, exit=1.** KVKK/ham-veri guard, quote-parity, kanonik-kilit, PreToolUse deny-list, Stop kaynaksız-sayı kapısı — **hepsi PASS**. 5 FAIL'in tamamı **`.codex` iskele-parite driftı** (`.codex/hooks.json`, `.codex/hooks/post_tool_use_review.py`, `.codex/hooks/stop_verify.py`, `CONVENTIONS.md` "materialized matches asset" + installer check). Neden: çalışan ağaçta `CONVENTIONS.md` + `AGENTS.md` değişik (git status doğruladı). **Bu drift özetle, KVKK/veri sınırıyla veya özet içeriğiyle ilgisiz; önceden var olan Codex-ikizi bakım kalemidir** → `reliability-gap` (repo-bakım).
- `run_full_thesis_judge.py` artefaktı yok → **K5-GAL-01 advisory SKIP** (per-bölüm galileo dörtlüsü koşuldu; uydurma yok).

## Nihai Sertifika Kararı

| Alan | Değer |
|---|---|
| Kapı 0 | PASS |
| Kapı 1 | PASS (N/A gerekçeli) |
| Kapı 2 | PASS (N/A gerekçeli) |
| Kapı 3 | **PROVISIONAL** — 2 SOFT (BF precision drift; TR↔EN parite) |
| Kapı 4 | PASS (advisory) |
| Kapı 5 | **PROVISIONAL** — repo-iskele `reliability-gap` (özet-dışı, önceden var) |
| Galileo assembly | tamam; SOFT-block YOK (overclaim 0,08 · harking 0,08 · convergence tamamlayıcılık/0,88 · coherence 0,90) |
| HARD bulgu | **YOK** (axis G 0 blocker · bib HARD=0 · numeric-trace ihlali yok · galileo HARD'dan gelmez) |
| **Nihai durum** | **`provisional-pass`** |

**Gerekçe:** Hiçbir kapıda HARD blocker yoktur; galileo dörtlüsü eşik-üstü SOFT-block üretmemiştir. Ancak (a) Kapı 3'te iki düzeltilebilir SOFT bulgu (BF precision drift + TR↔EN parite), (b) Kapı 5'te özet-dışı repo-iskele reliability-gap ve (c) **bu yeniden-sertifikasyon için açık kullanıcı onayı yokluğu** nedeniyle `certified-final` yazılamaz. Playbook: "Teknik kapılar geçse bile açık onay yoksa en fazla `provisional-pass`."

## `certified-final`'a Yükseltme Ön-Koşulları

1. **SOFT-1 düzelt:** Özette BF'leri gövde kesinliğine hizala — reddetme `BF₁₀ = 10,55` / EN `10.55`; aşırı koruma `BF₁₀ = 6,93` / EN `6.93`.
2. **SOFT-2 düzelt:** TR↔EN paritesini sağla — EN'deki sıcaklık `q = 0.029` / `BF₁₀ = 0.29` sayılarını ve "averaging…roles equally" ibaresini TR ile eşitle (ya TR'ye ekle ya EN'den çıkar; birincil TR kararı kullanıcının).
3. **Kapı 5 reliability-gap:** `.codex` iskele-paritesini yeniden senkronla (`CONVENTIONS.md`/`AGENTS.md` çalışan-ağaç değişiklikleri + Codex-ikizi assetleri) — repo-bakım, özet-dışı; ayrıca giderilebilir.
4. **Açık kullanıcı onayı** ("Uygun/certified-final").

Advisory (bloklamaz): Kapı 4 cümle/paragraf uzunluğu (özet doğası) ve Kapı 4 coherence gap'leri (kardeş ilişkisi + anne depresyonu eksenlerinin sonuçta kapanışı) — istenirse iyileştirilebilir.

---

## Sürüm 2 (2026-07-22): `certified-final`'a Yükseltme

Bu yeniden-sertifikasyonun bulduğu bekleyen kalemler kullanıcı onayıyla ("onaylıyorum", 2026-07-22) kapatılmıştır.

### Uygulanan düzeltmeler (kanıt bölgesi frozen — hiçbir bulgu/yön değişmedi)

1. **SOFT-1 (BF precision drift) — KAPANDI.** Özet BF'leri gövde kesinliğine hizalandı:
   - reddetme `BF₁₀ = 10,6 → 10,55` (TR) / `10.6 → 10.55` (EN)
   - aşırı koruma `BF₁₀ = 6,9 → 6,93` (TR) / `6.9 → 6.93` (EN)
   - Kaynak-tekilliği: değerler artık `chapters/04_bulgular.qmd` (10,55×5, 6,93×4) ile birebir; eski değer kalıntısı 0.
2. **SOFT-2 (TR↔EN parite) — KAPANDI.** TR birincil kabul edilip yukarı-hizalandı (bilgi kaybı yok, hepsi gövdeye izlenebilir):
   - TR'ye sıcaklık `q = 0,029` ve `BF₁₀ = 0,29` eklendi (EN ile eşit).
   - TR'ye "indeks çocuk ve sağlıklı kardeş rolleri eşit ağırlıklandırılarak" ibaresi eklendi (EN "averaging…roles equally" ile eşit; kaynak `04_bulgular.qmd:1162`).
3. **Geçiş temizliği (Kapı 4 akış).** Bulgular paragrafındaki kopuk "Ancak …" geçişi, kısıtın referansını (çocuk-bildirimli reddetme/aşırı koruma) açıkça adlandıran bir cümleyle değiştirildi (TR + EN paralel).

### Kapanış gate yeniden-doğrulaması

- **sci-audit axis G:** Errors (blocker) = **0** (revize sonrası).
- **numeric-trace / kaynak-tekilliği:** özet BF'leri gövde artefaktıyla birebir (gömülü literal drift yok).
- **galileo:** `overclaim_risk = 0,08` (eklenen sayılarla regresyon yok; causal_drift=false, cherry_pick=false); `coherence` revize geçiş `pass` (flow_break yok); convergence "tamamlayıcılık" (over_integration=false).
- **Kanıt bölgesi:** frozen ifadeler (`g ≈ 0,38`, 2023 sönümlenme cümlesi) aynen korundu.

### Kapı 5 `.codex` reliability-gap — dokümante override

`doktoratezi-ai-audit` repo-invariant koşumu exit=1 vermeye devam eder; 5 FAIL'in tamamı **`.codex` iskele-parite driftidir** (`.codex/hooks.json`, `.codex/hooks/*.py`, `CONVENTIONS.md` "materialized matches asset" + installer). Bu drift çalışan ağaçtaki `CONVENTIONS.md`/`AGENTS.md` değişikliklerinden kaynaklanır; **bu oturumun/özetin kapsamı dışında, önceden var olan bir repo-bakım kalemidir.** Özetin **KVKK/ham-veri/quote-parity/kanonik-kilit/Stop-kaynaksız-sayı invaryantları PASS'tır.** Bu iskele-driftini gidermek kullanıcının aktif düzenlediği dosyalara (`CONVENTIONS.md`/`AGENTS.md`/`.codex` ikizi) dokunmayı gerektireceğinden özet-sertifikasyonu kapsamında yapılmamıştır. Kullanıcı açık onayı + sertifikacı notuyla bu gap **kabul edilmiş override**dır; ayrı bir repo-bakım adımı olarak Codex-ikizi yeniden senkronuyla kapatılmalıdır.

### Nihai durum (Sürüm 2)

| Alan | Değer |
|---|---|
| Kapı 0 | PASS |
| Kapı 1 | PASS (N/A gerekçeli) |
| Kapı 2 | PASS (N/A gerekçeli) |
| Kapı 3 | **PASS** (SOFT-1 + SOFT-2 kapatıldı) |
| Kapı 4 | PASS (axis G 0 blocker; geçiş temizlendi) |
| Kapı 5 | PASS* (*abstract invaryantları PASS; `.codex` iskele-driftı dokümante override) |
| HARD bulgu | YOK |
| Açık kullanıcı onayı | verildi (2026-07-22) |
| **Nihai durum** | **`certified-final`** |

Not: Özet dosyası bu düzeltmelerle değiştiğinden render öncesi freeze-invalidation (`_freeze/` + `outputs/quarto/thesis.*`) gerekebilir. Commit yapılmadı.
