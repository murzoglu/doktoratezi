# GENEL BİLGİLER — Kapsamlı Bölüm Talimatnamesi

Durum: `textbook-taslak-zenginlestirildi`

Veri kesim tarihi: 2026-07-02

> **Kanonik kural otoritesi:** Bölüm içerik kuralı →
> `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` §3.4 (genelden
> özele; güncel/güvenilir literatür; **yorum ve sonuç çıkarımından kaçınılır**;
> `GEREÇ ve YÖNTEM`e doğal geçiş); alt başlık → §1.3; atıf → §1.8; tez-kaynak
> yasağı → §4.2. Bu dosya bu teze özgü **kapsamlı yürütme talimatnamesi**dir;
> kural tanımlamaz. Klasör haritası: `03_bolum-hazirlik/README.md`.

## Bölüm İşlevi

`GENEL BİLGİLER`, tezin kuramsal ve ampirik arka planını genelden özele
kurar. Bu bölümde çalışma sonuçları yorumlanmaz; hipotez sonuçları, nitel
temalar ve karma yöntem bütünleştirmesi yalnız kavramsal zemine bağlanır.
Yorum, etki büyüklüğü tartışması ve kanıt bütünleştirme dili `TARTIŞMA ve SONUÇ`
bölümüne bırakılır.

Bu bölümün üretim hedefi, `GİRİŞ ve AMAÇ` bölümünde kurulan problem ve amaç
cümlelerini tekrarlamadan `GEREÇ ve YÖNTEM` bölümündeki tasarım, örneklem,
ölçekler ve karma yöntem gerekçesini anlaşılır kılmaktır.

## Yazım Sınırları

- Ham klinik veri, satır düzeyi veri, ham nitel transcript, aile düzeyi hassas
  ayrıntı veya doğrudan alıntı kullanılmaz.
- Nitel repo yalnız kanonik tema/denetim katmanı olarak kullanılır; ayrıntılı
  nitel bulgu anlatımı `BULGULAR` ve `TARTIŞMA ve SONUÇ` bölümlerine kalır.
- Bölüm resmi kılavuza uygun biçimde alt başlıkla yapılandırılabilir.
- Görünür tez metninde araç, connector, MCP, API çağrısı, sorgu DSL'i veya
  operasyonel telemetri yer almaz; bunlar yalnız hazırlık ve sertifikasyon
  kayıtlarında tutulur.
- T1DM biyolojisi kısa pediatrik bağlam düzeyinde kalır; genetik, farmakoloji,
  ilaç geliştirme, regülasyon, DDI ve mekanistik omics katmanları açık yazım
  ihtiyacı olmadıkça dışarıda bırakılır.

## Alt Başlık Omurgası

Bu sürümde `chapters/02_genel_bilgiler.qmd`, yalnız dar literatür arka planı
değil, tezin tüm temel kavramlarını bulgu vermeden açıklayan ders kitabı
niteliğinde bir bölüm olarak yazılmıştır.

