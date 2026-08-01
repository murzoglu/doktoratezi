---
description: Yapay zeka nesrini ÖZE HİÇ DOKUNMADAN insansılaştırır (ritim/klişe/ses); DOKUNULMAZ envanteri mekanik bekçiyle zorlar, kapılardan geçirip onaya sunar
argument-hint: "[insansılaştırılacak metin — ör. chapters/05_tartisma_ve_sonuc.qmd pasajı / seçili taslak]"
allowed-tools: Bash(grep *), Bash(sed *), Bash(nl *), Bash(head *), Bash(awk *), Bash(python3 scripts/eval/humanize_invariant_guard.py*), Bash(python3 scripts/eval/ch05_span_guard.py*), Bash(python3 scripts/util/tr_corpus_audit.py*), Bash(python3 scripts/util/terim_tutarlilik_audit.py*), Bash(python3 scripts/util/bib_hygiene.py*), Bash(python3 scripts/util/claim_certification.py*), Bash(python3 scripts/util/csr_causal_label_audit.py*), Bash(python3 scripts/util/csr_numeric_trace_audit.py*), Read
---

<!--
İKİZ NOTU: Bu komutun Copilot karşılığı `.github/prompts/akademik-metin-insansilastirma.prompt.md`
dosyasıdır; ikisi `tests/test_claude_hooks.py::test_slash_command_twins_are_complete`
kapısıyla senkron tutulur. Politika değişirse iki dosya birlikte güncellenir.
-->

# /akademik-metin-insansilastirma — İnsansılaştırma Kapısı (üslup değişir, öz değişmez)

İnsansılaştırılacak metin: **$ARGUMENTS** — boşsa kullanıcıdan pasajı/konumu iste.

`akademik-metin-insansilastirma` skill'i
(`.claude/skills/akademik-metin-insansilastirma/SKILL.md`) bu işte **bağlayıcıdır**.
Skill'i ve beş referansını oku (`dokunulmazlik-envanteri.md`, `llm-imza-kaliplari.md`,
`ritim-muhendisligi.md`, `kaynak-dogrulama.md`, `ornek-insansilastirma.md`).

## En sıkı kriter (her şeyin üstünde)

> **Hiçbir bilginin, verinin, referansın, iddianın ÖZÜ değişmez.** Sayı · oran · p ·
> güven aralığı · etki büyüklüğü · örneklem/birim · bulgu yönü · anlamlılık · koşul ve
> kapsam · kesinlik derecesi · nedensellik derecesi · çekince · kanıt-düzeyi etiketi ·
> atıf anahtarı · çapraz-referans · kimin neyi iddia ettiği — **düşemez, mutasyona
> uğrayamaz, yuvarlanamaz, eklenemez, güçlendirilemez, zayıflatılamaz.**
> Bu bir temenni değil, `scripts/eval/humanize_invariant_guard.py` ile **mekanik**
> zorlanan bir sözleşmedir; HARD ihlalde override yoktur.

## Otomatik toplanan bağlam

```bash
head -45 .claude/skills/akademik-metin-insansilastirma/SKILL.md
python3 scripts/eval/humanize_invariant_guard.py --help 2>&1 | head -12
```

## Yürütme (sıra sabittir)

1. **Adım 0 — doğrula + envanter (atlanamaz).** Pasajın gerçek dosya:satırını
   `grep -rn` ile bul (dosya adı TAHMİN ETME).
   `python3 scripts/eval/humanize_invariant_guard.py inventory <dosya>` ile 12 sınıflık
   DOKUNULMAZ envanteri çıkar; üstüne **anlamsal öz notunu** elle ekle (yön · kapsam ·
   koşul · kip/kesinlik · nedensellik · atfetme · örneklem birimi · çekincenin yeri).
   Sayıları üreten artefakttan teyit et (gömülü literal yok). Metin↔artefakt çelişkisi
   varsa **yazma, çelişkiyi bildir**.
2. **Adım 1 — teşhis.** `metrics` ile kaynağı ölç: `cv`, `B`, kısa/uzun pay,
   `max_uniform_run` (sınırı raporda gözlenen/sınır çifti verir), `cliche_per_1000`,
   `connective_start_ratio`, `MATTR` (uzunluktan bağımsız çeşitlilik). Hangi katmanın
   (cümle / paragraf / sözcük) öncelikli olduğunu bu çıktı belirler; körlemesine yazma.
