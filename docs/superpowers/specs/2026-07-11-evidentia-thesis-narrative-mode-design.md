# evidentia — Tez Narratif Derin-Literatür Modu (SR değil) — Tasarım

> **Tarih:** 2026-07-11 · **Durum:** onaylandı (kullanıcı: "uygun") · **Kapsam:** yapılandırma (yetenek kurulumu), bölüm metni yazımı değil.
> **Bağlayıcı üst kaynak:** `tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md` + `marmara-tez-formati-talimatnamesi.md`.

## 1. Amaç

evidentia plugin'ini bu repoda **tez yazımına** uygun yapılandırmak: Marmara tez kılavuzu çerçevesinde, ilgili bölümlerde (**Giriş ve Amaç**, **Genel Bilgiler**, **Tartışma ve Sonuç**) **en derinlikli bilimsel literatür incelemesi + sentez + tartışma** yapabilme yeteneğini kurmak. Amaç **sistematik derleme (systematic review) yazmak değildir**.

## 2. Premise'i değiştiren bulgular (recon `w9b3jc92z`)

1. **evidentia'da narratif/tez modu yoktur.** Tüm komutlar (`/evidentia`, `-synthesize`, `-appraise`…) PRISMA **P0→P7** hattına bağlıdır; sınıflandırıcı yalnız *sistematik vs kapsam* ayırır. `medical-research` `.claude/evidentia.local.md`'yi Adım 0.1'de okur ama **derleme-tipini değiştiren YAML anahtarı yoktur**.
2. **evidentia'nın tek sanctioned yerel yapılandırma yüzeyi** = `.claude/evidentia.local.md` (git-ignored). Plugin kurulumu `~/.claude/plugins/marketplaces/cureonics-marketplace/plugins/evidentia` (v2.3.0) — **upstream/marketplace, iç dosyaları düzenlenmez**; özelleştirme §1.5/§1.6 *extension* doktriniyle repo katmanına yapılır.
3. **Referans formatı APA/CSL değil.** Kanonik kural: metin-içi **yazar-yıl Türkçeleştirilmiş** (§1.8), kaynakça **Enstitü AMA-11 özel** (§4). Repo şu an `references/apa.csl` kullanıyor → **canlı tutarsızlık**; §11 override APA-7'yi açıkça reddeder.
4. **Hedef bölüm olgunluğu:** Giriş (01) gelişmiş ama ince; Genel Bilgiler (02) ana gövde, 7 alt-başlık boş (H1–H5 ile eşleşir); **Tartışma (05) en büyük boşluk** — prose atıflar `[@key]` değil, `references.bib`'de yok.
5. Off-the-shelf Enstitü AMA-11 CSL **repoda yok** (`find *.csl` → yalnız `apa.csl`) → **custom CSL üretilecek**.

## 3. Locked kararlar

- **Kapsam:** Tam profil + özel komut (kullanıcı seçimi).
- **CSL:** apa.csl → custom Enstitü AMA-11 CSL bu turda taşınır (kullanıcı seçimi).

## 4. Mimari ilke

evidentia'nın PRISMA komutları **olduğu gibi kalır** (gerçek SR için). Tez-narratif-derin-lit modu, evidentia extension doktrini uyarınca **repo katmanında** bir profil olarak eklenir. 3-katman sınırı korunur: **evidentia getirir → t1dm-tez-rehberi üretir → sci-audit denetler**. Ham katılımcı verisi hiçbir connector'a gitmez (KVKK).

## 5. Bileşenler

### ① `.claude/evidentia.local.md` (YENİ, git-ignored)

YAML frontmatter (fonksiyonel):

```yaml
enabled: true
known_connected: [pubmed-epmc, openalex, semantic-scholar, anamnesis,
  evidentia-kb, annas-reader, openathens, yok-akademik, minerva-evidence]
fulltext_tier: copyright_gated
completeness_gate: standard
auto_ingest_rag: true
default_modules: []   # psiko/pediatrik tez — ilaç-istihbaratı modülü yok
```

Gövde (serbest not, evidentia Adım 0.1 "okur"): **PROJE MODU banner'ı** — "bu repoda varsayılan çalışma modu = tez-narratif-derin-lit; PRISMA akış/RoB/GRADE yalnız kullanıcı açıkça 'sistematik derleme' derse. Narratif-mod doktrini: `.claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md` §Narratif Derin-Lit Modu." KVKK sınırı hatırlatması.

- **Neden git-ignored:** evidentia sözleşmesi (`.gitignore`'da mevcut Minerva bloğuna eklenir; hostname/iç bilgi taşımaz ama evidentia yerel-config konvansiyonu git-ignore'dur).

### ② `literatur-kanit-evidentia.md` → YENİ §"Narratif Derin-Lit Modu (tez; SR değil)" (TRACKED)

