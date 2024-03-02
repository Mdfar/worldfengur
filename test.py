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

breeding_data = []
competition_link = []
for asses_urls in assesment_url:
    index = assesment_url.index(asses_urls)
    driver.get(asses_urls)
    wait.until(EC.visibility_of_element_located((By.XPATH,'//table[1]/tbody/tr[1]/td[1]')))
    i = 0
    for para in driver.find_elements(By.XPATH,'//table[2]/tbody/tr[3]/td/p'):
        i+=1
        if para.text == 'No records found':
            continue
        if para.text == 'Breeding assessment':
            path = '//table[2]/tbody/tr[3]/td/table['+str(i)+']'
            breeding_header = [header.text for header in driver.find_elements(By.XPATH,path+'/tbody/tr[1]/th')]
            breeding_header = breeding_header[:-1]
            for row in driver.find_elements(By.XPATH,path+'/tbody/tr[position()>1]'):
                row_data = [cell.text for cell in row.find_elements(By.XPATH,".//td")]
                row_data.insert(0, FEIF_ID[index])
                breeding_data.append(row_data[:-1])
                
        elif para.text == 'Sports and gæðingakeppni competition results':
            path = '//table[2]/tbody/tr[3]/td/table['+ str(i-1)+']'
            for row in driver.find_elements(By.XPATH,path+'/tbody/tr[position()>1]'):
                links = row.find_elements(By.XPATH,".//td[*]/span/a")
                comp_url = links[0].get_attribute("href")
                comp_url = comp_url+'&lang=ENG'
                competition_link.append(comp_url)
            break
breeding_header.insert(0, "FEIF ID")
breeding_assessment = pd.DataFrame(breeding_data, columns=breeding_header)

driver.get(competition_link[0])
wait.until(EC.visibility_of_element_located((By.XPATH,'//form/table[3]/tbody')))
fields = [field.text.strip() for field in driver.find_elements(By.CLASS_NAME, "clsWfDark")]
competition_header = [header.text for header in driver.find_elements(By.XPATH,'//form/table[3]/tbody/tr[1]/th')]
fields.extend(competition_header)
each_comp = []
for link in competition_link:
    driver.get(link)
    wait.until(EC.visibility_of_element_located((By.XPATH,'//form/table[3]/tbody')))
    results = [result.text.strip() for result in driver.find_elements(By.CLASS_NAME, "clsWfWhite")]
    results[0] = results[0].split()[0]
    for row in driver.find_elements(By.XPATH,'//form/table[3]/tbody/tr[position()>1]'):
        add_row = []
        row_data = [cell.text for cell in row.find_elements(By.XPATH,".//td")]
        add_row = results + row_data
        each_comp.append(add_row)
        
competitions_results = pd.DataFrame(each_comp, columns=fields)

bulp_result = []
for blup in blup_url:
    index = blup_url.index(blup)
    driver.get(blup)
    wait.until(EC.visibility_of_element_located((By.XPATH,'//table[2]/tbody/tr[3]/td/table[*]/tbody')))
    head = [cell.text for cell in driver.find_elements(By.CLASS_NAME,"clsWfDarkLeft")]
    row_data = [cell.text for cell in driver.find_elements(By.CLASS_NAME,"clsWfWhite")]
    row_data.insert(0,FEIF_ID[index])
    bulp_result.append(row_data)
header = head[2:]
header.insert(0,"FEIF ID")
blup_evaluation = pd.DataFrame(bulp_result, columns=header)
driver.quit()
