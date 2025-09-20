"""
Google Sheets'ten grup bilgilerini analiz et
"""

import sys
import os
import pandas as pd
import numpy as np

# Ana dizini path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from google_sheets_api import GoogleSheetsAPI

def analyze_sheet_structure():
    """Google Sheets'in yapısını analiz et"""

    print("="*60)
    print("GOOGLE SHEETS GRUP ANALİZİ")
    print("="*60)

    # Google Sheets API başlat
    sheets = GoogleSheetsAPI('dr-murzoglu-doktora.json')

    # Ana veri tablosu ID'si
    SHEET_ID = "1AIeTlphqgSLy8ESwa5lblhSgH_ZbHTvX8RafW3vshG8"

    try:
        # Önce sheet'teki ilk 10 satırı inceleyelim
        print("\n[1] İlk 10 satırı inceliyorum...")
        sample_data = sheets.read_range(SHEET_ID, 'A1:Z10')

        if sample_data:
            print(f"İlk {len(sample_data)} satır okundu")

            # Başlıkları göster
            headers = sample_data[0] if sample_data else []
            print(f"\nBaşlıklar ({len(headers)} sütun):")
            for i, header in enumerate(headers[:26]):  # İlk 26 sütun (A-Z)
                print(f"  {chr(65+i)}: {header}")

        # Sheet'teki tüm sayfaları kontrol et
        print("\n[2] Sheet'teki tüm sayfaları kontrol ediyorum...")

        # Farklı sheet/tab'ları kontrol et
        service = sheets.sheets_service
        spreadsheet = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
        sheets_list = spreadsheet.get('sheets', [])

        print(f"\nToplam {len(sheets_list)} sayfa bulundu:")
        for sheet in sheets_list:
            props = sheet.get('properties', {})
            title = props.get('title', 'Unknown')
            sheet_id = props.get('sheetId', 'Unknown')
            grid_props = props.get('gridProperties', {})
            rows = grid_props.get('rowCount', 0)
            cols = grid_props.get('columnCount', 0)

            print(f"\nSayfa: {title}")
            print(f"  ID: {sheet_id}")
            print(f"  Boyut: {rows} satır x {cols} sütun")

            # Her sayfadan örnek veri al
            if title != "Sayfa1":  # Ana sayfa değilse
                try:
                    sample = sheets.read_range(SHEET_ID, f'{title}!A1:E5')
                    if sample:
                        print(f"  İlk birkaç satır:")
                        for row in sample[:3]:
                            print(f"    {row[:5]}")  # İlk 5 sütun
                except:
                    print(f"  [!] Bu sayfadan veri okunamadı")

        # Tüm veriyi yükle ve grupları analiz et
        print("\n[3] Tüm veriyi yükleyip grup bilgilerini analiz ediyorum...")
        df = sheets.sheets_to_dataframe(SHEET_ID, 'A:BZ', header=True)

        print(f"\nToplam veri: {df.shape[0]} satır x {df.shape[1]} sütun")

        # Potansiyel grup sütunlarını ara
        print("\n[4] Potansiyel grup sütunları:")
        potential_group_cols = []

        for col in df.columns:
            # Grup, Diyabet, Kontrol, DM gibi kelimeler içeren sütunlar
            if any(word in str(col).lower() for word in ['grup', 'group', 'diyabet', 'dm', 'kontrol', 'hasta', 'tip']):
                potential_group_cols.append(col)
                print(f"\n  {col}:")
                value_counts = df[col].value_counts(dropna=False)
                for val, count in value_counts.head(10).items():
                    print(f"    {val}: {count}")

        # Katılımcı numaralarını analiz et
        if 'Katılımcı No' in df.columns:
            print("\n[5] Katılımcı numaralarını analiz ediyorum...")
            participant_nos = df['Katılımcı No'].dropna()
            print(f"Benzersiz katılımcı sayısı: {participant_nos.nunique()}")

            # Numara formatlarını kontrol et
            sample_nos = participant_nos.head(20).tolist()
            print("\nİlk 20 katılımcı numarası:")
            for no in sample_nos:
                print(f"  {no}")

            # Numara desenlerini analiz et
            print("\nNumara desenleri:")
            # D ile başlayanlar (Diyabet?)
            d_count = sum(1 for no in participant_nos if str(no).upper().startswith('D'))
            # K ile başlayanlar (Kontrol?)
            k_count = sum(1 for no in participant_nos if str(no).upper().startswith('K'))
            # Sayı ile başlayanlar
            num_count = sum(1 for no in participant_nos if str(no)[0].isdigit())

            print(f"  D ile başlayan: {d_count}")
            print(f"  K ile başlayan: {k_count}")
            print(f"  Sayı ile başlayan: {num_count}")
            print(f"  Diğer: {len(participant_nos) - d_count - k_count - num_count}")

        # DM Tanı Tarihi analizi
        if 'DM Tanı Tarihi' in df.columns:
            print("\n[6] DM Tanı Tarihi analizi:")
            dm_dates = df['DM Tanı Tarihi']
            has_dm_date = dm_dates.notna().sum()
            no_dm_date = dm_dates.isna().sum()

            print(f"  DM tanı tarihi olan: {has_dm_date}")
            print(f"  DM tanı tarihi olmayan: {no_dm_date}")

            # Bunları grup olarak kullan
            df['Grup_Tahmini'] = df['DM Tanı Tarihi'].apply(
                lambda x: 'Diyabet' if pd.notna(x) and str(x).strip() not in ['', '0', 'nan']
                else 'Kontrol'
            )

            print("\nTahmini grup dağılımı:")
            print(df['Grup_Tahmini'].value_counts())

        # Sonuçları kaydet
        print("\n[7] Analiz sonuçlarını kaydediyorum...")

        # Grup bilgili veriyi kaydet
        df.to_csv('data/raw/data_with_group_analysis.csv', index=False, encoding='utf-8-sig')
        print("[OK] data/raw/data_with_group_analysis.csv")

        # Analiz raporunu kaydet
        with open('data/raw/group_analysis_report.txt', 'w', encoding='utf-8') as f:
            f.write("GRUP ANALİZ RAPORU\n")
            f.write("="*60 + "\n\n")

            if 'Grup_Tahmini' in df.columns:
                f.write("Grup Dağılımı (DM Tanı Tarihine Göre):\n")
                for grup, count in df['Grup_Tahmini'].value_counts().items():
                    f.write(f"  {grup}: {count} ({count/len(df)*100:.1f}%)\n")

            f.write(f"\nToplam Katılımcı: {len(df)}\n")

            if potential_group_cols:
                f.write(f"\nPotansiyel Grup Sütunları:\n")
                for col in potential_group_cols:
                    f.write(f"  - {col}\n")

        print("[OK] data/raw/group_analysis_report.txt")

        return df

    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Ana fonksiyon"""

    # Sheet yapısını analiz et
    df = analyze_sheet_structure()

    if df is not None:
        print("\n" + "="*60)
        print("ANALİZ TAMAMLANDI!")
        print("="*60)

        if 'Grup_Tahmini' in df.columns:
            print("\nGrup belirleme önerisi:")
            print("DM Tanı Tarihi olan katılımcılar → Diyabet Grubu")
            print("DM Tanı Tarihi olmayan katılımcılar → Kontrol Grubu")

            print("\nBu gruplamayı kullanmak için veri temizleme scriptini güncelleyin.")

    return df

if __name__ == "__main__":
    df = main()