# 03 Gereç ve Yöntem — Klinisyen Diline Uyarlama · ONAY TASLAĞI

Bu dosya **onay yüzeyidir**: teze (`chapters/03_gerec_ve_yontem.qmd`) **yazılmadan önce**
eski↔yeni metinler burada karşılaştırılır. Onayladığın alt-birimler teze Edit'lenir.

**Değişmez:** yalnız register/anlaşılırlık sadeleşir. Sayı · atıf `[@...]` · çapraz-ref (§, @tbl,
@fig) · hipotez (H1-H5) · kurum · tarih **DOKUNULMAZ** (`verify_authored_spans` ile mekanik
doğrulandı). Kısalt/böl + jargon glossu + Marmara-düz cümle; kaynak kapsamı/temkini korunur.

**Durum:** D1 dalgası **ONAYLANDI + UYGULANDI** → `.claude/worktrees/niteliksel-kol-rebuild/chapters/03_gerec_ve_yontem_new.qmd` (2026-07-29). İki minör kullanıcı düzeltmesiyle: G0 fiilimsiyle tek cümle; §3.1 ¶14 ilk cümle "iç içe geçmiş (hiyerarşik) özelliktedir" (tekrar giderildi). **Eski `chapters/03_gerec_ve_yontem.qmd` dokunulmadı.** DOKUNULMAZ grep-doğrulandı. Sıradaki: **D2 Evren ve Örneklem**.

> **İş modeli (kalıcı):** yeni içerik worktree `niteliksel-kol-rebuild`'de `chapters/{03,04,05}_..._new.qmd` dosyalarına yazılır; eski dosyalar değişmez. `_new.qmd` = tam bölüm kopyası, onaylı dalgalar özgün bölümleri sırayla değiştirir.

Onay biçimi: alt-birim bazında "uygun" / "şu değişsin". Onaylananlar teze işlenir, sonra D1 dalga
kapısı (`sci-audit:check-turkish` + `verify-citations` + `terim_tutarlilik_audit`).

---

## G0 · Bölüm girişi (satır 3–8)

**DOKUNULMAZ:** yok (atıf/sayı yok). **Değişim:** cümle bölme; anlam birebir.

**ESKİ:**
> Tip 1 diyabetin aile içindeki etkisini yalnız gruplar arası farklarla değil, aynı ailenin farklı üyelerinin deneyimiyle de görebilmek, tasarımın hem karşılaştırmalı hem de aile içi bir bakışı birlikte taşımasını gerektirir. Bu araştırma, T1DM tanılı çocuğu olan aileleri sağlıklı kontrol aileleriyle; ebeveynlik tutumu, anne depresif belirtileri ve kardeş ilişkileri ekseninde, hem gruplar arası karşılaştırma hem de aile içi deneyim düzeyinde karma yöntemle incelemektedir.

**YENİ:**
> Tip 1 diyabetin aile içindeki etkisi yalnız gruplar arası farklarla değil, aynı ailenin farklı üyelerinin deneyimiyle de görülebilir. Bu nedenle araştırma tasarımı hem karşılaştırmalı hem de aile içi bir bakışı birlikte taşır. Bu araştırma, T1DM tanılı çocuğu olan aileleri sağlıklı kontrol aileleriyle ebeveynlik tutumu, anne depresif belirtileri ve kardeş ilişkileri ekseninde karma yöntemle incelemektedir; karşılaştırma hem gruplar arası hem de aile içi deneyim düzeyinde yapılmıştır.

---

## §3.1 Araştırma Tasarımı — ¶12 (satır 12)

**DOKUNULMAZ (doğrulandı):** `[@creswellPlanoClark2018]` · `§3.9` · `(T1DM)`. **Değişim:** tek
~180 kelimelik cümle → kısa düz cümleler; eğilim skoru glossu yedirildi.

**ESKİ:**
> Araştırma, eşzamanlı (yakınsak; *convergent*) karma yöntem tasarımıyla planlanmıştır [@creswellPlanoClark2018]; baskın nicel bir desene nitel bileşenin iç içe (*embedded*) yerleştiği bu tasarımda her iki kolun verisi aynı saha döneminde toplanmış, bütünleştirme ise yorum aşamasında yapılmıştır. Baskın nicel bileşen, aile-kümeli (her ailede bir indeks çocuk ve bir sağlıklı kardeş) bir olgu–kontrol kesitsel anket çalışmasıdır. Kontrol grubu, indeks çocukların yaş ve cinsiyet dağılımı bakımından karşılaştırılabilir ailelerden ardışık örneklemeyle oluşturulmuş; birebir/oranlı bir vaka-kontrol eşleştirme algoritması uygulanmamış, gruplar arası denge çözümleme aşamasında eğilim skoru temelli ağırlıklandırma ve kovaryat ayarlamasıyla sağlanmıştır (bkz. §3.9). Buna iç içe yerleşen tamamlayıcı nitel bileşen, aynı klinik bağlamdan seçilen bir alt örneklemle yürütülen bireysel yarı yapılandırılmış görüşmelere dayanır. Nicel kolun önceliği, önceden belirlenmiş beş hipotezin sınanması; nitel kolun işlevi ise bu örüntülerin anne, Tip 1 diyabet (T1DM) tanılı çocuk ve sağlıklı kardeş deneyimleri üzerinden bağlamsallaştırılmasıdır. Karma bütünleştirmede nitel bulgular nicel sonuçları doğrulayan ikincil kanıt olarak değil, ölçeklerin yakalayamayabileceği role dayalı deneyim katmanlarını açıklayan tamamlayıcı bir kanıt türü olarak konumlandırılmıştır.

**YENİ:**
> Araştırma, eşzamanlı karma yöntem (yakınsak; *convergent*) tasarımıyla planlanmıştır [@creswellPlanoClark2018]. Bu tasarımda baskın olan nicel desendir; nitel bileşen bu desenin içine yerleştirilmiştir (*embedded*). Her iki kolun verisi aynı saha döneminde toplanmış, bütünleştirme yorum aşamasında yapılmıştır. Baskın nicel bileşen, aile-kümeli bir olgu–kontrol kesitsel anket çalışmasıdır; her ailede bir indeks çocuk ve bir sağlıklı kardeş yer alır. Kontrol grubu, indeks çocukların yaş ve cinsiyet dağılımı bakımından karşılaştırılabilir ailelerden ardışık örneklemeyle oluşturulmuştur. Birebir eşleştirme algoritması uygulanmamış; gruplar arası denge, çözümleme aşamasında eğilim skoru temelli ağırlıklandırma (bir ailenin ilgili gruba düşme olasılığına göre ağırlık verme) ve kovaryat ayarlamasıyla sağlanmıştır (bkz. §3.9). Nitel bileşen, aynı klinik bağlamdan seçilen bir alt örneklemle yürütülen bireysel yarı yapılandırılmış görüşmelere dayanır. Nicel kolun önceliği, önceden belirlenmiş beş hipotezin sınanmasıdır; nitel kolun işlevi ise bu örüntüleri anne, Tip 1 diyabet (T1DM) tanılı çocuk ve sağlıklı kardeş deneyimleri üzerinden bağlamsallaştırmaktır. Nitel bulgular, nicel sonuçları doğrulayan ikincil kanıt olarak değil; ölçeklerin yakalayamayabileceği role dayalı deneyim katmanlarını açıklayan tamamlayıcı bir kanıt türü olarak konumlandırılmıştır.

---

## §3.1 Araştırma Tasarımı — ¶14 (satır 14)

**DOKUNULMAZ (doğrulandı):** `[@deLosReyes2015; @ferro2022informantAgreement]` · `ICC`.
**Değişim:** tek uzun cümle → 6 kısa cümle; ICC ("aile içi benzerlik") glossu yedirildi.

**ESKİ:**
> Çalışmanın veri yapısı iç içe hiyerarşiktir. Her aile, bir indeks çocuk, bir kardeş ve ortak anne bildirimini içerir; aynı aileye ait çocuk satırları aile düzeyi değişkenleri paylaştığından klasik gözlem bağımsızlığı varsayımı karşılanmaz. Bu nedenle çıkarımsal çözümlemeler aile içi korelasyonu (sınıf-içi korelasyon katsayısı, ICC) hesaba katan çok düzeyli (*multilevel*) modeller ya da aile bazında kümelenmiş standart hatalar üzerinden yürütülmüştür. Aynı ebeveynlik davranışının farklı aile üyelerince farklı konumlardan raporlanabilmesi nedeniyle çalışma, çoklu bilgi kaynağı (*multi-informant*) yaklaşımını benimsemiştir; bu yaklaşımda bilgi verenler arasındaki düşük ya da orta düzeydeki örtüşme yalnız ölçüm hatası değil, bağlama ve role özgü geçerli bilgi olarak da değerlendirilir [@deLosReyes2015; @ferro2022informantAgreement].

