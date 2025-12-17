from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options = chrome_options)

driver.get("https://www.sunbeaminfo.in/internship")

driver.implicitly_wait(10)

table_body = driver.find_element(By.CLASS_NAME, "table")
table_rows = table_body.find_elements(By.TAG_NAME, 'tr')


import pandas as pd
data_list = []


for row in table_rows[1:]: 
    cols = row.find_elements(By.TAG_NAME, 'td')
    info = {
        "sr": cols[0].text,
        "Batch": cols[1].text,
        "Batch duration": cols[2].text,
        "startdate": cols[3].text,
        "end_date": cols[4].text,
        "time": cols[5].text,
        "Fees": cols[6].text,
        "Brochure": cols[7].text
    }
    data_list.append(info)
    print(info)

df = pd.DataFrame(data_list)
df.to_csv("internship_batch_schedules.csv", index=False)

driver.quit()