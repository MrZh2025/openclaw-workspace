# 生成中介模型分析报告
library(officer)
library(flextable)
library(lavaan)
library(psych)
library(haven)

# 读取数据
mean <- read_sav("C:/Users/Mr Zhou/.openclaw/workspace/分析结果/中介模型数据.sav")

# 运行模型
model <- '
  X =~ A1 + A2 + A3 + A4
  M =~ B1 + B2 + B3 + B4
  Y =~ C1 + C2 + C3 + C4
  M ~ a*X
  Y ~ b*M + c*X
'
fit <- sem(model, data = mean, std.lv = FALSE, estimator = "MLR")
param <- parameterEstimates(fit, standardized = TRUE)

# ============ 创建 Word 文档 ============
doc <- read_docx()

# 标题
doc <- body_add_par(doc, "中介模型分析报告（X->M->Y）", style = "heading 1")
doc <- body_add_par(doc, "", style = "Normal")

# 1. 样本说明
doc <- body_add_par(doc, "一、样本说明", style = "heading 2")
doc <- body_add_par(doc, paste0("本研究模拟数据共 ", nrow(mean), " 份样本，包含 3 个潜变量（X、M、Y），每个潜变量由 4 个观测题目测量，共计 12 个观测变量。"), style = "Normal")
doc <- body_add_par(doc, "", style = "Normal")

# 2. 相关系数矩阵
doc <- body_add_par(doc, "二、相关系数矩阵", style = "heading 2")
cor_matrix <- cor(mean)
ft_cor <- flextable(as.data.frame(round(cor_matrix, 3)))
ft_cor <- theme_tron(ft_cor)
ft_cor <- set_table_properties(ft_cor, layout = "autofit")
doc <- body_add_flextable(doc, ft_cor)
doc <- body_add_par(doc, "", style = "Normal")

# 3. CFA 因子载荷表
doc <- body_add_par(doc, "三、验证性因子分析结果", style = "heading 2")
loading_data <- param[param$op == "=~", c("lhs", "rhs", "est", "std.all")]
loading_data <- loading_data[loading_data$rhs != "1", ]
names(loading_data) <- c("Latent", "Item", "Unstd", "Std")
ft_loading <- flextable(loading_data)
ft_loading <- theme_tron(ft_loading)
ft_loading <- set_table_properties(ft_loading, layout = "autofit")
doc <- body_add_flextable(doc, ft_loading)
doc <- body_add_par(doc, "", style = "Normal")

# 4. 模型拟合度表
doc <- body_add_par(doc, "四、模型拟合度指标", style = "heading 2")
fit_measures <- fitMeasures(fit, c("chisq", "df", "pvalue", "cfi", "tli", "rmsea", "srmr", "gfi", "agfi"))
fit_df <- data.frame(
  Measure = c("Chi-square", "df", "p", "CFI", "TLI", "RMSEA", "SRMR", "GFI", "AGFI"),
  Value = round(c(fit_measures[1], fit_measures[2], fit_measures[3], 
               fit_measures[4], fit_measures[5], fit_measures[6], 
               fit_measures[7], fit_measures[8], fit_measures[9]), 3)
)
ft_fit <- flextable(fit_df)
ft_fit <- theme_tron(ft_fit)
ft_fit <- set_table_properties(ft_fit, layout = "autofit")
doc <- body_add_flextable(doc, ft_fit)
doc <- body_add_par(doc, "", style = "Normal")

# 5. 信度检验表
doc <- body_add_par(doc, "五、信度与效度检验", style = "heading 2")
alpha_X <- alpha(mean[,1:4])$total$raw_alpha
alpha_M <- alpha(mean[,5:8])$total$raw_alpha
alpha_Y <- alpha(mean[,9:12])$total$raw_alpha
loading_X <- param[param$lhs %in% c("A1","A2","A3","A4") & param$op == "=~", "std.all"]
loading_M <- param[param$lhs %in% c("B1","B2","B3","B4") & param$op == "=~", "std.all"]
loading_Y <- param[param$lhs %in% c("C1","C2","C3","C4") & param$op == "=~", "std.all"]
ave_X <- mean(loading_X^2)
ave_M <- mean(loading_M^2)
ave_Y <- mean(loading_Y^2)
cr_X <- (sum(loading_X))^2 / ((sum(loading_X))^2 + sum((1-loading_X^2)))
cr_M <- (sum(loading_M))^2 / ((sum(loading_M))^2 + sum((1-loading_M^2)))
cr_Y <- (sum(loading_Y))^2 / ((sum(loading_Y))^2 + sum((1-loading_Y^2)))

