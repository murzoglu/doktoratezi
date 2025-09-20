"""
Hipotez Testleri - Klinik Protokol Uyarınca
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import mannwhitneyu, chi2_contingency, pearsonr, spearmanr
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Türkçe karakter ayarları
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

def load_data():
    """Temizlenmiş veriyi yükle"""
    print("Veri yukleniyor...")
    df = pd.read_csv('data/cleaned/cleaned_dataset.csv')
    print(f"Toplam {len(df)} katilimci yuklendi")
    print(f"Grup dagilimi: {df['Grup'].value_counts().to_dict()}")
    return df

def test_normality(data, variable_name):
    """Normallik testi (Shapiro-Wilk)"""
    stat, p_value = stats.shapiro(data.dropna())
    is_normal = p_value > 0.05
    return is_normal, p_value

def compare_groups(df, variable, group_col='Grup'):
    """İki grup karşılaştırması (t-test veya Mann-Whitney U)"""
    
    # Grupları ayır
    control = df[df[group_col] == 'Kontrol'][variable].dropna()
    diabetes = df[df[group_col] == 'Diyabet'][variable].dropna()
    
    if len(control) < 3 or len(diabetes) < 3:
        return None
    
    # Normallik testi
    control_normal, _ = test_normality(control, f"{variable}_Kontrol")
    diabetes_normal, _ = test_normality(diabetes, f"{variable}_Diyabet")
    
    # Test seçimi
    if control_normal and diabetes_normal:
        # Parametrik test (t-test)
        stat, p_value = stats.ttest_ind(control, diabetes)
        test_type = 't-test'
    else:
        # Non-parametrik test (Mann-Whitney U)
        stat, p_value = mannwhitneyu(control, diabetes, alternative='two-sided')
        test_type = 'Mann-Whitney U'
    
    # Etki büyüklüğü (Cohen's d veya r)
    if test_type == 't-test':
        pooled_std = np.sqrt(((len(control)-1)*control.std()**2 + (len(diabetes)-1)*diabetes.std()**2) / (len(control) + len(diabetes) - 2))
        effect_size = (control.mean() - diabetes.mean()) / pooled_std if pooled_std > 0 else 0
        effect_type = "Cohen's d"
    else:
        # r = Z / sqrt(N) for Mann-Whitney
        z_score = stat / np.sqrt(len(control) + len(diabetes))
        effect_size = z_score
        effect_type = 'r'
    
    return {
        'variable': variable,
        'test': test_type,
        'statistic': stat,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'control_mean': control.mean(),
        'control_std': control.std(),
        'control_n': len(control),
        'diabetes_mean': diabetes.mean(),
        'diabetes_std': diabetes.std(),
        'diabetes_n': len(diabetes),
        'effect_size': effect_size,
        'effect_type': effect_type
    }

def test_primary_hypotheses(df):
    """Birincil hipotezleri test et"""
    
    print("\n" + "="*60)
    print("BİRİNCİL HİPOTEZ TESTLERİ")
    print("="*60)
    
    results = []
    
    # H1: Diyabetli çocukların annelerinde depresyon düzeyi daha yüksek
    print("\nH1: Anne depresyon düzeyleri karşılaştırması")

    # Beck toplam skor
    beck_vars = ['Beck_Toplam', 'Beck_Total_Score']

    for var in beck_vars:
        if var in df.columns:
            result = compare_groups(df, var)
            if result:
                results.append(result)
                print(f"\n{var}:")
                print(f"  Kontrol: {result['control_mean']:.2f} ± {result['control_std']:.2f} (n={result['control_n']})")
                print(f"  Diyabet: {result['diabetes_mean']:.2f} ± {result['diabetes_std']:.2f} (n={result['diabetes_n']})")
                print(f"  Test: {result['test']}")
                print(f"  p-değeri: {result['p_value']:.4f} {'*' if result['significant'] else ''}")
                print(f"  Etki büyüklüğü ({result['effect_type']}): {result['effect_size']:.3f}")

    # Beck alt boyutları - madde bazında analiz
    # Cognitive-Affective (1-13) ve Somatic-Performance (14-21) olarak gruplandırma
    cognitive_items = [f'Beck_{i}' for i in range(1, 14)]
    somatic_items = [f'Beck_{i}' for i in range(14, 22)]

    # Cognitive-Affective alt boyut
    df['Beck_Cognitive_Affective'] = df[cognitive_items].sum(axis=1)
    result = compare_groups(df, 'Beck_Cognitive_Affective')
    if result:
        results.append(result)
        print(f"\nBeck_Cognitive_Affective:")
        print(f"  Kontrol: {result['control_mean']:.2f} ± {result['control_std']:.2f} (n={result['control_n']})")
        print(f"  Diyabet: {result['diabetes_mean']:.2f} ± {result['diabetes_std']:.2f} (n={result['diabetes_n']})")
        print(f"  Test: {result['test']}")
        print(f"  p-değeri: {result['p_value']:.4f} {'*' if result['significant'] else ''}")
        print(f"  Etki büyüklüğü ({result['effect_type']}): {result['effect_size']:.3f}")

    # Somatic-Performance alt boyut
    df['Beck_Somatic_Performance'] = df[somatic_items].sum(axis=1)
    result = compare_groups(df, 'Beck_Somatic_Performance')
    if result:
        results.append(result)
        print(f"\nBeck_Somatic_Performance:")
        print(f"  Kontrol: {result['control_mean']:.2f} ± {result['control_std']:.2f} (n={result['control_n']})")
        print(f"  Diyabet: {result['diabetes_mean']:.2f} ± {result['diabetes_std']:.2f} (n={result['diabetes_n']})")
        print(f"  Test: {result['test']}")
        print(f"  p-değeri: {result['p_value']:.4f} {'*' if result['significant'] else ''}")
        print(f"  Etki büyüklüğü ({result['effect_type']}): {result['effect_size']:.3f}")

    # H2: Ebeveynlik tutumları farklılığı (EMBU) - madde bazında analiz gerekiyor
    print("\n\nH2: Ebeveynlik tutumları (EMBU) karşılaştırması")
    print("Not: EMBU alt boyutları hesaplanıyor...")

    # EMBU maddeleri - Duygusal Sıcaklık, Reddedicilik, Aşırı Koruma boyutlarına ayrılmalı
    # Literatüre göre EMBU-C kısa form madde dağılımı:
    # Duygusal Sıcaklık: 2, 4, 12, 14, 19, 23
    # Reddedicilik: 1, 7, 8, 11, 13, 17, 18, 20
    # Aşırı Koruma: 3, 5, 6, 9, 10, 15, 16, 21, 22

    warmth_items = ['Ebeveyn_EMBU_2', 'Ebeveyn_EMBU_4', 'Ebeveyn_EMBU_12',
                   'Ebeveyn_EMBU_14', 'Ebeveyn_EMBU_19', 'Ebeveyn_EMBU_23']
    rejection_items = ['Ebeveyn_EMBU_1', 'Ebeveyn_EMBU_7', 'Ebeveyn_EMBU_8',
                      'Ebeveyn_EMBU_11', 'Ebeveyn_EMBU_13', 'Ebeveyn_EMBU_17',
                      'Ebeveyn_EMBU_18', 'Ebeveyn_EMBU_20']
    overprotection_items = ['Ebeveyn_EMBU_3', 'Ebeveyn_EMBU_5', 'Ebeveyn_EMBU_6',
                           'Ebeveyn_EMBU_9', 'Ebeveyn_EMBU_10', 'Ebeveyn_EMBU_15',
                           'Ebeveyn_EMBU_16', 'Ebeveyn_EMBU_21', 'Ebeveyn_EMBU_22']

    # Duygusal Sıcaklık
    if all(item in df.columns for item in warmth_items):
        df['EMBU_Duygusal_Sicaklik'] = df[warmth_items].mean(axis=1)
        result = compare_groups(df, 'EMBU_Duygusal_Sicaklik')
        if result:
            results.append(result)
            print(f"\nEMBU_Duygusal_Sicaklik:")
            print(f"  Kontrol: {result['control_mean']:.2f} ± {result['control_std']:.2f} (n={result['control_n']})")
            print(f"  Diyabet: {result['diabetes_mean']:.2f} ± {result['diabetes_std']:.2f} (n={result['diabetes_n']})")
            print(f"  Test: {result['test']}")
            print(f"  p-değeri: {result['p_value']:.4f} {'*' if result['significant'] else ''}")
            print(f"  Etki büyüklüğü ({result['effect_type']}): {result['effect_size']:.3f}")

    # Reddedicilik
    if all(item in df.columns for item in rejection_items):
        df['EMBU_Reddedicilik'] = df[rejection_items].mean(axis=1)
        result = compare_groups(df, 'EMBU_Reddedicilik')
        if result:
            results.append(result)
            print(f"\nEMBU_Reddedicilik:")
            print(f"  Kontrol: {result['control_mean']:.2f} ± {result['control_std']:.2f} (n={result['control_n']})")
            print(f"  Diyabet: {result['diabetes_mean']:.2f} ± {result['diabetes_std']:.2f} (n={result['diabetes_n']})")
            print(f"  Test: {result['test']}")
            print(f"  p-değeri: {result['p_value']:.4f} {'*' if result['significant'] else ''}")
            print(f"  Etki büyüklüğü ({result['effect_type']}): {result['effect_size']:.3f}")

    # Aşırı Koruma
    if all(item in df.columns for item in overprotection_items):
        df['EMBU_Asiri_Koruma'] = df[overprotection_items].mean(axis=1)
        result = compare_groups(df, 'EMBU_Asiri_Koruma')
        if result:
            results.append(result)
            print(f"\nEMBU_Asiri_Koruma:")
            print(f"  Kontrol: {result['control_mean']:.2f} ± {result['control_std']:.2f} (n={result['control_n']})")
            print(f"  Diyabet: {result['diabetes_mean']:.2f} ± {result['diabetes_std']:.2f} (n={result['diabetes_n']})")
            print(f"  Test: {result['test']}")
            print(f"  p-değeri: {result['p_value']:.4f} {'*' if result['significant'] else ''}")
            print(f"  Etki büyüklüğü ({result['effect_type']}): {result['effect_size']:.3f}")
    
    return pd.DataFrame(results)

def test_correlations(df):
    """Korelasyon analizleri"""
    
    print("\n" + "="*60)
    print("KORELASYON ANALİZLERİ")
    print("="*60)
    
    correlations = []
    
    # Anne depresyon skoru ile ebeveynlik tutumları
    print("\nAnne Depresyon - Ebeveynlik Tutumları Korelasyonları:")

    beck_col = 'Beck_Total_Score' if 'Beck_Total_Score' in df.columns else 'Beck_Toplam'

    if beck_col in df.columns:
        beck_score = df[beck_col].dropna()

        # EMBU alt boyutları hesaplanmışsa kullan
        embu_vars = []
        if 'EMBU_Duygusal_Sicaklik' in df.columns:
            embu_vars.extend(['EMBU_Duygusal_Sicaklik', 'EMBU_Reddedicilik', 'EMBU_Asiri_Koruma'])

        for var in embu_vars:
            if var in df.columns:
                embu_score = df[var].dropna()

                # Ortak indeksleri bul
                common_idx = beck_score.index.intersection(embu_score.index)

                if len(common_idx) > 30:
                    r, p = pearsonr(beck_score[common_idx], embu_score[common_idx])

                    correlations.append({
                        'variable_1': beck_col,
                        'variable_2': var,
                        'r': r,
                        'p_value': p,
                        'n': len(common_idx),
                        'significant': p < 0.05
                    })

                    print(f"\n{beck_col} vs {var}:")
                    print(f"  r = {r:.3f}, p = {p:.4f} {'*' if p < 0.05 else ''}")
                    print(f"  n = {len(common_idx)}")

    # Grup içi korelasyonlar
    for group in ['Kontrol', 'Diyabet']:
        print(f"\n\n{group} Grubu İçi Korelasyonlar:")

        group_df = df[df['Grup'] == group]

        if beck_col in group_df.columns:
            beck_score = group_df[beck_col].dropna()

            for var in ['EMBU_Duygusal_Sicaklik', 'EMBU_Reddedicilik', 'EMBU_Asiri_Koruma']:
                if var in group_df.columns:
                    embu_score = group_df[var].dropna()

                    common_idx = beck_score.index.intersection(embu_score.index)

                    if len(common_idx) > 10:
                        r, p = pearsonr(beck_score[common_idx], embu_score[common_idx])

                        correlations.append({
                            'group': group,
                            'variable_1': beck_col,
                            'variable_2': var,
                            'r': r,
                            'p_value': p,
                            'n': len(common_idx),
                            'significant': p < 0.05
                        })

                        print(f"\n{beck_col} vs {var}:")
                        print(f"  r = {r:.3f}, p = {p:.4f} {'*' if p < 0.05 else ''}")
                        print(f"  n = {len(common_idx)}")
    
    return pd.DataFrame(correlations)

def create_hypothesis_report(comparison_results, correlation_results):
    """Hipotez test raporu oluştur"""
    
    report = []
    report.append("="*70)
    report.append("HİPOTEZ TEST RAPORU")
    report.append("="*70)
    report.append(f"\nTarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("\n" + "="*70)
    report.append("1. GRUP KARŞILAŞTIRMALARI")
    report.append("="*70)
    
    # Beck skorları
    report.append("\nA. BECK DEPRESYON ÖLÇEĞİ:")
    if len(comparison_results) > 0 and 'variable' in comparison_results.columns:
        beck_results = comparison_results[comparison_results['variable'].str.contains('Beck')]

        if len(beck_results) > 0:
            for _, row in beck_results.iterrows():
                report.append(f"\n{row['variable']}:")
                report.append(f"  Kontrol: {row['control_mean']:.2f} ± {row['control_std']:.2f} (n={row['control_n']})")
                report.append(f"  Diyabet: {row['diabetes_mean']:.2f} ± {row['diabetes_std']:.2f} (n={row['diabetes_n']})")
                report.append(f"  Test: {row['test']}")
                report.append(f"  p-değeri: {row['p_value']:.4f} {'***' if row['p_value'] < 0.001 else '**' if row['p_value'] < 0.01 else '*' if row['p_value'] < 0.05 else ''}")
                report.append(f"  Etki büyüklüğü ({row['effect_type']}): {row['effect_size']:.3f}")
        else:
            report.append("\nBeck verileri bulunamadı veya hesaplanamadı.")
    else:
        report.append("\nKarşılaştırma sonuçları elde edilemedi.")

    # EMBU skorları
    report.append("\n\nB. EMBU EBEVEYNLİK TUTUMLARI:")
    if len(comparison_results) > 0 and 'variable' in comparison_results.columns:
        embu_results = comparison_results[comparison_results['variable'].str.contains('EMBU')]

        if len(embu_results) > 0:
            for _, row in embu_results.iterrows():
                report.append(f"\n{row['variable']}:")
                report.append(f"  Kontrol: {row['control_mean']:.2f} ± {row['control_std']:.2f} (n={row['control_n']})")
                report.append(f"  Diyabet: {row['diabetes_mean']:.2f} ± {row['diabetes_std']:.2f} (n={row['diabetes_n']})")
                report.append(f"  Test: {row['test']}")
                report.append(f"  p-değeri: {row['p_value']:.4f} {'***' if row['p_value'] < 0.001 else '**' if row['p_value'] < 0.01 else '*' if row['p_value'] < 0.05 else ''}")
                report.append(f"  Etki büyüklüğü ({row['effect_type']}): {row['effect_size']:.3f}")
        else:
            report.append("\nEMBU verileri bulunamadı veya hesaplanamadı.")
    else:
        report.append("\nKarşılaştırma sonuçları elde edilemedi.")
    
    report.append("\n" + "="*70)
    report.append("2. KORELASYON ANALİZLERİ")
    report.append("="*70)
    
    # Genel korelasyonlar
    general_corr = correlation_results[~correlation_results.get('group', pd.Series()).notna()]
    if len(general_corr) > 0:
        report.append("\nA. TÜM ÖRNEKLEM:")
        for _, row in general_corr.iterrows():
            report.append(f"\n{row['variable_1']} - {row['variable_2']}:")
            report.append(f"  r = {row['r']:.3f}, p = {row['p_value']:.4f} {'*' if row['significant'] else ''}")
            report.append(f"  n = {row['n']}")
    
    # Grup içi korelasyonlar
    for group in ['Kontrol', 'Diyabet']:
        group_corr = correlation_results[correlation_results.get('group', '') == group]
        if len(group_corr) > 0:
            report.append(f"\n\nB. {group.upper()} GRUBU:")
            for _, row in group_corr.iterrows():
                report.append(f"\n{row['variable_1']} - {row['variable_2']}:")
                report.append(f"  r = {row['r']:.3f}, p = {row['p_value']:.4f} {'*' if row['significant'] else ''}")
                report.append(f"  n = {row['n']}")
    
    report.append("\n" + "="*70)
    report.append("3. HİPOTEZ DEĞERLENDİRMESİ")
    report.append("="*70)

    # H1 değerlendirmesi
    if len(comparison_results) > 0 and 'variable' in comparison_results.columns:
        beck_results = comparison_results[comparison_results['variable'].str.contains('Beck')]
        if len(beck_results) > 0:
            # Beck_Total_Score veya Beck_Toplam kolonunu bul
            beck_total = beck_results[
                (beck_results['variable'] == 'Beck_Total_Score') |
                (beck_results['variable'] == 'Beck_Toplam')
            ]
            if len(beck_total) > 0:
                if beck_total.iloc[0]['significant']:
                    report.append("\nH1: DESTEKLENDI")
                    report.append(f"Diyabetli çocukların annelerinde depresyon düzeyi anlamlı olarak daha yüksektir (p={beck_total.iloc[0]['p_value']:.4f}).")
                else:
                    report.append("\nH1: DESTEKLENMEDİ")
                    report.append(f"Gruplar arasında depresyon düzeyi açısından anlamlı fark bulunamamıştır (p={beck_total.iloc[0]['p_value']:.4f}).")
            else:
                report.append("\nH1: DEĞERLENDİRİLEMEDİ")
                report.append("Beck toplam skoru hesaplanamadı.")
        else:
            report.append("\nH1: DEĞERLENDİRİLEMEDİ")
            report.append("Beck verileri bulunamadı.")

        # H2 değerlendirmesi
        embu_results = comparison_results[comparison_results['variable'].str.contains('EMBU')]
        if len(embu_results) > 0:
            significant_embu = embu_results[embu_results['significant']]
            if len(significant_embu) > 0:
                report.append("\nH2: KISMEN DESTEKLENDI")
                report.append("Ebeveynlik tutumlarında şu boyutlarda anlamlı farklar bulunmuştur:")
                for _, row in significant_embu.iterrows():
                    report.append(f"  - {row['variable']}: p={row['p_value']:.4f}")
            else:
                report.append("\nH2: DESTEKLENMEDİ")
                report.append("Gruplar arasında ebeveynlik tutumları açısından anlamlı fark bulunamamıştır.")
        else:
            report.append("\nH2: DEĞERLENDİRİLEMEDİ")
            report.append("EMBU verileri bulunamadı.")
    else:
        report.append("\nHİPOTEZLER DEĞERLENDİRİLEMEDİ")
        report.append("Karşılaştırma sonuçları elde edilemedi.")
    
    report.append("\n" + "="*70)
    report.append("İSTATİSTİKSEL NOTLAR:")
    report.append("* p < 0.05, ** p < 0.01, *** p < 0.001")
    report.append("Normallik testine göre uygun test (t-test veya Mann-Whitney U) seçilmiştir.")
    report.append("="*70)
    
    return "\n".join(report)

def main():
    """Ana analiz fonksiyonu"""
    
    print("\n" + "="*60)
    print("HİPOTEZ TESTLERİ BAŞLATILIYOR")
    print("="*60)
    
    try:
        # Veriyi yükle
        df = load_data()
        
        # Birincil hipotez testleri
        comparison_results = test_primary_hypotheses(df)
        
        # Korelasyon analizleri
        correlation_results = test_correlations(df)
        
        # Sonuçları kaydet
        comparison_results.to_csv('results/hypothesis_test_comparisons.csv', index=False, encoding='utf-8-sig')
        comparison_results.to_excel('results/hypothesis_test_comparisons.xlsx', index=False)
        print("\n[OK] Karşılaştırma sonuçları kaydedildi")
        
        correlation_results.to_csv('results/hypothesis_test_correlations.csv', index=False, encoding='utf-8-sig')
        correlation_results.to_excel('results/hypothesis_test_correlations.xlsx', index=False)
        print("[OK] Korelasyon sonuçları kaydedildi")
        
        # Rapor oluştur
        report = create_hypothesis_report(comparison_results, correlation_results)
        
        # Raporu kaydet
        with open('results/hypothesis_test_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        print("[OK] Hipotez test raporu oluşturuldu")
        
        # Raporu ekrana yazdır
        print("\n" + report)
        
        print("\n" + "="*60)
        print("HİPOTEZ TESTLERİ TAMAMLANDI")
        print("="*60)
        
    except Exception as e:
        print(f"\n[HATA] Hipotez testleri sırasında hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()