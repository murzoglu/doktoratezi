# T1DM Niteliksel Tez — Yol Haritası v1

**Hazırlanma:** 2026-05-04
**Skill:** `niteliksel-arastirma-rehberi-t1dm` (Faz 0-3 karar akışı uygulandı)
**Kapsam:** Mevcut çalışmaların envanteri + sıradaki 4 faz (Kalite Pekiştirme → Bölüm Yazımı → Format → Yayım & Savunma)

---

## A. Mevcut Durum Envanteri

### A.1 Tasarım sabitleri (doğrulanmış)

| Boyut | Değer | Kaynak |
|---|---|---|
| Tasarım | Niteliksel tanımlayıcı + fenomenolojik duyarlılık + multi-informant family | `02_processed/cleaned_text/thesis_qualitative_cleaned_current.md` |
| Birim | **Triad** (anne + T1DM çocuk + sağlıklı kardeş) — *dyad değil* | Aynı |
| Örneklem | 7 aile × 3 katılımcı = **21 görüşme** | Aynı |
| Aile kodları | 011, 014, 019, 020, 026, 201, 202 (tümü DM; "kontrol" niteliksel kolda yok) | `01_raw_data/interviews_docx/` |
| Saha | Marmara Üniv. Hastanesi Çocuk Endokrinoloji polikliniği | Method metni |
| Görüşme süresi | 15-25 dk/birey, 40-70 dk/aile | Method metni |
| Analiz çerçevesi | Braun-Clarke refleksif tematik analiz | Method metni |
| Yazılım | Manuel — MS Word + Excel (renk kodlama) | Method metni |
| Analist | OM (birinci) + BA (gözlemci + critical friend) | Method metni |
| Etik onay | DM Parenting Attitudes Ethics Protocol 2023-02 | `01_raw_data/ethics_protocol/` |
| Tema mimarisi | 6 tema (journal yapısı) / 4 makro tema (tez yapısı) | `03_analysis/triadic_matrices/` + cleaned text |

### A.2 Tamamlanmış işler ✅

| # | Çıktı | Yer | Durum |
|---|---|---|---|
| 1 | Etik protokol (2023-02) | `01_raw_data/ethics_protocol/` | Onaylı |
| 2 | Görüşme rehberi (anne/hasta/kardeş) | `01_raw_data/interview_guides/` | Tamam |
| 3 | Demografik form | `01_raw_data/demographics/` | Tamam |
| 4 | 21 görüşme transkripti (DOCX) | `01_raw_data/interviews_docx/family_*/` | Tamam |
| 5 | Birleştirilmiş transkript (Markdown) | `02_processed/transcripts/all_transcripts_merged.md` | Tamam |
| 6 | Cleaned thesis text (~12k kelime) | `02_processed/cleaned_text/thesis_qualitative_cleaned_current.md` | YÖNTEM bölümü ileri taslak |
| 7 | Codebook v1 (24 kod, 5 kategori) | `03_analysis/codebook/codebook_draft_v1.md` | İlk geçiş |
| 8 | COREQ-uyumlu Method iskeleti | `03_analysis/methodology/methodology_skeleton_coreq.md` | Skeleton — doldurulmamış |
| 9 | 6 tema triadic matrix v3 | `03_analysis/triadic_matrices/theme_0[1-6]_*.docx` | Tamam |
| 10 | Theme comparison spreadsheet | `03_analysis/spreadsheets/` | Tamam |
| 11 | Mother thematic memo | `03_analysis/thematic_memos/mother_theme_memo.docx` | Tamam |
| 12 | Pediatric Diabetes manuscript v2 (Results+Discussion) | `04_manuscripts/journal_pediatric_diabetes/` | Journal-ready |
| 13 | Refleksif notlar | Method metninde *anılıyor* | Ayrı dosya yok ⚠️ |
| 14 | Critical friend (BA) süreci | Method metninde *uygulanmış* | Audit trail yok ⚠️ |

