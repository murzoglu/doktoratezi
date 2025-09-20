"""
Grup değişkenini düzelt ve veriyi güncelle
"""

import pandas as pd
import numpy as np
import os

def fix_groups():
    """Grup değişkenini düzelt"""

    print("="*60)
    print("GRUP DEĞİŞKENİ DÜZELTME")
    print("="*60)

    # Ham veriyi yükle (orijinal Google Sheets verisi)
    print("\n[1] Ham veri yükleniyor...")
    df_raw = pd.read_csv('data/raw/main_dataset.csv')
    print(f"Ham veri: {df_raw.shape[0]} satır x {df_raw.shape[1]} sütun")

    # DM Tanı Tarihi sütununu kontrol et
    if 'DM Tanı Tarihi' in df_raw.columns:
        print("\n[2] DM Tanı Tarihi sütunu analizi:")

        dm_dates = df_raw['DM Tanı Tarihi']

        # Değerleri göster
        print("\nDM Tanı Tarihi değer dağılımı:")
        value_counts = dm_dates.value_counts(dropna=False).head(20)
        for val, count in value_counts.items():
            print(f"  {val}: {count}")

        # Boş olmayanları say
        has_dm_date = 0
        no_dm_date = 0

        for val in dm_dates:
            # Değeri string'e çevir ve kontrol et
            val_str = str(val).strip()

            # Boş değerler: NaN, nan, boş string, None
            if val_str in ['nan', 'NaN', '', 'None', 'null'] or pd.isna(val):
                no_dm_date += 1
            else:
                has_dm_date += 1

        print(f"\nDM tanı tarihi OLAN (Diyabet): {has_dm_date}")
        print(f"DM tanı tarihi OLMAYAN (Kontrol): {no_dm_date}")

        # Grup değişkeni oluştur
        def assign_group(val):
            val_str = str(val).strip()
            if val_str in ['nan', 'NaN', '', 'None', 'null'] or pd.isna(val):
                return 'Kontrol'
            else:
                return 'Diyabet'

        df_raw['Grup'] = dm_dates.apply(assign_group)

        # Grup dağılımını kontrol et
        print("\n[3] Yeni grup dağılımı:")
        for grup, count in df_raw['Grup'].value_counts().items():
            print(f"  {grup}: {count} ({count/len(df_raw)*100:.1f}%)")

    # Katılımcı numaralarını da kontrol et
    if 'Katılımcı No' in df_raw.columns:
        print("\n[4] Katılımcı numaraları analizi:")
        participant_nos = df_raw['Katılımcı No'].astype(str)

        # D ile başlayanlar
        d_participants = participant_nos.str.upper().str.startswith('D')
        k_participants = participant_nos.str.upper().str.startswith('K')

        d_count = d_participants.sum()
        k_count = k_participants.sum()

        print(f"  D ile başlayan: {d_count} (muhtemelen Diyabet)")
        print(f"  K ile başlayan: {k_count} (muhtemelen Kontrol)")

        # Eğer D/K prefixi varsa bunu da kontrol edelim
        if d_count > 0 or k_count > 0:
            print("\n[5] Katılımcı numarası ile grup uyumu kontrolü:")

            # D ile başlayanların grup dağılımı
            if d_count > 0:
                d_groups = df_raw[d_participants]['Grup'].value_counts()
                print(f"\nD ile başlayanların grup dağılımı:")
                for grup, count in d_groups.items():
                    print(f"  {grup}: {count}")

            # K ile başlayanların grup dağılımı
            if k_count > 0:
                k_groups = df_raw[k_participants]['Grup'].value_counts()
                print(f"\nK ile başlayanların grup dağılımı:")
                for grup, count in k_groups.items():
                    print(f"  {grup}: {count}")

            # Eğer katılımcı numarası daha güvenilirse onu kullan
            if d_count > 10 and k_count > 10:
                print("\n[!] Katılımcı numarası bazlı grup ataması yapılıyor...")

                def assign_group_by_id(row):
                    participant_no = str(row['Katılımcı No']).upper()
                    if participant_no.startswith('D'):
                        return 'Diyabet'
                    elif participant_no.startswith('K'):
                        return 'Kontrol'
                    else:
                        # DM Tanı Tarihi'ne bak
                        return assign_group(row['DM Tanı Tarihi'])

                df_raw['Grup'] = df_raw.apply(assign_group_by_id, axis=1)

                print("\nGüncellenmiş grup dağılımı:")
                for grup, count in df_raw['Grup'].value_counts().items():
                    print(f"  {grup}: {count} ({count/len(df_raw)*100:.1f}%)")

    # Güncellenmiş veriyi kaydet
    print("\n[6] Güncellenmiş veri kaydediliyor...")

    # Raw veriyi güncelle
    df_raw.to_csv('data/raw/main_dataset_with_groups.csv', index=False, encoding='utf-8-sig')
    print("[OK] data/raw/main_dataset_with_groups.csv")

    # Temizlenmiş veriyi de güncelle
    if os.path.exists('data/cleaned/cleaned_dataset.csv'):
        df_clean = pd.read_csv('data/cleaned/cleaned_dataset.csv')

        # Grup sütununu ekle/güncelle
        df_clean['Grup'] = df_raw['Grup'].values[:len(df_clean)]

        # Kaydet
        df_clean.to_csv('data/cleaned/cleaned_dataset.csv', index=False, encoding='utf-8-sig')
        df_clean.to_excel('data/cleaned/cleaned_dataset.xlsx', index=False)
        print("[OK] data/cleaned/cleaned_dataset.csv (güncellendi)")
        print("[OK] data/cleaned/cleaned_dataset.xlsx (güncellendi)")

    # Grup bilgi raporu
    with open('data/cleaned/group_info.txt', 'w', encoding='utf-8') as f:
        f.write("GRUP BİLGİLERİ\n")
        f.write("="*60 + "\n\n")
        f.write("Grup Belirleme Yöntemi:\n")
        f.write("- DM Tanı Tarihi OLAN → Diyabet Grubu\n")
        f.write("- DM Tanı Tarihi OLMAYAN → Kontrol Grubu\n")

        if 'Katılımcı No' in df_raw.columns and (d_count > 10 or k_count > 10):
            f.write("\nKatılımcı Numarası Kontrolü:\n")
            f.write(f"- D ile başlayan: {d_count} katılımcı\n")
            f.write(f"- K ile başlayan: {k_count} katılımcı\n")

        f.write(f"\nFinal Grup Dağılımı:\n")
        for grup, count in df_raw['Grup'].value_counts().items():
            f.write(f"- {grup}: {count} ({count/len(df_raw)*100:.1f}%)\n")

    print("[OK] data/cleaned/group_info.txt")

    return df_raw

def main():
    """Ana fonksiyon"""

    try:
        df = fix_groups()

        print("\n" + "="*60)
        print("GRUP DEĞİŞKENİ DÜZELTİLDİ!")
        print("="*60)

        if 'Grup' in df.columns:
            print("\nFinal grup dağılımı:")
            for grup, count in df['Grup'].value_counts().items():
                print(f"  {grup}: {count} kişi")

            # Protokoldeki beklenen sayılarla karşılaştır
            print("\nProtokol ile karşılaştırma:")
            print("  Beklenen: ~100 Diyabet, ~95 Kontrol")
            print(f"  Gerçekleşen: {df['Grup'].value_counts().to_dict()}")

    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()