# Bölüm Finalizasyon Sertifikası

Durum: `certified-final` (Kapı 0–5 PASS; kullanıcı açık onayı 2026-07-25 alındı)

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | 03 — GEREÇ ve YÖNTEM |
| Bölüm başlığı | GEREÇ ve YÖNTEM |
| Üretim dosyası | `chapters/03_gerec_ve_yontem.qmd` |
| Hazırlık briefi | `tez-yazim/03_bolum-hazirlik/03_gerec-ve-yontem.md` |
| Sertifikasyon tarihi | 2026-07-25 |
| Önceki sertifika | `03-gerec-ve-yontem-sertifika-2026-07-16.md` (`certified-final`) |
| Yeniden sertifikasyon nedeni | Bölüm bu oturum dizisinde `/anlatim-zenginligi` ile 3.15–3.18 alt-başlıklarında düzenlendi (COREQ/trustworthiness izahı, açık bilim/ön-kayıt/HARKing izahı, etik onam-muvafakat + KVKK/GDPR psödonimleştirme izahı, LLM sınırlılık/insan-gözetimi izahı); 6 yeni referans eklenip referans kapısından geçirildi. |
| Sertifikasyonu uygulayan | Ona (Claude Opus 4.8) — Kapı 0–5 yeniden denetimi |
| Uygulama onayı | **Alındı** (2026-07-25) — `certified-final`'a yükseltildi. |

## Bu Oturumdaki Değişiklik Envanteri

`chapters/03_gerec_ve_yontem.qmd` (+ yardımcı dosyalar) üzerinde:

1. **§3.15 Raporlama Standartları ve Güvenilirlik:** COREQ 32-madde açılımı +
   üç COREQ alanı; trustworthiness'ın nicel geçerlik-güvenirliğin nitel karşılığı
   olarak çerçevelenmesi; Lincoln-Guba dört ölçütü izahı; Tracy big-tent; quote-ID
   gizlilik↔şeffaflık gerekçesi. (Kanıt bölgesi: 32/29/üçü sayıları + 5 atıf token'ı
   birebir korundu.)
2. **§3.16 Açık Bilim, Kayıtlılık ve Ön-Kayıttan Sapmalar:** OSF/prospektif ön-kayıt
   tanımı; ikincil-veri ön-kaydında koruyucu işlevin analiz kararlarına kayması
   (`@mertensKrypotos2019preregExisting`); doğrulayıcı/keşifsel tanımı; HARKing açılımı;
   yanlış-pozitif/iyimserlik gerekçesi (`@bakker2020preregQuality`).
3. **§3.17 Etik Hususlar:** Helsinki Bildirgesi + GCP izahı; çocuk onam/muvafakat
   (assent) yapısı ve çocuğun reddine öncelik (`@hesterMiner2024consentAssent`);
   KVKK/GDPR psödonimleştirme≠anonimleştirme, kimliklenebilirlik spektrumu
   (`@joo2023deidentification`). (Kanıt bölgesi: tarih/protokol/karar no/kurum/yaş
   birebir korundu.)
4. **§3.18 Yapay Zekâ Destekli Araç Kullanımı:** LLM tanımı; hallüsinasyon/alan-bilgisi
   sınırlılık gerekçesi ve şeffaf belgeleme (`@bell2023writeAlgorithm`); insan-gözetimi
   ve araştırmacı sorumluluğu (`@helmy2025tenRulesGenAI`). (Kanıt bölgesi: olgusal
   AI-kullanım/PII-aktarılmama beyanları birebir korundu.)
5. **Kapı 4 düzeltmesi:** `chapters/00b_kisaltmalar.qmd` içine `GCP` ve `LLM`
   kısaltmaları alfabetik konumlarına eklendi (kısaltma tutarlılığı).

Değişen dosyalar (git diff --stat): `03_gerec_ve_yontem.qmd` (+62/−…),
`00b_kisaltmalar.qmd` (+2), `references/references.bib` (+6 girdi, bu oturumda
yalnız bu 6; diğer bib değişiklikleri önceki oturum çalışmasıdır),
`referans-denetim-ledgeri.md` (+6 `cite-ok` satırı).

## Kapı Sonuçları

