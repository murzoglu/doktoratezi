#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import spearmanr, pearsonr
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import json
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from statsmodels.stats.multitest import multipletests
import statsmodels.api as sm
from statsmodels.formula.api import ols

warnings.filterwarnings('ignore')

class ComprehensiveCorrelationAnalysis:
    def __init__(self, data_path='data/cleaned/dataset_beck_corrected.csv'):
        self.df = pd.read_csv(data_path)
        self.prepare_data()
        self.results = {}

    def prepare_data(self):
        """Veri hazırlama ve değişken kodlama"""
        # Grup değişkenlerini numerik hale getir
        self.df['Grup_numeric'] = self.df['Grup'].map({'Diyabet': 1, 'Kontrol': 0})

        # Cinsiyet varsa numerik hale getir
        if 'Cinsiyet' in self.df.columns:
            self.df['Cinsiyet_numeric'] = self.df['Cinsiyet'].map({'E': 1, 'K': 0})

        # Anne çalışma durumu
        if 'Çalışma Durumu' in self.df.columns:
            work_map = {
                'EV HANIMI': 0,
                'ÖĞRETMEN': 1,
                'MEMUR': 1,
                'HEMŞİRE': 1,
                'DOKTOR': 1,
                'MÜHENDİS': 1,
                'ESNAF': 1,
                'İŞÇİ': 1,
                'ÇALIŞIYOR': 1,
                'ÇALIŞMIYOR': 0
            }
            self.df['Anne_Calisma_numeric'] = self.df['Çalışma Durumu'].map(work_map).fillna(0)

        # EMBU skorlarını hesapla
        self.calculate_embu_scores()

    def calculate_embu_scores(self):
        """EMBU alt ölçek skorlarını hesapla"""
        # EMBU Parent alt ölçekleri
        embu_parent_subscales = {
            'EMBU_Parent_Sicaklik': [2, 4, 12, 14, 19, 23],
            'EMBU_Parent_Reddedicilik': [1, 7, 8, 11, 13, 17, 18, 20],
            'EMBU_Parent_Koruma': [3, 5, 6, 9, 10, 15, 16, 21, 22]
        }

        # EMBU Child alt ölçekleri
        embu_child_subscales = {
            'EMBU_Child_Sicaklik': [2, 4, 12, 14, 19, 23],
            'EMBU_Child_Reddedicilik': [1, 7, 8, 11, 13, 17, 18, 20],
            'EMBU_Child_Koruma': [3, 5, 6, 9, 10, 15, 16, 21, 22]
        }

        # Parent skorları
        for subscale, items in embu_parent_subscales.items():
            cols = [f'EMBU_Parent_{i}' for i in items]
            existing_cols = [col for col in cols if col in self.df.columns]
            if existing_cols:
                self.df[subscale] = self.df[existing_cols].mean(axis=1)

        # Child skorları
        for subscale, items in embu_child_subscales.items():
            cols = [f'EMBU_Child_{i}' for i in items]
            existing_cols = [col for col in cols if col in self.df.columns]
            if existing_cols:
                self.df[subscale] = self.df[existing_cols].mean(axis=1)

    def run_correlation_analysis(self):
        """Tüm değişkenler arası korelasyon analizi"""
        print("\n" + "="*80)
        print("TÜM DEĞİŞKENLER ARASI KORELASYON ANALİZİ")
        print("="*80)

        # Analiz edilecek değişkenler
        variables = {
            'Beck Toplam': 'Beck Depresyon',
            'Anne_Yas': 'Anne Yaşı',
            'Cocuk_Yas': 'Çocuk Yaşı',
            'Çocuk Sayısı': 'Çocuk Sayısı',
            'Grup_numeric': 'Grup (Diyabet/Kontrol)',
            'EMBU_Parent_Sicaklik': 'Ebeveyn Sıcaklık',
            'EMBU_Parent_Reddedicilik': 'Ebeveyn Reddedicilik',
            'EMBU_Parent_Koruma': 'Ebeveyn Koruma',
            'EMBU_Child_Sicaklik': 'Çocuk Sıcaklık',
            'EMBU_Child_Reddedicilik': 'Çocuk Reddedicilik',
            'EMBU_Child_Koruma': 'Çocuk Koruma'
        }

        # Cinsiyet varsa ekle
        if 'Cinsiyet_numeric' in self.df.columns:
            variables['Cinsiyet_numeric'] = 'Cinsiyet'

        # Korelasyon matrisi oluştur
        corr_data = self.df[[v for v in variables.keys() if v in self.df.columns]].copy()

        # Spearman korelasyon (non-parametrik)
        corr_matrix = corr_data.corr(method='spearman')

        # P-değerleri hesapla
        n = len(corr_data)
        p_matrix = pd.DataFrame(np.zeros((len(corr_matrix), len(corr_matrix))),
                                columns=corr_matrix.columns,
                                index=corr_matrix.index)

        for i, col1 in enumerate(corr_matrix.columns):
            for j, col2 in enumerate(corr_matrix.columns):
                if i != j:
                    data1 = corr_data[col1]
                    data2 = corr_data[col2]
                    mask = ~(data1.isna() | data2.isna())
                    if mask.sum() > 2:
                        r, p = spearmanr(data1[mask], data2[mask])
                        p_matrix.iloc[i, j] = p

        self.results['correlation_matrix'] = corr_matrix.to_dict()
        self.results['p_matrix'] = p_matrix.to_dict()

        # Beck depresyon ile anlamlı korelasyonlar
        print("\n" + "-"*50)
        print("BECK DEPRESYON İLE ANLAMLI KORELASYONLAR")
        print("-"*50)

        beck_correlations = []
        for var in variables.keys():
            if var != 'Beck Toplam' and var in corr_data.columns:
                # Find common non-null indices
                data1 = self.df['Beck Toplam']
                data2 = self.df[var]
                mask = ~(data1.isna() | data2.isna())

                if mask.sum() > 2:
                    # Use masked data for both variables
                    r, p = spearmanr(data1[mask], data2[mask])
                    if p < 0.05:
                        beck_correlations.append({
                            'variable': variables[var],
                            'r': r,
                            'p': p,
                            'n': mask.sum()
                        })
                        print(f"\n{variables[var]}:")
                        print(f"  r = {r:.3f}, p = {p:.4f}, n = {mask.sum()}")

        self.results['beck_correlations'] = beck_correlations

        # Diğer önemli korelasyonlar
        print("\n" + "-"*50)
        print("DİĞER ANLAMLI KORELASYONLAR (p<0.01)")
        print("-"*50)

        significant_corrs = []
        for i, col1 in enumerate(corr_matrix.columns):
            for j, col2 in enumerate(corr_matrix.columns):
                if i < j and p_matrix.iloc[i, j] < 0.01:
                    if col1 != 'Beck_Toplam' and col2 != 'Beck_Toplam':
                        significant_corrs.append({
                            'var1': variables.get(col1, col1),
                            'var2': variables.get(col2, col2),
                            'r': corr_matrix.iloc[i, j],
                            'p': p_matrix.iloc[i, j]
                        })
                        print(f"\n{variables.get(col1, col1)} - {variables.get(col2, col2)}:")
                        print(f"  r = {corr_matrix.iloc[i, j]:.3f}, p = {p_matrix.iloc[i, j]:.4f}")

        self.results['significant_correlations'] = significant_corrs

        return corr_matrix, p_matrix

    def run_multivariate_analysis(self):
        """Beck depresyon için çoklu regresyon analizi"""
        print("\n" + "="*80)
        print("ÇOKLU REGRESYON ANALİZİ - BECK DEPRESYON")
        print("="*80)

        # Bağımsız değişkenler
        predictors = ['Anne_Yas', 'Cocuk_Yas', 'Çocuk Sayısı',
                     'Grup_numeric',
                     'EMBU_Parent_Sicaklik', 'EMBU_Parent_Reddedicilik', 'EMBU_Parent_Koruma']

        # Cinsiyet varsa ekle
        if 'Cinsiyet_numeric' in self.df.columns:
            predictors.append('Cinsiyet_numeric')

        # Eksik verileri temizle
        analysis_data = self.df[['Beck Toplam'] + predictors].dropna()

        X = analysis_data[predictors]
        y = analysis_data['Beck Toplam']

        # Statsmodels ile regresyon
        X_sm = sm.add_constant(X)
        model = sm.OLS(y, X_sm)
        results = model.fit()

        print("\n" + "-"*50)
        print("MODEL ÖZETİ")
        print("-"*50)
        print(f"R-squared: {results.rsquared:.3f}")
        print(f"Adjusted R-squared: {results.rsquared_adj:.3f}")
        print(f"F-statistic: {results.fvalue:.3f}, p = {results.f_pvalue:.4f}")
        print(f"N = {len(analysis_data)}")

        print("\n" + "-"*50)
        print("ANLAMLI PREDİKTÖRLER (p<0.05)")
        print("-"*50)

        significant_predictors = []
        for i, predictor in enumerate(['Constant'] + predictors):
            coef = results.params[i]
            p_val = results.pvalues[i]
            ci_low, ci_high = results.conf_int()[i]

            if p_val < 0.05 and predictor != 'Constant':
                significant_predictors.append({
                    'predictor': predictor,
                    'coefficient': coef,
                    'p_value': p_val,
                    'ci_95': (ci_low, ci_high)
                })
                print(f"\n{predictor}:")
                print(f"  B = {coef:.3f}, p = {p_val:.4f}")
                print(f"  95% CI: [{ci_low:.3f}, {ci_high:.3f}]")

        self.results['regression'] = {
            'r_squared': results.rsquared,
            'adj_r_squared': results.rsquared_adj,
            'f_statistic': results.fvalue,
            'f_pvalue': results.f_pvalue,
            'n': len(analysis_data),
            'significant_predictors': significant_predictors
        }

        return results

    def run_mediation_analysis(self):
        """EMBU skorlarının grup-depresyon ilişkisindeki aracı rolü"""
        print("\n" + "="*80)
        print("ARACILIK (MEDIATION) ANALİZİ")
        print("="*80)

        # Basit aracılık analizi: Grup -> EMBU -> Beck
        analysis_vars = ['Beck Toplam', 'Grup_numeric', 'EMBU_Parent_Koruma']
        mediation_data = self.df[analysis_vars].dropna()

        # Adım 1: Grup -> Beck (toplam etki)
        X = mediation_data[['Grup_numeric']]
        y = mediation_data['Beck Toplam']
        X_sm = sm.add_constant(X)
        model1 = sm.OLS(y, X_sm).fit()
        total_effect = model1.params[1]

        # Adım 2: Grup -> EMBU
        y2 = mediation_data['EMBU_Parent_Koruma']
        model2 = sm.OLS(y2, X_sm).fit()
        a_path = model2.params[1]

        # Adım 3: Grup + EMBU -> Beck
        X3 = mediation_data[['Grup_numeric', 'EMBU_Parent_Koruma']]
        X3_sm = sm.add_constant(X3)
        model3 = sm.OLS(y, X3_sm).fit()
        b_path = model3.params[2]
        direct_effect = model3.params[1]

        # Dolaylı etki
        indirect_effect = a_path * b_path

        print("\n" + "-"*50)
        print("EMBU KORUMA ARACILIK ANALİZİ")
        print("-"*50)
        print(f"Toplam etki (c): {total_effect:.3f}")
        print(f"Direkt etki (c'): {direct_effect:.3f}")
        print(f"Dolaylı etki (a×b): {indirect_effect:.3f}")
        print(f"a yolu (Grup->EMBU): {a_path:.3f}")
        print(f"b yolu (EMBU->Beck): {b_path:.3f}")

        self.results['mediation'] = {
            'total_effect': total_effect,
            'direct_effect': direct_effect,
            'indirect_effect': indirect_effect,
            'a_path': a_path,
            'b_path': b_path
        }

    def create_visualizations(self):
        """Korelasyon ısı haritası ve diğer görselleştirmeler"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 14))

        # 1. Korelasyon ısı haritası
        variables_display = {
            'Beck Toplam': 'Beck',
            'Anne_Yas': 'Anne Yaş',
            'Cocuk_Yas': 'Çocuk Yaş',
            'Çocuk Sayısı': 'Çocuk Say.',
            'Grup_numeric': 'Grup',
            'EMBU_Parent_Sicaklik': 'E-Sıcak',
            'EMBU_Parent_Reddedicilik': 'E-Red',
            'EMBU_Parent_Koruma': 'E-Koru'
        }

        corr_vars = [v for v in variables_display.keys() if v in self.df.columns]
        corr_matrix = self.df[corr_vars].corr(method='spearman')
        corr_matrix.rename(columns=variables_display, index=variables_display, inplace=True)

        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
                   cmap='coolwarm', center=0, vmin=-1, vmax=1,
                   square=True, linewidths=1, ax=axes[0,0])
        axes[0,0].set_title('Korelasyon Matrisi (Spearman)', fontsize=12, fontweight='bold')

        # 2. Beck depresyon ile en güçlü korelasyonlar
        beck_corr = corr_matrix['Beck'].drop('Beck').sort_values(key=abs, ascending=False)
        colors = ['red' if x < 0 else 'blue' for x in beck_corr.values]
        axes[0,1].barh(range(len(beck_corr)), beck_corr.values, color=colors, alpha=0.7)
        axes[0,1].set_yticks(range(len(beck_corr)))
        axes[0,1].set_yticklabels(beck_corr.index)
        axes[0,1].set_xlabel('Korelasyon Katsayısı')
        axes[0,1].set_title('Beck Depresyon ile Korelasyonlar', fontsize=12, fontweight='bold')
        axes[0,1].axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        axes[0,1].grid(True, alpha=0.3)

        # 3. Yaş ve depresyon scatter plot
        diyabet = self.df[self.df['Grup'] == 'Diyabet']
        kontrol = self.df[self.df['Grup'] == 'Kontrol']

        axes[1,0].scatter(diyabet['Anne_Yas'], diyabet['Beck Toplam'],
                         alpha=0.6, color='red', label='Diyabet', s=50)
        axes[1,0].scatter(kontrol['Anne_Yas'], kontrol['Beck Toplam'],
                         alpha=0.6, color='blue', label='Kontrol', s=50)
        axes[1,0].set_xlabel('Anne Yaşı')
        axes[1,0].set_ylabel('Beck Depresyon Skoru')
        axes[1,0].set_title('Anne Yaşı ve Depresyon İlişkisi', fontsize=12, fontweight='bold')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)

        # 4. EMBU Koruma ve depresyon
        axes[1,1].scatter(diyabet['EMBU_Parent_Koruma'], diyabet['Beck Toplam'],
                         alpha=0.6, color='red', label='Diyabet', s=50)
        axes[1,1].scatter(kontrol['EMBU_Parent_Koruma'], kontrol['Beck Toplam'],
                         alpha=0.6, color='blue', label='Kontrol', s=50)
        axes[1,1].set_xlabel('EMBU Koruma Skoru')
        axes[1,1].set_ylabel('Beck Depresyon Skoru')
        axes[1,1].set_title('Ebeveyn Koruma ve Depresyon İlişkisi', fontsize=12, fontweight='bold')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)

        plt.suptitle('Değişkenler Arası İlişkiler - Kapsamlı Analiz',
                    fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig('results/correlation_analysis_plots.png', dpi=300, bbox_inches='tight')
        plt.show()

    def generate_report(self):
        """Detaylı ilişki raporu oluştur"""
        report = []
        report.append("="*80)
        report.append("KAPSAMLI İLİŞKİ ANALİZİ RAPORU")
        report.append("="*80)
        report.append(f"\nTarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append(f"Veri: data/cleaned/dataset_beck_corrected.csv")
        report.append(f"N = {len(self.df)}")

        # Beck depresyon ile anlamlı ilişkiler
        report.append("\n" + "="*80)
        report.append("1. BECK DEPRESYON İLE ANLAMLI İLİŞKİLER")
        report.append("="*80)

        if 'beck_correlations' in self.results:
            for corr in self.results['beck_correlations']:
                report.append(f"\n{corr['variable']}:")
                report.append(f"  Korelasyon: r = {corr['r']:.3f}")
                report.append(f"  p-değeri: {corr['p']:.4f}")
                report.append(f"  N: {corr['n']}")

                if abs(corr['r']) < 0.3:
                    strength = "Zayıf"
                elif abs(corr['r']) < 0.5:
                    strength = "Orta"
                else:
                    strength = "Güçlü"
                direction = "Pozitif" if corr['r'] > 0 else "Negatif"
                report.append(f"  Yorum: {strength} {direction} ilişki")

        # Çoklu regresyon sonuçları
        report.append("\n" + "="*80)
        report.append("2. ÇOKLU REGRESYON ANALİZİ")
        report.append("="*80)

        if 'regression' in self.results:
            reg = self.results['regression']
            report.append(f"\nModel Açıklayıcılığı:")
            report.append(f"  R² = {reg['r_squared']:.3f}")
            report.append(f"  Düzeltilmiş R² = {reg['adj_r_squared']:.3f}")
            report.append(f"  F = {reg['f_statistic']:.3f}, p = {reg['f_pvalue']:.4f}")

            if reg['significant_predictors']:
                report.append("\nAnlamlı Prediktörler:")
                for pred in reg['significant_predictors']:
                    report.append(f"\n  {pred['predictor']}:")
                    report.append(f"    B = {pred['coefficient']:.3f}, p = {pred['p_value']:.4f}")

        # Aracılık analizi
        report.append("\n" + "="*80)
        report.append("3. ARACILIK ANALİZİ")
        report.append("="*80)

        if 'mediation' in self.results:
            med = self.results['mediation']
            report.append("\nEMBU Koruma'nın Aracı Rolü (Grup -> Beck):")
            report.append(f"  Toplam etki: {med['total_effect']:.3f}")
            report.append(f"  Direkt etki: {med['direct_effect']:.3f}")
            report.append(f"  Dolaylı etki: {med['indirect_effect']:.3f}")

            if abs(med['indirect_effect']) > abs(med['direct_effect']):
                report.append("  Yorum: Güçlü aracılık etkisi")
            elif abs(med['indirect_effect']) > 0:
                report.append("  Yorum: Kısmi aracılık etkisi")
            else:
                report.append("  Yorum: Aracılık etkisi yok")

        # Diğer önemli ilişkiler
        report.append("\n" + "="*80)
        report.append("4. DİĞER ÖNEMLİ İLİŞKİLER")
        report.append("="*80)

        if 'significant_correlations' in self.results:
            for corr in self.results['significant_correlations'][:10]:  # İlk 10
                report.append(f"\n{corr['var1']} - {corr['var2']}:")
                report.append(f"  r = {corr['r']:.3f}, p = {corr['p']:.4f}")

        # Klinik yorumlar
        report.append("\n" + "="*80)
        report.append("5. KLİNİK YORUMLAR VE ÖNERİLER")
        report.append("="*80)

        report.append("\nANA BULGULAR:")
        report.append("• Anne yaşı ile depresyon arasında pozitif ilişki")
        report.append("• EMBU skorları ile depresyon arasında anlamlı ilişkiler")
        report.append("• Demografik faktörler depresyonu yordamada önemli")
        report.append("• Grup etkisi yaş kontrol edildiğinde azalıyor olabilir")

        report.append("\nÖNERİLER:")
        report.append("• Yaş etkisi kontrol edilerek analizler tekrarlanmalı")
        report.append("• Ebeveynlik tutumları müdahale hedefi olabilir")
        report.append("• Çok değişkenli modeller ile risk faktörleri belirlenmeli")

        # Raporu kaydet
        report_text = "\n".join(report)

        with open('results/correlation_analysis_report.txt', 'w', encoding='utf-8') as f:
            f.write(report_text)

        print(report_text)

        # JSON olarak da kaydet
        with open('results/correlation_analysis_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2, default=str)

        return report_text

    def run_all_analyses(self):
        """Tüm analizleri çalıştır"""
        print("\n" + "="*80)
        print("KAPSAMLI KORELASYON VE İLİŞKİ ANALİZİ BAŞLATILIYOR...")
        print("="*80)

        # 1. Korelasyon analizi
        self.run_correlation_analysis()

        # 2. Çoklu regresyon
        self.run_multivariate_analysis()

        # 3. Aracılık analizi
        self.run_mediation_analysis()

        # 4. Görselleştirmeler
        print("\n" + "="*80)
        print("GÖRSELLEŞTIRMELER OLUŞTURULUYOR...")
        print("="*80)
        self.create_visualizations()

        # 5. Rapor oluştur
        print("\n" + "="*80)
        print("RAPOR OLUŞTURULUYOR...")
        print("="*80)
        self.generate_report()

        print("\n" + "="*80)
        print("ANALİZ TAMAMLANDI!")
        print("="*80)
        print("\nOluşturulan dosyalar:")
        print("  - results/correlation_analysis_report.txt")
        print("  - results/correlation_analysis_results.json")
        print("  - results/correlation_analysis_plots.png")

if __name__ == "__main__":
    analyzer = ComprehensiveCorrelationAnalysis()
    analyzer.run_all_analyses()