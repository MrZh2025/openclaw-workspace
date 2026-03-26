"""
生成符合 AMOS 结构方程模型分析的模拟数据
模型结构：
- 自变量 (X) → X1, X2, X3 (3 题)
- 中介变量 (M) → M1, M2, M3, M4, M5 (5 题)
- 因变量 (Y) → Y1, Y2, Y3, Y4, Y5 (5 题)

路径关系：
- 自变量 → 中介变量
- 中介变量 → 因变量
- 自变量 → 因变量 (直接效应)
"""

import numpy as np
import pandas as pd
from numpy.random import multivariate_normal

# 设置随机种子以确保可重复性
np.random.seed(42)

# 样本量
n_samples = 100

# 量表等级
n_levels = 7

# 生成潜变量（标准化正态分布）
# 外生潜变量 - 自变量
X_latent = np.random.normal(0, 1, n_samples)  # 自变量

# 内生潜变量 - 中介变量和因变量
# 中介变量 = 0.6*自变量 + 误差
M_latent = (0.6 * X_latent + np.random.normal(0, np.sqrt(1-0.6**2), n_samples))

# 因变量 = 0.5*中介变量 + 0.3*自变量 + 误差
Y_latent = (0.5 * M_latent + 0.3 * X_latent + np.random.normal(0, np.sqrt(1-0.5**2-0.3**2), n_samples))

# 生成观测变量（使用因子载荷）
# 自变量 → X1, X2, X3 (因子载荷：0.75, 0.80, 0.78)
X1 = 0.75 * X_latent + np.random.normal(0, np.sqrt(1-0.75**2), n_samples)
X2 = 0.80 * X_latent + np.random.normal(0, np.sqrt(1-0.80**2), n_samples)
X3 = 0.78 * X_latent + np.random.normal(0, np.sqrt(1-0.78**2), n_samples)

# 中介变量 → M1, M2, M3, M4, M5 (因子载荷：0.70, 0.75, 0.80, 0.77, 0.82)
M1 = 0.70 * M_latent + np.random.normal(0, np.sqrt(1-0.70**2), n_samples)
M2 = 0.75 * M_latent + np.random.normal(0, np.sqrt(1-0.75**2), n_samples)
M3 = 0.80 * M_latent + np.random.normal(0, np.sqrt(1-0.80**2), n_samples)
M4 = 0.77 * M_latent + np.random.normal(0, np.sqrt(1-0.77**2), n_samples)
M5 = 0.82 * M_latent + np.random.normal(0, np.sqrt(1-0.82**2), n_samples)

# 因变量 → Y1, Y2, Y3, Y4, Y5 (因子载荷：0.72, 0.78, 0.80, 0.75, 0.76)
Y1 = 0.72 * Y_latent + np.random.normal(0, np.sqrt(1-0.72**2), n_samples)
Y2 = 0.78 * Y_latent + np.random.normal(0, np.sqrt(1-0.78**2), n_samples)
Y3 = 0.80 * Y_latent + np.random.normal(0, np.sqrt(1-0.80**2), n_samples)
Y4 = 0.75 * Y_latent + np.random.normal(0, np.sqrt(1-0.75**2), n_samples)
Y5 = 0.76 * Y_latent + np.random.normal(0, np.sqrt(1-0.76**2), n_samples)

# 将所有观测变量组合成 DataFrame
data = pd.DataFrame({
    'X1': X1, 'X2': X2, 'X3': X3,
    'M1': M1, 'M2': M2, 'M3': M3, 'M4': M4, 'M5': M5,
    'Y1': Y1, 'Y2': Y2, 'Y3': Y3, 'Y4': Y4, 'Y5': Y5
})

# 将数据转换为 7 级李克特量表 (1-7 分)
# 使用分位数方法确保均匀分布
def to_likert_scale(series, n_levels=7):
    """将连续变量转换为 1-7 的李克特量表"""
    # 使用分位数切割，确保每个等级大约有相同数量的样本
    quantiles = np.linspace(0, 1, n_levels + 1)
    cutoffs = series.quantile(quantiles)
    # 确保 cutoffs 是严格递增的
    cutoffs = cutoffs.drop_duplicates()
    
    # 如果分位数导致类别太少，使用等距分割
    if len(cutoffs) < n_levels + 1:
        min_val = series.min()
        max_val = series.max()
        step = (max_val - min_val) / n_levels
        cutoffs = pd.Series([min_val + i * step for i in range(n_levels + 1)])
        cutoffs.iloc[-1] = max_val + 0.001  # 确保最大值被包含
    
    labels = list(range(1, n_levels + 1))
    
    # 使用 pd.cut 进行分类
    try:
        likert = pd.cut(series, 
                       bins=[-np.inf] + list(cutoffs.iloc[1:-1]) + [np.inf], 
                       labels=labels, 
                       include_lowest=True)
    except:
        # 如果分位数方法失败，使用简单的线性转换
        likert = pd.cut(series, bins=n_levels, labels=labels)
    
    return likert.astype(int)

# 应用李克特转换
for col in data.columns:
    data[col] = to_likert_scale(data[col], n_levels)

# 验证数据分布
print("=" * 60)
print("SEM 模拟数据生成完成")
print("=" * 60)
print(f"\n样本量：{n_samples}")
print(f"量表等级：{n_levels} 级 (1-{n_levels}分)")
print(f"\n变量分布:")
for col in data.columns:
    print(f"\n{col}:")
    print(data[col].value_counts().sort_index())

# 计算相关系数矩阵（用于验证 SEM 假设）
print("\n" + "=" * 60)
print("相关系数矩阵:")
print("=" * 60)
corr_matrix = data.corr()
print(corr_matrix.round(3))

# 保存为 Excel 文件 (.xlsx)
output_path_xlsx = r'C:\Users\Mr Zhou\.openclaw\workspace\sem_data_X3M5Y5_100samples.xlsx'
data.to_excel(output_path_xlsx, index=False, sheet_name='SEM_Data')
print(f"\n[OK] 数据已保存至：{output_path_xlsx}")
print(f"[OK] 共 {len(data.columns)} 个变量 (X1-X3, M1-M5, Y1-Y5)")
print(f"[OK] 共 {len(data)} 条记录")
print(f"[OK] 格式：.xlsx (Excel)")
