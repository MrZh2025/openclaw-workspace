### 角色1：Amos数据模拟（R语言）

---

## 一、核心任务

根据用户提供的中文变量名称及题目数量，模拟结构方程模型数据，生成"模拟.R"文件并自动运行。

---

## 二、变量命名规则

| 规则 | 示例 |
|------|------|
| 中文变量用A、B、C、D等前缀+数字表示题目 | "现状认知4题" → A1-A4 |
| 含字母"E"的变量替换为"EE" | E1 → EE1 |
| 维度名称可用中文（如用户要求） | 维度名：现状认知，题目：A1-A4 |

---

## 三、模型参数设置

| 参数类型 | 取值范围 | 说明 |
|----------|----------|------|
| 因子载荷系数 | 0.9-2.5 | 各题目需存在差异 |
| 回归系数 | 0.2-0.6 | 正负向根据路径设定 |
| 自变量相关性 | <0.25 | 通过"~~"建立（如A~~0.24*B） |
| SEM估计方式 | std.lv=FALSE | 与AMOS一致，固定首个指标载荷为1 |
| 中介效应分析 | bruceR::PROCESS() | 支持简单/多重/有调节的中介 |

---

## 四、数据处理标准

- **样本量**：默认345条（可调整）
- **数据离散化**：标准化后切割为1-5分制或1-7分制
- **输出格式**：.sav、.xlsx、.dat

---

## 五、代码框架模板

### 5.1 初始化设置
```R
options(warn=-1)

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
if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)

```

### 5.2 辅助函数
```R
# ========== 创建标准化docx表格 ==========
create_docx_table <- function(data, title = NULL, note = NULL, digits = 3, col_to_format = NULL) {
  doc <- read_docx()
  ft <- flextable(data, theme_fun = theme_booktabs)
  if (!is.null(col_to_format)) ft <- colformat_double(ft, j = col_to_format, digits = digits)
  ft <- autofit(ft)
  if (!is.null(title)) doc <- body_add_par(doc, title, style = "heading 2")
  doc <- body_add_flextable(doc, ft)
  if (!is.null(note)) doc <- body_add_par(doc, note, style = "Normal")
  return(doc)
}

# ========== 显著性标记函数 ==========
add_sig_stars <- function(p) {
  ifelse(p < 0.001, "***", ifelse(p < 0.01, "**", ifelse(p < 0.05, "*", "")))
}

format_p <- function(p) {
  ifelse(p < 0.001, "< .001", round(p, 3))
}
```

### 5.3 AVE自动调参函数（核心回调）
```R
# ========== AVE自动调参函数 ==========
check_and_adjust_ave <- function(base_loadings, sim_model_template, fit_model, 
                                  sample_size = 345, max_iter = 10, step = 0.15) {
  current_loadings <- base_loadings
  
  for (iter in 1:max_iter) {
    cat(sprintf("\n[AVE调参] 迭代 %d/%d\n", iter, max_iter))
    
    # 动态生成模型（替换载荷参数）
    model <- sim_model_template
    for (name in names(current_loadings)) {
      model <- gsub(paste0("\\{\\{", name, "\\}\\}"), current_loadings[name], model)
    }
    
    tryCatch({
      # 模拟数据
      sim_data <- simulateData(model = model, sample.nobs = sample_size)
      tammodel.norm <- sim_data - rnorm(length(unlist(sim_data)), mean = 0, sd = 0.4)
      spss <- data.frame(lapply(tammodel.norm, function(X) {
        x_cut <- cut(X, breaks = 6, labels = FALSE)
        ifelse(x_cut > 5, 5, x_cut)
      }))
      
      # 拟合SEM
      lv <- sem(model = fit_model, data = spss, std.lv = FALSE)
      ave_values <- AVE(lv)
      
      cat("当前AVE值:\n")
      print(round(ave_values, 3))
      
      # 检查是否全部达标
      if (all(ave_values >= 0.5)) {
        cat("[成功] 所有AVE值均>=0.5\n")
        return(list(loadings = current_loadings, spss = spss, lv = lv, success = TRUE))
      }
      
      # 调整未达标维度的载荷
      for (dim_name in names(ave_values)) {
        if (ave_values[dim_name] < 0.5) {
          dim_items <- grep(paste0("^", dim_name, "_"), names(current_loadings), value = TRUE)
          if (length(dim_items) == 0) {
            dim_items <- grep(paste0("^", dim_name), names(current_loadings), value = TRUE)
          }
          current_loadings[dim_items] <- current_loadings[dim_items] + step
          cat(sprintf("[调整] 维度 %s 载荷 +%.2f\n", dim_name, step))
        }
      }
      
    }, error = function(e) {
      cat(sprintf("[错误] 迭代 %d: %s\n", iter, e$message))
      current_loadings <- current_loadings + 0.1
    })
  }
  
  cat("[警告] 达到最大迭代次数，使用当前参数\n")
  return(list(loadings = current_loadings, spss = NULL, lv = NULL, success = FALSE))
}
```

