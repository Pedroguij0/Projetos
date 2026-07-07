import http.server
import json
import os
import subprocess
import sys
import tempfile
import threading
import webbrowser
from pathlib import Path
from datetime import datetime

PORT = int(os.environ.get('PORT', 0))

"""
Lista de navegadores suportados.
Substitua "CAMINHO_DO_SEU_NAVEGADOR" pelo caminho real do executavel.
Ex: Chrome: C:\Program Files\Google\Chrome\Application\chrome.exe
    Firefox: C:\Program Files\Mozilla Firefox\firefox.exe
Para descobrir o caminho: clique com botao direito no atalho do navegador > "Abrir local do arquivo"
"""
NAVEGADORES = [
    {'nome': 'Google Chrome', 'exe': 'CAMINHO_DO_SEU_NAVEGADOR\\chrome.exe', 'codigo': 'chrome', 'processo': 'chrome.exe'},
    {'nome': 'Mozilla Firefox', 'exe': 'CAMINHO_DO_SEU_NAVEGADOR\\firefox.exe', 'codigo': 'firefox', 'processo': 'firefox.exe'},
    {'nome': 'Microsoft Edge', 'exe': 'CAMINHO_DO_SEU_NAVEGADOR\\msedge.exe', 'codigo': 'edge', 'processo': 'msedge.exe'},
    {'nome': 'Brave Browser', 'exe': 'CAMINHO_DO_SEU_NAVEGADOR\\brave.exe', 'codigo': 'brave', 'processo': 'brave.exe'},
    {'nome': 'Navegador Padrao', 'exe': None, 'codigo': 'default', 'processo': None},
]

SITES = [
    {'nome': 'YouTube', 'url': 'https://www.youtube.com'},
    {'nome': 'GitHub', 'url': 'https://www.github.com'},
    {'nome': 'Google', 'url': 'https://www.google.com'},
    {'nome': 'Reddit', 'url': 'https://www.reddit.com'},
    {'nome': 'Wikipedia', 'url': 'https://www.wikipedia.org'},
    {'nome': 'Stack Overflow', 'url': 'https://stackoverflow.com'},
    {'nome': 'Twitter / X', 'url': 'https://www.x.com'},
    {'nome': 'URL Propria', 'url': None},
]

screenshot_dir = Path.home() / 'Pictures' / 'BroserAuto Screenshots'
screenshot_dir.mkdir(parents=True, exist_ok=True)


