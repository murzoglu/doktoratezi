# 📊 İstatistiksel Analiz Araçları - Özet Rapor

## ✅ Yüklenen Araçlar ve Kütüphaneler

### 1. Python İstatistik Paketleri

#### Temel Paketler (Yüklü ✓)
- **scipy** - Temel istatistiksel testler
- **statsmodels** - Regresyon ve ileri analizler
- **pingouin** - Kullanıcı dostu istatistik fonksiyonları
- **scikit-learn** - Machine learning ve çapraz doğrulama
- **factor-analyzer** - Faktör analizi ve güvenilirlik

#### Görselleştirme (Yüklü ✓)
- **matplotlib** - Temel grafikler
- **seaborn** - İstatistiksel görselleştirme
- **plotly** - İnteraktif grafikler

#### Veri İşleme (Yüklü ✓)
- **pandas** - Veri manipülasyonu
- **numpy** - Sayısal hesaplamalar
- **openpyxl** - Excel dosya işleme

### 2. Hazırlanan Analiz Scriptleri

#### Veri Hazırlama
- `01_load_data.py` - Google Sheets'ten veri yükleme
- `02_clean_data.py` - Veri temizleme ve dönüştürme

#### Tanımlayıcı Analizler
- `03_descriptive_stats.py` - Tanımlayıcı istatistikler
  - Demografik özellikler
  - Merkezi eğilim ölçüleri
  - Dağılım ölçüleri
  - Normallik testleri

#### Hipotez Testleri
- `04_hypothesis_testing.py` - Grup karşılaştırmaları
  - T-testleri (parametrik)
  - Mann-Whitney U (non-parametrik)
  - Ki-kare testleri
  - Korelasyon analizleri
  - Effect size hesaplamaları

#### İleri Analizler
- `05_advanced_analysis.py` - Regresyon ve modellemeler
  - Çoklu doğrusal regresyon
  - Lojistik regresyon
  - Mediasyon analizi (Baron & Kenny)
  - Moderasyon analizi
  - Hiyerarşik regresyon

#### Güvenilirlik ve Faktör
- `06_reliability_factor_analysis.py`
  - Cronbach's alpha
  - Item-total korelasyonları
  - Split-half güvenilirlik
  - Açıklayıcı faktör analizi (EFA)
  - KMO ve Bartlett testleri

### 3. SPSS Alternatifi GUI Araçları

#### Ücretsiz Alternatifler

**1. JASP** (Önerilen)
- **URL:** https://jasp-stats.org/
- **Özellikler:**
  - SPSS benzeri arayüz
  - Tüm temel analizler
  - Bayesian istatistikler
  - APA formatında tablolar
  - **Platform:** Windows, Mac, Linux

**2. jamovi**
- **URL:** https://www.jamovi.org/
- **Özellikler:**
  - Modern, kullanıcı dostu arayüz
  - R tabanlı, Python desteği
  - Modüler yapı
  - Gerçek zamanlı sonuçlar
  - **Platform:** Windows, Mac, Linux

**3. BlueSky Statistics**
- **URL:** https://www.blueskystatistics.com/
- **Özellikler:**
  - SPSS'e en benzer arayüz
  - Tüm klasik testler
  - R tabanlı
  - **Platform:** Windows, Mac

**4. Orange**
- **URL:** https://orange.biolab.si/
- **Kurulum:** `pip install orange3`
- **Özellikler:**
  - Görsel programlama
  - Python tabanlı
  - Machine learning odaklı
  - **Platform:** Windows, Mac, Linux

### 4. Protokole Göre Gerekli Analizler

#### ✅ Hazır Olanlar
1. **Tanımlayıcı İstatistikler**
   - Ortalama, SD, median, IQR
   - Frekans tabloları
   - Grafikler

