# Referans Denetim Ledgeri

Bu ledger, tez metnine girecek her dış referans için bibliyografik kimlik,
tam metin kanıtı, Zotero mutabakatı, claim/pasaj izi ve iki repo
AI-reliability kapanışını tek yerde izler.

> **Otorite zinciri:** Bu dosya **dış referans denetiminin tek kanonik
> yeri**dir — ledger satır şeması, durum makinesi (`Durum Sözlüğü`) ve her
> citation'ın kaydı burada tutulur. Devredilen otoriteler: referans **kapısı
> sırası** → `00_kaynak-kurallari/talimatname-claude-code.md` §4
> (`/referans-kapisi`); **kanıt/tam-metin detayı** →
> `01_mimari/evidentia-entegrasyon-cercevesi.md` §4–5 +
> `00_kaynak-kurallari/tam-metin-erisim-kaskadi.md`; **künye biçimi (AMA-11)** →
> `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` §4. Klasör
> haritası: `02_kanit-haritalari/README.md`.

## Zorunlu Kapı Sırası

Kapı sırasının **kanonik detayı** tek yerdedir, burada tekrarlanmaz: süreç
sırası → `00_kaynak-kurallari/talimatname-claude-code.md` §4
(`/referans-kapisi`); kanıt/tam-metin detayı →
`01_mimari/evidentia-entegrasyon-cercevesi.md` §4–5 +
`00_kaynak-kurallari/tam-metin-erisim-kaskadi.md`. Özet sıra — bu ledger'ın
her satırının kapatması gereken kapılar:

