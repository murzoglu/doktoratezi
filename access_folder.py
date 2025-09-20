"""
Belirli bir Google Drive klasörüne erişim sağlama
"""

from google_drive_api import GoogleDriveAPI

def access_specific_folder(folder_id):
    """
    Belirli bir klasöre erişim sağlar ve içeriğini listeler

    Args:
        folder_id: Google Drive klasör ID'si
    """
    # API istemcisini başlat
    drive = GoogleDriveAPI('dr-murzoglu-doktora.json')

    print("="*60)
    print(f"KLASÖR ERİŞİMİ: {folder_id}")
    print("="*60)

    # 1. Klasör bilgilerini al
    print("\n1. Klasör Bilgileri:")
    print("-"*40)
    folder_info = drive.get_file_info(folder_id)

    if folder_info:
        print(f"\nKlasör Adı: {folder_info.get('name')}")
        print(f"Klasör ID: {folder_info.get('id')}")
        print(f"Web Link: {folder_info.get('webViewLink')}")

    # 2. Klasör içeriğini listele
    print("\n2. Klasör İçeriği:")
    print("-"*40)

    # Klasördeki tüm dosya ve alt klasörleri listele
    query = f"'{folder_id}' in parents and trashed = false"
    items = drive.list_files(query=query, page_size=100)

    # Dosyaları ve klasörleri ayır
    folders = []
    files = []

    if items:
        for item in items:
            if item.get('mimeType') == 'application/vnd.google-apps.folder':
                folders.append(item)
            else:
                files.append(item)

        # Klasörleri listele
        if folders:
            print(f"\n[KLASORLER] ({len(folders)} adet):")
            for folder in folders:
                print(f"   - {folder['name']} (ID: {folder['id']})")

        # Dosyaları listele
        if files:
            print(f"\n[DOSYALAR] ({len(files)} adet):")
            for file in files:
                size = file.get('size', 'N/A')
                if size != 'N/A':
                    size_mb = int(size) / (1024 * 1024)
                    size_str = f"{size_mb:.2f} MB"
                else:
                    size_str = "N/A"

                print(f"   - {file['name']}")
                print(f"      - ID: {file['id']}")
                print(f"      - Tip: {file['mimeType']}")
                print(f"      - Boyut: {size_str}")
                print(f"      - Degistirilme: {file.get('modifiedTime', 'N/A')}")
    else:
        print("Klasör boş veya erişim yok.")

    # 3. Alt klasörleri de tara (isteğe bağlı)
    print("\n3. Alt Klasorlerin Icerigi:")
    print("-"*40)

    if folders:
        for subfolder in folders[:3]:  # İlk 3 alt klasörü göster
            print(f"\n[{subfolder['name']}] icerigi:")
            sub_query = f"'{subfolder['id']}' in parents and trashed = false"
            sub_items = drive.list_files(query=sub_query, page_size=10)

            if sub_items:
                for item in sub_items[:5]:  # Her alt klasörden max 5 dosya göster
                    if item.get('mimeType') == 'application/vnd.google-apps.folder':
                        print(f"     [KLASOR] {item['name']}")
                    else:
                        print(f"     [DOSYA] {item['name']}")
            else:
                print("     (Bos klasor)")

    return items

def download_file_from_folder(folder_id, file_name_pattern=None):
    """
    Klasörden dosya indir

    Args:
        folder_id: Klasör ID'si
        file_name_pattern: İndirilecek dosya adı veya pattern
    """
    drive = GoogleDriveAPI('dr-murzoglu-doktora.json')

    query = f"'{folder_id}' in parents and trashed = false"
    if file_name_pattern:
        query += f" and name contains '{file_name_pattern}'"

    files = drive.list_files(query=query, page_size=10)

    if files:
        print(f"\n[INDIRILEBILECEK DOSYALAR]:")
        for i, file in enumerate(files):
            print(f"{i+1}. {file['name']} (ID: {file['id']})")

        # İlk dosyayı örnek olarak indir
        if len(files) > 0:
            file_to_download = files[0]
            print(f"\n'{file_to_download['name']}' indiriliyor...")
            success = drive.download_file(
                file_to_download['id'],
                f"downloaded_{file_to_download['name']}"
            )
            if success:
                print("[BASARILI] Indirme tamamlandi!")
    else:
        print("İndirilecek dosya bulunamadı.")

if __name__ == "__main__":
    # Verilen klasör ID'si
    FOLDER_ID = "1C8vsNG-kVbYmL3tCG_lYuyUvYElSCTvs"

    try:
        # Klasöre erişim sağla ve içeriğini listele
        items = access_specific_folder(FOLDER_ID)

        # İsteğe bağlı: Belirli bir dosyayı indir
        # download_file_from_folder(FOLDER_ID, "example")

        print("\n" + "="*60)
        print("[BASARILI] Klasore basariyla erisildi!")
        print("="*60)

    except Exception as e:
        print(f"\n[HATA] Hata olustu: {e}")
        print("\nOlasi cozumler:")
        print("1. Service account email'ini klasore ekleyin:")
        print("   Email: doktora@dr-murzoglu.iam.gserviceaccount.com")
        print("2. Google Drive'da klasoru sag tiklayip 'Paylas' secin")
        print("3. Service account email'ini 'Goruntuleyici' veya 'Duzenleyici' olarak ekleyin")
        print("4. Drive API'nin etkinlestirildiginden emin olun")