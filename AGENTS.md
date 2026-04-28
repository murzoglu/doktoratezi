# AGENTS.md - Doktora Tezi Ajan Rehberi

Bu depo Quarto + R ile yazilan Tip 1 Diyabet, ebeveynlik tutumu, Beck Depresyon ve KIA analizlerine ait doktora tezi calismasidir. Ayrintili ve guncel proje baglami icin once [CLAUDE.md](CLAUDE.md) dosyasini oku; burada yalnizca ajanlarin her iste basinda bilmesi gereken kararlar var.

## Calisma Oncelikleri

- Tez, metin, kod yorumlari ve commit mesajlari icin tercih edilen dil Turkcedir; `_quarto.yml` `lang: tr` kullanir.
- EMBU veri mimarisi v2.0 yururluktedir ve aktif calisma hattidir. CSV basligi hatali, PDF kanonik karari kesinlesmistir ve saha dogrulama fazi gereksizdir.
- Beck Depresyon ve KIA analizleri EMBU ile paralel ilerler.
- Ham veri ve kimliklenebilir bilgi sinirlarina dikkat et: `data/raw/`, `data/cleaned/`, `data/identified/`, `data/backup/`, uretilmis `data/processed/*`, `outputs/*`, `_targets/` ve credential JSON dosyalari git disinda kalmalidir.

## Mimari Sinirlar

- [R/](R/) kutuphane katmanidir: saf fonksiyonlar, `source()` ile yuklenir, dosya yazma/okuma yan etkisi tasimamalidir.
- [scripts/R/](scripts/R/) runner katmanidir: [R/](R/) fonksiyonlarini cagirir ve `data/processed/` ile `outputs/` altina dosya yazar.
- [tests/](tests/) `stopifnot()` tabanli dogrulama testlerini icerir; sessiz cikis PASS kabul edilir.
- [chapters/](chapters/) Quarto bolumleridir; kok belge [thesis.qmd](thesis.qmd) tarafindan include edilir.
- Kök [docs/](docs/) altındaki kanonik belgeler ve `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` aktif karar kaynağıdır. `docs/veri-duzenleme/` veya arşiv kopyaları tarihsel bağlamdır.

## Komutlar

```bash
# Paket ortami
Rscript -e 'renv::restore(prompt = FALSE)'
Rscript -e 'renv::status()'

# Targets pipeline; path/raw manifest + KISIM II-V hash kontrollu veri yukleme/skor/SES/eksik veri/Tablo 1/DAG/PS/H1/H2/H3/H4 hedefleri
Rscript -e 'targets::tar_make()'

# EMBU runner'lari yalniz dogrulama/yeniden uretim gerektiginde, sirasiyla
Rscript scripts/R/01_embu_stage1_standardize.R
Rscript scripts/R/02_embu_stage2_likert4.R
Rscript scripts/R/03_embu_stage3_family.R

# Testler
Rscript tests/test_embu_stage1.R
Rscript tests/test_embu_stage2_likert4.R
Rscript tests/test_embu_stage3_family.R

# Quarto
quarto check
quarto render thesis.qmd
```

## Domain Notlari

- EMBU formlari 29 P sorusu ve 29 C sorusu icerir; sutun sirasi karisik oldugu icin elle pozisyona dayanma. `find_embu_columns()` soru numarasini regex ile cikarir.
- EMBU-C satirlari 4'lu veya 6'li Likert olabilir. Siniflandirma `classify_embu_c_likert()`, aile ici karisim isaretleme `mark_mixed_likert_families()` ile yapilir.
- Gecerli aralik disi EMBU degerleri Stage 1'de `NA` yapilir; eski Stage 1-3 CSV raporlari `archive/2026-04-26_pre_canonical_embu/outputs/tables/` altinda tutulur.
- Aile yapisi icin birincil anahtar `aile_no` x `cocuk_no`; aile genis/uzun format eslestirmesi [R/04_embu_stage3_family.R](R/04_embu_stage3_family.R) icindedir.

## Dokumani Kopyalama, Bagla

- Genel proje ozeti, komutlar ve aktif analiz durumu: [CLAUDE.md](CLAUDE.md)
- Kanonik EMBU-P formu: [docs/KANONIK_KISALTILMIS_EMBU_EBEVEYN.md](docs/KANONIK_KISALTILMIS_EMBU_EBEVEYN.md)
- Kanonik EMBU-C formu: [docs/KANONIK_KISALTILMIS_EMBU_COCUK.md](docs/KANONIK_KISALTILMIS_EMBU_COCUK.md)
- Final referans veri haritasi: [docs/FINAL_REFERENCE_VERI_HARITASI.md](docs/FINAL_REFERENCE_VERI_HARITASI.md)
- Kanonik analiz baz kilidi: [data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock](data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock)
- Kanonik form oncesi karar gecmisi ve CSV raporlari: [archive/2026-04-26_pre_canonical_embu/README.md](archive/2026-04-26_pre_canonical_embu/README.md)
