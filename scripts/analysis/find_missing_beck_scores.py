"""
Ham veri dosyalarından eksik Beck skorlarını bul ve birleştir
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_all_raw_data():
    """Tüm ham veri dosyalarını yükle"""

    print("="*70)
    print("HAM VERİ DOSYALARINI YÜKLEME")
    print("="*70)

    data_files = {
        'main_dataset': 'data/raw/main_dataset.csv',
        'main_with_groups': 'data/raw/main_dataset_with_groups.csv',
        'dm_cocuk_embu': 'data/raw/DM_Cocuk_EMBU.xlsx',
        'spss_data': 'data/raw/spss_20012025.xlsx',
        'cleaned_reclassified': 'data/cleaned/dataset_reclassified.csv'
    }

    datasets = {}

    for name, path in data_files.items():
        try:
            if path.endswith('.xlsx'):
                df = pd.read_excel(path)
            else:
                df = pd.read_csv(path)

            datasets[name] = df
            print(f"\n{name}:")
            print(f"  Satır sayısı: {len(df)}")
            print(f"  Sütun sayısı: {len(df.columns)}")

            # Beck sütunlarını kontrol et
            beck_cols = [col for col in df.columns if 'Beck' in str(col) or 'beck' in str(col)]
            if beck_cols:
                print(f"  Beck sütunları: {len(beck_cols)} adet")
                print(f"    İlk 5: {beck_cols[:5]}")

        except Exception as e:
            print(f"  [HATA] {name} yüklenemedi: {e}")

    return datasets

def analyze_beck_completeness(datasets):
    """Her veri setindeki Beck skorlarının tamlığını analiz et"""

    print("\n" + "="*70)
    print("BECK SKORLARI TAMLIK ANALİZİ")
    print("="*70)

    beck_analysis = {}

    for name, df in datasets.items():
        print(f"\n{name}:")

        # Beck sütunlarını bul
        beck_cols = [col for col in df.columns if 'Beck' in str(col) or 'beck' in str(col)]

        if not beck_cols:
            print("  Beck sütunu yok")
            continue

        # Beck toplam sütununu bul
        beck_total_cols = [col for col in beck_cols if 'Toplam' in str(col) or 'Total' in str(col) or 'total' in str(col)]

        if beck_total_cols:
            beck_total = beck_total_cols[0]
            non_null = df[beck_total].notna().sum()
            total = len(df)
            print(f"  Beck Toplam sütunu: {beck_total}")
            print(f"  Dolu kayıt: {non_null}/{total} ({non_null/total*100:.1f}%)")

            # Eksik olan katılımcıları bul
            if 'Katılımcı No' in df.columns or 'Katilimci_No' in df.columns:
                id_col = 'Katılımcı No' if 'Katılımcı No' in df.columns else 'Katilimci_No'
                missing_ids = df[df[beck_total].isna()][id_col].tolist()
                if missing_ids:
                    print(f"  Eksik olan ID'ler (ilk 10): {missing_ids[:10]}")

            beck_analysis[name] = {
                'total_col': beck_total,
                'completeness': non_null/total,
                'non_null': non_null,
                'total': total
            }

        # Beck maddeleri kontrolü
        beck_items = [col for col in beck_cols if any(str(i) in str(col) for i in range(1, 22))]
        if beck_items:
            print(f"  Beck madde sayısı: {len(beck_items)}")
            # Her maddedeki tamlık
            items_completeness = df[beck_items].notna().mean()
            print(f"  Maddelerin ortalama tamlığı: {items_completeness.mean()*100:.1f}%")

    return beck_analysis

def find_complementary_scores(datasets):
    """Farklı veri setlerindeki tamamlayıcı Beck skorlarını bul"""

    print("\n" + "="*70)
    print("TAMAMLAYICI BECK SKORLARINI BULMA")
    print("="*70)

    # Katılımcı ID'lerine göre Beck skorlarını topla
    all_beck_scores = {}

    for name, df in datasets.items():
        # ID sütununu bul
        id_cols = ['Katılımcı No', 'Katilimci_No', 'Katilimci No', 'ID', 'id']
        id_col = None
        for col in id_cols:
            if col in df.columns:
                id_col = col
                break

        if not id_col:
            print(f"\n{name}: ID sütunu bulunamadı")
            continue

        # Beck toplam sütununu bul
        beck_total_cols = [col for col in df.columns if 'Beck' in str(col) and ('Toplam' in str(col) or 'Total' in str(col))]

        if not beck_total_cols:
            continue

        beck_total = beck_total_cols[0]

        # Her katılımcının Beck skorunu kaydet
        for idx, row in df.iterrows():
            participant_id = str(row[id_col])
            beck_score = row[beck_total]

            if pd.notna(beck_score):
                if participant_id not in all_beck_scores:
                    all_beck_scores[participant_id] = {}
                all_beck_scores[participant_id][name] = beck_score

    # Çakışmaları ve tamamlayıcıları analiz et
    print(f"\nToplam {len(all_beck_scores)} farklı katılımcı için Beck skoru bulundu")

    # Birden fazla kaynakta olan katılımcılar
    multiple_sources = {pid: sources for pid, sources in all_beck_scores.items() if len(sources) > 1}
    print(f"\nBirden fazla kaynakta Beck skoru olan: {len(multiple_sources)} katılımcı")

    if multiple_sources:
        print("\nÖrnek çakışmalar (ilk 5):")
        for pid, sources in list(multiple_sources.items())[:5]:
            print(f"  {pid}: {sources}")

    return all_beck_scores

def merge_beck_scores(datasets, all_beck_scores):
    """Eksik Beck skorlarını birleştir"""

    print("\n" + "="*70)
    print("BECK SKORLARINI BİRLEŞTİRME")
    print("="*70)

    # Ana veri setini al (cleaned_reclassified)
    main_df = datasets.get('cleaned_reclassified')

    if main_df is None:
        print("[HATA] Ana veri seti bulunamadı")
        return None

    main_df = main_df.copy()

    # Eksik Beck skorlarını doldur
    filled_count = 0

    # ID sütununu bul
    id_col = 'Katilimci_No' if 'Katilimci_No' in main_df.columns else 'Katılımcı No'

    # Beck toplam sütununu bul veya oluştur
    beck_total_col = None
    for col in main_df.columns:
        if 'Beck' in str(col) and 'Toplam' in str(col):
            beck_total_col = col
            break

    if beck_total_col is None:
        beck_total_col = 'Beck_Toplam_Merged'
        main_df[beck_total_col] = np.nan

    print(f"\nAna veri setindeki Beck toplam sütunu: {beck_total_col}")
    initial_missing = main_df[beck_total_col].isna().sum()
    print(f"Başlangıçta eksik: {initial_missing}/{len(main_df)}")

    # Her satır için Beck skorunu kontrol et ve doldur
    for idx, row in main_df.iterrows():
        participant_id = str(row[id_col])
        current_beck = row[beck_total_col]

        # Eğer Beck skoru eksikse ve başka kaynakta varsa
        if pd.isna(current_beck) and participant_id in all_beck_scores:
            # İlk bulduğu kaynaktan al
            sources = all_beck_scores[participant_id]
            if sources:
                new_score = list(sources.values())[0]
                main_df.at[idx, beck_total_col] = new_score
                filled_count += 1
                source_name = list(sources.keys())[0]
                print(f"  {participant_id}: {new_score} ({source_name} kaynağından)")

    final_missing = main_df[beck_total_col].isna().sum()
    print(f"\nDoldurma sonrası eksik: {final_missing}/{len(main_df)}")
    print(f"Doldurulan kayıt: {filled_count}")

    # Beck maddelerini de kontrol et
    beck_items = [col for col in main_df.columns if 'Beck' in str(col) and any(str(i) in str(col) for i in range(1, 22))]
    if beck_items:
        # Eğer maddeler varsa toplamı yeniden hesapla
        print(f"\n{len(beck_items)} Beck maddesi bulundu, toplam yeniden hesaplanıyor...")
        # Önce numeric'e çevir
        for col in beck_items:
            main_df[col] = pd.to_numeric(main_df[col], errors='coerce')
        main_df['Beck_Calculated_New'] = main_df[beck_items].sum(axis=1)

        # Hesaplanan ile mevcut toplamı karşılaştır
        comparison = main_df[[beck_total_col, 'Beck_Calculated_New']].copy()
        comparison['Difference'] = comparison[beck_total_col] - comparison['Beck_Calculated_New']

        # Büyük farklar var mı?
        large_diffs = comparison[abs(comparison['Difference']) > 2].dropna()
        if len(large_diffs) > 0:
            print(f"\n[UYARI] {len(large_diffs)} kayıtta toplam ile hesaplanan arasında >2 fark var")

    return main_df

def save_merged_data(df):
    """Birleştirilmiş veriyi kaydet"""

    print("\n" + "="*70)
    print("VERİYİ KAYDETME")
    print("="*70)

    # CSV olarak kaydet
    output_path = 'data/cleaned/dataset_with_merged_beck.csv'
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"[OK] Birleştirilmiş veri kaydedildi: {output_path}")

    # Excel olarak da kaydet
    excel_path = 'data/cleaned/dataset_with_merged_beck.xlsx'
    df.to_excel(excel_path, index=False)
    print(f"[OK] Excel formatında kaydedildi: {excel_path}")

    # Özet istatistikler
    print("\nÖzet İstatistikler:")
    print(f"  Toplam kayıt: {len(df)}")

    # Beck tamlığı
    beck_cols = [col for col in df.columns if 'Beck' in str(col) and ('Toplam' in str(col) or 'Calculated' in str(col))]
    for col in beck_cols:
        non_null = df[col].notna().sum()
        print(f"  {col}: {non_null}/{len(df)} dolu ({non_null/len(df)*100:.1f}%)")

    return output_path

def main():
    """Ana fonksiyon"""

    print("\n" + "="*70)
    print("EKSİK BECK SKORLARINI BULMA VE BİRLEŞTİRME")
    print("="*70)

    try:
        # 1. Tüm ham veri dosyalarını yükle
        datasets = load_all_raw_data()

        # 2. Beck skorlarının tamlığını analiz et
        beck_analysis = analyze_beck_completeness(datasets)

        # 3. Tamamlayıcı skorları bul
        all_beck_scores = find_complementary_scores(datasets)

        # 4. Skorları birleştir
        merged_df = merge_beck_scores(datasets, all_beck_scores)

        if merged_df is not None:
            # 5. Veriyi kaydet
            output_path = save_merged_data(merged_df)

            print("\n" + "="*70)
            print("İŞLEM TAMAMLANDI")
            print("="*70)

            return merged_df, output_path

    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    main()