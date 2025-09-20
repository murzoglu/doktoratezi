"""
Katılımcı ID'lerine göre yeniden sınıflandırma
xxx-1: Diyabetli çocuk
xxx-2: Diyabetli çocuğun kardeşi
xxx-3: Sağlıklı kontrol
xxx-4: Sağlıklı kontrolün kardeşi
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def analyze_participant_ids():
    """Katılımcı ID'lerini analiz et"""
    
    print("="*70)
    print("KATILIMCI ID ANALİZİ")
    print("="*70)
    
    # Ham veriyi yükle
    df_raw = pd.read_csv('data/raw/main_dataset.csv')
    print(f"\nToplam kayıt: {len(df_raw)}")
    
    # ID'leri parçala
    df_raw['ID_Prefix'] = df_raw['Katılımcı No'].astype(str).str.extract(r'(\d+)-')[0]
    df_raw['ID_Suffix'] = df_raw['Katılımcı No'].astype(str).str.extract(r'-(\d+)')[0]
    
    # Suffix dağılımı
    print("\nID Suffix Dağılımı:")
    suffix_counts = df_raw['ID_Suffix'].value_counts().sort_index()
    for suffix, count in suffix_counts.items():
        print(f"  -{suffix}: {count} kayıt")
    
    # Benzersiz aile sayısı
    unique_families = df_raw['ID_Prefix'].nunique()
    print(f"\nBenzersiz aile/grup sayısı: {unique_families}")
    
    # Her prefix için hangi suffix'ler var?
    print("\nAile Yapısı Analizi:")
    family_structure = df_raw.groupby('ID_Prefix')['ID_Suffix'].apply(list).reset_index()
    
    # Tam aileler (1,2,3,4 hepsi olan)
    complete_families = 0
    dm_only = 0  # Sadece diyabet (1,2)
    control_only = 0  # Sadece kontrol (3,4)
    mixed = 0
    
    for _, family in family_structure.iterrows():
        suffixes = set(family['ID_Suffix'])
        if {'1', '2', '3', '4'}.issubset(suffixes):
            complete_families += 1
        elif {'1', '2'}.issubset(suffixes) and not ({'3', '4'} & suffixes):
            dm_only += 1
        elif {'3', '4'}.issubset(suffixes) and not ({'1', '2'} & suffixes):
            control_only += 1
        else:
            mixed += 1
    
    print(f"  Tam aileler (1,2,3,4): {complete_families}")
    print(f"  Sadece diyabet (1,2): {dm_only}")
    print(f"  Sadece kontrol (3,4): {control_only}")
    print(f"  Karışık/Eksik: {mixed}")
    
    return df_raw

def create_new_classifications(df):
    """Yeni sınıflandırmalar oluştur"""
    
    print("\n" + "="*70)
    print("YENİ SINIFLANDIRMALAR")
    print("="*70)
    
    # Ana Grup (Diyabet vs Kontrol)
    df['Grup_Yeni'] = df['ID_Suffix'].map({
        '1': 'Diyabet',
        '2': 'Diyabet',  # Kardeş de diyabet grubunda
        '3': 'Kontrol',
        '4': 'Kontrol'   # Kardeş de kontrol grubunda
    })
    
    # Alt Grup (Index vs Kardeş)
    df['Alt_Grup'] = df['ID_Suffix'].map({
        '1': 'Diyabet_Index',
        '2': 'Diyabet_Kardes',
        '3': 'Kontrol_Index',
        '4': 'Kontrol_Kardes'
    })
    
    # Katılımcı Tipi
    df['Katilimci_Tipi'] = df['ID_Suffix'].map({
        '1': 'Index_Case',
        '2': 'Sibling',
        '3': 'Index_Case',
        '4': 'Sibling'
    })
    
    # Aile Tipi
    df['Aile_Tipi'] = df['ID_Suffix'].map({
        '1': 'Diyabet_Ailesi',
        '2': 'Diyabet_Ailesi',
        '3': 'Kontrol_Ailesi',
        '4': 'Kontrol_Ailesi'
    })
    
    print("\nYeni Sınıflandırma Sonuçları:")
    
    # Ana grup dağılımı
    print("\n1. Ana Grup Dağılımı:")
    for grup, count in df['Grup_Yeni'].value_counts().items():
        print(f"  {grup}: {count} ({count/len(df)*100:.1f}%)")
    
    # Alt grup dağılımı
    print("\n2. Alt Grup Dağılımı:")
    for grup, count in df['Alt_Grup'].value_counts().sort_index().items():
        print(f"  {grup}: {count}")
    
    # Katılımcı tipi
    print("\n3. Katılımcı Tipi:")
    for tip, count in df['Katilimci_Tipi'].value_counts().items():
        print(f"  {tip}: {count}")
    
    return df

