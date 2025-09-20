"""
Mükerrer Kayıtları Temizle ve Veriyi Düzenle
"""

import pandas as pd
import numpy as np
from datetime import datetime

def clean_duplicates():
    """Mükerrer kayıtları temizle"""
    
    print("="*60)
    print("MÜKERRER KAYIT TEMİZLEME")
    print("="*60)
    
    # Veriyi yükle
    df = pd.read_csv('data/cleaned/cleaned_dataset.csv')
    print(f"\nBaşlangıç: {len(df)} satır")
    
    # Mükerrer kayıtları tespit et
    duplicates = df[df.duplicated(subset=['Katilimci_No'], keep=False)]
    unique_dup_ids = duplicates['Katilimci_No'].unique()
    print(f"Mükerrer ID sayısı: {len(unique_dup_ids)}")
    print(f"Toplam mükerrer satır: {len(duplicates)}")
    
    # Mükerrer kayıtları incele
    print("\nMükerrer Kayıt Detayları:")
    for participant_id in unique_dup_ids[:5]:  # İlk 5 örnek
        dup_rows = df[df['Katilimci_No'] == participant_id]
        print(f"\n{participant_id}: {len(dup_rows)} kayıt")
        
        # Beck skorlarını karşılaştır
        beck_scores = dup_rows['Beck_Total_Score'].values
        if len(set(beck_scores)) == 1:
            print(f"  Beck skorları aynı: {beck_scores[0]}")
        else:
            print(f"  Beck skorları farklı: {beck_scores}")
    
    # Mükerrer kayıtları temizle
    # Strateji: Her katılımcı için ilk kayıtı tut
    df_clean = df.drop_duplicates(subset=['Katilimci_No'], keep='first')
    
    print(f"\nTemizleme sonrası: {len(df_clean)} satır")
    print(f"Silinen kayıt: {len(df) - len(df_clean)}")
    
    # Benzersiz katılımcı sayısını kontrol et
    unique_participants = df_clean['Katilimci_No'].nunique()
    print(f"Benzersiz katılımcı: {unique_participants}")
    
    return df_clean

def verify_embu_conversion(df):
    """EMBU ölçek dönüşümü doğrula"""
    
    print("\n" + "="*60)
    print("EMBU ÖLÇEK DOĞRULAMA")
    print("="*60)
    
    embu_cols = [col for col in df.columns if 'EMBU' in col]
    
    conversion_needed = False
    
    for col in embu_cols:
        values = df[col].dropna()
        max_val = values.max()
        
        if max_val <= 4:
            print(f"\n[!] {col}: 4'lü skalada (max={max_val})")
            conversion_needed = True
            
            # Dönüşüm formülü: 
            # 4'lü -> 6'lı: yeni_değer = (eski_değer - 1) * (5/3) + 1
            # 1->1, 2->2.67, 3->4.33, 4->6
            
            print(f"  Dönüştürülüyor...")
            df[col] = df[col].apply(lambda x: ((x - 1) * (5/3) + 1) if pd.notna(x) else x)
            
            new_max = df[col].max()
            print(f"  Yeni maksimum: {new_max:.2f}")
    
    if not conversion_needed:
        print("\nTüm EMBU verileri zaten 6'lı skalada")
    
    return df

def fix_missing_data(df):
    """Eksik verileri düzenle"""
    
    print("\n" + "="*60)
    print("EKSİK VERİ DÜZENLEME")
    print("="*60)
    
    # Beck alt ölçek hesaplamaları
    beck_items = [f'Beck_{i}' for i in range(1, 22)]
    
    # Eksik Beck maddelerini doldur (ortalama imputation)
    print("\nBeck eksik maddeleri dolduruluyor...")
    for col in beck_items:
        if col in df.columns:
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                # Grup bazında ortalama ile doldur
                df[col] = df.groupby('Grup')[col].transform(
                    lambda x: x.fillna(x.mean())
                )
                print(f"  {col}: {missing_count} eksik dolduruldu")
    
    # Beck toplamı yeniden hesapla
    print("\nBeck toplam skorları yeniden hesaplanıyor...")
    df['Beck_Calculated'] = df[beck_items].sum(axis=1)
    
    # Tutarlılık kontrolü
    if 'Beck_Total_Score' in df.columns:
        corr = df['Beck_Calculated'].corr(df['Beck_Total_Score'])
        print(f"Hesaplanan vs Mevcut Beck korelasyonu: {corr:.3f}")
    
    return df

def fix_group_imbalance(df):
    """Grup dengesizliğini kontrol et"""
    
    print("\n" + "="*60)
    print("GRUP DENGESİZLİĞİ KONTROLÜ")
    print("="*60)
    
    group_counts = df['Grup'].value_counts()
    print("\nMevcut grup dağılımı:")
    for grup, count in group_counts.items():
        print(f"  {grup}: {count} ({count/len(df)*100:.1f}%)")
    
    # DM tanı tarihi olan ancak Kontrol grubunda olanlar var mı?
    if 'DM Tanı Tarihi' in df.columns:
        kontrolde_dm = df[(df['Grup'] == 'Kontrol') & df['DM Tanı Tarihi'].notna()]
        if len(kontrolde_dm) > 0:
            print(f"\n[!] Kontrol grubunda {len(kontrolde_dm)} DM tanılı kayıt var!")
    
    # Katılımcı numarası kontrolü
    d_participants = df[df['Katilimci_No'].str.startswith('D', na=False)]
    k_participants = df[df['Katilimci_No'].str.startswith('K', na=False)]
    
    if len(d_participants) > 0:
        print(f"\nD ile başlayan: {len(d_participants)} kayıt")
        d_grup = d_participants['Grup'].value_counts()
        for grup, count in d_grup.items():
            print(f"  {grup}: {count}")
    
    if len(k_participants) > 0:
        print(f"\nK ile başlayan: {len(k_participants)} kayıt")
        k_grup = k_participants['Grup'].value_counts()
        for grup, count in k_grup.items():
            print(f"  {grup}: {count}")
    
    return df