| Alt başlık | Yazım işlevi | Tez bağlantısı | Kaçınılacak taşma |
|---|---|---|---|
| `2.1 Çocukluk Çağında Tip 1 Diyabet` | T1DM tanımı, kısa patofizyoloji, klinik seyir, öz yönetim, insülin, glukoz izlemi, HbA1c ve teknoloji. | Klinik bağlam, HbA1c ve hastalık süresi değişkenleri. | Tedavi protokolü veya ilaç/farmakoloji ayrıntısı. |
| `2.2 Pediatrik T1DM'de Psikososyal Bakım` | ADA/ISPAD çizgisinde yaşam kalitesi, diyabet sıkıntısı, hipoglisemi korkusu, okul, akran ve özerklik. | Psikososyal değişkenlerin tıbbi bakım bağlamından kopmaması. | Müdahale önerisi veya sonuç yorumu. |
| `2.3 Türkiye Bağlamında Pediatrik T1DM` | Türkiye'de bakım ekosistemi, aile eğitimi, okul/teknoloji erişimi, YÖK tez katmanı ve yerel literatür görünürlüğü. | Türkiye örnekleminin yorum zemini. | Tek tip kültürel genelleme. |
| `2.4 Çocukluk ve Ergenlik Döneminde Kronik Hastalık` | Gelişimsel görevler, beden algısı, akran yaşamı, tedaviye uyum ve özerklik. | Yaş, kardeş yaşı, tanı yaşı ve DM süresinin kavramsal yeri. | Yaşa göre çalışma bulgusu vermek. |
| `2.5 Aile Sistemleri ve Kronik Hastalık` | Aile rolleri, rutin değişimi, bakım yükü ve anne merkezli bakım emeği. | Anne, hasta çocuk ve kardeşi aynı aile bağlamında düşünmek. | Baba/diğer bakım verenleri yok saymak. |
| `2.6 Ebeveynlik Kuramları` | Sıcaklık, kontrol, kabul-red, bağlanma, özerklik desteği ve aşırı koruyuculuk. | EMBU boyutlarının kuramsal zemini. | T1DM bulgularını önden tartışmak. |
| `2.7 Algılanan Ebeveynlik ve EMBU Çerçevesi` | EMBU-P/C, duygusal sıcaklık, reddetme, aşırı koruma, karşılaştırma/ayrımcılık. | Anne öz-bildirimi ile çocuk algısı ayrımı. | Ölçek skor sonuçları. |
| `2.8 T1DM Bağlamında Ebeveynlik` | Hastalık yönetimi, izlem, uyarı, kontrol ve güvenlik davranışlarının çift anlamlılığı. | T1DM'ye özgü ebeveynlik ve çoklu bilgi kaynağı bağlamı. | Nedensel iddia. |
| `2.9 Anne Depresif Belirtileri` | Beck bağlamında depresif belirti dili, bakım stresi, suçluluk ve tükenmişlik. | Anne ruhsal yükü ve ebeveynlik algısı ilişkisi. | Klinik tanı veya tedavi dili. |
| `2.10 Anne Depresif Belirtileri ve Ebeveynlik Yolları` | Sıcaklık, reddetme, aşırı koruma, sosyal istenirlik ve öz-eleştiri yolları. | Beck-EMBU-P ilişkisinin kavramsal zemini. | Antidepresan veya klinik tanı sonucu yorumlamak. |
| `2.11 Sağlıklı Kardeş Deneyimi` | Görünmez yük, ilgi adaleti, kıskançlık, koruyuculuk, teknoloji alarmı ve dahil edilme. | Sağlıklı kardeşin bağımsız aile üyesi ve bilgi kaynağı olarak konumu. | Kardeşi tek yönlü mağduriyet anlatısına indirgemek. |
| `2.12 Kardeş İlişkileri ve KİA/SRQ` | Sıcaklık/yakınlık, çatışma, rekabet, statü/güç, yaş farkı ve doğum sırası. | KİA/SRQ'nun kavramsal boyutları. | KİA sonuçlarını vermek. |
| `2.13 Sosyoekonomik ve Kültürel Bağlam` | SES, anne eğitimi/çalışma durumu, teknoloji ve sağlık hizmetine erişim. | Kovaryat ve bağlam değişkenleri. | Kültürü tek değişken gibi kullanmak. |
| `2.14 Demografik ve Klinik Değişkenlerin Kavramsal Yeri` | Yaş, aile büyüklüğü, DM süresi, tanı yaşı ve HbA1c. | Analizlerdeki bağlamsal değişkenler. | Bulgu tablosunu önden yazmak. |
| `2.15 Ölçüm Araçlarının Kuramsal Temeli` | EMBU-P/C, Beck, KİA/SRQ ve demografik-tıbbi formun neyi ölçtüğü; ebeveynlik, depresif belirti ve kardeş ilişkisi için mevcut alternatif ölçek aileleri; Türkiye validasyon/uyarlama katmanı. | Ölçek seçiminin gerekçesi, hangi ölçüm için hangi araç ailesinin uygun olduğu ve tez araçlarının sınırları. | Tez örneklemindeki psikometrik sonuçları veya kesme noktası sınıflamalarını vermek. |
| `2.16 Psikometrik Kavramlara Kısa Giriş` | COSMIN ölçüm özellikleri, içerik/yapısal geçerlik, güvenirlik katsayılarının sınırları, uçta yığılma, ölçüm değişmezliği, latent değişken ve Türkiye validasyonu ayrımı. | Ölçek puanlarının kavramsal yorum sınırı. | Formül yoğun yöntem anlatısı, estimator adı veya bulgu düzeyi model uyumu. |
| `2.17 Çoklu Bilgi Kaynağı Yaklaşımı` | Anne, çocuk ve kardeş bildirimlerinin birbirinin yerine geçmemesi. | Triadik aile bakışı ve role özgü algılar. | Informant farklarını hata diye yazmak. |
| `2.18 Diadik Uyum ve Tutarsızlık` | Anne ve çocuk bildirimlerinin benzerlik/ayrışma anlamı; uyumun tek bir sayıdan ibaret olmaması. | Anne-çocuk algı farklarının aile konumu olarak okunması. | Analiz adı, katsayı, yöntem uygulaması veya hipotez sonucu. |
| `2.19 Triadik Aile Tasarımı` | Anne-hasta çocuk-sağlıklı kardeş üçgeni ve aynı olayın üç konumdan görülmesi. | Nitel triadik görüşmelerin gerekçesi. | Ham alıntı veya tema bulgusu. |
| `2.20 Karma Yöntem Mantığı` | Nicel ölçekler ve nitel anlatıların tamamlayıcılık/ayrışma mantığı. | Farklı kanıt türlerini birlikte okuma zemini. | Nitel veriyi nicelin kanıtı gibi sunmak veya bütünleştirme tekniği anlatmak. |
| `2.21 Bağlam Değişkenleri ve Yorum Sınırları` | SES, anne eğitimi, aile büyüklüğü, yaş farkı, DM süresi ve HbA1c'nin bağlamsal anlamı. | Bulguların aile ve klinik bağlamdan kopmadan okunması. | Model, eksik veri yöntemi veya teknik duyarlılık analizi anlatmak. |
| `2.22 Keşifsel Okuma ve Kanıt Dili` | Hipotez, ikincil gözlem, ölçüm özelliği, nitel tema ve literatür bağlantısının farklı kanıt ağırlığı. | Sonuç dilinin temkinli kurulması. | Analiz adı, ek yöntem listesi veya doğrulayıcı sonuç iddiası. |
| `2.23 Etik, Açık Bilim ve Veri Mahremiyeti` | Çocuk sağlık verisi, KVKK, açık bilim-mahremiyet dengesi ve ham verinin paylaşılmaması. | Veri mahremiyeti ve açık bilim. | Yöntem bölümündeki onam/prosedür ayrıntısı veya araç/iş akışı anlatısı. |
| `2.24 Tezin Kavramsal Sentez Modeli` | T1DM'nin aile düzenini değiştirmesi ve bunun ebeveynlik, anne ruhsal yükü, kardeş ilişkisi ve çoklu bilgi kaynağı farklarında görünmesi. | Bölüm sonu kavramsal model. | Tartışma sonucunu önden vermek. |

