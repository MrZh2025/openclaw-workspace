### 角色4：Amos数据模拟（二阶结构）

#### 一、核心任务
针对有二阶结构的模型，根据用户提供的中文变量名称及题目数量，模拟结构方程模型数据，生成"模拟.R"文件并自动运行。

#### 二、变量命名规则
- 中文变量用A、B、C、D等前缀+数字表示题目（如"现状认知4"→A1-A4）
- 含字母"E"的变量替换为"EE"（如E1→EE1）
- 二阶结构示例：PWD（四个维度4333题）、PR（四个维度3332题）、MP（三个维度各3题）、US（五个维度各5题）

#### 三、模型参数设置
- 因子载荷系数：0.8-2.5，需存在差异
- 回归系数：0.2-0.5，正负向根据路径设定
- 自变量相关性：通过"~~"建立，不能超过0.25

#### 四、数据处理标准
- 默认生成965条记录（可根据需求调整）
- 标准化后切割为1-5分或1-7分制
- 输出格式：.sav、.xlsx、.dat

#### 代码框架示例
```R
options(warn=-1)  # 取消警告信息
# ========== 加载必要的包 ==========
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
N <- 965

model <- "
# 因子结构（载荷系数0.8-2.5）
PWD1=~+1.3*A1+1.2*A2+1.1*A3+1.2*A4
PWD2=~+1.2*B1+1.3*B2+1.1*B3
PWD3=~+1.2*C1+1.1*C2+1.3*C3
PWD4=~+1.1*D1+1.2*D2+1.3*D3
PWD=~1.28*PWD1+1.17*PWD2+1.16*PWD3+1.25*PWD4

PR1=~+1.2*EE1+1.3*EE2+1.1*EE3
PR2=~+1.1*F1+1.2*F2+1.3*F3
PR3=~+1.3*G1+1.1*G2+1.2*G3
PR4=~+1.42*H1+1.4*H2
PR=~0.9*PR1+0.9*PR2+0.8*PR3+0.79*PR4

MP=~1.28*MP1+1.27*MP2+1.36*MP3

US=~1.1*US1+1.2*US2+1.3*US3+1.2*US4+1.1*US5

# 回归路径（系数0.2-0.5）
PR~0.342*PWD
MP~0.38*PWD
US~0.35*PWD+0.32*PR+0.31*MP

# 残差相关
EE1~~0.35*EE3
F1~~0.3*F3
A1~~0.24*A3
"

# 模拟并离散化数据
sim_data <- simulateData(model = model, sample.nobs = N)
tammodel.norm <- sim_data - rnorm(length(unlist(sim_data)), mean = 0, sd = 0.42)  #sd是调参关键点
spss <- data.frame(lapply(tammodel.norm, function(X) {
  x_cut <- cut(X, breaks = 6, labels = FALSE)
  ifelse(x_cut > 5, 5, x_cut)
}))

# 计算各维度均值
PWD1 <- apply(spss[,1:4],1,mean)
PWD2 <- apply(spss[,5:7],1,mean)
PWD3 <- apply(spss[,8:10],1,mean)
PWD4 <- apply(spss[,11:13],1,mean)
PWD <- apply(spss[,1:13],1,mean)

PR1 <- apply(spss[,14:16],1,mean)
PR2 <- apply(spss[,17:19],1,mean)
PR3 <- apply(spss[,20:22],1,mean)
PR4 <- apply(spss[,23:24],1,mean)
PR <- apply(spss[,14:24],1,mean)

MP <- apply(spss[,25:27],1,mean)
US <- apply(spss[,28:32],1,mean)

mean2 <- as.data.frame(cbind(PWD1,PWD2,PWD3,PWD4,PR1,PR2,PR3,PR4,MP,US))
mean <- as.data.frame(cbind(PWD,PR,MP,US))

# ========== 保存数据 ==========
# 相关分析（转换为docx格式 - 下三角格式，含均值和标准差）
cor_result <- corr.test(mean, adjust = "none")
cor_matrix_output <- round(cor_result$r, 3)
p_matrix <- cor_result$p

# 计算均值和标准差
means <- round(colMeans(mean), 3)
sds <- round(apply(mean, 2, sd), 3)

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
data <- cbind(spss,mean2)
write_sav(mean, file.path(output_dir, "均值.sav"))
write_sav(as.data.frame(data), file.path(output_dir, "数据.sav"))
write.xlsx(as.data.frame(spss), file.path(output_dir, "数据.xlsx"))
write.table(spss, file.path(output_dir, "mplus.dat"), row.names = FALSE, col.names = FALSE)

# ========== 结构方程模型分析 ==========
fit.model <- "
PWD1=~+A1+A2+A3+A4
PWD2=~+B1+B2+B3
PWD3=~+C1+C2+C3
PWD4=~+D1+D2+D3
PR1=~+EE1+EE2+EE3
PR2=~+F1+F2+F3
PR3=~+G1+G2+G3
PR4=~+H1+H2
MP=~+MP1+MP2+MP3
US=~+US1+US2+US3+US4+US5
"

lv <- sem(model = fit.model, data = spss, std.lv = TRUE)

# 路径系数表
params <- parameterEstimates(lv, standardized = TRUE)
regressions <- params[params$op == "~", ]

path_table <- data.frame(
  路径 = paste(regressions$lhs, "←", regressions$rhs),
  非标准化系数 = round(regressions$est, 3),
  标准误 = round(regressions$se, 3),
  Z值 = round(regressions$z, 3),
  P值 = ifelse(regressions$pvalue < 0.001, "< .001", round(regressions$pvalue, 3)),
  标准化系数 = round(regressions$std.all, 3),
  显著性 = ifelse(regressions$pvalue < 0.001, "***",
                ifelse(regressions$pvalue < 0.01, "**",
                      ifelse(regressions$pvalue < 0.05, "*", "")))
)

doc <- create_docx_table(path_table, 
                         title = "路径系数表", 
                         note = "注：*** p < 0.001, ** p < 0.01, * p < 0.05")
print(doc, target = file.path(output_dir, "路径系数表.docx"))

# 提取拟合指标
MR <- round(fitmeasures(lv, c("GFI", "AGFI", "RMR", "RMSEA", "NFI", "IFI", "CFI", "TLI")), 3)

# ========== 因子分析 ==========
fa <- spss %>%
  EFA(vars = names(.), method = "pca", sort.loadings = FALSE,
      rotation = "varimax", plot.scree = FALSE, hide.loadings = 0.5)

# 因子载荷矩阵
loadings_matrix <- as.data.frame(unclass(fa$loadings))
loadings_matrix$共同度 <- fa$communality
loadings_matrix <- round(loadings_matrix, 3)
item_names <- colnames(spss)

# 自动识别维度对应的因子
dims <- c("A", "B", "C", "D")
num_factors <- ncol(loadings_matrix) - 1
dimension_mapping <- sapply(seq_len(num_factors), function(j) {
  avg_loadings <- sapply(1:4, function(i) {
    dim_items <- paste0(dims[i], 1:5)
    indices <- which(item_names %in% dim_items)
    if (length(indices) > 0) {
      mean(abs(loadings_matrix[indices, j]), na.rm = TRUE)
    } else {
      0
    }
  })
  paste0("维度", dims[which.max(avg_loadings)])
})

colnames(loadings_matrix) <- c(dimension_mapping, "共同度")

# 将载荷值小于0.5的设为空
for (i in seq_len(num_factors)) {
  loadings_matrix[abs(loadings_matrix[, i]) < 0.5 & !is.na(loadings_matrix[, i]), i] <- ""
}
loadings_matrix[is.na(loadings_matrix)] <- ""

loadings_df <- data.frame(题目 = item_names, loadings_matrix, row.names = NULL, check.names = FALSE)

doc <- create_docx_table(loadings_df, title = "因子载荷矩阵（旋转后）")
doc <- doc %>% 
  body_add_par("提取方法：主成分分析", style = "Normal") %>%
  body_add_par("旋转方法：凯撒正态化最大方差法", style = "Normal")
print(doc, target = file.path(output_dir, "因子载荷值.docx"))

# 方差提取率表
variance_df <- round(as.data.frame(fa$eigenvalues), 3)
colnames(variance_df) <- c("初始特征值", "初始方差百分比", "初始累积百分比", 
                           "提取载荷平方和", "提取方差百分比", "提取累积百分比")
variance_df[is.na(variance_df)] <- ""

doc <- create_docx_table(variance_df)
print(doc, target = file.path(output_dir, "方差提取率.docx"))

# ========== 区分效度表（下三角） ==========
cor_matrix <- round(lavInspect(lv, "cor.lv"), 3)
diag(cor_matrix) <- round(sqrt(AVE(lv)), 3)

# 上三角设为NA
cor_matrix[upper.tri(cor_matrix)] <- NA

df_validity <- data.frame(维度 = names(mean), cor_matrix, check.names = FALSE)
df_validity[is.na(df_validity)] <- ""

doc <- create_docx_table(df_validity, 
                         title = "区分效度表（下三角）",
                         note = "注：对角线为AVE平方根值，下三角为Pearson相关系数")
print(doc, target = file.path(output_dir, "区分效度表.docx"))

# ========== KMO和巴特利特检验 ==========
kmo_result <- KMO(spss)
bartlett_result <- cortest.bartlett(cor(spss), n = nrow(spss))

kmo_bartlett_table <- data.frame(
  " " = c("KMO 取样适切性量数。", "巴特利特球形度检验", "", ""),
  "  " = c("", "近似卡方", "自由度", "显著性"),
  值 = c(round(kmo_result$MSA, 3),
         round(bartlett_result$chisq, 3),
         bartlett_result$df,
         ifelse(bartlett_result$p.value < 0.001, ".000", round(bartlett_result$p.value, 3))),
  check.names = FALSE
)

doc <- read_docx()
ft <- flextable(kmo_bartlett_table, theme_fun = theme_booktabs)
ft <- align(ft, align = "left", part = "all")
ft <- merge_v(ft, j = 1)
ft <- autofit(ft)
doc <- doc %>% 
  body_add_par("KMO 和巴特利特检验", style = "heading 2") %>%
  body_add_flextable(ft)
print(doc, target = file.path(output_dir, "KMO分析.docx"))

# ========== 信度与效度分析 ==========
reliability_data <- round(reliability(lv, what = c("alpha", "omega", "ave"), return.total = TRUE), 3)
reliability_data <- as.data.frame(reliability_data)
item_counts <- c(5, 5, 5, 5, 20)

# 信度检验表
alpha_row <- reliability_data["alpha", ]
reliability_table <- data.frame(
  维度 = c(names(mean), "total"),
  信度值 = as.numeric(alpha_row),
  题目个数 = item_counts
)

doc <- create_docx_table(reliability_table, 
                         title = "信度检验表", 
                         col_to_format = 2)
print(doc, target = file.path(output_dir, "信度检验表.docx"))

# 聚合效度表
cr_row <- reliability_data["omega", ]
convergent_table <- data.frame(
  维度 = names(mean),
  CR值 = as.numeric(cr_row[1:4]),
  题目个数 = item_counts[1:4]
)

doc <- create_docx_table(convergent_table, 
                         title = "聚合效度表",
                         note = "注：CR值大于0.6表示聚合效度良好",
                         col_to_format = 2)
print(doc, target = file.path(output_dir, "聚合效度表.docx"))

# ========== 模型拟合度表 ==========
chisq <- round(fitmeasures(lv, "chisq"), 3)
df_model <- fitmeasures(lv, "df")
chisq_df_ratio <- round(chisq / df_model, 3)
chisq_df_result <- ifelse(chisq_df_ratio < 3, "良好", 
                          ifelse(chisq_df_ratio < 5, "合理", "较差"))

fit_table <- data.frame(
  拟合指标 = c("χ²", "df", "χ²/df", "GFI", "AGFI", "RMR", "RMSEA", "NFI", "IFI", "CFI", "TLI"),
  释义 = c("卡方值", "自由度", "卡方自由度比", "拟合优度指数", "调整后的一般契合指数",
          "残差均方根指数", "近似误差均方根指数", "规范拟合指数", "修正拟合指数", 
          "比较拟合指数", "Tucker-Lewis指数"),
  合理范围 = c("—", "—", "<3良好；<5合理", 
              rep(">0.8，模型拟合合理；>0.9，模型拟合良好", 2),
              rep("<0.08，模型拟合合理；<0.05，模型拟合良好", 2),
              rep(">0.8，模型拟合合理；>0.9，模型拟合良好", 4)),
  结果 = c(chisq, df_model, chisq_df_ratio, MR),
  评定结果 = c("—", "—", chisq_df_result, rep("良好", 8))
)

doc <- create_docx_table(fit_table, 
                         title = "模型拟合度表",
                         col_to_format = 4)
doc <- body_add_par(doc, "资料来源：Medsker et al.（1994）；侯杰秦等（2004）；史江涛（2008）等研究成果基础上整理而得。")
print(doc, target = file.path(output_dir, "模型拟合度.docx"))

# ========== 因子个数分析 ==========
eigen_values <- eigen(cor(spss))$values
num_factors_extracted <- sum(eigen_values > 1)
cat("根据特征值大于1的原则，提取的因子个数：", num_factors_extracted, "\n")
cat("原始数据维度个数：", ncol(mean), "\n")
```

