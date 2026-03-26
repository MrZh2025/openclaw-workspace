# -*- coding: utf-8 -*-
"""
SOR Model Analysis - SOR 模型分析
"""
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Read data
df = pd.read_excel(r'C:\Users\Mr Zhou\.openclaw\workspace\data\raw\原始数据.xlsx')

# Variable definitions (SOR model)
variables = {
    # S - Stimulus (External)
    '地理标志认证': list(df.columns[0:4]),
    '地理标志感知强度': list(df.columns[4:8]),
    # O - Organism (Psychological)
    '品牌认知度': list(df.columns[8:12]),
    '品牌信任度': list(df.columns[12:16]),
    '感知价值': list(df.columns[16:20]),
    # M - Moderator
    '产品涉入度': list(df.columns[20:24]),
    '电商平台信息可信度': list(df.columns[24:28]),
    '线上购买经验': list(df.columns[28:32]),
    # R - Response
    '购买意愿': list(df.columns[32:36])
}

# Calculate construct scores
construct_scores = {}
for name, cols in variables.items():
    construct_scores[name] = df[cols].mean(axis=1)
scores_df = pd.DataFrame(construct_scores)

print("=" * 70)
print("SOR Model Analysis")
print("=" * 70)

# Descriptive statistics
print("\n[Table 1] Descriptive Statistics")
print("-" * 70)
print(f"Sample Size: N = {len(df)}")
for col in scores_df.columns:
    print(f"  {col}: M={scores_df[col].mean():.3f}, SD={scores_df[col].std():.3f}")

# Correlation matrix
print("\n[Table 2] Correlation Matrix")
print("-" * 70)
corr_matrix = scores_df.corr()
print(corr_matrix.round(3).to_string())
corr_matrix.to_excel(r'C:\Users\Mr Zhou\.openclaw\workspace\data\output\相关系数矩阵.xlsx')
print("\n[OK] Correlation matrix saved")

# Reliability analysis
def cronbach_alpha(items):
    items = items.dropna()
    n_items = items.shape[1]
    if n_items < 2:
        return np.nan
    variances = items.var(ddof=1)
    total_variance = items.sum(axis=1).var(ddof=1)
    alpha = (n_items / (n_items - 1)) * (1 - variances.sum() / total_variance)
    return alpha

print("\n[Table 3] Reliability (Cronbach alpha)")
print("-" * 70)
for name, cols in variables.items():
    alpha = cronbach_alpha(df[cols])
    status = "Excellent" if alpha >= 0.8 else ("Good" if alpha >= 0.7 else "Acceptable")
    print(f"  {name}: alpha = {alpha:.4f} [{status}]")

# Path Analysis
print("\n" + "=" * 70)
print("Path Analysis (Regression)")
print("=" * 70)

X_S = scores_df[['地理标志认证', '地理标志感知强度']].values
y_O_cog = scores_df['品牌认知度'].values
y_O_trust = scores_df['品牌信任度'].values
y_O_value = scores_df['感知价值'].values
y_R = scores_df['购买意愿'].values

# S -> O paths
print("\n[Path 1] Stimulus -> Organism")
print("-" * 70)

model_cog = LinearRegression().fit(X_S, y_O_cog)
print(f"\nH1a: S -> Brand Cognition")
print(f"  R2 = {r2_score(y_O_cog, model_cog.predict(X_S)):.4f}")
print(f"  Geo Cert coef: {model_cog.coef_[0]:.4f}")
print(f"  Geo Intensity coef: {model_cog.coef_[1]:.4f}")

model_trust = LinearRegression().fit(X_S, y_O_trust)
print(f"\nH1b: S -> Brand Trust")
print(f"  R2 = {r2_score(y_O_trust, model_trust.predict(X_S)):.4f}")
print(f"  Geo Cert coef: {model_trust.coef_[0]:.4f}")
print(f"  Geo Intensity coef: {model_trust.coef_[1]:.4f}")

model_value = LinearRegression().fit(X_S, y_O_value)
print(f"\nH1c: S -> Perceived Value")
print(f"  R2 = {r2_score(y_O_value, model_value.predict(X_S)):.4f}")
print(f"  Geo Cert coef: {model_value.coef_[0]:.4f}")
print(f"  Geo Intensity coef: {model_value.coef_[1]:.4f}")

# O -> R path
print("\n[Path 2] Organism -> Response")
print("-" * 70)

X_O = scores_df[['品牌认知度', '品牌信任度', '感知价值']].values
model_OR = LinearRegression().fit(X_O, y_R)
print(f"\nH2: O -> Purchase Intention")
print(f"  R2 = {r2_score(y_R, model_OR.predict(X_O)):.4f}")
print(f"  Brand Cognition coef: {model_OR.coef_[0]:.4f}")
print(f"  Brand Trust coef: {model_OR.coef_[1]:.4f}")
print(f"  Perceived Value coef: {model_OR.coef_[2]:.4f}")

