"""
Google Drive'daki PDF ve Google Docs belgelerini analiz eden script
"""

from google_drive_api import GoogleDriveAPI
from googleapiclient.http import MediaIoBaseDownload
import io
import os
import json
from datetime import datetime

class DocumentAnalyzer:
    def __init__(self, credentials_file='dr-murzoglu-doktora.json'):
        self.drive = GoogleDriveAPI(credentials_file)
        self.documents = []
        self.pdf_files = []
        self.google_docs = []

    def find_all_documents(self, folder_id):
        """
        Belirtilen klasör ve alt klasörlerdeki tüm belgeleri bulur
        """
        print(f"\n[TARAMA] Klasor taraniyor: {folder_id}")

        # Bu klasördeki dosyaları al
        query = f"'{folder_id}' in parents and trashed = false"
        items = self.drive.service.files().list(
            q=query,
            pageSize=100,
            fields="files(id, name, mimeType, parents, createdTime, modifiedTime, size)"
        ).execute().get('files', [])

        for item in items:
            mime_type = item.get('mimeType')

            # PDF dosyaları
            if mime_type == 'application/pdf':
                self.pdf_files.append(item)
                print(f"  [PDF] {item['name']}")

            # Google Docs belgeleri
            elif mime_type == 'application/vnd.google-apps.document':
                self.google_docs.append(item)
                print(f"  [DOCS] {item['name']}")

            # Alt klasörleri de tara
            elif mime_type == 'application/vnd.google-apps.folder':
                print(f"  [KLASOR] {item['name']} - alt klasor taraniyor...")
                self.find_all_documents(item['id'])

    def download_pdf(self, file_id, file_name):
        """
        PDF dosyasını indirir
        """
        try:
            # Güvenli dosya adı oluştur
            safe_name = "".join(c for c in file_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            file_path = f"downloads/{safe_name}"

            # downloads klasörünü oluştur
            os.makedirs("downloads", exist_ok=True)

            request = self.drive.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

            # Dosyayı kaydet
            fh.seek(0)
            with open(file_path, 'wb') as f:
                f.write(fh.read())

            return file_path
        except Exception as e:
            print(f"    [HATA] PDF indirilemedi: {e}")
            return None

    def export_google_doc(self, file_id, file_name):
        """
        Google Docs belgesini text olarak dışa aktarır
        """
        try:
            # Text olarak export et
            request = self.drive.service.files().export_media(
                fileId=file_id,
                mimeType='text/plain'
            )
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

            # Text içeriği al
            fh.seek(0)
            content = fh.read().decode('utf-8', errors='ignore')
            return content

        except Exception as e:
            print(f"    [HATA] Google Doc okunamadi: {e}")
            return None

    def analyze_documents(self):
        """
        Tüm belgeleri analiz eder
        """
        print("\n" + "="*60)
        print("BELGE ANALIZI BASLIYOR")
        print("="*60)

        analysis_results = {
            'pdf_files': [],
            'google_docs': [],
            'summary': {},
            'generated_at': datetime.now().isoformat()
        }

        # PDF dosyalarını analiz et
        print(f"\n[PDF ANALIZI] {len(self.pdf_files)} adet PDF bulundu")
        print("-"*40)

        for pdf in self.pdf_files:
            print(f"\n[ISLEM] {pdf['name']}")

            pdf_info = {
                'name': pdf['name'],
                'id': pdf['id'],
                'size_kb': int(pdf.get('size', 0)) / 1024 if pdf.get('size') else 0,
                'created': pdf.get('createdTime'),
                'modified': pdf.get('modifiedTime'),
                'download_status': 'pending'
            }

            # PDF'i indir
            file_path = self.download_pdf(pdf['id'], pdf['name'])
            if file_path:
                pdf_info['download_status'] = 'success'
                pdf_info['local_path'] = file_path
                print(f"  [INDIRILDI] {file_path}")
            else:
                pdf_info['download_status'] = 'failed'

            analysis_results['pdf_files'].append(pdf_info)

        # Google Docs belgelerini analiz et
        print(f"\n[GOOGLE DOCS ANALIZI] {len(self.google_docs)} adet Google Docs bulundu")
        print("-"*40)

        for doc in self.google_docs:
            print(f"\n[ISLEM] {doc['name']}")

            doc_info = {
                'name': doc['name'],
                'id': doc['id'],
                'created': doc.get('createdTime'),
                'modified': doc.get('modifiedTime'),
                'content_preview': '',
                'word_count': 0
            }

            # İçeriği al
            content = self.export_google_doc(doc['id'], doc['name'])
            if content:
                # İlk 500 karakteri önizleme olarak sakla
                doc_info['content_preview'] = content[:500] + '...' if len(content) > 500 else content
                doc_info['word_count'] = len(content.split())
                doc_info['export_status'] = 'success'
                print(f"  [OKUNDU] {doc_info['word_count']} kelime")

                # İçeriği dosyaya kaydet
                safe_name = "".join(c for c in doc['name'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                os.makedirs("docs_export", exist_ok=True)
                with open(f"docs_export/{safe_name}.txt", 'w', encoding='utf-8') as f:
                    f.write(content)
            else:
                doc_info['export_status'] = 'failed'

            analysis_results['google_docs'].append(doc_info)

        # Özet bilgi
        analysis_results['summary'] = {
            'total_documents': len(self.pdf_files) + len(self.google_docs),
            'pdf_count': len(self.pdf_files),
            'google_docs_count': len(self.google_docs),
            'successful_pdf_downloads': sum(1 for p in analysis_results['pdf_files'] if p['download_status'] == 'success'),
            'successful_doc_exports': sum(1 for d in analysis_results['google_docs'] if d.get('export_status') == 'success')
        }

        return analysis_results

    def create_index(self, results):
        """
        Analiz sonuçlarından dizin oluşturur
        """
        print("\n" + "="*60)
        print("BELGE DIZINI OLUSTURULUYOR")
        print("="*60)

        # JSON olarak kaydet
        with open('document_index.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("\n[KAYIT] document_index.json dosyasi olusturuldu")

        # Markdown dizin oluştur
        with open('BELGE_DIZINI.md', 'w', encoding='utf-8') as f:
            f.write("# Doktora Tezi Belge Dizini\n\n")
            f.write(f"Oluşturulma Tarihi: {results['generated_at']}\n\n")

            # Özet
            f.write("## Özet\n\n")
            f.write(f"- **Toplam Belge:** {results['summary']['total_documents']}\n")
            f.write(f"- **PDF Dosyaları:** {results['summary']['pdf_count']}\n")
            f.write(f"- **Google Docs:** {results['summary']['google_docs_count']}\n")
            f.write(f"- **İndirilen PDF:** {results['summary']['successful_pdf_downloads']}\n")
            f.write(f"- **Dışa Aktarılan Docs:** {results['summary']['successful_doc_exports']}\n\n")

            # PDF Dosyaları
            f.write("## PDF Dosyaları\n\n")
            for pdf in results['pdf_files']:
                f.write(f"### {pdf['name']}\n")
                f.write(f"- **ID:** {pdf['id']}\n")
                f.write(f"- **Boyut:** {pdf['size_kb']:.2f} KB\n")
                f.write(f"- **Oluşturulma:** {pdf.get('created', 'N/A')}\n")
                f.write(f"- **Değiştirilme:** {pdf.get('modified', 'N/A')}\n")
                f.write(f"- **İndirme Durumu:** {pdf['download_status']}\n")
                if pdf.get('local_path'):
                    f.write(f"- **Yerel Dosya:** {pdf['local_path']}\n")
                f.write("\n")

            # Google Docs
            f.write("## Google Docs Belgeleri\n\n")
            for doc in results['google_docs']:
                f.write(f"### {doc['name']}\n")
                f.write(f"- **ID:** {doc['id']}\n")
                f.write(f"- **Kelime Sayısı:** {doc['word_count']}\n")
                f.write(f"- **Oluşturulma:** {doc.get('created', 'N/A')}\n")
                f.write(f"- **Değiştirilme:** {doc.get('modified', 'N/A')}\n")
                f.write(f"- **Dışa Aktarma:** {doc.get('export_status', 'N/A')}\n")
                if doc.get('content_preview'):
                    f.write(f"\n**İçerik Önizlemesi:**\n```\n{doc['content_preview'][:300]}...\n```\n")
                f.write("\n")

        print("[KAYIT] BELGE_DIZINI.md dosyasi olusturuldu")

        return True

def main():
    # Ana klasör ID'si
    MAIN_FOLDER_ID = "1C8vsNG-kVbYmL3tCG_lYuyUvYElSCTvs"

    # Analyzer oluştur
    analyzer = DocumentAnalyzer()

    try:
        # Tüm belgeleri bul
        print("\n[BASLANGIC] Tum belgeler taraniyor...")
        analyzer.find_all_documents(MAIN_FOLDER_ID)

        # Belgeleri analiz et
        results = analyzer.analyze_documents()

        # Dizin oluştur
        analyzer.create_index(results)

        print("\n" + "="*60)
        print("[TAMAMLANDI] Belge analizi ve dizin olusturma basarili!")
        print("="*60)
        print("\nOlusturulan dosyalar:")
        print("  - document_index.json (JSON formati)")
        print("  - BELGE_DIZINI.md (Markdown formati)")
        print("  - downloads/ (indirilen PDF dosyalari)")
        print("  - docs_export/ (disa aktarilan Google Docs)")

    except Exception as e:
        print(f"\n[KRITIK HATA]: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()