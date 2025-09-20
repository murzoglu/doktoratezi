"""
Kardeş İlişkileri Anketi Analizi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def load_and_explore_sibling_data():
    """Kardeş ilişkileri verilerini yükle ve incele"""

    print("="*60)
    print("KARDEŞ İLİŞKİLERİ ANKETİ ANALİZİ")
    print("="*60)

    # Temizlenmiş veriyi yükle
    df = pd.read_csv('data/cleaned/cleaned_dataset.csv')
    print(f"\nVeri yüklendi: {df.shape[0]} katılımcı, {df.shape[1]} değişken")

    # Kardeş ile ilgili sütunları bul
    print("\n[1] KARDEŞ İLE İLGİLİ SÜTUNLAR")
    print("-"*40)

    sibling_cols = []
    kardes_keywords = ['kardes', 'kardesi', 'sibling', 'brother', 'sister']

    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in kardes_keywords):
            sibling_cols.append(col)

    print(f"Kardeş ile ilgili {len(sibling_cols)} sütun bulundu:")
    for col in sibling_cols:
        non_null = df[col].notna().sum()
        print(f"  - {col}: {non_null} veri")

    # Kardeş sayısı analizi
    if 'Cocuk_Sayisi' in df.columns:
        print("\n[2] AİLE YAPISI ANALİZİ")
        print("-"*40)

        cocuk_sayisi = df['Cocuk_Sayisi'].value_counts().sort_index()
        print("\nÇocuk sayısı dağılımı:")
        for sayi, count in cocuk_sayisi.items():
            print(f"  {sayi} çocuk: {count} aile ({count/len(df)*100:.1f}%)")

        # Kardeş varlığı
        df['Kardes_Var'] = df['Cocuk_Sayisi'] > 1
        kardes_dagilim = df['Kardes_Var'].value_counts()
        print(f"\nKardeş varlığı:")
        print(f"  Kardeşi olan: {kardes_dagilim.get(True, 0)} ({kardes_dagilim.get(True, 0)/len(df)*100:.1f}%)")
        print(f"  Tek çocuk: {kardes_dagilim.get(False, 0)} ({kardes_dagilim.get(False, 0)/len(df)*100:.1f}%)")

    # Kardeş yaş ve cinsiyet analizi
    if 'Kardes_Yas' in df.columns:
        print("\n[3] KARDEŞ DEMOGRAFİK BİLGİLER")
        print("-"*40)

        kardes_yas = df['Kardes_Yas'].dropna()
        if len(kardes_yas) > 0:
            print(f"\nKardeş yaşı istatistikleri:")
            print(f"  Ortalama: {kardes_yas.mean():.1f} yıl")
            print(f"  Medyan: {kardes_yas.median():.1f} yıl")
            print(f"  Min-Max: {kardes_yas.min():.1f} - {kardes_yas.max():.1f} yıl")

    if 'Kardes_Cinsiyet' in df.columns:
        kardes_cinsiyet = df['Kardes_Cinsiyet'].value_counts()
        print(f"\nKardeş cinsiyet dağılımı:")
        for cinsiyet, count in kardes_cinsiyet.items():
            print(f"  {cinsiyet}: {count} ({count/df['Kardes_Cinsiyet'].notna().sum()*100:.1f}%)")

    # Kardeş ilişkileri ölçeği varsa analiz et
    # EMBU'da kardeş ilişkileri soruları olabilir
    kardes_olcek_cols = []
    for col in df.columns:
        if ('kardes' in col.lower() or 'sibling' in col.lower()) and \
           any(x in col.lower() for x in ['skor', 'score', 'puan', 'olcek', 'scale']):
            kardes_olcek_cols.append(col)

    if kardes_olcek_cols:
        print("\n[4] KARDEŞ İLİŞKİLERİ ÖLÇEĞİ")
        print("-"*40)
        print(f"{len(kardes_olcek_cols)} ölçek sorusu bulundu")
        for col in kardes_olcek_cols:
            print(f"  - {col}")

    return df, sibling_cols

def analyze_sibling_relationships_by_group(df):
    """Gruplara göre kardeş ilişkilerini analiz et"""

    print("\n[5] GRUP KARŞILAŞTIRMALARI")
    print("-"*40)

    if 'Grup' not in df.columns:
        print("[!] Grup değişkeni bulunamadı")
        return None

    # Grup dağılımı
    print("\nGrup dağılımı:")
    for grup, count in df['Grup'].value_counts().items():
        print(f"  {grup}: {count} katılımcı")

    results = {}

    # Kardeş varlığı karşılaştırması
    if 'Kardes_Var' in df.columns:
        print("\n[5.1] Kardeş Varlığı - Grup Karşılaştırması")

        crosstab = pd.crosstab(df['Grup'], df['Kardes_Var'])
        print("\nÇapraz tablo:")
        print(crosstab)

        # Ki-kare testi
        chi2, p_value, dof, expected = stats.chi2_contingency(crosstab)
        print(f"\nKi-kare testi:")
        print(f"  chi2 = {chi2:.3f}, p = {p_value:.3f}")

        if p_value < 0.05:
            print("  [OK] Gruplar arasında anlamlı fark VAR")
        else:
            print("  - Gruplar arasında anlamlı fark YOK")

        results['kardes_varligi_chi2'] = {'chi2': chi2, 'p_value': p_value}

    # Çocuk sayısı karşılaştırması
    if 'Cocuk_Sayisi' in df.columns:
        print("\n[5.2] Çocuk Sayısı - Grup Karşılaştırması")

        for grup in df['Grup'].unique():
            grup_data = df[df['Grup'] == grup]['Cocuk_Sayisi'].dropna()
            if len(grup_data) > 0:
                print(f"\n{grup} grubu:")
                print(f"  Ortalama çocuk sayısı: {grup_data.mean():.2f}")
                print(f"  Medyan: {grup_data.median():.1f}")

        # T-test veya Mann-Whitney U
        diyabet = df[df['Grup'] == 'Diyabet']['Cocuk_Sayisi'].dropna()
        kontrol = df[df['Grup'] == 'Kontrol']['Cocuk_Sayisi'].dropna()

        if len(diyabet) > 0 and len(kontrol) > 0:
            # Normallik testi
            _, p_norm_d = stats.shapiro(diyabet) if len(diyabet) >= 3 else (None, 0)
            _, p_norm_k = stats.shapiro(kontrol) if len(kontrol) >= 3 else (None, 0)

            if p_norm_d and p_norm_k and p_norm_d > 0.05 and p_norm_k > 0.05:
                # T-test
                t_stat, p_value = stats.ttest_ind(diyabet, kontrol)
                print(f"\nT-test: t = {t_stat:.3f}, p = {p_value:.3f}")
                test_name = 't-test'
            else:
                # Mann-Whitney U
                u_stat, p_value = stats.mannwhitneyu(diyabet, kontrol)
                print(f"\nMann-Whitney U: U = {u_stat:.1f}, p = {p_value:.3f}")
                test_name = 'Mann-Whitney U'

            if p_value < 0.05:
                print(f"  [OK] Çocuk sayısında anlamlı fark VAR")
            else:
                print(f"  - Çocuk sayısında anlamlı fark YOK")

            results['cocuk_sayisi'] = {'test': test_name, 'p_value': p_value}

    # Kardeş yaşı karşılaştırması
    if 'Kardes_Yas' in df.columns:
        print("\n[5.3] Kardeş Yaşı - Grup Karşılaştırması")

        for grup in df['Grup'].unique():
            grup_data = df[df['Grup'] == grup]['Kardes_Yas'].dropna()
            if len(grup_data) > 0:
                print(f"\n{grup} grubu kardeş yaşları:")
                print(f"  Ortalama: {grup_data.mean():.1f} yıl")
                print(f"  Medyan: {grup_data.median():.1f} yıl")

        diyabet_yas = df[df['Grup'] == 'Diyabet']['Kardes_Yas'].dropna()
        kontrol_yas = df[df['Grup'] == 'Kontrol']['Kardes_Yas'].dropna()

        if len(diyabet_yas) > 0 and len(kontrol_yas) > 0:
            t_stat, p_value = stats.ttest_ind(diyabet_yas, kontrol_yas)
            print(f"\nT-test: t = {t_stat:.3f}, p = {p_value:.3f}")

            if p_value < 0.05:
                print(f"  [OK] Kardeş yaşlarında anlamlı fark VAR")
            else:
                print(f"  - Kardeş yaşlarında anlamlı fark YOK")

            results['kardes_yasi'] = {'t_stat': t_stat, 'p_value': p_value}

    return results

def analyze_sibling_impact_on_depression(df):
    """Kardeş varlığının depresyon üzerindeki etkisini analiz et"""

    print("\n[6] KARDEŞ VARLIĞI - DEPRESYON İLİŞKİSİ")
    print("-"*40)

    if 'Beck_Total_Score' not in df.columns:
        print("[!] Beck toplam skoru bulunamadı")
        return None

    if 'Kardes_Var' not in df.columns:
        print("[!] Kardeş varlığı değişkeni bulunamadı")
        return None

    # Kardeş varlığına göre Beck skorları
    print("\nBeck Depresyon Skorları - Kardeş Varlığı:")

    kardes_var = df[df['Kardes_Var'] == True]['Beck_Total_Score'].dropna()
    kardes_yok = df[df['Kardes_Var'] == False]['Beck_Total_Score'].dropna()

    if len(kardes_var) > 0:
        print(f"\nKardeşi olanlar (n={len(kardes_var)}):")
        print(f"  Ortalama: {kardes_var.mean():.2f}")
        print(f"  Medyan: {kardes_var.median():.1f}")
        print(f"  Min-Max: {kardes_var.min():.0f} - {kardes_var.max():.0f}")

    if len(kardes_yok) > 0:
        print(f"\nTek çocuklar (n={len(kardes_yok)}):")
        print(f"  Ortalama: {kardes_yok.mean():.2f}")
        print(f"  Medyan: {kardes_yok.median():.1f}")
        print(f"  Min-Max: {kardes_yok.min():.0f} - {kardes_yok.max():.0f}")

    # T-test
    if len(kardes_var) > 0 and len(kardes_yok) > 0:
        t_stat, p_value = stats.ttest_ind(kardes_var, kardes_yok)
        print(f"\nT-test: t = {t_stat:.3f}, p = {p_value:.3f}")

        # Cohen's d
        pooled_std = np.sqrt(((len(kardes_var)-1)*kardes_var.std()**2 +
                              (len(kardes_yok)-1)*kardes_yok.std()**2) /
                             (len(kardes_var) + len(kardes_yok) - 2))
        cohens_d = (kardes_var.mean() - kardes_yok.mean()) / pooled_std
        print(f"Cohen's d: {cohens_d:.3f}")

        if p_value < 0.05:
            print("[OK] Kardeş varlığı Beck skorlarını anlamlı şekilde etkiliyor")
        else:
            print("- Kardeş varlığının Beck skorlarına anlamlı etkisi yok")

    # Grup bazında analiz
    print("\n[6.1] Grup Bazında Kardeş-Depresyon İlişkisi")

    for grup in df['Grup'].unique():
        grup_df = df[df['Grup'] == grup]

        kardes_var = grup_df[grup_df['Kardes_Var'] == True]['Beck_Total_Score'].dropna()
        kardes_yok = grup_df[grup_df['Kardes_Var'] == False]['Beck_Total_Score'].dropna()

        if len(kardes_var) > 0 and len(kardes_yok) > 0:
            print(f"\n{grup} Grubu:")
            print(f"  Kardeşi olanlar: {kardes_var.mean():.2f} (n={len(kardes_var)})")
            print(f"  Tek çocuklar: {kardes_yok.mean():.2f} (n={len(kardes_yok)})")

            t_stat, p_value = stats.ttest_ind(kardes_var, kardes_yok)
            print(f"  T-test: p = {p_value:.3f}")

def create_visualizations(df):
    """Görselleştirmeler oluştur"""

    import os
    os.makedirs('results/figures', exist_ok=True)

    # Stil ayarları
    plt.style.use('seaborn-v0_8-darkgrid')
    colors = ['#FF6B6B', '#4ECDC4']

    # Figure 1: Kardeş varlığı dağılımı
    if 'Kardes_Var' in df.columns and 'Grup' in df.columns:
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Genel dağılım
        kardes_counts = df['Kardes_Var'].value_counts()
        axes[0].pie(kardes_counts.values,
                   labels=['Kardeşi Var' if x else 'Tek Çocuk' for x in kardes_counts.index],
                   autopct='%1.1f%%',
                   colors=colors)
        axes[0].set_title('Kardeş Varlığı Dağılımı')

        # Grup bazında
        crosstab = pd.crosstab(df['Grup'], df['Kardes_Var'], normalize='index') * 100
        crosstab.plot(kind='bar', ax=axes[1], color=colors)
        axes[1].set_title('Gruplara Göre Kardeş Varlığı (%)')
        axes[1].set_xlabel('Grup')
        axes[1].set_ylabel('Yüzde (%)')
        axes[1].legend(['Tek Çocuk', 'Kardeşi Var'])
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)

        plt.tight_layout()
        plt.savefig('results/figures/sibling_distribution.png', dpi=300)
        plt.close()
        print("\n[OK] Grafik kaydedildi: sibling_distribution.png")

    # Figure 2: Kardeş varlığı ve Beck skorları
    if 'Kardes_Var' in df.columns and 'Beck_Total_Score' in df.columns:
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Box plot
        data_to_plot = [df[df['Kardes_Var']==False]['Beck_Total_Score'].dropna(),
                       df[df['Kardes_Var']==True]['Beck_Total_Score'].dropna()]
        axes[0].boxplot(data_to_plot, labels=['Tek Çocuk', 'Kardeşi Var'])
        axes[0].set_ylabel('Beck Toplam Skor')
        axes[0].set_title('Kardeş Varlığına Göre Depresyon Skorları')
        axes[0].grid(True, alpha=0.3)

        # Grup bazında ortalamalar
        if 'Grup' in df.columns:
            grup_means = df.groupby(['Grup', 'Kardes_Var'])['Beck_Total_Score'].mean().unstack()
            grup_means.plot(kind='bar', ax=axes[1], color=colors)
            axes[1].set_title('Grup ve Kardeş Varlığına Göre Ortalama Beck Skorları')
            axes[1].set_xlabel('Grup')
            axes[1].set_ylabel('Ortalama Beck Skoru')
            axes[1].legend(['Tek Çocuk', 'Kardeşi Var'])
            axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)

        plt.tight_layout()
        plt.savefig('results/figures/sibling_depression_relationship.png', dpi=300)
        plt.close()
        print("[OK] Grafik kaydedildi: sibling_depression_relationship.png")

    # Figure 3: Çocuk sayısı dağılımı
    if 'Cocuk_Sayisi' in df.columns:
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))

        cocuk_dagilim = df['Cocuk_Sayisi'].value_counts().sort_index()
        cocuk_dagilim.plot(kind='bar', color='#4ECDC4', ax=ax)
        ax.set_title('Ailelerdeki Çocuk Sayısı Dağılımı')
        ax.set_xlabel('Çocuk Sayısı')
        ax.set_ylabel('Aile Sayısı')
        ax.grid(True, alpha=0.3)

        # Değerleri bar üzerine yaz
        for i, v in enumerate(cocuk_dagilim.values):
            ax.text(i, v + 1, str(v), ha='center')

        plt.tight_layout()
        plt.savefig('results/figures/children_count_distribution.png', dpi=300)
        plt.close()
        print("[OK] Grafik kaydedildi: children_count_distribution.png")

def save_results(df, results):
    """Analiz sonuçlarını kaydet"""

    import os
    os.makedirs('results/tables', exist_ok=True)

    # Excel'e kaydet
    with pd.ExcelWriter('results/tables/sibling_analysis_results.xlsx') as writer:

        # Genel özet
        summary = pd.DataFrame({
            'Metrik': ['Toplam Katılımcı', 'Kardeşi Olan', 'Tek Çocuk',
                       'Ortalama Çocuk Sayısı', 'Ortalama Kardeş Yaşı'],
            'Değer': [
                len(df),
                df['Kardes_Var'].sum() if 'Kardes_Var' in df.columns else 'N/A',
                (~df['Kardes_Var']).sum() if 'Kardes_Var' in df.columns else 'N/A',
                df['Cocuk_Sayisi'].mean() if 'Cocuk_Sayisi' in df.columns else 'N/A',
                df['Kardes_Yas'].mean() if 'Kardes_Yas' in df.columns else 'N/A'
            ]
        })
        summary.to_excel(writer, sheet_name='Özet', index=False)

        # Grup karşılaştırmaları
        if 'Grup' in df.columns and 'Kardes_Var' in df.columns:
            crosstab = pd.crosstab(df['Grup'], df['Kardes_Var'], margins=True)
            crosstab.to_excel(writer, sheet_name='Grup_Kardeş_Çapraz')

        # Kardeş-Depresyon ilişkisi
        if 'Kardes_Var' in df.columns and 'Beck_Total_Score' in df.columns:
            kardes_beck = df.groupby('Kardes_Var')['Beck_Total_Score'].agg(['mean', 'median', 'std', 'count'])
            kardes_beck.to_excel(writer, sheet_name='Kardeş_Beck_İlişkisi')

    print("\n[OK] Sonuçlar kaydedildi: results/tables/sibling_analysis_results.xlsx")

def main():
    """Ana fonksiyon"""

    try:
        # 1. Veriyi yükle ve incele
        df, sibling_cols = load_and_explore_sibling_data()

        # 2. Grup karşılaştırmaları
        results = analyze_sibling_relationships_by_group(df)

        # 3. Kardeş-Depresyon ilişkisi
        analyze_sibling_impact_on_depression(df)

        # 4. Görselleştirmeler
        create_visualizations(df)

        # 5. Sonuçları kaydet
        save_results(df, results)

        print("\n" + "="*60)
        print("KARDEŞ İLİŞKİLERİ ANALİZİ TAMAMLANDI!")
        print("="*60)

        print("\nÖNEMLİ BULGULAR:")

        # Özet bulgular
        if 'Kardes_Var' in df.columns:
            kardes_var_pct = df['Kardes_Var'].sum() / len(df) * 100
            print(f"• Katılımcıların %{kardes_var_pct:.1f}'inin kardeşi var")

        if 'Beck_Total_Score' in df.columns and 'Kardes_Var' in df.columns:
            kardes_beck = df[df['Kardes_Var']==True]['Beck_Total_Score'].mean()
            tek_beck = df[df['Kardes_Var']==False]['Beck_Total_Score'].mean()

            if pd.notna(kardes_beck) and pd.notna(tek_beck):
                if kardes_beck < tek_beck:
                    print(f"• Kardeşi olanların depresyon skoru daha düşük ({kardes_beck:.1f} vs {tek_beck:.1f})")
                else:
                    print(f"• Tek çocukların depresyon skoru daha düşük ({tek_beck:.1f} vs {kardes_beck:.1f})")

        print("\nDetaylı sonuçlar için:")
        print("• results/tables/sibling_analysis_results.xlsx")
        print("• results/figures/ klasöründeki grafikler")

    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()