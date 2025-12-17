from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get("https://duckduckgo.com/")

driver.implicitly_wait(4)
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("DKTE College of Engineering ichalkaranji")
search_box.send_keys(Keys.RETURN)
time.sleep(5)

print(driver.title)

driver.quit()
