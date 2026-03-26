### 角色7：频率分析自动化
读取本地的频率分析结果文档，以及类似年级分布.png这样的图片，插入到分析报告的第二章节中，并对表格进行解读分析，学术性口吻，不换行输出。参考如下代码：
………………………………………………………………
import pandas as pd
from docx import Document
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import os

# ========== 辅助函数 ==========
# 创建标准化的docx表格
def create_docx_table(doc, data, title=None, note=None):
    """
    创建标准化的docx表格
    :param doc: docx文档对象
    :param data: 数据框
    :param title: 表格标题
    :param note: 表格注释
    :return: 添加表格后的docx文档对象
    """
    if title:
        doc.add_heading(title, 2)
    
    table = doc.add_table(rows=data.shape[0]+1, cols=data.shape[1])
    table.style = 'Light Grid Accent 1'
    
    # 添加表头
    for j, col in enumerate(data.columns):
        table.cell(0, j).text = str(col)
    
    # 添加数据
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            table.cell(i+1, j).text = str(data.iloc[i, j])
    
    if note:
        para = doc.add_paragraph()
        para.paragraph_format.first_line_indent = Cm(0.74)
        para.add_run(note)
    
    return doc

# 计算相关系数矩阵（下三角格式）
def create_correlation_table(data):
    """
    创建相关系数表（下三角格式，含均值和标准差）
    :param data: 数据框
    :return: 格式化的相关系数表
    """
    # 计算相关系数和p值
    corr_matrix = data.corr()
    p_values = pd.DataFrame(index=corr_matrix.index, columns=corr_matrix.columns)
    
    # 计算p值
    from scipy import stats
    for i in range(len(corr_matrix.columns)):
        for j in range(len(corr_matrix.columns)):
            if i != j:
                _, p_val = stats.pearsonr(data.iloc[:, i], data.iloc[:, j])
                p_values.iloc[i, j] = p_val
            else:
                p_values.iloc[i, j] = 0
    
    # 创建相关系数表（下三角格式，带显著性标记）
    cor_display = corr_matrix.round(3).astype(str)
    
    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix.columns)):
            if i > j:
                # 下三角显示相关系数及显著性
                p_val = p_values.iloc[i, j]
                if p_val < 0.001:
                    cor_display.iloc[i, j] = f"{corr_matrix.iloc[i, j]:.3f}***"
                elif p_val < 0.01:
                    cor_display.iloc[i, j] = f"{corr_matrix.iloc[i, j]:.3f}**"
                elif p_val < 0.05:
                    cor_display.iloc[i, j] = f"{corr_matrix.iloc[i, j]:.3f}*"
                else:
                    cor_display.iloc[i, j] = f"{corr_matrix.iloc[i, j]:.3f}"
            elif i == j:
                # 对角线显示1.00
                cor_display.iloc[i, j] = "1.00"
            else:
                # 上三角为空
                cor_display.iloc[i, j] = ""
    
    # 计算均值和标准差
    means = data.mean().round(3)
    sds = data.std().round(3)
    
    # 创建数据框，添加均值和标准差列
    cor_df = pd.DataFrame({
        '变量': cor_display.index,
        '均值': means,
        '标准差': sds
    })
    
    # 添加相关系数列
    for col in cor_display.columns:
        cor_df[col] = cor_display[col]
    
    return cor_df

# 读取基础数据
try:
    df = pd.read_excel('基础数据.xlsx')
    print(f"成功读取数据，共{len(df)}份样本\n")
except:
    print("读取Excel失败，尝试读取SPSS文件")
    import pyreadstat
    df, meta = pyreadstat.read_sav('基础数据.sav')
    print(f"成功读取数据，共{len(df)}份样本\n")

N = len(df)

# 创建Word文档
doc = Document()

# 设置默认字体
style = doc.styles['Normal']
style.font.name = '宋体'
style._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
style.font.size = Pt(12)

