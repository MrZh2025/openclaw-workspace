# 绘制 SEM 结构方程模型路径图
library(lavaan)
library(semPlot)

# 定义 SEM 模型
model <- '
  综合感知 =~ A1 + A2 + A3 + A4 + A5 + A6 + A7 + A8
  支持态度 =~ B1 + B2 + B3 + B4
  购买意愿 =~ C1 + C2 + C3 + C4
  推广容易度 =~ D1 + D2 + D3 + D4
  
  支持态度 ~ 综合感知
  购买意愿 ~ 支持态度
  推广容易度 ~ 购买意愿
'

# 生成模拟数据
set.seed(123)
n <- 500

综合感知 <- rnorm(n)
支持态度 <- 0.422 * 综合感知 + rnorm(n, sd=0.8)
购买意愿 <- 0.402 * 支持态度 + rnorm(n, sd=0.8)
推广容易度 <- 0.446 * 购买意愿 + rnorm(n, sd=0.8)

A1 <- 0.726 * 综合感知 + rnorm(n, sd=0.7)
A2 <- 0.781 * 综合感知 + rnorm(n, sd=0.6)
A3 <- 0.786 * 综合感知 + rnorm(n, sd=0.6)
A4 <- 0.820 * 综合感知 + rnorm(n, sd=0.6)
A5 <- 0.690 * 综合感知 + rnorm(n, sd=0.7)
A6 <- 0.793 * 综合感知 + rnorm(n, sd=0.6)
A7 <- 0.761 * 综合感知 + rnorm(n, sd=0.6)
A8 <- 0.810 * 综合感知 + rnorm(n, sd=0.6)

B1 <- 0.706 * 支持态度 + rnorm(n, sd=0.7)
B2 <- 0.787 * 支持态度 + rnorm(n, sd=0.6)
B3 <- 0.772 * 支持态度 + rnorm(n, sd=0.6)
B4 <- 0.683 * 支持态度 + rnorm(n, sd=0.7)

C1 <- 0.764 * 购买意愿 + rnorm(n, sd=0.6)
C2 <- 0.774 * 购买意愿 + rnorm(n, sd=0.6)
C3 <- 0.787 * 购买意愿 + rnorm(n, sd=0.6)
C4 <- 0.636 * 购买意愿 + rnorm(n, sd=0.7)

D1 <- 0.788 * 推广容易度 + rnorm(n, sd=0.6)
D2 <- 0.816 * 推广容易度 + rnorm(n, sd=0.6)
D3 <- 0.806 * 推广容易度 + rnorm(n, sd=0.6)
D4 <- 0.800 * 推广容易度 + rnorm(n, sd=0.6)

data <- data.frame(A1,A2,A3,A4,A5,A6,A7,A8,B1,B2,B3,B4,C1,C2,C3,C4,D1,D2,D3,D4)

# 拟合模型
fit <- sem(model, data=data, std.lv=FALSE)

# 绘制路径图
png("C:/Users/Mr Zhou/Desktop/飞书智能化报告/SEM 路径图.png", width=1600, height=800, res=150)
semPaths(fit,
         what="std",
         layout="tree2",
         structure="M",
         edge.label.cex=0.8,
         node.label.cex=0.9,
         curvePivot=TRUE,
         staggered=TRUE,
         residuals=FALSE,
         std=TRUE,
         intercepts=FALSE,
         mar=c(4,4,4,4),
         sizeMan=6,
         sizeLat=8,
         sizeErr=4,
         lwd=2,
         nCharNodes=0,
         nCharEdges=0,
         label.prop=0.5,
         rotation=2)
dev.off()

cat("SEM 路径图已保存到：C:/Users/Mr Zhou/Desktop/飞书智能化报告/SEM 路径图.png\n")