bağlam (anonim/türetilmiş) → bibliyografik kimlik (DOI/PMID/PMCID/OpenAlex/YÖK)
→ tam metin (OpenAthens → Anna's → PMC/OA → Zotero attachment) → Zotero
mutabakatı (item key ≠ BibTeX key; `references/references.bib` export) →
claim/pasaj notu → çift AI-reliability (`t1dm-qual-ai-audit` +
`doktoratezi-ai-audit`). Kapı kapanmadan satır durumu `cite-ok` olmaz.

**Ledger sınırı (KVKK/telif):** Uzun telifli tam-metin pasajı ledger'a
kopyalanmaz; yalnız sayfa/pasaj düzeyi claim notu tutulur
(`talimatname-claude-code.md` §2).

## Durum Sözlüğü

Bu durum makinesi (`candidate → cite-ok`) referans denetiminin **kanonik durum
otoritesi**dir; diğer belgeler (talimatname §4, evidentia §5, ana plan) buna
işaret eder, yeniden tanımlamaz.

| Durum | Anlam |
|---|---|
| `candidate` | Kaynak bulundu, henüz tez citation adayı olarak onaylanmadı. |
| `full-text-ok` | Tam metin veya eşdeğer resmi metin kanıtı görüldü. |
| `full-text-exception` | Tam metne erişilemedi; kullanım gerekçesi açıkça yazıldı ve ayrıca gözden geçirilecek. |
| `zotero-ok` | Zotero item key, BibTeX key ve `references/references.bib` mutabık. |
| `reliability-ok` | Nitel ve nicel AI-reliability kapıları geçti. |
| `cite-ok` | Kaynak tez metnine citation olarak girebilir. |
| `retired` | Kaynak kullanılmayacak; neden notu yazıldı. |

Tam metin rota ayrıntısı için bkz.
`tez-yazim/00_kaynak-kurallari/tam-metin-erisim-kaskadi.md`.

## Ledger

2026-07-01 yazım oturumunda `GİRİŞ ve AMAÇ` bölümü için dört dış
referans taslak metne alınmıştır. İlk Zotero taramasında kayıtlar proje
collection'ında bulunmamış, ardından açık onayla Zotero Web API senkronizasyonu
tamamlanmıştır. Güncel durumda kullanılan tüm citation'lar `T1DM Thesis`
collection'ında item, attachment/note ve pin'li BibTeX key ile kapalıdır.

| Citation key | DOI/PMID/ID | Zotero item key | Tam metin kanıtı | Kullanılan iddia | Bölüm | Nitel AI | Nicel AI | Durum | Not |
|---|---|---|---|---|---|---|---|---|---|
| `whittemore2012` | DOI: `10.1177/0145721712445216`; PMID: `22581804`; PMCID: `PMC3401246` | `F2JMM3VP`; URL attachment `XHZ52THA`; note `FGM3VEAJ` | PubMed/PMC `PMC3401246` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | T1DM ebeveynlerinde günlük bakım sorumluluğu, aile rutini değişimi, psikolojik sıkıntı ve çocuk/aile sonuçlarıyla ilişki. | `GİRİŞ ve AMAÇ` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `whittemore2012` olarak pin'lendi. |
| `crandell2017` | DOI: `10.1037/fsh0000305`; PMID: `29172624`; PMCID: `PMC5880719` | `BZPDC2SR`; URL attachment `IQMHF6WI`; note `8NSZ5CVQ` | PubMed/PMC `PMC5880719` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Kronik fiziksel hastalığı olan çocuklarda ebeveynlik boyutları ile çocuk iyilik hali arasındaki ilişki. | `GİRİŞ ve AMAÇ, GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `crandell2017` olarak pin'lendi; dergi yayın yılı 2018, tez citation key'i korunur. |
| `lummerAikey2021` | DOI: `10.1177/1074840720977177`; PMID: `33305651`; Semantic Scholar `a8f0eb4d4f4ba866a618958a8dc6ea7e73c336a3` | `JWHTB4R6`; URL attachment `4RUITFXZ`; note `SCPVNQQA` | Anna `annas-reader` Bearer MCP `article_search` ve `read_article` DOI/Crossref eşleşmesi; PubMed-EPMC/Unpaywall `no-oa`; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Kronik hastalık bağlamında sağlıklı kardeş uyumu; deneyim, psikososyal uyum, baş etme ve iletişim temaları. | `GİRİŞ ve AMAÇ` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `lummerAikey2021` olarak pin'lendi. |
| `deLosReyes2015` | DOI: `10.1037/a0038498`; PMID: `25915035`; PMCID: `PMC4486608`; Semantic Scholar `5e3385e32737b4234e1f892f936066c4de07e6d2` | `MIDTPNQH`; URL attachment `HKPRVBFM`; note `WP8K48UM` | PubMed/PMC `PMC4486608` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Çoklu bilgi kaynağı yaklaşımında düşük-orta örtüşmenin bağlama/role özgü bilgi olarak yorumlanabilmesi. | `GİRİŞ ve AMAÇ` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `deLosReyes2015` olarak pin'lendi. |
| `pinquart2013` | DOI: `10.1093/jpepsy/jst020`; PMID: `23660152`; OpenAlex `W2156083233` | `WMIPQ3M7`; attachment `XUKCX94W`; URL attachment `M8TKJ6KB`; notes `KMRMARKQ`, `DRA4G9N5` | MK OpenAthens -> OUP resmi HTML tam metin erişimi doğrulandı; Zotero'ya HTML tam metin snapshot PDF'i ve yayıncı URL'si eklendi; Zotero `T1DM Thesis` collection `9ZFDHMZA`. Anna `article_search` DOI kimliğini buldu, ancak eski `read_article` denemesi 404; PubMed-EPMC `no-oa`; PDF uç noktası Cloudflare doğrulamasına takıldı. | Kronik fiziksel hastalık bağlamında ebeveyn-çocuk ilişkisi, sıcaklık/duyarlılık, kontrol ve aşırı koruyuculuk farklarına ilişkin meta-analitik kanıt. | `GİRİŞ ve AMAÇ, GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `pinquart2013` olarak pin'lendi; duplicate `HA5D36RQ` sürüm korumalı Web API delete ile kaldırıldı. OUP HTML snapshot yayıncı PDF'i değildir. 2026-07-02 giriş zenginleştirme koşusunda çift AI-reliability geçti; citation `chapters/01_giris.qmd` metnine alındı. |
| `sharpeRossiter2002` | DOI: `10.1093/jpepsy/27.8.699` | yok | Anna `read_article` 404. | Eski/aday kardeş kronik hastalık meta-analizi. | `GİRİŞ ve AMAÇ` | not-run | not-run | `retired` | Kardeş ekseni için tam metni doğrulanan `lummerAikey2021` kullanıldı. |
| `ada2026children` | DOI: `10.2337/dc26-S014`; PMID: `41358890`; PMCID: `PMC12690182` | `5JM3EIX6`; URL attachment `GNHSM4PA`; note `W7QKQCCS` | PubMed/PMC `PMC12690182` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Pediatrik T1DM bakımında gelişimsel, aile katılımlı ve psikososyal bağlama duyarlı bakım çerçevesi. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `ada2026children` olarak pin'lendi. |
| `deWit2022ispadPsychological` | DOI: `10.1111/pedi.13428`; PMID: `36464988`; PMCID: `PMC10107478` | `6H8NHHZ9`; URL attachment `IXEP5QDQ`; note `JPEBAGX7` | PubMed/PMC `PMC10107478` canlı tam metin; ISPAD Chapter 15 resmi sayfası 2024 güncel yüzey olarak ayrıca doğrulandı; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Psikososyal tarama, bakım veren iyilik hali, aile işlevselliği, ebeveyn katılımı, özerklik desteği, iletişim ve teknoloji yükü. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `deWit2022ispadPsychological` olarak pin'lendi. |
| `eviz2026turkiyeCare` | DOI: `10.4274/jcrpe.galenos.2025.2025-1-7`; PMID: `41090400`; PMCID: `PMC12989894` | `DZD64HM5`; URL attachment `PQH8T3GG`; note `9ERT4KZX` | PubMed/PMC `PMC12989894` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Türkiye'de pediatrik T1DM bakımında kapsamlı aile eğitimi, ekip çalışması, bireyselleştirilmiş plan, teknoloji kullanımı, ulusal veri sınırlılığı, çalışma döneminde sensör geri ödeme durumu ve sosyoekonomik aktarılabilirlik sınırı. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `eviz2026turkiyeCare` olarak pin'lendi. |
| `trojanowski2021` | DOI: `10.1093/jpepsy/jsab064`; PMID: `34657955`; OpenAlex `W3205701329` | `DWAU45FS`; URL attachment `DGX22ZRR`; note `AE9VPWMW` | MK OpenAthens login sonrası OUP resmi HTML tam metin sayfasında `Abstract`, `Materials and Methods`, `Risk of Bias`, `Results`, `Discussion`, `Clinical Implications` ve PDF linki görüldü. PubMed-EPMC/Unpaywall ve OpenAlex OA/repository `closed`; Anna `article_search` DOI eşleşti, `read_article` 404. | T1DM gençlerinde ebeveynlik, aile çatışması, eleştirel ebeveynlik, destek, katılım ve ilişki kalitesinin psikolojik sağlıkla ilişkisi. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `trojanowski2021` olarak pin'lendi; resmi HTML tam metin PDF yerine kabul edildi. 2026-07-05: GİRİŞ 2. paragrafta destekleyici/eleştirel ebeveynlik-diyabet distresi cümlesinde zaten kullanıldığı bölüm sütununa yansıtıldı. |
| `chen2023parentDepression` | DOI: `10.3389/fendo.2023.1095729`; PMID: `36936139`; PMCID: `PMC10014558` | `2NHFKRDE`; URL attachment `99UPRGDG`; note `DU7FUJ7H` | PubMed/PMC `PMC10014558` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Ebeveyn depresyon/depresif belirti prevalansı: genel %22,4; anneler %31,5; babalar %16,3; 12 yaş altı çocuk ebeveynleri %32,3; ergen ebeveynleri %16,0. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `chen2023parentDepression` olarak pin'lendi; klinik tanı değil öz-bildirim belirti alanı olarak kullanılacak. |
| `chanShorey2022` | DOI: `10.1016/j.pedn.2021.12.002`; PMID: `34929508`; OpenAlex `W4200560240` | `QIAE8E7K`; URL attachment `UWFJGJK2`; note `KDZEC4DJ` | OpenAthens/ScienceDirect denemesi headless/IP blok ekranında kaldı; resmi Journal of Pediatric Nursing PDF URL'si bulundu ancak Cloudflare otomatik erişimi engelledi; Anna `article_search` DOI eşleşti fakat `read_article` yanlış fuzzy match'i reddetti; NUS ScholarBank metadata var ancak `TEXT` bitstream `401 restricted`; Europe PMC `isOpenAccess: false`, OpenAlex `oa_status: closed`, `any_repository_has_fulltext: false`. | T1DM tanılı çocukların sağlıklı kardeşlerinin deneyim ve gereksinimleri için sistematik derleme adayı. | — (metinde kullanılmıyor) | 55/55 passed | 142/142 passed | `full-text-exception` | Metindeki ana citation yükü `ludvigsen2026siblingT1D` kaynağına kaydırıldı; Chan/Shorey manuel kurumsal erişim kapanana kadar final citation olarak kullanılmamalı. 2026-07-05: GİRİŞ kardeş paragrafından da çıkarıldı; kardeş bilgi/duygusal destek/görünürlük gereksinimi iddiası `ludvigsen2026siblingT1D` (T1DM-özgü nitel, PMC OA) + `lummerAikey2021` (kardeş uyumu bütünleştirici derleme) üzerine konsolide edildi. Anna `read_article` DOI kayıtlı ancak SciDB yanlış-eşleşme reddi; PubMed-EPMC/Unpaywall `no-oa` (2026-07-05 yeniden doğrulandı). |
| `ludvigsen2026siblingT1D` | DOI: `10.1177/26350106261442180`; PMID: `42159283`; PMCID: `PMC13219770`; OpenAlex `W7161753006` | `6HTRN4MF`; URL attachment `FXFWHKES`; note `STVW6DX5` | PubMed/PMC `PMC13219770` canlı tam metin; OpenAlex OA `hybrid`, license `cc-by`, repository full text var; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | T1DM tanılı çocuğun sağlıklı kardeşlerinde tanı döneminin zorluğu, aile atmosferi, dahil edilme isteği, günlük yaşam yükü, gece alarmı, ebeveyn yorgunluğu ve bilgi/destek gereksinimi. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `ludvigsen2026siblingT1D` olarak pin'lendi; `references.bib` girdisi temizlendi. |
| `tuncay2025yoktez` | YÖK Tez No. `935669`; detail key `AduC2X1gXt_-LXqq8aVtQQ`; encrypted no `VJ6aT40-pEoQL5ApWj57oA` | `N3ZEJMDK`; URL attachment `IUSCZMJE`; note `6FPPG5AF` | YÖK Tez izinli tam metin; PDF page 1 erişimi doğrulandı, toplam 102 sayfa. | Türkiye örnekleminde T1DM'li çocuk/ergenlerde ebeveyn tutumları, öz bakım gücü ve hastalığa yönelik tutum ilişkisini yerel literatür katmanı olarak göstermek. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `retired` | Zotero BibTeX key `tuncay2025yoktez` olarak pin'lendi.  2026-07-03: Marmara kılavuzu §3.8.2 (tez kaynak olamaz) uyarınca GENEL BİLGİLER metninden çıkarıldı; dergi karşılığı `ceran2024selfmgmt / ozguven2025parentalCollab`. |
| `tatar2023yoktez` | YÖK Tez No. `793371`; detail key `ym_jLg6RI5Z6INC_my0d4w`; encrypted no `g_E5VJlV7R5fMp1P5iDU2w` | `V5FAQHKR`; URL attachment `F5NJSWH5`; note `FXV7UTIT` | YÖK Tez izinli tam metin; PDF page 1 erişimi doğrulandı, toplam 98 sayfa. | Türkiye örnekleminde T1DM'li ergenlerde ebeveyn izlemi ve diyabetin aileye etkisi kesişimini yerel literatür katmanı olarak göstermek. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `retired` | Zotero BibTeX key `tatar2023yoktez` olarak pin'lendi.  2026-07-03: Marmara kılavuzu §3.8.2 (tez kaynak olamaz) uyarınca GENEL BİLGİLER metninden çıkarıldı; dergi karşılığı `ozguven2025parentalCollab`. |
| `avan2017yoktez` | YÖK Tez No. `473884`; detail key `DvZLHQ6MBM7mesxbjk0-ew`; encrypted no `jWusuN4jzH6TGc63tJfJ5w` | `EGSQ5W2Z`; URL attachment `ENNFGMU4`; note `XSSJWK92` | YÖK Tez izinli tam metin; PDF page 1 erişimi doğrulandı, toplam 107 sayfa. | Türkiye örnekleminde diyabet bakımında ebeveyn izlemi, tedaviye uyum ve metabolik parametreler ilişkisinin yerel çalışma örneği. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `retired` | Zotero BibTeX key `avan2017yoktez` olarak pin'lendi.  2026-07-03: Marmara kılavuzu §3.8.2 (tez kaynak olamaz) uyarınca GENEL BİLGİLER metninden çıkarıldı; dergi karşılığı `ozguven2025parentalCollab`. |
| `kesenYener2024yoktez` | YÖK Tez No. `915866`; detail key `_4WcKKPMzVwtmLoPJB58nQ`; encrypted no `SlhkrKcLpuqsknqZ8INSWg` | `Z7VJNS2A`; URL attachment `MC9MP86G`; note `ATJPERE3` | YÖK Tez izinli tam metin; PDF page 1 erişimi doğrulandı, toplam 95 sayfa. | Türkiye örnekleminde T1DM hipoglisemi korkusunu çocuk ve ebeveyn formlarıyla ölçmeye yönelik yerel psikometrik çalışma. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `retired` | Zotero BibTeX key `kesenYener2024yoktez` olarak pin'lendi.  2026-07-03: Marmara kılavuzu §3.8.2 (tez kaynak olamaz) uyarınca GENEL BİLGİLER metninden çıkarıldı; dergi karşılığı `senCelasin2018plbss`. |
| `demirkiran2025yoktez` | YÖK Tez No. `956108`; detail key `XCGolJL_9C9e8JczB7ZSog`; encrypted no `juJRmrCqFwzChRgVSN0hzQ` | `BETBXWXD`; URL attachment `XJE7GK28`; note `BHTA5V9K` | YÖK Tez izinli tam metin; PDF page 1 erişimi doğrulandı, toplam 103 sayfa. | Türkiye örnekleminde algılanan helikopter ebeveynlik, diyabet yönetimi/öz yeterlilik, uyum, psikolojik sağlamlık ve anksiyete/depresyon kesişimini yerel literatür katmanı olarak göstermek. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `retired` | Zotero BibTeX key `demirkiran2025yoktez` olarak pin'lendi.  2026-07-03: Marmara kılavuzu §3.8.2 (tez kaynak olamaz) uyarınca GENEL BİLGİLER metninden çıkarıldı; dergi karşılığı `ozguven2025parentalCollab / adal2015psychosocial`. |
| `turk2015yoktez` | YÖK Tez No. `448907`; detail key `q3b73mAO6hBrS5wmP8RnTg`; encrypted no `teSYS89LFJbbZfI1vY4ZNA` | `AWJNJ8HR`; URL attachment `MI94RDHS`; note `5EJEHX5G` | YÖK Tez izinli tam metin; PDF page 1 erişimi doğrulandı, toplam 68 sayfa. | Türkiye örnekleminde T1DM'li adölesanlarda diyabet bakımında ebeveyn izlemi ölçeğinin psikometrik arka planı. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `retired` | Zotero BibTeX key `turk2015yoktez` olarak pin'lendi.  2026-07-03: Marmara kılavuzu §3.8.2 (tez kaynak olamaz) uyarınca GENEL BİLGİLER metninden çıkarıldı; dergi karşılığı `ozguven2025parentalCollab`. |
| `cetintas2019yoktez` | YÖK Tez No. `612448`; detail key `Jem1jaZr2bW_38b0wLlv2Q`; encrypted no `IlgIlxo6FRhgMWR6O3XOHA` | `PQN4W2PK`; URL attachment `235VTPEQ`; note `7AFGHTGB` | YÖK Tez izinli tam metin; PDF page 1 erişimi doğrulandı, toplam 97 sayfa. | Türkiye örnekleminde diyabetin aileye etkisi ölçeğinin Türkçe geçerlik-güvenirlik çalışmasını yerel psikometrik kaynak olarak göstermek. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `retired` | Zotero BibTeX key `cetintas2019yoktez` olarak pin'lendi.  2026-07-03: Marmara kılavuzu §3.8.2 (tez kaynak olamaz) uyarınca GENEL BİLGİLER metninden çıkarıldı; dergi karşılığı `cetintas2021dfis`. |
| `bell2025globalT1D` | DOI: `10.1111/dom.16501`; PMID: `40536127`; PMCID: `PMC12312823` | `XUXVD2CK`; URL attachment `TSVBQFJW`; note `UDMD7TWZ` | PubMed/PMC `PMC12312823` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Küresel T1DM epidemiolojisi, çocukluk/ergenlikte artan prevalans, tanı yaşının ve DKA/teknoloji-veri boşluklarının kavramsal bağlamı. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `bell2025globalT1D` olarak pin'lendi. |
| `tauschmann2025ispadGlucoseMonitoring2024` | DOI: `10.1159/000543156`; PMID: `39884260`; PMCID: `PMC11854985` | `P542X9BR`; URL attachment `CBS3CE8T`; note `6E97NBQQ` | PubMed/PMC `PMC11854985` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Pediatrik T1DM'de BGM, CGM ve AID ekosistemi; teknoloji erişimi, veri yorumlama, alarm yükü ve aile içi sorumluluk paylaşımı. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `tauschmann2025ispadGlucoseMonitoring2024` olarak pin'lendi. |
| `lindholmOlinder2022ispadEducation` | DOI: `10.1111/pedi.13418`; PMID: `36120721`; PMCID: `PMC10107631` | `5ZBKMDE4`; URL attachment `GWTXTW5F`; note `98TEZH4P` | PubMed/PMC `PMC10107631` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Diyabet eğitimini tanıdan itibaren ve yaşam boyu devam eden, aile ve bakım verenleri içeren, psikososyal uyum ve öz-yeterliği kapsayan yapılandırılmış süreç olarak kurmak. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `lindholmOlinder2022ispadEducation` olarak pin'lendi. |
| `abraham2022ispadHypoglycemia` | DOI: `10.1111/pedi.13443`; PMID: `36537534`; PMCID: `PMC10107518` | `HWGVZTB2`; URL attachment `QU679U5B`; note `G6ZN4EP8` | PubMed/PMC `PMC10107518` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Hipoglisemi ve hipoglisemi korkusunu çocuk ve bakım verenler için fizyolojik-psikolojik bariyer, gece izlem, okul/spor güvenliği ve ebeveyn kontrol davranışı bağlamı olarak açıklamak. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `abraham2022ispadHypoglycemia` olarak pin'lendi. |
| `sangha2026diabetesDistress` | DOI: `10.3389/fcdhc.2026.1652578`; PMID: `42368394`; PMCID: `PMC13293899` | `29TNFV9B`; URL attachment `4W2N6A36`; note `R3WT7FTN` | PubMed/PMC `PMC13293899` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Ergen ve ebeveyn perspektifinde diabetes distress'in günlük yaşam, akran/okul desteği, stigma, gelecek maliyeti ve sorumluluk devri bağlamında dyadik yaşanması. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `sangha2026diabetesDistress` olarak pin'lendi. |
| `vieira2026parentFOH` | DOI: `10.3390/bs16060942`; PMID: `42352775`; PMCID: `PMC13295629` | `WIJQE8RW`; URL attachment `C8SKH9CI`; note `Z9WX4NB7` | PubMed/PMC `PMC13295629` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Ebeveyn emotion regulation, hipoglisemi korkusu-worry/behavior boyutları ve parental diabetes distress arasındaki ilişkileri kesitsel/ilişkisel çerçevede açıklamak. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `vieira2026parentFOH` olarak pin'lendi; nedensel dil kullanılmamalı. |
| `quinn2026t1dScreeningPsychosocial` | DOI: `10.1007/s00125-026-06717-2`; PMID: `42065735`; PMCID: `PMC13236767` | `H5PKSF9U`; URL attachment `EDB2N78R`; note `E4CRQKME` | PubMed/PMC `PMC13236767` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Pediatrik T1DM'nin güncel staging/screening ufkunda aile kaygısı, risk bilgisi, izlem davranışı, ortak karar ve veri mahremiyeti gibi psikososyal-etik boyutları kavramsal sınır notu olarak açıklamak. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `quinn2026t1dScreeningPsychosocial` olarak pin'lendi. |
| `ayranci2025yoktez` | YÖK Tez No. `953420`; detail key `NJ9Kp_4c1cW6zXpiBlWqqQ`; encrypted no `GosktCRLLH7KUmCx7glmzA` | `IFB9XK34`; URL attachment `BJWSFJS7`; note `5Q8MZPTB` | YÖK Tez izinli tam metin; PDF page 1 erişimi doğrulandı, toplam 95 sayfa. | Türkiye bağlamında T1DM yönetim yöntemi, akran zorbalığı, depresyon/anksiyete ve yaşam kalitesi kesişimini yerel okul-akran/psikososyal tez katmanı olarak göstermek. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `retired` | Zotero BibTeX key `ayranci2025yoktez` olarak pin'lendi; yerel tez kanıtı olarak sınırlı kullanılacak.  2026-07-03: Marmara kılavuzu §3.8.2 (tez kaynak olamaz) uyarınca GENEL BİLGİLER metninden çıkarıldı; dergi karşılığı `yuksel2024qol / adal2015psychosocial`. |
| `mokkink2018cosmin` | DOI: `10.1007/s11136-017-1765-4`; PMID: `29260445`; PMCID: `PMC5891552` | `M8T9FFS6`; URL attachment `P8K6AQTU`; note `SPWV22PB` | PubMed/PMC `PMC5891552` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | COSMIN ölçüm özellikleri, yapısal geçerlik, iç tutarlılık, kültürler arası geçerlik ve ölçüm değişmezliği çerçevesini psikometri okuryazarlığı için açıklamak. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `mokkink2018cosmin` olarak pin'lendi. |
| `putnickBornstein2016measurementInvariance` | DOI: `10.1016/j.dr.2016.06.004`; PMID: `27942093`; PMCID: `PMC5145197` | `7KZ76DAM`; URL attachment `Z8IAPCSB`; note `ZGA932JT` | PubMed/PMC `PMC5145197` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Configural, metric, scalar ve residual ölçüm değişmezliği basamaklarını kavramsal olarak açıklamak. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `putnickBornstein2016measurementInvariance` olarak pin'lendi. |
| `trizanoHermosilla2016omegaAlpha` | DOI: `10.3389/fpsyg.2016.00769`; PMID: `27303333`; PMCID: `PMC4880791` | `4XXRXT7M`; URL attachment `PRRABMHI`; note `HJAC8VMS` | PubMed/PMC `PMC4880791` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Cronbach alfa sınırları, omega katsayısı ve çarpık/congeneric madde koşullarında iç tutarlılık yorumunu açıklamak. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `trizanoHermosilla2016omegaAlpha` olarak pin'lendi. |
| `li2016ordinalCFA` | DOI: `10.3758/s13428-015-0619-7`; PMID: `26174714` | `NZV7W3N3`; URL attachment `GEC8WCD3`; note `8G8RGZB8` | Springer resmi tam metin sayfası ve PubMed metadata doğrulandı; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Dört-beş kategorili Likert maddeler için ordinal CFA, WLSMV/MLR ve küçük örneklem uyum yorumu bağlamını açıklamak. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `li2016ordinalCFA` olarak pin'lendi. |
| `dirik2015sEmbuTurkish` | PMID: `26111288` | `9WNZ4HAB`; URL attachment `CJTXXIHK`; note `ZGV2R6HI` | Türk Psikiyatri Dergisi resmi PDF tam metni; PubMed metadata doğrulandı; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | S-EMBU-C/KAET-Ç Türkçe psikometrik zemini ve algılanan ebeveynlik ölçümünün yakın araçlarla kıyaslanabilirliğini açıklamak. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Tezdeki 29 maddelik paralel EMBU-P/C ile birebir aynı form gibi yazılmayacak. |
| `hisli1989bdiTurkishUniversity` | Psikoloji Dergisi 7(23):3-13; açık PDF | `THXA6EC4`; URL attachment `5VCAN8XA`; file attachment `UAUNRWTV`; note `38GH4PXT` | Türk Psikologlar Derneği PDF arşivi; PDF 9 sayfa, taranmış; sayfa 1 görsel kontrolü ile başlık/yazar/özet doğrulandı. | Beck Depresyon Envanteri Türkçe geçerlik-güvenirlik zeminini depresif belirti dili için sınırlı kullanmak. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Kesme noktası veya klinik tanı sonucu olarak kullanılmayacak. |
| `akturk2005bdipcTurkish` | Türkiye Aile Hekimliği Dergisi 9(3):117-122 | `BB76NUEU`; URL attachment `BM58AXHB`; note `CSRGFIBS` | Turkish Journal of Family Practice açık erişim/CC BY makale sayfası doğrulandı; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | BDI-PC/BDÖ-BB kısa tarama alternatifini Beck ailesinde Türkiye validasyon örneği olarak göstermek. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 21 maddelik Beck Depresyon Envanteri ile birebir eşdeğer gibi yazılmayacak. |
| `furmanBuhrmester1985srq` | PMID: `3987418`; DOI: `10.2307/1129733` | `H8VZE5PT`; URL attachment `3U2ISEFQ`; note `36APDHQ2` | University of Denver PDF tam metin ve PubMed metadata doğrulandı; Anna Crossref DOI eşleşmesi; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | SRQ/KİA'nın sıcaklık/yakınlık, göreli statü/güç, çatışma ve rekabet boyutlarını kavramsal olarak açıklamak. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | Kardeş ilişkisini yalnız aile konstelasyonu değişkenlerine indirgememek için kullanılacak. 2026-07-05 sertifikasyon: bayat item `Z5RKE9QG` Zotero'da 404 bulundu; DOI `10.2307/1129733` ile T1DM Thesis collection üyeliği yeniden kuruldu ve BibTeX key `furmanBuhrmester1985srq` pinlendi (yeni item `H8VZE5PT`). |
| `apalaci1996yoktez` | YÖK Tez No. `52148`; detail key `hJ3EPiUcex4VqnPi_fClcA`; encrypted no `hJ3EPiUcex4VqnPi_fClcA` | `79P3BCMC`; URL attachment `7M7UE8JS`; note `KDKXNIG7` | YÖK MCP thesis details ve PDF gate doğrulandı; toplam 157 sayfa, page 1 retrieval başarılı ancak OCR boş/taranmış çıktı. | KİA/SRQ'nun Türkiye uyarlama/kullanım tarihçesinde YÖK tez katmanını göstermek. | `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | Ham tez verisi veya ayrıntılı alıntı kullanılmayacak.  2026-07-03: Marmara §3.8.2 istisnası — SRQ/KİA Türkçe uyarlama hattının önemli birincil kaynağı olduğu için danışman kararıyla korundu (bölümdeki tek tez-kaynak istisnası). 2026-07-07: GEREÇ ve YÖNTEM §Kardeş İlişkileri Anketi'nde SRQ'nun Türkçe uyarlama kaynağı olarak metne bağlandı (bilinçli tez-yasağı istisnası, kullanıcı onayı). |
| `aktas2017kardesIliskileriOlcegi` | DOI: `10.21764/maeuefd.340206` | `RX4SHNCT`; URL attachment `W2JFZ83W`; note `RQ5FEFHX` | DergiPark PDF tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Türkiye'de kardeş ilişkileri için yerel ölçek geliştirme, AFA/DFA ve güvenirlik örneğini alternatif araç olarak açıklamak. | `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | Tezde kullanılan KİA/SRQ yerine geçmiş gibi yazılmayacak. 2026-07-07: GEREÇ ve YÖNTEM §Kardeş İlişkileri Anketi'nde 'ek/karşılaştırmalı kaynak' olarak eklendi; kullanılan araç olarak sunulmadı (bu not korundu). |
| `cetintas2021dfis` | DOI: `10.1111/jspn.12308`; PMID: `32844587` | `4E2VMUUC`; note `2V6DI5VB`; URL attachment `USW37IJK`; T1DM Thesis `9ZFDHMZA` | Anna's Archive Crossref-doğrulamalı tam metin; DFIS Türkçe geçerlik-güvenirlik (121 ebeveyn, 6-18 yaş T1DM). | Diyabetin aileye etkisi ölçeğinin Türkçe geçerlik-güvenirliği. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: `cetintas2019yoktez` tezinin dergi versiyonu (aynı yazar); §3.8.2 tez-yasağı uyumu için değiştirme. |
| `senCelasin2018plbss` | DOI: `10.4274/jcrpe.5028`; PMID: `28825591`; PMCID: `PMC5985386` | `6TKF4MS5`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC5985386` canlı tam metin. | Türkçe ebeveyn hipoglisemi korkusu ölçeği (P-LBSS) geçerliği; worry/behavior boyutları. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: `kesenYener2024yoktez` yerine (§3.8.2). §2.2'deki worry/behavior cümlesini de destekler. |
| `ozguven2025parentalCollab` | DOI: `10.4274/jcrpe.galenos.2024.2024-4-7`; PMID: `39711005`; PMCID: `PMC12118314` | `9BRQJZG8`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC12118314` canlı tam metin. | Türkiye T1DM ergen; ebeveyn katılımı/izlemi → öz-yeterlik, yaşam kalitesi, HbA1c. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: `tatar2023yoktez`, `avan2017yoktez`, `turk2015yoktez` yerine (§3.8.2). 2026-07-05: GİRİŞ ulusal literatür cümlesinde `tuncay2025yoktez` tez atfının dergi karşılığı olarak eklendi. |
| `yuksel2024qol` | DOI: `10.14744/SEMB.2024.21456`; PMID: `39021699`; PMCID: `PMC11249999` | `ENDQ6QEV`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC11249999` canlı tam metin. | Türkiye olgu-kontrol; T1DM'de depresyon/anksiyete daha yüksek, yaşam kalitesi daha düşük. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: `ayranci2025yoktez` yerine (§3.8.2); akran zorbalığı iddiası kaldırıldı. 2026-07-05: GİRİŞ ulusal literatür cümlesine psikososyal sonuç hattı için eklendi. |
| `ceran2024selfmgmt` | DOI: `10.1007/s00431-024-05650-z`; PMID: `38864877`; PMCID: `PMC11322394` | `C5JXI4HW`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC11322394` canlı tam metin. | Türkiye T1DM ebeveyn öz-yönetim ölçeği geliştirme-geçerlik (190 ebeveyn). | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: `tuncay2025yoktez` yerine (§3.8.2). 2026-07-05: GİRİŞ ulusal literatür cümlesine ebeveyn öz-yönetimi hattı için eklendi. |
| `adal2015psychosocial` | DOI: `10.4274/jcrpe.1745`; PMID: `25800477`; PMCID: `PMC4439893` | `Z8SN66BQ`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC4439893` canlı tam metin. | Türkiye 295 T1DM ergen; depresyon/anksiyete + algılanan aile desteği (BDI). | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: `demirkiran2025yoktez` / `ayranci2025yoktez` destek kaynağı (§3.8.2). 2026-07-05: GİRİŞ ulusal literatür cümlesine psikososyal uyum hattı için eklendi. |
| `dimeglio2018t1d` | DOI: `10.1016/S0140-6736(18)31320-5`; PMID: `29916386`; PMCID: `PMC6661119` | `WJVX8GXN`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC6661119` canlı tam metin (Lancet seminer). | T1DM tanımı: otoimmün beta-hücre yıkımı, insülin eksikliği, kronik hiperglisemi; patogenez, insülin rejimleri ve DKA genel çerçevesi. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.1 textbook yeniden yazımı; T1DM temel tanım/patofizyoloji otoriter seminer kaynağı. |
| `deBock2022ispadGlycemicTargets` | DOI: `10.1111/pedi.13455`; PMID: `36537523`; PMCID: `PMC10107615` | `S9CBWMPP`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC10107615` canlı tam metin. | ISPAD 2022 glisemik hedefler ve glukoz izlemi; HbA1c hedefi, hedef aralıkta geçirilen süre (TIR). | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.1 HbA1c/glisemik hedef tanımı. |
| `compas2012coping` | DOI: `10.1146/annurev-clinpsy-032511-143108`; PMID: `22224836`; PMCID: `PMC3319320` | `UMIRI6XR`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC3319320` canlı tam metin. | Kronik hastalıkta çocuk/ergen baş etme ve uyum; kontrol-temelli baş etme modeli, tedaviye uyumu etkilemesi, psikososyal uyum. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.4 kronik hastalık/gelişim/baş etme kaynağı (Elicit ile bulundu, PMC OA). |
| `rollandWalsh2006` | DOI: `10.1097/01.mop.0000245354.83454.68`; PMID: `16969168` | `NMXVNM5P`; T1DM Thesis `9ZFDHMZA` | Anna's Archive Crossref-doğrulamalı tam metin (Curr Opin Pediatr). | Aile Sistemleri–Hastalık modeli; çocuk/ergen kronik hastalığında aile dinamikleri, uyum, hastalık davranışı ve seyir ilişkisi. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.5 aile sistemleri kuramsal çerçeve (Elicit→Anna's). |
| `rosland2012family` | DOI: `10.1007/s10865-011-9354-4`; PMID: `21691845` | `BM38N9FH`; T1DM Thesis `9ZFDHMZA` | Anna's Archive Crossref-doğrulamalı tam metin (J Behav Med). | Aile davranışları ve iletişim örüntülerinin kronik hastalık sonuçlarıyla ilişkisi (erişkin hasta; ilke aktarımı): uyum/dikkatli yanıt olumlu, eleştiri/aşırı koruma/kontrol olumsuz. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.5 aile davranışı/iletişim; erişkin→pediatrik dolaylı aktarım etiketli. |
| `pinquart2017parentingDimensions` | DOI: `10.1037/dev0000295`; PMID: `28459276` | `DC3Z572U`; T1DM Thesis `9ZFDHMZA` | Anna's Archive Crossref-doğrulamalı tam metin (Dev Psychol). | Ebeveynlik boyutları/stilleri ile çocuk/ergen sonuçları meta-analizi: sıcaklık/davranışsal kontrol/özerklik tanıma/otoritatif koruyucu; sert-psikolojik kontrol/otoriter riskli. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.6 ebeveynlik boyut/stil kuramsal temel (Elicit→Anna's). |
| `rohner2004parAcceptance` | DOI: `10.1037/0003-066X.59.8.830`; PMID: `15554863` | `2GG5FNE4`; T1DM Thesis `9ZFDHMZA` | Anna's Archive Crossref-doğrulamalı tam metin (Am Psychol). | Ebeveyn kabul-red kuramı (PARTheory): sıcaklık-sevgi/düşmanlık/ihmal/red; algılanan kabul-red ↔ psikolojik uyum; sıcaklık bağlanma sinyali. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.6 kabul-red + bağlanma kaynağı (Elicit→Anna's). |
| `arrindell2005sembu` | DOI: `10.1027/1015-5759.21.1.56` | `UIK78UVM`; T1DM Thesis `9ZFDHMZA` | RUG kurumsal repository OA PDF (Eur J Psychol Assess). | s-EMBU algılanan ebeveyn tutumu aracı; üç alt ölçek (reddetme, duygusal sıcaklık, aşırı koruma) ve kültürler-arası faktör geçerliği; öz-bildirim doğası. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.7 EMBU çerçevesi/boyutları (Elicit→OA). |
| `castro1993embuChildren` | DOI: `10.1177/002076409303900105`; PMID: `8478163` | `VC3I6MSX`; T1DM Thesis `9ZFDHMZA` | Anna's Archive Crossref-doğrulamalı tam metin (Int J Soc Psychiatry). | EMBU'nun çocuk örnekleminde (7-12 yaş) dört faktörü: Duygusal Sıcaklık, Reddetme, Kontrol Çabaları, Favouring Subject (kayırma/karşılaştırma). | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.7 çocuk EMBU 4 boyut/karşılaştırma (Elicit→Anna's). |
| `young2014parentalInvolvement` | DOI: `10.1007/s11892-014-0546-5`; PMID: `25212099`; PMCID: `PMC4283591` | `REG3BXGC`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC4283591` canlı tam metin. | T1DM'li gençlerde ebeveyn katılımının miktar, tip (izlem/problem çözme) ve nitelik (sıcak/eleştirel) boyutları biyopsikososyal sonuçlarla ilişkili; paylaşılan sorumluluk. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.8 diyabette ebeveyn katılımı/izlem niteliği (Elicit→PMC OA). |
| `jaser2011familyInteraction` | DOI: `10.1007/s11892-011-0222-y`; PMID: `21853415`; PMCID: `PMC3370388` | `UTUICUG4`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC3370388` canlı tam metin. | Pediatrik T1DM'de aile etkileşimi; ergenliğe geçerken ebeveyn izleminin önemi, en iyi sonuçların sıcak/iş birlikçi katılımla; ebeveyn distresinin rolü. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.8 aile etkileşimi/izlem-sıcaklık (Elicit→PMC OA). |
| `goodman2020parentingMediator` | DOI: `10.1007/s10567-020-00322-4`; PMID: `32734498` | `ZEHTTTDD`; T1DM Thesis `9ZFDHMZA` | Anna's Archive Crossref-doğrulamalı tam metin (Clin Child Fam Psychol Rev). | Anne depresyonu → sorunlu ebeveynlik (aracı) → çocuk işlevi; hem olumlu (sıcaklık) hem olumsuz ebeveynlik aracılık eder; ebeveynlik değiştirilebilir; aracılık nedenselliğin gerekli ama yeterli olmayan göstergesi. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-04: §2.10 anne depresif belirti→ebeveynlik yolları (Elicit→Anna's). |
| `yesilkaya2016turkiyeIncidence` | DOI: `10.1111/dme.13063`; PMID: `26814362` | `FBXASA3B`; T1DM Thesis `9ZFDHMZA` | Anna's Archive Crossref-doğrulamalı tam metin (Diabetic Medicine). | Türkiye ilk ulusal kayıt (SGK 2011-2013): 17.175 prevalan, prevalans 0,75/1.000, 2013'te 2.465 yeni olgu, yaşa-standardize insidans 10,8/100.000 (WHO), tanı yaşı ort. 10,6±4,6, en yüksek oran 10-14 yaş (%40,6). | `GİRİŞ ve AMAÇ` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-05: §1 Türkiye epidemiyoloji (Elicit→Anna's). |
| `ogle2022idfAtlas` | DOI: `10.1016/j.diabres.2021.109083`; PMID: `34883188` | `A83GVB7G`; T1DM Thesis `9ZFDHMZA` | **Kanıt notu:** headline insidans tahminleri NCBI E-utilities yapısal abstract'ında birebir; makale açık erişim; otomatik PDF/HTML fetch yayıncı bot-koruması nedeniyle 403 (Unpaywall+Anna's), tam metin gövdesi görülmedi. | IDF Atlas 10. baskı: 2021'de <15 yaş 108.300, <20 yaş 149.500 yeni tanı; 215 ülke/bölge. | `GİRİŞ ve AMAÇ` | 55/55 passed | 142/142 passed | `cite-ok` (abstract-doğrulamalı) | 2026-07-05: §1 küresel insidans headline (Elicit→NCBI abstract + doğrulanmış OA). |
| `haller2024ispadScreeningStaging` | DOI: `10.1159/000543035`; PMID: `39662065`; PMCID: `PMC11854978` | `MM4MZPQI`; URL attachment + note (import-doi) | PubMed/PMC `PMC11854978` canlı tam metin (JATS bölümleri çekildi: Screening/Goals/Psychological Burden/Conclusions); Zotero `T1DM Thesis` collection `9ZFDHMZA`. | T1DM tarama/evreleme: presemptomatik Evre 1-2, Evre 3 klinik başlangıç; popülasyon/genetik-risk otoantikor taraması; tanıda DKA %15-80 dünya geneli → tarama+izlemle <%5; teplizumab ile ilerlemeyi geciktirme; tarama pozitifliğinde ebeveyn (özellikle anne) kaygı/depresif belirti; çocuk ruh sağlığı-bakım veren baş etme ilişkisi. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: §2.1 geniş zenginleştirme; ISPAD 2024 staging/screening PMC-OA. Zotero BibTeX key `haller2024ispadScreeningStaging` olarak pin'lendi. |
| `ziegler2013isletAutoantibodies` | DOI: `10.1001/jama.2013.6285`; PMID: `23780460`; PMCID: `PMC4878912` | `4BK7VMZW`; URL attachment + note (import-doi) | PubMed/PMC `PMC4878912` canlı tam metin; abstract sayısal iddialar birebir doğrulandı; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | ≥2 adacık otoantikoru olan çocuklarda 10 yılda T1D'ye ilerleme %69,7 (%95 GA 65,1-74,3); tek otoantikor %14,5; otoantikor yok %0,4 (15 yaş). | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: §2.1 doğal seyir/evreleme sayısal kanıtı. Zotero BibTeX key `ziegler2013isletAutoantibodies` olarak pin'lendi. |
| `adolfsson2022ispadExercise` | DOI: `10.1111/pedi.13452`; PMID: `36537529`; PMCID: `PMC10107219` | `Z9NSBXJD`; URL attachment + note (import-doi) | PubMed/PMC `PMC10107219` canlı tam metin (PMCID çözümlendi); Zotero `T1DM Thesis` collection `9ZFDHMZA`. | ISPAD 2022 egzersiz: egzersizin diyabet yönetiminin parçası olması ve hipoglisemi riski nedeniyle planlama/ayarlama gerektirmesi. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: §2.1 beslenme-egzersiz paragrafı. Zotero BibTeX key `adolfsson2022ispadExercise` olarak pin'lendi. |
| `buchberger2016depressionAnxiety` | DOI: `10.1016/j.psyneuen.2016.04.019`; PMID: `27179232` | `A4USNWGM`; URL attachment + note (import-doi) | Anna's `read_article` Crossref-doğrulamalı tam metin gövdesi (sayfa 1 başlık/yazar/dergi + abstract eşleşti); PubMed metadata; PMC yok; OpenAthens bu oturumda yüklü değil; Zotero `T1DM Thesis` `9ZFDHMZA`. | Çocuk/ergen T1DM'de depresif belirti havuzlanmış prevalans %30,04 (%95 GA 16,33-43,74; 14 çalışma), anksiyete belirtileri %32'ye varan; belirti düzeyleri glisemik kontrolle ilişkili; erken psikososyal tarama gereği. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: §2.2 çocuk psikososyal morbidite. Zotero BibTeX key pin'lendi. Kullanıcı candidate PMID hatalı çıktı (aphid genetiği); doğru PMID `27179232` distiller ile bulundu. |
| `hagger2016diabetesDistress` | DOI: `10.1007/s11892-015-0694-2`; PMID: `26748793` | `HVSCHJSE`; URL attachment + note (import-doi) | Anna's `read_article` Crossref-doğrulamalı tam metin gövdesi (sayfa 1 başlık/yazar/dergi + abstract eşleşti); PubMed metadata; PMC yok; OpenAthens yüklü değil; Zotero `9ZFDHMZA`. | Ergenlerde diyabet sıkıntısı: yaklaşık üçte biri yüksek DD; suboptimal glisemik kontrol/düşük öz-yeterlik/azalmış öz-bakımla ilişkili; DD psikiyatrik tanı değil, depresyon/anksiyeteden ayrı ama ilişkili. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: §2.2 diyabet sıkıntısı yapısı. Zotero BibTeX key pin'lendi. Kullanıcı candidate PMID hatalı (nörobilim); doğru PMID `26748793` distiller ile bulundu. |
| `franceschi2021cgmPsychological` | DOI: `10.3389/fped.2021.660173`; PMID: `34026692`; PMCID: `PMC8131655` | `43UV8EQH`; URL attachment + note (import-doi) | PubMed/PMC `PMC8131655` canlı tam metin; Zotero `9ZFDHMZA`. | Pediatrik CGM psikolojik sonuçlar sistematik derleme: isCGM ergenlerde DD/aile çatışması/hipoglisemi korkusu/QoL iyileştirebilir; rtCGM memnuniyet/QoL artırır ama diyabet yükü/aile çatışması/depresif belirti üzerinde etkisiz; uyku/anksiyete tartışmalı. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: §2.2 teknoloji-psikososyal. Zotero BibTeX key pin'lendi. Nedensel dil kullanılmadı. |
| `canha2025aidDistress` | DOI: `10.1111/dme.15503`; PMID: `39726162`; PMCID: `PMC11929561` | `WJFHSMCR`; URL attachment + note (import-doi) | PubMed/PMC `PMC11929561` canlı tam metin; Zotero `9ZFDHMZA`. | AID→diyabet sıkıntısı meta-analizi (40 çalışma; 1131 pediatrik, 1085 bakım veren): bakım verenlerde orta düzey DD azalması (BAS SMD -0,48; RCT -0,22), özellikle küçük çocuk ebeveynleri; çocuk/ergen hastalarda anlamlı değişiklik yok. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: §2.2 AID-psikososyal. Zotero BibTeX key pin'lendi. İlişkisel dil; nedensellik yok. |
| `younghyman2016adaPsychosocial` | DOI: `10.2337/dc16-2053`; PMID: `27879358`; PMCID: `PMC5127231` | `Z8C6M2A2`; URL attachment + note (import-doi) | PubMed/PMC `PMC5127231` canlı tam metin; Zotero `9ZFDHMZA`. | ADA psikososyal bakım pozisyon bildirisi: depresyon/diyabet sıkıntısı/anksiyete dahil rutin psikososyal taramanın diyabet bakımına entegre edilmesi önerisi (tüm yaşlar). | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: §2.2 rutin psikososyal tarama. Zotero BibTeX key pin'lendi. |
| `sahin2015parentalAttitude` | DOI: `10.5152/npa.2015.7248`; PMID: `28360693`; PMCID: `PMC5353187` | `J9PESGNX`; URL attachment + note (import-doi) | PubMed/PMC `PMC5353187` canlı tam metin (Nöropsikiyatri Arşivi OA); Zotero `T1DM Thesis` `9ZFDHMZA`. | Türkiye çok merkezli: 50 T1DM ergen (12-18y) + 50 kontrol + ebeveynleri (PARI ölçeği); otoriter ebeveyn tutumu T1DM grubunda daha yaygın; ebeveynler kaçınma temelli baş etmeyi daha sık kullanıyor; ergen psikopatoloji %68. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: §2.3 tez çekirdek kavram (algılanan ebeveyn tutumu) Türkiye örneği. Zotero BibTeX key pin'lendi. |
| `kucukdag2024maternalEmotion` | DOI: `10.4183/aeb.2024.477`; PMID: `41069543`; PMCID: `PMC12506879` | `6VCUNKV9`; URL attachment + note (import-doi) | PubMed/PMC `PMC12506879` canlı tam metin; Zotero `9ZFDHMZA`. | Türkiye (Düzce): 70 T1DM + 70 sağlıklı çocuk ve anneleri; diyabetli çocuk annelerinde Beck depresyon puanları, DERS duygu düzenleme güçlükleri (nonacceptance/clarity/impulse) ve helplessness baş etme kontrol annelerine göre daha yüksek. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: §2.3 tez çekirdek kavram (anne depresif belirtileri/duygu düzenleme) Türkiye örneği. Zotero BibTeX key pin'lendi. |
| `dundar2023turkiyeIncidence` | DOI: `10.5152/TurkArchPediatr.2023.23036`; PMID: `37670553`; PMCID: `PMC10544421` | `A5VEX7VF`; URL attachment + note (import-doi) | PubMed/PMC `PMC10544421` canlı tam metin (Turkish Archives of Pediatrics OA); Zotero `9ZFDHMZA`. | Türkiye (Malatya il düzeyi kohort, <18y, 2007-2019, TÜİK payda): ortalama T1DM insidansı 13,1/100.000 çocuk-yıl (kız 13,8; erkek 12,4); artan trend AAPC +%8,3; en dik artış 15-17 yaş (AAPC %30,1). İl düzeyi — ulusal değil. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: §2.3 güncel Türkiye insidans trendi; §1 ulusal kayıt (`yesilkaya2016turkiyeIncidence`) ile ayrı veri/coğrafya/dönem. Zotero BibTeX key pin'lendi. |