### A.3 Kritik eksikler (skill referansı + neden önemli)

| # | Eksik | Skill Ref | Neden Kritik |
|---|---|---|---|
| E1 | "Tematik doygunluk" kavramı methodda kullanılmış (`İlke 3` ihlali) | `02-orneklem-bilgi-gucu.md` | Braun-Clarke 2021 RTA'da saturation eleştirilir; jüri "doygunluğu nasıl ölçtün" diye sorabilir → **Malterud information power**'a çevirilmeli |
| E2 | COREQ 32-madde **doldurulmuş** checklist yok | `assets/coreq-32-madde-tr.md`, `scripts/coreq-checklist-validator.py` | Yöntem bölümünün her maddenin hangi paragrafta karşılandığını gösteren tablo şart |
| E3 | Positionality statement ayrı dosya değil | `assets/positionality-tr.md` | Refleksivite süreçtir; tek paragrafta gömülü kalmamalı (`İlke 5`) |
| E4 | Refleksif günlük örnekleri / şablonu yok | `assets/refleksif-gunluk-sablonu-tr.md` | Method metninde anılan "refleksif notlar" görünür kanıt yok → audit trail boşluğu |
| E5 | Audit trail dokümantasyonu yok | `assets/audit-trail-log-tr.md` | OM-BA tartışma sürecinin tarihli kaydı yok; codebook revizyon geçmişi yok |
| E6 | KVKK Veri Yönetim Planı yok | `09-etik-kvkk-refleksivite.md` | Özel nitelikli sağlık verisi + çocuk verisi → DMP zorunlu |
| E7 | Tek-kodlayıcı + öznellik savunma argümanı yok | `11-yazim-ve-jurinin-soracaklari.md` (Q14) | Jüri savunmasında muhtemel itiraz; Braun-Clarke epistemik tutarsızlık çerçevesi hazırlanmalı |
| E8 | Triadic methodology literatürü zayıf | `12-t1dm-tezi-spesifik-uyarlamalar.md` | Method'ta "multi-informant family design" deniliyor ama Marshall, Pyett, Vaughn vd. atıfları yok |
| E9 | Tez Bulgular/Tartışma bölümleri tez formatında değil | — | Sadece journal manuscript var; tez 4-makro-tema yapısında ayrı yazım gerekli |
| E10 | Tez Giriş + Genel Bilgiler bölümleri yok | — | Marmara şablonunda zorunlu (3.2.3, 3.2.4) |
| E11 | Kaynakça taslağı yok | — | Marmara `references.bib` veya manuel format gerekli |
| E12 | Marmara şablon uyumluluğu kontrol edilmemiş | `05_references/thesis_guidelines/marmara_thesis_writing_guide.md` | Format reddi savunma takvimini geciktirir |
| E13 | LLM kullanım beyanı (Claude/GPT yardımcısı varsa) | `assets/llm-kullanim-beyani-tr.md` | Niteliksel analizde LLM kullanıldıysa OSF + tez beyanı şart |
| E14 | OSF kaydı / DOI yok | — | Açık bilim katmanı; aynı zamanda tez sonrası makale yayım gücü için |
| E15 | JARS-Qual + SRQR ek kontrol listeleri yok | `assets/jars-qual-kontrol-listesi-tr.md`, `assets/srqr-21-madde-tr.md` | COREQ tek başına yetmez; tamamlayıcı çerçeveler tartışma + tartışma kalitesi açısından |

### A.4 Methodda dikkat çeken karar noktaları

**Pozitif (savunulabilir):**
- ✅ Critical friend yaklaşımı (BA), inter-coder agreement zorlamaması — Braun-Clarke 2021 ile uyumlu
- ✅ Önlüksüz görüşme, klinik otoriteden uzaklaşma — power dynamics farkındalığı
- ✅ Saha notları + paralinguistik veri (BA) — multi-modal triangulation
- ✅ Triad → multi-informant triangulation argümanı doğru
- ✅ Member checking yerine **görüşme içi özetleme** kararı (sebep belirtilmiş)