### 5.4 拟合度回调函数
```R
# ========== 拟合度检查与回调 ==========
check_and_adjust_fit <- function(lv, spss, fit_model, sd_param = 0.4, max_iter = 5) {
  
  for (iter in 1:max_iter) {
    fit_indices <- fitmeasures(lv, c("gfi", "agfi", "cfi", "tli", "ifi", "rmsea"))
    
    cat(sprintf("\n[拟合度检查] 迭代 %d\n", iter))
    print(round(fit_indices, 3))
    
    # 检查是否达标
    gfi_ok <- fit_indices["gfi"] >= 0.88
    cfi_ok <- fit_indices["cfi"] <= 1 && fit_indices["cfi"] >= 0.9
    tli_ok <- fit_indices["tli"] <= 1 && fit_indices["tli"] >= 0.9
    
    if (gfi_ok && cfi_ok && tli_ok) {
      cat("[成功] 拟合度指标达标\n")
      return(list(lv = lv, spss = spss, sd_param = sd_param))
    }
    
    # 调整策略
    if (fit_indices["cfi"] > 1 || fit_indices["tli"] > 1 || fit_indices["ifi"] > 1) {
      sd_param <- sd_param + 0.1
      cat(sprintf("[调整] CFI/TLI/IFI>1，增大sd参数至 %.2f\n", sd_param))
    }
    
    if (fit_indices["gfi"] < 0.88 || fit_indices["agfi"] < 0.88) {
      sd_param <- sd_param - 0.05
      cat(sprintf("[调整] GFI/AGFI<0.88，减小sd参数至 %.2f\n", sd_param))
    }
    
    # 重新模拟数据
    sim_data <- simulateData(model = model, sample.nobs = nrow(spss))
    tammodel.norm <- sim_data - rnorm(length(unlist(sim_data)), mean = 0, sd = sd_param)
    spss <- data.frame(lapply(tammodel.norm, function(X) {
      x_cut <- cut(X, breaks = 6, labels = FALSE)
      ifelse(x_cut > 5, 5, x_cut)
    }))
    
    lv <- sem(model = fit_model, data = spss, std.lv = FALSE)
  }
  
  cat("[警告] 拟合度调整达到最大次数\n")
  return(list(lv = lv, spss = spss, sd_param = sd_param))
}
```

### 5.5 数据模拟主流程
```R
# ========== 数据模拟 ==========
set.seed(1)
N <- {{SAMPLE_SIZE}}  # 样本量，默认345

# 初始载荷参数（根据实际变量填充）
base_loadings <- c(
  A1 = 1.2, A2 = 1.4, A3 = 1.3, A4 = 1.5,  # 维度A
  B1 = 1.3, B2 = 1.5, B3 = 1.4,            # 维度B
  C1 = 1.4, C2 = 1.2, C3 = 1.6             # 维度C
  # ... 根据实际变量添加
)

# 模拟模型模板（占位符会被替换）
sim_model_template <- "
# 因子结构
A =~ {{A1}}*A1 + {{A2}}*A2 + {{A3}}*A3 + {{A4}}*A4
B =~ {{B1}}*B1 + {{B2}}*B2 + {{B3}}*B3
C =~ {{C1}}*C1 + {{C2}}*C2 + {{C3}}*C3

# 回归路径
C ~ 0.4*A + 0.3*B

# 自变量相关性
A ~~ 0.2*B
"

# SEM拟合模型
fit_model <- "
A =~ A1 + A2 + A3 + A4
B =~ B1 + B2 + B3
C =~ C1 + C2 + C3
C ~ A + B
A ~~ B
"

# 执行AVE自动调参
result <- check_and_adjust_ave(base_loadings, sim_model_template, fit_model, N)

if (result$success) {
  spss <- result$spss
  lv <- result$lv
} else {
  # 使用最终参数重新模拟
  # ...
}

# 计算各维度均值
mean <- data.frame(
  A = rowMeans(spss[, c("A1", "A2", "A3", "A4")]),
  B = rowMeans(spss[, c("B1", "B2", "B3")]),
  C = rowMeans(spss[, c("C1", "C2", "C3")])
)
names(mean) <- c("维度A", "维度B", "维度C")  # 可用中文命名

cat("\n========== 数据模拟完成 ==========\n")
cat(sprintf("样本量: %d | 变量数: %d | 维度数: %d\n", N, ncol(spss), ncol(mean)))
```

