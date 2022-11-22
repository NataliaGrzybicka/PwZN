import requests
from bs4 import BeautifulSoup
import argparse
import json

parser = argparse.ArgumentParser()  #argumenty

parser.add_argument('-json', '--plik_json', default = 'dane_www')

args = parser.parse_args()

output_file = args.plik_json    #pobranie nazwy pliku wyjsciowego

producs_list = [] # pusta lista na charmsy

req = requests.get('https://pl.pandora.net/pl/charmsy-i-bransoletki/charmsy/', headers={'User-Agent': 'Mozilla/5.0'})    #wywolanie strony, z ktorej pobierane beda dane

print(req.status_code)

if(req.status_code==200):  #sprawdzdenie statusu polaczenia, 200 oznacza ok
    print('Polaczono poprawnie')

    soup = BeautifulSoup(req.text, 'html.parser') #parsowanie strony przez piekna zupe

    charms = soup.find('div', {'class': 'search-result-content'}) #znajduje pojemnik, w ktorym sa wszystkie charmsy

    for charm in charms.find_all('li', {'class': 'SearchGrid__tile grid-tile js-grid-tile'}): # znajduje jednego charmsa
        info = charm.find('div', {'class': 'product-tile-info-group'}) # znajduje pojemnik na nazwe i cene charmsa
        name = info.find('a') # w tym pojemniku znajduje nazwe chamsa
        price = info.find('span') # znajduje tez cene charmsa

        gift = str(name.text.strip())
         
        price = str(price.text.strip())

        producs_list.append((gift, price))   #dodaje do listy tupla z charmsem i jego cena


    with open(str(output_file)+'.json','w', encoding="utf8") as f:     #zapis listy charmsow z cenami do pliku .json
        json.dump(producs_list, f, ensure_ascii=False, indent=4)