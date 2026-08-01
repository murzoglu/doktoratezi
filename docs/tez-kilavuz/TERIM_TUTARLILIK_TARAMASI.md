# Terim Tutarlılık Taraması — Tutarsız İsimlendirme İçerebilen Terimler

Oluşturma tarihi: 2026-07-29
Durum: **tespit raporu** — bu belge hiçbir tez dosyasını değiştirmez; yalnız
tutarsız isimlendirme *adaylarını* önceliklendirilmiş biçimde listeler.
Kapsam: `chapters/*.qmd` (00c, 02, 03, 04, 05 + diğer bölümler)
Yöntem: Bilinen eşanlamlı/varyant çiftlerinin frekans taraması (`grep`), ardından
yanlış-pozitiflerin (İngilizce özet, ilk-geçiş parantezi, farklı kavram) elenmesi.

> Not: Frekanslar tarama anındaki değerlerdir; küçük sapmalar bağlam-elemesinden
> kaynaklanabilir. Öncelik sütunu düzeltme aciliyetini gösterir.

---

## A. YÜKSEK ÖNCELİK — Gerçek tutarsızlık, kavramsal karışıklık riski

Bu terimler aynı kavramı iki+ biçimde adlandırıyor ve okuyucuyu yanıltabilir
veya ölçek/yapı kimliğini bulanıklaştırabilir.

| # | Kavram | Bulunan varyantlar (frekans) | Önerilen tek biçim | Neden kritik |
|---|---|---|---|---|
| A1 | Gizil değişken | `latent` (48) · `gizil` (19) · `gizli` (13) · `örtük` (4) | **gizil** (ilk geçişte *latent*) | Ayrı belge var: `ONERI_gizil-latent-ortuk-terim-standardi.md`. Ayrıca `gizli` bir yerde *confounder* anlamında (farklı kavram!). |
| A2 | EMBU alt ölçeği "Aşırı Koruma" | `aşırı koruma` (86) · `aşırı koruyuculuk` (6) | **aşırı koruma** (alt ölçek adı olarak) | Alt ölçek adı; tablo/metin tutarlılığı zorunlu (kanonik form "Aşırı Koruma"). ⚠ Ancak `aşırı koruyuculuk`'un 6 kullanımının bir kısmı **genel kavramsal** anlamdadır (ör. 02_genel sat. 152 "özerklik desteği ile aşırı koruyuculuk arasındaki ayrım"), Dirik-özel değil. Yalnız *alt ölçek adı* olarak kullanıldığı yerler "aşırı koruma"ya hizalanmalı; genel kavramsal kullanım kasıtlı olabilir. |
| A3 | EMBU alt ölçeği "Reddetme" | `reddetme` (196) · `reddedicilik` (1) | **reddetme** | Aynı; kanonik form "Reddetme". `reddedicilik` Dirik'in terimidir, yalnız kaynak-anlatımında kalmalı. |
| A4 | Alt ölçek adı ⚠ bağlam ayrımı | tez alt ölçeği "aşırı koruma" · Dirik/genel kavram "aşırı koruyuculuk" | İki bağlamı **ayır**, körlemesine değiştirme | Üç ayrı kullanım var: (1) tezin *kendi alt ölçeği* → "aşırı koruma"; (2) *Dirik uyarlamasından söz* → onun terimi "aşırı koruyuculuk"; (3) *genel kuramsal kavram* → serbest. Yalnız (1) hizalanır. |
| A5 | Çoklu karşılaştırma düzeltmesi bağlamı | `çoklu karşılaştırma` (6) · `yanlış keşif` (2) · `yanlış-keşif` (11) | tireleme sabitle: **yanlış-keşif** | Aynı kavramın tireli/tiresiz karışımı. |
| A6 | Ölçek adı kısaltması | `s-EMBU` (26) · `EMBU` (181) · `KAET` (3) | Bağlama göre **s-EMBU** (kısa form) / **EMBU** (genel) | KAET = Dirik'in Türkçe kısaltması; yalnız Dirik bağlamında. Karışık kullanım netleştirilmeli. |
| A7 | KİA/SRQ ölçek adı | `KİA` (25) · `SRQ` (31) · `Kardeş İlişki(leri)` (20) | İlk geçişte tanımla, sonra **tek kısaltma** | Aynı ölçeğin üç adı; hangisinin birincil olduğu sabitlenmeli. |

---

## B. ORTA ÖNCELİK — Tireleme / yazım varyasyonu (kavram net, biçim tutarsız)

Anlam karışmıyor ama biçimsel tutarlılık (Marmara format + akış) için düzeltilmeli.

| # | Kavram | Varyantlar (frekans) | Önerilen | Not |
|---|---|---|---|---|
| B1 | Aile-içi | `aile içi` (61) · `aile-içi` (11) | **aile içi** (baskın) veya tek biçim | Sıfat/belirteç kullanımına göre karar. |
| B2 | Aile düzeyi | `aile düzeyi` (22) · `aile-düzeyi` (2) | **aile düzeyi** | Baskın biçim. |
| B3 | Etki büyüklüğü | `etki büyüklüğü` (25) · `etki-büyüklüğü` (2) | **etki büyüklüğü** | Baskın biçim. |
| B4 | Eksik veri | `eksik veri` (11) · `eksik-veri` (6) | tek biçim seç | İsim "eksik veri", sıfat "eksik-veri" ayrımı yapılabilir. |
| B5 | Çok düzeyli | `çok düzeyli` (17) · `çok-düzeyli` (8) · `multilevel` (metin içi) | **çok düzeyli** | `multilevel` yalnız İngilizce özette kalmalı (bkz. §D). |
| B6 | p değeri | `p değeri` (6) · `p-değeri` (0) | **p değeri** | Tutarlı; izleme için listede. |
| B7 | Kesme puanı / noktası | `kesme puanı` (2) · `kesme noktası` (2) | **kesme puanı** | İkisi eşanlamlı; tek biçim. |
| B8 | Tip 1 Diyabet yazımı | `Tip 1 Diyabet` (3) · `Tip 1 diyabet` (52) | **Tip 1 diyabet** | Büyük/küçük harf tutarlılığı (başlık dışı). |
| B9 | Eğilim skoru | `eğilim skoru` (10) · `eğilim puanı` (0) | **eğilim skoru** | Tutarlı; izleme. |

