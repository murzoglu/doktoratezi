"""
install_statistical_tools.py
İstatistiksel analiz araçlarını yükler ve test eder
"""

import subprocess
import sys
import importlib

def install_package(package):
    """Tek bir paketi yükler"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except:
        return False

def check_package(package_name, import_name=None):
    """Paketin yüklü olup olmadığını kontrol eder"""
    if import_name is None:
        import_name = package_name.split('==')[0].replace('-', '_')

    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False

def main():
    print("="*60)
    print("İSTATİSTİKSEL ANALİZ ARAÇLARI KURULUMU")
    print("="*60)

    # Kritik paketler listesi
    critical_packages = [
        ('scipy', 'scipy'),
        ('statsmodels', 'statsmodels'),
        ('pingouin', 'pingouin'),
        ('scikit-learn', 'sklearn'),
        ('factor-analyzer', 'factor_analyzer'),
    ]

    # İsteğe bağlı gelişmiş paketler
    optional_packages = [
        ('pymc', 'pymc'),  # Bayesian
        ('lifelines', 'lifelines'),  # Survival analysis
        ('dabest', 'dabest'),  # Effect sizes
    ]

    print("\n[KRİTİK PAKETLER]")
    print("-"*40)

    installed = []
    failed = []

    for package, import_name in critical_packages:
        print(f"Kontrol ediliyor: {package}...", end=" ")

        if check_package(package, import_name):
            print("[OK] Yuklu")
            installed.append(package)
        else:
            print("Yükleniyor...")
            if install_package(package):
                print(f"  [OK] {package} yuklendi")
                installed.append(package)
            else:
                print(f"  [HATA] {package} yuklenemedi")
                failed.append(package)

    print("\n[ÖZET]")
    print("-"*40)
    print(f"Yüklü paketler: {len(installed)}")
    print(f"Başarısız: {len(failed)}")

    if failed:
        print(f"\nBaşarısız paketler: {', '.join(failed)}")
        print("\nManuel yükleme için:")
        for pkg in failed:
            print(f"  pip install {pkg}")

    # Test scriptleri oluştur
    print("\n[TEST SCRİPTLERİ OLUŞTURULUYOR]")
    print("-"*40)

    test_code = '''
# Test: İstatistiksel paketlerin çalışıp çalışmadığını kontrol et
import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
import pingouin as pg
from sklearn.linear_model import LinearRegression

print("[OK] Tum temel paketler basariyla import edildi!")

# Basit test
data = pd.DataFrame({
    'x': np.random.normal(0, 1, 100),
    'y': np.random.normal(0, 1, 100)
})

# T-test
t_stat, p_value = stats.ttest_ind(data['x'], data['y'])
print(f"\\nT-test örneği: t={t_stat:.3f}, p={p_value:.3f}")

print("\\n[OK] Test basarili!")
'''

    with open('scripts/test_packages.py', 'w', encoding='utf-8') as f:
        f.write(test_code)

    print("[OK] Test scripti olusturuldu: scripts/test_packages.py")

    # JAMOVI benzeri GUI araçları önerisi
    print("\n[SPSS/JAMOVI BENZERİ GUI ARAÇLARI]")
    print("-"*40)
    print("Python'da SPSS benzeri GUI araçları:")
    print()
    print("1. JASP (ücretsiz): https://jasp-stats.org/")
    print("   - SPSS benzeri arayüz")
    print("   - R tabanlı")
    print()
    print("2. jamovi (ücretsiz): https://www.jamovi.org/")
    print("   - Modern arayüz")
    print("   - R tabanlı, Python entegrasyonu var")
    print()
    print("3. Orange (ücretsiz): https://orange.biolab.si/")
    print("   - Görsel programlama")
    print("   - Python tabanlı")
    print("   Yükleme: pip install orange3")
    print()
    print("4. BlueSky Statistics (ücretsiz): https://www.blueskystatistics.com/")
    print("   - SPSS'e en benzer arayüz")
    print("   - R tabanlı")

    print("\n" + "="*60)
    print("KURULUM TAMAMLANDI!")
    print("="*60)

if __name__ == "__main__":
    main()