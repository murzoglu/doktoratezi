# Terim Düzeltme Adayları — Tespit + Uygulama Raporu

Oluşturma tarihi: 2026-07-29
Durum: **UYGULANDI (2026-07-29)** — aşağıdaki adaylar düzeltildi.

> **UYGULAMA NOTU (2026-07-29):** Kullanıcı kararıyla:
> - **A1 yönü TERSİNE çevrildi:** kanonik biçim `gizil` DEĞİL **`latent`**.
>   Tüm `gizil*` → `latent*` ve latent-anlamlı `gizli*` → `latent` yapıldı
>   (`gizli`=confounder, `gizlilik`, `gizli sinyal` metaforu KORUNDU). Bu kararın
>   Marmara `lang: tr` kuralına aykırı olduğu bildirildi ve kabul edildi.
> - **A5** yanlış keşif → yanlış-keşif (4 yer) uygulandı.
> - **B-grubu** tireleme hizalandı (azınlık tireli → baskın tiresiz; 34 değişiklik).
> - Kanonik sözlük `terim-sozlugu.yaml` A1 ters çevrildi; `K4-TERM-01` PASS.
> - Değişmezlik: sayı/istatistik/atıf/yön birebir korundu (03: 112=112 atıf).
>
> Aşağıdaki tablo, uygulama öncesi tespit dökümüdür (tarihsel kayıt).
Kaynak: (1) `terim_tutarlilik_audit.py` HARD bulguları (zorlanan A-grubu),
(2) sözlükte henüz zorlanmayan B/C-grubu tireleme adaylarının güncel taraması.
Yöntem: `python3 scripts/util/terim_tutarlilik_audit.py --json` + `grep` frekans.

> Değişmezlik: Her aday yalnız *terim-dili* düzeltmesidir; sayı/istatistik/atıf/
> yön DEĞİŞMEZ. Her düzeltme bağlam kontrolü ister (isim vs sıfat, kaynak-terimi).

---

## 1. KESİN ADAY — Audit HARD bulguları (zorlanan; K4-TERM-01 teslim engeli)

Bunlar sözlükte `zorlama: hard` olan terimlerin muafiyet-dışı ihlalleridir;
düzeltilene kadar `K4-TERM-01` FAIL verir.

| # | Konum | Bulunan | Kanonik biçim | Bağlam / not |
|---|---|---|---|---|
| 1 | `chapters/02_genel_bilgiler.qmd:398` | `Latent değişken` | **Gizil değişken** | Cümle başı: "Latent değişken kavramı, doğrudan gözlenemeyen yapının…". Gerçek gizil-yapı anlamı; ilk-geçişte `Gizil değişken (*latent variable*)` verilebilir. |
| 2 | `chapters/05_tartisma_ve_sonuc.qmd:424` | `gizli değişken` | **gizil değişken** | "…gizli değişken düzeyinde anne-çocuk uyuşmazlığı…". Gerçek latent (ölçüm modeli) anlamı — confounder DEĞİL; §4.4.6'ya atıf. |
| 3 | `chapters/00b_kisaltmalar.qmd:30` | `Yanlış Keşif` | **Yanlış-Keşif** | Kısaltma tablosu: "BH-FDR \| Benjamini-Hochberg Yanlış Keşif Oranı Düzeltmesi". Tireleme sabitlensin. |
| 4 | `chapters/00b_kisaltmalar.qmd:59` | `Yanlış Keşif` | **Yanlış-Keşif** | Kısaltma tablosu: "FDR \| Yanlış Keşif Oranı". |
| 5 | `chapters/03_gerec_ve_yontem.qmd:127` | `yanlış keşif` | **yanlış-keşif** | "…Benjamini-Hochberg yanlış keşif oranı düzeltmesi…". |
| 6 | `chapters/04_bulgular.qmd:8` | `yanlış keşif` | **yanlış-keşif** | "…çoklu karşılaştırma için Benjamini-Hochberg yanlış keşif…". |

**Not (A5 tireleme):** `yanlış-keşif` kararı yalnız FDR bileşik terimini bağlar;
ayrı kavram olan `çoklu karşılaştırma` dokunulmaz.

---

## 2. GÜÇLÜ ADAY — B-grubu tireleme (henüz zorlanmıyor; azınlık biçim düzeltilir)

Anlam net; yalnız biçimsel tutarlılık (baskın biçme hizalama). Her biri isim/sıfat
bağlam kontrolü ister. Sözlüğe `zorlama: hard` eklenmeden önce düzeltilmesi önerilir.

