# evidentia Tez Narratif Derin-Literatür Modu — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** evidentia'yı bu repoda tez-narratif-derin-lit (SR değil) modunda çalıştıran yapılandırma + davranış-doktrini + rota + `/tez-literatur` komutu + custom Enstitü AMA-11 CSL kurmak.

**Architecture:** evidentia PRISMA komutları değişmeden kalır; narratif mod repo katmanına (evidentia extension doktrini §1.5/§1.6) eklenir. 3-katman sınırı: evidentia getirir → t1dm-tez-rehberi üretir → sci-audit denetler. Referans render'ı APA→Enstitü AMA-11 CSL'e taşınır.

**Tech Stack:** Markdown/YAML (config + doktrin + komut), CSL 1.0.2 XML (citeproc), Quarto/pandoc-citeproc (render), BibTeX (`references/references.bib`), Python (YAML validasyonu).

## Global Constraints

- **Dil:** tez/çıktı Türkçe; edilgen 3. tekil. Kaynak: spec §5②.
- **Referans render:** metin-içi yazar-yıl (`[@key]`); kaynakça Enstitü AMA-11 alfabetik; **italik/kalın yok**. Kaynak: kanonik §1.8 + §4.
- **et-al KARARI (onaylı):** global **"ve ark."** (default-locale tr, embedded `<locale>` term override). İngilizce kaynakta da "ve ark.".
- **DOI KARARI (onaylı):** standart `https://doi.org/<DOI>` (kılavuz örneğindeki fazladan `doi:` alınmaz).
- **Bibliyografya yapısal terimleri (In:/editors/ed.):** İngilizce AMA (literatür çoğunluğu İngilizce; makalelerde yapısal terim yok). Türkçe kitap bölümü nadirdir → YAGNI, gerekirse elle düzeltilir.
- **evidentia format-agnostik:** yalnız gerçek BibTeX künyesi + `[@key]` üretir; elle biçimlenmiş kaynakça string üretmez.
- **KVKK:** connector'a **yalnız literatür terimi** — katılımcı/ham/aile-düzeyi veri/kimlikleyici asla.
- **UYDURMA REFERANS YASAĞI:** her künye gerçek DOI/PMID/YÖK-ID veya "VERİ BULUNAMADI".
- **Dokunulmaz:** plugin iç dosyaları (`~/.claude/plugins/.../evidentia`), `.claude/settings.json permissions.deny`, `.env` (Read/Bash deny), ham veri katmanları.
- **Commit:** repo kuralı #14 — **yalnız kullanıcı açıkça isteyince**; `git add .` yasak. Aşağıdaki "Commit" adımları tamamlık için gösterilir; yürütmede tek yetkili commit'te toplanır.
- **apa.csl silinmez** (arşiv olarak kalır).

## File Structure

| Dosya | Sorumluluk | Durum |
|---|---|---|
| `references/marmara-ama11.csl` | Enstitü AMA-11 custom CSL (yazar-yıl in-text + AMA alfabetik bib) | YENİ, tracked |
| `references/_csl_test/test-refs.bib` + `test.qmd` | CSL render smoke-test koşum takımı | YENİ, tracked (küçük) |
| `_quarto.yml` | `csl:` → marmara-ama11.csl rewire | MODIFY |
| `.claude/evidentia.local.md` | evidentia yerel yapılandırma (knob + proje-modu banner) | YENİ, **git-ignored** |
| `.gitignore` | `.claude/evidentia.local.md` satırı | MODIFY |
| `.claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md` | §Narratif Derin-Lit Modu doktrini | MODIFY |
| `.claude/skills/t1dm-tez-rehberi/SKILL.md` | Faz 1.5 narratif-mod varsayılan + entry-points satırı | MODIFY |
| `.claude/commands/tez-literatur.md` | `/tez-literatur <bölüm> <konu>` komutu | YENİ, tracked |
| `CONVENTIONS.md` (+ audit ikizi) | rule 7 narratif-mod notu (tutarlılık) | MODIFY |

---

### Task 1: Enstitü AMA-11 custom CSL + render smoke-test

**Files:**
- Create: `references/_csl_test/test-refs.bib`
- Create: `references/_csl_test/test.qmd`
- Create: `references/marmara-ama11.csl`