**Risk noktaları (düzeltme gerekli):**
- ⚠️ "Veri doygunluğuna ulaşıldı" ifadesi — RTA epistemolojisiyle çelişir
- ⚠️ "Konsensüs üretmemek" doğru karar ama jüriye karşı reframe edilmeli
- ⚠️ "Müsait olunan ailelerle 7'de durdu" → ÖRNEKLEM KAPSAMI sınırı + bilgi gücü argümanı yapılmalı
- ⚠️ Codebook v1'in iteratif geçirildiği belge zinciri yok (codebook v2, v3 yok)
- ⚠️ "Yazılım kullanılmadı" gerekçesi metodolojik (data closeness) ama jüri "QDPX export, denetim izi" sorabilir → savunma argümanı hazırlanmalı

---

## B. Yol Haritası — 4 Faz

### FAZ A — Kalite Pekiştirme (2-3 hafta) **[Önce bunu]**

**Amaç:** Mevcut çalışmayı niteliksel araştırma raporlama standartlarına çek; eksik artefaktları üret. Tez yazımını başlatmadan önce metodoloji ve etik altyapı kapanmalı.

**Öncelikli paketler:**

| Paket | İş | Çıktı | Skill ref |
|---|---|---|---|
| A.1 | "Doygunluk" → "bilgi gücü" reframe | YÖNTEM bölümünde Malterud 5 boyut tablosu + 1 paragraf yeniden yazım | `02-orneklem-bilgi-gucu.md` |
| A.2 | COREQ 32-madde doldurma | `04_manuscripts/thesis/coreq_32_completed.md` (her madde + sayfa eşleştirme) | `assets/coreq-32-madde-tr.md` + `scripts/coreq-checklist-validator.py` |
| A.3 | Positionality statement (TR + EN) | `03_analysis/methodology/positionality_OM.md`, `_BA.md` | `assets/positionality-tr.md` |
| A.4 | Refleksif günlük örnekleri (n=3-5 örnek girdi) | `03_analysis/reflexive/journal_excerpts.md` (anonim) | `assets/refleksif-gunluk-sablonu-tr.md` |
| A.5 | Audit trail tablosu (codebook tarihi, kararlar, OM-BA tartışmaları) | `03_analysis/methodology/audit_trail.md` | `assets/audit-trail-log-tr.md` |
| A.6 | Codebook v2 (kategori birleştirme + tema-kod haritası) | `03_analysis/codebook/codebook_v2.md` | `04-rta-6-faz-derinlemesine.md` |
| A.7 | KVKK Veri Yönetim Planı | `01_raw_data/ethics_protocol/kvkk_data_management_plan.md` | `09-etik-kvkk-refleksivite.md` |
| A.8 | LLM kullanım beyanı (kullanıldıysa) | `03_analysis/methodology/llm_use_statement.md` | `assets/llm-kullanim-beyani-tr.md` + `06-llm-destekli-kodlama.md` |
| A.9 | Triadic methodology literatür ekleme | YÖNTEM'e Vaughn, Marshall, Pyett atıfları | `12-t1dm-tezi-spesifik-uyarlamalar.md` |
| A.10 | Jüri savunma argüman dosyası (taslak) | `03_analysis/methodology/defense_arguments.md` | `11-yazim-ve-jurinin-soracaklari.md` |

**Sıralama:** A.1 → A.6 → A.2 → A.3-A.5 paralel → A.7-A.10 paralel
**Bitmeden FAZ B başlatma:** Çünkü Bulgular bölümü COREQ'e ve doldurulmuş codebook'a anchor olmalı.

### FAZ B — Tez Bölüm Yazımı (4-6 hafta)

