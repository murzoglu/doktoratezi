# 🍊 Orange3 Hızlı Başlangıç Kılavuzu

## 📥 Kurulum (EN KOLAY YOL)

### Windows için Standalone Kurulum:
1. **İndirme Linki:** https://orangedatamining.com/download/
2. **"Orange3-3.36.2-Miniconda-x86_64.exe"** dosyasını indirin (500MB)
3. Kurulum sihirbazını takip edin
4. **Başlat Menüsü → Orange3** ile açın

## 🚀 İlk Kullanım

### Adım 1: Veriyi Hazırlayın
```bash
# Önce veriyi Orange3 formatına dönüştürün
python scripts/preprocessing/prepare_data_for_orange.py
```

Bu komut şu dosyaları oluşturacak:
- `data/orange3/dataset.csv` - Ana veri
- `data/orange3/dataset.tab` - Tab formatı
- `data/orange3/metadata.txt` - Değişken bilgileri

### Adım 2: Orange3'ü Açın ve Veri Yükleyin

1. **Orange3'ü başlatın**
2. **Sol panel**den **"Data → File"** widget'ini sürükleyin
3. **File widget**'ine çift tıklayın
4. **Browse** ile `data/orange3/dataset.csv` dosyasını seçin
5. **Data Table** widget'i ekleyerek veriyi görün

## 📊 Temel Analizler (5 Dakikada)

### 1️⃣ Tanımlayıcı İstatistikler
```
File → Feature Statistics (değişken özeti)
     → Distributions (histogramlar)
     → Box Plot (kutu grafikleri)
```

### 2️⃣ Grup Karşılaştırması (Diyabet vs Kontrol)
```
File → Select Columns (Grup'u target yap)
     → Box Plot (gruplar arası)
     → Test & Score (istatistiksel testler)
```

### 3️⃣ Korelasyon Analizi
```
File → Correlations (korelasyon matrisi)
     → Scatter Plot (saçılım grafikleri)
```

### 4️⃣ Beck Depresyon Analizi
```
File → Select Columns (Beck_* değişkenleri)
     → Box Plot (Grup'a göre)
     → Linear Regression
```

## 🎯 Klinik Çalışma için Özel Workflow

### Hazır Workflow'u Yükleyin:
1. Orange3'te **File → Open**
2. `orange_workflows/clinical_analysis.ows` dosyasını seçin
3. Otomatik olarak tüm widget'lar yüklenecek

### Workflow İçeriği:
- **File:** Veri yükleme
- **Data Table:** Veri görüntüleme
- **Distributions:** Dağılımlar
- **Box Plot:** Grup karşılaştırmaları
- **Correlations:** Korelasyon matrisi
- **Test & Score:** Model değerlendirme
- **t-SNE:** Boyut indirgeme
- **Scatter Plot:** Görselleştirme

## 🔧 Sık Kullanılan Widget'lar

### Veri İşleme
| Widget | İşlevi |
|--------|--------|
| **Select Columns** | Değişken seçimi |
| **Select Rows** | Veri filtreleme |
| **Impute** | Eksik veri doldurma |
| **Discretize** | Sürekli → Kategorik |

### Görselleştirme
| Widget | İşlevi |
|--------|--------|
| **Box Plot** | Kutu grafikleri |
| **Scatter Plot** | Saçılım grafikleri |
| **Distributions** | Histogramlar |
| **Heat Map** | Korelasyon ısı haritası |

### İstatistiksel Analiz
| Widget | İşlevi |
|--------|--------|
| **Test & Score** | Model karşılaştırma |
| **Correlations** | Korelasyon analizi |
| **Feature Statistics** | Tanımlayıcı istatistikler |
| **ANOVA** | Varyans analizi |

### Machine Learning
| Widget | İşlevi |
|--------|--------|
| **Logistic Regression** | Grup tahmini |
| **Random Forest** | Sınıflandırma |
| **Linear Regression** | Regresyon |
| **ROC Analysis** | Model performansı |

## 💡 Pratik İpuçları

### Grup Karşılaştırması Yapmak İçin:
1. **Select Columns** widget'i ekleyin
2. "Grup" değişkenini **target** olarak işaretleyin
3. **Box Plot** ekleyin ve "Group by" olarak Grup'u seçin

### Sonuçları Kaydetmek İçin:
- **Grafikler:** Widget'ta sağ tık → Save Image
- **Tablolar:** Data Table → Save As
- **Raporlar:** File menüsü → Report

### Eksik Veri Problemleri:
1. **Impute** widget'i ekleyin
2. Method: "Average" (sayısal) veya "Most frequent" (kategorik)
3. Sonucu yeni bir Data Table'da görün

## 📈 Örnek Analiz Senaryoları

### Senaryo 1: Beck Skorları Grup Karşılaştırması
```
File → Select Columns (Beck_Total_Score, Grup)
     → Box Plot
     → T-test (Python Script widget ile)
```

### Senaryo 2: Prediktif Model Oluşturma
```
File → Data Sampler (70/30 split)
     → Test & Score
        - Logistic Regression
        - Random Forest
        - SVM
     → ROC Analysis
```

### Senaryo 3: Kümeleme Analizi
```
File → Distances → Hierarchical Clustering
                  → Dendrogram
```

## 🆘 Sorun Giderme

### "File not found" hatası:
- Dosya yolunda Türkçe karakter olmamasına dikkat edin
- Mutlak yol yerine göreceli yol kullanın

### Widget bağlantı hatası:
- Veri tiplerinin uyumlu olduğundan emin olun
- Bağlantı oklarının doğru yönde olduğunu kontrol edin

### Bellek hatası:
- **Data Sampler** ile veriyi örnekleyin
- Gereksiz değişkenleri **Select Columns** ile çıkarın

## 📚 Ek Kaynaklar

- **Video Eğitimler:** https://www.youtube.com/OrangeDataMining
- **Örnek Workflow'lar:** https://orange.biolab.si/workflows/
- **Widget Dokümantasyonu:** https://orange3.readthedocs.io/

## ✅ Kontrol Listesi

- [ ] Orange3 kuruldu
- [ ] Veri Orange formatına dönüştürüldü
- [ ] İlk workflow oluşturuldu
- [ ] Temel widget'lar öğrenildi
- [ ] İlk analiz tamamlandı

---

**Hazır mısınız?** Orange3'ü açın ve analizlerinize başlayın! 🚀