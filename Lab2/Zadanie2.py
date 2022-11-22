#Natalia Grzybicka 305 014
import argparse
import numpy as np
import tqdm
from PIL import Image, ImageDraw
import imageio.v2 as imageio

class Ising: # deklaracja klasy Ising
    def __init__(self, n, j, beta, b, kroki, gestosc): # konstruktor
        self.n = n
        self.j = j
        self.beta = beta
        self.b = b
        self.kroki = kroki
        self.system = np.random.choice([1, -1], size=[self.n, self.n], p=[gestosc, 1-gestosc]) # siatka wypelniona losowo wartosciami +-1, wylosowanie 1 z prawd. gestosc, wylosowanie -1 z prawd. 1-gestosc

    def oblicz_delta_E(self, Sij, Sn): # funkcja obliczajaca zmiane hamiltonianu wywolana spinem S_ij, Sn jest to suma spinow sasiadujacych ze spinem S_ij uwzgledniana w Hamiltonianie 
        return 2 * Sij * (self.b + self.j * Sn)

    def oblicz_magnetyzacje(self): # funkcja obliczajaca magnetyzacje ukladu
        return np.sum(self.system)/(self.n**2) # magnetyzacja to suma wszystkich spinow w siatce podzielona przez liczbe spinow

    def run(self, klatki, gif, txt): # funkcja z symulacja
        img = Image.new('RGB', (2*self.n, 2*self.n), (255, 255, 255)) # mnozenie przez 2 zeby powstajace obrazki byly wieksze
        images = []
        imagesPIL = []
        draw = ImageDraw.Draw(img)

        if txt is not None:
            f = open(str(txt)+'.txt', 'w') # otwarcie pliku do zapisu magnetyzacji
            f.write('krok \t magnetyzacja \n')
        
        for wiersz in range(self.n): # wyrysowanie poczatkowej siatki
            for kolumna in range(self.n):
                if(self.system[wiersz, kolumna] == 1):
                    draw.rectangle((2*wiersz, 2*kolumna, 2*(wiersz+1), 2*(kolumna+1)), (235, 153, 255)) #fioletowy
                else:
                    draw.rectangle((2*wiersz, 2*kolumna, 2*(wiersz+1), 2*(kolumna+1)), (255,255,255)) # bialy

        if klatki is not None: # wyrysowanie poczatkowego stanu siatki
                img.save(str(klatki)+str(0)+'.png')
                images.append(imageio.imread(str(klatki)+str(0)+'.png'))
                imagesPIL.append(img)

        for krok in tqdm.tqdm(range(self.kroki)): # petla po calkowitej liczbie krokow
            img = Image.new('RGB', (2*self.n, 2*self.n), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            for spins in range(self.n*self.n): # wybor spinu tyle razy ile jest spinow w siatce

                i = np.random.randint(self.n) # losowanie dowolnego spinu S_ij (mozna dwa razy wylosowac ten sam spin)
                j = np.random.randint(self.n)

                # suma wszystkich spinow sasiadujacych ze spinem S_ij z uwzglednieniem periodycznych warunkow brzegowych (torus)
                Sn = self.system[(i - 1) % self.n, j] + self.system[(i + 1) % self.n, j] + self.system[i, (j - 1) % self.n] + self.system[i, (j + 1) % self.n]

                dE = self.oblicz_delta_E(self.system[i, j], Sn) # licze zmiane energii dla zmienionego spinu

                if dE < 0 or np.random.random() < np.exp(-dE*self.beta): # jezeli zmiana energii jest ujemna badz wylosowana liczba z przedzialu [0,1] nie miesci sie w prawdopodobienstwie zmiany stanu spinu 
                    self.system[i, j] = -self.system[i, j]

                if(self.system[i,j]==1):
                    draw.rectangle((2*i, 2*j, 2*(i+1), 2*(j+1)), (235, 153, 255)) # fioletowy
                else:
                    draw.rectangle((2*i, 2*j, 2*(i+1), 2*(j+1)), (255,255,255)) # bialy

            if klatki is not None: # wyrysowanie aktualnego stanu siatki
                img.save(str(klatki)+str(krok+1)+'.png')
                images.append(imageio.imread(str(klatki)+str(krok+1)+'.png'))
                imagesPIL.append(img)

            if txt is not None:
                magnetyzacja = self.oblicz_magnetyzacje()
                f.write(str(krok+1) + '\t' + str(magnetyzacja) + '\n')
            
        # wygenerowanie klatek jest konieczne aby wygenerowac animacje gif, ale nie jest konieczne do wygenerowania pliku z magnetyzacja
        if gif is not None:
            #imageio.mimsave(str(gif)+'.gif', images)
            imagesPIL[0].save(str(gif)+'.gif', save_all=True, append_images=imagesPIL[1:], optimize=False, duration=40, loop=0)

        if txt is not None:
            f.close()       

#--------------------------pobranie argumentow od uzytkownika---------------------------------

parser = argparse.ArgumentParser()

parser.add_argument('-n', '--wymiar_siatki', default = 1000)
parser.add_argument('-j', '--calka_wymiany', default = 1)
parser.add_argument('-beta', '--parametr', default =5e5)
parser.add_argument('-b', '--indukcja_magnetyczna', default = 1.9999) 
parser.add_argument('-k', '--liczba_krokow', default = 100)
parser.add_argument('-g', '--gestosc_spinow', default = 0.2)
parser.add_argument('-png', '--nazwa_klatek')
parser.add_argument('-gif', '--nazwa_gif')
parser.add_argument('-txt', '--nazwa_magnetyzacja')

args = parser.parse_args()

N=int(args.wymiar_siatki)
J=args.calka_wymiany
Beta=args.parametr
B=args.indukcja_magnetyczna
K=int(args.liczba_krokow)
G=args.gestosc_spinow

#---------------------------------symulacja w zaleznosci od argumentow podanych przez uzytkownika------------------------------
print('\nRozpoczecie symulacji\n')
print('Po symulacji w folderze powstana nastepujace pliki:')

if args.nazwa_klatek is not None:
    print('Klatki animacji w formacie PNG')
    if args.nazwa_gif is not None:
        print('Plik z animacja w formacie GIF')

if args.nazwa_magnetyzacja is not None:
    print('Plik z magnetyzacja w formacie TXT')

if args.nazwa_klatek is None:
    if args.nazwa_gif is None:
        if args.nazwa_magnetyzacja is None:
            print('-----')
    else: # jesli uzytkownik podal gif ale nie klatki
        if args.nazwa_magnetyzacja is None:
            print('-----')

print('\nPostep symulacji\n')

ising = Ising(N, J, Beta, B, K, G) # obiekt klasy Ising
ising.run(args.nazwa_klatek, args.nazwa_gif, args.nazwa_magnetyzacja)

    