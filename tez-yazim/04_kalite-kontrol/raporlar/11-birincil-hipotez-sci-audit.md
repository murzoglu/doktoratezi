# §11 Birincil Hipotez Bulguları — Pilot Didaktik Katman Denetim Raporu

Tarih: 2026-07-13 · Kapsam: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` §11 (H1–H5) didaktik mini-blok pilotu · Durum: **pilot tamam, kullanıcı onayı bekliyor**

Plan: `docs/superpowers/plans/2026-07-13-csr-didaktik-katman-pilot-s11.md`
Spec: `docs/superpowers/specs/2026-07-13-csr-didaktik-aciklama-katmani-design.md`

## Yapılan iş

§11'in beş hipotez alt bölümünün her istatistik tekniğine 3-parçalı etiketli mini-blok
(**Bilimsel soru** → **Yöntem & tatbik** → **Nasıl değerlendirilir**) eklendi. Mevcut
`> Yöntem kutusu` blockquote'ları (H1/H2/H3/H5) mini-bloğa dönüştürüldü; H4'te eksik olan
kutu eklendi. Bölüm-sonu `Karar Kutusu` verdict blokları değiştirilmedi (ölçüt-baş /
verdict-son ayrımı).

| Alt bölüm | Mini-blok | Teknikler |
|---|---|---|
| §11.1 H1 | 4 | çok düzeyli+ICC · Bayesçi BF · IRT GRM · üçlü etkileşim |
| §11.2 H2 | 3 | APIM · Olsen-Kenny düad CFA · TOST-durumu |
| §11.3 H3 | 4 | IPTW ANCOVA · antidepresan strata · Bayesçi ROPE/BF · TOST |
| §11.4 H4 | 2 | WLSMV ordinal SEM (kutu eklendi) · çoklu-grup değişmezlik |
| §11.5 H5 | 6 | üst çerçeve · ICC+Bland-Altman · RSA · CFM · Olsen-Kenny CFA · k-katsayısı |
| **Toplam** | **19** | |

Commit'ler: `77bc711` (H1) · `926dabe` (H2) · `61bd6bf` (H3) · `2955caa` (H4) ·
`9b87136` (H5) · `f271b33` (konvansiyon hizalama). Baseline: `8c09f14`.

## Denetim sonuçları

**Kanonik sayı / R-literal koruması (HARD):** R-chunk imzası baseline ile **birebir aynı**
(`N_CHUNKS=60`, `CHUNK_HASH=cbed6d5ae41d71c101fd6e023e11f462`). Hiçbir istatistik değeri,
β, GA, BF, p, verdict veya kod literali değişmedi — yalnız düzyazı açıklama eklendi. **PASS**.

**Axis A / no-fabrication (HARD):** Eklenen düzyazıda **yeni Pandoc `[@key]` atıfı yok**
(git diff `[@…]` taraması boş). Eklenen tüm yazar-yıl künyeleri (Funder ve Ozer, Schäfer ve
Schwarz, Pinquart, Lakens, Cicchetti, Achenbach, De Los Reyes, Kenny, Cheung ve Rensvold,
Chen) baseline CSR'da **zaten mevcuttu** (uydurma değil; provenans baseline `8c09f14`'e karşı
doğrulandı). **PASS**.

**Axis G / Türkçe imla (HARD):** İzole eklenen 110 satırda `tr_sciaudit --strictness
certification` → **BLOCKER YOK** (0 `decimal-dot-p-value`, 0 `encoding-error`). Advisory:
32 `abbreviation-review` (ICC/IPTW/SEM/RSA/CFM/BF/TOST/SESOI/SD/FDR/GRM — hepsi §3
Kısaltmalar'da tanımlı), 2 `sentence-long`. **PASS** (advisory kabul).

**Tutarlılık düzeltmesi (gate bulgusu):** İlk taslakta 4 mini-blokta "ve ark." kullanılmıştı;
CSR belge-geneli **"ve diğerleri"** konvansiyonunu kullanıyor (baseline 59× / 0×). Dört örnek
belgenin yerleşik konvansiyonuna hizalandı (`f271b33`). Yazarlar zaten belgede mevcut olduğundan
bu bir uydurma değil, abbreviation-tutarlılık düzeltmesidir.

**3-parça bütünlüğü:** 19 mini-bloğun tamamında üç parça da mevcut (19 Bilimsel soru +
19 Yöntem & tatbik + 19 Nasıl değerlendirilir; dengeli).

**Galileo advisory (SOFT/advisory):** `audit_stack_healthcheck.py` → **TÜMÜ PASS**
(judge_ok=True, embedding_ok=True, claim_match mode=embedding; sci-audit axis-G canlı).
Mini-bloklar mevcut doğrulanmış künyeleri yeniden kullanıp yeni nicel iddia eklemediğinden
groundedness riski yapısal olarak düşüktür.

## Bilinçli sınırlar

- 2 `sentence-long` advisory kabul edildi (teknik içerik; blocker değil) — istenirse
  bölünebilir.
- `quarto render` bu pilotta çalıştırılmadı; R-literalleri byte-düzeyinde korunduğundan
  render riski yoktur (chunk imzası değişmedi). Tam render kullanıcı onayı sonrası
  yayılım aşamasında.
- Yayılım (kalan 22 bölüm) bu pilotun **kapsamı dışındadır**; ayrı plan + ayrı onay gerektirir.

## Karar

Pilot §11 didaktik katmanı **HARD kapıların tamamından geçti**, Galileo advisory canlı/PASS.
Kullanıcı format/ton/derinlik onayı sonrası kalan bölümlere yayılım başlatılabilir.
