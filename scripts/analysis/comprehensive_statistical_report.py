"""
Kapsamlı İstatistiksel Rapor
Tüm analizlerin özeti
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def create_comprehensive_report():
    """Tüm analiz sonuçlarını birleştiren kapsamlı rapor"""
    
    report = []
    report.append("="*80)
    report.append("DİYABETLİ ÇOCUKLARIN ANNELERİNDE DEPRESYON VE EBEVEYNLİK TUTUMLARI")
    report.append("KLİNİK ARAŞTIRMA SONUÇ RAPORU")
    report.append("="*80)
    report.append(f"\nRapor Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # 1. ÇALIŞMA TASARIMI VE ÖRNEKLEM
    report.append("\n" + "="*80)
    report.append("1. ÇALIŞMA TASARIMI VE ÖRNEKLEM")
    report.append("="*80)
    
    report.append("\n1.1. Çalışma Grubu:")
    report.append("  - Toplam Katılımcı: 194")
    report.append("  - Kontrol Grubu: 156 (80.4%)")
    report.append("  - Diyabet Grubu: 38 (19.6%)")
    report.append("  - Not: Protokolde beklenen ~100 diyabet, ~95 kontrol")
    
    # 2. DEMOGRAFİK ÖZELLİKLER
    report.append("\n" + "="*80)
    report.append("2. DEMOGRAFİK ÖZELLİKLER")
    report.append("="*80)
    
    report.append("\n2.1. Yaş Ortalamaları:")
    report.append("  - Anne: 39.4 ± 5.7 yıl")
    report.append("    * Kontrol: 39.8 yıl")
    report.append("    * Diyabet: 37.9 yıl")
    report.append("    * p = 0.034 (anlamlı fark)")
    
    report.append("\n  - Çocuk: 12.5 ± 2.6 yıl")
    report.append("    * Kontrol: 12.2 yıl")
    report.append("    * Diyabet: 13.5 yıl")
    report.append("    * p = 0.003 (anlamlı fark)")
    
    report.append("\n2.2. Diğer Demografik Özellikler:")
    report.append("  - Çalışan Anne Oranı: %87.6")
    report.append("  - Ortalama Çocuk Sayısı: 2.9")
    report.append("  - Kardeşi Olan Çocuk Oranı: %99 (192/194)")
    report.append("  - Anne Antidepresan Kullanım Oranı: %1.0")
    
    # 3. BECK DEPRESYON ÖLÇEĞİ SONUÇLARI
    report.append("\n" + "="*80)
    report.append("3. BECK DEPRESYON ÖLÇEĞİ SONUÇLARI")
    report.append("="*80)
    
    report.append("\n3.1. Toplam Skorlar:")
    report.append("  - Kontrol: 21.74 ± 15.31")
    report.append("  - Diyabet: 25.58 ± 14.18")
    report.append("  - Test: Mann-Whitney U")
    report.append("  - p = 0.066 (sınırda anlamlılık)")
    
    report.append("\n3.2. Alt Boyutlar:")
    report.append("  A. Bilişsel-Duygulanım (Cognitive-Affective):")
    report.append("     - Kontrol: 5.92 ± 5.11")
    report.append("     - Diyabet: 7.63 ± 4.74")
    report.append("     - p = 0.043 * (anlamlı fark)")
    
    report.append("\n  B. Somatik-Performans:")
    report.append("     - Kontrol: 4.15 ± 4.00")
    report.append("     - Diyabet: 5.16 ± 3.54")
    report.append("     - p = 0.055 (sınırda anlamlılık)")
    
    # 4. EMBU EBEVEYNLİK TUTUMLARI
    report.append("\n" + "="*80)
    report.append("4. EMBU EBEVEYNLİK TUTUMLARI ÖLÇEĞİ SONUÇLARI")
    report.append("="*80)
    
    report.append("\n4.1. Duygusal Sıcaklık:")
    report.append("  - Kontrol: 3.13 ± 0.93")
    report.append("  - Diyabet: 3.35 ± 0.90")
    report.append("  - p = 0.210 (anlamlı değil)")
    
    report.append("\n4.2. Reddedicilik:")
    report.append("  - Kontrol: 4.34 ± 0.54")
    report.append("  - Diyabet: 4.34 ± 0.56")
    report.append("  - p = 0.920 (anlamlı değil)")
    
    report.append("\n4.3. Aşırı Koruma:")
    report.append("  - Kontrol: 2.86 ± 0.59")
    report.append("  - Diyabet: 2.79 ± 0.55")
    report.append("  - p = 0.536 (anlamlı değil)")
    
    # 5. KORELASYON ANALİZLERİ
    report.append("\n" + "="*80)
    report.append("5. KORELASYON ANALİZLERİ")
    report.append("="*80)
    
    report.append("\n5.1. Tüm Örneklemde (n=190):")
    report.append("  - Beck x Duygusal Sıcaklık: r = 0.244, p = 0.001 **")
    report.append("  - Beck x Reddedicilik: r = 0.047, p = 0.517")
    report.append("  - Beck x Aşırı Koruma: r = 0.281, p < 0.001 ***")
    
    report.append("\n5.2. Kontrol Grubunda (n=152):")
    report.append("  - Beck x Duygusal Sıcaklık: r = 0.263, p = 0.001 **")
    report.append("  - Beck x Aşırı Koruma: r = 0.311, p < 0.001 ***")
    
    report.append("\n5.3. Diyabet Grubunda (n=38):")
    report.append("  - Anlamlı korelasyon bulunmamıştır")
    
    # 6. HİPOTEZ TESTLERİ SONUÇLARI
    report.append("\n" + "="*80)
    report.append("6. HİPOTEZ TESTLERİ SONUÇLARI")
    report.append("="*80)
    
    report.append("\nH1: Diyabetli çocukların annelerinde depresyon düzeyi daha yüksektir")
    report.append("    SONUÇ: DESTEKLENMEDİ")
    report.append("    - Toplam Beck skoru açısından anlamlı fark yok (p=0.066)")
    report.append("    - Ancak Bilişsel-Duygulanım alt boyutunda anlamlı fark var (p=0.043)")
    
    report.append("\nH2: Gruplar arasında ebeveynlik tutumları farklıdır")
    report.append("    SONUÇ: DESTEKLENMEDİ")
    report.append("    - Hiçbir EMBU alt boyutunda anlamlı fark bulunmamıştır")
    
    # 7. BULGULARIN YORUMLANMASI
    report.append("\n" + "="*80)
    report.append("7. BULGULARIN YORUMLANMASI VE KLİNİK ÖNEMİ")
    report.append("="*80)
    
    report.append("\n7.1. Önemli Bulgular:")
    report.append("  1. Diyabetli çocukların annelerinde bilişsel-duygulanım")
    report.append("     semptomları anlamlı olarak yüksek (p=0.043)")
    report.append("\n  2. Anne depresyonu ile aşırı korumacı tutum arasında")
    report.append("     pozitif korelasyon (r=0.281, p<0.001)")
    report.append("\n  3. Kontrol grubunda depresyon-ebeveynlik ilişkisi")
    report.append("     diyabet grubuna göre daha güçlü")
    
    report.append("\n7.2. Çalışmanın Kısıtlılıkları:")
    report.append("  1. Grup büyüklüğü dengesizliği (38 vs 156)")
    report.append("  2. Protokolde beklenen örneklem büyüklüğüne ulaşılamaması")
    report.append("  3. Kesitsel tasarım nedeniyle nedensellik kurulamaması")
    
    report.append("\n7.3. Klinik Öneriler:")
    report.append("  1. Diyabetli çocukların annelerinde bilişsel-duygulanım")
    report.append("     semptomlarına odaklı tarama ve müdahale")
    report.append("  2. Aşırı korumacı tutumların depresyonla ilişkisi")
    report.append("     nedeniyle ebeveyn eğitimi programları")
    report.append("  3. Multidisipliner takım yaklaşımının önemi")
    
    # 8. İSTATİSTİKSEL NOTLAR
    report.append("\n" + "="*80)
    report.append("8. İSTATİSTİKSEL NOTLAR")
    report.append("="*80)
    report.append("\n- Anlamlılık düzeyleri: * p<0.05, ** p<0.01, *** p<0.001")
    report.append("- Normal dağılım göstermeyen veriler için Mann-Whitney U testi kullanılmıştır")
    report.append("- Korelasyon analizlerinde Pearson korelasyon katsayısı kullanılmıştır")
    report.append("- Eksik veriler listwise deletion yöntemiyle ele alınmıştır")
    
    report.append("\n" + "="*80)
    report.append("RAPOR SONU")
    report.append("="*80)
    
    return "\n".join(report)

def create_executive_summary():
    """Yönetici özeti oluştur"""
    
    summary = []
    summary.append("="*60)
    summary.append("YÖNETİCİ ÖZETİ")
    summary.append("="*60)
    
    summary.append("\nÇALIŞMA: Diyabetli Çocukların Annelerinde Depresyon ve")
    summary.append("         Ebeveynlik Tutumları Araştırması")
    
    summary.append("\nÖRNEKLEM: 194 anne (38 diyabet, 156 kontrol)")
    
    summary.append("\nANA BULGULAR:")
    summary.append("1. Diyabetli çocukların annelerinde bilişsel-duygulanım")
    summary.append("   belirtileri anlamlı olarak yüksek (p=0.043)")
    summary.append("\n2. Depresyon ile aşırı korumacı tutum arasında")
    summary.append("   anlamlı pozitif ilişki (r=0.281, p<0.001)")
    summary.append("\n3. Gruplar arasında ebeveynlik tutumlarında")
    summary.append("   anlamlı fark bulunmamıştır")
    
    summary.append("\nÖNERİLER:")
    summary.append("- Diyabetli çocuk annelerine psikolojik destek")
    summary.append("- Ebeveyn eğitimi programları")
    summary.append("- Multidisipliner takip")
    
    summary.append("\n" + "="*60)
    
    return "\n".join(summary)

def main():
    """Ana fonksiyon"""
    
    print("\n" + "="*60)
    print("KAPSAMLI İSTATİSTİKSEL RAPOR OLUŞTURULUYOR")
    print("="*60)
    
    try:
        # Kapsamlı rapor
        full_report = create_comprehensive_report()
        
        # Raporu kaydet
        with open('results/comprehensive_statistical_report.txt', 'w', encoding='utf-8') as f:
            f.write(full_report)
        print("\n[OK] Kapsamlı rapor kaydedildi")
        
        # Yönetici özeti
        executive_summary = create_executive_summary()
        
        # Özeti kaydet
        with open('results/executive_summary.txt', 'w', encoding='utf-8') as f:
            f.write(executive_summary)
        print("[OK] Yönetici özeti kaydedildi")
        
        # Özeyi ekrana yazdır
        print("\n" + executive_summary)
        
        print("\n" + "="*60)
        print("RAPORLAMA TAMAMLANDI")
        print("="*60)
        print("\nOluşturulan dosyalar:")
        print("  - results/comprehensive_statistical_report.txt")
        print("  - results/executive_summary.txt")
        
    except Exception as e:
        print(f"\n[HATA] Rapor oluşturulurken hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()