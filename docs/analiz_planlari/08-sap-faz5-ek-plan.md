# Faz V Ek Plan — Artık İlişki Yüzeyi (Residual Association Surface)

**Sürüm:** v0.1 (2026-07-14)
**Kapsam:** SAP KISIM L (§136-141) — [KEŞİFSEL · POST-HOC]
**OSF katmanı:** Layer 6 (Open-Ended Registration amendment hedefi)
**Kanonik baz:** `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` rev 2 (DEĞİŞMEZ)
**Modül:** `R/64_phase5_residual_associations.R` · **Runner:** `scripts/R/58_phase5_residual_associations_audit.R` · **Test:** `tests/test_phase5_residual_associations.R` (PASS)
**Target:** `_targets.R` → `phase5_residual_results`

## 0. Epistemik statü ve kapanış ilişkisi

Bu faz, sapma tablosu (#4) ile ilan edilen **analitik kapanışın SONRASINDA, yazar talebiyle**
eklenen bütünleştirici bir keşif katmanıdır. **YENİ VERİ YOK; kanonik kilit DEĞİŞMEZ; H1-H5
confirmatory çekirdek DEĞİŞMEZ.** Tüm çıktılar korelasyoneldir; nedensel dil yasaktır. Çoklu
karşılaştırma her paragraf içinde BH-FDR ile ele alınır. HARKing yasağı gereği hiçbir bulgu
confirmatory prior'ı güçlendirmez.

**Kapanış (#4) ile tutarlılık:** Faz V bulgularının çoğu ya mevcut örüntüyü **doğrular** (§138
aşırı koruma gradyanı; kalabalıklık joint modelde bağımsız değil → #4'ün "kalabalık ampirik-null"
verdikti birleşik modelle teyit) ya da **bilgilendirici null**'dur (§136, §137 dolaylı etkiler,
§140). FDR-dayanıklı tek yeni ilişki §139'dur (eğitim farkı → reddetme) ve o da SES ekseninin
parçasıdır. Dolayısıyla Faz V, kapanışın "yeni confirmatory sinyal yok" sonucunu **geçersiz
kılmaz, teyit eder**; katkısı bütünleştirici çerçeveleme (özellikle §137 informant-transmisyon
darboğazı) ve birkaç türetilmiş/az-işlenmiş yüzeyin belgelenmesidir.

## 1. Analizler

### §136. Maternal depresyon → kardeş ilişkisi [Tier B]
- **Yöntem:** `beck_total` → `srq_ho_{warmth,status,conflict,rivalry}_mean`; ham Pearson r + `group_f`+`ses_latent` kısmi kontrollü standardize β; TOST(|r|=.10); BH-FDR (4 boyut).
- **Gerekçe:** H2 grup→SRQ null bulmuştu; farklı bir eksen (anne depresyonu) denenir.
- **Sonuç (kanonik):** 4 boyutun tümü FDR-null (en düşük p_bh=0,140, rivalry ham r=−0,14 p=0,035). Anne depresyonu bu örneklemde kardeş ilişki kalitesini sistematik yordamıyor.

### §137. İnformant transmisyon / b-yolu + reddetme-dışı mediasyon [Tier B]
- **Yöntem:** Her EMBU alt ölçeği için a (Beck→EMBU-P), b (EMBU-P→EMBU-C_idx | Beck), dolaylı a·b (1000-bootstrap yüzdelik %95 GA), c′; kovaryat anne_yas_z + ses_latent_z. R/23 yalnız reddetme'yi test etmişti → 4 alt ölçek.
- **Sonuç (kanonik):** Tüm dolaylı etkiler null (GA sıfır içerir). a-yolu sıcaklık −0,23 / reddetme 0,15 / karşılaştırma 0,21 (anlamlı) ama b-yolu tüm boyutlarda zayıf (|b|≤0,10, hiçbiri anlamlı değil). **Bulgunun çekirdeği:** anne öz-raporu (EMBU-P) → çocuk algısı (EMBU-C) transmisyonu boyutlar-arası zayıf; depresyonun ebeveynliğe etkisi çocuk algısına "geçmez" — bu, mediasyonların neden null çıktığını açıklar (kırılma b-yolunda).

