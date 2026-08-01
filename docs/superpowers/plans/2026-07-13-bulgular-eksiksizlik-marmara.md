# BULGULAR Eksiksizlik + Marmara Mimarisi — Uygulama Planı

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `chapters/04_bulgular.qmd` bölümünü, nicel (CSR-FINAL.qmd §9–§16) ve nitel (niteliksel_kanonik_sonuclar.qmd) kanonik kaynaklardaki TÜM bulguları eksiksiz taşıyacak ve Marmara tez kılavuzu mimarisine uyacak biçimde yerinde zenginleştirmek.

**Architecture:** Yaklaşım A (yerinde cerrahi zenginleştirme). Mevcut yorumsuz/doğru omurga korunur; 22 APA tablosu sondaki toplu bloktan konu bölümlerine dağıtılır (figürler zaten inline), CSR §13.5/§13.6 + §15/§16 nicel katmanları ve 6 nitel çapraz netice + eksik ankrajlar eklenir, başlıklar Marmara numaralı biçime (`4.`, `4.1.`, `4.1.1.`) çevrilir, joint-display tek kanonik tabloya birleştirilir.

**Tech Stack:** Quarto (`.qmd`, `lang: tr`), R chunk `apa_render_table()` + `apa_tr_decimal()` yardımcıları, önceden-render carbon SVG şekilleri (`docs/assets/figures/carbon/`), `outputs/tables/apa_t*.csv` (gitignored, render-zamanı okunur).

**Tasarım kaynağı (spec):** [`docs/superpowers/specs/2026-07-13-bulgular-eksiksizlik-marmara-design.md`](../specs/2026-07-13-bulgular-eksiksizlik-marmara-design.md)
**Kanonik kaynaklar:** `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` (nicel), `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd` (nitel).

## Global Constraints

- **Yorumsuz.** Hiçbir yorum/çıkarım/literatür-karşılaştırma cümlesi girmez (marmara §3.6). Yorum → Tartışma.
- **İzlenebilirlik / uydurma-yok.** Her sayı CSR.qmd §9–§16 veya `outputs/tables/apa_t*.csv` ankrajına birebir izlenir; bu plandaki sayılar kanonik kaynaktan verbatim kopyalanmıştır — değiştirilmez, yuvarlanmaz (Stop kapısı kaynaksız sayıyı bloklar).
- **Ondalık biçim (marmara §1.4/§12):** ondalık **virgül**; virgülden önce daima `0`; ortalama/yüzde **1 basamak**; test/oran/β/r/d **2 basamak** (bilimsel gerekçe varsa daha fazla); `p` **3 basamak** (`p=0,038` / `p<0,001`). Anlatıda elle uygulanır; tablo render'ı `apa_tr_decimal()` ile otomatik.
- **KVKK.** Nitel tarafta yalnız tema/alt tema/kod etiketi/quote-ID; ham transcript, alıntı metni, aile demografisi, satır düzeyi veri GİRMEZ.
- **Tablo/şekil (marmara §1.6/§1.7):** tablo başlığı üstte (`#| tbl-cap`), şekil altyazısı altta (`![...]`); aynı bulgu hem tablo hem şekil değil (katsayı-forest'lar tabloda kalır); dipnotta kısaltma/test/p.
- **Başlık (marmara §1.3):** ana başlık `# 4. BULGULAR` (14 pt kalın büyük harf); alt başlık numaraları `4.1.` … en çok dört düzey (`4.4.6.`); birinci düzey her sözcük ilk harfi büyük, ikinci+ düzey yalnız ilk sözcük; bağlaç (ve/ile) küçük; başlık sonunda noktalama yok; `[KEŞİFSEL]`/`[KEŞİFSEL·İKİNCİL]` etiketleri korunur.
- **Kapsam dışı:** 01–03/05 bölümlerinin numaralandırılması; yeni analiz/sayı üretimi; `outputs`/`_targets` yeniden üretimi.
- **Commit politikası:** Repo kuralı gereği commit yalnız kullanıcı onayıyla; commit mesajları Türkçe, `docs(bulgular): …` biçiminde; her mesaj sonuna `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` eklenir. Aşağıdaki commit adımları önerilen kesme noktalarıdır; yürütmede kullanıcı onayına tabidir.

---

## File Structure

| Dosya | Sorumluluk | İşlem |
|---|---|---|
| `chapters/04_bulgular.qmd` | Tek hedef üretim dosyası — tüm görevler burada | Modify |
| `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` | Nicel kanonik kaynak (salt okunur referans) | Read-only |
| `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd` | Nitel kanonik kaynak (salt okunur referans) | Read-only |
| `docs/assets/figures/carbon/**` | Önceden-render SVG şekilleri (yol referansı) | Read-only |

Tüm görevler tek dosyaya sıralı düzenlemedir; her görev bağımsız-incelenebilir bir teslimatla biter.

**Doğrulama yardımcıları (her görevde kullanılır):**
- Bir ankrajın/chunk'ın yerleştiğini doğrula: `grep -n "<desen>" chapters/04_bulgular.qmd`
- Şekil yolu var mı: `test -f docs/assets/figures/carbon/<...>.svg && echo VAR`
- Ondalık ihlali (İngilizce nokta `p`): `grep -nE "p ?[=<] ?\.?[0-9]*\." chapters/04_bulgular.qmd` (nokta-ondalık `p` bulmamalı)

---

### Task 1: Başlık iskeleti ve Marmara numaralandırma

**Files:**
- Modify: `chapters/04_bulgular.qmd` (tüm `#`/`##`/`###` başlıkları)

**Interfaces:**
- Produces: numaralı başlık ağacı (`# 4. BULGULAR`, `## 4.1.` … `## 4.8.`, `### 4.3.1.` …) — sonraki görevler bu numaralı çapaları hedefler.

**Numaralandırma haritası (mevcut → yeni):**
```
# BULGULAR                                  → # 4. BULGULAR
## Örneklem ve Tanımlayıcı Bulgular         → ## 4.1. Örneklem ve Tanımlayıcı Bulgular
## Ölçek ve Veri Kalitesi (Psikometrik...)  → ## 4.2. Ölçek ve Veri Kalitesi (Psikometrik Bulgular)
## Birincil Hipotez Bulguları (H1–H5)       → ## 4.3. Birincil Hipotez Bulguları (H1–H5)
### H1 — Çocuk Algısı (EMBU-C)              → ### 4.3.1. H1 — Çocuk Algısı (EMBU-C)
### H2 — Kardeş İlişkisi (KİA / SRQ)        → ### 4.3.2. H2 — Kardeş İlişkisi (KİA / SRQ)
### H3 — Anne Öz-Bildirimi (EMBU-P)         → ### 4.3.3. H3 — Anne Öz-Bildirimi (EMBU-P)
### H4 — Anne Depresyonu → ...SEM           → ### 4.3.4. H4 — Anne Depresyonu → EMBU-P Latent Yapısal Eşitlik Modeli
### H5 — Diadik Tutarlılık                  → ### 4.3.5. H5 — Diadik Tutarlılık
## [KEŞİFSEL] Genişletilmiş Analiz Katmanları → ## 4.4. [KEŞİFSEL] Genişletilmiş Analiz Katmanları
   (mevcut [KEŞİFSEL] paragrafları 4.4.1–4.4.5 alt başlıklara bölünür — Task 7)
## Robustluk ve Bayesçi Doğrulama           → ## 4.5. Robustluk ve Bayesçi Doğrulama
## Niteliksel Kol Bulguları                 → ## 4.6. Niteliksel Kol Bulguları
### Niteliksel Örneklem ve Analitik Çerçeve → ### 4.6.1. Niteliksel Örneklem ve Analitik Çerçeve
### Tema 1. ...                             → ### 4.6.2. Tema 1 — Sağlıklı Kardeşin Görünmeyen Yükü
### Tema 2. ...                             → ### 4.6.3. Tema 2 — Annenin Tıbbi Bakıcı Rolüne Kayması
### Tema 3. ...                             → ### 4.6.4. Tema 3 — T1DM Tanılı Çocuğun İçeriden Deneyimi
### Tema 4. ...                             → ### 4.6.5. Tema 4 — Aynı Evde Üç Farklı Deneyim
## Karma Bulgulara Köprü (Joint Display)    → ## 4.7. Karma Bulgulara Köprü (Joint Display)
## Genel Bulgu Sentezi                      → ## 4.8. Genel Bulgu Sentezi
## APA Tablo Seti                           → (Task 12'de silinecek — şimdilik dokunma)
## Karma-Kol Kanonik Bütünleştirme (Provisional) → (Task 11'de birleştirilecek — şimdilik dokunma)
```
Not: `### Tema N.` başlıklarındaki nokta kaldırılıp em-dash'li kanonik başlığa çevrilir (başlık sonu noktalama yok kuralı; kanonik tema adları spec §3'te).