**Interfaces:**
- Produces: `references/marmara-ama11.csl` — Task 2 bunu `_quarto.yml csl:`'e bağlar.

- [ ] **Step 1: Yaz — deterministik test bib (5 künye, §4.3 şekilleri)**

`references/_csl_test/test-refs.bib`:

```bibtex
@article{fadini2022,
  author = {Fadini, Gian Paolo and Del Prato, Stefano and Avogaro, Angelo and Solini, Anna},
  title = {Challenges and opportunities in real-world evidence on the renal effects of sodium-glucose cotransporter-2 inhibitors},
  journaltitle = {Diabetes, Obesity and Metabolism},
  shortjournal = {Diabetes Obes Metab},
  date = {2022}, volume = {24}, number = {2}, pages = {177-186},
  doi = {10.1111/dom.14599}, langid = {english}
}
@article{xie2019,
  author = {Xie, Y and Shi, X and Sheng, K and Han, G and Li, W and Zhao, Q and Jiang, L and Zhou, T},
  title = {PI3K/Akt signaling transduction pathway, erythropoiesis and glycolysis in hypoxia},
  shortjournal = {Mol Med Rep}, date = {2019}, volume = {19}, number = {2}, pages = {783-791},
  doi = {10.3892/mmr.2018.9713}, langid = {english}
}
@article{dilek2024,
  author = {Dilek, B and Songür, K and Erdinç Gündüz, N and Ellidokuz, H and Başçı, O and Gülbahar, S and Akalın, E},
  title = {Lateral epikondilit tanılı hastalarda klinik ve ultrasonografik bulgular ile tedavi değişimi arasındaki ilişki: 6 aylık sonuçlar},
  shortjournal = {DEU Tıp Derg}, date = {2024}, volume = {38}, number = {3}, pages = {251-262}, langid = {turkish}
}
@incollection{nestler2018,
  author = {Nestler, Eric J and Hyman, Steven E},
  title = {Molecular mechanisms of antidepressant action},
  booktitle = {Goodman \& Gilman's Pharmacological Basis of Therapeutics},
  editor = {Brunton, Laurence L and Hilal-Dandan, Randa and Knollmann, Björn C},
  edition = {13}, publisher = {McGraw-Hill}, location = {New York}, date = {2018},
  pages = {257-276}, langid = {english}
}
@article{john2017,
  author = {John, Thomas A and Marquez, Bianca R},
  title = {A two author test entry for the ve conjunction},
  shortjournal = {J Test Ref}, date = {2017}, volume = {5}, number = {1}, pages = {10-15},
  doi = {10.1000/test.2017}, langid = {english}
}
```

- [ ] **Step 2: Yaz — test .qmd (beklenen çıktı yorumda sabitlenir)**

`references/_csl_test/test.qmd`:

```markdown
---
title: "CSL smoke-test — Enstitü AMA-11"
bibliography: test-refs.bib
csl: ../marmara-ama11.csl
lang: tr
nocite: |
  @fadini2022, @xie2019, @dilek2024, @nestler2018, @john2017
---

Metin-içi denemeler:
- 4 yazar (parenthetical): [@fadini2022] → beklenen: (Fadini ve ark., 2022)
- 4 yazar (narrative): @fadini2022 → beklenen: Fadini ve ark. (2022)
- 2 yazar: [@john2017] → beklenen: (John ve Marquez, 2017)
- çoklu: [@fadini2022; @xie2019] → beklenen: (Fadini ve ark., 2022; Xie ve ark., 2019)

## Kaynaklar
::: {#refs}
:::

<!-- BEKLENEN KAYNAKÇA (alfabetik; italik/kalın yok; standart doi):
Dilek B, Songür K, Erdinç Gündüz N, Ellidokuz H, Başçı O, Gülbahar S, ve ark. Lateral epikondilit tanılı hastalarda klinik ve ultrasonografik bulgular ile tedavi değişimi arasındaki ilişki: 6 aylık sonuçlar. DEU Tıp Derg. 2024;38(3):251-262.
Fadini GP, Del Prato S, Avogaro A, Solini A. Challenges and opportunities in real-world evidence on the renal effects of sodium-glucose cotransporter-2 inhibitors. Diabetes Obes Metab. 2022;24(2):177-186. https://doi.org/10.1111/dom.14599
John TA, Marquez BR. A two author test entry for the ve conjunction. J Test Ref. 2017;5(1):10-15. https://doi.org/10.1000/test.2017
Nestler EJ, Hyman SE. Molecular mechanisms of antidepressant action. In: Brunton LL, Hilal-Dandan R, Knollmann BC, editors. Goodman & Gilman's Pharmacological Basis of Therapeutics. 13th ed. New York: McGraw-Hill; 2018. p. 257-276.
Xie Y, Shi X, Sheng K, Han G, Li W, Zhao Q, ve ark. PI3K/Akt signaling transduction pathway, erythropoiesis and glycolysis in hypoxia. Mol Med Rep. 2019;19(2):783-791. https://doi.org/10.3892/mmr.2018.9713
-->
```