class BroserAutoHandler(http.server.BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self._send_cors()
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        try:
            if self.path == '/api/navegadores':
                return self._json([n['nome'] for n in NAVEGADORES])

            if self.path == '/api/sites':
                return self._json([s['nome'] for s in SITES])

            render_dir = self._get_render_dir()
            if self.path == '/' or self.path == '':
                filepath = render_dir / 'index.html'
            else:
                filepath = render_dir / self.path.lstrip('/')

            if not filepath.exists() or not filepath.is_file():
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Not Found')
                return

            content_type = {
                '.html': 'text/html; charset=utf-8',
                '.css': 'text/css; charset=utf-8',
                '.js': 'application/javascript; charset=utf-8',
                '.png': 'image/png',
                '.ico': 'image/x-icon',
                '.svg': 'image/svg+xml',
            }.get(filepath.suffix, 'application/octet-stream')

            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            with open(filepath, 'rb') as f:
                self.wfile.write(f.read())

        except Exception as e:
            self._json({'error': str(e)}, 500)

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length)) if length > 0 else {}

            if self.path == '/api/open-browser' or self.path == '/api/open-url':
                nav = next((n for n in NAVEGADORES if n['nome'] == body.get('browser')), None)
                if not nav:
                    return self._json({'error': 'Navegador nao encontrado'}, 400)
                url = body.get('url', '')
                if nav['codigo'] == 'default' or not nav['exe'] or not os.path.exists(nav['exe']):
                    webbrowser.open(url)
                else:
                    subprocess.Popen([nav['exe'], url], shell=True)
                return self._json({'nav': nav['nome'], 'url': url})

            if self.path == '/api/close-browser':
                nav = next((n for n in NAVEGADORES if n['nome'] == body.get('browser')), None)
                if nav and nav.get('processo'):
                    subprocess.run(['taskkill', '/f', '/im', nav['processo']],
                                   capture_output=True, text=True)
                return self._json({'success': True})

            if self.path == '/api/screenshot':
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                filename = f'screenshot_{timestamp}.png'
                filepath = screenshot_dir / filename

                import ctypes
                import struct
                user32 = ctypes.windll.user32
                gdi32 = ctypes.windll.gdi32

                width = user32.GetSystemMetrics(0)
                height = user32.GetSystemMetrics(1)
                hdc_screen = user32.GetDC(None)
                hdc_mem = gdi32.CreateCompatibleDC(hdc_screen)
                hbitmap = gdi32.CreateCompatibleBitmap(hdc_screen, width, height)
                gdi32.SelectObject(hdc_mem, hbitmap)
                gdi32.BitBlt(hdc_mem, 0, 0, width, height, hdc_screen, 0, 0, 0x00CC0020)

                from PIL import Image
                bmp_info = ctypes.create_string_buffer(struct.calcsize('I4H4I2H'))
                gdi32.GetObjectA(hbitmap, ctypes.sizeof(bmp_info), ctypes.byref(bmp_info))
                data = ctypes.create_string_buffer(width * height * 4)
                bitmap_bits = ctypes.c_void_p(struct.unpack_from('I', bmp_info, 20)[0])

                if hasattr(gdi32, 'GetDIBits'):
                    bmi = ctypes.create_string_buffer(40 + 256 * 4)
                    ctypes.memset(bmi, 0, 40)
                    struct.pack_into('I', bmi, 0, 40)
                    struct.pack_into('I', bmi, 4, width)
                    struct.pack_into('i', bmi, 8, -height)
                    struct.pack_into('H', bmi, 12, 1)
                    struct.pack_into('H', bmi, 14, 32)
                    gdi32.GetDIBits(hdc_mem, hbitmap, 0, height, data, bmi, 0)

                img = Image.frombuffer('RGBA', (width, height), data, 'raw', 'BGRA', 0, 1)
                img.save(filepath)

                gdi32.DeleteObject(hbitmap)
                gdi32.DeleteDC(hdc_mem)
                user32.ReleaseDC(None, hdc_screen)

                subprocess.Popen(['explorer.exe', '/select,', str(filepath)])
                return self._json({'filename': filename, 'filepath': str(filepath)})

            if self.path == '/api/scroll-down':
                import time
                import ctypes
                for _ in range(5):
                    ctypes.windll.user32.keybd_event(0x22, 0, 0, 0)
                    time.sleep(0.1)
                    ctypes.windll.user32.keybd_event(0x22, 0, 2, 0)
                    time.sleep(0.25)
                return self._json({'success': True})

            if self.path == '/api/scroll-up':
                import time
                import ctypes
                for _ in range(5):
                    ctypes.windll.user32.keybd_event(0x21, 0, 0, 0)
                    time.sleep(0.1)
                    ctypes.windll.user32.keybd_event(0x21, 0, 2, 0)
                    time.sleep(0.25)
                return self._json({'success': True})

            if self.path == '/api/type-text':
                import ctypes
                text = body.get('text', '')
                for char in text:
                    ctypes.windll.user32.keybd_event(ord(char.upper()), 0, 0, 0)
                    ctypes.windll.user32.keybd_event(ord(char.upper()), 0, 2, 0)
                return self._json({'success': True})

            if self.path == '/api/shutdown':
                self._json({'success': True})
                threading.Timer(0.2, self._shutdown).start()
                return

            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

        except Exception as e:
            self._json({'error': str(e)}, 500)

    def _get_render_dir(self):
        candidates = [
            Path(__file__).parent / 'renderer',
            Path(sys.executable).parent / 'renderer',
            Path.cwd() / 'renderer',
        ]
        for d in candidates:
            if d.exists():
                return d
        return Path(__file__).parent / 'renderer'

    def _send_cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _json(self, data, status=200):
        self.send_response(status)
        self._send_cors()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _shutdown(self):
        print('\n  Encerrando servidor...')
        self.server.shutdown()

    def log_message(self, format, *args):
        pass


def main():
    server = http.server.HTTPServer(('', PORT), BroserAutoHandler)
    port = server.server_address[1]

    print('')
    print('  BroserAuto - Automacao Web')
    print('  ' + '=' * 30)
    print(f'  URL: http://localhost:{port}')
    print('  Pressione Ctrl+C para encerrar')
    print('')

    threading.Timer(0.5, lambda: webbrowser.open(f'http://localhost:{port}')).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  Encerrando servidor...')
        server.shutdown()


if __name__ == '__main__':
    main()