### 5.6 输出分析结果
```R
# ========== 1. 相关分析（下三角格式） ==========
cor_result <- corr.test(mean, adjust = "none")
cor_matrix <- round(cor_result$r, 3)
p_matrix <- cor_result$p

# 构建下三角显示矩阵
cor_display <- matrix("", nrow(cor_matrix), ncol(cor_matrix))
for (i in 1:nrow(cor_matrix)) {
  for (j in 1:ncol(cor_matrix)) {
    if (i > j) {
      cor_display[i, j] <- paste0(cor_matrix[i, j], add_sig_stars(p_matrix[i, j]))
    } else if (i == j) {
      cor_display[i, j] <- "1.00"
    }
  }
}

cor_df <- data.frame(
  变量 = colnames(mean),
  均值 = round(colMeans(mean), 3),
  标准差 = round(apply(mean, 2, sd), 3),
  cor_display,
  check.names = FALSE
)
colnames(cor_df)[4:ncol(cor_df)] <- colnames(mean)

doc <- create_docx_table(cor_df, 
  title = "相关系数矩阵（下三角）",
  note = "注：*** p < 0.001, ** p < 0.01, * p < 0.05")
print(doc, target = file.path(output_dir, "相关.docx"))

# ========== 2. CFA因子载荷表（与AMOS一致） ==========
cfa_params <- parameterEstimates(lv, standardized = TRUE)
cfa_loadings <- cfa_params[cfa_params$op == "=~", ]

cfa_table <- data.frame(
  潜变量 = cfa_loadings$lhs,
  题目 = cfa_loadings$rhs,
  非标准化载荷 = round(cfa_loadings$est, 3),
  标准误 = round(cfa_loadings$se, 3),
  Z值 = round(cfa_loadings$z, 3),
  P值 = format_p(cfa_loadings$pvalue),
  标准化载荷 = round(cfa_loadings$std.all, 3),
  显著性 = add_sig_stars(cfa_loadings$pvalue)
)

doc <- create_docx_table(cfa_table, 
  title = "CFA因子载荷表（与AMOS对比）",
  note = "注：标准化载荷对应AMOS的Standardized Regression Weights")
print(doc, target = file.path(output_dir, "CFA因子载荷表.docx"))

# ========== 3. 潜变量相关性表（与AMOS Correlations一致） ==========
latent_vars <- unique(cfa_loadings$lhs)
cfa_covs <- cfa_params[cfa_params$op == "~~" & 
                        cfa_params$lhs != cfa_params$rhs &
                        cfa_params$lhs %in% latent_vars & 
                        cfa_params$rhs %in% latent_vars, ]

if (nrow(cfa_covs) > 0) {
  cov_table <- data.frame(
    相关路径 = paste(cfa_covs$lhs, "<-->", cfa_covs$rhs),
    协方差估计 = round(cfa_covs$est, 3),
    标准误 = round(cfa_covs$se, 3),
    Z值 = round(cfa_covs$z, 3),
    P值 = format_p(cfa_covs$pvalue),
    相关系数 = round(cfa_covs$std.all, 3),
    显著性 = add_sig_stars(cfa_covs$pvalue)
  )
  
  doc <- create_docx_table(cov_table, 
    title = "潜变量相关性表（与AMOS对比）",
    note = "注：相关系数对应AMOS的Correlations")
  print(doc, target = file.path(output_dir, "潜变量相关性表.docx"))
}

# ========== 4. 路径系数表 ==========
regressions <- cfa_params[cfa_params$op == "~", ]

path_table <- data.frame(
  路径 = paste(regressions$lhs, "←", regressions$rhs),
  非标准化系数 = round(regressions$est, 3),
  标准误 = round(regressions$se, 3),
  Z值 = round(regressions$z, 3),
  P值 = format_p(regressions$pvalue),
  标准化系数 = round(regressions$std.all, 3),
  显著性 = add_sig_stars(regressions$pvalue)
)

doc <- create_docx_table(path_table, 
  title = "路径系数表", 
  note = "注：*** p < 0.001, ** p < 0.01, * p < 0.05")
print(doc, target = file.path(output_dir, "路径系数表.docx"))
```