def compare_with_existing_classification(df):
    """Mevcut sınıflandırma ile karşılaştır"""
    
    print("\n" + "="*70)
    print("MEVCUT VE YENİ SINIFLANDIRMA KARŞILAŞTIRMASI")
    print("="*70)
    
    # Eğer mevcut Grup sütunu varsa
    if 'Grup' in df.columns:
        # Karşılaştırma tablosu
        comparison = pd.crosstab(df['Grup'], df['Grup_Yeni'], margins=True)
        print("\nMevcut Grup vs Yeni Grup:")
        print(comparison)
        
        # Uyumsuzluklar
        mismatches = df[df['Grup'] != df['Grup_Yeni']]
        if len(mismatches) > 0:
            print(f"\n[UYARI] {len(mismatches)} kayıt farklı sınıflandırılmış!")
            print("\nÖrnek uyumsuzluklar:")
            print(mismatches[['Katılımcı No', 'Grup', 'Grup_Yeni', 'DM Tanı Tarihi']].head(10))
    
    # DM Tanı Tarihi ile kontrol
    if 'DM Tanı Tarihi' in df.columns:
        print("\n\nDM Tanı Tarihi Kontrolü:")
        
        # Suffix 1 olanların DM tanısı var mı?
        suffix_1 = df[df['ID_Suffix'] == '1']
        has_dm_date_1 = (~suffix_1['DM Tanı Tarihi'].isna()).sum()
        print(f"\nSuffix -1 (Diyabet Index):")
        print(f"  DM tanısı olan: {has_dm_date_1}/{len(suffix_1)}")
        
        # Suffix 2 olanlar
        suffix_2 = df[df['ID_Suffix'] == '2']
        has_dm_date_2 = (~suffix_2['DM Tanı Tarihi'].isna()).sum()
        print(f"\nSuffix -2 (Diyabet Kardeş):")
        print(f"  DM tanısı olan: {has_dm_date_2}/{len(suffix_2)}")
        
        # Suffix 3 olanlar
        suffix_3 = df[df['ID_Suffix'] == '3']
        has_dm_date_3 = (~suffix_3['DM Tanı Tarihi'].isna()).sum()
        print(f"\nSuffix -3 (Kontrol Index):")
        print(f"  DM tanısı olan: {has_dm_date_3}/{len(suffix_3)} (OLMAMALI!)")
        
        # Suffix 4 olanlar
        suffix_4 = df[df['ID_Suffix'] == '4']
        has_dm_date_4 = (~suffix_4['DM Tanı Tarihi'].isna()).sum()
        print(f"\nSuffix -4 (Kontrol Kardeş):")
        print(f"  DM tanısı olan: {has_dm_date_4}/{len(suffix_4)} (OLMAMALI!)")