| `fang2025techDisparities` | DOI: `10.1001/jamanetworkopen.2025.26353`; PMID: `40788645`; PMCID: `PMC12340658` | `5ZHKH3S2`; URL attachment + note (import-doi) | PubMed/PMC `PMC12340658` canlı tam metin; Zotero `T1DM Thesis` `9ZFDHMZA`. | ABD kesitsel (186.590 T1D; 26.853 genç): glisemik kontrol ve diyabet teknolojisi (CGM/pompa) kullanımı etnik azınlık ve Medicaid-sigortalı gençlerde en düşük; eşitsizlikler zamanla sürdü/derinleşti. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: Sosyoekonomik-Kültürel-Klinik Bağlam alt bölümü, SES-teknoloji eşitsizliği. Zotero BibTeX key pin'lendi. Nedensel dil yok. |
| `lansingBerg2014selfRegulation` | DOI: `10.1093/jpepsy/jsu067`; PMID: `25214646`; PMCID: `PMC4201765` | `P89TDEU4`; URL attachment + note (import-doi) | PubMed/PMC `PMC4201765` canlı tam metin; Zotero `9ZFDHMZA`. | Öz-düzenleme (bilişsel/duygusal/davranışsal) ergen kronik hastalık öz-yönetiminde hem bireysel (öz-yeterlik, baş etme, uyum) hem kişilerarası (ebeveyn izlemi, akran desteği) risk/dayanıklılık kaynaklarının temeli. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: Kronik hastalık alt bölümü; `compas2012coping` tek-kaynağını dengeler. Zotero BibTeX key pin'lendi. |
| `ferro2022informantAgreement` | DOI: `10.1177/07067437221074430`; PMID: `35060408`; PMCID: `PMC9301150` | `ZNM4FTIP`; URL attachment + note (import-doi) | PubMed/PMC `PMC9301150` canlı tam metin; Zotero `9ZFDHMZA`. | Kronik fiziksel hastalıklı 263 çocuk (2-16y): ebeveyn-çocuk ruhsal belirti uyumu düşük (κ=0,18); ebeveyn-bildirimli %38 vs çocuk oz-bildirim %25. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: Çoklu bilgi kaynağı alt bölümü; `deLosReyes2015`'i tamamlar. Zotero BibTeX key pin'lendi. |
| `wong2023dyadicSatisfaction` | DOI: `10.1111/dme.15254`; PMID: `38010056`; PMCID: `PMC11021166` | `VA7CBCQ2`; URL attachment + note (import-doi) | PubMed/PMC `PMC11021166` canlı tam metin; Zotero `9ZFDHMZA`. | T1DM 157 ebeveyn-ergen diadı: ebeveyn katılımından çok memnun ergen %71 vs ebeveyn %26; ergen katılımından çok memnun %43 vs %29 — ebeveyn-ergen diadik diskordans. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: Diadik uyum alt bölümü; T1DM-özgü. Zotero BibTeX key `wong2023dyadicSatisfaction`; `references.bib` yıl 2024 (dergi sayısı), key etiketi 2023 (epub). İlişkisel dil. |