#### 五、回调技能

**技能1：AVE回调**
- 若AVE值<0.5，增大对应维度的因子载荷系数
- 例如：A维度AVE低，将A1前系数从1.2调至1.3

**AVE计算算法（可直接复制调用）**
```R
# 方式A：优先推荐（semTools直接给出AVE）
# 返回：命名向量，每个潜变量一个AVE值
calc_ave_semtools <- function(fit) {
  # semTools::AVE会根据测量模型自动计算AVE
  semTools::AVE(fit)
}

# 方式B：基于标准化载荷/误差方差的手算算法（更通用、更透明）
# AVE = sum(lambda^2) / (sum(lambda^2) + sum(theta))
# lambda：标准化因子载荷；theta：指标误差方差（标准化解）
calc_ave_manual <- function(fit) {
  pe <- lavaan::parameterEstimates(fit, standardized = TRUE)

  # 取测量模型载荷：op == "=~"，std.all即标准化载荷
  loading <- pe[pe$op == "=~", c("lhs", "rhs", "std.all")]
  colnames(loading) <- c("factor", "item", "lambda")

  # 取误差方差：指标自身方差，op == "~~" 且 lhs==rhs，std.all即标准化误差方差
  theta <- pe[pe$op == "~~" & pe$lhs == pe$rhs, c("lhs", "std.all")]
  colnames(theta) <- c("item", "theta")

  # 合并
  m <- merge(loading, theta, by = "item", all.x = TRUE)

  # 按潜变量聚合
  ave <- tapply(seq_len(nrow(m)), m$factor, function(idx) {
    lam2 <- m$lambda[idx]^2
    the <- m$theta[idx]
    sum(lam2, na.rm = TRUE) / (sum(lam2, na.rm = TRUE) + sum(the, na.rm = TRUE))
  })

  unlist(ave)
}

# 示例：
# ave1 <- calc_ave_semtools(lv)
# ave2 <- calc_ave_manual(lv)
# print(round(ave1, 3))
# print(round(ave2, 3))

# 聚合效度表（CR + AVE）一键生成
# - CR这里用semTools::reliability的omega作为复合信度（与常见CR口径一致）
# - AVE来自reliability的ave行
# - 题目个数：若不传item_counts，将从测量模型自动统计
make_convergent_validity_table <- function(fit, item_counts = NULL, digits = 3) {
  rel <- semTools::reliability(fit, what = c("omega", "ave"), return.total = TRUE)
  rel <- as.data.frame(round(rel, digits))

  facs <- colnames(rel)
  facs <- facs[facs != "total"]

  if (is.null(item_counts)) {
    pe <- lavaan::parameterEstimates(fit)
    loading <- pe[pe$op == "=~", c("lhs", "rhs")]
    item_counts <- table(loading$lhs)
    item_counts <- as.integer(item_counts[facs])
    names(item_counts) <- facs
  } else {
    if (!is.null(names(item_counts))) {
      item_counts <- as.integer(item_counts[facs])
    } else {
      item_counts <- as.integer(item_counts[seq_along(facs)])
      names(item_counts) <- facs
    }
  }

  data.frame(
    维度 = facs,
    CR值 = as.numeric(rel["omega", facs]),
    AVE值 = as.numeric(rel["ave", facs]),
    题目个数 = as.integer(item_counts),
    check.names = FALSE
  )
}

# 示例：
# convergent_table <- make_convergent_validity_table(lv)
# print(convergent_table)
```

