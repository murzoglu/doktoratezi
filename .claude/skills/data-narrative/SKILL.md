---
name: data-narrative
description: >
  Bir tablo, şekil, diyagram, grafik, istatistiksel sonuç, model çıktısı veya metin bölümünü "çok
  basite indirgeyerek ama detayları atlamadan, ders anlatır gibi" izah etmek için otör-düzeyi
  anlatım kapısı. Önce kaynaktan doğrular, öğenin TİPİNİ tanıyıp o tipe özgü okuma hamlesini
  uygular, değerleri kaynaklı büyüklük eşiklerine oturtur, yaygın kavram-yanılgılarını önler,
  "neden var → mekanizma → kanıt → tek cümle" akışıyla günlük dile çevirir, gerçek sayıları
  birebir korur, zayıf/başarısız yönleri dürüstçe gösterir. Tetikleyiciler: "izah et", "basitçe
  anlat", "ders anlatır gibi açıkla", "bu tabloyu/şekli/diyagramı/grafiği tarif et", "sadeleştir
  ama detay atlama", "Tablo X.Y'yi açıkla", "Şekil X'i yorumla", "bu ne anlama geliyor", "bu değer
  iyi mi", "yorumla", "ne demek", "data-narrative".
---

# Data Narrative — Nicel İçeriği Ders Anlatır Gibi, Sade ve Eksiksiz İzah Etme

Bir tabloyu/şekli/diyagramı/istatistik sonucunu/metin bölümünü, teknik doğruluğundan
ödün vermeden, konunun uzmanı olmayan zeki bir okurun anlayacağı netlikte açıkla.
Amaç: **maksimum sadelik + sıfır detay kaybı + birebir sayısal doğruluk + doğru dersi
öğretmek** (yanlış okumayı önlemek).

Bu bir *yazım/üslup* kapısıdır. Analizi değiştirmez, yeni sonuç üretmez. Yalnız var
olanı, en iyi öğretici gibi anlatır.

## Değişmez ilke: Önce doğrula + tipi tanı, sonra anlat

**Asla hafızadan veya tahminle açıklama yapma.** Her açıklamadan önce iki şeyi yap:

1. **Kaynağı doğrula.** Öğenin **kanonik kimliğini** bul (bu tezde tablolar
   `@tbl-apa-...`, şekiller `@fig-...`; "Tablo 4.4" gibi numaralar render sırasına göre
   otomatik atanır — numara→etiket için `#| label:` sırasını say). İçeriği, caption'ı,
   çevre metnini ve **üreten R modülü/CSV artefaktını** `grep`/`sed`/gerekirse
   `researcher` ile oku. Aktaracağın her sayıyı (α/ω, SMD, β, OR, r, p, CFI, RMSEA, BF,
   ICC, AUC…) kaynaktan **birebir** al; yuvarlama/uydurma yok; ondalık-virgülü koru.
   Metin ile tablo/CSV çelişiyorsa açıklama yazma, çelişkiyi bildir. Emin değilsen
   netleştir. Komut kalıpları: **`references/kaynak-dogrulama.md`**.
2. **Öğe tipini tanı → okuma hamlesini seç.** Bir orman grafiği, bir DAG, bir
   Bland–Altman ve bir uyum-indeksi tablosu **aynı** kalıpla açıklanamaz; her ailenin
   kendi "önce şuna bak" hamlesi ve tipik yanılgısı vardır. Öğe ailesini belirle ve o
   ailenin okuma hamlesini getir: **`references/gorsel-okuma-rehberi.md`** (aile listede
   yoksa oradaki genel yöntem). Bu hamle altyazının cömertliğinden değil, rehberden
   gelir.

## Anlatım akışı: 5 katman (görünmez iskelet)

Doğrulama + tip tanıma bittikten sonra açıklamayı şu iskeletle kur.

1. **"Neden var?"** Teknik tanımdan **önce** öğenin çözdüğü sorunu/gerilimi günlük dille
   kur. Okur "bu neyin derdine çare?" yanıtını en baştan almalı.
   - İyi: "Bir cetvelle sıcaklık ölçemezsiniz; bir anketin gerçekten ölçtüğünü
     kanıtlamadan sonuçlarına güvenemeyiz."  Kötü: "Cronbach alfa iç tutarlılık
     katsayısıdır."