## Önerilen Anlatı Akışı

1. Bölüm T1DM'nin pediatrik kronik bakım doğasıyla açılır; hastalık yalnız
   glisemik yönetim değil, çocuk ve aile yaşamını düzenleyen uzun süreli bir
   bağlam olarak tanıtılır.
2. Psikososyal bakım ve Türkiye bağlamı, uluslararası kılavuzlar ile yerel
   bakım ekosistemi arasında köprü kurar. YÖK tezleri bu noktada hakemli
   kanıtın yerine değil, Türkiye'de hangi kavramların çalışıldığını gösteren
   yerel literatür katmanı olarak kullanılır.
3. Çocukluk/ergenlikte kronik hastalık ve aile sistemi başlıkları, bakım
   yükünün aile rollerini ve anne merkezli emeği nasıl yapılandırabileceğini
   açıklar.
4. Ebeveynlik kuramları, EMBU çerçevesi ve T1DM bağlamında ebeveynlik
   başlıkları, bakım güvenliği ile özerklik-kontrol gerilimini kuramsal olarak
   birleştirir.
5. Anne depresif belirtileri, sağlıklı kardeş deneyimi, kardeş ilişkileri ve
   SES/demografik-klinik değişkenler, çalışma değişkenlerinin neden ayrı ayrı
   değil aynı aile bağlamında okunacağını gösterir.
6. Ölçüm araçları, psikometri, çoklu bilgi kaynağı, diadik uyum, triadik tasarım
   ve karma yöntem bölümleri okuyucuyu kavramsal olarak hazırlar; teknik
   analiz ayrıntılarını yöntem bölümüne bırakır.
7. Bağlam değişkenleri, kanıt dili, etik/açık bilim ve sentez modeli bölümün
   son katmanını oluşturur; burada sonuç yorumu yapılmaz.

## Evidentia D0-D6 Uygulama Protokolü

Bu bölüm için Evidentia kapsamı `t1dm_psychosocial_thesis` profiliyle
sınırlandırılır. Varsayılan aktif katman akademik literatür, tam metin,
Türkiye/YÖK ve Zotero mutabakatıdır. İlaç, farmakoloji, regülasyon,
TİTCK/SGK, DDI, HTA, klinik trial ve omics katmanları açık tetikleyici
yoksa çağrılmaz.