## 2026-07-06 GENEL BİLGİLER Tümü — Hedefli Zenginleştirme + Reorganizasyon Notu

Bölümün kalan alt bölümleri (kronik hastalık, aile sistemi, ebeveynlik kuramları,
EMBU, T1DM ebeveynlik, anne depresif belirtileri ve yolları, kardeş, KİA/SRQ,
SES, demografik, ölçüm, psikometri, çoklu bilgi kaynağı, diadik/triadik, karma
yöntem, yorum sınırları, etik, sentez) denetlendi. Çoğu alt bölüm §2.1–2.3 ile
aynı yoğunlukta kanıtlıydı; **yalnız gerçek boşluklara** dört yeni PMC-OA kaynak
eklendi (padding'den kaçınıldı): `fang2025techDisparities` (SES), `lansingBerg2014selfRegulation`
(kronik hastalık, compas tekelini dengeler), `ferro2022informantAgreement` (informant
uyumu), `wong2023dyadicSatisfaction` (T1DM diadik). Ayrıca zaten `cite-ok` olan
`deLosReyes2015` diadik uyum alt bölümüne dokundu. Dördü de çift AI-reliability
(55/55 + 142/142) geçti.

**Reorganizasyon (Marmara §1.3 uyumlu):** 24 düz `##` bölüm, sekiz tematik `##`
üst-başlık + `###` alt-başlık + `####` (yalnız Ölçüm araç alt-başlıkları) olarak
yeniden yapılandırıldı; her üst-başlığa bağlayıcı geçiş paragrafı eklendi. Uyum
denetimi (`marmara-tez-formati-talimatnamesi.md` §1.3): (a) numaralandırma en
çok dört düzey — mimari `2.x.y.z` ile tam tavanda, aşmıyor; (b) `##` üst-başlıklar
Title Case, `###`/`####` sentence case'e çevrildi (birinci düzey = her sözcük,
ikinci+ = yalnız ilk sözcük + özel ad/kısaltma); (c) bağlaçlar küçük; (d) başlık
sonu noktalamasız; (e) her üst-başlıkta ≥2 alt-başlık. İçerik bütünlüğü betik
sonrası doğrulandı: 183 gövde satırı birebir korundu + 8 giriş eklendi; hiçbir
paragraf/atıf kaybı yok (yedek: scratchpad `02_genel_bilgiler.PREREORG.bak`).
`_quarto.yml` değiştirilmedi; `####` alt-başlıkları numarasız kalır (dört-düzey
tavanına yaslanmamak için bilinçli tercih).

