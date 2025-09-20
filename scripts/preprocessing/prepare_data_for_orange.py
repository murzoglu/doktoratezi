"""
prepare_data_for_orange.py
Orange3 için veriyi uygun formata dönüþtürür
"""

import pandas as pd
import os

def convert_to_orange_format():
    """CSV'yi Orange3 tab formatýna dönüþtürür"""

    # Temizlenmiþ veriyi yükle
    try:
        df = pd.read_csv('data/cleaned/cleaned_dataset.csv')
        print(f"[OK] Veri yuklendi: {df.shape}")
    except:
        print("[!] Once veri temizleme scriptini calistirin")
        return

    # Orange3 için özel format ayarlarý
    os.makedirs('data/orange3', exist_ok=True)

    # 1. Tab-separated format (.tab)
    # Orange3 bu formatý doðrudan okuyabilir
    df.to_csv('data/orange3/dataset.tab', sep='\t', index=False)
    print("[OK] Tab format: data/orange3/dataset.tab")

    # 2. CSV format (Orange3 uyumlu)
    df.to_csv('data/orange3/dataset.csv', index=False)
    print("[OK] CSV format: data/orange3/dataset.csv")

    # 3. Metadata dosyasý oluþtur
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
        f.write('\n'.join(metadata))

    print("[OK] Metadata: data/orange3/metadata.txt")

    # 4. Özet istatistikler
    summary = df.describe(include='all')
    summary.to_csv('data/orange3/summary_stats.csv')
    print("[OK] Ozet istatistikler: data/orange3/summary_stats.csv")

    print("\n[ORANGE3 KULLANIM]")
    print("-"*40)
    print("1. Orange3'u acin")
    print("2. File widget'i ekleyin")
    print("3. 'data/orange3/dataset.csv' dosyasini secin")
    print("4. Data Table widget'i ile veriyi gorun")
    print("5. Analizlerinizi baslatýn!")

    return df

if __name__ == "__main__":
    convert_to_orange_format()
