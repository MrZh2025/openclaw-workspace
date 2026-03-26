# 锦州地区老年高血压患者心理弹性与服药依从性问卷数据模拟
# 执行语言：R
# 样本量：345（AMOS 默认）

library(MASS)
library(lavaan)
library(psych)
library(haven)
library(openxlsx)

set.seed(20260313)
n <- 345

# ==================== 一、人口学变量模拟 ====================
gender <- sample(c("男", "女"), n, replace = TRUE, prob = c(0.48, 0.52))
age_group <- sample(c("60-69 岁", "70-79 岁", "80-89 岁", "≥90 岁"), n, replace = TRUE, 
                    prob = c(0.35, 0.40, 0.20, 0.05))
education <- sample(c("未受教育", "小学", "初中", "高中/中专", "大专及以上"), n, replace = TRUE,
                    prob = c(0.10, 0.25, 0.30, 0.20, 0.15))
marriage <- sample(c("未婚", "已婚", "离婚", "丧偶"), n, replace = TRUE,
                   prob = c(0.02, 0.65, 0.08, 0.25))
economy <- sample(c("贫困", "一般", "良好", "富裕"), n, replace = TRUE,
                  prob = c(0.15, 0.50, 0.28, 0.07))
insurance <- sample(c("城镇职工", "城镇居民", "新农合", "商业保险", "无医保"), n, replace = TRUE,
                    prob = c(0.25, 0.30, 0.35, 0.05, 0.05))
living <- sample(c("独居", "与配偶同住", "与子女同住", "养老院", "其他"), n, replace = TRUE,
                 prob = c(0.12, 0.45, 0.30, 0.08, 0.05))
caregiver <- sample(c("配偶", "子女", "其他亲属", "护工", "无照护者"), n, replace = TRUE,
                    prob = c(0.40, 0.35, 0.12, 0.08, 0.05))
social_support <- sample(c("极低", "较低", "一般", "较高", "极高"), n, replace = TRUE,
                         prob = c(0.08, 0.20, 0.35, 0.27, 0.10))

# ==================== 二、疾病用药变量模拟 ====================
diagnosis_time <- sample(c("<1 年", "1-5 年", "6-10 年", ">10 年"), n, replace = TRUE,
                         prob = c(0.15, 0.40, 0.28, 0.17))
bp_control <- sample(c("极差", "较差", "一般", "良好"), n, replace = TRUE,
                     prob = c(0.08, 0.25, 0.40, 0.27))
complications <- sample(c("冠心病", "脑卒中", "糖尿病", "肾病", "高血脂", "其他", "无"), n, replace = TRUE,
                        prob = c(0.15, 0.12, 0.20, 0.10, 0.18, 0.05, 0.20))
med_adherence_yes <- sample(c("否", "是"), n, replace = TRUE, prob = c(0.25, 0.75))
med_types <- sample(c("1 种", "2 种", "≥3 种"), n, replace = TRUE, prob = c(0.35, 0.40, 0.25))
med_freq <- sample(c("每天 1 次", "每天 2 次", "每天 3 次及以上", "按需服用"), n, replace = TRUE,
                   prob = c(0.50, 0.30, 0.12, 0.08))
side_effect <- sample(c("否", "是"), n, replace = TRUE, prob = c(0.65, 0.35))
bp_monitor <- sample(c("否", "是"), n, replace = TRUE, prob = c(0.30, 0.70))
measure_freq <- sample(c("几乎不测", "每周 1 次及以下", "每周 2-3 次", "每天 1 次及以上"), n, replace = TRUE,
                       prob = c(0.15, 0.30, 0.35, 0.20))
followup <- sample(c("从不", "1-3 次", "4-6 次", "7-12 次", ">12 次"), n, replace = TRUE,
                   prob = c(0.05, 0.25, 0.35, 0.25, 0.10))
accessibility <- sample(c("极不便捷", "不太便捷", "一般", "较便捷", "很便捷"), n, replace = TRUE,
                        prob = c(0.05, 0.15, 0.30, 0.35, 0.15))
knowledge_disease <- sample(c("根本不了解", "不太了解", "大概了解", "很清楚"), n, replace = TRUE,
                            prob = c(0.10, 0.30, 0.40, 0.20))
knowledge_med <- sample(c("根本不了解", "不太了解", "大概了解", "很清楚"), n, replace = TRUE,
                        prob = c(0.08, 0.25, 0.42, 0.25))
