# -*- coding: utf-8 -*-
"""
数据分析脚本 - 信度分析 + 效度分析
"""
import pandas as pd
import numpy as np
from scipy import stats
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_kmo, calculate_bartlett_sphericity
import warnings
warnings.filterwarnings('ignore')

# 读取数据
df = pd.read_excel(r'C:\Users\Mr Zhou\.openclaw\workspace\data\raw\原始数据.xlsx')

# 定义各维度的列
dimensions = {
    '地理标志认证': list(df.columns[0:4]),
    '地理标志认知': list(df.columns[4:8]),
    '品牌熟悉度': list(df.columns[8:12]),
    '品牌信任度': list(df.columns[12:16]),
    '感知价值': list(df.columns[16:20]),
    '产品涉入度': list(df.columns[20:24]),
    '平台信息信任': list(df.columns[24:28]),
    '线上购买经验': list(df.columns[28:32]),
    '购买意愿': list(df.columns[32:36])
}

# ========== 信度分析 (Cronbach's α) ==========
def cronbach_alpha(items):
    """计算 Cronbach's α系数"""
    items = items.dropna()
    n_items = items.shape[1]
    if n_items < 2:
        return np.nan
    variances = items.var(ddof=1)
    total_variance = items.sum(axis=1).var(ddof=1)
    alpha = (n_items / (n_items - 1)) * (1 - variances.sum() / total_variance)
    return alpha

print("=" * 60)
print("信度分析结果 (Cronbach's α)")
print("=" * 60)

reliability_results = {}
for dim_name, cols in dimensions.items():
    alpha = cronbach_alpha(df[cols])
    reliability_results[dim_name] = alpha
    status = "[优秀]" if alpha >= 0.8 else ("[良好]" if alpha >= 0.7 else ("[可接受]" if alpha >= 0.6 else "[需改进]"))
    print(f"{dim_name}: α = {alpha:.4f} {status}")

# 总体信度
overall_alpha = cronbach_alpha(df)
print(f"\n总体信度: α = {overall_alpha:.4f}")

# ========== 效度分析 ==========
print("\n" + "=" * 60)
print("效度分析结果")
print("=" * 60)

# KMO 和 Bartlett 检验
kmo_all, kmo_model = calculate_kmo(df)
chi_square_value, p_value = calculate_bartlett_sphericity(df)

print(f"\nKMO 值：{kmo_model:.4f}")
kmo_status = "[非常适合]" if kmo_model >= 0.8 else ("[适合]" if kmo_model >= 0.7 else ("[一般]" if kmo_model >= 0.6 else "[不适合]"))
print(f"KMO 评价：{kmo_status}")

print(f"\nBartlett 球形检验:")
print(f"  卡方值：{chi_square_value:.2f}")
print(f"  p 值：{p_value:.6f}")
print(f"  结果：{'[显著，适合因子分析]' if p_value < 0.05 else '[不显著，不适合因子分析]'}")

# 探索性因子分析 (EFA)
print("\n" + "=" * 60)
print("探索性因子分析 (EFA)")
print("=" * 60)

fa = FactorAnalyzer(n_factors=9, rotation='varimax')
fa.fit(df)

# 因子载荷矩阵
loadings = pd.DataFrame(fa.loadings_, columns=[f'因子{i+1}' for i in range(9)], index=df.columns)

# 计算各维度的 AVE 和 CR
print("\n各维度 AVE(平均方差抽取量) 和 CR(组合信度):")
print("-" * 60)

validity_results = {}
for dim_name, cols in dimensions.items():
    dim_loadings = loadings.loc[cols]
    # 取每个题目在对应因子上的最大载荷
    max_loadings = dim_loadings.abs().max(axis=1)
    
    # AVE = (Σ载荷²) / n
    ave = (max_loadings ** 2).mean()
    
    # CR = (Σ载荷)² / [(Σ载荷)² + Σ(1-载荷²)]
    sum_loading = max_loadings.sum()
    sum_error = (1 - max_loadings ** 2).sum()
    cr = (sum_loading ** 2) / (sum_loading ** 2 + sum_error)
    
    validity_results[dim_name] = {'AVE': ave, 'CR': cr}
    ave_status = "[OK]" if ave >= 0.5 else "[?]"
    cr_status = "[OK]" if cr >= 0.7 else "[?]"
    print(f"{dim_name}: AVE = {ave:.4f} {ave_status}, CR = {cr:.4f} {cr_status}")

# 保存结果到文件
results_df = pd.DataFrame({
    '维度': list(dimensions.keys()),
    'Cronbach_α': [reliability_results[d] for d in dimensions.keys()],
    'AVE': [validity_results[d]['AVE'] for d in dimensions.keys()],
    'CR': [validity_results[d]['CR'] for d in dimensions.keys()]
})

results_df.to_excel(r'C:\Users\Mr Zhou\.openclaw\workspace\data\output\信度效度分析结果.xlsx', index=False)
print("\n[OK] 分析结果已保存至：data/output/信度效度分析结果.xlsx")

# 保存因子载荷矩阵
loadings.to_excel(r'C:\Users\Mr Zhou\.openclaw\workspace\data\output\因子载荷矩阵.xlsx')
print("[OK] 因子载荷矩阵已保存至：data/output/因子载荷矩阵.xlsx")

print("\n" + "=" * 60)
print("分析完成！")
print("=" * 60)
