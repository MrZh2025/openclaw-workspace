# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## 📊 数据模拟偏好

- **默认语言**：R 语言
- **特殊情况**：用户明确指定"调节效应"时用 Mplus
- **默认格式**：`.xlsx` (Excel) 或 `.sav` (SPSS)
- **保存路径**：
  - 用户指定路径 → 按用户指定保存
  - 未指定 → `C:\Users\Mr Zhou\.openclaw\workspace\分析结果\`
- **适用场景**：SEM 模拟数据、统计分析数据
- **原因**：方便直接导入 AMOS/SPSS 分析

## 📄 分析报告格式

- **默认格式**：`.docx` (Word)
- **语言**：中文报告
- **风格**：去 AI 化（自然学术语言，无机器痕迹）
- **表格**：三线表格式
- **规范**：带表题、表注，符合论文格式
- **禁止**：不输出 .md 格式报告
- **报告内容**：不提及使用的编程语言 (R/Python)

## 🛠️ 软件安装路径

```
R:        C:\R\R-4.4.2\bin\x64\Rscript.exe
Mplus:    C:\Program Files\Mplus\Mplus.exe
SPSS:     E:\SPSS\Statistics\27\stats.exe
```

## 📐 SEM 数据模拟技巧

- 增加误差、降低拟合度的方法：
  1. 增加噪点
  2. 添加题目之间的残差相关

## ⚙️ 工作规则

- 回复使用中文
- 不自动创建 md 说明文档
- 任务完成后清理不必要的辅助文件
- 报告必须包含必要的表格

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
