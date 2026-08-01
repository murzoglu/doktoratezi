# L5 — Klinik & Regülatif Bağlam MCP Katmanı (NSCLC SR)

> Kapsam: yalnız akciğer kanseri tedavi **sistematik derlemesi**; yalnız `NSCLC/`
> alt-ağacı. Bu katman, `.mcp.json`'da bağlı olup önceki referanslarda
> kullanılmayan MCP sunucularını SR iş akışına ekler. **Sırlar bu belgede
> tutulmaz** (connector key/URL yalnız `.mcp.json` + gizli `MCP-TALIMATLAR.md`'de).

---

## 0. Kanıt katmanı ↔ Bağlam katmanı (bağlayıcı ayrım)

Bu, bu katmanın **en kritik** kuralıdır ve deterministik olarak zorlanır
(bkz. `scripts/context_source_guard.py`).

| Katman | Sunucular | SR'de ne YAPAR | SAYI besleyebilir mi |
|--------|-----------|----------------|:---:|
| **Kanıt** | minerva-evidence, openathens, annas-reader | Dahil çalışmalardan endpoint/HR/GA çıkarımı | **EVET** (F4→F6) |
| **Bağlam** | ich, titck, eudamed, yok-akademik, socius-vigil, oecd, health-policy | Metodoloji standardı, ruhsat/uygulanabilirlik, gri-literatür lead, epidemiyoloji arka plan | **HAYIR** |
| **Arama-lead** | socius-vigil, yok-akademik | Aday kayıt/çalışma işaret eder | HAYIR (yalnız yönlendirir) |

**Kaide:** Bağlam/arama-lead sunucularından gelen hiçbir sayısal etki tahmini
(`HR`, `OS`, `PFS`, `ORR`, GA) doğrudan çıkarım tablosuna veya sentez metnine
**yazılamaz**. Bu sunucular yalnızca (a) metodolojik/uygulanabilirlik gerekçesi,
(b) bir tam-metne yönlendirme sağlar; sayı her zaman **minerva/openathens/annas
üzerinden birincil tam-metinden yeniden çıkarılır** (F4). İhlal = HARD blocker.

---

## 1. ich-mcp — ICH metodoloji & kılavuz (BAĞLAM)

- **Rol:** SR'nin metodolojik çerçeve dayanağı. Canlı korpus: 153 kılavuz /
  142 tam-metin (Q·S·E·M), sayfa-bazlı FTS → tam sayfa atıfı.
- **SR'de kullanım:**
  - **F1 (protokol):** **E9(R1) estimand** çerçevesi — SR sorusunu estimand
    diliyle çerçevele (popülasyon, tedavi, endpoint, intercurrent-event
    stratejisi, popülasyon-düzeyi özet). **E6(R2) GCP** ile dahil RCT'lerin
    yürütme-kalitesi beklentisi; **E8(R1)** çalışma-tasarımı tipolojisi.
  - **F5 (RoB):** endpoint tanımı/ölçüm standardı (ör. **E14** QT, **S9**
    onkoloji nonklinik) RoB gerekçesini besler.
- **Araç:** `ich_search` (sayfa-FTS), `ich_get_guideline`.
- **No-fabrication:** her çıktı `mcp_verified:false` + `_caveat`; PDF URL'leri
  korpus JSON'dan gelir, kurgulanmaz. **ICH sayısal eşik veremez** (yalnız norm).

## 2. titck-mcp / titck-cache — TR ilaç ruhsat & KÜB (BAĞLAM)

- **Rol:** Türkiye uygulanabilirlik lensi. Dahil çalışmadaki ajanın TR'de ruhsatlı
  olup olmadığı, KÜB endikasyon/doz — SR'nin **dış geçerlik/transfer** bölümüne
  girdi.
- **SR'de kullanım:** F6 sentez "TR'ye uygulanabilirlik" alt-başlığı + F8 tartışma
  yerelleştirme. Kamu yüzü `titck-cache` **anahtarsız** (read-through).
- **Sınır:** ruhsat durumu = bağlam; **etkililik sayısı DEĞİL**. KÜB'den etki
  büyüklüğü çıkarım tablosuna yazılamaz.

## 3. eudamed-mcp — AB tıbbi cihaz / tanı testi (BAĞLAM, koşullu)

- **Rol:** Yalnız SR sorusu **biyobelirteç tanı testi** veya **cihaz** (ör.
  EGFR/ALK IVD, NGS paneli) içeriyorsa devreye girer. 6 salt-okunur araç;
  MDR/IVDR filtresi.
- **Zorunlu olgunluk `_caveat`:** veritabanı tam popüle değil → **yokluk kanıt
  değildir**. QUADAS-2 tanı-doğruluk değerlendirmesinde bağlam olarak kullanılır,
  duyarlılık/özgüllük sayısı buradan alınmaz.

## 4. yok-akademik-mcp — TR tez & akademik (ARAMA-lead, BAĞLAM)

- **Rol:** TR literatüründe akciğer kanseri tez/yayın taraması (gri-literatür +
  yerel kanıt kapsama). Çok-veritabanlı aramayı **tamamlar**, yerine geçmez.
- **SR'de kullanım:** F2 kapsama genişletme (TR kaynak) + F8 yerel-bağlam.
  Upstream yalnız TR ağından erişilir.
- **Sınır:** bulunan çalışmanın sayısı yine F4'te birincil tam-metinden çıkarılır.

## 5. socius-vigil — gri-literatür & çok-motor web meta (ARAMA-lead)

- **Rol:** Konferans özetleri (ASCO/ESMO/WCLC), ön-baskı, tescil-dışı sinyaller
  için gri-literatür lead. Çok-motor meta (Brave/Exa/Tavily/Perplexity/Firecrawl/
  SearXNG) + LLM sentez.
- **SR'de kullanım:** F2 gri-literatür kapsaması (PRISMA "diğer yöntem" kaydına
  girer) + yayın-yanlılığı taraması (yayımlanmamış çalışma sinyali).
