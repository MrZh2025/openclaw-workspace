# -*- coding: utf-8 -*-
"""
使用 Graphviz 精确还原 AMOS 原图风格
"""
import os
os.environ['PATH'] = r'C:\Program Files (x86)\Graphviz\bin;' + os.environ['PATH']

from graphviz import Digraph

# 创建有向图
dot = Digraph(comment='SEM 路径图', format='png')

# 图形属性 - 简化布局
dot.attr(rankdir='LR', size='20,12', dpi='150')
dot.attr('graph', label='', bgcolor='white', margin='0')
dot.attr('node', fontname='Arial', fontsize='10')
dot.attr('edge', fontname='Arial', fontsize='9')

# ============ 潜变量（椭圆节点）============
latent_vars = ['综合感知', '支持态度', '购买意愿', '推广容易度']
for lv in latent_vars:
    dot.node(lv, lv, shape='ellipse', style='filled', fillcolor='white',
             color='black', penwidth='1.5', width='1.8', height='1.2')

# ============ 综合感知的观测变量 (A1-A8) - 左侧垂直排列 ============
a_nodes = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8']
a_errors = ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8']
a_loadings = ['0.726', '0.781', '0.786', '0.820', '0.690', '0.793', '0.761', '0.810']

with dot.subgraph(name='cluster_A') as c:
    c.attr(rank='same')
    for i, (obs, err, loading) in enumerate(zip(a_nodes, a_errors, a_loadings)):
        # 观测变量
        c.node(obs, obs, shape='box', style='filled', fillcolor='white',
               color='black', penwidth='1.2', width='0.7', height='0.5')
        # 误差项
        c.node(err, err, shape='ellipse', style='filled', fillcolor='white',
               color='black', penwidth='1.2', width='0.5', height='0.5')
        # 误差到观测变量
        c.edge(err, obs, color='black', penwidth='1')

# 综合感知到观测变量
for obs, loading in zip(a_nodes, a_loadings):
    dot.edge('综合感知', obs, label=loading, color='black', penwidth='1', dir='back')

# ============ 支持态度的观测变量 (B1-B4) - 上方 ============
b_nodes = ['B1', 'B2', 'B3', 'B4']
b_errors = ['e9', 'e10', 'e11', 'e12']
b_loadings = ['0.706', '0.787', '0.772', '0.683']

with dot.subgraph(name='cluster_B') as c:
    c.attr(rank='same')
    for obs, err, loading in zip(b_nodes, b_errors, b_loadings):
        c.node(obs, obs, shape='box', style='filled', fillcolor='white',
               color='black', penwidth='1.2', width='0.7', height='0.5')
        c.node(err, err, shape='ellipse', style='filled', fillcolor='white',
               color='black', penwidth='1.2', width='0.5', height='0.5')
        c.edge(err, obs, color='black', penwidth='1')

for obs, loading in zip(b_nodes, b_loadings):
    dot.edge('支持态度', obs, label=loading, color='black', penwidth='1', dir='back')

# 支持态度残差
dot.node('e21', 'e21', shape='ellipse', style='filled', fillcolor='white',
         color='black', penwidth='1.2', width='0.5', height='0.5')
dot.edge('e21', '支持态度', color='black', penwidth='1', dir='back')

# ============ 购买意愿的观测变量 (C1-C4) - 上方 ============
c_nodes = ['C1', 'C2', 'C3', 'C4']
c_errors = ['e13', 'e14', 'e15', 'e16']
c_loadings = ['0.764', '0.774', '0.787', '0.636']

with dot.subgraph(name='cluster_C') as c:
    c.attr(rank='same')
    for obs, err, loading in zip(c_nodes, c_errors, c_loadings):
        c.node(obs, obs, shape='box', style='filled', fillcolor='white',
               color='black', penwidth='1.2', width='0.7', height='0.5')
        c.node(err, err, shape='ellipse', style='filled', fillcolor='white',
               color='black', penwidth='1.2', width='0.5', height='0.5')
        c.edge(err, obs, color='black', penwidth='1')

for obs, loading in zip(c_nodes, c_loadings):
    dot.edge('购买意愿', obs, label=loading, color='black', penwidth='1', dir='back')

# 购买意愿残差
dot.node('e22', 'e22', shape='ellipse', style='filled', fillcolor='white',
         color='black', penwidth='1.2', width='0.5', height='0.5')
dot.edge('e22', '购买意愿', color='black', penwidth='1', dir='back')

# ============ 推广容易度的观测变量 (D1-D4) - 上方 ============
d_nodes = ['D1', 'D2', 'D3', 'D4']
d_errors = ['e17', 'e18', 'e19', 'e20']
d_loadings = ['0.788', '0.816', '0.806', '0.800']

with dot.subgraph(name='cluster_D') as c:
    c.attr(rank='same')
    for obs, err, loading in zip(d_nodes, d_errors, d_loadings):
        c.node(obs, obs, shape='box', style='filled', fillcolor='white',
               color='black', penwidth='1.2', width='0.7', height='0.5')
        c.node(err, err, shape='ellipse', style='filled', fillcolor='white',
               color='black', penwidth='1.2', width='0.5', height='0.5')
        c.edge(err, obs, color='black', penwidth='1')

for obs, loading in zip(d_nodes, d_loadings):
    dot.edge('推广容易度', obs, label=loading, color='black', penwidth='1', dir='back')

# 推广容易度残差
dot.node('e23', 'e23', shape='ellipse', style='filled', fillcolor='white',
         color='black', penwidth='1.2', width='0.5', height='0.5')
dot.edge('e23', '推广容易度', color='black', penwidth='1', dir='back')

# ============ 结构路径 ============
dot.edge('综合感知', '支持态度', label='0.422', color='black', penwidth='1.2')
dot.edge('支持态度', '购买意愿', label='0.402', color='black', penwidth='1.2')
dot.edge('购买意愿', '推广容易度', label='0.446', color='black', penwidth='1.2')

# ============ 保存 ============
output_path = 'C:/Users/Mr Zhou/Desktop/飞书智能化报告/SEM 路径图_简洁版'
dot.render(output_path, view=False, cleanup=True)

print(f"SEM 路径图已保存：{output_path}.png")
