---
description: Marmara tez narratif derin-literatür incelemesi + sentez + tartışma (systematic review DEĞİL)
argument-hint: "<bölüm: giris|genel-bilgiler|tartisma> <konu>"
---

# /tez-literatur — Narratif Derin-Lit Modu

Kullanıcı argümanı: **$ARGUMENTS**

Bu komut sistematik derleme ÇALIŞTIRMAZ. Marmara tez kılavuzu çerçevesinde
narratif derin-literatür incelemesi + sentez + tartışma üretir.

## Yürütme

1. **Kapsam + tedbir kapısı** — t1dm-tez-rehberi Faz 0 (hipotez/SAP kısmı, veri
   çerçevesi, artefakt, kanonik-kilit, OSF) + Faz 0.5 tedbir denetimi. Kapı
   geçmezse dur.
2. **Doktrini yükle** — `.claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md`
   §"Narratif Derin-Lit Modu (tez; SR değil)" (kaskad + çıktı sözleşmesi + gate'ler).
3. **Bölüm sözleşmesini seç** — `$ARGUMENTS` ilk tokeni:
   - `giris` → literatür özet; alt başlık yok; boşluk+önem+amaç.
   - `genel-bilgiler` → genelden özele; yorum/sonuç çıkarımından kaçın; H1–H5 alt-başlık.
   - `tartisma` → karşılaştır-literatürle; hipotez destek beyanı; bulgu/istatistik tekrarı yok.
4. **D0–D6 kaskad** — evidentia connectors (pubmed-epmc, openalex, semantic-scholar,
   anamnesis, evidentia-kb, openathens, annas-reader, yok-akademik) + Minerva
   (`minerva_literature_search` D2; `minerva_*_fulltext`/`get_article` D4, annas ÖNCESİ).
   **Minerva Türkçe-sorgu = `mode:semantic` zorunlu** (hibrit BM25 TR↔EN karıştırır;
   bkz. `literatur-kanit-evidentia.md` Minerva mod kuralı). Ağır fan-out için
   `evidentia:evidence-synthesizer` alt-ajanı. **KVKK: yalnız literatür terimi.**
5. **Sentez** — anamnesis GraphRAG; retrieve-don't-dump. Birleşik bağlam paketi için
   `scripts/mcp/graphrag_query.py` (hybrid_query + graph_neighbors + Galileo füzyon
   yeniden-sıralama).
6. **Taslak + künye** — Türkçe `[@key]` metin + `references/references.bib` künye
   adayları. Hiçbir künye **referans kapısı** (`/referans-kapisi`) `cite-ok`
   olmadan kaynakçaya girmez. Kaynakça biçimini `references/marmara-ama11.csl` render eder.
7. **Denetim** — sci-audit Faz 3.6 (axis A referans, B claim, C istatistik, G Türkçe imla).

## Devir (scope guard)
- Gerçek sistematik/kapsam derleme → `/evidentia:evidentia` (PRISMA P0→P7).
- MLR/promosyon → `promo-censor`; bireysel SGK/dava → `ius-salutis`.

## Bağlayıcı
UYDURMA REFERANS YASAĞI · PRIOR/HARKing tuzağı · tez kaynak olamaz (§4.2) ·
web ≤%5 yalnız .gov/.int/.eu · ana gate her zaman t1dm-tez-rehberi.

- **Referans Bütünlük Şiarı (RBŞ — konstitüsyonel; `tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md` §4.1):** Bir referanstan zenginleştirme/analiz yaparken makalenin **bir parçasını değil tamamını geniş bağlamda semantik kavra**, bu bağlamı **rafine ederek** revize et; **hem kaynağın hem tez metninin somut bilimsel iddialarını çarpıtma** (cherry-pick / düzleştirme / abartma yok; kaynak kendi kapsam+koşuluyla aktarılır).
