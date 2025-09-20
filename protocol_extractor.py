"""
Etik kurul ve protokol belgelerini okuma ve analiz etme
"""

from google_drive_api import GoogleDriveAPI
from google_sheets_api import GoogleSheetsAPI
from googleapiclient.http import MediaIoBaseDownload
import io
import os
import json

def download_protocol_pdfs(drive):
    """
    Protokol ile ilgili PDF'leri indirir
    """
    os.makedirs("protocol_docs", exist_ok=True)

    # İndirilecek dosyaların ID'leri ve isimleri
    protocol_files = [
        {"id": "13mc8i0CO48NMatnfj1foNNjlptd3icN8", "name": "PROTOKOL_KODU.pdf"},
        {"id": "1Q7PLn4xK6y_FhaeUUS7kn1rBD0ACM_Cy", "name": "MUTF_Etik_Kurul_Basvurusu.pdf"},
        {"id": "12ZgArfILSz-64adgZkocyz75R3brk1iW", "name": "Enstitu_Onayi.pdf"},
        {"id": "1QuNUXsYblK_dFP1B4oy1Jq_Nlirx6mto", "name": "Bilgilendirilmis_Gonullu_Olur_Formu.pdf"},
        {"id": "128uFyiwAzvYOOIseVpKlFLZJ2DUUOq_Y", "name": "Beck_Depresyon_Olcegi.pdf"},
        {"id": "12BwXmmNx4Qfi0Y3_xUnkjEAUOHYaV5PF", "name": "EMBU_Cocuk.pdf"},
        {"id": "125oczmsjJSqcGxEmKgNXqwJxZst6lX_7", "name": "EMBU_Ebeveyn.pdf"},
        {"id": "12Cyx689ZS3EMmYLyCxWj0BtSbRexku6w", "name": "Kardes_Iliskileri_Anketi.pdf"},
        {"id": "124v2YfZAfujfLSQvAbFWia9SEvJxyVZ5", "name": "Kontrol_Grubu_Demografik.pdf"},
        {"id": "12574EJ5mOfC-iyma68lamWX2E8kEeRhf", "name": "Diyabetli_Cocuklar_Demografik.pdf"}
    ]

    downloaded_files = []

    for file_info in protocol_files:
        try:
            print(f"[INDIRILIYOR] {file_info['name']}")

            request = drive.service.files().get_media(fileId=file_info['id'])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

            # Dosyayı kaydet
            file_path = f"protocol_docs/{file_info['name']}"
            fh.seek(0)
            with open(file_path, 'wb') as f:
                f.write(fh.read())

            downloaded_files.append(file_path)
            print(f"  [OK] Indirildi: {file_path}")

        except Exception as e:
            print(f"  [HATA] {file_info['name']}: {e}")

    return downloaded_files

def read_google_docs_protocols(drive):
    """
    Google Docs formatındaki protokol belgelerini okur
    """
    # Google Docs ID'leri
    doc_ids = [
        {"id": "1qoRVxXa1N2_K4WAmrUN7YQI4mDkLtReAcf9dIzm6ufE", "name": "Doktora_Tez_Izlem_Raporu_2"},
        {"id": "1gxZVFwy02MnKTX_mbxNtQ12B50Sfb7pr6e8SY9JtbKs", "name": "Doktora_Tez_Izlem_1_Raporu"},
        {"id": "1zP9NaF4tClcKggCPuKSX0_cGnyEVYzjFd36rEzh5FME", "name": "Tez_Izlem_Komitesi_1_Rapor_Sunumu"}
    ]

    docs_content = []
    os.makedirs("protocol_docs/google_docs", exist_ok=True)

    for doc_info in doc_ids:
        try:
            print(f"[OKUNUYOR] {doc_info['name']}")

            # Text olarak export et
            request = drive.service.files().export_media(
                fileId=doc_info['id'],
                mimeType='text/plain'
            )
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

            # İçeriği al ve kaydet
            fh.seek(0)
            content = fh.read().decode('utf-8', errors='ignore')

            # Dosyaya kaydet
            file_path = f"protocol_docs/google_docs/{doc_info['name']}.txt"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            docs_content.append({
                'name': doc_info['name'],
                'content': content,
                'path': file_path
            })

            print(f"  [OK] Okundu: {len(content)} karakter")

        except Exception as e:
            print(f"  [HATA] {doc_info['name']}: {e}")

    return docs_content

def read_patient_data_sheets(sheets_api):
    """
    Hasta veri tablolarından bilgi okur
    """
    # Ana veri tablosu ID'si
    SHEET_ID = "1AIeTlphqgSLy8ESwa5lblhSgH_ZbHTvX8RafW3vshG8"  # Hasta_Verileri_Final

    try:
        print("\n[VERI TABLOSU] Hasta verileri okunuyor...")

        # İlk 5 satır ve tüm sütunları oku (başlıklar ve örnek veri)
        data = sheets_api.read_range(SHEET_ID, 'A1:AZ5')

        if data and len(data) > 0:
            headers = data[0] if len(data) > 0 else []
            sample_data = data[1:5] if len(data) > 1 else []

            # Toplam satır sayısını kontrol et
            all_data = sheets_api.read_range(SHEET_ID, 'A:A')
            total_rows = len(all_data) if all_data else 0

            return {
                'headers': headers,
                'sample_data': sample_data,
                'total_rows': total_rows,
                'column_count': len(headers)
            }

    except Exception as e:
        print(f"  [HATA] Veri tablosu okunamadi: {e}")
        return None

def main():
    print("="*60)
    print("KLINIK CALISMA PROTOKOLU ANALIZI")
    print("="*60)

    # API'leri başlat
    drive = GoogleDriveAPI('dr-murzoglu-doktora.json')
    sheets = GoogleSheetsAPI('dr-murzoglu-doktora.json')

    # 1. PDF'leri indir
    print("\n1. PDF Belgeler Indiriliyor...")
    print("-"*40)
    pdf_files = download_protocol_pdfs(drive)

    # 2. Google Docs belgelerini oku
    print("\n2. Google Docs Belgeleri Okunuyor...")
    print("-"*40)
    google_docs = read_google_docs_protocols(drive)

    # 3. Hasta veri tablolarını oku
    print("\n3. Hasta Veri Tablolari Analiz Ediliyor...")
    print("-"*40)
    patient_data_info = read_patient_data_sheets(sheets)

    # Sonuçları kaydet
    results = {
        'pdf_files': pdf_files,
        'google_docs': [{'name': d['name'], 'path': d['path'], 'size': len(d['content'])} for d in google_docs],
        'patient_data': patient_data_info
    }

    with open('protocol_analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n" + "="*60)
    print("ANALIZ TAMAMLANDI!")
    print("="*60)
    print(f"\nIndirilen PDF: {len(pdf_files)}")
    print(f"Okunan Google Docs: {len(google_docs)}")
    if patient_data_info:
        print(f"Veri Tablosu: {patient_data_info['total_rows']} satir, {patient_data_info['column_count']} sutun")

    print("\nOlusturulan dosyalar:")
    print("  - protocol_docs/ (PDF ve text dosyalari)")
    print("  - protocol_analysis_results.json")

    return results, google_docs

if __name__ == "__main__":
    results, docs_content = main()