| Faz | Uygulama kararı | Çıktı |
|---|---|---|
| D0 Kapsam | Popülasyon: 7-17 yaş T1DM tanılı çocuklar, sağlıklı kardeşler, anneler ve karşılaştırma aileleri. Kavramlar: ebeveynlik, depresif belirti, bakım yükü, kardeş ilişkisi, çoklu bilgi kaynağı, triadik aile tasarımı, karma yöntem. | Kapsam dışı: erişkin diyabet, T2DM-only, ilaç/farmakoloji, genetik/omics, yalnız tedavi müdahalesi, hasta düzeyi öneri. |
| D1 Bibliyografik tarama | PubMed/Europe PMC, OpenAlex/Semantic Scholar citation graph, YÖK Tez ve mevcut Zotero kütüphanesi birlikte taranır. | Aday kaynak listesi DOI/PMID/YÖK ID ile çıkarılır. |
| D2 Semantik genişletme | Seed kaynaklardan benzer çalışmalar, atıf veren/atıf yapılan kaynaklar ve sistematik derlemeler bulunur. OpenAlex veya Semantic Scholar 429/5xx verirse PubMed related ve EPMC alternatif kullanılır. | Aynı iddiayı destekleyen, çelişen veya dolaylı kalan kaynaklar ayrılır. |
| D3 Rerank | Öncelik: güncel kılavuzlar ve sistematik derleme/meta-analizler; sonra T1DM'ye özgü nicel/nitel çalışmalar; en son kronik hastalık lateral kanıtları. | Her kaynak için çalışma tipi, popülasyon, aktarılabilirlik ve kullanılacak claim belirlenir. |
| D4 Tam metin | Nihai citation olacak her kaynak için PMC/EPMC, OpenAthens/yayıncı, Anna's/annas-reader veya legal OA kanıtı kapanır. | Tam metin yoksa `candidate` veya `full-text-exception`; metne citation olarak girmez. |
| D5 Çapraz doğrulama | Kılavuz, ebeveyn depresyonu, kardeş deneyimi ve multi-informant iddiaları en az iki kaynakla desteklenir veya dolaylı kanıt olarak etiketlenir. | Güçlü, sınırlı ve dolaylı claim ayrımı yapılır. |
| D6 Tez entegrasyonu | `references.bib`, Zotero item key, BibTeX key, ledger satırı ve bölüm metni eşleştirilir. | Final bölüm öncesi nitel + nicel AI-reliability ve Quarto render kapıları çalışır. |

## Arama Stratejisi

İngilizce akademik sorgular:

```text
("type 1 diabetes" OR T1D OR T1DM) AND (child* OR adolescent*) AND
(family functioning OR parenting OR parent-child) AND
(systematic review OR meta-analysis OR review)

("type 1 diabetes") AND parenting AND psychological health AND youth

("type 1 diabetes") AND (parent* OR caregiver*) AND
(depression OR depressive symptoms OR diabetes distress OR caregiver burden)

("type 1 diabetes") AND sibling* AND
(experience* OR needs OR adjustment OR relationship*)

("chronic illness" OR "chronic disease") AND sibling* AND child*
AND (systematic review OR review)

multi-informant child adolescent mental health parent child agreement
```

Türkçe/YÖK sorguları:

```text
tip 1 diyabet
diyabet çocuk ebeveyn
tip 1 diyabet anne depresyon
kronik hastalık kardeş ilişkileri
diyabetik çocuk kardeş
ebeveyn tutumu diyabet çocuk
tip 1 diyabet akran zorbalığı
tip 1 diyabet yaşam kalitesi teknoloji
```

Canlı YÖK notu: 2026-07-02 derinleştirilmiş YÖK Tez taramasında izinli tam
metin erişimi olan T1DM tezleri ebeveyn tutumu/öz bakım, ebeveyn izlemi,
diyabetin aileye etkisi, hipoglisemi korkusu, helikopter ebeveynlik,
psikolojik sağlamlık ve anksiyete/depresyon başlıklarında yoğunlaşmıştır.
Doğrudan T1DM tanılı çocukların sağlıklı kardeş deneyimini odağa alan yerel tez
sonucu saptanmamıştır; bu gözlem nihai boşluk iddiası değil, kardeş boyutunun
Türkiye tez literatüründe daha az görünür olabileceğine dair denetlenebilir
çalışma notudur.

## Kaynak Öncelik Matrisi

