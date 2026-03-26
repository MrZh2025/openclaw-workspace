# 中介模型数据模拟 X→M→Y
# 样本量：400
# 执行时间：2026-03-13

library(lavaan)
library(haven)
library(openxlsx)

set.seed(20260313)
n <- 400

# ============ 参数设置 ============
# 因子载荷 (0.9-2.5 范围)
lambda_X <- c(1.2, 1.3, 1.1, 1.4)  # X 的 4 个题目
lambda_M <- c(1.3, 1.2, 1.4, 1.1)  # M 的 4 个题目
lambda_Y <- c(1.1, 1.3, 1.2, 1.4)  # Y 的 4 个题目

# 路径系数 (0.2-0.6 范围)
a_path <- 0.45  # X→M
b_path <- 0.38  # M→Y
c_prime <- 0.25 # X→Y (直接效应)

# 误差方差
theta_X <- 1.0
theta_M <- 1.0
theta_Y <- 1.0

# ============ 生成潜变量 ============
# 生成外生潜变量 X
X_latent <- rnorm(n, mean = 0, sd = 1)

# 生成内生潜变量 M (X→M)
M_latent <- a_path * X_latent + rnorm(n, mean = 0, sd = sqrt(theta_M))

# 生成内生潜变量 Y (X→Y, M→Y)
Y_latent <- c_prime * X_latent + b_path * M_latent + rnorm(n, mean = 0, sd = sqrt(theta_Y))

# ============ 生成观测变量 (题目) ============
# X 的题目 (A1-A4)
A1 <- lambda_X[1] * X_latent + rnorm(n, 0, 1)
A2 <- lambda_X[2] * X_latent + rnorm(n, 0, 1)
A3 <- lambda_X[3] * X_latent + rnorm(n, 0, 1)
A4 <- lambda_X[4] * X_latent + rnorm(n, 0, 1)

# M 的题目 (B1-B4)
B1 <- lambda_M[1] * M_latent + rnorm(n, 0, 1)
B2 <- lambda_M[2] * M_latent + rnorm(n, 0, 1)
B3 <- lambda_M[3] * M_latent + rnorm(n, 0, 1)
B4 <- lambda_M[4] * M_latent + rnorm(n, 0, 1)

# Y 的题目 (C1-C4)
C1 <- lambda_Y[1] * Y_latent + rnorm(n, 0, 1)
C2 <- lambda_Y[2] * Y_latent + rnorm(n, 0, 1)
C3 <- lambda_Y[3] * Y_latent + rnorm(n, 0, 1)
C4 <- lambda_Y[4] * Y_latent + rnorm(n, 0, 1)

# ============ 组装数据框 ============
mean <- data.frame(
  A1 = A1, A2 = A2, A3 = A3, A4 = A4,
  B1 = B1, B2 = B2, B3 = B3, B4 = B4,
  C1 = C1, C2 = C2, C3 = C3, C4 = C4
)

# ============ 验证模型 (CFA+路径分析) ============
model <- '
  # 测量模型
  X =~ A1 + A2 + A3 + A4
  M =~ B1 + B2 + B3 + B4
  Y =~ C1 + C2 + C3 + C4
  
  # 结构模型
  M ~ a*X
  Y ~ b*M + c*X
'

fit <- sem(model, data = mean, std.lv = FALSE, estimator = "MLR")
summary(fit, fit.measures = TRUE, standardized = TRUE)

# ============ 输出表格 ============
# 1. 相关系数矩阵
cor_matrix <- cor(mean)
write.xlsx(cor_matrix, "C:/Users/Mr Zhou/.openclaw/workspace/分析结果/相关系数矩阵.xlsx", rowNames = TRUE)

# 2. CFA 因子载荷表
param <- parameterEstimates(fit, standardized = TRUE)
loading_X <- param[param$lhs %in% c("A1","A2","A3","A4") & param$op == "=~", c("lhs","est","std.all")]
loading_M <- param[param$lhs %in% c("B1","B2","B3","B4") & param$op == "=~", c("lhs","est","std.all")]
loading_Y <- param[param$lhs %in% c("C1","C2","C3","C4") & param$op == "=~", c("lhs","est","std.all")]

# 3. 路径系数表
paths <- param[param$op == "~" & param$rhs != "1", c("lhs","rhs","est","std.all","pvalue")]

# 4. 模型拟合度表
fit_measures <- fitMeasures(fit, c("chisq","df","pvalue","cfi","tli","rmsea","srmr","gfi","agfi"))
fit_df <- data.frame(
  指标 = c("χ²","df","p","CFI","TLI","RMSEA","SRMR","GFI","AGFI"),
  值 = round(c(fit_measures[1], fit_measures[2], fit_measures[3], 
               fit_measures[4], fit_measures[5], fit_measures[6], 
               fit_measures[7], fit_measures[8], fit_measures[9]), 3)
)

# 5. 信度检验表 (Cronbach's α + AVE)
library(psych)
alpha_X <- alpha(mean[,1:4])$total$raw_alpha
alpha_M <- alpha(mean[,5:8])$total$raw_alpha
alpha_Y <- alpha(mean[,9:12])$total$raw_alpha

# AVE 计算 (因子载荷平方和 / (因子载荷平方和 + 误差方差和))
ave_X <- mean(loading_X$std.all^2)
ave_M <- mean(loading_M$std.all^2)
ave_Y <- mean(loading_Y$std.all^2)

reliability_df <- data.frame(
  变量 = c("X", "M", "Y"),
  Cronbach_α = round(c(alpha_X, alpha_M, alpha_Y), 3),
  AVE = round(c(ave_X, ave_M, ave_Y), 3)
)

# ============ 保存数据 ============
write_sav(mean, "C:/Users/Mr Zhou/.openclaw/workspace/分析结果/中介模型数据.sav")
write.xlsx(mean, "C:/Users/Mr Zhou/.openclaw/workspace/分析结果/中介模型数据.xlsx", rowNames = FALSE)

cat("\n========== 数据模拟完成 ==========\n")
cat("样本量:", n, "\n")
cat("变量: X(4 题), M(4 题), Y(4 题)\n")
cat("路径系数: X→M =", a_path, ", M→Y =", b_path, ", X→Y =", c_prime, "\n")
cat("间接效应:", round(a_path * b_path, 3), "\n")
cat("文件已保存至：分析结果/\n")
cat("================================\n")
