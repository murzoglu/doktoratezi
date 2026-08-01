# TARTIŞMA ve SONUÇ — Derin-Literatür Yeniden Yazımı Uygulama Planı

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `chapters/05_tartisma_ve_sonuc.qmd` bölümünü, tüm bulguları (H1–H5 + [KEŞFİSEL] + nitel 4 tema + karma) en geniş tam-metin literatürle bilimsel derinlikte tartışan, akıcı (alt başlıksız) Marmara-uyumlu bir bölüm olarak yeniden yazmak.

**Architecture:** 8 bulgu-kümesi paralel literatür fan-out'u (D0–D6; minerva-openathens-annas + anamnesis) → kalıcı kanıt matrisi (`tartisma-kanit-matrisi.tsv`) → çapraz-uzlaştırma → akıcı Marmara taslağı (M1–M11, aday-atıflı) → toplu referans kapısı + sci-audit + Kapı 0–5. Kanıt bilgi-verici düzlemine göre örgütlenir (çocuk→anne→depresyon→kardeş); özgün değer "informant×boyut×deneyim ayrışma haritalaması"dır.

**Tech Stack:** Quarto (`.qmd`), R/targets (yalnız okuma — sayı kaynağı CSR + `apa_t*.csv`), Evidentia MCP connector'ları (pubmed-epmc, openalex, semantic-scholar, anamnesis, evidentia-kb, annas-reader, openathens, minerva-evidence), `scripts/util/bib_hygiene.py`, `zotero-refs` MCP, sci-audit plugin.

**Spec:** `docs/superpowers/specs/2026-07-13-tartisma-sonuc-derin-lit-design.md`

## Global Constraints

Her görevin gereksinimleri bu bölümü örtük içerir. Değerler spec + Marmara talimatnamesinden verbatim:

- **Alt başlık YOK** (Marmara §3.7); akış paragraf omurgası + geçiş cümleleri.
- **Bulgu/istatistik tekrarı YOK** — tablo/şekle atıf yeterli; test sonucu yeniden yazılmaz. Yorumda gereken tek sayı, çerçeveleme için minimal (ör. "0,16 SD küçük etki") olabilir; tam istatistik blok tekrarı yasak.
- **Nedensellik dili YOK** — kesitsel + olgu-kontrol; yalnız "ilişkili / öngörüyor / bağlı"; "neden olur / yol açar" yazılmaz.
- **[KEŞFİSEL] disiplini** — keşfisel/post-hoc bulgu "literatürle tutarlı / hipotez-üretici" çerçevelenir; asla "doğrulandı / kanıtlandı".
- **Kanıt türü ayrımı** — nitel tema ≠ nicel etki kanıtı; nicel sonuç ≠ nitel mekanizma kanıtı.
- **Sayı biçimi** — ondalık virgül + baştan sıfır; `p` 3 basamak (`p=0,038` / `p<0,001`); ortalama/yüzde 1 basamak; test istatistiği/oran 2 basamak.
- **Dil** — Türkçe edilgen 3. tekil; metin-içi `[@key]` (2 yazar "ve"; 3+ "ilk-yazar ve ark."; çoklu `;`). Elle biçimli kaynakça string üretme — CSL render eder.
- **KVKK** — connector'lara YALNIZ literatür terimleri; katılımcı/ham/aile-düzeyi/transkript verisi asla. Nitel kanıt yalnız `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd`.
- **Minerva mod kuralı** — TR sorgu → `mode:semantic` ZORUNLU; EN sorgu → `hybrid`/HyDE.
- **Tam-metin sırası** — `minerva_*`/`rominedb` → openathens (`oa_fetch_fulltext`) → `annas-reader` (annas kurumsal banttan SONRA); hepsi `anamnesis.ingest_document`. Hedefli çıkarım; uzun verbatim / toptan çoğaltma YOK.
- **Aday atıf** — kapı kapanana dek her yeni atıf `<!-- cand -->` işaretli.
- **Kaynak ankrajı** — `<!-- kaynak: dosya#ankraj -->` yorumları korunur (izlenebilirlik).
- **Sayı kaynağı** — nicel değerler yalnız `docs/CLINICAL-STUDY-REPORT-FINAL.*` + `outputs/tables/apa_t*.csv`; satır-düzeyi veri açılmaz.

---

## Faz A — Literatür Fan-out (Görev 1–8, paralel) + Uzlaştırma (Görev 9)

> **Yürütme notu:** Görev 1–8 birbirinden bağımsızdır → Workflow fan-out veya paralel alt-ajanlarla koşulur (ultracode). Her görev **dosyaya yazmaz**; ana pencereye/koordinatöre **kanıt matrisi satırlarını** (aşağıdaki şema) döndürür. Konsolide TSV'yi yalnız Görev 9 yazar (paralel-yazma çakışması önlenir).

