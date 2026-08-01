# Tablolar Dizini — Detaylı İzahat (Ders Anlatır Gibi)

Bu belge, tezin **Tablolar Dizini**'ndeki her tabloyu `data-narrative` skill'iyle, teknik
doğruluğundan ödün vermeden, uzmanı olmayan zeki bir okurun anlayacağı netlikte açıklar.
Numaralandırma `outputs/quarto/thesis.pdf` **TABLOLAR DİZİNİ**'nden (resmî render) alınmıştır;
her sayı/etiket kaynağından (chapters/*.qmd) birebir teyit edilir. Kardeş belge (şekiller):
`DETAYLI-IZAHAT.md`.

## Tablo indeksi (thesis.pdf, TABLOLAR DİZİNİ)

| No | Kısa başlık | Bölüm | Sayfa |
|---|---|---|---|
| 2.1 | T1DM evrelemesi ve aile açısından anlamı | Genel Bilgiler | 10 |
| 2.2 | Ebeveynlik kuramlarının tarihsel-kavramsal gelişimi | Genel Bilgiler | 22 |
| 2.3 | EMBU ailesinin geliştirilme/uyarlanma tarihçesi | Genel Bilgiler | 25 |
| 2.4 | Ölçüm araçlarının kuramsal ve psikometrik özeti | Genel Bilgiler | 37 |
| 3.1 | q25 sözel yön + ters puanlama kararı | Gereç ve Yöntem | 56 |
| 3.2 | Doğrulayıcı hipotez çözümleme planı (birincil hat) | Gereç ve Yöntem | 63 |
| 3.3 | Kullanılan yapay zekâ araçları ve kategorileri | Gereç ve Yöntem | 77 |
| 4.1 | Örneklem özellikleri | Bulgular | 80 |
| 4.2 | Kovaryat dengesi | Bulgular | 81 |
| 4.3 | Eksik veri özeti | Bulgular | 81 |
| 4.4 | Eğilim skoru modeli + ortak destek | Bulgular | 81 |
| 4.5 | SES kompozit + latent SES CFA uyum | Bulgular | 82 |
| 4.6 | H1 doğrulayıcı grup ana etkisi (BH-FDR) | Bulgular | 87 |
| 4.7 | H1 çok düzeyli sabit etkiler | Bulgular | 87 |
| 4.8 | H1 Bayesçi çift raporlama | Bulgular | 87 |
| 4.9 | H2 aile-ortalama Welch testleri | Bulgular | 89 |
| 4.10 | H2 APIM sabit etkileri | Bulgular | 89 |
| 4.11 | H3 birincil + IPTW grup etkileri | Bulgular | 91 |
| 4.12 | H3 duyarlılık + çift raporlama | Bulgular | 91 |
| 4.13 | H4 Beck → EMBU-P SEM | Bulgular | 93 |
| 4.14 | H4 çok-grup ölçüm değişmezliği | Bulgular | 93 |
| 4.15 | H5 diadik tutarlılık stratejileri | Bulgular | 96 |
| 4.16 | Aracılık + koşullu süreç | Bulgular | 98 |
| 4.17 | LPA/LCA/Bifaktör model seçim tanıları | Bulgular | 99 |
| 4.18 | Ağ merkeziyet + NCT | Bulgular | 100 |
| 4.19 | Eşzamanlı klinik sınıflandırma performansı | Bulgular | 102 |
| 4.20 | DM klinik alt-analizleri | Bulgular | 106 |
| 4.21 | H1 dönem duyarlılığı (2023 alt örneklem) | Bulgular | 113 |
| 4.22 | Robustluk: çoklu evren + TOST | Bulgular | 117 |
| 4.23 | Ölçülmemiş karıştırıcı + falsifikasyon | Bulgular | 117 |
| 4.24 | Bayesçi çift raporlama (global) | Bulgular | 119 |
| 4.25 | Genel bulgu sentezi | Bulgular | 128 |
| 5.1 | Veri toplama yılı × grup dağılımı | Tartışma/Ek | 150 |
| 5.2–5.5 | Ölçüm değişmezliği eksen-bazlı uyum (WLSMV; dört eksen alt-tablosu) | Tartışma/Ek | 175–176 |
| 5.6 | H3 eşdeğerlik (TOST) SESOI duyarlılığı | Tartışma/Ek | 177 |
| 5.7 | Bayesçi grup etkisi: önsel merkez duyarlılığı | Tartışma/Ek | 178 |

> Not: dizinde 5.x bloğunda ölçüm değişmezliği alt-tabloları eksen başına tekrar
> numaralandığından (5.2–5.5) küçük bir numara belirsizliği vardır; içerik tektir.

---

# Tablo 2.1'i Anlamak — Basitçe, Ama Eksiksiz

**Tablo 2.1 = T1DM'nin evrelemesi ve her evrenin aile açısından anlamı**
Kanonik etiket: `@tbl-t1dm-evreleme` · Kaynak: chapters/02_genel_bilgiler.qmd:17-23 · Aile:
kavramsal/referans tablo.

## Bu tablo hangi soruna çözüm?

Tip 1 diyabet "bir anda başlayan" bir hastalık gibi görünse de, aslında **kademeli** ilerler.
Bu tez ailedeki ebeveynlik tutumunu incelediğinden, okurun önce "hastalığın hangi
aşamasında ailenin ne yaşadığını" görmesi gerekir. Tablo, tıbbi evreyi doğrudan **aile
deneyimine** bağlar.

Okuma hamlesi (referans tablo): **satırlar boyunca (Evre 1 → 3) ilerle, her evrede son
sütunun "aile açısından anlamı"nı oku** — tıbbi tanım ile ailevi yük yan yana.

## Tablo ne söylüyor?

| Evre | Biyolojik işaret | Aile açısından anlamı |
|---|---|---|
| Evre 1 | ≥2 otoantikor pozitif, glisemi normal, belirti yok | Belirsizlik yükü; tanı zamanı bilinmez |
| Evre 2 | ≥2 otoantikor pozitif, disglisemi, belirti yok | Yakın izlem; artan bakım-veren kaygısı |
| Evre 3 | Aşikâr hiperglisemi, sıklıkla semptomatik | Tanı krizi; aile rutininin yeniden örgütlenmesi |

İçerik [chapters/02_genel_bilgiler.qmd:19-21], kaynak [@dimeglio2018t1d; @haller2024ispadScreeningStaging].

**Ders:** hastalık presemptomatik evreden (Evre 1-2) aşikâr diyabete (Evre 3) ilerlerken,
ailenin yükü "soyut belirsizlik"ten "somut kriz + rutin yeniden kurulumu"na dönüşür. Bu,
tezin ebeveynlik tutumunu neden hastalık bağlamında okuduğunu temellendirir.

## Bir cümleyle

> Tablo 2.1, T1DM'nin biyolojik evrelerini (otoantikor/glisemi/belirti) her evrenin aile
> için anlamına (belirsizlik → izlem kaygısı → tanı krizi) bağlayarak, hastalığın ailevi
> yükünün kademeli ve evreye özgü olduğunu gösterir.

*Komşu öğe:* ölçüm araçları özeti `@tbl-olcum-ozet` (Tablo 2.4) aynı biçimde açılabilir.

---

# Tablo 2.2'yi Anlamak — Basitçe, Ama Eksiksiz

**Tablo 2.2 = Ebeveynlik kuramlarının tarihsel-kavramsal gelişimi**
Kanonik etiket: `@tbl-ebeveynlik-kuramlari` · Kaynak: chapters/02_genel_bilgiler.qmd:135-144 ·
Aile: kavramsal/soy-ağacı tablosu.

## Bu tablo hangi soruna çözüm?

"Ebeveynlik tutumu" tek bir kişinin icadı değil; on yıllar içinde birikmiş bir düşünce
zinciridir. Bu tezin kullandığı EMBU'nun (sıcaklık–reddetme–koruma eksenleri) **nereden
geldiğini** anlamadan, neden bu boyutların seçildiği havada kalır. Tablo, bu soy ağacını
kronolojik olarak dizer.

Okuma hamlesi: **satırları yukarıdan aşağıya (Schaefer 1959 → Rohner 2004) izle; son sütun
("bu teze katkısı") her kuramın EMBU'ya bıraktığı mirası verir.**

## Tablo ne söylüyor?

Zincir, iki büyük fikirde birleşir: (1) ebeveynliği **iki eksende** (sevgi–düşmanlık ×
özerklik–kontrol) düşünmek — Schaefer'in dairesel modeli, EMBU'nun kavramsal atası; (2)
odağı ebeveyn davranışından **çocuğun algısına** kaydırmak — Schaefer'in çocuk-bildirim
envanteri (CRPBI). Sonraki kuramlar (Baumrind talepkârlık × duyarlılık; Maccoby & Martin
dört-gözlü tipoloji; Darling & Steinberg tarz-uygulama ayrımı; Rohner kabul-red kuramı)
bu iki fikri derinleştirir [chapters/02_genel_bilgiler.qmd:137-142].

**Ders:** EMBU'nun "sıcaklık, reddetme, aşırı koruma" boyutları keyfî değildir; altı
kuramlık bir birikimimin damıtımıdır — özellikle Schaefer'in iki-eksen mirası ile
algı-odaklı ölçüm geleneği.

## Bir cümleyle

> Tablo 2.2, ebeveynlik tutumu kavramının Schaefer'in iki-eksenli modelinden Rohner'in
> kabul-red kuramına uzanan altı kuramlık gelişimini dizerek, bu tezde kullanılan EMBU
> boyutlarının bu kuramsal birikimden nasıl türediğini görünür kılar.

*Komşu öğe:* EMBU tarihçesi `@tbl-embu-gelisim` (Tablo 2.3) aynı biçimde açılabilir.

---

# Tablo 2.3'ü Anlamak — Basitçe, Ama Eksiksiz

**Tablo 2.3 = EMBU ailesinin geliştirilme ve uyarlanma tarihçesi**
Kanonik etiket: `@tbl-embu-gelisim` · Kaynak: chapters/02_genel_bilgiler.qmd:164-173 · Aile:
kavramsal/kronolojik tablo.

## Bu tablo hangi soruna çözüm?

Tez tek bir "EMBU" kullanmıyor; EMBU'nun **belirli bir sürümünü** (kısaltılmış, çocuk formu,
karşılaştırma boyutu eklenmiş) kullanıyor. Bu sürümün nasıl oluştuğunu bilmeden, ölçeğin
neden bu maddeleri/boyutları taşıdığı anlaşılmaz. Tablo, özgün EMBU'dan bugün kullanılan
forma uzanan zinciri verir.

Okuma hamlesi: **aşamaları yıl sırasına göre izle (1980 → 2010); her satırın "katkı"
sütunu ölçeğin bugünkü hâline ne eklediğini söyler.**

## Tablo ne söylüyor?

- **Özgün EMBU (1980, Perris ve ark.):** 81 madde, 15 boyut, retrospektif ebeveynlik anıları.
- **Boyut indirgeme (1983, Arrindell ve ark.):** yinelenebilir 3 faktör — sıcaklık, reddetme,
  aşırı koruma.
- **Kısaltılmış s-EMBU (1999, Arrindell ve ark.):** 23 madde, 3 faktörlü kısa form.
- **Çapraz-ulusal doğrulama (2005):** 3 faktörün kültürler arası tutarlılığı.
- **Çocuk formu EMBU-C (1993, Castro ve ark.):** çocuk uyarlaması + **karşılaştırma** boyutu.
- **Türkçe s-EMBU-C (2015, Dirik ve ark.):** 3 faktörlü çocuk formunun Türkçe geçerliği.
- **Karşılaştırma alt ölçeği (2010, Sümer ve ark.):** 5 maddelik karşılaştırma boyutunun
  eklenmesi [chapters/02_genel_bilgiler.qmd:166-172].

**Ders:** bu tezin dört boyutlu (sıcaklık, reddetme, aşırı koruma, **karşılaştırma**) 29
maddelik formu, iki ayrı katkının birleşimidir: Arrindell'in üç çekirdek faktörü + Castro/
Sümer çizgisindeki karşılaştırma boyutu. Dördüncü boyut (karşılaştırma) kardeş bağlamı için
kritiktir.

## Bir cümleyle

> Tablo 2.3, EMBU'nun 1980 özgün formundan bu tezde kullanılan dört boyutlu forma uzanan
> gelişimini dizerek, sıcaklık/reddetme/aşırı korumanın Arrindell çekirdeğinden,
> karşılaştırma boyutunun ise Castro/Sümer katkısından geldiğini gösterir.

*Komşu öğe:* ölçüm araçları özeti `@tbl-olcum-ozet` (Tablo 2.4) aynı biçimde açılabilir.

---

# Tablo 2.4'ü Anlamak — Basitçe, Ama Eksiksiz

**Tablo 2.4 = Çalışmada kullanılan ölçüm araçlarının kuramsal ve psikometrik özeti**
Kanonik etiket: `@tbl-olcum-ozet` · Kaynak: chapters/02_genel_bilgiler.qmd:330-336 · Aile:
ölçüm-aracı özet tablosu.

## Bu tablo hangi soruna çözüm?

Bir araştırmayı okurken ilk sorular: **hangi kavram, kimden, hangi araçla, hangi formatta
ölçüldü?** Tablo 2.4, çalışmanın tüm ölçüm araçlarını tek bakışta bu sütunlarla özetler —
puanları yorumlamadan önceki zorunlu haritadır.

Okuma hamlesi: **her satır bir araç; "kim doldurdu" (bilgi kaynağı) sütunu kritiktir** —
aynı kavramı farklı kaynakların bildirmesi, bu tezin çok-bilgi-verici tasarımının temelidir.

## Tablo ne söylüyor?

| Araç | Ne ölçer | Kim | Format |
|---|---|---|---|
| s-EMBU-C | Algılanan ebeveyn tutumu (4 boyut) | Çocuk (indeks + kardeş) | 29 madde, 4'lü Likert |
| s-EMBU-P | Öz-bildirilen ebeveyn tutumu (4 boyut) | Anne | 29 madde, 4'lü Likert |
| Beck Depresyon Envanteri | Depresif belirti şiddeti | Anne | 21 madde, 0–3 puan |
| KİA / SRQ | Kardeş ilişkisi (4 boyut) | Çocuk (indeks + kardeş) | Çok maddeli Likert |
| Demografik-tıbbi form | Aile/klinik/SES bağlamı | Aile/kayıt | Yapılandırılmış |

İçerik [chapters/02_genel_bilgiler.qmd:330-336].

**Ders + dürüstlük kapısı:** s-EMBU-P ve s-EMBU-C **paralel** madde yapısıdır — aynı davranış
dili iki perspektiften (anne öz-bildirimi ↔ çocuk algısı) okunur; tezin diadik uyum sorusu
(H5) buradan doğar. Önemli bir kaynak inceliği: Türkçe s-EMBU-C zemini için atıfta bulunulan
Dirik ve ark. (2015) çalışması, **bu tezdeki 29 maddelik dört-boyutlu form ile birebir aynı
form değildir**; arka plan/dilsel karşılık olarak okunur (bkz. Tablo 2.3) — bu ayrım tezde
açıkça belirtilir ve gizlenmez.

## Bir cümleyle

> Tablo 2.4, beş ölçüm aracını "ne ölçer / kim doldurur / hangi format" sütunlarıyla
> haritalar; s-EMBU'nun paralel anne–çocuk yapısı tezin çok-bilgi-verici (diadik) tasarımının
> temelidir ve Türkçe zemin kaynakları (Dirik 2015) birebir-aynı-form değil arka plan olarak
> konumlandırılır.

*Komşu öğe:* q25 ters puanlama `@tbl-q25-yon` (Tablo 3.1) aynı biçimde açılabilir.

---

# Tablo 3.1'i Anlamak — Basitçe, Ama Eksiksiz

**Tablo 3.1 = q25 maddesinin çocuk/ebeveyn formlarında sözel yönü ve ters puanlama kararı**
Kanonik etiket: `@tbl-q25-yon` · Kaynak: chapters/03_gerec_ve_yontem.qmd:68-73 · Aile: veri-
işleme/kodlama kararı tablosu.

## Bu tablo hangi soruna çözüm?

Paralel anne–çocuk formlarında bir madde iki formda **zıt sözel yönde** yazılmış olabilir.
Eğer bu fark düzeltilmezse, aynı davranış iki formda ters puanlanır ve karşılaştırma bozulur.
Tablo 3.1, tek bir maddede (q25) bu tuzağı ve nasıl çözüldüğünü belgeler — küçük ama
veri-bütünlüğü açısından kritik bir karar.

Okuma hamlesi: **iki satırı (çocuk formu ↔ ebeveyn formu) karşılaştır; "sözel yön" ile "ters
puanlama" sütunlarının neden farklı olduğunu gör.**

## Tablo ne söylüyor?

| Form | Sözel yön | Ters puanlama | Sonuç |
|---|---|---|---|
| Çocuk (s-EMBU-C) | İzin **verme** ("…izin verir mi?") | **Var** ($5-x$) | Yüksek final = daha yüksek aşırı koruma |
| Ebeveyn (s-EMBU-P) | **Kısıtlama** ("…hiç izin vermem") | **Yok** | Yüksek final = daha yüksek aşırı koruma |

İçerik [chapters/03_gerec_ve_yontem.qmd:70-71].

**Ders — veri bütünlüğü:** çocuk maddesi "izin verir mi?" (yani yüksek ham puan = *daha az*
aşırı koruma) diye yazıldığından ters puanlanır ($5-x$); ebeveyn maddesi "hiç izin vermem"
(yüksek ham puan = *daha çok* aşırı koruma) diye yazıldığından ters puanlanmaz. Bu düzeltme
sayesinde **her iki formda yüksek final puan aynı şeyi** — daha yüksek aşırı korumayı —
gösterir. Bu yapılmasaydı, anne–çocuk karşılaştırması bu maddede sistematik olarak yanlış
yönde olurdu.

## Bir cümleyle

> Tablo 3.1, q25 maddesinin çocuk ve ebeveyn formlarında zıt sözel yönde yazıldığını ve bu
> nedenle yalnız çocuk maddesinin ters puanlandığını (5−x) belgeler; böylece her iki formda
> yüksek final puan tutarlı biçimde daha yüksek aşırı korumayı gösterir.

*Komşu öğe:* çözümleme planı `@tbl-analiz-plani` (Tablo 3.2) aynı biçimde açılabilir.

---

# Tablo 3.2'yi Anlamak — Basitçe, Ama Eksiksiz

**Tablo 3.2 = Doğrulayıcı hipotezlerin çözümleme planı özeti (birincil hat)**
Kanonik etiket: `@tbl-analiz-plani` · Kaynak: chapters/03_gerec_ve_yontem.qmd:145-153 · Aile:
kavramsal/plan tablosu.

## Bu tablo hangi soruna çözüm?

Bir çalışmanın güvenilirliği, analizlerin **veriye bakmadan önce** planlanmış olmasına bağlıdır
(ön-kayıt mantığı). Tablo 3.2, beş doğrulayıcı hipotezin her biri için "hangi sonuç, hangi
modelle, hangi kovaryatlarla, hangi çokluk düzeltmesiyle" sınanacağını tek bakışta gösterir —
sonuçlara güvenmenin ön koşulu olan yol haritasıdır.

Okuma hamlesi: **her satır bir hipotez; "birincil model" ve "çoklu düzeltme" sütunları o
hipotezin sağlamlık zeminidir.**

## Tablo ne söylüyor?

| H | Sonuç | Birincil model | Çokluk |
|---|---|---|---|
| H1 | çocuk algısı (s-EMBU-C) | çok düzeyli model (aile rastgele etkisi) | BH-FDR |
| H2 | kardeş ilişkisi (KİA 4 boyut) | Welch t + APIM + diadik CFA | BH-FDR |
| H3 | anne öz-bildirimi (s-EMBU-P) | kovaryans analizi + eğilim skoru (HC3) | BH-FDR |
| H4 | anne depresyonu ↔ ebeveynlik | WLSMV ordinal SEM (latent) | BH-FDR |
| H5 | anne–çocuk diadik uyum | 5 paralel strateji | aile içi (≥3 strateji) |

İçerik [chapters/03_gerec_ve_yontem.qmd:147-151].

**Ders:** her hipotezin modeli soruya göre seçilmiştir — H1 aile-içi bağımlılık için çok
düzeyli, H4 latent kavramlar için ordinal SEM, H5 tek ölçütün kırılganlığına karşı **beş
paralel strateji** (güçlü bulgu için ≥3'ünün aynı yönde uyuşması önceden şart koşulmuş). H1–H4
çokluk düzeltmesi BH-FDR'dir. Bu tablo, sonraki bütün 4.x sonuç tablolarının **önceden
sabitlenmiş** çerçevesidir.

## Bir cümleyle

> Tablo 3.2, beş doğrulayıcı hipotezin her birinin sonuç değişkenini, soruya uygun birincil
> modelini, kovaryatlarını ve çokluk düzeltmesini önceden sabitleyerek, Bulgular'daki sonuç
> tablolarının dayandığı doğrulayıcı çerçeveyi belgeler.

*Komşu öğe:* örneklem özellikleri `@tbl-apa-sample-characteristics` (Tablo 4.1) aynı biçimde
açılabilir.

---

# Tablo 3.3'ü Anlamak — Basitçe, Ama Eksiksiz

**Tablo 3.3 = Tez sürecinde kullanılan yapay zekâ araçları ve kategorileri**
Kanonik etiket: `@tbl-ai-kullanim` · Kaynak: chapters/03_gerec_ve_yontem.qmd:233-242 · Aile:
şeffaflık/yönetişim tablosu.

## Bu tablo hangi soruna çözüm?

Bilimsel dürüstlük, yapay zekâ (YZ) araçlarının **hangi işlerde** kullanıldığını açıkça
beyan etmeyi gerektirir (ICMJE/COPE şeffaflık ilkesi). Tablo 3.3, kullanılan araçları,
sürümlerini ve kullanım kategorilerini belgeler — bir örtme değil, bir şeffaflık beyanıdır.

Okuma hamlesi: **hangi araç, hangi kategoride kullanıldı, ve sınır neresi (hangi veri asla
aktarılmadı)?**

## Tablo ne söylüyor?

- Araçlar: **ChatGPT** (OpenAI, GPT-4 sınıfı) ve **Claude** (Anthropic, Claude 4 sınıfı),
  2025–2026, kategoriler (i)–(vi) [chapters/03_gerec_ve_yontem.qmd:239-240].
- Kategoriler [:233]: (i) dil/üslup; (ii) raporlama standardı (APA 7/JARS/COREQ) ön-denetimi;
  (iii) bilimsel-metodolojik-istatistiksel iç tutarlılık + estimand/sonuç gözden geçirme;
  (iv) metin–tablo–şekil sayısal mutabakat; (v) kaynak/künye (DOI/PMID) doğrulama desteği;
  (vi) yeniden/duyarlılık analizi gerektirebilecek noktaların belirlenmesi.

**Ders + KVKK sınırı (dürüstlük kapısı):** yalnız **psödonimleştirilmiş nicel veri ve
toplulaştırılmış çıktı özetleri** (model katsayıları, uyum ölçütleri) ikincil kontrol için
kullanılmış; **kimliklendirilebilir hiçbir içerik** — ham nitel dökümler, saha notları,
demografik formlar, takma-ad eşleme anahtarları — YZ sistemlerine **aktarılmamıştır** [:233].
Bu, hem YZ-şeffaflığı hem KVKK sınırının açık beyanıdır.

## Bir cümleyle

> Tablo 3.3, tez sürecinde ChatGPT ve Claude'un altı tanımlı kategoride (dil, raporlama,
> tutarlılık, sayısal mutabakat, kaynak doğrulama, duyarlılık) kullanıldığını şeffafça
> beyan eder ve kimliklendirilebilir hiçbir verinin bu araçlara aktarılmadığını belgeler.

*Komşu öğe:* çözümleme planı `@tbl-analiz-plani` (Tablo 3.2) aynı biçimde açılabilir.

---

# Tablo 4.1'i Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.1 = Örneklem özellikleri**
Kanonik etiket: `@tbl-apa-sample-characteristics` · Kaynak: chapters/04_bulgular.qmd:534
(render) + :477-508 (anlatı) · Aile: betimsel/Tablo-1 (grup karşılaştırma).

## Bu tablo hangi soruna çözüm?

Herhangi bir grup karşılaştırmasından önce cevaplanması gereken ilk soru: **iki grup, ilgi
değişkeni dışında da farklı mı?** Tablo 4.1, DM ve kontrol ailelerini sosyodemografik, anne
ruh sağlığı, klinik ve psikolojik göstergelerde karşılaştırır ve her satırda grupların ne
kadar ayrıştığını **standardize ortalama fark (SMD)** ile verir.

Okuma hamlesi (Tablo 1 ailesi): **hangi satırlar gruplar arası dengesiz** — SMD sütununu
eşiğe göre tara; sonra bu dengesizliğin ayarlamayla nasıl ele alındığını sor.

## İşe yaradı mı? — Kanıt + büyüklük okuryazarlığı

SMD yorumu (Austin 2009; **gelenek, yasa değil**): |SMD| < 0,10 iyi denge; 0,10–0,25 sınırda;
0,25–0,50 dengesiz; ≥ 0,50 ciddi dengesizlik [chapters/04_bulgular.qmd:480-482].

| Değişken | SMD | Yorum |
|---|---|---|
| Anne antidepresan (DM %29 / kontrol %9) | 0,53 | ciddi dengesizlik ❌ |
| Eş eğitim düzeyi | 0,32 | dengesiz ⚠️ |
| Anne eğitim düzeyi | 0,29 | dengesiz ⚠️ |
| Eş mesleki indeks (ISEI-08) | 0,23 | sınırda |
| Anne yaşı | 0,21 | sınırda |
| **Latent SES kompoziti** | **0,03** | iyi denge ✓ |

Değerler [chapters/04_bulgular.qmd:484-494].

**Yanlış okumayı önceden düzeltelim:**
- *Ham dengesizlik ≠ yanlı sonuç.* Üç SES göstergesi tek tek dengesizken (0,29/0,32/0,23),
  birleşik latent SES dengeli (0,03) — çünkü ayarlama bu kompozit üzerinden yapılır.
- *Antidepresan dengesizliği (0,53) niye "düzeltilmiyor"?* Çünkü o bir **aracı** düğümdür
  (Şekil 4.2/Tablo 4.4 mantığı), karıştırıcı değil; ana modele konması etkinin bir kısmını
  görünmez kılardı.

## Bir cümleyle

> Tablo 4.1, DM ve kontrol ailelerinin birkaç ham değişkende (özellikle anne antidepresan
> SMD = 0,53) ayrıştığını, ancak nedensel ayarlama setinin çekirdeği olan latent SES'in
> dengeli olduğunu (SMD = 0,03) gösterir — ham dengesizlik, ayarlama stratejisiyle ele alınan
> bir tasarım sorunudur, sonucun yanlılığı değil.

*Komşu öğeler:* kovaryat dengesi `@tbl-apa-covariate-balance` (Tablo 4.2) ve nedensel harita
`@fig-causal-dag` (Şekil 4.2) aynı biçimde açılabilir.

---

# Tablo 4.2'yi Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.2 = Kovaryat dengesi (ağırlık öncesi / IPTW / eşleştirme)**
Kanonik etiket: `@tbl-apa-covariate-balance` · Kaynak: chapters/04_bulgular.qmd:540 (render) +
:497-501 (anlatı) · Aile: denge sonuç tablosu (Love grafiğinin sayısal karşılığı).

## Bu tablo hangi soruna çözüm?

Tablo 4.1 ham dengesizliği gösterdi. Tablo 4.2, **ayarlamanın işe yarayıp yaramadığını**
sayısal olarak belgeler: birincil ayarlama setindeki her değişken için ağırlık öncesi, IPTW
sonrası ve eşleştirme sonrası |SMD| ve IPTW kararı. (Şekil 4.3 bunun görselidir.)

Okuma hamlesi: **her değişkende |SMD| ağırlıktan *sonra* eşiğin altına indi mi?** Öncesi/
sonrası kıyası tablonun mesajıdır.

## İşe yaradı mı? — Kanıt

Birincil ayarlama seti = latent SES + kardeş yaş farkı + aile çocuk sayısı.

| Aşama | En büyük \|SMD\| | Eşik (0,10) | Yorum |
|---|---|---|---|
| Ağırlık öncesi | **0,220** (kardeş yaş farkı) | üstünde | ayarlama gerek ⚠️ |
| IPTW sonrası | **0,004** (latent SES) | çok altında | neredeyse sıfır ✓ |

Değerler [chapters/04_bulgular.qmd:497-501]. **0,220 → 0,004.**

**Yanlış okumayı önceden düzeltelim:** bu tablo **ayarlama setinin** dengesini gösterir;
Tablo 4.1'deki büyük ham dengesizlikler (ör. antidepresan 0,53) burada yer almaz çünkü onlar
ayarlama setinde değildir (aracı/tasarım kararı). Denge kazanımı bir nedensellik kanıtı değil,
gözlenen karıştırıcılarda karşılaştırmayı "elmayla elma"ya yaklaştıran bir tasarım katmanıdır.

## Bir cümleyle

> Tablo 4.2, birincil ayarlama setindeki en büyük grup farkının IPTW ile 0,220'den 0,004'e —
> denge eşiğinin belirgin altına — indiğini sayısal olarak belgeler; Şekil 4.3'ün sayısal
> karşılığıdır ve yalnız gözlenen karıştırıcılarda dengeyi gösterir.

*Komşu öğeler:* Love grafiği `@fig-smd-love` (Şekil 4.3) ve eğilim modeli
`@tbl-apa-propensity-model` (Tablo 4.4) aynı biçimde açılabilir.

---

# Tablo 4.3'ü Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.3 = Eksik veri özeti**
Kanonik etiket: `@tbl-apa-missing-data` · Kaynak: chapters/04_bulgular.qmd:546 (render) +
:515-524 (anlatı) · Aile: eksik veri sonuç tablosu.

## Bu tablo hangi soruna çözüm?

Sonuçlara güvenmenin bir ön koşulu, verinin ne kadarının gerçekten toplanabildiği ve
boşlukların nasıl ele alındığıdır. Tablo 4.3, değişken bazında analitik paydayı, analitik
eksik n/yüzdesini ve **çalışma tasarımından kaynaklanan yapısal boş hücreleri** ayrı ayrı
gösterir. (Şekil 4.6 bunun görselidir.)

Okuma hamlesi: **her satırda eksiklik analitik mi (gerçekten toplanamadı) yoksa tasarım
kaynaklı mı (tanım gereği yok)?** Bu ayrım tablonun kalbidir.

## Tablo ne söylüyor? — Kanıt

| Tür | Değişken | Oran | Yorum |
|---|---|---|---|
| Analitik | ISEI-08 mesleki indeks | %9,1 | en yüksek analitik eksik ⚠️ |
| Analitik | Beck toplam | %1,2 | düşük ✓ |
| Analitik | Maddi gösterge | %0,4 | ihmal edilebilir ✓ |
| Tasarım | DM süresi (aile düzeyi) | %50,2 | yapısal (yalnız DM'de) |

Değerler [chapters/04_bulgular.qmd:516-522].

**Yanlış okumayı önceden düzeltelim:** *tasarım kaynaklı boşluk ≠ analitik eksiklik.* DM süresi yalnız DM çocuklarında anlamlıdır; kontrol ailelerinde olmaması tanım gereğidir, "eksik veri" değildir. Bu yüzden bu boşluklar grup karşılaştırmalı imputasyonla doldurulmaz. Analitik eksiklik gerçekte çok düşüktür.

## Bir cümleyle

> Tablo 4.3, gerçek (analitik) eksikliğin çok düşük olduğunu (en yüksek ISEI-08 %9,1; Beck
> %1,2) ama DM bağlamına özgü zamanlama boşluklarının yapısal (analitik olmayan)
> olduğunu ve bilinçle impute edilmediğini belgeler.

*Komşu öğe:* eksik veri örüntüsü `@fig-missing-pattern` (Şekil 4.6) aynı biçimde açılabilir.

---

# Tablo 4.4'ü Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.4 = Eğilim skoru modeli ve ortak destek**
Kanonik etiket: `@tbl-apa-propensity-model` · Kaynak: chapters/04_bulgular.qmd:552 (render) +
:503-505 (anlatı) · Aile: model-katsayı + ortak-destek sonuç tablosu.

## Bu tablo hangi soruna çözüm?

Gözlemsel çalışmada grupları rastgele atayamadığımız için, "sanki rastgele atanmış gibi"
yapmayı istatistikle taklit ederiz. Bunun motoru **eğilim skorudur**: bir ailenin arka plan
özelliklerine bakarak DM grubunda olma olasılığı. Tablo 4.4, bu olasılığı üreten modeli (üst
kısım) ve karşılaştırmanın geçerli olduğu bölgeyi (ortak destek, alt kısım) belgeler.

Okuma hamlesi: **üst kısımda her yordayıcının OR'una ve %95 GA'sının 1'i içerip içermediğine
bak; alt kısımda ortak desteğin çakışma aralığını oku.**

## Tablo ne söylüyor?

- **Üst — eğilim modeli:** grup üyeliğini yordayan lojistik regresyon; girdiler DAG'dan:
  latent SES, kardeş yaş farkı, aile çocuk sayısı. Katsayılar **OR (%95 GA)** birimindedir.
  OR > 1 → o özellik DM grubunda olma olasılığını artırır; GA 1'i içeriyorsa yordayıcı sinyali
  belirsiz. (Kesin OR değerleri tablodadır; kaynak metinde sayı olarak geçmediğinden burada
  uydurulmaz.)
- **Orta — IPTW:** skorun tersiyle stabilize ağırlıklar (uç ağırlıklar 99. persentilde
  budanmış).
- **Alt — ortak destek:** DM ve kontrol eğilim dağılımlarının çakıştığı aralık [caption :553;
  :503-505]. (Görseli Şekil 4.4.)

**Numeracy + yanlış okumayı düzeltme:** OR = 1,8 kabaca "olasılık 1,8 kat" demektir ama düşük
taban oranında riske eşit değildir — abartma. Ve *ortak destek ≠ denge:* bu tablo
karşılaştırılabilirliğin ön koşulunu (örtüşme) verir; dengenin kendisini Tablo 4.2 (|SMD|
0,220→0,004) gösterir. Model bir nedensellik iddiası kurmaz.

## Bir cümleyle

> Tablo 4.4, aileleri arka plan özelliklerine göre DM/kontrol grubuna yerleştirme olasılığını
> (eğilim skoru) üreten lojistik modeli ve karşılaştırmanın geçerli olduğu ortak destek
> aralığını belgeler; bu, sonraki grup karşılaştırmalarını "elmayla elma"ya yaklaştıran
> tasarım katmanının motorudur, bir nedensellik iddiası değildir.

*Komşu öğeler:* kovaryat dengesi `@tbl-apa-covariate-balance` (Tablo 4.2) ve ortak destek
görseli `@fig-propensity-overlap` (Şekil 4.4) aynı biçimde açılabilir.

---

# Tablo 4.5'i Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.5 = SES kompozit bileşenleri ve latent SES CFA uyum ölçütleri**
Kanonik etiket: `@tbl-apa-ses-composite` · Kaynak: chapters/04_bulgular.qmd:558 (render) +
:492-495 (anlatı) · Aile: kompozit + CFA uyum sonuç tablosu.

## Bu tablo hangi soruna çözüm?

Sosyoekonomik durumu (SES) tek göstergeyle ölçmek kırılgandır ve gruplar arası dengesizdir.
Tablo 4.5, üç göstergeyi (eğitim, mesleki statü, materyal) tek bir **latent SES** ölçüsünde
birleştiren doğrulayıcı faktör analizini (CFA) ve bu birleştirmenin uyumunu belgeler.

Okuma hamlesi: **bileşenler latent SES'e güçlü/pozitif yükleniyor mu (kompozit geçerliği), ve
CFA uyum ölçütleri kabul bandında mı?**

## Tablo ne söylüyor? — büyüklük okuryazarlığı

- Üç ham SES göstergesi tek tek dengesizken (eğitim 0,29, eş eğitim 0,32, ISEI-08 0,23),
  birleşik latent SES gruplar arası dengelidir (**SMD = 0,03**) [chapters/04_bulgular.qmd:487-493].
- CFA uyum ölçütleri tabloda raporlanır; caption önemli bir inceliği açıklar: **birden büyük
  TLI değerleri örneklem oynamasından kaynaklanır ve iyi uyuma işaret eder; bazı yazılımlar
  raporlamada 1,00'a sınırlar** [caption :559]. (Uyum eşikleri Hu–Bentler 1999 geleneğidir;
  kesin yükleme/uyum değerleri tablodadır, burada uydurulmaz.)

**Yanlış okumayı önceden düzeltelim:**
- *TLI > 1 bir hata değildir* — küçük örneklemde olabilen, iyi uyuma işaret eden bir taşmadır;
  yazılım 1,00'a kırpabilir.
- *İyi uyum, "SES'i kusursuz ölçtük" demek değildir;* kompozit, bileşenlerini tutarlı
  özetler ve grup dengesi sağlar — amacı budur.

## Bir cümleyle

> Tablo 4.5, eğitim/mesleki statü/materyal göstergelerini tek bir latent SES ölçüsünde
> birleştiren CFA'nın iyi uyum verdiğini ve bu birleşik ölçünün — tek tek dengesiz bileşenlerin
> aksine — gruplar arası dengeli olduğunu (SMD = 0,03) belgeler; TLI > 1 bir hata değil iyi
> uyum işaretidir.

*Komşu öğe:* örneklem özellikleri `@tbl-apa-sample-characteristics` (Tablo 4.1) aynı biçimde
açılabilir.

---

# Tablo 4.6'yı Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.6 = H1 doğrulayıcı grup ana etkisi (dört EMBU-C alt ölçeği, BH-FDR)**
Kanonik etiket: `@tbl-apa-h1-group` · Kaynak: chapters/04_bulgular.qmd:659 (render) +
:608-616 (anlatı) · Aile: doğrulayıcı hipotez sonuç tablosu.

## Bu tablo hangi soruna çözüm?

H1'in **ön-kayıtlı doğrulayıcı** sorusu: DM ailelerindeki çocuklar (indeks + kardeş eşit
ağırlıkla) kontrol çocuklarına kıyasla farklı bir ebeveynlik mi algılıyor? Tablo 4.6, dört
EMBU-C boyutunda grup ana etkisini ve çokluk düzeltmeli anlamlılığı verir.

Okuma hamlesi: **her boyutta %95 GA sıfırı içeriyor mu, ve BH-FDR düzeltmeli q < 0,05 mü?**

## Tablo ne söylüyor? — Kanıt

| Alt ölçek | b (ölçek puanı) | %95 GA | BH-FDR q | Karar |
|---|---|---|---|---|
| Reddetme | 0,14 | [0,07; 0,22] | 0,001 | DM daha yüksek ✓ |
| Aşırı koruma | 0,19 | [0,07; 0,30] | 0,003 | DM daha yüksek ✓ |
| Sıcaklık | 0,14 | [0,02; 0,25] | 0,029 | sınırda anlamlı ⚠️ |
| Karşılaştırma | 0,13 | [−0,01; 0,26] | 0,069 | anlamlı değil ❌ |

Değerler [chapters/04_bulgular.qmd:611-617]. Dört boyuttan üçü BH-FDR sonrası anlamlıdır.

**Yanlış okumayı önceden düzeltelim — anlamlı ≠ sağlam.** Bu tablo frekansçı doğrulayıcı
sonuçtur; sinyallerin **sağlamlığı türdeş değildir**. Sıcaklık burada q = 0,029 ile anlamlı
görünse de Bayesçi çapraz-kontrol (Tablo 4.8) onu doğrulamaz. Dolayısıyla "üçü anlamlı"yı
"üçü de sağlam" diye okuma; sağlam olanlar reddetme ve aşırı korumadır.

## Bir cümleyle

> Tablo 4.6, H1 doğrulayıcı test ailesinde dört EMBU-C boyutundan üçünde (reddetme, aşırı
> koruma, sıcaklık) BH-FDR sonrası anlamlı grup farkı bulunduğunu belgeler; ancak sinyallerin
> sağlamlığı türdeş değildir ve nihai sağlamlık Bayesçi çapraz-kontrolle (Tablo 4.8) birlikte
> okunur.

*Komşu öğeler:* rol-özgül sabit etkiler `@tbl-apa-h1-primary` (Tablo 4.7) ve Bayesçi çift
raporlama `@tbl-apa-h1-bayesian` (Tablo 4.8) — aşağıda.

---

# Tablo 4.7'yi Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.7 = H1 çok düzeyli kovaryans analizi sabit etkileri (rol-özgül kontrastlar)**
Kanonik etiket: `@tbl-apa-h1-primary` · Kaynak: chapters/04_bulgular.qmd:665 (render) +
:626-634 (anlatı) · Aile: sabit-etki sonuç tablosu (betimsel ayrıştırma).

## Bu tablo hangi soruna çözüm?

Tablo 4.6 "grup ana etkisini" (indeks + kardeş ortalaması) verdi. Peki bu fark **hangi çocuk
rolünden** geliyor — hasta indeks çocuktan mı, sağlıklı kardeşten mi? Tablo 4.7, grup ana
etkisini rol-özgül hücrelere ayrıştırır.

Okuma hamlesi: **her rol-özgül kontrastta GA sıfırı içeriyor mu** — ama bunlar **betimsel**
ayrıştırmadır, ayrı bir düzeltme ailesi değildir.

## Tablo ne söylüyor? — Kanıt

Rol-özgül kontrastlar (kontrol indeks çocuğa göre) [chapters/04_bulgular.qmd:628-634]:

| Kontrast | b (ölçek puanı) | %95 GA |
|---|---|---|
| Reddetme — DM indeks | 0,15 | [0,05; 0,26] |
| Reddetme — DM kardeş | 0,13 | [0,03; 0,24] |
| Aşırı koruma — DM indeks | 0,20 | [0,05; 0,35] |
| Sıcaklık — DM kardeş | 0,16 | [0,02; 0,30] |

Ek çapraz-doğrulama: taban etkisine dayanıklı GRM reddetme farkını β = 0,14 SD ([0,04; 0,25])
düzeyinde doğrular; aile içi ICC ≈ 0,14 [:634-640].

**Yanlış okumayı önceden düzeltelim:** bu kontrastlar **düzeltilmiş q iddiası taşımaz** —
grup ana etkisinin (Tablo 4.6) betimsel/keşifsel ayrıştırmasıdır, ham katsayı ve GA ile
raporlanır. Rol × yaş × cinsiyet üçlü etkileşimi anlamsızdır (FDR p > 0,200), yani fark
çocuğun yaşı/cinsiyetine göre değişmez.

## Bir cümleyle

> Tablo 4.7, H1 grup ana etkisinin hem hasta indeks çocuk hem sağlıklı kardeş rollerinde
> (reddetme DM-indeks 0,15 / DM-kardeş 0,13; aşırı koruma DM-indeks 0,20) görüldüğünü betimsel
> olarak ayrıştırır; bu hücre kontrastları düzeltilmiş anlamlılık iddiası taşımaz, ana etkinin
> yön/büyüklük dökümüdür.

*Komşu öğeler:* grup ana etkisi `@tbl-apa-h1-group` (Tablo 4.6) ve Bayesçi hat
`@tbl-apa-h1-bayesian` (Tablo 4.8).

---

# Tablo 4.8'i Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.8 = H1 Bayesçi çift raporlama**
Kanonik etiket: `@tbl-apa-h1-bayesian` · Kaynak: chapters/04_bulgular.qmd:671 (render) +
:646-652 (anlatı) · Aile: Bayesçi sonuç tablosu (BF/pd/güvenilir aralık).

## Bu tablo hangi soruna çözüm?

Frekansçı analiz (Tablo 4.6) "etki yoktur"u doğrudan söyleyemez; yalnız "fark bulamadım" der.
Tablo 4.8, bağımsız bir **Bayesçi** hatla H1'i sınar ve iki kritik ayrımı yapar: "kanıt
yetersizliği" ile "etki-yokluğu lehine kanıt". Böylece hangi bulgunun *gerçekten* sağlam
olduğunu iki çerçevenin uzlaşmasıyla gösterir.

Okuma hamlesi: **her boyutta Bayes faktörü BF₁₀'ı Jeffreys ölçeğine oturt; BF₁₀ < 1 → H0
lehine oku.** Yön olasılığı pd 1'e ne kadar yakın?

## Tablo ne söylüyor? — büyüklük okuryazarlığı

BF₁₀ ölçeği (Jeffreys/Lee-Wagenmakers): 1–3 zayıf, 3–10 orta, 10–30 güçlü; **BF₁₀ < 1 → H0
lehine**.

| Alt ölçek | Posterior b | %95 güvenilir aralık | BF₁₀ | Kanıt |
|---|---|---|---|---|
| Reddetme | 0,16 | [0,06; 0,26] (pd = 0,999) | 10,55 | H1 lehine **güçlü** ✓ |
| Aşırı koruma | 0,21 | [0,06; 0,36] | 6,93 | H1 lehine **orta** ✓ |
| Sıcaklık | 0,09 | [−0,05; 0,23] | 0,29 | **H0 lehine orta** ❌ |
| Karşılaştırma | 0,13 | [−0,04; 0,30] | 0,53 | H0 lehine zayıf/anekdotal |

Değerler [chapters/04_bulgular.qmd:646-652].

**Yanlış okumayı önceden düzeltelim — en kritik ders:** sıcaklık, Tablo 4.6'da frekansçı
anlamlıydı (q = 0,029) ama burada BF₁₀ = 0,29 ile **H0 lehine** kanıt verir. İki çerçeve
ayrıştığında bulgu **sağlam sayılmaz**. Ayrıca "kanıt yetersizliği" (BF ≈ 1) ile "H0 lehine
kanıt" (BF₁₀ ≪ 1) farklıdır — Bayesçi hattın kattığı değer tam budur.

## Bir cümleyle

> Tablo 4.8, H1'in yalnız reddetme (BF₁₀ = 10,55, güçlü) ve aşırı koruma (BF₁₀ = 6,93, orta)
> boyutlarında iki çerçevede tutarlı biçimde doğrulandığını; sıcaklığın frekansçı
> anlamlılığına rağmen Bayesçi hatta H0 lehine (BF₁₀ = 0,29) çıktığını ve bu nedenle sağlam
> sayılmadığını belgeler.

*Komşu öğeler:* grup ana etkisi `@tbl-apa-h1-group` (Tablo 4.6) ve orman grafiği
`@fig-h1-forest` (Şekil 4.7).

---

# Tablo 4.9'u Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.9 = H2 aile-ortalama Welch testleri**
Kanonik etiket: `@tbl-apa-h2-family-mean` · Kaynak: chapters/04_bulgular.qmd:705 (render) +
:714-716 (anlatı) · Aile: grup karşılaştırma sonuç tablosu.

## Bu tablo hangi soruna çözüm?

H2, **kardeş ilişkisinin** dört boyutunda (yakınlık, güç, çatışma, rekabet) DM ve kontrol
aileleri arasında fark olup olmadığını sorar. En sade sınama, her ailenin iki kardeşinin
ortalamasını alıp iki grubu karşılaştırmaktır (Welch t). Tablo 4.9 bunu belgeler.

Okuma hamlesi: **her boyutta grup farkı ve etki büyüklüğü (d) ne; sıfırdan ayırt edilebiliyor
mu?**

## Tablo ne söylüyor? — büyüklük okuryazarlığı

Dört SRQ boyutunun **tamamında** grup farkı küçüktür: etki büyüklüğü **d < 0,20** (Cohen
geleneğinde "küçük"ün altı) [chapters/04_bulgular.qmd:714-716]; aile-ortalama testleri 241
aile üzerinden yürütülmüştür.

**Yanlış okumayı önceden düzeltelim — anlamsız ≠ etki yok.** Küçük ve anlamsız fark, "kardeş
ilişkisinde grup farkı yoktur" demek değildir; "mevcut örneklemde bir fark gösterilememiştir"
demektir (kanıt yokluğu ≠ yokluk kanıtı). Bu ayrımı doğrudan test edecek eşdeğerlik sınaması
(TOST) H2'de ön-kayıtlı olmadığından uygulanmamıştır.

## Bir cümleyle

> Tablo 4.9, kardeş ilişkisinin dört boyutunda DM–kontrol farkının küçük (d < 0,20) ve
> anlamsız olduğunu gösterir; bu, farkın yokluğunun kanıtı değil, mevcut örneklemde farkın
> gösterilemediğidir.

*Komşu öğe:* APIM sabit etkileri `@tbl-apa-h2-apim` (Tablo 4.10) aynı biçimde açılabilir.

---

# Tablo 4.10'u Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.10 = H2 APIM sabit etkileri**
Kanonik etiket: `@tbl-apa-h2-apim` · Kaynak: chapters/04_bulgular.qmd:711 (render) +
:717-723 (anlatı) · Aile: APIM sabit-etki sonuç tablosu.

## Bu tablo hangi soruna çözüm?

İki kardeşin ilişki algısı birbirinden bağımsız değildir. Aktör-partner karşılıklı bağımlılık
modeli (APIM), "kendi algım kendi çıktımı ne kadar belirliyor (**aktör**)" ile "kardeşimin
algısı benim çıktımı ne kadar belirliyor (**partner**)" etkilerini ayırıp grup farkını bu
yapıyı hesaba katarak sınar. Tablo 4.10, bu modelin sabit etkilerini verir.

Okuma hamlesi: **grup, rol ve grup × rol etkilerinin GA'ları sıfırı içeriyor mu?**

## Tablo ne söylüyor? — Kanıt

- APIM'de grup, rol ve grup × rol etkilerinin **hiçbiri anlamlı değildir**
  (FDR-düzeltilmiş **p > 0,350**) [chapters/04_bulgular.qmd:717-720].
- İki kardeşin yanıtlarını latent düzeyde ilişkilendiren Olsen-Kenny ayırt-edilebilir düad
  CFA'da, çatışma/kavga boyutundaki latent korelasyon **r = 0,27**'dir [:721-723].

**Yanlış okumayı önceden düzeltelim:** yine *anlamsız ≠ yok*; H2 dört boyut için bulgu "fark
yoktur" değil **"farkın varlığına ilişkin kanıt yetersizdir"** diliyle raporlanır (TOST
ön-kayıtlı değil). Ayrıca çift-yönlü latent korelasyon (r = 0,27) bir "etki" değil,
birlikte-değişimdir.

## Bir cümleyle

> Tablo 4.10, kardeşlerin karşılıklı etkisini modelleyen APIM'de grup/rol/grup × rol
> etkilerinin hiçbirinin anlamlı olmadığını (FDR p > 0,350) gösterir; kardeş çatışma algıları
> latent düzeyde orta düzeyde ilişkilidir (r = 0,27) ama bu bir grup farkı değildir.

*Komşu öğeler:* Welch testleri `@tbl-apa-h2-family-mean` (Tablo 4.9) ve APIM yol diyagramı
`@fig-h2-apim-path` (Şekil 4.8).

---

# Tablo 4.11'i Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.11 = H3 birincil ve IPTW grup etkileri**
Kanonik etiket: `@tbl-apa-h3-primary-iptw` · Kaynak: chapters/04_bulgular.qmd:750 (render) +
:755-762 (anlatı) · Aile: hipotez sonuç tablosu.

## Bu tablo hangi soruna çözüm?

H1'de **çocuklar** DM ailelerinde daha çok reddetme/aşırı koruma algıladı. H3, aynı soruyu
**annenin kendi ağzından** sorar: anne kendi ebeveynlik tutumunda grup farkı bildiriyor mu?
Tablo 4.11, dört EMBU-P boyutunda birincil ve ağırlıklandırılmış (IPTW) grup etkilerini verir.

Okuma hamlesi: **her boyutta GA sıfırı içeriyor mu; birincil ve IPTW sonuçları tutarlı mı?**

## Tablo ne söylüyor? — Kanıt

Dört EMBU-P boyutunda ham grup katsayıları (241 anne) [chapters/04_bulgular.qmd:756-760]:

| Alt ölçek | b (ölçek puanı) | %95 GA | Karar |
|---|---|---|---|
| Sıcaklık | 0,06 | [−0,07; 0,20] | anlamsız ❌ |
| Aşırı koruma | 0,06 | [−0,12; 0,24] | anlamsız ❌ |
| Reddetme | −0,05 | [−0,12; 0,02] | anlamsız ❌ |
| Karşılaştırma | 0,06 | [−0,08; 0,20] | anlamsız ❌ |

Dördü de anlamsız (FDR p > 0,500); standardize etki küçük (|β| < 0,17; en büyük mutlak
reddetmede β = −0,16). IPTW ile tekrarda katsayılar −0,04 ile 0,05 arası, yine anlamsız
(p > 0,510) — **birincil ve ağırlıklı sonuçlar tutarlı**.

**En önemli ders — bilgi-verici ayrışması:** H1 (çocuk) reddetme farkı bildirirken H3 (anne)
bildirmiyor. Bu çelişki değil, bilgi vericiye özgü geçerli bilgidir; fark **anne
öz-bildiriminde görünür olmuyor**.

## Bir cümleyle

> Tablo 4.11, annelerin kendi bildirdikleri dört ebeveynlik boyutunda DM–kontrol farkının
> birincil ve IPTW analizlerde tutarlı biçimde anlamsız kaldığını (hepsi FDR p > 0,500)
> gösterir; çocukların bildirdiği reddetme farkıyla (H1) birlikte okunduğunda bu, bir
> bilgi-verici ayrışmasına işaret eder.

*Komşu öğeler:* H3 duyarlılık `@tbl-apa-h3-sensitivity` (Tablo 4.12) ve katmanlı forest
`@fig-h3-stratified-forest` (Şekil 4.9).

---

# Tablo 4.12'yi Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.12 = H3 duyarlılık ve çift raporlama**
Kanonik etiket: `@tbl-apa-h3-sensitivity` · Kaynak: chapters/04_bulgular.qmd:756 (render) +
:762-776 (anlatı) · Aile: duyarlılık/Bayesçi/TOST katman tablosu.

## Bu tablo hangi soruna çözüm?

Tablo 4.11 "fark bulamadı". Ama "fark bulamamak" ile "fark yok demek" farklıdır. Tablo 4.12,
bu null bulguyu farklı katmanlarla sınar: antidepresan-katmanlı analiz, Bayesçi kanıt (BF/ROPE)
ve eşdeğerlik sınaması (TOST) — "gerçekten fark yok mu, yoksa güç mü yetmedi?" sorusunu yanıtlar.

Okuma hamlesi: **BF₁₀'ı Jeffreys ölçeğine oturt (BF₁₀ < 1 → H0 lehine); ROPE payı yüksek mi;
TOST kararı hangi sınıra bağlı?**

## Tablo ne söylüyor? — büyüklük okuryazarlığı

- **Katmanlar:** antidepresan kullanan (n = 46) ve kullanmayan (n = 195) anneler ayrı ayrı;
  sonuç bütün örneklemden farklılaşmaz [chapters/04_bulgular.qmd:762-767].
- **Bayesçi:** BF₁₀ = 0,17–0,23 → veri **H0 lehine orta düzeyde** kanıt sunar; ROPE (pratik
  eşdeğerlik) payı: sıcaklık %68, aşırı koruma %61, reddetme %93, karşılaştırma %69 [:768-772].
- **TOST (±0,30 SMD):** aşırı koruma ve karşılaştırma "Eşdeğer", sıcaklık ve reddetme
  "Belirsiz"; **ancak karar sınıra duyarlıdır** — daha katı ±0,20/±0,25 bantlarında hiçbir
  boyutta biçimsel eşdeğerlik kalmaz [:772-776].

**Yanlış okumayı önceden düzeltelim:** "Eşdeğer" mutlak değil, **SESOI'ye koşulludur**; katı
sınırda erir. Ama Bayesçi hattın "H0 lehine orta kanıt" (BF < 1) sonucu, H3 null'unun yalnız
"güç yetmedi" değil, gerçekten fark-yokluğu lehine olduğunu güçlendirir — özellikle reddetmede
ROPE %93.

## Bir cümleyle

> Tablo 4.12, H3 null bulgusunun antidepresan katmanlarında sabit kaldığını, Bayesçi hatta H0
> lehine orta kanıt (BF₁₀ = 0,17–0,23; reddetme ROPE %93) sunduğunu ve TOST eşdeğerliğinin
> yalnız ±0,30 sınırında geçerli — daha katı sınırlarda belirsiz — olduğunu belgeler.

*Komşu öğe:* H3 birincil `@tbl-apa-h3-primary-iptw` (Tablo 4.11) ve katmanlı forest
`@fig-h3-stratified-forest` (Şekil 4.9).

---

# Tablo 4.13'ü Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.13 = H4 Beck → EMBU-P latent yapısal eşitlik modeli (SEM)**
Kanonik etiket: `@tbl-apa-h4-sem` · Kaynak: chapters/04_bulgular.qmd:813 (render) +
:801-810 (anlatı) · Aile: SEM sonuç tablosu (yol katsayıları + uyum indeksleri).

## Bu tablo hangi soruna çözüm?

H4, annedeki **depresyon** ile annenin **ebeveynlik tutumları** arasındaki ilişkiyi sorar.
Ne depresyon ne de tutum doğrudan ölçülür; 50 madde (21 Beck + 29 EMBU-P) ile dolaylı yoklanır.
SEM, bu gürültülü maddelerin arkasındaki kavramları çıkarıp aralarındaki yolları tek bütünde
tahmin eder. Tablo iki yarıdan oluşur: **yapısal yollar** (asıl bulgu) ve **uyum indeksleri**
(modele güvenilir mi?).

Okuma hamlesi: **üstte her yolun β işaret/büyüklüğü + GA; altta uyum indekslerinin hepsini
birlikte oku (tek indekse kanma).**

## Tablo ne söylüyor? — Kanıt + büyüklük okuryazarlığı

**Yapısal yollar** — dörtten üçü FDR-anlamlı [chapters/04_bulgular.qmd:808-810]:

| Yol (Beck →) | β | %95 GA | FDR p | Yorum |
|---|---|---|---|---|
| Sıcaklık | −0,28 | [−0,45; −0,15] | < 0,001 | depresyon ↑ → sıcaklık ↓ ✓ |
| Reddetme | 0,33 | [0,19; 0,53] | < 0,001 | depresyon ↑ → reddetme ↑ ✓ |
| Karşılaştırma | 0,28 | [0,14; 0,49] | < 0,001 | depresyon ↑ → karşılaştırma ↑ ✓ |
| Aşırı koruma | 0,08 | — | 0,22 | anlamsız ❌ |

**Uyum indeksleri** (Hu–Bentler 1999 eşikleri) [:805, :810]:

| İndeks | Değer | Eşik | Karne |
|---|---|---|---|
| RMSEA | 0,027 | ≤ 0,06 | mükemmel *görünüyor* ⚠️ |
| SRMR | 0,127 | ≤ 0,08 | eşiğin üstünde ❌ |
| CFI / TLI | 0,887 / 0,890 | ≥ 0,90 | altında ⚠️ |

n = 237 (kontrol 121, DM 116).

**Yanlış okumayı önceden düzeltelim — iki kritik ders:**
- *Tek parlak indekse kanma.* RMSEA yüksek serbestlik derecesinde yanıltıcı düşer; SRMR ve
  CFI/TLI daha ihtiyatlı hikâyeyi anlatır. Model uyumu **karışık ve sınırlıdır** — tezin kendi
  ifadesi [:810].
- *İyi/anlamlı yol ≠ nedensellik.* Kesitsel tasarım gereği yollar "yordar/açıklar" değil
  **"birlikte değişir" (eş-değişim)** diliyle okunur [:795-799].

## Bir cümleyle

> Tablo 4.13, annedeki depresyon ile azalan sıcaklık (β = −0,28) ve artan reddetme/
> karşılaştırma (β = 0,33 / 0,28) arasında anlamlı **birlikte-değişim** yolları gösterir; ancak
> modelin uyumu karışıktır (RMSEA 0,027 iyi görünse de SRMR 0,127 ve CFI/TLI 0,887/0,890
> eşiklerin altında), bu yüzden bulgular nedensellik değil eş-değişim düzeyinde okunur.

*Komşu öğe:* çok-grup değişmezlik `@tbl-apa-h4-invariance` (Tablo 4.14) aynı biçimde açılabilir.

---

# Tablo 4.14'ü Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.14 = H4 çok-grup (DM vs Kontrol) ölçüm değişmezliği**
Kanonik etiket: `@tbl-apa-h4-invariance` · Kaynak: chapters/04_bulgular.qmd:819 (render) +
:791-797 (anlatı) · Aile: değişmezlik/uyum sonuç tablosu.

## Bu tablo hangi soruna çözüm?

H4 modelini (Tablo 4.13) DM ve kontrol gruplarında karşılaştırmak için önce **ölçüm cetvelinin
iki grupta aynı cetvel** olduğundan emin olmak gerekir. Aynı maddeye iki grup sistematik farklı
yanıt veriyorsa karşılaştırma "elmayla armut" olur. Tablo 4.14 bu sınavın karnesidir.

Okuma hamlesi: **iki ayrı soruyu iki ayrı sütun grubundan yanıtla** — "değişmezlik sağlandı
mı?" → **fark (Δ) sütunları**; "model uyumu iyi mi?" → her satırın **mutlak** uyum sütunları.

## Tablo ne söylüyor? — büyüklük okuryazarlığı

**Soru 1 — Değişmezlik (Δ sütunları; kural: ΔCFI ≤ −0,010 / ΔRMSEA ≥ 0,015 = ihlal — Cheung-
Rensvold 2002):**

| Geçiş | ΔCFI | ΔRMSEA | Karar |
|---|---|---|---|
| configural → metrik | −0,009 | \|Δ\| < 0,003 | eşik içinde ✓ |
| metrik → scalar | +0,005 | \|Δ\| < 0,003 | eşik içinde ✓ |

**Soru 2 — Mutlak uyum (Hu-Bentler):** CFI ≈ 0,82, SRMR ≈ 0,14 — üç düzeyde de **sınırlı**
[chapters/04_bulgular.qmd:791-797].

**Yanlış okumayı önceden düzeltelim — en kritik ders:** *değişmezlik sağlandı ≠ model iyi.*
Δ sütunları "cetvel iki grupta benzer" der; mutlak sütunlar "ama cetvel zaten pek iyi değil"
der. Bunlar iki ayrı yargıdır; tablo yalnız birincisini (değişmezlik kabul edilebilir) ihtiyatla
destekler. Ayrıca scalar düzeyi bazı boş kategoriler birleştirilerek çözüldüğünden temkinli
okunur.

## Bir cümleyle

> Tablo 4.14, DM ve kontrol ölçüm cetvelinin kademe kademe eşitlendiğinde kayda değer biçimde
> bozulmadığını (ΔCFI/ΔRMSEA eşik içinde → değişmezlik kabul edilebilir) gösterir; ama aynı
> satırların mutlak uyumu sınırlıdır (CFI ≈ 0,82; SRMR ≈ 0,14) — "cetvel benzer" ile "cetvel
> iyi" iki ayrı yargıdır.

*Komşu öğe:* H4 SEM `@tbl-apa-h4-sem` (Tablo 4.13) aynı biçimde açılabilir.

---

# Tablo 4.15'i Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.15 = H5 diadik tutarlılık stratejileri (beş paralel strateji)**
Kanonik etiket: `@tbl-apa-h5-concordance` · Kaynak: chapters/04_bulgular.qmd:896 (render) +
:856-925 (anlatı) · Aile: çok-stratejili sonuç tablosu.

## Bu tablo hangi soruna çözüm?

H5, anne ile çocuğun **aynı** ebeveynlik ilişkisini benzer mi algıladığını sorar. Tek bir uyum
ölçütü kırılgan olacağından, tez beş paralel strateji kullanır ve "güçlü bulgu" için önceden
**en az üçünün aynı yönde uyuşmasını** şart koşar. Tablo 4.15 bu beş stratejiyi gruplu özetler.

Okuma hamlesi: **strateji strateji oku; her biri uyumun farklı bir yüzünü ölçer; yönler
(DM > Kontrol mü, tersi mi) uyuşuyor mu?**

## Tablo ne söylüyor? — Dürüst bilanço

- **Strateji 1 (ICC + Bland-Altman):** mutlak uyum **düşük** (Cicchetti "fakir-zayıf");
  anne↔indeks ICC kontrol 0,03–0,20 / DM −0,01–0,08; alt ölçek bazında **dörtte dördü
  kontrol > DM** (sıcaklık 0,145/0,027; aşırı koruma 0,204/0,009; reddetme 0,029/−0,006;
  karşılaştırma 0,103/0,084) [chapters/04_bulgular.qmd:872-883].
- **Strateji 2 (RSA):** yalnız sıcaklık+reddetme; a4 reddetme havuz −13,96 (p = 0,012);
  gruba ayrılmış yön oyu üretmez [:876-887].
- **Strateji 3 (ortak yazgı):** reddetme yakınsamadı; sıcaklık +0,03 (p = 0,486), aşırı koruma
  +0,18 (p = 0,043), karşılaştırma +0,10 (p = 0,262) [:888-892].
- **Strateji 4 (latent düad CFA):** reddetme latent r havuz 0,19 / kontrol 0,17 / DM 0,29;
  ama DM modeli **zayıf uyumlu** (RMSEA 0,120; SRMR 0,254) → temkinli [:893-897].
- **Strateji 5 (Kenny k):** güven aralıkları sıfırı kapsayacak kadar geniş → güvenilir sonuç
  yok [:898-905].

**Dürüstlük kapısı + yanlış okuma düzeltmesi:** önceden konan **≥3 strateji aynı yön** şartı
**karşılanmamıştır**: baskın manifest kanıt (Strateji 1) dört boyutta kontrol > DM (0/4
DM > kontrol); tek ters sinyal Strateji 4'te (yalnız reddetme, zayıf uyum). Yani "en güçlü,
dört boyutlu kanıt düşük uyum gösterir" temel sonuçtur; *korelasyon ≠ uyum* ve *negatif ICC
hata değildir*.

## Bir cümleyle

> Tablo 4.15, beş stratejinin en güçlüsü ve dört boyutu kapsayanı (ICC/Bland-Altman) anne–çocuk
> uyumunun düşük ve dört boyutta da kontrol > DM olduğunu gösterir; önceden konan üç-strateji
> triangülasyon şartı karşılanmadığından yönlü bir "güçlü bulgu" ilan edilmez.

*Komşu öğeler:* Bland-Altman `@fig-h5-bland-altman` (Şekil 4.10) ve RSA `@fig-h5-rsa-surface`
(Şekil 4.11) aynı biçimde açılabilir.

---

# Tablo 4.16'yı Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.16 = [KEŞİFSEL] Aracılık ve koşullu süreç sonuçları**
Kanonik etiket: `@tbl-apa-mediation` · Kaynak: chapters/04_bulgular.qmd:933 (render) +
:939-957 (anlatı) · Aile: aracılık sonuç tablosu.

## Bu tablo hangi soruna çözüm?

"Annedeki depresyon, çocuğun algıladığı reddetmeyi **annenin reddetmesi üzerinden** mi
etkiliyor?" sorusu bir **aracılık** sorusudur: Beck → EMBU-P reddetme (a-yolu) → EMBU-C
reddetme (b-yolu). Tablo 4.16, bu zinciri ve grup moderasyonunu test eder.

Okuma hamlesi: **a-yolu × b-yolu = dolaylı etki; dolaylı etkinin GA'sı sıfırı içeriyor mu?**
İçeriyorsa aracılık **yok**.

## Tablo ne söylüyor? — Kanıt

- **Tek-aracı modeli (BCa bootstrap, n = 1000):** a-yolu (Beck → anne reddetmesi) anlamlı;
  b-yolu (anne reddetmesi → çocuk reddetme algısı) **anlamsız**; dolaylı etki GA'sı **sıfırı
  içerir** → aracılık yok [chapters/04_bulgular.qmd:944-949].
- **Çok düzeyli model:** a-yolu anlamlı, dolaylı etki anlamsız.
- **Koşullu süreç (Hayes Model 14):** grup moderasyonu (a3) ve aracılı moderasyon indeksi (IMM)
  **anlamsız** [:951-955].
- Imai-Keele-Tingley duyarlılığında kritik ρ < 0,05; bu nedenle dolaylı etki yerine **doğrudan
  etki `c'`** değerlendirilmiş ve reddetme yolunda **üç modelin üçünde de (3/3) pozitif,
  anlamlı** doğrudan etki bulunmuştur [:955-957]. (Kesin a/b/dolaylı katsayıları tablodadır;
  gövdede sayı olarak geçmediğinden burada uydurulmaz.)

**Yanlış okumayı önceden düzeltelim:** a-yolu anlamlı olması **aracılık kanıtı değildir** —
b-yolu anlamsız ve dolaylı etki sıfırı içerdiğinden **aracılık gösterilememiştir**. Bulgu
"depresyon çocuk algısını *doğrudan* birlikte-değişimle" yansıtır, anne reddetmesi *üzerinden*
değil. **[KEŞİFSEL].**

## Bir cümleyle

> Tablo 4.16, Beck → anne reddetmesi → çocuk reddetme algısı aracılık zincirinde dolaylı
> etkinin sıfırı içerdiğini (aracılık yok) ama doğrudan etkinin (c') reddetme yolunda üç
> modelde de anlamlı kaldığını gösterir; bu keşifsel bulgu aracılık değil doğrudan
> birlikte-değişim olarak okunur.

*Komşu öğe:* H4 SEM `@tbl-apa-h4-sem` (Tablo 4.13) aynı biçimde açılabilir.

---

# Tablo 4.17'yi Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.17 = [KEŞİFSEL] Latent profil, latent sınıf ve Bifaktör S-1 model seçim tanıları**
Kanonik etiket: `@tbl-apa-lpa-bifactor` · Kaynak: chapters/04_bulgular.qmd:952 (render) +
:968-982 (anlatı) · Aile: model-seçim tanı tablosu.

## Bu tablo hangi soruna çözüm?

Aileleri ruh sağlığı ve ebeveynlik göstergelerine göre **kaç doğal gruba (profile/sınıfa)**
ayırabiliriz? Tablo 4.17, profil/sınıf sayısına göre model-seçim tanılarını (BIC, entropi,
BLRT) verir — "kaç profil?" kararının gerekçesidir.

Okuma hamlesi: **BIC minimumu nerede — ama parsimoni kuralı (ΔBIC ≤ 2) ve yorumlanabilirlik ne
diyor?** Sayısal minimum tek başına seçim değildir.

## Tablo ne söylüyor? — büyüklük okuryazarlığı

- LPA'da **BIC sayısal minimumu 4-profildedir**; yine de **3-profil** benimsenmiştir — ΔBIC ≈ 2
  parsimoni eşiği (Raftery 1995) ve yorumlanabilirlik gereği [caption :985].
- poLCA (kategorik) 2-sınıf çözümü destekler: BIC = 2641,0; sınıf oranları %63,4 / %36,6;
  **entropi = 0,60**; modal sınıf regresyonunda DM üyeliği anlamlı değiştirmez (OR = 0,99;
  %95 GA [0,57; 1,71]; p = 0,962) [chapters/04_bulgular.qmd:977-980].
- Bifaktör S-1 modeli sınır-altı uyum → yalnız keşifsel [:980-981].

**Yanlış okumayı önceden düzeltelim:** *en düşük BIC otomatik kazanan değildir* — seçim kuralı
(ΔBIC ≤ 2) tablo ve metinde aynı profil sayısını göstermelidir (burada bilinçle 4 değil 3).
Entropi 0,60, iyi ayrım için yol gösterici 0,80 eşiğinin **altındadır** → profiller keskin
ayrışmaz. **[KEŞİFSEL].**

## Bir cümleyle

> Tablo 4.17, LPA'da BIC minimumu 4-profilde olsa da parsimoni ve yorumlanabilirlik gereği
> keşifsel olarak 3-profilin benimsendiğini; poLCA 2-sınıf çözümünde (entropi 0,60, sınırlı
> ayrım) DM üyeliğinin sınıfı anlamlı değiştirmediğini (OR = 0,99) gösterir.

*Komşu öğe:* LPA model-seçim şekli `@fig-lpa-fit-indices` (Şekil 4.12) aynı biçimde açılabilir.

---

# Tablo 4.18'i Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.18 = [KEŞİFSEL] Ağ merkeziyet ve Ağ Karşılaştırma Testi (NCT)**
Kanonik etiket: `@tbl-apa-network` · Kaynak: chapters/04_bulgular.qmd:970 (render) +
:989-998 (anlatı) · Aile: ağ merkeziyet + karşılaştırma tablosu.

## Bu tablo hangi soruna çözüm?

Ebeveynlik, kardeş ilişkisi ve anne depresyonu göstergeleri arasında hangi ikili **doğrudan**
(diğer her şey sabitken) bağlı, hangi düğüm merkezî, ve DM ile kontrol ağları birbirinden
farklı mı? Tablo 4.18, ağ merkeziyet ölçütlerini ve Ağ Karşılaştırma Testi (NCT) sonuçlarını
verir.

Okuma hamlesi: **hangi düğüm en yüksek merkeziyette; DM ↔ kontrol ağ farkı anlamlı mı (NCT p)?**

## Tablo ne söylüyor? — Kanıt

- Dokuz değişken (dört EMBU-P + dört SRQ + Beck total) üzerinde EBIC-LASSO Gauss grafik modeli
  (γ = 0,5), havuzlanmış n = 238 [chapters/04_bulgular.qmd:990-991].
- En güçlü kenarlar, düğüm merkeziyeti ve case-dropping bootstrap kararlılık katsayısı tabloda
  raporlanır (gövdede inline-R ile üretildiğinden buraya sayı olarak uydurulmaz).
- **NCT:** ağ invaryans ve global strength p değerleri **DM ve kontrol ağlarının anlamlı
  düzeyde ayrışmadığını** gösterir [:994-996].

**Yanlış okumayı önceden düzeltelim:**
- *Kenar nedensel ok değildir:* "koşullu bağımlılık nedensellik olarak yorumlanmamıştır" [:996].
  GGM yönsüz ve **[KEŞİFSEL]**dir.
- *Anlamsız ≠ özdeş:* NCT'de fark bulunamaması "iki ağ aynıdır" demek değil, mevcut örneklemde
  farkın gösterilemediğidir.

## Bir cümleyle

> Tablo 4.18, dokuz göstergenin doğrudan (kısmi korelasyon) bağlantı iskeletini ve merkeziyetini
> keşifsel olarak özetler ve DM ile kontrol ağlarının anlamlı düzeyde ayrışmadığını (NCT)
> gösterir; kenarlar nedensel ok değildir ve "ayrışma yok" ağların özdeşliğinin kanıtı değildir.

*Komşu öğeler:* ağ grafiği `@fig-network-graph` (Şekil 4.13) ve NCT `@fig-network-nct`
(Şekil 4.14) aynı biçimde açılabilir.

---

# Tablo 4.19'u Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.19 = [KEŞİFSEL] Eşzamanlı klinik sınıflandırma (tarama) modeli performansı**
Kanonik etiket: `@tbl-apa-clinical` · Kaynak: chapters/04_bulgular.qmd:1001 (render) +
:1010-1024, :1133 (anlatı) · Aile: sınıflandırma performans tablosu.

## Bu tablo hangi soruna çözüm?

Elimizdeki bilgilerle (demografi/SES; ve ek olarak ebeveynlik tutumları), yüksek depresif
belirti taşıyan anneleri **ayırt edebilir miyiz**? Tablo 4.19, bir tarama modelinin ayrım
gücünü (AUC) ve işletme noktası performansını (duyarlılık, özgüllük, PPV, NPV) verir.

Okuma hamlesi: **AUC ne düzeyde (0,5 = şans); Youden işletme noktasında duyarlılık/özgüllük
dengesi ne?**

## Tablo ne söylüyor? — büyüklük okuryazarlığı

- **Temel model** = DM grup + anne yaşı + latent SES + aile çocuk sayısı; **genişletilmiş** =
  temel + dört EMBU-P; iç-validasyonlu **optimizm-düzeltilmiş bootstrap** (B = 1000)
  [chapters/04_bulgular.qmd:1011-1013].
- Genişletilmiş modelin **AUC = 0,70** (Hosmer-Lemeshow geleneğinde 0,70–0,80 = kabul
  edilebilir) [:1133].
- Youden işletme noktası: eşik 0,22; **duyarlılık 0,75; özgüllük 0,60; PPV 0,41; NPV 0,87**
  [:1015-1016].

**Yanlış okumayı önceden düzeltelim — üç uyarı:**
- *Eşzamanlı sınıflandırma ≠ ileriye dönük yordama:* "şu an kimde yüksek belirti eşlik ediyor"u
  sınıflar, "gelecekte kim geliştirir"i değil.
- *Ortak-yöntem varyansı:* yordayıcılar (EMBU-P) ve sonuç (Beck) aynı anne/oturumda öz-bildirim
  olduğundan ayrım gücünün bir kısmı bağımsız yordama değil ortak-yöntem olabilir.
- **[KEŞİFSEL]**, dış-doğrulanmamış.

## Bir cümleyle

> Tablo 4.19, ebeveynlik-eklenen modelin yüksek depresif belirtiyi eşzamanlı olarak orta
> düzeyde ayırt ettiğini (AUC = 0,70; Youden'da duyarlılık 0,75 / özgüllük 0,60) gösterir; ama
> bu kesitsel, ortak-yöntem varyansına açık ve dış-doğrulanmamış keşifsel bir sonuçtur.

*Komşu öğeler:* ROC `@fig-clinical-roc` (Şekil 4.15), DCA `@fig-clinical-dca` (Şekil 4.16).

---

# Tablo 4.20'yi Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.20 = [KEŞİFSEL] DM klinik zamanlama alt-analizleri**
Kanonik etiket: `@tbl-apa-dm-clinical` · Aile: klinik zamanlama sonuç tablosu.

## Bu tablo hangi soruna çözüm?

Yalnız DM grubunda hastalık süresi ve tanı yaşı gibi klinik zamanlama göstergeleri ebeveynlik tutumuyla ilişkili mi? Tablo 4.20 bu bağlamsal alt-analizleri toplar; doğrulayıcı hipotez kararlarını değiştirmez.

## Tablo ne söylüyor? — Dürüst bilanço

- DM süresi: kübik spline vs doğrusal karşılaştırmalar doğrulayıcı bir ek sinyal üretmez.
- Tanı yaşı (üç strata): F testi hiçbir sonuçta anlamlı değildir; etki büyüklükleri küçük banttadır.

**Yanlış okumayı önceden düzeltelim:** Bu tablo klinik zamanlama değişkenlerini hipotez-üretici bağlam olarak sunar; kesitsel tasarım nedeniyle nedensel ya da klinik karar verdirici yorum taşımaz.

## Bir cümleyle

> Tablo 4.20, DM süresi ve tanı yaşının ebeveynlik tutumları için doğrulayıcı bir ek sinyal üretmediğini, bu değişkenlerin yalnız bağlamsal/keşifsel düzeyde okunması gerektiğini gösterir.

*Komşu öğe:* eğilim/örneklem `@tbl-apa-sample-characteristics` (Tablo 4.1) aynı biçimde açılabilir.


---

# Tablo 4.21'i Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.21 = H1 dönem duyarlılığı (2023 ortak-takvim alt örneklemi)**
Kanonik etiket: `@tbl-apa-h1-period2023` · Kaynak: chapters/04_bulgular.qmd:1190 (render) +
:1181-1186 (anlatı) · Aile: duyarlılık sonuç tablosu.

## Bu tablo hangi soruna çözüm?

DM ve kontrol aileleri farklı yıllarda toplandıysa, H1 farkı "diyabet"ten değil "dönem/kohort"
farkından geliyor olabilir. En temiz sınav: **iki grubun en geniş ortak takvim desteğine sahip
olduğu 2023 alt örnekleminde** H1'i yeniden çalıştırmak. Tablo 4.21 bunu belgeler — H1'in en
sıkı dürüstlük sınavlarından biri.

Okuma hamlesi: **tam örneklemde doğrulanan etkiler, dengeli dönem alt örnekleminde hayatta
kalıyor mu?**

## Tablo ne söylüyor? — Dürüst bilanço

Birincil H1 estimandı yalnız 2023 alt örnekleminde (n = 40 kontrol, 108 DM indeks aile)
[chapters/04_bulgular.qmd:1184]:

| Alt ölçek | b (2023) | %95 GA | q | Tam örneklem b |
|---|---|---|---|---|
| Reddetme | 0,02 | [−0,09; 0,13] | 0,69 | 0,14 |
| Aşırı koruma | 0,11 | [−0,06; 0,27] | 0,61 | 0,19 |
| Sıcaklık | −0,08 | — | 0,61 | 0,14 |
| Karşılaştırma | −0,06 | — | 0,69 | 0,13 |

**Dört boyutun hiçbirinde grup farkı için kanıt kalmaz.** Cohen d de aynı yönü verir: reddetme
d 0,38 → −0,00 (p = 0,99); aşırı koruma d 0,37 → 0,26 (p = 0,19) [:1184].

**Dürüstlük kapısı — gizlenmez:** tam örneklemde doğrulanan iki boyut (reddetme, aşırı koruma),
dönem-dengeli 2023 alt örnekleminde **sönümlenir**. Bu, H1 sinyalinin bir kısmının
dönem/kohort yapısıyla iç içe olabileceğine dair önemli bir sınırlılıktır ve Sınırlılıklar'da
taşınır. (Alt örneklem küçüldüğü için güç kaybı da katkıda bulunur — iki açıklama birbirini
dışlamaz.)

## Bir cümleyle

> Tablo 4.21, tam örneklemde doğrulanan H1 reddetme ve aşırı koruma etkilerinin, iki grubun en
> dengeli ortak-takvim dilimi olan 2023 alt örnekleminde (n = 148) anlamlılığını yitirdiğini
> dürüstçe belgeler — sinyalin bir kısmının dönem/kohort yapısıyla iç içe olabileceğine işaret
> eden bir duyarlılık bulgusu.

*Komşu öğeler:* H1 ana etki `@tbl-apa-h1-group` (Tablo 4.6) ve duyarlılık `@tbl-apa-sensitivity`
(Tablo 4.23).

---

# Tablo 4.22'yi Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.22 = Robustluk: çoklu evren ve TOST**
Kanonik etiket: `@tbl-apa-robustness` · Kaynak: chapters/04_bulgular.qmd:1311 (render) +
:1298-1306 (anlatı) · Aile: robustluk özet tablosu.

## Bu tablo hangi soruna çözüm?

Bir bulgu tek bir analiz seçimine bağlıysa kırılgandır. Tablo 4.22 iki robustluk katmanını
toplar: **çoklu-evren** (bulgu seçimler boyunca hayatta kalıyor mu?) ve **TOST eşdeğerlik**
(null bulgular gerçekten "fark yok"a mı işaret ediyor?).

Okuma hamlesi: **çoklu-evrende anlamlı spesifikasyon oranı ne; TOST kararı hangi sınıra bağlı?**

## Tablo ne söylüyor? — Kanıt

- **Çoklu-evren (H1 çocuk algısı):** reddetme 25 spesifikasyonda **%100 p < 0,05** (medyan
  β = 0,12) → sağlam; aşırı koruma ve sıcaklık %100; **karşılaştırma yalnız %3** → kırılgan
  [chapters/04_bulgular.qmd:1298-1301]. (H3 tarafında permütasyon testi n = 5000 anlamlılık
  üretmez.)
- **TOST (H3, ±0,30 SMD):** aşırı koruma ve karşılaştırma "Eşdeğer", sıcaklık ve reddetme
  "Belirsiz"; daha katı ±0,20/±0,25 bantlarında hiçbir boyutta biçimsel eşdeğerlik kalmaz
  [:1304-1306].

**Yanlış okumayı önceden düzeltelim:** çoklu-evren bir **dağılımdır**, tek test değildir;
renkli nominal anlamlılık çokluk-düzeltilmiş değildir (dürüst global yargı permütasyon). TOST
"Eşdeğer" kararı **SESOI'ye koşulludur**, mutlak değildir.

## Bir cümleyle

> Tablo 4.22, H1 reddetme bulgusunun analitik seçimlere karşı sağlam (25 spesifikasyonun %100'ü
> anlamlı, medyan β = 0,12) ama karşılaştırmanın kırılgan (%3) olduğunu; H3 TOST eşdeğerliğinin
> ise yalnız ±0,30 sınırında geçerli olduğunu özetler.

*Komşu öğeler:* spec eğrisi `@fig-specification-curve` (Şekil 4.26) ve duyarlılık
`@tbl-apa-sensitivity` (Tablo 4.23).

---

# Tablo 4.23'ü Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.23 = Ölçülmemiş karıştırıcı ve falsifikasyon duyarlılığı**
Kanonik etiket: `@tbl-apa-sensitivity` · Kaynak: chapters/04_bulgular.qmd:1317 (render) +
:1307-1330 (anlatı) · Aile: duyarlılık/falsifikasyon özet tablosu.

## Bu tablo hangi soruna çözüm?

Gözlemsel tasarımda iki tehdit vardır: (1) **ölçülmemiş** bir karıştırıcı bulguyu değiştirebilir
mi? (2) Yöntem, ilişki **beklenmeyen** yerde bile sahte sinyal üretiyor mu? Tablo 4.23 bu iki
sınamayı (sağlamlık değeri/E-değeri + negatif kontrol/falsifikasyon) toplar.

Okuma hamlesi: **gizli karıştırıcının bulguyu silmesi için gereken güç yüksek mi (RV/E); sahte
yordayıcılar temiz kalıyor mu?**

## Tablo ne söylüyor? — Dürüst bilanço

- **Ölçülmemiş karıştırıcı (H3):** RV_q = 0,04–0,08; E-değeri 1,36–1,59 → **zayıf-orta**
  dayanıklılık [chapters/04_bulgular.qmd:1308-1311].
- **Negatif kontrol:** rastgele sayı yordayıcısı beklendiği gibi anlamsız; ama **aile numarası**
  yordayıcısı EMBU-P sıcaklıkta anlamlı çıkmış (β = 0,098; p = 0,003) ve Bonferroni (0,006)
  sonrası bile anlamlı — bu tam rastgele değil, olası bir **dönem/kohort vekili**; artık ilişki
  Sınırlılıklar'da uyarı olarak taşınır [:1313-1322].
- **Eksik veri robustluğu:** tamamlanmış olgu (N = 219), FIML (N = 241), MI (m = 50) arası en
  büyük katsayı farkı **0,01 SD**; MNAR delta reddetme −0,04 (p ≈ 0,31) [:1324-1328].
- **SES operasyonelleştirme:** dört SES tanımıyla H3 reddetme −0,04/−0,03/−0,04/−0,03; yayılım
  0,01 SD [:1329-1330].

**Yanlış okumayı önceden düzeltelim:** düşük RV/E "sonuç yanlış" değil "gizli karıştırıcı görece
kolay değiştirebilir → temkinli oku" demektir. Aile numarası sinyali dürüstçe bir dönem/kohort
uyarısı olarak raporlanır (4.21 dönem sönümlenmesiyle tutarlı). Eksik veri ve SES tanımı
robustluğu ise yüksektir (yayılım ≈ 0,01 SD).

## Bir cümleyle

> Tablo 4.23, bulguların ölçülmemiş karıştırıcıya karşı yalnız zayıf-orta dayanıklı olduğunu
> (RV_q = 0,04–0,08), bir negatif kontrolün (aile numarası β = 0,098) olası dönem/kohort
> vekili olarak dürüstçe işaretlendiğini, buna karşılık eksik-veri ve SES-tanımı seçimlerine
> karşı sonuçların çok kararlı (yayılım ≈ 0,01 SD) olduğunu özetler.

*Komşu öğeler:* sensemakr konturu `@fig-sensemakr-contour` (Şekil 4.27) ve dönem duyarlılığı
`@tbl-apa-h1-period2023` (Tablo 4.21).

---

# Tablo 4.24'ü Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.24 = Bayesçi çift raporlama (global) + MCMC tanıları**
Kanonik etiket: `@tbl-apa-bayesian-global` · Kaynak: chapters/04_bulgular.qmd:1342 (render) +
:1348-1362 (anlatı) · Aile: Bayesçi özet + tanı tablosu.

## Bu tablo hangi soruna çözüm?

Bölüm boyunca dağınık verilen Bayesçi sonuçları (H1 + H3) tek yerde toplar ve **modellere ne
kadar güvenilebileceğini** (MCMC yakınsama tanıları) belgeler. İki iş yapar: kanıtı özetler ve
"bu Bayesçi sayılar sayısal olarak kararlı mı?" sorusunu yanıtlar.

Okuma hamlesi: **BF₁₀'ı Jeffreys ölçeğine oturt; sonra tanı sütunlarına bak — R̂, ESS,
ıraksayan geçiş sağlıklı mı?**

## Tablo ne söylüyor? — Kanıt

- H1 reddetme: BF₁₀ = 10,55 (güçlü H1; b = 0,16; pd = 0,999; ROPE içi %12,8); H1 sıcaklık:
  BF₁₀ = 0,29 (H0). H3 dört boyutta BF₁₀ 0,17–0,23; reddetmede ROPE %93 ("orta-güçlü H0")
  [chapters/04_bulgular.qmd:1348-1353].
- **MCMC tanıları:** dört zincir × 4000 (1500 ısınma); tüm modellerde **R̂ ≤ 1,003**;
  ıraksayan geçiş yok; Pareto-k < 0,7; ESS > 1000 [:1355-1361].

**Yanlış okumayı önceden düzeltelim:** **ESS > 1000 bir örneklem büyüklüğü değildir** — MCMC
kestiriminin Monte Carlo kararlılığını gösterir (tez bunu açıkça belirtir [:1358-1361]).
Sağlıklı R̂/ESS/ıraksama-yokluğu "model doğru" demez, yalnız "Bayesçi sayılar güvenilir biçimde
kestirildi" der.

## Bir cümleyle

> Tablo 4.24, H1 reddetme (BF₁₀ = 10,55, güçlü) ve H1 sıcaklık/H3 (BF₁₀ < 1, H0 lehine) Bayesçi
> kanıtını tek yerde özetler ve tüm modellerin sağlıklı yakınsadığını (R̂ ≤ 1,003, ıraksama yok,
> ESS > 1000) belgeler; ESS bir örneklem büyüklüğü değil MCMC kararlılık göstergesidir.

*Komşu öğe:* H1 Bayesçi `@tbl-apa-h1-bayesian` (Tablo 4.8) ve önsel merkez duyarlılığı
`@tbl-apa-prior-center` (Tablo 5.7).

---

# Tablo 4.25'i Anlamak — Basitçe, Ama Eksiksiz

**Tablo 4.25 = Genel bulgu sentezi**
Kanonik etiket: `@tbl-apa-result-synthesis` · Kaynak: chapters/04_bulgular.qmd:1552 (render) +
:1512, :1576 (anlatı) · Aile: kapstone/bütünleşik sentez tablosu.

## Bu tablo hangi soruna çözüm?

Onlarca analizin sonunda okur "peki sonuçta ne bulundu?" diye sorar. Tablo 4.25, birincil ve
genişletilmiş bulguları — ve karma tezin niteliksel kolunun deneyimsel bağlamını — tek bir
bütünleşik özette toplar. Belgenin doruk tablosudur.

Okuma hamlesi: **hipotez satırlarını yatay oku; nicel bulgu + niteliksel bağlam + yakınsama
tipi + çekince sütunlarını birlikte değerlendir.**

## Tablo ne söylüyor?

Her hipotez için nicel karar, (varsa) niteliksel deneyimsel bağlam, yakınsama tipi (ör.
"açıklayıcı genişleme") ve nedensellik/kapsam çekincesi bir arada verilir. Örneğin H1: DM
çocuklarının reddetme/aşırı koruma algısı iki çerçevede tutarlı (reddetme b = 0,14 [0,07; 0,22],
q = 0,001, BF₁₀ = 10,55; g ≈ 0,38); niteliksel kolda "normalleşme dili yükün yokluğu değildir"
teması açıklayıcı genişleme sağlar; çekince: nedensellik yok, nitel bağlam mekanizma değildir
[chapters/04_bulgular.qmd:1512].

**Yanlış okumayı önceden düzeltelim:** yakınsama (nicel ↔ nitel aynı yönü göstermesi)
**nedensellik değildir**; niteliksel kol deneyimsel *bağlam* verir, nicel örüntünün mekanizması
değil. Sentez tablosu bulguları birleştirir, iddiaları güçlendirmez.

## Bir cümleyle

> Tablo 4.25, beş hipotezin nicel kararını, niteliksel deneyimsel bağlamını, yakınsama tipini
> ve çekincelerini tek bütünleşik özette toplar; yakınsama nedensellik değil, karma-yöntem
> bağlam zenginleştirmesidir.

*Komşu öğe:* tüm 4.x sonuç tabloları bu sentezin bileşenleridir.

---

# Tablo 5.1'i Anlamak — Basitçe, Ama Eksiksiz

**Tablo 5.1 = Veri toplama yılı × grup dağılımı**
Kanonik etiket: `@tbl-yil-grup` · Kaynak: chapters/05_tartisma_ve_sonuc.qmd:960 (render) +
:950-965 (anlatı) · Aile: çapraz-tablo (seçilim yapısı).

## Bu tablo hangi soruna çözüm?

Tartışma'da kritik bir sınırlılık ele alınır: DM ve kontrol aileleri **aynı yıllarda mı**
toplandı? Değilse, grup farkı "diyabet"ten değil "dönem"den geliyor olabilir. Tablo 5.1, yıl ×
grup çapraz-tablosuyla bu seçilim yapısını görünür kılar — Tablo 4.21 dönem-sönümlenmesinin
nedenini açıklar.

Okuma hamlesi: **her yılda iki grubun sayısına bak; nerede ortak temsil (örtüşme) geniş?**

## Tablo ne söylüyor? — Kanıt

| Yıl | DM | Kontrol | Toplam |
|---|---|---|---|
| 2023 | 108 | 40 | 148 |
| 2024 | 6 | 36 | 42 |
| 2025 | 6 | 45 | 51 |

Değerler [chapters/05_tartisma_ve_sonuc.qmd:955-960]. DM aileleri büyük ölçüde **2023'te**
toplanmış; kontroller 2024–2025'e yayılmış. 2023, iki grubun en geniş ortak temsile sahip
olduğu dönemdir.

**Yanlış okumayı önceden düzeltelim:** bu bir karıştırıcı değil, bir **seçilim yanlılığı**
mekanizmasıdır — ortak temsil dönemi dışındaki katılımcılar üzerinde koşullanma, ortak-etki
üzerinden yanlılık üretebilir (Hernán 2004). Nitekim bir grup farkının seçilim yapısı
dengelendiğinde (2023, Tablo 4.21) büyüklüğünü yitirmesi bu yapıyla tutarlıdır.

## Bir cümleyle

> Tablo 5.1, DM ailelerinin çoğunlukla 2023'te (108/40), kontrollerin ise 2024–2025'e yayılarak
> toplandığını gösterir; bu dönemsel seçilim yapısı, H1 etkilerinin 2023 dengeli alt örnekleminde
> neden sönümlendiğinin (Tablo 4.21) yapısal açıklamasıdır.

*Komşu öğe:* H1 dönem duyarlılığı `@tbl-apa-h1-period2023` (Tablo 4.21) aynı biçimde açılabilir.

---

# Tablo 5.2–5.5'i Anlamak — Basitçe, Ama Eksiksiz

**Tablo 5.2–5.5 = Ölçüm değişmezliği eksen-bazlı uyum ölçütleri (WLSMV; dört eksen alt-tablosu)**
Kanonik etiket: `@tbl-apa-invariance` · Kaynak: chapters/07_ekler.qmd:14-20 (Ek 3) · Aile:
değişmezlik uyum tablosu (eksen başına alt-tablo).

## Bu tablo hangi soruna çözüm?

Bir ölçek, farklı gruplarda **aynı şeyi aynı biçimde** ölçmüyorsa gruplar arası karşılaştırma
yanıltıcı olur. Tablo 5.2–5.5, EMBU ölçeğinin dört eksende — tanı grubu, bilgi verici rolü,
yaş, cinsiyet — değişmezlik taramasının WLSMV uyum ölçütlerini eksen başına ayrı alt-tabloda
verir.

Okuma hamlesi: **her eksende yapılandırmasal → metrik → skalar geçişinde ΔCFI/ΔRMSEA eşik
içinde mi?**

## Tablo ne söylüyor? — büyüklük okuryazarlığı

- Dört eksen: tanı grubu (5.2), bilgi verici rolü (5.3), yaş (5.4), cinsiyet (5.5); her eksende
  yapılandırmasal/metrik/skalar düzeyler [chapters/07_ekler.qmd:16].
- Δ eşikleri (Cheung-Rensvold 2002; Chen 2007): **ΔCFI ≥ −0,010 ve ΔRMSEA ≤ 0,015** [:16].
- **Önemli sınır:** sıralı maddelerde bazı gruplarda boş yanıt kategorileri olduğunda tam-kategori
  model **yakınsamamış**; bu durumda değişmezlik yalnız ikiye indirgenmiş (1 vs. >1) duyarlılık
  çözümüyle değerlendirilebilmiştir [:16]. Yakınsamayan modeller tabloda "—" ile gösterilir.
  (Kesin uyum değerleri artefakt `psychval_measurement_invariance.csv`'dendir; burada
  uydurulmaz.)

**Yanlış okumayı önceden düzeltelim:** yakınsamama bir bulgu değil bir **kestirim sınırıdır**
(boş kategoriler); "—" satırı "değişmezlik yok" demek değildir. Ayrıca (Tablo 4.14'teki gibi)
Δ-temelli değişmezlik, mutlak uyumun iyi olduğu anlamına gelmez.

## Bir cümleyle

> Tablo 5.2–5.5, EMBU değişmezliğini dört eksende (tanı/rol/yaş/cinsiyet) yapılandırmasal-metrik-
> skalar düzeylerde ΔCFI ≥ −0,010 / ΔRMSEA ≤ 0,015 ölçütüyle tarar; bazı sıralı-madde modelleri
> boş kategoriler nedeniyle yakınsamadığından ikiye-indirgenmiş duyarlılıkla değerlendirilmiş ve
> "—" ile işaretlenmiştir.

*Komşu öğe:* H4 çok-grup değişmezlik `@tbl-apa-h4-invariance` (Tablo 4.14) aynı biçimde açılabilir.

---

# Tablo 5.6'yı Anlamak — Basitçe, Ama Eksiksiz

**Tablo 5.6 = H3 eşdeğerlik (TOST) kararının SESOI sınırına duyarlılığı**
Kanonik etiket: `@tbl-apa-tost-sensitivity` · Kaynak: chapters/07_ekler.qmd:78-84 (Ek 5) ·
Aile: eşdeğerlik duyarlılık tablosu.

## Bu tablo hangi soruna çözüm?

H3'te "fark yok" demek için eşdeğerlik testi (TOST) kullanıldı; ama bu testin kararı, "önemsiz
sayılan en küçük fark" (SESOI) sınırına bağlıdır. Tablo 5.6, H3 kararının **farklı SESOI
bantlarında** (±0,20 / ±0,25 / ±0,30 SMD) nasıl değiştiğini gösterir — "eşdeğer" iddiasının ne
kadar sağlam olduğunun sınavı.

Okuma hamlesi: **her alt ölçekte, sınır daraldıkça (±0,30 → ±0,20) "Eşdeğer" kararı hayatta
kalıyor mu?**

## Tablo ne söylüyor? — Kanıt

- Sütunlar: alt ölçek, SESOI, gözlenen d, TOST p, NHST p, karar (Eşdeğer/Belirsiz/…)
  [chapters/07_ekler.qmd:84-100].
- **±0,30 SMD:** aşırı koruma ve karşılaştırma "Eşdeğer"; sıcaklık ve reddetme "Belirsiz".
- **±0,20 / ±0,25 SMD:** hiçbir alt ölçekte biçimsel eşdeğerlik kalmaz (hepsi "Belirsiz")
  [chapters/04_bulgular.qmd:772-776]. (Kesin d/p değerleri artefakt `tost_sensitivity.csv`'dendir.)

**Yanlış okumayı önceden düzeltelim:** "Eşdeğer" kararı **mutlak değil, SESOI'ye koşulludur**;
yalnız en geniş (±0,30) sınırda ve yalnız iki boyutta geçerlidir. Bu yüzden H3 null'u için
"eşdeğerlik gösterildi" değil, "eşdeğerlik yalnız gevşek sınırda ve kısmen" denir.

## Bir cümleyle

> Tablo 5.6, H3 TOST eşdeğerlik kararının SESOI sınırına duyarlı olduğunu — yalnız ±0,30'da ve
> yalnız aşırı koruma/karşılaştırmada "Eşdeğer", daha katı ±0,20/±0,25'te hepsi "Belirsiz" —
> belgeleyerek "eşdeğerlik" iddiasının koşulluluğunu gösterir.

*Komşu öğe:* H3 duyarlılık `@tbl-apa-h3-sensitivity` (Tablo 4.12) aynı biçimde açılabilir.

---

# Tablo 5.7'yi Anlamak — Basitçe, Ama Eksiksiz

**Tablo 5.7 = Bayesçi grup etkisi: önsel merkezine duyarlılık**
Kanonik etiket: `@tbl-apa-prior-center` · Kaynak: chapters/07_ekler.qmd:110-118 (Ek 6) · Aile:
Bayesçi önsel-duyarlılık tablosu.

## Bu tablo hangi soruna çözüm?

Bayesçi sonuç, analizden **önce** seçilen önsele (prior) bağlıdır. Bir eleştirmen "sonucu önsel
belirledi" diyebilir. Tablo 5.7, kilit bulguların önselin **merkezine** duyarlılığını sınar:
aynı analiz üç farklı önsel merkeziyle (skeptik sıfır; literatür/mevcut yön; ters yön) yeniden
çalıştırılır — sonuç önsele değil veriye mi dayanıyor?

Okuma hamlesi: **BF₁₀'ın kanıt sınıfı (Güçlü H1 / Orta H0 …) üç merkezde de aynı kalıyor mu?**

## Tablo ne söylüyor? — Kanıt

- Sınanan bulgular: H1 çocuk reddetme (birincil) + önsel yönü tartışmalı H3 sıcaklık ve reddetme;
  üç merkez (skeptik 0; literatür yönü; ters yön); önsel SS tümünde 0,50
  [chapters/07_ekler.qmd:112-118].
- Sütunlar: BF₁₀, sonsal ortalama, yön olasılığı pd, kanıt sınıfı. (Kesin BF değerleri artefakt
  `bayes_prior_center_sensitivity.csv`'dendir; burada uydurulmaz.)

**Yanlış okumayı önceden düzeltelim — sayısal bütünlük:** Savage-Dickey BF önsel genişliğine ve
merkezine duyarlıdır; bu yüzden BF **sınıf etiketi** (ör. "güçlü H1") sayısal BF ile tutarlı
olmalı ve merkez seçimine karşı kararlı sunulmalıdır (AGENTS.md yön-mantığı kaidesi). Tablo tam
bu kararlılığı belgelemek için vardır — bulgunun önsele değil veriye dayandığını gösterir.

## Bir cümleyle

> Tablo 5.7, kilit Bayesçi bulguların (H1 çocuk reddetme; H3 sıcaklık/reddetme) önselin merkezine
> — skeptik, literatür yönü, ters yön — duyarlılığını sınayarak, BF kanıt sınıfının önsel seçimine
> değil veriye dayandığını belgeler.

*Komşu öğe:* Bayesçi global `@tbl-apa-bayesian-global` (Tablo 4.24) aynı biçimde açılabilir.

---

## Notlar

- Bu belge tezin **Tablolar Dizini'nin tamamını** kapsar: **2.1–2.4, 3.1–3.3, 4.1–4.25 ve
  5.1–5.7** (5.2–5.5 = tek değişmezlik tablosunun dört eksen alt-tablosu).
- Numaralandırma `outputs/quarto/thesis.pdf` TABLOLAR DİZİNİ'nden alınmıştır; içerik ve sayılar
  chapters/*.qmd kaynaklarından birebir teyit edilmiştir; ondalık-virgül korunmuştur.
- Tablo 2.1–2.4, 3.1–3.3 **kavramsal/referans/plan/yönetişim**; 4.x sonuç tablolarında **büyüklük
  okuryazarlığı** katmanı (SMD Austin; CFA/SEM Hu-Bentler; ΔCFI Cheung-Rensvold; BF Jeffreys/
  Lee-Wagenmakers; ICC Koo-Li/Cicchetti; LPA entropi/ΔBIC Raftery; AUC Hosmer; RV/E-değeri)
  kaynağıyla devrededir.
- Hücre-düzeyi değerleri gitignored `outputs/` artefaktlarında/inline-R'de olan tablolarda
  (ör. 4.4/4.5/4.16/4.18/4.24 ve 5.2–5.7) kaynak metinde görünmeyen değerler
  **uydurulmamıştır** (AGENTS.md); metindeki özet değerler kullanılıp gerisi ilgili tabloya
  yönlendirilmiştir.
- **Hipotez okuma anahtarları:** H1 (4.6/4.7/4.8, Bayesçi 4.24) sağlam = reddetme + aşırı koruma;
  **ama** 2023 dengeli alt örneklemde (4.21) sönümlenir + aile-numarası negatif kontrolü (4.23) +
  yıl×grup seçilim yapısı (5.1) dönem/kohort çekincesi verir. H2/H3 null ("anlamsız ≠ yok");
  bilgi-verici ayrışması çocuk↔anne; H3 eşdeğerliği SESOI'ye koşullu (4.12/5.6). H4 değişmezlik ≠
  iyi uyum (4.14/5.2–5.5); eş-değişim ≠ nedensellik. H5 triangülasyon karşılanmaz (4.15).
  [KEŞİFSEL] (4.16–4.20): aracılık yok; LPA 3-profil; ağlar ayrışmaz; klinik orta AUC + ortak-
  yöntem varyansı; DM alt-analizler güçsüz. Bayesçi kararlılık: önsel merkezine dirençli (5.7).
- Tablo–şekil çiftleri: 4.2↔Ş4.3; 4.3↔Ş4.6; 4.4↔Ş4.4; 4.6/4.8↔Ş4.7; 4.10↔Ş4.8; 4.11/4.12↔Ş4.9;
  4.13/4.14↔(H4); 4.15↔Ş4.10/4.11; 4.17↔Ş4.12; 4.18↔Ş4.13/4.14; 4.19↔Ş4.15/4.16/4.17;
  4.22↔Ş4.26; 4.23↔Ş4.27; 5.1↔Tablo 4.21.
- Kardeş belge (şekiller): `DETAYLI-IZAHAT.md` (Şekil 4.1–4.27).
- Bu belge yalnız var olanı izah eder; hiçbir analizi/sonucu değiştirmez.
