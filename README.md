# BroserAuto — Automação de Navegador

![Versão](https://img.shields.io/badge/vers%C3%A3o-2.0.0-7c6ff7)
![Plataforma](https://img.shields.io/badge/plataforma-Windows-4d9eff)
![Linguagem](https://img.shields.io/badge/python-3.8%2B-3dcf8e)
![Linguagem](https://img.shields.io/badge/node.js-18%2B-3dcf8e)

**BroserAuto** é uma ferramenta desktop com interface web que permite controlar navegadores automaticamente: abrir, fechar, navegar, capturar tela, rolar páginas e digitar texto — tudo através de uma interface visual moderna e intuitiva.

> ⚡ Disponível em duas versões: **Python** (recomendado) e **Node.js**.

---

## 📋 Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| 🌐 **Abrir Navegador** | Abre o navegador escolhido em um site predefinido ou URL personalizada |
| ❌ **Fechar Navegador** | Encerra completamente o processo do navegador selecionado |
| 📸 **Screenshot** | Captura a tela inteira e salva em `Pictures/BroserAuto Screenshots/` |
| ⬇️ **Rolar para Baixo** | Simula 5 teclas `Page Down` no navegador ativo |
| ⬆️ **Rolar para Cima** | Simula 5 teclas `Page Up` no navegador ativo |
| ⌨️ **Digitar Texto** | Aguarda 3 segundos e digita qualquer texto no campo ativo |
| 🔗 **Abrir URL no Site Atual** | Navega para uma nova URL mantendo o navegador já aberto |
| 🚪 **Sair do App** | Encerra o servidor do BroserAuto |

### Navegadores Suportados

- Google Chrome
- Mozilla Firefox
- Microsoft Edge
- Brave Browser
- Navegador Padrão do Sistema

### Sites Predefinidos

- YouTube, GitHub, Google, Reddit, Wikipedia, Stack Overflow, Twitter / X
- **URL Própria** — digite qualquer endereço personalizado

---

## 🚀 Como Usar

### ✅ Versão Executável (`.exe`) — Recomendado

1. Baixe o arquivo **`Browser_Auto.exe`**
2. Dê um duplo clique para executar
3. O navegador padrão abrirá automaticamente na interface do BroserAuto
4. Pronto! Acesse as funcionalidades pelos botões na tela

> 📌 O executável foi gerado com PyInstaller e não requer Python instalado.

---

### 🐍 Versão Python (código-fonte)

#### Requisitos

- Python 3.8 ou superior
- Windows (para funcionalidades de automação via PowerShell)

#### Execução

```bash
python main.py
```

O servidor inicia em uma porta aleatória e abre automaticamente o navegador na interface.

> 💡 Para usar uma porta específica: `set PORT=8080 && python main.py`

---

### 🟢 Versão Node.js

#### Requisitos

- Node.js 18 ou superior
- Windows

#### Execução

```bash
node server.js
```

---

## 🖥️ Interface — Guia Passo a Passo

### 1. Configuração

1. **Selecione o Navegador** no primeiro menu suspenso
2. **Selecione o Site de destino** no segundo menu
3. Se escolher **"URL Própria"**, digite o endereço completo no campo que aparecerá

### 2. Ações Principais

| Botão | O que faz |
|---|---|
| 🔵 **Abrir Navegador** | Abre o navegador escolhido no site selecionado |
| 🟠 **Fechar Navegador** | Fecha **forçadamente** todo o processo do navegador (taskkill) |
| 🟡 **Screenshot** | Captura a tela inteira e abre o Explorer mostrando o arquivo salvo |
| 🔵 **Rolar para Baixo** | Dá 5 "Page Downs" na página ativa |
| 🔵 **Rolar para Cima** | Dá 5 "Page Ups" na página ativa |
| 🟢 **Digitar Texto** | Abre um prompt para digitar o texto. Clique no campo de destino **dentro de 3 segundos** após confirmar |

### 3. Controle

| Botão | O que faz |
|---|---|
| 🟠 **Abrir URL no Site Atual** | Abre uma nova URL no navegador que já está aberto |
| 🔴 **Sair do App** | Encerra o servidor completamente |

> 📊 A **barra de status** (rodapé) mostra o que está acontecendo em tempo real e a URL atualmente aberta.

---

## 📸 Screenshots

As capturas de tela são salvas automaticamente em:

```
C:\Users\SEU_USUARIO\Pictures\BroserAuto Screenshots\
```

O nome do arquivo segue o padrão: `screenshot_AAAA-MM-DDTHH-MM-SS.png`

Após capturar, o **Windows Explorer** é aberto com o arquivo já selecionado.

---

## 🏗️ Estrutura do Projeto

```
BroserAuto/
├── Browser_Auto.exe       # 🔥 Executável (Python compilado)
├── main.py                # 🐍 Servidor Python (backend)
├── server.js              # 🟢 Servidor Node.js (alternativa)
├── package.json           # Config Node.js
├── renderer/
│   ├── index.html         # Interface web
│   ├── renderer.js        # Lógica do frontend
│   └── style.css          # Estilos dark theme
└── README.md              # Este arquivo
```

---

## 🔧 Gerar o .exe (para desenvolvedores)

Para compilar o `main.py` em executável com PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --add-data "renderer;renderer" --name "Browser_Auto" main.py
```

O arquivo `Browser_Auto.exe` será gerado na pasta `dist/`.

---

## 🛠️ API Endpoints

O servidor expõe os seguintes endpoints HTTP para integração:

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/navegadores` | Lista navegadores disponíveis |
| `GET` | `/api/sites` | Lista sites predefinidos |
| `POST` | `/api/open-browser` | Abre navegador em URL (`{browser, url}`) |
| `POST` | `/api/close-browser` | Fecha navegador (`{browser}`) |
| `POST` | `/api/screenshot` | Captura screenshot da tela |
| `POST` | `/api/scroll-down` | Rola página para baixo |
| `POST` | `/api/scroll-up` | Rola página para cima |
| `POST` | `/api/type-text` | Digita texto (`{text}`) |
| `POST` | `/api/open-url` | Abre URL no navegador atual (`{browser, url}`) |
| `POST` | `/api/shutdown` | Encerra o servidor |

---

## 📝 Notas Técnicas

- **Automação de teclado**: usa `SendKeys` do Windows Forms via PowerShell
- **Screenshot**: captura via `System.Drawing` do .NET via PowerShell
- **Tema escuro**: interface com design moderno em tons de roxo e azul
- **CORS**: habilitado para integração com outras aplicações
- **Porta dinâmica**: o servidor escolhe uma porta aleatória disponível (ou use `PORT`)

---

## 📄 Licença

Este projeto é de uso pessoal e educacional.
