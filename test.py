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

FEIF_ID = ['IS2021187814','IS2011135727']
basics_url = []
assesment_url = []
blup_url = []
lists = [basics_url,assesment_url,blup_url]
path_code = ['hross_skoda','hross_skoda_doma','hross_skoda_kynbotamat']
root_path = 'https://www.worldfengur.com/'
common_ext = '.jsp?lang=ENG&FN='
for ids in FEIF_ID:
    for i in range(3):
        Url_string = root_path+path_code[i]+common_ext+ids
        lists[i].append(Url_string)
username = 'gudjong'
password = 'alendis'
wait = WebDriverWait(driver, 100)
driver.get("https://www.worldfengur.com/login.jsp")
wait.until(EC.visibility_of_element_located(("name", 'userid')))
driver.find_element("name", 'userid').send_keys(username)
driver.find_element("name", 'password').send_keys(password)
driver.find_element("name", "Submit").click()

allresults = []
all_field = []
for base_url in basics_url:
    driver.get(base_url)   
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "clsWfDark")))
    fields = [field.text.strip() for field in driver.find_elements(By.CLASS_NAME, "clsWfDark")]
    fields.insert(7,"Colour Description")
    all_field.append(fields)
    results = [result.text.strip() for result in driver.find_elements(By.CLASS_NAME, "clsWfWhite")]
    allresults.append(results)

unique_items = []
for sublist in all_field:
    for item in sublist:
        if item not in unique_items:
            unique_items.append(item)
items = []
for i, j in zip(all_field,allresults):
    item_dict = []
    for item in unique_items:
        if item in i:
            index = i.index(item)
            item_dict.append(j[index])
        else:
            item_dict.append('')
    items.append(item_dict)
basic_info = pd.DataFrame(items, columns=unique_items)
length = basic_info.shape[0]
print("Length of DataFrame:", length)