**Kanıt matrisi satır şeması** (Görev 1–8 ortak çıktı sözleşmesi; TSV kolonları):
```
kume  claim  source_ids  bib_key  bulgu_ankraj  population_fit  measurement_fit  fulltext_locator  iliski  confidence
```
- `kume`: C1…C8
- `claim`: TR, tek cümle, tartışmada kullanılacak dış-literatür iddiası
- `source_ids`: `DOI:…` / `PMID:…` / `OpenAlex:W…` (en az bir çözümlenebilir kimlik)
- `bib_key`: `references.bib` @key (varsa) veya `YENI:<önerilen-key>`
- `bulgu_ankraj`: `CSR#<anchor>` veya `apa_tXX` veya `niteliksel...#tema-N`
- `population_fit` / `measurement_fit`: `direct|partial|indirect` (+ kısa transfer notu)
- `fulltext_locator`: `<route>:<sayfa/tablo>` (ör. `openathens:Table2`) veya `abstract-only`
- `iliski`: `benzer|farkli|bosluk-doldurur`
- `confidence`: `high|moderate|low`

**Her Faz-A görevinin ortak adım iskeleti** (D0–D6, `literatur-kanit-evidentia.md` §0.3):
1. **D0 kapsam:** PICO facet'lerini yaz (popülasyon / yapı / sonuç / yöntem / coğrafya).
2. **D1 geniş tarama:** `pubmed_search_articles` + `openalex_search_entities` + `semantic-scholar` (+ EPMC `AFF:"Turkey"` varyantı).
3. **D2 semantik genişletme:** `minerva_literature_search` (EN sorgu `hybrid`; TR sorgu `mode:semantic`), OpenAlex citation graph (`openalex_get_citation_graph`), `kb_search`.
4. **D4 tam-metin (kritik endpoint için):** `minerva_literature_fulltext_by_doi`/`minerva_rominedb_*` → `oa_fetch_fulltext` → `annas-reader`; her biri `anamnesis.ingest_document`. Sonra `anamnesis.hybrid_query` çok-sorgulu.
5. **D5 çapraz-doğrulama:** kritik iddiada ≥2 bağımsız/otoriter kaynak (G-XVAL).
6. **Çıktı:** kanıt matrisi satırları (yukarıdaki şema) + kısa `gap_log` (bulunamayan/erişilemeyen).
7. **Doğrulama:** her satırın `source_ids` en az bir çözümlenebilir kimlik taşır (G-BIB); kritik `claim`ler ≥2 kaynaklı (G-XVAL); KVKK — sorgularda yalnız literatür terimi.

---

### Task 1: C1 — H1 çocuk algısı / reddetme literatürü

**Files:**
- Return-only (dosya yok): kanıt matrisi satırları (kume=C1)

**Interfaces:**
- Consumes: `chapters/04_bulgular.qmd` §4.3.1 (H1: β=0,16 SD; BF₁₀=8,12), `docs/CLINICAL-STUDY-REPORT-FINAL.*#h1-karar`
- Produces: C1 kanıt matrisi satırları (şema yukarıda)

- [ ] **Step 1: D0 facet'leri yaz** — popülasyon: `child/adolescent type 1 diabetes`; yapı: `perceived parental rejection`, `parental acceptance-rejection`, `EMBU-C child report`; sonuç: `child adjustment/internalizing`; yöntem: `meta-analysis`, `informant discrepancy`; coğrafya: `Turkey`.
- [ ] **Step 2: D1–D2 tarama** — sorgu varyantları: `type 1 diabetes child perceived parenting rejection`, `chronic illness parental acceptance rejection child report`, `Pinquart chronic physical illness parenting meta-analysis`, `parent child informant discrepancy internalizing`. Minerva TR varyantı `mode:semantic`.
- [ ] **Step 3: D4 tam-metin** — Pinquart kronik-hastalık meta-analizi + Rohner PARTheory + en az bir çocuk↔ebeveyn ayrışma kaynağının etki büyüklüğü/GA/alt-grup endpoint'ini çıkar (locator kaydet).
- [ ] **Step 4: D5 + çıktı** — matris satırlarını üret; `iliski` alanında H1 küçük etki (d≈0,16) Pinquart bandının (d≈0,13–0,30) neresinde konumlandığını işaretle.
- [ ] **Step 5: Doğrulama** — G-BIB (her satır kimlikli), G-XVAL (H1 konumlandırması ≥2 kaynak), KVKK (yalnız literatür terimi). Satırları koordinatöre döndür.

### Task 2: C2 — H3 anne öz-rapor H₀ + sosyal istenirlik literatürü

**Files:** Return-only (kume=C2)

**Interfaces:**
- Consumes: `04_bulgular.qmd` §4.3.3 (H3: BF₁₀ 0,17–0,25; TOST 2/4 Equivalent; ROPE %61–92), `CSR#h3-karar`
- Produces: C2 kanıt matrisi satırları

