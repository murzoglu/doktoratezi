"""
Diyabet Hastalarını Bulma ve Entegre Etme
Tüm veri kaynaklarını tara ve diyabet hastalarını bul
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import sys
sys.path.append('.')
from google_drive_api import GoogleDriveAPI
from google_sheets_api import GoogleSheetsAPI

def analyze_all_data_sources():
    """Tüm veri kaynaklarını analiz et"""
    
    print("="*70)
    print("TÜM VERİ KAYNAKLARINI TARAMA")
    print("="*70)
    
    all_data = {}
    diabetes_counts = {}
    
    # 1. Lokal CSV ve Excel dosyaları
    print("\n1. LOKAL DOSYALAR:")
    print("-" * 40)
    
    local_files = [
        'data/raw/main_dataset.csv',
        'data/raw/main_dataset.xlsx',
        'data/raw/main_dataset_with_groups.csv',
        'data/cleaned/cleaned_dataset.csv',
        'data/cleaned/cleaned_dataset.xlsx',
        'data/cleaned/cleaned_dataset_no_duplicates.csv'
    ]
    
    for file_path in local_files:
        if os.path.exists(file_path):
            try:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)
                
                all_data[file_path] = df
                
                # Diyabet hastalarını say
                dm_count = 0
                if 'DM Tanı Tarihi' in df.columns:
                    dm_count = (~df['DM Tanı Tarihi'].isna()).sum()
                elif 'Grup' in df.columns:
                    dm_count = (df['Grup'] == 'Diyabet').sum()
                
                diabetes_counts[file_path] = dm_count
                
                print(f"\n{os.path.basename(file_path)}:")
                print(f"  Toplam kayıt: {len(df)}")
                print(f"  Diyabet hasta: {dm_count}")
                print(f"  Benzersiz ID: {df.get('Katilimci_No', df.get('Katılımcı No', pd.Series())).nunique()}")
                
            except Exception as e:
                print(f"\n{os.path.basename(file_path)}: HATA - {e}")
    
    return all_data, diabetes_counts

def check_participant_id_patterns(all_data):
    """Katılımcı ID desenlerini kontrol et"""
    
    print("\n" + "="*70)
    print("KATILIMCI ID DESEN ANALİZİ")
    print("="*70)
    
    for file_path, df in all_data.items():
        if 'raw' in file_path:
            print(f"\n{os.path.basename(file_path)}:")
            
            id_col = None
            if 'Katilimci_No' in df.columns:
                id_col = 'Katilimci_No'
            elif 'Katılımcı No' in df.columns:
                id_col = 'Katılımcı No'
            
            if id_col:
                ids = df[id_col].astype(str)
                
                # ID desenlerini analiz et
                patterns = {}
                for id_val in ids:
                    if '-' in id_val:
                        prefix = id_val.split('-')[0]
                        patterns[prefix] = patterns.get(prefix, 0) + 1
                
                # En sık kullanılan desenler
                sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)
                
                print("  ID desenleri (prefix-suffix formatında):")
                for prefix, count in sorted_patterns[:10]:
                    print(f"    {prefix}-X: {count} kayıt")
                
                # DM tanısı ile ilişki
                if 'DM Tanı Tarihi' in df.columns:
                    print("\n  Prefix ve DM tanısı ilişkisi:")
                    for prefix, count in sorted_patterns[:5]:
                        prefix_df = df[ids.str.startswith(prefix)]
                        dm_count = (~prefix_df['DM Tanı Tarihi'].isna()).sum()
                        print(f"    {prefix}-X: {dm_count}/{len(prefix_df)} DM tanılı")

def find_missing_diabetes_patients(all_data):
    """Eksik diyabet hastalarını bul"""
    
    print("\n" + "="*70)
    print("EKSİK DİYABET HASTALARI ANALİZİ")
    print("="*70)
    
    # Ham veriyi al
    raw_df = all_data.get('data/raw/main_dataset.csv')
    
    if raw_df is not None:
        print("\nDM Tanı Tarihi Analizi:")
        
        if 'DM Tanı Tarihi' in raw_df.columns:
            dm_dates = raw_df['DM Tanı Tarihi']
            
            # Boş olmayan değerleri incele
            non_empty = dm_dates[dm_dates.notna()]
            print(f"\nDM tanı tarihi olan: {len(non_empty)} kayıt")
            
            # Benzersiz tarihler
            unique_dates = non_empty.unique()
            print(f"Benzersiz tanı tarihi: {len(unique_dates)}")
            
            # İlk 10 tarihi göster
            print("\nİlk 10 DM tanı tarihi:")
            for date in unique_dates[:10]:
                count = (dm_dates == date).sum()
                print(f"  {date}: {count} hasta")
        
        # Grup değişkeni kontrolü
        if 'Grup' in raw_df.columns:
            print("\nGrup değişkeni analizi:")
            print(raw_df['Grup'].value_counts())
            
            # Grup ataması yapılmamış olanlar
            if 'Belirtilmemiş' in raw_df['Grup'].values:
                unspecified = raw_df[raw_df['Grup'] == 'Belirtilmemiş']
                print(f"\nBelirtilmemiş grup: {len(unspecified)} kayıt")
                
                # Bunların DM tanısı var mı?
                if 'DM Tanı Tarihi' in unspecified.columns:
                    dm_in_unspecified = (~unspecified['DM Tanı Tarihi'].isna()).sum()
                    print(f"  Bunlardan {dm_in_unspecified} tanesinin DM tanısı var!")

def search_google_drive_data():
    """Google Drive'da ek veri ara"""
    
    print("\n" + "="*70)
    print("GOOGLE DRIVE VERİ ARAMA")
    print("="*70)
    
    try:
        drive_api = GoogleDriveAPI('dr-murzoglu-doktora.json')
        folder_id = '1C8vsNG-kVbYmL3tCG_lYuyUvYElSCTvs'
        
        # Klasördeki tüm dosyalar
        files = drive_api.list_files(folder_id)
        
        print(f"\nToplam {len(files)} dosya bulundu")
        
        # Google Sheets dosyalarını filtrele
        sheets = [f for f in files if 'spreadsheet' in f.get('mimeType', '').lower()]
        print(f"Google Sheets sayısı: {len(sheets)}")
        
        if sheets:
            sheets_api = GoogleSheetsAPI('dr-murzoglu-doktora.json')
            
            for sheet in sheets[:5]:  # İlk 5 sheet
                print(f"\n{sheet['name']}:")
                print(f"  ID: {sheet['id']}")
                
                try:
                    # Sheet'i aç ve ilk sayfayı oku
                    metadata = sheets_api.service.spreadsheets().get(
                        spreadsheetId=sheet['id']
                    ).execute()
                    
                    sheet_props = metadata.get('sheets', [])
                    if sheet_props:
                        first_sheet = sheet_props[0]['properties']['title']
                        rows = sheet_props[0]['properties']['gridProperties']['rowCount']
                        cols = sheet_props[0]['properties']['gridProperties']['columnCount']
                        
                        print(f"  İlk sayfa: {first_sheet}")
                        print(f"  Boyut: {rows} x {cols}")
                        
                        # Veriyi oku
                        range_name = f"{first_sheet}!A1:Z100"
                        result = sheets_api.service.spreadsheets().values().get(
                            spreadsheetId=sheet['id'],
                            range=range_name
                        ).execute()
                        
                        values = result.get('values', [])
                        if values and len(values) > 1:
                            # DataFrame'e çevir
                            df = pd.DataFrame(values[1:], columns=values[0] if values else [])
                            
                            # DM veya Diyabet kelimelerini ara
                            dm_cols = [col for col in df.columns if 'DM' in str(col) or 'Diyabet' in str(col)]
                            if dm_cols:
                                print(f"  DM/Diyabet sütunları bulundu: {dm_cols}")
                            
                            # Grup sütunu var mı?
                            if 'Grup' in df.columns:
                                print(f"  Grup sütunu var")
                                grup_counts = df['Grup'].value_counts()
                                print(f"  Grup dağılımı: {grup_counts.to_dict()}")
                
                except Exception as e:
                    print(f"  HATA: {str(e)[:100]}")
        
        # Excel dosyaları
        excel_files = [f for f in files if f['name'].endswith(('.xlsx', '.xls'))]
        print(f"\nExcel dosya sayısı: {len(excel_files)}")
        for excel in excel_files[:5]:
            print(f"  - {excel['name']}")
            
    except Exception as e:
        print(f"\nGoogle Drive erişim hatası: {e}")