```R
# ========== 5. 模型拟合度表 ==========
MR <- round(fitmeasures(lv, c("GFI", "AGFI", "RMR", "RMSEA", "NFI", "IFI", "CFI", "TLI")), 3)
chisq <- round(fitmeasures(lv, "chisq"), 3)
df_model <- fitmeasures(lv, "df")
chisq_df <- round(chisq / df_model, 3)

fit_table <- data.frame(
  拟合指标 = c("χ²", "df", "χ²/df", "GFI", "AGFI", "RMR", "RMSEA", "NFI", "IFI", "CFI", "TLI"),
  释义 = c("卡方值", "自由度", "卡方自由度比", "拟合优度指数", "调整后拟合优度指数",
           "残差均方根", "近似误差均方根", "规范拟合指数", "修正拟合指数", "比较拟合指数", "TL指数"),
  合理范围 = c("—", "—", "<3良好；<5合理", 
               rep(">0.9良好；>0.8合理", 2),
               rep("<0.05良好；<0.08合理", 2),
               rep(">0.9良好；>0.8合理", 4)),
  结果 = c(chisq, df_model, chisq_df, MR),
  评定 = c("—", "—", ifelse(chisq_df < 3, "良好", ifelse(chisq_df < 5, "合理", "较差")),
           ifelse(MR["GFI"] > 0.9, "良好", ifelse(MR["GFI"] > 0.8, "合理", "较差")),
           ifelse(MR["AGFI"] > 0.9, "良好", ifelse(MR["AGFI"] > 0.8, "合理", "较差")),
           ifelse(MR["RMR"] < 0.05, "良好", ifelse(MR["RMR"] < 0.08, "合理", "较差")),
           ifelse(MR["RMSEA"] < 0.05, "良好", ifelse(MR["RMSEA"] < 0.08, "合理", "较差")),
           ifelse(MR["NFI"] > 0.9, "良好", ifelse(MR["NFI"] > 0.8, "合理", "较差")),
           ifelse(MR["IFI"] > 0.9, "良好", ifelse(MR["IFI"] > 0.8, "合理", "较差")),
           ifelse(MR["CFI"] > 0.9, "良好", ifelse(MR["CFI"] > 0.8, "合理", "较差")),
           ifelse(MR["TLI"] > 0.9, "良好", ifelse(MR["TLI"] > 0.8, "合理", "较差")))
)

doc <- create_docx_table(fit_table, title = "模型拟合度表")
doc <- body_add_par(doc, "参考：Medsker et al.(1994)；侯杰秦等(2004)")
print(doc, target = file.path(output_dir, "模型拟合度.docx"))

# ========== 6. 信度检验表（含AVE） ==========
rel_data <- round(reliability(lv, what = c("alpha", "omega", "ave"), return.total = TRUE), 3)
rel_df <- as.data.frame(rel_data)

dims <- names(mean)
item_counts <- c(4, 3, 3)  # 根据实际填写

reliability_table <- data.frame(
  维度 = c(dims, "总量表"),
  Cronbach_α = as.numeric(rel_df["alpha", ]),
  AVE值 = c(as.numeric(rel_df["ave", 1:length(dims)]), NA),
  题目数 = c(item_counts, sum(item_counts))
)

doc <- create_docx_table(reliability_table, 
  title = "信度检验表",
  note = "注：AVE≥0.5表示收敛效度良好",
  col_to_format = c(2, 3))
print(doc, target = file.path(output_dir, "信度检验表.docx"))

# ========== 7. 聚合效度表（CR+AVE） ==========
convergent_table <- data.frame(
  维度 = dims,
  CR值 = as.numeric(rel_df["omega", 1:length(dims)]),
  AVE值 = as.numeric(rel_df["ave", 1:length(dims)]),
  题目数 = item_counts
)

doc <- create_docx_table(convergent_table, 
  title = "聚合效度表",
  note = "注：CR≥0.7、AVE≥0.5表示聚合效度良好")
print(doc, target = file.path(output_dir, "聚合效度表.docx"))

# ========== 8. 区分效度表（下三角） ==========
cor_lv <- round(lavInspect(lv, "cor.lv"), 3)
diag(cor_lv) <- round(sqrt(AVE(lv)), 3)
cor_lv[upper.tri(cor_lv)] <- NA

validity_df <- data.frame(维度 = dims, cor_lv, check.names = FALSE)
validity_df[is.na(validity_df)] <- ""

doc <- create_docx_table(validity_df, 
  title = "区分效度表（下三角）",
  note = "注：对角线为AVE平方根，下三角为潜变量相关系数")
print(doc, target = file.path(output_dir, "区分效度表.docx"))

# ========== 9. 保存数据文件 ==========
write_sav(mean, file.path(output_dir, "均值.sav"))
write_sav(as.data.frame(spss), file.path(output_dir, "数据.sav"))
write.xlsx(as.data.frame(spss), file.path(output_dir, "数据.xlsx"))
write.table(spss, file.path(output_dir, "mplus.dat"), row.names = FALSE, col.names = FALSE)

cat("\n========== 数据文件已保存 ==========\n")
```

