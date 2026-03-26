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
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# ========== 辅助函数 ==========
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

add_sig_stars <- function(p) {
  ifelse(p < 0.001, "***", ifelse(p < 0.01, "**", ifelse(p < 0.05, "*", "")))
}

format_p <- function(p) {
  ifelse(p < 0.001, "< .001", round(p, 3))
}

# ========== 数据模拟 ==========
set.seed(2026)
N <- 336

cat("========== 开始数据模拟 ==========\n")
cat(sprintf("样本量：%d\n\n", N))

# ------------------------------
# 第一部分：患者一般情况调查表
# ------------------------------
cat("模拟第一部分：患者一般情况...\n")

性别 <- sample(c(1, 2), N, replace=TRUE, prob=c(0.48, 0.52))
年龄 <- round(rnorm(N, mean=58, sd=12))
年龄 <- pmax(35, pmin(85, 年龄))
民族 <- sample(c(1, 2), N, replace=TRUE, prob=c(0.92, 0.08))
身高 <- round(rnorm(N, mean=165, sd=8))
体重 <- round(rnorm(N, mean=68, sd=10))
BMI <- round(体重 / ((身高/100)^2), 1)
空腹血糖 <- round(rnorm(N, mean=7.8, sd=2.5), 1)
空腹血糖 <- pmax(4.5, 空腹血糖)
文化程度 <- sample(c(1, 2, 3, 4), N, replace=TRUE, prob=c(0.25, 0.30, 0.28, 0.17))
婚姻状况 <- sample(c(1, 2, 3, 4), N, replace=TRUE, prob=c(0.05, 0.78, 0.12, 0.05))
职业情况 <- sample(c(1, 2, 3, 4, 5, 6), N, replace=TRUE, prob=c(0.35, 0.20, 0.10, 0.05, 0.15, 0.15))
看望频率 <- sample(c(1, 2, 3, 4), N, replace=TRUE, prob=c(0.40, 0.35, 0.15, 0.10))
家庭收入 <- sample(c(1, 2, 3), N, replace=TRUE, prob=c(0.45, 0.35, 0.20))
医疗支付 <- sample(c(1, 2, 3, 4), N, replace=TRUE, prob=c(0.35, 0.30, 0.28, 0.07))
吸烟 <- sample(c(1, 2, 3), N, replace=TRUE, prob=c(0.65, 0.15, 0.20))
饮酒 <- sample(c(1, 2), N, replace=TRUE, prob=c(0.80, 0.20))
发现途径 <- sample(c(1, 2, 3), N, replace=TRUE, prob=c(0.35, 0.45, 0.20))
患病时间 <- sample(c(1, 2, 3), N, replace=TRUE, prob=c(0.50, 0.35, 0.15))
锻炼情况 <- sample(c(1, 2, 3, 4), N, replace=TRUE, prob=c(0.20, 0.35, 0.30, 0.15))
饮食控制 <- sample(c(1, 2, 3), N, replace=TRUE, prob=c(0.25, 0.45, 0.30))
并发症 <- sample(c(1, 2), N, replace=TRUE, prob=c(0.55, 0.45))

患者一般情况 <- data.frame(
  性别，年龄，民族，身高，体重，BMI, 空腹血糖，文化程度，婚姻状况，职业情况，
  看望频率，家庭收入，医疗支付，吸烟，饮酒，发现途径，患病时间，锻炼情况，
  饮食控制，并发症
)

# ------------------------------
# 第二部分：DSQL 糖尿病生活质量特异性表
# ------------------------------
cat("模拟第二部分：DSQL 生活质量量表...\n")