def create_integrated_dataset(all_data):
    """Entegre veri seti oluştur"""
    
    print("\n" + "="*70)
    print("ENTEGRE VERİ SETİ OLUŞTURMA")
    print("="*70)
    
    # En güncel ve temiz veriyi bul
    if 'data/cleaned/cleaned_dataset_no_duplicates.csv' in all_data:
        base_df = all_data['data/cleaned/cleaned_dataset_no_duplicates.csv'].copy()
    elif 'data/cleaned/cleaned_dataset.csv' in all_data:
        base_df = all_data['data/cleaned/cleaned_dataset.csv'].copy()
    else:
        base_df = all_data['data/raw/main_dataset.csv'].copy()
    
    print(f"\nTemel veri seti: {len(base_df)} kayıt")
    
    # Grup atamasını yeniden yap
    if 'DM Tanı Tarihi' in base_df.columns:
        print("\nGrup ataması yeniden yapılıyor...")
        
        def assign_group(row):
            dm_date = row.get('DM Tanı Tarihi')
            
            # DM tanı tarihi varsa kesinlikle Diyabet
            if pd.notna(dm_date) and str(dm_date).strip() not in ['', 'nan', 'NaN', 'None']:
                return 'Diyabet'
            
            # Katılımcı No kontrolü (eğer varsa)
            participant_no = str(row.get('Katilimci_No', row.get('Katılımcı No', '')))
            
            # Bazı özel ID patternleri diyabet gösteriyor olabilir
            # Örneğin 3XX serisi diyabet, 4XX-5XX kontrol olabilir
            if participant_no.startswith('3'):
                # 3XX serisi için ek kontrol yap
                pass
            
            return 'Kontrol'
        
        base_df['Grup_Yeni'] = base_df.apply(assign_group, axis=1)
        
        print("\nYeni grup dağılımı:")
        print(base_df['Grup_Yeni'].value_counts())
        
        # Eski grupla karşılaştır
        if 'Grup' in base_df.columns:
            print("\nEski vs Yeni grup karşılaştırması:")
            comparison = pd.crosstab(base_df['Grup'], base_df['Grup_Yeni'])
            print(comparison)
            
            # Farklı atananlar
            different = base_df[base_df['Grup'] != base_df['Grup_Yeni']]
            if len(different) > 0:
                print(f"\n{len(different)} kayıt farklı atanmış:")
                print(different[['Katilimci_No', 'Grup', 'Grup_Yeni', 'DM Tanı Tarihi']].head(10))
    
    return base_df

