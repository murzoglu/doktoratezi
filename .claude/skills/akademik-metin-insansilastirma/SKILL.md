---
name: akademik-metin-insansilastirma
description: >
  Yapay zeka yardımıyla üretilmiş akademik nesri, **öze hiç dokunmadan** doğal insan
  akademik yazımına yeniden kurgulayan otör-düzeyi üslup kapısı. Tekdüze LLM ritmini
  (düşük burstiness), klişe geçiş kalıplarını ve şablon paragraf iskeletini kırar;
  buna karşılık her sayı, istatistik ifadesi, güven aralığı, atıf, çapraz-referans,
  kanıt-düzeyi etiketi, çekince, olumsuzlama ve iddia kapsamı **birebir** korunur.
  Koruma retorik değil **mekaniktir**: `scripts/eval/humanize_invariant_guard.py`
  düşme/mutasyon/uydurma/kesinlik-enflasyonunu HARD kapıyla durdurur. Eşanlamlı
  değiştirme (synonym swapping) ve "kelime salatası" YASAKTIR. Tetikleyiciler:
  "insansılaştır", "humanize", "robotik dili düzelt", "yapay zeka kokusunu al",
  "metin çok makine gibi", "cümle ritmi tekdüze", "LLM klişelerini temizle".
  DEĞİL: sadeleştirme (klinisyen-diline-uyarlama), literatür zenginleştirme
  (anlatim-zenginligi), figür/tablo sunumu (veri-gosterimi-zenginligi), ayrı
  açıklama üretimi (data-narrative).
---

# Akademik Metin İnsansılaştırma — üslup değişir, öz değişmez

Sunulan pasajı, deneyimli bir akademik yazarın kaleminden çıkmış gibi yeniden kur:
değişken ritimli, klişesiz, kendi sesine sahip, düşünsel akışı görünür bir nesir.
**Karşılığında metnin bilimsel özü tek bir karakter bile kaymaz.**

## Değişmez temel (bu skill'in tek kırmızı çizgisi)

> **Öz dokunulmazdır.** Bir sayı, oran, p değeri, güven aralığı, etki büyüklüğü,
> örneklem sayısı, bulgunun yönü, anlamlılık durumu, karşılaştırma grubu, koşul/kapsam
> ifadesi, çekince, kanıt-düzeyi etiketi, atıf anahtarı, çapraz-referans veya bir
> kaynağa atfedilen iddianın sahibi **değişemez, düşemez, eklenemez, yuvarlanamaz,
> güçlendirilemez, zayıflatılamaz.**

Bu ilkenin iki ayağı vardır ve **ikisi de** geçilmelidir:

| Ayak | Kapsam | Zorlama |
|---|---|---|
| **Sözel öz** (token) | sayı · istatistik ifadesi · aralık · atıf · `@tbl-*`/`@fig-*` · `§` · `[KEŞİFSEL]` · birim | **mekanik** — `humanize_invariant_guard.py guard` |
| **Anlamsal öz** (semantik) | yön · kapsam · koşul · nedensellik derecesi · atfetme · kesinlik derecesi | **ajan denetimi** + kesinlik/olumsuzluk/çekince sözlüğü + galileo SOFT |

Mekanik ayak *düşmeyi* yakalar, *eklenen abartıyı* kısmen yakalar. Anlamsal ayağın
sorumlusu sensin: **guard PASS verdi diye metin doğru değildir.**

## Kapsam ve dürüstlük sınırı (atlanamaz)

Bu kapı bir **yazım kalitesi** aracıdır: şablon LLM nesrini akademik insan nesrine
çevirir. Aşağıdakiler kapsam dışıdır ve yapılmaz:

- **YZ-kullanım beyanı silinmez/gizlenmez.** Kaynak metinde ICMJE/COPE/kurum
  gereği bir yapay zeka kullanım beyanı varsa aday metinde **aynen kalır** (guard
  bunu `yz_beyani` sınıfında HARD izler). Kurumsal beyan yükümlülüğü üslupla ortadan
  kalkmaz; bu skill beyanı değil **nesri** düzeltir.