knowledge_harm <- sample(c("根本不了解", "不太了解", "大概了解", "很清楚"), n, replace = TRUE,
                         prob = c(0.06, 0.22, 0.45, 0.27))
hospitalization <- sample(c("否", "是"), n, replace = TRUE, prob = c(0.70, 0.30))

# ==================== 三、生活方式变量模拟 ====================
smoking <- sample(c("否", "是"), n, replace = TRUE, prob = c(0.75, 0.25))
smoke_amount <- sample(c("少于 3 支/天", "3-5 支/天", "5-10 支/天", ">10 支/天", "已戒烟"), n, replace = TRUE,
                       prob = c(0.30, 0.25, 0.20, 0.10, 0.15))
drinking <- sample(c("否", "是"), n, replace = TRUE, prob = c(0.70, 0.30))
drink_freq <- sample(c("偶尔", "有时", "经常", "几乎每天", "已戒酒"), n, replace = TRUE,
                     prob = c(0.35, 0.30, 0.15, 0.10, 0.10))
salt_intake <- sample(c("≤6 克", ">6 克"), n, replace = TRUE, prob = c(0.35, 0.65))
routine <- sample(c("不太规律", "一般", "比较规律", "非常规律"), n, replace = TRUE,
                  prob = c(0.15, 0.35, 0.35, 0.15))
exercise <- sample(c("无", "1-2 次", "3-4 次", "≥5 次"), n, replace = TRUE,
                   prob = c(0.25, 0.40, 0.25, 0.10))
hobby <- sample(c("无", "1-2 项", "3-4 项", "5 项及以上"), n, replace = TRUE,
                prob = c(0.15, 0.45, 0.30, 0.10))
coping <- sample(c("消极回避", "被动接受", "积极应对", "主动管理"), n, replace = TRUE,
                 prob = c(0.10, 0.30, 0.40, 0.20))
self_efficacy <- sample(c("极低", "较低", "一般", "较高", "极高"), n, replace = TRUE,
                        prob = c(0.08, 0.22, 0.35, 0.25, 0.10))
emotion <- sample(c("经常焦虑/抑郁", "偶尔焦虑/抑郁", "情绪平稳", "经常积极乐观", "始终积极乐观"), n, replace = TRUE,
                  prob = c(0.10, 0.25, 0.35, 0.22, 0.08))

# ==================== 四、服药依从性量表模拟（9 题，Likert 4 点） ====================
# 潜变量：服药依从性 (MedAdherence)
# 因子载荷：0.9-2.5（固定首题载荷为 1）
# 题目 36-44，分数越高表示依从性越好（需反向计分题处理）

# 生成潜变量得分
med_latent <- rnorm(n, mean = 3.0, sd = 0.8)

# 观测变量（增加误差，降低拟合度）
A1 <- round(pmax(1, pmin(4, med_latent * 1.0 + rnorm(n, 0, 0.65))))  # 题 36：忘记服药（反向）
A2 <- round(pmax(1, pmin(4, med_latent * 1.3 + rnorm(n, 0, 0.60))))  # 题 37：疏忽漏服（反向）
A3 <- round(pmax(1, pmin(4, med_latent * 1.5 + rnorm(n, 0, 0.55))))  # 题 38：自行减量（反向）
A4 <- round(pmax(1, pmin(4, med_latent * 1.4 + rnorm(n, 0, 0.58))))  # 题 39：自行加量（反向）
A5 <- round(pmax(1, pmin(4, med_latent * 1.2 + rnorm(n, 0, 0.62))))  # 题 40：忘带药（反向）
A6 <- round(pmax(1, pmin(4, med_latent * 1.6 + rnorm(n, 0, 0.52))))  # 题 41：担心副作用（反向）
A7 <- round(pmax(1, pmin(4, med_latent * 1.5 + rnorm(n, 0, 0.55))))  # 题 42：怕麻烦（反向）
A8 <- round(pmax(1, pmin(4, med_latent * 1.4 + rnorm(n, 0, 0.58))))  # 题 43：经济压力（反向）
A9 <- round(pmax(1, pmin(4, med_latent * 1.7 + rnorm(n, 0, 0.50))))  # 题 44：严格按医嘱（正向）

# 反向题转换（1→4, 2→3, 3→2, 4→1）
A1_r <- 5 - A1
A2_r <- 5 - A2
A3_r <- 5 - A3
A4_r <- 5 - A4
A5_r <- 5 - A5
A6_r <- 5 - A6
A7_r <- 5 - A7
A8_r <- 5 - A8
A9_r <- A9  # 正向题