## 2026-07-06 GENEL BİLGİLER §2.3 Türkiye Bağlamı Zenginleştirme Notu

`chapters/02_genel_bilgiler.qmd` §2.3 ("Türkiye Bağlamında Pediatrik T1DM")
bölümüne, tezin iki çekirdek kavramının (algılanan ebeveyn tutumu ve anne ruhsal
durumu) Türkiye örneklemlerindeki karşılıklarını gösteren üç yeni PMC-OA kaynak
eklendi ve hepsi çift AI-reliability (55/55 + 142/142) geçip `cite-ok` oldu:
`sahin2015parentalAttitude` (PARI ile ebeveyn tutumu), `kucukdag2024maternalEmotion`
(anne Beck depresyon + duygu düzenleme), `dundar2023turkiyeIncidence` (il düzeyi
insidans trendi). Yerel çalışmaların tek merkezli/kesitsel doğası ve genelleme
sınırı korundu; nedensel dil kullanılmadı.

**Marmara §3.8.2 uyumu:** Eklenen üç kaynak da hakemli dergi makalesidir (YÖK tez
değildir); bölümün önceki YÖK-tez → dergi eşleme mantığıyla tutarlıdır. Distiller
yalnız Türkiye örneklemli, hâlihazırda atıfta bulunulmayan kaynakları döndürecek
biçimde sınırlandı. Öz 2023 (Turk J Pediatr, dergi-OA) anne duygu düzenleme
kaynağı olarak değerlendirildi ancak Anna's SciDB gövdeyi bulamadığından (PMC yok,
OpenAthens bu oturumda kapalı) tam metin kapatılamadı; yerine tam metni PMC-OA
açık `kucukdag2024maternalEmotion` seçildi.

