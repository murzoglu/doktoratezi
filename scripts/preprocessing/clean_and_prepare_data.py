"""
Veri Temizleme ve Hazırlama - Klinik Çalışma
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

def load_and_examine_data():
    """Veriyi yükler ve yapısını inceler"""

    print("="*60)
    print("VERİ YÜKLEME VE İNCELEME")
    print("="*60)

    # Veriyi yükle
    df = pd.read_csv('data/raw/main_dataset.csv')
    print(f"\nVeri boyutu: {df.shape[0]} satır x {df.shape[1]} sütun")

    # Sütun isimlerini düzelt
    df.columns = df.columns.str.strip()

    # Veri tiplerini kontrol et
    print("\n[VERİ TİPLERİ]")
    print("-"*40)

    # Beck sütunlarını kontrol et
    beck_cols = [col for col in df.columns if 'Beck' in col]
    print(f"Beck sütun sayısı: {len(beck_cols)}")

    if beck_cols:
        # Beck değerlerini sayısala çevir
        for col in beck_cols:
            # String değerleri kontrol et
            unique_vals = df[col].unique()
            print(f"\n{col} benzersiz değerler: {unique_vals[:5]}...")

            # Sayısala dönüştür
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def identify_groups(df):
    """Diyabet ve kontrol gruplarını belirle"""

    print("\n[GRUP BELİRLEME]")
    print("-"*40)

    # DM Tanı Tarihi sütununu kontrol et
    if 'DM Tanı Tarihi' in df.columns:
        # Değerleri incele
        dm_values = df['DM Tanı Tarihi'].value_counts(dropna=False)
        print("DM Tanı Tarihi değer dağılımı:")
        print(dm_values.head(10))

        # Grup değişkeni oluştur - Farklı mantık kullanalım
        # Katılımcı Çocuk sütunu varsa onu da kontrol et
        if 'Katılımcı Çocuk' in df.columns:
            print("\nKatılımcı Çocuk değerleri:")
            print(df['Katılımcı Çocuk'].value_counts(dropna=False))

            # Eğer 'Diyabet' veya 'Kontrol' gibi değerler varsa
            df['Grup'] = df['Katılımcı Çocuk'].apply(
                lambda x: 'Diyabet' if pd.notna(x) and 'diyabet' in str(x).lower()
                else ('Kontrol' if pd.notna(x) and 'kontrol' in str(x).lower()
                else 'Belirtilmemiş')
            )
        else:
            # DM tanı tarihi olan/olmayan şeklinde ayır
            df['Grup'] = df['DM Tanı Tarihi'].apply(
                lambda x: 'Diyabet' if pd.notna(x) and str(x).strip() != ''
                else 'Kontrol'
            )
    else:
        # Varsayılan grup ata
        print("DM Tanı Tarihi sütunu bulunamadı!")
        df['Grup'] = 'Belirtilmemiş'

    # Grup dağılımı
    print("\nGrup dağılımı:")
    print(df['Grup'].value_counts())

    return df

def clean_data(df):
    """Veriyi temizler ve hazırlar"""

    print("\n[VERİ TEMİZLEME]")
    print("-"*40)

    # Türkçe karakterleri düzelt
    replacements = {
        'ç': 'c', 'Ç': 'C',
        'ğ': 'g', 'Ğ': 'G',
        'ı': 'i', 'İ': 'I',
        'ö': 'o', 'Ö': 'O',
        'ş': 's', 'Ş': 'S',
        'ü': 'u', 'Ü': 'U',
        ' ': '_'
    }

    new_columns = []
    for col in df.columns:
        new_col = col
        for tr_char, en_char in replacements.items():
            new_col = new_col.replace(tr_char, en_char)
        new_columns.append(new_col)

    df.columns = new_columns
    print("[OK] Sütun isimleri temizlendi")

    # Beck skorlarını sayısala çevir
    beck_cols = [col for col in df.columns if 'Beck' in col and col != 'Beck_Total_Score']
    for col in beck_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Beck toplam skoru hesapla
    if beck_cols:
        # NaN değerleri 0 olarak say (veya başka bir strateji)
        df['Beck_Total_Score'] = df[beck_cols].fillna(0).sum(axis=1)
        print(f"[OK] Beck toplam skor hesaplandı")

        # Beck kategorileri
        df['Beck_Category'] = pd.cut(
            df['Beck_Total_Score'],
            bins=[-1, 13, 19, 28, 63],
            labels=['Minimal', 'Hafif', 'Orta', 'Şiddetli']
        )
        print(f"[OK] Beck kategorileri oluşturuldu")

    # EMBU skorlarını kontrol et
    embu_cols = [col for col in df.columns if 'EMBU' in col.upper()]
    if embu_cols:
        print(f"[OK] {len(embu_cols)} EMBU sütunu bulundu")
        for col in embu_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Yaş hesaplama
    date_cols = [col for col in df.columns if 'Dogum_Tarihi' in col or 'Doğum_Tarihi' in col]
    for col in date_cols:
        try:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            age_col = col.replace('Dogum_Tarihi', 'Yas').replace('Doğum_Tarihi', 'Yas')
            df[age_col] = (pd.Timestamp.now() - df[col]).dt.days / 365.25
            df[age_col] = df[age_col].round(1)
            print(f"[OK] {age_col} hesaplandı")
        except:
            pass

    # Eksik veri analizi
    print("\n[EKSİK VERİ ANALİZİ]")
    print("-"*40)

    missing_summary = df.isnull().sum()
    missing_pct = (missing_summary / len(df)) * 100

    high_missing = missing_pct[missing_pct > 50]
    if len(high_missing) > 0:
        print(f"%50'den fazla eksik veri içeren {len(high_missing)} sütun var")
        # Bu sütunları çıkar
        cols_to_drop = high_missing.index.tolist()
        df = df.drop(columns=cols_to_drop)
        print(f"[OK] {len(cols_to_drop)} sütun çıkarıldı")

    return df

def save_cleaned_data(df):
    """Temizlenmiş veriyi kaydet"""

    print("\n[VERİ KAYDETME]")
    print("-"*40)

    # Klasörleri oluştur
    os.makedirs('data/cleaned', exist_ok=True)
    os.makedirs('results/tables', exist_ok=True)

    # CSV olarak kaydet
    df.to_csv('data/cleaned/cleaned_dataset.csv', index=False, encoding='utf-8-sig')
    print("[OK] data/cleaned/cleaned_dataset.csv")

    # Excel olarak kaydet
    df.to_excel('data/cleaned/cleaned_dataset.xlsx', index=False)
    print("[OK] data/cleaned/cleaned_dataset.xlsx")

    # Özet istatistikler
    summary = df.describe(include='all').T
    summary.to_excel('results/tables/summary_statistics.xlsx')
    print("[OK] results/tables/summary_statistics.xlsx")

    return df

def generate_data_report(df):
    """Veri raporu oluştur"""

    print("\n" + "="*60)
    print("VERİ RAPORU")
    print("="*60)

    print(f"\nToplam katılımcı: {len(df)}")
    print(f"Değişken sayısı: {df.shape[1]}")

    # Grup dağılımı
    if 'Grup' in df.columns:
        print("\nGrup dağılımı:")
        for grup, count in df['Grup'].value_counts().items():
            print(f"  {grup}: {count} ({count/len(df)*100:.1f}%)")

    # Beck skorları özeti
    if 'Beck_Total_Score' in df.columns:
        print(f"\nBeck Depresyon Skorları:")
        print(f"  Ortalama: {df['Beck_Total_Score'].mean():.2f}")
        print(f"  Medyan: {df['Beck_Total_Score'].median():.1f}")
        print(f"  Min-Max: {df['Beck_Total_Score'].min():.0f} - {df['Beck_Total_Score'].max():.0f}")

        if 'Beck_Category' in df.columns:
            print("\nBeck Kategorileri:")
            for cat, count in df['Beck_Category'].value_counts().items():
                print(f"  {cat}: {count} ({count/len(df)*100:.1f}%)")

    # Yaş özeti
    age_cols = [col for col in df.columns if 'Yas' in col]
    if age_cols:
        for col in age_cols:
            if df[col].notna().sum() > 0:
                print(f"\n{col}:")
                print(f"  Ortalama: {df[col].mean():.1f} yıl")
                print(f"  Min-Max: {df[col].min():.1f} - {df[col].max():.1f}")

    # Eksik veri özeti
    missing_summary = df.isnull().sum()
    cols_with_missing = missing_summary[missing_summary > 0]

    if len(cols_with_missing) > 0:
        print(f"\nEksik veri içeren sütun sayısı: {len(cols_with_missing)}")
        print("En çok eksik veri içeren 5 sütun:")
        for col in cols_with_missing.nlargest(5).index:
            pct = (missing_summary[col] / len(df)) * 100
            print(f"  {col}: {missing_summary[col]} ({pct:.1f}%)")
    else:
        print("\nEksik veri yok!")

    # Raporu dosyaya kaydet
    report_path = 'data/cleaned/data_report.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"Veri Temizleme Raporu\n")
        f.write(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"{'='*60}\n\n")
        f.write(f"Toplam katılımcı: {len(df)}\n")
        f.write(f"Değişken sayısı: {df.shape[1]}\n")

        if 'Grup' in df.columns:
            f.write(f"\nGrup dağılımı:\n")
            for grup, count in df['Grup'].value_counts().items():
                f.write(f"  {grup}: {count} ({count/len(df)*100:.1f}%)\n")

    print(f"\n[OK] Rapor kaydedildi: {report_path}")

    return df

def main():
    """Ana fonksiyon"""

    try:
        # 1. Veriyi yükle ve incele
        df = load_and_examine_data()

        # 2. Grupları belirle
        df = identify_groups(df)

        # 3. Veriyi temizle
        df = clean_data(df)

        # 4. Temiz veriyi kaydet
        df = save_cleaned_data(df)

        # 5. Rapor oluştur
        df = generate_data_report(df)

        print("\n" + "="*60)
        print("VERİ TEMİZLEME TAMAMLANDI!")
        print("="*60)
        print("\nTemizlenmiş veri:")
        print("  - data/cleaned/cleaned_dataset.csv")
        print("  - data/cleaned/cleaned_dataset.xlsx")
        print("\nSonraki adım: Hipotez testleri ve analizler")

        return df

    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    df = main()