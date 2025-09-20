"""
Orange3 Kurulum ve Konfigürasyon Script'i
"""

import subprocess
import sys
import os

def install_orange_alternative():
    """Orange3 için alternatif kurulum yöntemleri"""

    print("="*60)
    print("ORANGE3 KURULUM KILAVUZU")
    print("="*60)

    print("\n[OPTION 1] Anaconda ile Kurulum (ÖNERİLEN)")
    print("-"*40)
    print("""
1. Anaconda'yı indirin: https://www.anaconda.com/download
2. Anaconda Prompt'u açın
3. Şu komutları çalıştırın:

   conda create -n orange3 python=3.11
   conda activate orange3
   conda install -c conda-forge orange3

4. Orange3'ü başlatın:
   orange-canvas
    """)

    print("\n[OPTION 2] Standalone Installer (EN KOLAY)")
    print("-"*40)
    print("""
Windows için hazır kurulum paketi:
1. https://orangedatamining.com/download/ adresine gidin
2. Windows installer'ı indirin (yaklaşık 500MB)
3. Kurulumu tamamlayın
4. Başlat menüsünden Orange3'ü açın
    """)

    print("\n[OPTION 3] pip ile kurulum (C++ Build Tools gerekli)")
    print("-"*40)
    print("""
1. Microsoft C++ Build Tools'u indirin:
   https://visualstudio.microsoft.com/visual-cpp-build-tools/

2. Kurulumda şunları seçin:
   - Desktop development with C++
   - Windows 10/11 SDK

3. Kurulum sonrası:
   pip install orange3
    """)

    print("\n[OPTION 4] Basitleştirilmiş pip kurulumu")
    print("-"*40)
    print("Sadece temel Orange3 widget'ları için:")

    packages = [
        'orange-canvas-core',
        'orange-widget-base',
        'pyqtgraph',
        'AnyQt'
    ]

    for pkg in packages:
        print(f"pip install {pkg}")

    return True

def prepare_data_for_orange():
    """Orange3 için veri hazırlama"""

    print("\n" + "="*60)
    print("ORANGE3 İÇİN VERİ HAZIRLAMA")
    print("="*60)

    script_content = '''"""
prepare_data_for_orange.py
Orange3 için veriyi uygun formata dönüştürür
"""

import pandas as pd
import os

def convert_to_orange_format():
    """CSV'yi Orange3 tab formatına dönüştürür"""

    # Temizlenmiş veriyi yükle
    try:
        df = pd.read_csv('data/cleaned/cleaned_dataset.csv')
        print(f"[OK] Veri yuklendi: {df.shape}")
    except:
        print("[!] Once veri temizleme scriptini calistirin")
        return

    # Orange3 için özel format ayarları
    os.makedirs('data/orange3', exist_ok=True)

    # 1. Tab-separated format (.tab)
    # Orange3 bu formatı doğrudan okuyabilir
    df.to_csv('data/orange3/dataset.tab', sep='\\t', index=False)
    print("[OK] Tab format: data/orange3/dataset.tab")

    # 2. CSV format (Orange3 uyumlu)
    df.to_csv('data/orange3/dataset.csv', index=False)
    print("[OK] CSV format: data/orange3/dataset.csv")

    # 3. Metadata dosyası oluştur
    metadata = []
    metadata.append("# Orange3 Dataset Metadata")
    metadata.append(f"# Rows: {df.shape[0]}")
    metadata.append(f"# Columns: {df.shape[1]}")
    metadata.append("# Variable Types:")

    for col in df.columns:
        dtype = str(df[col].dtype)
        if 'float' in dtype or 'int' in dtype:
            var_type = 'continuous'
        else:
            var_type = 'discrete'
        metadata.append(f"# {col}: {var_type}")

    with open('data/orange3/metadata.txt', 'w') as f:
        f.write('\\n'.join(metadata))

    print("[OK] Metadata: data/orange3/metadata.txt")

    # 4. Özet istatistikler
    summary = df.describe(include='all')
    summary.to_csv('data/orange3/summary_stats.csv')
    print("[OK] Ozet istatistikler: data/orange3/summary_stats.csv")

    print("\\n[ORANGE3 KULLANIM]")
    print("-"*40)
    print("1. Orange3'u acin")
    print("2. File widget'i ekleyin")
    print("3. 'data/orange3/dataset.csv' dosyasini secin")
    print("4. Data Table widget'i ile veriyi gorun")
    print("5. Analizlerinizi baslatın!")

    return df

if __name__ == "__main__":
    convert_to_orange_format()
'''

    # Script'i kaydet
    with open('scripts/preprocessing/prepare_data_for_orange.py', 'w') as f:
        f.write(script_content)

    print("[OK] Veri hazırlama scripti: scripts/preprocessing/prepare_data_for_orange.py")

    return True

