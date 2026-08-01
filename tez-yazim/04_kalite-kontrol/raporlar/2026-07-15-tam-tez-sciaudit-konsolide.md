# Tam Tez sci-audit — Konsolide Rapor (7 Eksen)

**Tarih:** 2026-07-15
**Kapsam:** Tüm tez metni — `chapters/00a–00c`, `01–07_*.qmd` + `docs/CLINICAL-STUDY-REPORT-FINAL.md`
**Protokol:** `.claude/skills/t1dm-tez-rehberi/references/manuskript-denetimi-sciaudit.md` (A–G, 7 eksen)
**Yapılandırma:** `.claude/sci-audit.local.md` (`gate_unsourced_numeric: true`, `gate_tr_pvalue_dot: true`)
**Araçlar:** `bib_hygiene.py`, `claim_certification.py`, `csr_numeric_trace_audit.py`, `csr_causal_label_audit.py`, `karma_ledger_check.py`, `tr_corpus_audit.py`

---

## Yönetici Özeti

| Sonuç | Sayı |
|---|---|
| 🔴 **BLOCKER** (teslim engeli) | **0** |
| 🟠 **MAJOR** (teslim öncesi düzeltilmeli) | **0** |
| 🟡 **WARNING / advisory** (stil/isteğe bağlı) | 52 (tümü değerlendirildi; eylem gerekmez) |

**Karar: Tez 7 eksende de teslim engeli taşımıyor.** Tüm sert kapılar (referans çözünürlüğü,
claim grounding, istatistik iç-tutarlılığı, halüsinasyon sinyalleri, raporlama kılavuzu uyumu,
AI-şeffaflık, Türkçe imla/p-değeri) TEMİZ geçmiştir. Kalan bulgular ya deterministik tarayıcı
false-positive'leri ya da bilinçli teslim-aşaması alanları ya da isteğe bağlı retorik önerilerdir.

---

## Axis A — Referans Bütünlüğü ✅ TEMİZ