| Kaynak | Kimlik | Durum | Bölümde kullanılacak claim | Not |
|---|---|---|---|---|
| ADA Professional Practice Committee 2026 | DOI `10.2337/dc26-S014`; PMID `41358890`; PMCID `PMC12690182` | `cite-ok` | Pediatrik diyabet bakımında yaşa/gelişime uygun bakım ve psikososyal izlem bağlamı. | Zotero/ledger kapısı kapalı. |
| Bell ve Lain 2025 | DOI `10.1111/dom.16501`; PMID `40536127`; PMCID `PMC12312823` | `cite-ok` | Küresel T1DM epidemiolojisi, artan çocuk/ergen yükü, kayıt/veri boşlukları, DKA ve teknoloji bağlamının dikkatli yorumlanması. | PMC tam metin; çift reliability geçti. |
| ISPAD psikolojik bakım kılavuzu | DOI `10.1111/pedi.13428`; PMID `36464988`; PMCID `PMC10107478`; 2024 ISPAD Chapter 15 sayfası | `cite-ok` | Pediatrik diyabette psikolojik bakım ve aile/çocuk ruhsal gereksinimleri. | Peer-reviewed anchor ve resmi ISPAD web yüzeyi birlikte izlendi. |
| ISPAD 2024 glukoz izlem kılavuzu | DOI `10.1159/000543156`; PMID `39884260`; PMCID `PMC11854985` | `cite-ok` | BGM, CGM, AID, erken CGM başlatma, kapiller ölçümün kalan rolü ve teknoloji-aile yükü. | PMC tam metin; çift reliability geçti. |
| ISPAD 2022 diyabet eğitimi kılavuzu | DOI `10.1111/pedi.13418`; PMID `36120721`; PMCID `PMC10107631` | `cite-ok` | Yapılandırılmış diyabet eğitiminin sürekli, aileyi içeren ve psikososyal uyum/öz-yeterlik hedefli bir süreç olması. | PMC tam metin; çift reliability geçti. |
| ISPAD 2022 hipoglisemi kılavuzu | DOI `10.1111/pedi.13443`; PMID `36537534`; PMCID `PMC10107518` | `cite-ok` | Hipoglisemi ve hipoglisemi korkusunun fizyolojik-psikolojik bariyer, gece izlem ve kaçınma davranışı bağlamı. | PMC tam metin; çift reliability geçti. |
| Eviz ve ark. 2026 | DOI `10.4274/jcrpe.galenos.2025.2025-1-7`; PMID `41090400`; PMCID `PMC12989894` | `cite-ok` | Türkiye'de pediatrik T1DM bakımında ekip çalışması, aile eğitimi, yazılı plan, teknoloji ve ulusal veri sınırlılığı. | Zotero item `DZD64HM5`; çift reliability geçti. |
| Whittemore ve ark. | DOI `10.1177/0145721712445216`; PMID `22581804`; PMCID `PMC3401246` | `cite-ok` | T1DM ebeveynlerinde psikolojik sıkıntı, aile rutini ve bakım yükü. | `GİRİŞ ve AMAÇ` ledger'ında kapalı. |
| Crandell ve ark. | DOI `10.1037/fsh0000305`; PMID `29172624`; PMCID `PMC5880719` | `cite-ok` | Kronik fiziksel hastalığı olan çocuklarda ebeveynlik boyutları ve çocuk iyilik hali. | T1DM'ye dolaylı aktarılacak; nedensellik iddiası kurulmayacak. |
| Pinquart 2013 | DOI `10.1093/jpepsy/jst020`; PMID `23660152` | `cite-ok` | Kronik fiziksel hastalıkta ebeveyn-çocuk ilişkisi, kontrol ve aşırı koruyuculuk meta-analizi. | 2026-07-02 giriş koşusunda çift AI-reliability geçti; §2.5'te kullanıldı; ledger Bölüm sütunu GENEL BİLGİLER'e genişletildi. |
| Trojanowski ve ark. | DOI `10.1093/jpepsy/jsab064`; PMID `34657955` | `cite-ok` | T1DM gençlerinde ebeveynlik, aile çatışması/destek/ilişki kalitesi ve psikolojik sağlık. | OpenAthens/OUP resmi HTML tam metin kapısı kapalı. |
| Chen ve ark. 2023 | DOI `10.3389/fendo.2023.1095729`; PMID `36936139`; PMCID `PMC10014558` | `cite-ok` | T1DM çocuk/ergen ebeveynlerinde depresyon/depresif belirti prevalansı ve anne-baba farkları. | PMC ve Zotero/ledger kapısı kapalı. |
| Sangha ve ark. 2026 | DOI `10.3389/fcdhc.2026.1652578`; PMID `42368394`; PMCID `PMC13293899` | `cite-ok` | Ergen ve ebeveyn diabetes distress deneyiminin günlük yaşam, okul/akran, stigma, gelecek maliyeti ve sorumluluk devri bağlamında ilişkisel yaşanması. | PMC tam metin; çift reliability geçti. |
| Vieira ve ark. 2026 | DOI `10.3390/bs16060942`; PMID `42352775`; PMCID `PMC13295629` | `cite-ok` | Ebeveyn hipoglisemi korkusu, emotion regulation ve parental diabetes distress ilişkisini kesitsel/ilişkisel çerçevede kurmak. | PMC tam metin; nedensel dil yok; çift reliability geçti. |
| Quinn ve ark. 2026 | DOI `10.1007/s00125-026-06717-2`; PMID `42065735`; PMCID `PMC13236767` | `cite-ok` | Pediatrik T1DM erken tarama/risk bilgisinin aile kaygısı, ortak karar ve veri mahremiyeti boyutunu sınırlı etik arka plan olarak vermek. | PMC tam metin; tezin tanı almış çocuk odağı korunacak; çift reliability geçti. |
| Chan ve Shorey 2022 | DOI `10.1016/j.pedn.2021.12.002`; PMID `34929508` | `full-text-exception` | T1DM tanılı çocukların sağlıklı kardeşlerinin deneyim ve gereksinimleri. | Tam metin kapanmadığı için metinde final citation olarak kullanılmadı. |
| Lummer-Aikey ve Goldstein 2021 | DOI `10.1177/1074840720977177`; PMID `33305651` | `cite-ok` | Kronik hastalık bağlamında kardeş uyumu, baş etme, iletişim ve psikososyal uyum. | T1DM dışı/lateral kanıt olarak etiketlenecek. |
| De Los Reyes ve ark. 2015 | DOI `10.1037/a0038498`; PMID `25915035`; PMCID `PMC4486608` | `cite-ok` | Çoklu bilgi kaynağı yaklaşımında düşük-orta örtüşmenin bağlama özgü bilgi olarak yorumlanması. | Triadik aile bakışı için kavramsal anchor. |
| Ludvigsen ve Haugstvedt 2026 | DOI `10.1177/26350106261442180`; PMID `42159283`; PMCID `PMC13219770` | `cite-ok` | T1DM tanılı çocukların sağlıklı kardeşlerinde tanı dönemi, aile atmosferi, bilgi/dahil edilme gereksinimi ve teknoloji alarmı. | T1DM kardeş ekseninde tam metni açık güncel nitel anchor. |
| Mokkink ve ark. 2018 | DOI `10.1007/s11136-017-1765-4`; PMID `29260445`; PMCID `PMC5891552` | `cite-ok` | COSMIN ölçüm özellikleri, yapısal geçerlik, iç tutarlılık ve ölçüm değişmezliği çerçevesi. | PMC tam metin; kavramsal ölçüm arka planı olarak kullanılacak. |
| Putnick ve Bornstein 2016 | DOI `10.1016/j.dr.2016.06.004`; PMID `27942093`; PMCID `PMC5145197` | `cite-ok` | Configural/metric/scalar/residual ölçüm değişmezliği kavramsal açıklaması. | PMC tam metin; teknik formül anlatısına dönüştürülmeyecek. |
| Trizano-Hermosilla ve Alvarado 2016 | DOI `10.3389/fpsyg.2016.00769`; PMID `27303333`; PMCID `PMC4880791` | `cite-ok` | Cronbach alfa sınırları, omega ve congeneric/skewed madde koşullarında güvenirlik yorumu. | PMC tam metin; alfa tek başına geçerlik kanıtı değildir notu için. |
| Li 2016 | DOI `10.3758/s13428-015-0619-7`; PMID `26174714` | `cite-ok` | Likert tipi maddelerde yapısal geçerlik yorumuna kavramsal hazırlık. | Springer yayıncı tam metin ve PubMed kaydı doğrulandı. |
| Dirik, Yorulmaz ve Karancı 2015 | PMID `26111288`; Türk Psikiyatri Dergisi PDF | `cite-ok` | S-EMBU-C/KAET-Ç Türkçe psikometrik zemini ve algılanan ebeveynlik ölçümünün alternatif araçlarla ilişkisi. | Tezdeki 29 maddelik paralel EMBU-P/C ile birebir aynı form gibi yazılmayacak. |
| Hisli 1989 | Psikoloji Dergisi 7(23):3-13; açık PDF | `cite-ok` | Beck Depresyon Envanteri Türkçe geçerlik-güvenirlik zemini. | Taranmış PDF; klinik tanı veya kesme noktası sonucu olarak kullanılmayacak. |
| Aktürk ve ark. 2005 | Türkiye Aile Hekimliği Dergisi 9(3):117-122; açık erişim sayfası | `cite-ok` | BDI-PC/BDÖ-BB'nin Türkiye'deki kısa tarama alternatifi olarak konumu. | 21 maddelik Beck ile birebir eşdeğer gibi yazılmayacak. |
| Furman ve Buhrmester 1985 | PMID `3987418`; University of Denver PDF | `cite-ok` | SRQ/KİA için sıcaklık/yakınlık, göreli statü/güç, çatışma ve rekabet boyutları. | Açık PDF ve PubMed kaydı doğrulandı. |
| YÖK Apalaçi 1996 | YÖK Tez No. `52148` | `cite-ok` | KİA/SRQ'nun Türkiye uyarlama/kullanım tarihçesinde YÖK tez katmanı. | YÖK MCP details ve PDF gate doğrulandı; taranmış PDF nedeniyle OCR sınırlı. |
| Aktaş 2017 | DOI `10.21764/maeuefd.340206` | `cite-ok` | Türkiye'de kardeş ilişkileri için yerel ölçek geliştirme örneği. | DergiPark PDF tam metin; tezde kullanılan KİA/SRQ ile alternatif ölçek olarak ayrılacak. |
| YÖK Tuncay 2025 | YÖK Tez No. `935669` | `cite-ok` | Türkiye'de T1DM'li çocuk/ergenlerde ebeveyn tutumu, öz bakım ve hastalığa yönelik tutum. | YÖK izinli PDF page 1 erişimi, Zotero item `N3ZEJMDK`, çift reliability geçti. |
| YÖK Tatar 2023 | YÖK Tez No. `793371` | `cite-ok` | Türkiye'de T1DM'li ergenlerde ebeveyn izlemi ve diyabetin aileye etkisi. | YÖK izinli PDF page 1 erişimi, Zotero item `V5FAQHKR`, çift reliability geçti. |
| YÖK Avan 2017 | YÖK Tez No. `473884` | `cite-ok` | Ebeveyn izlemi, tedaviye uyum ve metabolik parametreler. | YÖK izinli PDF page 1 erişimi, Zotero item `EGSQ5W2Z`, çift reliability geçti. |
| YÖK Kesen Yener 2024 | YÖK Tez No. `915866` | `cite-ok` | Hipoglisemi korkusu çocuk ve ebeveyn formlarının geliştirilmesi. | YÖK izinli PDF page 1 erişimi, Zotero item `Z7VJNS2A`, çift reliability geçti. |
| YÖK Demirkıran 2025 | YÖK Tez No. `956108` | `cite-ok` | Helikopter ebeveynlik, diyabet yönetimi/öz yeterlilik, uyum, psikolojik sağlamlık ve anksiyete/depresyon. | YÖK izinli PDF page 1 erişimi, Zotero item `BETBXWXD`, çift reliability geçti. |
| YÖK Ayrancı 2025 | YÖK Tez No. `953420` | `cite-ok` | Diyabet yönetim yöntemi, akran zorbalığı, depresyon/anksiyete ve yaşam kalitesi kesişimini yerel okul-akran/psikososyal tez katmanı olarak göstermek. | YÖK izinli PDF page 1 erişimi, Zotero item `IFB9XK34`; çift reliability geçti. |
| YÖK Türk 2015 | YÖK Tez No. `448907` | `cite-ok` | Diyabet bakımında ebeveyn izlemi ölçeği geçerlik-güvenirliği. | YÖK izinli PDF page 1 erişimi, Zotero item `AWJNJ8HR`, çift reliability geçti. |
| YÖK Çetintaş 2019 | YÖK Tez No. `612448` | `cite-ok` | Diyabetin aileye etkisi ölçeği Türkçe geçerlik-güvenirliği. | YÖK izinli PDF page 1 erişimi, Zotero item `PQN4W2PK`, çift reliability geçti. |

