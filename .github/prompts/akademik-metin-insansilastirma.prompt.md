---
description: 'Yapay zeka nesrini ÖZE HİÇ DOKUNMADAN insansılaştırır (cümle ritmi/klişe/paragraf mimarisi/ses); sayı-istatistik-atıf-çekince-kapsam DOKUNULMAZ ve mekanik bekçiyle zorlanır; kapıdan geçirip onaya sunar (dosyaya doğrudan yazmaz)'
mode: agent
---

# /akademik-metin-insansilastirma — İnsansılaştırma Kapısı (Copilot ikizi)

İnsansılaştırılacak metin: **${input:hedef:seçili metin veya chapters/<bolum>.qmd konumu}** — boşsa editör seçimini kullan.

Bu prompt, Claude komutu [.claude/commands/akademik-metin-insansilastirma.md](../../.claude/commands/akademik-metin-insansilastirma.md)
ve skill [.claude/skills/akademik-metin-insansilastirma/SKILL.md](../../.claude/skills/akademik-metin-insansilastirma/SKILL.md)
ile **aynı doktrinin** Copilot/VS Code ikizidir; üçü de bu işte **bağlayıcıdır**. Skill'in beş
referansını (`dokunulmazlik-envanteri.md`, `llm-imza-kaliplari.md`, `ritim-muhendisligi.md`,
`kaynak-dogrulama.md`, `ornek-insansilastirma.md`) oku.

## EN SIKI KRİTER — öz dokunulmazdır

> **Hiçbir bilginin, verinin, referansın, iddianın ÖZÜ değişmez.** Sayı · oran · p ·
> güven aralığı · etki büyüklüğü · örneklem ve analiz birimi · bulgu yönü · anlamlılık ·
> koşul/kapsam öbeği · kesinlik derecesi (kip) · nedensellik derecesi · çekince ·
> kanıt-düzeyi etiketi (`[KEŞİFSEL]`) · atıf anahtarı · `@tbl-*`/`@fig-*`/`§` ·
> kimin neyi iddia ettiği — **düşemez, mutasyona uğrayamaz, yuvarlanamaz, eklenemez,
> güçlendirilemez, zayıflatılamaz.** Ondalık virgül (`0,38`) da özün parçasıdır.

Bu sözleşme retorik değil **mekaniktir**: `scripts/eval/humanize_invariant_guard.py`
12 sınıfı çokluk sayımıyla karşılaştırır; HARD ihlalde **override yoktur**.

## Yürütme (sıra sabittir)

1. **Adım 0 — doğrula + envanter (atlanamaz).** Pasajın gerçek dosya:satırını
   `grep -rn "<parça>" chapters/` ile bul — **dosya adı tahmin etme**. Sonra:
   ```bash
   python3 scripts/eval/humanize_invariant_guard.py inventory chapters/<bolum>.qmd
   ```
   Üstüne **anlamsal öz notunu** elle ekle: yön · kapsam · koşul · kip/kesinlik ·
   nedensellik · atfetme · örneklem birimi · çekincenin bağlandığı bulgu. Sayıları
   üreten artefakttan teyit et (gömülü literal yok — AGENTS.md sayısal bütünlük
   kaideleri). Metin↔artefakt çelişkisi varsa **yazma, çelişkiyi bildir**.
2. **Adım 1 — teşhis (ölçüm önce, yazım sonra).**
   `python3 scripts/eval/humanize_invariant_guard.py metrics <dosya>` →
   `cv` (hedef ≥ 0,40) · `B` · kısa/uzun cümle payı (≥ 0,10) · `max_uniform_run` (≤ 4) ·
   `cliche_per_1000` (≤ 2,0) · `connective_start_ratio` (≤ 0,25) · `MATTR` (≥ 0,60).
   Not: `max_uniform_run` sınırı ve `MATTR` metin uzunluğuna göre normalize edilmiştir;
   ham `TTR` uzun bölümlerde mekanik düşer, eşik ölçütü değildir.
   Hangi katmanın öncelikli olduğunu bu çıktı belirler.
3. **Adım 2 — SEN yaz (otomatik eşanlamlı motoru YASAK).** Katman sırası sabittir:
   **A** cümle ritmi (5–8 sözcüklük tez cümlesi + 28–40 sözcüklük analitik cümle;
   zinciri kır, cılızları birleştir, bilgi sırasını değiştir) → **B** paragraf mimarisi
   ("konu→3 destek→özet" şablonunu kır, uzunlukları dalgalandır) → **C** sözcük
   (klişeyi **sil**, yerine eşanlamlı koyma) → **D** ses/derinlik (var olan kanıtın
   yorumu; **yeni kanıt/sayı/atıf yok**).
   **Değişmeyecekler:** kanonik terim (`docs/tez-kilavuz/terim-sozlugu.yaml`), ölçek ve
   alt ölçek adları, tanı adları, yöntem adları, grup/değişken adları, rol adları
   (eş ≠ partner ≠ ebeveyn). **Yasak:** bağlamsız parafraz motoru, zorlama nadir sözcük,
   görünmez karakter/homoglif/sıfır-genişlik. Gerçek boşluk varsa `[Yazar notu: …]`
   bırak; kaynak uydurma (yeni atıf gerekiyorsa önce [referans-kapisi.prompt.md](referans-kapisi.prompt.md)).
