"""
KAPSAMLI EMBU ANALİZİ
=====================
EMBU Çocuk ve EMBU Ebeveyn skorlarının detaylı analizi
Gruplar arası farklılıkların tespiti

EMBU (Egna Minnen Beträffande Uppfostran - "Memories of Upbringing")
Ebeveynlik tutumlarını değerlendiren ölçek

Alt Boyutlar:
1. Duygusal Sıcaklık (Emotional Warmth)
2. Reddedicilik (Rejection)
3. Aşırı Koruma (Overprotection)
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import (
    mannwhitneyu, ttest_ind,
    wilcoxon, ttest_rel,
    kruskal, f_oneway,
    pearsonr, spearmanr,
    chi2_contingency
)
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
sns.set_palette("husl")

class EMBUAnalysis:
    """EMBU skorları kapsamlı analiz sınıfı"""

    def __init__(self, data_path='data/cleaned/dataset_beck_corrected.csv'):
        self.data_path = data_path
        self.df = None
        self.results = {}

        # EMBU alt boyut maddeleri
        self.embu_parent_subscales = {
            'Duygusal_Sicaklik': [2, 4, 12, 14, 19, 23],
            'Reddedicilik': [1, 7, 8, 11, 13, 17, 18, 20],
            'Asiri_Koruma': [3, 5, 6, 9, 10, 15, 16, 21, 22]
        }

        # EMBU Çocuk formu maddeleri (varsa)
        self.embu_child_subscales = {
            'Duygusal_Sicaklik': [2, 6, 9, 12, 14, 19, 23],
            'Reddedicilik': [1, 7, 13, 17],
            'Asiri_Koruma': [3, 4, 5, 8, 10, 11, 15, 16, 18, 20, 21, 22]
        }

    def load_data(self):
        """Veriyi yükle ve hazırla"""
        print("="*80)
        print("VERİ YÜKLEME")
        print("="*80)

        self.df = pd.read_csv(self.data_path)
        print(f"\nToplam kayıt: {len(self.df)}")

        # EMBU sütunlarını kontrol et
        embu_cols = [col for col in self.df.columns if 'EMBU' in col or 'embu' in col]
        print(f"\nEMBU ile ilgili sütun sayısı: {len(embu_cols)}")

        if embu_cols:
            print("\nİlk 10 EMBU sütunu:")
            for col in embu_cols[:10]:
                non_null = self.df[col].notna().sum()
                print(f"  {col}: {non_null}/{len(self.df)} dolu ({non_null/len(self.df)*100:.1f}%)")

        # Grupları kontrol et
        if 'Grup' in self.df.columns:
            print(f"\nGrup dağılımı:")
            for grup, count in self.df['Grup'].value_counts().items():
                print(f"  {grup}: {count} ({count/len(self.df)*100:.1f}%)")

        return self.df

    def calculate_embu_subscales(self):
        """EMBU alt boyut skorlarını hesapla"""
        print("\n" + "="*80)
        print("EMBU ALT BOYUT SKORLARI HESAPLAMA")
        print("="*80)

        # EBEVEYN EMBU skorları
        print("\n1. EBEVEYN EMBU SKORLARI")
        print("-" * 50)

        for subscale, items in self.embu_parent_subscales.items():
            # Boşluklu sütun isimleri için
            cols = [f'Ebeveyn EMBU {i}' for i in items]
            # Alternatif isimler de kontrol et
            alt_cols = [f'Ebeveyn_EMBU_{i}' for i in items]

            available = [col for col in cols if col in self.df.columns]
            if not available:
                available = [col for col in alt_cols if col in self.df.columns]

            if available:
                # Alt boyut skorunu hesapla (ortalama)
                # Önce numeric'e çevir
                for col in available:
                    self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

                self.df[f'EMBU_Parent_{subscale}'] = self.df[available].mean(axis=1)

                print(f"\n{subscale}:")
                print(f"  Maddeler: {items}")
                print(f"  Mevcut: {len(available)}/{len(items)}")

                # Tanımlayıcı istatistikler
                score = self.df[f'EMBU_Parent_{subscale}'].dropna()
                if len(score) > 0:
                    print(f"  N = {len(score)}")
                    print(f"  Ortalama = {score.mean():.2f} ± {score.std():.2f}")
                    print(f"  Medyan = {score.median():.2f}")
                    print(f"  Min-Max = {score.min():.2f} - {score.max():.2f}")

        # ÇOCUK EMBU skorları (eğer varsa)
        print("\n2. ÇOCUK EMBU SKORLARI")
        print("-" * 50)

        # Önce çocuk EMBU sütunlarını kontrol et
        child_embu_cols = [col for col in self.df.columns if 'Cocuk_EMBU' in col or 'Child_EMBU' in col]

        if child_embu_cols:
            for subscale, items in self.embu_child_subscales.items():
                cols = [f'Cocuk_EMBU_{i}' for i in items]
                available = [col for col in cols if col in self.df.columns]

                if available:
                    self.df[f'EMBU_Child_{subscale}'] = self.df[available].mean(axis=1)

                    print(f"\n{subscale}:")
                    print(f"  Maddeler: {items}")
                    print(f"  Mevcut: {len(available)}/{len(items)}")

                    score = self.df[f'EMBU_Child_{subscale}'].dropna()
                    if len(score) > 0:
                        print(f"  N = {len(score)}")
                        print(f"  Ortalama = {score.mean():.2f} ± {score.std():.2f}")
        else:
            print("Çocuk EMBU verileri bulunamadı")

    def analyze_group_differences(self):
        """Gruplar arası EMBU farklılıklarını analiz et"""
        print("\n" + "="*80)
        print("GRUPLAR ARASI EMBU FARKLILIKLARI")
        print("="*80)

        if 'Grup' not in self.df.columns:
            print("[UYARI] Grup değişkeni bulunamadı")
            return

        # Analiz edilecek EMBU skorları
        embu_scores = [col for col in self.df.columns if 'EMBU_Parent_' in col or 'EMBU_Child_' in col]

        group_results = {}

        for score_col in embu_scores:
            print(f"\n{score_col.replace('_', ' ')}")
            print("-" * 50)

            # Grupları ayır
            diyabet = self.df[self.df['Grup'] == 'Diyabet'][score_col].dropna()
            kontrol = self.df[self.df['Grup'] == 'Kontrol'][score_col].dropna()

            if len(diyabet) > 0 and len(kontrol) > 0:
                # Tanımlayıcı istatistikler
                print(f"Diyabet (n={len(diyabet)}): {diyabet.mean():.2f} ± {diyabet.std():.2f}")
                print(f"Kontrol (n={len(kontrol)}): {kontrol.mean():.2f} ± {kontrol.std():.2f}")
                print(f"Fark: {diyabet.mean() - kontrol.mean():.2f}")

                # Normallik testi
                _, p_norm_d = stats.shapiro(diyabet) if len(diyabet) <= 5000 else stats.normaltest(diyabet)
                _, p_norm_k = stats.shapiro(kontrol) if len(kontrol) <= 5000 else stats.normaltest(kontrol)

                # Test seçimi
                if p_norm_d > 0.05 and p_norm_k > 0.05:
                    # Parametrik: Independent t-test
                    stat, p_value = ttest_ind(diyabet, kontrol)
                    test_name = "Independent t-test"

                    # Cohen's d
                    pooled_std = np.sqrt(((len(diyabet)-1)*diyabet.std()**2 +
                                         (len(kontrol)-1)*kontrol.std()**2) /
                                        (len(diyabet)+len(kontrol)-2))
                    cohens_d = (diyabet.mean() - kontrol.mean()) / pooled_std
                    effect_size = f"Cohen's d = {cohens_d:.3f}"
                else:
                    # Non-parametrik: Mann-Whitney U
                    stat, p_value = mannwhitneyu(diyabet, kontrol, alternative='two-sided')
                    test_name = "Mann-Whitney U"

                    # Etki büyüklüğü r
                    z = (stat - len(diyabet)*len(kontrol)/2) / np.sqrt(len(diyabet)*len(kontrol)*(len(diyabet)+len(kontrol)+1)/12)
                    r = abs(z) / np.sqrt(len(diyabet) + len(kontrol))
                    effect_size = f"r = {r:.3f}"

                print(f"\nTest: {test_name}")
                print(f"İstatistik: {stat:.3f}")
                print(f"p-değeri: {p_value:.4f}")
                print(f"Etki büyüklüğü: {effect_size}")

                # Sonuç yorumu
                if p_value < 0.05:
                    print(f"SONUÇ: İstatistiksel olarak ANLAMLI fark var (p<0.05)")
                    if diyabet.mean() > kontrol.mean():
                        print(f"-> Diyabet grubunda {score_col.split('_')[-1]} daha yüksek")
                    else:
                        print(f"-> Kontrol grubunda {score_col.split('_')[-1]} daha yüksek")
                else:
                    print("SONUÇ: Anlamlı fark yok")

                # Sonuçları kaydet
                group_results[score_col] = {
                    'test': test_name,
                    'statistic': stat,
                    'p_value': p_value,
                    'effect_size': effect_size,
                    'diyabet_mean': diyabet.mean(),
                    'diyabet_std': diyabet.std(),
                    'kontrol_mean': kontrol.mean(),
                    'kontrol_std': kontrol.std(),
                    'significant': p_value < 0.05
                }

        self.results['group_differences'] = group_results
        return group_results

    def analyze_subgroup_differences(self):
        """Alt gruplar (index ve kardeşler) arası EMBU farklılıkları"""
        print("\n" + "="*80)
        print("ALT GRUPLAR ARASI EMBU ANALİZİ")
        print("="*80)

        if 'Alt_Grup' not in self.df.columns:
            print("[UYARI] Alt grup değişkeni bulunamadı")
            return

        embu_scores = [col for col in self.df.columns if 'EMBU_Parent_' in col]

        for score_col in embu_scores:
            print(f"\n{score_col.replace('_', ' ')}")
            print("-" * 50)

            # 4 alt grup
            groups = []
            group_names = []

            for alt_grup in ['Diyabet_Index', 'Diyabet_Kardes', 'Kontrol_Index', 'Kontrol_Kardes']:
                data = self.df[self.df['Alt_Grup'] == alt_grup][score_col].dropna()
                if len(data) > 0:
                    groups.append(data)
                    group_names.append(alt_grup)
                    print(f"{alt_grup}: {data.mean():.2f} ± {data.std():.2f} (n={len(data)})")

            if len(groups) >= 3:
                # Kruskal-Wallis testi (non-parametrik ANOVA)
                stat, p_value = kruskal(*groups)
                print(f"\nKruskal-Wallis H testi:")
                print(f"  H = {stat:.3f}, p = {p_value:.4f}")

                if p_value < 0.05:
                    print("  SONUÇ: Alt gruplar arasında anlamlı fark var")

                    # Post-hoc: İkili Mann-Whitney U testleri
                    print("\n  Post-hoc ikili karşılaştırmalar:")
                    for i in range(len(groups)):
                        for j in range(i+1, len(groups)):
                            _, p = mannwhitneyu(groups[i], groups[j], alternative='two-sided')
                            if p < 0.05:
                                print(f"    {group_names[i]} vs {group_names[j]}: p = {p:.4f} *")
                else:
                    print("  SONUÇ: Alt gruplar arasında anlamlı fark yok")

    def analyze_parent_child_correlation(self):
        """Ebeveyn ve çocuk EMBU skorları arasındaki korelasyon"""
        print("\n" + "="*80)
        print("EBEVEYN-ÇOCUK EMBU KORELASYONLARI")
        print("="*80)

        # Ebeveyn ve çocuk skorlarını eşleştir
        parent_scores = [col for col in self.df.columns if 'EMBU_Parent_' in col]
        child_scores = [col for col in self.df.columns if 'EMBU_Child_' in col]

        if not child_scores:
            print("Çocuk EMBU skorları bulunamadı, korelasyon analizi yapılamıyor")
            return

        correlation_results = {}

        for subscale in ['Duygusal_Sicaklik', 'Reddedicilik', 'Asiri_Koruma']:
            parent_col = f'EMBU_Parent_{subscale}'
            child_col = f'EMBU_Child_{subscale}'

            if parent_col in self.df.columns and child_col in self.df.columns:
                # Ortak gözlemleri bul
                valid_idx = self.df[[parent_col, child_col]].dropna().index

                if len(valid_idx) > 3:
                    parent_data = self.df.loc[valid_idx, parent_col]
                    child_data = self.df.loc[valid_idx, child_col]

                    # Spearman korelasyonu (non-parametrik)
                    r_spearman, p_spearman = spearmanr(parent_data, child_data)

                    # Pearson korelasyonu
                    r_pearson, p_pearson = pearsonr(parent_data, child_data)

                    print(f"\n{subscale}:")
                    print(f"  N = {len(valid_idx)}")
                    print(f"  Pearson r = {r_pearson:.3f}, p = {p_pearson:.4f}")
                    print(f"  Spearman r = {r_spearman:.3f}, p = {p_spearman:.4f}")

                    if p_spearman < 0.05:
                        print(f"  -> Anlamlı korelasyon var!")

                    correlation_results[subscale] = {
                        'n': len(valid_idx),
                        'pearson_r': r_pearson,
                        'pearson_p': p_pearson,
                        'spearman_r': r_spearman,
                        'spearman_p': p_spearman
                    }

        self.results['parent_child_correlation'] = correlation_results

    def analyze_embu_beck_relationship(self):
        """EMBU skorları ile Beck depresyon skorları arasındaki ilişki"""
        print("\n" + "="*80)
        print("EMBU - BECK DEPRESYON İLİŞKİSİ")
        print("="*80)

        # Beck skorunu bul
        beck_col = None
        for col in ['Beck Toplam', 'Beck_Total_Score', 'Beck_Calculated_New']:
            if col in self.df.columns:
                beck_col = col
                break

        if not beck_col:
            print("Beck skoru bulunamadı")
            return

        embu_scores = [col for col in self.df.columns if 'EMBU_Parent_' in col]

        relationship_results = {}

        for embu_col in embu_scores:
            # Ortak gözlemler
            valid_idx = self.df[[embu_col, beck_col]].dropna().index

            if len(valid_idx) > 10:
                embu_data = self.df.loc[valid_idx, embu_col]
                beck_data = self.df.loc[valid_idx, beck_col]

                # Korelasyon analizi
                r, p = spearmanr(embu_data, beck_data)

                subscale = embu_col.split('_')[-1]
                print(f"\n{subscale} - Beck Depresyon:")
                print(f"  N = {len(valid_idx)}")
                print(f"  Spearman r = {r:.3f}")
                print(f"  p-değeri = {p:.4f}")

                if p < 0.05:
                    if r > 0:
                        print(f"  -> {subscale} arttıkça depresyon artıyor")
                    else:
                        print(f"  -> {subscale} arttıkça depresyon azalıyor")

                    # Korelasyon gücü
                    if abs(r) < 0.3:
                        strength = "Zayıf"
                    elif abs(r) < 0.7:
                        strength = "Orta"
                    else:
                        strength = "Güçlü"
                    print(f"  İlişki gücü: {strength}")

                relationship_results[subscale] = {
                    'n': len(valid_idx),
                    'r': r,
                    'p': p,
                    'significant': p < 0.05
                }

        self.results['embu_beck_relationship'] = relationship_results

    def create_visualizations(self):
        """EMBU skorları görselleştirmeleri"""
        print("\n" + "="*80)
        print("GÖRSELLEŞTİRMELER")
        print("="*80)

        embu_parent_cols = [col for col in self.df.columns if 'EMBU_Parent_' in col]

        if not embu_parent_cols:
            print("EMBU skorları bulunamadı")
            return

        fig, axes = plt.subplots(2, 3, figsize=(16, 10))
        axes = axes.flatten()

        for idx, embu_col in enumerate(embu_parent_cols[:6]):
            if idx < len(axes):
                ax = axes[idx]
                subscale = embu_col.split('_')[-1]

                # Grup karşılaştırması - Box plot
                if 'Grup' in self.df.columns:
                    data_to_plot = []
                    labels = []
                    colors = []

                    for grup in ['Diyabet', 'Kontrol']:
                        grup_data = self.df[self.df['Grup'] == grup][embu_col].dropna()
                        if len(grup_data) > 0:
                            data_to_plot.append(grup_data)
                            labels.append(grup)
                            colors.append('salmon' if grup == 'Diyabet' else 'lightblue')

                    if data_to_plot:
                        bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True)
                        for patch, color in zip(bp['boxes'], colors):
                            patch.set_facecolor(color)
                            patch.set_alpha(0.7)

                        # Ortalama çizgileri
                        for i, data in enumerate(data_to_plot):
                            ax.hlines(data.mean(), i+0.75, i+1.25, colors='red',
                                     linestyles='--', linewidth=2, label='Ortalama' if i==0 else '')

                        ax.set_title(f'{subscale}', fontsize=12, fontweight='bold')
                        ax.set_ylabel('Skor', fontsize=10)
                        ax.grid(True, alpha=0.3)

                        # İstatistiksel test sonucu
                        if len(data_to_plot) == 2:
                            _, p = mannwhitneyu(data_to_plot[0], data_to_plot[1], alternative='two-sided')
                            if p < 0.001:
                                sig_text = '***'
                            elif p < 0.01:
                                sig_text = '**'
                            elif p < 0.05:
                                sig_text = '*'
                            else:
                                sig_text = 'ns'
                            ax.text(0.5, 0.95, f'p={p:.3f} {sig_text}',
                                   transform=ax.transAxes, ha='center', fontsize=10)

        # Kullanılmayan subplot'ları gizle
        for idx in range(len(embu_parent_cols), len(axes)):
            axes[idx].axis('off')

        plt.suptitle('EMBU Ebeveynlik Tutumları - Grup Karşılaştırmaları',
                    fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig('results/embu_group_comparisons.png', dpi=300, bbox_inches='tight')
        plt.close()

        print("[OK] EMBU grup karşılaştırma grafikleri kaydedildi")

        # Korelasyon ısı haritası
        self.create_correlation_heatmap()

    def create_correlation_heatmap(self):
        """EMBU skorları korelasyon ısı haritası"""

        # EMBU ve Beck skorlarını seç
        cols_to_correlate = []

        # EMBU skorları
        embu_cols = [col for col in self.df.columns if 'EMBU_Parent_' in col or 'EMBU_Child_' in col]
        cols_to_correlate.extend(embu_cols)

        # Beck skoru
        for col in ['Beck Toplam', 'Beck_Total_Score', 'Beck_Calculated_New']:
            if col in self.df.columns:
                cols_to_correlate.append(col)
                break

        if len(cols_to_correlate) > 1:
            # Korelasyon matrisi
            corr_data = self.df[cols_to_correlate].dropna()

            if len(corr_data) > 10:
                corr_matrix = corr_data.corr(method='spearman')

                # Görselleştirme
                plt.figure(figsize=(10, 8))
                mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)

                sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
                           cmap='coolwarm', center=0, vmin=-1, vmax=1,
                           square=True, linewidths=1,
                           cbar_kws={"shrink": 0.8, "label": "Spearman Korelasyon"})

                plt.title('EMBU ve Beck Skorları Korelasyon Matrisi',
                         fontsize=12, fontweight='bold', pad=20)

                # Sütun isimlerini kısalt
                labels = []
                for col in corr_matrix.columns:
                    if 'EMBU_Parent_' in col:
                        labels.append(f"E-{col.split('_')[-1][:3]}")
                    elif 'EMBU_Child_' in col:
                        labels.append(f"Ç-{col.split('_')[-1][:3]}")
                    elif 'Beck' in col:
                        labels.append('Beck')
                    else:
                        labels.append(col[:10])

                plt.gca().set_xticklabels(labels, rotation=45, ha='right')
                plt.gca().set_yticklabels(labels, rotation=0)

                plt.tight_layout()
                plt.savefig('results/embu_correlation_heatmap.png', dpi=300, bbox_inches='tight')
                plt.close()

                print("[OK] EMBU korelasyon ısı haritası kaydedildi")

    def generate_report(self):
        """Detaylı EMBU analiz raporu"""
        print("\n" + "="*80)
        print("RAPOR OLUŞTURMA")
        print("="*80)

        report_lines = []
        report_lines.append("="*80)
        report_lines.append("EMBU EBEVEYNLİK TUTUMLARI KAPSAMLı ANALİZ RAPORU")
        report_lines.append("="*80)
        report_lines.append(f"\nTarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report_lines.append(f"Veri: {self.data_path}")

        # 1. GRUPLAR ARASI FARKLILIKLAR
        report_lines.append("\n" + "="*80)
        report_lines.append("1. GRUPLAR ARASI EMBU FARKLILIKLARI")
        report_lines.append("="*80)

        if 'group_differences' in self.results:
            significant_findings = []

            for score, result in self.results['group_differences'].items():
                subscale = score.split('_')[-1]
                report_lines.append(f"\n{subscale}:")
                report_lines.append(f"  Diyabet: {result['diyabet_mean']:.2f} ± {result['diyabet_std']:.2f}")
                report_lines.append(f"  Kontrol: {result['kontrol_mean']:.2f} ± {result['kontrol_std']:.2f}")
                report_lines.append(f"  Test: {result['test']}")
                report_lines.append(f"  p-değeri: {result['p_value']:.4f}")
                report_lines.append(f"  {result['effect_size']}")

                if result['significant']:
                    report_lines.append(f"  SONUÇ: **ANLAMLI FARK VAR**")

                    if result['diyabet_mean'] > result['kontrol_mean']:
                        direction = "Diyabet grubunda daha yüksek"
                    else:
                        direction = "Kontrol grubunda daha yüksek"

                    significant_findings.append(f"{subscale}: {direction} (p={result['p_value']:.3f})")
                else:
                    report_lines.append(f"  SONUÇ: Anlamlı fark yok")

            # Anlamlı bulgular özeti
            if significant_findings:
                report_lines.append("\n" + "-"*50)
                report_lines.append("ANLAMLI BULGULAR:")
                for finding in significant_findings:
                    report_lines.append(f"  • {finding}")

        # 2. EMBU-BECK İLİŞKİSİ
        report_lines.append("\n" + "="*80)
        report_lines.append("2. EMBU - BECK DEPRESYON İLİŞKİSİ")
        report_lines.append("="*80)

        if 'embu_beck_relationship' in self.results:
            significant_correlations = []

            for subscale, result in self.results['embu_beck_relationship'].items():
                report_lines.append(f"\n{subscale}:")
                report_lines.append(f"  Korelasyon: r = {result['r']:.3f}")
                report_lines.append(f"  p-değeri: {result['p']:.4f}")
                report_lines.append(f"  N: {result['n']}")

                if result['significant']:
                    if result['r'] > 0:
                        direction = "pozitif"
                    else:
                        direction = "negatif"

                    significant_correlations.append(
                        f"{subscale}: {direction} ilişki (r={result['r']:.3f}, p={result['p']:.3f})"
                    )

            if significant_correlations:
                report_lines.append("\n" + "-"*50)
                report_lines.append("ANLAMLI İLİŞKİLER:")
                for corr in significant_correlations:
                    report_lines.append(f"  • {corr}")

        # 3. KLİNİK YORUMLAR
        report_lines.append("\n" + "="*80)
        report_lines.append("3. KLİNİK YORUMLAR VE ÖNERİLER")
        report_lines.append("="*80)

        report_lines.append("\nANA BULGULAR:")
        report_lines.append("• Diyabetli çocukların ebeveynlerinde farklı tutum paternleri gözlenebilir")
        report_lines.append("• Ebeveynlik tutumları ile maternal depresyon arasında ilişki olabilir")
        report_lines.append("• Aile dinamiklerinin hastalık yönetimine etkisi değerlendirilmeli")

        report_lines.append("\nÖNERİLER:")
        report_lines.append("• Aile danışmanlığı programları geliştirilmeli")
        report_lines.append("• Ebeveynlik becerilerini güçlendirici müdahaleler planlanmalı")
        report_lines.append("• Longitudinal takip çalışmaları yapılmalı")

        report_lines.append("\n" + "="*80)

        # Raporu kaydet
        report_text = "\n".join(report_lines)

        with open('results/embu_comprehensive_report.txt', 'w', encoding='utf-8') as f:
            f.write(report_text)

        print("[OK] EMBU analiz raporu kaydedildi: embu_comprehensive_report.txt")

        # JSON olarak da kaydet
        with open('results/embu_analysis_results.json', 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': self.results,
                'n_samples': len(self.df)
            }, f, indent=2, default=str)

        print("[OK] JSON sonuçları kaydedildi: embu_analysis_results.json")

        return report_text

    def run_complete_analysis(self):
        """Tüm EMBU analizlerini çalıştır"""
        print("\n" + "="*80)
        print("KAPSAMLI EMBU ANALİZİ BAŞLIYOR")
        print("="*80)

        # 1. Veri yükleme
        self.load_data()

        # 2. Alt boyut skorlarını hesapla
        self.calculate_embu_subscales()

        # 3. Gruplar arası farklılıklar
        self.analyze_group_differences()

        # 4. Alt gruplar arası farklılıklar
        self.analyze_subgroup_differences()

        # 5. Ebeveyn-çocuk korelasyonları
        self.analyze_parent_child_correlation()

        # 6. EMBU-Beck ilişkisi
        self.analyze_embu_beck_relationship()

        # 7. Görselleştirmeler
        self.create_visualizations()

        # 8. Rapor oluştur
        self.generate_report()

        print("\n" + "="*80)
        print("ANALİZ TAMAMLANDI")
        print("="*80)

        return self.results

def main():
    """Ana fonksiyon"""

    try:
        # EMBU analiz sınıfını başlat
        embu_analysis = EMBUAnalysis()

        # Tüm analizleri çalıştır
        results = embu_analysis.run_complete_analysis()

        print("\n" + "="*80)
        print("BAŞARILI")
        print("="*80)
        print("\nOluşturulan dosyalar:")
        print("  - results/embu_comprehensive_report.txt")
        print("  - results/embu_analysis_results.json")
        print("  - results/embu_group_comparisons.png")
        print("  - results/embu_correlation_heatmap.png")

        # Anlamlı bulgular özeti
        if 'group_differences' in results:
            print("\nANLAMLI BULGULAR:")
            for score, result in results['group_differences'].items():
                if result['significant']:
                    subscale = score.split('_')[-1]
                    print(f"  • {subscale}: p = {result['p_value']:.4f}")

        return results

    except Exception as e:
        print(f"\n[HATA] {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()