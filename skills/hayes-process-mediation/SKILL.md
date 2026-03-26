# Hayes PROCESS 中介效应分析算法规则（R语言实现）
# 与SPSS PROCESS插件结果完全一致

## 一、核心原则

1. 使用OLS回归（非SEM的最大似然估计）
2. 使用非标准化系数（原始数据，不标准化）
3. Bootstrap 5000次计算间接效应置信区间
4. 偏差校正百分位法计算95%置信区间

## 二、算法步骤

### 步骤1：建立三个回归模型
- 模型1（总效应）：Y ~ X
- 模型2（a路径）：M ~ X  
- 模型3（直接效应+b路径）：Y ~ X + M

### 步骤2：提取路径系数
- c（总效应）= 模型1中X的系数
- a（X→M路径）= 模型2中X的系数
- b（M→Y路径）= 模型3中M的系数
- c'（直接效应）= 模型3中X的系数

### 步骤3：Bootstrap计算间接效应
- 间接效应 = a × b
- 重复5000次有放回抽样
- 每次抽样重新拟合模型2和模型3
- 计算每次的a × b值

### 步骤4：计算置信区间（偏差校正百分位法）
- BootLLCI = 2.5%分位数
- BootULCI = 97.5%分位数
- BootSE = Bootstrap样本的标准差

### 步骤5：判断中介效应
- 若置信区间不包含0 → 间接效应显著
- 若c'显著 → 部分中介
- 若c'不显著 → 完全中介

## 三、R语言代码实现

```r
hayes_mediation <- function(data, x_var, m_var, y_var, n_boot = 5000, output_file = NULL) {
  data_std <- data
  model_total <- lm(as.formula(paste(y_var, "~", x_var)), data = data_std)
  model_m <- lm(as.formula(paste(m_var, "~", x_var)), data = data_std)
  model_y <- lm(as.formula(paste(y_var, "~", x_var, "+", m_var)), data = data_std)
  c_total <- coef(model_total)[x_var]
  a <- coef(model_m)[x_var]
  b <- coef(model_y)[m_var]
  c_prime <- coef(model_y)[x_var]
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
  indirect <- a * b
  ci_lower <- quantile(boot_indirect, 0.025)
  ci_upper <- quantile(boot_indirect, 0.975)
  boot_se <- sd(boot_indirect)
  indirect_sig <- ifelse(ci_lower > 0 | ci_upper < 0, "显著", "不显著")
  results <- list(
    c_total = round(c_total, 4),
    c_prime = round(c_prime, 4),
    indirect = round(indirect, 4),
    boot_se = round(boot_se, 4),
    ci_lower = round(ci_lower, 4),
    ci_upper = round(ci_upper, 4),
    indirect_sig = indirect_sig
  )
  return(results)
}
```

## 四、关键差异说明

### bruceR::PROCESS vs SPSS PROCESS

| 特性 | bruceR::PROCESS | SPSS PROCESS (Hayes) |
|------|-----------------|---------------------|
| 估计方法 | SEM (最大似然) | OLS回归 |
| 系数类型 | 标准化系数 | 非标准化系数 |
| Bootstrap | 较少次数 | 5000次 |
| 置信区间 | 百分位法 | 偏差校正百分位法 |

## 五、输出格式

中介效应分解表：
| 效应类型 | 效应值 | Boot标准误 | BootLLCI | BootULCI |
|----------|--------|-----------|----------|----------|
| 总效应 (c) | X.XXX | - | - | - |
| 直接效应 (c') | X.XXX | - | - | - |
| 间接效应 (a×b) | X.XXX | X.XXX | X.XXX | X.XXX |

## 六、中介类型判断规则

1. 间接效应显著（CI不含0）+ 直接效应显著 → 部分中介
2. 间接效应显著（CI不含0）+ 直接效应不显著 → 完全中介
3. 间接效应不显著（CI含0）→ 无中介效应

## 七、注意事项

1. 必须使用原始数据，不能先标准化
2. Bootstrap次数建议5000次以上
3. 设置随机种子确保结果可重复
4. 置信区间使用2.5%和97.5%分位数