# 标题
title = doc.add_heading('基础数据频率分析报告', 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in title.runs:
    run.font.name = '黑体'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    run.font.size = Pt(20)

# 样本说明
para_intro = doc.add_paragraph()
para_intro.paragraph_format.first_line_indent = Cm(0.74)
para_intro.add_run(f'本次调查共收集有效问卷{N}份，调查对象为短视频用户，主要围绕短视频使用行为及文旅信息采纳情况展开。以下为各题项的详细频率统计分析结果。')

doc.add_paragraph()

# 1. 短视频用户
doc.add_heading('一、短视频用户筛选', 2)
col = df.columns[0]
freq = df[col].value_counts().sort_index()
pct = (freq / N * 100).round(2)

table1 = doc.add_table(rows=len(freq)+2, cols=3)
table1.style = 'Light Grid Accent 1'
table1.rows[0].cells[0].text = '选项'
table1.rows[0].cells[1].text = '频数'
table1.rows[0].cells[2].text = '百分比(%)'

for i, (idx, val) in enumerate(freq.items(), 1):
    table1.rows[i].cells[0].text = str(idx)
    table1.rows[i].cells[1].text = str(val)
    table1.rows[i].cells[2].text = f'{pct[idx]:.2f}%'

table1.rows[-1].cells[0].text = '合计'
table1.rows[-1].cells[1].text = str(N)
table1.rows[-1].cells[2].text = '100.00%'

para1 = doc.add_paragraph()
para1.paragraph_format.first_line_indent = Cm(0.74)
yes_pct = pct.iloc[0]
para1.add_run(f'在{N}份有效样本中，{freq.iloc[0]}人（{yes_pct:.2f}%）表示是短视频用户，仅{freq.iloc[1] if len(freq)>1 else 0}人（{pct.iloc[1] if len(pct)>1 else 0:.2f}%）表示不是短视频用户，说明短视频在调查对象中的渗透率极高，绝大多数受访者均有使用短视频的经历，符合当前移动互联网时代短视频平台广泛普及的现实情况。')

doc.add_paragraph()

# 2. 性别分布
doc.add_heading('二、性别分布', 2)
col = df.columns[1]
freq = df[col].value_counts().sort_index()
pct = (freq / N * 100).round(2)

table2 = doc.add_table(rows=len(freq)+2, cols=3)
table2.style = 'Light Grid Accent 1'
table2.rows[0].cells[0].text = '性别'
table2.rows[0].cells[1].text = '频数'
table2.rows[0].cells[2].text = '百分比(%)'

for i, (idx, val) in enumerate(freq.items(), 1):
    table2.rows[i].cells[0].text = str(idx)
    table2.rows[i].cells[1].text = str(val)
    table2.rows[i].cells[2].text = f'{pct[idx]:.2f}%'

table2.rows[-1].cells[0].text = '合计'
table2.rows[-1].cells[1].text = str(N)
table2.rows[-1].cells[2].text = '100.00%'

# 插入性别分布图
if os.path.exists('性别分布.png'):
    doc.add_paragraph()
    pic_para = doc.add_paragraph()
    pic_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = pic_para.add_run()
    run.add_picture('性别分布.png', width=Cm(12))
    caption = doc.add_paragraph('图1 性别分布')
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in caption.runs:
        run.font.size = Pt(10.5)

para2 = doc.add_paragraph()
para2.paragraph_format.first_line_indent = Cm(0.74)
male_count = freq.iloc[0]
female_count = freq.iloc[1] if len(freq) > 1 else 0
male_pct = pct.iloc[0]
female_pct = pct.iloc[1] if len(pct) > 1 else 0
para2.add_run(f'从性别分布来看，男性受访者{male_count}人，占比{male_pct:.2f}%；女性受访者{female_count}人，占比{female_pct:.2f}%。样本性别比例较为均衡，女性略多于男性，这与短视频用户的实际性别结构基本吻合，多项研究表明女性用户在短视频平台上的活跃度和使用时长普遍高于男性，本次调查样本具有一定的代表性。')

doc.add_paragraph()

# 3. 年龄分布
doc.add_heading('三、年龄分布', 2)
col = df.columns[2]
freq = df[col].value_counts().sort_index()
pct = (freq / N * 100).round(2)

table3 = doc.add_table(rows=len(freq)+2, cols=3)
table3.style = 'Light Grid Accent 1'
table3.rows[0].cells[0].text = '年龄段'
table3.rows[0].cells[1].text = '频数'
table3.rows[0].cells[2].text = '百分比(%)'

for i, (idx, val) in enumerate(freq.items(), 1):
    table3.rows[i].cells[0].text = str(idx)
    table3.rows[i].cells[1].text = str(val)
    table3.rows[i].cells[2].text = f'{pct[idx]:.2f}%'

table3.rows[-1].cells[0].text = '合计'
table3.rows[-1].cells[1].text = str(N)
table3.rows[-1].cells[2].text = '100.00%'

# 插入年龄分布图
if os.path.exists('年龄分布.png'):
    doc.add_paragraph()
    pic_para = doc.add_paragraph()
    pic_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = pic_para.add_run()
    run.add_picture('年龄分布.png', width=Cm(12))
    caption = doc.add_paragraph('图2 年龄分布')
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in caption.runs:
        run.font.size = Pt(10.5)

para3 = doc.add_paragraph()
para3.paragraph_format.first_line_indent = Cm(0.74)
para3.add_run(f'年龄分布呈现明显的年轻化特征，18-24岁年龄段的受访者{freq.iloc[1]}人，占比{pct.iloc[1]:.2f}%，构成样本的主体。小于18岁的受访者{freq.iloc[0]}人，占比{pct.iloc[0]:.2f}%；大于24岁的受访者{freq.iloc[2]}人，占比{pct.iloc[2]:.2f}%。整体来看，样本以青年群体为主，这一结果与短视频用户的年龄结构高度一致，根据相关行业报告，18-30岁青年群体是短视频平台的核心用户，本次调查准确地捕捉到了这一主要用户群体的特征，为后续分析短视频对文旅决策的影响提供了适切的样本基础。')

doc.add_paragraph()

# 4. 年级分布
doc.add_heading('四、学历层次分布', 2)
col = df.columns[3]
freq = df[col].value_counts().sort_index()
pct = (freq / N * 100).round(2)

table4 = doc.add_table(rows=len(freq)+2, cols=3)
table4.style = 'Light Grid Accent 1'
table4.rows[0].cells[0].text = '学历'
table4.rows[0].cells[1].text = '频数'
table4.rows[0].cells[2].text = '百分比(%)'

for i, (idx, val) in enumerate(freq.items(), 1):
    table4.rows[i].cells[0].text = str(idx)
    table4.rows[i].cells[1].text = str(val)
    table4.rows[i].cells[2].text = f'{pct[idx]:.2f}%'

table4.rows[-1].cells[0].text = '合计'
table4.rows[-1].cells[1].text = str(N)
table4.rows[-1].cells[2].text = '100.00%'

# 插入年级分布图
if os.path.exists('年级分布.png'):
    doc.add_paragraph()
    pic_para = doc.add_paragraph()
    pic_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = pic_para.add_run()
    run.add_picture('年级分布.png', width=Cm(12))
    caption = doc.add_paragraph('图3 学历层次分布')
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in caption.runs:
        run.font.size = Pt(10.5)

para4 = doc.add_paragraph()
para4.paragraph_format.first_line_indent = Cm(0.74)
para4.add_run(f'学历分布呈现中等偏高的特征，本科学历受访者最多，共{freq.iloc[1]}人，占比{pct.iloc[1]:.2f}%；专科学历受访者{freq.iloc[0]}人，占比{pct.iloc[0]:.2f}%；硕士学历受访者{freq.iloc[2]}人，占比{pct.iloc[2]:.2f}%；博士学历受访者{freq.iloc[3]}人，占比{pct.iloc[3]:.2f}%。整体来看，本科和专科学历受访者占据绝对多数，达到{(pct.iloc[0]+pct.iloc[1]):.2f}%，这反映了当前高等教育普及化背景下年轻群体的学历结构特点，也说明短视频用户群体具有较高的教育水平和信息素养，对文旅信息的接收、理解和采纳能力较强。')

doc.add_paragraph()

# 5. 学科分布
doc.add_heading('五、学科分布', 2)
col = df.columns[4]
freq = df[col].value_counts().sort_index()
pct = (freq / N * 100).round(2)

table5 = doc.add_table(rows=len(freq)+2, cols=3)
table5.style = 'Light Grid Accent 1'
table5.rows[0].cells[0].text = '学科类别'
table5.rows[0].cells[1].text = '频数'
table5.rows[0].cells[2].text = '百分比(%)'

for i, (idx, val) in enumerate(freq.items(), 1):
    table5.rows[i].cells[0].text = str(idx)
    table5.rows[i].cells[1].text = str(val)
    table5.rows[i].cells[2].text = f'{pct[idx]:.2f}%'

table5.rows[-1].cells[0].text = '合计'
table5.rows[-1].cells[1].text = str(N)
table5.rows[-1].cells[2].text = '100.00%'

# 插入学科分布图
if os.path.exists('学科分布.png'):
    doc.add_paragraph()
    pic_para = doc.add_paragraph()
    pic_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = pic_para.add_run()
    run.add_picture('学科分布.png', width=Cm(12))
    caption = doc.add_paragraph('图4 学科分布')
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in caption.runs:
        run.font.size = Pt(10.5)

para5 = doc.add_paragraph()
para5.paragraph_format.first_line_indent = Cm(0.74)
para5.add_run(f'学科分布呈现多元化特征，自然科学类专业受访者{freq.iloc[0]}人，占比{pct.iloc[0]:.2f}%；社会科学类专业受访者{freq.iloc[1]}人，占比{pct.iloc[1]:.2f}%；人文科学类专业受访者{freq.iloc[2]}人，占比{pct.iloc[2]:.2f}%；其他专业受访者{freq.iloc[3]}人，占比{pct.iloc[3]:.2f}%。三大学科门类的受访者分布较为均衡，说明短视频的使用和文旅信息的获取并不局限于特定学科背景，而是跨学科的普遍现象，这为研究短视频对不同知识背景群体的文旅决策影响提供了多样化的样本来源。')

doc.add_paragraph()

# 6. 使用经验
doc.add_heading('六、短视频使用经验', 2)
col = df.columns[5]
freq = df[col].value_counts().sort_index()
pct = (freq / N * 100).round(2)

table6 = doc.add_table(rows=len(freq)+2, cols=3)
table6.style = 'Light Grid Accent 1'
table6.rows[0].cells[0].text = '使用时长'
table6.rows[0].cells[1].text = '频数'
table6.rows[0].cells[2].text = '百分比(%)'

for i, (idx, val) in enumerate(freq.items(), 1):
    table6.rows[i].cells[0].text = str(idx)
    table6.rows[i].cells[1].text = str(val)
    table6.rows[i].cells[2].text = f'{pct[idx]:.2f}%'

table6.rows[-1].cells[0].text = '合计'
table6.rows[-1].cells[1].text = str(N)
table6.rows[-1].cells[2].text = '100.00%'

# 插入使用经验分布图
if os.path.exists('使用经验分布.png'):
    doc.add_paragraph()
    pic_para = doc.add_paragraph()
    pic_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = pic_para.add_run()
    run.add_picture('使用经验分布.png', width=Cm(12))
    caption = doc.add_paragraph('图5 短视频使用经验分布')
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in caption.runs:
        run.font.size = Pt(10.5)

para6 = doc.add_paragraph()
para6.paragraph_format.first_line_indent = Cm(0.74)
para6.add_run(f'从短视频使用经验来看，使用时间在3年以上的受访者{freq.iloc[3]}人，占比{pct.iloc[3]:.2f}%，为最大群体；使用时间2-3年的受访者{freq.iloc[2]}人，占比{pct.iloc[2]:.2f}%；使用时间1-2年的受访者{freq.iloc[1]}人，占比{pct.iloc[1]:.2f}%；使用时间不足1年的受访者{freq.iloc[0]}人，占比{pct.iloc[0]:.2f}%。数据显示，超过{(pct.iloc[2]+pct.iloc[3]):.2f}%的受访者使用短视频已有2年以上的经验，说明样本群体对短视频平台具有较高的熟悉度和使用粘性，长期的使用经验使得用户对短视频内容的筛选、判断和信任度建立了相对稳定的认知模式，这为研究短视频内容对文旅决策的影响机制提供了成熟用户样本的支持。')

doc.add_paragraph()

# 7. 使用平台
doc.add_heading('七、主要使用的短视频平台', 2)
col = df.columns[6]
freq = df[col].value_counts().sort_index()
pct = (freq / N * 100).round(2)

table7 = doc.add_table(rows=len(freq)+2, cols=3)
table7.style = 'Light Grid Accent 1'
table7.rows[0].cells[0].text = '平台名称'
table7.rows[0].cells[1].text = '频数'
table7.rows[0].cells[2].text = '百分比(%)'

for i, (idx, val) in enumerate(freq.items(), 1):
    table7.rows[i].cells[0].text = str(idx)
    table7.rows[i].cells[1].text = str(val)
    table7.rows[i].cells[2].text = f'{pct[idx]:.2f}%'

table7.rows[-1].cells[0].text = '合计'
table7.rows[-1].cells[1].text = str(N)
table7.rows[-1].cells[2].text = '100.00%'

# 插入使用平台分布图
if os.path.exists('使用平台分布.png'):
    doc.add_paragraph()
    pic_para = doc.add_paragraph()
    pic_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = pic_para.add_run()
    run.add_picture('使用平台分布.png', width=Cm(14))
    caption = doc.add_paragraph('图6 主要使用的短视频平台分布')
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in caption.runs:
        run.font.size = Pt(10.5)

para7 = doc.add_paragraph()
para7.paragraph_format.first_line_indent = Cm(0.74)
para7.add_run(f'在主要使用的短视频平台分布方面，抖音以{freq.iloc[1]}人（{pct.iloc[1]:.2f}%）的占比位居首位，成为受访者使用最多的短视频平台，这与抖音在国内短视频市场的领先地位相符；小红书以{freq.iloc[4]}人（{pct.iloc[4]:.2f}%）的占比位列第二，作为生活方式分享平台，小红书在文旅内容传播方面具有显著优势，其"种草"属性与文旅信息采纳行为高度契合；快手、B站、微博等平台分别占有一定比例，形成了多元化的平台使用格局。整体来看，抖音和小红书两大平台的用户占比超过{(pct.iloc[1]+pct.iloc[4]):.2f}%，说明这两个平台在文旅信息传播和用户决策影响方面具有重要地位，是研究短视频驱动文旅消费的关键平台样本。')

doc.add_paragraph()

# 8. 文旅采纳行为
doc.add_heading('八、文旅信息采纳行为', 2)
col = df.columns[7]
freq = df[col].value_counts().sort_index()
pct = (freq / N * 100).round(2)

table8 = doc.add_table(rows=len(freq)+2, cols=3)
table8.style = 'Light Grid Accent 1'
table8.rows[0].cells[0].text = '是否采纳'
table8.rows[0].cells[1].text = '频数'
table8.rows[0].cells[2].text = '百分比(%)'

for i, (idx, val) in enumerate(freq.items(), 1):
    table8.rows[i].cells[0].text = str(idx)
    table8.rows[i].cells[1].text = str(val)
    table8.rows[i].cells[2].text = f'{pct[idx]:.2f}%'

table8.rows[-1].cells[0].text = '合计'
table8.rows[-1].cells[1].text = str(N)
table8.rows[-1].cells[2].text = '100.00%'

# 插入文旅采纳行为分布图
if os.path.exists('文旅采纳行为分布.png'):
    doc.add_paragraph()
    pic_para = doc.add_paragraph()
    pic_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = pic_para.add_run()
    run.add_picture('文旅采纳行为分布.png', width=Cm(12))
    caption = doc.add_paragraph('图7 文旅信息采纳行为分布')
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in caption.runs:
        run.font.size = Pt(10.5)

para8 = doc.add_paragraph()
para8.paragraph_format.first_line_indent = Cm(0.74)
para8.add_run(f'在文旅信息采纳行为方面，{freq.iloc[0]}人（{pct.iloc[0]:.2f}%）的受访者表示曾经因为观看短视频而产生过文旅信息采纳行为，包括根据短视频推荐选择文旅目的地并产生出游决策等具体行为。这一高比例数据充分说明，短视频已成为影响用户文旅决策的重要信息源和决策参考渠道，短视频通过视觉化、场景化的内容呈现方式，有效降低了用户对目的地的信息获取成本和认知门槛，激发了用户的旅游意愿并促进了决策行为的发生。仅有{freq.iloc[1]}人（{pct.iloc[1]:.2f}%）的受访者表示未曾产生过此类行为，说明绝大多数短视频用户都在不同程度上受到了短视频内容的影响，产生了从信息接触到行为转化的完整决策链条。')

doc.add_paragraph()

# 插入汇总图
if os.path.exists('基础数据分布汇总.png'):
    doc.add_page_break()
    doc.add_heading('九、基础数据分布汇总', 2)
    pic_para = doc.add_paragraph()
    pic_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = pic_para.add_run()
    run.add_picture('基础数据分布汇总.png', width=Cm(16))
    caption = doc.add_paragraph('图8 基础数据分布汇总')
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in caption.runs:
        run.font.size = Pt(10.5)
    doc.add_paragraph()

# 综合分析
doc.add_heading('十、综合分析', 1)

para_summary = doc.add_paragraph()
para_summary.paragraph_format.first_line_indent = Cm(0.74)
para_summary.add_run(f'综合以上八个维度的频率分析结果，本次调查样本呈现出以下显著特征：第一，样本具有高度的代表性和针对性，{N}份有效样本中98%以上为短视频用户，且超过81%产生过文旅信息采纳行为，样本聚焦于短视频与文旅决策的核心研究对象，为后续深入分析提供了精准的数据基础。第二，样本人口统计特征呈现明显的年轻化、高学历化特点，18-24岁青年群体占比超过60%，本科及以上学历占比超过65%，这一群体具有较强的信息接收能力、审美鉴赏能力和消费决策能力，是文旅市场的主力消费群体，也是短视频营销的重点目标人群。第三，样本的短视频使用经验较为丰富，65%以上的受访者使用短视频已超过2年，长期的使用经验培养了用户对短视频内容的筛选判断能力和平台算法的适应性，使得用户能够更有效地从海量短视频内容中获取符合自身需求的文旅信息。第四，样本的平台使用呈现集中化趋势，抖音和小红书两大平台用户占比超过57%，这两个平台在内容生态、算法推荐、用户画像等方面具有鲜明特色，是研究短视频驱动文旅消费机制的典型样本平台。')

para_summary2 = doc.add_paragraph()
para_summary2.paragraph_format.first_line_indent = Cm(0.74)
para_summary2.add_run(f'从样本的内在逻辑来看，各维度之间呈现出较强的关联性和一致性：年轻化的年龄结构与高学历特征相互印证，反映了当前高等教育普及化背景下青年群体的基本面貌；丰富的短视频使用经验与高文旅采纳率相互支撑，说明长期的短视频使用习惯培养了用户对短视频文旅内容的信任和依赖，从而促进了信息采纳行为的发生；集中化的平台使用分布与主流短视频平台的市场格局相吻合，体现了样本的真实性和代表性。基于以上分析，本次调查样本具有良好的结构效度和内容效度，能够有效支撑后续关于短视频影响文旅决策机制、路径和效果的深入研究，为揭示短视频时代文旅信息传播与消费行为的新特征、新规律提供了可靠的实证依据。')

# ========== 相关分析 ==========
# 选择数值型变量进行相关分析
numeric_cols = df.select_dtypes(include=['number']).columns
if len(numeric_cols) > 1:
    # 创建相关系数表（下三角格式，含均值和标准差）
    cor_df = create_correlation_table(df[numeric_cols])
    
    # 添加相关分析章节
    doc.add_heading('十一、变量相关分析', 1)
    doc = create_docx_table(
        doc, 
        cor_df, 
        title="相关系数矩阵（下三角）",
        note="注：下三角为Pearson相关系数及显著性标记。*** p < 0.001, ** p < 0.01, * p < 0.05"
    )
    
    # 添加相关分析解读
    para_corr = doc.add_paragraph()
    para_corr.paragraph_format.first_line_indent = Cm(0.74)
    para_corr.add_run('相关分析结果显示，各变量之间存在不同程度的关联性。从相关系数矩阵可以看出，短视频使用经验与文旅信息采纳行为呈显著正相关关系，表明使用短视频时间越长，用户因短视频内容产生文旅决策行为的可能性越高。同时，年龄与短视频使用经验之间存在负相关关系，反映出年轻群体更早接触并长期使用短视频平台的特征。学历与文旅信息采纳行为之间的正相关关系表明，教育水平较高的用户更倾向于通过短视频获取文旅信息并做出决策。这些相关性为后续构建结构方程模型、探究变量间的因果关系提供了基础依据。')

# 保存文档
doc.save('频率分析报告_含图片.docx')
print("✓ 已生成：频率分析报告_含图片.docx")
print(f"\n分析完成！共分析{N}份样本，8个维度，已插入8张图片。")
……………………………………

注意：文字部分不是固定的，灵活处理
注意：学术性口吻输出文字。不换行输出。
