# 05_entegrasyon — Nitel-Nicel Entegrasyon Katmanı

Bu klasör tez yazımının **karma entegrasyon katmanı**dır: nicel (H1–H5) ve nitel
(triadik, 4 makro tema) kolların **kanıt türü karıştırılmadan** bir araya
getirildiği **tek kanonik yer**. Tek-otorite ilkesi geçerlidir (bkz.
`00_kaynak-kurallari/README.md`).

> **Çekirdek ilke:** İki kol **ayrı kanıt türü**dür. Nitel tema nicel etki
> tahmini, nicel sonuç nitel temanın nedensel/mekanistik kanıtı yapılmaz; joint
> display iki kolu yan yana getirir ve ilişki türünü **açık etiketler** (marmara
> §6). H5 dyadic concordance'ta nicel *hangi boyut/ne kadar*, nitel *neden/nasıl*.

## Tek-Otorite Haritası

| Dosya | Otorite alanı | Diğer dosyalarla ilişki |
|---|---|---|
| `nitel-nicel-joint-display-plan.md` | **Joint display** (kanonik): tablo alanları + ilişki türü sözlüğü (uyum / tamamlayıcılık / ayrışma / açıklayıcı genişleme) + güvenli nicel/nitel kaynak listesi. | Joint display **alanlarının** tek kaynağı. `01_mimari/iki-repo-entegrasyon-plani.md` ve `03_bolum-hazirlik/04_bulgular.md` + `05_tartisma-ve-sonuc.md` buraya işaret eder. |
| `nitel-cikti-cercevesi.md` | **Nitel kol çıktı çerçevesi** (kanonik): RTA/COREQ/bilgi gücü, quote bütünlüğü, skill bağlayıcı ilkeleri, güvenli aktarım sözleşmesi, KVKK sınırı. | Nitel çıktının tek çerçevesi (`niteliksel-arastirma-rehberi-t1dm`). Joint display **alanını** plana devreder; kendi §0 otorite zinciri vardır. |
| `karma-kanit-ledgeri.tsv` | **Kanıt-ledger** (kanonik): ankraj-provenanslı her nicel-nitel kanıt satırı; her satır `{#tema-N}` / H1–H5 çapası ve dosya referansıyla işaretlidir. | Drift-guard: `scripts/util/karma_ledger_check.py` (`PYTHONDONTWRITEBYTECODE=1 python3 scripts/util/karma_ledger_check.py`, exit 0/1/2). HARD=0 olmadan bölüm final sayılmaz (bkz. Kapı 5 playbook). |
| `karma-sentez-kanonik.md` | **Kanonik karma sentez** (kanonik — tek doğruluk kaynağı): doldurulmuş joint-display + meta-çıkarım (Task 4 çıktısı). | BULGULAR joint-display / TARTIŞMA meta-çıkarım için birincil kaynak. `nitel-nicel-joint-display-plan.md` alan sözlüğüdür; doldurulmuş tablo bu dosyadadır. |

## Entegrasyon katmanı dışı bağlı omurga (devredilen otoriteler)

| Konu | Kanonik otorite | Katman |
|---|---|---|
| Karma bölüm-kaynak-kapı haritası | `marmara-tez-formati-talimatnamesi.md` §6 | 00 |
| Nitel bulgu biçimi (tema/rol, anonim alıntı, kanıt ayrımı) | marmara §7 | 00 |
| Karma yöntem derinliği (GRAMMS, MMAT, convergent parallel) | `t1dm-tez-rehberi/references/karma-yontem.md` | skill |
| Nitel metodoloji (RTA 6 faz, bilgi gücü, IRR, jüri) | `niteliksel-arastirma-rehberi-t1dm` skill | skill |
| Nitel iç veri denetimi (quote/codebook/COREQ/matris) | nitel kol (niteliksel/) `./dmnitel` komutları | repo |
| Bulgular/Tartışma yürütme talimatnamesi | `03_bolum-hazirlik/04_bulgular.md`, `05_tartisma-ve-sonuc.md` | 03 |
| Veri sınırı (KVKK — en yüksek hassasiyet) | `talimatname-claude-code.md` §2 + `nitel-cikti-cercevesi.md` §8 | 00/05 |

## Joint display üretim zinciri

```
Kanonik girdiler
  ├── nitel: niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd
  └── nicel: docs/CLINICAL-STUDY-REPORT-FINAL.qmd

05_entegrasyon/nitel-nicel-joint-display-plan.md   (alan + ilişki sözlüğü)
        │
        ▼
05_entegrasyon/karma-kanit-ledgeri.tsv             (ankraj-provenanslı kanıt-ledger)
        │  drift-guard: scripts/util/karma_ledger_check.py  [HARD=0 zorunlu]
        │
        ▼
05_entegrasyon/karma-sentez-kanonik.md             (doldurulmuş joint-display + meta-çıkarım)
        │
        ▼
BULGULAR (yorumsuz köprü)     →     TARTIŞMA (yorumlu karma bütünleştirme)
  chapters/04_bulgular.qmd           chapters/05_tartisma_ve_sonuc.qmd
  (brief: 03_bolum-hazirlik/04_bulgular.md)  (brief: 03_bolum-hazirlik/05_tartisma-ve-sonuc.md)
```

## Öncelik zinciri

Çakışmada: (1) kullanıcı/danışman → (2) resmi `docs/tez-kilavuz/` → (3)
`00_kaynak-kurallari` kanonik kural (biçim/süreç) → (4) bu klasördeki
entegrasyon otoritesi → (5) eski notlar. Nitel metodoloji kararında
`niteliksel-arastirma-rehberi-t1dm` skill, nicel/karma teknik kararda
`t1dm-tez-rehberi` skill birincildir.

## KVKK sınırı (bu katman en yüksek hassasiyette)

Ham görüşme metni özel nitelikli **sağlık + çocuk** verisidir; joint display'e
ve karma senteze **yalnız** de-identified tema/codebook/COREQ/audit-trail
çıktıları ve araştırmacı onaylı anonim alıntılar (aile no + rol etiketi / quote
ID) girer. Aile-düzeyi ayrıntı, demografi satırı ve ham alıntı satıra **girmez**
(tam metin: `nitel-cikti-cercevesi.md` §8).

## Duplikasyon önleme kuralı

Joint display alan/ilişki tanımı yalnız `nitel-nicel-joint-display-plan.md`'de;
nitel metodoloji/biçim yalnız `nitel-cikti-cercevesi.md`'de tutulur. Karma
bölüm-kaynak-kapı **haritası** marmara §6'da (burada tekrar edilmez). Yeni bir
joint display alanı önce plana, yeni bir nitel yazım ilkesi önce çerçeveye
yazılır; diğer belgeler pointer verir (bkz. 2026-07-06 rafinasyonu: iki dosya
Kapı/otorite başlıklarıyla omurgaya bağlandı).
