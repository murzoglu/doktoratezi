from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import os
import io

class GoogleDriveAPI:
    def __init__(self, credentials_file='dr-murzoglu-doktora.json'):
        """
        Google Drive API istemcisini başlatır

        Args:
            credentials_file: Service account JSON dosyasının yolu
        """
        self.SCOPES = ['https://www.googleapis.com/auth/drive']

        # Service account kimlik bilgilerini yükle
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_file,
            scopes=self.SCOPES
        )

        # Drive servisini oluştur
        self.service = build('drive', 'v3', credentials=self.credentials)

    def list_files(self, query=None, page_size=10):
        """
        Drive'daki dosyaları listeler

        Args:
            query: Drive API arama sorgusu (opsiyonel)
            page_size: Sayfa başına döndürülecek dosya sayısı

        Returns:
            Dosya listesi
        """
        try:
            results = self.service.files().list(
                q=query,
                pageSize=page_size,
                fields="nextPageToken, files(id, name, mimeType, modifiedTime, size)"
            ).execute()

            items = results.get('files', [])

            if not items:
                print('Dosya bulunamadı.')
                return []
            else:
                print(f'{len(items)} dosya bulundu:')
                for item in items:
                    print(f"  - {item['name']} (ID: {item['id']})")
                return items

        except Exception as error:
            print(f'Hata oluştu: {error}')
            return []

    def upload_file(self, file_path, parent_folder_id=None):
        """
        Dosya yükler

        Args:
            file_path: Yüklenecek dosyanın yolu
            parent_folder_id: Hedef klasörün ID'si (opsiyonel)

        Returns:
            Yüklenen dosyanın ID'si
        """
        try:
            file_name = os.path.basename(file_path)

            file_metadata = {'name': file_name}
            if parent_folder_id:
                file_metadata['parents'] = [parent_folder_id]

            media = MediaFileUpload(file_path, resumable=True)

            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name'
            ).execute()

            print(f"Dosya yüklendi: {file.get('name')} (ID: {file.get('id')})")
            return file.get('id')

        except Exception as error:
            print(f'Yükleme hatası: {error}')
            return None

    def download_file(self, file_id, destination_path):
        """
        Dosya indirir

        Args:
            file_id: İndirilecek dosyanın ID'si
            destination_path: İndirilecek dosyanın kaydedileceği yol

        Returns:
            Başarı durumu (True/False)
        """
        try:
            request = self.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"İndirme: {int(status.progress() * 100)}%")

            # Dosyayı diske yaz
            fh.seek(0)
            with open(destination_path, 'wb') as f:
                f.write(fh.read())

            print(f"Dosya indirildi: {destination_path}")
            return True

        except Exception as error:
            print(f'İndirme hatası: {error}')
            return False

    def create_folder(self, folder_name, parent_folder_id=None):
        """
        Klasör oluşturur

        Args:
            folder_name: Oluşturulacak klasörün adı
            parent_folder_id: Üst klasörün ID'si (opsiyonel)

        Returns:
            Oluşturulan klasörün ID'si
        """
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }

            if parent_folder_id:
                file_metadata['parents'] = [parent_folder_id]

            folder = self.service.files().create(
                body=file_metadata,
                fields='id, name'
            ).execute()

            print(f"Klasör oluşturuldu: {folder.get('name')} (ID: {folder.get('id')})")
            return folder.get('id')

        except Exception as error:
            print(f'Klasör oluşturma hatası: {error}')
            return None

    def delete_file(self, file_id):
        """
        Dosya veya klasörü siler

        Args:
            file_id: Silinecek dosya/klasörün ID'si

        Returns:
            Başarı durumu (True/False)
        """
        try:
            self.service.files().delete(fileId=file_id).execute()
            print(f"Dosya/Klasör silindi: {file_id}")
            return True

        except Exception as error:
            print(f'Silme hatası: {error}')
            return False

    def share_file(self, file_id, email, role='reader'):
        """
        Dosyayı paylaşır

        Args:
            file_id: Paylaşılacak dosyanın ID'si
            email: Paylaşılacak kişinin email adresi
            role: İzin rolü ('reader', 'writer', 'owner')

        Returns:
            Başarı durumu (True/False)
        """
        try:
            permission = {
                'type': 'user',
                'role': role,
                'emailAddress': email
            }

            self.service.permissions().create(
                fileId=file_id,
                body=permission,
                fields='id'
            ).execute()

            print(f"Dosya paylaşıldı: {email} ({role})")
            return True

        except Exception as error:
            print(f'Paylaşım hatası: {error}')
            return False

    def get_file_info(self, file_id):
        """
        Dosya bilgilerini getirir

        Args:
            file_id: Bilgileri alınacak dosyanın ID'si

        Returns:
            Dosya bilgileri
        """
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields='id, name, mimeType, size, createdTime, modifiedTime, parents, webViewLink, webContentLink'
            ).execute()

            print(f"Dosya Bilgileri:")
            print(f"  - Ad: {file.get('name')}")
            print(f"  - ID: {file.get('id')}")
            print(f"  - Tip: {file.get('mimeType')}")
            print(f"  - Boyut: {file.get('size', 'N/A')} bytes")
            print(f"  - Oluşturulma: {file.get('createdTime')}")
            print(f"  - Değiştirilme: {file.get('modifiedTime')}")
            print(f"  - Web Linki: {file.get('webViewLink', 'N/A')}")

            return file

        except Exception as error:
            print(f'Dosya bilgisi hatası: {error}')
            return None