**Amaç:** Marmara şablonuna uygun, COREQ + JARS-Qual + Tracy big-tent kriterleri karşılayan tez metnini üretmek.

**Bölüm bazlı:**

| Bölüm | Anahtar içerik | Skill ref | Tahmini süre |
|---|---|---|---|
| B.1 — Giriş & Amaç | T1DM aile yükü literatürü; ana ve alt araştırma soruları | — | 1 hafta |
| B.2 — Genel Bilgiler | T1DM epidemiyolojisi + aile sistemleri teorisi (Bowen) + bakım yükü literatürü | `05_references/literature/` (zaten 11 PDF var) | 1.5 hafta |
| B.3 — Yöntem | A.1-A.10 çıktılarını entegre et; mevcut taslağı genişlet | `03-gorusme-protokolu-tasarim.md`, `04-rta-6-faz-derinlemesine.md` | 1 hafta (FAZ A çıktıları varsa) |
| B.4 — Bulgular | 4 makro tema yapısında — sağlıklı kardeş / anne ekseni dönüşümü / T1DM çocuk deneyimi / triadic karşılaştırma; her tema için **kalın betimleme + kod-tema-aile haritası** | `10-yorumlama-ve-yaygin-hatalar.md` | 2 hafta |
| B.5 — Tartışma & Sonuç | Bulguların literatürle diyaloğu + sınırlılıklar + aktarılabilirlik (transferability) çerçevesi + öneri | `10-yorumlama-ve-yaygin-hatalar.md` (kalın betimleme + analitik genelleme) | 1.5 hafta |
| B.6 — Türkçe + İngilizce Özet | Marmara şablonu (3.2.1, 3.2.2) | Marmara guide | 0.5 hafta |

**Bulgular yapısı kararı (kritik):**
Mevcut journal manuscript v2 = 6-tema yapısı. Tez ise 4-makro-tema önerilmiş. **REPO_CONTEXT.md uyarısı:** "Do not assume thesis and journal structures are interchangeable." → İki yapı arasında **netleştirilmiş bir mapping** gerekli (B.4 öncesi karar verilmeli).

### FAZ C — Format & Compliance (2-3 hafta, FAZ B sonu paralel)

| Paket | Çıktı | Kontrol |
|---|---|---|
| C.1 | Marmara şablonu uygulama (kapak, onay, beyan, içindekiler) | `marmara_thesis_writing_guide.md` |
| C.2 | Kaynakça (Marmara stilinde) | Anılan tüm kaynakların `references.bib` veya manuel listesi |
| C.3 | Ekler — görüşme rehberi, COREQ tablosu, codebook, demografik tablo, positionality, refleksif günlük örnekleri, audit trail | Marmara 3.2.9 |
| C.4 | Tablolar + şekiller (görsel kalite kontrolü) | Marmara 2.9 |
| C.5 | Yazım denetimi + akademik dil revizyonu (Türkçe APA 7) | Marmara 2.7 + 2.10 + 2.12 |
| C.6 | JARS-Qual + SRQR ek kontrol listeleri (savunma için) | `assets/jars-qual-kontrol-listesi-tr.md`, `assets/srqr-21-madde-tr.md` |

### FAZ D — Yayım & Savunma (paralel + son)

| Paket | İş | Anahtar |
|---|---|---|
| D.1 | OSF projesi açma + ön-kayıt sapma tablosu (retrospektif) | OSF page → tez bölümü "açık bilim" alt-başlığında belirtilebilir |
| D.2 | Pediatric Diabetes manuscript revizyonu | Tezdeki refleksif/COREQ artefaktlarla uyumlandırma |
| D.3 | Tez ön-savunma | Önceki yapılan ön savunma feedback'ini topla → düzelt |
| D.4 | Tez esas savunma | Defense argument dosyası (A.10) + slayt setleri |
| D.5 | Yayım stratejisi | (a) Pediatric Diabetes makale (mevcut), (b) Tez tabanlı 1-2 ek makale (sağlıklı kardeş odaklı; triadic comparison odaklı) |

