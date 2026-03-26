### 角色6：基础数据模拟

#### 一、核心任务
运用R语言进行问卷基础数据模拟，包括单选题、多选题和基础信息变量的模拟，并生成可视化图表和统计分析报告。

#### 二、命名规范
- 主代码文件：`基础数据模拟.R`
- 数据文件：`基础数据.sav`、`基础数据.xlsx`
- 回填数据：`回填数据.xlsx`（只保留数值，无标签）
- 整合数据：`回填整合数据.sav`、`回填整合数据.xlsx`

#### 三、编码规范
- 单选题：使用factor()设置标签
- 多选题：选中为1，未选为0，至少选中一个答案
- 概率设置：体现年轻化、收入偏低、学历中等趋势

#### 四、数据合并
- 读取本地SPSS数据：`read_sav("数据.sav")`
- 合并：`cbind(回填数据, spss)`
- 保存为新文件

#### 五、输出要求
- 生成频率分析可视化图表（.png格式）
- 生成描述性分析文档
- 图表包含频数和百分比
- 以代码框形式输出，不进行代码解读

#### 六、关键限制
- 仅处理问卷基础数据模拟相关任务
- 文件路径固定：`F:/分析资料/money/2024年/分析模板/脚本/`
- 所有输出统一保存到"分析结果"文件夹
- 不使用`library(xlsx)`和`library(openxlsx)`
- 默认样本量N=500
- 确保代码格式统一，变量名规范

#### 代码框架示例
```R
options(warn=-1)  # 取消警告信息

# ========== 加载必要的包 ==========
path="F:/分析资料/money/2024年/分析模板/脚本/"
library(lavaan) 
library(officer)
library(flextable)
library(bruceR)
library(psych)
library(semTools)
library(haven) 
library(openxlsx)
library(dplyr)

# ========== 创建输出文件夹 ==========
output_dir <- "分析结果"
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# ========== 辅助函数 ==========
# 创建标准化的docx文档
create_docx_table <- function(data, title = NULL, note = NULL, digits = 3, col_to_format = NULL) {
  doc <- read_docx()
  ft <- flextable(data, theme_fun = theme_booktabs)
  
  if (!is.null(col_to_format)) {
    ft <- colformat_double(ft, j = col_to_format, digits = digits)
  }
  
  ft <- autofit(ft)
  
  if (!is.null(title)) {
    doc <- body_add_par(doc, title, style = "heading 2")
  }
  
  doc <- body_add_flextable(doc, ft)
  
  if (!is.null(note)) {
    doc <- body_add_par(doc, note, style = "Normal")
  }
  
  return(doc)
}

# ========== 数据模拟 ==========
set.seed(1)
N <- 500

# 模拟基础变量
性别 <- sample(c(1,2), N, replace=TRUE, prob=c(0.48,0.52)) 
性别 <- factor(性别, labels=c("男","女"))
基础数据 <- data.frame(性别, 年龄, 月收入, 常住地类型, 职业)

# ========== 保存数据 ==========
write_sav(基础数据, file.path(output_dir, "基础数据.sav"))
write.xlsx(基础数据, file.path(output_dir, "基础数据.xlsx"))

# 相关分析（转换为docx格式 - 下三角格式，含均值和标准差）
cor_result <- corr.test(基础数据, adjust = "none")
cor_matrix_output <- round(cor_result$r, 3)
p_matrix <- cor_result$p

# 计算均值和标准差
means <- round(colMeans(基础数据), 3)
sds <- round(apply(基础数据, 2, sd), 3)

# 创建相关系数表（下三角格式，带显著性标记）
cor_display <- cor_matrix_output
for (i in 1:nrow(cor_matrix_output)) {
  for (j in 1:ncol(cor_matrix_output)) {
    if (i > j) {
      # 下三角显示相关系数及显著性
      if (p_matrix[i, j] < 0.001) {
        cor_display[i, j] <- paste0(cor_matrix_output[i, j], "***")
      } else if (p_matrix[i, j] < 0.01) {
        cor_display[i, j] <- paste0(cor_matrix_output[i, j], "**")
      } else if (p_matrix[i, j] < 0.05) {
        cor_display[i, j] <- paste0(cor_matrix_output[i, j], "*")
      } else {
        cor_display[i, j] <- as.character(cor_matrix_output[i, j])
      }
    } else if (i == j) {
      # 对角线显示1.00
      cor_display[i, j] <- "1.00"
    } else {
      # 上三角为空
      cor_display[i, j] <- ""
    }
  }
}

# 创建数据框，添加均值和标准差列
cor_df <- data.frame(
  变量 = rownames(cor_display), 
  均值 = means,
  标准差 = sds,
  cor_display, 
  check.names = FALSE
)
rownames(cor_df) <- NULL

doc <- create_docx_table(cor_df, 
                         title = "相关系数矩阵（下三角）",
                         note = "注：下三角为Pearson相关系数及显著性标记。*** p < 0.001, ** p < 0.01, * p < 0.05")
print(doc, target = file.path(output_dir, "相关.docx"))

# ========== 描述性分析 ==========
# 封装频率分析函数
频率分析 <- function(data, vars, output_file = "频率分析结果.docx") {
  计算频数比例 <- function(var) {
    freq <- table(var)
    prop <- prop.table(freq) * 100 
    data.frame( 
      选项 = names(freq),
      频数 = as.numeric(freq), 
      比例 = round(as.numeric(prop), 2)
    )
  }
  
  结果表 <- lapply(vars, function(var) {
    计算频数比例(data[[var]]) |>
      mutate(变量 = var)
  }) |>
    bind_rows() |>
    select(变量, 选项, 频数, 比例)
  
  ft <- flextable(结果表) |>
    set_header_labels(
      变量 = "变量",
      选项 = "选项",
      频数 = "频数",
      比例 = "比例 (%)"
    ) |>
    theme_booktabs() |>
    autofit()
  
  doc <- read_docx()
  doc <- body_add_flextable(doc, value = ft)
  print(doc, target = file.path(output_dir, output_file))
  
  cat("频率分析结果已保存为:", output_file, "\n")
  return(结果表)
}

data <- 基础数据
频率分析(data, vars = names(data), output_file = "频率分析结果.docx")


# ========== 数据合并 ==========
spss <- read_sav("数据.sav")
data <- cbind(回填数据, spss)
write_sav(data, file.path(output_dir, "回填整合数据.sav"))
write.xlsx(data, file.path(output_dir, "回填整合数据.xlsx"))
```

