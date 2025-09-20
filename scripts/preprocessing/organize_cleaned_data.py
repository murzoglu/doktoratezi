"""
data/cleaned klasörünü düzenle ve temizle
Eski dosyaları arşivle, final veri setlerini organize et
"""

import os
import shutil
import pandas as pd
from datetime import datetime

def create_archive_folder():
    """Arşiv klasörü oluştur"""
    archive_dir = 'data/cleaned/archive'
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        print(f"[OK] Arşiv klasörü oluşturuldu: {archive_dir}")
    return archive_dir

def archive_old_files():
    """Eski dosyaları arşivle"""
    
    print("="*60)
    print("ESKİ DOSYALARI ARŞİVLEME")
    print("="*60)
    
    archive_dir = create_archive_folder()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Arşivlenecek dosyalar
    files_to_archive = [
        'cleaned_dataset.csv',
        'cleaned_dataset.xlsx',
        'cleaned_dataset_no_duplicates.csv',
        'cleaned_dataset_no_duplicates.xlsx',
        'final_integrated_dataset.csv',  # DM_ kayıtları içeren hatalı veri
        'final_integrated_dataset.xlsx',
        'data_report.txt',
        'group_info.txt'
    ]
    
    archived_count = 0
    for file in files_to_archive:
        source_path = f'data/cleaned/{file}'
        if os.path.exists(source_path):
            # Arşiv adına timestamp ekle
            name, ext = os.path.splitext(file)
            archive_name = f"{name}_{timestamp}{ext}"
            dest_path = os.path.join(archive_dir, archive_name)
            
            shutil.move(source_path, dest_path)
            print(f"[ARŞİV] {file} -> archive/{archive_name}")
            archived_count += 1
    
    print(f"\nToplam {archived_count} dosya arşivlendi.")
    return archived_count

def prepare_final_dataset():
    """Final veri setini hazırla"""
    
    print("\n" + "="*60)
    print("FİNAL VERİ SETİ HAZIRLAMA")
    print("="*60)
    
    # final_dataset_without_dm.csv dosyasını yükle
    source_file = 'data/cleaned/final_dataset_without_dm.csv'
    
    if not os.path.exists(source_file):
        print("[HATA] final_dataset_without_dm.csv bulunamadı!")
        # cleaned_dataset_no_duplicates.csv'yi kullan
        source_file = 'data/cleaned/archive/cleaned_dataset_no_duplicates_*.csv'
        import glob
        files = glob.glob(source_file)
        if files:
            source_file = files[0]
            print(f"[BİLGİ] Arşivden yükleniyor: {source_file}")
    
    # Veriyi yükle
    df = pd.read_csv(source_file)
    
    print(f"\nVeri yüklendi: {len(df)} kayıt")
    print(f"Grup dağılımı: {df['Grup'].value_counts().to_dict()}")
    
    # Temiz sütun isimleri
    df.columns = df.columns.str.strip()
    
    # Gerçekten mükerrer kayıtlar var mı kontrol et
    duplicates = df[df.duplicated(subset=['Katilimci_No'], keep=False)]
    if len(duplicates) > 0:
        print(f"\n[UYARI] {len(duplicates)} mükerrer kayıt bulundu, temizleniyor...")
        df = df.drop_duplicates(subset=['Katilimci_No'], keep='first')
        print(f"Temizleme sonrası: {len(df)} kayıt")
    
    return df

