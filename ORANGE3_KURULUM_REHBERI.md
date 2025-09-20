# Orange3 Kurulum Rehberi

## Durum
Orange3 kurulumu için Visual C++ Build Tools gerekli. Aşağıdaki alternatiflerden birini kullanın.

## OPTION 1: Standalone Installer (EN KOLAY - ÖNERİLEN)
1. **İndirme:** https://orangedatamining.com/download/
2. **Orange3-3.36.2-Miniconda-x86_64.exe** dosyasını indirin (500MB)
3. Kurulum sihirbazını takip edin
4. **Başlat Menüsü → Orange3** ile açın

## OPTION 2: Anaconda ile Kurulum
```bash
conda create -n orange3 python=3.11
conda activate orange3
conda install -c conda-forge orange3
orange-canvas
```

## OPTION 3: Visual C++ Build Tools Kurarak pip ile
1. **Microsoft C++ Build Tools İndirme:**
   https://visualstudio.microsoft.com/visual-cpp-build-tools/

2. **Kurulumda seçin:**
   - Desktop development with C++
   - Windows 10/11 SDK
   - MSVC v143 - VS 2022 C++ x64/x86 build tools

3. **Kurulum sonrası terminali yeniden açın ve:**
```bash
pip install orange3
```

## OPTION 4: Pre-built Wheel Dosyaları
Python 3.11 için pre-built wheel:
```bash
pip install https://pypi.org/packages/cp311/orange3
```

## Mevcut Kurulumlar

### ✅ Başarıyla Kuruldu:
- numpy 2.2.6
- scipy 1.16.1
- scikit-learn 1.7.2
- matplotlib 3.10.6
- pandas
- PyQt5 5.15.11
- pyqtgraph 0.13.7
- bottleneck 1.6.0

### ❌ Kurulum Başarısız:
- Orange3 (Visual C++ Build Tools eksik)
- openTSNE (C compiler gerekli)

## Test Komutu
```bash
python test_orange3.py
```

## GitHub'dan Klonlanan Kaynak
Orange3 kaynak kodu başarıyla klonlandı:
```
D:\GitHub Repos\doktoratezi\orange3\
```

## Sonraki Adımlar
1. **Standalone installer kullanın** (en kolay)
2. VEYA Anaconda/Miniconda kullanın
3. VEYA Visual C++ Build Tools kurun

## Veri Hazırlama
Orange3 kurulduktan sonra:
```bash
python scripts/preprocessing/prepare_data_for_orange.py
```

Bu komut veriyi Orange3 formatına dönüştürecek.