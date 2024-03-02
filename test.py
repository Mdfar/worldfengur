from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import time
import pandas as pd

chrome_options = Options();
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
try:
    driver = webdriver.Chrome(options = chrome_options, service=ChromeService(ChromeDriverManager().install()))
except:
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

username = 'gudjong'
password = 'alendis'
wait = WebDriverWait(driver, 40)
driver.get("https://www.worldfengur.com/login.jsp")
work = driver.find_element(By.TAG_NAME, 'h1').text
if work == "WORLDFENGUR":
    print("Pass")