---

## C. DÜŞÜK ÖNCELİK — İzlenmeli, çoğu zaten tutarlı

| # | Kavram | Varyantlar | Durum |
|---|---|---|---|
| C1 | skor vs puan | `skor` (23) · `puan` (96) | **Farklı kullanımlar olabilir**: "eğilim skoru" (türetilmiş) vs "ölçek puanı" (ham). Kasıtlı ayrım olabilir; doğrula. |
| C2 | ölçüm vs ölçme | `ölçüm` (154) · `ölçme` (19) | "ölçme aracı" vs "ölçüm değeri" ayrımı olası; kasıtlıysa bırak. |
| C3 | örneklem vs örnek | `örneklem` (173) · `örnek` (183) | **Doğrulandı: yanlış-pozitif.** "örnek"in yalnız **1** kullanımı örneklem-dışı-olmayan; kalan ~182'si "örneğin/örnek olarak/bir örnek" bağlacı. Tutarsızlık YOK. |
| C4 | bilgi verici | `bilgi-verici` (47) · `bilgi verici` (22) · `informant` (12) | Tireleme sabitle: **bilgi verici**. `informant` İngilizce özet/parantez. |
| C5 | çoklu atama | `çoklu atama` (5) · `çoklu değerleme/atfetme` (0) | Tutarlı görünüyor; izleme. |
| C6 | veri seti | `veri seti` (10) · `veri kümesi/-seti` (0) | Tutarlı; izleme. |
| C7 | ön-kayıt | `ön-kayıt` (21) · `ön kayıt/önkayıt` (0) | Tutarlı; izleme. |

---

## D. YANLIŞ-POZİTİF — Tutarsızlık DEĞİL (düzeltilmemeli)

Bu varyasyonlar bilinçli/gerekli; standardizasyon bunlara dokunmamalı.

| # | Görünen "varyant" | Neden yanlış-pozitif |
|---|---|---|
| D1 | `T1D` (209) vs `T1DM` (201) | `T1D`, kelime-sınırıyla arandığında **0**; hepsi `T1DM`/`T1D-...` içinde. Gerçek bağımsız `T1D` yok. |
| D2 | `latent`, `dyadic`, `multilevel`, `informant` (İngilizce) | Büyük kısmı **İngilizce özette** (`00c`) veya **ilk-geçiş parantezinde** (`diadik (*dyadic*)`). İngilizce metinde İngilizce terim doğrudur. |
| D3 | `reddedicilik`, `aşırı koruyuculuk` (Dirik terimleri) | Dirik uyarlamasından **söz ederken** onun terimini kullanmak doğru; yalnız tezin *kendi* alt ölçeğini adlandırırken tez terimi kullanılmalı (bkz. A4). |
| D4 | `gizli` (confounder) | 2 kullanım *unmeasured confounder* anlamında — latent DEĞİL; "gizil"e çevrilmemeli (bkz. A1 notu). |
| D5 | `örnek` (örneğin) | Çoğu "örneğin/örnek olarak" bağlacı; ölçek-örneklem terimi değil. |

---

## E. Önerilen Sonraki Adım

Bu rapor yalnız **tespit**tir. Uygulama için önerilen sıra:

1. **A grubu önce** (kavramsal risk): A1 (gizil) → A2/A3/A4 (EMBU alt ölçek adları)
   → A6/A7 (ölçek kısaltmaları). Her biri ayrı, doğrulanabilir tur.
2. **B grubu** (tireleme): tek `grep`-tabanlı geçişle toplu düzeltilebilir; ama
   her biri bağlam kontrolü ister (isim vs sıfat).
3. **C grubu**: yalnız kasıtlı-ayrım teyidi; çoğu dokunulmadan bırakılabilir.
4. **D grubu**: dokunma.

Her uygulama turunda değişmezlik kuralı geçerli: sayı/istatistik/atıf/yön
korunur; yalnız terim-dili düzenlenir. Uygulama sonrası `karma_ledger_check` +
`tr_corpus_audit --fail-on blocker` çalıştırılmalı.

## F. İlgili belgeler

- Gizil-latent-örtük standardı (A1 detayı): `docs/tez-kilavuz/ONERI_gizil-latent-ortuk-terim-standardi.md`
- Kanonik EMBU alt ölçek adları (A2-A4): `docs/protokol/KANONIK_KISALTILMIS_EMBU_COCUK.md`, `docs/protokol/KANONIK_KISALTILMIS_EMBU_EBEVEYN.md`
- Arrindell/Dirik terim farkı (A4/D3): `docs/protokol/ARRINDELL_DIRIK_DERIN_FARK_ANALIZI.md`