def generate_report(all_data, diabetes_counts):
    """Detaylı rapor oluştur"""
    
    report = []
    report.append("="*70)
    report.append("DİYABET HASTA VERİSİ ARAMA RAPORU")
    report.append("="*70)
    report.append(f"\nTarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    report.append("\n" + "="*70)
    report.append("1. VERİ DOSYALARI ÖZETİ")
    report.append("="*70)
    
    for file_path, dm_count in diabetes_counts.items():
        total_count = len(all_data[file_path])
        report.append(f"\n{os.path.basename(file_path)}:")
        report.append(f"  Toplam kayıt: {total_count}")
        report.append(f"  Diyabet hasta: {dm_count}")
        report.append(f"  Diyabet oranı: {dm_count/total_count*100:.1f}%")
    
    report.append("\n" + "="*70)
    report.append("2. TESPİTLER VE ÖNERİLER")
    report.append("="*70)
    
    max_dm = max(diabetes_counts.values())
    report.append(f"\nMaksimum diyabet hasta sayısı: {max_dm}")
    report.append(f"Protokol beklentisi: ~100 diyabet hastası")
    report.append(f"Açık: {100 - max_dm} hasta")
    
    report.append("\nÖneriler:")
    report.append("1. Google Drive'daki tüm spreadsheet'leri kontrol et")
    report.append("2. Katılımcı ID desenlerini yeniden incele")
    report.append("3. 'Belirtilmemiş' grubu içindeki hastaları kontrol et")
    report.append("4. DM tanı tarihi formatını standardize et")
    report.append("5. Eksik veya yanlış kodlanmış kayıtları düzenle")
    
    report.append("\n" + "="*70)
    
    return "\n".join(report)

def main():
    """Ana fonksiyon"""
    
    print("\n" + "="*70)
    print("DİYABET HASTA VERİSİ ARAMA VE ENTEGRASYON")
    print("="*70)
    
    try:
        # 1. Tüm veri kaynaklarını analiz et
        all_data, diabetes_counts = analyze_all_data_sources()
        
        # 2. Katılımcı ID desenlerini kontrol et
        check_participant_id_patterns(all_data)
        
        # 3. Eksik diyabet hastalarını bul
        find_missing_diabetes_patients(all_data)
        
        # 4. Google Drive'da ara
        search_google_drive_data()
        
        # 5. Entegre veri seti oluştur
        integrated_df = create_integrated_dataset(all_data)
        
        # 6. Rapor oluştur
        report = generate_report(all_data, diabetes_counts)
        
        # Raporu kaydet
        with open('results/diabetes_data_search_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("\n" + report)
        
        # Entegre veri setini kaydet (eğer değişiklik varsa)
        if 'Grup_Yeni' in integrated_df.columns:
            integrated_df['Grup'] = integrated_df['Grup_Yeni']
            integrated_df.drop('Grup_Yeni', axis=1, inplace=True)
            
            integrated_df.to_csv('data/cleaned/integrated_dataset.csv', index=False, encoding='utf-8-sig')
            integrated_df.to_excel('data/cleaned/integrated_dataset.xlsx', index=False)
            
            print("\n[OK] Entegre veri seti kaydedildi:")
            print("  - data/cleaned/integrated_dataset.csv")
            print("  - data/cleaned/integrated_dataset.xlsx")
        
        print("\n" + "="*70)
        print("ARAMA VE ENTEGRASYON TAMAMLANDI")
        print("="*70)
        
    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()