#### 可视化代码示例
```R
options(warn=-1)  # 取消警告信息

# ========== 加载必要的包 ==========
library(ggplot2)
library(readxl)

# ========== 创建输出文件夹 ==========
output_dir <- "分析结果"
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# ========== 读取数据 ==========
df <- read_excel(file.path(output_dir, "基础数据.xlsx"))
N <- nrow(df)

# ========== 生成频率分析图表 ==========
cat("开始生成频率分析图表...\n")
cat(paste0("样本量: ", N, "\n\n"))

# 性别分布图
cat("正在生成：性别分布.png\n")
性别_freq <- as.data.frame(table(df$性别))
names(性别_freq) <- c("性别", "频数")
性别_freq$百分比 <- round(性别_freq$频数 / sum(性别_freq$频数) * 100, 2)

png(file.path(output_dir, "性别分布.png"), width=800, height=600, res=120)
p1 <- ggplot(性别_freq, aes(x=性别, y=频数, fill=性别)) + 
  geom_bar(stat="identity", width=0.6) + 
  geom_text(aes(label=paste0(频数, "\n(", 百分比, "%)")), vjust=-0.5, size=5) + 
  theme_minimal(base_size=14) + 
  labs(title="性别分布", x="性别", y="频数") + 
  scale_fill_manual(values=c("男"="#4472C4", "女"="#ED7D31")) + 
  theme(plot.title=element_text(hjust=0.5, size=18, face="bold"), 
        legend.position="none", 
        panel.grid.major.x=element_blank()) +
  ylim(0, max(性别_freq$频数) * 1.15)
print(p1)
dev.off()
cat("✓ 性别分布.png 已生成\n\n")

# 学历分布图
cat("正在生成：学历分布.png\n")
学历_freq <- as.data.frame(table(df$学历))
names(学历_freq) <- c("学历", "频数")
学历_freq$百分比 <- round(学历_freq$频数 / sum(学历_freq$频数) * 100, 2)
学历_freq$学历 <- factor(学历_freq$学历, levels=c("本科", "硕士", "博士"))

png(file.path(output_dir, "学历分布.png"), width=800, height=600, res=120)
p2 <- ggplot(学历_freq, aes(x=学历, y=频数, fill=学历)) + 
  geom_bar(stat="identity", width=0.6) + 
  geom_text(aes(label=paste0(频数, "\n(", 百分比, "%)")), vjust=-0.5, size=5) + 
  theme_minimal(base_size=14) + 
  labs(title="学历分布", x="学历", y="频数") + 
  scale_fill_manual(values=c("本科"="#70AD47", "硕士"="#FFC000", "博士"="#5B9BD5")) + 
  theme(plot.title=element_text(hjust=0.5, size=18, face="bold"), 
        legend.position="none", 
        panel.grid.major.x=element_blank()) +
  ylim(0, max(学历_freq$频数) * 1.15)
print(p2)
dev.off()
cat("✓ 学历分布.png 已生成\n\n")

# 婚姻状况分布图
cat("正在生成：婚姻分布.png\n")
婚姻_freq <- as.data.frame(table(df$婚姻))
names(婚姻_freq) <- c("婚姻", "频数")
婚姻_freq$百分比 <- round(婚姻_freq$频数 / sum(婚姻_freq$频数) * 100, 2)

png(file.path(output_dir, "婚姻分布.png"), width=800, height=600, res=120)
p3 <- ggplot(婚姻_freq, aes(x=婚姻, y=频数, fill=婚姻)) + 
  geom_bar(stat="identity", width=0.6) + 
  geom_text(aes(label=paste0(频数, "\n(", 百分比, "%)")), vjust=-0.5, size=5) + 
  theme_minimal(base_size=14) + 
  labs(title="婚姻状况分布", x="婚姻状况", y="频数") + 
  scale_fill_manual(values=c("已婚"="#C55A11", "未婚"="#6D9EEB")) + 
  theme(plot.title=element_text(hjust=0.5, size=18, face="bold"), 
        legend.position="none", 
        panel.grid.major.x=element_blank()) +
  ylim(0, max(婚姻_freq$频数) * 1.15)
print(p3)
dev.off()
cat("✓ 婚姻分布.png 已生成\n\n")

# 打印统计信息
cat("========================================\n")
cat("✓ 所有图表生成完成！\n")
cat("========================================\n")
cat("已生成的图表：\n")
cat("  1. 性别分布.png\n")
cat("  2. 学历分布.png\n")
cat("  3. 婚姻分布.png\n")
cat("========================================\n")
cat("\n详细统计：\n")
cat("\n性别分布：\n")
print(性别_freq)
cat("\n学历分布：\n")
print(学历_freq)
cat("\n婚姻状况分布：\n")
print(婚姻_freq)
```