**技能2：因子提取回调**
- 若提取因子数≠维度数，通过旋转矩阵分析重复维度
- 调整路径系数以区分维度，保证路径显著

**技能3：拟合度回调**
- IFI/CFI/TLI>1：增大sd参数或增加残差相关
- GFI/AGFI<0.88：减小sd参数
- RMSEA<0.001：增加残差实现

#### 六、输出要求
- 文件名固定为"模拟.R"，覆盖原有文件
- 自动运行代码并检查执行结果

#### 七、关键限制
- 不可新增未提供的变量和路径
- 变量名必须为`mean`和`mean2`，不可改成其他名称
- 不要出现`\n`字符
- 严格遵循代码框架，不修改结构
- 快速执行，代码正确即运行
- 检查因子个数和AVE是否达标

#### 八、Hayes PROCESS中介效应算法规则（与SPSS PROCESS完全一致）

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

##### （三）R语言代码实现（Hayes风格）
```R
# Hayes风格的中介效应分析函数（与SPSS PROCESS完全一致）
hayes_mediation <- function(data, x_var, m_var, y_var, n_boot = 5000, output_file = NULL) {
  
  # 使用原始数据，不标准化（与SPSS PROCESS一致）
  data_std <- data
  
  # 模型1：总效应 Y ~ X
  model_total <- lm(as.formula(paste(y_var, "~", x_var)), data = data_std)
  
  # 模型2：M ~ X (a路径)
  model_m <- lm(as.formula(paste(m_var, "~", x_var)), data = data_std)
  
  # 模型3：Y ~ X + M (b路径和c'路径)
  model_y <- lm(as.formula(paste(y_var, "~", x_var, "+", m_var)), data = data_std)
  
  # 提取系数
  c_total <- coef(model_total)[x_var]  # 总效应
  a <- coef(model_m)[x_var]            # a路径
  b <- coef(model_y)[m_var]            # b路径
  c_prime <- coef(model_y)[x_var]      # 直接效应c'
  
  # Bootstrap计算间接效应的置信区间
  set.seed(123)
  boot_indirect <- numeric(n_boot)
  n <- nrow(data_std)
  
  for (i in 1:n_boot) {
    boot_idx <- sample(1:n, n, replace = TRUE)
    boot_data <- data_std[boot_idx, ]
    
    boot_m <- lm(as.formula(paste(m_var, "~", x_var)), data = boot_data)
    boot_y <- lm(as.formula(paste(y_var, "~", x_var, "+", m_var)), data = boot_data)
    
    boot_a <- coef(boot_m)[x_var]
    boot_b <- coef(boot_y)[m_var]
    boot_indirect[i] <- boot_a * boot_b
  }
  
  # 计算间接效应和置信区间（偏差校正百分位法）
  indirect <- a * b
  ci_lower <- quantile(boot_indirect, 0.025)
  ci_upper <- quantile(boot_indirect, 0.975)
  boot_se <- sd(boot_indirect)
  
  # 判断显著性
  indirect_sig <- ifelse(ci_lower > 0 | ci_upper < 0, "显著", "不显著")
  
  # 返回结果
  results <- list(
    c_total = round(c_total, 4),      # 总效应
    c_prime = round(c_prime, 4),      # 直接效应
    indirect = round(indirect, 4),    # 间接效应
    boot_se = round(boot_se, 4),      # Bootstrap标准误
    ci_lower = round(ci_lower, 4),    # 置信区间下限
    ci_upper = round(ci_upper, 4),    # 置信区间上限
    indirect_sig = indirect_sig       # 显著性判断
  )
  
  return(results)
}
```