**YENİ:**
> Çalışmanın veri yapısı iç içe (hiyerarşik) bir yapıdadır. Her aile bir indeks çocuğu, bir kardeşi ve ortak anne bildirimini içerir. Aynı aileye ait çocuk satırları aile düzeyi değişkenleri paylaştığından, gözlemlerin bağımsızlığı varsayımı karşılanmaz. Bu nedenle çıkarımsal çözümlemeler, aile içi benzerliği (sınıf-içi korelasyon; ICC) hesaba katan çok düzeyli (*multilevel*) modellerle ya da aile bazında kümelenmiş standart hatalarla yürütülmüştür. Aynı ebeveynlik davranışı farklı aile üyelerince farklı konumlardan raporlanabildiğinden, çalışma çoklu bilgi kaynağı (*multi-informant*) yaklaşımını benimsemiştir. Bu yaklaşımda bilgi verenler arasındaki düşük veya orta düzeyde örtüşme, yalnız ölçüm hatası değil; bağlama ve role özgü geçerli bilgi olarak da değerlendirilir [@deLosReyes2015; @ferro2022informantAgreement].

---

## §3.1 Araştırma Tasarımı — ¶16 (satır 16, raporlama çerçeveleri)

**DOKUNULMAZ (doğrulandı):** 7 çerçeve atfı — `[@vandenbroucke2007strobe]` `[@appelbaum2018jarsQuant]`
`[@collins2015tripod]` `[@tong2007coreq]` `[@obrien2014srqr]` `[@levitt2018jarsQual]`
`[@ocathain2008gramms]`. **Değişim:** tek dev cümle → 3 cümle (nicel / nitel / karma).

**ESKİ:**
> Nicel kolun raporlanmasında olgu–kontrol çalışmaları için STROBE [@vandenbroucke2007strobe], nicel psikolojik araştırma için JARS-Quant [@appelbaum2018jarsQuant] ve öngörü/risk modelleri için TRIPOD [@collins2015tripod] çerçeveleri; nitel kolun raporlanmasında COREQ [@tong2007coreq], SRQR [@obrien2014srqr] ve JARS-Qual [@levitt2018jarsQual] çerçeveleri; karma bütünleştirmenin raporlanmasında ise GRAMMS [@ocathain2008gramms] çerçevesi esas alınmıştır.

**YENİ:**
> Nicel kolun raporlanmasında olgu–kontrol çalışmaları için STROBE [@vandenbroucke2007strobe], nicel psikolojik araştırma için JARS-Quant [@appelbaum2018jarsQuant] ve öngörü/risk modelleri için TRIPOD [@collins2015tripod] çerçeveleri esas alınmıştır. Nitel kolun raporlanmasında COREQ [@tong2007coreq], SRQR [@obrien2014srqr] ve JARS-Qual [@levitt2018jarsQual] çerçeveleri kullanılmıştır. Karma bütünleştirmenin raporlanmasında ise GRAMMS [@ocathain2008gramms] çerçevesi esas alınmıştır.

---

## §3.2 Araştırma Soruları ve Hipotezler — ¶20 (satır 20)

**DOKUNULMAZ (doğrulandı):** H1–H5 ifadeleri **birebir**. **Değişim:** temel soru düz bildirim
korundu; beş hipotez **madde-listesine** alındı (pedagojik yeniden sıralama — küme/yön/ifade
değişmez, yalnız okunabilirlik). ⚠️ *yeniden sıralama* → ayrı onay maddesi.

**ESKİ:**
> Araştırmanın temel sorusu, T1DM tanılı çocuğu olan ailelerde ebeveynlik tutumu, anne depresif belirtileri ve kardeş ilişkilerinin sağlıklı kontrol ailelerine göre nasıl örüntülendiği ve bu örüntülerin anne, hasta çocuk ve sağlıklı kardeş bakış açıları arasında nasıl ayrıştığıdır. Bu soru doğrultusunda beş doğrulayıcı hipotez önceden belirlenmiştir: T1DM tanılı çocuklar ile sağlıklı kardeşlerinin algıladığı ebeveynlik tutumları kontrol grubundan farklılaşmaktadır (H1); kardeş ilişkisi sıcaklık/yakınlık, statü/güç, çatışma ve rekabet boyutlarında gruplar arasında farklılaşmaktadır (H2); annelerin öz-bildirdiği ebeveynlik tutumları gruplar arasında farklılaşmaktadır (H3); anne depresif belirti düzeyi ebeveynlik tutumu boyutlarıyla ilişkilidir (H4); ve anne öz-bildirimi ile çocuk algısı arasındaki diadik tutarlılık düşük düzeydedir (H5). Bu hipotezlere ilişkin çözümleme modelleri İstatistiksel Analiz başlığında tanımlanmış; nitel bölüm ise bu örüntüleri anne, hasta çocuk ve sağlıklı kardeş deneyimleri üzerinden bağlamsallaştırmayı amaçlamıştır.

**YENİ:**
> Araştırmanın temel sorusu, T1DM tanılı çocuğu olan ailelerde ebeveynlik tutumu, anne depresif belirtileri ve kardeş ilişkilerinin sağlıklı kontrol ailelerine göre nasıl örüntülendiği ve bu örüntülerin anne, hasta çocuk ve sağlıklı kardeş bakış açıları arasında nasıl ayrıştığıdır. Bu soru doğrultusunda önceden beş doğrulayıcı hipotez belirlenmiştir:
>
> - T1DM tanılı çocuklar ile sağlıklı kardeşlerinin algıladığı ebeveynlik tutumları kontrol grubundan farklılaşmaktadır (H1).
> - Kardeş ilişkisi sıcaklık/yakınlık, statü/güç, çatışma ve rekabet boyutlarında gruplar arasında farklılaşmaktadır (H2).
> - Annelerin öz-bildirdiği ebeveynlik tutumları gruplar arasında farklılaşmaktadır (H3).
> - Anne depresif belirti düzeyi ebeveynlik tutumu boyutlarıyla ilişkilidir (H4).
> - Anne öz-bildirimi ile çocuk algısı arasındaki diadik tutarlılık düşük düzeydedir (H5).
>
> Bu hipotezlere ilişkin çözümleme modelleri İstatistiksel Analiz başlığında tanımlanmıştır. Nitel bölüm ise bu örüntüleri anne, hasta çocuk ve sağlıklı kardeş deneyimleri üzerinden bağlamsallaştırmayı amaçlamıştır.

---

## §3.3 Çalışmanın Yeri ve Tarihi — ¶24 (satır 24)

**DOKUNULMAZ (doğrulandı):** kurumlar (Marmara Ü. EAH; İstanbul Medeniyet Ü. Göztepe SYŞH; Çocuk
Endokrinoloji ve Diyabet Bilim Dalı) + tarihler (Şubat 2023, Aralık 2025) **birebir**.
**Değişim:** çok hafif — uzun cümleler noktayla ayrıldı; zaten klinisyen-okur dostu.

**ESKİ:**
> Çalışma çok merkezli olarak iki kurumda yürütülmüştür. Birincil koordinasyon merkezi T.C. Sağlık Bakanlığı Marmara Üniversitesi Eğitim ve Araştırma Hastanesi'dir; hasta grubu Çocuk Endokrinoloji ve Diyabet Bilim Dalı'ndan, sağlıklı kontrol grubu ise aynı kurumun Hasta Çocuk Kliniği–Genel Pediatri polikliniğinden alınmıştır. İkinci merkez, İstanbul Medeniyet Üniversitesi Göztepe Süleyman Yalçın Şehir Hastanesi Çocuk Endokrinoloji Polikliniği'dir ve yalnız hasta grubu alımına katkı vermiştir. Saha süreci Şubat 2023'te hasta alımıyla başlamış ve Aralık 2025'te tamamlanmıştır; verilerin çözümlenmesi bunu izleyen dönemde yürütülmüştür. Anket uygulamaları ve nitel görüşmeler poliklinik ortamında gerçekleştirilmiştir.

**YENİ:**
> Çalışma çok merkezli olarak iki kurumda yürütülmüştür. Birincil koordinasyon merkezi T.C. Sağlık Bakanlığı Marmara Üniversitesi Eğitim ve Araştırma Hastanesi'dir. Hasta grubu bu kurumun Çocuk Endokrinoloji ve Diyabet Bilim Dalı'ndan, sağlıklı kontrol grubu ise aynı kurumun Hasta Çocuk Kliniği–Genel Pediatri polikliniğinden alınmıştır. İkinci merkez İstanbul Medeniyet Üniversitesi Göztepe Süleyman Yalçın Şehir Hastanesi Çocuk Endokrinoloji Polikliniği'dir; bu merkez yalnız hasta grubu alımına katkı vermiştir. Saha süreci Şubat 2023'te hasta alımıyla başlamış, Aralık 2025'te tamamlanmıştır; verilerin çözümlenmesi bunu izleyen dönemde yürütülmüştür. Anket uygulamaları ve nitel görüşmeler poliklinik ortamında gerçekleştirilmiştir.

---

## Onay kutusu (kullanıcı doldurur)

- [x] G0 Bölüm girişi — onaylı (fiilimsi düzeltmesiyle) · uygulandı
- [x] §3.1 ¶12 Araştırma Tasarımı — onaylı · uygulandı
- [x] §3.1 ¶14 veri yapısı / ICC — onaylı (tekrar giderme) · uygulandı
- [x] §3.1 ¶16 raporlama çerçeveleri — onaylı · uygulandı
- [x] §3.2 ¶20 Hipotezler — onaylı (madde-listesi yeniden sıralaması **onaylandı**) · uygulandı
- [x] §3.3 ¶24 Yer/Tarih — onaylı · uygulandı

Tümü `03_gerec_ve_yontem_new.qmd`'ye işlendi. Sıradaki dalga: **D2 Evren ve Örneklem**
(§Evren ve Örneklem + dahil/dışlama · güç analizi · örnekleme). Dalga kapısı (03 tamamlanınca):
`sci-audit:check-turkish` + `verify-citations` + `terim_tutarlilik_audit`.

