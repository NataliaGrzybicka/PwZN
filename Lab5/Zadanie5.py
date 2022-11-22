from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

import argparse
import json

parser = argparse.ArgumentParser()  #argumenty

parser.add_argument('-json', '--plik_json', default = 'dane_www')

args = parser.parse_args()

output_file = args.plik_json  

options = Options()
#options.add_argument('--headless') # zeby strona sie nie wyswietlala
options.add_argument('--disable-notifications') # na wyskakujace okienka o pokazywanie powiadomien itp. (ale to nie usuwa np. cookies!)

service = Service('webdriver/chromedriver.exe')
driver = webdriver.Chrome(service = service, options = options)

driver.get('https://www.lot.com/pl/pl') # otwierana strona


# nacisniecie guzika w wyskakujacym okienku

button = driver.find_element(By.CSS_SELECTOR, '#onetrust-accept-btn-handler')
button.click()
time.sleep(5) # wazne !!! pozwolic stronie sie zaladowac po nacisnieciu guzika

loty = []

elements = driver.find_elements( By.CSS_SELECTOR, 'a.price-box') # znalezienie wszystkich lotow dedykowanych dla mnie

for element in elements: # iterowanie sie po lotach dla mnie
    element.find_element
    lot = element.text
    lot_split = lot.splitlines() # lot jest wyszukiwany w formacie nazwa\ndata1\ndata2\n...
    print(lot_split)
    loty.append(lot_split)


# przewijanie w dol

for _ in range(10):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(1)


with open(str(output_file)+'.json','w', encoding="utf8") as f:     #zapis listy lotow dedykowanych dla mnie
        json.dump(loty, f, ensure_ascii=False, indent=4)
        print("Zapisano do pliku json")


time.sleep(1000) # zeby strona nie wylaczyla sie za szybko

driver.close()
