# Klinik Çalışma Analiz İş Akışı

## 📋 Genel Bakış

Bu doküman, doktora tezi kapsamındaki klinik çalışmanın veri analizi ve yayın sürecini adım adım açıklamaktadır.

## 🔄 İş Akışı Diyagramı

```
1. VERİ HAZIRLAMA
   ├── Google Sheets'ten veri çekme
   ├── Veri temizleme
   └── Değişken kodlama
           ↓
2. KALİTE KONTROLÜ
   ├── Eksik veri analizi
   ├── Aykırı değer tespiti
   └── Veri doğrulama
           ↓
3. TANIMLAYICI ANALİZ
   ├── Demografik özellikler
   ├── Ölçek güvenilirlikleri
   └── Temel istatistikler
           ↓
4. ÇIKARIMSAL ANALİZ
   ├── Hipotez testleri
   ├── Grup karşılaştırmaları
   └── İlişki analizleri
           ↓
5. İLERİ ANALİZLER
   ├── Regresyon modelleri
   ├── Mediasyon/Moderasyon
   └── Alt grup analizleri
           ↓
6. RAPORLAMA
   ├── Tablo ve grafikler
   ├── Sonuç yorumlama
   └── Makale yazımı
```

## 🚀 Adım Adım Uygulama

### Adım 1: Ortam Hazırlama

```bash
# Gerekli paketleri yükle
pip install -r requirements_analysis.txt

# Jupyter notebook başlat (opsiyonel)
jupyter notebook
```

### Adım 2: Veri Yükleme

```bash
# Google Sheets'ten veri çek
python scripts/preprocessing/01_load_data.py
```

**Çıktılar:**
- `data/raw/main_dataset.csv`
- `data/raw/main_dataset.xlsx`
- `data/raw/metadata.json`

### Adım 3: Veri Temizleme

```bash
# Veriyi temizle ve hazırla
python scripts/preprocessing/02_clean_data.py
```

**Çıktılar:**
- `data/cleaned/cleaned_dataset.csv`
- `data/cleaned/summary_statistics.xlsx`
- `data/cleaned/cleaning_report.txt`

### Adım 4: Tanımlayıcı Analizler

```bash
# Tanımlayıcı istatistikler
python scripts/analysis/03_descriptive_stats.py
```

**Çıktılar:**
- `results/tables/descriptive_statistics.xlsx`
- `results/figures/` (grafikler)
- `results/reports/descriptive_report.txt`

### Adım 5: Hipotez Testleri

```bash
# Hipotez testleri ve grup karşılaştırmaları
python scripts/analysis/04_hypothesis_testing.py
```

**Çıktılar:**
- `results/tables/hypothesis_tests.xlsx`
- `results/tables/group_comparisons.xlsx`

### Adım 6: İleri Analizler

```bash
# Regresyon ve ileri analizler
python scripts/analysis/05_advanced_analysis.py
```

**Çıktılar:**
- `results/models/` (model sonuçları)
- `results/tables/regression_results.xlsx`

## 📊 Analiz Kontrol Listesi

### Veri Kalitesi
- [ ] Tüm değişkenler doğru yüklenmiş mi?
- [ ] Eksik veri oranları kabul edilebilir düzeyde mi? (<%20)
- [ ] Aykırı değerler kontrol edildi mi?
- [ ] Veri giriş hataları düzeltildi mi?

### İstatistiksel Varsayımlar
- [ ] Normallik testleri yapıldı mı?
- [ ] Varyans homojenliği kontrol edildi mi?
- [ ] Örneklem büyüklüğü yeterli mi?
- [ ] Bağımsızlık varsayımı sağlanıyor mu?

### Güvenilirlik
- [ ] Ölçeklerin Cronbach alpha değerleri hesaplandı mı? (>0.70)
- [ ] Test-retest güvenilirliği kontrol edildi mi? (eğer varsa)
- [ ] Inter-rater güvenilirlik hesaplandı mı? (eğer gerekiyorsa)

### Etik ve Raporlama
- [ ] Etik kurul onay numarası belirtildi mi?
- [ ] STROBE kontrol listesi dolduruldu mu?
- [ ] Tüm istatistiksel testler raporlandı mı?
- [ ] Güven aralıkları ve etki büyüklükleri hesaplandı mı?

## 🔧 Sorun Giderme

### Sorun: Google Sheets bağlantısı kurulamıyor
**Çözüm:**
```python
# Service account JSON dosyasının yolunu kontrol et
from google_sheets_api import GoogleSheetsAPI
sheets = GoogleSheetsAPI('dr-murzoglu-doktora.json')
```

### Sorun: Eksik paketler
**Çözüm:**
```bash
# Eksik paketi tek tek yükle
pip install pandas scipy matplotlib seaborn
```

### Sorun: Bellek hatası (büyük veri setleri)
**Çözüm:**
```python
# Veriyi parça parça yükle
df = pd.read_csv('file.csv', chunksize=1000)
```

## 📈 Performans İpuçları

1. **Veri Yükleme:**
   - Büyük dosyalar için `pickle` formatı kullanın
   - Gereksiz sütunları yükleme sırasında hariç tutun

2. **Analiz Hızlandırma:**
   - Numpy ve pandas vektörize işlemlerini kullanın
   - Loop yerine apply() fonksiyonlarını tercih edin

3. **Görselleştirme:**
   - Yüksek çözünürlük için dpi=300 kullanın
   - Büyük grafikler için plotly (interaktif) tercih edin

## 📚 Ek Kaynaklar

### Python İstatistik Paketleri
- **scipy.stats:** Temel istatistiksel testler
- **statsmodels:** Regresyon ve zaman serisi analizleri
- **pingouin:** Kullanıcı dostu istatistik fonksiyonları
- **scikit-learn:** Machine learning ve çapraz doğrulama

### Referans Dokümantasyon
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [SciPy Statistics](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Seaborn Gallery](https://seaborn.pydata.org/examples/index.html)

## 🎯 Yayın Hedefleri

### Öncelikli Analizler
1. Gruplar arası Beck Depresyon skorları karşılaştırması
2. EMBU ebeveyn tutumu analizleri
3. Kardeş ilişkileri değerlendirmesi
4. Risk faktörleri regresyon analizi

### Makale Planı
1. **Ana Makale:** Grup karşılaştırmaları ve temel bulgular
2. **İkinci Makale:** Kardeş ilişkileri odaklı analizler
3. **Üçüncü Makale:** Risk faktörleri ve prediktif modeller

## 📞 Destek

Analiz sürecinde sorun yaşarsanız:
1. Bu dokümandaki sorun giderme bölümünü kontrol edin
2. `scripts/` klasöründeki kodlardaki yorumları inceleyin
3. Error mesajlarını Google'da aratın
4. Stack Overflow'da benzer sorunları araştırın

---

*Son güncelleme: 20 Eylül 2025*