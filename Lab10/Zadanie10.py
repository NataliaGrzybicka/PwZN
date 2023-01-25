import requests
from bs4 import BeautifulSoup
import time
from PIL import Image, ImageFilter
from concurrent.futures import ProcessPoolExecutor, as_completed


def pobierz_i_zmodyfikuj(iterator):

    strona = 'http://www.if.pw.edu.pl/~mrow/dyd/wdprir/'        # strona, z której pobieram

    req = requests.get(strona)  # pobieranie strony
    status = req.status_code    # sprawdzenie statusu

    if status==200:
        print("Status = ", status)

    else:
        print("Blad pobrania strony")
    

    soup = BeautifulSoup(req.text,'html.parser')

    for a in soup.find_all('a', href=True):     # wyszukuje a href
        url =  a['href']

        zdjecie = 'img'+str(iterator)   #szukam konkretne obrazki

        if zdjecie in url:
            img = requests.get(url=strona+url, stream=True).content     # tworzenie url


            with open('oryginaly/obrazek'+str(iterator)+'.png', 'wb') as handler:    #zapis obrazu oryginalnego ze strony
                handler.write(img) 
                im = Image.open('oryginaly/obrazek'+str(iterator)+'.png')
                im_bw = im.convert("L") # zrobienie czarno-bialego obrazka
                im_blur = im_bw.filter(ImageFilter.GaussianBlur(radius = 50))  # blurowanie obrazka
                im_blur.save('blury/obrazek_blur'+str(iterator)+'.png')  # zapis nowego obrazka
                print('Zmodyfikowano obraz numer ' + str(iterator))

# bez uzycia watkow

z_watkami = True

if( not z_watkami):

    start = time.time()
    for iterator in range(0, 10):
        pobierz_i_zmodyfikuj(iterator)
    stop = time.time() 

    print(f'Bez wątków: {stop - start = } s')  

# z uzyciem watkow

else:

    if __name__ == '__main__':
        start_watki = time.time()
        with ProcessPoolExecutor(10) as ex:
            for iterator in range(0, 10):
                ex.submit(pobierz_i_zmodyfikuj, iterator)
        stop_watki = time.time() 

        print(f'Z wątkami: {stop_watki - start_watki = } s')  