- [ ] **Step 1:** Yukarıdaki haritaya göre tüm ana/alt başlıkları Edit ile numaralı biçime çevir. `## APA Tablo Seti` ve `## Karma-Kol Kanonik Bütünleştirme` başlıklarına DOKUNMA (sonraki görevler).
- [ ] **Step 2 (doğrulama):** `grep -nE "^#+ (4\.|4\.[0-9])" chapters/04_bulgular.qmd` — 4.1–4.8 ve 4.3.1–4.3.5, 4.6.1–4.6.5 başlıklarının numaralı çıktığını gör. `grep -nE "^### Tema [0-9]\." chapters/04_bulgular.qmd` boş dönmeli (eski biçim kalmadı).
- [ ] **Step 3 (commit):**
```bash
git add chapters/04_bulgular.qmd
git commit -m "docs(bulgular): Marmara numaralı başlık iskeleti (4.x)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: 4.1 Örneklem — tanımlayıcı tabloları taşı + eksik-veri profili

**Files:**
- Modify: `chapters/04_bulgular.qmd` (4.1 bölümü + sondaki APA blokundan t01–t05 chunk'ları)

**Interfaces:**
- Consumes: Task 1 numaralı başlıklar.
- Produces: 4.1 içinde `apa_render_table("t01…t05")` chunk'ları yerleşik.

**İçerik spesifikasyonu:**
- **Taşı:** Sondaki "APA Tablo Seti"nden şu 5 R chunk'ını KES ve 4.1'in ilgili anlatı paragrafından hemen sonraya yapıştır (aynı `#| label`, `#| tbl-cap`, `apa_render_table()` çağrısı korunur):
  - `t01_sample_characteristics` ("Örneklem özellikleri.") — örneklem paragrafından sonra
  - `t02_covariate_balance` ("Kovaryat dengesi.") — SMD denge paragrafından sonra
  - `t03_missing_data` ("Eksik veri özeti.") — eksik veri cümlesinden sonra
  - `t04_propensity_model` ("Eğilim skoru modeli ve ortak destek.") — IPTW cümlesinden sonra
  - `t05_ses_composite` ("SES kompozit bileşenleri.") — latent SES cümlesinden sonra
- **Anlatıya ekle (GAP — eksik-veri profili, CSR §9.5):** mevcut "en yüksek eksiklik ISEI-08 mesleki indeksindedir (%9,1)" cümlesini genişlet: "…ISEI-08 mesleki indeksinde %9,1; materyal göstergede %0,4; Beck toplamında %1,2 düzeyindedir. Kontrol grubunda DM yılı (%50,2) ve HbA1c (%83,8) tasarım kaynaklı yapısal eksikliktir ve imputasyona alınmamıştır." (Sayılar CSR §9.5/§10 miss-fig; ondalık virgül.)
- **Opsiyonel şekil:** 4.1'e görsel-özgü iki şekil eklenebilir (mevcut fig-01/02/04/05'e ek): `fig-03-smd-love-plot.svg` (denge love-plot) ve `fig-06-missing-pattern-primary.svg` (eksik-örüntü). Marmara "aynı bulgu tablo+şekil değil" — love-plot Tablo 2 ile örtüşürse yalnız biri; öneri: fig-06 (eksik-örüntü görsel-özgü) eklenir, fig-03 opsiyonel bırakılır. Altyazı biçimi diğer şekillerle aynı.