# ==================== 五、心理弹性量表模拟（25 题，Likert 5 点） ====================
# 潜变量：心理弹性 (Resilience)
# 因子载荷：0.9-2.5

res_latent <- rnorm(n, mean = 3.5, sd = 0.9)

# 观测变量 B1-B25（题 45-69）
B1 <- round(pmax(1, pmin(5, res_latent * 1.0 + rnorm(n, 0, 0.70))))
B2 <- round(pmax(1, pmin(5, res_latent * 1.3 + rnorm(n, 0, 0.65))))
B3 <- round(pmax(1, pmin(5, res_latent * 1.4 + rnorm(n, 0, 0.62))))
B4 <- round(pmax(1, pmin(5, res_latent * 1.5 + rnorm(n, 0, 0.60))))
B5 <- round(pmax(1, pmin(5, res_latent * 1.2 + rnorm(n, 0, 0.68))))
B6 <- round(pmax(1, pmin(5, res_latent * 1.4 + rnorm(n, 0, 0.62))))
B7 <- round(pmax(1, pmin(5, res_latent * 1.6 + rnorm(n, 0, 0.58))))
B8 <- round(pmax(1, pmin(5, res_latent * 1.5 + rnorm(n, 0, 0.60))))
B9 <- round(pmax(1, pmin(5, res_latent * 1.3 + rnorm(n, 0, 0.65))))
B10 <- round(pmax(1, pmin(5, res_latent * 1.4 + rnorm(n, 0, 0.62))))
B11 <- round(pmax(1, pmin(5, res_latent * 1.5 + rnorm(n, 0, 0.60))))
B12 <- round(pmax(1, pmin(5, res_latent * 1.7 + rnorm(n, 0, 0.55))))
B13 <- round(pmax(1, pmin(5, res_latent * 1.4 + rnorm(n, 0, 0.62))))
B14 <- round(pmax(1, pmin(5, res_latent * 1.3 + rnorm(n, 0, 0.65))))
B15 <- round(pmax(1, pmin(5, res_latent * 1.5 + rnorm(n, 0, 0.60))))
B16 <- round(pmax(1, pmin(5, res_latent * 1.6 + rnorm(n, 0, 0.58))))
B17 <- round(pmax(1, pmin(5, res_latent * 1.4 + rnorm(n, 0, 0.62))))
B18 <- round(pmax(1, pmin(5, res_latent * 1.5 + rnorm(n, 0, 0.60))))
B19 <- round(pmax(1, pmin(5, res_latent * 1.3 + rnorm(n, 0, 0.65))))
B20 <- round(pmax(1, pmin(5, res_latent * 1.4 + rnorm(n, 0, 0.62))))
B21 <- round(pmax(1, pmin(5, res_latent * 1.6 + rnorm(n, 0, 0.58))))
B22 <- round(pmax(1, pmin(5, res_latent * 1.5 + rnorm(n, 0, 0.60))))
B23 <- round(pmax(1, pmin(5, res_latent * 1.4 + rnorm(n, 0, 0.62))))
B24 <- round(pmax(1, pmin(5, res_latent * 1.5 + rnorm(n, 0, 0.60))))
B25 <- round(pmax(1, pmin(5, res_latent * 1.6 + rnorm(n, 0, 0.58))))

# ==================== 六、构建结构方程模型 ====================
# 心理弹性 → 服药依从性（假设正向影响）
med_latent_final <- 0.45 * res_latent + rnorm(n, 0, 0.8)

# 重新生成依从性观测变量
A1 <- round(pmax(1, pmin(4, med_latent_final * 1.0 + rnorm(n, 0, 0.65))))
A2 <- round(pmax(1, pmin(4, med_latent_final * 1.3 + rnorm(n, 0, 0.60))))
A3 <- round(pmax(1, pmin(4, med_latent_final * 1.5 + rnorm(n, 0, 0.55))))
A4 <- round(pmax(1, pmin(4, med_latent_final * 1.4 + rnorm(n, 0, 0.58))))
A5 <- round(pmax(1, pmin(4, med_latent_final * 1.2 + rnorm(n, 0, 0.62))))
A6 <- round(pmax(1, pmin(4, med_latent_final * 1.6 + rnorm(n, 0, 0.52))))
A7 <- round(pmax(1, pmin(4, med_latent_final * 1.5 + rnorm(n, 0, 0.55))))
A8 <- round(pmax(1, pmin(4, med_latent_final * 1.4 + rnorm(n, 0, 0.58))))
A9 <- round(pmax(1, pmin(4, med_latent_final * 1.7 + rnorm(n, 0, 0.50))))