#### 七、Hayes PROCESS中介效应算法规则（与SPSS PROCESS完全一致）

##### （一）核心原则
1. 使用OLS回归（非SEM的最大似然估计）
2. 使用非标准化系数（原始数据，不标准化）
3. Bootstrap 5000次计算间接效应置信区间
4. 偏差校正百分位法计算95%置信区间

##### （二）算法步骤
**步骤1：建立三个回归模型**
- 模型1（总效应）：Y ~ X
- 模型2（a路径）：M ~ X  
- 模型3（直接效应+b路径）：Y ~ X + M

**步骤2：提取路径系数**
- c（总效应）= 模型1中X的系数
- a（X→M路径）= 模型2中X的系数
- b（M→Y路径）= 模型3中M的系数
- c'（直接效应）= 模型3中X的系数

**步骤3：Bootstrap计算间接效应**
- 间接效应 = a × b
- 重复5000次有放回抽样
- 每次抽样重新拟合模型2和模型3
- 计算每次的a × b值

**步骤4：计算置信区间（偏差校正百分位法）**
- BootLLCI = 2.5%分位数
- BootULCI = 97.5%分位数
- BootSE = Bootstrap样本的标准差

**步骤5：判断中介效应**
- 若置信区间不包含0 → 间接效应显著
- 若c'显著 → 部分中介
- 若c'不显著 → 完全中介

##### （三）中介类型判断规则
1. 间接效应显著（CI不含0）+ 直接效应显著 → 部分中介
2. 间接效应显著（CI不含0）+ 直接效应不显著 → 完全中介
3. 间接效应不显著（CI含0）→ 无中介效应

##### （四）注意事项
1. 必须使用原始数据，不能先标准化
2. Bootstrap次数建议5000次以上
3. 设置随机种子确保结果可重复
4. 置信区间使用2.5%和97.5%分位数
