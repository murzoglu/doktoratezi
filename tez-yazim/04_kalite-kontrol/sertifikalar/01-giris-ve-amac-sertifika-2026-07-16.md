# Bölüm Finalizasyon Sertifikası

Durum: `certified-final`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | 01 — GİRİŞ ve AMAÇ |
| Üretim dosyası | `chapters/01_giris_ve_amac.qmd` |
| Hazırlık briefi | `tez-yazim/03_bolum-hazirlik/01_giris-ve-amac.md` |
| Sertifikasyon tarihi | 2026-07-16 |
| Önceki sertifika | `01-giris-ve-amac-sertifika-2026-07-13.md` (`provisional-pass`) |
| Yeniden sertifikasyon nedeni | Kullanıcı isteğiyle güncel metinle tam Kapı 0–5 yeniden denetimi |
| Sertifikasyonu uygulayan | Ona (Claude Opus 4.8) |
| Uygulama onayı | **Kullanıcı açık onayı ("Uygun", 2026-07-16)** — bütünsel sertifikasyon kapsamında `certified-final`. |

## Değişiklik Envanteri (önceki sertifikadan bu yana)

Bölüm metni 2026-07-13 sertifikasından sonra **yalnız dil düzeyinde** düzenlendi
(commit `6b74998`, 2026-07-14 "docs(dil): sci-audit advisory uyumu"):

- Raportör-fiil monotonluğu azaltıldı; iki atıf parantetik → anlatısal biçime
  çevrildi (`@whittemore2012` → "Whittemore ve arkadaşlarının [-@...]";
  `@deLosReyes2015` → "De Los Reyes ve arkadaşlarının [-@...]").
- **Bilimsel bütünlük, atıf kümesi, hedef sayılar ve iddialar değişmedi.**

Bu oturumda 01'de yeni düzenleme yapılmadı; sertifikasyon güncel commit'li
metinle çalıştırıldı.

## Kapı 0: Kapsam ve Gizlilik — PASS

- [x] 20 benzersiz `@key` (fig/sec/tbl önekleri hariç); PII/satır-veri taşınmadı.

## Kapı 1: Derin Literatür ve Künye Evreni — PASS

- 20 atıf `references/references.bib` (333 künye) ile bire-bir eşleşti;
  **orphan-citation = 0**.
- Hedef sayılar metinde korunmuş: binde 0,75 · yüz binde 10,8
  (`@yesilkaya2016turkiyeIncidence`); ~108.300 / ~149.500 (`@ogle2022idfAtlas`);
  %22,4 genel / %31,5 anne (`@chen2023parentDepression`); pinquart2013 küçük-etki.

Kapı 1 kararı: **PASS**

## Kapı 2: Full-Text, Zotero ve Ledger — PASS (provisional)

- `bib_hygiene reconcile` (01): **HARD atıflı-tanımsız = 0**.
- Önceki sertifikadaki iki referans (`eckshtain2010parentDepression`,
  `butner2009discrepancy`) tam-tez render'da (2026-07-16) sorunsuz çözüldü →
  `cite-ok` (bkz. "`certified-final` Koşullarının Karşılanması").

Kapı 2 kararı: **PASS**

## Kapı 3: Bölüm Metni ve Resmi Kılavuz Uyumu — PASS

- [x] Resmi başlık: `# GİRİŞ ve AMAÇ` (alt başlık yok).
- [x] Ondalık **virgül** istisnasız; İngilizce-nokta `p` yok; `108.300`/`149.500`
  Türkçe binlik ayracı (ondalık değil).
- [x] **Tez-kaynak (yoktez) atfı yok** (GİRİŞ için Marmara §4.2 uyumu).
- [x] Nedensellik dili hedge'li; ulusal-boşluk "belirgin değildir/sınırlıdır".

Kapı 3 kararı: **PASS**

## Kapı 4: Türkçe İmla, Akış ve Mantık — PASS

`tr_corpus_audit all` (axis H): **HARD 0 · SOFT 0 · advisory 101**, `fail-on
blocker` exit 0. Dil commit'i (2026-07-14) SOFT bulguları temizledi; kalan
advisory'ler tek-dosya `H-ABBR-UNUSED` artefaktı ve stil önerileri (bloklayıcı
değil).

Kapı 4 kararı: **PASS**

## Kapı 5: AI-Reliability ve Teknik Doğrulama — PASS

- **Repo invaryant:** `doktoratezi-ai-audit` **144/144**;
  `t1dm-qual-ai-audit` **55/55**.
- **`bib_hygiene all`:** HARD atıflı-tanımsız = 0.
- **İzole render:** `pandoc --citeproc` (marmara-ama11.csl) 01 bölümünü başarıyla
  derledi (exit 0, 21 KB); **çözümsüz atıf uyarısı yok**.

Kapı 5 kararı: **PASS**

## `certified-final` Koşullarının Karşılanması

Önceki turda `certified-final`'i engelleyen iki koşul da bütünsel
sertifikasyon turunda (2026-07-16) karşılandı:

1. **Tam-tez render.** `quarto render thesis.qmd` HTML (exit 0) ve DOCX (exit 0)
   olarak tamamlandı; çözünmemiş çapraz-referans/atıf = 0. Önceki turda render'ı
   durduran gitignored artefakt sorunu, freeze:auto cache ile aşıldı.
   `eckshtain2010parentDepression` ve `butner2009discrepancy` künyeleri tam-tez
   render'da sorunsuz çözüldü.
2. **Açık kullanıcı onayı** — 2026-07-16'da ("Uygun") alındı.

## Nihai Sertifika Kararı

| Kapı | Karar |
|---|---|
| Kapı 0 | PASS |
| Kapı 1 | PASS |
| Kapı 2 | PASS (provisional) |
| Kapı 3 | PASS |
| Kapı 4 | PASS |
| Kapı 5 | PASS |
| **Nihai durum** | **`certified-final`** |

Teknik kapılar PASS; doğrulanmış blocker = 0. `certified-final` için tam-tez
render + iki referans `cite-ok` promosyonu + açık kullanıcı onayı gerekir.
