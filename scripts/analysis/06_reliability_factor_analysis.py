"""
06_reliability_factor_analysis.py
Güvenilirlik ve Faktör Analizleri
"""

import pandas as pd
import numpy as np
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
from factor_analyzer.factor_analyzer import calculate_kmo
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def load_data():
    """Temizlenmiş veriyi yükler"""
    try:
        df = pd.read_csv('data/cleaned/cleaned_dataset.csv')
        print(f"[✓] Veri yüklendi: {df.shape[0]} satır")
        return df
    except:
        print("[!] Veri bulunamadı.")
        return None

def cronbach_alpha(df, items):
    """Cronbach's alpha hesaplar"""

    # Eksik verileri temizle
    df_items = df[items].dropna()

    if len(df_items) < 2:
        return None

    # Item sayısı
    n_items = len(items)

    # Item varyansları
    item_variances = df_items.var(axis=0, ddof=1)

    # Toplam skor varyansı
    total_scores = df_items.sum(axis=1)
    total_variance = total_scores.var(ddof=1)

    # Cronbach's alpha formülü
    alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)

    return alpha

def item_total_correlations(df, items):
    """Item-total korelasyonlarını hesaplar"""

    df_items = df[items].dropna()
    results = []

    for item in items:
        # Bu item hariç toplam skor
        other_items = [i for i in items if i != item]
        corrected_total = df_items[other_items].sum(axis=1)

        # Item-total korelasyon
        correlation = df_items[item].corr(corrected_total)

        # Bu item çıkarılırsa alpha
        if len(other_items) > 1:
            alpha_if_deleted = cronbach_alpha(df, other_items)
        else:
            alpha_if_deleted = None

        results.append({
            'Item': item,
            'Item_Mean': df_items[item].mean(),
            'Item_SD': df_items[item].std(),
            'Corrected_Item_Total_Corr': correlation,
            'Alpha_if_Deleted': alpha_if_deleted
        })

    return pd.DataFrame(results)

