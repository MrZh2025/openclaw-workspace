# -*- coding: utf-8 -*-
"""
使用 Graphviz 绘制 AMOS 风格 SEM 结构方程模型路径图
参考用户提供的图片风格
"""
import os
os.environ['PATH'] = r'C:\Program Files (x86)\Graphviz\bin;' + os.environ['PATH']

from graphviz import Digraph

# 创建有向图
dot = Digraph(comment='SEM 路径图', format='png')

# 图形属性 - 参考原图风格
dot.attr(rankdir='LR', size='24,14', dpi='150')
dot.attr('graph', fontname='SimHei', fontsize='14', label='', labelloc='t', labeljust='c', bgcolor='#F5F5F5')
dot.attr('node', fontname='SimHei', fontsize='11')
dot.attr('edge', fontname='Arial', fontsize='9')

# ============ 潜变量（椭圆节点）- 紫色 ============
latent_vars = ['综合感知', '支持态度', '购买意愿', '推广容易度']
for lv in latent_vars:
    dot.node(lv, lv, shape='ellipse', style='filled', fillcolor='#E0D4F0',
             color='black', penwidth='1.5', width='2.0', height='1.5',
             fontsize='13', fontcolor='black', fontname='SimHei')

# ============ 综合感知的观测变量 (A1-A8) - 垂直排列在左侧 ============
# 误差项 e1-e8 在观测变量左侧
a_nodes = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8']
a_errors = ['e8', 'e7', 'e6', 'e5', 'e4', 'e3', 'e2', 'e1']
a_loadings = [0.726, 0.781, 0.786, 0.820, 0.690, 0.793, 0.761, 0.810]

with dot.subgraph(name='cluster_A') as c:
    c.attr(style='invis', rank='same')
    for i, (obs, err, loading) in enumerate(zip(a_nodes, a_errors, a_loadings)):
        # 误差项
        c.node(err, err, shape='ellipse', style='filled', fillcolor='#E0D4F0',
               color='black', penwidth='1.2', width='0.6', height='0.6', fontsize='9')
        # 观测变量
        c.node(obs, obs, shape='box', style='filled', fillcolor='#E0D4F0',
               color='black', penwidth='1.2', width='0.9', height='0.7', fontsize='10')
        # 误差到观测变量的箭头
        c.edge(err, obs, color='black', penwidth='1.2')

# 综合感知到观测变量的箭头（因子载荷）
for obs, loading in zip(a_nodes, a_loadings):
    dot.edge('综合感知', obs, label=f'{loading:.3f}', color='black', penwidth='1.2',
             fontcolor='black', fontsize='8', dir='back')

# ============ 支持态度的观测变量 (B1-B4) - 水平排列在上方 ============
b_nodes = ['B1', 'B2', 'B3', 'B4']
b_errors = ['e9', 'e10', 'e11', 'e12']
b_loadings = [0.706, 0.787, 0.772, 0.683]

with dot.subgraph(name='cluster_B') as c:
    c.attr(style='invis', rank='same')
    for obs, err, loading in zip(b_nodes, b_errors, b_loadings):
        c.node(err, err, shape='ellipse', style='filled', fillcolor='#E0D4F0',
               color='black', penwidth='1.2', width='0.6', height='0.6', fontsize='9')
        c.node(obs, obs, shape='box', style='filled', fillcolor='#E0D4F0',
               color='black', penwidth='1.2', width='0.9', height='0.7', fontsize='10')
        c.edge(err, obs, color='black', penwidth='1.2')

for obs, loading in zip(b_nodes, b_loadings):
    dot.edge('支持态度', obs, label=f'{loading:.3f}', color='black', penwidth='1.2',
             fontcolor='black', fontsize='8', dir='back')

# 支持态度的误差项 e21 - 指向潜变量
dot.node('e21', 'e21', shape='ellipse', style='filled', fillcolor='#E0D4F0',
         color='black', penwidth='1.2', width='0.6', height='0.6', fontsize='9')