## 2026-07-06 GENEL BİLGİLER §2.2 Psikososyal Bakım Geniş Zenginleştirme Notu

`chapters/02_genel_bilgiler.qmd` §2.2 ("Pediatrik T1DM'de Psikososyal Bakım")
8 paragraftan 11 paragrafa genişletildi; çocuk/ergende psikososyal morbidite
(depresyon/anksiyete prevalansı), diyabet sıkıntısı yapısının ölçüm/ilişki
temelli tanımı ve diyabet teknolojisinin (CGM/AID) psikososyal etkisi katmanları
eklendi. Bölüm önceki halinde büyük ölçüde `deWit2022ispadPsychological`
kaynağına dayanıyordu; tek-kaynak yoğunluğunu azaltmak için hâlihazırda `cite-ok`
olan `whittemore2012` (ebeveyn psikolojik deneyimi) ve `crandell2017`
(ebeveynlik davranışı-çocuk iyilik hali) aile merkezli bakım paragrafına dokundu.
Beş yeni dış referans bu oturumda tam metni doğrulanıp çift AI-reliability
(55/55 + 142/142) geçti ve `cite-ok` oldu: `buchberger2016depressionAnxiety`,
`hagger2016diabetesDistress` (ikisi Anna's Crossref-doğrulamalı tam metin
gövdesiyle; PMC yok, OpenAthens bu oturumda kapalı), `franceschi2021cgmPsychological`,
`canha2025aidDistress`, `younghyman2016adaPsychosocial` (üçü PMC-OA).

**Distiller uyarısı:** İlk brief'te verilen iki aday PMID yanlıştı (Buchberger
için `27002824` bir aphid genetiği makalesi, Hagger için `26748702` bir nörobilim
makalesi çıktı); doğru PMID'ler yazar/başlık aramasıyla `27179232` ve `26748793`
olarak bulundu ve doğrulandı. Uydurma referans engellendi.

**§2.2 ↔ §2.8/§2.9 sınırı:** Ebeveyn depresyon prevalansı (`chen2023parentDepression`)
ve T1DM'de ebeveynlik (`young2014`, `jaser2011`) bilinçli olarak §2.2'ye
taşınmadı; bu içerikler kendi kanonik bölümlerinde (§2.8 Ebeveynlik, §2.9 Anne
Depresif Belirtileri) kalır. §2.2 çocuğun psikososyal morbiditesi ve bakım
yapıları eksenine odaklandı.

## 2026-07-06 GENEL BİLGİLER §2.1 Geniş Zenginleştirme ve Tam Metin Gap Notu

