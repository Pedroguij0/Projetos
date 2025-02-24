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
import sys
import pyperclip
   
   

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
driver.get("https://chatgpt.com/")
time.sleep(2)
try:
    disconnected = driver.find_element(By.XPATH,'//*[@id="radix-:rh:"]/div/div/a')
    disconnected.click()
except:
    pass
botao = driver.find_element(By.XPATH,'//*[@id="composer-background"]/div[1]/div/div[1]/div')
py.click(1190, 517)
acoes = ActionChains(driver)
acoes.double_click(botao).perform()
time.sleep(2)
py.write("Defina Revolução francesa\n", interval=0.05)
time.sleep(25)
try:
    down = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/main/div[1]/div[1]/div/div/div/div[4]/button')
    down.click()
except:
    py.click(1911, 890, clicks=15)
    time.sleep(2)
response = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div[1]/div/div/div/article[2]/div/div/div/div/div[2]/div/div/span[1]/button/span')
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
title = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div[1]/div/div/div/article[4]/div/div/div/div/div[2]/div/div/span[1]/button/span')
title.click()
time.sleep(2)
py.hotkey('alt', 'tab')
time.sleep(2)
py.hotkey('ctrl','s')
time.sleep(1)
py.hotkey('ctrl', 'v')
py.press('enter')
print("The summary of the video has been saved on your computer")
