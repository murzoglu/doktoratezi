# DOCX render — Marmara format katmanı

Bu klasör, `quarto render thesis.qmd --to docx` çıktısını Marmara Tez Formatı
Talimatnamesi'ne (`tez-yazim/00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md`)
uydurmak için kullanılan üç artefaktı içerir. `_quarto.yml` bunlara bağlıdır.

| Dosya | Rol |
|---|---|
| `marmara-reference.docx` | Pandoc reference-doc. §1.1 kenar boşlukları (A4, sol/sağ 2,5 cm, üst/alt 2 cm), §1.2 ana metin (TNR 12 pt, 1,5 aralık, iki yana yaslı) ve **siyah köprü rengi**, §1.3 başlıklar (ana bold 14 pt, alt bold 12 pt) ve **dizin başlıkları** (`TOCHeading` → Heading1), §1.6/§1.7 şekil/tablo başlığı (TNR 12 pt, tek aralık), dizin girdileri (`TOC1`–`TOC9`, TNR 11 pt, nokta öncülü sağ sekme). |
| `build_marmara_reference.py` | `marmara-reference.docx`'i üreten/yenileyen script. Pandoc default reference-doc'unu alır, Marmara değerlerini enjekte eder. |
| `marmara-caption-bold.lua` | §1.7 "etiket kalın, devamı normal" kuralını uygular: caption etiketini (`Tablo 1.` / `Şekil 2a.`) bold sarar. `quarto` sentinel filtresinden **sonra** çalışır. |

## Yeniden üretim

```bash
# reference-doc'u yeniden üret (Pandoc/Quarto sürümü değişince veya sıfırdan)
python3 tez-yazim/02_sablonlar/docx/build_marmara_reference.py

# tezi DOCX render et
quarto render thesis.qmd --to docx
```

## `_quarto.yml` bağlantısı

```yaml
crossref:
  title-delim: "."          # §1.6/§1.7: "Tablo 1." / "Şekil 1." (nokta ayırıcı)
filters:
  - quarto                  # crossref caption'ı önce üretir
  - tez-yazim/02_sablonlar/docx/marmara-caption-bold.lua  # etiketi sonra bold'lar
format:
  docx:
    reference-doc: tez-yazim/02_sablonlar/docx/marmara-reference.docx
```

## Notlar

- Lua filtre tüm formatlarda (HTML/PDF/DOCX) çalışır; caption AST yapısı ortak
  olduğu için HTML'de de etiket bold olur — Marmara ile tutarlı, zararsız.
- `TEZ ŞABLONLARI-2026-2RV.docx` kapak/ön-bölüm yerleşim otoritesidir; metin
  biçimi (10 pt/1,15 aralık) Marmara ana-metin kuralıyla çeliştiğinden biçim
  reference-doc üzerinden §1.2'ye göre zorlanır.
- **Dizin katmanı (§1.2/§1.3).** Pandoc varsayılanı `TOCHeading` stilini
  `Heading1`'den türetir ama bold'u kapatır (`<w:b w:val="0"/>`), tema fontuna
  (`majorHAnsi`) ve maviye (`365F91`) çevirir; ayrıca `Hyperlink` mavidir
  (`4F81BD`). §1.3 içindekiler/şekiller/tablolar dizinlerini **ana başlık**
  sayar (kalın, 14 punto) ve §1.2 ana metni siyah ister. Bu nedenle build
  script'i override'ı kaldırır (stil `Heading1`'i devralır, `outlineLvl 9`
  korunur ki dizin başlıkları kendi dizinlerine düşmesin) ve köprüleri
  siyaha çeker — PDF hattı zaten
  `linkcolor/citecolor/urlcolor/toccolor: black` ile tamamen siyahtır.
- **`TOC1`–`TOC9`.** Pandoc default reference-doc'unda tanımlı değildir; alan
  (`TOC \o "1-3" \h \z \u`) Word'de güncellenince yerleşik tema varsayılanları
  üretilirdi. Resmi Marmara şablonunun `TOC1` stili (TNR, bold, 11 pt, 1,5
  aralık) esas alınarak açıkça tanımlanır; sağ sekme metin genişliğine
  (9072 twip = 11906 − 2×1417) nokta öncüyle sabitlenir.
