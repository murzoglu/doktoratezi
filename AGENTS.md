# AGENTS.md - Doktora Tezi Ajan Rehberi

Bu depo Quarto + R ile yazilan Tip 1 Diyabet, ebeveynlik tutumu, Beck Depresyon ve KIA analizlerine ait doktora tezi calismasidir. Ayrintili ve guncel proje baglami icin once [CLAUDE.md](CLAUDE.md) dosyasini oku; burada yalnizca ajanlarin her iste basinda bilmesi gereken kararlar var.

## Calisma Oncelikleri

- Tez, metin, kod yorumlari ve commit mesajlari icin tercih edilen dil Turkcedir; `_quarto.yml` `lang: tr` kullanir.
- Tez yazimi, format, bolum sirasi, ozet/summary, tablo/sekil ve kaynakca islerinde once
  [tez-yazim/README.md](tez-yazim/README.md) ve [docs/tez-kilavuz/](docs/tez-kilavuz/) resmi
  Marmara kaynaklari kullanilir; bu kaynaklar eski stil notlarina ustundur.
- EMBU veri mimarisi v2.0 yururluktedir ve aktif calisma hattidir. CSV basligi hatali, PDF kanonik karari kesinlesmistir ve saha dogrulama fazi gereksizdir.
- Beck Depresyon ve KIA analizleri EMBU ile paralel ilerler.
- Ham veri ve kimliklenebilir bilgi sinirlarina dikkat et: `data/raw/`, `data/cleaned/`, `data/identified/`, `data/backup/`, uretilmis `data/processed/*`, `outputs/*`, `_targets/` ve credential JSON dosyalari git disinda kalmalidir.

## Mimari Sinirlar

- [R/](R/) kutuphane katmanidir: saf fonksiyonlar, `source()` ile yuklenir, dosya yazma/okuma yan etkisi tasimamalidir.
- [scripts/R/](scripts/R/) runner katmanidir: [R/](R/) fonksiyonlarini cagirir ve `data/processed/` ile `outputs/` altina dosya yazar.
- [tests/](tests/) `stopifnot()` tabanli dogrulama testlerini icerir; sessiz cikis PASS kabul edilir.
- [chapters/](chapters/) Quarto bolumleridir; kok belge [thesis.qmd](thesis.qmd) tarafindan include edilir.
- [tez-yazim/](tez-yazim/) resmi kilavuz merkezli yazim mimarisi, sablonlar, kalite kontrol ve iki-kol entegrasyon katmanidir; gercek tez uretim dosyalarinin yerine gecmez.
- Kök [docs/](docs/) altındaki kanonik belgeler ve `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` aktif karar kaynağıdır. `docs/veri-duzenleme/` veya arşiv kopyaları tarihsel bağlamdır.

## Sayisal Butunluk Kaideleri (zorunlu)

Bu kaideler bir denetimde ortaya cikan uc kok-neden hata sinifini (BF10 driftini,
LPA tablo/metin celiskisini, imkansiz AUC optimizm duzeltmesini) tekrar etmemek
icin gecerlidir. Sayisal bir sonuc (BF, beta, ICC, AUC, CFI, entropi ...) ureten
her degisiklikte baglayicidir.

- **Sayilar kaynaktan okunur, koda gomulmez.** APA tablo/metin ureten [R/](R/)
  fonksiyonlari istatistik degerlerini gomulu literal olarak tasiyamaz; degeri
  uretilmis model/CSV artefaktindan (`outputs/models/*`, `data/processed/*`)
  okumalidir. `scripts/util/r_generator_literal_audit.py` bunu tarar ve checklist
  orkestratorunde **K5-LIT-01** kapisi olarak zorunludur (herhangi bulgu = FAIL).
- **Turev CSV girdileri `targets` ile dosya-izlenir.** Bir hedefin okudugu turetilmis
  CSV/RDS, `_targets.R`'de `format = "file"` ile izlenmelidir; boylece kaynak
  artefakt degisince icerik-hash gecersizlemesi tetiklenir ve stale deger okunmaz.
- **Model/veri her degistiginde tam `tar_make()` calistirilir.** Yalniz ilgili
  runner degil; tum boru hatti calistirilir ve kapanista `tar_outdated()` bos
  (0 hedef) olmalidir. Aksi halde metin/tablo stale artefakt gosterebilir.
- **Yon-mantigi test edilir, yalniz mevcudiyet degil.** Bir buyukluk yalnizca
  hesaplanmis olmasi degil, dogru yonde olmasi ile dogrulanir (or. optimizm
  duzeltilmis AUC <= ham AUC; Savage-Dickey BF sinif etiketi sayisal BF ile
  tutarli). Ilgili `tests/*` bu yon-savlarini icerir.
- **Model secim kurali metin ile tabloda ayni olmalidir.** LPA/model secimi tek
  parsimoni kuralina (Raftery 1995 ΔBIC≤2 "bare mention" esigi) baglidir; APA
  tablosu ve gerekce metni ayni profil/model sayisini gostermelidir.

## Komutlar