def create_final_files(df):
    """Final dosyaları oluştur"""
    
    print("\n" + "="*60)
    print("FİNAL DOSYALARI OLUŞTURMA")
    print("="*60)
    
    # 1. Ana veri seti (tüm sütunlarla)
    df.to_csv('data/cleaned/final_dataset.csv', index=False, encoding='utf-8-sig')
    df.to_excel('data/cleaned/final_dataset.xlsx', index=False)
    print("[OK] final_dataset.csv ve .xlsx kaydedildi")
    
    # 2. Analiz için önemli sütunlar
    important_cols = ['Katilimci_No', 'Grup', 'Anne_Yas', 'Katilimci_Cocuk_Yas', 
                     'Cocuk_Sayisi', 'Calisma_Durumu']
    
    # Beck sütunları
    beck_cols = [col for col in df.columns if 'Beck' in col]
    important_cols.extend(beck_cols)
    
    # EMBU sütunları
    embu_cols = [col for col in df.columns if 'EMBU' in col]
    important_cols.extend(embu_cols[:23])  # İlk 23 EMBU maddesi
    
    # Mevcut sütunları filtrele
    available_cols = [col for col in important_cols if col in df.columns]
    df_analysis = df[available_cols]
    
    df_analysis.to_csv('data/cleaned/dataset_for_analysis.csv', index=False, encoding='utf-8-sig')
    df_analysis.to_excel('data/cleaned/dataset_for_analysis.xlsx', index=False)
    print(f"[OK] dataset_for_analysis.csv ve .xlsx kaydedildi ({len(available_cols)} sütun)")
    
    # 3. Diyabet grubu ayrı
    df_diabetes = df[df['Grup'] == 'Diyabet']
    df_diabetes.to_csv('data/cleaned/diabetes_group.csv', index=False, encoding='utf-8-sig')
    print(f"[OK] diabetes_group.csv kaydedildi ({len(df_diabetes)} kayıt)")
    
    # 4. Kontrol grubu ayrı
    df_control = df[df['Grup'] == 'Kontrol']
    df_control.to_csv('data/cleaned/control_group.csv', index=False, encoding='utf-8-sig')
    print(f"[OK] control_group.csv kaydedildi ({len(df_control)} kayıt)")
    
    return available_cols

