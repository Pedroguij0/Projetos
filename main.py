# -*- coding: utf-8 -*-
import pyautogui as py
from time import sleep
import openpyxl
import pandas as pd
from selenium import webdriver
import keyboard
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os

planilha = pd.read_excel('Vendas.xlsx', engine='openpyxl')
faturamento = planilha[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()
print(faturamento)
print('-' * 40)
qtde_produtos = planilha[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
print(qtde_produtos)
print('-' * 40)
ticket_médio = (faturamento['Valor Final']/ qtde_produtos['Quantidade']).to_frame()
print(round(ticket_médio, 2))
soma_total = ticket_médio.sum().values[0]
print("A soma do ticket médio de todas as lojas acima é de:",round(soma_total, 2))
os.system("taskkill /f /im chrome.exe")
py.alert("Não mexa no PC agora, bocózão")
chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(r"user-data-dir=C:\\Users\\allme\\AppData\\Local\\Google\\Chrome\\User Data")
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.get("https://mail.google.com/mail/u/0/?hl=pt-BR#inbox")
sleep(3)
elemento = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div/div[2]/div[1]/div[1]/div/div')
elemento.click()
py.click(1345,490)
sleep(1)
py.write("user@gmail.com")
sleep(1)
py.press("tab")
sleep(1)
py.press("tab")
sleep(1)
keyboard.write("favor ignore")
sleep(1)
py.press('tab')
sleep(1)
texto = f"Iai\nsegue relatório de vendas(isso eh um teste):\n\nfaturamento:\n{faturamento}\n{'-' * 60}\nQuantidade Vendida:\n{qtde_produtos}\n{'-' * 60}\nTicket Medio:\n{ticket_médio}"
keyboard.write(texto)
sleep(40)
enviar = driver.find_element(By.XPATH, '//*[@id=":bj"]')
enviar.click()
py.alert("Email enviado")