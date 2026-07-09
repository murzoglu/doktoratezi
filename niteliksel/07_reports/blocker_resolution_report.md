# Blokaj Çözümleme Raporu

AI destekli çıktılar yalnızca yardımcı, ön-denetim veya tutarlılık kontrolü olarak değerlendirilir. Kodlama, tema geliştirme ve yorumlama kararları araştırmacı sorumluluğundadır.

## Kapatılan Blokajlar

- `06_manuscript_outputs/quotes_used.csv` üretildi: temizlenmiş tez metnindeki seçilmiş ve anonimleştirilmiş alıntılardan 116 kayıt.
- `01_deidentified/coded_segments.csv` üretildi: aynı 116 kayıt aile, rol, tema, alt tema, kod ve quote ID alanlarıyla ön-kodlama taslağına dönüştürüldü.
- `03_analysis/codebook/codebook_v3.csv` gerçek quote ID havuzuyla kısmen bağlandı: 23 kodun 18'i seçilmiş alıntı havuzunda karşılık buldu.
- `04_triadic_matrices/triadic_matrix_from_cleaned_thesis.csv` üretildi: 57 aile-tema-alt tema satırı; 7 aile ve 4 tez makro teması kapsandı.
- `07_reports/quote_integrity_report.md` üretildi: mevcut seçilmiş alıntı havuzu için kritik bulgu, uyarı veya öneri üretmedi.
- `07_reports/negative_case_report_tema_4_triadic.md` üretildi: Tema 4 için negatif vaka / gerilim ön-tarama raporu oluşturuldu.

## Kalan Blokajlar

Beş kod için temizlenmiş tez metnindeki seçilmiş alıntı havuzunda güvenli ve doğrudan bağlanabilir quote ID bulunmadı. Bu kodlarda placeholder ID bırakıldı; kaynak alıntı uydurulmadı.

- `TANI_BILGI_ARAYISI`
- `GECE_TAKIP`
- `YARAR_BULMA_OLGUNLASMA`
- `SAGLIK_EKIBI_DESTEGI`
- `MANEVI_BASA_CIKMA`

## Bilimsel Uygunluk Notu

`coded_segments.csv` nihai kodlama dosyası değildir. Bu dosya temizlenmiş tez metninden seçilmiş alıntılara dayanan, araştırmacı-denetimli bir ön-kodlama / denetim girdisidir. Tema üretimi veya nihai bulgu iddiası taşımaz.

Kalan beş kod ancak araştırmacının seçtiği ve anonimleştirilmiş kaynak alıntılarla bağlandıktan sonra codebook v3 final sürüme yükseltilmelidir.

## Doğrulama

- `./dmnitel lint-codebook 03_analysis/codebook/codebook_v3.csv`
- `./dmnitel check-quotes --source 02_processed/cleaned_text/thesis_qualitative_cleaned_current.md --quotes 06_manuscript_outputs/quotes_used.csv --output 07_reports/quote_integrity_report.md`
- `./dmnitel build-triadic-matrix --coded-data 01_deidentified/coded_segments.csv --output 04_triadic_matrices/triadic_matrix_from_cleaned_thesis.csv`
- `./dmnitel find-negative-cases --coded-data 01_deidentified/coded_segments.csv --theme "TEMA 4: Aynı Ev, Üç Farklı Deneyim: Triadik Karşılaştırmalı Okuma (Anne–Hasta–Kardeş)" --output 07_reports/negative_case_report_tema_4_triadic.md`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`

## Araştırmacı Kararı İçin Notlar

- Kalan beş kod için gerçek, anonimleştirilmiş alıntı ID'si araştırmacı tarafından atanmalıdır.
- Triadik matrisin özet, convergence, divergence, negative case ve analytic memo alanları araştırmacı yorumu ile doldurulmalıdır.
- Negatif vaka raporu kesin yorum değil, yalnızca kontrol edilmesi gereken gerilim alanlarını görünür kılan bir ön-denetim çıktısıdır.
