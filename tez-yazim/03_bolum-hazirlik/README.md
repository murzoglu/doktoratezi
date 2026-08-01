# 03_bolum-hazirlik — Bölüm Hazırlık / Talimatname Katmanı

Bu klasör tez yazımının **bölüm hazırlık katmanı**dır: her resmi Marmara bölümü
için, o bölümün **bu karma tezde** nasıl kurulacağını anlatan **kapsamlı
yürütme talimatnamesi**. Tek-otorite ilkesi geçerlidir (bkz.
`00_kaynak-kurallari/README.md`).

> **Temel ayrım:** Bu talimatnameler **biçim/içerik kuralı tanımlamaz**. Her
> resmi kural `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md`
> §3'tedir (bölüm içerik kuralları) ve buraya **yeniden yazılmaz**. Bu klasör
> yalnız **bu teze özgü yürütme stratejisi**ni taşır: paragraf/alt-başlık
> omurgası, kanıt eşlemesi (H1–H5 / triadik / dış literatür), karma yöntem
> bütünleştirmesi, anti-pattern'ler ve bölüm kapanış kapıları. Kural çakışırsa
> kanonik talimatname esastır.

## Tek-Otorite Haritası

| Dosya | Resmi bölüm | Yöneten kanonik kural |
|---|---|---|
| `01_giris-ve-amac.md` | GİRİŞ ve AMAÇ | marmara §3.3 (+ §1.3 alt başlıksız) |
| `02_genel-bilgiler.md` | GENEL BİLGİLER | marmara §3.4 |
| `03_gerec-ve-yontem.md` | GEREÇ ve YÖNTEM | marmara §3.5 (+ §6 karma, §7 nitel) |
| `04_bulgular.md` | BULGULAR | marmara §3.6 (+ §7 nitel, §8 istatistik) |
| `05_tartisma-ve-sonuc.md` | TARTIŞMA ve SONUÇ | marmara §3.7 (+ §1.3 alt başlıksız) |
| `06_kaynaklar-ekler.md` | KAYNAKLAR + EKLER | marmara §4 (AMA-11), §3.9–3.10 |

Not: Özet/Summary (marmara §3.2) ve ön bölümler (§2) hazırlık iskeleti
`02_sablonlar/`'dadır; bu klasör tez **metin** bölümlerinin hazırlığıdır.

## Bölüm hazırlık katmanı dışı bağlı omurga (devredilen otoriteler)

| Konu | Kanonik otorite | Katman |
|---|---|---|
| Bölüm içerik/biçim kuralları, bölüm sırası | marmara §3, §5 | 00 |
| Karma bölüm-kaynak-kapı haritası | marmara §6 + `01_mimari/iki-repo-entegrasyon-plani.md` | 00/01 |
| Nitel bulgu biçimi + nitel kol çıktı çerçevesi | marmara §7 + `05_entegrasyon/nitel-cikti-cercevesi.md` | 00/05 |
| Joint display alanları | `05_entegrasyon/nitel-nicel-joint-display-plan.md` | 05 |
| İstatistik yazım biçimi | marmara §8 (+ §1.4) | 00 |
| Referans kapısı + citation kaydı | `talimatname-claude-code.md` §4 + `02_kanit-haritalari/referans-denetim-ledgeri.md` | 00/02 |
| Doldurulacak iskelet | `02_sablonlar/bolum-sablonu.md` | 02 |
| Kritik kaynak seçimi | `06_kritik-kaynaklar/kritik-dosya-manifesti.tsv` | 06 |
| Bölüm sertifikasyonu (Kapı 0–5) | `04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md` | 04 |

## Üretim zinciri (bu talimatnamenin yeri)

```
03_bolum-hazirlik/<bölüm>.md   (bu katman: strateji + kanıt eşlemesi)
        │  iskelet: 02_sablonlar/bolum-sablonu.md
        │  kanıt kaydı: 02_kanit-haritalari/<bölüm>-kanit-haritasi.md + referans-denetim-ledgeri.md
        ▼
chapters/0X_*.qmd  →  thesis.qmd        (üretim: gerçek tez metni)
        │
        ▼
04_kalite-kontrol/  →  sertifika        (kapanış: format §12 + Kapı 0–5 + sci-audit)
```

## Sabitler (karıştırma)

- **Nicel kol:** 482 satır = 241 aile × 2 (DM=120, kontrol=121); EMBU-P/C, Beck,
  KİA/SRQ; H1–H5 (H5 diadik tutarlılık = birincil yenilik). Kaynak:
  `docs/CLINICAL-STUDY-REPORT-FINAL.md`, `_targets.R`.
- **Nitel kol:** 7 aile × 3 = 21 görüşme (triad: anne + T1DM'li çocuk + sağlıklı
  kardeş); RTA; **tez = 4 makro tema** (journal = 6 tema — karıştırma). Aktarım
  kaynağı: `niteliksel/06_manuscript_outputs/qualitative_canonical_results_for_doktoratezi.md`.
- İki kol **ayrı kanıt türü**; joint display kanıt türünü açık etiketler
  (marmara §6).

## Öncelik zinciri

Çakışmada: (1) kullanıcı/danışman → (2) resmi `docs/tez-kilavuz/` → (3)
`00_kaynak-kurallari` kanonik kural → (4) bu talimatname → (5) eski notlar.
Analiz/veri/hipotez kararında repo kanıtı (`_targets.R`, testler, protokol, CSR)
üstündür.

## Duplikasyon önleme kuralı

Bir biçim/içerik kuralı bu talimatnamelere **tam metniyle yazılmaz**; marmara
§3.x'e pointer verilir. Dated **Uygulama Notu** kayıtları audit-trail'dir —
silinmez, yalnız eklenir (bkz. 2026-07-06 rafinasyonu: dört bölüm talimatnamesi
kapsamlı hâle getirildi, kural tanımı tek otoriteye — marmara talimatnamesi —
bırakıldı, dated notlar korundu).
