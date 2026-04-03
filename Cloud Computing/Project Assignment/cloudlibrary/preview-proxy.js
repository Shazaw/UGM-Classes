// Local preview proxy — forwards API to remote server
const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');
const url = require('url');

const REMOTE = 'http://157.230.244.123';
const PORT = 4200;
const STATIC = path.join(__dirname, 'frontend/public');

const MIME = {
  '.html':'text/html','.css':'text/css','.js':'application/javascript',
  '.json':'application/json','.png':'image/png','.jpg':'image/jpeg',
  '.svg':'image/svg+xml','.ico':'image/x-icon','.woff2':'font/woff2',
};

const server = http.createServer((req, res) => {
  const parsed = url.parse(req.url);

  // Proxy API and uploads
  if (parsed.pathname.startsWith('/api') || parsed.pathname.startsWith('/uploads')) {
    const options = { hostname: '157.230.244.123', port: 80, path: req.url, method: req.method, headers: { ...req.headers, host: '157.230.244.123' } };
    const proxy = http.request(options, pr => {
      res.writeHead(pr.statusCode, pr.headers);
      pr.pipe(res);
    });
    proxy.on('error', e => { res.writeHead(502); res.end('Proxy error: ' + e.message); });
    req.pipe(proxy);
    return;
  }

  // Serve SPA — all routes serve index.html
  let filePath = path.join(STATIC, parsed.pathname);
  if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
    filePath = path.join(STATIC, 'index.html');
  }

  const ext = path.extname(filePath);
  fs.readFile(filePath, (err, data) => {
    if (err) { res.writeHead(404); res.end('Not found'); return; }
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'text/plain', 'Cache-Control': 'no-cache' });
    res.end(data);
  });
});

server.listen(PORT, () => console.log(`Preview proxy at http://localhost:${PORT}`));
