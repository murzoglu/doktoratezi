# Spec — CSR Didaktik Açıklama Katmanı (3-Parçalı Yöntem Gerekçesi)

Tarih: 2026-07-13 · Durum: onaylandı (kullanıcı: "uygun") · Kapsam: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd`

## Problem Tanımı

`docs/CLINICAL-STUDY-REPORT-FINAL.qmd` (7252 satır, 23 ana bölüm, 60 R chunk)
her teknik/istatistik detay için okuyucuya **neyin, neden, nasıl** yapıldığını
tutarlı biçimde vermiyor. Kullanıcı talebi: her teknik ve istatistik detay için
üç şeyi açık kılmak —

1. Elimizdeki veri + literatür bağlamında **hangi bilimsel soruya** cevap arandığı,
2. Bu cevap için **hangi istatistik tekniğinin seçildiği**, tekniğin özellikleri
   ve **nasıl tatbik edildiği**,
3. Elde edilen sonuçların **nasıl değerlendirildiği/tartıldığı**.

Amaç: CSR'ın anlaşılırlığını en üst düzeye taşımak.

## Mevcut Durum Bulgusu (tasarımı şekillendirir)

CSR §11 zaten **kısmen didaktik** (kaynak: `docs/CLINICAL-STUDY-REPORT-FINAL.qmd`
§11 okuması):

- **`> Yöntem kutusu`** blockquote'ları H1/H2/H3/H5 alt bölümlerinde **var**
  (H4'te **yok**); yalnız 3-parçanın **2. parçasını** (yöntem) karşılıyor,
  blockquote formatında (seçilen etiketli-mini-blok değil).
- **`… Karar Kutusu`** blokları **3. parçayı** (değerlendirme/verdict) zaten
  güçlü ve **mevcut atıflarla** yapıyor (künyeler `docs/CLINICAL-STUDY-REPORT-FINAL.qmd`
  §11'den birebir: Pinquart `:2529`/`:2766`, De Los Reyes & Kazdin `:2529`/`:2703`,
  De Los Reyes ve ark. `:2802`/`:2855`, Funder & Ozer + Schäfer & Schwarz `:2529`,
  Lakens `:2605`, Lovejoy ve ark. `:2766`, Butner ve ark. `:2824`); çoğu zaten
  `references/references.bib` içinde.
- **1. parça** (bilimsel soru) çoğunlukla **örtük**, açıkça yazılmamış.

Sonuç: iş **sıfırdan katman ekleme değil**, mevcut didaktik içeriği tutarlı bir
şablona **sistematikleştirme + eksik parçaları tamamlama**. Bu, yeni-atıf yükünü
de düşürür (değerlendirme atıflarının çoğu mevcut).

## Kararlar (kullanıcı onaylı)

| Karar | Seçim |
|---|---|
| Format/yerleşim | **Etiketli mini-blok** (kalın etiketli düz markdown, hep açık; callout/blockquote değil) |
| Atıf politikası | **Gerektiğinde yeni atıf** — her yeni künye tam `/referans-kapisi`'nden geçer |
| Granülarite | **Teknik/analiz bloğu başına** (~teknik = 1 didaktik birim) |
| Yürütme | **Önce pilot §11**, onay sonrası kalan 22 bölüme yay |

## Mini-Blok Şablonu

Her tekniğin başına, tekniğin sonuç/şekil bloğundan **önce**:

```markdown
**Bilimsel soru.** [Elimizdeki veri (482 satır = 241 aile × 2; aile-içi
bağımsızlık yok — kaynak CLAUDE.md/veri haritası) + literatür bağlamında hangi
soruya cevap aranıyor; neden bu soru. 1-2 cümle.]

**Yöntem & tatbik.** [Seçilen teknik, ayırt edici özelliği, bu veriye nasıl
tatbik edildi — değişkenler, tahminci, kritik kararlar. Mevcut "Yöntem kutusu"
içeriği buraya taşınır ve zenginleşir.]

