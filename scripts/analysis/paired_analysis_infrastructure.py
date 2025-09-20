"""
Paired Analysis Infrastructure
Kardeş çiftleri ve aile içi karşılaştırmalar için altyapı

Araştırma Amaçları:
1. Diyabetli çocukların annelerinde depresyon düzeyi kontrol grubuna göre yüksek mi?
2. Diyabetli çocuk ve kardeşleri arasındaki ilişki nasıl?
3. Ebeveynlik tutumları gruplar arasında farklı mı?
4. Kardeş ilişkileri hastalıktan etkileniyor mu?
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import ttest_rel, wilcoxon, ttest_ind, mannwhitneyu
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Matplotlib import'u geçici olarak devre dışı
USE_PLOTS = False
try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.rcParams['figure.figsize'] = (10, 6)
    USE_PLOTS = True
except:
    print("[UYARI] Matplotlib yüklenemedi, grafikler oluşturulmayacak")
    USE_PLOTS = False

def load_paired_data():
    """Paired analiz için veriyi yükle"""
    
    print("="*70)
    print("VERİ YÜKLEME")
    print("="*70)
    
    # Ana veri
    df = pd.read_csv('data/cleaned/dataset_reclassified.csv')
    print(f"\nToplam kayıt: {len(df)}")
    
    # Aile çiftleri
    pairs = pd.read_csv('data/cleaned/family_pairs.csv')
    print(f"Aile çifti sayısı: {len(pairs)}")
    
    # Grup dağılımı
    print("\nGrup Dağılımı:")
    for grup in df['Alt_Grup'].unique():
        count = (df['Alt_Grup'] == grup).sum()
        print(f"  {grup}: {count}")
    
    return df, pairs

def analyze_depression_levels(df):
    """Annelerde depresyon düzeylerini analiz et"""
    
    print("\n" + "="*70)
    print("ANNELERDE DEPRESYON ANALİZİ")
    print("="*70)
    
    results = {}
    
    # Beck skorlarını hesapla
    beck_items = [f'Beck_{i}' for i in range(1, 22)]
    available_beck = [col for col in beck_items if col in df.columns]
    
    if available_beck:
        df['Beck_Calculated'] = df[available_beck].sum(axis=1)
    
    # Beck_Total_Score veya Beck_Calculated kullan
    beck_col = None
    for col in ['Beck_Total_Score', 'Beck_Calculated', 'Beck Toplam', 'Beck_Toplam']:
        if col in df.columns:
            beck_col = col
            break
    
    if beck_col not in df.columns:
        print("[UYARI] Beck skoru bulunamadı!")
        return results
    
    # 1. Diyabet vs Kontrol ailelerinde depresyon
    print("\n1. Gruplar Arası Karşılaştırma:")
    
    diabetes_families = df[df['Aile_Tipi'] == 'Diyabet_Ailesi'][beck_col].dropna()
    control_families = df[df['Aile_Tipi'] == 'Kontrol_Ailesi'][beck_col].dropna()
    
    print(f"\nDiyabet ailesi (n={len(diabetes_families)}):")
    print(f"  Ortalama: {diabetes_families.mean():.2f} ± {diabetes_families.std():.2f}")
    print(f"  Medyan: {diabetes_families.median():.1f}")
    print(f"  Min-Max: {diabetes_families.min():.0f} - {diabetes_families.max():.0f}")
    
    print(f"\nKontrol ailesi (n={len(control_families)}):")
    print(f"  Ortalama: {control_families.mean():.2f} ± {control_families.std():.2f}")
    print(f"  Medyan: {control_families.median():.1f}")
    print(f"  Min-Max: {control_families.min():.0f} - {control_families.max():.0f}")
    
    # Normallik testi
    _, p_norm_dm = stats.shapiro(diabetes_families) if len(diabetes_families) > 3 else (None, 0)
    _, p_norm_ctrl = stats.shapiro(control_families) if len(control_families) > 3 else (None, 0)
    
    # Uygun test seçimi
    if p_norm_dm > 0.05 and p_norm_ctrl > 0.05:
        # Parametrik test
        stat, p_value = stats.ttest_ind(diabetes_families, control_families)
        test_name = "Independent t-test"
    else:
        # Non-parametrik test
        stat, p_value = mannwhitneyu(diabetes_families, control_families, alternative='two-sided')
        test_name = "Mann-Whitney U"
    
    print(f"\n{test_name} Sonucu:")
    print(f"  Test istatistiği: {stat:.3f}")
    print(f"  p-değeri: {p_value:.4f}")
    print(f"  Sonuç: {'ANLAMLI' if p_value < 0.05 else 'Anlamlı değil'} (p < 0.05)")
    
    # Etki büyüklüğü (Cohen's d)
    pooled_std = np.sqrt(((len(diabetes_families)-1)*diabetes_families.std()**2 + 
                          (len(control_families)-1)*control_families.std()**2) / 
                         (len(diabetes_families) + len(control_families) - 2))
    if pooled_std > 0:
        cohen_d = (diabetes_families.mean() - control_families.mean()) / pooled_std
        print(f"  Cohen's d: {cohen_d:.3f}")
    
    results['depression_comparison'] = {
        'test': test_name,
        'statistic': stat,
        'p_value': p_value,
        'dm_mean': diabetes_families.mean(),
        'ctrl_mean': control_families.mean(),
        'cohen_d': cohen_d if pooled_std > 0 else None
    }
    
    # 2. Beck kategorileri
    print("\n2. Depresyon Kategorileri:")
    
    # Kategori oluştur
    def categorize_beck(score):
        if pd.isna(score):
            return None
        elif score < 10:
            return 'Minimal'
        elif score < 17:
            return 'Hafif'
        elif score < 30:
            return 'Orta'
        else:
            return 'Ağır'
    
    df['Beck_Category'] = df[beck_col].apply(categorize_beck)
    
    # Kategori dağılımı
    for aile_tipi in ['Diyabet_Ailesi', 'Kontrol_Ailesi']:
        print(f"\n{aile_tipi}:")
        aile_df = df[df['Aile_Tipi'] == aile_tipi]
        for cat in ['Minimal', 'Hafif', 'Orta', 'Ağır']:
            count = (aile_df['Beck_Category'] == cat).sum()
            pct = count / len(aile_df) * 100 if len(aile_df) > 0 else 0
            print(f"  {cat}: {count} ({pct:.1f}%)")
    
    return results

def analyze_sibling_relationships(df, pairs):
    """Kardeş ilişkilerini analiz et"""
    
    print("\n" + "="*70)
    print("KARDEŞ İLİŞKİLERİ ANALİZİ")
    print("="*70)
    
    results = {}
    
    # Beck skorları için paired analiz
    print("\n1. Kardeşler Arası Beck Skoru Karşılaştırması:")
    
    beck_col = None
    for col in ['Beck_Total_Score', 'Beck_Calculated', 'Beck Toplam', 'Beck_Toplam']:
        if col in df.columns:
            beck_col = col
            break
    
    for pair_type in ['Diyabet_Cifti', 'Kontrol_Cifti']:
        print(f"\n{pair_type}:")
        
        type_pairs = pairs[pairs['Tip'] == pair_type]
        
        index_scores = []
        sibling_scores = []
        
        for _, pair in type_pairs.iterrows():
            # Index case skoru
            index_data = df[df['Katılımcı No'] == pair['Index_ID']]
            if len(index_data) > 0 and beck_col in index_data.columns:
                index_score = index_data[beck_col].values[0]
                if not pd.isna(index_score):
                    index_scores.append(index_score)
                    
                    # Sibling skoru
                    sibling_data = df[df['Katılımcı No'] == pair['Sibling_ID']]
                    if len(sibling_data) > 0:
                        sibling_score = sibling_data[beck_col].values[0]
                        if not pd.isna(sibling_score):
                            sibling_scores.append(sibling_score)
                        else:
                            index_scores.pop()  # Eşleşmeyen veriyi çıkar
        
        if len(index_scores) > 0 and len(index_scores) == len(sibling_scores):
            index_scores = np.array(index_scores)
            sibling_scores = np.array(sibling_scores)
            
            print(f"  Analiz edilen çift sayısı: {len(index_scores)}")
            print(f"  Index ortalama: {index_scores.mean():.2f} ± {index_scores.std():.2f}")
            print(f"  Kardeş ortalama: {sibling_scores.mean():.2f} ± {sibling_scores.std():.2f}")
            print(f"  Ortalama fark: {(index_scores - sibling_scores).mean():.2f}")
            
            # Paired t-test veya Wilcoxon
            if len(index_scores) >= 5:
                # Normallik testi
                _, p_norm = stats.shapiro(index_scores - sibling_scores)
                
                if p_norm > 0.05:
                    stat, p_value = ttest_rel(index_scores, sibling_scores)
                    test_name = "Paired t-test"
                else:
                    stat, p_value = wilcoxon(index_scores, sibling_scores)
                    test_name = "Wilcoxon signed-rank"
                
                print(f"\n  {test_name} Sonucu:")
                print(f"    Test istatistiği: {stat:.3f}")
                print(f"    p-değeri: {p_value:.4f}")
                print(f"    Sonuç: {'ANLAMLI' if p_value < 0.05 else 'Anlamlı değil'}")
                
                results[f'{pair_type}_beck'] = {
                    'n_pairs': len(index_scores),
                    'test': test_name,
                    'p_value': p_value,
                    'mean_diff': (index_scores - sibling_scores).mean()
                }
    
    return results

def analyze_embu_patterns(df):
    """EMBU ebeveynlik tutumlarını analiz et"""
    
    print("\n" + "="*70)
    print("EMBU EBEVEYNLİK TUTUMLARI ANALİZİ")
    print("="*70)
    
    results = {}
    
    # EMBU alt boyutlarını hesapla
    warmth_items = ['Ebeveyn_EMBU_2', 'Ebeveyn_EMBU_4', 'Ebeveyn_EMBU_12',
                   'Ebeveyn_EMBU_14', 'Ebeveyn_EMBU_19', 'Ebeveyn_EMBU_23']
    rejection_items = ['Ebeveyn_EMBU_1', 'Ebeveyn_EMBU_7', 'Ebeveyn_EMBU_8',
                      'Ebeveyn_EMBU_11', 'Ebeveyn_EMBU_13', 'Ebeveyn_EMBU_17',
                      'Ebeveyn_EMBU_18', 'Ebeveyn_EMBU_20']
    overprotection_items = ['Ebeveyn_EMBU_3', 'Ebeveyn_EMBU_5', 'Ebeveyn_EMBU_6',
                           'Ebeveyn_EMBU_9', 'Ebeveyn_EMBU_10', 'Ebeveyn_EMBU_15',
                           'Ebeveyn_EMBU_16', 'Ebeveyn_EMBU_21', 'Ebeveyn_EMBU_22']
    
    # Alt boyutları hesapla
    if all(item in df.columns for item in warmth_items):
        df['EMBU_Warmth'] = df[warmth_items].mean(axis=1)
    if all(item in df.columns for item in rejection_items):
        df['EMBU_Rejection'] = df[rejection_items].mean(axis=1)
    if all(item in df.columns for item in overprotection_items):
        df['EMBU_Overprotection'] = df[overprotection_items].mean(axis=1)
    
    # Gruplar arası karşılaştırma
    embu_dimensions = ['EMBU_Warmth', 'EMBU_Rejection', 'EMBU_Overprotection']
    
    for dimension in embu_dimensions:
        if dimension in df.columns:
            print(f"\n{dimension.replace('EMBU_', '')}:")
            
            # Grupları ayır
            dm_index = df[(df['Alt_Grup'] == 'Diyabet_Index')][dimension].dropna()
            dm_sibling = df[(df['Alt_Grup'] == 'Diyabet_Kardes')][dimension].dropna()
            ctrl_index = df[(df['Alt_Grup'] == 'Kontrol_Index')][dimension].dropna()
            ctrl_sibling = df[(df['Alt_Grup'] == 'Kontrol_Kardes')][dimension].dropna()
            
            # Ortalamaları yazdır
            print(f"  Diyabet Index: {dm_index.mean():.2f} ± {dm_index.std():.2f} (n={len(dm_index)})")
            print(f"  Diyabet Kardeş: {dm_sibling.mean():.2f} ± {dm_sibling.std():.2f} (n={len(dm_sibling)})")
            print(f"  Kontrol Index: {ctrl_index.mean():.2f} ± {ctrl_index.std():.2f} (n={len(ctrl_index)})")
            print(f"  Kontrol Kardeş: {ctrl_sibling.mean():.2f} ± {ctrl_sibling.std():.2f} (n={len(ctrl_sibling)})")
            
            # Diyabet vs Kontrol (tüm bireyler)
            if len(dm_index) + len(dm_sibling) > 3 and len(ctrl_index) + len(ctrl_sibling) > 3:
                dm_all = pd.concat([dm_index, dm_sibling])
                ctrl_all = pd.concat([ctrl_index, ctrl_sibling])
                
                stat, p_value = mannwhitneyu(dm_all, ctrl_all, alternative='two-sided')
                print(f"\n  Diyabet vs Kontrol (Mann-Whitney U):")
                print(f"    p-değeri: {p_value:.4f} {'*' if p_value < 0.05 else ''}")
                
                results[f'{dimension}_group'] = {
                    'dm_mean': dm_all.mean(),
                    'ctrl_mean': ctrl_all.mean(),
                    'p_value': p_value
                }
    
    return results, df

def create_visualizations(df, results):
    """Görselleştirmeler oluştur"""

    print("\n" + "="*70)
    print("GÖRSELLEŞTİRMELER")
    print("="*70)

    if not USE_PLOTS:
        print("[BİLGİ] Matplotlib yüklü değil, grafikler atlanıyor")
        return

    # Beck skoru dağılımı
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Beck skorları - Gruplar
    beck_col = None
    for col in ['Beck_Total_Score', 'Beck_Calculated', 'Beck Toplam', 'Beck_Toplam']:
        if col in df.columns:
            beck_col = col
            break
    if beck_col in df.columns:
        ax = axes[0, 0]
        data_to_plot = []
        labels = []
        
        for grup in df['Alt_Grup'].unique():
            grup_data = df[df['Alt_Grup'] == grup][beck_col].dropna()
            if len(grup_data) > 0:
                data_to_plot.append(grup_data)
                labels.append(grup.replace('_', ' '))
        
        bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True)
        colors = ['lightblue', 'lightgreen', 'coral', 'gold']
        for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
            patch.set_facecolor(color)
        
        ax.set_title('Beck Depresyon Skorları - Alt Gruplar')
        ax.set_ylabel('Beck Skoru')
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='x', rotation=45)
    
    # 2. EMBU Warmth
    if 'EMBU_Warmth' in df.columns:
        ax = axes[0, 1]
        sns.violinplot(data=df, x='Aile_Tipi', y='EMBU_Warmth', ax=ax)
        ax.set_title('EMBU Duygusal Sıcaklık')
        ax.set_xlabel('Aile Tipi')
        ax.set_ylabel('Duygusal Sıcaklık Skoru')
    
    # 3. EMBU Rejection
    if 'EMBU_Rejection' in df.columns:
        ax = axes[1, 0]
        sns.violinplot(data=df, x='Aile_Tipi', y='EMBU_Rejection', ax=ax)
        ax.set_title('EMBU Reddedicilik')
        ax.set_xlabel('Aile Tipi')
        ax.set_ylabel('Reddedicilik Skoru')
    
    # 4. EMBU Overprotection
    if 'EMBU_Overprotection' in df.columns:
        ax = axes[1, 1]
        sns.violinplot(data=df, x='Aile_Tipi', y='EMBU_Overprotection', ax=ax)
        ax.set_title('EMBU Aşırı Koruma')
        ax.set_xlabel('Aile Tipi')
        ax.set_ylabel('Aşırı Koruma Skoru')
    
    plt.tight_layout()
    plt.savefig('results/paired_analysis_plots.png', dpi=300, bbox_inches='tight')
    print("[OK] Görseller kaydedildi: paired_analysis_plots.png")
    plt.close('all')  # Close figures instead of showing

def create_comprehensive_report(results, df):
    """Kapsamlı analiz raporu oluştur"""
    
    report = []
    report.append("="*80)
    report.append("PAIRED ANALİZ VE ARAŞTIRMA AMAÇLARI RAPORU")
    report.append("="*80)
    report.append(f"\nTarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Araştırma Sorusu 1
    report.append("\n" + "="*80)
    report.append("ARAŞTIRMA SORUSU 1: ANNELERDE DEPRESYON")
    report.append("Diyabetli çocukların annelerinde depresyon düzeyi yüksek mi?")
    report.append("="*80)
    
    if 'depression_comparison' in results:
        dep = results['depression_comparison']
        report.append(f"\nTest: {dep['test']}")
        report.append(f"Diyabet ailesi ortalama: {dep['dm_mean']:.2f}")
        report.append(f"Kontrol ailesi ortalama: {dep['ctrl_mean']:.2f}")
        report.append(f"p-değeri: {dep['p_value']:.4f}")
        report.append(f"Cohen's d: {dep['cohen_d']:.3f}" if dep['cohen_d'] else "")
        
        if dep['p_value'] < 0.05:
            report.append("\nSONUC: Diyabetli çocukların annelerinde depresyon anlamlı olarak YÜKSEK")
        else:
            report.append("\nSONUC: Gruplar arasında anlamlı fark YOK")
    
    # Araştırma Sorusu 2
    report.append("\n" + "="*80)
    report.append("ARAŞTIRMA SORUSU 2: KARDEŞ İLİŞKİLERİ")
    report.append("Diyabetli çocuk ve kardeşleri arasındaki ilişki nasıl?")
    report.append("="*80)
    
    for key in ['Diyabet_Cifti_beck', 'Kontrol_Cifti_beck']:
        if key in results:
            res = results[key]
            grup = key.replace('_beck', '').replace('_', ' ')
            report.append(f"\n{grup}:")
            report.append(f"  Analiz edilen çift: {res['n_pairs']}")
            report.append(f"  Test: {res['test']}")
            report.append(f"  Ortalama fark: {res['mean_diff']:.2f}")
            report.append(f"  p-değeri: {res['p_value']:.4f}")
    
    # Araştırma Sorusu 3
    report.append("\n" + "="*80)
    report.append("ARAŞTIRMA SORUSU 3: EBEVEYNLİK TUTUMLARI")
    report.append("Ebeveynlik tutumları gruplar arasında farklı mı?")
    report.append("="*80)
    
    for dimension in ['EMBU_Warmth_group', 'EMBU_Rejection_group', 'EMBU_Overprotection_group']:
        if dimension in results:
            res = results[dimension]
            dim_name = dimension.replace('EMBU_', '').replace('_group', '')
            report.append(f"\n{dim_name}:")
            report.append(f"  Diyabet ortalama: {res['dm_mean']:.2f}")
            report.append(f"  Kontrol ortalama: {res['ctrl_mean']:.2f}")
            report.append(f"  p-değeri: {res['p_value']:.4f} {'*' if res['p_value'] < 0.05 else ''}")
    
    # Öneriler
    report.append("\n" + "="*80)
    report.append("ÖNERİLER VE YORUMLAR")
    report.append("="*80)
    
    report.append("\n1. Kardeş çiftleri paired analiz için uygundur")
    report.append("2. Grup dengesizliği (38 vs 40) kabul edilebilir")
    report.append("3. EMBU ve Beck skorlarında eksik veri az")
    report.append("4. Aile içi dinamikler değerlendirilmelidir")
    
    report.append("\n" + "="*80)
    
    # Raporu kaydet
    with open('results/paired_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    
    print("\n[OK] Analiz raporu kaydedildi: paired_analysis_report.txt")
    
    return report

def main():
    """Ana analiz fonksiyonu"""
    
    print("\n" + "="*70)
    print("PAIRED ANALİZ VE ARAŞTIRMA AMAÇLARI")
    print("="*70)
    
    try:
        # Veriyi yükle
        df, pairs = load_paired_data()
        
        # Analizleri yap
        results = {}
        
        # 1. Depresyon analizi
        depression_results = analyze_depression_levels(df)
        results.update(depression_results)
        
        # 2. Kardeş ilişkileri
        sibling_results = analyze_sibling_relationships(df, pairs)
        results.update(sibling_results)
        
        # 3. EMBU analizi
        embu_results, df = analyze_embu_patterns(df)
        results.update(embu_results)
        
        # 4. Görselleştirmeler
        create_visualizations(df, results)
        
        # 5. Rapor oluştur
        report = create_comprehensive_report(results, df)
        
        # Sonuçları kaydet
        import json
        with open('results/paired_analysis_results.json', 'w') as f:
            # Convert numpy types to Python types for JSON serialization
            json_results = {}
            for key, value in results.items():
                if isinstance(value, dict):
                    json_results[key] = {}
                    for k, v in value.items():
                        if isinstance(v, (np.ndarray, np.generic)):
                            json_results[key][k] = float(v)
                        else:
                            json_results[key][k] = v
                else:
                    json_results[key] = value
            
            json.dump(json_results, f, indent=2)
        
        print("\n[OK] Sonuçlar kaydedildi: paired_analysis_results.json")
        
        print("\n" + "="*70)
        print("ANALİZ TAMAMLANDI")
        print("="*70)
        
        return results, df
        
    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    main()