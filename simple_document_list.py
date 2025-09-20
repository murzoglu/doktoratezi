"""
Basit belge listesi oluşturma
"""

from google_drive_api import GoogleDriveAPI
import json
from datetime import datetime

def list_all_documents(folder_id, drive, depth=0):
    """
    Tüm belgeleri listeler
    """
    all_items = []

    try:
        # Bu klasördeki dosyaları al
        query = f"'{folder_id}' in parents and trashed = false"
        items = drive.service.files().list(
            q=query,
            pageSize=100,
            fields="files(id, name, mimeType, size, createdTime, modifiedTime)"
        ).execute().get('files', [])

        for item in items:
            item_info = {
                'name': item.get('name', 'Unknown'),
                'id': item['id'],
                'type': item['mimeType'],
                'size': item.get('size', 0),
                'created': item.get('createdTime'),
                'modified': item.get('modifiedTime'),
                'depth': depth
            }

            mime_type = item.get('mimeType')

            # PDF veya Google Docs ise listeye ekle
            if mime_type in ['application/pdf', 'application/vnd.google-apps.document']:
                all_items.append(item_info)

            # Alt klasör ise recursive olarak tara
            elif mime_type == 'application/vnd.google-apps.folder':
                sub_items = list_all_documents(item['id'], drive, depth + 1)
                all_items.extend(sub_items)

    except Exception as e:
        print(f"Hata: {e}")

    return all_items

def main():
    # Ana klasör ID'si
    MAIN_FOLDER_ID = "1C8vsNG-kVbYmL3tCG_lYuyUvYElSCTvs"

    # Drive API başlat
    drive = GoogleDriveAPI('dr-murzoglu-doktora.json')

    print("Belgeler taraniyor...")

    # Tüm belgeleri listele
    documents = list_all_documents(MAIN_FOLDER_ID, drive)

    # Sonuçları kaydet
    result = {
        'scan_date': datetime.now().isoformat(),
        'total_documents': len(documents),
        'documents': documents
    }

    # JSON dosyasına kaydet
    with open('document_list.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # Özet rapor oluştur
    pdf_count = sum(1 for d in documents if 'pdf' in d['type'].lower())
    doc_count = sum(1 for d in documents if 'document' in d['type'].lower())

    print(f"\nTarama tamamlandi!")
    print(f"Toplam belge: {len(documents)}")
    print(f"PDF dosyalari: {pdf_count}")
    print(f"Google Docs: {doc_count}")

    # Basit bir markdown raporu oluştur
    with open('BELGE_LISTESI.md', 'w', encoding='utf-8') as f:
        f.write("# Doktora Tezi Belge Listesi\n\n")
        f.write(f"Tarama Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"## Özet\n")
        f.write(f"- Toplam Belge: {len(documents)}\n")
        f.write(f"- PDF Dosyaları: {pdf_count}\n")
        f.write(f"- Google Docs: {doc_count}\n\n")

        f.write("## PDF Dosyaları\n\n")
        for doc in documents:
            if 'pdf' in doc['type'].lower():
                f.write(f"- **{doc['name']}**\n")
                f.write(f"  - ID: `{doc['id']}`\n")
                size_kb = int(doc.get('size', 0)) / 1024
                if size_kb > 0:
                    f.write(f"  - Boyut: {size_kb:.2f} KB\n")
                f.write("\n")

        f.write("## Google Docs Belgeleri\n\n")
        for doc in documents:
            if 'document' in doc['type'].lower():
                f.write(f"- **{doc['name']}**\n")
                f.write(f"  - ID: `{doc['id']}`\n")
                f.write(f"  - Oluşturulma: {doc.get('created', 'N/A')}\n")
                f.write("\n")

    print("\nDosyalar olusturuldu:")
    print("- document_list.json")
    print("- BELGE_LISTESI.md")

if __name__ == "__main__":
    main()