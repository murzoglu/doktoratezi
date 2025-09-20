"""
Ham Veri klasörünü incele ve içeriğini listele
"""

from google_drive_api import GoogleDriveAPI

def explore_ham_veri_folder():
    """
    Ham Veri klasörünün içeriğini detaylı inceler
    """
    # API istemcisini başlat
    drive = GoogleDriveAPI('dr-murzoglu-doktora.json')

    # Ham Veri klasörünün ID'si
    HAM_VERI_FOLDER_ID = "1knoOZrEBMbwR1D2S-_f0WM2pmO93g9WX"

    print("="*60)
    print("HAM VERI KLASORU ANALIZI")
    print("="*60)

    # Klasör bilgilerini al
    print("\n1. Klasor Bilgileri:")
    print("-"*40)
    folder_info = drive.get_file_info(HAM_VERI_FOLDER_ID)

    # Klasör içeriğini listele
    print("\n2. Klasor Icerigi:")
    print("-"*40)

    query = f"'{HAM_VERI_FOLDER_ID}' in parents and trashed = false"
    items = drive.list_files(query=query, page_size=100)

    if items:
        # Dosya türlerine göre grupla
        excel_files = []
        google_sheets = []
        other_files = []
        folders = []

        for item in items:
            mime_type = item.get('mimeType')
            if mime_type == 'application/vnd.google-apps.folder':
                folders.append(item)
            elif mime_type == 'application/vnd.google-apps.spreadsheet':
                google_sheets.append(item)
            elif 'sheet' in mime_type.lower() or 'excel' in mime_type.lower() or item['name'].endswith(('.xlsx', '.xls')):
                excel_files.append(item)
            else:
                other_files.append(item)

        # Google Sheets dosyalarını listele
        if google_sheets:
            print(f"\n[GOOGLE SHEETS] ({len(google_sheets)} adet):")
            for sheet in google_sheets:
                print(f"   - {sheet['name']}")
                print(f"     ID: {sheet['id']}")
                print(f"     Degistirilme: {sheet.get('modifiedTime', 'N/A')}")

        # Excel dosyalarını listele
        if excel_files:
            print(f"\n[EXCEL DOSYALARI] ({len(excel_files)} adet):")
            for excel in excel_files:
                size = excel.get('size', 'N/A')
                if size != 'N/A':
                    size_kb = int(size) / 1024
                    print(f"   - {excel['name']} ({size_kb:.2f} KB)")
                else:
                    print(f"   - {excel['name']}")
                print(f"     ID: {excel['id']}")

        # Alt klasörleri listele
        if folders:
            print(f"\n[ALT KLASORLER] ({len(folders)} adet):")
            for folder in folders:
                print(f"   - {folder['name']} (ID: {folder['id']})")

                # Alt klasör içeriğini de göster
                sub_query = f"'{folder['id']}' in parents and trashed = false"
                sub_items = drive.list_files(query=sub_query, page_size=5)
                if sub_items:
                    for sub_item in sub_items[:3]:
                        print(f"       * {sub_item['name']}")

        # Diğer dosyalar
        if other_files:
            print(f"\n[DIGER DOSYALAR] ({len(other_files)} adet):")
            for file in other_files:
                print(f"   - {file['name']}")
                print(f"     Tip: {file['mimeType']}")

        # Toplam özet
        print(f"\n[OZET]:")
        print(f"   Toplam: {len(items)} dosya/klasor")
        print(f"   Google Sheets: {len(google_sheets)}")
        print(f"   Excel: {len(excel_files)}")
        print(f"   Klasor: {len(folders)}")
        print(f"   Diger: {len(other_files)}")

        return items
    else:
        print("Ham Veri klasoru bos veya erisim yok.")
        return []

def download_sample_data():
    """
    Örnek veri dosyası indir
    """
    drive = GoogleDriveAPI('dr-murzoglu-doktora.json')
    HAM_VERI_FOLDER_ID = "1knoOZrEBMbwR1D2S-_f0WM2pmO93g9WX"

    # İlk Google Sheets dosyasını bul
    query = f"'{HAM_VERI_FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.spreadsheet' and trashed = false"
    sheets = drive.list_files(query=query, page_size=1)

    if sheets:
        sheet = sheets[0]
        print(f"\n[ORNEK VERI]: {sheet['name']}")
        print(f"   ID: {sheet['id']}")

        # Google Sheets'i okumak için sheets API kullan
        from google_sheets_api import GoogleSheetsAPI
        sheets_api = GoogleSheetsAPI('dr-murzoglu-doktora.json')

        # İlk 10 satırı oku
        try:
            data = sheets_api.read_range(sheet['id'], 'A1:Z10')
            if data:
                print("\n[ILK SATIRLAR]:")
                for i, row in enumerate(data[:5]):
                    print(f"   Satir {i+1}: {row[:5]}...")  # İlk 5 sütunu göster
        except Exception as e:
            print(f"   Okuma hatasi: {e}")

if __name__ == "__main__":
    try:
        # Ham veri klasörünü incele
        items = explore_ham_veri_folder()

        # Örnek veri indir
        if items:
            print("\n" + "="*60)
            download_sample_data()

        print("\n" + "="*60)
        print("[TAMAMLANDI] Ham veri klasoru analizi bitti!")
        print("="*60)

    except Exception as e:
        print(f"\n[HATA]: {e}")
        print("\nCozum onerileri:")
        print("1. Service account'a Ham Veri klasoru icin erisim izni verin")
        print("2. Google Sheets API'nin aktif oldugunu kontrol edin")