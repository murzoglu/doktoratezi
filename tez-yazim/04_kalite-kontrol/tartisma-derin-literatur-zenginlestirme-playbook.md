# Tartışma Derin-Literatür Zenginleştirme Playbook'u

Sürüm: 1.0 · 2026-07-26

> **Konum ve amaç.** Bu playbook, **Tartışma ve Sonuç** bölümünün
> (`chapters/05_tartisma_ve_sonuc.qmd`) `/anlatim-zenginligi` kapısıyla
> işlenmesini, **en geniş kapsam ve derinlikte çok-yönlü kanıt analizi + tam-metin
> literatür tartışması** hedefiyle **aşama aşama** yönetir. Bulgular
> bölümünden farkı: Tartışma **yorum-yüklü** bir bölümdür — literatürle
> karşılaştırma, hipotez-destek beyanı ve tasarım-sınırlı çıkarım burada
> **gereklidir**. Bu playbook, `/anlatim-zenginligi` komutunun (`.claude/commands/`)
> yerine geçmez; onu Tartışma bağlamında **evidentia + Minerva + anamnesis +
> sci-audit + galileo (AI-judge)** araçlarıyla uçtan uca nasıl işleteceğimizi
> tanımlar. **Denetimlerde bu playbook'a harfiyen uyulur.**

## Otorite zinciri (çakışmada üstten alta)

1. `AGENTS.md` "Sayısal Bütünlük Kaideleri" — kanıt-değeri dokunulmazlığı, kaynak-tekilliği.
2. `tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md` **§4.1 Referans
   Bütünlük Şiarı (RBŞ)** — konstitüsyonel; her referans-entegrasyon kararında bağlayıcı.
3. `tez-yazim/00_kaynak-kurallari/` Marmara yazım sözleşmesi + `docs/tez-kilavuz/`
   (Tartışma bölüm sözleşmesi, §3.6 değil — Tartışma yorum içerir).
4. `.claude/commands/anlatim-zenginligi.md` — komut sözleşmesi (6 adım, üç-kademeli kapı).
5. `.claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md` — D0–D6 kaskad.
6. `.claude/galileo.local.md` — SOFT-block eşikleri (AI-judge).
7. Bu playbook — yürütme eşgüdümü (yukarıdakileri yeniden tanımlamaz, işletir).

## Kanıt-bölgesi sınır sözleşmesi (Tartışma'ya özgü)