- [ ] **Step 1: D0 facet** — yapı: `maternal self-report parenting`, `social desirability responding`, `defensive responding`, `good-mother self-presentation`; bağlam: `T1DM maternal burden/stress/distress`; yöntem: `equivalence/TOST interpretation`, `self-report vs observed parenting`.
- [ ] **Step 2: D1–D2 tarama** — `type 1 diabetes maternal stress caregiving burden`, `social desirability parenting self-report bias`, `parent self-report versus observed parenting discrepancy`, `Streisand pediatric parenting stress diabetes`. Minerva TR `mode:semantic`.
- [ ] **Step 3: D4 tam-metin** — Streisand-Monaghan + bir sosyal-istenirlik/savunmacı-yanıt kaynağı + (varsa) öz-rapor↔gözlem farkı kaynağının endpoint'i.
- [ ] **Step 4: D5 + çıktı** — matris satırları; `iliski`de H3 H₀'ın "yük yokluğu değil öz-rapor görünürlük sınırı" yorumunu besleyen kaynakları işaretle (nitel Tema 2 ile karma köprüye zemin).
- [ ] **Step 5: Doğrulama** — G-BIB/G-XVAL/KVKK; döndür.

### Task 3: C3 — H4 maternal depresyon → ebeveynlik literatürü

**Files:** Return-only (kume=C3)

**Interfaces:**
- Consumes: `04_bulgular.qmd` §4.3.4 (H4: Beck→sıcaklık −0,28; reddetme +0,33; karşılaştırma +0,28; aşırı koruma ns), `CSR#h4-karar`
- Produces: C3 kanıt matrisi satırları

- [ ] **Step 1: D0 facet** — yapı: `maternal depression`, `parenting behavior`, `mediator/pathway`; sonuç: `warmth/rejection/hostility`; yöntem: `meta-analysis`, `latent SEM cross-sectional`; bağlam: `pediatric chronic illness`.
- [ ] **Step 2: D1–D2 tarama** — `maternal depression parenting behavior meta-analysis` (Lovejoy/Goodman), `depression parenting warmth hostility pathway`, `maternal depression type 1 diabetes child`. Minerva TR `mode:semantic`.
- [ ] **Step 3: D4 tam-metin** — Lovejoy 2000 + Goodman mediator + (varsa) T1DM maternal depresyon kaynağının yön/büyüklük endpoint'i.
- [ ] **Step 4: D5 + çıktı** — matris satırları; `iliski`de kesitsel-SEM yorum sınırını (a-yolu var, b-yolu ns) besleyen kaynakları işaretle.
- [ ] **Step 5: Doğrulama** — G-BIB/G-XVAL/KVKK; döndür.

### Task 4: C4 — H2 kardeş ilişkisi / kronik hastalık literatürü

**Files:** Return-only (kume=C4)

**Interfaces:**
- Consumes: `04_bulgular.qmd` §4.3.2 (H2: d<0,20; FDR p>0,350; "kanıt yetersizliği ≠ eşdeğerlik"), `CSR#h2-karar`
- Produces: C4 kanıt matrisi satırları

- [ ] **Step 1: D0 facet** — popülasyon: `siblings of children with chronic illness/type 1 diabetes`; yapı: `sibling relationship quality`, `well-sibling adjustment/burden`; ölçüm: `SRQ Furman-Buhrmester`; yöntem: `systematic review/meta-analysis`.
- [ ] **Step 2: D1–D2 tarama** — `siblings chronic illness psychological adjustment meta-analysis`, `well sibling type 1 diabetes burden`, `sibling relationship pediatric chronic disease`, `Furman Buhrmester sibling relationship questionnaire`. Minerva TR `mode:semantic`.
- [ ] **Step 3: D4 tam-metin** — Lummer-Aikey + bir kronik-hastalık kardeş meta-analizi/derlemesinin karma (artmış çatışma vs destek) örüntü endpoint'i.
- [ ] **Step 4: D5 + çıktı** — matris satırları; `iliski`de null bulgunun "kardeş ilişkisi sağlam ama görünmez yük ölçekte görünmeyebilir" (nitel Tema 1 karma köprü) çerçevesini besleyen kaynaklar.
- [ ] **Step 5: Doğrulama** — G-BIB/G-XVAL/KVKK; döndür.

### Task 5: C5 — H5 diadik / informant / triadik literatürü (birincil karma katkı)

**Files:** Return-only (kume=C5)

**Interfaces:**
- Consumes: `04_bulgular.qmd` §4.3.5 (H5: triangülasyon karşılanmadı; ICC kontrol>DM 4/4; Olsen-Kenny reddetme r=0,19), `CSR#h5-karar`, `CSR#sec-genel-hipotez-ozet`
- Produces: C5 kanıt matrisi satırları

- [ ] **Step 1: D0 facet** — yapı: `parent-child dyadic concordance/agreement`, `informant discrepancy` (De Los Reyes), `Social Relations Model`; ölçüm: `ICC agreement` (Cicchetti, Koo-Li), `Kenny-Kashy-Cook dyadic`; sonuç: `clinical implication of low agreement`.
- [ ] **Step 2: D1–D2 tarama** — `parent child agreement parenting perception dyadic`, `informant discrepancy De Los Reyes clinical`, `intraclass correlation agreement interpretation guidelines`, `social relations model parent child`. Minerva TR `mode:semantic`.
- [ ] **Step 3: D4 tam-metin** — De Los Reyes informant-discrepancy çerçevesi + Cicchetti/Koo-Li ICC eşik kaynağı + Kenny-Kashy-Cook diadik kaynağının yorum endpoint'i.
- [ ] **Step 4: D5 + çıktı** — matris satırları; `iliski`de "düşük uyum = ölçüm hatası değil, informant-özgü geçerli varyans" (De Los Reyes) çerçevesini birincil karma katkıya (nitel Tema 4) bağla.
- [ ] **Step 5: Doğrulama** — G-BIB/G-XVAL/KVKK; döndür.