- [ ] **Step 1:** t01–t05 chunk'larını sondan kes, 4.1'de ilgili paragraflardan sonra sırayla yerleştir.
- [ ] **Step 2:** Eksik-veri profili cümlesini yukarıdaki verbatim sayılarla genişlet.
- [ ] **Step 3 (opsiyonel):** `test -f docs/assets/figures/carbon/primary/fig-06-missing-pattern-primary.svg && echo VAR`; varsa 4.1 eksik-veri paragrafından sonra alt-altyazılı şekil ekle.
- [ ] **Step 4 (doğrulama):** `grep -n "t01_sample\|t02_covariate\|t03_missing\|t04_propensity\|t05_ses" chapters/04_bulgular.qmd` — beş chunk'ın SADECE 4.1'de (sondaki blokta değil) bir kez geçtiğini doğrula. `grep -n "%0,4\|%1,2\|%50,2\|%83,8" chapters/04_bulgular.qmd` eksik-veri sayılarını gör.
- [ ] **Step 5 (commit):**
```bash
git add chapters/04_bulgular.qmd
git commit -m "docs(bulgular): 4.1 tanımlayıcı tabloları konuya taşı + tam eksik-veri profili

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: 4.2 Psikometri — yanlış-atıf düzelt + güvenirlik/geçerlik ankrajları + psychval şekilleri

**Files:**
- Modify: `chapters/04_bulgular.qmd` (4.2 bölümü)

**Interfaces:**
- Consumes: Task 1 başlıkları.
- Produces: 4.2 güvenirlik anlatısı (8 alt-ölçek α/ω) + psychval-01/02 şekilleri; apa_t05 yanlış-atıfı kaldırılmış.

**İçerik spesifikasyonu:**
- **F1 düzelt:** 4.2 sonundaki "Güvenirlik ve faktör göstergeleri Tablo 5'te (`apa_t05`) özetlenmiştir." cümlesini KALDIR — `apa_t05` SES kompozitidir, güvenirlik değil. Yerine güvenirlik şekline atıf (aşağıda).
- **GAP — 8 alt-ölçek α/ω anlatıya (CSR §10.1 fig), verbatim:**
  - EMBU-P: sıcaklık α=0,68 / ω=0,69; aşırı koruma α=0,75 / ω=0,75; karşılaştırma α=0,70 / ω=0,72; reddetme α=0,45 / ω=0,48 (zaten var).
  - EMBU-C: sıcaklık α=0,81 / ω=0,81; aşırı koruma α=0,61 / ω=0,64; karşılaştırma α=0,79 / ω=0,80; reddetme α=0,72 / ω=0,75 (zaten var).
  - (Not: raporlanan ham değerler EMBU-P sıcaklık 0,678/0,687 vb.; Marmara §12 iki basamak → 0,68/0,69. Güvenirlik katsayısı için iki basamak yeterli.)
- **GAP — §10.5 kriter-geçerlik ρ (verbatim, ondalık virgül, p üç basamak):** "Kriter geçerliği taramasında sıcaklık(P)×Beck ρ=−0,22 (p<0,001); reddetme(P)×Beck ρ=0,17 (p=0,008); karşılaştırma(P)×Beck ρ=0,26 (p<0,001); karşılaştırma(C)×SRQ çatışma ρ=0,30 (p<0,001); karşılaştırma(C)×SRQ sıcaklık ρ=−0,16 (p<0,001); karşılaştırma(C)×SRQ rekabet ρ=0,14 (p=0,002) yönünde anlamlı ilişkiler bulunmuştur (14 korelasyon, FDR düzeltmesi)."
- **Şekil ekle:** 4.2'ye güvenirlik ve taban etkisi görsel-özgü şekilleri:
  - `psychval-01-reliability.svg` — güvenirlik paragrafından sonra, altyazı: "EMBU-P ve EMBU-C alt ölçeklerinde Cronbach α ve McDonald ω güvenirlik katsayıları (%95 güven aralığıyla)."
  - `psychval-02-floor.svg` — taban etkisi paragrafından sonra, altyazı: "EMBU-P ve EMBU-C reddetme alt ölçeği maddelerinde taban etkisi oranları."
  - (Opsiyon: `psychval-03-cfa.svg` CFA, `psychval-06-validity.svg` geçerlik ısı haritası — görsel-özgüyse eklenebilir; ikiden fazla şekil eklenerek bölüm boğulmaz.)

- [ ] **Step 1:** apa_t05 yanlış-atıf cümlesini kaldır.
- [ ] **Step 2:** 8 alt-ölçek α/ω değerlerini güvenirlik paragrafına ekle (EMBU-P/C sıcaklık/aşırı koruma/karşılaştırma; reddetme zaten var).
- [ ] **Step 3:** §10.5 kriter-geçerlik ρ cümlesini ekle.
- [ ] **Step 4:** `psychval-01-reliability.svg` ve `psychval-02-floor.svg` şekillerini alt-altyazılı ekle (yol: `docs/assets/figures/carbon/psychometric/`).
- [ ] **Step 5 (doğrulama):** `grep -n "apa_t05" chapters/04_bulgular.qmd` — 4.2'de GEÇMEMELİ (yalnız 4.1'de t05_ses chunk'ı). `grep -n "psychval-01-reliability\|psychval-02-floor\|ρ=0,30\|ρ=−0,22" chapters/04_bulgular.qmd` yeni içeriği gör.
- [ ] **Step 6 (commit):**
```bash
git add chapters/04_bulgular.qmd
git commit -m "docs(bulgular): 4.2 psikometri — apa_t05 yanlış-atıf düzeltildi, 8 alt-ölçek α/ω + kriter-geçerlik ρ + psychval şekilleri

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: 4.3.1 H1 — tabloları taşı + rol-özgül kontrast

**Files:**
- Modify: `chapters/04_bulgular.qmd` (4.3.1 + sondaki bloktan t06/t07)

**İçerik spesifikasyonu:**
- **Taşı:** `t06_h1_primary` ("H1 çok-düzeyli kovaryans analizi sabit etkileri.") ve `t07_h1_bayesian` ("H1 Bayesçi çift raporlama.") chunk'larını 4.3.1'in ilgili paragraflarından sonraya taşı.
- **GAP — rol-özgül kontrast (CSR §11.1.5, verbatim):** H1 anlatısına, havuz DM etkisinden sonra ekle: "Rol-özgül kontrastlarda reddetme farkı DM-indeks çocukta β=0,15 SD (%95 GA [0,05; 0,26]) ve DM-kardeşte β=0,14 SD ([0,03; 0,24]) düzeyindedir; aşırı koruma alt ölçeğinde DM-indeks çocuk kontrastı β=0,20 SD ([0,05; 0,35]) ile sıfırdan ayrık, sıcaklıkta DM-kardeş kontrastı β=0,16 SD ([0,02; 0,30]) düzeyindedir." (Bu, havuz sonucuyla çelişmez; rol kırılımı yorumsuz betimlenir.)

