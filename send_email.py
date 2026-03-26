#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQ 邮箱邮件发送脚本
使用前请替换下方的账号和授权码占位符
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# ==================== 配置区域 ====================
# 请替换为你的 QQ 邮箱账号（如：123456789@qq.com）
SENDER_EMAIL = "YOUR_QQ_EMAIL"

# 请替换为你的 QQ 邮箱授权码（不是登录密码！）
SENDER_AUTH_CODE = "YOUR_AUTH_CODE"

# 收件人邮箱
RECEIVER_EMAIL = "469193415@qq.com"

# 邮件主题
SUBJECT = "Openclaw 测试邮件"

# 邮件内容
CONTENT = "123456"
# ================================================


def send_email():
    """发送 QQ 邮件"""
    
    # 检查是否已替换占位符
    if SENDER_EMAIL == "YOUR_QQ_EMAIL":
        print("❌ 错误：请先替换 SENDER_EMAIL 为你的 QQ 邮箱账号！")
        return False
    
    if SENDER_AUTH_CODE == "YOUR_AUTH_CODE":
        print("❌ 错误：请先替换 SENDER_AUTH_CODE 为你的 QQ 邮箱授权码！")
        return False
    
    try:
        # 创建邮件对象
        msg = MIMEText(CONTENT, 'plain', 'utf-8')
        msg['From'] = Header(f"QQ邮箱<{SENDER_EMAIL}>", 'utf-8')
        msg['To'] = Header(RECEIVER_EMAIL, 'utf-8')
        msg['Subject'] = Header(SUBJECT, 'utf-8')
        
        # 连接 SMTP 服务器（SSL 加密）
        print(f"正在连接到 smtp.qq.com:465...")
        server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=10)
        
        # 登录
        print(f"正在登录邮箱：{SENDER_EMAIL}")
        server.login(SENDER_EMAIL, SENDER_AUTH_CODE)
        
        # 发送邮件
        print(f"正在发送邮件至：{RECEIVER_EMAIL}")
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        
        # 关闭连接
        server.quit()
        
        print("✅ 邮件发送成功！")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ 认证失败：请检查邮箱账号和授权码是否正确")
        return False
    except smtplib.SMTPConnectError:
        print("❌ 连接失败：请检查网络连接或 SMTP 服务器设置")
        return False
    except Exception as e:
        print(f"❌ 发送失败：{str(e)}")
        return False


if __name__ == "__main__":
    send_email()
