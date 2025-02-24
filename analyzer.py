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

sys.stdout.reconfigure(encoding = 'utf8')

def video_download(url, dirct="Video"):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    if not os.path.exists(dirct):
        os.makedirs(dirct)
    safe_title = re.sub(r'[^\w\s-]', '', yt.title).replace(" ", "_")
    archive_dirct = os.path.join(dirct, safe_title + ".mp4")
    stream.download(output_path=dirct, filename = safe_title+".mp4")
    return archive_dirct

def audio_extraction(video_path, audio_path="audio.wav"):
    (
        ffmpeg
        .input(video_path)
        .output(audio_path, format="wav", acodec="pcm_s16le", ar="16000", ac="1")
        .run(overwrite_output=True)
    )
    return audio_path

def audio_transcribe(audio_path):
    print("Loading whisper model...")
    model = whisper.load_model("small").to(torch.device('cpu'))
    print("Trasnscribing audio...")
    result = model.transcribe(audio_path, language="pt", fp16 = False)
    return result["text"]

def summarize_text(transcript): 
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
    py.write(f"Resuma o seguinte texto, sem saudacoes:", interval=0.05)
    pyperclip.copy(transcript)
    py.hotkey('ctrl', 'v')
    time.sleep(2)
    py.press('enter')
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
    return

def video_analyzer(url):
    print("Downloading video....")
    video_path = video_download(url)
    print("Extracting audio...")
    audio_path = audio_extraction(video_path)
    print("Transcribing audio...")
    transcript = audio_transcribe(audio_path)
    print("Final analysis:")
    print(transcript)
    print("Summarizing content...")
    summary = summarize_text(transcript)
    return summary
url = str(input("\nCole a url do vídeo desejado"))
video_analyzer(url)