- [ ] **Step 1:** t06/t07 chunk'larını sondan kes, 4.3.1'e yerleştir.
- [ ] **Step 2:** rol-özgül kontrast cümlesini ekle.
- [ ] **Step 3 (doğrulama):** `grep -n "t06_h1_primary\|t07_h1_bayesian\|0,20 SD\|DM-indeks" chapters/04_bulgular.qmd`.
- [ ] **Step 4 (commit):**
```bash
git add chapters/04_bulgular.qmd
git commit -m "docs(bulgular): 4.3.1 H1 tabloları taşındı + rol-özgül kontrast eklendi

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: 4.3.2–4.3.4 H2/H3/H4 — tabloları taşı

**Files:**
- Modify: `chapters/04_bulgular.qmd` (4.3.2/4.3.3/4.3.4 + sondaki bloktan t08–t12)

**İçerik spesifikasyonu:**
- **Taşı:** `t08_h2_family_mean`, `t09_h2_apim` → 4.3.2; `t10_h3_primary_iptw`, `t11_h3_sensitivity` → 4.3.3; `t12_h4_sem` → 4.3.4. Her chunk ilgili anlatı paragrafından sonra. (H2/H3/H4 anlatı sayıları CSR ile eşleşiyor — Task envanterinde ✓; ek gap yok.)

- [ ] **Step 1:** t08/t09 → 4.3.2.
- [ ] **Step 2:** t10/t11 → 4.3.3.
- [ ] **Step 3:** t12 → 4.3.4.
- [ ] **Step 4 (doğrulama):** `grep -n "t08_h2\|t09_h2\|t10_h3\|t11_h3\|t12_h4" chapters/04_bulgular.qmd` — beşi de yalnız 4.3.x'te.
- [ ] **Step 5 (commit):**
```bash
git add chapters/04_bulgular.qmd
git commit -m "docs(bulgular): 4.3.2–4.3.4 H2/H3/H4 tabloları konuya taşındı

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: 4.3.5 H5 — tabloyu taşı

**Files:**
- Modify: `chapters/04_bulgular.qmd` (4.3.5 + sondaki bloktan t13)

