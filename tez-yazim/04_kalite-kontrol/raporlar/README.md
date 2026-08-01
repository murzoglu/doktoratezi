# Kalite Kontrol Raporları

Bu klasör bölüm bazlı otomatik/yarı otomatik kalite kontrol raporlarını tutar.

Önerilen adlandırma:

```text
<bolum-kodu>-tr-sciaudit.md      # sci-audit axis G (Türkçe imla/yazım)
<bolum-kodu>-tr-sciaudit.json    # deterministik CLI makine-okunur çıktı (opsiyonel)
<bolum-kodu>-sci-audit.md        # sci-audit axes A-F (manüskript adli denetim)
```

Denetimler **`sci-audit@cureonics-marketplace` plugin** üzerinden koşulur
(kanonik araç). Türkçe imla/yazım ön-denetimi için:

```bash
# İnteraktif:
/sci-audit:check-turkish chapters/<bolum>.qmd --strictness certification

# Deterministik CLI (rapor üretimi; plugin-bundled):
SCIA="$(ls -d $HOME/.claude/plugins/cache/cureonics-marketplace/sci-audit/*/ | sort -V | tail -1)"
python3 "${SCIA}skills/turkish-sci-style/scripts/tr_sciaudit.py" chapters/<bolum>.qmd \
  --strictness certification --format md --fail-on error \
  --out tez-yazim/04_kalite-kontrol/raporlar/<bolum-kodu>-tr-sciaudit.md
```

Manüskript adli denetimi (referans/claim/istatistik/halüsinasyon/kılavuz/
AI-şeffaflık) için `/sci-audit:audit chapters/<bolum>.qmd` → `/sci-audit:audit-report
--out <bolum-kodu>-sci-audit.md`.

> Not: Bu klasördeki mevcut `01-giris-tr-sciaudit.md` / `02-yontem-tr-sciaudit.md`
> raporları, 2026-07-06'da silinen repo-local `scripts/util/tr_sciaudit.py` ile
> üretilmiş tarihsel çıktılardır; CLI birebir aynı olduğundan içerik geçerlidir.
> Yeni koşumlar yalnız `sci-audit` plugin üzerinden yapılır.

Bu raporlar insan editör okumasının yerine geçmez; Kapı 4/5 için makine-okunur
denetim kanıtı sağlar.