# 生理功能维度 (12 题)
生理_1 <- sample(1:5, N, replace=TRUE, prob=c(0.08, 0.20, 0.30, 0.27, 0.15))
生理_2 <- sample(1:5, N, replace=TRUE, prob=c(0.10, 0.22, 0.28, 0.25, 0.15))
生理_3 <- sample(1:5, N, replace=TRUE, prob=c(0.12, 0.25, 0.30, 0.23, 0.10))
生理_4 <- sample(1:5, N, replace=TRUE, prob=c(0.15, 0.30, 0.30, 0.18, 0.07))
生理_5 <- sample(1:5, N, replace=TRUE, prob=c(0.18, 0.32, 0.28, 0.15, 0.07))
生理_6 <- sample(1:5, N, replace=TRUE, prob=c(0.20, 0.35, 0.28, 0.12, 0.05))
生理_7 <- sample(1:5, N, replace=TRUE, prob=c(0.22, 0.35, 0.28, 0.10, 0.05))
生理_8 <- sample(1:5, N, replace=TRUE, prob=c(0.15, 0.30, 0.32, 0.18, 0.05))
生理_9 <- sample(1:5, N, replace=TRUE, prob=c(0.18, 0.32, 0.30, 0.15, 0.05))
生理_10 <- sample(1:5, N, replace=TRUE, prob=c(0.20, 0.35, 0.28, 0.12, 0.05))
生理_11 <- sample(1:5, N, replace=TRUE, prob=c(0.22, 0.35, 0.28, 0.10, 0.05))
生理_12 <- sample(1:5, N, replace=TRUE, prob=c(0.18, 0.32, 0.30, 0.15, 0.05))

# 心理/精神维度 (8 题)
心理_1 <- sample(1:5, N, replace=TRUE, prob=c(0.15, 0.28, 0.30, 0.20, 0.07))
心理_2 <- sample(1:5, N, replace=TRUE, prob=c(0.12, 0.25, 0.32, 0.23, 0.08))
心理_3 <- sample(1:5, N, replace=TRUE, prob=c(0.18, 0.30, 0.30, 0.17, 0.05))
心理_4 <- sample(1:5, N, replace=TRUE, prob=c(0.10, 0.22, 0.35, 0.25, 0.08))
心理_5 <- sample(1:5, N, replace=TRUE, prob=c(0.12, 0.25, 0.32, 0.23, 0.08))
心理_6 <- sample(1:5, N, replace=TRUE, prob=c(0.15, 0.28, 0.32, 0.20, 0.05))
心理_7 <- sample(1:5, N, replace=TRUE, prob=c(0.08, 0.20, 0.35, 0.27, 0.10))
心理_8 <- sample(1:5, N, replace=TRUE, prob=c(0.10, 0.22, 0.32, 0.28, 0.08))

# 社会关系维度 (4 题)
社会_1 <- sample(1:5, N, replace=TRUE, prob=c(0.25, 0.35, 0.25, 0.10, 0.05))
社会_2 <- sample(1:5, N, replace=TRUE, prob=c(0.30, 0.38, 0.22, 0.07, 0.03))
社会_3 <- sample(1:5, N, replace=TRUE, prob=c(0.28, 0.35, 0.25, 0.09, 0.03))
社会_4 <- sample(1:5, N, replace=TRUE, prob=c(0.20, 0.32, 0.30, 0.13, 0.05))

# 治疗维度 (4 题)
治疗_1 <- sample(1:5, N, replace=TRUE, prob=c(0.25, 0.35, 0.25, 0.10, 0.05))
治疗_2 <- sample(1:5, N, replace=TRUE, prob=c(0.28, 0.38, 0.22, 0.09, 0.03))
治疗_3 <- sample(1:5, N, replace=TRUE, prob=c(0.15, 0.30, 0.32, 0.18, 0.05))
治疗_4 <- sample(1:5, N, replace=TRUE, prob=c(0.20, 0.32, 0.30, 0.13, 0.05))

DSQL 数据 <- data.frame(
  生理_1, 生理_2, 生理_3, 生理_4, 生理_5, 生理_6, 生理_7, 生理_8, 生理_9, 生理_10, 生理_11, 生理_12,
  心理_1, 心理_2, 心理_3, 心理_4, 心理_5, 心理_6, 心理_7, 心理_8,
  社会_1, 社会_2, 社会_3, 社会_4,
  治疗_1, 治疗_2, 治疗_3, 治疗_4
)