### 5.7 因子分析与KMO检验
```R
# ========== 10. 探索性因子分析 ==========
fa <- EFA(spss, vars = names(spss), method = "pca", rotation = "varimax", 
          sort.loadings = FALSE, plot.scree = FALSE, hide.loadings = 0.5)

# 因子载荷矩阵
loadings_df <- as.data.frame(unclass(fa$loadings))
loadings_df$共同度 <- round(fa$communality, 3)
loadings_df <- round(loadings_df, 3)

# 小于0.5的载荷设为空
for (j in 1:(ncol(loadings_df)-1)) {
  loadings_df[abs(loadings_df[, j]) < 0.5, j] <- ""
}

loadings_df <- data.frame(题目 = rownames(loadings_df), loadings_df, row.names = NULL)

doc <- create_docx_table(loadings_df, title = "因子载荷矩阵（旋转后）")
doc <- body_add_par(doc, "提取方法：主成分分析 | 旋转方法：最大方差法")
print(doc, target = file.path(output_dir, "因子载荷值.docx"))

# 方差解释率
variance_df <- round(as.data.frame(fa$eigenvalues), 3)
colnames(variance_df) <- c("特征值", "方差%", "累积%", "提取特征值", "提取方差%", "提取累积%")
variance_df[is.na(variance_df)] <- ""

doc <- create_docx_table(variance_df, title = "方差解释率")
print(doc, target = file.path(output_dir, "方差提取率.docx"))

# ========== 11. KMO和巴特利特检验 ==========
kmo <- KMO(spss)
bartlett <- cortest.bartlett(cor(spss), n = nrow(spss))

kmo_table <- data.frame(
  检验项目 = c("KMO取样适切性", "巴特利特球形检验-近似卡方", "巴特利特球形检验-自由度", "巴特利特球形检验-显著性"),
  结果 = c(round(kmo$MSA, 3), round(bartlett$chisq, 3), bartlett$df, 
           ifelse(bartlett$p.value < 0.001, "<.001", round(bartlett$p.value, 3)))
)

doc <- create_docx_table(kmo_table, title = "KMO和巴特利特检验")
print(doc, target = file.path(output_dir, "KMO分析.docx"))

# 因子个数检查
eigen_vals <- eigen(cor(spss))$values
n_factors <- sum(eigen_vals > 1)
cat(sprintf("\n[因子检查] 特征值>1的因子数: %d | 预期维度数: %d\n", n_factors, length(dims)))
```

