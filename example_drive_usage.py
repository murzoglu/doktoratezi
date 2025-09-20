"""
Google Drive API kullanım örnekleri

Bu script Google Drive API'nin temel işlevlerini gösterir.
"""

from google_drive_api import GoogleDriveAPI

def main():
    # Google Drive API istemcisini başlat
    drive = GoogleDriveAPI('dr-murzoglu-doktora.json')

    print("="*50)
    print("GOOGLE DRIVE API ÖRNEKLERİ")
    print("="*50)

    # 1. Dosyaları listele
    print("\n1. Drive'daki dosyaları listeleme:")
    print("-"*30)
    files = drive.list_files(page_size=5)

    # 2. Klasör oluştur
    print("\n2. Yeni klasör oluşturma:")
    print("-"*30)
    folder_id = drive.create_folder("Doktora Tezi Verileri")

    # 3. Dosya yükleme örneği
    print("\n3. Dosya yükleme:")
    print("-"*30)
    print("Not: Yüklemek için bir dosya oluşturalım")
    with open("test_file.txt", "w", encoding="utf-8") as f:
        f.write("Bu bir test dosyasıdır.\nDoktora tezi için örnek veri.")

    file_id = drive.upload_file("test_file.txt", parent_folder_id=folder_id)

    # 4. Dosya bilgilerini alma
    if file_id:
        print("\n4. Dosya bilgilerini alma:")
        print("-"*30)
        file_info = drive.get_file_info(file_id)

    # 5. Dosya indirme
    if file_id:
        print("\n5. Dosya indirme:")
        print("-"*30)
        drive.download_file(file_id, "downloaded_test_file.txt")

    # 6. Dosya paylaşma (email adresi gerekli)
    # NOT: Gerçek bir email adresi kullanın
    # print("\n6. Dosya paylaşma:")
    # print("-"*30)
    # drive.share_file(file_id, "example@email.com", role="reader")

    # 7. Arama örneği - sadece klasörleri listele
    print("\n7. Sadece klasörleri arama:")
    print("-"*30)
    folders = drive.list_files(
        query="mimeType='application/vnd.google-apps.folder'",
        page_size=5
    )

    # 8. Belirli bir klasördeki dosyaları listele
    if folder_id:
        print("\n8. Belirli klasördeki dosyaları listeleme:")
        print("-"*30)
        files_in_folder = drive.list_files(
            query=f"'{folder_id}' in parents",
            page_size=10
        )

    # Temizlik - test dosyalarını sil (opsiyonel)
    import os
    if os.path.exists("test_file.txt"):
        os.remove("test_file.txt")
    if os.path.exists("downloaded_test_file.txt"):
        os.remove("downloaded_test_file.txt")

    print("\n" + "="*50)
    print("Örnekler tamamlandı!")
    print("="*50)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nHata oluştu: {e}")
        print("\nOlası sebepler:")
        print("1. Service account dosyası (dr-murzoglu-doktora.json) bulunamadı")
        print("2. Google Drive API etkinleştirilmemiş olabilir")
        print("3. Service account'un Drive erişim izni olmayabilir")
        print("\nÇözüm:")
        print("1. Google Cloud Console'da Drive API'yi etkinleştirin")
        print("2. Service account'a gerekli izinleri verin")
        print("3. Paylaşılan bir Drive kullanıyorsanız, service account email'ini ekleyin")