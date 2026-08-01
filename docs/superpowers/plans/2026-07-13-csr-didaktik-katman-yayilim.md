# CSR Didaktik Katman — Yayılım Uygulama Planı (§8–§10, §12–§16 + §6/§17)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pilot §11'de doğrulanan didaktik katmanı CSR'ın kalan teknik-taşıyan bölümlerine (§8, §9, §10, §12, §13, §14, §15, §16) teknik mini-bloğuyla; §6 Giriş ve §17 Tartışma'ya uyarlanmış anlatı-didaktik çerçeveyle yaymak.

**Architecture:** `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` in-place düzenlenir. İki şablon: (A) **teknik mini-blok** (§11'de doğrulanmış — Bilimsel soru / Yöntem & tatbik / Nasıl değerlendirilir), (B) **anlatı-didaktik çerçeve** (yeni — Bölümün sorusu / Yaklaşım & çerçeve / Nasıl okunmalı). R-chunk literalleri değişmez; bölüm-sonu verdict/karar blokları korunur.

**Tech Stack:** Quarto (.qmd), Türkçe Marmara format sözleşmesi, sci-audit (A/B/C/G), galileo advisory, `references/references.bib`, `/referans-kapisi` (yeni atıf).

## Global Constraints

(Kaynak: `docs/superpowers/specs/2026-07-13-csr-didaktik-aciklama-katmani-design.md` + pilot doğrulaması `tez-yazim/04_kalite-kontrol/raporlar/11-birincil-hipotez-sci-audit.md`)

- **Format:** Türkçe edilgen 3. tekil; ondalık **virgül**; mini-blok `**bold**` etiket (başlık değil, kaskad ≤4 bozulmaz); yazar-yıl konvansiyonu **"ve diğerleri"** (belge geneli; "ve ark." KULLANILMAZ — pilot gate bulgusu).
- **R-literal koruması:** ` ```{r ` blokları byte-düzeyinde değişmez. Baseline imza (her task'ta doğrulanır): `N_CHUNKS` + `CHUNK_HASH` (yayılım başında yeniden ölçülür; pilot sonrası HEAD üzerinden).
- **Kanonik sayı koruması:** hiçbir istatistik değeri/verdict değişmez.
- **Yinelenme yok:** teknik mini-blok parça 3 = a-priori ÖLÇÜT; bölüm-sonu `Karar/Kanonik Karar` blokları = VERDICT (dokunulmaz).
- **Atıf (KRİTİK — pilottan farklı):** Bu bölümler, özellikle §6 Giriş ve §17 Tartışma, mevcut `references.bib`'de olmayan literatür isteyebilir. **Önce mevcut künye yeniden kullanılır**; eksikse künye **Task 1 citation-reconnaissance**'ta işaretlenir ve metne girmeden önce **`/referans-kapisi`** (bağlam→DOI/PMID→tam metin→Zotero→ledger→iki-kol AI-reliability) kapatılır. Uydurma yasağı mutlak; doğrulanamayan = "VERİ BULUNAMADI".
- **Veri sınırı:** yalnız aggregate; satır/PII yok.
- **Keşifsel etiket:** §12, §15, §16 `[KEŞİFSEL · İKİNCİL]` bölümleridir; mini-bloklar bu etiketi korur, doğrulayıcı dil kullanmaz.
- **Nedensellik:** kesitsel → ilişkisel/betimsel; nedensel dil yok.
- **Anchor kuralı:** yukarıdan aşağıya, metin-çapalı Edit; her alt-başlığın (`## x.y` / `### x.y.z`) hemen altına, ilk sonuç/tablo/chunk'tan ÖNCE eklenir.

---

## Şablon A — Teknik Mini-Blok (doğrulanmış, §11 deseni)

Kaynak-örnek: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` §11 (commit `9b87136`). Yapı:

```markdown
**Bilimsel soru.** [veri + literatür bağlamında hangi soru; veri kısıtı]
**Yöntem & tatbik.** [teknik, ayırt edici özellik, bu veriye tatbik]
**Nasıl değerlendirilir.** [a-priori ölçüt: etki+GA/eşik/benchmark/keşifsel etiket/nedensellik sınırı]
```

## Şablon B — Anlatı-Didaktik Çerçeve (YENİ; §6 Giriş, §17 Tartışma)

Teknik değil; anlatı bölümünün okuyucuya yön veren çerçevesi. Bölüm başına **bir** kez, ilk `##` alt-başlıktan önce.

```markdown
**Bölümün sorusu.** [bu bölüm hangi bilimsel soruyu/boşluğu ele alıyor]
**Yaklaşım & çerçeve.** [hangi kuramsal/literatür çerçevesiyle; nasıl örgütlendiği]
**Nasıl okunmalı.** [okuyucuya yorum rehberi: bu bölüm ne yapar/ne yapmaz; sonraki bölümlerle bağ]
```

**§6 Giriş exemplar (tam taslak):**
```markdown
**Bölümün sorusu.** Tip 1 diyabetli çocukların, sağlıklı kardeşlerinin ve annelerinin oluşturduğu aile sisteminde ebeveynlik tutumu, anne depresyonu ve kardeş ilişkisi nasıl bir kuramsal zincir oluşturur; bu çalışma hangi boşluğu doldurur?

**Yaklaşım & çerçeve.** Bölüm, epidemiyolojik/klinik bağlamdan (T1DM ve aile sistemi) çoklu-informant kuramsal çerçeveye ve oradan çalışmanın özgün katkısına doğru genelden-özele örgütlenir; ebeveyn ve çocuk perspektiflerinin ayrışması bir ölçüm sorunu değil, kuramsal olarak bilgilendirici bir olgu olarak konumlandırılır.

**Nasıl okunmalı.** Bu bölüm literatürü *özetler ve boşluğu gerekçelendirir*; bulgu veya yorum içermez (onlar Bulgular ve Tartışma'dadır). Kuramsal zincir, §7 hipotezlerine ve §11 birincil bulgularına doğrudan eşlenir.
```

**§17 Tartışma exemplar (tam taslak):**
```markdown
**Bölümün sorusu.** Birincil (H1–H5) ve keşifsel bulgular, mevcut literatür karşısında nasıl konumlanır; hangi örüntüler yakınsar, hangileri ayrışır ve olası nedenleri nedir?

**Yaklaşım & çerçeve.** Her bulgu, benzer/farklı yön + olası neden ekseninde literatürle karşılaştırılır; çoklu-informant ayrışma (De Los Reyes ve diğerleri, 2015) ve etki-büyüklüğü kalibrasyonu (Pinquart, 2013) çerçeveleri konumlandırmanın omurgasıdır.

**Nasıl okunmalı.** Bu bölüm *yorumdur, hipotez testi değil*; bulgu ve istatistik değerlerini tekrar etmez, kesitsel tasarım nedeniyle nedensel iddia kurmaz. Sonuç ve öneriler §19'a bırakılır.
```

---

### Task 1: Citation reconnaissance (yeni-atıf önyükleme — gate)

**Files:** Read: hedef bölümler; Modify: `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md`

**Interfaces:** Produces: `MISSING_CITES` listesi (bölüm × iddia × aday künye) — sonraki drafting task'ları bunu tüketir.

- [ ] **Step 1: Yayılım baseline R-chunk imzasını kaydet**

```bash
python3 - <<'PY'
import re, hashlib
t = open("docs/CLINICAL-STUDY-REPORT-FINAL.qmd", encoding="utf-8").read()
b = re.findall(r'^```\{r.*?^```', t, re.M | re.S)
print("N_CHUNKS =", len(b), "CHUNK_HASH =", hashlib.md5("".join(b).encode()).hexdigest())
PY
```
Expected: değerler NOT EDİLİR (yayılım boyunca değişmemeli).

- [ ] **Step 2: Mevcut atıf envanterini çıkar**

```bash
grep -oE '\[@[a-zA-Z0-9_:-]+\]' references/references.bib docs/CLINICAL-STUDY-REPORT-FINAL.qmd 2>/dev/null | sort -u > /tmp/mevcut_atif.txt || true
grep -oE '@[a-z]+[0-9]{4}' references/references.bib | sort -u | head -50
```
Expected: mevcut künye anahtarları listesi (yeniden kullanım havuzu).

- [ ] **Step 3: Her hedef bölüm için, mini-blok "Bilimsel soru/Bölümün sorusu" parçasının literatür bağlamı gerektirdiği yerleri işaretle**

§6 Giriş ve §17 Tartışma yüksek olasılıkla mevcut künyelerle karşılanır (zaten literatür-yoğun); §8–§16 teknik mini-blokları pilottaki gibi çoğunlukla **yöntemsel** çerçeve olduğundan yeni atıf gerektirmez (metodoloji ifadeleri kaynak-serbesttir; yalnız benchmark/karşılaştırma iddiası atıf ister). Her gerçek yeni-atıf ihtiyacı `MISSING_CITES`'a yazılır.

- [ ] **Step 4: MISSING_CITES boş değilse her künye için `/referans-kapisi`**

Run (her künye): `/referans-kapisi "<künye>"` → cite-ok olana kadar. Kapanmayan künye O İDDİAYI metne sokmaz ("VERİ BULUNAMADI").
Expected: `MISSING_CITES`'daki her satır ya cite-ok ya da gap.

- [ ] **Step 5: Commit (ledger güncellemesi varsa)**

```bash
git add tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md references/references.bib
git commit -m "docs(csr): yayılım citation-reconnaissance — yeni künyeler cite-ok (referans kapısı)"
```

---

### Task 2: §8 Yöntem (13 alt-başlık → hafif teknik mini-blok)

**Files:** Modify: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` §8

**Interfaces:** Consumes: baseline imza. Produces: §8'de alt-başlık başına kompakt mini-blok.

- [ ] **Step 1: Her alt-başlığa Şablon A (kompakt) uygula**

§8 zaten yöntemi *tarif ettiğinden* burada mini-blok **kompakt**tır: "Bilimsel soru" (bu adım neyi çözer) + "Nasıl değerlendirilir" (a-priori ölçüt) vurgulu; "Yöntem & tatbik" mevcut anlatıya kısa köprü. Alt-başlıklar ve teknik: 8.1 tasarım · 8.2 örneklem · 8.3 ölçüm araçları · 8.4 reprodüksiyon · 8.5 eksik veri (FIML/MI m=50) · 8.6 DAG · 8.7 SES latent · 8.8 eğilim skoru · 8.9 birincil test yöntemleri · 8.10 çoklu karşılaştırma (FDR) · 8.11 duyarlılık üçlüsü (multiverse/TOST/sensemakr) · 8.12 Bayesçi hat · 8.13 sayısal hassasiyet. Her biri için mini-blok, çapası `## 8.x` başlığının hemen altı.

- [ ] **Step 2: R-literal + Commit** (imza doğrula; `git commit -m "docs(csr): §8 Yöntem didaktik mini-bloklar"`).

---

### Task 3: §9 Tanımlayıcı Bulgular

**Files:** Modify §9. **Teknik daneleri:** 9.1 örneklem akışı (STROBE) · 9.2 Tablo 1 + SMD denge · 9.3 demografik yorum · 9.4 DM klinik profil · 9.5 eksik veri profili.

- [ ] **Step 1:** 9.1'e STROBE akış + 9.2'ye Tablo1/SMD-denge mini-bloğu (bilimsel soru: gruplar temelde dengeli mi; yöntem: standardize ortalama fark |SMD|; ölçüt: |SMD|<0,10 iyi denge). 9.5'e eksik-veri karakterizasyonu (MCAR/MAR/MNAR + structural missing) mini-bloğu. 9.3/9.4 saf yorum → mini-blok yerine kısa çerçeve cümlesi (opsiyonel).
- [ ] **Step 2:** R-literal + Commit.

---

### Task 4: §10 Psikometrik Bulgular

**Files:** Modify §10. **Teknik daneleri:** 10.1 α + ω · 10.2 faktör yapısı (CFA) · 10.3 taban etkisi · 10.4 ölçüm değişmezliği · 10.5 kriter/eşzamanlı geçerlik · 10.6 genel karar.

- [ ] **Step 1:** 10.1–10.5'e Şablon A. Örn 10.1: soru=alt ölçekler iç tutarlı mı; yöntem=Cronbach α + McDonald ω (ω tau-eşdeğerlik varsaymaz, α'ya üstün); ölçüt=ω≥0,70 kabul, düşük α tarihsel EMBU-C bağlamında (α .49–.69) okunur. 10.4 ölçüm değişmezliği = pilot §11.4.3 deseni. 10.6 (karar) verdict → dokunulmaz.
- [ ] **Step 2:** R-literal + Commit.

---

### Task 5: §12 Aracılık/LPA/Ağ/Klinik Fayda [KEŞİFSEL]

**Files:** Modify §12. **Teknik daneleri:** 12.1 aracılık (Beck→EMBU-P→EMBU-C) · 12.2 LPA (anne tipolojisi) · 12.3 ağ analizi (GGM) · 12.4 klinik fayda (ROC/AUC/kalibrasyon/DCA) · 12.5 DM klinik alt-analiz.

- [ ] **Step 1:** Her `## 12.x`'e Şablon A + `[KEŞİFSEL]` disiplini. İçerik kaynakları: `references/mediation-modelleri.md`, `latent-degisken-yontemleri.md`, `network-analizi.md`, `klinik-fayda.md`. Örn 12.3: soru=semptom/boyutlar arası koşullu bağımlılık yapısı; yöntem=EBIC-LASSO GGM (kısmi korelasyon; koşullu bağımlılık ≠ nedensellik); ölçüt=kenar stabilitesi (CS-coefficient bootstrap), merkeziyet dikkatli. 12.4: ROC/AUC + Youden + DCA net fayda + iç validasyon (optimism düzeltme) zorunlu.
- [ ] **Step 2:** R-literal + Commit.

---

### Task 6: §13 Robustluk ve Sensitivite

**Files:** Modify §13. **Teknik daneleri:** 13.1 multiverse (specification curve) · 13.2 TOST · 13.3 sensemakr RV + E-value · 13.4 negatif kontrol/falsifikasyon.

- [ ] **Step 1:** Her `## 13.x`'e Şablon A. Kaynak `references/robustluk-ve-sensitivite.md`. Örn 13.1: soru=bulgu analitik-esneklik seçimlerine dayanıklı mı; yöntem=specr çok-evren + Simonsohn inferential test (permütasyon); ölçüt=spec dağılımının çoğunluğu + cherry-pick yok. 13.3: sensemakr Robustness Value + VanderWeele E-value; ölçüt=RV gözlenen kovaryat gücüne göre.
- [ ] **Step 2:** R-literal + Commit.

---

### Task 7: §14 Bayesçi Paralel Hat

**Files:** Modify §14. **Teknik daneleri:** 14.1 çift raporlama · 14.2 MCMC tanıları · 14.3 yönetici yorum.

- [ ] **Step 1:** 14.1'e Şablon A (soru=frekentist bulgu Bayesçi kanıtla örtüşüyor mu; yöntem=brms + Savage-Dickey BF + ROPE; ölçüt=BF Jeffreys + R̂≤1,01/ESS/divergent=0). 14.2 MCMC tanıları mini-bloğu (yöntem=R̂/ESS/Pareto-k; ölçüt=yakınsama eşikleri). 14.3 verdict → dokunulmaz.
- [ ] **Step 2:** R-literal + Commit.

---

### Task 8: §15 Çok-informant/Sağlamlık [KEŞİFSEL] (11 alt-başlık, 15 chunk)

**Files:** Modify §15. **En yoğun bölüm.** Teknik daneleri: 15.3 çok-informant yapısal · 15.4 psikometrik robustleştirme · 15.5 antidepresan/mental yük · 15.6 H5 ext · 15.7 HbA1c stratifikasyon · 15.8 nedensel aracılık/DAG/dağılımsal · 15.9 multiverse/meta · 15.10 klinik karar/replikasyon. (15.1/15.2/15.11 statü/özet/karar → çerçeve cümlesi, verdict korunur.)

- [ ] **Step 1:** 15.3–15.10'a Şablon A + `[KEŞİFSEL]`. Bölüm büyük olduğundan alt-gruplar hâlinde işlenip **tek commit** yerine 2 commit (15.3–15.6, 15.7–15.10) uygundur.
- [ ] **Step 2:** R-literal + Commit(ler).

---

### Task 9: §16 Sosyodemografik/Bağlamsal [KEŞİFSEL] (14 alt-başlık)

**Files:** Modify §16. Teknik daneleri: 16.3 diferansiyel ebeveynlik etki (PDT) · 16.4 sosyal tabakalaşma · 16.5 anne komorbidite · 16.6 aile yapısı/konstelasyon · 16.7 DM maruziyet yoğunluğu · 16.8 anne mental yük yansıması · 16.9 yönlü kardeş-ilişki topografi · 16.10 moderatörler (cinsiyet/anne yaşı) · 16.11 klinik zamanlama/metabolik · 16.13 ebeveyn yaş farkı (assortatif) · 16.14 seçilim/alım-dönemi geçerlik. (16.1/16.2/16.12 statü/matris/denetim → çerçeve.)

- [ ] **Step 1:** İlgili `## 16.x`'e Şablon A + `[KEŞİFSEL]`. 2 commit uygun (16.3–16.8, 16.9–16.14).
- [ ] **Step 2:** R-literal + Commit(ler).

---

### Task 10: §6 Giriş — Anlatı-didaktik (Şablon B)

**Files:** Modify §6.

- [ ] **Step 1:** §6 başlığının hemen altına (ilk `## 6.1`'den önce) Şablon B §6 exemplar'ını (yukarıda tam taslak) ekle. Yeni atıf gerekiyorsa Task 1 cite-ok künyeleri kullanılır.
- [ ] **Step 2:** R-literal + Commit.

---

### Task 11: §17 Tartışma — Anlatı-didaktik (Şablon B)

**Files:** Modify §17.

- [ ] **Step 1:** §17 başlığının hemen altına Şablon B §17 exemplar'ını ekle. Tartışma zaten atıf-yoğun → mevcut künyeler; yeni gerekiyorsa cite-ok.
- [ ] **Step 2:** R-literal + Commit.

---

### Task 12: Tam-doküman denetim kapısı

**Files:** Read/verify CSR; Create: `tez-yazim/04_kalite-kontrol/raporlar/csr-yayilim-sci-audit.md`

- [ ] **Step 1:** R-chunk imzası Task 1 baseline ile aynı (tüm yayılım boyunca literal değişmedi).
- [ ] **Step 2:** İzole eklemeler axis-G (`tr_sciaudit --strictness certification`): 0 `decimal-dot-p-value`, 0 `encoding-error`, 0 "ve ark." kalıntı.
- [ ] **Step 3:** Yeni `[@key]` varsa hepsi `references.bib`'de + ledger cite-ok (Task 1 ile mutabık).
- [ ] **Step 4:** `/sci-audit:audit docs/CLINICAL-STUDY-REPORT-FINAL.qmd --lang tr --strictness certification` — error/blocker sıfır.
- [ ] **Step 5:** Galileo advisory (`galileo_reference_prose`/`coherence` + healthcheck) — soft-block yok.
- [ ] **Step 6:** `quarto render docs/CLINICAL-STUDY-REPORT-FINAL.qmd` — exit 0 (literaller korunduğundan kırılmamalı).
- [ ] **Step 7:** Rapor yaz + commit; kullanıcıya kapanış özeti.

---

## Self-Review

**1. Spec/kapsam coverage:** Kullanıcı seçimi (teknik bölümler + §8 + Giriş/Tartışma) → Task 2 (§8), 3 (§9), 4 (§10), 5 (§12), 6 (§13), 7 (§14), 8 (§15), 9 (§16) teknik mini-blok; Task 10 (§6), 11 (§17) anlatı-didaktik. Anlatı/ön-arka kalan bölümler (§1-5,7,18-23) kapsam dışı (teknik yok) — bilinçli.
**2. Placeholder scan:** İki şablon tanımlı; Şablon B iki exemplar tam taslak; teknik bölümler için envanter + içerik-noktaları + doğrulanmış §11 deseni referansı. Drafting execution'da §11 desenine göre yapılır (validated-template propagation).
**3. Atıf riski:** Task 1 citation-reconnaissance yeni-atıf ihtiyacını front-load eder; gate kapanmadan iddia metne girmez — plan boyunca invaryant.
**4. Type/anchor consistency:** Tüm çapalar gerçek `## x.y`/`### x.y.z` başlıklarıyla eşleşti (grep doğrulandı). `CHUNK_HASH`/`N_CHUNKS` imzası Task 1'de tanımlı, her task aynı ada karşı kontrol eder. Konvansiyon "ve diğerleri" Global Constraints'te sabit (pilot gate dersi).

## Notlar

- **Yürütme ölçeği büyük** (~11 bölüm, ~50+ mini-blok). Bağımsız-bölüm yapısı **workflow fan-out**a uygundur (her bölüm bir alt-ajan; şablon + verification gate + adversaryel literal-koruma kontrolü). Alternatif: subagent-driven-development (bölüm başına taze alt-ajan + inceleme).
- **§8 ve Giriş/Tartışma** en fazla atıf-hassas; Task 1 bunları önceler.
- Her task bağımsız test-edilebilir (literal-koruma + axis-G) ve ayrı commit'lenir.