dot.edge('e21', '支持态度', color='black', penwidth='1.2', dir='back')

# ============ 购买意愿的观测变量 (C1-C4) - 水平排列在上方 ============
c_nodes = ['C1', 'C2', 'C3', 'C4']
c_errors = ['e13', 'e14', 'e15', 'e16']
c_loadings = [0.764, 0.774, 0.787, 0.636]

with dot.subgraph(name='cluster_C') as c:
    c.attr(style='invis', rank='same')
    for obs, err, loading in zip(c_nodes, c_errors, c_loadings):
        c.node(err, err, shape='ellipse', style='filled', fillcolor='#E0D4F0',
               color='black', penwidth='1.2', width='0.6', height='0.6', fontsize='9')
        c.node(obs, obs, shape='box', style='filled', fillcolor='#E0D4F0',
               color='black', penwidth='1.2', width='0.9', height='0.7', fontsize='10')
        c.edge(err, obs, color='black', penwidth='1.2')

for obs, loading in zip(c_nodes, c_loadings):
    dot.edge('购买意愿', obs, label=f'{loading:.3f}', color='black', penwidth='1.2',
             fontcolor='black', fontsize='8', dir='back')

# 购买意愿的误差项 e22 - 指向潜变量
dot.node('e22', 'e22', shape='ellipse', style='filled', fillcolor='#E0D4F0',
         color='black', penwidth='1.2', width='0.6', height='0.6', fontsize='9')
dot.edge('e22', '购买意愿', color='black', penwidth='1.2', dir='back')

# ============ 推广容易度的观测变量 (D1-D4) - 水平排列在上方 ============
d_nodes = ['D1', 'D2', 'D3', 'D4']
d_errors = ['e17', 'e18', 'e19', 'e20']
d_loadings = [0.788, 0.816, 0.806, 0.800]

with dot.subgraph(name='cluster_D') as c:
    c.attr(style='invis', rank='same')
    for obs, err, loading in zip(d_nodes, d_errors, d_loadings):
        c.node(err, err, shape='ellipse', style='filled', fillcolor='#E0D4F0',
               color='black', penwidth='1.2', width='0.6', height='0.6', fontsize='9')
        c.node(obs, obs, shape='box', style='filled', fillcolor='#E0D4F0',
               color='black', penwidth='1.2', width='0.9', height='0.7', fontsize='10')
        c.edge(err, obs, color='black', penwidth='1.2')

for obs, loading in zip(d_nodes, d_loadings):
    dot.edge('推广容易度', obs, label=f'{loading:.3f}', color='black', penwidth='1.2',
             fontcolor='black', fontsize='8', dir='back')

# 推广容易度的误差项 e23 - 指向潜变量
dot.node('e23', 'e23', shape='ellipse', style='filled', fillcolor='#E0D4F0',
         color='black', penwidth='1.2', width='0.6', height='0.6', fontsize='9')
dot.edge('e23', '推广容易度', color='black', penwidth='1.2', dir='back')

# ============ 结构模型路径（潜变量之间）============
path_coefficients = [
    ('综合感知', '支持态度', 0.422),
    ('支持态度', '购买意愿', 0.402),
    ('购买意愿', '推广容易度', 0.446)
]

for from_lv, to_lv, coef in path_coefficients:
    dot.edge(from_lv, to_lv, label=f'{coef:.3f}', color='black', penwidth='1.2',
             fontcolor='black', fontsize='9')

# ============ 保存并渲染 ============
output_path = 'C:/Users/Mr Zhou/Desktop/飞书智能化报告/SEM 路径图_参考原图'
dot.render(output_path, view=False, cleanup=True)

print(f"SEM 路径图已保存：{output_path}.png")
print("风格：参考用户提供的原图（紫色主题、误差项指向观测变量）")
