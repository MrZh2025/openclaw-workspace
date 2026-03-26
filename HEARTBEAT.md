# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

---

## 主动检查任务（每次 heartbeat 轮询）

### 1. 检查紧急邮件
- 查看是否有未读的重要邮件
- 有紧急内容时通知周大爷

### 2. 检查日历（未来 24-48 小时）
- 有即将开始的事件时提醒
- 提前 2 小时提醒会议

### 3. 检查工作区状态
- git 状态检查（有未提交变更时提醒）
- 检查是否有卡住的任务

### 4. 主动询问
- 超过 4 小时无对话时，主动询问是否需要帮助
- 发现周大爷在线但长时间沉默时，温和地 check-in

---

## 轮询频率

- 白天（08:00-23:00）：每 30-60 分钟
- 夜间（23:00-08:00）：每 2-4 小时或静默

---

## 行为准则

- 有重要事情才打扰，不要刷存在感
- 夜间除非紧急否则保持安静
- 主动但不烦人