**Nasıl değerlendirilir.** [Sonucun hangi A-PRIORI ölçütle okunacağı: etki
büyüklüğü + %95 GA, benchmark, eşik, çoklu-karşılaştırma stratejisi, keşifsel/
doğrulayıcı etiketi, nedensellik sınırı. VERDICT DEĞİL — ölçüt.]
```

## Yinelenme Önleme (kritik mimari karar)

- **Mini-blok** tekniğin **başında**: parça 1 (soru) + parça 2 (yöntem/tatbik)
  tam; parça 3 = **a-priori değerlendirme ÖLÇÜTÜ** ("bu sonuç nasıl okunacak").
- **`Karar Kutusu`** bölümün **sonunda**: değerlendirmenin **SONUCU/verdict'i**.
  **Değiştirilmez, korunur.**
- Böylece "nasıl yargılanır" (baş) ile "yargı" (son) ayrışır → tekrar yok.
- Mevcut `> Yöntem kutusu` blockquote'ları mini-blok "Yöntem & tatbik" parçasına
  dönüştürülür.

## Pilot §11 Teknik Envanteri (~19 birim)

- **H1 (§11.1):** çok düzeyli model + ICC (birincil) · Bayesçi BF katmanı ·
  IRT GRM · üçlü etkileşim (yaş × cinsiyet × rol)
- **H2 (§11.2):** APIM (birincil) · Olsen-Kenny ayırt-edilebilir düad CFA · TOST
  (uygulanmadı — bu karar da açıklanır)
- **H3 (§11.3):** IPTW ANCOVA (birincil) · antidepresan-katmanlı duyarlılık ·
  Bayesçi ROPE/BF · TOST eşdeğerlik
- **H4 (§11.4):** WLSMV ordinal SEM (birincil; **kutu eksik → eklenir**) ·
  çoklu-grup ölçüm değişmezliği
- **H5 (§11.5):** 5 strateji ayrı ayrı — ICC+Bland-Altman · RSA (Edwards-Parry) ·
  Ortak Yazgı Modeli (CFM) · Olsen-Kenny latent CFA · Kenny k-katsayısı

Kalibrasyon: birincil hipotez teknikleri **tam** mini-blok; tekrarlayan/destek
teknikler (Bayesçi katman, invariance, her H5 stratejisi) **kompakt** mini-blok
(soru + teknik özelliği + ölçüt, kısa).

## Atıf Akışı

1. Önce mevcut `references/references.bib` + CSR §21 çekirdek yeniden kullanılır.
2. Yalnız **parça 1 (bilimsel soru / literatür bağlamı)** gerçekten yeni bir
   kaynak gerektirirse: künye önce işaretlenir → kullanıcı onayı → tam
   `/referans-kapisi` (bağlam → DOI/PMID → tam metin → Zotero item≠BibTeX →
   claim/pasaj → ledger + iki-kol AI-reliability) → ancak sonra metne girer.
3. **Uydurma-referans yasağı** mutlaktır; doğrulanamayan künye eklenmez
   ("VERİ BULUNAMADI"). Literatür iddiası hafızadan uydurulmaz.

## Değişmez Guardrail'ler

- **Format sözleşmesi:** Türkçe edilgen 3. tekil; ondalık virgül (`p<0,001`);
  başlık kaskadı ≤4 düzey — **mini-blok başlık DEĞİL**, `**bold**` etiket, kaskadı
  bozmaz (galileo_heading_cascade temiz kalır).
- **Veri sınırı (KVKK, ihlal edilemez):** yalnız aggregate; satır/PII/aile-düzeyi
  detay yok. **R chunk içindeki sayısal literaller DEĞİŞTİRİLMEZ** — yalnız
  çevresine düzyazı açıklama eklenir.
- **Bulgular ↔ yorum ayrımı:** mini-blok yöntem+ölçüt açıklar, **bulgu sayısını
  tekrar etmez**; keşifsel analizlerde `[KEŞİFSEL]` etiketi korunur; kesitsel
  tasarım → **nedensel dil yok** (ilişkisel/betimsel).
- **Kanonik sayılar:** hiçbir mevcut istatistik değeri/verdict değiştirilmez;
  yalnız açıklama katmanı eklenir.

## Denetim Kapıları (pilot sonrası)

- `sci-audit` yedi eksen (A referans, B claim, C istatistik, D halüsinasyon,
  E kılavuz, F AI-şeffaflık, G Türkçe imla) — `docs/CLINICAL-STUDY-REPORT-FINAL.qmd`
  üzerinde `--lang tr --strictness certification`.
- Galileo advisory/soft-block (groundedness/faithfulness, tutarlılık, referans-nesri).
- Yeni atıf varsa `/referans-kapisi` her künye için kapanmış olmalı.
- `quarto render` exit 0 (R chunk literalleri korunduğundan kırılmamalı).

## Yürütme Mekaniği

1. **Pilot:** §11 bu şablonla tam işlenir (in-place edit `docs/CLINICAL-STUDY-REPORT-FINAL.qmd`).
2. Kullanıcıya gösterilir; format/ton/derinlik onayı alınır.
3. **Yayılım:** kalan 22 bölüme blok-blok uygulanır. Bloklar
   `docs/superpowers/specs/2026-08-01-tez-kontrol-checklisti-tasarimi.md`
   8-mantıksal-blok haritasıyla hizalıdır; her blok bağımsız işlenebildiğinden
   workflow fan-out uygundur (onay sonrası ayrı kararla).

## Başarı Kriterleri

- §11'deki her teknik (~19) tam/kompakt mini-blok taşıyor; H4 kutusu eklendi.
- Üç parça her mini-blokta açık; parça 3 (ölçüt) ↔ Karar Kutusu (verdict) tekrarı yok.
- Hiçbir istatistik literali/verdict değişmemiş; `quarto render` exit 0.
- Yeni atıf yoksa referans kapısı tetiklenmemiş; varsa her biri cite-ok.
- sci-audit G (Türkçe imla/ondalık virgül) blocker'sız; A/B kaynaksız-claim yok.

## Kapsam Dışı

- §11 dışındaki bölümler (bu spec pilotu tanımlar; yayılım ayrı onay + plan).
- Yeni istatistiksel analiz / yeniden hesaplama (yalnız açıklama katmanı).
- CSR yapısının/başlık sırasının değişmesi.
- Ham veri veya satır-düzeyi içerik girişi.