### Task 6: C6 — Nitel 4 makro tema literatürü

**Files:** Return-only (kume=C6)

**Interfaces:**
- Consumes: `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd` (tema 1–4, de-identified), `nitel-cikti-cercevesi.md`
- Produces: C6 kanıt matrisi satırları

- [ ] **Step 1: D0 facet** — Tema 1 `well-sibling invisible burden`; Tema 2 `medicalization of mothering, illness intrusiveness, caregiver guilt`; Tema 3 `child lived experience T1DM, stigma-normalization, autonomy`; Tema 4 `family systems, role differentiation, multi-informant illness meaning`. Yöntem: `reflexive thematic analysis`, `qualitative chronic illness family`.
- [ ] **Step 2: D1–D2 tarama** — `type 1 diabetes family lived experience qualitative`, `mothers caregiving burden diabetes qualitative`, `well siblings chronic illness qualitative experience`, `illness intrusiveness family`, `children type 1 diabetes stigma normalization qualitative`. Minerva TR `mode:semantic`.
- [ ] **Step 3: D4 tam-metin** — her tema için ≥1 nitel/karma kaynağın bağlamsal bulgu endpoint'i (thick description transfer notu).
- [ ] **Step 4: D5 + çıktı** — matris satırları; `iliski`de her temanın literatürdeki karşılığı + boşluk (triadik multi-informant nitel tasarımın özgünlüğü). KVKK: yalnız de-identified tema/kod; ham alıntı yok.
- [ ] **Step 5: Doğrulama** — G-BIB/G-XVAL/KVKK (nitel kaynak sınırı); döndür.

### Task 7: C7 — Keşfisel katmanlar literatürü ([KEŞFİSEL])

**Files:** Return-only (kume=C7)

**Interfaces:**
- Consumes: `04_bulgular.qmd` §4.4 (aracılık, LPA/LCA, ağ/NCT, klinik risk skoru/DCA, DM klinik, taban-duyarlı IRT, multiverse/TOST/sensemakr), `apa_t14–t21`
- Produces: C7 kanıt matrisi satırları

- [ ] **Step 1: D0 facet** — `causal mediation sensitivity (Imai-Keele-Tingley)`, `latent profile analysis parenting typology`, `Gaussian graphical model psychopathology network`, `decision curve analysis clinical utility (Vickers-Elkin)`, `floor effect item response theory`, `multiverse/specification curve`.
- [ ] **Step 2: D1–D2 tarama** — her keşfisel yöntem için metodolojik ankraj + (varsa) substantif uygulama kaynağı. Minerva TR `mode:semantic`.
- [ ] **Step 3: D4 tam-metin** — yalnız metne girecek metodolojik/eşik kaynaklarının (ör. DCA net-benefit, ISPAD HbA1c eşiği) endpoint'i.
- [ ] **Step 4: D5 + çıktı** — matris satırları; **HER C7 satırı `iliski` alanında "hipotez-üretici/keşfisel" işaretli**; `claim` dili "doğrulandı" içermez.
- [ ] **Step 5: Doğrulama** — G-BIB/G-XVAL/KVKK + [KEŞFİSEL] dil kontrolü; döndür.

### Task 8: C8 — Psikometri / ölçüm literatürü (kesişen)

**Files:** Return-only (kume=C8)

**Interfaces:**
- Consumes: `04_bulgular.qmd` §4.2 (EMBU-P reddetme α=0,45; taban etkisi; 4-faktör sınırlı; invariance), `apa_t*` psikometri
- Produces: C8 kanıt matrisi satırları

- [ ] **Step 1: D0 facet** — `EMBU short form (s-EMBU) factor structure`, `EMBU reliability child adolescent`, `low internal consistency short subscale interpretation`, `floor effect measurement`, `measurement invariance`, `Turkish EMBU adaptation`.
- [ ] **Step 2: D1–D2 tarama** — `s-EMBU factor structure validation`, `EMBU rejection subscale reliability`, `measurement invariance parenting scale groups`, `EMBU Turkish adaptation validity`. Minerva TR `mode:semantic`.
- [ ] **Step 3: D4 tam-metin** — s-EMBU validasyon + Türkçe adaptasyon kaynağının α/ω/faktör endpoint'i.
- [ ] **Step 4: D5 + çıktı** — matris satırları; `iliski`de reddetme α=0,45'in literatürdeki EMBU reddetme güvenirlik profiliyle karşılaştırması + Türk T1DM örnekleminde adaptasyon boşluğu.
- [ ] **Step 5: Doğrulama** — G-BIB/G-XVAL/KVKK; döndür.

### Task 9: Çapraz-uzlaştırma + kanıt matrisi TSV yaz

