const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { spawn, execFile, exec } = require('child_process');

const PORT = parseInt(process.env.PORT, 10) || 0;

/* Lista de navegadores suportados.
   Substitua "CAMINHO_DO_SEU_NAVEGADOR" pelo caminho real do executavel.
   Ex: Chrome normalmente em C:\Program Files\Google\Chrome\Application\chrome.exe
       Para descobrir: clique com botao direito no atalho > "Abrir local do arquivo" */
const NAVEGADORES = [
  { nome: 'Google Chrome', exe: 'CAMINHO_DO_SEU_NAVEGADOR\\chrome.exe', codigo: 'chrome', processo: 'chrome.exe' },
  { nome: 'Mozilla Firefox', exe: 'CAMINHO_DO_SEU_NAVEGADOR\\firefox.exe', codigo: 'firefox', processo: 'firefox.exe' },
  { nome: 'Microsoft Edge', exe: 'CAMINHO_DO_SEU_NAVEGADOR\\msedge.exe', codigo: 'edge', processo: 'msedge.exe' },
  { nome: 'Brave Browser', exe: 'CAMINHO_DO_SEU_NAVEGADOR\\brave.exe', codigo: 'brave', processo: 'brave.exe' },
  { nome: 'Navegador Padrao', exe: null, codigo: 'default', processo: null },
];

const SITES = [
  { nome: 'YouTube', url: 'https://www.youtube.com' },
  { nome: 'GitHub', url: 'https://www.github.com' },
  { nome: 'Google', url: 'https://www.google.com' },
  { nome: 'Reddit', url: 'https://www.reddit.com' },
  { nome: 'Wikipedia', url: 'https://www.wikipedia.org' },
  { nome: 'Stack Overflow', url: 'https://stackoverflow.com' },
  { nome: 'Twitter / X', url: 'https://www.x.com' },
  { nome: 'URL Propria', url: null },
];

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.png': 'image/png',
  '.ico': 'image/x-icon',
  '.svg': 'image/svg+xml',
};

const screenshotDir = path.join(os.homedir(), 'Pictures', 'BroserAuto Screenshots');

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}
ensureDir(screenshotDir);

function sendPowerShell(script) {
  return new Promise((resolve, reject) => {
    const ps = spawn('powershell.exe', [
      '-NoProfile', '-NonInteractive', '-WindowStyle', 'Hidden',
      '-Command', script
    ], { stdio: ['pipe', 'pipe', 'pipe'] });
    let stdout = '', stderr = '';
    ps.stdout.on('data', d => stdout += d.toString());
    ps.stderr.on('data', d => stderr += d.toString());
    ps.on('close', code => {
      if (code === 0) resolve(stdout.trim());
      else reject(new Error(stderr.trim() || `PowerShell exit code: ${code}`));
    });
    ps.on('error', reject);
  });
}

function sendPowerShellKeys(keys) {
  return sendPowerShell(
    `Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('${keys.replace(/'/g, "''")}')`
  );
}

function getNav(nome) {
  return NAVEGADORES.find(n => n.nome === nome);
}

function serveStatic(res, filePath) {
  const ext = path.extname(filePath);
  const ct = MIME_TYPES[ext] || 'application/octet-stream';
  fs.readFile(filePath, (err, data) => {
    if (err) { res.writeHead(404, { 'Content-Type': 'text/plain' }); res.end('Not Found'); return; }
    res.writeHead(200, { 'Content-Type': ct, 'Cache-Control': 'no-cache, no-store, must-revalidate' });
    res.end(data);
  });
}

function parseBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => { try { resolve(JSON.parse(body)); } catch (e) { reject(new Error('Invalid JSON')); } });
    req.on('error', reject);
  });
}

function json(res, data, status = 200) {
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(data));
}

function getRenderDir() {
  const candidates = [
    path.join(__dirname, 'renderer'),
    path.join(path.dirname(process.execPath), 'renderer'),
    path.join(process.cwd(), 'renderer'),
  ];
  for (const dir of candidates) {
    if (fs.existsSync(dir)) return dir;
  }
  return path.join(__dirname, 'renderer');
}

