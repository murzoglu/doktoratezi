# Bölüm Finalizasyon Sertifikası

Durum: `certified-final`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | `01-giris-ve-amac` |
| Bölüm başlığı | `GİRİŞ ve AMAÇ` |
| Üretim dosyası | `chapters/01_giris.qmd` |
| Hazırlık briefi | `tez-yazim/03_bolum-hazirlik/01_giris-ve-amac.md` |
| Sertifikasyon tarihi | 2026-07-05 |
| Sertifikasyonu uygulayan | Claude Code (Fable 5) |
| Uygulama onayı | `verildi` |
| Onay veren | Mahir Kurt; kullanıcı mesajları: "Tam sertifikasyon koş" + zotero-gap düzeltmesi için "İzin verdim" |
| Önceki sertifika | `01-giris-ve-amac-sertifika-2026-07-01.md` (bu sürüm onu supersede eder) |

## Bu Sürümün Kapsamı

2026-07-05 oturumunda bölüm iki eksende revize edildi ve tam yeniden
sertifikasyona alındı:

1. **Marmara kılavuzu §3.8.2 uyumu (tez kaynak olamaz).** GİRİŞ metninde 2026-07-02
   zenginleştirme koşusunda eklenmiş olup önceki sertifikada değerlendirilmemiş
   üç YÖK tez atfı, tam metni doğrulanmış hakemli dergi karşılıklarıyla
   değiştirildi:
   - `tuncay2025yoktez` → `ozguven2025parentalCollab` + `ceran2024selfmgmt`
   - `demirkiran2025yoktez` → `adal2015psychosocial`
   - `ayranci2025yoktez` → `yuksel2024qol`

   "Ulusal tez literatüründe…" cümlesi "Ulusal hakemli literatürde…" olarak
   yeniden yazıldı; ulusal boşluk iddiası "belirgin değildir" kalıbında korundu.

2. **Kardeş ekseni tam metin konsolidasyonu.** `chanShorey2022`
   (`full-text-exception`) GİRİŞ metninden çıkarıldı; tam metin kapısı
   2026-07-05'te yeniden denetlendi (Anna SciDB yanlış-eşleşme reddi;
   PubMed-EPMC/Europe PMC/Unpaywall `no-oa`). Kardeş bilgi/duygusal
   destek/görünürlük gereksinimi iddiası tam metni açık `ludvigsen2026siblingT1D`
   (PMC OA, T1DM-özgü nitel) + `lummerAikey2021` (kardeş uyumu bütünleştirici
   derleme) üzerine konsolide edildi.

## Kapı 0: Kapsam ve Gizlilik

- [x] Bölüm dosyası ve hazırlık briefi okundu.
- [x] `docs/tez-kilavuz` dosya varlığı ve `format-kontrati.md` okundu.
- [x] Kritik kaynak manifesti okundu (`06_kritik-kaynaklar/README.md`).
- [x] Ham veri, ham transcript, satır düzeyi veri, `.env`, token veya credential
      rapora taşınmadı. GİRİŞ yalnız dış literatür iddiaları içerir; katılımcı
      satır verisi kullanılmaz.

Kapı 0 kararı: `PASS`

## Kapı 1: Derin Literatür ve Künye Evreni

Bölümdeki 18 dış atfın tamamı `referans-denetim-ledgeri.md` içinde doğrulanmış
künye satırına (DOI/PMID/PMCID/OpenAlex/YÖK ID) bağlıdır ve tümü `cite-ok`
durumundadır. Otomatik denetim (bölüm atıfları ↔ ledger durum sütunu):
`cite-ok: 18 | diğer: 0 | orphan claim: yok`.

Yeni dergi karşılıkları (`ozguven2025parentalCollab`, `ceran2024selfmgmt`,
`adal2015psychosocial`, `yuksel2024qol`) GENEL BİLGİLER sertifikasyonunda zaten
Evidentia/PubMed-EPMC/PMC kapsam-doğrulaması ile eklenmişti. 2026-07-05 tam metin
yeniden taraması (`chanShorey2022`, `ogle2022idfAtlas`) ve PubMed free-full-text
kardeş derleme taraması ek OA kaynağı bulunmadığını teyit etti.

Kapı 1 kararı: `PASS`

## Kapı 2: Full-Text, Zotero ve Bağlam

Zotero Web API erişimi doğrulandı (`status`: key_loaded, user library
read/write/notes/files). 18 referansın tamamında künye-ID + Zotero item key +
`references/references.bib` girdisi mutabık.

`T1DM Thesis` collection (`9ZFDHMZA`) export'u ile bölüm atıfları karşılaştırıldı
ve bir `zotero-gap` bulundu ve kapatıldı:

| Bloklayıcı | Durum | Çözüm |
|---|---|---|
| `zotero-gap` (`furmanBuhrmester1985srq`) | Kapandı | Ledger'daki item `Z5RKE9QG` Zotero'da `404 Item not found` idi (bayat kayıt). Kaynak DOI `10.2307/1129733` (Crossref + PMID `3987418` doğrulamalı) ile T1DM Thesis collection'a yeniden import edildi; yeni item `H8VZE5PT`, URL attachment `3U2ISEFQ`, note `36APDHQ2`, BibTeX key `furmanBuhrmester1985srq` pinlendi. Ledger güncellendi. |

Kapatma sonrası export 57 girdi; bölümde olup export'ta olmayan atıf: yok
(18/18 mutabık, orphan citation yok).

Kapı 2 kararı: `PASS`

