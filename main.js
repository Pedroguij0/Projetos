const { app, BrowserWindow, ipcMain, shell, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn, execFile } = require('child_process');
const os = require('os');

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

let mainWindow;
let screenshotDir;

app.whenReady().then(() => {
  screenshotDir = path.join(app.getPath('pictures'), 'BroserAuto Screenshots');
  if (!fs.existsSync(screenshotDir)) {
    fs.mkdirSync(screenshotDir, { recursive: true });
  }

  mainWindow = new BrowserWindow({
    width: 560,
    height: 720,
    resizable: false,
    title: 'BroserAuto - Automacao Web',
    backgroundColor: '#0f1117',
    show: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
});

app.on('window-all-closed', () => {
  app.quit();
});

function sendPowerShellKeys(keys) {
  return new Promise((resolve, reject) => {
    const ps = spawn('powershell.exe', [
      '-NoProfile', '-NonInteractive', '-WindowStyle', 'Hidden',
      '-Command', `Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('${keys.replace(/'/g, "''")}')`
    ]);
    ps.on('close', (code) => code === 0 ? resolve() : reject(new Error(`PowerShell exit code: ${code}`)));
    ps.on('error', reject);
  });
}

ipcMain.handle('get-navegadores', () => {
  return NAVEGADORES.map(n => n.nome);
});

ipcMain.handle('get-sites', () => {
  return SITES.map(s => s.nome);
});

ipcMain.handle('open-browser', async (event, browserNome, url) => {
  const nav = NAVEGADORES.find(n => n.nome === browserNome);
  if (!nav) throw new Error('Navegador nao encontrado');

  if (nav.codigo === 'default') {
    await shell.openExternal(url);
  } else if (fs.existsSync(nav.exe)) {
    spawn(nav.exe, [url], { detached: true });
  } else {
    await shell.openExternal(url);
  }

  return { nav: nav.nome, url };
});

ipcMain.handle('close-browser', async (event, browserNome) => {
  const nav = NAVEGADORES.find(n => n.nome === browserNome);
  if (!nav || !nav.processo) return;

  await new Promise((resolve, reject) => {
    execFile('taskkill', ['/f', '/im', nav.processo], (err) => {
      if (err && !err.message.includes('Nao encontrado')) reject(err);
      else resolve();
    });
  });
});

ipcMain.handle('take-screenshot', async () => {
  const screenshotDesktop = require('screenshot-desktop');
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const filename = `screenshot_${timestamp}.png`;
  const filepath = path.join(screenshotDir, filename);

  const img = await screenshotDesktop({ format: 'png' });
  fs.writeFileSync(filepath, img);

  return { filename, filepath };
});

ipcMain.handle('scroll-down', async () => {
  for (let i = 0; i < 5; i++) {
    await sendPowerShellKeys('{PGDN}');
    await new Promise(r => setTimeout(r, 250));
  }
});

ipcMain.handle('scroll-up', async () => {
  for (let i = 0; i < 5; i++) {
    await sendPowerShellKeys('{PGUP}');
    await new Promise(r => setTimeout(r, 250));
  }
});

ipcMain.handle('type-text', async (event, text) => {
  await sendPowerShellKeys(text.replace(/{/g, '{{}').replace(/}/g, '{}}'));
});

ipcMain.handle('open-url', async (event, browserNome, url) => {
  const nav = NAVEGADORES.find(n => n.nome === browserNome);
  if (!nav) throw new Error('Navegador nao encontrado');

  if (nav.codigo === 'default') {
    await shell.openExternal(url);
  } else if (fs.existsSync(nav.exe)) {
    spawn(nav.exe, [url], { detached: true });
  } else {
    await shell.openExternal(url);
  }
});

ipcMain.handle('open-screenshot-folder', async () => {
  shell.openPath(screenshotDir);
});