# 计算 DSQL 维度均值
DSQL 维度均值 <- data.frame(
  生理功能 = rowMeans(DSQL 数据[, c("生理_1", "生理_2", "生理_3", "生理_4", "生理_5", "生理_6", 
                                   "生理_7", "生理_8", "生理_9", "生理_10", "生理_11", "生理_12")]),
  心理精神 = rowMeans(DSQL 数据[, c("心理_1", "心理_2", "心理_3", "心理_4", "心理_5", "心理_6", "心理_7", "心理_8")]),
  社会关系 = rowMeans(DSQL 数据[, c("社会_1", "社会_2", "社会_3", "社会_4")]),
  治疗维度 = rowMeans(DSQL 数据[, c("治疗_1", "治疗_2", "治疗_3", "治疗_4")])
)

# ------------------------------
# 第三部分：SDSCA 糖尿病自我管理行为量表
# ------------------------------
cat("模拟第三部分：SDSCA 自我管理行为...\n")

SDSCA_1 <- sample(0:7, N, replace=TRUE, prob=c(0.05, 0.08, 0.10, 0.12, 0.18, 0.20, 0.15, 0.12))
SDSCA_2 <- sample(0:7, N, replace=TRUE, prob=c(0.06, 0.08, 0.10, 0.12, 0.18, 0.20, 0.15, 0.11))
SDSCA_3 <- sample(0:7, N, replace=TRUE, prob=c(0.08, 0.10, 0.12, 0.15, 0.20, 0.18, 0.10, 0.07))
SDSCA_4 <- sample(0:7, N, replace=TRUE, prob=c(0.15, 0.20, 0.22, 0.18, 0.12, 0.08, 0.03, 0.02))
SDSCA_5 <- sample(0:7, N, replace=TRUE, prob=c(0.10, 0.12, 0.15, 0.18, 0.20, 0.15, 0.07, 0.03))
SDSCA_6 <- sample(0:7, N, replace=TRUE, prob=c(0.08, 0.10, 0.12, 0.15, 0.22, 0.18, 0.10, 0.05))
SDSCA_7 <- sample(0:7, N, replace=TRUE, prob=c(0.12, 0.15, 0.18, 0.20, 0.18, 0.10, 0.05, 0.02))
SDSCA_8 <- sample(0:7, N, replace=TRUE, prob=c(0.10, 0.12, 0.15, 0.18, 0.20, 0.15, 0.07, 0.03))
SDSCA_9 <- sample(0:7, N, replace=TRUE, prob=c(0.15, 0.18, 0.20, 0.18, 0.15, 0.08, 0.04, 0.02))
SDSCA_10 <- sample(0:7, N, replace=TRUE, prob=c(0.18, 0.20, 0.22, 0.18, 0.12, 0.06, 0.03, 0.01))
SDSCA_11 <- sample(0:7, N, replace=TRUE, prob=c(0.05, 0.05, 0.08, 0.10, 0.15, 0.22, 0.20, 0.15))

SDSCA 数据 <- data.frame(
  SDSCA_1, SDSCA_2, SDSCA_3, SDSCA_4, SDSCA_5, SDSCA_6, SDSCA_7, SDSCA_8, SDSCA_9, SDSCA_10, SDSCA_11
)

SDSCA 维度均值 <- data.frame(
  饮食管理 = rowMeans(SDSCA 数据[, c("SDSCA_1", "SDSCA_2", "SDSCA_3", "SDSCA_4")]),
  运动管理 = rowMeans(SDSCA 数据[, c("SDSCA_5", "SDSCA_6")]),
  血糖监测 = rowMeans(SDSCA 数据[, c("SDSCA_7", "SDSCA_8")]),
  足部护理 = rowMeans(SDSCA 数据[, c("SDSCA_9", "SDSCA_10")]),
  用药依从 = rowMeans(SDSCA 数据[, c("SDSCA_11")])
)

# ------------------------------
# 第四部分：照顾者一般资料
# ------------------------------
cat("模拟第四部分：照顾者一般资料...\n")