# S -> R direct
print("\n[Path 3] Stimulus -> Response (Direct)")
print("-" * 70)

model_SR = LinearRegression().fit(X_S, y_R)
print(f"\nH3: S -> Purchase Intention (Direct)")
print(f"  R2 = {r2_score(y_R, model_SR.predict(X_S)):.4f}")
print(f"  Geo Cert coef: {model_SR.coef_[0]:.4f}")
print(f"  Geo Intensity coef: {model_SR.coef_[1]:.4f}")

# Full model
print("\n[Path 4] Full Model (S + O -> R)")
print("-" * 70)

X_full = scores_df[['地理标志认证', '地理标志感知强度', '品牌认知度', '品牌信任度', '感知价值']].values
model_full = LinearRegression().fit(X_full, y_R)
print(f"\nFull Model R2 = {r2_score(y_R, model_full.predict(X_full)):.4f}")
for i, name in enumerate(['地理标志认证', '地理标志感知强度', '品牌认知度', '品牌信任度', '感知价值']):
    print(f"  {name} coef: {model_full.coef_[i]:.4f}")

# Mediation Analysis
print("\n" + "=" * 70)
print("Mediation Analysis")
print("=" * 70)

print("\n[Table 4] Mediation Effects")
print("-" * 70)

for mediator in ['品牌认知度', '品牌信任度', '感知价值']:
    # Step 1: S -> R (total effect c)
    model_c = LinearRegression().fit(X_S, y_R)
    c_total = model_c.coef_.sum()
    
    # Step 2: S -> M (path a)
    y_M = scores_df[mediator].values
    model_a = LinearRegression().fit(X_S, y_M)
    a_path = model_a.coef_.mean()
    
    # Step 3: S + M -> R (path b and c')
    X_sm = np.column_stack([X_S, y_M])
    model_b = LinearRegression().fit(X_sm, y_R)
    b_path = model_b.coef_[-1]
    c_prime = model_b.coef_[:-1].sum()
    
    indirect = a_path * b_path
    
    print(f"\nMediator: {mediator}")
    print(f"  Total effect (c): {c_total:.4f}")
    print(f"  Direct effect (c'): {c_prime:.4f}")
    print(f"  Indirect effect (a*b): {indirect:.4f}")
    if c_total != 0:
        print(f"  Mediation ratio: {indirect/c_total*100:.2f}%")

# Moderation Analysis
print("\n" + "=" * 70)
print("Moderation Analysis")
print("=" * 70)

print("\n[Table 5] Moderation Effects")
print("-" * 70)

scaler = StandardScaler()

for moderator in ['产品涉入度', '电商平台信息可信度', '线上购买经验']:
    X_S_mean = scores_df[['地理标志认证', '地理标志感知强度']].mean(axis=1).values.reshape(-1, 1)
    X_S_std = scaler.fit_transform(X_S_mean)
    M = scores_df[moderator].values.reshape(-1, 1)
    M_std = scaler.fit_transform(M)
    interaction = X_S_std * M_std
    
    X_mod = np.column_stack([X_S_std, M_std, interaction])
    model_mod = LinearRegression().fit(X_mod, y_R)
    
    r2_mod = r2_score(y_R, model_mod.predict(X_mod))
    interact_coef = model_mod.coef_[-1]
    
    residuals = y_R - model_mod.predict(X_mod)
    mse = np.sum(residuals**2) / (len(y_R) - X_mod.shape[1] - 1)
    se = np.sqrt(mse / len(y_R))
    t_value = interact_coef / se if se > 0 else 0
    p_value = 2 * (1 - stats.t.cdf(abs(t_value), len(y_R) - X_mod.shape[1] - 1))
    
    print(f"\nModerator: {moderator}")
    print(f"  Interaction coef: {interact_coef:.4f}")
    print(f"  t-value: {t_value:.3f}")
    print(f"  p-value: {p_value:.4f}")
    print(f"  Significant: {'Yes' if p_value < 0.05 else 'No'}")
    print(f"  Model R2: {r2_mod:.4f}")

# Save summary
results_summary = {
    'Construct': list(variables.keys()),
    'Items': [len(cols) for cols in variables.values()],
    'Cronbach_alpha': [cronbach_alpha(df[cols]) for cols in variables.values()]
}
results_summary_df = pd.DataFrame(results_summary)
results_summary_df.to_excel(r'C:\Users\Mr Zhou\.openclaw\workspace\data\output\模型分析结果汇总.xlsx', index=False)

print("\n" + "=" * 70)
print("Analysis Complete!")
print("=" * 70)
print("\n[OK] Results saved to: data/output/模型分析结果汇总.xlsx")
print("[OK] Correlation matrix saved to: data/output/相关系数矩阵.xlsx")