def create_orange_workflow():
    """Orange3 için hazır workflow oluştur"""

    print("\n" + "="*60)
    print("ORANGE3 WORKFLOW ÖRNEĞİ")
    print("="*60)

    workflow = '''<?xml version='1.0' encoding='utf-8'?>
<scheme version="2.0" title="Klinik Çalışma Analizi">
    <nodes>
        <node id="0" name="File" position="(100, 200)">
            <properties>
                <property name="recent_paths">data/orange3/dataset.csv</property>
            </properties>
        </node>
        <node id="1" name="Data Table" position="(250, 100)" />
        <node id="2" name="Distributions" position="(250, 200)" />
        <node id="3" name="Box Plot" position="(250, 300)" />
        <node id="4" name="Correlations" position="(400, 200)" />
        <node id="5" name="Test and Score" position="(400, 300)" />
        <node id="6" name="t-SNE" position="(550, 200)" />
        <node id="7" name="Scatter Plot" position="(700, 200)" />
    </nodes>
    <links>
        <link source_node_id="0" sink_node_id="1" />
        <link source_node_id="0" sink_node_id="2" />
        <link source_node_id="0" sink_node_id="3" />
        <link source_node_id="0" sink_node_id="4" />
        <link source_node_id="0" sink_node_id="5" />
        <link source_node_id="0" sink_node_id="6" />
        <link source_node_id="6" sink_node_id="7" />
    </links>
</scheme>'''

    # Workflow'u kaydet
    os.makedirs('orange_workflows', exist_ok=True)
    with open('orange_workflows/clinical_analysis.ows', 'w') as f:
        f.write(workflow)

    print("[OK] Workflow kaydedildi: orange_workflows/clinical_analysis.ows")
    print("\nOrange3'te File > Open ile bu workflow'u açabilirsiniz")

    return True

def create_orange_guide():
    """Orange3 kullanım kılavuzu"""

    guide = '''# Orange3 Kullanım Kılavuzu - Klinik Çalışma

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
'''

    with open('ORANGE3_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide)

    print("[OK] Kullanım kılavuzu: ORANGE3_GUIDE.md")

    return True

def main():
    print("="*60)
    print("ORANGE3 KURULUM VE YAPILANDIRMA")
    print("="*60)

    # Kurulum seçenekleri
    install_orange_alternative()

    # Veri hazırlama
    prepare_data_for_orange()

    # Workflow oluştur
    create_orange_workflow()

    # Kullanım kılavuzu
    create_orange_guide()

    print("\n" + "="*60)
    print("ORANGE3 HAZIR!")
    print("="*60)
    print("\n[YAPILACAKLAR]")
    print("1. Orange3'ü yukarıdaki yöntemlerden biriyle kurun")
    print("2. python scripts/preprocessing/prepare_data_for_orange.py")
    print("3. Orange3'ü açın ve orange_workflows/clinical_analysis.ows dosyasını yükleyin")
    print("\nDetaylar için: ORANGE3_GUIDE.md")

if __name__ == "__main__":
    main()