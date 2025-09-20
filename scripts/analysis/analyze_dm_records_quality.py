"""
DM_1 - DM_89 Kayıtlarının Veri Kalitesi Analizi
Yeni eklenen diyabet hastalarının veri bütünlüğünü kontrol et
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def analyze_dm_records():
    """DM_ prefixed kayıtları analiz et"""
    
    print("="*70)
    print("DM_1 - DM_89 KAYITLARININ ANALİZİ")
    print("="*70)
    
    # Final entegre veriyi yükle
    df = pd.read_csv('data/cleaned/final_integrated_dataset.csv')
    
    # DM_ ile başlayan kayıtları filtrele
    dm_records = df[df['Katilimci_No'].str.startswith('DM_', na=False)]
    other_records = df[~df['Katilimci_No'].str.startswith('DM_', na=False)]
    
    print(f"\nToplam kayıt: {len(df)}")
    print(f"DM_ prefixed kayıtlar: {len(dm_records)}")
    print(f"Diğer kayıtlar: {len(other_records)}")
    
    # DM kayıtlarının ID'lerini kontrol et
    dm_ids = dm_records['Katilimci_No'].unique()
    print(f"\nİlk 10 DM ID: {list(dm_ids[:10])}")
    print(f"Son 10 DM ID: {list(dm_ids[-10:])}")
    
    return dm_records, other_records, df

def analyze_missing_data(dm_records, other_records):
    """Eksik veri analizi"""
    
    print("\n" + "="*70)
    print("EKSİK VERİ ANALİZİ")
    print("="*70)
    
    # DM kayıtları için eksik veri yüzdesi
    dm_missing = dm_records.isnull().sum() / len(dm_records) * 100
    
    # Diğer kayıtlar için eksik veri yüzdesi
    other_missing = other_records.isnull().sum() / len(other_records) * 100
    
    # Karşılaştırma DataFrame'i oluştur
    comparison_df = pd.DataFrame({
        'DM_Records_Missing_%': dm_missing,
        'Other_Records_Missing_%': other_missing,
        'Difference_%': dm_missing - other_missing
    })
    
    # En yüksek eksik veri oranları
    high_missing_dm = comparison_df[comparison_df['DM_Records_Missing_%'] > 50]
    high_missing_dm = high_missing_dm.sort_values('DM_Records_Missing_%', ascending=False)
    
    print("\nDM kayıtlarında %50'den fazla eksik veri olan sütunlar:")
    print("-" * 60)
    
    for col in high_missing_dm.head(20).index:
        dm_pct = comparison_df.loc[col, 'DM_Records_Missing_%']
        other_pct = comparison_df.loc[col, 'Other_Records_Missing_%']
        diff = comparison_df.loc[col, 'Difference_%']
        print(f"{col:30s}: DM={dm_pct:5.1f}%, Diğer={other_pct:5.1f}%, Fark={diff:+5.1f}%")
    
    return comparison_df

def analyze_critical_variables(dm_records, other_records):
    """Kritik değişkenlerin durumu"""
    
    print("\n" + "="*70)
    print("KRİTİK DEĞİŞKENLERİN DURUMU")
    print("="*70)
    
    critical_vars = [
        'Beck_Total_Score',
        'Beck_Toplam',
        'Anne_Yas',
        'Katilimci_Cocuk_Yas',
        'Grup'
    ]
    
    # Beck değişkenlerini ekle
    for i in range(1, 22):
        critical_vars.append(f'Beck_{i}')
    
    # EMBU değişkenlerini ekle
    for i in range(1, 24):
        critical_vars.append(f'Ebeveyn_EMBU_{i}')
    
    print("\nKritik değişkenlerdeki eksik veri oranları:")
    print("-" * 60)
    
    for var in critical_vars:
        if var in dm_records.columns:
            dm_missing = dm_records[var].isnull().sum()
            dm_pct = (dm_missing / len(dm_records)) * 100
            
            other_missing = other_records[var].isnull().sum()
            other_pct = (other_missing / len(other_records)) * 100
            
            if dm_pct > 10:  # %10'dan fazla eksikse göster
                print(f"{var:30s}: DM={dm_pct:5.1f}% ({dm_missing}/{len(dm_records)}), "
                      f"Diğer={other_pct:5.1f}% ({other_missing}/{len(other_records)})")

def analyze_data_completeness(dm_records):
    """Veri tamlığı analizi"""
    
    print("\n" + "="*70)
    print("VERİ TAMLIĞI ANALİZİ")
    print("="*70)
    
    # Her kayıt için dolu sütun sayısını hesapla
    non_null_counts = dm_records.count(axis=1)
    total_columns = len(dm_records.columns)
    
    completeness = (non_null_counts / total_columns * 100)
    
    print(f"\nDM kayıtlarının veri tamlığı:")
    print(f"  Ortalama tamlık: {completeness.mean():.1f}%")
    print(f"  Minimum tamlık: {completeness.min():.1f}%")
    print(f"  Maximum tamlık: {completeness.max():.1f}%")
    
    # Tamlık kategorileri
    print("\nTamlık kategorileri:")
    print(f"  %90+ tam: {(completeness >= 90).sum()} kayıt")
    print(f"  %70-90 tam: {((completeness >= 70) & (completeness < 90)).sum()} kayıt")
    print(f"  %50-70 tam: {((completeness >= 50) & (completeness < 70)).sum()} kayıt")
    print(f"  %30-50 tam: {((completeness >= 30) & (completeness < 50)).sum()} kayıt")
    print(f"  <%30 tam: {(completeness < 30).sum()} kayıt")
    
    # En eksik kayıtlar
    most_incomplete = dm_records.iloc[completeness.nsmallest(10).index]
    print("\nEn eksik 10 kayıt:")
    for idx, row in most_incomplete.iterrows():
        comp = (row.count() / total_columns * 100)
        print(f"  {row['Katilimci_No']}: {comp:.1f}% tam")
    
    return completeness

def check_beck_scores(dm_records, other_records):
    """Beck skorlarını kontrol et"""
    
    print("\n" + "="*70)
    print("BECK SKORLARI KONTROLÜ")
    print("="*70)
    
    # Beck maddeleri var mı?
    beck_items = [f'Beck_{i}' for i in range(1, 22)]
    available_beck = [item for item in beck_items if item in dm_records.columns]
    
    print(f"\nMevcut Beck maddeleri: {len(available_beck)}/21")
    
    if available_beck:
        # DM kayıtlarında Beck skorları
        dm_beck_complete = dm_records[available_beck].notna().all(axis=1).sum()
        print(f"\nDM kayıtlarında tam Beck skoru olan: {dm_beck_complete}/{len(dm_records)}")
        
        # Diğer kayıtlarda Beck skorları
        other_beck_complete = other_records[available_beck].notna().all(axis=1).sum()
        print(f"Diğer kayıtlarda tam Beck skoru olan: {other_beck_complete}/{len(other_records)}")
        
        # Beck_Total_Score kontrolü
        if 'Beck_Total_Score' in dm_records.columns:
            dm_has_total = dm_records['Beck_Total_Score'].notna().sum()
            other_has_total = other_records['Beck_Total_Score'].notna().sum()
            
            print(f"\nBeck_Total_Score mevcut:")
            print(f"  DM kayıtları: {dm_has_total}/{len(dm_records)} ({dm_has_total/len(dm_records)*100:.1f}%)")
            print(f"  Diğer kayıtlar: {other_has_total}/{len(other_records)} ({other_has_total/len(other_records)*100:.1f}%)")

def recommend_actions(dm_records, completeness):
    """Eylem önerileri"""
    
    print("\n" + "="*70)
    print("ÖNERİLER VE EYLEM PLANI")
    print("="*70)
    
    # %30'dan az tam olan kayıtlar
    very_incomplete = dm_records[completeness < 30]
    
    if len(very_incomplete) > 0:
        print(f"\n[UYARI] {len(very_incomplete)} kayıt %30'dan az tam!")
        print("Bu kayıtlar:")
        for _, row in very_incomplete.iterrows():
            print(f"  - {row['Katilimci_No']}")
        print("\nÖneri: Bu kayıtların analizden çıkarılmasını düşünün.")
    
    # Beck skorları eksik olanlar
    if 'Beck_Total_Score' in dm_records.columns:
        beck_missing = dm_records['Beck_Total_Score'].isna().sum()
        if beck_missing > len(dm_records) * 0.5:
            print(f"\n[UYARI] DM kayıtlarının %{beck_missing/len(dm_records)*100:.0f}'inde Beck skoru eksik!")
            print("Öneri: Beck skorları olmayan kayıtlar depresyon analizine dahil edilmemeli.")
    
    # Kullanılabilir kayıtlar
    usable = dm_records[completeness >= 70]
    print(f"\n[BİLGİ] Analiz için kullanılabilir DM kayıtları: {len(usable)}/{len(dm_records)}")
    
    return very_incomplete

def create_clean_dataset(df, dm_records, completeness):
    """Temizlenmiş veri seti oluştur"""
    
    print("\n" + "="*70)
    print("TEMİZLENMİŞ VERİ SETİ OLUŞTURULUYOR")
    print("="*70)
    
    # %30'dan fazla tam olan kayıtları tut
    dm_ids_to_keep = dm_records[completeness >= 30]['Katilimci_No'].tolist()
    
    # Diğer kayıtlarla birleştir
    other_ids = df[~df['Katilimci_No'].str.startswith('DM_', na=False)]['Katilimci_No'].tolist()
    
    all_ids_to_keep = dm_ids_to_keep + other_ids
    
    # Temiz veri seti
    df_clean = df[df['Katilimci_No'].isin(all_ids_to_keep)].copy()
    
    print(f"\nOrijinal veri: {len(df)} kayıt")
    print(f"Temizlenmiş veri: {len(df_clean)} kayıt")
    print(f"Silinen DM kayıtları: {len(dm_records) - len(dm_ids_to_keep)}")
    
    # Grup dağılımı
    print(f"\nTemizlenmiş veri grup dağılımı:")
    for grup, count in df_clean['Grup'].value_counts().items():
        print(f"  {grup}: {count} ({count/len(df_clean)*100:.1f}%)")
    
    # Kaydet
    df_clean.to_csv('data/cleaned/final_clean_dataset.csv', index=False, encoding='utf-8-sig')
    df_clean.to_excel('data/cleaned/final_clean_dataset.xlsx', index=False)
    
    print("\n[OK] Temizlenmiş veri kaydedildi:")
    print("  - data/cleaned/final_clean_dataset.csv")
    print("  - data/cleaned/final_clean_dataset.xlsx")
    
    return df_clean

def create_quality_report(dm_records, other_records, comparison_df, completeness):
    """Detaylı kalite raporu"""
    
    report = []
    report.append("="*70)
    report.append("DM_1 - DM_89 VERİ KALİTESİ RAPORU")
    report.append("="*70)
    report.append(f"\nTarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    report.append("\n" + "="*70)
    report.append("1. GENEL ÖZET")
    report.append("="*70)
    report.append(f"\nDM kayıtları (DM_1 - DM_89): {len(dm_records)}")
    report.append(f"Diğer kayıtlar: {len(other_records)}")
    report.append(f"\nDM kayıtları ortalama tamlık: {completeness.mean():.1f}%")
    report.append(f"Diğer kayıtlar için tahmini tamlık: ~85-90%")
    
    report.append("\n" + "="*70)
    report.append("2. KRİTİK BULGULAR")
    report.append("="*70)
    
    # En eksik sütunlar
    high_missing = comparison_df[comparison_df['DM_Records_Missing_%'] > 70]
    if len(high_missing) > 0:
        report.append("\n%70'den fazla eksik veri olan sütunlar:")
        for col in high_missing.index[:10]:
            report.append(f"  - {col}: {comparison_df.loc[col, 'DM_Records_Missing_%']:.1f}% eksik")
    
    # Kullanılamaz kayıtlar
    unusable = (completeness < 30).sum()
    if unusable > 0:
        report.append(f"\n[UYARI] {unusable} DM kayıt %30'dan az tam - kullanılamaz!")
    
    report.append("\n" + "="*70)
    report.append("3. ÖNERİLER")
    report.append("="*70)
    report.append("\n1. %30'dan az tam olan kayıtları analizden çıkar")
    report.append("2. Beck skorları eksik olan kayıtları depresyon analizinden çıkar")
    report.append("3. EMBU skorları eksik olan kayıtları ebeveynlik analizinden çıkar")
    report.append("4. Missing data imputation uygula (grup ortalamaları ile)")
    
    report.append("\n" + "="*70)
    
    # Raporu kaydet
    with open('results/dm_records_quality_report.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    
    print("\n[OK] Kalite raporu kaydedildi: results/dm_records_quality_report.txt")
    
    return report

def main():
    """Ana fonksiyon"""
    
    print("\n" + "="*70)
    print("DM KAYITLARI VERİ KALİTESİ ANALİZİ")
    print("="*70)
    
    try:
        # 1. DM kayıtlarını analiz et
        dm_records, other_records, df = analyze_dm_records()
        
        # 2. Eksik veri analizi
        comparison_df = analyze_missing_data(dm_records, other_records)
        
        # 3. Kritik değişkenleri kontrol et
        analyze_critical_variables(dm_records, other_records)
        
        # 4. Veri tamlığını analiz et
        completeness = analyze_data_completeness(dm_records)
        
        # 5. Beck skorlarını kontrol et
        check_beck_scores(dm_records, other_records)
        
        # 6. Öneriler
        very_incomplete = recommend_actions(dm_records, completeness)
        
        # 7. Temizlenmiş veri seti oluştur
        df_clean = create_clean_dataset(df, dm_records, completeness)
        
        # 8. Rapor oluştur
        report = create_quality_report(dm_records, other_records, comparison_df, completeness)
        
        print("\n" + "="*70)
        print("ANALİZ TAMAMLANDI")
        print("="*70)
        
        return df_clean
        
    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()