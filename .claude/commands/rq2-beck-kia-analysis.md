---
description: Beck Depresyon ve KIA/SRQ için aktif RQ2 analizini planla veya taslaklaştır
argument-hint: "[odak: betimsel tablo | eksik veri | regresyon | bulgular taslağı]"
---

# /rq2-beck-kia-analysis

Kullanıcı odağı: **$ARGUMENTS**

Beck Depresyon ve KIA/SRQ analizlerinin aktif RQ2 hattı için uygulanabilir, kısa
bir kontrol listesi üret.

Önce şunları oku:

- `AGENTS.md`
- `CLAUDE.md`
- ilgili `R/` ve `scripts/R/` kodu
- raporlama etkileniyorsa `chapters/04_bulgular.qmd`

Kontrol listesinde şunları belirt:

1. İncelenecek veri kaynakları ve değişkenler.
2. Aralık dışı Beck veya KIA/SRQ değerleri dahil gerekli temizlik/doğrulama adımları.
3. Uygun betimsel tablo ve şekiller.
4. Varsayımları ve kovaryatlarıyla aday istatistiksel modeller.
5. Değişmesi olası R/Quarto dosyaları.
6. En az doğrulama komutları.

Kısıtlar:

- EMBU v2.0 hattı aktiftir; kullanıcı açıkça istemedikçe EMBU artefaktlarını değiştirme.
- Ham veri ve kimliklenebilir bilgiyi yanıta alma.
- Yeni bir analiz mimarisi kurmak yerine depo içi örüntüleri izle.
- Kod değişikliğinde `R/` saf-fonksiyon ve `scripts/R/` runner ayrımını koru.