2. **Grup Karşılaştırmaları**
   - Diyabet vs Kontrol grubu
   - T-test ve Mann-Whitney U
   - Effect size (Cohen's d, r)

3. **Güvenilirlik Analizleri**
   - Beck Depresyon Ölçeği (Cronbach's α)
   - EMBU ölçekleri
   - Item analizleri

4. **Korelasyon Analizleri**
   - Pearson korelasyon
   - Spearman korelasyon
   - Partial korelasyon

5. **Regresyon Modelleri**
   - Beck skorları için prediktörler
   - Grup üyeliği tahmini
   - Hiyerarşik modeller

6. **Mediasyon/Moderasyon**
   - Aracı değişken analizleri
   - Düzenleyici değişken analizleri
   - Sobel testi

### 5. Kullanım Kılavuzu

#### Hızlı Başlangıç

```bash
# 1. Gerekli paketleri yükle
pip install -r requirements_statistical.txt

# 2. Veri yükle
python scripts/preprocessing/01_load_data.py

# 3. Veri temizle
python scripts/preprocessing/02_clean_data.py

# 4. Tanımlayıcı analizler
python scripts/analysis/03_descriptive_stats.py

# 5. Hipotez testleri
python scripts/analysis/04_hypothesis_testing.py

# 6. İleri analizler
python scripts/analysis/05_advanced_analysis.py

# 7. Güvenilirlik analizi
python scripts/analysis/06_reliability_factor_analysis.py
```

#### Test Script'i

```bash
# Paketleri test et
python scripts/test_packages.py
```

### 6. Analiz Kontrol Listesi

#### Varsayım Kontrolleri
- [x] Normallik testleri (Shapiro-Wilk)
- [x] Varyans homojenliği (Levene)
- [x] Çoklu bağlantı kontrolü (VIF)
- [x] Aykırı değer analizi

#### İstatistiksel Testler
- [x] Parametrik testler (t-test, ANOVA)
- [x] Non-parametrik testler (Mann-Whitney, Kruskal-Wallis)
- [x] Effect size hesaplamaları
- [x] Güven aralıkları
- [x] Power analizi (post-hoc)

#### Raporlama
- [x] APA formatında tablolar
- [x] Yayın kalitesinde grafikler
- [x] STROBE kontrol listesi uyumlu
- [x] Tekrarlanabilir analizler

### 7. Çıktı Dosyaları

Analizler sonucunda oluşacak dosyalar:

```
results/
├── tables/
│   ├── descriptive_statistics.xlsx
│   ├── hypothesis_test_results.xlsx
│   ├── reliability_analysis.xlsx
│   └── regression_results.xlsx
├── figures/
│   ├── grup_dagilimi.png
│   ├── beck_skorlari.png
│   ├── korelasyon_matrisi.png
│   └── reliability_comparison.png
├── models/
│   ├── multiple_regression_summary.txt
│   ├── logistic_regression.xlsx
│   └── mediation_results.xlsx
└── reports/
    ├── descriptive_report.txt
    └── final_analysis_report.pdf
```

### 8. Sorun Giderme

#### Paket Yükleme Sorunları
```bash
# Tek tek yükle
pip install scipy statsmodels pingouin scikit-learn factor-analyzer
```

#### Bellek Sorunları
```python
# Büyük veri setleri için
df = pd.read_csv('file.csv', chunksize=1000)
```

#### Import Hataları
```python
# Alternatif import
try:
    import pingouin as pg
except:
    import scipy.stats as stats  # Fallback
```

### 9. Kaynaklar ve Dokümantasyon

- [SciPy Stats](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Statsmodels](https://www.statsmodels.org/)
- [Pingouin](https://pingouin-stats.org/)
- [Factor Analyzer](https://github.com/EducationalTestingService/factor_analyzer)
- [JASP Guides](https://jasp-stats.org/how-to-use-jasp/)
- [jamovi User Guide](https://www.jamovi.org/user-manual.html)

### 10. Destek ve Yardım

Analiz sürecinde yardım için:
1. Script içindeki yorumları okuyun
2. `--help` parametresi ile scriptleri çalıştırın
3. Error mesajlarını Google'da aratın
4. Stack Overflow'da arayın
5. GitHub Issues'da sorun bildirin

---

**Durum:** ✅ Tüm araçlar hazır ve çalışır durumda
**Tarih:** 20 Eylül 2025
**Sonraki Adım:** Veri analizlerine başlayabilirsiniz!