| Öğe | Durum |
|---|---|
| Sayı/istatistik (g, β, SE, p, %GA, ICC, AUC, BF, N, %) | **DOKUNULMAZ** — aynen korunur; artefakttan okunur |
| Bulgunun içeriği / yönü / anlamlılığı / büyüklüğü / sırası | **DOKUNULMAZ** |
| `@tbl-*` / `@fig-*` / `[@key]` token'ları | **AYNEN korunur** |
| **Literatür yorumu + karşılaştırma** | **DÜZENLENİR** (Tartışma'nın işi budur) |
| **Hipotez-destek beyanı** (desteklendi/desteklenmedi/kısmen) | **DÜZENLENİR** — ama bulgu yönüyle bire bir tutarlı |
| **Tasarım-sınırlı çıkarım** (nedensellik dili) | **DÜZENLENİR** — olgu-kontrol/kesitsel sınırında tutulur |
| Yeni atıf | **ADAY** — `/referans-kapisi` `cite-ok` olmadan metne girmez |

**Bulgular'dan kritik ayrım:** Bulgular'da yorum-sızıntısı yasaktı (Marmara §3.6);
Tartışma'da yorum *beklenir*. Ancak yorum **bulgunun sayısını/yönünü değiştiremez**:
"anlamlı değildi" → "eğilim" yapılamaz; g'ye kaynakta olmayan "güçlü/klinik" etiketi
eklenemez; korelasyon "neden" yapılamaz. Yorum = bulgunun literatürdeki yerini
konumlama, sayının kendisini değil.

---

## Aşama aşama işlenecek Tartışma alt-blokları (bilgi-verici düzlem sırası)

Tartışma tek `#` başlık altında akıcı nesir + **bold-işaretçili tematik bloklar**
biçiminde yazılmıştır. İşleme sırası bölümün kendi mantık zincirini izler:
bilgi-verici düzlemleri → uyum/karma → keşifsel → ölçüm → sonuç. Her blok **tek
aşama** olarak ele alınır; bir aşama tam kapanmadan (Faz 0→5) sonrakine geçilmez.

| # | Aşama (blok) | Odak düzlem | Ağırlıklı hipotez |
|---|---|---|---|
| T1 | Çocuk algısı düzlemi (giriş + H1 desteklenme) | Çocuk-bildirimli EMBU-C | H1 |
| T2 | Anne öz-bildirimi düzlemi (H3 desteklenmeme) | Anne-bildirimli EMBU-P | H3 |
| T3 | Anne depresyonu aracılık yolu | Beck → ebeveynlik | H4 |
| T4 | Kardeş konumu | Kardeş ilişkisi (KİA/SRQ) | H2 |
| T5 | Anne–çocuk algı uyumu | Diadik konkordans | H5 |
| T6 | Karma bütünleştirme (nicel ↔ nitel) | Joint display | H1–H5 |
| T7 | **Aracılık zincirindeki kırılma** (bold) | Beck→reddetme→çıktı | keşifsel |
| T8 | **Dağılımın üst-ucundaki gizli sinyal** (bold) | kantil/floor | keşifsel |
| T9 | **Kişi-merkezli ebeveynlik tipolojisi** (bold, LPA) | latent profil | keşifsel |
| T10 | **Ağ yapısında grup farkı için kanıt yokluğu** (bold) | ağ analizi | keşifsel |
| T11 | **Ayrım gücü ile klinik fayda ayrışması** (bold) | ROC/DCA | keşifsel |
| T12 | **Ölçüm katmanı: latent etki + bifaktör anomalisi** (bold) | psikometri | keşifsel |
| T13 | **Robustluk katmanının işlevi** (bold) | duyarlılık | doğrulayıcı |
| T14 | **Kardeş mimarisi + algı uyumunun kaynağa özgülüğü** (bold) | kardeş/diadik | keşifsel |
| T15 | **Çocuk-düzeyi moderatörler + aşırı korumanın gradyanı** (bold) | moderatör | keşifsel |
| T16 | **Diyabet klinik ağırlığı ile ebeveynlik bağlantısızlığı** (bold) | klinik | keşifsel |
| T17 | Sınırlılıklar + Sonuç + gelecek yön | tüm bölüm | — |

> Blok sınırları `grep -nE '^\*\*[^*]+\*\*' chapters/05_tartisma_ve_sonuc.qmd`
> ile **her oturumda yeniden doğrulanır** (dosya değiştikçe satır kayar; hatırdan
> satır yazma). Bir oturumda 1–3 bitişik blok işlenebilir; fazlası kanıt-derinliğini
> zayıflatır.

---

## FAZ 0 — Kapsam ve tedbir kapısı (her aşama başında)

Amaç: aşamayı **doğru bağlama** oturtmak; kanıt-bölgesini sabitlemek.

1. **Bağlamı sabitle — dosya adı TAHMİN ETME.** İşlenecek bloğun gerçek satır
   aralığını `grep -n` ile bul. Bloğun hangi hipoteze/artefakta bağlı olduğunu
   (yukarıdaki T-tablosu) doğrula.
2. **Kaynak-tekilliği ön-teyidi:** blokta geçen her sayının artefakttan geldiğini
   doğrula (`python3 scripts/util/r_generator_literal_audit.py` PASS; gömülü literal yok).
3. **Kanıt-değeri envanteri:** blokta geçen tüm sayı/istatistik/`@tbl`/`@fig`/`[@key]`
   token'larını **liste hâlinde dondur** — bunlar aşama boyunca değişmeyecek referans setidir.
4. **t1dm-tez-rehberi Faz 0 + Faz 0.5 tedbir kapısı:** hipotez/SAP kısmı, veri
   çerçevesi, kanonik-kilit, OSF, PII sınırı. Kapı geçmezse **dur**.
5. **KVKK sınırı:** bu aşamada dış gateway'e (Minerva/anamnesis/galileo) yalnız
   **literatür terimi + manuskript metni** gider; ham satır/aile-düzeyi/transkript **asla**.

## FAZ 1 — Kaynak envanteri ve kanıt boşluğu haritası

Amaç: bloğun mevcut atıflarını çıkarıp **hangi iddianın hangi kaynağa bağlı,
hangi iddianın kaynaksız/zayıf** olduğunu haritalamak.

1. **Mevcut atıfları çıkar:** blok içi `[@key]` listesini topla; her birini
   `references-denetim-ledgeri.md`'de ara — `cite-ok` mu, hangi tam-metin kanıtına dayanıyor.
2. **İddia↔kaynak matrisi kur:** blokta yorum/karşılaştırma taşıyan her cümleyi
   listele; karşısına dayandığı kaynağı (veya "KAYNAKSIZ") yaz.
3. **Kanıt boşluğu tespiti:** güçlendirilmesi gereken iddialar (kaynaksız
   karşılaştırma, tek-cümle-alıntıya dayanan zayıf temellendirme, güncel
   meta-analizle teyit edilmemiş benchmark) → Faz 2 derin-literatür hedefleri.
4. **Yorum-disiplini ön-tarama:** blokta nedensellik-aşımı (`neden`, `yol açar`,
   `sağlar`) veya kaynaksız etki-etiketi (`güçlü`, `klinik açıdan`) var mı? Bunlar
   Faz 3'te ya kaynakla temellendirilecek ya tasarım-sınırına çekilecek.

---

## FAZ 2 — RBŞ tam-metin derin literatür protokolü (playbook'un kalbi)

> **Konstitüsyonel kural (RBŞ §4.1):** Bir referanstan zenginleştirme yaparken
> makalenin **bir parçasını değil tamamını geniş bağlamda semantik olarak kavra**,
> bu bağlamı **rafine ederek** revize et; **hem kaynağın hem tez metninin somut
> bilimsel iddialarını çarpıtma.** Tek çekilmiş cümleden zenginleştirme =
> cherry-pick = çarpıtma. Bu faz, RBŞ'yi araç-adımlarına döker.

Bu faz Faz 1'de tespit edilen **her kanıt boşluğu** ve **her güçlendirilecek
iddia** için ayrı ayrı koşulur. Amaç token tasarrufu değil **kanıt doygunluğu**dur.

### 2.0 Araç yığını (oturum başında sağlık kontrolü)

```bash
python3 scripts/mcp/audit_stack_healthcheck.py     # MINERVA/GALILEO/SCI-AUDIT/ANAMNESIS/CLAIM-CERT
```

Beşi de PASS değilse eksik aracın devrede olduğu adımı **atlamadan** dur ve raporla.

| Araç | Erişim (Ona exec) | Fazdaki rolü |
|---|---|---|
| **evidentia** (D0–D6 kaskad) | `/evidentia:*` (Claude Code) / connector MCP'leri | Bibliyografik + semantik geniş tarama, çapraz-doğrulama |
| **Minerva** (Roche korpus) | `python3 scripts/mcp/mcp_tool_call.py minerva <araç> '<json>'` | D2 semantik arama + D4 tam-metin (`_fulltext_by_doi`, annas ÖNCESİ) |
| **anamnesis** (GraphRAG) | `scripts/mcp/anamnesis_ingest.py` + `graphrag_query.py` | Tam-metni ingest → chunk-alıntı (verbatim kopya YOK; telif) |
| **galileo** (AI-judge) | `python3 scripts/mcp/mcp_tool_call.py galileo <araç> -` | `claim_source_match` (iddia↔kaynak groundedness) |
| **sci-audit** (HARD) | plugin cache `python3 .../scripts/*.py` | Faz 4 kapısı (burada değil) |

### 2.1 Sorgu ayrıştırma (evidentia D0.4)

Kanıt boşluğunu facet'lere böl: **popülasyon** (`child/adolescent type 1
diabetes`), **yapı** (`parenting`, `overprotection`, `rejection`, `EMBU`,
`maternal depression`, `sibling relationship`, `dyadic concordance`), **sonuç**
(`adjustment`, `internalizing`, `glycemic control`), **yöntem** (`meta-analysis`,
`validation`, `dyadic`, `multi-informant`), **coğrafya** (`Turkey`, `Turkish sample`).
Dar / geniş / lateral / ölçüm-odaklı / Türkiye-odaklı **varyantları ayrı** çalıştır.

### 2.2 Bibliyografik + semantik geniş tarama (D1–D2)

- **evidentia connector'ları:** PubMed/EPMC, OpenAlex, Semantic Scholar, Paper
  Search, PsyArXiv/OSF (psikoloji sinyali), YÖK Tez (`yoktez-mcp`, TR bağlam).
  ERIC yalnız eğitim/okul/gelişim sinyalinde; ClinicalTrials yalnız müdahale sinyalinde.
- **Minerva D2 semantik booster** (Türkçe sorgu = `mode:semantic` **zorunlu**;
  İngilizce = hibrit):
  ```bash
  python3 scripts/mcp/mcp_tool_call.py minerva minerva_literature_search \
    '{"query":"type 1 diabetes maternal depression child-reported parenting","mode":"hybrid","top_k":8}'
  ```
- **Semantik genişletme:** seminal makalelerin cited-by/reference ağı, MeSH/concept
  varyantları, ölçek-aracı adları. İlk sonuçlarla yetinme (D2 kuralı).

### 2.3 Eleme, rerank, transfer matrisi (D3)

Adayları etiketle: çalışma tipi (meta-analiz > sistematik derleme > T1DM-özgül
primer > validation > tez), popülasyon yaşı, **T1DM özgüllüğü**, ölçüm aracı
(EMBU/PARI/CDI…), ülke, tarih. **Transfer riski** değerlendir: kaynağın ölçümü/
popülasyonu bu tezin iddiasına gerçekten transfer edilebilir mi? Eski ama seminal
kaynağı sadece tarih nedeniyle düşürme; benchmark/prior için meta-analizi önceliklendir.

### 2.4 Tam metin + bütünsel kavrama (D4 — RBŞ çekirdeği)

**Her kullanılacak kaynak için** (Faz 1'de güçlendirilecek iddiaya bağlı):

1. **Kimlik doğrula:** DOI/PMID/PMCID (PubMed/OpenAlex).
2. **Tam-metin kaskadı** (sıra sabittir):
   PMC/OA → OpenAthens (lisanslı) → **Minerva** (`minerva_literature_fulltext_by_doi`,
   annas ÖNCESİ) → annas-reader (son çare). Deterministik yardımcı:
   ```bash
   python3 scripts/mcp/fulltext_cascade.py --doi <DOI> --title "..."
   ```
3. **anamnesis'e ingest → hybrid_query ile chunk-alıntıla** (verbatim toplu kopya
   YOK — telif; KVKK: yalnız DOI/başlık gider):
   ```bash
   python3 scripts/mcp/anamnesis_ingest.py --doi <DOI>          # tam metni ingest
   python3 scripts/mcp/graphrag_query.py "<iddia sorgusu>"       # hybrid + graph + füzyon
   ```
4. **BÜTÜNSEL KAVRAMA (RBŞ zorunlu):** Kaynağı kullanmadan önce **amaç / yöntem /
   örneklem / ana-iddia / koşul-kısıt / temkin** ekseninde tam metnini özümse.
   Zenginleştirmeyi bu **bütün-makale** anlayışından türet — tek çekilmiş cümleden
   değil. Kaynağın somut bilimsel iddiasını **kapsam + koşuluyla** temsil et
   (ör. "diyabette daha zayıf", "çocuk-bildiriminde tutarsız"); düzleştirme /
   abartma / olduğundan-uyumlu gösterme **yok**; uyumsuz kanıt "uyumlu"ya çevrilmez.

### 2.5 Çapraz-doğrulama (D5)

Çelişki, terminoloji ve transfer riskini çöz: aynı iddiayı destekleyen/çelişen
kaynakları karşılaştır; `claim_ledger` güven düzeyi belirle. Çelişkili kanıt
varsa **iki yönü de** Tartışma'da temsil et (tek yönü seçme = cherry-pick).

### 2.6 Faz 2 çıktısı (Faz 3'e devredilen paket)

Her güçlendirilecek iddia için:
- **claim_ledger satırı:** iddia → kaynak(lar) → tam-metin lokatörü → kapsam/koşul
  notu → güven düzeyi → çelişki notu.
- **Yeni kaynak adayları:** `references.bib`'de olmayanlar → Faz 3 öncesi
  `/referans-kapisi` (7-adım) kuyruğuna alınır; `cite-ok` olmadan metne girmez.
- **KVKK teyidi:** gateway'e yalnız literatür terimi gitti; ham veri sızmadı.

---

## FAZ 3 — Çok-yönlü kanıt analizi + Türkçe revizyon (aday, dosyaya yazmadan)

Amaç: Faz 2'nin bütünsel-kavranmış kanıtını, bloğun **bilgi-verici düzlem
mantığına** oturan, çok-yönlü ve derinlikli bir Tartışma nesrine dönüştürmek —
**kanıt-değeri dokunulmadan**. Revizyon **önizleme parçasına** yazılır; chapter
dosyasına Faz 5 onayından önce dokunulmaz.

### 3.1 Çok-yönlü kanıt sentezi (tek yön değil)

Her güçlendirilen iddia için Tartışma nesri şu yönleri **birlikte** taşır:

1. **Uyum ekseni:** bu çalışmanın bulgusu hangi kaynak(lar)la aynı yönde?
   (ör. "bu çalışmanın çocuk-bildirimli reddetme farkı [iç], Pinquart 2013
   meta-analizi [dış] ile uyumludur").
2. **Ayrışma/çelişki ekseni:** hangi kaynak farklı yön/büyüklük buluyor? **Neden**
   (popülasyon, ölçüm, bilgi-verici düzlemi, tasarım)? Çelişki gizlenmez, açıklanır.
3. **Koşul/kapsam ekseni:** kaynak kendi sınırıyla aktarılır ("diyabette daha
   zayıf", "yalnız ergen örnekleminde", "çocuk-bildiriminde tutarsız").
4. **Mekanizma-hipotezi ekseni:** kesitsel tasarımda mekanizma **iddia edilmez**,
   yalnız **hipotez düzeyinde** önerilir ("mekanizma değil hipotez düzeyinde okunmalıdır").
5. **Katkı ekseni:** bu çalışmanın özgün katkısı (ör. çok-bilgi-verici düzlem
   haritası, diadik konkordans ölçümü) literatürdeki boşluğa göre konumlanır.

### 3.2 Türkçe revizyon kuralları (Marmara sözleşmesi)

- **Pasif 3. tekil**; **ondalık virgül** (`0,38`, `p<0,001`).
- **Teknik terim ilk geçişte:** tam ad + parantezde kısaltma/özgün karşılık.
- **`[@key]` / `@tbl-*` / `@fig-*` token'ları, tüm sayı/istatistik ve bulgunun
  içeriği/yönü/anlamlılığı/sırası AYNEN korunur.**
- **Hipotez-destek beyanı** bulgu yönüyle bire bir: "H1 desteklenmiştir" yalnız
  bulgu öyleyse; "kısmen desteklenmiştir" yalnız bulgu kısmiyse. Yumuşatma/güçlendirme yok.
- Nesir kalitesi: `tez-yazim/04_kalite-kontrol/insan-turkcesi-retorik-playbook.md`
  (şablon geçiş cümlesi, reporting-verb monotonluğu, cümle uzunluğu).

### 3.3 Kırmızı bayraklar (bulgu mutasyonu → aday'dan çıkar)

- Kaynakta olmayan aktör ekleme (ör. sonucu "anneden" diye niteleme, kaynak öyle demiyorsa).
- g/β/r'ye kaynakta olmayan büyüklük etiketi ("küçük/orta/güçlü") ekleme — metrik
  **tanımı** izah edilebilir, ama **bu** sonucun büyüklük yargısı kaynakta yoksa etiketlenmez.
- "anlamlı değildi" → "eğilim/kısmen" yumuşatma; korelasyonu "neden" yapma.
- Bulgu cümlelerini birleştirme veya sırasını değiştirme.
- Uyumsuz kaynağı "uyumlu" gösterme; çelişkiyi gizleme (RBŞ ihlali).

### 3.4 Yeni atıf = ADAY (uydurma YASAK)

Faz 2'de çıkan yeni kaynaklar bir "öneri" bloğunda listelenir; revizyon
uygulanmadan **önce** `/referans-kapisi` (7-adım: DOI → tam-metin → Zotero →
claim → ledger → iki-kol AI → `cite-ok`) tamamlanır. Kapı kapanmadan hiçbir atıf metne girmez.

---

## FAZ 4 — Üç-kademeli denetim kapısı (UYGULAMADAN ÖNCE)

> **Sıra sabittir:** aday revizyon önce **sci-audit (HARD)**, sonra **galileo
> (SOFT-block + AI-judge)**, sonra **advisory**'den geçer. Denetimi render/onay
> sonrasına **ERTELEME** — kapı onaydan öncedir. Kademeler birbirinin yerine
> geçmez; sci-audit HARD **atlanamaz** ve override edilemez.

Aday revizyonu bir önizleme dosyasına yaz (ör. `/tmp/tartisma_<blok>_aday.md`),
denetimleri **o parça üzerinde** koştur.

### Kademe 1 — sci-audit (HARD; override YOK)

`<sürüm>` = `ls ~/.claude/plugins/cache/cureonics-marketplace/sci-audit/` ile doğrula.

| Eksen | Komut | Blocker koşulu |
|---|---|---|
| **G** Türkçe imla + ondalık-virgül | `python3 .../turkish-sci-style/scripts/tr_sciaudit.py <aday>` | `Errors (blocker): 0` değilse FAIL (nokta-`p` = blocker) |
| **C** İstatistik tutarlılık | `python3 .../stats-forensics/scripts/stats_forensics.py <aday>` | JSON `counts.error > 0` = FAIL |
| **A/B** Citation/claim bütünlüğü | `python3 .../claim-grounding/scripts/claim_grounding.py <aday>` + `python3 scripts/util/bib_hygiene.py reconcile` | HARD undefined > 0 = FAIL |

Ek zorunlu HARD (Tartışma'ya özgü):
```bash
python3 scripts/util/r_generator_literal_audit.py          # K5-LIT: literal=0
python3 scripts/util/karma_ledger_check.py                 # nicel↔nitel karma iddia tutarlılığı
```
Herhangi HARD bulgu = **düzelt-ve-tekrar**; onaya çıkma.

### Kademe 2 — galileo (SOFT-block + AI-judge; insan-override'lı)

Payload alanı **`text`** (kritik); eşikler `.claude/galileo.local.md`.

```bash
# Revize metnin bütünsel yargısı (faithfulness/groundedness/marmara/hallucination)
echo '{"text":"<aday nesir>","section_type":"discussion"}' \
  | python3 scripts/mcp/mcp_tool_call.py galileo galileo_judge -

# Her güçlendirilen/yeni iddia ↔ kaynağı temellendirme (RBŞ sadakat teyidi)
echo '{"claim":"<iddia>","source_text":"<kaynak chunk>"}' \
  | python3 scripts/mcp/mcp_tool_call.py galileo galileo_claim_source_match -
```

| Sinyal | Eşik (SOFT-block) | Anlam |
|---|---|---|
| `faithfulness` | < 0,60 | metin kaynağa sadık değil → düzelt |
| `groundedness` | < 0,60 | iddia temellenmemiş → kaynak ekle/çek |
| `citation_support` | `unsupported` (nicel iddia) | atıf desteği yok → `/referans-kapisi` |
| `harking` / `overclaim` | < 0,60 | sonradan-hipotez / aşırı-iddia riski |

> **Tartışma notu:** groundedness/marmara skorları **izole** parça denetiminde
> düşük çıkabilir (bağlam kopması artefaktı, ~0,34–0,42). Bu durumda skoru
> **tam-bölüm bağlamıyla** yeniden koştur veya `evidence` alanına Faz 2 kaynak
> chunk'larını ekleyerek teyit et; artefaktsa sertifikada belgelenir.

### Kademe 3 — advisory (bloklamaz; kalite sinyali)

```bash
echo '{"sections":[{"id":"tartisma-<blok>","text":"<aday>"}]}' \
  | python3 scripts/mcp/mcp_tool_call.py galileo galileo_reference_prose -   # atıf yoğunluğu, reporting-verb monotonluğu
echo '{"text":"<aday>"}' \
  | python3 scripts/mcp/mcp_tool_call.py galileo galileo_coherence -          # paragraf akışı, tekrar
```

Tartışma için özellikle: **atıf yoğunluğu/1k-kelime** makul mü (sıfır-atıf blok =
substantif boşluk sinyali); reporting-verb tekdüzeliği ("bulunmuştur…bulunmuştur")
kırıldı mı.

### Faz 4 çıktısı — kapı özeti

Tablo hâlinde: her kademe (HARD/SOFT/advisory) × her araç × sonuç (PASS/FAIL/skor).
Herhangi HARD FAIL veya override edilmemiş SOFT-block varken **onaya çıkılmaz**.

---

## FAZ 5 — Onay, Edit ve kapanış doğrulama

### 5.1 Onaya sun (dosyaya yazmadan)

Kullanıcıya üç şeyi birlikte sun:
1. **Diff** (eski → yeni), kanıt-bölgesinin değişmediği vurgulanır.
2. **Kapı özeti** — Faz 4 tablosu (HARD/SOFT/advisory + galileo skorları).
3. **Aday atıflar + `/referans-kapisi` durumu** (`cite-ok` / beklemede).

**Açık kullanıcı onayı olmadan Edit/commit yok.** (Drift/betim gerektiren her
karar `ask_clarifying_questions` ile onaylanır — Bulgular protokolüyle aynı.)

### 5.2 Onay sonrası Edit + kapanış

```bash
# Edit uygulandıktan sonra bölüm kapanış denetimi:
python3 .../turkish-sci-style/scripts/tr_sciaudit.py chapters/05_tartisma_ve_sonuc.qmd
python3 .../stats-forensics/scripts/stats_forensics.py chapters/05_tartisma_ve_sonuc.qmd
python3 scripts/util/bib_hygiene.py reconcile --chapters chapters/05_tartisma_ve_sonuc.qmd
python3 scripts/util/karma_ledger_check.py
```

Yeni atıf metne girdiyse **tam senkron**: model/veri değişmese de bib/render
etkilendiyse `tar_make()` çalıştır, `tar_outdated()` = 0 teyit et. Bölüm bütünü
kapanıyorsa `/tez-dogrulama` (kapanış doğrulama paketi) koş.

### 5.3 Bölüm kapanışı → sertifikasyon

Tüm bloklar (T1–T17) Faz 0–5'ten geçtikten sonra bölüm bütünü için
`/bolum-sertifika chapters/05_tartisma_ve_sonuc.qmd` (Kapı 0–5). **`certified-final`
yalnız kullanıcının açık onayıyla** (öz-sertifikasyon yasak; azami `provisional-pass`).

---

## Aşama-aşama ilerleme çizelgesi (denetim izi)

Her blok için bu satır doldurulur; **denetimde bu çizelgeye bakılır**:

| Blok | Faz 0 kapsam | Faz 1 boşluk | Faz 2 tam-metin (kaynak sayısı) | Faz 3 aday | Faz 4 HARD | Faz 4 galileo | Faz 5 onay | Durum |
|---|---|---|---|---|---|---|---|---|
| T1 Çocuk algısı |  |  |  |  |  |  |  | pending |
| T2 Anne öz-bildirim |  |  |  |  |  |  |  | pending |
| T3 Anne depresyonu |  |  |  |  |  |  |  | pending |
| T4 Kardeş |  |  |  |  |  |  |  | pending |
| T5 Algı uyumu |  |  |  |  |  |  |  | pending |
| T6 Karma |  |  |  |  |  |  |  | pending |
| T7–T16 keşifsel bloklar |  |  |  |  |  |  |  | pending |
| T17 Sınırlılıklar/Sonuç |  |  |  |  |  |  |  | pending |

> Bu tablo playbook'un **canlı kaydı değildir** (şablondur); her oturumda todo
> sistemi + kapı özetleri gerçek izi tutar. Bir blok "Durum = done" olmadan
> sonraki bloğa geçme kuralı bağlayıcıdır.

---

## Devir kararları (hangi görev hangi kapıya)

| Görev | Doğru kapı |
|---|---|
| Bloğu literatürle derinlemesine konumlama | **bu playbook** (`/anlatim-zenginligi` + Faz 2) |
| Geniş narratif derin-lit sentezi (tek konu) | `/tez-literatur tartisma <konu>` |
| Yeni referans yerleştirme | `/referans-kapisi` (7-adım) |
| Gerçek sistematik/kapsam derleme (PRISMA) | `/evidentia:evidentia` |
| Bir tablo/figür değeri yanlış aktarılıyor | `/veri-gosterimi-zenginligi` (kaynağa hizala) |
| Yeni sayı/analiz gerek | **hiçbiri** — pipeline (`_targets.R` + `R/`) |
| Bölüm finalizasyonu | `/bolum-sertifika` (Kapı 0–5) |

## Master checklist ID eşlemesi

`tez-yazim/04_kalite-kontrol/tez-kontrol-checklisti.md` · otomasyon
`scripts/util/tez_checklist_verify.py`:

| Faz kontrolü | Checklist ID |
|---|---|
| Kaynak-tekilliği (literal=0) | K5-LIT-01 |
| Sayı↔artefakt izi | K5-NUM-03 |
| Türkçe imla (axis G) | K4-* (sci-audit G) |
| İstatistik tutarlılık (axis C) | K5-* (sci-audit C) |
| Citation bütünlüğü (axis A/B) | K1/K2-* (bib_hygiene + claim-grounding) |
| Karma iddia tutarlılığı | karma_ledger_check |
| Referans bütünlüğü (RBŞ) | talimatname §4.1 (konstitüsyonel) |

## Bağlayıcı kurallar (çiğnenmez)

- **Kanıt-değeri DOKUNULMAZ.** Sayı/istatistik ve bulgunun içeriği/yönü/
  anlamlılığı/büyüklüğü/sırası aynen kalır; yeniden-yorum, yuvarlama, güçlendirme
  yok. Tartışma yorumu bulgunun **yerini** konumlar, **değerini** değil.
- **RBŞ (§4.1) konstitüsyonel:** her kaynak tam metniyle bütünsel-semantik
  kavranır; cherry-pick = çarpıtma; kaynak kendi kapsam+koşuluyla aktarılır;
  uyumsuz kanıt "uyumlu"ya çevrilmez; çelişki gizlenmez.
- **Kanıt doygunluğu > token tasarrufu.** Ciddi iddia için D1'de durma; D2 semantik
  genişletme + D4 tam-metin + D5 çapraz-doğrulama varsayılan.
- **sci-audit (HARD) atlanamaz;** `tez_checklist_verify` onun, `galileo` da
  sci-audit'in **yerine geçmez** — üçü ayrı kademedir.
- **Denetim onaydan öncedir** (erteleme yok); onaysız Edit/commit yok.
- **Uydurma referans/sayı yok** — sayı artefakttan, atıf `/referans-kapisi`'ndan.
- **KVKK:** dış gateway'e (Minerva/anamnesis/galileo) yalnız literatür terimi +
  manuskript metni; ham/katılımcı/aile-düzeyi/transkript **asla**.
- **Aşama disiplini:** bir blok Faz 0→5 tam kapanmadan sonrakine geçilmez;
  `certified-final` yalnız açık kullanıcı onayıyla.

## Bağlama (cross-reference)

- Kardeş playbook (Bulgular): `bulgular-zenginlestirme-esgudum-playbook.md`.
- Komut sözleşmeleri: `.claude/commands/{anlatim-zenginligi,tez-literatur,referans-kapisi,bolum-sertifika}.md`.
- Kaskad doktrini: `.claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md`.
- AI-judge eşikleri: `.claude/galileo.local.md`.
- MCP köprü erişimi: `scripts/mcp/README.md`.
- Denetim doktrini: `.claude/skills/t1dm-tez-rehberi/references/manuskript-denetimi-sciaudit.md`.
