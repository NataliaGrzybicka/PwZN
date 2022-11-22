import argparse
from collections import Counter # do zliczenia slow w array
from ascii_graph import Pyasciigraph

parser = argparse.ArgumentParser()

parser.add_argument('-pl', '--input_file_pl', default = 'Cierpienia_mlodego_Wertera.txt')
parser.add_argument('-en', '--input_file_en', default = 'The_Sorrows_of_Young_Werter.txt')
parser.add_argument('-a', '--liczba_slow', default = 10)
parser.add_argument('-m', '--min_dlugosc', default = 0)

args = parser.parse_args()

print('Ksiazka poddana analizie')
print(args.input_file_pl, ' <- tytul polski')
print(args.input_file_en, ' <- tytul angielski\n')

# definicja funkcji analizujacej zadany plik

def analiza(input, liczba_slow , min_dlugosc):
    # odczytywanie z pliku
    slowa = [] # pusty array na slowa na poczatek

    with open(input, 'r', encoding="utf8") as f:
        for line in f:
            slowa = slowa + line.strip().split(' ') # rozszerzanie listy slow przy kazdej nowej linii


    # usuniecie przecinkow, dwukropkow, kropek itp.
    slowa = [sub.replace(',', '') for sub in slowa]
    slowa = [sub.replace('.', '') for sub in slowa]
    slowa = [sub.replace(':', '') for sub in slowa]
    slowa = [sub.replace('-', '') for sub in slowa]

    # wyrzucenie z listy zbyt krotkich slow
    slowa = [slowo for slowo in slowa if len(slowo)>=int(min_dlugosc)]

    # zliczanie slow
    liczebnosc = list(Counter(slowa).items())

    # sortowanie 
    liczebnosc.sort(key=lambda x: x[1]) # sortowanie rosnaco
    liczebnosc.reverse() # odwrocenie posortowanej listy (czyli teraz jest posortowana malejaco)

    liczebnosc = liczebnosc[0:int(liczba_slow)]

    hist = Pyasciigraph()

    for line in hist.graph('Liczebnosc slow w wersji polskiej', liczebnosc):
        print(line)


#-----------------------------------WERSJA POLSKA------------------------------------------------------
print('\nWersja polska:')
analiza(args.input_file_pl, args.liczba_slow, args.min_dlugosc)


#-----------------------------------WERSJA ANGIELSKA------------------------------------------------------
print('\nWersja angielska')
analiza(args.input_file_en, args.liczba_slow, args.min_dlugosc)