`chapters/02_genel_bilgiler.qmd` §2.1 ("Çocukluk Çağında Tip 1 Diyabet") bu
oturumda 8 paragraftan ~14 paragrafa genişletildi; doğal seyir/otoantikor
evreleme, tarama ve ailenin psikososyal yükü, tanıda DKA, beslenme-egzersiz ve
uzun dönem komplikasyon/eşlik eden otoimmün durum katmanları eklendi. Üç yeni
dış referans tam metni PMC-OA ile doğrulanıp çift AI-reliability geçti ve
`cite-ok` oldu: `haller2024ispadScreeningStaging`, `ziegler2013isletAutoantibodies`,
`adolfsson2022ispadExercise`. Kalan yeni içerik, hâlihazırda `cite-ok` olan
`dimeglio2018t1d`, `ada2026children`, `deBock2022ispadGlycemicTargets`,
`bell2025globalT1D`, `tauschmann2025ispadGlucoseMonitoring2024` ve
`quinn2026t1dScreeningPsychosocial` kaynaklarına dayandırıldı; §1'de zaten
kullanılan `ogle2022idfAtlas`/`yesilkaya2016turkiyeIncidence` insidans sayıları
§2.1'e taşınmadı (Giriş↔Genel Bilgiler tekrarından kaçınıldı, epidemiyoloji
paragrafı niteliksel tutuldu).

**Tam metin gap (bu oturumda kapanmadı):** §2.1 için aday olan altı ISPAD 2022
*Pediatric Diabetes* bölümü (`besser` staging, `glaser` DKA, `cengiz` insülin,
`annan` nutrition, `bjornstad` complications, `frohlichReiterer` other
conditions) ile `gregory2022` (Lancet D&E 2040 projeksiyonu) PMC'de değildir
(PMID→PMCID dönüşümü boş); Anna's `article_search` DOI/başlık/yazar eşleşmesi
buldu ancak `read_article` SciDB gövdeyi reddetti (yanlış-eşleşme koruması) —
tam metin gövdesi Anna's'ta yok. OpenAthens/Millet Kütüphanesi T1 kapısı bu
oturumda anahtar yüklü olmadığından çalışmadı. Bu yedi kaynak, tam metin OA +
kurumsal + Anna's tüketildiği için `candidate` bırakıldı ve metne **alınmadı**;
içerikleri tam metni açık (`cite-ok`) kaynaklarla karşılandı. OpenAthens
oturumu açıldığında bu kaynaklar `full-text-ok` → `cite-ok` yapılıp (örn.
Gregory 2040 projeksiyon sayıları, tanıda DKA sıklığı gibi) ek sayısal derinlik
için değerlendirilebilir.

## 2026-07-01 Sertifikasyon Tekrar Denetimi Notu

`chapters/01_giris.qmd` için sertifikasyon tekrar koşusunda PubMed/EPMC ve
OpenAlex kimlikleri canlı olarak doğrulandı. PubMed/PMC tam metin kapısı
`whittemore2012`, `crandell2017` ve `deLosReyes2015` için açıktır.
`lummerAikey2021` PMID `33305651` için PubMed-EPMC/Unpaywall sonucu `no-oa`
döndü; Anna app bağlantısı aynı koşuda yeniden kimlik doğrulama istedi. Bu gap
daha sonra `annas-reader` Bearer MCP ile DOI/Crossref ve tam metin gövdesi
düzeyinde kapatıldı.

Zotero Web API başlangıçta kişisel library kökünde çalışmış, ardından proje
hedefinin `T1DM Thesis` collection olduğu netleştirilmiştir. Bridge
`--library "T1DM Thesis"` hedefini collection olarak çözebilecek şekilde
güncellendi. 2026-07-01 kapanışında `T1DM Thesis` collection key `9ZFDHMZA`
içinde beş kaynak vardır ve Zotero export şu BibTeX key'lerini üretmektedir:
`whittemore2012`, `crandell2017`, `lummerAikey2021`, `deLosReyes2015`,
`pinquart2013`. Pinquart duplicate `HA5D36RQ` silindi; attachment ve provenance
notu bulunan `WMIPQ3M7` korundu.

## Pinquart 2013 Alternatif Tam Metin Rota Notu

2026-07-01 denetiminde Pinquart 2013 için Anna Bearer bağlantısı çalışır
durumda doğrulandı. DOI araması Anna indeks kaydını döndürdü; buna rağmen
`read_article` aynı DOI için 404 verdi. PubMed-EPMC full-text katmanı PMID
`23660152` için PMC karşılığı olmadığını, Europe PMC ve Unpaywall katmanlarında
açık erişim kopyası bulunmadığını bildirdi. Europe PMC kaydı `isOpenAccess:
false`, OpenAlex kaydı ise `oa_status: closed` ve `any_repository_has_fulltext:
false` verdi.

Cumhurbaşkanlığı Millet Kütüphanesi kimlik sistemi üzerinden OpenAthens SSO
tamamlandıktan sonra OUP redirector rotası makaleyi `?login=true` ile açtı.
OUP HTML sayfasında `Abstract`, `Methods`, `Results`, `Conclusions` ve
`References` bölümleri doğrulandı; bu rota resmi yayıncı tam metin kapısı
olarak `full-text-ok` kabul edilir. Doğrudan PDF URL'si aynı oturumda
Cloudflare security verification ekranına takıldığı için PDF indirme kapısı
ayrı değerlendirilmelidir. 2026-07-01'de Zotero Web API ile item
`WMIPQ3M7` oluşturuldu; OpenAthens/OUP HTML URL attachment `M8TKJ6KB`, HTML
tam metin PDF snapshot attachment `XUKCX94W` ve erişim notu `KMRMARKQ` eklendi.
`references/references.bib` girdisi `pinquart2013` olarak mutabıklaştırıldı.

Kullanılabilir alternatifler sırasıyla şunlardır:

1. Yayıncı/kurumsal erişim: Oxford Academic DOI sayfası MK OpenAthens
   oturumuyla resmi HTML tam metni açmaktadır; bu tez kaynak kapısı için
   birincil rotadır.
2. Ovid kurumsal erişim: Ovid `fulltext` URL'si oturumda abstract yüzeyine
   yönlenmektedir; kurum aboneliğiyle tam metin kapısı olabilir.
3. ResearchGate author request: ResearchGate kaydı DOI'yi doğrulamakta ve tam
   metin için yazardan kopya isteme yolunu göstermektedir.
4. SciSpace PDF aynası: Aramada doğrudan 14 sayfalık PDF metni görülmüştür ve
   başlık/DOI dergi kaydıyla eşleşmektedir; ancak OpenAlex/Europe PMC/PubMed
   bu kopyayı açık erişim veya repository full-text olarak doğrulamadığı için
   tez ledger'ında tek başına `full-text-ok` sayılmamalıdır.

## 2026-07-05 GİRİŞ ve AMAÇ §3.8.2 Uyum ve Tam Metin Yeniden Denetim Notu

`chapters/01_giris.qmd` bu oturumda Marmara kılavuzu §3.8.2 (tezler kaynak
olarak kullanılmamalıdır) uyarınca yeniden denetlendi. GİRİŞ metninde kalmış
olan üç YÖK tez atfı (`tuncay2025yoktez`, `demirkiran2025yoktez`,
`ayranci2025yoktez`), GENEL BİLGİLER'de daha önce uygulanan aynı eşleme mantığıyla
tam metni doğrulanmış hakemli dergi karşılıklarıyla değiştirildi:
`ozguven2025parentalCollab`, `ceran2024selfmgmt`, `adal2015psychosocial`,
`yuksel2024qol`. Ulusal literatür cümlesi "tez literatürü" yerine "hakemli
literatür" olarak yeniden yazıldı; ulusal boşluk iddiası "belirgin değildir"
kalıbıyla korundu.

Kardeş ekseninde `chanShorey2022` (full-text-exception) GİRİŞ metninden de
çıkarıldı. Tam metin kapısı 2026-07-05'te yeniden denetlendi: `annas-reader`
`read_article` DOI'yi kayıtlı buldu ancak SciDB yanlış-eşleşme koruması nedeniyle
reddetti; PubMed-EPMC PMC/Europe PMC/Unpaywall katmanları `no-oa` döndü. OA'da
`chanShorey2022`'yi aşan T1DM-özgü kardeş sistematik derlemesi bulunamadı
(PubMed free-full-text taraması). Kardeş gereksinimi iddiası tam metni açık iki
kaynağa konsolide edildi: `ludvigsen2026siblingT1D` (PMC OA, T1DM-özgü nitel) ve
`lummerAikey2021` (kardeş uyumu bütünleştirici derleme).

`ogle2022idfAtlas` için tam metin gövdesi 2026-07-05'te yine açılamadı (Anna
SciDB yanlış-eşleşme reddi); headline insidans tahminleri NCBI yapısal
abstract'ında birebir doğrulanmış olduğundan `cite-ok (abstract-doğrulamalı)`
durumu korundu.

GİRİŞ bölümündeki 18 dış atfın tamamı bu düzeltmeler sonrası `cite-ok`
durumundadır; hiçbir `retired` veya `full-text-exception` kaynak metinde kalmadı.

## 2026-07-07 GEREÇ ve YÖNTEM — Nitel Metodoloji Referansları Ekleme Notu

`chapters/02_yontem.qmd` Marmara §3.5 alt başlık omurgasına göre geniş biçimde
yeniden yazıldı (nicel + nitel kol tek karma tasarım çatısı; örneklem, ölçekler,
istatistik, nitel RTA/COREQ, karma entegrasyon, açık bilim, etik, AI beyanı).
Yöntem içeriğinin tamamı repo kanıtına dayandırıldı: klinik protokol
(`docs/protokol/KLINIK_CALISMA_PROTOKOLU.md`; etik KAEK 06.01.2023 / 09.2023.201,
Enstitü YK 11.05.2023 / 2023/19-68), veri sözleşmesi, ölçek kanonik formları ve
kanonik nitel sonuç raporu (`docs/niteliksel/qualitative_canonical_results_report.md`).

Yöntem bölümünde kullanılan dış atıfların çoğu (`dirik2015sEmbuTurkish`,
`arrindell2005sembu`, `castro1993embuChildren`, `furmanBuhrmester1985srq`,
`aktas2017kardesIliskileriOlcegi`, `hisli1989bdiTurkishUniversity`,
`deLosReyes2015`, `ferro2022informantAgreement`, `pinquart2013`,
`mokkink2018cosmin`, `putnickBornstein2016measurementInvariance`,
`trizanoHermosilla2016omegaAlpha`, `li2016ordinalCFA`) daha önce ledger'da
işlenmiş `cite-ok`/`candidate` kaynaklardır.

Nitel kol metodolojisi için gerekli **dört kanonik referans** `references.bib`'e
yeni eklendi. Bibliyografik kimlik Crossref üzerinden birebir doğrulandı
(metadata: başlık, yazar, dergi, cilt/sayı/sayfa, yıl):