### §138. Aşırı korumanın sosyo-demografik gradyanı [Tier B]
- **Yöntem:** Birleşik model `embu_p_asiri_koruma_mean` ~ anne_yas_z + ses_latent_z + kalabalik_indeksi_z + group_f (standardize β + %95 GA). Ek bivariate doğrulama: kullanılmamış prestij/sınıf eksenleri aile_isei08, aile_siops08 (Pearson), aile_egp7 (Spearman).
- **Gerekçe:** anne_yas (R/57 §120) ve ISEI gradyanı (R/52 §100) ile ÖRTÜŞÜR → doğrulama; kalabalik_indeksi birleşik focal katkı.
- **Sonuç (kanonik):** Birleşik modelde anne_yas β=−0,18 (p=0,004) + ses_latent β=−0,27 (p<0,001) sağlam; **kalabalik_indeksi bağımsız DEĞİL** (β=0,06 p=0,33 — bivariate r=0,175 age/SES ile açıklanıyor). Prestij/sınıf doğrulaması aynı yönde: aile_isei08 r=−0,17, aile_siops08 r=−0,17, aile_egp7 ρ=+0,15. Yorum: genç + düşük-SES → daha yüksek anne-bildirimli aşırı koruma; kalabalıklık ise bağımsız katkı sağlamaz.

### §139. Eşler-arası eğitim farkı → ebeveynlik [Tier C]
- **Yöntem:** `egitim_fark` → embu_p_reddetme/asiri_koruma (Pearson); cift_kazanc → reddetme (nokta-biserial); BH-FDR.
- **Sonuç (kanonik):** egitim_fark → reddetme r=0,166 (p_bh=0,030) — **Faz V'in FDR-dayanıklı tek yeni ilişkisi**; egitim_fark → aşırı koruma trend (r=0,11 p=0,086); cift_kazanc null. Eşler-arası eğitim uyumsuzluğu daha yüksek anne-bildirimli reddetme ile ilişkili.

### §140. Aynı-cinsiyet düad → kardeş ilişkisi [Tier C]
- **Yöntem:** `same_sex` (Aynı/Farklı) → srq_ho_* (Cohen d + t; TOST SESOI d=0.20).
- **Gerekçe:** H2 APIM yalnız age_gap moderatörünü almıştı; düad cinsiyet-kompozisyonu test edilmemişti.
- **Sonuç (kanonik):** warmth d=−0,22 (p=0,085; aynı-cins düadlar hafifçe daha yüksek sıcaklık, 3,31 vs 3,21) — eğilim düzeyinde, FDR-sonrası anlamsız (p_bh=0,339); diğer 3 boyut null.

### §141. BH-FDR ve kapanış-uzlaşması
- Paragraf-içi BH-FDR (§136 4 test, §139 3 test, §140 4 test). Toplam 11 testten **1'i FDR-dayanıklı** (§139 egitim_fark→reddetme). §137 ve §138 kendi model-aileleri içinde raporlanır.

## 2. Tez artefaktı haritası

| Belge | Konum | İçerik |
|---|---|---|
| Yöntem | `chapters/03_gerec_ve_yontem.qmd` keşifsel katman enümerasyonu | Faz V bir madde |
| Bulgular | `chapters/04_bulgular.qmd` §4.4.7 | Sayısal bulgu + tablo göndermesi, [KEŞİFSEL] |
| CSR | `docs/CLINICAL-STUDY-REPORT-FINAL.md` §16.16 + §16.2 kanıt matrisi satırı | Ayrıntılı rapor + CSV provenansı |
| Tartışma | `chapters/05_tartisma_ve_sonuc.qmd` keşifsel-katman paragrafı + sınırlılık | Yorum, "öneri/hipotez-üretici düzeyde" |

## 3. Sınırlılıklar
Kesitsel; korelasyonel; küçük etkiler (|r|/|β| ≤ 0,27); tek-merkez; baba ebeveynlik davranışı
ölçülmedi (§137 transmisyon yalnız anne→çocuk ekseni). Dış-validasyon gerektiren öneri düzeyinde.