4. **Adım 3 — mekanik kapı, UYGULAMADAN ÖNCE.** Aday metni geçici dosyaya yaz:
   ```bash
   python3 scripts/eval/humanize_invariant_guard.py all \
     --source /tmp/kaynak_pasaj.md --candidate /tmp/aday_pasaj.md
   ```
   | Çıktı | Karar |
   |---|---|
   | `HARD İHLAL` (düşme · mutasyon · uydurma · kesinlik enflasyonu) | **override yok** — düzelt-ve-tekrar |
   | `SOFT` (yön/atıf-bloğu/çekince eklemesi) | her satır tek tek gerekçelendirilir |
   | `ÜSLUP HEDEFİ` bulgusu | Katman A–C'ye dön |
   | exit 0 | Adım 4 |

   Guard PASS'i **gerekli ama yeterli değildir**: eklenen abartıyı, kayan atfetmeyi,
   kapsam genişlemesini sen okuyarak denetlersin.
5. **Adım 4 — kapılar (araçları karıştırma).**

   | Kademe | Copilot ortamı aracı | Rol |
   |---|---|---|
   | **HARD** | `python3 scripts/eval/humanize_invariant_guard.py guard …` | Öz dokunulmazlığı (12 sınıf) |
   | **HARD** | `python3 scripts/util/tr_corpus_audit.py all --fail-on blocker` + `tez_checklist_verify.py --fast` | Türkçe imla + ondalık virgül (nokta-`p` = blocker) |
   | **HARD** | `python3 scripts/util/terim_tutarlilik_audit.py` | Kanonik terim kayması (eşanlamlı sızıntısı) |
   | **HARD** | `citation-forensics` skill + `python3 scripts/util/bib_hygiene.py all` | Axis A atıf bütünlüğü |
   | **HARD** | `stats-forensics` + `claim-grounding` skilleri + `claim_certification.py` + `csr_causal_label_audit.py` | Axis B/C iddia + nedensellik etiketi |
   | **HARD** | `turkish-sci-style` skill (`tr_sciaudit.py <dosya> --strictness certification`) | Axis G |
   | **SOFT-block** | `galileo-audit` MCP `galileo_judge` (`text`=aday, `evidence`=**kaynak pasaj**) | faithfulness/groundedness — anlamsal öz kayması |
   | **advisory** | `galileo_coherence` · `hallucination-signals` skill | akış · aşırı-kesinlik sinyali |

   HARD = override yok. SOFT-block eşikleri [.claude/galileo.local.md](../../.claude/galileo.local.md).
6. **Adım 5 — onaya sun.** (a) diff (eski→yeni), (b) guard raporu (HARD 0 · SOFT +
   gerekçe), (c) ritim tablosu (kaynak↔aday: cv, B, kısa/uzun, klişe/1000, MATTR),
   (d) **anlamsal öz beyanı** (yön/kapsam/koşul/kesinlik/atfetme değişmedi — hangi
   cümlede neye dikkat edildi), (e) yazar notları. **Açık kullanıcı onayı olmadan
   Edit/commit yok.**
7. **Onay sonrası.** Düzenle → `python3 scripts/eval/ch05_span_guard.py HEAD chapters/<bolum>.qmd`
   → Bulgular yeniden sıralandıysa `csr_numeric_trace_audit.py` + tam `tar_make()` →
   bölüm kapanıyorsa [tez-dogrulama.prompt.md](tez-dogrulama.prompt.md).

## Dürüstlük ve kapsam sınırı

- **YZ-kullanım beyanı silinmez/gizlenmez** — guard `yz_beyani` sınıfında HARD izler;
  kurumsal/ICMJE beyan yükümlülüğü üslup düzeltmesiyle ortadan kalkmaz.
- **Dedektör skoru kabul ölçütü değildir** (yanlış-pozitif oranı yüksek, sürüm-bağımlı);
  kabul ölçütü guard + repo kapılarıdır. Metin üçüncü taraf dedektör/humanizer servisine
  **yüklenmez** (dışa aktarım + KVKK).
- **KVKK:** gateway'e yalnız manuskript/literatür metni; katılımcı/ham/aile-düzeyi veri
  asla. Guard `data/raw|identified|cleaned|backup` ve `_targets/` yollarını reddeder.
- **Bu kapı sadeleştirme değildir** ([klinisyen-diline-uyarlama](klinisyen-diline-uyarlama.prompt.md)),
  literatür zenginleştirme değildir ([anlatim-zenginligi](anlatim-zenginligi.prompt.md)),
  figür/tablo sunumu değildir ([veri-gosterimi-zenginligi](veri-gosterimi-zenginligi.prompt.md)),
  ayrı açıklama üretimi değildir ([data-narrative](data-narrative.prompt.md)).
