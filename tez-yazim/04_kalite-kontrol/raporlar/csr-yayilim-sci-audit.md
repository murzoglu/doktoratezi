# CSR Didaktik Katman Yayılımı — Denetim Raporu (§6, §8–§17)

Tarih: 2026-07-13 · Kapsam: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` pilot-dışı bölümler · Durum: **yayılım tamam, tam render kullanıcı onayında**

Plan: `docs/superpowers/plans/2026-07-13-csr-didaktik-katman-yayilim.md`
Pilot: `tez-yazim/04_kalite-kontrol/raporlar/11-birincil-hipotez-sci-audit.md`

## Yapılan iş (bölüm × işlem)

| Bölüm | İşlem | Birim |
|---|---|---|
| §8 Yöntem | Hafif tutarlılık pass'i (Yöntem kutusu → mini-blok biçimi) | 10 relabel |
| §9 Tanımlayıcı | Tam mini-blok (STROBE / SMD / eksik veri) | 3 |
| §10 Psikometri | Tam mini-blok (α+ω / CFA / taban / değişmezlik / geçerlik) | 5 |
| §12 Aracılık/LPA/Ağ/Fayda [KEŞF] | Kutu koru+çerçevele + fresh | 5 |
| §13 Robustluk | Multiverse/TOST/RV/negatif-kontrol | 4 |
| §14 Bayesçi | BF-ROPE / MCMC | 2 |
| §15 Çok-informant [KEŞF] | 8 keşifsel teknik | 8 |
| §16 Sosyodemografik [KEŞF] | 5 kutu relabel + 4 fresh mini-blok | 9 |
| §6 Giriş | Anlatı-didaktik çerçeve (Şablon B) | 1 |
| §17 Tartışma | Anlatı-didaktik çerçeve (Şablon B) | 1 |

Bilinçli **kapsam dışı** (teknik yok / fizibilite-sınırlı / verdict): §1-5, §7, §9.3-9.4 yorum, §10.6 / §14.3 / §15.11 karar, §16.5/16.6/16.12/16.13 ("test edilemez"/"betimsel"/"boştu"/denetim), §18-23.

## Denetim sonuçları (izole eklemeler, 8c09f14 → HEAD)

- **R-literal / kanonik sayı koruması (HARD):** R-chunk imzası tüm yayılım boyunca **birebir sabit** (`N_CHUNKS=60`, `CHUNK_HASH=cbed6d5ae41d71c101fd6e023e11f462`). Hiçbir istatistik değeri/verdict/kod literali değişmedi. **PASS**.
- **Yapı bütünlüğü:** 321 net eklenen satır; 50 "Bilimsel soru" + 2 "Bölümün sorusu" + 65 "Yöntem & tatbik" (50 tam mini-blok + 15 §8/§16 relabel) + 50 "Nasıl değerlendirilir". Bold dengesi tam (0 dengesiz), 0 kaçak ATX başlık, code-fence dengeli (120 çit). **PASS**.
- **No-fabrication (axis A/B — HARD):** 0 yeni Pandoc `[@key]`; eklenen tüm yazar-yıl künyeleri baseline CSR'da zaten mevcut (Austin, De Los Reyes, Pinquart, Hu-Bentler, Marsh, Li, Rhemtulla, Cheung-Rensvold, Chen, Putnick-Bornstein, Terwee, Mokkink, Prinsen, Campbell-Fiske, Vehtari, Lakens, Simonsohn, Cinelli, VanderWeele...). **PASS**.
- **Türkçe imla (axis G — HARD):** izole eklemelerde `tr_sciaudit --strictness certification` → **BLOCKER YOK** (0 `decimal-dot-p-value`, 0 `encoding-error`, 0 "ve ark." kalıntı, 0 İng. ondalık-nokta p).
- **Konvansiyon:** yazar-yıl "ve diğerleri" (pilot gate dersi korundu, 0 "ve ark.").

## Advisory (blocker değil, kabul)

- `abbreviation-review` (91): ICC/IPTW/SEM/GGM/LPA/TOST/RV/AUC/DCA/BF vb. — hepsi §3 Kısaltmalar'da tanımlı.
- `sentence-long`/`paragraph-too-long` (24): teknik içerik yoğunluğu; blocker değil.
- `decimal-dot` (8): **tamamı bölüm-referansı** (§8.5, §11.5, §13.1, §15.5, §12.2, §16.3 ...) — yanlış-pozitif, gerçek ondalıklar virgüllü.
- `causal-overclaim` (1): §16.8'de relabel edilen **mevcut** kutunun gövdesinde (didaktik pass yalnız etiketi değiştirdi; içerik pre-existing) — kapsam dışı.

## Render

`quarto render` bu fazda çalıştırılmadı; render-güvenliği iki bağımsız kanıtla desteklenir: (1) R-chunk imzası byte-düzeyinde değişmedi (kanonik CSR zaten render ediliyordu), (2) eklenen markdown iyi-biçimli (bold dengesi + fence dengesi). Tam render kullanıcı onayı sonrası son adımdır.

## Karar

CSR didaktik katman yayılımı **HARD kapıların tamamından geçti**. Pilot §11 ile birlikte CSR'ın tüm teknik-taşıyan bölümleri (§8–§16) 3-parçalı didaktik mini-blok taşıyor; §6/§17 anlatı-didaktik çerçeveye kavuştu. `certified-final` yalnız tam `quarto render` (exit 0) + kullanıcının açık onayıyla verilir.