---
---

# D2 · Evren ve Örneklem — ONAY BEKLİYOR

**Durum:** 7 alt-birim Claude-authored yazıldı. **Mekanik DOKUNULMAZ:** `verify_authored_spans`
7/7 PASS (45 span). **Adversaryal doğrulama (4 mercek workflow):** DOKUNULMAZ-tamlık ✅ ·
overclaim ✅ · sadakat: ¶40 "Monte Carlo" geri kondu · register: ¶34 gerçek madde-listesi. Teze
YAZILMADI. Sayı (241/482/120/121/240/242, 7–17, α=0,05, %80, d=0,5–0,8/0,8/0,5, ~25/~64/30/~120/~240/39,
OpenEpi 3.01) · atıf (6) · @fig-strobe-flow · ölçütler **DOKUNULMAZ**.

## §3.4 Evren ve Örneklem — ¶28
**ESKİ:** Araştırmanın evrenini, tanımlanan iki merkezde izlenen 7–17 yaş aralığındaki T1DM tanılı çocuklar ile aynı kurumlara başvuran, kronik hastalığı olmayan sağlıklı kontrol çocukları ve bu çocukların 7–17 yaş aralığındaki sağlıklı kardeşleri ve anneleri oluşturmuştur. Örneklem birimi ailedir: her aileden bir indeks çocuk, aynı ailenin bir sağlıklı kardeşi ve ortak bir anne çalışmaya alınmıştır.
**YENİ:** Araştırmanın evrenini üç grup oluşturmuştur: tanımlanan iki merkezde izlenen 7–17 yaş aralığındaki T1DM tanılı çocuklar; aynı kurumlara başvuran, kronik hastalığı olmayan sağlıklı kontrol çocukları; ve bu çocukların 7–17 yaş aralığındaki sağlıklı kardeşleri ile anneleri. Örneklem birimi ailedir; her aileden bir indeks çocuk, aynı ailenin bir sağlıklı kardeşi ve ortak bir anne çalışmaya alınmıştır.
**Değişim:** üç grup iki noktalı yapıyla ayrıldı; anlam birebir.

## §3.4 ¶30 Rol dağılımı
**Değişim:** hafif — uzun cümleler noktayla ayrıldı. **Tüm sayılar + `@vandenbroucke2007strobe` + `@fig-strobe-flow` + "DM klinik alt-analiz" birebir.**
**YENİ:** Çocuk-satırı düzeyinde her katılımcı dört rol etiketinden biriyle temsil edilmiştir: T1DM tanılı indeks çocuk, T1DM tanılı çocuğun sağlıklı kardeşi, sağlıklı kontrol indeks çocuğu ve sağlıklı kontrol çocuğunun sağlıklı kardeşi. Anne bildirimi ailenin indeks satırına gömülüdür. Final referans veri seti aile düzeyinde 241 aile, çocuk-satırı düzeyinde 482 çocuk gözlemi içermektedir. Rol dağılımı 120 T1DM tanılı indeks çocuk, 120 T1DM tanılı çocuğun sağlıklı kardeşi, 121 sağlıklı kontrol indeks çocuğu ve 121 sağlıklı kontrol kardeşi biçimindedir; böylece grup düzeyinde 240 T1DM ve 242 kontrol çocuk gözlemi elde edilmiştir. Kilitlenmiş kanonik veri tabanından aile düzeyi analiz tabanına, gruplara ve DM klinik alt-analiz katmanına geçişi özetleyen katılımcı akışı, epidemiyolojik raporlama kılavuzlarının önerdiği akış şeması biçiminde [@vandenbroucke2007strobe] bulgular bölümündeki @fig-strobe-flow içinde gösterilmiştir.

## §3.4.1 Dahil edilme ve dışlanma ölçütleri — ¶34
**Değişim:** dahil ölçütleri **madde-listesine** alındı (⚠️ yeniden sıralama — okunabilirlik; ölçüt kümesi/anlam sabit); dışlanma ölçütleri düz cümlede kaldı. "yalnızca iki ailede anne boşanmıştır" + "tanı yaşı klinik olarak olası aralıktadır" birebir.
**YENİ:**
> T1DM grubu için dahil edilme ölçütleri şunlardır:
>
> - Tip 1 diyabet tanısı almış olmak;
> - 7–17 yaş aralığında bulunmak;
> - aynı yaş aralığında en az bir sağlıklı kardeşe sahip olmak;
> - her iki ebeveynin hayatta olması;
> - soruları anlayıp yanıtlayabilecek düzeyde Türkçe biliyor olmak.
>
> Sağlıklı kontrol grubunda bu ölçütlere ek olarak çocuğun ve kardeşinin herhangi bir kronik hastalığının bulunmaması aranmıştır. Anneler için birincil bakım verenlerden biri olmak ve çocuklarıyla birlikte yaşamak koşulu getirilmiştir. Dışlanma nedenleri; T1DM dışında kronik hastalık veya engellilik bulunması, kardeşte kronik sağlık sorunu bulunması ve anne ya da babada engellilik bulunmasıdır. Katılımdan çekilme talebi, tutarsız yanıt örüntüsü ya da araştırmacı kararıyla çıkarılma durumlarında ilgili gönüllünün verileri çözümlemeye alınmamıştır. Çözümlemeye alınan tüm ailelerde her iki ebeveyn hayattadır ve annelerin büyük çoğunluğu evlidir; yalnızca iki ailede anne boşanmıştır. Tüm T1DM olgularının tanı yaşı klinik olarak olası aralıktadır.

## §3.4.2 Örneklem büyüklüğü ve güç analizi — ¶38 (a priori)
**Değişim:** tek dev cümle bölündü; "a priori" için gloss ("veriyi toplamadan önce planlanan gerekli katılımcı sayısı"); tüm sayı/atıf/OpenEpi + "sınırda kabul edilmelidir" çekincesi birebir.
**YENİ:** Nicel kol için birincil (*a priori*) örneklem büyüklüğü — yani veriyi toplamadan önce planlanan gerekli katılımcı sayısı — EMBU ve Kardeş İlişkileri Anketi alt ölçeklerinin her biri için hesaplanmıştır. Hesap, çift yönlü α = 0,05, %80 güç ve iki bağımsız grup ortalama karşılaştırması çerçevesinde [@cohen1988power] açık kaynaklı OpenEpi (sürüm 3.01) yazılımıyla yapılmıştır [@openepi2013]. Beklenen etki büyüklüğü (orta ilâ büyük düzey; yaklaşık d = 0,5–0,8) ve grup varyansları, ebeveynlik tutumu ve kardeş ilişkisi alanındaki önceki Türkçe çalışmalardan alınmıştır. Bu varsayımlarla grup başına asgari örneklem, büyük etki (d = 0,8) için yaklaşık 25, orta etki (d = 0,5) için yaklaşık 64 bireydir. Alt ölçek puanlarındaki değişkenliği karşılamak için grup başına en az 30 bireylik bir taban benimsenmiştir. Ulaşılan final örneklem grup başına yaklaşık 120 aileyle, orta-etki (d = 0,5) gereksiniminin belirgin biçimde üzerindedir ve etik kurulun öngördüğü asgari sayıyı aşmaktadır. Bu hesap iki grup ortalama farkı içindir; çok maddeli yapısal eşitlik (WLSMV), diadik doğrulayıcı faktör ve çok düzeyli modeller için ayrı bir a priori güç simülasyonu yürütülmediğinden, örneklem bu daha karmaşık modeller açısından sınırda kabul edilmelidir.

## §3.4.2 ¶40 Karmaşık modeller için güç gerekçesi
**Değişim:** cümleler bölündü; **¶40 sadakat düzeltmesi: "Monte Carlo" geri kondu**; tüm atıf + `simr`/`pwr` + TOST + "yalnız bağlamsal/keşifsel" çekincesi birebir.
**YENİ:** Bu birincil güç hesabı iki grup ortalama farkı içindir; çalışmanın çok düzeyli (aile içi yuvalanma), yapısal eşitlik (H4) ve aktör–partner (H2/H5 diadik) modellerinin örneklem gereksinimini doğrudan yansıtmaz. Bu karmaşık modeller için ayrı bir a priori güç hesabı yerine, tasarıma dayalı iki dayanak esas alınmıştır. Birincisi, çok düzeyli ve diadik modellerde asıl belirleyici toplam birey sayısından çok küme (aile) sayısıdır; yaklaşık 240 aileyle sağlanan küme sayısı, çok düzeyli modeller için önerilen kaba alt sınırların üzerindedir [@maas2005sufficient]. İkincisi, tek bir etki için gözlenen (retrospektif) güç hesaplamak yerine — gözlenen güç p değerinin birebir dönüşümü olduğundan ek bilgi taşımaz [@hoenigHeisey2001abusePower] — sonuçların belirsizliği doğrudan etki büyüklüğü güven aralıkları, Bayesçi güvenilir aralıklar ve eşdeğerlik (TOST) sınırlarıyla raporlanmıştır. Yapısal eşitlik ve çok düzeyli modeller için gerektiğinde `simr` ve `pwr` paketleriyle Monte Carlo/simülasyon temelli hassasiyet çözümlemesi tamamlayıcı olarak değerlendirilmiştir [@green2016simr]. DM'ye özgü klinik zamanlama değişkenleri doğrulayıcı hipotez kararlarını genişletmez; yalnız bağlamsal/keşifsel düzeyde okunur.

