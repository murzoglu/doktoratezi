"""
01_load_data.py
Google Sheets'ten veri yükleme ve birleştirme
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Ana dizini path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from google_sheets_api import GoogleSheetsAPI

def load_main_dataset():
    """Ana veri setini yükler"""

    print("="*60)
    print("VERİ YÜKLEME BAŞLIYOR")
    print("="*60)

    # Google Sheets API başlat
    sheets = GoogleSheetsAPI('dr-murzoglu-doktora.json')

    # Ana veri tablosu ID'si
    SHEET_ID = "1AIeTlphqgSLy8ESwa5lblhSgH_ZbHTvX8RafW3vshG8"

    try:
        print("\n[1/3] Google Sheets'ten veri okunuyor...")

        # Tüm veriyi oku
        df = sheets.sheets_to_dataframe(SHEET_ID, 'A:BZ', header=True)

        print(f"[OK] {df.shape[0]} satır, {df.shape[1]} sütun veri yüklendi")

        # Sütun isimlerini temizle
        df.columns = df.columns.str.strip()

        # İlk kontroller
        print("\n[2/3] Veri yapısı kontrol ediliyor...")
        print(f"  - Toplam katılımcı: {df.shape[0]}")
        print(f"  - Değişken sayısı: {df.shape[1]}")

        # Grup değişkeni oluştur (DM tanı tarihi boş değilse diyabet grubu)
        if 'DM Tanı Tarihi' in df.columns:
            df['Grup'] = df['DM Tanı Tarihi'].notna().astype(int)
            df['Grup'] = df['Grup'].map({0: 'Kontrol', 1: 'Diyabet'})
            print(f"  - Diyabet grubu: {(df['Grup'] == 'Diyabet').sum()}")
            print(f"  - Kontrol grubu: {(df['Grup'] == 'Kontrol').sum()}")

        # Veriyi kaydet
        print("\n[3/3] Veri kaydediliyor...")

        # Raw data olarak kaydet
        os.makedirs('data/raw', exist_ok=True)
        df.to_csv('data/raw/main_dataset.csv', index=False, encoding='utf-8-sig')
        df.to_excel('data/raw/main_dataset.xlsx', index=False)

        print("[OK] data/raw/main_dataset.csv")
        print("[OK] data/raw/main_dataset.xlsx")

        return df

    except Exception as e:
        print(f"\n[HATA] Veri yüklenemedi: {e}")
        return None

def create_metadata(df):
    """Veri seti meta bilgilerini oluşturur"""

    metadata = {
        'load_date': datetime.now().isoformat(),
        'n_rows': df.shape[0],
        'n_cols': df.shape[1],
        'columns': list(df.columns),
        'dtypes': df.dtypes.astype(str).to_dict(),
        'missing_counts': df.isnull().sum().to_dict(),
        'missing_percentages': (df.isnull().sum() * 100 / len(df)).round(2).to_dict()
    }

    # Metadata'yı JSON olarak kaydet
    import json
    with open('data/raw/metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print("\n[OK] Metadata oluşturuldu: data/raw/metadata.json")

    return metadata

def generate_data_summary(df):
    """Veri özet raporu oluşturur"""

    summary = []
    summary.append("="*60)
    summary.append("VERİ SETİ ÖZET RAPORU")
    summary.append("="*60)
    summary.append(f"\nYükleme Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    summary.append(f"Toplam Satır: {df.shape[0]}")
    summary.append(f"Toplam Sütun: {df.shape[1]}")

    # Değişken kategorileri
    summary.append("\nDEĞİŞKEN KATEGORİLERİ:")
    summary.append("-"*40)

    # Beck soruları
    beck_cols = [col for col in df.columns if col.startswith('Beck')]
    summary.append(f"Beck Depresyon Ölçeği: {len(beck_cols)} soru")

    # EMBU soruları
    embu_cols = [col for col in df.columns if 'EMBU' in col or 'embu' in col.lower()]
    summary.append(f"EMBU Ölçeği: {len(embu_cols)} soru")

    # Demografik değişkenler
    demo_cols = ['Katılımcı No', 'Anne Doğum Tarihi', 'Çocuk Sayısı',
                 'Katılımcı Çocuk Doğum Tarihi', 'Katılımcı Çocuk Cinsiyet',
                 'Medeni Durum', 'Eğitim Durumu', 'Çalışma Durumu']
    demo_present = [col for col in demo_cols if col in df.columns]
    summary.append(f"Demografik Değişkenler: {len(demo_present)}")

    # Eksik veri özeti
    summary.append("\nEKSİK VERİ ÖZETİ:")
    summary.append("-"*40)

    missing_summary = df.isnull().sum()
    high_missing = missing_summary[missing_summary > len(df) * 0.1]

    if len(high_missing) > 0:
        summary.append(f"%10'dan fazla eksik veri içeren sütunlar:")
        for col, count in high_missing.items():
            pct = (count / len(df)) * 100
            summary.append(f"  - {col}: {count} ({pct:.1f}%)")
    else:
        summary.append("Tüm değişkenlerde eksik veri oranı %10'un altında.")

    # Grup dağılımı
    if 'Grup' in df.columns:
        summary.append("\nGRUP DAĞILIMI:")
        summary.append("-"*40)
        grup_counts = df['Grup'].value_counts()
        for grup, count in grup_counts.items():
            pct = (count / len(df)) * 100
            summary.append(f"  {grup}: {count} ({pct:.1f}%)")

    # Raporu kaydet
    report_path = 'data/raw/data_summary.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary))

    print('\n'.join(summary))
    print(f"\n[OK] Özet rapor kaydedildi: {report_path}")

def main():
    """Ana fonksiyon"""

    # Veriyi yükle
    df = load_main_dataset()

    if df is not None:
        # Metadata oluştur
        metadata = create_metadata(df)

        # Özet rapor oluştur
        generate_data_summary(df)

        print("\n" + "="*60)
        print("VERİ YÜKLEME TAMAMLANDI!")
        print("="*60)
        print("\nSonraki adım: python scripts/preprocessing/02_clean_data.py")

        return df
    else:
        print("\n[!] Veri yükleme başarısız oldu.")
        return None

if __name__ == "__main__":
    df = main()