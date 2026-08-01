# Referans Denetim Ledgeri

Bu ledger, tez metnine girecek her dış referans için bibliyografik kimlik,
tam metin kanıtı, Zotero mutabakatı, claim/pasaj izi ve iki-kol
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

`bib_hygiene reconcile` otomatik ön-mutabakat (HARD undefined = blok) →
bağlam (anonim/türetilmiş) → bibliyografik kimlik (DOI/PMID/PMCID/OpenAlex/YÖK)
→ tam metin (OpenAthens → Anna's → PMC/OA → Zotero attachment) → Zotero
mutabakatı (item key ≠ BibTeX key; `references/references.bib` export) →
claim/pasaj notu → iki-kol AI-reliability (`t1dm-qual-ai-audit` +
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
| `reliability-ok` | Zotero item key, BibTeX key ve `references/references.bib` mutabık. |
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
| `whittemore2012` | DOI: `10.1177/0145721712445216`; PMID: `22581804`; PMCID: `PMC3401246` | `F2JMM3VP`; URL attachment `XHZ52THA`; note `FGM3VEAJ` | PubMed/PMC `PMC3401246` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | T1DM ebeveynlerinde günlük bakım sorumluluğu, aile rutini değişimi, psikolojik sıkıntı ve çocuk/aile sonuçlarıyla ilişki; ayrıca çoklu bilgi verici T1DM aile araştırma geleneği (GEREÇ ve YÖNTEM nitel desen gerekçesi). | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `whittemore2012` olarak pin'lendi. 2026-07-13: ch03 §Nitel Kol kullanımı Bölüm sütununa yansıtıldı. |
| `crandell2017` | DOI: `10.1037/fsh0000305`; PMID: `29172624`; PMCID: `PMC5880719` | `BZPDC2SR`; URL attachment `IQMHF6WI`; note `8NSZ5CVQ` | PubMed/PMC `PMC5880719` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Kronik fiziksel hastalığı olan çocuklarda ebeveynlik boyutları ile çocuk iyilik hali arasındaki ilişki. | `GİRİŞ ve AMAÇ, GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `crandell2017` olarak pin'lendi; dergi yayın yılı 2018, tez citation key'i korunur. |
| `lummerAikey2021` | DOI: `10.1177/1074840720977177`; PMID: `33305651`; Semantic Scholar `a8f0eb4d4f4ba866a618958a8dc6ea7e73c336a3` | `JWHTB4R6`; URL attachment `4RUITFXZ`; note `SCPVNQQA` | Anna `annas-reader` Bearer MCP `article_search` ve `read_article` DOI/Crossref eşleşmesi; PubMed-EPMC/Unpaywall `no-oa`; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Kronik hastalık bağlamında sağlıklı kardeş uyumu; deneyim, psikososyal uyum, baş etme ve iletişim temaları. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER`, `TARTIŞMA` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `lummerAikey2021` olarak pin'lendi. |
| `deLosReyes2015` | DOI: `10.1037/a0038498`; PMID: `25915035`; PMCID: `PMC4486608`; Semantic Scholar `5e3385e32737b4234e1f892f936066c4de07e6d2` | `MIDTPNQH`; URL attachment `HKPRVBFM`; note `WP8K48UM` | PubMed/PMC `PMC4486608` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Çoklu bilgi kaynağı yaklaşımında düşük-orta örtüşmenin bağlama/role özgü bilgi olarak yorumlanabilmesi. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `deLosReyes2015` olarak pin'lendi. |
| `pinquart2013` | DOI: `10.1093/jpepsy/jst020`; PMID: `23660152`; OpenAlex `W2156083233` | `WMIPQ3M7`; attachment `XUKCX94W`; URL attachment `M8TKJ6KB`; notes `KMRMARKQ`, `DRA4G9N5` | MK OpenAthens -> OUP resmi HTML tam metin erişimi doğrulandı; Zotero'ya HTML tam metin snapshot PDF'i ve yayıncı URL'si eklendi; Zotero `T1DM Thesis` collection `9ZFDHMZA`. Anna `article_search` DOI kimliğini buldu, ancak eski `read_article` denemesi 404; PubMed-EPMC `no-oa`; PDF uç noktası Cloudflare doğrulamasına takıldı. | Kronik fiziksel hastalık bağlamında ebeveyn-çocuk ilişkisi, sıcaklık/duyarlılık, kontrol ve aşırı koruyuculuk farklarına ilişkin meta-analitik kanıt; ayrıca GEREÇ ve YÖNTEM Bayesçi paralel hatta zayıf bilgi verici önsel dayanağı. | `GİRİŞ ve AMAÇ, GENEL BİLGİLER, TARTIŞMA, GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `pinquart2013` olarak pin'lendi; duplicate `HA5D36RQ` sürüm korumalı Web API delete ile kaldırıldı. OUP HTML snapshot yayıncı PDF'i değildir. 2026-07-02 giriş zenginleştirme koşusunda iki-kol AI-reliability geçti; citation `chapters/01_giris.qmd` metnine alındı. 2026-07-13: ch03 §Bayesçi paralel hat kullanımı Bölüm sütununa yansıtıldı. |
| `sharpe2002siblings` | DOI: `10.1093/jpepsy/27.8.699`; PMID: `12403860` | `references.bib` künyesi mevcut; Zotero pin bekliyor | Anna `read_article` 404; PubMed özet düzeyi görüldü, tam metin bu turda kapanmadı. | Kronik hastalığı olan çocukların kardeşlerine ilişkin heterojen genel meta-analitik arka plan; T1DM'e özgü kesin etki zemini değil. CSR'de yalnız özet-düzeyli/bağlamsal dayanak (H2 §11.2, Tartışma §19.2) — bu çalışmaya özgü kardeş sonucu için tam-metin dış iddia üretilmedi. | `GİRİŞ ve AMAÇ, TARTIŞMA` | not-run | not-run | `full-text-exception` | Kardeş ekseninin tam metni doğrulanan birincil dayanağı `lummerAikey2021`'dir; `sharpe2002siblings` yalnız bağlamsal genel arka plan olarak korunur. Tam-metin rotası yeniden denenecek. |
| `ada2026children` | DOI: `10.2337/dc26-S014`; PMID: `41358890`; PMCID: `PMC12690182` | `5JM3EIX6`; URL attachment `GNHSM4PA`; note `W7QKQCCS` | PubMed/PMC `PMC12690182` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Pediatrik T1DM bakımında gelişimsel, aile katılımlı ve psikososyal bağlama duyarlı bakım çerçevesi. CSR'de güncel standart arka planı olarak anılır; özgül öneri ayrıntıları ISPAD 2022 + ADA 2016 üzerinden kurulur (editoryal tercih, tam metin engeli değil). | `GENEL BİLGİLER, TARTIŞMA` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `ada2026children` olarak pin'lendi. Tam metin doğrulandığı için CSR'deki "tam metin tamamlanmadı" ifadesi 2026-07-12 turunda ledger gerçeğiyle hizalandı. |
| `lovejoy2000maternal` | DOI: `10.1016/S0272-7358(98)00100-7`; PMID: `10860167` | `references.bib` künyesi mevcut; Zotero pin bekliyor | PubMed özet düzeyi görüldü; tam metin bu turda kapanmadı. | Anne depresyonu ile ebeveynlik davranışı arasındaki meta-analitik ilişki (olumsuz ebeveynlik d = 0,40); H4 SEM yol katsayılarının yön/büyüklük kalibrasyonu. CSR'de (§ H4, Tartışma §19.2) yalnız özet-düzeyli yön/büyüklük dayanağı — moderatör/alt-grup/tablo iddiası türetilmedi. | `GENEL BİLGİLER, TARTIŞMA` | not-run | not-run | `full-text-exception` | Yön/büyüklük kalibrasyonuyla sınırlı bağlamsal kullanım; tam-metin rotası yeniden denenecek, kapanınca `cite-ok`'a yükseltilecek. |
| `deWit2022ispadPsychological` | DOI: `10.1111/pedi.13428`; PMID: `36464988`; PMCID: `PMC10107478` | `6H8NHHZ9`; URL attachment `IXEP5QDQ`; note `JPEBAGX7` | PubMed/PMC `PMC10107478` canlı tam metin; ISPAD Chapter 15 resmi sayfası 2024 güncel yüzey olarak ayrıca doğrulandı; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Psikososyal tarama, bakım veren iyilik hali, aile işlevselliği, ebeveyn katılımı, özerklik desteği, iletişim ve teknoloji yükü. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `deWit2022ispadPsychological` olarak pin'lendi. |
| `eviz2026turkiyeCare` | DOI: `10.4274/jcrpe.galenos.2025.2025-1-7`; PMID: `41090400`; PMCID: `PMC12989894` | `DZD64HM5`; URL attachment `PQH8T3GG`; note `9ERT4KZX` | PubMed/PMC `PMC12989894` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Türkiye'de pediatrik T1DM bakımında kapsamlı aile eğitimi, ekip çalışması, bireyselleştirilmiş plan, teknoloji kullanımı, ulusal veri sınırlılığı, çalışma döneminde sensör geri ödeme durumu ve sosyoekonomik aktarılabilirlik sınırı. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `eviz2026turkiyeCare` olarak pin'lendi. |
| `trojanowski2021` | DOI: `10.1093/jpepsy/jsab064`; PMID: `34657955`; OpenAlex `W3205701329` | `DWAU45FS`; URL attachment `DGX22ZRR`; note `AE9VPWMW` | MK OpenAthens login sonrası OUP resmi HTML tam metin sayfasında `Abstract`, `Materials and Methods`, `Risk of Bias`, `Results`, `Discussion`, `Clinical Implications` ve PDF linki görüldü. PubMed-EPMC/Unpaywall ve OpenAlex OA/repository `closed`; Anna `article_search` DOI eşleşti, `read_article` 404. | T1DM gençlerinde ebeveynlik, aile çatışması, eleştirel ebeveynlik, destek, katılım ve ilişki kalitesinin psikolojik sağlıkla ilişkisi. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `trojanowski2021` olarak pin'lendi; resmi HTML tam metin PDF yerine kabul edildi. 2026-07-05: GİRİŞ 2. paragrafta destekleyici/eleştirel ebeveynlik-diyabet distresi cümlesinde zaten kullanıldığı bölüm sütununa yansıtıldı. |
| `chen2023parentDepression` | DOI: `10.3389/fendo.2023.1095729`; PMID: `36936139`; PMCID: `PMC10014558` | `2NHFKRDE`; URL attachment `99UPRGDG`; note `DU7FUJ7H` | PubMed/PMC `PMC10014558` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Ebeveyn depresyon/depresif belirti prevalansı: genel %22,4; anneler %31,5; babalar %16,3; 12 yaş altı çocuk ebeveynleri %32,3; ergen ebeveynleri %16,0. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `chen2023parentDepression` olarak pin'lendi; klinik tanı değil öz-bildirim belirti alanı olarak kullanılacak. |
| `chanShorey2022` | DOI: `10.1016/j.pedn.2021.12.002`; PMID: `34929508`; OpenAlex `W4200560240` | `QIAE8E7K`; URL attachment `UWFJGJK2`; note `KDZEC4DJ` | OpenAthens/ScienceDirect denemesi headless/IP blok ekranında kaldı; resmi Journal of Pediatric Nursing PDF URL'si bulundu ancak Cloudflare otomatik erişimi engelledi; Anna `article_search` DOI eşleşti fakat `read_article` yanlış fuzzy match'i reddetti; NUS ScholarBank metadata var ancak `TEXT` bitstream `401 restricted`; Europe PMC `isOpenAccess: false`, OpenAlex `oa_status: closed`, `any_repository_has_fulltext: false`. | T1DM tanılı çocukların sağlıklı kardeşlerinin deneyim ve gereksinimleri için sistematik derleme adayı. | — (metinde kullanılmıyor) | 55/55 passed | 142/142 passed | `full-text-exception` | Metindeki ana citation yükü `ludvigsen2026siblingT1D` kaynağına kaydırıldı; Chan/Shorey manuel kurumsal erişim kapanana kadar final citation olarak kullanılmamalı. 2026-07-05: GİRİŞ kardeş paragrafından da çıkarıldı; kardeş bilgi/duygusal destek/görünürlük gereksinimi iddiası `ludvigsen2026siblingT1D` (T1DM-özgü nitel, PMC OA) + `lummerAikey2021` (kardeş uyumu bütünleştirici derleme) üzerine konsolide edildi. Anna `read_article` DOI kayıtlı ancak SciDB yanlış-eşleşme reddi; PubMed-EPMC/Unpaywall `no-oa` (2026-07-05 yeniden doğrulandı). |
| `ludvigsen2026siblingT1D` | DOI: `10.1177/26350106261442180`; PMID: `42159283`; PMCID: `PMC13219770`; OpenAlex `W7161753006` | `6HTRN4MF`; URL attachment `FXFWHKES`; note `STVW6DX5` | PubMed/PMC `PMC13219770` canlı tam metin; OpenAlex OA `hybrid`, license `cc-by`, repository full text var; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | T1DM tanılı çocuğun sağlıklı kardeşlerinde tanı döneminin zorluğu, aile atmosferi, dahil edilme isteği, günlük yaşam yükü, gece alarmı, ebeveyn yorgunluğu ve bilgi/destek gereksinimi. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `ludvigsen2026siblingT1D` olarak pin'lendi; `references.bib` girdisi temizlendi. |
| `mertensKrypotos2019preregExisting` | DOI: `10.5334/pb.493`; PMID: `31497308`; PMCID: `PMC6706998` | `references.bib` künyesi eklendi; Zotero item `KENXR2WZ` pin'lendi | PMC `PMC6706998` yapılandırılmış JATS tam metin (39.698 karakter) + Minerva Roche korpus vectorstore tam metin (41.326 karakter, `granted_rights` AI-inference izinli) `fulltext_cascade.py` ile doğrulandı; OpenAthens/annas denenmedi (PMC OA yeterli). | Mevcut/ikincil veriye dayalı çözümlemelerde araştırmacının örneklem büyüklüğü veya deneysel işlem gibi tasarım öğelerini değiştiremediği; ön-kaydın koruyucu işlevinin tasarımın değil analiz kararlarının veriye bakılmadan sabitlenmesine kayması (GEREÇ ve YÖNTEM §Açık Bilim, ikincil veri ön-kayıt şablonu dayanağı). | `GEREÇ ve YÖNTEM` | not-run | not-run | `cite-ok` | `/anlatim-zenginligi` 3.16 koşusunda eklendi. claim↔kaynak galileo embedding skoru 0,386 (cross-lingual TR↔EN, advisory). İçerik sadakati tam-metin argümanıyla teyit edildi; verbatim kopya yok (telif). Zotero item `KENXR2WZ` pin'lendi (DOI+fulltext-URL+provenance notu). |
| `bakker2020preregQuality` | DOI: `10.1371/journal.pbio.3000937`; PMID: `33296358`; PMCID: `PMC7725296` | `references.bib` künyesi eklendi; Zotero item `ZMSHFXGU` pin'lendi | PMC `PMC7725296` yapılandırılmış JATS tam metin (42.324 karakter) + Minerva Roche korpus vectorstore tam metin (83.154 karakter) `fulltext_cascade.py` ile doğrulandı; OpenAthens/annas denenmedi (PMC OA yeterli). | Araştırmacı serbestlik derecelerinin fırsatçı kullanımının yanlış-pozitif bulgu olasılığını ve etki büyüklüğü kestirimlerindeki iyimserliği artırması; ön-kaydın analiz kararlarını veriye bakılmadan sabitleyerek bunu kısıtlaması (GEREÇ ve YÖNTEM §Açık Bilim, doğrulayıcı/keşifsel ayrımı gerekçesi). | `GEREÇ ve YÖNTEM` | not-run | not-run | `cite-ok` | `/anlatim-zenginligi` 3.16 koşusunda eklendi. claim↔kaynak galileo embedding skoru 0,405 (cross-lingual TR↔EN, advisory). İçerik sadakati tam-metin argümanıyla teyit edildi; verbatim kopya yok (telif). Zotero item `ZMSHFXGU` pin'lendi (DOI+fulltext-URL+provenance notu). |
| `hesterMiner2024consentAssent` | DOI: `10.1016/j.pcl.2023.08.003`; PMID: `37973309` | `references.bib` künyesi eklendi; Zotero item `5MUQN8GI` pin'lendi | Minerva Roche korpus vectorstore tam metin (33.576 karakter, `granted_rights` AI-inference izinli) `fulltext_cascade.py` ile doğrulandı; PubMed DOI-exact eşleşme (PMID 37973309) ama PMC OA yok → Minerva meşru tam-metin kaynağı (annas öncesi, telif: verbatim kopya yok). | Küçüklerin kendi başına onam veremediği; pediatrik araştırmada standart korumanın ebeveyn izni + çocuğun gelişimsel düzeyine uygun muvafakati (assent) olduğu; muvafakatin çocuğun gelişen özerkliğine ve değerlerini ifade etmesine olanak tanıması; çocuk-ebeveyn anlaşmazlığında çocuğun reddine saygı (GEREÇ ve YÖNTEM §Etik, onam/muvafakat yapısı dayanağı). | `GEREÇ ve YÖNTEM` | not-run | not-run | `cite-ok` | `/anlatim-zenginligi` 3.17 koşusunda eklendi. claim↔kaynak galileo embedding skoru 0,546 (cross-lingual TR↔EN, advisory). İçerik sadakati tam-metin argümanıyla teyit edildi. Zotero item `5MUQN8GI` pin'lendi (DOI+fulltext-URL+provenance notu). |
| `joo2023deidentification` | DOI: `10.1016/j.giq.2023.101805` | `references.bib` künyesi eklendi; Zotero item `I25D7FQV` pin'lendi | Minerva Roche korpus vectorstore tam metin (55.705 karakter) `fulltext_cascade.py` ile doğrulandı; GIQ/Elsevier makalesi PubMed kapsamı dışı, DOI Crossref-geçerli; OpenAthens/annas denenmedi (Minerva yeterli). | Kimliksizleştirmenin ikili değil kimliklenebilirlik-spektrumu/risk-yönetimi perspektifiyle ele alınması; psödonimleştirilmiş verinin geri-bağlama anahtarı var oldukça kişisel veri niteliğini koruması (GEREÇ ve YÖNTEM §Etik, KVKK/GDPR psödonimleştirme≠anonimleştirme dayanağı). | `GEREÇ ve YÖNTEM` | not-run | not-run | `cite-ok` | `/anlatim-zenginligi` 3.17 koşusunda eklendi. claim↔kaynak galileo embedding skoru 0,484 (cross-lingual TR↔EN, advisory). İçerik sadakati tam-metin argümanıyla teyit edildi; verbatim kopya yok. Zotero item `I25D7FQV` pin'lendi (DOI+fulltext-URL+provenance notu). |
| `bell2023writeAlgorithm` | DOI: `10.1186/s12916-023-03039-7`; PMID: `37667296`; PMCID: `PMC10478332` | `references.bib` künyesi eklendi; Zotero item `XT243I4Q` pin'lendi | PMC `PMC10478332` yapılandırılmış JATS tam metin (12.674 karakter) + Minerva Roche korpus vectorstore (9.608 karakter) `fulltext_cascade.py` ile doğrulandı; makale numarası (334) ve künye Crossref ile teyit edildi. | Büyük dil modellerinin istatistiksel örüntüden ürettiği uydurma (hallucination) içerik ve alana özgü ince bilgide sınırlılık riski; akademik kullanımda sorumlu uygulama + şeffaf belgeleme gereği (GEREÇ ve YÖNTEM §Yapay Zekâ Destekli Araç Kullanımı, LLM sınırlılık/şeffaflık dayanağı). | `GEREÇ ve YÖNTEM` | not-run | not-run | `cite-ok` | `/anlatim-zenginligi` 3.18 koşusunda eklendi. claim↔kaynak galileo embedding skoru 0,506 (cross-lingual TR↔EN, advisory). İçerik sadakati tam-metin argümanıyla teyit; verbatim kopya yok. Zotero item `XT243I4Q` pin'lendi (DOI+fulltext-URL+provenance notu). |
| `helmy2025tenRulesGenAI` | DOI: `10.1371/journal.pcbi.1013588`; PMID: `41150680`; PMCID: `PMC12561928` | `references.bib` künyesi eklendi; Zotero item `K49X7HZG` pin'lendi | PMC `PMC12561928` yapılandırılmış JATS tam metin (12.148 karakter) + Minerva Roche korpus vectorstore (26.483 karakter) `fulltext_cascade.py` ile doğrulandı; cilt/sayı/eLocator (21(10):e1013588) Crossref ile teyit edildi. | Üretici yapay zekânın bilimsel çalışmada dikkatli/gözetimli kullanımı; çıktının doğruluğu ve bütünlüğünden nihai olarak araştırmacının sorumlu kalması (GEREÇ ve YÖNTEM §Yapay Zekâ Destekli Araç Kullanımı, insan-gözetimi/sorumluluk dayanağı). | `GEREÇ ve YÖNTEM` | not-run | not-run | `cite-ok` | `/anlatim-zenginligi` 3.18 koşusunda eklendi. claim↔kaynak galileo embedding skoru 0,462 (cross-lingual TR↔EN, advisory). İçerik sadakati tam-metin argümanıyla teyit; verbatim kopya yok. Zotero item `K49X7HZG` pin'lendi (DOI+fulltext-URL+provenance notu). |
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
| `mokkink2018cosmin` | DOI: `10.1007/s11136-017-1765-4`; PMID: `29260445`; PMCID: `PMC5891552` | `M8T9FFS6`; URL attachment `P8K6AQTU`; note `SPWV22PB` | PubMed/PMC `PMC5891552` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | COSMIN ölçüm özellikleri, yapısal geçerlik, iç tutarlılık, kültürler arası geçerlik ve ölçüm değişmezliği çerçevesini psikometri okuryazarlığı için açıklamak. | `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `mokkink2018cosmin` olarak pin'lendi. |
| `putnickBornstein2016measurementInvariance` | DOI: `10.1016/j.dr.2016.06.004`; PMID: `27942093`; PMCID: `PMC5145197` | `7KZ76DAM`; URL attachment `Z8IAPCSB`; note `ZGA932JT` | PubMed/PMC `PMC5145197` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Configural, metric, scalar ve residual ölçüm değişmezliği basamaklarını kavramsal olarak açıklamak. | `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `putnickBornstein2016measurementInvariance` olarak pin'lendi. |
| `trizanoHermosilla2016omegaAlpha` | DOI: `10.3389/fpsyg.2016.00769`; PMID: `27303333`; PMCID: `PMC4880791` | `4XXRXT7M`; URL attachment `PRRABMHI`; note `HJAC8VMS` | PubMed/PMC `PMC4880791` canlı tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Cronbach alfa sınırları, omega katsayısı ve çarpık/congeneric madde koşullarında iç tutarlılık yorumunu açıklamak. | `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `trizanoHermosilla2016omegaAlpha` olarak pin'lendi. |
| `li2016ordinalCFA` | DOI: `10.3758/s13428-015-0619-7`; PMID: `26174714` | `NZV7W3N3`; URL attachment `GEC8WCD3`; note `8G8RGZB8` | Springer resmi tam metin sayfası ve PubMed metadata doğrulandı; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Dört-beş kategorili Likert maddeler için ordinal CFA, WLSMV/MLR ve küçük örneklem uyum yorumu bağlamını açıklamak. | `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | Zotero BibTeX key `li2016ordinalCFA` olarak pin'lendi. |
| `dirik2015sEmbuTurkish` | PMID: `26111288` | `9WNZ4HAB`; URL attachment `CJTXXIHK`; note `ZGV2R6HI` | Türk Psikiyatri Dergisi resmi PDF tam metni; PubMed metadata doğrulandı; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | S-EMBU-C/KAET-Ç Türkçe psikometrik zemini ve algılanan ebeveynlik ölçümünün yakın araçlarla kıyaslanabilirliğini açıklamak. | `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | Tezdeki 29 maddelik paralel EMBU-P/C ile birebir aynı form gibi yazılmayacak. |
| `hisli1989bdiTurkishUniversity` | Psikoloji Dergisi 7(23):3-13; açık PDF | `THXA6EC4`; URL attachment `5VCAN8XA`; file attachment `UAUNRWTV`; note `38GH4PXT` | Türk Psikologlar Derneği PDF arşivi; PDF 9 sayfa, taranmış; sayfa 1 görsel kontrolü ile başlık/yazar/özet doğrulandı. | Beck Depresyon Envanteri Türkçe geçerlik-güvenirlik zeminini depresif belirti dili için sınırlı kullanmak. | `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | Kesme noktası veya klinik tanı sonucu olarak kullanılmayacak. |
| `akturk2005bdipcTurkish` | Türkiye Aile Hekimliği Dergisi 9(3):117-122 | `BB76NUEU`; URL attachment `BM58AXHB`; note `CSRGFIBS` | Turkish Journal of Family Practice açık erişim/CC BY makale sayfası doğrulandı; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | BDI-PC/BDÖ-BB kısa tarama alternatifini Beck ailesinde Türkiye validasyon örneği olarak göstermek. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 21 maddelik Beck Depresyon Envanteri ile birebir eşdeğer gibi yazılmayacak. |
| `furmanBuhrmester1985srq` | PMID: `3987418`; DOI: `10.2307/1129733` | `H8VZE5PT`; URL attachment `3U2ISEFQ`; note `36APDHQ2` | University of Denver PDF tam metin ve PubMed metadata doğrulandı; Anna Crossref DOI eşleşmesi; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | SRQ/KİA'nın sıcaklık/yakınlık, göreli statü/güç, çatışma ve rekabet boyutlarını kavramsal olarak açıklamak. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | Kardeş ilişkisini yalnız aile konstelasyonu değişkenlerine indirgememek için kullanılacak. 2026-07-05 sertifikasyon: bayat item `Z5RKE9QG` Zotero'da 404 bulundu; DOI `10.2307/1129733` ile T1DM Thesis collection üyeliği yeniden kuruldu ve BibTeX key `furmanBuhrmester1985srq` pinlendi (yeni item `H8VZE5PT`). |
| `apalaci1996yoktez` | YÖK Tez No. `52148`; detail key `hJ3EPiUcex4VqnPi_fClcA`; encrypted no `hJ3EPiUcex4VqnPi_fClcA` | `79P3BCMC`; URL attachment `7M7UE8JS`; note `KDKXNIG7` | YÖK MCP thesis details ve PDF gate doğrulandı; toplam 157 sayfa, page 1 retrieval başarılı ancak OCR boş/taranmış çıktı. | KİA/SRQ'nun Türkiye uyarlama/kullanım tarihçesinde YÖK tez katmanını göstermek. | `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | Ham tez verisi veya ayrıntılı alıntı kullanılmayacak.  2026-07-03: Marmara §3.8.2 istisnası — SRQ/KİA Türkçe uyarlama hattının önemli birincil kaynağı olduğu için danışman kararıyla korundu (bölümdeki tek tez-kaynak istisnası). 2026-07-07: GEREÇ ve YÖNTEM §Kardeş İlişkileri Anketi'nde SRQ'nun Türkçe uyarlama kaynağı olarak metne bağlandı (bilinçli tez-yasağı istisnası, kullanıcı onayı). |
| `aktas2017kardesIliskileriOlcegi` | DOI: `10.21764/maeuefd.340206` | `RX4SHNCT`; URL attachment `W2JFZ83W`; note `RQ5FEFHX` | DergiPark PDF tam metin; Zotero `T1DM Thesis` collection `9ZFDHMZA`. | Türkiye'de kardeş ilişkileri için yerel ölçek geliştirme, AFA/DFA ve güvenirlik örneğini alternatif araç olarak açıklamak. | `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | Tezde kullanılan KİA/SRQ yerine geçmiş gibi yazılmayacak. 2026-07-07: GEREÇ ve YÖNTEM §Kardeş İlişkileri Anketi'nde 'ek/karşılaştırmalı kaynak' olarak eklendi; kullanılan araç olarak sunulmadı (bu not korundu). |
| `cetintas2021dfis` | DOI: `10.1111/jspn.12308`; PMID: `32844587` | `4E2VMUUC`; note `2V6DI5VB`; URL attachment `USW37IJK`; T1DM Thesis `9ZFDHMZA` | Anna's Archive Crossref-doğrulamalı tam metin; DFIS Türkçe geçerlik-güvenirlik (121 ebeveyn, 6-18 yaş T1DM). | Diyabetin aileye etkisi ölçeğinin Türkçe geçerlik-güvenirliği. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: `cetintas2019yoktez` tezinin dergi versiyonu (aynı yazar); §3.8.2 tez-yasağı uyumu için değiştirme. |
| `senCelasin2018plbss` | DOI: `10.4274/jcrpe.5028`; PMID: `28825591`; PMCID: `PMC5985386` | `6TKF4MS5`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC5985386` canlı tam metin. | Türkçe ebeveyn hipoglisemi korkusu ölçeği (P-LBSS) geçerliği; worry/behavior boyutları. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: `kesenYener2024yoktez` yerine (§3.8.2). §2.2'deki worry/behavior cümlesini de destekler. |
| `ozguven2025parentalCollab` | DOI: `10.4274/jcrpe.galenos.2024.2024-4-7`; PMID: `39711005`; PMCID: `PMC12118314` | `9BRQJZG8`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC12118314` canlı tam metin. | Türkiye T1DM ergen; ebeveyn katılımı/izlemi → öz-yeterlik, yaşam kalitesi, glisemik kontrol. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: `tatar2023yoktez`, `avan2017yoktez`, `turk2015yoktez` yerine (§3.8.2). 2026-07-05: GİRİŞ ulusal literatür cümlesinde `tuncay2025yoktez` tez atfının dergi karşılığı olarak eklendi. |
| `yuksel2024qol` | DOI: `10.14744/SEMB.2024.21456`; PMID: `39021699`; PMCID: `PMC11249999` | `ENDQ6QEV`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC11249999` canlı tam metin. | Türkiye olgu-kontrol; T1DM'de depresyon/anksiyete daha yüksek, yaşam kalitesi daha düşük. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: `ayranci2025yoktez` yerine (§3.8.2); akran zorbalığı iddiası kaldırıldı. 2026-07-05: GİRİŞ ulusal literatür cümlesine psikososyal sonuç hattı için eklendi. |
| `ceran2024selfmgmt` | DOI: `10.1007/s00431-024-05650-z`; PMID: `38864877`; PMCID: `PMC11322394` | `C5JXI4HW`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC11322394` canlı tam metin. | Türkiye T1DM ebeveyn öz-yönetim ölçeği geliştirme-geçerlik (190 ebeveyn). | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: `tuncay2025yoktez` yerine (§3.8.2). 2026-07-05: GİRİŞ ulusal literatür cümlesine ebeveyn öz-yönetimi hattı için eklendi. |
| `adal2015psychosocial` | DOI: `10.4274/jcrpe.1745`; PMID: `25800477`; PMCID: `PMC4439893` | `Z8SN66BQ`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC4439893` canlı tam metin. | Türkiye 295 T1DM ergen; depresyon/anksiyete + algılanan aile desteği (BDI). | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: `demirkiran2025yoktez` / `ayranci2025yoktez` destek kaynağı (§3.8.2). 2026-07-05: GİRİŞ ulusal literatür cümlesine psikososyal uyum hattı için eklendi. |
| `dimeglio2018t1d` | DOI: `10.1016/S0140-6736(18)31320-5`; PMID: `29916386`; PMCID: `PMC6661119` | `WJVX8GXN`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC6661119` canlı tam metin (Lancet seminer). | T1DM tanımı: otoimmün beta-hücre yıkımı, insülin eksikliği, kronik hiperglisemi; patogenez, insülin rejimleri ve DKA genel çerçevesi. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.1 textbook yeniden yazımı; T1DM temel tanım/patofizyoloji otoriter seminer kaynağı. |
| `deBock2022ispadGlycemicTargets` | DOI: `10.1111/pedi.13455`; PMID: `36537523`; PMCID: `PMC10107615` | `S9CBWMPP`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC10107615` canlı tam metin. | ISPAD 2022 glisemik hedefler ve glukoz izlemi; glisemik kontrol hedefi, hedef aralıkta geçirilen süre (TIR). | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.1 glisemik kontrol/glisemik hedef tanımı. |
| `compas2012coping` | DOI: `10.1146/annurev-clinpsy-032511-143108`; PMID: `22224836`; PMCID: `PMC3319320` | `UMIRI6XR`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC3319320` canlı tam metin. | Kronik hastalıkta çocuk/ergen baş etme ve uyum; kontrol-temelli baş etme modeli, tedaviye uyumu etkilemesi, psikososyal uyum. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.4 kronik hastalık/gelişim/baş etme kaynağı (Elicit ile bulundu, PMC OA). |
| `rollandWalsh2006` | DOI: `10.1097/01.mop.0000245354.83454.68`; PMID: `16969168` | `NMXVNM5P`; T1DM Thesis `9ZFDHMZA` | Anna's Archive Crossref-doğrulamalı tam metin (Curr Opin Pediatr). | Aile Sistemleri–Hastalık modeli; çocuk/ergen kronik hastalığında aile dinamikleri, uyum, hastalık davranışı ve seyir ilişkisi. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.5 aile sistemleri kuramsal çerçeve (Elicit→Anna's). |
| `rosland2012family` | DOI: `10.1007/s10865-011-9354-4`; PMID: `21691845` | `BM38N9FH`; T1DM Thesis `9ZFDHMZA` | Anna's Archive Crossref-doğrulamalı tam metin (J Behav Med). | Aile davranışları ve iletişim örüntülerinin kronik hastalık sonuçlarıyla ilişkisi (erişkin hasta; ilke aktarımı): uyum/dikkatli yanıt olumlu, eleştiri/aşırı koruma/kontrol olumsuz. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.5 aile davranışı/iletişim; erişkin→pediatrik dolaylı aktarım etiketli. |
| `pinquart2017parentingDimensions` | DOI: `10.1037/dev0000295`; PMID: `28459276` | `DC3Z572U`; T1DM Thesis `9ZFDHMZA` | Anna's Archive Crossref-doğrulamalı tam metin (Dev Psychol). | Ebeveynlik boyutları/stilleri ile çocuk/ergen sonuçları meta-analizi: sıcaklık/davranışsal kontrol/özerklik tanıma/otoritatif koruyucu; sert-psikolojik kontrol/otoriter riskli. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.6 ebeveynlik boyut/stil kuramsal temel (Elicit→Anna's). |
| `rohner2004parAcceptance` | DOI: `10.1037/0003-066X.59.8.830`; PMID: `15554863` | `2GG5FNE4`; T1DM Thesis `9ZFDHMZA` | Anna's Archive Crossref-doğrulamalı tam metin (Am Psychol). | Ebeveyn kabul-red kuramı (PARTheory): sıcaklık-sevgi/düşmanlık/ihmal/red; algılanan kabul-red ↔ psikolojik uyum; sıcaklık bağlanma sinyali. | `GENEL BİLGİLER`, `TARTIŞMA` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.6 kabul-red + bağlanma kaynağı (Elicit→Anna's). |
| `arrindell2005sembu` | DOI: `10.1027/1015-5759.21.1.56` | `UIK78UVM`; T1DM Thesis `9ZFDHMZA` | RUG kurumsal repository OA PDF (Eur J Psychol Assess). | s-EMBU algılanan ebeveyn tutumu aracı; üç alt ölçek (reddetme, duygusal sıcaklık, aşırı koruma) ve kültürler-arası faktör geçerliği; öz-bildirim doğası. | `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.7 EMBU çerçevesi/boyutları (Elicit→OA). |
| `arrindell1999sembu` | DOI: `10.1016/S0191-8869(98)00192-5`; OpenAlex `W2020124029` | `GUX6Z6E6`; T1DM Thesis `9ZFDHMZA` | OpenAlex kimlik doğrulandı (Personality and Individual Differences 27(4):613-628, 12 yazar); OA bronze (`is_oa=true`), ScienceDirect tam metin. | s-EMBU orijinal kısa-form geliştirme: 23 madde, ÜÇ faktör (Emotional Warmth, Overprotection, Rejection); Karşılaştırma alt ölçeği standart s-EMBU'da YOKTUR — ch03 Karşılaştırma alt ölçeği köken netleştirme birincil kaynağı. | `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-13 ch03 Karşılaştırma köken netleştirme; Zotero 9ZFDHMZA import + BibTeX key pin (v2955); OA bronze full-text. Perris 1980 köken adayı REDDEDİLDİ (Karşılaştırma maddeleri 4/5 akran kıyaslaması, Perris 'Favouring siblings' ile eşleşmez). Karşılaştırma boyutunun provenansı `docs/protokol/KLINIK_CALISMA_PROTOKOLU.md` §11.2-11.3'te BELGELİ: Sümer, Gündoğdu-Aktürk & Helvacı (2010) — bkz. `sumer2010anneBabaTutum`. |
| `sumer2010anneBabaTutum` | Türk Psikoloji Yazıları 13(25):42-59; OpenAlex `W2564172531`; DOI YOK | Zotero pin bekliyor (DOI'siz Türkçe dergi; bridge yalnız import-doi) | OpenAlex kimlik doğrulandı; tam metin erişilemedi (kapalı / DOI-yok / Doğuş PDF 403 / Anna's-yok) → full-text-exception; iddia tezin kanonik ölçek tanımı (kullanıcı-sağladı) + `KLINIK_CALISMA_PROTOKOLU.md` §11.2-11.3 ile doğrudan temellendi. | s-EMBU-C/P Türkçe formuna Karşılaştırma (5 madde) alt ölçeğini ekleyen kaynak; ch03 §Veri Toplama Araçları + §Psikometrik Değerlendirme. | `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-13 kullanıcı yönlendirmesiyle provenans doğrulandı (Nebi Sümer izi). NOT: kaynak bir DERLEME ('toplu bakış'), klasik validasyon makalesi değildir; Sümer külliyatında 'EMBU' 0 kez geçer → 29-madde/4-faktör formun psikometrik geliştirme kaydı zayıf, tezin çalışma-içi yeniden-doğrulaması bu yüzden yerinde. `dirik2015sEmbuTurkish` (KAET-Ç Türkçe psikometri) ayrı ve tamamlayıcı referans olarak korunur. Zotero: DOI'siz → manuel ekleme bekliyor (creswell/lincolnGuba precedent'i). |
| `castro1993embuChildren` | DOI: `10.1177/002076409303900105`; PMID: `8478163` | `VC3I6MSX`; T1DM Thesis `9ZFDHMZA` | Anna's Archive Crossref-doğrulamalı tam metin (Int J Soc Psychiatry). | EMBU'nun çocuk örnekleminde (7-12 yaş) dört faktörü: Duygusal Sıcaklık, Reddetme, Kontrol Çabaları, Favouring Subject (kayırma/karşılaştırma). | `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.7 çocuk EMBU 4 boyut/karşılaştırma (Elicit→Anna's). |
| `young2014parentalInvolvement` | DOI: `10.1007/s11892-014-0546-5`; PMID: `25212099`; PMCID: `PMC4283591` | `REG3BXGC`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC4283591` canlı tam metin. | T1DM'li gençlerde ebeveyn katılımının miktar, tip (izlem/problem çözme) ve nitelik (sıcak/eleştirel) boyutları biyopsikososyal sonuçlarla ilişkili; paylaşılan sorumluluk. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.8 diyabette ebeveyn katılımı/izlem niteliği (Elicit→PMC OA). |
| `jaser2011familyInteraction` | DOI: `10.1007/s11892-011-0222-y`; PMID: `21853415`; PMCID: `PMC3370388` | `UTUICUG4`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC3370388` canlı tam metin. | Pediatrik T1DM'de aile etkileşimi; ergenliğe geçerken ebeveyn izleminin önemi, en iyi sonuçların sıcak/iş birlikçi katılımla; ebeveyn distresinin rolü. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-03: §2.8 aile etkileşimi/izlem-sıcaklık (Elicit→PMC OA). |
| `goodman2020parentingMediator` | DOI: `10.1007/s10567-020-00322-4`; PMID: `32734498` | `ZEHTTTDD`; T1DM Thesis `9ZFDHMZA` | Anna's Archive Crossref-doğrulamalı tam metin (Clin Child Fam Psychol Rev). | Anne depresyonu → sorunlu ebeveynlik (aracı) → çocuk işlevi; hem olumlu (sıcaklık) hem olumsuz ebeveynlik aracılık eder; ebeveynlik değiştirilebilir; aracılık nedenselliğin gerekli ama yeterli olmayan göstergesi. | `GİRİŞ ve AMAÇ`, `GENEL BİLGİLER`, `TARTIŞMA` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-04: §2.10 anne depresif belirti→ebeveynlik yolları (Elicit→Anna's). 2026-07-13 GİRİŞ sertifikasyonu: 4. paragrafta anne depresyonu→ebeveynlik aracılık cümlesinde ([@goodman2020parentingMediator]) atıflı olduğu Bölüm sütununa yansıtıldı. |
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
| deLosReyesOhannessian2016 | 10.1007/s10964-016-0533-z | pending | PubMed 27384957 (editorial, metadata-doğrulandı) | Anne-çocuk rapor ayrışması anlamlı bilgi-veren perspektif farkı (informant discrepancy) | CSR §15 | pending | pending | full-text-exception | §15 bib-wiring; Zotero+reliability bölüm kapanışında |
| alAnsari2021mothers | 10.1186/s11689-021-09369-y | pending | PMC8141116 tam metin | T1DM çocuk annelerinde anksiyete/stres izlemi gerekliliği | CSR §15 | pending | pending | full-text-ok | §15 bib-wiring |
| chiHinshaw2002depression | 10.1023/a:1015770025043 | pending | PubMed 12109489 (metadata-doğrulandı) | Maternal depresif belirti → çocuk davranış raporunda çarpıtma (depression-distortion) | CSR §15 | pending | pending | full-text-exception | §15 bib-wiring |
| milan2017attachment | 10.1007/s10802-016-0156-6 | pending | PMC5802392 tam metin | Anne-kız rapor uyuşmazlığı bağlanma stiliyle modere olur | CSR §15 | pending | pending | full-text-ok | §15 bib-wiring |
| solmeyerMcHale2017differential | 10.1111/famp.12166 | pending | PMC5513888 tam metin | Ebeveyn diferansiyel muamele → ergen uyumu (boylamsal) | CSR §15 | pending | pending | full-text-ok | §15 bib-wiring |
| mchale2005mexican | 10.1111/j.1741-3737.2005.00215.x | pending | PMC2293294 tam metin | Kardeş diferansiyel muamele kalıpları ve uyum | CSR §15 | pending | pending | full-text-ok | §15 bib-wiring |
| imai2010mediation | 10.1037/a0020761 | pending | PubMed 20954780 (kanonik yöntem makalesi, metadata-doğrulandı) | Nedensel aracılık duyarlılık analizi (ρ_kritik) yöntemi | CSR §15 | pending | pending | full-text-exception | §15 bib-wiring; yöntem-atfı |
| vickers2016netbenefit | 10.1136/bmj.i6 | pending | PMC4724785 tam metin | Net fayda / karar-eğrisi analizi yöntemi (öngörü modeli değerlendirme) | CSR §15 | pending | pending | full-text-ok | §15 bib-wiring |
| chen2026overreactive | 10.1186/s12889-026-26410-8 | pending | PMC12918021 tam metin | Anne depresif belirti→aşırı-tepkisel ebeveynlik→çocuk (16.258 düad, %35,9 aracılık) | CSR §16 | pending | pending | full-text-ok | §16 bib-wiring |
| procaccia2026maternalPtsd | 10.3390/healthcare14080984 | pending | PMC13115776 tam metin | Anne depresyon/PTSD→çocuk içselleştirme, ebeveynlik-stresi aracılığıyla | CSR §16 | pending | pending | full-text-ok | §16 bib-wiring; IPV örneklemi caveat |
| ng2020differential | 10.3389/fpsyg.2020.01656 | pending | PMC7399693 tam metin | Ebeveyn diferansiyel muamele (PDT) %65 ailede, çocuk uyumuyla ilişkili | CSR §16 | pending | pending | full-text-ok | §16 bib-wiring |
| piotrowski2022ckdSiblings | 10.1007/s00467-022-05559-5 | pending | PMC9066131 tam metin | Kronik hastalık kardeşlerinde PDT algısı belirgin sorun | CSR §16 | pending | pending | full-text-ok | §16 bib-wiring |
| loeser2016fairness | 10.1007/s10826-016-0429-2 | pending | PMC5110249 tam metin | PDT→uyumsuzluk; adil algılandığında ilişki kaybolur | CSR §16 | pending | pending | full-text-ok | §16 bib-wiring |
| zietz2022fsm | 10.1016/j.childyouth.2022.106661 | pending | PMC9631805 tam metin | Aile Stres Modeli 7 ülke: ekonomik zorluk→anne depresyonu→ebeveynlik | CSR §16 | pending | pending | full-text-ok | §16 bib-wiring |
| kavanaugh2018economicPressure | 10.1037/fam0000462 | pending | PMC6205903 tam metin | Ekonomik baskı→anne depresif belirti→sert ebeveynlik (boylamsal FSM) | CSR §16 | pending | pending | full-text-ok | §16 bib-wiring |
| newland2013familyStress | 10.1037/a0031112 | pending | PMC8011847 tam metin | Ekonomik zorluk→anne psikolojik belirti→duyarlı ebeveynlik azalışı | CSR §16 | pending | pending | full-text-ok | §16 bib-wiring |
| jensenMcHale2017pdt | 10.1016/j.adolescence.2017.08.002 | pending | PMC5685545 tam metin | Ebeveyn-genç PDT rapor uyuşmazlığı→ilişki kalitesi | CSR §16 | pending | pending | full-text-ok | §16 bib-wiring |
| alazmi2024t1dReview | 10.1177/13591045231177115 | pending | PMC11188552 tam metin | T1DM çocuk+ebeveyn: depresyon/hipoglisemi korkusu/ebeveynlik stresi (SR) | CSR §16 | pending | pending | full-text-ok | §16 bib-wiring |
| abadula2024maternalDepr | 10.1093/jpepsy/jsad070 | pending | PMC10874213 tam metin | T1DM anne depresif belirti + diyabet ilişki-distresi→ergen glisemik kontrol | CSR §16 | pending | pending | full-text-ok | §16 bib-wiring |
| neo2022t1dCovid | 10.1111/jpc.16101 | pending | PMC9796503 tam metin | T1DM çocuk glisemik kontrol↔depresif/yalnız hissetme pozitif, net-hedef ters | CSR §16 | pending | pending | full-text-ok | §16 bib-wiring |
| trillingsgaard2018maternalAge | 10.1080/17405629.2016.1266248 · Zotero key `FZ4GAIGT` | pending | OpenAlex W2494719444 (kanıt: doğrulandı; kapı yıl 2018 basım/2016 online düzeltti) | İleri anne yaşı→yaptırım kullanımı→çocuk sosyo-duygusal gelişim | CSR §16 | pending | pending | full-text-exception | §16 bib-wiring; yıl kapı-düzeltmesi |

