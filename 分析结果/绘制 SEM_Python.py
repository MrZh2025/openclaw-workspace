# -*- coding: utf-8 -*-
"""
使用 graphviz 绘制 SEM 结构方程模型路径图
"""
from graphviz import Digraph

# 创建有向图
dot = Digraph(comment='SEM 路径图', format='png')
dot.attr(rankdir='LR', size='16,10', dpi='150')
dot.attr('node', shape='ellipse', style='filled', fillcolor='lightblue', fontname='SimHei')
dot.attr('edge', fontname='SimHei', fontsize='10')

# 定义潜变量（椭圆节点）
latent_vars = {
    '综合感知': '综合感知',
    '支持态度': '支持态度',
    '购买意愿': '购买意愿',
    '推广容易度': '推广容易度'
}

# 定义观测变量（矩形节点）及其对应的潜变量
observed_vars = {
    '综合感知': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'],
    '支持态度': ['B1', 'B2', 'B3', 'B4'],
    '购买意愿': ['C1', 'C2', 'C3', 'C4'],
    '推广容易度': ['D1', 'D2', 'D3', 'D4']
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

# 添加潜变量节点
for lv_id, lv_name in latent_vars.items():
    dot.node(lv_id, lv_name, shape='ellipse', fillcolor='lightblue', width='1.5', height='1.0')

# 添加观测变量和误差项
for lv_id, obs_list in observed_vars.items():
    # 为每个潜变量创建子图
    with dot.subgraph(name=f'cluster_{lv_id}') as c:
        c.attr(style='invis')
        c.attr(rank='same')
        
        for obs in obs_list:
            # 观测变量（矩形）
            dot.node(obs, obs, shape='box', fillcolor='lightgreen', width='0.8', height='0.6')
            # 误差项（小圆）
            error_id = f'e_{obs}'
            dot.node(error_id, '', shape='circle', fillcolor='lightyellow', width='0.3', height='0.3')
            
            # 因子载荷路径
            loading = factor_loadings.get(obs, 0.7)
            dot.edge(lv_id, obs, label=f'{loading:.2f}', color='blue')
            # 误差路径
            dot.edge(error_id, obs, color='gray', style='dashed')

# 添加结构模型路径（潜变量之间的关系）
for (from_lv, to_lv), coef in path_coefficients.items():
    dot.edge(from_lv, to_lv, label=f'β={coef:.3f}', color='red', penwidth='2', labelcolor='red')

# 保存并渲染
output_path = 'C:/Users/Mr Zhou/Desktop/飞书智能化报告/SEM 路径图_Python'
dot.render(output_path, view=False, cleanup=True)

print(f"SEM 路径图已保存：{output_path}.png")