def save_cleaned_data(df):
    """Temizlenmiş veriyi kaydet"""
    
    print("\n" + "="*60)
    print("VERİYİ KAYDETME")
    print("="*60)
    
    # Yedek al
    import shutil
    import os
    
    backup_dir = 'data/backup'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Mevcut dosyaları yedekle
    if os.path.exists('data/cleaned/cleaned_dataset.csv'):
        shutil.copy2('data/cleaned/cleaned_dataset.csv', 
                    f'{backup_dir}/cleaned_dataset_{timestamp}.csv')
        print(f"[OK] Yedek alındı: cleaned_dataset_{timestamp}.csv")
    
    # Temizlenmiş veriyi kaydet
    df.to_csv('data/cleaned/cleaned_dataset_no_duplicates.csv', index=False, encoding='utf-8-sig')
    df.to_excel('data/cleaned/cleaned_dataset_no_duplicates.xlsx', index=False)
    
    print("[OK] Temizlenmiş veri kaydedildi:")
    print("  - data/cleaned/cleaned_dataset_no_duplicates.csv")
    print("  - data/cleaned/cleaned_dataset_no_duplicates.xlsx")
    
    # Özet istatistikler
    print(f"\nFinal veri:")
    print(f"  Satır sayısı: {len(df)}")
    print(f"  Sütun sayısı: {len(df.columns)}")
    print(f"  Benzersiz katılımcı: {df['Katilimci_No'].nunique()}")
    print(f"  Grup dağılımı: {df['Grup'].value_counts().to_dict()}")
    
    return df

def create_data_quality_summary(df):
    """Veri kalite özeti oluştur"""
    
    summary = []
    summary.append("="*70)
    summary.append("VERİ TEMİZLİK VE KALİTE ÖZETİ")
    summary.append("="*70)
    summary.append(f"\nTarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    summary.append("\n" + "="*70)
    summary.append("TEMİZLEME SONUÇLARI")
    summary.append("="*70)
    
    summary.append(f"\nFinal veri boyutu: {df.shape[0]} x {df.shape[1]}")
    summary.append(f"Benzersiz katılımcı: {df['Katilimci_No'].nunique()}")
    
    # Grup dağılımı
    summary.append("\nGrup Dağılımı:")
    for grup, count in df['Grup'].value_counts().items():
        summary.append(f"  {grup}: {count} ({count/len(df)*100:.1f}%)")
    
    # Eksik veri durumu
    missing_total = df.isnull().sum().sum()
    missing_pct = (missing_total / (df.shape[0] * df.shape[1])) * 100
    summary.append(f"\nToplam eksik veri: {missing_total} ({missing_pct:.2f}%)")
    
    # EMBU skala durumu
    embu_cols = [col for col in df.columns if 'EMBU' in col]
    if embu_cols:
        embu_sample = df[embu_cols[0]].dropna()
        summary.append(f"\nEMBU skala aralığı: {embu_sample.min():.1f} - {embu_sample.max():.1f}")
    
    # Beck skoru durumu
    if 'Beck_Total_Score' in df.columns:
        beck_stats = df.groupby('Grup')['Beck_Total_Score'].agg(['mean', 'std'])
        summary.append("\nBeck Skorları:")
        for grup in beck_stats.index:
            mean = beck_stats.loc[grup, 'mean']
            std = beck_stats.loc[grup, 'std']
            summary.append(f"  {grup}: {mean:.1f} ± {std:.1f}")
    
    summary.append("\n" + "="*70)
    
    return "\n".join(summary)

def main():
    """Ana fonksiyon"""
    
    print("\n" + "="*60)
    print("VERİ TEMİZLEME VE DÜZENLEME")
    print("="*60)
    
    try:
        # 1. Mükerrer kayıtları temizle
        df = clean_duplicates()
        
        # 2. EMBU dönüşümü kontrol et
        df = verify_embu_conversion(df)
        
        # 3. Eksik verileri düzenle
        df = fix_missing_data(df)
        
        # 4. Grup dengesizliğini kontrol et
        df = fix_group_imbalance(df)
        
        # 5. Temizlenmiş veriyi kaydet
        df = save_cleaned_data(df)
        
        # 6. Özet rapor oluştur
        summary = create_data_quality_summary(df)
        
        with open('results/data_cleaning_summary.txt', 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print("\n" + summary)
        
        print("\n" + "="*60)
        print("VERİ TEMİZLEME TAMAMLANDI")
        print("="*60)
        
        return df
        
    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()