- **Dedektör skoru kabul ölçütü değildir.** AI dedektörlerinin yanlış-pozitif oranı
  yüksektir ve skorları sürüm-bağımlıdır; bu skill'in kabul ölçütü
  `humanize_invariant_guard.py` + repo kapılarıdır, üçüncü taraf bir yüzde değil.
  Metni bir dedektöre **yüklemek** de KVKK açısından dışa aktarımdır — yapılmaz.
- **Kaynak/veri üretimi yoktur.** İnsansılaştırma adına yeni örnek, yeni sayı, yeni
  atıf, yeni yorum eklenmez. Metnin derinliği ancak *var olan kanıtın* daha iyi
  ifadesiyle artar.

## Adım 0 — Envanteri çıkar (yeniden yazmadan ÖNCE, atlanamaz)

Neyi koruyacağını bilmeden yazmaya başlama.

```bash
# 1) Pasajın gerçek konumunu bul — dosya adı TAHMİN ETME
grep -rn "<pasajdan 5-8 kelimelik özgün parça>" chapters/

# 2) DOKUNULMAZ envanteri çıkar (12 sınıf, çokluk sayımıyla)
python3 scripts/eval/humanize_invariant_guard.py inventory chapters/<bolum>.qmd

# 3) Kaynak metnin üslup teşhisi — neyi düzelteceğini ölç
python3 scripts/eval/humanize_invariant_guard.py metrics chapters/<bolum>.qmd
```