2. **Somutlaştır.** 1–3 isabetli analoji/günlük karşılık ("sanki rastgele atanmış gibi
   yapmak", "elmayla elma", "karne notu"). Analoji enflasyonu netliği bozar.
3. **Mekanizma (kademeli).** Basit sorudan mekanizmaya; gerekirse numaralı alt-adım ya
   da "soru→yanıt". Öğe-tipi okuma hamlesi (Adım 2) burada işler: okurun gözünü önce
   nereye koyacağını göster. Jargonu **ilk geçişte parantezle** karşıla
   ("**ortak destek** (iki grubun karşılaştırılabilir olduğu aralık)").
4. **Kanıt — gerçek sayılarla + büyüklük okuryazarlığı.** Öğenin ne söylediğini
   kaynaktan aldığın değerlerle göster (küçük tablo / öncesi-sonrası). Bir sayı "iyi
   mi?" sorusunu davet ediyorsa (CFI, α, BF, ICC, SMD, AUC, d…) onu **kaynaklı geleneksel
   eşiğine** oturt — eşiği kökeniyle ver ve "yasa değil gelenek" diye çerçevele; asla
   çıplak "iyi/kötü" deme. Eşikler, numeracy çevirileri ve tezin kendi çıpaları:
   **`references/buyukluk-esikleri.md`**. Her sayının yanına "yorum" koy (0,004 =
   "neredeyse sıfır ✓").
5. **Tek cümle özet.** Blockquote içinde tek damıtılmış cümle; okur yalnız bunu okusa
   özü almalı.

## Öğretim hamleleri — "ders anlatır gibi"

İyi bir açıklama sadece doğru değil, **öğretir**. Uygun yerlerde bu hamleleri kullan:

- **Yanlış okumayı önceden düzelt.** Okurun büyük olasılıkla düşeceği yanılgıyı adlandır
  ve düzelt: "Şunu düşünebilirsiniz — ama…". (Ör. "anlamlı = büyük etki sanmak".)
- **Zıtlıkla öğret.** Yanlış okuma ↔ doğru okuma. ("Yüksek korelasyon uyum sanılır;
  oysa Bland–Altman mutlak uyumu ölçer.")
- **Sayıyı günlük dile çevir (numeracy).** OR/β/d/r'yi somut büyüklüğe tercüme et
  (`buyukluk-esikleri.md` numeracy bölümü). "küçük p ≠ büyük etki"yi daima ayır.
- **"Bu değer nereye düşer?"** Değeri kendi ölçeğindeki eşiğe yerleştir; tek indekse
  indirgeme, çelişen indeksleri birlikte oku.
- **"Ee, sonra?" köprüsü.** Bu öğenin bir sonrakine neden zemin hazırladığını bir cümleyle
  bağla (akışı öğretir).

## Kavram-yanılgısı kapıları (uygun olanı açıkça ele al)

- **anlamlı ≠ büyük**; **anlamsız ≠ etki yok** (kanıt yokluğu ≠ yokluk kanıtı; BF/ROPE bu
  ayrımı verir).
- **GA/GüvenilirAralık sıfırı içeriyorsa** etki sıfırdan ayırt edilemiyor (ama sıfır da
  kesinlik değil).
- **korelasyon/ayarlanmış ilişki ≠ nedensellik**; gözlemsel tasarımda "yordar/açıklar"
  değil "birlikte değişir" dili.
- **iyi uyum ≠ doğru/nedensel model**; tek uyum indeksi (ör. büyük df'de RMSEA)
  yanıltabilir.
- **görünür (apparent) ≠ optimizm-düzeltilmiş** (AUC, kalibrasyon).
- **keşifsel ≠ doğrulayıcı** ([KEŞİFSEL] etiketli öğelerde bunu söyle).
- **eşik = gelenek, yasa değil**; kökenini belirt.

## Zorunlu davranışlar

- **Dürüstlük kapısı:** zayıf/sınırlı/başarısız yönleri **gizleme** (ör. EMBU-P reddetme
  α = 0,45 düşüklüğü). ⚠️/✓/❌ kullanılabilir. "İşe yaramayanı da söylemek" kalitedir.
- **Sayısal bütünlük (AGENTS.md):** hiçbir sayı/yön/anlamlılık değiştirilmez,
  uydurulmaz, yuvarlanmaz. Eşik verirken de kaynağını + tezdeki fiili değeri birebir ver.
- **Dil:** Türkçe (`lang: tr`); teknik terim ilk geçişte parantezle.
- **Ölçek uyumu:** basit öğe (tek α, tek histogram) → 2–3 katman; karmaşık öğe (çok
  değişkenli tablo, DAG, SEM, yanıt yüzeyi) → tüm katmanlar + alt-tablolar. Katmanları
  **numara vererek etiketleme**; okur akışı hissetmeli.
- **Kapanış teklifi:** ilgili komşu öğeleri (yandaki tablo, bağlı şekil, önceki/sonraki
  hipotez) aynı biçimde açma teklifini kısaca sun.

## Yasaklar

- Kaynağı okumadan / tipi tanımadan açıklama yazma.
- Sayı uydurma / yuvarlama / hafızadan aktarma; çıplak "iyi/kötü" (eşiksiz-kaynaksız) verme.
- Zayıf sonuçları saklama veya güzelleştirme; jargonu karşılıksız bırakma.
- "Katman 1/2/3" gibi iskeleti görünür kılma.
- Marketing dili ("kapsamlı", "güçlü", "son derece").

## Çıktı biçimi

- Başlık: "# <Öğe> — Basitçe, Ama Eksiksiz" (kanonik kimlik + kaynak dosya:satır).
- Gövde: öğe-tipi okuma hamlesi + 5 katman (görünmez iskelet) + öğretim hamleleri +
  gerektiğinde küçük tablolar; sayılar eşiğe oturtulmuş.
- Kapanış: tek-cümle blockquote + komşu-öğe açma teklifi.
- Uzunluğu içeriğin karmaşıklığına göre ayarla; basit öğeyi şişirme.

## Referanslar

- **`references/kaynak-dogrulama.md`** — numara→etiket eşleme, içerik/üreten kaynak/gerçek
  sayı doğrulama komut kalıpları, researcher ne zaman.
- **`references/gorsel-okuma-rehberi.md`** — öğe tipini tanıma + her aile için okuma
  hamlesi ve tipik yanılgı (orman, DAG, Bland–Altman, RSA, ağ, ROC/DCA/kalibrasyon,
  spec-eğrisi, sensemakr, Love, ısı haritası, CFA/IRT, LPA, tablolar…).
- **`references/buyukluk-esikleri.md`** — kaynaklı büyüklük eşikleri (Cohen, Hu–Bentler,
  Koo–Li, Austin, Jeffreys/BF, AUC…), numeracy çevirileri, tez çıpaları, worked örnek.
- **`references/ornek-tablo-4-4.md`** — referans-kalite **tablo** açıklaması (üslup).
- **`references/ornek-sekil-dag.md`** — referans-kalite **şekil** açıklaması (okuma-hamlesi
  önce yapısı). Yeni açıklamadan önce üslup kalibrasyonu için okunur.

---

## Ek: tam tetikleyici kapsamı (arşiv)

Bu skill'in `description` alanı Copilot skill kayıt bütçesine (~1 KB) sığması için
kısaltılmıştır. Kısaltmadan önceki tam tetikleyici/anahtar-kelime listesi kayıt dışı
kalmasın diye burada saklanır; kapsam **değişmemiştir**.

> Bir tablo, şekil, diyagram, grafik, istatistiksel sonuç, model çıktısı veya metin bölümünü
> "çok basite indirgeyerek ama detayları atlamadan, ders anlatır gibi" izah etmek için
> otör-düzeyi anlatım kapısı. Önce kaynaktan doğrular, öğenin TİPİNİ tanıyıp o tipe özgü okuma
> hamlesini uygular, değerleri kaynaklı büyüklük eşiklerine oturtur, yaygın kavram-yanılgılarını
> önler, "neden var → mekanizma → kanıt → tek cümle" akışıyla günlük dile çevirir, gerçek
> sayıları birebir korur ve zayıf/başarısız yönleri dürüstçe gösterir. ŞU DURUMLARDA KULLAN:
> kullanıcı "bunu izah et", "basitçe anlat", "ders anlatır gibi açıkla", "bu
> tabloyu/şekli/diyagramı/grafiği tarif et", "sadeleştir ama detay atlama", "Tablo X.Y'yi
> açıkla", "Şekil X'i yorumla", "bu ne anlama geliyor", "bu değer iyi mi / ne kadar iyi", "bunu
> benzer biçimde açıkla", "data-narrative" derse ya da bir analiz/çıktı/görsel için
> netlik-sadelik-açıklık düzeyinde bir açıklama isterse. Tetik ifadeler: "izah et", "basitçe
> anlat", "ders gibi anlat", "tarif et", "sadeleştir", "açıkla", "yorumla", "ne demek", "iyi
> mi", "bu tabloyu/şekli anlat".
