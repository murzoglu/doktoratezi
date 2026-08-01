# 02_kanit-haritalari — Kanıt Haritaları Katmanı

Bu klasör tez yazımının **kanıt haritaları katmanı**dır: tez metnine giren her
iddianın kaynağa (repo kanıtı veya doğrulanmış dış referans) izlenebilir
kılındığı **tek kanonik yer**. Tek-otorite ilkesi geçerlidir — bir kayıt yalnız
bir dosyada tutulur; diğer dosyalar onu **yeniden yazmaz, işaret eder**
(bkz. `00_kaynak-kurallari/README.md`).

İki tür kanıt haritası vardır ve **çakışmaz**:
- **Dış referans denetimi** (dünyadan gelen citation) → `referans-denetim-ledgeri.md`.
- **Bölüm iddiası ↔ repo kanıtı** eşlemesi (kendi CSR/targets/protokol kanıtımız)
  → bölüm-bazlı kanıt haritaları (aşağıda, `Create later`).

## Tek-Otorite Haritası

| Dosya | Otorite alanı | Diğer dosyalarla ilişki |
|---|---|---|
| `referans-denetim-ledgeri.md` | **Dış referans denetimi** (kanonik): ledger satır şeması, durum makinesi (`candidate → cite-ok`) ve her citation'ın kaydı (DOI/PMID, tam metin, Zotero, claim, bölüm, iki-kol AI-reliability). | Dış citation denetiminin tek kaynağı. Kapı **sırasını** `talimatname` §4'e, kanıt/tam-metin **detayını** `evidentia` §4–5'e devreder. |

## Planlanan bölüm kanıt haritaları (`Create later` — ana plan fazları)

Her resmi bölüm için iddia ↔ kaynak eşlemesi ayrı dosyada üretilecek
(`tez-yazim-ana-plani.md` Faz 1–7 "Create later" adımları). Bu dosyalar **repo
kanıtı**nı (CSR, `_targets`, protokol, veri haritası) bölüm iddiasına bağlar;
dış citation'ları burada tekrar tutmaz, `referans-denetim-ledgeri.md`'ye işaret
eder.

| Dosya (planlanan) | Resmi bölüm |
|---|---|
| `giris-ve-amac-kanit-haritasi.md` | GİRİŞ ve AMAÇ |
| `genel-bilgiler-kanit-haritasi.md` | GENEL BİLGİLER |
| `gerec-ve-yontem-kanit-haritasi.md` | GEREÇ ve YÖNTEM |
| `bulgular-kanit-haritasi.md` | BULGULAR |
| `tartisma-ve-sonuc-kanit-haritasi.md` | TARTIŞMA ve SONUÇ |
| `kaynaklar-ekler-kanit-haritasi.md` | KAYNAKLAR ve EKLER |

## Kanıt haritaları katmanı dışı bağlı omurga (devredilen otoriteler)

| Konu | Kanonik otorite | Katman |
|---|---|---|
| Referans kapısı **sırası** (6 kapı, `/referans-kapisi`) | `00_kaynak-kurallari/talimatname-claude-code.md` §4 | 00 |
| Kanıt/tam-metin kaskadı (OpenAthens → Anna's → PMC/OA → Zotero) | `01_mimari/evidentia-entegrasyon-cercevesi.md` §4–5 + `00_kaynak-kurallari/tam-metin-erisim-kaskadi.md` | 01/00 |
| Künye biçimi (AMA-11, alfabetik) | `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` §4 | 00 |
| İki-kol AI-reliability + sci-audit (adli/imla) | `00_kaynak-kurallari/talimatname-claude-code.md` §6 | 00/plugin |
| Veri sınırı (KVKK) — uzun telifli pasaj ledger'a kopyalanmaz | `00_kaynak-kurallari/talimatname-claude-code.md` §2 | 00 |

## Öncelik zinciri

Çakışmada: (1) kullanıcı/danışman açık talimatı → (2) resmi `docs/tez-kilavuz/`
→ (3) `00_kaynak-kurallari` kanonik otorite (biçim/süreç) → (4) bu klasördeki
kanıt kaydı → (5) repo içi eski notlar. Bir citation'ın **durumu** yalnız bu
klasördeki ledger'da `cite-ok` olduğunda tez metnine girer; bir iddianın **repo
kanıtı** çakışırsa repo kanıtı (`_targets.R`, testler, protokol, CSR) üstündür.

## Duplikasyon önleme kuralı

Yeni bir kanıt kaydı eklenirken: dış citation ise `referans-denetim-ledgeri.md`
satırına; repo-kanıtı iddiası ise ilgili bölüm kanıt haritasına yazılır. Kapı
sırası, tam-metin kaskadı ve künye biçimi burada **tam metniyle tekrarlanmaz**;
yukarıdaki devredilen otoritelere pointer verilir (bkz. 2026-07-06 rafinasyonu:
ledger "Zorunlu Kapı Sırası" bölümü `talimatname` §4 + `evidentia` §5'e
devredildi, durum makinesi tek otorite olarak ledger'da bırakıldı).
