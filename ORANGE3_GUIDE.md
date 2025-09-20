# Orange3 Kullanım Kılavuzu - Klinik Çalışma

## 1. Kurulum

### Windows Standalone (Önerilen)
1. https://orangedatamining.com/download/ adresinden indirin
2. Installer'ı çalıştırın (500MB)
3. Başlat menüsünden Orange3'ü açın

### Anaconda ile
```bash
conda create -n orange3 python=3.11
conda activate orange3
conda install -c conda-forge orange3
orange-canvas
```

## 2. Veri Yükleme

### Adım 1: Veriyi Hazırlayın
```bash
python scripts/preprocessing/prepare_data_for_orange.py
```

### Adım 2: Orange3'te Açın
1. Orange3'ü başlatın
2. Sol panelden "Data" > "File" widget'ini sürükleyin
3. File widget'ine çift tıklayın
4. "data/orange3/dataset.csv" dosyasını seçin

## 3. Temel Analizler

### Tanımlayıcı İstatistikler
1. **Data Table**: Veriyi tablo olarak görün
2. **Feature Statistics**: Değişken istatistikleri
3. **Distributions**: Histogramlar
4. **Box Plot**: Kutu grafikleri

### Grup Karşılaştırmaları
1. **Select Columns**: "Grup" değişkenini seçin
2. **Box Plot**: Gruplar arası karşılaştırma
3. **Test & Score**: İstatistiksel testler

### Korelasyon Analizi
1. **Correlations**: Korelasyon matrisi
2. **Scatter Plot**: Saçılım grafikleri
3. **Linear Regression**: Regresyon analizi

## 4. İleri Analizler

### Sınıflandırma (Grup Tahmini)
```
File → Select Columns → Test & Score
                     ↓
              [Logistic Regression]
              [Random Forest]
              [SVM]
```

### Kümeleme Analizi
```
File → Distances → Hierarchical Clustering → Dendrogram
```

### Boyut İndirgeme
```
File → PCA → Scatter Plot
File → t-SNE → Scatter Plot
```

## 5. Widget'lar ve İşlevleri

### Veri İşleme
- **Select Columns**: Değişken seçimi
- **Select Rows**: Satır filtreleme
- **Impute**: Eksik veri doldurma
- **Discretize**: Sürekli → Kategorik

### Görselleştirme
- **Box Plot**: Kutu grafikleri
- **Scatter Plot**: Saçılım grafikleri
- **Distributions**: Histogramlar
- **Heat Map**: Isı haritası
- **Violin Plot**: Keman grafikleri

### İstatistik
- **Test & Score**: Model değerlendirme
- **Correlations**: Korelasyon analizi
- **Feature Statistics**: Özet istatistikler
- **Rank**: Değişken önem sıralaması

### Machine Learning
- **Logistic Regression**: Lojistik regresyon
- **Linear Regression**: Doğrusal regresyon
- **Random Forest**: Rastgele orman
- **SVM**: Destek vektör makineleri
- **Neural Network**: Yapay sinir ağları

## 6. Örnek İş Akışları

### Beck Depresyon Analizi
```
File → Select Columns (Beck_*) → Box Plot (by Grup)
                               → Test & Score
                               → ROC Analysis
```

### Grup Karşılaştırması
```
File → Select Columns (Grup as target)
     → Data Sampler (70/30 split)
     → Test & Score → Confusion Matrix
                    → ROC Analysis
```

## 7. Sonuçları Dışa Aktarma

### Grafikler
- Widget'ta sağ tık → "Save Image"
- Format: PNG, SVG, PDF

### Tablolar
- Data Table'da "Save As"
- Format: CSV, Excel, Tab

### Raporlar
- File menüsü → "Report"
- Tüm analizleri HTML olarak kaydet

## 8. İpuçları

### Performans
- Büyük veriler için "Sample" widget kullanın
- PCA ile boyut indirgeyin
- Gereksiz değişkenleri çıkarın

### Görselleştirme
- Renk kodlaması için "Color" seçeneğini kullanın
- Interactive grafikler için zoom/pan
- Multiple plots için "Subplots" özelliği

### Hata Ayıklama
- Widget'lar arası bağlantıları kontrol edin
- Veri tiplerini doğrulayın
- Eksik veri uyarılarını takip edin

## 9. Klinik Çalışma için Özel Analizler

### Güvenilirlik Analizi
```python
# Orange3'te doğrudan Cronbach's alpha yok
# Python Script widget'i ile ekleyin:

import numpy as np
from Orange.data import Table

def cronbach_alpha(data):
    items = data.X
    n_items = items.shape[1]
    item_variances = np.var(items, axis=0, ddof=1)
    total_variance = np.var(np.sum(items, axis=1), ddof=1)
    alpha = (n_items / (n_items - 1)) * (1 - np.sum(item_variances) / total_variance)
    return alpha

out_data = in_data
alpha = cronbach_alpha(in_data)
print(f"Cronbach's Alpha: {alpha:.3f}")
```

### Effect Size Hesaplama
```python
# Python Script widget'i
import numpy as np
from scipy import stats

def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    d = (np.mean(group1) - np.mean(group2)) / pooled_std
    return d
```

## 10. Kaynaklar

- [Orange3 Documentation](https://orange3.readthedocs.io/)
- [Video Tutorials](https://www.youtube.com/OrangeDataMining)
- [Example Workflows](https://orange.biolab.si/workflows/)
- [Widget Catalog](https://orange.biolab.si/widget-catalog/)

---

**Hazırlayan**: Doktora Tezi Analiz Sistemi
**Tarih**: 20 Eylül 2025
