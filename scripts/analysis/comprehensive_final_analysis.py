"""
KAPSAMLı NİHAİ ANALİZ
=====================
Düzeltilmiş Beck skorları ile tüm analizlerin yeniden yapılması
Protokolde belirtilen araştırma amaçlarına yönelik detaylı istatistiksel analiz

Araştırma Amaçları:
1. Diyabetli çocukların annelerinde depresyon düzeyini değerlendirme
2. Kardeş ilişkilerini analiz etme
3. Ebeveynlik tutumlarını inceleme
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import (
    shapiro, normaltest, jarque_bera,  # Normallik testleri
    ttest_ind, mannwhitneyu,           # Bağımsız grup karşılaştırmaları
    ttest_rel, wilcoxon,                # Eşleştirilmiş karşılaştırmalar
    chi2_contingency, fisher_exact,     # Kategorik değişkenler
    pearsonr, spearmanr,                # Korelasyon
    f_oneway, kruskal                   # Çoklu grup karşılaştırmaları
)
from statsmodels.stats.power import ttest_power
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime
import json

# Matplotlib ayarları
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['figure.figsize'] = (12, 8)
sns.set_style("whitegrid")

class ComprehensiveAnalysis:
    """Kapsamlı nihai analiz sınıfı"""

    def __init__(self, data_path='data/cleaned/dataset_beck_corrected.csv'):
        """Veri yükleme ve hazırlık"""
        self.data_path = data_path
        self.df = None
        self.results = {}
        self.statistical_tests = []

    def load_data(self):
        """Düzeltilmiş veriyi yükle"""
        print("="*80)
        print("VERİ YÜKLEME")
        print("="*80)

        self.df = pd.read_csv(self.data_path)

        # Temel bilgiler
        print(f"\nToplam kayıt: {len(self.df)}")
        print(f"Değişken sayısı: {len(self.df.columns)}")

        # Grup dağılımı
        if 'Grup' in self.df.columns:
            print(f"\nGrup dağılımı:")
            for grup, count in self.df['Grup'].value_counts().items():
                print(f"  {grup}: {count} ({count/len(self.df)*100:.1f}%)")

        # Alt grup dağılımı
        if 'Alt_Grup' in self.df.columns:
            print(f"\nAlt grup dağılımı:")
            for grup, count in self.df['Alt_Grup'].value_counts().items():
                print(f"  {grup}: {count}")

        return self.df

    def descriptive_statistics(self):
        """Tanımlayıcı istatistikler"""
        print("\n" + "="*80)
        print("TANIMLAYICI İSTATİSTİKLER")
        print("="*80)

        results = {}

        # Yaş değişkenleri
        age_vars = ['Anne_Yas', 'Katilimci_Cocuk_Yas']
        for var in age_vars:
            if var in self.df.columns:
                data = self.df[var].dropna()
                results[var] = {
                    'n': len(data),
                    'mean': data.mean(),
                    'std': data.std(),
                    'median': data.median(),
                    'min': data.min(),
                    'max': data.max(),
                    'q1': data.quantile(0.25),
                    'q3': data.quantile(0.75),
                    'iqr': data.quantile(0.75) - data.quantile(0.25),
                    'skewness': data.skew(),
                    'kurtosis': data.kurtosis()
                }

                print(f"\n{var}:")
                print(f"  N: {results[var]['n']}")
                print(f"  Ortalama: {results[var]['mean']:.2f} ± {results[var]['std']:.2f}")
                print(f"  Medyan (Q1-Q3): {results[var]['median']:.1f} ({results[var]['q1']:.1f}-{results[var]['q3']:.1f})")
                print(f"  Min-Max: {results[var]['min']:.1f}-{results[var]['max']:.1f}")
                print(f"  Çarpıklık: {results[var]['skewness']:.3f}")
                print(f"  Basıklık: {results[var]['kurtosis']:.3f}")

        # Beck skorları
        beck_vars = ['Beck_Total_Score', 'Beck Toplam', 'Beck_Calculated_New']
        for var in beck_vars:
            if var in self.df.columns:
                data = self.df[var].dropna()
                if len(data) > 0:
                    results[f'Beck_Score ({var})'] = {
                        'n': len(data),
                        'mean': data.mean(),
                        'std': data.std(),
                        'median': data.median(),
                        'min': data.min(),
                        'max': data.max()
                    }

                    print(f"\nBeck Depresyon Skoru ({var}):")
                    print(f"  N: {len(data)}")
                    print(f"  Ortalama: {data.mean():.2f} ± {data.std():.2f}")
                    print(f"  Medyan: {data.median():.1f}")
                    print(f"  Min-Max: {data.min():.0f}-{data.max():.0f}")
                    break

        self.results['descriptive'] = results
        return results

    def normality_tests(self):
        """Normallik testleri"""
        print("\n" + "="*80)
        print("NORMALLİK TESTLERİ")
        print("="*80)
        print("\nİstatistiksel Gerekçe:")
        print("Parametrik testlerin uygulanabilmesi için veri dağılımının")
        print("normal dağılıma uygunluğu test edilmelidir.")
        print("\nKullanılan Testler:")
        print("1. Shapiro-Wilk: n<50 için en güçlü test")
        print("2. D'Agostino-Pearson: Çarpıklık ve basıklığı birlikte değerlendirir")
        print("3. Jarque-Bera: Büyük örneklemler için uygundur")

        normality_results = {}

        # Test edilecek değişkenler
        test_vars = ['Anne_Yas', 'Katilimci_Cocuk_Yas', 'Beck Toplam', 'Beck_Calculated_New']

        for var in test_vars:
            if var in self.df.columns:
                data = self.df[var].dropna()
                if len(data) > 3:
                    print(f"\n{var} (n={len(data)}):")

                    results = {}

                    # Shapiro-Wilk testi
                    if len(data) <= 5000:
                        stat_sw, p_sw = shapiro(data)
                        results['shapiro_wilk'] = {'statistic': stat_sw, 'p_value': p_sw}
                        print(f"  Shapiro-Wilk: W={stat_sw:.4f}, p={p_sw:.4f}")

                    # D'Agostino-Pearson testi
                    if len(data) >= 8:
                        stat_dp, p_dp = normaltest(data)
                        results['dagostino_pearson'] = {'statistic': stat_dp, 'p_value': p_dp}
                        print(f"  D'Agostino-Pearson: K²={stat_dp:.4f}, p={p_dp:.4f}")

                    # Jarque-Bera testi
                    stat_jb, p_jb = jarque_bera(data)
                    results['jarque_bera'] = {'statistic': stat_jb, 'p_value': p_jb}
                    print(f"  Jarque-Bera: JB={stat_jb:.4f}, p={p_jb:.4f}")

                    # Sonuç
                    is_normal = all(r.get('p_value', 0) > 0.05 for r in results.values() if r)
                    results['is_normal'] = is_normal
                    print(f"  Sonuç: {'Normal dağılım' if is_normal else 'Normal dağılım DEĞİL'}")

                    normality_results[var] = results

                    # Test kaydı
                    self.statistical_tests.append({
                        'test': 'Normality Tests',
                        'variable': var,
                        'results': results,
                        'conclusion': 'Normal' if is_normal else 'Non-normal'
                    })

        self.results['normality'] = normality_results
        return normality_results

    def group_comparisons(self):
        """Gruplar arası karşılaştırmalar"""
        print("\n" + "="*80)
        print("GRUPLAR ARASI KARŞILAŞTIRMALAR")
        print("="*80)

        comparison_results = {}
        beck_col = None  # Beck column tanımını başta yap

        # 1. Ana gruplar (Diyabet vs Kontrol) - Beck skorları
        print("\n1. DEPRESYON DÜZEYLERİ (Diyabet vs Kontrol)")
        print("-" * 50)

        if 'Grup' in self.df.columns:
            beck_col = None
            for col in ['Beck Toplam', 'Beck_Total_Score', 'Beck_Calculated_New']:
                if col in self.df.columns:
                    beck_col = col
                    break

            if beck_col:
                diyabet = self.df[self.df['Grup'] == 'Diyabet'][beck_col].dropna()
                kontrol = self.df[self.df['Grup'] == 'Kontrol'][beck_col].dropna()

                print(f"\nDiyabet grubu (n={len(diyabet)}): {diyabet.mean():.2f} ± {diyabet.std():.2f}")
                print(f"Kontrol grubu (n={len(kontrol)}): {kontrol.mean():.2f} ± {kontrol.std():.2f}")

                # Normallik kontrolü ve test seçimi
                _, p_norm_d = shapiro(diyabet) if len(diyabet) <= 5000 else normaltest(diyabet)
                _, p_norm_k = shapiro(kontrol) if len(kontrol) <= 5000 else normaltest(kontrol)

                if p_norm_d > 0.05 and p_norm_k > 0.05:
                    # Parametrik test: Independent t-test
                    stat, p_value = ttest_ind(diyabet, kontrol)
                    test_name = "Independent t-test"
                    print(f"\n{test_name} (Parametrik):")
                    print(f"  Gerekçe: Her iki grup normal dağılım gösteriyor")
                    print(f"  t = {stat:.3f}, p = {p_value:.4f}")

                    # Etki büyüklüğü (Cohen's d)
                    pooled_std = np.sqrt(((len(diyabet)-1)*diyabet.std()**2 +
                                          (len(kontrol)-1)*kontrol.std()**2) /
                                         (len(diyabet)+len(kontrol)-2))
                    cohens_d = (diyabet.mean() - kontrol.mean()) / pooled_std
                    print(f"  Cohen's d = {cohens_d:.3f}")

                    # Güç analizi
                    power = ttest_power(cohens_d, len(diyabet), 0.05)
                    print(f"  İstatistiksel güç = {power:.3f}")
                else:
                    # Non-parametrik test: Mann-Whitney U
                    stat, p_value = mannwhitneyu(diyabet, kontrol, alternative='two-sided')
                    test_name = "Mann-Whitney U"
                    print(f"\n{test_name} (Non-parametrik):")
                    print(f"  Gerekçe: En az bir grup normal dağılım göstermiyor")
                    print(f"  U = {stat:.1f}, p = {p_value:.4f}")

                    # Etki büyüklüğü (r)
                    z = (stat - len(diyabet)*len(kontrol)/2) / np.sqrt(len(diyabet)*len(kontrol)*(len(diyabet)+len(kontrol)+1)/12)
                    r = z / np.sqrt(len(diyabet) + len(kontrol))
                    print(f"  Etki büyüklüğü r = {r:.3f}")

                comparison_results['depression_main_groups'] = {
                    'test': test_name,
                    'statistic': stat,
                    'p_value': p_value,
                    'diyabet_mean': diyabet.mean(),
                    'kontrol_mean': kontrol.mean(),
                    'significant': p_value < 0.05
                }

                print(f"\nSonuç: {'İstatistiksel olarak anlamlı fark var (p<0.05)' if p_value < 0.05 else 'Anlamlı fark yok (p≥0.05)'}")

                self.statistical_tests.append({
                    'test': test_name,
                    'comparison': 'Diyabet vs Kontrol (Beck)',
                    'p_value': p_value,
                    'significant': p_value < 0.05
                })

        # 2. Alt gruplar karşılaştırması (4 grup)
        print("\n2. ALT GRUPLAR KARŞILAŞTIRMASI")
        print("-" * 50)

        if 'Alt_Grup' in self.df.columns and beck_col:
            groups = []
            group_names = []

            for alt_grup in ['Diyabet_Index', 'Diyabet_Kardes', 'Kontrol_Index', 'Kontrol_Kardes']:
                if alt_grup in self.df['Alt_Grup'].values:
                    group_data = self.df[self.df['Alt_Grup'] == alt_grup][beck_col].dropna()
                    if len(group_data) > 0:
                        groups.append(group_data)
                        group_names.append(alt_grup)
                        print(f"{alt_grup} (n={len(group_data)}): {group_data.mean():.2f} ± {group_data.std():.2f}")

            if len(groups) >= 2:
                # Normallik kontrolü
                all_normal = all(shapiro(g)[1] > 0.05 if len(g) <= 5000 else normaltest(g)[1] > 0.05
                                 for g in groups if len(g) > 3)

                if all_normal and len(groups) > 2:
                    # One-way ANOVA
                    stat, p_value = f_oneway(*groups)
                    test_name = "One-way ANOVA"
                    print(f"\n{test_name} (Parametrik):")
                    print(f"  Gerekçe: Tüm gruplar normal dağılım gösteriyor")
                    print(f"  F = {stat:.3f}, p = {p_value:.4f}")

                    # Post-hoc test (Tukey HSD)
                    if p_value < 0.05:
                        print("\nPost-hoc Tukey HSD testi:")
                        all_data = []
                        all_groups = []
                        for i, g in enumerate(groups):
                            all_data.extend(g)
                            all_groups.extend([group_names[i]] * len(g))

                        tukey = pairwise_tukeyhsd(all_data, all_groups, alpha=0.05)
                        print(tukey)
                else:
                    # Kruskal-Wallis H testi
                    stat, p_value = kruskal(*groups)
                    test_name = "Kruskal-Wallis H"
                    print(f"\n{test_name} (Non-parametrik):")
                    print(f"  Gerekçe: En az bir grup normal dağılım göstermiyor")
                    print(f"  H = {stat:.3f}, p = {p_value:.4f}")

                comparison_results['subgroups'] = {
                    'test': test_name,
                    'statistic': stat,
                    'p_value': p_value,
                    'significant': p_value < 0.05
                }

                self.statistical_tests.append({
                    'test': test_name,
                    'comparison': '4 Alt Grup',
                    'p_value': p_value,
                    'significant': p_value < 0.05
                })

        self.results['comparisons'] = comparison_results
        return comparison_results

    def paired_analyses(self):
        """Eşleştirilmiş analizler (Kardeş çiftleri)"""
        print("\n" + "="*80)
        print("EŞLEŞTİRİLMİŞ ANALİZLER (KARDEŞ ÇİFTLERİ)")
        print("="*80)
        print("\nİstatistiksel Gerekçe:")
        print("Aile içi faktörleri kontrol etmek için kardeş çiftleri")
        print("eşleştirilmiş örneklem olarak analiz edilir.")

        paired_results = {}

        # Aile çiftlerini yükle
        try:
            pairs_df = pd.read_csv('data/cleaned/family_pairs.csv')
            print(f"\nToplam aile çifti: {len(pairs_df)}")

            beck_col = None
            for col in ['Beck Toplam', 'Beck_Total_Score', 'Beck_Calculated_New']:
                if col in self.df.columns:
                    beck_col = col
                    break

            if beck_col:
                # Diyabet aileleri
                print("\n1. DİYABET AİLELERİ")
                print("-" * 50)

                diyabet_pairs = pairs_df[pairs_df['Tip'] == 'Diyabet_Cifti']

                index_scores = []
                sibling_scores = []

                for _, pair in diyabet_pairs.iterrows():
                    index_data = self.df[self.df['Katılımcı No'] == pair['Index_ID']]
                    sibling_data = self.df[self.df['Katılımcı No'] == pair['Sibling_ID']]

                    if not index_data.empty and not sibling_data.empty:
                        if beck_col in index_data.columns and beck_col in sibling_data.columns:
                            index_score = index_data[beck_col].iloc[0]
                            sibling_score = sibling_data[beck_col].iloc[0]

                            if pd.notna(index_score) and pd.notna(sibling_score):
                                index_scores.append(index_score)
                                sibling_scores.append(sibling_score)

                if len(index_scores) > 0:
                    print(f"Analiz edilen çift sayısı: {len(index_scores)}")
                    print(f"Index ortalama: {np.mean(index_scores):.2f} ± {np.std(index_scores):.2f}")
                    print(f"Kardeş ortalama: {np.mean(sibling_scores):.2f} ± {np.std(sibling_scores):.2f}")

                    # Normallik kontrolü
                    diff = np.array(index_scores) - np.array(sibling_scores)
                    _, p_norm = shapiro(diff) if len(diff) <= 5000 else normaltest(diff)

                    if p_norm > 0.05:
                        # Paired t-test
                        stat, p_value = ttest_rel(index_scores, sibling_scores)
                        test_name = "Paired t-test"
                        print(f"\n{test_name} (Parametrik):")
                        print(f"  Gerekçe: Fark skorları normal dağılım gösteriyor")
                    else:
                        # Wilcoxon signed-rank test
                        stat, p_value = wilcoxon(index_scores, sibling_scores)
                        test_name = "Wilcoxon signed-rank"
                        print(f"\n{test_name} (Non-parametrik):")
                        print(f"  Gerekçe: Fark skorları normal dağılım göstermiyor")

                    print(f"  Test istatistiği = {stat:.3f}, p = {p_value:.4f}")
                    print(f"  Ortalama fark = {np.mean(diff):.2f}")

                    paired_results['diyabet_siblings'] = {
                        'test': test_name,
                        'statistic': stat,
                        'p_value': p_value,
                        'mean_diff': np.mean(diff),
                        'significant': p_value < 0.05
                    }

                    self.statistical_tests.append({
                        'test': test_name,
                        'comparison': 'Diyabet Kardeş Çiftleri',
                        'p_value': p_value,
                        'significant': p_value < 0.05
                    })

                # Kontrol aileleri
                print("\n2. KONTROL AİLELERİ")
                print("-" * 50)

                kontrol_pairs = pairs_df[pairs_df['Tip'] == 'Kontrol_Cifti']

                index_scores = []
                sibling_scores = []

                for _, pair in kontrol_pairs.iterrows():
                    index_data = self.df[self.df['Katılımcı No'] == pair['Index_ID']]
                    sibling_data = self.df[self.df['Katılımcı No'] == pair['Sibling_ID']]

                    if not index_data.empty and not sibling_data.empty:
                        if beck_col in index_data.columns and beck_col in sibling_data.columns:
                            index_score = index_data[beck_col].iloc[0]
                            sibling_score = sibling_data[beck_col].iloc[0]

                            if pd.notna(index_score) and pd.notna(sibling_score):
                                index_scores.append(index_score)
                                sibling_scores.append(sibling_score)

                if len(index_scores) > 0:
                    print(f"Analiz edilen çift sayısı: {len(index_scores)}")
                    print(f"Index ortalama: {np.mean(index_scores):.2f} ± {np.std(index_scores):.2f}")
                    print(f"Kardeş ortalama: {np.mean(sibling_scores):.2f} ± {np.std(sibling_scores):.2f}")

                    # Normallik kontrolü
                    diff = np.array(index_scores) - np.array(sibling_scores)
                    _, p_norm = shapiro(diff) if len(diff) <= 5000 else normaltest(diff)

                    if p_norm > 0.05:
                        stat, p_value = ttest_rel(index_scores, sibling_scores)
                        test_name = "Paired t-test"
                        print(f"\n{test_name} (Parametrik):")
                    else:
                        stat, p_value = wilcoxon(index_scores, sibling_scores)
                        test_name = "Wilcoxon signed-rank"
                        print(f"\n{test_name} (Non-parametrik):")

                    print(f"  Test istatistiği = {stat:.3f}, p = {p_value:.4f}")
                    print(f"  Ortalama fark = {np.mean(diff):.2f}")

                    paired_results['kontrol_siblings'] = {
                        'test': test_name,
                        'statistic': stat,
                        'p_value': p_value,
                        'mean_diff': np.mean(diff),
                        'significant': p_value < 0.05
                    }

                    self.statistical_tests.append({
                        'test': test_name,
                        'comparison': 'Kontrol Kardeş Çiftleri',
                        'p_value': p_value,
                        'significant': p_value < 0.05
                    })

        except FileNotFoundError:
            print("\n[UYARI] family_pairs.csv dosyası bulunamadı")

        self.results['paired'] = paired_results
        return paired_results

    def embu_analysis(self):
        """EMBU Ebeveynlik Tutumları Analizi"""
        print("\n" + "="*80)
        print("EMBU EBEVEYNLİK TUTUMLARI ANALİZİ")
        print("="*80)

        embu_results = {}

        # EMBU alt boyutları
        embu_subscales = {
            'Duygusal_Sicaklik': [2, 4, 12, 14, 19, 23],
            'Reddedicilik': [1, 7, 8, 11, 13, 17, 18, 20],
            'Asiri_Koruma': [3, 5, 6, 9, 10, 15, 16, 21, 22]
        }

        # EMBU skorlarını hesapla
        for subscale, items in embu_subscales.items():
            embu_cols = [f'Ebeveyn_EMBU_{i}' for i in items]
            available_cols = [col for col in embu_cols if col in self.df.columns]

            if available_cols:
                self.df[f'EMBU_{subscale}'] = self.df[available_cols].mean(axis=1)
                print(f"\n{subscale}: {len(available_cols)}/{len(items)} madde mevcut")

        # Gruplar arası EMBU karşılaştırması
        if 'Grup' in self.df.columns:
            for subscale in embu_subscales.keys():
                col_name = f'EMBU_{subscale}'
                if col_name in self.df.columns:
                    print(f"\n{subscale.replace('_', ' ').upper()}")
                    print("-" * 50)

                    diyabet = self.df[self.df['Grup'] == 'Diyabet'][col_name].dropna()
                    kontrol = self.df[self.df['Grup'] == 'Kontrol'][col_name].dropna()

                    if len(diyabet) > 0 and len(kontrol) > 0:
                        print(f"Diyabet (n={len(diyabet)}): {diyabet.mean():.2f} ± {diyabet.std():.2f}")
                        print(f"Kontrol (n={len(kontrol)}): {kontrol.mean():.2f} ± {kontrol.std():.2f}")

                        # Test seçimi
                        _, p_norm_d = shapiro(diyabet) if len(diyabet) <= 5000 else normaltest(diyabet)
                        _, p_norm_k = shapiro(kontrol) if len(kontrol) <= 5000 else normaltest(kontrol)

                        if p_norm_d > 0.05 and p_norm_k > 0.05:
                            stat, p_value = ttest_ind(diyabet, kontrol)
                            test_name = "Independent t-test"
                        else:
                            stat, p_value = mannwhitneyu(diyabet, kontrol, alternative='two-sided')
                            test_name = "Mann-Whitney U"

                        print(f"{test_name}: p = {p_value:.4f}")
                        print(f"Sonuç: {'Anlamlı fark var' if p_value < 0.05 else 'Anlamlı fark yok'}")

                        embu_results[subscale] = {
                            'test': test_name,
                            'p_value': p_value,
                            'diyabet_mean': diyabet.mean(),
                            'kontrol_mean': kontrol.mean(),
                            'significant': p_value < 0.05
                        }

                        self.statistical_tests.append({
                            'test': test_name,
                            'comparison': f'EMBU {subscale}',
                            'p_value': p_value,
                            'significant': p_value < 0.05
                        })

        self.results['embu'] = embu_results
        return embu_results

    def correlation_analysis(self):
        """Korelasyon analizleri"""
        print("\n" + "="*80)
        print("KORELASYON ANALİZLERİ")
        print("="*80)
        print("\nİstatistiksel Gerekçe:")
        print("Değişkenler arası ilişkilerin yönü ve gücünü belirlemek için")
        print("Pearson (normal dağılım) veya Spearman (non-parametrik) korelasyonu kullanılır.")

        correlation_results = {}

        # Ana değişkenler
        main_vars = ['Anne_Yas', 'Katilimci_Cocuk_Yas', 'Beck Toplam', 'Cocuk_Sayisi']
        available_vars = [var for var in main_vars if var in self.df.columns]

        # EMBU değişkenleri ekle
        embu_vars = ['EMBU_Duygusal_Sicaklik', 'EMBU_Reddedicilik', 'EMBU_Asiri_Koruma']
        available_vars.extend([var for var in embu_vars if var in self.df.columns])

        if len(available_vars) >= 2:
            print(f"\nAnaliz edilen değişkenler: {', '.join(available_vars)}")

            # Korelasyon matrisi
            corr_matrix = pd.DataFrame(index=available_vars, columns=available_vars)
            p_matrix = pd.DataFrame(index=available_vars, columns=available_vars)

            for i, var1 in enumerate(available_vars):
                for j, var2 in enumerate(available_vars):
                    if i < j:  # Sadece üst üçgen
                        data1 = self.df[var1].dropna()
                        data2 = self.df[var2].dropna()

                        # Ortak gözlemleri bul
                        common_idx = data1.index.intersection(data2.index)
                        if len(common_idx) > 3:
                            data1_common = data1.loc[common_idx]
                            data2_common = data2.loc[common_idx]

                            # Normallik kontrolü
                            _, p_norm1 = shapiro(data1_common) if len(data1_common) <= 5000 else normaltest(data1_common)
                            _, p_norm2 = shapiro(data2_common) if len(data2_common) <= 5000 else normaltest(data2_common)

                            if p_norm1 > 0.05 and p_norm2 > 0.05:
                                # Pearson korelasyonu
                                r, p_val = pearsonr(data1_common, data2_common)
                                test_type = 'Pearson'
                            else:
                                # Spearman korelasyonu
                                r, p_val = spearmanr(data1_common, data2_common)
                                test_type = 'Spearman'

                            corr_matrix.loc[var1, var2] = r
                            corr_matrix.loc[var2, var1] = r
                            p_matrix.loc[var1, var2] = p_val
                            p_matrix.loc[var2, var1] = p_val

                            # Anlamlı korelasyonları rapor et
                            if p_val < 0.05:
                                print(f"\n{var1} - {var2}:")
                                print(f"  {test_type} r = {r:.3f}, p = {p_val:.4f}")
                                print(f"  n = {len(common_idx)}")

                                # Korelasyon gücü yorumu
                                if abs(r) < 0.3:
                                    strength = "Zayıf"
                                elif abs(r) < 0.7:
                                    strength = "Orta"
                                else:
                                    strength = "Güçlü"
                                print(f"  İlişki: {strength} {'pozitif' if r > 0 else 'negatif'}")

                                correlation_results[f"{var1}_{var2}"] = {
                                    'method': test_type,
                                    'r': r,
                                    'p_value': p_val,
                                    'n': len(common_idx),
                                    'strength': strength
                                }

            # Korelasyon matrisi ısı haritası
            try:
                plt.figure(figsize=(10, 8))
                mask = np.triu(np.ones_like(corr_matrix.astype(float), dtype=bool))
                sns.heatmap(corr_matrix.astype(float), mask=mask, annot=True,
                           cmap='coolwarm', center=0, vmin=-1, vmax=1,
                           square=True, linewidths=1, cbar_kws={"shrink": 0.8})
                plt.title('Korelasyon Matrisi')
                plt.tight_layout()
                plt.savefig('results/correlation_matrix.png', dpi=300, bbox_inches='tight')
                plt.close()
                print("\n[OK] Korelasyon matrisi kaydedildi: correlation_matrix.png")
            except:
                print("\n[UYARI] Korelasyon matrisi görselleştirilemedi")

        self.results['correlations'] = correlation_results
        return correlation_results

    def categorical_analyses(self):
        """Kategorik değişken analizleri"""
        print("\n" + "="*80)
        print("KATEGORİK DEĞİŞKEN ANALİZLERİ")
        print("="*80)

        categorical_results = {}

        # Beck depresyon kategorileri
        beck_col = None
        for col in ['Beck Toplam', 'Beck_Total_Score', 'Beck_Calculated_New']:
            if col in self.df.columns:
                beck_col = col
                break

        if beck_col:
            # Depresyon kategorileri oluştur
            def categorize_beck(score):
                if pd.isna(score):
                    return np.nan
                elif score <= 9:
                    return 'Minimal'
                elif score <= 16:
                    return 'Hafif'
                elif score <= 29:
                    return 'Orta'
                else:
                    return 'Ağır'

            self.df['Beck_Category'] = self.df[beck_col].apply(categorize_beck)

            # Grup ve depresyon kategorisi çapraz tablosu
            if 'Grup' in self.df.columns:
                print("\nDepresyon Kategorileri - Grup Dağılımı")
                print("-" * 50)

                crosstab = pd.crosstab(self.df['Grup'], self.df['Beck_Category'],
                                       margins=True, margins_name='Toplam')
                print(crosstab)

                # Chi-square testi
                crosstab_test = pd.crosstab(self.df['Grup'], self.df['Beck_Category'])
                chi2, p_value, dof, expected = chi2_contingency(crosstab_test)

                print(f"\nChi-square testi:")
                print(f"  Chi-square = {chi2:.3f}, df = {dof}, p = {p_value:.4f}")
                print(f"  Sonuç: {'Gruplar arasında depresyon kategorileri farklıdır' if p_value < 0.05 else 'Anlamlı fark yok'}")

                # Cramér's V (etki büyüklüğü)
                n = crosstab_test.sum().sum()
                cramers_v = np.sqrt(chi2 / (n * (min(crosstab_test.shape) - 1)))
                print(f"  Cramér's V = {cramers_v:.3f}")

                categorical_results['depression_categories'] = {
                    'test': 'Chi-square',
                    'chi2': chi2,
                    'p_value': p_value,
                    'cramers_v': cramers_v,
                    'significant': p_value < 0.05
                }

                self.statistical_tests.append({
                    'test': 'Chi-square',
                    'comparison': 'Depresyon Kategorileri x Grup',
                    'p_value': p_value,
                    'significant': p_value < 0.05
                })

        # Çalışma durumu analizi
        if 'Calisma_Durumu' in self.df.columns and 'Grup_Yeni' in self.df.columns:
            print("\nÇalışma Durumu - Grup Dağılımı")
            print("-" * 50)

            crosstab = pd.crosstab(self.df['Grup'], self.df['Calisma_Durumu'],
                                   margins=True, margins_name='Toplam')
            print(crosstab)

            # Fisher's exact test (2x2 tablo için)
            if crosstab.shape == (3, 3):  # Toplam satır/sütun dahil
                crosstab_test = crosstab.iloc[:-1, :-1]
                if crosstab_test.shape == (2, 2):
                    odds_ratio, p_value = fisher_exact(crosstab_test)
                    print(f"\nFisher's Exact Test:")
                    print(f"  Odds Ratio = {odds_ratio:.3f}, p = {p_value:.4f}")

                    categorical_results['work_status'] = {
                        'test': "Fisher's Exact",
                        'odds_ratio': odds_ratio,
                        'p_value': p_value,
                        'significant': p_value < 0.05
                    }

        self.results['categorical'] = categorical_results
        return categorical_results

    def generate_visualizations(self):
        """Görselleştirmeler"""
        print("\n" + "="*80)
        print("GÖRSELLEŞTİRMELER")
        print("="*80)

        try:
            # 1. Beck skorları dağılımı
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))

            beck_col = None
            for col in ['Beck Toplam', 'Beck_Total_Score', 'Beck_Calculated_New']:
                if col in self.df.columns:
                    beck_col = col
                    break

            if beck_col and 'Grup_Yeni' in self.df.columns:
                # Box plot
                ax = axes[0, 0]
                self.df.boxplot(column=beck_col, by='Grup_Yeni', ax=ax)
                ax.set_title('Beck Skorları - Grup Karşılaştırması')
                ax.set_xlabel('Grup')
                ax.set_ylabel('Beck Skoru')

                # Histogram
                ax = axes[0, 1]
                for grup in self.df['Grup'].unique():
                    data = self.df[self.df['Grup'] == grup][beck_col].dropna()
                    ax.hist(data, alpha=0.5, label=grup, bins=15)
                ax.set_xlabel('Beck Skoru')
                ax.set_ylabel('Frekans')
                ax.set_title('Beck Skorları Dağılımı')
                ax.legend()

            # Alt gruplar
            if 'Alt_Grup' in self.df.columns and beck_col:
                ax = axes[1, 0]
                alt_gruplar = self.df['Alt_Grup'].dropna().unique()
                positions = range(len(alt_gruplar))
                data_to_plot = [self.df[self.df['Alt_Grup'] == g][beck_col].dropna() for g in alt_gruplar]
                bp = ax.boxplot(data_to_plot, positions=positions, patch_artist=True)
                ax.set_xticks(positions)
                ax.set_xticklabels(alt_gruplar, rotation=45, ha='right')
                ax.set_ylabel('Beck Skoru')
                ax.set_title('Beck Skorları - Alt Gruplar')
                ax.grid(True, alpha=0.3)

            # Korelasyon scatter plot
            if 'Anne_Yas' in self.df.columns and beck_col:
                ax = axes[1, 1]
                ax.scatter(self.df['Anne_Yas'], self.df[beck_col], alpha=0.5)
                ax.set_xlabel('Anne Yaşı')
                ax.set_ylabel('Beck Skoru')
                ax.set_title('Anne Yaşı - Beck Skoru İlişkisi')

                # Trend çizgisi
                valid_data = self.df[['Anne_Yas', beck_col]].dropna()
                if len(valid_data) > 2:
                    z = np.polyfit(valid_data['Anne_Yas'], valid_data[beck_col], 1)
                    p = np.poly1d(z)
                    ax.plot(valid_data['Anne_Yas'].sort_values(),
                           p(valid_data['Anne_Yas'].sort_values()),
                           "r--", alpha=0.8, label=f'Trend: y={z[0]:.2f}x+{z[1]:.2f}')
                    ax.legend()

            plt.suptitle('Kapsamlı Analiz Görselleştirmeleri', fontsize=16, y=1.02)
            plt.tight_layout()
            plt.savefig('results/comprehensive_analysis_plots.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("[OK] Görselleştirmeler kaydedildi: comprehensive_analysis_plots.png")

        except Exception as e:
            print(f"[HATA] Görselleştirme oluşturulamadı: {e}")

        return True

    def generate_report(self):
        """Detaylı rapor oluştur"""
        print("\n" + "="*80)
        print("DETAYLI RAPOR OLUŞTURMA")
        print("="*80)

        report_lines = []
        report_lines.append("="*80)
        report_lines.append("KAPSAMLı NİHAİ ANALİZ RAPORU")
        report_lines.append("="*80)
        report_lines.append(f"\nTarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report_lines.append(f"Veri: {self.data_path}")
        report_lines.append(f"Toplam kayıt: {len(self.df)}")

        # 1. Tanımlayıcı istatistikler
        report_lines.append("\n" + "="*80)
        report_lines.append("1. TANIMLAYICI İSTATİSTİKLER")
        report_lines.append("="*80)

        if 'descriptive' in self.results:
            for var, stats in self.results['descriptive'].items():
                if 'mean' in stats:
                    report_lines.append(f"\n{var}:")
                    report_lines.append(f"  N = {stats['n']}")
                    report_lines.append(f"  Ortalama ± SS = {stats['mean']:.2f} ± {stats['std']:.2f}")
                    report_lines.append(f"  Medyan = {stats['median']:.1f}")
                    report_lines.append(f"  Min-Max = {stats['min']:.1f} - {stats['max']:.1f}")

        # 2. Normallik testleri
        report_lines.append("\n" + "="*80)
        report_lines.append("2. NORMALLİK TESTLERİ")
        report_lines.append("="*80)

        if 'normality' in self.results:
            for var, tests in self.results['normality'].items():
                report_lines.append(f"\n{var}:")
                if 'shapiro_wilk' in tests:
                    report_lines.append(f"  Shapiro-Wilk: p = {tests['shapiro_wilk']['p_value']:.4f}")
                if 'jarque_bera' in tests:
                    report_lines.append(f"  Jarque-Bera: p = {tests['jarque_bera']['p_value']:.4f}")
                report_lines.append(f"  Sonuç: {'Normal dağılım' if tests.get('is_normal', False) else 'Normal dağılım DEĞİL'}")

        # 3. Gruplar arası karşılaştırmalar
        report_lines.append("\n" + "="*80)
        report_lines.append("3. GRUPLAR ARASI KARŞILAŞTIRMALAR")
        report_lines.append("="*80)

        if 'comparisons' in self.results:
            if 'depression_main_groups' in self.results['comparisons']:
                comp = self.results['comparisons']['depression_main_groups']
                report_lines.append(f"\nDepresyon Düzeyleri (Diyabet vs Kontrol):")
                report_lines.append(f"  Test: {comp['test']}")
                report_lines.append(f"  Diyabet ortalaması: {comp['diyabet_mean']:.2f}")
                report_lines.append(f"  Kontrol ortalaması: {comp['kontrol_mean']:.2f}")
                report_lines.append(f"  p-değeri: {comp['p_value']:.4f}")
                report_lines.append(f"  Sonuç: {'ANLAMLI FARK VAR' if comp['significant'] else 'Anlamlı fark yok'}")

        # 4. Eşleştirilmiş analizler
        report_lines.append("\n" + "="*80)
        report_lines.append("4. EŞLEŞTİRİLMİŞ ANALİZLER")
        report_lines.append("="*80)

        if 'paired' in self.results:
            for group, analysis in self.results['paired'].items():
                report_lines.append(f"\n{group.replace('_', ' ').title()}:")
                report_lines.append(f"  Test: {analysis['test']}")
                report_lines.append(f"  Ortalama fark: {analysis['mean_diff']:.2f}")
                report_lines.append(f"  p-değeri: {analysis['p_value']:.4f}")
                report_lines.append(f"  Sonuç: {'ANLAMLI' if analysis['significant'] else 'Anlamlı değil'}")

        # 5. EMBU analizleri
        report_lines.append("\n" + "="*80)
        report_lines.append("5. EMBU EBEVEYNLİK TUTUMLARI")
        report_lines.append("="*80)

        if 'embu' in self.results:
            for subscale, analysis in self.results['embu'].items():
                report_lines.append(f"\n{subscale.replace('_', ' ')}:")
                report_lines.append(f"  Test: {analysis['test']}")
                report_lines.append(f"  p-değeri: {analysis['p_value']:.4f}")
                report_lines.append(f"  Sonuç: {'ANLAMLI' if analysis['significant'] else 'Anlamlı değil'}")

        # 6. Korelasyon analizleri
        report_lines.append("\n" + "="*80)
        report_lines.append("6. KORELASYON ANALİZLERİ")
        report_lines.append("="*80)

        if 'correlations' in self.results:
            report_lines.append("\nAnlamlı korelasyonlar:")
            for pair, corr in self.results['correlations'].items():
                report_lines.append(f"\n{pair.replace('_', ' - ')}:")
                report_lines.append(f"  {corr['method']} r = {corr['r']:.3f}")
                report_lines.append(f"  p = {corr['p_value']:.4f}")
                report_lines.append(f"  İlişki: {corr['strength']}")

        # 7. İstatistiksel test özeti
        report_lines.append("\n" + "="*80)
        report_lines.append("7. İSTATİSTİKSEL TEST ÖZETİ")
        report_lines.append("="*80)

        significant_tests = [t for t in self.statistical_tests if t.get('significant', False)]
        report_lines.append(f"\nToplam test sayısı: {len(self.statistical_tests)}")
        report_lines.append(f"Anlamlı sonuç sayısı: {len(significant_tests)}")

        if significant_tests:
            report_lines.append("\nAnlamlı bulgular:")
            for test in significant_tests:
                report_lines.append(f"  - {test['comparison']}: p = {test['p_value']:.4f}")

        # 8. Sonuçlar ve öneriler
        report_lines.append("\n" + "="*80)
        report_lines.append("8. SONUÇLAR VE ÖNERİLER")
        report_lines.append("="*80)

        report_lines.append("\nANA BULGULAR:")

        # Ana bulguları özetle
        if 'comparisons' in self.results and 'depression_main_groups' in self.results['comparisons']:
            if self.results['comparisons']['depression_main_groups']['significant']:
                report_lines.append("1. Diyabetli çocukların annelerinde depresyon düzeyi anlamlı olarak yüksektir.")

        report_lines.append("\nİSTATİSTİKSEL YÖNTEM GEREKÇELERİ:")
        report_lines.append("- Normallik testleri ile parametrik/non-parametrik test seçimi yapılmıştır")
        report_lines.append("- Eşleştirilmiş örneklemler için paired testler kullanılmıştır")
        report_lines.append("- Kategorik değişkenler için Chi-square veya Fisher's exact test uygulanmıştır")
        report_lines.append("- Etki büyüklükleri (Cohen's d, Cramér's V) hesaplanmıştır")

        report_lines.append("\n" + "="*80)

        # Raporu kaydet
        report_text = "\n".join(report_lines)

        with open('results/comprehensive_final_report.txt', 'w', encoding='utf-8') as f:
            f.write(report_text)

        print("[OK] Detaylı rapor kaydedildi: comprehensive_final_report.txt")

        # JSON formatında da kaydet
        with open('results/analysis_results.json', 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'data_path': self.data_path,
                'n_samples': len(self.df),
                'results': self.results,
                'statistical_tests': self.statistical_tests,
                'n_significant': len(significant_tests)
            }, f, indent=2, default=str)

        print("[OK] JSON sonuçları kaydedildi: analysis_results.json")

        return report_text

    def run_all_analyses(self):
        """Tüm analizleri çalıştır"""
        print("\n" + "="*80)
        print("TÜM ANALİZLER ÇALIŞTIRILIYOR")
        print("="*80)

        # 1. Veri yükleme
        self.load_data()

        # 2. Tanımlayıcı istatistikler
        self.descriptive_statistics()

        # 3. Normallik testleri
        self.normality_tests()

        # 4. Gruplar arası karşılaştırmalar
        self.group_comparisons()

        # 5. Eşleştirilmiş analizler
        self.paired_analyses()

        # 6. EMBU analizleri
        self.embu_analysis()

        # 7. Korelasyon analizleri
        self.correlation_analysis()

        # 8. Kategorik analizler
        self.categorical_analyses()

        # 9. Görselleştirmeler
        self.generate_visualizations()

        # 10. Rapor oluştur
        self.generate_report()

        print("\n" + "="*80)
        print("TÜM ANALİZLER TAMAMLANDI")
        print("="*80)

        return self.results

def main():
    """Ana fonksiyon"""

    print("\n" + "="*80)
    print("KAPSAMLı NİHAİ ANALİZ BAŞLIYOR")
    print("="*80)

    try:
        # Analiz sınıfını başlat
        analysis = ComprehensiveAnalysis()

        # Tüm analizleri çalıştır
        results = analysis.run_all_analyses()

        print("\n" + "="*80)
        print("BAŞARILI")
        print("="*80)
        print("\nOluşturulan dosyalar:")
        print("  - results/comprehensive_final_report.txt")
        print("  - results/analysis_results.json")
        print("  - results/comprehensive_analysis_plots.png")
        print("  - results/correlation_matrix.png")

        return results

    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()