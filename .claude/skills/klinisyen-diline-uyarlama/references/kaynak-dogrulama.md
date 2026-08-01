# Kaynak doğrulama + DOKUNULMAZ envanter (Gemini'ye göndermeden ÖNCE)

Amaç: pasajı yeniden üsluplatmadan önce (1) gerçek konumu bul, (2) korunacak her şeyin
**envanterini** çıkar — bu envanter hem Gemini'nin sistem talimatına gömülür hem de Adım 2
değerlendirmesinde diff ölçütü olur.

## 1. Gerçek dosya:satırı bul (dosya adı TAHMİN ETME)

```bash
grep -rn "<seçili ayırt edici ifade>" chapters/
```
Pasajın çevresini oku (`sed -n 'A,Bp' chapters/<dosya>.qmd` veya Read). Belirsizse netleştir,
tahmin etme.

## 2. DOKUNULMAZ envanteri çıkar

Bu pasajda korunacak **her** öğeyi listele:

| Sınıf | Nasıl bulunur | Örnek |
|---|---|---|
| Sayılar | Tüm rakam/oran/yüzde/eşik | `SMD = 0,53`, `%29`, `0,220 → 0,004`, `medyan 38,5` |
| Atıf token | `\[@[^]]+\]` | `[@austin2009balanceDiagnostics]` |
| Tablo/şekil token | `@tbl-\*`, `@fig-\*` | `@tbl-apa-sample-characteristics`, `@fig-smd-love` |
| Faz etiketi | `\[KEŞİFSEL\]`, `\[POST-HOC\]` | keşifsel bulgu bloğu |
| Çekince/kapsam | "yalnız …", "neredeyse", "sınırda", "analizlerde dikkate alınan" | kapsam sınırı |
| Bulgu yönü/anlamlılık | "daha yüksek/düşük", "anlamlı/anlamlı değil" | yön ifadeleri |

```bash
grep -oE '@(tbl|fig)-[A-Za-z0-9_-]+|\[@[^]]+\]|\[(KEŞİFSEL|POST-HOC)\]' chapters/<dosya>.qmd
```

## 3. Sayıyı artefakta bağla (kaynak-tekilliği)

Aktaracağın her istatistik **üretilmiş artefakttan** doğrulanır, metinden değil kopyalanır.
Metin↔artefakt çelişkisi görürsen **yeniden yazma; çelişkiyi bildir.** Bulgular pasajı için
numeric-trace:

```bash
python3 scripts/util/csr_numeric_trace_audit.py --csr chapters/04_bulgular.qmd \
  --out-report outputs/reports/ch04_numeric_trace_audit.md
```
Yüksek-risk eşsiz = 0 olmalı. (Yeniden sıralama Bulgular'a dokunuyorsa uygulamadan sonra
tekrar koşulur — bkz. SKILL.md yeniden sıralama kapısı.)

## 4. Çapraz-referans haritası

Pasajın bağlı olduğu ileri/geri atıfları not et: "@tbl-…", "@fig-…", "yukarıda/aşağıda
belirtildiği gibi", özet/summary'de aynı sayının tekrarı. Yeniden sıralama yaparsan bu zincir
**yeniden doğrulanır**; kırılırsa yeniden sıralama geri alınır.

## 5. Envanteri harness spec'ine sınıfla (maskeleme granülerliği)

Envanter, `constrained_rewrite.py` spec'inin `spans`/`caveats` alanlarına dönüşür; maske
granülerliği hem kanıt bütünlüğünü hem dikişsizliği belirler (kalibrasyon dersleri):

- **Atomik değer** (sayı/oran/eşik) → `spans`, cümle-içi minimal maske.
- **Çekince / kapsam sınırı** → `caveats`, **TAM CÜMLE** maskele (model yeniden kurup zayıflatamaz).
- **Tam-yüklemli kapsam öbeği** ("…yalnız X ve Y alt ölçeklerinde tahmin edilmiştir") →
  **TAM CÜMLE ya da yüklem-DAHİL öbek** maskele. Parça (yalnız "X ve Y'de") maskelenirse model
  özne/yüklemi yeniden kurunca **bağlaçsız dikiş (run-on)** doğar — H5 ¶4 dersi.
- **Kalın yapısal etiket** (`**Strateji N (…).**`) → `spans` (düşmesin/yeniden adlandırılmasın).
- `@tbl-*`/`@fig-*`/`[@key]` otomatik maskelenir (spec'e elle eklemek gerekmez).

Tam granülerlik tablosu + `default_system` register kuralları: `gemini-prompt-sablonu.md`.

## Çıktı

Bu adımın çıktısı: `{dosya:satır, spans[] (sayı/token/etiket), caveats[] (tam-cümle çekince),
glossary{}, capraz_ref[]}` — SKILL.md Adım 1'de harness spec'ine (`constrained_rewrite.py`),
Adım 2'de diff ölçütüne beslenir. `verify` maskeleneni birebir garanti eder; maskeleme
listesinin **tam** olması bu adımın (Claude Adım 0) sorumluluğudur.
