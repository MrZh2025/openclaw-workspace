import http from 'http';
import https from 'https';

const CONFIG = {
  feishu: 'https://open.feishu.cn/open-apis/bot/v2/hook/8bdf3236-6e2e-486f-a05d-b03d0baadf6f',
  serverchan: 'SCT329453TdRWKJwroLepiHUPHmTAS6cQN',
  qmsg: 'f5c465659019fb1ef5c3221525f30451'
};

const PORT = 9099;

function httpPost(url, payload, contentType = 'application/json') {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const body = typeof payload === 'string' ? payload : JSON.stringify(payload);
    const req = https.request({
      hostname: u.hostname,
      path: u.pathname + u.search,
      method: 'POST',
      headers: {
        'Content-Type': contentType,
        'Content-Length': Buffer.byteLength(body)
      }
    }, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => resolve({ status: res.statusCode, body: data }));
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

function extractMessage(data) {
  if (typeof data === 'string') return data;
  if (data.text) return data.text;
  if (data.content && data.content.text) return data.content.text;
  if (data.message) return data.message;
  if (data.msg) return data.msg;
  if (data.payload && data.payload.text) return data.payload.text;
  return JSON.stringify(data, null, 2);
}

const server = http.createServer((req, res) => {
  if (req.method !== 'POST') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    return res.end('Webhook Forwarder OK');
  }

  let body = '';
  req.on('data', chunk => body += chunk);
  req.on('end', async () => {
    let data;
    try { data = JSON.parse(body); } catch { data = { text: body }; }

    const msg = extractMessage(data);
    const title = msg.substring(0, 30).replace(/\n/g, ' ') + '...';
    const now = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });

    console.log(`[${now}] Received webhook, forwarding to 3 targets...`);

    const results = await Promise.allSettled([
      httpPost(CONFIG.feishu, { msg_type: 'text', content: { text: msg } }),
      httpPost(
        `https://sctapi.ftqq.com/${CONFIG.serverchan}.send`,
        `title=${encodeURIComponent(title)}&desp=${encodeURIComponent(msg)}`,
        'application/x-www-form-urlencoded'
      ),
      httpPost(
        `https://qmsg.zendee.cn/send/${CONFIG.qmsg}`,
        `msg=${encodeURIComponent(msg.substring(0, 500))}`,
        'application/x-www-form-urlencoded'
      )
    ]);

    const summary = results.map((r, i) => {
      const name = ['飞书', '微信', 'QQ'][i];
      return `${name}:${r.status === 'fulfilled' ? r.value.status : 'error'}`;
    }).join(', ');

    console.log(`[${now}] ${summary}`);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ ok: true, summary }));
  });
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`Webhook Forwarder running on http://127.0.0.1:${PORT}`);
  console.log('Targets: 飞书 + 微信(Server酱) + QQ(Qmsg)');
});
