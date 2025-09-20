from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd

class GoogleSheetsAPI:
    def __init__(self, credentials_file='dr-murzoglu-doktora.json'):
        """
        Google Sheets API istemcisini başlatır

        Args:
            credentials_file: Service account JSON dosyasının yolu
        """
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        # Service account kimlik bilgilerini yükle
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_file,
            scopes=self.SCOPES
        )

        # Sheets servisini oluştur
        self.service = build('sheets', 'v4', credentials=self.credentials)

    def create_spreadsheet(self, title):
        """
        Yeni bir Google Sheets dosyası oluşturur

        Args:
            title: Oluşturulacak dosyanın adı

        Returns:
            Oluşturulan dosyanın ID'si ve URL'i
        """
        try:
            spreadsheet = {
                'properties': {
                    'title': title
                }
            }

            spreadsheet = self.service.spreadsheets().create(
                body=spreadsheet,
                fields='spreadsheetId, spreadsheetUrl'
            ).execute()

            print(f"Yeni spreadsheet oluşturuldu:")
            print(f"  - ID: {spreadsheet.get('spreadsheetId')}")
            print(f"  - URL: {spreadsheet.get('spreadsheetUrl')}")

            return {
                'id': spreadsheet.get('spreadsheetId'),
                'url': spreadsheet.get('spreadsheetUrl')
            }

        except Exception as error:
            print(f'Spreadsheet oluşturma hatası: {error}')
            return None

    def read_range(self, spreadsheet_id, range_name):
        """
        Belirtilen aralıktaki verileri okur

        Args:
            spreadsheet_id: Google Sheets dosyasının ID'si
            range_name: Okunacak aralık (örn: 'Sheet1!A1:C10')

        Returns:
            Okunan veriler
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()

            values = result.get('values', [])

            if not values:
                print('Veri bulunamadı.')
                return []
            else:
                print(f'{len(values)} satır veri okundu.')
                return values

        except Exception as error:
            print(f'Veri okuma hatası: {error}')
            return []

    def write_range(self, spreadsheet_id, range_name, values, value_input_option='USER_ENTERED'):
        """
        Belirtilen aralığa veri yazar

        Args:
            spreadsheet_id: Google Sheets dosyasının ID'si
            range_name: Yazılacak aralık (örn: 'Sheet1!A1')
            values: Yazılacak veriler (2D liste)
            value_input_option: Değer girdi seçeneği ('RAW' veya 'USER_ENTERED')

        Returns:
            Güncellenen hücre sayısı
        """
        try:
            body = {
                'values': values
            }

            result = self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body
            ).execute()

            print(f"{result.get('updatedCells')} hücre güncellendi.")
            return result.get('updatedCells')

        except Exception as error:
            print(f'Veri yazma hatası: {error}')
            return 0

    def append_rows(self, spreadsheet_id, range_name, values, value_input_option='USER_ENTERED'):
        """
        Belirtilen aralığın sonuna satır ekler

        Args:
            spreadsheet_id: Google Sheets dosyasının ID'si
            range_name: Eklenecek aralık (örn: 'Sheet1!A:E')
            values: Eklenecek veriler (2D liste)
            value_input_option: Değer girdi seçeneği ('RAW' veya 'USER_ENTERED')

        Returns:
            Eklenen satır sayısı
        """
        try:
            body = {
                'values': values
            }

            result = self.service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()

            updates = result.get('updates', {})
            print(f"{updates.get('updatedRows', 0)} satır eklendi.")
            return updates.get('updatedRows', 0)

        except Exception as error:
            print(f'Satır ekleme hatası: {error}')
            return 0

    def clear_range(self, spreadsheet_id, range_name):
        """
        Belirtilen aralıktaki verileri temizler

        Args:
            spreadsheet_id: Google Sheets dosyasının ID'si
            range_name: Temizlenecek aralık (örn: 'Sheet1!A1:C10')

        Returns:
            Başarı durumu (True/False)
        """
        try:
            self.service.spreadsheets().values().clear(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()

            print(f"Aralık temizlendi: {range_name}")
            return True

        except Exception as error:
            print(f'Temizleme hatası: {error}')
            return False

    def batch_update(self, spreadsheet_id, requests):
        """
        Toplu güncelleme yapar

        Args:
            spreadsheet_id: Google Sheets dosyasının ID'si
            requests: Güncelleme istekleri listesi

        Returns:
            Güncelleme sonuçları
        """
        try:
            body = {
                'requests': requests
            }

            result = self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=body
            ).execute()

            print(f"{len(result.get('replies', []))} güncelleme tamamlandı.")
            return result

        except Exception as error:
            print(f'Toplu güncelleme hatası: {error}')
            return None

    def format_cells(self, spreadsheet_id, sheet_id, start_row, end_row, start_col, end_col, format_dict):
        """
        Hücreleri formatlar

        Args:
            spreadsheet_id: Google Sheets dosyasının ID'si
            sheet_id: Sheet ID'si (genellikle 0)
            start_row: Başlangıç satırı (0-indexed)
            end_row: Bitiş satırı
            start_col: Başlangıç sütunu (0-indexed)
            end_col: Bitiş sütunu
            format_dict: Format özellikleri

        Returns:
            Başarı durumu (True/False)
        """
        try:
            requests = [{
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': start_row,
                        'endRowIndex': end_row,
                        'startColumnIndex': start_col,
                        'endColumnIndex': end_col
                    },
                    'cell': {
                        'userEnteredFormat': format_dict
                    },
                    'fields': 'userEnteredFormat'
                }
            }]

            self.batch_update(spreadsheet_id, requests)
            print(f"Hücreler formatlandı.")
            return True

        except Exception as error:
            print(f'Formatlama hatası: {error}')
            return False

    def add_sheet(self, spreadsheet_id, sheet_title):
        """
        Yeni bir sayfa ekler

        Args:
            spreadsheet_id: Google Sheets dosyasının ID'si
            sheet_title: Eklenecek sayfanın adı

        Returns:
            Eklenen sayfanın ID'si
        """
        try:
            request = {
                'addSheet': {
                    'properties': {
                        'title': sheet_title
                    }
                }
            }

            result = self.batch_update(spreadsheet_id, [request])
            sheet_id = result['replies'][0]['addSheet']['properties']['sheetId']

            print(f"Yeni sayfa eklendi: {sheet_title} (ID: {sheet_id})")
            return sheet_id

        except Exception as error:
            print(f'Sayfa ekleme hatası: {error}')
            return None

    def delete_sheet(self, spreadsheet_id, sheet_id):
        """
        Bir sayfayı siler

        Args:
            spreadsheet_id: Google Sheets dosyasının ID'si
            sheet_id: Silinecek sayfanın ID'si

        Returns:
            Başarı durumu (True/False)
        """
        try:
            request = {
                'deleteSheet': {
                    'sheetId': sheet_id
                }
            }

            self.batch_update(spreadsheet_id, [request])
            print(f"Sayfa silindi: {sheet_id}")
            return True

        except Exception as error:
            print(f'Sayfa silme hatası: {error}')
            return False

    def dataframe_to_sheets(self, spreadsheet_id, dataframe, sheet_name='Sheet1', start_cell='A1'):
        """
        Pandas DataFrame'i Google Sheets'e yazar

        Args:
            spreadsheet_id: Google Sheets dosyasının ID'si
            dataframe: Yazılacak pandas DataFrame
            sheet_name: Hedef sayfa adı
            start_cell: Başlangıç hücresi

        Returns:
            Başarı durumu (True/False)
        """
        try:
            # DataFrame'i listeye çevir (başlıklarla birlikte)
            values = [dataframe.columns.tolist()] + dataframe.values.tolist()

            # Veriyi yaz
            range_name = f"{sheet_name}!{start_cell}"
            self.write_range(spreadsheet_id, range_name, values)

            print(f"DataFrame Google Sheets'e yazıldı.")
            return True

        except Exception as error:
            print(f'DataFrame yazma hatası: {error}')
            return False

    def sheets_to_dataframe(self, spreadsheet_id, range_name, header=True):
        """
        Google Sheets verilerini pandas DataFrame'e çevirir

        Args:
            spreadsheet_id: Google Sheets dosyasının ID'si
            range_name: Okunacak aralık
            header: İlk satırın başlık olup olmadığı

        Returns:
            Pandas DataFrame
        """
        try:
            values = self.read_range(spreadsheet_id, range_name)

            if not values:
                return pd.DataFrame()

            if header and len(values) > 1:
                df = pd.DataFrame(values[1:], columns=values[0])
            else:
                df = pd.DataFrame(values)

            print(f"DataFrame oluşturuldu: {df.shape[0]} satır, {df.shape[1]} sütun")
            return df

        except Exception as error:
            print(f'DataFrame oluşturma hatası: {error}')
            return pd.DataFrame()