# -*- coding: utf-8 -*-
"""
使用 matplotlib 绘制 AMOS 风格 SEM 结构方程模型路径图
AMOS 软件风格：潜变量在中间，观测变量在周围，误差项在旁边
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Rectangle, Circle, FancyArrowPatch
from matplotlib.font_manager import FontProperties

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'STHeiti']
plt.rcParams['axes.unicode_minus'] = False

# 创建图形
fig, ax = plt.subplots(figsize=(22, 14), dpi=150)
ax.set_xlim(-3, 25)
ax.set_ylim(-5, 16)
ax.axis('off')

# ============ 定义潜变量位置 (x, y) - AMOS 风格：水平排列在中间 ============
latent_positions = {
    '综合感知': (3, 8),
    '支持态度': (9, 8),
    '购买意愿': (15, 8),
    '推广容易度': (21, 8)
}

# 因子载荷（标准化系数）
factor_loadings = {
    'A1': 0.726, 'A2': 0.781, 'A3': 0.786, 'A4': 0.820,
    'A5': 0.690, 'A6': 0.793, 'A7': 0.761, 'A8': 0.810,
    'B1': 0.706, 'B2': 0.787, 'B3': 0.772, 'B4': 0.683,
    'C1': 0.764, 'C2': 0.774, 'C3': 0.787, 'C4': 0.636,
    'D1': 0.788, 'D2': 0.816, 'D3': 0.806, 'D4': 0.800
}

# 路径系数（结构模型）
path_coefficients = {
    ('综合感知', '支持态度'): 0.422,
    ('支持态度', '购买意愿'): 0.402,
    ('购买意愿', '推广容易度'): 0.446
}

# 潜变量到观测变量的映射
latent_to_obs = {
    '综合感知': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'],
    '支持态度': ['B1', 'B2', 'B3', 'B4'],
    '购买意愿': ['C1', 'C2', 'C3', 'C4'],
    '推广容易度': ['D1', 'D2', 'D3', 'D4']
}

# ============ 观测变量位置 - AMOS 风格：潜变量上方和下方排列 ============
observed_positions = {}
error_positions = {}

# 综合感知的观测变量 (A1-A8) - 上 4 个，下 4 个
lv_x, lv_y = latent_positions['综合感知']
for i in range(4):
    observed_positions[f'A{i+1}'] = (lv_x - 2 + i * 1.3, lv_y + 3.5)  # 上方
for i in range(4, 8):
    observed_positions[f'A{i+1}'] = (lv_x - 2 + (i-4) * 1.3, lv_y - 3.5)  # 下方

# 支持态度的观测变量 (B1-B4) - 上 2 个，下 2 个
lv_x, lv_y = latent_positions['支持态度']
for i in range(2):
    observed_positions[f'B{i+1}'] = (lv_x - 1 + i * 2.0, lv_y + 3.5)  # 上方
for i in range(2, 4):
    observed_positions[f'B{i+1}'] = (lv_x - 1 + (i-2) * 2.0, lv_y - 3.5)  # 下方

# 购买意愿的观测变量 (C1-C4) - 上 2 个，下 2 个
lv_x, lv_y = latent_positions['购买意愿']
for i in range(2):
    observed_positions[f'C{i+1}'] = (lv_x - 1 + i * 2.0, lv_y + 3.5)  # 上方
for i in range(2, 4):
    observed_positions[f'C{i+1}'] = (lv_x - 1 + (i-2) * 2.0, lv_y - 3.5)  # 下方

# 推广容易度的观测变量 (D1-D4) - 上 2 个，下 2 个
lv_x, lv_y = latent_positions['推广容易度']
for i in range(2):
    observed_positions[f'D{i+1}'] = (lv_x - 1 + i * 2.0, lv_y + 3.5)  # 上方
for i in range(2, 4):
    observed_positions[f'D{i+1}'] = (lv_x - 1 + (i-2) * 2.0, lv_y - 3.5)  # 下方

# 误差项位置 - AMOS 风格：在观测变量外侧
for obs, (ox, oy) in observed_positions.items():
    if oy > 8:  # 上方的观测变量，误差在上方
        error_positions[f'e_{obs}'] = (ox, oy + 1.2)
    else:  # 下方的观测变量，误差在下方
        error_positions[f'e_{obs}'] = (ox, oy - 1.2)

# ============ 第一步：绘制所有箭头（最底层）============

# 1. 结构路径（潜变量之间）- 红色粗箭头
for (from_lv, to_lv), coef in path_coefficients.items():
    x1, y1 = latent_positions[from_lv]
    x2, y2 = latent_positions[to_lv]
    
    # 绘制直线箭头
    arrow = FancyArrowPatch((x1+0.8, y1), (x2-0.8, y2),
                            color='#DC143C', lw=3.5, arrowstyle='->',
                            mutation_scale=25, zorder=1)
    ax.add_patch(arrow)
    
    # 路径系数标签 - 放在箭头上方，白色背景
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    ax.text(mid_x, mid_y + 0.5, f'{coef:.3f}', ha='center', va='bottom',
            fontsize=13, fontweight='bold', color='#DC143C',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', ec='#DC143C', lw=1.5))

# 2. 因子载荷路径（潜变量到观测变量）- 蓝色箭头
for lv_name, obs_list in latent_to_obs.items():
    lx, ly = latent_positions[lv_name]
    for obs in obs_list:
        ox, oy = observed_positions[obs]
        loading = factor_loadings[obs]
        
        # 确定箭头起点（从椭圆边缘出发）
        if oy > ly:  # 观测变量在上方
            start_y = ly + 0.6
        else:  # 观测变量在下方
            start_y = ly - 0.6
        
        arrow = FancyArrowPatch((lx, start_y), (ox, oy),
                                color='#4169E1', lw=1.5, arrowstyle='->',
                                mutation_scale=15, alpha=0.8, zorder=2)
        ax.add_patch(arrow)
        
        # 因子载荷标签 - 放在箭头中间，白色背景
        mid_x = (lx + ox) / 2
        mid_y = (ly + oy) / 2
        ax.text(mid_x + 0.2, mid_y, f'{loading:.2f}', ha='left', va='center',
                fontsize=10, color='#4169E1', style='italic',
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white', ec='#4169E1', lw=0.8, alpha=0.9))

# 3. 误差路径（误差项到观测变量）- 灰色虚线箭头
for obs, (ox, oy) in observed_positions.items():
    ex, ey = error_positions[f'e_{obs}']
    arrow = FancyArrowPatch((ex, ey), (ox, oy),
                            color='gray', lw=1.2, arrowstyle='->',
                            mutation_scale=12, linestyle='--', zorder=2)
    ax.add_patch(arrow)

# ============ 第二步：绘制所有节点（在箭头之上）============

# 1. 潜变量（椭圆）- AMOS 风格
for name, (x, y) in latent_positions.items():
    ellipse = Ellipse((x, y), width=2.2, height=1.4,
                      color='#E6F3FF', ec='#00008B', lw=3, zorder=10)
    ax.add_patch(ellipse)
    ax.text(x, y, name, ha='center', va='center', fontsize=13, fontweight='bold',
            color='#00008B', zorder=11)

# 2. 观测变量（矩形）- AMOS 风格
for name, (x, y) in observed_positions.items():
    rect = Rectangle((x-0.55, y-0.35), 1.1, 0.7,
                     color='#E8F5E9', ec='#2E7D32', lw=2, zorder=10)
    ax.add_patch(rect)
    ax.text(x, y, name, ha='center', va='center', fontsize=11, fontweight='bold',
            color='#2E7D32', zorder=11)

# 3. 误差项（小圆）- AMOS 风格
for name, (x, y) in error_positions.items():
    circle = Circle((x, y), 0.22, color='#FFF9C4', ec='#F57F17', lw=2, zorder=10)
    ax.add_patch(circle)

# ============ 添加 AMOS 风格图例（底部）============
legend_y = -3.5
ax.text(1, legend_y + 1.2, '图例', fontsize=15, fontweight='bold')

# 潜变量
ellipse = Ellipse((2.5, legend_y + 0.7), width=0.8, height=0.5, color='#E6F3FF', ec='#00008B', lw=3)
ax.add_patch(ellipse)
ax.text(4, legend_y + 0.7, '潜变量（椭圆）', fontsize=12, va='center')

# 观测变量
rect = Rectangle((6, legend_y + 0.45), 0.7, 0.5, color='#E8F5E9', ec='#2E7D32', lw=2)
ax.add_patch(rect)
ax.text(7.3, legend_y + 0.7, '观测变量（矩形）', fontsize=12, va='center')

# 误差项
circle = Circle((10, legend_y + 0.7), 0.2, color='#FFF9C4', ec='#F57F17', lw=2)
ax.add_patch(circle)
ax.text(10.8, legend_y + 0.7, '误差项（圆）', fontsize=12, va='center')

# 结构路径
arrow = FancyArrowPatch((13, legend_y + 0.7), (14.5, legend_y + 0.7),
                        color='#DC143C', lw=3.5, arrowstyle='->', mutation_scale=25)
ax.add_patch(arrow)
ax.text(15, legend_y + 0.7, '结构路径（β系数）', fontsize=12, va='center', color='#DC143C')

# 因子载荷
arrow = FancyArrowPatch((17.5, legend_y + 0.7), (19, legend_y + 0.7),
                        color='#4169E1', lw=1.5, arrowstyle='->', mutation_scale=15)
ax.add_patch(arrow)
ax.text(19.5, legend_y + 0.7, '因子载荷', fontsize=12, va='center', color='#4169E1')

# 误差路径
arrow = FancyArrowPatch((21.5, legend_y + 0.7), (23, legend_y + 0.7),
                        color='gray', lw=1.2, arrowstyle='->', linestyle='--')
ax.add_patch(arrow)
ax.text(23.5, legend_y + 0.7, '误差路径', fontsize=12, va='center', color='gray')

# ============ 保存 ============
plt.tight_layout()
plt.savefig('C:/Users/Mr Zhou/Desktop/飞书智能化报告/SEM 路径图_AMOS 风格.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("SEM 路径图已保存：C:/Users/Mr Zhou/Desktop/飞书智能化报告/SEM 路径图_AMOS 风格.png")
print("图片尺寸：22x14 英寸，150 DPI")
print("风格：AMOS 软件风格（潜变量居中，观测变量上下排列）")