- `bib_hygiene.py`: **HARD=0**.
- **286/286 DOI** geçerli/çözünür; uydurma veya yanlış künye yok.
- Ledger çaprazı: tezde atıfı olup ledger'da olmayan **8 kaynak** `unverified` işaretli
  (kanonik metodoloji kaynakları — hamaker2015clpm, steyerbergVergouwe2014 vb.; bib'de doğrulandı).
  → **WARNING** (blocker değil; ledger tamamlama teslim öncesi opsiyonel).

## Axis B — Claim Grounding ✅ TEMİZ

- `claim_certification.py`: **WARN** (yüksek-riskli eşleşmeyen = 0).
- Tez bulgular: **169 iddia / 168 kaynağa bağlı**.
- CSR'de 7 "high-risk unsourced" işareti → tümü dış-literatür sayıları (atıflı); **yüksek-riskli
  eşleşmeyen iddia = 0**.

## Axis C — İstatistik İç-Tutarlılığı ✅ TEMİZ

- `csr_numeric_trace_audit.py`: CI kapsama **0 sorun**, p-eşiği **0 çelişki**.
- 1 minor SEM anotasyonu (`04_bulgular.qmd:394` — DM-grup dyad CFA: CFI=0,984 vs SRMR=0,254).
  Kaynak `h5_dyadic_cfa_fit_measures.csv` ile doğrulandı: gerçek model çıktısı (n=120, tekile-yakın
  matris). → **WARNING** (doğru değer; blocker değil).
- Cuijpers2015 düzeltmesi doğrulandı: CSR `g=0,29` / `g=0,34` (PMID 41707889 abstract ile birebir);
  hatalı `g=0,40` kaldırıldı, tezde bulunmadığı teyit edildi.

## Axis D — Halüsinasyon Sinyalleri ✅ TEMİZ

- `csr_causal_label_audit.py`: causal_revise=**0**, label_errors=**0**.
- 11 nedensel-inceleme satırı → tümü `[KEŞİFSEL]` etiketleri altında (false-positive).
- 12 "aşırı-kesinlik" sinyali → tümü kesinliği YADSIYAN ifadeler (false-positive).
- Atıfsız yöntem / checksum ihlali: yok.

## Axis E — Raporlama Kılavuzu ✅ TEMİZ

- `karma_ledger_check.py`: **0 bulgu**.
- **15/15 kılavuz öğesi** mevcut: STROBE, COREQ, JARS-Mixed, SRQR, güç analizi, eksik veri,
  etik onay (09.2023.201), ön-kayıt, etki büyüklüğü+CI, FDR, refleksivite, bilgi gücü,
  Lincoln-Guba, açık bilim, AI/LLM beyanı.

## Axis F — AI Şeffaflık ✅ TEMİZ

- **AI/LLM kullanım beyanı mevcut ve içerikli** (`03_gerec_ve_yontem.qmd:208`): kullanım kapsamı
  (yazım/düzenleme/tutarlılık ön-denetimi), araştırmacı sorumluluğu, KVKK/gizlilik (ham veri
  aktarılmadı) net biçimde belgelenmiş.
- **Placeholder envanteri — tümü bilinçli teslim/savunma-aşaması alanları:**
  - `00a`: `{İMZA}`, `{TARİH}`, `{SAVUNMA TARİHİ}`, `{Kurum}`, `{Enstitü Müdürü}`, `{TİK üyeleri}`, `{YIL}`
  - `06`: `{Doğum yeri}`, `{gg.aa.yyyy}`, hazırlanan makale künyeleri (yayım aşamasında tamamlanır)
  - `07`: `[TARANMIŞ BELGE EKLENECEK]` — etik onay + ölçek izin belgeleri (fiziksel teslim öncesi)
  - `06:5`'te açıkça belgelenmiş: "`{…}` alanları öğrenci tarafından doldurulur."
  - `{.unnumbered}` = Quarto attribute (placeholder değil).
- **Sızıntı bulunmayan kod/metin placeholder'ı: `chapters/` gövdesinde 0** (TODO/FIXME/TBD yok).

## Axis G — Türkçe İmla / Yazım ✅ TEMİZ

- `tr_corpus_audit.py all`: **HARD=0**, SOFT=31, advisory=21.
- **Ondalık virgül tutarlı:** TR bölümlerde istatistik değerleri virgüllü (`β=0,16`, `0,29`);
  yanlış nokta-ondalık **yok**. Nokta içeren 35 sayı incelendi → tümü meşru: binlik ayracı
  (`108.300`, `1.435`), yazılım sürümü (`3.01`), tarih (`06.01.2023`), bölüm ref (`§4.4.6`).
- **p-değeri nokta ihlali: 0** (blocker kriteri temiz).
- **EN SUMMARY nokta tutarlı:** İngilizce özette virgül-ondalık yok; `0.16` düzeltmesi doğrulandı.
- SOFT (31): çoğu kısaltma-tarayıcı false-positive (`H1`–`H5`, `DM-`, `KEŞİFSEL`,
  `CLINICAL/STUDY/REPORT/FINAL` = dosya adı parçaları); 4 başlık-derinliği (§ genel bilgiler L4)
  ve `E-`/`JARS-` kırpma artefaktları. → stilistik, blocker değil.
- advisory (21): geçiş belirteci sıklığı, parantetik/anlatısal atıf dengesi, raportör-fiil
  çeşitliliği. → isteğe bağlı retorik iyileştirme.

---

## Teslim Öncesi Opsiyonel İyileştirmeler (blocker değil)

1. Ledger'daki 8 `unverified` metodoloji kaynağını doğrulanmış statüye taşımak (Axis A).
2. `02_genel_bilgiler` L291–323 düzey-4 başlıkları düzey-3'e indirmek (Marmara başlık derinliği).
3. Advisory retorik önerileri (anlatısal atıf dengesi, geçiş belirteçleri) seçmeli uygulamak.

Bu maddeler teslimi engellemez; tez mevcut haliyle 7-eksenli sci-audit'i geçmektedir.