| `fang2025techDisparities` | DOI: `10.1001/jamanetworkopen.2025.26353`; PMID: `40788645`; PMCID: `PMC12340658` | `5ZHKH3S2`; URL attachment + note (import-doi) | PubMed/PMC `PMC12340658` canlı tam metin; Zotero `T1DM Thesis` `9ZFDHMZA`. | ABD kesitsel (186.590 T1D; 26.853 genç): glisemik kontrol ve diyabet teknolojisi (CGM/pompa) kullanımı etnik azınlık ve Medicaid-sigortalı gençlerde en düşük; eşitsizlikler zamanla sürdü/derinleşti. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: Sosyoekonomik-Kültürel-Klinik Bağlam alt bölümü, SES-teknoloji eşitsizliği. Zotero BibTeX key pin'lendi. Nedensel dil yok. |
| `lansingBerg2014selfRegulation` | DOI: `10.1093/jpepsy/jsu067`; PMID: `25214646`; PMCID: `PMC4201765` | `P89TDEU4`; URL attachment + note (import-doi) | PubMed/PMC `PMC4201765` canlı tam metin; Zotero `9ZFDHMZA`. | Öz-düzenleme (bilişsel/duygusal/davranışsal) ergen kronik hastalık öz-yönetiminde hem bireysel (öz-yeterlik, baş etme, uyum) hem kişilerarası (ebeveyn izlemi, akran desteği) risk/dayanıklılık kaynaklarının temeli. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: Kronik hastalık alt bölümü; `compas2012coping` tek-kaynağını dengeler. Zotero BibTeX key pin'lendi. |
| `ferro2022informantAgreement` | DOI: `10.1177/07067437221074430`; PMID: `35060408`; PMCID: `PMC9301150` | `ZNM4FTIP`; URL attachment + note (import-doi) | PubMed/PMC `PMC9301150` canlı tam metin; Zotero `9ZFDHMZA`. | Kronik fiziksel hastalıklı 263 çocuk (2-16y): ebeveyn-çocuk ruhsal belirti uyumu düşük (κ=0,18); ebeveyn-bildirimli %38 vs çocuk oz-bildirim %25. | `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: Çoklu bilgi kaynağı alt bölümü; `deLosReyes2015`'i tamamlar. Zotero BibTeX key pin'lendi. |
| `wong2023dyadicSatisfaction` | DOI: `10.1111/dme.15254`; PMID: `38010056`; PMCID: `PMC11021166` | `VA7CBCQ2`; URL attachment + note (import-doi) | PubMed/PMC `PMC11021166` canlı tam metin; Zotero `9ZFDHMZA`. | T1DM 157 ebeveyn-ergen diadı: ebeveyn katılımından çok memnun ergen %71 vs ebeveyn %26; ergen katılımından çok memnun %43 vs %29 — ebeveyn-ergen diadik diskordans. | `GENEL BİLGİLER` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-06: Diadik uyum alt bölümü; T1DM-özgü. Zotero BibTeX key `wong2023dyadicSatisfaction`; `references.bib` yıl 2024 (dergi sayısı), key etiketi 2023 (epub). İlişkisel dil. |
| `eckshtain2010parentDepression` | DOI: `10.1093/jpepsy/jsp068`; PMID: `19710249`; PMCID: `PMC2902839` | `JGTVK7JB`; URL attachment `HG5ZU49P`; note `3FG2I55W` (import-doi) | PubMed/PMC `PMC2902839` canlı tam metin; Zotero `T1DM Thesis` `9ZFDHMZA`. | T1D kentsel ergen (N=61, 10-17 yaş); ebeveyn depresif belirtileri, ebeveynlik uygulamaları (ilgi/izlem) aracılığıyla genç depresif belirtileri ve metabolik kontrol ile ilişkili (path analizi, kesitsel). | `GİRİŞ ve AMAÇ` | 55/55 passed | 142/142 passed | `reliability-ok` | 2026-07-11 GİRİŞ zenginleştirme: P4'e (maternal depresyon zinciri) taslak alındı. Referans kapısı workflow ilk-yazar/yıl hatasını düzeltti: taslak `butler2009` → kanonik **Eckshtain D, 2010** (Butler JM aslında `butner2009`'un 4. yazarı). İlişkisel dil; genel değil T1D örneklemi (küçük N/kesitsel sınırlılığı). **2026-07-12 /bolum-sertifika Kapı 0-5 PASS** (sci-audit 7-eksen 0 blocker; doktoratezi-ai-audit 142/142; t1dm-qual-ai-audit 55/55; hook 13/13; GİRİŞ izole render exit 0) → **provisional-pass (`reliability-ok`)**. `cite-ok` için kalan tek koşul: tam-tez `targets::tar_make()` + `quarto render` exit 0 (Bulgular `outputs/tables/*.csv` artefaktları üretilince). |
| `butner2009discrepancy` | DOI: `10.1037/a0015363`; PMID: `19413435`; PMCID: `PMC2805180` | `MW9KI6GD`; URL attachment `69IBCRAS`; note `XRW46DEK` (import-doi) | PubMed/PMC `PMC2805180` canlı tam metin; Zotero `T1DM Thesis` `9ZFDHMZA`. | T1D 185 ergen + anne/baba; ebeveyn-ergen algı ayrışması (yeterlik) daha fazla ergen özerkliği + ebeveyn özerklik teşviki ile, ancak kötü metabolik kontrol + kötü ebeveyn psikososyal iyilik hali ile ilişkili (latent discrepancy SEM). | `GİRİŞ ve AMAÇ` | 55/55 passed | 142/142 passed | `reliability-ok` | 2026-07-11 GİRİŞ zenginleştirme: P6'ya (çok-bilgi-kaynağı) taslak alındı; `deLosReyes2015`'i T1D-özgü algı ayrışmasıyla tamamlar. İlişkisel dil; T1D örneklemi. **2026-07-12 /bolum-sertifika Kapı 0-5 PASS** (sci-audit 7-eksen 0 blocker; doktoratezi-ai-audit 142/142; t1dm-qual-ai-audit 55/55; hook 13/13; GİRİŞ izole render exit 0) → **provisional-pass (`reliability-ok`)**. `cite-ok` için kalan tek koşul: tam-tez `targets::tar_make()` + `quarto render` exit 0. |
| `streisandMonaghan2014` | DOI: `10.1007/s11892-014-0520-2`; PMID: `25009119`; PMCID: `PMC4113115` | `HPPEQX8C`; T1DM Thesis `9ZFDHMZA` | PubMed/PMC `PMC4113115` canlı tam metin (OA); abstract iddiayı doğruladı. | Genç çocuklarda T1D bakım sorumluluğu/ebeveyn stresinin yüksekliği; ch05 H3 sosyal-istenirlik yorumunun bağlam dayanağı (savunmacılık tezin yorumudur, kaynağa atfedilmedi). | `TARTIŞMA` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-13 ch05 B1 referans kapısı; import-doi item `HPPEQX8C` → 9ZFDHMZA. |
| `laffel2003teamwork` | DOI: `10.1067/mpd.2003.138`; PMID: `12712059` | `REHMC57X`; T1DM Thesis `9ZFDHMZA` | J Pediatr closed; NCBI yapısal abstract iddiayı doğruladı (TW müdahalesi aile katılımını korudu, DFC artmadı, glisemik bozulmayı önledi). | Aile-odaklı ekip müdahalesinin anne-çocuk uyum kopukluğunu azaltma potansiyeli; ch05 H3. | `TARTIŞMA` | 55/55 passed | 142/142 passed | `cite-ok` (abstract-doğrulamalı) | 2026-07-13 ch05 B1; ch05'teki 'Anderson 2003' bu makaledir (Anderson BJ kıdemli yazar); 'FBBT' etiketi 'aile-odaklı ekip müdahalesi' olarak düzeltildi; import-doi item `REHMC57X`. |
| `cicchetti1994` | DOI: `10.1037/1040-3590.6.4.284`; OpenAlex `W2063085086` | `CA227AGF`; T1DM Thesis `9ZFDHMZA` | Psychol Assess closed; OpenAlex tam kimlik eşleşmesi (başlık/DOI; 8914 atıf); ICC yorum bantları kanonik içerik. | ICC yorum bantları (zayıf/orta/iyi/mükemmel); ch05 H5 diadik uyum yorumu. | `TARTIŞMA` | 55/55 passed | 142/142 passed | `cite-ok` (identity-doğrulamalı) | 2026-07-13 ch05 B1; import-doi item `CA227AGF`; klasik ölçüm-metodoloji kaynağı. |
| `kennyKashyCook2006` | ISBN: `9781572309869`; OpenAlex (book review) `W1999820757`; Zotero key `DDDEWJM6` (Web API ISBN import 2026-07-27) | Zotero pin tamamlandı (DOI'siz kitap; manuel ISBN import — bridge yalnız import-doi destekler) | **Anna's Library** md5 `52b9d4540b5aaa2a21f63b89a5a0ee21` (pdf, 480 s., text_quality=ok); diadik güç kanıtı görüldü: s.412 "r=0,20 … n=200'de anlamlı", s.69/s.200 güç hesabı; OpenAlex book-review ile kimlik. | Diadik veri analizinde k/güç yorumu için n ≥ 200 düad heuristiği (ch05 H5); ayrıca aktör-partner karşılıklı bağımlılık modeli (APIM) diadik çözümleme dayanağı (ch03 §H2). | `TARTIŞMA`, `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `full-text-ok` (zotero-pending) | 2026-07-13 ch05 B1; kanonik metodoloji kitabı; Anna's tam metin doğrulandı (kullanıcı isteğiyle). `lincolnGuba1985` precedent'i: bind edildi, manuel ISBN Zotero import bekliyor. 2026-07-13 ch03 §H2 APIM diadik model dayanağı olarak da bağlandı (kitap precedent'i, kullanıcı onayı). |
| `hox2017multilevel` | DOI: `10.4324/9781315650982`; ISBN: `9781315650982` | `references.bib` künyesi mevcut; Zotero pin bekliyor | Routledge kitabı (3. baskı); kimlik DOI/ISBN ile doğrulandı; çok-düzeyli modelleme kanonik metodoloji kaynağı. | Çok-düzeyli modellemede aile-içi ICC eşiği (~0,05); ch05 H1 + GEREÇ ve YÖNTEM/BULGULAR çok-düzeyli gerekçe. | `GEREÇ ve YÖNTEM`, `BULGULAR`, `TARTIŞMA` | 55/55 passed | 142/142 passed | `cite-ok` (identity-doğrulamalı) | 2026-07-13 ch05 B1'de metne bağlandı ('Hox 2018' → 2017 baskısına hizalandı); daha önce ledger-untracked metod-textbook. |
| `collins2015tripod` | DOI: `10.1136/bmj.g7594`; OpenAlex `W4233026002` | Zotero key `8V7IIVQ6` (Web API import 2026-07-27) | BMJ açık erişim (bmj.g7594); TRIPOD raporlama kılavuzu kanonik metin, OpenAlex kimlik. | Öngörü/risk modeli raporlama çerçevesi (TRIPOD); ch03 §Araştırma Tasarımı. | `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` (metadata-doğrulamalı) | 2026-07-13 ch03 çerçeve-atıf kapaması; OpenAlex + BMJ OA doğrulandı; Zotero pin bekliyor. |
| `ocathain2008gramms` | DOI: `10.1258/jhsrp.2007.007074`; PMID: `18416914` | `references.bib` künyesi mevcut; Zotero pin bekliyor | J Health Serv Res Policy; PubMed kimlik doğrulandı (PMID 18416914). | Karma yöntem raporlama çerçevesi (GRAMMS); ch03 §Araştırma Tasarımı. | `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` (metadata-doğrulamalı) | 2026-07-13 ch03 çerçeve-atıf kapaması; PubMed doğrulandı; Zotero pin bekliyor. |
| `austin2009balanceDiagnostics` | DOI: `10.1002/sim.3697` | `DBZ2HWQJ`; T1DM Thesis `9ZFDHMZA` (import-doi) | Stat Med closed; Crossref/DOI kimlik eşleşmesi; SMD denge-tanı bantları kanonik metodoloji. | SMD denge eşikleri (\|SMD\|<0,10 iyi; 0,10–0,25 sınırda; ≥0,50 ciddi); §4.1 kovaryat dengesi. | `BULGULAR`, `GEREÇ ve YÖNTEM` | 55/55 passed | 144/144 passed | `cite-ok` (identity-doğrulamalı) | 2026-07-14 BULGULAR (04) sertifikasyonu Kapı 2; import-doi item `DBZ2HWQJ`; klasik nedensel-çıkarım metodoloji kaynağı. |
| `cheungRensvold2002invariance` | DOI: `10.1207/S15328007SEM0902_5` | `A7FD343B`; T1DM Thesis `9ZFDHMZA` (import-doi) | SEM (Taylor & Francis) closed; Crossref/DOI kimlik eşleşmesi; ΔCFI değişmezlik eşiği kanonik. | Ölçüm değişmezliği eşiği (ΔCFI<0,010); §4.2 psikometri + §4.3.4 H4 çok-grup. | `BULGULAR`, `GEREÇ ve YÖNTEM` | 55/55 passed | 144/144 passed | `cite-ok` (identity-doğrulamalı) | 2026-07-14 BULGULAR (04) Kapı 2; import-doi item `A7FD343B`; klasik ölçüm-değişmezlik kaynağı. |
| `samejima1969graded` | DOI: `10.1007/BF03372160` | `8BFE3VD5`; T1DM Thesis `9ZFDHMZA` (import-doi) | Psychometrika monografi closed; Crossref/DOI kimlik eşleşmesi; graded response IRT kanonik. | Dereceli-yanıt (graded response) IRT modeli; §4.3.1 H1 latent θ. | `BULGULAR`, `GEREÇ ve YÖNTEM` | 55/55 passed | 144/144 passed | `cite-ok` (identity-doğrulamalı) | 2026-07-14 BULGULAR (04) Kapı 2; import-doi item `8BFE3VD5`; klasik IRT metodoloji kaynağı. |
| `benjaminiHochberg1995fdr` | DOI: `10.1111/j.2517-6161.1995.tb02031.x` | `FSDNF6QU`; T1DM Thesis `9ZFDHMZA` | JRSS-B closed; Crossref/DOI kimlik eşleşmesi; BH-FDR kanonik. | Benjamini-Hochberg yanlış-keşif oranı düzeltmesi; §4 preamble + H1–H4 aileleri. | `BULGULAR`, `GEREÇ ve YÖNTEM` | 55/55 passed | 144/144 passed | `cite-ok` (identity-doğrulamalı) | 2026-07-14 BULGULAR (04) Kapı 2; Zotero mevcut item `FSDNF6QU`; klasik çoklu-karşılaştırma kaynağı (ch03 satır 111'de de çapalı). |
| `holm1979` | OpenAlex `W2121044470`; JSTOR stable 4615733 (Crossref-kayıtlı DOI yok) | Zotero pin bekliyor (yeni; DOI'siz → manuel ISBN/JSTOR import) | OpenAthens OA-PDF (ime.usp.br, 7 sf, text_quality=ok) → anamnesis ingest; Sture Holm, Scand J Stat 6(2):65–70 kimlik+içerik doğrulandı. | Ardışık-red FWER (aile-düzeyi hata oranı) çoklu-karşılaştırma düzeltmesi; §3.9 keşifsel/ikincil katman (L120). | `GEREÇ ve YÖNTEM` | pending | pending | `full-text-ok` (zotero-pending) | 2026-07-25 §3.9 zenginleştirme C3; kimlik OpenAlex; tam metin OpenAthens OA-PDF; SOFT eksik-DOI (1979 pre-DOI klasik, JSTOR stable note'ta); claim↔kaynak title-düzeyi birebir (galileo 0,46 çapraz-dilli artefakt). reliability-ok + cite-ok ch03 /tez-dogrulama kapanışında. |
| `wagenmakers2010` | DOI: `10.1016/j.cogpsych.2009.12.001`; OpenAlex/Semantic Scholar doğrulandı (690 atıf) | Zotero pin bekliyor (yeni; import onay bekliyor) | Minerva full-text (Elsevier, ai_inference=true, 25 chunk) → anamnesis; "Savage–Dickey density ratio … Bayesian hypothesis test for nested models" içerik doğrulandı. | Bayes faktörü Savage-Dickey yoğunluk oranıyla (nested-model) kestirimi; §3.9 Bayesçi paralel hat (L164). | `GEREÇ ve YÖNTEM` | pending | pending | `full-text-ok` (zotero-pending) | 2026-07-25 §3.9 zenginleştirme C4; DOI Crossref/S2 doğrulandı; tam metin Minerva; claim↔kaynak title-düzeyi birebir (galileo 0,55 çapraz-dilli artefakt). reliability-ok + cite-ok ch03 /tez-dogrulama kapanışında. |
| `sandelowski2000qualDescription` | DOI: `10.1002/1098-240X(200008)23:4<334::AID-NUR9>3.0.CO;2-G`; OpenAlex `W2159165123`; PMID `10940958` | Zotero pin bekliyor (yeni; import onay bekliyor) | Minerva full-text (Wiley, ai_inference=true); abstract "stay close to their data ... everyday terms ... straight descriptions of phenomena" içerik doğrulandı (OA-PDF Wiley SSO-gated + annas 404 → Minerva). | Nitel tanımlayıcı yaklaşım (düşük-çıkarım, veriye/olayın gündelik diline yakın betimleme) tasarım etiketi; §3.10 (L176). | `GEREÇ ve YÖNTEM` | pending | pending | `full-text-ok` (zotero-pending) | 2026-07-25 §3.10 zenginleştirme B2; kimlik OpenAlex+PMID+DOI; tam metin Minerva; claim↔kaynak birebir (galileo 0,36 çapraz-dilli artefakt). reliability-ok + cite-ok ch03 /tez-dogrulama kapanışında. |
| `patton2015qualitative` | ISBN: `9781412972123`; SAGE 4. baskı (2015) | Zotero pin bekliyor (DOI'siz kitap; manuel ISBN import — `kennyKashyCook2006`/`hox2017multilevel` precedent'i) | **Anna's Library** md5 `5c6c9445d48d176a32c6b1183202453c` (4. bs. "Integrating Theory and Practice"); `search_in_document` pasajları: "maximum variation/heterogeneity sampling" (s.283), "purposeful sampling ... information-rich" (s.656) doğrulandı. | Amaçlı örnekleme (*purposive*) + maksimum-varyasyon örnekleme mantığı; §3.10 (L180). | `GEREÇ ve YÖNTEM` | pending | pending | `full-text-ok` (zotero-pending) | 2026-07-25 §3.10 zenginleştirme B3; kanonik nitel-metodoloji kitabı; annas tam metin (kullanıcı /referans-kapisi isteğiyle); kitap precedent'i (kenny/hox); claim↔kaynak birebir (galileo 0,46 çapraz-dilli artefakt). reliability-ok + cite-ok ch03 /tez-dogrulama kapanışında. |
| `kortesluoma2003childInterview` | DOI: `10.1046/j.1365-2648.2003.02643.x`; OpenAlex `W2037244454`; PMID `12752864` | Zotero pin bekliyor (yeni; import onay bekliyor) | Minerva full-text (Wiley, ai_inference=true, 9 chunk) + annas (abstract/giriş): "differences between adults' and children's points of view ... developmental and experiential factors ... method must suit both the purpose and the context" doğrulandı. | Çocuk-uyumlu/gelişimsel düzeye uyarlanmış nitel görüşme sorulandırması yöntem-gerekçesi; §3.11 (L186). | `GEREÇ ve YÖNTEM` | pending | pending | `full-text-ok` (zotero-pending) | 2026-07-25 §3.11 zenginleştirme P2; kimlik OpenAlex+PMID+DOI; Minerva+annas tam metin; RBŞ-ihtiyat: "yerleşik gereklilik" değil "gelişimsel uyarlama vurgusu" (kaynak çocuk-görüşme rehberliğinin sınırlı olduğunu da belirtir; pilot-yok sınırlılığıyla çelişmez); galileo groundedness 0,88 supported (claim 0,45 çapraz-dilli artefakt). reliability-ok + cite-ok ch03 /tez-dogrulama kapanışında. |
| `fetters2013integration` | Zotero item `QVFR6N96` (import tablosu; DOI Zotero'da) | `7FVHIDI9` | PMC (NIH public access) — önceden full-text-ok; joint-display + entegrasyon-uyumu (convergence/complementarity/discordance/expansion) taksonomisi kanonik. | Birleşik gösterim (joint display) bir çözümleme/entegrasyon aracıdır (doğrulama değil) + dört ilişki-türü taksonomisi; §3.13 (L196). | `GEREÇ ve YÖNTEM` | pending | pending | `full-text-ok` (zotero-ok) | 2026-07-25 §3.13 karma-yöntem entegrasyonu; önceden Zotero-import + full-text-ok, ch03'e ilk yerleştirme; kanonik joint-display/entegrasyon kaynağı (Fetters, Curry & Creswell 2013 HSR). reliability-ok + cite-ok ch03 /tez-dogrulama kapanışında. |
| `guetterman2015jointDisplay` | Zotero item `5SNNRAR3` (import tablosu; DOI Zotero'da) | `AUG5DCKJ` | PMC (NIH public access) — önceden full-text-ok; joint-display görselleştirme/entegrasyon kanonik. | Birleşik gösterim (joint display) entegrasyon çözümleme aracı olarak; §3.13 (L196). | `GEREÇ ve YÖNTEM` | pending | pending | `full-text-ok` (zotero-ok) | 2026-07-25 §3.13 karma-yöntem entegrasyonu; önceden Zotero-import + full-text-ok, ch03'e ilk yerleştirme; kanonik joint-display kaynağı (Guetterman, Fetters & Creswell 2015). reliability-ok + cite-ok ch03 /tez-dogrulama kapanışında. |
| `simonsohn2020specificationCurve` | DOI: `10.1038/s41562-020-0912-z` | `5A8AS84M`; T1DM Thesis `9ZFDHMZA` (import-doi) | Nat Hum Behav closed; Crossref/DOI kimlik eşleşmesi; specification curve kanonik. | Spesifikasyon-eğrisi/çoklu-evren analizi; §4.5 robustluk (H3) + §4.4.6 H1 çoklu-evren. | `BULGULAR`, `GEREÇ ve YÖNTEM` | 55/55 passed | 144/144 passed | `cite-ok` (identity-doğrulamalı) | 2026-07-14 BULGULAR (04) Kapı 2; import-doi item `5A8AS84M`; ch03 multiverse `steegen2016multiverse` ile tamamlayıcı. |
| `knafl2003fmsf` | DOI: `10.1177/1074840703255435`; OpenAlex `W2096332371` | `X5KVW57E`; note `4UXFF6GH`; T1DM Thesis `9ZFDHMZA` | OpenAlex kimlik doğrulandı; OA kapalı (`is_oa=false`, J Family Nursing/SAGE) → kanonik metodoloji, tanımsal iddia için full-text-exception. | Aile Yönetim Tarzı Çerçevesi (FMSF) aile-düzeyi kuramsal temel; ch03 §Nitel Kol. | `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-13 ch03 FMSF bağlama; Zotero 9ZFDHMZA import + BibTeX key pin (v2947); OA kapalı → tanımsal iddia için full-text-exception. |
| `tracy2010qualityCriteria` | DOI: `10.1177/1077800410383121`; OpenAlex `W2103879113` | `UMB7KAZD`; T1DM Thesis `9ZFDHMZA` | OpenAlex kimlik doğrulandı; OA kapalı (SAGE Qualitative Inquiry) → tanımsal iddia için full-text-exception. | Big-tent sekiz nitel kalite ölçütü; ch03 §Raporlama Standartları ve Güvenilirlik (Lincoln-Guba destek). | `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-13 Zotero import + BibTeX key pin (v2948); OA kapalı → full-text-exception. |
| `birt2016member` | DOI: `10.1177/1049732316654870`; OpenAlex `W2460117687` | `44EP84JB`; T1DM Thesis `9ZFDHMZA` | OpenAlex kimlik doğrulandı; OA kapalı (SAGE Qual Health Research) → tanımsal iddia için full-text-exception. | Member checking (katılımcı doğrulaması); ch03 §Nitel Veri Toplama sınırlılık cümlesi. | `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `cite-ok` | 2026-07-13 Zotero import + BibTeX key pin (v2949); OA kapalı → full-text-exception. |
| `creswellPlanoClark2018` | ISBN: `9781483344379`; SAGE 2018, 3. baskı | Zotero pin bekliyor (DOI'siz kitap; bridge yalnız import-doi) | SAGE kanonik karma-yöntem tasarım kitabı; ISBN kimlik doğrulandı. | Eşzamanlı/convergent karma yöntem tasarımı tipolojisi; ch03 §Araştırma Tasarımı. | `GEREÇ ve YÖNTEM` | 55/55 passed | 142/142 passed | `candidate` (zotero-pending) | 2026-07-13 tasarım kararı convergent/embedded'e hizalandı; kitap Zotero kapatılamadı (import-isbn yok; `kennyKashyCook2006`/`lincolnGuba1985` precedent'i). **Metne @cite ALINMADI** — tasarım cümlesi atıfsız; Zotero kapanınca bağlanacak. |

<!-- CSR bib-wiring toplu ekleme 2026-07-14: referans-kapısı Adım 0-3+6 (workflow doğrulama) -->
| `wolff2019probast` | DOI: `10.7326/M18-1376` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (W2907554860) DOI 10.7326/m18-1376 ile tam eşleşme döndürdü: başlık "PROBAST: A Tool to Assess the Risk of Bias and Applicability of Prediction Model Studies", dergi Annals of Internal Medicine, 9 yazar APA ile birebir. Green OA ta | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI);  |
| `reise2012bifactor` | DOI: `10.1080/00273171.2012.715555` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (W2025929695) ve Semantic Scholar (get_paper) aynı DOI'yi döndürdü: 10.1080/00273171.2012.715555; başlık "The Rediscovery of Bifactor Measurement Models", tek yazar S. P. Reise, 2012, Multivariate Behavioral Research. OpenAlex OA d | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI);  |
| `spirtes2000causation` | DOI: `10.7551/mitpress/1754.001.0001` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex ile doğrulandı: MIT Press eBook kaydı (W4302423442, DOI 10.7551/mitpress/1754.001.0001) ve bir kitap incelemesi kaydı (W1985826111) "Causation, Prediction, and Search, 2nd edn. Peter Spirtes, Clark Glymour, Richard Scheines, MIT Pr | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI);  |
| `koenkerBassett1978quantile` | DOI: `10.2307/1913643` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex ID lookup on 10.2307/1913643 çözüldü: "Regression Quantiles", Econometrica (Wiley), 1978, 12.927 atıf — kantil regresyonun kanonik makalesi. Başlık/yıl/dergi/cilt(46,1)/sayfa(33-50) APA ile birebir eşleşti; APA'da listelenmeyen DOI | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-exception` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI); OA yok (is_oa=false), DOI+metadata connector-doğrulı → exception;  |
| `conger2010ses` | DOI: `10.1111/j.1741-3737.2010.00725.x` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (W1988075665) ve Semantic Scholar birlikte DOI 10.1111/j.1741-3737.2010.00725.x'i, üç yazarı (Rand D. Conger, Katherine J. Conger, Monica J. Martin), 2010 yılını, Journal of Marriage and Family dergisini ve başlığı doğruladı; APA i | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI);  |
| `bakkKuha2021latentExternal` | DOI: `10.1111/bmsp.12227` | — (references.bib-primary; Zotero import onay bekliyor) | PubMed (PMID 33200411) ve Crossref DOI 10.1111/bmsp.12227 doğrulandı: Bakk Z. & Kuha J., Br J Math Stat Psychol 74(2):340-362, 2021 — APA ile tam eşleşme. PMC8247311 açık-erişim tam-metin mevcut. | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI);  |
| `downey1995resourceDilution` | DOI: `10.2307/2096320` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (W2057782860) DOI 10.2307/2096320 ile birebir eşleşti: yazar Downey (Douglas B.), yıl 1995, başlık "When Bigger Is Not Better...", dergi American Sociological Review (SAGE), 958 atıf. open_access.is_oa=false (closed) → paywalled. C | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-exception` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI); OA yok (is_oa=false), DOI+metadata connector-doğrulı → exception;  |
| `ackerman2011positiveEngagement` | DOI: `10.1037/a0025288` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (W1979475315) ve Semantic Scholar (DOI:10.1037/a0025288) DOI'yi çözdü; her ikisi başlık, 2011, Journal of Family Psychology ve yazarları (Ackerman, Kashy, Donnellan, Conger) doğruladı. OpenAlex volume/number/pages 25(5):719-730 APA | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI);  |
| `higgins2011sequential` | DOI: `10.1002/sim.4088` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (title.search) ve PubMed (PMID 21472757) aynı yayını doğruladı: başlık ve üç yazar (Higgins JPT, Whitehead A, Simmonds M) tam eşleşiyor, dergi Statistics in Medicine, DOI 10.1002/sim.4088. Ancak yetkili künye 2011; 30(9):903-921 (e | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI); SEED-DÜZELTME (CSR §21 künyesi hatalıydı, doğru yayın atandı);  |
| `ganzeboomTreiman1996isei` | DOI: `10.1006/ssre.1996.0010` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (W2124242630) ve Semantic Scholar (paperId 4ab716b1...) her ikisi de aynı başlık, yazarlar (H.B.G. Ganzeboom, D.J. Treiman), 1996 yılı, Social Science Research dergisi ve DOI 10.1006/ssre.1996.0010 ile eşleşti; DOI çözülüyor. OpenA | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-exception` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI); OA yok (is_oa=false), DOI+metadata connector-doğrulı → exception;  |
| `hertwig2002parentalInvestment` | DOI: `10.1037/0033-2909.128.5.728` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (W2101734703) tam eşleşme döndürdü: başlık "Parental investment: How an equity motive can produce inequality", 2002, Psychological Bulletin 128(5), DOI 10.1037/0033-2909.128.5.728 doğrulandı; is_oa=true (green), tam-metin PDF MPG P | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI);  |
| `hansen2014agreementChronic` | DOI: `10.1186/1471-2296-15-39` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (W2113260385) DOI 10.1186/1471-2296-15-39 ile birebir çözüldü: başlık, 2014, BMC Family Practice (ISSN 1471-2296), gold OA CC-BY tam metin. PubMed PMID 24580758 aynı başlığı doğruladı. Yazar/yıl/başlık/dergi APA ile tutarlı. | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI);  |
| `eradus2024differentialWarmth` | DOI: `10.1037/fam0001194` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (W4391244023) DOI 10.1037/fam0001194 ile birebir eşleşme: başlık, Journal of Family Psychology, 2024, OA green (UvA Pure repo tam-metni). PubMed (PMID 38271066) beş yazarı ve cilt/sayı/sayfayı (38(3):387-399) doğruladı; Meta-Analys | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI);  |
| `buist2013siblingMeta` | DOI: `10.1016/j.cpr.2012.10.007` | — (references.bib-primary; Zotero import onay bekliyor) | PubMed (PMID 23159327) doğruladı: yazarlar Buist KL, Deković M, Prinzie P; Clin Psychol Rev 33(1):97-106, Feb 2013; DOI 10.1016/j.cpr.2012.10.007 (Meta-Analysis türü). Tüm alanlar APA ile birebir eşleşti. Elsevier paywalled, PMCID yok. | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-exception` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI); OA yok (is_oa=false), DOI+metadata connector-doğrulı → exception;  |
| `dumenci2000mtmm` | DOI: `10.1016/B978-012691360-6/50021-5` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (W1016666186): tam başlık "Multitrait-multimethod Analysis" bölümü "Handbook of Applied Multivariate Statistics and Mathematical Modeling" içinde GERÇEKTEN var (DOI 10.1016/B978-012691360-6/50021-5, s.583-611), ancak yazarı Levent  | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI); SEED-DÜZELTME (CSR §21 künyesi hatalıydı, doğru yayın atandı);  |
| `wysocki2008bfst` | DOI: `10.1016/j.beth.2007.04.001` | — (references.bib-primary; Zotero import onay bekliyor) | PubMed (PMID 18328868) ve OpenAlex ile doğrulandı. PubMed metadata: yazar dizisi (Wysocki, Harris, Buckloh, Mertlich, Lochrie, Taylor, Sadler, White), başlık, Behavior Therapy, cilt 39 sayı 1 s.33-46 tam olarak APA ile eşleşti. APA'da liste | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-exception` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI); OA yok (is_oa=false), DOI+metadata connector-doğrulı → exception;  |
| `cameron2007screening` | DOI: `10.2337/dc07-0603` | — (references.bib-primary; Zotero import onay bekliyor) | PubMed (PMID 17644619) döndürdü: Cameron FJ, Northam EA, Ambler GR, Daneman D; "Routine psychological screening in youth with type 1 diabetes and their parents: a notion whose time has come?"; Diabetes Care 30(10):2716-24; 2007 Oct; DOI 10. | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-exception` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI); OA yok (is_oa=false), DOI+metadata connector-doğrulı → exception;  |
| `makowski2019bayestestr` | DOI: `10.21105/joss.01541` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (W2968619018) doğruladı: DOI 10.21105/joss.01541 çözülüyor; yazar (Makowski, Ben-Shachar, Lüdecke), yıl 2019, başlık, dergi (Journal of Open Source Software), cilt 4, sayı 40, sayfa 1541 APA ile birebir eşleşiyor. OA durumu diamond | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI);  |
| `rumburg2017maternalDistress` | DOI: `10.1111/pedi.12350` | — (references.bib-primary; Zotero import onay bekliyor) | PubMed (PMID 26712240) ve OpenAlex (W2218490829) aynı künyeyi döndürdü: DOI 10.1111/pedi.12350, yazarlar Rumburg TM, Lord JH, Savin KL, Jaser SS; Pediatric Diabetes 18(1):67-70. Baskı sayısı 2017 (online-first 2015-12-29). Tüm alanlar APA i | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI);  |
| `jensenThomsen2024pdt` | DOI: `10.1111/cdev.14091` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (W4392468430) ve PubMed (PMID 38439142) her ikisi de yayini dogruladi: Jensen, A.C. & Thomsen, A.E. (2024), Child Development, cilt 95, sayi 4, DOI 10.1111/cdev.14091 (cozuluyor). Yazar/yil/baslik/dergi/cilt/sayi APA ile tam eslest | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-exception` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI); SEED-DÜZELTME (CSR §21 künyesi hatalıydı, doğru yayın atandı); OA yok (is_oa=false), DOI+metadata connector-doğrulı → exception;  |
| `pedersen2017missingImputation` | DOI: `10.2147/CLEP.S129785` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (id W2607507174, DOI 10.2147/clep.s129785) döndürdü: Alma B. Pedersen, Ellen M. Mikkelsen, Deirdre Cronin-Fenton ve diğerleri (7 yazar), 2017, Clinical Epidemiology, Vol 9, s. 157-166 — küratörlü APA'nın ilk üç yazarı, yıl, dergi v | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI);  |
| `lipsitch2010negativeControls` | DOI: `10.1097/EDE.0b013e3181d61eeb` | — (references.bib-primary; Zotero import onay bekliyor) | PubMed (PMID 20335814) + OpenAlex: 2010'da Tchetgen Tchetgen ile Cohen ortak-yazarlı TEK yayın Lipsitch M, Tchetgen Tchetgen E, Cohen T (2010) "Negative controls: a tool for detecting confounding and bias in observational studies", Epidemio | CSR bib-wiring (§8/§13/§15/§16/§21 metodolojik+klinik atıf) | CSR (bib-wiring) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı workflow doğrulı 2026-07-14 (connector kimlik+DOI); SEED-DÜZELTME (CSR §21 künyesi hatalıydı, doğru yayın atandı);  |

| `rohrer2015birthOrder` | DOI: `10.1073/pnas.1506451112` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex/PNAS kimlik; §21.4 küratörlü künye. | Doğum sırası → kişilik/algı (kaynak-seyrelmesi bağlamı) | CSR §16 (bağlamsal) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-exception` | referans-kapısı 2026-07-14; OA-dışı, DOI+metadata doğrulı. |
| `maas2005sufficient` | DOI: `10.1027/1614-2241.1.3.86` | — (references.bib-primary) | Crossref DOI kimlik doğrulı: Maas & Hox (2005) "Sufficient sample sizes for multilevel modeling", *Methodology* 1(3):86–92. | Çok-düzeyli modelde asıl belirleyici birey değil küme (aile) sayısı; ~240 aile önerilen alt sınırların üzerinde (güç analizi §Örneklem büyüklüğü). | `GEREÇ ve YÖNTEM` | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `cite-ok` (identity-doğrulamalı) | 2026-07-16 GEREÇ ve YÖNTEM güç-analizi genişletmesinde metne bağlandı; klasik metodoloji kaynağı, DOI Crossref ile teyit. |
| `hoenigHeisey2001abusePower` | DOI: `10.1198/000313001300339897` | — (references.bib-primary) | Crossref DOI kimlik doğrulı: Hoenig & Heisey (2001) "The abuse of power", *The American Statistician* 55(1):19–24. | Gözlenen/retrospektif güç, p değerinin bire-bir dönüşümü olduğundan ek bilgi taşımaz; belirsizlik CI/Bayes/TOST ile raporlanır (güç analizi §Örneklem büyüklüğü). | `GEREÇ ve YÖNTEM` | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `cite-ok` (identity-doğrulamalı) | 2026-07-16 GEREÇ ve YÖNTEM'de retrospektif güç eleştirisi için metne bağlandı; DOI Crossref ile teyit. |
| `green2016simr` | DOI: `10.1111/2041-210X.12504` | — (references.bib-primary) | Crossref DOI kimlik doğrulı: Green & MacLeod (2016) "SIMR: An R package for power analysis of GLMMs by simulation", *Methods in Ecology and Evolution* 7(4):493–498. | SEM/çok-düzeyli modeller için simülasyon-temelli hassasiyet (sensitivity) güç çözümlemesi `simr`/`pwr` (güç analizi §Örneklem büyüklüğü). | `GEREÇ ve YÖNTEM` | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `cite-ok` (identity-doğrulamalı) | 2026-07-16 GEREÇ ve YÖNTEM'de simülasyon-temelli güç için metne bağlandı; DOI Crossref ile teyit. |
| `vandenbroucke2007strobe` | DOI: `10.1371/journal.pmed.0040297`; PMID: `17941715`; PMCID: `PMC2020496` | — (references.bib-primary) | PMC açık tam metin; Crossref DOI kimlik doğrulı: Vandenbroucke ve ark. (2007) "STROBE: Explanation and Elaboration", *PLoS Medicine* 4(10):e297. | Epidemiyolojik gözlemsel çalışma raporlama kılavuzu; katılımcı akış şeması gerekçesi (§Araştırma evreni ve örneklem, `@fig-strobe-flow`). | `GEREÇ ve YÖNTEM` | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `cite-ok` (identity-doğrulamalı) | 2026-07-16 GEREÇ ve YÖNTEM'de STROBE akış şeması atfı için metne bağlandı; PMC tam metin + DOI Crossref teyit. |
| `perris1980embu` | DOI: `10.1111/j.1600-0447.1980.tb00581.x` | — (references.bib-primary) | Crossref DOI kimlik doğrulı: Perris ve ark. (1980) "Development of a new inventory for assessing memories of parental rearing behaviour", *Acta Psychiatrica Scandinavica* 61(4):265–274. | EMBU'nun özgün geliştirme kaynağı (§EMBU çerçevesi gelişim tarihi, `@tbl-embu-gelisim`). | `GENEL BİLGİLER` | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `cite-ok` (identity-doğrulamalı) | 2026-07-16 GENEL BİLGİLER EMBU gelişim tarihi için metne bağlandı; DOI Crossref teyit. |
| `arrindell1983embuDimensions` | DOI: `10.1111/j.1600-0447.1983.tb00338.x` | — (references.bib-primary) | Crossref DOI kimlik doğrulı: Arrindell ve ark. (1983) "Psychometric evaluation of an inventory for assessment of parental rearing practices: A Dutch form of the EMBU", *Acta Psychiatrica Scandinavica* 67(3):163–177. **DOI seed-düzeltme:** bib'te önceki `tb06731.x` alakasız makaleye (midazolam RCT) çözülüyordu; doğru `tb00338.x` atandı. | EMBU boyut yapısının psikometrik değerlendirmesi (§EMBU çerçevesi, `@tbl-embu-gelisim`). | `GENEL BİLGİLER` | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `cite-ok` (identity-doğrulamalı) | 2026-07-16 GENEL BİLGİLER'de metne bağlandı; **hatalı DOI Crossref sorgusuyla saptanıp düzeltildi**. |
| `baumrind1971parenting` | DOI: `10.1037/h0030372` | — (references.bib-primary) | Crossref DOI kimlik doğrulı: Baumrind (1971) "Current patterns of parental authority", *Developmental Psychology* 4(1,Pt.2):1–103. | Baumrind ebeveynlik tipolojisi (§Ebeveynlik kuramları tarihsel gelişim, `@tbl-ebeveynlik-kuramlari`). | `GENEL BİLGİLER` | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `cite-ok` (identity-doğrulamalı) | 2026-07-16 GENEL BİLGİLER ebeveynlik kuramları için metne bağlandı; DOI Crossref teyit. |
| `maccobyMartin1983` | ISBN/incollection (Wiley, Handbook of Child Psychology Vol.4, 4. baskı) | — (references.bib-primary) | Kitap bölümü (DOI'siz doğru); Maccoby & Martin (1983) "Socialization in the context of the family", ed. Hetherington & Mussen. | Maccoby-Martin iki-boyutlu ebeveynlik modeli (§Ebeveynlik kuramları, `@tbl-ebeveynlik-kuramlari`). | `GENEL BİLGİLER` | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `cite-ok` (identity-doğrulamalı) | 2026-07-16 metne bağlandı; klasik kitap bölümü, DOI'siz künye doğru. |
| `schaefer1965crpbi` | DOI: `10.2307/1126465` | — (references.bib-primary) | Crossref DOI kimlik doğrulı: Schaefer (1965) "Children's reports of parental behavior: An inventory", *Child Development* 36(2):413–424. | CRPBI ölçek kökeni (§Ebeveynlik kuramları, `@tbl-ebeveynlik-kuramlari`). | `GENEL BİLGİLER` | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `cite-ok` (identity-doğrulamalı) | 2026-07-16 metne bağlandı; DOI Crossref teyit. |
| `schaefer1959circumplex` | DOI: `10.1037/h0041114` | — (references.bib-primary) | Crossref DOI kimlik doğrulı: Schaefer (1959) "A circumplex model for maternal behavior", *Journal of Abnormal and Social Psychology* 59(2):226–235. | Schaefer circumplex modeli (§Ebeveynlik kuramları tarihsel kök, `@tbl-ebeveynlik-kuramlari`). | `GENEL BİLGİLER` | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `cite-ok` (identity-doğrulamalı) | 2026-07-16 metne bağlandı; DOI Crossref teyit. |
| `parker1979pbi` | DOI: `10.1111/j.2044-8341.1979.tb02487.x` | — (references.bib-primary) | Crossref DOI kimlik doğrulı: Parker, Tupling & Brown (1979) "A Parental Bonding Instrument", *British Journal of Medical Psychology* 52(1):1–10. | PBI ölçek kökeni (§Ebeveynlik ölçümü, `@tbl-ebeveynlik-kuramlari`). | `GENEL BİLGİLER` | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `cite-ok` (identity-doğrulamalı) | 2026-07-16 metne bağlandı; DOI Crossref teyit. |
| `darlingSteinberg1993` | DOI: `10.1037/0033-2909.113.3.487` | — (references.bib-primary) | Crossref DOI kimlik doğrulı: Darling & Steinberg (1993) "Parenting style as context: An integrative model", *Psychological Bulletin* 113(3):487–496. | Ebeveynlik stili-bağlam bütünleştirici modeli (§Ebeveynlik kuramları, `@tbl-ebeveynlik-kuramlari`). | `GENEL BİLGİLER` | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `cite-ok` (identity-doğrulamalı) | 2026-07-16 metne bağlandı; DOI Crossref teyit. |
| `beck1988bdiReview` | DOI: `10.1016/0272-7358(88)90050-5` | — (references.bib-primary) | Crossref DOI kimlik doğrulı: Beck, Steer & Garbin (1988) "Psychometric properties of the BDI: Twenty-five years of evaluation", *Clinical Psychology Review* 8(1):77–100. | BDI psikometrik gelişim tarihi (§Beck Depresyon Envanteri). | `GENEL BİLGİLER` | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `cite-ok` (identity-doğrulamalı) | 2026-07-16 metne bağlandı; DOI Crossref teyit. |
| `beck1996bdiII` | kitap (Psychological Corporation, San Antonio TX) | — (references.bib-primary) | BDI-II el kitabı (DOI'siz doğru); Beck, Steer & Brown (1996). | BDI-II revizyon kaynağı (§Beck Depresyon Envanteri gelişim tarihi). | `GENEL BİLGİLER` | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `cite-ok` (identity-doğrulamalı) | 2026-07-16 metne bağlandı; klasik el kitabı, DOI'siz künye doğru. |
| `hamaker2015clpm` | DOI: `10.1037/a0038889` | Zotero key `QGFME3NW` | OpenAlex (W1971772643) kimlik doğrulı; Psychological Methods 20(1). | Cross-lagged panel eleştirisi (boyuna tasarım önerisi §18) | CSR §18 (sınırlılık/gelecek) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-exception` | referans-kapısı 2026-07-14; OA-dışı, connector kimlik. |

<!-- CSR narrative bib-wiring 9 künye 2026-07-14 -->
| `funderOzer2019effectSize` | DOI: `10.1177/2515245919847202` | Zotero key `3UJ393NT` | OpenAlex (W2944339144) and Semantic Scholar both resolve DOI 10.1177/2515245919847202 to title "Evaluating Effect Size in Psychological Research: Sense and Nonsense", authors D. C. Funder & D. J. Ozer, year 201 | CSR narrative in-text atıf | CSR (§10-§18) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı narrative-pas 2026-07-14 (connector kimlik+DOI);  |
| `schafer2019meaningfulness` | DOI: `10.3389/fpsyg.2019.00813` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex W2937326640: title "The Meaningfulness of Effect Sizes in Psychological Research: Differences Between Sub-Disciplines and the Impact of Potential Biases", Frontiers in Psychology, 2019, DOI 10.3389/fps | CSR narrative in-text atıf | CSR (§10-§18) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı narrative-pas 2026-07-14 (connector kimlik+DOI);  |
| `mackinnon2007mediation` | DOI: `10.1146/annurev.psych.58.110405.085542` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex lookup by DOI 10.1146/annurev.psych.58.110405.085542 returns exactly one work: "Mediation Analysis" by David P. MacKinnon, Amanda J. Fairchild, Matthew S. Fritz (all Arizona State University), Annual R | CSR narrative in-text atıf | CSR (§10-§18) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı narrative-pas 2026-07-14 (connector kimlik+DOI);  |
| `preacher2015advances` | DOI: `10.1146/annurev-psych-010814-015258` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (W2140253433), Semantic Scholar (548a8691...), and PubMed (PMID 25148853) all resolve the same work: title "Advances in Mediation Analysis: A Survey and Synthesis of New Developments", single author Kr | CSR narrative in-text atıf | CSR (§10-§18) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı narrative-pas 2026-07-14 (connector kimlik+DOI);  |
| `rijnhart2021mediation` | DOI: `10.1186/s12874-021-01426-3` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (W3210373320) ve Semantic Scholar (DOI:10.1186/s12874-021-01426-3) her ikisi de tam başlık eşleşmesi verdi: "Mediation analysis methods used in observational research: a scoping review and recommendati | CSR narrative in-text atıf | CSR (§10-§18) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı narrative-pas 2026-07-14 (connector kimlik+DOI);  |
| `walterEliasziwDonner1998` | DOI: `10.1002/(SICI)1097-0258(19980115)17:1<101::AID-SIM727>3.0.CO;2-E` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (W2124381750) and PubMed (PMID 9463853) both confirm: title "Sample size and optimal designs for reliability studies"; authors Walter S.D., Eliasziw M., Donner A.; journal Statistics in Medicine; 1998; | CSR narrative in-text atıf | CSR (§10-§18) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-exception` | referans-kapısı narrative-pas 2026-07-14 (connector kimlik+DOI); OA yok, DOI+metadata doğrulı → exception;  |
| `wakelin2025familyInterventions` | DOI: `10.1111/1753-0407.70112` | — (references.bib-primary; Zotero import onay bekliyor) | PubMed PMID 40524654 (queried via pubmed_search_articles + get_article_metadata) confirms the reference. Authors: Wakelin KE, Read RK, Williams AY, Francois-Walcott RR, O'Donnell N, Satherley RM, Harrington MP, | CSR narrative in-text atıf | CSR (§10-§18) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı narrative-pas 2026-07-14 (connector kimlik+DOI);  |
| `steyerbergVergouwe2014` | DOI: `10.1093/eurheartj/ehu207` | — (references.bib-primary; Zotero import onay bekliyor) | OpenAlex (W2154286581) ve PubMed (PMID 24898551) her ikisi de künyeyi tam doğruladı. Başlık birebir eşleşti; yazarlar Steyerberg, Ewout W. & Vergouwe, Yvonne; dergi European Heart Journal; yıl 2014; cilt 35, sa | CSR narrative in-text atıf | CSR (§10-§18) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı narrative-pas 2026-07-14 (connector kimlik+DOI);  |
| `prikken2019` | DOI: `10.1016/j.diabres.2019.03.025` | — (references.bib-primary; Zotero import onay bekliyor) | The explicit author list the user supplied ("Prikken, S., Raymaekers, K., Oris, L., et al.") + year 2019 matches EXACTLY one real paper: PMID 30904747, "A triadic perspective on control perceptions in youth wit | CSR narrative in-text atıf | CSR (§10-§18) | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı narrative-pas 2026-07-14 (connector kimlik+DOI); seed-başlık farkı, doğru yayın connector-teyitli;  |
| `kennyKashyCook2006dyadic` | ISBN: `978-1-57230-986-9` (kitap) | — (references.bib-primary) | Kanonik diadik-veri analizi kitabı (Guilford); connector/kanonik kimlik. | Diadik veri analizi çerçevesi (§11 H5) | CSR §11/§17 | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı narrative-pas 2026-07-14; kitap. |
| `borsboom2021network` | DOI: `10.1038/s43586-021-00055-w` | — (references.bib-primary) | Nature Reviews Methods Primers ağ-analizi; kanonik. | Psikolojik ağ analizi çerçevesi (§16 network) | CSR §16 | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-exception` | referans-kapısı 2026-07-14; kanonik, connector kimlik. |

<!-- CSR §11 klinik-yorum evidence 2026-07-14 -->
| `pinquartKauser2018culture` | DOI: `10.1037/cdp0000149` | — (references.bib-primary) | DOI 10.1037/cdp0000149 resolves consistently across two independent connectors to the target paper. OpenAlex (W2606859482): title "Do the associations of parenting styles with beha | Klinik yorum evidence-deepening (§11) | CSR §11 | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-exception` | referans-kapısı klinik-yorum pas 2026-07-14; connector DOI-teyit. |
| `borelli2010discrepancies` | DOI: `10.1111/j.1939-0025.2010.01044.x` | — (references.bib-primary) | DOI 10.1111/j.1939-0025.2010.01044.x resolves on OpenAlex (W2112351493) to this exact paper. Cross-verified on PubMed (PMID 20636946) and journal metadata. Authors: Borelli JL, Lut | Klinik yorum evidence-deepening (§11) | CSR §11 | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı klinik-yorum pas 2026-07-14; connector DOI-teyit. |
| `vermaes2012siblings` | DOI: `10.1093/jpepsy/jsr081` | — (references.bib-primary) | DOI 10.1093/jpepsy/jsr081 resolves consistently across three connectors to the same work. OpenAlex (W2102841024): title "Psychological Functioning of Siblings in Families of Childr | Klinik yorum evidence-deepening (§11) | CSR §11 | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı klinik-yorum pas 2026-07-14; connector DOI-teyit. |
| `barlowEllard2006chronic` | DOI: `10.1111/j.1365-2214.2006.00591.x` | — (references.bib-primary) | DOI 10.1111/j.1365-2214.2006.00591.x resolves consistently across OpenAlex (W2013160749), Semantic Scholar (paperId 0204f79f...), confirming: authors Jane H. Barlow + David R. Ella | Klinik yorum evidence-deepening (§11) | CSR §11 | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı klinik-yorum pas 2026-07-14; connector DOI-teyit. |
| `deLosReyes2011discrepancies` | DOI: `10.1080/15374416.2011.533405` | — (references.bib-primary) | DOI 10.1080/15374416.2011.533405 resolves to OpenAlex W2157039680 and PubMed PMID 21229439 — the same work. Author: De Los Reyes, Andres (single author, University of Maryland). Ye | Klinik yorum evidence-deepening (§11) | CSR §11 | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-exception` | referans-kapısı klinik-yorum pas 2026-07-14; connector DOI-teyit. |
| `sattoe2012proxy` | DOI: `10.1186/1477-7525-10-10` | — (references.bib-primary) | DOI 10.1186/1477-7525-10-10 resolves identically across three independent connectors. OpenAlex (W2125135097): title "The proxy problem anatomized: child-parent disagreement in heal | Klinik yorum evidence-deepening (§11) | CSR §11 | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı klinik-yorum pas 2026-07-14; connector DOI-teyit. |
| `luo2025maternalDepression` | DOI: `10.1007/s10964-025-02284-8` | — (references.bib-primary) | DOI 10.1007/s10964-025-02284-8 resolves consistently across three independent connectors: OpenAlex (W4416022275), Semantic Scholar (70cf3ace...), and PubMed (PMID 41205139). Author | Klinik yorum evidence-deepening (§11) | CSR §11 | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-exception` | referans-kapısı klinik-yorum pas 2026-07-14; connector DOI-teyit. |
| `papp2022informant` | DOI: `10.1080/08870446.2022.2057496` | — (references.bib-primary) | DOI 10.1080/08870446.2022.2057496 resolves across three independent connectors to one article: OpenAlex W4220810790 (publication_year 2022, biblio vol 39 issue 2 pp 233-251, journa | Klinik yorum evidence-deepening (§11) | CSR §11 | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-exception` | referans-kapısı klinik-yorum pas 2026-07-14; connector DOI-teyit. |
| `liskola2021informant` | DOI: `10.1186/s13034-021-00396-0` | — (references.bib-primary) | DOI 10.1186/s13034-021-00396-0 resolves consistently across OpenAlex (W3133525682) and PubMed (PMID 34425862, PMC8383450). Author list matches exactly: Liskola K, Raaska H, Lapinle | Klinik yorum evidence-deepening (§11) | CSR §11 | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-ok` | referans-kapısı klinik-yorum pas 2026-07-14; connector DOI-teyit. |
| `lancaster2015concordance` | DOI: `10.1037/fsh0000092` | — (references.bib-primary) | DOI 10.1037/fsh0000092 resolves via OpenAlex (W2325391832) to a single work: "Association between diabetes treatment adherence and parent-child agreement regarding treatment respon | Klinik yorum evidence-deepening (§11) | CSR §11 | bölüm kapanışında (WS-D) | bölüm kapanışında (WS-D) | `full-text-exception` | referans-kapısı klinik-yorum pas 2026-07-14; connector DOI-teyit. |

| `cusson2020evalue` | DOI: `10.1093/ije/dyaa127` | — (references.bib-primary) | DOI 10.1093/ije/dyaa127 resolves identically across three independent sources. OpenAlex W3091170675: title "Bias factor, maximum bias and the E-value: | Klinik yorum evidence (batch-1 §9-14) | CSR §9-§14 | bölüm kapanışında | bölüm kapanışında | `full-text-ok` | referans-kapısı 2026-07-14 batch-1. |
| `wang2023evalue` | DOI: `10.1097/CORR.0000000000002528` | — (references.bib-primary) | DOI 10.1097/CORR.0000000000002528 resolves in OpenAlex (W4318920297) and PubMed (PMID 36728049) to a single real article. First author Chien-Wei Wang  | Klinik yorum evidence (batch-1 §9-14) | CSR §9-§14 | bölüm kapanışında | bölüm kapanışında | `full-text-ok` | referans-kapısı 2026-07-14 batch-1. |
| `simonsohn2015specification` | DOI: `10.2139/ssrn.2694998` | — (references.bib-primary) | DOI 10.2139/ssrn.2694998 resolves via OpenAlex (W2174191405) to exactly this SSRN working paper. Authors confirmed: Uri Simonsohn (ORCID 0000-0002-860 | Klinik yorum evidence (batch-1 §9-14) | CSR §9-§14 | bölüm kapanışında | bölüm kapanışında | `superseded` | referans-kapısı 2026-07-14 batch-1. **2026-07-21: aynı çalışmanın hakemli VoR'una (`simonsohn2020specificationCurve`, Nat Hum Behav 2020;4(11):1208–1214, doi 10.1038/s41562-020-0912-z; Crossref-doğrulandı) taşındı; CSR §13.6 in-text atıf VoR'a güncellendi; SSRN preprint künyesi references.bib'den kaldırıldı (bib-orphan). SOFT AMA-11 volume/pages bayrağı böylece kapandı.** |
| `duru2016qolT1dm` | DOI: `10.1055/s-0035-1555938` | — (references.bib-primary) | DOI 10.1055/s-0035-1555938 resolves in OpenAlex (W2289085298) and PubMed (PMID 26285067) to the same article. Authors Duru NS, Civilibal M, Elevli M ( | Klinik yorum evidence (batch-1 §9-14) | CSR §9-§14 | bölüm kapanışında | bölüm kapanışında | `full-text-exception` | referans-kapısı 2026-07-14 batch-1. |
| `pinquart2019ptss` | DOI: `10.1002/jts.22354` | — (references.bib-primary) | DOI 10.1002/jts.22354 uc kaynakta da ayni gercek yayina cozuluyor: OpenAlex W2911697804 (count=1, tam eslesme), PubMed PMID 30688373, Semantic Scholar | Klinik yorum evidence (batch-1 §9-14) | CSR §9-§14 | bölüm kapanışında | bölüm kapanışında | `full-text-exception` | referans-kapısı 2026-07-14 batch-1. |
| `zhang2020sensitivity` | DOI: `10.1002/pds.5117` | — (references.bib-primary) | DOI 10.1002/pds.5117 resolves to a real work across three independent sources. OpenAlex (W3087582330): title "Assessing the impact of unmeasured confo | Klinik yorum evidence (batch-1 §9-14) | CSR §9-§14 | bölüm kapanışında | bölüm kapanışında | `full-text-ok` | referans-kapısı 2026-07-14 batch-1. |
| `yangzong2016tibetanEmbu` | DOI: `10.2147/PRBM.S111073` | — (references.bib-primary) | DOI 10.2147/PRBM.S111073 resolves to a genuine article on both OpenAlex (W2562989573) and PubMed (PMID 28053560, PMC5189697). Title matches exactly: " | Klinik yorum evidence (batch-1 §9-14) | CSR §9-§14 | bölüm kapanışında | bölüm kapanışında | `full-text-ok` | referans-kapısı 2026-07-14 batch-1. |
| `kruschke2017bayesian` | DOI: `10.3758/s13423-016-1221-4` | — (references.bib-primary) | OpenAlex DOI lookup resolved to W3124625789 with exact title "The Bayesian New Statistics: Hypothesis testing, estimation, meta-analysis, and power an | Klinik yorum evidence (batch-1 §9-14) | CSR §9-§14 | bölüm kapanışında | bölüm kapanışında | `full-text-ok` | referans-kapısı 2026-07-14 batch-1. |
| `heinrich2021pfactor` | DOI: `10.1177/10731911211060298` | — (references.bib-primary) | DOI 10.1177/10731911211060298 resolves consistently across OpenAlex (W3216909787), Semantic Scholar (paperId 5e99f0d8...), to a real published article | Klinik yorum evidence (batch-1 §9-14) | CSR §9-§14 | bölüm kapanışında | bölüm kapanışında | `full-text-ok` | referans-kapısı 2026-07-14 batch-1. |
| `floresKanter2018bifactor` | DOI: `10.35670/1667-4545.v18.n3.22221` | — (references.bib-primary) | DOI 10.35670/1667-4545.v18.n3.22221 resolves in OpenAlex (W2909338852) and Semantic Scholar (5be49c77) to a single work: "Best Practices in the Use of | Klinik yorum evidence (batch-1 §9-14) | CSR §9-§14 | bölüm kapanışında | bölüm kapanışında | `full-text-ok` | referans-kapısı 2026-07-14 batch-1. |
| `katz2014t1dmFamily` | DOI: `10.1111/pedi.12065` | — (references.bib-primary) | DOI 10.1111/pedi.12065 çözüldü — üç bağımsız kaynakta aynı yayın. OpenAlex W1845551963: "Family-based psychoeducation and care ambassador intervention | Klinik yorum evidence (batch-1 §9-14) | CSR §9-§14 | bölüm kapanışında | bölüm kapanışında | `full-text-ok` | referans-kapısı 2026-07-14 batch-1. |
## 2026-07-06 GENEL BİLGİLER Tümü — Hedefli Zenginleştirme + Reorganizasyon Notu

Bölümün kalan alt bölümleri (kronik hastalık, aile sistemi, ebeveynlik kuramları,
EMBU, T1DM ebeveynlik, anne depresif belirtileri ve yolları, kardeş, KİA/SRQ,
SES, demografik, ölçüm, psikometri, çoklu bilgi kaynağı, diadik/triadik, karma
yöntem, yorum sınırları, etik, sentez) denetlendi. Çoğu alt bölüm §2.1–2.3 ile
aynı yoğunlukta kanıtlıydı; **yalnız gerçek boşluklara** dört yeni PMC-OA kaynak
eklendi (padding'den kaçınıldı): `fang2025techDisparities` (SES), `lansingBerg2014selfRegulation`
(kronik hastalık, compas tekelini dengeler), `ferro2022informantAgreement` (informant
uyumu), `wong2023dyadicSatisfaction` (T1DM diadik). Ayrıca zaten `cite-ok` olan
`deLosReyes2015` diadik uyum alt bölümüne dokundu. Dördü de iki-kol AI-reliability
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
eklendi ve hepsi iki-kol AI-reliability (55/55 + 142/142) geçip `cite-ok` oldu:
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
Beş yeni dış referans bu oturumda tam metni doğrulanıp iki-kol AI-reliability
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
dış referans tam metni PMC-OA ile doğrulanıp iki-kol AI-reliability geçti ve
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
kanonik nitel sonuç raporu (`niteliksel/qualitative_canonical_results_report.md`).

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
(OpenAthens → Anna's → PMC/OA), Zotero item key mutabakatı ve iki-kol AI-reliability
kapıları henüz kapatılmadı. Bölüm bu nedenle **taslak/`provisional`** statüsündedir;
finalizasyon için `04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`
(Kapı 0-5) ve açık uygulama onayı gerekir. Bu dört referans yaygın-kabul görmüş
metodoloji standartlarıdır (RTA, bilgi gücü, COREQ); tam-metin kapısı finalizasyonda
kapatılacaktır.

## 2026-07-07 GEREÇ ve YÖNTEM — Nitel Metodoloji Referansları KAPI KAPANIŞI

Kullanıcı talimatıyla (tam-metin + Zotero + iki-kol AI-reliability) nitel metodoloji
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
| `lincolnGuba1985` | — (kitap; DOI yok; Naturalistic Inquiry, SAGE 1985) | Anna's Library md5 `d90d2fd517c2593c0d50d6c2a5f22ac5` (pdf, 421 s., text_quality=ok); kanonik kitap kimlik + tam metin doğrulandı (2026-07-13) | **Zotero import bekliyor** (DOI'siz; ISBN ile elle eklenecek; bridge yalnız import-doi destekler) | 142/142 + 55/55 PASS | `full-text-ok` (zotero-pending) |

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
- **Deterministik/repo:** sci-audit axis G üç bölümde de 0 blocker; iki-kol AI-reliability
  142/142 + 55/55; `git diff --check` temiz; `quarto check` OK. Harici servise yalnız
  yayımlanmış bibliyografik künye gönderildi (KVKK; `99_ai_use_log` güncellendi).

## 2026-07-12 Pinquart 2013 Minerva-404 Tetiklemeli Yeniden Doğrulama Notu

Minerva vectorstore CSR iddia-doğrulama koşusunda `pinquart2013`
(DOI `10.1093/jpepsy/jst020`) için `minerva_literature_fulltext_by_doi`
**404** döndürdü (kaynak Roche Minerva korpusunda aynalı değil). Bu, ledger
durumunu değiştirmez; kaynak zaten 2026-07-01'de MK OpenAthens → OUP resmi
HTML rotasıyla `cite-ok` sertifikalıdır. Minerva-404 yalnız o korpusun
kapsam boşluğudur, kaynağın geçerliliğine dair kanıt değildir.

Doktrin tam-metin cascade'i bu turda yeniden yürütüldü:

1. **OpenAthens (Tier 3, lisanslı-öncelikli):** Plugin `openathens` connector'ı
   HTTP 401 (Bearer kapısı aktif/beklenen). Ancak bu ortamda
   `OPENATHENS_MCP_API_KEY` `.env`'de **yok** (yalnız ham
   `OPENATHENS_USERNAME/PASSWORD/LOGIN_URL/INSTITUTION` +
   `MILLET_KUTUPHANESI_DATABASES_URL` mevcut) → MCP köprüsü kimlik
   doğrulayamadı. 2026-07-01 OUP HTML rotası (interaktif SSO) hâlâ birincil
   full-text kaynağıdır.
2. **Anna's Archive (Tier 5, son çare):** `annas-reader` connector CANLI
   (`annas-mcp v3.4.2`, `ANNAS_MCP_API_KEY` set). `article_search`
   DOI kaydını doğruladı (başlık/yazar/dergi/yıl birebir); `read_article`
   yine **404** (tam-metin PDF Anna aynasında yok — 2026-07-01 ile tutarlı).
3. **Europe PMC (keyless, legal, otoriter — özet katmanı):** PMID `23660152`
   abstract'ı çekildi ve CSR'daki üç kullanım noktasındaki (§bağlamsal dayanak,
   H3 Bayesçi prior, H1 örtüşme) tüm sayısal iddialar **birebir doğrulandı**:
   *"Based on 325 included studies"* (325 çalışma ✅),
   *"parent-child relationship … g = -.16"* (g = −0,16 ✅),
   *"overprotection (g = .39)"* (aşırı koruma g = 0,39 ✅),
   sayfa 708-721 · cilt 38(7) ✅ · DOI/PMID ✅ — `references.bib` künyesiyle tam uyum.

**Sonuç:** `pinquart2013` `cite-ok` korunur. CSR'daki özet-düzeyli meta-analitik
dayanak (325 çalışma; parent-child g = −0,16; overprotection g = 0,39) otoriter
Europe PMC abstract'ıyla teyitlidir; Minerva-404 dokümanı bloklamaz. Harici
servislere yalnız yayımlanmış DOI/künye + arama terimi gönderildi (KVKK).

## 2026-07-12 OpenAthens MCP Connector Kurulumu + Tier 3 Yeniden Deneme

Yukarıdaki 2026-07-12 notunda OpenAthens MCP'sinin `OPENATHENS_MCP_API_KEY`
eksikliğinden 401 verdiği belirlenmişti. `MCP-TALIMATLAR.md` §4 uyarınca
evidentia plugin `openathens` connector'ının (self-host
`https://openathens.cureonics.com/mcp`) Bearer anahtarı `.env`'e eklendi
(`OPENATHENS_MCP_API_KEY`, 64 hex). `.bashrc` `.env` auto-load mekanizması
sayesinde Claude Code oturumunda connector artık **✔ Connected**
(`claude mcp list`: openathens + annas-reader + minerva-evidence +
galileo-audit + zotero-refs beşi de canlı). Güvenlik: `MCP-TALIMATLAR.md`
(gerçek connector sırları içerir) `.gitignore`'a eklendi; `.env` zaten ignored.

**OpenAthens Tier 3 (lisanslı) yeniden deneme — Pinquart 2013:**

- `oa_server_info` → institution `Cumhurbaşkanlığı Millet Kütüphanesi`,
  redirector `go.openathens.net/redirector/mk.gov.tr` (SAML kapısı aktif).
- `oa_resolve(10.1093/jpepsy/jst020)` → redirector access URL üretildi.
- `oa_fetch_fulltext(10.1093/jpepsy/jst020)` → **`manual_required`**
  (`auth_failed: publisher SSO/JS-challenge not cleared at
  academic.oup.com/SHIBBOLETH`). OUP anti-bot Shibboleth otomatik geçilemedi —
  doktrinle tutarlı (anti-bot yayıncı → `manual_required` deep-link). 2026-07-01
  interaktif SSO ile açılan resmi OUP HTML rotası hâlâ birincil full-text
  kaynağıdır; otomatik headless fetch bu yayıncıda kapalıdır.

**Sonuç:** OpenAthens MCP operasyonel; connector-seviyesi kurulum tamamlandı.
Pinquart 2013 tam-metni bu yayıncıda yalnız interaktif SSO ile açılır
(2026-07-01 `cite-ok` sertifikası geçerli). Sayısal iddialar zaten otoriter
Europe PMC abstract'ıyla teyitli olduğundan durum değişmez.

## TARTIŞMA ve SONUÇ — Derin-Lit Toplu Kapı (2026-07-13)

> **2026-07-14 zahidi2019 tam-metin → 41/41 tam-metin TAMAM:** kullanıcı zahidi2019 OA PDF'ini `eksikler/`'e sağladı (digitalcommons bot-koruması WebFetch/openathens/curl'ü engellemişti). Hedefli sayı çıkarımı: tam-sample öz-rapor↔gözlem r=−0,03..0,08; tedavi-alan alt-grup r=−0,23..0,11, tedavi-almayan r=0,03..0,15 — hiçbiri anlamlı değil (araçlar CAIC/PICCOLO vs APQ). Böylece **41 ampirik referansın TAMAMI tam-metin**-doğrulanmış (34 ilk+gap turları, 3 Minerva-RoMine, 3 OUP PDF, 1 zahidi PDF). Telif: yalnız istatistik/olgu çıkarıldı; telifli PDF'ler .gitignore'da, commit edilmedi; metne verbatim pasaj taşınmadı.

> **2026-07-14 OUP PDF turu (40/41 tam-metin):** kullanıcı 3 OUP J Pediatr Psychol tam-metin PDF'ini (kurumsal erişim) `eksikler/` altında sağladı; hedefli SAYI çıkarımı yapıldı (telifli verbatim kopya yok, PDF'ler .gitignore'da — commit edilmez). Yeni tam-metin sayıları metne işlendi: **pinquart2013** diyabet alt-grubu (k=16) ebeveyn-çocuk ilişkisi g=−0,23 (%95 GA −0,43;−0,04) anlamlı; **pinquart2011** informant-çifti g=0,46 (ebeveyn)/0,37 (öğretmen)/0,17 (çocuk öz-bildirim), GA örtüşmez; **barryMenkhaus2020** ICC 0,787/0,781 + %16,1 izlem teyit. Tam-metin erişimi **40/41**; yalnız zahidi2019 abstract-teyit (openathens, sayıları doğru). Böylece 41 ampirik kaynağın tümünün metindeki sayıları tam-metin/abstract-teyitli.

> **2026-07-14 annas+openathens yeniden tarama (kalan 4):** annas JPP holdingleri 2007'de bitiyor (2011/2013/2020 ciltleri yok), read_article 404. **zahidi2019 → openathens OK** (digitalcommons OA; abstract teyit: n=133, öz-rapor↔gözlem r=−0,03–0,08 anlamsız — metindeki değerlerle birebir, düzeltme gerekmedi). **3 OUP J Pediatr Psychol kaynağı** (pinquart2013, pinquart2011behaviorProblems, barryMenkhaus2020) → academic.oup.com **Shibboleth challenge_required** (yalnız noVNC insan-çözümüyle açılır; annas+RoMine korpusunda yok). Bu 3'ün metindeki g/ICC değerleri abstract-kaynaklı ve doğru; tam-metin tablo (hastalık-özgü g + informant-çifti GA) VNC gerektiriyor. Efektif tam-metin: 37/41 + zahidi abstract-teyit.

> **2026-07-14 Minerva-RoMine turu (37/41 tam-metin):** evidentia v2.3.1 bu oturumda uygulanamadı (marketplace kaynağı 404; MCP restart-required) ve openathens hâlâ v0.1.0 Elsevier'de challenge_required veriyor. Ancak Minerva-RoMine köprüsü (`scripts/mcp/minerva_evidence_bridge.py`, RoMine full-text API, 26,5M dok) openathens'in çekemediği 3 Elsevier/ScienceDirect tam metnini getirdi: lovejoy2000, arrindell1999, elhabashy2023 → tam-metin erişimi 34→**37/41**. Tam-metin doğruluk düzeltmesi: **elhabashy2023 abstract'ındaki '%38' gövdeyle uyuşmadı** — SDQ ebeveyn-raporu küçük kardeş %18 (9/50) + öz-rapor büyük kardeş %20 (10/50); metin buna göre düzeltildi (tam-metin önceliği). Kalan **4 kaynak abstract-düzeyi** (RoMine korpusunda yok): pinquart2013, pinquart2011behaviorProblems, barryMenkhaus2020 (OUP J Pediatr Psychol) + zahidi2019 (küçük OA dergi). KVKK: RoMine'a yalnız DOI gönderildi.

> **2026-07-27 P5 tam-metin re-teyit:** Tartışma P5 denetiminde elhabashy2023 %18/%20 alt-grup değerleri bağımsız kaynaklarda (Unpaywall/EuropePMC/SemanticScholar/Crossref) doğrulanamadı; yalnız abstract %38 agregatı erişilebilirdi. Kullanıcının sağladığı yerel tam-metin PDF (s. e518, "Siblings' behavioral concerns and psychosocial functioning") tez metnini **birebir teyit etti**: "SDQ parent reports, 18% of younger siblings (n = 9 out of 50)" + "SDQ self-reports, 20% (n = 10 out of 50) of older siblings". Abstract'taki %38 iki alt-grubun birleşimi. Ledger durumu `full-text-exception` → `full-text-ok`. Kanıt-değeri değişmedi; metne dokunulmadı.

> **2026-07-14 gap-kapatma turu:** Abstract-only kalan 17 referans için agresif çoklu-rota tam-metin fan-out'u (Workflow wfe4vt06h). 10/17 tam-metne ulaşıldı → toplam **35/41 tam-metin**. Yeni tablo-düzeyi somut sayılar tartışmaya işlendi (sahin2015 PARI alt-ölçekleri, jaser2007 Sobel-aracılık, pinquart2017 boyut-r'leri, sharpe2002 Mz+alt-grup, kirchhofer2025 SEM-B, devins1997 F-testleri, arrindell2005/naivarSen2020 α'ları). **Hâlâ paywall-gap (7):** pinquart2013, pinquart2011, zahidi2019, lovejoy2000, elhabashy2023, barryMenkhaus2020, arrindell1999 — OUP/Elsevier/ScienceDirect Shibboleth insan-VNC gerektiriyor; bu kaynaklar abstract/özet-düzeyi sayılarla (uydurma yok) kaldı. Bibliyografik kimlik+claim+Zotero tüm 42'de tam; durum `reliability-ok` korunur.

> **2026-07-13 tam-metin derinleşme:** 41 ampirik referans için tam-metin çalışma-kartı fan-out'u koşuldu (minerva→openathens→annas→anamnesis); 25/41 tam-metin erişildi, kalanı abstract+metadata. Tartışma her ampirik atıfta çalışma tasarımı+N+somut sonuç (sayılarla) taşıyacak biçimde yeniden dokundu. Dürüst düzeltmeler: zahidi2019 (öz-rapor↔gözlem r≈0, adli örneklem→transfer sınırı), sahin2015 (PARI/otoriter, EMBU/reddetme değil), streisand2014 (yük öz-raporda %21-24 görünür → H3 EMBU-P-spesifik yeniden çerçevelendi), dinleyici2019 (diyabet alt-grup psikososyal QoL kontrolden düşük değil). Somutlaştırma bibliyografik kimliği/claim'i değiştirmez; durum `reliability-ok` korunur.

42 yeni künye Faz-C referans kapısından geçirildi (BibTeX fan-out: pubmed-epmc/openalex ile DOI/PMID çözüldü, kanonik metadata + claim doğrulandı; Zotero Web API ile 9ZFDHMZA koleksiyonuna import edildi, bibtex-key pin'lendi). bib_hygiene: HARD atıflı-tanımsız 0, bad_doi 0, dup_doi 0; render 0 çözümsüz atıf. **Durum `reliability-ok`** (bibliyografik kimlik + claim + Zotero item-key + iki-kol AI-reliability). İki-kol: nitel `t1dm-qual-ai-audit` **55/55 PASS**; nicel hook-sözleşme 14/14 + R-yönetişim 3/3 + `claim_check` atıf-temellendirme PASS. NOT: doktoratezi-ai-audit paketi 134/142 — 8 başarısız = **önceden var olan, TARTIŞMA-dışı hook-drift** (uncommitted pre_tool_use_policy.py); atıf/veri-sınırı/nitel katmanları tam PASS. `cite-ok` stamp'i bu harici hook-drift iş akışı çözülünce (142/142) verilecek. zahidi2019 başlık-düzeyi teyit (tam-metin önerilir).

| Citation key | DOI | PMID | Zotero item key | Claim | Durum |
|---|---|---|---|---|---|
| `barryMenkhaus2020t1dScreening` | `10.1093/jpepsy/jsz089` | 31769852 | `KCV6RENC` | destekli | `reliability-ok` |
| `branje2003srmFamilyPerception` | `10.1111/1467-6494.t01-1-00001` | — | `GIX6SU62` | destekli | `reliability-ok` |
| `clarkWatson1995validity` | `10.1037/1040-3590.7.3.309` | — | `JTAXSMUX` | destekli | `reliability-ok` |
| `commissariat2016identity` | `10.1177/1049732316628835` | 26893304 | `62DZUZR8` | destekli | `reliability-ok` |
| `deLosReyes2021needsGoals` | `10.1016/j.cpr.2021.102114` | 35066239 | `ZTZHETI5` | destekli | `reliability-ok` |
| `deLosReyesKazdin2005` | `10.1037/0033-2909.131.4.483` | 16060799 | `CQN4E99W` | destekli | `reliability-ok` |
| `devins1997illnessintrusiveness` | `10.1007/BF02895149` | 9706357 | `H4K2B3R3` | destekli | `reliability-ok` |
| `dinleyici2019siblingQoLTurkiye` | `10.4274/balkanmedj.galenos.2019.2019.7.142` | 31647208 | `UBHAJRSK` | destekli | `reliability-ok` |
| `eid2017bifactorS1` | `10.1037/met0000083` | — | `3DT33NWW` | destekli | `reliability-ok` |
| `eisinga2013twoItem` | `10.1007/s00038-012-0416-3` | — | `MRXFXWIP` | destekli | `reliability-ok` |
| `epskampFried2018ggm` | `10.1037/met0000167` | — | `I9THSMDZ` | destekli | `reliability-ok` |
| `goodman2011maternalMetaanalytic` | `10.1007/s10567-010-0080-1` | 21052833 | `BZVWR5ZQ` | destekli | `reliability-ok` |
| `haugstvedt2011` | `10.1111/j.1399-5448.2010.00661.x` | 20522171 | `NABHAITS` | destekli | `reliability-ok` |
| `imaiKeeleYamamoto2010mediationDuyarlilik` | `10.1214/10-sts321` | — | `QFFM9V5M` | destekli | `reliability-ok` |
| `jaser2007t1dmMediators` | `10.1093/jpepsy/jsm104` | 17991690 | `8HRQ8WC2` | destekli | `reliability-ok` |
| `kirchhofer2025sibsRiskModel` | `10.1093/jpepsy/jsaf017` | 40327755 | `AJVPQUWC` | destekli | `reliability-ok` |
| `koo2016iccGuideline` | `10.1016/j.jcm.2016.02.012` | 27330520 | `48GRT55K` | destekli | `reliability-ok` |
| `lakens2018esdegerlik` | `10.1177/2515245918770963` | — | `WT4EM6HE` | destekli | `reliability-ok` |
| `lakens2018nullBF` | `10.1093/geronb/gby065` | 29878211 | `B7GGFG65` | destekli | `reliability-ok` |
| `leung2021fourIs` | `10.1111/dme.14443` | 33107064 | `K2N95DN8` | destekli | `reliability-ok` |
| `li2012sEmbuChinese` | `10.2466/02.08.09.21.PR0.110.1.263-275` | 22489392 | `4V9XWUUX` | destekli | `reliability-ok` |
| `lindstrom2017missionimpossible` | `10.1016/j.pedn.2017.06.002` | 28888496 | `XFWCEAC9` | destekli | `reliability-ok` |
| `long2018cancerSibReview` | `10.1002/pon.4669` | 29441699 | `W55BJQ83` | destekli | `reliability-ok` |
| `macaulay2020parentalsleep` | `10.1080/15402002.2019.1647207` | 31370700 | `EVIXSMAR` | destekli | `reliability-ok` |
| `maxwellCole2011crossMediation` | `10.1080/00273171.2011.606716` | — | `Q5Z6PCIE` | destekli | `reliability-ok` |
| `mcneishWolf2020toplamPuan` | `10.3758/s13428-020-01398-0` | — | `2PW4EHWA` | destekli | `reliability-ok` |
| `morsbachPrinz2006` | `10.1007/s10567-006-0001-5` | 16636897 | `7ZWQPPVM` | destekli | `reliability-ok` |
| `naivarSen2020embuTurkey` | `10.3390/ijerph17072176` | 32218210 | `48WQ2EMH` | destekli | `reliability-ok` |
| `nylund2007sinifSayisi` | `10.1080/10705510701575396` | — | `J27KEICW` | destekli | `reliability-ok` |
| `otonomiEbeveynlikProfilleri2021` | `10.1007/s10964-021-01538-5` | — | `KGQNVHSZ` | destekli | `reliability-ok` |
| `penelo2010embucClinical` | `10.1016/j.comppsych.2009.08.003` | 20579519 | `CI3UXP22` | destekli | `reliability-ok` |
| `penelo2012sEmbuAdolescent` | `10.1016/j.comppsych.2011.01.009` | 21397217 | `QX73FWJD` | destekli | `reliability-ok` |
| `pinquart2011behaviorProblems` | `10.1093/jpepsy/jsr042` | 21810623 | `QKE2ADJA` | destekli | `reliability-ok` |
| `rad2023siblingDynamics` | `10.3390/children10030587` | 36980145 | `NTXZHZVP` | destekli | `reliability-ok` |
| `sijtsma2009alpha` | `10.1007/s11336-008-9101-0` | — | `IKPE9A82` | destekli | `reliability-ok` |
| `tavakolDennick2011alpha` | `10.5116/ijme.4dfb.8dfd` | — | `T2GSXXPC` | destekli | `reliability-ok` |
| `uludasdemir2026motherfather` | `10.1002/nop2.70673` | 42433195 | `EUHG2XDR` | destekli | `reliability-ok` |
| `vanBorkulo2022nct` | `10.1037/met0000476` | 35404628 | `WSIDBP9S` | destekli | `reliability-ok` |
| `vickersElkin2006dca` | `10.1177/0272989X06295361` | 17099194 | `H6EZZPIT` | destekli | `reliability-ok` |
| `waiteJones2020medicalcareermother` | `10.1111/bjhp.12409` | 32150659 | `EZHEHNNV` | destekli | `reliability-ok` |
| `webster2018siblingcaringroles` | `10.1111/1467-9566.12627` | 29023907 | `H992RQ3D` | destekli | `reliability-ok` |
| `zahidi2019` | `10.20429/jgpha.2019.070217` | — | `S7JQIQT9` | destekli | `reliability-ok (full-text-exception)` |

## 2026-07-14 TÜM-KÜTÜPHANE Tam-Metin Denetimi + Kapanış Turu

Kullanıcı talebiyle Zotero `T1DM Thesis` (9ZFDHMZA) kütüphanesi uçtan uca denetlendi (ledger-iddia × Zotero-gerçek çapraz-denetim, şema-duyarlı ayrıştırma; salt-okunur denetim betiği). Bulgu: 158 top-level item'ın yalnız 64'ü tam (koleksiyon+attachment+note) idi; 6 cite-ok item attachment'sız, 11 item koleksiyon-dışı, 35 item ledger'da item-key ile izlenmiyordu, 12 kaynak pin bekliyordu. Eksiksiz kapsam kararıyla tam-metin kampanyası yürütüldü.

**Sonuç:** 57 kaynak işlendi — **48 tam-metin doğrulandı** (EuropePMC OA / PMC NIH-public-access / annas-reader Crossref-doğrulamalı), **9 dürüst-boşluk** (OA yok + annas erişemedi / OpenAthens VNC-gated; yayıncı DOI sayfası bağlandı, tam metin bu turda alınamadı). Her kaynak 9ZFDHMZA koleksiyonuna eklendi, BibTeX key pinlendi, tarihli provenance note yazıldı. Dublike item oluşmadı (import-doi find-or-create; doğrulama: top-level 158→174 = +11 koleksiyona-eklenen +5 yeni-oluşan, child +114 = 57×2). KVKK: yalnız literatür DOI/metadata dış servise gitti; telifli tam metin bağlama dökülmedi (kimlik-doğrulama amaçlı sayfa-1 kontrolü).

### Tam metin doğrulanan (full-text-ok)

| Citation key | Zotero item key | Attachment | Rota | Durum |
|---|---|---|---|---|
| `achenbach1987crossinformant` | `ZCATXNZB` | `3IMWJI5S` | annas-reader | `full-text-ok` |
| `adams1991siblings` | `2Q2AX4F7` | `MXMV8QSX` | annas-reader | `full-text-ok` |
| `affrunti2015maternal` | `556JEIZW` | `GNVMXEP4` | annas-reader | `full-text-ok` |
| `azimi2024caregiver` | `T4QA46S4` | `T2KWKNIE` | EPMC/PMC OA | `full-text-ok` |
| `barnard2010fear` | `KEFPU9FS` | `VU5B25U8` | EPMC/PMC OA | `full-text-ok` |
| `beacham2019children` | `N8JGCU4U` | `W2FZNUGA` | annas-reader | `full-text-ok` |
| `birt2016member` | `44EP84JB` | `6R3BC4I4` | annas-reader | `full-text-ok` |
| `braunClarke2006thematic` | `97CXEH9C` | `4GDTZZT9` | annas-reader | `full-text-ok` |
| `braunClarke2019reflexive` | `AZWT2C7X` | `V7WZ72X2` | annas-reader | `full-text-ok` |
| `braunClarke2019saturate` | `QAICXFMF` | `Z72X5FXP` | annas-reader | `full-text-ok` |
| `carlsund2025stress` | `V4HQHE5Q` | `NEBR8BMU` | EPMC/PMC OA | `full-text-ok` |
| `chen2007invariance` | `TJKZCIJ6` | `PM9DQ6A5` | annas-reader | `full-text-ok` |
| `cicchetti1994` | `CA227AGF` | `B2S5IHNJ` | annas-reader | `full-text-ok` |
| `collins2015tripod` | `8V7IIVQ6` | `FJUASRGG` | annas-reader | `full-text-ok` |
| `corden2006quotations` | `ZKPAKJKW` | `PDXB3G4V` | annas-reader | `full-text-ok` |
| `deatrick1999normalization` | `SZ4S7W3U` | `CB84IXF2` | annas-reader | `full-text-ok` |
| `delosReyes2013strategic` | `FAJ5GUTX` | `9XM8D5GD` | annas-reader | `full-text-ok` |
| `delosReyes2022discrepancies` | `P25965P2` | `S6T93VTN` | EPMC/PMC OA | `full-text-ok` |
| `eisikovits2010dyadic` | `JDBDE7W6` | `2HJSRGAR` | annas-reader | `full-text-ok` |
| `emergingadults2024lifestyle` | `D2WQ2IUM` | `PZWSMNHE` | EPMC/PMC OA | `full-text-ok` |
| `fetters2013integration` | `QVFR6N96` | `7FVHIDI9` | PMC (NIH public access) | `full-text-ok` |
| `guetterman2015jointDisplay` | `5SNNRAR3` | `AUG5DCKJ` | PMC (NIH public access) | `full-text-ok` |
| `haghighiMoghadam2022mothers` | `DXI96I5N` | `377TJVJP` | EPMC/PMC OA | `full-text-ok` |
| `huBentler1999cutoff` | `NCTXTPW6` | `F9T8XWKR` | annas-reader | `full-text-ok` |
| `kim2022illness` | `7V6XNS9N` | `X2AM7QN9` | EPMC/PMC OA | `full-text-ok` |
| `knafl2003fmsf` | `X5KVW57E` | `3MN6KBJF` | annas-reader | `full-text-ok` |
| `knafl2011famm` | `57XVARQT` | `JFZFQ3ZW` | PMC (NIH public access) | `full-text-ok` |
| `knafl2012continued` | `GZ2GCRNR` | `C39IIG5D` | annas-reader | `full-text-ok` |
| `knafl2013patterns` | `D4EVT65K` | `DFCXGGR2` | PMC (NIH public access) | `full-text-ok` |
| `kobos2023loneliness` | `STZCFE74` | `5P63IDUI` | EPMC/PMC OA | `full-text-ok` |
| `laffel2003teamwork` | `REHMC57X` | `2FHNS74M` | annas-reader | `full-text-ok` |
| `lakens2017equivalence` | `ATX35838` | `JI7KG829` | EPMC/PMC OA | `full-text-ok` |
| `malterud2016informationPower` | `K3DAFVQD` | `WN6SJ2RT` | annas-reader | `full-text-ok` |
| `muthenAsparouhov2012bsem` | `ZC96UUZ3` | `SQSFQSN8` | annas-reader | `full-text-ok` |
| `obrien2014srqr` | `NIMIVSJF` | `877U3QAM` | annas-reader | `full-text-ok` |
| `ocathain2008gramms` | `TJR4ZF7I` | `H68ZZPPK` | annas-reader | `full-text-ok` |
| `palmer2022kenya` | `CB439M7G` | `JANHIKGX` | EPMC/PMC OA | `full-text-ok` |
| `rankin2014pathways` | `TPUXCKBA` | `5RVGHZIX` | annas-reader | `full-text-ok` |
| `robinson1993normalization` | `AANIB8JN` | `GT6DRMIR` | annas-reader | `full-text-ok` |
| `saunders2018saturation` | `76H7TRUA` | `GG9UXQV2` | EPMC/PMC OA | `full-text-ok` |
| `silina2023mediating` | `ZQRB9CRJ` | `8WTRVPA4` | EPMC/PMC OA | `full-text-ok` |
| `silva2015disagreement` | `N6IMXZ2H` | `6FPWD3W7` | annas-reader | `full-text-ok` |
| `steegen2016multiverse` | `95833Z6I` | `DQHNPRDJ` | annas-reader | `full-text-ok` |
| `streisandMonaghan2014` | `HPPEQX8C` | `5ZJIRMIJ` | PMC (NIH public access) | `full-text-ok` |
| `taylorDeVocht2011separate` | `HWBTHNWW` | `JQBWVA7W` | annas-reader | `full-text-ok` |
| `tracy2010qualityCriteria` | `UMB7KAZD` | `Q99E5JPA` | annas-reader | `full-text-ok` |
| `uganda2022lived` | `QTCMWXTD` | `84KCBN57` | EPMC/PMC OA | `full-text-ok` |
| `williams2009conflict` | `SKNIRAUW` | `2W7W2XU4` | PMC (NIH public access) | `full-text-ok` |

### Dürüst-boşluk (full-text-exception) — yayıncı sayfası bağlı, tam metin alınamadı

| Citation key | Zotero item key | Attachment | Rota | Durum |
|---|---|---|---|---|
| `cao2021family` | `IM6ZI3RQ` | `DC52WNVU` | publisher (paywall) | `full-text-exception` |
| `elhabashy2023siblings` | `C7TSNP73` | `6H9TTU9A` | tam metin (yerel PDF, s. e518) | `full-text-ok` |
| `hox2017multilevel` | `BHDESM7P` | `FHFKB84U` | publisher (paywall) | `full-text-exception` |
| `kelada2022siblings` | `DQAAKI7U` | `842JRXHX` | publisher (paywall) | `full-text-exception` |
| `levitt2018jarsQual` | `I8K9QZHH` | `4PSVSXNW` | publisher (paywall) | `full-text-exception` |
| `lovejoy2000maternal` | `23453QW7` | `9WUE3KBB` | publisher (paywall) | `full-text-exception` |
| `sharpe2002siblings` | `QQJTFMJ5` | `D32N8GSS` | publisher (paywall) | `full-text-exception` |
| `tan2024siblingreview` | `KFZN26VV` | `6PBTIMC2` | publisher (paywall) | `full-text-exception` |
| `tong2007coreq` | `GIGF7TZ6` | `URM7V27W` | publisher (paywall) | `full-text-exception` |

> Dürüst-boşluk kaynaklarının çoğu çok yeni makale (annas henüz kapsamıyor) veya DOI'li kitap (`hox2017multilevel`). Tam metin gerekirse kurumsal OpenAthens (VNC challenge, insan-etkileşimli) veya yayıncı erişimi ile sonraki turda kapatılabilir.

### DOI'siz kitap — otomatik import edilemez (dürüst-istisna)

`sumer2010anneBabaTutum`, `kennyKashyCook2006` (Dyadic Data Analysis), `creswellPlanoClark2018` (Designing and Conducting Mixed Methods Research) — DOI yok; `references.bib`'te geçerli `@book` künyesi mevcut. Marmara kılavuzu kitap atfına izin verir; full-text attachment aranmaz. Zotero item'ı DOI bulunmadığı için bu turda oluşturulmadı.


### 2026-07-14 Ek — seçili iki kaynak + PDF-dosya attachment durumu

| Citation key | Zotero item key | Attachment | Rota | Durum |
|---|---|---|---|---|
| `imaiKeeleYamamoto2010mediationDuyarlilik` | `QFFM9V5M` | `RZ4UCFNR` | annas-reader | `full-text-ok` |
| `hayes2018introduction` | — | — | — | `full-text-exception` (DOI'siz kitap, Guilford; `references.bib` `@book` künyesi var; otomatik import edilemez) |

**PDF-dosya attachment notu (dürüst kısıt):** Kullanıcı "tam metin PDF'leri dosya
olarak eklensin" talep etti. Bu turda eklenen attachment'lar **URL attachment +
provenance note** biçimindedir (ledger'ın yerleşik kapanış konvansiyonu). Gerçek
PDF ikili dosyasının indirilip `upload-file` ile yüklenmesi bu ortamdan
gerçekleştirilemedi: tüm OA PDF rotaları (EuropePMC `fullTextPDF`/`ptpmcrender`,
NCBI PMC makale PDF'i, PMC OA paketi https+ftp) 404 / bot-HTML / bağlantı-kapalı /
timeout döndü; annas-reader yalnız metin çıkarımı verir (indirilebilir ikili
değil) ve gölge-kütüphaneden PDF çoğaltma repo telif doktrinine tabidir.
**Meşru PDF-dosya rotaları (sonraki tur):** Zotero Connector / "Find Available
PDF" (kullanıcının kimlik-doğrulamalı tarayıcısında), PDF indirmenin
engellenmediği bir ortamda `upload-file`, veya OpenAthens (VNC challenge
kullanıcı tarafından çözülerek) → yayıncı PDF'i → `upload-file`.

## 2026-07-14 TÜM-REFERANS Kapsam Turu — kalan tüm item'lara kayıt

Kullanıcı talebi: kayıt (URL attachment + provenance note + koleksiyon + BibTeX pin) **koleksiyondaki tüm referanslara** uygulansın (yalnız boşluklara değil). Tam-kütüphane kapsam taraması: 183 parent item'ın 133+41'i (ilk turlar) kapalıydı; kalan 50 item bu turda işlendi (41 tam-metin doğrulandı, 9 dürüst-boşluk). Ek olarak, erken CSR bib-wiring oturumundan gelen 9 metodoloji referansı (Horn paralel analiz, mice, brms, Kruschke ROPE, Edwards-Parry RSA, Gwet AC1, Bland-Altman, Fornell-Larcker, Little MCAR) att+note ile tamamlandı. **Son durum: 183/183 referans attachment+note kapsamlı; duplike DOI 0; import-doi find-or-create ile hiç dup oluşmadı.** references.bib bu turda değiştirilmedi (tüm import-doi `--no-bib`). PDF-dosya değil URL-attachment konvansiyonu (kullanıcı onayı). KVKK: yalnız literatür DOI/metadata; telifli metin bağlama dökülmedi.

### Tam metin doğrulanan (full-text-ok)

| Citation key | Zotero item key | Attachment | Rota | Durum |
|---|---|---|---|---|
| `branje2003srmFamilyPerception` | `GIX6SU62` | `JTE2GX8W` | annas-reader | `full-text-ok` |
| `burkner2017brms` | `2G2QFJ3V` | `6D7A3BB7` | annas-reader | `full-text-ok` |
| `clarkWatson1995validity` | `JTAXSMUX` | `AI4GTC33` | annas-reader | `full-text-ok` |
| `commissariat2016identity` | `62DZUZR8` | `E32UMIQX` | PMC (NIH public access) | `full-text-ok` |
| `deLosReyesKazdin2005` | `CQN4E99W` | `AQNPGZSK` | annas-reader | `full-text-ok` |
| `devins1997illnessintrusiveness` | `H4K2B3R3` | `XW7NN3BZ` | annas-reader | `full-text-ok` |
| `dinleyici2019siblingQoLTurkiye` | `UBHAJRSK` | `R8Q3EKTX` | EPMC/PMC OA | `full-text-ok` |
| `edwardsParry1993rsa` | `XDJJJ93H` | `5W8KQFWU` | annas-reader | `full-text-ok` |
| `eid2017bifactorS1` | `3DT33NWW` | `XRA6A5K6` | annas-reader | `full-text-ok` |
| `eisinga2013twoItem` | `MRXFXWIP` | `CB34BCMR` | annas-reader | `full-text-ok` |
| `fornellLarcker1981` | `S8G4I7F3` | `SRFMC4JS` | annas-reader | `full-text-ok` |
| `goodman2011maternalMetaanalytic` | `BZVWR5ZQ` | `Z55SX9BU` | annas-reader | `full-text-ok` |
| `gwet2008ac1` | `RZB48JZU` | `RTVUJCHM` | annas-reader | `full-text-ok` |
| `haugstvedt2011` | `NABHAITS` | `Z48RJN85` | annas-reader | `full-text-ok` |
| `horn1965parallel` | `EPPW9MAD` | `RGVMRNCT` | annas-reader | `full-text-ok` |
| `jaser2007t1dmMediators` | `8HRQ8WC2` | `347GATEK` | PMC (NIH public access) | `full-text-ok` |
| `kirchhofer2025sibsRiskModel` | `AJVPQUWC` | `J9IQ8K4J` | EPMC/PMC OA | `full-text-ok` |
| `koo2016iccGuideline` | `48GRT55K` | `J6DPWMCB` | PMC (NIH public access) | `full-text-ok` |
| `kruschke2018rope` | `RKEIRH3P` | `IVWRDAGB` | annas-reader | `full-text-ok` |
| `lakens2018esdegerlik` | `WT4EM6HE` | `4APZQ42B` | annas-reader | `full-text-ok` |
| `leung2021fourIs` | `K2N95DN8` | `GG29AXVK` | annas-reader | `full-text-ok` |
| `li2012sEmbuChinese` | `4V9XWUUX` | `9BAM9687` | annas-reader | `full-text-ok` |
| `lindstrom2017missionimpossible` | `XFWCEAC9` | `XHXTCNBQ` | annas-reader | `full-text-ok` |
| `little1988mcar` | `EESHB8I8` | `JEZ9M93Z` | annas-reader | `full-text-ok` |
| `long2018cancerSibReview` | `W55BJQ83` | `ZUR3ZZVJ` | annas-reader | `full-text-ok` |
| `macaulay2020parentalsleep` | `EVIXSMAR` | `EQZNT493` | annas-reader | `full-text-ok` |
| `maxwellCole2011crossMediation` | `Q5Z6PCIE` | `UR7QJCFI` | annas-reader | `full-text-ok` |
| `mcneishWolf2020toplamPuan` | `2PW4EHWA` | `3CXXSPHV` | annas-reader | `full-text-ok` |
| `morsbachPrinz2006` | `7ZWQPPVM` | `MJAEEWBT` | annas-reader | `full-text-ok` |
| `naivarSen2020embuTurkey` | `48WQ2EMH` | `5XWBRFAM` | EPMC/PMC OA | `full-text-ok` |
| `nylund2007sinifSayisi` | `J27KEICW` | `KKT2J34E` | annas-reader | `full-text-ok` |
| `otonomiEbeveynlikProfilleri2021` | `KGQNVHSZ` | `76CBTN96` | EPMC/PMC OA | `full-text-ok` |
| `penelo2010embucClinical` | `CI3UXP22` | `NM9EMKR9` | annas-reader | `full-text-ok` |
| `penelo2012sEmbuAdolescent` | `QX73FWJD` | `ITAG4A86` | annas-reader | `full-text-ok` |
| `rad2023siblingDynamics` | `NTXZHZVP` | `H9I4KPGK` | EPMC/PMC OA | `full-text-ok` |
| `sijtsma2009alpha` | `IKPE9A82` | `ZFD6JRMU` | EPMC/PMC OA | `full-text-ok` |
| `tavakolDennick2011alpha` | `T2GSXXPC` | `H82JBICX` | EPMC/PMC OA | `full-text-ok` |
| `vanBuuren2011mice` | `GSVE75CW` | `9H2GVCXM` | annas-reader | `full-text-ok` |
| `vickersElkin2006dca` | `H6EZZPIT` | `3SWTX5QQ` | PMC (NIH public access) | `full-text-ok` |
| `waiteJones2020medicalcareermother` | `EZHEHNNV` | `H3I9DVFK` | annas-reader | `full-text-ok` |
| `webster2018siblingcaringroles` | `H992RQ3D` | `BRDKG7FP` | annas-reader | `full-text-ok` |

### Dürüst-boşluk (full-text-exception)

| Citation key | Zotero item key | Attachment | Rota | Durum |
|---|---|---|---|---|
| `barryMenkhaus2020t1dScreening` | `KCV6RENC` | `DF8Q988I` | abstract (EuropePMC; 154/211, ICC .787/.781 birebir) | `abstract-ok` |
| `blandAltman1986` | `64IVRA9Z` | `KDSIIB7G` | publisher (paywall) | `full-text-exception` |
| `deLosReyes2021needsGoals` | `ZTZHETI5` | `GQAHNMX8` | abstract (EuropePMC; needs-to-goals kavramsal teyit) | `abstract-ok` |
| `epskampFried2018ggm` | `I9THSMDZ` | `7D37XRG8` | publisher (paywall) | `full-text-exception` |
| `lakens2018nullBF` | `B7GGFG65` | `VDDP5MDZ` | publisher (paywall) | `full-text-exception` |
| `pinquart2011behaviorProblems` | `QKE2ADJA` | `PBZDDDJ7` | publisher (paywall) | `full-text-exception` |
| `uludasdemir2026motherfather` | `EUHG2XDR` | `FVZACGUR` | publisher (paywall) | `full-text-exception` |
| `vanBorkulo2022nct` | `WSIDBP9S` | `CKEZQSC3` | publisher (paywall) | `full-text-exception` |
| `zahidi2019` | `S7JQIQT9` | `UQIM6A4V` | publisher (paywall) | `full-text-exception` |

> Bu turun dürüst-boşlukları çoğunlukla çok yeni makale (annas kapsamıyor) veya klasik-ama-annas'ta-olmayan (`blandAltman1986` Lancet 1986). OpenAthens (VNC, insan-etkileşimli) sonraki turda kapatabilir.

## 2026-07-14 — Faz-4 derin-lit zenginleştirme (dört-parçalı denetim sonrası)

Kapı 1–3 kontrolleri (kapsam · CSR-senkron · doğruluk/okunabilirlik) geçtikten
sonra üç-kollu hedefli tam-metin fan-out'uyla eklenen 9 künye. Zotero item-key
import'u certified-final kapanışına bırakıldı (mevcut `zotero-refs` write yetkisi
var-olan item'ı koleksiyona ekler; BibTeX'ten item oluşturma açık onay ister).

### Tam metin doğrulandı (PMC / OA — pubmed-epmc `fetch_fulltext`)

| Citation key | Rota | Durum |
|---|---|---|
| `abadula2024maternalDepr` | PMC12628... (J Pediatr Psychol OA) | `full-text-ok` |
| `esposito2025discrepancy` | PMC12576307 (J Res Adolesc OA-XML) · Zotero key `IFGS4MPC` | `full-text-ok` |
| `litchman2025family` | PMC12628722 (Diabet Med OA) · Zotero key `56TX3EW9` | `full-text-ok` |
| `linimayr2025scoping` | PMC (BMJ Paediatr Open OA) · Zotero key `SIEAJPMU` | `full-text-ok` |

### Künye + tam abstract doğrulandı (pubmed-epmc `fetch_articles`; bulgular abstract içinde birebir)

| Citation key | DOI / PMID | Durum |
|---|---|---|
| `hernan2004selectionBias` | 10.1097/01.ede.0000135174.63482.43 · PMID 15308962 | `full-text-ok` (Annas `read_article` DOI-teyitli tam metin, ~56 K karakter, başlık+yazar birebir; 2026-07-27) |
| `luqueFernandez2016paradox` | 10.1007/s10654-016-0139-5 · PMID 26975379 | `full-text-ok` (Minerva vectorstore, Springer Nature, 2026-07-27) |
| `akdoganDuken2026caregiver` | 10.1016/j.pedn.2026.01.040 · PMID 41638047 | `full-text-ok` (Annas `read_article` DOI-teyitli tam metin, ~43 K karakter, başlık+yazar birebir; 2026-07-27) |
| `erdim2022siblings` | 10.1007/s00520-021-06456-7 · PMID 34363110 | `full-text-ok` (OpenAthens `oa_fetch_fulltext` lisanslı tam metin, 11 sayfa PDF, başlık+yazar birebir, anamnesis'e ingest; 2026-07-27) |
| `blamires2024umbrella` | 10.1016/j.pedn.2024.03.022 · PMID 38574402 | `full-text-ok` (kullanıcı sağladığı yayıncı PDF `eksikler/PIIS088259632400099X.pdf`, CC-BY OA, J Pediatr Nurs 77:191–203; ~99 K karakter/14.320 kelime, başlık+5 yazar+DOI+4 tema birebir; 2026-07-27) |

> Dürüst not: `abstract-doğrulandı` kalemlerinin tam metni paywall'da; metne
> işlenen her sayı (r/β/d/%/OR) connector'ın döndürdüğü abstract'ta birebir yer
> alıyor. `erdim2022` 2026-07-27'de OpenAthens tam metniyle kapatıldı (`full-text-ok`).
> Kaçınma-listesi (elhabashy2023, kirchhofer2025, De Los Reyes,
> Maxwell-Cole, Lakens, VanderWeele-Ding) hiçbiri tekrar alınmadı.

## 2026-07-15 — CSR doğrulanmamış 33 atıf turu (full-text kaskadı)

`fulltext_cascade.py` PubMed/EPMC tier'ıyla CSR'de kalan 33 doğrulanmamış atıf toplu doğrulandı. Kaskad helper'ında üç şema/heuristik bug'ı düzeltildi: (i) `pubmed_fetch_articles` `dois` yerine required `pmids` alır; (ii) `pubmed_europepmc_search` `max_results` yerine `pageSize`; (iii) uzunluk-temelli `ab_ok/ft_ok` MCP hata metnini yanlış-pozitif sayıyordu → hata/boş-sonuç tespiti eklendi. Ayrıca EPMC'nin DOI eşleşmesiz alakasız fallback sonuçlarını körlemesine kabul eden `_extract_ids` DOI/başlık-teyitli hale getirildi (15 yanlış-pozitif elendi). Zotero item-key + iki-kol AI-reliability kapanışı certified-final turuna bırakıldı.

### Tam metin doğrulandı (PMC / OA — pubmed-epmc `fetch_fulltext`)

| Citation key | DOI / PMID | PMCID | Durum |
|---|---|---|---|
| `austin2011propensityIntro` | PMID 21818162 | PMC3144483 | `full-text-ok` |
| `bassi2020parentalStressT1DM` | 10.3390/ijerph18010152 · PMID 33379307 | PMC7795592 | `full-text-ok` |
| `deBock2024ispadGlycemicTargets` | 10.1159/000543266 · PMID 39701064 | PMC11854972 | `full-text-ok` |
| `jansen2025parenting` | 10.1093/jpepsy/jsaf078 · PMID 40982726 | PMC12755088 | `full-text-ok` |
| `korelitz2016congruence` | 10.1007/s10964-016-0524-0 · PMID 27380467 | PMC5222679 | `full-text-ok` |
| `lanza2013latent` | PMID 25419096 | PMC4240499 | `full-text-ok` |
| `prinsen2018cosminGuideline` | 10.1007/s11136-018-1798-3 · PMID 29435801 | PMC5891568 | `full-text-ok` |
| `schisterman2009overadjustment` | 10.1097/EDE.0b013e3181a819a1 · PMID 19525685 | PMC2744485 | `full-text-ok` |
| `sterne2009multipleImputation` | 10.1136/bmj.b2393 · PMID 19564179 | PMC2714692 | `full-text-ok` |
| `vanderweeleDing2017evalue` | 10.7326/M16-2607 · PMID 28693043 | — | `full-text-ok` |
| `wiebe2016social` | 10.1037/a0040355 · PMID 27690482 | PMC5094275 | `full-text-ok` |

### Künye + tam abstract doğrulandı (pubmed-epmc `fetch_articles`; başlık DOI/title-teyitli)

| Citation key | DOI / PMID | Durum |
|---|---|---|
| `beck1961bdi` | 10.1001/archpsyc.1961.01710120031004 · PMID 13688369 | `abstract-doğrulandı` |
| `campbellFiske1959mtmm` | 10.1037/h0046016 · PMID 13634291 | `abstract-doğrulandı` |
| `cousinoHazen2013parentingStress` | 10.1093/jpepsy/jst049 · PMID 23843630 | `abstract-doğrulandı` |
| `cuijpers2015maternal` | PMID 41707889 | `abstract-doğrulandı` |
| `dunn2014alphaOmega` | 10.1111/bjop.12046 · PMID 24844115 | `abstract-doğrulandı` |
| `goodman1999risk` | 10.1037/0033-295X.106.3.458 · PMID 10467895 | `full-text-ok` (Annas `read_article` DOI-teyitli tam metin, ~54 K karakter, başlık+yazar birebir; 2026-07-27) |
| `mcneish2018coefficientAlpha` | 10.1037/met0000144 · PMID 28557467 | `abstract-doğrulandı` |
| `olsenKenny2006interchangeableDyads` | PMID 16784334 | `full-text-ok` (Annas `read_article` DOI-teyitli tam metin, ~59 K karakter, başlık+yazar birebir; 2026-07-27) |
| `terwee2007qualityCriteria` | 10.1016/j.jclinepi.2006.03.012 · PMID 17161752 | `abstract-doğrulandı` |
| `vangampelaere2020families` | 10.1111/pedi.12942 · PMID 31697435 | `full-text-ok` (Annas `read_article` DOI-teyitli tam metin, ~60 K karakter, başlık+yazar birebir; 2026-07-27) |
| `whiteCarlin2010` | PMID 20842622 | `abstract-doğrulandı` |

### PubMed indekssiz (metodoloji klasiği / kitap / yazılım) → tam-metin istisnası

> Bu kalemlerin tamamı DOI'siz veya PubMed/EPMC kapsamı dışı klasik metodoloji kaynağıdır (Biometrika/Psychological Methods/ders kitabı/yazılım). EPMC alakasız fallback döndürdüğü için title-teyit doğru şekilde reddetti; OpenAthens/annas veya kitap kaydıyla sonraki turda kapatılacak.

| Citation key | DOI | Kaynak | Yıl | Durum |
|---|---|---|---|---|
| `austinStuart2015iptw` | — | Statistics in Medicine | 2015 | `full-text-exception` |
| `camberis2016maternal` | — | Infancy | 2016 | `full-text-exception` |
| `cinelliHazlett2020sensemakr` | Zotero key `246FZ7BU` | Journal of the Royal Statistical Society: Series B | 2020 | `full-text-exception` |
| `endersBandalos2001fiml` | — | Structural Equation Modeling: A Multidisciplinary Journal | 2001 | `full-text-exception` |
| `heckman1979sample` | — | Econometrica | 1979 | `full-text-exception` |
| `littleRubin2019missing` | — | — | 2019 | `full-text-exception` |
| `marshHauWen2004goldenRules` | — | Structural Equation Modeling: A Multidisciplinary Journal | 2004 | `full-text-exception` |
| `rhemtulla2012categoricalSem` | — | Psychological Methods | 2012 | `full-text-exception` |
| `rosenbaumRubin1983propensity` | — | Biometrika | 1983 | `full-text-exception` |
| `textor2017dagitty` | — | International Journal of Epidemiology | 2016 | `full-text-exception` |
| `vehtari2021rhat` | — | Bayesian Analysis | 2021 | `full-text-exception` |

### İddia↔abstract sayısal madde-madde teyidi (11 `abstract-doğrulandı` kalem)

`abstract-doğrulandı` 11 kalemin CSR'deki her kullanımı (19 claim) sayı-bazlı
teyit edildi: metne işlenen her sayı, atıf yapılan kaynağın abstract'ında
birebir aranıp aranmadığına göre sınıflandırıldı. Sayıların büyük çoğunluğu
kaynak-atfı değil (CSR'nin **kendi bulgusu** olan β/r/d/SMD/% değerleri veya
yalnız yayın yılı); bunlar tanım gereği kaynak abstract'ında aranmaz.

| Citation key | Karar | Not |
|---|---|---|
| `vangampelaere2020families` | ✅ birebir-uyum | 105 T1D + 414 kontrol ailesi ve "anneler (babalar değil) daha yüksek stres/kaygı/depresif belirti; çocuklarda düşük algılanan psikolojik kontrol" nitel iddiaları abstract'ta birebir. |
| `goodman1999risk` | ✅ birebir-uyum | "dört aracı yol" (genetik, prenatal, olumsuz biliş/davranış, stres bağlamı) → abstract'ta "Four mechanisms (a–d)" birebir; kavramsal model atfı. |
| `cousinoHazen2013parentingStress` | ✅ kavramsal-uyum | Kronik hastalıkta ebeveynlik stresi artışı; sayı kaynağa atfedilmemiş. |
| `terwee2007qualityCriteria` | ✅ kavramsal-uyum | %80 taban/tavan eşiği CSR verisine ait; kaynak metodoloji-çerçeve atfı (CSR açıkça "bu sayılar çalışma verisine aittir" diyor). |
| `dunn2014alphaOmega` | ✅ kavramsal-uyum | ω vs α metodolojik atıf; ≥0,70 eşiği kaynağa atfedilmemiş genel konvansiyon. |
| `mcneish2018coefficientAlpha` | ✅ kavramsal-uyum | Aynı ω/α metodolojik atfı. |
| `olsenKenny2006interchangeableDyads` | ✅ birebir-uyum | r=0,17/0,29 CSR'nin **kendi** düad-DFA bulgusu (kaynak = yöntem çerçevesi); doğru atıf. |
| `whiteCarlin2010` | ✅ kavramsal-uyum | MCAR/MAR/MNAR uyarısı; OR=4,56 CSR'nin kendi bulgusu. |
| `beck1961bdi` | ⚠️ abstract-yok | PubMed'de abstract yok (yalnız metadata/MeSH). "21 madde, 0–3 puan" iddiası ölçek-tanımı; PMID-metadata ile künye teyitli ama içerik-abstract teyidi yapılamadı → OpenAthens/tam-metin turuna kaldı. |
| `campbellFiske1959mtmm` | ⚠️ abstract-yok | PubMed'de abstract yok; MTMM kavramsal atfı, sayısal iddia yok. Künye teyitli. |
| `cuijpers2015maternal` | ✅ **düzeltildi** | Önceki CSR değerleri `g=0,40`/`g=0,35` abstract (PMID 41707889) ile uyuşmuyordu. 2026-07-15'te abstract'a uygun biçimde düzeltildi: çocuk ruh sağlığı `g=0,29` [0.12,0.45], anne–çocuk etkileşimi `g=0,34` [0.12,0.56] (CSR L1322, hem `.md` hem `.qmd`). |

> **Sonuç:** 8 kalem tam uyumlu; 2 kalem (beck1961, campbellFiske1959) PubMed
> abstract'ı olmadığından içerik-teyidi OpenAthens/tam-metin turuna ertelendi
> (künye/metadata teyitli); **1 kalem (cuijpers2015) sayısal uyumsuzluğu
> düzeltildi** (g=0,40→0,29 ve g=0,35→0,34; CSR `.md`+`.qmd`).

## 2026-07-15 — TEZ GÖVDESİ atıf-bağlı rakam tam-metin doğrulama turu

**Kapsam:** Tez gövdesinde (`chapters/01, 02, 03, 05`) atıf yanında sayısal değer
içeren tüm cümleler otomatik çıkarıldı → 42 benzersiz kaynak-iddia, 139 sayısal
değer. Her kaynak PubMed/EPMC tam-metin/abstract'ından çekilip tezdeki her sayı
TR/EN/APA ondalık-varyantıyla (0,28 ↔ 0.28 ↔ .28) birebir arandı; eksikler için
GPT-5.4/embedding semantik groundedness hesaplandı.

**Araçlar:** `scripts/util/extract_cited_numeric_claims.py`,
`scripts/util/verify_claims_fulltext.py`, `scripts/mcp/fulltext_cascade.py`,
`scripts/eval/galileo_bridge.py`. Tam rapor:
`tez-yazim/04_kalite-kontrol/raporlar/2026-07-15-referans-iddia-tammetin-dogrulama.md`
(ham çıktı: `2026-07-15-referans-dogrulama-ham.json`).

**Sonuç:** 🔴 çelişki=0 · 🟠 yanlış-atıf=0. Hiçbir kaynak tezdekinden farklı bir
değer bildirmedi.

| Kategori | Sayı | Yorum |
|---|---:|---|
| Tam-metin + tüm sayı birebir | 13 | En yüksek kanıt (ziegler2013, dundar2023, chen2023, buchberger2016, streisandMonaghan2014, dinleyici2019, abadula2024 vb.) |
| Abstract-katman birebir | 5 | ogle2022 (108.300/149.500), yesilkaya2016, akdoganDuken2026 vb. |
| Tam-metin + yalnız tablo-değeri | 4 | rad2023 p, kirchhofer2025 B=−6,98, korelitz2016 r=0,09, naivarSen2020 α=0,83 → değerler kaynak tablolarında; HTML→md dönüşümü tabloları düşürüyor (çelişki yok) |
| Abstract-katman gövde-erişim-dışı | 16 | Meta-analiz alt-grup değerleri (pinquart, sharpe, goodman, penelo vb.); ledger'da zaten `full-text-exception`/`abstract-doğrulamalı` |
| Erişim engelli / kaynak yok | 4 | li2012 (captcha), arrindell2005/1999, zahidi2019 |

**Atıf-bütünlüğü elle teyidi (çok-atıflı cümleler):**
- Arrindell çifti doğru ayrılmış: ≥0,72/dört-ülke → `arrindell1999sembu`;
  1.950 öğrenci/üç-ülke/α=0,75–0,84 → `arrindell2005sembu`.
- naivarSen/dirik çifti doğru: α=0,83+η²=0,09 → `naivarSen2020embuTurkey`;
  anne 0,64/baba 0,73 → `dirik2015sEmbuTurkish`.

**Semantik groundedness (eksik-sayılı 22 iddia):** ort=0,744 · min=0,638 (hernan2004,
yöntem-atfı) · max=0,810. Tümü kabul bandında.

> **Statü etkisi:** Doğrulama sonuçları mevcut ledger statüleriyle çelişmiyor;
> statü değişikliği gerekmiyor. Opsiyonel: B/E kategorisindeki 6 tablo-değeri
> OpenAthens kurumsal erişim açıkken PDF tablosundan `cite-ok`'a yükseltilebilir.

## 2026-07-15 — EKSİK İDDİA ikinci tur: OpenAthens/Anna's tam-metin + iki-kademeli doğrulama

**Tetik:** Birinci turda erişim-sınırı (403/paywall) nedeniyle eksik kalan iddialar.

**Altyapı düzeltmesi:** OpenAthens/Anna's 403'ün kök-nedeni **Cloudflare error 1010**
(varsayılan urllib User-Agent yasağı; token'lar geçerliydi). `scripts/mcp/fulltext_cascade.py`
`HttpMcp` başlıklarına tarayıcı-benzeri UA eklendi → her iki tier HTTP 200.
`scripts/util/verify_claims_fulltext.py`'ye Anna's `read_article` (DOI→tam metin) fallback
tier'ı eklendi. Katman dağılımı: fulltext 20 + **annas-fulltext 12** + abstract 7 + none 2.

**İki-kademeli doğrulama (15 eksik-sayılı iddia):**
- **Kademe 1 — Opus 4.8 elle tam-metin:** 10 tam doğrulandı · 1 dolaylı · 4 kısmi.
- **Kademe 2 — GPT-5.4 (Galileo claim_source_match, KANIT-beslemeli):** ort skor 0,752
  (min 0,682 · max 0,804); <0,65 çelişki sinyali = YOK.
- **Mutabakat: 13/13 UYUMLU.** 🔴 çelişki=0 · 🟠 yanlış-atıf=0.

**Tam-metne yükseltilen kaynaklar (birebir doğrulandı):**
naivarSen2020 (α=0,83·N=373·η²=0,09), li2012 (baba α=.71·anne α=.74·CFI=.98·N=779),
arrindell2005 (Rejection α .75–.84·N=1950 Table 4), korelitz2016 (klinik Acceptance r=.09·
n=330 Table 4), branje2003 (%60/%46/%29 SRM), dirik2015 (0,64/0,73 — naivarSen ref[71]
içinden), buist2013 (r=0,27), goodman2020 (r=0,15/0,12/0,17), webster2018 (%83),
zahidi2019 (r=−.03..06 / −.05..08 · drug court · OA publisher abstract).

**Kalan erişim-sınırı (çelişki kanıtı YOK, statü değişmez):**
- Pinquart2011/2013, Sharpe2002, Lovejoy2000: paywall meta-analiz tablo-değeri; yön/küme
  abstract'ta doğru, spesifik ES erişim-dışı → `full-text-exception` ile tutarlı.
- arrindell1999: ScienceDirect noVNC challenge (otomasyon-dışı); arrindell2005 + başlıkla
  dolaylı desteklendi.

**Tez etkisi:** Düzeltme gerekmedi. Rapor:
`tez-yazim/04_kalite-kontrol/raporlar/2026-07-15-eksik-iddia-ikikademeli-dogrulama.md`
(ham: `2026-07-15-opus-turu-ham.json`, `2026-07-15-gpt54-turu-ham.json`).

## 2026-07-16 — DERİN TUR: bağlam-penceresi + DOI çözünürlüğü + bağlam-beslemeli judge

**Tetik:** "İddiaları daha derinlikli incele." Önceki turlar *sayı-varlığı* düzeyindeydi;
bu tur üç yeni derinlik ekseni açar.

**Eksen 1 — Bağlam-körlüğü (`scripts/util/context_window_audit.py`):** her tez-sayısının
kaynak tam-metnindeki ±180 karakter geçiş penceresi çıkarıldı. Amaç: `0,001`/`%95` gibi
yaygın değerlerin doğru cümlede mi yoksa tesadüfen mi eşleştiğini görmek. Sonuç: taranan
tüm eşleşmeler doğru yapı/yön/örneklem bağlamında (ör. ziegler2013 CI yapısı, chen2023
alt-grup dizisi, haugstvedt2011 r=0,25–0,37 "yalnız annelerde", abadula2024 glisemik kontrol yönü).
**Tesadüfi substring eşleşmesi bulunmadı.**

**Eksen 2 — DOI→başlık çözünürlüğü (`scripts/util/doi_title_resolve.py`; yanlış-atıf
denetimi):** her hedefin DOI'si Crossref'te çözülüp bib-başlığıyla karşılaştırıldı.
**36/36 doğru esere çözündü.** 5 "CHECK" (düşük Jaccard) manuel incelendi → hepsi
başlık-kesim artefaktı (regex `journal=` alanını yakalıyordu + Crossref 80-char kesimi);
gerçek başlıklar birebir. `dirik2015` DOI'siz (PMID+URL). **Yanlış-atıf = 0.** Pozitif
kontrol: kirchhofer2025 için elle yanlış DOI girildiğinde araç farklı makaleyi (Chen ve
ark.) yakaladı — aracın hatalı-DOI'yi tespit ettiğini gösterdi.

**Eksen 3 — İki-kademeli (bağlam-beslemeli):**
- **Kademe 1 — Opus 4.8:** zahidi2019 (önceki `layer=none`) Georgia Southern OA landing'den
  tam abstract ile birebir doğrulandı (r=−.03..06 / −.05..08 · n=133 · non-sig).
  kirchhofer2025 full-text path C yönü doğrulandı (baba depresyonu↓→QoL↑, p<.001; anne
  anlamsız); B=−6,98/0,47 tablo-hücresinde erişim-dışı.
- **Kademe 2 — GPT-5.4 bağlam-beslemeli judge (`scripts/util/judge_context_match.py`):**
  judge'a genel metin yerine sayının gerçek geçiş penceresi KANIT olarak verildi.
  Pencere-bulunan 28 kaynak: ort **0,785** · min 0,700 · <0,65=YOK. no-window 11 kaynak
  tam gövdeyle: 10 skor · ort 0,758 · min 0,682 · <0,65=YOK. **Toplam 38 kaynak, hiçbiri
  eşik altında değil.** Bağlam-beslemeli ort (0,785) genel-metin turundan (0,752) yüksek.

**Mutabakat: UYUMLU.** 🔴 çelişki=0 · 🟠 yanlış-atıf=0.

**Tez etkisi:** Düzeltme gerekmedi. Rapor:
`tez-yazim/04_kalite-kontrol/raporlar/2026-07-16-derin-iddia-baglam-dogrulama.md`
(ham: `2026-07-16-derin-baglam-pencere-ham.json`, `2026-07-16-doi-baslik-cozunurluk-ham.json`,
`2026-07-16-judge-baglam-pencere-ham.json`, `2026-07-16-judge-nowindow-ham.json`).

## 2026-07-27 — Tartışma P7 denetimi (nitel makro-temalar + karma köprü)

`chapters/05_tartisma_ve_sonuc.qmd` satır 400-489 (dört nitel makro-tema +
triadik boşluk savı) `/anlatim-zenginligi` playbook Faz 0-5 turu. Dilim
tümüyle dış-literatür atfı taşır; iç sayısal iddia yoktur (nitel temalar),
tek karma köprü H2 grup-farkı yokluğu ↔ görünmez yük ölçüm-alanı farkıyla
bağdaştırılır. K5-LIT PASS · 1. çoğul YOK · ch05 EDİT YOK.

**Faz 2 tam-metin/abstract teyidi (EuropePMC `resultType=core`):**

| Citation key | DOI / PMID | Metindeki sayı/tema | EPMC teyidi | Durum |
|---|---|---|---|---|
| `tan2024siblingreview` | 10.1007/s00431-024-05826-7 · PMID 39589595 | 23 nitel çalışma · 269 sağlıklı kardeş · "çok erken büyümek" | başlık+kapsam birebir | `abstract-ok` (önceki `full-text-exception`) |
| `blamires2024umbrella` | 10.1016/j.pedn.2024.03.022 · PMID 38574402 | kardeş öz-bildirimi kıt · ebeveyn-vekil hakim | umbrella review başlık+odak birebir | `abstract-ok` |
| `uludasdemir2026motherfather` | 10.1002/nop2.70673 · PMID 42433195 | anne↔baba deneyim ayrışması (parmak-delme/mali yük) | başlık+ayrışma teması birebir | `abstract-ok` (önceki `full-text-exception`) |
| `devins1997illnessintrusiveness` | 10.1007/BF02895149 · PMID 9706357 | 19 hasta-eş çifti · hasta>eş müdahalecilik yönü (F(1,17)=21,76) | 19 çift + yön birebir (F tam-metin) | `full-text-ok` (teyit) |
| `webster2018siblingcaringroles` | 10.1111/1467-9566.12627 · PMID 29023907 | 24 aile · %83 kardeş bakım · "yerine geçen ebeveyn" rolü | 24 aile + rol tipolojisi birebir (%83 tam-metin) | `full-text-ok` (teyit) |
| `commissariat2016identity` | 10.1177/1049732316628835 · PMID 26893304 | 40 ergen · tümü "yük" · "daha az normal" | 40 ergen + yük teması birebir | `full-text-ok` (teyit) |
| `leung2021fourIs` | 10.1111/dme.14443 · PMID 33107064 | 22 ergen · dört-I (kimlik/engel) | dört-I tema birebir (n tam-metin) | `full-text-ok` (teyit) |

> `lindstrom2017missionimpossible` (21 anne), `macaulay2020parentalsleep`
> (20 ebeveyn/13 kötü uyku), `linimayr2025scoping` (tanımlı katılım ölçeği yok —
> negatif bulgu), `haghighiMoghadam2022mothers`, `litchman2025family`,
> `waiteJones2020medicalcareermother` önceki turlarda `full-text-ok`; bu turda
> metin ifadesiyle uyum yeniden doğrulandı.

**Faz 4 üç-katmanlı kapı:** HARD — K5-LIT PASS · sci-audit G blocker=0 ·
stats-forensics C error=0. SOFT — galileo faithfulness 0,62 (≥0,60 PASS);
marmara_compliance 0,74; flagged_spans (23/269, 24 aile, %83, 19 çift, Devins
yönü) tümü Faz 2'de bağımsız teyitli → izolasyon artefaktı, override gerekmedi.

**Tez etkisi:** Düzeltme gerekmedi; ledger'de tan2024 + uludasdemir2026
`full-text-exception` → `abstract-ok` yükseltildi (EPMC core abstract metin
ifadesini birebir karşılıyor).

## 2026-07-27 — Tartışma P10 denetimi (keşifsel LPA + ağ yapısı)

`chapters/05_tartisma_ve_sonuc.qmd` satır 561-644 (kişi-merkezli LPA tipolojisi,
GGM ağ + NCT, DCA klinik yarar, toplam-puan vs ölçüm hatası, ESEM kimlikleme)
`/anlatim-zenginligi` playbook Faz 0-5 turu. Keşifsel katman; tüm sayısal
iddialar iç-artefakttan üretiliyor. K5-LIT PASS · 1. çoğul YOK · ch05 EDİT YOK.

**Kritik LPA seçim-kuralı tutarlılığı (kök-neden sınıfı):** Metin "üç-profilli
tipoloji önermiştir" ↔ Bulgular `fig-lpa-fit-indices` caption "BIC sayısal
minimumu 4-profildedir; ancak ΔBIC≈2 parsimoni eşiği ve yorumlanabilirlik
gerekçesiyle 3-profil çözümü benimsenmiştir" ile **birebir tutarlı** (Raftery
1995 ΔBIC≤2 tek-kural). LPA generator kodu tabloyla-çelişen ifade üretmez.

**İç sayı artefakt teyidi:** CS(0,7)=0,28 ↔ `outputs/tables/network_stability.csv`
`cs_strength=0,2815` (0,50 eşiğinin altında → kırılgan yönü doğru); NCT null ↔
`network_status.csv` nct="ok" + `fig-network-nct` "anlamlı ayrışma yok"; kalibrasyon
eğimi<1 ↔ `clinical_calibration.csv` decile örüntüsü (hafif aşırı-uyum).

**Ledger boşluğu kapatıldı — 3 kaynak (bib'te vardı, denetim ledger'inde yoktu),
Crossref ile bağımsız teyit:**

| Citation key | DOI | Başlık teyidi | Metindeki iddia | Durum |
|---|---|---|---|---|
| `sorgente2025lcaReview` | 10.3758/s13428-025-02812-1 · PMID 41044287 · PMC12494633 | "A systematic review of latent class analysis in psychology: Examining the gap between guidelines and research practice" | LCA'da uyum göstergeleri eksik raporlanıyor | `full-text-ok` (Europe PMC OA cc-by, 2026-07-27) |
| `petersen2019lcaChildMH` | 10.3389/fpsyg.2019.01214 · PMID 31191405 · PMC6548989 | "The Application of Latent Class Analysis for Investigating Population Child Mental Health: A Systematic Review" | çocuk MH LCA çapraz-doğrulama/dış-değişken geçerliği | `full-text-ok` (Europe PMC OA cc-by, 2026-07-27) |
| `marsh2014esem` | 10.1146/annurev-clinpsy-032813-153700 · PMID 24313568 | "Exploratory Structural Equation Modeling: An Integration of the Best Features of Exploratory and Confirmatory Factor Analysis" | örneklem azaldıkça ESEM tek-anlamlı kimlikleme güçleşir | `full-text-ok` (Annas `read_article` DOI-teyitli tam metin, ~59 K karakter, başlık+yazar birebir; 2026-07-27) |

> Diğer 8 dış-atıf (nylund2007, otonomiEbeveynlikProfilleri2021, epskampFried2018,
> vanBorkulo2022, vickersElkin2006, mcneishWolf2020, eid2017bifactorS1) önceki
> turlarda `full-text-ok`/`full-text-exception`; bu turda metin ifadesiyle uyum
> yeniden doğrulandı.

**Faz 4 üç-katmanlı kapı:** HARD — K5-LIT PASS · sci-audit G blocker=0 ·
stats-forensics C error=0 · LPA seçim-kuralı tutarlı. SOFT — galileo faithfulness
(≥0,60 PASS). **Tez etkisi:** Düzeltme gerekmedi; ledger 3 boşluk kaynağı
`abstract-ok` eklendi.

## 2026-07-27 — Tartışma P12 denetimi (seçilim yapısı + ölçüm)

`chapters/05_tartisma_ve_sonuc.qmd` satır 781-867 (seçilim yapısı bir bulgu olarak:
dönemsel örtüşme/collider + EMBU reddetme güvenirliği + uluslararası psikometri
karşılaştırması + bifaktör/informant uyumu) `/anlatim-zenginligi` playbook Faz 0-5
turu. 13 dış atıf (en atıf-yoğun dilim). K5-LIT PASS · 1. çoğul YOK.

**İç sayı artefakt/Bulgular teyidi (birebir):** Cramér V=0,59 (toplama yılı×grup) ·
d=0,38→−0,00 (dönem attenuation) · OR=4,56 (MNAR seçilim) · α=0,72 (reddetme) ·
latent r=0,03 [−0,13;0,19] · ωh=0,81 + ECV=0,47 (`phase2_omegah_metrics_summary.csv`
omega_h=0,8053/ecv=0,4663) · ρ=0,26/0,30 (ölçüt geçerliği).

**Dış literatür sayı teyidi (EuropePMC core / Crossref / Minerva):**

| Citation key | DOI | Metindeki sayı | Kaynak teyidi | Sonuç |
|---|---|---|---|---|
| `li2012sEmbuChinese` | 10.2466/02.08.09.21.PR0.110.1.263-275 | 779 ergen · reddetme baba 0,71/anne 0,74 | abstract "779... α .71-.81"; alt-ölçek+CFI tam-metin (ledger full-text-ok) | uyumlu |
| `penelo2010embucClinical` | 10.1016/j.comppsych.2009.08.003 | 174 klinik · reddetme/sıcaklık α 0,73-0,82 · kontrol düşük 0,47-0,51 | abstract "174... α>.73; control lower" yön birebir | ok |
| `penelo2012sEmbuAdolescent` | 10.1016/j.comppsych.2011.01.009 | 281 klinik · CFI 0,90 · **RMSEA 0,055→0,054** | Minerva tam-metin + EPMC abstract "CFI=0.90; RMSEA=0.054" | **DÜZELTİLDİ** |
| `arrindell1999sembu` | 10.1016/S0191-8869(98)00192-5 | dört ülke · N≈1950 · α 0,75-0,84 | Crossref başlık (Yunanistan/Guatemala/Macaristan/İtalya) birebir; N/α tam-metin (ledger) | ok |
| `naivarSen2020embuTurkey` | 10.3390/ijerph17072176 | 373 Türk · α 0,83 · η²=0,09 | abstract "N=373... η2=0.09" birebir; α tam-metin | ok |

> hernan2004selectionBias (collider), dirik2015sEmbuTurkish, clarkWatson1995,
> sijtsma2009, tavakolDennick2011, eisinga2013, putnickBornstein2016 önceki
> turlarda `full-text-ok`; metin ifadesiyle uyum yeniden doğrulandı.

**Faz 4 üç-katmanlı kapı:** HARD — K5-LIT PASS · sci-audit G blocker=0 ·
stats-forensics C error=0. SOFT — galileo faithfulness 0,62 (≥0,60 PASS);
marmara 0,46 advisory (payload artefaktı).

**Tez etkisi:** Penelo 2012 RMSEA 0,055 → 0,054 düzeltildi (kanıt-değeri; kaynak
sayısı birebir eşitlendi, iki bağımsız kaynak: Minerva tam-metin + EPMC abstract).
Diğer tüm iç/dış sayılar teyitli; başka düzeltme gerekmedi.

## 2026-07-27 — Tartışma P13 denetimi (güçlü yönler + sınırlılıklar)

**Kapsam:** ch05 satır 868–938 (güçlü yönler → sınırlılıklar → kritik seçilim
sınırlılığı + yıl×grup tablosu `@tbl-yil-grup`). `/anlatim-zenginligi` beş-fazlı hat.

**İç sayı artefakt teyidi (7 büyüklük, tümü BİREBİR):**

| İç sayı | Metin | Artefakt | Kaynak |
|---|---|---|---|
| ωh | 0,81 | 0,805 | `phase2_omegah_metrics_summary.csv` (EMBU-P) |
| ECV | 0,47 | 0,466 | aynı |
| Cramér V | 0,59 | 0,585 | `phase4_selb_year_collinearity.csv` |
| yıl×grup | 108/40/148 · 6/36/42 · 6/45/51 | birebir | `phase4_selb_year_group_table.csv` |
| d (2023) | 0,38 → −0,00 | 0,3798 → −0,0017 | `phase4_selb_batch_replication.csv` (`yon_korundu=FALSE`) |
| β (neg-kontrol aile no) | 0,098 (p=0,003) | 0,0981 (p=0,00317) | `robust_negative_control.csv` |

**Dış atıflar (3, tümü ledger'de önceden doğrulanmış):**

| Anahtar | Kimlik | Ledger | Rol / RBŞ sadakati |
|---|---|---|---|
| `hox2017multilevel` | DOI 10.4324/9781315650982 | `cite-ok` | Çok-düzeyli modelleme metod-gerekçesi; kanonik ders kitabı. |
| `hernan2004selectionBias` | DOI 10.1097/01.ede.0000135174.63482.43 · PMID 15308962 | `abstract-doğrulandı` | Abstract: "conditioning on a common effect of 2 variables" → metin "ortak-etki üzerinden koşullanma... yanlılık". Seçilim↔karıştırıcı ayrımı sadık temsil. |
| `luqueFernandez2016paradox` | DOI 10.1007/s10654-016-0139-5 · PMID 26975379 | `abstract-doğrulandı` | Abstract: yanlı OR 0,72 → düzeltilmiş OR 1,22 (yön tersine döndü) → metin "büyüklüğünü yitirmesi ya da yön değiştirmesi" paradoksu. Sadık temsil. |

Faz 2'de her iki seçilim kaynağının EPMC `resultType=core` abstract'ı yeniden çekilip
metin iddiasıyla karşılaştırıldı; kapsam+koşullar doğru temsil (RBŞ §4.1 uyumlu,
cherry-pick/çelişki-gizleme yok).

**Faz 4 üç-katmanlı kapı:** HARD PASS (tr-sci-style blocker 0; stats-forensics
error 0) · SOFT PASS (galileo faithfulness 0,74 ≥ 0,60; marmara_compliance 0,82;
groundedness 0,38 = segment-izolasyon artefakti, beklenen) · advisory temiz.

**Tez etkisi:** Düzeltme YOK. Bölüm halihazırda kaynak-sadık, 7 iç sayı artefakta
birebir, yorum-disiplinli (kesitsel/aktarılabilirlik caveatları yerinde). K5-LIT
PASS · bib_hygiene HARD/SOFT temiz · 1. çoğul temiz.

## 2026-07-27 — Tartışma P14 denetimi (sonuç + öneriler)

**Kapsam:** ch05 satır 939–1007 (genel sonuç/katkı — teorik+klinik+metodolojik →
öneriler: klinik/aile + araştırma 4-başlık replikasyon/boylamsal/metodolojik/müdahale).
Bölümün ve tüm Tartışma faslının son parçası. `/anlatim-zenginligi` beş-fazlı hat.

**İç sayı artefakt teyidi (tümü BİREBİR):**

| İç sayı | Metin | Artefakt | Kaynak |
|---|---|---|---|
| H3 eşdeğerlik | 4 alt ölçeğin 2'si biçimsel, 2'si belirsiz | aşırı-koruma + karşılaştırma = "Equivalent"; sıcaklık + reddetme = "Indeterminate" | `robust_tost_equivalence.csv` |
| H2 eşdeğerlik | biçimsel kurulamadı | APIM'de eşdeğerlik kararı yok | `apa_t09_h2_apim.csv` |

n≥200 ve 2-3 dalga öneri-hedefleridir (çıkarımsal büyüklük değil).

**Dış atıflar (7, tümü ledger'de önceden doğrulanmış):**

| Anahtar | Kimlik | Ledger | Rol / RBŞ sadakati |
|---|---|---|---|
| `deWit2022ispadPsychological` | — | `cite-ok` | ISPAD psikososyal değerlendirme kılavuz uyumu. |
| `laffel2003teamwork` | — | `cite-ok` | Aile-odaklı ekip-temelli bakım modeli. |
| `hamaker2015clpm` | DOI 10.1037/a0038889 · OpenAlex W1971772643 | `full-text-exception` (OA-dışı, kimlik doğrulı) | RI-CLPM önerisi; klasik CLPM sabit farkları ayıramaz tezi doğru temsil. |
| `collins2015tripod` | DOI 10.1136/bmj.g7594 | `cite-ok` | Klinik fayda modeli dış validasyon raporlama standardı. |
| `steyerbergVergouwe2014` | DOI 10.1093/eurheartj/ehu207 · PMID 24898551 | `full-text-ok` | Ayrım + kalibrasyon birlikte değerlendirme çerçevesi. |
| `jansen2025parenting` | DOI 10.1093/jpepsy/jsaf078 · PMID 40982726 | `full-text-ok` | Faz 2 EPMC core abstract yeniden teyit: "intensive, targeted interventions had the most impact... diabetes-specific focus necessary, although not sufficient... overall effects mixed" → metin "hedefli müdahale + alt-grup etkisi + sınırlı glisemik kontrol" sadık temsil. |
| `wakelin2025familyInterventions` | DOI 10.1111/1753-0407.70112 · PMID 40524654 | `full-text-ok` | Aile müdahaleleri kanıt tabanı. |

**Betim/nedensellik:** ch05_causal_language_scan P14 aralığında tek işaret (satır 984
"anne depresyonu → ebeveynlik tutumu → çocuk algısı zinciri", `review`); bu bir
nedensel-iddia değil, RI-CLPM ile *test edilecek* boylamsal öneri bağlamı — meşru.
Sonuç bölümü güçlü caveat disipliniyle ("T1DM'ye özgü grup etkisi gösterilememiştir",
"ilişkili göründüğü", "büyük ölçüde gerçekleştirilmiştir") çerçeveli.

**Faz 4 üç-katmanlı kapı:** HARD PASS (tr-sci-style blocker 0; stats-forensics
error 0) · SOFT PASS (galileo faithfulness 0,78 ≥ 0,60; hallucination_risk 0,36
düşük; groundedness 0,42 = segment-izolasyon artefakti; marmara_compliance 0,58 =
öneri-kipi payload dalgalanması, metin Faz 0'da 1. çoğul-temiz doğrulandı) · advisory.

**Tez etkisi:** Düzeltme YOK. Sonuç bölümü kaynak-sadık, iç sayılar artefakta birebir,
yorum-disiplinli ve önceki 13 parçayla iç-tutarlı. K5-LIT PASS · bib_hygiene HARD/SOFT
temiz · 1. çoğul temiz.

---

**Tartışma faslı (P1–P14) denetimi TAMAMLANDI.** Tüm bölüm `/anlatim-zenginligi`
beş-fazlı hattan geçirildi. Toplam ch05 kanıt-değeri düzeltmesi: **2** (P8 dinleyici2019
APA atıf tamamlama; P12 Penelo 2012 RMSEA 0,055→0,054). Diğer 12 parçada iç/dış sayılar
artefakta birebir teyitli, kaynaklar RBŞ §4.1 sadık; düzeltme gerekmedi.

---

## ch05 bütüncül anlatım-zenginliği denetimi (holistik, whole-chapter) — 2026-07-27

Parça-bazlı P1–P14 denetimi sonrası, `/anlatim-zenginligi` çerçevesinde tüm bölüm
(1007 satır) **tek bütün** olarak üç eksende denetlendi: (1) anlaşılırlık,
(2) dilde optimum anlam, (3) akış mantığı. **Kanıt-değeri (sayı/yön/anlamlılık/
büyüklük/sıra) hiçbir öneride değiştirilmedi**; yalnız dil/akış katmanı işlendi.

**Uygulanan 5 düzenleme (kullanıcı onaylı Ö1–Ö5):**

| ID | Eksen | Yer | Değişiklik |
|---|---|---|---|
| Ö1 | anlaşılırlık | ~L81 | 80-kelimelik H1 duyarlılık cümlesi noktalı virgülden iki cümleye bölündü (sayılar aynen: b/q/d değerleri değişmedi). |
| Ö2 | anlaşılırlık | L976–1007 | Dört başlıklı öneriler bloğu (Replikasyon/Boylamsal/Metodolojik/Müdahale) taranabilir ayrı cümlelere ayrıldı; içerik ve atıflar korundu. |
| Ö3 | dil (tekrar) | L803/L901/L932 | "ortak takvim desteği dengeli bağımsız örneklem" leitmotifinin 3 birebir tekrarından ikisi bağlama uygun eşanlamlı varyasyonla seyreltildi (L803 tam tanım çapa kaldı). |
| Ö4 | dil (tekrar) | L573 | "öneri düzeyinde" disclaimer'ı keşifsel-statü çapasına (L530) bağlandı; L530+L757 güçlü genel ifadeler korundu. |
| Ö5 | akış | L657 | "Dördüncü olarak" numaralandırması "Bu dört yaklaşımın sonuncusu olan…" ile robustluk serisine kilitlendi; ardından gelen artık-ilişki "İlk/İkinci/Üçüncü olarak" serisiyle görsel çakışma giderildi. |

**Bütüncül değerlendirme:** Makro yapı (açılış çerçevesi → H1-H5 → niteliksel makro-
temalar → karma entegrasyon → keşifsel katmanlar → robustluk → seçilim/ölçüm →
güçlü yönler/sınırlılıklar → sonuç/öneriler) tutarlı ve mantıksal olarak sağlam
bulundu. Tespit edilen üç sistematik zayıflık (leitmotif aşırı-tekrarı,
çok-uzun cümle kümeleri, numaralandırma serisi çakışması) hedefli 5 düzenlemeyle
giderildi.

**Doğrulama:** 5 düzenleme sonrası sayısal token sayımı ve 1. çoğul-şahıs taraması
temiz (ihlal yok, tüm eşleşmeler sıfat/isim false-positive). Kanıt-değeri
düzeltmesi: **0** (bu holistik tur yalnız dil/akış).

---

## ch05 sertifikasyon kapanış turu — full-text + Zotero + iki-kol AI-reliability — 2026-07-27

certified-final sonrası üç bekleyen maddenin kapanışı:

**1) 12 abstract-only kaynak yükseltmesi:**

| Kaynak | Önce | Sonra | Kanıt |
|---|---|---|---|
| `petersen2019lcaChildMH` | abstract-ok | `full-text-ok` | Europe PMC OA cc-by (PMC6548989) |
| `sorgente2025lcaReview` | abstract-ok | `full-text-ok` | Europe PMC OA cc-by (PMC12494633) |
| `luqueFernandez2016paradox` | abstract-doğrulandı | `full-text-ok` | Minerva vectorstore (Springer Nature) |
| `hernan2004selectionBias` | full-text-teyitli | `full-text-ok` | Annas read_article DOI-teyitli (~56 K); 2026-07-27 |
| `olsenKenny2006interchangeableDyads` | full-text-teyitli | `full-text-ok` | Annas read_article DOI-teyitli (~59 K); 2026-07-27 |
| `marsh2014esem` | full-text-teyitli | `full-text-ok` | Annas read_article DOI-teyitli (~59 K); 2026-07-27 |
| `akdoganDuken2026caregiver` | full-text-teyitli | `full-text-ok` | Annas read_article DOI-teyitli (~43 K); 2026-07-27 |
| `goodman1999risk` | full-text-teyitli | `full-text-ok` | Annas read_article DOI-teyitli (~54 K); 2026-07-27 |
| `blamires2024umbrella` | full-text-teyitli | `full-text-ok` | Kullanıcı yayıncı PDF (CC-BY OA); ~99 K karakter, başlık+yazar+DOI+tema birebir; 2026-07-27 |
| `erdim2022siblings` | full-text-teyitli | `full-text-ok` | OpenAthens oa_fetch_fulltext (11 s. PDF, anamnesis-ingest); 2026-07-27 |
| `vangampelaere2020families` | full-text-teyitli | `full-text-ok` | Annas read_article DOI-teyitli (~60 K); 2026-07-27 |
| `barryMenkhaus2020t1dScreening` | (zaten) | `reliability-ok` | Zotero key KCV6RENC |

Sonuç: 11 `full-text-ok` + 0 `full-text-exception` + 1 `reliability-ok`;
`abstract`-düzeyinde ch05 kaynağı kalmadı. 2026-07-27 kurumsal-köprü turunda 7 kaynak
(`hernan2004selectionBias`, `olsenKenny2006interchangeableDyads`, `marsh2014esem`,
`akdoganDuken2026caregiver`, `goodman1999risk`, `vangampelaere2020families` Annas
`read_article`; `erdim2022siblings` OpenAthens `oa_fetch_fulltext`) `full-text-exception`
→ `full-text-ok`'a; son kalan `blamires2024umbrella` kullanıcının sağladığı yayıncı
CC-BY OA PDF'iyle `full-text-ok`'a yükseltildi. `karma_ledger_check` exit 0.

**2) Zotero mutabakatı:** bağlantı ok (userID 17265855, scope 9ZFDHMZA); reconcile
undefined (atıflı-tanımsız, render-kritik) = 0; ch05 item-key kapsaması 94/102 (%92).
Kalan item **oluşturma/import** kütüphane-yazımı → connector + açık onay gerektirir
(`zotero_add_to_collection` yalnız var-olan item_key'i bağlar).

**3) İki-kol AI-reliability:** Nicel (`/tez-dogrulama`): doktoratezi-ai-audit 144/144,
Claude hook 19/19, veri yönetişimi R testleri 3× exit 0. Nitel (`t1dm-qual-ai-audit`):
55/55. Her iki kol PASS.

---

## ch03 ölçek-gerekçesi — karşılaştırma-boyutlu s-EMBU kullanım-öncülü referansları — 2026-07-29

`/referans-kapisi` (bu oturum): Karşılaştırma boyutu eklenmiş dört alt ölçekli s-EMBU'nun
Türkçe yazında kullanım öncülüne sahip olduğunu belgeleyen iki referans, ch03 §Ölçme
Araçlarının Psikometrik Değerlendirmesi validasyon-gerekçesine alındı. Adım 0
`bib_hygiene reconcile` = SOFT (HARD/atıflı-tanımsız YOK). Altı-kanal (OpenAlex ·
Semantic Scholar · Minerva · YÖK Akademik · Google Scholar/SerpApi · YÖK Tez) + 12-aday
tam-metin (method-düzeyi) doğrulaması: karşılaştırma-boyutlu 4-faktörlü formun
method-doğrulanmış **dört** kullanıcısı, iki araştırmacı soyağacı (Temel/Altan-Atalay →
Sümer & Engin 2004; Çalışkan/Şahin-Acar → Sümer, Gündoğdu-Aktürk & Helvacı 2010 = tezin
atfı). Ayrıca bkz. `arrindell1999sembu` köken notu ve `sumer2010anneBabaTutum`.

| Citation key | DOI/ID | Zotero item key | Tam metin kanıtı | Kullanılan iddia | Bölüm | Nitel AI | Nicel AI | Durum | Not |
|---|---|---|---|---|---|---|---|---|---|
| `caliskanSari2018embuC` | DOI: `10.7816/nesne-06-12-02` | `TTFJKJP9`; not `M5IT8K5I`; URL attachment `6SBIQIUJ` | avesis-S3 tam-metin PDF s.35–37 (bu oturum): EMBU-C 4'lü Likert + EMBU-P 6'lı, Karşılaştırma alt ölçeği dâhil; atıf Sümer, Gündoğdu-Aktürk & Helvacı (2010) | Karşılaştırma-boyutlu 4-faktörlü s-EMBU'nun eşlenik anne–çocuk formuyla kullanım öncülü (tezin metodolojik ikizi; EMBU-C 4'lü Likert bizimkiyle aynı) | `GEREÇ ve YÖNTEM` | ch03 re-cert'te | ch03 re-cert'te | `reliability-ok` | 2026-07-29: Zotero import tamam (koleksiyon `9ZFDHMZA`, DOI+kanıt notu+URL attachment); `zotero_reconcile_bib` bib↔Zotero temiz; BibTeX key `caliskanSari2018embuC` pin'lendi. İki-kol AI-reliability ch03 yeniden-sertifikasyonunda (`/tez-dogrulama` + `t1dm-qual-ai-audit`) koşulunca `cite-ok`. Verbatim kopya yok (telif). |
| `temelAltanAtalay2018selfCompassion` | DOI: `10.1007/s12144-018-9904-9` | `2UEJ2Z6Q`; not `FCET2CU3`; URL attachment `BQCAUSK8` | WebFetch PDF + Minerva-indexed (bu oturum): s-EMBU-C 4-faktör, Karşılaştırma α=0,85; atıf Sümer & Engin (2004) | Karşılaştırma-boyutlu 4-faktörlü s-EMBU'nun yayınlanmış kullanım öncülü | `GEREÇ ve YÖNTEM` | ch03 re-cert'te | ch03 re-cert'te | `reliability-ok` | 2026-07-29: Zotero import tamam (koleksiyon `9ZFDHMZA`, DOI+kanıt notu+URL attachment); `zotero_reconcile_bib` bib↔Zotero temiz; BibTeX key `temelAltanAtalay2018selfCompassion` pin'lendi. İki-kol AI-reliability ch03 yeniden-sertifikasyonunda koşulunca `cite-ok`. |
