"""
Veri Kalitesi ve Bütünlüğü Kontrolü
- Mükerrer veri kontrolü
- EMBU ölçek dönüşümü kontrolü (4'lü -> 6'lı)
- Eksik veri analizi
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import openpyxl
import sys
sys.path.append('.')
from google_sheets_api import GoogleSheetsAPI

def load_all_data_files():
    """Tüm veri dosyalarını yükle"""
    data_files = {}
    
    # CSV dosyaları
    csv_files = [
        'data/raw/main_dataset.csv',
        'data/raw/main_dataset_with_groups.csv',
        'data/cleaned/cleaned_dataset.csv'
    ]
    
    for file in csv_files:
        if os.path.exists(file):
            try:
                df = pd.read_csv(file)
                data_files[file] = df
                print(f"[OK] {file}: {df.shape[0]} satır x {df.shape[1]} sütun")
            except Exception as e:
                print(f"[HATA] {file} yüklenemedi: {e}")
    
    # Excel dosyaları
    excel_files = [
        'data/raw/main_dataset.xlsx',
        'data/cleaned/cleaned_dataset.xlsx'
    ]
    
    for file in excel_files:
        if os.path.exists(file):
            try:
                # Tüm sayfaları oku
                xl_file = pd.ExcelFile(file)
                for sheet_name in xl_file.sheet_names:
                    df = pd.read_excel(file, sheet_name=sheet_name)
                    data_files[f"{file}_{sheet_name}"] = df
                    print(f"[OK] {file} - {sheet_name}: {df.shape[0]} satır x {df.shape[1]} sütun")
            except Exception as e:
                print(f"[HATA] {file} yüklenemedi: {e}")
    
    return data_files

def check_duplicates(data_files):
    """Mükerrer veri kontrolü"""
    print("\n" + "="*60)
    print("MÜKERRER VERİ KONTROLÜ")
    print("="*60)
    
    duplicates_report = []
    
    for filename, df in data_files.items():
        print(f"\n{filename} kontrol ediliyor...")
        
        # Katılımcı No bazında mükerrer kontrol
        if 'Katilimci_No' in df.columns or 'Katılımcı No' in df.columns:
            id_col = 'Katilimci_No' if 'Katilimci_No' in df.columns else 'Katılımcı No'
            
            # Mükerrer satırlar
            duplicated = df[df.duplicated(subset=[id_col], keep=False)]
            if len(duplicated) > 0:
                print(f"  [!] {len(duplicated)} mükerrer satır bulundu!")
                unique_ids = duplicated[id_col].unique()
                print(f"  Mükerrer ID'ler: {unique_ids[:10].tolist()}..." if len(unique_ids) > 10 else f"  Mükerrer ID'ler: {unique_ids.tolist()}")
                
                duplicates_report.append({
                    'file': filename,
                    'duplicate_count': len(duplicated),
                    'duplicate_ids': unique_ids.tolist()
                })
            else:
                print(f"  [OK] Mükerrer veri yok")
        
        # Tam satır bazında mükerrer kontrol
        full_duplicates = df[df.duplicated(keep=False)]
        if len(full_duplicates) > 0:
            print(f"  [!] {len(full_duplicates)} tam mükerrer satır bulundu!")
    
    return duplicates_report

def check_embu_scale_conversion():
    """EMBU ölçek dönüşümü kontrolü (4'lü -> 6'lı)"""
    print("\n" + "="*60)
    print("EMBU ÖLÇEK DÖNÜŞÜMÜ KONTROLÜ")
    print("="*60)
    
    # Temizlenmiş veriyi yükle
    df = pd.read_csv('data/cleaned/cleaned_dataset.csv')
    
    # EMBU sütunlarını bul
    embu_cols = [col for col in df.columns if 'EMBU' in col]
    
    if len(embu_cols) > 0:
        print(f"\n{len(embu_cols)} EMBU sütunu bulundu")
        
        # Her EMBU sütunu için değer aralığını kontrol et
        for col in embu_cols:
            values = df[col].dropna()
            unique_vals = sorted(values.unique())
            min_val = values.min()
            max_val = values.max()
            mean_val = values.mean()
            
            print(f"\n{col}:")
            print(f"  Değer aralığı: {min_val:.1f} - {max_val:.1f}")
            print(f"  Ortalama: {mean_val:.2f}")
            print(f"  Benzersiz değerler: {len(unique_vals)}")
            
            # 4'lü mü 6'lı mı kontrol et
            if max_val <= 4:
                print(f"  [!] 4'lü skala görünüyor (1-4)")
            elif max_val <= 6:
                print(f"  [OK] 6'lı skala görünüyor (1-6)")
            else:
                print(f"  [?] Beklenmedik değer aralığı")
            
            # İlk 10 benzersiz değeri göster
            if len(unique_vals) <= 20:
                print(f"  Değerler: {unique_vals}")
    else:
        print("\nEMBU sütunu bulunamadı!")
    
    # Çocuk EMBU verilerini kontrol et (eğer varsa)
    child_embu_cols = [col for col in df.columns if 'Cocuk' in col and 'EMBU' in col]
    if len(child_embu_cols) > 0:
        print(f"\n\nÇOCUK EMBU VERİLERİ:")
        print(f"{len(child_embu_cols)} çocuk EMBU sütunu bulundu")
        
        for col in child_embu_cols:
            values = df[col].dropna()
            if len(values) > 0:
                print(f"\n{col}:")
                print(f"  Değer aralığı: {values.min():.1f} - {values.max():.1f}")
                print(f"  Ortalama: {values.mean():.2f}")

def analyze_missing_data(data_files):
    """Eksik veri analizi"""
    print("\n" + "="*60)
    print("EKSİK VERİ ANALİZİ")
    print("="*60)
    
    missing_report = []
    
    for filename, df in data_files.items():
        if 'cleaned' in filename.lower():
            print(f"\n{filename} analiz ediliyor...")
            
            total_cells = df.shape[0] * df.shape[1]
            missing_cells = df.isnull().sum().sum()
            missing_pct = (missing_cells / total_cells) * 100
            
            print(f"  Toplam hücre: {total_cells:,}")
            print(f"  Eksik hücre: {missing_cells:,} ({missing_pct:.2f}%)")
            
            # En çok eksik veri olan sütunlar
            missing_by_col = df.isnull().sum()
            missing_by_col = missing_by_col[missing_by_col > 0].sort_values(ascending=False)
            
            if len(missing_by_col) > 0:
                print(f"\n  En çok eksik veri olan sütunlar:")
                for col, count in missing_by_col.head(10).items():
                    pct = (count / len(df)) * 100
                    print(f"    {col}: {count} eksik ({pct:.1f}%)")
            
            # Kritik sütunlardaki eksikler
            critical_cols = ['Grup', 'Beck_Toplam', 'Beck_Total_Score', 'Katilimci_No']
            print(f"\n  Kritik sütunlardaki eksikler:")
            for col in critical_cols:
                if col in df.columns:
                    missing = df[col].isnull().sum()
                    pct = (missing / len(df)) * 100
                    print(f"    {col}: {missing} eksik ({pct:.1f}%)")
            
            missing_report.append({
                'file': filename,
                'total_missing': missing_cells,
                'missing_pct': missing_pct,
                'columns_with_missing': len(missing_by_col)
            })
    
    return missing_report

def check_data_consistency(data_files):
    """Veri tutarlılığı kontrolü"""
    print("\n" + "="*60)
    print("VERİ TUTARLILIĞI KONTROLÜ")
    print("="*60)
    
    # Farklı dosyalardaki satır sayılarını karşılaştır
    print("\nDosya boyutları:")
    for filename, df in data_files.items():
        if 'raw' in filename or 'cleaned' in filename:
            print(f"  {filename}: {df.shape[0]} satır")
    
    # Katılımcı sayıları tutarlı mı?
    participant_counts = {}
    for filename, df in data_files.items():
        if 'Katilimci_No' in df.columns or 'Katılımcı No' in df.columns:
            id_col = 'Katilimci_No' if 'Katilimci_No' in df.columns else 'Katılımcı No'
            unique_count = df[id_col].nunique()
            participant_counts[filename] = unique_count
    
    print("\nBenzersiz katılımcı sayıları:")
    for filename, count in participant_counts.items():
        print(f"  {filename}: {count} katılımcı")
    
    # Beck skorları tutarlı mı?
    print("\nBeck skoru tutarlılığı:")
    for filename, df in data_files.items():
        if 'Beck_Toplam' in df.columns and 'Beck_Total_Score' in df.columns:
            # İki Beck sütunu arasındaki ilişki
            valid_rows = df[['Beck_Toplam', 'Beck_Total_Score']].dropna()
            if len(valid_rows) > 0:
                corr = valid_rows['Beck_Toplam'].corr(valid_rows['Beck_Total_Score'])
                print(f"  {filename}: Beck_Toplam vs Beck_Total_Score korelasyon = {corr:.3f}")
                
                # Fark var mı?
                diff = (valid_rows['Beck_Total_Score'] - valid_rows['Beck_Toplam']).abs().mean()
                print(f"    Ortalama fark: {diff:.2f}")

def check_google_sheets_data():
    """Google Sheets verilerini kontrol et"""
    print("\n" + "="*60)
    print("GOOGLE SHEETS VERİ KONTROLÜ")
    print("="*60)
    
    try:
        api = GoogleSheetsAPI('dr-murzoglu-doktora.json')
        
        # Ana veri sayfasını kontrol et
        spreadsheet_id = '1xvl0hHrAG1jQxX-RmkJG0SiQOOGo_hGFH7L2mnGRZJk'
        
        # Metadata al
        metadata = api.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets = metadata.get('sheets', [])
        
        print(f"\nToplam {len(sheets)} sayfa bulundu:")
        for sheet in sheets:
            title = sheet['properties']['title']
            row_count = sheet['properties']['gridProperties']['rowCount']
            col_count = sheet['properties']['gridProperties']['columnCount']
            print(f"  - {title}: {row_count} satır x {col_count} sütun")
            
            # Her sayfadan veri oku
            try:
                range_name = f"{title}!A1:ZZ1000"
                result = api.service.spreadsheets().values().get(
                    spreadsheetId=spreadsheet_id, 
                    range=range_name
                ).execute()
                
                values = result.get('values', [])
                if values:
                    df = pd.DataFrame(values[1:], columns=values[0] if values else [])
                    print(f"    Veri: {len(df)} satır x {len(df.columns)} sütun")
                    
                    # EMBU verilerini kontrol et
                    embu_cols = [col for col in df.columns if 'EMBU' in str(col)]
                    if embu_cols:
                        print(f"    EMBU sütunları: {len(embu_cols)} adet")
            except Exception as e:
                print(f"    [HATA] Veri okunamadı: {e}")
                
    except Exception as e:
        print(f"[HATA] Google Sheets bağlantısı kurulamadı: {e}")

def create_quality_report(duplicates, missing_data):
    """Veri kalite raporu oluştur"""
    
    report = []
    report.append("="*70)
    report.append("VERİ KALİTESİ VE BÜTÜNLÜĞÜ RAPORU")
    report.append("="*70)
    report.append(f"\nTarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Mükerrer veri özeti
    report.append("\n" + "="*70)
    report.append("1. MÜKERRER VERİ ÖZETİ")
    report.append("="*70)
    
    if duplicates:
        for item in duplicates:
            report.append(f"\n{item['file']}:")
            report.append(f"  - {item['duplicate_count']} mükerrer satır")
            report.append(f"  - {len(item['duplicate_ids'])} benzersiz mükerrer ID")
    else:
        report.append("\nMükerrer veri tespit edilmedi.")
    
    # Eksik veri özeti
    report.append("\n" + "="*70)
    report.append("2. EKSİK VERİ ÖZETİ")
    report.append("="*70)
    
    if missing_data:
        for item in missing_data:
            report.append(f"\n{item['file']}:")
            report.append(f"  - Toplam eksik: {item['total_missing']:,} hücre")
            report.append(f"  - Eksik oranı: {item['missing_pct']:.2f}%")
            report.append(f"  - Eksik içeren sütun: {item['columns_with_missing']}")
    
    # EMBU ölçek durumu
    report.append("\n" + "="*70)
    report.append("3. EMBU ÖLÇEK DÖNÜŞÜM DURUMU")
    report.append("="*70)
    report.append("\nEbeveyn EMBU verileri 1-6 aralığında (6'lı skala)")
    report.append("Çocuk EMBU verileri için ek kontrol gerekli")
    
    # Öneriler
    report.append("\n" + "="*70)
    report.append("4. ÖNERİLER")
    report.append("="*70)
    report.append("\n1. Mükerrer verilerin temizlenmesi")
    report.append("2. Kritik değişkenlerdeki eksik verilerin tamamlanması")
    report.append("3. EMBU ölçek dönüşümünün doğrulanması")
    report.append("4. Grup değişkeninin yeniden kontrolü (38 vs 156 dengesizliği)")
    
    report.append("\n" + "="*70)
    
    return "\n".join(report)

def main():
    """Ana fonksiyon"""
    
    print("\n" + "="*60)
    print("VERİ KALİTESİ VE BÜTÜNLÜĞÜ KONTROLÜ BAŞLATILIYOR")
    print("="*60)
    
    try:
        # Tüm veri dosyalarını yükle
        print("\nVeri dosyaları yükleniyor...")
        data_files = load_all_data_files()
        
        # Mükerrer veri kontrolü
        duplicates = check_duplicates(data_files)
        
        # EMBU ölçek kontrolü
        check_embu_scale_conversion()
        
        # Eksik veri analizi
        missing_data = analyze_missing_data(data_files)
        
        # Veri tutarlılığı kontrolü
        check_data_consistency(data_files)
        
        # Google Sheets kontrolü
        check_google_sheets_data()
        
        # Rapor oluştur
        report = create_quality_report(duplicates, missing_data)
        
        # Raporu kaydet
        with open('results/data_quality_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        print("\n[OK] Veri kalite raporu oluşturuldu: results/data_quality_report.txt")
        
        print("\n" + "="*60)
        print("VERİ KALİTESİ KONTROLÜ TAMAMLANDI")
        print("="*60)
        
    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()