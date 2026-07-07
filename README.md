# BroserAuto — Automacao Web

Aplicacao para automatizar navegadores web no Windows: abrir/fechar navegadores, navegar para URLs, capturar screenshots, rolar paginas e digitar texto — tudo por uma interface web local.

## Funcionalidades

- **Abrir navegador** — Abre o navegador selecionado em um site pre-definido ou URL personalizada
- **Fechar navegador** — Fecha forcadamente o processo do navegador selecionado
- **Screenshot** — Captura a tela inteira e salva em `~/Pictures/BroserAuto Screenshots/`
- **Rolagem** — Simula Page Down / Page Up (5 vezes)
- **Digitar texto** — Envia texto diretamente para a janela ativa via teclado virtual
- **Abrir URL** — Abre uma URL personalizada no navegador atual
- **Encerrar servidor** — Desliga o servidor web local

## Requisitos

- **Windows** 7, 8, 10 ou 11
- **Python 3.6+** (recomendado) — [Download](https://python.org)
  - Pacote extra: `Pillow` (para screenshot via Python)
  - Instale com: `pip install Pillow`
- **Node.js 12+** (alternativa) — [Download](https://nodejs.org)
- Navegadores instalados: Chrome, Firefox, Edge, Brave ou outro

## Como usar

### 1. Configurar caminhos dos navegadores

Antes de usar, voce precisa configurar os caminhos dos executaveis dos navegadores.

**Para descobrir o caminho do seu navegador:**
1. Clique com o botao direito no atalho do navegador (na area de trabalho ou menu iniciar)
2. Selecione **"Abrir local do arquivo"**
3. Copie o caminho completo da pasta
4. Adicione o nome do executavel (`chrome.exe`, `firefox.exe`, etc.)

**Onde configurar:**
- **Se usar Python** (`main.py`): Edite a lista `NAVEGADORES` no topo do arquivo
- **Se usar Node.js** (`server.js`): Edite a constante `NAVEGADORES` no topo do arquivo

Substitua `CAMINHO_DO_SEU_NAVEGADOR` pelo caminho real.

Exemplo:
```python
# Antes:
{'nome': 'Google Chrome', 'exe': 'CAMINHO_DO_SEU_NAVEGADOR\\chrome.exe', ...}
# Depois:
{'nome': 'Google Chrome', 'exe': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', ...}
```

### 2. Iniciar o servidor

Ha tres formas de iniciar:

| Launcher | Descricao |
|---|---|
| `launcher_debug.bat` | Janela de terminal visivel — ideal para desenvolvedores |
| `launcher_script.ps1` | PowerShell com saida colorida |
| `launcher_app.vbs` | Silencioso (sem janela) — executa em segundo plano |

O servidor escolhe automaticamente Python 3 (preferencial) ou Node.js (fallback).

Apos iniciar, o navegador padrao abrira em `http://localhost:PORTA_ALEATORIA`.

### 3. Usar a interface

- Selecione um navegador e um site nos menus
- Clique nos botoes para executar as acoes
- O status e exibido na barra inferior

### 4. Encerrar

- Clique em **"Sair do App"** na interface
- Ou pressione `Ctrl+C` no terminal

## Estrutura do projeto

```
browser-auto-electron - Teste/
├── server.js              # Servidor Node.js
├── main.py                # Servidor Python
├── launcher_debug.bat     # Launcher com terminal (CMD)
├── launcher_script.ps1    # Launcher PowerShell
├── launcher_app.vbs       # Launcher silencioso (VBScript)
├── package.json           # Dependencias Node/Electron
├── build.js               # Script de build
├── renderer/
│   ├── index.html         # Interface HTML
│   ├── style.css          # Estilos
│   └── renderer.js        # Logica do frontend
├── dist/                  # Builds gerados
└── README.md
```

## Screenshots

As capturas de tela sao salvas em:
```
C:\Users\SEU_USUARIO\Pictures\BroserAuto Screenshots\
```

## Build (gerar executavel)

```bash
npm install
npm run build
```

Isso copia todos os arquivos para `dist/` e, se o electron-builder estiver disponivel, gera um executavel portatil.

## Compatibilidade

- **Navegadores suportados:** Google Chrome, Mozilla Firefox, Microsoft Edge, Brave Browser, Navegador Padrao
- **Sites pre-definidos:** YouTube, GitHub, Google, Reddit, Wikipedia, Stack Overflow, Twitter/X
- **Runtime:** Python 3 (nativo) ou Node.js (alternativa)

## Notas

- O servidor escolhe uma porta disponivel automaticamente (porta 0 = porta aleatoria)
- O Navegador Padrao usa o comando `start` do Windows, sem necessidade de caminho
- Screenshot via Python usa `Pillow` + `ctypes`; via Node.js usa PowerShell