## §3.4.2 ¶42 Nitel örneklem (bilgi gücü)
**YENİ:** Nitel kolun örneklem büyüklüğü ise sayısal güç yerine bilgi gücü çerçevesiyle gerekçelendirilmiştir; ilgili değerlendirme nitel kolun kendi alt başlığında sunulmuştur.

## §3.4.3 Örnekleme yöntemi — ¶46
**YENİ:** Nicel kolda katılımcılar ardışık örneklemeyle alınmıştır: dahil edilme ölçütlerini karşılayan ve polikliniğe başvuran tüm ailelere katılım daveti yapılmıştır. Kontrol grubu, indeks çocukların yaş ve cinsiyet dağılımı bakımından karşılaştırılabilir sağlıklı çocuklar ve aileleri arasından oluşturulmuştur. Nitel alt örneklem ise ardışık/olasılıklı seçim yerine amaçlı örneklemeyle (*purposive sampling*) oluşturulmuş; bu örneklemin oluşturulması ve katılım süreci nitel kolun ilgili alt başlığında ayrıntılandırılmıştır.

## D2 Onay kutusu — TÜMÜ ONAYLANDI + UYGULANDI (2026-07-29, revizyonsuz)
- [x] ¶28 Evren
- [x] ¶30 Rol dağılımı
- [x] ¶34 Dahil/dışlanma (+ madde-listesi yeniden sıralaması onaylandı)
- [x] ¶38 a priori güç
- [x] ¶40 karmaşık-model güç (Monte Carlo geri kondu)
- [x] ¶42 nitel bilgi gücü
- [x] ¶46 Örnekleme yöntemi

Tümü `03_gerec_ve_yontem_new.qmd`'ye işlendi; DOKUNULMAZ grep-teyit; ana dosya temiz.

---
---

# D3 · Değişkenler + Veri Toplama Araçları — ONAY BEKLİYOR

**Durum:** 10 alt-birim Claude-authored. **Mekanik DOKUNULMAZ:** `verify_authored_spans` 7/7 PASS
(43 span). **Adversaryal doğrulama (4 mercek):** DOKUNULMAZ-tamlık ✅ · register ✅ · overclaim:
3 "eklenen gerekçe" bulgusu **kaynağa karşı FALSE POSITIVE** (üç cümle de `chapters/03`'te birebir
var — grep-teyit; sadeleştirmede eklenmedi) · sadakat: **¶85 "klinik ayırt etme çalışmasında"
geri kondu** (≥17 kesme puanının klinik-doğrulama provenansı). q25 tablosu (@tbl-q25-yon)
**dokunulmadı**. Teze YAZILMADI.

## §3.5 Değişkenler ve Tanımları — ¶50 · ¶52 · ¶54
**¶50 (değişkenler):** değişiklik minimal (zaten liste-benzeri, net); "365,25" + "(T1DM/kontrol)" birebir.
**¶54 (T1DM klinik):** değişiklik yok (zaten klinisyen-dostu); "120 T1DM indeks çocuğun 39'unda" + "*structural missing*" birebir.

**¶52 SES — ESKİ:** …Maddi varlık indeksi polikorik (*polychoric*) temel bileşen analiziyle, şeffaflık amaçlı duyarlılık değişkenleri eş-ağırlıklı ve Hollingshead tipi kompozitlerle [@hollingshead1975], birincil sosyoekonomik kovaryat ise doğrulayıcı faktör analizine dayalı latent skorla temsil edilmiştir.
**¶52 SES — YENİ:** Sosyoekonomik durum; eğitim ve mesleğe dayalı uluslararası sosyoekonomik indeks (*International Socio-Economic Index*, ISEI) [@ganzeboomTreiman1996isei] ile maddi varlık göstergelerini birlikte kullanan üç katmanlı bir kompozit hattıyla üretilmiştir. Maddi varlık indeksi, sıralı değişkenlere uygun bir temel bileşen analiziyle (polikorik) hesaplanmıştır. Şeffaflık amaçlı duyarlılık değişkenleri eş-ağırlıklı ve Hollingshead tipi kompozitlerle üretilmiş [@hollingshead1975]; birincil sosyoekonomik kovaryat ise doğrulayıcı faktör analizine dayalı bir latent skorla temsil edilmiştir.
*(Değişim: tek cümle 3 cümleye bölündü; "polikorik" için gloss. ISEI/Hollingshead/latent/polikorik birebir.)*

## §3.6.2 s-EMBU-C — ¶66 (en yoğun; tek dev paragraf → 3 paragraf)
**Değişim:** tek ~350 kelimelik paragraf **3 paragrafa** bölündü (tanım+yapı / köken+genişleme / q25+uygulama); "içerirken…genişlemektedir" iki cümleye ayrıldı. **Tüm madde sayıları (29, 23, 24, 24+5=29, 9/7/8/5), 5 atıf, `q25`, @tbl-q25-yon birebir.** q25 tablosu dokunulmadı.
**YENİ (özet ilk paragraf):** Çocuğun algıladığı anne tutumunu ölçen s-EMBU-C, kısaltılmış EMBU'nun çocuk-bildirim formudur [@arrindell2005sembu; @castro1993embuChildren]. … Ölçek 29 maddeden oluşur ve dörtlü Likert biçiminde (1 = en düşük sıklık; 4 = en yüksek sıklık) yanıtlanır… Ölçek dört alt ölçek sunar: Duygusal Sıcaklık (9 madde), Aşırı Koruma (7 madde), Reddetme (8 madde) ve Karşılaştırma (5 madde). *(Tam metin `03_new.qmd`'de.)*

## §3.6.3 s-EMBU-P — ¶77
**YENİ:** Annenin kendi ebeveynlik tutumunu öz-bildirimle değerlendiren s-EMBU-P, çocuk formuyla aynı madde sırasını ve dörtlü Likert biçimini paylaşan 29 maddelik ebeveyn-bildirim formudur ve aynı dört alt ölçeği (Duygusal Sıcaklık, Aşırı Koruma, Reddetme, Karşılaştırma) üretir [@arrindell2005sembu]. Form aile/indeks düzeyinde, anketi getiren indeks çocuk hedef alınarak yanıtlanmıştır. Ebeveyn ve çocuk formlarının madde düzeyinde eşlenik yapısı, anne öz-bildirimi ile çocuk algısı arasındaki diadik (anne ↔ çocuk) tutarlılık çözümlemesini doğrudan olanaklı kılar. Ebeveyn formu da çocuk formuyla eşlenik dört alt ölçekli yapısıyla bu örneklemde ayrı bir çalışma-içi psikometrik değerlendirmeye tabi tutulmuştur (bkz. Ölçme Araçlarının Psikometrik Değerlendirmesi).

## §3.6.4 Kardeş İlişkileri Anketi — ¶81
**Değişim:** noktalı virgül → ayrı cümle. **Furman ve Buhrmester (1985), Apalaçi (1996), 3 atıf, 48 madde, beşli Likert, 4 boyut birebir.**
**YENİ:** Kardeş ilişkisinin niteliğini çocuğun bakış açısından değerlendiren Kardeş İlişkileri Anketi, özgün olarak Furman ve Buhrmester (1985) tarafından geliştirilmiştir [@furmanBuhrmester1985srq]. Ölçeğin Türkçeye uyarlaması Apalaçi (1996) tarafından yapılmış ve çalışmada bu Türkçe uyarlama kullanılmıştır [@apalaci1996yoktez]. Türkçe kardeş ilişkileri ölçümüne ilişkin ek/karşılaştırmalı bir kaynak için ayrıca bkz. [@aktas2017kardesIliskileriOlcegi]. Ölçek 48 maddeden oluşur ve beşli Likert biçiminde (1 = hemen hemen hiç; 5 = çok çok fazla) yanıtlanır; anketi hem indeks hem kardeş çocuk kendi bakış açısından doldurmuştur. Ölçek dört üst düzey boyut sunar: Sıcaklık/Yakınlık, Statü/Güç, Çatışma ve Rekabet. Ebeveyn karşılaştırmasını göreli yönde soran maddeler, puanlamada bu yön dikkate alınarak işlenmiştir.

## §3.6.5 Beck Depresyon Envanteri — ¶85 (¶85 provenans düzeltmesiyle)
**Değişim:** cümleler bölündü; **"klinik ayırt etme çalışmasında" ibaresi geri kondu** (adversaryal doğrulama bulgusu); 21/0–3/0–63/≥17, 2 atıf, "sürekli"/"ikili gösterge", "klinik tanı taşımaz"/"keşifsel" birebir.
**YENİ:** Annenin son bir haftadaki depresif belirti düzeyini ölçen Beck Depresyon Envanteri, Türkçe geçerlik ve güvenirlik çalışması temel alınarak uygulanmıştır [@hisli1989bdiTurkishUniversity]. Envanter 21 maddeden oluşur; her madde 0–3 arası puanlanır ve toplam puan 0–63 aralığındadır. Toplam puan tüm maddeler yanıtlandığında hesaplanmış, herhangi bir madde eksik olduğunda toplam puan eksik bırakılmıştır. Çözümlemelerde Beck toplam puanı öncelikle **sürekli** değişken olarak kullanılmıştır. Ayrık şiddet bantları (ör. minimal/hafif/orta/şiddetli), Türkçe literatürde tek bir yerleşik eşik kümesine dayanmadığından ve mevcut geçerlik kanıtı anne örneklemine doğrudan aktarılamadığından raporlanmamıştır. Yalnız keşifsel klinik-fayda çözümlemelerinde, Hisli'nin psikiyatri polikliniği örneklemindeki klinik ayırt etme çalışmasında kullanılan Beck toplam ≥ 17 kesme puanı [@hisli1988bdiClinical] operasyonel bir **ikili gösterge** olarak alınmıştır; bu gösterge klinik tanı veya ileriye dönük risk anlamı taşımaz, yalnız güncel depresif belirti yükünün görece yüksek olduğu grubu betimsel olarak işaretler ve keşifsel yorumlanır.

