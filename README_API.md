# Google Drive ve Sheets API Entegrasyonu

Bu proje Google Drive ve Google Sheets API'lerini Python ile kullanmak için hazırlanmıştır.

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Service Account JSON dosyanızın (`dr-murzoglu-doktora.json`) proje dizininde olduğundan emin olun.

## API'leri Etkinleştirme

Google Cloud Console'da aşağıdaki API'leri etkinleştirin:

1. **Google Drive API**: https://console.cloud.google.com/apis/library/drive.googleapis.com
2. **Google Sheets API**: https://console.cloud.google.com/apis/library/sheets.googleapis.com

## Dosyalar

### API Sınıfları
- `google_drive_api.py`: Google Drive işlemleri için sınıf
- `google_sheets_api.py`: Google Sheets işlemleri için sınıf

### Örnek Kullanımlar
- `example_drive_usage.py`: Drive API kullanım örnekleri
- `example_sheets_usage.py`: Sheets API kullanım örnekleri

## Google Drive API Özellikleri

```python
from google_drive_api import GoogleDriveAPI

drive = GoogleDriveAPI('dr-murzoglu-doktora.json')

# Dosyaları listele
files = drive.list_files()

# Klasör oluştur
folder_id = drive.create_folder("Klasör Adı")

# Dosya yükle
file_id = drive.upload_file("dosya.txt", parent_folder_id=folder_id)

# Dosya indir
drive.download_file(file_id, "indirilecek_dosya.txt")

# Dosya bilgilerini al
info = drive.get_file_info(file_id)

# Dosya paylaş
drive.share_file(file_id, "email@example.com", role="reader")

# Dosya/Klasör sil
drive.delete_file(file_id)
```

## Google Sheets API Özellikleri

```python
from google_sheets_api import GoogleSheetsAPI
import pandas as pd

sheets = GoogleSheetsAPI('dr-murzoglu-doktora.json')

# Yeni spreadsheet oluştur
result = sheets.create_spreadsheet("Dosya Adı")
spreadsheet_id = result['id']

# Veri yaz
data = [['Başlık1', 'Başlık2'], ['Değer1', 'Değer2']]
sheets.write_range(spreadsheet_id, 'Sheet1!A1', data)

# Veri oku
values = sheets.read_range(spreadsheet_id, 'Sheet1!A1:B10')

# Satır ekle
new_rows = [['Yeni', 'Veri']]
sheets.append_rows(spreadsheet_id, 'Sheet1!A:B', new_rows)

# Pandas DataFrame entegrasyonu
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
sheets.dataframe_to_sheets(spreadsheet_id, df, 'Sheet1')

# Sheets'ten DataFrame oku
df = sheets.sheets_to_dataframe(spreadsheet_id, 'Sheet1!A1:B10')

# Yeni sayfa ekle
sheet_id = sheets.add_sheet(spreadsheet_id, "Yeni Sayfa")

# Hücreleri formatla
format_dict = {
    'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 1.0},
    'textFormat': {'bold': True}
}
sheets.format_cells(spreadsheet_id, 0, 0, 1, 0, 2, format_dict)
```

## Önemli Notlar

### Erişim İzinleri
1. Service account email adresini (`doktora@dr-murzoglu.iam.gserviceaccount.com`) Google Drive klasörlerinize veya Sheets dosyalarınıza editör olarak ekleyin.

2. Alternatif olarak, oluşturulan dosyaları `share_file()` metodu ile kendi email adresinizle paylaşabilirsiniz.

### Güvenlik
- `dr-murzoglu-doktora.json` dosyasını **asla** public repository'lere yüklemeyin.
- Bu dosyayı `.gitignore` dosyanıza ekleyin.
- Production ortamında environment variable veya secret management sistemi kullanın.

### Limit ve Kotalar
- Google API'leri günlük kullanım kotalarına sahiptir.
- Büyük veri setleri için batch işlemleri kullanın.
- Rate limiting'e dikkat edin (saniyede çok fazla istek yapmayın).

## Sorun Giderme

### "API not enabled" hatası
Google Cloud Console'da ilgili API'yi etkinleştirin.

### "Permission denied" hatası
Service account'un dosyaya erişim izni olduğundan emin olun.

### "Credentials not found" hatası
`dr-murzoglu-doktora.json` dosyasının doğru konumda olduğundan emin olun.

## Örnekleri Çalıştırma

```bash
# Drive API örnekleri
python example_drive_usage.py

# Sheets API örnekleri
python example_sheets_usage.py
```

## Destek

Daha fazla bilgi için Google API dokümantasyonuna bakın:
- [Google Drive API](https://developers.google.com/drive)
- [Google Sheets API](https://developers.google.com/sheets)