"""
02_clean_data.py
Veri temizleme ve hazırlama
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_raw_data():
    """Ham veriyi yükler"""
    try:
        df = pd.read_csv('data/raw/main_dataset.csv')
        print(f"[OK] Ham veri yüklendi: {df.shape[0]} satır, {df.shape[1]} sütun")
        return df
    except Exception as e:
        print(f"[HATA] Veri yüklenemedi: {e}")
        return None

def clean_column_names(df):
    """Sütun isimlerini temizler"""
    # Türkçe karakterleri değiştir
    replacements = {
        'ç': 'c', 'Ç': 'C',
        'ğ': 'g', 'Ğ': 'G',
        'ı': 'i', 'İ': 'I',
        'ö': 'o', 'Ö': 'O',
        'ş': 's', 'Ş': 'S',
        'ü': 'u', 'Ü': 'U'
    }

    new_columns = []
    for col in df.columns:
        new_col = col
        for tr_char, en_char in replacements.items():
            new_col = new_col.replace(tr_char, en_char)
        # Boşlukları alt çizgi ile değiştir
        new_col = new_col.replace(' ', '_')
        # Özel karakterleri kaldır
        new_col = ''.join(c if c.isalnum() or c == '_' else '' for c in new_col)
        new_columns.append(new_col)

    df.columns = new_columns
    print(f"[OK] Sütun isimleri temizlendi")
    return df

def handle_missing_values(df):
    """Eksik değerleri işler"""

    print("\n[EKSIK DEĞER ANALİZİ]")
    print("-"*40)

    # Eksik değer sayıları
    missing_counts = df.isnull().sum()
    missing_pct = (missing_counts / len(df)) * 100

    # Eksik değer raporu
    missing_report = pd.DataFrame({
        'Missing_Count': missing_counts,
        'Missing_Percent': missing_pct
    })
    missing_report = missing_report[missing_report['Missing_Count'] > 0]
    missing_report = missing_report.sort_values('Missing_Percent', ascending=False)

    if len(missing_report) > 0:
        print(f"Eksik değer içeren sütun sayısı: {len(missing_report)}")
        print("\nEn çok eksik değer içeren 10 sütun:")
        print(missing_report.head(10))

        # Strateji 1: %50'den fazla eksik olan sütunları çıkar
        high_missing_cols = missing_report[missing_report['Missing_Percent'] > 50].index
        if len(high_missing_cols) > 0:
            print(f"\n[!] %50'den fazla eksik değer içeren {len(high_missing_cols)} sütun çıkarılıyor...")
            df = df.drop(columns=high_missing_cols)

        # Strateji 2: Sayısal değişkenler için median ile doldur
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().any():
                median_val = df[col].median()
                df[col].fillna(median_val, inplace=True)

        # Strateji 3: Kategorik değişkenler için mod ile doldur
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().any():
                mode_val = df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown'
                df[col].fillna(mode_val, inplace=True)

        print(f"[OK] Eksik değerler işlendi")
    else:
        print("Eksik değer bulunamadı.")

    return df

def create_derived_variables(df):
    """Türetilmiş değişkenler oluşturur"""

    print("\n[TÜRETİLMİŞ DEĞİŞKENLER]")
    print("-"*40)

    # Beck Depresyon toplam skoru
    beck_cols = [col for col in df.columns if col.startswith('Beck_')]
    if beck_cols:
        df['Beck_Total_Score'] = df[beck_cols].sum(axis=1)
        print(f"[OK] Beck toplam skor hesaplandı")

        # Beck kategorileri (0-13: Minimal, 14-19: Hafif, 20-28: Orta, 29-63: Şiddetli)
        df['Beck_Category'] = pd.cut(df['Beck_Total_Score'],
                                     bins=[0, 13, 19, 28, 63],
                                     labels=['Minimal', 'Hafif', 'Orta', 'Siddetli'])
        print(f"[OK] Beck depresyon kategorileri oluşturuldu")

    # Yaş hesaplama (eğer doğum tarihleri varsa)
    date_cols = [col for col in df.columns if 'Dogum_Tarihi' in col]
    for col in date_cols:
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                age_col = col.replace('Dogum_Tarihi', 'Yas')
                df[age_col] = (pd.Timestamp.now() - df[col]).dt.days / 365.25
                df[age_col] = df[age_col].round(1)
                print(f"[OK] {age_col} hesaplandı")
            except:
                pass

    # Aile büyüklüğü kategorisi
    if 'Cocuk_Sayisi' in df.columns:
        df['Aile_Buyuklugu'] = pd.cut(df['Cocuk_Sayisi'],
                                      bins=[0, 1, 2, 3, 10],
                                      labels=['Tek_Cocuk', '2_Cocuk', '3_Cocuk', '4+_Cocuk'])
        print(f"[OK] Aile büyüklüğü kategorileri oluşturuldu")

    return df

def encode_categorical_variables(df):
    """Kategorik değişkenleri kodlar"""

    print("\n[KATEGORİK DEĞİŞKEN KODLAMA]")
    print("-"*40)

    # Binary kodlama için sütunlar
    binary_mappings = {
        'Cinsiyet': {'Erkek': 1, 'Kiz': 0, 'E': 1, 'K': 0, '1': 1, '0': 0},
        'Medeni_Durum': {'Evli': 1, 'Bekar': 0, '1': 1, '0': 0},
        'Calisma_Durumu': {'Calisiyor': 1, 'Calismiyor': 0, '1': 1, '0': 0},
        'Anne_Antidepresan': {'Evet': 1, 'Hayir': 0, '1': 1, '0': 0}
    }

    for col, mapping in binary_mappings.items():
        if col in df.columns:
            df[f'{col}_Coded'] = df[col].map(mapping)
            print(f"[OK] {col} kodlandı")

    # Ordinal kodlama için sütunlar
    ordinal_mappings = {
        'Egitim_Durumu': {
            'Ilkokul': 1, 'Ortaokul': 2, 'Lise': 3,
            'Onlisans': 4, 'Lisans': 5, 'Lisansustu': 6
        }
    }

    for col, mapping in ordinal_mappings.items():
        if col in df.columns:
            df[f'{col}_Coded'] = df[col].map(mapping)
            print(f"[OK] {col} kodlandı")

    return df

def remove_outliers(df, columns=None, method='iqr', threshold=3):
    """Aykırı değerleri tespit eder ve işler"""

    print("\n[AYKIRI DEĞER ANALİZİ]")
    print("-"*40)

    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns

    outlier_report = []

    for col in columns:
        if col.endswith('_Score') or col.startswith('Beck_'):
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
            elif method == 'zscore':
                mean = df[col].mean()
                std = df[col].std()
                lower_bound = mean - threshold * std
                upper_bound = mean + threshold * std

            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            if len(outliers) > 0:
                outlier_report.append({
                    'Column': col,
                    'Outlier_Count': len(outliers),
                    'Outlier_Percent': (len(outliers) / len(df)) * 100
                })

    if outlier_report:
        outlier_df = pd.DataFrame(outlier_report)
        print(outlier_df)
        print(f"\n[!] Aykırı değerler tespit edildi ancak veri setinde tutuldu.")
        print("    (Klinik çalışmalarda aykırı değerler önemli bilgi içerebilir)")

    return df

def save_cleaned_data(df):
    """Temizlenmiş veriyi kaydeder"""

    print("\n[VERİ KAYDETME]")
    print("-"*40)

    # Cleaned klasörünü oluştur
    import os
    os.makedirs('data/cleaned', exist_ok=True)

    # CSV olarak kaydet
    df.to_csv('data/cleaned/cleaned_dataset.csv', index=False, encoding='utf-8-sig')
    print("[OK] data/cleaned/cleaned_dataset.csv")

    # Excel olarak kaydet
    df.to_excel('data/cleaned/cleaned_dataset.xlsx', index=False)
    print("[OK] data/cleaned/cleaned_dataset.xlsx")

    # Özet istatistikler
    summary_stats = df.describe(include='all').T
    summary_stats.to_excel('data/cleaned/summary_statistics.xlsx')
    print("[OK] data/cleaned/summary_statistics.xlsx")

    return df

def generate_cleaning_report(df_original, df_cleaned):
    """Temizleme raporu oluşturur"""

    report = []
    report.append("="*60)
    report.append("VERİ TEMİZLEME RAPORU")
    report.append("="*60)
    report.append(f"\nTarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("\nORİJİNAL VERİ:")
    report.append(f"  - Satır sayısı: {df_original.shape[0]}")
    report.append(f"  - Sütun sayısı: {df_original.shape[1]}")
    report.append("\nTEMİZLENMİŞ VERİ:")
    report.append(f"  - Satır sayısı: {df_cleaned.shape[0]}")
    report.append(f"  - Sütun sayısı: {df_cleaned.shape[1]}")
    report.append("\nYENİ DEĞİŞKENLER:")

    new_cols = set(df_cleaned.columns) - set(df_original.columns)
    for col in new_cols:
        report.append(f"  - {col}")

    # Raporu kaydet
    with open('data/cleaned/cleaning_report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

    print('\n'.join(report))

def main():
    """Ana fonksiyon"""

    print("="*60)
    print("VERİ TEMİZLEME BAŞLIYOR")
    print("="*60)

    # Ham veriyi yükle
    df = load_raw_data()
    if df is None:
        return None

    df_original = df.copy()

    # Temizleme adımları
    df = clean_column_names(df)
    df = handle_missing_values(df)
    df = create_derived_variables(df)
    df = encode_categorical_variables(df)
    df = remove_outliers(df)

    # Temizlenmiş veriyi kaydet
    df = save_cleaned_data(df)

    # Temizleme raporu
    generate_cleaning_report(df_original, df)

    print("\n" + "="*60)
    print("VERİ TEMİZLEME TAMAMLANDI!")
    print("="*60)
    print("\nSonraki adım: python scripts/analysis/03_descriptive_stats.py")

    return df

if __name__ == "__main__":
    df_cleaned = main()