**Files:**
- Create: `tez-yazim/02_kanit-haritalari/tartisma-kanit-matrisi.tsv`

**Interfaces:**
- Consumes: Görev 1–8 kanıt matrisi satırları (tümü)
- Produces: konsolide, dedup'lanmış `tartisma-kanit-matrisi.tsv` (Faz-B taslağının tek kanıt kaynağı)

- [ ] **Step 1: Birleştir** — 8 kümenin satırlarını tek listede topla.
- [ ] **Step 2: Kaynak-dedup** — aynı `source_ids` birden çok kümede varsa tek `bib_key`e uzlaştır; küme-etiketi çoklu olabilir (ör. De Los Reyes hem C1 hem C5). Çelişen `claim`leri harmonize et.
- [ ] **Step 3: TSV yaz** — başlık satırı = şema kolonları; her satır bir sekme-ayraçlı kayıt. UTF-8.
- [ ] **Step 4: Doğrulama** —
Run: `awk -F'\t' 'NR>1 && NF!=10 {print "BAD ROW "NR": "NF" cols"}' tez-yazim/02_kanit-haritalari/tartisma-kanit-matrisi.tsv; echo "rows: $(($(wc -l < tez-yazim/02_kanit-haritalari/tartisma-kanit-matrisi.tsv)-1))"`
Expected: hiç "BAD ROW" yok; rows > 0. Her satırın `source_ids` boş değil.
- [ ] **Step 5: Commit + ⏸ CHECKPOINT**
```bash
git add tez-yazim/02_kanit-haritalari/tartisma-kanit-matrisi.tsv
git commit -m "docs(tartisma): kanıt matrisi — 8 küme derin-lit fan-out konsolidasyonu

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```
**⏸ KULLANICI İNCELE:** kanıt matrisi doğru/yeterli mi? Onay sonrası Faz-B.

---

## Faz B — Akıcı Marmara Taslağı (Görev 10–14, sıralı)

> Her taslak görevi `tartisma-kanit-matrisi.tsv`'yi kaynak alır, `chapters/05_tartisma_ve_sonuc.qmd`'yi düzenler, aday-atıf (`<!-- cand -->`) + kaynak-ankraj yorumlarıyla yazar. Görevler mevcut alt-başlıklı içeriği aşamalı olarak akıcı omurgayla değiştirir.

### Task 10: M1 sentez + M2 hipotez yorumu (çocuk→anne→depresyon→kardeş)

**Files:**
- Modify: `chapters/05_tartisma_ve_sonuc.qmd` (M1+M2 hareketleri; mevcut satır 5–25 alt-başlıklı H bölümleri akıcıya dönüşür)
- Read: `tez-yazim/02_kanit-haritalari/tartisma-kanit-matrisi.tsv` (C1–C4)

**Interfaces:**
- Consumes: kanıt matrisi C1–C4 satırları
- Produces: 05.qmd başında alt-başlıksız M1+M2 akışı

- [ ] **Step 1: M1 sentez** — birkaç cümlede en önemli çıktıların çerçevesi (tekrar değil): informant düzlemine göre ayrışma (çocukta H1 sinyal / annede H3 H₀). Özgün-değer cümlesi.
- [ ] **Step 2: M2 yaz (sıra: H1→H3→H4→H2)** — her hipotez için: destek durumu AÇIK ("desteklendi/kısmi/desteklenmedi") + benzer/farklı çalışma (matris C1–C4) + olası neden + tedbir denetimi (etki büyüklüğü/GA baskın; tek meta-analiz mutlak değil; popülasyon transferi). Aday atıflar `[@key]` + `<!-- cand -->`.
- [ ] **Step 3: Doğrulama — bulgu-tekrarı taraması**
Run: `grep -nE 'BF₁₀ = [0-9]|β = [0-9]|p < 0,0|CFI = |RMSEA = |%9[0-9]|ROPE %' chapters/05_tartisma_ve_sonuc.qmd | sed -n '1,40p'`
Expected: M1+M2 bölgesinde tam istatistik-blok tekrarı yok (çerçeveleme için tek minimal sayı kabul; tablo/şekle atıf tercih). Fazlalık varsa sadeleştir.
- [ ] **Step 4: Doğrulama — nedensellik dili taraması**
Run: `grep -nE 'neden ol|yol aç|-e neden|sonucunu doğur|kanıtla(dı|r|nmış)' chapters/05_tartisma_ve_sonuc.qmd`
Expected: eşleşme yok (M1+M2 bölgesi).
- [ ] **Step 5: Commit**
```bash
git add chapters/05_tartisma_ve_sonuc.qmd
git commit -m "feat(tartisma): M1 sentez + M2 hipotez yorumu (informant düzlemi, akıcı)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

### Task 11: M3 H5 + karma yenilik + M4 nitel temalar

**Files:**
- Modify: `chapters/05_tartisma_ve_sonuc.qmd` (M3+M4)
- Read: kanıt matrisi C5, C6

**Interfaces:**
- Consumes: matris C5 (diadik/informant) + C6 (nitel tema)
- Produces: M3 (H5+karma novelty) + M4 (nitel 4 tema) akışı

- [ ] **Step 1: M3 yaz** — H5 diadik: nicel *NE* (hangi boyutta/ne kadar uyum/uyumsuzluk; triangülasyon karşılanmadı — betimsel) / nitel *NEDEN* (rol-temelli çerçeveleme). De Los Reyes informant-discrepancy çerçevesi (C5): düşük uyum = ölçüm hatası değil, informant-özgü geçerli varyans. **Özgün-değer omurgası:** ayrışma haritalaması birincil katkı. Aday atıflar.
- [ ] **Step 2: M4 yaz** — 4 makro tema literatürle (C6) + negatif vaka (Aile 201) + refleksif okuma. Nitel aktarılabilirlik (thick description) ≠ nicel genellenebilirlik ayrımı açık. Ham alıntı yok; quote-ID/tema düzeyi.
- [ ] **Step 3: Doğrulama — kanıt-türü ayrımı**
Run: `grep -nE 'tema.{0,30}(etki büyüklüğü|β|kanıtla)|nitel.{0,30}nedensel' chapters/05_tartisma_ve_sonuc.qmd`
Expected: eşleşme yok (nitel tema nicel etki/nedensel kanıt yapılmamış).
- [ ] **Step 4: Doğrulama — nedensellik + KVKK**
Run: `grep -nE 'neden ol|yol aç' chapters/05_tartisma_ve_sonuc.qmd; grep -nE '[A-ZÇĞİÖŞÜ][a-zçğıöşü]+ (dedi|anlattı|söyledi)' chapters/05_tartisma_ve_sonuc.qmd`
Expected: nedensellik eşleşmesi yok; ham-alıntı-imzası yok.
- [ ] **Step 5: Commit**
```bash
git add chapters/05_tartisma_ve_sonuc.qmd
git commit -m "feat(tartisma): M3 H5+karma yenilik + M4 nitel tema yorumu

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