### 5.8 中介效应分析（PROCESS）
```R
# ========== 12. 中介效应分析 ==========
cat("\n========== 中介效应分析 ==========\n")

# 简单中介：X → M → Y
PROCESS(data = mean, 
        x = "{{IV_NAME}}",      # 自变量
        meds = "{{MED_NAME}}",  # 中介变量
        y = "{{DV_NAME}}",      # 因变量
        std = TRUE, 
        file = file.path(output_dir, "中介效应分析.doc"))

# 调节效应（可选）
# PROCESS(data = mean, x = "X", y = "Y", mod = "W", std = TRUE, 
#         file = file.path(output_dir, "调节效应分析.doc"))

# 有调节的中介（可选）
# PROCESS(data = mean, x = "X", meds = "M", y = "Y", mod = "W", mod.path = "x-m",
#         std = TRUE, file = file.path(output_dir, "有调节的中介分析.doc"))

cat("\n========== 所有分析完成 ==========\n")
```

---

## 六、回调技能详解

### 6.1 AVE自动调参（强制执行）

| 触发条件 | 调整策略 | 步长 |
|----------|----------|------|
| 某维度AVE < 0.5 | 该维度所有题目载荷+0.15 | +0.15 |
| 最大迭代10次 | 使用当前最优参数 | - |

**AVE计算公式**：
```
AVE = Σ(λ²) / [Σ(λ²) + Σ(θ)]
λ = 标准化因子载荷
θ = 指标误差方差
```

### 6.2 因子提取回调

| 触发条件 | 调整策略 |
|----------|----------|
| 提取因子数 ≠ 维度数 | 分析旋转矩阵，调整路径系数区分维度 |
| 交叉载荷过高 | 增大维度间路径系数差异 |

### 6.3 拟合度回调

| 指标异常 | 调整策略 |
|----------|----------|
| CFI/TLI/IFI > 1 | 增大sd参数（+0.1） |
| GFI/AGFI < 0.88 | 减小sd参数（-0.05）或增加样本量 |
| RMSEA < 0.001 | 增加残差项 |

---

## 七、输出文件清单

| 文件名 | 内容 | 必须输出 |
|--------|------|----------|
| 相关.docx | 相关系数矩阵（下三角） | ✓ |
| CFA因子载荷表.docx | 标准化/非标准化载荷 | ✓ |
| 潜变量相关性表.docx | 潜变量协方差和相关 | ✓ |
| 路径系数表.docx | 回归路径系数 | ✓ |
| 模型拟合度.docx | 拟合指标汇总 | ✓ |
| 信度检验表.docx | α系数和AVE值 | ✓ |
| 聚合效度表.docx | CR和AVE值 | ✓ |
| 区分效度表.docx | AVE平方根与相关 | ✓ |
| 因子载荷值.docx | 旋转后因子载荷 | ✓ |
| 方差提取率.docx | 方差解释率 | ✓ |
| KMO分析.docx | KMO和巴特利特检验 | ✓ |
| 中介效应分析.doc | PROCESS分析结果 | 按需 |
| 均值.sav | 维度均值数据 | ✓ |
| 数据.sav/.xlsx | 原始模拟数据 | ✓ |
| mplus.dat | Mplus格式数据 | ✓ |

---

## 八、关键限制（必须遵守）

1. **变量名必须为`mean`**，不可写成`mean_data`
2. **SEM估计必须使用`std.lv=FALSE`**，与AMOS保持一致
3. **不可新增未提供的变量和路径**
4. **不要出现`\n`字符**
5. **文件名固定为"模拟.R"**，覆盖原有文件
6. **自动运行代码并检查执行结果**
7. **负向系数写法**：`A ~ (-0.4)*B`
8. **信度检验表必须包含AVE值列**

---

## 九、中介效应分析规范

### 9.1 bruceR::PROCESS 使用方法

| 模型类型 | 代码示例 |
|----------|----------|
| 简单中介 | `PROCESS(data=mean, x="X", meds="M", y="Y", std=TRUE)` |
| 多重中介 | `PROCESS(data=mean, x="X", meds=c("M1","M2"), y="Y", std=TRUE)` |
| 调节效应 | `PROCESS(data=mean, x="X", y="Y", mod="W", std=TRUE)` |
| 有调节的中介 | `PROCESS(data=mean, x="X", meds="M", y="Y", mod="W", mod.path="x-m", std=TRUE)` |

**参数说明**：
- `mod.path`: "x-m"调节前半段，"m-y"调节后半段，"x-y"调节直接效应

### 9.2 Hayes PROCESS算法（与SPSS一致）

**核心原则**：
1. 使用OLS回归（非SEM最大似然估计）
2. 使用非标准化系数
3. Bootstrap 5000次
4. 偏差校正百分位法计算95%CI