## Kapı 3: Bölüm Metni ve Resmi Kılavuz Uyumu

- [x] Resmi başlık doğru: `# GİRİŞ ve AMAÇ`.
- [x] Alt başlık yok (kılavuz GİRİŞ için alt başlık önermez).
- [x] Bölüm işlevi doğru: problem → boşluk → gerekçe → amaç → H1-H5 alt amaçlar.
- [x] Tablo/şekil/cross-reference yok; istatistik/`p` değeri yok (bölüm işlevi
      korunmuş).
- [x] Ondalık virgül kuralı: `binde 0,75`, `yüz binde 10,8`, `%22,4`, `%31,5`.
      `108.300` ve `149.500` binlik ayırıcılı sayım değerleridir ve
      `ogle2022idfAtlas` atfıyla aynı cümlededir.
- [x] Orphan claim yok: tüm sayısal iddialar aynı paragrafta atıflı.
- [x] Citation key'lerin tamamı `references/references.bib` içinde çözülüyor
      (18/18).

Kapı 3 kararı: `PASS`

## Kapı 4: Türkçe İmla, Akış ve Mantık

Zorunlu repo-local ön-denetim:

```text
.venv-tr-sciaudit/bin/python scripts/util/tr_sciaudit.py chapters/01_giris.qmd \
  --strictness certification --format md \
  --out tez-yazim/04_kalite-kontrol/raporlar/01-giris-tr-sciaudit.md \
  --fail-on error
EXIT: 0 | Errors: 0 | Warnings: 12 | Info: 1
```

Uyarılar bloklayıcı değildir ve önceki sertifikalı baseline ile aynı üslup
sinyalleridir: uzun cümle/paragraf (tez giriş registeri için beklenen
"very-hard" okunabilirlik), binlik ayırıcı sayılarda `decimal-dot` yanlış
pozitifi (denetimin kendi "identifier istisnası" kapsamında; ondalık değil,
sayımdır) ve `IDF` kısaltma incelemesi (ilk kullanımda açık). Gerekçeli kabul
edildi.

Kapı 4 kararı: `PASS`

## Kapı 5: AI-Reliability ve Teknik Doğrulama

| Komut | Sonuç |
|---|---|
| `./dmnitel ai-context` | PASS; tez yazım merkezi ve güvenli bağlam kapıları doğrulandı. |
| Nitel `t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py` | PASS; `55/55 passed`; roster OpenAI/GitHub token redaction PASS. |
| Nicel `doktoratezi-ai-audit/scripts/test_repo_ai_reliability.py` | PASS; `142/142 passed`. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` (nitel repo) | PASS; `Ran 90 tests ... OK`. |
| `python3 -m unittest discover -s tests` (nicel repo Python) | PASS; `Ran 18 tests ... OK`. |
| `python3 scripts/util/zotero_env_bridge.py status --json` | PASS; Web API key loaded, read/write/notes/files yetkileri var. |
| `git diff --check` | PASS; çıktı yok. |
| `quarto check` | PASS; Quarto 1.6.43, Pandoc 3.4.0, R 4.x, TinyTeX OK. |
| Proje-bağlamlı bölüm render (`{{< include chapters/01_giris.qmd >}}`) | PASS; exit 0, HTML üretildi, çözülmemiş `?@` atıf yok. |
| Pandoc citeproc atıf çözümü | PASS; 18/18 atıf `references.bib`'e çözüldü; yeni dergi karşılıkları kaynakçada göründü. |
| Sır/credential taraması (diff) | PASS; anahtar/token/parola sızıntısı yok. |

AI-use log: dış MCP kullanımı (annas-reader, pubmed-epmc, Zotero Web API import)
`99_ai_use_log/ai_use_log.csv` içine kaydedildi.

Kapı 5 kararı: `PASS`

## Bloklayıcılar ve Çözüm

| Bloklayıcı | Durum | Çözüm |
|---|---|---|
| `format-gap` (§3.8.2 tez atfı) | Kapandı | Üç YÖK tez atfı tam metni açık hakemli dergi karşılıklarıyla değiştirildi. |
| `full-text-gap` (`chanShorey2022`) | Kapandı | Kaynak metinden çıkarıldı; iddia tam metni açık iki kaynağa konsolide edildi. |
| `zotero-gap` (`furmanBuhrmester1985srq`) | Kapandı | Bayat 404 item DOI ile T1DM Thesis collection'a yeniden import edildi; ledger güncellendi. |
| `approval-gap` | Kapandı | Kullanıcı 2026-07-05 tarihli açık onay verdi. |

## Nihai Sertifika Kararı

| Alan | Değer |
|---|---|
| Kapı 0 | `PASS` |
| Kapı 1 | `PASS` |
| Kapı 2 | `PASS` |
| Kapı 3 | `PASS` |
| Kapı 4 | `PASS` |
| Kapı 5 | `PASS` |
| Nihai durum | `certified-final` |

Final notu:

```text
chapters/01_giris.qmd; §3.8.2 tez-yasağı uyumu, kardeş ekseni tam metin
konsolidasyonu, Zotero collection mutabakatı (zotero-gap kapatıldı), Türkçe
akış, çift AI-reliability (55/55 + 142/142), Quarto üretilebilirliği ve atıf
çözümü açısından kapatılmıştır. 18/18 dış atıf cite-ok; metinde retired veya
full-text-exception kaynak kalmadı. Açık kullanıcı uygulama onayı alındığı için
bölüm certified-final statüsüne yükseltilmiştir.
```
