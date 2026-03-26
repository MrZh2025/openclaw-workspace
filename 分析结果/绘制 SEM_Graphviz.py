# -*- coding: utf-8 -*-
"""
使用 Graphviz 绘制专业 SEM 结构方程模型路径图
"""
import os
# 添加 Graphviz 到 PATH
os.environ['PATH'] = r'C:\Program Files (x86)\Graphviz\bin;' + os.environ['PATH']

from graphviz import Digraph

# 创建有向图
dot = Digraph(comment='SEM 路径图', format='png')
dot.attr(rankdir='LR', size='20,12', dpi='150')
dot.attr('graph', fontname='SimHei', fontsize='16', label='结构方程模型 (SEM) 路径图', labelloc='t', labeljust='c')
dot.attr('node', fontname='SimHei', fontsize='11')
dot.attr('edge', fontname='SimHei', fontsize='10')

# ============ 潜变量（椭圆节点）============
latent_vars = ['综合感知', '支持态度', '购买意愿', '推广容易度']
for lv in latent_vars:
    dot.node(lv, lv, shape='ellipse', style='filled', fillcolor='lightblue', 
             color='darkblue', penwidth='2.5', width='1.8', height='1.2', fontsize='12', fontcolor='darkblue')

# ============ 观测变量和误差项 ============
observed_config = {
    '综合感知': [('A1', 0.726), ('A2', 0.781), ('A3', 0.786), ('A4', 0.820), 
                 ('A5', 0.690), ('A6', 0.793), ('A7', 0.761), ('A8', 0.810)],
    '支持态度': [('B1', 0.706), ('B2', 0.787), ('B3', 0.772), ('B4', 0.683)],
    '购买意愿': [('C1', 0.764), ('C2', 0.774), ('C3', 0.787), ('C4', 0.636)],
    '推广容易度': [('D1', 0.788), ('D2', 0.816), ('D3', 0.806), ('D4', 0.800)]
}

# 为每个潜变量创建子图（观测变量在同一 rank）
for lv_id, obs_list in observed_config.items():
    with dot.subgraph(name=f'cluster_{lv_id}') as c:
        c.attr(style='invis', rank='same')
        
        for obs, loading in obs_list:
            # 观测变量（矩形）
            c.node(obs, obs, shape='box', style='filled', fillcolor='lightgreen',
                   color='darkgreen', penwidth='1.5', width='0.9', height='0.6', fontsize='10')
            
            # 误差项（小圆）
            error_id = f'e_{obs}'
            c.node(error_id, '', shape='circle', style='filled', fillcolor='lightyellow',
                   color='orange', penwidth='1.5', width='0.35', fontsize='8')
            
            # 误差到观测变量的虚线
            c.edge(error_id, obs, style='dashed', color='gray', penwidth='1')
            
            # 潜变量到观测变量的实线（因子载荷）
            dot.edge(lv_id, obs, label=f'{loading:.2f}', color='blue', penwidth='1.5', 
                     fontcolor='blue', fontsize='9', style='solid')

# ============ 结构模型路径（潜变量之间的关系）============
path_coefficients = [
    ('综合感知', '支持态度', 0.422),
    ('支持态度', '购买意愿', 0.402),
    ('购买意愿', '推广容易度', 0.446)
]

for from_lv, to_lv, coef in path_coefficients:
    dot.edge(from_lv, to_lv, label=f'β={coef:.3f}', color='red', penwidth='3', 
             fontcolor='red', fontsize='11', style='solid')

# ============ 保存并渲染 ============
output_path = 'C:/Users/Mr Zhou/Desktop/飞书智能化报告/SEM 路径图_Graphviz'
dot.render(output_path, view=False, cleanup=True)

print(f"SEM 路径图已保存：{output_path}.png")
print("特点：Graphviz 专业布局、无遮挡、清晰美观")