## §3.6 / ¶58 · ¶62 · ¶87 (hafif dokunuş / değişiklik minimal)
Veri Toplama girişi (telif notu), demografik-form alan dökümü ve nitel görüşme-rehberi çapraz-referansı: hafif dokunuş; içerik/atıf birebir.

## D3 Onay kutusu — TÜMÜ ONAYLANDI + UYGULANDI (2026-07-29, revizyonsuz)
- [x] ¶50 Değişkenler · ¶54 T1DM klinik (minimal/değişiklik yok)
- [x] ¶52 SES kompoziti (polikorik glossu)
- [x] ¶66 s-EMBU-C (3-paragraf bölme; q25 tablosu dokunulmadı)
- [x] ¶77 s-EMBU-P
- [x] ¶81 Kardeş İlişkileri Anketi
- [x] ¶85 Beck (klinik ayırt etme provenansı korundu)
- [x] ¶58 · ¶62 · ¶87 (hafif)

Tümü `03_gerec_ve_yontem_new.qmd`'ye işlendi; DOKUNULMAZ + q25 tablosu grep-teyit; ana dosya temiz.

---
---

# D4 · Ölçme Araçlarının Psikometrik Değerlendirmesi — ONAY BEKLİYOR

**Durum:** 7 alt-birim Claude-authored (en jargon-yoğun dalga). **Mekanik DOKUNULMAZ:**
`verify_authored_spans` 7/7 PASS (47 span). **Adversaryal doğrulama (4 mercek workflow):**
**dördü de TEMİZ** (sadakat/RBŞ ✅ · overclaim ✅ · Marmara register ✅ · DOKUNULMAZ-tamlık ✅ —
sıfır bulgu). **BSEM önsel notasyonu (λ_ana∼Normal(0,5; 0,5), Normal(0; 0,01), β∼Normal(0; 1))
metinde tutuldu** (DOKUNULMAZ; Ek'e taşıma-bağımlılığı yaratmamak için — istenirse Ek 7'ye
havale edilebilir). Tüm ~16 atıf + kısaltma + kod (`blavaan`/`targets`) + @sec-ek-psikometri
birebir. Tam ESKİ↔YENİ: `/tmp/kdu_03_d4_authored.md`. Teze YAZILMADI.

**Değişim örüntüsü:** tüm alt-birimlerde tek dev cümle-zincirleri kısa düz cümlelere bölündü;
noktalı-virgül zincirleri ayrıldı; jargon (KMO, WLSMV, bifaktör, BSEM, invariance, Fornell-Larcker,
Gwet AC1, TOST, MCAR) yerinde bırakıldı (klinik-karşılık sözlüğü + parantez-içi açılım). Sayı/
notasyon/atıf/yön (negatif/pozitif beklenen ilişki) değişmedi.

## §3.7 ¶91 giriş
**YENİ:** Kullanılan ebeveyn tutumu ölçeğinin, Karşılaştırma boyutu eklenmiş dört alt ölçekli sürümü Türkçe yazında daha önce de kullanılmıştır [@temelAltanAtalay2018selfCompassion]. Bu sürüm, eşlenik anne–çocuk formlarıyla birlikte bir çalışmada da uygulanmıştır [@caliskanSari2018embuC]. Bununla birlikte, sürümün birincil hipotez sınamalarına güçlü bir metodolojik omurga sağlaması amacıyla, çocuk ve ebeveyn formlarının faktör yapısı ve güvenirliği bu örneklemde ayrıca teyit edici bir çalışma-içi psikometrik değerlendirmeye tabi tutulmuştur. Bu tercih iki tasarım gerekçesine dayanır: (i) her iki form … dört faktörlü sürümde uygulanmıştır [@sumer2010anneBabaTutum]; (ii) ölçüm özelliklerinin … geçerliğini teyit etmek amaçlanmıştır. Bu değerlendirme hattı, güncel ölçüm-değerlendirme (COSMIN) ilkeleriyle uyumlu yürütülmüş ve ön-kayıt edilmiştir [@mokkink2018cosmin]. … ayrıntılı bulgular ise Ek 7'de (@sec-ek-psikometri) raporlanmaktadır.

## §3.7.1 ¶95 Madde düzeyi çözümleme ve güvenirlik
**YENİ:** Her alt ölçek için madde düzeyinde ortalama, standart sapma, çarpıklık, basıklık ile taban ve tavan etkisi oranları hesaplanmıştır. Sıralı verilerde çarpık dağılım ve taban/tavan yığılması, sonraki kestirim ve kategori kararlarını belirleyen ölçütler olarak kullanılmıştır. Güvenirlik yalnız Cronbach alfa katsayısıyla sınırlandırılmamıştır; tau-eşitliği varsayımına daha az bağımlı olan McDonald omega katsayıları, sıralı maddeler için polikorik korelasyon temelinde hesaplanmış ve önyükleme (*bootstrap*) temelli güven aralıklarıyla raporlanmıştır [@dunn2014alphaOmega; @trizanoHermosilla2016omegaAlpha]. Çocuk formunun aile içinde yuvalanmış yapısı nedeniyle güvenirlik ayrıca aile içi ve aile-arası bileşenlerine ayrıştırılarak incelenmiştir. Madde ayırt ediciliği, düzeltilmiş madde-toplam korelasyonları ve madde çıkarıldığında güvenirlikteki değişimle değerlendirilmiştir.

## §3.7.2 ¶99 Faktör yapısının sınanması
**YENİ:** Dört faktörlü yapının bu örneklemde geçerli olup olmadığı, doğrulayıcı analiz doğrudan dayatılmadan önce keşfedici faktör analiziyle taranmıştır. Bu tarama; faktörleştirilebilirlik (Kaiser–Meyer–Olkin [KMO] örneklem yeterliliği ve Bartlett küresellik ölçütleri), faktör sayısı (polikorik korelasyon matrisi üzerinde paralel çözümleme [@horn1965parallel] ve en küçük ortalama kısmi ölçütü) ve madde-faktör örüntüsünü kapsamıştır. Ardından, dört düzeyli sıralı maddelere uygun bir kestirimci olan ağırlıklı en küçük kareler ortalama-varyans düzeltmeli yöntemle (*Weighted Least Squares Mean and Variance adjusted*, WLSMV) doğrulayıcı faktör analizi yürütülmüştür [@li2016ordinalCFA]. Tek faktörlü, dört faktörlü, ikinci düzey ve bifaktör (bir genel + özgül faktörlü; *bifactor*) modeller birbirleriyle karşılaştırılmıştır. Kurulan faktör yapısının gözlenen veriyle ne kadar örtüştüğünü gösteren model uyumu; ki-kare istatistiğinin yanı sıra CFI, TLI, RMSEA (%90 güven aralığı ile) ve SRMR üzerinden yerleşik eşik ölçütleriyle değerlendirilmiştir. Bu indeksler yüksek uyumda CFI/TLI'nin 1'e, RMSEA ve SRMR'nin ise sıfıra yaklaşmasını bekler [@huBentler1999cutoff]. Çocuk formundaki aile içi bağımlılık; sınıf-içi korelasyonun hesaplanması ve aile numarasının kümeleme değişkeni alındığı çok düzeyli doğrulayıcı analizle ele alınmıştır.

## §3.7.3 ¶103 Bayesçi doğrulayıcı analiz (BSEM)
**Not:** önsel notasyonu metinde tutuldu; klinik gloss önde (kesin sıfıra sabitlemek yerine sıfıra yaklaştırma).
**YENİ:** Görece küçük örneklem koşullarında, çapraz yüklemeleri ve hata kovaryanslarını kesin sıfır sayan klasik doğrulayıcı analizin kısıtları göz önünde bulundurulmuştur. Bu koşullarda söz konusu ikincil parametreleri kesin sıfıra sabitlemek yerine, sıfır merkezli ve çok küçük varyanslı bilgi verici önsellerle "yaklaşık sıfıra" çeken Bayesçi yapısal eşitlik modeli (BSEM), bir *ön-uçuş* (preflight) planı olarak tanımlanmıştır [@muthenAsparouhov2012bsem]. Bu planda önsel sınıfları ayrıştırılmıştır: birincil (ana) faktör yükleri için görece geniş bir bilgi verici önsel (λ_ana ∼ Normal(0,5; 0,5)); çapraz yükler ve artık (hata) kovaryanslar için ise sıfır merkezli, dar varyanslı "yaklaşık sıfır" önselleri (ör. Normal(0; 0,01)) öngörülmüştür. Yapısal katsayılar için β ∼ Normal(0; 1); eşik ile latent varyans/ölçek parametreleri için `blavaan` varsayılan zayıf bilgi verici önselleri kullanılacak biçimde, model sözdizimi ve yakınsama ölçütleri analiz öncesinde sabitlenmiştir. Bu hat, yeniden üretilebilir varsayılan çözümleme hattının (`targets`) dışında yalnız isteğe bağlı bir psikometrik sağlamlık adımı olarak konumlandırılmıştır; bu nedenle H4 için doğrulayıcı olarak raporlanan çözüm WLSMV kestirimidir (bkz. Bulgular, §H4). BSEM örneklemesi yürütüldüğünde model uyumu sonsal öngörücü olasılık (*posterior predictive p*, PPP) değeriyle değerlendirilecek ve yakınsama tanı ölçütleriyle denetlenecek biçimde tasarlanmıştır.

