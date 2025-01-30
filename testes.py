from selenium import webdriver
import pyautogui as py
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
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
py.press("tab")
sleep(1)
py.write("favor ignore")
sleep(1)
py.press('tab')
sleep(1)
py.write("Isto é apenas um teste")
sleep(1)
enviar = driver.find_element(By.XPATH, '//*[@id=":bj"]')
enviar.click()
py.alert("Email enviado")