Asıl davranış doktrini. İçerik:

- **Kaskad alt-kümesi:** D0 → D1 → D2 → **D3\*** → D4 → D5 → D6. **D3\* (kısmi KALIR):** relevance rerank + AFF/TR transferability seçimi/curation — derin-lit sentezi için değerli, çalışır. **ATLA:** yalnız D3'ün SR title/abstract **tarama-kapısı** (dahil/hariç eleme) + PRISMA akış-diyagramı + RoB2/ROBINS-I/QUADAS-2 + GRADE/SoF. (Bu araçlar SR modunda kalır; narratif modda çalışmaz.) *[güncelleme 2026-07-11: D3 relevance-curation korundu, final review M2.]*
- **Marmara çıktı sözleşmesi:** Türkçe, edilgen 3. tekil; metin-içi **yazar-yıl `[@key]`** (2 yazar "ve"; 3+ "…ve ark."; çoklu `;`); ondalık virgül + baştan sıfır; kaynakça biçimi **CSL render eder** — evidentia **format-agnostik BibTeX künyesi + `[@key]`** üretir, elle biçimlenmiş kaynakça string üretmez.
- **Bölüm hedefleme:**
  - *Giriş ve Amaç:* literatür **özet**, alt başlık yok, boşluk+önem+amaç.
  - *Genel Bilgiler:* genelden özele, güncel literatür özeti, **yorum/sonuç çıkarımından kaçın**; 7 alt-başlık H1–H5'e eşlenir.
  - *Tartışma ve Sonuç:* **karşılaştır-literatürle** — benzer/farklı yönler + muhtemel neden; hipotez destek beyanı; bulgu/istatistik **tekrarı yok**; Giriş/Genel Bilgiler tekrarı yok; sonda Sonuç+öneriler. Karma-yöntem etiketi (uyum/tamamlayıcılık/ayrışma/genişleme).
- **Sentez motoru:** `/evidentia:evidentia-synthesize` + `evidence-synthesizer` alt-ajanı (ağır fan-out) + anamnesis GraphRAG. Minerva `minerva_literature_search` (D2), `minerva_*_fulltext`/`get_article` (D4, annas ÖNCESİ).
- **Bağlayıcı gate'ler (tekrar):** UYDURMA REFERANS YASAĞI (her künye gerçek DOI/PMID/YÖK-ID veya "VERİ BULUNAMADI"); PRIOR/HARKing tuzağı (veri sonrası literatür yalnız Tartışma yorumu veya `[KEŞİFSEL]`); **KVKK — connector'a yalnız literatür terimi**; tez kaynak olamaz (§4.2); web ≤%5 yalnız .gov/.int/.eu.

### ③ `t1dm-tez-rehberi/SKILL.md` Faz 1.5 (TRACKED, düzenleme)

- Narratif mod bu repoda Giriş/Genel Bilgiler/Tartışma literatür işinde **varsayılan**; PRISMA yalnız açık "sistematik/kapsam derleme" talebinde.
- Giriş-noktaları tablosuna satır: `/tez-literatur <bölüm> <konu>` → "Marmara narratif derin-lit (SR değil)".

### ④ `.claude/commands/tez-literatur.md` (YENİ, TRACKED)

Slash komut. Kullanım: `/tez-literatur <bölüm> <konu>`; `<bölüm>` ∈ {giris, genel-bilgiler, tartisma}.

- Adım: (a) t1dm-tez-rehberi Faz 0/0.5 kapsam+tedbir kapısı; (b) köprü §Narratif Derin-Lit Modu doktrinini yükle; (c) bölüme göre çıktı sözleşmesini seç; (d) D0-D6 kaskad (evidentia connectors + Minerva); (e) anamnesis sentez; (f) Türkçe `[@key]` taslak + `references.bib` künye adayları (referans-kapısı `cite-ok` şartı); (g) sci-audit Faz 3.6'ya devret.
- Devir (scope guard): SR istenirse `/evidentia:evidentia`; MLR/promo dışı.

### ⑤ `references/marmara-ama11.csl` (YENİ custom) + `_quarto.yml` rewire (TRACKED)

**Metin-içi (citation) — §1.8:**

- author-date; `<layout prefix="(" suffix=")" delimiter="; ">`.
- İki yazar: "Ad ve Soyad" → `and="text"` (locale term "ve").
- 3+ yazar: `et-al-min="3" et-al-use-first="1"` → "İlk ve ark.".
- Yazar-yıl arası virgül; çoklu kaynak `;`; yıl her zaman; `Ad ve ark. (2024)` (cümle içi) vs `(Ad ve ark., 2024)` (cümle sonu — narrative vs parenthetical CSL ayrımı).
- Aynı yazar-yıl: `disambiguate-add-year-suffix="true"` → 2017a/b.
- İsim: `form="short"` (soyad + baş harf), `initialize-with=". "`.

