# Bölüm Finalizasyon Sertifikası

Durum: `certified-final`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu | 02 — GENEL BİLGİLER |
| Üretim dosyası | `chapters/02_genel_bilgiler.qmd` |
| Hazırlık briefi | `tez-yazim/03_bolum-hazirlik/02_genel-bilgiler.md` |
| Sertifikasyon tarihi | 2026-07-16 |
| Önceki sertifika | `02-genel-bilgiler-sertifika-2026-07-07.md` (`certified-final`) |
| Yeniden sertifikasyon nedeni | Bölüm bu oturumda genişletildi (+60/−11 satır): 4 yeni tablo, ebeveynlik kuramları ve EMBU/Beck/KİA gelişim tarihi anlatıları, 10 klasik referans. |
| Sertifikasyonu uygulayan | Ona (Claude Opus 4.8) — Kapı 0–5 yeniden denetimi |
| Uygulama onayı | **Kullanıcı açık onayı ("Uygun", 2026-07-16)** — bütünsel sertifikasyon kapsamında `certified-final`. |

## Bu Oturumdaki Değişiklik Envanteri

`chapters/02_genel_bilgiler.qmd` (+60/−11 satır):

1. **Ebeveynlik kuramları:** Tarihsel anlatı (Schaefer 1959 circumplex →
   CRPBI 1965 → Baumrind 1971 → Maccoby-Martin 1983 → Darling-Steinberg 1993 →
   Rohner PARTheory) + `@tbl-ebeveynlik-kuramlari` (6 satır).
2. **EMBU çerçevesi:** Gelişim tarihi (Perris 1980 → Arrindell 1983 →
   s-EMBU 1999/2005 → Castro çocuk formu 1993 → Dirik Türkçe 2015 → Sümer 2010) +
   `@tbl-embu-gelisim`.
3. **Beck Depresyon Envanteri:** 1961 → 1988 gözden geçirme → 1996 BDI-II gelişim
   tarihi.
4. **KİA/SRQ:** Furman-Buhrmester 1985 yapısal→ilişki-niteliği geçişi.
5. **Özet tablolar:** `@tbl-olcum-ozet` (5 araç) + `@tbl-t1dm-evreleme`
   (ADA/ISPAD 3-evre).
6. **10 klasik referans** `references.bib`'e eklendi (aşağıda Kapı 2).

Sınır: Ham veri / PII / satır-düzeyi veri sertifikaya taşınmadı.

## Kapı 0: Kapsam ve Gizlilik — PASS

- [x] Değişiklik envanteri git diff'ten çıkarıldı; 73 benzersiz `@key`; PII yok.

## Kapı 1: Derin Literatür ve Künye Evreni — PASS

- 73 atıf `references/references.bib` (333 künye) ile bire-bir eşleşti;
  **orphan-citation = 0**.
- 4 yeni tablonun tümü hem `{#tbl-…}` tanımlı hem gövdede `@tbl-…` atıflı.

Kapı 1 kararı: **PASS**

## Kapı 2: Full-Text, DOI ve Ledger Mutabakatı — PASS (1 DOI hatası düzeltildi)

Bu oturumda eklenen 10 klasik referansın metadata + DOI doğrulaması Crossref
canlı API ile yapıldı:

| Künye | DOI | Crossref eşleşme |
|---|---|---|
| `perris1980embu` | `10.1111/j.1600-0447.1980.tb00581.x` | ✓ (Perris 1980, Acta Psychiatr Scand) |
| `arrindell1983embuDimensions` | `10.1111/j.1600-0447.1983.tb00338.x` | ✓ **DÜZELTİLDİ** (aşağıya bkz.) |
| `baumrind1971parenting` | `10.1037/h0030372` | ✓ (Baumrind 1971, Dev Psychol) |
| `maccobyMartin1983` | — (kitap bölümü) | DOI'siz doğru (Handbook of Child Psych. Vol.4) |
| `schaefer1965crpbi` | `10.2307/1126465` | ✓ (Schaefer 1965, Child Dev) |
| `schaefer1959circumplex` | `10.1037/h0041114` | ✓ (Schaefer 1959, J Abnorm Soc Psychol) |
| `parker1979pbi` | `10.1111/j.2044-8341.1979.tb02487.x` | ✓ (Parker 1979, Br J Med Psychol) |
| `darlingSteinberg1993` | `10.1037/0033-2909.113.3.487` | ✓ (Darling & Steinberg 1993, Psychol Bull) |
| `beck1988bdiReview` | `10.1016/0272-7358(88)90050-5` | ✓ (Beck ve ark. 1988, Clin Psychol Rev) |
| `beck1996bdiII` | — (kitap) | DOI'siz doğru (BDI-II Manual) |

### ⚠️ Saptanan ve düzeltilen DOI hatası

