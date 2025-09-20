"""
Tüm Veri Kaynaklarını Entegre Et
Google Drive'dan indirilen yeni verilerle mevcut verileri birleştir
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def analyze_new_data():
    """Yeni indirilen verileri analiz et"""
    
    print("="*70)
    print("YENİ VERİ ANALİZİ")
    print("="*70)
    
    # DM+ Çocuk EMBU verisi
    print("\n1. DM_Cocuk_EMBU.xlsx analizi:")
    df_dm = pd.read_excel('data/raw/DM_Cocuk_EMBU.xlsx')
    print(f"   Toplam satır: {len(df_dm)}")
    print(f"   Toplam sütun: {len(df_dm.columns)}")
    
    # Katılımcı sayısı
    if 'Katılımcı_no' in df_dm.columns:
        unique_participants = df_dm['Katılımcı_no'].nunique()
        print(f"   Benzersiz katılımcı: {unique_participants}")
    
    # DM tanı tarihi kontrolü
    dm_date_cols = [col for col in df_dm.columns if 'DM' in col.upper() or 'tanı' in col.lower()]
    if dm_date_cols:
        print(f"   DM ile ilgili sütunlar: {dm_date_cols[:3]}")
        for col in dm_date_cols:
            non_empty = (~df_dm[col].isna()).sum()
            print(f"     {col}: {non_empty} dolu kayıt")
    
    # SPSS verisi
    print("\n2. spss_20012025.xlsx analizi:")
    try:
        df_spss = pd.read_excel('data/raw/spss_20012025.xlsx')
        print(f"   Toplam satır: {len(df_spss)}")
        print(f"   Toplam sütun: {len(df_spss.columns)}")
        
        # İlk birkaç sütun
        print(f"   İlk sütunlar: {list(df_spss.columns[:5])}")
    except Exception as e:
        print(f"   HATA: {e}")
        df_spss = None
    
    return df_dm, df_spss

def compare_with_existing_data(df_dm, df_existing):
    """Yeni veri ile mevcut veriyi karşılaştır"""
    
    print("\n" + "="*70)
    print("VERİ KARŞILAŞTIRMA")
    print("="*70)
    
    # Mevcut veri
    print("\nMevcut veri (cleaned_dataset_no_duplicates.csv):")
    print(f"  Satır: {len(df_existing)}")
    print(f"  Diyabet grubu: {(df_existing['Grup'] == 'Diyabet').sum()}")
    print(f"  Kontrol grubu: {(df_existing['Grup'] == 'Kontrol').sum()}")
    
    # Yeni veri
    print("\nYeni veri (DM_Cocuk_EMBU.xlsx):")
    print(f"  Satır: {len(df_dm)}")
    print(f"  Benzersiz ID: {df_dm['Katılımcı_no'].nunique() if 'Katılımcı_no' in df_dm.columns else 'N/A'}")
    
    # ID format farkları
    if 'Katilimci_No' in df_existing.columns:
        existing_ids = set(df_existing['Katilimci_No'].astype(str).unique())
        print(f"\nMevcut veri ID örnekleri: {list(existing_ids)[:5]}")
    
    if 'Katılımcı_no' in df_dm.columns:
        new_ids = set(df_dm['Katılımcı_no'].astype(str).unique())
        print(f"Yeni veri ID örnekleri: {list(new_ids)[:10]}")
        
        # Ortak ID'ler var mı?
        if 'Katilimci_No' in df_existing.columns:
            common_ids = existing_ids.intersection(new_ids)
            print(f"\nOrtak ID sayısı: {len(common_ids)}")
            if common_ids:
                print(f"Ortak ID örnekleri: {list(common_ids)[:5]}")

def integrate_datasets(df_dm, df_existing):
    """Veri setlerini entegre et"""
    
    print("\n" + "="*70)
    print("VERİ ENTEGRASYONU")
    print("="*70)
    
    # Sütun eşleştirme
    column_mapping = {
        'Katılımcı_no': 'Katilimci_No',
        'Anket_tarihi': 'Anket_Tarihi',
        'Anne_Doğum_tarihi': 'Anne_Dogum_Tarihi',
        # Diğer sütunlar...
    }
    
    # Yeni veriyi hazırla
    df_dm_clean = df_dm.copy()
    
    # Boş satırları temizle
    df_dm_clean = df_dm_clean.dropna(subset=['Katılımcı_no'])
    print(f"\nBoş ID'ler temizlendi: {len(df_dm)} -> {len(df_dm_clean)} satır")
    
    # Benzersiz katılımcılar
    df_dm_unique = df_dm_clean.drop_duplicates(subset=['Katılımcı_no'], keep='first')
    print(f"Mükerrerler temizlendi: {len(df_dm_clean)} -> {len(df_dm_unique)} satır")
    
    # Grup ataması
    # DM tanı tarihi sütunu varsa kullan
    dm_date_col = None
    for col in df_dm_unique.columns:
        if 'DM' in col.upper() and 'tanı' in col.lower():
            dm_date_col = col
            break
    
    if dm_date_col:
        print(f"\nDM tanı tarihi sütunu bulundu: {dm_date_col}")
        has_dm = (~df_dm_unique[dm_date_col].isna()).sum()
        print(f"DM tanısı olan: {has_dm}")
        
        # Grup ata
        df_dm_unique['Grup'] = df_dm_unique[dm_date_col].apply(
            lambda x: 'Diyabet' if pd.notna(x) else 'Kontrol'
        )
    else:
        # Tümü diyabet grubu olarak işaretle (çünkü dosya adı DM+)
        print("\nDosya adına göre tüm kayıtlar Diyabet grubu olarak işaretleniyor")
        df_dm_unique['Grup'] = 'Diyabet'
    
    print(f"\nYeni veri grup dağılımı:")
    print(df_dm_unique['Grup'].value_counts())
    
    # ID formatını düzenle
    df_dm_unique['Katilimci_No'] = 'DM_' + df_dm_unique['Katılımcı_no'].astype(str)
    
    # Mevcut veri ile birleştir
    print("\nVeriler birleştiriliyor...")
    
    # Ortak sütunları bul
    common_cols = set(df_existing.columns).intersection(set(df_dm_unique.columns))
    print(f"Ortak sütunlar: {len(common_cols)}")
    
    # Sadece önemli sütunları seç
    important_cols = ['Katilimci_No', 'Grup']
    
    # Beck sütunları
    beck_cols = [col for col in df_dm_unique.columns if 'Beck' in col or 'beck' in col]
    if beck_cols:
        print(f"Beck sütunları bulundu: {len(beck_cols)}")
        important_cols.extend(beck_cols[:21])  # Beck 1-21
    
    # EMBU sütunları
    embu_cols = [col for col in df_dm_unique.columns if 'EMBU' in col or 'embu' in col]
    if embu_cols:
        print(f"EMBU sütunları bulundu: {len(embu_cols)}")
        important_cols.extend(embu_cols)
    
    # Seçilen sütunlarla yeni DataFrame
    available_cols = [col for col in important_cols if col in df_dm_unique.columns]
    df_dm_final = df_dm_unique[available_cols]
    
    print(f"\nEntegre edilecek yeni veri:")
    print(f"  Satır: {len(df_dm_final)}")
    print(f"  Sütun: {len(df_dm_final.columns)}")
    
    return df_dm_final

def create_final_integrated_dataset(df_existing, df_new):
    """Final entegre veri setini oluştur"""
    
    print("\n" + "="*70)
    print("FİNAL VERİ SETİ OLUŞTURULUYOR")
    print("="*70)
    
    # Veri setlerini birleştir
    df_integrated = pd.concat([df_existing, df_new], ignore_index=True, sort=False)
    
    print(f"\nBirleştirilmiş veri:")
    print(f"  Toplam satır: {len(df_integrated)}")
    print(f"  Toplam sütun: {len(df_integrated.columns)}")
    print(f"  Benzersiz katılımcı: {df_integrated['Katilimci_No'].nunique()}")
    
    # Grup dağılımı
    print(f"\nGrup dağılımı:")
    for grup, count in df_integrated['Grup'].value_counts().items():
        print(f"  {grup}: {count} ({count/len(df_integrated)*100:.1f}%)")
    
    # Eksik verileri doldur
    print("\nEksik veriler dolduruluyor...")
    
    # Beck skorlarını hesapla
    beck_items = [f'Beck_{i}' for i in range(1, 22)]
    available_beck = [col for col in beck_items if col in df_integrated.columns]
    
    if available_beck:
        df_integrated['Beck_Total_Calculated'] = df_integrated[available_beck].sum(axis=1)
        
        # Eğer Beck_Total_Score boşsa, hesaplananı kullan
        if 'Beck_Total_Score' not in df_integrated.columns:
            df_integrated['Beck_Total_Score'] = df_integrated['Beck_Total_Calculated']
        else:
            df_integrated['Beck_Total_Score'] = df_integrated['Beck_Total_Score'].fillna(
                df_integrated['Beck_Total_Calculated']
            )
    
    return df_integrated

def save_integrated_data(df_integrated):
    """Entegre veriyi kaydet"""
    
    print("\n" + "="*70)
    print("VERİYİ KAYDETME")
    print("="*70)
    
    # Kaydet
    output_path = 'data/cleaned/final_integrated_dataset.csv'
    df_integrated.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"[OK] CSV kaydedildi: {output_path}")
    
    output_excel = 'data/cleaned/final_integrated_dataset.xlsx'
    df_integrated.to_excel(output_excel, index=False)
    print(f"[OK] Excel kaydedildi: {output_excel}")
    
    # Özet rapor
    with open('results/data_integration_report.txt', 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("VERİ ENTEGRASYON RAPORU\n")
        f.write("="*70 + "\n")
        f.write(f"\nTarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"\nFinal Veri Seti:\n")
        f.write(f"  Toplam kayıt: {len(df_integrated)}\n")
        f.write(f"  Benzersiz katılımcı: {df_integrated['Katilimci_No'].nunique()}\n")
        f.write(f"\nGrup Dağılımı:\n")
        for grup, count in df_integrated['Grup'].value_counts().items():
            f.write(f"  {grup}: {count} ({count/len(df_integrated)*100:.1f}%)\n")
        f.write("\n" + "="*70 + "\n")
    
    print("[OK] Rapor kaydedildi: results/data_integration_report.txt")
    
    return df_integrated

def main():
    """Ana fonksiyon"""
    
    print("\n" + "="*70)
    print("TÜM VERİ KAYNAKLARINI ENTEGRE ETME")
    print("="*70)
    
    try:
        # 1. Yeni verileri analiz et
        df_dm, df_spss = analyze_new_data()
        
        # 2. Mevcut veriyi yükle
        df_existing = pd.read_csv('data/cleaned/cleaned_dataset_no_duplicates.csv')
        
        # 3. Verileri karşılaştır
        compare_with_existing_data(df_dm, df_existing)
        
        # 4. Veri setlerini entegre et
        df_new = integrate_datasets(df_dm, df_existing)
        
        # 5. Final veri setini oluştur
        df_integrated = create_final_integrated_dataset(df_existing, df_new)
        
        # 6. Entegre veriyi kaydet
        df_final = save_integrated_data(df_integrated)
        
        print("\n" + "="*70)
        print("ÖZET")
        print("="*70)
        print(f"\nBaşlangıç: {len(df_existing)} kayıt, {(df_existing['Grup']=='Diyabet').sum()} diyabet")
        print(f"Eklenen: {len(df_new)} yeni kayıt")
        print(f"Final: {len(df_final)} kayıt, {(df_final['Grup']=='Diyabet').sum()} diyabet")
        print(f"\nProtokol hedefi: ~100 diyabet hastası")
        print(f"Ulaşılan: {(df_final['Grup']=='Diyabet').sum()} diyabet hastası")
        
        print("\n" + "="*70)
        print("ENTEGRASYON TAMAMLANDI")
        print("="*70)
        
    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()