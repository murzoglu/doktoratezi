"""
Google Sheets API kullanım örnekleri

Bu script Google Sheets API'nin temel işlevlerini gösterir.
"""

from google_sheets_api import GoogleSheetsAPI
import pandas as pd

def main():
    # Google Sheets API istemcisini başlat
    sheets = GoogleSheetsAPI('dr-murzoglu-doktora.json')

    print("="*50)
    print("GOOGLE SHEETS API ÖRNEKLERİ")
    print("="*50)

    # 1. Yeni bir spreadsheet oluştur
    print("\n1. Yeni spreadsheet oluşturma:")
    print("-"*30)
    spreadsheet_info = sheets.create_spreadsheet("Doktora Tezi Veri Analizi")

    if spreadsheet_info:
        spreadsheet_id = spreadsheet_info['id']
        print(f"Spreadsheet URL: {spreadsheet_info['url']}")

        # 2. Veri yazma
        print("\n2. Veri yazma:")
        print("-"*30)
        data = [
            ['İsim', 'Yaş', 'Bölüm', 'Not Ortalaması'],
            ['Ali Yılmaz', 25, 'Bilgisayar Müh.', 3.45],
            ['Ayşe Demir', 23, 'Elektrik Müh.', 3.78],
            ['Mehmet Kaya', 24, 'Makine Müh.', 3.21],
            ['Fatma Öz', 22, 'Endüstri Müh.', 3.92],
            ['Ahmet Can', 26, 'Bilgisayar Müh.', 3.65]
        ]
        sheets.write_range(spreadsheet_id, 'Sheet1!A1:D6', data)

        # 3. Veri okuma
        print("\n3. Veri okuma:")
        print("-"*30)
        read_data = sheets.read_range(spreadsheet_id, 'Sheet1!A1:D6')
        for row in read_data[:3]:  # İlk 3 satırı göster
            print(f"  {row}")

        # 4. Satır ekleme
        print("\n4. Yeni satırlar ekleme:")
        print("-"*30)
        new_rows = [
            ['Zeynep Yıldız', 24, 'Yazılım Müh.', 3.88],
            ['Murat Ak', 25, 'Veri Bilimi', 3.55]
        ]
        sheets.append_rows(spreadsheet_id, 'Sheet1!A:D', new_rows)

        # 5. Pandas DataFrame ile çalışma
        print("\n5. Pandas DataFrame entegrasyonu:")
        print("-"*30)

        # DataFrame oluştur
        df = pd.DataFrame({
            'Ürün': ['Laptop', 'Mouse', 'Klavye', 'Monitor', 'Kamera'],
            'Adet': [5, 15, 10, 3, 2],
            'Birim Fiyat': [15000, 150, 500, 5000, 2000],
            'Toplam': [75000, 2250, 5000, 15000, 4000]
        })
        print("Oluşturulan DataFrame:")
        print(df)

        # Yeni bir sayfa ekle
        print("\n6. Yeni sayfa ekleme:")
        print("-"*30)
        sheet_id = sheets.add_sheet(spreadsheet_id, "Envanter")

        # DataFrame'i Sheets'e yaz
        sheets.dataframe_to_sheets(spreadsheet_id, df, 'Envanter', 'A1')
        print("DataFrame Google Sheets'e yazıldı")

        # 7. Sheets'ten DataFrame'e okuma
        print("\n7. Sheets'ten DataFrame'e veri okuma:")
        print("-"*30)
        df_from_sheets = sheets.sheets_to_dataframe(spreadsheet_id, 'Sheet1!A1:D10')
        print("Google Sheets'ten okunan DataFrame:")
        print(df_from_sheets.head())

        # 8. Hücre formatlama
        print("\n8. Hücre formatlama:")
        print("-"*30)
        format_dict = {
            'backgroundColor': {
                'red': 0.95,
                'green': 0.95,
                'blue': 1.0
            },
            'textFormat': {
                'bold': True,
                'fontSize': 12
            }
        }
        sheets.format_cells(spreadsheet_id, 0, 0, 1, 0, 4, format_dict)
        print("Başlık satırı formatlandı")

        # 9. Toplu güncelleme örneği
        print("\n9. Toplu güncelleme:")
        print("-"*30)
        requests = [
            {
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': 0,
                        'dimension': 'COLUMNS',
                        'startIndex': 0,
                        'endIndex': 4
                    },
                    'properties': {
                        'pixelSize': 150
                    },
                    'fields': 'pixelSize'
                }
            }
        ]
        sheets.batch_update(spreadsheet_id, requests)
        print("Sütun genişlikleri güncellendi")

        # 10. Belirli bir aralığı temizleme
        print("\n10. Veri temizleme:")
        print("-"*30)
        # Önce test için veri ekleyelim
        test_data = [['Test', 'Veri', 'Temizlenecek']]
        sheets.write_range(spreadsheet_id, 'Sheet1!F1:H1', test_data)
        # Sonra temizleyelim
        sheets.clear_range(spreadsheet_id, 'Sheet1!F1:H1')
        print("Belirtilen aralık temizlendi")

    print("\n" + "="*50)
    print("Örnekler tamamlandı!")
    print("NOT: Oluşturulan dosyalara erişmek için:")
    print("1. Service account email'ini Google Drive'da paylaşın")
    print("2. Veya dosyayı manuel olarak kendinizle paylaşın")
    print("="*50)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nHata oluştu: {e}")
        print("\nOlası sebepler:")
        print("1. Service account dosyası (dr-murzoglu-doktora.json) bulunamadı")
        print("2. Google Sheets API etkinleştirilmemiş olabilir")
        print("3. Service account'un Sheets erişim izni olmayabilir")
        print("4. pandas kütüphanesi yüklü değil (pip install pandas)")
        print("\nÇözüm:")
        print("1. Google Cloud Console'da Sheets API'yi etkinleştirin")
        print("2. Service account'a gerekli izinleri verin")
        print("3. Gerekli Python paketlerini yükleyin: pip install -r requirements.txt")