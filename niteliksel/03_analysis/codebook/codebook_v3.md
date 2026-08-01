# Codebook v3 — Kanonik Kod Listesi (Kod ↔ Eksen ↔ Makro-Tema)

**Versiyon:** 3.0 | **Tarih:** 2026-07-29 | **Durum:** Kanonik (Task 1.3 çıktısı)
**Önceki sürüm:** `codebook_v2.md` (2026-05-04, 23 kod)
**Gibi dosyalar:**
- Tüketir: `theme_architecture_v3.md` (4 makro/17 alt-tema + 8-eksen Rosetta)
- Tüketir: `codebook_v2.md` (kod adları ve tanımlar temeli)
- Tüketir: `niteliksel/new/triadik_matris_extracted.csv` (eksen doluluk doğrulaması)
- Üretir: ch07 kod ağacı ekinin kaynağı

> **KVKK (sert sınır):** Bu belgede gerçek ad, doğum tarihi veya adres yer almaz.
> Kanıt `quote_id` formatıyla gösterilir: `{aile_no}_{rol}_{q}_{eksen}`.
> Verbatim transkript bloğu konulmamıştır. Katılımcı verisi hiçbir harici
> MCP/connector'a gönderilmemiştir.

---

## Özet

| Boyut | v2 | v3 | Değişim |
|---|---|---|---|
| Toplam kod sayısı | 23 | **24** | +1 yeni |
| Kategori sayısı | 5 | 5 | değişmez |
| Yazım hatası düzeltme | `AILE_ICI_ADELET` | `AILE_ICI_ADALET` | düzeltildi |
| Yeni kod | — | `KARDES_KORUYUCU_ROLU` | v2'de önerilmişti |
| Kaldırılan kod | — | — | yok |
| Birleştirilen kod | — | — | yok |
| 8-eksen hizalama | yok | **var** — her koda baskın eksen atandı | yeni katman |
| Makro-tema hizalama | kısmi (Bölüm 4 v2) | **tam** — her koda birincil T1–T4 atandı | güçlendirildi |

**Metodolojik çerçeve:** Braun & Clarke (2022) refleksif tematik analiz (RTA).
Kodlar iteratif inşa edilen merkezi düzenleyici kavramlardır; bu versiyon tema
mimarisi v3'ün 8-eksen Rosetta tablosuyla hizalanmış kanonik formdur.
**Frekans ≠ önem:** Kod yoğunluğu denetim sayısıdır; tema önemi araştırma
sorusundaki merkezi düzenleyici işleviyle değerlendirilir.

---

## 1. Kanonik Kod Listesi (24 Kod, 5 Kategori)

