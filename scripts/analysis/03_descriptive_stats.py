"""
03_descriptive_stats.py
Tanımlayıcı istatistikler ve görselleştirmeler
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Grafik ayarları
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

def load_cleaned_data():
    """Temizlenmiş veriyi yükler"""
    try:
        df = pd.read_csv('data/cleaned/cleaned_dataset.csv')
        print(f"[✓] Veri yüklendi: {df.shape[0]} satır, {df.shape[1]} sütun")
        return df
    except Exception as e:
        print(f"[HATA] Veri yüklenemedi: {e}")
        return None

def demographic_analysis(df):
    """Demografik analizler"""

    print("\n" + "="*60)
    print("DEMOGRAFİK ÖZELLİKLER")
    print("="*60)

    demo_stats = {}

    # Grup dağılımı
    if 'Grup' in df.columns:
        grup_counts = df['Grup'].value_counts()
        print("\n[GRUP DAĞILIMI]")
        for grup, count in grup_counts.items():
            pct = (count / len(df)) * 100
            print(f"  {grup}: {count} ({pct:.1f}%)")
        demo_stats['Grup'] = grup_counts.to_dict()

    # Cinsiyet dağılımı
    if 'Katilimci_Cocuk_Cinsiyet' in df.columns:
        cinsiyet_counts = df['Katilimci_Cocuk_Cinsiyet'].value_counts()
        print("\n[CİNSİYET DAĞILIMI]")
        for cinsiyet, count in cinsiyet_counts.items():
            pct = (count / len(df)) * 100
            print(f"  {cinsiyet}: {count} ({pct:.1f}%)")
        demo_stats['Cinsiyet'] = cinsiyet_counts.to_dict()

    # Yaş istatistikleri
    yas_cols = [col for col in df.columns if col.endswith('_Yas')]
    if yas_cols:
        print("\n[YAŞ İSTATİSTİKLERİ]")
        for col in yas_cols:
            if col in df.columns:
                mean_age = df[col].mean()
                std_age = df[col].std()
                median_age = df[col].median()
                print(f"\n{col}:")
                print(f"  Ortalama: {mean_age:.1f} ± {std_age:.1f}")
                print(f"  Medyan: {median_age:.1f}")
                print(f"  Min-Max: {df[col].min():.1f} - {df[col].max():.1f}")

    # Eğitim durumu
    if 'Egitim_Durumu' in df.columns:
        egitim_counts = df['Egitim_Durumu'].value_counts()
        print("\n[EĞİTİM DURUMU]")
        for egitim, count in egitim_counts.items():
            pct = (count / len(df)) * 100
            print(f"  {egitim}: {count} ({pct:.1f}%)")

    return demo_stats

def scale_reliability_analysis(df):
    """Ölçek güvenilirlik analizleri"""

    print("\n" + "="*60)
    print("ÖLÇEK GÜVENİLİRLİK ANALİZLERİ")
    print("="*60)

    # Beck Depresyon Ölçeği
    beck_cols = [col for col in df.columns if col.startswith('Beck_') and not col.endswith('_Score')]
    if beck_cols:
        beck_data = df[beck_cols].dropna()
        if len(beck_data) > 0:
            # Cronbach Alpha hesaplama
            item_variances = beck_data.var(axis=0, ddof=1)
            total_variance = beck_data.sum(axis=1).var(ddof=1)
            n_items = len(beck_cols)
            cronbach_alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)

            print(f"\n[BECK DEPRESYON ÖLÇEĞİ]")
            print(f"  Madde sayısı: {n_items}")
            print(f"  Cronbach's α: {cronbach_alpha:.3f}")

            if cronbach_alpha >= 0.9:
                print(f"  Güvenilirlik: Mükemmel")
            elif cronbach_alpha >= 0.8:
                print(f"  Güvenilirlik: İyi")
            elif cronbach_alpha >= 0.7:
                print(f"  Güvenilirlik: Kabul edilebilir")
            else:
                print(f"  Güvenilirlik: Düşük")

def group_comparisons(df):
    """Gruplar arası karşılaştırmalar"""

    print("\n" + "="*60)
    print("GRUPLAR ARASI KARŞILAŞTIRMALAR")
    print("="*60)

    if 'Grup' not in df.columns:
        print("[!] Grup değişkeni bulunamadı")
        return

    # Beck skorları karşılaştırması
    if 'Beck_Total_Score' in df.columns:
        print("\n[BECK DEPRESYON SKORLARI]")

        diyabet_scores = df[df['Grup'] == 'Diyabet']['Beck_Total_Score'].dropna()
        kontrol_scores = df[df['Grup'] == 'Kontrol']['Beck_Total_Score'].dropna()

        print(f"\nDiyabet Grubu (n={len(diyabet_scores)}):")
        print(f"  Ortalama: {diyabet_scores.mean():.2f} ± {diyabet_scores.std():.2f}")
        print(f"  Medyan: {diyabet_scores.median():.2f}")

        print(f"\nKontrol Grubu (n={len(kontrol_scores)}):")
        print(f"  Ortalama: {kontrol_scores.mean():.2f} ± {kontrol_scores.std():.2f}")
        print(f"  Medyan: {kontrol_scores.median():.2f}")

        # T-test (normal dağılım varsayımı)
        t_stat, p_value = stats.ttest_ind(diyabet_scores, kontrol_scores)
        print(f"\nT-test sonucu:")
        print(f"  t = {t_stat:.3f}, p = {p_value:.4f}")

        if p_value < 0.05:
            print(f"  [✓] İstatistiksel olarak anlamlı fark var (p < 0.05)")
        else:
            print(f"  [x] İstatistiksel olarak anlamlı fark yok (p ≥ 0.05)")

        # Mann-Whitney U testi (non-parametrik)
        u_stat, p_value_mw = stats.mannwhitneyu(diyabet_scores, kontrol_scores)
        print(f"\nMann-Whitney U testi:")
        print(f"  U = {u_stat:.1f}, p = {p_value_mw:.4f}")

def create_visualizations(df):
    """Görselleştirmeler oluşturur"""

    print("\n" + "="*60)
    print("GÖRSELLEŞTİRMELER OLUŞTURULUYOR")
    print("="*60)

    import os
    os.makedirs('results/figures', exist_ok=True)

    # 1. Grup dağılımı pasta grafiği
    if 'Grup' in df.columns:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        grup_counts = df['Grup'].value_counts()
        colors = ['#FF6B6B', '#4ECDC4']
        ax.pie(grup_counts.values, labels=grup_counts.index, autopct='%1.1f%%',
               startangle=90, colors=colors)
        ax.set_title('Grup Dağılımı', fontsize=14, fontweight='bold')
        plt.savefig('results/figures/grup_dagilimi.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[✓] Grup dağılımı grafiği kaydedildi")

    # 2. Beck skorları histogram ve boxplot
    if 'Beck_Total_Score' in df.columns and 'Grup' in df.columns:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Histogram
        for grup in df['Grup'].unique():
            grup_data = df[df['Grup'] == grup]['Beck_Total_Score'].dropna()
            axes[0].hist(grup_data, alpha=0.6, label=grup, bins=15)
        axes[0].set_xlabel('Beck Depresyon Skoru')
        axes[0].set_ylabel('Frekans')
        axes[0].set_title('Beck Skorları Dağılımı')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # Boxplot
        df.boxplot(column='Beck_Total_Score', by='Grup', ax=axes[1])
        axes[1].set_xlabel('Grup')
        axes[1].set_ylabel('Beck Depresyon Skoru')
        axes[1].set_title('Gruplar Arası Beck Skorları Karşılaştırması')
        plt.suptitle('')  # Ana başlığı kaldır

        plt.tight_layout()
        plt.savefig('results/figures/beck_skorlari.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[✓] Beck skorları grafiği kaydedildi")

    # 3. Korelasyon matrisi
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        # Sadece önemli değişkenleri seç
        important_cols = [col for col in numeric_cols if
                         'Beck' in col or 'Yas' in col or 'Score' in col or 'Coded' in col][:15]

        if len(important_cols) > 1:
            corr_matrix = df[important_cols].corr()

            plt.figure(figsize=(12, 10))
            mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
            sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
                       cmap='coolwarm', center=0, square=True, linewidths=0.5,
                       cbar_kws={"shrink": 0.8})
            plt.title('Korelasyon Matrisi', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.savefig('results/figures/korelasyon_matrisi.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("[✓] Korelasyon matrisi kaydedildi")

def generate_descriptive_report(df, results):
    """Tanımlayıcı istatistik raporu oluşturur"""

    report = []
    report.append("="*60)
    report.append("TANIMLAYICI İSTATİSTİK RAPORU")
    report.append("="*60)
    report.append(f"\nAnaliz Tarihi: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"Toplam Katılımcı: {len(df)}")

    # Özet tablo oluştur
    summary_df = pd.DataFrame()

    # Sayısal değişkenler için özet
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if 'Score' in col or 'Yas' in col:
            summary_df.loc[col, 'N'] = df[col].notna().sum()
            summary_df.loc[col, 'Ortalama'] = df[col].mean()
            summary_df.loc[col, 'Std'] = df[col].std()
            summary_df.loc[col, 'Min'] = df[col].min()
            summary_df.loc[col, 'Q1'] = df[col].quantile(0.25)
            summary_df.loc[col, 'Medyan'] = df[col].median()
            summary_df.loc[col, 'Q3'] = df[col].quantile(0.75)
            summary_df.loc[col, 'Max'] = df[col].max()

    # Excel'e kaydet
    os.makedirs('results/tables', exist_ok=True)
    summary_df.to_excel('results/tables/descriptive_statistics.xlsx')
    print("\n[✓] Tanımlayıcı istatistikler: results/tables/descriptive_statistics.xlsx")

    # Text rapor kaydet
    with open('results/reports/descriptive_report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

    return summary_df

def main():
    """Ana fonksiyon"""

    print("="*60)
    print("TANIMLAYICI İSTATİSTİK ANALİZİ")
    print("="*60)

    # Veriyi yükle
    df = load_cleaned_data()
    if df is None:
        print("[!] Önce veri temizleme scriptini çalıştırın:")
        print("    python scripts/preprocessing/02_clean_data.py")
        return None

    # Analizler
    demo_results = demographic_analysis(df)
    scale_reliability_analysis(df)
    group_comparisons(df)
    create_visualizations(df)

    # Rapor oluştur
    os.makedirs('results/reports', exist_ok=True)
    summary_df = generate_descriptive_report(df, demo_results)

    print("\n" + "="*60)
    print("TANIMLAYICI ANALİZ TAMAMLANDI!")
    print("="*60)
    print("\nOluşturulan dosyalar:")
    print("  - results/figures/ (grafikler)")
    print("  - results/tables/ (tablolar)")
    print("  - results/reports/ (raporlar)")
    print("\nSonraki adım: python scripts/analysis/04_hypothesis_testing.py")

    return df, summary_df

if __name__ == "__main__":
    df, summary = main()