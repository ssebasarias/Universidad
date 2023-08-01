from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Opciones de navegación
options =  webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

driver = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\chromedriver_win32\chromedriver.exe")
driver.get('https://www.elespectador.com/')

""""
button = driver.find_element_by_class("div.Header-BurgerIcon false")
button.click()
time.sleep(5)
"""

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      'div.Header-BurgerIcon false'.replace(' ', '.'))))\
    .click()

search =  driver.find_element_by_name('keywords')
search.send_keys('Economia')
search.send_keys(Keys.ENTER)
time.sleep(5)

driver.quit()