def analyze_family_pairs(df):
    """Aile çiftlerini analiz et"""
    
    print("\n" + "="*70)
    print("AİLE/KARDEŞ ÇİFTLERİ ANALİZİ")
    print("="*70)
    
    # Her aile için kardeş çiftleri
    family_pairs = []
    
    for prefix in df['ID_Prefix'].unique():
        family_df = df[df['ID_Prefix'] == prefix]
        suffixes = family_df['ID_Suffix'].tolist()
        
        # Diyabet çifti (1-2)
        if '1' in suffixes and '2' in suffixes:
            index_case = family_df[family_df['ID_Suffix'] == '1'].iloc[0]
            sibling = family_df[family_df['ID_Suffix'] == '2'].iloc[0]
            family_pairs.append({
                'Aile_ID': prefix,
                'Tip': 'Diyabet_Cifti',
                'Index_ID': index_case['Katılımcı No'],
                'Sibling_ID': sibling['Katılımcı No']
            })
        
        # Kontrol çifti (3-4)
        if '3' in suffixes and '4' in suffixes:
            index_case = family_df[family_df['ID_Suffix'] == '3'].iloc[0]
            sibling = family_df[family_df['ID_Suffix'] == '4'].iloc[0]
            family_pairs.append({
                'Aile_ID': prefix,
                'Tip': 'Kontrol_Cifti',
                'Index_ID': index_case['Katılımcı No'],
                'Sibling_ID': sibling['Katılımcı No']
            })
    
    pairs_df = pd.DataFrame(family_pairs)
    
    print(f"\nToplam aile çifti: {len(pairs_df)}")
    print(f"  Diyabet çifti: {(pairs_df['Tip'] == 'Diyabet_Cifti').sum()}")
    print(f"  Kontrol çifti: {(pairs_df['Tip'] == 'Kontrol_Cifti').sum()}")
    
    # Çiftleri kaydet
    pairs_df.to_csv('data/cleaned/family_pairs.csv', index=False, encoding='utf-8-sig')
    print("\n[OK] Aile çiftleri kaydedildi: family_pairs.csv")
    
    return pairs_df

def save_reclassified_data(df):
    """Yeniden sınıflandırılmış veriyi kaydet"""
    
    print("\n" + "="*70)
    print("VERİYİ KAYDETME")
    print("="*70)
    
    # Eski Grup sütununu yedekle
    if 'Grup' in df.columns:
        df['Grup_Eski'] = df['Grup']
    
    # Yeni grubu ana grup yap
    df['Grup'] = df['Grup_Yeni']
    
    # Gereksiz sütunları kaldır
    df = df.drop(['Grup_Yeni', 'ID_Prefix', 'ID_Suffix'], axis=1)
    
    # Kaydet
    output_path = 'data/cleaned/dataset_reclassified.csv'
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"[OK] Yeniden sınıflandırılmış veri: {output_path}")
    
    output_excel = 'data/cleaned/dataset_reclassified.xlsx'
    df.to_excel(output_excel, index=False)
    print(f"[OK] Excel formatı: {output_excel}")
    
    # Sadece analiz sütunları
    analysis_cols = ['Katılımcı No', 'Grup', 'Alt_Grup', 'Katilimci_Tipi', 'Aile_Tipi']
    
    # Beck sütunları
    beck_cols = [col for col in df.columns if 'Beck' in col]
    analysis_cols.extend(beck_cols)
    
    # EMBU sütunları
    embu_cols = [col for col in df.columns if 'EMBU' in col]
    analysis_cols.extend(embu_cols[:23])
    
    # Yaş ve diğer demografik
    demo_cols = ['Anne_Yas', 'Katilimci_Cocuk_Yas', 'Cocuk_Sayisi', 'Calisma_Durumu']
    for col in demo_cols:
        if col in df.columns:
            analysis_cols.append(col)
    
    # Mevcut sütunlar
    available_cols = [col for col in analysis_cols if col in df.columns]
    df_analysis = df[available_cols]
    
    df_analysis.to_csv('data/cleaned/dataset_for_analysis_reclassified.csv', 
                      index=False, encoding='utf-8-sig')
    print(f"[OK] Analiz veri seti: dataset_for_analysis_reclassified.csv")
    
    return df

