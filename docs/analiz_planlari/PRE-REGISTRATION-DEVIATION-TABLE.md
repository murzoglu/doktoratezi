# Pre-registration Deviation Table

**OSF project:** <https://osf.io/vqrt5/>
**Layer 1 reflective registration:** <https://osf.io/d524q/>
**Layer 2 secondary data preregistration:** <https://osf.io/pytfe/>
**Kanonik veri kilidi:** `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` (2026-04-26)
**Tablo durumu:** Analiz başlamadan önce başlatıldı; sapma oldukça aynı gün güncellenir.

## Sapma Kayıt Tablosu

| # | Tarih | Kayıt katmanı | Ön-kayıtlı karar | Uygulanan değişiklik | Sapma tipi | Gerekçe | Doğrulayıcı statü |
|---|---|---|---|---|---|---|---|
| 0 | 2026-04-27 | Layer 1 + Layer 2 | İki katmanlı OSF stratejisi: psikometrik validasyon reflective kayıt, H1-H5 secondary data preregistration | Uygulama tamamlandı; kayıtlar `d524q` ve `pytfe` olarak submit edildi | Kayıt notu | Analiz öncesi izleme tablosu başlatıldı | Geçerli |
| 1 | 2026-05-01 | Layer 1 + Layer 2 (kapsam yalnızca KISIM I-XVIII) | SAP v3.0 KISIM I-XVIII çerçevesi | Faz II SAP (KISIM XIX-XXXV) eklendi; **2026-05-02 revizyonuyla yeni veri gerektiren 4 hedef (F2-19, F2-35, F2-38, F2-42) çıkarıldı, son kapsam 41 post-hoc analiz, 18 yeni R/ modülü, mevcut n=241 kanonik baz** | Tip 3 (major, post-hoc bütünleşik amendment) | Çalışma-sonu verileri (CSR v1.1 + CSR-V2) ışığında ortaya çıkan 13 boşluk maddesi (12'si mevcut veriyle kapatıldı, dış-validasyon protokolü ileri çalışma kapsamı dışı): EMBU reddetme α/ω düşüklüğü ve floor effect (CSR §10.1, §10.3); H4 SEM CFI=.887/SRMR=.127 (CSR §11.4.2); anne antidepresan SMD=0.53 (CSR §9.2); H5 strateji büyüklük çelişkisi (CSR §11.5.6); negative control flag (CSR §13.5); HbA1c n=39 yetersiz güç (CSR §12.5.1); H1 multiverse eksikliği (CSR §13.6 paradoksu); kesitsel tasarım Imai-Keele duyarlılık ihtiyacı (CSR §16.1); H2 TOST eksikliği (CSR §11.2.2 itirafı); H1 R̂=1.012-1.013 sıkı eşik üstü (CSR §14.1); multi-informant trifactor + LDS modellenmemesi (CSR §15.1.2); Bayesian meta-pooling eksikliği (CSR §15.1.1) | `docs/analiz_planlari/STATISTICAL-ANALYSIS-PLAN-PHASE-2.md` v1.1 (kapsam revizyonu); OSF Layer 3 amendment submit hedefi 2026-05-08 |

## Sapma Tipleri

- **Tip 1, trivial:** Paket sürümü, çıktı biçimi, font, tablo/şekil başlığı veya analitik sonucu değiştirmeyen uygulama ayrıntısı.
- **Tip 2, minor:** Kovaryat kodlama düzeltmesi, model yakınsama fallback'i, alt grup sunum biçimi veya aynı estimandı koruyan yöntemsel ikame.
- **Tip 3, major:** Birincil hipotez, estimand, outcome veya ana model ailesi değişikliği. Tip 3 sapmalar doğrulayıcı analiz olarak yorumlanmaz; keşifsel olarak etiketlenir.

## Kullanım Kuralı

Her analiz runner'ı veya rapor üretimi sonrasında, ön-kayıtlı planla yapılan uygulama arasında fark varsa bu tablo güncellenir. Boş bırakılmış küçük sapmalar bile yöntemsel şeffaflığı zayıflatacağı için Tip 1 değişiklikler de kayda alınır.