- [ ] **Step 3: Render'ı çalıştır — CSL yokken FAIL/uyumsuzluk doğrula**

Run: `cd references/_csl_test && quarto render test.qmd --to plain 2>&1 | tail -30`
Expected: `marmara-ama11.csl` henüz yok → citeproc hata verir veya (varsa apa.csl fallback yok) render çöker. Bu, CSL'in gerekli olduğunu kanıtlar.

- [ ] **Step 4: Yaz — `references/marmara-ama11.csl` (CSL 1.0.2 author-date, aşağıdaki KESİN sözleşmeye göre)**

CSL yapı sözleşmesi (execution bu sözleşmeye göre XML üretir, Step 5 render'la doğrular):

- Kök: `<style xmlns="http://purl.org/net/xbiblio/csl/1.0" version="1.0.2" class="in-text" default-locale="tr">`.
- `<info>`: title "Marmara Enstitü AMA-11 (yazar-yıl)", id, updated.
- **Embedded `<locale>` (xml:lang yok → global term override):**
  - `<term name="et-al">ve ark.</term>` (+ form="short" aynı)
  - `<term name="and">ve</term>` (metin-içi "ve" için citation'da `and="text"`)
  - `<term name="in">In:</term>`, `<term name="editor" form="verb-short">editors</term>` veya AMA "editors" — İngilizce yapısal (Global Constraint).
  - `<term name="edition" form="short">ed.</term>`, `<term name="page" form="short">p.</term>`.
- **Makrolar:**
  - `author`: `<names variable="author">` → `<name and="text" delimiter=", " initialize-with="" name-as-sort-order="all" sort-separator=" " et-al-min="7" et-al-use-first="6"/>` → çıktı "Fadini GP" (soyad + baş harfler bitişik, nokta yok). `<et-al term="et-al"/>`. NOT: initialize-with="" + `<name form="short">` yerine AMA baş-harf birleşik için `initialize-with=""` ve `<name>` given'ı initial'a çevirir; render-test ile ayarlanır.
  - `author-short` (metin-içi): `<name form="short" and="text" delimiter=", " et-al-min="3" et-al-use-first="1"/>` → "Fadini" / "Fadini ve ark." / "John ve Marquez".
  - `issued-year`: `<date variable="issued"><date-part name="year"/></date>` + `year-suffix`.
  - `container`: `<text variable="container-title" form="short"/>` (kısaltma; `shortjournal` alanı sağlar).
  - `access-doi`: `<text variable="DOI" prefix="https://doi.org/"/>` (standart, `doi:` yok).
- **`<citation>`:** `<layout prefix="(" suffix=")" delimiter="; ">` → `author-short` + `, ` + `issued-year`. `disambiguate-add-year-suffix="true"`. `et-al-min="3" et-al-use-first="1"`.
- **`<bibliography>`:** `<sort><key macro="author"/><key variable="issued"/></sort>`. `<layout suffix=".">`:
  - makale: `author`. ` `. title. ` `. container. ` `. `issued-year`;`volume`(`issue`):`pages`. ` `. doi. — italik/kalın YOK (hiçbir yerde `font-style`/`font-weight`).
  - kitap bölümü (`type="chapter"`): author. title. `In:` editor `editors.` booktitle. `edition ed.` publisher-place: publisher; year. `p.` pages.
  - `et-al-min="7" et-al-use-first="6"`.

- [ ] **Step 5: Render'ı çalıştır — beklenen çıktıyla eşleştir, uyana kadar CSL'i düzelt**

Run: `cd references/_csl_test && quarto render test.qmd --to plain 2>&1 | tail -40`
Expected: Kaynakça 5 künye **alfabetik** (Dilek, Fadini, John, Nestler, Xie); her satır Step 2 yorumundaki BEKLENEN ile karakter-düzeyinde eşleşir (italik yok, `ve ark.` global, `https://doi.org/` standart, `In:`/`editors`/`ed.` İngilizce). Metin-içi: "(Fadini ve ark., 2022)", "Fadini ve ark. (2022)", "(John ve Marquez, 2017)", çoklu "; " ayraçlı. Eşleşene kadar CSL makro/term'lerini düzelt ve yeniden render et.

- [ ] **Step 6: Commit** (governance: yürütmede tek yetkili commit'te toplanır)

```bash
git add references/marmara-ama11.csl references/_csl_test/
git commit -m "feat(refs): Enstitü AMA-11 custom CSL + render smoke-test"
```

---

### Task 2: `_quarto.yml` CSL rewire + tam render smoke

**Files:**
- Modify: `_quarto.yml` (`csl:` satırı)

**Interfaces:**
- Consumes: `references/marmara-ama11.csl` (Task 1).

- [ ] **Step 1: `_quarto.yml`'de mevcut csl satırını doğrula**

Run: `grep -n 'csl:' _quarto.yml`
Expected: `csl: references/apa.csl` (veya benzeri) tek satır.

- [ ] **Step 2: csl satırını yeni CSL'e çevir**

`_quarto.yml` içinde `csl: references/apa.csl` → `csl: references/marmara-ama11.csl`. (apa.csl dosyası silinmez; yalnız referans değişir.)

- [ ] **Step 3: Tam tezi render et — bozulmadığını doğrula**

Run: `quarto render 2>&1 | tail -40`
Expected: Hatasız tamamlanır; `outputs/quarto/` üretilir. Kaynakça bölümü AMA-11 biçiminde (alfabetik, italik yok). Render 126 künyeyi işler.

- [ ] **Step 4: Kaynakça çıktısını göz-doğrula (3 künye örnekle)**

Run: `grep -A2 -i 'diabetes\|pinquart\|ispad' outputs/quarto/*.html 2>/dev/null | head -20` (veya docx → pandoc plain).
Expected: Örnek künyeler AMA-11 düzeninde (`Yazar. Başlık. Derg. Yıl;Cilt(Sayı):Sayfa. https://doi.org/…`), italik/kalın yok.

- [ ] **Step 5: Commit**

```bash
git add _quarto.yml
git commit -m "build(refs): kaynakça render'ını apa.csl'den Enstitü AMA-11'e taşı"
```

---

### Task 3: `.claude/evidentia.local.md` + `.gitignore`

**Files:**
- Create: `.claude/evidentia.local.md`
- Modify: `.gitignore`

**Interfaces:**
- Produces: evidentia Adım 0.1'in okuyacağı yerel yapılandırma; köprü §Narratif Derin-Lit Modu'na (Task 4) işaret eder.

- [ ] **Step 1: `.gitignore`'a satır ekle**

`.gitignore` içindeki mevcut Minerva bloğuna ekle:

```gitignore
# evidentia yerel yapılandırma (operatör-yerel, git-ignore konvansiyonu)
.claude/evidentia.local.md
```

- [ ] **Step 2: Yaz — `.claude/evidentia.local.md`**

```markdown
---
enabled: true
known_connected:
  - pubmed-epmc
  - openalex
  - semantic-scholar
  - anamnesis
  - evidentia-kb
  - annas-reader
  - openathens
  - yok-akademik
  - minerva-evidence
fulltext_tier: copyright_gated
completeness_gate: standard
auto_ingest_rag: true
default_modules: []
---

# evidentia — Proje Modu (T1DM-Tez)

**Varsayılan çalışma modu = TEZ NARRATİF DERİN-LİT (systematic review DEĞİL).**
PRISMA akış-diyagramı / RoB / GRADE / tarama-kapısı yalnız kullanıcı açıkça
"sistematik derleme" veya "kapsam derlemesi" derse çalışır.

Narratif-mod doktrini (bağlayıcı):
`.claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md`
§"Narratif Derin-Lit Modu (tez; SR değil)".

Çıktı sözleşmesi: Türkçe edilgen 3. tekil; metin-içi yazar-yıl `[@key]`
("ve"/"ve ark."); ondalık virgül + baştan sıfır; kaynakça biçimini CSL
(`references/marmara-ama11.csl`) render eder — evidentia format-agnostik
BibTeX + `[@key]` üretir.

KVKK: connector'lara **yalnız literatür arama terimi** gider; katılımcı/ham/
aile-düzeyi veri, transkript veya kimlikleyici asla gönderilmez.
```

- [ ] **Step 3: YAML frontmatter geçerliliğini doğrula**

Run: `python3 -c "import yaml,sys; d=yaml.safe_load(open('.claude/evidentia.local.md').read().split('---')[1]); print('OK keys:', sorted(d)); assert d['enabled'] is True and 'minerva-evidence' in d['known_connected']"`
Expected: `OK keys: ['auto_ingest_rag', 'completeness_gate', 'default_modules', 'enabled', 'fulltext_tier', 'known_connected']`

- [ ] **Step 4: git-ignore edildiğini doğrula**

Run: `git check-ignore .claude/evidentia.local.md && git status --porcelain .claude/evidentia.local.md`
Expected: birinci komut yolu basar (ignore'lu); ikinci komut **boş** (untracked görünmez).

- [ ] **Step 5: Commit** (yalnız `.gitignore` tracked)

```bash
git add .gitignore
git commit -m "chore(evidentia): yerel yapılandırma git-ignore + proje-modu"
```

---

### Task 4: Köprü §Narratif Derin-Lit Modu doktrini

**Files:**
- Modify: `.claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md`

**Interfaces:**
- Consumes: D0-D6 kaskad (§0.3, mevcut), Minerva §1.2 (mevcut).
- Produces: `§Narratif Derin-Lit Modu (tez; SR değil)` — Task 5 SKILL Faz 1.5 ve Task 6 komut buna işaret eder.

- [ ] **Step 1: Ekleme noktasını bul**

Run: `grep -n '^## \|^# ' .claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md | head -40`
Expected: §0.3 kaskad ve §1.1/§1.2 başlıkları görünür; yeni bölümü §1.2'den sonra (veya kaskad tablosunun hemen ardına) eklemek için satır no belirle.

- [ ] **Step 2: Yaz — yeni bölüm (uygun satıra ekle)**

```markdown
## Narratif Derin-Lit Modu (tez; SR değil)

> Bu repoda literatür işinin **varsayılan** modu. `/evidentia` PRISMA hattı
> yalnız kullanıcı açıkça "sistematik/kapsam derleme" derse çalışır.

**Kaskad alt-kümesi:** D0 → D1 → D2 → D4 → D5 → D6. **ATLA:** PRISMA akış-
diyagramı, tarama-kapısı, RoB2/ROBINS-I/QUADAS-2, GRADE/SoF. (Bunlar SR
modunda kalır.)

**Çıktı sözleşmesi (Marmara):** Türkçe edilgen 3. tekil; metin-içi yazar-yıl
`[@key]` (2 yazar "ve"; 3+ "ilk-yazar ve ark."; çoklu `;`); ondalık virgül +
baştan sıfır; kaynakça biçimini CSL (`references/marmara-ama11.csl`) render
eder — **format-agnostik BibTeX + `[@key]`** üret, elle biçimli kaynakça
string üretme.

**Bölüm hedefleme:**
- *Giriş ve Amaç:* literatür **özet**, alt başlık yok; boşluk + önem + amaç.
- *Genel Bilgiler:* genelden özele, güncel literatür özeti, **yorum/sonuç
  çıkarımından kaçın**; 7 alt-başlık H1–H5'e eşlenir.
- *Tartışma ve Sonuç:* **karşılaştır-literatürle** — benzer/farklı yön +
  muhtemel neden; hipotez destek beyanı; bulgu/istatistik **tekrarı yok**;
  Giriş/Genel Bilgiler tekrarı yok; sonda Sonuç + öneriler. Karma-yöntem
  etiketi (uyum/tamamlayıcılık/ayrışma/genişleme); nitel tema ≠ etki büyüklüğü.

**Sentez motoru:** `/evidentia:evidentia-synthesize` + `evidence-synthesizer`
alt-ajanı (ağır fan-out) + anamnesis GraphRAG. Minerva `minerva_literature_search`
(D2) + `minerva_*_fulltext`/`get_article` (D4, annas ÖNCESİ).

**Bağlayıcı gate'ler:** UYDURMA REFERANS YASAĞI; PRIOR/HARKing tuzağı (veri
sonrası literatür yalnız Tartışma yorumu veya `[KEŞİFSEL]`); **KVKK — yalnız
literatür terimi**; tez kaynak olamaz (§4.2); web ≤%5 yalnız .gov/.int/.eu.

**Giriş noktası:** `/tez-literatur <bölüm> <konu>` (bölüm ∈ giris|genel-bilgiler|
tartisma) veya doğrudan t1dm-tez-rehberi Faz 1.5.
```

- [ ] **Step 3: Bölümün eklendiğini doğrula**

Run: `grep -n 'Narratif Derin-Lit Modu' .claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md`
Expected: en az 1 eşleşme (yeni başlık).

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md
git commit -m "docs(bridge): narratif derin-lit modu (SR değil) doktrini"
```

---

### Task 5: SKILL.md Faz 1.5 narratif-mod varsayılanı + entry-points satırı

**Files:**
- Modify: `.claude/skills/t1dm-tez-rehberi/SKILL.md`

**Interfaces:**
- Consumes: köprü §Narratif Derin-Lit Modu (Task 4); `/tez-literatur` komutu (Task 6).

- [ ] **Step 1: Faz 1.5 + entry-points tablosunu bul**

Run: `grep -n 'Faz 1.5\|/evidentia-kol\|evidence-synthesizer\|minerva_literature_search' .claude/skills/t1dm-tez-rehberi/SKILL.md`
Expected: Faz 1.5 başlığı ve giriş-noktaları tablosunun satır aralığı (≈250-258) görünür.

- [ ] **Step 2: Faz 1.5'e varsayılan-mod cümlesi ekle**

Faz 1.5 gövdesine, delegation kuralının hemen ardına ekle:

```markdown
**Varsayılan mod (bu repo):** Giriş/Genel Bilgiler/Tartışma literatür işi
**narratif derin-lit** modunda yürür (bkz. köprü §"Narratif Derin-Lit Modu";
PRISMA akış/RoB/GRADE yok). PRISMA P0→P7 yalnız kullanıcı açıkça
"sistematik/kapsam derleme" isterse (`/evidentia:evidentia`).
```

- [ ] **Step 3: Entry-points tablosuna satır ekle**

Giriş-noktaları tablosuna (minerva satırından sonra) ekle:

```markdown
| `/tez-literatur <bölüm> <konu>` | Marmara narratif derin-lit (SR değil); bölüm ∈ giris\|genel-bilgiler\|tartisma |
```

- [ ] **Step 4: Değişiklikleri doğrula**

Run: `grep -n 'narratif derin-lit\|/tez-literatur' .claude/skills/t1dm-tez-rehberi/SKILL.md`
Expected: en az 2 eşleşme (Faz 1.5 cümlesi + tablo satırı).

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/t1dm-tez-rehberi/SKILL.md
git commit -m "docs(skill): Faz 1.5 narratif-mod varsayılanı + /tez-literatur girişi"
```

---

### Task 6: `/tez-literatur` slash komutu

**Files:**
- Create: `.claude/commands/tez-literatur.md`

**Interfaces:**
- Consumes: köprü §Narratif Derin-Lit Modu (Task 4), t1dm-tez-rehberi Faz 0/0.5/1.5, sci-audit Faz 3.6.

- [ ] **Step 1: Mevcut komut biçimini örnekle (frontmatter deseni)**

Run: `ls .claude/commands/ && head -8 .claude/commands/tez-oturum.md 2>/dev/null`
Expected: mevcut komutların YAML frontmatter deseni (ör. `description:`, `argument-hint:`) görünür; aynı deseni izle.

- [ ] **Step 2: Yaz — `.claude/commands/tez-literatur.md`**

```markdown
---
description: Marmara tez narratif derin-literatür incelemesi + sentez + tartışma (systematic review DEĞİL)
argument-hint: "<bölüm: giris|genel-bilgiler|tartisma> <konu>"
---

# /tez-literatur — Narratif Derin-Lit Modu

Kullanıcı argümanı: **$ARGUMENTS**

Bu komut sistematik derleme ÇALIŞTIRMAZ. Marmara tez kılavuzu çerçevesinde
narratif derin-literatür incelemesi + sentez + tartışma üretir.

## Yürütme

1. **Kapsam + tedbir kapısı** — t1dm-tez-rehberi Faz 0 (hipotez/SAP kısmı, veri
   çerçevesi, artefakt, kanonik-kilit, OSF) + Faz 0.5 tedbir denetimi. Kapı
   geçmezse dur.
2. **Doktrini yükle** — `.claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md`
   §"Narratif Derin-Lit Modu (tez; SR değil)" (kaskad + çıktı sözleşmesi + gate'ler).
3. **Bölüm sözleşmesini seç** — `$ARGUMENTS` ilk tokeni:
   - `giris` → literatür özet; alt başlık yok; boşluk+önem+amaç.
   - `genel-bilgiler` → genelden özele; yorum/sonuç çıkarımından kaçın; H1–H5 alt-başlık.
   - `tartisma` → karşılaştır-literatürle; hipotez destek beyanı; bulgu/istatistik tekrarı yok.
4. **D0–D6 kaskad** — evidentia connectors (pubmed-epmc, openalex, semantic-scholar,
   anamnesis, evidentia-kb, openathens, annas-reader, yok-akademik) + Minerva
   (`minerva_literature_search` D2; `minerva_*_fulltext`/`get_article` D4, annas ÖNCESİ).
   Ağır fan-out için `evidentia:evidence-synthesizer` alt-ajanı. **KVKK: yalnız
   literatür terimi.**
5. **Sentez** — anamnesis GraphRAG; retrieve-don't-dump.
6. **Taslak + künye** — Türkçe `[@key]` metin + `references/references.bib` künye
   adayları. Hiçbir künye **referans kapısı** (`/referans-kapisi`) `cite-ok`
   olmadan kaynakçaya girmez. Kaynakça biçimini `references/marmara-ama11.csl` render eder.
7. **Denetim** — sci-audit Faz 3.6 (axis A referans, B claim, C istatistik, G Türkçe imla).

## Devir (scope guard)
- Gerçek sistematik/kapsam derleme → `/evidentia:evidentia` (PRISMA P0→P7).
- MLR/promosyon → `promo-censor`; bireysel SGK/dava → `ius-salutis`.

## Bağlayıcı
UYDURMA REFERANS YASAĞI · PRIOR/HARKing tuzağı · tez kaynak olamaz (§4.2) ·
web ≤%5 yalnız .gov/.int/.eu · ana gate her zaman t1dm-tez-rehberi.
```

- [ ] **Step 3: Komut dosyasını doğrula**

Run: `test -f .claude/commands/tez-literatur.md && head -4 .claude/commands/tez-literatur.md`
Expected: dosya var; geçerli YAML frontmatter (`description:` + `argument-hint:`).

- [ ] **Step 4: Commit**

```bash
git add .claude/commands/tez-literatur.md
git commit -m "feat(command): /tez-literatur narratif derin-lit komutu"
```

---

### Task 7: Tutarlılık senkronu + final doğrulama

**Files:**
- Modify: `CONVENTIONS.md`
- Modify: `plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/assets/ai-reliability/CONVENTIONS.md` (ikiz — varsa aynı not)
- Modify: `docs/superpowers/specs/2026-07-11-evidentia-thesis-narrative-mode-design.md` (lint temizliği)

**Interfaces:**
- Consumes: tüm önceki task'lar.

- [ ] **Step 1: conventions rule 7'ye narratif-mod notu ekle (tutarlılık)**

`CONVENTIONS.md` rule 7 (evidence roster / Minerva notu) sonuna bir cümle:

```markdown
Repo varsayılan literatür modu **narratif derin-lit** (`/tez-literatur`; SR
değil); PRISMA P0→P7 yalnız açık sistematik/kapsam derleme talebinde
(`/evidentia:evidentia`). Doktrin: `literatur-kanit-evidentia.md` §Narratif
Derin-Lit Modu; yapılandırma `.claude/evidentia.local.md`.
```

- [ ] **Step 2: Audit ikizinde aynı notun gerekliliğini kontrol et**

Run: `grep -n 'Minerva\|rule 7\|evidence.*roster\|evidentia' plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/assets/ai-reliability/CONVENTIONS.md | head`
Expected: ikizde karşılık gelen rule 7 bloğu bulunursa aynı cümleyi ekle; yoksa atla (ve bunu not et).

- [ ] **Step 3: Spec markdown lint temizliği**

`docs/superpowers/specs/2026-07-11-evidentia-thesis-narrative-mode-design.md` — başlık/fence/liste çevresine boş satır ekle (MD022/MD031/MD032). 

Run: `npx --yes markdownlint-cli2 "docs/superpowers/specs/2026-07-11-evidentia-thesis-narrative-mode-design.md" 2>&1 | tail -5` (veya IDE tanılamasını temiz doğrula).
Expected: MD022/031/032 uyarıları düşer (0'a yakın).

- [ ] **Step 4: Final entegrasyon doğrulaması**

Run:
```bash
quarto render 2>&1 | tail -5
python3 -c "import yaml; yaml.safe_load(open('.claude/evidentia.local.md').read().split('---')[1]); print('local.md OK')"
test -f .claude/commands/tez-literatur.md && echo "command OK"
grep -q 'Narratif Derin-Lit Modu' .claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md && echo "bridge OK"
git check-ignore .claude/evidentia.local.md && echo "local.md ignored OK"
```
Expected: render hatasız; `local.md OK`, `command OK`, `bridge OK`, `local.md ignored OK`.

- [ ] **Step 5: Commit**

```bash
git add CONVENTIONS.md plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/assets/ai-reliability/CONVENTIONS.md docs/superpowers/specs/2026-07-11-evidentia-thesis-narrative-mode-design.md
git commit -m "docs(conventions): narratif-mod tutarlılık notu + spec lint"
```

---

## Self-Review

**1. Spec coverage:**
- spec §5① local.md → Task 3 ✓
- spec §5② bridge doktrini → Task 4 ✓
- spec §5③ SKILL Faz 1.5 → Task 5 ✓
- spec §5④ /tez-literatur → Task 6 ✓
- spec §5⑤ CSL + _quarto rewire → Task 1 + Task 2 ✓
- spec §8 test/kabul (CSL smoke, tam render, YAML parse, komut, KVKK) → Task 1 Step 5, Task 2 Step 3, Task 3 Step 3, Task 6, doktrin gate'leri ✓
- spec §7 kararlar (global "ve ark.", standart DOI, dergi kısaltma) → Global Constraints + Task 1 sözleşme ✓
- spec §6 tutarlılık (conventions) → Task 7 ✓

**2. Placeholder scan:** Kod adımları tam içerik taşıyor (bib, qmd, YAML, komut metni); CSL adımı kesin element/term sözleşmesi + deterministik render-testi (beklenen çıktı karakter düzeyinde sabit). "TBD/uygun şekilde" yok.

**3. Type/isim tutarlılığı:** `references/marmara-ama11.csl` (Task 1 üretir → Task 2 tüketir), `.claude/evidentia.local.md` (Task 3 üretir → Task 7 doğrular), `§Narratif Derin-Lit Modu` başlığı (Task 4 üretir → Task 5/6/7 atıfta bulunur), `/tez-literatur` (Task 6 üretir → Task 5 tablo + Task 7 conventions atıfta bulunur) — adlar tutarlı.

**Not (CSL riski):** CSL author-initial ("Fadini GP") ve global "ve ark." term override render-test döngüsüyle (Task 1 Step 5) ayarlanır; ilk XML taslağı beklenen çıktıya uyana kadar iterasyon beklenir — bu bir plan boşluğu değil, TDD döngüsüdür.
