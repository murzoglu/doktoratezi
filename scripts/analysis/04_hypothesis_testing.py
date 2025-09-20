"""
04_hypothesis_testing.py
Hipotez testleri ve grup karşılaştırmaları
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import shapiro, levene, ttest_ind, mannwhitneyu, chi2_contingency
import pingouin as pg
import warnings
warnings.filterwarnings('ignore')

def load_data():
    """Temizlenmiş veriyi yükler"""
    try:
        df = pd.read_csv('data/cleaned/cleaned_dataset.csv')
        print(f"[✓] Veri yüklendi: {df.shape[0]} satır")
        return df
    except:
        print("[!] Veri bulunamadı. Önce temizleme scriptini çalıştırın.")
        return None

def normality_tests(df, variables):
    """Normallik testleri (Shapiro-Wilk)"""

    print("\n" + "="*60)
    print("NORMALLİK TESTLERİ (Shapiro-Wilk)")
    print("="*60)

    results = []

    for var in variables:
        if var in df.columns:
            # Genel normallik
            data = df[var].dropna()
            if len(data) >= 3:
                stat, p_value = shapiro(data)
                results.append({
                    'Variable': var,
                    'Group': 'All',
                    'N': len(data),
                    'Statistic': stat,
                    'p_value': p_value,
                    'Normal': 'Yes' if p_value > 0.05 else 'No'
                })

                # Grup bazında normallik
                if 'Grup' in df.columns:
                    for grup in df['Grup'].unique():
                        grup_data = df[df['Grup'] == grup][var].dropna()
                        if len(grup_data) >= 3:
                            stat, p_value = shapiro(grup_data)
                            results.append({
                                'Variable': var,
                                'Group': grup,
                                'N': len(grup_data),
                                'Statistic': stat,
                                'p_value': p_value,
                                'Normal': 'Yes' if p_value > 0.05 else 'No'
                            })

    results_df = pd.DataFrame(results)

    # Özet yazdır
    print("\nÖzet (p < 0.05 = Normal dağılım yok):")
    print("-"*40)
    for var in variables:
        if var in results_df['Variable'].values:
            var_results = results_df[results_df['Variable'] == var]
            print(f"\n{var}:")
            for _, row in var_results.iterrows():
                print(f"  {row['Group']:10} - p={row['p_value']:.4f} - {row['Normal']}")

    return results_df

def homogeneity_of_variance(df, variables):
    """Varyans homojenliği testi (Levene)"""

    print("\n" + "="*60)
    print("VARYANS HOMOJENLİĞİ TESTİ (Levene)")
    print("="*60)

    results = []

    if 'Grup' in df.columns:
        for var in variables:
            if var in df.columns:
                groups = []
                for grup in df['Grup'].unique():
                    grup_data = df[df['Grup'] == grup][var].dropna()
                    if len(grup_data) >= 2:
                        groups.append(grup_data)

                if len(groups) >= 2:
                    stat, p_value = levene(*groups)
                    results.append({
                        'Variable': var,
                        'Statistic': stat,
                        'p_value': p_value,
                        'Equal_Variance': 'Yes' if p_value > 0.05 else 'No'
                    })

                    print(f"{var}: p={p_value:.4f} - {'Eşit' if p_value > 0.05 else 'Eşit değil'}")

    return pd.DataFrame(results)

def independent_t_tests(df, variables):
    """Bağımsız örneklem t-testleri"""

    print("\n" + "="*60)
    print("BAĞIMSIZ ÖRNEKLEM T-TESTLERİ")
    print("="*60)

    results = []

    if 'Grup' not in df.columns:
        print("[!] Grup değişkeni bulunamadı")
        return None

    groups = df['Grup'].unique()
    if len(groups) != 2:
        print(f"[!] T-test için 2 grup gerekli. {len(groups)} grup bulundu.")
        return None

    group1_name = groups[0]
    group2_name = groups[1]

    for var in variables:
        if var in df.columns:
            group1_data = df[df['Grup'] == group1_name][var].dropna()
            group2_data = df[df['Grup'] == group2_name][var].dropna()

            if len(group1_data) >= 2 and len(group2_data) >= 2:
                # Parametrik t-test
                t_stat, p_value = ttest_ind(group1_data, group2_data)

                # Effect size (Cohen's d)
                pooled_std = np.sqrt(((len(group1_data)-1)*group1_data.std()**2 +
                                     (len(group2_data)-1)*group2_data.std()**2) /
                                    (len(group1_data) + len(group2_data) - 2))
                cohen_d = (group1_data.mean() - group2_data.mean()) / pooled_std if pooled_std > 0 else 0

                results.append({
                    'Variable': var,
                    f'{group1_name}_Mean': group1_data.mean(),
                    f'{group1_name}_SD': group1_data.std(),
                    f'{group1_name}_N': len(group1_data),
                    f'{group2_name}_Mean': group2_data.mean(),
                    f'{group2_name}_SD': group2_data.std(),
                    f'{group2_name}_N': len(group2_data),
                    't_statistic': t_stat,
                    'p_value': p_value,
                    'Cohen_d': cohen_d,
                    'Significant': 'Yes' if p_value < 0.05 else 'No'
                })

                print(f"\n{var}:")
                print(f"  {group1_name}: {group1_data.mean():.2f} ± {group1_data.std():.2f}")
                print(f"  {group2_name}: {group2_data.mean():.2f} ± {group2_data.std():.2f}")
                print(f"  t={t_stat:.3f}, p={p_value:.4f}, d={cohen_d:.3f}")
                print(f"  {'*** ANLAMLI ***' if p_value < 0.05 else 'Anlamlı değil'}")

    return pd.DataFrame(results)

def mann_whitney_tests(df, variables):
    """Mann-Whitney U testleri (non-parametrik)"""

    print("\n" + "="*60)
    print("MANN-WHITNEY U TESTLERİ (Non-parametrik)")
    print("="*60)

    results = []

    if 'Grup' not in df.columns:
        return None

    groups = df['Grup'].unique()
    if len(groups) != 2:
        return None

    group1_name = groups[0]
    group2_name = groups[1]

    for var in variables:
        if var in df.columns:
            group1_data = df[df['Grup'] == group1_name][var].dropna()
            group2_data = df[df['Grup'] == group2_name][var].dropna()

            if len(group1_data) >= 2 and len(group2_data) >= 2:
                u_stat, p_value = mannwhitneyu(group1_data, group2_data)

                # Effect size (rank biserial correlation)
                n1, n2 = len(group1_data), len(group2_data)
                r = 1 - (2*u_stat) / (n1 * n2)

                results.append({
                    'Variable': var,
                    f'{group1_name}_Median': group1_data.median(),
                    f'{group1_name}_IQR': group1_data.quantile(0.75) - group1_data.quantile(0.25),
                    f'{group2_name}_Median': group2_data.median(),
                    f'{group2_name}_IQR': group2_data.quantile(0.75) - group2_data.quantile(0.25),
                    'U_statistic': u_stat,
                    'p_value': p_value,
                    'Effect_size_r': r,
                    'Significant': 'Yes' if p_value < 0.05 else 'No'
                })

                print(f"\n{var}:")
                print(f"  {group1_name} Median: {group1_data.median():.2f}")
                print(f"  {group2_name} Median: {group2_data.median():.2f}")
                print(f"  U={u_stat:.1f}, p={p_value:.4f}, r={r:.3f}")

    return pd.DataFrame(results)

def chi_square_tests(df, categorical_vars):
    """Ki-kare testleri"""

    print("\n" + "="*60)
    print("Kİ-KARE TESTLERİ")
    print("="*60)

    results = []

    if 'Grup' not in df.columns:
        return None

    for var in categorical_vars:
        if var in df.columns:
            # Çapraz tablo oluştur
            crosstab = pd.crosstab(df[var], df['Grup'])

            # Ki-kare testi
            chi2, p_value, dof, expected = chi2_contingency(crosstab)

            # Cramér's V (effect size)
            n = crosstab.sum().sum()
            min_dim = min(crosstab.shape[0]-1, crosstab.shape[1]-1)
            cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0

            results.append({
                'Variable': var,
                'Chi2': chi2,
                'p_value': p_value,
                'df': dof,
                'Cramers_V': cramers_v,
                'Significant': 'Yes' if p_value < 0.05 else 'No'
            })

            print(f"\n{var}:")
            print(f"  χ²={chi2:.3f}, p={p_value:.4f}, V={cramers_v:.3f}")
            print(f"  {'*** ANLAMLI ***' if p_value < 0.05 else 'Anlamlı değil'}")

    return pd.DataFrame(results)

def correlation_analysis(df, variables):
    """Korelasyon analizleri"""

    print("\n" + "="*60)
    print("KORELASYON ANALİZLERİ")
    print("="*60)

    # Pearson korelasyonları
    numeric_vars = [v for v in variables if v in df.columns]
    if len(numeric_vars) >= 2:
        corr_matrix = df[numeric_vars].corr(method='pearson')

        # Anlamlı korelasyonları bul
        significant_corrs = []
        for i in range(len(numeric_vars)):
            for j in range(i+1, len(numeric_vars)):
                var1 = numeric_vars[i]
                var2 = numeric_vars[j]

                # Korelasyon ve p-değeri
                data1 = df[var1].dropna()
                data2 = df[var2].dropna()

                # Ortak veriye sahip gözlemler
                common_idx = data1.index.intersection(data2.index)
                if len(common_idx) >= 3:
                    r, p = stats.pearsonr(df.loc[common_idx, var1],
                                         df.loc[common_idx, var2])

                    if p < 0.05:
                        significant_corrs.append({
                            'Var1': var1,
                            'Var2': var2,
                            'r': r,
                            'p_value': p,
                            'N': len(common_idx)
                        })

        if significant_corrs:
            print("\nAnlamlı Korelasyonlar (p < 0.05):")
            print("-"*40)
            for corr in significant_corrs:
                print(f"{corr['Var1']} <-> {corr['Var2']}: r={corr['r']:.3f}, p={corr['p_value']:.4f}")

        return pd.DataFrame(significant_corrs)

    return None

def save_results(normality_df, homogeneity_df, ttest_df, mw_df, chi2_df, corr_df):
    """Sonuçları Excel'e kaydet"""

    import os
    os.makedirs('results/tables', exist_ok=True)

    with pd.ExcelWriter('results/tables/hypothesis_test_results.xlsx') as writer:
        if normality_df is not None and not normality_df.empty:
            normality_df.to_excel(writer, sheet_name='Normality_Tests', index=False)

        if homogeneity_df is not None and not homogeneity_df.empty:
            homogeneity_df.to_excel(writer, sheet_name='Homogeneity_Tests', index=False)

        if ttest_df is not None and not ttest_df.empty:
            ttest_df.to_excel(writer, sheet_name='T_Tests', index=False)

        if mw_df is not None and not mw_df.empty:
            mw_df.to_excel(writer, sheet_name='Mann_Whitney_Tests', index=False)

        if chi2_df is not None and not chi2_df.empty:
            chi2_df.to_excel(writer, sheet_name='Chi_Square_Tests', index=False)

        if corr_df is not None and not corr_df.empty:
            corr_df.to_excel(writer, sheet_name='Correlations', index=False)

    print("\n[✓] Sonuçlar kaydedildi: results/tables/hypothesis_test_results.xlsx")