---

## C. Hızlı Karar Noktaları (Kullanıcıya Sorular)

Aşağıdakiler yola çıkmadan önce netleşmeli:

1. **Tezin teslim takvimi nedir?** (Faz A-D toplam ~12-15 hafta gibi tahminim — sıkışık takvim varsa C ve D paralelleşmeli)
2. **OSF kaydı yapıldı mı, yoksa tez sonrası mı planlanıyor?**
3. **Pediatric Diabetes manuscript ne durumda?** (submit edilmiş mi, revizyon bekliyor mu, henüz hazırlanıyor mu?)
4. **LLM (Claude/GPT) niteliksel kodlama veya yazım sürecinde kullanıldı mı?** Eğer evet → A.8 zorunlu
5. **Niteliksel kolun OSF/repository kararı:** Kanonik olarak `osf.io/pytfe` (nicel kol) altında mı, yoksa ayrı proje mi?
6. **Tezde nicel + niteliksel KARMA sunum mu, yoksa niteliksel arm AYRI tez mi?** Bu soru tezin Bölüm 1 (Giriş) çerçevesini tamamen değiştirir
7. **Üye-kontrolü (member reflection) yapılmamış olması — ek bir adım daha mı (4-6 ay sonra) yoksa açık-sınır olarak mı raporlansın?**
8. **Journal vs tez tema yapısı (6 vs 4)** kararı — hangisi öncelikli?

---

## D. Skill Sabitleri Güncellemesi (skill yazarına not)

`niteliksel-arastirma-rehberi-t1dm/SKILL.md` "Tezin Sabitleri" bölümünde şu **yanlış varsayımlar** düzeltilmeli:

| Yanlış varsayım (eski) | Doğru (gerçek) |
|---|---|
| "~12-20 dyad" | 7 aile triadı = 21 katılımcı |
| "anne-çocuk dyadik görüşme" | anne + T1DM çocuk + sağlıklı kardeş **triadik** |
| "EMBU paralel sorular" | EMBU paralel **değil**; aile yaşamı/rol/yük/adalet temalı |
| "DM=120, kontrol=121" niteliksel | Niteliksel kolda **kontrol grubu yok**; tüm 7 aile DM |
| "OSF pytfe & d524q" niteliksel | Belki sadece nicel; niteliksel için ayrı OSF gerekli (henüz yok) |
| "H5 dyadic concordance niteliksel boyut" | H5 nicel kola özgü; niteliksel kol **multi-informant triangulation** üzerinden ilerliyor |

İlerideki iterasyonlarda skill'in `references/12-t1dm-tezi-spesifik-uyarlamalar.md` dosyası güncellenmeli.

---

## E. Önerilen Hemen-Sonraki 3 İş

Faz A başlamadan önce **bugün/yarın** yapılacaklar:

1. **Karar Noktaları (C bölümü)** soruların yanıtlanması — özellikle 1, 4, 6
2. **A.1 (doygunluk → bilgi gücü reframe)** — küçük ama jüri açısından kritik düzelti; YÖNTEM metninin 1 paragrafı yeniden yazılır + Malterud 2016 tablosu eklenir
3. **A.6 (codebook v2)** — codebook v1 + 6 tema triadic matrices arasındaki bağlantı haritası; bu yapılmadan tez Bulgular bölümü yazılamaz

---

**Son not:** Bu yol haritası `niteliksel-arastirma-rehberi-t1dm` skill'inin Faz 0-3 karar akışı + 8 ilkesi + referans dosyaları temel alınarak hazırlandı. Her FAZ adımı için ilgili skill referansı kolon "Skill ref" altında belirtildi — tez yazımı sırasında o dosyaya gidip detaylı rehberlik alınabilir.
