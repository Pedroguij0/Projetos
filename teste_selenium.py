import os
from pytubefix import YouTube
import whisper
import ffmpeg
import re
import torch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui as py
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:\\Users\\allme\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("--profile-directory=Pedro Guilherme")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(service=Service(), options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.maximize_window()
driver.get('https://chatgpt.com')
time.sleep(2)
disconnected = driver.find_element(By.XPATH, '//*[@id="radix-:ra:"]/div/div/a')
disconnected.click()
time.sleep(1)
py.click(627, 451, clicks=2)
prompt= driver.find_element(By.XPATH, '//*[@id="composer-background"]/div[1]/div/div[1]/div')
prompt.click()
time.sleep(2)
py.write("historia do brasil, resumo", interval=0.05)
py.press('enter')
time.sleep(35)
wait = WebDriverWait(driver, 3)
try:
    down = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div[2]/div/div/div/div[3]/button')))
    driver.execute_script("arguments[0].click();", down)
    print("Botão clicado com sucesso!")
except Exception as e:
    print(e)
response = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div[2]/div/div/div/article[2]/div/div/div/div/div[2]/div/div/span[1]/button/span')
response.click()
py.write("Se esse resumo fosse o titulo de um arquivo qualquer, digite como seria o titulo, sem nenhum caracter especial, sem aspas e totalmente breve, pequeno", interval=0.1)
py.press('enter')
time.sleep(5)
py.hotkey('win', 'r')
py.write("notepad", interval=0.1)
py.press('enter')
time.sleep(1)
py.write("segue o resumo:\n", interval=0.1)
time.sleep(2)
py.hotkey('ctrl','v')
time.sleep(2)
py.hotkey('alt', 'tab')
time.sleep(2)
title = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div[2]/div/div/div/article[4]/div/div/div/div/div[2]/div/div/span[1]/button/span')
title.click()
time.sleep(2)
py.hotkey('alt', 'tab')
time.sleep(2)
py.hotkey('ctrl','s')
time.sleep(1)
py.hotkey('ctrl', 'v')
py.press('enter')
time.sleep(1)
py.press('tab')
time.sleep(1)
py.press('enter')
print("The summary of the video has been saved on your computer")

'''p = py.position()
print(p)'''