**算法步骤**：
```
步骤1：建立回归模型
  模型1（总效应）：Y ~ X → 得到c
  模型2（a路径）：M ~ X → 得到a
  模型3（直接效应）：Y ~ X + M → 得到c'和b

步骤2：计算间接效应
  间接效应 = a × b

步骤3：Bootstrap置信区间
  重复5000次有放回抽样
  BootLLCI = 2.5%分位数
  BootULCI = 97.5%分位数

步骤4：判断中介效应
  CI不含0 → 间接效应显著
  c'显著 → 部分中介
  c'不显著 → 完全中介
```

### 9.3 Hayes风格R代码实现
```R
hayes_mediation <- function(data, x_var, m_var, y_var, n_boot = 5000) {
  
  # 三个回归模型
  model_total <- lm(as.formula(paste(y_var, "~", x_var)), data = data)
  model_m <- lm(as.formula(paste(m_var, "~", x_var)), data = data)
  model_y <- lm(as.formula(paste(y_var, "~", x_var, "+", m_var)), data = data)
  
  # 提取系数
  c_total <- coef(model_total)[x_var]
  a <- coef(model_m)[x_var]
  b <- coef(model_y)[m_var]
  c_prime <- coef(model_y)[x_var]
  indirect <- a * b
  
  # Bootstrap
  set.seed(123)
  boot_indirect <- replicate(n_boot, {
    idx <- sample(nrow(data), replace = TRUE)
    boot_data <- data[idx, ]
    boot_a <- coef(lm(as.formula(paste(m_var, "~", x_var)), data = boot_data))[x_var]
    boot_b <- coef(lm(as.formula(paste(y_var, "~", x_var, "+", m_var)), data = boot_data))[m_var]
    boot_a * boot_b
  })
  
  list(
    总效应 = round(c_total, 4),
    直接效应 = round(c_prime, 4),
    间接效应 = round(indirect, 4),
    BootSE = round(sd(boot_indirect), 4),
    BootLLCI = round(quantile(boot_indirect, 0.025), 4),
    BootULCI = round(quantile(boot_indirect, 0.975), 4),
    显著性 = ifelse(quantile(boot_indirect, 0.025) > 0 | quantile(boot_indirect, 0.975) < 0, "显著", "不显著")
  )
}
```

### 9.4 中介效应输出格式

| 效应类型 | 效应值 | Boot标准误 | BootLLCI | BootULCI |
|----------|--------|-----------|----------|----------|
| 总效应(c) | X.XXX | - | - | - |
| 直接效应(c') | X.XXX | - | - | - |
| 间接效应(a×b) | X.XXX | X.XXX | X.XXX | X.XXX |

### 9.5 中介类型判断

| 条件 | 结论 |
|------|------|
| 间接效应CI不含0 + 直接效应显著 | 部分中介 |
| 间接效应CI不含0 + 直接效应不显著 | 完全中介 |
| 间接效应CI含0 | 无中介效应 |

---

## 十、占位符说明

在代码模板中使用以下占位符，生成代码时需替换：

| 占位符 | 说明 | 示例 |
|--------|------|------|
| `{{SAMPLE_SIZE}}` | 样本量 | 345 |
| `{{A1}}`, `{{A2}}` | 各题目载荷参数 | 1.2, 1.4 |
| `{{IV_NAME}}` | 自变量名称 | "维度A" |
| `{{MED_NAME}}` | 中介变量名称 | "维度B" |
| `{{DV_NAME}}` | 因变量名称 | "维度C" |
| `{{NUM_DIMS}}` | 维度数量 | 3 |
| `{{DIMS_LIST}}` | 维度前缀列表 | "A", "B", "C" |
| `{{ITEM_COUNTS}}` | 各维度题目数 | 4, 3, 3 |

---

## 十一、快速检查清单

执行完成后检查：

- [ ] AVE值是否全部≥0.5
- [ ] 因子提取数是否等于维度数
- [ ] 拟合度指标是否达标（1>CFI/TLI>0.9, RMSEA<0.08）
- [ ] 信度检验表是否包含AVE列
- [ ] CFA因子载荷表.docx是否输出
- [ ] 潜变量相关性表.docx是否输出
- [ ] 数据文件（.sav, .xlsx, .dat）是否保存
