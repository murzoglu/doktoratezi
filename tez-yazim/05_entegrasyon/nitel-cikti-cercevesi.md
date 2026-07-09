# Niteliksel Çıktı Çerçevesi

Sürüm: 1.0 · 2026-07-06 · Kapsam: Tezin **nitel kolu** ile ilgili her çıktının
(yöntem, bulgular, joint display, tartışma, ekler) yazımı, denetimi ve biçimi.

Bu belge nitel çıktıları **`niteliksel-arastirma-rehberi-t1dm` skill'inin
sağladığı çerçeve dahilinde** yapılandırır. Karma yöntem entegrasyonunun (joint
display) planı `nitel-nicel-joint-display-plan.md`'dedir; bu belge o planın
**metodolojik/biçim çerçevesi** ve nitel kanıtın güvenli aktarım sözleşmesidir.

---

## 0. Otorite zinciri (hangi belge neyi belirler)

Bu dosya **nitel kol çıktı çerçevesinin** tek kanonik yeridir; klasör
tek-otorite haritası: `05_entegrasyon/README.md`.

| Katman | Belge | Ne belirler |
|---|---|---|
| Skill çerçevesi | `niteliksel-arastirma-rehberi-t1dm` (SKILL.md + `references/`) | RTA 6 faz, bilgi gücü, COREQ/SRQR/JARS-Qual, IRR tartışması, refleksivite, yorumlama, jüri savunması, T1DM-spesifik uyarlamalar. **Birincil metodoloji çerçevesi.** |
| Biçim | `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` (Bölüm 7) | Nitel bulguların tezdeki **biçimi** (tema/alt tema/rol, anonim alıntı, kanıt ayrımı). |
| Karma plan | `05_entegrasyon/nitel-nicel-joint-display-plan.md` | Joint display tablo alanları ve ilişki türü etiketleri. |
| Süreç talimatnamesi | `00_kaynak-kurallari/talimatname-claude-code.md` | Rota, KVKK sınırı, dmnitel kapıları. |
| Kritik kaynaklar | `06_kritik-kaynaklar/README.md` (Nitel Repo Koşullu Kaynakları) | Hangi nitel dosya nerede, hangi erişim sınırıyla. |

**Kural:** Nitel metodoloji sorusu (neden RTA, kaç dyad, kappa zorunlu mu,
tema=anlamlandırma mı) → `niteliksel-arastirma-rehberi-t1dm` skill birincildir.
Karma yöntem entegrasyonu (joint display, GRAMMS, MMAT) bu tez-yazim repo
belgeleri + `t1dm-tez-rehberi/references/karma-yontem.md` ile yürür.

---

## 1. Nitel kolun kimliği (bağlam)

