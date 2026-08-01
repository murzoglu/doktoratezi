# İnsan-Türkçesi Bilimsel Retorik Playbook (Kapı 4 — üretim tarafı)

Sürüm: 1.0 · 2026-07-12

> **Konum:** Bu belge Kapı 4'ün **üretim (production)** tarafıdır;
> `turkce-bilimsel-yazim-denetimi.md` ise **denetim (detection)** tarafıdır.
> Denetçi (sci-audit axis G) *hataları yakalar*; bu playbook *metni baştan
> insan-elinden-çıkmış gibi üretmenin* kurallarını verir. İkisi birlikte Kapı
> 4'ü kapatır. Kanonik kural otoritesi hâlâ `marmara-tez-formati-talimatnamesi.md`
> §1–§5'tir; bu playbook onu retorik düzeyde işletir, yeniden tanımlamaz.

## Neden gerekli

Otomatik üretilen Türkçe akademik metin, imla açısından temiz olsa bile
**"makine-Türkçesi" imzası** taşır: aşırı düzenli cümle uzunluğu, şablon geçiş
kalıpları, gereksiz üst-anlatı ("Bu bölümde... ele alınacaktır"), İngilizce
sözdizim gölgesi ve retorik monotonluk. Marmara jürisi ve hakem, bu imzayı
"akıcı değil / yapay" olarak okur. Bu playbook o imzayı sistematik olarak siler.

## A. Cümle ritmi ve varyans (anti-monotonluk)

1. **Uzunluk varyansı zorunlu.** Ardışık üç cümle benzer uzunlukta olmasın;
   kısa (≤12 sözcük) — orta — uzun örüntüsünü bilinçli değiştir. Denetçi
   ortalama uzunluğa bakar; jüri *varyansa* bakar.
2. **Tek fikir = tek cümle** değil. İlişkili iki bulguyu bazen bir bileşik
   cümlede bağla (çünkü/ancak/dolayısıyla), bazen ayır. Mekanik "her bulguya
   bir cümle" ritmi yapay okunur.
3. **Paragraf yayı:** her paragraf iddia → kanıt → yorum/geçiş yayını izlesin;
   paragrafı bir sonrakine bağlayan köprü cümlesiyle bitir (şablon geçişle değil).

## B. Yasak makine-imzaları (kara liste)

| Kaçın | Yerine |
|---|---|
| "Bu bölümde ... ele alınacaktır / incelenecektir" | Doğrudan konuya gir; üst-anlatıyı at |
| "Yukarıda belirtildiği gibi", "aşağıdaki tabloda görüldüğü üzere" (aşırı) | Tek sefer yeter; tekrarını sil |
| "Sonuç olarak" / "Özetle" her paragraf başında | En çok bir kez, gerçek sentezde |
| "önemli bir role sahiptir", "kritik öneme sahiptir" | Somut etki: "*g* = 0,39 ile orta düzey ilişki" |
| "literatürde birçok çalışma" (belirsiz) | Sayı + atıf: "üç meta-analiz (…)" |
| Her cümlede edilgen + "-mektedir" zinciri | Edilgen koru ama fiil zamanı/yapısını çeşitlendir |
| Bağlaç olarak sürekli "Ayrıca / Bununla birlikte / Ek olarak" | Anlam ilişkisine uygun tek bağlaç; tekrarını kır |

## C. Marmara register (korunacak insan-Türkçesi)

- **Edilgen 3. tekil şahıs** akademik normdur ("bulunmuştur", "saptanmıştır") —
  ama fiil çeşitliliğiyle: gösterilmiştir / elde edilmiştir / gözlenmiştir /
  ortaya konmuştur. Aynı fiili peş peşe kullanma.
- **Ondalık virgül** her sayıda (G5 blocker): *p* = 0,003; *r* = 0,42; %95 GA.
- **Terim tutarlılığı:** bir kavram tez boyunca tek Türkçe karşılıkla anılır
  (ör. "aşırı koruma" — "overprotection" veya "aşırı korumacılık" ile
  karıştırma). İlk geçişte İngilizcesini parantezle ver, sonra Türkçe kullan.
- **İngilizce sızıntısı yok:** "sample" → örneklem, "outcome" → sonuç değişkeni,
  "baseline" → başlangıç, "effect size" → etki büyüklüğü.

## D. Argüman akışı (tartışma bölümü için)

1. **Bulguyu tekrar etme, yorumla.** Sonuçlar bölümündeki sayıyı Tartışma'da
   aynen tekrarlama; onu literatürle *konumlandır* (uyum/çelişki/genişletme).
2. **Nedensellik disiplini** (sci-audit + `claim_certification` ile hizalı):
   kesitsel/korelasyonel bulguda "neden olur / artırır / yol açar" YASAK;
   "ilişkili bulunmuştur / birlikte değişmektedir / öngörmektedir (kesitsel)".
   H1–H4 doğrulayıcı hattında bile mekanizma dili ancak açık *caveat* ile.
3. **Keşifsel/post-hoc etiket görünür olsun:** keşifsel bulgu cümlesinde
   "keşifsel olarak" / "hipotez üretici" ibaresini cümle içine göm; okuyucu
   doğrulayıcı sanmasın (`csr_causal_label_audit` bunu tarar).
4. **Negatif/null bulguyu sahiplen:** "anlamlı fark bulunmamıştır" cümlesini
   güç/örneklem sınırıyla dürüstçe çerçevele; gizleme.

## E. GraphRAG destekli yazımda provenance disiplini

- `scripts/mcp/graphrag_query.py` çıktısındaki chunk'lar **sentez girdisidir**,
  kopyalanacak metin değil. Chunk'tan cümle üretirken kaynağın atıf-anahtarını
  (füzyon/graf genişletmesinde görünen `doc_id`) cümleye bağla.
- **Füzyon yeniden-sıralaması** insan önceliği içindir; galileo ikinci-görüşü
  "gömülü-ilgili" bayrağı verdiyse o kaynağı gözden kaçırma.
- Her sayısal iddia bir üretilmiş artefakta veya cite-ok künyeye izlenebilmeli
  (`claim_certification.py` bunu zorlar). Kaynaksız sayı = Stop kapısı.

## F. Üretim sonrası mini-ritüel (yazar öz-denetimi)

Bölüm taslağı biter bitmez, sci-audit'e vermeden **önce** yazar şunu yapar:

1. Metni **sesli oku** (zihinsel): takılan/robotik cümleyi işaretle.
2. **B tablosundaki kara-liste** kalıplarını `grep`le tara, kırp.
3. Ardışık 3 cümlenin uzunluğunu say; hepsi yakınsa birini böl/birleştir.
4. Aynı fiilin (ör. "bulunmuştur") paragraf içi tekrarını çeşitlendir.
5. Ancak bundan sonra Kapı 4 denetçisini (`turkce-bilimsel-yazim-denetimi.md`)
   çalıştır.

---

**Bağlı belgeler:** denetim tarafı `turkce-bilimsel-yazim-denetimi.md`;
nedensellik/etiket zorlaması `scripts/util/claim_certification.py` +
`csr_causal_label_audit.py`; kanonik register `marmara-tez-formati-talimatnamesi.md`
§1–§5; GraphRAG sentez `scripts/mcp/graphrag_query.py`.
