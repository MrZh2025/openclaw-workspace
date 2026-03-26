# -*- coding: utf-8 -*-
"""
使用 matplotlib 绘制专业 SEM 结构方程模型路径图 - 无遮挡版
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Rectangle, Circle, FancyArrowPatch
from matplotlib.font_manager import FontProperties

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'STHeiti']
plt.rcParams['axes.unicode_minus'] = False

# 创建图形
fig, ax = plt.subplots(figsize=(20, 12), dpi=150)
ax.set_xlim(-2, 22)
ax.set_ylim(-2, 14)
ax.axis('off')
ax.set_title('结构方程模型 (SEM) 路径图', fontsize=18, fontweight='bold', pad=30, y=0.95)

# 定义潜变量位置 (x, y) - 水平排列在中间
latent_positions = {
    '综合感知': (2, 7),
    '支持态度': (8, 7),
    '购买意愿': (14, 7),
    '推广容易度': (20, 7)
}

# 因子载荷
factor_loadings = {
    'A1': 0.726, 'A2': 0.781, 'A3': 0.786, 'A4': 0.820,
    'A5': 0.690, 'A6': 0.793, 'A7': 0.761, 'A8': 0.810,
    'B1': 0.706, 'B2': 0.787, 'B3': 0.772, 'B4': 0.683,
    'C1': 0.764, 'C2': 0.774, 'C3': 0.787, 'C4': 0.636,
    'D1': 0.788, 'D2': 0.816, 'D3': 0.806, 'D4': 0.800
}

# 路径系数
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

# 观测变量位置 - 垂直排列在潜变量下方，分两排
observed_positions = {}
error_positions = {}

# 综合感知的观测变量 (A1-A8) - 分两排，每排 4 个
lv_x, lv_y = latent_positions['综合感知']
for i in range(4):
    observed_positions[f'A{i+1}'] = (lv_x - 1.5 + i * 1.0, lv_y - 2.5)
for i in range(4, 8):
    observed_positions[f'A{i+1}'] = (lv_x - 1.5 + (i-4) * 1.0, lv_y - 4.0)

# 支持态度的观测变量 (B1-B4) - 单排
lv_x, lv_y = latent_positions['支持态度']
for i in range(4):
    observed_positions[f'B{i+1}'] = (lv_x - 1.5 + i * 1.0, lv_y - 2.5)

# 购买意愿的观测变量 (C1-C4) - 单排
lv_x, lv_y = latent_positions['购买意愿']
for i in range(4):
    observed_positions[f'C{i+1}'] = (lv_x - 1.5 + i * 1.0, lv_y - 2.5)

# 推广容易度的观测变量 (D1-D4) - 单排
lv_x, lv_y = latent_positions['推广容易度']
for i in range(4):
    observed_positions[f'D{i+1}'] = (lv_x - 1.5 + i * 1.0, lv_y - 2.5)

# 误差项位置 - 在观测变量右侧
for obs, (ox, oy) in observed_positions.items():
    error_positions[f'e_{obs}'] = (ox + 0.9, oy)

# ============ 绘制潜变量之间的路径（结构模型）- 最先绘制，在最底层 ============
for (from_lv, to_lv), coef in path_coefficients.items():
    x1, y1 = latent_positions[from_lv]
    x2, y2 = latent_positions[to_lv]
    
    # 绘制弧形箭头（避免与潜变量重叠）
    mid_x = (x1 + x2) / 2
    mid_y = y1 + 0.8  # 向上拱起
    
    # 使用曲线箭头
    arrow = FancyArrowPatch((x1+0.7, y1), (x2-0.7, y2),
                            connectionstyle=f"arc3,rad=-{0.3}",
                            color='red', lw=3, arrowstyle='->', 
                            mutation_scale=20, zorder=5)
    ax.add_patch(arrow)
    
    # 路径系数标签 - 放在箭头上方
    ax.text(mid_x, mid_y + 0.3, f'β={coef:.3f}', ha='center', va='bottom', 
            fontsize=12, fontweight='bold', color='red',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', ec='red', lw=1))

# ============ 绘制潜变量到观测变量的路径（测量模型）============
for lv_name, obs_list in latent_to_obs.items():
    lx, ly = latent_positions[lv_name]
    for obs in obs_list:
        ox, oy = observed_positions[obs]
        loading = factor_loadings[obs]
        
        # 绘制箭头（从潜变量到观测变量）
        arrow = FancyArrowPatch((lx, ly-0.7), (ox, oy+0.35),
                                color='blue', lw=1.5, arrowstyle='->',
                                mutation_scale=15, alpha=0.7, zorder=4)
        ax.add_patch(arrow)
        
        # 因子载荷标签 - 放在箭头中间偏右
        mid_x = (lx + ox) / 2 + 0.3
        mid_y = (ly + oy) / 2 - 0.2
        ax.text(mid_x, mid_y, f'{loading:.2f}', ha='left', va='center',
                fontsize=9, color='blue', style='italic',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', ec='none', alpha=0.8))

# ============ 绘制误差项到观测变量的路径 ============
for obs, (ox, oy) in observed_positions.items():
    ex, ey = error_positions[f'e_{obs}']
    # 虚线箭头
    arrow = FancyArrowPatch((ex-0.2, ey), (ox+0.5, oy),
                            color='gray', lw=1, arrowstyle='->',
                            linestyle='--', mutation_scale=10, zorder=3)
    ax.add_patch(arrow)

# ============ 绘制潜变量（椭圆）- 在路径之上 ============
for name, (x, y) in latent_positions.items():
    ellipse = Ellipse((x, y), width=1.8, height=1.2, 
                      color='lightblue', ec='darkblue', lw=2.5, zorder=10)
    ax.add_patch(ellipse)
    ax.text(x, y, name, ha='center', va='center', fontsize=12, fontweight='bold', 
            color='darkblue', zorder=11)

# ============ 绘制观测变量（矩形）- 在路径之上 ============
for name, (x, y) in observed_positions.items():
    rect = Rectangle((x-0.45, y-0.3), 0.9, 0.6, 
                     color='lightgreen', ec='darkgreen', lw=1.5, zorder=10)
    ax.add_patch(rect)
    ax.text(x, y, name, ha='center', va='center', fontsize=10, fontweight='bold', 
            color='darkgreen', zorder=11)

# ============ 绘制误差项（小圆）- 在路径之上 ============
for name, (x, y) in error_positions.items():
    circle = Circle((x, y), 0.18, color='lightyellow', ec='orange', lw=1.5, zorder=10)
    ax.add_patch(circle)

# ============ 添加图例 ============
legend_y = 1.2
ax.text(1, legend_y + 0.9, '图例', fontsize=14, fontweight='bold')

# 潜变量
ellipse = Ellipse((2, legend_y + 0.65), width=0.6, height=0.4, color='lightblue', ec='darkblue', lw=2)
ax.add_patch(ellipse)
ax.text(3, legend_y + 0.65, '潜变量', fontsize=11, va='center')

# 观测变量
rect = Rectangle((4.5, legend_y + 0.5), 0.5, 0.3, color='lightgreen', ec='darkgreen', lw=1.5)
ax.add_patch(rect)
ax.text(5.5, legend_y + 0.65, '观测变量', fontsize=11, va='center')

# 误差项
circle = Circle((7, legend_y + 0.65), 0.15, color='lightyellow', ec='orange', lw=1.5)
ax.add_patch(circle)
ax.text(7.6, legend_y + 0.65, '误差项', fontsize=11, va='center')

# 结构路径
arrow = FancyArrowPatch((9, legend_y + 0.65), (10, legend_y + 0.65),
                        color='red', lw=3, arrowstyle='->', mutation_scale=20)
ax.add_patch(arrow)
ax.text(10.5, legend_y + 0.65, '结构路径 (β系数)', fontsize=11, va='center', color='red')

# 因子载荷
arrow = FancyArrowPatch((12.5, legend_y + 0.65), (13.5, legend_y + 0.65),
                        color='blue', lw=1.5, arrowstyle='->', mutation_scale=15, alpha=0.7)
ax.add_patch(arrow)
ax.text(14, legend_y + 0.65, '因子载荷', fontsize=11, va='center', color='blue')

# 误差路径
arrow = FancyArrowPatch((15.5, legend_y + 0.65), (16.5, legend_y + 0.65),
                        color='gray', lw=1, arrowstyle='->', linestyle='--')
ax.add_patch(arrow)
ax.text(17, legend_y + 0.65, '误差路径', fontsize=11, va='center', color='gray')

# ============ 保存 ============
plt.tight_layout()
plt.savefig('C:/Users/Mr Zhou/Desktop/飞书智能化报告/SEM 路径图_专业版.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("SEM 路径图已保存：C:/Users/Mr Zhou/Desktop/飞书智能化报告/SEM 路径图_专业版.png")
print("图片尺寸：20x12 英寸，150 DPI")
print("特点：无遮挡、分层绘制、专业配色")
