# GİRİŞ ve AMAÇ — Kapsamlı Bölüm Talimatnamesi

> **Kanonik kural otoritesi:** Bölüm içerik kuralı →
> `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` §3.3 (genel çerçeve
> + bilimsel boşluk + önem/katkı + açık-ölçülebilir amaç); **alt başlık
> kullanılmaz** → §1.3; metin içi atıf → §1.8; tez-kaynak yasağı → §4.2. Bu
> talimatname kural tanımlamaz; bu teze özgü yürütme stratejisini verir. Klasör
> haritası: `03_bolum-hazirlik/README.md`.

## Bölüm İşlevi

`GİRİŞ ve AMAÇ` tez konusuna genel çerçeve verir, mevcut bilgi birikimini ve
bilinmeyen yönleri **özet** biçimde sunar, araştırmanın önemini/katkısını ortaya
koyar, temel araştırma sorusunu gerekçelendirir ve amacı **açık, ölçülebilir,
gerçekçi** biçimde ifade eder. **Alt başlık kullanılmaz** (marmara §1.3/§3.3);
akış paragraf düzeyinde kurulur. Bu bölüm karma tezin nicel (H1–H5) ve nitel
(triadik) kollarının **neden birlikte gerektiğini** kurar; ayrıntı yöntem/bulgu/
tartışmaya bırakılır. Gerçekleştirilmiş 8-paragraf akışı ve kaynak seti aşağıdaki
dated Uygulama Notlarında (2026-07-02, 2026-07-05) belgelidir.

## Yazım Sınırları (ihlal edilemez)

- **Amaç ≠ literatür özeti:** amaç doğrudan hedef cümlesidir; ayrıntılı literatür
  taraması Giriş'e değil `GENEL BİLGİLER`e aittir.
- **Hipotez ≠ araştırma sorusu:** ikisi karıştırılmaz; nitel araştırma sorusu
  nicel hipotezin basit açıklaması gibi sunulmaz.
- **Tez kaynağı kullanılmaz** (marmara §4.2): YÖK tez atıfları final metinde
  tam metni doğrulanmış hakemli dergi karşılığıyla değiştirilir.
- Ham veri/quote/aile demografisi girmez; sayısal prevalans/etki verilirse
  kaynak popülasyonu + belirsizlik + aktarılabilirlik **aynı cümlede** belirtilir.
- Ulusal boşluk iddiası mutlak yokluk olarak değil "belirgin değildir/
  sınırlıdır" kalıbıyla, hakemli literatür iziyle sınırlandırılır.

## Bu Tez İçin İçerik Sırası

1. T1DM'nin çocuk ve aile bağlamındaki önemi.
2. Ebeveyn tutumu, depresif belirti ve kardeş ilişkisi alanındaki bilimsel boşluk.
3. Nicel H1-H5 hattının gerekçesi.
4. Nitel triadik kolun gerekçesi.
5. Karma yöntem tasarımının neden gerekli olduğu.
6. Ana amaç ve varsa alt amaçlar.

## Kaynak Kapıları

- Repo içi: `docs/CLINICAL-STUDY-REPORT-FINAL.md`, `docs/analiz_planlari/`.
- Nitel: `niteliksel/qualitative_canonical_results_report.md`.
- Bağlam: `./dmnitel ai-context` ve Anamnesis/context gate.
- Dış literatür: Evidentia D0-D6 kaskadı.
- Tam metin: önce OpenAthens/kurumsal yayıncı erişimi, başarısızsa Anna's
  Library/annas-reader, ardından PMC/OA/repository ve diğer kanıtlı rotalar;
  tam metin veya açık istisna yoksa citation yok.
- Kaynakça: Zotero item key, BibTeX key ve `references/references.bib`
  mutabakatı.
- Kapanış: nitel ve nicel AI-reliability kontrolleri birlikte geçmeli.

## Yazım Kontrolü

- [x] Amaç literatür özeti değil, doğrudan hedef cümlesi.
- [x] Hipotez ve araştırma sorusu birbirine karıştırılmadı.
- [x] Nitel kol nicel hipotezlerin basit açıklaması gibi sunulmadı.
- [x] Her dış referans `referans-denetim-ledgeri.md` içinde tam metin, claim
      ve citation key düzeyinde izlendi.
- [x] Marmara kılavuzu §3.8.2: bölümde tez kaynağı kullanılmıyor (2026-07-05).

## Uygulama Notu - 2026-07-01

- `chapters/01_giris.qmd` resmi `# GİRİŞ ve AMAÇ` başlığıyla alt başlıksız
  altı-paragraf akışına dönüştürüldü.
- Doğrudan yazımda kullanılan dış kaynak seti:
  `whittemore2012`, `crandell2017`, `lummerAikey2021`, `deLosReyes2015`.
- Pinquart 2013 için Anna `read_article` 404 ve PubMed-EPMC `no-oa` kaldı;
  ancak MK OpenAthens üzerinden OUP resmi HTML tam metni doğrulandı ve Zotero
  item/URL/file attachment/not kapısı 2026-07-01'de kapatıldı.