### Task 12: M5 karma bütünleştirme + M6 keşfisel + M7 psikometri

**Files:**
- Modify: `chapters/05_tartisma_ve_sonuc.qmd` (M5+M6+M7; mevcut satır 77–129 "provisional meta-çıkarım/köprü" bloğu BURAYA erir ve alt-başlıkları kaldırılır)
- Read: kanıt matrisi C7, C8 + Bulgular 4.7 joint display

**Interfaces:**
- Consumes: matris C7 (keşfisel) + C8 (psikometri); Bulgular §4.7 joint display etiketleri
- Produces: M5 (karma bütünleştirme) + M6 (keşfisel ihtiyatlı) + M7 (psikometri) akışı; provisional blok konsolide

- [ ] **Step 1: M5 yaz** — joint display'i (Bulgular 4.7) *yorumlar*: uyum/tamamlayıcılık/ayrışma/açıklayıcı-genişleme etiketleri akış içinde. Mevcut 4 meta-çıkarım + 4 köprü içeriği buraya eritilir (tekrar değil, yorum). Ayrışma = teorik katkı, hata değil.
- [ ] **Step 2: M6 yaz** — keşfisel katmanlar (C7) ihtiyatlı: "literatürle tutarlı / hipotez-üretici". Her cümle `[KEŞFİSEL]` epistemik çerçeveli; dış-validasyon şartı.
- [ ] **Step 3: M7 yaz** — psikometrik/ölçüm çıkarımları (C8): EMBU reddetme α=0,45 literatür profili, taban etkisi, Türk T1DM adaptasyon zorunluluğu.
- [ ] **Step 4: Eski provisional blok temizliği** — satır 77–129 arası alt-başlıklı "Karma-Kol Meta-Çıkarım / Tartışma Köprüsü" başlıklarını kaldır; içerik M5'e erimiş olmalı. `<!-- kaynak: -->` ankrajları korunur.
- [ ] **Step 5: Doğrulama — alt-başlık + keşfisel-dil**
Run: `grep -nE '^#{2,}' chapters/05_tartisma_ve_sonuc.qmd; grep -nE '\[KEŞFİSEL\]|keşfisel' chapters/05_tartisma_ve_sonuc.qmd | head`
Expected: `##` başlık YOK (M12 Sonuç dahil hepsi akıcı — yalnız bölüm-başı `# TARTIŞMA ve SONUÇ` kalır); keşfisel bulgular ihtiyat çerçeveli.
- [ ] **Step 6: Commit**
```bash
git add chapters/05_tartisma_ve_sonuc.qmd
git commit -m "feat(tartisma): M5 karma bütünleştirme (provisional konsolide) + M6 keşfisel + M7 psikometri

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

### Task 13: M8 güçlü yönler + M9 sınırlılıklar + M10 sonuç + M11 öneriler

**Files:**
- Modify: `chapters/05_tartisma_ve_sonuc.qmd` (M8–M11; mevcut Sonuç satır 63–73 akıcıya uyarlanır)

**Interfaces:**
- Consumes: tüm matris + spec §4 M8–M11
- Produces: kapanış akışı (güçlü yön → sınırlılık → sonuç → öneriler)

- [ ] **Step 1: M8 güçlü yönler** — karma tasarım, triad multi-informant, açık bilim/tekrarlanabilirlik, sensitivite üçlüsü.
- [ ] **Step 2: M9 sınırlılıklar** — kesitsel/nedensellik, örneklem (nicel 241 aile; nitel 7 aile — aktarılabilirlik ≠ genellenebilirlik), öz-bildirim/sosyal istenirlik, EMBU-P reddetme α, HbA1c %32,5, informant yanlılığı, tek-merkez/kültür + sapma şeffaflığı (OSF pytfe/d524q).
- [ ] **Step 3: M10 sonuç** — varılan sonuçlar açık/kısa; amacın ne ölçüde gerçekleştiği; teorik/klinik/metodolojik katkı.
- [ ] **Step 4: M11 öneriler** — klinik/aile · araştırma · politika; amaç-bulgu sınırlı; aşırı genelleme yok.
- [ ] **Step 5: Doğrulama — öneri sınırı + nedensellik**
Run: `grep -nE 'neden ol|yol aç|kanıtla(dı|r)' chapters/05_tartisma_ve_sonuc.qmd; grep -cE '^#{2,}' chapters/05_tartisma_ve_sonuc.qmd`
Expected: nedensellik eşleşmesi yok; `##` sayısı = 0.
- [ ] **Step 6: Commit**
```bash
git add chapters/05_tartisma_ve_sonuc.qmd
git commit -m "feat(tartisma): M8–M11 güçlü yön/sınırlılık/sonuç/öneriler (akıcı kapanış)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

### Task 14: Tam bölüm birleştirme + akış/geçiş düzeltme

**Files:**
- Modify: `chapters/05_tartisma_ve_sonuc.qmd` (bütünsel geçiş cümleleri + tutarlılık)

**Interfaces:**
- Consumes: M1–M11 taslağı
- Produces: tek akıcı bölüm (geçişler pürüzsüz; tekrar yok)

- [ ] **Step 1: Bütünsel okuma** — M1→M11 geçiş cümlelerini ekle/düzelt; hareketler arası tekrar (özellikle M2↔M5 hipotez, M4↔M6) ayıkla.
- [ ] **Step 2: Doğrulama — bölüm-izole render**
Run: `quarto render chapters/05_tartisma_ve_sonuc.qmd --to html 2>&1 | tail -20`
Expected: hata yok (yalnız `<!-- cand -->` atıflar henüz bib'de yoksa `[?@key]` uyarısı olabilir — Faz-C'de kapanır).
- [ ] **Step 3: ⏸ CHECKPOINT commit**
```bash
git add chapters/05_tartisma_ve_sonuc.qmd
git commit -m "feat(tartisma): tam akıcı bölüm birleştirme + geçiş düzeltme (taslak tamam)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```
**⏸ KULLANICI İNCELE:** taslak akış/içerik/özgün-değer yeterli mi? Onay sonrası Faz-C.

