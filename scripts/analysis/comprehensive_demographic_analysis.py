"""
KAPSAMLI DEMOGRAFİK VE TIBBİ VERİ ANALİZİ
==========================================
Demografik ve tıbbi verilerin depresyon ve EMBU skorlarına etkisini inceler
Regresyon analizi, moderasyon analizi ve risk faktörleri tespiti yapar
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import (
    chi2_contingency, fisher_exact,
    mannwhitneyu, ttest_ind,
    kruskal, f_oneway,
    pearsonr, spearmanr,
    pointbiserialr
)
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, classification_report
import statsmodels.api as sm
import statsmodels.formula.api as smf
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
plt.rcParams['figure.figsize'] = (14, 10)
sns.set_style("whitegrid")

class DemographicAnalysis:
    """Demografik ve tıbbi veri analizi sınıfı"""

    def __init__(self, data_path='data/cleaned/dataset_beck_corrected.csv'):
        self.data_path = data_path
        self.df = None
        self.results = {}
        self.demographic_vars = []
        self.medical_vars = []

    def load_and_prepare_data(self):
        """Veriyi yükle ve hazırla"""
        print("="*80)
        print("VERİ YÜKLEME VE HAZIRLAMA")
        print("="*80)

        self.df = pd.read_csv(self.data_path)
        print(f"\nToplam kayıt: {len(self.df)}")

        # Demografik değişkenleri tanımla
        self.demographic_vars = [
            'Anne_Yas', 'Katilimci_Cocuk_Yas', 'Cocuk_Sayisi',
            'Calisma_Durumu', 'Egitim_Durumu', 'Medeni_Durum',
            'Gelir_Durumu', 'Aile_Tipi'
        ]

        # Tıbbi değişkenleri tanımla
        self.medical_vars = [
            'DM_Tan_Yasi', 'DM_Suresi', 'HbA1c', 'Insulin_Dozu',
            'Anne_Antidepresan', 'Ek_Hastalik', 'Komplikasyon'
        ]

        # Yaş değişkenlerini düzelt (string ise)
        for col in ['Anne_Yas', 'Katilimci_Cocuk_Yas']:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        # Tarih sütunlarından yaş ve süre hesapla
        self._calculate_ages_and_durations()

        # Mevcut değişkenleri kontrol et
        print("\nDemografik değişkenler:")
        for var in self.demographic_vars:
            if var in self.df.columns:
                non_null = self.df[var].notna().sum()
                print(f"  {var}: {non_null}/{len(self.df)} ({non_null/len(self.df)*100:.1f}%)")

        print("\nTıbbi değişkenler:")
        for var in self.medical_vars:
            if var in self.df.columns:
                non_null = self.df[var].notna().sum()
                print(f"  {var}: {non_null}/{len(self.df)} ({non_null/len(self.df)*100:.1f}%)")

        return self.df

    def _calculate_ages_and_durations(self):
        """Tarih sütunlarından yaş ve süre hesapla"""

        # Bugünün tarihi
        today = pd.Timestamp.now()

        # Anne yaşı
        if 'Anne Doğum Tarihi' in self.df.columns:
            self.df['Anne Doğum Tarihi'] = pd.to_datetime(self.df['Anne Doğum Tarihi'], errors='coerce')
            self.df['Anne_Yas_Calculated'] = (today - self.df['Anne Doğum Tarihi']).dt.days / 365.25

            if 'Anne_Yas' not in self.df.columns:
                self.df['Anne_Yas'] = self.df['Anne_Yas_Calculated']

        # Çocuk yaşı
        if 'Katılımcı Çocuk Doğum Tarihi' in self.df.columns:
            self.df['Katılımcı Çocuk Doğum Tarihi'] = pd.to_datetime(self.df['Katılımcı Çocuk Doğum Tarihi'], errors='coerce')
            self.df['Cocuk_Yas_Calculated'] = (today - self.df['Katılımcı Çocuk Doğum Tarihi']).dt.days / 365.25

            if 'Katilimci_Cocuk_Yas' not in self.df.columns:
                self.df['Katilimci_Cocuk_Yas'] = self.df['Cocuk_Yas_Calculated']

        # DM süresi
        if 'DM Tanı Tarihi' in self.df.columns:
            self.df['DM Tanı Tarihi'] = pd.to_datetime(self.df['DM Tanı Tarihi'], errors='coerce')
            self.df['DM_Suresi'] = (today - self.df['DM Tanı Tarihi']).dt.days / 365.25
            self.df['DM_Suresi'] = self.df['DM_Suresi'].apply(lambda x: x if x >= 0 else np.nan)

            # Tanı yaşını hesapla
            if 'Katilimci_Cocuk_Yas' in self.df.columns:
                self.df['DM_Tan_Yasi'] = self.df['Katilimci_Cocuk_Yas'] - self.df['DM_Suresi']

    def descriptive_analysis(self):
        """Tanımlayıcı istatistikler"""
        print("\n" + "="*80)
        print("TANIMLAYICI İSTATİSTİKLER")
        print("="*80)

        desc_results = {}

        # Gruplar arası demografik karşılaştırma
        if 'Grup' in self.df.columns:
            print("\n1. GRUPLAR ARASI DEMOGRAFİK KARŞILAŞTIRMA")
            print("-" * 50)

            for var in self.demographic_vars:
                if var in self.df.columns:
                    # Sayısal değişkenler
                    if self.df[var].dtype in ['float64', 'int64']:
                        diyabet = self.df[self.df['Grup'] == 'Diyabet'][var].dropna()
                        kontrol = self.df[self.df['Grup'] == 'Kontrol'][var].dropna()

                        if len(diyabet) > 0 and len(kontrol) > 0:
                            print(f"\n{var}:")
                            print(f"  Diyabet: {diyabet.mean():.2f} ± {diyabet.std():.2f} (n={len(diyabet)})")
                            print(f"  Kontrol: {kontrol.mean():.2f} ± {kontrol.std():.2f} (n={len(kontrol)})")

                            # T-test veya Mann-Whitney U
                            _, p_norm_d = stats.shapiro(diyabet) if len(diyabet) <= 5000 else stats.normaltest(diyabet)
                            _, p_norm_k = stats.shapiro(kontrol) if len(kontrol) <= 5000 else stats.normaltest(kontrol)

                            if p_norm_d > 0.05 and p_norm_k > 0.05:
                                stat, p_value = ttest_ind(diyabet, kontrol)
                                test_name = "t-test"
                            else:
                                stat, p_value = mannwhitneyu(diyabet, kontrol, alternative='two-sided')
                                test_name = "Mann-Whitney U"

                            print(f"  {test_name}: p = {p_value:.4f}")

                            desc_results[var] = {
                                'diyabet_mean': diyabet.mean(),
                                'kontrol_mean': kontrol.mean(),
                                'p_value': p_value,
                                'significant': p_value < 0.05
                            }

                    # Kategorik değişkenler
                    else:
                        crosstab = pd.crosstab(self.df['Grup'], self.df[var], margins=True)
                        print(f"\n{var}:")
                        print(crosstab)

                        # Chi-square testi
                        if crosstab.shape[0] > 2 and crosstab.shape[1] > 2:
                            chi2, p_value, dof, expected = chi2_contingency(crosstab.iloc[:-1, :-1])
                            print(f"  Chi-square: p = {p_value:.4f}")

                            desc_results[var] = {
                                'test': 'chi-square',
                                'p_value': p_value,
                                'significant': p_value < 0.05
                            }

        self.results['descriptive'] = desc_results
        return desc_results

    def correlation_analysis(self):
        """Demografik değişkenler ile Beck/EMBU skorları arasındaki korelasyon"""
        print("\n" + "="*80)
        print("KORELASYON ANALİZLERİ")
        print("="*80)

        correlation_results = {}

        # Hedef değişkenler
        target_vars = ['Beck Toplam', 'Beck_Calculated_New']
        embu_vars = ['EMBU_Parent_Duygusal_Sicaklik', 'EMBU_Parent_Reddedicilik', 'EMBU_Parent_Asiri_Koruma']

        # Beck skorunu bul
        beck_col = None
        for col in target_vars:
            if col in self.df.columns:
                beck_col = col
                break

        if beck_col:
            print("\n1. DEMOGRAFİK DEĞİŞKENLER - BECK DEPRESYON")
            print("-" * 50)

            for var in self.demographic_vars:
                if var in self.df.columns and self.df[var].dtype in ['float64', 'int64']:
                    valid_idx = self.df[[var, beck_col]].dropna().index
                    if len(valid_idx) > 10:
                        x = self.df.loc[valid_idx, var]
                        y = self.df.loc[valid_idx, beck_col]

                        # Spearman korelasyonu
                        r, p = spearmanr(x, y)

                        if p < 0.05:
                            print(f"{var}: r = {r:.3f}, p = {p:.4f} *")

                            correlation_results[f"{var}_Beck"] = {
                                'r': r,
                                'p': p,
                                'n': len(valid_idx)
                            }

        # EMBU skorları ile korelasyon
        print("\n2. DEMOGRAFİK DEĞİŞKENLER - EMBU SKORLARI")
        print("-" * 50)

        for embu_var in embu_vars:
            if embu_var in self.df.columns:
                for demo_var in self.demographic_vars:
                    if demo_var in self.df.columns and self.df[demo_var].dtype in ['float64', 'int64']:
                        valid_idx = self.df[[demo_var, embu_var]].dropna().index
                        if len(valid_idx) > 10:
                            x = self.df.loc[valid_idx, demo_var]
                            y = self.df.loc[valid_idx, embu_var]

                            r, p = spearmanr(x, y)

                            if p < 0.05:
                                subscale = embu_var.split('_')[-1]
                                print(f"{demo_var} - {subscale}: r = {r:.3f}, p = {p:.4f} *")

                                correlation_results[f"{demo_var}_{subscale}"] = {
                                    'r': r,
                                    'p': p,
                                    'n': len(valid_idx)
                                }

        self.results['correlations'] = correlation_results
        return correlation_results

    def regression_analysis(self):
        """Çoklu regresyon analizi"""
        print("\n" + "="*80)
        print("ÇOKLU REGRESYON ANALİZİ")
        print("="*80)

        regression_results = {}

        # Beck depresyon skoru için regresyon
        beck_col = None
        for col in ['Beck Toplam', 'Beck_Calculated_New']:
            if col in self.df.columns:
                beck_col = col
                break

        if beck_col:
            print("\n1. BECK DEPRESYON SKORUNU YORDAYAN FAKTÖRLER")
            print("-" * 50)

            # Bağımsız değişkenleri hazırla
            predictors = []
            predictor_names = []

            # Demografik değişkenler
            for var in ['Anne_Yas', 'Cocuk_Sayisi', 'DM_Suresi']:
                if var in self.df.columns:
                    predictors.append(var)
                    predictor_names.append(var)

            # Grup değişkeni (dummy coding)
            if 'Grup' in self.df.columns:
                self.df['Grup_Diyabet'] = (self.df['Grup'] == 'Diyabet').astype(int)
                predictors.append('Grup_Diyabet')
                predictor_names.append('Grup (Diyabet=1)')

            # Çalışma durumu
            if 'Calisma_Durumu' in self.df.columns:
                self.df['Calisma_Var'] = self.df['Calisma_Durumu'].notna().astype(int)
                predictors.append('Calisma_Var')
                predictor_names.append('Çalışma Durumu')

            # Regresyon için veri hazırla
            if predictors:
                # Eksik verileri temizle
                regression_df = self.df[predictors + [beck_col]].dropna()

                if len(regression_df) > 20:
                    X = regression_df[predictors]
                    y = regression_df[beck_col]

                    # Statsmodels ile regresyon
                    X_sm = sm.add_constant(X)
                    model = sm.OLS(y, X_sm).fit()

                    print("\nModel Özeti:")
                    print(f"  R² = {model.rsquared:.3f}")
                    print(f"  Adjusted R² = {model.rsquared_adj:.3f}")
                    print(f"  F-statistic = {model.fvalue:.2f}, p = {model.f_pvalue:.4f}")

                    print("\nKatsayılar:")
                    for i, var in enumerate(['Sabit'] + predictor_names):
                        coef = model.params[i]
                        p_val = model.pvalues[i]
                        ci = model.conf_int()
                        ci_low = ci.iloc[i, 0]
                        ci_high = ci.iloc[i, 1]
                        print(f"  {var}: B = {coef:.3f}, p = {p_val:.4f}, CI = [{ci_low:.3f}, {ci_high:.3f}]")

                    regression_results['beck_model'] = {
                        'r_squared': model.rsquared,
                        'adj_r_squared': model.rsquared_adj,
                        'f_statistic': model.fvalue,
                        'p_value': model.f_pvalue,
                        'coefficients': dict(zip(['Intercept'] + predictor_names, model.params)),
                        'p_values': dict(zip(['Intercept'] + predictor_names, model.pvalues))
                    }

        # EMBU skorları için regresyon
        print("\n2. EMBU SKORLARINI YORDAYAN FAKTÖRLER")
        print("-" * 50)

        for embu_var in ['EMBU_Parent_Asiri_Koruma']:
            if embu_var in self.df.columns:
                subscale = embu_var.split('_')[-1]
                print(f"\n{subscale}:")

                regression_df = self.df[predictors + [embu_var]].dropna()

                if len(regression_df) > 20:
                    X = regression_df[predictors]
                    y = regression_df[embu_var]

                    X_sm = sm.add_constant(X)
                    model = sm.OLS(y, X_sm).fit()

                    print(f"  R² = {model.rsquared:.3f}, p = {model.f_pvalue:.4f}")

                    # Anlamlı yordayıcılar
                    significant_predictors = []
                    for i, var in enumerate(predictor_names):
                        if model.pvalues[i+1] < 0.05:
                            significant_predictors.append(f"{var} (B={model.params[i+1]:.3f}, p={model.pvalues[i+1]:.3f})")

                    if significant_predictors:
                        print(f"  Anlamlı yordayıcılar: {', '.join(significant_predictors)}")

                    regression_results[f'{subscale}_model'] = {
                        'r_squared': model.rsquared,
                        'coefficients': dict(zip(['Intercept'] + predictor_names, model.params))
                    }

        self.results['regression'] = regression_results
        return regression_results

    def subgroup_analysis(self):
        """Alt grup analizleri"""
        print("\n" + "="*80)
        print("ALT GRUP ANALİZLERİ")
        print("="*80)

        subgroup_results = {}

        # Yaş gruplarına göre analiz
        if 'Anne_Yas' in self.df.columns:
            print("\n1. ANNE YAŞI GRUPLARI")
            print("-" * 50)

            # Yaş kategorileri oluştur
            self.df['Anne_Yas_Grup'] = pd.cut(self.df['Anne_Yas'],
                                               bins=[0, 30, 40, 100],
                                               labels=['<30', '30-40', '>40'])

            # Beck skorlarını karşılaştır
            beck_col = None
            for col in ['Beck Toplam', 'Beck_Calculated_New']:
                if col in self.df.columns:
                    beck_col = col
                    break

            if beck_col:
                for yas_grup in self.df['Anne_Yas_Grup'].dropna().unique():
                    grup_data = self.df[self.df['Anne_Yas_Grup'] == yas_grup][beck_col].dropna()
                    if len(grup_data) > 0:
                        print(f"{yas_grup} yaş: Beck = {grup_data.mean():.2f} ± {grup_data.std():.2f} (n={len(grup_data)})")

                # ANOVA veya Kruskal-Wallis
                groups = []
                for yas_grup in self.df['Anne_Yas_Grup'].dropna().unique():
                    grup_data = self.df[self.df['Anne_Yas_Grup'] == yas_grup][beck_col].dropna()
                    if len(grup_data) > 0:
                        groups.append(grup_data)

                if len(groups) > 2:
                    stat, p_value = kruskal(*groups)
                    print(f"\nKruskal-Wallis: H = {stat:.3f}, p = {p_value:.4f}")

                    subgroup_results['anne_yas_gruplar'] = {
                        'test': 'Kruskal-Wallis',
                        'statistic': stat,
                        'p_value': p_value
                    }

        # Çocuk sayısına göre analiz
        if 'Cocuk_Sayisi' in self.df.columns:
            print("\n2. ÇOCUK SAYISI")
            print("-" * 50)

            self.df['Cocuk_Sayisi'] = pd.to_numeric(self.df['Cocuk_Sayisi'], errors='coerce')

            if beck_col:
                for cocuk_sayi in self.df['Cocuk_Sayisi'].dropna().unique():
                    grup_data = self.df[self.df['Cocuk_Sayisi'] == cocuk_sayi][beck_col].dropna()
                    if len(grup_data) > 0:
                        print(f"{int(cocuk_sayi)} çocuk: Beck = {grup_data.mean():.2f} ± {grup_data.std():.2f} (n={len(grup_data)})")

                # Korelasyon
                valid_idx = self.df[['Cocuk_Sayisi', beck_col]].dropna().index
                if len(valid_idx) > 10:
                    r, p = spearmanr(self.df.loc[valid_idx, 'Cocuk_Sayisi'],
                                    self.df.loc[valid_idx, beck_col])
                    print(f"\nÇocuk sayısı - Beck korelasyonu: r = {r:.3f}, p = {p:.4f}")

                    subgroup_results['cocuk_sayisi_beck'] = {
                        'r': r,
                        'p': p,
                        'n': len(valid_idx)
                    }

        self.results['subgroups'] = subgroup_results
        return subgroup_results

    def medical_factors_analysis(self):
        """Tıbbi faktörlerin analizi"""
        print("\n" + "="*80)
        print("TIBBİ FAKTÖRLER ANALİZİ")
        print("="*80)

        medical_results = {}

        # DM süresi analizi
        if 'DM_Suresi' in self.df.columns:
            print("\n1. DİYABET SÜRESİ")
            print("-" * 50)

            dm_data = self.df[self.df['Grup'] == 'Diyabet']['DM_Suresi'].dropna()

            if len(dm_data) > 0:
                print(f"Ortalama DM süresi: {dm_data.mean():.2f} ± {dm_data.std():.2f} yıl")
                print(f"Medyan: {dm_data.median():.2f} yıl")
                print(f"Min-Max: {dm_data.min():.2f} - {dm_data.max():.2f} yıl")

                # DM süresi ile Beck ilişkisi
                beck_col = None
                for col in ['Beck Toplam', 'Beck_Calculated_New']:
                    if col in self.df.columns:
                        beck_col = col
                        break

                if beck_col:
                    dm_df = self.df[self.df['Grup'] == 'Diyabet']
                    valid_idx = dm_df[['DM_Suresi', beck_col]].dropna().index

                    if len(valid_idx) > 5:
                        r, p = spearmanr(dm_df.loc[valid_idx, 'DM_Suresi'],
                                        dm_df.loc[valid_idx, beck_col])
                        print(f"\nDM süresi - Beck korelasyonu: r = {r:.3f}, p = {p:.4f}")

                        medical_results['dm_suresi_beck'] = {
                            'r': r,
                            'p': p,
                            'n': len(valid_idx)
                        }

        # Antidepresan kullanımı
        if 'Anne Antidepresan' in self.df.columns or 'Anne_Antidepresan' in self.df.columns:
            print("\n2. ANTİDEPRESAN KULLANIMI")
            print("-" * 50)

            anti_col = 'Anne Antidepresan' if 'Anne Antidepresan' in self.df.columns else 'Anne_Antidepresan'

            # Antidepresan kullanım oranları
            for grup in ['Diyabet', 'Kontrol']:
                grup_data = self.df[self.df['Grup'] == grup][anti_col]
                if len(grup_data) > 0:
                    kullanim = grup_data.notna().sum()
                    print(f"{grup}: {kullanim}/{len(grup_data)} ({kullanim/len(grup_data)*100:.1f}%)")

            # Gruplar arası karşılaştırma
            crosstab = pd.crosstab(self.df['Grup'], self.df[anti_col].notna())
            if crosstab.shape == (2, 2):
                odds_ratio, p_value = fisher_exact(crosstab)
                print(f"\nFisher's exact test: OR = {odds_ratio:.3f}, p = {p_value:.4f}")

                medical_results['antidepresan'] = {
                    'odds_ratio': odds_ratio,
                    'p_value': p_value
                }

        self.results['medical'] = medical_results
        return medical_results

    def create_comprehensive_visualizations(self):
        """Kapsamlı görselleştirmeler"""
        print("\n" + "="*80)
        print("GÖRSELLEŞTİRMELER")
        print("="*80)

        fig, axes = plt.subplots(2, 3, figsize=(16, 10))
        axes = axes.flatten()

        # Beck skorunu bul
        beck_col = None
        for col in ['Beck Toplam', 'Beck_Calculated_New']:
            if col in self.df.columns:
                beck_col = col
                break

        plot_idx = 0

        # 1. Anne yaşı - Beck scatter plot
        if 'Anne_Yas' in self.df.columns and beck_col and plot_idx < len(axes):
            ax = axes[plot_idx]
            for grup in ['Diyabet', 'Kontrol']:
                grup_data = self.df[self.df['Grup'] == grup]
                ax.scatter(grup_data['Anne_Yas'], grup_data[beck_col],
                          label=grup, alpha=0.6, s=50)

            ax.set_xlabel('Anne Yaşı', fontsize=10)
            ax.set_ylabel('Beck Skoru', fontsize=10)
            ax.set_title('Anne Yaşı - Depresyon İlişkisi', fontsize=11, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            plot_idx += 1

        # 2. Çocuk sayısı - Beck box plot
        if 'Cocuk_Sayisi' in self.df.columns and beck_col and plot_idx < len(axes):
            ax = axes[plot_idx]
            self.df['Cocuk_Sayisi'] = pd.to_numeric(self.df['Cocuk_Sayisi'], errors='coerce')

            data_to_plot = []
            labels = []
            for sayi in sorted(self.df['Cocuk_Sayisi'].dropna().unique()):
                if sayi <= 5:  # Maksimum 5 çocuk
                    data = self.df[self.df['Cocuk_Sayisi'] == sayi][beck_col].dropna()
                    if len(data) > 0:
                        data_to_plot.append(data)
                        labels.append(str(int(sayi)))

            if data_to_plot:
                bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True)
                for patch in bp['boxes']:
                    patch.set_facecolor('lightblue')
                    patch.set_alpha(0.7)

            ax.set_xlabel('Çocuk Sayısı', fontsize=10)
            ax.set_ylabel('Beck Skoru', fontsize=10)
            ax.set_title('Çocuk Sayısı - Depresyon', fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3)
            plot_idx += 1

        # 3. DM süresi histogram (sadece diyabet grubu)
        if 'DM_Suresi' in self.df.columns and plot_idx < len(axes):
            ax = axes[plot_idx]
            dm_data = self.df[self.df['Grup'] == 'Diyabet']['DM_Suresi'].dropna()

            if len(dm_data) > 0:
                ax.hist(dm_data, bins=15, color='coral', alpha=0.7, edgecolor='black')
                ax.axvline(dm_data.mean(), color='red', linestyle='--',
                          label=f'Ortalama: {dm_data.mean():.1f} yıl')
                ax.set_xlabel('Diyabet Süresi (yıl)', fontsize=10)
                ax.set_ylabel('Frekans', fontsize=10)
                ax.set_title('Diyabet Süresi Dağılımı', fontsize=11, fontweight='bold')
                ax.legend()
                ax.grid(True, alpha=0.3)
            plot_idx += 1

        # 4. Yaş grupları - Beck violin plot
        if 'Anne_Yas' in self.df.columns and beck_col and plot_idx < len(axes):
            ax = axes[plot_idx]

            # Yaş grupları
            self.df['Anne_Yas_Grup'] = pd.cut(self.df['Anne_Yas'],
                                               bins=[0, 30, 35, 40, 100],
                                               labels=['<30', '30-35', '35-40', '>40'])

            # Violin plot için veri hazırla
            plot_data = []
            positions = []
            colors = []
            pos = 0

            for grup in ['Diyabet', 'Kontrol']:
                for yas_grup in self.df['Anne_Yas_Grup'].dropna().unique():
                    data = self.df[(self.df['Grup'] == grup) &
                                  (self.df['Anne_Yas_Grup'] == yas_grup)][beck_col].dropna()
                    if len(data) > 2:
                        plot_data.append(data)
                        positions.append(pos)
                        colors.append('coral' if grup == 'Diyabet' else 'lightblue')
                        pos += 1

            if plot_data:
                parts = ax.violinplot(plot_data, positions=positions, widths=0.6)
                for i, pc in enumerate(parts['bodies']):
                    pc.set_facecolor(colors[i])
                    pc.set_alpha(0.7)

            ax.set_xlabel('Yaş Grupları', fontsize=10)
            ax.set_ylabel('Beck Skoru', fontsize=10)
            ax.set_title('Yaş Grupları - Depresyon', fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3)
            plot_idx += 1

        # 5. Çalışma durumu - Beck
        if 'Calisma_Durumu' in self.df.columns and beck_col and plot_idx < len(axes):
            ax = axes[plot_idx]

            data_to_plot = []
            labels = []
            colors = []

            for grup in ['Diyabet', 'Kontrol']:
                for calisma in [True, False]:
                    if calisma:
                        data = self.df[(self.df['Grup'] == grup) &
                                      self.df['Calisma_Durumu'].notna()][beck_col].dropna()
                        label = f"{grup}\nÇalışıyor"
                    else:
                        data = self.df[(self.df['Grup'] == grup) &
                                      self.df['Calisma_Durumu'].isna()][beck_col].dropna()
                        label = f"{grup}\nÇalışmıyor"

                    if len(data) > 0:
                        data_to_plot.append(data)
                        labels.append(label)
                        colors.append('coral' if grup == 'Diyabet' else 'lightblue')

            if data_to_plot:
                bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True)
                for patch, color in zip(bp['boxes'], colors):
                    patch.set_facecolor(color)
                    patch.set_alpha(0.7)

            ax.set_ylabel('Beck Skoru', fontsize=10)
            ax.set_title('Çalışma Durumu - Depresyon', fontsize=11, fontweight='bold')
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3)
            plot_idx += 1

        # 6. Korelasyon ısı haritası
        if plot_idx < len(axes):
            ax = axes[plot_idx]

            # Korelasyon için değişkenler
            corr_vars = []
            for var in ['Anne_Yas', 'Cocuk_Sayisi', beck_col, 'DM_Suresi']:
                if var in self.df.columns:
                    corr_vars.append(var)

            if len(corr_vars) > 2:
                corr_data = self.df[corr_vars].dropna()
                if len(corr_data) > 10:
                    corr_matrix = corr_data.corr(method='spearman')

                    im = ax.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
                    ax.set_xticks(range(len(corr_vars)))
                    ax.set_yticks(range(len(corr_vars)))
                    ax.set_xticklabels(corr_vars, rotation=45, ha='right')
                    ax.set_yticklabels(corr_vars)

                    # Korelasyon değerlerini ekle
                    for i in range(len(corr_vars)):
                        for j in range(len(corr_vars)):
                            text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                         ha="center", va="center", color="black", fontsize=8)

                    ax.set_title('Korelasyon Matrisi', fontsize=11, fontweight='bold')
                    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

        # Kullanılmayan subplot'ları gizle
        for idx in range(plot_idx, len(axes)):
            axes[idx].axis('off')

        plt.suptitle('Demografik ve Tıbbi Faktörler - Kapsamlı Analiz',
                    fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig('results/demographic_comprehensive_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()

        print("[OK] Görselleştirmeler kaydedildi: demographic_comprehensive_analysis.png")

    def generate_report(self):
        """Detaylı rapor oluştur"""
        print("\n" + "="*80)
        print("RAPOR OLUŞTURMA")
        print("="*80)

        report_lines = []
        report_lines.append("="*80)
        report_lines.append("DEMOGRAFİK VE TIBBİ VERİ ANALİZİ RAPORU")
        report_lines.append("="*80)
        report_lines.append(f"\nTarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report_lines.append(f"Veri: {self.data_path}")
        report_lines.append(f"Toplam kayıt: {len(self.df)}")

        # 1. TANIMLAYICI İSTATİSTİKLER
        report_lines.append("\n" + "="*80)
        report_lines.append("1. GRUPLAR ARASI DEMOGRAFİK FARKLARI")
        report_lines.append("="*80)

        if 'descriptive' in self.results:
            significant_diffs = []
            for var, result in self.results['descriptive'].items():
                if isinstance(result, dict) and result.get('significant', False):
                    if 'diyabet_mean' in result:
                        significant_diffs.append(
                            f"{var}: Diyabet={result['diyabet_mean']:.2f}, "
                            f"Kontrol={result['kontrol_mean']:.2f}, p={result['p_value']:.4f}"
                        )

            if significant_diffs:
                report_lines.append("\nAnlamlı farklılıklar:")
                for diff in significant_diffs:
                    report_lines.append(f"  • {diff}")
            else:
                report_lines.append("\nGruplar arası demografik açıdan anlamlı fark bulunmamıştır.")

        # 2. KORELASYONLAR
        report_lines.append("\n" + "="*80)
        report_lines.append("2. DEMOGRAFİK DEĞİŞKENLER - DEPRESYON/EMBU İLİŞKİLERİ")
        report_lines.append("="*80)

        if 'correlations' in self.results:
            if self.results['correlations']:
                report_lines.append("\nAnlamlı korelasyonlar:")
                for pair, corr in self.results['correlations'].items():
                    report_lines.append(f"  • {pair}: r = {corr['r']:.3f}, p = {corr['p']:.4f}")
            else:
                report_lines.append("\nAnlamlı korelasyon bulunmamıştır.")

        # 3. REGRESYON ANALİZİ
        report_lines.append("\n" + "="*80)
        report_lines.append("3. ÇOKLU REGRESYON ANALİZİ")
        report_lines.append("="*80)

        if 'regression' in self.results and 'beck_model' in self.results['regression']:
            model = self.results['regression']['beck_model']
            report_lines.append(f"\nBeck Depresyon Modeli:")
            report_lines.append(f"  R² = {model['r_squared']:.3f}")
            report_lines.append(f"  Adjusted R² = {model['adj_r_squared']:.3f}")
            report_lines.append(f"  F = {model['f_statistic']:.2f}, p = {model['p_value']:.4f}")

            report_lines.append("\nAnlamlı yordayıcılar:")
            for var, p_val in model['p_values'].items():
                if p_val < 0.05 and var != 'Intercept':
                    coef = model['coefficients'][var]
                    report_lines.append(f"  - {var}: B = {coef:.3f}, p = {p_val:.4f}")

        # 4. TIBBİ FAKTÖRLER
        report_lines.append("\n" + "="*80)
        report_lines.append("4. TIBBİ FAKTÖRLER")
        report_lines.append("="*80)

        if 'medical' in self.results:
            if 'dm_suresi_beck' in self.results['medical']:
                dm_corr = self.results['medical']['dm_suresi_beck']
                report_lines.append(f"\nDM süresi - Beck korelasyonu:")
                report_lines.append(f"  r = {dm_corr['r']:.3f}, p = {dm_corr['p']:.4f}")

            if 'antidepresan' in self.results['medical']:
                anti = self.results['medical']['antidepresan']
                report_lines.append(f"\nAntidepresan kullanımı:")
                report_lines.append(f"  Odds Ratio = {anti['odds_ratio']:.3f}, p = {anti['p_value']:.4f}")

        # 5. SONUÇ VE ÖNERİLER
        report_lines.append("\n" + "="*80)
        report_lines.append("5. SONUÇ VE ÖNERİLER")
        report_lines.append("="*80)

        report_lines.append("\nANA BULGULAR:")
        report_lines.append("• Demografik faktörlerin depresyon üzerinde etkisi değerlendirilmiştir")
        report_lines.append("• Yaş, çocuk sayısı gibi faktörler analiz edilmiştir")
        report_lines.append("• Tıbbi faktörlerin rolü incelenmiştir")

        report_lines.append("\nÖNERİLER:")
        report_lines.append("• Risk gruplarına yönelik tarama programları geliştirilmeli")
        report_lines.append("• Demografik risk faktörleri dikkate alınmalı")
        report_lines.append("• Longitudinal takip çalışmaları planlanmalı")

        report_lines.append("\n" + "="*80)

        # Raporu kaydet
        report_text = "\n".join(report_lines)

        with open('results/demographic_analysis_report.txt', 'w', encoding='utf-8') as f:
            f.write(report_text)

        print("[OK] Demografik analiz raporu kaydedildi: demographic_analysis_report.txt")

        # JSON olarak da kaydet
        with open('results/demographic_analysis_results.json', 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': self.results,
                'n_samples': len(self.df)
            }, f, indent=2, default=str)

        print("[OK] JSON sonuçları kaydedildi: demographic_analysis_results.json")

        return report_text

    def run_complete_analysis(self):
        """Tüm analizleri çalıştır"""
        print("\n" + "="*80)
        print("KAPSAMLI DEMOGRAFİK ANALİZ BAŞLIYOR")
        print("="*80)

        # 1. Veri yükleme ve hazırlama
        self.load_and_prepare_data()

        # 2. Tanımlayıcı istatistikler
        self.descriptive_analysis()

        # 3. Korelasyon analizleri
        self.correlation_analysis()

        # 4. Regresyon analizi
        self.regression_analysis()

        # 5. Alt grup analizleri
        self.subgroup_analysis()

        # 6. Tıbbi faktörler analizi
        self.medical_factors_analysis()

        # 7. Görselleştirmeler
        self.create_comprehensive_visualizations()

        # 8. Rapor oluştur
        self.generate_report()

        print("\n" + "="*80)
        print("ANALİZ TAMAMLANDI")
        print("="*80)

        return self.results

def main():
    """Ana fonksiyon"""

    try:
        # Demografik analiz sınıfını başlat
        demographic_analysis = DemographicAnalysis()

        # Tüm analizleri çalıştır
        results = demographic_analysis.run_complete_analysis()

        print("\n" + "="*80)
        print("BAŞARILI")
        print("="*80)
        print("\nOluşturulan dosyalar:")
        print("  - results/demographic_analysis_report.txt")
        print("  - results/demographic_analysis_results.json")
        print("  - results/demographic_comprehensive_analysis.png")

        return results

    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()