Envanterdeki her `[HARD]` satır bir **sözleşmedir**. Ek olarak elle çıkar:
kim-neyi-iddia-ediyor eşlemesi, koşul öbekleri ("… kontrol edildiğinde", "yalnızca
DM grubunda"), zaman/kip ("saptanmıştır" ≠ "saptanabilir"), karşılaştırma yönü.
Ayrıntı: `references/dokunulmazlik-envanteri.md`.

Sayısal değerleri **üreten artefakttan** teyit et (gömülü literal yok; `AGENTS.md`
"Sayisal Butunluk Kaideleri"). Metin ile artefakt çelişiyorsa **yazma, çelişkiyi bildir.**

## Adım 1 — Teşhis: metin neden "makine gibi" okunuyor?

`metrics` çıktısını üç eksende oku (eşikler `CONFIG`; hepsi sezgisel):

| Eksen | Ölçüt | LLM imzası | Hedef |
|---|---|---|---|
| **Ritim (burstiness)** | `cv` = SS/ortalama · `B` = (σ−μ)/(σ+μ) | cv ≈ 0,25–0,35; tekdüze seri sınırı aşar | cv ≥ 0,40 · `seri ≤ sınır` |
| **Sözcük çeşitliliği (perplexity vekili)** | `MATTR` (200 sözcüklük kayan pencere) | düşük MATTR + tekrarlı öbek | MATTR ≥ 0,60 |
| **Kalıp** | `cliche_per_1000`, `connective_start_ratio` | "bu bağlamda", "önem arz etmektedir" | ≤ 2,0 · ≤ 0,25 |

> **Neden MATTR, ham TTR değil?** Ham tür/belirteç oranı metin uzadıkça mekanik olarak
> düşer (14.000 sözcüklük bir bölümde TTR ≈ 0,30 normaldir, imza değildir). MATTR sabit
> pencerede ölçtüğü için uzunluktan bağımsızdır; rapor ham TTR'yi bilgi olarak yine
> gösterir. Aynı mantıkla `max_uniform_run` sınırı da metin uzunluğuyla logaritmik
> büyür (`maks(4, ⌈log₂ cümle sayısı⌉)`) — uzun metinde uzun seri şansa bağlıdır.

Teşhis yönlendirir: klişe yoğunsa sözcük katmanı, `max_uniform_run` yüksekse cümle
katmanı, `paragraph_len_cv` düşükse paragraf mimarisi öncelikli hedeftir.

## Adım 2 — Yeniden yaz (SEN yazarsın; otomatik eşanlamlı motoru YASAK)

Üç katman, **bu sırayla**. Sıra önemlidir: yapı düzelirse sözcük katmanına daha az
dokunmak gerekir — ve öz riski sözcük katmanındadır.

### Katman A — Cümle ritmi (en güvenli, en yüksek getirili)
- **Asimetri kur:** 5–8 sözcüklük tez cümlesinin ardına 28–40 sözcüklük analitik
  cümle. Ardışık üç cümle benzer uzunlukta olmasın.
- **Böl ve birleştir:** uzun bir "ve/ayrıca" zincirini iki cümleye ayır; iki cılız
  cümleyi noktalı virgülle tek düşünceye bağla.
- **Bilgi sırasını değiştir:** koşul öbeğini öne al ("Yaş ve cinsiyet kontrol
  edildiğinde, …"), yüklemi geciktir. Sayı ve koşul birlikte taşınır — koşulu
  cümleden koparıp atma.

### Katman B — Paragraf mimarisi
- "Konu cümlesi → 3 destek → özet" şablonunu kır: bazen bulguyla başla, bazen
  gerilimle; her paragrafı sonuç cümlesiyle kapatma.
- Paragraf uzunluklarını değiştir (2 cümlelik geçiş paragrafı meşrudur).
- Bağlaçla başlayan cümle oranını düşür: "Ayrıca X" yerine bağı **anlamla** kur.

### Katman C — Sözcük (en riskli — cerrahi dokun)
- **Klişeyi sil, yerine sözcük koyma.** "Bu bağlamda, X incelenmiştir" → "X
  incelenmiştir". Klişenin karşılığı çoğu zaman **boşluktur**, eşanlamlı değil.
- **KANONİK TERİM ASLA DEĞİŞMEZ.** `docs/tez-kilavuz/terim-sozlugu.yaml` kapsamındaki
  terimler (ör. "ortanca" → "medyan" yapılamaz), ölçek/alt ölçek adları, tanı
  adları, istatistik terimleri, değişken adları eşanlamlıya çevrilemez. Perplexity
  artışı **anlatım kurgusundan** gelir, terim oynatmaktan değil.
- **Yasak:** bağlam gözetmeyen eşanlamlı motoru, "kelime salatası", zorlama nadir
  sözcük, dedektör-kaçırma amaçlı görünmez karakter/homoglif/sıfır-genişlik
  ekleme (bu sonuncusu manipülasyondur; kesinlikle yapılmaz).

Ayrıntılı kalıp listesi ve güvenli karşılıklar: `references/llm-imza-kaliplari.md`;
ritim şablonları: `references/ritim-muhendisligi.md`.

### Katman D — Ses ve düşünsel derinlik (öz eklemeden)
- **Var olan kanıtı yorumla, yeni kanıt uydurma.** Metinde zaten olan bir çelişkiyi
  görünür kıl, bir sınırlılığın *neden* önemli olduğunu söyle.
- **Aşırı kesinliği yumuşat, ama tersini de yapma:** kaynakta "göstermektedir" ise
  "olabilir"e indirme, "olabilir" ise "kanıtlamaktadır"a yükseltme. Kesinlik derecesi
  de özün parçasıdır (guard `kesinlik` sınıfında yükseltmeyi HARD sayar).
- Doldurulması gereken gerçek boşluk varsa metne **yazar notu** bırak:
  `[Yazar notu: burada X çalışmasıyla karşılaştırma yararlı olur — atıf
  /referans-kapisi'ndan geçmeli]`. Kendin kaynak uydurma.

## Adım 3 — Mekanik kapı (uygulamadan ÖNCE; atlanamaz)

Aday metni geçici bir dosyaya yaz ve koştur:

```bash
python3 scripts/eval/humanize_invariant_guard.py all \
  --source /tmp/kaynak_pasaj.md --candidate /tmp/aday_pasaj.md
```

| Çıktı | Anlam | Karar |
|---|---|---|
| `HARD İHLAL` | öz değişmiş (düşme · mutasyon · uydurma · kesinlik enflasyonu) | **override YOK** — düzelt, yeniden koş |
| `SOFT` | yön/atıf-bloğu/çekince eklemesi — meşru olabilir | gerekçelendir veya geri al |
| `ÜSLUP HEDEFİ` bulgusu | insansılaştırma yeterince olmamış | Katman A–C'ye dön |
| exit 0 | öz korundu + üslup hedefleri tuttu | Adım 4 |

`guard` PASS'i **yeterli değil, gerekli**dir: eklenen abartıyı, kayan atfetmeyi ve
kapsam genişlemesini sen okuyarak denetlersin (`references/dokunulmazlik-envanteri.md`
§Anlamsal öz kontrol listesi).

## Adım 4 — Repo kapıları (HARD / SOFT-block / advisory)

| Kademe | Komut / araç | Rol |
|---|---|---|
| **HARD** | `python3 scripts/util/tr_corpus_audit.py all --fail-on blocker` | Türkçe imla + **ondalık virgül** (nokta-`p` = blocker) |
| **HARD** | `python3 scripts/util/terim_tutarlilik_audit.py` | kanonik terim kayması (eşanlamlı sızıntısının asıl bekçisi) |
| **HARD** | `python3 scripts/util/bib_hygiene.py all` · `citation-forensics` skill | atıf bütünlüğü, uydurma kaynak |
| **HARD** | `python3 scripts/util/claim_certification.py` · `csr_causal_label_audit.py` | iddia temellendirme + nedensellik etiketi |
| **HARD** | `turkish-sci-style` skill (`tr_sciaudit.py … --strictness certification`) | axis G |
| **SOFT-block** | `galileo-audit` → `galileo_judge` (`evidence` = kaynak pasaj) | faithfulness/groundedness — *anlamsal* öz kayması |
| **advisory** | `galileo_coherence` · `hallucination-signals` skill | akış · aşırı-kesinlik sinyali |
| **HARD (bölüm işi)** | `python3 scripts/eval/ch05_span_guard.py HEAD chapters/<bolum>.qmd` | dosyaya uygulandıysa git-referanslı span kontrolü |

Herhangi HARD/blocker = düzelt-ve-tekrar. KVKK: gateway'e yalnız manuskript/literatür
metni; katılımcı/ham/aile-düzeyi veri **asla**.

## Adım 5 — Onaya sun (dosyaya doğrudan yazma)

Sunum paketi:
1. **Diff** (eski → yeni), pasaj bazında.
2. **Guard raporu**: HARD boş; SOFT satırları + her biri için gerekçe.
3. **Ritim tablosu**: kaynak vs aday (`cv`, `B`, kısa/uzun pay, klişe/1000, MATTR).
4. **Anlamsal öz beyanı**: "yön, kapsam, koşul, atfetme, kesinlik derecesi
   değişmedi" — hangi cümlede neye dikkat edildiğiyle.
5. **Aday yazar notları** (varsa) + gereken atıf kapısı uyarısı.

**Açık kullanıcı onayı olmadan Edit/commit yok.** Onay sonrası: düzenle →
`ch05_span_guard.py` (ya da ilgili bölüm için `guard`) → bölüm kapanıyorsa
`/tez-dogrulama`.

## Sık yapılan üç ölümcül hata (kaçın)

1. **Eşanlamlıyla perplexity avı.** "Anlamlı" → "manidar", "ortanca" → "medyan"
   yapıldığı an terim kapısı ve okur birlikte kaybedilir. Ritmi değiştir, terimi değil.
2. **Çekinceyi "akıcılık" adına düşürmek.** "Kesitsel olduğundan nedensellik
   çıkarılamaz" cümlesi bir üslup fazlalığı değil, bulgunun kapsamıdır; düşerse
   bulgu değişmiş olur (guard HARD verir).
3. **Sadeleştirmeyi insansılaştırma sanmak.** Jüri için sadeleştirme ayrı kapıdır
   (`klinisyen-diline-uyarlama`); bu kapı **karmaşıklığı korur**, tekdüzeliği kırar.

## Referanslar

- `references/dokunulmazlik-envanteri.md` — 12 sözel sınıf + anlamsal öz kontrol listesi
- `references/llm-imza-kaliplari.md` — Türkçe LLM klişe haritası ve güvenli karşılıkları
- `references/ritim-muhendisligi.md` — burstiness kalıpları, hedef metrikler, şablonlar
- `references/kaynak-dogrulama.md` — doğrulama + kapı komut kalıpları, KVKK sınırı
- `references/ornek-insansilastirma.md` — uçtan uca çözümlü örnek (öncesi/sonrası/rapor)
