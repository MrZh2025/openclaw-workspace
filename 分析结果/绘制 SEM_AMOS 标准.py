# -*- coding: utf-8 -*-
"""
使用 Graphviz 绘制标准 AMOS 风格 SEM 路径图
AMOS 软件经典布局
"""
import os
os.environ['PATH'] = r'C:\Program Files (x86)\Graphviz\bin;' + os.environ['PATH']

from graphviz import Digraph

dot = Digraph('SEM', format='png')

# 图形属性
dot.attr(rankdir='LR', size='24,14', dpi='150')
dot.attr('graph', label='', bgcolor='white')
dot.attr('node', shape='ellipse', fontname='Arial', fontsize='11', width='1.5', height='1.0')
dot.attr('edge', fontname='Arial', fontsize='9')

# ============ 潜变量（椭圆）- 中间水平排列 ============
dot.node('综合感知', '综合感知', shape='ellipse', style='filled', fillcolor='#FFE0E0', penwidth='2')
dot.node('支持态度', '支持态度', shape='ellipse', style='filled', fillcolor='#E0FFE0', penwidth='2')
dot.node('购买意愿', '购买意愿', shape='ellipse', style='filled', fillcolor='#E0E0FF', penwidth='2')
dot.node('推广容易度', '推广容易度', shape='ellipse', style='filled', fillcolor='#FFFFE0', penwidth='2')

# ============ 综合感知 A1-A8 - 下方垂直排列 ============
a_vars = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8']
a_errs = ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8']
a_load = ['0.73', '0.78', '0.79', '0.82', '0.69', '0.79', '0.76', '0.81']

with dot.subgraph(name='cluster_A') as c:
    c.attr(rank='same')
    for obs, err, load in zip(a_vars, a_errs, a_load):
        c.node(obs, obs, shape='box', style='filled', fillcolor='white', width='0.6', height='0.5')
        c.node(err, err, shape='ellipse', style='filled', fillcolor='white', width='0.4', height='0.4')
        c.edge(err, obs, arrowhead='normal')

for obs, load in zip(a_vars, a_load):
    dot.edge('综合感知', obs, label=load, arrowhead='normal')

# ============ 支持态度 B1-B4 - 下方 ============
b_vars = ['B1', 'B2', 'B3', 'B4']
b_errs = ['e9', 'e10', 'e11', 'e12']
b_load = ['0.71', '0.79', '0.77', '0.68']

with dot.subgraph(name='cluster_B') as c:
    c.attr(rank='same')
    for obs, err, load in zip(b_vars, b_errs, b_load):
        c.node(obs, obs, shape='box', style='filled', fillcolor='white', width='0.6', height='0.5')
        c.node(err, err, shape='ellipse', style='filled', fillcolor='white', width='0.4', height='0.4')
        c.edge(err, obs, arrowhead='normal')

for obs, load in zip(b_vars, b_load):
    dot.edge('支持态度', obs, label=load, arrowhead='normal')

# 支持态度残差
dot.node('e21', 'e21', shape='ellipse', style='filled', fillcolor='white', width='0.4', height='0.4')
dot.edge('e21', '支持态度', arrowhead='normal')

# ============ 购买意愿 C1-C4 - 下方 ============
c_vars = ['C1', 'C2', 'C3', 'C4']
c_errs = ['e13', 'e14', 'e15', 'e16']
c_load = ['0.76', '0.77', '0.79', '0.64']

with dot.subgraph(name='cluster_C') as c:
    c.attr(rank='same')
    for obs, err, load in zip(c_vars, c_errs, c_load):
        c.node(obs, obs, shape='box', style='filled', fillcolor='white', width='0.6', height='0.5')
        c.node(err, err, shape='ellipse', style='filled', fillcolor='white', width='0.4', height='0.4')
        c.edge(err, obs, arrowhead='normal')

for obs, load in zip(c_vars, c_load):
    dot.edge('购买意愿', obs, label=load, arrowhead='normal')

# 购买意愿残差
dot.node('e22', 'e22', shape='ellipse', style='filled', fillcolor='white', width='0.4', height='0.4')
dot.edge('e22', '购买意愿', arrowhead='normal')

# ============ 推广容易度 D1-D4 - 下方 ============
d_vars = ['D1', 'D2', 'D3', 'D4']
d_errs = ['e17', 'e18', 'e19', 'e20']
d_load = ['0.79', '0.82', '0.81', '0.80']

with dot.subgraph(name='cluster_D') as c:
    c.attr(rank='same')
    for obs, err, load in zip(d_vars, d_errs, d_load):
        c.node(obs, obs, shape='box', style='filled', fillcolor='white', width='0.6', height='0.5')
        c.node(err, err, shape='ellipse', style='filled', fillcolor='white', width='0.4', height='0.4')
        c.edge(err, obs, arrowhead='normal')

for obs, load in zip(d_vars, d_load):
    dot.edge('推广容易度', obs, label=load, arrowhead='normal')

# 推广容易度残差
dot.node('e23', 'e23', shape='ellipse', style='filled', fillcolor='white', width='0.4', height='0.4')
dot.edge('e23', '推广容易度', arrowhead='normal')

# ============ 结构路径（单向箭头）============
dot.edge('综合感知', '支持态度', label='0.42', penwidth='1.5')
dot.edge('支持态度', '购买意愿', label='0.40', penwidth='1.5')
dot.edge('购买意愿', '推广容易度', label='0.45', penwidth='1.5')

# ============ 保存 ============
output_path = 'C:/Users/Mr Zhou/Desktop/飞书智能化报告/SEM 路径图_AMOS 标准'
dot.render(output_path, view=False, cleanup=True)

print(f"已保存：{output_path}.png")
