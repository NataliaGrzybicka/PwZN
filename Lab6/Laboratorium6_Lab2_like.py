import numpy as np
import numba
from numba import typed
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
import argparse
import tqdm
from PIL import Image, ImageDraw

#--------------------------pobranie argumentow od uzytkownika---------------------------------

parser = argparse.ArgumentParser()

parser.add_argument('-n', '--wymiar_siatki', default = 1000)
parser.add_argument('-j', '--calka_wymiany', default = 1)
parser.add_argument('-beta', '--parametr', default = 1000)
parser.add_argument('-b', '--indukcja_magnetyczna', default = 5) 
parser.add_argument('-k', '--liczba_krokow', default = 100)
parser.add_argument('-g', '--gestosc_spinow', default = 0.2)
parser.add_argument('-png', '--nazwa_klatek')
parser.add_argument('-gif', '--nazwa_gif')
parser.add_argument('-txt', '--nazwa_magnetyzacja')

args = parser.parse_args()

N = int(args.wymiar_siatki)
J = args.calka_wymiany
Beta = float(args.parametr)
B = args.indukcja_magnetyczna
K = int(args.liczba_krokow)
G = args.gestosc_spinow

png = args.nazwa_klatek
gif = args.nazwa_gif
txt = args.nazwa_magnetyzacja

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

print('\nPostep symulacji\n')

#-------------------------- definicje funkcji-------------------------------------

@numba.njit(numba.int64(numba.int64, numba.int64))
def oblicz_delta_E(Sij, Sn): # funkcja obliczajaca zmiane hamiltonianu wywolana spinem S_ij, Sn jest to suma spinow sasiadujacych ze spinem S_ij uwzgledniana w Hamiltonianie 
        return 2 * Sij * (B + J * Sn)

@numba.njit
def oblicz_magnetyzacje(siatka, N): # funkcja obliczajaca magnetyzacje ukladu
    return np.sum(siatka)/(N**2) # magnetyzacja to suma wszystkich spinow w siatce podzielona przez liczbe spinow

@numba.njit(numba.int32(numba.int32[:,:], numba.int64, numba.int64))
def nastepny_stan_spinu(siatka, i, j): # funkcja mogaca zmodyfikowac stan spinu

    # suma wszystkich spinow sasiadujacych ze spinem S_ij z uwzglednieniem periodycznych warunkow brzegowych (torus)
    Sn = siatka[(i - 1) % N, j] + siatka[(i + 1) % N, j] + siatka[i, (j - 1) % N] + siatka[i, (j + 1) % N]

    dE = oblicz_delta_E(siatka[i, j], Sn) # licze zmiane energii dla zmienionego spinu

    if dE < 0 or np.random.random() < np.exp(-dE*Beta): # jezeli zmiana energii jest ujemna badz wylosowana liczba z przedzialu [0,1] nie miesci sie w prawdopodobienstwie zmiany stanu spinu 
        siatka[i, j] = -siatka[i, j]  

    return siatka[i,j] 

@numba.njit()
def aktualizuj_stan_siatki(siatka, N):

    for _ in range(N*N): # petla po liczbie spinow (mozna kilka razy wylosowac ten sam spin)

            i = np.random.randint(N) # losowanie dowolnego spinu S_ij (mozna dwa razy wylosowac ten sam spin)
            j = np.random.randint(N)

            siatka[i,j] = nastepny_stan_spinu(siatka, i, j) # siatka wejsciowa jest caly czas modyfikowana, dynamika asynchroniczna

def rysuj_siatke(siatka, N, krok):

    img = Image.new('RGB', (2*N, 2*N), (255, 255, 255)) # mnozenie przez 2 zeby powstajace obrazki byly wieksze
    draw = ImageDraw.Draw(img)

    for wiersz in range(N):
            for kolumna in range(N):
                if(siatka[wiersz, kolumna] == 1):
                    draw.rectangle((2*wiersz, 2*kolumna, 2*(wiersz+1), 2*(kolumna+1)), (235, 153, 255)) #fioletowy
                else:
                    draw.rectangle((2*wiersz, 2*kolumna, 2*(wiersz+1), 2*(kolumna+1)), (255,255,255)) # bialy

    if png is not None: # wyrysowanie aktualnego stanu siatki
        img.save(str(png)+str(krok+1)+'.png')
        
    imagesPIL.append(img)


def symulacja(liczba_krokow):
    # siatka wypelniona losowo wartosciami +-1, wylosowanie 1 z prawd. gestosc, wylosowanie -1 z prawd. 1-gestosc
    siatka = np.random.choice([1, -1], size=[N, N], p=[G, 1-G]) 

    stany_siatki = typed.List()
    stany_siatki.append(siatka.copy())

    for krok in tqdm.tqdm(range(liczba_krokow)):

        aktualizuj_stan_siatki(siatka, N)

        stany_siatki.append(siatka.copy())

        rysuj_siatke(siatka, N, krok)

        if txt is not None:
            magnetyzacja = oblicz_magnetyzacje(siatka, N)
            f.write(str(krok+1) + '\t' + str(magnetyzacja) + '\n')

    return stany_siatki

imagesPIL = []

if txt is not None:
    f = open(str(txt)+'.txt', 'w') # otwarcie pliku do zapisu magnetyzacji
    f.write('krok \t magnetyzacja \n')

stany_siatki = symulacja(K)

# wygenerowanie klatek jest konieczne aby wygenerowac animacje gif, ale nie jest konieczne do wygenerowania pliku z magnetyzacja
if gif is not None:
    imagesPIL[0].save(str(gif)+'.gif', save_all=True, append_images=imagesPIL[1:], optimize=False, duration=40, loop=0)

if txt is not None:
    f.close()   