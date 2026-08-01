# SR Protokolü — <KONU> (NSCLC)

> Önceden-kayıt belgesi. Sentez/alt-grup kararları burada **ön-taahhüt** edilir
> (HARKing'e karşı). Doldurulmadan F2 aramaya geçilmez.

## 1. Künye
- **Başlık:**
- **PROSPERO kayıt ID:** (ZORUNLU adım — kayıt yapılana dek `beklemede`; alınan ID
  buraya yazılır. Kayıt yapılamıyorsa gerekçe + alternatif kayıt ortamı belirtilir.)
- **Kayıt tarihi:**
- **Tarih / sürüm:**
- **Protokol sapmaları (PRISMA-P):** kayıt sonrası her değişiklik tarih + gerekçe
  ile burada listelenir; F8 sertifikası bu listeyi kayıt tarihine karşı denetler
  (planlanmamış sapma = SOFT bulgu → gerekçe veya düzeltme).

## 2. Gerekçe (arka plan)
- Klinik sorun + mevcut belirsizlik + bu derlemenin katkısı.

## 3. Araştırma sorusu — PICOTS
- **P (Popülasyon):** histoloji (adeno/skuamöz), evre (TNM), biyobelirteç
  (EGFR/ALK/ROS1/KRAS G12C/PD-L1 …), tedavi hattı (1L/2L+).
- **I (Müdahale):** ajan/modalite (ICI/TKI/kemoterapi/ADC/cerrahi/RT).
- **C (Komparatör):**
- **O (Sonuç):** birincil (ör. OS), ikincil (PFS/ORR/toksisite/QoL); tanımlar.
- **T (Zaman):** takip/yayın aralığı.
- **S (Ortam/Tasarım):** dahil edilen çalışma tipleri (RCT / gözlemsel …).

## 4. Uygunluk kriterleri
- **Dahil:**
- **Hariç:**
- **Dil/yayın türü sınırı:** (varsa gerekçe)

## 5. Bilgi kaynakları & arama
- Veritabanları: PubMed/MEDLINE, Embase (EPMC), Cochrane CENTRAL, ClinicalTrials.gov,
  kılavuz (NCCN/ESMO/ASCO).
- Gri literatür / snowballing: (evet/hayır + plan)
- Tam arama dizesi: → `02_search/<konu>_search_log.md`

## 6. Tarama süreci
- İki-bağımsız-tarayıcı (simülasyon) + anlaşmazlık çözümü.
- Dışlama neden kodları (PRISMA): tanımla.

## 7. Veri çıkarımı
- Çıkarılacak alanlar → `templates/04_extraction_template.csv`.
- Kaynak lokatörü (PMID/DOI + tablo/şekil) zorunlu.

## 8. Yanlılık riski (RoB)
- Araç: RCT→RoB 2 · gözlemsel→ROBINS-I · tanısal→QUADAS-2.

## 9. Sentez planı
- **Meta-analiz:** uygunsa model (rastgele/sabit), etki ölçüsü (HR/OR/RR),
  heterojenite (I²/τ²), yayın yanlılığı (funnel/Egger).
- **Uygun değilse:** SWiM narratif sentez.
- **Önceden-planlı alt-gruplar:** (belirteç/histoloji/hat) — post-hoc olanlar
  ayrıca işaretlenecek.

## 10. Kanıt kesinliği
- **GRADE** her birincil endpoint için.

## 11. Sınırlar
- Ham/hasta-düzeyi veri toplanmaz; IPD-meta kapsam dışı.