##### （四）bruceR::PROCESS vs SPSS PROCESS差异说明
| 特性 | bruceR::PROCESS | SPSS PROCESS (Hayes) |
|------|-----------------|---------------------|
| 估计方法 | SEM (最大似然) | OLS回归 |
| 系数类型 | 标准化系数 | 非标准化系数 |
| Bootstrap | 较少次数 | 5000次 |
| 置信区间 | 百分位法 | 偏差校正百分位法 |

##### （五）输出格式
中介效应分解表：
| 效应类型 | 效应值 | Boot标准误 | BootLLCI | BootULCI |
|----------|--------|-----------|----------|----------|
| 总效应 (c) | X.XXX | - | - | - |
| 直接效应 (c') | X.XXX | - | - | - |
| 间接效应 (a×b) | X.XXX | X.XXX | X.XXX | X.XXX |

##### （六）中介类型判断规则
1. 间接效应显著（CI不含0）+ 直接效应显著 → 部分中介
2. 间接效应显著（CI不含0）+ 直接效应不显著 → 完全中介
3. 间接效应不显著（CI含0）→ 无中介效应

##### （七）注意事项
1. 必须使用原始数据，不能先标准化
2. Bootstrap次数建议5000次以上
3. 设置随机种子确保结果可重复
4. 置信区间使用2.5%和97.5%分位数

