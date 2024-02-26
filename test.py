from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

chrome_options = Options();
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options,service=ChromeService(ChromeDriverManager().install()))

driver.get("https://www.google.com/search?q=python")
headss = driver.find_elements(By.TAG_NAME,"h3")
for head in headss:
    print(head.text)