## Repo İçi Kanıt Eşlemesi

| Tez bileşeni | Repo içi kaynak | Kullanım sınırı |
|---|---|---|
| Çalışma tasarımı ve örneklem | `docs/protokol/KLINIK_CALISMA_PROTOKOLU.md`; `docs/CLINICAL-STUDY-REPORT-FINAL.md` | Yöntem gerekçesi için aggregate düzey; sonuç yorumu yok. |
| Ölçekler | `docs/protokol/KANONIK_KISALTILMIS_EMBU_EBEVEYN.md`; `docs/protokol/KANONIK_KISALTILMIS_EMBU_COCUK.md`; `docs/protokol/KANONIK_BECK_DEPRESYON_ENVANTERI.md`; `docs/protokol/KANONIK_KARDES_ILISKILERI_ANKETI.md`; `dirik2015sEmbuTurkish`; `hisli1989bdiTurkishUniversity`; `akturk2005bdipcTurkish`; `furmanBuhrmester1985srq`; `apalaci1996yoktez`; `aktas2017kardesIliskileriOlcegi` | Kavram ve ölçüm alanı tanımı; alternatif araç aileleri; Türkiye validasyon/uyarlama katmanı. Tez örneklemindeki psikometrik sonuç tartışması yok. |
| Nitel temsil | `docs/niteliksel/qualitative_canonical_results_report.md` | Triadik aile tasarımını gerekçelendirmek için de-identified tema düzeyi; ham alıntı yok. |
| Kritik kaynak manifesti | `tez-yazim/06_kritik-kaynaklar/kritik-dosya-manifesti.tsv` | Hangi repo artefaktının hangi bölümde kullanılacağını denetler. |
| Referans ledgeri | `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` | DOI/PMID, full-text, Zotero key, claim ve reliability kapanışını izler. |

