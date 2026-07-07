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

PORT = int(os.environ.get("PORT", 0))

"""
Lista de navegadores suportados.
Substitua "CAMINHO_DO_SEU_NAVEGADOR" pelo caminho real do executavel.
Ex: Chrome: C:\Program Files\Google\Chrome\Application\chrome.exe
Para descobrir: clique com botao direito no atalho > "Abrir local do arquivo"
"""
NAVEGADORES = [
    {"nome": "Google Chrome",    "exe": "CAMINHO_DO_SEU_NAVEGADOR\\chrome.exe",              "codigo": "chrome",  "processo": "chrome.exe"},
    {"nome": "Mozilla Firefox",  "exe": "CAMINHO_DO_SEU_NAVEGADOR\\firefox.exe",              "codigo": "firefox", "processo": "firefox.exe"},
    {"nome": "Microsoft Edge",   "exe": "CAMINHO_DO_SEU_NAVEGADOR\\msedge.exe",               "codigo": "edge",    "processo": "msedge.exe"},
    {"nome": "Brave Browser",    "exe": "CAMINHO_DO_SEU_NAVEGADOR\\brave.exe",                "codigo": "brave",   "processo": "brave.exe"},
    {"nome": "Navegador Padrao", "exe": None,                                                "codigo": "default", "processo": None},
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

SCREENSHOT_DIR = Path.home() / "Pictures" / "BroserAuto Screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def get_render_dir():
    candidates = [
        Path(__file__).parent / "renderer",
        Path(sys.executable).parent / "renderer",
        Path.cwd() / "renderer",
    ]
    if hasattr(sys, "_MEIPASS"):
        candidates.insert(0, Path(sys._MEIPASS) / "renderer")
    for d in candidates:
        if d.is_dir():
            return d
    return Path(__file__).parent / "renderer"


RENDER_DIR = get_render_dir()


def run_powershell(script):
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-WindowStyle", "Hidden", "-Command", script],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"PowerShell exit code: {result.returncode}")
    return result.stdout.strip()


def send_keys(keys):
    escaped = keys.replace("'", "''")
    run_powershell(
        f"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{escaped}')"
    )


def get_nav(nome):
    return next((n for n in NAVEGADORES if n["nome"] == nome), None)


def open_in_browser(nav, url):
    if nav["codigo"] == "default" or not nav["exe"] or not os.path.exists(nav["exe"]):
        os.startfile(url)
    else:
        subprocess.Popen(
            [nav["exe"], url],
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW,
            close_fds=True
        )


_server_instance = None


class BroserAutoHandler(http.server.BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass

    def _set_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json_response(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self._set_cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw)

    def do_OPTIONS(self):
        self.send_response(204)
        self._set_cors()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        pathname = parsed.path

        if pathname == "/api/navegadores":
            return self._json_response([n["nome"] for n in NAVEGADORES])

        if pathname == "/api/sites":
            return self._json_response([s["nome"] for s in SITES])

        self._serve_static(pathname)

    def do_POST(self):
        parsed = urlparse(self.path)
        pathname = parsed.path

        try:
            if pathname == "/api/open-browser":
                body = self._read_body()
                nav = get_nav(body.get("browser", ""))
                if not nav:
                    return self._json_response({"error": "Navegador nao encontrado"}, 400)
                open_in_browser(nav, body["url"])
                return self._json_response({"nav": nav["nome"], "url": body["url"]})

            if pathname == "/api/close-browser":
                body = self._read_body()
                nav = get_nav(body.get("browser", ""))
                if nav and nav["processo"]:
                    try:
                        subprocess.run(["taskkill", "/f", "/im", nav["processo"]], capture_output=True, check=False)
                    except Exception:
                        pass
                return self._json_response({"success": True})

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

                subprocess.Popen(["explorer.exe", f'/select,"{filepath}"'], shell=True)
                return self._json_response({"filename": filename, "filepath": str(filepath)})

            if pathname == "/api/scroll-down":
                for _ in range(5):
                    send_keys("{PGDN}")
                    time.sleep(0.25)
                return self._json_response({"success": True})

            if pathname == "/api/scroll-up":
                for _ in range(5):
                    send_keys("{PGUP}")
                    time.sleep(0.25)
                return self._json_response({"success": True})

            if pathname == "/api/type-text":
                body = self._read_body()
                text = body.get("text", "")
                text = text.replace("{", "{{}").replace("}", "{}}")
                send_keys(text)
                return self._json_response({"success": True})

            if pathname == "/api/open-url":
                body = self._read_body()
                nav = get_nav(body.get("browser", ""))
                if not nav:
                    return self._json_response({"error": "Navegador nao encontrado"}, 400)
                open_in_browser(nav, body["url"])
                return self._json_response({"success": True})

            if pathname == "/api/shutdown":
                self._json_response({"success": True})
                threading.Thread(target=self._shutdown_server, daemon=True).start()
                return

            self._json_response({"error": "Rota nao encontrada"}, 404)

        except Exception as e:
            print(f"Error: {e}")
            self._json_response({"error": str(e)}, 500)

    def _serve_static(self, pathname):
        if pathname == "/":
            file_path = RENDER_DIR / "index.html"
        else:
            relative = pathname.lstrip("/")
            file_path = RENDER_DIR / relative

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

    @staticmethod
    def _shutdown_server():
        global _server_instance
        time.sleep(0.2)
        if _server_instance:
            _server_instance.shutdown()


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

    threading.Timer(0.5, lambda: webbrowser.open(f"http://localhost:{port}")).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Servidor encerrado.")
        server.server_close()


if __name__ == "__main__":
    main()