## §3.7.4 ¶107 Ölçüm eşdeğerliği · §3.7.5 ¶111 Geçerlik/uyum · §3.7.6 ¶115 Taban/sağlamlık
**YENİ (¶107):** …üç eksende ölçüm eşdeğerliği (*measurement invariance*): tanı grubu (T1DM/kontrol), bilgi verici rolü (indeks çocuk/kardeş) ile yaş ve cinsiyet. Yapılandırmasal, metrik ve skalar düzeyler sırayla sınanmıştır. Düzeyler arası geçişler … CFI, RMSEA ve SRMR değişim ölçütleriyle de değerlendirilmiştir [@putnickBornstein2016measurementInvariance; @chen2007invariance]. … (skalar eşdeğerlik sağlanmazsa ölçüm-eşitsizliği vs gerçek algı ayrışması tam ayrıştırılamadığı çekincesi korundu.)
**YENİ (¶111):** Yakınsak ve ayırt edici geçerlik; ortalama açıklanan varyans, bileşik güvenirlik ve Fornell-Larcker ölçütü çerçevesinde [@fornellLarcker1981]. Beklenen ilişkiler (duygusal sıcaklık ile negatif; reddetme ve karşılaştırma ile pozitif) sınanmıştır. Raporcular arası uyum; sınıf-içi korelasyon, Bland-Altman uyum sınırları [@blandAltman1986] ve Gwet AC1 [@gwet2008ac1] ile değerlendirilmiştir.
**YENİ (¶115):** Taban etkisi çok evrenli (*multiverse*) çözümlemeyle ele alınmış; stratejiler paralel işletilip spesifikasyon eğrisiyle özetlenmiştir [@steegen2016multiverse]. "Fark yok" iddiası iki tek-yönlü test (*two one-sided tests*, TOST) ile değerlendirilmiştir [@lakens2017equivalence]. Eksik veri Little MCAR ile incelenmiştir [@little1988mcar].
*(Üçünde de cümle bölme; 3 eksen, tüm atıf ve çekinceler birebir. Tam metin `/tmp/kdu_03_d4_authored.md` ve uygulama sonrası `03_new.qmd`'de.)*

## D4 Onay kutusu — TÜMÜ ONAYLANDI + UYGULANDI (2026-07-30, revizyonsuz; 4-mercek TEMİZ)
- [x] ¶91 giriş (COSMIN / Ek 7)
- [x] ¶95 madde düzeyi + güvenirlik (α/ω/polikorik/bootstrap)
- [x] ¶99 faktör yapısı (KMO/Bartlett/paralel/WLSMV/bifaktör/CFI-TLI-RMSEA-SRMR)
- [x] ¶103 BSEM (önsel notasyonu **metinde tutuldu** — kullanıcı onayı)
- [x] ¶107 ölçüm eşdeğerliği
- [x] ¶111 geçerlik + raporcular arası uyum
- [x] ¶115 taban etkisi + sağlamlık (multiverse/TOST/MCAR)

Tümü `03_gerec_ve_yontem_new.qmd`'ye işlendi; DOKUNULMAZ (16 atıf + BSEM notasyonu + kısaltmalar) grep-teyit; ana dosya temiz. Sıradaki: **D5 Veri Toplama Süreci + İstatistiksel Analiz** (tanımlayıcı istatistikler + grup dengesi + eksik veri yönetimi).

---

# D5 — Veri Toplama Süreci ve Veri Yönetimi + İstatistiksel Analiz (öneri; onay bekliyor)

Kaynak: `chapters/03_gerec_ve_yontem.qmd` §Veri Toplama Süreci ve Veri Yönetimi (¶119, ¶121) + §İstatistiksel Analiz (¶127) + §Tanımlayıcı istatistikler ve grup dengesi (¶131) + §Eksik veri yönetimi (¶135). **Dört-mercek adversaryal doğrulama: 4/4 TEMİZ** (sadakat-RBŞ · eklenen-iddia · Marmara-register · DOKUNULMAZ-tamlık). `verify_authored_spans` = 24 span PASS.

**Bu dalgada değiştirilmeyen iki alt-birim (kasıtlı):**
- **¶119 (işe alım süreci)** — DEĞİŞMEDİ. "Poliklinik başvurusunu izleyen dahil edilme değerlendirmesi" kaynağın işe alım-yeri provenansıdır (yasaklı register-ekleme "poliklinikte" ifadesi değil); zaten düz anlatım, klinisyene açık. Dokunulmadı.
- **¶123 (R/`targets`/`renv` + paket listesi)** — DEĞİŞMEDİ. Saf araç-envanteri; her paketin yanında zaten Türkçe işlev açıklaması var (ör. `dagitty` için "kovaryat seti türetme…"). Sadeleştirme detay kaybı riski taşırdı; olduğu gibi bırakıldı.

**Bu dalganın niteliği:** Dört alt-birim de zaten sayı/atıf yoğun ve doğru register'da; klinisyen-erişilebilirliği için gereken tek müdahale **uzun iç-içe cümlelerin noktalı-virgülden bölünmesi** oldu. Hiçbir alt-birimde jargon-çevirisi eklenmedi (terimler zaten parantezli klinik-karşılıkla tanımlı), hiçbir sayı/atıf/çekince dokunulmadı. Bu, "ölçek uyumu → hafif dokunuş" ilkesinin uygulamasıdır.

## D5-a · ¶121 Veri yönetimi ve değişmezlik
**Değişiklik:** İki uzun cümle noktalı-virgülden bölündü ("…kilitler; toplam…" → "…kilitler. Toplam…"; "…saklanmaz, çözümleme…" → "…saklanmaz; çözümleme…"). İçerik birebir.
**DOKUNULMAZ (korundu):** `s-EMBU-C q25` ters puanlama · `%50 madde mevcutluğu eşiği` · `SHA-256` · satır/sütun doğrulaması · "skorlar referans dosyada saklanmaz / çözümleme katmanında üretilir" değişmezlik ilkesi.

## D5-b · ¶127 İstatistiksel analiz (çokluk / test ailesi / güven aralığı)
**Değişiklik:** (1) "α = 0,05 olarak belirlenmiş; birincil…" iki cümleye bölündü. (2) İç-içe Holm cümlesi bölündü: sıfat-öbeği ("…denetleyen Holm düzeltmesiyle…") bağımsız cümleye alındı ("…Holm düzeltmesiyle ele alınmıştır [@holm1979]; Holm düzeltmesi, o test ailesinde en az bir yanlış-pozitif çıkma olasılığını … denetler."). Aynı önerme; "en az bir yanlış-pozitif / test ailesi düzeyinde hata oranı" ifadesi ESKİ'de zaten vardı.
**DOKUNULMAZ (korundu):** `α = 0,05` · `[@benjaminiHochberg1995fdr]` · `[@holm1979]` · *test ailesidir* (italik) · "test ailesi ≠ sosyal aile" ayrımı · FDR(birincil H1–H4) ↔ Holm(keşifsel/ikincil) hat ayrımı · `%95 güven aralığı` + `%95 güvenilir aralığı` · `BCa` · `1000 yineleme` (×3: aracılık/ağ-kalibrasyon/diadik).

## D5-c · ¶131 Tanımlayıcı istatistikler ve grup dengesi
**Değişiklik:** "…aile düzeyinde raporlanmış; grup dengesizliği…" noktadan bölündü. SMD gerekçesi ("istatistiksel anlamlılık ≠ pratik denge", p'den bağımsız etki-büyüklüğü ölçeği) birebir korundu.
**DOKUNULMAZ (korundu):** `SMD` (standardize ortalama fark) · `[@austin2009balanceDiagnostics]` · medyan/ÇAA · p-bağımsızlık gerekçesi.

## D5-d · ¶135 Eksik veri yönetimi
**Değişiklik:** Dört noktalı-virgül cümle bölmesi ("gerekçesi; …" → ayrı cümle; "…yürütülmüş; tam-vaka…" → "…yürütülmüştür. Tam-vaka…"; "Çoklu atama, zincirli…" → "Çoklu atama; zincirli…"; "…dayanıklılık, atanmış…" → "…dayanıklılık; atanmış…"). PMM em-dash açıklaması ESKİ ile birebir aynı (kötüleştirilmedi).
**DOKUNULMAZ (korundu):** üç çerçeve = sağlamlık kanıtı mantığı · `FIML` tanımı + `[@endersBandalos2001fiml]` · *multiple imputation* (italik) · `MAR` varsayımı · "tam-vaka … tamamlayıcı" çekincesi · `[@vanBuuren2011mice]` · `m = 50` · `otuz iterasyon` · PMM/lojistik/orantılı-olasılıklar eşlemesi · sabit tohum · `MNAR` + `delta` duyarlılık · DM'ye özgü klinik zamanlama değişkenlerinin grup karşılaştırmalı atama kapsamı dışında tutulması · `[@littleRubin2019missing]`.

*(Dört alt-birimin tam ESKİ↔YENİ metni `/tmp/kdu_03_d5_authored.md`'de.)*

## Tez-geneli bağlam etkisi notu (D5)
- **Terim tutarlılığı:** yeni terim getirilmedi; "test ailesi", `SMD`, `FIML`, `MAR/MNAR`, `delta`, `m = 50` mevcut kanonik kullanımlarla aynı. Backlog etkisi yok.
- **Çapraz-referans:** ¶127'deki FDR/Holm ayrımı Bulgular'daki çokluk-düzeltme raporlamasını çerçeveler; bölme sonrası atıf zinciri değişmedi. ¶135 eksik-veri çerçevesi Duyarlılık (§sec-cok-evren) ve Bayesçi hatla tutarlı.
- **Özet/summary:** yöntem-özeti sayıları (α, m=50, %95) değişmedi → İngilizce özet senkronu gerektirmez.

## D5 Onay kutusu — TÜMÜ ONAYLANDI + UYGULANDI (2026-07-30, revizyonsuz; 4-mercek TEMİZ)
- [x] D5-a ¶121 veri yönetimi (değişmezlik/SHA-256/%50 eşiği)
- [x] D5-b ¶127 istatistiksel analiz (α/FDR/Holm/test ailesi/BCa)
- [x] D5-c ¶131 tanımlayıcı + grup dengesi (SMD)
- [x] D5-d ¶135 eksik veri (FIML/MI/m=50/MNAR-delta)
- [x] ¶119 (işe alım) ve ¶123 (R paket listesi) DEĞİŞMEDEN kalsın onayı

Onay sonrası: dördü `03_gerec_ve_yontem_new.qmd`'ye işlenir (ana dosya dokunulmaz); DOKUNULMAZ grep-teyit; journal + bellek güncellenir. Sıradaki: **D6 — Nedensel çıkarım çerçevesi + Hipotez temelli modeller + Duyarlılık + Bayesçi hat + keşifsel katmanlar**.

---

# D6-A — Nedensel çıkarım çerçevesi + H1–H5 modelleri (öneri; onay bekliyor)

Kaynak: `chapters/03_gerec_ve_yontem.qmd` §Nedensel çıkarım çerçevesi (¶139) + §Hipotez temelli modeller H1–H5 (¶155,157,159,161,163). **D6, en yoğun DOKUNULMAZ-yüzeyli bölge olduğu için iki yarıda sunulur; bu D6-A.** (D6-B = ¶167 duyarlılık + ¶171 Bayesçi + ¶175–179 keşifsel.)

**Doğrulama:** `verify_authored_spans` 6/6 PASS (61 span; ¶139 geliştirilmiş hâl 20 span). **Dört-mercek adversaryal: 4/4 TEMİZ** (sadakat-RBŞ · eklenen-iddia · Marmara-register · DOKUNULMAZ-tamlık; 55/55 token birebir).

**Değiştirilmeyen (kasıtlı):**
- **¶143 (hipotez intro)** — zaten kısa/açık; dokunulmadı.
- **@tbl-analiz-plani (H1–H5 plan tablosu, 6 satır)** — VERBATIM DOKUNULMAZ; dokunulmadı.
- **¶161 (H4) ve ¶163 (H5)** — zaten cümle-cümle bölünmüş, klinisyen-okunur; sadeleştirme gereksiz → YENİ = ESKİ (değişiklik yok). Dört mercek de teyit etti.

**Bu dalganın niteliği:** baskın müdahale **dev tek-zincir cümlelerin bölünmesi** (¶139 ~450 kelimelik tek zincirdi). Jargon zaten parantezli glossa'lı; çeviri eklenmedi, sayı/atıf/çekince dokunulmadı.

## D6-A-a · ¶139 Nedensel çıkarım çerçevesi
**Değişiklik:** ~450 kelimelik tek-zincir paragraf ~13 cümleye bölündü. Kritik bölme noktaları: (1) "toplam-etki … anlamındadır**;** ancak…" → ayrı cümle; (2) nokta-tanımlanamazlık iki nedeni ayrıldı (olgu cümlesi "…oluşturur;" + sonuç "koşullandığından… değildir"); (3) IPTW zinciri "budanmış**,** … değerlendirilmiş **ve** … belirlenmiştir" → üç ayrı cümle; (4) **[mercek-3 advisory üzerine]** anne-yaşı H1-dışlama gerekçesi (iki-nokta + noktalı-virgül + gecikmeli "varsayılmıştır") üç cümleye bölündü — governing fiil "varsayılmıştır" iki kez tekrarlandı; yeni iddia yok.
**DOKUNULMAZ (korundu, 20 span):** `[@textor2017dagitty]` · *Directed Acyclic Graph* / *backdoor set* / *selection node*, S / *point-identified* / *propensity score* / *doubly robust* / *genişletilmiş* / *algıladığı* (italik) · `@fig-causal-dag` · `@tbl-apa-sample-characteristics` · `§@sec-cok-evren` · `[@rosenbaumRubin1983propensity; @austin2011propensityIntro]` · `[@austinStuart2015iptw]` · `(IPTW)` · `SMD ≈ 0,21` · `99. persentilde budanmıştır` · **çekinceler:** "nokta-tanımlanabilir DEĞİLDİR" · "koşullu ilişkiler olarak okunmalıdır" · "nedensellik iddiası kurmaz ve randomizasyon üretmez" · anne yaşı H1'de-dışlandı ↔ H3/H4'te-ayarlandı ayrımı.

## D6-A-b · ¶155 H1 – Çocuk algısı
**Değişiklik:** 2 noktalı-virgül bölmesi ("bağımsız değildir**;** birincil model" → ayrı cümle; "kestirilmektedir**;** bu kontrastlar" → ayrı cümle). Bold etiket korundu.
**DOKUNULMAZ (korundu):** `s-EMBU-C` · `[@hox2017multilevel]` · `[@samejima1969graded]` · latent yetenek (θ) · *graded response* · rol × yaş × cinsiyet · **keşifsel/post-hoc** etiketi · dört düzeyli rol faktörü · çekince "doğrulayıcı düzeltilmiş anlamlılık iddiası taşımaz".

## D6-A-c · ¶157 H2 – Kardeş ilişkisi
**Değişiklik:** 1 noktalı-virgül bölmesi ("[@kennyKashyCook2006]**;** kardeş yaş farkı" → ayrı cümle). Bold korundu.
**DOKUNULMAZ (korundu):** Welch t-testi + Hedges g · varyans-homojenliği gerekçesi · (aktör)/(partner) APIM · `[@kennyKashyCook2006]` · `[@olsenKenny2006interchangeableDyads]` · aynı cinsiyet düzenleyici.

## D6-A-d · ¶159 H3 – Anne öz-bildirimi
**Değişiklik:** 1 bölme ("eklenmemiş (…kılabilir)**;** bunun yerine" → "eklenmemiştir (…kılabilir)**.** Bunun yerine"). Bold korundu.
**DOKUNULMAZ (korundu):** `s-EMBU-P` · kovaryans analizi kovaryatları · antidepresan = ARACI olduğu için ana modele konmama mantığı · `HC3` sağlam standart hata.

## D6-A-e · ¶161 H4 & D6-A-f · ¶163 H5 — DEĞİŞİKLİK YOK
İkisi de zaten klinisyen-okunur cümle yapısında; **YENİ = ESKİ**. Dört mercek de birebir aynılığı + DOKUNULMAZ tamlığı (WLSMV/polikorik/eşdeğerlik; beş strateji/ICC(2,1)=ICC(A,1)/RSA/common fate/bootstrap/"en az üç strateji güçlü-bulgu ön-ölçütü") teyit etti. Bütünlük için envanterde tutuldu.

*(¶139/¶155/¶157/¶159 tam ESKİ↔YENİ `/tmp/kdu_03_d6a_authored.md`'de; ¶139'un ek anne-yaşı bölmesi bu taslaktaki nihai hâldir.)*

## Tez-geneli bağlam etkisi notu (D6-A)
- **Terim tutarlılığı:** yeni terim yok; DAG/IPTW/θ/WLSMV/ICC/APIM/HC3 mevcut kanonik kullanımla aynı. Backlog etkisi yok.
- **Çapraz-referans:** `@fig-causal-dag`, `@tbl-apa-sample-characteristics`, `@tbl-analiz-plani`, `§@sec-cok-evren` ve 8 atıf token'ı bölme sonrası korundu; ¶139'daki `§@sec-cok-evren` ileri-atıfı D6-B (¶167) ile tutarlı kalır.
- **Özet/summary:** yöntem-tasarım anlatısı; sayısal sonuç yok → özet senkronu gerektirmez.

## D6-A Onay kutusu — TÜMÜ ONAYLANDI + UYGULANDI (2026-07-30; 4-mercek TEMİZ)
- [x] D6-A-a ¶139 nedensel çıkarım çerçevesi (DAG/seçilim/IPTW/çift-sağlam + anne-yaşı ek bölme)
- [x] D6-A-b ¶155 H1 (çok düzeyli + IRT θ + keşifsel rol kontrastı)
- [x] D6-A-c ¶157 H2 (Welch/Hedges g + APIM + diyad CFA)
- [x] D6-A-d ¶159 H3 (kovaryans + eğilim skoru + HC3)
- [x] D6-A-e ¶161 H4 + D6-A-f ¶163 H5 DEĞİŞMEDEN kalsın onayı
- [x] ¶143 + @tbl-analiz-plani DEĞİŞMEDEN kalsın onayı

Onay sonrası: değişen dört alt-birim (¶139, ¶155, ¶157, ¶159) `03_gerec_ve_yontem_new.qmd`'ye işlenir (ana dosya dokunulmaz); DOKUNULMAZ grep-teyit; sonra **D6-B** (¶167 + ¶171 + ¶175–179).

---

# D-REV — Register standardı v2 propagasyonu (D1–D6-A geriye dönük) (öneri; onay bekliyor)

Kullanıcı talimatı: "bu ilkeleri daha önce yazdığın D1–D5 için de uygula." Standart v2 (`klinisyen-uyarlama-register-standardi.md`): coinage sadeleştir (çizge→nedensel diyagram · kestirimci→kestirim yöntemi · yordam→işlem/yöntem; **kovaryat kalır**) + ağır glossa→dipnot (yalnız kaynağın MEVCUT tanımı birebir) + uzun cümle böl. ¶139-rev bu dalganın emsali olarak zaten uygulandı (4/4 TEMİZ).

**Doğrulama:** `verify_authored_spans` 7/7 PASS · **4-mercek adversaryal 4/4 TEMİZ** (kalan ≥45-kelime cümle=0; gövdede opak coinage=0; 23/23 R paketi; 3 dipnot kaynak tanımıyla karakter-düzeyinde birebir; sıfır overclaim).

| Birim | Değişiklik | Korunan DOKUNULMAZ |
|---|---|---|
| **DREV-1** ¶73 Demografik form | 56-kelime enümerasyon → 2 cümle | tüm alan listeleri · tanı tarihi/diyabet süresi · kovaryat |
| **DREV-2** ¶114 Faktör yapısı | kestirimci→kestirim yöntemi | `@li2016ordinalCFA` · WLSMV + *Weighted Least Squares…* |
| **DREV-3** ¶130 Taban etkisi | yordam→işlem | `@lakens2017equivalence` · *two one-sided tests*, TOST |
| **DREV-4** ¶123 R-paket listesi | 97-kelime run-on → **13 madde-liste** + çizge→nedensel diyagram ×2 | 23/23 paket + `targets`/`renv` · dagitty işlev tanımı |
| **DREV-5** ¶150 Eksik veri | FIML/MI/PMM tanımları → **3 dipnot** + uzun cümle böl | 3 atıf · *multiple imputation* · m=50 · otuz iterasyon · MAR/MNAR/delta · orantılı olasılıklar reg. · yapısal eksik · tam-vaka çekincesi |
| **DREV-6** ¶158 Hipotez intro | 51-kelime iki-nokta-liste → 4 cümle | `@tbl-analiz-plani` (kuyruk, dokunulmadı) · aktör–partner · aile rastgele etkisi/kümelenmiş SE |
| **DREV-7** ¶176 H4 | kestirimci→kestirim yöntemi | WLSMV · polikorik korelasyon |

**Not:** DREV-6'da yalnız ilk uzun cümle bölünür; `@tbl-analiz-plani` cümlesi **değişmez** (kuyrukta kalır). D6-A'da "değişmez" işaretlenen ¶161/¶163 (H4/H5) — H4'te yalnız tek terim (kestirimci→kestirim yöntemi, DREV-7); H5 hâlâ dokunulmaz.

## D-REV Onay kutusu — TÜMÜ ONAYLANDI + UYGULANDI (2026-07-30; 4-mercek TEMİZ)
- [x] DREV-1 ¶73 Demografik form (enümerasyon böl)
- [x] DREV-2 ¶114 + DREV-7 ¶176 (kestirimci→kestirim yöntemi ×2)
- [x] DREV-3 ¶130 (yordam→işlem)
- [x] DREV-4 ¶123 R-paket → madde-liste + çizge→nedensel diyagram
- [x] DREV-5 ¶150 Eksik veri (FIML/MI/PMM → dipnot + böl)
- [x] DREV-6 ¶158 Hipotez intro (iki-nokta-liste böl)

Onay sonrası: 7 birim `03_gerec_ve_yontem_new.qmd`'ye işlenir (ana dosya dokunulmaz); grep-teyit; ardından **D6-B** (¶167/¶171/¶175–179) doğrudan **standart v2 ile** yazılır.

---

# D6-B — Duyarlılık + Bayesçi hat + keşifsel katmanlar (standart v2; öneri; onay bekliyor)

Kaynak: `chapters/03` ¶167 (§Duyarlılık), ¶171 (§Bayesçi paralel hat), ¶175/¶177/¶179 (§Tamamlayıcı ve keşifsel). Bölümün en yoğun sayı/önsel bölgesi. **verify_authored_spans 5/5 PASS · 4-mercek adversaryal 4/4 TEMİZ** (¶200'ün 30+ nicel öğesi tek tek doğrulandı: reddetme −0,15, g ≈ −0,22 eksi işaretleri + tüm önsel dağılımları/atıflar korundu; sıfır yön-kayması).

**4-mercek sonrası üç sıkılaştırma (fidelity-artırıcı; DOKUNULMAZ'a dokunmaz):**
- **D6B-3** aracılık glossa'sı dipnottan çıkarılıp kaynaktaki gibi **satır-içi em-dash**'e döndürüldü ("gösterir" eklemesi kalktı — verbatim).
- **D6B-5** "şu ilişkileri" → nötr **"şunları"**; iki yüzey de **madde-listesine** (öğeler kaynaktaki accusative hâliyle birebir) → gerçek ≥45-kelime cümle 0.
- **D6B-1** H1 3-set'i de (5-set'in kardeşi) madde-listesine (parallellik).

| Birim | Değişiklik | Korunan DOKUNULMAZ |
|---|---|---|
| **D6B-1** ¶167 Duyarlılık | yordam→işlem ×2 · multiverse **5-set + H1 3-set → madde-liste** · TOST cümlesi böl | multiverse setleri içerikleriyle · ±0,30 SMD · SESOI · @pinquart2013 · *estimand*/β · RV/E-değeri · negatif kontrol/*falsification*/*batch* · 4 atıf |
| **D6B-2** ¶171 Bayesçi | dev-¶ → **5 mantıksal paragraf** · *divergent transition* def → **dipnot** · MERKEZİNE→merkezine | **tüm önseller:** Normal(·;0,50)/Normal(0,20;0,50)/Normal(0;0,50)/Normal(0;2)/student-t(3;0;2,5) · sıcaklık 0,20/aşırı koruma 0,30/reddetme −0,15/karşılaştırma 0,10 · g≈0,39 / g≈−0,22 + "Pinquart yönü değil/tözsel tercih" çekincesi · 0,25/0,50/1,00 · BF₁₀ · dört zincir/4000/1500 · R̂<1,01 · ROPE · Ek 6/@tbl-apa-prior-center · 6 atıf |
| **D6B-3** ¶175 Keşifsel 5 aile | aracılık glossa satır-içi (verbatim) · uzun cümle böl | keşifsel/post-hoc · "nedensellik olarak yorumlanmamıştır" · "ileriye dönük risk yordama modeli değildir" · n=39 · ROC/CART/*random forest* · 2 atıf |
| **D6B-4** ¶177 Ölçüm-genişletme | çizge→nedensel diyagram · cümle böl | trifaktör…seçilim/merkez katmanları · [-@sec-kesifsel-genisletme] |
| **D6B-5** ¶179 Artık + gelişimsel-diadik | iki yüzey → **madde-liste** ("şunları") | b-yolu · triadik LPA · n=39 · keşifsel/post-hoc · "doğrulayıcı çekirdeği değiştirmez" |

**İstişari (bölünmedi, kasıtlı):** D6B-2'de rapor-listesi cümlesi (~46k) ve D6B-4'te ölçüm-genişletme katalog cümlesi (~57k) — ikisi de tek-yüklemli doğal envanter; madde-liste yapmak 11+ öğeye bölerdi. Nesir bırakıldı; register mercek "istişari" saydı.

## D6-B Onay kutusu — TÜMÜ ONAYLANDI + UYGULANDI (2026-07-30; 4-mercek TEMİZ + 3 sıkılaştırma)
- [x] D6B-1 ¶167 Duyarlılık (yordam→işlem · multiverse+H1 madde-liste · TOST böl)
- [x] D6B-2 ¶171 Bayesçi (5 paragraf · divergent transition dipnot · tüm önseller korundu)
- [x] D6B-3 ¶175 Keşifsel 5 aile (aracılık satır-içi · böl)
- [x] D6B-4 ¶177 Ölçüm-genişletme (çizge→nedensel diyagram · böl)
- [x] D6B-5 ¶179 Artık + gelişimsel-diadik (madde-liste)

Onay sonrası: 5 birim `03_new.qmd`'ye işlenir (ana dosya dokunulmaz); grep-teyit; **Bölüm 03'ün nicel kolu (D1–D6) tamamlanır** → sonra D7 (Nitel kol) + D8 (Raporlama/Etik/YZ).