---

## Faz C — Referans Kapısı + Denetim + Sertifikasyon (Görev 15–17)

### Task 15: Toplu referans kapısı + bib entegrasyonu

**Files:**
- Modify: `references/references.bib` (yeni `YENI:` @key'ler → gerçek künye)
- Modify: `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` (cite-ok satırları)
- Modify: `chapters/05_tartisma_ve_sonuc.qmd` (`<!-- cand -->` işaretlerini kaldır)

**Interfaces:**
- Consumes: kanıt matrisi TSV (`bib_key` YENI olanlar) + taslak aday atıflar
- Produces: cite-ok referanslar; bib_hygiene temiz

- [ ] **Step 1: Ön-mutabakat (önce başarısız beklenir)**
Run: `python3 scripts/util/bib_hygiene.py all --chapters chapters/05_tartisma_ve_sonuc.qmd; echo "exit=$?"`
Expected: exit=1 (atıflı-tanımsız YENI @key'ler — henüz bib'de yok). Bu, kapının yapılacak işi gösterir.
- [ ] **Step 2: Yeni künyeleri ekle** — matris `YENI:` satırları için `references.bib`'e AMA-11/BibTeX künye ekle (DOI + tam-metin doğrulanmış; `/referans-kapisi` 7 adım: DOI→tam-metin→Zotero 9ZFDHMZA→claim→iki-kol AI-reliability). `zotero-refs` ile koleksiyon senkron + `zotero_set_tag`.
- [ ] **Step 3: Aday işaretleri kaldır** — 05.qmd'de `<!-- cand -->` yorumlarını sil (kapı kapandı).
- [ ] **Step 4: Doğrulama (şimdi geçer)**
Run: `python3 scripts/util/bib_hygiene.py all --chapters chapters/05_tartisma_ve_sonuc.qmd; echo "exit=$?"`
Expected: exit=0 (atıflı-tanımsız yok; alan/DOI/dup temiz).
- [ ] **Step 5: Ledger güncelle** — her yeni referansın satırı `cite-ok` durumuna geçer.
- [ ] **Step 6: Commit**
```bash
git add references/references.bib tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md chapters/05_tartisma_ve_sonuc.qmd
git commit -m "feat(tartisma): toplu referans kapısı — yeni künyeler cite-ok + bib_hygiene temiz

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

### Task 16: sci-audit A–G + düzeltmeler

**Files:**
- Modify: `chapters/05_tartisma_ve_sonuc.qmd` (audit blocker düzeltmeleri)

**Interfaces:**
- Consumes: cite-ok bölüm
- Produces: sci-audit blocker'sız bölüm

- [ ] **Step 1: sci-audit koş** — `sci-audit:audit` (axis A uydurma/yanlış-atıf · B kaynaksız iddia · C istatistik/bulgu-tekrarı · F AI-şeffaflık · G Türkçe bilimsel dil). Türkçe → axis G auto.
- [ ] **Step 2: Blocker düzelt** — HARD bulgular (uydurma atıf, kaynaksız iddia, nedensellik dili, bulgu-tekrarı, imla) giderilir. Deterministik bulgu LLM-yargısına üstün.
- [ ] **Step 3: Doğrulama — yeniden koş**
Expected: axis A–G HARD blocker yok.
- [ ] **Step 4: Commit**
```bash
git add chapters/05_tartisma_ve_sonuc.qmd
git commit -m "fix(tartisma): sci-audit A-G blocker düzeltmeleri

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

### Task 17: quarto render + Kapı 0–5 sertifikası + final

**Files:**
- Create: `tez-yazim/04_kalite-kontrol/sertifikalar/05-tartisma-ve-sonuc-sertifika-2026-07-13.md`

**Interfaces:**
- Consumes: cite-ok + audit-temiz bölüm
- Produces: Kapı 0–5 sertifikası; render-doğrulanmış bölüm

- [ ] **Step 1: Bölüm-izole render**
Run: `quarto render chapters/05_tartisma_ve_sonuc.qmd --to html 2>&1 | tail -20`
Expected: hata yok; `[?@key]` çözümsüz-atıf uyarısı YOK (tüm atıflar bib'de).
- [ ] **Step 2: Kapı 0–5 kontrol listesi** — brief §8 kapanış kapıları: bulgu-tekrarı yok · hipotez destek açık · nedensellik+kanıt-türü ayrımı · karma joint-display etiketi · öneri amaç-bulgu sınırlı, alt-başlık yok · dış referans cite-ok + iki-kol AI-reliability · format §12 + sci-audit temiz.
- [ ] **Step 3: Sertifika yaz** — `bolum-sertifika` skill formatında; Kapı 0–5 durumları + kanıt (bib_hygiene exit0, sci-audit rapor, render log, matris TSV).
- [ ] **Step 4: Final commit + ⏸ AÇIK ONAY**
```bash
git add tez-yazim/04_kalite-kontrol/sertifikalar/05-tartisma-ve-sonuc-sertifika-2026-07-13.md
git commit -m "docs(tartisma): Kapı 0-5 sertifikası — 05 Tartışma ve Sonuç derin-lit finalize

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```
**⏸ certified-final yalnız AÇIK KULLANICI ONAYIYLA** (bolum-sertifika kuralı).

---

## Öz-İnceleme (plan ↔ spec)

**Spec kapsama kontrolü:**
- Spec §3 C1–C8 kümeleri → Görev 1–8 ✓
- Spec §4 M1–M11 akışı → Görev 10–14 ✓ (M1+M2→G10, M3+M4→G11, M5+M6+M7→G12, M8–M11→G13, birleştirme→G14)
- Spec §5 literatür motoru (D0–D6, minerva/openathens/annas/anamnesis) → Görev 1–8 ortak iskelet ✓
- Spec §6 kanıt matrisi → Görev 9 (şema + TSV) ✓
- Spec §7 toplu referans kapısı → Görev 15 ✓
- Spec §8 sci-audit + Kapı 0–5 → Görev 16–17 ✓
- Spec §9 kademeli yürütme (2 checkpoint) → Görev 9 (⏸) + Görev 14 (⏸) ✓
- Spec §10 deliverables → Görev 9 (TSV), 14 (qmd), 15 (bib/ledger), 17 (sertifika) ✓
- Spec K1 alt-başlıksız → Görev 12/13 grep `##`=0 ✓; K2 [KEŞFİSEL] → Görev 7/12 ✓; K3 taslak→toplu → Faz sırası ✓; K4 informant sıra → Görev 10 ✓; K5 kalıcı matris → Görev 9 ✓; K6 8-küme+dedup → Görev 1–9 ✓

**Placeholder taraması:** Faz-A görevlerinde gerçek prose önceden yazılamaz (retrieval'a bağlı); bunun yerine her görev exact facet + exact sorgu varyantı + exact matris şeması + exact doğrulama komutu taşır — plan-uygun kesinlik. Kod/komut adımları exact.

**Tip tutarlılığı:** matris şeması (10 kolon) Görev 1–8 çıktısı ↔ Görev 9 TSV ↔ Görev 15 `bib_key` tüketimi tutarlı; `<!-- cand -->` Görev 10–14 üretir ↔ Görev 15 kaldırır.