```bash
# Paket ortami
Rscript -e 'renv::restore(prompt = FALSE)'
Rscript -e 'renv::status()'

# Targets pipeline; path/raw manifest + KISIM II-XVI hash kontrollu veri yukleme/skor/SES/eksik veri/Tablo 1/DAG/PS/H1-H5/VI-XII/APA figur+tablo + yayin/risk/zaman hedefleri
Rscript -e 'targets::tar_make()'

# EMBU runner'lari yalniz dogrulama/yeniden uretim gerektiginde, sirasiyla
Rscript scripts/R/01_embu_stage1_standardize.R
Rscript scripts/R/02_embu_stage2_likert4.R
Rscript scripts/R/03_embu_stage3_family.R

# Testler
Rscript tests/test_embu_stage1.R
Rscript tests/test_embu_stage2_likert4.R
Rscript tests/test_embu_stage3_family.R

# Kapsamli tez kontrol checklisti (8 eksen, 28 madde; salt-okuma orkestrator)
python3 scripts/util/tez_checklist_verify.py --fast       # hizli on-ucus (agir kontroller SKIP)
python3 scripts/util/tez_checklist_verify.py              # tam denetim (render/PDF/renv/targets dahil)
python3 scripts/util/tez_checklist_verify.py --audit-doc  # belge<->script ID senkronu (yetim=exit 1)

# Quarto
quarto check
quarto render thesis.qmd

# Ortak yazar DOCX round-trip (repo erisimi olmayan ortak yazardan online
# "Degisiklikleri Izle" duzeltmesi almak; yalniz pandoc + Python stdlib)
python3 scripts/util/coauthor_docx_roundtrip.py export                    # render docx'i outbox/ altina hazirlar
python3 scripts/util/coauthor_docx_roundtrip.py import --edited inbox/donen.docx  # degisiklik+yorumlari .qmd satirina esleyen rapor uretir
```

## Domain Notlari

- EMBU formlari 29 P sorusu ve 29 C sorusu icerir; sutun sirasi karisik oldugu icin elle pozisyona dayanma. `find_embu_columns()` soru numarasini regex ile cikarir.
- EMBU-C satirlari 4'lu veya 6'li Likert olabilir. Siniflandirma `classify_embu_c_likert()`, aile ici karisim isaretleme `mark_mixed_likert_families()` ile yapilir.
- Gecerli aralik disi EMBU degerleri Stage 1'de `NA` yapilir; eski Stage 1-3 CSV raporlari `archive/2026-04-26_pre_canonical_embu/outputs/tables/` altinda tutulur.
- Aile yapisi icin birincil anahtar `aile_no` x `cocuk_no`; aile genis/uzun format eslestirmesi [R/04_embu_stage3_family.R](R/04_embu_stage3_family.R) icindedir.

## Dokumani Kopyalama, Bagla

- Genel proje ozeti, komutlar ve aktif analiz durumu: [CLAUDE.md](CLAUDE.md)
- Resmi kilavuz merkezli tez yazim mimarisi: [tez-yazim/README.md](tez-yazim/README.md)
- Kapsamli tez kontrol checklisti (8 eksen, 28 madde, kapsama matrisi): [tez-yazim/04_kalite-kontrol/tez-kontrol-checklisti.md](tez-yazim/04_kalite-kontrol/tez-kontrol-checklisti.md); otomasyon `scripts/util/tez_checklist_verify.py`
- Bulgular zenginlestirme iki kardes slash-komut: `/anlatim-zenginligi` (nesir anlatim + referans; kanit/figur/tablo dokunulmaz) ve `/veri-gosterimi-zenginligi` (veri-gosterim katmani: R cikti<->metin mutabakati, figur/tablo veri-tutarliligi + estetik/Turkce/tasarim, eksik-ama-yararli yeni gorsel, baslik/altyazi + betim netligi; kanit _degeri_ dokunulmaz). Ikisi de sayi/yon/anlamliligi degistirmez; esgudum sirasi ve devir protokolu: [tez-yazim/04_kalite-kontrol/bulgular-zenginlestirme-esgudum-playbook.md](tez-yazim/04_kalite-kontrol/bulgular-zenginlestirme-esgudum-playbook.md)
- Marmara resmi tez kilavuzu ve sablonlari: [docs/tez-kilavuz/](docs/tez-kilavuz/)
- Kanonik EMBU-P formu: [docs/protokol/KANONIK_KISALTILMIS_EMBU_EBEVEYN.md](docs/protokol/KANONIK_KISALTILMIS_EMBU_EBEVEYN.md)
- Kanonik EMBU-C formu: [docs/protokol/KANONIK_KISALTILMIS_EMBU_COCUK.md](docs/protokol/KANONIK_KISALTILMIS_EMBU_COCUK.md)
- Final referans veri haritasi: [docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md](docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md)
- Kanonik analiz baz kilidi: [data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock](data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock)
- Kanonik form oncesi karar gecmisi ve CSV raporlari: [archive/2026-04-26_pre_canonical_embu/README.md](archive/2026-04-26_pre_canonical_embu/README.md)