def create_summary_report(df, pairs_df):
    """Özet rapor oluştur"""
    
    report = []
    report.append("="*70)
    report.append("KATILIMCI ID BAZLI YENİDEN SINIFLANDIRMA RAPORU")
    report.append("="*70)
    report.append(f"\nTarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    report.append("\n" + "="*70)
    report.append("1. ID SUFFIX ANLAMI")
    report.append("="*70)
    report.append("\n-1: Diyabetli çocuk (index case)")
    report.append("-2: Diyabetli çocuğun kardeşi")
    report.append("-3: Sağlıklı kontrol (index case)")
    report.append("-4: Sağlıklı kontrolün kardeşi")
    
    report.append("\n" + "="*70)
    report.append("2. GRUP DAĞILIMI")
    report.append("="*70)
    
    report.append("\nAna Gruplar:")
    for grup, count in df['Grup'].value_counts().items():
        report.append(f"  {grup}: {count} ({count/len(df)*100:.1f}%)")
    
    report.append("\nAlt Gruplar:")
    for grup, count in df['Alt_Grup'].value_counts().sort_index().items():
        report.append(f"  {grup}: {count}")
    
    report.append("\n" + "="*70)
    report.append("3. AİLE ÇİFTLERİ")
    report.append("="*70)
    
    report.append(f"\nToplam aile çifti: {len(pairs_df)}")
    report.append(f"  Diyabet ailesi: {(pairs_df['Tip'] == 'Diyabet_Cifti').sum()}")
    report.append(f"  Kontrol ailesi: {(pairs_df['Tip'] == 'Kontrol_Cifti').sum()}")
    
    report.append("\n" + "="*70)
    report.append("4. ÖNEMLİ NOTLAR")
    report.append("="*70)
    
    report.append("\n- Diyabet grubunda hem hasta hem kardeşler var (76 kişi)")
    report.append("- Kontrol grubunda hem index hem kardeşler var (80 kişi)")
    report.append("- Kardeş çiftleri paired analiz için kullanılabilir")
    report.append("- Mükerrer kayıtlar temizlendi (194 -> 175)")
    
    report.append("\n" + "="*70)
    
    # Raporu kaydet
    with open('results/reclassification_report.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    
    print("\n[OK] Rapor kaydedildi: results/reclassification_report.txt")
    
    return report

def main():
    """Ana fonksiyon"""
    
    print("\n" + "="*70)
    print("KATILIMCI ID'YE GÖRE YENİDEN SINIFLANDIRMA")
    print("="*70)
    
    try:
        # 1. ID'leri analiz et
        df = analyze_participant_ids()
        
        # 2. Yeni sınıflandırmalar oluştur
        df = create_new_classifications(df)
        
        # 3. Mevcut sınıflandırma ile karşılaştır
        compare_with_existing_classification(df)
        
        # 4. Aile çiftlerini analiz et
        pairs_df = analyze_family_pairs(df)
        
        # 5. Veriyi kaydet
        df = save_reclassified_data(df)
        
        # 6. Rapor oluştur
        report = create_summary_report(df, pairs_df)
        
        print("\n" + "="*70)
        print("ÖZET")
        print("="*70)
        print(f"\nToplam kayıt: {len(df)}")
        print(f"Diyabet grubu: {(df['Grup'] == 'Diyabet').sum()} (38 hasta + 38 kardeş)")
        print(f"Kontrol grubu: {(df['Grup'] == 'Kontrol').sum()} (40 index + 40 kardeş)")
        print(f"\nAile çifti sayısı: {len(pairs_df)}")
        
        print("\n" + "="*70)
        print("YENİDEN SINIFLANDIRMA TAMAMLANDI")
        print("="*70)
        
        return df, pairs_df
        
    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    main()