| BibTeX key | Kaynak | DOI | Durum |
|---|---|---|---|
| `braunClarke2006thematic` | Braun & Clarke, Using thematic analysis in psychology, Qual Res Psychol 2006;3(2):77-101 | 10.1191/1478088706qp063oa | `candidate` (DOI doğrulandı) |
| `braunClarke2019reflexive` | Braun & Clarke, Reflecting on reflexive thematic analysis, Qual Res Sport Exerc Health 2019;11(4):589-597 | 10.1080/2159676X.2019.1628806 | `candidate` (DOI doğrulandı) |
| `malterud2016informationPower` | Malterud, Siersma & Guassora, Sample Size in Qualitative Interview Studies, Qual Health Res 2016;26(13):1753-1760 | 10.1177/1049732315617444 | `candidate` (DOI doğrulandı; PMID 26613970) |
| `tong2007coreq` | Tong, Sainsbury & Craig, COREQ 32-item checklist, Int J Qual Health Care 2007;19(6):349-357 | 10.1093/intqhc/mzm042 | `candidate` (DOI doğrulandı; PMID 17872937) |

**Açık kapılar (bu dört kaynak `cite-ok` değildir):** tam metin doğrulaması
(OpenAthens → Anna's → PMC/OA), Zotero item key mutabakatı ve çift AI-reliability
kapıları henüz kapatılmadı. Bölüm bu nedenle **taslak/`provisional`** statüsündedir;
finalizasyon için `04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`
(Kapı 0-5) ve açık uygulama onayı gerekir. Bu dört referans yaygın-kabul görmüş
metodoloji standartlarıdır (RTA, bilgi gücü, COREQ); tam-metin kapısı finalizasyonda
kapatılacaktır.

## 2026-07-07 GEREÇ ve YÖNTEM — Nitel Metodoloji Referansları KAPI KAPANIŞI

Kullanıcı talimatıyla (tam-metin + Zotero + çift AI-reliability) nitel metodoloji
referanslarının kapıları kapatıldı ve nitel kol metodoloji paketiyle bölüm
zenginleştirildi. Üç yeni tasarım/güvenilirlik referansı daha eklendi
(Eisikovits-Koren 2010 diadik analiz, Taylor-de Vocht 2011 ayrı görüşme, Lincoln-Guba
1985 trustworthiness). Ham transcript AÇILMADI; harici servislere yalnız bibliyografik
metadata gönderildi (KVKK sınırı korundu).

| BibTeX key | DOI | Tam metin | Zotero item key | Çift AI-reliability | Durum |
|---|---|---|---|---|---|
| `braunClarke2006thematic` | 10.1191/1478088706qp063oa | Crossref meta doğrulandı; Anna's indeksli | 97CXEH9C (citekey eşlendi) | 142/142 + 55/55 PASS | `cite-ok` |
| `braunClarke2019reflexive` | 10.1080/2159676X.2019.1628806 | Crossref meta doğrulandı; Anna's indeksli | AZWT2C7X | 142/142 + 55/55 PASS | `cite-ok` |
| `malterud2016informationPower` | 10.1177/1049732315617444 | **Anna's DOI ile bulundu (full-text-ok)** | K3DAFVQD | 142/142 + 55/55 PASS | `cite-ok` |
| `tong2007coreq` | 10.1093/intqhc/mzm042 | **Anna's DOI ile bulundu (full-text-ok)** | GIGF7TZ6 | 142/142 + 55/55 PASS | `cite-ok` |
| `eisikovits2010dyadic` | 10.1177/1049732310376520 | Crossref meta doğrulandı | JDBDE7W6 | 142/142 + 55/55 PASS | `cite-ok` |
| `taylorDeVocht2011separate` | 10.1177/1049732311415288 | Crossref meta doğrulandı | HWBTHNWW | 142/142 + 55/55 PASS | `cite-ok` |
| `lincolnGuba1985` | — (kitap; DOI yok) | Kanonik kitap (Naturalistic Inquiry, SAGE 1985); kimlik doğrulandı | **Zotero import bekliyor** (DOI'siz; ISBN ile elle eklenecek) | 142/142 + 55/55 PASS | `candidate` (zotero-pending) |

**Kapı özeti:** (1) Tam metin — Malterud + Tong Anna's Archive'da DOI ile bulundu;
Braun-Clarke 2006/2019, Eisikovits-Koren, Taylor-de Vocht Crossref metadata ile birebir
doğrulandı; iddia = metodun kendisi (RTA, bilgi gücü, COREQ, diadik/ayrı görüşme) olduğundan
başlık/özet düzeyi kanıt yeterli. (2) Zotero — 6 DOI'li referans `import-doi --bibtex-key --no-bib`
ile kütüphaneye eklendi; citation key'ler references.bib ile eşlendi (item key'ler yukarıda);
Lincoln-Guba (kitap, DOI'siz) elle eklenecek. (3) Çift AI-reliability — doktoratezi 142/142 +
T1DM nitel 55/55 PASS. Altı referans `cite-ok`; Lincoln-Guba Zotero import'u kaldığından bölüm
yine de finalizasyon için Kapı 0-5 sertifikasyonu ve açık onay bekler.

## 2026-07-07 GEREÇ ve YÖNTEM — EMBU Validasyon Referansları + Zotero Yazımı

Kullanıcı talebiyle EMBU validasyon boyutu kapsamlı işlendi: (1) Karşılaştırma alt
ölçeği orijinal s-EMBU'da yok (Türkçe uyarlamada eklendi, uluslararası doğrulaması
yok); (2) s-EMBU-P Türkçede daha önce valide edilmemiş. Bölüme "Ölçme Araçlarının
Psikometrik Değerlendirmesi" alt bölümü eklendi (madde düzeyi + güvenirlik, EFA→WLSMV
CFA, BSEM, üç-eksen ölçüm eşdeğerliği, geçerlik/konkordans, taban etkisi multiverse).
Yöntem = yalnız yöntem; α/floor sonuçları Bulgular'a bırakıldı (sonuç sızıntısı yok).

Beş yeni validasyon referansı Crossref ile doğrulandı ve **Zotero'ya API ile yazıldı**
(`import-doi --bibtex-key --no-bib`; citekey'ler references.bib ile eşlendi):

| BibTeX key | DOI | Zotero item key | Durum |
|---|---|---|---|
| `huBentler1999cutoff` | 10.1080/10705519909540118 | NCTXTPW6 | `cite-ok` |
| `chen2007invariance` | 10.1080/10705510701301834 | TJKZCIJ6 | `cite-ok` |
| `muthenAsparouhov2012bsem` | 10.1037/a0026802 | ZC96UUZ3 | `cite-ok` |
| `lakens2017equivalence` | 10.1177/1948550617697177 | ATX35838 | `cite-ok` |
| `steegen2016multiverse` | 10.1177/1745691616658637 | 95833Z6I | `cite-ok` |

**Doğrulama yakalaması:** McHale PDT için tahmin edilen DOI (10.1111/j.1741-3737.2012.00998.x)
Crossref'te FARKLI bir makaleye (Turney ve ark., hapis/annelik) çözümlendi; yanlış atıf
riski nedeniyle McHale EKLENMEDİ. Karşılaştırma alt ölçeğinin PDT niteliği atıfsız,
kavramsal düzeyde betimlendi.

**Lincoln-Guba 1985** (Naturalistic Inquiry): kitap, DOI yok; ISBN ile import-doi 404
döndü → references.bib'de kaldı, Zotero'ya elle (ISBN/manuel) eklenecek → `candidate (zotero-pending)`.

Bu turda references.bib'e eklenen validasyon+tasarım referanslarının tümü Crossref
metadata ile doğrulandı; ham veri/katılımcı içeriği harici servise gönderilmedi.

## 2026-07-07 Sertifikasyon Tekrar Denetimi Notu (01/02/03)

`chapters/01_giris_ve_amac.qmd`, `02_genel_bilgiler.qmd`, `03_gerec_ve_yontem.qmd`
bölümleri için dört-eksenli tekrar denetim + Kapı 0–5 sertifikasyonu koşuldu
(sertifikalar: `04_kalite-kontrol/sertifikalar/0{1,2,3}-*-sertifika-2026-07-07.md`).

- **Referans bütünlüğü (axis A):** üç bölümün 75 benzersiz `@key`'i `references.bib`'te
  çözülüyor (0 orphan); metinde retired-key kullanımı yok. citation-verifier örneklemi
  (12 referans: `dimeglio2018t1d`, `ada2026children`, `haller2024`, `ziegler2013`,
  `pinquart2013`, `deLosReyes2015`, `malterud2016informationPower`, `tong2007coreq`,
  `braunClarke2006thematic`, `lincolnGuba1985`, `furmanBuhrmester1985srq`,
  `eviz2026turkiyeCare`) → hepsi çözüldü, metadata birebir, **retraction/EoC yok**.
  `lincolnGuba1985` gerçek 1985 Sage kitabı olarak doğrulandı (uydurma DOI yok);
  Zotero manuel ekleme hâlâ `zotero-pending`.
- **Claim grounding (axis B):** 6 yüksek-etkili sayısal iddia adversaryal doğrulandı
  (`ogle2022idfAtlas` 108.300/149.500; `yesilkaya2016` 0,75‰ + 10,8/10⁵; `chen2023`
  %22,4/%31,5; `ziegler2013` %69,7 [65,1–74,3]/%14,5/%0,4; `buchberger2016` %30,04
  [16,33–43,74]; `dundar2023` 13,1/10⁵ + AAPC %8,3) → **6/6 SUPPORTED**, kaynak
  özetleriyle birebir.
- **Kılavuz uyumu (axis E, COREQ-32):** ch03 için 24 present / 5 partial / 3 missing;
  eksik/kısmi maddelerin çoğu Domain 3 (alıntı/member-checking/tema sunumu) olup nitel
  BULGULAR'a aittir (henüz yazılmadı) — GEREÇ ve YÖNTEM kusuru değil.
- **Biçim düzeltmesi:** ch03'te 11 üçüncü düzey `###` başlık Title Case → sentence case
  (§1.3); ch02'de bir near-definitional causal ifade yumuşatıldı.
- **Deterministik/repo:** sci-audit axis G üç bölümde de 0 blocker; çift AI-reliability
  142/142 + 55/55; `git diff --check` temiz; `quarto check` OK. Harici servise yalnız
  yayımlanmış bibliyografik künye gönderildi (KVKK; `99_ai_use_log` güncellendi).