`arrindell1983embuDimensions` künyesindeki DOI (`…tb06731.x`) Crossref'te
**tamamen alakasız bir makaleye** ("Effect of midazolam, flunitrazepam, and
placebo…") çözülüyordu. Crossref bibliyografik sorgusuyla doğru kayıt
bulundu ve DOI **`10.1111/j.1600-0447.1983.tb00338.x`** olarak düzeltildi
(başlık/yazar/yıl/dergi yeniden doğrulandı). Bu, mekanik atıf denetiminin değil
kaynak-kimlik doğrulamasının yakaladığı bir bütünlük hatasıdır.

- **Ledger:** 10 künye `referans-denetim-ledgeri.md` ana tablosuna `cite-ok`
  (identity-doğrulamalı) durumuyla eklendi; DOI-düzeltme not düşüldü.
- `bib_hygiene reconcile` (02): **HARD atıflı-tanımsız = 0** (tek SOFT
  `simonsohn2015specification`, 02'nin atıfı değil — genel bib alan eksiği).

Kapı 2 kararı: **PASS**

## Kapı 3: Bölüm Metni ve Resmi Kılavuz Uyumu — PASS

- [x] Resmi başlık: `# GENEL BİLGİLER`.
- [x] **4 yeni tablo Pandoc JSON ile geçerli**; tüm 02 dosyası sözdizim-geçerli.
- [x] **Tablo↔metin tutarlılığı:** Ebeveynlik kuramları tablosundaki her satır
  (Schaefer/Baumrind/Maccoby-Martin/Darling-Steinberg/Rohner) gövde metninde
  atıflı; EMBU gelişim tablosu (Perris/Arrindell/Castro/Dirik/Sümer) metinle
  birebir; T1DM evreleme tablosu ADA/ISPAD 3-evre standardıyla klinik doğru
  (`@dimeglio2018t1d; @haller2024ispadScreeningStaging`).
- [x] Ondalık **virgül** (eklenen içerikte 0,4 · 14,5 · 65,1 · 69,7 · 74,3);
  İngilizce-nokta `p`/etki değeri yok.
- [x] `@apalaci1996yoktez` (SRQ Türkçe uyarlaması) tez-kaynak istisnası —
  bu oturumda eklenmedi, Marmara §3.8.2 bilinçli istisna (03 sertifikasıyla
  tutarlı).

Kapı 3 kararı: **PASS**

## Kapı 4: Türkçe İmla, Akış ve Mantık — PASS

`tr_corpus_audit all` (axis H): **HARD 0 · SOFT 0 · advisory 76**, exit 0.

- **Baseline karşılaştırması (`git stash`):** baseline SOFT=4 · advisory=78;
  bu oturum sonrası **SOFT 4→0**. Yani bu oturumun genişletmesi 02'nin dil
  kalitesini **iyileştirdi**, yeni major/blocker üretmedi.
- Kalan advisory'ler tek-dosya `H-ABBR-UNUSED` artefaktı ve bir yanlış pozitif
  başlık uyarısı (`H-HC6c` §186 "T1DM bağlamında ebeveynlik" — başlık büyük
  harfli özel ad T1DM ile başlıyor; araç ilk sözcüğü yanlış saptıyor; bu oturum
  öncesinden mevcut).

Kapı 4 kararı: **PASS**

## Kapı 5: AI-Reliability ve Teknik Doğrulama — PASS

| Eksen | Sonuç |
|---|---|
| A referans bütünlüğü | 10 künye Crossref-doğrulı; 1 DOI hatası düzeltildi; orphan 0 |
| B claim grounding | Kuram/ölçek/evreleme iddiaları kaynakla desteklendi |
| C iç-tutarlılık | Tablo↔metin sayı ve yıl tutarlı |
| D halüsinasyon | Uydurma kaynak/yıl yok; klasik künyeler Crossref-teyitli |
| E kılavuz uyumu | T1DM evreleme ADA/ISPAD standardıyla uyumlu |
| F AI-şeffaflık | Repo-düzeyi AI-kullanım beyanı korunuyor |

- **Repo invaryant:** `doktoratezi-ai-audit` **144/144**;
  `t1dm-qual-ai-audit` **55/55**.
- **`git diff --check`:** temiz.
- **İzole render:** `pandoc --citeproc` (marmara-ama11.csl) 02'yi başarıyla
  derledi (exit 0, 190 KB); 7 yeni klasik referans + 4 tablo çıktıda çözüldü;
  **çözümsüz bib atıfı uyarısı yok**. 4 uyarı yalnız Quarto `tbl-` çapraz-referans
  önekleri (tam tez render'ında çözülür).

Kapı 5 kararı: **PASS**

## `certified-final` koşulları karşılandı

Tüm teknik/dil/referans/format kapıları PASS; doğrulanmış blocker = 0. Playbook
Nihai Karar Kuralı #5 gereği `certified-final` için gereken **açık kullanıcı
uygulama onayı** 2026-07-16 tarihinde bütünsel sertifikasyon kapsamında ("Uygun")
alınmıştır. Tam-tez render'ı (`quarto render thesis.qmd`) HTML+DOCX exit 0 ile
tamamlanmış; çözülmemiş atıf/çapraz-başvuru = 0. Durum `certified-final`.

## Nihai Sertifika Kararı

| Kapı | Karar |
|---|---|
| Kapı 0 | PASS |
| Kapı 1 | PASS |
| Kapı 2 | PASS (1 DOI hatası saptandı ve düzeltildi) |
| Kapı 3 | PASS |
| Kapı 4 | PASS (baseline SOFT 4→0 iyileşme) |
| Kapı 5 | PASS (144/144 + 55/55; render temiz) |
| **Nihai durum** | **`certified-final`** |

**Karar gerekçesi:** Bu oturumun tablo/anlatı genişletmesi ve 10 klasik
referansı güncel metinle yeniden denetlendi; bir DOI kimlik hatası saptanıp
düzeltildi, dil kalitesi iyileşti (SOFT 4→0), yeni blocker üretilmedi.
`certified-final` için gereken açık kullanıcı uygulama onayı 2026-07-16
tarihinde bütünsel sertifikasyon kapsamında ("Uygun") alınmıştır.
