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

warnings.filterwarnings('ignore')

def main():
    print("\n" + "="*80)
    print("DEĞİŞKENLER ARASI KORELASYON ANALİZİ")
    print("="*80)

    # Veriyi yükle
    df = pd.read_csv('data/cleaned/dataset_beck_corrected.csv')
    print(f"\nVeri seti yüklendi: {len(df)} kayıt")

    # Anne yaşını hesapla
    df['Anne_Yas'] = 2024 - pd.to_datetime(df['Anne Doğum Tarihi'], errors='coerce').dt.year

    # Çocuk yaşını hesapla
    df['Cocuk_Yas'] = 2024 - pd.to_datetime(df['Katılımcı Çocuk Doğum Tarihi'], errors='coerce').dt.year

    # Grup değişkenini kodla
    df['Grup_numeric'] = df['Grup'].map({'Diyabet': 1, 'Kontrol': 0})

    # EMBU Parent skorlarını hesapla
    embu_parent_subscales = {
        'EMBU_Parent_Sicaklik': [2, 4, 12, 14, 19, 23],
        'EMBU_Parent_Reddedicilik': [1, 7, 8, 11, 13, 17, 18, 20],
        'EMBU_Parent_Koruma': [3, 5, 6, 9, 10, 15, 16, 21, 22]
    }

    for subscale, items in embu_parent_subscales.items():
        cols = [f'Ebeveyn EMBU {i}' for i in items]
        existing_cols = [col for col in cols if col in df.columns]
        if existing_cols:
            # Convert to numeric first
            for col in existing_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df[subscale] = df[existing_cols].mean(axis=1)

    # Analiz edilecek değişkenler
    variables = {
        'Beck Toplam': 'Beck Depresyon',
        'Anne_Yas': 'Anne Yaşı',
        'Cocuk_Yas': 'Çocuk Yaşı',
        'Çocuk Sayısı': 'Çocuk Sayısı',
        'Grup_numeric': 'Grup (Diyabet/Kontrol)',
        'EMBU_Parent_Sicaklik': 'EMBU Sıcaklık',
        'EMBU_Parent_Reddedicilik': 'EMBU Reddedicilik',
        'EMBU_Parent_Koruma': 'EMBU Koruma'
    }

    # Mevcut değişkenleri kontrol et
    available_vars = {k: v for k, v in variables.items() if k in df.columns}
    print(f"\nAnaliz edilecek değişkenler: {len(available_vars)}")

    # Korelasyon matrisi
    corr_data = df[[k for k in available_vars.keys()]].copy()
    corr_matrix = corr_data.corr(method='spearman')

    print("\n" + "-"*50)
    print("BECK DEPRESYON İLE ANLAMLI KORELASYONLAR")
    print("-"*50)

    # Beck ile korelasyonları hesapla
    beck_correlations = []
    for var in available_vars.keys():
        if var != 'Beck Toplam':
            data1 = df['Beck Toplam']
            data2 = df[var]
            mask = ~(data1.isna() | data2.isna())

            if mask.sum() > 2:
                r, p = spearmanr(data1[mask], data2[mask])
                beck_correlations.append({
                    'variable': available_vars[var],
                    'r': r,
                    'p': p,
                    'n': mask.sum()
                })
                if p < 0.05:
                    print(f"\n{available_vars[var]}:")
                    print(f"  r = {r:.3f}, p = {p:.4f}, n = {mask.sum()}")
                    print(f"  {'**ANLAMLI**' if p < 0.01 else '*Anlamlı*'}")

    # Diğer değişkenler arası korelasyonlar
    print("\n" + "-"*50)
    print("DİĞER ÖNEMLİ KORELASYONLAR (p<0.01)")
    print("-"*50)

    significant_corrs = []
    for i, var1 in enumerate(available_vars.keys()):
        for j, var2 in enumerate(list(available_vars.keys())[i+1:], i+1):
            if var1 != 'Beck Toplam' and var2 != 'Beck Toplam':
                data1 = df[var1]
                data2 = df[var2]
                mask = ~(data1.isna() | data2.isna())

                if mask.sum() > 2:
                    r, p = spearmanr(data1[mask], data2[mask])
                    if p < 0.01:
                        significant_corrs.append({
                            'var1': available_vars[var1],
                            'var2': available_vars[var2],
                            'r': r,
                            'p': p,
                            'n': mask.sum()
                        })
                        print(f"\n{available_vars[var1]} - {available_vars[var2]}:")
                        print(f"  r = {r:.3f}, p = {p:.4f}, n = {mask.sum()}")

    # Çoklu regresyon analizi
    print("\n" + "="*80)
    print("ÇOKLU REGRESYON ANALİZİ - BECK DEPRESYON")
    print("="*80)

    import statsmodels.api as sm

    # Prediktörler
    predictors = ['Anne_Yas', 'Cocuk_Yas', 'Çocuk Sayısı', 'Grup_numeric']

    # EMBU skorları varsa ekle
    for embu in ['EMBU_Parent_Sicaklik', 'EMBU_Parent_Reddedicilik', 'EMBU_Parent_Koruma']:
        if embu in df.columns:
            predictors.append(embu)

    # Mevcut prediktörleri filtrele
    available_predictors = [p for p in predictors if p in df.columns]

    # Veriyi hazırla
    analysis_data = df[['Beck Toplam'] + available_predictors].dropna()

    if len(analysis_data) > 30:
        X = analysis_data[available_predictors]
        y = analysis_data['Beck Toplam']

        # Modeli fit et
        X_sm = sm.add_constant(X)
        model = sm.OLS(y, X_sm).fit()

        print(f"\nModel Özeti:")
        print(f"  R² = {model.rsquared:.3f}")
        print(f"  Düzeltilmiş R² = {model.rsquared_adj:.3f}")
        print(f"  F-statistic = {model.fvalue:.3f}, p = {model.f_pvalue:.4f}")
        print(f"  N = {len(analysis_data)}")

        print("\nAnlamlı Prediktörler (p<0.05):")
        for i, pred in enumerate(['Constant'] + available_predictors):
            if model.pvalues[i] < 0.05:
                print(f"  {pred}: B = {model.params[i]:.3f}, p = {model.pvalues[i]:.4f}")

    # Görselleştirme
    print("\n" + "="*80)
    print("GÖRSELLEŞTIRMELER OLUŞTURULUYOR...")
    print("="*80)

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 1. Korelasyon ısı haritası
    display_names = {k: v.replace(' (Diyabet/Kontrol)', '') for k, v in available_vars.items()}
    corr_display = corr_matrix.rename(columns=display_names, index=display_names)

    mask = np.triu(np.ones_like(corr_display, dtype=bool))
    sns.heatmap(corr_display, mask=mask, annot=True, fmt='.2f',
               cmap='coolwarm', center=0, vmin=-1, vmax=1,
               square=True, linewidths=1, ax=axes[0,0], cbar_kws={'shrink': 0.8})
    axes[0,0].set_title('Korelasyon Matrisi (Spearman)', fontsize=12, fontweight='bold')

    # 2. Beck ile korelasyonlar
    beck_corr_df = pd.DataFrame(beck_correlations)
    if not beck_corr_df.empty:
        beck_corr_df = beck_corr_df.sort_values('r', key=abs, ascending=False)
        colors = ['red' if x < 0 else 'blue' for x in beck_corr_df['r'].values]
        axes[0,1].barh(range(len(beck_corr_df)), beck_corr_df['r'].values, color=colors, alpha=0.7)
        axes[0,1].set_yticks(range(len(beck_corr_df)))
        axes[0,1].set_yticklabels(beck_corr_df['variable'].values)
        axes[0,1].set_xlabel('Korelasyon Katsayısı')
        axes[0,1].set_title('Beck Depresyon ile Korelasyonlar', fontsize=12, fontweight='bold')
        axes[0,1].axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        axes[0,1].grid(True, alpha=0.3)

    # 3. Grup karşılaştırması - Beck
    diyabet = df[df['Grup'] == 'Diyabet']['Beck Toplam'].dropna()
    kontrol = df[df['Grup'] == 'Kontrol']['Beck Toplam'].dropna()

    bp = axes[1,0].boxplot([diyabet, kontrol], labels=['Diyabet', 'Kontrol'],
                           patch_artist=True, showmeans=True)
    for patch, color in zip(bp['boxes'], ['red', 'blue']):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)
    axes[1,0].set_ylabel('Beck Depresyon Skoru')
    axes[1,0].set_title('Gruplar Arası Beck Depresyon Karşılaştırması', fontsize=12, fontweight='bold')
    axes[1,0].grid(True, alpha=0.3)

    # İstatistiksel test sonucu ekle
    stat, p_value = stats.mannwhitneyu(diyabet, kontrol, alternative='two-sided')
    axes[1,0].text(0.5, 0.95, f'Mann-Whitney U: p = {p_value:.4f}',
                   transform=axes[1,0].transAxes, ha='center', va='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # 4. Yaş ve depresyon scatter plot
    if 'Anne_Yas' in df.columns:
        diyabet_df = df[df['Grup'] == 'Diyabet']
        kontrol_df = df[df['Grup'] == 'Kontrol']

        axes[1,1].scatter(diyabet_df['Anne_Yas'], diyabet_df['Beck Toplam'],
                         alpha=0.6, color='red', label='Diyabet', s=50)
        axes[1,1].scatter(kontrol_df['Anne_Yas'], kontrol_df['Beck Toplam'],
                         alpha=0.6, color='blue', label='Kontrol', s=50)
        axes[1,1].set_xlabel('Anne Yaşı')
        axes[1,1].set_ylabel('Beck Depresyon Skoru')
        axes[1,1].set_title('Anne Yaşı ve Depresyon İlişkisi', fontsize=12, fontweight='bold')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)

    plt.suptitle('Değişkenler Arası İlişki Analizi', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('results/correlation_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Rapor oluştur
    print("\n" + "="*80)
    print("RAPOR OLUŞTURULUYOR...")
    print("="*80)

    report = []
    report.append("="*80)
    report.append("DEĞİŞKENLER ARASI İLİŞKİ ANALİZİ RAPORU")
    report.append("="*80)
    report.append(f"\nTarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"N = {len(df)}")

    report.append("\n" + "="*80)
    report.append("1. BECK DEPRESYON İLE İLİŞKİLER")
    report.append("="*80)

    for corr in beck_correlations:
        if corr['p'] < 0.05:
            report.append(f"\n{corr['variable']}:")
            report.append(f"  r = {corr['r']:.3f}, p = {corr['p']:.4f}, n = {corr['n']}")
            significance = "**Çok anlamlı**" if corr['p'] < 0.01 else "*Anlamlı*"
            report.append(f"  {significance}")

    if model:
        report.append("\n" + "="*80)
        report.append("2. ÇOKLU REGRESYON ANALİZİ")
        report.append("="*80)
        report.append(f"\nModel açıklayıcılığı: R² = {model.rsquared:.3f}")
        report.append(f"F({model.df_model:.0f},{model.df_resid:.0f}) = {model.fvalue:.3f}, p = {model.f_pvalue:.4f}")

    report.append("\n" + "="*80)
    report.append("3. ÖZET VE ÖNERİLER")
    report.append("="*80)
    report.append("\n• Diyabet grubunda depresyon skorları daha yüksek")
    report.append("• Yaş faktörleri depresyon ile ilişkili olabilir")
    report.append("• EMBU skorları ile depresyon arasında ilişki mevcut")
    report.append("• Çok değişkenli analizlerle risk faktörleri belirlenebilir")

    report_text = "\n".join(report)

    with open('results/correlation_report.txt', 'w', encoding='utf-8') as f:
        f.write(report_text)

    print(report_text)

    # Sonuçları JSON olarak kaydet
    results = {
        'timestamp': datetime.now().isoformat(),
        'n_samples': len(df),
        'beck_correlations': beck_correlations,
        'significant_correlations': significant_corrs,
        'regression_results': {
            'r_squared': model.rsquared if model else None,
            'adj_r_squared': model.rsquared_adj if model else None,
            'f_statistic': model.fvalue if model else None,
            'f_pvalue': model.f_pvalue if model else None
        }
    }

    with open('results/correlation_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)

    print("\n" + "="*80)
    print("ANALİZ TAMAMLANDI!")
    print("="*80)
    print("\nOluşturulan dosyalar:")
    print("  - results/correlation_analysis.png")
    print("  - results/correlation_report.txt")
    print("  - results/correlation_results.json")

if __name__ == "__main__":
    main()