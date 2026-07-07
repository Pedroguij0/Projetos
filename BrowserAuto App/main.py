"""
BroserAuto - Automacao Web (Python)
Traducao completa do server.js para Python.
Toda a logica do backend esta aqui. O frontend (renderer/) continua em HTML/CSS/JS.
"""

import http.server
import json
import os
import sys
import subprocess
import webbrowser
import time
import threading
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime

# ============================================================
# Porta (0 = automatica)
# ============================================================
PORT = int(os.environ.get("PORT", 0))

# ============================================================
# Dados — identicos ao server.js
# ============================================================
NAVEGADORES = [
    {"nome": "Google Chrome",    "exe": r"C:\Program Files\Google\Chrome\Application\chrome.exe",              "codigo": "chrome",  "processo": "chrome.exe"},
    {"nome": "Mozilla Firefox",  "exe": r"C:\Program Files\Mozilla Firefox\firefox.exe",                       "codigo": "firefox", "processo": "firefox.exe"},
    {"nome": "Microsoft Edge",   "exe": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",      "codigo": "edge",    "processo": "msedge.exe"},
    {"nome": "Brave Browser",    "exe": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe", "codigo": "brave",   "processo": "brave.exe"},
    {"nome": "Navegador Padrao", "exe": None,                                                                   "codigo": "default", "processo": None},
]

SITES = [
    {"nome": "YouTube",        "url": "https://www.youtube.com"},
    {"nome": "GitHub",         "url": "https://www.github.com"},
    {"nome": "Google",         "url": "https://www.google.com"},
    {"nome": "Reddit",         "url": "https://www.reddit.com"},
    {"nome": "Wikipedia",      "url": "https://www.wikipedia.org"},
    {"nome": "Stack Overflow", "url": "https://stackoverflow.com"},
    {"nome": "Twitter / X",    "url": "https://www.x.com"},
    {"nome": "URL Propria",    "url": None},
]

MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css":  "text/css; charset=utf-8",
    ".js":   "application/javascript; charset=utf-8",
    ".png":  "image/png",
    ".ico":  "image/x-icon",
    ".svg":  "image/svg+xml",
}

# ============================================================
# Diretorio de screenshots
# ============================================================
SCREENSHOT_DIR = Path.home() / "Pictures" / "BroserAuto Screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# Encontrar pasta renderer/
# ============================================================
def get_render_dir():
    """Procura a pasta renderer/ em varios locais possiveis (compativel com PyInstaller)."""
    candidates = [
        Path(__file__).parent / "renderer",
        Path(sys.executable).parent / "renderer",
        Path.cwd() / "renderer",
    ]
    # PyInstaller extrai arquivos em sys._MEIPASS quando usa --onefile
    if hasattr(sys, "_MEIPASS"):
        candidates.insert(0, Path(sys._MEIPASS) / "renderer")

    for d in candidates:
        if d.is_dir():
            return d
    return Path(__file__).parent / "renderer"


RENDER_DIR = get_render_dir()

# ============================================================
# Helpers — PowerShell
# ============================================================
def run_powershell(script: str) -> str:
    """Executa um script PowerShell e retorna stdout. Lanca excecao em caso de erro."""
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-WindowStyle", "Hidden", "-Command", script],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"PowerShell exit code: {result.returncode}")
    return result.stdout.strip()


def send_keys(keys: str):
    """Envia teclas via SendKeys do Windows Forms."""
    escaped = keys.replace("'", "''")
    run_powershell(
        f"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{escaped}')"
    )


def get_nav(nome: str):
    """Encontra um navegador pelo nome."""
    return next((n for n in NAVEGADORES if n["nome"] == nome), None)


def open_in_browser(nav: dict, url: str):
    """Abre uma URL no navegador especificado."""
    if nav["codigo"] == "default" or not nav["exe"] or not os.path.exists(nav["exe"]):
        # Navegador padrao do sistema
        os.startfile(url)
    else:
        subprocess.Popen(
            [nav["exe"], url],
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW,
            close_fds=True
        )

# ============================================================
# Referencia global ao servidor (para o shutdown)
# ============================================================
_server_instance = None

# ============================================================
# Handler HTTP
# ============================================================
class BroserAutoHandler(http.server.BaseHTTPRequestHandler):
    """Handler que replica exatamente a API do server.js original."""

    # Silencia os logs de cada request no console (opcional — remova para debug)
    def log_message(self, format, *args):
        pass

    # ----------------------------------------------------------
    # CORS
    # ----------------------------------------------------------
    def _set_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    # ----------------------------------------------------------
    # Helpers de resposta
    # ----------------------------------------------------------
    def _json_response(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self._set_cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw)

    # ----------------------------------------------------------
    # OPTIONS (preflight CORS)
    # ----------------------------------------------------------
    def do_OPTIONS(self):
        self.send_response(204)
        self._set_cors()
        self.end_headers()

    # ----------------------------------------------------------
    # GET
    # ----------------------------------------------------------
    def do_GET(self):
        parsed = urlparse(self.path)
        pathname = parsed.path

        # --- API: listar navegadores ---
        if pathname == "/api/navegadores":
            return self._json_response([n["nome"] for n in NAVEGADORES])

        # --- API: listar sites ---
        if pathname == "/api/sites":
            return self._json_response([s["nome"] for s in SITES])

        # --- Arquivos estaticos (renderer/) ---
        self._serve_static(pathname)

    # ----------------------------------------------------------
    # POST
    # ----------------------------------------------------------
    def do_POST(self):
        parsed = urlparse(self.path)
        pathname = parsed.path

        try:
            # --- Abrir navegador ---
            if pathname == "/api/open-browser":
                body = self._read_body()
                nav = get_nav(body.get("browser", ""))
                if not nav:
                    return self._json_response({"error": "Navegador nao encontrado"}, 400)
                open_in_browser(nav, body["url"])
                return self._json_response({"nav": nav["nome"], "url": body["url"]})

            # --- Fechar navegador ---
            if pathname == "/api/close-browser":
                body = self._read_body()
                nav = get_nav(body.get("browser", ""))
                if nav and nav["processo"]:
                    try:
                        subprocess.run(
                            ["taskkill", "/f", "/im", nav["processo"]],
                            capture_output=True, check=False
                        )
                    except Exception:
                        pass
                return self._json_response({"success": True})

            # --- Screenshot ---
            if pathname == "/api/screenshot":
                timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
                filename = f"screenshot_{timestamp}.png"
                filepath = SCREENSHOT_DIR / filename
                escaped_path = str(filepath).replace("\\", "\\\\")

                run_powershell(f"""
                    Add-Type -AssemblyName System.Windows.Forms,System.Drawing
                    $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
                    $bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
                    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
                    $graphics.CopyFromScreen($bounds.X, $bounds.Y, 0, 0, $bounds.Size)
                    $bitmap.Save('{escaped_path}', [System.Drawing.Imaging.ImageFormat]::Png)
                    $graphics.Dispose()
                    $bitmap.Dispose()
                """)

                # Abre o Explorer mostrando o arquivo
                subprocess.Popen(["explorer.exe", f'/select,"{filepath}"'], shell=True)
                return self._json_response({"filename": filename, "filepath": str(filepath)})

            # --- Scroll down ---
            if pathname == "/api/scroll-down":
                for _ in range(5):
                    send_keys("{PGDN}")
                    time.sleep(0.25)
                return self._json_response({"success": True})

            # --- Scroll up ---
            if pathname == "/api/scroll-up":
                for _ in range(5):
                    send_keys("{PGUP}")
                    time.sleep(0.25)
                return self._json_response({"success": True})

            # --- Digitar texto ---
            if pathname == "/api/type-text":
                body = self._read_body()
                text = body.get("text", "")
                # Escapar chaves para o SendKeys
                text = text.replace("{", "{{}")
                text = text.replace("}", "{}}")
                send_keys(text)
                return self._json_response({"success": True})

            # --- Abrir URL (em navegador ja aberto) ---
            if pathname == "/api/open-url":
                body = self._read_body()
                nav = get_nav(body.get("browser", ""))
                if not nav:
                    return self._json_response({"error": "Navegador nao encontrado"}, 400)
                open_in_browser(nav, body["url"])
                return self._json_response({"success": True})

            # --- Shutdown ---
            if pathname == "/api/shutdown":
                self._json_response({"success": True})
                # Encerrar o servidor em outra thread para a resposta ser enviada primeiro
                threading.Thread(target=self._shutdown_server, daemon=True).start()
                return

            # Rota nao encontrada
            self._json_response({"error": "Rota nao encontrada"}, 404)

        except Exception as e:
            print(f"Error: {e}")
            self._json_response({"error": str(e)}, 500)

    # ----------------------------------------------------------
    # Servir arquivos estaticos
    # ----------------------------------------------------------
    def _serve_static(self, pathname: str):
        if pathname == "/":
            file_path = RENDER_DIR / "index.html"
        else:
            # Remover a barra inicial e resolver o caminho
            relative = pathname.lstrip("/")
            file_path = RENDER_DIR / relative

        # Seguranca: impedir path traversal
        try:
            file_path = file_path.resolve()
            if not str(file_path).startswith(str(RENDER_DIR.resolve())):
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"Forbidden")
                return
        except Exception:
            pass

        if not file_path.is_file():
            self.send_response(404)
            self._set_cors()
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        ext = file_path.suffix
        content_type = MIME_TYPES.get(ext, "application/octet-stream")
        data = file_path.read_bytes()

        self.send_response(200)
        self._set_cors()
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # ----------------------------------------------------------
    # Shutdown
    # ----------------------------------------------------------
    @staticmethod
    def _shutdown_server():
        global _server_instance
        time.sleep(0.2)
        if _server_instance:
            _server_instance.shutdown()


# ============================================================
# Iniciar servidor
# ============================================================
def main():
    global _server_instance

    server = http.server.HTTPServer(("localhost", PORT), BroserAutoHandler)
    _server_instance = server
    port = server.server_address[1]

    print()
    print("  BroserAuto - Automacao Web (Python)")
    print("  " + "=" * 30)
    print(f"  URL: http://localhost:{port}")
    print("  Pressione Ctrl+C para encerrar")
    print()

    # Abrir navegador padrao apos meio segundo
    threading.Timer(0.5, lambda: webbrowser.open(f"http://localhost:{port}")).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Servidor encerrado.")
        server.server_close()


if __name__ == "__main__":
    main()
