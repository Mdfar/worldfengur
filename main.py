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

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options,service=ChromeService(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 40)

username = 'gudjong'
try:
    password = os.environ["SOME_SECRET"]
    driver.get("https://www.worldfengur.com/login.jsp")
    wait.until(EC.visibility_of_element_located((By.NAME, 'userid')))
    driver.find_element("name", 'userid').send_keys(username)
    driver.find_element("name", 'password').send_keys(password)
    driver.find_element("name", "Submit").click()
    driver.get("https://www.worldfengur.com/hross_leita_star.jsp")
    FFIE = 'IS2010286682'
    wait.until(EC.visibility_of_element_located((By.ID, "fnr")))
    driver.find_element("id", 'fnr').send_keys(FFIE)
    driver.find_element("id", 'leita').click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "clsWfDark")))
    fields = driver.find_elements(By.CLASS_NAME, "clsWfDark")
    results = driver.find_elements(By.CLASS_NAME, "clsWfWhite")
    keys = []
    values = []
    for field in fields:
        text = field.text
        keys.append(text)
    for result in results:
        text = result.text
        values.append(text)
    values[7] = values[6]+","+values[7]
    del values[6]
    
    data = []
    header = ['Field','Value']
    for h in range(len(keys)):
        data.append([keys[h],values[h]])
    basic_info = pd.DataFrame(data, columns=header)
    
    assesment = driver.find_elements(By.XPATH,'//*[@id="tab"]/ul/li[3]/a')
    blup = driver.find_elements(By.XPATH,'//*[@id="tab"]/ul/li[5]/a')
    
    for i in range(1):
        asses_urls = assesment[i].get_attribute("href")
        blup_url = blup[i].get_attribute("href")
    driver.get(asses_urls)
    wait.until(EC.visibility_of_element_located((By.XPATH,'//table[2]/tbody/tr[3]/td/table[1]/tbody/tr[1]/th')))
    headers_1 = [header.text for header in driver.find_elements(By.XPATH,'//table[2]/tbody/tr[3]/td/table[1]/tbody/tr[1]/th')]
    data_1 = []
    for row in driver.find_elements(By.XPATH,'//table[2]/tbody/tr[3]/td/table[1]/tbody/tr[position()>1]'):
        row_data = [cell.text for cell in row.find_elements(By.XPATH,".//td")]
        data_1.append(row_data)
    
    headers_2 = [header.text for header in driver.find_elements(By.XPATH,'//table[2]/tbody/tr[3]/td/table[2]/tbody/tr[1]/th')]
    data_2 = []
    for row in driver.find_elements(By.XPATH,'//table[2]/tbody/tr[3]/td/table[2]/tbody/tr[position()>1]'):
        row_data = [cell.text for cell in row.find_elements(By.XPATH,".//td")]
        data_2.append(row_data)
        
    breeding_assessment = pd.DataFrame(data_1, columns=headers_1)
    competition_results = pd.DataFrame(data_2, columns=headers_2)
    
    driver.get(blup_url)
    
    heads = []
    values = []
    data = []
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"clsWfDarkLeft")))
    for row in driver.find_elements(By.XPATH,'//table[2]/tbody/tr[3]/td/table[*]/tbody'):
        head = [cell.text for cell in row.find_elements(By.CLASS_NAME,"clsWfDarkLeft")]
        row_data = [cell.text for cell in row.find_elements(By.CLASS_NAME,"clsWfWhite")]
        for h in head:
            heads.append(h)
        for h in row_data:
            values.append(h)
    del heads[:2]
    
    for i in range(len(heads)):
        data.append([heads[i],values[i]])
    
    header = ['Field','Value']
    blup_evaluation = pd.DataFrame(data, columns=header)
    driver.quit()
    
    #basic_info.to_csv('basic_info.csv', index=False)
    #breeding_assessment.to_csv('breeding_assessment.csv', index=False)
    #competition_results.to_csv('competition_results.csv', index=False)
    #blup_evaluation.to_csv('blup_evaluation.csv', index=False)
except KeyError:
    password = ''
#add waits
private_key_id = os.environ["PRIVATE_KEY_ID"]
private_key = os.environ["PRIVATE_KEY"]
credentials = {
    "type": "service_account",
    "project_id": "ac-gs-api",
    "private_key_id": private_key_id,
    "private_key": private_key,
    "client_email": "python-api@ac-gs-api.iam.gserviceaccount.com",
    "client_id": "100992285732075720915",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/python-api%40ac-gs-api.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}
gc = gspread.service_account_from_dict(credentials)
sh = gc.open('Worldfengur_info')
worksheet = sh.worksheet("Basic_Info")
worksheet.update([basic_info.columns.values.tolist()] + basic_info.values.tolist())
worksheet = sh.worksheet("Breeding_Assessment")
worksheet.update([breeding_assessment.columns.values.tolist()] + breeding_assessment.values.tolist())
worksheet = sh.worksheet("Competition_Results")
worksheet.update([competition_results.columns.values.tolist()] + competition_results.values.tolist())
worksheet = sh.worksheet("Blup_Evaluation")
worksheet.update([blup_evaluation.columns.values.tolist()] + blup_evaluation.values.tolist())
