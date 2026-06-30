"""
Arquivo de testes e experimentos para o projeto User Creation Auto.
"""

# === Teste de captura de clique com pynput ===
'''
from pynput import mouse

def on_mouse_click(x, y, button, pressed):
    if pressed:
        print(f'Mouse clicado em ({x}, {y}) com o botão {button}')
        return False

with mouse.Listener(on_click=on_mouse_click) as listener:
    print("Clique em qualquer lugar da tela...")
    listener.join()
'''

# === Teste de calibragem de posições ===
'''
from config import POSICOES_TELA
from webconfig import AutomacaoWeb

automacao = AutomacaoWeb()
automacao.calibrar_posicoes()
for posicao in POSICOES_TELA.values():
    py.click(posicao)
print("Teste de clique concluído.")
'''

# === Teste de screenshot ===
from pathlib import Path
import pyautogui as py

input("\nPressione ENTER para capturar um screenshot de teste...")
caminho = Path("C:/Users/allme/Downloads/errosaqui.png")
py.screenshot(caminho)
print(f"Screenshot salvo em: {caminho}")

variavel_teste = "teste"
print(variavel_teste.upper())