## Yazım Üretim Kuralları

- Her alt başlık bir konu cümlesiyle açılacak ve bir geçiş cümlesiyle
  sonraki alt başlığa bağlanacak.
- Atıflar, final yazımda yalnız `cite-ok` veya kapıları tamamlanmış yeni
  kaynaklardan verilecek.
- Sayısal prevalans veya etki büyüklüğü aktarılırsa kaynak popülasyonu,
  çalışma tipi, belirsizlik ve aktarılabilirlik sınırı aynı paragrafta
  belirtilecek.
- T1DM'ye özgü olmayan kronik hastalık kaynakları "dolaylı/lateral kanıt" olarak
  yazılacak; T1DM sonucu gibi sunulmayacak.
- Çoklu bilgi kaynağı farkları "hata" veya "uyumsuzluk" olarak peşinen
  değersizleştirilmeyecek; rol ve bağlam farkı olarak çerçevelenecek.
- `GİRİŞ ve AMAÇ` bölümündeki amaç ve hipotez paragrafları tekrarlanmayacak; bu bölüm
  araştırma sorularının neden ölçülebilir ve anlamlı olduğunu açıklayan arka planı verecek.

## Final Yazım Öncesi Kontrol Listesi

- [x] Her alt başlık için en az bir kılavuz, sistematik derleme/meta-analiz veya
      T1DM'ye özgü çalışma adayı belirlendi.