**İçerik spesifikasyonu:**
- **Taşı:** `t13_h5_concordance` ("H5 diadik tutarlılık stratejileri.") → 4.3.5 (beş strateji anlatısından sonra, fig-12/fig-13'ten önce veya sonra). H5 figürleri (fig-12 BA-grid, fig-13 RSA-surface) zaten 4.3.5'te — dokunma. H5 sayıları CSR §11.5 ile eşleşiyor; ek gap yok.

- [ ] **Step 1:** t13 chunk'ını sondan kes, 4.3.5'e yerleştir.
- [ ] **Step 2 (doğrulama):** `grep -n "t13_h5_concordance" chapters/04_bulgular.qmd` — yalnız 4.3.5.
- [ ] **Step 3 (commit):**
```bash
git add chapters/04_bulgular.qmd
git commit -m "docs(bulgular): 4.3.5 H5 tablosu konuya taşındı

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 7: 4.4.1–4.4.5 [KEŞİFSEL] — alt başlıklandır + tabloları taşı

**Files:**
- Modify: `chapters/04_bulgular.qmd` (4.4 bölümü + sondaki bloktan t14–t18)

**İçerik spesifikasyonu:**
- **Alt başlıklandır:** Mevcut 4.4 içindeki `[KEŞİFSEL] Aracılık`, `[KEŞİFSEL] Latent profil…`, `[KEŞİFSEL] Ağ analizi`, `[KEŞİFSEL] Klinik fayda`, `[KEŞİFSEL] DM klinik alt-analizler` **bold paragraf** başlangıçlarını `### 4.4.1.`–`### 4.4.5.` numaralı alt başlıklara çevir (metin gövdesi aynı).
  - `### 4.4.1. [KEŞİFSEL] Aracılık`
  - `### 4.4.2. [KEŞİFSEL] Latent Profil ve Sınıf Analizi`
  - `### 4.4.3. [KEŞİFSEL] Ağ Analizi`
  - `### 4.4.4. [KEŞİFSEL] Klinik Fayda`
  - `### 4.4.5. [KEŞİFSEL] DM Klinik Alt-Analizler`
- **Taşı:** `t14_mediation` → 4.4.1; `t15_lpa_bifactor` → 4.4.2; `t16_network` → 4.4.3; `t17_clinical` → 4.4.4; `t18_dm_clinical` → 4.4.5. İlgili figürler (fig-15, fig-16/17, fig-18-21) zaten bu paragraflarda — dokunma.

- [ ] **Step 1:** Beş [KEŞİFSEL] bold-paragraf başlangıcını numaralı `###` alt başlığa çevir.
- [ ] **Step 2:** t14–t18 chunk'larını sondan kes, ilgili 4.4.x alt bölümlerine yerleştir.
- [ ] **Step 3 (doğrulama):** `grep -nE "^### 4\.4\.[1-5]\." chapters/04_bulgular.qmd` beş başlığı; `grep -n "t14_mediation\|t15_lpa\|t16_network\|t17_clinical\|t18_dm" chapters/04_bulgular.qmd` beş chunk'ı yalnız 4.4.x'te göster.
- [ ] **Step 4 (commit):**
```bash
git add chapters/04_bulgular.qmd
git commit -m "docs(bulgular): 4.4 keşifsel katman alt başlıklandırıldı + t14–t18 taşındı

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 8: 4.4.6 [KEŞİFSEL·İKİNCİL] İleri Psikometrik ve Bağlamsal Katman (YENİ — §15+§16)

**Files:**
- Modify: `chapters/04_bulgular.qmd` (4.4 sonuna yeni `### 4.4.6.` alt bölümü)

**İçerik spesifikasyonu (CSR §15 ve §16, verbatim sayılar, YORUMSUZ):**
Yeni alt bölüm `### 4.4.6. [KEŞİFSEL·İKİNCİL] İleri Psikometrik ve Bağlamsal Katman` — giriş cümlesi: "Aşağıdaki bulgular ön-kayıtlı planın ikincil/keşifsel katmanıdır; birincil hipotez sonucu gibi yorumlanmaz ve dış-validasyon olmadan klinik öneriye çıkarılmaz."

**§15 ileri psikometri/ikincil (verbatim):**
- Trifaktör T-CFA: CFI medyan 0,90; RMSEA 0,05.
- Latent informant-discrepancy SEM: reddetme latent uyuşmazlık r=0,03 (%95 GA [−0,13; 0,19]).
- Floor-aware IRT: indeks çocukta reddetme d=0,37; aşırı koruma latent d=0,54 (manifest 0,37'nin üzerinde).
- Reliability generalization: EMBU-P ω_h=0,66; ECV=0,41. <!-- GÜNCELLİK UYARISI (2026-07-26): Bu enstrüman-düzeyi değerler bu plan notunda BAYATTIR. Kanonik güncel değer EMBU-P ω_h=0,81; ECV=0,47 (kaynak: outputs/tables/phase2_omegah_metrics_summary.csv; runner: scripts/R/37_reliability_generalization_audit.R). Tarihsel plan bağlamı olarak korunmuştur; canlı tez metni (§4.4.6) kanonik değeri r-call ile okur. -->
- **H1 çoklu-evren:** 120/120 spesifikasyon; medyan β=0,13; p<0,05 payı %75; spec-curve çıkarımsal t=4,08; permütasyon p<0,001 (anlamlı). *(Not: 4.5'teki H3 %0-null'ıyla asimetri — yorumsuz betimlenir; yorum Tartışma'da.)*
- Meta-analitik havuzlama: 0,14 (%95 GA [0,05; 0,23]); τ=0,11.
- Klinik karar modeli (genişletilmiş): AUC=0,70; standardize net fayda 0,86 (eşik 0,05).
- HbA1c×ebeveynlik Bayesçi: sıcaklık pd=0,94; karşılaştırma pd=0,95 (n=39).

**§16 bağlamsal (verbatim):**
- Diferansiyel ebeveynlik (PDT): Holm-düzeltmede 16 testin 0'ı anlamlı; DM baba-kayırma d=−0,27 ([−0,52; −0,01], p=0,039, düzeltilmemiş).
- Sosyal tabakalaşma: EGP gradyanı Holm-anlamsız; ISEI/SIOPS/EGP göstergeleri yüksek eşdoğrusallık.
- Anne komorbidite: komorbidite→Beck d=0,29 (Holm-anlamsız); antidepresan kullanımı DM %29,2, kontrol %9,1 (χ²=14,45; Cramér V=0,25).
- Aile yapısı: diadik karşılıklılık r=0,18–0,38.
- DM maruziyet yoğunluğu: 9 testin 0'ı Holm-anlamlı.
- **Anne mental sağlık → çocuk:** güncel Beck≥17 olan annelerin çocuklarında EMBU-C reddetme algısı b=0,13 (p=0,004), DM grubu ve antidepresandan bağımsız; latent sınıf riskli grubu reddetme-uyuşmazlığını (p<0,001) ve kardeş çatışmasını (p=0,006) yordamaktadır.
- Yönlü kardeş mimarisi: 3 grup ve 14 fasette FDR-anlamlı bulgu yok.
- Çocuk moderatör: cinsiyet×grup 8 testte 0 Holm-anlamlı; anne yaşı→aşırı koruma b=−0,03/yıl (p=0,004).
- **Seçilim denetimi:** HbA1c eksikliği MNAR seçilim OR=4,56 (p<0,001); yıl×grup ilişkisi Cramér V=0,59; H1 çocuk-reddetme farkı yalnız-2023 alt-örnekleminde zayıflamaktadır (dönem temkini).

**Şekiller (görsel-özgü seçki, 6–10 arası):** ilgili paragraflardan sonra alt-altyazılı ekle:
- `phase2/phase2_f01_trifactor.svg`, `phase2_f02_xinfo.svg`, `phase2_f03_floor_irt.svg`, `phase2_f05_h1_spec_curve.svg`, `phase2_f06_meta_forest.svg`, `phase2_f12_dca_heatmap.svg`
- `exploratory/expl_f01_reciprocity.svg`, `expl_f02_pdt_direction.svg`, `expl_f03_comorbidity.svg`, `expl_f06_integrated_panel.svg`
(Her biri için `test -f` ile varlık doğrula; olmayanı ekleme.)

- [ ] **Step 1:** 4.4.5'ten sonra `### 4.4.6.` alt bölümünü giriş cümlesiyle oluştur.
- [ ] **Step 2:** §15 sekiz bulgusunu yorumsuz paragraf(lar) hâlinde yaz (verbatim sayılar).
- [ ] **Step 3:** §16 dokuz bulgusunu yorumsuz paragraf(lar) hâlinde yaz (verbatim sayılar).
- [ ] **Step 4:** Mevcut phase2/exploratory SVG'lerini `test -f` ile doğrula ve görsel-özgü seçkiyi alt-altyazılı ekle.
- [ ] **Step 5 (doğrulama):** `grep -n "4.4.6\|çoklu-evren\|OR=4,56\|b=0,13\|pd=0,94" chapters/04_bulgular.qmd`; ondalık denetimi `grep -nE "p ?[=<] ?\.[0-9]" chapters/04_bulgular.qmd` (nokta-ondalık p bulmamalı).
- [ ] **Step 6 (commit):**
```bash
git add chapters/04_bulgular.qmd
git commit -m "docs(bulgular): 4.4.6 [KEŞİFSEL·İKİNCİL] §15+§16 ileri psikometri/bağlam katmanı eklendi

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 9: 4.5 Robustluk — tabloları taşı + §13.5/§13.6 ekle

**Files:**
- Modify: `chapters/04_bulgular.qmd` (4.5 + sondaki bloktan t19/t20/t21)

**İçerik spesifikasyonu:**
- **Taşı:** `t19_robustness` → 4.5 (çoklu evren/TOST paragrafından sonra); `t20_sensitivity` → 4.5 (sensemakr/negatif kontrol paragrafından sonra); `t21_bayesian_global` → 4.5 (Bayesçi paragraftan sonra). Figürler (fig-22 spec-curve, fig-23 sensemakr) zaten 4.5'te.
- **GAP §13.5 (verbatim), yeni paragraf:** "**Eksik-veri çerçevesi sağlamlığı.** H3 birincil tahminleri üç eksik-veri çerçevesinde tekrarlanmıştır: tamamlanmış olgu (N=219), tam bilgi maksimum olabilirlik (FIML, N=241) ve çoklu atama (MI, m=50, N=241). Çerçeveler arası en büyük katsayı yayılımı reddetme alt ölçeğinde 0,01 SD düzeyindedir; MNAR delta duyarlılık ızgarasında reddetme etkisi −0,04 dolayında sabit kalmış (p≈0,31), birincil sonucun yönü değişmemiştir."
- **GAP §13.6 (verbatim), yeni paragraf:** "**SES operasyonelleştirme sağlamlığı.** H3 reddetme tahmini dört farklı sosyoekonomik durum tanımıyla tekrarlanmıştır: latent doğrulayıcı faktör analizi, Hollingshead indeksi, eşit-ağırlıklı kompozit ve ham ISEI-08. Standardize grup katsayısı sırasıyla −0,04; −0,03; −0,04 ve −0,03 düzeyinde, tanımlar arası yayılım 0,01 SD ile sınırlı kalmıştır."

- [ ] **Step 1:** t19/t20/t21 chunk'larını sondan kes, 4.5'e yerleştir.
- [ ] **Step 2:** §13.5 eksik-veri çerçevesi paragrafını ekle.
- [ ] **Step 3:** §13.6 SES operasyonelleştirme paragrafını ekle.
- [ ] **Step 4 (doğrulama):** `grep -n "t19_robustness\|t20_sensitivity\|t21_bayesian\|FIML\|Hollingshead\|MNAR delta" chapters/04_bulgular.qmd`.
- [ ] **Step 5 (commit):**
```bash
git add chapters/04_bulgular.qmd
git commit -m "docs(bulgular): 4.5 robustluk tabloları taşındı + §13.5 eksik-veri çerçevesi & §13.6 SES sağlamlığı eklendi

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 10: 4.6 Niteliksel — analitik ölçek + ankraj doldurma + çapraz netice + negatif vaka/odak matris

**Files:**
- Modify: `chapters/04_bulgular.qmd` (4.6.1–4.6.5 + yeni 4.6.6, 4.6.7)

**İçerik spesifikasyonu (nitel kanonik .qmd, YORUMSUZ, yalnız kod/quote-ID — KVKK):**

- **4.6.1 GAP — analitik ölçek sayıları:** örneklem/çerçeve paragrafına ekle: "Analitik taban yedi aile triadı (011, 014, 019, 020, 026, 201, 202) ve 21 bireysel görüşmedir (yedi anne, yedi T1DM tanılı çocuk, yedi sağlıklı kardeş). Refleksif tematik analiz beş kategoride 23 koddan oluşan bir codebook üretmiş; 116 araştırmacı-denetimli kodlanmış segment ve 57 satırlık triadik matris (aile × tema × alt tema) oluşturulmuştur. Rol düzeyinde kodlanmış alıntı dağılımı anne 55, T1DM tanılı çocuk 36, sağlıklı kardeş 25'tir."

- **4.6.2 (Tema 1) GAP kod:** öne çıkan kodlar satırına ekle: `KARDES_ILISKISI`, `BESLENME_KONTROL` (mevcutlara ek).
- **4.6.3 (Tema 2) GAP:** quote ID ankrajına `014_mother_q002` ekle; kod satırına `KAYGI_KIRILGANLIK`, `COCUK_OZERKLIK_OZBAKIM`, `AILE_DESTEGI`, `ILETISIM_CATISMA` ekle.
- **4.6.4 (Tema 3) GAP:** quote ID'lere `026_t1dm_child_q002`, `202_t1dm_child_q002` ekle; kod satırına `RUTIN_TAKIP`, `BESLENME_KONTROL`, `AKRAN_CEVRE_DESTEGI`, `KARDES_ILISKISI` ekle.
- **4.6.5 (Tema 4) GAP — öne çıkan kod satırı EKLE (tamamen eksik):** "öne çıkan kodlar: `RUTIN_TAKIP`, `KAYGI_KIRILGANLIK`, `OFKE_ADALETSIZLIK`, `KARDES_GORUNMEZ_YUK`, `KARDES_ILISKISI`, `AILE_ICI_ADALET`, `COCUK_OZERKLIK_OZBAKIM`." Ayrıca triadik quote ID'leri her rol için 5'e tamamla:
  - anne: mevcut `011_mother_q006`, `020_mother_q009`, `026_mother_q008` + ekle `026_mother_q009`, `011_mother_q007`
  - T1DM çocuk: mevcut `011_t1dm_child_q004`, `020_t1dm_child_q001`, `026_t1dm_child_q008` + ekle `020_t1dm_child_q002`, `014_t1dm_child_q002`
  - kardeş: mevcut `011_healthy_sibling_q001`, `020_healthy_sibling_q001`, `019_healthy_sibling_q002` + ekle `019_healthy_sibling_q003`, `201_healthy_sibling_q001`

- **4.6.6 (YENİ) — Çapraz Bilimsel Neticeler:** 4.6.5'ten sonra yeni `### 4.6.6. Çapraz Bilimsel Neticeler`. Giriş: "Dört makro temanın çapraz okumasından altı temalar-arası bilimsel netice belirmektedir." Altı netice (yorumsuz betim):
  1. Tip 1 diyabet ailede aile-düzeyi bir düzenleme rejimi üretmekte; gündelik yaşam ölçüm, beslenme ve izlem etrafında yeniden kurulmaktadır.
  2. Anne bakımı hem klinik hem ahlaki sorumluluk olarak içselleştirmektedir.
  3. Sağlıklı kardeşin yükü çoğu zaman sessiz taşınmaktadır (açık şikâyet nadir).
  4. T1DM tanılı çocuk normalleşme ile farklılık arasında sürekli müzakere etmektedir.
  5. Koruma, kontrol ve adalet aynı ebeveyn davranışında birleşebilmektedir.
  6. Üç rolün farklı anlatısı bir ölçüm hatası değil, bağlamsal bir bilimsel sonuçtur.

- **4.6.7 (YENİ) — Negatif Vaka, Sınırlayıcı Örüntüler ve Odak Aile Matrisi:** yeni `### 4.6.7.`. İçerik (yorumsuz):
  - Tema 4 için sistematik negatif-vaka taraması üç alanda yürütülmüştür: temalarla karşıtlık işaretleri, "normal" söyleminin sınırları ve Aile 201'in rol temsili.
  - Odak aile matrisi, ailelerin temalara katkısında eşitsiz dağılım göstermektedir (Aile 011 ve 202 en yüksek odak; Aile 201 en düşük tek-alan temsili). Bu dağılım, bilgi gücünün aileler arası eşitsiz dağıldığını ve Aile 201'in aktarılabilirlik tartışmasına bağlandığını belgelemektedir. *(Yorum Tartışma'ya bırakılır.)*

- [ ] **Step 1:** 4.6.1 analitik ölçek sayılarını ekle.
- [ ] **Step 2:** Tema 1–3 (4.6.2–4.6.4) eksik kod + quote ID ankrajlarını ekle.
- [ ] **Step 3:** Tema 4 (4.6.5) öne çıkan kod satırını ekle + her rol için quote ID'leri 5'e tamamla.
- [ ] **Step 4:** 4.6.6 Çapraz Bilimsel Neticeler alt bölümünü (6 netice) ekle.
- [ ] **Step 5:** 4.6.7 Negatif Vaka + Odak Aile Matrisi alt bölümünü ekle.
- [ ] **Step 6 (doğrulama):** `grep -n "116 araştırmacı\|57 satır\|014_mother_q002\|201_healthy_sibling_q001\|4.6.6\|4.6.7\|Çapraz Bilimsel" chapters/04_bulgular.qmd`. KVKK: `grep -niE "transcript|ham görüşme" chapters/04_bulgular.qmd` boş dönmeli (alıntı metni yok).
- [ ] **Step 7 (commit):**
```bash
git add chapters/04_bulgular.qmd
git commit -m "docs(bulgular): 4.6 nitel — analitik ölçek + eksik kod/quote ankrajları + çapraz netice + negatif vaka/odak matris

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 11: 4.7 Joint display birleştirme + 4.8 sentez hizalama

**Files:**
- Modify: `chapters/04_bulgular.qmd` (4.7, iki joint-display tablosu; 4.8 sentez)

**İçerik spesifikasyonu:**
- **F3 birleştir:** İki joint-display tablosu ("Karma Bulgulara Köprü" 5 satır + "Karma-Kol Kanonik Bütünleştirme (Provisional)" 6 satır) tek kanonik tabloya indirilir. Daha zengin **6 satırlı** sürüm (H1–H5 + Meta triadik informant asimetrisi; sütunlar: Odak | Nicel verdikt | Nitel örüntü | İlişki türü | Yorum sınırı) tutulur; provenans HTML yorum ankrajları (`<!-- kaynak: … -->`) korunur. İkinci başlık `## 4.7.` altında tek tablo olur; ilk tablonun içeriği zenginse birleştir, tekrarı sil.
- **"Provisional/TASLAK" kaldır:** `<!-- TASLAK / provisional-pass … -->` yorum satırı ve başlıktaki "(Provisional)" ibaresi silinir; başlık `## 4.7. Karma Bulgulara Köprü (Joint Display)`.
- **4.8 hizalama:** Genel Bulgu Sentezi paragrafı, nitel omurga "dört makro tema + altı çapraz netice" olacak biçimde güncellenir (mevcut nicel özet korunur; yorum cümlesi girmez). Kapanış cümlesi "…yorumu *Tartışma ve Sonuç* bölümünde ele alınmaktadır." korunur.

- [ ] **Step 1:** İki joint-display bölümünü 4.7 altında tek 6-satırlı kanonik tabloya birleştir; ikinci başlığı/tabloyu kaldır.
- [ ] **Step 2:** "(Provisional)" ibaresini ve `<!-- TASLAK … -->` yorumunu kaldır.
- [ ] **Step 3:** 4.8 sentez paragrafını "dört makro tema + altı çapraz netice" omurgasına hizala (yorumsuz).
- [ ] **Step 4 (doğrulama):** `grep -nc "Joint Display\|joint-display\|İlişki türü" chapters/04_bulgular.qmd` — yalnız bir joint-display tablosu; `grep -ni "provisional\|TASLAK" chapters/04_bulgular.qmd` boş dönmeli.
- [ ] **Step 5 (commit):**
```bash
git add chapters/04_bulgular.qmd
git commit -m "docs(bulgular): 4.7 joint-display tek kanonik tabloya birleştirildi (provisional kaldırıldı) + 4.8 sentez hizalandı

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 12: Toplu blok kaldırma + biçim/ondalık cilası + kapanış doğrulaması

**Files:**
- Modify: `chapters/04_bulgular.qmd` (eski "APA Tablo Seti" başlığı + genel biçim)

**İçerik spesifikasyonu:**
- **F2:** Tüm 22 chunk taşındığından, artık boş kalan `## APA Tablo Seti` başlığını ve giriş paragrafını (satır ~345–350 civarı) sil. `apa-table-helpers` yardımcı chunk'ı (dosya başındaki `apa_read_table`/`apa_tr_decimal`/`apa_render_table`) KORUNUR (chunk'lar hâlâ onu kullanıyor).
- **F5/F6 biçim cilası:** anlatıda ondalık virgül/`p` biçimi, şekil alt-altyazı `Şekil N.` kalıbı, tablo `#| tbl-cap` üst konum ve gerekli dipnotlar denetlenir.

- [ ] **Step 1:** Boş "## APA Tablo Seti" başlığı + giriş paragrafını sil; `apa-table-helpers` chunk'ının durduğunu doğrula.
- [ ] **Step 2 (doğrulama — chunk bütünlüğü):** `grep -c "apa_render_table(" chapters/04_bulgular.qmd` → 22 (hepsi konu bölümlerinde). `grep -n "## APA Tablo Seti" chapters/04_bulgular.qmd` boş.
- [ ] **Step 3 (doğrulama — ondalık):** `grep -nE "[0-9] ?[=<] ?\.[0-9]|p ?[=<] ?\.[0-9]" chapters/04_bulgular.qmd` → İngilizce nokta-ondalık p/sayı bulmamalı (axis G blocker önizleme).
- [ ] **Step 4 (doğrulama — şekil yolları):** `grep -oE "docs/assets/figures/[^)]*\.svg" chapters/04_bulgular.qmd | sort -u | while read f; do test -f "$f" || echo "YOK $f"; done` → hiçbir "YOK" satırı olmamalı.
- [ ] **Step 5 (render dumanı):** `quarto render chapters/04_bulgular.qmd --to html 2>&1 | tail -20` (izole render mümkünse) veya tam `quarto render` ile bölüm chunk'larının kırılmadığını doğrula. Hata varsa düzelt.
- [ ] **Step 6 (sci-audit 7-eksen):** `/sci-audit:audit chapters/04_bulgular.qmd --lang tr --strictness certification --type jars` çalıştır; `/sci-audit:check-turkish chapters/04_bulgular.qmd --strictness certification` ile axis G. `blocker`/`error` sıfırlanmadan kapanma yok. Rapor: `tez-yazim/04_kalite-kontrol/raporlar/04-bulgular-sci-audit.md`.
- [ ] **Step 7 (commit):**
```bash
git add chapters/04_bulgular.qmd
git commit -m "docs(bulgular): toplu APA Tablo Seti bloğu kaldırıldı (22 tablo dağıtıldı) + biçim/ondalık cilası

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 13: Kanonik izlenebilirlik çapraz-doğrulaması (paralelleştirilebilir kapanış)

**Files:**
- Read-only doğrulama; düzeltme gerekirse `chapters/04_bulgular.qmd`.

**İçerik spesifikasyonu:**
Bölüm bittiğinde, her alt bölümün sayılarının kanonik kaynak ankrajıyla birebir eşleştiği bağımsız doğrulanır. Alt bölüm başına bir doğrulama ajanı (4.1 tanımlayıcı, 4.2 psikometri, 4.3.x H1–H5, 4.4.x keşifsel, 4.5 robustluk, 4.6 nitel) paralel çalıştırılabilir; her ajan yalnız kendi bölümündeki her sayıyı CSR.qmd/nitel.qmd'ye izler ve uydurma/uyuşmazlık raporlar (`.filter(Boolean)` düzeyinde bulgu). Bulunan uyuşmazlık düzeltilir.

- [ ] **Step 1:** Paralel doğrulama ajanları (bölüm-başına) dağıt; her biri kanonik ankraja karşı sayı-eşleme raporu döndürsün.
- [ ] **Step 2:** Raporlanan uyuşmazlıkları (varsa) düzelt; hiç uydurma sayı olmadığını teyit et.
- [ ] **Step 3 (commit — yalnız düzeltme varsa):**
```bash
git add chapters/04_bulgular.qmd
git commit -m "docs(bulgular): kanonik izlenebilirlik çapraz-doğrulaması düzeltmeleri

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review (yazım-planı kontrolü)

**1. Spec kapsamı:** spec §3 bölüm ağacının her düğümü bir göreve eşlendi — 4.1→T2, 4.2→T3, 4.3.1→T4, 4.3.2-4→T5, 4.3.5→T6, 4.4.1-5→T7, 4.4.6→T8, 4.5→T9, 4.6→T10, 4.7/4.8→T11, F2/biçim→T12, doğrulama→T13. Numaralandırma→T1. Spec §5 düzeltmeleri: F1→T3, F2→T12, F3→T11, F4→T1, F5/F6→T12. Boşluk yok.
**2. Placeholder taraması:** somut sayılar/ankrajlar/quote-ID'ler verbatim verildi; "TODO/TBD/uygun biçimde" yok. Prose görevlerinde tam faktör yükü (sayı+ankraj+yerleşim+biçim) belirtildi; cümle düzeyi ifade yürütmede üretilir (prose için doğal).
**3. Tutarlılık:** chunk kimlikleri (`t01_sample_characteristics` … `t22_result_synthesis`) tüm görevlerde `outputs/tables/apa_t*.csv` adlarıyla birebir; şekil yolları `find` envanteriyle doğrulanmış; heading numaraları çakışmasız.

## Execution Handoff

Plan tamamlandı ve kaydedildi: `docs/superpowers/plans/2026-07-13-bulgular-eksiksizlik-marmara.md`

---

## FAZ 2 — Açıklayıcılık, Okunabilirlik ve 03↔04 Uyumu (2026-07-13, kullanıcı onaylı)

**Amaç:** Gereç-Yöntem (03) ve Bulgular (04) bölümlerini istatistik-uzmanı-olmayan okur için daha açıklayıcı kılmak, Marmara anlam-akışı/okunabilirlik iyileştirmesi yapmak, iki bölümün uyumunu mükemmelleştirmek ve kapanışta tam sci-audit 7-eksen koşmak. Kaynak üslup: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` "Yöntem & tatbik" / "Nasıl değerlendirilir" düz-dil kutuları.

- **F2-A (03 açıklayıcılık + kip):** Adı geçip açıklanmayan yöntemlere akışa-gömülü 1–2 cümlelik düz-dil açıklama (WLSMV, dereceli yanıt IRT, eğilim skoru/IPTW, FDR, TOST, Bayesçi BF/ROPE, çoklu evren, sensemakr/E-değeri, RSA, ortak yazgı, Olsen-Kenny, APIM). Gelecek-zaman fiilleri (`raporlanacaktır` vb.) → geçmiş edilgen (`raporlanmıştır`); tamamlanmış-belge tonu (Marmara §1.4).
- **F2-B (04 açıklayıcılık, yorumsuz):** Her H alt bölümü + kritik keşifsel katman başına kısa yöntem-yönlendirme cümlesi (analiz ne yapar + sayı nasıl okunur); yorum/verdict eklenmez, sayı değişmez.
- **F2-C (03↔04 uyum):** yöntem adları, hipotez ifadeleri, alt-ölçek etiketleri, kovaryat seti, FDR/Holm, H5 beş-strateji, ondalık/`p` biçimi birebir hizalanır.
- **F2-D (tam eksen):** düzenleme sonrası `/sci-audit:audit chapters/03_gerec_ve_yontem.qmd` ve `chapters/04_bulgular.qmd` --lang tr --strictness certification (A–G); blocker sıfırlanır; rapor `tez-yazim/04_kalite-kontrol/raporlar/` altına.

**Kısıt:** Bulgular yorumsuz kalır; sayılar kanonik kaynağa izlenebilir; KVKK sınırı korunur; commit onaylı kesme noktalarında.
