# 腾讯云 OpenClaw 微信接入完整教程

> 周大爷专属教程 · 2026-03-26 更新  
> 🐴💻 牛马 - 笔记本电脑 出品

---

## 📋 目录

1. [接入方式对比](#一接入方式对比)
2. [企业微信机器人（推荐）](#二企业微信机器人推荐)
3. [微信公众号接入](#三微信公众号接入)
4. [个人微信接入（第三方方案）](#四个人微信接入第三方方案)
5. [飞书/钉钉接入](#五飞书钉钉接入)
6. [常见问题排查](#六常见问题排查)

---

## 一、接入方式对比

| 接入方式 | 难度 | 费用 | 稳定性 | 推荐度 |
|----------|------|------|--------|--------|
| **企业微信机器人** | ⭐⭐ | 免费 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **微信公众号（服务号）** | ⭐⭐⭐ | 300 元/年认证费 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **个人微信（WechatFerry）** | ⭐⭐⭐⭐ | 免费 | ⭐⭐⭐ | ⭐⭐⭐ |
| **飞书机器人** | ⭐⭐ | 免费 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **钉钉机器人** | ⭐⭐ | 免费 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**周大爷推荐：企业微信机器人** —— 免费、稳定、官方支持！

---

## 二、企业微信机器人（推荐）

### 2.1 创建企业微信应用

#### 步骤 1：注册企业微信

1. 访问 https://work.weixin.qq.com
2. 点击"立即注册"
3. 填写企业信息（个人可用"个体户"或"工作室"名义）
4. 完成验证（可用个人微信扫码验证）

> 💡 **提示**：个人使用可以创建一个"一人企业"，不需要营业执照。

#### 步骤 2：创建自建应用

1. 登录企业微信管理后台
2. 进入 **应用管理 → 应用 → 创建应用**
3. 填写应用信息：
   - 名称：`牛马助手`（随便取）
   - 图标：选个喜欢的
   - 可见范围：选择你自己

4. 点击"创建"

#### 步骤 3：获取 API 密钥

创建完成后，记下以下信息：

```
企业 ID (CorpID):     wwxxxxxxxxxxxxx
应用 AgentId:         1000001
应用 Secret:          xxxxxxxxxxxxxxxxxxxxxxxx
```

> ⚠️ **重要**：Secret 只显示一次，记得复制保存！

#### 步骤 4：配置可信域名（可选）

如果需要接收消息回调：

1. 进入应用详情页
2. 点击"企业可信 IP"
3. 添加你的腾讯云服务器公网 IP

---

### 2.2 配置 OpenClaw

#### 方式 1：通过 Dashboard 配置

1. 访问 `http://你的服务器 IP:18789`
2. 进入 **插件/技能管理**
3. 搜索并安装 `wechat-work` 或 `企业微信` 插件
4. 填写配置：

```json
{
  "corpId": "wwxxxxxxxxxxxxx",
  "agentId": "1000001",
  "secret": "xxxxxxxxxxxxxxxxxxxxxxx"
}
```

#### 方式 2：手动配置配置文件

SSH 登录服务器，编辑配置文件：

```bash
nano ~/.openclaw/openclaw.json
```

添加企业微信配置：

```json
{
  "wechatWork": {
    "enabled": true,
    "corpId": "wwxxxxxxxxxxxxx",
    "agentId": "1000001",
    "secret": "xxxxxxxxxxxxxxxxxxxxxxx",
    "port": 18791
  }
}
```

保存后重启 OpenClaw：

```bash
openclaw gateway restart
```

---

### 2.3 测试连接

#### 发送测试消息

在服务器执行：

```bash
curl -X POST "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "touser": "@all",
  "msgtype": "text",
  "agentid": 1000001,
  "text": {
    "content": "测试消息"
  }
}'
```

> 需要先用 Secret 获取 ACCESS_TOKEN

#### 在微信中接收消息

1. 打开企业微信 APP
2. 找到你创建的应用（牛马助手）
3. 应该能看到测试消息

---

### 2.4 双向交互（接收 + 发送）

如果需要给机器人发消息并得到回复，需要配置回调：

#### 步骤 1：配置回调 URL

1. 企业微信后台 → 应用 → 接收消息设置
2. 填写：
   - URL: `http://你的服务器 IP:18791/wechat`
   - Token: 自己设一个（如 `openclaw2026`）
   - EncodingAESKey: 点击随机生成

3. 点击"保存"

#### 步骤 2：验证回调

OpenClaw 会自动处理验证请求，如果配置正确，企业微信会显示"验证成功"。

#### 步骤 3：测试对话

在企业微信中给机器人发消息：

```
你好，帮我查一下今天的天气
```

应该能收到回复！

---

## 三、微信公众号接入

> 适合需要服务更多用户的场景

### 3.1 注册微信公众号

1. 访问 https://mp.weixin.qq.com
2. 选择注册 **服务号**（订阅号不支持高级接口）
3. 填写信息并完成认证（300 元/年）

### 3.2 获取 API 凭证

1. 登录公众号后台
2. 进入 **开发 → 基本配置**
3. 获取：
   - 开发者 ID (AppID)
   - 开发者密码 (AppSecret)

### 3.3 配置服务器

1. 在 **开发 → 基本配置** 中
2. 填写服务器配置：
   - URL: `http://你的服务器 IP:18791/wechat-mp`
   - Token: 自己设一个
   - EncodingAESKey: 随机生成

3. 提交验证

### 3.4 OpenClaw 配置

```json
{
  "wechatMP": {
    "enabled": true,
    "appId": "wx_xxxxxxxxxxxxxxxx",
    "appSecret": "xxxxxxxxxxxxxxxxxxxxxxx",
    "token": "openclaw2026",
    "encodingAesKey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "port": 18791
  }
}
```

---

## 四、个人微信接入（第三方方案）

> ⚠️ 注意：个人微信没有官方 API，以下方案存在封号风险，谨慎使用！

### 4.1 WechatFerry 方案（推荐）

WechatFerry 是一个开源的微信机器人框架。

#### 步骤 1：准备 Windows 服务器

个人微信需要 Windows 环境，建议：

- 在腾讯云另开一台 Windows 服务器（约 100 元/月）
- 或者在本地电脑运行

#### 步骤 2：安装 WechatFerry

```powershell
# 克隆项目
git clone https://github.com/lich0821/WeChatFerry.git
cd WeChatFerry

# 安装依赖
pip install -r requirements.txt
```

#### 步骤 3：配置 OpenClaw 桥接

在 OpenClaw 中配置 webhook：

```json
{
  "webhook": {
    "enabled": true,
    "port": 18792,
    "path": "/wcf",
    "handlers": ["wechatferry_handler.py"]
  }
}
```

#### 步骤 4：登录微信

1. 在服务器上登录你的个人微信
2. WechatFerry 会自动拦截消息
3. 转发给 OpenClaw 处理

> ⚠️ **风险提示**：使用第三方工具登录个人微信可能导致账号被封，建议用小号测试！

---

### 4.2 微信云托管方案（官方，但复杂）

腾讯官方提供的方案，需要：

1. 注册微信小程序
2. 使用微信云托管
3. 开发自定义消息处理

**不推荐**：开发成本高，适合企业级应用。

---

## 五、飞书/钉钉接入

### 5.1 飞书机器人（简单好用）

#### 步骤 1：创建飞书应用

1. 访问 https://open.feishu.cn
2. 进入 **开发者后台 → 创建应用**
3. 填写应用信息

#### 步骤 2：获取凭证

- App ID
- App Secret

#### 步骤 3：配置机器人

1. 应用功能 → 机器人
2. 创建机器人
3. 获取 Webhook URL

#### 步骤 4：OpenClaw 配置

```json
{
  "feishu": {
    "enabled": true,
    "appId": "cli_xxxxxxxxxxxxxxxx",
    "appSecret": "xxxxxxxxxxxxxxxxxxxxxxx",
    "webhookUrl": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxx"
  }
}
```

---

### 5.2 钉钉机器人

#### 步骤 1：创建钉钉应用

1. 访问 https://open-dev.dingtalk.com
2. 创建企业内部应用

#### 步骤 2：获取凭证

- AppKey
- AppSecret

#### 步骤 3：OpenClaw 配置

```json
{
  "dingtalk": {
    "enabled": true,
    "appKey": "dingxxxxxxxxxxxxxxx",
    "appSecret": "xxxxxxxxxxxxxxxxxxxxxxx"
  }
}
```

---

## 六、常见问题排查

### 问题 1：企业微信收不到消息

**排查步骤：**

```bash
# 1. 检查 OpenClaw 服务状态
openclaw gateway status

# 2. 查看日志
openclaw gateway logs | grep wechat

# 3. 检查端口是否监听
netstat -tlnp | grep 18791

# 4. 测试 API 调用
curl "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=你的 CorpID&corpsecret=你的 Secret"
```

**可能原因：**
- Secret 配置错误
- 防火墙未放行端口
- 企业微信应用未正确配置可见范围

---

### 问题 2：回调验证失败

**排查步骤：**

1. 检查 URL 是否可访问：
```bash
curl http://你的服务器 IP:18791/wechat
```

2. 检查防火墙：
```bash
# 腾讯云控制台 → 防火墙 → 添加规则
端口：18791  TCP
```

3. 检查 Token 配置是否一致

---

### 问题 3：消息延迟高

**解决方案：**

```bash
# 1. 检查服务器资源
htop

# 2. 检查网络延迟
ping work.weixin.qq.com

# 3. 增加 Swap（如果内存不足）
free -h
```

---

### 问题 4：机器人不回复

**排查清单：**

- [ ] OpenClaw 服务是否运行
- [ ] 模型 API Key 是否配置正确
- [ ] 企业微信回调 URL 是否正确
- [ ] 日志中是否有错误信息

**查看日志：**
```bash
# 实时查看日志
openclaw gateway logs --follow

# 查看最近 100 行
openclaw gateway logs --lines 100
```

---

## 📞 技术支持

遇到问题可以：

1. 查看 OpenClaw 官方文档：https://docs.openclaw.ai
2. 加入 Discord 社区：https://discord.gg/clawd
3. 查看企业微信开发文档：https://open.work.weixin.qq.com

---

## 🎯 快速检查清单

部署完成后，逐项检查：

- [ ] 腾讯云服务器正常运行
- [ ] OpenClaw Dashboard 可访问
- [ ] 企业微信应用创建成功
- [ ] CorpID、Secret 配置正确
- [ ] 防火墙端口已放行
- [ ] 能收到测试消息
- [ ] 机器人能回复消息
- [ ] 配置文件已备份

---

**教程完成！** 🐴💻

周大爷，按这个教程一步步来，保证能把微信接入搞定！有哪里不清楚随时问我～