3. **Adım 2 — SEN yaz (otomatik eşanlamlı motoru YASAK).** Katman sırası sabit:
   **A** cümle ritmi (asimetri, böl-birleştir, bilgi sırası) → **B** paragraf mimarisi
   (şablon iskeleti kır, uzunluk dalgalandır) → **C** sözcük (klişeyi **sil**, yerine
   eşanlamlı koyma) → **D** ses/derinlik (var olan kanıtın yorumu; yeni kanıt yok).
   **Kanonik terim, ölçek/alt ölçek adı, tanı adı, yöntem adı, grup adı değişmez**
   (`docs/tez-kilavuz/terim-sozlugu.yaml`). Görünmez karakter/homoglif/sıfır-genişlik
   ekleme kesinlikle yasak. Gerçek boşluk varsa `[Yazar notu: …]` bırak, kaynak uydurma.
4. **Adım 3 — mekanik kapı (UYGULAMADAN ÖNCE).** Aday metni geçici dosyaya yaz:
   `python3 scripts/eval/humanize_invariant_guard.py all --source <kaynak> --candidate <aday>`.
   `HARD İHLAL` (düşme · mutasyon · uydurma · kesinlik enflasyonu) = **override yok**,
   düzelt-ve-tekrar. `SOFT` satırlarının **her biri** gerekçelendirilir. `ÜSLUP HEDEFİ`
   bulgusu varsa Katman A–C'ye dön. Guard PASS'i gerekli ama yeterli değildir; eklenen
   abartıyı/kapsam genişlemesini sen okuyarak denetlersin.
5. **Adım 4 — repo kapıları.** HARD: `tr_corpus_audit.py all --fail-on blocker` ·
   `terim_tutarlilik_audit.py` · `bib_hygiene.py all` · `claim_certification.py` ·
   `csr_causal_label_audit.py` · `turkish-sci-style` (certification).
   SOFT-block: `galileo_judge` (`text` = aday, `evidence` = **kaynak pasaj**).
   Advisory: `galileo_coherence`, `hallucination-signals`. Herhangi HARD/blocker =
   düzelt-ve-tekrar.
6. **Adım 5 — onaya sun.** (a) diff (eski→yeni), (b) guard raporu (HARD 0 · SOFT +
   gerekçe), (c) ritim tablosu (kaynak↔aday: cv, B, kısa/uzun, klişe/1000, MATTR),
   (d) **anlamsal öz beyanı** (yön/kapsam/koşul/kesinlik/atfetme değişmedi — hangi
   cümlede neye dikkat edildi), (e) yazar notları + gereken atıf kapısı uyarısı.
   **Açık kullanıcı onayı olmadan Edit/commit yok.**
7. **Onay sonrası.** Düzenle → `python3 scripts/eval/ch05_span_guard.py HEAD chapters/<bolum>.qmd`
   → Bulgular'da yeniden sıralama olduysa `csr_numeric_trace_audit.py` + tam `tar_make()`
   → bölüm kapanıyorsa `/tez-dogrulama`.

## Bağlayıcı sınırlar

- **Kelime salatası yasağı:** bağlam gözetmeyen eşanlamlı/parafraz motoru, zorlama nadir
  sözcük, görünmez karakter/homoglif kullanılmaz. Perplexity artışı **kurgudan** gelir.
- **YZ-kullanım beyanı silinmez/gizlenmez** (guard `yz_beyani` sınıfında HARD izler);
  kurumsal/ICMJE beyan yükümlülüğü üslup düzeltmesiyle ortadan kalkmaz.
- **Dedektör skoru kabul ölçütü değildir** (yanlış-pozitif oranı yüksektir); metin
  üçüncü taraf dedektör/humanizer servisine **yüklenmez** (dışa aktarım + KVKK).
- **KVKK:** gateway'e yalnız manuskript/literatür metni; katılımcı/ham/aile-düzeyi veri
  asla. Guard korumalı veri yollarını (`data/raw|identified|cleaned|backup`, `_targets/`)
  zaten reddeder.
- **Bu kapı sadeleştirme değildir** (`/klinisyen-diline-uyarlama`), literatür
  zenginleştirme değildir (`/anlatim-zenginligi`), figür/tablo sunumu değildir
  (`/veri-gosterimi-zenginligi`), ayrı açıklama üretimi değildir (`data-narrative`).
