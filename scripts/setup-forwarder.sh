#!/bin/bash
# 一键部署 webhook 转发服务（飞书+微信+QQ）

echo "=== [1/4] 创建 systemd 服务 ==="
cat > /etc/systemd/system/webhook-forwarder.service << 'EOF'
[Unit]
Description=OpenClaw Webhook Forwarder (飞书+微信+QQ)
After=network.target

[Service]
Type=simple
ExecStart=/root/.nvm/versions/node/v22.22.1/bin/node /root/.openclaw/workspace/scripts/webhook-forwarder.mjs
Restart=always
RestartSec=5
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF

echo "=== [2/4] 启动转发服务 ==="
systemctl daemon-reload
systemctl enable webhook-forwarder
systemctl start webhook-forwarder
sleep 2
systemctl status webhook-forwarder --no-pager | head -10

echo "=== [3/4] 更新定时任务 delivery 指向本地转发 ==="
cd /root/.openclaw/cron
cp jobs.json jobs.json.bak
sed -i 's|https://open.feishu.cn/open-apis/bot/v2/hook/8bdf3236-6e2e-486f-a05d-b03d0baadf6f|http://127.0.0.1:9099/forward|g' jobs.json
echo "done"

echo "=== [4/4] 重启 OpenClaw 网关 ==="
openclaw gateway restart

echo ""
echo "=== 部署完成 ==="
echo "转发服务: http://127.0.0.1:9099"
echo "推送目标: 飞书 + 微信(Server酱) + QQ(Qmsg)"
echo ""
echo "测试命令："
echo "curl -X POST http://127.0.0.1:9099/forward -H 'Content-Type: application/json' -d '{\"text\":\"测试推送：飞书+微信+QQ 三端同步\"}'"