- Sharpe/Rossiter 2002, Anna/PubMed-EPMC tam metin kapısı kapanmadığı için bu
  geçişte citation olarak kullanılmadı.
- Zotero Web API erişimi doğrulandı; Pinquart 2013 için `zotero-ok` kapısı
  kapandı. Diğer giriş kaynakları için Zotero import/write ayrı kapanış
  gerektirir.
- AI-reliability kapıları 2026-07-01'de çalıştırıldı: nitel gate 55/55,
  nicel gate 142/142 geçti. Bölüm Zotero import/write kapısı kapanmadığı için
  kaynakça açısından final-kapalı değildir.

## Uygulama Notu - 2026-07-02 (zenginleştirme koşusu)

- Bölüm, resmi kılavuz 3.3 beklentisine göre alt başlıksız sekiz-paragraf
  akışına genişletildi: (1) epidemiyolojik çerçeve + aile olayı, (2) ebeveynlik
  boyutları + meta-analitik fark kanıtı, (3) anne depresif belirti ekseni (H4
  gerekçesi), (4) sağlıklı kardeş ekseni + KİA/SRQ boyutları, (5) çoklu bilgi
  kaynağı gerekçesi, (6) Türkiye bağlamı + açık bilimsel boşluk + temel
  araştırma sorusu + katkı, (7) karma tasarım, (8) ana amaç + H1-H5 alt amaçlar.
- Yeni kullanılan citation'ların tamamı ledger'da kapısı kapalı kaynaklardır;
  yeni dış retrieval yapılmadı: `bell2025globalT1D`, `pinquart2013`,
  `chen2023parentDepression`, `ludvigsen2026siblingT1D`,
  `furmanBuhrmester1985srq`, `eviz2026turkiyeCare`, `tuncay2025yoktez`,
  `demirkiran2025yoktez`, `ayranci2025yoktez`.
- `pinquart2013` için bekleyen iki-kol AI-reliability koşusu 2026-07-02'de
  kapatıldı (nitel 55/55, nicel 142/142) → ledger durumu `cite-ok`.
- Ledger'da GİRİŞ'te yeniden kullanılan sekiz GENEL BİLGİLER kaynağının bölüm
  sütunu `GİRİŞ ve AMAÇ, GENEL BİLGİLER` olarak genişletildi.
- `chen2023parentDepression` sayıları ledger claim sınırında kullanıldı
  (genel %22,4; anne %31,5); öz-bildirim belirti dili korundu, klinik tanı
  dili kullanılmadı.
- Ulusal boşluk iddiası mutlak yokluk olarak değil "belirgin değildir /
  sınırlıdır" kalıbıyla, YÖK tez katmanı atıflarıyla sınırlandırılarak yazıldı.
- Bölüm sertifikasyon playbook'u (Kapı 0-5) henüz bu sürüm için yeniden
  koşulmadı; bölüm statüsü taslak/provisional'dır.

## Uygulama Notu - 2026-07-05 (§3.8.2 uyum + tam metin yeniden denetim)

- Marmara §3.8.2 (tez kaynak olamaz) uyarınca GİRİŞ metninde kalmış üç YÖK tez
  atfı hakemli dergi karşılıklarıyla değiştirildi: `tuncay2025yoktez →`
  `ozguven2025parentalCollab`/`ceran2024selfmgmt`, `demirkiran2025yoktez →`
  `adal2015psychosocial`, `ayranci2025yoktez → yuksel2024qol`. Ulusal literatür
  cümlesi "tez literatürü" yerine "hakemli literatür" kalıbına çevrildi; ulusal
  boşluk iddiası "belirgin değildir" formunda korundu. Bu, önceki
  sertifikasyonda (2026-07-01) bölümde tez atfı olmadığı için değerlendirilmemiş
  olan, 2026-07-02 zenginleştirme koşusunda eklenmiş tez atıflarının düzeltmesidir.
- Kardeş ekseninde `chanShorey2022` (full-text-exception) GİRİŞ metninden de
  çıkarıldı; tam metin kapısı 2026-07-05'te yeniden denetlendi (Anna SciDB
  yanlış-eşleşme reddi; PubMed-EPMC/Europe PMC/Unpaywall `no-oa`). Kardeş
  bilgi/duygusal destek/görünürlük gereksinimi iddiası tam metni açık
  `ludvigsen2026siblingT1D` + `lummerAikey2021` üzerine konsolide edildi.
- `ogle2022idfAtlas` tam metin gövdesi 2026-07-05'te yine açılamadı; headline
  insidans tahminleri NCBI yapısal abstract'ında doğrulandığından
  `cite-ok (abstract-doğrulamalı)` korundu.
- Sonuç: GİRİŞ'teki 18 dış atfın tamamı `cite-ok`; metinde `retired`/`exception`
  kaynak kalmadı. Yeni dış retrieval içerik iddiası eklemedi; değişim atıf-eşleme
  ve tam metin yeniden doğrulamayla sınırlıdır.