def main():
    """Ana fonksiyon"""

    print("="*60)
    print("HİPOTEZ TESTLERİ VE GRUP KARŞILAŞTIRMALARI")
    print("="*60)

    # Veriyi yükle
    df = load_data()
    if df is None:
        return

    # Test edilecek değişkenler
    continuous_vars = ['Beck_Total_Score', 'Anne_Yas', 'Katilimci_Cocuk_Yas']
    categorical_vars = ['Cinsiyet_Coded', 'Medeni_Durum_Coded', 'Calisma_Durumu_Coded']

    # Mevcut değişkenleri filtrele
    continuous_vars = [v for v in continuous_vars if v in df.columns]
    categorical_vars = [v for v in categorical_vars if v in df.columns]

    # Beck sütunlarını ekle
    beck_cols = [col for col in df.columns if col.startswith('Beck_') and not col.endswith('_Score')]
    continuous_vars.extend(beck_cols[:5])  # İlk 5 Beck sorusu

    print(f"\nAnaliz edilecek sürekli değişkenler: {len(continuous_vars)}")
    print(f"Analiz edilecek kategorik değişkenler: {len(categorical_vars)}")

    # Testleri çalıştır
    normality_results = normality_tests(df, continuous_vars)
    homogeneity_results = homogeneity_of_variance(df, continuous_vars)
    ttest_results = independent_t_tests(df, continuous_vars)
    mw_results = mann_whitney_tests(df, continuous_vars)
    chi2_results = chi_square_tests(df, categorical_vars)
    corr_results = correlation_analysis(df, continuous_vars)

    # Sonuçları kaydet
    save_results(normality_results, homogeneity_results,
                ttest_results, mw_results, chi2_results, corr_results)

    print("\n" + "="*60)
    print("HİPOTEZ TESTLERİ TAMAMLANDI!")
    print("="*60)
    print("\nSonraki adım: python scripts/analysis/05_advanced_analysis.py")

if __name__ == "__main__":
    main()