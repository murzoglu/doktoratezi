"""
Demografik Veri Analizi
Kapsamlı demografik analiz ve grup karşılaştırmaları
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Grafik stil ayarları
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('husl')

def load_data():
    """Temizlenmiş veriyi yükle"""

    df = pd.read_csv('data/cleaned/cleaned_dataset.csv')
    print("="*70)
    print("DEMOGRAFİK VERİ ANALİZİ")
    print("="*70)
    print(f"\nVeri yüklendi: {df.shape[0]} katılımcı, {df.shape[1]} değişken")

    # Grup dağılımı
    if 'Grup' in df.columns:
        print(f"\nGrup dağılımı:")
        for grup, count in df['Grup'].value_counts().items():
            print(f"  {grup}: {count} ({count/len(df)*100:.1f}%)")

    return df

def analyze_age_demographics(df):
    """Yaş demografisi analizi"""

    print("\n" + "="*70)
    print("1. YAŞ DEMOGRAFİSİ")
    print("="*70)

    age_columns = {
        'Anne_Yas': 'Anne Yaşı',
        'Katilimci_Cocuk_Yas': 'Katılımcı Çocuk Yaşı',
        'Kardes_Yas': 'Kardeş Yaşı',
        'Es_Yas': 'Eş Yaşı'
    }

    results = {}

    for col, label in age_columns.items():
        if col in df.columns:
            data = df[col].dropna()
            if len(data) > 0:
                print(f"\n{label}:")
                print(f"  N: {len(data)}")
                print(f"  Ortalama: {data.mean():.1f} ± {data.std():.1f} yıl")
                print(f"  Medyan: {data.median():.1f} yıl")
                print(f"  Min-Max: {data.min():.1f} - {data.max():.1f} yıl")
                print(f"  25-75 persentil: {data.quantile(0.25):.1f} - {data.quantile(0.75):.1f}")

                results[col] = {
                    'mean': data.mean(),
                    'std': data.std(),
                    'median': data.median(),
                    'min': data.min(),
                    'max': data.max()
                }

                # Grup karşılaştırması
                if 'Grup' in df.columns:
                    print(f"\n  Grup karşılaştırması:")
                    for grup in df['Grup'].unique():
                        grup_data = df[df['Grup'] == grup][col].dropna()
                        if len(grup_data) > 0:
                            print(f"    {grup}: {grup_data.mean():.1f} ± {grup_data.std():.1f} (n={len(grup_data)})")

                    # T-test
                    if len(df['Grup'].unique()) == 2:
                        grup1_data = df[df['Grup'] == df['Grup'].unique()[0]][col].dropna()
                        grup2_data = df[df['Grup'] == df['Grup'].unique()[1]][col].dropna()

                        if len(grup1_data) > 0 and len(grup2_data) > 0:
                            t_stat, p_value = stats.ttest_ind(grup1_data, grup2_data)
                            print(f"  T-test: t={t_stat:.2f}, p={p_value:.3f}")
                            if p_value < 0.05:
                                print(f"  [!] Gruplar arasında anlamlı fark VAR")

    return results

def analyze_gender_distribution(df):
    """Cinsiyet dağılımı analizi"""

    print("\n" + "="*70)
    print("2. CİNSİYET DAĞILIMI")
    print("="*70)

    gender_columns = ['Katilimci_Cocuk_Cinsiyet', 'Kardes_Cinsiyet']

    for col in gender_columns:
        if col in df.columns:
            print(f"\n{col}:")
            value_counts = df[col].value_counts()
            for val, count in value_counts.items():
                print(f"  {val}: {count} ({count/df[col].notna().sum()*100:.1f}%)")

            # Grup bazında cinsiyet dağılımı
            if 'Grup' in df.columns:
                print(f"\n  Grup bazında dağılım:")
                crosstab = pd.crosstab(df['Grup'], df[col])
                print(crosstab)

                # Ki-kare testi
                chi2, p_value, dof, expected = stats.chi2_contingency(crosstab)
                print(f"\n  Ki-kare testi: chi2={chi2:.2f}, p={p_value:.3f}")
                if p_value < 0.05:
                    print(f"  [!] Gruplar arasında cinsiyet dağılımında anlamlı fark VAR")

def analyze_parental_status(df):
    """Ebeveyn durumu analizi"""

    print("\n" + "="*70)
    print("3. EBEVEYN DURUMU")
    print("="*70)

    # Medeni durum
    if 'Medeni_Durum' in df.columns:
        print("\nMedeni Durum:")
        med_durum = df['Medeni_Durum'].value_counts()
        for val, count in med_durum.items():
            print(f"  {val}: {count} ({count/df['Medeni_Durum'].notna().sum()*100:.1f}%)")

    # Eş sağ durumu
    if 'Es_Sag' in df.columns:
        print("\nEş Sağ Durumu:")
        es_sag = df['Es_Sag'].value_counts()
        for val, count in es_sag.items():
            print(f"  {val}: {count} ({count/df['Es_Sag'].notna().sum()*100:.1f}%)")

    # Anne antidepresan kullanımı
    if 'Anne_Antidepresan' in df.columns:
        print("\nAnne Antidepresan Kullanımı:")
        antidepresan = df['Anne_Antidepresan'].value_counts()
        for val, count in antidepresan.items():
            print(f"  {val}: {count} ({count/df['Anne_Antidepresan'].notna().sum()*100:.1f}%)")

        # Grup karşılaştırması
        if 'Grup' in df.columns:
            print("\n  Grup bazında antidepresan kullanımı:")
            crosstab = pd.crosstab(df['Grup'], df['Anne_Antidepresan'])
            print(crosstab)

            chi2, p_value, dof, expected = stats.chi2_contingency(crosstab)
            print(f"\n  Ki-kare testi: chi2={chi2:.2f}, p={p_value:.3f}")
            if p_value < 0.05:
                print(f"  [!] Gruplar arasında antidepresan kullanımında anlamlı fark VAR")

def analyze_education_employment(df):
    """Eğitim ve çalışma durumu analizi"""

    print("\n" + "="*70)
    print("4. EĞİTİM VE ÇALIŞMA DURUMU")
    print("="*70)

    # Eğitim durumu
    education_cols = ['Egitim_Durumu', 'Es_Egitim_Durumu']

    for col in education_cols:
        if col in df.columns:
            print(f"\n{col}:")
            edu_counts = df[col].value_counts()
            for val, count in edu_counts.items():
                print(f"  {val}: {count} ({count/df[col].notna().sum()*100:.1f}%)")

    # Çalışma durumu
    employment_cols = ['Calisma_Durumu', 'Es_Calisma_Durumu']

    for col in employment_cols:
        if col in df.columns:
            print(f"\n{col}:")
            emp_counts = df[col].value_counts()
            for val, count in emp_counts.items():
                print(f"  {val}: {count} ({count/df[col].notna().sum()*100:.1f}%)")

            # Grup karşılaştırması
            if 'Grup' in df.columns and col == 'Calisma_Durumu':
                print("\n  Grup bazında çalışma durumu:")
                crosstab = pd.crosstab(df['Grup'], df[col])
                print(crosstab)

                chi2, p_value, dof, expected = stats.chi2_contingency(crosstab)
                print(f"\n  Ki-kare testi: chi2={chi2:.2f}, p={p_value:.3f}")

def analyze_socioeconomic_status(df):
    """Sosyoekonomik durum analizi"""

    print("\n" + "="*70)
    print("5. SOSYOEKONOMİK DURUM")
    print("="*70)

    # Ev sahipliği
    if 'Ev_Sahipligi' in df.columns:
        print("\nEv Sahipliği:")
        ev_sahip = df['Ev_Sahipligi'].value_counts()
        for val, count in ev_sahip.items():
            print(f"  {val}: {count} ({count/df['Ev_Sahipligi'].notna().sum()*100:.1f}%)")

    # Ev oda sayısı
    if 'Ev_Oda_Sayisi' in df.columns:
        oda_sayisi = df['Ev_Oda_Sayisi'].dropna()
        if len(oda_sayisi) > 0:
            print(f"\nEv Oda Sayısı:")
            print(f"  Ortalama: {oda_sayisi.mean():.1f}")
            print(f"  Medyan: {oda_sayisi.median():.0f}")
            print(f"  Min-Max: {oda_sayisi.min():.0f} - {oda_sayisi.max():.0f}")

    # Araba sahipliği
    if 'Arabaniz_Var_mi' in df.columns:
        print("\nAraba Sahipliği:")
        araba = df['Arabaniz_Var_mi'].value_counts()
        for val, count in araba.items():
            print(f"  {val}: {count} ({count/df['Arabaniz_Var_mi'].notna().sum()*100:.1f}%)")

def analyze_health_status(df):
    """Sağlık durumu analizi"""

    print("\n" + "="*70)
    print("6. SAĞLIK DURUMU")
    print("="*70)

    # Engel durumu
    if 'Engel_Durumu' in df.columns:
        print("\nEngel Durumu:")
        engel = df['Engel_Durumu'].value_counts()
        for val, count in engel.items():
            print(f"  {val}: {count} ({count/df['Engel_Durumu'].notna().sum()*100:.1f}%)")

    # Eş engel durumu
    if 'Esiniz_Engel_Durumu' in df.columns:
        print("\nEş Engel Durumu:")
        es_engel = df['Esiniz_Engel_Durumu'].value_counts()
        for val, count in es_engel.items():
            print(f"  {val}: {count} ({count/df['Esiniz_Engel_Durumu'].notna().sum()*100:.1f}%)")

def analyze_demographic_depression_relationship(df):
    """Demografik değişkenler ve depresyon ilişkisi"""

    print("\n" + "="*70)
    print("7. DEMOGRAFİK DEĞİŞKENLER - DEPRESYON İLİŞKİSİ")
    print("="*70)

    if 'Beck_Total_Score' not in df.columns:
        print("[!] Beck toplam skoru bulunamadı")
        return

    # Anne yaşı - depresyon korelasyonu
    if 'Anne_Yas' in df.columns:
        anne_yas = df['Anne_Yas'].dropna()
        beck_scores = df.loc[anne_yas.index, 'Beck_Total_Score']

        valid_idx = beck_scores.notna()
        if valid_idx.sum() > 0:
            corr, p_value = stats.pearsonr(anne_yas[valid_idx], beck_scores[valid_idx])
            print(f"\nAnne Yaşı - Beck Skoru Korelasyonu:")
            print(f"  r = {corr:.3f}, p = {p_value:.3f}")
            if p_value < 0.05:
                print(f"  [!] Anlamlı korelasyon VAR")

    # Çalışma durumu - depresyon ilişkisi
    if 'Calisma_Durumu' in df.columns:
        print("\nÇalışma Durumu - Beck Skoru:")
        for durum in df['Calisma_Durumu'].unique():
            if pd.notna(durum):
                beck_mean = df[df['Calisma_Durumu'] == durum]['Beck_Total_Score'].mean()
                beck_std = df[df['Calisma_Durumu'] == durum]['Beck_Total_Score'].std()
                n = df[df['Calisma_Durumu'] == durum]['Beck_Total_Score'].notna().sum()
                print(f"  {durum}: {beck_mean:.1f} ± {beck_std:.1f} (n={n})")

        # T-test
        calisanlar = df[df['Calisma_Durumu'] == 1]['Beck_Total_Score'].dropna()
        calismayanlar = df[df['Calisma_Durumu'] == 0]['Beck_Total_Score'].dropna()

        if len(calisanlar) > 0 and len(calismayanlar) > 0:
            t_stat, p_value = stats.ttest_ind(calisanlar, calismayanlar)
            print(f"\n  T-test: t={t_stat:.2f}, p={p_value:.3f}")
            if p_value < 0.05:
                print(f"  [!] Çalışma durumu Beck skorunu anlamlı şekilde etkiliyor")

    # Anne antidepresan - çocuk depresyon ilişkisi
    if 'Anne_Antidepresan' in df.columns:
        print("\nAnne Antidepresan Kullanımı - Çocuk Beck Skoru:")
        for durum in df['Anne_Antidepresan'].unique():
            if pd.notna(durum):
                beck_mean = df[df['Anne_Antidepresan'] == durum]['Beck_Total_Score'].mean()
                beck_std = df[df['Anne_Antidepresan'] == durum]['Beck_Total_Score'].std()
                n = df[df['Anne_Antidepresan'] == durum]['Beck_Total_Score'].notna().sum()
                print(f"  {durum}: {beck_mean:.1f} ± {beck_std:.1f} (n={n})")

def create_demographic_visualizations(df):
    """Demografik görselleştirmeler"""

    import os
    os.makedirs('results/figures', exist_ok=True)

    # Figure 1: Yaş dağılımları
    age_cols = ['Anne_Yas', 'Katilimci_Cocuk_Yas', 'Kardes_Yas', 'Es_Yas']
    existing_age_cols = [col for col in age_cols if col in df.columns]

    if existing_age_cols:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()

        for i, col in enumerate(existing_age_cols[:4]):
            data = df[col].dropna()
            axes[i].hist(data, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
            axes[i].axvline(data.mean(), color='red', linestyle='--', label=f'Ort: {data.mean():.1f}')
            axes[i].set_xlabel('Yaş (yıl)')
            axes[i].set_ylabel('Frekans')
            axes[i].set_title(col.replace('_', ' '))
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)

        # Boş grafikleri gizle
        for i in range(len(existing_age_cols), 4):
            axes[i].axis('off')

        plt.suptitle('Yaş Dağılımları', fontsize=16)
        plt.tight_layout()
        plt.savefig('results/figures/age_distributions.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("\n[OK] Grafik kaydedildi: age_distributions.png")

    # Figure 2: Kategorik değişkenler
    if 'Grup' in df.columns:
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()

        categorical_vars = [
            ('Calisma_Durumu', 'Çalışma Durumu'),
            ('Anne_Antidepresan', 'Anne Antidepresan'),
            ('Ev_Sahipligi', 'Ev Sahipliği'),
            ('Arabaniz_Var_mi', 'Araba Sahipliği'),
            ('Engel_Durumu', 'Engel Durumu'),
            ('Medeni_Durum', 'Medeni Durum')
        ]

        plot_idx = 0
        for col, title in categorical_vars:
            if col in df.columns and plot_idx < 6:
                crosstab = pd.crosstab(df['Grup'], df[col], normalize='index') * 100
                crosstab.plot(kind='bar', ax=axes[plot_idx], color=['#FF6B6B', '#4ECDC4'])
                axes[plot_idx].set_title(title)
                axes[plot_idx].set_xlabel('Grup')
                axes[plot_idx].set_ylabel('Yüzde (%)')
                axes[plot_idx].legend(title=col.replace('_', ' '))
                axes[plot_idx].set_xticklabels(axes[plot_idx].get_xticklabels(), rotation=0)
                plot_idx += 1

        # Boş grafikleri gizle
        for i in range(plot_idx, 6):
            axes[i].axis('off')

        plt.suptitle('Grup Bazında Demografik Değişkenler', fontsize=16)
        plt.tight_layout()
        plt.savefig('results/figures/demographic_by_group.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Grafik kaydedildi: demographic_by_group.png")

    # Figure 3: Depresyon ve demografik faktörler
    if 'Beck_Total_Score' in df.columns:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # Anne yaşı vs Beck skoru
        if 'Anne_Yas' in df.columns:
            axes[0, 0].scatter(df['Anne_Yas'], df['Beck_Total_Score'], alpha=0.5)
            axes[0, 0].set_xlabel('Anne Yaşı')
            axes[0, 0].set_ylabel('Beck Skoru')
            axes[0, 0].set_title('Anne Yaşı - Depresyon İlişkisi')
            axes[0, 0].grid(True, alpha=0.3)

        # Çalışma durumu vs Beck skoru
        if 'Calisma_Durumu' in df.columns:
            data_to_plot = []
            labels = []
            for durum in df['Calisma_Durumu'].unique():
                if pd.notna(durum):
                    data_to_plot.append(df[df['Calisma_Durumu'] == durum]['Beck_Total_Score'].dropna())
                    labels.append(f"Durum {durum}")

            if data_to_plot:
                axes[0, 1].boxplot(data_to_plot, labels=labels)
                axes[0, 1].set_ylabel('Beck Skoru')
                axes[0, 1].set_title('Çalışma Durumu - Depresyon')
                axes[0, 1].grid(True, alpha=0.3)

        # Anne antidepresan vs Beck skoru
        if 'Anne_Antidepresan' in df.columns:
            data_to_plot = []
            labels = []
            for durum in df['Anne_Antidepresan'].unique():
                if pd.notna(durum):
                    data_to_plot.append(df[df['Anne_Antidepresan'] == durum]['Beck_Total_Score'].dropna())
                    labels.append(f"Antidepresan {durum}")

            if data_to_plot:
                axes[1, 0].boxplot(data_to_plot, labels=labels)
                axes[1, 0].set_ylabel('Beck Skoru')
                axes[1, 0].set_title('Anne Antidepresan - Çocuk Depresyon')
                axes[1, 0].grid(True, alpha=0.3)

        # Çocuk yaşı vs Beck skoru
        if 'Katilimci_Cocuk_Yas' in df.columns:
            axes[1, 1].scatter(df['Katilimci_Cocuk_Yas'], df['Beck_Total_Score'], alpha=0.5)
            axes[1, 1].set_xlabel('Çocuk Yaşı')
            axes[1, 1].set_ylabel('Beck Skoru')
            axes[1, 1].set_title('Çocuk Yaşı - Depresyon İlişkisi')
            axes[1, 1].grid(True, alpha=0.3)

        plt.suptitle('Demografik Faktörler ve Depresyon İlişkisi', fontsize=16)
        plt.tight_layout()
        plt.savefig('results/figures/demographics_depression_relationship.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("[OK] Grafik kaydedildi: demographics_depression_relationship.png")

def save_demographic_results(df, results):
    """Demografik analiz sonuçlarını kaydet"""

    import os
    os.makedirs('results/tables', exist_ok=True)

    with pd.ExcelWriter('results/tables/demographic_analysis.xlsx') as writer:

        # Genel özet
        summary_data = {
            'Toplam Katılımcı': [len(df)],
            'Ortalama Anne Yaşı': [df['Anne_Yas'].mean() if 'Anne_Yas' in df.columns else None],
            'Ortalama Çocuk Yaşı': [df['Katilimci_Cocuk_Yas'].mean() if 'Katilimci_Cocuk_Yas' in df.columns else None],
            'Çalışan Anne Oranı': [(df['Calisma_Durumu'] == 1).sum() / df['Calisma_Durumu'].notna().sum() * 100 if 'Calisma_Durumu' in df.columns else None],
            'Anne Antidepresan Oranı': [(df['Anne_Antidepresan'] == 1).sum() / df['Anne_Antidepresan'].notna().sum() * 100 if 'Anne_Antidepresan' in df.columns else None]
        }

        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Özet', index=False)

        # Yaş istatistikleri
        age_stats = []
        for col in ['Anne_Yas', 'Katilimci_Cocuk_Yas', 'Kardes_Yas', 'Es_Yas']:
            if col in df.columns:
                data = df[col].dropna()
                if len(data) > 0:
                    age_stats.append({
                        'Değişken': col,
                        'N': len(data),
                        'Ortalama': data.mean(),
                        'Std': data.std(),
                        'Medyan': data.median(),
                        'Min': data.min(),
                        'Max': data.max()
                    })

        if age_stats:
            age_df = pd.DataFrame(age_stats)
            age_df.to_excel(writer, sheet_name='Yaş_İstatistikleri', index=False)

        # Grup karşılaştırmaları
        if 'Grup' in df.columns:
            # Yaş karşılaştırması
            group_age_stats = []
            for col in ['Anne_Yas', 'Katilimci_Cocuk_Yas', 'Kardes_Yas']:
                if col in df.columns:
                    for grup in df['Grup'].unique():
                        data = df[df['Grup'] == grup][col].dropna()
                        if len(data) > 0:
                            group_age_stats.append({
                                'Değişken': col,
                                'Grup': grup,
                                'N': len(data),
                                'Ortalama': data.mean(),
                                'Std': data.std()
                            })

            if group_age_stats:
                group_df = pd.DataFrame(group_age_stats)
                group_df.to_excel(writer, sheet_name='Grup_Karşılaştırma', index=False)

    print("\n[OK] Sonuçlar kaydedildi: results/tables/demographic_analysis.xlsx")

def generate_demographic_report(df):
    """Demografik analiz raporu oluştur"""

    report = []
    report.append("="*70)
    report.append("DEMOGRAFİK ANALİZ RAPORU")
    report.append("="*70)
    report.append(f"\nTarih: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"Toplam Katılımcı: {len(df)}")

    # Grup dağılımı
    if 'Grup' in df.columns:
        report.append("\nGRUP DAĞILIMI:")
        for grup, count in df['Grup'].value_counts().items():
            report.append(f"  {grup}: {count} ({count/len(df)*100:.1f}%)")

    # Yaş ortalamaları
    report.append("\nYAŞ ORTALAMALARI:")
    for col, label in [('Anne_Yas', 'Anne'), ('Katilimci_Cocuk_Yas', 'Çocuk'),
                       ('Kardes_Yas', 'Kardeş'), ('Es_Yas', 'Eş')]:
        if col in df.columns:
            mean_age = df[col].mean()
            if pd.notna(mean_age):
                report.append(f"  {label}: {mean_age:.1f} yıl")

    # Aile yapısı
    if 'Cocuk_Sayisi' in df.columns:
        report.append(f"\nOrtalama Çocuk Sayısı: {df['Cocuk_Sayisi'].mean():.1f}")

    # Çalışma durumu
    if 'Calisma_Durumu' in df.columns:
        calisan = (df['Calisma_Durumu'] == 1).sum()
        total = df['Calisma_Durumu'].notna().sum()
        if total > 0:
            report.append(f"\nÇalışan Anne Oranı: %{calisan/total*100:.1f}")

    # Anne antidepresan kullanımı
    if 'Anne_Antidepresan' in df.columns:
        kullanan = (df['Anne_Antidepresan'] == 1).sum()
        total = df['Anne_Antidepresan'].notna().sum()
        if total > 0:
            report.append(f"Anne Antidepresan Kullanım Oranı: %{kullanan/total*100:.1f}")

    # Raporu kaydet
    with open('results/demographic_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

    print("\n[OK] Rapor kaydedildi: results/demographic_analysis_report.txt")

    return report

def main():
    """Ana fonksiyon"""

    try:
        # 1. Veriyi yükle
        df = load_data()

        # 2. Yaş demografisi
        age_results = analyze_age_demographics(df)

        # 3. Cinsiyet dağılımı
        analyze_gender_distribution(df)

        # 4. Ebeveyn durumu
        analyze_parental_status(df)

        # 5. Eğitim ve çalışma durumu
        analyze_education_employment(df)

        # 6. Sosyoekonomik durum
        analyze_socioeconomic_status(df)

        # 7. Sağlık durumu
        analyze_health_status(df)

        # 8. Demografik-depresyon ilişkisi
        analyze_demographic_depression_relationship(df)

        # 9. Görselleştirmeler
        create_demographic_visualizations(df)

        # 10. Sonuçları kaydet
        save_demographic_results(df, age_results)

        # 11. Rapor oluştur
        report = generate_demographic_report(df)

        print("\n" + "="*70)
        print("DEMOGRAFİK ANALİZ TAMAMLANDI!")
        print("="*70)

        print("\n📊 ÖNEMLİ BULGULAR:")

        # Anne yaşı
        if 'Anne_Yas' in df.columns:
            anne_yas_mean = df['Anne_Yas'].mean()
            print(f"\n• Ortalama anne yaşı: {anne_yas_mean:.1f} yıl")
            if anne_yas_mean < 35:
                print("  → Genç anne profili")
            elif anne_yas_mean > 40:
                print("  → Olgun anne profili")

        # Çocuk yaşı
        if 'Katilimci_Cocuk_Yas' in df.columns:
            cocuk_yas_mean = df['Katilimci_Cocuk_Yas'].mean()
            print(f"\n• Ortalama çocuk yaşı: {cocuk_yas_mean:.1f} yıl")
            if cocuk_yas_mean < 10:
                print("  → Çoğunlukla ilkokul çağı")
            elif cocuk_yas_mean < 14:
                print("  → Çoğunlukla ortaokul çağı")
            else:
                print("  → Çoğunlukla lise çağı")

        # Çalışma durumu
        if 'Calisma_Durumu' in df.columns:
            calisan_oran = (df['Calisma_Durumu'] == 1).sum() / df['Calisma_Durumu'].notna().sum() * 100
            print(f"\n• Çalışan anne oranı: %{calisan_oran:.1f}")
            if calisan_oran < 30:
                print("  → Düşük istihdam oranı")
            elif calisan_oran > 50:
                print("  → Yüksek istihdam oranı")

        # Anne antidepresan
        if 'Anne_Antidepresan' in df.columns:
            antidepresan_oran = (df['Anne_Antidepresan'] == 1).sum() / df['Anne_Antidepresan'].notna().sum() * 100
            if antidepresan_oran > 10:
                print(f"\n• Anne antidepresan kullanım oranı yüksek: %{antidepresan_oran:.1f}")

        print("\n📁 Detaylı sonuçlar için:")
        print("• results/tables/demographic_analysis.xlsx")
        print("• results/demographic_analysis_report.txt")
        print("• results/figures/ klasöründeki grafikler")

    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()