# 反向计分处理
A1_r <- 5 - A1
A2_r <- 5 - A2
A3_r <- 5 - A3
A4_r <- 5 - A4
A5_r <- 5 - A5
A6_r <- 5 - A6
A7_r <- 5 - A7
A8_r <- 5 - A8
A9_r <- A9

# ==================== 七、创建数据框 ====================
data <- data.frame(
  # 人口学
  Q1_性别 = gender,
  Q2_年龄 = age_group,
  Q3_文化程度 = education,
  Q4_婚姻 = marriage,
  Q5_经济 = economy,
  Q6_医保 = insurance,
  Q7_居住 = living,
  Q8_照护者 = caregiver,
  Q9_社会支持 = social_support,
  # 疾病用药
  Q10_确诊时间 = diagnosis_time,
  Q11_血压控制 = bp_control,
  Q12_并发症 = complications,
  Q13_遵医嘱 = med_adherence_yes,
  Q14_药品种类 = med_types,
  Q15_服药频率 = med_freq,
  Q16_不良反应 = side_effect,
  Q17_血压仪 = bp_monitor,
  Q18_测量频率 = measure_freq,
  Q19_随诊次数 = followup,
  Q20_就医便捷 = accessibility,
  Q21_疾病知识 = knowledge_disease,
  Q22_用药知识 = knowledge_med,
  Q23_危害知识 = knowledge_harm,
  Q24_住院史 = hospitalization,
  # 生活方式
  Q25_吸烟 = smoking,
  Q26_吸烟量 = smoke_amount,
  Q27_饮酒 = drinking,
  Q28_饮酒频率 = drink_freq,
  Q29_食盐 = salt_intake,
  Q30_作息 = routine,
  Q31_运动 = exercise,
  Q32_爱好 = hobby,
  Q33_应对方式 = coping,
  Q34_自我效能 = self_efficacy,
  Q35_情绪 = emotion,
  # 服药依从性（反向题已转换）
  Q36_忘记服药 = A1_r,
  Q37_疏忽漏服 = A2_r,
  Q38_自行减量 = A3_r,
  Q39_自行加量 = A4_r,
  Q40_忘带药 = A5_r,
  Q41_担心副作用 = A6_r,
  Q42_怕麻烦 = A7_r,
  Q43_经济压力 = A8_r,
  Q44_严格按医嘱 = A9_r,
  # 心理弹性
  Q45_适应变化 = B1,
  Q46_人际关系 = B2,
  Q47_外界支持 = B3,
  Q48_从容应付 = B4,
  Q49_成功经历 = B5,
  Q50_幽默积极 = B6,
  Q51_更有力量 = B7,
  Q52_恢复状态 = B8,
  Q53_理性看待 = B9,
  Q54_尽力配合 = B10,
  Q55_小目标 = B11,
  Q56_不放弃 = B12,
  Q57_寻求帮助 = B13,
  Q58_集中注意 = B14,
  Q59_主动担责 = B15,
  Q60_不气馁 = B16,
  Q61_内心强大 = B17,
  Q62_艰难决定 = B18,
  Q63_调节情绪 = B19,
  Q64_积极预期 = B20,
  Q65_生活目的 = B21,
  Q66_掌控节奏 = B22,
  Q67_尝试新方法 = B23,
  Q68_坚持习惯 = B24,
  Q69_管理成效 = B25
)

# ==================== 八、信效度分析 ====================
# 服药依从性量表（列 36-44）
med_items <- data[, 36:44]
med_alpha <- psych::alpha(med_items, check.keys = TRUE)$total$std.alpha
med_avr <- psych::alpha(med_items, check.keys = TRUE)$total$ave_r
med_item_total <- psych::alpha(med_items, check.keys = TRUE)$item.total

# 心理弹性量表（列 45-69）
res_items <- data[, 45:69]
res_alpha <- psych::alpha(res_items)$total$std.alpha
res_avr <- psych::alpha(res_items)$total$ave_r
res_item_total <- psych::alpha(res_items)$item.total

# 相关系数矩阵（服药依从性 Q36-Q44 为列 36-44，心理弹性 Q45-Q69 为列 45-69）
cor_matrix <- cor(data[, c(36:44, 45:69)], use = "complete.obs")