def create_data_dictionary(df, important_cols):
    """Veri sözlüğü oluştur"""
    
    print("\n" + "="*60)
    print("VERİ SÖZLÜĞÜ OLUŞTURMA")
    print("="*60)
    
    with open('data/cleaned/DATA_DICTIONARY.md', 'w', encoding='utf-8') as f:
        f.write("# Veri Sözlüğü\n")
        f.write("="*60 + "\n\n")
        f.write(f"**Oluşturulma Tarihi:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        
        f.write("## Veri Setleri\n\n")
        f.write("### 1. final_dataset.csv / .xlsx\n")
        f.write(f"- **Kayıt Sayısı:** {len(df)}\n")
        f.write(f"- **Sütun Sayısı:** {len(df.columns)}\n")
        f.write(f"- **Açıklama:** Tüm temizlenmiş veri (mükerrerler temizlenmiş)\n\n")
        
        f.write("### 2. dataset_for_analysis.csv / .xlsx\n")
        f.write(f"- **Kayıt Sayısı:** {len(df)}\n")
        f.write(f"- **Sütun Sayısı:** {len(important_cols)}\n")
        f.write(f"- **Açıklama:** Analiz için önemli değişkenler\n\n")
        
        f.write("### 3. diabetes_group.csv\n")
        f.write(f"- **Kayıt Sayısı:** {(df['Grup']=='Diyabet').sum()}\n")
        f.write(f"- **Açıklama:** Sadece diyabet grubu\n\n")
        
        f.write("### 4. control_group.csv\n")
        f.write(f"- **Kayıt Sayısı:** {(df['Grup']=='Kontrol').sum()}\n")
        f.write(f"- **Açıklama:** Sadece kontrol grubu\n\n")
        
        f.write("## Değişkenler\n\n")
        
        # Değişken kategorileri
        f.write("### Demografik Değişkenler\n")
        demo_vars = ['Katilimci_No', 'Grup', 'Anne_Yas', 'Katilimci_Cocuk_Yas', 
                    'Cocuk_Sayisi', 'Calisma_Durumu', 'Egitim_Durumu']
        for var in demo_vars:
            if var in df.columns:
                non_null = df[var].notna().sum()
                f.write(f"- **{var}**: {non_null}/{len(df)} dolu\n")
        
        f.write("\n### Beck Depresyon Ölçeği\n")
        f.write("- **Beck_1 - Beck_21**: Madde skorları (0-3)\n")
        f.write("- **Beck_Toplam**: Toplam skor (0-63)\n")
        f.write("- **Beck_Total_Score**: Hesaplanmış toplam skor\n")
        f.write("- **Beck_Category**: Depresyon kategorisi\n")
        
        f.write("\n### EMBU Ebeveynlik Tutumları\n")
        f.write("- **Ebeveyn_EMBU_1 - Ebeveyn_EMBU_23**: Madde skorları (1-6)\n")
        f.write("- Alt boyutlar:\n")
        f.write("  - Duygusal Sıcaklık: 2, 4, 12, 14, 19, 23\n")
        f.write("  - Reddedicilik: 1, 7, 8, 11, 13, 17, 18, 20\n")
        f.write("  - Aşırı Koruma: 3, 5, 6, 9, 10, 15, 16, 21, 22\n")
        
        f.write("\n## Grup Dağılımı\n\n")
        for grup, count in df['Grup'].value_counts().items():
            f.write(f"- **{grup}**: {count} kayıt ({count/len(df)*100:.1f}%)\n")
        
        f.write("\n" + "="*60 + "\n")
    
    print("[OK] DATA_DICTIONARY.md kaydedildi")

def create_readme():
    """README dosyası oluştur"""
    
    readme_content = """# Temizlenmiş Veri Klasörü

## İçerik

### Ana Veri Setleri
- `final_dataset.csv` / `.xlsx`: Temizlenmiş ana veri seti
- `dataset_for_analysis.csv` / `.xlsx`: Analiz için hazır veri
- `diabetes_group.csv`: Diyabet grubu verileri
- `control_group.csv`: Kontrol grubu verileri

### Dokümantasyon
- `DATA_DICTIONARY.md`: Veri sözlüğü
- `README.md`: Bu dosya

### Arşiv Klasörü
- `archive/`: Eski veri dosyalarının yedeği

## Notlar

1. **Mükerrer Kayıtlar**: Temizlendi (194 -> 175 kayıt)
2. **DM_1-DM_89 Kayıtları**: Eksik veri nedeniyle çıkarıldı
3. **Grup Dengesizliği**: Kontrol (137) > Diyabet (38)

## Kullanım

Analiz için `dataset_for_analysis.csv` dosyasını kullanın.
"""
    
    with open('data/cleaned/README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("[OK] README.md kaydedildi")

def clean_temporary_files():
    """Geçici dosyaları temizle"""
    
    print("\n" + "="*60)
    print("GEÇİCİ DOSYALARI TEMİZLEME")
    print("="*60)
    
    temp_files = ['final_dataset_without_dm.csv']
    
    for file in temp_files:
        path = f'data/cleaned/{file}'
        if os.path.exists(path):
            os.remove(path)
            print(f"[SİLİNDİ] {file}")

def main():
    """Ana fonksiyon"""
    
    print("\n" + "="*60)
    print("DATA/CLEANED KLASÖRÜ DÜZENLEME")
    print("="*60)
    
    try:
        # 1. Eski dosyaları arşivle
        archive_old_files()
        
        # 2. Final veri setini hazırla
        df = prepare_final_dataset()
        
        # 3. Final dosyaları oluştur
        important_cols = create_final_files(df)
        
        # 4. Veri sözlüğü oluştur
        create_data_dictionary(df, important_cols)
        
        # 5. README oluştur
        create_readme()
        
        # 6. Geçici dosyaları temizle
        clean_temporary_files()
        
        print("\n" + "="*60)
        print("ÖZET")
        print("="*60)
        print("\nOluşturulan dosyalar:")
        print("  - final_dataset.csv / .xlsx")
        print("  - dataset_for_analysis.csv / .xlsx")
        print("  - diabetes_group.csv")
        print("  - control_group.csv")
        print("  - DATA_DICTIONARY.md")
        print("  - README.md")
        print("\nArşivlenen dosyalar: archive/ klasöründe")
        
        print("\n" + "="*60)
        print("DÜZENLEME TAMAMLANDI")
        print("="*60)
        
    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()