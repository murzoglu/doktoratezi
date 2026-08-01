# KAYNAK DOĞRULAMA VE KAPI KOMUTLARI

Bu kapı hiçbir zaman "hafızadan" çalışmaz. Önce pasajın gerçek yerini ve sayıların
gerçek kaynağını doğrula; sonra yaz; sonra kapılardan geçir; en sonda onaya sun.

---

## 1. Pasajı bul (dosya adı TAHMİN ETME)

```bash
# özgün 5-8 kelimelik parçayla ara
grep -rn "duygusal sıcaklık ile depresyon" chapters/

# bölüm bağlamını oku (satır aralığı)
sed -n '120,175p' chapters/04_bulgular.qmd
```

Pasaj bir `.qmd` içindeyse **satır numarasını not et**; onay sonrası düzenleme ve
`ch05_span_guard.py` kontrolü buna dayanır.

---

## 2. Sayıları artefakttan teyit et (gömülü literal yasağı)

`AGENTS.md` → "Sayisal Butunluk Kaideleri": metindeki her sayının kaynağı üretilmiş
artefakttır. İnsansılaştırma sırasında sayıya dokunulmaz; ancak **metin ile artefakt
zaten çelişiyorsa** yeniden yazım bu çelişkiyi kalıcılaştırır. O yüzden:

```bash
# sayının hangi hedeften geldiğini bul
grep -rn "0,38\|0.38" outputs/tables/ 2>/dev/null | head
grep -rn "<hedef_adi>" _targets.R

# üretici R modülünü oku (literal var mı?)
grep -rn "<hedef_adi>" R/ | head
python3 scripts/util/r_generator_literal_audit.py
```

Çelişki varsa **yazma**: çelişkiyi bildir, `t1dm-tez-rehberi` kapsam kapısına dön.

---

## 3. Kaynak/aday dosyalarını hazırla

Guard iki dosya karşılaştırır. `.qmd` bölümünün tamamıyla çalışabilirsin ya da
pasajı geçici dosyalara alabilirsin:

```bash
sed -n '120,175p' chapters/04_bulgular.qmd > /tmp/kaynak_pasaj.md
# aday metni /tmp/aday_pasaj.md olarak yaz (henüz .qmd'ye DOKUNMA)
```

**Veri sınırı:** guard `data/raw|identified|cleaned|backup` ve `_targets/` yollarını
reddeder (`assert_safe_path`). Bu araca yalnız manuskript metni beslenir.

---

## 4. Mekanik kapı

```bash
# yalnız öz
python3 scripts/eval/humanize_invariant_guard.py guard \
  --source /tmp/kaynak_pasaj.md --candidate /tmp/aday_pasaj.md

# öz + ritim + üslup hedefleri
python3 scripts/eval/humanize_invariant_guard.py all \
  --source /tmp/kaynak_pasaj.md --candidate /tmp/aday_pasaj.md

# makine-okunur (rapor/otomasyon)
python3 scripts/eval/humanize_invariant_guard.py all \
  --source /tmp/kaynak_pasaj.md --candidate /tmp/aday_pasaj.md --json
```

Exit: `0` temiz · `1` HARD (öz ihlali; **override yok**) · `2` SOFT/üslup hedefi.

---

## 5. Repo kapıları (uygulamadan ÖNCE)

```bash
# Türkçe imla + ondalık virgül (nokta-p blocker)
python3 scripts/util/tr_corpus_audit.py all --fail-on blocker
python3 scripts/util/tez_checklist_verify.py --fast

# kanonik terim kayması (eşanlamlı sızıntısının bekçisi)
python3 scripts/util/terim_tutarlilik_audit.py

# atıf bütünlüğü
python3 scripts/util/bib_hygiene.py all

# iddia temellendirme + nedensellik etiketi
python3 scripts/util/claim_certification.py
python3 scripts/util/csr_causal_label_audit.py

# sci-audit axis G (kuruluysa)
python3 ~/.claude/plugins/marketplaces/cureonics-marketplace/plugins/sci-audit/skills/turkish-sci-style/scripts/tr_sciaudit.py \
  /tmp/aday_pasaj.md --strictness certification
```

Galileo SOFT-block (MCP `galileo-audit`): `galileo_judge` çağrısında
`text` = aday pasaj, `evidence` = **kaynak pasaj** (+ ilgili artefakt özeti),
`section_type` = bölüm tipi. Eşikler `.claude/galileo.local.md`
(groundedness/faithfulness < 0,60 = blok). MCP yoksa CLI yedeği:

```bash
printf '%s' "$JSON" | python3 scripts/eval/galileo_bridge.py
```

---

## 6. Onay sonrası

```bash
# düzenlemeyi uygula (kullanıcı onayından SONRA), ardından git-referanslı span kontrolü
python3 scripts/eval/ch05_span_guard.py HEAD chapters/<bolum>.qmd

# bölüm kapanıyorsa
python3 scripts/util/tez_checklist_verify.py --section "<bölüm>"
```

Bulgular bölümünde yeniden sıralama yapıldıysa `csr_numeric_trace_audit.py` ve tam
`tar_make()` senkronu gerekir (AGENTS.md "Tam senkron" kaidesi).

---

## 7. KVKK ve dışa aktarım sınırı

- Gateway'e (galileo/minerva) yalnız **manuskript ve literatür metni** gider;
  katılımcı, aile, ham satır verisi **asla**.
- Metni üçüncü taraf bir "AI dedektörü" veya "humanizer" servisine **yüklemek
  yasaktır**: bu, tez metninin dışa aktarımıdır ve aynı zamanda bu kapının kabul
  ölçütü değildir.
- Terminal çıktısında ham veri görülürse özetlenmez; yalnız güvenli/aggregate sonuç
  bildirilir.