# ==================== 九、验证性因子分析 (CFA) ====================
cfa_model <- '
  服药依从性 =~ Q36_忘记服药 + Q37_疏忽漏服 + Q38_自行减量 + Q39_自行加量 + 
               Q40_忘带药 + Q41_担心副作用 + Q42_怕麻烦 + Q43_经济压力 + Q44_严格按医嘱
  心理弹性 =~ Q45_适应变化 + Q46_人际关系 + Q47_外界支持 + Q48_从容应付 +
             Q49_成功经历 + Q50_幽默积极 + Q51_更有力量 + Q52_恢复状态 +
             Q53_理性看待 + Q54_尽力配合 + Q55_小目标 + Q56_不放弃 +
             Q57_寻求帮助 + Q58_集中注意 + Q59_主动担责 + Q60_不气馁 +
             Q61_内心强大 + Q62_艰难决定 + Q63_调节情绪 + Q64_积极预期 +
             Q65_生活目的 + Q66_掌控节奏 + Q67_尝试新方法 + Q68_坚持习惯 + Q69_管理成效
  服药依从性 ~ 心理弹性
'

cfa_fit <- cfa(cfa_model, data = data, estimator = "WLSMV", ordered = names(data)[36:69])
fit_indices <- fitMeasures(cfa_fit, c("chisq", "df", "pvalue", "cfi", "tli", "rmsea", "srmr", "gfi", "agfi"))

# ==================== 十、聚合效度与区分效度 ====================
# 因子载荷
med_loadings <- inspect(cfa_fit, "std")$lambda["服药依从性", ]
res_loadings <- inspect(cfa_fit, "std")$lambda["心理弹性", ]

# AVE 计算
med_ave <- mean(med_loadings^2)
res_ave <- mean(res_loadings^2)

# CR 计算
med_cr <- (sum(med_loadings))^2 / ((sum(med_loadings))^2 + sum(1 - med_loadings^2))
res_cr <- (sum(res_loadings))^2 / ((sum(res_loadings))^2 + sum(1 - res_loadings^2))

# 潜变量相关
latent_cor <- lavInspect(cfa_fit, "std.all")$psi[1, 2]

# ==================== 十一、KMO 与巴特利特检验 ====================
kmo_med <- psych::KMO(cor(med_items))$MSA
kmo_res <- psych::KMO(cor(res_items))$MSA

# ==================== 十二、输出结果表格 ====================
cat("\n========== 数据模拟完成 ==========\n")
cat(sprintf("样本量：%d\n", n))
cat(sprintf("服药依从性 Cronbach's α: %.3f\n", med_alpha))
cat(sprintf("服药依从性 AVE: %.3f\n", med_ave))
cat(sprintf("心理弹性 Cronbach's α: %.3f\n", res_alpha))
cat(sprintf("心理弹性 AVE: %.3f\n", res_ave))
cat(sprintf("模型 CFI: %.3f\n", fit_indices["cfi"]))
cat(sprintf("模型 TLI: %.3f\n", fit_indices["tli"]))
cat(sprintf("模型 RMSEA: %.3f\n", fit_indices["rmsea"]))
cat("==================================\n\n")

# ==================== 十三、保存数据 ====================
# 保存为 SPSS 格式
haven::write_sav(data, "C:\\Users\\Mr Zhou\\.openclaw\\workspace\\分析结果\\高血压问卷数据.sav")

# 保存为 Excel 格式
wb <- createWorkbook()
addWorksheet(wb, "原始数据")
writeData(wb, "原始数据", data)
addWorksheet(wb, "信度分析")
writeData(wb, "信度分析", data.frame(
  量表 = c("服药依从性", "心理弹性"),
  Cronbach_α = c(med_alpha, res_alpha),
  平均相关 = c(med_avr, res_avr),
  AVE = c(med_ave, res_ave),
  CR = c(med_cr, res_cr)
))
addWorksheet(wb, "模型拟合度")
writeData(wb, "模型拟合度", data.frame(
  指标 = names(fit_indices),
  数值 = unname(fit_indices)
))
saveWorkbook(wb, "C:\\Users\\Mr Zhou\\.openclaw\\workspace\\分析结果\\高血压问卷数据.xlsx", overwrite = TRUE)

# 保存为 DAT 格式
write.table(data, "C:\\Users\\Mr Zhou\\.openclaw\\workspace\\分析结果\\高血压问卷数据.dat", 
            sep = "\t", row.names = FALSE, fileEncoding = "UTF-8")

cat("数据已保存至：分析结果/\n")
cat("  - 高血压问卷数据.sav\n")
cat("  - 高血压问卷数据.xlsx\n")
cat("  - 高血压问卷数据.dat\n")
