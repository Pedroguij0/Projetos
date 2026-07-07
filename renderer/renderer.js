/* renderer.js — Interface do BroserAuto Web */
(function () {
    const API_BASE = window.location.origin;
    let selectedBrowser = null;
    let selectedSite = null;

    const browserSelect = document.getElementById('browserSelect');
    const siteSelect = document.getElementById('siteSelect');
    const customUrlContainer = document.getElementById('customUrlContainer');
    const customUrlInput = document.getElementById('customUrlInput');
    const statusBar = document.getElementById('statusBar');
    const urlIndicator = document.getElementById('urlIndicator');

    function log(msg, type) {
        statusBar.textContent = msg;
        statusBar.style.color = type === 'error' ? '#ff5f7e' : type === 'success' ? '#3dcf8e' : '#8b93b4';
    }

    async function fetchAPI(endpoint, data) {
        const opts = {
            method: data ? 'POST' : 'GET',
            headers: { 'Content-Type': 'application/json' },
        };
        if (data) opts.body = JSON.stringify(data);
        const res = await fetch(`${API_BASE}${endpoint}`, opts);
        return res.json();
    }

    async function loadSelects() {
        try {
            const browsers = await fetchAPI('/api/navegadores');
            browsers.forEach(b => {
                const opt = document.createElement('option');
                opt.value = b;
                opt.textContent = b;
                browserSelect.appendChild(opt);
            });
            if (browsers.length > 0) {
                browserSelect.value = browsers[0];
                selectedBrowser = browsers[0];
            }
        } catch (e) {
            log('Erro ao carregar navegadores: ' + e.message, 'error');
        }

        try {
            const sites = await fetchAPI('/api/sites');
            sites.forEach(s => {
                const opt = document.createElement('option');
                opt.value = s;
                opt.textContent = s;
                siteSelect.appendChild(opt);
            });
            if (sites.length > 0) {
                siteSelect.value = sites[0];
                selectedSite = sites[0];
            }
        } catch (e) {
            log('Erro ao carregar sites: ' + e.message, 'error');
        }
    }

    browserSelect.addEventListener('change', () => {
        selectedBrowser = browserSelect.value;
    });

    siteSelect.addEventListener('change', () => {
        selectedSite = siteSelect.value;
        customUrlContainer.style.display = selectedSite === 'URL Propria' ? 'block' : 'none';
    });

    document.getElementById('btnOpenBrowser').addEventListener('click', async () => {
        if (!selectedBrowser) { log('Selecione um navegador.', 'error'); return; }
        let url = null;

        if (selectedSite === 'URL Propria') {
            url = customUrlInput.value.trim();
            if (!url) { log('Digite uma URL personalizada.', 'error'); return; }
            if (!url.startsWith('http://') && !url.startsWith('https://')) url = 'https://' + url;
        } else {
            const siteUrls = {
                'YouTube': 'https://www.youtube.com',
                'GitHub': 'https://www.github.com',
                'Google': 'https://www.google.com',
                'Reddit': 'https://www.reddit.com',
                'Wikipedia': 'https://www.wikipedia.org',
                'Stack Overflow': 'https://stackoverflow.com',
                'Twitter / X': 'https://www.x.com',
            };
            url = siteUrls[selectedSite];
        }
        if (!url) { log('URL invalida.', 'error'); return; }

        try {
            const result = await fetchAPI('/api/open-browser', { browser: selectedBrowser, url });
            log(`${selectedBrowser} aberto em: ${url}`, 'success');
            urlIndicator.textContent = url;
        } catch (e) {
            log('Erro ao abrir navegador: ' + e.message, 'error');
        }
    });

    document.getElementById('btnCloseBrowser').addEventListener('click', async () => {
        if (!selectedBrowser) { log('Selecione um navegador.', 'error'); return; }
        try {
            await fetchAPI('/api/close-browser', { browser: selectedBrowser });
            log(`${selectedBrowser} fechado.`, 'success');
            urlIndicator.textContent = 'Nenhuma pagina aberta';
        } catch (e) {
            log('Erro ao fechar navegador: ' + e.message, 'error');
        }
    });

    document.getElementById('btnScreenshot').addEventListener('click', async () => {
        try {
            const result = await fetchAPI('/api/screenshot');
            log(`Screenshot salvo: ${result.filename}`, 'success');
        } catch (e) {
            log('Erro ao capturar screenshot: ' + e.message, 'error');
        }
    });

    document.getElementById('btnScrollDown').addEventListener('click', async () => {
        try {
            await fetchAPI('/api/scroll-down');
            log('Rolou para baixo', 'info');
        } catch (e) {
            log('Erro ao rolar: ' + e.message, 'error');
        }
    });

    document.getElementById('btnScrollUp').addEventListener('click', async () => {
        try {
            await fetchAPI('/api/scroll-up');
            log('Rolou para cima', 'info');
        } catch (e) {
            log('Erro ao rolar: ' + e.message, 'error');
        }
    });

    document.getElementById('btnTypeText').addEventListener('click', async () => {
        const text = prompt('Digite o texto a ser enviado para o navegador:');
        if (!text) return;
        try {
            await fetchAPI('/api/type-text', { text });
            log(`Texto digitado: "${text}"`, 'info');
        } catch (e) {
            log('Erro ao digitar texto: ' + e.message, 'error');
        }
    });

    document.getElementById('btnOpenUrl').addEventListener('click', async () => {
        const url = prompt('Digite a URL para abrir:');
        if (!url) return;
        let fullUrl = url.trim();
        if (!fullUrl.startsWith('http://') && !fullUrl.startsWith('https://')) fullUrl = 'https://' + fullUrl;
        try {
            const result = await fetchAPI('/api/open-url', { browser: selectedBrowser, url: fullUrl });
            log(`URL aberta: ${fullUrl}`, 'success');
            urlIndicator.textContent = fullUrl;
        } catch (e) {
            log('Erro ao abrir URL: ' + e.message, 'error');
        }
    });

    document.getElementById('btnExit').addEventListener('click', async () => {
        try {
            await fetchAPI('/api/shutdown');
            log('Servidor encerrando...', 'info');
            document.body.innerHTML = '<h2 style="color:white;text-align:center;margin-top:50px">Servidor encerrado.</h2>';
        } catch (e) {
            log('Erro ao encerrar: ' + e.message, 'error');
        }
    });

    loadSelects();
})();