| # | Kavram | Baskın (kanonik) | Azınlık (aday) | Not |
|---|---|---|---|---|
| B1 | Aile içi | `aile içi` (61) | `aile-içi` (11) | Belirteç kullanımı baskın; sıfat-tamlaması için tutarlılık kararı. |
| B2 | Aile düzeyi | `aile düzeyi` (22) | `aile-düzeyi` (2) | Azınlık 2 kullanım hizalanır. |
| B3 | Etki büyüklüğü | `etki büyüklüğü` (25) | `etki-büyüklüğü` (2) | Azınlık 2 kullanım hizalanır. |
| B4 | Eksik veri | `eksik veri` (6) | `eksik-veri` (5) | Neredeyse eşit; isim "eksik veri" / sıfat "eksik-veri" ayrımı yapılabilir (kasıtlıysa bırak). |
| B5 | Çok düzeyli | `çok düzeyli` (13) | `çok-düzeyli` (7) | Baskın tiresiz; `multilevel` yalnız İng. özette kalmalı. |

---

## 3. İZLEME — C-grubu (çoğu kasıtlı ayrım; düzeltme ADAYI DEĞİL)

| # | Kavram | Durum | Karar |
|---|---|---|---|
| C1 | skor vs puan | `eğilim skoru` (7) türetilmiş · `ölçek puanı` (17) ham | **Kasıtlı ayrım — dokunma.** |
| C4 | bilgi verici tireleme | `bilgi-verici` (46) · `bilgi verici` (19) | Tireleme sabitlenebilir (baskın `bilgi-verici`); düşük öncelik. |
| B4-alt | kesme puanı/noktası | `kesme puanı` (2) · `kesme noktası` (2) | Eşanlamlı; tek biçim seçilebilir (düşük öncelik). |

---

## 4. YANLIŞ-POZİTİF — Düzeltilmemeli (teyit edildi)

| # | Görünen "tutarsızlık" | Neden yanlış-pozitif |
|---|---|---|
| Y1 | `Tip 1 Diyabet` (büyük D, 3) vs `Tip 1 diyabet` (52) | 3 kullanımın tamamı **başlık/künye**: `00a` künye, `00c` tez başlığı, `02` bölüm başlığı. Gövde tutarsızlığı yok. |
| Y2 | `gizli` (confounder, 04_bulgular:1281-1282) | Gözlenmeyen karıştırıcı anlamı (paragraf başı "Ölçülmemiş karıştırıcı"). Latent DEĞİL → audit paragraf-bağlamıyla INFO'ya düşürdü; **düzeltilmez**. |
| Y3 | `aşırı koruyuculuk`/`reddedicilik` (Dirik/meta-analiz bağlamı) | Kaynak-terimi ya da genel kuramsal kavram; audit bağlamsal muafiyetle INFO. Yalnız tezin *kendi alt ölçeği* olarak kullanılırsa aday olur — mevcut kullanımlar muaf. |

---

## 5. Özet ve önerilen sıra

- **Kesin (bölüm 1):** 6 HARD — A1 latent/gizli→gizil (2), A5 yanlış keşif→yanlış-keşif (4).
  Düzeltilene kadar `K4-TERM-01` teslim engeli.
- **Güçlü (bölüm 2):** B1-B5 tireleme — 5 kavram, ~24 azınlık kullanım; bağlam kontrolüyle.
- **İzleme (bölüm 3):** C1 kasıtlı (dokunma); C4/kesme düşük öncelik.
- **Dokunma (bölüm 4):** Y1-Y3 yalancı-pozitif.

Önerilen uygulama sırası: **bölüm 1 (A-grubu) → bölüm 2 (B-grubu) → sözlüğe B-grubu
`zorlama: hard` ekle (F5)**. Her tur sonrası `karma_ledger_check` +
`terim_tutarlilik_audit.py --fail-on hard` + ilgili `--section` orkestratör koşumu.

## 6. İlgili belgeler
- Sözlük (otorite): `docs/tez-kilavuz/terim-sozlugu.yaml`
- Tespit taraması (A1-A7 gerekçe): `docs/tez-kilavuz/TERIM_TUTARLILIK_TARAMASI.md`
- 3-katman tasarım: `docs/tez-kilavuz/ONERI_terim-sozlugu-ve-denetim-tasarimi.md`
- A1 detay: `docs/tez-kilavuz/ONERI_gizil-latent-ortuk-terim-standardi.md`
- Denetçi: `scripts/util/terim_tutarlilik_audit.py` · kapı `K4-TERM-01`