async function handleRequest(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }

  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const pathname = url.pathname;

  try {
    if (pathname === '/api/navegadores' && req.method === 'GET') {
      return json(res, NAVEGADORES.map(n => n.nome));
    }

    if (pathname === '/api/sites' && req.method === 'GET') {
      return json(res, SITES.map(s => s.nome));
    }

    if (pathname === '/api/open-browser' && req.method === 'POST') {
      const body = await parseBody(req);
      const nav = getNav(body.browser);
      if (!nav) return json(res, { error: 'Navegador nao encontrado' }, 400);
      if (nav.codigo === 'default' || !nav.exe || !fs.existsSync(nav.exe)) {
        exec(`start "" "${body.url}"`);
      } else {
        spawn(nav.exe, [body.url], { detached: true, stdio: 'ignore' });
      }
      return json(res, { nav: nav.nome, url: body.url });
    }

    if (pathname === '/api/close-browser' && req.method === 'POST') {
      const body = await parseBody(req);
      const nav = getNav(body.browser);
      if (!nav || !nav.processo) return json(res, { success: true });
      await new Promise((resolve, reject) => {
        execFile('taskkill', ['/f', '/im', nav.processo], err => {
          if (err && !err.message.includes('Nao encontrado')) reject(err);
          else resolve();
        });
      });
      return json(res, { success: true });
    }

    if (pathname === '/api/screenshot' && req.method === 'POST') {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
      const filename = `screenshot_${timestamp}.png`;
      const filepath = path.join(screenshotDir, filename);
      const escapedPath = filepath.replace(/\\/g, '\\\\');

      await sendPowerShell(`
        Add-Type -AssemblyName System.Windows.Forms,System.Drawing
        $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
        $bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        $graphics.CopyFromScreen($bounds.X, $bounds.Y, 0, 0, $bounds.Size)
        $bitmap.Save('${escapedPath}', [System.Drawing.Imaging.ImageFormat]::Png)
        $graphics.Dispose()
        $bitmap.Dispose()
      `);

      exec(`explorer.exe /select,"${filepath}"`);
      return json(res, { filename, filepath });
    }

    if (pathname === '/api/scroll-down' && req.method === 'POST') {
      for (let i = 0; i < 5; i++) {
        await sendPowerShellKeys('{PGDN}');
        await new Promise(r => setTimeout(r, 250));
      }
      return json(res, { success: true });
    }

    if (pathname === '/api/scroll-up' && req.method === 'POST') {
      for (let i = 0; i < 5; i++) {
        await sendPowerShellKeys('{PGUP}');
        await new Promise(r => setTimeout(r, 250));
      }
      return json(res, { success: true });
    }

    if (pathname === '/api/type-text' && req.method === 'POST') {
      const body = await parseBody(req);
      const text = body.text.replace(/{/g, '{{}').replace(/}/g, '{}}');
      await sendPowerShellKeys(text);
      return json(res, { success: true });
    }

    if (pathname === '/api/open-url' && req.method === 'POST') {
      const body = await parseBody(req);
      const nav = getNav(body.browser);
      if (!nav) return json(res, { error: 'Navegador nao encontrado' }, 400);
      if (nav.codigo === 'default' || !nav.exe || !fs.existsSync(nav.exe)) {
        exec(`start "" "${body.url}"`);
      } else {
        spawn(nav.exe, [body.url], { detached: true, stdio: 'ignore' });
      }
      return json(res, { success: true });
    }

    if (pathname === '/api/shutdown' && req.method === 'POST') {
      json(res, { success: true });
      setTimeout(shutdown, 200);
      return;
    }

    const renderDir = getRenderDir();
    let filePath = pathname === '/' ? path.join(renderDir, 'index.html') : path.join(renderDir, pathname);
    res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
    serveStatic(res, filePath);

  } catch (err) {
    console.error('Error:', err);
    if (!res.headersSent) json(res, { error: err.message }, 500);
  }
}

const server = http.createServer(handleRequest);

function shutdown() {
  console.log('\n  Encerrando servidor...');
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(0), 3000);
}

process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);

server.listen(PORT, () => {
  const port = server.address().port;
  console.log('');
  console.log('  BroserAuto - Automacao Web');
  console.log('  ' + '='.repeat(30));
  console.log(`  URL: http://localhost:${port}`);
  console.log('  Pressione Ctrl+C para encerrar');
  console.log('');
  setTimeout(() => exec(`start "" "http://localhost:${port}"`), 500);
});