reliability_df <- data.frame(
  Variable = c("X", "M", "Y"),
  Alpha = round(c(alpha_X, alpha_M, alpha_Y), 3),
  CR = round(c(cr_X, cr_M, cr_Y), 3),
  AVE = round(c(ave_X, ave_M, ave_Y), 3)
)
ft_rel <- flextable(reliability_df)
ft_rel <- theme_tron(ft_rel)
ft_rel <- set_table_properties(ft_rel, layout = "autofit")
doc <- body_add_flextable(doc, ft_rel)
doc <- body_add_par(doc, "", style = "Normal")

# 6. 路径系数表
doc <- body_add_par(doc, "六、结构模型路径系数", style = "heading 2")
paths <- param[param$op == "~" & param$rhs != "1", c("lhs", "rhs", "est", "std.all", "pvalue")]
names(paths) <- c("DV", "IV", "Estimate", "Std", "p")
ft_paths <- flextable(paths)
ft_paths <- theme_tron(ft_paths)
ft_paths <- set_table_properties(ft_paths, layout = "autofit")
doc <- body_add_flextable(doc, ft_paths)
doc <- body_add_par(doc, "", style = "Normal")

# 7. 中介效应分析
doc <- body_add_par(doc, "七、中介效应分析", style = "heading 2")
a_coef <- param[param$lhs == "M" & param$rhs == "X", "std.all"]
b_coef <- param[param$lhs == "Y" & param$rhs == "M", "std.all"]
c_coef <- param[param$lhs == "Y" & param$rhs == "X", "std.all"]
indirect <- a_coef * b_coef
total <- indirect + c_coef

mediation_df <- data.frame(
  Effect = c("Direct (X->Y)", "Indirect (X->M->Y)", "Total"),
  Value = round(c(c_coef, indirect, total), 3),
  Percent = c(round(c_coef/total*100, 1), round(indirect/total*100, 1), "100.0")
)
ft_med <- flextable(mediation_df)
ft_med <- theme_tron(ft_med)
ft_med <- set_table_properties(ft_med, layout = "autofit")
doc <- body_add_flextable(doc, ft_med)
doc <- body_add_par(doc, paste0("\nMediation effect percentage: ", round(indirect/total*100, 1), "%"), style = "Normal")
doc <- body_add_par(doc, "", style = "Normal")

# 8. 聚合效度表
doc <- body_add_par(doc, "八、聚合效度检验", style = "heading 2")
convergent_df <- data.frame(
  Variable = c("X", "M", "Y"),
  Loading_Range = c(paste0(round(min(loading_X), 2), "-", round(max(loading_X), 2)),
                   paste0(round(min(loading_M), 2), "-", round(max(loading_M), 2)),
                   paste0(round(min(loading_Y), 2), "-", round(max(loading_Y), 2))),
  CR = round(c(cr_X, cr_M, cr_Y), 3),
  AVE = round(c(ave_X, ave_M, ave_Y), 3)
)
ft_conv <- flextable(convergent_df)
ft_conv <- theme_tron(ft_conv)
ft_conv <- set_table_properties(ft_conv, layout = "autofit")
doc <- body_add_flextable(doc, ft_conv)
doc <- body_add_par(doc, "", style = "Normal")

# 9. 区分效度表
doc <- body_add_par(doc, "九、区分效度检验", style = "heading 2")
latent_cor <- lavInspect(fit, "cor.lv")
sqrt_ave <- c(sqrt(ave_X), sqrt(ave_M), sqrt(ave_Y))
discriminant_df <- as.data.frame(round(latent_cor, 3))
discriminant_df$Variable = c("X", "M", "Y")
ft_disc <- flextable(discriminant_df)
ft_disc <- theme_tron(ft_disc)
ft_disc <- set_table_properties(ft_disc, layout = "autofit")
doc <- body_add_flextable(doc, ft_disc)
doc <- body_add_par(doc, paste0("\nNote: Diagonal shows sqrt(AVE) values (X=", round(sqrt_ave[1], 3), 
                                 ", M=", round(sqrt_ave[2], 3), 
                                 ", Y=", round(sqrt_ave[3], 3), ")"), style = "Normal")
doc <- body_add_par(doc, "", style = "Normal")

# 10. KMO 分析表
doc <- body_add_par(doc, "十、KMO 检验", style = "heading 2")
kmo_result <- KMO(cor(mean))
kmo_df <- data.frame(
  Variable = c("X", "M", "Y", "Overall"),
  KMO = round(c(kmo_result$MSA[1], kmo_result$MSA[2], kmo_result$MSA[3], kmo_result$MSA), 3)
)
ft_kmo <- flextable(kmo_df)
ft_kmo <- theme_tron(ft_kmo)
ft_kmo <- set_table_properties(ft_kmo, layout = "autofit")
doc <- body_add_flextable(doc, ft_kmo)
doc <- body_add_par(doc, "", style = "Normal")

# 保存文档
print(doc, target = "C:/Users/Mr Zhou/.openclaw/workspace/分析结果/中介模型分析报告.docx")

cat("\n========== 报告生成完成 ==========\n")
cat("文件：中介模型分析报告.docx\n")
cat("================================\n")