def reliability_analysis(df, scale_name, items):
    """Kapsamlı güvenilirlik analizi"""

    print("\n" + "="*60)
    print(f"GÜVENİLİRLİK ANALİZİ: {scale_name}")
    print("="*60)

    # Eksik veri kontrolü
    df_scale = df[items].dropna()
    n_complete = len(df_scale)
    n_missing = len(df) - n_complete

    print(f"\n[VERİ BİLGİSİ]")
    print(f"Madde sayısı: {len(items)}")
    print(f"Tam veri: {n_complete} ({n_complete/len(df)*100:.1f}%)")
    print(f"Eksik veri: {n_missing} ({n_missing/len(df)*100:.1f}%)")

    if n_complete < 30:
        print(f"[!] Yetersiz veri (n={n_complete}). En az 30 gözlem önerilir.")
        return None

    # Cronbach's Alpha
    alpha = cronbach_alpha(df, items)
    print(f"\n[CRONBACH'S ALPHA]")
    print(f"α = {alpha:.4f}")

    # Güvenilirlik yorumu
    if alpha >= 0.9:
        reliability = "Mükemmel"
    elif alpha >= 0.8:
        reliability = "İyi"
    elif alpha >= 0.7:
        reliability = "Kabul edilebilir"
    elif alpha >= 0.6:
        reliability = "Sınırda"
    else:
        reliability = "Düşük"

    print(f"Güvenilirlik düzeyi: {reliability}")

    # Split-half reliability
    if len(items) >= 4:
        # İlk yarı ve ikinci yarı
        half1 = items[:len(items)//2]
        half2 = items[len(items)//2:]

        score1 = df_scale[half1].sum(axis=1)
        score2 = df_scale[half2].sum(axis=1)

        r_half = score1.corr(score2)

        # Spearman-Brown düzeltmesi
        r_sb = (2 * r_half) / (1 + r_half)

        print(f"\n[SPLIT-HALF RELIABİLİTY]")
        print(f"r_half = {r_half:.4f}")
        print(f"Spearman-Brown = {r_sb:.4f}")

    # Item-total korelasyonları
    item_stats = item_total_correlations(df, items)

    print(f"\n[ITEM ANALİZİ]")
    print(item_stats.to_string())

    # Problemli itemler
    problematic_items = item_stats[item_stats['Corrected_Item_Total_Corr'] < 0.3]
    if not problematic_items.empty:
        print(f"\n[!] DÜşÜK KORELASYONLU ITEMLER (r < 0.3):")
        for _, item in problematic_items.iterrows():
            print(f"  - {item['Item']}: r = {item['Corrected_Item_Total_Corr']:.3f}")

    return {
        'scale': scale_name,
        'n_items': len(items),
        'n_complete': n_complete,
        'alpha': alpha,
        'reliability': reliability,
        'item_stats': item_stats
    }

def factor_analysis(df, items, n_factors=None):
    """Açıklayıcı faktör analizi (EFA)"""

    print("\n" + "="*60)
    print("AÇIKLAYICI FAKTÖR ANALİZİ (EFA)")
    print("="*60)

    # Veriyi hazırla
    df_items = df[items].dropna()

    if len(df_items) < 100:
        print(f"[!] Faktör analizi için yetersiz örneklem (n={len(df_items)})")
        print("    Minimum 100, ideal olarak madde sayısının 5-10 katı önerilir")
        return None

    # Kaiser-Meyer-Olkin (KMO) testi
    kmo_all, kmo_model = calculate_kmo(df_items)
    print(f"\n[KMO TESTİ]")
    print(f"KMO = {kmo_model:.4f}")

    if kmo_model >= 0.9:
        adequacy = "Mükemmel"
    elif kmo_model >= 0.8:
        adequacy = "İyi"
    elif kmo_model >= 0.7:
        adequacy = "Orta"
    elif kmo_model >= 0.6:
        adequacy = "Zayıf"
    else:
        adequacy = "Kabul edilemez"

    print(f"Örneklem yeterliliği: {adequacy}")

    # Bartlett's test of sphericity
    chi_square_value, p_value = calculate_bartlett_sphericity(df_items)
    print(f"\n[BARTLETT TESTİ]")
    print(f"χ² = {chi_square_value:.2f}, p = {p_value:.4e}")

    if p_value < 0.05:
        print("Faktör analizi için uygun (p < 0.05)")
    else:
        print("[!] Faktör analizi için uygun değil (p >= 0.05)")
        return None

    # Faktör sayısını belirle (eigenvalue > 1)
    if n_factors is None:
        fa_temp = FactorAnalyzer(n_factors=len(items), rotation=None)
        fa_temp.fit(df_items)
        eigenvalues = fa_temp.get_eigenvalues()[0]
        n_factors = sum(eigenvalues > 1)
        print(f"\n[FAKTÖR SAYISI]")
        print(f"Eigenvalue > 1 kriteri: {n_factors} faktör")

    # Faktör analizi
    fa = FactorAnalyzer(n_factors=n_factors, rotation='varimax')
    fa.fit(df_items)

    # Faktör yükleri
    loadings = pd.DataFrame(
        fa.loadings_,
        columns=[f'Factor{i+1}' for i in range(n_factors)],
        index=items
    )

    print(f"\n[FAKTÖR YÜKLERİ]")
    print(loadings.round(3).to_string())

    # Açıklanan varyans
    variance = fa.get_factor_variance()
    variance_df = pd.DataFrame({
        'Factor': [f'Factor{i+1}' for i in range(n_factors)],
        'SS_Loadings': variance[0],
        'Prop_Var': variance[1],
        'Cum_Var': variance[2]
    })

    print(f"\n[AÇIKLANAN VARYANS]")
    print(variance_df.to_string())
    print(f"\nToplam açıklanan varyans: {variance[2][-1]*100:.1f}%")

    # Communalities
    communalities = pd.DataFrame({
        'Item': items,
        'Communality': fa.get_communalities()
    })

    print(f"\n[COMMUNALITIES]")
    low_comm = communalities[communalities['Communality'] < 0.4]
    if not low_comm.empty:
        print("Düşük communality (<0.4) olan itemler:")
        for _, item in low_comm.iterrows():
            print(f"  - {item['Item']}: {item['Communality']:.3f}")

    return {
        'kmo': kmo_model,
        'bartlett_chi2': chi_square_value,
        'bartlett_p': p_value,
        'n_factors': n_factors,
        'loadings': loadings,
        'variance': variance_df,
        'communalities': communalities
    }

def create_reliability_plots(results_dict):
    """Güvenilirlik analizi grafiklerini oluşturur"""

    import os
    os.makedirs('results/figures', exist_ok=True)

    # Cronbach's Alpha karşılaştırması
    if results_dict:
        scales = []
        alphas = []

        for scale_name, result in results_dict.items():
            if result and 'alpha' in result:
                scales.append(scale_name)
                alphas.append(result['alpha'])

        if scales:
            plt.figure(figsize=(10, 6))
            colors = ['green' if a >= 0.7 else 'orange' if a >= 0.6 else 'red' for a in alphas]
            bars = plt.bar(scales, alphas, color=colors)

            # Referans çizgileri
            plt.axhline(y=0.7, color='green', linestyle='--', alpha=0.5, label='Kabul edilebilir (0.70)')
            plt.axhline(y=0.8, color='blue', linestyle='--', alpha=0.5, label='İyi (0.80)')

            plt.xlabel('Ölçek')
            plt.ylabel("Cronbach's Alpha")
            plt.title("Ölçek Güvenilirlikleri")
            plt.legend()
            plt.ylim(0, 1)

            # Değerleri bar üzerine yaz
            for bar, alpha in zip(bars, alphas):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{alpha:.3f}', ha='center', va='bottom')

            plt.tight_layout()
            plt.savefig('results/figures/reliability_comparison.png', dpi=300)
            plt.close()
            print("\n[✓] Güvenilirlik grafiği kaydedildi: results/figures/reliability_comparison.png")

def save_reliability_results(results_dict):
    """Güvenilirlik analizi sonuçlarını kaydet"""

    import os
    os.makedirs('results/tables', exist_ok=True)

    with pd.ExcelWriter('results/tables/reliability_analysis.xlsx') as writer:
        # Özet tablo
        summary = []
        for scale_name, result in results_dict.items():
            if result:
                summary.append({
                    'Scale': scale_name,
                    'N_Items': result.get('n_items', 'N/A'),
                    'N_Complete': result.get('n_complete', 'N/A'),
                    'Cronbach_Alpha': result.get('alpha', 'N/A'),
                    'Reliability': result.get('reliability', 'N/A')
                })

        if summary:
            pd.DataFrame(summary).to_excel(writer, sheet_name='Summary', index=False)

        # Her ölçek için detaylı sonuçlar
        for scale_name, result in results_dict.items():
            if result and 'item_stats' in result:
                result['item_stats'].to_excel(writer, sheet_name=f'{scale_name[:20]}_Items', index=False)

    print("[✓] Güvenilirlik sonuçları kaydedildi: results/tables/reliability_analysis.xlsx")

def main():
    """Ana fonksiyon"""

    print("="*60)
    print("GÜVENİLİRLİK VE FAKTÖR ANALİZLERİ")
    print("="*60)

    # Veriyi yükle
    df = load_data()
    if df is None:
        return

    results = {}

    # 1. Beck Depresyon Ölçeği güvenilirlik analizi
    beck_items = [col for col in df.columns if col.startswith('Beck_') and not col.endswith('_Score')]
    if len(beck_items) >= 3:
        print("\n[1] BECK DEPRESYON ÖLÇEĞİ")
        beck_results = reliability_analysis(df, 'Beck Depression', beck_items[:21])
        if beck_results:
            results['Beck_Depression'] = beck_results

    # 2. EMBU ölçekleri (eğer varsa)
    embu_items = [col for col in df.columns if 'EMBU' in col.upper()]
    if len(embu_items) >= 3:
        print("\n[2] EMBU ÖLÇEĞİ")
        embu_results = reliability_analysis(df, 'EMBU', embu_items)
        if embu_results:
            results['EMBU'] = embu_results

    # 3. Faktör analizi (Beck için)
    if len(beck_items) >= 5 and len(df) >= 100:
        print("\n[3] BECK ÖLÇEĞİ FAKTÖR ANALİZİ")
        factor_results = factor_analysis(df, beck_items[:10])  # İlk 10 madde
        if factor_results:
            results['Beck_Factor_Analysis'] = factor_results

    # Grafikleri oluştur
    create_reliability_plots(results)

    # Sonuçları kaydet
    save_reliability_results(results)

    print("\n" + "="*60)
    print("GÜVENİLİRLİK ANALİZLERİ TAMAMLANDI!")
    print("="*60)

if __name__ == "__main__":
    main()