if (location.protocol === 'file:') {
  document.body.innerHTML = '<div style="padding:40px;color:#ff5f7e;font-family:sans-serif">' +
    '<h2>Erro: Abra pelo servidor</h2>' +
    '<p>Nao abra o arquivo HTML direto. Execute primeiro:</p>' +
    '<pre style="background:#1a1d2e;padding:12px;margin:12px 0">node server.js</pre>' +
    '<p>E depois acesse <strong>http://localhost</strong> no navegador.</p>' +
    '</div>';
  throw new Error('Abra pelo servidor local, nao pelo file://');
}

async function apiGet(endpoint) {
  const res = await fetch(`/api${endpoint}`);
  if (!res.ok) throw new Error(`API erro ${res.status}: ${res.statusText}`);
  return res.json();
}

async function apiPost(endpoint, data) {
  const res = await fetch(`/api${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: data ? JSON.stringify(data) : undefined,
  });
  if (!res.ok) throw new Error(`API erro ${res.status}: ${res.statusText}`);
  return res.json();
}

const browserSelect = document.getElementById('browserSelect');
const siteSelect = document.getElementById('siteSelect');
const customUrlContainer = document.getElementById('customUrlContainer');
const customUrlInput = document.getElementById('customUrlInput');
const statusBar = document.getElementById('statusBar');
const urlIndicator = document.getElementById('urlIndicator');

let currentBrowser = null;
let currentUrl = null;

function setStatus(msg, color) {
  statusBar.textContent = msg;
  statusBar.style.color = color || '#8b93b4';
}

function setUrlIndicator(url) {
  urlIndicator.textContent = url ? url : 'Nenhuma pagina aberta';
}

async function init() {
  try {
    const navegadores = await apiGet('/navegadores');
    const sites = await apiGet('/sites');

    navegadores.forEach(n => {
      const opt = document.createElement('option');
      opt.value = n;
      opt.textContent = n;
      browserSelect.appendChild(opt);
    });

    sites.forEach(s => {
      const opt = document.createElement('option');
      opt.value = s;
      opt.textContent = s;
      siteSelect.appendChild(opt);
    });

    siteSelect.addEventListener('change', () => {
      customUrlContainer.style.display = siteSelect.value === 'URL Propria' ? 'block' : 'none';
    });

    setStatus('Pronto — escolha um navegador e site para comecar.', '#3dcf8e');
  } catch (err) {
    setStatus(`Falha ao conectar ao servidor: ${err.message}`, '#ff5f7e');
  }
}

function getUrl() {
  const site = siteSelect.value;
  const siteMap = {
    'YouTube': 'https://www.youtube.com',
    'GitHub': 'https://www.github.com',
    'Google': 'https://www.google.com',
    'Reddit': 'https://www.reddit.com',
    'Wikipedia': 'https://www.wikipedia.org',
    'Stack Overflow': 'https://stackoverflow.com',
    'Twitter / X': 'https://www.x.com',
  };

  if (site === 'URL Propria') {
    let url = customUrlInput.value.trim();
    if (!url || url === 'https://') {
      setStatus('Digite uma URL valida no campo URL Propria.', '#ff5f7e');
      return null;
    }
    if (!url.startsWith('http')) url = 'https://' + url;
    return url;
  }

  return siteMap[site] || null;
}

document.getElementById('btnOpenBrowser').addEventListener('click', async () => {
  const browser = browserSelect.value;
  const url = getUrl();
  if (!url) return;

  setStatus(`Abrindo ${browser} em ${url}...`, '#7c6ff7');

  try {
    const result = await apiPost('/open-browser', { browser, url });
    currentBrowser = result.nav;
    currentUrl = result.url;
    setStatus(`${browser} aberto — ${url}`, '#3dcf8e');
    setUrlIndicator(url);
  } catch (err) {
    setStatus(`Erro: ${err.message}`, '#ff5f7e');
  }
});

document.getElementById('btnCloseBrowser').addEventListener('click', async () => {
  const browser = browserSelect.value;
  setStatus(`Encerrando ${browser}...`, '#ff8c42');

  try {
    await apiPost('/close-browser', { browser });
    currentBrowser = null;
    currentUrl = null;
    setStatus(`${browser} encerrado.`, '#ff8c42');
    setUrlIndicator(null);
  } catch (err) {
    setStatus(`Erro ao fechar: ${err.message}`, '#ff5f7e');
  }
});

document.getElementById('btnScreenshot').addEventListener('click', async () => {
  setStatus('Capturando tela...', '#f5c842');

  try {
    const result = await apiPost('/screenshot');
    setStatus(`Screenshot salvo: ${result.filename}`, '#3dcf8e');
  } catch (err) {
    setStatus(`Erro no screenshot: ${err.message}`, '#ff5f7e');
  }
});

document.getElementById('btnScrollDown').addEventListener('click', async () => {
  setStatus('Rolando para baixo...', '#4d9eff');

  try {
    await apiPost('/scroll-down');
    setStatus('Pagina rolada para baixo.', '#3dcf8e');
  } catch (err) {
    setStatus(`Erro: ${err.message}`, '#ff5f7e');
  }
});

document.getElementById('btnScrollUp').addEventListener('click', async () => {
  setStatus('Rolando para cima...', '#4d9eff');

  try {
    await apiPost('/scroll-up');
    setStatus('Pagina rolada para cima.', '#3dcf8e');
  } catch (err) {
    setStatus(`Erro: ${err.message}`, '#ff5f7e');
  }
});

document.getElementById('btnTypeText').addEventListener('click', async () => {
  const text = prompt('Digite o texto a ser digitado na tela:\n(Voce tera 3 segundos para clicar no campo de destino)');
  if (!text) return;

  setStatus('Digitando em 3 segundos — clique no campo destino!', '#3dcf8e');

  setTimeout(async () => {
    try {
      await apiPost('/type-text', { text });
      setStatus('Texto digitado com sucesso.', '#3dcf8e');
    } catch (err) {
      setStatus(`Erro ao digitar: ${err.message}`, '#ff5f7e');
    }
  }, 3000);
});

document.getElementById('btnOpenUrl').addEventListener('click', async () => {
  const browser = browserSelect.value;
  const url = getUrl();
  if (!url) return;

  setStatus(`Abrindo ${url} no ${browser}...`, '#ff8c42');

  try {
    await apiPost('/open-url', { browser, url });
    currentUrl = url;
    setStatus(`Nova URL aberta: ${url}`, '#3dcf8e');
    setUrlIndicator(url);
  } catch (err) {
    setStatus(`Erro: ${err.message}`, '#ff5f7e');
  }
});

document.getElementById('btnExit').addEventListener('click', async () => {
  if (confirm('Deseja realmente sair do Browser Auto?')) {
    setStatus('Encerrando servidor...', '#ff5f7e');
    try {
      await apiPost('/shutdown');
    } catch (err) {
      setStatus('Servidor encerrado.', '#ff5f7e');
    }
  }
});

init();
