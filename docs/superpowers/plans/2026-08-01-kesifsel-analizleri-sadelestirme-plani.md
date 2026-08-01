# Keşifsel Analizler (Genişletilmiş Analiz Katmanları) Sadeleştirme Planı

Bu dosya, tezin 04_bulgular.qmd bölümünde yer alan "Keşifsel Analizler" alt başlıklarını sadeleştirmek için oluşturulmuştur. H1-H5 arası temel hipotezlerde yaptığımız "istatistiksel jargondan klinik/günlük dile çeviri" prensibi burada da harfiyen uygulanacaktır.

## İcra Edilecek Adımlar

1.  **Aracılık Analizi (Mediation):**
    *   **Eski Durum:** "BCa bootstrap, Imai-Keele-Tingley, a-yolu/b-yolu, Hayes'in 14 numaralı şablonu" gibi ağır terminoloji var.
    *   **Yeni Durum:** Bunlar "Dolaylı/aracı etki modeli", "direkt etki", "aracının devreden çıkması" gibi daha net kavramlara çevrilecek. Sonuç metni: "Anne depresyonunun çocuğu etkilemesi, annenin 'reddedici tutumu' üzerinden gerçekleşmiyor; depresyon çocuğu doğrudan etkiliyor" şeklinde netleştirilecek.

2.  **Latent Profil ve Sınıf Analizi (LPA/LCA):**
    *   **Eski Durum:** "tidyLPA, mclust arka ucu, poLCA duyarlılık çözümlemesi, log-olabilirlik, Bifaktör S-1 modeli, BLRT" kavramları var.
    *   **Yeni Durum:** "Gizli profil ayırma yöntemi", "farklı algoritma denemeleri", "3'lü gruplama uyumu" biçiminde yazılacak. "İstatistiksel yazılımın aileleri doğal gruplara ayırması ve diyabetin bu grup dağılımında bir fark yaratmaması" ana fikri öne çıkarılacak.

3.  **Ağ Analizi (Network Analysis):**
    *   **Eski Durum:** "EBIC-LASSO Gauss grafik modeli, düğüm strength merkeziyeti, case-dropping bootstrap kararlılık katsayısı, NCT (ağ invaryansı)" geçiyor.
    *   **Yeni Durum:** "İlişki ağı modeli", "kilit/merkez konu", "bağların gücü" ve "ağ yapıları karşılaştırması" olarak sadeleştirilecek.

4.  **Klinik Fayda (Clinical Utility):**
    *   **Eski Durum:** "Youden indeksi, iç-validasyonlu optimizm-düzeltilmiş bootstrap, DCA net fayda, kalibrasyon bini, CART hata profili, Random Forest" geçiyor.
    *   **Yeni Durum:** "En uygun eşik noktası", "modelin kendi kendini test etmesi", "klinik fayda-zarar analizi" ve "yapay zekâ önem sıralaması" gibi terimlere dönüştürülecek.

5.  **DM Klinik Alt-Analizler:**
    *   **Eski Durum:** "Kübik spline ile doğrusal karşılaştırma, metabolik kontrol etkileşimi" vb. ifadeler incelenecek.
    *   **Yeni Durum:** "Hastalık süresinin eğrisel ve düz etkisi", "kan şekerinin tutuma etkisi" biçiminde yalınlaştırılacak.

## İcra Yöntemi
Her adım `sed`/`grep` ile okunacak, `replace.py` scriptleri ile regex veya `replace()` kullanılarak değiştirilecek ve her adım sonrasında `tez_checklist_verify.py` test edilerek sayıların ve atıfların (p/b/β, @fig, @tbl vb.) bozulmadığı garanti altına alınacaktır. Tablo başlıkları (`tbl-cap`) daha önce güncellendiği için sadece gövde metinleri (*Kanıt* ve **Bulgu özeti** bölümleri) değiştirilecektir.
