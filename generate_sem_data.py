"""
生成符合 AMOS 结构方程模型分析的模拟数据
模型结构：
- 照护压力 → Q1, Q2, Q3, Q4
- 安全保障 → Q5, Q6, Q7
- 风险担忧 → Q8, Q9, Q10, Q11
- 家庭养老焦虑 (中介变量，无观测题项)
- 黄金避险行为 (因变量，无观测题项)
- 避险意愿 → Q20, Q21, Q22
- 配置认知 → Q23, Q24, Q25

路径关系：
- 照护压力 → 家庭养老焦虑
- 安全保障 → 家庭养老焦虑
- 风险担忧 → 家庭养老焦虑
- 家庭养老焦虑 → 黄金避险行为
- 避险意愿 → 黄金避险行为
- 配置认知 → 黄金避险行为
"""

import numpy as np
import pandas as pd
from numpy.random import multivariate_normal

# 设置随机种子以确保可重复性
np.random.seed(42)

# 样本量
n_samples = 250

# 生成潜变量（标准化正态分布）
# 外生潜变量
care_stress = np.random.normal(0, 1, n_samples)      # 照护压力
security_safety = np.random.normal(0, 1, n_samples)   # 安全保障
risk_worry = np.random.normal(0, 1, n_samples)        # 风险担忧
avoidance_willingness = np.random.normal(0, 1, n_samples)  # 避险意愿
allocation_cognition = np.random.normal(0, 1, n_samples)   # 配置认知

# 内生潜变量（中介和因变量）
# 家庭养老焦虑 = 0.4*照护压力 + 0.3*安全保障 + 0.5*风险担忧 + 误差
family_anxiety = (0.4 * care_stress + 
                  0.3 * security_safety + 
                  0.5 * risk_worry + 
                  np.random.normal(0, 0.5, n_samples))

# 黄金避险行为 = 0.5*家庭养老焦虑 + 0.4*避险意愿 + 0.3*配置认知 + 误差
gold_avoidance = (0.5 * family_anxiety + 
                  0.4 * avoidance_willingness + 
                  0.3 * allocation_cognition + 
                  np.random.normal(0, 0.5, n_samples))

# 生成观测变量（使用因子载荷）
# 照护压力 → Q1, Q2, Q3, Q4 (因子载荷：0.7, 0.75, 0.8, 0.72)
Q1 = 0.7 * care_stress + np.random.normal(0, np.sqrt(1-0.7**2), n_samples)
Q2 = 0.75 * care_stress + np.random.normal(0, np.sqrt(1-0.75**2), n_samples)
Q3 = 0.8 * care_stress + np.random.normal(0, np.sqrt(1-0.8**2), n_samples)
Q4 = 0.72 * care_stress + np.random.normal(0, np.sqrt(1-0.72**2), n_samples)

# 安全保障 → Q5, Q6, Q7 (因子载荷：0.75, 0.8, 0.78)
Q5 = 0.75 * security_safety + np.random.normal(0, np.sqrt(1-0.75**2), n_samples)
Q6 = 0.8 * security_safety + np.random.normal(0, np.sqrt(1-0.8**2), n_samples)
Q7 = 0.78 * security_safety + np.random.normal(0, np.sqrt(1-0.78**2), n_samples)

# 风险担忧 → Q8, Q9, Q10, Q11 (因子载荷：0.7, 0.75, 0.8, 0.73)
Q8 = 0.7 * risk_worry + np.random.normal(0, np.sqrt(1-0.7**2), n_samples)
Q9 = 0.75 * risk_worry + np.random.normal(0, np.sqrt(1-0.75**2), n_samples)
Q10 = 0.8 * risk_worry + np.random.normal(0, np.sqrt(1-0.8**2), n_samples)
Q11 = 0.73 * risk_worry + np.random.normal(0, np.sqrt(1-0.73**2), n_samples)

# 避险意愿 → Q20, Q21, Q22 (因子载荷：0.75, 0.8, 0.77)
Q20 = 0.75 * avoidance_willingness + np.random.normal(0, np.sqrt(1-0.75**2), n_samples)
Q21 = 0.8 * avoidance_willingness + np.random.normal(0, np.sqrt(1-0.8**2), n_samples)
Q22 = 0.77 * avoidance_willingness + np.random.normal(0, np.sqrt(1-0.77**2), n_samples)

# 配置认知 → Q23, Q24, Q25 (因子载荷：0.78, 0.82, 0.75)
Q23 = 0.78 * allocation_cognition + np.random.normal(0, np.sqrt(1-0.78**2), n_samples)
Q24 = 0.82 * allocation_cognition + np.random.normal(0, np.sqrt(1-0.82**2), n_samples)
Q25 = 0.75 * allocation_cognition + np.random.normal(0, np.sqrt(1-0.75**2), n_samples)

# 将所有观测变量组合成 DataFrame
data = pd.DataFrame({
    'Q1': Q1, 'Q2': Q2, 'Q3': Q3, 'Q4': Q4,
    'Q5': Q5, 'Q6': Q6, 'Q7': Q7,
    'Q8': Q8, 'Q9': Q9, 'Q10': Q10, 'Q11': Q11,
    'Q20': Q20, 'Q21': Q21, 'Q22': Q22,
    'Q23': Q23, 'Q24': Q24, 'Q25': Q25
})

# 将数据转换为五级李克特量表 (1-5 分)
# 使用分位数方法确保均匀分布
def to_likert_scale(series):
    """将连续变量转换为 1-5 的李克特量表"""
    # 使用分位数切割，确保每个等级大约有相同数量的样本
    quantiles = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    cutoffs = series.quantile(quantiles)
    # 确保 cutoffs 是严格递增的
    cutoffs = cutoffs.drop_duplicates()
    
    # 如果分位数导致类别太少，使用等距分割
    if len(cutoffs) < 6:
        min_val = series.min()
        max_val = series.max()
        cutoffs = pd.Series([min_val, 
                            min_val + 0.4*(max_val-min_val),
                            min_val + 0.6*(max_val-min_val),
                            min_val + 0.8*(max_val-min_val),
                            max_val])
    
    labels = [1, 2, 3, 4, 5]
    
    # 使用 pd.cut 进行分类
    try:
        likert = pd.cut(series, 
                       bins=[-np.inf] + list(cutoffs.iloc[1:-1]) + [np.inf], 
                       labels=labels, 
                       include_lowest=True)
    except:
        # 如果分位数方法失败，使用简单的线性转换
        likert = pd.cut(series, bins=5, labels=labels)
    
    return likert.astype(int)

# 应用李克特转换
for col in data.columns:
    data[col] = to_likert_scale(data[col])

# 验证数据分布
print("=" * 60)
print("SEM 模拟数据生成完成")
print("=" * 60)
print(f"\n样本量：{n_samples}")
print(f"\n变量分布:")
for col in data.columns:
    print(f"\n{col}:")
    print(data[col].value_counts().sort_index())

# 计算相关系数矩阵（用于验证 SEM 假设）
print("\n" + "=" * 60)
print("相关系数矩阵（部分）:")
print("=" * 60)
corr_matrix = data.corr()
print(corr_matrix.round(3))

# 保存为 CSV 文件
output_path = r'C:\Users\Mr Zhou\.openclaw\workspace\sem_simulation_data.csv'
data.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"\n[OK] 数据已保存至：{output_path}")
print(f"[OK] 共 {len(data.columns)} 个变量 (Q1-Q25)")
print(f"[OK] 共 {len(data)} 条记录")