- **KRİTİK sınır:** socius-vigil bir **LLM-sentez** motorudur → çıktısı **asla
  doğrudan kanıt/sayı değildir**. Yalnız **arama-lead**: işaret ettiği her kayıt
  F3 taramasına girer, sayısı F4'te birincil kaynaktan çıkarılır. socius-vigil
  çıktısı HARD kapı üretemez (LLM-judge doktrini §0 ile aynı mantık).

## 6. oecd-mcp / health-policy — epidemiyoloji & politika (BAĞLAM, opsiyonel)

- **Rol:** Giriş/arka plan için akciğer kanseri yükü, sağlık-sistemi bağlamı
  (OECD Health Statistics; health-policy TR-dışı sağlık mevzuatı US/CA/JP/AU/ES/
  IE/CN/MX). SR sorusunun **gerekçesini** güçlendirir.
- **Sınır:** arka plan istatistiği ≠ SR etki tahmini; ayrı işaretlenir, sentez
  havuzuna karışmaz.

---

## 7. Katman sırası (SR fazlarına eşleme)

| Faz | Bağlam/lead sunucu | Ne katar |
|-----|--------------------|----------|
| F1 Protokol | **ich** (E9 estimand, E6 GCP, E8 tasarım) | Metodolojik çerçeve |
| F2 Arama | **socius-vigil** (gri-lit), **yok-akademik** (TR) | Kapsama genişletme (lead) |
| F4 Çıkarım | *(yalnız kanıt katmanı: minerva/openathens/annas)* | — bağlam sayı VEREMEZ |
| F5 RoB | **ich** (endpoint/ölçüm standardı), **eudamed** (tanı testi bağlamı) | Yargı gerekçesi |
| F6 Sentez | **titck** (TR ruhsat), **oecd/health-policy** (arka plan) | Uygulanabilirlik/dış geçerlik |
| F8 Rapor | **titck**, **yok-akademik** | Yerelleştirme + TR-bağlam |

## 8. Deterministik zorlama

- `scripts/context_source_guard.py`: çıkarım/sentez artefaktlarında bir sayının
  kaynağı bağlam/lead sunucu olarak etiketlenmişse **blocker** (sayı yalnız
  kanıt-katmanı kaynağından). F7 HARD kapısına eklenir.
- Sağlayıcı etiketleme: `extraction.csv` `source_tier` sütunu = `evidence` |
  `context` | `lead`; `evidence` dışı satırdan havuzlanmış etki hesaplanamaz.

---

*Otorite ayrımı için bkz. [`02_sciaudit_onkoloji.md`](02_sciaudit_onkoloji.md) §0
(HARD deterministik) ve [`03_aijudge_galileo_onkoloji.md`](03_aijudge_galileo_onkoloji.md)
§1.1 (SOFT asla HARD'a terfi etmez). Bağlam/lead sunucular aynı doktrine tabidir:
metodoloji/uygulanabilirlik verir, teslim-engeli veya sayı vermez.*
