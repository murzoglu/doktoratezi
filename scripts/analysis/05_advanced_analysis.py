"""
05_advanced_analysis.py
İleri istatistiksel analizler: Regresyon, Mediasyon, Moderasyon
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import cross_val_score
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

def multiple_regression_analysis(df, dependent_var, independent_vars):
    """Çoklu doğrusal regresyon analizi"""

    print("\n" + "="*60)
    print("ÇOKLU DOĞRUSAL REGRESYON ANALİZİ")
    print("="*60)
    print(f"Bağımlı Değişken: {dependent_var}")
    print(f"Bağımsız Değişkenler: {', '.join(independent_vars)}")

    # Eksik verileri temizle
    vars_to_use = [dependent_var] + independent_vars
    df_clean = df[vars_to_use].dropna()

    if len(df_clean) < 20:
        print(f"[!] Yetersiz veri (n={len(df_clean)}). En az 20 gözlem gerekli.")
        return None

    # Bağımsız değişkenleri hazırla
    X = df_clean[independent_vars]
    y = df_clean[dependent_var]

    # Sabit terim ekle
    X = sm.add_constant(X)

    # Model oluştur ve fit et
    model = sm.OLS(y, X)
    results = model.fit()

    # Sonuçları yazdır
    print("\n" + results.summary().as_text())

    # Model metrikleri
    print("\n[MODEL METRİKLERİ]")
    print(f"R-squared: {results.rsquared:.4f}")
    print(f"Adjusted R-squared: {results.rsquared_adj:.4f}")
    print(f"F-statistic: {results.fvalue:.4f}")
    print(f"Prob (F-statistic): {results.f_pvalue:.4f}")

    # Katsayılar tablosu
    coef_df = pd.DataFrame({
        'Coefficient': results.params,
        'Std_Error': results.bse,
        't_value': results.tvalues,
        'p_value': results.pvalues,
        'Lower_95%': results.conf_int()[0],
        'Upper_95%': results.conf_int()[1]
    })

    print("\n[KATSAYILAR]")
    print(coef_df.to_string())

    # VIF (Variance Inflation Factor) - Multicollinearity check
    from statsmodels.stats.outliers_influence import variance_inflation_factor

    vif_data = pd.DataFrame()
    vif_data["Variable"] = X.columns
    vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]

    print("\n[MULTICOLLINEARITY CHECK - VIF]")
    print(vif_data[vif_data["Variable"] != "const"].to_string())
    print("(VIF > 10 indicates multicollinearity problem)")

    return results, coef_df

def logistic_regression_analysis(df, dependent_var, independent_vars):
    """Lojistik regresyon analizi"""

    print("\n" + "="*60)
    print("LOJİSTİK REGRESYON ANALİZİ")
    print("="*60)

    # Veriyi hazırla
    vars_to_use = [dependent_var] + independent_vars
    df_clean = df[vars_to_use].dropna()

    if len(df_clean) < 20:
        print(f"[!] Yetersiz veri (n={len(df_clean)})")
        return None

    X = df_clean[independent_vars]
    y = df_clean[dependent_var]

    # Binary değişken kontrolü
    if len(y.unique()) != 2:
        print(f"[!] {dependent_var} binary değil. {len(y.unique())} farklı değer var.")
        return None

    # Model oluştur
    X = sm.add_constant(X)
    model = sm.Logit(y, X)
    results = model.fit(disp=0)

    print("\n" + results.summary().as_text())

    # Odds ratios
    odds_ratios = np.exp(results.params)
    odds_ci = np.exp(results.conf_int())

    odds_df = pd.DataFrame({
        'OR': odds_ratios,
        'Lower_95%': odds_ci[0],
        'Upper_95%': odds_ci[1],
        'p_value': results.pvalues
    })

    print("\n[ODDS RATIOS]")
    print(odds_df.to_string())

    # Model performans metrikleri
    from sklearn.metrics import classification_report, roc_auc_score

    y_pred = results.predict(X) > 0.5
    print("\n[MODEL PERFORMANSI]")
    print(classification_report(y, y_pred, target_names=['Grup 0', 'Grup 1']))

    if len(np.unique(y)) == 2:
        auc = roc_auc_score(y, results.predict(X))
        print(f"AUC: {auc:.4f}")

    return results, odds_df

def mediation_analysis(df, x_var, mediator_var, y_var, covariates=None):
    """Mediasyon (aracılık) analizi - Baron & Kenny yöntemi"""

    print("\n" + "="*60)
    print("MEDİASYON ANALİZİ")
    print("="*60)
    print(f"X (Bağımsız): {x_var}")
    print(f"M (Aracı): {mediator_var}")
    print(f"Y (Bağımlı): {y_var}")

    # Veriyi hazırla
    vars_needed = [x_var, mediator_var, y_var]
    if covariates:
        vars_needed.extend(covariates)

    df_clean = df[vars_needed].dropna()

    if len(df_clean) < 30:
        print(f"[!] Yetersiz veri (n={len(df_clean)}). Mediasyon için en az 30 gözlem önerilir.")
        return None

    # Step 1: X -> Y (c path - total effect)
    print("\n[STEP 1: Total Effect (c path)]")
    formula1 = f"{y_var} ~ {x_var}"
    if covariates:
        formula1 += " + " + " + ".join(covariates)

    model1 = smf.ols(formula1, data=df_clean).fit()
    c_path = model1.params[x_var]
    c_pvalue = model1.pvalues[x_var]
    print(f"c = {c_path:.4f}, p = {c_pvalue:.4f}")

    # Step 2: X -> M (a path)
    print("\n[STEP 2: X -> Mediator (a path)]")
    formula2 = f"{mediator_var} ~ {x_var}"
    if covariates:
        formula2 += " + " + " + ".join(covariates)

    model2 = smf.ols(formula2, data=df_clean).fit()
    a_path = model2.params[x_var]
    a_pvalue = model2.pvalues[x_var]
    print(f"a = {a_path:.4f}, p = {a_pvalue:.4f}")

    # Step 3: X + M -> Y (b and c' paths)
    print("\n[STEP 3: Direct and Indirect Effects]")
    formula3 = f"{y_var} ~ {x_var} + {mediator_var}"
    if covariates:
        formula3 += " + " + " + ".join(covariates)

    model3 = smf.ols(formula3, data=df_clean).fit()
    b_path = model3.params[mediator_var]
    b_pvalue = model3.pvalues[mediator_var]
    c_prime_path = model3.params[x_var]
    c_prime_pvalue = model3.pvalues[x_var]

    print(f"b = {b_path:.4f}, p = {b_pvalue:.4f}")
    print(f"c' = {c_prime_path:.4f}, p = {c_prime_pvalue:.4f}")

    # Indirect effect (a*b)
    indirect_effect = a_path * b_path
    print(f"\n[INDIRECT EFFECT]")
    print(f"a*b = {indirect_effect:.4f}")

    # Sobel test for indirect effect
    from scipy import stats
    se_a = model2.bse[x_var]
    se_b = model3.bse[mediator_var]
    se_ab = np.sqrt(b_path**2 * se_a**2 + a_path**2 * se_b**2)
    z_sobel = indirect_effect / se_ab if se_ab > 0 else 0
    p_sobel = 2 * (1 - stats.norm.cdf(abs(z_sobel)))

    print(f"Sobel test: z = {z_sobel:.4f}, p = {p_sobel:.4f}")

    # Proportion mediated
    if c_path != 0:
        prop_mediated = indirect_effect / c_path
        print(f"Proportion mediated: {prop_mediated:.2%}")

    # Mediation type
    if p_sobel < 0.05:
        if c_prime_pvalue >= 0.05:
            print("\n[SONUÇ] TAM MEDİASYON")
        else:
            print("\n[SONUÇ] KISMİ MEDİASYON")
    else:
        print("\n[SONUÇ] MEDİASYON YOK")

    return {
        'total_effect': c_path,
        'direct_effect': c_prime_path,
        'indirect_effect': indirect_effect,
        'sobel_z': z_sobel,
        'sobel_p': p_sobel
    }

def moderation_analysis(df, x_var, moderator_var, y_var):
    """Moderasyon (düzenleyicilik) analizi"""

    print("\n" + "="*60)
    print("MODERASYON ANALİZİ")
    print("="*60)
    print(f"X (Bağımsız): {x_var}")
    print(f"W (Moderatör): {moderator_var}")
    print(f"Y (Bağımlı): {y_var}")

    # Veriyi hazırla
    df_clean = df[[x_var, moderator_var, y_var]].dropna()

    # Değişkenleri standardize et (interaction için)
    scaler = StandardScaler()
    df_clean[f'{x_var}_z'] = scaler.fit_transform(df_clean[[x_var]])
    df_clean[f'{moderator_var}_z'] = scaler.fit_transform(df_clean[[moderator_var]])

    # Interaction terimi oluştur
    df_clean['interaction'] = df_clean[f'{x_var}_z'] * df_clean[f'{moderator_var}_z']

    # Model
    formula = f"{y_var} ~ {x_var}_z + {moderator_var}_z + interaction"
    model = smf.ols(formula, data=df_clean).fit()

    print("\n" + model.summary().as_text())

    # Interaction etkisi
    interaction_coef = model.params['interaction']
    interaction_p = model.pvalues['interaction']

    print(f"\n[INTERACTION ETKİSİ]")
    print(f"β = {interaction_coef:.4f}, p = {interaction_p:.4f}")

    if interaction_p < 0.05:
        print("*** ANLAMLI MODERASYON ETKİSİ VAR ***")

        # Simple slopes analysis
        print("\n[SIMPLE SLOPES ANALİZİ]")

        # Düşük moderatör seviyesi (-1 SD)
        low_mod = -1
        slope_low = model.params[f'{x_var}_z'] + interaction_coef * low_mod
        print(f"Düşük {moderator_var}: β = {slope_low:.4f}")

        # Yüksek moderatör seviyesi (+1 SD)
        high_mod = 1
        slope_high = model.params[f'{x_var}_z'] + interaction_coef * high_mod
        print(f"Yüksek {moderator_var}: β = {slope_high:.4f}")
    else:
        print("Moderasyon etkisi anlamlı değil")

    return model

def hierarchical_regression(df, y_var, block1_vars, block2_vars, block3_vars=None):
    """Hiyerarşik regresyon analizi"""

    print("\n" + "="*60)
    print("HİYERARŞİK REGRESYON ANALİZİ")
    print("="*60)

    all_vars = [y_var] + block1_vars + block2_vars
    if block3_vars:
        all_vars.extend(block3_vars)

    df_clean = df[all_vars].dropna()

    results = []

    # Model 1 (Block 1)
    X1 = sm.add_constant(df_clean[block1_vars])
    y = df_clean[y_var]
    model1 = sm.OLS(y, X1).fit()
    results.append(('Model 1', model1))

    print(f"\n[MODEL 1] - {', '.join(block1_vars)}")
    print(f"R² = {model1.rsquared:.4f}, Adj. R² = {model1.rsquared_adj:.4f}")
    print(f"F = {model1.fvalue:.4f}, p = {model1.f_pvalue:.4f}")

    # Model 2 (Block 1 + Block 2)
    X2 = sm.add_constant(df_clean[block1_vars + block2_vars])
    model2 = sm.OLS(y, X2).fit()
    results.append(('Model 2', model2))

    print(f"\n[MODEL 2] - {', '.join(block1_vars + block2_vars)}")
    print(f"R² = {model2.rsquared:.4f}, Adj. R² = {model2.rsquared_adj:.4f}")
    print(f"F = {model2.fvalue:.4f}, p = {model2.f_pvalue:.4f}")

    # R² değişimi
    r2_change = model2.rsquared - model1.rsquared
    print(f"ΔR² = {r2_change:.4f}")

    # Model 3 (eğer varsa)
    if block3_vars:
        X3 = sm.add_constant(df_clean[block1_vars + block2_vars + block3_vars])
        model3 = sm.OLS(y, X3).fit()
        results.append(('Model 3', model3))

        print(f"\n[MODEL 3] - {', '.join(block1_vars + block2_vars + block3_vars)}")
        print(f"R² = {model3.rsquared:.4f}, Adj. R² = {model3.rsquared_adj:.4f}")
        print(f"F = {model3.fvalue:.4f}, p = {model3.f_pvalue:.4f}")

        r2_change2 = model3.rsquared - model2.rsquared
        print(f"ΔR² = {r2_change2:.4f}")

    return results

def save_advanced_results(results_dict):
    """İleri analiz sonuçlarını kaydet"""

    import os
    os.makedirs('results/models', exist_ok=True)

    # Her analiz için ayrı dosya oluştur
    for analysis_name, result in results_dict.items():
        if result is not None:
            if hasattr(result, 'summary'):
                # Model summary'yi text olarak kaydet
                with open(f'results/models/{analysis_name}_summary.txt', 'w') as f:
                    f.write(result.summary().as_text())

            if isinstance(result, pd.DataFrame):
                # DataFrame'leri Excel'e kaydet
                result.to_excel(f'results/models/{analysis_name}.xlsx', index=False)

    print("\n[✓] Sonuçlar results/models/ klasörüne kaydedildi")

def main():
    """Ana fonksiyon"""

    print("="*60)
    print("İLERİ İSTATİSTİKSEL ANALİZLER")
    print("="*60)

    # Veriyi yükle
    df = load_data()
    if df is None:
        return

    # Analiz sonuçlarını sakla
    results = {}

    # 1. Çoklu Regresyon - Beck skorları için
    if 'Beck_Total_Score' in df.columns:
        print("\n[1] Beck Depresyon Skorları için Çoklu Regresyon")
        predictors = ['Anne_Yas', 'Cocuk_Sayisi', 'Egitim_Durumu_Coded']
        predictors = [p for p in predictors if p in df.columns][:3]  # Max 3 değişken

        if len(predictors) >= 2:
            reg_results, coef_df = multiple_regression_analysis(
                df, 'Beck_Total_Score', predictors
            )
            if reg_results:
                results['multiple_regression'] = reg_results

    # 2. Lojistik Regresyon - Grup tahminlemesi için
    if 'Grup' in df.columns:
        print("\n[2] Grup Üyeliği için Lojistik Regresyon")
        # Grup değişkenini binary'ye çevir
        df['Grup_Binary'] = (df['Grup'] == 'Diyabet').astype(int)

        predictors = ['Beck_Total_Score', 'Anne_Yas']
        predictors = [p for p in predictors if p in df.columns]

        if len(predictors) >= 1:
            log_results, odds_df = logistic_regression_analysis(
                df, 'Grup_Binary', predictors
            )
            if log_results:
                results['logistic_regression'] = log_results

    # 3. Mediasyon Analizi örneği
    # Hipotez: Grup -> Anne_Antidepresan -> Beck_Total_Score
    required_vars = ['Grup_Binary', 'Anne_Antidepresan_Coded', 'Beck_Total_Score']
    if all(v in df.columns for v in required_vars):
        print("\n[3] Mediasyon Analizi")
        mediation_results = mediation_analysis(
            df,
            'Grup_Binary',
            'Anne_Antidepresan_Coded',
            'Beck_Total_Score'
        )
        if mediation_results:
            results['mediation'] = pd.DataFrame([mediation_results])

    # 4. Moderasyon Analizi örneği
    # Hipotez: Grup * Cocuk_Sayisi -> Beck_Total_Score
    required_vars = ['Grup_Binary', 'Cocuk_Sayisi', 'Beck_Total_Score']
    if all(v in df.columns for v in required_vars):
        print("\n[4] Moderasyon Analizi")
        mod_results = moderation_analysis(
            df,
            'Grup_Binary',
            'Cocuk_Sayisi',
            'Beck_Total_Score'
        )
        if mod_results:
            results['moderation'] = mod_results

    # 5. Hiyerarşik Regresyon
    if 'Beck_Total_Score' in df.columns:
        print("\n[5] Hiyerarşik Regresyon")

        # Block 1: Demografik değişkenler
        block1 = ['Anne_Yas', 'Cocuk_Sayisi']
        block1 = [v for v in block1 if v in df.columns]

        # Block 2: Hastalık değişkenleri
        block2 = ['Grup_Binary']
        block2 = [v for v in block2 if v in df.columns]

        if len(block1) >= 1 and len(block2) >= 1:
            hier_results = hierarchical_regression(
                df,
                'Beck_Total_Score',
                block1,
                block2
            )
            if hier_results:
                results['hierarchical_regression'] = hier_results

    # Sonuçları kaydet
    if results:
        save_advanced_results(results)

    print("\n" + "="*60)
    print("İLERİ ANALİZLER TAMAMLANDI!")
    print("="*60)
    print("\nSonraki adım: Sonuçları yorumlayın ve makale yazımına başlayın")

if __name__ == "__main__":
    main()