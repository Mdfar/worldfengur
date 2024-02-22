from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time
import pandas as pd

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

username = 'gudjong'
password = 'alendis'
#add waits
driver.get("https://www.worldfengur.com/login.jsp")
time.sleep(2)
driver.find_element("name", 'userid').send_keys(username)
# find password input field and insert password as well
driver.find_element("name", 'password').send_keys(password)
# click login button
driver.find_element("name", "Submit").click()
time.sleep(2)

driver.get("https://www.worldfengur.com/hross_leita_star.jsp")
time.sleep(2)
FFIE = 'IS2010286682'
driver.find_element("id", 'fnr').send_keys(FFIE)
driver.find_element("id", 'leita').click()
time.sleep(2)
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

assesment = driver.find_elements(By.XPATH,'//*[@id="tab"]/ul/li[3]/a')
blup = driver.find_elements(By.XPATH,'//*[@id="tab"]/ul/li[5]/a')

for i in range(1):
    asses_urls = assesment[i].get_attribute("href")
    blup_url = blup[i].get_attribute("href")
driver.get(asses_urls)
time.sleep(2)

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
    
Breeding_assessment = pd.DataFrame(data_1, columns=headers_1)
competition_results = pd.DataFrame(data_2, columns=headers_2)

driver.get(blup_url)
time.sleep(2)

heads = []
values = []
data = []
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