Her giriş:
- **ID** — kanonik kod kimliği
- **Kısa ad**
- **Tanım** — çalışma tanımı (RTA'da iteratif; v1 tabanından genişletildi)
- **Dahil et / Hariç tut** — kodlama sınırı
- **Baskın triadik eksen** — `new/triadik_matris_extracted.csv` ile doğrulanmış birincil eksen (ve ikincil varsa)
- **Birincil makro tema** — alt-tema bağlamıyla; çoklu eşleşme mümkün, birincil kalın
- **Perspektif** — kodun ağırlıklı görüldüğü bilgi verici(ler)
- **Örnek quote_id** — KVKK-uyumlu referans (anonimleştirilmiş; verbatim alıntı değil)

---

### Kategori 1 — Tanı ve İlk Dönem Deneyimi (3 Kod)

---

#### KOD-01: `TANI_SOK_KORKU`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Tanı şoku / korku |
| **Tanım** | Tanı anında ve hemen sonrasında yaşanan yoğun şok, korku, "dünya başıma yıkıldı" ve varoluşsal çöküş anlatıları; belirsizlik, anlamsızlık, çaresizlik hissi. İlk dönem duygusal sarsılmayı — tanı sonrası suçluluk döngüsüne (bkz. T2.1 + SUCLULUK) geçişten önce — kapsar. |
| **Dahil et** | Tanı anı; "dünya yıkıldı" metaforları; acil belirsizlik; "ne olacak?" korkusu |
| **Hariç tut** | Sonraki dönem rutin kaygılar (→ KAYGI_KIRILGANLIK); suçluluk anlatıları (→ SUCLULUK) |
| **Baskın eksen** | `hastalik_algisi` |
| **Birincil makro tema** | **T2** (alt-tema 2.1 — Tanı Sonrası Suçluluk + Sarsılan Annelik Kimliği); T3 ve T1 cross-perspektif |
| **Perspektif** | Anne (birincil), hasta çocuk, kardeş (cross) |
| **Örnek quote_id** | `026_mother_q_hastalik` · `014_mother_q_hastalik` · `011_healthy_sibling_q_hastalik` |

---

#### KOD-02: `TANI_HASTANE_SURECI`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Hastane süreci |
| **Tanım** | Hastaneye yatış, ilk tedavi eğitimi, ilk insülin ve ölçüm pratiği, sağlık personeli ile kurulan ilk temas; "bize öğrettiler" anlatıları. Tanı döneminin pratik-tıbbi boyutunu kapsar; duygusal sarsılmadan (→ TANI_SOK_KORKU) ve bilgi arayışından (→ TANI_BILGI_ARAYISI) ayrıştırılır. |
| **Dahil et** | Yatış/servis süreci; eğitim ve ilk pratik; hemşire/doktor ile temas; ilk iğne/ölçüm |
| **Hariç tut** | Tanı anı duyguları (→ TANI_SOK_KORKU); sonraki kontrol süreçleri |
| **Baskın eksen** | `hastalik_algisi` |
| **Birincil makro tema** | **T2** (2.1) + **T3** (3.2) |
| **Perspektif** | Anne, hasta çocuk |
| **Örnek quote_id** | `011_mother_q_hastalik` |

---

#### KOD-03: `TANI_BILGI_ARAYISI`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Bilgi arayışı |
| **Tanım** | Tanı sonrası yoğun bilgi arayışı; internetten, sağlık ekibinden ve çevreden öğrenme çabası; "ne yapacağız, nasıl yönetiriz?" anlatıları. Pratik-entelektüel uyum çabasını duygusal sarsılmadan ayrıştırır. |
| **Dahil et** | "Araştırdım, sordum"; pratik öğrenme anlatıları; diyet/insülin öğrenme |
| **Hariç tut** | Duygusal destek arayışı (→ AILE_DESTEGI / SAGLIK_EKIBI_DESTEGI); rutin takip (→ RUTIN_TAKIP) |
| **Baskın eksen** | `hastalik_algisi` |
| **Birincil makro tema** | **T2** (2.1) |
| **Perspektif** | Anne (birincil) |
| **Örnek quote_id** | `014_mother_q_hastalik` |

---

### Kategori 2 — Günlük Yönetim Yükü ve Rutinlerin Yeniden Örgütlenmesi (5 Kod)

---

#### KOD-04: `RUTIN_TAKIP`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Takip rutini |
| **Tanım** | Günlük ölçüm–insülin–doz ayarı–kayıt döngüsünün sürekliliği; evde, okulda ve dışarıda sürdürülen yönetim rutini. Yönetim yükünün kronolojik boyutunu kapsar; beslenme kısıtları (→ BESLENME_KONTROL) ve gece takip (→ GECE_TAKIP) ayrı kodlanır. |
| **Dahil et** | "Her gün ölçüm/insülin"; doz ayarı; okulda/dışarıda yönetim döngüsü |
| **Hariç tut** | Sadece diyet/beslenme (→ BESLENME_KONTROL); gece ritüeli (→ GECE_TAKIP); teknoloji (→ TEKNOLOJI_DESTEGI) |
| **Baskın eksen** | `gunluk_sosyal` |
| **İkincil eksen** | `kisit` |
| **Birincil makro tema** | **T2** (2.2) + **T4** (4.1) |
| **Perspektif** | Anne (birincil), hasta çocuk |
| **Örnek quote_id** | `026_mother_q_gunluk` · `019_mother_q_gunluk` · `014_mother_q_gunluk` |

---

#### KOD-05: `BESLENME_KONTROL`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Beslenme kontrolü |
| **Tanım** | Karbonhidrat sayımı, diyet kısıtlamaları ve evde ortak yeme düzeninin yeniden örgütlenmesi; aile üyelerinin de kısıtlandığı paylaşılmış kısıtlılık örüntüsü. Tüm triaddaki en cross-cutting kodlardan biridir: anne yönetim yükünü, hasta çocuk bedensel özerklik kaybını, kardeş gönüllü mahrumiyeti ön plana taşır. |
| **Dahil et** | Diyet; karbonhidrat sayımı; "evde artık ... yemiyoruz"; gönüllü kısıtlama |
| **Hariç tut** | Okul kafeteryasındaki sosyal dinamikler (→ OKUL_SOSYAL_UYUM); gece beslenme (→ GECE_TAKIP) |
| **Baskın eksen** | `kisit` |
| **Birincil makro tema** | **T4** (4.1 — tüm triad; ortak kısıtlılıklar); T1 (1.1), T2 (2.2), T3 (3.2) |
| **Perspektif** | Tümü |
| **Örnek quote_id** | `011_mother_q_kisit` · `019_sibling_q_kisit` · `019_patient_q_kisit` |

---

#### KOD-06: `GECE_TAKIP`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Gece uyanıklığı |
| **Tanım** | Gece hipoglisemi korkusu; alarm kurma, gece ölçümü yapma, uyku bölünmesi; klinisyen iznini aşan gece rutinleri. Kaybetme korkusunun davranışsal yansıması olarak annenin kaygı yönetim mekanizması işlevi görür. |
| **Dahil et** | Gece ölçümü; alarm; gece hasta başında bekleme; uyku bozukluğu |
| **Hariç tut** | Gündüz takip rutini (→ RUTIN_TAKIP); genel kaybetme korkusu (→ KAYGI_KIRILGANLIK) |
| **Baskın eksen** | `kaybetme_korkusu` |
| **İkincil eksen** | `annelik_donusum` |
| **Birincil makro tema** | **T2** (2.2 + 2.3) |
| **Perspektif** | Anne (birincil) |
| **Örnek quote_id** | `026_mother_q_kaybetme` · `014_mother_q_kaybetme` · `019_mother_q_kaybetme` |

---

#### KOD-07: `OKUL_SOSYAL_UYUM`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Okul / sosyal uyum |
| **Tanım** | Okulda ölçüm/insülin yönetimi; öğretmen ve akranlarla uyum; gezilerde ve okul etkinliklerinde katılım kısıtları; kurumsal yapısal kırılganlıklar (okulda bekleyen anne, sınıfta ölçüm utancı). |
| **Dahil et** | Okul kafeteryası; sınıfta ölçüm; öğretmen farkındalığı; gezilerde kısıt |
| **Hariç tut** | Ev içi rutin (→ RUTIN_TAKIP); genel akran damgalanması (→ AKRAN_CEVRE_DESTEGI) |
| **Baskın eksen** | `gunluk_sosyal` |
| **Birincil makro tema** | **T3** (3.3 + 3.2) |
| **Perspektif** | Hasta çocuk (birincil), kardeş, anne |
| **Örnek quote_id** | `019_patient_q_gunluk` · `026_mother_q_gunluk` · `011_patient_q_gunluk` |

---

#### KOD-08: `TEKNOLOJI_DESTEGI`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Teknoloji desteği |
| **Tanım** | Sensör, pompa ve izleme uygulaması kullanımı; teknoloji erişiminin sağladığı güven ve rahatlamanın yanı sıra finansal yük, erişim eşitsizliği ve sistemik destek boşluğu anlatıları. `ihtiyaclar` ekseninde aynı zamanda sistemik talep boyutunu kapsar. |
| **Dahil et** | Sensör/pompa talebi ve kullanımı; "sensör olunca rahatladık"; SGK/finansal kısıt |
| **Hariç tut** | Sağlık ekibi ilişkisi (→ SAGLIK_EKIBI_DESTEGI); ilaç tedavisinin kendisi (→ RUTIN_TAKIP) |
| **Baskın eksen** | `ihtiyaclar` |
| **Birincil makro tema** | **T2** (2.2) + **T3** (3.4) |
| **Perspektif** | Anne (birincil), hasta çocuk |
| **Örnek quote_id** | `026_patient_q_ihtiyaclar` · `011_mother_q_ihtiyaclar` · `026_mother_q_ihtiyaclar` |

---

### Kategori 3 — Duygusal Deneyim ve Anlamlandırma (5 Kod)

---

#### KOD-09: `KAYGI_KIRILGANLIK`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Süreğen kaygı |
| **Tanım** | Sürekli tetikte olma, kronik belirsizlik ve "bir şey olacak" korkusu; triadın tamamında gözlemlenen ortak duygusal iklim. Tanı anı şokundan (→ TANI_SOK_KORKU) ve spesifik gece korkusundan (→ GECE_TAKIP) ayrıştırılır; daha geniş ve kronik kaygı halini kapsar. |
| **Dahil et** | "Hep endişeliyim"; kronik kaygı; "ne olacak bilmiyorum"; belirsizlik içinde yaşama |
| **Hariç tut** | Tanı anı şoku (→ TANI_SOK_KORKU); gece özgül korkusu (→ GECE_TAKIP); spesifik kaybetme senaryoları (→ ANNE_HIPERVIJILANS) |
| **Baskın eksen** | `kaybetme_korkusu` |
| **Birincil makro tema** | **T4** (4.2 — triadik kaybetme kaygısı; tüm perspektiflerde); T2 (2.3) destekleyici |
| **Perspektif** | Tümü |
| **Örnek quote_id** | `019_mother_q_kaybetme` · `011_sibling_q_kaybetme` · `026_sibling_q_kaybetme` |

---

#### KOD-10: `SUCLULUK`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Suçluluk |
| **Tanım** | "Benim yüzümden oldu" hissi; annenin öz-sorgulaması, günlük kararlar üzerindeki vicdan baskısı ("kızdım, yaptım, yapmadım") ve psikosomatik empati; ayrıca sağlıklı kardeşin kıskançlık-suçluluk döngüsü. |
| **Dahil et** | "Kendimi suçladım"; vicdan anlatıları; yanlış yaptım mı sorusu; kardeşin "istemezdim ama" suçluluğu |
| **Hariç tut** | Genel üzüntü (suçluluk yok); öfke ve adaletsizlik (→ OFKE_ADALETSIZLIK) |
| **Baskın eksen** | `annelik_donusum` |
| **İkincil eksen** | `hastalik_algisi` |
| **Birincil makro tema** | **T2** (2.1) |
| **Perspektif** | Anne (birincil), kardeş (ek) |
| **Örnek quote_id** | `014_mother_q_hastalik` · `026_mother_q_hastalik` · `019_mother_q_annelik` |

---

#### KOD-11: `OFKE_ADALETSIZLIK`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Öfke / adaletsizlik |
| **Tanım** | Hastalığa, duruma ve eşitsizliğe dair öfke anlatıları; "neden bize/bana", "bu adil değil"; kardeşin ilgi asimetrisine öfkesi, hasta çocuğun sosyal kısıtlamalara öfkesi. Basit kıskançlıktan analitik olarak ayrıştırılır (KVKK M31 yorumlama disiplini). |
| **Dahil et** | "Bu adil değil"; "neden hep benim başıma"; "sinirleniyorum çünkü"; kısıtlamaya direniş |
| **Hariç tut** | Yalnızca üzüntü (öfke yok); suçluluk (→ SUCLULUK) |
| **Baskın eksen** | `kardes_yasantisi` |
| **İkincil eksen** | `kisit` |
| **Birincil makro tema** | **T1** (1.3 — çok boyutlu adaletsizlik) |
| **Perspektif** | Kardeş (birincil), hasta çocuk, anne (cross) |
| **Örnek quote_id** | `014_sibling_q_annelik` · `014_healthy_sibling_q_ergenlik` |

---

#### KOD-12: `KABULLENME_NORMALLESME`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Kabullenme / normalleşme |
| **Tanım** | Zamanla alışma, hastalığı günlük rutine oturtma ve normalleştirme anlatıları; "artık normal geliyor", "bir yaşam tarzı" söylemi; avantaja çevirme stratejileri. Yorumlama disiplini gerektirir: normalleştirme söylemi hem özgün uyum hem duygusal baskılamanın göstergesi olabilir. |
| **Dahil et** | "Artık alıştık"; "bir yaşam tarzı"; avantaj çerçeveleme ("ücretsiz müzeye girebiliyorum") |
| **Hariç tut** | İnkar/direnç (→ ILETISIM_CATISMA); yarar bulma anlatıları (→ YARAR_BULMA_OLGUNLASMA) |
| **Baskın eksen** | `hastalik_algisi` |
| **Birincil makro tema** | **T3** (3.1 — "hiçbir şey değişmedi" söylemi) |
| **Perspektif** | Hasta çocuk (birincil), anne (destekleyici) |
| **Örnek quote_id** | `014_patient_q_gunluk` · `026_patient_q_hastalik` · `011_mother_q_hastalik` |

---

#### KOD-13: `YARAR_BULMA_OLGUNLASMA`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Yarar bulma / olgunlaşma |
| **Tanım** | Hastalık deneyiminden empati, sorumluluk ve erken olgunlaşma kazanımı; "daha güçlü/bilinçli oldum", "sorumluluk öğrendim" anlatıları. Hem hasta çocukta hem sağlıklı kardeşte görülür; kardeşte T1.2 (erken olgunlaşma) ile bağlantılı. Normalleştirmeden (→ KABULLENME_NORMALLESME) ayrı: burada aktif anlam inşası söz konusudur. |
| **Dahil et** | "Daha olgun oldum"; "sorumluluk öğrendim"; "bize güç verdi"; post-hoc anlam çerçeveleme |
| **Hariç tut** | Basit "alıştık" normalleştirmesi (→ KABULLENME_NORMALLESME) |
| **Baskın eksen** | `kardes_yasantisi` |
| **İkincil eksen** | `hastalik_algisi` |
| **Birincil makro tema** | **T1** (1.2 — erken olgunlaşma) + **T3** (cross) |
| **Perspektif** | Kardeş, hasta çocuk, anne (cross) |
| **Örnek quote_id** | `026_sibling_q_kardes` · `019_sibling_q_kardes` |

---

### Kategori 4 — Aile İlişkileri ve Rollerin Dönüşümü (7 Kod)

> **Not:** v3'te bu kategoriye 1 yeni kod eklenmiştir: `KARDES_KORUYUCU_ROLU` (bkz. v2→v3 değişim tablosu).

---

#### KOD-14: `ANNE_HIPERVIJILANS`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Anne hipervijilansı |
| **Tanım** | Annenin sürekli izleme, kontrol etme ve bırakmakta zorlanma hali; klinisyen iznini aşan gece ölçümleri, okulun önünde bekleme, sosyal etkinliklerden geri çekilme; "kontrol etmeden duramıyorum". Kaybetme korkusunun davranışsal çıktısı, annelik dönüşümünün baskın görünümü. |
| **Dahil et** | Sürekli kontrol; "bırakmak istemiyorum"; yalnız bırakmama; okulda bekleme |
| **Hariç tut** | Gece özgül ritüeli (→ GECE_TAKIP); genel kaygı (→ KAYGI_KIRILGANLIK) |
| **Baskın eksen** | `annelik_donusum` |
| **İkincil eksen** | `kaybetme_korkusu` |
| **Birincil makro tema** | **T2** (2.2 + 2.3) |
| **Perspektif** | Anne |
| **Örnek quote_id** | `026_mother_q_gunluk` · `019_mother_q_kaybetme` · `014_mother_q_gunluk` |

---

#### KOD-15: `COCUK_OZERKLIK_OZBAKIM`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Özerklik / öz-bakım |
| **Tanım** | T1DM'li çocuğun özerklik talepleri ve "ben yapabilirim" söylemi; anne-çocuk kontrol gerilimi; ergenlikle yoğunlaşan bağımsızlaşma çabası ve diyabet yönetimini sahiplenme ya da reddedme dinamiği. |
| **Dahil et** | "Kendim yapmak istiyorum"; "bırak ben yapayım"; bakımı gizli yönetme |
| **Hariç tut** | İletişim çatışmaları (→ ILETISIM_CATISMA); okul uyumu (→ OKUL_SOSYAL_UYUM) |
| **Baskın eksen** | `ergenlik` |
| **İkincil eksen** | `annelik_donusum` |
| **Birincil makro tema** | **T3** (3.4) + **T2** (2.4) |
| **Perspektif** | Hasta çocuk (birincil), anne |
| **Örnek quote_id** | `020_mother_q_ergenlik` · `019_patient_q_kisit` · `202_patient_q_ergenlik` |

---

#### KOD-16: `KARDES_GORUNMEZ_YUK`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Kardeşin görünmez yükü |
| **Tanım** | Sağlıklı kardeşin ilgi asimetrisinden kaynaklanan ikinci planda kalma deneyimi; gönüllü mahrumiyet ve fark edilmeyen duygusal yük; "ben de isterdim ama". Pasif geri planda kalma boyutunu kapsar; aktif nöbet rolü için bkz. `KARDES_KORUYUCU_ROLU`. |
| **Dahil et** | "İkinci planda kaldım"; "benim de canım çekti ama yiyemedim"; fark edilmeme |
| **Hariç tut** | Aktif nöbet/bakım rolü (→ KARDES_KORUYUCU_ROLU); kardeş ilişkisi dönüşümü (→ KARDES_ILISKISI) |
| **Baskın eksen** | `kardes_yasantisi` |
| **İkincil eksen** | `kisit` |
| **Birincil makro tema** | **T1** (1.1 + 1.3) |
| **Perspektif** | Kardeş (birincil), anne (farkındalık anlatısı) |
| **Örnek quote_id** | `019_mother_q_kardes` · `014_sibling_q_annelik` · `011_healthy_sibling_q_kisit` |

---

#### KOD-17: `KARDES_ILISKISI`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Kardeş ilişkisi |
| **Tanım** | Kardeşler arasındaki ilişkinin T1DM sürecinde dönüşümü — yakınlaşma ve bağ güçlenmesi, ama aynı zamanda "hasta otoritesi" kaynaklı çatışma, güç dengesizliği ve sınır müzakeresi. Karşılıklı dönüşümü vurgular. |
| **Dahil et** | "Eskiden kavga ederdik, şimdi..."; "aramızdaki bağ güçlendi"; hasta otoritesi çatışması |
| **Hariç tut** | Yalnızca görünmez yük (→ KARDES_GORUNMEZ_YUK); yalnızca nöbet rolü (→ KARDES_KORUYUCU_ROLU) |
| **Baskın eksen** | `kardes_yasantisi` |
| **Birincil makro tema** | **T1** (1.2 + 1.3 cross) + **T4** (4.4) |
| **Perspektif** | Kardeş, hasta çocuk |
| **Örnek quote_id** | `014_sibling_q_kardes` · `026_patient_q_kardes` · `019_patient_q_kardes` |

---

#### KOD-18: `AILE_ICI_ADALET`

> **v2 → v3 düzeltme:** `AILE_ICI_ADELET` (yazım hatası) → `AILE_ICI_ADALET`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Aile içi adalet |
| **Tanım** | Ailedeki dikkat, zaman ve kaynakların dağılımındaki algılanan eşitsizlik; annenin adalet ikilemi, kardeşin ilgi asimetrisi algısı ve T1DM'li çocuğun "el üstünde tutulmak" ya da "ikinci planda kalmak" arasındaki gerilim. Aynı ebeveyn davranışı üç bilgi verici tarafından farklı anlam çerçevelerine oturtulmaktadır — bu anlam asimetrisi tezin temel triadik bulgusudur. |
| **Dahil et** | Dikkat dağılımı adaletsizliği; annenin adalet ikilemi; "haksızlık yaptığımın farkındayım"; kardeşin "neden hep o" sorusu |
| **Hariç tut** | Sadece kardeş geri planda kalma (→ KARDES_GORUNMEZ_YUK); iletişim çatışmaları (→ ILETISIM_CATISMA) |
| **Baskın eksen** | `kardes_yasantisi` |
| **İkincil eksen** | `annelik_donusum` |
| **Birincil makro tema** | **T4** (4.3 — üç perspektif farklı okur; anlam asimetrisi); T1 (1.3) + T2 (2.6) destekleyici |
| **Perspektif** | Tümü |
| **Örnek quote_id** | `014_sibling_q_annelik` · `014_mother_q_kardes` · `014_patient_q_annelik` |

---

#### KOD-19: `ILETISIM_CATISMA`

| Alan | İçerik |
|---|---|
| **Kısa ad** | İletişim / çatışma |
| **Tanım** | Aile içi iletişim gerilimleri, diyabet yönetimi kuralları etrafındaki çatışmalar ve ergenlikle yoğunlaşan sınır müzakereleri; "laf dinlemiyor", gizli yeme, anne-çocuk geriliminin patlama noktaları. |
| **Dahil et** | Çatışma anlatıları; kural ihlalleri; "bağırıyorum artık"; sessizlik ve çekilme |
| **Hariç tut** | Yalnız duygu paylaşımı; özerklik talebi (→ COCUK_OZERKLIK_OZBAKIM) |
| **Baskın eksen** | `ergenlik` |
| **İkincil eksen** | `annelik_donusum` |
| **Birincil makro tema** | **T2** (2.4) + **T3** (cross) |
| **Perspektif** | Anne, hasta çocuk |
| **Örnek quote_id** | `020_mother_q_ergenlik` · `014_mother_q_ergenlik` · `011_mother_q_ergenlik` |

---

#### KOD-20 (YENİ v3): `KARDES_KORUYUCU_ROLU`

> **v3'te eklendi.** v2'de önerilmişti ("KARDES_KORUYUCU_ROLU eklensin mi?" — Bölüm 8, Öneri). `theme_architecture_v3.md` Alt-tema 1.2 ("Erken Olgunlaşma ve Nöbetçi Kardeş Rolü") bu kodun kanonik alt-temasıdır. `KARDES_GORUNMEZ_YUK` ile kısmi örtüşme vardır; ayrım şöyle: Görünmez Yük = pasif/fark edilmeme; Koruyucu Rol = aktif nöbet ve bakım emeği.

| Alan | İçerik |
|---|---|
| **Kısa ad** | Kardeşin koruyucu rolü |
| **Tanım** | Sağlıklı kardeşin "nöbetçi kardeş" veya "küçük bakıcı" rolüne geçişi; hipoglisemi ataklarına hazırlık, hasta kardeşin şekerini aktif izleme, acil durum yöneticisi kimliği ve bu sorumluluğun çocukluk döneminden erken sıyrılmaya yol açması. T4.4 "küçük bakıcılar" alt-tematik bağlantısı güçlüdür. |
| **Dahil et** | "Şekeri düştüğünde ne yapacağımı öğrendim"; "her zaman peşindeyim"; "acil durumda ben hallediyorum" |
| **Hariç tut** | Pasif geri planda kalma (→ KARDES_GORUNMEZ_YUK); kardeşlik ilişkisi değişimi genel (→ KARDES_ILISKISI) |
| **Baskın eksen** | `kardes_yasantisi` |
| **İkincil eksen** | `kaybetme_korkusu` |
| **Birincil makro tema** | **T1** (1.2 — erken olgunlaşma + nöbetçi kardeş); T4 (4.4) destekleyici |
| **Perspektif** | Kardeş (birincil), anne (gözlemci anlatı) |
| **Örnek quote_id** | `026_mother_q_kardes` · `014_sibling_q_kaybetme` · `019_sibling_q_kardes` · `011_healthy_sibling_q_kardes` |

---

### Kategori 5 — Başa Çıkma Kaynakları ve Destek Sistemleri (4 Kod)

---

#### KOD-21: `AILE_DESTEGI`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Aile içi destek |
| **Tanım** | Eş, büyükanne ve diğer aile üyeleriyle rol paylaşımı ve iş bölümü; duygusal destek ve yükü birlikte taşıma. Ayrıca annenin eş rolünün silikleşmesi ve mahremiyet kaybı da bu kodla etiketlenir — bakım yükünün çift ilişkisine yansıması. |
| **Dahil et** | "Eşim destek oldu"; "baba üstlendi"; "birlikte hallettik"; eş rolü silikleşmesi |
| **Hariç tut** | Sağlık ekibi (→ SAGLIK_EKIBI_DESTEGI); destek boşluğu (→ SAGLIK_EKIBI_DESTEGI kapsamında da) |
| **Baskın eksen** | `annelik_donusum` |
| **Birincil makro tema** | **T2** (2.5 + 2.6) |
| **Perspektif** | Anne |
| **Örnek quote_id** | `014_mother_q_hastalik` (vicdan metaforu) |

---

#### KOD-22: `SAGLIK_EKIBI_DESTEGI`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Sağlık ekibi |
| **Tanım** | Doktor ve hemşireden alınan eğitim, danışmanlık ve duygusal destek; sağlık ekibiyle kurulan güven ilişkisi ya da hissedilen destek boşluğu ve sistemik kırılganlık. Erişim eşitsizliği anlatıları bu kodda toplanır. |
| **Dahil et** | "Doktor açıkladı, rahatladım"; hemşire eğitimi; "destek bulamadım" |
| **Hariç tut** | Teknoloji/sensör erişimi (→ TEKNOLOJI_DESTEGI); akran desteği (→ AKRAN_CEVRE_DESTEGI) |
| **Baskın eksen** | `ihtiyaclar` |
| **Birincil makro tema** | **T2** + **T3** (cross) |
| **Perspektif** | Anne (birincil), hasta çocuk |
| **Örnek quote_id** | `026_mother_q_ihtiyaclar` · `011_mother_q_ihtiyaclar` |

---

#### KOD-23: `AKRAN_CEVRE_DESTEGI`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Akran / çevre desteği |
| **Tanım** | Arkadaş, okul çevresi ve sosyal ağdan destek ya da dışlanma deneyimi; damgalanma kaygısı ve sosyal görünürlük yönetimi (başkalarına söyleme/söylememe kararı). T3.3 (utanç ve damgalanma) ile doğrudan bağlantılıdır. |
| **Dahil et** | "Arkadaşlarım yardım etti"; "dışlanmışlık gibi oluyor"; "söylemedim çünkü..."; sosyal kısıt |
| **Hariç tut** | Okul kurumsal yönetimi (→ OKUL_SOSYAL_UYUM); sağlık ekibi (→ SAGLIK_EKIBI_DESTEGI) |
| **Baskın eksen** | `gunluk_sosyal` |
| **Birincil makro tema** | **T3** (3.3) |
| **Perspektif** | Hasta çocuk (birincil), kardeş |
| **Örnek quote_id** | `019_patient_q_gunluk` · `011_patient_q_gunluk` · `020_patient_q_gunluk` |

---

#### KOD-24: `MANEVI_BASA_CIKMA`

| Alan | İçerik |
|---|---|
| **Kısa ad** | Manevi başa çıkma |
| **Tanım** | İnanç, dua ve kadere dair söylemler; "Allah bir çaresini gösterir", "elhamdülillah bir çözümü var" — manevi anlam çerçevesinin kaygı yönetiminde işlev görmesi. Anne anlatısında belirgin; bazı ailelerde dayanıklılık kaynağı. |
| **Dahil et** | İnanç temelli ifadeler; kader çerçeveleme; manevi teselli |
| **Hariç tut** | Rasyonel bilgi arayışı (→ TANI_BILGI_ARAYISI); yarar bulma (→ YARAR_BULMA_OLGUNLASMA) |
| **Baskın eksen** | `annelik_donusum` |
| **Birincil makro tema** | **T2** (cross) |
| **Perspektif** | Anne (birincil) |
| **Örnek quote_id** | `011_mother_q_hastalik` |

---

## 2. v2 → v3 Kod Değişim Tablosu

| Kod | Durum | Değişim Açıklaması |
|---|---|---|
| `TANI_SOK_KORKU` | **Korunan** | Tanım genişletildi (varoluşsal boyut eklendi); eksen ve makro-tema atandı |
| `TANI_HASTANE_SURECI` | **Korunan** | Eksen ve makro-tema atandı |
| `TANI_BILGI_ARAYISI` | **Korunan** | Eksen ve makro-tema atandı |
| `RUTIN_TAKIP` | **Korunan** | T4 (4.1) birincil tema olarak eklendi; eksen atandı |
| `BESLENME_KONTROL` | **Korunan** | T4 birincil makro tema atandı (cross-cutting vurgusu güçlendi) |
| `GECE_TAKIP` | **Korunan** | `kaybetme_korkusu` baskın eksen olarak atandı |
| `OKUL_SOSYAL_UYUM` | **Korunan** | Eksen ve makro-tema atandı |
| `TEKNOLOJI_DESTEGI` | **Korunan** | `ihtiyaclar` baskın eksen olarak atandı; sistemik boyut vurgulandı |
| `KAYGI_KIRILGANLIK` | **Korunan** | T4 (4.2) birincil tema olarak atandı — triadik kapsam vurgusu |
| `SUCLULUK` | **Korunan** | Eksen ve makro-tema atandı; psikosomatik empati boyutu eklendi |
| `OFKE_ADALETSIZLIK` | **Korunan** | Eksen ve makro-tema atandı |
| `KABULLENME_NORMALLESME` | **Korunan** | Yorumlama disiplini notu eklendi (baskılama vs. uyum) |
| `YARAR_BULMA_OLGUNLASMA` | **Korunan** | T1 (1.2) ile bağlantı netleştirildi |
| `ANNE_HIPERVIJILANS` | **Korunan** | `annelik_donusum` baskın eksen, `kaybetme_korkusu` ikincil |
| `COCUK_OZERKLIK_OZBAKIM` | **Korunan** | `ergenlik` baskın eksen atandı |
| `KARDES_GORUNMEZ_YUK` | **Korunan** | `KARDES_KORUYUCU_ROLU` ile ayrım netleştirildi |
| `KARDES_ILISKISI` | **Korunan** | T4 (4.4) bağlantısı eklendi |
| ~~`AILE_ICI_ADELET`~~ → `AILE_ICI_ADALET` | **Düzeltildi** | Yazım hatası giderildi (v2'de notlanmıştı); T4 (4.3) birincil makro tema atandı; triadik anlam asimetrisi vurgusu güçlendi |
| `ILETISIM_CATISMA` | **Korunan** | `ergenlik` baskın eksen atandı |
| `AILE_DESTEGI` | **Korunan** | T2 (2.5) — eş rolü silikleşmesi bağlantısı eklendi |
| `SAGLIK_EKIBI_DESTEGI` | **Korunan** | `ihtiyaclar` baskın eksen atandı |
| `AKRAN_CEVRE_DESTEGI` | **Korunan** | T3 (3.3) birincil bağlantısı netleştirildi |
| `MANEVI_BASA_CIKMA` | **Korunan** | Eksen ve makro-tema atandı |
| **`KARDES_KORUYUCU_ROLU`** | **YENİ** | v2 Bölüm 8 önerisi onaylandı; T1.2 (Erken Olgunlaşma) ve T4.4 (Küçük Bakıcılar) için kanonik kod; `KARDES_GORUNMEZ_YUK`'tan ayrıştırılmış (pasif yük vs. aktif nöbet) |

**Özet:** 23 korunan + 1 yazım düzeltmesi + 1 yeni = **24 kanonik kod**. Kaldırılan veya birleştirilen kod yok.

---

## 3. Doğrulama: Makro Tema × Kod Kapsama Tablosu

> Task gerekliliği: Her makro tema (T1–T4) codebook'ta ≥1 kodla eşli.

| Makro Tema | Birincil Kodlar (v3) | Adet |
|---|---|---|
| **T1** — Sağlıklı Kardeşin Görünmeyen Yükü | `KARDES_GORUNMEZ_YUK` · `KARDES_KORUYUCU_ROLU` · `OFKE_ADALETSIZLIK` · `YARAR_BULMA_OLGUNLASMA` · `KARDES_ILISKISI` | **5** |
| **T2** — Anneliğin Tıbbi Bakıcıya Kayması | `TANI_SOK_KORKU` · `TANI_HASTANE_SURECI` · `TANI_BILGI_ARAYISI` · `RUTIN_TAKIP` · `GECE_TAKIP` · `TEKNOLOJI_DESTEGI` · `SUCLULUK` · `ANNE_HIPERVIJILANS` · `ILETISIM_CATISMA` · `AILE_DESTEGI` · `SAGLIK_EKIBI_DESTEGI` · `MANEVI_BASA_CIKMA` | **12** |
| **T3** — Hastalığın İçinden: T1DM'li Çocuk | `KABULLENME_NORMALLESME` · `OKUL_SOSYAL_UYUM` · `COCUK_OZERKLIK_OZBAKIM` · `AKRAN_CEVRE_DESTEGI` | **4** |
| **T4** — Aynı Evde Üç Farklı Deneyim (Triadik) | `BESLENME_KONTROL` (4.1) · `KAYGI_KIRILGANLIK` (4.2) · `AILE_ICI_ADALET` (4.3) | **3** |

**Sonuç:** T1 ✓ (5 kod) · T2 ✓ (12 kod) · T3 ✓ (4 kod) · T4 ✓ (3 kod) — **Tüm makro temalar ≥1 kod ile karşılandı.**

> **Nota bene:** Pek çok kod birden fazla makro temada destekleyici işlev görür (örn. `BESLENME_KONTROL` aynı zamanda T1+T2+T3'te). Yukarıda yalnızca birincil ataması gösterilmiştir.

---

## 4. Doğrulama: 8 Eksen × Kod Kapsama Tablosu

> Task gerekliliği: 8 eksenin (hastalik_algisi … ihtiyaclar) hepsi ≥1 kodla eşli.

| Triadik Eksen | Baskın Eksen Olan Kodlar | Eksen Kanıtı (CSV alıntı sayısı) | Durum |
|---|---|---|---|
| `hastalik_algisi` | `TANI_SOK_KORKU` · `TANI_HASTANE_SURECI` · `TANI_BILGI_ARAYISI` · `KABULLENME_NORMALLESME` | 20 alıntı | ✓ |
| `kisit` | `BESLENME_KONTROL` · `KARDES_GORUNMEZ_YUK` (ikincil) · `OFKE_ADALETSIZLIK` (ikincil) | 16 alıntı | ✓ |
| `gunluk_sosyal` | `RUTIN_TAKIP` · `OKUL_SOSYAL_UYUM` · `AKRAN_CEVRE_DESTEGI` | 16 alıntı | ✓ |
| `ergenlik` | `COCUK_OZERKLIK_OZBAKIM` · `ILETISIM_CATISMA` | 8 alıntı (ince örüntü; COREQ M31) | ✓ |
| `kaybetme_korkusu` | `KAYGI_KIRILGANLIK` · `GECE_TAKIP` · `KARDES_KORUYUCU_ROLU` (ikincil) · `ANNE_HIPERVIJILANS` (ikincil) | 12 alıntı | ✓ |
| `kardes_yasantisi` | `KARDES_GORUNMEZ_YUK` · `KARDES_KORUYUCU_ROLU` · `KARDES_ILISKISI` · `YARAR_BULMA_OLGUNLASMA` · `OFKE_ADALETSIZLIK` · `AILE_ICI_ADALET` (ikincil) | 17 alıntı | ✓ |
| `annelik_donusum` | `ANNE_HIPERVIJILANS` · `SUCLULUK` · `ILETISIM_CATISMA` (ikincil) · `AILE_DESTEGI` · `MANEVI_BASA_CIKMA` · `AILE_ICI_ADALET` (ikincil) | 12 alıntı | ✓ |
| `ihtiyaclar` | `TEKNOLOJI_DESTEGI` · `SAGLIK_EKIBI_DESTEGI` | 8 alıntı (ince örüntü; COREQ M31) | ✓ |

**Sonuç:** 8/8 eksen ≥1 kodla karşılandı. ✓

**İnce-örüntü notu (COREQ M31):** `ergenlik` ve `ihtiyaclar` eksenleri 8/21 katılımcıda belgelenmiş ince örüntülerdir. `theme_architecture_v3.md` "Negatif Vaka" bölümünde ayrıntılı raporlanmıştır. Bu eksenlere bağlı kodlar codebook'ta kanonik olarak korunur; ancak bulgular bölümünde ince-örüntü işareti ve negatif vaka yorumuyla birlikte sunulmalıdır.

---

## 5. Metodolojik Notlar

1. **Frekans ≠ önem:** Kod yoğunluğu denetim sayısıdır; tema önemi araştırma sorusundaki merkezi düzenleyici işleviyle belirlenir (Braun & Clarke, 2022). Örn. `MANEVI_BASA_CIKMA` düşük kodlama sıklığına karşın T2 bütünlüğü için analitik değer taşımaktadır.

2. **Çoklu makro tema eşleşmesi:** Bir kodun birden fazla makro temada görünmesi, multi-informant triangülasyonunun doğal sonucudur; zayıflık değil güç işaretidir. T4 (triadik sentez) bu çakışmaları karşılaştırmalı olarak analiz eder.

3. **KARDES_KORUYUCU_ROLU vs. KARDES_GORUNMEZ_YUK ayrımı:** İki kod aynı analitik eksenin farklı boyutlarını kapsar: Görünmez Yük → pasif geri planda kalma ve fark edilmeme; Koruyucu Rol → aktif nöbet, acil durum hazırlığı ve bakım emeği. Kodlama sırasında her ikisi birlikte uygulanabilir (co-occurring codes).

4. **RTA inter-coder:** Kappa/AC1 hesaplanmamıştır — RTA epistemolojisi gereği. BA (eleştirel arkadaş / non-participant observer) biçimsel uzlaşı değil analitik derinlik amacıyla işbirliği yürütmüştür. (`niteliksel/03_analysis/methodology/` — positionality ve audit trail belgeleri).

5. **AILE_ICI_ADALET T4 ataması gerekçesi:** Aynı ebeveyn davranışı (yoğun bakım/dikkat) üç bilgi verici tarafından farklı anlam çerçevelerine oturtulmaktadır — bu anlam asimetrisi kodun triadik karşılaştırma (T4.3) işlevini öne çıkarır; aynı zamanda T1 (kardeş) ve T2 (annelik ikilemi) bağlantıları güçlüdür.

6. **BESLENME_KONTROL T4 ataması gerekçesi:** En cross-cutting kodlardan biridir — tüm triad aynı kısıtlılıkla farklı deneyimler yaşar; bu ortaklık T4.1 (Ortak Kısıtlılıklar) alt-tematik içeriğin tam karşılığıdır.

7. **v1 tanım tabanı:** Kod tanımları v1 (`codebook_draft_v1.md`) çalışma tanımlarını temel alır ve genişletir. v1 yorumlama başvuru belgesi olmayı sürdürmektedir.

8. **Journal-stil eşlemesi:** v2 Bölüm 4 Journal-Thesis hibrit haritalama (23 kod × J1-J6 × T1-T4) bu v3 ile uyumludur; v2'nin hibrit tablosu geçerliliğini korumaktadır. Her kodun journal bağlantısı için bkz. `codebook_v2.md` Bölüm 4.

---

## 6. Bağlantılı Belgeler

| Belge | İlişki |
|---|---|
| `codebook_v2.md` | Temel kod tanımları + journal-thesis hibrit haritalama (geçerli) |
| `theme_architecture_v3.md` | 4 makro tema × 17 alt-tema + 8-eksen Rosetta tablosu (bu v3'ün girdi belgesi) |
| `codebook_draft_v1.md` | Orijinal kod tanımları (arşiv; referans) |
| `niteliksel/new/triadik_matris_extracted.csv` | Eksen doluluk doğrulama kaynağı (110 alıntı, 8 eksen) |
| `niteliksel/03_analysis/methodology/` | COREQ, audit trail, positionality (OM/BA) |
| `t1dm-tez-rehberi/references/karma-yontem.md` | T4 → joint display karma yöntem köprüsü |

---

*Belge:* `niteliksel/03_analysis/codebook/codebook_v3.md`
*Task 1.3 çıktısı — 2026-07-29*
*Versiyon geçmişi:* v1 (taslak) → v2 (kanonik hibrit, 2026-05-04) → v3 (bu belge; 8-eksen hizalama + makro-tema atamaları + KARDES_KORUYUCU_ROLU + ADALET yazım düzeltmesi)
