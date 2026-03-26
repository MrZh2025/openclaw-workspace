# 腾讯云 OpenClaw 部署完整教程

> 周大爷专属教程 · 2026-03-26 更新  
> 🐴💻 牛马 - 笔记本电脑 出品  
> 适用：腾讯云轻量应用服务器 (Lighthouse)

---

## 📋 目录

1. [准备工作](#一准备工作)
2. [购买服务器](#二购买服务器)
3. [SSH 登录](#三 ssh 登录)
4. [一键部署脚本](#四一键部署脚本)
5. [配置防火墙](#五配置防火墙)
6. [访问 Dashboard](#六访问 dashboard)
7. [配置 AI 模型](#七配置 ai 模型)
8. [安全加固](#八安全加固)
9. [日常维护](#九日常维护)
10. [常见问题](#十常见问题)

---

## 一、准备工作

### 1.1 注册腾讯云账号

1. 访问 https://cloud.tencent.com
2. 点击右上角"免费注册"
3. 用微信扫码注册
4. 完成实名认证（需要身份证）

### 1.2 准备工具

| 工具 | 用途 | 下载地址 |
|------|------|----------|
| **SSH 客户端** | 连接服务器 | Windows 自带 PowerShell 或 [Termius](https://termius.com) |
| **文本编辑器** | 编辑配置文件 | VS Code / Notepad++ |
| **浏览器** | 访问 Dashboard | Chrome / Edge |

### 1.3 预算说明

| 项目 | 费用 | 备注 |
|------|------|------|
| 腾讯云服务器 | ¥99/年 | 轻量应用服务器 2 核 2G |
| 域名（可选） | ¥55/年 | 用于 HTTPS |
| AI 模型 API | 按量计费 | DeepSeek 约¥1/百万 tokens |
| **首年总计** | **约¥150-200** | 个人使用足够 |

---

## 二、购买服务器

### 2.1 进入购买页面

1. 访问腾讯云轻量应用服务器：https://cloud.tencent.com/product/lighthouse
2. 点击"立即购买"

### 2.2 选择配置

**推荐配置：**

```
套餐类型：轻量应用服务器
CPU/内存：2 核 2GB
系统盘：50GB SSD
带宽：50Mbps
地域：重庆（离泸州最近，延迟<20ms）
镜像：Ubuntu 22.04 LTS
```

> 💡 **提示**：如果有"OpenClaw 应用镜像"直接选，可以省去安装步骤。

### 2.3 购买流程

1. 选择购买时长：**12 个月**（年付更划算）
2. 勾选"自动续费"（可选，避免忘记续费数据丢失）
3. 点击"立即购买"
4. 完成支付

### 2.4 获取服务器信息

购买成功后，在控制台可以看到：

```
公网 IP：123.123.123.123
用户名：root
初始密码：（短信发送到你手机）
```

> ⚠️ **重要**：把 IP 和密码记下来！

---

## 三、SSH 登录

### 3.1 Windows PowerShell 登录

1. 按 `Win + R`，输入 `powershell`，回车
2. 执行命令：

```powershell
ssh root@你的服务器公网 IP
```

3. 第一次连接会提示确认，输入 `yes`
4. 输入密码（输入时不显示，正常）
5. 首次登录会要求修改密码，设置一个复杂的

### 3.2 使用密钥登录（推荐）

更安全的方式是用 SSH 密钥：

#### 步骤 1：生成密钥（本地电脑执行）

```powershell
ssh-keygen -t ed25519 -C "openclaw@zhou"
```

按回车接受默认路径，设置一个密码短语（可选）。

#### 步骤 2：上传公钥到服务器

```powershell
# 首次用密码登录
ssh root@你的服务器 IP

# 在服务器上执行
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

#### 步骤 3：复制公钥内容

本地执行：
```powershell
Get-Content C:\Users\Mr Zhou\.ssh\id_ed25519.pub
```

复制输出内容，在服务器上执行：
```bash
echo "你的公钥内容" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

#### 步骤 4：密钥登录测试

```powershell
ssh -i C:\Users\Mr Zhou\.ssh\id_ed25519 root@你的服务器 IP
```

---

## 四、一键部署脚本

### 4.1 复制脚本

登录服务器后，创建部署脚本：

```bash
nano deploy-openclaw.sh
```

### 4.2 粘贴以下内容

```bash
#!/bin/bash

# =====================================================
# 腾讯云 OpenClaw 一键部署脚本
# 适用：Ubuntu 22.04 LTS
# 作者：牛马 - 笔记本电脑 🐴💻
# =====================================================

set -e

echo "=========================================="
echo "  腾讯云 OpenClaw 一键部署"
echo "  开始时间：$(date)"
echo "=========================================="

# 1. 配置 Swap
echo ""
echo "=== [1/6] 配置 Swap (4GB) ==="
if [ ! -f /swapfile ]; then
    fallocate -l 4G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
    echo "✓ Swap 配置完成"
else
    echo "✓ Swap 已存在，跳过"
fi

# 2. 更新系统源（腾讯云镜像）
echo ""
echo "=== [2/6] 更新系统源 ==="
sed -i 's/archive.ubuntu.com/mirrors.cloud.tencent.com/g' /etc/apt/sources.list
sed -i 's/security.ubuntu.com/mirrors.cloud.tencent.com/g' /etc/apt/sources.list
apt update -y
echo "✓ 系统源更新完成"

# 3. 安装必要工具
echo ""
echo "=== [3/6] 安装必要工具 ==="
apt install -y curl git wget net-tools htop vim
echo "✓ 工具安装完成"

# 4. 安装 Node.js 22
echo ""
echo "=== [4/6] 安装 Node.js 22 ==="
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt-get install -y nodejs
echo "Node.js 版本：$(node --version)"
echo "npm 版本：$(npm --version)"
echo "✓ Node.js 安装完成"

# 5. 安装 OpenClaw
echo ""
echo "=== [5/6] 安装 OpenClaw ==="
npm config set registry https://registry.npmmirror.com
npm install -g openclaw@latest
echo "OpenClaw 版本：$(openclaw --version)"
echo "✓ OpenClaw 安装完成"

# 6. 初始化配置
echo ""
echo "=== [6/6] 初始化配置 ==="
echo "请按照提示完成配置："
echo "1. 用 GitHub 账号登录"
echo "2. 选择 AI 模型提供商"
echo "3. 输入 API Key"
echo ""
read -p "按回车继续..."
openclaw onboard --install-daemon

# 完成
echo ""
echo "=========================================="
echo "  🎉 部署完成！"
echo "=========================================="
echo ""
echo "📌 重要信息："
echo "   Dashboard: http://$(curl -s ifconfig.me):18789"
echo "   配置文件：~/.openclaw/openclaw.json"
echo "   技能目录：~/.openclaw/skills/"
echo ""
echo "🔧 常用命令："
echo "   openclaw gateway status   # 查看状态"
echo "   openclaw gateway logs     # 查看日志"
echo "   openclaw dashboard        # 打开面板"
echo ""
echo "部署完成时间：$(date)"
echo "=========================================="
```

### 4.3 执行脚本

```bash
# 给脚本添加执行权限
chmod +x deploy-openclaw.sh

# 执行
./deploy-openclaw.sh
```

### 4.4 按提示完成配置

脚本会引导你：

1. **GitHub 登录**：会显示一个链接，在浏览器打开登录 GitHub 授权
2. **选择模型**：推荐选 DeepSeek 或 通义千问
3. **输入 API Key**：提前去对应平台申请

---

## 五、配置防火墙

### 5.1 腾讯云控制台配置

1. 登录腾讯云控制台：https://console.cloud.tencent.com
2. 进入 **轻量应用服务器 → 我的服务器**
3. 点击你的服务器卡片
4. 进入 **防火墙** 标签页

### 5.2 添加规则

点击"添加规则"，添加以下端口：

| 端口范围 | 协议 | 说明 |
|----------|------|------|
| 18789 | TCP | OpenClaw Dashboard（必选） |
| 22 | TCP | SSH 登录（必选） |
| 18790 | TCP | 邮件发送服务（可选） |
| 18791 | TCP | 微信/企业微信回调（可选） |
| 80 | TCP | HTTP（可选，用于域名访问） |
| 443 | TCP | HTTPS（可选，用于域名访问） |

### 5.3 验证端口

在本地电脑执行：
```powershell
Test-NetConnection 你的服务器 IP -Port 18789
```

显示 `TcpTestSucceeded : True` 表示成功。

---

## 六、访问 Dashboard

### 6.1 打开浏览器

访问：
```
http://你的服务器公网 IP:18789
```

### 6.2 首次登录

1. 用 GitHub 账号登录（和配置时同一个）
2. 进入 Dashboard 主界面

### 6.3 界面说明

```
┌─────────────────────────────────────────┐
│  OpenClaw Dashboard                     │
├─────────────────────────────────────────┤
│  📊 概览      - 服务状态、资源使用      │
│  🤖 模型管理  - 配置 AI 模型             │
│  🧩 技能管理  - 安装/管理 Skills        │
│  💬 会话管理  - 查看历史对话            │
│  ⚙️  设置      - 系统配置               │
└─────────────────────────────────────────┘
```

---

## 七、配置 AI 模型

### 7.1 推荐模型配置

#### DeepSeek（性价比高）

```json
{
  "name": "DeepSeek V3",
  "provider": "deepseek",
  "baseUrl": "https://api.deepseek.com/v1",
  "apiKey": "你的 DeepSeek API Key",
  "models": ["deepseek-chat", "deepseek-coder"],
  "primary": "deepseek-chat"
}
```

**获取 API Key：**
1. 访问 https://platform.deepseek.com
2. 注册/登录
3. 进入 API Keys 页面
4. 创建新 Key

#### 通义千问（阿里云）

```json
{
  "name": "通义千问 Qwen2.5",
  "provider": "dashscope",
  "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
  "apiKey": "你的 DashScope API Key",
  "models": ["qwen-plus", "qwen-turbo"],
  "primary": "qwen-plus"
}
```

**获取 API Key：**
1. 访问 https://dashscope.console.aliyun.com
2. 注册/登录
3. 开通服务
4. 创建 API Key

#### 腾讯混元（腾讯云）

```json
{
  "name": "腾讯混元",
  "provider": "hunyuan",
  "baseUrl": "https://hunyuan.tencentcloudapi.com",
  "apiKey": "你的腾讯云密钥",
  "secretId": "你的 SecretId",
  "models": ["hunyuan-lite", "hunyuan-standard"],
  "primary": "hunyuan-lite"
}
```

**获取密钥：**
1. 访问 https://console.cloud.tencent.com/cam/capi
2. 创建密钥对（SecretId + SecretKey）

---

### 7.2 在 Dashboard 配置

1. 进入 **模型管理**
2. 点击"添加模型"
3. 填写上述配置
4. 点击"测试连接"
5. 保存

---

## 八、安全加固

### 8.1 修改 SSH 端口

```bash
# 备份 SSH 配置
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

# 修改端口（改为 2222）
sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config

# 重启 SSH 服务
systemctl restart sshd

echo "✓ SSH 端口已改为 2222"
echo "⚠️ 下次登录请用：ssh -p 2222 root@你的服务器 IP"
```

### 8.2 安装 Fail2Ban（防暴力破解）

```bash
apt install -y fail2ban
systemctl enable fail2ban
systemctl start fail2ban

# 检查状态
systemctl status fail2ban
```

### 8.3 配置自动更新

```bash
apt install -y unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades
```

### 8.4 创建备份脚本

```bash
cat > /root/backup-openclaw.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/root/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份 OpenClaw 配置
tar -czf $BACKUP_DIR/openclaw_$DATE.tar.gz ~/.openclaw/

# 删除 30 天前的备份
find $BACKUP_DIR -name "openclaw_*.tar.gz" -mtime +30 -delete

echo "备份完成：$BACKUP_DIR/openclaw_$DATE.tar.gz"
EOF

chmod +x /root/backup-openclaw.sh
```

### 8.5 添加定时任务

```bash
# 每天凌晨 3 点自动备份
echo "0 3 * * * /root/backup-openclaw.sh" | crontab -

# 查看定时任务
crontab -l
```

---

## 九、日常维护

### 9.1 常用命令

```bash
# 查看服务状态
openclaw gateway status

# 查看实时日志
openclaw gateway logs --follow

# 重启服务
openclaw gateway restart

# 停止服务
openclaw gateway stop

# 启动服务
openclaw gateway start

# 更新 OpenClaw
npm install -g openclaw@latest
openclaw gateway restart

# 查看资源占用
htop

# 查看磁盘空间
df -h

# 查看内存使用
free -h
```

### 9.2 日志位置

```bash
# OpenClaw 日志
~/.openclaw/logs/

# 系统日志
/var/log/syslog

# Nginx 日志（如果配置了反向代理）
/var/log/nginx/
```

### 9.3 备份恢复

```bash
# 手动备份
/root/backup-openclaw.sh

# 恢复备份（先停止服务）
openclaw gateway stop
tar -xzf /root/backups/openclaw_20260326.tar.gz -C ~/
openclaw gateway start
```

---

## 十、常见问题

### 问题 1：安装时卡住不动

**原因**：内存不足

**解决**：
```bash
# 检查 Swap 是否生效
free -h

# 如果 Swap 为 0，重新配置
swapoff -a
fallocate -l 4G /swapfile
mkswap /swapfile
swapon /swapfile
```

---

### 问题 2：Dashboard 打不开

**排查步骤**：

```bash
# 1. 检查服务状态
openclaw gateway status

# 2. 检查端口监听
netstat -tlnp | grep 18789

# 3. 检查防火墙
# 腾讯云控制台 → 防火墙 → 确认 18789 已放行

# 4. 查看日志
openclaw gateway logs --lines 50
```

---

### 问题 3：API Key 无效

**解决**：

1. 确认 API Key 复制完整（无空格）
2. 确认账户有余额
3. 确认 API 服务已开通
4. 在 Dashboard 重新测试连接

---

### 问题 4：服务器很卡

**排查**：

```bash
# 查看 CPU 使用
top

# 查看内存使用
free -h

# 查看磁盘 IO
iotop

# 查看网络
iftop
```

**优化**：

```bash
# 增加 Swap
fallocate -l 8G /swapfile2
mkswap /swapfile2
swapon /swapfile2

# 清理缓存
apt clean
journalctl --vacuum-time=7d
```

---

### 问题 5：SSH 连不上

**解决**：

```bash
# 1. 检查服务器是否运行
在腾讯云控制台查看服务器状态

# 2. 重启服务器
在腾讯云控制台点击"重启"

# 3. 用 VNC 登录
腾讯云控制台 → 登录 → VNC 登录

# 4. 检查 SSH 服务
systemctl status sshd
systemctl restart sshd
```

---

## 📞 获取帮助

### 官方资源

- OpenClaw 文档：https://docs.openclaw.ai
- OpenClaw Discord：https://discord.gg/clawd
- GitHub 仓库：https://github.com/openclaw/openclaw

### 社区资源

- B 站教程：搜索"OpenClaw 部署"
- 知乎专栏：OpenClaw 实战
- 腾讯云开发者社区

---

## 🎯 部署检查清单

完成后逐项勾选：

- [ ] 腾讯云服务器已购买
- [ ] SSH 可以正常登录
- [ ] 一键部署脚本执行成功
- [ ] Dashboard 可以访问
- [ ] AI 模型配置完成
- [ ] 防火墙端口已放行
- [ ] SSH 端口已修改（安全加固）
- [ ] Fail2Ban 已安装
- [ ] 备份脚本已配置
- [ ] 测试对话成功

---

## 💰 费用总结

| 项目 | 首年 | 次年 | 备注 |
|------|------|------|------|
| 腾讯云服务器 | ¥99 | ¥99 | 轻量应用服务器 |
| 域名（可选） | ¥55 | ¥55 | 用于 HTTPS |
| DeepSeek API | ¥50 | ¥50 | 预估个人使用 |
| **总计** | **¥204** | **¥204** | 约¥17/月 |

---

**教程完成！** 🐴💻

---

*最后更新：2026-03-26*  
*作者：牛马 - 笔记本电脑 🐴💻*  
*适用：OpenClaw 最新版本*
