# Türkçe Bilimsel Yazım Denetimi (sci-audit axis G)

Sürüm: 2.0 · 2026-07-06 · **Kanonik araç: `sci-audit@cureonics-marketplace`
plugin, axis G (Türkçe bilimsel yazım/imla).**

> **Rafine notu (v1 → v2):** Bu denetimin eski sürümü, repo içinde ayrı bir
> `scripts/util/tr_sciaudit.py` + `.venv-tr-sciaudit` + `gecturk_selfhost_endpoint.py`
> + `requirements/tr-sciaudit.txt` + `tests/test_tr_sciaudit.py` kopyası
> çalıştırıyordu. Aynı `tr_sciaudit` CLI'si artık `sci-audit` plugin'inde
> **bundle** edilmiştir (CLI sözleşmesi birebir korunmuştur). Duplikasyonu
> tamamen kaldırmak için **plugin sürümü tek kanonik araçtır**; repo-local
> kopyalar (script + endpoint + test + requirements + venv) **2026-07-06'da
> silinmiştir**. Tez imla/yazım denetimi Kapı 4'te yalnız bu plugin üzerinden
> yürür (`bolum-finalizasyon-sertifikasyon-playbook.md`).

## Amaç ve kapsam

sci-audit axis G, Türkçe tez bölümlerini şu eksenlerde tarar:

1. biçimsel yazım sinyalleri (encoding artefact, noktalama boşluğu, tekrar),
2. okunabilirlik ve üslup (cümle/paragraf uzunluğu, hece sayımı, Ateşman skoru),
3. akademik register (birinci kişi, konuşma dili, İngilizce terim sızıntısı),
4. nedensellik/genelleme dili disiplini,
5. **ondalık virgül ve `p` değeri yazımı** (G5: Türkçe metinde İngilizce
   ondalık-nokta `p` değeri **blocker**tır),
6. kısaltma/terim tutarlılığı (certification modunda),
7. opsiyonel Zemberek, GECTurk, TDK provider durumları + `style-judge` alt-ajanı.

Bu araç bilimsel doğruluk, istatistiksel uygunluk, kaynak doğrulama,
intihal/benzerlik veya klinik yorum sertifikası **vermez**. Manüskript adli
denetimi (referans/claim/istatistik/halüsinasyon/kılavuz/AI-şeffaflık)
sci-audit'in **axes A–F**'sindedir; KVKK/ham veri/quote-parity ise repo-özel
ai-audit plugin'lerindedir (bkz. playbook "AI-Reliability Katman Sınırı").

## Kanonik komut

```bash
# İnteraktif (birincil):
/sci-audit:check-turkish chapters/<bolum>.qmd --strictness certification \
  [--enable-tdk --terms "diyabet,depresyon,ebeveyn,kardeş,ölçek,yöntem"] \
  [--enable-zemberek] [--enable-gecturk --gecturk-url http://127.0.0.1:8765/check] \
  [--abbreviations project-abbr.txt]

# Deterministik CLI (CI/rapor; plugin-bundled — repo-local kopya değil):
SCIA="$(ls -d /home/mahirkurt/.claude/plugins/cache/cureonics-marketplace/sci-audit/*/ | sort -V | tail -1)"
python3 "${SCIA}skills/turkish-sci-style/scripts/tr_sciaudit.py" chapters/<bolum>.qmd \
  --strictness certification --format md --fail-on error \
  --out tez-yazim/04_kalite-kontrol/raporlar/<bolum>-tr-sciaudit.md
```

Severity eşlemesi: `error → blocker`, `warning → major`, `info → minor`.
`--strictness`: `draft` (hafif) veya `certification` (tam; kısaltma tutarlılığı
eklenir). `--fail-on error` blocker'da non-zero exit döner.

## Provider davranışı (deterministik çekirdek her zaman çalışır)

| Provider | Varsayılan | Başarılı durum | Güvenli fallback |
|---|---|---|---|
| Deterministik çekirdek (G1–G6) | Her zaman | Ağsız, web dahil çalışır | Yok — daima çalışır |
| TDK | Kapalı (`--enable-tdk --terms`) | Sınırlı terim `sozluk.gov.tr/gts` | HTTP hatası `error` statüsü; denetim sürer |
| Zemberek | Kapalı (`--enable-zemberek`) | Morfoloji örneklemi | Paket yoksa `unavailable`; bloklamaz |
| GECTurk | Kapalı (`--enable-gecturk --gecturk-url`) | Self-host endpoint JSON | URL yoksa `unavailable`; public API varsayılmaz |
| `style-judge` (alt-ajan) | Opsiyonel | Register/akıcılık rubriği | Deterministik G-denetimi tek başına geçerli; çakışmada deterministik kazanır |

## Güvenlik ve gizlilik

- Deterministik çekirdek metni **dış API'ye göndermez**; ağsız çalışır.
- Privacy invaryantı: yalnız açıkça verilen dosya okunur; `data/`, `_targets/`,
  `outputs/`, transkript, `.env`/credential otomatik taranmaz (PreToolUse hook
  ayrıca zorlar).
- TDK yalnız sınırlı terim listesiyle; sözlüğün tamamı indirilmez.
- Raporlar yalnız türetilmiş metrik ve kısa kanıt parçaları içerir.

## Stop-gate yapılandırması (opsiyonel)

Proje kökünde `.claude/sci-audit.local.md` frontmatter'ı Stop-gate'i ayarlar:

```markdown
---
lang: auto                    # auto | tr | en
gate_unsourced_numeric: true  # kaynaksız sayısal iddiayı bloke et
gate_tr_pvalue_dot: true      # Türkçe metinde İngilizce ondalık-nokta p'yi bloke et
---
```

## Kabul kriteri (Kapı 4)

- `/sci-audit:check-turkish` (veya bundled CLI) ilgili bölüm için çalıştırıldı.
- Çıktı raporu `tez-yazim/04_kalite-kontrol/raporlar/<bolum>-tr-sciaudit.md`'ye
  ve sertifika dosyasına işlendi.
- `error` (blocker) yok.
- `warning` (major) bulguları düzeltildi veya bilinçli kabul notuyla sertifikaya
  geçirildi.
- İnsan editör okuması hâlâ zorunlu.