- [x] Her yeni citation için DOI/PMID/PMCID/YÖK ID veya resmi URL ledger'a
      yazıldı.
- [x] Her yeni citation için Zotero item key, BibTeX key ve `references.bib`
      mutabakatı kapandı.
- [x] Tam metin kanıtı olmayan kaynak metne citation olarak girmedi.
- [x] Türkiye/YÖK katmanı nihai boşluk iddiası kurulmadan önce genişletilmiş
      Türkçe/İngilizce terimlerle tekrarlandı.
- [x] Görünür tez metninde operasyonel tool/connector jargonu kalmadı.
- [x] Çalışma bulgusu, keşifsel sonuç, nitel quote veya satır düzeyi veri
      bu bölüme taşınmadı.
- [x] Bölüm sonu `GEREÇ ve YÖNTEM`e doğal geçiş yapıyor.

## Uygulama ve Doğrulama Komutları

Yazım aşamasında önerilen dar doğrulama sırası:

```bash
cd /mnt/thunderbolt/workspaces/doktoratezi
python3 scripts/util/zotero_env_bridge.py status --json
rg -n 'candidate|full-text-exception|zotero-ok|cite-ok' \
  tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md
quarto check
quarto render thesis.qmd
```

Referanslı bölüm kapanışında çift AI-reliability:

```bash
cd /mnt/thunderbolt/workspaces/T1DM\ Niteliksel
PYTHONDONTWRITEBYTECODE=1 python3 \
  plugins/t1dm-qual-ai-audit/skills/t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py

cd /mnt/thunderbolt/workspaces/doktoratezi
PYTHONDONTWRITEBYTECODE=1 python3 \
  plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/test_repo_ai_reliability.py
```

## Uygulama Notu - 2026-07-02 (entegre yapı koşusu)

- Bölüm, kanonik entegre yapı (Evidentia + `t1dm-tez-rehberi` +
  `niteliksel-arastirma-rehberi-t1dm`) içinde güncellendi. Operasyon kılavuzu:
  `T1DM Niteliksel/00_context/KANONIK_TEZ_YAZIM_PLAYBOOK.md` (tek entegre
  playbook; §6 tüm-MCP matrisi, §7 tam-metin araç kaskadı).
- İki `cite-ok` kaynak, bu briefin Kaynak Öncelik Matrisinde zaten GENEL
  BİLGİLER için planlanmıştı ve metne alındı — **yeni dış retrieval yapılmadı**:
  - §2.5 Aile Sistemleri → `@pinquart2013` (kronik hastalıkta aile yeniden
    örgütlenmesi; küçük fakat sistematik sıcaklık azalması / aşırı koruma artışı).
  - §2.6 Ebeveynlik Kuramları → `@crandell2017` (ebeveynlik boyutları ↔
    psikososyal sonuç; dolaylı/lateral kanıt, nedensellik iddiası kurulmadı).
- Her iki kaynak giriş'ten farklı, bölüme özgü kavramsal çerçeveyle yazıldı
  (giriş problem cümlesi tekrarı yok).
- Ledger `referans-denetim-ledgeri.md`: `pinquart2013` ve `crandell2017` Bölüm
  sütunu `GİRİŞ ve AMAÇ` → `GİRİŞ ve AMAÇ, GENEL BİLGİLER` olarak genişletildi;
  bu briefin matrisinde `pinquart2013` durumu `zotero-ok` → `cite-ok` düzeltildi.
- Harici MCP kullanılmadı (yalnız ledger yeniden kullanımı) → `/ai-kayit`
  gerekmedi. Kapanış: çift AI-reliability + `quarto render`.
- Bölüm statüsü taslak/`textbook-taslak-zenginlestirildi`; Kapı 0–5 bölüm
  sertifikasyonu bu sürüm için yeniden koşulmadı.