**Kaynakça (bibliography) — §4:**

- `<bibliography>` sort: yazar (family) → issued year.
- Künye düzeni: `Yazar AA, Soyad BB. Başlık cümle-düzeni. Derg Kıs. Yıl;Cilt(Sayı):Sayfa. https://doi.org/<DOI>`.
- İtalik/kalın **yok** (font-style/weight kullanma).
- `et-al-min="7" et-al-use-first="6"` (>6 → ilk 6 + et-al term).
- Dergi: `container-title` `form="short"` → kısaltma **bib entry'de `shortjournal`/abbrev alanı varsa** render olur (bkz. §7 bağımlılık).
- Kitap bölümü, proceedings, web (.gov/.int/.eu), rapor, veri tabanı tipleri §4.3 Tablo 1 örneklerine göre.

**Çok-dilli et-al — KARAR (onaylı 2026-07-11):** global **"ve ark."** — `default-locale="tr"`, et-al term "ve ark." her kaynakta. (§4.1 hem "et al." hem "ve ark." kabul eder; Türkçe tez varsayılanı, `language`-bağlı ikili layout kırılganlığından kaçınılır.)

**Rewire:** `apa.csl` silinmez (arşiv); `_quarto.yml` `csl:` → `references/marmara-ama11.csl`.

## 6. Veri akışı (örnek)

`/tez-literatur tartisma "H4 maternal depresyon → ebeveynlik"`
→ Faz 0/0.5 kapsam+tedbir → Faz 1.5 narratif mod → köprü D0-D6 (yalnız literatür terimi) → anamnesis sentez → Türkçe `[@key]` taslak + `references.bib` adayları → referans-kapısı `cite-ok` → sci-audit A/B/C/G → `chapters/05_tartisma_ve_sonuc.qmd`.

## 7. Bağımlılıklar / açık noktalar

- **Dergi kısaltması:** CSL `form="short"` ister; `references.bib` künyelerinin abbrev alanı taşıması **referans-kapısı**nın sorumluluğu. CSL kısaltmayı üretemez, yalnız var olanı seçer. (İmplementasyon notu, blocker değil.)
- **DOI biçimi belirsizliği:** §4.3 örneği literal `https://doi.org/doi:10.1111/…` (fazladan "doi:") gösteriyor — büyük olasılıkla kılavuz dizgi hatası. CSL standart `https://doi.org/<DOI>` üretir; kullanıcıya son onayda teyit ettirilir.
- **Çok-dilli et-al** kırılırsa global "ve ark." fallback'ine düşülür.

## 8. Test / kabul kriterleri

- [ ] **CSL smoke-test:** `references.bib`'ten 4 künye (makale ≤6, makale >6, Türkçe >6, kitap bölümü) mini `.qmd` ile render → §4.3 Tablo 1 ile eşleşir (italik/kalın yok, alfabetik, AMA düzen).
- [ ] **Metin-içi:** yazar-yıl "ve"/"ve ark.", çoklu `;`, year-suffix doğru.
- [ ] **Tam render:** `quarto render` bozulmaz (126 künye, tüm bölümler); `_quarto.yml` yeni CSL'e bağlı.
- [ ] `.claude/evidentia.local.md` frontmatter geçerli; evidentia Adım 0.1 okuyabilir.
- [ ] `/tez-literatur` komutu tetiklenir; KVKK sınırı (yalnız literatür terimi) gözlenir.
- [ ] Köprü §Narratif Derin-Lit Modu + SKILL Faz 1.5 + conventions tutarlı (aspirasyonel connector listesi çelişkisi büyütülmez).

## 9. Kapsam dışı / kısıtlar

- Bu tur **yeteneği kurar**, bölüm metnini yazmaz. Kurulumdan sonra `/tez-literatur <bölüm>` ile çalıştırılır (opsiyonel demo koşumu).
- **Dokunulmaz:** plugin iç dosyaları, `.claude/settings.json permissions.deny`, `.env` (Read/Bash deny), ham veri katmanları.
- **Commit:** repo kuralı (#14) — yalnız kullanıcı açıkça isteyince; `git add .` yok.
- **CSL rewire tüm tezin render'ını etkiler** (geri alınabilir, git); smoke + tam render ile korunur.

## 10. Reddedilen alternatifler

- **Plugin komutu forklama** (medical-research repo-lokal kopya + PRISMA soyma): duplikasyon + upstream drift → red.
- **Sadece local.md + hep -synthesize**: narratif sözleşme/komut yok; kullanıcı eledi → red.
- **CSL: hazır vancouver/AMA yamalama**: standart AMA sayısal/atıf-sırası; yazar-yıl+alfabetik'e çevirmek custom yazmaktan kırılgan → red.