照顾者_性别 <- sample(c(1, 2), N, replace=TRUE, prob=c(0.42, 0.58))
照顾者_年龄 <- round(rnorm(N, mean=52, sd=14))
照顾者_年龄 <- pmax(25, pmin(80, 照顾者_年龄))
照顾者_文化程度 <- sample(c(1, 2, 3), N, replace=TRUE, prob=c(0.30, 0.40, 0.30))
照顾者_婚姻 <- sample(c(1, 2), N, replace=TRUE, prob=c(0.85, 0.15))
照顾者_月收入 <- sample(c(1, 2, 3), N, replace=TRUE, prob=c(0.40, 0.40, 0.20))
照顾者_慢性病 <- sample(c(1, 2), N, replace=TRUE, prob=c(0.65, 0.35))
照顾者_关系 <- sample(c(1, 2, 3), N, replace=TRUE, prob=c(0.55, 0.35, 0.10))
照顾者_每日时间 <- sample(c(1, 2, 3), N, replace=TRUE, prob=c(0.30, 0.45, 0.25))
照顾者_照顾年限 <- sample(c(1, 2, 3), N, replace=TRUE, prob=c(0.35, 0.40, 0.25))
照顾者_分担者 <- sample(c(1, 2), N, replace=TRUE, prob=c(0.40, 0.60))

照顾者一般资料 <- data.frame(
  照顾者_性别，照顾者_年龄，照顾者_文化程度，照顾者_婚姻，照顾者_月收入，
  照顾者_慢性病，照顾者_关系，照顾者_每日时间，照顾者_照顾年限，照顾者_分担者
)

# ------------------------------
# 第五部分：照顾能力量表 (25 题，3 点计分)
# ------------------------------
cat("模拟第五部分：照顾能力量表...\n")

照顾能力数据 <- data.frame()
for (i in 1:25) {
  照顾能力数据[[paste0("能力_", i)]] <- sample(1:3, N, replace=TRUE, prob=c(0.35, 0.45, 0.20))
}

照顾能力维度均值 <- data.frame(
  病情观察 = rowMeans(照顾能力数据[, c("能力_1", "能力_2", "能力_3")]),
  生活协助 = rowMeans(照顾能力数据[, c("能力_4", "能力_5", "能力_6")]),
  疾病认知 = rowMeans(照顾能力数据[, c("能力_7", "能力_8")]),
  应对能力 = rowMeans(照顾能力数据[, c("能力_9", "能力_10", "能力_11")]),
  情绪管理 = rowMeans(照顾能力数据[, c("能力_12", "能力_13", "能力_14", "能力_15")]),
  资源利用 = rowMeans(照顾能力数据[, c("能力_16", "能力_17", "能力_18", "能力_19", "能力_20")]),
  自我调适 = rowMeans(照顾能力数据[, c("能力_21", "能力_22", "能力_23", "能力_24", "能力_25")])
)

# ========== 合并所有数据 ==========
cat("\n合并所有数据...\n")
完整数据 <- cbind(患者一般情况，DSQL 数据，SDSCA 数据，照顾者一般资料，照顾能力数据)

# ========== 保存数据文件 ==========
cat("\n保存数据文件...\n")
write_sav(完整数据，file.path(output_dir, "糖尿病问卷完整数据.sav"))
write.xlsx(完整数据，file.path(output_dir, "糖尿病问卷完整数据.xlsx"), rowNames=FALSE)

# 保存维度均值数据
维度均值数据 <- cbind(DSQL 维度均值，SDSCA 维度均值，照顾能力维度均值)
write_sav(维度均值数据，file.path(output_dir, "糖尿病问卷维度均值.sav"))
write.xlsx(维度均值数据，file.path(output_dir, "糖尿病问卷维度均值.xlsx"), rowNames=FALSE)

cat("\n========== 数据模拟完成 ==========\n")
cat(sprintf("样本量：%d\n", N))
cat(sprintf("总变量数：%d\n", ncol(完整数据)))
cat(sprintf("维度变量数：%d\n", ncol(维度均值数据)))
cat("\n已保存文件:\n")
cat("  - 糖尿病问卷完整数据.sav\n")
cat("  - 糖尿病问卷完整数据.xlsx\n")
cat("  - 糖尿病问卷维度均值.sav\n")
cat("  - 糖尿病问卷维度均值.xlsx\n")
