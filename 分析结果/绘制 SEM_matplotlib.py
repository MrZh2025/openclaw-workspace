# -*- coding: utf-8 -*-
"""
使用 matplotlib 和 networkx 绘制 SEM 结构方程模型路径图
"""
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建图形
fig, ax = plt.subplots(figsize=(16, 10), dpi=150)
ax.set_xlim(0, 20)
ax.set_ylim(0, 14)
ax.axis('off')
ax.set_title('结构方程模型 (SEM) 路径图', fontsize=16, fontweight='bold', pad=20)

# 定义潜变量位置 (x, y)
latent_positions = {
    '综合感知': (3, 7),
    '支持态度': (8, 9),
    '购买意愿': (13, 9),
    '推广容易度': (18, 7)
}

# 定义观测变量位置
observed_positions = {}
# 综合感知的观测变量 (A1-A8)
for i in range(8):
    angle = np.pi * 0.8 + i * 0.15
    x = 3 + 2.5 * np.cos(angle)
    y = 7 + 2.5 * np.sin(angle)
    observed_positions[f'A{i+1}'] = (x, y)

# 支持态度的观测变量 (B1-B4)
for i in range(4):
    angle = np.pi * 0.3 + i * 0.4
    x = 8 + 2.0 * np.cos(angle)
    y = 9 + 2.0 * np.sin(angle)
    observed_positions[f'B{i+1}'] = (x, y)

# 购买意愿的观测变量 (C1-C4)
for i in range(4):
    angle = np.pi * 0.3 + i * 0.4
    x = 13 + 2.0 * np.cos(angle)
    y = 9 + 2.0 * np.sin(angle)
    observed_positions[f'C{i+1}'] = (x, y)

# 推广容易度的观测变量 (D1-D4)
for i in range(4):
    angle = np.pi * 1.2 + i * 0.4
    x = 18 + 2.0 * np.cos(angle)
    y = 7 + 2.0 * np.sin(angle)
    observed_positions[f'D{i+1}'] = (x, y)

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

# 绘制潜变量（椭圆）
for name, (x, y) in latent_positions.items():
    circle = plt.Circle((x, y), 0.9, color='lightblue', ec='darkblue', lw=2, zorder=10)
    ax.add_patch(circle)
    ax.text(x, y, name, ha='center', va='center', fontsize=11, fontweight='bold', color='darkblue', zorder=11)

# 绘制观测变量（矩形）和误差项
for name, (x, y) in observed_positions.items():
    # 矩形节点
    rect = plt.Rectangle((x-0.5, y-0.35), 1.0, 0.7, color='lightgreen', ec='darkgreen', lw=1.5, zorder=10)
    ax.add_patch(rect)
    ax.text(x, y, name, ha='center', va='center', fontsize=10, fontweight='bold', color='darkgreen', zorder=11)
    
    # 误差项（小圆）
    ex = x + 0.7
    ey = y - 0.5
    error_circle = plt.Circle((ex, ey), 0.2, color='lightyellow', ec='orange', lw=1, zorder=10)
    ax.add_patch(error_circle)
    
    # 误差到观测变量的虚线
    ax.annotate('', xy=(x, y-0.35), xytext=(ex, ey+0.2),
                arrowprops=dict(arrowstyle='->', color='gray', linestyle='--', lw=1))

# 绘制潜变量之间的路径（结构模型）
for (from_lv, to_lv), coef in path_coefficients.items():
    x1, y1 = latent_positions[from_lv]
    x2, y2 = latent_positions[to_lv]
    
    # 计算方向
    dx = x2 - x1
    dy = y2 - y1
    dist = np.sqrt(dx**2 + dy**2)
    
    # 起点和终点（在圆的边缘）
    start_x = x1 + 0.9 * dx / dist
    start_y = y1 + 0.9 * dy / dist
    end_x = x2 - 0.9 * dx / dist
    end_y = y2 - 0.9 * dy / dist
    
    # 绘制箭头
    ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                arrowprops=dict(arrowstyle='->', color='red', lw=2.5, ec='red'))
    
    # 路径系数标签
    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2
    ax.text(mid_x, mid_y + 0.4, f'β={coef:.3f}', ha='center', va='bottom', 
            fontsize=11, fontweight='bold', color='red', bbox=dict(boxstyle='round', facecolor='white', ec='none'))

# 绘制潜变量到观测变量的路径（测量模型）
latent_to_obs = {
    '综合感知': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'],
    '支持态度': ['B1', 'B2', 'B3', 'B4'],
    '购买意愿': ['C1', 'C2', 'C3', 'C4'],
    '推广容易度': ['D1', 'D2', 'D3', 'D4']
}

for lv_name, obs_list in latent_to_obs.items():
    lx, ly = latent_positions[lv_name]
    for obs in obs_list:
        ox, oy = observed_positions[obs]
        loading = factor_loadings[obs]
        
        # 绘制箭头
        ax.annotate('', xy=(ox, oy), xytext=(lx, ly),
                    arrowprops=dict(arrowstyle='->', color='blue', lw=1, ec='blue', alpha=0.6))
        
        # 因子载荷标签
        mid_x = (lx + ox) / 2
        mid_y = (ly + oy) / 2
        ax.text(mid_x + 0.15, mid_y + 0.15, f'{loading:.2f}', ha='left', va='bottom',
                fontsize=8, color='blue', bbox=dict(boxstyle='round', facecolor='white', ec='none', alpha=0.7))

# 添加图例
legend_x, legend_y = 2, 1.5
ax.text(legend_x, legend_y + 0.8, '图例', fontsize=12, fontweight='bold')

# 潜变量图例
circle = plt.Circle((legend_x + 0.5, legend_y + 0.6), 0.25, color='lightblue', ec='darkblue', lw=2)
ax.add_patch(circle)
ax.text(legend_x + 1.2, legend_y + 0.6, '潜变量', fontsize=10, va='center')

# 观测变量图例
rect = plt.Rectangle((legend_x + 3, legend_y + 0.45), 0.5, 0.35, color='lightgreen', ec='darkgreen', lw=1.5)
ax.add_patch(rect)
ax.text(legend_x + 4, legend_y + 0.6, '观测变量', fontsize=10, va='center')

# 误差项图例
error_circle = plt.Circle((legend_x + 5.5, legend_y + 0.6), 0.15, color='lightyellow', ec='orange', lw=1)
ax.add_patch(error_circle)
ax.text(legend_x + 6.1, legend_y + 0.6, '误差项', fontsize=10, va='center')

# 结构路径图例
ax.annotate('', xy=(legend_x + 0.8, legend_y + 0.1), xytext=(legend_x + 0.3, legend_y + 0.1),
            arrowprops=dict(arrowstyle='->', color='red', lw=2.5))
ax.text(legend_x + 1.2, legend_y + 0.1, '结构路径 (β)', fontsize=10, va='center', color='red')

# 因子载荷图例
ax.annotate('', xy=(legend_x + 3.5, legend_y), xytext=(legend_x + 3, legend_y),
            arrowprops=dict(arrowstyle='->', color='blue', lw=1, alpha=0.6))
ax.text(legend_x + 4, legend_y, '因子载荷', fontsize=10, va='center', color='blue')

# 保存
plt.tight_layout()
plt.savefig('C:/Users/Mr Zhou/Desktop/飞书智能化报告/SEM 路径图_Python.png', dpi=150, bbox_inches='tight')
plt.close()

print("SEM 路径图已保存：C:/Users/Mr Zhou/Desktop/飞书智能化报告/SEM 路径图_Python.png")