- **Tasarım:** Nitel tanımlayıcı + fenomenolojik duyarlılık, multi-informant
  **triad** (anne + T1DM'li çocuk + sağlıklı kardeş), Braun-Clarke **Refleksif
  Tematik Analiz (RTA)**, COREQ-uyumlu.
- **Örneklem (nitel kol):** **7 aile × 3 = 21 görüşme** (aile kodları 011, 014,
  019, 020, 026, 201, 202). ⚠️ Bu nitel koldur; karma tezin nicel kolu ayrıdır
  (241 aile, R pipeline). İkisi **karıştırılmaz**.
- **Tema yapısı:** **Tez = 4 makro tema. Journal = 6 tema.** Değiştirilebilir
  değil; yeniden yazımdan önce hedef çıktı netleştirilir.
- **Nitel kolun teze rolü:** H5 dyadic concordance'ın (anne ↔ çocuk algı uyumu)
  **niteliksel boyutu** — nicel uyum *hangi* boyutlarda uyum/uyumsuzluk olduğunu,
  nitel kol **neden ve nasıl**'ı yanıtlar.

---

## 2. Teze giren güvenli nitel çıktılar

Teze yalnız araştırmacı-onaylı **anonim/türetilmiş** çıktı girer. Kaynak
haritası (paired nitel repo: `/mnt/thunderbolt/workspaces/T1DM Niteliksel`):

| Çıktı | Kaynak | Tezde kullanım |
|---|---|---|
| Kanonik nitel sonuç raporu | `docs/niteliksel/qualitative_canonical_results_report.md` (doktoratezi kopyası) | Nitel kolun **varsayılan temsil kaynağı** (Bulgular). |
| Aktarım kaynağı (hash eşli) | Nitel repo `06_manuscript_outputs/qualitative_canonical_results_for_doktoratezi.md` | Doktoratezi kopyasıyla hash mutabakatı. |
| Codebook | Nitel repo `03_analysis/codebook/codebook_v2.md` (kanonik; v3.csv draft) | Tema/kod tanımı. |
| COREQ 32 madde | Nitel repo `03_analysis/methodology/coreq_32_completed.md` | Gereç ve Yöntem + Ekler. |
| Audit trail | Nitel repo `03_analysis/methodology/audit_trail.md` | Yöntem güvenilirlik izi. |
| Positionality (OM/BA) | Nitel repo `03_analysis/methodology/positionality_*.md` | Refleksivite / konum bildirimi. |
| LLM kullanım beyanı | Nitel repo `03_analysis/methodology/llm_use_statement.md` | Yöntem + AI şeffaflık. |
| Triadik matrisler | Nitel repo `04_triadic_matrices/` | Rol karşılaştırması (anne/çocuk/kardeş). |
| Nitel AI-reliability | Nitel repo `07_reports/ai_reliability_qualitative_canonical_results_report.md` | Quote-ID/code-ID/copy-parity; ham alıntı yok. |

**Varsayılan olmayan:** Ham transcript, demografi satırı veya geniş nitel repo
yeniden taraması. Bunlar teze girmez, dış araca gönderilmez.

---

## 3. Alıntı bütünlüğü ve negatif vaka — transkript AÇMADAN

- **Alıntı bütünlüğü** transcript açarak değil, paired nitel repoda
  `./dmnitel check-quotes --source <deidentified-source> --quotes <quotes.csv>`
  ile denetlenir.
- **Negatif/alternatif vaka** `./dmnitel find-negative-cases --coded-data
  <coded.csv> --theme "<tema>"` ile taranır.
- **COREQ metin içi kanıt** `./dmnitel audit-coreq --methods <methods.md>
  --results <results.md>` ile.
- **Codebook tutarlılığı** `./dmnitel lint-codebook <codebook.csv>` ile.
- **Triadik matris** `./dmnitel build-triadic-matrix --coded-data <coded.csv>
  --output 04_triadic_matrices/<name>.csv` ile.

Teze yalnız araştırmacı onaylı **anonim alıntı (aile no + rol etiketi)** veya
**quote ID** girer; ham alıntı dökümü yapılmaz (Marmara format talimatnamesi
Bölüm 7).

---

## 4. Skill'in bağlayıcı ilkeleri (yazımı yönlendiren)

`niteliksel-arastirma-rehberi-t1dm` 8 ilkesinden tez yazımına doğrudan yansıyan:

1. **Nitel ≠ küçük-örneklemli nicel.** Nitel kol anlam/deneyim/süreç/bağlam
   yanıtlar; "az katılımcılı nicel" olarak çerçevelenmez.
2. **RTA seçimi metodolojiktir** — gerekçesi Yöntem bölümünde açık yazılır
   (çoklu-vaka örüntü + dyadic uyum → RTA).
3. **"Saturasyon" RTA'da kullanılmaz** — yerine **bilgi gücü** (Malterud) veya
   **data sufficiency**. Yöntem/raporlamada "doygunluğa ulaşıldı" ifadesi yazılmaz.
4. **IRR otomatik gereklilik değildir** — jüri/IRB isterse uzlaşma stratejisi:
   anlaşmazlık çözümünü dokümante et + opsiyonel **Krippendorff α / Gwet AC1**
   (kappa paradoksuna karşı) + raporlamanın anlamını açıkla.
   `./dmnitel` çıktıları ve nitel repo `outputs/qualitative/irr/` bu kararı besler.
5. **Refleksivite süreçtir** — konum bildirimi + refleksif günlük + audit trail;
   Yöntem'de özet, Ekler'de örnek.
6. **Etik dinamiktir** — process consent; anonimleştirme kompozit pseudonym +
   redaction + sentetik tipikleştirme ile (KVKK özel nitelikli sağlık + çocuk
   verisi).
7. **LLM-destekli kodlama tek katman değildir** — birincil analiz LLM'e
   devredilmez; halüsinasyon kontrolü + OSF prompt zinciri arşivleme; LLM Use
   Statement (nitel repo `llm_use_statement.md`).
8. **Tema = "central organizing concept"** — katılımcı sözünün başlığı değil;
   "şu üç katılımcı söyledi" sayması tema değildir.

---

## 5. Nitel bölümlerin biçimi (Marmara kılavuzu)

Nitel çıktı da resmi Marmara biçimine uyar
(`marmara-tez-formati-talimatnamesi.md`):

- **Gereç ve Yöntem:** tasarım (nitel tanımlayıcı + RTA), örneklem (7 aile triad),
  veri toplama (yarı-yapılandırılmış + çocuk-uyumlu), analiz (RTA 6 faz),
  güvenilirlik (Lincoln-Guba/Tracy), etik (etik kurul tarih+sayı → Ekler),
  refleksivite, COREQ atfı. Alt başlıklarla yapılandırılabilir.
- **Bulgular:** 4 makro tema; tema/alt tema/örüntü/rol karşılaştırması; yorumsuz;
  anonim alıntı/quote ID; şekil (tema haritası) alt başlığı **altta**, tablo
  (triadik matris) başlığı **üstte** (Bölüm 1.6–1.7).
- **Tartışma ve Sonuç:** triadik yorum, dyadic uyum/uyumsuzluğun neden/nasıl'ı,
  negatif vaka, refleksif sınırlar; alt başlıksız (şablon kuralı).
- **Ekler:** COREQ tablosu, codebook, audit trail, LLM beyanı, etik onay.

---

## 6. Karma yöntem entegrasyonu (joint display)

- Nicel H1–H5 ile nitel triadik temalar **aynı tabloda** ama **kanıt türü
  karıştırılmadan** (`nitel-nicel-joint-display-plan.md`).
- İlişki türü açık etiketlenir: **uyum / tamamlayıcılık / ayrışma / açıklayıcı
  genişleme**.
- Joint display Bulgular'da **yorumsuz**, Tartışma'da yorumlu.
- H5 nicel (ICC + Bland-Altman + RSA + Common Fate + k-coefficient) *hangi*
  boyutta uyum/uyumsuzluk; nitel kol *neden/nasıl* — biri diğerinin doğrulaması
  gibi yazılmaz.
- Karma entegrasyon derinliği: `t1dm-tez-rehberi/references/karma-yontem.md`
  (GRAMMS, MMAT, Creswell convergent parallel).

---

## 7. Devir noktaları (bu çerçeve DIŞINDA)

| Soru | Devir |
|---|---|
| RTA fazı, kodlama, tema, kaç dyad, IRR, jüri savunması | → `niteliksel-arastirma-rehberi-t1dm` skill (`references/`) |
| Karma yöntem joint display / MMAT / convergence | → `t1dm-tez-rehberi/references/karma-yontem.md` |
| EMBU-C CFA / ICC-Bland-Altman nicel (H5) | → `t1dm-tez-rehberi` (KISIM IV/V, `h5-diadik-tutarlilik.md`) |
| Nitel iç veri denetimi (quote/codebook/COREQ/matris) | → paired nitel repo `./dmnitel` komutları |
| Nitel metin adli denetimi + Türkçe imla (COREQ/SRQR uyumu, AI-şeffaflık, imla) | → `sci-audit` plugin (axis E `--type coreq/srqr`, axis F, axis G) |
| Dış literatür (nitel metodoloji referansı: Braun-Clarke, Malterud, Tracy) | → Evidentia (`01_mimari/evidentia-entegrasyon-cercevesi.md`) |
| Tez / tema haritası render | → `carbon-quarto-scientific` / `carbon-html-report` |

---

## 8. KVKK sınırı (nitel kol — en yüksek hassasiyet)

Ham görüşme metinleri özel nitelikli **sağlık + çocuk** verisidir (KVKK).

- Korumalı alanlar (paired nitel repo): `01_raw_data/`,
  `02_processed/transcripts/`, `01_deidentified/`, `00_raw_locked/`, `.remember/`.
- Bu alanlardan satır düzeyi içerik, aile düzeyi hassas detay, ham alıntı,
  demografi satırı, onam/protokol kişisel içeriği **bu tez-yazim reposuna
  kopyalanmaz, bağlama dökülmez, memory'ye yazılmaz, hiçbir harici MCP/RAG/
  connector'a gönderilmez**.
- İsim, doğum tarihi, adres, imzalı onam metni veya aile-düzeyi demografik satır
  raporlamada **kullanılmaz**; yerine aile numarası + rol etiketi.
- Karma sentezde yalnız de-identified tema/codebook/COREQ/audit-trail çıktıları
  ve araştırmacı onaylı anonim alıntılar kullanılır.

Her harici AI/MCP kullanımı `./dmnitel log-ai-use` ile kaydedilir; `--data-type`
daima "anonim/türetilmiş"; ham/kimliklenebilir bayrakları `no` kalır (kod
düzeyinde zorlanır).
