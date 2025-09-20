"""
Google Docs içeriklerini okuma ve özetleme
"""

from google_drive_api import GoogleDriveAPI
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
import io
import os

def read_google_docs(doc_id, drive):
    """
    Google Docs içeriğini okur
    """
    try:
        # Text olarak export et
        request = drive.service.files().export_media(
            fileId=doc_id,
            mimeType='text/plain'
        )
        fh = io.BytesIO()
        from googleapiclient.http import MediaIoBaseDownload
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        # Text içeriği al
        fh.seek(0)
        content = fh.read().decode('utf-8', errors='ignore')
        return content

    except Exception as e:
        print(f"Hata: {e}")
        return None

def main():
    # Drive API başlat
    drive = GoogleDriveAPI('dr-murzoglu-doktora.json')

    # document_list.json dosyasını oku
    with open('document_list.json', 'r', encoding='utf-8') as f:
        doc_list = json.load(f)

    # Google Docs belgelerini filtrele
    google_docs = [d for d in doc_list['documents'] if 'document' in d['type'].lower()]

    print(f"Toplam {len(google_docs)} Google Docs bulundu.\n")

    # Her birini oku ve kaydet
    os.makedirs("google_docs_content", exist_ok=True)

    docs_summary = []

    for i, doc in enumerate(google_docs[:10], 1):  # İlk 10 doküman
        print(f"\n[{i}/{min(10, len(google_docs))}] {doc['name']}")
        print("-" * 50)

        content = read_google_docs(doc['id'], drive)

        if content:
            # Dosya adını güvenli hale getir
            safe_name = "".join(c for c in doc['name'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            file_path = f"google_docs_content/{safe_name}.txt"

            # İçeriği dosyaya kaydet
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Özet bilgi hazırla
            lines = content.split('\n')
            word_count = len(content.split())
            char_count = len(content)

            summary_info = {
                'name': doc['name'],
                'id': doc['id'],
                'word_count': word_count,
                'char_count': char_count,
                'line_count': len(lines),
                'file_path': file_path,
                'first_lines': '\n'.join(lines[:5]) if lines else ''
            }

            docs_summary.append(summary_info)

            print(f"[OK] Icerik okundu: {word_count} kelime, {len(lines)} satir")
            print(f"[OK] Kaydedildi: {file_path}")

            # İlk birkaç satırı göster
            if lines:
                print("\nIlk satirlar:")
                for line in lines[:3]:
                    if line.strip():
                        print(f"  > {line[:100]}...")
        else:
            print("[HATA] Icerik okunamadi")

    # Özet rapor oluştur
    with open('google_docs_summary.json', 'w', encoding='utf-8') as f:
        json.dump(docs_summary, f, ensure_ascii=False, indent=2)

    # Markdown raporu
    with open('GOOGLE_DOCS_ICERIKLERI.md', 'w', encoding='utf-8') as f:
        f.write("# Google Docs İçerik Analizi\n\n")
        f.write(f"Toplam {len(docs_summary)} belge okundu.\n\n")

        for doc in docs_summary:
            f.write(f"## {doc['name']}\n\n")
            f.write(f"- **Kelime Sayısı:** {doc['word_count']:,}\n")
            f.write(f"- **Karakter Sayısı:** {doc['char_count']:,}\n")
            f.write(f"- **Satır Sayısı:** {doc['line_count']:,}\n")
            f.write(f"- **Dosya:** `{doc['file_path']}`\n\n")

            if doc['first_lines']:
                f.write("### İlk Satırlar:\n```\n")
                f.write(doc['first_lines'][:500])
                f.write("\n```\n\n")

    print(f"\n\n{'='*60}")
    print("TAMAMLANDI!")
    print(f"{'='*60}")
    print(f"\nOkunan Google Docs: {len(docs_summary)}")
    print("\nOluşturulan dosyalar:")
    print("  - google_docs_content/ (içerik dosyaları)")
    print("  - google_docs_summary.json")
    print("  - GOOGLE_DOCS_ICERIKLERI.md")

if __name__ == "__main__":
    main()