"""
Orange3 Test Script
Test Orange3 kurulumunu kontrol eder
"""

import sys
import importlib

def test_orange3():
    """Orange3 kurulumunu test et"""

    print("="*60)
    print("ORANGE3 KURULUM TESTİ")
    print("="*60)

    modules_to_test = [
        ('Orange', 'Orange core'),
        ('Orange.data', 'Orange data module'),
        ('Orange.widgets', 'Orange widgets'),
        ('Orange.classification', 'Classification module'),
        ('Orange.regression', 'Regression module'),
        ('Orange.evaluation', 'Evaluation module'),
        ('Orange.preprocess', 'Preprocessing module'),
        ('Orange.statistics', 'Statistics module'),
    ]

    success_count = 0
    failed_modules = []

    for module_name, description in modules_to_test:
        try:
            module = importlib.import_module(module_name)
            print(f"[OK] {description} ({module_name})")
            success_count += 1
        except ImportError as e:
            print(f"[HATA] {description} ({module_name}): {str(e)}")
            failed_modules.append(module_name)

    print("\n" + "="*60)
    print("TEST SONUCU")
    print("="*60)
    print(f"Başarılı: {success_count}/{len(modules_to_test)}")
    print(f"Başarısız: {len(failed_modules)}/{len(modules_to_test)}")

    if failed_modules:
        print("\nBaşarısız modüller:")
        for module in failed_modules:
            print(f"  - {module}")

    # Versiyon bilgisi
    if success_count > 0:
        try:
            import Orange
            print(f"\nOrange3 Versiyon: {Orange.__version__}")
        except:
            print("\nVersiyon bilgisi alınamadı")

    return success_count == len(modules_to_test)

def test_orange_canvas():
    """Orange Canvas'ı test et"""

    print("\n" + "="*60)
    print("ORANGE CANVAS TESTİ")
    print("="*60)

    try:
        import Orange.canvas
        print("[OK] Orange Canvas modülü yüklü")

        # Canvas'ı başlatmayı test et (GUI açmadan)
        try:
            from Orange.canvas.application.canvasmain import CanvasMainWindow
            print("[OK] Orange Canvas GUI modülleri hazır")
            print("\nOrange Canvas'ı başlatmak için terminalde şu komutu çalıştırın:")
            print("  python -m Orange.canvas")
            print("veya")
            print("  orange-canvas")
            return True
        except ImportError as e:
            print(f"[UYARI] Canvas GUI modülleri eksik: {e}")
            return False

    except ImportError:
        print("[HATA] Orange Canvas modülü bulunamadı")
        return False

def test_data_loading():
    """Veri yükleme test et"""

    print("\n" + "="*60)
    print("VERİ YÜKLEME TESTİ")
    print("="*60)

    try:
        import Orange
        import numpy as np

        # Basit bir veri seti oluştur
        data = Orange.data.Table.from_numpy(
            Orange.data.Domain(
                [Orange.data.ContinuousVariable('x'),
                 Orange.data.ContinuousVariable('y')],
                Orange.data.DiscreteVariable('class', values=['A', 'B'])
            ),
            np.array([[1.0, 2.0], [3.0, 4.0]]),
            np.array([0, 1])
        )

        print(f"[OK] Veri yükleme başarılı")
        print(f"  - Satır sayısı: {len(data)}")
        print(f"  - Değişken sayısı: {len(data.domain.attributes)}")
        print(f"  - Hedef değişken: {data.domain.class_var}")
        return True

    except Exception as e:
        print(f"[HATA] Veri yükleme başarısız: {e}")
        return False

if __name__ == "__main__":
    # Testleri çalıştır
    orange_ok = test_orange3()
    canvas_ok = test_orange_canvas()
    data_ok = test_data_loading()

    # Özet
    print("\n" + "="*60)
    print("GENEL DURUM")
    print("="*60)

    if orange_ok and canvas_ok and data_ok:
        print("[OK] Orange3 tamamen kurulu ve çalışıyor!")
        print("\nOrange3'ü başlatmak için:")
        print("  1. Komut satırından: orange-canvas")
        print("  2. Python'dan: python -m Orange.canvas")
    elif orange_ok:
        print("[UYARI] Orange3 kısmen kurulu")
        print("Tam kurulum için: pip install orange3")
    else:
        print("[HATA] Orange3 kurulu değil")
        print("\nKurulum önerileri:")
        print("  1. pip install orange3")
        print("  2. conda install -c conda-forge orange3")
        print("  3. Standalone installer: https://orangedatamining.com/download/")