| Kapı | Ad | Sonuç | Kanıt |
|---|---|---|---|
| 0 | Kapsam ve Hassasiyet Sınırı | **PASS** | Bölüm dosyası + brief + resmi kaynak manifesti mevcut; PII taraması temiz (ham veri/transcript/credential/TC-no yok; yalnız olgusal kurum adı ve yöntem metni). |
| 1 | Derin Literatür ve Künye Evreni | **PASS** | Bölümdeki 89 benzersiz atıf token'ının tamamı `references.bib`'te tanımlı (orphan-citation yok); bu oturumda eklenen 6 yeni atıf tam-metinle doğrulanıp `cite-ok`. |
| 2 | Tam Metin, Zotero ve Bağlam | **PASS** | `bib_hygiene` HARD atıflı-tanımsız (yok) · yakın-dup (yok); `thesis_semantic` bib-dup gerçek-dup (yok); 6 yeni atıf Zotero'ya pin'lendi (itemKey KENXR2WZ, ZMSHFXGU, 5MUQN8GI, I25D7FQV, XT243I4Q, K49X7HZG). |
| 3 | Metin, Kılavuz Uyumu, İçerik Sadakati | **PASS** | `galileo_overclaim_judge` 0,12 (causal_drift=false, cherry_pick=false); `galileo_harking_judge` 0,34 (post_hoc_as_prior=false); bölüm `thesis.qmd` satır 24'te dahil; alt-başlık claim↔kaynak eşleşmeleri tam-metinle teyit. |
| 4 | Türkçe İmla, Akış, Terminoloji | **PASS** | `tr_corpus_audit all --fail-on blocker` **EXIT 0** (0 blocker); GCP+LLM kısaltma tutarlılığı düzeltildi; `galileo_coherence` warning (tek doğal geçiş: nicel ölçek→nitel görüşme sınırı, §21↔22; advisory, dokunulmadı). |
| 5 | AI-Reliability, Repo Invaryant, Render | **PASS** | `r_generator_literal_audit` (K5-LIT-01) **PASS** (gömülü literal yok); `quarto check` tüm bileşen OK; bölüm render **EXIT 0** ("Output created"), citeproc bibliyografya hatasız (6 yeni atıf dahil çözüldü). |

## Advisory Notlar (teslim-engelleyici değil)

- **`galileo_judge` groundedness 0,42 / hallucination_risk 0,56 (advisory):** Judge'un
  işaretledikleri çalışmanın kendi olgusal tasarım verileridir (241 aile, 482 katılımcı,
  saha tarihleri, HbA1c n=39). Bunlar kanonik veri kilidinden gelen birincil gerçeklerdir,
  dış-atıf gerektirmez. LLM-judge advisory kademedir; AGENTS.md gereği HARD kapı asla
  LLM-yargısına bağlanmaz.
- **`H-TRANS` / `H-BRAK` (advisory):** Geçiş belirteci seyrekliği ve parantetik atıf
  oranı; yöntem bölümü için beklenen profil, blocker değil.
- **`galileo_coherence` warning (§21↔22):** Nicel ölçekler→nitel görüşme rehberi
  tematik geçişi; doğal bölüm-içi sınır, bu oturumda dokunulmadı.

## Numeric-Integrity ve Kanıt Bölgesi Beyanı

Bu oturumun tüm düzenlemeleri anlatım/izah katmanındadır. Hiçbir sayısal sonuç
(istatistik, tarih, protokol kodu, örneklem sayısı, yaş aralığı) değiştirilmemiş;
her alt-başlıkta kanıt bölgesi (sayılar + mevcut atıf token'ları) deterministik diff
ile korunmuştur. Eklenen 6 atfın hiçbiri gömülü literal taşımaz; K5-LIT-01 temizdir.

## Nihai Karar

**Kapı 0–5: 6/6 PASS.** Kullanıcı açık onayı 2026-07-25 tarihinde alınmış ve bölüm
`certified-final` statüsüne yükseltilmiştir. Bu statü, bölümün sonraki bir içerik
düzenlemesine kadar geçerlidir; kanıt bölgesini (sayı/istatistik/atıf) etkileyen her
yeni değişiklik yeniden sertifikasyon gerektirir.
